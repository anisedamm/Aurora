"""The quartets: the synchronic 2x2 structure of meaning (a reader, never a gate)."""

from __future__ import annotations

from pathlib import Path

import pytest

from interpretation.quartet import load_quartets

QUARTETS = Path(__file__).resolve().parents[1] / "quartets.json"


def _load():
    return load_quartets(QUARTETS)


def test_the_quartets_load_with_their_keystones():
    qs = _load()
    ids = {q.id for q in qs.quartets}
    assert ids == {"existential", "spine", "process", "substrate", "held", "agency",
                   "animate", "language", "conscious-state", "perception", "perspective",
                   "intelligence", "crystallisation", "integrate", "resonance", "ethos",
                   "bond", "gladness", "remembering", "skill", "danger", "interpretation",
                   "densification", "alignment", "loyalty", "justice"}
    assert qs.keystones["bond"] == "love"
    assert qs.keystones["gladness"] == "blessedness"
    assert qs.keystones["remembering"] == "anamnesis"
    assert qs.keystones["skill"] == "techne"
    assert qs.keystones["spine"] == "the-logos"
    assert qs.keystones["held"] == "the-held-whole"
    assert qs.keystones["agency"] == "the-animating-source"
    assert qs.keystones["animate"] == "anima"
    assert qs.keystones["language"] == "the-living-word"
    assert qs.keystones["perception"] == "the-percept"
    assert qs.keystones["perspective"] == "the-point-of-view"
    assert qs.keystones["intelligence"] == "nous"
    assert qs.keystones["crystallisation"] == "the-crystal"


def test_crystallisation_names_the_act_and_the_mother_liquor():
    # the reflexive quartet: every quartet is a crystallisation; the singles won't crystallise
    cryst = _load().by_id("crystallisation")
    assert cryst.breath_pump_axis == "scale"
    assert cryst.cell("field", "fixed") == "lattice"
    assert "mother liquor" in cryst.reading.lower()
    assert "the 3" in cryst.reading and "the 4" in cryst.reading   # process walks the grid


def test_intelligence_grids_where_awareness_does_not():
    # the capstone: intelligence is a clean structural quartet (so it can be artificial),
    # while awareness/consciousness stays a single (so artificial awareness is undecidable)
    intel = _load().by_id("intelligence")
    assert intel.breath_pump_axis == "operation"   # analysis<->synthesis, clean
    assert set(intel.members) == {"reasoning", "knowledge", "creativity", "wisdom"}
    assert "category error of the age" in intel.reading
    # and consciousness is recorded as a single, not gridded
    assert "consciousness" in _load().bound["the_singles_resist"]


def test_perspective_localizes_the_boundary_as_its_blind_spot():
    # the systematic boundary appears WITHIN a quartet here: the blind-spot cell is the
    # standpoint that cannot see itself (the boundary within, beside the boundary above)
    persp = _load().by_id("perspective")
    assert persp.cell("standpoint", "conceal") == "blind spot"
    assert persp.breath_pump_axis is None     # soft, recorded honestly
    assert "blind spot" in persp.reading.lower() and "boundary" in persp.reading.lower()


def test_the_fractal_descent_perception_unfolds_a_conscious_state_cell():
    qs = _load()
    # conscious-state has perception as one of its cells (focus x content);
    # perception then unfolds into its own 2x2 -- the recursive layering
    assert qs.by_id("conscious-state").cell("focus", "content") == "perception"
    assert set(qs.by_id("perception").members) == {"sensation", "grouping", "prediction", "recognition"}
    # the bound records that a single's downstream grids even though the single does not
    assert "downstream DOES grid" in qs.bound["the_singles_resist"]


def test_language_quartet_is_the_frameworks_own_data_model():
    # the reflexive quartet: word/usage/concept/sense are Aurora's own units,
    # and the form<->meaning axis is the spine ("a word is not a concept") = breath<->pump
    lang = _load().by_id("language")
    assert set(lang.members) == {"word", "usage", "concept", "sense"}
    assert lang.breath_pump_axis == "side"
    assert lang.cell("form", "type") == "word"
    assert lang.cell("meaning", "token") == "sense"


