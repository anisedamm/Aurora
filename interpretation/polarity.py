"""The polarities: the 2 layer -- the first cut, recorded at last.

The number-structure has always named the 2 (the first cut, the polarity, the
threshold, the binary); this module reads the layer that records it. The root
antonyms of meaning are the pairs that stay paired no matter how derived -- the
defining line of language expressing positive and negative sense.

Two grounded findings carry the layer:

  * **the morpheme line** -- positive poles carry toward-morphemes (ad-, con-,
    pro-), negative poles carry against-morphemes (re-, dis-, contra-, in-,
    mis-, and with- = OE *wid*, against): language's positive sense moves toward
    and binds, its negative sense moves back, apart, against. At the map's
    scale, Empedocles inscribed in grammar -- love-morphemes and strife-morphemes.
  * **the axes are polarities** -- every quartet axis is an antonym pair already
    at work; the 4s were built of 2s from the start. `axis_pairs` reads them
    live off the quartet map: the layer is computed against the record, not
    asserted beside it.

The bound guards the layer from dualism: the negative pole is not the enemy
(NOT ATTESTED is the gate doing its work; the custodian's refusals are negation
in service of truth -- a yes that cannot say no is not assent but reflex).

A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .quartet import Quartets

VALID_KINDS = ("complementary", "contrary", "converse", "reversive", "privative")


@dataclass(frozen=True)
class Pair:
    """One root antonym couple: the positive pole, the negative, and the line."""

    id: str
    positive: str
    negative: str
    kind: str           # one of VALID_KINDS (the attested typology of opposition)
    derivation: str     # the morphology: which pole is marked, and by what morpheme
    line: str           # what this pair divides
    aurora: str         # where the framework embodies it

    @property
    def summary(self) -> str:
        return (
            f"{self.id} — {self.positive} vs {self.negative}  [{self.kind}]\n"
            f"  derivation: {self.derivation}\n"
            f"  the line:   {self.line}\n"
            f"  in Aurora:  {self.aurora}"
        )


@dataclass(frozen=True)
class AxisPair:
    """A live polarity read off a recorded lattice: the 2 a 4 is built of."""

    quartet_id: str
    axis: str
    poles: tuple[str, str]


def axis_pairs(quartets: Quartets) -> list[AxisPair]:
    """Every quartet axis in the map, as the antonym pair it already is."""
    out: list[AxisPair] = []
    for q in quartets.quartets:
        out.append(AxisPair(quartet_id=q.id, axis=q.row_axis, poles=q.row_poles))
        out.append(AxisPair(quartet_id=q.id, axis=q.col_axis, poles=q.col_poles))
    return out


@dataclass
class Polarities:
    pairs: list[Pair] = field(default_factory=list)
    bound: dict = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def by_id(self, pid: str) -> Pair:
        for p in self.pairs:
            if p.id == pid:
                return p
        raise KeyError(f"unknown pair {pid!r}; have {[p.id for p in self.pairs]}")

    def summary(self, quartets: Quartets | None = None) -> str:
        rows = [self.title or "the polarities", ""]
        for p in self.pairs:
            rows.append(p.summary)
            rows.append("")
        if quartets is not None:
            live = axis_pairs(quartets)
            rows.append(
                f"  the live polarities: {len(live)} axis-pairs across "
                f"{len(quartets.quartets)} lattices -- the 2s the 4s are built of:"
            )
            for ap in live:
                rows.append(f"    {ap.poles[0]} <-> {ap.poles[1]}  ({ap.quartet_id}: {ap.axis})")
        if "the_morpheme_line" in self.bound:
            rows.append(f"  bound: {self.bound['the_morpheme_line']}")
        if "the_guard_on_no" in self.bound:
            rows.append(f"  bound: {self.bound['the_guard_on_no']}")
        rows.append("  a reader, not a ruler: descriptive, never a gate.")
        return "\n".join(rows)


def load_polarities(path) -> Polarities:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    pairs = []
    for e in raw.get("pairs", []):
        kind = e.get("kind", "")
        if kind not in VALID_KINDS:
            raise ValueError(
                f"pair {e.get('id')!r} has kind {kind!r}; the attested typology is "
                f"{VALID_KINDS} -- an unnamed kind of opposition is surfaced, not guessed"
            )
        pairs.append(Pair(
            id=e["id"], positive=e["positive"], negative=e["negative"], kind=kind,
            derivation=e.get("derivation", ""), line=e.get("line", ""),
            aurora=e.get("aurora", ""),
        ))
    return Polarities(
        pairs=pairs,
        bound=raw.get("bound", {}),
        title=raw.get("title", ""),
        note=raw.get("note", ""),
    )
