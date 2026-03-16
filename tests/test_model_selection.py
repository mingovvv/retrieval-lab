import pytest

from embedding_retrieval.config import RetrievalConfig
from embedding_retrieval.embeddings.base import FakeEmbeddings
from embedding_retrieval.factory import create_embeddings


def test_create_embeddings_returns_fake_implementation() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        embedding_kwargs={"dimensions": 12},
    )

    embeddings = create_embeddings(config)

    assert isinstance(embeddings, FakeEmbeddings)
    assert embeddings.dimensions == 12


def test_create_embeddings_rejects_unknown_provider() -> None:
    config = RetrievalConfig(
        embedding_provider="unknown",
        embedding_model="none",
    )

    with pytest.raises(ValueError):
        create_embeddings(config)