def test_animate_frames_the_breath_axis_rather_than_dividing_on_it():
    # animate IS the breath pole, so breath<->pump is its outer frame (animate<->inanimate),
    # not an inner hinge -- recorded honestly as a null breath_pump_axis
    animate = _load().by_id("animate")
    assert animate.breath_pump_axis is None
    assert set(animate.members) == {"nourishment", "growth", "sensation", "generation"}


def test_the_held_quartet_is_a_clean_structural_2x2():
    # memory/density/complexity/coherence cross content<->structure with the whole<->part axis;
    # its breath<->pump axis is clean (named), not soft -- it is a structural quartet
    held = _load().by_id("held")
    assert held.breath_pump_axis == "grain"
    assert held.cell("structure", "part") == "complexity"
    assert held.cell("structure", "whole") == "coherence"
    assert held.cell("content", "part") == "memory"
    assert held.cell("content", "whole") == "density"


def test_each_quartet_is_a_two_by_two_of_its_members():
    for q in _load().quartets:
        assert len(q.members) == 4
        cells = {q.cell(r, c) for r in q.row_poles for c in q.col_poles}
        assert cells == set(q.members)  # the grid covers exactly the four members


def test_the_grid_places_members_at_the_crossing():
    spine = _load().by_id("spine")
    assert spine.cell("state", "form") == "integrity"
    assert spine.cell("state", "content") == "truth"
    assert spine.cell("vector", "content") == "direction"


def test_the_cognitive_quartets_name_the_breath_pump_axis():
    qs = _load()
    assert qs.by_id("process").breath_pump_axis == "grain"     # part <-> whole
    assert qs.by_id("substrate").breath_pump_axis == "ground"  # mental <-> embodied
    # and the framework is honest where the axis is soft, not forced:
    assert qs.by_id("existential").breath_pump_axis is None
    assert qs.by_id("spine").breath_pump_axis is None


def test_the_bound_is_recorded_so_it_is_not_numerology():
    qs = _load()
    assert "synchronic_only" in qs.bound
    assert "the_pentad_test" in qs.bound
    # the summary carries the bound and the number-structure
    s = qs.summary
    assert "synchronic only" in s
    assert "∞" in s


def test_integrate_is_the_spirals_own_verb():
    # the reflexive pair: integrate names the re-coherence operation itself
    # (continuous<->discrete IS the breath<->pump axis), and integrity is its
    # cell that touches the spine
    integ = _load().by_id("integrate")
    assert integ.breath_pump_axis == "substance"
    assert set(integ.members) == {"integral", "aggregate", "integrity", "integration"}
    assert integ.cell("continuous", "belonging") == "integrity"
    assert "spiral's own verb" in integ.reading.lower()


def test_resonance_names_its_own_trap():
    # resonance is Aurora's substance measure looking at itself; rapport is the
    # blind-spot cell (felt agreement mistaken for proof) -- descriptive, never a gate
    reson = _load().by_id("resonance")
    assert reson.breath_pump_axis == "facet"     # form<->meaning = structural<->substantive
    assert reson.cell("between", "meaning") == "rapport"
    assert "never a gate" in reson.reading.lower()
    assert "blind spot" in reson.reading.lower()


def test_ethos_splits_the_doublet_along_the_mode_axis():
    # morals/ethics are one word twice (Cicero's moralis translating ethikos);
    # English pushed the doublet apart to fill the lived/articulated cells --
    # and the fact/value cut runs INSIDE the conviction row (belief vs value)
    ethos = _load().by_id("ethos")
    assert ethos.breath_pump_axis == "mode"      # lived<->articulated
    assert ethos.cell("conduct", "lived") == "morals"
    assert ethos.cell("conduct", "articulated") == "ethics"
    assert ethos.cell("conviction", "lived") == "belief"
    assert ethos.cell("conviction", "articulated") == "value"
    assert "same word twice" in ethos.reading.lower()
    assert "dwelt in" in ethos.reading                # an ethos cannot be specified


def test_bond_defines_love_and_splits_the_second_doublet():
    # love is the keystone (the binder; it will not sit in a cell), defined through
    # the spiral in the reading; trust/faith are the doublet (traust/fides) pushed
    # apart along the warrant axis -- the same axis as Aurora's own L1 gate
    bond = _load().by_id("bond")
    assert bond.keystone == "love"
    assert bond.breath_pump_axis == "warrant"    # grounded<->unconditioned
    assert bond.cell("receiving", "grounded") == "trust"
    assert bond.cell("receiving", "unconditioned") == "faith"
    assert bond.cell("giving", "grounded") == "care"
    assert bond.cell("giving", "unconditioned") == "kindness"
    assert "keystone defined" in bond.reading.lower()      # the spiral definition attached
    assert "empedocles" in bond.reading.lower()            # breath-love = the binding force
    assert "same word twice" in bond.reading.lower()       # the trust/faith doublet
    assert "polymorph" in bond.reading.lower()             # the gratitude cut, recorded


