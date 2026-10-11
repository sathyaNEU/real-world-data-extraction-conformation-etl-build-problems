"""Assertions on the shipped pack: input gates, the answer, the ladder, bin margins, rounding edges."""
import datetime as dt
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
n_ok = 0
LOTS = 13


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def edge(v):
    return abs((v * 10) % 1 - 0.5)


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
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2", "test_")), "file name %s carries no author noun" % f)

    s = E.solve(T)
    ok(s["lots"] == LOTS, "answer is %d lots (%d)" % (LOTS, s["lots"]))
    ok(s["cover"] >= W.COVER > s["settings"][s["lots"] - 1]["cover"], "the answer clears 95 per cent and one lot fewer does not")
    ok(min(W.SETTINGS) <= s["lots"] - 3 and max(W.SETTINGS) >= s["lots"] + 5, "the asked settings run well either side of the answer")
    lo, hi = s["lam"], s["lam"]
    while E.lots_needed(lo, s["avail"]) == s["lots"]:
        lo -= 0.05
    while E.lots_needed(hi, s["avail"]) == s["lots"]:
        hi += 0.05
    ok((s["lam"] - lo) / s["lam"] >= 0.025 and (hi - s["lam"]) / s["lam"] >= 0.025,
       "expected failures sit at least 2.5 per cent inside the answer's lot bin (%.1f < %.1f < %.1f)" % (lo, s["lam"], hi))
    vals = [s["lam"]] + list(s["by_year"].values()) + list(s["by_region"].values()) + [
        100 * v["cover"] for v in s["settings"].values() if 0.05 < 100 * v["cover"] < 99.95]
    for v in vals:
        ok(edge(v) >= 0.04, "figure %.4f clear of its one-decimal rounding edge" % v)
    ok(abs(sum(s["by_year"].values()) - s["lam"]) < 1e-6, "years add to the total")
    ok(abs(sum(s["by_region"].values()) - s["lam"]) < 1e-6, "regions add to the total")
    ok(list(s["in_service"].values()) == sorted(s["in_service"].values(), reverse=True), "supported relays fall year on year")

    r, avail = E.rungs(T)
    ans = r["ANSWER"][0]
    for k, (v, l) in r.items():
        if k == "ANSWER":
            continue
        ok(l != s["lots"], "rung %s lands on %d lots, not the answer" % (k, l))
    ok(r["window_no_renewal"][1] >= s["lots"] + 3, "keeping today's module in every month is at least three lots high")
    ok(r["window_no_renewal"][0] >= 1.25 * ans, "and at least 25 per cent high")
    ok(r["install_renewal"][0] <= 0.88 * ans, "exposure from fitting rather than the go-live is at least 12 per cent low")
    ok(r["relay_age_window_no_renewal"][0] <= 0.88 * ans, "relay age in place of module age is at least 12 per cent low")
    ok(r["trailing_rate"][0] <= 0.80 * ans, "the trailing twelve-month rate is at least 20 per cent low")
    # staged schemes and the superseded plan show in the supported-relay column
    reg0, wo0, hist0, subs0, stock0, plan0 = E.load(T)
    fl0 = E.fleet(reg0)
    in25 = E.in_service_jan1(fl0, plan0["2025 plan (superseded)"])
    ok(sum(in25[y] != s["in_service"][y] for y in in25) >= 6, "the 2025 plan misstates the supported relays in most years")
    p26 = plan0["Approved 2026"]
    first = {sub: min((w or E.month_add(W.PROGRAMME_END, 1)) for _, w in rows) for sub, rows in p26.items()}
    live = fl0[fl0["status"] == "IN SERVICE"]
    by_station = {y: int(sum(1 for sub in live["sub_code"] if sub in first and first[sub] > dt.date(y, 1, 1))) for y in range(2027, 2036)}
    ok(sum(by_station[y] != s["in_service"][y] for y in by_station) >= 5, "reading a staged scheme by station misstates the supported relays")
    # every module counted in the rates is in the history the procedure names, and the failures tie to it
    f = E.failures(wo0, fl0, hist0)
    ok(len(f) == s["n_fail"] and f["fitted"].notna().all(), "every failure ties to the module it removed")
    ok((hist0["removal_reason"] == "FAILED").sum() >= len(f), "the history records a removal for every failure")
    print("CHECKS PASS", n_ok)


if __name__ == "__main__":
    main()
