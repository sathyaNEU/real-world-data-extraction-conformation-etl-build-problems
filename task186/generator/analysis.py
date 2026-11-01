"""Every rung, the golden and both asks, computed from target/ alone (no generator state).

Used by checks.py, golden.py, writeup.py and ceiling.py. verify.py recomputes on its own code path.
"""
import datetime as dt
import os
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import params as P

F = {
    "tip": "tip_events_20250701_20261130.csv",
    "library": "tip_library_catalogue_r1.xlsx",
    "logins": "ct_operator_logins.csv",
    "register": "screening_officer_register.xlsx",
    "roster": "lane_roster_20251201_20261130.csv",
    "leave": "hr_leave_taken_20251201_20261130.csv",
    "counts": "ct_unit_bag_counts_hourly_utc.csv",
    "units": "ct_unit_register.csv",
}
WIN0, WIN1 = P.WIN0, P.WIN1
MONTHS = [(2025, 12)] + [(2026, m) for m in range(1, 12)]
QUARTERS = [("Q1", dt.date(2025, 12, 1), dt.date(2026, 2, 28)), ("Q2", dt.date(2026, 3, 1), dt.date(2026, 5, 31)),
            ("Q3", dt.date(2026, 6, 1), dt.date(2026, 8, 31)), ("Q4", dt.date(2026, 9, 1), dt.date(2026, 11, 30))]
LIB_SHARE_CATS = ["GUN", "KNF", "IED", "OTH"]


# ------------------------------------------------------------------------------------------------ loading
def read_sheet(path, sheet, header_row_text):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    for i, r in enumerate(rows):
        if r and r[0] == header_row_text:
            hdr = [c for c in r if c is not None]
            body = [x[:len(hdr)] for x in rows[i + 1:] if x and x[0] is not None]
            return pd.DataFrame(body, columns=hdr)
    raise ValueError("header %s not found in %s" % (header_row_text, sheet))


def load(target):
    T = {}
    T["tip"] = pd.read_csv(os.path.join(target, F["tip"]), dtype={"image_no": str, "operator_login": str})
    lib = os.path.join(target, F["library"])
    T["images"] = read_sheet(lib, "Images", "image_no")
    T["objects"] = read_sheet(lib, "Objects", "object_code")
    T["logins"] = pd.read_csv(os.path.join(target, F["logins"]), dtype=str)
    T["register"] = read_sheet(os.path.join(target, F["register"]), "Officers", "staff_no")
    T["roster"] = pd.read_csv(os.path.join(target, F["roster"]), dtype=str)
    T["leave"] = pd.read_csv(os.path.join(target, F["leave"]), dtype={"payroll_no": str})
    T["counts"] = pd.read_csv(os.path.join(target, F["counts"]))
    T["units"] = pd.read_csv(os.path.join(target, F["units"]), dtype=str)
    return T


def population(T):
    reg = T["register"]
    return sorted(reg.loc[reg["endorsement_30_nov_2026"] == "Current", "staff_no"].tolist())


# ------------------------------------------------------------------------------------------------ main call
def tip_events(T, dedupe=True, local_window=True):
    tip = T["tip"].copy()
    if dedupe:
        tip = tip.drop_duplicates()
    tip["t_utc"] = pd.to_datetime(tip["event_utc"], utc=True)
    tip["t_local"] = tip["t_utc"].dt.tz_convert(P.TZ.key)
    tip["date"] = tip["t_local"].dt.date if local_window else tip["t_utc"].dt.date
    lg = T["logins"].set_index("login")["staff_no"]
    tip["staff_no"] = tip["operator_login"].map(lg)
    tip["image6"] = tip["image_no"].str.zfill(6)
    obj = T["images"].assign(image_no=lambda d: d["image_no"].astype(str).str.zfill(6)).set_index("image_no")["object_code"]
    tip["object_code"] = tip["image6"].map(obj)
    tip["hit"] = (tip["result"] == "HIT").astype(int)
    tip = tip.sort_values(["staff_no", "t_utc"], kind="mergesort")
    tip["prior_obj"] = tip.groupby(["staff_no", "object_code"]).cumcount()
    tip["prior_img"] = tip.groupby(["staff_no", "image6"]).cumcount()
    tip["in_window"] = (tip["date"] >= WIN0) & (tip["date"] <= WIN1)
    win = tip[tip["in_window"]].copy()
    win["prior_obj_win"] = win.groupby(["staff_no", "object_code"]).cumcount()
    tip = tip.join(win["prior_obj_win"])
    return tip


def logistic_at_zero(x, y, iters=40):
    """Fit P(hit) = 1/(1+exp(-(a + b x))) by Newton steps; return the fitted P at x = 0."""
    X = np.column_stack([np.ones_like(x, dtype=float), x.astype(float)])
    beta = np.zeros(2)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ beta))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + np.eye(2) * 1e-6
        g = X.T @ (y - p)
        step = np.linalg.solve(H, g)
        beta += step
        if np.abs(step).max() < 1e-10:
            break
    return 1.0 / (1.0 + np.exp(-beta[0]))


