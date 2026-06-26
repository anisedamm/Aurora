"""Tension: held opposite (paradox) vs excluded opposite (binary), and segmentation between."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.glossary import load_glossary
from interpretation.tension import (
    DIACHRONIC,
    EXCLUDED,
    HELD,
    NEUTRAL,
    SEGMENTED,
    SYNCHRONIC,
    tension,
    tensions,
)

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "glossary.json"
RELATIONS = ROOT / "relations.json"


def _world():
    return load_glossary(GLOSSARY), load_relations(RELATIONS)


def test_glossary_loads_the_authored_paradoxes():
    g, _ = _world()
    assert "paradoxical-equilibrium" in g.paradoxes
    assert g.paradoxes["paradoxical-equilibrium"]["value"] == "equilibrium"


def test_a_breath_sign_holds_its_opposite_as_a_paradox():
    g, rel = _world()
    t = tension("labrys", g, rel)
    assert t.kind == HELD and t.mode == SYNCHRONIC
    assert t.tension == 0.30
    assert any(p == "paradoxical-equilibrium" for p, _ in t.holds)


def test_the_ouroboros_holds_two_paradoxes_the_most_tension():
    g, rel = _world()
    t = tension("ouroboros", g, rel)
    assert t.kind == HELD
    assert t.tension == 0.65                      # cyclical-unity 0.35 + paradoxical-equilibrium 0.30
    assert len(t.holds) == 2


def test_an_inverted_word_holds_its_opposite_across_time():
    g, rel = _world()
    t = tension("revolution", g, rel)             # return -> rupture: the sense inverted
    assert t.kind == HELD and t.mode == DIACHRONIC


def test_a_bit_excludes_its_opposite_cleanly():
    g, rel = _world()
    t = tension("signal", g, rel)
    assert t.kind == EXCLUDED
    assert t.excludes == ("noise",)


def test_a_shard_is_segmented_and_may_become_its_own_binary():
    # justice is a shard carved from the paradox equilibrium, that then took its own antonym
    g, rel = _world()
    t = tension("justice", g, rel)
    assert t.kind == SEGMENTED
    assert t.fell_from == "equilibrium"
    assert t.excludes == ("injustice",)           # the paradox fully resolved into a distinction


def test_a_breath_sign_without_a_paradox_is_neutral():
    g, rel = _world()
    t = tension("ankh", g, rel)                   # holds life, divinity — but no held-opposition
    assert t.kind == NEUTRAL


def test_the_whole_corpus_shows_the_three_stances():
    g, rel = _world()
    ts = tensions(g, rel)
    assert {h.value for h in ts.held} == {"equilibrium", "unity", "genesis"}
    assert ts.keystone.value == "equilibrium" and ts.keystone.held_tension == 0.60
    assert "revolution" in ts.inverted
    assert {"signal", "true", "yes", "right"} <= set(ts.binaries)


def test_a_held_paradox_records_how_the_pump_segments_it():
    g, rel = _world()
    ts = tensions(g, rel)
    eq = next(h for h in ts.held if h.value == "equilibrium")
    assert eq.segmented_into == ["balance", "justice", "moderation", "symmetry"]
    assert [s for s, _ in eq.held_by] == ["labrys", "ouroboros"]
