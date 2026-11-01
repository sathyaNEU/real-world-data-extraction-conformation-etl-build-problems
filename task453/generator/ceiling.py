"""task453 ask layer against the careful solver's routes, on the cut pack.

    python3 task453/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The one ask of the
design note's ask sheet (Ask A) gives ten figures: the dwellings that responded to the survey in October to December
2026, region by region and in all, each dwelling counted once however many months it responded. Every route below
is a complete pipeline over the cut pack (the fieldwork log and the unit lookup for the ask; both collection systems'
exports, the region concordance, the release and the Act for the calls), scored figure by figure against
figures.json; a count is kept only when it is exact.

The cracker lands the call (each interview's effect on the redesigned questionnaire against the same interview on
the previous one, month and region held fixed, the six averaged: the trigger restated at 6.5, four regions), runs
the hygiene battery (exact duplicate rows, one row per reference and month, each reference built from its unit, group
and line, one region per unit, one label per outcome code, the log tied to Survey Operations' response rates) and
applies every filed rule (the fourth quarter's contact months, the fieldwork system's own Full response and Partial
response, each dwelling once, the unit's region), and takes the ask on its natural read: a dwelling is its
dwelling_ref. The mirror stops at the default path (the gap between the two questionnaires' rotation groups in July to
November 2025: 7.2 per cent, two regions) and takes the ask on the same natural read without the battery. The full
includer reads a dwelling as its reference with the month it entered (the contact month less its interview number
plus one) and has to give back figures.json exactly: the route code's control. The stops are the sheet's other
wrong paths, each scored as a route.

The pair is the ask sheet's formula: 38 recommendation and components (the trigger, the change and the designated
regions), 7 instruction following, 55 asks over the ten counts, a response off the call keeping r = 5 of the 38, and
2 for a chart criterion either response may keep. Printed beside it on the same routes: the pair with the chart's five
criteria and the CSV's two inside the 55 (each scored from the response's own change, since both follow the call
through the methodology note's section 4), and each pair again if the device is found."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V   # noqa: E402  (the bundle-only readers: both exports conformed, the release, the fit)

TASK = os.path.dirname(HERE)
ACT = "regional_employment_support_act_2021_extract.pdf"
RESP_BOOK = "lfs_response_rates_2025-2026.xlsx"
GOLDEN_CSV = os.path.join(TASK, "golden", "regional_unemployment_redesigned_basis_2024-2026.csv")
Q4 = ("2026-10", "2026-11", "2026-12")
RESPONDING = ("Full response", "Partial response")
OUT_OF_SCOPE = ("Vacant", "Derelict or demolished", "Not a private dwelling")
REC, INS, ASK, OFF, CHART = 38.0, 7.0, 55.0, 5.0, 2.0      # the ask sheet's planning weights, r and chart allowance
STOPS = {
    "interviews counted (each responding contact)": "interviews",
    "every dwelling counted, responding or not": "every dwelling",
    "eligible dwellings counted": "eligible",
    "full responses only": "full only",
}


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling453-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


def label(ym):
    return dt.date(int(ym[:4]), int(ym[5:7]), 1).strftime("%b-%Y")


def trigger_in_force(folder):
    """the Act's section 8, read from the extract"""
    from pypdf import PdfReader
    text = " ".join(" ".join((p.extract_text() or "").split()) for p in PdfReader(os.path.join(folder, ACT)).pages)
    m = re.search(r"The trigger rate is (\d+\.\d) per cent", text)
    if not m:
        raise SystemExit("the Act's section 8 could not be read from %s" % ACT)
    return float(m.group(1))


def restate(base, points):
    return round(base + round(points + 1e-9, 1), 1)


def arm_gap(cells):
    """the default path: in each of July to November 2025 the rotation groups on the redesigned questionnaire against
    those still on the previous one, the national rate of each, the five months averaged"""
    gaps = []
    for ym in ("2025-07", "2025-08", "2025-09", "2025-10", "2025-11"):
        u = defaultdict(float)
        l = defaultdict(float)
        for (m, _, _, sysno), (uu, ll) in cells.items():
            if m == ym:
                u[sysno] += uu
                l[sysno] += ll
        gaps.append(100.0 * u[1] / l[1] - 100.0 * u[0] / l[0])
    return float(np.mean(gaps))


def averages_2026(regs, rates):
    return np.mean([rates[label("2026-%02d" % m)] for m in range(1, 13)], axis=0)


