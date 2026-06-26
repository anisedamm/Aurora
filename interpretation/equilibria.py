"""Equilibrium points: where cultures unite, across geography and medium, on one truth.

The constellation reads which values a single regime's web rested on; `confluence`
weighs independent lineages of *one* sign; `migrate` and `arc` follow *one* value across
the threshold. This module asks the relational question beneath all of them: across
**cultures separated by geography, time, and medium** - a Minoan double axe, an Egyptian
serpent, a Greek cosmogony, and later the explicit words of the pump regime - where did
human understanding of experience, however it was committed (non-phonetic symbol, myth,
or phonetic word), **unite on the same retained concept**? Those meeting-places are
**equilibrium points**: a single conceptual truth that more than one culture, attending
the world in its own way, arrived at and held.

Two readings sit on each equilibrium point, and they are the user's question made
computable:

  * **the union across cultures** - which cultures (and regions, and media) hold the
    value. A value held by two signs of the *same* culture is held, but it is not yet an
    equilibrium *point*; the point is the **geographic union** of independent cultures on
    one truth. (So *eternity*, held by two Egyptian signs, is reported as held-but-local,
    while *divinity*, carried by Minoan, Egyptian and Greek alike, is a true point.)

  * **high density -> explicit refinement, in the same space of meaning** - a breath sign
    holds the value at **high density**: one mark carrying it *alongside* several other
    values, all at once. The pump regime, attending analytically, **refines** that same
    space into separate explicit words, each carrying one facet alone (density 1). The
    equilibrium point shows both: the value held whole at high density across cultures,
    then segmented into explicit single-value words - meaning moving from density to
    refinement over time, in one conceptual space.

And alongside, **how what was worth translating changed**: the `committed_because` of a
breath sign (why a culture fixed the whole field in a lasting form) set beside the
refinements' aspects (what each explicit word was carved off to name) - the changing
criterion of *what is worth committing to a form that outlives a voice*.

The holdings are **measured** from the signs; the cultures and the dispersal are
**authored**, surfaced here, a proxy throughout - never a claim of strict diffusion or
etymology, only a reading of where understanding converged. A reader, like the atlas: it
introduces no gate and ranks no culture's worth. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .migration import migrate
from .regime import BREATH, PUMP, SCRIPT_CONCEPTUAL
from .weighting import WeightedField

# A value must unite at least this many *distinct* cultures to be an equilibrium point
# (a geographic union, not one culture holding it in two signs).
MIN_CULTURES = 2

# Media a value can be committed in - the user's list, made a small vocabulary.
SYMBOL = "symbol"   # a non-phonetic conceptual sign (symbology)
MYTH = "myth"       # a remembered state-shift carried as story (mythology)
WORD = "word"       # a phonetic lexeme (phonetic language)


def _canonical(raw: dict, aliases: dict) -> dict:
    """Re-express a weighted field in the harmonised value vocabulary (as the
    constellation and migration do), so kin value-names are seen as one value."""
    out: dict[str, float] = {}
    for k, v in raw.items():
        ck = aliases.get(k, k)
        out[ck] = out.get(ck, 0.0) + v
    return out


@dataclass(frozen=True)
class Expression:
    """One culture's expression of a value, in one medium, at one density.

    `density` is how many distinct values the form carries *at once*: a breath sign
    holds several (high density, meaning held whole); a refined pump word carries one
    (density 1, meaning made explicit). `rationale` is why it was worth committing -
    a sign's `committed_because`, or a refinement's aspect.
    """

    value: str
    source: str       # the sign id, or the refined term
    label: str        # the sign or word as it reads
    culture: str
    region: str
    medium: str       # symbol / myth / word
    regime: str       # breath / pump
    year: int | None
    density: int      # values held at once (1 = fully refined / explicit)
    rationale: str = ""


@dataclass
class Equilibrium:
    """A conceptual equilibrium point: where cultures unite on one retained truth, and
    how that truth moved from high-density holding to explicit refinement over time."""

    value: str
    expressions: list[Expression] = field(default_factory=list)

    @property
    def holdings(self) -> list[Expression]:
        """The high-density side: signs that held the value whole (density > 1)."""
        return [e for e in self.expressions if e.density > 1]

    @property
    def refinements(self) -> list[Expression]:
        """The explicit side: single-value words the space was refined into (density 1)."""
        return [e for e in self.expressions if e.density == 1]

    @property
    def cultures(self) -> list[str]:
        """The distinct cultures that held the value whole - the geographic union."""
        return sorted({e.culture for e in self.holdings if e.culture})

    @property
    def regions(self) -> list[str]:
        return sorted({e.region for e in self.holdings if e.region})

    @property
    def media(self) -> list[str]:
        return sorted({e.medium for e in self.expressions})

    @property
    def hold_density(self) -> float:
        """The mean density of the holdings - how whole the value was held, on average."""
        h = self.holdings
        return round(sum(e.density for e in h) / len(h), 2) if h else 0.0

    @property
    def is_point(self) -> bool:
        """True when distinct cultures unite on the value - a geographic equilibrium point."""
        return len(self.cultures) >= MIN_CULTURES

    @property
    def span(self) -> tuple[int, int] | None:
        years = [e.year for e in self.holdings if e.year is not None]
        return (min(years), max(years)) if years else None

    @property
    def headline(self) -> str:
        n = len(self.cultures)
        refined = (f"refined into {len(self.refinements)} explicit word(s)"
                   if self.refinements else "its dispersal not yet mapped")
        return (f"{self.value:<12} {n} cultures: {', '.join(self.cultures)}"
                f"  | held density {self.hold_density:.1f} → {refined}")

    @property
    def summary(self) -> str:
        rows = [
            f"EQUILIBRIUM POINT '{self.value}': {len(self.cultures)} culture(s) unite on it "
            f"across {', '.join(self.media)} — {', '.join(self.cultures)}"
        ]
        rows.append(f"  held whole at high density (mean {self.hold_density:.1f} values per sign), "
                    "each culture in its own medium:")
        for e in sorted(self.holdings, key=lambda e: (e.year if e.year is not None else 0, e.culture)):
            yr = f"{e.year:>6}" if e.year is not None else "     —"
            rows.append(f"    {yr}  {e.culture:<9} {e.medium:<6} {e.label} — "
                        f"held among {e.density} values; {e.region}")
        if self.refinements:
            rows.append(f"  then refined — the same space made explicit — into "
                        f"{len(self.refinements)} single-value word(s) (density 1):")
            for e in self.refinements:
                rows.append(f"    {e.label:<12} — {e.rationale}")
        else:
            rows.append("  its dispersal into explicit words is not yet mapped (held whole, "
                        "honestly not re-traced)")
        worth = next((e.rationale for e in sorted(
            self.holdings, key=lambda e: (e.year if e.year is not None else 0)) if e.rationale), "")
        if worth:
            rows.append(f"  what was worth committing, then: \"{worth}\"")
        rows.append("  density moved high→1: one truth held whole across cultures, then "
                    "segmented into explicit words — high density to explicit refinement.")
        rows.append("  note: holdings measured; cultures and dispersal authored, surfaced — "
                    "a proxy for where understanding converged. Descriptive, never a gate.")
        return "\n".join(rows)


@dataclass
class Equilibria:
    """The whole field of equilibrium points - where cultures unite, ranked by union."""

    points: list[Equilibrium] = field(default_factory=list)
    held_local: list[Equilibrium] = field(default_factory=list)  # held, but within one culture

    def point(self, value: str) -> Equilibrium | None:
        for p in self.points:
            if p.value == value:
                return p
        return None

    @property
    def summary(self) -> str:
        rows = [f"conceptual equilibrium points — where cultures unite across geography and "
                f"medium: {len(self.points)} point(s)"]
        for p in self.points:
            rows.append("  " + p.headline)
        if self.held_local:
            rows.append("  held, but within a single culture (not yet a geographic union):")
            for p in self.held_local:
                rows.append(f"    {p.value:<12} {p.cultures[0] if p.cultures else '—'} only")
        rows.append("  note: a value unites cultures when distinct cultures, each in their own "
                    "medium, hold the same retained truth — measured holdings, authored")
        rows.append("        cultures; a reader, not a ruler. Descriptive, never a gate.")
        return "\n".join(rows)


def _expressions_for_signs(glossary: Glossary, regime: str) -> dict[str, list[Expression]]:
    """For each value, the high-density holdings: the regime's signs that carried it."""
    aliases = glossary.value_aliases
    by_value: dict[str, list[Expression]] = {}
    for c in sorted(glossary.concepts.values(), key=lambda c: c.id):
        retained = c.retained_field()
        if c.regime != regime or not retained:
            continue
        canon = WeightedField(_canonical(retained, aliases)).normalized()
        density = len(canon)
        conceptual = [u for u in c.usages.values() if u.mode == SCRIPT_CONCEPTUAL]
        medium = SYMBOL if conceptual else MYTH
        label = conceptual[0].word if conceptual else c.id
        rationale = next((u.committed_because for u in c.usages.values() if u.committed_because), "")
        for value in canon:
            by_value.setdefault(value, []).append(Expression(
                value=value, source=c.id, label=label, culture=c.culture, region=c.region,
                medium=medium, regime=regime, year=c.origin_year(), density=density,
                rationale=rationale,
            ))
    return by_value


