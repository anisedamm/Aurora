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

Beneath that sits a deeper threshold the framework now names. A culture's
**mode of attention** decides how it writes: a **breath** culture (participatory,
holistic) writes in *conceptual* signs that hold a weighted field of meaning at
once — the Minoan labrys, the Egyptian ankh; a **pump** culture (analytic,
segmenting) writes in *phonetic* signs that spell a sound and defer meaning to a
lexicon. We assume writing is phonetic — but it wasn't meant to be. The **ghost
lag** is breath-meaning still moving under pump-language, and the cardinal error
becomes **phonetic projection**: reading a breath-era sign (or a myth) as if it
spelled a word, when the context dictates the manifestation of what is meant.

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

L1 is the **only gate**: you cannot interpret a sign you cannot show was used. L2
and L3 *describe* and never block — a surprising reading may be perfectly
defensible; the framework reports the shape and leaves the judgement to a human.

The headline output is deliberately **not** "the meaning." It is L3's gap: the
live answer to *"is this reading hearing the sign's own time, or ours?"*

Each layer **generalises across the two regimes**. L1 attests a *phonetic* word by
showing it in a cited quotation, and a *conceptual* sign by citing the material
artifact it survives on and the weighted field it carries. L2 reads a word into a
**sense**, and a symbol into a **weighted field**. L3 catches two forms of the same
mistake — reading the present into the past: **anachronism** (a later *sense*
projected onto an earlier word) and **phonetic projection** (a later *mode of
attention* projected onto a breath-era sign).

## Layout

```
interpretation/
  regime.py        # the attention axis: breath (holistic) vs pump (analytic)
  weighting.py     # weighted meaning: a conceptual sign's field + resonance
  fingerprint.py   # content hash (exact) + MinHash recognition (a similarity proxy)
  provenance.py    # the source axis: author vs mirror vs collaboration vs external
  ledger.py        # append-only, hash-chained, timestamped record of readings
  semantics.py     # a diachronic algebra of senses (descent lattice; incl. abstraction)
  glossary.py      # the authored map: concepts, attested usages (phonetic + conceptual)
  reading.py       # the three layers: attest (L1) / read (L2) / drift + project (L3)
  alignment.py     # purpose x fidelity (phonetic) / purpose x resonance (conceptual)
  memory.py        # the return path: remember() + memory_chain() — inverse of projection
  imprint.py       # the active recorder (default author: anise.damm)
  manifest.py      # defensive-publication manifest
glossary.json              # breath signs (labrys, ankh, ouroboros, myth) + pump words
interpretation_ledger.jsonl  MANIFEST.md
docs/thought-flow.md       # the living reasoning journal behind the design
tests/                     # the suite (89 tests)
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

## The breath/pump threshold: attention before the phoneme

The deepest reading the framework supports. A culture's **mode of attention**
governs how it commits meaning to a lasting form:

- **breath** — a participatory, holistic attention. Meaning is carried *whole*, by
  a **conceptual** sign: a symbol that holds a weighted field of values at once.
  Writing is reserved for what is profound enough to need a form that outlives word
  of mouth. (Barfield's "original participation"; McGilchrist's right hemisphere.)
- **pump** — an analytic, segmenting attention. Meaning is mechanised into
  discrete, re-combinable **phonetic** units that spell a sound and defer meaning to
  a lexicon. (The left hemisphere's grasping, re-presenting world.)

The script follows the attention. So the **labrys** — the Minoan double axe — is
not the word "axe": it is a breath-era sign holding *paradoxical equilibrium*
(opposed blades in balance), *sovereignty*, *divinity*, and *belonging*, all at
once and in proportion.

```
$ python -m interpretation weigh labrys-knossos
labrys (labrys-knossos) — a breath/conceptual sign
  retained field: paradoxical-equilibrium (0.30), divinity (0.25), sovereignty (0.25), unity-belonging (0.20)
  committed to writing because: to hold and transmit the society's axis — balanced
    sovereignty, the divine, and belonging — in a form that outlived any one voice
```

That last line is the framework's answer to *what made a thing important enough to
require a way to translate it, available to everyone* — the action behind the
intention, recorded on the sign itself.

**Reading meaning as weighted alignment, not strict lexicon.** A symbol is not
looked up; it is *read* by proposing how its weight is distributed. A reading is
true insofar as it **resonates** with the field the culture retained:

```
$ python -m interpretation read labrys-knossos
reading labrys-knossos as a weighted field: paradoxical-equilibrium (0.30), divinity (0.25), ...
  resonance with the retained field: 1.00
```

**The ghost lag, made catchable.** The cardinal error is to read a breath-era sign
in the pump mode — as if it spelled a word. That is **phonetic projection**, and it
is the deeper sibling of anachronism: where anachronism projects a later *sense*,
this projects a later *mode of attention*.

```
$ python -m interpretation project labrys-knossos
PHONETIC PROJECTION: reading labrys-knossos (breath/conceptual) in the phonetic mode
  - imposing a later mode of attention, as if the sign spelled a word;
    ghost lag 800 year(s) across the threshold
