"""The CLI front end: the authored map, the three layers, and record/align/publish."""

from __future__ import annotations

from pathlib import Path

from interpretation.__main__ import main

GLOSSARY = str(Path(__file__).resolve().parents[1] / "glossary.json")


def _g(*argv):
    return ["--glossary", GLOSSARY, *argv]


def test_concepts_lists_the_seed(capsys):
    assert main(_g("concepts")) == 0
    out = capsys.readouterr().out
    assert "revolution" in out and "democracy" in out


def test_trace_shows_descent_with_shifts(capsys):
    assert main(_g("trace", "revolution")) == 0
    out = capsys.readouterr().out
    assert "inversion" in out and "celestial-return" in out


def test_attest_passes_for_a_real_usage(capsys):
    assert main(_g("attest", "rev-1688")) == 0
    assert "ATTESTED" in capsys.readouterr().out


def test_read_and_drift(capsys):
    assert main(_g("read", "rev-1688", "political-restoration")) == 0
    assert main(_g("drift", "rev-1688", "irreversible-rupture")) == 0
    assert "ANACHRONISM" in capsys.readouterr().out


def test_sense_order_and_common(capsys):
    assert main(_g("sense", "order", "revolution")) == 0
    assert main(_g("sense", "common", "revolution",
                   "political-restoration", "irreversible-rupture")) == 0


def test_imprint_align_manifest_verify_roundtrip(tmp_path, capsys):
    led = str(tmp_path / "ledger.jsonl")
    out = str(tmp_path / "MANIFEST.md")

    def run(*argv):
        return main(["--glossary", GLOSSARY, "--ledger", led, *argv])

    assert run("imprint", "--id", "rev-1789", "--title", "usage", "--kind", "usage",
               "--text", "the revolution is the beginning of a new age", "--concept", "revolution") == 0
    assert run("imprint", "--id", "my-reading", "--title", "my reading",
               "--kind", "interpretation", "--concept", "revolution",
               "--sense", "irreversible-rupture", "--parents", "rev-1789",
               "--text", "an irreversible forward break founding a new order") == 0
    capsys.readouterr()
    assert run("align", "my-reading") == 0
    assert "interpretive alignment" in capsys.readouterr().out
    assert run("manifest", "--out", out) == 0
    assert run("verify") == 0
    assert "intact" in capsys.readouterr().out
    assert "defensive publication" in Path(out).read_text()


def test_mirror_source_without_lineage_warns(tmp_path, capsys):
    led = str(tmp_path / "ledger.jsonl")
    rc = main(["--ledger", led, "imprint", "--id", "m", "--title", "mirror reading",
               "--kind", "interpretation", "--source", "mirror", "--actor", "claude",
               "--text", "a gloss produced by a mirror"])
    assert rc == 0
    assert "warning" in capsys.readouterr().out      # reflection without lineage is surfaced
