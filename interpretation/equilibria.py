"""Equilibrium points: where cultures unite, across geography and medium, on one truth.

The constellation reads which values a single regime's web rested on; `confluence`
weighs independent lineages of *one* sign; `migrate` and `arc` follow *one* value across
the threshold. This module asks the relational question beneath all of them: across
**cultures separated by geography, time, and medium** - a Minoan double axe, an Egyptian
serpent, a Greek cosmogony, and the words of many tongues - where did human understanding
of experience, however it was committed (non-phonetic symbol, myth, or phonetic word),
**unite on the same retained concept**? Those meeting-places are **equilibrium points**.

A truth is united on in **two opposite ways**, one at each end of the density gradient,
and the framework now reads both:

  * **held whole (the breath web, high density).** A breath sign holds a value at high
    density - one mark carrying it *alongside* several other values, all at once. When
    distinct cultures each hold the same value whole, in their own medium, they unite on
    it: *divinity* is held by the Minoan labrys, the Egyptian ankh, and the Greek divine
    order alike. That same space is later **refined** by the pump regime into separate
    explicit words (balance, justice, moderation, symmetry), each carrying one facet
    alone (density 1) - meaning moving from density to refinement, in one space.

  * **named across tongues (the phonetic web, density 1).** The pump regime segments;
    each phonetic word names one concept explicitly. But independent **tongues**,
    separated by geography, converge on naming the *same family of inner experience* -
    Portuguese *saudade*, Welsh *hiraeth* and Romanian *dor* on a longing for the absent;
    Danish *hygge*, Dutch *gezelligheid* and German *Gemütlichkeit* on a cosy
    togetherness. These words are **kin, not identical** (each is precisely
    untranslatable), yet their convergence is an equilibrium point at the *refined* end -
    the union not of holding-whole but of each-naming.

So the two ways of uniting sit at the two ends of the one gradient: the breath cultures
meet by holding a truth whole; the tongues meet by each refining the same experience into
a word. And alongside, **how what was worth translating changed**: a sign's
`committed_because` (why a culture fixed the whole field in a lasting form) beside the
refinements' aspects and the tongues' `valued_for` (what each explicit word was carved off
to name).

The holdings are **measured** from the signs and lexemes; the cultures, the dispersal, and
the cross-tongue kinships are **authored** and surfaced - a proxy for where understanding
converged, never a claim of strict diffusion or that kin words are the same word. A
reader, like the atlas: it introduces no gate and ranks no culture's worth. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .lexicon import Lexicon
from .migration import migrate
from .regime import BREATH, PUMP, SCRIPT_CONCEPTUAL
from .weighting import WeightedField

# A value must unite at least this many *distinct* cultures (or tongues) to be an
# equilibrium point - a union, not one culture holding it in two signs.
MIN_CULTURES = 2

# Media a value can be committed in - the user's list, made a small vocabulary.
SYMBOL = "symbol"   # a non-phonetic conceptual sign (symbology)
MYTH = "myth"       # a remembered state-shift carried as story (mythology)
WORD = "word"       # a phonetic lexeme (phonetic language)

# How a point's cultures unite - the two ends of the density gradient.
HELD_WHOLE = "held-whole"          # high density: each culture held the truth whole
NAMED = "named-across-tongues"     # density 1: each tongue named the same experience

# Expression roles.
HOLDING = "holding"        # a culture/tongue carrying the value
REFINEMENT = "refinement"  # a pump-era word the breath value was segmented into


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
    holds several (high density, meaning held whole); a refined pump word or a single
    tongue's word carries one (density 1, meaning made explicit). `kind` separates the
    holdings (cultures/tongues carrying the value) from the refinements (the dispersal).
    """

    value: str
    source: str       # the sign id, the lexeme id, or the refined term
    label: str        # the sign or word as it reads
    culture: str      # the culture or tongue
    region: str
    medium: str       # symbol / myth / word
    regime: str       # breath / pump
    year: int | None
    density: int      # values held at once (1 = fully refined / explicit)
    kind: str = HOLDING
    rationale: str = ""  # committed_because / valued_for / a refinement's aspect


