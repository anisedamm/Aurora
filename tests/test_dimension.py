"""Dimensional meaning: the tree as a system of axes (conveyance × culture × time × depth)."""

from __future__ import annotations

from pathlib import Path

from interpretation.dimension import SYMBOL, STORY, WORD, _conveyance_of, meaning_space
from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon
from interpretation.regime import BREATH, PUMP, SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "glossary.json"
LEXICON = ROOT / "lexicon.json"


def _world():
    return load_glossary(GLOSSARY), load_lexicon(LEXICON)


def test_conveyance_classifies_symbol_story_and_word():
    assert _conveyance_of(SCRIPT_CONCEPTUAL, BREATH) == SYMBOL     # a conceptual sign
    assert _conveyance_of(SCRIPT_PHONETIC, BREATH) == STORY        # a breath truth in words (myth)
    assert _conveyance_of(SCRIPT_PHONETIC, PUMP) == WORD           # a pump-era lexeme


def test_the_three_conveyance_dimensions_are_populated():
    g, lex = _world()
    sp = meaning_space(g, lex)
    assert sp.conveyance.size == 3
    assert sp.conveyance_counts[SYMBOL] == 3          # labrys, ankh, ouroboros
    assert sp.conveyance_counts[STORY] >= 1           # theogony and other breath-truth texts
    assert sp.conveyance_counts[WORD] >= len(lex.lexemes)   # every lexeme is a word


def test_culture_and_time_axes():
    g, lex = _world()
    sp = meaning_space(g, lex)
    assert sp.culture.values[0] == "shared"           # shared tongue first
    assert set(sp.culture.values) == {"shared", "Danish", "Nguni", "Portuguese", "Yaghan"}
    assert sp.time.values == ("primal", "agrarian", "classical", "modern", "reflexive")


def test_the_meaning_space_has_a_volume_and_a_depth_range():
    g, lex = _world()
    sp = meaning_space(g, lex)
    assert sp.volume == sp.conveyance.size * sp.culture.size * sp.time.size == 75
    assert sp.depth_min == 0                           # the cornerstones
    assert sp.depth_max >= 10                           # the deepest frontier leaves


def test_cross_dimensional_values_span_symbol_and_word():
    # the values held whole as a breath symbol AND dispersed into pump words
    g, lex = _world()
    sp = meaning_space(g, lex)
    assert sp.cross_dimensional == ["divinity", "equilibrium", "unity"]


def test_summary_names_the_dimensions():
    g, lex = _world()
    s = meaning_space(g, lex).summary
    assert "conveyance dimension" in s
    assert "culture dimension" in s
    assert "time dimension" in s
    assert "depth dimension" in s
    assert "never a gate" in s
