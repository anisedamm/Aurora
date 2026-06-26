"""The weave: paired antonym couples as one relational web of meaning.

`condensation.py` reads a single term — its binary pole (compression) and the field
condensed upon it (condensation), and the connection between *two* terms. This module
lifts that to the **whole web**, the way `constellation.py` lifts a single breath sign
to the system-level web of a regime's shared values. It reads every antonym couple and
every shared-meaning edge at once and asks the three questions that only make sense of
the web entire:

  * **Which root antonyms are always paired, no matter how derived?** A couple is a
    **root** when *neither* pole carries a condensed field of its own — both are
    bit-like, irreducible distinctions (signal/noise, true/false, right/wrong). However
    much meaning is later condensed and compounded on top, a derived opposition bottoms
    out on these: they are the couples that stay coupled no matter how derived. The
    condensed couples (justice/injustice, self/other) are *refinements* — a root
    distinction with a field grown on it.

  * **Which words have the most branches and overlap?** The **hub(s)** — the terms with
    the highest degree across antonym, synonym and associate edges, and whose meaning
    overlaps the most other terms. The hub binds the web; it is where the most
    meaning-connections meet.

  * **In which key defining word does the most truth of meaning lie?** The
    **keystone** — the word the most *others are defined in terms of* (its defining
    reach, read from synonyms, associates, and the lexicon's `defined_in_terms_of`
    compounding). Meaning is relational, so the truth of it gathers where the web leans
    hardest: the word the most other words need in order to mean what they mean.

The web is read from the authored `relations.json` (the couples and shared meaning) and
the lexicon (the compounding over time). It is a proxy carrying its provenance, not a
real semantics; like every measure here but attestation, it is **descriptive, never a
gate** — it surfaces where the web's truth gathers; it does not crown a word. Pure
standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .condensation import Relations, _compound
from .lexicon import Lexicon


@dataclass(frozen=True)
class Couple:
    """An antonym pair, read as one edge of the web's binary skeleton.

    `root` is True when neither pole carries a condensed field — both are irreducible
    (bit-like): the couple is always paired no matter how meaning is later derived.
    """

    a: str
    b: str
    root: bool = False

    @property
    def axis(self) -> str:
        return f"{self.a}|{self.b}"


@dataclass(frozen=True)
class Node:
    """One term's place in the web."""

    term: str
    branches: int            # distinct neighbours across antonym/synonym/associate edges
    overlap: int             # other terms whose meaning-connections it shares
    defining_reach: int      # how many other terms are defined in terms of this one
    poles: tuple[str, ...] = ()
    kin: tuple[str, ...] = ()


