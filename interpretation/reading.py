"""The three layers of reading a concept's history.

The sibling *integrity-alignment-system* separates a *verdict* (does this clear
the line?) from *understanding* (what is this, really?) and then adds a third
layer that refuses to trust the verdict on faith. Conceptual history needs the
same three, because the failure modes are the same:

  L1  **Attestation**  - Is the usage real? The word, shown in a cited text.
                         A gate: you cannot interpret what was never said.
  L2  **Reading**      - What did the word mean *here*, described in its own
                         context. Never a verdict on "the meaning"; a description.
  L3  **Anachronism**  - Has our reading drifted from the usage's own time into a
                         later sense? The proxy (our reading) vs. the target (what
                         the word did then). Drift is the hermeneutic Goodhart.

L1 is the only gate. L2 and L3 *describe* and never block - a skipped or surprising
reading may be perfectly legitimate; the framework reports the shape and leaves the
judgement to a human. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .fingerprint import normalize
from .glossary import Usage
from .semantics import SenseLattice


# --- L1: Attestation --------------------------------------------------------

@dataclass
class Attestation:
    """Whether a usage is admissible: the word, shown, in a cited text."""

    usage_id: str
    ok: bool
    reasons: list[str] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        head = "ATTESTED" if self.ok else "NOT ATTESTED"
        why = "" if self.ok else " - " + "; ".join(self.reasons)
        return f"{head}: {self.usage_id}{why}"


def _word_in_quotation(word: str, quotation: str) -> bool:
    """Does the cited word actually occur in the quotation (modulo case/inflection)?

    Matches on a normalised word-token prefix so an inflected or declined form
    (Latin *revolutionibus* for *revolution*) still counts as the word being shown -
    a deliberately generous test, because attestation should err toward admitting a
    real usage, not toward a brittle exact match.
    """
    w = normalize(word)
    if not w:
        return False
    tokens = normalize(quotation).split()
    stem = w.split()[0][:5]  # first 5 chars of the first word: tolerate inflection
    return any(tok.startswith(stem) for tok in tokens) or w in normalize(quotation)


def attest(usage: Usage) -> Attestation:
    """L1: is this usage attested? The one gate in the framework.

    A usage is admissible only if it cites a source, carries a quotation, and the
    word can actually be shown within that quotation. An interpretation built on a
    usage that fails attestation is built on sand - so this is the gate, and the
    only one.
    """
    reasons: list[str] = []
    if not usage.citation.strip():
        reasons.append("no citation: the usage names no source")
    if not usage.quotation.strip():
        reasons.append("no quotation: nothing to show the word in")
    elif not _word_in_quotation(usage.word, usage.quotation):
        reasons.append(
            f"the word {usage.word!r} does not appear in the quotation - "
            f"the citation does not show the usage it claims"
        )
    return Attestation(usage_id=usage.id, ok=not reasons, reasons=reasons)


# --- L2: Reading ------------------------------------------------------------

@dataclass
class Reading:
    """A described sense of a usage, in its own context. Never 'the meaning'."""

    usage_id: str
    sense_id: str
    sense_label: str
    sense_gloss: str
    usage_year: int
    sense_year: int

    @property
    def summary(self) -> str:
        return (
            f"reading {self.usage_id} in the sense '{self.sense_label}' "
            f"({self.sense_gloss})\n"
            f"  note: this is *a* reading of the usage, situated in its context - "
            f"not a verdict on the word's one true meaning."
        )


def read(usage: Usage, sense_id: str, lattice: SenseLattice) -> Reading:
    """L2: describe the sense a usage is being read in. Descriptive, never a gate.

    Raises only if the sense is not in the concept's lattice (you cannot read a
    usage in a sense the authored map does not record) - that is a lookup error,
    not a verdict.
    """
    sense = lattice.senses[sense_id]  # KeyError if unknown - surfaced, not guessed
    return Reading(
        usage_id=usage.id,
        sense_id=sense_id,
        sense_label=sense.label,
        sense_gloss=sense.gloss,
        usage_year=usage.year,
        sense_year=sense.year,
    )


# --- L3: Anachronism drift --------------------------------------------------

@dataclass
class Drift:
    """How far a reading has drifted from the usage's own time.

    Direction-aware, because conceptual history has two opposite errors:

      * **anachronism** (the cardinal one) - reading a *later* sense back into an
        *earlier* usage: hearing post-1789 'rupture' in a 1688 'revolution'.
      * **archaism** - reading a much *earlier*, perhaps obsolete sense into a
        later usage. Weaker evidence (a sense can persist), so it is reported but
        not treated as the primary signal.
    """

    usage_id: str
    sense_id: str
    usage_year: int
    sense_year: int
    anachronism_years: int      # sense postdates the usage by this many years (the error)
    archaism_years: int         # sense predates the usage by this many years (suggestive)

    @property
    def anachronistic(self) -> bool:
        return self.anachronism_years > 0

    @property
    def verdict(self) -> str:
        if self.anachronistic:
            return (
                f"ANACHRONISM: reading {self.usage_id} ({self.usage_year}) in a sense "
                f"first attested {self.sense_year} - a later meaning projected back "
                f"{self.anachronism_years} year(s)"
            )
        if self.archaism_years > 0:
            return (
                f"in period: the sense predates the usage by {self.archaism_years} "
                f"year(s) (available, though check it had not lapsed)"
            )
        return f"in period: the sense was contemporary with {self.usage_id}"


def drift(usage: Usage, sense_id: str, lattice: SenseLattice) -> Drift:
    """L3: measure the gap between a reading's sense and the usage's own time.

    The proxy is the sense we read; the target is the sense available *then*. A
    positive `anachronism_years` is the hermeneutic version of a green check that
    measured the wrong thing. Descriptive - it reports the gap; it never blocks a
    reading (a human decides whether the projection is defensible).
    """
    sense = lattice.senses[sense_id]
    gap = sense.year - usage.year
    return Drift(
        usage_id=usage.id,
        sense_id=sense_id,
        usage_year=usage.year,
        sense_year=sense.year,
        anachronism_years=max(0, gap),
        archaism_years=max(0, -gap),
    )
