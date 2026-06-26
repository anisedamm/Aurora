"""Binary thought vs relational meaning: compression (the bit) vs condensation (the field)."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import (
    KIND_BIT,
    KIND_CONDENSED,
    RELATION_ANTONYM,
    RELATION_ASSOCIATE,
    RELATION_NONE,
    RELATION_SYNONYM,
    condense,
    connect,
    load_relations,
)
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = ROOT / "relations.json"
LEXICON = ROOT / "lexicon.json"


def _rel():
    return load_relations(RELATIONS)


def _lex():
    return load_lexicon(LEXICON)


def test_relations_load_with_symmetric_poles():
    rel = _rel()
    # a pole declared one way holds both ways, even for a bare opposite
    assert "signal" in rel.antonyms_of("noise")
    assert "noise" in rel.antonyms_of("signal")


def test_a_bit_is_pure_compression_no_field():
    # signal/noise — the floor of natural computing: one distinction, no field
    c = condense("signal", _rel(), _lex())
    assert c.compression == 1
    assert c.poles == ("noise",)
    assert c.condensation == 0
    assert c.kind == KIND_BIT
    assert c.ratio == 0.0
    assert "pure compression" in c.verdict


def test_right_wrong_is_a_bit_too():
    c = condense("right", _rel())          # no lexicon needed for the bare distinction
    assert c.kind == KIND_BIT
    assert c.poles == ("wrong",)
    assert c.condensation == 0


def test_a_word_keeps_the_bit_and_condenses_a_field():
    # justice keeps the binary distinction (justice|injustice) but gathers meaning on it
    c = condense("justice", _rel(), _lex())
    assert c.compression == 1
    assert c.poles == ("injustice",)
    assert c.kind == KIND_CONDENSED
    assert {"fairness", "equity"} <= set(c.field)       # the associated lexical meaning
    assert c.condensation > 0
    assert c.ratio == float(c.condensation)


def test_meaning_is_compounded_over_time_through_the_lexicon():
    # language as the compounded creation of meaning over time: wellbeing's ancestry
    c = condense("wellbeing", _rel(), _lex())
    assert "water" in c.compound and "freedom" in c.compound  # built on far earlier words
    assert c.oldest == "water"
    assert c.span is not None and c.span > 40000             # ~ -40000 -> 1990
    assert c.condensation >= len(c.compound)


def test_compounding_needs_the_lexicon():
    # without the lexicon the field still reads, but no compounded ancestry
    c = condense("wellbeing", _rel())
    assert c.compound == ()
    assert c.span is None
    assert c.condensation == len(c.field)


def test_an_unlexicalised_term_has_a_field_but_no_compound():
    c = condense("unity", _rel(), _lex())     # a breath value, not a lexicon lexeme
    assert c.compound == ()
    assert set(c.field) >= {"wholeness", "oneness"}
    assert c.kind == KIND_CONDENSED


def test_unknown_term_is_refused():
    import pytest

    with pytest.raises(KeyError):
        condense("telepathy", _rel(), _lex())


def test_connect_antonyms_are_the_binary_axis():
    conn = connect("signal", "noise", _rel(), _lex())
    assert conn.relation == RELATION_ANTONYM
    assert "binary axis" in conn.verdict


def test_connect_synonyms_share_condensed_meaning():
    conn = connect("freedom", "liberty", _rel(), _lex())   # liberty is a bare synonym name
    assert conn.relation == RELATION_SYNONYM


def test_connect_associated_by_a_shared_field():
    # not poles, not declared kin, but overlapping compounded/associated meaning
    conn = connect("freedom", "wellbeing", _rel(), _lex())
    assert conn.relation == RELATION_ASSOCIATE
    assert conn.overlap > 0.0
    assert conn.shared                                     # they share earlier words


def test_connect_unconnected_terms():
    conn = connect("signal", "justice", _rel(), _lex())
    assert conn.relation == RELATION_NONE
    assert conn.overlap == 0.0
