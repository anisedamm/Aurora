"""The chronicle: the whole system read as one experience over linear time."""

from __future__ import annotations

from pathlib import Path

from interpretation.chronicle import (
    LEXEME,
    MYTHOLOGY,
    REMEMBRANCE,
    THRESHOLD,
    chronicle,
)
from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]


def _world():
    return load_glossary(ROOT / "glossary.json"), load_lexicon(ROOT / "lexicon.json")


def test_the_axis_is_linear_and_ordered_in_time():
    g, lex = _world()
    ch = chronicle(g, lex)
    years = [m.year for m in ch.moments]
    assert years == sorted(years)                 # one linear time scale, ascending
    first, last = ch.span
    assert first == -40000 and last == 1990       # from the first named necessity to wellbeing


def test_both_strands_are_present_on_one_axis():
    g, lex = _world()
    ch = chronicle(g, lex)
    kinds = {m.kind for m in ch.moments}
    assert MYTHOLOGY in kinds and LEXEME in kinds   # mythology and the language explosion, together
    # the four breath signs that held meaning whole
    assert {m.ref for m in ch.mythology} == {
        "labrys-knossos", "ankh-relief", "ouroboros-netherworld", "divine-order",
    }
    # the whole lexicon is the explosion strand
    assert len(ch.explosion) == len(lex.lexemes)


def test_non_phonetic_mythology_is_held_whole_before_the_inner_life_is_named():
    g, lex = _world()
    ch = chronicle(g, lex)
    # every breath sign is fixed before the inner life enters the lexicon
    last_myth = max(m.year for m in ch.mythology)
    assert ch.inner_life_dawn is not None
    assert last_myth < ch.inner_life_dawn         # mythology held whole early; inner life comes late


def test_the_inner_life_enters_late_and_climbs():
    g, lex = _world()
    ch = chronicle(g, lex)
    assert ch.inner_life_dawn == -400             # 'soul' is the first inner-experience word
    exp_years = [m.year for m in ch.experiential]
    # the inner-experience words cluster in the later axis, none among the earliest namings
    assert min(exp_years) == -400
    assert all(m.year >= -400 for m in ch.experiential)
    assert len(ch.experiential) == 13


def test_remembrances_and_thresholds_link_the_two_regimes():
    g, lex = _world()
    ch = chronicle(g, lex)
    # the threshold edges are placed for every breath tradition
    assert {m.ref for m in ch.moments if m.kind == THRESHOLD} == {
        "labrys", "ankh", "ouroboros", "divine-order",
    }
    # the Theogony is a remembrance carrying the divine order forward across the threshold
    theogony = next(m for m in ch.moments if m.ref == "theogony")
    assert theogony.kind == REMEMBRANCE
    assert theogony.year == -700
    assert "divine-order" in theogony.gloss


def test_chronicle_is_a_reader_not_a_ruler():
    g, lex = _world()
    s = chronicle(g, lex).summary
    assert "the system as one experience over linear time" in s
    assert "non-phonetic mythology and the language explosion on one axis" in s
    assert "a reader, not a ruler" in s
    assert "Descriptive" in s


def test_an_empty_record_is_handled():
    from interpretation.glossary import Glossary
    from interpretation.lexicon import Lexicon

    ch = chronicle(Glossary(), Lexicon())
    assert ch.moments == []
    assert ch.span is None
    assert ch.inner_life_dawn is None
    assert "empty record" in ch.verdict
