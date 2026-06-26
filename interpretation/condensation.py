"""Binary thought and relational meaning: compression vs condensation.

Natural computing reads one bit: 0 or 1 — yes/no, signal/noise, true/false,
right/wrong. A bit is a *pure distinction*: it separates two states and carries
nothing else. That is **compression** — meaning squeezed down to the single yes/no
that can be transmitted with perfect fidelity, and is empty of everything but the
cut. It is fixed, singular, and exact, and it is the floor every code rests on.

Human thought is *also* built on the distinction — a word draws a boundary, and its
sharpest form is the **antonym**, the pole a word stands against (light/dark,
justice/injustice). So a word is binary in *structure*: under it lies the same one
bit. But a word does not stop at the cut. Onto that binary skeleton it **condenses**
an associated field — its **synonyms** (the kin it shares meaning with) and its
connections to other concepts — so the single fixed bit acquires a relational,
proportional, *meant* content that the bit alone can never hold. This is the move the
whole framework turns on, read at the level of the word: meaning is not the cut but
the field gathered on it. Condensation is not compression's loss-less squeezing; it is
the opposite gesture — the **accretion of associated sense around a distinction**, so
one token carries far more than one bit.

And the field is not assembled at once. Language is the **compounded creation of
meaning over time**: a later word is defined in terms of earlier ones (the lexicon's
`defined_in_terms_of` web, read here as compounding), so a word's meaning is its whole
ancestry compounded into it — *wellbeing* condenses *flow* and *freedom*, which
condense *self* and *justice*, down to *water* and *fire*. The deeper that ancestry,
the more time has been condensed into the one token.

This module reads, for a single term, the two facets named above — its
**compression** (the binary pole it sets up: one bit) and its **condensation** (the
associated field and the compounded ancestry gathered upon that bit) — and reads the
**connection** between two terms as either an *antonym* (the binary axis: a
distinction) or a *synonym* (condensed meaning shared). The relations are an
**authored map** (`relations.json`), a proxy carrying its provenance, not a real
thesaurus; the compounding is read from the lexicon. Like every measure here but
attestation, it is **descriptive, never a gate**. Pure standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .lexicon import Lexicon

# The kinds of meaning-connection between two terms.
RELATION_ANTONYM = "antonym"        # opposed poles — the binary axis (a distinction)
RELATION_SYNONYM = "synonym"        # kin — condensed meaning shared
RELATION_ASSOCIATE = "associate"    # connected by a shared field, neither pole nor kin
RELATION_NONE = "unconnected"       # no recorded meaning-connection

# How a term sits on the compression/condensation contrast.
KIND_BIT = "bit"                    # a pole, no field: pure compression (the 0/1 floor)
KIND_CONDENSED = "condensed"        # a pole, with a field condensed upon it (a word)
KIND_UNPOLARISED = "unpolarised"    # a field, but no clean opposite on record


@dataclass(frozen=True)
class Term:
    """One term and its authored meaning-connections.

    `antonyms` are the poles it stands against (its binary structure); `synonyms`
    the kin it shares meaning with; `associates` looser connections. The lists are a
    proxy — an authored map of how a term sits among others, not a real thesaurus.
    """

    id: str
    word: str
    gloss: str = ""
    antonyms: tuple[str, ...] = ()
    synonyms: tuple[str, ...] = ()
    associates: tuple[str, ...] = ()


@dataclass
class Relations:
    """The authored map of meaning-connections, with symmetric adjacency.

    A connection declared one way is read both ways: if *a* names *b* as an antonym,
    *b* is an antonym of *a*, even when *b* has no entry of its own — so a bare pole
    (e.g. *noise* against *signal*) need not be spelled out twice.
    """

    terms: dict[str, Term] = field(default_factory=dict)
    title: str = ""
    note: str = ""
    _ant: dict[str, set[str]] = field(default_factory=dict, repr=False)
    _syn: dict[str, set[str]] = field(default_factory=dict, repr=False)
    _assoc: dict[str, set[str]] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        for t in self.terms.values():
            self._ant.setdefault(t.id, set()).update(t.antonyms)
            self._syn.setdefault(t.id, set()).update(t.synonyms)
            self._assoc.setdefault(t.id, set()).update(t.associates)
            for other in t.antonyms:
                self._ant.setdefault(other, set()).add(t.id)
            for other in t.synonyms:
                self._syn.setdefault(other, set()).add(t.id)
            for other in t.associates:
                self._assoc.setdefault(other, set()).add(t.id)

    def known(self, term_id: str) -> bool:
        return term_id in self.terms

    def term(self, term_id: str) -> Term:
        if term_id not in self.terms:
            raise KeyError(f"unknown term {term_id!r}")
        return self.terms[term_id]

    def antonyms_of(self, term_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._ant.get(term_id, set())))

    def synonyms_of(self, term_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._syn.get(term_id, set())))

    def associates_of(self, term_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._assoc.get(term_id, set())))


def load_relations(path) -> Relations:
    """Load the authored relations map (JSON) into a Relations."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    terms = {
        t["id"]: Term(
            id=t["id"],
            word=t.get("word", t["id"]),
            gloss=t.get("gloss", ""),
            antonyms=tuple(t.get("antonyms", ())),
            synonyms=tuple(t.get("synonyms", ())),
            associates=tuple(t.get("associates", ())),
        )
        for t in raw.get("terms", [])
    }
    return Relations(terms=terms, title=raw.get("title", ""), note=raw.get("note", ""))


