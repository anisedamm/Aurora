"""Manifest: turn the private chain into a public, defensible record.

Priority over a reading is protected here by *publication*, not secrecy - the
same defensive-publication move the sibling system makes. The load-bearing line
is the **chain head hash**: because every record is chained, that one hash
commits to the entire ledger. Anchor it to a witness you do not control (commit
this file to git and push - the commit graph is an independent, dated witness)
and the whole record becomes provable "this reading existed, as mine, by this
date" to a third party.

Re-deriving the manifest later and finding the same head hash proves the record
has not been altered since it was anchored.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from .glossary import Glossary
from .ledger import KIND_INTERPRETATION, Ledger


def _short(h: str, n: int = 12) -> str:
    return h[:n] + "..." if len(h) > n else h


def build_manifest(
    ledger: Ledger,
    glossary: Glossary | None = None,
    *,
    generated_at: str | None = None,
) -> str:
    """Render a publishable Markdown manifest of the whole ledger."""
    stamp = generated_at or datetime.now(timezone.utc).isoformat()
    v = ledger.verify()
    head = ledger.head_hash
    kinds = Counter(r.kind for r in ledger.records)
    concepts = sorted({r.concept for r in ledger.records if r.concept})

    # Per-record alignment, computed only for interpretations when a glossary is given.
    aligns: dict[int, str] = {}
    if glossary is not None:
        from .alignment import align_record

        for i, r in enumerate(ledger.records):
            if r.kind == KIND_INTERPRETATION:
                a = align_record(r.id, ledger, glossary)
                aligns[i] = f"{a.value:.2f}/{a.influence}"

    lines = [
        "# Interpretation manifest — defensive publication",
        "",
        "This document is a tamper-evident, timestamped record of original",
        "authorship over a body of conceptual-history readings. It is published",
        "openly: the goal is to establish priority *and* keep the readings",
        "available to scholarship, not to hide them.",
        "",
        f"- generated_at: `{stamp}`",
        f"- records: **{len(ledger.records)}**",
        f"- chain head hash: `{head}`",
        f"- chain status: **{'intact' if v.ok else 'BROKEN: ' + v.reason}**",
        f"- concepts: {', '.join(f'`{c}`' for c in concepts) or '—'}",
        "- record kinds: " + ", ".join(f"{k}×{n}" for k, n in sorted(kinds.items())),
        "",
        "Anchor the chain head hash above to a witness you do not control (commit",
        "this file to git and push) to turn 'recorded' into real-world provable",
        "'recorded by this date'.",
        "",
        "| # | id | title | owner | source | kind | concept | regime/mode | sense | align | anchor |",
        "|---|----|-------|-------|--------|------|---------|-------------|-------|-------|--------|",
    ]
    for i, r in enumerate(ledger.records):
        anchor = r.external_anchor or "—"
        rm = "/".join(x for x in (r.regime, r.mode) if x) or "—"
        lines.append(
            f"| {i} | `{r.id}` | {r.title} | {r.author} | {r.source} | {r.kind} "
            f"| {r.concept or '—'} | {rm} | {r.sense or '—'} "
            f"| {aligns.get(i, '—')} | `{anchor}` |"
        )

    lines += [
        "",
        "## How to verify",
        "",
        "```bash",
        "python -m interpretation verify     # recompute the chain; any edit breaks it",
        "python -m interpretation manifest   # re-derive this file; head hash must match",
        "```",
        "",
        "A record's `source` says how it was produced (author vs mirror); its",
        "`owner` says who holds priority. A mirror-produced reading names the",
        "author-information and the attested usage it reflects in its lineage, so a",
        "reflection can never be read as an origination.",
        "",
        "`align` is `value/influence` — `value = purpose x fidelity` (descriptive,",
        "faithfulness to the recorded usage, not absolute meaning) and `influence`",
        "is how many downstream readings build on it. Alignment accrues as distinct",
        "other readers corroborate a reading; it is shown, never enforced.",
    ]
    return "\n".join(lines) + "\n"


def write_manifest(
    ledger: Ledger,
    path,
    glossary: Glossary | None = None,
    *,
    generated_at: str | None = None,
) -> str:
    """Write the manifest to `path` and return its text."""
    from pathlib import Path

    text = build_manifest(ledger, glossary, generated_at=generated_at)
    Path(path).write_text(text, encoding="utf-8")
    return text
