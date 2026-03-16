from .base import FakeEmbeddings
from ..config import RetrievalConfig


def build_embeddings(config: RetrievalConfig):
    provider = config.embedding_provider.lower()
    if provider == "fake":
        dimensions = int(config.embedding_kwargs.get("dimensions", 8))
        return FakeEmbeddings(dimensions=dimensions)
    if provider in {"google", "google_genai", "gemini"}:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(
            model=config.embedding_model,
            output_dimensionality=768,
            **config.embedding_kwargs,
        )
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=config.embedding_model, **config.embedding_kwargs)
    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=config.embedding_model,
            **config.embedding_kwargs,
        )
    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(model=config.embedding_model, **config.embedding_kwargs)
    raise ValueError(f"Unsupported embedding provider: {config.embedding_provider}")
