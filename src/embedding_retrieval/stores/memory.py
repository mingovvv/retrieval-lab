from dataclasses import dataclass
from math import sqrt

from ..compat import Document, Embeddings
from ..types import SearchResult


@dataclass(slots=True)
class IndexedDocument:
    document: Document
    vector: list[float]


class InMemoryVectorStore:
    def __init__(self, embeddings: Embeddings) -> None:
        self._embeddings = embeddings
        self._documents: list[IndexedDocument] = []

    def add_documents(self, documents: list[Document]) -> None:
        if not documents:
            return
        vectors = self._embeddings.embed_documents([doc.page_content for doc in documents])
        self._documents.extend(
            IndexedDocument(document=document, vector=vector)
            for document, vector in zip(documents, vectors, strict=True)
        )

    def similarity_search(self, query: str, top_k: int) -> list[SearchResult]:
        query_vector = self._embeddings.embed_query(query)
        ranked = sorted(
            (
                SearchResult(
                    document=item.document,
                    score=_cosine_similarity(query_vector, item.vector),
                    metadata=item.document.metadata,
                )
                for item in self._documents
            ),
            key=lambda result: result.score,
            reverse=True,
        )
        return ranked[:top_k]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    numerator = sum(x * y for x, y in zip(left, right, strict=True))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)
