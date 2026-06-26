"""Folding: layers of corroborating depth, until a concept is deemed truth — and woveable.

`condensation.py` gathers meaning *laterally* — the field of associated sense condensed
onto a single distinction (the bit and its synonyms). This module reads the orthogonal
motion the framework was missing: meaning **folded** *vertically* — layer on layer of
**corroborating depth**, each resting on established truth beneath it, until the concept
has gathered enough depth to be **deemed true**.

The two are not the same. Condensation is breadth — how much associated meaning rides on
a distinction. Folding is depth — how many layers of already-established meaning a concept
rests on, each a stratum that corroborates it. A concept that rests, layer beneath layer,
all the way down to the given cornerstones has *folded in* the whole grounding; that
accumulated depth is what lets it be held as true rather than merely asserted.

And folding has **precedence over weaving**. A concept cannot legitimately enter the
relational web (`weave.py` — its antonyms and synonyms, its place among truths) until it
has folded deep enough to cross the **truth threshold**. The order the framework runs on,
made explicit at last:

    attest → condense → **fold** (gain corroborating depth to be deemed true) → weave

Three states fall out, by fold-depth (the number of corroborating layers beneath a
concept, down to the given base):

  * **given** — depth 0: an *axiom*. A cornerstone (`fire`, `kin`) or an a-priori
    distinction (`true`, `signal`): true without folding, because it is what folding
    rests on. It is woveable not by earning depth but by being the ground.
  * **folding** — depth below the threshold: meaning is accruing layers but has *not yet*
    been deemed true. It cannot yet be woven; a connection drawn to it is provisional.
  * **deemed-true** — depth at or above the threshold: folded enough to be held as true,
    and so admissible to the weave. Truth earned by depth.

The threshold is an **authored** number (a proxy for "deep enough to corroborate", not a
proof of truth), and folding, like the rest, is **descriptive**: it *surfaces* whether a
woven concept has been folded to truth — it does not silently block the weave, it reports
where a connection outran its grounding. Pure standard library.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .condensation import Relations, _compound
from .lexicon import Lexicon

# Fold states, by corroborating depth.
GIVEN = "given"              # depth 0: an axiom — true without folding (the ground)
FOLDING = "folding"          # 0 < depth < threshold: gaining depth, not yet deemed true
DEEMED_TRUE = "deemed-true"  # depth >= threshold: folded enough — woveable

# How many corroborating layers a derived concept must fold in to be deemed true.
DEFAULT_TRUTH_THRESHOLD = 3


def _levels(lexicon: Lexicon) -> dict[str, int]:
    """Each concept's fold-depth: the longest chain of grounding beneath it (0 at the
    cornerstones). The level is the number of corroborating layers it rests on."""
    lex = lexicon.lexemes
    memo: dict[str, int] = {}

    def level(cid: str) -> int:
        if cid in memo:
            return memo[cid]
        memo[cid] = 0  # guard against cycles; cornerstones stay 0
        parents = [p for p in lex[cid].defined_in_terms_of if p in lex]
        memo[cid] = 0 if not parents else 1 + max(level(p) for p in parents)
        return memo[cid]

    for cid in lex:
        level(cid)
    return memo


@dataclass(frozen=True)
class Layer:
    """One stratum of a concept's grounding: the supports folded in at a given depth."""

    level: int
    members: tuple[str, ...] = ()

    @property
    def width(self) -> int:
        """How many concepts corroborate at this layer (the breadth of this fold)."""
        return len(self.members)


@dataclass
class Fold:
    """One concept's folded depth: the corroborating layers beneath it, and its truth state."""

    concept: str
    word: str = ""
    fold_depth: int = 0           # corroborating layers beneath it (0 = given/axiom)
    corroboration: int = 0        # total established concepts folded in (the weight of depth)
    layers: list[Layer] = field(default_factory=list)
    status: str = GIVEN
    threshold: int = DEFAULT_TRUTH_THRESHOLD

    @property
    def woveable(self) -> bool:
        """Admissible to the weave: a given axiom, or folded to truth. Never while still
        merely *folding* — a concept cannot be woven before it is deemed true."""
        return self.status != FOLDING

    @property
    def verdict(self) -> str:
        if self.status == GIVEN:
            return (f"GIVEN: '{self.word or self.concept}' is an axiom — true without folding "
                    "(the ground the rest rests on); woveable as given")
        if self.status == FOLDING:
            return (f"FOLDING: '{self.word or self.concept}' has folded {self.fold_depth} "
                    f"layer(s) (< {self.threshold}) — not yet deemed true; not yet woveable")
        return (f"DEEMED TRUE: '{self.word or self.concept}' folded {self.fold_depth} layers of "
                f"depth ({self.corroboration} corroborating concept(s)) — truth earned, woveable")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        for layer in self.layers:
            tag = "the given base" if layer.level == 0 else f"fold {layer.level}"
            rows.append(f"    {tag:<14} {', '.join(layer.members)}")
        rows.append("  note: folding is depth (corroboration), not breadth (condensation); "
                    "the threshold is an authored proxy. Descriptive, never a gate.")
        return "\n".join(rows)


