import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def load_env(start_path: str | Path | None = None) -> Path:
    start = Path(start_path).resolve() if start_path else Path.cwd().resolve()
    for candidate in [start, *start.parents]:
        env_path = candidate / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=False)
            return env_path
    raise FileNotFoundError("Could not find a .env file from the current path upwards")


@dataclass(slots=True)
class RetrievalConfig:
    embedding_provider: str
    embedding_model: str
    llm_provider: str = "google_genai"
    llm_model: str = "gemini-2.0-flash"
    vector_store: str = "memory"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    embedding_kwargs: dict[str, Any] = field(default_factory=dict)
    llm_kwargs: dict[str, Any] = field(default_factory=dict)
    vector_store_kwargs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "RetrievalConfig":
        load_env()
        return cls(
            embedding_provider=os.getenv("EMBEDDING_PROVIDER", "fake"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "fake"),
            llm_provider=os.getenv("LLM_PROVIDER", "google_genai"),
            llm_model=os.getenv("LLM_MODEL", "gemini-2.0-flash"),
            vector_store=os.getenv("VECTOR_STORE", "memory"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
            top_k=int(os.getenv("TOP_K", "3")),
            vector_store_kwargs={
                "url": os.getenv("UPSTASH_VECTOR_REST_URL", ""),
                "token": os.getenv("UPSTASH_VECTOR_REST_TOKEN", ""),
                "namespace": os.getenv("UPSTASH_VECTOR_NAMESPACE", ""),
            },
        )

    def with_overrides(self, **kwargs: Any) -> "RetrievalConfig":
        return replace(self, **kwargs)
