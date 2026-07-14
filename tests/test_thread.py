"""The signal threads: kept paths, weighed in measured bits (never asserted)."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.quartet import load_quartets
from interpretation.thread import (
    corpus_documents,
    entropy,
    load_threads,
    mutual_information,
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
    assert ids == {"bond-thread", "gladness-thread", "signal-thread"}
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
    assert w.documents == len(docs) == 18
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
