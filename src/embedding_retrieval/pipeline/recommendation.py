"""추천 파이프라인.

ClientRequest → 포지션별 하이브리드 검색 → 중복 감지 → PositionResult 리스트 반환.
PROCESS.md STEP 1~3 구현.
"""
from __future__ import annotations

import uuid

from ..search.hybrid import HybridSearcher
from ..types import (
    ClientRequest,
    EngineerCandidate,
    PositionResult,
    RecommendationResponse,
)
from ..weights import get_weights
from .query_builder import build_queries


class RecommendationPipeline:
    """멀티 포지션 추천 파이프라인."""

    def __init__(self, searcher: HybridSearcher) -> None:
        self._searcher = searcher

    def recommend(
        self,
        request: ClientRequest,
        multiplier: int = 3,
    ) -> RecommendationResponse:
        """ClientRequest → RecommendationResponse.

        Parameters
        ----------
        request : ClientRequest
        multiplier : top_k에 곱할 배수 (후보 풀 확장, 중복 처리 대비)
        """
        queries = build_queries(request)
        position_results: list[PositionResult] = []

        # --- STEP 2: 포지션별 검색 ---
        for pos_req, query in zip(request.positions, queries):
            cap_w, exp_w = get_weights(
                pos_req.position,
                pos_req.engineer_role,
                request.weights,
            )
            fetch_k = pos_req.engineer_cnt * multiplier

            candidates = self._searcher.search(
                capability_query=query["capability_query"],
                experience_query=query["experience_query"],
                weights=(cap_w, exp_w),
                top_k=fetch_k,
                only_available=request.only_available,
                only_full_time=request.only_full_time,
                engineer_role=pos_req.engineer_role,
                grades=pos_req.grades or None,
            )

            position_results.append(PositionResult(
                position=pos_req.position,
                candidates=candidates,
            ))

        # --- STEP 3: Cross-Position 중복 감지 + 해소 ---
        self._resolve_duplicates(position_results, request)

        return RecommendationResponse(
            request_id=uuid.uuid4().hex[:12],
            positions=position_results,
        )

    @staticmethod
    def _resolve_duplicates(
        position_results: list[PositionResult],
        request: ClientRequest,
    ) -> None:
        """Greedy 순차 배정 방식으로 중복 해소.

        포지션 순서대로 필요 인원만큼 확정하고, 확정된 엔지니어는
        이후 포지션 후보에서 제거한다. 각 포지션이 최소한의 인원을
        확보할 수 있도록 공정하게 분배.
        """
        claimed: set[str] = set()  # 이미 배정된 engineer_id

        for pos_req, pr in zip(request.positions, position_results):
            # 이미 배정된 엔지니어 제거
            available = [c for c in pr.candidates if c.engineer_id not in claimed]
            # 필요 인원만큼 확정
            selected = available[:pos_req.engineer_cnt]
            # 확정된 엔지니어 등록
            for c in selected:
                claimed.add(c.engineer_id)
            # rank 재정렬
            for rank, c in enumerate(selected, start=1):
                c.rank = rank
            pr.candidates = selected
