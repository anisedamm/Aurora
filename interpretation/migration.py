"""Migration: a single value tracked across the breath->pump threshold.

The constellation shows which values a breath web rested on. This closes the loop
to the founding question — *how the pump transition redistributed them*. A value the
breath regime held **whole** (concentrated in a few signs, each carrying it *alongside*
others, in one participatory field) is, after the threshold, **segmented**: the
analytic regime carves it into several separate lexemes, each taking one facet and
usually losing the holism that made it one.

The labrys is the case the whole framework began from: it held *paradoxical
equilibrium* — opposed blades in balance as a single living truth. The pump regime
split that into `balance` (mechanics), `justice` (law), `moderation` (virtue),
`symmetry` (form) — four lexical domains, each keeping a shard, all dropping the
*paradox* of opposites-held-as-one. `migrate` shows both sides: where a value
concentrated when held whole, and the lexemes it dispersed into when meaning was
segmented.

The breath side is computed from the signs (via the harmonised value vocabulary); the
pump side is **authored** (`migrations` in the glossary) — a proxy reading of the
redistribution, surfaced in the map, not a claim of strict etymology. Descriptive,
never a gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .regime import BREATH
from .weighting import WeightedField


def _canonical(raw: dict, aliases: dict) -> dict:
    out: dict[str, float] = {}
    for k, v in raw.items():
        out[aliases.get(k, k)] = out.get(aliases.get(k, k), 0.0) + v
    return out


@dataclass(frozen=True)
class Shard:
    """One pump-era lexeme that carved off a facet of a once-whole value."""

    term: str
    aspect: str
    citation: str = ""
    period: str = ""


@dataclass
class Migration:
    """A value's passage across the threshold: held whole, then dispersed."""

    value: str
    breath_signs: list[tuple[str, float]] = field(default_factory=list)  # (sign, weight)
    breath_weight: float = 0.0
    shards: list[Shard] = field(default_factory=list)
    note: str = ""

    @property
    def concentration(self) -> int:
        """How many breath signs held the value whole."""
        return len(self.breath_signs)

    @property
    def dispersion(self) -> int:
        """How many separate pump-era lexemes the value scattered into."""
        return len(self.shards)

    @property
    def verdict(self) -> str:
        if not self.breath_signs and not self.shards:
            return f"'{self.value}': not found in the breath web, and no dispersal mapped"
        held = (
            f"held whole across {self.concentration} breath sign(s) "
            f"(weight {self.breath_weight:.2f})"
        ) if self.breath_signs else "not load-bearing in the breath web"
        disp = (
            f"dispersed into {self.dispersion} pump-era lexeme(s)"
        ) if self.shards else "dispersal not yet mapped"
        return f"MIGRATION of '{self.value}': {held}; {disp}"

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.note:
            rows.append(f"  {self.note}")
        if self.breath_signs:
            held = ", ".join(f"{s} ({w:.2f})" for s, w in self.breath_signs)
            rows.append(f"  breath side (held whole, with other values): {held}")
        if self.shards:
            rows.append("  pump side (segmented into separate lexemes):")
            for sh in self.shards:
                rows.append(f"    {sh.term:<12} — {sh.aspect}")
        rows.append("  note: the breath side is measured; the dispersal is an authored "
                    "reading of the redistribution, a proxy. Descriptive, never a gate.")
        return "\n".join(rows)


def migrate(value: str, glossary: Glossary, *, regime: str = BREATH) -> Migration:
    """Track `value` from its breath-side concentration to its pump-side dispersal.

    The breath side is computed: which signs of `regime` held the value (in the
    harmonised vocabulary), and with what total weight. The pump side is the authored
    `migrations` entry for the value - the lexemes it scattered into. Descriptive.
    """
    aliases = glossary.value_aliases
    signs: list[tuple[str, float]] = []
    total = 0.0
    for c in sorted(glossary.concepts.values(), key=lambda c: c.id):
        if c.regime != regime or not c.retained_field():
            continue
        canon = WeightedField(_canonical(c.retained_field(), aliases)).normalized()
        if value in canon:
            signs.append((c.id, round(canon[value], 4)))
            total += canon[value]

    entry = glossary.migrations.get(value, {})
    shards = [
        Shard(term=s["term"], aspect=s.get("aspect", ""),
              citation=s.get("citation", ""), period=s.get("period", ""))
        for s in entry.get("shards", [])
    ]
    return Migration(
        value=value, breath_signs=signs, breath_weight=round(total, 4),
        shards=shards, note=entry.get("note", ""),
    )
