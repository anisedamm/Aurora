"""The synonym web: nearness recorded honestly -- no true synonyms."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from interpretation.quartet import load_quartets
from interpretation.synonym import VALID_KINDS, load_synonyms

ROOT = Path(__file__).resolve().parents[1]
SYNONYMS = ROOT / "synonyms.json"
QUARTETS = ROOT / "quartets.json"


def _syn():
    return load_synonyms(SYNONYMS)


def test_the_links_load_with_kind_and_differentia():
    sy = _syn()
    assert len(sy.links) >= 12
    for l in sy.links:
        assert l.kind in VALID_KINDS
        # the first law enforced: every link records what keeps the pair apart
        assert l.differentia.strip()
        assert l.derivation and l.aurora
    ids = {l.id for l in sy.links}
    # the record's own differentiations are in the web
    for expected in ("trust-faith", "morals-ethics", "respect-regard",
                     "forgive-pardon", "worth-value", "constancy-stability",
                     "royal-regal", "love-charity"):
        assert expected in ids


def test_the_first_law_is_enforced_by_the_loader(tmp_path):
    # a link without a differentia is refused: no true synonyms
    bad = {"links": [{"id": "x-y", "a": "x", "b": "y", "kind": "near",
                      "differentia": "  "}]}
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="first law"):
        load_synonyms(p)
    # and an unnamed kind of nearness is surfaced, not guessed
    bad2 = {"links": [{"id": "x-y", "a": "x", "b": "y", "kind": "vibes",
                       "differentia": "real"}]}
    p2 = tmp_path / "bad2.json"
    p2.write_text(json.dumps(bad2), encoding="utf-8")
    with pytest.raises(ValueError, match="typology"):
        load_synonyms(p2)


def test_the_kinds_carry_the_attested_typology():
    sy = _syn()
    kinds = {l.kind for l in sy.links}
    # register (the strata), calque (built twice), doublet (one root twice),
    # near (nuance), scalar (intensity) all present in the web
    assert kinds == set(VALID_KINDS)
    # the calques are the record's founding finds
    assert sy.by_id("morals-ethics").kind == "calque"
    assert sy.by_id("forgive-pardon").kind == "calque"
    # royal/regal: one root arrived twice
    assert sy.by_id("royal-regal").kind == "doublet"
    # worth/value: the strata are the regimes
    assert sy.by_id("worth-value").kind == "register"


def test_the_web_is_checked_against_the_record():
    sy = _syn()
    qs = load_quartets(QUARTETS)
    w = sy.web(qs)
    # most links stand with both ends in the lattice corpus
    assert len(w["live"]) >= 10
    # and what reaches beyond is reported, not hidden
    assert len(w["live"]) + len(w["beyond"]) == len(sy.links)
    live_ids = {l.id for l in w["live"]}
    assert "trust-faith" in live_ids and "meaning-sense" in live_ids


def test_the_chain_is_a_walk_not_a_proof():
    sy = _syn()
    # a walk exists where links join: trust -> faith is one step
    assert sy.chain("trust", "faith") == ["trust", "faith"]
    # longer walks accumulate distance (non-transitivity: nearness drifts)
    path = sy.chain("empathy", "compassion")
    assert path[0] == "empathy" and path[-1] == "compassion"
    assert len(path) >= 3            # via sympathy: the drift is countable
    # absence is recorded, not bridged
    with pytest.raises(KeyError):
        sy.chain("trust", "royal")


def test_the_bound_carries_the_three_laws():
    sy = _syn()
    assert "NO TRUE SYNONYMS SURVIVE" in sy.bound["the_first_law"]
    assert "differentia".upper() in sy.bound["the_first_law"].upper()
    assert "THE STRATA ARE THE REGIMES" in sy.bound["the_register_stratification"]
    assert "non-transitive" in sy.bound["the_non_transitivity"]
    assert "two relations" in sy.bound["the_webs_two_axes"]


def test_the_summary_carries_the_web_and_the_laws():
    sy = _syn()
    s = sy.summary(load_quartets(QUARTETS))
    assert "trust ~ faith" in s
    assert "differentia" in s
    assert "live in the" in s
    assert "never a gate" in s


def test_unknown_link_and_word_are_surfaced_not_guessed():
    sy = _syn()
    with pytest.raises(KeyError):
        sy.by_id("nope")
    with pytest.raises(KeyError):
        sy.neighbors("nope")
