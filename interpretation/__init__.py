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
    KIND_SYMBOL,
    KIND_MYTH,
    NON_WORK_KINDS,
)
from .regime import (
    BREATH,
    PUMP,
    SCRIPT_CONCEPTUAL,
    SCRIPT_PHONETIC,
    VALID_REGIMES,
    VALID_MODES,
    NATIVE_SCRIPT,
    is_phonetic_projection,
)
from .weighting import WeightedField
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
    WeightedReading,
    Projection,
    attest,
    read,
    drift,
    read_symbol,
    project,
)
from .alignment import (
    Alignment,
    interpretive_alignment_of,
    weighted_alignment_of,
    align_record,
    RECOGNITION_THRESHOLD,
    CORROBORATION_TARGET,
)
from .memory import (
    Remembrance,
    remember,
    MemoryChain,
    MemoryLink,
    memory_chain,
    Confluence,
    Lineage,
    ConfluencePair,
    confluence,
    CONVERGENCE_THRESHOLD,
)
from .constellation import (
    Constellation,
    ValueWeight,
    SignAffinity,
    constellation,
    AFFINITY_THRESHOLD,
)
from .migration import Migration, Shard, migrate
from .condensation import (
    Term,
    Relations,
    load_relations,
    Condensation,
    condense,
    Connection,
    connect,
    RELATION_ANTONYM,
    RELATION_SYNONYM,
    RELATION_ASSOCIATE,
    RELATION_NONE,
    KIND_BIT,
    KIND_CONDENSED,
    KIND_UNPOLARISED,
)
from .weave import Couple, Node, Weave, weave
from .frontier import Frontier, FrontierWord, frontier
from .cornerstone import Cornerstones, CornerstoneWord, cornerstones
from .dimension import Axis, MeaningSpace, meaning_space, SYMBOL, STORY, WORD
from .dimensionless import (
    Invariant,
    Dimensionless,
    Dimensionlessness,
    load_invariants,
    dimensionless,
    KIND_APRIORI,
    KIND_MANIFEST,
)
from .lexicon import (
    Lexeme,
    Lexicon,
    load_lexicon,
    lexical_coherence,
    EraPoint,
    Proliferation,
    proliferation,
    Untranslatable,
    untranslatables,
    SHARED_LANGUAGE,
)
from .imprint import Imprinter, ImprintReceipt, DEFAULT_AUTHOR
from .manifest import build_manifest, write_manifest
from .arc import Arc, ArcStop, arc
from .signal import Signal, compute_signal
from .atlas import Atlas, atlas

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
    "KIND_SYMBOL",
    "KIND_MYTH",
    "NON_WORK_KINDS",
    # the attention axis (breath vs pump)
    "BREATH",
    "PUMP",
    "SCRIPT_CONCEPTUAL",
    "SCRIPT_PHONETIC",
    "VALID_REGIMES",
    "VALID_MODES",
    "NATIVE_SCRIPT",
    "is_phonetic_projection",
    "WeightedField",
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
    "WeightedReading",
    "Projection",
    "attest",
    "read",
    "drift",
    "read_symbol",
    "project",
    # alignment: purpose x fidelity (phonetic) / purpose x resonance (conceptual)
    "Alignment",
    "interpretive_alignment_of",
    "weighted_alignment_of",
    "align_record",
    "RECOGNITION_THRESHOLD",
    "CORROBORATION_TARGET",
    # the return path (inverse of projection): remembrance across the ghost lag
    "Remembrance",
    "remember",
    "MemoryChain",
    "MemoryLink",
    "memory_chain",
    "Confluence",
    "Lineage",
    "ConfluencePair",
    "confluence",
    "CONVERGENCE_THRESHOLD",
    # the constellation: the system-level web of a regime's shared values
    "Constellation",
    "ValueWeight",
    "SignAffinity",
    "constellation",
    "AFFINITY_THRESHOLD",
    # migration: a value tracked across the breath->pump threshold
    "Migration",
    "Shard",
    "migrate",
    # condensation: binary thought (compression) vs relational meaning (condensation)
    "Term",
    "Relations",
    "load_relations",
    "Condensation",
    "condense",
    "Connection",
    "connect",
    "RELATION_ANTONYM",
    "RELATION_SYNONYM",
    "RELATION_ASSOCIATE",
    "RELATION_NONE",
    "KIND_BIT",
    "KIND_CONDENSED",
    "KIND_UNPOLARISED",
    # the weave: paired antonym couples as one relational web (roots, hubs, keystone)
    "Couple",
    "Node",
    "Weave",
    "weave",
    # the frontier: meaning at the leaf-edge of the tree (unpolarised, singular, reaching)
    "Frontier",
    "FrontierWord",
    "frontier",
    # the cornerstones: meaning at the root-base of the tree (innate, self-standing roots)
    "Cornerstones",
    "CornerstoneWord",
    "cornerstones",
    # dimensional meaning: the tree as a system of axes (conveyance × culture × time × depth)
    "Axis",
    "MeaningSpace",
    "meaning_space",
    "SYMBOL",
    "STORY",
    "WORD",
    # the dimensionless: invariants proposed as universal truth, and the unattestable gap
    "Invariant",
    "Dimensionless",
    "Dimensionlessness",
    "load_invariants",
    "dimensionless",
    "KIND_APRIORI",
    "KIND_MANIFEST",
    # the lexicon over time: phonetic language as the record of growing understanding
    "Lexeme",
    "Lexicon",
    "load_lexicon",
    "lexical_coherence",
    "EraPoint",
    "Proliferation",
    "proliferation",
    "Untranslatable",
    "untranslatables",
    "SHARED_LANGUAGE",
    # active recorder + publication
    "Imprinter",
    "ImprintReceipt",
    "DEFAULT_AUTHOR",
    "build_manifest",
    "write_manifest",
    # the arc: one thread traced unbroken across both regimes
    "Arc",
    "ArcStop",
    "arc",
    # the capstone: signal = integrity x direction(truth)
    "Signal",
    "compute_signal",
    # the atlas: the whole history of meaning, composed on one screen
    "Atlas",
    "atlas",
]
