"""The attention axis: breath vs pump, and the phonetic-projection test."""

from __future__ import annotations

from interpretation.regime import (
    BREATH,
    PUMP,
    SCRIPT_CONCEPTUAL,
    SCRIPT_PHONETIC,
    NATIVE_SCRIPT,
    is_phonetic_projection,
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
