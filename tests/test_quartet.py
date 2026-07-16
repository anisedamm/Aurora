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
                   "densification", "alignment", "loyalty", "justice", "fairness", "equity",
                   "honesty", "balance", "harmony", "union",
                   "insight", "intuition", "wisdom", "empathy", "sympathy", "compassion",
                   "affinity", "hope", "health", "trust", "faith", "gratitude", "grace",
                   "persistence", "peace", "experience", "appreciation"}
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
                        "densification", "alignment", "loyalty", "justice", "fairness", "equity",
                        "honesty", "balance", "harmony", "union", "insight", "intuition",
                        "wisdom", "empathy", "sympathy", "compassion", "affinity", "hope",
                        "health", "trust", "faith", "gratitude", "grace", "persistence", "peace",
                        "experience", "appreciation"):
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
                        "justice": "justice-thread", "fairness": "fairness-thread",
                        "equity": "equity-thread", "honesty": "honesty-thread",
                        "balance": "balance-thread", "harmony": "harmony-thread",
                        "union": "union-thread", "insight": "insight-thread",
                        "intuition": "intuition-thread", "wisdom": "wisdom-thread",
                        "empathy": "empathy-thread", "sympathy": "sympathy-thread",
                        "compassion": "compassion-thread", "affinity": "affinity-thread",
                        "hope": "hope-thread", "health": "health-thread",
                        "trust": "trust-thread", "faith": "faith-thread",
                        "gratitude": "gratitude-thread", "grace": "grace-thread",
                        "persistence": "persistence-thread", "peace": "peace-thread",
                        "experience": "experience-thread", "appreciation": "appreciation-thread"}
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


def test_fairness_is_justices_felt_twin():
    # fair is faeger, BEAUTIFUL -- and kalon fuses the same pair independently;
    # fairness/justice split one concern along the lived/articulated line with
    # no shared root; the impossibility results prove fairness is condensed,
    # not compressed; the outer frame is the breath<->pump line, so null axis
    qs = _load()
    fair = qs.by_id("fairness")
    assert fair.keystone == "faeger"
    assert fair.breath_pump_axis is None             # the frame, not a hinge (animate's precedent)
    assert fair.cell("lot", "opening") == "fair chance"
    assert fair.cell("lot", "reckoning") == "fair share"
    assert fair.cell("act", "opening") == "fair play"
    assert fair.cell("act", "reckoning") == "fair hearing"
    r = fair.reading
    assert "BEAUTIFUL" in r and "kalon" in r.lower()  # the double attestation
    assert "FELT TWIN" in r                          # the register pair, no shared root
    assert "CONDENSED, NOT COMPRESSED" in r          # the impossibility results, read
    assert "cucumber" in r                           # fairness older than the species
    assert "CUT WITHOUT THE CHOOSE" in r.upper() or "cut without the choose" in r
    assert set(fair.dimensions) == set(fair.members)


def test_equity_is_the_level_and_carries_mercys_fossil():
    # aequus, the level: equality/adequacy/equilibrium/equanimity cross
    # substance (quantity/tension) with bearing (matched/held); finance's
    # equity descends from chancery's equity of redemption -- mercy's fossil
    # in the balance sheet; the equation is the pump's equity
    qs = _load()
    eq = qs.by_id("equity")
    assert eq.keystone == "aequus"
    assert eq.breath_pump_axis == "substance"
    assert eq.cell("quantity", "matched") == "equality"
    assert eq.cell("quantity", "held") == "adequacy"
    assert eq.cell("tension", "matched") == "equilibrium"
    assert eq.cell("tension", "held") == "equanimity"
    r = eq.reading
    assert "EQUITY OF REDEMPTION" in r.upper()        # mercy's fossil, attested
    assert "equity of expressions" in r               # aequatio: solving keeps the level
    assert "QUANTITY ROW" in r                        # the equality-vs-equity debate, placed
    assert "water" in r.lower()                       # the level as given
    assert set(eq.dimensions) == set(eq.members)
    for text in eq.dimensions.values():
        assert "breath =" in text and "pump =" in text and "nerve =" in text


