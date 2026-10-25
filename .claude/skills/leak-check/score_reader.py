#!/usr/bin/env python3
"""Score an isolated reader's reported figures against the generator's own.

The cracker table in a design note is a model of the opponent written by the author. The stage 4
reader is the measurement. task190 architecture 6 carried a cracker table claiming all three asks
missed and a precut pair ceiling of 28.5; its round-3 reader, holding only the pack and the prompt,
reported 43 of 43 graded figures. This script is how that is found before a build ships rather than
after three stage 4 rounds.

Usage
    python3 score_reader.py taskNN <reader.json> [--call-key K]... [--tol-pct 0.0] [--all-keys] [--quiet]

<reader.json> is a flat object the reader hands back, keyed exactly as <task>/generator/figures.json
is keyed, holding only the figures the reader actually committed to. A nested golden value is
addressed with a dot: "a1_Norte.contacts": 1965. Keys the reader did not answer are left out; a key
that is not in figures.json is reported as unknown and scored as nothing.

Only builds that nest the committed answer under `call.` are read as such without help. Many file it
at the top level under its own name ("plants_over_amber", "sectors_over_tolerance",
"referred_count"), and on those the scorer saw no call at all and reported "0 of 0 hit", which reads
as a pass and is the one output an audit must never produce silently. So name the call's keys with
--call-key, once per key; a key named this way is the committed answer whatever it is called, and
the scorer refuses to run when it can find no call key at all.

**Provenance is not scored.** `figures.json` carries provenance beside the graded answers: a pack's row
counts, a standard's stated constants, the window's dates. Those are not rubric criteria, and counting them
as ask figures inflates the leak: one build's reader scored 24 of 49 and 22 of the 24 were file row counts,
stated constants and window bounds, with every genuine device figure missed except two. They are dropped by
a prefix and exact-name list, printed in full on every run so the exclusion is auditable; `--all-keys` turns
it off. The list is a naming convention and not a reading of the submission, so a graded figure filed under
a provenance-shaped name is dropped silently: check the printed exclusions against the submission's blocks
before acting on a run.

**Emitting the key list.** `score_reader.py taskNN --emit-keys [--call-key K]...` writes the flat key
paths a reader should be briefed with, dropping any path whose own components name the call's members. A
component is distinguishing when every sibling at its position is a golden call member: a five-plant annex
naming the one plant over amber beside four that are not says nothing, while `call.slot_offences.<slot>`
holding exactly the eight slots of the committed slate hands the answer over. Brief from this output, never
from a raw flatten of `figures.json`.

**Hand the reader the key list.** Keys the reader invents are not in `figures.json`, score as nothing and
leave the denominator, so a reader that answered twenty ask figures under its own names measures as zero.
The scorer now refuses such a run rather than passing it, but the cure is the brief: give the reader the
flat key paths to fill.

A hit is an exact match at the golden's own precision: a float is compared rounded to the golden's
decimal places, a list elementwise, a string case-insensitively on the golden's first words. Pass
--tol-pct to allow a relative tolerance instead, for a figure whose rounding the ask does not state.

Exit status
    0  the call missed and under 20 per cent of ask figures hit: the ask layer holds
    1  the call was hit, or 35 per cent or more of ask figures hit: Gate F has failed, and the repair
       re-sites the devices rather than re-wording the asks (supplemental-stumping 1.1c)
    2  between 20 and 35 per cent of ask figures hit, call missed: thin, one ask needs re-siting
    3  usage or file error
"""
import json
import os
import sys
from pathlib import Path

CALL_PREFIX = "call"
# Keys under `call.` that are shared inputs rather than the committed answer. A build that nests its
# population, denominator and recorded counts under `call.` would otherwise trip the call verdict on
# figures every competent solver computes on the way, whatever answer it then files.
CALL_INPUT_WORDS = ("recorded", "payments", "population", "denominator", "window", "sent",
                    "baseline", "rows", "count_in", "exposure", "total_", "_total")


def decimals(x):
    s = repr(x)
    return len(s.split(".")[1]) if "." in s and "e" not in s.lower() else 0


