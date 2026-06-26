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
  memory.py        # the return path: remember() / memory_chain() / confluence()
  constellation.py # the system-level web: which values were load-bearing across a regime
  migration.py     # a value across the threshold: held whole, then dispersed into lexemes
  condensation.py  # binary thought (compression) vs relational meaning (condensation): the bit + its field
  weave.py         # the antonym couples as one web: root couples, the branching hubs, the keystone word
  frontier.py      # the leaf-edge of the tree: unpolarised, singular, experiential words at the frontier
  cornerstone.py   # the root-base of the tree: innate, self-standing words built on nothing (frontier's dual)
  dimension.py     # the tree as a system: conveyance (symbol/story/word) × culture × time × depth
  lexicon.py       # phonetic language over time: the explosion, sieve->success, coherence
  arc.py           # one thread traced unbroken across both regimes (migrate + proliferation)
  signal.py        # the capstone: signal = integrity x direction(truth) — the record on itself
  atlas.py         # the whole history of meaning composed on one screen (a reader, not a ruler)
  imprint.py       # the active recorder (default author: anise.damm)
  manifest.py      # defensive-publication manifest
glossary.json              # breath signs + pump words + value_aliases + migrations
lexicon.json               # the phonetic lexicon traced over time (the explosion)
relations.json             # the authored map of meaning-connections (antonyms + synonyms)
interpretation_ledger.jsonl  MANIFEST.md
docs/thought-flow.md       # the living reasoning journal behind the design
tests/                     # the suite (166 tests)
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

**Confluence: independent paths that corroborate — or fork.** When *two lineages that
never copied each other* remember the same source truth, their meeting is evidence.
`confluence` groups the rememberings into independent paths (by whether one remembers
the other) and weighs them: independent lineages that **converge** on the same
conceptual field corroborate the source — the return-path analogue of the sibling
system's *independent corroboration* — while lineages that **diverge** mark a fork in
the tradition.

```
$ python -m interpretation confluence ouroboros
CONFLUENCE: 2 independent lineages converge on 'ouroboros' — the retained truth is independently corroborated
    ouroboros-alchemy  [ouroboros-alchemy -> ouroboros-medieval]  witness ... to-origin 0.90 (preserves)
    ouroboros-jung     [ouroboros-jung]                           witness ... to-origin 0.85 (preserves)
    ouroboros-alchemy x ouroboros-jung: 0.90 (converge)

$ python -m interpretation confluence labrys
DIVERGENCE: of 2 lineages remembering 'labrys', 1 preserve(s) the source; the lineages have forked into incompatible memories
    labrys-emblem     witness ... to-origin 0.40 (diverged)     # re-read as sovereign power and group identity
    labrys-religious  witness ... to-origin 0.95 (preserves)    # the sacred equilibrium kept
    labrys-emblem x labrys-religious: 0.40 (diverge)
```

The Egyptian-rooted alchemical reading of the ouroboros and a modern reading arrive
*independently* at its unity-of-opposites (0.90) — so the truth is corroborated, not
an artifact of one transmission. The labrys, by contrast, has **forked**: a
religious-historical lineage keeps its paradoxical equilibrium while a later emblematic
one re-reads it as sovereign power and group identity — incompatible memories of one
sign, surfaced and named, never adjudicated.

### The constellation: the web's load-bearing values

The single sign, the chain, the confluence — then the whole web. `constellation`
lifts to the system level and asks which conceptual *values* were load-bearing
*across* a regime: recurring, with weight, across many signs. It is "systemic
alignment and underlying values retained across time and culture" made a measurement.

```
$ python -m interpretation constellation
constellation of the breath web: 4 sign(s), 5 load-bearing value(s)
  keystone value: divinity (reach 3, weight 0.80)
  load-bearing values (carried across signs):
    divinity     reach 3  weight 0.80
    unity        reach 2  weight 0.70
    equilibrium  reach 2  weight 0.60
    eternity     reach 2  weight 0.40
    sovereignty  reach 2  weight 0.40
  kinships (signs sharing a value-field):
    labrys x ouroboros: 0.50
    ankh x labrys: 0.40
  clusters: [['ankh', 'labrys', 'ouroboros'], ['divine-order']]; islands ['divine-order']
```

