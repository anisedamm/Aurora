"""Crystallisation: the crystal — order precipitated from the fluid.

The framework reads *meaning* settling out of usage. This module names the shape of
that settling itself, as a frame that any ordering process can be read against: how a
disordered fluid (of larvae, of lexemes, of attention) **precipitates** into a held,
spanning order — and how that order **dissolves** back. It is the coherence/decoherence
axis of the whole system, drawn as a single picture.

It rests on **two binary axes**, and nothing else:

  * **scale**  — `field` (the whole, extensive) vs `seed` (the local, a point).
  * **phase**  — `fluid` (disordered, mobile) vs `fixed` (ordered, committed).

Their tensor product (2 ⊗ 2 — a genuine *quartet*) gives four quadrants:

                 fluid                 fixed
      field      supersaturation       lattice
      seed       fluctuation           nucleus

  * **supersaturation** (field/fluid) — the whole field primed and over-full with
    latent order, yet nothing committed: maximal potential, zero realised.
  * **fluctuation** (seed/fluid) — local transient order that flickers in and out,
    sub-critical: a seed that has not held.
  * **nucleus** (seed/fixed) — one fluctuation has reached critical size and *holds*:
    committed order, but local — the threshold crossed.
  * **lattice** (field/fixed) — the nucleus has propagated order across the whole
    field: order that *spans*. This is the keystone, **the-crystal**.

The **quartetual equations.** Read a state as two order parameters in [0, 1] — extent
`sigma` (seed 0 → field 1) and order `phi` (fluid 0 → fixed 1). Its membership in the
four quadrants is the four bilinear products of the axes, which **partition unity**:

      supersaturation = sigma * (1 - phi)
      lattice         = sigma * phi
      fluctuation     = (1 - sigma) * (1 - phi)
      nucleus         = (1 - sigma) * phi
      ---------------------------------------------------  sum == 1

A state is thus a convex blend of the four corners. The keystone scalar is the lattice
weight, **coherence = sigma * phi** — realised order that spans the field. It is exactly
the shape of `lexicon.lexical_coherence` (the largest connected component's fraction of
the web): a nucleus is a tiny component; the lattice is the giant one. **Crystallisation**
is the rise of that scalar toward 1 (order precipitates); **decoherence** is its fall
toward 0 (the lattice fragments back to fluid). The canonical precipitation path runs
supersaturation → fluctuation → nucleus → lattice: concentrate, commit, propagate.

A worked proxy — a **coral reef** read on this frame (authored, illustrative, not a
claim of reef biology):

      supersaturation — warm, aragonite-saturated water with a larval supply: reef-ready, unbuilt
      fluctuation     — transient recruitment that settles and is swept away (sub-critical)
      nucleus         — a founding colony that holds: the first stable accreting site
      lattice         — the reef: accreted structure spanning the field (coherence)
      decoherence     — bleaching / storm fragmentation: the lattice dissolving to fluid

Like everything here this is an **authored map** — a proxy for an ordering process, not
the process itself. It measures and *describes* the shape of coherence; it ranks nothing
and gates nothing. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# The two axes.
SCALE_FIELD = "field"   # the whole, extensive
SCALE_SEED = "seed"     # the local, a point
VALID_SCALES = {SCALE_FIELD, SCALE_SEED}

PHASE_FLUID = "fluid"   # disordered, mobile
PHASE_FIXED = "fixed"   # ordered, committed
VALID_PHASES = {PHASE_FLUID, PHASE_FIXED}

# The four quadrants (the quartet) and the keystone.
SUPERSATURATION = "supersaturation"
LATTICE = "lattice"
FLUCTUATION = "fluctuation"
NUCLEUS = "nucleus"
KEYSTONE = "the-crystal"

# (scale, phase) -> quadrant name.
QUARTET: dict[tuple[str, str], str] = {
    (SCALE_FIELD, PHASE_FLUID): SUPERSATURATION,
    (SCALE_FIELD, PHASE_FIXED): LATTICE,
    (SCALE_SEED, PHASE_FLUID): FLUCTUATION,
    (SCALE_SEED, PHASE_FIXED): NUCLEUS,
}

# The canonical precipitation path: concentrate, commit, propagate.
PRECIPITATION = (SUPERSATURATION, FLUCTUATION, NUCLEUS, LATTICE)


def _extent(scale: str) -> float:
    """sigma: how widely order spans — seed 0.0, field 1.0."""
    return 1.0 if scale == SCALE_FIELD else 0.0


def _order(phase: str) -> float:
    """phi: how committed order is — fluid 0.0, fixed 1.0."""
    return 1.0 if phase == PHASE_FIXED else 0.0


def validate_scale(scale: str) -> None:
    if scale not in VALID_SCALES:
        raise ValueError(f"unknown scale {scale!r}; expected one of {sorted(VALID_SCALES)}")


def validate_phase(phase: str) -> None:
    if phase not in VALID_PHASES:
        raise ValueError(f"unknown phase {phase!r}; expected one of {sorted(VALID_PHASES)}")


def _unit(name: str, x: float) -> float:
    if not 0.0 <= x <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]; got {x}")
    return float(x)


@dataclass(frozen=True)
class Quadrant:
    """One corner of the quartet: a (scale, phase) pairing with its own gloss."""

    name: str
    scale: str
    phase: str
    gloss: str

    @property
    def extent(self) -> float:
        return _extent(self.scale)

    @property
    def order(self) -> float:
        return _order(self.phase)

    @property
    def coherence(self) -> float:
        """The lattice weight at this corner: spanning, realised order."""
        return self.extent * self.order


QUADRANTS: dict[str, Quadrant] = {
    SUPERSATURATION: Quadrant(
        SUPERSATURATION, SCALE_FIELD, PHASE_FLUID,
        "the whole field primed and over-full, yet nothing committed",
    ),
    LATTICE: Quadrant(
        LATTICE, SCALE_FIELD, PHASE_FIXED,
        "order propagated across the whole field — the crystal",
    ),
    FLUCTUATION: Quadrant(
        FLUCTUATION, SCALE_SEED, PHASE_FLUID,
        "local transient order, sub-critical: a seed that has not held",
    ),
    NUCLEUS: Quadrant(
        NUCLEUS, SCALE_SEED, PHASE_FIXED,
        "local order that holds: the threshold crossed",
    ),
}


def quadrant(scale: str, phase: str) -> Quadrant:
    """The quadrant for a (scale, phase) pairing."""
    validate_scale(scale)
    validate_phase(phase)
    return QUADRANTS[QUARTET[(scale, phase)]]


def memberships(extent: float, order: float) -> dict[str, float]:
    """The four quadrant weights of a state — the quartetual equations.

    A state (extent `sigma`, order `phi`) is a convex blend of the four corners; its
    weights are the bilinear products of the axes, and they sum to 1 exactly.
    """
    sigma = _unit("extent", extent)
    phi = _unit("order", order)
    return {
        SUPERSATURATION: sigma * (1.0 - phi),
        LATTICE: sigma * phi,
        FLUCTUATION: (1.0 - sigma) * (1.0 - phi),
        NUCLEUS: (1.0 - sigma) * phi,
    }


@dataclass
class CrystalState:
    """A point read on the frame: its quadrant blend and its coherence."""

    extent: float                 # sigma — seed 0 .. field 1
    order: float                  # phi   — fluid 0 .. fixed 1
    weights: dict[str, float] = field(default_factory=dict)

    @property
    def coherence(self) -> float:
        """Realised, spanning order — the lattice weight sigma * phi."""
        return self.weights[LATTICE]

    @property
    def dominant(self) -> str:
        """The quadrant the state sits nearest (ties resolve by the quartet order)."""
        order = (SUPERSATURATION, LATTICE, NUCLEUS, FLUCTUATION)
        return max(order, key=lambda q: self.weights[q])

    @property
    def summary(self) -> str:
        rows = [
            f"state (extent {self.extent:.2f}, order {self.order:.2f}) — "
            f"nearest {self.dominant}, coherence {self.coherence:.2f}",
        ]
        for q in (SUPERSATURATION, LATTICE, FLUCTUATION, NUCLEUS):
            rows.append(f"    {q:<16} {self.weights[q]:.2f}")
        rows.append("  note: the four weights partition unity; coherence is the lattice weight. "
                    "A description, never a ranking.")
        return "\n".join(rows)


def read_state(extent: float, order: float) -> CrystalState:
    """Read a state (extent, order) into its quadrant blend and coherence."""
    w = memberships(extent, order)
    return CrystalState(extent=_unit("extent", extent), order=_unit("order", order), weights=w)


def _as_state(stop) -> CrystalState:
    """Coerce a quadrant name or an (extent, order) pair into a CrystalState."""
    if isinstance(stop, CrystalState):
        return stop
    if isinstance(stop, str):
        if "," in stop:  # an "extent,order" coordinate pair, e.g. "0.3,1.0"
            extent, order = (float(x) for x in stop.split(",", 1))
            return read_state(extent, order)
        q = QUADRANTS.get(stop)
        if q is None:
            raise ValueError(f"unknown quadrant {stop!r}; expected one of {sorted(QUADRANTS)}")
        return read_state(q.extent, q.order)
    extent, order = stop
    return read_state(extent, order)


@dataclass
class Crystallisation:
    """A process read across the frame: does coherence precipitate, or decohere?"""

    stops: list[CrystalState] = field(default_factory=list)

    @property
    def coherences(self) -> list[float]:
        return [s.coherence for s in self.stops]

    @property
    def net(self) -> float:
        """Change in coherence from first stop to last."""
        if len(self.stops) < 2:
            return 0.0
        return self.stops[-1].coherence - self.stops[0].coherence

    @property
    def direction(self) -> str:
        """crystallising (coherence rises), decohering (falls), or held (flat)."""
        if self.net > 1e-9:
            return "crystallising"
        if self.net < -1e-9:
            return "decohering"
        return "held"

    @property
    def is_precipitation(self) -> bool:
        """True when the path is the canonical supersaturation→fluctuation→nucleus→lattice."""
        return tuple(s.dominant for s in self.stops) == PRECIPITATION

    @property
    def summary(self) -> str:
        path = " -> ".join(s.dominant for s in self.stops) or "—"
        rows = [
            f"crystallisation: {self.direction} (net coherence {self.net:+.2f})",
            f"  path: {path}",
        ]
        for s in self.stops:
            rows.append(f"    {s.dominant:<16} coherence {s.coherence:.2f}")
        if self.is_precipitation:
            rows.append("  this is the canonical precipitation path: concentrate, commit, propagate")
        rows.append("  note: an authored frame — coherence rising is order precipitated from the "
                    "fluid; falling is decoherence. Descriptive, never a gate.")
        return "\n".join(rows)


def crystallise(stops) -> Crystallisation:
    """Read a process — a sequence of quadrant names or (extent, order) pairs.

    Each stop becomes a `CrystalState`; the process's direction is the sign of the net
    change in coherence (the lattice weight) from first stop to last. A rise is
    crystallisation — order precipitating from the fluid; a fall is decoherence.
    """
    return Crystallisation(stops=[_as_state(s) for s in stops])


# A decohered lattice does not fall back to raw fluid: it leaves a **skeleton** — the
# substrate that once carried the order, held dormant through the trough. This is what
# separates re-coherence from a first crystallisation: order re-nucleates on a *retained*
# skeleton, under a new map, and climbs to a *new* lattice — not the old one restored.
SKELETON = "skeleton"


@dataclass
class Recoherence:
    """A second coherence, grown on the skeleton a decohered lattice left behind.

    The arc: coherence → decoherence → a dormant skeleton → re-nucleation (a spark of
    order re-committing at a seed, still spanning nothing) → re-coherence, climbing to a
    *new* lattice. It is not the old lattice restored — it is a new one, on the same
    substrate, under a new map. The same shape `arc.py` names when a whole sign,
    dispersed across the threshold, re-coheres into the phonetic web in a new mode.
    """

    stops: list[CrystalState] = field(default_factory=list)
    same_skeleton: bool = True   # authored: the substrate persisted through the trough
    new_map: bool = True         # authored: the re-coherence follows new rules, not the old

    @property
    def coherences(self) -> list[float]:
        return [s.coherence for s in self.stops]

    @property
    def _trough_index(self) -> int:
        cs = self.coherences
        if not cs:
            return 0
        return min(range(len(cs)), key=lambda i: (cs[i], i))

    @property
    def crest(self) -> float:
        """The first reef: the highest coherence reached before the trough."""
        return max(self.coherences[: self._trough_index + 1], default=0.0)

    @property
    def trough(self) -> float:
        """The bleached skeleton: the lowest coherence — order gone, substrate held."""
        cs = self.coherences
        return cs[self._trough_index] if cs else 0.0

    @property
    def recrest(self) -> float:
        """The rebuilding reef: the highest coherence reached after the trough."""
        return max(self.coherences[self._trough_index :], default=0.0)

    @property
    def renucleation(self) -> int | None:
        """The spark: the first stop after the trough where order re-commits at a seed.

        Order has turned (phi fixed) but nothing spans yet (coherence still low) — the
        turn happens before the climb is visible. 'It started with a sparkle, a light.'
        """
        for i in range(self._trough_index, len(self.stops)):
            s = self.stops[i]
            if s.order > 0.5 and s.coherence <= 0.5:
                return i
        return None

    @property
    def decohered(self) -> bool:
        return self.crest - self.trough > 1e-9

    @property
    def re_cohered(self) -> bool:
        return self.recrest - self.trough > 1e-9

    @property
    def is_recoherence(self) -> bool:
        """A fall to a skeleton, then a new climb grown on it — not restoration."""
        return self.decohered and self.re_cohered and self.same_skeleton

    @property
    def summary(self) -> str:
        verdict = "re-coherence" if self.is_recoherence else "not yet re-coherence"
        rows = [
            f"{verdict}: a second climb on a retained skeleton",
            f"  crest    — the first reef:        coherence {self.crest:.2f}",
            f"  trough   — the bleached skeleton: coherence {self.trough:.2f}"
            + ("  (substrate held)" if self.same_skeleton else "  (substrate lost)"),
            f"  re-crest — the rebuilding reef:   coherence {self.recrest:.2f}",
        ]
        spark = self.renucleation
        if spark is not None:
            rows.append(f"  spark    — re-nucleation at stop {spark}: order re-commits at a seed, "
                        "spanning nothing yet — the turn before the climb")
        if self.is_recoherence:
            rows.append("  this is re-coherence: not the old lattice restored, but a new one on the "
                        "same skeleton" + (", under a new map" if self.new_map else ""))
        rows.append("  note: an authored frame — the same skeleton, different life, a different "
                    "trajectory. Descriptive, never a gate.")
        return "\n".join(rows)


def recohere(stops, *, same_skeleton: bool = True, new_map: bool = True) -> Recoherence:
    """Read a process as re-coherence: a coherence that fell to a skeleton and climbed again.

    Each stop becomes a `CrystalState`; the reading finds the first reef (crest), the
    bleached skeleton it fell to (trough), the spark that re-committed order at a seed
    (re-nucleation), and the reef rebuilding on that retained substrate (re-crest). Unlike
    a first crystallisation, re-coherence starts from a *held skeleton*, not raw fluid,
    and climbs to a *new* lattice — the same ground, a new map.
    """
    return Recoherence(
        stops=[_as_state(s) for s in stops],
        same_skeleton=same_skeleton,
        new_map=new_map,
    )


@dataclass
class CrystalFrame:
    """The frame itself, on one screen: the two axes, the quartet, the keystone."""

    @property
    def summary(self) -> str:
        return "\n".join([
            "the crystal — order precipitated from the fluid",
            "  axes: scale (field/seed) x phase (fluid/fixed)",
            "             fluid             fixed",
            f"    field    {SUPERSATURATION:<16}  {LATTICE}",
            f"    seed     {FLUCTUATION:<16}  {NUCLEUS}",
            f"  keystone: {KEYSTONE} (the lattice — coherence = extent x order)",
            "  the quartetual equations (a state's four weights, summing to 1):",
            "    supersaturation = sigma * (1 - phi)      lattice = sigma * phi",
            "    fluctuation     = (1 - sigma) * (1 - phi) nucleus = (1 - sigma) * phi",
            "  precipitation: " + " -> ".join(PRECIPITATION),
            "  note: an authored frame for reading coherence/decoherence. "
            "Descriptive, never a gate.",
        ])


def frame() -> CrystalFrame:
    """The crystallisation frame, ready to print."""
    return CrystalFrame()
