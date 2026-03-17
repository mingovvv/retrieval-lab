"""Reciprocal Rank Fusion (RRF).

Dense와 BM25 두 랭킹 리스트를 하나로 합산한다.
"""
from __future__ import annotations


def rrf_score(rank: int, k: int = 60) -> float:
    """RRF 점수. rank는 1-based."""
    return 1.0 / (k + rank)


def fuse_results(
    dense_ranked: list[tuple[str, float]],
    bm25_ranked: list[tuple[str, float]],
    alpha: float = 0.5,
    beta: float = 0.5,
    k: int = 60,
) -> list[tuple[str, float]]:
    """Dense + BM25 랭킹을 RRF로 합산.

    Parameters
    ----------
    dense_ranked : list of (doc_id, score) — Dense 점수 내림차순
    bm25_ranked  : list of (doc_id, score) — BM25 점수 내림차순
    alpha : Dense RRF 가중치
    beta  : BM25 RRF 가중치
    k     : RRF smoothing 상수 (기본 60)

    Returns
    -------
    list of (doc_id, fused_score) 내림차순
    """
    scores: dict[str, float] = {}

    for rank, (doc_id, _) in enumerate(dense_ranked, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + alpha * rrf_score(rank, k)

    for rank, (doc_id, _) in enumerate(bm25_ranked, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + beta * rrf_score(rank, k)

    return sorted(scores.items(), key=lambda x: -x[1])
