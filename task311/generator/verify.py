"""Independent verifier for task311: reads only the shipped bundle (target/ or target.zip) and recomputes the call,
every share, the flip point, the published 2025 table, the cheap routes and the 2024 ask, then checks them against
generator/figures.json and submission.md. Its own code path: nothing from the generator's modules.

    python3 task311/generator/verify.py [path to target folder or target.zip]
"""
import csv
import datetime as dt
import io
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REG = {1: "North", 2: "Central Valley", 3: "Lakeshore", 4: "Southern Uplands", 5: "Metro"}
ABBR = {"NOR": 1, "CVL": 2, "LKS": 3, "SUP": 4, "MET": 5}
BOOST = 1200


class Bundle:
    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if path.endswith(".zip") else None

    def read(self, name):
        if self.zip:
            return self.zip.read("target/" + name)
        return open(os.path.join(self.path, name), "rb").read()

    def names(self):
        if self.zip:
            return sorted(n[len("target/"):] for n in self.zip.namelist() if n.startswith("target/"))
        return sorted(os.listdir(self.path))


def pdf_text(b):
    return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(b)).pages)


def load(bundle):
    nm = list(csv.DictReader(io.StringIO(bundle.read("northmark_phms_case_export_2023-2025.csv").decode("utf-8"))))
    os_ = json.loads(bundle.read("ostrander_phms2025_cases.json").decode("utf-8"))["cases"]
    wts = list(csv.DictReader(io.StringIO(bundle.read("phms_area_weights_2023-2025.csv").decode("utf-8"))))
    cw = openpyxl.load_workbook(io.BytesIO(bundle.read("moh_survey_area_concordance_2024.xlsx")), read_only=True)
    crow = [r for r in cw["Concordance"].iter_rows(values_only=True)]
    cross = [r for r in crow[4:] if r and r[0]]
    old2new = {str(r[0]): str(r[2]) for r in cross}
    new2old = {str(r[2]): str(r[0]) for r in cross}
    newreg = {str(r[2]): r[3] for r in cross}
    return nm, os_, wts, old2new, new2old, newreg


def interviews_2025(nm, os_, wts, new2old, newreg):
    """Per region (by name) the 2025 areas: weight, completes, usable answers. Complete = 1100/1120 or CI/CP."""
    w25 = {r["area_pre2024"]: r for r in wts if r["wave"] == "2025"}
    areas = {}
    for r in nm:
        if r["wave"] != "2025":
            continue
        a = r["area_at_assignment"]
        if r["disposition"] in ("1100", "1120"):
            areas.setdefault(a, []).append({"1": 1, "2": 0, "3": 0}.get(r["q_rx_cost"]))
    for r in os_:
        if r["final_disposition"] in ("CI", "CP"):
            ab, num = r["survey_area"].split("-")
            a = "%d%03d" % (ABBR[ab], int(num))
            areas.setdefault(a, []).append({"Y": 1, "N": 0, "NP": 0}.get(r["rx_cost"]))
    out = {}
    for a, ys in areas.items():
        wrow = w25[new2old[a]]
        m_all = len(ys)
        wt = float(wrow["design_weight"]) * int(wrow["occupied_dwellings"]) / m_all
        y = np.array([v for v in ys if v is not None], float)
        stratum = "S" if wrow["stratum"] == "CVS" else "C"
        out.setdefault(newreg[a], []).append(dict(code=a, w=wt, m_all=m_all, y=y, stratum=stratum))
    for k in out:
        out[k].sort(key=lambda d: d["code"])
    return out


def taylor(areas):
    W_ = sum(d["w"] * len(d["y"]) for d in areas)
    p = sum(d["w"] * d["y"].sum() for d in areas) / W_
    v = 0.0
    for h in sorted(set(d["stratum"] for d in areas)):
        z = np.array([d["w"] * (d["y"] - p).sum() / W_ for d in areas if d["stratum"] == h])
        if len(z) > 1:
            v += len(z) / (len(z) - 1) * ((z - z.mean()) ** 2).sum()
    return p, v


