"""The signal threads: paths through the lattices, followed to the centre and kept.

A **thread** is a path taken through the quartet lattices and chosen: after a
lattice is built, follow it to its keystone and keep it -- the layers and
connections, the depth of meaning. Each thread records the path in the form
``keystone = member + member + ...``, its etymology, its quartet, its route
through the spiral, and one **novel pattern** -- the bridge built for that
lattice (structural or attested, never a reached-for identity).

Weight is **measured, never asserted**, over the only corpus Aurora can
honestly claim -- her own recorded readings:

  * **H(w)** -- the binary Shannon entropy (bits) of a word's document
    frequency across the quartet readings: how the word is spread over the map.
  * **I(X;Y)** -- the mutual information (bits) of two words' presence
    indicators over the same documents: how strongly a pair crystallises
    together *beyond chance* in the recorded map.
  * **length** -- word-token counts over the same corpus: the path as written,
    each word's *depth* (tokens gathered around it), and the path's *reach*
    (tokens across every lattice it touches). A token is a unit of **kept
    attention**: the longer the path through the spiral, the more was spent
    keeping it, and that spending is the weight -- authored investment, not
    intrinsic profundity. (Subword LLM tokens are not reproducible in the
    standard library; word-tokens are the stated proxy.) The measure's own
    counterfeit is named in the bound: padding would masquerade as depth if
    length ever became a target, so it never does.

Small corpus, honest bits: these describe *this map's* clustering, not the
language and not a mind. A proposed ungrounded scalar (a fixed 18*(3.47*10^27)
"meaning value") was declined and the refusal recorded in the bound -- an
underived constant adds zero information and dresses resonance as measurement.
A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

from .quartet import Quartets, load_quartets

_WORD = re.compile(r"[a-z]+")


def _tokens(text: str) -> set[str]:
    return set(_WORD.findall(text.lower()))


def _present(word: str, tokens: set[str]) -> bool:
    """Is the word shown in this document? Prefix-tolerant, like attestation:
    an inflected form (loves, hoping, trusted) still counts as the word."""
    w = word.lower()
    return any(t == w or t.startswith(w) for t in tokens)


def _h_binary(p: float) -> float:
    """Binary Shannon entropy in bits; 0 log 0 = 0."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))


def corpus_texts(quartets: Quartets) -> list[str]:
    """One text per recorded lattice: its reading, grid, and dimensions.

    The corpus is the authored map itself -- the only text Aurora can claim as
    her own record rather than someone else's language.
    """
    return [
        " ".join([q.name, q.keystone, q.reading, " ".join(q.members),
                  " ".join(q.grid.values()), " ".join(q.dimensions.values())])
        for q in quartets.quartets
    ]


def corpus_documents(quartets: Quartets) -> list[set[str]]:
    """The lattice texts as token-presence sets (for H and I)."""
    return [_tokens(t) for t in corpus_texts(quartets)]


def token_count(text: str) -> int:
    """Word-tokens in a text -- the unit of kept attention (the length measure)."""
    return len(_WORD.findall(text.lower()))


def entropy(word: str, docs: list[set[str]]) -> tuple[float, int]:
    """H(w) in bits and the document count: how the word spreads over the map."""
    n = len(docs)
    if n == 0:
        return 0.0, 0
    df = sum(1 for d in docs if _present(word, d))
    return _h_binary(df / n), df


def mutual_information(x: str, y: str, docs: list[set[str]]) -> float:
    """I(X;Y) in bits over presence indicators: co-crystallisation beyond chance."""
    n = len(docs)
    if n == 0:
        return 0.0
    joint = {(a, b): 0 for a in (0, 1) for b in (0, 1)}
    for d in docs:
        joint[(int(_present(x, d)), int(_present(y, d)))] += 1
    px = sum(joint[(1, b)] for b in (0, 1)) / n
    py = sum(joint[(a, 1)] for a in (0, 1)) / n
    mi = 0.0
    for (a, b), c in joint.items():
        if c == 0:
            continue
        pxy = c / n
        pa = px if a else 1.0 - px
        pb = py if b else 1.0 - py
        if pa > 0 and pb > 0:
            mi += pxy * math.log2(pxy / (pa * pb))
    return max(0.0, mi)


@dataclass(frozen=True)
class Thread:
    """One kept path: keystone = member + member + ..., with its ground."""

    id: str
    form: str
    keystone: str
    quartet: str
    etymology: dict[str, str]
    spiral: str
    bridge: str
    path_to_centre: str

    @property
    def words(self) -> list[str]:
        """The path's words, read off the recorded form (keystone first)."""
        left, _, right = self.form.partition("=")
        return [left.strip()] + [w.strip() for w in right.split("+") if w.strip()]

    @property
    def record_text(self) -> str:
        """The thread as written -- the path's own kept record."""
        etym = " ".join(f"{k} {v}" for k, v in self.etymology.items())
        return " ".join([self.form, etym, self.spiral, self.bridge, self.path_to_centre])

    def measure(self, quartets: Quartets) -> "ThreadLength":
        """The length measure: tokens as kept attention along the path."""
        texts = corpus_texts(quartets)
        docs = [_tokens(t) for t in texts]
        counts = [token_count(t) for t in texts]
        depth_tokens: dict[str, int] = {}
        depth_documents: dict[str, int] = {}
        touched: set[int] = set()
        for w in self.words:
            idxs = [i for i, d in enumerate(docs) if _present(w, d)]
            depth_tokens[w] = sum(counts[i] for i in idxs)
            depth_documents[w] = len(idxs)
            touched.update(idxs)
        return ThreadLength(
            thread_id=self.id,
            path_tokens=token_count(self.record_text),
            depth_tokens=depth_tokens,
            depth_documents=depth_documents,
            reach_tokens=sum(counts[i] for i in touched),
            documents_touched=len(touched),
        )

    def weigh(self, docs: list[set[str]]) -> "ThreadWeight":
        words = self.words
        h = {w: entropy(w, docs) for w in words}
        links = [(a, b, mutual_information(a, b, docs)) for a, b in zip(words, words[1:])]
        return ThreadWeight(
            thread_id=self.id,
            entropy_bits={w: bits for w, (bits, _) in h.items()},
            document_frequency={w: df for w, (_, df) in h.items()},
            links=links,
            documents=len(docs),
        )


