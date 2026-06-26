"""Tension: whether a concept HOLDS its opposite (paradox) or EXCLUDES it (a clean cut).

The founding image of the whole framework is the labrys: *opposed blades held in
balance as one*. The ouroboros is the same move — *consumption and renewal held as one
cycle*, end as beginning. These breath signs do not resolve an opposition into a
distinction; they **hold** it, taut, as a living unity. That holding is the deepest form
of the framework's subject, and it had — until now — no measure.

This module supplies it, by reading the three stances a concept can take toward its
opposite:

  * **held — paradox** (breath). The opposite is carried *within*, as one whole. The
    labrys holds *paradoxical-equilibrium*; the ouroboros holds *cyclical-unity*. The
    tension is retained: the two poles pull against each other and balance, and the
    meaning is exactly that pull. This is the most condensed meaning of all, and the bit
    can never hold it.

  * **excluded — binary** (the bit). The opposite is set cleanly *outside*: signal|noise,
    true|false — a pure distinction, 0 xor 1, the poles mutually exclusive. The tension is
    *resolved* to a cut; there is no holding, only difference. This is the floor of
    natural computing, and the opposite gesture to the paradox.

  * **segmented** (pump). A shard carved from a once-held paradox. The pump regime took
    *equilibrium* — opposed forces held as one — and split it into *balance*, *justice*,
    *moderation*, *symmetry*, each keeping a facet and **dropping the paradox of
    opposites-held-as-one** (the glossary's own words). The tension is not resolved but
    *dissipated*: scattered across lexemes that no longer oppose anything.

And a fourth, across time rather than at once: a word whose sense **inverted** holds its
opposite *diachronically*. *revolution* meant a turning-*back* (restoration), then its
sense flipped to a breaking-*forward* (irreversible rupture): the one word carried
opposed meanings across its history. A synchronic paradox holds its opposite in one
moment (the labrys); a diachronic one holds it across the word's life (revolution).

So the founding thesis, finally measured: **the bit EXCLUDES its opposite, the breath
sign HOLDS it as one, and the pump regime SEGMENTS the holding away.** The held-opposition
markers are authored (`paradoxes` in the glossary), grounded in the signs' own glosses and
linked to the migrations that segment them — a proxy, surfaced, not a proof. Descriptive,
never a gate. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .condensation import Relations
from .glossary import Glossary

# The stances a concept takes toward its opposite.
HELD = "paradox"          # holds its opposite as one living whole (breath) — tension retained
EXCLUDED = "binary"       # excludes its opposite cleanly (the bit) — tension resolved to a cut
SEGMENTED = "segmented"   # a shard carved from a once-held paradox (pump) — tension dissipated
OPPOSED = "opposed"       # sets up an opposition and excludes the pole, but carries a field
NEUTRAL = "neutral"       # no opposition on record

# How a paradox is held: at once, or across the word's life.
SYNCHRONIC = "synchronic"  # opposites held in one moment (the labrys, the ouroboros)
DIACHRONIC = "diachronic"  # opposites held across time, via an inverted sense (revolution)


@dataclass(frozen=True)
class HeldParadox:
    """One held-opposition: a value carrying two poles as one, and how it is segmented."""

    paradox: str                              # the field value-name (e.g. paradoxical-equilibrium)
    value: str                                # the canonical/migrated value (e.g. equilibrium)
    opposites: str                            # the poles held as one
    held_by: list[tuple[str, float]] = field(default_factory=list)  # (sign, weight)
    segmented_into: list[str] = field(default_factory=list)         # pump shard terms

    @property
    def held_tension(self) -> float:
        return round(sum(w for _, w in self.held_by), 4)


@dataclass
class Tension:
    """One concept's stance toward its opposite."""

    concept: str
    word: str = ""
    kind: str = NEUTRAL
    tension: float = 0.0                       # held-opposition retained (synchronic weight)
    holds: list[tuple[str, str]] = field(default_factory=list)  # (paradox, opposites gloss)
    excludes: tuple[str, ...] = ()             # the antonym pole(s) set outside
    fell_from: str = ""                        # the paradox value this is a shard of (segmented)
    mode: str = ""                             # synchronic / diachronic / both (for a paradox)

    @property
    def verdict(self) -> str:
        if self.kind == HELD:
            held = "; ".join(f"{p} ({g})" for p, g in self.holds) or "an opposite across time"
            when = f" [{self.mode}]" if self.mode else ""
            return (f"PARADOX{when}: '{self.word or self.concept}' holds its opposite as one — "
                    f"{held}" + (f"; tension {self.tension:.2f}" if self.tension else ""))
        if self.kind == EXCLUDED:
            return (f"BINARY: '{self.word or self.concept}' excludes its opposite cleanly — "
                    f"a distinction {'|'.join((self.word or self.concept, *self.excludes))}; "
                    "tension resolved to a cut (the bit)")
        if self.kind == SEGMENTED:
            tail = (f"; and now excludes its own opposite "
                    f"({'|'.join((self.word or self.concept, *self.excludes))})") if self.excludes else ""
            return (f"SEGMENTED: '{self.word or self.concept}' is a shard carved from the paradox "
                    f"'{self.fell_from}' — the held-opposition dropped, tension dissipated{tail}")
        if self.kind == OPPOSED:
            return (f"OPPOSED: '{self.word or self.concept}' sets up an opposition "
                    f"({'|'.join((self.word or self.concept, *self.excludes))}) and excludes the pole "
                    "— a condensed distinction, not a held paradox")
        return f"NEUTRAL: '{self.word or self.concept}' carries no held opposition on record"

    @property
    def summary(self) -> str:
        rows = [self.verdict]
        if self.kind == HELD and self.mode in (DIACHRONIC, "both"):
            rows.append("    its sense inverted over time — the one word carried opposed meanings "
                        "across its history (a paradox in time, not at once)")
        rows.append("  note: the bit excludes its opposite, the breath sign holds it as one, the pump "
                    "regime segments the holding away. An authored proxy, descriptive, never a gate.")
        return "\n".join(rows)


