"""The return path: remembrance is the faithful inverse of phonetic projection."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import Usage, load_glossary
from interpretation.memory import remember

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def test_concept_retained_field_falls_back_to_its_symbol():
    g = load_glossary(GLOSSARY)
    # ouroboros declares no concept-level field, so its truth is its attested symbol's
    assert g.concept("ouroboros").retained_field()["cyclical-unity"] > 0
    # divine-order declares one explicitly
    assert g.concept("divine-order").retained_field()["primal-powers"] > 0
    assert g.concept("divine-order").origin_year() == -3000


def test_theogony_faithfully_remembers_the_breath_era_cosmogony():
    g = load_glossary(GLOSSARY)
    r = remember(g.usage("theogony"), g)
    assert r.remembered == "divine-order"
    assert r.crosses_threshold                 # written at the pump side, truth on the breath side
    assert r.span_years == -700 - (-3000)      # 2300 years carried back
    assert r.fidelity >= 0.6                   # a faithful memory
    assert r.attested
    assert "faithful" in r.gloss


def test_alchemy_remembers_the_ouroboros_across_the_lag():
    g = load_glossary(GLOSSARY)
    r = remember(g.usage("ouroboros-alchemy"), g)
    assert r.crosses_threshold
    assert r.span_years == 300 - (-1300)       # 1600 years
    assert r.fidelity >= 0.6


def test_a_disjoint_memory_has_lapsed():
    g = load_glossary(GLOSSARY)
    bad = Usage(id="bad", word="x", quotation="x bears no relation here",
                citation="somewhere, 300 CE", year=300, regime="pump", mode="phonetic",
                field={"unrelated-notion": 1.0}, remembers="ouroboros")
    r = remember(bad, g)
    assert r.crosses_threshold
    assert r.fidelity == 0.0
    assert "lapsed" in r.gloss                 # a projection in disguise


def test_remembering_within_the_same_era_is_not_a_return():
    g = load_glossary(GLOSSARY)
    early = Usage(id="early", word="ouroboros", quotation="the ouroboros, of old",
                  citation="a Bronze Age source", year=-1000, regime="breath", mode="phonetic",
                  field={"cyclical-unity": 1.0}, remembers="ouroboros")
    r = remember(early, g)
    assert not r.crosses_threshold             # -1000 is still before the -300 threshold
    assert "not a return" in r.gloss


def test_remember_without_a_declared_return_raises():
    g = load_glossary(GLOSSARY)
    with pytest.raises(ValueError):
        remember(g.usage("rev-1789"), g)       # a pump word that remembers nothing
