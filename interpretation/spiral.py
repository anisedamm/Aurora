"""The spiral (L4): re-coherence, the return arm of the breath -> pump -> nerve cycle.

`migrate` reads a value's *dispersal* across the breath->pump threshold; `spiral` reads
its *return* across the pump->nerve one. Where L3 measures the distance from then to now,
L4 measures whether the segmented pieces come back to a whole - and, crucially, *whether
the return is honest*.

The measure has two facets of resonance (the `cloud` case forced this) times a complexity:

    re-coherence = ( structural , substantive ) x complexity

  * **structural** - does the re-cohered field have the *shape* of the retained truth?
  * **substantive** - is the *living substance* present, or hollowed / harvested / owned?
  * **complexity** - how many differentiated pump shards are held in the one whole.

The verdict is never collapsed to one number. A sign is **faithful** (high on both),
**counterfeit** (structurally a return, substantively hollow - the synthetic breath), or
**mixed**. And it can be **resistant**: a nerve-native origin (no breath whole to return
to) or a refusal of meaning. A `returns_to` reached for rather than grounded in a value
the breath web actually holds is **spiral projection** (`regime.is_spiral_projection`) -
flagged, not honoured. The spiral, like L1 attestation, must be able to *refuse*.

`scatter` is the fragmentation counterpart - the weight a sign carries that re-coheres as
neither shape nor substance, the dis-cohering residue. nerve's other face, measured.

An authored map throughout (`recoherences` in the glossary); descriptive, never a gate.
Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import GatherShard, Glossary, Recoherence
from .regime import BREATH, is_spiral_projection

FACETS_FOR_FULL_COMPLEXITY = 5   # this many re-cohered shards reads as full complexity
FAITHFUL_FLOOR = 0.66            # high on a facet
STRUCTURAL_FLOOR = 0.50          # enough shape to be a return at all
COUNTERFEIT_SUBSTANTIVE_CEIL = 0.40  # substance this low, with shape, is counterfeit

OUTCOME_GLOSS = {
    "faithful": "a faithful synthesis — the segments return to a whole, true to the source",
    "counterfeit": "a counterfeit aggregation — the form of the whole without the life (the synthetic breath)",
    "mixed": "a mixed re-coherence — faithful in one facet, counterfeit in another; the judgement is the human's",
    "resistant": "RESISTANT — no honest return to read; the spiral declines to manufacture one",
}


def returns_for(value: str, glossary: Glossary) -> list[Recoherence]:
    """The nerve signs that re-cohere *toward* `value` - the recoherence entries whose
    `returns_to` names it. The value-scale view of the return (one value, the signs that
    bring it back), as `migrate`/`arc` read the same value's dispersal and climb."""
    out = [rec for rec in glossary.recoherences.values() if value in rec.returns_to]
    return sorted(out, key=lambda r: (r.year, r.sign))


def breath_values(glossary: Glossary) -> set[str]:
    """The values the breath web actually holds (alias-resolved) - the only honest
    targets a `returns_to` can name. Anything else is reached for, not attested."""
    aliases = glossary.value_aliases
    out: set[str] = set()
    for c in glossary.concepts.values():
        if c.regime != BREATH:
            continue
        for k in c.retained_field():
            out.add(aliases.get(k, k))
    return out


def scatter(rec: Recoherence) -> float:
    """The fragmentation degree: the weight that re-coheres as neither shape nor
    substance - the dis-cohering residue. nerve's other face."""
    return round(sum(f.weight * (1.0 - max(f.structural, f.substantive)) for f in rec.carries), 4)


@dataclass
class RecohereReading:
    """The L4 verdict on one nerve sign: the two facets, the complexity, the outcome."""

    sign: str
    returns_to: tuple[str, ...]
    structural: float
    substantive: float
    complexity: float
    scatter: float
    outcome: str           # faithful / counterfeit / mixed / resistant
    grounded: bool
    projection: bool       # a reached-for returns_to (spiral projection)
    provisional: bool

    @property
    def verdict(self) -> str:
        if self.outcome == "resistant":
            why = ("a reached-for return (spiral projection)" if self.projection
                   else "a nerve-native origin: no breath whole to return to")
            return f"re-coherence of '{self.sign}': RESISTANT — {why}"
        prov = " (provisional — the sense is still live)" if self.provisional else ""
        return (
            f"re-coherence of '{self.sign}' -> {', '.join(self.returns_to)}: "
            f"structural {self.structural:.2f} x substantive {self.substantive:.2f}, "
            f"complexity {self.complexity:.2f}, scatter {self.scatter:.2f} "
            f"-> {self.outcome.upper()}{prov}"
        )

    @property
    def summary(self) -> str:
        return f"{self.verdict}\n  {OUTCOME_GLOSS[self.outcome]}"


