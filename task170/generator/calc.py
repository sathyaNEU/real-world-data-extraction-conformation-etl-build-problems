"""task170 golden computation, from the pack alone (target/), the way Human Factors' analyst works it.

The call: every Phase 1 to 3 driver's ETCS starts in the recorder log, counted on the driver's own count of starts
(staff numbers chained through Resourcing's crosswalk, test starts left out); each train data entry error the safety
desk recorded (category TDE, not withdrawn, linked reports once) placed at its start; the chance of an error read in
bands of 50 on that count; and each driver on a Phase 4 roster run along it from the starts the driver already has,
for twelve months at the driver's 2026 monthly cab activations (duties worked, latest issue). The asks: Class 461
units accepted for ETCS service by each Phase 4 depot's go-live (each allocated unit's two driving vehicles as the
formation list holds them, actual or planned acceptance); and the Phase 1 to 3 depots' level transition errors and
brake interventions of January to October 2026 (the recorder downloads' reports, stamped in UTC, folded into the
manual reports of the same event)."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import common as C

BANDS = list(range(0, 650, 50)) + [10 ** 9]     # the golden's bands: 50 starts each to 600, then one band
SLOW = ("Spare", "Instructor", "Manager", "Restricted duties")


def load(target):
    P = lambda f: os.path.join(target, f)
    d = {}
    d["som"] = pd.read_csv(P(C.F_SOM), dtype={"driver_id": str, "unit": str})
    d["reg"] = pd.read_excel(P(C.F_REG), dtype={"Staff No": str, "Unit": str, "SoM Ref": str})
    d["roster"] = pd.read_excel(P(C.F_ROSTER), dtype={"Staff No": str})
    d["xwalk"] = pd.read_csv(P(C.F_XWALK), dtype=str)
    d["duty"] = pd.read_csv(P(C.F_DUTY), dtype={"staff_no": str})
    d["alloc"] = pd.read_csv(P(C.F_ALLOC), dtype=str)
    d["works"] = pd.read_excel(P(C.F_WORKS), dtype={"Vehicle": str, "Unit": str})
    d["form"] = pd.read_csv(P(C.F_FORM), dtype=str)
    d["renum"] = pd.read_csv(P(C.F_RENUM), dtype=str)
    return d


def chain(xw):
    """every staff number to the person's latest number"""
    nxt = dict(zip(xw["old_staff_no"], xw["new_staff_no"]))

    def last(s):
        seen = set()
        while s in nxt and s not in seen:
            seen.add(s)
            s = nxt[s]
        return s
    return last


def starts(d):
    """driver starts with each start's place on the driver's own count (0 for the first ETCS start)"""
    s = d["som"]
    s = s[s["som_type"] != "TST"].copy()
    last = chain(d["xwalk"])
    s["person"] = s["driver_id"].map(last)
    s["t"] = pd.to_datetime(s["obr_utc"].str.slice(0, 19))
    s = s.sort_values(["person", "t", "som_ref"], kind="mergesort")
    s["n"] = s.groupby("person").cumcount()
    return s


def to_utc(local):
    return [C.local_to_utc(t.to_pydatetime()) for t in local]


def tde_errors(d, s):
    """each recorded train data entry error (primary report, not withdrawn) with the driver and the start it was
    made at: the SoM Ref of the error's own report or of a report linked to it, else the driver's last start before
    the report (the register's time is local; the recorder's UTC)"""
    r = d["reg"]
    r = r[(r["Category"] == "TDE") & (r["Status"] != "Withdrawn")].copy()
    linked = r[r["Linked To"].notna()]
    ref_of_link = linked[linked["SoM Ref"].notna()].groupby("Linked To")["SoM Ref"].first()
    e = r[r["Linked To"].isna()].copy()
    e["ref"] = e["SoM Ref"].where(e["SoM Ref"].notna(), e["Report No"].map(ref_of_link))
    last = chain(d["xwalk"])
    e["person"] = e["Staff No"].map(last)
    e["t_utc"] = to_utc(pd.to_datetime(e["Received"]))
    by_ref = s.set_index("som_ref")["n"]
    e["n"] = e["ref"].map(by_ref)
    miss = e["n"].isna()
    if miss.any():
        grp = {k: v for k, v in s.groupby("person")}
        vals = []
        for p, t in zip(e.loc[miss, "person"], e.loc[miss, "t_utc"]):
            g = grp.get(p)
            if g is None:
                vals.append(np.nan)
                continue
            k = int(np.searchsorted(g["t"].values, np.datetime64(t), side="right")) - 1
            vals.append(float(g["n"].values[k]) if k >= 0 else np.nan)
        e.loc[miss, "n"] = vals
    return e


def tallies(s, e):
    """starts and errors at each place on the drivers' own counts"""
    T = np.bincount(s["n"].values.astype(int)).astype(float)
    E = np.bincount(e["n"].dropna().values.astype(int), minlength=len(T)).astype(float)[:len(T)]
    return T, E


