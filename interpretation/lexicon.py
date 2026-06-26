"""The lexicon over time: phonetic language as the record of growing understanding.

The breath apparatus reads signs that held meaning whole. This is its pump-side
counterpart: phonetic language does not hold meaning whole, it **proliferates** —
an explosion of words, each a concept a culture deemed worth a name. Traced over
time, that explosion is a record of how human understanding of conceptual meaning
grew, and three things move together within it:

  * **the explosion** — the count of lexicalised concepts climbs era over era;
  * **the sieve->success gradient** — what gets named drifts from *sieve-aligned*
    (a discriminating filter on raw experience: water, danger, kin — concrete
    necessity) toward *success-aligned* (abstract, experiential, aspirational:
    soul, freedom, empathy, wellbeing — what a thriving society values);
  * **coherence and experience together** — words come to be defined in terms of
    earlier words, so the lexicon's definitional web connects; as it coheres, more
    abstract and experiential concepts become sayable, and understanding of human
    experience itself deepens.

Lexicalisation is **valuation**: a concept earns a word when a culture values it
enough (each lexeme's `valued_for`, the phonetic echo of `committed_because`), and
which concepts a *given* tongue named — and others did not — is read by the
`untranslatables`. As ever: an authored map, a proxy carrying its provenance, and
every measure here is descriptive, never a gate. Pure standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

SHARED_LANGUAGE = "shared"


@dataclass(frozen=True)
class Lexeme:
    """One word: a concept a culture valued enough to name, placed in time and regime."""

    id: str
    word: str
    gloss: str
    concept: str
    language: str
    era: str
    year: int
    alignment: float           # sieve(0) -> success(1)
    experiential: bool
    valued_for: str
    defined_in_terms_of: tuple[str, ...] = ()
    region: str = ""           # where the tongue is spoken (authored provenance)


@dataclass
class Lexicon:
    lexemes: dict[str, Lexeme] = field(default_factory=dict)
    title: str = ""
    note: str = ""
    kinships: dict = field(default_factory=dict)  # authored kin-concept families across tongues

    def by_era(self) -> dict[str, list[Lexeme]]:
        out: dict[str, list[Lexeme]] = {}
        for lx in self.lexemes.values():
            out.setdefault(lx.era, []).append(lx)
        return out


def load_lexicon(path) -> Lexicon:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    lexemes = {
        e["id"]: Lexeme(
            id=e["id"], word=e["word"], gloss=e.get("gloss", ""),
            concept=e.get("concept", e["id"]), language=e.get("language", SHARED_LANGUAGE),
            era=e.get("era", ""), year=int(e.get("year", 0)),
            alignment=float(e.get("alignment", 0.0)), experiential=bool(e.get("experiential", False)),
            valued_for=e.get("valued_for", ""),
            defined_in_terms_of=tuple(e.get("defined_in_terms_of", ())),
            region=e.get("region", ""),
        )
        for e in raw.get("lexemes", [])
    }
    return Lexicon(
        lexemes=lexemes, title=raw.get("title", ""), note=raw.get("note", ""),
        kinships=dict(raw.get("kinships", {})),
    )


def _largest_component_fraction(lexemes: list[Lexeme]) -> float:
    """Fraction of these lexemes in the largest connected component of the
    definitional web (defined_in_terms_of as undirected edges) - the coherence of
    the web, in the sibling system's sense: one puzzle vs scattered islands."""
    ids = {lx.id for lx in lexemes}
    if not ids:
        return 0.0
    parent = {i: i for i in ids}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for lx in lexemes:
        for dep in lx.defined_in_terms_of:
            if dep in ids:
                parent[find(lx.id)] = find(dep)
    sizes: dict[str, int] = {}
    for i in ids:
        r = find(i)
        sizes[r] = sizes.get(r, 0) + 1
    return round(max(sizes.values()) / len(ids), 4)


def lexical_coherence(lexicon: Lexicon) -> float:
    """Coherence of the whole lexicon's definitional web."""
    return _largest_component_fraction(list(lexicon.lexemes.values()))