```

**Myth as conceptual memory.** Going back through this lens, a myth is not a story
but a *memory* — a remembered state-shift, embedded enough to keep its place,
lifted up a ladder of abstraction (each rung the `abstraction` shift in the sense
lattice), each form making the memory more transmissible:

```
$ python -m interpretation trace divine-order
    pre-literate  elemental: the elements as living powers  [origin]
      Bronze Age  primal: primal/chthonic powers, personified  [abstraction]
  Archaic Greece  olympian: the ordered Olympian pantheon  [abstraction]
      Classical–  allegorical: gods as allegories of forces  [abstraction]
```

Hesiod's *Theogony* (c. 700 BCE) is recorded as the **phonetic crossing**: a
breath-era memory written down *at* the threshold, "so the memory would not be lost
as the mode of attention changed." To read it literally — as a genealogy of actual
beings — is phonetic projection; to read it as conceptual memory is to hear it in
its own regime.

So the second factor of alignment is re-read for this regime as **resonance**:

> **interpretive alignment = purpose × resonance** (conceptual regime)

where `resonance` is the weighted-field coherence with the retained conceptual
truth. A reading that imposes the phonetic mode forfeits all resonance — the
published `MANIFEST.md` carries the labrys read faithfully (value `1.00`) beside a
recorded *foil*, the labrys read as a syllable (value `0.00`, "phonetic
projection"), so the evidence record shows the error being caught.

### The return path: remembrance (the inverse of projection)

Projection and remembrance both traverse the ghost lag, in opposite directions and
with opposite valence. **Projection** drags the *present* mode of attention *back*
over a *past* sign — an error, it imposes. **Remembrance** carries a *past*
conceptual truth *forward* into a *later* record — a virtue, when faithful, it
preserves. Myth is the paradigm: a pump-era text that keeps a breath-era truth alive
across the threshold. `remember` scores how faithfully it does so — the resonance of
what the record carries with what the culture retained, and the span it reached back:

```
$ python -m interpretation remember theogony
REMEMBRANCE: theogony carries 'divine-order' back 2300 year(s) across the threshold
  (resonance 0.85)  ->  a faithful remembrance: the breath-era truth is carried back intact

$ python -m interpretation remember ouroboros-alchemy
REMEMBRANCE: ouroboros-alchemy carries 'ouroboros' back 1600 year(s) across the threshold
  (resonance 0.90)  ->  a faithful remembrance: the breath-era truth is carried back intact
```

When the carried field no longer resonates with the retained truth, the memory has
*lapsed* — "a projection in disguise" — so the same number that scores a faithful
return also catches a return that failed. Like every measure here but attestation, it
is **descriptive, never a gate**: it measures the return; a human judges the memory.

**The transmission lineage.** A truth is rarely carried in one hop. `chain` traces
it through *successive* rememberings, reporting at each link its **to-origin**
resonance (cumulative drift from the source truth) and its **to-prev** resonance (the
faithfulness of that single hop), and marking whether the memory **decayed** or was
**restored**:

```
$ python -m interpretation chain ouroboros
memory chain of 'ouroboros': 3 remembering(s) over 3250 year(s); survival 0.85, low-water 0.55 (decayed then restored)
   origin  ouroboros               to-origin 1.00  to-prev —
      300  ouroboros-alchemy       to-origin 0.90  to-prev 0.90  [decayed -0.10]
     1478  ouroboros-medieval      to-origin 0.55  to-prev 0.55  [decayed -0.35]
     1950  ouroboros-jung          to-origin 0.85  to-prev 0.45  [restored +0.30]
```

The serpent's unity-of-opposites is carried faithfully into Greco-Egyptian alchemy,
worn down to mere ornament in late-medieval heraldry, then **restored** by a modern
reading that returns to the source. Restoration is real and measurable: a later
record can recover a truth an earlier one let slip — which is how a breath society's
values survive the great change in attention, not in one carry but down a lineage.
This is the sibling system's `trace` (the thread of conclusions) turned on the return
path. Descriptive, never a gate.

## The worked example: *revolution* (the pump-regime contrast)

The textbook case of conceptual history (Koselleck's own), and the **phonetic
contrast** to the breath-era signs above. The **word** held still while the
**concept** inverted:

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

## Interpretive alignment = purpose × fidelity (phonetic regime)

Where does one reading sit among the others recorded for a concept? In the **pump
/ phonetic** regime, the framework uses the sibling system's `alignment = purpose ×
truth`, with **truth re-read as fidelity to the historical usage** (in the **breath
/ conceptual** regime the second factor is **resonance**, above; one command,
`align`, dispatches on the regime of the sign being read):

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
