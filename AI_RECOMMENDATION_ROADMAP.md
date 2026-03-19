# AI 인재 추천 기능 — 검증 로드맵

> Notion `Vector Database Collection` 설계 스펙 기준.
> 벡터 DB(Upstash)에 데이터를 **한 번 적재하고 재활용**하는 것을 전제로,
> Phase별로 src 구현 → notebook 검증 순서로 진행한다.

---

## 현재 상태 (AS-IS)

| 구분 | 상태 |
|------|------|
| `notebooks/phase1/01_embedding_quality.ipynb` | **완료** (Gemini 768차원 품질, 인메모리) |
| `notebooks/phase1/02_dual_vector_quality.ipynb` | **완료** (듀얼 벡터 분리 효과, 인메모리) |
| `DualUpstashStore` | 구현 완료 (capability/experience 네임스페이스) |
| `UpstashVectorStoreAdapter` | 구현 완료 |
| `RecommendationPipeline` | 구현 완료 (greedy 중복 해소) |
| **EngineerProfile Upstash 적재** | **미완료** |
| **Skill(capability_master) Upstash 적재** | **미완료** |
| `exact_skill_score` | 미구현 |
| `capability_master` 스토어 | 미구현 |
| `normalize_skill()` | 미구현 |
| LLM Re-ranking | 미구현 |
| Structured Ops | 미구현 |
| 대기열(waitlist) | 미구현 |

---

## Phase 0 — Upstash 적재 (선행 필수)

> **목표**: EngineerProfile 100개 + Skill 84개를 Upstash에 1회 적재하고,
> 이후 모든 노트북에서 재임베딩 없이 재활용한다.

### 왜 Phase 0이 먼저인가

- Phase 1(인메모리)은 API 호출마다 임베딩을 새로 생성 → 비용 낭비, 테스트 재현 불안정
- Upstash에 적재한 뒤 검색만 하면 임베딩 비용 0
- 이후 모든 Phase 노트북은 Upstash에서 검색하는 구조로 통일

### 0-1. src 구현

#### `src/embedding_retrieval/stores/capability_master.py` (신규)

```
역할: Skill 마스터 임베딩 순수 저장소 (Notion capability_master 컬렉션)
      비즈니스 로직(normalize)은 담당하지 않음 — 단일 책임
네임스페이스: "capability_master"
주요 메서드:
  - add_skills(skills: list[Skill]) -> None
  - search(query: str, top_k: int = 1) -> list[SkillSearchResult]
      → SkillSearchResult: {name, category, score}
  - is_empty() -> bool   (적재 여부 확인용)
```

#### `src/embedding_retrieval/services/profile_ingest.py` (신규)

```
역할: EngineerProfile → DualUpstashStore 적재 (독립 이식 가능)
      기존 ingest_service.py를 수정하지 않음 — 이식 시 이 파일만 떼어가면 됨
주요 함수:
  - ingest_profiles(
        profiles: list[EngineerProfile],
        store: DualUpstashStore,
        skip_if_exists: bool = True
    ) -> int
      → capability_text → "capability" namespace
      → experience_text → "experience" namespace
      → 반환: 새로 적재된 프로필 수 (skip된 것 제외)
```

#### `src/embedding_retrieval/services/skill_ingest.py` (신규)

```
역할: Skill → CapabilityMasterStore 적재 (독립 이식 가능)
      profile_ingest.py와 완전히 분리 — 필요한 것만 떼어다 쓸 수 있음
주요 함수:
  - ingest_skills(
        skills: list[Skill],
        store: CapabilityMasterStore,
        skip_if_exists: bool = True
    ) -> int
      → embed_text(=name) → "capability_master" namespace
      → 반환: 새로 적재된 스킬 수
```

---

### 0-2. notebook

#### `notebooks/setup/00_upstash_ingest.ipynb` (신규)

> 이 노트북은 **1회만 실행**한다. 이후 노트북은 검색만 사용.
> phase2~7 폴더가 아닌 `setup/`에 분리 — "적재 전용"임을 명시적으로 구분.

**Cell 구성**

