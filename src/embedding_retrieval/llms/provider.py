from ..config import RetrievalConfig


def build_llm(config: RetrievalConfig):
    provider = config.llm_provider.lower()
    if provider in {"google", "google_genai", "gemini"}:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=config.llm_model,
            **config.llm_kwargs,
        )
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=config.llm_model, **config.llm_kwargs)
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=config.llm_model, **config.llm_kwargs)
    raise ValueError(f"Unsupported llm provider: {config.llm_provider}")
