"""The atlas: the whole history of meaning, composed on one screen."""

from __future__ import annotations

from pathlib import Path

from interpretation.atlas import atlas
from interpretation.glossary import load_glossary
from interpretation.ledger import Ledger
from interpretation.lexicon import load_lexicon

ROOT = Path(__file__).resolve().parents[1]


def _world():
    return (
        Ledger(ROOT / "interpretation_ledger.jsonl"),
        load_glossary(ROOT / "glossary.json"),
        load_lexicon(ROOT / "lexicon.json"),
    )


def test_atlas_composes_the_whole_reading():
    led, g, lex = _world()
    a = atlas(led, g, lex, manifest_path=ROOT / "MANIFEST.md")
    assert a.signal.value == 1                       # the backing is sound
    assert a.breath.keystone.value == "divinity"     # the breath web's keystone
    assert a.hub == "labrys"                          # the hub sign
    assert {m.value for m in a.migrations} == {"divinity", "equilibrium", "unity"}
    assert len(a.explosion.points) == 6               # five pump eras plus the nerve era
    assert [arc.value for arc in a.arcs] == ["equilibrium"]   # the one unbroken arc
    assert a.arcs[0].reaches == 0.92


def test_atlas_is_a_reader_not_a_ruler():
    led, g, lex = _world()
    s = atlas(led, g, lex, manifest_path=ROOT / "MANIFEST.md").summary
    assert "history of meaning this record assembles" in s
    assert "keystone value: divinity" in s
    assert "the unbroken arc" in s
    assert "read-only, gates nothing" in s