@dataclass
class Folding:
    """The whole tree read by fold-depth: what is given, what is folding, what is deemed true."""

    folds: list[Fold] = field(default_factory=list)
    threshold: int = DEFAULT_TRUTH_THRESHOLD
    provisional: list[str] = field(default_factory=list)   # woven terms not yet folded to truth

    def _by_status(self, status: str) -> list[Fold]:
        return sorted((f for f in self.folds if f.status == status),
                      key=lambda f: (-f.fold_depth, f.word or f.concept))

    @property
    def given(self) -> list[Fold]:
        return self._by_status(GIVEN)

    @property
    def folding(self) -> list[Fold]:
        return self._by_status(FOLDING)

    @property
    def deemed_true(self) -> list[Fold]:
        return self._by_status(DEEMED_TRUE)

    @property
    def deepest(self) -> Fold | None:
        return max(self.folds, key=lambda f: f.fold_depth, default=None)

    @property
    def verdict(self) -> str:
        legit = "legitimate" if not self.provisional else f"{len(self.provisional)} provisional"
        return (f"folding (truth threshold {self.threshold}): {len(self.given)} given, "
                f"{len(self.folding)} folding, {len(self.deemed_true)} deemed true; "
                f"the weave is {legit}")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        deepest = self.deepest
        if deepest is not None:
            rows.append(f"  deepest fold: '{deepest.word}' — {deepest.fold_depth} layers, "
                        f"{deepest.corroboration} corroborating concept(s)")
        rows.append("  folding precedes weaving — a concept earns the web by gaining depth:")
        rows.append(f"    given (axioms, true without folding): "
                    f"{', '.join(f.word for f in self.given) or '—'}")
        rows.append(f"    folding (gaining depth, not yet truth): "
                    f"{', '.join(f.word for f in self.folding) or '—'}")
        rows.append(f"    deemed true (folded ≥ {self.threshold}, woveable): "
                    f"{', '.join(f.word for f in self.deemed_true) or '—'}")
        if self.provisional:
            rows.append(f"  PROVISIONAL — woven before folded to truth: {', '.join(self.provisional)}")
            rows.append("    a connection drawn to a concept that has not yet folded to truth; surfaced, not blocked.")
        else:
            rows.append("  every woven concept is folded to truth or given — the weave rests on earned depth.")
        rows.append("  note: depth corroborates, breadth condenses; the threshold is an authored proxy. "
                    "Descriptive, never a gate.")
        return "\n".join(rows)


def fold(concept: str, lexicon: Lexicon, *, threshold: int = DEFAULT_TRUTH_THRESHOLD,
         levels: dict[str, int] | None = None) -> Fold:
    """Read one concept's folded depth: the corroborating layers beneath it, and whether
    it has folded enough to be deemed true (and so woveable).

    A concept absent from the tree is **given** — an axiom (a cornerstone or an a-priori
    distinction), true without folding. Otherwise its fold-depth is the longest chain of
    grounding beneath it, its corroboration the total established concepts it rests on, and
    its layers the strata of that grounding from the given base upward. Descriptive.
    """
    lex = lexicon.lexemes
    if concept not in lex:
        return Fold(concept=concept, word=concept, fold_depth=0, corroboration=0,
                    status=GIVEN, threshold=threshold)

    levels = levels if levels is not None else _levels(lexicon)
    ancestry = _compound(concept, lexicon)[0]
    depth = levels[concept]
    by_level: dict[int, list[str]] = defaultdict(list)
    for anc in ancestry:
        by_level[levels[anc]].append(lex[anc].word)
    layers = [Layer(level=lv, members=tuple(sorted(by_level[lv]))) for lv in sorted(by_level)]

    if depth == 0:
        status = GIVEN
    elif depth >= threshold:
        status = DEEMED_TRUE
    else:
        status = FOLDING
    return Fold(concept=concept, word=lex[concept].word, fold_depth=depth,
                corroboration=len(ancestry), layers=layers, status=status, threshold=threshold)


def folding(lexicon: Lexicon, relations: Relations | None = None, *,
            threshold: int = DEFAULT_TRUTH_THRESHOLD) -> Folding:
    """Read the whole tree by fold-depth, and audit the weave's legitimacy.

    Every lexeme is folded; if `relations` is given, every woven term is checked — a term
    folded to truth or given is legitimately woveable, while a woven term still merely
    *folding* is **provisional** (woven before it was deemed true). Surfaced, never blocked.
    """
    levels = _levels(lexicon)
    folds = [fold(cid, lexicon, threshold=threshold, levels=levels) for cid in lexicon.lexemes]

    provisional: list[str] = []
    if relations is not None:
        for term in relations.terms:
            f = fold(term, lexicon, threshold=threshold, levels=levels)
            if not f.woveable:                      # folding, but woven in the relations map
                provisional.append(term)
    return Folding(folds=folds, threshold=threshold, provisional=sorted(provisional))