def designate(regs, avg, trigger):
    return [regs[i] for i in range(len(regs)) if avg[i] >= trigger - 1e-9]


def conformance(cells, regs, rates, nat):
    """the cracker's conformance check: the cells both systems export, conformed, against the release's Table 1
    (national rate) and Table 2 (regional rates)"""
    by_mr, by_m = defaultdict(lambda: [0.0, 0.0]), defaultdict(lambda: [0.0, 0.0])
    for (m, r, _, _), (u, l) in cells.items():
        by_mr[(m, r)][0] += u
        by_mr[(m, r)][1] += l
        by_m[m][0] += u
        by_m[m][1] += l
    t2 = sum(abs(round(100.0 * u / l, 1) - rates[label(m)][regs.index(r)]) < 1e-9 for (m, r), (u, l) in by_mr.items())
    t1 = sum(abs(round(100.0 * u / l, 1) - nat[label(m)]) < 1e-9 for m, (u, l) in by_m.items())
    return t1, len(by_m), t2, len(by_mr)


def load_fieldwork(folder):
    import pyarrow.parquet as pq
    fw = pq.read_table(os.path.join(folder, V.FIELD)).to_pydict()     # the verifier's own read
    with open(os.path.join(folder, V.PSU), newline="") as fh:
        lk = list(csv.DictReader(fh))
    return fw, lk


def battery(folder, fw, lk):
    """the hygiene battery a careful analyst runs on the fieldwork log before counting: each line is (check, passed,
    detail)"""
    rows = list(zip(*[fw[c] for c in fw]))
    out = []
    out.append(("exact duplicate rows", len(rows) == len(set(rows)), "%d dropped" % (len(rows) - len(set(rows)))))
    keys = list(zip(fw["contact_month"], fw["dwelling_ref"]))
    out.append(("one row per reference and contact month", len(keys) == len(set(keys)), "%d rows" % len(keys)))
    built = sum(ref == "%s%s%02d" % (p, g, int(n)) for ref, p, g, n in
                zip(fw["dwelling_ref"], fw["psu"], fw["rotation_group"], fw["line"]))
    out.append(("each reference built from its unit, group and line", built == len(keys), "%d of %d" % (built, len(keys))))
    units = defaultdict(set)
    for r in lk:
        units[r["psu"]].add(r["region_2025"])
    out.append(("every unit in the lookup, one region each", set(fw["psu"]) <= set(units) and
                all(len(v) == 1 for v in units.values()), "%d units" % len(units)))
    pairs = set(zip(fw["outcome"], fw["outcome_desc"]))
    out.append(("one label per outcome code", len(pairs) == len({c for c, _ in pairs}) == len({d for _, d in pairs}),
                "%d codes" % len(pairs)))
    # counts that tie: Survey Operations' monthly response rates against the log, region by region
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(folder, RESP_BOOK), read_only=True, data_only=True).worksheets[0]
    head = next(ws.iter_rows(min_row=4, max_row=4, values_only=True))
    names = {r["region_name"]: r["region_2025"] for r in lk}
    book = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] in Q4:
            for h, v in zip(head[1:], row[1:]):
                if h in names:
                    book[(row[0], names[h])] = float(v)
    reg_of = {r["psu"]: r["region_2025"] for r in lk}
    el, rs = defaultdict(int), defaultdict(int)
    for m, p, d in zip(fw["contact_month"], fw["psu"], fw["outcome_desc"]):
        if m in Q4 and d not in OUT_OF_SCOPE:
            el[(m, reg_of[p])] += 1
            rs[(m, reg_of[p])] += d in RESPONDING
    tie = sum(abs(round(100.0 * rs[k] / el[k], 1) - book[k]) < 1e-9 for k in book)
    out.append(("the log ties to Survey Operations' response rates, October to December 2026", tie == len(book) == 27,
                "%d of %d region-months (a month holds one dwelling per reference, so the tie confirms no count)"
                % (tie, len(book))))
    return out