def officer_table(T, tip=None):
    if tip is None:
        tip = tip_events(T)
    pop = population(T)
    reg = T["register"].set_index("staff_no")
    lib_cat = T["images"].merge(T["objects"], on="object_code")
    cat_code = {"Firearms and parts": "GUN", "Knives and bladed items": "KNF",
                "Improvised explosive device components": "IED", "Other prohibited items": "OTH"}
    shares = T["objects"]["category"].map(cat_code).value_counts(normalize=True)
    rows = []
    for s in pop:
        a = tip[(tip["staff_no"] == s)]
        w = a[a["in_window"]]
        f = w[w["prior_obj"] == 0]
        fi = w[w["prior_img"] == 0]
        fw = w[w["prior_obj_win"] == 0]
        cat_bal = np.mean([w.loc[w["threat_category"] == c, "hit"].mean() for c in LIB_SHARE_CATS])
        cat_rw = sum(shares[c] * f.loc[f["threat_category"] == c, "hit"].mean() for c in LIB_SHARE_CATS)
        logit0 = logistic_at_zero(np.log1p(w["prior_obj"].values), w["hit"].values)
        rows.append(dict(staff_no=s, surname=reg.loc[s, "surname"], given=reg.loc[s, "given_name"],
                         employment=reg.loc[s, "employment"], checkpoint=reg.loc[s, "home_checkpoint"],
                         n=len(w), hits=int(w["hit"].sum()), overall=w["hit"].mean(),
                         n_first=len(f), first_hits=int(f["hit"].sum()), golden=f["hit"].mean(),
                         first_img=fi["hit"].mean(), first_winonly=fw["hit"].mean(), cat_bal=cat_bal,
                         cat_rw=cat_rw, logit0=logit0, repeat_share=1 - len(f) / len(w)))
    return pd.DataFrame(rows)


def designated(tab, col):
    return sorted(tab.loc[tab[col] < P.STANDARD, "staff_no"].tolist())


def main_call(T):
    tip = tip_events(T)
    tab = officer_table(T, tip)
    win = tip[tip["in_window"]]
    pooled = {k: float(win.loc[win["prior_obj"] == k, "hit"].mean()) for k in (0, 1, 2)}
    shares = {k: float((win["prior_obj"] == k).mean()) for k in (0, 1)}
    out = dict(table=tab, golden=designated(tab, "golden"), r0=designated(tab, "overall"),
               r1=designated(tab, "cat_bal"), r2=designated(tab, "first_img"), r2b=designated(tab, "first_winonly"),
               v_cat_rw=designated(tab, "cat_rw"), v_logit=designated(tab, "logit0"),
               pooled_hit_first=pooled[0], pooled_hit_repeat=float(win.loc[win["prior_obj"] > 0, "hit"].mean()),
               pooled_hit_k1=pooled[1], share_first=shares[0], n_window=len(win), n_events=len(tip))
    return out


# ------------------------------------------------------------------------------------------------ ask A
def to_min(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def xray_time(T, use_leave=True, mode="slot"):
    """Each officer's X-ray time per month, hours (the standard's equal share of the lane at each moment)."""
    ro = T["roster"].copy()
    ro["s"] = ro["start"].map(to_min)
    ro["e"] = ro["finish"].map(to_min)
    if use_leave:
        pay = T["register"].set_index("payroll_no")["staff_no"]
        lv = T["leave"]
        absent = set(zip(lv.loc[lv["leave_type"] == "Personal leave", "payroll_no"].map(pay),
                         lv.loc[lv["leave_type"] == "Personal leave", "leave_date"]))
        keep = [(a, b) not in absent for a, b in zip(ro["staff_no"], ro["roster_date"])]
        ro = ro[keep]
    hours = defaultdict(float)
    for (d, ln), g in ro.groupby(["roster_date", "lane"]):
        y, m = int(d[:4]), int(d[5:7])
        if mode == "nodiv":
            for s, a, b in zip(g["staff_no"], g["s"], g["e"]):
                hours[(s, (y, m))] += (b - a) / 60.0
            continue
        if mode == "blockkey":
            c = g.groupby(["s", "e"])["staff_no"].transform("count")
            for s, a, b, k in zip(g["staff_no"], g["s"], g["e"], c):
                hours[(s, (y, m))] += (b - a) / 60.0 / k
            continue
        pts = sorted(set(g["s"]).union(g["e"]))
        S, A, B = g["staff_no"].values, g["s"].values, g["e"].values
        for lo, hi in zip(pts[:-1], pts[1:]):
            on = (A <= lo) & (B >= hi)
            k = int(on.sum())
            if k:
                for s in S[on]:
                    hours[(s, (y, m))] += (hi - lo) / 60.0 / k
    return hours


def whole_month_population(T):
    reg = T["register"]
    out = {}
    for y, m in MONTHS:
        first = dt.date(y, m, 1)
        last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))
        ok = []
        for s, e, left in zip(reg["staff_no"], reg["xray_endorsed"], reg["left"]):
            e = e.date() if hasattr(e, "date") else e
            lf = left.date() if hasattr(left, "date") else left
            if e <= first and (lf is None or pd.isna(lf) or lf >= last):
                ok.append(s)
        out[(y, m)] = ok
    return out