def components(areas):
    ys = [d["y"] for d in areas]
    m = np.array([len(y) for y in ys], float)
    n, k = m.sum(), len(ys)
    gm = np.concatenate(ys).mean()
    msb = (m * (np.array([y.mean() for y in ys]) - gm) ** 2).sum() / (k - 1)
    msw = sum(((y - y.mean()) ** 2).sum() for y in ys) / (n - k)
    m0 = (n - (m ** 2).sum() / n) / (k - 1)
    return max((msb - msw) / m0, 0.0), msw


def share(areas, sb, sw, add):
    a = np.array([d["w"] * d["m_all"] for d in areas])
    a = a / a.sum()
    m = np.array([len(d["y"]) for d in areas], float)
    v0 = (a ** 2 * (sb + sw / m)).sum()
    v1 = (a ** 2 * (sb + sw / (m + add))).sum()
    return 1 - math.sqrt(v1 / v0)


def kish_held(areas):
    """Kish's projection, the intraclass correlation from the design effect with the weighting effect divided out."""
    n = sum(len(d["y"]) for d in areas)
    k = len(areas)
    p, v = taylor(areas)
    deff = v / (p * (1 - p) / n)
    wts = np.concatenate([np.full(len(d["y"]), d["w"]) for d in areas])
    dw = n * (wts ** 2).sum() / wts.sum() ** 2
    mbar = n / k
    rho = max((deff / dw - 1) / (mbar - 1), 0.0)
    add = BOOST / k
    return 1 - math.sqrt(n / (n + BOOST) * (1 + (mbar + add - 1) * rho) / (1 + (mbar - 1) * rho)), deff, dw


def ask_2024(nm, wts, old2new, newreg):
    """The 2024 cases placed by the numbering in force when assigned. The switch is read from the data: the first
    assignment date of a number the pre-2024 series never had."""
    old_set = set(old2new)
    new_only = set(old2new.values()) - old_set
    switch = min(dt.date.fromisoformat(r["assigned"]) for r in nm if r["wave"] == "2024" and r["area_at_assignment"] in new_only)
    last_old_only = max(dt.date.fromisoformat(r["assigned"]) for r in nm if r["wave"] == "2024" and r["area_at_assignment"] in (old_set - set(old2new.values())))
    w24 = {r["area_pre2024"]: r for r in wts if r["wave"] == "2024"}
    new2old = {v: k for k, v in old2new.items()}
    areas = {}
    for r in nm:
        if r["wave"] != "2024" or r["disposition"] not in ("1100", "1120"):
            continue
        code = r["area_at_assignment"]
        new = old2new[code] if dt.date.fromisoformat(r["assigned"]) < switch else code
        areas.setdefault(new, []).append({"1": 1, "2": 0, "3": 0}.get(r["q_rx_cost"]))
    out = {}
    for a, ys in areas.items():
        wrow = w24[new2old[a]]
        wt = float(wrow["design_weight"]) * int(wrow["occupied_dwellings"]) / len(ys)
        y = np.array([v for v in ys if v is not None], float)
        out.setdefault(newreg[a], []).append(dict(code=a, w=wt, m_all=len(ys), y=y,
                                                  stratum="S" if wrow["stratum"] == "CVS" else "C"))
    res = {}
    for reg, ar in out.items():
        p, v = taylor(ar)
        res[reg] = dict(completes=sum(d["m_all"] for d in ar), est=100 * p, se=100 * math.sqrt(v))
    return res, switch, last_old_only


