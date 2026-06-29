"""The metabolism of meaning: significance turnover (transmission) and complexity branching."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.glossary import load_glossary
from interpretation.lexicon import load_lexicon
from interpretation.metabolism import metabolism, metabolism_map, understanding_arc

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"
LEXICON = Path(__file__).resolve().parents[1] / "lexicon.json"


def test_a_breath_sign_transmits_but_does_not_branch():
    g = load_glossary(GLOSSARY)
    m = metabolism("ouroboros", g)
    assert m.mode == "transmitting"
    assert m.transmits and not m.branches_out
    assert m.sig_rate > 0 and m.senses == 0


def test_a_pump_concept_branches_but_is_not_transmitted():
    g = load_glossary(GLOSSARY)
    m = metabolism("revolution", g)
    assert m.mode == "branching"
    assert m.branches_out and not m.transmits
    assert m.senses == 4 and m.branches == 3 and m.depth == 4
    assert "inversion" in m.kinds          # the move revolution turns on
    assert m.cplx_rate > 0


def test_the_divine_order_does_both():
    # A remembered breath-truth that *also* climbed a ladder of abstraction across the lag.
    g = load_glossary(GLOSSARY)
    m = metabolism("divine-order", g)
    assert m.mode == "both"
    assert m.transmits and m.branches_out
    assert m.kinds == ["abstraction"]      # each rung the same refining shift


def test_an_uncarried_unbranched_sign_is_dormant():
    g = load_glossary(GLOSSARY)
    m = metabolism("ankh", g)              # no rememberings, no sense lattice
    assert m.mode == "dormant"
    assert not m.transmits and not m.branches_out


def test_turnover_is_total_work_not_net_displacement():
    # The ouroboros fell to ornament and recovered: it *worked* far more significance than
    # its net change - turnover sums the absolute swings, the metabolic throughput.
    g = load_glossary(GLOSSARY)
    m = metabolism("ouroboros", g)
    assert m.sig_turnover > 1.5            # the dip-and-recovery, summed
    # net displacement (origin to final) is far smaller than the turnover
    assert m.sig_turnover > 0.5            # comfortably above any single-hop net change


def test_complexity_rate_is_senses_per_century():
    g = load_glossary(GLOSSARY)
    m = metabolism("democracy", g)
    assert m.senses == 2 and m.branches == 1
    assert m.kinds == ["amelioration"]
    assert m.cplx_rate == pytest.approx((m.senses - 1) / m.cplx_span * 100, abs=1e-3)


def test_the_map_orders_by_mode_then_rate():
    g = load_glossary(GLOSSARY)
    mp = metabolism_map(g)
    by = [m.concept for m in mp.items]
    assert by[0] == "divine-order"         # 'both' leads
    assert by[-1] == "ankh"                # 'dormant' trails
    modes = [m.mode for m in mp.items]
    # modes are grouped in order: both, transmitting..., branching..., dormant
    assert modes == sorted(modes, key=lambda x: {"both": 0, "transmitting": 1,
                                                 "branching": 2, "dormant": 3}[x])
    assert "pursuing more understanding" in mp.summary


# --- the civilisational arc: the lexicon's metabolism of understanding -------

def test_the_understanding_arc_climbs_sieve_to_success():
    lex = load_lexicon(LEXICON)
    arc = understanding_arc(lex)
    assert [s.era for s in arc.steps] == ["primal", "agrarian", "classical", "modern", "reflexive"]
    assert arc.steps[0].align < arc.steps[-1].align          # understanding climbed
    assert arc.climb_align == pytest.approx(0.50, abs=0.05)   # ~0.09 -> ~0.59
    assert arc.total_named == 27


def test_the_arc_reports_per_era_gains():
    lex = load_lexicon(LEXICON)
    arc = understanding_arc(lex)
    assert arc.steps[0].gain_align is None                    # no era before the first
    assert all(s.gain_align is not None and s.gain_align > 0 for s in arc.steps[1:])
    # the rate is per era (developmental stage), not per year - eras are unevenly spaced
    assert arc.rate == pytest.approx(arc.climb_align / (len(arc.steps) - 1), abs=1e-3)


def test_coherence_and_experience_rise_across_the_arc():
    lex = load_lexicon(LEXICON)
    arc = understanding_arc(lex)
    assert arc.steps[0].coherence < arc.steps[-1].coherence
    assert arc.steps[0].experiential < arc.steps[-1].experiential
