"""capability_master 벡터 저장소.

Skill 마스터 데이터를 임베딩하여 저장하고 검색하는 순수 저장소.
normalize 비즈니스 로직은 담당하지 않음 — pipeline/normalizer.py 에서 담당.
"""
from __future__ import annotations

import time

from ..compat import Document, Embeddings
from ..types import Skill, SkillSearchResult
from .upstash import UpstashVectorStoreAdapter

NAMESPACE = "capability_master"


class CapabilityMasterStore:
    """Skill 마스터 임베딩 순수 저장소 (Notion capability_master 컬렉션).

    네임스페이스: "capability_master"

    책임:
      - add_skills  : Skill 목록 임베딩 후 저장
      - search      : query 와 가장 유사한 스킬 검색
      - is_empty    : 적재 여부 확인 (idempotent guard 용)

    이식 방법:
      실제 프로젝트에서 이 파일을 그대로 복사하고
      Upstash URL / TOKEN 을 환경변수로 주입하면 바로 사용 가능.
    """

    def __init__(self, embeddings: Embeddings, url: str, token: str) -> None:
        self._store = UpstashVectorStoreAdapter(
            embeddings=embeddings,
            url=url,
            token=token,
            namespace=NAMESPACE,
        )

    def add_skills(self, skills: list[Skill]) -> None:
        """스킬 목록을 임베딩하여 capability_master 네임스페이스에 저장."""
        if not skills:
            return
        ts = int(time.time())
        docs = [
            Document(
                page_content=skill.embed_text,
                metadata={
                    "master_id": skill.skill_id,
                    "name": skill.name,
                    "type": "skill",
                    "category": skill.category,
                    "created_at": ts,
                },
            )
            for skill in skills
        ]
        self._store.add_documents(docs)

    def search(self, query: str, top_k: int = 1) -> list[SkillSearchResult]:
        """query 와 가장 유사한 스킬을 반환.

        Parameters
        ----------
        query : str
            검색할 스킬명 (LLM 1차 정규화 결과 또는 원본 입력)
        top_k : int
            반환할 최대 결과 수

        Returns
        -------
        list[SkillSearchResult]
            name, category, score, skill_id 포함
        """
        results = self._store.similarity_search(query, top_k=top_k)
        return [
            SkillSearchResult(
                name=r.metadata.get("name", ""),
                category=r.metadata.get("category", ""),
                score=r.score,
                master_id=int(r.metadata.get("master_id", 0)),
            )
            for r in results
        ]

    def is_empty(self) -> bool:
        """데이터가 적재되지 않은 상태이면 True.

        idempotent guard 용도 — 노트북 setup 단계에서 이미 적재됐는지 확인.
        """
        try:
            results = self._store.similarity_search("Java", top_k=1)
            return len(results) == 0
        except Exception:
            return True