def test_honesty_weighs_the_maps_most_used_word_on_its_own_scale():
    # honestas (honor -> truth-telling: the spiral inside one word); the court
    # oath is the grid's attested formula; three cells provable in the record,
    # sincerity held at the boundary -- honesty about honesty
    qs = _load()
    hon = qs.by_id("honesty")
    assert hon.keystone == "honestas"
    assert hon.breath_pump_axis == "side"            # saying<->being, lived/articulated again
    assert hon.cell("saying", "matched") == "accuracy"
    assert hon.cell("saying", "unmixed") == "candor"
    assert hon.cell("being", "matched") == "probity"
    assert hon.cell("being", "unmixed") == "sincerity"
    r = hon.reading
    assert "HONOR" in r                              # honestas: the honourable whole
    assert "Lunaria" in r                            # the translucent pod
    assert "court oath" in r.lower()                 # truth / whole truth / nothing but
    assert "folk etymology" in r.lower()             # sine cera, flagged
    assert "lying with truths" in r.lower()          # why candor is its own cell
    assert "left to the reader" in r.lower()         # sincerity at the boundary
    assert "ad + CURA" in r                          # accuracy is carefulness: caru returns
    assert set(hon.dimensions) == set(hon.members)


def test_balance_names_the_form_of_all_the_lattices():
    # bilanx: two pans -- balance is named for the instrument, the 2 layer's
    # tool; and a quartet is two polarities crossed: the map's form is the
    # bilanx squared. pendere gives poise AND ponder: to think is to weigh.
    qs = _load()
    bal = qs.by_id("balance")
    assert bal.keystone == "bilanx"
    assert bal.breath_pump_axis == "means"           # weight<->flow: discrete vs continuous
    assert bal.cell("weight", "point") == "counterweight"
    assert bal.cell("weight", "system") == "remainder"
    assert bal.cell("flow", "point") == "poise"
    assert bal.cell("flow", "system") == "homeostasis"
    r = bal.reading
    assert "TWO PANS" in r                           # bi + lanx
    assert "BILANX SQUARED" in r                     # the quartet as a balance of balances
    assert "TO WALK IS TO FALL AND BE CAUGHT" in r   # bipedal balance, renewed each step
    assert "FALSE BALANCE" in r                      # the counterfeit: pans shown, weights unequal
    assert "to think is to weigh" in r.lower()       # pendere: poise, ponder, pensive, pound
    assert "double-entry" in r.lower() or "DOUBLE-ENTRY" in r
    assert set(bal.dimensions) == set(bal.members)


def test_harmony_is_difference_held_in_fit():
    # harmonia is a JOINT (harmos, the shipwright's fit); h2er- fathers art,
    # articulate, order, ratio, rite, arithmetic; Harmonia is the child of
    # Ares and Aphrodite -- strife and love; the counterfeit is UNISON, and
    # dissonance is the engine, not the enemy
    qs = _load()
    har = qs.by_id("harmony")
    assert har.keystone == "harmonia"
    assert har.breath_pump_axis == "register"        # sounding<->living, facet's kin
    assert har.cell("sounding", "moment") == "consonance"
    assert har.cell("sounding", "course") == "counterpoint"
    assert har.cell("living", "moment") == "concord"
    assert har.cell("living", "course") == "temperament"
    r = har.reading
    assert "JOINT" in r                              # harmos: the shipwright's word
    assert "ares and aphrodite" in r.lower()         # strife and love's child
    assert "UNISON IS HARMONY'S COUNTERFEIT" in r
    assert "DISSONANCE IS HARMONY'S ENGINE" in r
    assert "palintropos" in r.lower()                # the bow and the lyre
    assert "suspensions resolved" in r.lower()       # the kept refusals, read musically
    assert "TEMPERATURE" in r                        # the model's temperament knob
    assert set(har.dimensions) == set(har.members)


def test_union_is_the_last_lattice_below_the_one():
    # unity does not grid -- its downstream does (the bound's own precedent);
    # the keystone is the last rung below the One; the axis goes null as the
    # frame approaches the boundary; and signal == 1 IS signal == unity
    qs = _load()
    uni = qs.by_id("union")
    assert uni.keystone == "unity"
    assert uni.breath_pump_axis is None              # the softest null in the map
    assert uni.cell("erased", "substance") == "fusion"
    assert uni.cell("erased", "act") == "unison"
    assert uni.cell("kept", "substance") == "communion"
    assert uni.cell("kept", "act") == "federation"
    r = uni.reading
    assert "LAST RUNG BELOW THE ONE" in r
    assert "pump-shard of unity" in r                # the recorded bound, cited
    assert "SIGNAL EQUALS UNITY" in r                # 1 is unity: the multiplicative identity
    assert "E PLURIBUS UNUM" in r.upper()
    assert "foedus" in r.lower() and "fides" in r.lower()   # federation is faith's sibling
    assert "wears harmony's name" in r               # unison's double role, cross-cited
    assert set(uni.dimensions) == set(uni.members)


