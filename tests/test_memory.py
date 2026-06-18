"""The return path: remembrance is the faithful inverse of phonetic projection."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import Usage, load_glossary
from interpretation.memory import confluence, memory_chain, remember

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


# --- the memory chain: transmission across a lineage of rememberings --------

def test_chain_traces_decay_then_restoration():
    g = load_glossary(GLOSSARY)
    chain = memory_chain("ouroboros", g)
    assert [ln.by_id for ln in chain.carriers] == [
        "ouroboros-alchemy", "ouroboros-medieval", "ouroboros-jung"
    ]                                          # ordered in time
    assert chain.low_water == 0.55             # medieval ornament nearly lapses
    assert chain.survival == 0.85              # the modern reading carries it back
    assert chain.restored                      # decayed, then restored


def test_chain_links_report_origin_and_per_hop_resonance():
    g = load_glossary(GLOSSARY)
    by = {ln.by_id: ln for ln in memory_chain("ouroboros", g).links}
    assert by["ouroboros"].is_origin and by["ouroboros"].to_origin == 1.0
    assert by["ouroboros-alchemy"].to_origin == 0.90 and by["ouroboros-alchemy"].movement == "decayed"
    assert by["ouroboros-medieval"].to_origin == 0.55
    assert by["ouroboros-jung"].movement == "restored" and by["ouroboros-jung"].delta > 0


def test_a_single_hop_chain_is_not_restored():
    g = load_glossary(GLOSSARY)
    chain = memory_chain("divine-order", g)
    assert len(chain.carriers) == 1
    assert not chain.restored


def test_a_concept_with_no_rememberings_has_an_origin_only_chain():
    g = load_glossary(GLOSSARY)
    chain = memory_chain("revolution", g)      # a pump word nothing remembers
    assert chain.carriers == []
    assert chain.survival == 1.0               # nothing has carried it, so nothing is lost


# --- confluence: independent lineages corroborate or diverge ----------------

def test_independent_lineages_that_converge_corroborate_the_source():
    g = load_glossary(GLOSSARY)
    conf = confluence("ouroboros", g)
    roots = {ln.root for ln in conf.lineages}
    assert roots == {"ouroboros-alchemy", "ouroboros-jung"}   # two independent paths
    assert conf.independently_corroborated
    assert all(p.converges for p in conf.pairs)


def test_lineage_groups_carriers_by_their_root():
    g = load_glossary(GLOSSARY)
    conf = confluence("ouroboros", g)
    by_root = {ln.root: ln.members for ln in conf.lineages}
    # medieval extends the alchemy lineage; jung is its own path back to the source
    assert by_root["ouroboros-alchemy"] == ["ouroboros-alchemy", "ouroboros-medieval"]
    assert by_root["ouroboros-jung"] == ["ouroboros-jung"]


def test_divergent_lineages_are_a_fork_not_a_corroboration():
    g = load_glossary(GLOSSARY)
    conf = confluence("labrys", g)
    assert not conf.independently_corroborated
    preserved = {ln.root for ln in conf.corroborating}
    assert preserved == {"labrys-religious"}          # only the faithful path preserves it
    assert conf.pairs[0].convergence < 0.5            # the paths have forked
    assert "DIVERGENCE" in conf.verdict


def test_a_single_lineage_has_no_confluence_to_weigh():
    g = load_glossary(GLOSSARY)
    conf = confluence("divine-order", g)
    assert len(conf.lineages) == 1
    assert not conf.independently_corroborated
    assert "only one lineage" in conf.verdict
