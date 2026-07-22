"""The spiral (L4): re-coherence, the two-facet verdict, and the refusal."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import CarryFacet, GatherShard, Recoherence, load_glossary
from interpretation.spiral import breath_values, recohere, scatter, spiral

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def _g():
    return load_glossary(GLOSSARY)


def _outcome(key):
    g = _g()
    return recohere(g.recoherences[key], breath_values(g)).outcome


# --- the spectrum: the measure discriminates --------------------------------

def test_the_faithful_pole_reads_faithful():
    assert _outcome("wiki") == "faithful"
    assert _outcome("meme") == "faithful"


def test_viral_reads_mixed():
    assert _outcome("viral") == "mixed"


def test_cloud_and_friend_read_counterfeit():
    # structurally a return, substantively hollow -- the synthetic breath
    assert _outcome("cloud") == "counterfeit"
    assert _outcome("friend") == "counterfeit"


def test_a_breath_origin_value_re_coheres_faithfully():
    assert _outcome("equilibrium") == "faithful"


# --- the refusal: resistant and spiral projection ---------------------------

def test_a_nerve_native_origin_is_resistant():
    g = _g()
    r = recohere(g.recoherences["spam"], breath_values(g))
    assert r.outcome == "resistant"
    assert not r.grounded
    assert not r.projection  # it asserts no return, so it cannot be projecting one


def test_a_reached_for_return_is_spiral_projection_and_resistant():
    g = _g()
    # a manufactured returns_to: a value the breath web does not hold
    bogus = Recoherence(
        id="bogus", sign="bogus", returns_to=("nonexistent-value",),
        gathers=(GatherShard("a"), GatherShard("b")),
        carries=(CarryFacet("x", 1.0, 1.0, 1.0),),
    )
    r = recohere(bogus, breath_values(g))
    assert r.outcome == "resistant"
    assert r.projection  # asserted a return, but it is not grounded


# --- the two facets, complexity, and scatter --------------------------------

def test_the_verdict_keeps_both_facets_separate():
    g = _g()
    r = recohere(g.recoherences["cloud"], breath_values(g))
    assert r.structural > 0.66          # structurally a real return
    assert r.substantive < 0.40         # substantively hollow
    # the pair is never collapsed to one number
    assert r.structural != r.substantive


def test_scatter_is_natures_other_face():
    g = _g()
    # friend (the bond flattened to an edge) scatters more than wiki (the clean commons)
    assert scatter(g.recoherences["friend"]) > scatter(g.recoherences["wiki"])


def test_complexity_counts_re_cohered_shards():
    g = _g()
    viral = recohere(g.recoherences["viral"], breath_values(g))   # 5 shards
    friend = recohere(g.recoherences["friend"], breath_values(g))  # 4 shards
    assert viral.complexity == 1.0
    assert friend.complexity == 0.8


# --- the whole cycle, on a value --------------------------------------------

def test_spiral_traces_the_whole_cycle_on_a_breath_origin_value():
    s = spiral("equilibrium", _g())
    # breath: the labrys held it whole (measured from the glossary)
    assert any(sign == "labrys" for sign, _ in s.breath_signs)
    # pump: the migration shards it re-coheres
    assert {g.term for g in s.gathers} == {"balance", "justice", "moderation", "symmetry"}
    # nerve: a faithful return
    assert s.reading.outcome == "faithful"


def test_spiral_on_a_nerve_native_origin_holds_no_breath_whole():
    s = spiral("spam", _g())
    assert s.breath_signs == []
    assert s.reading.outcome == "resistant"


def test_unknown_recoherence_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        spiral("nope", _g())