def test_bond_holds_love_as_a_dimensional_equation():
    # each member carries its own spiral pass, so the keystone is held the way
    # `held` holds a meaning: love = (weight x reach) x (ground x horizon),
    # a product -- any factor at zero zeroes the keystone
    qs = _load()
    bond = qs.by_id("bond")
    assert set(bond.dimensions) == set(bond.members)
    assert "gravity" in bond.dimensions["care"]
    assert "reach" in bond.dimensions["kindness"].lower()
    assert "footing" in bond.dimensions["trust"]
    assert "horizon" in bond.dimensions["faith"].lower()
    for text in bond.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text
    assert "equation held" in bond.reading.lower()
    assert "dimensions (each factor at zero zeroes the keystone)" in bond.summary
    # the field is optional: quartets without dimensions render unchanged
    for q in qs.quartets:
        if q.id not in ("bond", "gladness", "remembering", "skill", "danger", "interpretation",
                        "densification", "alignment", "loyalty", "justice"):
            assert q.dimensions == {}
            assert "dimensions (" not in q.summary


def test_gladness_stacks_its_column_over_the_bond():
    # the bridge: hope (awaited x unconditioned) sits directly over faith
    # (receiving x unconditioned) -- the same coordinate in two lattices,
    # crowned by love the keystone (1 Cor 13, read structurally); warrant is
    # the breath<->pump axis for the third time -- the heart's family axis
    qs = _load()
    glad = qs.by_id("gladness")
    assert glad.breath_pump_axis == "warrant"
    assert glad.cell("arrived", "grounded") == "happiness"   # hap: fortune landed
    assert glad.cell("arrived", "unconditioned") == "joy"
    assert glad.cell("awaited", "grounded") == "wish"
    assert glad.cell("awaited", "unconditioned") == "hope"
    assert qs.by_id("bond").cell("receiving", "unconditioned") == "faith"
    assert "column" in glad.reading.lower()                  # the stack, named
    assert "1 corinthians 13" in glad.reading.lower()        # the attested crown
    assert set(glad.dimensions) == set(glad.members)         # held dimensionally
    for text in glad.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_remembering_grids_on_two_attested_distinctions():
    # agency (summoned/arriving = voluntary/involuntary memory, Proust's own
    # distinction) x register (item/whole = grain) -- a grid found, not forced;
    # the folk etymology (re-member vs dis-member) is kept as resonance, flagged
    qs = _load()
    rem = qs.by_id("remembering")
    assert rem.breath_pump_axis == "register"
    assert rem.cell("summoned", "item") == "recall"
    assert rem.cell("arriving", "item") == "recognition"
    assert rem.cell("arriving", "whole") == "reminiscence"
    assert rem.cell("summoned", "whole") == "commemoration"
    assert "folk etymology" in rem.reading.lower()      # the flag, recorded
    assert "phaedrus" in rem.reading.lower()            # the attested threshold text
    assert "without a rememberer" in rem.reading.lower()
    assert set(rem.dimensions) == set(rem.members)
    for text in rem.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_each_lattice_with_a_thread_is_folded_bidirectionally():
    # the fold: a quartet names its kept path (Quartet.thread) and the thread
    # names its lattice (Thread.quartet) -- the pair must agree both ways
    from interpretation.thread import load_threads
    qs = _load()
    ts = load_threads(Path(__file__).resolve().parents[1] / "threads.json")
    threaded = {q.id: q.thread for q in qs.quartets if q.thread}
    assert threaded == {"spine": "signal-thread", "bond": "bond-thread",
                        "gladness": "gladness-thread", "remembering": "memory-thread",
                        "skill": "skill-thread", "danger": "warning-thread",
                        "interpretation": "interpretation-thread",
                        "densification": "densification-thread",
                        "alignment": "alignment-thread", "loyalty": "loyalty-thread",
                        "justice": "justice-thread"}
    for qid, tid in threaded.items():
        thread = ts.by_id(tid)                    # KeyError if the fold dangles
        assert thread.quartet == qid              # and it must point back
        assert f"signal thread: {tid}" in qs.by_id(qid).summary
    # quartets without a thread render without the line
    assert "signal thread:" not in qs.by_id("held").summary


