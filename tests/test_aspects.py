"""The aspects view: the spiral seen whole, every sign by its regime profile."""

from __future__ import annotations

from pathlib import Path

from interpretation.aspects import aspects
from interpretation.glossary import load_glossary
from interpretation.regime import BREATH, NERVE, PUMP

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


def _a():
    return aspects(load_glossary(GLOSSARY))


def test_signs_cluster_by_their_dominant_regime():
    a = _a()
    assert set(a.clusters[BREATH]) >= {"ankh", "labrys", "ouroboros"}
    assert set(a.clusters[PUMP]) >= {"revolution", "democracy"}
    assert set(a.clusters[NERVE]) >= {"viral", "meme", "wiki", "cloud", "friend"}


def test_the_diagonal_is_the_signs_that_light_up_on_all_three():
    diag = set(_a().diagonal)
    # the synthesis signs score high on all three; a pure-breath sign does not
    assert {"viral", "wiki", "meme", "cloud"} <= diag
    assert "labrys" not in diag
    assert "revolution" not in diag


def test_the_nerve_keystone_is_what_the_cluster_returns_toward():
    v, reach = _a().keystone
    assert v == "unity"      # viral, meme, wiki, friend all return toward it
    assert reach == 4


def test_the_bridge_is_the_breath_sign_with_the_strongest_nerve_echo():
    # the ouroboros *is* the cycle -- the one breath sign with a real nerve echo
    assert _a().bridge == "ouroboros"


def test_each_nerve_sign_is_coloured_by_its_recohere_verdict():
    by_sign = {s.sign: s for s in _a().signs}
    assert by_sign["meme"].verdict == "faithful"
    assert by_sign["friend"].verdict == "counterfeit"
    assert by_sign["viral"].verdict == "mixed"
    # a pure-breath sign carries no re-coherence verdict
    assert by_sign["labrys"].verdict is None
    # and friend scatters more than meme
    assert by_sign["friend"].scatter > by_sign["meme"].scatter


def test_the_summary_is_a_reader_not_a_ruler():
    s = _a().summary
    assert "nerve keystone: unity" in s
    assert "the bridge: ouroboros" in s
    assert "gating nothing" in s or "gates nothing" in s
