from dataclasses import dataclass, field
from typing import Any

from .compat import Document


@dataclass(slots=True)
class SearchResult:
    document: Document
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)
