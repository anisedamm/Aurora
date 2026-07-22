"""The arc: one conceptual thread, traced unbroken across both regimes.

`migrate` shows a value held whole in the breath web dispersing into segmented pump
lexemes. `proliferation` shows the pump lexicon re-cohering over time. This unifies
them into a single timeline for one value: from the breath sign that held it entire,
across the threshold where it scattered, to the lexemes that carried a shard back into
the phonetic web - and the definitional thread those lexemes then climbed.

The flagship is the framework's first example. The Minoan labrys held *paradoxical
equilibrium* whole. Across the threshold it dispersed into balance, justice,
moderation, symmetry. One shard, **justice**, re-entered the lexicon - and from there
the definitional web climbs: justice -> virtue, freedom -> ... -> wellbeing, the sieve
->success alignment rising the whole way. So the thread runs unbroken from a Bronze-Age
double axe to flourishing named, across the ghost lag.

A shard that no lexeme carries is reported as dispersed-but-not-retraced (honest: this
lexicon did not follow it). An authored map, a proxy throughout; descriptive, never a
gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .lexicon import Lexicon
from .migration import NerveReturn, migrate


def _descendants(seeds: list[str], lexicon: Lexicon) -> set[str]:
    """Seeds plus every lexeme that transitively is defined in terms of a seed."""
    children: dict[str, list[str]] = {}
    for lx in lexicon.lexemes.values():
        for dep in lx.defined_in_terms_of:
            children.setdefault(dep, []).append(lx.id)
    seen: set[str] = set(seeds)
    stack = list(seeds)
    while stack:
        for ch in children.get(stack.pop(), []):
            if ch not in seen:
                seen.add(ch)
                stack.append(ch)
    return seen


@dataclass
class ArcStop:
    """One lexeme on the re-cohering thread, with the height it had reached."""

    lexeme: str
    word: str
    era: str
    year: int
    alignment: float


@dataclass
class Arc:
    value: str
    breath_signs: list[tuple[str, float]] = field(default_factory=list)
    breath_weight: float = 0.0
    breath_origin: int | None = None
    shards: list[str] = field(default_factory=list)
    lexicalized: list[tuple[str, str]] = field(default_factory=list)  # (shard term, lexeme id)
    thread: list[ArcStop] = field(default_factory=list)               # by year, climbing
    nerve: list[NerveReturn] = field(default_factory=list)            # the return across the SECOND threshold

    @property
    def reaches(self) -> float:
        """The highest sieve->success alignment the thread climbs to."""
        return max((s.alignment for s in self.thread), default=0.0)

    @property
    def span_years(self) -> int:
        if self.breath_origin is None or not self.thread:
            return 0
        return int(self.thread[-1].year - self.breath_origin)

    @property
    def summary(self) -> str:
        held = ", ".join(f"{s} ({w:.2f})" for s, w in self.breath_signs) or "—"
        rows = [
            f"arc of '{self.value}' across the threshold:",
            f"  breath    — held whole in {held}",
            f"  threshold — dispersed into {len(self.shards)} shard(s): {', '.join(self.shards) or '—'}",
        ]
        if self.lexicalized:
            relex = ", ".join(f"{term}->{lid}" for term, lid in self.lexicalized)
            rows.append(f"  pump      — {len(self.lexicalized)} shard re-lexicalised: {relex}")
            rows.append("  re-coherence (the thread climbs):")
            for s in self.thread:
                rows.append(f"    {s.year:>6}  {s.word:<12} align {s.alignment:.2f}")
            rows.append(f"  the thread reaches align {self.reaches:.2f} over ~{self.span_years} year(s) "
                        f"— from a sign held whole to flourishing named, unbroken across the ghost lag")
        else:
            rows.append("  pump      — dispersed, but no shard was re-traced into this lexicon")
        if self.nerve:
            rows.append("  nerve     — re-cohered across the second threshold:")
            for n in self.nerve:
                rows.append(f"    {n.sign:<12} — {n.outcome.upper()} "
                            f"(structural {n.structural:.2f} x substantive {n.substantive:.2f})")
            rows.append("  the thread now crosses BOTH thresholds: a breath sign held whole -> the pump "
                        "lexicon -> the nerve return — one value, unbroken from origin to re-coherence")
        rows.append("  note: an authored map, a proxy; descriptive, never a gate.")
        return "\n".join(rows)


def arc(value: str, glossary: Glossary, lexicon: Lexicon) -> Arc:
    """Trace one value unbroken: breath sign -> threshold dispersal -> pump re-coherence.

    Joins `migrate` (the breath side and the shards) to the lexicon (which shards
    became lexemes, and the definitional thread they then climbed). A shard is matched
    to a lexeme by word or concept; the thread is that lexeme together with everything
    later defined in terms of it, in time order - the re-cohering climb.
    """
    m = migrate(value, glossary)

    origins = []
    for sign_id, _ in m.breath_signs:
        try:
            y = glossary.concept(sign_id).origin_year()
            if y is not None:
                origins.append(y)
        except KeyError:
            continue
    breath_origin = min(origins) if origins else None

    by_word = {lx.word.lower(): lx for lx in lexicon.lexemes.values()}
    by_concept = {lx.concept.lower(): lx for lx in lexicon.lexemes.values()}
    lexicalized: list[tuple[str, str]] = []
    seeds: list[str] = []
    for sh in m.shards:
        lx = by_word.get(sh.term.lower()) or by_concept.get(sh.term.lower())
        if lx is not None:
            lexicalized.append((sh.term, lx.id))
            seeds.append(lx.id)

    thread_ids = _descendants(seeds, lexicon)
    thread = sorted(
        (ArcStop(lx.id, lx.word, lx.era, lx.year, lx.alignment)
         for lx in (lexicon.lexemes[i] for i in thread_ids)),
        key=lambda s: (s.year, s.lexeme),
    )

    return Arc(
        value=value,
        breath_signs=m.breath_signs,
        breath_weight=m.breath_weight,
        breath_origin=breath_origin,
        shards=[sh.term for sh in m.shards],
        lexicalized=lexicalized,
        thread=thread,
        nerve=m.nerve,           # the nerve return migrate already computed (Phase E)
    )
