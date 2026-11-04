"""Everything the submission states, recomputed from the shipped bundle alone."""
import datetime as dt
import os

import pandas as pd

import est
import pack as PK
import world as W

CUTOFF = dt.date(2026, 1, 20)


def load(target):
    ex = pd.read_csv(os.path.join(target, PK.FILES["export"]), dtype=str, keep_default_na=False)
    xw = pd.read_csv(os.path.join(target, PK.FILES["crosswalk"]), dtype=str, keep_default_na=False)
    rg = pd.read_csv(os.path.join(target, PK.FILES["register"]), dtype=str, keep_default_na=False)
    ab = pd.read_csv(os.path.join(target, PK.FILES["abstractions"]), dtype=str, keep_default_na=False)
    pr = pd.read_excel(os.path.join(target, PK.FILES["programme"]), sheet_name="Programme 2025-26",
                       header=None, dtype=object)
    return ex, xw, rg, ab, pr


def programme_points(pr):
    """the sample points the monitoring programme lists for the reporting year"""
    out = set()
    for i in range(len(pr)):
        v = pr.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            out.add(v)
    return out


def conform(ex, xw):
    """the laboratory export put in order: the authority's point code, ug/l, the governing version"""
    key = {(r.lab_code, r.client_point_code): (r.sample_point_code, r.water_body_code)
           for r in xw.itertuples()}
    d = ex.copy()
    d["point"] = [key.get((a, b), ("", ""))[0] for a, b in zip(d["lab_code"], d["client_point_code"])]
    d["wb_code"] = [key.get((a, b), ("", ""))[1] for a, b in zip(d["lab_code"], d["client_point_code"])]
    d["sdate"] = pd.to_datetime(d["sample_date"]).dt.date
    d["val"] = pd.to_numeric(d["result"], errors="coerce")
    d["rl"] = pd.to_numeric(d["reporting_limit"], errors="coerce")
    scale = d["units"].map({"ng/l": 0.001}).fillna(1.0)
    # a censored row carries no value: it is held at its own limit
    d["val"] = d["val"].where(d["qualifier"] != "<", d["rl"])
    d["val_ugl"] = d["val"] * scale
    d["rl_ugl"] = d["rl"] * scale
    d["ver"] = pd.to_numeric(d["version"], errors="coerce")
    return d


def governing(d):
    """clause 7.5: the approved result, the latest version, and no result where withdrawn"""
    f = d[d["sample_type"] == "FIELD"].copy()
    f = f.sort_values(["lab_sample_id", "determinand_code", "ver"])
    f = f.groupby(["lab_sample_id", "determinand_code"], as_index=False).tail(1)
    return f[f["result_status"] == "A"].copy()


def mcpa_population(target):
    ex, xw, rg, ab, pr = load(target)
    d = conform(ex, xw)
    g = governing(d)
    m = g[(g["determinand_code"] == "MCPA")
          & (g["sdate"] >= W.YEAR_FROM) & (g["sdate"] <= W.YEAR_TO)].copy()
    pts = programme_points(pr)
    m = m[m["point"].isin(pts)]
    m["det"] = m["qualifier"] != "<"
    return m, rg


def assess(target):
    m, rg = mcpa_population(target)
    names = {r.water_body_code: r.water_body_name for r in rg.itertuples()}
    out = {}
    sens = {}
    for code, grp in m.groupby("wb_code"):
        tp = [(r.sdate.year, r.sdate.month, r.val_ugl, r.rl_ugl, r.det) for r in grp.itertuples()]
        sens[code] = [t for t, lab in zip(tp, grp["lab_code"]) if lab == "TAS"]
        out[code] = {"name": names[code], "n": len(tp),
                     "nd": sum(1 for t in tp if not t[4]), "tp": tp}
    for code, o in out.items():
        tp = o["tp"]
        vals = [t[2] for t in tp]
        lims = [t[3] for t in tp]
        det = [t[4] for t in tp]
        o["mle"] = est.mle_fill(vals, lims, det)
        o["km"] = est.km_mean(vals, lims, det)
        o["cond"] = est.cond_fill(tp, sens[code])
        o["fitted_dist"] = est.fitted_distribution_mean(vals, lims, det)
        for mode in ("half", "zero", "full", "drop"):
            o[mode] = est.substitute(tp, mode)
        o["verdict"] = "non-compliant" if o["mle"] > W.STANDARD else "compliant"
    return out


