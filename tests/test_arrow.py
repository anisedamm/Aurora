"""The arrow of time: the record's irreversibility, measured -- never asserted."""

from __future__ import annotations

from pathlib import Path

from interpretation.arrow import (
    ATTESTED_ARROWS,
    arrow_report,
    chain_arrow,
    glossary_arrow,
    spiral_arrow,
)
from interpretation.glossary import load_glossary
from interpretation.ledger import Ledger
from interpretation.quartet import load_quartets

ROOT = Path(__file__).resolve().parents[1]


def test_the_chain_arrow_makes_the_past_expensive():
    ca = chain_arrow(Ledger(ROOT / "interpretation_ledger.jsonl"))
    assert ca.intact
    assert ca.records > 0
    # the forge-cost gradient: the oldest entry is the most expensive to
    # rewrite (it invalidates everything after), the newest the cheapest --
    # irreversibility is measured, not asserted
    assert ca.oldest_forge_cost == ca.records
    assert ca.newest_forge_cost == 1
    assert ca.oldest_forge_cost > ca.newest_forge_cost
    assert "expensive to forge" in ca.summary


def test_the_spiral_is_never_walked_backward():
    sa = spiral_arrow(load_quartets(ROOT / "quartets.json"))
    # most lattice readings walk the spiral, and every walk runs
    # breath -> pump -> nerve: one hundred lattices, one direction
    assert sa.walked >= 90
    assert sa.forward == sa.walked
    assert sa.backward == 0
    assert "measured, not decreed" in sa.summary


def test_the_glossary_arrow_orders_the_attested_years():
    ga = glossary_arrow(load_glossary(ROOT / "glossary.json"))
    assert ga.usages > 0
    assert ga.earliest is not None and ga.latest is not None
    assert ga.earliest < ga.latest
    # millennia of attested memory, ordered one way
    assert ga.span_years and ga.span_years > 1000
    assert "attested memory" in ga.summary


def test_the_report_carries_the_arrows_and_the_guards():
    r = arrow_report(
        Ledger(ROOT / "interpretation_ledger.jsonl"),
        load_quartets(ROOT / "quartets.json"),
        load_glossary(ROOT / "glossary.json"),
    )
    # the three measured arrows
    assert "chain arrow" in r and "spiral arrow" in r and "glossary arrow" in r
    # the attested arrows recorded, not claimed
    for name in ATTESTED_ARROWS:
        assert name in r
    # Eddington's coinage has a birthday; the direction is cultural
    assert "Eddington" in r and "1927" in r
    assert "Aymara" in r
    # the grain of drift, attested (Traugott), observed never imposed
    assert "Traugott" in r
    assert "descriptive, never a gate" in r
