"""Folding: corroborating layers of depth, until a concept is deemed true — then woveable."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.fold import DEEMED_TRUE, FOLDING, GIVEN, fold, folding
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "lexicon.json"
RELATIONS = ROOT / "relations.json"


def _world():
    return load_lexicon(LEXICON), load_relations(RELATIONS)


def test_a_cornerstone_is_given_an_axiom_true_without_folding():
    lex, _ = _world()
    f = fold("fire", lex)
    assert f.fold_depth == 0 and f.status == GIVEN
    assert f.woveable                              # woveable as the ground, not by folding


def test_a_shallow_concept_is_still_folding_not_yet_truth():
    lex, _ = _world()
    f = fold("season", lex)                        # built only on fire -> 1 layer
    assert f.fold_depth == 1 and f.status == FOLDING
    assert not f.woveable                          # cannot be woven before deemed true


def test_a_deep_concept_is_deemed_true_and_woveable():
    lex, _ = _world()
    f = fold("justice", lex)
    assert f.status == DEEMED_TRUE and f.woveable
    assert f.fold_depth == 4 and f.corroboration == 8


def test_the_layers_are_strata_from_the_given_base_upward():
    lex, _ = _world()
    f = fold("justice", lex)
    assert f.layers[0].level == 0
    assert set(f.layers[0].members) == {"fire", "kin", "water"}   # the given base
    assert f.fold_depth == max(layer.level for layer in f.layers) + 1


def test_an_off_tree_term_is_a_given_axiom():
    # a bit or a breath value is not in the lexicon tree — given, true without folding
    lex, _ = _world()
    f = fold("signal", lex)
    assert f.status == GIVEN and f.woveable and f.fold_depth == 0


def test_the_weave_is_legitimate_when_every_woven_term_is_folded_or_given():
    lex, rel = _world()
    fl = folding(lex, rel)                         # default threshold 3
    assert fl.provisional == []                    # nothing woven before folded to truth
    assert "legitimate" in fl.verdict
    assert {f.word for f in fl.given} == {"fire", "kin", "water", "danger"}


def test_raising_the_threshold_surfaces_provisional_weaves():
    # folding precedes weaving: lift the bar and some woven terms are not yet deemed true
    lex, rel = _world()
    fl = folding(lex, rel, threshold=5)
    assert set(fl.provisional) == {"justice", "self", "soul"}   # woven, but folded < 5
    assert "provisional" in fl.verdict


def test_the_deepest_fold_and_the_precedence_message():
    lex, rel = _world()
    fl = folding(lex, rel)
    assert fl.deepest.fold_depth == 6              # alienation / wellbeing
    assert "folding precedes weaving" in fl.summary
