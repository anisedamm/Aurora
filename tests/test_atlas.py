"""The atlas: the whole history of meaning, composed on one screen."""

from __future__ import annotations

from pathlib import Path

from interpretation.atlas import atlas
from interpretation.condensation import load_relations
from interpretation.dimensionless import load_invariants
from interpretation.glossary import load_glossary
from interpretation.ledger import Ledger
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]


def _world():
    return (
        Ledger(ROOT / "interpretation_ledger.jsonl"),
        load_glossary(ROOT / "glossary.json"),
        load_lexicon(ROOT / "lexicon.json"),
    )


def test_atlas_composes_the_whole_reading():
    led, g, lex = _world()
    a = atlas(led, g, lex, manifest_path=ROOT / "MANIFEST.md")
    assert a.signal.value == 1                       # the backing is sound
    assert a.breath.keystone.value == "divinity"     # the breath web's keystone
    assert a.hub == "labrys"                          # the hub sign
    assert {m.value for m in a.migrations} == {"divinity", "equilibrium", "unity"}
    assert len(a.explosion.points) == 5               # the five eras
    assert [arc.value for arc in a.arcs] == ["equilibrium"]   # the one unbroken arc
    assert a.arcs[0].reaches == 0.92


def test_atlas_is_a_reader_not_a_ruler():
    led, g, lex = _world()
    s = atlas(led, g, lex, manifest_path=ROOT / "MANIFEST.md").summary
    assert "history of meaning this record assembles" in s
    assert "keystone value: divinity" in s
    assert "the unbroken arc" in s
    assert "read-only, gates nothing" in s


def test_atlas_composes_the_meaning_tree_when_the_maps_are_given():
    led, g, lex = _world()
    rel = load_relations(ROOT / "relations.json")
    invs = load_invariants(ROOT / "invariants.json")
    a = atlas(led, g, lex, relations=rel, invariants=invs, manifest_path=ROOT / "MANIFEST.md")
    # the later layers fold in: tension, the base/edge, the web, folding, dimensions, dimensionless
    assert a.tension.keystone.value == "equilibrium"     # the most-held paradox
    assert a.base.base.word == "fire"                     # the tree's cornerstone
    assert a.frontier.leading.word == "mamihlapinatapai"  # the frontier's furthest-out
    assert a.web.keystone.term == "self"                  # the web's keystone
    assert a.beyond.nearest.invariant.id == "distinction"  # nearest the dimensionless
    s = a.summary
    assert "-- the meaning tree --" in s
    assert "the bit excludes its opposite" in s
    assert "the gap to 'outlasts time' is unattestable" in s


def test_atlas_meaning_tree_is_omitted_without_the_maps():
    # the existing three-arg call composes only what glossary+lexicon supply
    led, g, lex = _world()
    a = atlas(led, g, lex, manifest_path=ROOT / "MANIFEST.md")
    assert a.web is None and a.base is None and a.beyond is None
    assert a.tension is not None and a.space is not None   # these need no extra map
