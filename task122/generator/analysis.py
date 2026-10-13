"""task122: the golden analysis, run on the shipped pack only.

Main call: each dose's eGFR difference from placebo at month 36 (week 156) on the synopsis's estimand. Every
randomised patient as randomised; the central laboratory's CKD-EPI 2021 eGFR at the scheduled visits (the first
sample of a visit); baseline the mean of the screening and day-1 values; values from samples taken after a patient's
last dose set aside for patients who stopped study drug for good (read from the dosing record); each arm's mean
change by visit against placebo's; the chronic phase fitted from week 24, after the recovery that easing background
diuretics from week 12 produced, and carried to week 156 from the level the arm settled at.

Asks: hyperkalaemia (patients with an on-treatment serum potassium above 5.5 mmol/L from any laboratory; hyperkalaemia
adverse events, counted by event, that began on treatment) and exposure (patients who stopped study drug for good
before their week-52 visit; days on study drug before that visit, as patient-years)."""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

ARMS = ["Placebo", "VMK-4410 5 mg", "VMK-4410 10 mg", "VMK-4410 20 mg", "VMK-4410 40 mg"]
DOSES = ARMS[1:]
NOMINAL = {"DAY 1": 0, "WEEK 2": 2, "WEEK 4": 4, "WEEK 8": 8, "WEEK 12": 12, "WEEK 16": 16, "WEEK 20": 20,
           "WEEK 24": 24, "WEEK 32": 32, "WEEK 40": 40, "WEEK 52": 52}
HYPERK = {"Hyperkalaemia", "Blood potassium increased"}


def load(tgt):
    rd = lambda f: pd.read_csv(os.path.join(tgt, f), dtype=str, keep_default_na=False)
    T = {k: rd(k + ".csv") for k in ["dm", "sv", "ex", "ds", "lb", "ae", "cm"]}
    for k in ("lb",):
        T[k]["LBSTRESN"] = pd.to_numeric(T[k]["LBSTRESN"], errors="coerce")
    return T


def dosing_dates(T):
    ex = T["ex"]
    first = ex.groupby("USUBJID")["EXSTDTC"].min().map(date.fromisoformat)
    last = ex.groupby("USUBJID")["EXENDTC"].max().map(date.fromisoformat)
    sv = T["sv"]
    w52 = sv[sv["VISIT"] == "WEEK 52"].groupby("USUBJID")["SVSTDTC"].min().map(date.fromisoformat)
    return first, last, w52


def randomised(T):
    dm = T["dm"]
    r = dm[dm["ARM"] != ""]
    return dict(zip(r["USUBJID"], r["ARM"]))


def egfr_long(T, central_only=True, first_sample=True, keep_after_stop=False, stop_from_ds=False, actual=False):
    """central CKD-EPI 2021 eGFR at scheduled visits, change from baseline, with the estimand's set-aside"""
    arm = randomised(T)
    first, last, w52 = dosing_dates(T)
    lb = T["lb"]
    e = lb[(lb["LBTESTCD"] == "EGFR") & lb["USUBJID"].isin(arm)]
    if central_only:
        e = e[e["LBNAM"].str.startswith("Tavlund Central Laboratory")]
    e = e[e["VISIT"].isin(["SCREENING"] + list(NOMINAL))].copy()
    e["DT"] = e["LBDTC"].str[:10].map(date.fromisoformat)
    e = e.sort_values(["USUBJID", "VISIT", "LBDTC"], kind="mergesort")
    if first_sample:
        e = e.drop_duplicates(["USUBJID", "VISIT"], keep="first")
    else:
        e = e.groupby(["USUBJID", "VISIT"], as_index=False).agg({"LBSTRESN": "mean", "DT": "first", "LBDTC": "first"})
    base = e[e["VISIT"].isin(["SCREENING", "DAY 1"])].groupby("USUBJID")["LBSTRESN"].mean()
    on = e[e["VISIT"].isin(list(NOMINAL))].copy()
    on["ARM"] = on["USUBJID"].map(arm)
    on["BASE"] = on["USUBJID"].map(base)
    on["CHG"] = on["LBSTRESN"] - on["BASE"]
    on["W"] = on["VISIT"].map(NOMINAL)
    on["DAY"] = [(dt - first[u]).days + 1 for u, dt in zip(on["USUBJID"], on["DT"])]
    if not keep_after_stop:
        if stop_from_ds:
            ds = T["ds"]
            stp = ds[(ds["DSSCAT"] == "STUDY DRUG") & (ds["DSDECOD"] != "COMPLETED")]
            lastd = dict(zip(stp["USUBJID"], stp["DSSTDTC"].map(date.fromisoformat)))
        else:
            lastd = {u: last[u] for u in last.index if (u not in w52.index) or last[u] < w52[u]}
        keep = [not (u in lastd and dt > lastd[u]) for u, dt in zip(on["USUBJID"], on["DT"])]
        on = on[keep]
    return on[on["CHG"].notna()]


