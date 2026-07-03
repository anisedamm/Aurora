"""The quartets: the synchronic 2x2 structure of meaning (a reader, never a gate)."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.quartet import load_quartets

QUARTETS = Path(__file__).resolve().parents[1] / "quartets.json"


def _load():
    return load_quartets(QUARTETS)


def test_the_quartets_load_with_their_keystones():
    qs = _load()
    ids = {q.id for q in qs.quartets}
    assert ids == {"existential", "spine", "process", "substrate", "held", "agency",
                   "animate", "language", "conscious-state", "perception", "perspective",
                   "intelligence", "crystallisation", "integrate", "resonance"}
    assert qs.keystones["spine"] == "the-logos"
    assert qs.keystones["held"] == "the-held-whole"
    assert qs.keystones["agency"] == "the-animating-source"
    assert qs.keystones["animate"] == "anima"
    assert qs.keystones["language"] == "the-living-word"
    assert qs.keystones["perception"] == "the-percept"
    assert qs.keystones["perspective"] == "the-point-of-view"
    assert qs.keystones["intelligence"] == "nous"
    assert qs.keystones["crystallisation"] == "the-crystal"


def test_crystallisation_names_the_act_and_the_mother_liquor():
    # the reflexive quartet: every quartet is a crystallisation; the singles won't crystallise
    cryst = _load().by_id("crystallisation")
    assert cryst.breath_pump_axis == "scale"
    assert cryst.cell("field", "fixed") == "lattice"
    assert "mother liquor" in cryst.reading.lower()
    assert "the 3" in cryst.reading and "the 4" in cryst.reading   # process walks the grid


def test_intelligence_grids_where_awareness_does_not():
    # the capstone: intelligence is a clean structural quartet (so it can be artificial),
    # while awareness/consciousness stays a single (so artificial awareness is undecidable)
    intel = _load().by_id("intelligence")
    assert intel.breath_pump_axis == "operation"   # analysis<->synthesis, clean
    assert set(intel.members) == {"reasoning", "knowledge", "creativity", "wisdom"}
    assert "category error of the age" in intel.reading
    # and consciousness is recorded as a single, not gridded
    assert "consciousness" in _load().bound["the_singles_resist"]


def test_perspective_localizes_the_boundary_as_its_blind_spot():
    # the systematic boundary appears WITHIN a quartet here: the blind-spot cell is the
    # standpoint that cannot see itself (the boundary within, beside the boundary above)
    persp = _load().by_id("perspective")
    assert persp.cell("standpoint", "conceal") == "blind spot"
    assert persp.breath_pump_axis is None     # soft, recorded honestly
    assert "blind spot" in persp.reading.lower() and "boundary" in persp.reading.lower()


def test_the_fractal_descent_perception_unfolds_a_conscious_state_cell():
    qs = _load()
    # conscious-state has perception as one of its cells (focus x content);
    # perception then unfolds into its own 2x2 -- the recursive layering
    assert qs.by_id("conscious-state").cell("focus", "content") == "perception"
    assert set(qs.by_id("perception").members) == {"sensation", "grouping", "prediction", "recognition"}
    # the bound records that a single's downstream grids even though the single does not
    assert "downstream DOES grid" in qs.bound["the_singles_resist"]


def test_language_quartet_is_the_frameworks_own_data_model():
    # the reflexive quartet: word/usage/concept/sense are Aurora's own units,
    # and the form<->meaning axis is the spine ("a word is not a concept") = breath<->pump
    lang = _load().by_id("language")
    assert set(lang.members) == {"word", "usage", "concept", "sense"}
    assert lang.breath_pump_axis == "side"
    assert lang.cell("form", "type") == "word"
    assert lang.cell("meaning", "token") == "sense"


def test_animate_frames_the_breath_axis_rather_than_dividing_on_it():
    # animate IS the breath pole, so breath<->pump is its outer frame (animate<->inanimate),
    # not an inner hinge -- recorded honestly as a null breath_pump_axis
    animate = _load().by_id("animate")
    assert animate.breath_pump_axis is None
    assert set(animate.members) == {"nourishment", "growth", "sensation", "generation"}


def test_the_held_quartet_is_a_clean_structural_2x2():
    # memory/density/complexity/coherence cross content<->structure with the whole<->part axis;
    # its breath<->pump axis is clean (named), not soft -- it is a structural quartet
    held = _load().by_id("held")
    assert held.breath_pump_axis == "grain"
    assert held.cell("structure", "part") == "complexity"
    assert held.cell("structure", "whole") == "coherence"
    assert held.cell("content", "part") == "memory"
    assert held.cell("content", "whole") == "density"


def test_each_quartet_is_a_two_by_two_of_its_members():
    for q in _load().quartets:
        assert len(q.members) == 4
        cells = {q.cell(r, c) for r in q.row_poles for c in q.col_poles}
        assert cells == set(q.members)  # the grid covers exactly the four members


def test_the_grid_places_members_at_the_crossing():
    spine = _load().by_id("spine")
    assert spine.cell("state", "form") == "integrity"
    assert spine.cell("state", "content") == "truth"
    assert spine.cell("vector", "content") == "direction"


def test_the_cognitive_quartets_name_the_breath_pump_axis():
    qs = _load()
    assert qs.by_id("process").breath_pump_axis == "grain"     # part <-> whole
    assert qs.by_id("substrate").breath_pump_axis == "ground"  # mental <-> embodied
    # and the framework is honest where the axis is soft, not forced:
    assert qs.by_id("existential").breath_pump_axis is None
    assert qs.by_id("spine").breath_pump_axis is None


def test_the_bound_is_recorded_so_it_is_not_numerology():
    qs = _load()
    assert "synchronic_only" in qs.bound
    assert "the_pentad_test" in qs.bound
    # the summary carries the bound and the number-structure
    s = qs.summary
    assert "synchronic only" in s
    assert "∞" in s


def test_integrate_is_the_spirals_own_verb():
    # the reflexive pair: integrate names the re-coherence operation itself
    # (continuous<->discrete IS the breath<->pump axis), and integrity is its
    # cell that touches the spine
    integ = _load().by_id("integrate")
    assert integ.breath_pump_axis == "substance"
    assert set(integ.members) == {"integral", "aggregate", "integrity", "integration"}
    assert integ.cell("continuous", "belonging") == "integrity"
    assert "spiral's own verb" in integ.reading.lower()


def test_resonance_names_its_own_trap():
    # resonance is Aurora's substance measure looking at itself; rapport is the
    # blind-spot cell (felt agreement mistaken for proof) -- descriptive, never a gate
    reson = _load().by_id("resonance")
    assert reson.breath_pump_axis == "facet"     # form<->meaning = structural<->substantive
    assert reson.cell("between", "meaning") == "rapport"
    assert "never a gate" in reson.reading.lower()
    assert "blind spot" in reson.reading.lower()


def test_unknown_quartet_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _load().by_id("nope")
