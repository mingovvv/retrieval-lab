from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .compat import Document


@dataclass(slots=True)
class SearchResult:
    document: Document
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Domain types (PROCESS.md)
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class EngineerProfile:
    engineer_id: str
    grade: str                          # SENIOR | INTERMEDIATE | JUNIOR | EXPERT
    status: str                         # AVAILABLE | UNAVAILABLE
    engineer_role: str                  # DEVELOPER | PLANNER | QA | DESIGNER | PUBLISHER
    employment_type: str                # FULL_TIME | FREELANCER
    capability_text: str                # 기술스택 + 자격증
    experience_text: str                # 소개 + 프로젝트 경험 + 경력
    department_id: str = ""
    updated_at: int = 0                 # Unix timestamp


@dataclass(slots=True)
class PositionRequest:
    position: str                       # PL, 백엔드 개발자, 프론트엔드 개발자, ...
    engineer_role: str                  # DEVELOPER | PLANNER | QA | DESIGNER
    engineer_cnt: int
    grades: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    etc: str = ""                       # 추가 요건 (자연어)


@dataclass(slots=True)
class ClientRequest:
    project_name: str
    description: str
    positions: list[PositionRequest]
    only_available: bool = True
    only_full_time: bool = True
    weights: dict[str, float] = field(default_factory=lambda: {"capability": 0.5, "experience": 0.5})
    start_date: str = ""
    end_date: str = ""


@dataclass(slots=True)
class ScoreBreakdown:
    # Phase 2 — Notion 스펙 스코어링
    exact_skill_score: float = 0.0       # matched / required  (정형 매칭)
    dense_capability_score: float = 0.0  # cosine(cap_query, cap_vec)
    capability_score: float = 0.0        # 0.8×exact + 0.2×dense
    experience_score: float = 0.0        # cosine(exp_query, exp_vec)
    final_score: float = 0.0             # cap_w×capability + exp_w×experience
    # Legacy — BM25+RRF fallback (exact_skill_scores 미제공 시)
    capability_dense: float = 0.0
    capability_bm25: float = 0.0
    experience_dense: float = 0.0
    experience_bm25: float = 0.0
    capability_rrf: float = 0.0
    experience_rrf: float = 0.0


@dataclass(slots=True)
class EngineerCandidate:
    engineer_id: str
    rank: int
    score_breakdown: ScoreBreakdown
    profile: EngineerProfile
    recommendation_reason: str = ""


@dataclass(slots=True)
class PositionResult:
    position: str
    candidates: list[EngineerCandidate] = field(default_factory=list)


@dataclass(slots=True)
class RecommendationResponse:
    request_id: str
    positions: list[PositionResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Skill — 스킬 임베딩용 도메인 타입
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class Skill:
    skill_id: int
    name: str
    category: str       # LANGUAGE | FRAMEWORK | DATABASE | INFRA | DESIGN | CLOUD | DEVOPS | TOOL | OTHER
    embed_text: str     # 임베딩용 텍스트 — skill.name 그대로 사용


@dataclass(slots=True)
class SkillSearchResult:
    """capability_master 벡터 검색 결과 한 건."""
    name: str           # 마스터 표준 스킬명
    category: str       # LANGUAGE | FRAMEWORK | ...
    score: float        # cosine 유사도
    master_id: int = 0  # Notion capability_master 스펙 필드명
