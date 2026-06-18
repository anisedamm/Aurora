"""The glossary: the authored map of concepts, their attested usages, and senses.

A **concept** (a headword such as *revolution*) is not a meaning; it is a name
under which a history of meanings has gathered. The glossary records, for each
concept:

  * its **senses** over time and how they descend from one another - handed to
    `semantics.SenseLattice` as a diachronic algebra (see `semantics.py`);
  * its **usages** - attested occurrences of the word in a real text at a real
    date, each with the quotation and the citation that grounds it.

The map is **authored**, and it says so: it carries its provenance and is a proxy
for the real history of the word, not the history itself. It is loaded from
`glossary.json`. Pure standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .semantics import SenseLattice, lattice_from_senses


@dataclass(frozen=True)
class Usage:
    """An attested occurrence of a sign at a date - a word, or a conceptual symbol.

    The unit L1-Attestation gates on. A **phonetic** usage is admissible only if the
    word can be shown in a cited quotation. A **conceptual** usage (a breath-era
    symbol such as the labrys) is admissible only if it is shown in a cited material
    `artifact` and carries a non-empty weighted `field` - you cannot read a symbol
    that holds no recorded conceptual content.

    `committed_because` records *why this crossed the threshold into writing at all*:
    what made it profound enough to need a form that outlives word of mouth.
    """

    id: str
    word: str
    quotation: str
    citation: str
    year: int = 0
    period: str = ""
    concept: str = ""
    # the attention axis
    regime: str = "pump"             # breath (holistic) / pump (analytic)
    mode: str = "phonetic"           # conceptual / phonetic
    field: dict = field(default_factory=dict)   # weighted conceptual field (conceptual usages)
    artifact: str = ""               # the material attestation (conceptual usages)
    committed_because: str = ""      # why it was worth translating into a lasting form


@dataclass
class Concept:
    """A headword and the history of meanings gathered under it."""

    id: str
    name: str
    gloss: str
    lattice: SenseLattice
    usages: dict[str, Usage] = field(default_factory=dict)
    regime: str = ""             # the dominant attention regime of the concept
    threshold: int | None = None  # the breath->pump year for this tradition (the ghost lag's edge)

    def usage(self, usage_id: str) -> Usage:
        if usage_id not in self.usages:
            raise KeyError(f"unknown usage {usage_id!r} for concept {self.id!r}")
        return self.usages[usage_id]


@dataclass
class Glossary:
    """The whole authored map: concepts keyed by id, plus a flat usage index."""

    concepts: dict[str, Concept] = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def concept(self, concept_id: str) -> Concept:
        if concept_id not in self.concepts:
            raise KeyError(f"unknown concept {concept_id!r}")
        return self.concepts[concept_id]

    def usage(self, usage_id: str) -> Usage:
        """Find a usage by id across every concept (usage ids are global)."""
        for c in self.concepts.values():
            if usage_id in c.usages:
                return c.usages[usage_id]
        raise KeyError(f"unknown usage {usage_id!r}")

    def lattice_for_usage(self, usage_id: str) -> SenseLattice:
        """The sense lattice of the concept a usage belongs to."""
        return self.concept(self.usage(usage_id).concept).lattice


def from_mapping(raw: dict) -> Glossary:
    """Build a Glossary from a `{title, note, concepts: [...]}` mapping.

    Each concept's senses are validated as a sound order of descent (a malformed
    map raises, listing every problem), so the glossary never quietly holds a
    concept whose history does not form a well-defined lattice.
    """
    concepts: dict[str, Concept] = {}
    for c in raw.get("concepts", []):
        cid = c["id"]
        lattice = lattice_from_senses(c.get("senses", []), concept=cid)
        usages = {
            u["id"]: Usage(
                id=u["id"],
                word=u.get("word", ""),
                quotation=u.get("quotation", ""),
                citation=u.get("citation", ""),
                year=int(u.get("year", 0)),
                period=u.get("period", ""),
                concept=cid,
                regime=u.get("regime", "pump"),
                mode=u.get("mode", "phonetic"),
                field=dict(u.get("field", {})),
                artifact=u.get("artifact", ""),
                committed_because=u.get("committed_because", ""),
            )
            for u in c.get("usages", [])
        }
        concepts[cid] = Concept(
            id=cid,
            name=c.get("name", cid),
            gloss=c.get("gloss", ""),
            lattice=lattice,
            usages=usages,
            regime=c.get("regime", ""),
            threshold=c.get("threshold"),
        )
    return Glossary(concepts=concepts, title=raw.get("title", ""), note=raw.get("note", ""))


def load_glossary(path) -> Glossary:
    """Load an authored glossary (JSON) into a Glossary."""
    return from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))
