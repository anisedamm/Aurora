# Architecture — the map of the whole

The framework has grown to **27 modules across three pillars, 34 CLI commands, and five
authored maps** (plus the CLI and public-API surface). This is the map of how they fit: the
pillars they fall into, what depends on what
(extracted from the actual imports, not guessed), the data each reads, and the order the
readings run in. It is the code's atlas — a reader of the repository, the way `atlas` is a
reader of the content.

One sentence holds it all together, inherited from the sibling
`integrity-alignment-system`: **a check is a proxy, not a proof** — so every measure here
is *descriptive, never a gate*, save the one honest gate (attestation), and every authored
map carries its provenance and is recorded in the tamper-evident ledger.

## The three pillars and two capstones

Everything sits in one of three pillars, each organised around a **hub module**, and is
gathered by two capstones.

```
   ┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
   │  CONCEPTUAL-HISTORY      │ │   THE MEANING TREE       │ │   THE INTEGRITY SPINE   │
   │  the breath/pump reading │ │ binary→relational→       │ │  (inherited, turned     │
   │  & the three layers      │ │       proportional       │ │   hermeneutic)          │
   │                          │ │                          │ │                         │
   │  hub:  glossary          │ │  hub:  condensation      │ │  hub:  ledger           │
   │   ← semantics, regime,   │ │   ← lexicon              │ │   ← fingerprint,        │
   │     weighting            │ │                          │ │     provenance          │
   │                          │ │  tension   gradient      │ │                         │
   │  reading (L1/L2/L3)      │ │  fold      weave         │ │  imprint    manifest    │
   │  constellation migration │ │  frontier  cornerstone   │ │  alignment              │
   │  memory   arc   lexicon  │ │  dimension dimensionless │ │                         │
   └────────────┬─────────────┘ └────────────┬─────────────┘ └────────────┬────────────┘
                └────────────────────────────┼─────────────────────────────┘
                                             ▼
              signal  (the integrity verdict: integrity × direction(truth))
              atlas   (the whole reading, breath to bit, on one screen)
                                             ▼
                       __main__  (CLI)        __init__  (public API)
```

- **Conceptual-history reading** — the original framework: read a concept's history as a
  sequence of attested usages, across the breath/pump threshold, without letting the
  present read into the past. Hub: **`glossary`**.
- **The meaning tree** — the layers built in this line of work: how a bit becomes meaning,
  by condensing a field, holding or excluding its opposite, gaining proportion and depth,
  being woven into a web, and spanning (or transcending) dimensions. Hub: **`condensation`**
  (it owns `Relations` and the `_compound` ancestry walk the whole tree leans on).
- **The integrity spine** — the inherited mechanism that keeps every reading honest and
  attributable. Hub: **`ledger`**.
- **Capstones** — **`signal`** turns the discipline on the record itself; **`atlas`**
  composes every tested measure into one narrative.

## Dependency tiers (depends-on flows upward)

Extracted from the modules' actual `from .x import` statements. A module depends only on
modules in tiers above it — no cycles.

```
TIER 0  primitives (no internal dependencies)
   fingerprint   provenance   regime   weighting   semantics   lexicon

TIER 1  the hubs
   ledger        ← fingerprint, provenance                 (integrity)
   glossary      ← semantics                               (conceptual history)
   condensation  ← lexicon                                 (the meaning tree)

TIER 2  readings & records
   spine    │ imprint ← ledger,provenance · manifest ← glossary,ledger
            │ alignment ← fingerprint,glossary,ledger,reading,regime,weighting
   history  │ reading ← fingerprint,glossary,regime,semantics,weighting
            │ constellation ← glossary,regime,weighting · migration ← glossary,regime,weighting
            │ memory ← glossary,reading,weighting · arc ← glossary,lexicon,migration
   meaning  │ tension ← condensation,glossary · gradient ← condensation
            │ fold/weave/frontier/cornerstone ← condensation,lexicon
            │ dimension ← condensation,glossary,lexicon,migration,regime
            │ dimensionless ← arc,glossary,lexicon,migration

TIER 3  capstones (composers)
   signal   ← glossary,ledger,provenance,reading                 (integrity verdict)
   atlas    ← arc,condensation,constellation,cornerstone,dimension,dimensionless,
              fold,frontier,glossary,gradient,ledger,lexicon,migration,signal,
              tension,weave                                       (the whole reading)

TIER 4  surface
   __main__ (CLI: 34 commands)        __init__ (public API / exports)
```

## Module reference

