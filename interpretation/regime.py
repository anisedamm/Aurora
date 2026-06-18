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
"""

from __future__ import annotations

# Modes of attention (the deep axis).
BREATH = "breath"   # participatory, holistic - meaning carried whole
PUMP = "pump"       # analytic, segmenting - meaning mechanised into units
VALID_REGIMES = {BREATH, PUMP}

# Script modes (downstream of attention).
SCRIPT_CONCEPTUAL = "conceptual"  # a symbol holds a weighted field of meaning
SCRIPT_PHONETIC = "phonetic"      # a sign spells a sound, deferring to a lexicon
VALID_MODES = {SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC}

# The natural pairing of attention and script (not enforced - a breath culture can
# borrow a phonetic sign for a profound purpose; that is exactly the threshold).
NATIVE_SCRIPT = {BREATH: SCRIPT_CONCEPTUAL, PUMP: SCRIPT_PHONETIC}


def validate_regime(regime: str) -> None:
    if regime not in VALID_REGIMES:
        raise ValueError(f"unknown regime {regime!r}; expected one of {sorted(VALID_REGIMES)}")


def validate_mode(mode: str) -> None:
    if mode not in VALID_MODES:
        raise ValueError(f"unknown script mode {mode!r}; expected one of {sorted(VALID_MODES)}")


def is_phonetic_projection(usage_regime: str, usage_mode: str, read_mode: str) -> bool:
    """True when a breath/conceptual usage is being read in the pump/phonetic mode.

    This is the threshold error: imposing a later mode of attention on an earlier
    one - reading a symbol as if it spelled a word, a myth as if it reported a fact.
    """
    breath_side = usage_regime == BREATH or usage_mode == SCRIPT_CONCEPTUAL
    return breath_side and read_mode == SCRIPT_PHONETIC
