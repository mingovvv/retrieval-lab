from typing import Protocol

from ..compat import Document
from ..types import SearchResult


class VectorStore(Protocol):
    def add_documents(self, documents: list[Document]) -> None:
        ...

    def similarity_search(self, query: str, top_k: int) -> list[SearchResult]:
        ...
