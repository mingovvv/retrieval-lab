"""Skill → CapabilityMasterStore 적재 서비스.

profile_ingest.py 와 완전히 분리된 독립 파일.
이식 시 이 파일만 떼어가면 됨 — CapabilityMasterStore, Skill 에만 의존.
"""
from __future__ import annotations

from ..stores.capability_master import CapabilityMasterStore
from ..types import Skill


def ingest_skills(
    skills: list[Skill],
    store: CapabilityMasterStore,
    skip_if_exists: bool = True,
) -> int:
    """Skill 목록을 CapabilityMasterStore 에 적재한다.

    Parameters
    ----------
    skills : list[Skill]
        적재할 스킬 목록
    store : CapabilityMasterStore
        capability_master 네임스페이스 스토어
    skip_if_exists : bool
        True 이면 스토어에 이미 데이터가 있을 경우 전체 SKIP.
        중복 적재를 방지하는 idempotent guard.
        False 이면 기존 데이터 유무와 무관하게 항상 적재.

    Returns
    -------
    int
        실제로 적재된 스킬 수. SKIP 된 경우 0 반환.
    """
    if not skills:
        return 0

    if skip_if_exists and not store.is_empty():
        return 0

    store.add_skills(skills)
    return len(skills)
