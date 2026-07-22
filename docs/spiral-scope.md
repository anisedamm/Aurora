# Scope — the *spiral*: re-coherence and the information age

> **Status: SCOPING COMPLETE. Architecture locked; build-ready (plan in §21); code not yet started.**
> Supersedes the earlier `net-regime-scope.md`, which framed the information age as a
> third *regime pole*. This revision reframes it as the **closing of a spiral**: the
> layers become a cycle, the headline measure inverts from *division* to *return*, and
> the information age (**nerve**) is named as the phase where the pump's segmentation
> **re-coheres into a new whole at greater complexity**. It now carries worked examples
> spanning a **two-facet** (structural × substantive) spectrum — nerve-born (§10 *viral*;
> §12 *meme*/*friend*/*cloud*/*wiki*) and breath-origin (§14 *equilibrium*, the additivity
> proof) — the `recoherences` data model (§11), the nerve **lexicon** side (§13), the
> `aspects` whole-picture view (§15), and an **adversarial** pass (§16, *spam*) that bounds
> the thesis — the spiral must be able to *refuse*. The regime is **`nerve`** (the *mode*;
> the *net* is its medium), defined as a bodily/hemispheric system in §1. A review pass
> added the fragmentation measure (§17 `scatter`), the reflexive-reader risk (§18), and
> L1's nerve-regime traps (§19). All sixteen decisions (§9) are settled and the build plan
> is in §21 — scoping is **done**.

## 0. The turn

The framework's headline measure is L3's **gap** — a measure of *division* (how far a
reading has drifted from the usage's own time). The information age does not ask for a
*further* division. It asks the mirror question:

> *Not "how far does this further divide?" but "how does this established division
> **re-cohere** to the truth of the change in attention mode, as it reconverges with
> greater complexity?"*

So the extension is not a new pole on the attention axis. It is the **return arm of a
spiral** the framework already half-draws:

- breath **held meaning whole** (one sign, a weighted field of values, in proportion);
- pump **segmented** it (one word, one sense, deferred to a lexicon);
- **nerve returns the segmented pieces to a whole** — but a *differentiated* whole that
  keeps the analysis it re-coheres. Wholeness regained *at greater complexity*.

The framework already says this in two voices and never named the third phase:
`migrate` reads holism → segmentation; `proliferation` reads segmentation →
re-coherence (its coherence climbs `0.25 → 1.00`); `atlas` narrates *"the long labour
of language has been to re-cohere those words."* **Nerve is the regime where that
re-coherence completes.** Its emblem is already in the glossary: the **ouroboros** —
unity-of-opposites, the serpent returning to its own origin.

## 1. The spiral — three phases of a meaning

Three phases, because there are **three modes of attention** — and the framework names
them as a **bodily / hemispheric system**: each a great system of the body, each a
hemisphere-world in McGilchrist's sense. The *technology* of each (its script, its medium)
is **downstream** of the attention, never its name — which is exactly why the regime is
**`nerve`**, not *net*: the net is its **medium**, as the alphabet is the pump's. This
distinction is what keeps the term legible.

| regime | the body | hemisphere-world | mode of attention | native script | its medium |
|--------|----------|------------------|-------------------|---------------|------------|
| **breath** | the lung — respiration | right: participatory, present, contextual | **holistic** — meaning carried *whole* | conceptual (a weighted-field sign) | the carved / incised symbol |
| **pump** | the heart — circulation, the machine | left: grasping, abstracting, re-presenting | **analytic** — meaning *segmented* into units | phonetic (a sign spelling a sound) | the alphabet, the press |
| **nerve** | the nervous system — the body's own network | the network of both, mechanised | **associative** — meaning *recombined* from a field | recombinant (sense from neighbours / remix) | the net, the internet |

> **Read `nerve` as the *mode*, `net` as its *medium*.** The nerve regime is to the net
> what the pump regime is to the alphabet: the attention, not the technology. (`breath`
> and `pump` are inherited unchanged from the framework's `regime.py`; `nerve` is the
> additive third.)

Breath holds whole, pump segments, **nerve re-combines** — and the nerve regime is where
the segmented pieces *can* return to a whole. Those are the three phases:

| phase | regime | what happens to meaning | already in the code |
|-------|--------|-------------------------|---------------------|
| **whole** | breath | held as one weighted field | `weigh`, `read`-as-resonance |
| **segmented** | pump | dispersed into discrete lexemes/senses | `migrate` (holism → segmentation) |
| **re-cohered** | **nerve** | the segments return to a whole | `proliferation`, `confluence`, `arc` |

It is a **spiral, not a circle**. Breath's whole was *undifferentiated* (whole because
never divided); nerve's whole is *differentiated* (it re-coheres the pump's analysis
without discarding it — holding the unity **and** the segmentation at once). That extra
content is the "greater complexity," and it is **measurable** (§3).

## 2. The layers become a cycle (the ouroboros)

The three layers are today a one-way ladder. The spiral adds a fourth that **closes
the loop back to the first, one rung higher**:

| | layer | question | output | gates? |
|---|-------|----------|--------|--------|
| **L1** | Attestation | Is the usage *real*? | admissible / not | **yes** |
| **L2** | Reading | What did it mean *here*? | a described sense / field | no |
| **L3** | Anachronism | Has the reading drifted from *then* into a *later* sense? | the then→now gap | no |
| **L4** | **Re-coherence (`spiral`)** | Do the segmented pieces **return to a whole**, faithful to the retained truth? | the return-resonance × complexity | no |

L4 → re-attest the new, more complex whole → the spiral turns again. The layers stop
being a ladder and become the ouroboros — the framework's own seed sign is the diagram
of its meta-structure. **L1 remains the one gate; L2–L4 describe and never block.**

## 3. Re-coherence — the central measure (gap → return)

Where L3 measures **distance in time** (then → now), L4 measures **the return** of a
segmented field to a whole. It reuses the machinery already built for the return path:

- `remember` — how faithfully a later record carries an earlier truth back across the
  ghost lag;
- `confluence` — independent segmented lineages **converging** on one retained field =
  corroboration of the source truth (the mechanism of a *genuine* re-coherence);
- `constellation` — the load-bearing **keystone** the re-coherence returns *to* (the
  "truth of the change in attention mode," made a measurement).

**What `spiral <value>` computes.** Take a value (e.g. *equilibrium*): show its
breath-whole and its pump-segments, then measure the **return-resonance** of the
re-cohered nerve-whole against the constellation keystone, **scaled by complexity** — how
many differentiated pieces it holds in one *connected* field (the `proliferation`
largest-connected-component measure already does exactly this).

```
re-coherence = resonance( re-cohered field , retained truth )  ×  complexity
resonance    = ( structural , substantive )          # two facets, NOT one scalar — see below
complexity   = differentiation (count of re-cohered segments)  ×  coherence (largest-component fraction)
```

**Resonance has two facets** (the `cloud` example forced this, §12.3). A nerve whole can
rhyme with the retained truth in *shape* yet betray it in *substance*:

- **structural fidelity** — does the re-cohered whole have the *form* of the retained
  truth? (placeless immanence, participation, a single shared field)
- **substantive fidelity** — is the *living substance* present, or hollowed/harvested?
  (genuine affection, genuine life, freely given vs metered, owned, surveilled,
  optimised)

Collapsing the two into one number would lie about exactly the signs that matter most.
So the verdict is a **pair**, never a scalar (§4). High on both → **faithful synthesis**;
high complexity with substantive low → **counterfeit aggregation**; structural high /
substantive low is the distinctive nerve pathology — *the form of the whole without the
life* (the synthetic breath).

The breath-value a nerve sign returns *toward*, and the pump shards it re-coheres, are an
**authored declaration** — a `recoherences` map, the nerve-side mirror of the glossary's
`migrations` (which records the breath→pump dispersal). It says, per nerve value: which
retained value it returns to, and which shards it gathers — a proxy, surfaced and
provenance-carrying, never a claim of strict etymology. (Worked through for *viral* in
§10.)

Breath scores trivially-whole (few pieces); nerve's achievement is to hold *many*
differentiated pieces in one field and still resonate with the source — the spiral
returning at greater complexity, made legible. Descriptive, never a gate.

## 4. The guardrail — faithful synthesis vs counterfeit aggregation

"Nerve is the return to wholeness" is a strong, near-utopian thesis, and the framework's
spine is *descriptive, never a gate; it refuses to pre-decide.* So re-coherence is
**measured, never assumed.** Nerve is the regime where re-coherence is **attempted**; the
measure reports whether it **succeeded**. A nerve sign can be:

- a **faithful synthesis** — the segments genuinely re-cohere toward the retained truth
  (the `confluence` *converge* case); or
- a **counterfeit aggregation** — pieces piled into the *form* of a whole without the
  living unity: the **synthetic breath**. An LLM's plausible-but-hollow gloss; a meme
  that recombines fragments into noise; engagement-optimised slop.

**The verdict is a spectrum, not a switch — and two-dimensional.** Re-coherence runs
faithful ↔ counterfeit along *both* facets of resonance (§3): a sign can be structurally
faithful yet substantively counterfeit (`cloud`: real placeless immanence, but rented and
surveilled), or its very structure can be thin (`friend`: the bond flattened to an edge).
A real sign is usually **mixed**, and the measure must report *which facet fails* and stay
**provisional** for live senses, never collapse to a single crown. *`viral` is the proof
case (§10): structurally faithful (it restores participation and the shared field),
substantively partial (mechanised, sometimes pathological) — the framework reports both,
the judgement stays the human's.*

This is not a new failure mode to invent — `chain` already proves a return can **decay**
as well as **restore** (the ouroboros worn to medieval ornament, then *restored* by
Jung's reading). The guardrail is what makes L4 re-cohere *to the truth* rather than
merely re-cohere. Non-triumphalist, and faithful to the discipline.

This guardrail governs the *verdict* — whether a return *succeeds*. §16 extends it to the
*premise* — whether there is a return *at all*: some nerve signs are nerve-native origins or
refusals of meaning, and the spiral must **refuse** them (a third outcome, `resistant`)
rather than manufacture a return. Re-coherence is measured per sign, **never assumed of the
regime**.

## 5. The regime profile — aspect scores *alongside* the label, and the whole picture

The question shifts from **class** to **profile**: not *"what regime is a meme?"* but
*"how does this meme embody all three?"* A meme **is** breath (an image-macro holds a
whole gestalt at once), **is** pump (it spells words; segmentable components), **and is**
nerve (sense recomputed by remix, context, virality). Scoring high on all three at once is
the **signature of the synthesis** — the meme is not homeless between regimes, it is the
*exemplar* of the spiral's close.

**Both, as agreed:**

1. **Alongside the binary label (additive — breath/pump untouched).** Every usage keeps
   its existing single `regime` field; a new **aspect profile** `{breath, pump, nerve}`
   (each 0–1) sits beside it. `profile <sign>` shows it; `trace` surfaces it. The old
   binary classification is never removed or rewritten.
2. **The whole picture.** A system-level view aggregates the aspect profiles across
   *every* sign — the spiral seen whole: which signs are purely breath, which purely
   pump, and which (the memes, the emoji, *viral*) light up on all three. This is the
   `constellation` move applied to the profiles — a map of where each sign sits on the
   spiral, surfaced as one screen (folded into `atlas`, or its own `aspects` view). **Its
   shape is drafted in §15** (the clusters, the diagonal, the nerve keystone).

Illustratively (authored proxies, 0–1 per aspect):

| sign | breath | pump | nerve | reading |
|------|:------:|:----:|:---:|---------|
| `labrys` | 0.9 | 0.1 | 0.1 | a breath whole, barely segmented |
| `water` (lexeme) | 0.1 | 0.9 | 0.2 | a pump word, one discrete sense |
| `viral` | 0.6 | 0.7 | 0.8 | a pump word re-cohering into a nerve whole |
| `meme` | 0.7 | 0.6 | 0.9 | lights up on all three — the spiral's close |

A profile is an **authored proxy** carrying its provenance, like every map here — not a
claim that a sign "is" 0.7 breath, only a reading of how its attention is distributed.

## 6. The seeds — the *labrys* and *revolution* of the spiral's close

- **The synthesis exemplar** (embodies all three) — **`meme`** (Dawkins 1976 →
  nerve-native unit of recombinant culture) and/or the **emoji** (a literal return of
  *ideographic, weighted-field* signs inside a phonetic-script culture). The profile
  (§5) is read directly on these.
- **The live inversions** — **`viral`** (biology ~1898, contagion → culture: rapid,
  self-replicating spread, now often *valued*); and the spectrum companions worked in
  §12 — **`friend`** (philia → network edge; the counterfeit pole) and **`cloud`**
  (the heavens → placeless infrastructure; structurally faithful, morally counterfeit).
  Clean, datable sense-inversions of pump words, the `trace`/`drift` pattern freshly
  attested — and the first `spiral` readings (segmented senses returning toward a whole).
- **The nerve untranslatables** — *doomscroll, ghosting, rizz, cringe, based* —
  concepts the networked culture valued enough to name; lexicalisation-as-valuation
  (§ `lexicon.py`), observable **live**, extending `proliferation` with a *nerve* era.

Because the nerve crossing is **lived, not hindsight**, nerve senses carry an explicit
**provisional** marking: a contemporary reading is a proxy for a sense *not yet settled*,
and the framework must never report a still-negotiated live sense as fixed. (L1
attestation, by contrast, gets *easier* — the whole internet is cited usage.)

## 7. The invariant spine — do **not** touch

Additive only. **L1 attestation stays the one gate**; every other measure stays
**descriptive, never a gate**; the **authored map carries its provenance**; the
**ledger stays hash-chained**; **`signal == 1` must still hold** (CI runs it each push);
**breath and pump regimes are unchanged** — nerve and the profiles sit alongside them.

## 8. Model changes implied (for the build phase — not yet)

1. `regime.py` — add `NERVE` and a **native script** for it (`recombinant`); keep the
   breath/pump binary and all its behaviour bit-for-bit. Add the **aspect profile**
   type `{breath, pump, nerve}` (alongside, never replacing, the `regime` field).
2. `reading.py` — add **L4 `recohere()`** beside `attest`/`read`/`drift`/`project`,
   returning the §3 measure and a **two-facet** (structural, substantive) verdict (§4), or
   the third outcome **`resistant`** (§16) when there is no honest `returns_to`. Add a
   **spiral-projection** guard (the L4 analogue of `is_phonetic_projection`): a
   `returns_to` reached for, not attested, is flagged, not honoured.
3. A new **`spiral.py`** (generalising `arc`, validated on `equilibrium` in §14): one
   value read across all three phases — whole → segmented → re-cohered — with the
   re-coherence measure and two-facet verdict. `spiral` *calls* `arc` for the pre-nerve
   phases and extends it; `arc` is not replaced.
4. `glossary.json` — seed §6 (`viral`, `meme`, `friend`, `cloud`, `wiki`),
   provenance-carrying, `provisional` where live; profiles authored on the seed signs.
   Add a **`recoherences`** block (the nerve-side mirror of `migrations`, §11): per nerve
   value, `sign` / `returns_to` / `gathers` / `carries`.
5. `lexicon.py` / `lexicon.json` (§13) — seed nerve-era lexemes; add a **`recombination`**
   metric and an `untranslatables` **residence-time** reading; `proliferation` gains the
   sixth *nerve* era.
6. The **whole-picture** aspect view (§5.2, drafted §15) — a new `aspects` command (and an
   `atlas` line), reading the authored profiles and running `constellation` over the nerve
   cluster. A reader, not a ruler; gates nothing.
7. Tests + `seed.py` re-run + `manifest` refresh; confirm **`signal == 1`**.

## 9. Decisions

| # | decision | resolution | status |
|---|----------|-----------|--------|
| 1 | layer structure | **spiral** — layers as a cycle (L4 closes to L1, one rung up) | **locked** |
| 2 | headline measure | **re-coherence** — return-resonance × complexity (inverts gap→return) | **locked** |
| 3 | honesty guardrail | **faithful synthesis vs counterfeit aggregation** — measured, never assumed | **locked** |
| 4 | regime treatment | **profile + label** — aspect scores `{breath,pump,nerve}` alongside the binary regime, **and** a whole-picture aggregate | **locked** |
| 5 | nerve's thesis | nerve = the phase where segmentation **can** re-cohere to a whole at greater complexity — **measured per sign, never assumed of the regime** | **locked, bounded (§16)** |
| 6 | seeds | `meme`/`wiki` (faithful exemplars); `viral`/`friend`/`cloud` (live inversions, §10/§12) | **worked (§10, §12)** |
| 7 | measure inputs | complexity = differentiation × coherence; **resonance = (structural, substantive)**, two facets vs the `returns_to` retained field | **resolved (§3, §12)** |
| 8 | naming | regime **`nerve`** (mode; medium = the net) · script **`recombinant`** · layer/command **`spiral`** · L4 op **`recohere`** · data map **`recoherences`** · 3rd outcome **`resistant`** · error **`spiral projection`** (`is_spiral_projection`) · lexicon metric **`recombination`** · views **`profile`** / **`aspects`** | **locked (§1, §16)** |
| 9 | data model | `recoherences` = nerve-side mirror of `migrations` (`sign` / `returns_to` / `gathers` / `carries`) | **drafted (§11)** |
| 10 | nerve lexicon | sixth *nerve* era; new `recombination` metric; `untranslatables` residence-time → 0 | **drafted (§13)** |
| 11 | additivity | `spiral` reads breath-origin seeds and **completes** `arc` (validated on `equilibrium`) | **validated (§14)** |
| 12 | whole-picture view | `aspects` = `constellation` over the profiles: clusters, the diagonal, the nerve keystone | **drafted (§15)** |
| 13 | adversarial bound | `resistant` outcome + **spiral-projection** error + a `returns_to` honesty test (the spiral must be able to **refuse**) | **found (§16)** |
| 14 | build scope | phased plan A–D (foundation → `spiral` → lexicon → close); three-column extension = optional phase E | **resolved (§21)** |
| 15 | nerve's two faces | **`scatter`** — the fragmentation force within nerve, measured beside `recohere`; disambiguates `resistant` | **added (§17)** |
| 16 | methodology | the **reflexive** risk (a recombinant reader is a spiral-projection engine, §18); L1's **superabundance** traps (§19); the **resisted** ideas recorded (§20) | **named (§18–§20)** |

**All sixteen decisions are settled — scoping is complete.** The §10–§16 work exercises
the whole spiral by hand — **value scale** (`spiral`, nerve-born *and* breath-origin),
**lexicon scale** (`proliferation`), the **whole-picture** aggregate (`aspects`), and an
**adversarial** pass that bounds the thesis; a **review pass** (§17–§20) then measured
nerve's fragmentation face, named the reflexive risk, and bounded what was deliberately
left out. The architecture's four tests — discrimination, additivity, the two scales
agreeing, and *falsifiability* (it can refuse) — passed on paper. A measure that can fail
is a measure that can mean something. The build plan is §21.

## 10. Worked example — *viral* through the spiral (by hand, no code)

The first end-to-end test: trace one live word through all three phases and see whether
the spiral reading is **disciplined** (it produces a verdict, not a coronation) and
**non-trivial** (it says something the existing tools do not).

### The value under the word

The spiral reads a *value*, not a spelling. Under "viral" lies an old conceptual whole:
**a living force passing through the whole collective by participation** — contagion
*before* germ theory: miasma, blessing and curse passing by contact, the evil eye,
sympathetic transmission. In the glossary's vocabulary this sits in the **life** (the
ankh: the living breath/force) and **unity** (the collective as one shared field)
region of the retained truth. *[authored mapping — a `recoherences` entry, a proxy,
declared, not etymology.]*

### Phase 1 — whole (breath)

Contagion held *whole* and *participatory*: a potency moves through the collective and
all share one field; to be in the community is to be in the contagion — of blessing or
of plague. No discrete agent: the force and the field are one. (Not a written
breath-*sign* here, but the breath *mode* — meaning held whole, participatory.)

### Phase 2 — segmented (pump)

The analytic mode splits the one participatory force into discrete, domain-separated
mechanisms, each carving off a facet and dropping the participatory whole — the
`migrate` move (holism → segmentation) applied to *transmission*:

- **contagion** (medicine) — a *discrete agent*, the germ; the individual is infected,
  not the field (germ theory localises what was holistic);
- **transmission** (signal/mechanics) — a channel between a sender and a receiver;
- **influence** (society) — one mind acting on another;
- **propagation** (biology/physics) — mechanical replication;
- **circulation** (economy) — the spread of money, goods, news.

Each is a shard; the living, shared, whole field is gone.

### Phase 3 — re-cohered (nerve)

"Going viral" returns the shards to a whole *at greater complexity*: content spreads
through a networked collective **by participation** (you share, you remix — the meme
lives by your act); the field is again *one* (everyone connected); the force (affect,
idea) genuinely passes through and transforms the whole — **and** it keeps the pump's
analysis: it is measured (reach, R₀), mechanised (the algorithm), discrete-trackable.
The breath whole returns *carrying* the pump segments inside it. That is the spiral
closing: wholeness regained while keeping the differentiation.

### The measure, by hand

- **complexity** — *high*: ~5 distinct pump shards (contagion, transmission, influence,
  propagation, circulation) re-cohere into **one connected** field — "going viral" names
  them all at once. Many pieces, one whole.
- **return-resonance** vs the retained truth (life-as-participatory-transmission,
  unity-as-one-field) — **partial / contested**:
  - *faithful*: virality genuinely restores **participation** (you don't receive, you
    spread) and the **one shared field** (the collective is again a single contagious
    whole) — a real return;
  - *counterfeit*: the participation is **mechanised and harvested** — the field is an
    engagement metric, the "life" is often hollow (slop, bots, manufactured virality),
    and the contagion is frequently *pathological* (outrage, disinformation). The *form*
    of the living whole without the living unity — the **synthetic breath**.

### Verdict — and why it validates the architecture

`viral` is a **mixed re-coherence**: faithful in restoring participation and the shared
field, counterfeit in mechanising and hollowing them. The framework reports *both*,
scaled by complexity and marked **provisional** (the sense is live, still settling), and
**leaves the judgement to the human**. The spiral did not crown nerve as synthesis; it
*measured* a real and a counterfeit return in the **same** sign — exactly what
"re-cohere *to the truth*" was meant to do.

### The aspect profile (embodies-all-three)

As a sign in use, `viral` lights up on all three (§5): **breath** (it names a
participatory, shared-field whole), **pump** (it is measured, mechanised, segmentable
into metrics), **nerve** (its sense *is* its networked propagation). High on all three is
the signature of the spiral's close — the same profile `meme` carries.

### What the example changed in the design

1. The spiral needs an authored **`recoherences`** map (§3, §8.4) to declare the
   breath-value a nerve sign returns toward and the shards it gathers — without it,
   `spiral viral` has no retained truth to resonate against.
2. The verdict must be a **spectrum admitting "mixed"** (§4), not a binary — *viral*
   is faithful and counterfeit at once, and forcing a single label would lie.

## 11. The `recoherences` data model (draft)

Pinned **before** any further examples so each one fills a known shape. It is the
nerve-side mirror of the glossary's `migrations`: where `migrations` records the
breath→pump *dispersal* of a value into shards, `recoherences` records the pump→nerve
*return* of those shards into a new whole. Authored, provenance-carrying, **provisional**
(the crossing is lived, not hindsight). Drafted here as JSON; **not** yet written into
`glossary.json` (that is a build step — it re-seeds the ledger).

Per nerve value: the `sign` that carries the return; `returns_to`, the breath value(s) the
retained-truth resonance is measured against; `gathers`, the pump shards re-cohered (the
mirror of `migrations.shards`); and `carries`, the weighted field the nerve sign now holds
— the resonance *input*, exactly as a breath sign carries a field. The verdict
(faithful ↔ counterfeit, §4) is **computed** from these, never authored.

```json
"recoherences": {
  "_note": "Authored returns: how a value the pump segmented re-coheres, in the nerve regime, into a new whole at greater complexity — the mirror of `migrations`. A proxy, surfaced here, never strict etymology; nerve entries are provisional.",
  "viral": {
    "sign": "viral",
    "returns_to": ["life", "unity"],
    "note": "Contagion before germ theory — a living force passing through the whole collective by participation — segmented by the pump into discrete mechanisms, re-cohered by 'going viral' into networked, measured, participatory spread.",
    "gathers": [
      {"term": "contagion",    "facet": "the discrete infectious agent",         "domain": "medicine"},
      {"term": "transmission", "facet": "a channel from sender to receiver",      "domain": "signal"},
      {"term": "influence",    "facet": "one mind acting on another",             "domain": "society"},
      {"term": "propagation",  "facet": "mechanical replication",                 "domain": "biology"},
      {"term": "circulation",  "facet": "the spread of money, goods, news",       "domain": "economy"}
    ],
    "carries": {"participation": 0.30, "shared-field": 0.30, "measurement": 0.25, "pathology": 0.15},
    "provisional": true,
    "year": 1996
  }
}
```

`complexity` reads off `gathers` (differentiation) × the connectedness of `carries`;
`resonance` compares `carries` against the retained field of `returns_to`. For `viral`:
five shards re-cohered (high complexity); `carries` resonates with *life/unity* through
*participation* + *shared-field* (~0.60) but not through *measurement* + *pathology* —
the **mixed** verdict, derived, not declared.

## 12. Further worked examples — meme, friend, cloud (the spectrum's range)

Three more, chosen to land at *different* points on the faithful↔counterfeit spectrum —
the test being whether the measure **discriminates** rather than rubber-stamps nerve.

### 12.1 `meme` — the synthesis exemplar (faithful-leaning)

**Value:** mimesis as participatory becoming — culture transmitted by embodied imitation
(ritual, mask, dance), held whole, in the *unity* (belonging) and *eternity* (continuity
of the pattern) region. **Whole:** the participant *becomes* the imitated pattern; no
discrete unit. **Segmented:** Dawkins's coinage (1976) is itself the pump move — it
atomises cultural transmission into a discrete *replicator* (the gene analogy: selfish,
countable, competing), beside *idea, motif, custom*. **Re-cohered:** the internet meme
returns the unit to a living, **authorless, recombinant** whole that each sharer
*re-makes* — and does so as an **image-macro**: a literal return of *conceptual,
ideographic, weighted-field script* inside a phonetic culture. The profile (§5) lights up
on all three: breath (holds a gestalt whole), pump (a bounded, named format), nerve (sense
*is* its recombinant propagation). **Verdict — faithful-leaning:** the participation is
genuinely *creative* (remix is making, not forwarding) and meaning is again held whole in
a sign; the counterfeit risk is real but secondary (astroturfed virality, recombination
into reflex/noise). The strongest single piece of evidence that the spiral *closes*.

```json
"meme": {
  "sign": "meme",
  "returns_to": ["unity", "eternity"],
  "note": "Mimesis as participatory becoming, atomised by Dawkins (1976) into a discrete replicator, then re-cohered by the internet meme into a living, authorless, recombinant sign each sharer re-makes — a return of ideographic, weighted-field script inside a phonetic culture.",
  "gathers": [
    {"term": "replicator",     "facet": "the selfish discrete unit (Dawkins)", "domain": "biology"},
    {"term": "idea",           "facet": "the transmissible thought",           "domain": "psychology"},
    {"term": "motif / trope",  "facet": "the recurring form",                  "domain": "art"},
    {"term": "custom / fashion","facet": "the imitated practice",              "domain": "society"}
  ],
  "carries": {"creative-participation": 0.35, "collective-pattern": 0.30, "continuity": 0.20, "reflex-noise": 0.15},
  "provisional": true,
  "year": 2011
}
```

### 12.2 `friend` — the counterfeit pole

**Value:** philia — the chosen bond of mutual affection and reciprocal loyalty,
*belonging* (unity) held whole (xenia, kinship-by-choice, the oath-bond). **Whole:** you
and the friend share one field of care and obligation. **Segmented:** the bond abstracted
into functional roles — *acquaintance, ally, associate, contact, companion* — affection
split from relation. **Re-cohered:** the platform "friend" (Facebook, 2004; the new verb
*to friend*) re-aggregates the **whole social graph** into one networked field — the form
of a holistic return. **Verdict — counterfeit-leaning:** high complexity (the entire
graph as one field) × **low resonance** — the "friend" edge keeps the *form* of belonging
(connection, co-presence) while shedding its *substance* (chosen mutual affection); philia
flattened to a click. A genuine sliver survives (real bonds sustained across distance), so
*mixed-leaning-counterfeit*, not zero — the **synthetic breath** in its sharpest form.

```json
"friend": {
  "sign": "friend",
  "returns_to": ["unity"],
  "note": "Philia — the chosen bond of mutual affection — abstracted by the pump into functional roles, then re-aggregated by the platform 'friend' (Facebook, 2004) into one networked social field: the whole graph returns as a field, but the bond is flattened to an edge.",
  "gathers": [
    {"term": "acquaintance",      "facet": "the known but unbonded", "domain": "society"},
    {"term": "ally",              "facet": "the bond as alliance",   "domain": "politics"},
    {"term": "associate / contact","facet": "the functional tie",    "domain": "work"},
    {"term": "companion",         "facet": "the one who shares the way","domain": "life"}
  ],
  "carries": {"connection": 0.45, "shared-field": 0.20, "count-metric": 0.20, "affection": 0.15},
  "provisional": true,
  "year": 2004
}
```

### 12.3 `cloud` — structurally faithful, morally counterfeit

**Value:** the cloud of the heavens — the immanent, hidden, everywhere-and-nowhere divine
totality (Sinai's cloud, the shekhinah, the cloud-hidden god), in the *divinity* /
*eternity* region. **Whole:** the present-but-hidden numinous ground from which rain,
life, revelation descend. **Segmented:** carved into *vapor/weather* (meteorology),
*obscurity* (epistemics), *suspicion* ("under a cloud"). **Re-cohered:** "the cloud"
(computing, c. 2006) returns a **placeless, everywhere-present, hidden ground** in which
our extended memory dwells — the nerve regime *literally instantiating* placeless
immanence. **Verdict — split, a third texture:** structurally a *real* return (the
network genuinely is an immanent, placeless, hidden whole — a true rhyme with the divine
cloud) yet morally *counterfeit* (it is rented, proprietary, surveilled infrastructure;
the "everywhere" abstracts over very located, owned data centres). The numinous
hidden-whole becomes a *leased* hidden-whole — faithful in structure, counterfeit in
ownership. A texture neither *viral* nor *friend* shows.

```json
"cloud": {
  "sign": "cloud",
  "returns_to": ["divinity", "eternity"],
  "note": "The cloud of the heavens — immanent, hidden, everywhere-and-nowhere divine totality — segmented by the pump into weather, obscurity, suspicion, then re-cohered by 'the cloud' (computing, c. 2006) into a placeless networked ground; structurally a real return of placeless immanence, in fact a rented, surveilled, proprietary elsewhere.",
  "gathers": [
    {"term": "vapor / weather", "facet": "the meteorological mass", "domain": "science"},
    {"term": "obscurity",       "facet": "the hidden, the clouded", "domain": "epistemics"},
    {"term": "suspicion",       "facet": "'under a cloud'",         "domain": "morals"},
    {"term": "storage",         "facet": "the placeless data-store","domain": "computing"}
  ],
  "carries": {"placeless-immanence": 0.40, "hidden-ground": 0.25, "utility": 0.20, "proprietary-surveilled": 0.15},
  "provisional": true,
  "year": 2006
}
```

### The spectrum, seen across the four

| sign | complexity | structural | substantive | where it lands |
|------|:----------:|:----------:|:-----------:|----------------|
| `meme` | high | high | high | **faithful-leaning** (creative participation; a literal return of conceptual script) |
| `viral` | high | high | partial | **mixed (centre)** (real participation, counterfeit mechanisation) |
| `cloud` | high | high | low | **structurally faithful / morally counterfeit** (real placeless immanence, but rented & surveilled) |
| `friend` | high | mid | low | **counterfeit-leaning** (the graph returns as a field, but the bond is flattened to an edge) |

Splitting resonance into two facets is what *separates* `cloud` from `friend` — both
score substantively low, but `cloud`'s structural rhyme is genuine (the nerve **is** a
placeless immanent ground) while `friend`'s structure is itself thinned (a graph edge is
a weak image of philia's shared field). One scalar would have blurred them.

Four nerve signs, four *different* positions on the spectrum. The measure **discriminates**
— it does not crown nerve wholesale, and it does not dismiss it wholesale. That spread is
the architecture's second test, and the point of the guardrail: re-coherence is real,
partial, and counterfeit by turns, and the framework's job is to *measure which*, never to
decide. Descriptive, never a gate; provisional throughout, because the crossing is ours
and still moving.

### 12.4 The clean faithful pole — `wiki` / the open commons

To anchor the *top* of the spectrum (the four above top out at "faithful-leaning"), the
clearest faithful synthesis is the **collaboratively authored commons** — *wiki*
(Wikipedia, open source, the open encyclopaedia). It re-coheres the pump's segmented,
privately-authored knowledge into one **shared, participatory, recombinant whole** —
and, unusually, scores **high on both facets**: structural (a single connected web of
knowledge co-held by all) *and* substantive (authorship is genuinely distributed and
freely given; the whole is *non-proprietary*, the exact substance `cloud` forfeits). It
is the nerve regime keeping its promise — the synthesis that is not synthetic. Worth seeding
as the faithful anchor opposite `friend`. (Counterfeit risk remains real — vandalism,
capture, astroturfed consensus — which is why it is an *anchor*, not an absolute.)

## 13. The nerve lexicon — the explosion re-coheres into a shared field

The `spiral <value>` measure (§3) reads the return at the scale of **one value**. The
lexicon has its own, system-scale instrument — `proliferation` (§ `lexicon.py`), which
already traced the pump explosion's coherence climbing `0.25 → 1.00` over five eras. The
nerve regime is where that climb **completes into a new whole**: a sixth, *nerve* era whose
signature is not merely *coherence* (already maxed) but **recombination** and
**globalisation** — the lexicon-scale face of the spiral's close.

Draft sixth row (authored proxy, extending the README's table):

```
era         new  total  align   exp  coher  recomb
primal        4      4   0.09  0.00   0.25    0.00
agrarian      5      9   0.22  0.00   0.89    0.00
classical     5     14   0.35  0.07   0.93    0.05
modern        6     20   0.48  0.30   1.00    0.15
reflexive     7     27   0.59  0.48   1.00    0.25
nerve         8     35   0.64  0.55   1.00    0.55     <- the new era
```

Two new movements the existing columns can't see, and one new column:

- **recombination (the new column)** — nerve coins are increasingly **blends of existing
  lexemes**: *doomscroll* (doom+scroll), *mansplain*, *hashtag*, *selfie*. The
  definitional web stops merely *cohering* (words defined in terms of earlier words) and
  turns **generative** (words *composed from* earlier words). The segmented lexicon
  becomes a whole that **makes new wholes from its own parts** — re-coherence at the
  lexicon scale, measurable as the fraction of new lexemes that are recombinations.
- **globalisation of the untranslatable** — in the nerve era the per-tongue boundary
  **dissolves**: *schadenfreude, hygge, saudade, ubuntu* become instant shared loanwords.
  The `untranslatables` measure (which reads concepts a *single* tongue named) gains a
  **residence-time** reading — how long a concept stays single-tongue before the network
  shares it — and that time **collapses toward zero**. The segmented per-tongue lexicons
  re-cohere into one shared global field. (Differential valuation does not vanish — it is
  *shared faster*.)

So the two scales agree. At the **value** scale, `migrate` disperses and `spiral`
re-coheres one value across the threshold; at the **lexicon** scale, `proliferation`
re-coheres the whole vocabulary, and the *nerve* era is where that re-coherence becomes
**generative and global**. Same spiral, two magnifications.

**What the nerve coins reveal the culture values.** Lexicalisation is valuation
(§ `lexicon.py`), so the nerve era's new words are a mirror of what the nerve culture
holds and fears. They cluster tellingly — *doomscroll, ghosting, cringe, sus, parasocial,
based, mid* — around **attention, authenticity, social calibration, and mental health**:
the vocabulary of *mediated sociality* and its pathologies. Where the agrarian era named
*water* and *kin*, and the reflexive era named *empathy* and *wellbeing*, the nerve era
names the textures of a self performed to a network. That is the founding question — *use
the past to understand the cultural change* — answered in the coins themselves: a culture
names what it must newly navigate. (Descriptive; a reading the lexicon surfaces, not a
verdict on the age.)

**Model change (build phase):** `lexicon.json` gains nerve-era lexemes (*doomscroll,
ghosting, selfie, hashtag, stream, cloud, viral, meme, …*), each with `valued_for`,
`experiential`, and `defined_in_terms_of` (its recombination parents); `lexicon.py` gains
a **`recombination`** metric (fraction of an era's lexemes composed from existing ones)
and `untranslatables` gains a **residence-time** reading. As ever: authored proxies,
provisional, descriptive — never a gate. `proliferation --regime nerve` shows the close.

## 14. Validation — `equilibrium` through the spiral (a breath-origin value)

Every example so far began *in* the nerve (viral, meme, friend, cloud, wiki). The
architecture claims to be **additive** — the same `spiral` reads the framework's existing
seeds and **completes** the `arc` already shipped for them. The test: trace `equilibrium`,
the project's flagship value (the labrys's *paradoxical equilibrium*), all the way through.

The shipped `arc equilibrium` already gives the first phases — breath whole in
labrys/ouroboros (0.30 each), dispersed at the threshold into *balance, justice,
moderation, symmetry*, then the lexical thread climbing *justice (0.60) → … → wellbeing
(0.92)*. `spiral equilibrium` re-reads that as the three phases and **adds the nerve phase
the arc stops short of**:

- **whole (breath)** — the labrys held *paradoxical equilibrium*: opposed blades in
  balance as **one living whole**, the paradox (opposites-held-as-one) intact.
- **segmented (pump)** — *balance* (static mechanics), *justice* (law), *moderation*
  (virtue), *symmetry* (form). Each shard keeps a facet and **drops the paradox** —
  balance becomes the static evenness of two weights, not opposites in living tension.
  (Exactly `migrate equilibrium`.)
- **re-cohered (nerve)** — equilibrium returns as **dynamic, networked, self-regulating
  balance**: *homeostasis, resilience, sustainability, the feedback loop* — born of
  cybernetics and systems theory (Wiener 1948; Holling 1973), the nerve regime's own root.
  The static mean becomes a **living equilibrium held by a network**, and in doing so
  **recovers the paradox the pump had flattened**: opposites held in continuous tension, a
  balance that is *alive* and self-correcting — far closer to the labrys's living whole
  than the pump's static symmetry ever was.

**Two-facet verdict:**
- **structural — high, *higher than pump*:** dynamic balance-of-opposites-in-a-living-
  system genuinely rhymes with the labrys's paradoxical equilibrium. The nerve re-coherence
  is structurally *more* faithful to the breath whole than the pump segmentation was — the
  clearest demonstration of "return at greater complexity."
- **substantive — mixed:** genuine where the systemic balance is real (regenerative
  practice, true resilience); counterfeit where it is *greenwashing* — "sustainable" as a
  marketing skin, the form of living balance without the substance.

```json
"equilibrium": {
  "sign": "resilience",
  "returns_to": ["equilibrium"],
  "note": "The labrys's paradoxical equilibrium — opposed blades held as one living whole — flattened by the pump into static balance/justice/moderation/symmetry, then re-cohered by cybernetics and systems thinking into a dynamic, networked, self-regulating balance that recovers the living paradox the pump dropped.",
  "gathers": [
    {"term": "balance",    "facet": "static evenness of two weights", "domain": "mechanics"},
    {"term": "justice",    "facet": "balance moralised",              "domain": "law"},
    {"term": "moderation", "facet": "balance as personal virtue",     "domain": "ethics"},
    {"term": "symmetry",   "facet": "balance as formal correspondence","domain": "form"}
  ],
  "carries": {"dynamic-balance": 0.35, "self-regulation": 0.30, "paradox-recovered": 0.20, "greenwash-risk": 0.15},
  "provisional": true,
  "year": 1973
}
```

Note `returns_to` is **`equilibrium` itself** — a *breath-origin* value returns to its own
whole, where a nerve-*born* word (`viral` → `life`/`unity`, `cloud` → `divinity`) returns to
the breath keystone its sense maps onto. The data model (§11) handles both without change.

**What this validates:**
1. `spiral` reads a **breath-origin seed**, not only nerve-born signs — additive, as claimed.
2. `spiral` is the **generalisation of `arc`**: `arc` traced breath → pump →
   pump-re-coherence (stopping at *wellbeing*, 1990); `spiral` adds the **nerve phase** and
   the **two-facet verdict**. `arc` is the pre-nerve special case — in the build, `spiral`
   *calls* `arc` for the first phases and extends it, rather than replacing it.
3. The spiral can **return a breath quality the pump lost** (the paradox) — "greater
   complexity" made concrete, not asserted.

**One full turn of the cycle (§2).** Equilibrium's nerve whole — *resilience/homeostasis* —
is itself a new sign that can be **re-attested (L1)** and, in principle, re-segmented and
re-cohered again: the spiral turning once more, one rung up. The equilibrium trace is one
complete revolution of the ouroboros-layer, start to start.

## 15. The `aspects` whole-picture view (draft)

§5.2 promised a system-level view of the regime profiles — *the spiral seen whole*. This
pins its shape: the `constellation` move applied to the `{breath, pump, nerve}` profiles, so
every sign is placed at once and the clusters and the diagonal become visible.

```
$ python -m interpretation aspects
== the spiral seen whole: every sign by its regime profile ==
  sign          breath  pump  nerve  reading
  ankh           0.90   0.10  0.05   pure breath — a whole held
  labrys         0.90   0.10  0.10   pure breath — the paradox held
  ouroboros      0.85   0.15  0.25   breath, with a nerve echo (the cycle itself)
  revolution     0.10   0.90  0.15   pure pump — a word, a sense
  democracy      0.10   0.90  0.10   pure pump
  friend         0.30   0.60  0.75   nerve re-aggregation, breath thinned
  cloud          0.55   0.50  0.80   nerve, with a real breath rhyme
  viral          0.60   0.70  0.80   all three — the spiral's close
  wiki           0.65   0.55  0.85   all three — faithful (both facets)
  meme           0.70   0.60  0.90   all three — the synthesis exemplar
  ---
  clusters: breath {ankh, labrys, ouroboros} · pump {revolution, democracy}
            nerve   {friend, cloud, viral, wiki, meme}
  the diagonal: signs climb breath→pump→nerve as the spiral turns; the nerve cluster
                lights up on all three at once — the regime that holds the others
  nerve keystone: participation (reach 4) — the value the nerve cluster's re-coherence rests on
  the ouroboros is the bridge: the one breath sign with a real nerve echo (it *is* the cycle)
```

Three readings the aggregate adds that no single profile shows:

- **the clusters** — pure-breath, pure-pump, and the nerve cluster that scores high on
  *all three* (the signature §5/§12 predicted): nerve is not a fourth island but the regime
  that **holds the other two at once**;
- **the diagonal** — the signs that climb breath→pump→nerve are the spiral made visible as a
  shape, not just asserted;
- **the nerve keystone** — `constellation` run over the nerve cluster names the value its
  re-coherence rests on (*participation*), the nerve-regime analogue of breath's *divinity*
  keystone — the load-bearing truth of the information age, made a measurement.

And a small grace note: the **ouroboros** is the one breath sign with a real nerve echo —
it *is* the cycle the whole framework turns out to be. The aggregate surfaces that
without being told. Authored proxies throughout; descriptive, never a gate.

**Model change (build phase):** a new `aspects` command (and an `atlas` line), reading the
authored profiles off the glossary and running `constellation` over the nerve cluster. No
new measure — a *reader*, like `atlas`; gates nothing.

## 16. Adversarial test — a nerve sign that resists the spiral

The architecture has passed three *confirming* tests (§12, §13, §14). A scope is only
honest if it also tries to **break** itself. So: hunt for a nerve sign the spiral *cannot*
read, and see what the failure teaches. This is the framework's own move — the labrys foil,
the `signal` capstone — turned on the new layer.

### The clean resister — `spam` (a nerve-native origin)

`spam`: a tinned-meat brand (Hormel, 1937), routed through a Monty Python sketch, lands as
**unsolicited bulk noise**. Run the spiral and the *first* phase already fails — there is
**no breath whole** it returns *to*. Watch the measure try to supply one — *noise*, *the
swarm*, *the locust-plague*, *genesis-from-chaos* — and every candidate is **reached for**,
not attested. Spam is not a *return* to primordial chaos; it is a **new thing**, nerve-born,
with no holistic ancestor and no pump segmentation behind it. The honest output is not a
faithful or counterfeit verdict but a **refusal**:

> `spiral spam` → **RESISTANT**: nerve-native origin; no honest `returns_to`. The spiral
> declines to read a return where none exists.

This is the **L1 move lifted to L4**: attestation refuses what cannot be shown; the spiral
must refuse what cannot honestly be returned. The refusal *is* the finding.

### The subtler danger — the spiral over-accommodates

Worse than a sign it cannot read is the discovery that the spiral can read *almost
anything*: reach far enough up the abstraction ladder and every nerve sign acquires an
ancestor. `the algorithm` → *fate / the loom / moira / providence*; `deepfake` → *the idol
/ the simulacrum*; `doomscroll` → *apocalyptic vigilance*. These readings are **seductive**
— and that is exactly the alarm. A framework that can narrate a return for *any* sign
**measures nothing**: it has gone unfalsifiable — the failure the whole project exists to
forbid (a proxy wearing a proof's clothes). **The most beautiful re-coherence reading is
the one to distrust most.**

### What resists, in two types

- **Type A — nerve-native origin.** No honest breath whole to return to (`spam`, `deepfake`,
  `doxx`, `bot`). The spiral assumes nerve is a *return*; some nerve signs are *origins*.
- **Type B — meaning's refusal.** Signs whose content *negates* a stable whole — *post-
  irony*, the *shitpost*, "*random*", "lol nothing matters". There is no whole they fail to
  reach; the point is that there is none.

Both share one operational signature: **no honest `returns_to`** — which is exactly what
separates *resistant* from *counterfeit*. `cloud` and `friend` have a real whole they
*degrade* (so the two-facet verdict reads them); `spam` and the shitpost have **none to
degrade**.

### The new cardinal error — *spiral projection*

Every layer has its projection. L3 catches **anachronism** (a later *sense* read into an
earlier word) and **phonetic projection** (a later *mode of attention* read onto a breath
sign). L4 has its own: **spiral projection** — reading the *re-coherence narrative* onto a
nerve-native origin or a refusal of meaning, by **manufacturing a `returns_to`** it never
honestly had. It is the framework's besetting temptation on this layer — and the prettier
the return reads, the harder it must be checked.

### Consequences for the architecture

1. **Bound the thesis (revise decision 5).** Nerve is **not** "the regime that re-coheres,"
   full stop — *that was itself a pre-decided verdict, the very thing the framework
   forbids.* Nerve is the regime where meaning *can* re-cohere, *and also* fragment past
   anything pump did, *and also* be born new. **Re-coherence is measured per sign, never
   assumed of the regime.** This extends the §4 guardrail from the *verdict* to the
   *premise*: §4 refused to assume a return *succeeds*; §16 refuses to assume there *is* one.
2. **Add a third outcome: `resistant`** (beside faithful / counterfeit). The spiral, like
   L1, must be able to say "no honest reading here" and refuse — surfaced, never forced.
3. **A `returns_to` honesty test.** A `returns_to` must be a **specific, attested**
   conceptual lineage carrying its provenance — not an abstraction reached for to make the
   cycle run. When the only available ancestor is a vague keystone grabbed after the fact,
   the sign is `resistant`, not re-cohering. (The framework's own provenance discipline,
   applied to the nerve-side map.)
4. **Name nerve's other face — then measure it.** The spiral is the *return* arm; the
   adversarial signs reveal a *fragmentation* arm — the infinite feed, context collapse,
   the filter bubble. The scoping-review pass took this from a name to a measure: **`scatter`
   (§17)**, the division force within the nerve regime, which also disambiguates the
   overloaded `resistant` (a net-native origin scatters little; the feed scatters much).

The framework passing this test is **not** the spiral reading `spam`. It is the spiral
**refusing** to — and saying why. A measure that can fail is a measure that can mean
something.

## 17. The fragmentation arm — nerve's other face, measured (`scatter`)

§16 named a *fragmentation* arm and deferred measuring it — and that deferral left
`resistant` overloaded, lumping three different things under one word: a net-native
**origin** (`spam`), a **refusal** of meaning (the shitpost), and a sign that **actively
dis-coheres** (the infinite feed, doomscroll, context collapse). The first is merely new;
the others *do* something to meaning — the opposite of re-coherence. So the framework needs
the counterpart measure.

**`scatter` — division within the nerve regime.** Where `recohere` measures the *return* of
segments to a whole, `scatter` measures the *re-dispersal* of a whole into context-collapsed
fragments: how much a sign **decreases** the connectedness of a field (the inverse of §3's
`complexity` / largest-component measure) — attention split, context stripped, the gestalt
refused. The feed scatters (an infinite stream engineered against closure); doomscroll
scatters (compulsive fragments, no synthesis); the shitpost scatters (meaning negated).

This completes the picture the spiral half-drew — the full set of forces across the threshold:

| force | direction | measure |
|-------|-----------|---------|
| **migrate** | breath → pump: a whole *dispersed* into shards | `migrate` |
| **recohere** | pump → nerve: shards *returned* to a whole (the spiral) | `recohere` |
| **scatter** | within nerve: a whole *re-dispersed* into fragments | `scatter` (new) |

And it **disambiguates `resistant`**: a sign the spiral refuses is now read by `scatter`
too — `spam` scatters *low* (a net-native origin, not an attack on an existing whole), while
the feed and the shitpost scatter *high* (they take a whole and break it). Nerve's two faces
are no longer one named and one flagged; both are **measured**.

**The honest reading of a nerve sign is the pair** `(recohere, scatter)` — is it returning
us to a whole, or scattering us further, and how much of each? Most do some of both: the
`meme` re-coheres (a gestalt held) yet scatters (endless low-effort variants); `viral` does
both at once. Reporting the pair, never collapsing it, is the same discipline as the
two-facet resonance (§3): descriptive, never a gate.

*Model change:* `scatter()` beside `recohere()` in `reading.py` (or a small `fragment.py`);
CLI `scatter <sign>`; `aspects` (§15) can colour each nerve sign by its `(recohere, scatter)`
balance. Authored proxies, provisional, never a gate.

## 18. The reflexive turn — the instrument is a nerve artifact

The framework has turned its discipline on its own record (`signal`) and its own foil (the
labrys read phonetically). One mirror it has not yet held up: **the reader running these
measures is itself a nerve-regime artifact.** A large language model is recombinant,
statistical, authorless — sense computed from a field of neighbours — the nerve mode made a
machine. And it is *optimised to produce fluent, plausible re-coherences on demand*, which
makes it precisely a **spiral-projection engine** (§16): the tool most able to narrate a
beautiful `returns_to` for any sign is the one least able to feel when the return is
manufactured.

This sharpens the guard rather than decorating it. **`is_spiral_projection` matters *most*
when the reader is recombinant** — the prettier the gloss, the harder it must be checked —
and the framework's existing rule already half-anticipates this: a **mirror**-produced
reading (`provenance`) must declare its lineage and is never silently promoted to an
origination. §16's `returns_to` honesty test is that same rule, aimed at the same risk, now
named at its source. The framework reading the nerve regime *is the nerve regime reading
itself* — the ouroboros (§2) one turn deeper than the metaphor.

It also gives the **synthetic breath** (§4) its literal, present-day instance: LLM-generated
text is the paradigm counterfeit re-coherence — high *structural* fidelity (the exact form
of coherent, grounded meaning) over uncertain *substantive* fidelity (recombination without
a ground or an intent). The counterfeit the framework was built to catch is now
mass-produced — by tools like the one that helped write this. Naming that is the reflexive
honesty the whole project runs on.

## 19. L1 in the nerve regime — the superabundance trap

The scope has said repeatedly that L1 attestation gets *easier* in the nerve regime: the
whole internet is cited usage. True — and the one layer that genuinely **gates** deserves
the harder half of the truth. Superabundant usage brings failure modes the earlier regimes
never had:

- **ephemerality** — the usage deletes itself: dead links, removed posts, edited threads.
  An attestation can evaporate *after* it is cited (the inverse of the breath problem, where
  scarce attestations *survive*). The ledger's rule — *anchor to a witness you do not
  control* — becomes load-bearing: a nerve usage must be **archived** (a timestamped
  capture), not merely linked.
- **synthetic pollution** — much nerve-era text has **no human behind it**. A usage may be
  bot- or AI-generated, so "shown in a cited text" no longer implies "a culture meant it."
  L1 must attest not only that a sign was *used* but that it was used by a *cultural source*
  — the corpus itself now needs provenance.
- **personalised / owned context** — the "same" usage differs per viewer (no two feeds are
  alike) and sits on owned infrastructure; there may be no single public text to point at,
  and the citation is to a context that may be unreproducible.

None of these blocks attestation — L1 stays the one gate — but they are **new ways for the
gate to be fooled**, and the framework that prides itself on never letting a proxy wear a
proof's clothes should name them before it trusts a nerve citation. The fix is its own
discipline, intensified: capture and anchor; declare the corpus's provenance; treat
synthetic usage as *evidence of the machine*, not of the culture, unless a human source is
shown.

## 20. Deliberately out of scope (considered and declined)

Recording what was *resisted*, so the next reader knows it was weighed, not missed:

- **A second spiral turn / a post-nerve regime.** Tempting to model where the nerve whole
  goes next. Declined: we are inside the *first* nerve turn with no hindsight, and projecting
  a future regime is exactly the unfalsifiable over-reach (`spiral projection`) the framework
  forbids. The honest move is to mark it out of scope, not to model it.
- **A third resonance facet (durability / persistence).** Nerve signs are famously
  ephemeral, tempting a "does it last" axis beside structural and substantive (§3). Declined:
  persistence belongs *inside* substantive fidelity (a re-coherence that evaporates was never
  substantively whole), and adding axes is where measures lose their edge. Folded, not added.

Both may earn their place once Phase A–D are built and the nerve regime affords more
hindsight. Recorded here as **deferred, not dismissed**.

## 21. The build plan (resolving decision 14)

The scope is complete; this sequences §8's model changes into ordered phases. Each phase
is **additive**, ends with the suite green and **`signal == 1`**, and leaves the
breath/pump behaviour bit-for-bit. The recommended build is **phases A–D**; the
three-column `migrate`/`arc` generalisation (phase E) is genuinely optional and can follow.

**Invariant after every phase:** `pytest -q` green · `python -m interpretation signal` → `1`
· existing `breath`/`pump` command outputs unchanged (a golden-output check).

### Phase A — the regime foundation (no behaviour change)
- `regime.py`: add `NERVE` and the `recombinant` script; generalise `VALID_REGIMES` /
  `NATIVE_SCRIPT` from a binary to the ordered triple `breath → pump → nerve`, each with a
  ghost lag to its predecessor. Every breath/pump path stays identical.
- the **aspect profile** type `{breath, pump, nerve}`, *alongside* — never replacing — the
  `regime` field.
- `is_spiral_projection()` beside `is_phonetic_projection()` (the §16 guard).
- *Delivers:* the vocabulary and the guard; nothing reads yet — pure foundation.

### Phase B — the L4 measure and `spiral`
- `reading.py`: `recohere(usage, recoherence)` → the §3 measure with the two-facet
  `(structural, substantive)` verdict, **or** `resistant` when there is no honest
  `returns_to` (the §16 honesty test, via `is_spiral_projection`).
- `scatter()` (§17) beside `recohere()` — the fragmentation counterpart (division within
  nerve); the honest reading of a nerve sign is the `(recohere, scatter)` pair.
- `spiral.py`: `spiral(value)` — calls `arc` for the breath/pump phases, adds the nerve
  phase + verdict (generalises, does not replace, `arc`).
- `glossary.json`: the `recoherences` block (§11) for `viral`, `meme`, `friend`, `cloud`,
  `wiki`, `equilibrium`; the nerve seed concepts/usages; authored aspect profiles on the
  seed signs — all provenance-carrying, `provisional` where live.
- CLI: `spiral`, `recohere` / `profile`.
- *Delivers:* the value-scale spiral — the headline. Worked examples §10/§12/§14 run.

### Phase C — the lexicon scale
- `lexicon.json`: nerve-era lexemes (*doomscroll, ghosting, selfie, hashtag, …*) with
  `defined_in_terms_of` recombination parents.
- `lexicon.py`: the `recombination` metric; `proliferation` gains the sixth *nerve* era;
  `untranslatables` gains the residence-time reading.
- CLI: `proliferation --regime nerve`.
- *Delivers:* §13 — the spiral at the lexicon scale.

### Phase D — the whole picture and the close
- `aspects` command (and an `atlas` line): `constellation` over the profiles — clusters,
  the diagonal, the nerve keystone (§15); colour each sign by its `(recohere, scatter)` balance.
- the nerve-coin valuation reading (§13) and the L1-attestation cautions (§19) carried into
  the seed data: nerve usages **archived and anchored**, synthetic usage marked.
- tests for every new module; `seed.py` re-run; `manifest` refresh; CI runs `signal`.
- *Delivers:* §15, and the repository proving its own `signal == 1` with nerve seeded.

### Phase E — optional: the three-column extension
- generalise `migrate` / `arc` / `proliferation` to carry nerve as a first-class column
  everywhere (not only via `spiral`). Larger; defer until A–D are green and reviewed.

## Scoping complete

All sixteen decisions (§9) are settled. The architecture is **bounded** (§16),
**self-consistent**, **consistently named** (§1, §8), **validated on paper** at both
scales (§10–§14) and against an adversarial case (§16), and **deepened by a review pass**:
the fragmentation arm now measured (§17), the reflexive risk of a recombinant reader named
(§18), L1's nerve-regime traps named (§19), and the resisted ideas recorded (§20). The
document is now a build-ready specification: §8 says *what* changes, §21 says *in what
order*, and the invariant — `signal == 1`, breath/pump untouched, descriptive-never-a-gate
— holds at every step.

> **The through-line.** Breath held meaning whole; pump segmented it; nerve returns the
> segments to a whole at greater complexity — *when* it does, and the spiral measures
> whether it does, refusing the signs that only counterfeit the return or were never a
> return at all. The framework that read the first great change in attention now reads the
> one we are living through, by the same discipline: attest what is real, describe what it
> means, measure the distance — and never let the reading that resonates *now* pass for the
> meaning it is still becoming.