def walk(value, key):
    """Resolve a dotted key against figures.json, longest segment first.

    A figures.json key can itself contain a dot: a build that files one block per cutoff keys them
    "0.030", "0.015" and so on. Splitting the path on every dot made those unaddressable and the
    scorer reported them as unknown rather than scoring them, which understates a reader's hit
    count on exactly the builds whose candidates are decimal values. So at each level take the
    longest remaining prefix that the dict actually holds, and only then fall back to one segment.
    """
    cur = value
    rest = key
    while rest:
        if not isinstance(cur, dict):
            return None, False
        if rest in cur:
            return cur[rest], True
        parts = rest.split(".")
        for n in range(len(parts) - 1, 0, -1):
            head = ".".join(parts[:n])
            if head in cur:
                cur = cur[head]
                rest = ".".join(parts[n:])
                break
        else:
            return None, False
    return cur, True


def same(gold, got, tol_pct):
    if isinstance(gold, str) or isinstance(got, str):
        g, r = str(gold).strip().lower(), str(got).strip().lower()
        if not g or not r:
            return g == r
        head = " ".join(g.split()[:3])
        return head in r or " ".join(r.split()[:3]) in g
    if isinstance(gold, (list, tuple)):
        if not isinstance(got, (list, tuple)) or len(gold) != len(got):
            return False
        return all(same(a, b, tol_pct) for a, b in zip(gold, got))
    if isinstance(gold, bool) or isinstance(got, bool):
        return gold == got
    try:
        g, r = float(gold), float(got)
    except (TypeError, ValueError):
        return gold == got
    if tol_pct:
        return abs(g - r) <= abs(g) * tol_pct / 100.0
    d = decimals(gold)
    return round(g, d) == round(r, d)


def emit_keys(gold, call_keys, quiet=False):
    """Write the reader's key list, with any key path that distinguishes the call's own members removed.

    The reader has to be told which figures to fill or it names its own keys and the run scores nothing
    (H34). But a key path can BE the answer: one build nested the committed slate under
    `call.slot_offences.<slot>`, one component per slot, so the key list named eight of the week's
    forty-two slots and only those eight. Its reader wrote that the refined method "reproduces the same
    eight slots as the slate the key names, which is why I used it", and the run scored the call as landed
    on a brief that had handed it over.

    A component is DISTINGUISHING when every sibling at its position is a golden call member. Where the
    siblings also carry non-members the list says nothing: a five-plant annex names the one plant over
    amber alongside four that are not, which is how the pack itself reads. So drop the distinguishing
    paths, keep the rest, and the asks stay scoreable.
    """
    rows = list(flat_keys(gold))
    # The call is often a dict (slate, runner-up, totals), so collect every string it holds at any depth:
    # it is the members of call.slate that a key path can name, not the dict.
    def strings_in(val):
        out = set()
        if isinstance(val, dict):
            for v in val.values():
                out |= strings_in(v)
        elif isinstance(val, (list, tuple)):
            for v in val:
                out |= strings_in(v)
        elif isinstance(val, str):
            out.add(val)
        return out

    members = set()
    for key in call_keys:
        val, ok = walk(gold, key)
        if ok:
            members |= strings_in(val)
    members = {m for m in members if len(m) > 2}

    # group every key path by its parent prefix, then test each parent's child labels
    kids = {}
    for key in rows:
        parts = key.split(".")
        for i in range(1, len(parts)):
            kids.setdefault(".".join(parts[:i]), set()).add(parts[i])
    distinguishing = {par for par, ch in kids.items()
                      if ch and members and ch <= members}

    kept, dropped = [], []
    for key in rows:
        parts = key.split(".")
        bad = any(".".join(parts[:i]) in distinguishing for i in range(1, len(parts)))
        (dropped if bad else kept).append(key)
    if dropped and not quiet:
        sys.stderr.write("dropped %d key path(s) whose own components name the call's members, under: %s\n"
                         % (len(dropped), ", ".join(sorted(distinguishing))))
    return kept, dropped


