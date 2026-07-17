"""The meaning tree: causal meaning relationships read off the record.

The map's layers already store connections -- this module reads them into one
graph and traces **trees** through it. Six edge kinds, every one derived from
a recorded structure (the graph is computed against the record, never asserted
beside it):

  * **keystone** -- a keystone disperses into its members (quartets)
  * **kin**      -- members crystallised in the same lattice (kinship as
                    co-crystallisation)
  * **pole**     -- a member and the axis poles of its grid cell (position)
  * **polarity** -- the antonym pairs: every quartet axis, and the root pairs
                    of the 2 layer (the cut)
  * **thread**   -- consecutive words of a signal thread (the walked path)
  * **synonym**  -- the nearness links of the synonym web (each carrying its
                    differentia: nearness recorded, identity never claimed)

**Nodes of importance**: highly interlocked meaning. Importance is measured,
never asserted -- *interlock* is a node's connection count (degree), *depth*
is the kept-attention tokens gathered around it (the thread layer's length
measure). Words that live in several lattices (knowledge, sensation,
recognition, understanding, integrity) interlock most: the map's own hubs.

**On "causal"**: these edges record derivation IN THE MAP -- dispersal,
kinship, position, cut, walk: the causality of meaning-structure, not worldly
causation. A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

from .polarity import Polarities
from .quartet import Quartets
from .synonym import Synonyms
from .thread import Threads, corpus_texts, token_count, _present, _tokens

EDGE_KINDS = ("keystone", "kin", "pole", "polarity", "thread", "synonym")


@dataclass(frozen=True)
class Edge:
    """One recorded connection between two words, with its kind and source."""

    a: str
    b: str
    kind: str
    source: str     # the lattice / thread / pair the edge was read from

    def other(self, word: str) -> str:
        return self.b if word == self.a else self.a


@dataclass
class MeaningGraph:
    """The map's words as one graph; every edge read from a recorded layer."""

    adjacency: dict[str, list[Edge]] = field(default_factory=dict)

    @property
    def nodes(self) -> list[str]:
        return sorted(self.adjacency)

    def edges_of(self, word: str) -> list[Edge]:
        w = word.lower().strip()
        if w not in self.adjacency:
            raise KeyError(f"unknown word {w!r}: it appears in no recorded lattice, "
                           f"thread, or pair -- the tree reads the record, it does not guess")
        return self.adjacency[w]

    def degree(self, word: str) -> int:
        return len(self.edges_of(word))

    def hubs(self, limit: int = 15, quartets: Quartets | None = None) -> list[dict]:
        """Nodes of importance: ranked by interlock (connections), then depth
        (kept-attention tokens over the lattice readings), then name."""
        depth: dict[str, int] = {}
        if quartets is not None:
            texts = corpus_texts(quartets)
            docs = [_tokens(t) for t in texts]
            counts = [token_count(t) for t in texts]
            for w in self.adjacency:
                depth[w] = sum(c for d, c in zip(docs, counts) if _present(w, d))
        ranked = sorted(
            self.adjacency,
            key=lambda w: (-len(self.adjacency[w]), -depth.get(w, 0), w),
        )
        out = []
        for w in ranked[:limit]:
            sources = sorted({e.source for e in self.adjacency[w]})
            out.append({"word": w, "interlock": len(self.adjacency[w]),
                        "depth_tokens": depth.get(w, 0), "sources": sources})
        return out

    def tree(self, root: str, max_depth: int = 3) -> str:
        """Trace the meaning tree from a root: breadth-first over the record,
        each word placed once, its edge kind and source shown at the branch."""
        r = root.lower().strip()
        self.edges_of(r)   # surfaces KeyError for an unrecorded root
        lines = [f"the tree of {r!r} — causal meaning relationships read off the record"]
        seen = {r}
        frontier: list[tuple[str, int, str]] = [(r, 0, "")]
        while frontier:
            word, depth, label = frontier.pop(0)
            indent = "  " * depth
            lines.append(f"{indent}{label}{word}")
            if depth >= max_depth:
                continue
            children = []
            for e in sorted(self.adjacency[word], key=lambda e: (e.kind, e.other(word))):
                o = e.other(word)
                if o not in seen:
                    seen.add(o)
                    children.append((o, depth + 1, f"[{e.kind}: {e.source}] "))
            frontier.extend(children)
        lines.append(f"  ({len(seen)} word(s) reached; importance is interlock x depth, "
                     f"both measured -- descriptive, never a gate)")
        return "\n".join(lines)


def _norm(word: str) -> str:
    return word.lower().strip()


def build_graph(quartets: Quartets, threads: Threads,
                polarities: Polarities | None = None,
                synonyms: "Synonyms | None" = None) -> MeaningGraph:
    """Read the graph off the record: lattices, threads, the 2 layer, and the
    synonym web."""
    edges: dict[tuple[str, str, str], Edge] = {}

    def add(a: str, b: str, kind: str, source: str) -> None:
        a, b = _norm(a), _norm(b)
        if a == b:
            return
        key = (min(a, b), max(a, b), kind)
        if key not in edges:
            edges[key] = Edge(a=key[0], b=key[1], kind=kind, source=source)

    for q in quartets.quartets:
        for m in q.members:
            add(q.keystone, m, "keystone", q.id)
        for m1, m2 in combinations(q.members, 2):
            add(m1, m2, "kin", q.id)
        for cell_key, member in q.grid.items():
            row_pole, _, col_pole = cell_key.partition("/")
            add(member, row_pole, "pole", q.id)
            add(member, col_pole, "pole", q.id)
        add(q.row_poles[0], q.row_poles[1], "polarity", f"{q.id}:{q.row_axis}")
        add(q.col_poles[0], q.col_poles[1], "polarity", f"{q.id}:{q.col_axis}")

    for t in threads.threads:
        words = t.words
        for a, b in zip(words, words[1:]):
            add(a, b, "thread", t.id)

    if polarities is not None:
        for p in polarities.pairs:
            add(p.positive, p.negative, "polarity", p.id)

    if synonyms is not None:
        for l in synonyms.links:
            add(l.a, l.b, "synonym", l.id)

    graph = MeaningGraph()
    for e in edges.values():
        graph.adjacency.setdefault(e.a, []).append(e)
        graph.adjacency.setdefault(e.b, []).append(e)
    return graph