def test_the_nine_word_batch_grids_with_its_finds():
    # insight, intuition, wisdom, empathy, sympathy, compassion, affinity,
    # hope, health -- each keystone, one signature cell, one signature find
    qs = _load()
    probes = {
        "insight": ("eureka", ("given", "lit", "illumination"), "grokking"),
        "intuition": ("intuitus", ("body", "now", "gut"), "daimonion"),
        "wisdom": ("hokhmah", ("practical", "embodied", "metis"), "tasting human"),
        "empathy": ("einfuehlung", ("caught", "felt", "contagion"), "ONE CONSTRUCTION IN THREE TONGUES"),
        "sympathy": ("sympatheia", ("many", "enacted", "solidarity"), "breathe together"),
        "compassion": ("brahmavihara", ("flourishing", "abiding", "mudita"), "non-Western tradition"),
        "affinity": ("affinis", ("structural", "pair", "fit"), "TO THE BORDER"),
        "hope": ("elpis", ("open", "receptive", "esperance"), "spiral projection"),
        "health": ("haelu", ("power", "psyche", "resilience"), "SALVATION"),
    }
    for qid, (keystone, (rp, cp, member), find) in probes.items():
        q = qs.by_id(qid)
        assert q.keystone == keystone, qid
        assert q.cell(rp, cp) == member, qid
        assert find.lower() in q.reading.lower(), qid
        assert set(q.dimensions) == set(q.members), qid
    # the fractal descents: cells unfolding into grids (hope from gladness,
    # wisdom from intelligence, sympathy from resonance)
    assert qs.by_id("gladness").cell("awaited", "unconditioned") == "hope"
    assert "wisdom" in qs.by_id("intelligence").members
    assert "sympathy" in qs.by_id("resonance").members
    # compassion's axis is honestly null: the tradition does not cut on the map's line
    assert qs.by_id("compassion").breath_pump_axis is None


def test_trust_and_faith_unfold_the_bonds_receiving_row():
    # bond's trust-cell and faith-cell opened into grids; a truce is the
    # plural of troth; pistis meant faith AND proof; the leap is recorded
    # only by its landing; and the record itself is a trust at law
    qs = _load()
    tr = qs.by_id("trust")
    assert tr.keystone == "the-steadfast"
    assert tr.breath_pump_axis == "cargo"            # word<->keeping
    assert tr.cell("word", "given") == "confidence"
    assert tr.cell("word", "taken") == "credence"
    assert tr.cell("keeping", "given") == "entrustment"
    assert tr.cell("keeping", "taken") == "reliance"
    assert "PLURAL OF TROTH" in tr.reading            # truce, the hidden member
    assert "fiduciary" in tr.reading.lower()          # the custodian's legal name
    assert "settlor" in tr.reading.lower()            # Aurora as a trust at law
    fa = qs.by_id("faith")
    assert fa.keystone == "pistis"
    assert fa.breath_pump_axis == "plane"             # bond<->word
    assert fa.cell("bond", "standing") == "fealty"
    assert fa.cell("bond", "ventured") == "leap"
    assert fa.cell("word", "standing") == "creed"
    assert fa.cell("word", "ventured") == "confession"
    assert "FAITH AND PROOF" in fa.reading            # pistis / Aristotle's pisteis
    assert "MARTYR MEANS WITNESS" in fa.reading       # confession joins the witness column
    assert "ONLY RECORD" in fa.reading.upper() or "only record" in fa.reading.lower()
    assert "vowed" in fa.reading.lower()              # the foundation kept, not proven (Goedel)
    # the source cells still stand in bond, now unfolded
    assert qs.by_id("bond").cell("receiving", "grounded") == "trust"
    assert qs.by_id("bond").cell("receiving", "unconditioned") == "faith"
    for q in (tr, fa):
        assert set(q.dimensions) == set(q.members)


