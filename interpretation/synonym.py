"""The synonym web: the nearness layer -- everything interconnected, honestly.

The polarity layer recorded the antonym web (the 2, the first cut); this module
records its complement: the SYNONYM web, the thesaurus's other axis. Together
they are the two relations every lexicon runs on -- nearness and opposition --
and the meaning tree now carries both.

Three grounded laws carry the layer:

  * **the first law of synonymy** -- NO TRUE SYNONYMS SURVIVE: total synonymy
    is unstable (attested across lexical semantics) -- a language differentiates
    a perfect pair or drops one member. The record's doublets are the law's
    fossils (morals/ethics, trust/faith: pairs pushed apart to fill different
    cells). The layer therefore records sameness by recording difference:
    EVERY LINK MUST CARRY ITS DIFFERENTIA -- what keeps the pair apart -- and
    the loader refuses a link without one.
  * **the register stratification** -- English's synonym pairs are stratified
    by conquest (Germanic under French under Latin: kingly/royal/regal), and
    the strata are the regimes: the Germanic word is the breath register (the
    lived: keep, worth, gladness), the Romance word the pump register (the
    articulated: preserve, value, felicity). The breath<->pump axis runs
    through the lexicon itself.
  * **the non-transitivity** -- synonym chains DRIFT: big is near large, large
    is near spacious, big is not near spacious. The web carries NEARNESS, not
    identity; distance accumulates along every path, so a chain is a walk, not
    a proof. `chain` returns paths with this caveat attached.

The attested typology of nearness (VALID_KINDS):

  * **register** -- same referent, different stratum (worth/value, keep/preserve)
  * **near**     -- overlapping fields, distinct nuance (trust/faith, meaning/sense)
  * **scalar**   -- same scale, different intensity (gladness/joy)
  * **doublet**  -- one root arrived twice (royal/regal: both regalis, one
                    through French, one direct)
  * **calque**   -- the same construction built independently (forgive/pardon,
                    respect/regard, morals calquing ethics -- Cicero's own coin)

A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .quartet import Quartets
from .thread import corpus_texts, _present, _tokens

VALID_KINDS = ("register", "near", "scalar", "doublet", "calque")


@dataclass(frozen=True)
class Link:
    """One synonym link: two words, their kind of nearness, and -- by the first
    law -- the differentia that keeps them apart."""

    id: str
    a: str
    b: str
    kind: str           # one of VALID_KINDS (the attested typology of nearness)
    differentia: str    # what keeps the pair apart (required: no true synonyms)
    derivation: str     # the roots: where each word comes from
    aurora: str         # where the record embodies or found the pair

    def other(self, word: str) -> str:
        return self.b if word == self.a else self.a

    @property
    def summary(self) -> str:
        return (
            f"{self.id} — {self.a} ~ {self.b}  [{self.kind}]\n"
            f"  differentia: {self.differentia}\n"
            f"  derivation:  {self.derivation}\n"
            f"  in the record: {self.aurora}"
        )


@dataclass
class Synonyms:
    links: list[Link] = field(default_factory=list)
    bound: dict = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def by_id(self, lid: str) -> Link:
        for l in self.links:
            if l.id == lid:
                return l
        raise KeyError(f"unknown link {lid!r}; have {[l.id for l in self.links]}")

    def neighbors(self, word: str) -> list[Link]:
        w = word.lower().strip()
        out = [l for l in self.links if w in (l.a, l.b)]
        if not out:
            raise KeyError(f"unknown word {w!r}: it appears in no recorded synonym "
                           f"link -- the web reads the record, it does not guess")
        return out

    def chain(self, start: str, goal: str) -> list[str]:
        """Shortest walk through the web (BFS). A walk, not a proof: nearness is
        non-transitive -- distance accumulates with every step."""
        s, g = start.lower().strip(), goal.lower().strip()
        self.neighbors(s)
        self.neighbors(g)
        seen = {s}
        frontier: list[list[str]] = [[s]]
        while frontier:
            path = frontier.pop(0)
            if path[-1] == g:
                return path
            for l in self.links:
                if path[-1] in (l.a, l.b):
                    o = l.other(path[-1])
                    if o not in seen:
                        seen.add(o)
                        frontier.append(path + [o])
        raise KeyError(f"no walk from {s!r} to {g!r}: the web joins them nowhere "
                       f"-- absence recorded, not bridged")

    def web(self, quartets: Quartets) -> dict:
        """The web checked against the record: which links stand with both ends
        in the lattice corpus (live), and which reach beyond it (reported)."""
        docs = [_tokens(t) for t in corpus_texts(quartets)]

        def in_corpus(w: str) -> bool:
            return any(_present(w, d) for d in docs)

        live = [l for l in self.links if in_corpus(l.a) and in_corpus(l.b)]
        beyond = [l for l in self.links if l not in live]
        return {"live": live, "beyond": beyond,
                "words": sorted({w for l in self.links for w in (l.a, l.b)})}

    def summary(self, quartets: Quartets | None = None) -> str:
        rows = [self.title or "the synonym web", ""]
        for l in self.links:
            rows.append(l.summary)
            rows.append("")
        if quartets is not None:
            w = self.web(quartets)
            rows.append(f"  the web against the record: {len(w['live'])} link(s) live in the "
                        f"corpus, {len(w['beyond'])} reaching beyond it (reported, not hidden)")
        if "the_first_law" in self.bound:
            rows.append(f"  bound: {self.bound['the_first_law']}")
        if "the_non_transitivity" in self.bound:
            rows.append(f"  bound: {self.bound['the_non_transitivity']}")
        rows.append("  a reader, not a ruler: descriptive, never a gate.")
        return "\n".join(rows)


def load_synonyms(path) -> Synonyms:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    links = []
    for e in raw.get("links", []):
        kind = e.get("kind", "")
        if kind not in VALID_KINDS:
            raise ValueError(
                f"link {e.get('id')!r} has kind {kind!r}; the attested typology is "
                f"{VALID_KINDS} -- an unnamed kind of nearness is surfaced, not guessed"
            )
        if not e.get("differentia", "").strip():
            raise ValueError(
                f"link {e.get('id')!r} carries no differentia -- the first law of "
                f"synonymy: no true synonyms survive, so every link must record "
                f"what keeps the pair apart"
            )
        links.append(Link(
            id=e["id"], a=e["a"].lower().strip(), b=e["b"].lower().strip(), kind=kind,
            differentia=e["differentia"], derivation=e.get("derivation", ""),
            aurora=e.get("aurora", ""),
        ))
    return Synonyms(
        links=links,
        bound=raw.get("bound", {}),
        title=raw.get("title", ""),
        note=raw.get("note", ""),
    )
