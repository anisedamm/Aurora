"""signal = integrity x direction(truth): the framework's one verdict on itself.

The capstone, and the closing of the arc back to the sibling
*integrity-alignment-system*, whose signal this mirrors. The system asks, of its own
record, two questions and multiplies the answers - a **product**, so either factor at
zero zeros the signal: a failsafe is trustworthy or it is not, no partial credit.

  * **integrity** - is the record *sound*? The hash chain verifies (no reading has
    been altered or reordered) and the published manifest is *fresh* (its chain-head
    hash still commits to the current ledger - the public record has not fallen behind
    the private one).

  * **direction(truth)** - is the record *pointed at the truth*? Every reading is
    **grounded** in a sign that passes L1 attestation (no interpretation floats free
    of an attested usage), and every record **names its author and its provenance**
    (the source axis is declared, so a mirror's reflection can never pass for an
    origination).

A recorded *projection* - the labrys read phonetically, kept as a named foil - does
not lower the signal: it is grounded and attributed, and the framework correctly reads
its alignment as zero. That is the system working, the way a retraction is standing,
not a break. Descriptive of the backing's trustworthiness; it gates nothing but its
own one-line verdict (and CI). Pure standard library.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .glossary import Glossary
from .ledger import KIND_INTERPRETATION, KIND_USAGE, Ledger
from .provenance import VALID_SOURCES
from .reading import attest

_HEAD_RE = re.compile(r"chain head hash:\s*`?([0-9a-f]{64})`?")


def _manifest_head(manifest_path) -> str | None:
    p = Path(manifest_path)
    if not p.exists():
        return None
    m = _HEAD_RE.search(p.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def _grounded(rec, ledger: Ledger, glossary: Glossary) -> bool:
    for pid in rec.parents:
        parent = ledger.by_id(pid)
        if parent is None or parent.kind != KIND_USAGE:
            continue
        try:
            if attest(glossary.usage(pid)).ok:
                return True
        except KeyError:
            continue
    return False


@dataclass
class Signal:
    integrity: int
    direction: int
    chain_ok: bool
    manifest_fresh: bool
    grounded_ok: bool
    provenance_ok: bool
    reasons: list[str] = field(default_factory=list)

    @property
    def value(self) -> int:
        return self.integrity * self.direction

    @property
    def verdict(self) -> str:
        if self.value:
            return ("signal = integrity(1) x direction(truth)(1) = 1  ->  "
                    "a trustworthy backing for the interpretation of conceptual history")
        why = "; ".join(self.reasons) or "a factor is zero"
        return (f"signal = integrity({self.integrity}) x direction(truth)({self.direction}) "
                f"= 0  ->  not yet trustworthy: {why}")

    @property
    def summary(self) -> str:
        def mark(ok: bool) -> str:
            return "OK" if ok else "FAIL"
        return "\n".join([
            self.verdict,
            f"  integrity = {self.integrity}",
            f"    chain:    {mark(self.chain_ok)}",
            f"    manifest: {mark(self.manifest_fresh)} (head still commits to the ledger)",
            f"  direction(truth) = {self.direction}",
            f"    grounded:   {mark(self.grounded_ok)} (every reading rests on an attested sign)",
            f"    provenance: {mark(self.provenance_ok)} (every record names author and source)",
            "  note: a product - either factor at zero zeros the signal. A named projection "
            "(the foil) is standing, not a break.",
        ])


def compute_signal(
    ledger: Ledger,
    glossary: Glossary,
    *,
    manifest_path="MANIFEST.md",
) -> Signal:
    """Compute the framework's one verdict on its own record: integrity x direction."""
    reasons: list[str] = []

    chain = ledger.verify()
    chain_ok = chain.ok
    if not chain_ok:
        reasons.append(f"chain broken: {chain.reason}")

    head = _manifest_head(manifest_path)
    manifest_fresh = head is not None and head == ledger.head_hash
    if head is None:
        reasons.append("no published manifest to anchor the record")
    elif not manifest_fresh:
        reasons.append("manifest is stale: its head no longer commits to the ledger")

    ungrounded = [
        r.id for r in ledger.records
        if r.kind == KIND_INTERPRETATION and not _grounded(r, ledger, glossary)
    ]
    grounded_ok = not ungrounded
    if ungrounded:
        reasons.append(f"ungrounded reading(s): {ungrounded}")

    unattributed = [
        r.id for r in ledger.records
        if not r.author or r.source not in VALID_SOURCES
    ]
    provenance_ok = not unattributed
    if unattributed:
        reasons.append(f"unattributed record(s): {unattributed}")

    integrity = 1 if (chain_ok and manifest_fresh) else 0
    direction = 1 if (grounded_ok and provenance_ok) else 0
    return Signal(
        integrity=integrity, direction=direction, chain_ok=chain_ok,
        manifest_fresh=manifest_fresh, grounded_ok=grounded_ok,
        provenance_ok=provenance_ok, reasons=reasons,
    )