def _compound(start: str, lexicon: Lexicon) -> tuple[tuple[str, ...], str, int | None, int | None]:
    """The transitive `defined_in_terms_of` ancestry of `start`, oldest first.

    Language is the compounded creation of meaning over time: a word's meaning is the
    whole web of earlier words it is built from. Returns the ancestry (excluding
    `start`, ordered oldest year first), the oldest ancestor, its year, and `start`'s
    own year — so the *span* of years compounded into the term can be read.
    """
    lex = lexicon.lexemes
    start_year = lex[start].year if start in lex else None
    seen: set[str] = set()
    frontier = [start]
    while frontier:
        cur = frontier.pop()
        for dep in lex[cur].defined_in_terms_of if cur in lex else ():
            if dep in lex and dep not in seen and dep != start:
                seen.add(dep)
                frontier.append(dep)
    ordered = tuple(sorted(seen, key=lambda i: (lex[i].year, i)))
    oldest = ordered[0] if ordered else ""
    oldest_year = lex[oldest].year if oldest else None
    return ordered, oldest, oldest_year, start_year


@dataclass
class Condensation:
    """One term read on the compression/condensation contrast.

    `poles` is the binary axis the term sets up (compression — one bit); `field` is
    the associated lexical meaning gathered upon it (synonyms + associates); `compound`
    is the term's definitional ancestry (meaning compounded over time). The headline
    is the contrast: a bit holds compression and no condensation; a word keeps the
    bit and condenses a field on it.
    """

    word: str
    gloss: str = ""
    poles: tuple[str, ...] = ()
    kin: tuple[str, ...] = ()
    associates: tuple[str, ...] = ()
    compound: tuple[str, ...] = ()
    oldest: str = ""
    oldest_year: int | None = None
    term_year: int | None = None

    @property
    def field(self) -> tuple[str, ...]:
        """The associated lexical meaning beyond the bit (synonyms + associates)."""
        return tuple(sorted(set(self.kin) | set(self.associates)))

    @property
    def compression(self) -> int:
        """The binary skeleton: 1 bit if the term sets up a pole, else 0."""
        return 1 if self.poles else 0

    @property
    def condensation(self) -> int:
        """Distinct meanings condensed onto the distinction: field + compounded ancestry."""
        return len(self.field) + len(self.compound)

    @property
    def ratio(self) -> float | None:
        """Condensation per bit of compression — how much meaning rides on the one
        yes/no. None when the term is unpolarised (no bit to ride on)."""
        return float(self.condensation) if self.compression else None

    @property
    def span(self) -> int | None:
        """The years of meaning compounded into the term (oldest ancestor -> term)."""
        if self.term_year is None or self.oldest_year is None:
            return None
        return self.term_year - self.oldest_year

    @property
    def kind(self) -> str:
        if not self.poles:
            return KIND_UNPOLARISED
        return KIND_BIT if self.condensation == 0 else KIND_CONDENSED

    @property
    def verdict(self) -> str:
        poles = "|".join((self.word, *self.poles)) if self.poles else self.word
        if self.kind == KIND_BIT:
            return (f"BIT: '{self.word}' is pure compression — the distinction {poles}, "
                    f"one bit, no field condensed upon it")
        if self.kind == KIND_UNPOLARISED:
            return (f"UNPOLARISED: '{self.word}' carries a field of {self.condensation} "
                    f"meaning(s) but no clean opposite on record")
        return (f"CONDENSED: '{self.word}' keeps the bit ({poles}) and condenses "
                f"{self.condensation} meaning(s) upon it (ratio {self.ratio:.0f}:1)")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.gloss:
            rows.append(f"  {self.word} — {self.gloss}")
        rows.append(f"  compression (the bit): {self.compression}  "
                    f"[pole(s): {', '.join(self.poles) or '—'}]")
        rows.append(f"  condensation (meaning on the bit): {self.condensation}")
        if self.field:
            rows.append(f"    associated field (synonyms / connections): {', '.join(self.field)}")
        if self.compound:
            span = f" over ~{self.span} year(s)" if self.span is not None else ""
            rows.append(f"    compounded over time{span} from {len(self.compound)} earlier "
                        f"word(s): {', '.join(self.compound)}")
        elif self.term_year is not None:
            rows.append("    compounded over time: no earlier words on record (a primal term)")
        rows.append("  note: the bit is the fixed binary distinction; the field is the relational "
                    "meaning meant upon it. An authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def condense(term: str, relations: Relations, lexicon: Lexicon | None = None) -> Condensation:
    """Read one term as compression (its binary pole) plus condensation (the field and
    compounded ancestry gathered on it).

    The poles, kin and associates are read from the authored relations map; the
    compounded ancestry, when the term is in the lexicon, is read from its
    `defined_in_terms_of` web — language as the compounded creation of meaning over
    time. Descriptive, never a gate.
    """
    t = relations.term(term)
    compound: tuple[str, ...] = ()
    oldest, oldest_year, term_year = "", None, None
    if lexicon is not None and term in lexicon.lexemes:
        compound, oldest, oldest_year, term_year = _compound(term, lexicon)
    return Condensation(
        word=t.word,
        gloss=t.gloss,
        poles=relations.antonyms_of(term),
        kin=relations.synonyms_of(term),
        associates=relations.associates_of(term),
        compound=compound,
        oldest=oldest,
        oldest_year=oldest_year,
        term_year=term_year,
    )


def _meaning_set(term: str, relations: Relations, lexicon: Lexicon | None) -> set[str]:
    """A term's gathered meaning: its field plus any compounded ancestry."""
    out: set[str] = set()
    if relations.known(term):
        out |= set(relations.synonyms_of(term)) | set(relations.associates_of(term))
    if lexicon is not None and term in lexicon.lexemes:
        out |= set(_compound(term, lexicon)[0])
    return out


@dataclass
class Connection:
    """The meaning-connection between two terms: an antonym, a synonym, or neither."""

    a: str
    b: str
    relation: str
    shared: tuple[str, ...] = ()
    overlap: float = 0.0

    @property
    def verdict(self) -> str:
        if self.relation == RELATION_ANTONYM:
            return (f"ANTONYM: {self.a}|{self.b} — opposed poles, the binary axis: "
                    f"one distinction (compression)")
        if self.relation == RELATION_SYNONYM:
            return (f"SYNONYM: {self.a} ~ {self.b} — kin, condensed meaning shared "
                    f"(overlap {self.overlap:.2f})")
        if self.relation == RELATION_ASSOCIATE:
            return (f"ASSOCIATED: {self.a} … {self.b} — connected by a shared field "
                    f"(overlap {self.overlap:.2f})")
        return f"UNCONNECTED: {self.a} and {self.b} — no recorded meaning-connection"

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.shared:
            rows.append(f"  shared meaning: {', '.join(self.shared)}")
        if self.relation == RELATION_ANTONYM:
            rows.append("  an antonym is the word's binary skeleton — the yes/no a bit also "
                        "carries; the meaning is condensed elsewhere, in the field.")
        rows.append("  note: an authored proxy of meaning-connection, descriptive, never a gate.")
        return "\n".join(rows)


def connect(a: str, b: str, relations: Relations, lexicon: Lexicon | None = None) -> Connection:
    """Read the meaning-connection between two terms.

    Antonyms are the *binary axis* (the compression — a single distinction); synonyms
    are *condensed meaning shared* (the relational content). When neither is declared
    but the two share a field, they are *associated*. The overlap is the Jaccard of
    their gathered meanings — a proxy for how much condensed sense they hold in common.
    """
    if not relations.known(a) and not relations.known(b):
        raise KeyError(f"neither term is on the relations map: {a!r}, {b!r}")

    a_set = _meaning_set(a, relations, lexicon)
    b_set = _meaning_set(b, relations, lexicon)
    union = a_set | b_set
    shared = tuple(sorted(a_set & b_set))
    overlap = round(len(a_set & b_set) / len(union), 4) if union else 0.0

    if b in relations.antonyms_of(a) or a in relations.antonyms_of(b):
        relation = RELATION_ANTONYM
    elif b in relations.synonyms_of(a) or a in relations.synonyms_of(b):
        relation = RELATION_SYNONYM
    elif shared:
        relation = RELATION_ASSOCIATE
    else:
        relation = RELATION_NONE
    return Connection(a=a, b=b, relation=relation, shared=shared, overlap=overlap)
