from __future__ import annotations

import time

import numpy as np

from ..compat import Document, Embeddings
from ..types import SearchResult

# Gemini free tier: 100 RPM. batch_size=20, sleep=15s → ~80 RPM (안전 마진 확보)
_DEFAULT_BATCH_SIZE = 20
_DEFAULT_BATCH_SLEEP = 15.0  # seconds between batches
_FETCH_PAGE_SIZE = 100        # Upstash range API 한 페이지 크기


class UpstashVectorStoreAdapter:
    def __init__(
        self,
        embeddings: Embeddings,
        url: str,
        token: str,
        namespace: str | None = None,
        text_key: str = "text",
        batch_size: int = _DEFAULT_BATCH_SIZE,
        batch_sleep: float = _DEFAULT_BATCH_SLEEP,
    ) -> None:
        if not url or not token:
            raise ValueError("Upstash vector store requires both URL and token")

        from langchain_community.vectorstores.upstash import UpstashVectorStore

        self._namespace = namespace
        self._store = UpstashVectorStore(
            embedding=embeddings,
            text_key=text_key,
            index_url=url,
            index_token=token,
            namespace=namespace,
        )
        self._batch_size = batch_size
        self._batch_sleep = batch_sleep

    def add_documents(self, documents: list[Document]) -> None:
        """문서를 배치로 나눠 적재한다.

        Gemini free tier RPM 제한(100/min)을 초과하지 않도록
        batch_size 단위로 쪼개고 배치 사이에 batch_sleep 초 대기한다.
        """
        if not documents:
            return
        total = len(documents)
        for start in range(0, total, self._batch_size):
            batch = documents[start : start + self._batch_size]
            self._store.add_documents(batch)
            end = start + len(batch)
            print(f"  적재 {end}/{total} 완료", flush=True)
            if end < total:
                time.sleep(self._batch_sleep)

    def fetch_all(self) -> dict[str, np.ndarray]:
        """Upstash에 저장된 모든 벡터를 가져온다. 임베딩 API 재호출 없음.

        Returns
        -------
        dict[str, np.ndarray]
            engineer_id → 벡터 (768차원)
        """
        index = self._store._index
        result: dict[str, np.ndarray] = {}
        cursor = ""
        while True:
            resp = index.range(
                cursor=cursor,
                limit=_FETCH_PAGE_SIZE,
                include_vectors=True,
                include_metadata=True,
                namespace=self._namespace or "",
            )
            for vec in resp.vectors:
                if vec.metadata and "engineer_id" in vec.metadata:
                    result[vec.metadata["engineer_id"]] = np.array(vec.vector, dtype=float)
            cursor = resp.next_cursor
            if not cursor:
                break
        return result

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
