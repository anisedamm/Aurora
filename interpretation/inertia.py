"""The mechanics of meaning: bit-density, inertia, and ghost-lag crystallization.

Every layer before this read meaning as a *field* (a weighted distribution of
values) or as a *lineage* (a truth carried down a chain of rememberings). This layer
asks a different question, in a borrowed vocabulary - the **physics** of that field
as it moves through time:

  * **bit-density / mass** - how much meaning a sign *holds*. A weighted field is a
    distribution, so its Shannon entropy (in bits) measures how much distinction it
    packs: a breath sign that holds *paradoxical-equilibrium*, *sovereignty*,
    *divinity* and *belonging* at once is **massive**; a pump lexeme carrying one
    shard, or the labrys read as a bare syllable (`{syllabic-sign: 1.0}`), is
    near-**massless** (entropy 0). Mass is the informational weight of the meaning.

  * **velocity / inertia / momentum** - how the meaning *moved*. Along a truth's
    `memory_chain` each hop displaces the carried field by `1 - to_prev` over its
    span of years; summed and scaled, that is the meaning's **velocity** (distance
    travelled per millennium). Mass and velocity then have two faces. **Inertia** is
    `mass / velocity`: a heavy meaning that barely moved scores high - the weight
    *resisted* the change. **Momentum** is `mass x velocity`: the quantity of meaning
    *in motion* - a heavy meaning that nonetheless travelled far scores high, much
    meaning carried a long way through history. The divine order, massive and barely
    moved, is all inertia; the ouroboros, as massive but sent on a journey (worn to
    ornament, then restored), carries the momentum.

  * **crystallization (signal / noise)** - what the **ghost lag** made of the
    outcome. Carried across the breath->pump threshold, a memory's final field splits
    against the source truth: the overlap is **signal** (the truth that crystallized),
    the remainder is **noise** (weight that drifted onto values the source never
    held). The ghost lag - the years of breath-meaning still moving under
    pump-language up to the outcome - is the distance over which that crystallization
    had to survive.

  * **the cycle of significance** - a meaning's **significance** at each remembering is
    proxied as `mass x fidelity` (the *meaning* it holds times how much of the source
    *memory* survives in it), and over time it traces a lifecycle: it can **phase in**
    (rise toward its fullest moment), reach a **peak** (the 'peak meaning period'), hold
    in a **suspended stall** (significance flat - neither rising nor falling), and **phase
    out** (decline from the peak), sometimes **recovering**. A breath truth is typically
    *born full* - its peak is the source itself, so it has no phase-in: the breath
    signature. **Dissipation** is the phase-out read *proportionally*, relative to that
    peak rather than an absolute line: a meaning at its peak has dissipated nothing, one
    fallen to half its peak has dissipated 50%, whatever the absolute level. Anchored at
    the peak, the half-life follows.

  * **the terminal state** - and so the founding image, "chosen memory is retained but
    overwritten," becomes a measurable outcome. Composing the chain with `confluence`,
    a truth either **crystallized** (its lineage held the signal), **dissipated** (it
    phased out past half its peak significance and did not recover), is **suspended** (it
    settled into a stall at a reduced level, its outcome held open), or was
    **retained-but-overwritten** -
    the *sign* still carried (chosen, kept in use) while its *content* was replaced in
    a forked lineage. The labrys is the paradigm of the last: borne still as an emblem,
    its paradoxical equilibrium overwritten by sovereign power and group identity.

Like every measure here but attestation, this composes already-tested readings
(`weighting`, `memory`) and introduces a borrowed-physics *proxy*, never an oracle:
entropy is a proxy for "how much meaning," resonance-distance a proxy for "how far it
moved." Descriptive, never a gate. Pure standard library.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .glossary import Glossary
from .memory import CONVERGENCE_THRESHOLD, confluence, memory_chain
from .regime import BREATH
from .weighting import WeightedField

# Years per millennium - velocity and dissipation are reported per-millennium, the
# natural scale of a breath->pump transmission (these spans run to thousands of years).
MILLENNIUM = 1000

# A memory that ends below this *fraction of its own peak* significance - phased out past
# half of its fullest moment, and not recovered - is read as dissipated. A proportional
# line relative to the meaning's peak, not an absolute signal cutoff.
DISSIPATED_FRACTION = 0.5

# A step whose significance changes by less than this fraction of the peak is a **stall** -
# the meaning suspended, neither phasing in nor out. The flat band of the cycle.
STALL_BAND = 0.05


# --- bit-density: how much meaning a field holds -----------------------------

@dataclass(frozen=True)
class Density:
    """The informational weight of a weighted field: its bits of held meaning."""

    bits: float                 # Shannon entropy of the normalised field, in bits
    held: int                   # how many values carry weight (the breadth)
    dominant: list              # the heaviest values, normalised (for display)

    @property
    def gloss(self) -> str:
        if self.held == 0:
            return "massless: no weighted field to weigh"
        if self.held == 1:
            return "massless: one value carries all the weight (a single lexeme - entropy 0)"
        if self.bits >= 1.5:
            return "massive: meaning held whole across many values at once"
        return "light: meaning concentrated in few values (segmented)"


def bit_density(field_weights) -> Density:
    """The Shannon entropy (bits) of a weighted field - its informational mass.

    A field is a distribution over conceptual values; its entropy measures how much
    distinction it packs. One value carrying all the weight is entropy 0 (massless); a
    field spread in proportion across many values is high-entropy (massive). This is
    "informational bit density" made computable - a proxy for how much meaning a sign
    holds, never a claim about its worth. Descriptive.
    """
    norm = WeightedField(dict(field_weights)).normalized()
    ps = [p for p in norm.values() if p > 0]
    bits = -sum(p * math.log2(p) for p in ps)
    dominant = sorted(norm.items(), key=lambda kv: (-kv[1], kv[0]))
    return Density(bits=round(bits, 4), held=len(ps), dominant=dominant)


# --- the mechanics of a truth as it travels its memory chain -----------------

@dataclass
class Mechanics:
    """The physics of one truth across the ghost lag: mass, motion, and outcome."""

    concept: str
    origin_year: int | None
    threshold: int | None
    ghost_lag: int                 # years of breath-meaning carried under pump-language
    mass: float                    # bits of the retained source truth
    carriers: int                  # rememberings on the chain
    span_years: int                # origin -> last carrier
    velocity: float                # field-distance travelled per millennium
    inertia: float | None          # mass / velocity - resistance to drift (None if it never moved)
    momentum: float | None         # mass x velocity - the quantity of meaning in motion
    signal: float                  # the truth that crystallized (final to-origin)
    peak_significance: float       # the fullest significance (mass x fidelity) the memory reached
    peak_year: int | None          # when that peak fell - the 'peak meaning period'
    peak_at_origin: bool           # was the source itself its fullest moment? (born full)
    phase_in: float                # proportional rise from the start up to the peak, in [0, 1]
    stall_span: int                # the longest suspended (flat) span, in years
    dissipation: float             # proportional phase-out from peak at the end, in [0, 1]
    deepest_dissipation: float     # the deepest phase-out reached (before any recovery), in [0, 1]
    half_life: int | None          # years to lose half the peak significance (None: held)
    cycle: str                     # the lifecycle phrase: phase in -> peak -> stall -> phase out
    direction: str                 # evolved / reverted / recovered / held
    state: str                     # crystallized / retained-overwritten / dissipated / suspended / held-no-return
    overwritten: tuple | None = field(default=None)  # (lineage id, its to-origin) when forked

    @property
    def noise(self) -> float:
        """The weight that dissipated into noise - drift onto non-source values."""
        return round(max(0.0, 1.0 - self.signal), 4)

    @property
    def crystallization(self) -> int:
        """The signal share of the outcome, as a percentage."""
        return int(round(self.signal * 100))

    @property
    def state_gloss(self) -> str:
        return {
            "crystallized": "the truth crystallized as signal - carried whole across the lag",
            "retained-overwritten": "chosen memory retained but overwritten - the sign kept, its content replaced",
            "dissipated": "phased out past half its peak significance - the memory faded, not kept",
            "suspended": "suspended in a stall - significance settled at a reduced level, its outcome held open",
            "held-no-return": "held at the source - no return path recorded to measure",
            "no-field": "no weighted field to weigh - a pump concept segments meaning into senses, not a field",
        }[self.state]

    @property
    def lag_phrase(self) -> str:
        """How far the breath-meaning travelled under pump-language to the outcome."""
        if self.carriers == 0:
            return "no return path recorded"
        if self.ghost_lag == 0:
            return "at the threshold itself (the crossing)"
        return f"across {self.ghost_lag} year(s) of ghost lag"

    @property
    def verdict(self) -> str:
        if self.state == "no-field":
            return f"MECHANICS of '{self.concept}': no weighted field to weigh  ->  {self.state_gloss}"
        head = f"MECHANICS of '{self.concept}': mass {self.mass:.2f} bits"
        if self.carriers == 0:
            return f"{head}  ->  {self.state_gloss}"
        inert = "—" if self.inertia is None else f"{self.inertia:.1f}"
        if self.state == "retained-overwritten" and self.overwritten is not None:
            return (f"{head}, inertia {inert}; signal {self.signal:.2f} kept on one lineage but "
                    f"{self.overwritten[1]:.2f} on another {self.lag_phrase}  ->  {self.state_gloss}")
        if self.state == "dissipated":
            return (f"{head}, inertia {inert}; phased out {self.dissipation:.0%} from its peak "
                    f"{self.lag_phrase}  ->  {self.state_gloss}")
        if self.state == "suspended":
            return (f"{head}, inertia {inert}; suspended at {self.dissipation:.0%} off its peak "
                    f"{self.lag_phrase}  ->  {self.state_gloss}")
        return (f"{head}, inertia {inert}, crystallization {self.crystallization}% signal "
                f"{self.lag_phrase}  ->  {self.state_gloss}")

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.state == "no-field":
            rows.append("  (the mechanics layer weighs breath-era weighted fields; this concept "
                        "holds a sense-history, not a field)")
            rows.append("  note: a borrowed-physics proxy over the tested chain - entropy for mass, "
                        "resonance-distance for motion. Descriptive, never a gate.")
            return "\n".join(rows)
        rows.append(f"  density (mass): {self.mass:.2f} bits of meaning held by the source truth")
        if self.carriers == 0:
            rows.append("  motion: no rememberings on record - the truth was not carried forward to measure")
        else:
            inert = "—" if self.inertia is None else f"{self.inertia:.1f}"
            mom = "—" if self.momentum is None else f"{self.momentum:.2f}"
            rows.append(
                f"  motion: {self.carriers} remembering(s) over {self.span_years} year(s); "
                f"velocity {self.velocity:.3f}/millennium"
            )
            rows.append(
                f"  forces: momentum {mom} (meaning carried in motion) vs "
                f"inertia {inert} (mass resisting the drift)"
            )
            rows.append(
                f"  crystallization: signal {self.signal:.2f} / noise {self.noise:.2f} "
                f"{self.lag_phrase}"
            )
            peak_loc = "at the source" if self.peak_at_origin else f"at {self.peak_year}"
            deepest = (f"; deepest {self.deepest_dissipation:.0%} before recovering"
                       if self.deepest_dissipation > self.dissipation + 0.01 else "")
            hl = "" if self.half_life is None else f"; half-life ~{self.half_life} year(s)"
            rows.append(
                f"  dissipation: phased out {self.dissipation:.0%} from its peak significance "
                f"({self.peak_significance:.2f} {peak_loc}){deepest}{hl}"
            )
            rows.append(f"  cycle: {self.cycle}")
            rows.append(f"  direction: the meaning {self.direction} through time")
            if self.overwritten is not None:
                lid, to_origin = self.overwritten
                rows.append(f"  overwritten: the sign is retained, but lineage '{lid}' overwrote its "
                            f"content (to-origin {to_origin:.2f})")
        rows.append("  note: a borrowed-physics proxy over the tested chain - entropy for mass, "
                    "resonance-distance for motion. Descriptive, never a gate.")
        return "\n".join(rows)


def _velocity(links) -> tuple[float, int]:
    """Total field-distance per millennium along the chain, and its span in years.

    Each hop displaces the carried field by `1 - to_prev`; summed over the carriers and
    divided by the years from origin to the last carrier, scaled per-millennium. Returns
    (0.0, 0) when there is nothing (or no time) to move across.
    """
    carriers = [ln for ln in links if not ln.is_origin]
    if not carriers:
        return 0.0, 0
    origin_year = next((ln.year for ln in links if ln.is_origin), None)
    last_year = carriers[-1].year
    if origin_year is None or last_year is None:
        return 0.0, 0
    span = last_year - origin_year
    path = sum((1.0 - ln.to_prev) for ln in carriers if ln.to_prev is not None)
    if span <= 0:
        return 0.0, int(span)
    return path / span * MILLENNIUM, int(span)


@dataclass
class _PhaseOut:
    """Significance over time, read as the full cycle: phase in, stall, phase out."""

    peak: float                # the fullest significance reached (mass x fidelity)
    peak_year: int | None
    peak_at_origin: bool
    phase_in: float            # proportional rise from the start to the peak, in [0, 1]
    stall_span: int            # the longest suspended (flat) span, in years
    terminal_stall: bool       # did the memory end on a stall (a flat final step)?
    final_dissipation: float   # 1 - final/peak, clamped to [0, 1]
    deepest_dissipation: float # 1 - lowest carrier significance / peak
    half_life: int | None      # years to halve the peak significance, at the post-peak rate
    cycle: str                 # the lifecycle phrase


def _cycle_phrase(sig, peak_val: float, peak_at_origin: bool, phase_in: float,
                  stall_span: int) -> str:
    """Name the lifecycle a meaning's significance traced, in time order.

    Each step is a rise (phase in / recovery), a fall (phase out), or a stall (suspended);
    consecutive like steps are merged, and a rise after a fall reads as a recovery. A
    born-full truth (peak at the source) is prefixed as such - it never phased in.
    """
    if len(sig) < 2 or peak_val <= 0:
        return "held at the source"
    steps = []
    for i in range(1, len(sig)):
        d = (sig[i][2] - sig[i - 1][2]) / peak_val
        steps.append("stall" if abs(d) < STALL_BAND else ("rise" if d > 0 else "fall"))
    merged: list[str] = []
    for s in steps:
        if not merged or merged[-1] != s:
            merged.append(s)
    tokens: list[str] = []
    seen_fall = False
    rise_used = False
    for s in merged:
        if s == "rise":
            tokens.append("recovered" if seen_fall else f"phased in {phase_in:.0%}")
            rise_used = True
        elif s == "fall":
            tokens.append("faded")
            seen_fall = True
        else:
            tokens.append(f"stalled {stall_span} yr" if stall_span else "stalled")
    if peak_at_origin:
        tokens = ["born full"] + tokens
    return " → ".join(tokens) if tokens else "held"


def _phase_out(concept, chain, glossary: Glossary) -> _PhaseOut | None:
    """Track significance (`mass x fidelity`) down the chain across its whole cycle.

    Significance at a remembering is the informational mass it holds times how much of the
    source truth survives in it - the *meaning* weighted by the *memory*. The peak is the
    fullest such moment (the 'peak meaning period'); the memory may **phase in** up to it,
    **stall** (hold flat), and **phase out** from it - dissipation read proportionally,
    relative to the meaning's own height rather than an absolute line. Returns None when
    there is no remembering to trace.
    """
    sig: list[tuple[int | None, bool, float]] = []
    for ln in chain.links:
        if ln.is_origin:
            field_weights = concept.retained_field()
        else:
            try:
                field_weights = glossary.usage(ln.by_id).field
            except KeyError:
                field_weights = {}
        sig.append((ln.year, ln.is_origin, bit_density(field_weights).bits * max(0.0, ln.to_origin)))

    carriers = [t for t in sig if not t[1]]
    if not carriers:
        return None

    peak = sig[0]
    for t in sig[1:]:
        if t[2] > peak[2]:        # strictly greater keeps the earliest peak on ties
            peak = t
    peak_year, peak_at_origin, peak_val = peak[0], peak[1], peak[2]
    if peak_val <= 0:
        return _PhaseOut(0.0, peak_year, peak_at_origin, 0.0, 0, False, 0.0, 0.0, None,
                         "held at the source")

    phase_in = min(1.0, max(0.0, (peak_val - sig[0][2]) / peak_val))

    stall_span = 0
    terminal_stall = False
    for i in range(1, len(sig)):
        y0, y1 = sig[i - 1][0], sig[i][0]
        if y0 is None or y1 is None or y1 <= y0:
            continue
        if abs(sig[i][2] - sig[i - 1][2]) < STALL_BAND * peak_val:
            stall_span = max(stall_span, int(y1 - y0))
            if i == len(sig) - 1:
                terminal_stall = True

    final_val = carriers[-1][2]
    deepest_val = min(t[2] for t in carriers)
    final_diss = min(1.0, max(0.0, 1.0 - final_val / peak_val))
    deepest_diss = min(1.0, max(0.0, 1.0 - deepest_val / peak_val))

    half_life = None
    final_year = carriers[-1][0]
    if final_val < peak_val and peak_year is not None and final_year is not None and final_year > peak_year:
        lam = -math.log(max(final_val / peak_val, 1e-6)) / (final_year - peak_year)
        if lam > 0:
            half_life = int(round(math.log(2) / lam))

    return _PhaseOut(
        peak=round(peak_val, 4), peak_year=peak_year, peak_at_origin=peak_at_origin,
        phase_in=round(phase_in, 4), stall_span=stall_span, terminal_stall=terminal_stall,
        final_dissipation=round(final_diss, 4), deepest_dissipation=round(deepest_diss, 4),
        half_life=half_life,
        cycle=_cycle_phrase(sig, peak_val, peak_at_origin, phase_in, stall_span),
    )


def mechanics(concept_id: str, glossary: Glossary) -> Mechanics:
    """Read the physics of a truth across the ghost lag: mass, motion, and outcome.

    Composes the tested `memory_chain` (the lineage and its resonances over time) and
    `confluence` (whether the lineages converged or forked) with one new, borrowed
    measure - bit-density as informational mass. The mass is the entropy of the source
    truth; the velocity and inertia come from the chain's displacements; the
    signal/noise split is the final to-origin against the ghost lag; dissipation is the
    proportional phase-out of significance from its peak; and the terminal state
    distinguishes a truth that **crystallized** from one that **dissipated** (phased out
    past half its peak and did not recover) and from a sign **retained but overwritten** (a
    fork that kept the sign and replaced its content). Descriptive, never a gate.
    """
    concept = glossary.concept(concept_id)
    chain = memory_chain(concept_id, glossary)
    conf = confluence(concept_id, glossary)

    density = bit_density(concept.retained_field())
    mass = density.bits
    velocity, span = _velocity(chain.links)
    inertia = round(mass / velocity, 4) if velocity > 0 else None
    momentum = round(mass * velocity, 4) if velocity > 0 else None

    signal = round(chain.survival, 4)
    po = _phase_out(concept, chain, glossary)

    threshold = concept.threshold
    last_year = chain.carriers[-1].year if chain.carriers else None
    ghost_lag = (
        int(last_year - threshold)
        if (threshold is not None and last_year is not None and last_year > threshold)
        else 0
    )

    # Direction along the chain's net path through time. With a single carrier there is no
    # carrier-to-carrier trend, so it is read against the source (1.0) instead.
    if not chain.carriers:
        direction = "held"
    elif chain.restored:
        direction = "reverted, then recovered"
    else:
        net = (chain.carriers[-1].to_origin - chain.carriers[0].to_origin
               if len(chain.carriers) > 1 else chain.carriers[-1].to_origin - 1.0)
        direction = "reverted" if net < -0.001 else "progressed" if net > 0.001 else "held"

    # Terminal state: the fork (retained-but-overwritten) is read before dissipation, so a
    # sign whose latest lineage re-crystallized it still surfaces the branch that overwrote it.
    forked = len(conf.lineages) >= 2 and not conf.independently_corroborated
    diverged = [ln for ln in conf.lineages if ln.witness_to_origin < CONVERGENCE_THRESHOLD]
    overwritten = None
    if density.held == 0:
        state = "no-field"          # a pump concept holds senses, not a weighted field
    elif not chain.carriers:
        state = "held-no-return"
    elif forked and diverged:
        state = "retained-overwritten"
        worst = min(diverged, key=lambda ln: ln.witness_to_origin)
        overwritten = (worst.witness, round(worst.witness_to_origin, 4))
    elif po is not None and po.final_dissipation >= DISSIPATED_FRACTION:
        state = "dissipated"        # phased out past half its own peak, not recovered
    elif po is not None and po.terminal_stall and 0.15 <= po.final_dissipation < DISSIPATED_FRACTION:
        state = "suspended"         # settled into a stall at a reduced level - outcome held open
    else:
        state = "crystallized"

    return Mechanics(
        concept=concept_id,
        origin_year=chain.origin_year,
        threshold=threshold,
        ghost_lag=ghost_lag,
        mass=round(mass, 4),
        carriers=len(chain.carriers),
        span_years=span,
        velocity=round(velocity, 4),
        inertia=inertia,
        momentum=momentum,
        signal=signal,
        peak_significance=po.peak if po else round(mass, 4),
        peak_year=po.peak_year if po else chain.origin_year,
        peak_at_origin=po.peak_at_origin if po else True,
        phase_in=po.phase_in if po else 0.0,
        stall_span=po.stall_span if po else 0,
        dissipation=po.final_dissipation if po else 0.0,
        deepest_dissipation=po.deepest_dissipation if po else 0.0,
        half_life=po.half_life if po else None,
        cycle=po.cycle if po else "held at the source",
        direction=direction,
        state=state,
        overwritten=overwritten,
    )


# --- the whole web: the mechanics of every breath truth at once --------------

@dataclass
class MechanicsWeb:
    """The mechanics of a regime's truths together - mass against outcome."""

    regime: str
    items: list  # Mechanics, by mass descending

    @property
    def summary(self) -> str:
        head = (f"the mechanics of the {self.regime} web: {len(self.items)} truth(s), "
                "by informational mass")
        if not self.items:
            return (f"{head}\n  the {self.regime} regime holds no weighted-field web to weigh — "
                    "it segments meaning into senses, not fields (see `proliferation`).")
        rows = [head, f"  {'concept':<14}{'mass':>5}  {'momentum':>8}  {'inertia':>7}  {'signal':>6}  state"]
        for m in self.items:
            mom = f"{m.momentum:.2f}" if m.momentum is not None else "—"
            inert = f"{m.inertia:.1f}" if m.inertia is not None else "—"
            signal = f"{m.signal:.2f}" if m.carriers > 0 else "—"
            rows.append(f"  {m.concept:<14}{m.mass:>5.2f}  {mom:>8}  {inert:>7}  {signal:>6}  {m.state}")
        rows.append("  note: the breath truths are uniformly massive (meaning held whole); what "
                    "differs is how far\n        each moved (momentum) and the outcome the ghost lag "
                    "crystallized, not the mass.\n        Descriptive, never a ranking of worth.")
        return "\n".join(rows)