def _breath_field(concept: str, glossary: Glossary) -> dict:
    """The retained conceptual field of a breath sign, or {} if it is not one."""
    c = glossary.concepts.get(concept)
    if c is None or c.regime != "breath":
        return {}
    return c.retained_field()


def _inverted(concept: str, glossary: Glossary) -> bool:
    """True when the concept's sense history contains an inversion (a diachronic paradox)."""
    c = glossary.concepts.get(concept)
    if c is None:
        return False
    return any(s.shift == "inversion" for s in c.lattice.senses.values())


def _shard_of(term: str, glossary: Glossary) -> str:
    """If `term` is a pump-era shard of a segmented paradox, the value it fell from."""
    for value, entry in glossary.migrations.items():
        if value.startswith("_"):
            continue
        if any(sh.get("term") == term for sh in entry.get("shards", [])):
            return value
    return ""


def tension(concept: str, glossary: Glossary, relations: Relations | None = None) -> Tension:
    """Read one concept's stance toward its opposite: held (paradox), excluded (binary),
    segmented (a shard), opposed, or neutral.

    A breath sign holding a paradox value (or a concept whose sense inverted) **holds** its
    opposite; a shard of a segmented paradox carries it no longer (segmented); a bit
    **excludes** it; a condensed word with an antonym is opposed. Descriptive, never a gate.
    """
    word = concept
    c = glossary.concepts.get(concept)
    if c is not None:
        word = c.name.split(" (")[0]

    # 1. A breath sign or an inverted word — does it hold its opposite?
    field_vals = _breath_field(concept, glossary)
    holds = [(p, glossary.paradoxes[p].get("opposites", p))
             for p in field_vals if p in glossary.paradoxes]
    held_tension = round(sum(field_vals[p] for p, _ in holds), 4)
    inverted = _inverted(concept, glossary)
    if holds or inverted:
        mode = (("both" if holds else DIACHRONIC) if inverted else SYNCHRONIC)
        return Tension(concept=concept, word=word, kind=HELD, tension=held_tension,
                       holds=holds, mode=mode)

    # 2. A pump-era shard of a once-held paradox?
    fell = _shard_of(concept, glossary)
    excludes = tuple(relations.antonyms_of(concept)) if relations is not None else ()
    if fell:
        return Tension(concept=concept, word=word, kind=SEGMENTED, fell_from=fell, excludes=excludes)

    # 3. A relations term: a bit (excludes), or a condensed word that opposes.
    if relations is not None and relations.known(concept):
        if excludes:
            t = relations.terms[concept]
            is_bit = not (t.synonyms or t.associates)
            return Tension(concept=concept, word=word,
                           kind=EXCLUDED if is_bit else OPPOSED, excludes=excludes)
    return Tension(concept=concept, word=word, kind=NEUTRAL, excludes=excludes)