@dataclass
class EraPoint:
    """The state of the lexicon as of one era (cumulative)."""

    era: str
    year: int                  # the era's earliest lexeme year
    new: int                   # lexemes first named in this era
    cumulative: int            # total lexicon size through this era
    mean_alignment: float      # cumulative mean sieve->success alignment
    experiential_share: float  # cumulative fraction naming inner experience
    coherence: float           # cumulative definitional-web coherence


@dataclass
class Proliferation:
    points: list[EraPoint] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        if not self.points:
            return "an empty lexicon"
        a, z = self.points[0], self.points[-1]
        return (
            f"over {len(self.points)} eras the lexicon grew {a.cumulative}->{z.cumulative}; "
            f"sieve->success alignment rose {a.mean_alignment:.2f}->{z.mean_alignment:.2f}; "
            f"experiential share {a.experiential_share:.2f}->{z.experiential_share:.2f}; "
            f"coherence {a.coherence:.2f}->{z.coherence:.2f}"
        )

    @property
    def summary(self) -> str:
        rows = ["the explosion of phonetic language, traced era by era:",
                f"  {'era':<10} {'new':>4} {'total':>6} {'align':>6} {'exp':>5} {'coher':>6}"]
        for p in self.points:
            rows.append(
                f"  {p.era:<10} {p.new:>4} {p.cumulative:>6} {p.mean_alignment:>6.2f} "
                f"{p.experiential_share:>5.2f} {p.coherence:>6.2f}"
            )
        rows.append("  " + self.verdict)
        rows.append("  note: as the definitional web coheres, what can be named climbs from "
                    "concrete survival to inner experience — understanding deepening. Descriptive.")
        return "\n".join(rows)


def proliferation(lexicon: Lexicon) -> Proliferation:
    """Trace the lexicon era by era: the explosion, the sieve->success climb, and
    coherence and experiential share rising together.

    Eras are ordered by their earliest lexeme; each point is *cumulative* (the whole
    lexicon up to and including that era), so the trajectory reads as one growing web.
    """
    by_era = lexicon.by_era()
    eras = sorted(by_era, key=lambda e: min(lx.year for lx in by_era[e]))

    points: list[EraPoint] = []
    cumulative: list[Lexeme] = []
    for era in eras:
        new = by_era[era]
        cumulative = cumulative + new
        n = len(cumulative)
        points.append(EraPoint(
            era=era,
            year=min(lx.year for lx in new),
            new=len(new),
            cumulative=n,
            mean_alignment=round(sum(lx.alignment for lx in cumulative) / n, 4),
            experiential_share=round(sum(1 for lx in cumulative if lx.experiential) / n, 4),
            coherence=_largest_component_fraction(cumulative),
        ))
    return Proliferation(points=points)


@dataclass
class Untranslatable:
    """A concept a single tongue named, that the shared lexicon left unnamed."""

    lexeme: str
    word: str
    language: str
    concept: str
    gloss: str


def untranslatables(lexicon: Lexicon) -> list[Untranslatable]:
    """The concepts a specific language valued enough to name, and others did not.

    A lexeme is 'untranslatable' here when its concept is carried only by one
    specific (non-shared) tongue - no shared word covers it. Differential
    lexicalisation as differential valuation: each tongue names what it holds dear.
    """
    langs_by_concept: dict[str, set[str]] = {}
    for lx in lexicon.lexemes.values():
        langs_by_concept.setdefault(lx.concept, set()).add(lx.language)
    out = []
    for lx in lexicon.lexemes.values():
        langs = langs_by_concept[lx.concept]
        if lx.language != SHARED_LANGUAGE and SHARED_LANGUAGE not in langs and len(langs) == 1:
            out.append(Untranslatable(
                lexeme=lx.id, word=lx.word, language=lx.language,
                concept=lx.concept, gloss=lx.gloss,
            ))
    return sorted(out, key=lambda u: (u.language, u.word))
