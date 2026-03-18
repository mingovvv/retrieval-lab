# Retrieval Lab — ROADMAP

> AI 엔지니어 인재 추천 시스템의 벡터 검색 품질 및 성능 검증을 위한 단위 테스트 로드맵.
> API 개발이 아닌, 각 컴포넌트의 **조회 정확도·성능·스코어링 품질**을 검증하는 것이 목표.

---

## 현재 상태 (AS-IS)

### 구현 완료
- [x] Gemini / OpenAI / HuggingFace / Ollama / Fake 임베딩 프로바이더
- [x] DualUpstashStore (capability / experience 네임스페이스 분리)
- [x] BM25 순수 Python 구현 + RRF 퓨전
- [x] HybridSearcher (4-way: dense cap + dense exp + BM25 cap + BM25 exp)
- [x] RecommendationPipeline (포지션별 병렬 검색 + 중복 해소)
- [x] 포지션/역할 기반 가중치 매트릭스
- [x] 샘플 엔지니어 9명 데이터

### 스펙과의 GAP
| 항목 | 현재 구현 | Notion 스펙 (목표) |
|------|-----------|---------------------|
| capability 스코어 | BM25 + Dense via RRF | **0.8 × exact_skill_score + 0.2 × dense** |
| exact_skill_score | 미구현 | RDB engineer_skill 기반 정형 매칭 |
| experience 스코어 | BM25 + Dense via RRF | **순수 dense cosine** |
| 스킬 정규화 | 미구현 | capability_master 벡터 검색 (0.85 임계값) |
| LLM Re-ranking | 미구현 | structured output + matched_keywords |
| 대기열 (waitlist) | 미구현 | top-K에서 상위 N 노출, 나머지 대기 |
| Structured Ops | 미구현 | 조건 패치 JSON 명령 체계 |
| Human-in-the-loop | 미구현 | 확정/제외 + 재추천 (최대 5회) |

---

## Phase 1 — 임베딩 품질 검증
> **목표**: Gemini 768차원 임베딩이 인재 도메인에서 의미 유사도를 제대로 잡는지 확인

### 1-1. 임베딩 기초 품질 테스트
- [ ] `notebooks/phase1/01_embedding_quality.ipynb`
- Gemini embedding-2-preview 768차원 출력 확인
- 동일 기술 스택 엔지니어 간 cosine 유사도 측정
- 이종 기술 스택 간 cosine 거리 확인 (Java↔React, Java↔Spring 등)
- 차원 축소(3072→768) 전후 품질 비교

### 1-2. capability vs experience 분리 효과 검증
- [ ] `notebooks/phase1/02_dual_vector_quality.ipynb`
- capability_text만으로 임베딩 시 기술 유사 엔지니어끼리 클러스터링 되는지
- experience_text만으로 임베딩 시 도메인/경험 유사 엔지니어끼리 클러스터링 되는지
- 단일 벡터(합산) vs 듀얼 벡터 분리의 검색 품질 차이 정량화

---

## Phase 2 — Exact Skill Matching 구현 및 검증
> **목표**: Notion 스펙의 `capability_score = 0.8 × exact + 0.2 × dense` 공식 구현

### 2-1. exact_skill_score 구현
- [ ] `src/embedding_retrieval/search/exact_skill.py`
- `matched_required_skill_count / required_skill_count` 계산기
- 엔지니어별 보유 스킬 목록과 요청 스킬 목록 비교
- [ ] `notebooks/phase2/01_exact_skill_match.ipynb`
- 9명 샘플 데이터로 exact_skill_score 계산 결과 검증
- edge case: 스킬 0개 요청, 전체 매칭, 부분 매칭

### 2-2. capability_score 통합 (exact + dense)
- [ ] `notebooks/phase2/02_capability_score.ipynb`
- `0.8 × exact_skill_score + 0.2 × dense_capability_score` 통합 스코어
- BM25 기반 기존 방식 vs exact+dense 방식 비교
- 어떤 방식이 실제 기대 랭킹과 더 일치하는지 평가

### 2-3. experience_score 순수 dense 전환
- [ ] `notebooks/phase2/03_experience_dense_only.ipynb`
- experience를 BM25+RRF 제거하고 순수 cosine만으로 전환
- 기존 hybrid vs dense-only 비교
- 도메인 키워드("현대차", "ERP") 매칭 정확도

---

## Phase 3 — 스킬 정규화 (capability_master)
> **목표**: 오타/변형 스킬명을 마스터 데이터 기반으로 정규화

### 정규화 2단계 파이프라인
```
자유 텍스트 → [1단계] LLM 전처리 (오타 보정 + ops 구조화) → [2단계] capability_master (마스터 ID 매핑)
```
- **LLM**: 오타/약어/문맥 추론 (스푸링푸트 → Spring Boot)
- **capability_master**: 마스터 테이블 정규화 (동의어 통일, cosine ≥ 0.85로 ID 매핑)
- 오타 교정은 LLM 담당 → capability_master 임계값 0.85 안정적 유지

### 3-1. capability_master 컬렉션 구현
- [ ] `src/embedding_retrieval/stores/capability_master.py`
- 스킬/자격증 마스터 벡터 저장소
- `normalize_skill(term, type)` → 유사도 0.85 이상이면 마스터명 반환
- LLM이 1차 보정한 스킬명을 마스터 ID로 매핑하는 역할
- [ ] `notebooks/phase3/01_skill_normalization.ipynb`
- LLM 보정 후 입력 기준 정규화 테스트 (Spring Boot → master_id)
- 한글 정식명 매핑 (스프링부트 → Spring Boot)
- 임계값(0.85) 변경에 따른 오탐/미탐 변화