def recohere(rec: Recoherence, grounded_values: set[str]) -> RecohereReading:
    """Read whether a nerve sign re-coheres - and whether the return is honest.

    `grounded_values` is the set the breath web actually holds (`breath_values`). A
    `returns_to` empty or naming a value the web does not hold cannot be honoured, and the
    reading is `resistant`; otherwise the two-facet verdict is computed. Descriptive.
    """
    asserts = bool(rec.returns_to)
    grounded = asserts and all(v in grounded_values for v in rec.returns_to)
    projection = is_spiral_projection(",".join(rec.returns_to) or None, grounded)

    structural = round(sum(f.weight * f.structural for f in rec.carries), 4)
    substantive = round(sum(f.weight * f.substantive for f in rec.carries), 4)
    complexity = round(min(1.0, len(rec.gathers) / FACETS_FOR_FULL_COMPLEXITY), 4)

    if not grounded:
        outcome = "resistant"
    elif structural >= FAITHFUL_FLOOR and substantive >= FAITHFUL_FLOOR:
        outcome = "faithful"
    elif structural >= STRUCTURAL_FLOOR and substantive < COUNTERFEIT_SUBSTANTIVE_CEIL:
        outcome = "counterfeit"
    else:
        outcome = "mixed"

    return RecohereReading(
        sign=rec.sign, returns_to=rec.returns_to, structural=structural,
        substantive=substantive, complexity=complexity, scatter=scatter(rec),
        outcome=outcome, grounded=grounded, projection=projection,
        provisional=rec.provisional,
    )


@dataclass
class Spiral:
    """A value traced across the whole cycle: held whole, segmented, re-cohered."""

    key: str
    returns_to: tuple[str, ...]
    breath_signs: list[tuple[str, float]] = field(default_factory=list)
    gathers: tuple[GatherShard, ...] = ()
    reading: RecohereReading | None = None
    note: str = ""

    @property
    def summary(self) -> str:
        r = self.reading
        rows = [f"spiral of '{self.key}' across the threshold:"]
        if self.note:
            rows.append(f"  {self.note}")
        held = (", ".join(f"{s} ({w:.2f})" for s, w in self.breath_signs)
                if self.breath_signs else "— (a nerve-native origin: no breath whole held it)")
        rows.append(f"  breath    — held whole in {held}")
        if self.gathers:
            shards = ", ".join(g.term for g in self.gathers)
            rows.append(f"  pump      — segmented into {len(self.gathers)} shard(s): {shards}")
        else:
            rows.append("  pump      — no segmentation to re-cohere")
        if r is not None:
            rows.append(f"  nerve     — {r.verdict}")
            rows.append(f"              {OUTCOME_GLOSS[r.outcome]}")
        rows.append("  note: the breath side is measured; the dispersal and the carried field are "
                    "authored proxies. The spiral can refuse. Descriptive, never a gate.")
        return "\n".join(rows)


def spiral(key: str, glossary: Glossary) -> Spiral:
    """Trace a nerve sign / value across the cycle: which breath signs held the value it
    returns to (measured), the pump shards it re-coheres, and the re-coherence verdict.

    `key` is a `recoherences` entry id (e.g. 'viral', 'equilibrium', 'spam')."""
    if key not in glossary.recoherences:
        raise KeyError(
            f"unknown recoherence {key!r}; have {sorted(glossary.recoherences)}"
        )
    from .migration import migrate   # local import: migration reads recohere from here

    rec = glossary.recoherences[key]
    reading = recohere(rec, breath_values(glossary))

    signs: dict[str, float] = {}
    for v in rec.returns_to:
        for s, w in migrate(v, glossary).breath_signs:
            signs[s] = max(signs.get(s, 0.0), w)
    breath_signs = sorted(signs.items(), key=lambda kv: (-kv[1], kv[0]))

    return Spiral(
        key=key, returns_to=rec.returns_to, breath_signs=breath_signs,
        gathers=rec.gathers, reading=reading, note=rec.note,
    )
