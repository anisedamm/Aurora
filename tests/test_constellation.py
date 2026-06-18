"""The constellation: the system-level web of values a regime's signs share."""

from __future__ import annotations

from pathlib import Path

from interpretation.constellation import constellation
from interpretation.glossary import load_glossary

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def test_the_breath_web_has_four_signs():
    g = load_glossary(GLOSSARY)
    c = constellation(g)
    assert c.signs == ["ankh", "divine-order", "labrys", "ouroboros"]


def test_divinity_is_the_keystone_value():
    g = load_glossary(GLOSSARY)
    c = constellation(g)
    assert c.keystone.value == "divinity"
    assert c.keystone.reach == 3          # labrys, ankh, divine-order


def test_aliased_values_are_recognised_as_one():
    g = load_glossary(GLOSSARY)
    c = constellation(g)
    by_value = {v.value: v for v in c.values}
    # ankh's 'eternity-continuity' and ouroboros's 'eternity' are seen as one value
    assert by_value["eternity"].reach == 2
    # only load-bearing (reach >= 2) values are surfaced as such
    assert {v.value for v in c.load_bearing} == {"divinity", "unity", "equilibrium", "eternity", "sovereignty"}


def test_the_labrys_is_the_hub_of_the_web():
    g = load_glossary(GLOSSARY)
    c = constellation(g)
    pairs = {(e.a, e.b): e.affinity for e in c.affinities}
    assert pairs[("labrys", "ouroboros")] == 0.50
    assert ("ankh", "labrys") in pairs
    assert ["ankh", "labrys", "ouroboros"] in c.clusters
    assert c.islands == ["divine-order"]     # its cosmogonic values stand apart


def test_the_pump_regime_holds_no_weighted_web():
    g = load_glossary(GLOSSARY)
    c = constellation(g, regime="pump")
    assert c.signs == []                     # pump segments meaning into senses, not fields
    assert c.load_bearing == []