```
[Cell 1] 환경 확인
- Upstash URL/TOKEN 환경변수 존재 확인
- DualUpstashStore, CapabilityMasterStore 연결 확인

[Cell 2] 이미 적재됐는지 확인 (idempotent guard)
- DualUpstashStore: capability namespace에 engineer_id 샘플 조회
- CapabilityMasterStore: is_empty() 확인
- 이미 있으면 SKIP, 없으면 진행

[Cell 3] EngineerProfile 100개 적재
- SAMPLE_ENGINEER_PROFILES → ingest_profiles()
- capability_text → Upstash "capability" namespace
- experience_text → Upstash "experience" namespace
- 적재 완료 로그 출력

[Cell 4] Skill 84개 적재
- SAMPLE_SKILLS → ingest_skills()
- embed_text(=name) → Upstash "capability_master" namespace
- 적재 완료 로그 출력

[Cell 5] 적재 결과 검증
- "Java" 검색 → capability_master top-3 출력
- "eng-001" capability 조회 → 텍스트/메타데이터 확인
- "eng-001" experience 조회 → 텍스트/메타데이터 확인
```

---

## Phase 2 — exact_skill_score 구현 및 검증

> **목표**: Notion 스펙 `capability_score = 0.8 × exact_skill_score + 0.2 × dense_capability_score` 구현

> **Lab 전제**: SAMPLE_ENGINEER_PROFILES의 스킬명은 표준 영문으로 사전 정규화되어 있으므로
> 정규화(Phase 3) 없이 exact 매칭 테스트 가능.
> **실제 프로덕션 실행 순서는 Phase 3(정규화) → Phase 2(exact 매칭)** 임을 유의.

### GAP 배경

현재 구현은 BM25 + Dense → RRF 방식이다.
Notion 스펙은 정형 스킬 매칭(exact)이 주(0.8)이고, dense가 보조(0.2)다.

```
현재:  capability_score = RRF(BM25_score, dense_score)
목표:  capability_score = 0.8 × exact_skill_score + 0.2 × dense_capability_score

       exact_skill_score = matched_required_skill_count / required_skill_count
       dense_capability_score = cosine(capability_query_vec, capability_vec)  ← Upstash 조회
```

### 2-1. src 구현

#### `src/embedding_retrieval/search/exact_skill.py` (신규)

```
역할: engineer_skill 목록과 요청 스킬 목록 비교 — 순수 계산 함수만 담당
      sample_data, RDB, Upstash 어디에도 의존하지 않음 → 그대로 이식 가능
주요 함수:
  - calc_exact_skill_score(
        required_skills: list[str],
        engineer_skills: list[str]
    ) -> float
      → matched / len(required_skills)
      → required_skills 가 비어 있으면 0.0 반환
  - calc_capability_score(
        exact: float,
        dense: float,
        exact_weight: float = 0.8
    ) -> float
      → exact_weight * exact + (1 - exact_weight) * dense
```

#### `src/embedding_retrieval/search/hybrid.py` (수정)

```
핵심 설계 원칙:
  exact_skill_score는 HybridSearcher 내부에서 계산하지 않는다.
  외부(lab: sample_data, 실제: RDB)에서 계산한 결과를 dict로 주입받는다.
  → lab → production 이식 시 주입 소스만 바꾸면 됨, HybridSearcher 코드 수정 불필요

수정 내용:
  search(
      ...,
      exact_skill_scores: dict[str, float] | None = None
      # key: engineer_id, value: exact_skill_score
      # None이면 기존 BM25+RRF 방식으로 fallback
  ) -> list[EngineerCandidate]

  스코어 계산 흐름:
    dense_cap_score  ← Upstash 조회 (기존)
    exact_score      ← 주입된 dict에서 lookup (없으면 0.0)
    capability_score ← calc_capability_score(exact_score, dense_cap_score)
    experience_score ← Upstash 조회 (기존)
    final_score      ← cap_w * capability_score + exp_w * experience_score
```

### 2-2. notebook

#### `notebooks/phase2/01_exact_skill_match.ipynb` (신규)