def ask_a(fw, lk, how):
    """the ten figures a route gives, by region code and in all"""
    reg_of = {r["psu"]: r["region_2025"] for r in lk}
    seen = set()
    for m, ref, k, d, p in zip(fw["contact_month"], fw["dwelling_ref"], fw["interview_no"], fw["outcome_desc"], fw["psu"]):
        if m not in Q4:
            continue
        entered = V.month_index(m) - int(k) + 1
        r = reg_of[p]
        if how == "reference":                     # the natural read: a dwelling is its dwelling_ref
            if d in RESPONDING:
                seen.add((ref, r))
        elif how == "entry":                       # the full includer: the reference with the month it entered
            if d in RESPONDING:
                seen.add((ref, entered, r))
        elif how == "interviews":
            if d in RESPONDING:
                seen.add((ref, m, r))
        elif how == "every dwelling":
            seen.add((ref, entered, r))
        elif how == "eligible":
            if d not in OUT_OF_SCOPE:
                seen.add((ref, entered, r))
        elif how == "full only":
            if d == "Full response":
                seen.add((ref, entered, r))
        else:
            raise ValueError(how)
    by = defaultdict(int)
    for key in seen:
        by[key[-1]] += 1
    by["all"] = len(seen)
    return dict(by)


def call_tied(change, trigger, golden, regs, rates, nat):
    """the chart's five criteria and the CSV's two (the design note's shape), for a response whose change is `change`
    and whose trigger is `trigger`, each built on the methodology note's section 4 from the response's own change:
    months before July 2025 the published rate plus the change, from July 2025 as published"""
    months = ["%d-%02d" % (y, m) for y in (2024, 2025, 2026) for m in range(1, 13)]
    d = round(change + 1e-9, 1)
    gd = golden["change_points"]
    with open(GOLDEN_CSV, newline="") as fh:
        gcsv = {(r["month"], r["region"]): float(r["redesigned_basis_rate"]) for r in csv.DictReader(fh)}
    rows_ok = sum(abs(round(rates[label(ym)][i] + (d if ym < "2025-07" else 0.0), 1) - gcsv[(ym, c)]) < 1e-9
                  for ym in months for i, c in enumerate(regs))
    series_ok = sum(abs(round(nat[label(ym)] + (d if ym < "2025-07" else 0.0), 1) -
                        round(nat[label(ym)] + (gd if ym < "2025-07" else 0.0), 1)) < 1e-9 for ym in months)
    crit = {
        "chart: the national rate as published, January 2024 to December 2026": True,
        "chart: the national rate on the redesigned basis": series_ok == len(months),
        "chart: July to November 2025 shaded as both questionnaires in the field": True,
        "chart: the old and the restated trigger at their values": trigger == golden["restated_trigger_pct"],
        "chart: a title stating the change": d == gd,
        "CSV: every month, January 2024 to December 2026": True,
        "CSV: every region": True,
    }
    return crit, rows_ok, len(gcsv), series_ok, len(months)


def pair_sheet(kc, km, n):
    c, s = REC + INS + ASK * kc / n, OFF + INS + ASK * km / n
    return c, s, (c + s) / 2.0 + CHART


def pair_wide(kc, km, n):
    c, s = REC + INS + ASK * kc / n, OFF + INS + ASK * km / n
    return c, s, (c + s) / 2.0


