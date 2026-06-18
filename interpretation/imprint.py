"""The active recorder: press a piece of conceptual history into the ledger.

`Imprinter.imprint` checks provenance honesty first (a mirror-produced reading
that names no lineage is warned about, never blocked), then appends a
timestamped, chained record. Writing is kept separate from the reading layers
(`reading.py`) so you can record a usage or a gloss without first interrogating
it, and interrogate a stranger's reading without recording it.

The default author is **anise.damm** - the record of authorship this framework
was built to keep. Pure standard library.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .ledger import InterpretationRecord, Ledger
from .provenance import SOURCE_AUTHOR, integrity_warnings

DEFAULT_AUTHOR = "anise.damm"


@dataclass
class ImprintReceipt:
    record: InterpretationRecord
    warnings: list[str] = field(default_factory=list)

    @property
    def summary(self) -> str:
        r = self.record
        head = f"imprinted '{r.id}' ({r.kind}) by {r.author} via {r.source}"
        if self.warnings:
            return head + "\n" + "\n".join(f"  warning: {w}" for w in self.warnings)
        return head


@dataclass
class Imprinter:
    ledger: Ledger

    def imprint(
        self,
        *,
        artifact_id: str,
        title: str,
        text: str = "",
        author: str = DEFAULT_AUTHOR,
        kind: str = "note",
        source: str = SOURCE_AUTHOR,
        source_actor: str | None = None,
        parents: list[str] | None = None,
        concept: str | None = None,
        sense: str | None = None,
        word: str | None = None,
        citation: str | None = None,
        period: str | None = None,
        year: int | None = None,
        license: str | None = None,
        created_claimed: str | None = None,
        external_anchor: str | None = None,
        recorded_at: str | None = None,
    ) -> ImprintReceipt:
        """Record a piece of conceptual history. Surfaces provenance gaps; never blocks."""
        warnings = integrity_warnings(source, source_actor=source_actor, parents=parents)
        record = self.ledger.register(
            artifact_id=artifact_id,
            author=author,
            title=title,
            text=text,
            kind=kind,
            source=source,
            source_actor=source_actor,
            parents=parents,
            concept=concept,
            sense=sense,
            word=word,
            citation=citation,
            period=period,
            year=year,
            license=license,
            created_claimed=created_claimed,
            external_anchor=external_anchor,
            recorded_at=recorded_at,
        )
        return ImprintReceipt(record=record, warnings=warnings)