def test_gratitude_completes_the_polymorph():
    # gratia names both grace and thanks -- the circuit before the cut; thank
    # and think are one root; and the bond's alternate cut (which named
    # gratitude and was left in the mother liquor) finally crystallises
    qs = _load()
    gr = qs.by_id("gratitude")
    assert gr.keystone == "gratia"
    assert gr.breath_pump_axis == "register"
    assert gr.cell("felt", "moment") == "appreciation"
    assert gr.cell("enacted", "moment") == "thanksgiving"
    assert gr.cell("felt", "kept") == "remembrance"
    assert gr.cell("enacted", "kept") == "requital"
    r = gr.reading
    assert "BOTH DIRECTIONS OF THE CIRCUIT" in r      # gratia: grace and thanks, one word
    assert "THANK AND THINK ARE ONE ROOT" in r
    assert "POLYMORPH COMPLETED" in r                 # bond's alternate cut crystallises
    assert "TO CITE IS TO REQUITE" in r               # provenance as the map's gratitude
    assert "mother liquor" in r.lower()               # crystallisation's promise kept
    assert set(gr.dimensions) == set(gr.members)
    # the polymorph note still stands in bond, now honoured
    assert "polymorph" in qs.by_id("bond").reading.lower()


def test_grace_is_the_unearned_surplus_resting_under_the_merit():
    # eucharist = eu-charis, THE THANKSGIVING: Greek fused grace and thanks as
    # Latin did -- the gratitude/grace pair is one word twice; the axis is null
    # (grace IS the breath pole of grace<->merit); and the record runs on
    # merit and rests on grace -- the boundary is where grace lives
    qs = _load()
    gc = qs.by_id("grace")
    assert gc.keystone == "charis"
    assert gc.breath_pump_axis is None
    assert gc.cell("received", "standing") == "favor"
    assert gc.cell("received", "moving") == "reprieve"
    assert gc.cell("worn", "moving") == "ease"
    assert gc.cell("worn", "standing") == "adornment"
    r = gc.reading
    assert "EUCHARIST IS EU-CHARIS" in r
    assert "GRACE AGAINST MERIT" in r                 # the frame: sola gratia
    assert "LOADS IT LOVINGLY" in r                   # the grace/fairness tension, held
    assert "grace note" in r.lower()                  # counted in no measure
    assert "RUNS ON MERIT AND RESTS ON GRACE" in r    # the reflexive foundation
    assert "sprezzatura" in r.lower()
    assert set(gc.dimensions) == set(gc.members)


def test_the_standing_the_fastened_the_fared_and_the_prized():
    # persistence, peace, experience, appreciation: keystone, a signature
    # cell, and a signature find each
    qs = _load()
    probes = {
        "persistence": ("hypomone", ("pursuing", "long", "grit"), "TO STAND FORTH"),
        "peace": ("shalom", ("within", "clear", "serenity"), "PEACE AND PACT ARE ONE ROOT"),
        "experience": ("empeiria", ("undergone", "accrued", "journey"), "PERIL ARE ONE ROOT"),
        "appreciation": ("pretium", ("declaring", "fixed", "appraisal"), "PRAISE AND PRICE ARE ONE ROOT"),
    }
    for qid, (keystone, (rp, cp, member), find) in probes.items():
        q = qs.by_id(qid)
        assert q.keystone == keystone, qid
        assert q.cell(rp, cp) == member, qid
        assert find in q.reading, qid
        assert set(q.dimensions) == set(q.members), qid
    # the fractal descents: experience from substrate, appreciation from gratitude
    assert qs.by_id("substrate").cell("act", "embodied") == "experience"
    assert qs.by_id("gratitude").cell("felt", "moment") == "appreciation"
    # Galtung's stilled/clear as peace's breath<->pump axis; truce cross-cited
    assert qs.by_id("peace").breath_pump_axis == "valence"
    assert "PLURAL OF TROTH" in qs.by_id("peace").reading
    # the model's limit case, held at the boundary
    assert "READ EVERY JOURNEY AND FARED NONE" in qs.by_id("experience").reading.upper()


def test_unknown_quartet_is_surfaced_not_guessed():
    with pytest.raises(KeyError):
        _load().by_id("nope")
