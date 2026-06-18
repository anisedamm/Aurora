"""The interpretation ledger: append-only, hash-chained, tamper-evident."""

from __future__ import annotations

from interpretation.ledger import Ledger


def _seed(tmp_path):
    led = Ledger(tmp_path / "ledger.jsonl")
    led.register(artifact_id="u", author="anise.damm", title="usage",
                 text="the revolution restored our ancient liberties",
                 kind="usage", word="revolution", citation="pamphlet, 1689", year=1689)
    led.register(artifact_id="r", author="anise.damm", title="reading",
                 text="read as a return to a prior order", kind="interpretation",
                 concept="revolution", sense="political-restoration", parents=["u"])
    return led


def test_register_chains_and_verifies(tmp_path):
    led = _seed(tmp_path)
    assert led.verify().ok
    assert len(led.records) == 2
    assert led.records[1].prev_hash == led.records[0].entry_hash


def test_reload_from_disk_preserves_the_chain(tmp_path):
    _seed(tmp_path)
    reloaded = Ledger(tmp_path / "ledger.jsonl")
    assert reloaded.verify().ok
    assert reloaded.records[1].parents == ["u"]


def test_tampering_breaks_the_chain(tmp_path):
    led = _seed(tmp_path)
    led.records[0].title = "forged"      # alter a recorded field in memory
    v = led.verify()
    assert not v.ok
    assert v.broken_at == 0


def test_by_id_returns_the_latest_version(tmp_path):
    led = Ledger(tmp_path / "ledger.jsonl")
    led.register(artifact_id="r", author="anise.damm", title="v1", text="first")
    led.register(artifact_id="r", author="anise.damm", title="v2", text="second")
    assert led.by_id("r").title == "v2"


def test_domain_fields_survive_the_round_trip(tmp_path):
    led = _seed(tmp_path)
    reloaded = Ledger(tmp_path / "ledger.jsonl")
    usage = reloaded.by_id("u")
    assert usage.kind == "usage" and usage.word == "revolution" and usage.year == 1689
