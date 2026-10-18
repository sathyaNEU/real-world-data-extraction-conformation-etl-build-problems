"""task242 estimators on the cut pack: the misclassification flag on each zone's published dengue infection share (the
golden route and every rung of the ladder, with the implementation variants the closure asserts), each zone's Breteau
index for the November round and each zone's household response rate (golden and the device paths)."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

TOL_HIGH, TOL_LOW = 1.5, 2.0 / 3.0
ZONES = ["Kadalur", "Thenkarai", "Puthanpalli", "Melmangalam", "Vadakkupatti", "Kizhakkoor", "Velliyanur",
         "Chinnakulam", "Periyamalai", "Kottaivayal", "Sengalur", "Aranmanai"]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
YEAR0 = pd.Timestamp("2027-01-01")


def load(target, F):
    rd = lambda k, **kw: pd.read_csv(os.path.join(target, F[k]), **kw)
    D = {}
    D["cases"] = rd("cases", dtype=str)
    D["results"] = rd("results", dtype={"household_id": str})
    D["panel"] = rd("panel", dtype=str)
    D["sample"] = rd("sample", dtype=str)
    D["visits"] = rd("visits", dtype={"household_id": str})
    D["lab"] = rd("lab", dtype=str)
    D["insp"] = rd("insp", dtype={"premise_id": str})
    D["wards"] = rd("wards", dtype={"former_ward_nos": str})
    return D


# ------------------------------------------------------------------ the case line list
def zone_of(text):
    """the official zone a reporting unit's spelling stands for, or None for a non-resident"""
    t = re.sub(r"[^a-z ]", "", str(text).lower()).replace(" zone", "").strip()
    if t.startswith("nonresident") or t.startswith("non resident"):
        return None
    m = re.fullmatch(r"zone ([ivx]+)", t)
    if m:
        return ZONES[ROMAN.index(m.group(1).upper())]
    key = t.replace(" ", "")
    alias = {"kadaloor": "Kadalur", "puthenpalli": "Puthanpalli", "vadakupatti": "Vadakkupatti",
             "kizhakkur": "Kizhakkoor", "velliyanoor": "Velliyanur", "periamalai": "Periyamalai",
             "sengaloor": "Sengalur"}
    for z in ZONES:
        if key == z.lower():
            return z
    return alias.get(key)


def resident_cases(D, basis="onset", cls=None, dedup=False):
    c = D["cases"].copy()
    c["z"] = c["zone"].map(zone_of)
    c = c[c["z"].notna()]
    if cls:
        c = c[c["classification"] == cls]
    c["onset"] = pd.to_datetime(c["onset_date"], format="%d-%m-%Y")
    c["notified"] = pd.to_datetime(c["notified_on"], format="%d-%m-%Y")
    if dedup:
        c = c.sort_values("notified").drop_duplicates(["z", "onset", "age_yrs", "sex"], keep="first")
    c["t"] = c[basis]
    return c


def zone_counts(c, z, since=YEAR0):
    """the zone's cases by day from `since`, as a daily series indexed by day number from 1 January 2027"""
    x = c[(c["z"] == z) & (c["t"] >= since)]
    d = ((x["t"] - YEAR0).dt.days).values
    return np.bincount(d, minlength=400).astype(float)


# ------------------------------------------------------------------ the verification panel
def panel_cases(D):
    p = D["panel"]
    c = p[p["arm"] == "CONFIRMED CASE"].copy()
    c["days"] = (pd.to_datetime(c["collected_on"], format="%d-%m-%Y") - pd.to_datetime(c["onset_date"], format="%d-%m-%Y")).dt.days
    c["pos"] = (c["result_final"] == "REACTIVE").astype(int)
    return c


def specificity(D):
    p = D["panel"]
    k = p[p["arm"] == "NEGATIVE CONTROL"]
    return 1.0 - float((k["result_final"] == "REACTIVE").mean())


VISITS = [3, 7, 14, 21, 30, 45, 60, 75, 90, 120, 150]