def main(path):
    b = Bundle(path)
    nm, os_, wts, old2new, new2old, newreg = load(b)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    fails = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    regions = interviews_2025(nm, os_, wts, new2old, newreg)
    ok(sorted(regions) == sorted(REG.values()), "regions %s" % sorted(regions))
    shares, kish = {}, {}
    report = pdf_text(b.read("phms_2025_technical_report.pdf"))
    ok("Taylor" in report and "Table 2" in report, "report text not readable")
    flat_report = re.sub(r"\s+", " ", report)
    icc_pub = {}
    for name, ar in regions.items():
        sb, sw = components(ar)
        add = BOOST / len(ar)
        ok(abs(add - round(add)) < 1e-9, "boost per area not whole in %s" % name)
        kish[name], deff, dw = kish_held(ar)
        p, v = taylor(ar)
        n = sum(len(d["y"]) for d in ar)
        line = "%s %s %.1f %.2f %.2f" % (name, "{:,}".format(n), 100 * p, 100 * math.sqrt(v), deff)
        ok(line in flat_report, "published row not reproduced: %s" % line)
        mt = re.search(re.escape(line) + r" (\d\.\d{3})", flat_report)
        ok(mt is not None, "published intraclass correlation not found for %s" % name)
        icc = float(mt.group(1)) if mt else round(sb / (sb + sw), 3)
        ok(abs(icc - round(sb / (sb + sw), 3)) < 1e-9, "published intraclass correlation %s %.3f vs %.4f" % (name, icc, sb / (sb + sw)))
        icc_pub[name] = icc
        shares[name] = share(ar, icc, 1 - icc, add)
        ok(round(100 * shares[name]) == round(100 * share(ar, sb, sw, add)), "the published and unrounded correlation part %s" % name)
        key = name.lower().replace(" ", "_")
        ok(int(round(100 * shares[name])) == figs["share_pct_" + key], "share %s %.4f vs %s" % (name, shares[name], figs["share_pct_" + key]))
        ok("   - %s: %d%%" % (name, int(round(100 * shares[name]))) in sub, "submission share line %s" % name)
    order = sorted(shares, key=lambda k: -shares[k])
    ok(order[0] == figs["call"] == "Central Valley", "call %s" % order[0])
    ok(order[1] == figs["runner_up"], "runner-up %s" % order[1])
    ok(shares[order[0]] / shares[order[1]] >= 1.25, "margin %.3f" % (shares[order[0]] / shares[order[1]]))
    ok(sorted(kish, key=lambda k: -kish[k])[0] == "Lakeshore", "the Kish route should file Lakeshore")
    n_by = {k: sum(len(d["y"]) for d in v) for k, v in regions.items()}
    count = {k: 1 - math.sqrt(n / (n + BOOST)) for k, n in n_by.items()}
    ok(sorted(count, key=lambda k: -count[k])[0] == "North", "count scaling should file the North")
    # flip: the runner-up's smallest whole boost per area that removes a larger share than the call's
    ar = regions[order[1]]
    ic = icc_pub[order[1]]
    d = next(d for d in range(1, 400) if share(ar, ic, 1 - ic, float(d)) > shares[order[0]])
    d2 = next(d for d in range(1, 400) if round(100 * share(ar, ic, 1 - ic, float(d))) > round(100 * shares[order[0]]))
    ok(d == d2, "flip unrounded %d against whole per cents %d" % (d, d2))
    ok(d == figs["flip_per_area"] and d * len(ar) == figs["flip_interviews"], "flip %d" % d)
    # the 2024 ask
    res24, switch, last_old = ask_2024(nm, wts, old2new, newreg)
    ok(switch == dt.date(2024, 4, 22), "switch %s" % switch)
    ok(last_old < switch, "an old-only number after the switch")
    for name, x in res24.items():
        key = name.lower().replace(" ", "_")
        ok(x["completes"] == figs["ask_completes_" + key], "2024 completes %s" % name)
        ok(round(x["est"], 1) == figs["ask_est_" + key], "2024 estimate %s %.3f" % (name, x["est"]))
        ok(round(x["se"], 2) == figs["ask_se_" + key], "2024 se %s %.4f" % (name, x["se"]))
        ok("%s: %s completed interviews, estimate %.1f%%, standard error %.2f points" % (name, "{:,}".format(x["completes"]), x["est"], x["se"]) in sub,
           "submission 2024 line %s" % name)
    # every format reads back, with a positive control
    terms = pdf_text(b.read("wexcombe_boost_terms_2027.pdf"))
    ok("the same number of additional" in re.sub(r"\s+", " ", terms), "terms text not readable")
    names = b.names()
    ok(len(names) >= 10 and len({n.rsplit(".", 1)[1] for n in names}) >= 3, "input gates")
    ok(max(len(nm), 0) >= 25000, "bulk file rows %d" % len(nm))
    for bad in ("readme", "dictionary", "manifest", "field_notes", "codebook"):
        ok(not any(bad in n.lower() for n in names), "describing file %s" % bad)
    if fails:
        print("VERIFY FAIL")
        for f_ in fails:
            print("  " + f_)
        return 1
    print("VERIFY OK  call %s, shares %s, flip %d per area, 2024 switch %s"
          % (order[0], ", ".join("%s %d%%" % (k, round(100 * shares[k])) for k in order), d, switch))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
