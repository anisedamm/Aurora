"""The return path: how faithfully a later record carries an earlier truth back.

This is the **inverse of phonetic projection** (`reading.project`). Both traverse
the breath->pump ghost lag, in opposite directions and with opposite valence:

  * **projection** drags the *present* mode of attention *back* over a *past* sign -
    reading a breath-era symbol as if it spelled a word. An error: it imposes.

  * **remembrance** carries a *past* conceptual truth *forward* into a *later*
    record - a pump-era myth or text that keeps a breath-era truth alive across the
    threshold. A virtue, when it is faithful: it preserves.

Myth is the paradigm case. Hesiod's *Theogony* is a phonetic text written at the
threshold; read as conceptual memory (not as literal genealogy), it *remembers* the
breath-era truth of a cosmogonic succession. `remember` scores how faithfully a
later record carries an earlier truth: the **fidelity** is the resonance of what the
record carries with what the culture retained, and the **span** is the years the
memory reached back across the divide. It is **descriptive, never a gate** - it
measures the return; a human judges whether the memory is good enough.
"""

from __future__ import annotations

from dataclasses import dataclass

from .glossary import Glossary, Usage
from .reading import attest
from .weighting import WeightedField


@dataclass
class Remembrance:
    """How faithfully a later record carries an earlier breath-truth back across the lag."""

    by_id: str             # the later record doing the remembering
    remembered: str        # the earlier breath-truth (a concept id)
    fidelity: float        # resonance of the carried field with the retained truth [0,1]
    span_years: int        # how far back the memory reaches (later - earlier origin)
    crosses_threshold: bool  # does it genuinely return across the breath->pump divide?
    attested: bool         # both ends are attested (the record, and the retained truth)

    @property
    def gloss(self) -> str:
        if not self.attested:
            return "unattested: the record or the remembered truth is not shown"
        if not self.crosses_threshold:
            return "not a return: the record does not reach back across the threshold"
        if self.fidelity >= 0.6:
            return "a faithful remembrance: the breath-era truth is carried back intact"
        if self.fidelity >= 0.2:
            return "a partial memory: the truth is carried back, but worn down"
        return "the memory has all but lapsed — the return failed (a projection in disguise)"

    @property
    def verdict(self) -> str:
        return (
            f"REMEMBRANCE: {self.by_id} carries '{self.remembered}' back "
            f"{self.span_years} year(s) across the threshold (resonance "
            f"{self.fidelity:.2f})  ->  {self.gloss}"
        )


def remember(usage: Usage, glossary: Glossary) -> Remembrance:
    """Score the return path declared by `usage.remembers`.

    The later record carries a weighted field (`usage.field`); the remembered concept
    holds a retained conceptual truth (its declared field, or its attested symbol's
    field). Fidelity is the resonance between them; the span is how far back across
    the threshold the memory reaches. Raises ValueError if the usage declares no
    remembrance. Descriptive, never a gate.
    """
    if not usage.remembers:
        raise ValueError(f"usage {usage.id!r} declares no remembrance (no `remembers`)")

    concept = glossary.concept(usage.remembers)
    retained = concept.retained_field()
    carried = dict(usage.field)
    fidelity = WeightedField(carried).resonance(WeightedField(retained))

    earlier = concept.origin_year()
    later = usage.year
    span = (later - earlier) if (earlier is not None and later is not None) else 0

    threshold = concept.threshold
    crosses = (
        threshold is not None and earlier is not None and later is not None
        and earlier < threshold <= later
    )
    attested = attest(usage).ok and bool(retained)

    return Remembrance(
        by_id=usage.id,
        remembered=usage.remembers,
        fidelity=round(fidelity, 4),
        span_years=int(span),
        crosses_threshold=bool(crosses),
        attested=attested,
    )
