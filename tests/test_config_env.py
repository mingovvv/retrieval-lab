import os

from embedding_retrieval.config import RetrievalConfig


def test_retrieval_config_from_env_reads_values(monkeypatch) -> None:
    monkeypatch.setenv("EMBEDDING_PROVIDER", "ollama")
    monkeypatch.setenv("EMBEDDING_MODEL", "nomic-embed-text")
    monkeypatch.setenv("LLM_PROVIDER", "google_genai")
    monkeypatch.setenv("LLM_MODEL", "gemini-2.0-flash")
    monkeypatch.setenv("VECTOR_STORE", "memory")
    monkeypatch.setenv("UPSTASH_VECTOR_REST_URL", "https://example.upstash.io")
    monkeypatch.setenv("UPSTASH_VECTOR_REST_TOKEN", "token")
    monkeypatch.setenv("UPSTASH_VECTOR_NAMESPACE", "test")
    monkeypatch.setenv("CHUNK_SIZE", "256")
    monkeypatch.setenv("CHUNK_OVERLAP", "16")
    monkeypatch.setenv("TOP_K", "5")

    config = RetrievalConfig.from_env()

    assert config.embedding_provider == "ollama"
    assert config.embedding_model == "nomic-embed-text"
    assert config.llm_provider == "google_genai"
    assert config.llm_model == "gemini-2.0-flash"
    assert config.vector_store == "memory"
    assert config.chunk_size == 256
    assert config.chunk_overlap == 16
    assert config.top_k == 5
    assert config.vector_store_kwargs["url"] == "https://example.upstash.io"
    assert config.vector_store_kwargs["token"] == "token"
    assert config.vector_store_kwargs["namespace"] == "test"


def test_retrieval_config_with_overrides_keeps_original() -> None:
    original = RetrievalConfig.from_env()

    updated = original.with_overrides(top_k=10)

    assert updated.top_k == 10
    assert updated.embedding_provider == original.embedding_provider
    assert original.top_k != 10 or os.getenv("TOP_K") == "10"
