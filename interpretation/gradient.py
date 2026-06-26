"""Proportion: the gradient of degrees between two opposed poles.

The first prompt this framework grew from named meaning as *relational, proportional,
associated*. The `weave` gave the **relational** (antonym couples, synonym kin); the
`condensation` gave the **associated** (the field gathered on a distinction). The third —
**proportional** — was missing, and it is the one the bit most flatly denies.

A bit is an opposition collapsed to two points: 0 or 1, signal or noise, no between. The
`weave` keeps that shape — it gives an antonym couple as a binary *axis*, a clean cut. But
most meaning does not live at the poles; it lives *between* them, as a **degree**. Warmth
is not hot-or-cold but a position on a scale; regard is not love-or-hate but a continuum
with indifference at its centre. A gradient **fills the binary axis with proportion** — the
degrees the cut leaves out.

And the centre of a gradient is where this whole framework began. The midpoint (~0.50) is
the **balance** — the mean between the extremes — and that is exactly the point a breath
sign holds as a paradox: the labrys's *opposed blades in balance*, equilibrium. So the
gradient and the paradox (`tension`) are one opposition seen two ways: the paradox **holds**
both poles at once, at the balance point; the gradient **lays out** the degrees between
them, with the balance at its centre. Aristotle's *moderation* — equilibrium's own pump-era
shard, "the mean between extremes" — is literally the midpoint of the deficiency↔excess
gradient. Proportion recovers, as a scale's centre, the balance the breath held whole.

A reading reports an axis's **resolution** (how many degrees it distinguishes — a bit is 2,
the poles alone), its **proportionality** (how far it is from a pure cut), and each term's
**position** between the poles. The closing turn is the deepest: proportion can be found
beneath *any* apparent binary — refuse the cut as final and a continuum opens. The
gradients are an **authored map** (`gradients.json`), a proxy for where degrees fall, not a
measurement; descriptive, never a gate. Pure standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .condensation import Relations

_EPS = 1e-9


@dataclass(frozen=True)
class Step:
    """One degree on a gradient: a term at a proportion between the poles."""

    term: str
    position: float   # 0.0 at the low pole, 1.0 at the high pole


@dataclass
class Gradient:
    """A proportional axis: the ordered degrees between two opposed poles."""

    id: str
    axis: str = ""
    note: str = ""
    steps: list[Step] = field(default_factory=list)

    @property
    def ordered(self) -> list[Step]:
        return sorted(self.steps, key=lambda s: s.position)

    @property
    def poles(self) -> tuple[str, str]:
        o = self.ordered
        return (o[0].term, o[-1].term) if o else ("", "")

    @property
    def resolution(self) -> int:
        """How many degrees the axis distinguishes (a bit is 2 — the poles alone)."""
        return len(self.steps)

    @property
    def proportionality(self) -> float:
        """How far the axis is from a pure cut, in [0,1]: 0 for a bare bit (2 poles),
        rising toward 1 as more degrees fill the continuum."""
        intervals = self.resolution - 1
        return round(1 - 1 / intervals, 4) if intervals >= 1 else 0.0

    @property
    def balance(self) -> Step | None:
        """The degree nearest the midpoint — the mean between the extremes (the balance a
        breath sign holds as a paradox)."""
        return min(self.ordered, key=lambda s: abs(s.position - 0.5), default=None)

    def place(self, term: str) -> float | None:
        """Where a term sits on the axis (its proportion), or None if not on it."""
        for s in self.steps:
            if s.term == term:
                return s.position
        return None

    @staticmethod
    def _bar(position: float, width: int = 11) -> str:
        idx = max(0, min(width - 1, round(position * (width - 1))))
        return "[" + "·" * idx + "●" + "·" * (width - 1 - idx) + "]"

    def summary(self, focus: str = "") -> str:
        lo, hi = self.poles
        rows = [f"GRADIENT '{self.id}' ({lo} ↔ {hi}): {self.resolution} degrees of proportion "
                f"(proportionality {self.proportionality:.2f})"]
        bal = self.balance
        for s in self.ordered:
            tag = ""
            if bal is not None and abs(s.position - 0.5) < _EPS:
                tag = "  ← the balance (the mean between the extremes)"
            elif s.position == 0.0:
                tag = "  (the low pole)"
            elif s.position == 1.0:
                tag = "  (the high pole)"
            mark = " *" if focus and s.term == focus else "  "
            rows.append(f"  {mark}{s.term:<13} {s.position:>4.2f}  {self._bar(s.position)}{tag}")
        if focus and self.place(focus) is not None:
            p = self.place(focus)
            rows.append(f"  '{focus}' sits at {p:.2f} — {p:.0%} toward {hi}, {1 - p:.0%} toward {lo}")
        rows.append("  the axis is a continuum, not a cut: proportion between the poles, "
                    "the midpoint a balance. An authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def load_gradients(path) -> list[Gradient]:
    """Load the authored gradients map (JSON)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Gradient(
            id=g["id"], axis=g.get("axis", g["id"]), note=g.get("note", ""),
            steps=[Step(term=s["term"], position=float(s["position"])) for s in g.get("steps", [])],
        )
        for g in raw.get("gradients", [])
    ]


