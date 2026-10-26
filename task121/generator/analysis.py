"""The main call for task121 from the cut pack: what caused the rise in the under-triage rate from March 2026.

The calls the crews found critical or emergent are matched to the shift each was answered on, through the call-taker's
login and the scheduling system's employee number, and each shift carries the rest the call-taker had before it, from
the end of the previous shift the roster shows. The rungs below are the readings the ladder sets against the golden."""
import numpy as np
import pandas as pd

import common as K
import pack as P


def frame(target):
    d = P.load(target)
    calls = d["calls"].copy()
    calls["t"] = P.local(calls["call_answered"])
    calls = calls[(calls["t"].dt.date >= K.START) & (calls["t"].dt.date <= K.END)].copy()
    e = d["epcr"].copy()
    e["incident_no"] = e["incident_number"].str[:2] + "-" + e["incident_number"].str[2:]
    e["acuity"] = e["crew_acuity"].str[0].astype(int)
    worst = e.groupby("incident_no")["acuity"].min()
    calls["acuity"] = calls["incident_no"].map(worst)
    calls["under"] = calls["response"] == "COLD"
    r = d["roster"].copy()
    r["s"] = P.local(r["start"], False)
    r["e"] = P.local(r["end"], False)
    r = r.sort_values(["employee_no", "s"]).reset_index(drop=True)
    r["rest"] = (r["s"] - r.groupby("employee_no")["e"].shift(1)).dt.total_seconds() / 3600.0
    r["qr"] = r["rest"] < K.QUICK_RETURN_HOURS
    r["date"] = r["s"].dt.date
    tk = d["takers"].set_index("cad_login")["employee_no"]
    calls["emp"] = calls["call_taker"].map(tk)
    m = pd.merge_asof(calls.sort_values("t"), r[["employee_no", "s", "e", "qr", "rest", "shift"]].sort_values("s"),
                      left_on="t", right_on="s", left_by="emp", right_by="employee_no", direction="backward")
    m = m[m["t"] < m["e"]].copy()
    grads = set(d["takers"].loc[d["takers"]["academy_class"] != "", "cad_login"])
    m["graduate"] = m["call_taker"].isin(grads)
    m["after"] = m["t"].dt.date >= K.SPLIT
    m["month"] = list(zip(m["t"].dt.year, m["t"].dt.month))
    hi = m[m["acuity"].isin([1, 2])].copy()
    shifts = r[(r["date"] >= K.START) & (r["date"] <= K.END)].copy()
    shifts["after"] = shifts["date"] >= K.SPLIT
    return dict(d=d, calls=m, hi=hi, shifts=shifts, matched=len(m), answered=len(calls))


def rate(x):
    return 100.0 * x["under"].mean() if len(x) else float("nan")


def golden(target):
    F = frame(target)
    hi, sh = F["hi"], F["shifts"]
    b, a = hi[~hi["after"]], hi[hi["after"]]
    out = dict(F=F)
    out["before"], out["after"] = rate(b), rate(a)
    out["qr_share_before"] = 100.0 * sh.loc[~sh["after"], "qr"].mean()
    out["qr_share_after"] = 100.0 * sh.loc[sh["after"], "qr"].mean()
    out["after_qr"], out["after_rested"] = rate(a[a["qr"]]), rate(a[~a["qr"]])
    out["before_rested"] = rate(b[~b["qr"]])
    out["n_hi_before"], out["n_hi_after"] = len(b), len(a)
    out["monthly"] = {ym: rate(g) for ym, g in hi.groupby("month")}
    out["monthly_rested"] = {ym: rate(g[~g["qr"]]) for ym, g in hi.groupby("month")}
    out["monthly_qr"] = {ym: rate(g[g["qr"]]) for ym, g in hi.groupby("month")}
    out["cause"] = "quick_returns"
    return out


def rungs(target, G=None):
    """the readings a careful analyst takes on the way, each a figure the checks hold apart from the golden"""
    G = G or golden(target)
    hi = G["F"]["hi"]
    b, a = hi[~hi["after"]], hi[hi["after"]]
    ch = hi["protocol"].isin(K.RELEASE_CHANGED)
    vet = ~hi["graduate"]
    mix = b["protocol"].value_counts(normalize=True)
    std = sum(mix.get(pc, 0.0) * rate(a[a["protocol"] == pc]) for pc in mix.index)
    by_type = {t: (rate(b[b["shift"] == t]), rate(a[a["shift"] == t])) for t in ("Day", "Evening", "Night")}
    return dict(
        R0_step=(G["before"], G["after"]),
        Rp_changed=(rate(b[ch[b.index]]), rate(a[ch[a.index]])),
        Rp_unchanged=(rate(b[~ch[b.index]]), rate(a[~ch[a.index]])),
        Rg_veterans=(rate(b[vet[b.index]]), rate(a[vet[a.index]])),
        Rm_standardised=(G["before"], std),
        Rt_shift_type=by_type,
        Rd_rested=(G["before_rested"], G["after_rested"]),
        Rd_quick_return=(rate(b[b["qr"]]), G["after_qr"]),
    )
