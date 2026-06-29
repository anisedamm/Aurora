"""The mechanics of meaning: bit-density (mass), inertia, and ghost-lag crystallization."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import load_glossary
from interpretation.inertia import bit_density, mechanics, mechanics_web

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


# --- bit-density: how much meaning a field holds -----------------------------

def test_a_single_value_field_is_massless():
    # The labrys read as a bare syllable (the projection foil) carries no distinction.
    d = bit_density({"syllabic-sign": 1.0})
    assert d.bits == 0.0
    assert d.held == 1
    assert "massless" in d.gloss


def test_an_empty_field_is_massless():
    d = bit_density({})
    assert d.bits == 0.0
    assert d.held == 0


def test_a_breath_sign_is_massive():
    g = load_glossary(GLOSSARY)
    d = bit_density(g.usage("labrys-knossos").field)
    assert d.held == 4
    assert d.bits > 1.5          # four values held whole, in proportion
    assert "massive" in d.gloss


def test_holding_meaning_whole_outweighs_a_single_lexeme():
    g = load_glossary(GLOSSARY)
    whole = bit_density(g.usage("ouroboros-netherworld").field).bits
    lexeme = bit_density({"syllabic-sign": 1.0}).bits
    assert whole > lexeme        # the breath sign is more massive than the bare sign


# --- the mechanics of a truth across the ghost lag ---------------------------

def test_ouroboros_crystallized_as_signal():
    g = load_glossary(GLOSSARY)
    m = mechanics("ouroboros", g)
    assert m.state == "crystallized"
    assert m.signal == pytest.approx(0.85, abs=0.01)
    assert m.noise == pytest.approx(0.15, abs=0.01)
    assert m.crystallization == 85
    assert m.direction == "reverted, then recovered"   # decayed in heraldry, restored by Jung


def test_the_labrys_is_retained_but_overwritten():
    # The founding image made measurable: the sign is kept, its content replaced.
    g = load_glossary(GLOSSARY)
    m = mechanics("labrys", g)
    assert m.state == "retained-overwritten"
    assert m.overwritten is not None
    lineage, to_origin = m.overwritten
    assert lineage == "labrys-emblem"
    assert to_origin == pytest.approx(0.40, abs=0.01)   # equilibrium overwritten by sovereign power
    assert "retained but overwritten" in m.state_gloss


def test_mass_resists_drift_as_inertia():
    g = load_glossary(GLOSSARY)
    m = mechanics("ouroboros", g)
    assert m.mass > 0
    assert m.velocity > 0
    assert m.inertia == pytest.approx(m.mass / m.velocity, rel=1e-3)


def test_a_truth_with_no_return_path_is_held_at_the_source():
    g = load_glossary(GLOSSARY)
    m = mechanics("ankh", g)            # no usage remembers the ankh
    assert m.state == "held-no-return"
    assert m.carriers == 0
    assert m.inertia is None           # nothing moved, so nothing to resist
    assert m.half_life is None
    assert m.mass > 0                  # but the sign still holds its weighted field


def test_divine_order_crosses_at_the_threshold():
    g = load_glossary(GLOSSARY)
    m = mechanics("divine-order", g)
    assert m.state == "crystallized"
    assert m.ghost_lag == 0            # the Theogony was written *at* the threshold (-700)
    assert "the crossing" in m.lag_phrase


def test_signal_and_noise_partition_the_outcome():
    g = load_glossary(GLOSSARY)
    for cid in ("ouroboros", "labrys", "divine-order"):
        m = mechanics(cid, g)
        assert m.signal + m.noise == pytest.approx(1.0, abs=1e-6)


def test_a_dissipating_memory_has_a_finite_half_life():
    # ouroboros net-decayed from the source (0.85 < 1.0), so a half-life is defined.
    g = load_glossary(GLOSSARY)
    m = mechanics("ouroboros", g)
    assert m.half_life is not None and m.half_life > 0


def test_a_pump_concept_has_no_weighted_field_to_weigh():
    # revolution/democracy segment meaning into senses, not a field - honestly reported.
    g = load_glossary(GLOSSARY)
    m = mechanics("revolution", g)
    assert m.state == "no-field"
    assert m.mass == 0.0
    assert "segments meaning into senses" in m.state_gloss


def test_density_weighs_a_remembrances_carried_field():
    # A remembrance (a pump-mode usage on the return path) still carries a weighted
    # field; its mass is measurable - the earlier guard wrongly refused it.
    g = load_glossary(GLOSSARY)
    d = bit_density(g.usage("theogony").field)
    assert d.held == 4 and d.bits > 1.5


def test_the_web_reads_every_breath_truth_by_mass():
    g = load_glossary(GLOSSARY)
    web = mechanics_web(g)
    assert [m.concept for m in web.items] == ["labrys", "divine-order", "ouroboros", "ankh"]
    # uniformly massive; the outcome is what differs, not the mass
    assert all(m.mass >= 1.5 for m in web.items)
    states = {m.concept: m.state for m in web.items}
    assert states["labrys"] == "retained-overwritten"
    assert states["ankh"] == "held-no-return"


def test_the_pump_web_holds_no_field_mechanics():
    g = load_glossary(GLOSSARY)
    web = mechanics_web(g, regime="pump")
    assert web.items == []
    assert "no weighted-field web" in web.summary
