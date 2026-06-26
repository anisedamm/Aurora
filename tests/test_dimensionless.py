"""The dimensionless: invariants proposed as universal truth, and the gap no record crosses."""

from __future__ import annotations

from pathlib import Path

from interpretation.dimensionless import (
    KIND_APRIORI,
    KIND_MANIFEST,
    dimensionless,
    load_invariants,
)
from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]
INVARIANTS = ROOT / "invariants.json"
GLOSSARY = ROOT / "glossary.json"
LEXICON = ROOT / "lexicon.json"


def _world():
    return load_invariants(INVARIANTS), load_glossary(GLOSSARY), load_lexicon(LEXICON)


def test_invariants_split_into_a_priori_and_manifest():
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    assert {r.invariant.id for r in d.a_priori} == {"distinction", "identity", "truth"}
    assert {r.invariant.id for r in d.manifest} == {"unity", "equilibrium", "recurrence"}


def test_the_distinction_is_nearest_the_dimensionless():
    # the bit (0/1) — where the whole framework began — is the a-priori ground beneath all
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    assert d.nearest.invariant.id == "distinction"
    assert d.nearest.kind == KIND_APRIORI


def test_a_priori_invariants_are_presupposed_and_unattestable():
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    truth = next(r for r in d.readings if r.invariant.id == "truth")
    assert truth.kind == KIND_APRIORI
    assert truth.attested_span is None
    assert "total" in truth.attestation                 # the gap to universal is total
    assert "witnessed by none" in truth.attestation


def test_a_manifest_invariant_is_measured_across_the_record():
    # equilibrium is held whole in breath signs and crosses the threshold into pump words
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    eq = next(r for r in d.readings if r.invariant.id == "equilibrium")
    assert eq.kind == KIND_MANIFEST
    assert eq.concentration == 2 and eq.dispersion == 4
    assert eq.crosses_threshold
    assert eq.attested_span == 3590                     # the demonstrable span, in years
    assert "unattestable" in eq.attestation


def test_recurrence_is_measured_from_its_sign():
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    rec = next(r for r in d.readings if r.invariant.id == "recurrence")
    assert rec.kind == KIND_MANIFEST
    assert rec.concentration >= 1                        # the ouroboros sign holds it
    assert rec.attested_span and rec.attested_span > 0


def test_a_manifest_invariant_without_a_pump_thread_reaches_only_the_breath_stratum():
    inv, g, lex = _world()
    d = dimensionless(inv, g, lex)
    unity = next(r for r in d.readings if r.invariant.id == "unity")
    assert unity.concentration == 2 and unity.dispersion == 3
    assert unity.attested_span is None                   # held whole, but not re-traced in a thread
    assert "breath stratum only" in unity.attestation


def test_the_layer_certifies_none_and_names_the_gap_it_cannot_measure():
    inv, g, lex = _world()
    s = dimensionless(inv, g, lex).summary
    assert "meaning that may outlast time" in s
    assert "cannot show one outlasts time" in s
    assert "least witness" in s
    assert "proxy for universality" in s
