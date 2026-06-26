"""The cornerstones: meaning at the root-base of the linguistic tree.

`frontier.py` reads the leaf-edge of the tree — words nothing is yet built *on*,
reaching into newly-named perception. This module reads its **dual**: the **root-base**,
the words built on *nothing*, so fundamental and innate that the whole tree rests on them.
If the frontier is where comprehension is still reaching, the cornerstones are where it
*begins* — the base of the depth itself.

A cornerstone is a word with three properties, one kind seen three ways:

  * **a root of the tree** — nothing in its `defined_in_terms_of` ancestry: it is *built
    on nothing*, the floor where depth bottoms out. Where a frontier word has maximal
    depth (a long ancestry) and zero support, a cornerstone has zero depth and maximal
    **support** — the count of words that ultimately rest on it.

  * **innate / given** — it sits at the sieve end of the sieve→success axis: a
    discriminating filter on raw experience (*water*, *fire*, *kin*, *danger*), the
    concrete necessities a creature must tell apart to live. It is not reached by
    abstraction; it is given before abstraction begins.

  * **self-standing** — it needs *no relational associate* to be understood: no antonym
    to define it against, no synonym to stand in for it. *water* means water without an
    opposite. This is the deep symmetry with the frontier: both the cornerstone and the
    frontier word stand without a relational associate, but for opposite reasons — the
    frontier word has none because the web has **not yet reached** it (it reaches
    outward); the cornerstone has none because it is so foundational it **needs** none
    (everything reaches back to it). Same silence on the map, opposite nature.

The base of the depth is the cornerstone the most of the tree rests on. And the honest
contrast the framework always keeps: a word can *feel* fundamental and bear great weight
yet still be **derived** — *time* is built on *season*, which is built on *fire*; it is a
load-bearing **pillar**, not a cornerstone. Being relied upon is not the same as being a
root: the base is what is built on nothing. Read from the lexicon (the tree) and the
authored relations (whether a word needs an associate); an authored proxy, descriptive,
never a gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .condensation import Relations, _compound
from .lexicon import Lexicon

# How much of the tree must rest on a non-root before it counts as a load-bearing pillar.
_PILLAR_SUPPORT = 10


@dataclass(frozen=True)
class CornerstoneWord:
    """One lexeme placed relative to the root-base of the tree."""

    word: str
    gloss: str = ""
    year: int = 0
    era: str = ""
    alignment: float = 0.0
    root: bool = False           # built on nothing — a base of the tree
    depth: int = 0               # how much it is built on (0 = root)
    support: int = 0             # how many words ultimately rest on it (transitive)
    self_standing: bool = True   # needs no relational associate (no antonym, no synonym)
    score: float = 0.0           # cornerstone score (a product; 1.0 = the deepest base)

    @property
    def innate(self) -> float:
        """How sieve-given the word is: 1.0 = pure concrete necessity, 0.0 = abstract."""
        return round(1.0 - self.alignment, 4)

    @property
    def nature(self) -> str:
        if self.root and self.self_standing:
            return "a cornerstone — built on nothing, needs no relational associate: the given base"
        if self.root:
            return "a root with relational associates (a base, but drawn into the web)"
        if self.support >= _PILLAR_SUPPORT:
            return "a derived pillar — load-bearing, but built on earlier words (relied upon, not a root)"
        return "interior: built on earlier words, and built upon in turn"


@dataclass
class Cornerstones:
    """The root-base of the linguistic tree, where depth begins."""

    words: list[CornerstoneWord] = field(default_factory=list)  # all lexemes, score-desc

    @property
    def cornerstones(self) -> list[CornerstoneWord]:
        """The roots: words built on nothing, most-supporting first."""
        return sorted(
            (w for w in self.words if w.root),
            key=lambda w: (-w.support, -w.innate, w.word),
        )

    @property
    def base(self) -> CornerstoneWord | None:
        """The base of the depth itself: the cornerstone the most of the tree rests on."""
        cs = self.cornerstones
        return cs[0] if cs else None

    @property
    def derived_pillars(self) -> list[CornerstoneWord]:
        """The contrast: load-bearing words that are nonetheless built on earlier ones —
        relied upon, but not roots. (A word can feel fundamental yet be derived.)"""
        return sorted(
            (w for w in self.words if not w.root and w.support >= _PILLAR_SUPPORT),
            key=lambda w: (-w.support, w.word),
        )

    @property
    def verdict(self) -> str:
        base = self.base
        b = f"; the base of the depth: {base.word} ({base.support} rest on it)" if base else ""
        return (f"the root-base of the tree: {len(self.cornerstones)} cornerstone(s) "
                f"(built on nothing){b}")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        rows.append("  the cornerstones (built on nothing, innate, self-standing — the given base):")
        for w in self.cornerstones:
            stand = "self-standing" if w.self_standing else "in the web"
            rows.append(f"    {w.word:<8} {w.era:<9} innate {w.innate:.2f}  support {w.support:>2}  "
                        f"{stand:<13}  score {w.score:.2f}  — {w.nature}")
        base = self.base
        if base is not None:
            rows.append(f"  the base of the depth itself: '{base.word}' — {base.gloss}")
            rows.append(f"    {base.support} of the tree's words ultimately rest on it; built on nothing, "
                        "needing no relation: where depth begins.")
        pillars = self.derived_pillars
        if pillars:
            named = ", ".join(f"{w.word} (support {w.support}, depth {w.depth})" for w in pillars)
            rows.append(f"  contrast — derived pillars (load-bearing, yet built on earlier words): {named}")
            rows.append("    being relied upon is not being a root; the base is what is built on nothing.")
        rows.append("  note: the cornerstone and the frontier both stand without a relational associate — "
                    "one needs none, one is not yet reached. An authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def _support(lexicon: Lexicon) -> dict[str, int]:
    """Transitive support: how many lexemes have each word in their ancestry."""
    support = {i: 0 for i in lexicon.lexemes}
    for lid in lexicon.lexemes:
        for anc in _compound(lid, lexicon)[0]:
            if anc in support:
                support[anc] += 1
    return support


def cornerstones(lexicon: Lexicon, relations: Relations | None = None) -> Cornerstones:
    """Read the root-base of the linguistic tree.

    For each lexeme: whether it is a **root** (built on nothing — `defined_in_terms_of`
    empty), how much **support** it bears (how many words transitively rest on it), and
    whether it is **self-standing** (needs no antonym or synonym). The cornerstone score
    is a product — being a root, bearing much of the tree, and being innate (sieve-given)
    all deepen it; depth and abstraction pull it back toward the derived interior. Read
    from the lexicon and the authored relations; descriptive, never a gate.
    """
    support = _support(lexicon)
    max_support = max(support.values()) if support else 1
    words: list[CornerstoneWord] = []
    for lid, lx in lexicon.lexemes.items():
        depth = len(_compound(lid, lexicon)[0])
        root = depth == 0
        n_syn = len(relations.synonyms_of(lid)) if relations is not None else 0
        polarised = bool(relations.antonyms_of(lid)) if relations is not None else False
        self_standing = (n_syn == 0) and not polarised

        root_factor = 1.0 / (1 + depth)
        support_norm = support[lid] / max_support if max_support else 0.0
        innate = 1.0 - lx.alignment
        score = round(root_factor * support_norm * innate, 4)

        words.append(CornerstoneWord(
            word=lx.word, gloss=lx.gloss, year=lx.year, era=lx.era,
            alignment=lx.alignment, root=root, depth=depth, support=support[lid],
            self_standing=self_standing, score=score,
        ))
    words.sort(key=lambda w: (-w.score, w.depth, w.word))
    return Cornerstones(words=words)
