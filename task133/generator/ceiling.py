"""The ask layer's cracker and mirror sheets, scored on the cut pack (task133/target by default).

Stops per ask are complete pipelines a competent response files. The cracker lands the call and takes the best stop it
reaches without the ask's silent device (it nets credit notes against the duplicated lines and drops re-sent dockets,
the hygiene battery); the mirror stops at the call's most attractive wrong rung and handles the asks the same way.
Pair = mean of C = 38 + 7 + 55 Lc and S = 5 + 7 + 55 Ls.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402
import results as R  # noqa: E402

ASK_W = 55.0


def main(tdir):
    pk = A.Pack(tdir)
    gold_a = {k: R.rhu(v / 1e3, 0) for k, v in A.ask_a(tdir, pk).items()}
    gold_b = {k: R.nearest(v, 10) for k, v in A.ask_b(tdir).items()}
    stops_a = {
        "A0 billed carrier code, credit notes left out": dict(by_owner=False, credits=False),
        "A1 billed carrier code, credit notes netted (battery run)": dict(by_owner=False, credits=True),
        "A2 the unit's carrier, credit notes left out": dict(by_owner=True, credits=False),
        "golden": dict(by_owner=True, credits=True),
    }
    stops_b = {
        "B0 docket date, re-sent dockets kept": dict(by_weighbridge=False, dedupe=False),
        "B1 docket date, re-sent dockets dropped (battery run)": dict(by_weighbridge=False, dedupe=True),
        "golden": dict(by_weighbridge=True),
    }
    keep = {}
    print("ask A stops (%d figures):" % len(gold_a))
    for k, kw in stops_a.items():
        v = {c: R.rhu(x / 1e3, 0) for c, x in A.ask_a(tdir, pk, **kw).items()}
        keep[k] = sum(1 for c in gold_a if v[c] == gold_a[c])
        print("  %-62s keeps %2d of %d" % (k, keep[k], len(gold_a)))
    print("ask B stops (%d figures):" % len(gold_b))
    for k, kw in stops_b.items():
        v = {c: R.nearest(x, 10) for c, x in A.ask_b(tdir, **kw).items()}
        keep[k] = sum(1 for c in gold_b if v[c] == gold_b[c])
        print("  %-62s keeps %2d of %d" % (k, keep[k], len(gold_b)))
    tot = len(gold_a) + len(gold_b)
    ck = keep["A1 billed carrier code, credit notes netted (battery run)"] + keep["B1 docket date, re-sent dockets dropped (battery run)"]
    lc = ls = ck / tot
    C = 38 + 7 + ASK_W * lc
    S = 5 + 7 + ASK_W * ls
    print("cracker keeps %d of %d ask figures (%.1f per cent of ask weight); mirror the same" % (ck, tot, 100 * lc))
    print("C = %.1f, S = %.1f, pair ceiling = %.1f; mirror leakage = %.1f per cent" % (C, S, (C + S) / 2, 100 * ls))
    one = max(len(gold_a) + keep["B1 docket date, re-sent dockets dropped (battery run)"],
              keep["A1 billed carrier code, credit notes netted (battery run)"] + len(gold_b))
    C2 = 38 + 7 + ASK_W * one / tot
    print("if the cracker also finds one silent device: keeps %d of %d, C = %.1f, pair = %.1f" % (one, tot, C2, (C2 + S) / 2))
    z = os.path.join(os.path.dirname(tdir.rstrip("/")), "target.zip")
    if os.path.exists(z):
        print("measured on target.zip sha256 %s" % hashlib.sha256(open(z, "rb").read()).hexdigest()[:16])
    return dict(pair=(C + S) / 2, mirror=100 * ls)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