@dataclass
class Tensions:
    """The whole reading of how the corpus stands toward opposition."""

    held: list[HeldParadox] = field(default_factory=list)
    inverted: list[str] = field(default_factory=list)   # concepts whose sense inverted (diachronic)
    binaries: list[str] = field(default_factory=list)   # bit terms that purely exclude

    @property
    def keystone(self) -> HeldParadox | None:
        """The most-held paradox: the opposition the breath web carried with most weight."""
        return max(self.held, key=lambda h: h.held_tension, default=None)

    @property
    def verdict(self) -> str:
        k = self.keystone
        deepest = f"; most held: {k.value} (tension {k.held_tension:.2f})" if k else ""
        return (f"tension: {len(self.held)} held paradox(es), {len(self.inverted)} inverted "
                f"(diachronic), {len(self.binaries)} pure binary(ies){deepest}")

    @property
    def summary(self) -> str:
        rows = ["== tension: how concepts stand toward their opposite ==", "  three stances:"]
        rows.append("  HELD — paradox (breath: the opposite carried as one living whole):")
        for h in sorted(self.held, key=lambda h: (-h.held_tension, h.value)):
            held = ", ".join(f"{s} ({w:.2f})" for s, w in h.held_by) or "—"
            rows.append(f"    {h.value:<11} ({h.opposites}) — held by {held}; tension {h.held_tension:.2f}")
            seg = ", ".join(h.segmented_into)
            rows.append(f"        → pump segments it into: {seg or '(not mapped)'} "
                        + ("(the paradox dropped)" if h.segmented_into else ""))
        if self.inverted:
            rows.append("  INVERTED — diachronic paradox (pump: the opposite held across the word's life):")
            rows.append(f"    {', '.join(self.inverted)} — a sense that inverted into its opposite over time")
        rows.append("  EXCLUDED — binary (the bit: the opposite set cleanly outside, no holding):")
        rows.append(f"    {', '.join(self.binaries) or '—'}")
        rows.append("  the founding reading: the bit EXCLUDES its opposite, the breath sign HOLDS it "
                    "as one, the pump regime SEGMENTS the holding away.")
        rows.append("  note: held-opposition markers are authored, grounded in the signs' glosses; "
                    "a proxy, descriptive, never a gate.")
        return "\n".join(rows)


def tensions(glossary: Glossary, relations: Relations | None = None) -> Tensions:
    """Read the whole corpus's stance toward opposition: the held paradoxes (and how the
    pump regime segments each), the inverted (diachronic) paradoxes, and the pure binaries.

    Held paradoxes are computed from the authored `paradoxes` markers against the breath
    signs' fields; segmentation is read from the `migrations`; binaries are the bit terms
    of the relations map (an antonym, no field). Descriptive, never a gate.
    """
    held: list[HeldParadox] = []
    for pname, meta in glossary.paradoxes.items():
        if pname.startswith("_"):
            continue
        value = meta.get("value", pname)
        held_by = []
        for c in sorted(glossary.concepts.values(), key=lambda c: c.id):
            if c.regime == "breath" and pname in c.retained_field():
                held_by.append((c.id, round(c.retained_field()[pname], 4)))
        shards = [sh["term"] for sh in glossary.migrations.get(value, {}).get("shards", [])]
        held.append(HeldParadox(paradox=pname, value=value, opposites=meta.get("opposites", ""),
                                held_by=held_by, segmented_into=shards))

    inverted = sorted(c.id for c in glossary.concepts.values() if _inverted(c.id, glossary))

    binaries: list[str] = []
    if relations is not None:
        for tid, t in relations.terms.items():
            if t.antonyms and not (t.synonyms or t.associates):   # a bit: a pole, no field
                binaries.append(tid)
    return Tensions(held=held, inverted=inverted, binaries=sorted(binaries))
