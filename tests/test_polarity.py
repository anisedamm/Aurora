"""The polarities: the 2 layer -- root antonym pairs, the first cut recorded."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.polarity import (
    VALID_KINDS,
    axis_pairs,
    load_polarities,
)
from interpretation.quartet import load_quartets

ROOT = Path(__file__).resolve().parents[1]
POLARITIES = ROOT / "polarities.json"
QUARTETS = ROOT / "quartets.json"


def _load():
    return load_polarities(POLARITIES)


def test_the_root_pairs_load_with_both_poles():
    po = _load()
    ids = {p.id for p in po.pairs}
    assert {"yes-no", "true-false", "right-wrong", "valid-invalid", "accept-reject",
            "approve-disapprove", "allow-refuse", "confirm-contradict",
            "provide-withhold", "interpret-misinterpret", "facilitate-inhibit",
            "whole-part", "cohere-scatter"} == ids
    for p in po.pairs:
        assert p.positive and p.negative and p.kind in VALID_KINDS
        assert p.derivation and p.line and p.aurora


def test_an_unnamed_kind_of_opposition_is_surfaced_not_guessed(tmp_path):
    bad = tmp_path / "polarities.json"
    bad.write_text(
        '{"pairs": [{"id": "x", "positive": "up", "negative": "down", "kind": "vibes"}]}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="typology"):
        load_polarities(bad)


def test_right_is_straight_and_wrong_is_twisted():
    # the derivations carry the finds: right = reg- (the straight line),
    # wrong = wringan (wrung, twisted); yes = 'so be it', an optative
    po = _load()
    rw = po.by_id("right-wrong")
    assert "straight" in rw.derivation.lower()
    assert "twisted" in rw.derivation.lower() or "wrung" in rw.derivation.lower()
    assert rw.kind == "contrary"                     # a scale with a middle
    yn = po.by_id("yes-no")
    assert yn.kind == "complementary"
    assert "so be it" in yn.derivation.lower()


def test_misinterpret_is_privative_not_a_true_antonym():
    # the honest flag: you cannot misinterpret without interpreting --
    # the negative is a defective mode of the positive, not its reversal
    mi = _load().by_id("interpret-misinterpret")
    assert mi.kind == "privative"
    assert "defective mode" in mi.derivation or "defective mode" in mi.line


def test_the_morpheme_line_and_the_guard_are_in_the_bound():
    po = _load()
    bound = po.bound
    # the central find: toward-morphemes vs against-morphemes = love/strife in grammar
    assert "toward" in bound["the_morpheme_line"].lower()
    assert "against" in bound["the_morpheme_line"].lower()
    assert "strife" in bound["the_morpheme_line"].lower()
    # the guard: no is not the enemy -- the custodian's refusals are negation
    # in service of truth; a yes that cannot say no is not assent but reflex
    assert "reflex" in bound["the_guard_on_no"]
    assert "NOT ATTESTED" in bound["the_guard_on_no"]
    # markedness: the negative pole is the derived member
    assert "marked" in bound["markedness"].lower()


def test_the_axes_are_the_live_polarities():
    # every quartet axis is an antonym pair already at work: 2 per lattice,
    # read live off the recorded map -- the 2s the 4s are built of
    qs = load_quartets(QUARTETS)
    live = axis_pairs(qs)
    assert len(live) == 2 * len(qs.quartets)
    assert all(len(ap.poles) == 2 for ap in live)
    # the master polarity appears among them (grain axes cross part/whole)
    assert any(set(ap.poles) == {"part", "whole"} for ap in live)
    # and the summary can render them alongside the root pairs
    s = _load().summary(qs)
    assert "the live polarities" in s
    assert f"{len(live)} axis-pairs" in s


def test_whole_hale_holy_is_the_oldest_blessing():
    wp = _load().by_id("whole-part")
    assert "hale" in wp.derivation.lower() and "holy" in wp.derivation.lower()
    assert "breath<->pump" in wp.line                 # the map's master axis


def test_unknown_pair_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _load().by_id("nope")
