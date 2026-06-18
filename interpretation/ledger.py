"""The interpretation ledger: who read what into which usage, when - tamper-evident.

This is the provenance + attribution backing for the framework. It is an
**append-only, hash-chained log**, the same mechanism the sibling
*integrity-alignment-system* uses, scoped here to conceptual history. Each record
fingerprints a passage (a concept's gloss, an attested usage, a reading, a unit
of reasoning), names the author who owns it and the source that produced it, and
binds itself to the record before it via `prev_hash`. Altering or reordering any
past entry changes its `entry_hash` and breaks every link after it, which
`verify()` detects - so the record is tamper-evident though it is plain text.

Honesty about what a timestamp proves (the framework's own rule applied to
itself):

  * `recorded_at` is when *this system* saw the passage. The hash chain makes it
    tamper-evident **relative to the other entries** - you cannot backdate one
    record without rewriting the whole tail.
  * It is **not**, on its own, proof of absolute wall-clock time. For that you
    anchor the chain to a witness whose clock you do not control: commit the
    ledger to git (its commit graph is an independent witness), recorded in
    `external_anchor`. The ledger records the claim; the anchor upgrades it.

`created_claimed` is the author's own stated date - an unverified assertion, kept
separate from `recorded_at` so the two are never confused. The domain fields
(`concept`, `sense`, `word`, `citation`, `year`) let a record stand for a piece
of conceptual history, not just an opaque blob.

Pure standard library; the ledger persists as JSON Lines (one record per line).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .fingerprint import Fingerprint, fingerprint
from .provenance import SOURCE_AUTHOR

GENESIS_HASH = "0" * 64

# The kinds a record can take. `usage` is an attested word-in-a-text; an
# `interpretation` reads a sense into a usage; `concept` and `sense` record the
# authored map; `reasoning` records the thought-flow; the rest are documents.
KIND_CONCEPT = "concept"
KIND_USAGE = "usage"
KIND_INTERPRETATION = "interpretation"
KIND_SENSE = "sense"
KIND_REASONING = "reasoning"

# Records that are metadata *about* readings rather than readings themselves
# (reserved for retraction/contradiction, as in the sibling system); recognition,
# novelty and alignment exclude them.
RETRACTION_KIND = "retraction"
CONTRADICTION_KIND = "contradiction"
NON_WORK_KINDS = frozenset({RETRACTION_KIND, CONTRADICTION_KIND})


@dataclass
class InterpretationRecord:
    """One immutable, chained record in the conceptual-history ledger."""

    id: str                      # stable slug/key
    author: str                  # who *owns* it / holds priority ("is this mine?")
    title: str                   # human-readable name
    content_hash: str
    normalized_hash: str
    signature: list[int]
    n_shingles: int
    recorded_at: str             # UTC ISO-8601, set by this system
    kind: str = "note"           # concept / usage / interpretation / sense / reasoning / ...
    source: str = SOURCE_AUTHOR  # how it was produced: author vs mirror vs ...
    source_actor: str | None = None  # the producing agent (e.g. a model name)
    parents: list[str] = field(default_factory=list)  # lineage: ids it reflects/reads
    # --- the conceptual-history domain ----------------------------------
    concept: str | None = None   # the headword this record concerns ("revolution")
    sense: str | None = None     # for an interpretation: the sense id it reads in
    word: str | None = None      # for a usage: the word as it appears in the text
    citation: str | None = None  # for a usage: where the word is attested
    period: str | None = None    # human-readable period label ("post-1789")
    year: int | None = None      # representative year for drift comparison (BCE negative)
    # --- standing -------------------------------------------------------
    license: str | None = None
    schema_version: int = 1
    created_claimed: str | None = None   # author-stated date (unverified)
    external_anchor: str | None = None   # git SHA / URL, if any
    prev_hash: str = GENESIS_HASH
    entry_hash: str = ""

    def payload(self) -> dict:
        """The hashed content of the record (everything but `entry_hash`)."""
        d = asdict(self)
        d.pop("entry_hash")
        return d

    def compute_hash(self) -> str:
        canonical = json.dumps(self.payload(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class ChainVerification:
    ok: bool
    n_records: int
    broken_at: int | None = None   # index of the first bad record, if any
    reason: str = ""


@dataclass
class Ledger:
    """An append-only interpretation ledger backed by a JSONL file."""

    path: Path
    records: list[InterpretationRecord] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.records = self._load()

    def _load(self) -> list[InterpretationRecord]:
        if not self.path.exists():
            return []
        out: list[InterpretationRecord] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(InterpretationRecord(**json.loads(line)))
        return out

    @property
    def head_hash(self) -> str:
        return self.records[-1].entry_hash if self.records else GENESIS_HASH

    def register(
        self,
        *,
        artifact_id: str,
        author: str,
        title: str,
        text: str = "",
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
    ) -> InterpretationRecord:
        """Fingerprint `text` and append a new record to the chain.

        `recorded_at` is injectable only so tests can be deterministic; in normal
        use it defaults to now() in UTC.
        """
        fp: Fingerprint = fingerprint(text)
        record = InterpretationRecord(
            id=artifact_id,
            author=author,
            title=title,
            content_hash=fp.content_hash,
            normalized_hash=fp.normalized_hash,
            signature=list(fp.signature),
            n_shingles=fp.n_shingles,
            recorded_at=recorded_at or datetime.now(timezone.utc).isoformat(),
            kind=kind,
            source=source,
            source_actor=source_actor,
            parents=list(parents) if parents else [],
            concept=concept,
            sense=sense,
            word=word,
            citation=citation,
            period=period,
            year=year,
            license=license,
            created_claimed=created_claimed,
            external_anchor=external_anchor,
            prev_hash=self.head_hash,
        )
        record.entry_hash = record.compute_hash()
        self.records.append(record)
        self._append_to_file(record)
        return record

    def _append_to_file(self, record: InterpretationRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record), separators=(",", ":")) + "\n")

    def by_id(self, record_id: str) -> InterpretationRecord | None:
        """The latest record for an id (a re-imprint appends a new version)."""
        found = None
        for r in self.records:
            if r.id == record_id:
                found = r
        return found

    def verify(self) -> ChainVerification:
        """Recompute the chain; any altered or reordered record is caught."""
        prev = GENESIS_HASH
        for i, rec in enumerate(self.records):
            if rec.prev_hash != prev:
                return ChainVerification(
                    ok=False, n_records=len(self.records), broken_at=i,
                    reason=f"record {i} ({rec.id}): prev_hash does not chain",
                )
            if rec.compute_hash() != rec.entry_hash:
                return ChainVerification(
                    ok=False, n_records=len(self.records), broken_at=i,
                    reason=f"record {i} ({rec.id}): contents altered after recording",
                )
            prev = rec.entry_hash
        return ChainVerification(ok=True, n_records=len(self.records))
