"""Fingerprinting a passage: turn text into signals we can verify and recognise.

Two jobs live here, kept apart on purpose - the same discipline the sibling
*integrity-alignment-system* runs on, carried over verbatim because a reading is
recognised exactly the way an authored artifact is:

  * **Integrity** - a cryptographic hash of the bytes (and of the *normalised*
    text). Identical hash => the passage is word-for-word what was recorded.
    Exact and unforgeable; it answers "has this gloss been altered?"

  * **Recognition** - a MinHash signature over word shingles. A *similarity*
    signal: it survives paraphrase and reformatting, so two readings that say the
    same thing in different words are recognised as kin. It is a **proxy** for
    "this is the same interpretation", never a proof - two readers can land on
    similar phrasing independently, and a determined paraphrase can slip past any
    threshold. The framework treats this number with the suspicion a proxy
    deserves (see docs/thought-flow.md, step 1).

The permutation seed matches the sibling system's, so a passage fingerprinted
here lands in the same recognition space there. Pure standard library; the
package adds no dependencies.
"""

from __future__ import annotations

import hashlib
import random
import re
from dataclasses import dataclass

# Recognition parameters. k=3 keys on distinctive 3-word phrasing: it survives
# paraphrase yet does not collide with unrelated prose. num_perm sets the
# resolution of the MinHash Jaccard estimate.
SHINGLE_K = 3
NUM_PERM = 128

_MERSENNE_PRIME = (1 << 61) - 1
_MAX_HASH = (1 << 32) - 1
_PERM_SEED = 20260601  # fixed so signatures are reproducible across machines


def _make_permutations(num_perm: int) -> list[tuple[int, int]]:
    rng = random.Random(_PERM_SEED)
    return [
        (rng.randint(1, _MERSENNE_PRIME - 1), rng.randint(0, _MERSENNE_PRIME - 1))
        for _ in range(num_perm)
    ]


_PERMUTATIONS = _make_permutations(NUM_PERM)


def normalize(text: str) -> str:
    """Lowercase, strip punctuation to spaces, collapse whitespace.

    Normalisation lets recognition see through cosmetic edits (capitalisation,
    spacing, punctuation). It is deliberately lossy: the *content* hash is taken
    over the raw bytes, so exact-tamper detection is never weakened by this step.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def shingles(text: str, k: int = SHINGLE_K) -> frozenset[str]:
    """Word k-grams of the normalised text.

    Falls back to unigrams when the text is shorter than k words, so even a
    one-line gloss produces a usable (if weak) signature rather than none.
    """
    tokens = normalize(text).split()
    if not tokens:
        return frozenset()
    if len(tokens) < k:
        return frozenset(tokens)
    return frozenset(" ".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1))


def _shingle_hash(shingle: str) -> int:
    return int.from_bytes(hashlib.blake2b(shingle.encode(), digest_size=8).digest(), "big")


def _minhash(shingle_set: frozenset[str]) -> tuple[int, ...]:
    """MinHash signature: for each permutation, the min hash over all shingles."""
    if not shingle_set:
        return tuple([_MAX_HASH] * NUM_PERM)
    base = [(_shingle_hash(s) % _MERSENNE_PRIME) for s in shingle_set]
    sig = []
    for a, b in _PERMUTATIONS:
        sig.append(min(((a * h + b) % _MERSENNE_PRIME) % _MAX_HASH for h in base))
    return tuple(sig)


@dataclass(frozen=True)
class Fingerprint:
    """Everything we need to both verify and recognise a passage."""

    content_hash: str           # sha256 of raw bytes      -> exact tamper check
    normalized_hash: str        # sha256 of normalised text -> verbatim-modulo-format
    n_shingles: int             # size of the shingle set   -> confidence context
    signature: tuple[int, ...]  # MinHash                   -> similarity proxy

    def as_dict(self) -> dict:
        return {
            "content_hash": self.content_hash,
            "normalized_hash": self.normalized_hash,
            "n_shingles": self.n_shingles,
            "signature": list(self.signature),
        }


def fingerprint(text: str) -> Fingerprint:
    """Compute the integrity hashes and the recognition signature for `text`."""
    raw = text.encode("utf-8")
    norm = normalize(text)
    sset = shingles(text)
    return Fingerprint(
        content_hash=hashlib.sha256(raw).hexdigest(),
        normalized_hash=hashlib.sha256(norm.encode("utf-8")).hexdigest(),
        n_shingles=len(sset),
        signature=_minhash(sset),
    )


def jaccard(sig_a: tuple[int, ...], sig_b: tuple[int, ...]) -> float:
    """Estimated Jaccard similarity of two MinHash signatures, in [0, 1].

    Returns 0.0 when either side carries no real shingles, so an empty or
    near-empty passage can never be 'recognised' as someone's reading.
    """
    if not sig_a or not sig_b or len(sig_a) != len(sig_b):
        return 0.0
    empty = tuple([_MAX_HASH] * len(sig_a))
    if sig_a == empty or sig_b == empty:
        return 0.0
    return sum(1 for x, y in zip(sig_a, sig_b) if x == y) / len(sig_a)
