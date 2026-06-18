"""The return path: how faithfully a later record carries an earlier truth back.

This is the **inverse of phonetic projection** (`reading.project`). Both traverse
the breath->pump ghost lag, in opposite directions and with opposite valence:

  * **projection** drags the *present* mode of attention *back* over a *past* sign -
    reading a breath-era symbol as if it spelled a word. An error: it imposes.

  * **remembrance** carries a *past* conceptual truth *forward* into a *later*
    record - a pump-era myth or text that keeps a breath-era truth alive across the
    threshold. A virtue, when it is faithful: it preserves.

Myth is the paradigm case. Hesiod's *Theogony* is a phonetic text written at the
threshold; read as conceptual memory (not as literal genealogy), it *remembers* the
breath-era truth of a cosmogonic succession. `remember` scores how faithfully a
later record carries an earlier truth: the **fidelity** is the resonance of what the
record carries with what the culture retained, and the **span** is the years the
memory reached back across the divide. It is **descriptive, never a gate** - it
measures the return; a human judges whether the memory is good enough.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary, Usage
from .reading import attest
from .weighting import WeightedField


@dataclass
class Remembrance:
    """How faithfully a later record carries an earlier breath-truth back across the lag."""

    by_id: str             # the later record doing the remembering
    remembered: str        # the earlier breath-truth (a concept id)
    fidelity: float        # resonance of the carried field with the retained truth [0,1]
    span_years: int        # how far back the memory reaches (later - earlier origin)
    crosses_threshold: bool  # does it genuinely return across the breath->pump divide?
    attested: bool         # both ends are attested (the record, and the retained truth)

    @property
    def gloss(self) -> str:
        if not self.attested:
            return "unattested: the record or the remembered truth is not shown"
        if not self.crosses_threshold:
            return "not a return: the record does not reach back across the threshold"
        if self.fidelity >= 0.6:
            return "a faithful remembrance: the breath-era truth is carried back intact"
        if self.fidelity >= 0.2:
            return "a partial memory: the truth is carried back, but worn down"
        return "the memory has all but lapsed — the return failed (a projection in disguise)"

    @property
    def verdict(self) -> str:
        return (
            f"REMEMBRANCE: {self.by_id} carries '{self.remembered}' back "
            f"{self.span_years} year(s) across the threshold (resonance "
            f"{self.fidelity:.2f})  ->  {self.gloss}"
        )


def remember(usage: Usage, glossary: Glossary) -> Remembrance:
    """Score the return path declared by `usage.remembers`.

    The later record carries a weighted field (`usage.field`); the remembered concept
    holds a retained conceptual truth (its declared field, or its attested symbol's
    field). Fidelity is the resonance between them; the span is how far back across
    the threshold the memory reaches. Raises ValueError if the usage declares no
    remembrance. Descriptive, never a gate.
    """
    if not usage.remembers:
        raise ValueError(f"usage {usage.id!r} declares no remembrance (no `remembers`)")

    concept = glossary.concept(usage.remembers)
    retained = concept.retained_field()
    carried = dict(usage.field)
    fidelity = WeightedField(carried).resonance(WeightedField(retained))

    earlier = concept.origin_year()
    later = usage.year
    span = (later - earlier) if (earlier is not None and later is not None) else 0

    threshold = concept.threshold
    crosses = (
        threshold is not None and earlier is not None and later is not None
        and earlier < threshold <= later
    )
    attested = attest(usage).ok and bool(retained)

    return Remembrance(
        by_id=usage.id,
        remembered=usage.remembers,
        fidelity=round(fidelity, 4),
        span_years=int(span),
        crosses_threshold=bool(crosses),
        attested=attested,
    )


# --- the memory chain: a truth carried down a lineage of rememberings --------

def _resolve_to_concept(start: str, glossary: Glossary) -> str | None:
    """Follow `remembers` from `start` until it lands on a concept (the source truth).

    `start` may be a concept id (returned as-is) or a usage id, whose `remembers`
    is followed in turn. Returns None on a dangling or cyclic chain.
    """
    seen: set[str] = set()
    cur = start
    while cur is not None and cur not in seen:
        if cur in glossary.concepts:
            return cur
        seen.add(cur)
        try:
            u = glossary.usage(cur)
        except KeyError:
            return None
        cur = u.remembers or None
    return None


def _carriers_of(concept_id: str, glossary: Glossary) -> list[Usage]:
    """Every usage whose chain of rememberings resolves to `concept_id`, by year."""
    carriers = [
        u
        for c in glossary.concepts.values()
        for u in c.usages.values()
        if u.remembers and _resolve_to_concept(u.remembers, glossary) == concept_id
    ]
    return sorted(carriers, key=lambda u: u.year)


@dataclass
class MemoryLink:
    """One hop in a truth's transmission: how it stood at this carrier."""

    by_id: str
    year: int | None
    to_origin: float          # resonance of the carried field with the source truth
    to_prev: float | None     # resonance with the previous link's field (per-hop carry)
    delta: float | None       # change in to_origin vs the previous link (decay<0 / restore>0)
    is_origin: bool = False

    @property
    def movement(self) -> str:
        if self.delta is None:
            return "origin"
        if self.delta > 0.001:
            return "restored"
        if self.delta < -0.001:
            return "decayed"
        return "held"