def band_rates(T, E, edges=BANDS):
    k = np.arange(len(T))
    b = np.digitize(k, edges) - 1
    rates = np.array([E[b == i].sum() / T[b == i].sum() for i in range(len(edges) - 1)])
    return lambda x: rates[np.digitize(np.asarray(x), edges) - 1], rates


def forward(d, s):
    """each driver on a Phase 4 roster: the ETCS starts already made (prior) and the starts in the depot's first
    twelve months (twelve times the monthly cab activations on duties worked in January to October 2026, latest
    issue)"""
    last = chain(d["xwalk"])
    du = d["duty"]
    du = du[du["status"] == "Worked"]
    du = du.sort_values("issue").drop_duplicates(["duty_date", "staff_no", "duty_no"], keep="last")
    act = du.assign(person=du["staff_no"].map(last)).groupby("person")["cab_activations"].sum()
    ro = d["roster"]
    p4 = ro[ro["Depot"].isin(C.P4_CODES)].copy()
    p4["person"] = p4["Staff No"].map(last)
    prior = s.groupby("person").size()
    p4["prior"] = p4["person"].map(prior).fillna(0).astype(int)
    p4["starts"] = p4["person"].map(act).fillna(0).astype(float) * 12.0 / C.DUTY_MONTHS
    return p4


def run_along(pf, p4):
    """expected errors: each driver's starts from prior to prior + starts on the curve pf (a fractional last start
    counted at its share)"""
    hi = int(np.ceil((p4["prior"] + p4["starts"]).max())) + 2
    pv = np.asarray(pf(np.arange(hi)), float)
    cs = np.concatenate([[0.0], np.cumsum(pv)])
    a = p4["prior"].values.astype(float)
    b = a + p4["starts"].values

    def S(x):
        f = np.floor(x).astype(int)
        return cs[f] + (x - f) * pv[np.minimum(f, len(pv) - 1)]
    return S(b) - S(a)


# ------------------------------------------------------------------ the routes short of the curve on the count
def depot_windows(s):
    """each record start's month since its depot's go-live (the depot the driver's number belonged to)"""
    blk = {"%02d" % v: k for k, v in C.BLOCK.items()}
    dep = s["driver_id"].str.slice(0, 2).map(blk)
    gl = dep.map({c: pd.Timestamp(C.DEPOT[c][3]) for c in C.REC_CODES})
    loc = pd.Series([C.utc_to_local(t.to_pydatetime()) for t in s["t"]], index=s.index)
    loc = pd.to_datetime(loc)
    mi = (loc.dt.year - gl.dt.year) * 12 + (loc.dt.month - gl.dt.month) - (loc.dt.day < gl.dt.day).astype(int)
    return dep, mi


def rungs(d, s, e, p4):
    out = {}
    dep, mi = depot_windows(s)
    first = (mi >= 0) & (mi < 12)
    sf = s[first]
    ef = e[e["ref"].isin(set(sf["som_ref"])) | (e["ref"].isna() & e["n"].notna())]
    # an error belongs to the first-year window when its start does
    key = s.set_index(["person", "n"]).index
    win = pd.Series(first.values, index=key)
    e_first = e[[bool(win.get((p, int(n)), False)) if n == n else False for p, n in zip(e["person"], e["n"])]]
    U = float(p4["starts"].sum())
    out["pooled"] = len(e_first) / float(len(sf)) * U
    m_of = pd.Series(mi.values, index=key)
    e_m = np.array([m_of.get((p, int(n)), -1) for p, n in zip(e_first["person"], e_first["n"])])
    out["month"] = sum((e_m == m).sum() / float((mi[first] == m).sum()) * U / 12.0 for m in range(12))
    drivers = sf["person"].unique()
    per = e_first.groupby("person").size().reindex(drivers).fillna(0)
    out["per_driver"] = float(per.mean()) * len(p4)
    ro = d["roster"]
    last = chain(d["xwalk"])
    link = dict(zip(ro["Staff No"].map(last), ro["Link"]))
    slow_p = {p for p, l in link.items() if l in SLOW}
    sl = sf[sf["person"].isin(slow_p)]
    out["slow_analogue"] = len(e_first[e_first["person"].isin(slow_p)]) / float(len(sl)) * U
    # the pool held to years of service (bands of ten), each Phase 4 driver at the band's first-year rate
    qual = dict(zip(ro["Staff No"].map(last), pd.to_datetime(ro["Qualified"])))
    yrs = lambda p: (pd.Timestamp(C.RECORD_END) - qual[p]).days / 365.25 if p in qual else np.nan
    sf_y = sf["person"].map({p: yrs(p) for p in sf["person"].unique()})
    ef_y = e_first["person"].map({p: yrs(p) for p in e_first["person"].unique()})
    p4_y = p4["person"].map({p: yrs(p) for p in p4["person"]})
    sv = 0.0
    for lo, hi in ((0, 10), (10, 20), (20, 30), (30, 99)):
        a = ((sf_y >= lo) & (sf_y < hi)).sum()
        b = ((ef_y >= lo) & (ef_y < hi)).sum()
        sv += b / float(a) * p4.loc[(p4_y >= lo) & (p4_y < hi), "starts"].sum()
    out["service"] = sv
    return out