| Module | Pillar | Reads it as | One-line role |
|--------|--------|-------------|---------------|
| `fingerprint` | spine | — | content hash (exact) + MinHash recognition (a similarity proxy) |
| `provenance` | spine | — | the source axis: author / mirror / collaboration / external |
| `ledger` | spine | ledger.jsonl | append-only, hash-chained, timestamped record of readings |
| `imprint` | spine | — | the active recorder (default author: anise.damm) |
| `manifest` | spine | MANIFEST.md | defensive-publication manifest (commits to the chain head) |
| `alignment` | spine | — | interpretive alignment = purpose × fidelity (or × resonance) |
| `regime` | history | — | the attention axis: breath (holistic) vs pump (analytic) |
| `weighting` | history | — | a conceptual sign's weighted field + resonance |
| `semantics` | history | — | a diachronic algebra of senses (descent lattice; inversion) |
| `glossary` | history | glossary.json | the authored map: concepts, usages, aliases, migrations, paradoxes |
| `reading` | history | — | the three layers: attest (L1) / read (L2) / drift + project (L3) |
| `constellation` | history | — | the system-level breath web: load-bearing values across a regime |
| `migration` | history | — | a value across the threshold: held whole, then dispersed |
| `memory` | history | — | the return path: remember / memory_chain / confluence |
| `arc` | history | — | one thread traced unbroken across both regimes |
| `lexicon` | history | lexicon.json | phonetic language over time: the explosion, sieve→success, coherence |
| `condensation` | meaning | relations.json | the bit + its condensed field; owns `Relations` + `_compound` |
| `tension` | meaning | (glossary paradoxes) | holding the opposite (paradox) vs excluding it (binary) |
| `gradient` | meaning | gradients.json | proportion: the scale of degrees between two poles |
| `fold` | meaning | — | corroborating layers of depth → deemed true → woveable |
| `weave` | meaning | — | the antonym couples as one web: roots, hubs, keystone |
| `frontier` | meaning | — | the leaf-edge of the tree: unpolarised, singular, reaching |
| `cornerstone` | meaning | — | the root-base of the tree: innate, self-standing, given |
| `dimension` | meaning | — | the tree as a system: conveyance × culture × time × depth |
| `dimensionless` | meaning | invariants.json | invariants proposed as universal truth, and the unattestable gap |
| `signal` | capstone | ledger + manifest | the verdict: integrity × direction(truth) == 1 |
| `atlas` | capstone | all of the above | the whole history of meaning on one screen |

## The authored maps (data → module)

Every map is a **proxy carrying its provenance**, surfaced rather than hidden, and each is
imprinted into the ledger (so `signal` covers it).

| File | Read by | Carries |
|------|---------|---------|
| `glossary.json` | `glossary` | breath signs + pump words; `value_aliases`, `migrations`, `paradoxes` |
| `lexicon.json` | `lexicon` | lexemes over time: `defined_in_terms_of`, eras, languages, alignment |
| `relations.json` | `condensation` | meaning-connections: antonyms, synonyms, associates |
| `gradients.json` | `gradient` | proportional scales: terms placed in [0,1] between two poles |
| `invariants.json` | `dimensionless` | proposed invariants: grounding, domains, manifest/a-priori |
| `interpretation_ledger.jsonl` | `ledger` | the hash-chained record (37 records); `MANIFEST.md` publishes its head |

## The reading arc (dependency order)

The two pillars each have a pipeline; the capstones gather both.

```
conceptual history (per usage):
   attest ─→ read ─→ drift / project
   (L1: is it real?)  (L2: what here?)  (L3: present read into the past?)

the meaning tree (per concept):
   condense ─→ tension ─→ gradient ─→ fold ─→ weave ─→ frontier ╮
   bit+field   hold|       degrees    depth   relate   ╭ cornerstone (the edges)
               exclude      between    →truth                   ╰─→ dimension ─→ dimensionless
                            the poles                              (the system)   (beyond it)

capstones:
   signal (integrity)        atlas (the whole, breath to bit)
```

The deep symmetry the tree turns on: the **bit excludes** its opposite (a clean cut), the
**breath holds** it (a paradox), the **pump segments** it (drops the holding) — and
`gradient` fills the cut with proportion, whose midpoint is the very balance the breath
holds. Folding earns a concept its place in the weave; the cornerstone is where folding
bottoms out; the frontier is where it reaches; the dimensionless is the distinction (0/1)
the whole thing began from.

## CLI commands by pillar

```
the authored map     concepts · trace · regime · sense
the three layers     attest · read · drift · project · weigh · align
breath web/threshold constellation · migrate · remember · chain · confluence · arc
phonetic web         proliferation · untranslatables
the meaning tree     condense · connect · tension · gradient · fold · weave ·
                     frontier · cornerstones · dimensions · dimensionless
record & integrity   imprint · manifest · verify · signal · status
the whole            atlas
```

## How to read this map

Three hubs carry the weight — **`glossary`** (the concepts), **`ledger`** (the record),
**`condensation`** (the meaning tree). Each pillar's other modules are readings hung off its
hub; `signal` proves the record sound and `atlas` composes the rest. Nothing depends
downward, so any module can be read with only the tiers above it in mind. And the rule that
holds throughout: every line here is a proxy that tells the truth about being one —
descriptive, never a gate, but the one honest gate of attestation.
