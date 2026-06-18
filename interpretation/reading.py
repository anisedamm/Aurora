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
from .regime import BREATH, SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC, is_phonetic_projection
from .semantics import SenseLattice
from .weighting import WeightedField


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

    It dispatches on the script mode, because the two regimes are shown differently:

      * a **phonetic** usage is admissible only if it cites a source, carries a
        quotation, and the word can be shown within that quotation;
      * a **conceptual** usage (a breath-era symbol) is admissible only if it names
        the material `artifact` (or a source) it is attested in *and* carries a
        non-empty weighted field - you cannot read a symbol that holds no recorded
        conceptual content.

    An interpretation built on a usage that fails attestation is built on sand - so
    this is the gate, and the only one.
    """
    reasons: list[str] = []
    if usage.mode == SCRIPT_CONCEPTUAL:
        if not usage.artifact.strip() and not usage.citation.strip():
            reasons.append("no material attestation: the symbol names no artifact or source")
        if not usage.field:
            reasons.append("no weighted field: a symbol with no recorded conceptual content cannot be read")
    else:
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


@dataclass
class WeightedReading:
    """L2 for a conceptual sign: a proposed weighting against the retained field.

    A symbol is not read by picking a lexeme but by proposing how its weight is
    distributed across conceptual values. The reading is *true* insofar as it
    resonates with the field the culture retained - but, like every L2 here, it is a
    description, never a verdict on the symbol's one meaning.
    """

    usage_id: str
    proposed: WeightedField   # the reading's weighting
    retained: WeightedField   # the symbol's recorded field

    @property
    def resonance(self) -> float:
        return self.proposed.resonance(self.retained)

    @property
    def summary(self) -> str:
        dom = ", ".join(f"{k} ({w:.2f})" for k, w in self.proposed.dominant())
        return (
            f"reading {self.usage_id} as a weighted field: {dom}\n"
            f"  resonance with the retained field: {self.resonance:.2f}\n"
            f"  note: a symbol holds its values at once; this is a proposed weighting, "
            f"not a lexical meaning."
        )


def read_symbol(usage: Usage, reading_field: dict | None = None) -> WeightedReading:
    """L2 for a conceptual usage: describe its weighted field (or a proposed reading).

    With no `reading_field`, the reading is the symbol's own retained field (a
    faithful re-statement, resonance 1.0). Pass a weighting to read it your way and
    see how far it resonates. Descriptive, never a gate.
    """
    retained = WeightedField(dict(usage.field))
    proposed = WeightedField(dict(reading_field)) if reading_field is not None else retained
    return WeightedReading(usage_id=usage.id, proposed=proposed, retained=retained)


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


@dataclass
class Projection:
    """L3 across the attention threshold: is a breath-era sign read in the pump mode?

    The deeper sibling of anachronism. Anachronism projects a later *sense* onto an
    earlier usage; **phonetic projection** projects a later *mode of attention* -
    reading a conceptual symbol as if it spelled a word, or a myth as if it reported
    a fact. The `ghost_lag_years` is how far back across the breath->pump threshold
    that pump-mode reading reaches.
    """

    usage_id: str
    read_mode: str
    usage_regime: str
    usage_mode: str
    phonetic_projection: bool
    ghost_lag_years: int

    @property
    def verdict(self) -> str:
        if self.phonetic_projection:
            lag = f"; ghost lag {self.ghost_lag_years} year(s) across the threshold" if self.ghost_lag_years else ""
            return (
                f"PHONETIC PROJECTION: reading {self.usage_id} "
                f"({self.usage_regime}/{self.usage_mode}) in the phonetic mode - "
                f"imposing a later mode of attention, as if the sign spelled a word{lag}"
            )
        return (
            f"in regime: {self.usage_id} read in a mode consonant with its attention "
            f"({self.usage_regime}/{self.usage_mode})"
        )


def project(usage: Usage, read_mode: str, *, threshold: int | None = None) -> Projection:
    """L3: does reading `usage` in `read_mode` impose a later mode of attention?

    The cardinal error of the breath/pump threshold (Step 11 in the thought-flow):
    reading a conceptual, breath-era sign phonetically. Descriptive - it reports the
    ghost lag; a human decides whether the projection is defensible.
    """
    proj = is_phonetic_projection(usage.regime or "", usage.mode or "", read_mode)
    lag = max(0, threshold - usage.year) if (proj and threshold is not None) else 0
    return Projection(
        usage_id=usage.id,
        read_mode=read_mode,
        usage_regime=usage.regime or "",
        usage_mode=usage.mode or "",
        phonetic_projection=proj,
        ghost_lag_years=lag,
    )