# ------------------------------------------------------------------ ask A: Class 461 units accepted by go-live
def fleet(d, how="formations"):
    w = d["works"].copy()
    w["date"] = pd.to_datetime(w["Accepted"]).fillna(pd.to_datetime(w["Planned Acceptance"]))
    when = dict(zip(w["Vehicle"], w["date"]))
    status = dict(zip(w["Vehicle"], w["Status"]))
    golive = {c: pd.Timestamp(C.DEPOT[c][3]) for c in C.P4_CODES}
    if how in ("formations", "any", "accepted_only"):
        veh = {u: (a, b) for u, a, b in zip(d["form"]["unit"], d["form"]["vehicle_a_end"], d["form"]["vehicle_b_end"])}
    else:
        nxt = dict(zip(d["renum"]["old_unit"], d["renum"]["new_unit"]))

        def cur(u):
            while u in nxt:
                u = nxt[u]
            return u
        veh = {}
        for v, u, end in zip(w["Vehicle"], w["Unit"], w["End"]):
            key = cur(u) if how == "programme" else u
            veh.setdefault(key, ["", ""])["AB".index(end)] = v
        veh = {k: tuple(v) for k, v in veh.items()}
    out = {}
    for c in C.P4_CODES:
        units = d["alloc"].loc[d["alloc"]["depot"] == c, "unit"]
        acc = 0
        for u in units:
            vs = [v for v in veh.get(u, ("", "")) if v]
            ok = [v in when and when[v] <= golive[c] for v in vs]
            if how == "accepted_only":
                ok = [status.get(v) == "Accepted" for v in vs]
            good = (len(vs) == 2 and all(ok)) if how != "any" else any(ok)
            acc += int(good)
        out[c] = (acc, int(len(units)) - acc)
    return out


# ------------------------------------------------------------------ ask C: level transition errors and brake interventions
def events(d, how="golden", window=(dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1))):
    r = d["reg"]
    r = r[r["Category"].isin(["LTR", "BRK"]) & (r["Status"] != "Withdrawn")].copy()
    r["t"] = pd.to_datetime(r["Received"])
    obr = r["Reporter"] == "OBR download"
    if how in ("golden", "fold_day", "manual_only", "obr_only"):
        r.loc[obr, "t"] = [pd.Timestamp(C.utc_to_local(t.to_pydatetime())) for t in r.loc[obr, "t"]]
    r = r[(r["t"] >= window[0]) & (r["t"] < window[1])]
    r = r[r["Linked To"].isna()]
    if how == "all_rows":
        keep = r
    elif how == "obr_only":
        keep = r[r["Reporter"] == "OBR download"]
    elif how == "manual_only":
        keep = r[r["Reporter"] != "OBR download"]
    elif how == "fold_day":
        keep = r.assign(day=r["t"].dt.date).drop_duplicates(["Staff No", "Unit", "Category", "day"])
    else:
        # golden (recorder times read as UTC) and fold_as_local (recorder times read as local): a recorder report
        # is the same event as a manual report of the driver, unit and category up to 30 minutes after it
        man = r[r["Reporter"] != "OBR download"]
        ob = r[r["Reporter"] == "OBR download"]
        used = set()
        drop = set()
        mg = {k: g.sort_values("t") for k, g in man.groupby(["Staff No", "Unit", "Category"])}
        for i, row in ob.sort_values("t").iterrows():
            g = mg.get((row["Staff No"], row["Unit"], row["Category"]))
            if g is None:
                continue
            dtm = (g["t"] - row["t"]).dt.total_seconds() / 60.0
            cand = [j for j, x in zip(g.index, dtm) if 0 <= x <= 30 and j not in used]
            if cand:
                used.add(cand[0])
                drop.add(i)
        keep = r.drop(index=list(drop))
    out = {}
    for c in C.REC_CODES:
        k = keep[keep["Depot"] == c]
        out[c] = (int((k["Category"] == "LTR").sum()), int((k["Category"] == "BRK").sum()))
    return out


def compute(target):
    d = load(target)
    s = starts(d)
    e = tde_errors(d, s)
    T, E = tallies(s, e)
    pf, rates = band_rates(T, E)
    p4 = forward(d, s)
    res = {"data": d, "starts": s, "errors": e, "T": T, "E": E, "rates": rates, "p4": p4}
    res["call"] = float(run_along(pf, p4).sum())
    res["by_depot"] = {c: float(run_along(pf, p4[p4["Depot"] == c]).sum()) for c in C.P4_CODES}
    res["drivers"] = int(len(p4))
    res["starts_fwd"] = float(p4["starts"].sum())
    res["fleet"] = fleet(d)
    res["events"] = events(d)
    return res
