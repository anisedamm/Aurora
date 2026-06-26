"""The weave: paired antonym couples as one web — roots, hubs, and the keystone."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.lexicon import load_lexicon
from interpretation.weave import weave

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = ROOT / "relations.json"
LEXICON = ROOT / "lexicon.json"


def _world():
    return load_relations(RELATIONS), load_lexicon(LEXICON)


def test_root_antonyms_are_the_irreducible_bits():
    # the couples always paired no matter how derived: both poles bit-like
    rel, lex = _world()
    w = weave(rel, lex)
    roots = {c.axis for c in w.roots}
    assert roots == {"false|true", "noise|signal", "no|yes", "right|wrong"}
    assert all(c.root for c in w.roots)


def test_a_condensed_couple_is_not_a_root():
    rel, lex = _world()
    w = weave(rel, lex)
    justice_injustice = next(c for c in w.couples if c.axis == "injustice|justice")
    assert not justice_injustice.root            # justice carries a field — derived, not root


def test_hubs_have_the_most_branches_and_overlap():
    # the words with the most branches and overlap of synonyms and antonyms
    rel, lex = _world()
    w = weave(rel, lex)
    hub_terms = {n.term for n in w.hubs}
    assert hub_terms == {"freedom", "justice"}   # both at the top branch count
    assert all(n.branches == 7 for n in w.hubs)
    assert w.hubs[0].term == "freedom"           # overlap breaks the tie


def test_keystone_is_where_the_most_truth_of_meaning_lies():
    # the key defining word: the most others are defined in terms of it
    rel, lex = _world()
    w = weave(rel, lex)
    assert w.keystone.term == "self"
    assert w.keystone.defining_reach == 7        # seven words built on 'self'


def test_couples_and_terms_counted():
    rel, lex = _world()
    w = weave(rel, lex)
    assert len(w.couples) == 14
    assert len(w.nodes) == 14
    assert "the meaning web" in w.verdict


def test_keystone_holds_without_the_lexicon():
    # without the compounding web the reach is smaller, but self still leans hardest
    rel, _ = _world()
    w = weave(rel, None)
    assert w.keystone.term == "self"
    assert w.keystone.defining_reach == 4        # relations-only referrers
    # roots are unchanged — bit-likeness needs no lexicon
    assert {c.axis for c in w.roots} == {"false|true", "noise|signal", "no|yes", "right|wrong"}


def test_summary_answers_the_three_questions():
    rel, lex = _world()
    s = weave(rel, lex).summary
    assert "root antonyms" in s
    assert "hubs" in s
    assert "keystone" in s and "self" in s
    assert "never a gate" in s
