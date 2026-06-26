"""Equilibrium points: where cultures unite across geography and medium on one truth."""

from __future__ import annotations

from pathlib import Path

from interpretation.equilibria import MYTH, SYMBOL, WORD, equilibria
from interpretation.glossary import load_glossary

ROOT = Path(__file__).resolve().parents[1]


def _glossary():
    return load_glossary(ROOT / "glossary.json")


def test_cultures_unite_on_shared_equilibrium_points():
    eq = equilibria(_glossary())
    points = {p.value for p in eq.points}
    # values distinct cultures arrived at, each in their own way
    assert {"divinity", "equilibrium", "unity", "sovereignty"} <= points
    # divinity is the widest union: Minoan, Egyptian and Greek alike
    divinity = eq.point("divinity")
    assert divinity.cultures == ["Egyptian", "Greek", "Minoan"]
    assert len(divinity.cultures) == 3


def test_a_value_held_within_one_culture_is_not_a_geographic_union():
    eq = equilibria(_glossary())
    # eternity is held by two signs, but both are Egyptian — held, not a union
    assert eq.point("eternity") is None
    local = {p.value for p in eq.held_local}
    assert "eternity" in local


def test_the_union_crosses_media_not_only_geography():
    eq = equilibria(_glossary())
    divinity = eq.point("divinity")
    # carried as a myth (divine-order), a symbol (labrys, ankh) — non-phonetic both
    assert MYTH in divinity.media and SYMBOL in divinity.media
    media_of = {e.label: e.medium for e in divinity.holdings}
    assert media_of["divine-order"] == MYTH
    assert media_of["labrys"] == SYMBOL


def test_meaning_moves_from_high_density_to_explicit_refinement():
    eq = equilibria(_glossary())
    equilibrium = eq.point("equilibrium")
    # held whole at high density: each sign carries the value among several others
    assert equilibrium.hold_density > 1
    assert all(e.density > 1 for e in equilibrium.holdings)
    # then refined into explicit single-value words (density 1) in the same space
    refined = {e.label for e in equilibrium.refinements}
    assert {"balance", "justice", "moderation", "symmetry"} == refined
    assert all(e.density == 1 for e in equilibrium.refinements)
    assert all(e.medium == WORD for e in equilibrium.refinements)


def test_the_holdings_form_a_relational_timescale_across_cultures():
    eq = equilibria(_glossary())
    divinity = eq.point("divinity")
    years = sorted(e.year for e in divinity.holdings)
    # cultures meet on the same truth across a span of time and place
    assert years == [-3000, -1600, -1400]
    assert divinity.span == (-3000, -1400)
    assert len(divinity.regions) == 3   # three distinct geographies


def test_what_was_worth_committing_is_carried_on_the_point():
    eq = equilibria(_glossary())
    s = eq.point("equilibrium").summary
    assert "what was worth committing" in s
    assert "high density to explicit refinement" in s


def test_a_point_whose_dispersal_is_unmapped_is_reported_honestly():
    eq = equilibria(_glossary())
    # sovereignty unites Minoan and Egyptian but has no authored dispersal yet
    sovereignty = eq.point("sovereignty")
    assert sovereignty is not None
    assert sovereignty.refinements == []
    assert "not yet mapped" in sovereignty.summary


def test_equilibria_is_a_reader_not_a_ruler():
    s = equilibria(_glossary()).summary
    assert "where cultures unite across geography and medium" in s
    assert "a reader, not a ruler" in s
    assert "Descriptive, never a gate" in s
