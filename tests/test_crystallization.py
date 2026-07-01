"""The crystallisation frame: order precipitated from the fluid (the quartet)."""

from __future__ import annotations

from interpretation.crystallization import (
    FLUCTUATION,
    KEYSTONE,
    LATTICE,
    NUCLEUS,
    PRECIPITATION,
    SUPERSATURATION,
    crystallise,
    frame,
    memberships,
    quadrant,
    read_state,
    recohere,
)


def test_the_quartet_is_the_tensor_of_the_two_axes():
    assert quadrant("field", "fluid").name == SUPERSATURATION
    assert quadrant("field", "fixed").name == LATTICE
    assert quadrant("seed", "fluid").name == FLUCTUATION
    assert quadrant("seed", "fixed").name == NUCLEUS


def test_the_keystone_is_the_lattice():
    # the-crystal is the lattice corner: order spanning the whole field
    assert quadrant("field", "fixed").coherence == 1.0
    assert KEYSTONE == "the-crystal"


def test_the_quartetual_equations_partition_unity():
    # every state's four quadrant weights sum to exactly 1
    for sigma in (0.0, 0.25, 0.5, 0.75, 1.0):
        for phi in (0.0, 0.3, 0.5, 1.0):
            w = memberships(sigma, phi)
            assert abs(sum(w.values()) - 1.0) < 1e-12
    # the centre is an equal blend of all four corners
    assert memberships(0.5, 0.5) == {
        SUPERSATURATION: 0.25, LATTICE: 0.25, FLUCTUATION: 0.25, NUCLEUS: 0.25,
    }


def test_each_corner_is_pure_membership():
    assert read_state(1.0, 1.0).weights[LATTICE] == 1.0          # the crystal
    assert read_state(0.0, 0.0).weights[FLUCTUATION] == 1.0      # local + fluid
    assert read_state(0.0, 1.0).weights[NUCLEUS] == 1.0          # holds, but local
    assert read_state(1.0, 0.0).weights[SUPERSATURATION] == 1.0  # primed, uncommitted


def test_coherence_is_the_lattice_weight():
    # a nucleus has committed order but no extent — coherence (spanning order) is still 0
    assert read_state(0.0, 1.0).coherence == 0.0
    # only order that spans the field counts as the crystal
    assert read_state(1.0, 1.0).coherence == 1.0
    assert read_state(0.5, 0.8).coherence == 0.4


def test_precipitation_path_is_crystallising():
    c = crystallise(PRECIPITATION)
    assert c.direction == "crystallising"
    assert c.net == 1.0
    assert c.is_precipitation


def test_the_reverse_path_is_decoherence():
    c = crystallise(list(reversed(PRECIPITATION)))
    assert c.direction == "decohering"
    assert c.net == -1.0
    assert not c.is_precipitation


def test_a_reef_bleaching_decoheres():
    # lattice (the reef) fragmenting back toward fluctuation/supersaturation: coherence falls
    c = crystallise([LATTICE, NUCLEUS, FLUCTUATION])
    assert c.direction == "decohering"
    assert c.coherences == [1.0, 0.0, 0.0]


def test_states_accept_continuous_coordinates():
    c = crystallise([(1.0, 0.0), (0.2, 0.2), (0.1, 0.9), (1.0, 1.0)])
    assert c.direction == "crystallising"
    assert c.coherences[0] == 0.0
    assert c.coherences[-1] == 1.0


def test_the_reef_rebuilds_as_recoherence():
    # the whole arc: first reef -> bleaching -> dormant skeleton -> spark -> new reef
    r = recohere([LATTICE, FLUCTUATION, FLUCTUATION, NUCLEUS, (0.3, 1.0), LATTICE])
    assert r.is_recoherence
    assert r.crest == 1.0          # the first reef
    assert r.trough == 0.0         # the bleached skeleton
    assert r.recrest == 1.0        # the rebuilding reef
    assert r.renucleation == 3     # the spark: order re-commits at the nucleus


def test_recoherence_is_not_the_same_as_a_first_crystallisation():
    # a single climb from fluid never fell to a skeleton — it is not re-coherence
    r = recohere(PRECIPITATION)
    assert not r.decohered
    assert not r.is_recoherence


def test_a_lost_skeleton_is_not_recoherence():
    # if the substrate did not persist, a second climb is a fresh crystallisation
    r = recohere([LATTICE, FLUCTUATION, NUCLEUS, LATTICE], same_skeleton=False)
    assert r.decohered and r.re_cohered
    assert not r.is_recoherence


def test_the_spark_precedes_the_visible_climb():
    # at re-nucleation the coherence scalar is still ~0 — the turn happens before the climb
    r = recohere([LATTICE, FLUCTUATION, NUCLEUS, (0.5, 1.0), LATTICE])
    spark = r.renucleation
    assert spark is not None
    assert r.stops[spark].coherence <= 0.5
    assert r.stops[spark].order > 0.5


def test_frame_renders_the_keystone():
    s = frame().summary
    assert KEYSTONE in s
    assert "order precipitated from the fluid" in s
    assert "sigma * phi" in s
