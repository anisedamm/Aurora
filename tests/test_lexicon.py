"""The lexicon over time: the explosion, the sieve->success climb, coherence, valuation."""

from __future__ import annotations

from pathlib import Path

from interpretation.lexicon import (
    lexical_coherence,
    load_lexicon,
    proliferation,
    untranslatables,
)

LEXICON = Path(__file__).resolve().parents[1] / "lexicon.json"


def test_lexicon_loads():
    lex = load_lexicon(LEXICON)
    assert len(lex.lexemes) == 31
    assert lex.lexemes["water"].alignment < 0.2 and not lex.lexemes["water"].experiential
    assert lex.lexemes["wellbeing"].alignment > 0.85 and lex.lexemes["wellbeing"].experiential


def test_proliferation_is_an_explosion():
    pts = proliferation(load_lexicon(LEXICON)).points
    assert [p.era for p in pts] == ["primal", "agrarian", "classical", "modern", "reflexive"]
    totals = [p.cumulative for p in pts]
    assert totals == sorted(totals) and totals[0] < totals[-1]   # strictly growing


def test_sieve_to_success_alignment_climbs():
    pts = proliferation(load_lexicon(LEXICON)).points
    aligns = [p.mean_alignment for p in pts]
    assert aligns == sorted(aligns)              # never falls back toward the sieve
    assert aligns[0] < 0.2 and aligns[-1] > 0.5  # from concrete necessity toward flourishing


def test_coherence_and_experience_rise_together():
    pts = proliferation(load_lexicon(LEXICON)).points
    coher = [p.coherence for p in pts]
    exp = [p.experiential_share for p in pts]
    assert coher == sorted(coher) and exp == sorted(exp)      # both non-decreasing
    assert coher[-1] > coher[0] and exp[-1] > exp[0]          # both genuinely rise
    assert exp[0] == 0.0                                      # the sieve named no inner states


def test_the_whole_web_coheres():
    assert lexical_coherence(load_lexicon(LEXICON)) == 1.0


def test_untranslatables_are_what_one_tongue_valued():
    items = untranslatables(load_lexicon(LEXICON))
    langs = {u.language for u in items}
    words = {u.word for u in items}
    # each tongue's word is its own untranslatable concept — even the kin words, which
    # name a shared *family* of experience but are precisely distinct (saudade ≠ hiraeth)
    assert langs == {"Danish", "Dutch", "German", "Nguni", "Portuguese", "Romanian", "Welsh", "Yaghan"}
    assert {"hygge", "gezelligheid", "Gemütlichkeit", "saudade", "hiraeth", "dor",
            "ubuntu", "mamihlapinatapai"} == words
    # a shared concept (freedom) is not claimed by any single tongue
    assert "freedom" not in words