@dataclass
class Weave:
    """The whole relational web of paired antonym couples and shared meaning."""

    couples: list[Couple] = field(default_factory=list)
    nodes: list[Node] = field(default_factory=list)

    @property
    def roots(self) -> list[Couple]:
        """The irreducible couples — always paired no matter how derived."""
        return [c for c in self.couples if c.root]

    @property
    def hubs(self) -> list[Node]:
        """The most-connected terms: the top branch count, ties kept (overlap orders)."""
        if not self.nodes:
            return []
        top = max(n.branches for n in self.nodes)
        return sorted(
            (n for n in self.nodes if n.branches == top),
            key=lambda n: (-n.overlap, n.term),
        )

    @property
    def keystone(self) -> Node | None:
        """The key defining word: the most others are defined in terms of it (defining
        reach), with branches then name breaking ties. Where the truth of meaning lies."""
        if not self.nodes:
            return None
        return sorted(
            self.nodes,
            key=lambda n: (-n.defining_reach, -n.branches, n.term),
        )[0]

    @property
    def verdict(self) -> str:
        return (f"the meaning web: {len(self.couples)} antonym couple(s), "
                f"{len(self.roots)} root(s), {len(self.nodes)} term(s)")

    @property
    def summary(self) -> str:
        rows = [self.verdict]

        rows.append("  root antonyms (always paired, no matter how derived — both poles irreducible):")
        for c in self.roots:
            rows.append(f"    {c.axis}")
        if not self.roots:
            rows.append("    — (none: every couple carries a condensed field)")

        rows.append("  hubs (the most branches and overlap of synonyms and antonyms):")
        for n in self.hubs:
            rows.append(f"    {n.term:<12} branches {n.branches}  overlap {n.overlap}  "
                        f"[pole(s): {', '.join(n.poles) or '—'}]")

        k = self.keystone
        if k is not None:
            rows.append(f"  keystone — the key defining word the most truth of meaning lies in: "
                        f"{k.term}")
            rows.append(f"    {k.defining_reach} other word(s) are defined in terms of "
                        f"'{k.term}'; branches {k.branches}, overlap {k.overlap}")

        rows.append("  note: meaning is relational — the truth of it gathers where the web leans "
                    "hardest. An authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def _is_condensed(term: str, relations: Relations, lexicon: Lexicon | None) -> bool:
    """True when a pole carries a field of its *own* (declared synonyms/associates) or
    compounded ancestry — i.e. it is not an irreducible bit. A bare pole (no entry of its
    own) and a term that is only referenced by others are both still bit-like."""
    t = relations.terms.get(term)
    if t is not None and (t.synonyms or t.associates):
        return True
    if lexicon is not None and term in lexicon.lexemes and lexicon.lexemes[term].defined_in_terms_of:
        return True
    return False


def weave(relations: Relations, lexicon: Lexicon | None = None) -> Weave:
    """Read the whole relational web: the antonym couples (and which are roots), the
    hubs (most branches and overlap), and the keystone (the key defining word the most
    truth of meaning lies in).

    Couples are the antonym pairs; a couple is a **root** when neither pole is condensed.
    A term's **branches** is its degree across antonym/synonym/associate edges; its
    **overlap** is how many other terms share a meaning-connection with it; its
    **defining reach** is how many other terms are defined in terms of it (from synonyms,
    associates, and the lexicon's compounding). Descriptive, never a gate.
    """
    # 1. Couples: unordered antonym pairs, classified root vs derived.
    seen: set[frozenset[str]] = set()
    couples: list[Couple] = []
    for t in relations.terms.values():
        for pole in t.antonyms:
            key = frozenset({t.id, pole})
            if len(key) < 2 or key in seen:
                continue
            seen.add(key)
            a, b = sorted(key)
            root = not _is_condensed(a, relations, lexicon) and not _is_condensed(b, relations, lexicon)
            couples.append(Couple(a=a, b=b, root=root))
    couples.sort(key=lambda c: (not c.root, c.axis))

    # 2. Defining reach: directed in-references (who is defined in terms of whom).
    indegree: dict[str, int] = {}
    referrers: dict[str, set[str]] = {}
    for t in relations.terms.values():
        for name in set(t.synonyms) | set(t.associates):
            referrers.setdefault(name, set()).add(t.id)
    if lexicon is not None:
        for lx in lexicon.lexemes.values():
            for dep in lx.defined_in_terms_of:
                referrers.setdefault(dep, set()).add(lx.id)
    for name, refs in referrers.items():
        indegree[name] = len(refs - {name})

    # 3. Per-term branches and overlap, over the symmetric meaning-connection web.
    def neighbours(term: str) -> set[str]:
        return (set(relations.antonyms_of(term))
                | set(relations.synonyms_of(term))
                | set(relations.associates_of(term)))

    nbr = {tid: neighbours(tid) for tid in relations.terms}
    nodes: list[Node] = []
    for tid, t in relations.terms.items():
        overlap = sum(1 for other in relations.terms if other != tid and nbr[tid] & nbr[other])
        nodes.append(Node(
            term=tid,
            branches=len(nbr[tid]),
            overlap=overlap,
            defining_reach=indegree.get(tid, 0),
            poles=relations.antonyms_of(tid),
            kin=relations.synonyms_of(tid),
        ))
    nodes.sort(key=lambda n: (-n.branches, -n.defining_reach, n.term))

    return Weave(couples=couples, nodes=nodes)
