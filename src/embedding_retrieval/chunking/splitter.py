from ..compat import RecursiveCharacterTextSplitter
from ..config import RetrievalConfig


def create_text_splitter(config: RetrievalConfig) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
