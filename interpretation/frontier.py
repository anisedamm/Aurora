"""The frontier: meaning at the leaf-edge of the linguistic tree.

The `weave` reads the web's settled structure — the antonym couples (the bits), the
hubs, the keystone the rest are built on. This module reads the opposite place: the
**edge**, where comprehension is still reaching. Three kinds of word live there, and
they are the same kind seen from three sides:

  * **no absolute antonym** (unpolarised) — the word draws no clean distinction. It does
    not carve the world into this-against-that; it names a *positive presence*, a state
    or perception held in itself. Where a bit is all boundary and no content, these
    words are all content and no boundary.

  * **minimal or no synonyms** (singular) — no other word can stand in for it, so it
    cannot be compressed away. It carries meaning nothing else carries: maximal
    information in the plainest sense — zero redundancy. A bit is maximally
    redundant (any yes/no will do); a singular word is irreplaceable.

  * **a leaf of the tree** — nothing is yet *defined in terms of* it (the lexicon's
    `defined_in_terms_of` web, read as a tree). It sits at the growing tip: a word
    language has reached but not yet built upon. The interior of the tree is
    comprehended and load-bearing; the leaves are the frontier.

A word that is all three — an unpolarised, singular, experiential leaf — is meaning at
**the frontier of comprehended knowledge we can communicate**: an abstract
representation of contextual perception, named once, not yet woven into the web of
oppositions and equivalences. The untranslatables are the paradigm (*saudade*, *hygge*,
*ubuntu*, the wordless shared look of *mamihlapinatapai*): a tongue reached a perception
precise enough to name and singular enough that no other word, in any tongue on the map,
carries it.

Being unpolarised or singular is *not* enough — *time* has no antonym yet sits deep in
the interior, long since comprehended and built upon. The frontier is where unpolarised
*and* singular *and* leaf *and* experiential meet: a perception held at the edge of what
language has managed to say. Read from the lexicon (the tree) and the authored relations
(the polarity/synonymy); the map's *silence* about a word — no opposite, no equivalent —
is itself the mark of the frontier, and an authored proxy, not a proof. Descriptive,
never a gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .condensation import Relations, _compound
from .lexicon import Lexicon

# Factors that pull a word back from the frontier (a product, like the rest of the
# framework: any pull toward the settled interior lowers the score).
_INTERIOR = 0.4      # not a leaf: the tree has already grown past it
_CONCRETE = 0.5      # not experiential: a settled abstraction, not a perception
_POLARISED = 0.6     # carries an absolute antonym: a distinction has been drawn around it


@dataclass(frozen=True)
class FrontierWord:
    """One lexeme placed relative to the frontier of the tree."""

    word: str
    gloss: str = ""
    year: int = 0
    alignment: float = 0.0
    experiential: bool = False
    leaf: bool = False           # nothing defined in terms of it — a tip of the tree
    downstream: int = 0          # how many words are built on it (0 = leaf)
    depth: int = 0               # how much it is built on (compounded ancestry)
    polarised: bool = False      # has an absolute antonym on record
    singularity: float = 1.0     # 1 - synonym redundancy; 1.0 = irreplaceable
    score: float = 0.0           # frontier score (a product; 1.0 = furthest out)

    @property
    def unpolarised(self) -> bool:
        return not self.polarised

    @property
    def singular(self) -> bool:
        return self.singularity >= 1.0

    @property
    def nature(self) -> str:
        if self.leaf and self.experiential and self.unpolarised and self.singular:
            return "a singular perception, unwoven — pure frontier"
        if self.leaf and self.experiential:
            return "an experiential edge, partly woven in (an opposite or an equivalent on record)"
        if self.leaf:
            return "a settled abstraction at the edge (a leaf, but not a perception)"
        if self.unpolarised and self.singular:
            return "unpolarised and singular, but deep interior — long since comprehended"
        return "interior: built upon, woven into the web"


@dataclass
class Frontier:
    """The leaf-edge of the linguistic tree, where comprehension is still reaching."""

    words: list[FrontierWord] = field(default_factory=list)  # all lexemes, score-desc

    @property
    def frontier(self) -> list[FrontierWord]:
        """The reaching edge: experiential leaf-words, most-frontier first."""
        return [w for w in self.words if w.leaf and w.experiential]

    @property
    def pure(self) -> list[FrontierWord]:
        """The frontier proper: unpolarised *and* singular experiential leaves —
        a perception not yet woven into any opposition or equivalence."""
        return [w for w in self.frontier if w.unpolarised and w.singular]

    @property
    def leading(self) -> FrontierWord | None:
        """The word furthest out — the most frontier of all."""
        return self.frontier[0] if self.frontier else None

    @property
    def settled_unpolarised(self) -> list[FrontierWord]:
        """The contrast: words with no antonym that are nonetheless deep interior —
        unpolarised does not mean frontier."""
        return [w for w in self.words if w.unpolarised and w.singular and not w.leaf]

    @property
    def verdict(self) -> str:
        lead = self.leading
        tip = f"; furthest out: {lead.word}" if lead else ""
        return (f"the frontier of the tree: {len(self.frontier)} experiential leaf-word(s), "
                f"{len(self.pure)} unwoven (no antonym, no synonym){tip}")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        rows.append("  the reaching edge (leaf, experiential — abstract perception newly named):")
        for w in self.frontier:
            pole = "no-antonym" if w.unpolarised else "polarised"
            syn = "no-synonym" if w.singular else f"redund {1 - w.singularity:.2f}"
            rows.append(f"    {w.word:<18} {w.year:>5}  align {w.alignment:.2f}  "
                        f"{pole:<10} {syn:<12}  score {w.score:.2f}  — {w.nature}")
        lead = self.leading
        if lead is not None:
            rows.append(f"  furthest out: '{lead.word}' — {lead.gloss}")
            rows.append("    a leaf with no opposite and no equivalent: meaning at the edge of "
                        "what language has managed to say.")
        settled = self.settled_unpolarised
        if settled:
            shown = ", ".join(w.word for w in settled[:6])
            more = f", … (+{len(settled) - 6})" if len(settled) > 6 else ""
            rows.append(f"  contrast — unpolarised but interior (no antonym, yet long comprehended): {shown}{more}")
            rows.append("    lacking an opposite is not the frontier; being a leaf is.")
        rows.append("  note: the map's silence — no opposite, no equivalent — marks the frontier; "
                    "an authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def _downstream(lexicon: Lexicon) -> dict[str, int]:
    """How many lexemes are defined in terms of each one (its out-references)."""
    down = {i: 0 for i in lexicon.lexemes}
    for lx in lexicon.lexemes.values():
        for dep in lx.defined_in_terms_of:
            if dep in down:
                down[dep] += 1
    return down


def frontier(lexicon: Lexicon, relations: Relations | None = None) -> Frontier:
    """Read the leaf-edge of the linguistic tree.

    For each lexeme: whether it is a **leaf** (nothing defined in terms of it — the tip),
    how deep its ancestry runs, whether it is **polarised** (has an antonym) and how
    **singular** it is (the fewer synonyms, the more irreplaceable). The frontier score
    is a product — leaf, experiential, unpolarised and singular all push it out; any pull
    toward the settled interior lowers it. Read from the lexicon and the authored
    relations; descriptive, never a gate.
    """
    down = _downstream(lexicon)
    words: list[FrontierWord] = []
    for lid, lx in lexicon.lexemes.items():
        n_syn = len(relations.synonyms_of(lid)) if relations is not None else 0
        polarised = bool(relations.antonyms_of(lid)) if relations is not None else False
        singularity = 1.0 if n_syn == 0 else round(1.0 / (1 + n_syn), 4)
        leaf = down[lid] == 0

        factor = 1.0
        if not leaf:
            factor *= _INTERIOR
        if not lx.experiential:
            factor *= _CONCRETE
        if polarised:
            factor *= _POLARISED
        score = round(factor * singularity * lx.alignment, 4)

        words.append(FrontierWord(
            word=lx.word, gloss=lx.gloss, year=lx.year, alignment=lx.alignment,
            experiential=lx.experiential, leaf=leaf, downstream=down[lid],
            depth=len(_compound(lid, lexicon)[0]), polarised=polarised,
            singularity=singularity, score=score,
        ))
    words.sort(key=lambda w: (-w.score, -w.year, w.word))
    return Frontier(words=words)