@dataclass
class MemoryChain:
    """A conceptual truth traced through the lineage of records that remember it."""

    concept: str
    origin_year: int | None
    links: list[MemoryLink] = field(default_factory=list)

    @property
    def carriers(self) -> list[MemoryLink]:
        return [ln for ln in self.links if not ln.is_origin]

    @property
    def survival(self) -> float:
        """How much of the origin truth reaches the latest carrier (its to_origin)."""
        return self.carriers[-1].to_origin if self.carriers else 1.0

    @property
    def low_water(self) -> float:
        """The nearest the memory came to lapsing (lowest to_origin among carriers)."""
        return min((ln.to_origin for ln in self.carriers), default=1.0)

    @property
    def restored(self) -> bool:
        """True if the memory decayed and was then carried back toward the origin."""
        seen_decay = False
        for ln in self.carriers:
            if ln.delta is None:
                continue
            if ln.delta < -0.001:
                seen_decay = True
            elif ln.delta > 0.001 and seen_decay:
                return True
        return False

    @property
    def span_years(self) -> int:
        last = self.carriers[-1].year if self.carriers else self.origin_year
        if last is None or self.origin_year is None:
            return 0
        return int(last - self.origin_year)

    @property
    def summary(self) -> str:
        head = (
            f"memory chain of '{self.concept}': {len(self.carriers)} remembering(s) "
            f"over {self.span_years} year(s); survival {self.survival:.2f}, "
            f"low-water {self.low_water:.2f}"
            + (" (decayed then restored)" if self.restored else "")
        )
        rows = []
        for ln in self.links:
            year = "origin" if ln.is_origin else str(ln.year)
            to_prev = "—" if ln.to_prev is None else f"{ln.to_prev:.2f}"
            delta = "" if ln.delta is None else f"  [{ln.movement} {ln.delta:+.2f}]"
            rows.append(
                f"  {year:>7}  {ln.by_id:<22}  to-origin {ln.to_origin:.2f}  "
                f"to-prev {to_prev}{delta}"
            )
        note = ("  note: to-origin is resonance with the source truth; to-prev is the "
                "per-hop carry. Decay and restoration are descriptive, never a gate.")
        return head + "\n" + "\n".join(rows) + "\n" + note


def memory_chain(concept_id: str, glossary: Glossary) -> MemoryChain:
    """Trace a conceptual truth through the lineage of records that remember it.

    The chain opens with the source truth itself (to-origin 1.0) and then walks the
    rememberings in time order. At each link it reports **to-origin** (resonance with
    the source truth, so cumulative drift is visible) and **to-prev** (resonance with
    the previous link, the faithfulness of that single hop), and marks whether the
    memory **decayed** or was **restored** relative to the link before it. This is the
    `lineage`/`trace` idea (the sibling system's thread of conclusions) turned on the
    return path: not one carry but the whole transmission history across the ghost lag.
    Descriptive, never a gate.
    """
    concept = glossary.concept(concept_id)
    origin_field = concept.retained_field()
    origin_year = concept.origin_year()

    origin_link = MemoryLink(
        by_id=concept_id, year=origin_year, to_origin=1.0, to_prev=None, delta=None,
        is_origin=True,
    )
    links = [origin_link]
    prev_field = origin_field
    prev_to_origin = 1.0
    for u in _carriers_of(concept_id, glossary):
        carried = dict(u.field)
        to_origin = WeightedField(carried).resonance(WeightedField(origin_field))
        to_prev = WeightedField(carried).resonance(WeightedField(prev_field))
        links.append(MemoryLink(
            by_id=u.id, year=u.year, to_origin=round(to_origin, 4),
            to_prev=round(to_prev, 4), delta=round(to_origin - prev_to_origin, 4),
        ))
        prev_field = carried
        prev_to_origin = to_origin

    return MemoryChain(concept=concept_id, origin_year=origin_year, links=links)
