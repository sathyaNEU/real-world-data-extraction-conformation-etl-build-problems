"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task181/generator/ceiling.py

Rows: the cracker lands the call, runs the hygiene battery (dates parsed in each file's own order, exact
duplicates out, every sheet of the private hospital's log read and counted by the date admitted) and executes the
plan's definitions, but counts a hospital's patients by their hospital number, keeps the patients moved between
the two hospitals at both, keys the household survey's houses by the number on the form, and reads a laboratory
patient by the laboratory's reference. Where a careful solver could go either way (the laboratory's QC record),
the cracker takes the variant that keeps more. The mirror files the residence count and handles the asks the same
way, since they carry nothing from the call. The full includer resolves every device (a stress row, not the gate).
"""
import csv
import datetime as dt
import json
import os
import sys

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import build as B  # noqa: E402
from common import mw_of  # noqa: E402

HW = list(range(33, 41))
LW = list(range(35, 41))


def p(k):
    return os.path.join(TARGET, B.FILES[k])


def dmc_by_patient():
    rows = list(csv.DictReader(open(p("dmc"), encoding="utf-8")))
    first = {}
    for r in sorted(rows, key=lambda r: B._dt(r["ward_in"])):
        first.setdefault(r["hospital_no"], r)
    c = {w: 0 for w in HW}
    for r in first.values():
        y, w = mw_of(B._dt(r["ward_in"]))
        if y == 2027 and w in c:
            c[w] += 1
    return c


def dmc_by_segment():
    rows = list(csv.DictReader(open(p("dmc"), encoding="utf-8")))
    c = {w: 0 for w in HW}
    for r in rows:
        y, w = mw_of(B._dt(r["ward_in"]))
        if y == 2027 and w in c:
            c[w] += 1
    return c


def ddh_all_by_date():
    wb = load_workbook(p("ddh"), data_only=True)
    c = {w: 0 for w in HW}
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=5, values_only=True):
            if row[0]:
                y, w = mw_of(dt.datetime.strptime(row[4], "%m/%d/%Y").date())
                if y == 2027 and w in c:
                    c[w] += 1
    return c


def larval(key_purok):
    rows = list(csv.DictReader(open(p("larval"), encoding="utf-8")))
    houses = {}
    for r in rows:
        key = (r["barangay"], r["purok"], r["household_code"]) if key_purok else (r["barangay"], r["household_code"])
        pos = (r["larvae"] == "Y" or r["pupae"] == "Y") if r["team"] == "VCU" else int(r["containers_positive"] or 0) > 0
        houses[key] = houses.get(key, False) or pos
    out = {}
    for b in sorted(set(k[0] for k in houses)):
        hs = [v for k, v in houses.items() if k[0] == b]
        out[b] = round(100.0 * sum(hs) / len(hs), 1)
    return out


def lab(use_qc, identity):
    log = json.load(open(p("runlog"), encoding="utf-8"))
    rejected = {r["run_id"] for r in log["runs"] if r["qc"] == "Rejected"} if use_qc else set()
    rows = [r for r in csv.DictReader(open(p("lab"), encoding="utf-8")) if r["run_id"] not in rejected]
    first = {}
    for r in sorted(rows, key=lambda r: (dt.datetime.strptime(r["collected_on"], "%d/%m/%Y"), r["specimen_id"])):
        who = (r["patient_initials"], r["date_of_birth"], r["sex"]) if identity else r["patient_ref"]
        if r["result"] == "Positive" and who not in first:
            first[who] = r
    c = {(t, w): 0 for t in ("NS1", "IgM") for w in LW}
    for r in first.values():
        y, w = mw_of(dt.datetime.strptime(r["collected_on"], "%d/%m/%Y").date())
        t = "NS1" if r["test"].startswith("NS1") else "IgM"
        if y == 2027 and w in LW:
            c[(t, w)] += 1
    return c


def gold():
    g = B.golden_dmc(p("dmc")), B.golden_ddh(p("ddh"), p("dmc")), B.golden_larval(p("larval")), \
        B.golden_lab(p("lab"), p("runlog"))
    return g


def score(resp, g):
    dmc, ddh, larv, lb = resp
    gd, go, gl, gb = g
    kept = {"A": sum(dmc[w] == gd[w] for w in HW) + sum(ddh[w] == go[w] for w in HW),
            "B": sum(abs(larv[k] - gl[k]) < 0.05 for k in gl),
            "C": sum(lb[k] == gb[k] for k in gb)}
    n = {"A": 2 * len(HW), "B": len(gl), "C": len(gb)}
    return kept, n


def main():
    g = gold()
    variants = []
    for qc in (False, True):
        resp = (dmc_by_patient(), ddh_all_by_date(), larval(False), lab(qc, False))
        variants.append(score(resp, g))
    kept, n = max(variants, key=lambda kn: sum(kn[0].values()))
    seg = score((dmc_by_segment(), ddh_all_by_date(), larval(False), lab(False, False)), g)[0]
    full, _ = score((g[0], g[1], larval(True), lab(True, True)), g)
    N = sum(n.values())
    K = sum(kept.values())
    lc = K / N
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker per ask: A %d of %d, B %d of %d, C %d of %d" % (kept["A"], n["A"], kept["B"], n["B"], kept["C"], n["C"]))
    print("cracker (lands the call, battery, filed definitions; hospital numbers, both hospitals' moved patients, "
          "the form's house numbers, the laboratory's references): keeps %d of %d ask figures, response %.1f" % (K, N, c))
    print("mirror (the residence count, same ask handling): keeps %d of %d, response %.1f" % (K, N, s))
    print("segment counter (every ward segment an admission): A %d of %d" % (seg["A"], n["A"]))
    print("full includer (resolves every device, stress row): keeps %d of %d, response %.1f"
          % (sum(full.values()), N, 38 + 7 + 55 * sum(full.values()) / N))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc, kept, n


if __name__ == "__main__":
    main()
