"""The three layers: attestation gates, reading describes, drift catches anachronism."""

from __future__ import annotations

from pathlib import Path

from interpretation.glossary import Usage, load_glossary
from interpretation.reading import attest, drift, read

GLOSSARY = Path(__file__).resolve().parents[1] / "glossary.json"


# --- L1: attestation --------------------------------------------------------

def test_a_real_usage_is_attested():
    g = load_glossary(GLOSSARY)
    assert attest(g.usage("rev-1688")).ok
    assert attest(g.usage("rev-copernicus")).ok       # tolerates Latin inflection


def test_a_usage_whose_word_is_absent_is_not_attested():
    bogus = Usage(
        id="x", word="revolution",
        quotation="a treatise on the equality of conditions",
        citation="somewhere, 1800", year=1800,
    )
    result = attest(bogus)
    assert not result.ok
    assert any("does not appear" in r for r in result.reasons)


def test_a_usage_without_a_citation_is_not_attested():
    bogus = Usage(id="x", word="revolution", quotation="the revolution came", citation="")
    assert not attest(bogus).ok


# --- L2: reading ------------------------------------------------------------

def test_read_describes_the_sense_without_judging():
    g = load_glossary(GLOSSARY)
    r = read(g.usage("rev-1688"), "political-restoration", g.lattice_for_usage("rev-1688"))
    assert r.sense_label.startswith("return")
    assert "*a* reading" in r.summary and "one true meaning" in r.summary


# --- L3: anachronism drift --------------------------------------------------

def test_reading_a_later_sense_into_an_earlier_usage_is_anachronism():
    g = load_glossary(GLOSSARY)
    # 1688's "revolution" read in the post-1789 sense of irreversible rupture.
    d = drift(g.usage("rev-1688"), "irreversible-rupture", g.lattice_for_usage("rev-1688"))
    assert d.anachronistic
    assert d.anachronism_years == 1789 - 1689


def test_a_contemporary_sense_does_not_drift():
    g = load_glossary(GLOSSARY)
    d = drift(g.usage("rev-1789"), "irreversible-rupture", g.lattice_for_usage("rev-1789"))
    assert not d.anachronistic
    assert d.anachronism_years == 0


def test_an_earlier_sense_is_in_period_not_anachronistic():
    g = load_glossary(GLOSSARY)
    # The 1688 usage read in the restoration sense (available by 1660): in period.
    d = drift(g.usage("rev-1688"), "political-restoration", g.lattice_for_usage("rev-1688"))
    assert not d.anachronistic
    assert d.archaism_years == 1689 - 1660


def test_democracy_anachronism_spans_millennia():
    g = load_glossary(GLOSSARY)
    d = drift(g.usage("dem-aristotle"), "popular-self-government",
              g.lattice_for_usage("dem-aristotle"))
    assert d.anachronistic
    assert d.anachronism_years == 1780 - (-350)
