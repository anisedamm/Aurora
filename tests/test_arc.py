"""The arc: one value traced unbroken across both regimes, on one timeline."""

from __future__ import annotations

from pathlib import Path

from interpretation.arc import arc
from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]


def _world():
    return load_glossary(ROOT / "glossary.json"), load_lexicon(ROOT / "lexicon.json")


def test_equilibrium_runs_unbroken_from_the_labrys_to_flourishing():
    g, lex = _world()
    a = arc("equilibrium", g, lex)
    assert [s for s, _ in a.breath_signs] == ["labrys", "ouroboros"]   # held whole
    assert "justice" in a.shards                                       # dispersed
    assert a.lexicalized == [("justice", "justice")]                   # one shard re-lexicalised
    words = [s.word for s in a.thread]
    assert "justice" in words and "freedom" in words and "wellbeing" in words
    assert a.reaches == 0.92                                           # climbs to flourishing
    assert a.span_years == 1990 - (-1600)                             # ~3590 years, unbroken


def test_the_thread_climbs_the_sieve_to_success_axis():
    g, lex = _world()
    a = arc("equilibrium", g, lex)
    years = [s.year for s in a.thread]
    aligns = [s.alignment for s in a.thread]
    assert years == sorted(years)        # in time order
    assert aligns == sorted(aligns)      # alignment never falls back as the thread re-coheres


def test_a_value_whose_shards_were_not_relexicalised_has_no_thread():
    g, lex = _world()
    a = arc("divinity", g, lex)
    assert a.breath_signs                 # it was held whole in the breath web
    assert a.lexicalized == []            # but no shard re-entered this lexicon
    assert a.thread == []
