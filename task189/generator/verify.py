"""Independent verification: reads only the shipped bundle and the submission's figures.

Nothing here imports the generator's golden, pack or simulation. Every number is rebuilt from the
files a solver gets, by its own code path, and compared with figures.json.
"""
import datetime as dt
import glob
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd
import pdfplumber
from scipy.optimize import minimize
from scipy.stats import norm

STANDARD = 0.05
Y0, Y1 = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
K = [0]


def ok(cond, msg):
    K[0] += 1
    if not cond:
        raise AssertionError("verify: " + msg)


def _mean_censored(v, l, dd):
    """a lognormal fit with every observation at its own censoring point, written from scratch"""
    v, l, dd = np.asarray(v, float), np.asarray(l, float), np.asarray(dd, bool)
    lv, ll = np.log(v[dd]), np.log(l[~dd])

    def nll(p):
        s = math.exp(p[1])
        a = float(np.sum(norm.logpdf((lv - p[0]) / s) - p[1] - lv))
        b = float(np.sum(norm.logcdf((ll - p[0]) / s))) if ll.size else 0.0
        return -(a + b)

    best, bv = None, float("inf")
    for m0 in (float(np.mean(lv)) - 1, float(np.mean(lv)), float(np.mean(lv)) + 1):
        for s0 in (math.log(0.5), math.log(1.0), math.log(1.6)):
            r = minimize(nll, [m0, s0], method="Nelder-Mead",
                         options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 6000})
            if r.fun < bv:
                bv, best = float(r.fun), r.x
    mu, s = float(best[0]), math.exp(float(best[1]))
    tot = float(np.sum(v[dd]))
    for c in l[~dd]:
        z = (math.log(c) - mu) / s
        p = float(norm.cdf(z))
        tot += (c / 2) if p <= 1e-12 else math.exp(mu + s * s / 2) * float(norm.cdf(z - s)) / p
    return tot / v.size


