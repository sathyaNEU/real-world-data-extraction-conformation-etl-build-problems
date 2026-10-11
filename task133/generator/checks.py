"""Assertions on task133's shipped pack: input gates, the answer, the ladder, rounding margins."""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
n_ok = 0


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def edge(v, unit):
    return abs((v / unit) % 1 - 0.5)


def main():
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "10 or more input files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    bk = pd.read_csv(os.path.join(T, E.F["book"]), dtype=str)
    ok(len(bk) >= 25000, "loan book has 25,000 or more rows (%d)" % len(bk))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors on disk")
    for f in files:
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2", "test_")), "file name %s carries no author noun" % f)

    s = E.solve(T)
    A = s["total"]
    ok(abs(s["mult"] - 1.06) < 1e-12, "weighted PD multiplier 1.06")
    # every graded figure clears its rounding edge by at least six per cent of the bin
    vals = [("total", A, 1000), ("stage1", s["stage1"], 1000), ("stage2", s["stage2"], 1000)]
    for st in (1, 2):
        for p in ("PL36", "PL60"):
            vals += [("%s_s%d" % (p, st), s["%s_s%d" % (p, st)], 1000), ("%s_s%d_gca" % (p, st), s["%s_s%d_gca" % (p, st)], 1000),
                     ("%s_s%d_cov" % (p, st), s["%s_s%d_cov" % (p, st)], 0.01)]
    for key, v in s["by_band"].items():
        vals.append(("year %s %s" % key, v, 1000))
    for name, v, u in vals:
        ok(edge(v, u) >= 0.05, "%s clears its rounding edge (%.4f)" % (name, edge(v, u)))
    # the ladder
    rung = {}
    for nm, kw in [("uncond", dict(variant="uncond")), ("shift", dict(variant="shift")), ("nodisc", dict(disc=False)),
                   ("flat_ead", dict(flat_ead=True))]:
        rung[nm] = E.solve(T, **kw)["total"] / A - 1
    ok(rung["uncond"] >= 0.20, "the curve read from origination for every loan is at least 20 per cent high (%.3f)" % rung["uncond"])
    ok(rung["shift"] <= -0.06, "the curve shifted to months on book without the survival division is at least 6 per cent low (%.3f)" % rung["shift"])
    ok(rung["nodisc"] >= 0.06, "skipping the discount is at least 6 per cent high (%.3f)" % rung["nodisc"])
    ok(rung["flat_ead"] >= 0.10, "holding the balance flat is at least 10 per cent high (%.3f)" % rung["flat_ead"])
    # staging devices move the stage split, not only the total
    nh = E.solve(T, use_hardship=False)
    nm = E.solve(T, map_v3=False)
    ok(abs(nh["n2"] - s["n2"]) >= 300, "the hardship register moves at least 300 loans into stage 2 (%d)" % abs(nh["n2"] - s["n2"]))
    ok(abs(nm["n2"] - s["n2"]) >= 100, "the v3 conversion moves at least 100 loans across the stage line (%d)" % abs(nm["n2"] - s["n2"]))
    ok(s["n3"] > 0, "stage 3 loans are in the extract and outside the model")
    print("CHECKS PASS", n_ok, {k: round(v, 4) for k, v in rung.items()})


if __name__ == "__main__":
    main()
