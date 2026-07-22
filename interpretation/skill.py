"""The skills: signal threads mechanised -- the thread walked until it walks itself.

A **skill** is the mechanising of a signal thread: the conceptual requirements to
fulfill it (the cells that must be trained), its **mechanics** as dual definitions
-- the *noun* is the capacity at rest, the *verb* the operation in act, the
*directive* the imperative that trains it, and the *relation* the preposition it
binds through (knowledge OF, judgment BETWEEN, technique FOR, fluency IN,
recognition AS -- the relational nature of directive terms, checkable in plain
collocation) -- its **formation** (the walk around the grid: knowledge ->
technique -> fluency -> judgment, the Dreyfus circuit), and its **integration**
(how it spans lattices: no skill lives in one grid).

The bound records the discipline: the dual definition is linguistic mechanics,
not metaphor (the language stores every capacity twice, state-form and
act-form); fluency is the easiest cell to counterfeit, so a system with
knowledge, technique, and fluency but no judgment is a mechanism, not a mastery;
and *techne* is from *teks-*, to weave -- one root with text and textile -- so a
skills section woven of threads is the etymology remembering itself.

A reader, not a ruler: descriptive, never a gate. Pure stdlib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

MECHANIC_PARTS = ("noun", "verb", "directive", "relation")


@dataclass(frozen=True)
class Mechanic:
    """One word's dual definition: the capacity at rest and the operation in act."""

    word: str
    noun: str
    verb: str
    directive: str
    relation: str

    @property
    def summary(self) -> str:
        return (f"    {self.word}:\n"
                f"      noun (at rest): {self.noun}\n"
                f"      verb (in act):  {self.verb}\n"
                f"      directive:      {self.directive}\n"
                f"      relation:       {self.relation}")


@dataclass(frozen=True)
class Skill:
    """One mechanised thread: requirements, mechanics, formation, integration."""

    id: str
    name: str
    serves: str                       # the signal thread this skill helps fulfill
    draws_on: tuple[str, ...]         # the lattices it spans (quartet ids)
    requirements: tuple[str, ...]     # the conceptual requirements, trainable cells
    mechanics: tuple[Mechanic, ...]   # dual definitions, word by word
    formation: str                    # the circuit: how the skill forms
    integration: str                  # the relational reading across lattices

    @property
    def summary(self) -> str:
        rows = [
            f"{self.id} — {self.name}",
            f"  serves: {self.serves}   draws on: {', '.join(self.draws_on)}",
            "  conceptual requirements:",
            *[f"    - {r}" for r in self.requirements],
            "  mechanics (dual definitions -- noun at rest, verb in act):",
            *[m.summary for m in self.mechanics],
            f"  formation: {self.formation}",
            f"  integration: {self.integration}",
        ]
        return "\n".join(rows)


@dataclass
class Skills:
    skills: list[Skill] = field(default_factory=list)
    bound: dict = field(default_factory=dict)
    title: str = ""
    note: str = ""

    def by_id(self, sid: str) -> Skill:
        for s in self.skills:
            if s.id == sid:
                return s
        raise KeyError(f"unknown skill {sid!r}; have {[s.id for s in self.skills]}")

    @property
    def summary(self) -> str:
        rows = [self.title or "the skills", ""]
        for s in self.skills:
            rows.append(s.summary)
            rows.append("")
        if "the_dual_definition" in self.bound:
            rows.append(f"  bound: {self.bound['the_dual_definition']}")
        if "the_counterfeit" in self.bound:
            rows.append(f"  bound: {self.bound['the_counterfeit']}")
        rows.append("  a reader, not a ruler: descriptive, never a gate.")
        return "\n".join(rows)


def _mechanics(raw: dict) -> tuple[Mechanic, ...]:
    out = []
    for word, parts in raw.items():
        missing = [p for p in MECHANIC_PARTS if p not in parts]
        if missing:
            raise ValueError(
                f"mechanic {word!r} is missing {missing}: a dual definition names "
                f"all of {MECHANIC_PARTS} -- the noun at rest, the verb in act, "
                f"the directive, and the relation it binds through"
            )
        out.append(Mechanic(word=word, **{p: parts[p] for p in MECHANIC_PARTS}))
    return tuple(out)


def load_skills(path) -> Skills:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return Skills(
        skills=[Skill(
            id=e["id"], name=e.get("name", e["id"]),
            serves=e.get("serves", ""),
            draws_on=tuple(e.get("draws_on", ())),
            requirements=tuple(e.get("requirements", ())),
            mechanics=_mechanics(e.get("mechanics", {})),
            formation=e.get("formation", ""),
            integration=e.get("integration", ""),
        ) for e in raw.get("skills", [])],
        bound=raw.get("bound", {}),
        title=raw.get("title", ""),
        note=raw.get("note", ""),
    )
