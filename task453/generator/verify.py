"""An independent check of the goldens from the shipped bundle alone: its own readers (csv, openpyxl), its own
regression and classical decomposition, its own workplace and employer counts. It imports nothing from the
generator but the file names."""
import collections
import csv
import json
import math
import os
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from world import FILES   # noqa: E402  (file names only)


def regions_of(target):
    wb = openpyxl.load_workbook(os.path.join(target, FILES["conc"]), read_only=True)
    out, names = {}, {}
    for r in list(wb["Municipalities"].iter_rows(values_only=True))[1:]:
        if r[0]:
            out[str(r[0])] = str(r[3])
            names[str(r[3])] = str(r[4])
    return out, names


def monthly(target):
    reg, names = regions_of(target)
    tot = collections.defaultdict(float)
    wb = openpyxl.load_workbook(os.path.join(target, FILES["wide"]), read_only=True)
    for year in ("2021", "2022", "2023"):
        started = False
        for r in wb[year].iter_rows(values_only=True):
            if r and r[0] == "Municipality code":
                started = True
                continue
            if started and r and r[0]:
                for k in range(12):
                    tot[("%s-%02d" % (year, k + 1), reg[str(r[0])])] += float(r[3 + k])
    revised = collections.defaultdict(float)
    rev_months = set()
    with open(os.path.join(target, FILES["rev"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            revised[(r["reference_month"], reg[r["municipality_code"]])] += float(r["payroll_jobs"])
            rev_months.add(r["reference_month"])
    with open(os.path.join(target, FILES["long"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["reference_month"] not in rev_months:
                tot[(r["reference_month"], reg[r["municipality_code"]])] += float(r["payroll_jobs"])
    tot.update(revised)
    months = sorted({m for m, _ in tot})
    codes = sorted({c for _, c in tot})
    Y = np.array([[tot[(m, c)] for c in codes] for m in months])
    return months, codes, names, Y


def shares(months):
    mo = np.array([int(m[5:]) for m in months])
    yr = np.array([int(m[:4]) for m in months])
    return mo, yr


def level_shift_regression(months, y):
    """log jobs on twelve month dummies, a trend with a knot each January from 2022 and a step from January 2026"""
    mo, yr = shares(months)
    n = len(months)
    t = np.arange(n, dtype=float)
    cols = [(mo == k).astype(float) for k in range(1, 13)] + [t, (np.array(months) >= "2026-01").astype(float)]
    for y0 in range(2022, 2028):
        k = months.index("%d-01" % y0) if "%d-01" % y0 in months else None
        if k is not None:
            cols.append(np.maximum(0.0, t - k))
    X = np.column_stack(cols)
    b = np.linalg.lstsq(X, np.log(y), rcond=None)[0]
    eff = b[:12] - b[:12].mean()
    return eff[mo - 1], b[13]


def classical_factors(months, y):
    mo, _ = shares(months)
    n = len(y)
    trend = np.full(n, np.nan)
    for i in range(6, n - 6):
        trend[i] = (0.5 * y[i - 6] + y[i - 5:i + 6].sum() + 0.5 * y[i + 6]) / 12.0
    ratio = y / trend
    pos = np.arange(n) % 12
    f = np.array([np.nanmean(ratio[pos == k]) for k in range(12)])
    f = f / f.mean()
    return f[pos]


def test(months, y, sa):
    q1 = [i for i, m in enumerate(months) if m in ("2027-01", "2027-02", "2027-03")]
    y26 = [i for i, m in enumerate(months) if m.startswith("2026")]
    return 100.0 * (np.mean(sa[q1]) / np.mean(y[y26]) - 1.0)


def workplaces(target):
    reg, _ = regions_of(target)
    jobs = collections.defaultdict(lambda: [0, 0])
    emp = collections.defaultdict(set)
    with open(os.path.join(target, FILES["work"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            region = reg[r["municipality_code"]]
            k = 0 if r["reference_month"] == "2026-03" else 1
            n = int(r["payroll_jobs"])
            jobs[(region, r["municipality_code"], r["street_address"])][k] += n
            if k == 1 and n > 0:
                emp[region].add(r["payroll_account"][:9])
    lost = collections.defaultdict(lambda: [0, 0])
    for (region, _, _), (a, b) in jobs.items():
        if b < a:
            lost[region][0 if b == 0 else 1] += a - b
    return lost, {k: len(v) for k, v in emp.items()}


def r10(v):
    return int(math.floor(v / 10.0 + 0.5)) * 10


def main(target, golden_dir):
    months, codes, names, Y = monthly(target)
    brk = months.index("2026-01")
    gold, default, restated = [], [], []
    for j, c in enumerate(codes):
        y = Y[:, j]
        sf, ls = level_shift_regression(months, y)
        if test(months, y, np.exp(np.log(y) - sf)) < -1:
            gold.append(c)
        if test(months, y, y / classical_factors(months, y)) < -1:
            default.append(c)
        yr = y * np.where(np.arange(len(y)) < brk, math.exp(ls), 1.0)
        if test(months, y, y / classical_factors(months, yr)) < -1:
            restated.append(c)
    lost, emp = workplaces(target)
    problems = []
    if gold != ["E01", "E03", "E09"]:
        problems.append("regression with a level shift: %s" % gold)
    if restated != gold:
        problems.append("classical on the restated history: %s" % restated)
    if default != ["E03", "E08", "E09", "E10"]:
        problems.append("classical across the change: %s" % default)
    with open(os.path.join(golden_dir, "regional_payroll_jobs_2027q1.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            c = r["economic_region_code"]
            if int(r["employers_with_payroll_jobs_2027_03"]) != emp[c]:
                problems.append("employers %s %s against %s" % (c, r["employers_with_payroll_jobs_2027_03"], emp[c]))
            if int(r["jobs_lost_workplaces_none_left_2027_03"]) != r10(lost[c][0]):
                problems.append("jobs lost, none, %s" % c)
            if int(r["jobs_lost_workplaces_kept_some_2027_03"]) != r10(lost[c][1]):
                problems.append("jobs lost, fewer, %s" % c)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    if figs["call"] != [names[c] for c in gold]:
        problems.append("figures.json call %s" % figs["call"])
    for c in codes:
        f = figs["regions"][names[c]]
        lo, hi = f["pct_range"]
        y = Y[:, codes.index(c)]
        sf, _ = level_shift_regression(months, y)
        v = test(months, y, np.exp(np.log(y) - sf))
        if not (lo - 1e-9 <= round(v, 1) <= hi + 1e-9):
            problems.append("%s regression %.2f outside its range %s" % (c, v, f["pct_range"]))
        if r10(np.mean(y[[i for i, m in enumerate(months) if m.startswith("2026")]])) != f["avg_2026"]:
            problems.append("%s 2026 average" % c)
    if problems:
        raise SystemExit("verify failed: " + "; ".join(problems))
    print("verify: from the bundle alone, the level-shift regression and the classical decomposition on the restated "
          "history designate %s; the classical decomposition across the change designates %s; every CSV figure and the "
          "2026 averages recompute" % (", ".join(names[c] for c in gold), ", ".join(names[c] for c in default)))


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"))
