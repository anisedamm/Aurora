"""The atlas: the whole history of meaning this record assembles, on one screen.

Every other module reads one thing - a sign, a reading, a value, a lineage, a layer. The
atlas reads them *together*, composing the already-tested measures into a single narrative
of the arc the framework has traced: the backing's signal, the breath web's load-bearing
values, the threshold where they dispersed, the pump explosion that followed, the unbroken
thread that runs from one to the other - and then the meaning tree the later layers built:
how the bit holds or excludes its opposite, the tree's base and edge, the web it earns by
folding to truth, the dimensions it spans, and the dimensionless it can only point at.

It is the sibling system's `status` move - a reader, not a ruler. It introduces no new
measure and gates nothing; it only gathers what the tested functions already say, so a
person can see the whole at once. Read-only, descriptive. Pure standard library.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .arc import Arc, arc
from .condensation import Relations
from .constellation import Constellation, constellation
from .cornerstone import Cornerstones, cornerstones
from .dimension import MeaningSpace, meaning_space
from .dimensionless import Dimensionlessness, Invariant, dimensionless
from .fold import Folding, folding
from .frontier import Frontier, frontier
from .glossary import Glossary
from .ledger import Ledger
from .lexicon import Lexicon, Proliferation, proliferation
from .migration import Migration, migrate
from .signal import Signal, compute_signal
from .tension import Tensions, tensions
from .weave import Weave, weave


@dataclass
class Atlas:
    signal: Signal
    breath: Constellation
    explosion: Proliferation
    migrations: list[Migration] = field(default_factory=list)
    arcs: list[Arc] = field(default_factory=list)
    # the meaning tree (the later layers) - present when their inputs are supplied
    tension: Tensions | None = None
    space: MeaningSpace | None = None
    web: Weave | None = None
    frontier: Frontier | None = None
    base: Cornerstones | None = None
    truth: Folding | None = None
    beyond: Dimensionlessness | None = None

    @property
    def hub(self) -> str:
        deg: Counter[str] = Counter()
        for e in self.breath.affinities:
            deg[e.a] += 1
            deg[e.b] += 1
        return deg.most_common(1)[0][0] if deg else "—"

    @property
    def summary(self) -> str:
        rows = ["== atlas: the history of meaning this record assembles =="]

        rows.append(f"  signal:    {self.signal.value}  "
                    f"({'trustworthy backing' if self.signal.value else 'not yet trustworthy'})")

        k = self.breath.keystone
        keystone = f"{k.value} (reach {k.reach})" if k else "—"
        rows.append(f"  breath web — keystone value: {keystone}; hub sign: {self.hub}"
                    + (f"; islands {self.breath.islands}" if self.breath.islands else ""))

        if self.migrations:
            rows.append("  the threshold — values held whole, then dispersed:")
            for m in self.migrations:
                rows.append(f"    {m.value:<12} held {m.breath_weight:.2f} across "
                            f"{m.concentration} sign(s) -> {m.dispersion} lexeme(s)")

        pts = self.explosion.points
        if pts:
            a, z = pts[0], pts[-1]
            rows.append(
                f"  the pump explosion — lexicon {a.cumulative}->{z.cumulative} over "
                f"{len(pts)} eras; sieve->success {a.mean_alignment:.2f}->{z.mean_alignment:.2f}; "
                f"experiential {a.experiential_share:.2f}->{z.experiential_share:.2f}; "
                f"coherence {a.coherence:.2f}->{z.coherence:.2f}"
            )

        for a in self.arcs:
            first, last = a.thread[0], a.thread[-1]
            rows.append(
                f"  the unbroken arc — {a.value}: "
                f"{first.word}({first.alignment:.2f}) -> ... -> {last.word}({last.alignment:.2f}), "
                f"reaching {a.reaches:.2f} over ~{a.span_years} year(s)"
            )

        # -- the meaning tree (the later layers) --
        tree = self._tree_rows()
        if tree:
            rows.append("  -- the meaning tree --")
            rows.extend(tree)

        rows.append("  note: composed from already-tested measures - a reader, not a ruler; "
                    "read-only, gates nothing.")
        return "\n".join(rows)

    def _tree_rows(self) -> list[str]:
        rows: list[str] = []
        if self.tension is not None:
            k = self.tension.keystone
            held = f"most held: {k.value} ({k.held_tension:.2f})" if k else "—"
            rows.append(f"  tension — the bit excludes its opposite, the breath holds it "
                        f"({held}), the pump segments it away")
        if self.base is not None and self.base.base and self.frontier is not None and self.frontier.leading:
            b, fr = self.base.base, self.frontier.leading
            rows.append(f"  base & edge — cornerstone: {b.word} ({b.support} rest on it); "
                        f"frontier: {fr.word} (furthest out)")
        if self.web is not None and self.web.keystone:
            ks = self.web.keystone
            rows.append(f"  the web — keystone: {ks.term} ({ks.defining_reach} defined on it); "
                        f"{len(self.web.roots)} root antonym couple(s)")
        if self.truth is not None:
            legit = ("the weave rests on earned depth" if not self.truth.provisional
                     else f"{len(self.truth.provisional)} woven before folded to truth")
            rows.append(f"  folding to truth — threshold {self.truth.threshold}: {legit}")
        if self.space is not None:
            rows.append(f"  the meaning space — {self.space.conveyance.size} conveyance × "
                        f"{self.space.culture.size} culture × {self.space.time.size} era = "
                        f"{self.space.volume} cells, depth {self.space.depth_min}-{self.space.depth_max}")
        if self.beyond is not None and self.beyond.nearest:
            n = self.beyond.nearest
            rows.append(f"  the dimensionless — nearest: {n.invariant.name}; "
                        "the gap to 'outlasts time' is unattestable")
        return rows


def atlas(
    ledger: Ledger,
    glossary: Glossary,
    lexicon: Lexicon,
    *,
    relations: Relations | None = None,
    invariants: list[Invariant] | None = None,
    manifest_path="MANIFEST.md",
) -> Atlas:
    """Compose the whole reading: signal, the breath web, the threshold, the explosion,
    the unbroken arcs - and, when their maps are supplied, the meaning tree the later
    layers built (tension, the base and edge, the web, folding to truth, the dimensions,
    the dimensionless). One screen for the history of meaning the record holds."""
    sig = compute_signal(ledger, glossary, manifest_path=manifest_path)
    breath = constellation(glossary)
    explosion = proliferation(lexicon)

    values = [v for v in glossary.migrations if not v.startswith("_")]
    migrations = [migrate(v, glossary) for v in sorted(values)]
    arcs = [a for a in (arc(v, glossary, lexicon) for v in sorted(values)) if a.thread]

    # The meaning tree: tension and the dimensions need only glossary/lexicon; the web,
    # edges and folding need the relations map; the dimensionless needs the invariants.
    tension_ = tensions(glossary, relations)
    space = meaning_space(glossary, lexicon)
    web = frontier_ = base = truth = beyond = None
    if relations is not None:
        web = weave(relations, lexicon)
        frontier_ = frontier(lexicon, relations)
        base = cornerstones(lexicon, relations)
        truth = folding(lexicon, relations)
    if invariants is not None:
        beyond = dimensionless(invariants, glossary, lexicon)

    return Atlas(
        signal=sig, breath=breath, explosion=explosion,
        migrations=migrations, arcs=arcs,
        tension=tension_, space=space, web=web, frontier=frontier_,
        base=base, truth=truth, beyond=beyond,
    )
