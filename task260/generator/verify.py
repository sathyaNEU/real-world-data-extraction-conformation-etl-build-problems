"""Independent verifier for task260: reads only target/ and golden/, shares no code with the generator, and recomputes
the call (each reader's area by scipy's Mann-Whitney U, a leave-one-case-out jackknife by brute force, the
Obuchowski-Rockette interval written out on its own) and the asks (copies, hosts, episodes, film readers, costs) by
its own route.

    python3 task260/generator/verify.py"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
from openpyxl import load_workbook
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def find(target, start):
    return os.path.join(target, next(f for f in sorted(os.listdir(target)) if f.startswith(start)))


def rows_of(path, sheet=None, first=None):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == first)
    return [dict(zip(rows[h], r)) for r in rows[h + 1:] if any(v is not None for v in r)]


def study(target, prefix, code):
    with open(find(target, prefix), encoding="utf-8") as fh:
        rd = list(csv.DictReader(fh))
    cases = rows_of(find(target, "reader_study_case_sets"), code, "Case")
    truth = {str(c["Case"]): c["Outcome"] == "Malignant" for c in cases}
    best = {}
    for r in rd:
        if "pom" in r:
            key = (r["user_id"], r["case_code"], r["arm"] == "AIDED")
            val, rev = float(r["pom"]), int(r["revision"])
        else:
            key = (r["reader_ref"], r["case_ref"], r["condition"] == "AI-assisted")
            val, rev = round(float(r["malignancy_probability"]) * 100), int(r["edit_count"]) + 1
        if key[1] not in truth:
            continue
        if key not in best or rev > best[key][0]:
            best[key] = (rev, val)
    readers = sorted({k[0] for k in best})
    order = sorted(truth)
    pos = [c for c in order if truth[c]]
    neg = [c for c in order if not truth[c]]
    X = {(u, a): (np.array([best[(u, c, a)][1] for c in pos]), np.array([best[(u, c, a)][1] for c in neg]))
         for u in readers for a in (False, True)}
    return readers, X


def auc(p, n):
    return stats.mannwhitneyu(p, n).statistic / (len(p) * len(n))


def or_interval(readers, X):
    J = len(readers)
    keys = [(u, a) for a in (False, True) for u in readers]
    th = np.array([auc(*X[k]) for k in keys]).reshape(2, J)
    m, n = len(X[keys[0]][0]), len(X[keys[0]][1])
    Kc = m + n
    jack = np.zeros((2 * J, Kc))
    for i, k in enumerate(keys):
        p, q = X[k]
        for a in range(m):
            jack[i, a] = auc(np.delete(p, a), q)
        for b in range(n):
            jack[i, m + b] = auc(p, np.delete(q, b))
    c = jack - jack.mean(1, keepdims=True)
    C = (Kc - 1) / Kc * (c @ c.T)
    v, c1, c2, c3 = [], [], [], []
    for i in range(2):
        for j in range(J):
            for k in range(2):
                for l in range(J):
                    x = C[i * J + j, k * J + l]
                    if i == k and j == l:
                        v.append(x)
                    elif i != k and j == l:
                        c1.append(x)
                    elif i == k and j != l:
                        c2.append(x)
                    else:
                        c3.append(x)
    cov2, cov3 = np.mean(c2), np.mean(c3)
    resid = th - th.mean(1, keepdims=True) - th.mean(0, keepdims=True) + th.mean()
    mstr = (resid ** 2).sum() / (J - 1)
    den = mstr + J * max(cov2 - cov3, 0)
    df = den ** 2 / (mstr ** 2 / (J - 1))
    d = th[1].mean() - th[0].mean()
    se = math.sqrt(2 / J * den)
    t = stats.t.ppf(0.975, df)
    return d, d - t * se, d + t * se, th


def asks(target):
    with open(find(target, "ris_mammography"), encoding="utf-8") as fh:
        ris = [r for r in csv.DictReader(fh) if r["status"] == "COMPLETED" and r["exam_code"] in ("MAMS", "MAMT")]
    for r in ris:
        r["t"] = dt.datetime.strptime(r["study_datetime"], "%Y-%m-%dT%H:%M:%SZ")
    ris = [r for r in ris if dt.date(2025, 10, 1) <= r["t"].date() <= dt.date(2026, 9, 30)]
    native = {}
    for r in ris:
        if r["accession"].startswith("MW"):
            native.setdefault((r["patient_ref"], r["location_code"], r["exam_code"], r["t"].date()), []).append(r["t"])
    keep = []
    for r in ris:
        if r["accession"].startswith("LR"):
            ts = native.get((r["patient_ref"], r["location_code"], r["exam_code"], r["t"].date()), [])
            if any((r["t"] - t0) in (dt.timedelta(0), dt.timedelta(hours=1)) for t0 in ts):
                continue
        keep.append(r)
    loc = json.load(open(find(target, "screening_locations"), encoding="utf-8"))
    site_of = {x["code"]: x.get("site") for x in loc["locations"]}
    code_of = {s["name"]: s["code"] for s in loc["sites"]}
    vis = rows_of(find(target, "mobile_unit_visits"), None, "Unit")
    per = {}
    for r in keep:
        s = site_of[r["location_code"]]
        if s is None:
            hit = [code_of[v["Host site"]] for v in vis if v["Unit"] == r["location_code"]
                   and v["From"].date() <= r["t"].date() <= v["To"].date()]
            s = hit[0]
        per[s] = per.get(s, 0) + 1
    # Lumidra's quote: one episode per woman and screening round, counted in the period of its routine study
    ep = len({r["patient_ref"] for r in keep if r["exam_code"] == "MAMS"})
    wf = rows_of(find(target, "film_reader_workforce"), None, "Employee number")
    day = dt.datetime(2027, 4, 1)
    regs = {str(w["Professional registration"]).split()[-1] for w in wf if w["Reads films"] == "Y"
            and w["Start date"] <= day and (w["End date"] is None or w["End date"] >= day)}
    return per, ep, len(regs)


def pounds(x):
    return int(Decimal(repr(round(x, 6))).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    fails, gains, ok = [], {}, {}
    for prefix, code, tool in (("readpoint_MBS-AI-01", "MBS-AI-01", "Lumidra Detect"),
                               ("readpoint_MBS-AI-02", "MBS-AI-02", "Ondrix Mammo"),
                               ("readpoint_MBS-AI-03", "MBS-AI-03", "Halvic Breast")):
        readers, X = study(target, prefix, code)
        d, lo, hi, th = or_interval(readers, X)
        gains[tool], ok[tool] = d, lo > 0
    qual = [k for k in gains if ok[k]]
    call = max(qual, key=lambda k: gains[k]) if qual else None
    per, ep, seats = asks(target)
    studies = sum(per.values())
    cost = {"Ondrix Mammo": pounds(max(1.62 * studies, 60000) + 14800),
            "Lumidra Detect": pounds(2.08 * ep + 340 * seats + 9500),
            "Halvic Breast": pounds(2450 * seats + 5900 * 4 + 12000)}
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    if call != "Halvic Breast" or fig["call"] != call:
        fails.append("call %s" % call)
    for k in gains:
        if "%.3f" % gains[k] != fig["gain_3dp"][k]:
            fails.append("%s gain %.4f" % (k, gains[k]))
        if ok[k] != fig["qualifies"][k]:
            fails.append("%s verdict" % k)
    if per != fig["studies_per_site"]:
        fails.append("sites %s against %s" % (per, fig["studies_per_site"]))
    if ep != fig["episodes"] or seats != fig["readers_in_post"]:
        fails.append("episodes %d seats %d" % (ep, seats))
    if cost != fig["cost"]:
        fails.append("costs %s against %s" % (cost, fig["cost"]))
    tl = {r["Tool"]: r for r in rows_of(os.path.join(golden, "ai_tool_evaluation_2027.xlsx"), "Tools", "Tool")}
    for k in gains:
        if abs(tl[k]["Gain"] - round(gains[k], 3)) > 1e-9 or tl[k]["Meets the protocol"] != ("Yes" if ok[k] else "No"):
            fails.append("golden xlsx %s" % k)
    if fails:
        raise SystemExit("verify FAILED: " + "; ".join(fails))
    print("verify: %s; gains %s; studies %s (%d), %d episodes, %d film readers; costs %s; the golden matches" % (
        call, {k: round(v, 3) for k, v in gains.items()}, per, studies, ep, seats, cost))


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
