"""The chronicle: the whole system read as one experience over linear time.

Every other module reads the record by *kind* - a sign, a value, a lineage, a web.
Even the two that reach across the threshold keep a single thread: `arc` follows one
value end to end; `atlas` composes the measures but groups them by lens, not by date.
This module lays the *whole* record on one **linear time axis** and reads it forward,
the way a life is lived: in order, one moment after another.

Placed on one scale, the two halves of the framework's thesis stop being separate
chapters and become **interleaved strands of a single experience**:

  * **non-phonetic mythology** - the breath-era signs that held meaning *whole* (the
    labrys, the ankh, the ouroboros; the remembered divine order), each a Bronze-Age
    moment where a culture fixed a weighted field in a lasting form;
  * **the language explosion** - the phonetic lexicon proliferating over millennia,
    each word a concept a tongue valued enough to name, climbing late and slowly from
    concrete survival (water, kin) toward the inner life (soul, empathy, wellbeing).

Read in absolute time the shape is plain and is the point: the concrete necessities
are named first; the great signs hold meaning whole in a few Bronze-Age marks; the
threshold is crossed and the memory written down to survive the change in attention;
and only then, far down the axis, does the phonetic web explode and earn its way back
toward saying the inside of a life. Mythology held meaning whole in a handful of signs;
language took millennia to say what one of them held.

This is a *reader*, like the atlas - it introduces no new measure and gates nothing,
composing what the tested functions (the glossary's signs, thresholds and
remembrances; the lexicon's namings) already record, now ordered by date rather than
by kind. An authored map, a proxy throughout; descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .lexicon import Lexicon
from .regime import BREATH, PUMP, SCRIPT_CONCEPTUAL
from .weighting import WeightedField

# The strands placed on the axis. The first two are the user's question made literal -
# non-phonetic mythology held whole, and the phonetic explosion - the others are the
# crossings that link them: the threshold edges, and the remembrances that carry a
# breath truth forward across it.
MYTHOLOGY = "mythology"     # a breath/conceptual sign, meaning held whole
THRESHOLD = "threshold"     # the breath->pump edge for a tradition (the ghost lag's edge)
REMEMBRANCE = "remembrance"  # a later record carrying an earlier breath truth across
LEXEME = "lexeme"           # a phonetic word named - the language explosion
USAGE = "usage"             # a phonetic usage with no breath truth behind it (pump-native)

# A stable order for moments that fall in the same year (origin before its own edge,
# the edge before what crosses it), so the timeline is deterministic.
_KIND_RANK = {MYTHOLOGY: 0, LEXEME: 1, USAGE: 2, REMEMBRANCE: 3, THRESHOLD: 4}


@dataclass(frozen=True)
class Moment:
    """One dated event on the linear axis - a single thing the record places in time."""

    year: int
    kind: str
    regime: str          # breath / pump / threshold
    label: str
    gloss: str = ""
    period: str = ""
    experiential: bool = False   # names an inner experience (the lexicon's flag)
    ref: str = ""                # the id of the record it was read from


def _epoch(year: int) -> str:
    """A signed year rendered as the record renders it (raw), with an era tag."""
    return f"{year} BCE" if year < 0 else f"{year} CE"


@dataclass
class Chronicle:
    """The whole record on one linear time axis, read forward as lived experience."""

    moments: list[Moment] = field(default_factory=list)

    @property
    def span(self) -> tuple[int, int] | None:
        if not self.moments:
            return None
        return self.moments[0].year, self.moments[-1].year

    @property
    def mythology(self) -> list[Moment]:
        """The non-phonetic mythology strand: breath signs that held meaning whole."""
        return [m for m in self.moments if m.kind == MYTHOLOGY]

    @property
    def explosion(self) -> list[Moment]:
        """The language-explosion strand: the phonetic lexicon, named over time."""
        return [m for m in self.moments if m.kind == LEXEME]

    @property
    def experiential(self) -> list[Moment]:
        """The moments on the axis that name an inner experience."""
        return [m for m in self.explosion if m.experiential]

    @property
    def inner_life_dawn(self) -> int | None:
        """When the inner life first enters the record - the earliest experiential word."""
        years = [m.year for m in self.experiential]
        return min(years) if years else None

    @property
    def verdict(self) -> str:
        if not self.moments:
            return "an empty record - no moments to place on the axis"
        dawn = self.inner_life_dawn
        if dawn is not None:
            dawn_word = next((m.label for m in self.experiential if m.year == dawn), "—")
            inner = (f"{len(self.experiential)} of them inner-experience — the inner life "
                     f"entering at {_epoch(dawn)} ({dawn_word})")
        else:
            inner = "none of them yet naming an inner experience"
        return (
            f"{len(self.mythology)} sign(s) of non-phonetic mythology held meaning whole; "
            f"the phonetic explosion named {len(self.explosion)} concept(s), {inner}. "
            f"Meaning was held whole early, in a few signs; language climbed late and "
            f"slowly back toward the inside of a life."
        )

    @property
    def summary(self) -> str:
        rows = []
        if self.span:
            first, last = self.span
            rows.append(
                f"the system as one experience over linear time: "
                f"{len(self.moments)} moment(s), {_epoch(first)} … {_epoch(last)}"
            )
        else:
            rows.append("the system as one experience over linear time: (empty record)")
        for m in self.moments:
            star = " *" if m.experiential else ""
            line = f"{m.label}{star}"
            if m.gloss:
                tail = m.gloss if len(m.gloss) <= 46 else m.gloss[:45] + "…"
                line = f"{line} — {tail}"
            rows.append(f"  {m.year:>7}  {m.regime:<9} {m.kind:<11} {line}")
        rows.append("  " + self.verdict)
        rows.append("  (* names an inner experience) — non-phonetic mythology and the "
                    "language explosion on one axis; a reader, not a ruler. Descriptive.")
        return "\n".join(rows)


def chronicle(glossary: Glossary, lexicon: Lexicon) -> Chronicle:
    """Lay the whole record on one linear time axis, ordered by date.

    Composes, never measures: the breath signs that held meaning whole (conceptual
    usages, and a breath concept's mythic origin where no usage attests it), the
    threshold edges, the remembrances that carry a breath truth forward, the
    pump-native usages, and the lexicon's namings - placed on one scale and read
    forward. A reader, like the atlas; it introduces no new measure and gates nothing.
    """
    moments: list[Moment] = []

    for c in glossary.concepts.values():
        conceptual = [u for u in c.usages.values() if u.mode == SCRIPT_CONCEPTUAL]

        # non-phonetic mythology: signs that held a weighted field whole
        for u in conceptual:
            moments.append(Moment(
                year=u.year, kind=MYTHOLOGY, regime=BREATH, label=u.word,
                gloss=WeightedField(u.field).gloss if u.field else c.gloss,
                period=u.period, ref=u.id,
            ))

        # a breath concept whose mythic origin predates (and is not attested by) any
        # conceptual usage - the elemental memory before it was ever fixed in a sign
        if c.regime == BREATH and not conceptual:
            y = c.origin_year()
            if y is not None:
                order = c.lattice.diachronic_order(c.lattice.senses.keys())
                s = c.lattice.senses[order[0]] if order else None
                moments.append(Moment(
                    year=y, kind=MYTHOLOGY, regime=BREATH, label=c.name,
                    gloss=(s.gloss or s.label) if s else c.gloss,
                    period=(s.period if s else ""), ref=c.id,
                ))

        # the threshold edge: where this tradition crossed from breath to pump
        if c.threshold is not None:
            moments.append(Moment(
                year=c.threshold, kind=THRESHOLD, regime=THRESHOLD,
                label=f"{c.name}: breath→pump", gloss="the ghost lag's edge", ref=c.id,
            ))

        # the phonetic usages: remembrances carry a breath truth across; the rest are
        # pump-native conceptual-history (revolution, democracy)
        for u in (u for u in c.usages.values() if u.mode != SCRIPT_CONCEPTUAL):
            if u.remembers:
                moments.append(Moment(
                    year=u.year, kind=REMEMBRANCE, regime=u.regime, label=u.word,
                    gloss=f"carries '{u.remembers}' across the threshold",
                    period=u.period, ref=u.id,
                ))
            else:
                moments.append(Moment(
                    year=u.year, kind=USAGE, regime=u.regime, label=u.word,
                    gloss=u.citation, period=u.period, ref=u.id,
                ))

    # the language explosion: every word the lexicon names, in time
    for lx in lexicon.lexemes.values():
        moments.append(Moment(
            year=lx.year, kind=LEXEME, regime=PUMP, label=lx.word, gloss=lx.gloss,
            period=lx.era, experiential=lx.experiential, ref=lx.id,
        ))

    moments.sort(key=lambda m: (m.year, _KIND_RANK.get(m.kind, 9), m.ref))
    return Chronicle(moments=moments)