def se_curve(D, method="visits"):
    """the assay's sensitivity as a function of days since onset, read from the panel's confirmed cases"""
    c = panel_cases(D)
    t, y = c["days"].values.astype(float), c["pos"].values.astype(float)
    if method == "visits":                 # each scheduled visit's specimens, joined by straight lines
        g = np.array([np.argmin(np.abs(np.array(VISITS) - v)) for v in t])
        xs = np.array([t[g == j].mean() for j in range(len(VISITS))])
        ys = np.array([y[g == j].mean() for j in range(len(VISITS))])
        return lambda d: np.where(np.asarray(d) < 0, 0.0, np.interp(np.asarray(d, float), np.r_[0.0, xs], np.r_[0.0, ys]))
    if method == "steps":                  # the visit groups as steps, each held to the midpoint of the next
        g = np.array([np.argmin(np.abs(np.array(VISITS) - v)) for v in t])
        ys = np.array([y[g == j].mean() for j in range(len(VISITS))])
        edges = np.r_[0.0, [(a + b) / 2 for a, b in zip(VISITS[:-1], VISITS[1:])], 10 ** 6]
        def f(d):
            d = np.asarray(d, float)
            j = np.clip(np.searchsorted(edges, d, side="right") - 1, 0, len(ys) - 1)
            return np.where(d < 0, 0.0, ys[j])
        return f
    if method == "bins":                   # fixed bins of days, whatever the visit schedule
        e = np.array([0, 5, 10, 18, 25, 38, 53, 68, 83, 105, 135, 400])
        j = np.searchsorted(e, t, side="right") - 1
        ys = np.array([y[j == i].mean() if (j == i).any() else 0.0 for i in range(len(e) - 1)])
        def f(d):
            d = np.asarray(d, float)
            i = np.clip(np.searchsorted(e, d, side="right") - 1, 0, len(ys) - 1)
            return np.where(d < 0, 0.0, ys[i])
        return f
    if method == "logistic":               # a rise and a fade fitted by maximum likelihood
        from scipy.optimize import minimize

        def curve(th, d):
            a, r0, rs, f0, fs = th
            d = np.clip(d, -50, 1000)
            return 1 / (1 + np.exp(-a)) / (1 + np.exp(-(d - r0) / max(rs, 0.2))) / (1 + np.exp((d - f0) / max(fs, 1.0)))

        def nll(th):
            p = np.clip(curve(th, t), 1e-6, 1 - 1e-6)
            return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
        th = minimize(nll, [3.0, 4.0, 1.5, 70.0, 12.0], method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-6,
                                                                                      "fatol": 1e-8}).x
        return lambda d: np.where(np.asarray(d) < 0, 0.0, curve(th, np.asarray(d, float)))
    if method == "kernel":                 # a Gaussian kernel of 6 days over the specimens
        def f(d):
            d = np.atleast_1d(np.asarray(d, float))
            w = np.exp(-0.5 * ((d[:, None] - t[None, :]) / 6.0) ** 2)
            return np.where(d < 0, 0.0, (w * y).sum(1) / np.maximum(w.sum(1), 1e-9))
        return f
    raise ValueError(method)


def single_se(D, rule):
    c = panel_cases(D)
    if rule == "pooled":
        return float(c["pos"].mean())
    if rule == "from5":
        return float(c[c["days"] >= 5]["pos"].mean())
    if rule == "kit":
        return float(c[(c["days"] >= 5) & (c["days"] <= 60)]["pos"].mean())
    raise ValueError(rule)


# ------------------------------------------------------------------ the call
def zone_results(D):
    r = D["results"].copy()
    r["collected"] = pd.to_datetime(r["collected_on"])
    return r


def published(D):
    r = zone_results(D)
    out = {}
    for z in ZONES:
        x = r[r["zone"] == z]
        out[z] = (len(x), int((x["igm_result"] == "REACTIVE").sum()))
    return out


def effective_se(D, se, cases, z, timing="participant", curve_zone=None):
    """the assay's chance of finding a 2027 infection among the zone's tested residents: the curve averaged over the
    zone's cases by day since 1 January up to each specimen's collection, then over the zone's residents"""
    r = zone_results(D)
    x = r[r["zone"] == z]
    n = zone_counts(cases, curve_zone or z)
    days = np.arange(n.size)
    if timing == "participant":
        cd = ((x["collected"] - YEAR0).dt.days).values
    elif timing == "midpoint":
        cd = np.full(len(x), int(round(((x["collected"] - YEAR0).dt.days).mean())))
    elif timing == "start":
        cd = np.full(len(x), int(((x["collected"] - YEAR0).dt.days).min()))
    elif timing == "end":
        cd = np.full(len(x), int(((x["collected"] - YEAR0).dt.days).max()))
    vals = {}
    out = []
    for d in cd:
        if d not in vals:
            w = n * (days < d)
            vals[d] = float(np.sum(w * se(d - days)) / w.sum())
        out.append(vals[d])
    return float(np.mean(out))


def rogan_gladen(p, se, sp):
    return (p + sp - 1.0) / (se + sp - 1.0)


def call(D, route="golden", **kw):
    """each zone's estimated share infected since 1 January, its ratio to the published share, and the flag"""
    sp = kw.get("sp", specificity(D))
    pub = published(D)
    cases = resident_cases(D, basis=kw.get("basis", "onset"), cls=kw.get("cls"), dedup=kw.get("dedup", False))
    out = {}
    if route in ("pooled", "from5", "kit"):
        s1 = single_se(D, route)
    if route == "golden" or route == "variant":
        se = se_curve(D, kw.get("method", "visits"))
    if route == "city":
        se = se_curve(D, "visits")
        cases = cases.copy()
        cases["z"] = "city"
    for z in ZONES:
        n, a = pub[z]
        p = a / n
        if route in ("pooled", "from5", "kit"):
            s = s1
        elif route in ("golden", "variant"):
            s = effective_se(D, se, cases, z, timing=kw.get("timing", "participant"))
        elif route == "city":
            s = effective_se(D, se, cases, z, curve_zone="city")
        elif route in ("peak", "median", "mean", "w60", "w90"):
            s = plug_in(D, cases, z, route)
        A = rogan_gladen(p, s, sp)
        ratio = A / p
        out[z] = dict(n=n, a=a, p=p, se=s, A=A, ratio=ratio, flag=bool(ratio > TOL_HIGH or ratio < TOL_LOW))
    return out