def flat_keys(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flat_keys(v, prefix + ("." if prefix else "") + str(k))
    else:
        yield prefix


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 3
    task = argv[1]
    reader_path = Path(argv[2] if not argv[2].startswith("--") else os.devnull)
    tol_pct = 0.0
    quiet = "--quiet" in argv
    if "--tol-pct" in argv:
        tol_pct = float(argv[argv.index("--tol-pct") + 1])
    call_keys = {argv[i + 1] for i, a in enumerate(argv) if a == "--call-key" and i + 1 < len(argv)}
    all_keys = "--all-keys" in argv
    emit = "--emit-keys" in argv

    root = Path(__file__).resolve().parents[3]
    figures = root / task / "generator" / "figures.json"
    if not figures.exists():
        print("no %s: the generator writes it, and figures_check.py reads it too" % figures)
        return 3
    if not reader_path.exists():
        print("no %s" % reader_path)
        return 3
    gold = json.loads(figures.read_text())
    if emit:
        if not call_keys:
            call_keys = {k for k in gold if k == CALL_PREFIX or k.startswith(CALL_PREFIX)}
        if not call_keys:
            sys.stderr.write("name the call with --call-key, or a key path that IS the answer stays in\n")
            return 3
        kept, _ = emit_keys(gold, call_keys, quiet)
        print("\n".join(kept))
        return 0
    got = json.loads(reader_path.read_text())
    if not isinstance(got, dict):
        print("the reader file holds %s, not an object keyed like figures.json" % type(got).__name__)
        return 3

    # Provenance is not a rubric criterion. figures.json carries the pack's row counts, the standard's
    # stated constants and the window's dates beside the graded answers, and scoring those as ask figures
    # inflates the leak: one build's reader scored 24 of 49 and 22 of the 24 were row counts, stated
    # constants and window bounds, every genuine device figure missing but two. The excluded set is a
    # prefix list, not a guess at meaning, and every key it drops is printed so the exclusion is auditable.
    # --all-keys turns it off.
    PROVENANCE = ("counts.", "constants.", "parameters.", "input_gates.", "sources.", "spine.")
    PROVENANCE_EXACT = ("as_of", "window_from", "window_to", "delivery_month", "delivery_start",
                        "filing_due", "org", "tso", "generator", "created")

    def is_provenance(key):
        if all_keys:
            return False
        return key.startswith(PROVENANCE) or key.split(".")[0] in PROVENANCE_EXACT

    rows, unknown, context = [], [], []
    for key in got:
        g, ok = walk(gold, key)
        if not ok:
            unknown.append(key)
            continue
        hit = same(g, got[key], tol_pct)
        head = key.split(".")[0]
        if key in call_keys or head in call_keys:
            kind = CALL_PREFIX
        elif head.startswith(CALL_PREFIX):
            tail = key[len(head):].lstrip(".").lower()
            kind = "input" if any(w in tail for w in CALL_INPUT_WORDS) else CALL_PREFIX
        else:
            if is_provenance(key):
                context.append(key)
                continue
            kind = "ask"
        rows.append((kind, key, g, got[key], hit))

    if not any(r[0] == CALL_PREFIX for r in rows):
        print("no call figure among the %d scored keys, and none named with --call-key." % len(rows))
        print("This build does not nest its committed answer under %r, so the call cannot be scored"
              % CALL_PREFIX)
        print("and a silent '0 of 0' would read as a pass. Name it, for example:")
        for key in sorted(gold)[:8]:
            print("    --call-key %s" % key)
        return 3

    call = [r for r in rows if r[0] == CALL_PREFIX]
    inputs = [r for r in rows if r[0] == "input"]
    asks = [r for r in rows if r[0] == "ask"]
    call_hit = sum(1 for r in call if r[4])
    ask_hit = sum(1 for r in asks if r[4])
    share = 100.0 * ask_hit / len(asks) if asks else 0.0

    if not quiet:
        for kind in (CALL_PREFIX, "input", "ask"):
            block = [r for r in rows if r[0] == kind]
            if not block:
                continue
            print("== %s figures ==" % {CALL_PREFIX: "call", "input": "call input (not the committed answer)",
                                        "ask": "ask"}[kind])
            for _, key, g, r, hit in sorted(block, key=lambda r: r[1]):
                print("%-4s %-34s golden %-26s reader %s" % ("HIT" if hit else "miss", key,
                                                             json.dumps(g)[:26], json.dumps(r)[:26]))
            print()
    if context:
        print("provenance, not graded by the submission, so not scored (%d): %s" %
              (len(context), ", ".join(sorted(context)[:14]) + (" ..." if len(context) > 14 else "")))
        print()
    if unknown:
        print("not in figures.json, scored as nothing: %s" % ", ".join(sorted(unknown)))
        print()
    # A key named for a set ("plants_over_amber") reads equally as that set or as its size, and a reader
    # that answers the size scores a clean miss on a call it may have landed. One build's reader filed 1
    # and 2 against goldens of one plant and two quarters and named all three in its prose, so the scorer
    # reported the call missed on a build where it held. Flag the shape; the reader's own words decide it.
    counted = [(key, g, r) for kind, key, g, r, hit in rows
               if not hit and isinstance(g, (list, tuple)) and isinstance(r, (int, float))
               and not isinstance(r, bool) and float(r) == len(g)]
    if counted:
        print("READ AS A COUNT, so these misses are not sound: the reader answered the size of a set where")
        print("the golden holds its members, and the size is right. Read the reader's prose before scoring")
        print("the call, and rename the key or ask for the members next time.")
        for key, g, r in counted:
            print("     %-34s golden %-30s reader %s" % (key, json.dumps(g)[:30], json.dumps(r)))
        print()

    print("call figures   %d of %d hit" % (call_hit, len(call)))
    if inputs:
        print("call inputs    %d of %d hit (shared route figures, not the verdict)"
              % (sum(1 for r in inputs if r[4]), len(inputs)))
    print("ask figures    %d of %d hit (%.1f per cent)" % (ask_hit, len(asks), share))

    # The same silent pass the call guard above refuses, one axis over. A reader that names its own keys
    # scores every one of them as nothing, they leave the denominator, and a build whose ask layer was
    # never measured prints PASS. task187's reader committed to 20 ask figures as curtailment_mwh.CH01
    # and downtime_mwh.CH01, none of them a figures.json key, and the scorer reported 0 of 0 and passed
    # the build. Refuse instead, and say which it was: an unmeasured ask layer, or a reader that declined.
    if not asks:
        print("\nno ask figure could be scored, so the ask layer is UNMEASURED, not holding.")
        if unknown:
            print("The reader committed to %d figure(s) under names figures.json does not carry, so they"
                  % len(unknown))
            print("left the denominator. Hand the reader the key list (the flat figures.json key paths)")
            print("and score again; do not read this run as a pass.")
        else:
            print("The reader answered no ask figure at all. Either the brief did not ask for them or it")
            print("declined; neither is evidence about the devices. Re-run the reader.")
        return 3
    # Unknown keys outnumbering scored ones means the same thing in weaker form: most of what the reader
    # committed to never reached the scorer, so the share below is a floor and not the measurement.
    if len(unknown) > len(asks):
        print("\nthin: %d unscoreable key(s) against %d scored, so the share above is a floor, not the"
              % (len(unknown), len(asks)))
        print("measurement. Re-run the reader against the key list before acting on it.")
        return 3

    if call_hit:
        print("\nFAIL  the reader landed the call. Gate F has failed and the architecture is spent:")
        print("      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.")
        return 1
    if share >= 35.0:
        print("\nFAIL  the ask layer leaks %.1f per cent, at or over the 35 bar. Re-site the devices:" % share)
        print("      a reader hit means the device is absent from its path, not weak.")
        return 1
    if share >= 20.0:
        print("\nWARN  %.1f per cent of ask figures hit, over the fifth the pair arithmetic budgets." % share)
        print("      Name the ask that leaked and re-site its primary device.")
        return 2
    print("\nPASS  the call missed and the ask layer holds under a fifth.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
