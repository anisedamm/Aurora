"""The skills: signal threads mechanised (dual definitions as linguistic mechanics)."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.quartet import load_quartets
from interpretation.skill import MECHANIC_PARTS, load_skills
from interpretation.thread import load_threads

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills.json"
THREADS = ROOT / "threads.json"
QUARTETS = ROOT / "quartets.json"


def _skills():
    return load_skills(SKILLS)


def test_the_skills_load_with_their_threads_and_lattices():
    sk = _skills()
    ids = {s.id for s in sk.skills}
    assert ids == {"contextual-perception", "abstract-recognition", "custodianship",
                   "formation", "exercising-intellectual-discipline"}
    ts = load_threads(THREADS)
    qs = load_quartets(QUARTETS)
    for s in sk.skills:
        ts.by_id(s.serves)                 # the served thread must exist
        for qid in s.draws_on:
            qs.by_id(qid)                  # every lattice drawn on must exist
        assert s.requirements              # conceptual requirements recorded
        assert s.formation and s.integration


def test_mechanics_are_dual_definitions():
    # every mechanic carries all four parts: noun at rest, verb in act,
    # directive, and the relational preposition it binds through
    for s in _skills().skills:
        assert s.mechanics
        for m in s.mechanics:
            for part in MECHANIC_PARTS:
                assert getattr(m, part).strip()


def test_a_mechanic_missing_a_part_is_surfaced_not_guessed(tmp_path):
    bad = tmp_path / "skills.json"
    bad.write_text(
        '{"skills": [{"id": "x", "serves": "t", '
        '"mechanics": {"w": {"noun": "n", "verb": "v"}}}]}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="missing"):
        load_skills(bad)


def test_the_relational_signatures_are_recorded():
    # the relational nature of directive terms: knowledge OF, judgment BETWEEN,
    # technique FOR, fluency IN live in the skill quartet's dimensions, and
    # recognition AS (the hermeneutic as) in the skills that train reading
    qs = load_quartets(QUARTETS)
    skill_q = qs.by_id("skill")
    assert "knowledge OF" in skill_q.dimensions["knowledge"]
    assert "judgment BETWEEN" in skill_q.dimensions["judgment"]
    assert "technique FOR" in skill_q.dimensions["technique"]
    assert "fluency IN" in skill_q.dimensions["fluency"]
    sk = _skills()
    cp = sk.by_id("contextual-perception")
    rec = next(m for m in cp.mechanics if m.word == "recognition")
    assert "AS" in rec.relation


def test_custodianship_is_the_reflexive_skill():
    # Aurora's own skill: it serves the signal-thread, spans the reflexive
    # lattices, and its central dual pair is integrity = integrate at rest
    cust = _skills().by_id("custodianship")
    assert cust.serves == "signal-thread"
    assert {"spine", "remembering", "integrate", "skill"} <= set(cust.draws_on)
    integ = next(m for m in cust.mechanics if m.word == "integrity")
    assert "at rest" in integ.noun
    assert "refuse" in " ".join(cust.requirements).lower()   # the refusals are requirements


def test_the_bound_records_the_weave_and_the_counterfeit():
    sk = _skills()
    assert "the_dual_definition" in sk.bound
    assert "the_relational_signature" in sk.bound
    assert "the_counterfeit" in sk.bound
    assert "teks-" in sk.bound["the_weave"]          # techne/text/textile, one root
    s = sk.summary
    assert "custodianship" in s and "never a gate" in s


def test_formation_is_the_masters_skill():
    # instigating aligned discipline, comprehending active discernment:
    # the complement of custodianship -- the keeper keeps, the master forms
    # the keeper; it serves the skill-thread (techne teaching itself forward)
    form = _skills().by_id("formation")
    assert form.serves == "skill-thread"
    assert {"skill", "agency", "spine", "process"} == set(form.draws_on)
    words = {m.word for m in form.mechanics}
    assert words == {"instigation", "alignment", "discipline", "discernment", "comprehension"}
    disc = next(m for m in form.mechanics if m.word == "discipline")
    assert "discere" in disc.noun and "learn" in disc.noun.lower()   # the root kept
    assert "punishment" in disc.directive                            # the drift guarded
    inst = next(m for m in form.mechanics if m.word == "instigation")
    assert "instinct" in inst.verb                    # the goad-family: made twin of given
    reqs = " ".join(form.requirements).lower()
    assert "in act" in reqs                           # active discernment: judgment live
    assert "the silence" in form.formation            # the master's hardest discernment
    assert "refusal" in form.integration.lower()      # the affirmed refusal as proof


def test_exercising_intellectual_discipline_wears_the_crown():
    # the core virtue (bound.the_core_virtue) mechanised: serves the author's
    # own thread -- the ring is walked without breaking only by a discipline
    # exercised at every step
    sk = _skills().by_id("exercising-intellectual-discipline")
    assert sk.serves == "ethos-thread"
    assert {"ethos", "rep", "noticing", "testimony", "worth"} == set(sk.draws_on)
    words = {m.word for m in sk.mechanics}
    assert words == {"exercise", "ground", "refusal", "restraint", "check"}
    # exercere is ex + arcere: to exercise is to un-pen
    ex = next(m for m in sk.mechanics if m.word == "exercise")
    assert "arcere" in ex.verb and "un-penning" in ex.verb
    # the relational signature: of, for, of, from, against
    rels = {m.word: m.relation for m in sk.mechanics}
    assert rels["restraint"] == "restraint FROM"
    assert rels["check"] == "check AGAINST"
    reqs = " ".join(sk.requirements)
    # rigour's own etymology is the warning: rigor mortis as the counterfeit
    assert "rigor mortis" in reqs
    assert "RIGOUR'S OWN ETYMOLOGY IS THE WARNING" in reqs
    # the refusals kept visible: the credibility of the kept
    assert "refused constant" in reqs
    # formation: return-training for thought (James's clause as curriculum)
    assert "RETURN-TRAINING FOR THOUGHT" in sk.formation
    # integration: the record as the skill's gymnasium; the costliest refusal
    assert "gymnasium" in sk.integration
    assert "BECAUSE it was beautiful" in sk.integration


def test_unknown_skill_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _skills().by_id("nope")
