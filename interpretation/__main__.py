"""Command-line front end for the conceptual-history interpretation framework.

    # The authored map of concepts, their senses and attested usages:
    python -m interpretation concepts
    python -m interpretation trace revolution

    # The three layers, on one usage read in one sense:
    python -m interpretation attest rev-1688                 # L1: is the usage real?
    python -m interpretation read   rev-1688 political-restoration   # L2: what it meant here
    python -m interpretation drift  rev-1688 irreversible-rupture    # L3: anachronism?

    # The diachronic algebra of a word's senses:
    python -m interpretation sense order revolution
    python -m interpretation sense common revolution political-restoration irreversible-rupture

    # Record a reading as yours, then publish priority:
    python -m interpretation imprint gloss.md --id my-reading --title "..." \
        --kind interpretation --concept revolution --sense irreversible-rupture \
        --parents rev-1789
    python -m interpretation align my-reading
    python -m interpretation manifest --out MANIFEST.md
    python -m interpretation verify

Defaults: the ledger `interpretation_ledger.jsonl` and the glossary `glossary.json`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .alignment import align_record
from .constellation import constellation
from .glossary import load_glossary
from .imprint import DEFAULT_AUTHOR, Imprinter
from .lexicon import load_lexicon, proliferation, untranslatables
from .migration import migrate
from .ledger import Ledger
from .manifest import write_manifest
from .memory import confluence, memory_chain, remember
from .reading import attest, drift, project, read, read_symbol
from .regime import SCRIPT_CONCEPTUAL, SCRIPT_PHONETIC
from .weighting import WeightedField

DEFAULT_LEDGER = "interpretation_ledger.jsonl"
DEFAULT_GLOSSARY = "glossary.json"
DEFAULT_LEXICON = "lexicon.json"


def _glossary(args: argparse.Namespace):
    return load_glossary(getattr(args, "glossary", None) or DEFAULT_GLOSSARY)


def _lexicon(args: argparse.Namespace):
    return load_lexicon(getattr(args, "lexicon", None) or DEFAULT_LEXICON)


def _ledger(args: argparse.Namespace) -> Ledger:
    return Ledger(getattr(args, "ledger", None) or DEFAULT_LEDGER)


def _parents(value: str | None) -> list[str]:
    return [p.strip() for p in value.split(",") if p.strip()] if value else []


def _weights(value: str | None) -> dict | None:
    """Parse a weighted field from JSON ('{\"unity\":0.4}') or 'k=v,k=v'."""
    if not value:
        return None
    value = value.strip()
    if value.startswith("{"):
        import json
        return json.loads(value)
    out: dict[str, float] = {}
    for pair in value.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            out[k.strip()] = float(v)
    return out or None


# --- the authored map -------------------------------------------------------

def cmd_concepts(args: argparse.Namespace) -> int:
    g = _glossary(args)
    if g.title:
        print(g.title)
    for c in g.concepts.values():
        print(f"  {c.id}: {c.name} — {c.gloss}")
        print(f"     {len(c.lattice.senses)} sense(s), {len(c.usages)} attested usage(s)")
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    g = _glossary(args)
    c = g.concept(args.concept)
    thr = f"; breath→pump threshold {c.threshold}" if c.threshold is not None else ""
    print(f"{c.name} ({c.id}) — {c.gloss}")
    print(f"  regime: {c.regime or '—'}{thr}\n")
    print("senses, in order of descent:")
    for sid in c.lattice.diachronic_order(c.lattice.senses.keys()):
        s = c.lattice.senses[sid]
        edge = c.lattice.shift_into(sid)
        marker = f"  [{edge}]" if edge != "origin" else "  [origin]"
        print(f"  {s.period:>14}  {sid}: {s.label}{marker}")
        if s.gloss:
            print(f"                  {s.gloss}")
    print("\nattested usages:")
    for u in sorted(c.usages.values(), key=lambda u: u.year):
        tag = f"{u.regime}/{u.mode}"
        if u.mode == SCRIPT_CONCEPTUAL:
            print(f"  {u.period:>20}  [{tag}]  {u.id}: {u.word} — {WeightedField(u.field).gloss}")
            print(f"                        attested: {u.artifact or u.citation}")
        else:
            print(f"  {u.period:>20}  [{tag}]  {u.id}: \"{u.word}\" — {u.citation}")
    return 0


# --- the three layers -------------------------------------------------------

def cmd_attest(args: argparse.Namespace) -> int:
    g = _glossary(args)
    result = attest(g.usage(args.usage))
    print(result.verdict)
    return 0 if result.ok else 1


def cmd_read(args: argparse.Namespace) -> int:
    g = _glossary(args)
    usage = g.usage(args.usage)
    if usage.mode == SCRIPT_CONCEPTUAL:
        print(read_symbol(usage).summary)        # weighted reading (L2 for a symbol)
    else:
        if not args.sense:
            print("error: a phonetic usage is read in a sense; pass a sense id", file=sys.stderr)
            return 1
        print(read(usage, args.sense, g.lattice_for_usage(args.usage)).summary)
    return 0


def cmd_drift(args: argparse.Namespace) -> int:
    g = _glossary(args)
    usage = g.usage(args.usage)
    d = drift(usage, args.sense, g.lattice_for_usage(args.usage))
    print(d.verdict)
    return 0


def cmd_weigh(args: argparse.Namespace) -> int:
    g = _glossary(args)
    usage = g.usage(args.usage)
    if usage.mode != SCRIPT_CONCEPTUAL:
        print(f"{args.usage} is a phonetic usage — it carries a sense, not a weighted field",
              file=sys.stderr)
        return 1
    print(f"{usage.word} ({usage.id}) — a {usage.regime}/{usage.mode} sign")
    print(f"  retained field: {WeightedField(usage.field).gloss}")
    if usage.committed_because:
        print(f"  committed to writing because: {usage.committed_because}")
    return 0


def cmd_project(args: argparse.Namespace) -> int:
    g = _glossary(args)
    usage = g.usage(args.usage)
    threshold = g.concept(usage.concept).threshold
    print(project(usage, SCRIPT_PHONETIC, threshold=threshold).verdict)
    return 0


def cmd_remember(args: argparse.Namespace) -> int:
    g = _glossary(args)
    print(remember(g.usage(args.usage), g).verdict)
    return 0


def cmd_chain(args: argparse.Namespace) -> int:
    g = _glossary(args)
    print(memory_chain(args.concept, g).summary)
    return 0


def cmd_confluence(args: argparse.Namespace) -> int:
    g = _glossary(args)
    print(confluence(args.concept, g).summary)
    return 0


def cmd_constellation(args: argparse.Namespace) -> int:
    g = _glossary(args)
    print(constellation(g, regime=args.regime).summary)
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    g = _glossary(args)
    print(migrate(args.value, g).summary)
    return 0


def cmd_proliferation(args: argparse.Namespace) -> int:
    print(proliferation(_lexicon(args)).summary)
    return 0


def cmd_untranslatables(args: argparse.Namespace) -> int:
    lex = _lexicon(args)
    items = untranslatables(lex)
    print(f"{len(items)} concept(s) a single tongue valued enough to name:")
    for u in items:
        print(f"  {u.word} ({u.language}) — {u.gloss}")
    return 0


def cmd_regime(args: argparse.Namespace) -> int:
    g = _glossary(args)
    c = g.concept(args.concept)
    thr = c.threshold
    print(f"{c.name} ({c.id}) — dominant regime: {c.regime or '—'}; "
          f"breath→pump threshold: {thr if thr is not None else '—'}")
    for sid in c.lattice.diachronic_order(c.lattice.senses.keys()):
        s = c.lattice.senses[sid]
        side = s.regime or ("breath" if (thr is not None and s.year < thr) else "pump")
        print(f"  {s.period:>14}  {side:>6}  {sid}: {s.label}")
    return 0


# --- the diachronic algebra -------------------------------------------------

def cmd_sense(args: argparse.Namespace) -> int:
    g = _glossary(args)
    lattice = g.concept(args.concept).lattice
    if args.op == "order":
        order = lattice.diachronic_order(lattice.senses.keys())
        print(" -> ".join(lattice.senses[s].label for s in order))
    elif args.op == "ancestry":
        print(lattice.field_of(args.a).summary)
    elif args.op == "common":
        if not args.b:
            print("error: 'common' needs two senses", file=sys.stderr)
            return 1
        common = lattice.common(args.a, args.b)
        print(f"common root of {args.a!r} and {args.b!r} (meet): {common.summary}")
    elif args.op == "precedes":
        if not args.b:
            print("error: 'precedes' needs two senses", file=sys.stderr)
            return 1
        if lattice.precedes(args.a, args.b):
            print(f"'{args.a}' is ancestral to '{args.b}': the later sense was reached through it")
        else:
            print(f"'{args.a}' is not ancestral to '{args.b}'")
    return 0


# --- record, align, publish -------------------------------------------------

def cmd_align(args: argparse.Namespace) -> int:
    g = _glossary(args)
    led = _ledger(args)
    print(align_record(args.record, led, g).summary)
    return 0


def cmd_imprint(args: argparse.Namespace) -> int:
    led = _ledger(args)
    text = Path(args.file).read_text(encoding="utf-8") if args.file else (args.text or "")
    receipt = Imprinter(led).imprint(
        artifact_id=args.id,
        title=args.title,
        text=text,
        author=args.author,
        kind=args.kind,
        source=args.source,
        source_actor=args.actor,
        parents=_parents(args.parents),
        concept=args.concept,
        sense=args.sense,
        word=args.word,
        citation=args.citation,
        period=args.period,
        year=args.year,
        regime=args.regime,
        mode=args.mode,
        weights=_weights(args.weights),
        artifact=args.artifact,
        license=args.license,
        external_anchor=args.anchor,
    )
    print(receipt.summary)
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    led = _ledger(args)
    g = None
    try:
        g = _glossary(args)
    except (OSError, ValueError):
        pass  # manifest still renders without per-record alignment
    write_manifest(led, args.out, g)
    print(f"wrote {args.out} (head hash {led.head_hash[:12]}...)")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    led = _ledger(args)
    v = led.verify()
    if v.ok:
        print(f"chain intact: {v.n_records} record(s), head {led.head_hash[:12]}...")
        return 0
    print(f"CHAIN BROKEN at record {v.broken_at}: {v.reason}", file=sys.stderr)
    return 1


def cmd_status(args: argparse.Namespace) -> int:
    led = _ledger(args)
    v = led.verify()
    print("== interpretation status ==")
    print(f"  chain:    {'OK' if v.ok else 'BROKEN: ' + v.reason}")
    print(f"  records:  {v.n_records}")
    concepts = sorted({r.concept for r in led.records if r.concept})
    print(f"  concepts: {', '.join(concepts) or '—'}")
    try:
        g = _glossary(args)
        attested = sum(1 for c in g.concepts.values() for u in c.usages.values() if attest(u).ok)
        total = sum(len(c.usages) for c in g.concepts.values())
        print(f"  glossary: {len(g.concepts)} concept(s), {attested}/{total} usage(s) attested")
    except (OSError, ValueError) as exc:
        print(f"  glossary: (not loaded: {exc})")
    print(f"  head:     {led.head_hash[:12]}...")
    return 0 if v.ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="interpretation", description=__doc__)
    p.add_argument("--ledger", help=f"ledger path (default {DEFAULT_LEDGER})")
    p.add_argument("--glossary", help=f"glossary path (default {DEFAULT_GLOSSARY})")
    p.add_argument("--lexicon", help=f"lexicon path (default {DEFAULT_LEXICON})")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("concepts", help="list the concepts in the glossary")

    sp = sub.add_parser("trace", help="trace a concept's senses and usages over time")
    sp.add_argument("concept")

    sp = sub.add_parser("attest", help="L1: is a usage attested? (the word, shown, cited)")
    sp.add_argument("usage")

    sp = sub.add_parser("read", help="L2: describe a reading (a sense, or a symbol's weighted field)")
    sp.add_argument("usage")
    sp.add_argument("sense", nargs="?", help="sense id (phonetic usages only)")

    sp = sub.add_parser("drift", help="L3 (phonetic): is a reading anachronistic?")
    sp.add_argument("usage")
    sp.add_argument("sense")

    sp = sub.add_parser("project", help="L3 (conceptual): is a symbol being read phonetically? (the ghost lag)")
    sp.add_argument("usage")

    sp = sub.add_parser("weigh", help="show a conceptual sign's retained weighted field")
    sp.add_argument("usage")

    sp = sub.add_parser("remember", help="the return path: how faithfully a later record carries an earlier truth back")
    sp.add_argument("usage")

    sp = sub.add_parser("chain", help="trace a truth's transmission lineage: decay and restoration across rememberings")
    sp.add_argument("concept")

    sp = sub.add_parser("confluence", help="weigh independent lineages: do they corroborate the source or diverge?")
    sp.add_argument("concept")

    sp = sub.add_parser("constellation", help="the system-level web: which values were load-bearing across a regime")
    sp.add_argument("--regime", default="breath", help="breath (default) or pump")

    sp = sub.add_parser("migrate", help="track a value across the threshold: held whole, then dispersed into lexemes")
    sp.add_argument("value")

    sub.add_parser("proliferation", help="the explosion of phonetic language: the sieve->success climb and coherence over time")
    sub.add_parser("untranslatables", help="concepts a single tongue valued enough to name (differential lexicalisation)")

    sp = sub.add_parser("regime", help="show a concept's breath/pump threshold and which side each sense sits")
    sp.add_argument("concept")

    sp = sub.add_parser("sense", help="the diachronic algebra of a word's senses")
    sp.add_argument("op", choices=["order", "ancestry", "common", "precedes"])
    sp.add_argument("concept")
    sp.add_argument("a", nargs="?")
    sp.add_argument("b", nargs="?")

    sp = sub.add_parser("align", help="interpretive alignment = purpose x fidelity")
    sp.add_argument("record")

    sp = sub.add_parser("imprint", help="record a reading as yours")
    sp.add_argument("file", nargs="?", help="file whose text is the passage")
    sp.add_argument("--text", help="inline text instead of a file")
    sp.add_argument("--id", required=True)
    sp.add_argument("--title", required=True)
    sp.add_argument("--author", default=DEFAULT_AUTHOR)
    sp.add_argument("--kind", default="note")
    sp.add_argument("--source", default="author")
    sp.add_argument("--actor", help="the producing agent, e.g. a model name")
    sp.add_argument("--parents", help="comma-separated lineage ids")
    sp.add_argument("--concept")
    sp.add_argument("--sense")
    sp.add_argument("--word")
    sp.add_argument("--citation")
    sp.add_argument("--period")
    sp.add_argument("--year", type=int)
    sp.add_argument("--regime", help="attention regime: breath / pump")
    sp.add_argument("--mode", help="script mode: conceptual / phonetic")
    sp.add_argument("--weights", help='weighted field, JSON or "k=v,k=v" (conceptual readings)')
    sp.add_argument("--artifact", help="material attestation (conceptual usages)")
    sp.add_argument("--license")
    sp.add_argument("--anchor", help="external anchor, e.g. git:<sha>")

    sp = sub.add_parser("manifest", help="publish the ledger as a defensive-publication manifest")
    sp.add_argument("--out", default="MANIFEST.md")

    sub.add_parser("verify", help="recompute the chain; any edit breaks it")
    sub.add_parser("status", help="one screen: chain, records, glossary")
    return p


_COMMANDS = {
    "concepts": cmd_concepts,
    "trace": cmd_trace,
    "attest": cmd_attest,
    "read": cmd_read,
    "drift": cmd_drift,
    "project": cmd_project,
    "weigh": cmd_weigh,
    "remember": cmd_remember,
    "chain": cmd_chain,
    "confluence": cmd_confluence,
    "constellation": cmd_constellation,
    "migrate": cmd_migrate,
    "proliferation": cmd_proliferation,
    "untranslatables": cmd_untranslatables,
    "regime": cmd_regime,
    "sense": cmd_sense,
    "align": cmd_align,
    "imprint": cmd_imprint,
    "manifest": cmd_manifest,
    "verify": cmd_verify,
    "status": cmd_status,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return _COMMANDS[args.command](args)
    except (KeyError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