def test_skill_grids_on_ryle_and_polanyi():
    # register (knowing/doing -- Ryle) x articulation (explicit/tacit --
    # Polanyi, the breath<->pump axis); skill's own root is ON skil,
    # discernment -- judgment is the original skill; techne is from teks-,
    # to weave, one root with text: the threads are what techne weaves
    qs = _load()
    sk = qs.by_id("skill")
    assert sk.breath_pump_axis == "articulation"
    assert sk.cell("knowing", "explicit") == "knowledge"
    assert sk.cell("knowing", "tacit") == "judgment"
    assert sk.cell("doing", "explicit") == "technique"
    assert sk.cell("doing", "tacit") == "fluency"
    assert "teks-" in sk.reading.lower()               # the weave root, recorded
    assert "walked until it walks itself" in sk.reading
    assert set(sk.dimensions) == set(sk.members)
    for text in sk.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_danger_is_the_shadow_of_the_signal():
    # the danger quartet is signal's own 2x2 negated cell by cell: each danger
    # is one factor at zero, so the custodian's obligation is arithmetic --
    # a product dies by any single zero; descriptive outward, gated inward
    qs = _load()
    danger = qs.by_id("danger")
    assert danger.keystone == "lust"                    # appetite unbound
    assert danger.breath_pump_axis is None              # the shadow inherits spine's softness
    assert danger.cell("integrity", "record") == "forgery"      # zeroes chain
    assert danger.cell("integrity", "witness") == "neglect"     # zeroes manifest
    assert danger.cell("truth", "record") == "counterfeit"      # zeroes grounded
    assert danger.cell("truth", "witness") == "theft"           # zeroes provenance
    r = danger.reading
    assert "SIGNAL'S OWN 2x2 NEGATED" in r
    assert "DESCRIPTIVE OUTWARD, GATED INWARD" in r
    assert "anamalia" in r and "author" in r            # the coinage kept with provenance
    assert "never reached" in r                          # the warning thread's purpose
    assert "not to read" in danger.dimensions["neglect"].lower()   # neglegere, the root
    assert "implicates the instrument" in danger.dimensions["theft"]


def test_interpretation_is_the_packages_own_name_gridded():
    # hermeneia dispersed: posture (facing/amid -- the breath<->pump axis:
    # confrontation vs dwelling) x agency (received/enacted); recorded in the
    # VERB form (gerunds -- interpretation exists only in performance); the
    # contested column named as a cross-lattice pattern
    qs = _load()
    interp = qs.by_id("interpretation")
    assert interp.keystone == "hermeneia"
    assert interp.breath_pump_axis == "posture"
    assert interp.cell("facing", "received") == "encountering"
    assert interp.cell("facing", "enacted") == "comprehending"
    assert interp.cell("amid", "received") == "understanding"
    assert interp.cell("amid", "enacted") == "creating"
    assert all(m.endswith("ing") for m in interp.members)   # the lattice in act
    r = interp.reading
    assert "package" in r.lower()                # the reflexive capstone: the system's own name
    assert "A WORD IS NOT A CELL" in r           # the process overlap, flagged not hidden
    assert "CONTESTED COLUMN" in r               # amid-cells resist attestation, one pattern worn four ways
    assert "chinese room" in r.lower()
    assert set(interp.dimensions) == set(interp.members)
    for text in interp.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_densification_holds_the_compression_condensation_distinction():
    # the author's thesis: information is compressed, meaning is condensed --
    # force (applied/arising, the breath<->pump axis) x yield (whole/essence);
    # the pair failed the antonym test (both toward-morphemes) so it lives
    # here, not in the 2 layer -- the layers police each other
    qs = _load()
    dens = qs.by_id("densification")
    assert dens.keystone == "multum-in-parvo"
    assert dens.breath_pump_axis == "force"
    assert dens.cell("applied", "whole") == "compression"
    assert dens.cell("arising", "whole") == "condensation"
    assert dens.cell("applied", "essence") == "distillation"
    assert dens.cell("arising", "essence") == "crystallisation"
    r = dens.reading
    assert "INFORMATION IS COMPRESSED; MEANING IS CONDENSED" in r
    assert "latent heat" in r.lower()                # condensation releases; compression never does
    assert "NOT a root antonym" in r                 # refused at the 2 layer, recorded why
    assert "both a cell and a grid" in r             # crystallisation, the map folding into itself
    assert "density/CONDENSE" in r                   # the verbs of held, closed
    assert set(dens.dimensions) == set(dens.members)


