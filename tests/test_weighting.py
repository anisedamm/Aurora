"""Weighted meaning: a conceptual sign carries a field, and resonance measures fit."""

from __future__ import annotations

from interpretation.weighting import WeightedField

LABRYS = {"paradoxical-equilibrium": 0.30, "sovereignty": 0.25, "divinity": 0.25, "unity-belonging": 0.20}


def test_normalisation_makes_a_distribution():
    norm = WeightedField({"a": 2, "b": 2}).normalized()
    assert norm == {"a": 0.5, "b": 0.5}


def test_identical_fields_resonate_fully():
    assert WeightedField(LABRYS).resonance(LABRYS) == 1.0


def test_proportional_fields_resonate_fully():
    # resonance is over the normalised distribution, so scale does not matter
    doubled = {k: v * 2 for k, v in LABRYS.items()}
    assert WeightedField(LABRYS).resonance(doubled) == 1.0


def test_disjoint_fields_do_not_resonate():
    assert WeightedField(LABRYS).resonance({"syllabic-sign": 1.0}) == 0.0


def test_partial_overlap_is_between():
    r = WeightedField(LABRYS).resonance({"divinity": 1.0})
    assert 0.0 < r < 1.0


def test_empty_field_never_resonates():
    assert WeightedField({}).resonance(LABRYS) == 0.0
    assert WeightedField(LABRYS).resonance({}) == 0.0


def test_dominant_returns_heaviest_first():
    dom = WeightedField(LABRYS).dominant(n=2)
    assert dom[0][0] == "paradoxical-equilibrium"
    assert len(dom) == 2
