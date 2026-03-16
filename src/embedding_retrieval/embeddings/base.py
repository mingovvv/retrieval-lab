import hashlib
from math import sqrt

from ..compat import Embeddings


class FakeEmbeddings(Embeddings):
    def __init__(self, dimensions: int = 8) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        buckets = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            for index in range(self.dimensions):
                buckets[index] += digest[index] / 255.0

        magnitude = sqrt(sum(value * value for value in buckets))
        if magnitude == 0:
            return buckets
        return [value / magnitude for value in buckets]