def fmt(by, names, gold=None):
    return "; ".join("%s %s%s" % (names.get(k, k), "{:,}".format(by.get(k, 0)),
                                  " (%s)" % "{:,}".format(gold[names.get(k, k)]) if gold else "")
                     for k in sorted(names) + ["all"])


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = figs["q4_responding_dwellings"]
    fw, lk = load_fieldwork(folder)
    names = {r["region_2025"]: r["region_name"] for r in lk}
    n = len(names) + 1

    # the calls
    base = trigger_in_force(folder)
    cells = V.read_cells(folder)
    regs, rates, nat = V.read_release(folder)
    t1, n1, t2, n2 = conformance(cells, regs, rates, nat)
    print("cracker's conformance: the cells reproduce Table 1's national rate in %d of %d months and Table 2's "
          "regional rates in %d of %d" % (t1, n1, t2, n2))
    avg = averages_2026(regs, rates)
    change = float(V.fit_effects(cells).mean())
    c_trig = restate(base, change)
    c_des = [names[c] for c in designate(regs, avg, c_trig)]
    gap = arm_gap(cells)
    m_trig = restate(base, gap)
    m_des = [names[c] for c in designate(regs, avg, m_trig)]
    on_call = c_trig == figs["restated_trigger_pct"] and round(change + 1e-9, 1) == figs["change_points"] and \
        c_des == figs["designated"]
    off_call = m_trig != figs["restated_trigger_pct"] and m_des != figs["designated"]
    print("cracker's call: change %+.4f (%+.1f), trigger %.1f per cent, designates %s (%s)" % (
        change, round(change + 1e-9, 1), c_trig, ", ".join(c_des), "lands the golden" if on_call else "MISSES"))
    print("mirror's call (the default path, the arm gap %+.2f): trigger %.1f per cent, designates %s (%s)" % (
        gap, m_trig, ", ".join(m_des), "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call and t1 == n1 and t2 == n2):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    # the ask
    print("\nthe cracker's hygiene battery on the fieldwork log:")
    bat = battery(folder, fw, lk)
    for check, passed, detail in bat:
        print("  %-4s %s (%s)" % ("ok" if passed else "FAIL", check, detail))
    if not all(p for _, p, _ in bat):
        print("the battery fails on the cut pack: the routes below are not the cracker's")
        return 1
    full = ask_a(fw, lk, "entry")
    kf = sum(full.get(k, 0) == gold[names.get(k, k)] for k in list(names) + ["all"])
    if kf != n:
        print("CONTROL FAILED: the full includer gives %d of %d, the route code does not reproduce figures.json" % (kf, n))
        return 1
    crk = ask_a(fw, lk, "reference")
    mir = ask_a(fw, lk, "reference")
    kept = lambda by: sum(by.get(k, 0) == gold[names.get(k, k)] for k in list(names) + ["all"])
    kc, km = kept(crk), kept(mir)
    print("\nAsk A, responding dwellings October to December 2026 (figures.json in brackets):")
    print("  cracker, a dwelling is its dwelling_ref: " + fmt(crk, names, gold))
    print("  mirror, the same natural read without the battery: " + fmt(mir, names))
    print("  full includer (control), a dwelling is its reference with its entry month: " + fmt(full, names))
    print("\nper route, figures kept of %d:" % n)
    print("  %-62s %d" % ("cracker (natural read, battery run, every filed rule)", kc))
    print("  %-62s %d" % ("mirror (natural read, off the call)", km))
    for nm, how in STOPS.items():
        by = ask_a(fw, lk, how)
        print("  %-62s %d  (all %s)" % ("stop: " + nm, kept(by), "{:,}".format(by["all"])))
    print("  %-62s %d  (control, figures.json reproduced)" % ("full includer", kf))

    # the deliverable criteria that follow the call
    cc, crows, nrows, cser, nser = call_tied(change, c_trig, figs, regs, rates, nat)
    mc, mrows, _, mser, _ = call_tied(gap, m_trig, figs, regs, rates, nat)
    kcc, kmc = sum(cc.values()), sum(mc.values())
    print("\nthe chart's and the CSV's criteria, each response from its own change (they follow the call):")
    for k in cc:
        print("  %-74s cracker %-4s mirror %s" % (k, "yes" if cc[k] else "no", "yes" if mc[k] else "no"))
    print("  CSV rows on the golden at one decimal: cracker %d of %d, mirror %d of %d; chart months on the redesigned "
          "basis: cracker %d of %d, mirror %d of %d" % (crows, nrows, mrows, nrows, cser, nser, mser, nser))

    # the pair
    c, s, p = pair_sheet(kc, km, n)
    print("\nthe sheet's formula (38, 7, 55 over the %d counts; r = 5; plus 2 for a chart criterion either response "
          "may keep): cracker %.1f, mirror %.1f, pair %.1f" % (n, c, s, p))
    print("  if the cracker finds the reused reference (keeps all %d): pair %.1f" % (n, pair_sheet(n, km, n)[2]))
    print("  if the mirror finds it: pair %.1f" % pair_sheet(kc, n, n)[2])
    w = n + len(cc)
    c2, s2, p2 = pair_wide(kc + kcc, km + kmc, w)
    print("with the chart's %d criteria and the CSV's %d inside the 55 (%d ask criteria): cracker keeps %d, mirror %d; "
          "cracker %.1f, mirror %.1f, pair %.1f" % (
              sum(1 for k in cc if k.startswith("chart")), sum(1 for k in cc if k.startswith("CSV")), w,
              kc + kcc, km + kmc, c2, s2, p2))
    print("  if the cracker also finds the reused reference: pair %.1f" % pair_wide(n + kcc, km + kmc, w)[2])
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight (%.1f with the chart and the CSV inside it)" % (
        100.0 * km / n, 100.0 * (km + kmc) / w))
    print("Pair ceiling: %.1f (the sheet's formula on the measured keeps)" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
