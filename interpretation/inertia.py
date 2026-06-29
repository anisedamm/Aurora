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

  * **velocity / inertia** - how fast the meaning *moved*. Along a truth's
    `memory_chain` each hop displaces the carried field by `1 - to_prev` over its
    span of years; summed and scaled, that is the meaning's **velocity** (distance
    travelled per millennium). **Inertia** is `mass / velocity`: a heavy meaning that
    nonetheless barely moved scores high - the weight resisted the change, exactly as
    the founding intuition held ("the weight of conceptual meaning held determines its
    dissipation rate as memory").

  * **crystallization (signal / noise)** - what the **ghost lag** made of the
    outcome. Carried across the breath->pump threshold, a memory's final field splits
    against the source truth: the overlap is **signal** (the truth that crystallized),
    the remainder is **noise** (weight that drifted onto values the source never
    held). The ghost lag - the years of breath-meaning still moving under
    pump-language up to the outcome - is the distance over which that crystallization
    had to survive.

  * **dissipation as memory** - read off the chain as a half-life: at the net rate the
    signal eroded, how many years to lose half of what remains. A massive, inertial
    truth shows a long half-life (or none - it held); a light one dissipates fast.

  * **the terminal state** - and so the founding image, "chosen memory is retained but
    overwritten," becomes a measurable outcome. Composing the chain with `confluence`,
    a truth either **crystallized** (its lineage held the signal), **dissipated** (the
    signal fell to noise and no record kept it), or was **retained-but-overwritten** -
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

# A final signal at or above this is read as having crystallized; below it, as having
# dissipated into noise (mirrors memory.CONVERGENCE_THRESHOLD's role on the chain).
CRYSTALLIZED = 0.6


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
    inertia: float | None          # mass / velocity (None if it never moved)
    signal: float                  # the truth that crystallized (final to-origin)
    half_life: int | None          # years to lose half the remaining signal (None: held)
    direction: str                 # evolved / reverted / recovered / held
    state: str                     # crystallized / retained-overwritten / dissipated / held-no-return
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
            "dissipated": "the signal fell to noise - the memory dissipated, not kept",
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
            rows.append(
                f"  motion: {self.carriers} remembering(s) over {self.span_years} year(s); "
                f"velocity {self.velocity:.3f}/millennium, inertia {inert} (mass resisting the drift)"
            )
            rows.append(
                f"  crystallization: signal {self.signal:.2f} / noise {self.noise:.2f} "
                f"{self.lag_phrase}"
            )
            hl = "none — the meaning held against the lag" if self.half_life is None else f"~{self.half_life} year(s)"
            rows.append(f"  dissipation: half-life {hl} (the weight is the inertia against it)")
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


def _half_life(signal: float, span: int, decayed: bool) -> int | None:
    """Years to lose half the remaining signal, at the chain's net erosion rate.

    Only defined when the memory net-decayed (`signal < 1` with a decaying hop): then
    the signal is modelled as `exp(-lambda*t)` through the endpoint and the half-life is
    `ln2 / lambda`. A memory that held or fully recovered has no net dissipation to fit,
    so this is None - reported honestly as "the meaning held against the lag".
    """
    if not decayed or span <= 0 or signal >= 0.999:
        return None
    s = max(signal, 1e-6)
    lam = -math.log(s) / span
    if lam <= 0:
        return None
    return int(round(math.log(2) / lam))


def mechanics(concept_id: str, glossary: Glossary) -> Mechanics:
    """Read the physics of a truth across the ghost lag: mass, motion, and outcome.

    Composes the tested `memory_chain` (the lineage and its resonances over time) and
    `confluence` (whether the lineages converged or forked) with one new, borrowed
    measure - bit-density as informational mass. The mass is the entropy of the source
    truth; the velocity and inertia come from the chain's displacements; the
    signal/noise split is the final to-origin against the ghost lag; and the terminal
    state distinguishes a truth that **crystallized** from one **dissipated** into noise
    and from a sign **retained but overwritten** (a fork that kept the sign and replaced
    its content). Descriptive, never a gate.
    """
    concept = glossary.concept(concept_id)
    chain = memory_chain(concept_id, glossary)
    conf = confluence(concept_id, glossary)

    density = bit_density(concept.retained_field())
    mass = density.bits
    velocity, span = _velocity(chain.links)
    inertia = round(mass / velocity, 4) if velocity > 0 else None

    signal = round(chain.survival, 4)
    decayed = any((ln.delta is not None and ln.delta < -0.001) for ln in chain.links)
    half_life = _half_life(signal, span, decayed)

    threshold = concept.threshold
    last_year = chain.carriers[-1].year if chain.carriers else None
    ghost_lag = (
        int(last_year - threshold)
        if (threshold is not None and last_year is not None and last_year > threshold)
        else 0
    )

    # Direction along the chain's net path through time.
    if not chain.carriers:
        direction = "held"
    elif chain.restored:
        direction = "reverted, then recovered"
    else:
        net = chain.carriers[-1].to_origin - chain.carriers[0].to_origin
        direction = "reverted" if net < -0.001 else "progressed" if net > 0.001 else "held"

    # Terminal state: the fork (retained-but-overwritten) is read before the signal, so a
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
    elif signal >= CRYSTALLIZED:
        state = "crystallized"
    else:
        state = "dissipated"

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
        signal=signal,
        half_life=half_life,
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
        rows = [head, f"  {'concept':<14}{'mass':>5}  {'inertia':>7}  {'signal':>6}  state"]
        for m in self.items:
            inert = f"{m.inertia:.1f}" if m.inertia is not None else "—"
            signal = f"{m.signal:.2f}" if m.carriers > 0 else "—"
            rows.append(f"  {m.concept:<14}{m.mass:>5.2f}  {inert:>7}  {signal:>6}  {m.state}")
        rows.append("  note: the breath truths are uniformly massive (meaning held whole); what "
                    "differs is the\n        outcome the ghost lag crystallized, not the mass. "
                    "Descriptive, never a ranking of worth.")
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
