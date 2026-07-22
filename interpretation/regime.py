"""The regime axis: the mode of attention a culture brings to meaning.

The framework's v1 read a *word* carrying a *lexical sense*, and watched for
**anachronism** (a later sense projected onto an earlier usage). Beneath that sits
a deeper threshold this module names: the **mode of attention** a culture brings
to the world, of which the form of its writing is downstream.

  * **breath** - a participatory, holistic attention. Meaning is carried whole, by
    *conceptual* form: a symbol holds a weighted field of values at once (unity,
    belonging, divinity, ownership, paradoxical equilibrium) rather than spelling a
    sound. Writing is reserved for what is profound enough to need a form that
    outlives word of mouth. (Barfield's "original participation"; the right
    hemisphere's world in McGilchrist - living, contextual, present.)

  * **pump** - an analytic, segmenting attention. Meaning is mechanised into
    discrete, re-combinable units: the *phonetic* sign, which spells a sound and
    defers meaning to a lexicon. Efficient, transmissible, and blind to what it was
    not told to segment. (The left hemisphere's world - grasping, abstracting,
    re-presenting.)

The script follows the attention: a **conceptual** mark is the natural writing of
a breath culture, a **phonetic** sign of a pump culture. The **ghost lag** is the
residue of breath-meaning still moving under pump-language - and the cardinal error
this framework now catches is **phonetic projection**: reading a breath-era
conceptual sign (or a myth) in the pump mode, as if it carried strict lexical
meaning, when the context dictates the manifestation of what is meant.

This axis is an **authored map**, like everything here: a proxy for a real history
of consciousness, carrying its provenance, not the history itself. Pure stdlib.

A third regime is named here as the additive foundation for reading the **information
age** (the full design in `docs/spiral-scope.md`): **nerve** - a networked, associative
attention whose native script is **recombinant** (sense recomputed from a field of
neighbours / remix). It is the *mode*; the net is its *medium*, as the alphabet is the
pump's. breath -> pump -> nerve is an ordered sequence, each with a ghost lag to its
predecessor; breath and pump are unchanged - nerve and the aspect profile sit alongside.
"""

from __future__ import annotations

from dataclasses import dataclass

# Modes of attention (the deep axis).
BREATH = "breath"   # participatory, holistic - meaning carried whole
PUMP = "pump"       # analytic, segmenting - meaning mechanised into units
NERVE = "nerve"     # networked, associative - meaning recombined from a field
VALID_REGIMES = {BREATH, PUMP, NERVE}

# The regimes in order of succession; each has a ghost lag to the one before it.
REGIME_ORDER = (BREATH, PUMP, NERVE)

# Script modes (downstream of attention).
SCRIPT_CONCEPTUAL = "conceptual"   # a symbol holds a weighted field of meaning
SCRIPT_PHONETIC = "phonetic"       # a sign spells a sound, deferring to a lexicon
SCRIPT_RECOMBINANT = "recombinant" # a sign's sense is recomputed from its neighbours / remix
VALID_MODES = {SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC, SCRIPT_RECOMBINANT}

# The natural pairing of attention and script (not enforced - a culture can borrow a
# later sign for a profound purpose; that is exactly the threshold).
NATIVE_SCRIPT = {
    BREATH: SCRIPT_CONCEPTUAL,
    PUMP: SCRIPT_PHONETIC,
    NERVE: SCRIPT_RECOMBINANT,
}


def validate_regime(regime: str) -> None:
    if regime not in VALID_REGIMES:
        raise ValueError(f"unknown regime {regime!r}; expected one of {sorted(VALID_REGIMES)}")


def validate_mode(mode: str) -> None:
    if mode not in VALID_MODES:
        raise ValueError(f"unknown script mode {mode!r}; expected one of {sorted(VALID_MODES)}")


def predecessor(regime: str) -> str | None:
    """The regime immediately before this one in the succession, or None for breath."""
    validate_regime(regime)
    i = REGIME_ORDER.index(regime)
    return REGIME_ORDER[i - 1] if i > 0 else None


def is_phonetic_projection(usage_regime: str, usage_mode: str, read_mode: str) -> bool:
    """True when a breath/conceptual usage is being read in the pump/phonetic mode.

    This is the threshold error: imposing a later mode of attention on an earlier
    one - reading a symbol as if it spelled a word, a myth as if it reported a fact.
    """
    breath_side = usage_regime == BREATH or usage_mode == SCRIPT_CONCEPTUAL
    return breath_side and read_mode == SCRIPT_PHONETIC


def is_spiral_projection(returns_to: str | None, returns_to_grounded: bool) -> bool:
    """True when a re-coherence reading asserts a return without an honest ground.

    The L4 analogue of phonetic projection. Where phonetic projection imposes a later
    *mode of attention* on an earlier sign, spiral projection imposes the *re-coherence
    narrative* - manufacturing a breath value for a sign to "return to" - on a sign that
    never honestly had one (a nerve-native origin, or a refusal of meaning). A `returns_to`
    that is reached for, not grounded in an attested breath sign, is flagged, not honoured.
    """
    asserts_return = returns_to is not None
    return asserts_return and not returns_to_grounded


@dataclass(frozen=True)
class AspectProfile:
    """How a sign's attention is distributed across the three regimes, in [0, 1] each.

    A reading *alongside* the single `regime` label (never replacing it): not "this sign
    *is* breath," but "this is how its breath/pump/nerve aspects are weighted." A meme
    lights up on all three; the labrys is almost pure breath. An authored proxy that
    carries its provenance, like every map here - descriptive, never a gate.
    """

    breath: float = 0.0
    pump: float = 0.0
    nerve: float = 0.0

    def __post_init__(self) -> None:
        for name in REGIME_ORDER:
            v = getattr(self, name)
            if not 0.0 <= float(v) <= 1.0:
                raise ValueError(f"aspect {name!r} must be in [0, 1], got {v!r}")

    def as_dict(self) -> dict[str, float]:
        return {BREATH: self.breath, PUMP: self.pump, NERVE: self.nerve}

    def dominant(self) -> str:
        """The regime this sign leans on most (ties resolved by succession order)."""
        return max(REGIME_ORDER, key=lambda r: getattr(self, r))
