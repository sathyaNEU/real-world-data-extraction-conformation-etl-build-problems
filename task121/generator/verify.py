"""The independent verifier: every graded figure recomputed from the shipped files by a second code path (the walk
by dense least squares on dummy columns, the annexes by plain loops over the CSV rows), compared with
generator/figures.json at the stated rounding.

    python3 task121/generator/verify.py"""
from __future__ import annotations

import csv
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common as K   # noqa: E402

NAMES = {s[0]: s[1] for s in K.SECONDARIES}
TRUST = [NAMES[k] for k in K.TRUST_KEYS]


def rnd(x, nd):
    v = float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))
    s = "%.*f" % (nd, v)
    return "0.0" if s in ("-0.0", "0.0") and nd == 1 else s


def rows(target, key):
    with open(os.path.join(target, K.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def walk(target):
    reg = rows(target, "register")
    pred = {r["urn"]: r["predecessor_urn"] for r in reg if r["phase"] == "Primary" and r["predecessor_urn"]}
    P = [r for r in rows(target, "transfer") if r["p8_score"]]
    secs = sorted({r["ks4_school"] for r in P})
    pris = sorted({r["ks2_la"] + "/" + pred.get(r["ks2_urn"], r["ks2_urn"]) for r in P})
    si = {s: i for i, s in enumerate(secs)}
    pi = {p: i for i, p in enumerate(pris)}
    n = len(P)
    X = np.zeros((n, 2 + len(secs) + len(pris) - 1))
    y = np.zeros(n)
    for j, r in enumerate(P):
        poss = float(r["y11_sessions_possible"])
        X[j, 0] = 100.0 * (float(r["y11_sessions_auth_absence"]) + float(r["y11_sessions_unauth_absence"])) / poss
        X[j, 1] = 1.0 if r["disadvantaged"] == "Y" else 0.0
        X[j, 2 + si[r["ks4_school"]]] = 1.0
        q = pi[r["ks2_la"] + "/" + pred.get(r["ks2_urn"], r["ks2_urn"])]
        if q > 0:
            X[j, 2 + len(secs) + q - 1] = 1.0
        y[j] = float(r["p8_score"])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    eff = {s: beta[2 + i] for s, i in si.items()}
    t = [j for j, r in enumerate(P) if r["ks4_school"] in TRUST]
    h = [j for j, r in enumerate(P) if r["ks4_school"] == NAMES[K.FOCAL]]
    gap = y[h].mean() - y[t].mean()
    att = beta[0] * (X[h, 0].mean() - X[t, 0].mean())
    dis = beta[1] * (X[h, 1].mean() - X[t, 1].mean())
    own = np.mean([eff[P[j]["ks4_school"]] for j in h]) - np.mean([eff[P[j]["ks4_school"]] for j in t])
    return dict(gap=gap, att=att, dis=dis, own=own, rem=gap - att - dis - own,
                trust=y[t].mean(), halwick=y[h].mean())


HT = ["Autumn 1", "Autumn 2", "Spring 1", "Spring 2", "Summer 1", "Summer 2"]
HT_START = ["2025-09-03", "2025-11-03", "2026-01-05", "2026-02-23", "2026-04-13", "2026-06-08"]


def annex_a(target):
    moves = {}
    for r in rows(target, "movements"):
        if r["movement"] == "Transfer within trust":
            moves[r["upn"]] = (r["movement_date"], r["from_school"])
    tot = {}
    for r in rows(target, "attendance"):
        h = HT.index(r["half_term"])
        yg = int(r["year_group"]) - (1 if r["on_roll"] == "Y" else 0)
        if yg == 11 and h >= 4:
            continue
        acad = r["academy"]
        mv = moves.get(r["upn"])
        if mv and HT_START[h] < mv[0]:
            acad = mv[1]
        k = (acad, r["upn"])
        a = tot.setdefault(k, [0, 0])
        a[0] += int(r["sessions_possible"])
        a[1] += int(r["sessions_auth_absence"]) + int(r["sessions_unauth_absence"])
    out = {}
    for (acad, upn), (poss, miss) in tot.items():
        o = out.setdefault(acad, [0, 0, 0])
        o[0] += 1
        o[1] += miss >= 0.10 * poss
        o[2] += miss >= 0.50 * poss
    return {k: (100.0 * v[1] / v[0], 100.0 * v[2] / v[0]) for k, v in out.items()}


EB = {"Biology", "Chemistry", "Physics", "Computer Science", "History", "Geography", "French", "Spanish", "Urdu",
      "Polish"}
FIRST = EB | {"English Language", "English Literature", "Mathematics", "Combined Science"}
TA = {"L2D*": 8.5, "L2D": 7.0, "L2M": 5.5, "L2P": 4.0, "L1D*": 3.0, "L1D": 2.0, "L1M": 1.5, "L1P": 1.25, "U": 0.0}


def score(r):
    if r["qualification"] == "Technical Award":
        return TA[r["grade"]]
    if r["subject"] == "Combined Science":
        a, b = r["grade"].split("-")
        return (float(a) + float(b)) / 2
    return 0.0 if r["grade"] == "U" else float(r["grade"])


def a8(entries):
    by_code = {}
    for e in sorted(entries, key=lambda e: e["series"][-4:]):          # earliest series first
        c = e["discount_code"]
        if c not in by_code:
            by_code[c] = e
        elif e["subject"] not in FIRST and score(e) > score(by_code[c]):
            by_code[c] = e
    q = list(by_code.values())
    s = {e["subject"]: score(e) for e in q}
    total = 2 * s.get("Mathematics", 0.0)
    left = []
    if "English Language" in s and "English Literature" in s:
        hi, lo = sorted([s["English Language"], s["English Literature"]], reverse=True)
        total += 2 * hi
        left.append(lo)
    elif "English Language" in s or "English Literature" in s:
        total += s.get("English Language", s.get("English Literature"))
    ebs = []
    for e in q:
        if e["subject"] == "Combined Science":
            ebs += [score(e)] * 2
        elif e["subject"] in EB:
            ebs.append(score(e))
    ebs.sort(reverse=True)
    total += sum(ebs[:3])
    left += ebs[3:]
    left += [score(e) for e in q if e["subject"] not in FIRST]
    left.sort(reverse=True)
    return total + sum(left[:3])


def entered(entries):
    s = {e["subject"] for e in entries}
    sci = "Combined Science" in s or len(s & {"Biology", "Chemistry", "Physics", "Computer Science"}) >= 2
    return ("English Language" in s and "English Literature" in s and "Mathematics" in s and sci
            and bool(s & {"History", "Geography"}) and bool(s & {"French", "Spanish", "Urdu", "Polish"}))


def annex_b(target):
    by = {}
    centre = {}
    for r in rows(target, "results26"):
        by.setdefault(r["upn"], []).append(r)
        centre[r["upn"]] = r["centre_name"]
    for r in rows(target, "results25"):
        if r["upn"] in by:
            by[r["upn"]].append(r)
    out = {}
    for upn, es in by.items():
        o = out.setdefault(centre[upn], [0, 0.0, 0])
        o[0] += 1
        o[1] += a8(es)
        o[2] += entered(es)
    return {k: (v[1] / v[0], 100.0 * v[2] / v[0]) for k, v in out.items()}


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    n = 0
    w = walk(target)
    for k in ("gap", "att", "dis", "own", "rem"):
        n += 1
        if rnd(w[k], 1) != fig["walk"][k]:
            bad.append("walk %s %s against %s" % (k, rnd(w[k], 1), fig["walk"][k]))
    for k, f in (("trust", "trust_p8"), ("halwick", "halwick_p8")):
        n += 1
        if rnd(w[k], 2) != fig[f]:
            bad.append("%s %s against %s" % (k, rnd(w[k], 2), fig[f]))
    big = min(("att", "dis", "own", "rem"), key=lambda k: w[k])
    n += 1
    if big != fig["call"]["largest"]:
        bad.append("largest %s against %s" % (big, fig["call"]["largest"]))
    a = annex_a(target)
    for k, (pa, sa) in a.items():
        n += 2
        if rnd(pa, 1) != fig["annex_a"][k]["pa"]:
            bad.append("annex A pa %s %s against %s" % (k, rnd(pa, 1), fig["annex_a"][k]["pa"]))
        if rnd(sa, 1) != fig["annex_a"][k]["sa"]:
            bad.append("annex A sa %s %s against %s" % (k, rnd(sa, 1), fig["annex_a"][k]["sa"]))
    b = annex_b(target)
    for k, (av, eb) in b.items():
        n += 2
        if rnd(av, 1) != fig["annex_b"][k]["a8"]:
            bad.append("annex B a8 %s %s against %s" % (k, rnd(av, 1), fig["annex_b"][k]["a8"]))
        if rnd(eb, 1) != fig["annex_b"][k]["ebacc"]:
            bad.append("annex B ebacc %s %s against %s" % (k, rnd(eb, 1), fig["annex_b"][k]["ebacc"]))
    print("verify: %d figures, %s" % (n, "PASS" if not bad else "FAIL"))
    for x in bad:
        print("  ", x)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run(TASK))