Across the Minoan labrys, the Egyptian ankh, the ouroboros, and the remembered divine
order, **divinity** is the keystone — the value the breath web rests on — with unity,
equilibrium, eternity, and sovereignty carried across signs beneath it. The **labrys
is the hub** (it shares equilibrium with the ouroboros, divinity and sovereignty with
the ankh), while the cosmogonic *divine-order* sits apart as an **island**. The value
vocabulary is harmonised through the glossary's *authored* `value_aliases` (so
*eternity* and *eternity-continuity* are seen as one value) — a proxy grouping
surfaced in the map, not hidden. And the pump regime, asked the same question, holds
**no weighted web at all** (`constellation --regime pump` → 0 signs): it segments
meaning into lexical senses rather than holding it in fields — the breath/pump
difference, seen from the top. Descriptive, never a ranking of worth.

### Migration: a value across the threshold (how the transition redistributed it)

The constellation says which values the breath web rested on; `migrate` tracks *one*
value across the breath→pump threshold — where it concentrated when held **whole**, and
into which separate pump-era lexemes it dispersed when meaning was **segmented**. This
is the founding question made traceable: *how the pump transition redistributed the
values.*

```
$ python -m interpretation migrate equilibrium
MIGRATION of 'equilibrium': held whole across 2 breath sign(s) (weight 0.60); dispersed into 4 pump-era lexeme(s)
  The labrys held opposed blades in balance as one paradoxical whole; the pump regime
  carved that holism into separate analytic concepts ...
  breath side (held whole, with other values): labrys (0.30), ouroboros (0.30)
  pump side (segmented into separate lexemes):
    balance      — the static evenness of two weights — the physical facet, the paradox flattened
    justice      — balance moralised — giving each their due
    moderation   — balance as a personal virtue, the mean between extremes
    symmetry     — balance as formal, aesthetic correspondence
```

The labrys's **paradoxical equilibrium** — opposed blades held as one — is the case
the whole framework began from. The pump regime split it into *balance* (mechanics),
*justice* (law), *moderation* (virtue), *symmetry* (form): four lexical domains, each
keeping a shard, all dropping the *paradox* of opposites-held-as-one that made it one.
`divinity`, the keystone, likewise disperses into *the sacred*, *the holy*,
*transcendence* — set apart from the world it had pervaded. The breath side is
**measured** from the signs; the dispersal is **authored** (`migrations` in the
glossary) — a proxy reading of the redistribution, surfaced in the map, not a claim of
strict etymology. Holism becomes segmentation, and you can watch it happen,
value by value.

## Binary and relational meaning: compression vs condensation

Beneath every sign, breath or pump, lies the bare unit of natural computing: the
**bit**. Information reads `0` or `1` — *yes/no*, *signal/noise*, *true/false*,
*right/wrong*. A bit is a **pure distinction**: it separates two states and carries
nothing else. That is **compression** — meaning squeezed to the single yes/no that
transmits with perfect fidelity, fixed, singular, exact, and empty of all but the cut.

Human thought is built on the same distinction — a word draws a boundary, and its
sharpest form is the **antonym**, the pole it stands against. So a word is *binary in
structure*: under it lies the one bit. But a word does not stop at the cut. Onto that
binary skeleton it **condenses** an associated field — its **synonyms** and its
connections to other concepts — so the fixed bit takes on a relational, proportional,
*meant* content the bit alone can never hold. **Condensation** is the opposite gesture
to compression: not the loss-less squeezing of meaning into one bit, but the accretion
of associated sense *around* a distinction, so one token carries far more than one bit.

