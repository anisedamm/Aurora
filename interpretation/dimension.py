"""Dimensional meaning: the tree as a system layered across several axes at once.

Every other reading walks one structure — a sign, a web, the depth of the tree from
cornerstone to frontier. This module steps back to the shape the whole framework has
been building: the **conceptual language tree is the system**, and meaning is not laid
out along a single line but located in a space of several **dimensions**, each a
distinct way meaning is layered. Each conveyance adds a dimension; a concept's
*dimensional meaning* is how much of that space it occupies.

The axes the corpus already carries:

  * **conveyance** — *how* meaning is committed to a lasting form. Two are
    non-phonetic, holding meaning whole: the **symbol** (a breath/conceptual sign — the
    labrys, the ankh) and the **story** (a breath truth carried in phonetic words — a
    myth like the *Theogony*, an alchemical text). One is phonetic: the **word** (a
    pump-era lexeme that spells a sound and defers to a lexicon). Symbols and stories and
    words are three ways of conveying meaning, and each is a dimension the others cannot
    reach: a thing said in a symbol is not the thing said in a word.

  * **culture** — each language/dialect has *its own derivation*. The shared lexicon and
    each distinct tongue (the untranslatables' Portuguese, Nguni, Yaghan, Danish) are
    separate axes of meaning, layered like constellations and webs that need not coincide.

  * **time** — the eras, layered over historical time, beneath which lies the breath
    stratum the threshold divides from.

  * **depth** — the vertical axis the rest of the framework reads: from the cornerstones
    (built on nothing) up through the derived pillars to the frontier (built upon by
    nothing yet).

A concept that lives in only one cell — a single modern shared word, one mode, one
culture, one era — is *flat*. A value carried as a **symbol** in the breath regime and
re-derived as **words** in the pump regime, across several eras, is **cross-dimensional**:
its meaning has extent the flat word's cannot. Those are the values the migration and the
arc already trace (equilibrium, divinity, unity) — read here as occupying the conveyance
dimension in more than one mode. The space is an authored proxy, descriptive, never a
gate: it maps where meaning is layered; it does not rank the layers. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .condensation import _compound
from .glossary import Glossary
from .lexicon import Lexicon
from .migration import migrate
from .regime import BREATH, SCRIPT_CONCEPTUAL

# The conveyance dimension: how meaning is committed to a lasting form.
SYMBOL = "symbol"   # a breath/conceptual sign — holds a weighted field whole (non-phonetic)
STORY = "story"     # a breath truth carried in phonetic words — a myth (non-phonetic in spirit)
WORD = "word"       # a pump-era phonetic lexeme — spells a sound, defers to a lexicon


@dataclass(frozen=True)
class Axis:
    """One dimension of the meaning space, and the distinct positions along it."""

    name: str
    values: tuple[str, ...] = ()

    @property
    def size(self) -> int:
        return len(self.values)


@dataclass
class MeaningSpace:
    """The conceptual language tree read as a multi-dimensional system."""

    conveyance: Axis
    culture: Axis
    time: Axis
    depth_min: int = 0
    depth_max: int = 0
    conveyance_counts: dict[str, int] = field(default_factory=dict)
    cross_dimensional: list[str] = field(default_factory=list)

    @property
    def volume(self) -> int:
        """The cells of the meaning space the tree spans: conveyance × culture × time.
        A scalar proxy for how dimensional the whole system is (depth is the vertical)."""
        return self.conveyance.size * self.culture.size * self.time.size

    @property
    def verdict(self) -> str:
        return (f"the tree as a system: {self.conveyance.size} conveyance mode(s) × "
                f"{self.culture.size} culture(s) × {self.time.size} era(s) = "
                f"{self.volume} cell(s) of dimensional meaning, over depth {self.depth_min}–{self.depth_max}")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        rows.append("  the conveyance dimension (each a way of conveying meaning the others cannot reach):")
        for mode in (SYMBOL, STORY, WORD):
            n = self.conveyance_counts.get(mode, 0)
            kind = "non-phonetic" if mode in (SYMBOL, STORY) else "phonetic"
            rows.append(f"    {mode:<8} {n:>3}  ({kind})")
        rows.append(f"  the culture dimension (each tongue its own derivation): "
                    f"{', '.join(self.culture.values)}")
        rows.append(f"  the time dimension (layered over history, breath stratum beneath): "
                    f"{', '.join(self.time.values)}")
        rows.append(f"  the depth dimension (the vertical): cornerstone {self.depth_min} → frontier {self.depth_max}")
        if self.cross_dimensional:
            rows.append("  cross-dimensional values (carried as symbol AND word — the richest "
                        "dimensional meaning):")
            rows.append(f"    {', '.join(self.cross_dimensional)}")
        rows.append("  note: each conveyance, culture and era is a dimension meaning is layered in; "
                    "an authored proxy of the system's shape, descriptive, never a gate.")
        return "\n".join(rows)


def _conveyance_of(mode: str, concept_regime: str) -> str:
    """Classify a usage's conveyance: a conceptual sign is a symbol; a phonetic usage of
    a breath-regime concept is a story (a breath truth carried in words); otherwise a word."""
    if mode == SCRIPT_CONCEPTUAL:
        return SYMBOL
    return STORY if concept_regime == BREATH else WORD


def meaning_space(glossary: Glossary, lexicon: Lexicon) -> MeaningSpace:
    """Read the whole corpus as a multi-dimensional system: the conveyance modes
    (symbol/story/word), the cultures, the eras, and the depth range — the axes along
    which meaning is layered, and which values cross more than one conveyance mode.

    Symbols and stories are counted from the glossary's signs; words from the glossary's
    phonetic pump usages and every lexicon lexeme. Cultures and eras are the lexicon's
    tongues and strata. Descriptive, never a gate.
    """
    # Conveyance: classify every attested sign, then add the lexicon's words.
    counts = {SYMBOL: 0, STORY: 0, WORD: 0}
    for c in glossary.concepts.values():
        for u in c.usages.values():
            counts[_conveyance_of(u.mode, c.regime)] += 1
    counts[WORD] += len(lexicon.lexemes)

    # Culture: the tongues (shared first, then each distinct tongue).
    langs = sorted({lx.language for lx in lexicon.lexemes.values()},
                   key=lambda l: (l != "shared", l))

    # Time: eras ordered by their earliest lexeme.
    by_era = lexicon.by_era()
    eras = sorted(by_era, key=lambda e: min(lx.year for lx in by_era[e]))

    # Depth: the vertical, from the cornerstones (0) to the deepest frontier leaf.
    depths = [len(_compound(lid, lexicon)[0]) for lid in lexicon.lexemes]
    depth_min, depth_max = (min(depths), max(depths)) if depths else (0, 0)

    # Cross-dimensional: values held as a breath symbol AND dispersed into pump words.
    # Reuse `migrate` so the canonical value vocabulary (value_aliases) is honoured.
    cross = []
    for v in sorted(k for k in glossary.migrations if not k.startswith("_")):
        m = migrate(v, glossary)
        if m.breath_signs and m.shards:       # held as a symbol, dispersed into words
            cross.append(v)

    return MeaningSpace(
        conveyance=Axis("conveyance", (SYMBOL, STORY, WORD)),
        culture=Axis("culture", tuple(langs)),
        time=Axis("time", tuple(eras)),
        depth_min=depth_min,
        depth_max=depth_max,
        conveyance_counts=counts,
        cross_dimensional=cross,
    )
