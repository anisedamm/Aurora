"""Seed the interpretation ledger from the authored glossary.

Builds `interpretation_ledger.jsonl` and `MANIFEST.md` from scratch: it imprints
the framework, the thought-flow journal, the glossary map, then each concept, its
attested usages, and one reading per usage - a weighted reading for a breath-era
conceptual sign, a sense reading for a pump-era phonetic word - plus one recorded
*foil*: the labrys read phonetically, so the published record shows the framework
catching a phonetic projection. Every record is authored by **anise.damm**,
anchored to the current git commit. Re-runnable: it rewrites the ledger.

    python scripts/seed.py            # anchor to HEAD
    python scripts/seed.py <git-sha>  # anchor to a specific commit
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from interpretation.glossary import load_glossary           # noqa: E402
from interpretation.imprint import DEFAULT_AUTHOR, Imprinter  # noqa: E402
from interpretation.ledger import Ledger                    # noqa: E402
from interpretation.manifest import write_manifest          # noqa: E402
from interpretation.weighting import WeightedField          # noqa: E402

LEDGER = ROOT / "interpretation_ledger.jsonl"
GLOSSARY = ROOT / "glossary.json"
MANIFEST = ROOT / "MANIFEST.md"

# The in-period sense each seeded *phonetic* usage is read in (none anachronistic).
PHONETIC_READINGS = {
    "rev-copernicus": "celestial-return",
    "rev-1688": "political-restoration",
    "rev-1789": "irreversible-rupture",
    "dem-aristotle": "mob-rule",
    "dem-tocqueville": "popular-self-government",
    "theogony": "olympian",
}


def git_head() -> str | None:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
        return sha or None
    except (subprocess.CalledProcessError, OSError):
        return None


def main() -> int:
    anchor_sha = sys.argv[1] if len(sys.argv) > 1 else git_head()
    anchor = f"git:{anchor_sha}" if anchor_sha else None

    if LEDGER.exists():
        LEDGER.unlink()
    g = load_glossary(GLOSSARY)
    imp = Imprinter(Ledger(LEDGER))

    def imprint(**kw):
        kw.setdefault("author", DEFAULT_AUTHOR)
        kw.setdefault("external_anchor", anchor)
        return imp.imprint(**kw)

    imprint(artifact_id="language-framework", title="Conceptual history as language interpretation",
            text=(ROOT / "README.md").read_text(encoding="utf-8"), kind="framework",
            license="Apache-2.0")
    imprint(artifact_id="thought-flow", title="Thought flow — the living reasoning journal",
            text=(ROOT / "docs/thought-flow.md").read_text(encoding="utf-8"),
            kind="reasoning", source="collaboration", source_actor="claude",
            parents=["language-framework"])
    imprint(artifact_id="glossary-map", title="The authored glossary of conceptual histories",
            text=GLOSSARY.read_text(encoding="utf-8"), kind="concept",
            parents=["language-framework"])
    imprint(artifact_id="lexicon-map", title="The phonetic lexicon traced over time",
            text=(ROOT / "lexicon.json").read_text(encoding="utf-8"), kind="concept",
            regime="pump", parents=["language-framework"])
    imprint(artifact_id="relations-map",
            title="The authored map of meaning-connections (antonyms + synonyms)",
            text=(ROOT / "relations.json").read_text(encoding="utf-8"), kind="concept",
            parents=["language-framework"])
    imprint(artifact_id="invariants-map",
            title="Proposed invariants — claims of universal truth (the dimensionless)",
            text=(ROOT / "invariants.json").read_text(encoding="utf-8"), kind="concept",
            parents=["language-framework"])

    for c in g.concepts.values():
        cid = f"concept-{c.id}"
        is_symbol = c.regime == "breath" and not c.lattice.senses
        summary = "; ".join(f"{s.label} ({s.period})" for s in c.lattice.senses.values())
        imprint(artifact_id=cid, title=f"Concept: {c.name}", concept=c.id,
                kind="symbol" if is_symbol else "concept", regime=c.regime or None,
                parents=["glossary-map"],
                text=f"{c.name}: {c.gloss}" + (f"\nSenses: {summary}" if summary else ""))
        for u in sorted(c.usages.values(), key=lambda u: u.year):
            imprint(artifact_id=u.id, title=f"Usage: {u.citation or u.artifact}", concept=c.id,
                    kind="usage", word=u.word, citation=u.citation or u.artifact, period=u.period,
                    year=u.year, regime=u.regime, mode=u.mode,
                    weights=(dict(u.field) or None), artifact=(u.artifact or None),
                    parents=[cid], text=(u.quotation or u.artifact))
            if u.mode == "conceptual":
                dom = ", ".join(k for k, _ in WeightedField(u.field).dominant())
                imprint(artifact_id=f"read-{u.id}",
                        title=f"Reading: {u.word} as a weighted field",
                        concept=c.id, kind="interpretation", regime="breath", mode="conceptual",
                        weights=dict(u.field), parents=[u.id], period=u.period, year=u.year,
                        text=f"Read as a weighted field ({dom}): {c.gloss}")
            else:
                sid = PHONETIC_READINGS.get(u.id)
                if sid:
                    s = c.lattice.senses[sid]
                    imprint(artifact_id=f"read-{u.id}", title=f"Reading: {u.word} as {s.label}",
                            concept=c.id, sense=sid, kind="interpretation", regime="pump",
                            mode="phonetic", parents=[u.id], period=u.period, year=u.year,
                            text=(f"Read in its own period, '{u.word}' here carries the sense "
                                  f"'{s.label}': {s.gloss}"))

    # The foil: the labrys read phonetically, recorded so the error can be named.
    imprint(artifact_id="read-labrys-lexical",
            title="Reading (lexical foil): the labrys as a mere syllabic sign",
            concept="labrys", kind="interpretation", regime="pump", mode="phonetic",
            weights={"syllabic-sign": 1.0}, parents=["labrys-knossos"], year=-1600,
            text=("Read phonetically: the double axe taken as nothing but a written "
                  "syllable, the conceptual field discarded — the projection this "
                  "framework exists to catch."))

    led = imp.ledger
    write_manifest(led, MANIFEST, g)
    v = led.verify()
    print(f"seeded {len(led.records)} record(s); chain {'intact' if v.ok else 'BROKEN'}; "
          f"head {led.head_hash[:12]}...; anchor {anchor or '(none)'}")
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
