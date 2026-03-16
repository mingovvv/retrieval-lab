from ..stores.base import VectorStore
from ..types import SearchResult


class SearchService:
    def __init__(self, vector_store: VectorStore, top_k: int = 3) -> None:
        self._vector_store = vector_store
        self._top_k = top_k

    def search(self, query: str, top_k: int | None = None) -> list[SearchResult]:
        limit = top_k if top_k is not None else self._top_k
        return self._vector_store.similarity_search(query=query, top_k=limit)