```
[Cell 1] 샘플 스킬 보유 현황 테이블
- SAMPLE_ENGINEER_PROFILES 100명의 capability_text 파싱 결과 출력
- 엔지니어별 보유 스킬 목록 확인

[Cell 2] exact_skill_score 단위 테스트
- required=["Java","Spring Boot"], engineer_skills=["Java","Spring Boot","Docker"]  → 1.0
- required=["Java","Spring Boot"], engineer_skills=["Java","React"]                 → 0.5
- required=["Java","Spring Boot"], engineer_skills=["Python","FastAPI"]             → 0.0
- required=[]                                                                       → 0.0

[Cell 3] 시나리오별 exact_skill_score 계산 (100명 전체)
- 요청 스킬: ["Java", "Spring Boot"]  → 100명 중 exact_skill_score 분포 히스토그램
- 요청 스킬: ["React", "TypeScript"]  → 분포 히스토그램
- 요청 스킬: ["Python", "FastAPI"]    → 분포 히스토그램

[Cell 4] capability_score 통합 (exact 0.8 + dense 0.2)
- Upstash에서 dense_capability_score 조회
- capability_score = 0.8 × exact + 0.2 × dense 계산
- 기존 BM25+RRF 방식과 랭킹 비교 테이블
- 기대 엔지니어 top-3 적중률 비교 (exact+dense vs BM25+RRF)

[Cell 5] dense보정 효과 확인 ("semantic neighbor scoring")
- 요청: "Spring"  → exact 보유자 없음 / dense로 "Spring Boot" 보유자에 보정 점수 부여 확인
- 요청: "HTML"    → exact 보유자 없음 / dense로 "CSS" 보유자에 보정 점수 부여 확인
```

---

## Phase 3 — 스킬 정규화 (capability_master)

> **목표**: LLM 1차 정규화 이후, 내부 마스터 스킬명으로 2차 정규화

### 정규화 파이프라인

```
자유 텍스트 입력
  → [1단계] LLM: 오타/한글/약어 보정 ("스프링부트" → "Spring Boot")
  → [2단계] capability_master 벡터 검색: 마스터 표준명으로 매핑
              cosine >= 0.85 → 마스터명 반환
              cosine <  0.85 → 원본 유지 (미지 스킬로 처리)
```

> Phase 0에서 SAMPLE_SKILLS 84개가 capability_master에 적재돼 있는 것이 전제.

### 3-1. src 구현

#### `src/embedding_retrieval/pipeline/normalizer.py` (신규)

```
역할: 스킬 정규화 비즈니스 로직 전담 (Store와 분리)
      capability_master.py는 순수 Store — normalize 로직이 없음
      이 파일만 떼어다 실제 프로젝트에 붙이면 됨

주요 함수:
  - normalize_skill(
        term: str,
        master_store: CapabilityMasterStore,
        threshold: float = 0.85
    ) -> str
      1. term을 embed_query()로 임베딩
      2. master_store.search(term, top_k=1) 호출
      3. score >= threshold → result.name 반환 (마스터 표준명)
      4. score <  threshold → term 그대로 반환 (미지 스킬로 처리)

  - normalize_skills(
        terms: list[str],
        master_store: CapabilityMasterStore,
        threshold: float = 0.85
    ) -> list[str]
      → 각 term에 대해 normalize_skill() 호출
      → 결과 목록 반환 (정규화 실패 항목은 원본 유지)
```

### 3-2. notebook

#### `notebooks/phase3/01_skill_normalization.ipynb` (신규)

