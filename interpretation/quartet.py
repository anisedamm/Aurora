"""The quartets: the synchronic structure of meaning (a 2x2 of crossed polarities).

Tracing live values through the spiral (`regime.py`: breath -> pump -> nerve), they
cluster in **fours**, and each four is a **2x2** -- two crossed polarities, one of which
(clearly, for the cognitive quartets) is the framework's own breath<->pump (whole<->part)
axis. A meaning *at rest* is the crossing of the holistic/analytic polarity with one other.

This module is a **reader, not a ruler** (the `atlas`/`constellation` move): it introduces
no measure and gates nothing. It renders the authored quartet map, names each quartet's
**keystone** -- the undivided whole the 2x2 is the dispersal of -- and carries the
**bound** that keeps the structure honest rather than numerological:

  * it is the **synchronic** structure (a meaning frozen and analysed); the spiral is the
    **diachronic** one. Where meaning becomes temporal it goes triadic (time takes 3) or
    single (duree takes 1) -- the grid is space, time is the axis the cells are traversed
    along;
  * the **singles** (Being, the One, consciousness) refuse to split -- they are the
    horizon of meaning, not a cell;
  * a conceptual **five** is the continuum showing through the grid; irreducible fives
    live in mathematics (the Platonic solids, the quintic), which bounds the 2^n tendency
    rather than breaking it.

The binary measures are **quadratic**: `signal = (chain x manifest) x (grounded x
provenance)`; `re-coherence = (structural x substantive) x (differentiation x coherence)`
-- a binary of binaries, a 2x2 collapsed to one number.

An authored map, a proxy carrying its provenance; descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Quartet:
    """One 2x2: four members at the crossing of two polarities, and its keystone."""

    id: str
    name: str
    keystone: str                       # the undivided whole this 2x2 disperses (the 1 -> 4)
    members: tuple[str, ...]
    row_axis: str
    row_poles: tuple[str, str]
    col_axis: str
    col_poles: tuple[str, str]
    grid: dict[str, str]                # "rowpole/colpole" -> member
    breath_pump_axis: str | None        # which axis is whole<->part, or None where it is soft
    reading: str = ""

    def cell(self, row_pole: str, col_pole: str) -> str:
        return self.grid.get(f"{row_pole}/{col_pole}", "—")

    @property
    def summary(self) -> str:
        labels = [*self.members, *self.row_poles, *self.col_poles]
        w = max((len(x) for x in labels), default=8) + 2
        soft = "" if self.breath_pump_axis else "  (breath<->pump axis implicit, not a primary cross-axis)"
        rows = [
            f"{self.id} — {self.name}",
            f"  keystone: {self.keystone}  (the whole this 2x2 disperses)",
            f"  axes: {self.row_axis} ({'/'.join(self.row_poles)}) x "
            f"{self.col_axis} ({'/'.join(self.col_poles)}){soft}",
            "",
            f"    {'':<{w}}{self.col_poles[0]:<{w}}{self.col_poles[1]:<{w}}",
        ]
        for rp in self.row_poles:
            rows.append(
                f"    {rp:<{w}}{self.cell(rp, self.col_poles[0]):<{w}}"
                f"{self.cell(rp, self.col_poles[1]):<{w}}"
            )
        if self.breath_pump_axis:
            rows.append(f"  whole<->part axis: {self.breath_pump_axis}")
        if self.reading:
            rows.append(f"  reading: {self.reading}")
        return "\n".join(rows)


@dataclass
class Quartets:
    quartets: list[Quartet] = field(default_factory=list)
    number_structure: dict = field(default_factory=dict)
    bound: dict = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def by_id(self, qid: str) -> Quartet:
        for q in self.quartets:
            if q.id == qid:
                return q
        raise KeyError(f"unknown quartet {qid!r}; have {[q.id for q in self.quartets]}")

    @property
    def keystones(self) -> dict[str, str]:
        return {q.id: q.keystone for q in self.quartets}

    @property
    def summary(self) -> str:
        rows = [self.title or "the quartets", ""]
        for q in self.quartets:
            rows.append(q.summary)
            rows.append("")
        ns = self.number_structure
        if ns:
            rows.append("the number-structure (the numbers are the regime operations):")
            for k in ("1", "2", "3", "4", "infinity"):
                if k in ns:
                    label = "∞" if k == "infinity" else k
                    rows.append(f"  {label} — {ns[k]}")
        rows.append(
            "  bound: synchronic only (time refuses the grid; the singles refuse to split; "
            "a conceptual 'five' is the continuum showing through). Descriptive, never a gate."
        )
        return "\n".join(rows)


def _q(e: dict) -> Quartet:
    return Quartet(
        id=e["id"], name=e.get("name", e["id"]), keystone=e.get("keystone", ""),
        members=tuple(e.get("members", ())),
        row_axis=e["row_axis"], row_poles=tuple(e["row_poles"]),
        col_axis=e["col_axis"], col_poles=tuple(e["col_poles"]),
        grid=dict(e.get("grid", {})),
        breath_pump_axis=e.get("breath_pump_axis"),
        reading=e.get("reading", ""),
    )


def load_quartets(path) -> Quartets:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return Quartets(
        quartets=[_q(e) for e in raw.get("quartets", [])],
        number_structure=raw.get("number_structure", {}),
        bound=raw.get("bound", {}),
        title=raw.get("title", ""),
        note=raw.get("note", ""),
    )
