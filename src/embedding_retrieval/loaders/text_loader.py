from pathlib import Path


def load_texts(paths: list[str | Path]) -> list[str]:
    return [Path(path).read_text(encoding="utf-8") for path in paths]

