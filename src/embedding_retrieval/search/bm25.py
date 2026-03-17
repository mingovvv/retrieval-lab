"""Pure-Python BM25 인덱스.

키워드 빈도 기반 희소 검색. Dense 임베딩이 놓치는 정확한 기술명 매칭을 보완한다.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field


def _tokenize(text: str) -> list[str]:
    """공백 + 특수문자 기준 토크나이징. 소문자 변환."""
    return [t for t in re.split(r"[\s/,|·•\-\[\]()]+", text.lower()) if t]


@dataclass
class _DocEntry:
    doc_id: str
    tf: dict[str, int] = field(default_factory=dict)  # term → frequency
    length: int = 0


class BM25Index:
    """BM25 (Okapi BM25) 구현.

    Parameters
    ----------
    k1 : float
        term frequency saturation. 기본 1.5
    b : float
        document length normalization. 기본 0.75
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self._docs: dict[str, _DocEntry] = {}      # doc_id → entry
        self._df: dict[str, int] = {}               # term → document frequency
        self._avg_dl: float = 0.0
        self._n: int = 0

    def fit(self, documents: list[tuple[str, str]]) -> None:
        """인덱스 구축.

        Parameters
        ----------
        documents : list of (doc_id, text)
        """
        self._docs.clear()
        self._df.clear()

        for doc_id, text in documents:
            tokens = _tokenize(text)
            tf: dict[str, int] = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1

            self._docs[doc_id] = _DocEntry(doc_id=doc_id, tf=tf, length=len(tokens))

            for term in tf:
                self._df[term] = self._df.get(term, 0) + 1

        self._n = len(self._docs)
        total_len = sum(d.length for d in self._docs.values())
        self._avg_dl = total_len / self._n if self._n > 0 else 0.0

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """BM25 점수 기준 상위 문서 반환.

        Returns
        -------
        list of (doc_id, score) 내림차순
        """
        if not self._docs:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores: dict[str, float] = {}

        for term in query_tokens:
            df = self._df.get(term, 0)
            if df == 0:
                continue
            idf = math.log((self._n - df + 0.5) / (df + 0.5) + 1.0)

            for doc_id, entry in self._docs.items():
                tf = entry.tf.get(term, 0)
                if tf == 0:
                    continue
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * entry.length / self._avg_dl)
                score = idf * numerator / denominator
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        ranked = sorted(scores.items(), key=lambda x: -x[1])
        return ranked[:top_k]

    @property
    def doc_count(self) -> int:
        return self._n

    @property
    def vocab_size(self) -> int:
        return len(self._df)