@dataclass
class Equilibrium:
    """A conceptual equilibrium point: where cultures unite on one retained truth - by
    holding it whole, or by each naming it - and how it moved along the density gradient."""

    value: str
    expressions: list[Expression] = field(default_factory=list)

    @property
    def holdings(self) -> list[Expression]:
        """The cultures/tongues that carry the value - what makes it a union."""
        return [e for e in self.expressions if e.kind == HOLDING]

    @property
    def refinements(self) -> list[Expression]:
        """The explicit single-value words a held-whole value was segmented into."""
        return [e for e in self.expressions if e.kind == REFINEMENT]

    @property
    def cultures(self) -> list[str]:
        """The distinct cultures/tongues that hold the value - the union."""
        return sorted({e.culture for e in self.holdings if e.culture})

    @property
    def regions(self) -> list[str]:
        return sorted({e.region for e in self.holdings if e.region})

    @property
    def media(self) -> list[str]:
        return sorted({e.medium for e in self.expressions})

    @property
    def hold_density(self) -> float:
        """The mean density of the holdings: >1 when held whole, 1 when each-named."""
        h = self.holdings
        return round(sum(e.density for e in h) / len(h), 2) if h else 0.0

    @property
    def union_mode(self) -> str:
        """How the cultures unite: holding the truth whole, or each naming it."""
        return HELD_WHOLE if self.hold_density > 1 else NAMED

    @property
    def is_point(self) -> bool:
        """True when distinct cultures/tongues unite on the value - an equilibrium point."""
        return len(self.cultures) >= MIN_CULTURES

    @property
    def span(self) -> tuple[int, int] | None:
        years = [e.year for e in self.holdings if e.year is not None]
        return (min(years), max(years)) if years else None

    @property
    def headline(self) -> str:
        unit = "cultures" if self.union_mode == HELD_WHOLE else "tongues"
        head = f"{self.value:<22} {len(self.cultures)} {unit}: {', '.join(self.cultures)}"
        if self.union_mode == HELD_WHOLE:
            refined = (f"refined into {len(self.refinements)} explicit word(s)"
                       if self.refinements else "its dispersal not yet mapped")
            head += f"  | held density {self.hold_density:.1f} → {refined}"
        else:
            head += "  | each tongue named it (the inner life, refined)"
        return head

    def _sorted_holdings(self) -> list[Expression]:
        return sorted(self.holdings, key=lambda e: (e.year if e.year is not None else 0, e.culture))

    @property
    def summary(self) -> str:
        if self.union_mode == HELD_WHOLE:
            return self._summary_held_whole()
        return self._summary_named()

    def _summary_held_whole(self) -> str:
        rows = [
            f"EQUILIBRIUM POINT '{self.value}': {len(self.cultures)} culture(s) unite on it "
            f"across {', '.join(self.media)} — {', '.join(self.cultures)}"
        ]
        rows.append(f"  held whole at high density (mean {self.hold_density:.1f} values per sign), "
                    "each culture in its own medium:")
        for e in self._sorted_holdings():
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
        worth = next((e.rationale for e in self._sorted_holdings() if e.rationale), "")
        if worth:
            rows.append(f"  what was worth committing, then: \"{worth}\"")
        rows.append("  density moved high→1: one truth held whole across cultures, then "
                    "segmented into explicit words — high density to explicit refinement.")
        rows.append("  note: holdings measured; cultures and dispersal authored, surfaced — "
                    "a proxy for where understanding converged. Descriptive, never a gate.")
        return "\n".join(rows)

    def _summary_named(self) -> str:
        rows = [
            f"EQUILIBRIUM POINT '{self.value}': {len(self.cultures)} tongue(s) converge on "
            f"naming it — {', '.join(self.cultures)}"
        ]
        rows.append("  each tongue independently refined the same experience into its own "
                    "word (density 1):")
        for e in self._sorted_holdings():
            yr = f"{e.year:>6}" if e.year is not None else "     —"
            rows.append(f"    {yr}  {e.culture:<11} {e.medium:<5} {e.label} — {e.rationale}; {e.region}")
        rows.append("  these words are kin, not identical — each tongue's is untranslatable, yet "
                    "they meet on one family of experience: the convergence is the point.")
        rows.append("  where the breath web united by holding a truth whole at high density, the "
                    "tongues unite at the refined end — each naming one facet of the inner life.")
        rows.append("  note: lexemes measured; the cross-tongue kinship is authored, surfaced — "
                    "a proxy for convergence, never a claim the words are the same. Descriptive.")
        return "\n".join(rows)


