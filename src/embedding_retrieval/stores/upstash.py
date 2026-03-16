from __future__ import annotations

from ..compat import Document, Embeddings
from ..types import SearchResult


class UpstashVectorStoreAdapter:
    def __init__(
        self,
        embeddings: Embeddings,
        url: str,
        token: str,
        namespace: str | None = None,
    ) -> None:
        if not url or not token:
            raise ValueError("Upstash vector store requires both URL and token")

        from langchain_community.vectorstores.upstash import UpstashVectorStore

        self._store = UpstashVectorStore(
            embedding=embeddings,
            text_key="text",
            index_url=url,
            index_token=token,
            namespace=namespace,
        )

    def add_documents(self, documents: list[Document]) -> None:
        if not documents:
            return
        self._store.add_documents(documents)

    def similarity_search(self, query: str, top_k: int, filter: str | None = None) -> list[SearchResult]:
        results = self._store.similarity_search_with_score(query, k=top_k, filter=filter)
        return [
            SearchResult(
                document=document,
                score=float(score),
                metadata=document.metadata,
            )
            for document, score in results
        ]