def find_gradient(key: str, gradients: list[Gradient]) -> tuple[Gradient | None, str]:
    """Resolve `key` to a gradient — by its id, or by any term (pole or degree) on it.
    Returns (gradient, focus-term) where focus is the matched term (or '')."""
    for g in gradients:
        if g.id == key:
            return g, ""
    for g in gradients:
        if g.place(key) is not None:
            return g, key
    return None, ""


@dataclass
class Gradients:
    """The whole reading: which oppositions are proportional, which are bare binaries."""

    proportional: list[Gradient] = field(default_factory=list)
    binaries: list[str] = field(default_factory=list)   # bit axes (a|b) with no gradient

    @property
    def finest(self) -> Gradient | None:
        return max(self.proportional, key=lambda g: g.resolution, default=None)

    @property
    def verdict(self) -> str:
        return (f"proportion: {len(self.proportional)} proportional axis(es), "
                f"{len(self.binaries)} bare binary(ies) (no gradient)")

    @property
    def summary(self) -> str:
        rows = ["== proportion: the gradient between poles (not 0/1 but a degree) ==",
                "  proportional axes (a continuum filled with degrees):"]
        for g in sorted(self.proportional, key=lambda g: (-g.resolution, g.id)):
            lo, hi = g.poles
            bal = g.balance
            b = f"balance: {bal.term} ({bal.position:.2f})" if bal else "—"
            rows.append(f"    {g.id:<12} {lo} ↔ {hi:<12} {g.resolution} degrees; {b}")
        rows.append("  bare binary axes (no proportion — collapsed to two poles, the bit):")
        rows.append(f"    {', '.join(self.binaries) or '—'}")
        rows.append("  the reading: the bit is an axis cut to 0/1; proportion fills it with degrees; "
                    "the midpoint is the balance the breath sign holds (equilibrium = the mean).")
        rows.append("  and the deeper turn: proportion can be found beneath any apparent binary — "
                    "refuse the cut as final, and a continuum opens. Descriptive, never a gate.")
        return "\n".join(rows)


def read_gradients(gradients: list[Gradient], relations: Relations | None = None) -> Gradients:
    """Read the whole proportional picture: the gradients (proportional axes) against the
    bare binary axes of the relations map (a bit — an antonym couple with no field and no
    gradient). Descriptive, never a gate."""
    binaries: list[str] = []
    if relations is not None:
        seen: set[frozenset[str]] = set()
        for tid, t in relations.terms.items():
            if t.antonyms and not (t.synonyms or t.associates):     # a bit
                for pole in t.antonyms:
                    key = frozenset({tid, pole})
                    if key not in seen:
                        seen.add(key)
                        binaries.append("|".join(sorted(key)))
    return Gradients(proportional=list(gradients), binaries=sorted(binaries))
