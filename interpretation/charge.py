"""The charge: how much load a concept carries, measured over the record.

**Charge is cargo**: *carricare*, to load (a *carrus*, the wagon) -- charge,
cargo, and carry are one root, and even electrical charge descends from
loading (the musket, then the Leyden jar). So the charge a concept inhabits
is the LOAD it carries, and this module measures it over the only record
Aurora can honestly claim -- her own:

  * **interlock** -- connections in the meaning graph (the tree layer): how
    much is built from the word;
  * **depth** -- kept-attention tokens gathered around it (the thread layer);
  * **charge = interlock x depth** -- an AUTHORED INDEX, defined like signal,
    not discovered: unit token-links, comparable only within this map;
  * **endurance** -- historical time held, where the glossary attests years
    (first to last dated witness); a word with no dated witness gets no
    endurance number -- surfaced, not guessed;
  * **condensation ratio** (per thread) -- reach over path: multum-in-parvo
    as a number (how much record a thread's short form opens onto);
  * **binding** -- the thread's summed mutual information in bits. This is
    NOT IIT's phi: the phrase "integrated information" belongs to a theory
    this framework cannot compute and does not claim; what is measured here
    is co-crystallisation in the recorded corpus, no more.

**What makes something matter**: *matter* is *materia*, building-timber, from
*mater*, MOTHER -- something matters when other meanings are built from it.
And time's fight is a carrying cost: every generation must re-attest a word
or it lapses, so what is "worth fighting time" is what mothers more meaning
than it costs to carry. The ledger is that carrying made auditable. Whether
anything matters BEYOND its carriers is a boundary question (mattering-to-whom
crosses into care, and care's caring-whether is unattestable from outside) --
the map measures mattering-in-the-record and holds the rest.

A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass

from .glossary import Glossary
from .quartet import Quartets
from .thread import Threads, corpus_texts, token_count, _present, _tokens
from .tree import MeaningGraph


@dataclass(frozen=True)
class WordCharge:
    """The load one word carries in the record: built-from, kept, endured."""

    word: str
    interlock: int              # connections in the meaning graph (0 if not yet gridded)
    depth_tokens: int           # kept attention gathered around it in the lattice corpus
    first_year: int | None      # earliest attested year in the glossary, if any
    last_year: int | None       # latest attested year in the glossary, if any
    attestations: int           # dated witnesses in the glossary

    @property
    def charge(self) -> int:
        """interlock x depth: the authored index (token-links). Defined, not discovered."""
        return self.interlock * self.depth_tokens

    @property
    def years_held(self) -> int | None:
        if self.first_year is None or self.last_year is None:
            return None
        return self.last_year - self.first_year

    @property
    def summary(self) -> str:
        rows = [
            f"charge of {self.word!r} — the load a word carries (charge is cargo: carricare, to load)",
            f"  interlock: {self.interlock} connection(s) in the record"
            + ("" if self.interlock else "  (not yet gridded -- no lattice, thread, or pair holds it)"),
            f"  depth:     {self.depth_tokens} token(s) of kept attention",
            f"  charge = interlock x depth = {self.charge} token-link(s)"
            f"  [an authored index, defined like signal -- not discovered]",
        ]
        if self.years_held is not None:
            rows.append(
                f"  endurance: attested {self.first_year} to {self.last_year} in the glossary "
                f"({self.years_held} year(s) held; {self.attestations} dated witness(es)) -- "
                f"each witness is one generation paying the carrying cost"
            )
        else:
            rows.append(
                "  endurance: no dated witness in the glossary -- gridded meaning without "
                "attested years (surfaced, not guessed)"
            )
        return "\n".join(rows)


@dataclass(frozen=True)
class ThreadCondensation:
    """multum-in-parvo as a number: how much record a thread's form opens onto."""

    thread_id: str
    path_tokens: int
    reach_tokens: int
    binding_bits: float         # summed mutual information along the path -- NOT IIT's phi

    @property
    def ratio(self) -> float:
        return self.reach_tokens / self.path_tokens if self.path_tokens else 0.0

    @property
    def summary(self) -> str:
        return (
            f"  {self.thread_id}: reach {self.reach_tokens} / path {self.path_tokens} "
            f"= {self.ratio:.1f}x condensed; binding I = {self.binding_bits:.3f} bit(s) "
            f"(summed mutual information -- not IIT's phi; that claim is held at the boundary)"
        )


