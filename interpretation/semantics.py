"""A diachronic algebra of senses: composition over an authored order of descent.

The sibling *integrity-alignment-system* found a lattice hiding in knowledge: a
concept rests on the concepts it presupposes. Conceptual history holds a
different lattice in the *same shape*. A word's senses do not stand free in time:
a later sense **descends from** an earlier one through an act of semantic change -
the heavens' *revolution* (a cyclical return) is carried over into politics, then
**inverted** after 1789 into an irreversible rupture. Declare those edges of
descent and a word's senses stop being a list and become an algebra you can
compute with.

The carrier is the set of **ancestry-closed sets** of senses (down-sets of the
descent order). Each sense `s` names the principal closed set `ancestry(s)` - `s`
together with every sense it transitively descends from - and the operations are
the lattice's:

  * **combine**  (join):  ancestry(a) ∪ ancestry(b).
    "the whole semantic field the two senses jointly carry."
  * **common**   (meet):  ancestry(a) ∩ ancestry(b).
    "the shared root meaning both senses still carry."
  * **precedes** (order ≤):  ancestry(a) ⊆ ancestry(b).
    "a is ancestral to b - b's meaning was reached *through* a."

Closed sets are closed under union and intersection, so `(senses, combine,
common)` is a bounded distributive lattice. `SemanticField` exposes `|`, `&`,
`<=`, so the algebra reads like algebra.

Each edge of descent carries the **kind** of semantic change that produced it -
the classic typology (Bréal, Bloomfield): broadening, narrowing, metaphor,
metonymy, amelioration, pejoration, and the one conceptual history turns on,
**inversion** (a sense flips into its opposite while the word stays the same).

The same humility the whole framework runs on applies. The operations are
**exact** - proofs about the structure - but the structure is an **authored map**
(`glossary.json`): a human declared which sense descends from which, and that map
is a proxy for the real history of the word, not the history itself. A malformed
order is **surfaced, never silently patched**: a descent **cycle** (a sense
descending from itself) or a **dangling** edge (descent from an unknown sense)
leaves the order undefined, so `validate_senses` reports it and `SenseLattice`
refuses to build. The derived diachronic order is descriptive, never a gate.
Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# The classic typology of semantic change, carried on each edge of descent.
SHIFT_KINDS = frozenset({
    "broadening",     # the sense widens (revolution -> any radical transformation)
    "narrowing",      # the sense contracts to a special case
    "metaphor",       # carried across domains by resemblance (heavens -> politics)
    "metonymy",       # carried by contiguity/association
    "amelioration",   # the sense rises in standing (democracy: mob-rule -> self-rule)
    "pejoration",     # the sense falls in standing
    "inversion",      # the sense flips into its opposite (return -> rupture)
    "abstraction",    # a remembered truth lifted into a more transmissible form (myth)
    "specialisation", # bound to a technical domain
    "generalisation", # loosed from a technical domain
    "descent",        # an unmarked continuation (default)
})


@dataclass(frozen=True)
class Sense:
    """One sense of a word, and the senses it directly descends from."""

    id: str
    label: str
    year: int = 0                      # representative year first attested (BCE negative)
    period: str = ""                   # human-readable period label
    gloss: str = ""
    descends_from: tuple[str, ...] = ()
    shift: str = "descent"             # the kind of change on the edge from its parent(s)
    regime: str = ""                   # the attention regime this sense belongs to (breath/pump)


@dataclass(frozen=True)
class SemanticField:
    """An element of the algebra: an ancestry-closed set of senses.

    Carries a back-reference to its lattice (excluded from equality/hashing, so
    two fields are equal exactly when they cover the same senses) for rendering
    and to refuse cross-lattice operations.
    """

    senses: frozenset[str]
    lattice: "SenseLattice" = field(compare=False, repr=False)

    def __or__(self, other: "SemanticField") -> "SemanticField":
        """combine / join: the field carrying the union of both ancestries."""
        self._same_lattice(other)
        return SemanticField(self.senses | other.senses, self.lattice)

    def __and__(self, other: "SemanticField") -> "SemanticField":
        """common / meet: the shared root meaning both still carry."""
        self._same_lattice(other)
        return SemanticField(self.senses & other.senses, self.lattice)

    def __le__(self, other: "SemanticField") -> bool:
        """precedes: is this sense ancestral to (reached through by) `other`?"""
        self._same_lattice(other)
        return self.senses <= other.senses

    def __lt__(self, other: "SemanticField") -> bool:
        self._same_lattice(other)
        return self.senses < other.senses

    def __contains__(self, sense_id: str) -> bool:
        return sense_id in self.senses

    def _same_lattice(self, other: "SemanticField") -> None:
        if other.lattice is not self.lattice:
            raise ValueError("cannot compose senses from different lattices")

    @property
    def order(self) -> list[str]:
        """A descent-respecting order over the field's senses - one sequence in
        which they could have arisen (deterministic; year then id break ties)."""
        return self.lattice.diachronic_order(self.senses)

    @property
    def tip(self) -> list[str]:
        """The latest senses - those nothing else in the field descends from."""
        ancestral = {
            anc
            for sid in self.senses
            for anc in self.lattice.senses[sid].descends_from
            if anc in self.senses
        }
        return sorted(self.senses - ancestral)

    @property
    def summary(self) -> str:
        if not self.senses:
            return "no sense (the empty field)"
        names = " -> ".join(self.lattice.senses[s].label for s in self.order)
        return f"{len(self.senses)} sense(s): {names}"


def validate_senses(raw_senses: list[dict]) -> list[str]:
    """Report what stops a sense map from forming a well-defined order of descent.

    Surfaces, never resolves: **dangling** descent (an edge to an unknown sense),
    **self-loops**, and descent **cycles**. An empty list means the map is a sound
    DAG. Also flags an **unknown shift kind**, so the typology stays honest.
    """
    ids = [s["id"] for s in raw_senses]
    issues: list[str] = []

    seen: set[str] = set()
    for sid in ids:
        if sid in seen:
            issues.append(f"duplicate sense id: {sid!r}")
        seen.add(sid)

    descends = {s["id"]: list(s.get("descends_from", [])) for s in raw_senses}
    for sid, parents in descends.items():
        for p in parents:
            if p == sid:
                issues.append(f"sense {sid!r} descends from itself")
            elif p not in seen:
                issues.append(f"sense {sid!r} descends from unknown sense {p!r} (dangling)")

    for s in raw_senses:
        shift = s.get("shift", "descent")
        if shift not in SHIFT_KINDS:
            issues.append(f"sense {s['id']!r}: unknown shift kind {shift!r}")

    # Cycle detection over the known edges (dangling already reported).
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {sid: WHITE for sid in seen}

    def walk(start: str) -> None:
        stack = [(start, iter(descends.get(start, ())))]
        colour[start] = GREY
        while stack:
            node, it = stack[-1]
            advanced = False
            for nxt in it:
                if nxt not in colour:
                    continue
                if colour[nxt] == GREY:
                    issues.append(f"descent cycle through {nxt!r}")
                    continue
                if colour[nxt] == WHITE:
                    colour[nxt] = GREY
                    stack.append((nxt, iter(descends.get(nxt, ()))))
                    advanced = True
                    break
            if not advanced:
                colour[node] = BLACK
                stack.pop()

    for sid in seen:
        if colour[sid] == WHITE:
            walk(sid)

    out: list[str] = []
    for msg in issues:
        if msg not in out:
            out.append(msg)
    return out


@dataclass
class SenseLattice:
    """A lattice of a word's senses over an authored order of descent.

    Build it from a list of sense mappings (or via `Glossary`). Construction
    **refuses a malformed map** - any cycle, dangling edge or self-loop raises,
    with the same message `validate_senses` reports - so every operation runs on a
    guaranteed sound DAG.
    """

    senses: dict[str, Sense]
    concept: str = ""
    _ancestry: dict[str, frozenset[str]] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        for sid in self.senses:
            self._ancestry[sid] = self._compute_ancestry(sid)

    def _compute_ancestry(self, sid: str) -> frozenset[str]:
        seen: set[str] = set()
        stack = [sid]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(self.senses[cur].descends_from)
        return frozenset(seen)

    def ancestry(self, sense_id: str) -> frozenset[str]:
        """`sense_id` and every sense it transitively descends from."""
        if sense_id not in self.senses:
            raise KeyError(f"unknown sense: {sense_id!r}")
        return self._ancestry[sense_id]

    def field_of(self, sense_id: str) -> SemanticField:
        """The principal field named by a sense: its full ancestry."""
        return SemanticField(self.ancestry(sense_id), self)

    @property
    def bottom(self) -> SemanticField:
        """⊥ - the empty field."""
        return SemanticField(frozenset(), self)

    def _as_field(self, item) -> SemanticField:
        if isinstance(item, SemanticField):
            if item.lattice is not self:
                raise ValueError("cannot compose a field from a different lattice")
            return item
        return self.field_of(item)

    def combine(self, *items) -> SemanticField:
        """Join (∨): the field carrying the union of all these ancestries."""
        result = self.bottom
        for it in items:
            result = result | self._as_field(it)
        return result

    def common(self, *items) -> SemanticField:
        """Meet (∧): the root meaning common to all of these."""
        items = list(items)
        if not items:
            return self.bottom
        result = self._as_field(items[0])
        for it in items[1:]:
            result = result & self._as_field(it)
        return result

    def precedes(self, a: str, b: str) -> bool:
        """Order (≤): is `a` ancestral to `b`? (ancestry(a) ⊆ ancestry(b))."""
        return self.field_of(a) <= self.field_of(b)

    def roots(self) -> list[str]:
        """The earliest senses - those that descend from nothing recorded."""
        return sorted(sid for sid, s in self.senses.items() if not s.descends_from)

    def leaves(self) -> list[str]:
        """The latest senses - those nothing else descends from."""
        ancestral = {p for s in self.senses.values() for p in s.descends_from}
        return sorted(sid for sid in self.senses if sid not in ancestral)

    def diachronic_order(self, sense_ids) -> list[str]:
        """A topological order of the ancestry of `sense_ids` (Kahn; year then id
        break ties). Descriptive: one sound order in which the senses could have
        arisen, never a gate."""
        wanted: set[str] = set()
        for sid in sense_ids:
            wanted |= self.ancestry(sid)
        indeg = {
            sid: sum(1 for p in self.senses[sid].descends_from if p in wanted)
            for sid in wanted
        }
        children: dict[str, list[str]] = {sid: [] for sid in wanted}
        for sid in wanted:
            for p in self.senses[sid].descends_from:
                if p in wanted:
                    children[p].append(sid)

        def key(sid: str) -> tuple[int, str]:
            return (self.senses[sid].year, sid)

        ready = sorted((sid for sid, d in indeg.items() if d == 0), key=key)
        order: list[str] = []
        while ready:
            cur = ready.pop(0)
            order.append(cur)
            newly: list[str] = []
            for nxt in children[cur]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    newly.append(nxt)
            if newly:
                ready = sorted(ready + newly, key=key)
        return order

    def shift_into(self, sense_id: str) -> str:
        """The kind of semantic change on the edge into `sense_id` (or 'origin')."""
        s = self.senses[sense_id]
        return s.shift if s.descends_from else "origin"


def lattice_from_senses(raw_senses: list[dict], concept: str = "") -> SenseLattice:
    """Build a SenseLattice from a list of sense mappings, validating first.

    Raises ValueError (listing every problem) if the senses are not a sound DAG,
    so a malformed order of descent can never quietly produce confident answers.
    """
    issues = validate_senses(raw_senses)
    if issues:
        raise ValueError("malformed sense map: " + "; ".join(issues))
    senses = {
        s["id"]: Sense(
            id=s["id"],
            label=s.get("label", s["id"]),
            year=int(s.get("year", 0)),
            period=s.get("period", ""),
            gloss=s.get("gloss", ""),
            descends_from=tuple(s.get("descends_from", ())),
            shift=s.get("shift", "descent"),
            regime=s.get("regime", ""),
        )
        for s in raw_senses
    }
    return SenseLattice(senses=senses, concept=concept)
