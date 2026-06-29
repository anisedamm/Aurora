"""Equilibrium points: where cultures unite across geography and medium on one truth."""

from __future__ import annotations

from pathlib import Path

from interpretation.equilibria import (
    HELD_WHOLE,
    MYTH,
    NAMED,
    SYMBOL,
    WORD,
    equilibria,
)
from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]


def _world():
    return load_glossary(ROOT / "glossary.json"), load_lexicon(ROOT / "lexicon.json")


def test_cultures_unite_on_shared_equilibrium_points():
    g, lex = _world()
    eq = equilibria(g, lex)
    points = {p.value for p in eq.points}
    # values distinct cultures arrived at, each in their own way
    assert {"divinity", "equilibrium", "unity", "sovereignty"} <= points
    # divinity is the widest union: Minoan, Egyptian and Greek alike
    divinity = eq.point("divinity")
    assert divinity.cultures == ["Egyptian", "Greek", "Minoan"]
    assert len(divinity.cultures) == 3


def test_a_value_held_within_one_culture_is_not_a_geographic_union():
    g, lex = _world()
    eq = equilibria(g, lex)
    # eternity is held by two signs, but both are Egyptian — held, not a union
    assert eq.point("eternity") is None
    local = {p.value for p in eq.held_local}
    assert "eternity" in local


def test_the_union_crosses_media_not_only_geography():
    g, lex = _world()
    divinity = equilibria(g, lex).point("divinity")
    # carried as a myth (divine-order), a symbol (labrys, ankh) — non-phonetic both
    assert MYTH in divinity.media and SYMBOL in divinity.media
    media_of = {e.label: e.medium for e in divinity.holdings}
    assert media_of["divine-order"] == MYTH
    assert media_of["labrys"] == SYMBOL


def test_meaning_moves_from_high_density_to_explicit_refinement():
    g, lex = _world()
    equilibrium = equilibria(g, lex).point("equilibrium")
    assert equilibrium.union_mode == HELD_WHOLE
    # held whole at high density: each sign carries the value among several others
    assert equilibrium.hold_density > 1
    assert all(e.density > 1 for e in equilibrium.holdings)
    # then refined into explicit single-value words (density 1) in the same space
    refined = {e.label for e in equilibrium.refinements}
    assert {"balance", "justice", "moderation", "symmetry"} == refined
    assert all(e.density == 1 for e in equilibrium.refinements)
    assert all(e.medium == WORD for e in equilibrium.refinements)


def test_the_holdings_form_a_relational_timescale_across_cultures():
    g, lex = _world()
    divinity = equilibria(g, lex).point("divinity")
    years = sorted(e.year for e in divinity.holdings)
    # cultures meet on the same truth across a span of time and place
    assert years == [-3000, -1600, -1400]
    assert divinity.span == (-3000, -1400)
    assert len(divinity.regions) == 3   # three distinct geographies


def test_what_was_worth_committing_is_carried_on_the_point():
    g, lex = _world()
    s = equilibria(g, lex).point("equilibrium").summary
    assert "what was worth committing" in s
    assert "high density to explicit refinement" in s


def test_a_point_whose_dispersal_is_unmapped_is_reported_honestly():
    g, lex = _world()
    # sovereignty unites Minoan and Egyptian but has no authored dispersal yet
    sovereignty = equilibria(g, lex).point("sovereignty")
    assert sovereignty is not None
    assert sovereignty.refinements == []
    assert "not yet mapped" in sovereignty.summary


def test_tongues_converge_on_one_experience_at_the_refined_end():
    g, lex = _world()
    eq = equilibria(g, lex)
    longing = eq.point("longing-for-the-absent")
    assert longing is not None
    assert longing.union_mode == NAMED
    # distinct tongues, separated by geography, each named the same family of experience
    assert longing.cultures == ["Portuguese", "Romanian", "Welsh"]
    # at the refined end: every holding is a single explicit word (density 1)
    assert all(e.density == 1 and e.medium == WORD for e in longing.holdings)
    assert longing.refinements == []
    assert "kin, not identical" in longing.summary


def test_cosy_togetherness_unites_three_tongues():
    g, lex = _world()
    cosy = equilibria(g, lex).point("cosy-togetherness")
    assert {e.label for e in cosy.holdings} == {"hygge", "gezelligheid", "Gemütlichkeit"}
    assert cosy.cultures == ["Danish", "Dutch", "German"]


def test_the_holding_reason_comes_from_a_breath_sign_not_a_phonetic_crossing():
    g, lex = _world()
    divinity = equilibria(g, lex).point("divinity")
    s = divinity.summary
    # divine-order's only usage (theogony) is phonetic — a crossing, not a breath holding —
    # so its committed_because must NOT be surfaced as 'what was worth committing'
    assert "phonetic form" not in s
    # the reason must come from a breath sign actually held whole (the labrys)
    assert "to hold and transmit the society's axis" in s
    # divine-order is still listed as a held-whole myth, just without a holding-reason
    assert any(e.label == "divine-order" and e.rationale == "" for e in divinity.holdings)


def test_held_whole_and_named_points_are_grouped():
    g, lex = _world()
    eq = equilibria(g, lex)
    assert {p.value for p in eq.held_whole} == {"divinity", "sovereignty", "equilibrium", "unity"}
    assert {p.value for p in eq.named} == {"longing-for-the-absent", "cosy-togetherness"}


def test_without_a_lexicon_only_the_breath_points_are_found():
    g, _ = _world()
    eq = equilibria(g)   # lexicon optional — breath web still reads
    assert {p.value for p in eq.named} == set()
    assert eq.point("divinity") is not None


def test_equilibria_is_a_reader_not_a_ruler():
    g, lex = _world()
    s = equilibria(g, lex).summary
    assert "where cultures unite across geography and medium" in s
    assert "named across tongues" in s
    assert "a reader, not a ruler" in s
    assert "Descriptive, never a gate" in s
