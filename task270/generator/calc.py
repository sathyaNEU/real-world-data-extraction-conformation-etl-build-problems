"""The golden computation, read from the pack as a solver reads it: every pre-July pseudonym carried through the
crosswalk, the year-end lists for the population, each patient's 2026 proportion of days covered as the
specification defines it, and each network's share under 80 per cent over the population the specification files,
with every route the ladder names."""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np
import openpyxl
import pandas as pd

from common import BANK_HOLIDAYS, BORN_BY, NETWORK_NAME, PDC_LINE, TARGET, TIER_LINE, YEAR_END, YEAR_START
import records as R

DAY0 = YEAR_START.toordinal()
NDAYS = (YEAR_END - YEAR_START).days + 1


def tablets_a_day(text):
    t = text.upper()
    if t.startswith("TWO") or re.match(r"^(TAKE )?2\b", t) or "TAKE TWO" in t:
        return 2.0
    return 1.0


def load(target=TARGET):
    D = pd.read_csv(os.path.join(target, R.F_DISP), dtype=str)
    D["quantity"] = D["quantity"].astype(int)
    X = pd.read_csv(os.path.join(target, R.F_XWALK), dtype=str)
    xmap = dict(zip(X["old_pseudonym"], X["new_pseudonym"]))
    D["patient"] = D["patient_pseudonym"].map(lambda k: xmap.get(k, k))
    D["date"] = pd.to_datetime(D["dispensed_date"]).dt.date
    D["tpd"] = D["dosage_instructions"].map(tablets_a_day)
    D["days"] = (D["quantity"] / D["tpd"]).round().astype(int)
    Q = pd.read_csv(os.path.join(target, R.F_QUARVIS), dtype=str).fillna("")
    wb = openpyxl.load_workbook(os.path.join(target, R.F_SYNARIS), read_only=True)
    ws = wb["Lipid cohort"]
    rows = list(ws.iter_rows(values_only=True))
    T = pd.DataFrame(rows[1:], columns=rows[0])
    P = pd.read_csv(os.path.join(target, R.F_PRACTICES), dtype=str).fillna("")
    net = {r.practice_ods: r.network.replace(" PCN", "") for r in P.itertuples() if r.member_to == ""}
    pop = []
    for r in Q.itertuples():
        pop.append(dict(patient=r.nhs_pseudo, practice=r.practice_ods, yob=int(r.yob), system="Q",
                        care_home=r.care_home_since != "", coded_aid=r.mds_since != ""))
    for r in T.itertuples(index=False):
        pop.append(dict(patient=r[0], practice=r[1], yob=int(r[2]), system="T",
                        care_home=str(r[4]).startswith("Care home"), coded_aid=False))
    pop = pd.DataFrame(pop)
    name_to_code = {v: k for k, v in NETWORK_NAME.items()}
    pop["network"] = pop["practice"].map(lambda p: name_to_code[net[p]])
    return D, pop


def pdc_of(items):
    """Specification 2.2: from the first 2026 item to 31 December, each item's days from its quantity and dosage,
    an overlap moved to start when the earlier supply ends, any statin."""
    items = sorted(items)
    first = items[0][0]
    cov = np.zeros(NDAYS + 800, bool)
    nxt = 0
    for d, n in items:
        st = max(d, nxt)
        cov[st:st + n] = True
        nxt = st + n
    return cov[first:NDAYS].sum() / (NDAYS - first)


def periodic(dates, tol=1, need=0.9):
    """A fixed cycle: the steps between items equal one period (7, 14 or 28 days) to within tol on need of them."""
    ds = sorted(set(dates))
    if len(ds) < 5:
        return False
    g = np.diff(ds)
    med = float(np.median(g))
    step = min((7, 14, 28), key=lambda s: abs(s - med))
    return float(np.mean(np.abs(g - step) <= tol)) >= need


def _closed(d):
    return d.weekday() == 6 or d in BANK_HOLIDAYS


def same_weekday(dates):
    """Every item on one weekday, an item due on a Sunday or bank holiday supplied on the next day the pharmacy opens
    (the compliance-aid guidance's supply)."""
    ds = sorted(set(dates))
    for w in range(7):
        ok = True
        for d in ds:
            k = (d.weekday() - w) % 7
            if k and not (k <= 3 and all(_closed(d - dt.timedelta(days=j)) for j in range(1, k + 1))):
                ok = False
                break
        if ok:
            return True
    return False


def patient_table(target=TARGET):
    D, pop = load(target)
    y = D[(D["date"] >= YEAR_START) & (D["date"] <= YEAR_END)].copy()
    y["d"] = y["date"].map(lambda x: x.toordinal() - DAY0)
    grp = {k: list(zip(g["d"], g["days"])) for k, g in y.groupby("patient")}
    weekly = set(y.loc[y["days"] == 7, "patient"])
    out = pop.copy()
    out["n_items"] = out["patient"].map(lambda k: len(grp.get(k, [])))
    out["pdc"] = out["patient"].map(lambda k: pdc_of(grp[k]) if len(grp.get(k, [])) >= 2 else np.nan)
    out["weekly_items"] = out["patient"].isin(weekly)
    for tol, need, col in ((0, 0.9, "cyc0"), (1, 0.9, "cyc1"), (2, 0.9, "cyc2"), (3, 0.8, "cyc3")):
        out[col] = out["patient"].map(lambda k, t=tol, n=need: periodic([d for d, _ in grp.get(k, [])], t, n))
    dates = {k: list(g["date"]) for k, g in y.groupby("patient")}
    out["weekday"] = out["patient"].map(lambda k: len(set(dates.get(k, []))) >= 5 and same_weekday(dates[k]))
    for col in ("cyc2", "cyc3"):
        out[col + "w"] = out[col] & out["weekday"]
    out["aged65"] = out["yob"] <= BORN_BY
    out["eligible_base"] = out["aged65"] & (out["n_items"] >= 2)
    return out


ROUTES = {
    "R0": "every patient aged 65 and over with two or more 2026 items",
    "R1": "care home residents out",
    "R2": "care home residents and coded compliance-aid patients out",
    "R3": "care home residents and patients with weekly 7-day items out",
    "R4": "care home residents and full cover (99 per cent or more) out",
    "G": "care home residents and every fixed-cycle patient out, coded or not",
}


def route_mask(T, route, cyc="cyc1"):
    m = T["eligible_base"].copy()
    if route == "R0":
        return m
    m &= ~T["care_home"]
    if route == "R1":
        return m
    if route == "R2":
        return m & ~T["coded_aid"]
    if route == "R3":
        return m & ~T["weekly_items"]
    if route == "R4":
        return m & ~(T["pdc"] >= 0.99)
    if route == "G":
        return m & ~T[cyc] & ~T["coded_aid"]
    raise KeyError(route)


def shares(T, mask):
    out = {}
    for code in NETWORK_NAME:
        s = T[mask & (T["network"] == code)]
        out[code] = dict(n=int(len(s)), low=int((s["pdc"] < PDC_LINE).sum()),
                         share=float((s["pdc"] < PDC_LINE).mean()) if len(s) else float("nan"))
    return out


def tier(sh):
    return sorted(c for c, v in sh.items() if v["share"] >= TIER_LINE)
