"""Assertions on the shipped pack: input gates, the answer, the ladder, bin margins, no symptom on the wrong path."""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
n_ok = 0


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def main():
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "10 or more input files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    wo = pd.read_csv(os.path.join(T, E.F["wo"]), dtype=str)
    ok(len(wo) >= 25000, "work-order spine has 25,000 or more rows (%d)" % len(wo))
    ok(wo["reported_date"].min() >= "2021-01-01", "no work order before the EAM go-live")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors on disk")
    for f in files:
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2")), "file name %s carries no author noun" % f)

    s = E.solve(T)
    ok(s["lots"] == 19, "answer is 19 lots (%d)" % s["lots"])
    ok(s["cover"] >= W.COVER > s["settings"][s["lots"] - 1]["cover"], "19 lots clears 95 per cent and 18 does not")
    ok(s["avail"] == 39, "39 modules available")
    # bin margins on the expected failures
    def lots_at(l):
        return E.lots_needed(l, s["avail"])
    lo, hi = s["lam"], s["lam"]
    while lots_at(lo) == s["lots"]:
        lo -= 0.05
    while lots_at(hi) == s["lots"]:
        hi += 0.05
    ok((s["lam"] - lo) / s["lam"] >= 0.02 and (hi - s["lam"]) / s["lam"] >= 0.02,
       "expected failures sit at least 2 per cent inside the 19-lot bin (%.1f < %.1f < %.1f)" % (lo, s["lam"], hi))
    for y, v in s["by_year"].items():
        ok(abs(v * 10 - round(v * 10)) <= 0.45, "year %d figure clear of its rounding edge" % y)
    ok(abs(sum(s["by_year"].values()) - s["lam"]) < 1e-6, "years add to the total")
    ok(abs(sum(s["by_region"].values()) - s["lam"]) < 1e-6, "regions add to the total")
    ok(list(s["in_service"].values()) == sorted(s["in_service"].values(), reverse=True), "supported relays fall year on year")

    r, avail = E.rungs(T)
    ans = r["ANSWER"][0]
    for k, (v, l) in r.items():
        if k in ("ANSWER", "banded_window_2025_plan"):
            continue
        ok(l != s["lots"], "rung %s lands on %d lots, not the answer" % (k, l))
    # the superseded 2025 plan is a Layer 1 misreading: it may converge on the lot count, never on the
    # relays-supported column it feeds
    reg0, wo0, subs0, stock0, plan0 = E.load(T)
    in25 = E.in_service_jan1(E.fleet(reg0), plan0["2025 plan (superseded)"])
    ok(sum(in25[y] != s["in_service"][y] for y in in25) >= 6, "the 2025 plan misstates the supported relays in most years")
    ok(r["banded_install"][0] <= 0.88 * ans, "exposure from installation is at least 12 per cent low")
    ok(r["trailing_rate"][0] <= 0.88 * ans, "the trailing twelve-month rate is at least 12 per cent low")
    ok(r["pooled_window"][0] <= 0.6 * ans, "one pooled rate is far low")
    near = min(abs(v / ans - 1) for k, (v, l) in r.items() if k not in ("ANSWER", "banded_window_2025_plan"))
    ok(near >= 0.10, "every methodological rung at least 10 per cent from the answer (%.3f)" % near)

    # the wrong path has no arithmetic symptom: its own back-test ties exactly
    reg, wo2, subs, stock, plan = E.load(T)
    fl = E.fleet(reg)
    f = E.failures(wo2, fl)
    expI = E.exposure(fl, None)
    rI, cnt = E.rates(f, expI)
    ok(abs((rI * expI / 12).sum() - len(f)) < 1e-6, "install-exposure rates reproduce every recorded failure")
    expW = E.exposure(fl, W.MIGRATION)
    ok(expI.sum() > 2.5 * expW.sum(), "install exposure is mostly pre-2021 relay-months")
    ok((expI[3:] >= expW[3:]).all(), "bands")
    print("CHECKS PASS", n_ok)


if __name__ == "__main__":
    main()