def ladder(target):
    a = assess(target)
    rungs = {}
    for k in ("half", "zero", "full", "drop", "mle", "km", "cond", "fitted_dist"):
        rungs[k] = sum(1 for o in a.values() if o[k] > W.STANDARD)
    # the authority's own points only, the quality reflex
    m, rg = mcpa_population(target)
    labA = 0
    for code, grp in m.groupby("wb_code"):
        la = grp[grp["lab_code"] == "TAS"]
        if len(la) >= 2:
            v = est.mle_fill(list(la["val_ugl"]), list(la["rl_ugl"]), list(la["det"]))
            labA += 1 if v > W.STANDARD else 0
    rungs["own_points"] = labA
    return rungs


def ask_sampling(target):
    """A1: per water body, the compliance samples the year holds and how many below the limit"""
    a = assess(target)
    return {o["name"]: (o["n"], o["nd"]) for o in a.values()}


def ask_nitrate(target):
    """A2: the abstraction points' nitrate, as mg/l NO3, once per sample"""
    ex, xw, rg, ab, pr = load(target)
    d = conform(ex, xw)
    g = governing(d)
    pts = set(ab["sample_point_code"])
    n = g[g["point"].isin(pts) & g["determinand_code"].isin(["NO3", "NO3N"])
          & (g["sdate"] >= W.YEAR_FROM) & (g["sdate"] <= W.YEAR_TO)].copy()
    n["as_no3"] = [v * (W.NO3_FACTOR if c == "NO3N" else 1.0)
                   for v, c in zip(n["val"], n["determinand_code"])]
    # one sample is one occasion: the two sections submit the same round under two client codes
    n = n.sort_values(["point", "sample_date", "sample_time", "client_point_code"])
    n = n.groupby(["point", "sample_date", "sample_time"], as_index=False).head(1)
    out = {}
    names = {r.sample_point_code: r.sample_point_name for r in ab.itertuples()}
    for code, grp in n.groupby("point"):
        out[names[code]] = (round(float(grp["as_no3"].max()), 1),
                            int((grp["as_no3"] >= W.NITRATE_TRIGGER).sum()))
    return out


def ask_quarter(target):
    """A3: the quarter's ortho-phosphate, the reports against the export"""
    ex, xw, rg, ab, pr = load(target)
    d = conform(ex, xw)
    q = d[(d["determinand_code"] == "OPO4") & (d["sample_type"] == "FIELD")
          & (d["sample_date"].str[:7].isin(["2025-10", "2025-11", "2025-12"]))].copy()
    issued = set()
    for r in q.itertuples():
        ap = r.date_approved
        if ap and dt.date.fromisoformat(ap) <= CUTOFF:
            issued.add(r.lab_sample_id)
    g = governing(d)
    held = set(g.loc[(g["determinand_code"] == "OPO4")
                     & (g["sample_date"].str[:7].isin(["2025-10", "2025-11", "2025-12"])),
                     "lab_sample_id"])
    return {"reports": len(issued), "export": len(held),
            "one_only": len(issued ^ held)}


def report_rows(rows):
    """the rows the quarterly reports list: issued by the cut-off, as issued"""
    q = [r for r in rows if r["determinand_code"] == "OPO4" and r["sample_type"] == "FIELD"
         and r["sample_date"][:7] in ("2025-10", "2025-11", "2025-12")]
    best = {}
    for r in q:
        ap = r["date_approved"]
        if not ap or dt.date.fromisoformat(ap) > CUTOFF:
            continue
        k = r["lab_sample_id"]
        if k not in best or int(r["version"]) > int(best[k]["version"]):
            best[k] = r
    return list(best.values())


def compute(target):
    a = assess(target)
    L = ladder(target)
    count = L["mle"]
    nc = sorted(o["name"] for o in a.values() if o["mle"] > W.STANDARD)
    return {"count": count, "non_compliant": nc, "assess": a, "rungs": L,
            "a1": ask_sampling(target), "a2": ask_nitrate(target), "a3": ask_quarter(target)}
