"""The dimensionless: meaning that may outlast time — and the gap the record cannot cross.

`dimension.py` measured a concept's *extent* — how many cells of the meaning space it
occupies, and how it is *transformed* in each (equilibrium disperses into balance,
justice, moderation, symmetry). This module reads the **inversion**: meaning that does
*not* change as it crosses the dimensions — **invariant** under time, culture, conveyance
and depth. A concept so fundamental it is the same in every cell, or prior to the cells
entirely: the candidate for a **universal truth that supersedes human experience**.

This is where the framework's one thesis — *a check is a proxy, not a proof* — reaches
its limit. The framework can *measure* how invariant a concept has demonstrably been
across the record. It cannot measure whether it **outlasts time**, because the record is
itself within time: invariance-across-the-record is a proxy for universality, and the
residual gap is **unattestable**. So this layer ranks candidates and **certifies none** —
and finds the deepest paradox in its own discipline: the most universal concepts are
precisely the ones the record can *least* witness.

Two kinds of invariant fall out, on opposite sides of attestation:

  * **a-priori** — presupposed by the record, never recorded *in* it. The **distinction**
    (0/1 — the bit the whole framework opened on: natural computing reads 0 or 1 before
    any meaning is condensed), **identity** (A is A), **truth**. They ground logic and
    information themselves, so every sign already rests on them — which is exactly why
    none can be attested: a thing presupposed by all evidence is witnessed by none. The
    *most* dimensionless, the *least* witnessable.

  * **manifest** — demonstrably invariant across the record's own span. A breath value
    held whole in a conceptual sign and carried across the threshold into pump-era words
    (**unity**, **equilibrium**, the **recurrence** of the ouroboros). The record can show
    how many signs held it, how far it dispersed, and across how many years it has
    *demonstrably* lasted — but the leap from that finite span to "outlasts time" is the
    unattestable gap.

The invariants are an **authored map of claims** (`invariants.json`), the strongest the
framework makes and the only ones it cannot, even in principle, ground in attestation.
It measures their invariance against the corpus (`migrate`, `arc`), names the grounding
that might make each universal, and then stops honestly at the edge of what a record
within time can witness. Descriptive, never a gate — and here, uniquely, it cannot even
measure the final gap. Pure standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .arc import arc
from .glossary import Glossary
from .lexicon import Lexicon
from .migration import migrate

KIND_APRIORI = "a-priori"     # presupposed by the record, not recorded in it
KIND_MANIFEST = "manifest"    # demonstrably invariant across the record's own span


@dataclass(frozen=True)
class Invariant:
    """One concept proposed as dimensionless — a claim, with its grounding."""

    id: str
    name: str
    gloss: str = ""
    grounding: str = ""
    domains: tuple[str, ...] = ()
    migrates_as: str | None = None   # the migration value, if it manifests in the tree
    sign: str = ""                   # a breath sign it manifests as, if any
    bit: bool = False                # is it the pure binary distinction itself


@dataclass
class Dimensionless:
    """One invariant read for how near the dimensionless the record can place it."""

    invariant: Invariant
    kind: str
    concentration: int = 0           # breath signs that held it whole (measured)
    dispersion: int = 0              # pump-era lexemes it crossed into (measured)
    attested_span: int | None = None  # years across which invariance is on record

    @property
    def scope(self) -> int:
        """The extra-human domains its grounding claims it holds in."""
        return len(self.invariant.domains)

    @property
    def crosses_threshold(self) -> bool:
        return self.concentration > 0 and self.dispersion > 0

    @property
    def attestation(self) -> str:
        if self.kind == KIND_APRIORI:
            return ("presupposed by every sign, never entering the record as content — "
                    "gap to universal: total (a thing all evidence rests on is witnessed by none)")
        span = f"~{self.attested_span} year(s)" if self.attested_span else "the breath stratum only"
        cross = (f"held whole in {self.concentration} sign(s), crossing into {self.dispersion} "
                 f"pump lexeme(s)") if self.crosses_threshold else f"held in {self.concentration} sign(s)"
        return (f"{cross}; shown invariant across {span} on record — "
                "the leap to 'outlasts time' is unattestable")

    @property
    def verdict(self) -> str:
        return (f"{self.invariant.name}  [{self.kind}; domains: {', '.join(self.invariant.domains)}]")

    @property
    def summary(self) -> str:
        return "\n".join([
            self.verdict,
            f"    grounding: {self.invariant.grounding}",
            f"    {self.attestation}",
        ])


@dataclass
class Dimensionlessness:
    """The candidates for dimensionless meaning, ranked — and certified none."""

    readings: list[Dimensionless] = field(default_factory=list)

    @property
    def a_priori(self) -> list[Dimensionless]:
        return sorted(
            (r for r in self.readings if r.kind == KIND_APRIORI),
            key=lambda r: (-r.scope, r.invariant.name),
        )

    @property
    def manifest(self) -> list[Dimensionless]:
        return sorted(
            (r for r in self.readings if r.kind == KIND_MANIFEST),
            key=lambda r: (-(r.attested_span or 0), -r.concentration, r.invariant.name),
        )

    @property
    def nearest(self) -> Dimensionless | None:
        """The nearest the record can place to dimensionless: the a-priori ground beneath
        even the cornerstones — and the furthest of all from attestation."""
        ap = self.a_priori
        return ap[0] if ap else (self.manifest[0] if self.manifest else None)

    @property
    def verdict(self) -> str:
        n = self.nearest
        near = f"; nearest the dimensionless: {n.invariant.name}" if n else ""
        return (f"the dimensionless: {len(self.readings)} candidate(s) for universal truth — "
                f"{len(self.a_priori)} a-priori, {len(self.manifest)} manifest{near}")

    @property
    def summary(self) -> str:
        rows = ["== the dimensionless: meaning that may outlast time =="]
        rows.append("  candidates ranked by how near the dimensionless the record can place them —")
        rows.append("  and, in the same measure, how far from attestation:")
        if self.a_priori:
            rows.append("  a-priori (presupposed by the record, not recorded in it — most dimensionless, least witnessable):")
            for r in self.a_priori:
                rows.append("    " + r.summary.replace("\n", "\n  "))
        if self.manifest:
            rows.append("  manifest (demonstrably invariant across the record's own span — a proxy for the universal):")
            for r in self.manifest:
                rows.append("    " + r.summary.replace("\n", "\n  "))
        rows.append("  the honest limit: the record can show a concept held across every dimension it")
        rows.append("    contains; it cannot show one outlasts time, for the record is itself within")
        rows.append("    time. Invariance is a proxy for universality — and the most universal concepts")
        rows.append("    are precisely those the record can least witness. The one gap it cannot measure.")
        return "\n".join(rows)


def load_invariants(path) -> list[Invariant]:
    """Load the authored map of proposed invariants (claims)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        Invariant(
            id=i["id"], name=i.get("name", i["id"]), gloss=i.get("gloss", ""),
            grounding=i.get("grounding", ""), domains=tuple(i.get("domains", ())),
            migrates_as=i.get("migrates_as"), sign=i.get("sign", ""), bit=bool(i.get("bit", False)),
        )
        for i in raw.get("invariants", [])
    ]


