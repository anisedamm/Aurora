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


def test_weigh_shows_the_retained_field(capsys):
    assert main(_g("weigh", "labrys-knossos")) == 0
    out = capsys.readouterr().out
    assert "paradoxical-equilibrium" in out and "committed to writing because" in out


def test_project_flags_the_ghost_lag(capsys):
    assert main(_g("project", "labrys-knossos")) == 0
    out = capsys.readouterr().out
    assert "PHONETIC PROJECTION" in out and "ghost lag" in out


def test_remember_shows_the_return_path(capsys):
    assert main(_g("remember", "theogony")) == 0
    out = capsys.readouterr().out
    assert "REMEMBRANCE" in out and "carries 'divine-order'" in out and "faithful" in out


def test_chain_traces_the_transmission_lineage(capsys):
    assert main(_g("chain", "ouroboros")) == 0
    out = capsys.readouterr().out
    assert "memory chain of 'ouroboros'" in out
    assert "decayed then restored" in out
    assert "ouroboros-jung" in out and "restored" in out


def test_confluence_corroborates_or_forks(capsys):
    assert main(_g("confluence", "ouroboros")) == 0
    assert "independently corroborated" in capsys.readouterr().out
    assert main(_g("confluence", "labrys")) == 0
    assert "DIVERGENCE" in capsys.readouterr().out


def test_density_weighs_a_signs_informational_mass(capsys):
    assert main(_g("density", "labrys-knossos")) == 0
    out = capsys.readouterr().out
    assert "bits" in out and "massive" in out


def test_inertia_reads_the_mechanics_of_a_truth(capsys):
    assert main(_g("inertia", "labrys")) == 0
    out = capsys.readouterr().out
    assert "MECHANICS of 'labrys'" in out
    assert "retained but overwritten" in out and "ghost lag" in out


def test_inertia_with_no_concept_reads_the_whole_web(capsys):
    assert main(_g("inertia")) == 0
    out = capsys.readouterr().out
    assert "mechanics of the breath web" in out
    assert "labrys" in out and "ankh" in out


def test_inertia_profile_traces_the_mass_hop_by_hop(capsys):
    assert main(_g("inertia", "ouroboros", "--profile")) == 0
    out = capsys.readouterr().out
    assert "mass profile of 'ouroboros'" in out
    assert "ouroboros-medieval" in out and "to-origin" in out


def test_constellation_shows_the_load_bearing_values(capsys):
    assert main(_g("constellation")) == 0
    out = capsys.readouterr().out
    assert "keystone value: divinity" in out
    assert "load-bearing values" in out and "island" in out


def test_migrate_tracks_a_value_across_the_threshold(capsys):
    assert main(_g("migrate", "equilibrium")) == 0
    out = capsys.readouterr().out
    assert "MIGRATION of 'equilibrium'" in out
    assert "held whole" in out and "balance" in out


def test_proliferation_traces_the_explosion(capsys):
    assert main(["proliferation"]) == 0
    out = capsys.readouterr().out
    assert "explosion of phonetic language" in out
    assert "primal" in out and "reflexive" in out and "coherence" in out


def test_untranslatables_lists_single_tongue_concepts(capsys):
    assert main(["untranslatables"]) == 0
    out = capsys.readouterr().out
    assert "hygge" in out and "Danish" in out


def test_signal_reports_the_one_verdict(capsys):
    rc = main(["signal"])
    out = capsys.readouterr().out
    assert "signal = integrity" in out
    assert rc == 0 and "= 1" in out and "trustworthy backing" in out


def test_arc_traces_one_thread_across_both_regimes(capsys):
    assert main(_g("arc", "equilibrium")) == 0
    out = capsys.readouterr().out
    assert "arc of 'equilibrium'" in out
    assert "justice" in out and "wellbeing" in out and "unbroken across the ghost lag" in out


def test_atlas_reads_the_whole_on_one_screen(capsys):
    assert main(["atlas"]) == 0
    out = capsys.readouterr().out
    assert "history of meaning this record assembles" in out
    assert "breath web" in out and "pump explosion" in out and "unbroken arc" in out


def test_regime_shows_the_threshold_and_sides(capsys):
    assert main(_g("regime", "divine-order")) == 0
    out = capsys.readouterr().out
    assert "threshold" in out and "breath" in out and "pump" in out


def test_read_conceptual_shows_a_weighted_reading(capsys):
    assert main(_g("read", "labrys-knossos")) == 0
    out = capsys.readouterr().out
    assert "weighted field" in out and "resonance" in out


def test_trace_breath_concept_shows_regime_and_field(capsys):
    assert main(_g("trace", "labrys")) == 0
    out = capsys.readouterr().out
    assert "breath/conceptual" in out


def test_mirror_source_without_lineage_warns(tmp_path, capsys):
    led = str(tmp_path / "ledger.jsonl")
    rc = main(["--ledger", led, "imprint", "--id", "m", "--title", "mirror reading",
               "--kind", "interpretation", "--source", "mirror", "--actor", "claude",
               "--text", "a gloss produced by a mirror"])
    assert rc == 0
    assert "warning" in capsys.readouterr().out      # reflection without lineage is surfaced
