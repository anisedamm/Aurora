"""The mechanics of meaning: bit-density (mass), inertia, and ghost-lag crystallization."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import from_mapping, load_glossary
from interpretation.inertia import bit_density, mass_profile, mechanics, mechanics_web

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


def test_momentum_is_mass_times_velocity():
    g = load_glossary(GLOSSARY)
    m = mechanics("ouroboros", g)
    assert m.momentum == pytest.approx(m.mass * m.velocity, rel=1e-3)


def test_momentum_and_inertia_are_the_two_faces_of_motion():
    # The ouroboros was sent on a journey (high momentum); the divine order, as massive,
    # barely moved (high inertia, low momentum) - the two faces of mass-and-velocity.
    g = load_glossary(GLOSSARY)
    journeyed = mechanics("ouroboros", g)
    held = mechanics("divine-order", g)
    assert journeyed.mass == pytest.approx(held.mass, abs=0.1)   # ~equally massive
    assert journeyed.momentum > held.momentum                    # but the ouroboros moved
    assert journeyed.inertia < held.inertia                      # the divine order resisted


def test_a_truth_that_never_moved_has_no_momentum():
    g = load_glossary(GLOSSARY)
    m = mechanics("ankh", g)        # no rememberings - nothing in motion
    assert m.momentum is None and m.inertia is None


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


# --- the mass profile: overwritten (mass holds) vs thinned (mass falls) -------

def test_overwriting_holds_the_mass_while_the_signal_falls():
    # The labrys-emblem hop stays massive but stops speaking the source truth.
    g = load_glossary(GLOSSARY)
    prof = mass_profile("labrys", g)
    emblem = next(s for s in prof.stops if s.by_id == "labrys-emblem")
    assert emblem.mass > 1.7                  # still dense - the sign keeps saying a great deal
    assert emblem.to_origin < 0.5             # but no longer about the source: overwritten
    assert prof.low_mass > 1.7                # mass never really thinned across the chain


def test_thinning_drops_the_mass_with_the_signal():
    # The ouroboros worn to heraldic ornament loses informational weight *and* signal.
    g = load_glossary(GLOSSARY)
    prof = mass_profile("ouroboros", g)
    medieval = next(s for s in prof.stops if s.by_id == "ouroboros-medieval")
    assert medieval.mass < 1.7                # thinned - fewer values, an ornament
    assert medieval.to_origin < 0.7
    assert prof.low_mass < prof.origin_mass   # the mass genuinely dipped (unlike the labrys)


def test_the_profile_opens_at_the_origin():
    g = load_glossary(GLOSSARY)
    prof = mass_profile("ouroboros", g)
    assert prof.stops[0].is_origin and prof.stops[0].to_origin == 1.0
    assert [s.is_origin for s in prof.carriers] == [False, False, False]


def test_a_truth_with_no_return_path_has_an_empty_profile():
    g = load_glossary(GLOSSARY)
    prof = mass_profile("ankh", g)
    assert prof.carriers == []
    assert "no rememberings on record" in prof.summary


# --- dissipation as a proportional phase-out from peak (not an absolute cutoff) ---

def test_dissipation_is_proportional_to_the_peak():
    # The ouroboros dipped deeply (to the heraldic ornament) then recovered: the *deepest*
    # phase-out is large, the *final* phase-out small, both read relative to its own peak.
    g = load_glossary(GLOSSARY)
    m = mechanics("ouroboros", g)
    assert m.peak_at_origin                       # its fullest moment was the source
    assert 0.5 < m.deepest_dissipation < 0.6      # phased out ~55% at the medieval nadir
    assert m.dissipation < 0.2                    # but recovered to ~14% off its peak
    assert m.deepest_dissipation > m.dissipation  # it dissipated, then re-cohered
    assert m.state == "crystallized"              # so the *terminal* state still holds


def test_every_memory_carries_a_dissipation_in_the_unit_interval():
    g = load_glossary(GLOSSARY)
    for cid in ("ouroboros", "labrys", "divine-order"):
        m = mechanics(cid, g)
        assert 0.0 <= m.dissipation <= 1.0
        assert 0.0 <= m.deepest_dissipation <= 1.0


def _built(retained, carriers):
    """A one-concept breath glossary: a source field plus a list of remembering usages."""
    src = {"id": "src", "regime": "breath", "mode": "conceptual", "artifact": "a relief",
           "citation": "a source", "year": -2000, "field": retained}
    return from_mapping({"concepts": [{
        "id": "c", "name": "C", "regime": "breath", "threshold": -500, "year": -2000,
        "retained": retained, "senses": [], "usages": [src] + carriers,
    }]})


def _carrier(cid, year, remembers, field):
    return {"id": cid, "regime": "pump", "mode": "phonetic", "quotation": "q",
            "citation": "a record", "year": year, "remembers": remembers, "field": field}


def test_a_genuine_phase_out_reaches_the_dissipated_state():
    # A breath truth carried once into a late record that keeps almost none of it - a
    # genuine terminal dissipation, which the seeded corpus (all recovering or kept) lacks.
    g = _built({"a": 0.4, "b": 0.3, "c": 0.3},
               [_carrier("late", 500, "c", {"x": 0.7, "a": 0.15, "b": 0.15})])
    m = mechanics("c", g)
    assert m.state == "dissipated"
    assert m.dissipation >= 0.5            # fell past half its own peak significance
    assert "faded, not kept" in m.state_gloss
    assert m.direction == "reverted"


# --- completing the cycle: phase in, suspended stall ---------------------------

def test_seeded_breath_truths_are_born_full():
    # A breath truth's peak is the source itself: it never phases in - the breath signature.
    g = load_glossary(GLOSSARY)
    for cid in ("ouroboros", "labrys", "divine-order"):
        m = mechanics(cid, g)
        assert m.peak_at_origin
        assert m.phase_in == 0.0
        assert m.cycle.startswith("born full")


def test_a_meaning_can_phase_in_to_a_later_peak():
    # A sparse source that grows into a richer, on-source remembering peaks *after* origin.
    g = _built({"a": 0.5, "b": 0.5}, [
        _carrier("c1", 0, "c", {"a": 0.35, "b": 0.35, "c": 0.30}),
        _carrier("c2", 600, "c1", {"a": 0.2, "x": 0.8}),
    ])
    m = mechanics("c", g)
    assert not m.peak_at_origin
    assert m.phase_in > 0.05
    assert m.cycle.startswith("phased in")


def test_a_meaning_can_suspend_in_a_stall():
    # Falls to a middling level, then holds flat to the end: suspended, its outcome open.
    field = {"a": 0.3, "b": 0.2, "x": 0.25, "y": 0.25}
    g = _built({"a": 0.4, "b": 0.3, "c": 0.3}, [
        _carrier("s1", 0, "c", field),
        _carrier("s2", 700, "s1", dict(field)),
    ])
    m = mechanics("c", g)
    assert m.state == "suspended"
    assert m.stall_span == 700
    assert "stalled" in m.cycle
    assert 0.15 <= m.dissipation < 0.5
    assert "outcome held open" in m.state_gloss