```
[Cell 1] capability_master 적재 확인
- Phase 0에서 적재된 84개 스킬 샘플 조회
- 카테고리별 분포 확인

[Cell 2] LLM 1차 정규화 시뮬레이션
- 입력: ["스프링부트", "도커", "k8s", "리액트", "타입스크립트"]
- LLM 호출 → 1차 결과 출력
- (LLM이 이미 "Spring Boot", "Docker", "Kubernetes", "React", "TypeScript"로 변환)

[Cell 3] capability_master 2차 정규화
- LLM 출력 → normalize() 호출
- cosine 유사도와 함께 결과 출력
- threshold(0.85) 기준 매핑/미매핑 구분 테이블

[Cell 4] 임계값(threshold) 민감도 분석
- threshold: 0.70 / 0.75 / 0.80 / 0.85 / 0.90 각각
- 정규화 케이스별 오탐(false positive) / 미탐(false negative) 변화
- 최적 threshold 결정

[Cell 5] 전체 파이프라인 (LLM 1차 + capability_master 2차) 정확도
- 테스트 입력 20개 (한글, 오타, 약어 혼합)
- 기대 마스터명 vs 실제 반환값 비교 테이블
- 최종 정규화 성공률 출력
```

---

## Phase 4 — 최종 스코어링 파이프라인 E2E

> **목표**: Upstash 기반으로 final_score 계산 전체 흐름 검증

### 스코어링 공식 (Notion 스펙)

```
exact_skill_score   = matched_required_skill_count / required_skill_count
capability_score    = 0.8 × exact_skill_score + 0.2 × dense_capability_score
experience_score    = cosine(experience_query_vec, experience_vec)   ← Upstash 조회
final_score         = capability_weight × capability_score + experience_weight × experience_score
```

### 4-1. src 구현

#### `src/embedding_retrieval/pipeline/query_builder.py` (수정)

```
현재: capability_query, experience_query 텍스트 생성
추가: build_experience_query() Notion 스펙 형식 준수 확인
     [프로젝트] {project_name}: {description}
     [포지션] {position}
     [기타요건] {etc}
```

#### `src/embedding_retrieval/types.py` (수정)

```
ScoreBreakdown:
  현재: capability_dense, capability_bm25, experience_dense, experience_bm25, ...
  목표: exact_skill_score, dense_capability_score, capability_score,
        experience_score, final_score, matched_skills 필드 명확화
```

### 4-2. notebook

#### `notebooks/phase4/01_scoring_pipeline.ipynb` (신규)

```
[Cell 1] 검색 환경 구성
- DualUpstashStore 연결 (Phase 0 적재 데이터 활용)
- 스칼라 필터 파라미터 정의

[Cell 2] 포지션별 쿼리 생성 확인
- ClientRequest 예시 → build_queries() 결과 출력
- capability_query / experience_query 텍스트 확인

[Cell 3] 포지션별 full 스코어 계산 (5개 시나리오)
시나리오:
  A. Java/Spring 백엔드 + 제조업 ERP 경험 (cap:0.6, exp:0.4)
  B. React 프론트엔드 + 차트 대시보드 (cap:0.7, exp:0.3)
  C. PL + 제조업 리더십 (cap:0.2, exp:0.8)
  D. Python/FastAPI + 이커머스 물류 (cap:0.5, exp:0.5)
  E. UX 디자이너 + 핀테크 (cap:0.4, exp:0.6)

각 시나리오별 출력:
  engineer_id | exact_skill | dense_cap | capability | experience | final | rank

[Cell 4] 스칼라 필터 동작 확인
- only_available=True/False 결과 차이
- engineer_role 필터 적용 전후 후보 수 변화
- grade 필터 조합별 후보 수
- exclude_ids 블랙리스트 동작

[Cell 5] 가중치 민감도
- PL 시나리오: cap_weight 0.0~1.0 스위핑 → 랭킹 변화 라인 차트
- "가중치 조절이 실제 랭킹을 바꾸는가" 정량 확인

[Cell 6] 포지션 병렬 + 중복 해소
- ClientRequest (3포지션: PL 1명, 백엔드 3명, 프론트 2명)
- 중복 엔지니어가 여러 포지션에 등장하는 케이스 확인
- greedy 중복 해소 전후 배정 결과 테이블
```

---

## Phase 5 — LLM Re-ranking

> **목표**: 벡터 검색 top-K를 LLM이 재정렬하여 최종 품질 향상

### 5-1. src 구현

#### `src/embedding_retrieval/pipeline/reranker.py` (신규)

