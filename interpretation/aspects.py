"""The aspects view: the spiral seen whole, every sign by its regime profile.

A **reader, not a ruler** (the `atlas`/`constellation` move): it introduces no measure and
gates nothing. It places every sign at once by its authored `{breath, pump, nerve}` profile
(`glossary.aspects`) and surfaces three things no single profile shows:

  * **the clusters** - pure breath, pure pump, and the nerve cluster that scores high on
    *all three* at once (the synthesis signature): nerve is not a fourth island but the
    regime that holds the other two;
  * **the diagonal** - the signs that light up on all three, the spiral made visible as a
    shape rather than asserted;
  * **the nerve keystone** - `constellation` run over the nerve cluster's returns: the
    value its re-coherence rests on (the nerve-regime analogue of breath's *divinity*).

Each nerve sign is coloured by its `recohere` verdict (faithful / counterfeit / mixed /
resistant) and its `scatter` - the diachronic spiral's reading carried onto the synchronic
map. A small grace note: the **ouroboros** is the one breath sign with a real nerve echo -
it *is* the cycle the whole framework turns out to be. Descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .glossary import Glossary
from .regime import BREATH, NERVE, PUMP, REGIME_ORDER, AspectProfile
from .spiral import breath_values, recohere

DIAGONAL_FLOOR = 0.40   # an aspect this high on all three reads as "lights up on all three"


@dataclass(frozen=True)
class SignAspect:
    sign: str
    profile: AspectProfile
    reading: str
    dominant: str
    on_diagonal: bool
    verdict: str | None = None    # recohere outcome, for a nerve sign with a recoherence
    scatter: float | None = None


@dataclass
class Aspects:
    signs: list[SignAspect] = field(default_factory=list)
    clusters: dict[str, list[str]] = field(default_factory=dict)
    diagonal: list[str] = field(default_factory=list)
    keystone: tuple[str, int] | None = None   # (value, reach across the nerve cluster)
    bridge: str | None = None                 # the breath sign with the strongest nerve echo

    @property
    def summary(self) -> str:
        rows = ["== the spiral seen whole: every sign by its regime profile ==",
                f"  {'sign':<13}{'breath':>7}{'pump':>6}{'nerve':>7}   reading"]
        for s in self.signs:
            colour = f"  [{s.verdict}, scatter {s.scatter:.2f}]" if s.verdict else ""
            rows.append(
                f"  {s.sign:<13}{s.profile.breath:>7.2f}{s.profile.pump:>6.2f}"
                f"{s.profile.nerve:>7.2f}   {s.reading}{colour}"
            )
        rows.append("  ---")
        rows.append(
            f"  clusters: breath {{{', '.join(self.clusters.get(BREATH, []))}}} · "
            f"pump {{{', '.join(self.clusters.get(PUMP, []))}}} · "
            f"nerve {{{', '.join(self.clusters.get(NERVE, []))}}}"
        )
        rows.append(f"  the diagonal (lights up on all three): {', '.join(self.diagonal) or '—'} "
                    "— the spiral made visible as a shape")
        if self.keystone:
            v, reach = self.keystone
            rows.append(f"  nerve keystone: {v} (reach {reach}) — the value the nerve cluster's "
                        "re-coherence rests on (the analogue of breath's divinity)")
        if self.bridge:
            rows.append(f"  the bridge: {self.bridge} — the one breath sign with a real nerve echo "
                        "(it *is* the cycle)")
        rows.append("  note: authored profiles, read together; a reader, not a ruler — composed of "
                    "tested measures, gating nothing. Descriptive, never a gate.")
        return "\n".join(rows)


def _profile(raw: dict) -> AspectProfile:
    return AspectProfile(
        breath=float(raw.get("breath", 0.0)),
        pump=float(raw.get("pump", 0.0)),
        nerve=float(raw.get("nerve", 0.0)),
    )


def aspects(glossary: Glossary) -> Aspects:
    """Place every sign by its profile; cluster, find the diagonal, the nerve keystone, the
    bridge; colour each nerve sign by its re-coherence verdict. A reader."""
    bvals = breath_values(glossary)
    signs: list[SignAspect] = []
    for sign, raw in glossary.aspects.items():
        prof = _profile(raw)
        verdict = scatter_val = None
        rec = glossary.recoherences.get(sign)
        if rec is not None:
            r = recohere(rec, bvals)
            verdict, scatter_val = r.outcome, r.scatter
        signs.append(SignAspect(
            sign=sign, profile=prof, reading=raw.get("reading", ""),
            dominant=prof.dominant(),
            on_diagonal=all(getattr(prof, r) >= DIAGONAL_FLOOR for r in REGIME_ORDER),
            verdict=verdict, scatter=scatter_val,
        ))
    # order: by dominant regime (in succession), then by nerve aspect ascending
    signs.sort(key=lambda s: (REGIME_ORDER.index(s.dominant), s.profile.nerve, s.sign))

    clusters: dict[str, list[str]] = {r: [] for r in REGIME_ORDER}
    for s in signs:
        clusters[s.dominant].append(s.sign)
    diagonal = [s.sign for s in signs if s.on_diagonal]

    # the nerve keystone: the value the nerve cluster most returns toward (constellation move)
    reach: dict[str, int] = {}
    for s in signs:
        if s.dominant != NERVE:
            continue
        rec = glossary.recoherences.get(s.sign)
        if rec is not None:
            for v in rec.returns_to:
                reach[v] = reach.get(v, 0) + 1
    keystone = max(reach.items(), key=lambda kv: (kv[1], kv[0])) if reach else None

    breath_cluster = [s for s in signs if s.dominant == BREATH]
    bridge = max(breath_cluster, key=lambda s: s.profile.nerve).sign if breath_cluster else None

    return Aspects(signs=signs, clusters=clusters, diagonal=diagonal,
                   keystone=keystone, bridge=bridge)
