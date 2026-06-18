# Thought flow — reading conceptual history, recorded step by step as it was built

This is a **living reasoning journal**. It records *how this framework was thought
through, in order*, so the reasoning is imprinted alongside the code and travels
with it. The README explains the design as it now stands; this document explains
how it was reached, and is meant to **grow**: each time a capability is added,
append a numbered step, then imprint this file (`kind: reasoning`, author
`anise.damm`) so the chain holds a timestamped record of the thinking, not only the
result. The reasoning is part of the intellectual property; this is where it is
kept.

> How to keep this running alongside the work:
> ```bash
> # after appending a step below
> python -m interpretation imprint docs/thought-flow.md \
>     --id thought-flow --title "Thought flow" --kind reasoning \
>     --author "anise.damm" --source collaboration --actor claude \
>     --parents language-framework --anchor "git:$(git rev-parse HEAD)"
> python -m interpretation manifest --out MANIFEST.md
> ```

---

## Step 0 — The spine we inherited

The sibling *integrity-alignment-system* held one thesis: **a check is a proxy,
not a proof**, and the honest move is to keep watching the gap between the proxy
and the goal it stands for. It expressed that in three layers — integrity (a
pass/fail gate), observation (describe, never judge), alignment (distrust the
gate). Everything below is that same spine, turned from *data and authorship*
toward *the interpretation of conceptual history*. The question changed; the
discipline did not.

## Step 1 — A word is not a concept (the sign splits)

The first move is Saussure's: a **sign** is a *signifier* (the word, the
sound-image) bound to a *signified* (the concept). The binding is **arbitrary and
conventional**, which has a consequence conceptual history lives on — the same
signifier can carry different signifieds, and the same signified can be carried by
different signifiers. So "the word *revolution*" and "the concept of revolution"
are two things, and the first honest act is to refuse to collapse them. The word
on the page is a *proxy* for a concept, exactly as a green check is a proxy for
correctness. This is the spine's first translation: **never let the word
masquerade as the concept.**

## Step 2 — The gap is *temporal* (Begriffsgeschichte)

Saussure splits the sign; Koselleck sets it in motion. *Begriffsgeschichte* —
conceptual history — observes that a word's concept is not stable across time: it
**sediments, shifts, and sometimes inverts**. *Revolution* is the canonical case:
the astronomical *revolving-back* of the heavens (Copernicus, 1543), carried into
politics as a *turning-back* to a rightful order (1688), then **inverted** after
1789 into an *irreversible break forward*. The word held still; the concept turned
inside out. So the gap between word and concept is not only structural (Step 1) but
**historical**: to read a usage is to locate it in the word's own time, and the
distance between a usage's time and a reading's time is the thing to measure.

## Step 3 — A reading is a proxy for the meaning (hermeneutics)

Gadamer and Ricoeur supply the third piece: every interpretation is made from a
*horizon*, the interpreter's own situated vantage. There is no view from nowhere,
no final reading — understanding is the *fusion* of the reader's horizon with the
text's, and it is always partial, always revisable. So a reading is a **proxy** for
the meaning in exactly the sibling system's sense: evidence, never proof. The
recogniser's similarity over phrasings is the mechanical face of this — two readings
that say the same thing are *recognised* as kin, but recognition is a similarity and
similarity is never identity. We keep "proof" and "proxy" in different words here
too: the one thing that is exact is **attestation** (the word *was* used, here, in
this cited text); everything downstream of it is interpretation.

## Step 4 — The three layers fall out of the gap

Given a word, a usage, and a reading, three different questions hide inside "what
does this mean?", and answering them with one act is where interpretation goes
wrong — the same mistake as letting a verdict masquerade as understanding:

| Layer | Question | What it fixes |
|-------|----------|---------------|
| **L1 Attestation** | Is the usage real — the word, shown in a cited text? | you cannot interpret what was never said |
| **L2 Reading** | What did the word mean *here*, in its own context? | the gloss that *describes* rather than judges |
| **L3 Anachronism** | Has the reading drifted into a later sense? | nothing otherwise *distrusts* the reading |

L1 is the one **gate** — an exact, checkable fact (does the word occur in the
quotation it is cited from?), the hermeneutic analogue of a content hash. L2
**describes** the sense in its own context and refuses to call itself "the
meaning." L3 treats the reading the way L3-alignment treats a green check: with the
suspicion a proxy deserves.

## Step 5 — Anachronism is Goodhart's law, turned hermeneutic

The sibling system's load-bearing lesson was a *false green*: a local test that
passed by measuring the wrong condition. Interpretation has the identical trap,
and it has a name — Skinner's **"mythology of prolepsis"**: reading a later meaning
back into an earlier text because it *resonates now*. A reading optimised for
present resonance is a proxy that has drifted from its target (the sense the word
had *then*), and it can feel completely right while being completely anachronistic.
So `drift` measures the gap in years: if the sense assigned to a usage was first
attested *after* the usage, that is anachronism, reported with its magnitude — the
hermeneutic false green, made catchable. It is **direction-aware** (the rarer
opposite error, reading an obsolete earlier sense into a later usage, is reported as
*archaism* but treated as weaker evidence, since a sense can persist).

