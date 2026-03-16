from embedding_retrieval.config import RetrievalConfig
from embedding_retrieval.factory import create_retrieval_pipeline


def test_search_returns_expected_document_for_query() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        chunk_size=200,
        chunk_overlap=0,
        top_k=2,
    )
    ingest_service, search_service = create_retrieval_pipeline(config)

    ingest_service.add_texts(
        texts=[
            "LangChain provides abstractions for retrieval workflows.",
            "Spring Boot is commonly used for backend APIs.",
            "Ollama can run local embedding models on a developer machine.",
        ],
        metadatas=[
            {"source": "langchain"},
            {"source": "spring"},
            {"source": "ollama"},
        ],
    )

    results = search_service.search("local embedding model", top_k=1)

    assert len(results) == 1
    assert results[0].document.metadata["source"] == "ollama"


def test_search_respects_default_top_k() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        chunk_size=200,
        chunk_overlap=0,
        top_k=1,
    )
    ingest_service, search_service = create_retrieval_pipeline(config)

    ingest_service.add_texts(
        texts=[
            "alpha beta gamma",
            "delta epsilon zeta",
        ],
    )

    results = search_service.search("alpha")

    assert len(results) == 1
