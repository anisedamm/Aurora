"""The diachronic sense lattice: exact operations over an authored order of descent."""

from __future__ import annotations

import pytest

from interpretation.semantics import lattice_from_senses, validate_senses

REVOLUTION = [
    {"id": "return", "label": "cyclical return", "year": 1543},
    {"id": "restoration", "label": "political restoration", "year": 1660,
     "descends_from": ["return"], "shift": "metaphor"},
    {"id": "rupture", "label": "irreversible rupture", "year": 1789,
     "descends_from": ["restoration"], "shift": "inversion"},
    {"id": "transform", "label": "any transformation", "year": 1830,
     "descends_from": ["rupture"], "shift": "broadening"},
]


def _lat():
    return lattice_from_senses(REVOLUTION, concept="revolution")


def test_ancestry_is_the_chain_of_descent():
    lat = _lat()
    assert lat.ancestry("rupture") == {"return", "restoration", "rupture"}
    assert lat.ancestry("return") == {"return"}


def test_precedes_is_ancestry_containment():
    lat = _lat()
    assert lat.precedes("return", "rupture")        # the root is ancestral to all
    assert lat.precedes("restoration", "rupture")
    assert not lat.precedes("rupture", "return")    # descent is one-directional


def test_common_is_the_shared_root_meaning():
    lat = _lat()
    common = lat.common("restoration", "transform")
    assert common.senses == {"return", "restoration"}  # shared ancestry


def test_combine_is_the_union_of_fields():
    lat = _lat()
    combined = lat.combine("return", "rupture")
    assert combined.senses == {"return", "restoration", "rupture"}


def test_diachronic_order_respects_descent_and_time():
    lat = _lat()
    order = lat.diachronic_order(lat.senses.keys())
    assert order == ["return", "restoration", "rupture", "transform"]


def test_shift_into_names_the_kind_of_change():
    lat = _lat()
    assert lat.shift_into("return") == "origin"
    assert lat.shift_into("rupture") == "inversion"


def test_roots_and_leaves():
    lat = _lat()
    assert lat.roots() == ["return"]
    assert lat.leaves() == ["transform"]


# --- malformed maps are surfaced, never silently patched -------------------

def test_dangling_descent_is_reported():
    issues = validate_senses([{"id": "a", "descends_from": ["ghost"]}])
    assert any("dangling" in m for m in issues)


def test_cycle_is_reported():
    issues = validate_senses([
        {"id": "a", "descends_from": ["b"]},
        {"id": "b", "descends_from": ["a"]},
    ])
    assert any("cycle" in m for m in issues)


def test_self_descent_is_reported():
    issues = validate_senses([{"id": "a", "descends_from": ["a"]}])
    assert any("itself" in m for m in issues)


def test_unknown_shift_kind_is_reported():
    issues = validate_senses([
        {"id": "a"},
        {"id": "b", "descends_from": ["a"], "shift": "telepathy"},
    ])
    assert any("shift" in m for m in issues)


def test_construction_refuses_a_malformed_map():
    with pytest.raises(ValueError):
        lattice_from_senses([
            {"id": "a", "descends_from": ["b"]},
            {"id": "b", "descends_from": ["a"]},
        ])


def test_cross_lattice_composition_is_refused():
    a = _lat()
    b = _lat()
    with pytest.raises(ValueError):
        _ = a.field_of("return") | b.field_of("rupture")