```
역할: Phase 4 top-K 후보를 LLM structured output으로 재정렬
입력: position, project_description, candidates(top-K)
출력: rankings[{rank, engineer_id, matched_keywords, recommendation_reason}]
특이사항:
  - structured output으로 matched_keywords도 함께 추출 (추가 API 비용 없음)
  - 포지션 간 중복 해소 지시도 프롬프트에 포함
```

### 5-2. notebook

#### `notebooks/phase5/01_llm_reranking.ipynb` (신규)

```
[Cell 1] 재정렬 전 top-K 후보 확인
- Phase 4 시나리오 A (Java/Spring ERP) top-6 후보 출력
- score_breakdown 포함 출력

[Cell 2] LLM re-ranking 실행
- top-6 → LLM structured output → 재정렬 결과
- 재정렬 전후 순위 변화 테이블 (rank delta)
- matched_keywords 출력

[Cell 3] 추천 사유 품질 확인
- recommendation_reason 전체 출력 (자연스러움 수동 평가)
- score_breakdown 수치와 추천 사유 일치 여부 확인

[Cell 4] 대기열(waitlist) 구조 검증
- top-6 = 노출(rank 1~3) + 대기(rank 4~6)
- 특정 엔지니어 제외 시 rank 4 자동 승격 동작 확인
- 대기열 소진 후 재검색 트리거 조건 확인

[Cell 5] 포지션 간 중복 해소 (LLM 방식 vs greedy 방식 비교)
- 동일 엔지니어가 PL/백엔드 양쪽에 등장하는 케이스
- LLM 지시 기반 중복 해소 결과 vs greedy 배정 결과 비교
```

---

## Phase 6 — Structured Ops + 재추천 사이클

> **목표**: Human-in-the-loop 재추천 루프의 정합성 검증

### 6-1. src 구현

#### `src/embedding_retrieval/pipeline/ops_engine.py` (신규)

```
역할: ops JSON 명령을 ClientRequest 패치로 변환
지원 ops:
  Filter:    set_grade, add_grade, remove_grade, set_only_available, set_only_full_time
  Skill:     add_skill, remove_skill, boost_skill, require_skill
  Weight:    change_weight
  Exclusion: exclude_engineer, exclude_department, include_only_department
  Scope:     expand_candidates, update_etc, change_engineer_cnt
  LLM Hint:  llm_hint
```

### 6-2. notebook

#### `notebooks/phase6/01_structured_ops.ipynb` (신규)

```
[Cell 1] 각 op 단위 동작 확인
- add_skill("TypeScript") → capability_query에 TypeScript 추가 확인
- change_weight(cap=0.3, exp=0.7) → 가중치 변경 확인
- exclude_engineer("eng-001") → exclude_ids에 추가 확인

[Cell 2] ops 체이닝
- [add_skill, change_weight, exclude_engineer] 연속 적용
- 최종 ClientRequest 상태 출력

[Cell 3] 재추천 사이클 시뮬레이션 (최대 5회)
- 초기 추천 결과 확인
- 1회: "eng-001 제외" → 대기열 승격 (벡터 재검색 없음)
- 2회: 대기열 소진 → 벡터 재검색
- 3회: 포지션 재추천 (excluded 누적 반영)
- retry_count 5회 도달 시 강제 종료 확인

[Cell 4] locked / excluded 상태 관리
- locked: "eng-002 확정" → 이후 재추천에서 제외 안 됨
- excluded: "eng-003 제외" → 전역 블랙리스트 반영
- 혼합 액션(일부 확정 + 일부 제외 + 남은 자리 재추천)
```

---

## Phase 7 — 성능 벤치마크

> **목표**: 실서비스 규모에서의 레이턴시 확인

### notebook

#### `notebooks/phase7/01_latency_benchmark.ipynb` (신규)