def mechanics_web(glossary: Glossary, *, regime: str = BREATH) -> MechanicsWeb:
    """The mechanics of every sign of a regime that holds a weighted field, by mass.

    Lifts `mechanics` from one truth to the whole web - the system-level companion to
    `constellation`, read through the borrowed physics. It shows that the breath web's
    truths are uniformly *massive* (they held meaning whole) and that what separates them
    is the **outcome** the ghost lag made of each: crystallized, retained-but-overwritten,
    or held with no return path. Descriptive, never a gate.
    """
    signs = sorted(
        (c for c in glossary.concepts.values() if c.regime == regime and c.retained_field()),
        key=lambda c: c.id,
    )
    items = [mechanics(c.id, glossary) for c in signs]
    items.sort(key=lambda m: (-m.mass, m.concept))
    return MechanicsWeb(regime=regime, items=items)


# --- the mass profile: informational weight, hop by hop down the chain --------

@dataclass
class MassStop:
    """The informational weight a single remembering held, beside its fidelity."""

    by_id: str
    year: int | None
    mass: float           # bits of meaning this hop holds (entropy of its carried field)
    to_origin: float      # how much of the *source* truth it still holds (from the chain)
    is_origin: bool
    movement: str         # origin / held / decayed / restored (from the chain link)


