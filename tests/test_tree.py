"""The meaning tree: causal meaning relationships read off the record."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.polarity import load_polarities
from interpretation.quartet import load_quartets
from interpretation.synonym import load_synonyms
from interpretation.thread import load_threads
from interpretation.tree import EDGE_KINDS, build_graph

ROOT = Path(__file__).resolve().parents[1]


def _graph():
    return build_graph(
        load_quartets(ROOT / "quartets.json"),
        load_threads(ROOT / "threads.json"),
        load_polarities(ROOT / "polarities.json"),
        load_synonyms(ROOT / "synonyms.json"),
    )


def test_the_graph_is_read_off_the_record():
    g = _graph()
    # every edge kind is one of the six derived from recorded structures
    for edges in g.adjacency.values():
        for e in edges:
            assert e.kind in EDGE_KINDS
            assert e.source            # every edge names where it was read from
    # the graph is deterministic: two builds agree exactly
    g2 = _graph()
    assert {w: sorted((e.a, e.b, e.kind) for e in es) for w, es in g.adjacency.items()} \
        == {w: sorted((e.a, e.b, e.kind) for e in es) for w, es in g2.adjacency.items()}


def test_the_purpose_tree_traces_its_lattice():
    # the user's example: purpose reaches its kin (self, home, world), its
    # keystone (being-in-the-world), and its grid poles (telos, total)
    g = _graph()
    t = g.tree("purpose", max_depth=2)
    for word in ("self", "home", "world", "being-in-the-world", "telos", "total"):
        assert word in t
    assert "never a gate" in t


def test_interlocked_words_are_the_hubs():
    # words living in several lattices interlock most: knowledge (intelligence
    # + skill), sensation (animate + perception), understanding (process +
    # interpretation) all out-connect a single-lattice member like purpose
    g = _graph()
    for shared in ("knowledge", "sensation", "understanding"):
        assert g.degree(shared) > g.degree("purpose")
    # the window widens as the map grows (the verb lattices' members now
    # interlock heavily) -- presence, not position: a living record
    hubs = g.hubs(limit=35, quartets=load_quartets(ROOT / "quartets.json"))
    words = [h["word"] for h in hubs]
    assert "knowledge" in words
    # importance is measured: every hub carries interlock, depth, and sources
    for h in hubs:
        assert h["interlock"] >= 1 and h["depth_tokens"] >= 0 and h["sources"]


def test_the_synonym_web_interconnects_the_graph():
    # the sixth edge kind: nearness links, each read from the synonym layer
    g = _graph()
    assert "synonym" in EDGE_KINDS
    trust_syn = [e for e in g.edges_of("trust") if e.kind == "synonym"]
    assert any(e.other("trust") == "faith" for e in trust_syn)
    assert any(e.source == "trust-faith" for e in trust_syn)
    # the web joins lattices the other kinds never touched directly:
    # worth ~ value crosses from the worth lattice into the ethos square
    worth_syn = [e for e in g.edges_of("worth") if e.kind == "synonym"]
    assert any(e.other("worth") == "value" for e in worth_syn)
    # nearness and opposition both walkable: the thesaurus's two axes
    kinds_at_peace = {e.kind for e in g.edges_of("peace")}
    assert "synonym" in kinds_at_peace


def test_the_edges_carry_all_five_kinds():
    g = _graph()
    kinds = {e.kind for edges in g.adjacency.values() for e in edges}
    assert kinds == set(EDGE_KINDS)
    # polarity includes the root pairs of the 2 layer (yes <-> no)
    assert any(e.kind == "polarity" for e in g.edges_of("yes"))
    # thread edges walk the recorded paths (trust -> faith in signal-thread)
    assert any(e.kind == "thread" and e.other("trust") == "faith"
               for e in g.edges_of("trust"))
    # keystone edges disperse (love -> care) and pole edges place (purpose -> telos)
    assert any(e.kind == "keystone" and e.other("love") == "care"
               for e in g.edges_of("love"))
    assert any(e.kind == "pole" and e.other("purpose") == "telos"
               for e in g.edges_of("purpose"))


def test_an_unrecorded_word_is_surfaced_not_guessed():
    g = _graph()
    with pytest.raises(KeyError, match="reads the record"):
        g.tree("flibbertigibbet")
    with pytest.raises(KeyError):
        g.degree("nope")
