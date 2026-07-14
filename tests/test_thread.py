"""The signal threads: kept paths, weighed in measured bits (never asserted)."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.quartet import load_quartets
from interpretation.thread import (
    corpus_documents,
    corpus_texts,
    entropy,
    load_threads,
    mutual_information,
    token_count,
)

ROOT = Path(__file__).resolve().parents[1]
THREADS = ROOT / "threads.json"
QUARTETS = ROOT / "quartets.json"


def _threads():
    return load_threads(THREADS)


def _docs():
    return corpus_documents(load_quartets(QUARTETS))


def test_the_threads_load_with_their_forms():
    ts = _threads()
    ids = {t.id for t in ts.threads}
    assert ids == {"bond-thread", "gladness-thread", "signal-thread", "memory-thread",
                   "skill-thread", "warning-thread", "interpretation-thread",
                   "densification-thread", "alignment-thread", "loyalty-thread",
                   "justice-thread", "fairness-thread", "equity-thread", "honesty-thread",
                   "balance-thread", "harmony-thread", "union-thread"}
    bond = ts.by_id("bond-thread")
    assert bond.form == "love = care + kindness + trust + faith"
    assert bond.words == ["love", "care", "kindness", "trust", "faith"]
    assert bond.quartet == "bond"
    # every thread carries its ground: etymology, spiral, bridge, path
    for t in ts.threads:
        assert t.etymology and t.spiral and t.bridge and t.path_to_centre


def test_the_weights_are_measured_bits_not_constants():
    # H is a binary entropy (0..1 bits per word); I is non-negative and bounded
    # by min(H(X), H(Y)); no imported constants anywhere
    docs = _docs()
    ts = _threads()
    w = ts.by_id("signal-thread").weigh(docs)
    assert w.documents == len(docs) == 32
    for word, bits in w.entropy_bits.items():
        assert 0.0 <= bits <= 1.0
        assert 0 <= w.document_frequency[word] <= w.documents
    for a, b, mi in w.links:
        assert mi >= 0.0
        assert mi <= min(w.entropy_bits[a], w.entropy_bits[b]) + 1e-9
    assert w.total_entropy == pytest.approx(sum(w.entropy_bits.values()))
    assert w.binding == pytest.approx(sum(mi for _, _, mi in w.links))


def test_love_is_the_heaviest_coordinate_in_the_map():
    # love appears across the map (bond, its dimensions, the readings that cite
    # it) -- its document frequency dwarfs a word that lives in one lattice
    docs = _docs()
    _, df_love = entropy("love", docs)
    _, df_supersat = entropy("supersaturation", docs)
    assert df_love > df_supersat >= 1


def test_the_thread_binds_beyond_chance():
    # trust and faith co-crystallise (bond's doublet): their MI over the map's
    # documents is strictly positive -- the pair clusters beyond chance
    docs = _docs()
    assert mutual_information("trust", "faith", docs) > 0.0
    # and MI is symmetric, as it must be
    assert mutual_information("hope", "love", docs) == pytest.approx(
        mutual_information("love", "hope", docs))


def test_length_measures_kept_attention_in_tokens():
    # the token measure: grounded (unit, derivation, provenance), unlike the
    # refused constant -- the path as written, each word's depth (tokens
    # gathered around it), and the path's reach (union of lattices touched)
    qs = load_quartets(QUARTETS)
    thread = _threads().by_id("signal-thread")
    length = thread.measure(qs)
    assert length.path_tokens == token_count(thread.record_text) > 0
    for w in thread.words:
        assert length.depth_tokens[w] > 0          # every word gathers record
        assert length.depth_documents[w] >= 1
        # reach is a union, so no single word's depth can exceed it
        assert length.depth_tokens[w] <= length.reach_tokens
    assert length.documents_touched <= len(corpus_texts(qs))
    s = length.summary
    assert "kept attention" in s
    assert "padding is its counterfeit" in s        # the Goodhart, named


def test_the_longer_path_weighs_more_where_more_was_kept():
    # love (a keystone with dimensions, cited across the map) has gathered
    # more tokens than a member that lives in a single lattice
    qs = load_quartets(QUARTETS)
    bond = _threads().by_id("bond-thread").measure(qs)
    assert bond.depth_tokens["love"] > 0
    assert bond.depth_documents["love"] > 1
    glad = _threads().by_id("gladness-thread").measure(qs)
    assert bond.depth_tokens["love"] >= glad.depth_tokens["wish"]


def test_the_token_measure_is_recorded_in_the_bound():
    ts = _threads()
    assert "the_token_measure" in ts.bound
    assert "kept attention" in ts.bound["the_token_measure"].lower()
    assert "goodhart" in ts.bound["the_token_measure"].lower()


def test_the_refused_constant_is_recorded_in_the_bound():
    # the discipline: an ungrounded scalar (18*(3.47*10^27)) was declined and
    # the refusal recorded, so the next reader knows it was guarded
    ts = _threads()
    assert "the_refused_constant" in ts.bound
    assert "declined" in ts.bound["the_refused_constant"].lower()
    assert "measured bits" in ts.bound["the_refused_constant"].lower() \
        or "measured" in ts.bound["the_refused_constant"].lower()


def test_the_summary_carries_the_measures_and_the_bound():
    ts = _threads()
    qs = load_quartets(QUARTETS)
    s = ts.summary(qs)
    assert "bond-thread" in s and "signal-thread" in s
    assert "H(" in s and "I(" in s
    assert "no imported constants" in s
    assert "never a gate" in s


def test_unknown_thread_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _threads().by_id("nope")
