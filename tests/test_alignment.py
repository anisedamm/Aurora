"""Interpretive alignment = purpose x fidelity, and how fidelity accrues."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.alignment import interpretive_alignment_of
from interpretation.glossary import load_glossary
from interpretation.imprint import Imprinter
from interpretation.ledger import Ledger

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"

T1 = "an irreversible forward break that founds a wholly new political order"
T2 = "the events of 1688 understood as a total rupture sweeping away the past"
T3 = "a one-way break with the old regime beginning a new historical era"
T6 = "building on the rupture reading the break cannot be undone once it is made"


@pytest.fixture
def world(tmp_path):
    g = load_glossary(GLOSSARY)
    led = Ledger(tmp_path / "ledger.jsonl")
    imp = Imprinter(led)
    # two attested usages, recorded as usages so grounding can find them
    imp.imprint(artifact_id="rev-1789", title="usage 1789", kind="usage",
                text=g.usage("rev-1789").quotation, concept="revolution")
    imp.imprint(artifact_id="rev-1688", title="usage 1688", kind="usage",
                text=g.usage("rev-1688").quotation, concept="revolution")
    # r1: grounded, in-period reading by the author
    imp.imprint(artifact_id="r1", title="rupture reading", text=T1, kind="interpretation",
                concept="revolution", sense="irreversible-rupture", parents=["rev-1789"])
    # r2: the anachronism — 1688 read in the post-1789 sense
    imp.imprint(artifact_id="r2", title="anachronistic reading", text=T2, kind="interpretation",
                concept="revolution", sense="irreversible-rupture", parents=["rev-1688"])
    # r3: an independent reader corroborates the rupture sense
    imp.imprint(artifact_id="r3", title="independent reading", text=T3, kind="interpretation",
                author="j.scholar", concept="revolution", sense="irreversible-rupture",
                parents=["rev-1789"])
    # r6: a third reader builds directly on r1
    imp.imprint(artifact_id="r6", title="derived reading", text=T6, kind="interpretation",
                author="k.reader", concept="revolution", sense="irreversible-rupture",
                parents=["r1"])
    return led, g


def test_anachronistic_reading_forfeits_all_fidelity(world):
    led, g = world
    a = interpretive_alignment_of("r2", led, g)
    assert a.anachronistic
    assert a.fidelity == 0.0
    assert a.value == 0.0
    assert "anachronism" in a.gloss


def test_grounded_corroborated_reading_is_fully_aligned(world):
    led, g = world
    a = interpretive_alignment_of("r1", led, g)
    assert a.purpose == 1.0          # nothing preceded it
    assert a.grounded
    assert not a.anachronistic
    assert a.corroborators == ["j.scholar", "k.reader"]
    assert a.fidelity == 1.0         # grounded (0.5) + full corroboration (0.5)
    assert a.value == 1.0
    assert a.influence == 1          # r6 builds on it


def test_ungrounded_reading_loses_the_grounding_half_of_fidelity(tmp_path):
    g = load_glossary(GLOSSARY)
    led = Ledger(tmp_path / "ledger.jsonl")
    imp = Imprinter(led)
    imp.imprint(artifact_id="rev-1789", title="usage", kind="usage",
                text=g.usage("rev-1789").quotation, concept="revolution")
    imp.imprint(artifact_id="grounded", title="grounded", text=T1, kind="interpretation",
                concept="revolution", sense="irreversible-rupture", parents=["rev-1789"])
    imp.imprint(artifact_id="floating", title="floating", text=T3, kind="interpretation",
                concept="revolution", sense="irreversible-rupture", parents=[])
    floating = interpretive_alignment_of("floating", led, g)
    grounded = interpretive_alignment_of("grounded", led, g)
    assert not floating.grounded
    assert floating.fidelity < grounded.fidelity


def test_a_duplicate_reading_has_no_purpose(world):
    led, g = world
    Imprinter(led).imprint(artifact_id="dup", title="dup", text=T1, kind="interpretation",
                           concept="revolution", sense="irreversible-rupture",
                           parents=["rev-1789"])
    a = interpretive_alignment_of("dup", led, g)
    assert a.purpose == 0.0
    assert a.novelty_verdict == "DUPLICATE"


def test_alignment_of_a_missing_record_raises(world):
    led, g = world
    with pytest.raises(KeyError):
        interpretive_alignment_of("nope", led, g)
