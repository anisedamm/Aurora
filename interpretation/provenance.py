"""Provenance: who is the source of a reading, and is it the author or a mirror?

A reading of a concept's history is itself authored, and conceptual history is
the one field where the provenance of an *interpretation* is part of its
meaning: a gloss offered by the author, by a mirror (an AI reflecting the
author), by a collaboration, or quoted from an external scholar are four
different epistemic objects. The framework keeps two axes apart, exactly as the
sibling *integrity-alignment-system* does, because collapsing them is how
authorship of an interpretation gets lost or wrongly claimed:

  * **author** - who *owns* the reading and holds priority.   ("Is this mine?")
  * **source** - how it was *produced*.            ("Did I read it, or did a mirror?")

A large language model - Claude included - is a **mirror**: it can produce a
gloss without being the source of the insight. So a mirror-produced reading must
point (via `parents`) at the author-information it reflects - and, in this
domain, at the attested usage it reads. That lineage is what stops a reflection
from being silently promoted into an original interpretation.

`source` is an **attestation**, not a forensic finding. No system can read a
finished gloss and prove which words a human versus a model produced; that is
the same proxy-not-proof humility the rest of the framework runs on. What is
guaranteed is that the attestation is recorded immutably, timestamped, and kept
queryable - so the distinction, once made, cannot be quietly edited away.
"""

from __future__ import annotations

SOURCE_AUTHOR = "author"                # the human author's own reading
SOURCE_MIRROR = "mirror"                # produced by an AI reflecting the author
SOURCE_COLLABORATION = "collaboration"  # human-directed, mirror-drafted
SOURCE_EXTERNAL = "external"            # quoted from a third party; must be attributed

VALID_SOURCES = {
    SOURCE_AUTHOR,
    SOURCE_MIRROR,
    SOURCE_COLLABORATION,
    SOURCE_EXTERNAL,
}

# The only source that is an original human act. Everything else stands on
# something prior and must be able to name it.
ORIGINAL_SOURCES = {SOURCE_AUTHOR}

# Sources that reflect prior information and so must declare their lineage.
REFLECTING_SOURCES = {SOURCE_MIRROR, SOURCE_COLLABORATION, SOURCE_EXTERNAL}


def is_original(source: str) -> bool:
    """True when `source` is an original human act, not a reflection."""
    return source in ORIGINAL_SOURCES


def integrity_warnings(
    source: str,
    *,
    source_actor: str | None,
    parents: list[str] | None,
) -> list[str]:
    """Soft checks that keep provenance honest without hindering recording.

    These never block a record - the point is to *not* hide information - but
    they surface the gaps that would let a mirror's gloss pass as the author's.
    """
    if source not in VALID_SOURCES:
        raise ValueError(
            f"unknown source {source!r}; expected one of {sorted(VALID_SOURCES)}"
        )

    warnings: list[str] = []
    parents = parents or []

    if source in REFLECTING_SOURCES and not parents:
        warnings.append(
            f"source '{source}' reflects prior information but declares no "
            f"parents: a reflection without lineage cannot be told apart from "
            f"an origination"
        )
    if source in (SOURCE_MIRROR, SOURCE_EXTERNAL) and not source_actor:
        warnings.append(
            f"source '{source}' has no source_actor: the producing agent is "
            f"unattributed"
        )
    return warnings