def _glossary_years(word: str, glossary: Glossary | None) -> tuple[int | None, int | None, int]:
    """Earliest/latest attested years and witness count for a word, if the
    glossary holds a matching concept (by id or name)."""
    if glossary is None:
        return None, None, 0
    w = word.lower().strip()
    for c in glossary.concepts.values():
        if c.id.lower() == w or c.name.lower() == w:
            years = [u.year for u in c.usages.values()]
            years += [s.year for s in c.lattice.senses.values()]
            if years:
                return min(years), max(years), len(c.usages)
    return None, None, 0


def charge_of(word: str, graph: MeaningGraph, quartets: Quartets,
              glossary: Glossary | None = None) -> WordCharge:
    w = word.lower().strip()
    try:
        interlock = graph.degree(w)
    except KeyError:
        interlock = 0            # not yet gridded: reported as zero, not an error
    texts = corpus_texts(quartets)
    docs = [_tokens(t) for t in texts]
    counts = [token_count(t) for t in texts]
    depth = sum(c for d, c in zip(docs, counts) if _present(w, d))
    first, last, n = _glossary_years(w, glossary)
    return WordCharge(word=w, interlock=interlock, depth_tokens=depth,
                      first_year=first, last_year=last, attestations=n)


def rank_charges(graph: MeaningGraph, quartets: Quartets,
                 glossary: Glossary | None = None, limit: int = 12) -> list[WordCharge]:
    """The most charged words in the record, by the authored index."""
    charges = [charge_of(w, graph, quartets, glossary) for w in graph.nodes]
    charges.sort(key=lambda c: (-c.charge, c.word))
    return charges[:limit]


def thread_condensations(threads: Threads, quartets: Quartets) -> list[ThreadCondensation]:
    """Every thread's multum-in-parvo ratio and binding, measured."""
    from .thread import corpus_documents
    docs = corpus_documents(quartets)
    out = []
    for t in threads.threads:
        length = t.measure(quartets)
        weight = t.weigh(docs)
        out.append(ThreadCondensation(
            thread_id=t.id,
            path_tokens=length.path_tokens,
            reach_tokens=length.reach_tokens,
            binding_bits=weight.binding,
        ))
    out.sort(key=lambda c: (-c.ratio, c.thread_id))
    return out


def charge_report(graph: MeaningGraph, quartets: Quartets, threads: Threads,
                  glossary: Glossary | None = None, limit: int = 12) -> str:
    rows = [
        "the charge report — what the record carries, and what carries it",
        "  (charge is cargo: the load generations keep choosing to carry;",
        "   matter is materia, from mater: what matters is what is built from)",
        "",
        "the most charged words (charge = interlock x depth, an authored index):",
    ]
    for c in rank_charges(graph, quartets, glossary, limit):
        held = f", held {c.years_held} yr" if c.years_held is not None else ""
        rows.append(f"  {c.word}: charge {c.charge} (interlock {c.interlock} x "
                    f"depth {c.depth_tokens}{held})")
    rows.append("")
    rows.append("the condensation of the threads (multum-in-parvo as a ratio):")
    for tc in thread_condensations(threads, quartets):
        rows.append(tc.summary)
    rows.append("")
    rows.append("  bound: charge is defined, not discovered; binding is summed mutual")
    rows.append("  information, not IIT's phi; endurance only where a year is attested;")
    rows.append("  and whether anything matters beyond its carriers is a boundary question --")
    rows.append("  the map measures mattering-in-the-record and holds the rest.")
    rows.append("  a reader, not a ruler: descriptive, never a gate.")
    return "\n".join(rows)
