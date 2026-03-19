"""EngineerProfile → DualUpstashStore 적재 서비스.

기존 IngestService(범용 텍스트)와 독립적으로 분리된 파일.
이식 시 이 파일만 떼어가면 됨 — DualUpstashStore, EngineerProfile 에만 의존.
"""
from __future__ import annotations

from ..stores.dual_upstash import DualUpstashStore
from ..types import EngineerProfile


def ingest_profiles(
    profiles: list[EngineerProfile],
    store: DualUpstashStore,
    skip_if_exists: bool = True,
) -> int:
    """EngineerProfile 목록을 DualUpstashStore 에 적재한다.

    Parameters
    ----------
    profiles : list[EngineerProfile]
        적재할 프로필 목록
    store : DualUpstashStore
        capability / experience 네임스페이스를 가진 듀얼 스토어
    skip_if_exists : bool
        True 이면 스토어에 이미 데이터가 있을 경우 전체 SKIP.
        중복 적재를 방지하는 idempotent guard.
        False 이면 기존 데이터 유무와 무관하게 항상 적재.

    Returns
    -------
    int
        실제로 적재된 프로필 수. SKIP 된 경우 0 반환.
    """
    if not profiles:
        return 0

    if skip_if_exists and _has_data(store):
        return 0

    store.add_profiles(profiles)
    return len(profiles)


def _has_data(store: DualUpstashStore) -> bool:
    """capability 네임스페이스에 데이터가 이미 있으면 True."""
    try:
        results = store.search_capability("Java Spring Boot", top_k=1)
        return len(results) > 0
    except Exception:
        return False