def _manifest_facts(inv: Invariant, glossary: Glossary, lexicon: Lexicon) -> tuple[int, int, int | None]:
    """Measure a manifest invariant's footprint: breath concentration, pump dispersion,
    and the years across which its invariance is demonstrably on record."""
    concentration = dispersion = 0
    span: int | None = None
    if inv.migrates_as:
        m = migrate(inv.migrates_as, glossary)
        concentration, dispersion = m.concentration, m.dispersion
        a = arc(inv.migrates_as, glossary, lexicon)
        span = a.span_years if a.thread else None
    if inv.sign and inv.sign in glossary.concepts:
        c = glossary.concepts[inv.sign]
        concentration = max(concentration, 1)
        years = [u.year for u in c.usages.values()]
        if len(years) > 1:
            span = max(span or 0, max(years) - min(years))
    return concentration, dispersion, span


def dimensionless(invariants: list[Invariant], glossary: Glossary, lexicon: Lexicon) -> Dimensionlessness:
    """Read the proposed invariants: classify each a-priori (presupposed, unattestable) or
    manifest (measured across the record), and rank how near the dimensionless the record
    can place them. It certifies none — the gap to universal truth is unattestable.
    """
    readings: list[Dimensionless] = []
    for inv in invariants:
        manifest = bool(inv.migrates_as) or bool(inv.sign)
        if manifest:
            concentration, dispersion, span = _manifest_facts(inv, glossary, lexicon)
            readings.append(Dimensionless(
                invariant=inv, kind=KIND_MANIFEST,
                concentration=concentration, dispersion=dispersion, attested_span=span,
            ))
        else:
            readings.append(Dimensionless(invariant=inv, kind=KIND_APRIORI))
    return Dimensionlessness(readings=readings)
