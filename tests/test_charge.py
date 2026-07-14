"""The charge: the load a concept carries, measured over the record."""

from __future__ import annotations

from pathlib import Path

from interpretation.charge import (
    charge_of,
    charge_report,
    rank_charges,
    thread_condensations,
)
from interpretation.glossary import load_glossary
from interpretation.polarity import load_polarities
from interpretation.quartet import load_quartets
from interpretation.thread import load_threads
from interpretation.tree import build_graph

ROOT = Path(__file__).resolve().parents[1]


def _fixtures():
    qs = load_quartets(ROOT / "quartets.json")
    ts = load_threads(ROOT / "threads.json")
    po = load_polarities(ROOT / "polarities.json")
    g = load_glossary(ROOT / "glossary.json")
    return build_graph(qs, ts, po), qs, ts, g


def test_charge_is_the_product_of_interlock_and_depth():
    graph, qs, _, g = _fixtures()
    c = charge_of("integrity", graph, qs, g)
    assert c.interlock > 0 and c.depth_tokens > 0
    assert c.charge == c.interlock * c.depth_tokens
    assert "authored index" in c.summary          # defined like signal, not discovered


def test_endurance_is_reported_only_where_years_are_attested():
    graph, qs, _, g = _fixtures()
    # revolution is a glossary concept with dated witnesses: it holds real time
    rev = charge_of("revolution", graph, qs, g)
    assert rev.years_held is not None and rev.years_held >= 200
    assert rev.attestations >= 2
    # a gridded word with no dated witness gets no endurance number
    ori = charge_of("orientation", graph, qs, g)
    assert ori.years_held is None
    assert "surfaced, not guessed" in ori.summary


def test_an_ungridded_word_reports_zero_interlock_not_an_error():
    graph, qs, _, g = _fixtures()
    rev = charge_of("revolution", graph, qs, g)
    assert rev.interlock == 0                     # attested in the glossary, not yet gridded
    assert "not yet gridded" in rev.summary


def test_the_most_charged_words_are_the_load_bearers():
    graph, qs, _, g = _fixtures()
    ranked = rank_charges(graph, qs, g, limit=30)
    charges = [c.charge for c in ranked]
    assert charges == sorted(charges, reverse=True)
    words = [c.word for c in ranked]
    # the map's measured hubs carry the load (the exact order shifts as the
    # map grows -- a living record -- but the load-bearers stay in the van)
    assert "integrity" in words and "whole" in words
    assert all(c.charge == c.interlock * c.depth_tokens for c in ranked)


def test_every_thread_is_condensed_beyond_its_written_path():
    _, qs, ts, _ = _fixtures()
    tcs = thread_condensations(ts, qs)
    assert len(tcs) == len(ts.threads)
    for tc in tcs:
        assert tc.ratio > 1.0                     # reach exceeds the path as written
        assert tc.binding_bits >= 0.0
        assert "not IIT's phi" in tc.summary      # the boundary held by name


def test_the_report_carries_the_bounds():
    graph, qs, ts, g = _fixtures()
    r = charge_report(graph, qs, ts, g)
    assert "charge is cargo" in r                 # carricare: the load
    assert "mater" in r                           # matter is what is built from
    assert "not IIT's phi" in r
    assert "mattering-in-the-record" in r         # the boundary: the rest is held
    assert "never a gate" in r
