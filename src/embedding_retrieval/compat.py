from dataclasses import dataclass, field
from typing import Any


try:
    from langchain_core.documents import Document  # type: ignore
except ImportError:
    @dataclass(slots=True)
    class Document:
        page_content: str
        metadata: dict[str, Any] = field(default_factory=dict)


try:
    from langchain_core.embeddings import Embeddings  # type: ignore
except ImportError:
    class Embeddings:
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            raise NotImplementedError

        def embed_query(self, text: str) -> list[float]:
            raise NotImplementedError


try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore
except ImportError:
    class RecursiveCharacterTextSplitter:
        def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
            if chunk_overlap >= chunk_size:
                raise ValueError("chunk_overlap must be smaller than chunk_size")
            self._chunk_size = chunk_size
            self._chunk_overlap = chunk_overlap

        def split_documents(self, documents: list[Document]) -> list[Document]:
            split_docs: list[Document] = []
            step = self._chunk_size - self._chunk_overlap
            for document in documents:
                text = document.page_content
                if len(text) <= self._chunk_size:
                    split_docs.append(document)
                    continue
                start = 0
                chunk_index = 0
                while start < len(text):
                    end = min(start + self._chunk_size, len(text))
                    metadata = dict(document.metadata)
                    metadata["chunk_index"] = chunk_index
                    split_docs.append(Document(page_content=text[start:end], metadata=metadata))
                    if end >= len(text):
                        break
                    start += step
                    chunk_index += 1
            return split_docs
