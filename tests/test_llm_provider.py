import pytest

from embedding_retrieval.config import RetrievalConfig
from embedding_retrieval.factory import create_llm


def test_create_llm_rejects_unknown_provider() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        llm_provider="unknown",
        llm_model="none",
    )

    with pytest.raises(ValueError):
        create_llm(config)
