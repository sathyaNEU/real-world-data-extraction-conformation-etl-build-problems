"""task170 calculations from the shipped bundle: the golden and every rung, read from the files in a target folder
only (deliver.py, checks.py and ceiling.py call these; verify.py has its own code path)."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import common as C

K = 96                                   # months of follow-up the curves are read over
PLATEAU = 60                             # the join curve's level at five years of service


def mi(d):
    return d.year * 12 + d.month - 1


def hires(target):
    """Every spell that started on or after 1 January 2019, with its start month, last payroll month and follow-up
    to the October 2026 payroll."""
    hr = pd.read_csv(os.path.join(target, "hr_employment_history_2019_2026.csv"), dtype=str, keep_default_na=False)
    start = [dt.date.fromisoformat(x) for x in hr["contract_start"]]
    end = [dt.date.fromisoformat(x) if x else None for x in hr["contract_end"]]
    last = C.mindex(C.LAST_PAYROLL)
    S = [mi(x) for x in start]
    E = [mi(x) if x else None for x in end]
    hr["s"] = S
    hr["e"] = pd.Series(E, dtype=object)
    hr["f"] = [(min(e, last) if e is not None else last) - s + 1 for s, e in zip(S, E)]
    hr["left_k"] = pd.Series([(e - s + 1) if (e is not None and e <= last) else None for s, e in zip(S, E)], dtype=object)
    return hr


def id_map(hr):
    m = dict(zip(hr["legacy_employee_no"], hr["employee_no"]))
    m.update({e: e for e in hr["employee_no"]})
    return m


def spell_of(hr_by_emp, emp, month):
    for s, e, idx in hr_by_emp.get(emp, []):
        if s <= month and (e is None or month <= e):
            return idx
    return None


def joins(target, hr):
    """Each membership's first contribution month, placed on the spell it was made in."""
    reg = pd.read_excel(os.path.join(target, "ledstrand_member_register_2026-10.xlsx"), dtype={"employer_ref": str})
    idm = id_map(hr)
    by_emp = {}
    for idx, (emp, s, e) in enumerate(zip(hr["employee_no"], hr["s"], hr["e"])):
        by_emp.setdefault(emp, []).append((s, None if e is None or e != e else int(e), idx))
    out = {}
    rate = {}
    for ref, joined, r0 in zip(reg["employer_ref"], reg["joined"], reg["rate_at_join_pct"]):
        emp = idm.get(ref)
        jm = mi(pd.Timestamp(joined).date())
        idx = spell_of(by_emp, emp, jm)
        if idx is not None:
            out[idx] = jm
            rate[idx] = int(r0)
    return out, rate


def ipc_cancels(target, hr):
    """Each auto-enrolled policy's first payroll without a premium, from the date the cancellation was received."""
    ipc = pd.read_csv(os.path.join(target, "tarnmark_ipc_bordereau_2019_2026.csv"), dtype=str, keep_default_na=False)
    ipc = ipc[ipc["basis"] == "Auto"]
    idm = id_map(hr)
    by_emp = {}
    for idx, (emp, s, e) in enumerate(zip(hr["employee_no"], hr["s"], hr["e"])):
        by_emp.setdefault(emp, []).append((s, None if e is None or e != e else int(e), idx))
    out = {}
    for ref, start, recv in zip(ipc["employer_ref"], ipc["cover_start"], ipc["cancellation_received"]):
        emp = idm.get(ref)
        idx = spell_of(by_emp, emp, mi(dt.date.fromisoformat(start)))
        if idx is None:
            continue
        if recv:
            d = dt.date.fromisoformat(recv)
            out[idx] = mi(d) + (1 if d.day > C.CUTOFF_DAY else 0)
    return out


def km_incidence(event_k, follow):
    """Cumulative incidence of an event by payroll month k (1 to K) with follow-up censoring (Kaplan-Meier)."""
    ev = np.array([k if k is not None else 10 ** 6 for k in event_k])
    fu = np.array(follow)
    S, out = 1.0, []
    for k in range(1, K + 1):
        risk = (fu >= k) & (ev >= k)
        d = ((ev == k) & (fu >= k)).sum()
        n = risk.sum()
        S *= (1 - d / n) if n else 1.0
        out.append(1 - S)
    return np.array(out)