@dataclass
class Equilibria:
    """The whole field of equilibrium points - where cultures and tongues unite."""

    points: list[Equilibrium] = field(default_factory=list)
    held_local: list[Equilibrium] = field(default_factory=list)  # held/named within one culture

    def point(self, value: str) -> Equilibrium | None:
        for p in self.points:
            if p.value == value:
                return p
        return None

    @property
    def held_whole(self) -> list[Equilibrium]:
        return [p for p in self.points if p.union_mode == HELD_WHOLE]

    @property
    def named(self) -> list[Equilibrium]:
        return [p for p in self.points if p.union_mode == NAMED]

    @property
    def summary(self) -> str:
        rows = [f"conceptual equilibrium points — where cultures unite across geography and "
                f"medium: {len(self.points)} point(s)"]
        if self.held_whole:
            rows.append("  held whole across cultures (breath — high density, then refined):")
            for p in self.held_whole:
                rows.append("    " + p.headline)
        if self.named:
            rows.append("  named across tongues (phonetic — the inner life each tongue refined "
                        "into a word):")
            for p in self.named:
                rows.append("    " + p.headline)
        if self.held_local:
            rows.append("  held, but within a single culture (not yet a union):")
            for p in self.held_local:
                rows.append(f"    {p.value:<22} {p.cultures[0] if p.cultures else '—'} only")
        rows.append("  note: a value unites when distinct cultures hold the same truth whole, or "
                    "distinct tongues each name the same experience — measured holdings,")
        rows.append("        authored cultures and kinships; a reader, not a ruler. Descriptive, "
                    "never a gate.")
        return "\n".join(rows)


def _sign_holdings(glossary: Glossary, regime: str) -> dict[str, list[Expression]]:
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
        # the holding's reason is why the *breath sign* was fixed whole — so take it only
        # from a conceptual usage, never from a phonetic crossing (e.g. divine-order's
        # committed_because lives on the phonetic Theogony, which is a remembrance, not the
        # holding); a myth with no conceptual attestation simply carries no holding-reason.
        rationale = next((u.committed_because for u in conceptual if u.committed_because), "")
        for value in canon:
            by_value.setdefault(value, []).append(Expression(
                value=value, source=c.id, label=label, culture=c.culture, region=c.region,
                medium=medium, regime=regime, year=c.origin_year(), density=density,
                kind=HOLDING, rationale=rationale,
            ))
    return by_value


def _tongue_holdings(lexicon: Lexicon) -> dict[str, list[Expression]]:
    """For each authored kinship family, the tongues that each named that experience.

    A phonetic equilibrium point: distinct, untranslatable words from independent tongues
    that converged on one family of inner experience (the lexicon's `kinships`).
    """
    by_family: dict[str, list[Expression]] = {}
    for family, members in lexicon.kinships.items():
        if family.startswith("_"):
            continue
        member_set = set(members)
        exprs = [
            Expression(
                value=family, source=lx.id, label=lx.word, culture=lx.language,
                region=lx.region, medium=WORD, regime=PUMP, year=lx.year, density=1,
                kind=HOLDING, rationale=lx.valued_for,
            )
            for lx in lexicon.lexemes.values() if lx.concept in member_set
        ]
        if exprs:
            by_family[family] = exprs
    return by_family


def equilibria(glossary: Glossary, lexicon: Lexicon | None = None, *,
               regime: str = BREATH, min_cultures: int = MIN_CULTURES) -> Equilibria:
    """Find the equilibrium points: values distinct cultures/tongues unite on, across media.

    Two kinds, at the two ends of the density gradient. **Held whole**: a breath sign's
    canonical field is *measured* for the values it held and the density it held them at;
    distinct cultures holding the same value whole unite on it, and the **authored**
    dispersal (`migrate`) shows the explicit words it was later refined into. **Named
    across tongues**: distinct tongues that each named the same experience (the lexicon's
    authored `kinships`) unite at the refined end. A value is an equilibrium *point* when
    at least `min_cultures` distinct cultures/tongues hold it; one held within a single
    culture is reported as held-but-local. Descriptive.
    """
    built: list[Equilibrium] = []

    for value, holds in _sign_holdings(glossary, regime).items():
        m = migrate(value, glossary, regime=regime)
        refinements = [
            Expression(value=value, source=sh.term, label=sh.term, culture="", region="",
                       medium=WORD, regime=PUMP, year=None, density=1, kind=REFINEMENT,
                       rationale=sh.aspect)
            for sh in m.shards
        ]
        built.append(Equilibrium(value=value, expressions=holds + refinements))

    if lexicon is not None:
        for family, holds in _tongue_holdings(lexicon).items():
            built.append(Equilibrium(value=family, expressions=holds))

    points = sorted(
        (e for e in built if len(e.cultures) >= min_cultures),
        # held-whole points first, then by breadth of union, density, name
        key=lambda e: (e.union_mode != HELD_WHOLE, -len(e.cultures), -e.hold_density, e.value),
    )
    held_local = sorted(
        (e for e in built if 0 < len(e.cultures) < min_cultures),
        key=lambda e: e.value,
    )
    return Equilibria(points=points, held_local=held_local)
