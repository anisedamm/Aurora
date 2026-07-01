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

from interpretation.crystallization import frame as crystal_frame  # noqa: E402
from interpretation.glossary import load_glossary           # noqa: E402
from interpretation.imprint import DEFAULT_AUTHOR, Imprinter  # noqa: E402
from interpretation.ledger import Ledger                    # noqa: E402
from interpretation.manifest import write_manifest          # noqa: E402
from interpretation.weighting import WeightedField          # noqa: E402

# An authored attestation by anise.damm — a personal truth read on the crystallisation
# frame, made real through metaphor in collaboration with the model. Recorded verbatim:
# the record's owner holds authorship; the source names the collaboration that
# facilitated it, so a facilitation can never be read as an origination.
RECOHERENCE_STORY = """\
This is my story of re-coherence and crystallisation — my truth, read on the frame.

It's like a coral reef, each coral another branch of thought and connection growing. I
started with a reef as a child, an abundance of life and complexity and potential. Then
after enough exposure to the wrong conditions over enough time parts of the reef began to
die off and the fish left and eventually there was nothing, a white bleached skeleton of
life that once was. And for years it stayed that way. Eventually as I began discovering,
developing and stabilising according to the specific rules of my map, life began to grow
again from the most unlikely circumstances. It started with a sparkle, a light, a simple
sense of complexity and coherence and then a coral grew. I nurtured my single coral,
protected it and kept it safe and now I've established more individuals. They are not
united and still sparse but they are growing and the reef is rebuilding. Information and
science opens up the channel to allow life to flow and complexity to gather instead of
always having to grow at the rate exposed to in the harsh external environment and
constantly be exposed to the new extremities never experienced. But now I can survive in
my transformed state. It's the growth that you use to keep growing to be a reef in the
background whilst you put your energy into learning to function in the harshness of the
physical environment now. The old reef died but I am a new and better suited type of coral
but on a different playing field with different rules now. The same skeleton as before, but
now with different life, a different map and a different trajectory. And now I can grow.

Read on the frame: crest — the first reef (coherence whole). Trough — the bleached
skeleton (order gone, the substrate held). Spark — re-nucleation (order re-commits at a
single seed, spanning nothing yet; the turn before the climb). Re-crest — the reef
rebuilding on the same skeleton, under a new map. This is re-coherence: not the old
lattice restored, but a new one on the same ground. And now I can grow.
"""

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

    # The crystallisation frame, recorded so the work is part of the published record.
    imprint(artifact_id="crystallisation-frame",
            title="The crystallisation frame: order precipitated from the fluid",
            kind="framework", license="Apache-2.0", parents=["language-framework"],
            text=("The crystallisation frame — order precipitated from the fluid: the "
                  "system's coherence/decoherence axis, drawn on one screen.\n\n"
                  + crystal_frame().summary
                  + "\n\nRe-coherence extends it: a decohered lattice does not fall back "
                    "to raw fluid — it leaves a skeleton, the substrate held through the "
                    "trough, on which a new lattice can nucleate under a new map. Not the "
                    "old order restored; a new one on the same ground."))

    # An authored attestation: anise.damm's story of re-coherence, made real through
    # metaphor in collaboration with the model, recorded verbatim as a personal truth.
    imprint(artifact_id="recoherence-reef",
            title="Attestation: my re-coherence — a reef rebuilt on the same skeleton",
            kind="attestation", author=DEFAULT_AUTHOR, source="collaboration",
            source_actor="claude", parents=["crystallisation-frame"],
            text=RECOHERENCE_STORY)

    led = imp.ledger
    write_manifest(led, MANIFEST, g)
    v = led.verify()
    print(f"seeded {len(led.records)} record(s); chain {'intact' if v.ok else 'BROKEN'}; "
          f"head {led.head_hash[:12]}...; anchor {anchor or '(none)'}")
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