```
[Cell 1] 임베딩 생성 레이턴시
- Gemini embed_query() 단일 호출 50회 → p50, p95, p99
- embed_documents() 배치(10건, 50건, 100건) 처리 시간

[Cell 2] Upstash 검색 레이턴시
- capability 단일 검색 50회 → p50, p95, p99
- experience 단일 검색 50회
- 스칼라 필터 유무에 따른 레이턴시 차이
- top_k 변화(5, 10, 20, 50)에 따른 레이턴시

[Cell 3] E2E 파이프라인 레이턴시 (포지션 수별)
- 1포지션 / 3포지션 / 6포지션 각각 10회 측정
- 구간별 소요 시간: 쿼리 생성 / 임베딩 / 검색 / 스코어링 / LLM 재정렬
- 병목 구간 식별

[Cell 4] LLM Re-ranking 레이턴시
- top-K(6, 12, 18) 규모별 LLM 호출 시간
- structured output 추출 포함 시간
```

---

## 전체 순서 요약

```
[DONE] notebooks/phase1/01_embedding_quality.ipynb      — Gemini 임베딩 품질 (인메모리)
[DONE] notebooks/phase1/02_dual_vector_quality.ipynb    — 듀얼 벡터 분리 효과 (인메모리)

[Phase 0] ─── Upstash 적재 (1회 실행, 이후 재사용) ─────────────────────────────────────
  src:  stores/capability_master.py    (신규 — 순수 Store)
        services/profile_ingest.py     (신규 — 기존 ingest_service.py 수정 안 함)
        services/skill_ingest.py       (신규 — 독립 파일)
  ntb:  notebooks/setup/00_upstash_ingest.ipynb   ← setup/ 별도 폴더

[Phase 2] ─── exact_skill_score 구현 ────────────────────────────────────────────────────
  ※ lab 전제: sample_data 스킬명 표준화 → 정규화 없이 테스트 가능
  ※ 실제 프로덕션 순서: Phase 3(정규화) → Phase 2(exact 매칭)
  src:  search/exact_skill.py          (신규 — 순수 계산, 외부 의존 없음)
        search/hybrid.py               (수정 — exact_skill_scores dict 외부 주입)
  ntb:  notebooks/phase2/01_exact_skill_match.ipynb

[Phase 3] ─── 스킬 정규화 (capability_master) ──────────────────────────────────────────
  src:  pipeline/normalizer.py         (신규 — normalize 로직 전담, Store와 분리)
  ntb:  notebooks/phase3/01_skill_normalization.ipynb

[Phase 4] ─── 최종 스코어링 E2E ─────────────────────────────────────────────────────────
  src:  pipeline/query_builder.py      (검토/수정)
        types.py                       (수정 — ScoreBreakdown 필드 정리)
  ntb:  notebooks/phase4/01_scoring_pipeline.ipynb

[Phase 5] ─── LLM Re-ranking ───────────────────────────────────────────────────────────
  src:  pipeline/reranker.py           (신규)
  ntb:  notebooks/phase5/01_llm_reranking.ipynb

[Phase 6] ─── Structured Ops + 재추천 사이클 ──────────────────────────────────────────
  src:  pipeline/ops_engine.py         (신규)
  ntb:  notebooks/phase6/01_structured_ops.ipynb

[Phase 7] ─── 성능 벤치마크 ─────────────────────────────────────────────────────────────
  ntb:  notebooks/phase7/01_latency_benchmark.ipynb
```

---

## 우선순위 (MoSCoW)

| 순서 | Phase | 핵심 질문 | Must |
|------|-------|-----------|------|
| 1 | Phase 0 | Upstash에 데이터가 있는가? | Must |
| 2 | Phase 2 | exact+dense 조합이 실제로 의미있는 랭킹을 만드는가? | Must |
| 3 | Phase 3 | LLM + capability_master 2단계 정규화가 실용적인가? | Must |
| 4 | Phase 4 | 스칼라 필터·가중치·중복해소가 기대대로 동작하는가? | Must |
| 5 | Phase 5 | LLM 재정렬이 랭킹 품질을 실제로 향상시키는가? | Should |
| 6 | Phase 6 | 재추천 루프가 5회 안에 깨지지 않고 수렴하는가? | Should |
| 7 | Phase 7 | 레이턴시가 서비스 SLA(3포지션 기준 5초 이내)를 충족하는가? | Could |