def on_payroll(hr):
    """P(still on the payroll in month k), k = 1 to K, from the hires' leaving months (Kaplan-Meier)."""
    ev = np.array([k if (k is not None and k == k) else 10 ** 6 for k in hr["left_k"]])
    fu = np.array(hr["f"])
    S, out = 1.0, [1.0]
    for k in range(1, K):
        risk = (fu >= k) & (ev >= k)
        d = ((ev == k) & (fu >= k)).sum()
        n = risk.sum()
        S *= (1 - d / n) if n else 1.0
        out.append(S)
    return np.array(out)


def plan(target):
    p = pd.read_excel(os.path.join(target, "vch_hiring_plan_2027.xlsx"), sheet_name="Requisitions")
    p = p.copy()
    p["month"] = pd.to_datetime(p["planned_start"]).dt.month
    p["pay"] = [C.SCALE_2027[g] * float(f) for g, f in zip(p["grade"], p["fte"])]
    return p


def curves(target, plateau=PLATEAU):
    hr = hires(target)
    h = hr[hr["s"] >= C.mindex(C.HIST_START)].reset_index(drop=True)
    h["e"] = h["e"].astype(object).where(h["e"].notna(), None)
    h["left_k"] = h["left_k"].astype(object).where(h["left_k"].notna(), None)
    jm, rate = joins(target, h)
    jk = [(jm[i] - s + 1) if i in jm else None for i, s in enumerate(h["s"])]
    Cj = km_incidence(jk, h["f"])
    cm = ipc_cancels(target, h)
    ck = [(cm[i] - s + 1) if i in cm else None for i, s in enumerate(h["s"])]
    G = km_incidence(ck, h["f"])
    Se = on_payroll(h)
    mb = float(np.mean([C.match_pct(r) for r in rate.values()])) / 100
    return dict(hires=h, C=Cj, p=float(Cj[plateau - 1]), G=G, q=float(G[plateau - 1]), Se=Se, mb=mb,
                n_hires=len(h), n_joins=len(jm))


def forecast(target, cv=None, mode="golden", P=None):
    """The FY2027 match on the 2027 intake by hospital, and the intake contributing on the December 2027 payroll."""
    cv = cv or curves(target)
    P = plan(target) if P is None else P
    Cj, p, G, q, Se, mb = cv["C"], cv["p"], cv["G"], cv["q"], cv["Se"], cv["mb"]
    d = C.DEFAULT_RATE / 100
    by = {h: 0.0 for h in C.H_CODES}
    heads = {h: 0.0 for h in C.H_CODES}
    staff = {h: 0.0 for h in C.H_CODES}
    for hosp, m, pay in zip(P["hospital"], P["month"], P["pay"]):
        for k in range(1, 14 - int(m)):
            i = k - 1
            if mode == "golden":
                A = Cj[i] / p
                s, hd = (1 - A) * d + Cj[i] * cv["mb"], (1 - A) + Cj[i]
            elif mode == "ipc_clock":
                A = G[i] / q
                s, hd = (1 - A) * d + A * p * mb, (1 - A) + A * p
            elif mode == "ipc_carry":            # the cover's cancellations as the plan's opt-outs, all others at 3
                s, hd = (1 - G[i]) * d, 1 - G[i]
            elif mode == "ipc_carry_joiners":    # the same, with the opt-in record's joiners at their own rates
                s, hd = (1 - G[i] - Cj[i]) * d + Cj[i] * mb, 1 - G[i]
            elif mode == "joined_as_chosen":     # the join curve read as the share who have chosen
                s, hd = (1 - Cj[i]) * d + Cj[i] * p * mb, (1 - Cj[i]) + Cj[i] * p
            elif mode == "preference":           # only those who prefer to save, at their own rates, from month 1
                s, hd = p * mb, p
            elif mode == "preference_default":   # those who prefer to save, all at 3
                s, hd = p * d, p
            elif mode == "opt_in":               # the opt-in record replayed
                s, hd = Cj[i] * mb, Cj[i]
            elif mode == "nobody_leaves":        # every hire stays at 3 for the year
                s, hd = d, 1.0
            else:
                raise ValueError(mode)
            by[hosp] += Se[i] * pay * s
            if k == 13 - int(m):
                heads[hosp] += Se[i] * hd
                staff[hosp] += Se[i]
    return dict(by=by, total=sum(by.values()), heads=heads, staff=staff,
                heads_total=sum(heads.values()), staff_total=sum(staff.values()))