def arm_diffs(on):
    av = on.groupby(["ARM", "W"])["CHG"].mean().unstack(0)
    return {a: av[a] - av["Placebo"] for a in DOSES}, av


def line_at(series, start, end=52, at=156):
    s = series[(series.index >= start) & (series.index <= end)].dropna()
    b, a = np.polyfit(np.array(s.index, float) / 52.0, s.to_numpy(float), 1)
    return float(a + b * at / 52.0), float(b), float(a)


def routes(on):
    d, av = arm_diffs(on)
    out = {}
    for a in DOSES:
        s = d[a]
        r = {"w52": float(s.loc[52])}
        for k in (0, 4, 12, 16, 20, 24, 32):
            r["k%d" % k], r["s%d" % k], r["i%d" % k] = line_at(s, k)
        out[a] = r
    return out, d, av


def pooled_actual(on, start=24, at_days=1092):
    out = {}
    for a, g in on[on["W"] >= start].groupby("ARM"):
        b, c = np.polyfit((g["DAY"].to_numpy(float) - 1) / 365.25, g["CHG"].to_numpy(float), 1)
        out[a] = c + b * at_days / 365.25
    return {a: float(out[a] - out["Placebo"]) for a in DOSES}


def per_patient(on, start=24, at=156, min_n=3):
    vals = {}
    for (a, u), g in on[on["W"] >= start].groupby(["ARM", "USUBJID"]):
        if len(g) < min_n:
            continue
        b, c = np.polyfit(g["W"].to_numpy(float) / 52.0, g["CHG"].to_numpy(float), 1)
        vals.setdefault(a, []).append(c + b * at / 52.0)
    m = {a: float(np.mean(v)) for a, v in vals.items()}
    return {a: m[a] - m["Placebo"] for a in DOSES}


