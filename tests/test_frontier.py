"""The frontier: meaning at the leaf-edge of the tree — unpolarised, singular, reaching."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.frontier import frontier
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = ROOT / "relations.json"
LEXICON = ROOT / "lexicon.json"


def _world():
    return load_lexicon(LEXICON), load_relations(RELATIONS)


def test_the_furthest_out_word_is_the_singular_unwoven_perception():
    lex, rel = _world()
    f = frontier(lex, rel)
    assert f.leading.word == "mamihlapinatapai"   # leaf, no antonym, no synonym, most aligned
    assert f.leading.unpolarised and f.leading.singular and f.leading.leaf
    assert "edge of what language" in f.summary


def test_the_unwoven_frontier_is_the_singular_untranslatables():
    lex, rel = _world()
    f = frontier(lex, rel)
    pure = {w.word for w in f.pure}
    assert pure == {"mamihlapinatapai", "ubuntu", "hygge", "saudade", "sublime", "nostalgia"}
    assert all(w.unpolarised and w.singular and w.leaf and w.experiential for w in f.pure)


def test_polarised_or_synonymed_leaves_are_only_partly_woven():
    # experiential leaves that have an antonym or a synonym score lower — partly woven in
    lex, rel = _world()
    f = frontier(lex, rel)
    by_word = {w.word: w for w in f.frontier}
    assert by_word["wellbeing"].polarised                    # has an antonym (suffering)
    assert not by_word["wellbeing"].singular                 # has synonyms (flourishing, welfare)
    assert by_word["wellbeing"].score < by_word["mamihlapinatapai"].score


def test_unpolarised_is_not_enough_interior_words_are_settled():
    # 'time' has no antonym but sits deep in the interior — comprehended, not frontier
    lex, rel = _world()
    f = frontier(lex, rel)
    time = next(w for w in f.words if w.word == "time")
    assert time.unpolarised and time.singular     # no opposite, no equivalent on the map
    assert not time.leaf                           # but built upon — interior
    assert time.word in {w.word for w in f.settled_unpolarised}
    assert time.word not in {w.word for w in f.frontier}


def test_a_leaf_that_is_not_a_perception_is_a_settled_abstraction():
    # 'cause' and 'virtue' are leaves but not experiential — not the perceptual frontier
    lex, rel = _world()
    f = frontier(lex, rel)
    cause = next(w for w in f.words if w.word == "cause")
    assert cause.leaf and not cause.experiential
    assert "settled abstraction" in cause.nature
    assert cause.word not in {w.word for w in f.frontier}


def test_frontier_reads_without_relations_everything_unpolarised_and_singular():
    # with no polarity/synonymy map, every word is unpolarised and singular by default;
    # the frontier then falls back to the experiential leaves of the tree
    lex, _ = _world()
    f = frontier(lex, None)
    assert all(w.unpolarised and w.singular for w in f.words)
    assert f.leading.leaf and f.leading.experiential


def test_verdict_counts_the_edge():
    lex, rel = _world()
    f = frontier(lex, rel)
    assert len(f.frontier) == 9          # experiential leaves
    assert len(f.pure) == 6              # of which unwoven (no antonym, no synonym)
    assert "frontier of the tree" in f.verdict
