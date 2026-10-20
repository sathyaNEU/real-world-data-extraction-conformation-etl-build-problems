#!/usr/bin/env python3
"""Score an isolated reader's reported figures against the generator's own.

The cracker table in a design note is a model of the opponent written by the author. The stage 4
reader is the measurement. task190 architecture 6 carried a cracker table claiming all three asks
missed and a precut pair ceiling of 28.5; its round-3 reader, holding only the pack and the prompt,
reported 43 of 43 graded figures. This script is how that is found before a build ships rather than
after three stage 4 rounds.

Usage
    python3 score_reader.py taskNN <reader.json> [--tol-pct 0.0] [--quiet]

<reader.json> is a flat object the reader hands back, keyed exactly as <task>/generator/figures.json
is keyed, holding only the figures the reader actually committed to. A nested golden value is
addressed with a dot: "a1_Norte.contacts": 1965. Keys the reader did not answer are left out; a key
that is not in figures.json is reported as unknown and scored as nothing.

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
import sys
from pathlib import Path

CALL_PREFIX = "call"


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


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 3
    task = argv[1]
    reader_path = Path(argv[2])
    tol_pct = 0.0
    quiet = "--quiet" in argv
    if "--tol-pct" in argv:
        tol_pct = float(argv[argv.index("--tol-pct") + 1])

    root = Path(__file__).resolve().parents[3]
    figures = root / task / "generator" / "figures.json"
    if not figures.exists():
        print("no %s: the generator writes it, and figures_check.py reads it too" % figures)
        return 3
    if not reader_path.exists():
        print("no %s" % reader_path)
        return 3
    gold = json.loads(figures.read_text())
    got = json.loads(reader_path.read_text())
    if not isinstance(got, dict):
        print("the reader file holds %s, not an object keyed like figures.json" % type(got).__name__)
        return 3

    rows, unknown = [], []
    for key in got:
        g, ok = walk(gold, key)
        if not ok:
            unknown.append(key)
            continue
        hit = same(g, got[key], tol_pct)
        rows.append((CALL_PREFIX if key.split(".")[0].startswith(CALL_PREFIX) else "ask", key, g, got[key], hit))

    call = [r for r in rows if r[0] == CALL_PREFIX]
    asks = [r for r in rows if r[0] == "ask"]
    call_hit = sum(1 for r in call if r[4])
    ask_hit = sum(1 for r in asks if r[4])
    share = 100.0 * ask_hit / len(asks) if asks else 0.0

    if not quiet:
        for kind in (CALL_PREFIX, "ask"):
            block = [r for r in rows if r[0] == kind]
            if not block:
                continue
            print("== %s figures ==" % ("call" if kind == CALL_PREFIX else "ask"))
            for _, key, g, r, hit in sorted(block, key=lambda r: r[1]):
                print("%-4s %-34s golden %-26s reader %s" % ("HIT" if hit else "miss", key,
                                                             json.dumps(g)[:26], json.dumps(r)[:26]))
            print()
    if unknown:
        print("not in figures.json, scored as nothing: %s" % ", ".join(sorted(unknown)))
        print()

    print("call figures   %d of %d hit" % (call_hit, len(call)))
    print("ask figures    %d of %d hit (%.1f per cent)" % (ask_hit, len(asks), share))

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
