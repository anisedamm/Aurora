"""The atlas: the whole history of meaning this record assembles, on one screen.

Every other module reads one thing - a sign, a reading, a value, a lineage. The atlas
reads them *together*, composing the already-tested measures into a single narrative of
the arc the framework has traced: the backing's signal, the breath web's load-bearing
values, the threshold where they dispersed, the pump explosion that followed, and the
unbroken thread that runs from one to the other.

It is the sibling system's `status` move - a reader, not a ruler. It introduces no new
measure and gates nothing; it only gathers what the tested functions already say, so a
person can see the whole at once. Read-only, descriptive. Pure standard library.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .arc import Arc, arc
from .aspects import Aspects, aspects as aspects_view
from .constellation import Constellation, constellation
from .glossary import Glossary
from .ledger import Ledger
from .lexicon import Lexicon, Proliferation, proliferation
from .migration import Migration, migrate
from .regime import NERVE
from .signal import Signal, compute_signal


@dataclass
class Atlas:
    signal: Signal
    breath: Constellation
    explosion: Proliferation
    migrations: list[Migration] = field(default_factory=list)
    arcs: list[Arc] = field(default_factory=list)
    aspects: Aspects | None = None

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

        if self.aspects and self.aspects.keystone:
            v, reach = self.aspects.keystone
            verdicts = Counter(s.verdict for s in self.aspects.signs if s.verdict)
            spread = ", ".join(f"{n}x {o}" for o, n in
                               sorted(verdicts.items(), key=lambda kv: (-kv[1], kv[0])))
            n_nerve = len(self.aspects.clusters.get(NERVE, []))
            rows.append(
                f"  the nerve return — keystone {v} (reach {reach}); {n_nerve} sign(s) "
                f"span {spread or '—'}; bridge {self.aspects.bridge} (it is the cycle)"
            )

        rows.append("  note: composed from already-tested measures - a reader, not a ruler; "
                    "read-only, gates nothing.")
        return "\n".join(rows)


def atlas(
    ledger: Ledger,
    glossary: Glossary,
    lexicon: Lexicon,
    *,
    manifest_path="MANIFEST.md",
) -> Atlas:
    """Compose the whole reading: signal, the breath web, the threshold, the explosion,
    and any unbroken arcs - one screen for the history of meaning the record holds."""
    sig = compute_signal(ledger, glossary, manifest_path=manifest_path)
    breath = constellation(glossary)
    explosion = proliferation(lexicon)

    values = [v for v in glossary.migrations if not v.startswith("_")]
    migrations = [migrate(v, glossary) for v in sorted(values)]
    arcs = [a for a in (arc(v, glossary, lexicon) for v in sorted(values)) if a.thread]
    asp = aspects_view(glossary) if glossary.aspects else None

    return Atlas(
        signal=sig, breath=breath, explosion=explosion,
        migrations=migrations, arcs=arcs, aspects=asp,
    )