---

## Phase 4 — 최종 스코어링 파이프라인 검증
> **목표**: final_score 계산이 기대하는 랭킹을 만들어내는지 E2E 검증

### 4-1. 가중치별 랭킹 변화 테스트
- [ ] `notebooks/phase4/01_weight_sensitivity.ipynb`
- capability:experience = 0.7:0.3, 0.5:0.5, 0.3:0.7 각각의 랭킹 결과
- 포지션별 기본 가중치(PL 0.2:0.8, DEV 0.7:0.3 등)의 적절성 확인
- 가중치 변화에 따른 top-K 변동폭 측정

### 4-2. 스칼라 필터 정확성 테스트
- [ ] `notebooks/phase4/02_scalar_filter.ipynb`
- only_available, only_full_time, engineer_role, grade 필터 조합별 결과 검증
- 필터링 후 남은 후보 풀에서의 스코어링 정확도
- exclude_ids 블랙리스트 동작 확인

### 4-3. 포지션별 병렬 검색 + 중복 해소
- [ ] `notebooks/phase4/03_deduplication.ipynb`
- 동일 엔지니어가 여러 포지션에 걸릴 때 배정 전략 검증
- greedy allocation vs 최적 배정 결과 비교
- 포지션 순서에 따른 배정 편향 확인

---

## Phase 5 — LLM Re-ranking
> **목표**: 벡터 검색 top-K를 LLM이 재정렬하여 최종 품질 향상 확인

### 5-1. LLM Re-ranking 구현
- [ ] `src/embedding_retrieval/pipeline/reranker.py`
- structured output 스키마 (rank, matched_keywords, recommendation_reason)
- 포지션별 top-K 입력 → 순위 재조정 + 중복 해소
- [ ] `notebooks/phase5/01_llm_reranking.ipynb`
- 벡터 검색 결과 vs LLM 재정렬 결과 비교
- matched_keywords 추출 품질 확인
- 추천 사유 자연스러움 평가

### 5-2. 대기열(waitlist) 로직
- [ ] `notebooks/phase5/02_waitlist.ipynb`
- top-K(=engineer_cnt×2)에서 상위 N 노출, 하위 N 대기
- 제외 시 대기열 승격 동작 확인
- 대기열 소진 후 벡터 재검색 트리거

---

## Phase 6 — 재추천 및 Structured Ops
> **목표**: Human-in-the-loop 재추천 사이클의 정합성 검증

### 6-1. Structured Ops 엔진
- [ ] `src/embedding_retrieval/pipeline/ops_engine.py`
- add_skill, remove_skill, change_weight, exclude_engineer 등 ops 적용기
- ops 적용 전후 검색 조건 diff 확인
- [ ] `notebooks/phase6/01_structured_ops.ipynb`
- 각 op 타입별 동작 검증
- ops 체이닝 (여러 op 연속 적용) 결과 확인

### 6-2. 재추천 사이클 시뮬레이션
- [ ] `notebooks/phase6/02_re_recommendation.ipynb`
- 전체/포지션/개인/혼합 재추천 시나리오별 테스트
- locked/excluded 상태 관리 정합성
- retry_count 상한(5회) 도달 시 강제 종료

---

## Phase 7 — 성능 벤치마크
> **목표**: 실서비스 규모에서의 조회 레이턴시 및 처리량 확인

### 7-1. 임베딩 생성 성능
- [ ] `notebooks/phase7/01_embedding_latency.ipynb`
- Gemini API 단일 호출 레이턴시 (p50, p95, p99)
- 배치 임베딩 처리량 (100건, 500건, 1000건)
- 768차원 vs 3072차원 레이턴시 차이

### 7-2. 벡터 검색 레이턴시
- [ ] `notebooks/phase7/02_search_latency.ipynb`
- Upstash Vector 조회 레이턴시 (10건, 50건, 100건 스케일)
- 스칼라 필터 유무에 따른 레이턴시 변화
- 동시 포지션 병렬 검색 시 총 소요 시간

### 7-3. E2E 파이프라인 레이턴시
- [ ] `notebooks/phase7/03_e2e_latency.ipynb`
- 전처리(정규화+쿼리생성) → 임베딩 → 검색 → 스코어링 → LLM 재정렬
- 구간별 소요 시간 breakdown
- 3포지션/6포지션 요청 시 총 응답 시간

---

## 우선순위 요약

| 순서 | Phase | 핵심 질문 | 난이도 |
|------|-------|-----------|--------|
| 1 | Phase 1 | Gemini 임베딩이 인재 도메인에서 쓸만한가? | ★☆☆ |
| 2 | Phase 2 | exact_skill + dense 조합이 BM25보다 나은가? | ★★☆ |
| 3 | Phase 4 | 가중치·필터·중복해소가 기대대로 동작하는가? | ★★☆ |
| 4 | Phase 3 | 스킬 정규화가 실용적 정확도를 내는가? | ★★☆ |
| 5 | Phase 5 | LLM 재정렬이 랭킹 품질을 실제로 올리는가? | ★★★ |
| 6 | Phase 7 | 레이턴시가 서비스 SLA를 충족하는가? | ★★☆ |
| 7 | Phase 6 | 재추천 루프가 깨지지 않고 동작하는가? | ★★★ |
