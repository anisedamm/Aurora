"""Proportion: the gradient of degrees between two opposed poles."""

from __future__ import annotations

from pathlib import Path

from interpretation.condensation import load_relations
from interpretation.gradient import find_gradient, load_gradients, read_gradients

ROOT = Path(__file__).resolve().parents[1]
GRADIENTS = ROOT / "gradients.json"
RELATIONS = ROOT / "relations.json"


def _grads():
    return load_gradients(GRADIENTS)


def test_a_gradient_fills_the_axis_with_degrees():
    g = next(x for x in _grads() if x.id == "temperature")
    assert g.poles == ("cold", "hot")
    assert g.resolution == 5                       # five degrees, not a 2-point cut
    assert g.place("warm") == 0.75                 # a proportion between the poles


def test_the_midpoint_is_the_balance_the_mean_between_extremes():
    g = next(x for x in _grads() if x.id == "temperature")
    assert g.balance.term == "lukewarm" and g.balance.position == 0.5


def test_the_mean_gradient_centres_on_moderation_equilibriums_shard():
    # the balance of deficiency<->excess is moderation — equilibrium's own pump-era shard
    g = next(x for x in _grads() if x.id == "the-mean")
    assert g.poles == ("deficiency", "excess")
    assert g.balance.term == "moderation"
    assert g.resolution == 3


def test_proportionality_is_zero_for_a_cut_and_rises_with_degrees():
    three = next(x for x in _grads() if x.id == "the-mean")
    five = next(x for x in _grads() if x.id == "temperature")
    assert three.proportionality == 0.5            # 1 - 1/2
    assert five.proportionality == 0.75            # 1 - 1/4 — finer proportion


def test_find_gradient_by_id_or_by_a_term_on_it():
    grads = _grads()
    g, focus = find_gradient("temperature", grads)
    assert g.id == "temperature" and focus == ""
    g, focus = find_gradient("warm", grads)        # by a degree on the scale
    assert g.id == "temperature" and focus == "warm"
    g, focus = find_gradient("nonesuch", grads)
    assert g is None


def test_place_returns_none_off_the_axis():
    g = next(x for x in _grads() if x.id == "regard")
    assert g.place("lukewarm") is None             # belongs to a different gradient


def test_the_whole_reading_separates_proportional_axes_from_bare_binaries():
    rel = load_relations(RELATIONS)
    gs = read_gradients(_grads(), rel)
    assert {g.id for g in gs.proportional} == {"temperature", "the-mean", "regard", "luminance"}
    assert "noise|signal" in gs.binaries           # the bits: collapsed to two poles, no gradient
    assert "false|true" in gs.binaries
    assert gs.finest.resolution == 5
    assert "proportion can be found beneath any apparent binary" in gs.summary
