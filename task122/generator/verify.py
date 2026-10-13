"""task122: the independent verifier. Reads only the shipped bundle (target/), shares no code with the generator, and
recomputes the call, each dose's month-36 difference, the ladder's routes and the four asks; with --record it compares
them with the generator's record.

    python3 task122/generator/verify.py task122/target [--record record.json]
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date, timedelta

ARMS = ["Placebo", "VMK-4410 5 mg", "VMK-4410 10 mg", "VMK-4410 20 mg", "VMK-4410 40 mg"]
WEEK = {"DAY 1": 0, "WEEK 2": 2, "WEEK 4": 4, "WEEK 8": 8, "WEEK 12": 12, "WEEK 16": 16, "WEEK 20": 20, "WEEK 24": 24,
        "WEEK 32": 32, "WEEK 40": 40, "WEEK 52": 52}
CHECKS = [0]


def check(cond, label):
    if not cond:
        print("FAIL", label)
        sys.exit(1)
    CHECKS[0] += 1


def rows(tgt, name):
    with open(os.path.join(tgt, name), newline="") as fh:
        return list(csv.DictReader(fh))


def d(s):
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - b * mx, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tgt")
    ap.add_argument("--record")
    a = ap.parse_args()
    tgt = a.tgt
    arm = {r["USUBJID"]: r["ARM"] for r in rows(tgt, "dm.csv") if r["ARM"]}
    check(len(arm) == sum(1 for r in rows(tgt, "ds.csv") if r["DSDECOD"] == "RANDOMIZED"), "randomised patients in dm equal the randomisation milestones")
    first, last = {}, {}
    exr = defaultdict(list)
    for r in rows(tgt, "ex.csv"):
        u = r["USUBJID"]
        s, e = d(r["EXSTDTC"]), d(r["EXENDTC"])
        first[u] = min(first.get(u, s), s)
        last[u] = max(last.get(u, e), e)
        exr[u].append((s, e))
    wk52 = {}
    for r in rows(tgt, "sv.csv"):
        if r["VISIT"] == "WEEK 52":
            wk52[r["USUBJID"]] = d(r["SVSTDTC"])
    stopped = {u for u in arm if u not in wk52 or last[u] < wk52[u]}

    # ---------------------------------------------------------------- main call
    egfr = {}
    for r in rows(tgt, "lb.csv"):
        if r["LBTESTCD"] != "EGFR" or not r["LBNAM"].startswith("Tavlund Central") or r["USUBJID"] not in arm:
            continue
        v = r["VISIT"]
        if v != "SCREENING" and v not in WEEK:
            continue
        key = (r["USUBJID"], v)
        if key not in egfr or r["LBDTC"] < egfr[key][0]:
            egfr[key] = (r["LBDTC"], float(r["LBSTRESN"]))
    base = {}
    for u in arm:
        b = [egfr[(u, v)][1] for v in ("SCREENING", "DAY 1") if (u, v) in egfr]
        if b:
            base[u] = sum(b) / len(b)
    acc = defaultdict(list)
    for (u, v), (dtc, val) in egfr.items():
        if v == "SCREENING" or u not in base:
            continue
        if u in stopped and d(dtc) > last[u]:
            continue
        acc[(arm[u], WEEK[v])].append(val - base[u])
    mean = {k: sum(x) / len(x) for k, x in acc.items()}
    wks = sorted({w for (_, w) in mean})

    def route(dose, start, at=156):
        xs = [w / 52.0 for w in wks if w >= start]
        ys = [mean[(dose, w)] - mean[("Placebo", w)] for w in wks if w >= start]
        c, b = fit(xs, ys)
        return c + b * at / 52.0

    out = {"gold": {}, "routes": {}}
    for dose in ARMS[1:]:
        out["gold"][dose] = route(dose, 24)
        out["routes"][dose] = {"w52": mean[(dose, 52)] - mean[("Placebo", 52)], "k0": route(dose, 0), "k12": route(dose, 12),
                               "k16": route(dose, 16), "k20": route(dose, 20), "k32": route(dose, 32)}
    order = sorted(ARMS[1:], key=lambda x: -out["gold"][x])
    out["call"], out["runner"] = order[0], order[1]
    check(out["call"] == "VMK-4410 20 mg", "call 20 mg")
    check(max(ARMS[1:], key=lambda x: out["routes"][x]["k12"]) == "VMK-4410 40 mg", "the month-3 route files 40 mg")
    check(max(ARMS[1:], key=lambda x: out["routes"][x]["w52"]) == "VMK-4410 10 mg", "the week-52 difference files 10 mg")
    check(max(ARMS[1:], key=lambda x: out["routes"][x]["k0"]) == "VMK-4410 10 mg", "one slope through every visit files 10 mg")

    # ---------------------------------------------------------------- asks
    hik = defaultdict(set)
    for r in rows(tgt, "lb.csv"):
        if r["LBTESTCD"] != "K" or r["LBSPEC"] != "SERUM" or r["USUBJID"] not in arm or r["LBSTRESN"] == "":
            continue
        u = r["USUBJID"]
        t = d(r["LBDTC"])
        if first[u] < t <= last[u] and float(r["LBSTRESN"]) > 5.5:
            hik[arm[u]].add(u)
    ev = {}
    for r in rows(tgt, "ae.csv"):
        if r["AEDECOD"] not in ("Hyperkalaemia", "Blood potassium increased") or r["USUBJID"] not in arm:
            continue
        u = r["USUBJID"]
        s = r["AESTDTC"]
        if len(s) == 10:
            st = d(s)
        elif len(s) == 7:
            y, m = int(s[:4]), int(s[5:7])
            st = first[u] if (first[u].year, first[u].month) == (y, m) else date(y, m, 1)
        else:
            st = first[u] if first[u].year == int(s[:4]) else date(int(s[:4]), 1, 1)
        k = (u, r["AEGRPID"])
        ev[k] = min(ev.get(k, st), st)
    aes = defaultdict(int)
    for (u, g), st in ev.items():
        if first[u] <= st <= last[u]:
            aes[arm[u]] += 1
    years = defaultdict(float)
    for u, segs in exr.items():
        if u not in arm:
            continue
        cut = wk52.get(u)
        days = set()
        for s, e in segs:
            x = s
            while x <= e:
                if cut is None or x < cut:
                    days.add(x)
                x += timedelta(days=1)
        years[arm[u]] += len(days) / 365.25
    out["asks"] = {"A_k": {x: len(hik[x]) for x in ARMS}, "A_ae": {x: aes[x] for x in ARMS},
                   "B_stop": {x: sum(1 for u in stopped if arm[u] == x) for x in ARMS}, "B_years": {x: years[x] for x in ARMS}}
    if a.record:
        rec = json.load(open(a.record))
        for dose in ARMS[1:]:
            check(abs(rec["gold"][dose] - out["gold"][dose]) < 1e-9, "gold %s agrees" % dose)
            for k in ("w52", "k0", "k12", "k16", "k20", "k32"):
                check(abs(rec["routes"][dose][k] - out["routes"][dose][k]) < 1e-9, "route %s %s agrees" % (k, dose))
        for k in ("A_k", "A_ae", "B_stop"):
            for x in ARMS:
                check(rec["asks"][k][x] == out["asks"][k][x], "ask %s %s agrees (%s against %s)" % (k, x, rec["asks"][k][x], out["asks"][k][x]))
        for x in ARMS:
            check(abs(rec["asks"]["B_years"][x] - out["asks"]["B_years"][x]) < 1e-9, "ask B_years %s agrees" % x)
        check(rec["call"] == out["call"] and rec["runner"] == out["runner"], "call and runner-up agree")
    print("verify: %d checks passed; call %s; month-36 differences %s" % (
        CHECKS[0], out["call"], {k.replace("VMK-4410 ", ""): round(v, 3) for k, v in out["gold"].items()}))


if __name__ == "__main__":
    main()