## Step 6 — The senses form a lattice of descent

The sibling system found a lattice hiding in *knowledge* (a concept rests on the
concepts it presupposes). Conceptual history holds the same shape in a different
place: a word's senses, ordered by **descent** — a later sense arises *from* an
earlier one through an act of semantic change. Identify a sense with its
**ancestry** (itself plus all it descends from) and the operations are a lattice's:
**combine** (join — the whole field two senses jointly carry), **common** (meet —
the shared root meaning), **precedes** (order — `a` is ancestral to `b`). The
construction is deliberately the sibling's `algebra.py`, renamed from *prerequisite*
to *descent*: closed sets are closed under union and intersection, so it is a genuine
bounded lattice, and the laws are tested, not assumed. Two choices keep it honest,
both inherited: the operations are **exact** but the map is **authored** (a proxy for
the word's real history, carrying its provenance), and a malformed order — a descent
cycle, a dangling edge — is **surfaced, never silently patched**. Each edge also
carries the *kind* of change (the Bréal/Bloomfield typology), so **inversion** — the
move *revolution* makes — is first-class, not hidden inside a generic "it changed."

## Step 7 — Interpretive alignment = purpose × fidelity

The sibling system situates a piece of information with `alignment = purpose ×
truth`. Here the second factor is re-read for this domain: **truth becomes
fidelity to the historical usage**. `purpose` is unchanged (novelty — how much a
reading adds that is not already on record). `fidelity` folds the three layers into
one number: the chain is sound, the reading is **grounded** in an *attested* usage
(L1), it is **not anachronistic** (L3), and distinct *other* readers corroborate it.
Because it is a product, the quadrants stay honest — a fresh, grounded reading is
*purposeful but only half-aligned* until corroboration accrues; an anachronistic
reading is high-purpose and **zero-fidelity**, however clever. It is **descriptive,
never a gate**: a description of where a reading sits in the recorded conversation,
not a ranking of worth, and the record protects every reading in full regardless.

## Step 8 — Who reads is part of what is read (provenance)

Conceptual history is the field where the *provenance of an interpretation* is part
of its evidentiary weight, so the sibling system's two axes carry over without
strain. **author** is who owns a reading and holds priority — by default
`anise.damm`, the record this framework was built to keep. **source** is how the
reading was produced: a human's own reading, a **mirror's** (an AI reflecting the
author), a collaboration, or an external scholar quoted. The load-bearing rule is
the sibling's: a mirror can produce a gloss without being the source of the
insight, so a mirror-produced reading must declare its **lineage** — the
author-information *and the attested usage* it reflects — and the recorder warns,
never blocks, when that lineage is missing. A reflection can never be silently
promoted into an origination.

## Step 9 — The tamper-evident ledger, and priority by publication

A reading recorded is only as good as the record's integrity, so the backing is the
sibling's, scoped to this domain: an **append-only, hash-chained ledger**
(`ledger.py`) in which each reading is fingerprinted and bound to the one before it,
so any later edit or reordering breaks the chain and `verify()` catches it. Priority
over a reading is then established the open way — **defensive publication**:
`manifest.py` renders the whole chain into one shareable document whose load-bearing
line is the **chain head hash**, which (because every record is chained) commits to
the entire history. Anchor that hash to a witness whose clock you do not control —
commit `MANIFEST.md` to git and push — and "this reading was mine, by this date"
becomes provable to a third party. The honesty is the sibling's: a timestamp is
proof only as far as its anchor, and the framework says so rather than faking
wall-clock time.

## Step 10 — Neutrality: guard the reading, do not fix the meaning

The last commitment, load-bearing and stated once: the framework **protects the
integrity of a reading and guards against anachronism, but it neither fixes the
meaning nor walks the interpreter's path.** Every measure save the one honest gate
(attestation) is descriptive and blocks nothing; the authored map carries its
provenance and is never mistaken for the subject; no reading is ever refused a place
in the record. It guards the word, the usage, and the chain of custody over
readings — it does not pronounce what the word *truly* meant. That pronouncement is
the historian's, and an interpretation framework that made it would have become the
very thing it exists to catch: a proxy wearing the proof's clothes.

## The through-line

> A word is a proxy for a concept; a reading is a proxy for the meaning; a
> citation is the one thing that is proof, and only of *use*, not of sense. Attest
> what was said, describe what it meant *then*, and measure the distance between
> that and what we are tempted to hear now — but never let the reading that
> resonates today pass for the meaning it had in its own time.

This is the same spine as the sibling system: tell the truth about which of your
signals is a measurement and which is a substitute, and keep watching the gap
between them.

---

<!-- Append the next thought-flow step above this line, then imprint this file. -->