@dataclass
class MassProfile:
    """How a truth's informational mass moved, hop by hop, beside its signal.

    Mass (how much a hop holds) and to-origin (how much of the *source* it holds) move
    **independently** - which is the point. A hop can stay massive while its signal
    falls: the sign kept saying a great deal, but no longer about the source truth - it
    was **overwritten**, not thinned. Or both can fall together: the meaning **thinned**,
    worn down toward ornament. The profile makes the two cases visibly different.
    """

    concept: str
    stops: list[MassStop] = field(default_factory=list)

    @property
    def carriers(self) -> list[MassStop]:
        return [s for s in self.stops if not s.is_origin]

    @property
    def origin_mass(self) -> float:
        return self.stops[0].mass if self.stops else 0.0

    @property
    def final_mass(self) -> float:
        return self.stops[-1].mass if self.stops else 0.0

    @property
    def low_mass(self) -> float:
        return min((s.mass for s in self.stops), default=0.0)

    @property
    def final_signal(self) -> float:
        return self.carriers[-1].to_origin if self.carriers else 1.0

    @property
    def low_water(self) -> float:
        return min((s.to_origin for s in self.carriers), default=1.0)

    @property
    def summary(self) -> str:
        head = f"mass profile of '{self.concept}' (informational weight, hop by hop):"
        if not self.carriers:
            return head + "\n  no rememberings on record to profile the mass across."
        rows = [head, f"  {'year':>7}  {'id':<22}  {'mass':>5}  {'to-origin':>9}  movement"]
        for s in self.stops:
            year = "origin" if s.is_origin else str(s.year)
            move = "" if s.is_origin else s.movement
            rows.append(f"  {year:>7}  {s.by_id:<22}  {s.mass:>5.2f}  {s.to_origin:>9.2f}  {move}")
        rows.append(
            f"  mass {self.origin_mass:.2f} -> {self.final_mass:.2f} (low {self.low_mass:.2f}); "
            f"to-origin 1.00 -> {self.final_signal:.2f} (low {self.low_water:.2f})"
        )
        rows.append("  note: mass is how much a hop holds; to-origin is how much of the source it "
                    "still holds.\n        They move independently — a hop can stay massive while its "
                    "signal falls (overwritten),\n        or thin out while staying on-truth. "
                    "Descriptive, never a gate.")
        return "\n".join(rows)


def mass_profile(concept_id: str, glossary: Glossary) -> MassProfile:
    """Trace a truth's informational mass down its memory chain, beside its signal.

    Composes the tested `memory_chain` (for each hop's year, to-origin and movement) with
    `bit_density` (for the mass of the field that hop actually carried). Reading the two
    columns together separates a memory that was **overwritten** (mass held, signal fell)
    from one that **thinned** (both fell) - a distinction the resonance alone could not
    draw. Descriptive, never a gate.
    """
    concept = glossary.concept(concept_id)
    chain = memory_chain(concept_id, glossary)
    stops: list[MassStop] = []
    for ln in chain.links:
        if ln.is_origin:
            field_weights = concept.retained_field()
        else:
            try:
                field_weights = glossary.usage(ln.by_id).field
            except KeyError:
                field_weights = {}
        stops.append(MassStop(
            by_id=ln.by_id, year=ln.year, mass=bit_density(field_weights).bits,
            to_origin=ln.to_origin, is_origin=ln.is_origin, movement=ln.movement,
        ))
    return MassProfile(concept=concept_id, stops=stops)
