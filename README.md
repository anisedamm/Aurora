# Language

A framework for reading **conceptual history as language interpretation** — and
for keeping that reading honest.

It is built on one idea, the hermeneutic turn of the spine its sibling
[`integrity-alignment-system`](https://github.com/anisedamm/integrity-alignment-system)
runs on (*a check is a proxy, not a proof*):

> **A word is not a concept; a reading is not the meaning.** An interpretation is
> a *proxy* for what a concept once meant — so tell the truth about the distance
> between the word on the page and the sense it carried.

A concept (think of *revolution*) is not a fixed meaning but a name under which a
**history of meanings** has gathered. To read that history is to interpret a
sequence of attested usages — and the cardinal danger is letting *our* sense of a
word stand in for the sense it had *then*. This framework makes that danger
measurable.

It is **pure standard library** (no dependencies), authored by **anise.damm**, and
its readings are kept in a tamper-evident, timestamped, openly-publishable ledger.

## The three layers

The sibling system separates a *verdict* from *understanding*, then adds a third
layer that refuses to trust the verdict on faith. Conceptual history needs the
same three, because the failure modes are the same.

| Layer | Question it answers | Output | Gates? |
|-------|--------------------|--------|--------|
| **L1 Attestation** | Is the usage real — the word, shown in a cited text? | admissible / not, with reasons | **yes** |
| **L2 Reading** | What did the word mean *here*, in its own context? | a described sense, never "the meaning" | no |
| **L3 Anachronism** | Has our reading drifted from the usage's own time into a later sense? | the usage-to-reading gap, in years | no |

L1 is the **only gate**: you cannot interpret a word you cannot show was used. L2
and L3 *describe* and never block — a surprising reading may be perfectly
defensible; the framework reports the shape and leaves the judgement to a human.

The headline output is deliberately **not** "the meaning." It is L3's gap: the
live answer to *"is this reading hearing the word's own time, or ours?"*

## Layout

```
interpretation/
  fingerprint.py   # content hash (exact) + MinHash recognition (a similarity proxy)
  provenance.py    # the source axis: author vs mirror vs collaboration vs external
  ledger.py        # append-only, hash-chained, timestamped record of readings
  semantics.py     # a diachronic algebra of a word's senses (descent lattice)
  glossary.py      # the authored map: concepts, attested usages, senses
  reading.py       # the three layers: attest (L1) / read (L2) / drift (L3)
  alignment.py     # interpretive alignment = purpose x fidelity (descriptive)
  imprint.py       # the active recorder (default author: anise.damm)
  manifest.py      # defensive-publication manifest
glossary.json              # the authored conceptual histories (revolution, democracy)
interpretation_ledger.jsonl  MANIFEST.md
docs/thought-flow.md       # the living reasoning journal behind the design
tests/                     # the suite (49 tests)
```

## Quickstart

```bash
pip install -r requirements.txt   # only pytest, to run the suite; the framework is stdlib
pytest -q
```

```bash
# The authored map of concepts, their senses, and attested usages:
python -m interpretation concepts
python -m interpretation trace revolution

# The three layers, on one usage read in one sense:
python -m interpretation attest rev-1688                            # L1
python -m interpretation read   rev-1688 political-restoration      # L2
python -m interpretation drift  rev-1688 irreversible-rupture       # L3 -> ANACHRONISM
```

## The worked example: *revolution*

The textbook case of conceptual history (Koselleck's own). The **word** held
still while the **concept** inverted:

```
$ python -m interpretation trace revolution
        1543  celestial-return: cyclical return (astronomical)  [origin]
     c. 1660  political-restoration: return to a prior rightful order  [metaphor]
   post-1789  irreversible-rupture: irreversible forward rupture  [inversion]
    19th c.–  modern-transformation: any profound, rapid transformation  [broadening]
```

*Revolutio* named the **revolving of the heavens back** through their course
(Copernicus, *De revolutionibus*, 1543). Carried into politics by **metaphor**, it
meant a **turning-back** — the restoration of an ancient, rightful order (the
"Glorious Revolution" of 1688 was understood as a *return*). Then, after 1789, the
sense **inverted**: a *revolution* became an **irreversible break forward** into the
new, from which there is no going back. The word never changed; its concept turned
inside out.

So the cardinal error is exact and catchable. To read 1688's *revolution* with the
post-1789 sense of rupture is to hear our own age in theirs:

```
$ python -m interpretation drift rev-1688 irreversible-rupture
ANACHRONISM: reading rev-1688 (1689) in a sense first attested 1789
  - a later meaning projected back 100 year(s)
```

This is **Goodhart's law turned hermeneutic** (Skinner's "mythology of
prolepsis"): a reading that feels right *because it resonates now* has optimised
the wrong target. L3 measures the gap so the resonance cannot pass for the
historical sense unexamined.

## The diachronic algebra of senses

A word's senses do not stand free in time; a later sense **descends from** an
earlier one through an act of semantic change. Declare those edges and the senses
become a lattice you can compute with — the same machinery the sibling system uses
for its concept-units, turned from *prerequisite* order to **order of descent**.

A sense is identified with its **ancestry** (itself plus every sense it descends
from), and the operations are a lattice's:

| Operation | As | On ancestries |
|-----------|-----|---------------|
| **combine** | join `∨` | `ancestry(a) ∪ ancestry(b)` — the whole field two senses jointly carry |
| **common**  | meet `∧` | `ancestry(a) ∩ ancestry(b)` — the shared root meaning both still carry |
| **precedes** | order `≤` | `ancestry(a) ⊆ ancestry(b)` — `a` is ancestral to `b` |

```bash
$ python -m interpretation sense common revolution political-restoration modern-transformation
common root of 'political-restoration' and 'modern-transformation' (meet): 2 sense(s):
  cyclical return (astronomical) -> return to a prior rightful order
```

Each edge carries the **kind** of semantic change that produced it — the classic
typology (Bréal, Bloomfield): *broadening, narrowing, metaphor, metonymy,
amelioration, pejoration*, and the one conceptual history turns on, **inversion**.
*Democracy*, the second seeded concept, is an **amelioration**: a 4th-century-BCE
term of abuse for mob-rule that rose to an honorific ideal.

The same humility the rest of the framework runs on applies. The operations are
**exact** — proofs about the structure — but the structure is an **authored map**
(`glossary.json`): it carries its provenance, a proxy for the real history of the
word, not the history itself. A malformed order — a descent **cycle** or a
**dangling** edge — is **surfaced, never silently patched**: `validate_senses`
reports it and `SenseLattice` refuses to build.

## Interpretive alignment = purpose × fidelity

Where does one reading sit among the others recorded for a concept? The sibling
system's `alignment = purpose × truth`, with **truth re-read as fidelity to the
historical usage**:

- **purpose** — its contribution: how much the reading adds that is not already on
  record (novelty, `1 − similarity`). A restatement adds little; a fresh reading
  adds a lot.
- **fidelity** — how faithfully it sits in the concept's actual history, the three
  layers folded into one number:
  `fidelity = soundness × (not anachronistic) × (½·grounded + ½·corroboration)`
  — the chain verifies, the reading **descends from an attested usage** (L1), it is
  **not anachronistic** (L3), and distinct *other* readers corroborate it.

```
$ python -m interpretation align my-reading
interpretive alignment = purpose(1.00) x fidelity(0.50) = 0.50
  ->  a new reading, grounded but not yet corroborated
```

Because it is a product, the quadrants are honest: a fresh, grounded reading is
*purposeful but only half-aligned* until others corroborate it; an **anachronistic
reading is high-purpose, zero-fidelity**, however clever. Low alignment is a
*description of where a reading sits*, **never a verdict on its worth** — and the
record protects it in full either way. It is descriptive, never a gate.

## Provenance & authorship — who reads is part of what is read

Conceptual history is the one field where the **provenance of an interpretation**
is part of its meaning. The framework keeps two axes apart, as the sibling system
does:

- **author** — who *owns* the reading and holds priority. (Default: `anise.damm`.)
- **source** — how it was produced: `author` / `mirror` / `collaboration` /
  `external`. A large language model is a **mirror**: it can produce a gloss without
  being the source of the insight, so a mirror-produced reading must declare its
  **lineage** — the author-information and the attested usage it reflects. The
  recorder *warns* (never blocks) when that lineage is missing, so a reflection is
  never silently promoted to an origination.

```bash
python -m interpretation imprint gloss.md --id my-reading --title "A rupture reading" \
    --kind interpretation --concept revolution --sense irreversible-rupture \
    --parents rev-1789 --author "anise.damm"
python -m interpretation manifest --out MANIFEST.md   # publish priority, then commit to anchor
python -m interpretation verify                       # recompute the chain; any edit breaks it
```

Each reading is fingerprinted and appended to an **append-only, hash-chained
ledger**: altering or reordering any past record breaks every link after it, which
`verify()` detects. Priority over a reading is protected by **defensive
publication** — `MANIFEST.md` renders the whole chain into one shareable document
whose load-bearing line is the **chain head hash**. Commit it to git and push, and
the commit graph becomes an independent, dated witness: "this reading existed, as
mine, by this date," provable to a third party. As with the sibling system, the
honest limit is named — a timestamp is proof only as far as its anchor.

## Neutrality — the framework's stance

The framework **protects the integrity of a reading and guards against
anachronism, but it neither fixes the meaning nor walks the interpreter's path.**
Every measure here (`read`, `drift`, `align`) is **descriptive, never a gate** save
the one honest gate, attestation; the authored map carries its provenance and is
never mistaken for the subject; and no reading is ever blocked from being recorded.
It guards the reading and the usage — it does not decide what the word *truly*
meant. That is the human's work, which no system should pretend to do for them.

## Relationship to `integrity-alignment-system`

This is a **sibling**, not a fork. It carries over that project's spine, its
`fingerprint`/`provenance`/`ledger`/`manifest` mechanism, and its discipline of
never letting a proxy wear a proof's clothes — and turns them from *information
integrity* toward *the interpretation of conceptual history*. The full reasoning,
in the order it arrived, is the living journal in
[`docs/thought-flow.md`](docs/thought-flow.md).