```
$ python -m interpretation condense signal
BIT: 'signal' is pure compression — the distinction signal|noise, one bit, no field condensed upon it
  compression (the bit): 1  [pole(s): noise]
  condensation (meaning on the bit): 0

$ python -m interpretation condense justice
CONDENSED: 'justice' keeps the bit (justice|injustice) and condenses 14 meaning(s) upon it (ratio 14:1)
  compression (the bit): 1  [pole(s): injustice]
  condensation (meaning on the bit): 14
    associated field (synonyms / connections): boundary, debt, equilibrium, equity, fairness, freedom
    compounded over time over ~39500 year(s) from 8 earlier word(s): water, fire, kin, seed, ...
```

*signal* is the floor: a pole, no field — the bit. *justice* keeps that very bit
(*justice* | *injustice*) and condenses a field of associated meaning on it. The
`ratio` is the headline — **compression (binary) vs condensation (meaning)** as one
number: how much meant content rides on the single yes/no.

**Compounded meaning over time.** The field is not assembled at once. Language is the
**compounded creation of meaning over time**: a later word is *defined in terms of*
earlier ones (the lexicon's web, §the explosion), so its meaning is its whole ancestry
compounded into it. *wellbeing* condenses *flow* and *freedom*, which condense *self*
and *justice*, down to *water* and *fire* — ~42,000 years of meaning condensed into one
token. The deeper the ancestry, the more time the word carries.

**Synonyms and antonyms — the two kinds of meaning-connection.** An **antonym** is the
binary axis itself (the compression — a single distinction); a **synonym** is condensed
meaning shared (the relational content). `connect` reads which a pair are, and for
terms neither opposed nor kin but sharing a field, reports them *associated* with the
overlap of their gathered meanings:

```
$ python -m interpretation connect signal noise
ANTONYM: signal|noise — opposed poles, the binary axis: one distinction (compression)

$ python -m interpretation connect freedom wellbeing
ASSOCIATED: freedom … wellbeing — connected by a shared field (overlap 0.60)
  shared meaning: boundary, debt, fire, harvest, justice, kin, season, seed, self, soul, time, water
```

The relations are an **authored map** (`relations.json`), a proxy carrying its
provenance, not a real thesaurus; the compounding is read from the lexicon. As ever,
descriptive, never a gate.

### The weave: the antonym couples as one relational web

`condense` and `connect` read a term or a pair; `weave` lifts them to the **whole
web** — the way `constellation` lifts a single breath sign to the system-level web of a
regime's shared values. It reads every antonym couple and every shared-meaning edge at
once, and answers the three questions only the web entire can:

```
$ python -m interpretation weave
the meaning web: 14 antonym couple(s), 4 root(s), 14 term(s)
  root antonyms (always paired, no matter how derived — both poles irreducible):
    false|true
    noise|signal
    no|yes
    right|wrong
  hubs (the most branches and overlap of synonyms and antonyms):
    freedom      branches 7  overlap 5  [pole(s): bondage]
    justice      branches 7  overlap 3  [pole(s): injustice]
  keystone — the key defining word the most truth of meaning lies in: self
    7 other word(s) are defined in terms of 'self'; branches 6, overlap 4
```

- **Which root antonyms are always paired, no matter how derived?** The couples where
  *neither* pole carries a condensed field — both are irreducible bits:
  **true|false**, **signal|noise**, **yes|no**, **right|wrong**. However much meaning is
  later condensed and compounded on top, a derived opposition (*justice* | *injustice*)
  is a *refinement* — a root distinction with a field grown on it; it bottoms out on
  these four. They are the web's binary bedrock.
- **Which words have the most branches and overlap?** The **hubs**: *freedom* and
  *justice*, tied at seven branches, *freedom* edging ahead on overlap. They are where
  the most synonym/antonym/associate edges meet — the knots that bind the web.
- **In which key defining word does the most truth of meaning lie?** The **keystone**:
  **self**. Seven other words — *soul, freedom, flow, empathy, alienation, ubuntu,
  mamihlapinatapai* — are defined *in terms of* it. Meaning is relational, so the truth
  of it gathers where the web leans hardest: the reflexive *I* that the inner-life
  vocabulary is built upon. (It is the gateway of the framework's own arc — *self* →
  *freedom* → *wellbeing* — now shown to be the word the rest most depend on to mean
  what they mean.)

The keystone is read, not crowned: `weave` surfaces where the web's truth gathers and,
like every measure here but attestation, **gates nothing**.

### The frontier: meaning at the leaf-edge of the tree

The `weave` reads the web's *settled* structure; `frontier` reads its **edge**, where
comprehension is still reaching. Three kinds of word live there — and they are one kind
seen from three sides:

- **no absolute antonym** (*unpolarised*) — the word draws no clean distinction; it
  names a *positive presence*, a perception held in itself. Where a bit is all boundary
  and no content, these are all content and no boundary.
- **no synonym** (*singular*) — no other word can stand in for it, so it cannot be
  compressed away. It carries meaning nothing else carries: maximal information, zero
  redundancy — the exact opposite of a bit, which any yes/no can replace.
- **a leaf of the tree** — nothing is yet *defined in terms of* it; it sits at the
  growing tip. The interior is comprehended and load-bearing; the leaves are the
  frontier.

```
$ python -m interpretation frontier
the frontier of the tree: 9 experiential leaf-word(s), 6 unwoven (no antonym, no synonym); furthest out: mamihlapinatapai
  the reaching edge (leaf, experiential — abstract perception newly named):
    mamihlapinatapai    1860  align 0.90  no-antonym no-synonym    score 0.90  — a singular perception, unwoven — pure frontier
    ubuntu              1846  align 0.88  no-antonym no-synonym    score 0.88  — a singular perception, unwoven — pure frontier
    hygge               1920  align 0.85  no-antonym no-synonym    score 0.85  — a singular perception, unwoven — pure frontier
    saudade             1400  align 0.85  no-antonym no-synonym    score 0.85  — a singular perception, unwoven — pure frontier
    sublime             1750  align 0.83  no-antonym no-synonym    score 0.83  — a singular perception, unwoven — pure frontier
    nostalgia           1688  align 0.82  no-antonym no-synonym    score 0.82  — a singular perception, unwoven — pure frontier
    empathy             1909  align 0.88  polarised  redund 0.50   score 0.26  — an experiential edge, partly woven in
    ...
  furthest out: 'mamihlapinatapai' — the wordless shared look of two who each wish the other would begin
  contrast — unpolarised but interior (no antonym, yet long comprehended): flow, melancholy, time, …
```

A word that is all three — an unpolarised, singular, experiential leaf — is meaning at
**the frontier of comprehended knowledge we can communicate**: an *abstract
representation of contextual perception*, named once and not yet woven into the web of
oppositions and equivalences. The untranslatables are the paradigm, and **mamihlapinatapai**
— *the wordless shared look of two who each wish the other would begin* — sits furthest
out: a leaf with no opposite and no equivalent, meaning at the very edge of what language
has managed to say.

The score is a **product** (the framework's signature): leaf, experiential, unpolarised
and singular all push a word out; any pull toward the settled interior lowers it. So the
listing is a gradient — from *wellbeing* (an experiential leaf, but already given an
opposite, *suffering*, and equivalents, *flourishing/welfare* — partly woven in) out to
the wholly singular untranslatables. And the honest contrast is kept: being unpolarised
is *not* the frontier — *time* has no antonym yet sits deep in the interior, long since
comprehended and built upon. **The map's silence about a word — no opposite, no
equivalent — is itself the mark of the frontier**, and an authored proxy, not a proof.
Descriptive, never a gate.

### The cornerstones: meaning at the root-base of the tree

`frontier` reads the leaf-edge; `cornerstones` reads its **dual** — the **root-base**,
the words built on *nothing*, so fundamental and innate that the whole tree rests on
them. If the frontier is where comprehension is still reaching, the cornerstones are
where it *begins*: the base of the depth itself.

```
$ python -m interpretation cornerstones
the root-base of the tree: 4 cornerstone(s) (built on nothing); the base of the depth: fire (20 rest on it)
  the cornerstones (built on nothing, innate, self-standing — the given base):
    fire     primal    innate 0.95  support 20  self-standing  score 0.95  — a cornerstone — built on nothing, needs no relational associate: the given base
    kin      primal    innate 0.85  support 18  self-standing  score 0.77  — a cornerstone — built on nothing, needs no relational associate: the given base
    water    primal    innate 0.95  support  8  self-standing  score 0.38  — a cornerstone ...
    danger   primal    innate 0.90  support  1  self-standing  score 0.04  — a cornerstone ...
  contrast — derived pillars (load-bearing, yet built on earlier words): season (support 19, depth 1), time (support 14, depth 2), soul (support 12, depth 4)
```

A cornerstone is one kind of word seen three ways: **a root of the tree** (nothing in
its ancestry — built on nothing, with maximal *support*, the count of words that rest on
it); **innate / given** (the sieve end of the axis — *water*, *fire*, *kin*, *danger*, the
concrete necessities given before abstraction begins); and **self-standing** (needing
*no relational associate* — *water* means water with no opposite to define it against and
no synonym to replace it).

That last property is the deep symmetry with the frontier: **both the cornerstone and the
frontier word stand without a relational associate, for opposite reasons.** The frontier
word has none because the web has *not yet reached* it (it reaches outward); the
cornerstone has none because it is so foundational it *needs* none (everything reaches
back to it). Same silence on the map, opposite nature — the two ends of the tree.

The **base of the depth itself** is the cornerstone the most rests on: **fire** (the
elemental given, 20 of 27 words ultimately compound down to it), with **kin** beside it
(the social given, 18). And the honest contrast the framework always keeps: *season*,
*time* and *soul* bear enormous weight but are **derived pillars**, not roots — *time* is
built on *season*, which is built on *fire*. Being relied upon is not being a root; the
base is what is built on nothing.

### Dimensional meaning: the tree as a system of layered axes

Step back from the single tree and a larger shape appears, the one every layer has been
building toward: **the conceptual language tree is the system**, and meaning is not laid
along one line but located in a space of several **dimensions**, each a distinct way
meaning is layered — each conveyance adding meaning the others cannot reach.

```
$ python -m interpretation dimensions
the tree as a system: 3 conveyance mode(s) × 5 culture(s) × 5 era(s) = 75 cell(s) of dimensional meaning, over depth 0–14
  the conveyance dimension (each a way of conveying meaning the others cannot reach):
    symbol     3  (non-phonetic)
    story      6  (non-phonetic)
    word      32  (phonetic)
  the culture dimension (each tongue its own derivation): shared, Danish, Nguni, Portuguese, Yaghan
  the time dimension (layered over history, breath stratum beneath): primal, agrarian, classical, modern, reflexive
  the depth dimension (the vertical): cornerstone 0 → frontier 14
  cross-dimensional values (carried as symbol AND word — the richest dimensional meaning):
    divinity, equilibrium, unity
```

- **conveyance** — *how* meaning is committed to a lasting form. Two are non-phonetic,
  holding meaning whole: the **symbol** (a breath/conceptual sign — the labrys, the ankh)
  and the **story** (a breath truth carried in phonetic words — a myth like the
  *Theogony*). One is phonetic: the **word**. A thing said in a symbol is not the thing
  said in a word — each mode is a dimension.
- **culture** — each language/dialect has its own derivation (the shared lexicon, and
  each tongue the untranslatables come from), layered like constellations and webs that
  need not coincide.
- **time** — the eras, over history, with the breath stratum beneath the threshold.
- **depth** — the vertical the rest of the framework reads: cornerstone (0) → frontier.

A concept in one cell — a single modern shared word, one mode, one culture, one era — is
*flat*. A value carried as a **symbol** in the breath regime and re-derived as **words**
in the pump regime is **cross-dimensional**: *equilibrium*, *divinity*, *unity* (the
values `migrate` and `arc` already trace) occupy the conveyance dimension in more than
one mode, and their meaning has extent the flat word's cannot. The space is an authored
proxy of the system's shape — descriptive, never a gate.

## The phonetic web over time: the explosion of understanding

The breath apparatus reads signs that held meaning whole. Its **pump-side
counterpart** reads phonetic language the other way — *forward*, as it proliferates.
Phonetic language does not hold meaning whole; it explodes into words, each a concept
a culture deemed worth a name (a lexeme's `valued_for` — the phonetic echo of
`committed_because`). Traced over time, that explosion is the record of how human
understanding of conceptual meaning grew, and three things move together inside it:

```
$ python -m interpretation proliferation
the explosion of phonetic language, traced era by era:
  era         new  total  align   exp  coher
  primal        4      4   0.09  0.00   0.25
  agrarian      5      9   0.22  0.00   0.89
  classical     5     14   0.35  0.07   0.93
  modern        6     20   0.48  0.30   1.00
  reflexive     7     27   0.59  0.48   1.00
  over 5 eras the lexicon grew 4->27; sieve->success alignment rose 0.09->0.59;
  experiential share 0.00->0.48; coherence 0.25->1.00
```

- **The explosion** — the count of lexicalised concepts climbs era over era (4 → 27).
- **The sieve→success gradient** — what gets named drifts from *sieve-aligned* (a
  discriminating filter on raw experience: *water*, *danger*, *kin* — concrete
  necessity) toward *success-aligned* (abstract, experiential, aspirational: *soul*,
  *freedom*, *empathy*, *wellbeing* — what a thriving society values). Mean alignment
  climbs 0.09 → 0.59.
- **Coherence and experience, together** — later words are defined in terms of earlier
  ones, so the lexicon's definitional web connects; as it coheres (0.25 → 1.00), more
  abstract and *experiential* concepts become sayable (inner-experience share 0.00 →
  0.48). Understanding of human experience grew *as* the web cohered — exactly the
  higher-coherence society's deepening self-understanding, made a measurement.

And lexicalisation is **valuation** — which is why dialects differ in what they name.
A concept earns a word when a tongue values it enough, and `untranslatables` reads the
concepts one tongue valued that the shared lexicon left unnamed:

```
$ python -m interpretation untranslatables
4 concept(s) a single tongue valued enough to name:
  hygge (Danish) — cosy, safe togetherness worth seeking
  ubuntu (Nguni) — I am because we are — personhood through others
  saudade (Portuguese) — a longing for an absent, perhaps unrecoverable beloved or time
  mamihlapinatapai (Yaghan) — the wordless shared look of two who each wish the other would begin
```

So the two regimes meet from opposite directions: the breath web held many values
*whole* in few signs; the pump web *segments* them and then, over millennia, builds an
ever-finer, ever-more-coherent vocabulary back up toward the inner life — the migration
(holism → segmentation) and the proliferation (segmentation → re-coherence) are the
same threshold, read in both directions. As ever, an authored map and a proxy
throughout; descriptive, never a gate.

### The arc: one thread, unbroken across both regimes

`migrate` and `proliferation` are the same threshold read in opposite directions;
`arc` puts them on **one timeline** for a single value — the breath sign that held it
whole, the threshold where it dispersed, and the lexeme-thread it then climbed back up.
The flagship is the framework's first example, *paradoxical equilibrium*:

```
$ python -m interpretation arc equilibrium
arc of 'equilibrium' across the threshold:
  breath    — held whole in labrys (0.30), ouroboros (0.30)
  threshold — dispersed into 4 shard(s): balance, justice, moderation, symmetry
  pump      — 1 shard re-lexicalised: justice->justice
  re-coherence (the thread climbs):
      -500  justice      align 0.60
      -450  virtue       align 0.62
      1700  freedom      align 0.74
      1844  alienation   align 0.85
      1990  wellbeing    align 0.92
  the thread reaches align 0.92 over ~3590 year(s) — from a sign held whole to
  flourishing named, unbroken across the ghost lag
```

The Minoan labrys held equilibrium **whole**; the threshold scattered it into
*balance, justice, moderation, symmetry*; one shard, **justice**, re-entered the
phonetic web; and from there the definitional thread climbs — justice → virtue,
freedom → … → *wellbeing* — the sieve→success alignment rising the whole way, from
`0.60` to `0.92`. A single conceptual thread, traced unbroken from a Bronze-Age double
axe to *flourishing* named, across ~3,590 years and the great change in attention. A
shard no lexeme carried (e.g. *divinity*'s) is reported, honestly, as dispersed but not
re-traced. Descriptive, never a gate.

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

## The capstone: signal = integrity × direction(truth)

The framework turns its discipline on itself, exactly as the sibling system does. One
verdict, a **product** — either factor at zero zeros it, because a failsafe is
trustworthy or it is not:

```
$ python -m interpretation signal
signal = integrity(1) x direction(truth)(1) = 1  ->  a trustworthy backing for the interpretation of conceptual history
  integrity = 1
    chain:    OK
    manifest: OK (head still commits to the ledger)
  direction(truth) = 1
    grounded:   OK (every reading rests on an attested sign)
    provenance: OK (every record names author and source)
```

- **integrity** — the record is *sound*: the hash chain verifies (no reading altered
  or reordered) and the published manifest is *fresh* (its head still commits to the
  current ledger).
- **direction(truth)** — the record is *pointed at the truth*: every reading is
  grounded in a sign that passes L1 attestation, and every record names its author and
  provenance.

A recorded *projection* — the labrys read phonetically, kept as a named foil — does
**not** lower the signal: it is grounded and attributed, and the framework correctly
reads its alignment as zero. That is the system working, the way a retraction is
standing, not a break. CI runs `signal` on every push, so the repository proves its own
`signal == 1`. This closes the arc back to the sibling the framework was born from.

## The atlas: the whole on one screen

Every module reads one thing; `atlas` reads them *together*, composing the tested
measures into a single narrative of the arc the framework has traced — a reader, not a
ruler (the sibling system's `status` move), introducing no new measure and gating
nothing:

```
$ python -m interpretation atlas
== atlas: the history of meaning this record assembles ==
  signal:    1  (trustworthy backing)
  breath web — keystone value: divinity (reach 3); hub sign: labrys; islands ['divine-order']
  the threshold — values held whole, then dispersed:
    divinity     held 0.80 across 3 sign(s) -> 3 lexeme(s)
    equilibrium  held 0.60 across 2 sign(s) -> 4 lexeme(s)
    unity        held 0.70 across 2 sign(s) -> 3 lexeme(s)
  the pump explosion — lexicon 4->27 over 5 eras; sieve->success 0.09->0.59; experiential 0.00->0.48; coherence 0.25->1.00
  the unbroken arc — equilibrium: justice(0.60) -> ... -> wellbeing(0.92), reaching 0.92 over ~3590 year(s)
```

The whole journey at a glance: the backing is sound; the breath web rests on
*divinity*, hubbed at the *labrys*; those whole-held values dispersed at the threshold;
the phonetic lexicon then exploded and re-cohered, climbing from survival toward the
inner life; and one thread — *equilibrium* — runs unbroken from a Bronze-Age sign to
*flourishing* named. One screen for the entire arc.

## Relationship to `integrity-alignment-system`

This is a **sibling**, not a fork. It carries over that project's spine, its
`fingerprint`/`provenance`/`ledger`/`manifest` mechanism, and its discipline of
never letting a proxy wear a proof's clothes — and turns them from *information
integrity* toward *the interpretation of conceptual history*. The full reasoning,
in the order it arrived, is the living journal in
[`docs/thought-flow.md`](docs/thought-flow.md).
