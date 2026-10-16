"""Independent verifier for task233: reads only the shipped bundle and figures.json, recomputes every owed figure with
its own code (no import from the generator), and fails on any difference.

    python3 task233/generator/verify.py [target_dir] [figures.json]
"""
import csv
import json
import math
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def xlsx_sheet(path, sheet):
    """read one sheet of an xlsx as a list of row lists, without openpyxl"""
    z = zipfile.ZipFile(path)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            strings.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = {r.get("Id"): r.get("Target") for r in rels}
    target = None
    for sh in wb.find("m:sheets", ns):
        if sh.get("name") == sheet:
            target = rid[sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")]
    data = ET.fromstring(z.read("xl/" + target.lstrip("/").replace("xl/", "")))
    out = []
    for r in data.find("m:sheetData", ns):
        vals = []
        for c in r:
            v = c.find("m:v", ns); t = c.get("t")
            if v is None:
                isv = c.find("m:is", ns)
                vals.append("".join(x.text or "" for x in isv.iter("{%s}t" % ns["m"])) if isv is not None else "")
            elif t == "s":
                vals.append(strings[int(v.text)])
            else:
                vals.append(v.text)
        out.append(vals)
    return out


def logit(p):
    p = min(max(p, 1e-9), 1 - 1e-9)
    return math.log(p / (1 - p))


def expit(x):
    return 1 / (1 + math.exp(-x))


def main(target=None, figpath=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    figpath = figpath or os.path.join(HERE, "figures.json")
    fig = json.load(open(figpath))
    j = lambda n: os.path.join(target, n)
    reg = xlsx_sheet(j("school_register.xlsx"), "Schools")
    hdr = reg[0]; reg = [dict(zip(hdr, r)) for r in reg[1:]]
    d26 = {r["school_code"]: r["district_2026"] for r in reg}
    f26 = rows(j("leaver_destinations_frame_2026.csv"))
    f25 = {r["leaver_ref"]: r for r in rows(j("leaver_destinations_final_2025.csv"))}
    fu = rows(j("nonresponse_followup_2025_outcomes.csv"))
    xw = {r["case_no"]: "L" + r["leaver_ref"] for r in rows(j("followup_case_crosswalk_2025.csv"))}
    field = {"F01": "HE", "F02": "FE", "F03": "APP", "F04": "APP", "F05": "EMP", "F06": "NEET", "F07": "NEET"}

    # the comparable follow-up cases: resolved, still a nonrespondent in the final file, one outcome per case
    seen, comp = set(), []
    for r in fu:
        if r["outcome_code"] == "F99" or r["case_no"] in seen:
            continue
        seen.add(r["case_no"])
        lv = f25[xw[r["case_no"]]]
        if lv["return_form"] == "":
            comp.append((lv, field[r["outcome_code"]]))
    assert len(comp) == fig["components"]["comparable_cases"], ("cases", len(comp))
    delta = {}
    for s, dest in (("neet", "NEET"), ("he", "HE")):
        p = [float(lv["alloc_" + s]) for lv, _ in comp]; a = sum(f == dest for _, f in comp)
        li = [logit(x) for x in p]
        delta[s] = brentq(lambda x: sum(expit(v + x) for v in li) - a, -10, 10)
        assert round(math.exp(delta[s]), 2) == fig["components"]["odds_ratio_" + s], ("odds ratio", s, math.exp(delta[s]))
    import numpy as np
    import statsmodels.api as sm
    for s, dest in (("neet", "NEET"), ("he", "HE")):
        x = np.array([logit(float(lv["alloc_" + s])) for lv, _ in comp]); y = np.array([f == dest for _, f in comp], float)
        slope = sm.GLM(y, sm.add_constant(x), family=sm.families.Binomial()).fit().params[1]
        assert round(slope, 2) == fig["components"]["calibration_slope_" + s], ("slope", s, slope)
    gap = {}
    for s, dest in (("neet", "NEET"), ("he", "HE")):
        gap[s] = (sum(f == dest for _, f in comp) - sum(float(lv["alloc_" + s]) for lv, _ in comp)) / len(comp)
        assert round(gap[s] * 100, 1) == fig["rival"]["points_gap_" + s]

    # shifts and flags
    by = {}
    for r in f26:
        by.setdefault(d26[r["school_code"]], []).append(r)
    assert sum(len(v) for v in by.values()) == fig["components"]["leavers_2026"]
    assert sum(r["return_form"] == "" for r in f26) == fig["components"]["nonrespondents_2026"]
    fl = lambda x: "Suppressed" if abs(x) >= 3.0 else ("Caution" if abs(x) >= 1.0 else "Standard")
    wrong = 0
    for d, g in by.items():
        n = len(g); nr = [r for r in g if r["return_form"] == ""]
        for s in ("neet", "he"):
            sh = sum(expit(logit(float(r["alloc_" + s])) + delta[s]) - float(r["alloc_" + s]) for r in nr) / n * 100
            want = fig["flags"]["%s %s" % (d, s)]
            assert fl(sh) == want["flag"] and round(sh, 2) == want["shift"], ("flag", d, s, sh, want)
            wrong += fl(len(nr) * gap[s] / n * 100) != want["flag"]
    assert wrong == fig["rival"]["default_wrong"], ("default wrong", wrong)

    # published rates: form codes by the edition of the build, plus allocations, over every leaver
    cur = {(r["form"], r["activity_code"]): r["destination"] for r in rows(j("activity_codes.csv"))}
    old = {}
    for r in f25.values():
        if r["return_form"] == "LDS-2":
            old.setdefault(r["activity_code"], set()).add(r["destination"])
    assert all(len(v) == 1 for v in old.values())
    old = {k: next(iter(v)) for k, v in old.items()}

    def dest(r):
        if r["return_form"] == "LDS-2" and r["form_build"].startswith("7."):
            return old[r["activity_code"]]
        return cur[(r["return_form"], r["activity_code"])]

    def rate(g, s):
        dd = {"neet": "NEET", "he": "HE"}[s]
        return (sum(dest(r) == dd for r in g if r["return_form"]) + sum(float(r["alloc_" + s]) for r in g if not r["return_form"])) / len(g) * 100

    for d, g in by.items():
        for s in ("neet", "he"):
            assert round(rate(g, s), 1) == fig["flags"]["%s %s" % (d, s)]["rate"], ("rate", d, s)
    pts = {r["leaver_ref"]: int(r["exam_points"]) for r in rows(j("state_exam_points_2026.csv"))}
    band = lambda x: "AB1" if x >= 480 else ("AB2" if x >= 360 else ("AB3" if x >= 240 else "AB4"))
    bb = {}
    for r in f26:
        bb.setdefault(band(pts[r["leaver_ref"]]), []).append(r)
    for b, g in bb.items():
        want = fig["bands"][b]
        assert len(g) == want["leavers"] and round(rate(g, "neet"), 1) == want["neet"] and round(rate(g, "he"), 1) == want["he"], ("band", b)
    print("verify: %d flags, %d rates, %d band figures recomputed from the bundle" % (len(fig["flags"]), 2 * len(by), 3 * len(bb)))


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
