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


def programme_dates(pr):
    """each programme point's dates in the programme (regulation 4.1)"""
    out = {}
    for i in range(len(pr)):
        v = pr.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            out[v] = (dt.date.fromisoformat(str(pr.iloc[i, 7])[:10]),
                      dt.date.fromisoformat(str(pr.iloc[i, 8])[:10]))
    return out


def operational_points(target):
    op = pd.read_excel(os.path.join(target, PK.FILES["programme"]), sheet_name="Operational network",
                       header=None, dtype=object)
    out = {}
    for i in range(len(op)):
        v = op.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            out[v] = str(op.iloc[i, 2])
    return out


def shared_codes(target, xw, rg):
    """Tirneevin numbers a point ARWA-<catchment>-<last two digits>, so an operational point can carry
    the code of a compliance point in its catchment; such a point has no row of its own in the
    crosswalk. Returns {(lab, client code): (compliance point, operational point)}."""
    catch = {r.water_body_code: r.catchment for r in rg.itertuples()}
    abbr = {}
    for r in xw.itertuples():
        if r.lab_code == "TAS" and r.water_body_code:
            abbr[catch[r.water_body_code]] = r.client_point_code.split("-")[1]
    known = set(xw["sample_point_code"])
    owner = {(r.lab_code, r.client_point_code): r.sample_point_code for r in xw.itertuples()
             if r.water_body_code}
    out = {}
    for code, c in operational_points(target).items():
        if code in known or c not in abbr:
            continue
        key = ("TAS", "ARWA-%s-%s" % (abbr[c], code[-2:]))
        if key in owner:
            out[key] = (owner[key], code)
    return out


def bookings(target, programme="NUT"):
    """the nutrient bottles as the laboratories booked them: one booking per laboratory, client
    code, collection date and time, with its determinands' governing results"""
    ex, xw, rg, ab, pr = load(target)
    d = conform(ex, xw)
    f = d[(d["sample_type"] == "FIELD") & (d["programme"] == programme)].copy()
    f = f.sort_values(["lab_sample_id", "determinand_code", "ver"])
    f = f.groupby(["lab_sample_id", "determinand_code"], as_index=False).tail(1)
    out = []
    for key, grp in f.groupby(["lab_code", "client_point_code", "sample_date", "sample_time"]):
        sig = tuple(sorted((r.determinand_code, r.result, r.qualifier) for r in grp.itertuples()))
        opo = grp[grp["determinand_code"] == "OPO4"]
        out.append({"lab": key[0], "code": key[1], "date": dt.date.fromisoformat(key[2]),
                    "time": key[3], "point": grp["point"].iloc[0], "wb": grp["wb_code"].iloc[0],
                    "received": grp["date_received"].iloc[0], "sig": sig,
                    "newest": max(int(x.split("/")[2]) for x in grp["lab_sample_id"]),
                    "opo4": (opo["result_status"].iloc[0] if len(opo) else "",
                             opo["qualifier"].iloc[0] if len(opo) else "")})
    return out, xw, rg, pr


def visits(target):
    """each compliance point's monthly visit: the collection date and time of its pesticide sample"""
    pk, _xw, _rg, _pr = bookings(target, programme="PEST")
    out = {}
    for b in pk:
        out.setdefault(b["point"], set()).add((b["date"], b["time"]))
    return out


def bottles(target):
    """one entry per nutrient bottle taken on a compliance point's visit: a booking under the point's
    code whose collection date and time are those of the point's pesticide sample that month. A
    second booking of one bottle dated from the round's pre-registration, a bottle booked under the
    point first and later under the operational point it was taken at, and the bottles of an
    operational point the laboratory's numbering gives the same code all fall on no visit of the
    point they are booked to"""
    bk, xw, rg, pr = bookings(target)
    vis = visits(target)
    return [b for b in bk if (b["date"], b["time"]) in vis.get(b["point"], ())], pr


def ask_orthophosphate(target):
    """the return's ortho-phosphate figures: for each water body, the compliance samples the year
    holds an approved ortho-phosphate result for, and how many of those results were below the
    reporting limit"""
    bt, pr = bottles(target)
    pts = programme_points(pr)
    dates = programme_dates(pr)
    _ex, _xw, rg, _ab, _pr = load(target)
    names = {r.water_body_code: r.water_body_name for r in rg.itertuples()}
    out = {}
    for b in bt:
        if b["point"] not in pts or not (W.YEAR_FROM <= b["date"] <= W.YEAR_TO):
            continue
        frm, to = dates[b["point"]]
        if not (frm <= b["date"] <= to) or b["opo4"][0] != "A":
            continue
        n, nd = out.get(names[b["wb"]], (0, 0))
        out[names[b["wb"]]] = (n + 1, nd + (1 if b["opo4"][1] == "<" else 0))
    return out


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
            "a1": ask_sampling(target), "w": ask_orthophosphate(target)}
