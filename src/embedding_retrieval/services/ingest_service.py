from collections.abc import Iterable
from typing import Any

from ..compat import Document
from ..stores.base import VectorStore


class IngestService:
    def __init__(self, splitter, vector_store: VectorStore) -> None:
        self._splitter = splitter
        self._vector_store = vector_store

    def add_texts(self, texts: list[str], metadatas: list[dict[str, Any]] | None = None) -> list[Document]:
        documents = self._build_documents(texts=texts, metadatas=metadatas)
        split_documents = self._splitter.split_documents(documents)
        self._vector_store.add_documents(split_documents)
        return split_documents

    def add_documents(self, documents: Iterable[Document]) -> list[Document]:
        source_documents = list(documents)
        split_documents = self._splitter.split_documents(source_documents)
        self._vector_store.add_documents(split_documents)
        return split_documents

    def _build_documents(
        self,
        texts: list[str],
        metadatas: list[dict[str, Any]] | None,
    ) -> list[Document]:
        metadatas = metadatas or [{} for _ in texts]
        if len(texts) != len(metadatas):
            raise ValueError("texts and metadatas must have the same length")
        return [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas, strict=True)
        ]
