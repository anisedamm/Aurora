"""Weighted meaning: a conceptual sign carries a *field* of values, not a lexeme.

The pump regime asks "what word is this?" and expects one lexical answer. The
breath regime does not work that way: the labrys (the Minoan double axe) is not the
word "axe" - it holds, at once and in proportion, *paradoxical equilibrium*,
*sovereignty*, *divinity*, *belonging*. Its meaning is a **weighted field**, and to
read it is to propose a weighting, not to look up an entry.

A reading is **true** here insofar as it **resonates** with the field the culture
*retained* - how much of the weight coincides. `resonance` is the histogram
intersection of two normalised fields: 1.0 when a reading matches the retained
weighting exactly, 0.0 when they are disjoint. It is a **proxy** for fit to a
retained conceptual truth, never an oracle of what the sign "really" meant - the
same humility the rest of the framework runs on. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class WeightedField:
    """A field of conceptual values with proportional weights (need not sum to 1)."""

    weights: Mapping[str, float]

    def normalized(self) -> dict[str, float]:
        """Weights as a distribution summing to 1 (negatives clamped to 0)."""
        total = sum(max(0.0, w) for w in self.weights.values())
        if total <= 0:
            return {}
        return {k: max(0.0, w) / total for k, w in self.weights.items()}

    def resonance(self, other: "WeightedField | Mapping[str, float]") -> float:
        """Histogram intersection of two normalised fields, in [0, 1].

        How much of the weight the two fields hold *in common*. 1.0 = identical
        weighting; 0.0 = no shared value. Symmetric. This is the measure that makes
        'meaning as weighted alignment' computable without pretending to certainty.
        """
        other = other if isinstance(other, WeightedField) else WeightedField(other)
        a, b = self.normalized(), other.normalized()
        if not a or not b:
            return 0.0
        return round(sum(min(a.get(k, 0.0), b.get(k, 0.0)) for k in set(a) | set(b)), 4)

    def dominant(self, n: int = 3) -> list[tuple[str, float]]:
        """The n heaviest values, normalised, weight-descending then name."""
        norm = self.normalized()
        return sorted(norm.items(), key=lambda kv: (-kv[1], kv[0]))[:n]

    @property
    def gloss(self) -> str:
        if not self.weights:
            return "(no weighted field)"
        return ", ".join(f"{k} ({w:.2f})" for k, w in self.dominant(n=len(self.weights)))
