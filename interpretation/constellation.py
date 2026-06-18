"""The constellation: the system-level view of a regime's web of meaning.

A single sign holds a weighted field; a single chain follows one truth. The
constellation lifts to the whole web: across *all* the signs of a regime, which
conceptual **values** were load-bearing — recurring, with weight, across many signs
— and how do the signs cluster by the values they share?

This is "systemic alignment and underlying values retained across time and culture"
made visible. For the breath civilisation it asks: of equilibrium, unity, divinity,
life, sovereignty, eternity..., which carried the society — held across the labrys,
the ankh, the ouroboros, the remembered divine order — and which were particular to
one sign? And which signs are kin, sharing a value-field, versus standing apart?

Two honesty notes, both inherited from the spine. The value vocabulary is harmonised
through the glossary's **authored** `value_aliases` (so *eternity* and
*eternity-continuity* are seen as one value) — a proxy grouping, surfaced in the map,
not hidden in code. And every measure here is **descriptive**: it reports which values
the web rests on and how its signs cluster; it never ranks a value's worth or gates a
sign. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .regime import BREATH
from .weighting import WeightedField

# Two signs whose canonical fields resonate at or above this share enough of a
# value-field to count as kin in the web.
AFFINITY_THRESHOLD = 0.3


def _canonical(raw: dict, aliases: dict) -> dict:
    """Re-express a weighted field in the harmonised value vocabulary."""
    out: dict[str, float] = {}
    for k, v in raw.items():
        ck = aliases.get(k, k)
        out[ck] = out.get(ck, 0.0) + v
    return out


def _components(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[str]]:
    """Connected components (union-find): the clusters the affinity graph forms."""
    parent = {n: n for n in nodes}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    groups: dict[str, list[str]] = {}
    for n in nodes:
        groups.setdefault(find(n), []).append(n)
    return sorted((sorted(g) for g in groups.values()), key=lambda g: (-len(g), g[0]))


@dataclass
class ValueWeight:
    """One conceptual value's standing across the web."""

    value: str
    reach: int      # how many signs carry it
    weight: float   # its total weight summed across signs


@dataclass
class SignAffinity:
    a: str
    b: str
    affinity: float   # resonance of the two signs' canonical fields


@dataclass
class Constellation:
    """The web of one regime's signs, read by the values they share."""

    regime: str
    signs: list[str] = field(default_factory=list)
    values: list[ValueWeight] = field(default_factory=list)     # load-bearing first
    affinities: list[SignAffinity] = field(default_factory=list)  # >= threshold, desc
    clusters: list[list[str]] = field(default_factory=list)

    @property
    def load_bearing(self) -> list[ValueWeight]:
        """Values that recur — present in at least two signs."""
        return [v for v in self.values if v.reach >= 2]

    @property
    def keystone(self) -> ValueWeight | None:
        """The single most load-bearing value (widest reach, then heaviest)."""
        return self.values[0] if self.values else None

    @property
    def islands(self) -> list[str]:
        """Signs that share no value-field strongly enough to join a cluster."""
        return sorted(c[0] for c in self.clusters if len(c) == 1)

    @property
    def summary(self) -> str:
        rows = [
            f"constellation of the {self.regime} web: {len(self.signs)} sign(s), "
            f"{len(self.load_bearing)} load-bearing value(s)"
        ]
        if self.keystone:
            rows.append(f"  keystone value: {self.keystone.value} "
                        f"(reach {self.keystone.reach}, weight {self.keystone.weight:.2f})")
        rows.append("  load-bearing values (carried across signs):")
        for v in self.load_bearing:
            rows.append(f"    {v.value:<12} reach {v.reach}  weight {v.weight:.2f}")
        if self.affinities:
            rows.append("  kinships (signs sharing a value-field):")
            for e in self.affinities:
                rows.append(f"    {e.a} x {e.b}: {e.affinity:.2f}")
        rows.append(f"  clusters: {self.clusters}"
                    + (f"; islands {self.islands}" if self.islands else ""))
        rows.append("  note: which values the web rests on, and how its signs cluster — "
                    "descriptive, never a ranking of worth.")
        return "\n".join(rows)


def constellation(
    glossary: Glossary,
    *,
    regime: str = BREATH,
    affinity_threshold: float = AFFINITY_THRESHOLD,
) -> Constellation:
    """Read a regime's whole web by the conceptual values its signs share.

    A *sign* is a concept of the regime with a retained conceptual field. Each field
    is re-expressed in the harmonised vocabulary (the glossary's `value_aliases`); then
    every value is scored by **reach** (how many signs carry it) and **weight** (its
    total across the web), and every pair of signs by the **affinity** of their fields.
    The affinity graph's connected components are the web's clusters. Descriptive.
    """
    aliases = glossary.value_aliases
    signs = sorted(
        (c for c in glossary.concepts.values() if c.regime == regime and c.retained_field()),
        key=lambda c: c.id,
    )
    fields = {
        c.id: WeightedField(_canonical(c.retained_field(), aliases)).normalized()
        for c in signs
    }

    agg: dict[str, list] = {}
    for f in fields.values():
        for val, w in f.items():
            entry = agg.setdefault(val, [0, 0.0])
            entry[0] += 1
            entry[1] += w
    values = sorted(
        (ValueWeight(v, reach, round(wt, 4)) for v, (reach, wt) in agg.items()),
        key=lambda x: (-x.reach, -x.weight, x.value),
    )

    ids = [c.id for c in signs]
    affinities: list[SignAffinity] = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a = WeightedField(fields[ids[i]]).resonance(WeightedField(fields[ids[j]]))
            if a >= affinity_threshold:
                affinities.append(SignAffinity(ids[i], ids[j], round(a, 4)))
    affinities.sort(key=lambda e: (-e.affinity, e.a, e.b))

    clusters = _components(ids, [(e.a, e.b) for e in affinities])
    return Constellation(
        regime=regime, signs=ids, values=values, affinities=affinities, clusters=clusters
    )