def plug_in(D, cases, z, how):
    """one sensitivity per zone from a single lag (the peak, the median or the mean days since onset at the zone's
    middle fieldwork day), or the kit sensitivity over a fixed window"""
    se = se_curve(D, "visits")
    r = zone_results(D)
    mid = int(round(((r[r["zone"] == z]["collected"] - YEAR0).dt.days).mean()))
    n = zone_counts(cases, z)
    days = np.arange(n.size)
    w = n * (days < mid)
    f = w / w.sum()
    if how == "peak":
        return float(se(mid - days[np.argmax(w)]))
    if how == "median":
        return float(se(mid - days[np.searchsorted(np.cumsum(f), 0.5)]))
    if how == "mean":
        return float(se(mid - np.sum(f * days)))
    W = 60 if how == "w60" else 90
    lag = mid - days
    return single_se(D, "kit") * float(np.sum(f * ((lag >= 5) & (lag <= W))))


def flagged(out):
    return [z for z in ZONES if out[z]["flag"]]


# ------------------------------------------------------------------ ask A: the November round's Breteau index
def breteau(D, zone_from="premise", keep="inspected", dedup_exact=True):
    i = D["insp"].copy()
    if dedup_exact:
        i = i.drop_duplicates()
    wm = D["wards"]
    if zone_from == "premise":
        i["z"] = [ZONES[int(p.split("/")[0]) - 1] for p in i["premise_id"]]
    elif zone_from == "ward":                       # the ward number joined to the ward master as it stands
        i["z"] = i["ward_no"].map(dict(zip(wm["ward_no"].astype(int), wm["zone"])))
    elif zone_from == "dated":                      # the ward number read in the scheme in force on the day
        old = {}
        for _, w in wm.iterrows():
            for f in str(w["former_ward_nos"]).split(";"):
                old[int(re.match(r"\s*(\d+)", f).group(1))] = w["zone"]
        new = dict(zip(wm["ward_no"].astype(int), wm["zone"]))
        i["z"] = [old[w] if d < "2027-11-16" else new[w] for w, d in zip(i["ward_no"].astype(int), i["inspected_on"])]
    i = i.sort_values(["inspected_on", "record_id"], kind="mergesort")
    if keep == "inspected":                         # each house's first inspection in the month, a locked call not one
        i = i[i["remarks"].fillna("") != "LOCKED"].drop_duplicates("premise_id", keep="first")
    elif keep == "first":
        i = i.drop_duplicates("premise_id", keep="first")
    elif keep == "last":
        i = i.drop_duplicates("premise_id", keep="last")
    out = {}
    for z in ZONES:
        x = i[i["z"] == z]
        out[z] = 100.0 * x["positive_containers"].sum() / x["premise_id"].nunique()
    return out


# ------------------------------------------------------------------ ask B: the household response rate
def response(D, numerator="lab", denominator="sample"):
    s = D["sample"]
    v = D["visits"].drop_duplicates(["household_id", "start"])
    v = v.sort_values(["household_id", "start"], kind="mergesort")
    last = v.groupby("household_id")["visit_outcome"].last()
    if denominator == "sample":                     # every sampled household not found vacant or not a dwelling
        hh = s[["household_id", "zone"]].copy()
    else:                                           # the households the export shows a visit to
        hh = s[s["household_id"].isin(last.index)][["household_id", "zone"]].copy()
    hh["final"] = hh["household_id"].map(last)
    occ = hh[~hh["final"].isin([4, 5])]
    if numerator == "lab":                          # at least one member's specimen reached the laboratory
        got = set(D["lab"]["barcode"].str.slice(3, 9))
    elif numerator == "results":                    # at least one member has a result
        got = set(D["results"]["household_id"])
    elif numerator == "outcome":                    # the interview was completed
        got = set(last[last == 1].index)
    out = {}
    for z in ZONES:
        x = occ[occ["zone"] == z]
        out[z] = 100.0 * x["household_id"].isin(got).sum() / len(x)
    return out


def solve(target, F):
    D = load(target, F)
    X = {"golden": call(D, "golden")}
    for r in ("pooled", "from5", "kit", "city", "peak", "median", "mean", "w60", "w90"):
        X[r] = call(D, r)
    X["breteau"] = breteau(D)
    X["response"] = response(D)
    X["sp"] = specificity(D)
    X["se_single"] = {k: single_se(D, k) for k in ("pooled", "from5", "kit")}
    X["D"] = D
    return X
