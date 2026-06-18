"""signal = integrity x direction(truth): the framework's verdict on its own record."""

from __future__ import annotations

from pathlib import Path

from interpretation.glossary import load_glossary
from interpretation.imprint import Imprinter
from interpretation.ledger import Ledger
from interpretation.manifest import write_manifest
from interpretation.signal import compute_signal

ROOT = Path(__file__).resolve().parents[1]


def _repo():
    return Ledger(ROOT / "interpretation_ledger.jsonl"), load_glossary(ROOT / "glossary.json")


def test_the_repos_own_record_signals_trustworthy():
    led, g = _repo()
    s = compute_signal(led, g, manifest_path=ROOT / "MANIFEST.md")
    assert s.value == 1 and s.integrity == 1 and s.direction == 1


def test_tampering_zeroes_integrity_and_so_the_signal():
    led, g = _repo()
    led.records[0].title = "forged"                 # alter a recorded field
    s = compute_signal(led, g, manifest_path=ROOT / "MANIFEST.md")
    assert not s.chain_ok and s.integrity == 0 and s.value == 0


def test_a_stale_manifest_zeroes_integrity(tmp_path):
    led, g = _repo()
    stale = tmp_path / "M.md"
    stale.write_text("- chain head hash: `" + "0" * 64 + "`\n")
    s = compute_signal(led, g, manifest_path=stale)
    assert not s.manifest_fresh and s.integrity == 0


def test_an_ungrounded_reading_zeroes_direction(tmp_path):
    g = load_glossary(ROOT / "glossary.json")
    led = Ledger(tmp_path / "l.jsonl")
    Imprinter(led).imprint(artifact_id="floating", title="floating", kind="interpretation",
                           concept="revolution", text="a reading resting on no attested sign")
    m = tmp_path / "M.md"
    write_manifest(led, m, g)                        # fresh manifest -> integrity holds
    s = compute_signal(led, g, manifest_path=m)
    assert s.integrity == 1
    assert not s.grounded_ok and s.direction == 0 and s.value == 0


def test_an_unattributed_record_zeroes_direction(tmp_path):
    g = load_glossary(ROOT / "glossary.json")
    led = Ledger(tmp_path / "l.jsonl")
    led.register(artifact_id="anon", author="anise.damm", title="t", text="x",
                 kind="usage", source="bogus")       # invalid source, bypassing imprint's check
    m = tmp_path / "M.md"
    write_manifest(led, m, g)
    s = compute_signal(led, g, manifest_path=m)
    assert not s.provenance_ok and s.direction == 0


def test_a_recorded_projection_foil_does_not_lower_the_signal():
    # the labrys-lexical foil is a phonetic projection, kept on purpose; signal stays 1
    led, g = _repo()
    assert led.by_id("read-labrys-lexical") is not None
    assert compute_signal(led, g, manifest_path=ROOT / "MANIFEST.md").value == 1
