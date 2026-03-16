from ..config import RetrievalConfig
from ..factory import create_retrieval_pipeline
from ..scenarios.sample_data import SAMPLE_DOCUMENTS


def run_demo() -> None:
    config = RetrievalConfig(
        embedding_provider="fake",
        embedding_model="fake",
        chunk_size=200,
        chunk_overlap=0,
    )
    ingest_service, search_service = create_retrieval_pipeline(config)
    ingest_service.add_texts(
        texts=[item["text"] for item in SAMPLE_DOCUMENTS],
        metadatas=[item["metadata"] for item in SAMPLE_DOCUMENTS],
    )
    for result in search_service.search("local embedding model", top_k=2):
        print(f"{result.score:.4f} | {result.document.metadata} | {result.document.page_content}")
