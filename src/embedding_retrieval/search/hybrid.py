"""하이브리드 검색기.

DualUpstashStore(Dense) + BM25Index(Sparse)를 조합하여
포지션별 가중치 기반 최종 랭킹을 생성한다.
"""
from __future__ import annotations

from ..stores.dual_upstash import DualUpstashStore, _build_scalar_filter
from ..types import EngineerCandidate, EngineerProfile, ScoreBreakdown
from .bm25 import BM25Index
from .rrf import fuse_results


class HybridSearcher:
    """Dense + BM25 하이브리드 검색."""

    def __init__(
        self,
        store: DualUpstashStore,
        cap_bm25: BM25Index,
        exp_bm25: BM25Index,
        profiles: list[EngineerProfile],
    ) -> None:
        self._store = store
        self._cap_bm25 = cap_bm25
        self._exp_bm25 = exp_bm25
        # engineer_id → profile 매핑
        self._profiles = {p.engineer_id: p for p in profiles}

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
        rrf_k: int = 60,
    ) -> list[EngineerCandidate]:
        """4-way 검색 → RRF 합산 → 가중 결합 → EngineerCandidate 리스트 반환."""
        cap_w, exp_w = weights
        fetch_k = top_k * 3

        # --- 스칼라 필터 (Dense용) ---
        scalar_filter = _build_scalar_filter(
            only_available=only_available,
            only_full_time=only_full_time,
            engineer_role=engineer_role,
            grades=grades,
            exclude_ids=exclude_ids,
        )

        # --- 1. Dense 검색 ---
        cap_dense_raw = self._store.search_capability(capability_query, top_k=fetch_k, filter=scalar_filter)
        exp_dense_raw = self._store.search_experience(experience_query, top_k=fetch_k, filter=scalar_filter)

        cap_dense = [(r.metadata["engineer_id"], r.score) for r in cap_dense_raw]
        exp_dense = [(r.metadata["engineer_id"], r.score) for r in exp_dense_raw]

        # --- 2. BM25 검색 ---
        cap_bm25_all = self._cap_bm25.search(capability_query, top_k=fetch_k)
        exp_bm25_all = self._exp_bm25.search(experience_query, top_k=fetch_k)

        # BM25에는 스칼라 필터가 없으므로 exclude_ids 등 수동 필터링
        allowed = self._allowed_ids(
            only_available=only_available,
            only_full_time=only_full_time,
            engineer_role=engineer_role,
            grades=grades,
            exclude_ids=exclude_ids,
        )
        cap_bm25 = [(eid, s) for eid, s in cap_bm25_all if eid in allowed]
        exp_bm25 = [(eid, s) for eid, s in exp_bm25_all if eid in allowed]

        # --- 3. RRF 합산 (capability, experience 각각) ---
        cap_fused = fuse_results(cap_dense, cap_bm25, alpha=0.5, beta=0.5, k=rrf_k)
        exp_fused = fuse_results(exp_dense, exp_bm25, alpha=0.5, beta=0.5, k=rrf_k)

        # --- 4. 원본 점수 lookup용 dict ---
        cap_dense_map = dict(cap_dense)
        exp_dense_map = dict(exp_dense)
        cap_bm25_map = dict(cap_bm25)
        exp_bm25_map = dict(exp_bm25)
        cap_fused_map = dict(cap_fused)
        exp_fused_map = dict(exp_fused)

        # --- 5. 최종 점수: cap_w * cap_rrf + exp_w * exp_rrf ---
        all_ids = set(dict(cap_fused)) | set(dict(exp_fused))
        final_scores: dict[str, float] = {}
        for eid in all_ids:
            cap_score = cap_fused_map.get(eid, 0.0)
            exp_score = exp_fused_map.get(eid, 0.0)
            final_scores[eid] = cap_w * cap_score + exp_w * exp_score

        ranked = sorted(final_scores.items(), key=lambda x: -x[1])[:top_k]

        # --- 6. EngineerCandidate 생성 ---
        candidates = []
        for rank, (eid, final_score) in enumerate(ranked, start=1):
            profile = self._profiles.get(eid)
            if not profile:
                continue
            breakdown = ScoreBreakdown(
                capability_dense=cap_dense_map.get(eid, 0.0),
                capability_bm25=cap_bm25_map.get(eid, 0.0),
                experience_dense=exp_dense_map.get(eid, 0.0),
                experience_bm25=exp_bm25_map.get(eid, 0.0),
                capability_rrf=cap_fused_map.get(eid, 0.0),
                experience_rrf=exp_fused_map.get(eid, 0.0),
                final_score=final_score,
            )
            candidates.append(EngineerCandidate(
                engineer_id=eid,
                rank=rank,
                score_breakdown=breakdown,
                profile=profile,
            ))
        return candidates

    def _allowed_ids(
        self,
        only_available: bool,
        only_full_time: bool,
        engineer_role: str,
        grades: list[str] | None,
        exclude_ids: list[str] | None,
    ) -> set[str]:
        """BM25 결과에 적용할 필터. 프로필 메타데이터 기반."""
        result = set()
        for eid, p in self._profiles.items():
            if only_available and p.status != "AVAILABLE":
                continue
            if only_full_time and p.employment_type != "FULL_TIME":
                continue
            if engineer_role and p.engineer_role != engineer_role:
                continue
            if grades and p.grade not in grades:
                continue
            if exclude_ids and eid in exclude_ids:
                continue
            result.add(eid)
        return result