def ask_a(T, use_leave=True, mode="slot"):
    hrs = xray_time(T, use_leave, mode)
    pop = whole_month_population(T)
    return [sum(1 for s in pop[mk] if hrs.get((s, mk), 0.0) < P.CURRENCY_H) for mk in MONTHS], hrs


# ------------------------------------------------------------------------------------------------ ask B
def lane_hours(T):
    """Local hours each lane was staffed on each date, from the roster (start hour of every hour touched)."""
    ro = T["roster"]
    out = defaultdict(set)
    first = {}
    for d, ln, a, b in zip(ro["roster_date"], ro["lane"], ro["start"], ro["finish"]):
        s, e = to_min(a), to_min(b)
        for h in range(s // 60, (e - 1) // 60 + 1):
            out[(d, ln)].add(h)
        first[(d, ln)] = min(first.get((d, ln), 99), s // 60)
    return out, first


def unit_lanes(T):
    """Which unit stood on each lane on each date: register location where the unit's counted hours fit that lane,
    otherwise the open lane its hours fit that no other unit covers (one unit to a lane each day)."""
    c = T["counts"].copy()
    c["t"] = pd.to_datetime(c["hour_start_utc"]).dt.tz_localize("UTC").dt.tz_convert(P.TZ.key)
    c["date"] = c["t"].dt.strftime("%Y-%m-%d")
    c["h"] = c["t"].dt.hour
    lh, first = lane_hours(T)
    reg = T["units"].set_index("unit_serial")
    commissioned = reg["commissioned"].to_dict()
    home = reg["location"].to_dict()
    days = sorted(set(d for d, _ in lh))
    act = c.groupby(["date", "unit_serial"])["h"].apply(set).to_dict()
    assign = {}
    for d in days:
        open_lanes = [ln for ln in P.LANES if (d, ln) in lh]
        units = sorted(u for (dd, u) in act if dd == d)

        def fits(u, ln):
            hrs = act[(d, u)]
            allowed = lh[(d, ln)] | {h for h in range(0, first[(d, ln)])}
            return hrs <= allowed and len(hrs & lh[(d, ln)]) > 0

        def jac(u, ln):
            a, b = act[(d, u)] & lh[(d, ln)], act[(d, u)] | lh[(d, ln)]
            return len(a) / len(b)
        taken, done = set(), set()
        for u in units:
            ln = home.get(u)
            if ln in open_lanes and commissioned.get(u, "9999") <= d and fits(u, ln):
                assign[(d, ln)] = u
                taken.add(ln)
                done.add(u)
        pairs = sorted(((jac(u, ln), u, ln) for u in units if u not in done for ln in open_lanes
                        if ln not in taken and fits(u, ln)), reverse=True)
        for sc, u, ln in pairs:
            if u in done or ln in taken:
                continue
            assign[(d, ln)] = u
            taken.add(ln)
            done.add(u)
    return assign, c, lh


def ask_b(T, mode="golden"):
    """Passenger bags each lane screened in each quarter (local quarters of the screening year)."""
    c = T["counts"].copy()
    if mode == "register_utc":
        c["date"] = pd.to_datetime(c["hour_start_utc"]).dt.date
        loc = T["units"].set_index("unit_serial")["location"]
        c["lane"] = c["unit_serial"].map(loc)
        c = c[c["lane"].isin(P.LANES)]
        res = {}
        for q, a, b in QUARTERS:
            m = (c["date"] >= a) & (c["date"] <= b)
            res.update({(ln, q): int(v) for ln, v in c[m].groupby("lane")["bags_imaged"].sum().items()})
        return res
    assign, c, lh = unit_lanes(T)
    c["d"] = pd.to_datetime(c["date"]).dt.date
    if mode in ("register", "register_open"):
        loc = T["units"].set_index("unit_serial")["location"]
        c["lane"] = c["unit_serial"].map(loc)
    else:
        inv = {(d, u): ln for (d, ln), u in assign.items()}
        c["lane"] = [inv.get((d, u)) for d, u in zip(c["date"], c["unit_serial"])]
    c = c[c["lane"].isin(P.LANES)]
    if mode in ("golden", "register_open"):
        keep = [h in lh.get((d, ln), set()) for d, ln, h in zip(c["date"], c["lane"], c["h"])]
        c = c[keep]
    res = {}
    for q, a, b in QUARTERS:
        m = (c["d"] >= a) & (c["d"] <= b)
        res.update({(ln, q): int(v) for ln, v in c[m].groupby("lane")["bags_imaged"].sum().items()})
    for ln in P.LANES:
        for q, _, _ in QUARTERS:
            res.setdefault((ln, q), 0)
    return res


def rnd_k(v):
    return int(np.floor(v / 1000.0 + 0.5)) * 1000
