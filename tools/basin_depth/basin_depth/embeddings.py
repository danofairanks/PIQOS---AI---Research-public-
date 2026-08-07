"""Document embedding backends and bin-level signature vectors.

Implements protocol §4.1-4.2. Two backends are provided:

- `TermFrequencyBackend` (default, no extra dependencies): encodes a
  document as a hashed bag-of-words vector. This is exactly the
  "Alternative: Term-Frequency" path the protocol treats as a
  mandatory robustness check (§4.4) — here it doubles as the
  zero-dependency default so the tool runs out of the box.
- `SentenceTransformerBackend` (optional `[embeddings]` extra):
  wraps `sentence-transformers` per §4.1's exact specification
  (`all-MiniLM-L6-v2`, 384-dim).

Both implement the same `EmbeddingBackend` protocol, so
`compute_signatures` and everything downstream is backend-agnostic.
"""

from __future__ import annotations

import hashlib
from typing import Protocol

import numpy as np

from .corpus import Document, _tokenize
from .vocabulary import VocabPool


class EmbeddingBackend(Protocol):
    dim: int

    def encode(self, texts: list[str]) -> np.ndarray:
        """Return an (n_texts, dim) array of embeddings."""
        ...


class TermFrequencyBackend:
    """Zero-dependency embedding backend: hashed bag-of-words.

    Each document is mapped to a fixed-dimension vector by hashing
    tokens into buckets and counting, then L2-normalizing — a
    deterministic, seed-free analogue of a learned embedding that
    needs no model download and no GPU. Cosine similarity between two
    such vectors is a legitimate (if less semantically rich) proxy for
    document similarity, which is exactly what §4.4 asks the
    term-frequency alternative to provide.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim

    def encode(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float64)
        for i, text in enumerate(texts):
            for tok in _tokenize(text):
                h = int(hashlib.blake2b(tok.encode("utf-8"), digest_size=8).hexdigest(), 16)
                out[i, h % self.dim] += 1.0
            norm = np.linalg.norm(out[i])
            if norm > 0:
                out[i] /= norm
        return out


class SentenceTransformerBackend:
    """Protocol §4.1: `all-MiniLM-L6-v2` sentence-transformer embeddings.

    Requires the optional `sentence-transformers` dependency
    (`pip install basin-depth[embeddings]`). Imported lazily so the
    base package has no heavy/GPU dependencies.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", max_chars: int = 4000):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise ImportError(
                "SentenceTransformerBackend requires the 'embeddings' extra: "
                "pip install basin-depth[embeddings]"
            ) from exc
        self._model = SentenceTransformer(model_name)
        self.dim = self._model.get_sentence_embedding_dimension()
        self.max_chars = max_chars

    def encode(self, texts: list[str]) -> np.ndarray:
        truncated = [t[: self.max_chars] for t in texts]
        return np.asarray(self._model.encode(truncated, show_progress_bar=False))


def bin_signature(
    docs_in_bin: list[Document], vocab: VocabPool, backend: EmbeddingBackend
) -> np.ndarray | None:
    """Protocol §4.2: weighted-average embedding of the documents in one
    bin that contain at least one vocab-pool term, weighted by each
    document's vocabulary attention weight w_V(d) = (V-term count) /
    (total tokens). Returns None if no document in the bin matches.
    """
    filtered = [d for d in docs_in_bin if vocab.contains(d.text)]
    if not filtered:
        return None

    weights = np.array([
        vocab.count_in(d.text) / max(len(d.tokens), 1) for d in filtered
    ])
    if weights.sum() == 0:
        return None

    embeddings = backend.encode([d.text for d in filtered])
    return np.average(embeddings, axis=0, weights=weights)


def compute_signatures(
    bins: dict[str, list[Document]],
    quarters: list[str],
    vocab_pools: dict[str, VocabPool],
    backend: EmbeddingBackend,
) -> dict[str, dict[str, np.ndarray]]:
    """Protocol §4.2, applied across all bins and all vocab pools.

    Returns {pool_name: {quarter: signature_vector}}, omitting any
    (pool, quarter) pair with no matching documents.
    """
    signatures: dict[str, dict[str, np.ndarray]] = {name: {} for name in vocab_pools}
    for name, pool in vocab_pools.items():
        for q in quarters:
            sig = bin_signature(bins.get(q, []), pool, backend)
            if sig is not None:
                signatures[name][q] = sig
    return signatures
