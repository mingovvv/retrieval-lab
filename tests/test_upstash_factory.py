import pytest

from embedding_retrieval.config import RetrievalConfig
from embedding_retrieval.embeddings.base import FakeEmbeddings
from embedding_retrieval.factory import create_vector_store


def test_create_vector_store_rejects_missing_upstash_credentials() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        vector_store="upstash",
        vector_store_kwargs={"url": "", "token": ""},
    )

    with pytest.raises(ValueError):
        create_vector_store(config, FakeEmbeddings())
