"""Migration: a value held whole in the breath web, segmented after the threshold."""

from __future__ import annotations

from pathlib import Path

from interpretation.glossary import load_glossary
from interpretation.migration import migrate

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def test_equilibrium_is_held_whole_then_segmented():
    g = load_glossary(GLOSSARY)
    m = migrate("equilibrium", g)
    assert [s for s, _ in m.breath_signs] == ["labrys", "ouroboros"]   # held whole, by id
    assert m.breath_weight == 0.60
    assert m.dispersion == 4                                           # balance/justice/moderation/symmetry
    assert {sh.term for sh in m.shards} == {"balance", "justice", "moderation", "symmetry"}


def test_divinity_the_keystone_disperses_into_the_set_apart():
    g = load_glossary(GLOSSARY)
    m = migrate("divinity", g)
    assert m.concentration == 3                                        # ankh, divine-order, labrys
    assert m.breath_weight == 0.80
    assert {sh.term for sh in m.shards} == {"the sacred", "the holy", "transcendence"}


def test_a_value_held_in_breath_with_no_dispersal_mapped():
    g = load_glossary(GLOSSARY)
    m = migrate("sovereignty", g)                  # load-bearing (labrys, ankh) but unmapped
    assert m.concentration == 2
    assert m.dispersion == 0
    assert "dispersal not yet mapped" in m.verdict


def test_an_unknown_value_is_found_nowhere():
    g = load_glossary(GLOSSARY)
    m = migrate("telepathy", g)
    assert not m.breath_signs and not m.shards
    assert "not found" in m.verdict
