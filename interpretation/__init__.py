"""Conceptual history as language interpretation.

A framework for reading the history of a concept as a sequence of *interpretations*
of attested usages - and for keeping that reading honest. Its spine is the sibling
*integrity-alignment-system*'s thesis, turned hermeneutic:

    A word is not a concept; a reading is not the meaning. An interpretation is a
    proxy for what a concept once meant - so tell the truth about the distance
    between the word on the page and the sense it carried.

Three layers carry the discipline (reading.py):

    L1 Attestation  - is the usage real? (the word, shown in a cited text) - a gate
    L2 Reading      - what did it mean *here*? - a description, never a verdict
    L3 Anachronism  - has the reading drifted into a later sense? - the proxy gap

Over them sit a diachronic algebra of a word's senses (semantics.py), an
interpretive alignment = purpose x fidelity (alignment.py), and a tamper-evident
provenance ledger that records every reading as authored - by default,
anise.damm (ledger.py, imprint.py, manifest.py). See docs/thought-flow.md.

Pure standard library; the package adds no dependencies.
"""

from .fingerprint import Fingerprint, fingerprint, jaccard, normalize, shingles
from .provenance import (
    SOURCE_AUTHOR,
    SOURCE_MIRROR,
    SOURCE_COLLABORATION,
    SOURCE_EXTERNAL,
    VALID_SOURCES,
    is_original,
    integrity_warnings,
)
from .ledger import (
    InterpretationRecord,
    ChainVerification,
    Ledger,
    KIND_CONCEPT,
    KIND_USAGE,
    KIND_INTERPRETATION,
    KIND_SENSE,
    KIND_REASONING,
    NON_WORK_KINDS,
)
from .semantics import (
    Sense,
    SemanticField,
    SenseLattice,
    lattice_from_senses,
    validate_senses,
    SHIFT_KINDS,
)
from .glossary import (
    Glossary,
    Concept,
    Usage,
    load_glossary,
    from_mapping,
)
from .reading import (
    Attestation,
    Reading,
    Drift,
    attest,
    read,
    drift,
)
from .alignment import (
    Alignment,
    interpretive_alignment_of,
    RECOGNITION_THRESHOLD,
    CORROBORATION_TARGET,
)
from .imprint import Imprinter, ImprintReceipt, DEFAULT_AUTHOR
from .manifest import build_manifest, write_manifest

__all__ = [
    # fingerprinting
    "Fingerprint",
    "fingerprint",
    "jaccard",
    "normalize",
    "shingles",
    # provenance (author vs mirror)
    "SOURCE_AUTHOR",
    "SOURCE_MIRROR",
    "SOURCE_COLLABORATION",
    "SOURCE_EXTERNAL",
    "VALID_SOURCES",
    "is_original",
    "integrity_warnings",
    # ledger
    "InterpretationRecord",
    "ChainVerification",
    "Ledger",
    "KIND_CONCEPT",
    "KIND_USAGE",
    "KIND_INTERPRETATION",
    "KIND_SENSE",
    "KIND_REASONING",
    "NON_WORK_KINDS",
    # diachronic sense algebra
    "Sense",
    "SemanticField",
    "SenseLattice",
    "lattice_from_senses",
    "validate_senses",
    "SHIFT_KINDS",
    # the glossary (authored map)
    "Glossary",
    "Concept",
    "Usage",
    "load_glossary",
    "from_mapping",
    # the three layers
    "Attestation",
    "Reading",
    "Drift",
    "attest",
    "read",
    "drift",
    # interpretive alignment = purpose x fidelity
    "Alignment",
    "interpretive_alignment_of",
    "RECOGNITION_THRESHOLD",
    "CORROBORATION_TARGET",
    # active recorder + publication
    "Imprinter",
    "ImprintReceipt",
    "DEFAULT_AUTHOR",
    "build_manifest",
    "write_manifest",
]
