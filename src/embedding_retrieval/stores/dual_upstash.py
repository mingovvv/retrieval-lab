"""Upstash 기반 듀얼 벡터 스토어.

capability / experience 를 별도 네임스페이스로 관리하되,
외부에서는 하나의 인터페이스로 사용한다.
"""
from __future__ import annotations

from ..compat import Document, Embeddings
from ..types import EngineerProfile, SearchResult
from .upstash import UpstashVectorStoreAdapter


def _build_scalar_filter(
    *,
    only_available: bool = True,
    only_full_time: bool = True,
    engineer_role: str = "",
    grades: list[str] | None = None,
    exclude_ids: list[str] | None = None,
) -> str | None:
    """스칼라 필터 표현식을 조립한다."""
    parts: list[str] = []
    if only_available:
        parts.append("status = 'AVAILABLE'")
    if only_full_time:
        parts.append("employment_type = 'FULL_TIME'")
    if engineer_role:
        parts.append(f"engineer_role = '{engineer_role}'")
    if grades:
        grade_expr = " OR ".join(f"grade = '{g}'" for g in grades)
        parts.append(f"({grade_expr})")
    if exclude_ids:
        for eid in exclude_ids:
            parts.append(f"engineer_id != '{eid}'")
    return " AND ".join(parts) if parts else None


class DualUpstashStore:
    """capability / experience 네임스페이스를 감싸는 듀얼 스토어."""

    def __init__(self, embeddings: Embeddings, url: str, token: str) -> None:
        self._embeddings = embeddings
        self._cap_store = UpstashVectorStoreAdapter(
            embeddings=embeddings, url=url, token=token, namespace="capability",
        )
        self._exp_store = UpstashVectorStoreAdapter(
            embeddings=embeddings, url=url, token=token, namespace="experience",
        )

    @staticmethod
    def _profile_metadata(p: EngineerProfile) -> dict:
        return {
            "engineer_id": p.engineer_id,
            "grade": p.grade,
            "status": p.status,
            "engineer_role": p.engineer_role,
            "employment_type": p.employment_type,
            "department_id": p.department_id,
        }

    def add_profiles(self, profiles: list[EngineerProfile]) -> None:
        cap_docs = []
        exp_docs = []
        for p in profiles:
            meta = self._profile_metadata(p)
            cap_docs.append(Document(page_content=p.capability_text, metadata=meta))
            exp_docs.append(Document(page_content=p.experience_text, metadata=meta))
        self._cap_store.add_documents(cap_docs)
        self._exp_store.add_documents(exp_docs)

    def search_capability(
        self, query: str, top_k: int, filter: str | None = None,
    ) -> list[SearchResult]:
        return self._cap_store.similarity_search(query, top_k=top_k, filter=filter)

    def search_experience(
        self, query: str, top_k: int, filter: str | None = None,
    ) -> list[SearchResult]:
        return self._exp_store.similarity_search(query, top_k=top_k, filter=filter)

    def search(
        self,
        *,
        capability_query: str,
        experience_query: str,
        weights: tuple[float, float] = (0.5, 0.5),
        top_k: int = 5,
        only_available: bool = True,
        only_full_time: bool = True,
        engineer_role: str = "",
        grades: list[str] | None = None,
        exclude_ids: list[str] | None = None,
    ) -> list[SearchResult]:
        """capability + experience 동시 검색 → 가중 합산 결과 반환."""
        cap_w, exp_w = weights
        # 더 많은 후보를 가져와서 합산 후 top_k로 자르기
        fetch_k = top_k * 3

        scalar_filter = _build_scalar_filter(
            only_available=only_available,
            only_full_time=only_full_time,
            engineer_role=engineer_role,
            grades=grades,
            exclude_ids=exclude_ids,
        )

        cap_results = self.search_capability(capability_query, top_k=fetch_k, filter=scalar_filter)
        exp_results = self.search_experience(experience_query, top_k=fetch_k, filter=scalar_filter)

        # engineer_id 기준 점수 합산
        scores: dict[str, float] = {}
        docs: dict[str, SearchResult] = {}

        for r in cap_results:
            eid = r.metadata.get("engineer_id", "")
            scores[eid] = scores.get(eid, 0.0) + cap_w * r.score
            docs[eid] = r

        for r in exp_results:
            eid = r.metadata.get("engineer_id", "")
            scores[eid] = scores.get(eid, 0.0) + exp_w * r.score
            if eid not in docs:
                docs[eid] = r

        ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        return [
            SearchResult(
                document=docs[eid].document,
                score=score,
                metadata=docs[eid].metadata,
            )
            for eid, score in ranked
        ]
