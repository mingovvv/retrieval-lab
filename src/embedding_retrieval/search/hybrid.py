"""하이브리드 검색기.

DualUpstashStore(Dense) + BM25Index(Sparse)를 조합하여
포지션별 가중치 기반 최종 랭킹을 생성한다.
"""
from __future__ import annotations

from ..stores.dual_upstash import DualUpstashStore, _build_scalar_filter
from ..types import EngineerCandidate, EngineerProfile, ScoreBreakdown
from .bm25 import BM25Index
from .exact_skill import calc_capability_score
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
        exact_skill_scores: dict[str, float] | None = None,
    ) -> list[EngineerCandidate]:
        """4-way 검색 → 스코어링 → 가중 결합 → EngineerCandidate 리스트 반환.

        Parameters
        ----------
        exact_skill_scores : dict[str, float] | None
            engineer_id → exact_skill_score 매핑.
            제공 시: capability_score = 0.8×exact + 0.2×dense (Notion 스펙).
            None 시: 기존 BM25+RRF fallback.
        """
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

        cap_dense_map = dict(cap_dense)
        exp_dense_map = dict(exp_dense)

        # --- 2. exact_skill_scores 제공 시: Notion 스펙 스코어링 ---
        if exact_skill_scores is not None:
            all_ids = set(cap_dense_map) | set(exp_dense_map)
            final_scores: dict[str, float] = {}
            cap_score_map: dict[str, float] = {}
            exp_score_map: dict[str, float] = {}

            for eid in all_ids:
                exact = exact_skill_scores.get(eid, 0.0)
                dense_cap = cap_dense_map.get(eid, 0.0)
                cap_score = calc_capability_score(exact, dense_cap)
                exp_score = exp_dense_map.get(eid, 0.0)

                cap_score_map[eid] = cap_score
                exp_score_map[eid] = exp_score
                final_scores[eid] = cap_w * cap_score + exp_w * exp_score

            ranked = sorted(final_scores.items(), key=lambda x: -x[1])[:top_k]

            candidates = []
            for rank, (eid, final_score) in enumerate(ranked, start=1):
                profile = self._profiles.get(eid)
                if not profile:
                    continue
                breakdown = ScoreBreakdown(
                    exact_skill_score=exact_skill_scores.get(eid, 0.0),
                    dense_capability_score=cap_dense_map.get(eid, 0.0),
                    capability_score=cap_score_map[eid],
                    experience_score=exp_score_map[eid],
                    final_score=final_score,
                )
                candidates.append(EngineerCandidate(
                    engineer_id=eid,
                    rank=rank,
                    score_breakdown=breakdown,
                    profile=profile,
                ))
            return candidates

        # --- 3. fallback: BM25 검색 + RRF ---
        cap_bm25_all = self._cap_bm25.search(capability_query, top_k=fetch_k)
        exp_bm25_all = self._exp_bm25.search(experience_query, top_k=fetch_k)

        allowed = self._allowed_ids(
            only_available=only_available,
            only_full_time=only_full_time,
            engineer_role=engineer_role,
            grades=grades,
            exclude_ids=exclude_ids,
        )
        cap_bm25 = [(eid, s) for eid, s in cap_bm25_all if eid in allowed]
        exp_bm25 = [(eid, s) for eid, s in exp_bm25_all if eid in allowed]

        cap_fused = fuse_results(cap_dense, cap_bm25, alpha=0.5, beta=0.5, k=rrf_k)
        exp_fused = fuse_results(exp_dense, exp_bm25, alpha=0.5, beta=0.5, k=rrf_k)

        cap_bm25_map = dict(cap_bm25)
        exp_bm25_map = dict(exp_bm25)
        cap_fused_map = dict(cap_fused)
        exp_fused_map = dict(exp_fused)

        all_ids = set(dict(cap_fused)) | set(dict(exp_fused))
        final_scores = {}
        for eid in all_ids:
            final_scores[eid] = cap_w * cap_fused_map.get(eid, 0.0) + exp_w * exp_fused_map.get(eid, 0.0)

        ranked = sorted(final_scores.items(), key=lambda x: -x[1])[:top_k]

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
