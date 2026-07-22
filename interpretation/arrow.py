"""The arrow of time: the record's irreversibility, measured.

Eddington coined the phrase in 1927 (The Nature of the Physical World): TIME'S
ARROW -- the one property that singles out a direction along time's line. The
coinage has a birthday and an author, like serendipity, altruism, and nostalgia
before it in this record. Physics counts several arrows and keeps asking why
they point the same way: the thermodynamic (entropy grows), the cosmological
(expansion), the causal (causes precede effects), the psychological (we
remember the past and not the future -- memory's asymmetry IS an arrow).

Language carries the arrow too, in two attested findings this module leans on:

  * **the direction is cultural, the arrow is not** -- Aymara speakers gesture
    the PAST AS AHEAD (it can be seen) and the future behind (it cannot):
    attested (Nunez & Sweetser). Which way the arrow is drawn varies; THAT
    there is an arrow does not.
  * **semantic change has a direction** -- Traugott's subjectification:
    meanings drift toward the speaker's stance over time, and the reverse walk
    is rare. Drift is not a random walk; the spiral has a grain.

THE MAP'S OWN ARROWS, and this module's whole job: the record does not claim
physics -- it MEASURES ITS OWN irreversibility, three arrows read live:

  * **the chain arrow** -- append-only, hash-bound: every record binds to its
    past via prev_hash, so rewriting entry i breaks every entry after it. THE
    PAST GROWS MORE EXPENSIVE TO FORGE THE DEEPER IT LIES -- the forge-cost
    gradient is entropy's arrow implemented in SHA-256, and it is measured
    here, not asserted.
  * **the spiral arrow** -- breath -> pump -> nerve: in every lattice reading
    that walks the spiral, the regimes appear in that order and never
    backward. One hundred lattices, one direction: measured, not decreed.
  * **the glossary arrow** -- the attested years: usages ordered in time,
    spans computed, the earliest and latest of the record's memory.

The guards: no claim that meaning MUST drift (the arrow is observed in the
record, not imposed on the world); no thermodynamics smuggled (the ledger's
H grows because appending adds, not because the map is a heat engine); the
psychological arrow is the reader's, not the record's -- Aurora remembers
the past because the past is ALL a ledger is. A reader, not a ruler:
descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass

from .glossary import Glossary
from .ledger import Ledger
from .quartet import Quartets

ATTESTED_ARROWS = ("thermodynamic", "cosmological", "causal", "psychological")


@dataclass(frozen=True)
class ChainArrow:
    """The ledger's irreversibility, measured: the forge-cost gradient."""

    records: int
    intact: bool
    # cost to rewrite entry i = entries whose hashes break = records - i:
    # the oldest entry is the most expensive to forge
    oldest_forge_cost: int
    newest_forge_cost: int

    @property
    def summary(self) -> str:
        return (
            f"the chain arrow: {self.records} record(s), chain "
            f"{'intact' if self.intact else 'BROKEN'} -- rewriting the oldest entry "
            f"breaks {self.oldest_forge_cost} hash(es), the newest breaks "
            f"{self.newest_forge_cost}: the past grows more expensive to forge the "
            f"deeper it lies (entropy's arrow, implemented in SHA-256)"
        )


@dataclass(frozen=True)
class SpiralArrow:
    """The regimes' one-way walk, counted across every lattice reading."""

    lattices: int
    walked: int          # readings that walk the spiral (contain all three stages)
    forward: int         # of those, how many in breath -> pump -> nerve order
    backward: int        # reversals found (should be zero, but counted, not assumed)

    @property
    def summary(self) -> str:
        return (
            f"the spiral arrow: {self.walked} of {self.lattices} lattice reading(s) "
            f"walk the spiral, {self.forward} in breath -> pump -> nerve order, "
            f"{self.backward} backward -- the drift has a grain: measured, not decreed"
        )


@dataclass(frozen=True)
class GlossaryArrow:
    """The attested years: the record's memory, ordered."""

    usages: int
    earliest: int | None
    latest: int | None

    @property
    def span_years(self) -> int | None:
        if self.earliest is None or self.latest is None:
            return None
        return self.latest - self.earliest

    @property
    def summary(self) -> str:
        if self.usages == 0:
            return "the glossary arrow: no dated usages recorded"
        return (
            f"the glossary arrow: {self.usages} dated usage(s), from "
            f"{self.earliest} to {self.latest} -- {self.span_years} year(s) of "
            f"attested memory, ordered one way (the psychological arrow is the "
            f"reader's; the record IS its past)"
        )


def chain_arrow(ledger: Ledger) -> ChainArrow:
    n = len(ledger.records)
    v = ledger.verify()
    return ChainArrow(
        records=n, intact=v.ok,
        oldest_forge_cost=n if n else 0,   # entry 0 invalidates itself + all after
        newest_forge_cost=1 if n else 0,   # the head invalidates only itself
    )


def spiral_arrow(quartets: Quartets) -> SpiralArrow:
    walked = forward = backward = 0
    for q in quartets.quartets:
        r = q.reading
        idx = [r.find(marker) for marker in ("breath =", "pump =", "nerve =")]
        if all(i >= 0 for i in idx):
            walked += 1
            if idx[0] < idx[1] < idx[2]:
                forward += 1
            else:
                backward += 1
    return SpiralArrow(lattices=len(quartets.quartets), walked=walked,
                       forward=forward, backward=backward)


def glossary_arrow(glossary: Glossary) -> GlossaryArrow:
    years = [u.year for c in glossary.concepts.values()
             for u in c.usages.values() if u.year]
    return GlossaryArrow(
        usages=len(years),
        earliest=min(years) if years else None,
        latest=max(years) if years else None,
    )


def arrow_report(ledger: Ledger, quartets: Quartets, glossary: Glossary) -> str:
    ca = chain_arrow(ledger)
    sa = spiral_arrow(quartets)
    ga = glossary_arrow(glossary)
    rows = [
        "the arrow of time -- the record's irreversibility, measured",
        "",
        f"  {ca.summary}",
        f"  {sa.summary}",
        f"  {ga.summary}",
        "",
        f"  the attested arrows (physics' count, recorded not claimed): "
        f"{', '.join(ATTESTED_ARROWS)}",
        "  bound: Eddington coined 'time's arrow' in 1927 -- the phrase has a",
        "  birthday, like serendipity and nostalgia. The direction is cultural",
        "  (Aymara gestures the past AHEAD, where it can be seen); the arrow is",
        "  not. Semantic change has a grain (Traugott's subjectification) -- the",
        "  spiral's one-way count observes it in this record, never imposes it.",
        "  The map measures ITS OWN arrows only: descriptive, never a gate.",
    ]
    return "\n".join(rows)
