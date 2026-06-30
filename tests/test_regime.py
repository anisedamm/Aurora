"""The attention axis: breath -> pump -> nerve, and the projection tests."""

from __future__ import annotations

import pytest

from interpretation.regime import (
    BREATH,
    PUMP,
    NERVE,
    SCRIPT_CONCEPTUAL,
    SCRIPT_PHONETIC,
    SCRIPT_RECOMBINANT,
    VALID_REGIMES,
    VALID_MODES,
    NATIVE_SCRIPT,
    REGIME_ORDER,
    AspectProfile,
    predecessor,
    is_phonetic_projection,
    is_spiral_projection,
)


def test_native_scripts():
    assert NATIVE_SCRIPT[BREATH] == SCRIPT_CONCEPTUAL
    assert NATIVE_SCRIPT[PUMP] == SCRIPT_PHONETIC


def test_reading_a_breath_sign_phonetically_is_projection():
    assert is_phonetic_projection(BREATH, SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC)


def test_reading_a_breath_sign_conceptually_is_not_projection():
    assert not is_phonetic_projection(BREATH, SCRIPT_CONCEPTUAL, SCRIPT_CONCEPTUAL)


def test_reading_a_pump_word_phonetically_is_not_projection():
    assert not is_phonetic_projection(PUMP, SCRIPT_PHONETIC, SCRIPT_PHONETIC)


# --- the nerve regime: the additive third (Phase A) -------------------------

def test_nerve_is_a_valid_regime_with_a_recombinant_script():
    assert NERVE in VALID_REGIMES
    assert SCRIPT_RECOMBINANT in VALID_MODES
    assert NATIVE_SCRIPT[NERVE] == SCRIPT_RECOMBINANT


def test_regime_order_is_the_succession():
    assert REGIME_ORDER == (BREATH, PUMP, NERVE)


def test_predecessor_walks_back_the_succession():
    assert predecessor(BREATH) is None
    assert predecessor(PUMP) == BREATH
    assert predecessor(NERVE) == PUMP


def test_breath_pump_paths_are_unchanged():
    # the binary the framework shipped with still reads identically
    assert NATIVE_SCRIPT[BREATH] == SCRIPT_CONCEPTUAL
    assert NATIVE_SCRIPT[PUMP] == SCRIPT_PHONETIC
    assert is_phonetic_projection(BREATH, SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC)


# --- spiral projection: the L4 guard (Phase A) ------------------------------

def test_asserting_a_return_without_a_ground_is_spiral_projection():
    assert is_spiral_projection("unity", returns_to_grounded=False)


def test_a_grounded_return_is_not_spiral_projection():
    assert not is_spiral_projection("unity", returns_to_grounded=True)


def test_no_asserted_return_is_not_spiral_projection():
    # a nerve-native origin that claims no return cannot be projecting one
    assert not is_spiral_projection(None, returns_to_grounded=False)


# --- the aspect profile: alongside the label, never replacing it ------------

def test_aspect_profile_holds_three_weights_and_a_dominant():
    p = AspectProfile(breath=0.7, pump=0.6, nerve=0.9)  # a meme-like sign
    assert p.as_dict() == {BREATH: 0.7, PUMP: 0.6, NERVE: 0.9}
    assert p.dominant() == NERVE


def test_aspect_profile_dominant_breaks_ties_by_succession():
    p = AspectProfile(breath=0.5, pump=0.5, nerve=0.5)
    assert p.dominant() == BREATH


def test_aspect_profile_rejects_out_of_range_weights():
    with pytest.raises(ValueError):
        AspectProfile(breath=1.5)
