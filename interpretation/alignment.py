"""Interpretive alignment of a reading within the recorded history of a concept.

    interpretive alignment = purpose x fidelity

A graded, *descriptive* reading of where one interpretation sits relative to the
others recorded for the same concept. It never gates or blocks (it is
L2-Reading-shaped); it describes, so a human can decide what it means. It is the
sibling system's `alignment = purpose x truth`, with `truth` re-read for
conceptual history as **fidelity to the historical usage**:

  * **purpose** - contribution to the recorded reading of the concept: how much
    this reading adds that is not already on record (novelty, 1 - similarity). A
    reading that restates a known gloss adds little; a genuinely new reading adds
    a lot.

  * **fidelity** - how faithfully the reading sits in the concept's actual
    history. It is the product of the three layers turned into one number, and so
    it is exactly as honest as they are:
      - **soundness**: the ledger chain verifies (the record is untampered);
      - **grounding**: the reading descends from a usage that is recorded *and*
        passes L1-Attestation - a reading floating free of any attested usage is
        not grounded;
      - **not anachronistic**: L3 finds no later sense projected back into an
        earlier usage - an anachronistic reading forfeits fidelity entirely;
      - **corroboration**: distinct *other* readers concur (independently or by
        building on it).
    fidelity = soundness x (not anachronistic) x (0.5*grounding + 0.5*corroboration)

Because it is a product, the quadrants are honest: a fresh, well-grounded reading
is *purposeful but only half-aligned* (high purpose x ~0.5 fidelity) until other
readers corroborate it; an anachronistic reading is high-purpose, zero-fidelity,
however clever. Low alignment is a *description of where a reading sits*, never a
verdict on its worth - and the record protects it in full either way.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .fingerprint import jaccard
from .glossary import Glossary
from .ledger import KIND_INTERPRETATION, KIND_USAGE, NON_WORK_KINDS, Ledger
from .reading import attest, drift

# A similarity at or above this counts two readings as the same interpretation.
RECOGNITION_THRESHOLD = 0.2
# Distinct corroborating readers for full corroboration.
CORROBORATION_TARGET = 2


@dataclass
class Alignment:
    purpose: float                 # contribution to the recorded reading [0,1]
    fidelity: float                # faithfulness to the concept's history [0,1]
    novelty_verdict: str
    grounded: bool = False
    anachronistic: bool = False
    soundness_ok: bool = True
    corroborators: list[str] = field(default_factory=list)
    influence: int = 0             # distinct downstream readings that build on it

    @property
    def value(self) -> float:
        return round(self.purpose * self.fidelity, 4)

    @property
    def gloss(self) -> str:
        if self.anachronistic:
            return "a later sense read into an earlier usage (anachronism: no fidelity)"
        if not self.grounded:
            return "a reading not yet grounded in an attested usage"
        hi_p, hi_f = self.purpose >= 0.5, self.fidelity >= 0.5
        if hi_p and hi_f:
            return "adds to, and sits faithfully within, the concept's history"
        if hi_p and not hi_f:
            return "a new reading, grounded but not yet corroborated"
        if not hi_p and hi_f:
            return "a faithful restatement (adds little that is new)"
        return "neither new nor yet corroborated"

    @property
    def verdict(self) -> str:
        return (
            f"interpretive alignment = purpose({self.purpose:.2f}) x "
            f"fidelity({self.fidelity:.2f}) = {self.value:.2f}  ->  {self.gloss}"
        )

    @property
    def summary(self) -> str:
        lines = [
            self.verdict,
            f"  purpose:  {self.purpose:.2f}  (novelty: {self.novelty_verdict})",
            f"  fidelity: {self.fidelity:.2f}  (grounded: {self.grounded}; "
            f"anachronistic: {self.anachronistic}; chain sound: {self.soundness_ok}; "
            f"corroborated by: {self.corroborators or 'none'})",
            f"  influence: {self.influence} downstream reading(s) build on it (accrues over time)",
            "  note: fidelity is faithfulness to the recorded usage, a proxy - "
            "not a verdict on the word's absolute meaning.",
        ]
        return "\n".join(lines)


def _descendants(record_id: str, records: list) -> set[str]:
    """Every reading that transitively builds on `record_id` (via parents)."""
    children: dict[str, set[str]] = {}
    for r in records:
        if r.kind in NON_WORK_KINDS:
            continue
        for p in r.parents:
            children.setdefault(p, set()).add(r.id)
    seen: set[str] = set()
    stack = [record_id]
    while stack:
        for child in children.get(stack.pop(), ()):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen


def _grounded_in_attested_usage(rec, ledger: Ledger, glossary: Glossary) -> bool:
    """True if the reading descends from a usage that is both recorded and attested."""
    for pid in rec.parents:
        parent = ledger.by_id(pid)
        if parent is None or parent.kind != KIND_USAGE:
            continue
        try:
            usage = glossary.usage(pid)
        except KeyError:
            continue
        if attest(usage).ok:
            return True
    return False


def _anachronistic(rec, ledger: Ledger, glossary: Glossary) -> bool:
    """True if the reading reads its sense into a usage that predates the sense."""
    if not rec.sense:
        return False
    for pid in rec.parents:
        parent = ledger.by_id(pid)
        if parent is None or parent.kind != KIND_USAGE:
            continue
        try:
            usage = glossary.usage(pid)
            lattice = glossary.lattice_for_usage(pid)
        except KeyError:
            continue
        if rec.sense in lattice.senses and drift(usage, rec.sense, lattice).anachronistic:
            return True
    return False


def interpretive_alignment_of(
    record_id: str,
    ledger: Ledger,
    glossary: Glossary,
    *,
    corroboration_target: int = CORROBORATION_TARGET,
) -> Alignment:
    """Alignment of an already-recorded reading, against the CURRENT record.

    `purpose` is fixed at creation (novelty against the readings of the same
    concept that preceded it). `fidelity` accrues: it rises as distinct *other*
    readers corroborate the reading, and collapses if the chain breaks or the
    reading is anachronistic.
    """
    records = ledger.records
    rec, pos = None, -1
    for i, r in enumerate(records):
        if r.id == record_id and r.kind == KIND_INTERPRETATION:
            rec, pos = r, i
    if rec is None:
        raise KeyError(f"no interpretation record '{record_id}' in the ledger")

    # purpose = novelty at creation, against prior readings of the SAME concept.
    prior = [
        r for r in records[:pos]
        if r.kind == KIND_INTERPRETATION and r.concept == rec.concept
    ]
    exact_prior = any(
        rec.normalized_hash == p.normalized_hash for p in prior
    )
    best_prior = 1.0 if exact_prior else max(
        (jaccard(tuple(rec.signature), tuple(p.signature)) for p in prior),
        default=0.0,
    )
    purpose = round(1.0 - best_prior, 4)
    novelty_verdict = _novelty_label(best_prior, exact_prior)

    soundness_ok = ledger.verify().ok
    grounded = _grounded_in_attested_usage(rec, ledger, glossary)
    anachronistic = _anachronistic(rec, ledger, glossary)

    # corroboration: distinct OTHER readers whose reading of this concept overlaps.
    descendants = _descendants(record_id, records)
    corroborators: set[str] = set()
    for other in records:
        if other.kind != KIND_INTERPRETATION or other.id == record_id:
            continue
        if other.concept != rec.concept or other.author == rec.author:
            continue  # corroboration must be independent of the author
        overlaps = (
            (other.sense == rec.sense and bool(rec.sense))
            or other.normalized_hash == rec.normalized_hash
            or jaccard(tuple(other.signature), tuple(rec.signature)) >= RECOGNITION_THRESHOLD
        )
        if other.id in descendants or overlaps:
            corroborators.add(other.author)
    corroboration = min(1.0, len(corroborators) / max(corroboration_target, 1))

    not_anachronistic = 0.0 if anachronistic else 1.0
    fidelity = (
        (1.0 if soundness_ok else 0.0)
        * not_anachronistic
        * (0.5 * (1.0 if grounded else 0.0) + 0.5 * corroboration)
    )

    return Alignment(
        purpose=purpose,
        fidelity=round(fidelity, 4),
        novelty_verdict=novelty_verdict,
        grounded=grounded,
        anachronistic=anachronistic,
        soundness_ok=soundness_ok,
        corroborators=sorted(corroborators),
        influence=len(descendants),
    )


def _novelty_label(best_prior: float, exact: bool) -> str:
    if exact or best_prior >= 0.999:
        return "DUPLICATE"
    if best_prior >= 0.6:
        return "RESTATEMENT"
    if best_prior >= RECOGNITION_THRESHOLD:
        return "VARIANT"
    return "NOVEL"
