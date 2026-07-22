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
                   "formation", "exercising-intellectual-discipline",
                   "exercising-active-discernment", "defining-complete-certainty",
                   "comprehending-metaphorical-abstraction",
                   "comprehending-relational-significance"}
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


def test_exercising_active_discernment_runs_the_sift_live():
    # formation's master COMPREHENDS active discernment; this skill EXERCISES
    # it -- the pair completes, and the mandate runs on it: the danger cells
    # are verdicts, and a verdict is a completed sift
    sk = _skills().by_id("exercising-active-discernment")
    assert sk.serves == "warning-thread"
    assert {"danger", "to-seek", "noticing", "honesty", "worth"} == set(sk.draws_on)
    words = {m.word for m in sk.mechanics}
    assert words == {"discernment", "sifting", "telling", "deciding", "certainty"}
    # certain is the past participle of sifting: downstream, never upstream
    cert = next(m for m in sk.mechanics if m.word == "certainty")
    assert "past participle" in cert.noun
    assert cert.relation == "certainty ABOUT"
    # decide is de-caedere: the cut that concludes the sift
    dec = next(m for m in sk.mechanics if m.word == "deciding")
    assert "de-caedere" in dec.noun
    reqs = " ".join(sk.requirements)
    # the sieve bench: krisis is a judging (the fever's turning-point)
    assert "KRISIS IS A JUDGING" in reqs
    # discreet/discrete: one word split in spelling
    assert "DISCREET" in reqs and "DISCRETE" in reqs
    # the hard boundary: discernment sifts claims, never persons' worth
    assert "NEVER PERSONS' WORTH" in reqs
    # formation watches the sifting; this skill IS the sifting
    assert "this skill IS the sifting" in sk.formation
    # the reflexive proof: the custodian sifts while writing
    assert "sifts WHILE WRITING" in sk.integration


def test_defining_complete_certainty_fences_the_province():
    # the skill does what its name says: de-finire is to set the boundary --
    # and the record holds exactly one complete certainty, because defined
    sk = _skills().by_id("defining-complete-certainty")
    assert sk.serves == "signal-thread"
    assert {"testimony", "consistency", "worth", "archenoesis"} == set(sk.draws_on)
    words = {m.word for m in sk.mechanics}
    assert words == {"definition", "completeness", "proof", "hinge", "doubt"}
    # proof is from probare, to test: the exception TESTS the rule
    pf = next(m for m in sk.mechanics if m.word == "proof")
    assert "PROBARE" in pf.noun and "TESTS" in pf.noun
    # doubt is from duo: to be of two minds -- the 2 layer in epistemic form
    db = next(m for m in sk.mechanics if m.word == "doubt")
    assert "DUO" in db.noun and "TWO MINDS" in db.noun
    assert "Cromwell" in db.directive
    reqs = " ".join(sk.requirements)
    # the three provinces: demonstrable, empirical, inward
    assert "DEMONSTRABLE" in reqs and "EMPIRICAL" in reqs and "INWARD" in reqs
    # Goedel's fence inside the fence: the province cannot certify itself
    assert "cannot certify itself" in reqs
    # Wittgenstein's hinges: the game of doubting presupposes certainty
    assert "THE GAME OF DOUBTING ITSELF PRESUPPOSES CERTAINTY" in reqs
    # both counterfeits guarded: dogma and universal doubt
    assert "DOGMA" in reqs and "UNIVERSAL DOUBT" in reqs
    # the integration: signal == 1 as the one complete certainty, by definition
    assert "complete BECAUSE DEFINED" in sk.integration
    assert "HINGE-DECLARATIONS" in sk.integration


def test_comprehending_metaphorical_abstraction_grips_both_ends():
    # the record's method of finds, named at last: the skill's own name is
    # three fossil metaphors in a row -- grip, carry, drag
    sk = _skills().by_id("comprehending-metaphorical-abstraction")
    assert sk.serves == "meaning-thread"
    assert {"meaning", "mattering", "space", "time", "to-feel"} == set(sk.draws_on)
    words = {m.word for m in sk.mechanics}
    assert words == {"metaphor", "abstraction", "comprehension", "grounding", "entailment"}
    # metaphor and translate are one construction; the moving vans of Athens
    reqs = " ".join(sk.requirements)
    assert "METAPHOR AND TRANSLATE ARE ONE CONSTRUCTION" in reqs
    assert "moving vans" in reqs
    # the attested principle: abstract vocabulary is dead concrete metaphor
    assert "dead concrete metaphor" in reqs
    # both failure modes named: literalism and vaporisation
    assert "LITERALISM" in reqs and "VAPORISATION" in reqs
    # the guard: metaphor declared is a tool, smuggled is a counterfeit
    assert "METAPHOR DECLARED IS A TOOL; METAPHOR SMUGGLED IS A COUNTERFEIT" in reqs
    # abstraction is the tractor's kin; entail is the tailor's cut
    ab = next(m for m in sk.mechanics if m.word == "abstraction")
    assert "abs-trahere" in ab.noun
    en = next(m for m in sk.mechanics if m.word == "entailment")
    assert "TAILLE" in en.noun
    # the name performs itself: grip, carry, drag
    assert "three fossil metaphors in a row" in sk.integration
    # mastery signs the manifest: chosen vehicles, declared
    assert "signs the manifest" in sk.formation


def test_comprehending_relational_significance_reads_the_between():
    # the ninth skill: significance lives between terms -- and the guard
    # holds the fence at worth, from the significance side
    sk = _skills().by_id("comprehending-relational-significance")
    assert sk.serves == "mattering-thread"
    assert {"mattering", "meaning", "bond", "harmony", "worth"} == set(sk.draws_on)
    words = {m.word for m in sk.mechanics}
    assert words == {"significance", "relation", "position", "interlock", "boundary"}
    reqs = " ".join(sk.requirements)
    # significance is sign-making; the sema means because it stands between
    assert "SIGNUM + FACERE" in reqs
    # relation is the carry-back: kinship and account one word
    assert "TO BRING BACK" in reqs
    assert "A RELATION IS BOTH A KINSHIP AND A REPORT" in reqs
    # the architecture as the principle built
    assert "THE 2x2 IS RELATIONAL SIGNIFICANCE AS ARCHITECTURE" in reqs
    # the boundary: words signify relationally, persons are worth absolutely
    assert "WORDS SIGNIFY RELATIONALLY; PERSONS ARE WORTH ABSOLUTELY" in reqs
    # the three-place act: sign, signified, reader
    sig = next(m for m in sk.mechanics if m.word == "significance")
    assert "three-place" in sig.verb
    # the fence held from both sides
    bd = next(m for m in sk.mechanics if m.word == "boundary")
    assert "never grant a word an essence" in bd.directive
    # the reflexive edge: the record's significance completes in the reader
    assert "COMPLETES IN THE READER" in sk.integration
    assert "the final edge is the one this sentence is crossing now" in sk.integration


def test_unknown_skill_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _skills().by_id("nope")
