"""The ask layer's cracker and mirror sheets, scored on the cut pack (task134/target by default).

Stops are complete pipelines a competent response files. The cracker lands the call and takes the best stop it reaches
without an ask's silent device: it applies every filed rule (the licence's quarters by local date, its wet-tonne basis
and campaign rule, its formula for a vessel without a loading monitor, the lab's units) and runs the hygiene battery,
but reads the disposal site from the log's site column and each sample's area from the station plan, and has no key
for the loading-monitor revision or for the field duplicates. The mirror stops at the call's most attractive wrong
rung and handles the asks the same way. Pair = mean of C = 38 + 7 + 55 Lc and S = 5 + 7 + 55 Ls.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402

ASK_W = 55.0


def r1000(v):
    return int(round(v / 1000.0)) * 1000


def r2(v):
    return round(v + 1e-12, 2)


def main(tdir):
    gold_a, _ = A.ask_a(tdir)
    gold_b = A.ask_b(tdir)
    ga = {k: r1000(v) for k, v in gold_a.items()}
    gb = {k: r2(v) for k, v in gold_b.items()}
    stops_a = {
        "A0 site column, no revision, quarters in UTC": dict(site_by="planned", revision=False, clock="utc"),
        "A1 site column, no revision (cracker: filed rules applied)": dict(site_by="planned", revision=False),
        "A2 site from dump positions, no revision (full includer)": dict(revision=False),
        "A3 site from dump positions, revision, quarters in UTC": dict(clock="utc"),
        "golden": dict(),
    }
    stops_b = {
        "B0 station plan's area, duplicates dropped, mercury as reported": dict(part_by="plan", qa="drop", hg="raw"),
        "B1 station plan's area, duplicates dropped (cracker)": dict(part_by="plan", qa="drop"),
        "B2 sampled position's area, duplicates dropped (full includer)": dict(qa="drop"),
        "B3 station plan's area, duplicates paired": dict(part_by="plan"),
        "golden": dict(),
    }
    keep = {}
    print("ask A stops (%d figures):" % len(ga))
    for k, kw in stops_a.items():
        v, _ = A.ask_a(tdir, **kw)
        keep[k] = sum(1 for c in ga if r1000(v.get(c, 0.0)) == ga[c])
        print("  %-62s keeps %2d of %d" % (k, keep[k], len(ga)))
    print("ask B stops (%d figures):" % len(gb))
    for k, kw in stops_b.items():
        v = A.ask_b(tdir, **kw)
        keep[k] = sum(1 for c in gb if r2(v.get(c, -1.0)) == gb[c])
        print("  %-62s keeps %2d of %d" % (k, keep[k], len(gb)))
    tot = len(ga) + len(gb)
    ka = keep["A1 site column, no revision (cracker: filed rules applied)"]
    kb = keep["B1 station plan's area, duplicates dropped (cracker)"]
    lc = (ka + kb) / tot
    ls = lc
    C = 38 + 7 + ASK_W * lc
    S = 5 + 7 + ASK_W * ls
    print("cracker keeps %d of %d ask figures (%.1f per cent of ask weight); mirror the same" % (ka + kb, tot, 100 * lc))
    print("C = %.1f, S = %.1f, pair ceiling = %.1f; mirror leakage = %.1f per cent" % (C, S, (C + S) / 2, 100 * ls))
    fa = keep["A2 site from dump positions, no revision (full includer)"]
    fb = keep["B2 sampled position's area, duplicates dropped (full includer)"]
    C2 = 38 + 7 + ASK_W * (fa + fb) / tot
    print("full includer (both primaries found, the second devices missed): keeps %d of %d, C = %.1f, pair = %.1f"
          % (fa + fb, tot, C2, (C2 + S) / 2))
    z = os.path.join(os.path.dirname(tdir.rstrip("/")), "target.zip")
    if os.path.exists(z):
        print("measured on target.zip sha256 %s" % hashlib.sha256(open(z, "rb").read()).hexdigest()[:16])
    return dict(pair=(C + S) / 2, mirror=100 * ls, keep=keep, full=(C2 + S) / 2)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
