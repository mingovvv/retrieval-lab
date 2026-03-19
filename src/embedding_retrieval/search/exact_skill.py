"""정형 스킬 매칭 — 순수 계산 함수 + 스킬 파싱 헬퍼.

외부 의존(sample_data, RDB, Upstash) 없음 → 그대로 프로덕션에 이식 가능.

Notion 스펙:
    exact_skill_score   = matched_required_skill_count / required_skill_count
    capability_score    = 0.8 × exact_skill_score + 0.2 × dense_capability_score
"""
from __future__ import annotations


def parse_skills_from_capability(capability_text: str) -> list[str]:
    """capability_text 첫 번째 문단에서 스킬 목록을 파싱한다.

    capability_text 포맷:
        "Java / Spring Boot / PostgreSQL / Redis\n\n정보처리기사"
        → ["Java", "Spring Boot", "PostgreSQL", "Redis"]

    Parameters
    ----------
    capability_text : str
        EngineerProfile.capability_text

    Returns
    -------
    list[str]
        스킬 이름 목록 (자격증 제외, 공백 제거)
    """
    first_para = capability_text.split("\n\n")[0]
    return [s.strip() for s in first_para.split("/") if s.strip()]


def calc_exact_skill_score(
    required_skills: list[str],
    engineer_skills: list[str],
) -> float:
    """요청 스킬 대비 보유 스킬 매칭 비율을 반환한다.

    Parameters
    ----------
    required_skills : list[str]
        클라이언트가 요청한 스킬 목록 (이미 정규화된 표준명 가정)
    engineer_skills : list[str]
        엔지니어가 보유한 스킬 목록

    Returns
    -------
    float
        0.0 ~ 1.0. required_skills 가 비어 있으면 0.0.

    Examples
    --------
    >>> calc_exact_skill_score(["Java", "Spring Boot"], ["Java", "Spring Boot", "Docker"])
    1.0
    >>> calc_exact_skill_score(["Java", "Spring Boot"], ["Java", "React"])
    0.5
    >>> calc_exact_skill_score(["Java", "Spring Boot"], ["Python", "FastAPI"])
    0.0
    >>> calc_exact_skill_score([], ["Java"])
    0.0
    """
    if not required_skills:
        return 0.0
    engineer_set = {s.lower() for s in engineer_skills}
    matched = sum(1 for s in required_skills if s.lower() in engineer_set)
    return matched / len(required_skills)


def calc_capability_score(
    exact: float,
    dense: float,
    exact_weight: float = 0.8,
) -> float:
    """Notion 스펙 capability_score 계산.

    capability_score = exact_weight × exact + (1 - exact_weight) × dense

    Parameters
    ----------
    exact : float
        calc_exact_skill_score() 결과
    dense : float
        Upstash cosine 유사도 (dense_capability_score)
    exact_weight : float
        exact 비중. 기본값 0.8 (Notion 스펙).

    Returns
    -------
    float
        0.0 ~ 1.0
    """
    return exact_weight * exact + (1.0 - exact_weight) * dense