def golden(target):
    cv = curves(target)
    P = plan(target)
    F = forecast(target, cv, "golden", P)
    F.update(cv=cv, P=P, chosen={k: float(cv["C"][k - 1] / cv["p"]) for k in (1, 3, 6, 12)})
    return F


# ---------------------------------------------------------------------------------------------------- the asks
def deductions(target):
    return pd.read_csv(os.path.join(target, "payroll_deductions_2025-11_2026-10.csv"), dtype=str, keep_default_na=False)


def match_paid_2026(target, mode="golden", ded=None):
    """Ask A: the employer's match paid on the January to October 2026 payrolls, by hospital."""
    d = deductions(target) if ded is None else ded
    d = d[(d["code"] == "ERM") & (d["payroll"] >= "202601") & (d["payroll"] <= "202610")].copy()
    d["amt"] = d["amount"].astype(float)
    d["hosp"] = d["cost_centre"].str[:3]
    if mode == "golden":            # the person's match is written on each assignment's line: count it once
        d = d.drop_duplicates(["payroll", "run", "employee_ref"])
    elif mode == "lines":           # every ERM line summed
        pass
    elif mode == "main_only":       # the first run only, deduplicated
        d = d[d["run"] == "MAIN"].drop_duplicates(["payroll", "run", "employee_ref"])
    elif mode == "no_negatives":    # reversal lines dropped, deduplicated
        d = d[d["amt"] >= 0].drop_duplicates(["payroll", "run", "employee_ref"])
    elif mode == "main_assignment": # assignment 1 lines only
        d = d[d["assignment"] == "1"]
    else:
        raise ValueError(mode)
    g = d.groupby("hosp")["amt"].sum()
    return {h: float(g.get(h, 0.0)) for h in C.H_CODES}


def members_pre2019(target, mode="golden", ded=None):
    """Ask B: members whose membership began before 1 January 2019 and who were still active members on 1 November
    2026, by the hospital that paid them on the October 2026 payroll."""
    reg = pd.read_excel(os.path.join(target, "ledstrand_member_register_2026-10.xlsx"), dtype={"employer_ref": str})
    hr = pd.read_csv(os.path.join(target, "hr_employment_history_2019_2026.csv"), dtype=str, keep_default_na=False)
    idm = dict(zip(hr["legacy_employee_no"], hr["employee_no"]))
    idm.update({e: e for e in hr["employee_no"]})
    reg["joined_d"] = pd.to_datetime(reg["joined"]).dt.date
    reg["emp"] = reg["employer_ref"].map(idm)
    if mode == "anchor_first":      # the member number's first membership read as the start
        first = reg.groupby("member_no")["joined_d"].transform("min")
        sel = reg[(first < dt.date(2019, 1, 1)) & (reg["status"] == "Active")]
    else:
        sel = reg[(reg["joined_d"] < dt.date(2019, 1, 1)) & (reg["status"] == "Active")]
    if mode in ("golden", "anchor_first"):
        open_ = hr[hr["contract_end"] == ""]
        in_post = set(open_["employee_no"])
        sel = sel[sel["emp"].isin(in_post)]
        d = deductions(target) if ded is None else ded
        octo = d[(d["payroll"] == "202610") & (d["assignment"] == "1")].drop_duplicates("employee_ref")
        hosp = dict(zip(octo["employee_ref"], octo["cost_centre"].str[:3]))
        g = sel["emp"].map(hosp).value_counts()
    elif mode == "register":        # the register's Active rows by the hospital they joined at
        g = sel["hospital_at_join"].replace({"LRC": "LDM"}).value_counts()
    else:
        raise ValueError(mode)
    return {h: int(g.get(h, 0)) for h in C.H_CODES}