def mixed_model(on, start=24, at=156):
    """random intercept and slope per patient, fixed arm-specific intercepts and slopes, over visits from `start`"""
    import statsmodels.formula.api as smf
    import warnings
    d = on[on["W"] >= start].copy()
    d["T"] = d["W"] / 52.0
    d["ARMC"] = d["ARM"].map({a: i for i, a in enumerate(ARMS)})
    d["ARMF"] = pd.Categorical(d["ARMC"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = smf.mixedlm("CHG ~ C(ARMF) + C(ARMF):T - 1", d, groups=d["USUBJID"], re_formula="~T").fit(reml=True, method="lbfgs")
    fe = m.fe_params
    val = {}
    for i, a in enumerate(ARMS):
        val[a] = fe["C(ARMF)[%d]" % i] + fe["C(ARMF)[%d]:T" % i] * at / 52.0
    return {a: float(val[a] - val["Placebo"]) for a in DOSES}


# ------------------------------------------------------------------------------------------------ asks
def imputed_start(s, first):
    if len(s) == 10:
        return date.fromisoformat(s)
    if len(s) == 7:
        y, m = int(s[:4]), int(s[5:7])
        return first if (first.year, first.month) == (y, m) else date(y, m, 1)
    y = int(s[:4])
    return first if first.year == y else date(y, 1, 1)


def asks(T):
    arm = randomised(T)
    first, last, w52 = dosing_dates(T)
    out = {"A_k": {}, "A_ae": {}, "B_stop": {}, "B_years": {}}
    wrong = {"A_k_central": {}, "A_ae_rows": {}, "A_ae_one_term": {}, "A_ae_teae_rows_any": {}, "B_stop_ds": {},
             "B_years_rows": {}, "B_years_incl_visit": {}, "A_k_incl_day1_wk56": {}}
    lb = T["lb"]
    k = lb[(lb["LBTESTCD"] == "K") & (lb["LBSPEC"] == "SERUM") & lb["USUBJID"].isin(arm) & lb["LBSTRESN"].notna()].copy()
    k["DT"] = k["LBDTC"].str[:10].map(date.fromisoformat)
    k["F"] = k["USUBJID"].map(first)
    k["L"] = k["USUBJID"].map(last)
    on = k[(k["DT"] > k["F"]) & (k["DT"] <= k["L"])]
    hi = on[on["LBSTRESN"] > 5.5]
    hic = hi[hi["LBNAM"].str.startswith("Tavlund Central Laboratory")]
    hiw = k[(k["LBSTRESN"] > 5.5) & (k["DT"] >= k["F"])]
    ae = T["ae"]
    h = ae[ae["AEDECOD"].isin(HYPERK) & ae["USUBJID"].isin(arm)].copy()
    h["ST"] = [imputed_start(s, first[u]) for s, u in zip(h["AESTDTC"], h["USUBJID"])]
    ev = h.groupby(["USUBJID", "AEGRPID"])["ST"].min().reset_index()
    ev["ARM"] = ev["USUBJID"].map(arm)
    ev_on = ev[[first[u] <= s <= last[u] for u, s in zip(ev["USUBJID"], ev["ST"])]]
    rows_on = h[[first[u] <= s <= last[u] + timedelta(days=30) for u, s in zip(h["USUBJID"], h["ST"])]]
    ds = T["ds"]
    stp = ds[(ds["DSSCAT"] == "STUDY DRUG") & (ds["DSDECOD"] != "COMPLETED") & ds["USUBJID"].isin(arm)]
    ex = T["ex"][T["ex"]["USUBJID"].isin(arm)]
    days, rowdays, rowdays_incl = {}, {}, {}
    for u, g in ex.groupby("USUBJID"):
        cut = w52[u] if u in w52.index else None
        dd = set()
        rd = rdi = 0
        for a, b in zip(g["EXSTDTC"], g["EXENDTC"]):
            a, b = date.fromisoformat(a), date.fromisoformat(b)
            n = (b - a).days + 1
            for i in range(n):
                x = a + timedelta(days=i)
                if cut is None or x < cut:
                    dd.add(x)
            bb = b if cut is None else min(b, cut - timedelta(days=1))
            rd += max((bb - a).days + 1, 0)
            bi = b if cut is None else min(b, cut)
            rdi += max((bi - a).days + 1, 0)
        days[u] = len(dd)
        rowdays[u] = rd
        rowdays_incl[u] = rdi
    for a in ARMS:
        us = [u for u, x in arm.items() if x == a]
        out["A_k"][a] = int(hi[hi["USUBJID"].isin(us)]["USUBJID"].nunique())
        wrong["A_k_central"][a] = int(hic[hic["USUBJID"].isin(us)]["USUBJID"].nunique())
        wrong["A_k_incl_day1_wk56"][a] = int(hiw[hiw["USUBJID"].isin(us)]["USUBJID"].nunique())
        out["A_ae"][a] = int((ev_on["ARM"] == a).sum())
        hr = h[h["USUBJID"].isin(us)]
        wrong["A_ae_rows"][a] = int(sum(1 for u, s in zip(hr["USUBJID"], hr["ST"]) if first[u] <= s <= last[u]))
        wrong["A_ae_one_term"][a] = int(((ev_on["ARM"] == a) & ev_on.apply(
            lambda r: (h[(h["USUBJID"] == r["USUBJID"]) & (h["AEGRPID"] == r["AEGRPID"])]["AEDECOD"] == "Hyperkalaemia").any(), axis=1)).sum()) if len(ev_on) else 0
        wrong["A_ae_teae_rows_any"][a] = int(rows_on["USUBJID"].isin(us).sum())
        out["B_stop"][a] = int(sum(1 for u in us if (u not in w52.index) or last[u] < w52[u]))
        wrong["B_stop_ds"][a] = int(sum(1 for u in us if u in set(stp["USUBJID"])
                                        and ((u not in w52.index) or date.fromisoformat(stp[stp["USUBJID"] == u]["DSSTDTC"].iloc[0]) < w52[u])))
        out["B_years"][a] = sum(days[u] for u in us if u in days) / 365.25
        wrong["B_years_rows"][a] = sum(rowdays[u] for u in us if u in rowdays) / 365.25
        wrong["B_years_incl_visit"][a] = sum(rowdays_incl[u] for u in us if u in rowdays_incl) / 365.25
    return out, wrong


def run(tgt):
    T = load(tgt)
    on = egfr_long(T)
    rt, d, av = routes(on)
    gold = {a: rt[a]["k24"] for a in DOSES}
    order = sorted(DOSES, key=lambda a: -gold[a])
    R = {"T": T, "on": on, "routes": rt, "diff": d, "armmeans": av, "gold": gold, "call": order[0], "runner": order[1],
         "gap": gold[order[0]] - gold[order[1]], "slope24": {a: rt[a]["s24"] for a in DOSES},
         "int24": {a: rt[a]["i24"] for a in DOSES},
         "m12": {a: rt[a]["i24"] + rt[a]["s24"] * 1.0 for a in DOSES},
         "m24": {a: rt[a]["i24"] + rt[a]["s24"] * 2.0 for a in DOSES}}
    R["settled"] = {a: rt[a]["i24"] + rt[a]["s24"] * 24 / 52.0 for a in DOSES}
    R["rise_12_24"] = {a: float(d[a].loc[24] - d[a].loc[12]) for a in DOSES}
    L20, L40 = R["settled"]["VMK-4410 20 mg"], R["settled"]["VMK-4410 40 mg"]
    R["flip_slope"] = (L20 - L40) / ((156 - 24) / 52.0)
    arm = randomised(T)
    first, last, w52 = dosing_dates(T)
    R["n_arm"] = {a: sum(1 for x in arm.values() if x == a) for a in ARMS}
    R["n_stop"] = {a: sum(1 for u, x in arm.items() if x == a and ((u not in w52.index) or last[u] < w52[u])) for a in ARMS}
    R["loop"], R["eased"] = diuretics(T, arm, first)
    R["asks"], R["asks_wrong"] = asks(T)
    return R


def diuretics(T, arm, first):
    """patients on a loop diuretic at randomisation, and those whose loop diuretic was reduced or stopped on the day of
    their week-12, 16 or 20 visit"""
    cm = T["cm"] if "cm" in T else None
    sv = T["sv"]
    vis = sv[sv["VISIT"].isin(["WEEK 12", "WEEK 16", "WEEK 20"])]
    vdates = {}
    for u, dt in zip(vis["USUBJID"], vis["SVSTDTC"]):
        vdates.setdefault(u, set()).add(date.fromisoformat(dt))
    loop = cm[cm["CMCLASCD"] == "C03CA"]

    def daily(r):
        if r["CMDOSE"] != "":
            k = {"QD": 1, "BID": 2, "TID": 3}.get(r["CMDOSFRQ"], 1)
            return float(r["CMDOSE"]) * k
        nums = [float(x) for x in __import__("re").findall(r"(\d+(?:\.\d+)?) mg", r["CMDOSTXT"])]
        return sum(nums)

    on_loop, eased = {a: 0 for a in ARMS}, {a: 0 for a in ARMS}
    for u, g in loop.groupby("USUBJID"):
        if u not in arm:
            continue
        rd = first[u]
        g = g.sort_values("CMSTDTC")
        cover = [r for _, r in g.iterrows() if (r["CMENDTC"] == "" or date.fromisoformat(r["CMENDTC"]) >= rd)
                 and (len(r["CMSTDTC"]) < 10 or date.fromisoformat(r["CMSTDTC"]) <= rd)]
        if not cover:
            continue
        on_loop[arm[u]] += 1
        hit = False
        for _, r in g.iterrows():
            if r["CMENDTC"] == "":
                continue
            end = date.fromisoformat(r["CMENDTC"])
            nxt = end + timedelta(days=1)
            if nxt not in vdates.get(u, set()):
                continue
            after = [x for _, x in g.iterrows() if x["CMSTDTC"] == nxt.isoformat()]
            if not after or daily(after[0]) < daily(r):
                hit = True
        eased[arm[u]] += hit
    return on_loop, eased


# ------------------------------------------------------------------------------------------------ variants for the checks
WINDOW = {"WEEK 2": (15, 3), "WEEK 4": (29, 3), "WEEK 8": (57, 5), "WEEK 12": (85, 5), "WEEK 16": (113, 7),
          "WEEK 20": (141, 7), "WEEK 24": (169, 7), "WEEK 32": (225, 10), "WEEK 40": (281, 10), "WEEK 52": (365, 10)}


def egfr_long_window(T):
    """the main path with every visit taken outside its protocol window dropped"""
    on = egfr_long(T)
    keep = [v == "DAY 1" or abs(dy - WINDOW[v][0]) <= WINDOW[v][1] for v, dy in zip(on["VISIT"], on["DAY"])]
    return on[keep]


def egfr_recomputed(T):
    """the main path with eGFR recomputed from the reported creatinine, age at collection and sex"""
    import copy
    T2 = dict(T)
    lb = T["lb"].copy()
    dm = T["dm"]
    sex = dict(zip(dm["USUBJID"], dm["SEX"]))
    age = dict(zip(dm["USUBJID"], dm["AGE"]))
    cons = dict(zip(dm["USUBJID"], dm["RFICDTC"]))
    cr = lb[(lb["LBTESTCD"] == "CREAT") & lb["LBNAM"].str.startswith("Tavlund")].set_index("LBREFID")["LBSTRESN"]
    m = (lb["LBTESTCD"] == "EGFR") & lb["LBNAM"].str.startswith("Tavlund") & lb["USUBJID"].isin(set(dm[dm["ARM"] != ""]["USUBJID"]))
    vals = []
    for u, ref, dtc in zip(lb.loc[m, "USUBJID"], lb.loc[m, "LBREFID"], lb.loc[m, "LBDTC"]):
        yrs = (date.fromisoformat(dtc[:10]) - date.fromisoformat(cons[u])).days / 365.25
        mg = cr[ref] / 88.42
        vals.append(ckd_2021(mg, int(age[u]) + int(yrs), sex[u]))
    lb.loc[m, "LBSTRESN"] = vals
    T2["lb"] = lb
    return egfr_long(T2)


def ckd_2021(mg, age, sex):
    k, a = (0.7, -0.241) if sex == "F" else (0.9, -0.302)
    r = mg / k
    g = 142.0 * min(r, 1.0) ** a * max(r, 1.0) ** -1.200 * 0.9938 ** age
    return g * (1.012 if sex == "F" else 1.0)


def egfr_long_with_unscheduled(T):
    """the main path plus every unscheduled central eGFR on treatment, placed by actual study day"""
    on = egfr_long(T)
    arm = randomised(T)
    first, last, w52 = dosing_dates(T)
    lb = T["lb"]
    u = lb[(lb["LBTESTCD"] == "EGFR") & lb["LBNAM"].str.startswith("Tavlund") & (lb["VISIT"] == "UNSCHEDULED")
           & lb["USUBJID"].isin(arm)].copy()
    u["DT"] = u["LBDTC"].str[:10].map(date.fromisoformat)
    u = u[[first[x] < d <= last[x] for x, d in zip(u["USUBJID"], u["DT"])]]
    base = on.drop_duplicates("USUBJID").set_index("USUBJID")["BASE"]
    u["ARM"] = u["USUBJID"].map(arm)
    u["BASE"] = u["USUBJID"].map(base)
    u["CHG"] = u["LBSTRESN"] - u["BASE"]
    u["DAY"] = [(d - first[x]).days + 1 for x, d in zip(u["USUBJID"], u["DT"])]
    u["W"] = (u["DAY"] - 1) / 7.0
    return pd.concat([on, u[on.columns.intersection(u.columns)]], ignore_index=True).dropna(subset=["CHG"])


def with_week56(T):
    """each dose's line through weeks 24 to 56 with the off-treatment week-56 visit fitted in, read at week 156"""
    on = egfr_long(T)
    arm = randomised(T)
    lb = T["lb"]
    o = lb[(lb["LBTESTCD"] == "EGFR") & lb["LBNAM"].str.startswith("Tavlund") & (lb["VISIT"] == "WEEK 56 FOLLOW-UP")
           & lb["USUBJID"].isin(arm)].drop_duplicates("USUBJID").copy()
    base = on.drop_duplicates("USUBJID").set_index("USUBJID")["BASE"]
    o["ARM"] = o["USUBJID"].map(arm)
    o["CHG"] = o["LBSTRESN"] - o["USUBJID"].map(base)
    o["W"] = 56
    allv = pd.concat([on[["USUBJID", "ARM", "W", "CHG"]], o[["USUBJID", "ARM", "W", "CHG"]]]).dropna()
    av = allv.groupby(["ARM", "W"])["CHG"].mean().unstack(0)
    return {a: line_at(av[a] - av["Placebo"], 24, end=56)[0] for a in DOSES}


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join((p.extract_text() or "") for p in PdfReader(path).pages).replace("\n", " ")
