"""task170 independent verifier: reads only the bundle in a target folder, on its own code path (csv, openpyxl,
pyarrow and pypdf, no pandas, no calc.py), recomputes every graded figure and compares it with figures.json.

    python3 task170/generator/verify.py task170/target"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SC = ["RTN", "MWR", "KDG", "OYM", "NDR", "KBR", "WKL"]
SC_NAME = {"RTN": "Ruvari Town", "MWR": "Mwiri", "KDG": "Kendagi", "OYM": "Oyamo", "NDR": "Ndira", "KBR": "Kobura",
           "WKL": "Wakula"}
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def bin_of(label):
    s = label.strip().lower()
    if re.match(r"^\d{4}-\d{4}$", s):
        h = int(s[:2])
    elif re.match(r"^\d{2}:\d{2}-", s):
        h = int(s[:2])
    else:
        m = re.match(r"^(\d{1,2})(am|pm)-", s)
        h = int(m.group(1)) % 12 + (12 if m.group(2) == "pm" else 0)
    return (h - 18) % 24


def evening(s, morning=False):
    s = str(s).strip()
    m = re.match(r"^(\d{1,2})(:?)(\d{2})\s*([AaPp][Mm])?$", s)
    h, mi = int(m.group(1)), int(m.group(3))
    if m.group(4):
        h = h % 12 + (12 if m.group(4).upper() == "PM" else 0)
    t = h + mi / 60.0
    if morning:
        return t + 6
    return t - 18 if t >= 12 else t + 6


def entomology(target):
    n = defaultdict(int)
    mins = defaultdict(int)
    with open(os.path.join(target, "hlc_sentinel_2024_2026.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["an_ruvariensis"] == "":
                continue
            pos = "IN" if r["position"] in ("IN", "Indoor") else "OUT"
            b = bin_of(r["hour"])
            n[(pos, b)] += int(r["an_ruvariensis"])
            mins[(pos, b)] += int(r["minutes_collected"])
    bi = [n[("IN", h)] / mins[("IN", h)] for h in range(12)]
    bo = [n[("OUT", h)] / mins[("OUT", h)] for h in range(12)]
    return bi, bo


def behaviour(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "human_behaviour_survey_2025.xlsx"), read_only=True)
    people = []
    for ws in wb.worksheets:
        rows = ws.iter_rows(values_only=True)
        head = list(next(rows))
        i_in, i_bed, i_up = head.index("went_inside"), head.index("went_to_bed"), head.index("got_up")
        for r in rows:
            if r[0] is None:
                continue
            people.append((evening(r[i_in]), evening(r[i_bed]), evening(r[i_up], True)))
    ind, inb = [], []
    for h in range(12):
        t = h + 0.5
        ind.append(sum(1 for a, b, c in people if a <= t < c) / len(people))
        inb.append(sum(1 for a, b, c in people if b <= t < c) / len(people))
    return ind, inb, len(people)


def share(bi, bo, ind, inb):
    num = sum(bi[h] * inb[h] for h in range(12))
    den = sum(bi[h] * ind[h] + bo[h] * (1 - ind[h]) for h in range(12))
    return num / den


def trial(target):
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, "kinga5_final_report_2024.pdf")).pages)
    sites = ["Mabwe", "Kisiriri", "Kibondeni", "Chibowa", "Lukonde"]
    out = {}
    for s in sites:
        m = re.search(r"%s\s+([\d,]+)\s+([\d,]+\.\d)\s+([\d,]+)\s+([\d,]+\.\d)\s" % s, txt)
        out[s] = [float(x.replace(",", "")) for x in m.groups()]
    pooled = float(re.search(r"All sites\s+[\d,]+\s+[\d,.]+\s+[\d,]+\s+[\d,.]+\s+(\d+\.\d)", txt).group(1))

    def table(title, labels):
        seg = txt[txt.index(title):]
        vals = []
        for lab in labels:
            m = re.search(r"%s((?:\s+[\d.]+){5})" % re.escape(lab), seg)
            vals.append([float(x) for x in m.group(1).split()])
        return [[vals[h][i] for h in range(12)] for i in range(5)]

    hrs = ["%02d:00" % ((18 + h) % 24) for h in range(12)]
    halves = ["%02d:30" % ((18 + h) % 24) for h in range(12)]
    bi, bo = table("Table 2a", hrs), table("Table 2b", hrs)
    ind, inb = table("Table 3a", halves), table("Table 3b", halves)
    res = []
    for i, s in enumerate(sites):
        cc, pc, cn, pn = out[s]
        E = 1 - (cn / pn) / (cc / pc)
        f = share(bi[i], bo[i], [x / 100 for x in ind[i]], [x / 100 for x in inb[i]])
        var = (1 - E) ** 2 * (1 / cn + 1 / cc)
        res.append((E, f, var))
    q = sum(E * f / v for E, f, v in res) / sum(f * f / v for E, f, v in res)
    return q, pooled, ("96 to 98 per cent" in re.sub(r"\s+", " ", txt))


def baseline_and_use(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "obf_planning_baseline_2027.xlsx"), read_only=True)
    ws = wb.worksheets[0]
    base = {}
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] in SC:
            base[(r[0], r[2][:3])] = int(r[3])
    with zipfile.ZipFile(os.path.join(target, "lulanet_r_distribution_plan_2027.docx")) as z:
        x = z.read("word/document.xml").decode()
    text = re.sub(r"<[^>]+>", "|", x)
    use = {}
    for mname in ("April", "May", "June", "July", "August", "September", "October", "November", "December"):
        m = re.search(r"\|%s\|+(\d+)\|" % mname, text)
        use[mname[:3]] = int(m.group(1)) / 100
    return base, use


def nets(target):
    import pyarrow.parquet as pq
    t = pq.read_table(os.path.join(target, "nets_registration_2026.parquet")).to_pylist()
    seen, rows = set(), []
    for r in t:
        k = tuple(sorted((a, str(b)) for a, b in r.items()))
        if k in seen:
            continue
        seen.add(k)
        rows.append(r)
    mkey = {(r["sub_county"], r["ward"], r["dwelling_mark"], r["usual_members"], r["under_five"], r["sleeping_spaces"])
            for r in rows if r["round"] == "MAIN"}
    out = defaultdict(int)
    for r in rows:
        k = (r["sub_county"], r["ward"], r["dwelling_mark"], r["usual_members"], r["under_five"], r["sleeping_spaces"])
        if r["round"] == "MOPUP" and k in mkey:
            continue
        out[r["sub_county"]] += min(4, math.ceil(r["usual_members"] / 2))
    return dict(out)


def cases(target):
    fac = {}
    with open(os.path.join(target, "facility_list_2026.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            fac[r["mfl_code"]] = r
    by = {}
    with open(os.path.join(target, "khis_moh705_obf_2024_2026.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if not ("202601" <= r["period"] <= "202609"):
                continue
            k = (r["period"], r["mfl_code"], r["age_group"])
            if k not in by or r["last_updated"] > by[k]["last_updated"]:
                by[k] = r
    name = {v: k for k, v in SC_NAME.items()}
    out = defaultdict(int)
    for k, r in by.items():
        v = int(r["confirmed_obf"])
        if r["comment"].startswith("incl."):
            sat = [c for c, f in fac.items() if f["parent_mfl_code"] == r["mfl_code"]]
            for s in sat:
                v -= int(by[(r["period"], s, r["age_group"])]["confirmed_obf"])
        out[name[fac[r["mfl_code"]]["sub_county"]]] += v
    return dict(out)


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    bi, bo = entomology(target)
    ind, inb, n_people = behaviour(target)
    phi = share(bi, bo, ind, inb)
    q, pooled, use_note = trial(target)
    base, use = baseline_and_use(target)
    by = {s: sum(v * use[m] * q * phi for (sc, m), v in base.items() if sc == s) for s in SC}
    total = sum(by.values())
    ok("verify call", int(round(total / 1000.0)) * 1000 == F["call_cases_averted"], "%.1f" % total)
    btot = sum(base.values())
    ok("verify share", int(round(100 * total / btot)) == F["call_share_of_expected_pct"], "%.3f" % (100 * total / btot))
    ok("verify expected cases", btot == F["step_expected_cases"], str(btot))
    ok("verify per-bite protection", round(q, 2) == F["component_per_bite_protection"], "%.4f" % q)
    ok("verify in-bed share", round(phi, 2) == F["component_in_bed_share"], "%.4f" % phi)
    ok("verify trial pooled efficacy", abs(pooled - F["step_trial_pooled_efficacy_pct"]) < 1e-9, "%.1f" % pooled)
    ok("verify rival", int(round(sum(v * use[m] for (sc, m), v in base.items()) * pooled / 100 / 1000.0)) * 1000
       == F["rival_trial_efficacy_cases_averted"], "")
    for s in SC:
        ok("verify sub-county %s" % s, int(round(by[s] / 100.0)) * 100 == F["call_cases_averted_%s" % s], "%.1f" % by[s])
    nv = nets(target)
    for s in SC:
        ok("verify nets %s" % s, nv.get(s) == F["ask_nets_%s" % s], str(nv.get(s)))
    cv = cases(target)
    for s in SC:
        ok("verify reported cases %s" % s, cv.get(s) == F["ask_reported_cases_2026_%s" % s], str(cv.get(s)))
    ok("verify trial positive control", use_note, "")
    ok("verify survey read", n_people > 3000, str(n_people))
    print("\n%d FAIL" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