def equilibria(glossary: Glossary, *, regime: str = BREATH,
               min_cultures: int = MIN_CULTURES) -> Equilibria:
    """Find the equilibrium points: values distinct cultures unite on, across media.

    The holdings are **measured** - each sign's canonical field gives the values it held
    and the density it held them at. The refinements are the **authored** dispersal
    (`migrate`) of that value into explicit pump-era words. A value is an equilibrium
    *point* when at least `min_cultures` distinct cultures held it whole; one held by a
    single culture in several signs is reported as held-but-local. Descriptive.
    """
    holdings = _expressions_for_signs(glossary, regime)

    built: list[Equilibrium] = []
    for value, holds in holdings.items():
        m = migrate(value, glossary, regime=regime)
        refinements = [
            Expression(value=value, source=sh.term, label=sh.term, culture="", region="",
                       medium=WORD, regime=PUMP, year=None, density=1, rationale=sh.aspect)
            for sh in m.shards
        ]
        built.append(Equilibrium(value=value, expressions=holds + refinements))

    points = sorted(
        (e for e in built if len(e.cultures) >= min_cultures),
        key=lambda e: (-len(e.cultures), -e.hold_density, e.value),
    )
    held_local = sorted(
        (e for e in built if 0 < len(e.cultures) < min_cultures),
        key=lambda e: e.value,
    )
    return Equilibria(points=points, held_local=held_local)
