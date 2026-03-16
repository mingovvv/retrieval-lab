from .compat import Embeddings
from .chunking.splitter import create_text_splitter
from .config import RetrievalConfig
from .embeddings.provider import build_embeddings
from .llms.provider import build_llm
from .services.ingest_service import IngestService
from .services.search_service import SearchService
from .stores.base import VectorStore
from .stores.memory import InMemoryVectorStore
from .stores.upstash import UpstashVectorStoreAdapter


def create_embeddings(config: RetrievalConfig) -> Embeddings:
    return build_embeddings(config)


def create_vector_store(config: RetrievalConfig, embeddings: Embeddings) -> VectorStore:
    if config.vector_store == "memory":
        return InMemoryVectorStore(embeddings=embeddings)
    if config.vector_store == "upstash":
        return UpstashVectorStoreAdapter(
            embeddings=embeddings,
            url=str(config.vector_store_kwargs.get("url", "")),
            token=str(config.vector_store_kwargs.get("token", "")),
            namespace=str(config.vector_store_kwargs.get("namespace", "")) or None,
        )
    raise ValueError(f"Unsupported vector store: {config.vector_store}")


def create_llm(config: RetrievalConfig):
    return build_llm(config)


def create_retrieval_pipeline(config: RetrievalConfig) -> tuple[IngestService, SearchService]:
    embeddings = create_embeddings(config)
    vector_store = create_vector_store(config, embeddings)
    splitter = create_text_splitter(config)
    ingest_service = IngestService(splitter=splitter, vector_store=vector_store)
    search_service = SearchService(vector_store=vector_store, top_k=config.top_k)
    return ingest_service, search_service