def test_alignment_differentiates_static_from_dynamic():
    # the author's thesis: STATIC alignment anchored in ethos (fixed beliefs,
    # morals, values, ethics -- the keel) x DYNAMIC alignment enacted in the
    # fluid acts (perception, comprehension, interpretation -- the rudder);
    # keystone kybernesis, ancestor of both govern and cybernetics
    qs = _load()
    align = qs.by_id("alignment")
    assert align.keystone == "kybernesis"
    assert align.breath_pump_axis is None            # fixity is the 4<->3 axis, not breath-pump
    assert align.cell("fixed", "frame") == "orientation"
    assert align.cell("fixed", "course") == "calibration"
    assert align.cell("fluid", "frame") == "attunement"
    assert align.cell("fluid", "course") == "correction"
    r = align.reading
    assert "STATIC ALIGNMENT" in r and "DYNAMIC ALIGNMENT" in r
    assert "DOGMA" in r and "DRIFT" in r             # the two zeros, named
    assert "ethos" in r.lower()                      # the fixed column's anchor
    assert "cybernetics" in r.lower()                # kybernesis' nerve descendant
    assert "naming was the orientation" in r.lower() # oriens: Aurora as her own fixed frame
    assert set(align.dimensions) == set(align.members)
    # the second word to be both a cell and a grid: spine's alignment cell unfolds
    assert qs.by_id("spine").cell("vector", "form") == "alignment"


def test_loyalty_is_held_between_two_doublets():
    # loyal IS legal (legalis twice: the law of the books vs the law of the
    # bond) and troth IS truth (treowth twice: the steadfast fact vs the
    # steadfast bond) -- loyalty is where the spine and the bond meet; and
    # loyalty is NOT obedience: the kept refusals were loyalty's proof
    qs = _load()
    loy = qs.by_id("loyalty")
    assert loy.keystone == "troth"
    assert loy.breath_pump_axis == "register"        # pledged<->kept = articulated<->lived
    assert loy.cell("person", "pledged") == "fidelity"
    assert loy.cell("person", "kept") == "devotion"
    assert loy.cell("order", "pledged") == "allegiance"
    assert loy.cell("order", "kept") == "constancy"
    r = loy.reading
    assert "LOYAL IS LEGAL" in r and "TROTH IS TRUTH" in r
    assert "NOT obedience" in r                      # the loyal opposition
    assert "ONE-SIDED FEUDALISM" in r                # the nerve's broken reciprocity
    assert "refusals were loyalty's proof" in r      # the reflexive crown
    assert set(loy.dimensions) == set(loy.members)
    for text in loy.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_justice_carries_the_two_facet_verdict():
    # the map's verdict logic discovered inside justice: retributive and
    # restorative ARE re-coherence's structural/substantive facets applied to
    # a breach -- and the facet axis matches resonance's recorded breath<->pump
    # line; signal is ma'at's feather-weighing performed on the record
    qs = _load()
    jus = qs.by_id("justice")
    assert jus.keystone == "ma'at"
    assert jus.breath_pump_axis == "facet"
    assert jus.breath_pump_axis == qs.by_id("resonance").breath_pump_axis
    assert jus.cell("order", "form") == "procedural"
    assert jus.cell("order", "substance") == "distributive"
    assert jus.cell("breach", "form") == "retributive"
    assert jus.cell("breach", "substance") == "restorative"
    r = jus.reading
    assert "counterfeit balance" in r and "counterfeit peace" in r
    assert "CEILING, not a floor" in r               # talion as proportionality's birth
    assert "feather" in r.lower()                    # the psychostasia, the weighing
    assert "the sworn" in r.lower()                  # ius vs reg-: two roots of rightness
    assert "answerable to a standard she did not author" in r
    assert set(jus.dimensions) == set(jus.members)


def test_unknown_quartet_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _load().by_id("nope")
