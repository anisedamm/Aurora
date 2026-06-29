"""The metabolism of meaning: how actively a meaning is worked over time.

The mechanics layer (`inertia.py`) read a meaning as a *body in motion* - its mass,
momentum, the phase-out of its significance. This layer reads it as a *living thing*:
how fast it **metabolises** - turns over, branches, and refines - in the one pursuit the
whole framework takes meaning to be after, *more understanding*. A meaning metabolises in
two registers, and they turn out to be the breath/pump threshold seen once more:

  * **significance metabolism** (the transmission side) - how much significance a truth
    *turns over* as it is carried down its `memory_chain`. Not the net phase-out but the
    total worked: the sum of the absolute changes in significance (`mass x fidelity`)
    across its rememberings, per millennium. A truth that fell to ornament and was
    restored metabolised a great deal; one held flat, very little. This is how a **breath
    sign** lives: it is *transmitted* - remembered, worn, recovered - without ever
    branching, because it holds its meaning whole.

  * **complexity metabolism** (the branching side) - how fast a concept **branches and
    refines** into finer senses. Its sense lattice (`semantics.py`) is the record: the
    count of senses, the descent **branches** between them, the **depth** of the deepest
    refinement, the **kinds** of semantic work done (metaphor, inversion, amelioration,
    abstraction...), and the rate of new senses per century. This is how a **pump
    concept** lives: it *differentiates* - segmenting one word into a history of distinct
    meanings - without being carried as a weighted field.

A **breath** sign transmits but does not branch; a **pump** concept branches but is not
transmitted; and the cosmogonic **divine order** does *both* - a remembered truth that
also climbed a ladder of abstraction across the threshold. So the metabolic split is the
breath/pump distinction read as two ways of pursuing understanding: by **holding** meaning
whole and carrying it, or by **differentiating** it ever finer. Both are the same hunger.

The rates are borrowed-biology **proxies** over the tested chain and lattice - turnover for
how hard a memory worked, branching for how fast a concept refined - never a measure of how
much was truly understood. Descriptive, never a gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .inertia import mass_profile

MILLENNIUM = 1000
CENTURY = 100

# Order the metabolic modes for the web view: the hinge first, then the two single
# modes, then the dormant.
_MODE_ORDER = {"both": 0, "transmitting": 1, "branching": 2, "dormant": 3}


def _depth(lattice) -> int:
    """The longest chain of descent in a sense lattice - the deepest refinement."""
    memo: dict[str, int] = {}

    def d(sid: str) -> int:
        if sid in memo:
            return memo[sid]
        parents = [p for p in lattice.senses[sid].descends_from if p in lattice.senses]
        memo[sid] = 1 + max((d(p) for p in parents), default=0)
        return memo[sid]

    return max((d(sid) for sid in lattice.senses), default=0)


@dataclass
class Metabolism:
    """How actively a meaning is worked: transmitted (significance) and/or branched."""

    concept: str
    # significance metabolism (the transmission side)
    carriers: int
    sig_turnover: float       # total significance worked (sum of |Δ|), in bits
    sig_span: int             # years across which it was turned over
    sig_rate: float           # turnover per millennium
    # complexity metabolism (the branching side)
    senses: int
    branches: int             # descent edges between senses
    depth: int                # the deepest refinement chain
    kinds: list               # the kinds of semantic work done (refined by)
    cplx_span: int
    cplx_rate: float          # new senses per century

    @property
    def transmits(self) -> bool:
        return self.carriers > 0 and self.sig_turnover > 0.0

    @property
    def branches_out(self) -> bool:
        return self.branches > 0

    @property
    def mode(self) -> str:
        if self.transmits and self.branches_out:
            return "both"
        if self.transmits:
            return "transmitting"
        if self.branches_out:
            return "branching"
        return "dormant"

    @property
    def mode_gloss(self) -> str:
        return {
            "both": "both — it is transmitted *and* it branches in complexity",
            "transmitting": "transmitting — carried and worked across the lag, held whole (it does not branch)",
            "branching": "branching — it differentiates into finer senses (it is not carried as a field)",
            "dormant": "dormant — held at the source, neither transmitted nor branched",
        }[self.mode]

    @property
    def verdict(self) -> str:
        return f"metabolism of '{self.concept}': {self.mode_gloss}"

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.transmits:
            rows.append(
                f"  significance: {self.sig_turnover:.2f} turned over across {self.carriers} "
                f"remembering(s), {self.sig_span} year(s) — {self.sig_rate:.2f}/millennium"
            )
        else:
            rows.append("  significance: no transmission on record "
                        "(it carries no remembered weighted field to turn over)")
        if self.branches_out:
            refined = ", ".join(self.kinds) or "—"
            rows.append(
                f"  complexity: {self.senses} sense(s), {self.branches} branch(es), depth "
                f"{self.depth}, over {self.cplx_span} year(s) — {self.cplx_rate:.2f} sense(s)/century"
            )
            rows.append(f"    refined by: {refined}")
        else:
            rows.append("  complexity: held whole — no sense lattice to branch "
                        "(a breath sign holds meaning whole, it does not segment)")
        rows.append("  note: meaning as the pursuit of more understanding — transmitting (breath) and "
                    "branching\n        (pump) are its two metabolic modes. A borrowed-biology proxy; "
                    "descriptive, never a gate.")
        return "\n".join(rows)


def metabolism(concept_id: str, glossary: Glossary) -> Metabolism:
    """Read how actively a meaning metabolises: in significance, and in complexity.

    Composes the tested `mass_profile` (significance over the memory chain) and the
    concept's sense lattice (`semantics.py`) into the two metabolic rates - turnover per
    millennium (transmission) and new senses per century (branching) - plus the depth and
    kinds of refinement. The mode names which life the meaning leads: a breath sign
    transmits, a pump concept branches, the divine order does both. Descriptive.
    """
    concept = glossary.concept(concept_id)

    prof = mass_profile(concept_id, glossary)
    sigs = [s.mass * s.to_origin for s in prof.stops]
    turnover = sum(abs(sigs[i] - sigs[i - 1]) for i in range(1, len(sigs)))
    carriers = len(prof.carriers)
    first_y, last_y = prof.stops[0].year, prof.stops[-1].year
    sig_span = int(last_y - first_y) if (carriers and first_y is not None and last_y is not None) else 0
    sig_rate = (turnover / sig_span * MILLENNIUM) if sig_span > 0 else 0.0

    lattice = concept.lattice
    senses = lattice.senses
    branches = sum(len(s.descends_from) for s in senses.values())
    kinds = sorted({lattice.shift_into(sid) for sid in senses if senses[sid].descends_from})
    years = [s.year for s in senses.values()]
    cplx_span = int(max(years) - min(years)) if years else 0
    cplx_rate = ((len(senses) - 1) / cplx_span * CENTURY) if cplx_span > 0 else 0.0

    return Metabolism(
        concept=concept_id,
        carriers=carriers,
        sig_turnover=round(turnover, 4),
        sig_span=sig_span,
        sig_rate=round(sig_rate, 4),
        senses=len(senses),
        branches=branches,
        depth=_depth(lattice),
        kinds=kinds,
        cplx_span=cplx_span,
        cplx_rate=round(cplx_rate, 4),
    )


# --- the whole map: every concept's metabolism, by mode ----------------------

@dataclass
class MetabolismMap:
    """The metabolism of every concept together - the breath/pump split as modes."""

    items: list  # Metabolism, by mode then rate

    @property
    def summary(self) -> str:
        rows = ["the metabolism of meaning: "
                f"{len(self.items)} concept(s), by mode",
                f"  {'concept':<14}{'mode':<13}{'sig/millen':>11}{'senses':>8}{'branch/cent':>13}"]
        for m in self.items:
            sig = f"{m.sig_rate:.2f}" if m.transmits else "—"
            senses = str(m.senses) if m.branches_out else "—"
            cplx = f"{m.cplx_rate:.2f}" if m.branches_out else "—"
            rows.append(f"  {m.concept:<14}{m.mode:<13}{sig:>11}{senses:>8}{cplx:>13}")
        rows.append("  note: breath signs transmit (significance) but do not branch; pump concepts "
                    "branch\n        (complexity) but are not transmitted; the divine order does both — "
                    "meaning\n        pursuing more understanding, by holding it whole or by "
                    "differentiating it finer.\n        Descriptive, never a ranking of worth.")
        return "\n".join(rows)


def metabolism_map(glossary: Glossary) -> MetabolismMap:
    """Read every concept's metabolism at once, ordered by mode then rate.

    The system-level view: it shows the breath/pump threshold as two metabolic modes -
    the breath signs transmitting, the pump concepts branching, the divine order doing
    both - the framework's one thread (the pursuit of more understanding) seen from the
    top. Descriptive, never a gate.
    """
    items = [metabolism(cid, glossary) for cid in glossary.concepts]
    items.sort(key=lambda m: (
        _MODE_ORDER[m.mode],
        -(m.sig_rate if m.transmits else 0.0),
        -(m.cplx_rate if m.branches_out else 0.0),
        m.concept,
    ))
    return MetabolismMap(items=items)
