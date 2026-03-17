"""쿼리 텍스트 빌더.

ClientRequest의 포지션 정보를 벡터 검색용 쿼리 텍스트로 변환한다.
PROCESS.md 기준:
  - capability_query: 스킬명 나열 ("Java / Spring")
  - experience_query: 프로젝트 맥락 + 포지션 + 요건
"""
from __future__ import annotations

from ..types import ClientRequest, PositionRequest


def build_capability_query(position: PositionRequest) -> str:
    """스킬 리스트 → capability 검색용 텍스트."""
    if not position.skills:
        return position.position  # 스킬 미지정 시 포지션명으로 폴백
    return " / ".join(position.skills)


def build_experience_query(
    position: PositionRequest,
    project_name: str,
    project_description: str,
) -> str:
    """프로젝트 맥락 + 포지션 + 요건 → experience 검색용 텍스트."""
    parts: list[str] = []
    parts.append(f"[프로젝트] {project_name}: {project_description}")
    parts.append(f"[포지션] {position.position}")
    if position.etc:
        parts.append(f"[요건] {position.etc}")
    return "\n".join(parts)


def build_queries(
    request: ClientRequest,
) -> list[dict[str, str]]:
    """ClientRequest → 포지션별 쿼리 텍스트 리스트.

    Returns
    -------
    list of {"position": ..., "capability_query": ..., "experience_query": ...}
    """
    result = []
    for pos in request.positions:
        result.append({
            "position": pos.position,
            "capability_query": build_capability_query(pos),
            "experience_query": build_experience_query(
                pos, request.project_name, request.description,
            ),
        })
    return result