def run(target, figures):
    fig = json.load(open(figures, encoding="utf-8"))
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "fewer than ten files")
    ok(len(set(os.path.splitext(f)[1] for f in files)) >= 3, "fewer than three formats")

    ex = pd.read_csv(os.path.join(target, "lims_results_export_2025_2026.csv"), dtype=str,
                     keep_default_na=False)
    ok(len(ex) >= 25000, "the export holds %d rows" % len(ex))
    xw = pd.read_csv(os.path.join(target, "monitoring_point_crosswalk.csv"), dtype=str,
                     keep_default_na=False)
    rg = pd.read_csv(os.path.join(target, "water_body_register.csv"), dtype=str,
                     keep_default_na=False)
    ab = pd.read_csv(os.path.join(target, "abstraction_point_register.csv"), dtype=str,
                     keep_default_na=False)


    pr = pd.read_excel(os.path.join(target, "monitoring_programme_2025_26.xlsx"),
                       sheet_name="Programme 2025-26", header=None, dtype=object)
    prog_points, prog_rounds = set(), {}
    for i in range(len(pr)):
        v = pr.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            prog_points.add(v)
            prog_rounds[v] = int(pr.iloc[i, 4])
    ok(len(prog_points) == 37, "the programme lists %d points" % len(prog_points))

    key = {(r.lab_code, r.client_point_code): (r.sample_point_code, r.water_body_code)
           for r in xw.itertuples()}
    ex["point"] = [key.get((a, b), ("", ""))[0] for a, b in zip(ex["lab_code"],
                                                               ex["client_point_code"])]
    ex["wb"] = [key.get((a, b), ("", ""))[1] for a, b in zip(ex["lab_code"], ex["client_point_code"])]
    ex["d"] = pd.to_datetime(ex["sample_date"]).dt.date
    ex["num"] = pd.to_numeric(ex["result"], errors="coerce")
    ex["lim"] = pd.to_numeric(ex["reporting_limit"], errors="coerce")
    sc = ex["units"].map({"ng/l": 0.001}).fillna(1.0)
    ex["num"] = ex["num"].where(ex["qualifier"] != "<", ex["lim"])
    ex["ug"] = ex["num"] * sc
    ex["limug"] = ex["lim"] * sc
    ex["v"] = pd.to_numeric(ex["version"], errors="coerce")

    fieldrows = ex[ex["sample_type"] == "FIELD"].sort_values(["lab_sample_id", "determinand_code",
                                                             "v"])
    gov = fieldrows.groupby(["lab_sample_id", "determinand_code"], as_index=False).tail(1)
    gov = gov[gov["result_status"] == "A"]

    # ---- the call ------------------------------------------------------------------------------
    m = gov[(gov["determinand_code"] == "MCPA") & gov["point"].isin(prog_points)
            & (gov["d"] >= Y0) & (gov["d"] <= Y1)].copy()
    m["det"] = m["qualifier"] != "<"
    ok(len(m) == fig["compliance_samples_total"], "the population is %d rows" % len(m))
    names = {r.water_body_code: r.water_body_name for r in rg.itertuples()}
    verdicts, per = {}, {}
    for code, grp in m.groupby("wb"):
        v = _mean_censored(list(grp["ug"]), list(grp["limug"]), list(grp["det"]))
        verdicts[names[code]] = v > STANDARD
        per[names[code]] = (len(grp), int((~grp["det"]).sum()))
    ok(sum(verdicts.values()) == fig["call"], "the count is %d" % sum(verdicts.values()))
    ok(sorted(n for n, f in verdicts.items() if f) == fig["non_compliant"],
       "the non-compliant set is %s" % sorted(n for n, f in verdicts.items() if f))
    ok(len(verdicts) == fig["water_bodies_assessed"], "assessed %d water bodies" % len(verdicts))

    # the rungs, rebuilt here
    def sub(grp, mode):
        t, n = 0.0, 0
        for r in grp.itertuples():
            n += 1
            if r.det:
                t += r.ug
            elif mode == "half":
                t += r.limug / 2
            elif mode == "full":
                t += r.limug
            elif mode == "drop":
                n -= 1
        return t / n if n else 0.0

    for mode, want in (("half", fig["rungs"]["half"]), ("zero", fig["rungs"]["zero"]),
                       ("full", fig["rungs"]["full"]), ("drop", fig["rungs"]["drop"])):
        c = sum(1 for code, grp in m.groupby("wb") if sub(grp, mode) > STANDARD)
        ok(c == want, "the %s rung is %d, figures say %d" % (mode, c, want))

    # ---- A1 ------------------------------------------------------------------------------------
    for name, (n, nd) in per.items():
        want = fig["a1_sampling"][name]
        ok(n == want["samples"] and nd == want["below_limit"],
           "A1 %s: %d/%d against %s" % (name, n, nd, want))
    ok(sum(v["below_limit"] for v in fig["a1_sampling"].values()) == fig["below_limit_total"],
       "A1 below-limit total")

    # ---- the ortho-phosphate figures, rebuilt bottle by bottle ----------------------------------
    nut = ex[(ex["sample_type"] == "FIELD") & (ex["programme"] == "NUT")].sort_values(
        ["lab_sample_id", "determinand_code", "v"])
    nut = nut.groupby(["lab_sample_id", "determinand_code"], as_index=False).tail(1)
    bks = []
    for key, grp in nut.groupby(["lab_code", "client_point_code", "sample_date", "sample_time"]):
        o = grp[grp["determinand_code"] == "OPO4"]
        bks.append(dict(lab=key[0], code=key[1], d=dt.date.fromisoformat(key[2]), t=key[3],
                        pt=grp["point"].iloc[0], wb=grp["wb"].iloc[0], rec=grp["date_received"].iloc[0],
                        sig=frozenset(zip(grp["determinand_code"], grp["result"], grp["qualifier"])),
                        new=max(int(x.split("/")[2]) for x in grp["lab_sample_id"]),
                        st=o["result_status"].iloc[0] if len(o) else "", q=o["qualifier"].iloc[0] if len(o) else ""))
    out = set()
    # the same analysis on two bookings at one point, a few days apart
    grp1 = {}
    for i, b in enumerate(bks):
        grp1.setdefault((b["lab"], b["pt"], b["rec"], b["sig"]), []).append(i)
    for idx in grp1.values():
        idx.sort(key=lambda i: bks[i]["d"])
        out.update(a for a, c in zip(idx, idx[1:]) if 1 <= (bks[c]["d"] - bks[a]["d"]).days <= 3)
    # one bottle on two points: kept at the point of its newer booking
    grp2 = {}
    for i, b in enumerate(bks):
        grp2.setdefault((b["lab"], b["d"], b["t"], b["rec"], b["sig"]), []).append(i)
    for idx in grp2.values():
        if len({bks[i]["pt"] for i in idx}) > 1:
            top = max(idx, key=lambda i: bks[i]["new"])
            out.update(i for i in idx if i != top)
    # a Tirneevin code ARWA-<catchment>-<last two digits> that an operational point with no crosswalk row
    # of its own also carries
    op = pd.read_excel(os.path.join(target, "monitoring_programme_2025_26.xlsx"), sheet_name="Operational network",
                       header=None, dtype=object)
    catch = {r.water_body_code: r.catchment for r in rg.itertuples()}
    ab2 = {catch[r.water_body_code]: r.client_point_code.split("-")[1] for r in xw.itertuples()
           if r.lab_code == "TAS" and r.water_body_code}
    owner = {r.client_point_code: r.sample_point_code for r in xw.itertuples()
             if r.lab_code == "TAS" and r.water_body_code}
    listed = set(xw["sample_point_code"])
    labs = {}
    for b in bks:
        labs.setdefault(b["pt"], set()).add(b["lab"])
    for i in range(len(op)):
        c = op.iloc[i, 0]
        if not (isinstance(c, str) and c.startswith("ARW-")) or c in listed or str(op.iloc[i, 2]) not in ab2:
            continue
        code = "ARWA-%s-%s" % (ab2[str(op.iloc[i, 2])], c[-2:])
        if code not in owner:
            continue
        mine = [j for j, b in enumerate(bks) if b["lab"] == "TAS" and b["code"] == code and j not in out]
        if labs[owner[code]] - {"TAS"}:
            out.update(mine)
        else:
            per = {}
            for j in mine:
                per.setdefault((bks[j]["d"].year, bks[j]["d"].month), []).append(j)
            for js in per.values():
                out.update(sorted(js)[1:])
    frm = {}
    for i in range(len(pr)):
        v = pr.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            frm[v] = (dt.date.fromisoformat(str(pr.iloc[i, 7])[:10]), dt.date.fromisoformat(str(pr.iloc[i, 8])[:10]))
    opo = {}
    for j, b in enumerate(bks):
        if j in out or b["pt"] not in prog_points or b["st"] != "A":
            continue
        if not (Y0 <= b["d"] <= Y1 and frm[b["pt"]][0] <= b["d"] <= frm[b["pt"]][1]):
            continue
        n, nd = opo.get(names[b["wb"]], (0, 0))
        opo[names[b["wb"]]] = (n + 1, nd + (b["q"] == "<"))
    for name, (n, nd) in opo.items():
        want = fig["orthophosphate"][name]
        ok(n == want["samples"] and nd == want["below_limit"],
           "ortho-phosphate %s: %d/%d against %s" % (name, n, nd, want))
    ok(len(opo) == len(fig["orthophosphate"]), "ortho-phosphate covers %d water bodies" % len(opo))
    # the same figures a second way: a compliance point's nutrient bottle is the one filled on the visit
    # that took its pesticide sample, so it carries that sample's collection date and time
    pest = ex[(ex["sample_type"] == "FIELD") & (ex["programme"] == "PEST")]
    vset = set(zip(pest["point"], pest["sample_date"], pest["sample_time"]))
    opo_v = {}
    for b in bks:
        if (b["pt"], b["d"].isoformat(), b["t"]) not in vset or b["pt"] not in prog_points or b["st"] != "A":
            continue
        n, nd = opo_v.get(names[b["wb"]], (0, 0))
        opo_v[names[b["wb"]]] = (n + 1, nd + (b["q"] == "<"))
    ok(opo_v == opo, "the visit reading and the bottle rules disagree: %s against %s" % (opo_v, opo))
    ok(not (ex["result_status"].isin(["A", "P"]) == False).any(), "a result status other than A or P")

    # ---- the governing documents say nothing about the decisive step ---------------------------
    blob = ""
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            with pdfplumber.open(p) as pdf:
                blob += " " + " ".join(pg.extract_text() or "" for pg in pdf.pages)
        elif f.endswith((".csv", ".json")):
            blob += " " + open(p, encoding="utf-8", errors="ignore").read()
    low = re.sub(r"\s+", " ", blob).lower()
    for banned in ("half the reporting limit", "substitut", "censor", "kaplan", "nondetect",
                   "maximum likelihood", "non-detect"):
        ok(banned not in low, "a shipped file says '%s'" % banned)
    ok("each sample weighted equally" in low, "clause 7.2 does not file the weighting")
    ok("mcpa 0.05 ug/l annual average" in low, "Schedule 2 does not carry the standard")

    # ---- the deliverables agree with figures.json ----------------------------------------------
    task = os.path.dirname(os.path.abspath(target.rstrip("/")))
    xl = os.path.join(task, "golden", "annual_compliance_return_2025_26.xlsx")
    if os.path.exists(xl):
        rows = pd.read_excel(xl, sheet_name="Return 2025-26", header=5, dtype=object)
        rows = rows[rows["Water body"].notna()]
        nc = [r for r in rows.itertuples() if str(r._3) == "non-compliant"]
        ok(len(nc) == fig["call"], "the return workbook states %d non-compliant" % len(nc))
        for r in rows.itertuples():
            nm = str(r._2)
            want = fig["orthophosphate"].get(nm)
            if want:
                ok(int(r._4) == want["samples"] and int(r._5) == want["below_limit"],
                   "the return workbook disagrees at %s" % nm)
                ok((str(r._3) == "non-compliant") == (nm in fig["non_compliant"]),
                   "the return workbook's MCPA assessment disagrees at %s" % nm)
    return K[0]


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    figs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    print("independent checks passed:", run(tgt, figs))
