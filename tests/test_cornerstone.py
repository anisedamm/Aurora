"""The cornerstones: the root-base of the tree — innate, self-standing words built on nothing."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.cornerstone import cornerstones
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = ROOT / "relations.json"
LEXICON = ROOT / "lexicon.json"


def _world():
    return load_lexicon(LEXICON), load_relations(RELATIONS)


def test_the_cornerstones_are_the_primal_roots():
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    assert {w.word for w in cs.cornerstones} == {"fire", "kin", "water", "danger"}
    assert all(w.root and w.depth == 0 for w in cs.cornerstones)


def test_the_base_of_the_depth_is_what_the_most_rests_on():
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    assert cs.base.word == "fire"          # 20 of the tree's words ultimately rest on it
    assert cs.base.support == 20
    assert "where depth begins" in cs.summary


def test_cornerstones_are_self_standing_needing_no_relational_associate():
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    assert all(w.self_standing for w in cs.cornerstones)   # no antonym, no synonym needed
    assert all("needs no relational associate" in w.nature for w in cs.cornerstones)


def test_a_load_bearing_pillar_is_not_a_cornerstone_if_it_is_derived():
    # 'time' feels fundamental and bears much, but is built on season -> fire: a pillar, not a root
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    time = next(w for w in cs.words if w.word == "time")
    assert not time.root and time.depth > 0
    assert time.word in {w.word for w in cs.derived_pillars}
    assert time.word not in {w.word for w in cs.cornerstones}
    assert "derived pillar" in time.nature


def test_derived_pillars_are_load_bearing_but_built_on_earlier_words():
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    assert {w.word for w in cs.derived_pillars} == {"season", "time", "soul"}
    assert all(w.support >= 10 and not w.root for w in cs.derived_pillars)


def test_fire_is_the_deepest_cornerstone_by_score():
    lex, rel = _world()
    cs = cornerstones(lex, rel)
    assert cs.words[0].word == "fire"      # highest cornerstone score (root, most support, innate)
    assert cs.words[0].score > 0.9


def test_reads_without_relations():
    # without the relations map, roots are assumed self-standing by the map's silence
    lex, _ = _world()
    cs = cornerstones(lex, None)
    assert cs.base.word == "fire"
    assert all(w.self_standing for w in cs.cornerstones)
