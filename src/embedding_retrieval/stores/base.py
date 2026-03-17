from __future__ import annotations

from typing import Protocol

from ..compat import Document
from ..types import EngineerProfile, SearchResult


class VectorStore(Protocol):
    def add_documents(self, documents: list[Document]) -> None:
        ...

    def similarity_search(self, query: str, top_k: int, filter: str | None = None) -> list[SearchResult]:
        ...


class DualVectorStore(Protocol):
    """capability / experience 듀얼 벡터를 관리하는 스토어 프로토콜."""

    def add_profiles(self, profiles: list[EngineerProfile]) -> None:
        ...

    def search_capability(self, query: str, top_k: int, filter: str | None = None) -> list[SearchResult]:
        ...

    def search_experience(self, query: str, top_k: int, filter: str | None = None) -> list[SearchResult]:
        ...