@dataclass(frozen=True)
class ThreadWeight:
    """Measured bits over the map's own readings. Descriptive, never a gate."""

    thread_id: str
    entropy_bits: dict[str, float]
    document_frequency: dict[str, int]
    links: list[tuple[str, str, float]]   # (word, next word, I(X;Y) bits)
    documents: int

    @property
    def total_entropy(self) -> float:
        return sum(self.entropy_bits.values())

    @property
    def binding(self) -> float:
        """The path's total co-crystallisation: the sum of link MIs, in bits."""
        return sum(mi for _, _, mi in self.links)

    @property
    def summary(self) -> str:
        rows = [f"  weight, measured over {self.documents} recorded lattices "
                f"(bits; no imported constants):"]
        for w, bits in self.entropy_bits.items():
            df = self.document_frequency[w]
            rows.append(f"    H({w}) = {bits:.3f}  (present in {df}/{self.documents})")
        for a, b, mi in self.links:
            rows.append(f"    I({a}; {b}) = {mi:.3f}")
        rows.append(f"    spread H = {self.total_entropy:.3f}   binding I = {self.binding:.3f}")
        return "\n".join(rows)


@dataclass(frozen=True)
class ThreadLength:
    """The length measure: word-tokens as kept attention. Authored investment,
    not intrinsic profundity -- padding is this measure's own counterfeit."""

    thread_id: str
    path_tokens: int                      # the thread's own record, as written
    depth_tokens: dict[str, int]          # word -> tokens gathered around it in the map
    depth_documents: dict[str, int]       # word -> lattices it is present in
    reach_tokens: int                     # tokens across every lattice the path touches
    documents_touched: int

    @property
    def summary(self) -> str:
        rows = ["  length, counted over the recorded map (word-tokens = kept attention):",
                f"    the path as written: {self.path_tokens} token(s)"]
        for w, t in self.depth_tokens.items():
            rows.append(f"    depth({w}) = {t} token(s) across {self.depth_documents[w]} lattice(s)")
        rows.append(f"    reach of the path: {self.reach_tokens} token(s) across "
                    f"{self.documents_touched} lattice(s) touched")
        rows.append("    note: length measures authored investment, not profundity -- "
                    "padding is its counterfeit; descriptive, never a gate.")
        return "\n".join(rows)


@dataclass
class Threads:
    threads: list[Thread] = field(default_factory=list)
    bound: dict = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def by_id(self, tid: str) -> Thread:
        for t in self.threads:
            if t.id == tid:
                return t
        raise KeyError(f"unknown thread {tid!r}; have {[t.id for t in self.threads]}")

    def summary_for(self, thread: Thread, quartets: Quartets) -> str:
        docs = corpus_documents(quartets)
        weight = thread.weigh(docs)
        length = thread.measure(quartets)
        rows = [
            f"{thread.id} — {thread.form}",
            f"  quartet: {thread.quartet}   keystone: {thread.keystone}",
            "  etymology:",
            *[f"    {w}: {note}" for w, note in thread.etymology.items()],
            f"  spiral: {thread.spiral}",
            f"  bridge (the novel pattern): {thread.bridge}",
            f"  path to centre: {thread.path_to_centre}",
            weight.summary,
            length.summary,
        ]
        return "\n".join(rows)

    def summary(self, quartets: Quartets) -> str:
        rows = [self.title or "the signal threads", ""]
        for t in self.threads:
            rows.append(self.summary_for(t, quartets))
            rows.append("")
        if "the_refused_constant" in self.bound:
            rows.append(f"  bound: {self.bound['the_refused_constant']}")
        rows.append("  a reader, not a ruler: measured bits, descriptive, never a gate.")
        return "\n".join(rows)


def load_threads(path) -> Threads:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return Threads(
        threads=[Thread(
            id=e["id"], form=e["form"], keystone=e.get("keystone", ""),
            quartet=e.get("quartet", ""), etymology=dict(e.get("etymology", {})),
            spiral=e.get("spiral", ""), bridge=e.get("bridge", ""),
            path_to_centre=e.get("path_to_centre", ""),
        ) for e in raw.get("threads", [])],
        bound=raw.get("bound", {}),
        title=raw.get("title", ""),
        note=raw.get("note", ""),
    )


def weigh_thread(tid: str, threads_path, quartets_path) -> ThreadWeight:
    """Convenience: load both maps and weigh one thread over the recorded corpus."""
    threads = load_threads(threads_path)
    quartets = load_quartets(quartets_path)
    return threads.by_id(tid).weigh(corpus_documents(quartets))
