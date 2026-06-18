"""The authored glossary loads into concepts, usages, and sense lattices."""

from __future__ import annotations

from pathlib import Path

from interpretation.glossary import load_glossary

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def test_glossary_loads_the_seed_concepts():
    g = load_glossary(GLOSSARY)
    assert "revolution" in g.concepts
    assert "democracy" in g.concepts


def test_concept_carries_its_sense_lattice():
    g = load_glossary(GLOSSARY)
    rev = g.concept("revolution")
    assert rev.lattice.precedes("celestial-return", "irreversible-rupture")
    assert rev.lattice.shift_into("irreversible-rupture") == "inversion"


def test_usage_lookup_is_global_across_concepts():
    g = load_glossary(GLOSSARY)
    assert g.usage("rev-1688").concept == "revolution"
    assert g.usage("dem-aristotle").concept == "democracy"


def test_lattice_for_usage_finds_the_right_concept():
    g = load_glossary(GLOSSARY)
    lat = g.lattice_for_usage("dem-tocqueville")
    assert "popular-self-government" in lat.senses


def test_democracy_is_an_amelioration():
    g = load_glossary(GLOSSARY)
    dem = g.concept("democracy")
    assert dem.lattice.shift_into("popular-self-government") == "amelioration"


def test_breath_concept_carries_a_threshold_and_conceptual_usage():
    g = load_glossary(GLOSSARY)
    labrys = g.concept("labrys")
    assert labrys.regime == "breath"
    assert labrys.threshold == -800
    u = g.usage("labrys-knossos")
    assert u.mode == "conceptual"
    assert u.field["paradoxical-equilibrium"] > 0
    assert u.artifact            # attested in material culture, not a quotation


def test_myth_ladder_is_a_descent_of_abstraction():
    g = load_glossary(GLOSSARY)
    lat = g.concept("divine-order").lattice
    assert lat.precedes("elemental", "olympian")        # the memory abstracts upward
    assert lat.shift_into("olympian") == "abstraction"


def test_pump_concepts_remain_phonetic():
    g = load_glossary(GLOSSARY)
    assert g.usage("rev-1789").mode == "phonetic"
    assert g.concept("revolution").regime == "pump"
