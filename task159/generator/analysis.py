"""Every rung, the golden and every ask figure, computed from target/ alone (no generator state)."""
import csv
import datetime as dt
import math
import os
import re

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.stats import norm

TROY = 31.1034768
NEW_CUT, OLD_CUT = 0.90, 0.50


def _csv(path, skip_hash=False):
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if not (skip_hash and l.startswith("#"))]
    return pd.DataFrame(list(csv.DictReader(lines)))


# ---------------------------------------------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------------------------------------------

def grid(target):
    txt = open(os.path.join(target, "kessock_mine_grid_control.txt"), encoding="utf-8").read()
    e0 = float(re.search(r"E\(UTM\) = ([\d.]+)", txt).group(1))
    n0 = float(re.search(r"N\(UTM\) = ([\d.]+)", txt).group(1))
    a = float(re.search(r"a = ([\d.]+) degrees", txt).group(1))
    k = float(re.search(r"k = ([\d.]+)", txt).group(1))
    return e0, n0, a, k


def utm_to_kmg(e, n, g):
    e0, n0, a, k = g
    th = math.radians(a)
    de, dn = np.asarray(e, float) - e0, np.asarray(n, float) - n0
    dx = de * math.cos(th) - dn * math.sin(th)
    dy = de * math.sin(th) + dn * math.cos(th)
    return 10000.0 + dx / k, 20000.0 + dy / k


def au_gpt(ppb, grav, bdl="half"):
    out = []
    for p_, g_ in zip(ppb, grav):
        p_ = p_.strip()
        if p_.startswith(">"):
            out.append(float(g_))
        elif p_.startswith("<"):
            dl = float(p_[1:]) / 1000.0
            out.append({"half": dl / 2, "zero": 0.0, "dl": dl}[bdl])
        else:
            out.append(float(p_) / 1000.0)
    return np.array(out)


def blast_holes(target, bdl="half", with_dups=False, grav="use"):
    lims = _csv(os.path.join(target, "gc_assays_lims_export_20261105.csv"))
    types = {"BH", "BLASTHOLE"} | ({"DUP", "FIELD DUP"} if with_dups else set())
    h = lims[lims["SAMPLE_TYPE"].isin(types)].copy()
    gr = h["AU_GRAV_GPT"] if grav == "use" else pd.Series(["10.0"] * len(h), index=h.index)
    h["au"] = au_gpt(h["AU_PPB"], gr, bdl)
    x, y = utm_to_kmg(h["EASTING_UTM17"].astype(float), h["NORTHING_UTM17"].astype(float), grid(target))
    i = np.floor((x - 10000.0) / 10.0).astype(int)
    j = np.floor((y - 20000.0) / 10.0).astype(int)
    k = ((1300 - 5 - h["BENCH"].astype(int)) // 5).astype(int)
    h["ijk"] = i * 10000 + j * 100 + k
    return h


def model(target):
    m = _csv(os.path.join(target, "kl_mz_resource_model_2026R.csv"), skip_hash=True)
    m["ijk"] = m["IJK"].astype(int)
    m["au"] = m["AU_OK"].astype(float)
    m["t"] = m["DENSITY"].astype(float) * 500.0
    return m.set_index("ijk")


def paired(target, **kw):
    h = blast_holes(target, **kw)
    gc = h.groupby("ijk")["au"].mean()
    m = model(target)
    p = m.join(gc.rename("gc"), how="inner")
    return p


def plan(target):
    wb = load_workbook(os.path.join(target, "kessock_mine_plan_2027_v3.xlsx"), read_only=True, data_only=True)
    ws = wb["Schedule"]
    rows = list(ws.iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["au"] = df["AU_OK"].astype(float)
    df["t"] = df["TONNES"].astype(float)
    return df


# ---------------------------------------------------------------------------------------------------------------
# Main call
# ---------------------------------------------------------------------------------------------------------------

def oz(t, g):
    return float(np.sum(np.asarray(t) * np.asarray(g))) / TROY


def factor(p, c):
    """Grade control's gold over the model's gold, each side cut at c on its own grade."""
    gsel, msel = p["gc"] >= c, p["au"] >= c
    return oz(p["t"][gsel], p["gc"][gsel]) / oz(p["t"][msel], p["au"][msel])


def route_A(p, pl, c=NEW_CUT):
    sel = pl["au"] >= c
    return oz(pl["t"][sel], pl["au"][sel]) * factor(p, c)


def route_A_tonnes(p, pl, c=NEW_CUT):
    tf = p["t"][p["gc"] >= c].sum() / p["t"][p["au"] >= c].sum()
    return pl["t"][pl["au"] >= c].sum() * tf


def _ratios(p):
    r = (p["gc"] / p["au"]).values
    return r / r.mean()          # the record's grade-control-to-model ratios, centred so the model is right on average


def route_D(p, pl, c=NEW_CUT, centred=True):
    """Each scheduled block's expected grade-control gold above c: its model grade times every ratio the record holds."""
    r = _ratios(p) if centred else (p["gc"] / p["au"]).values
    mf, tf = pl["au"].values, pl["t"].values
    au_sum, t_sum = 0.0, 0.0
    for i in range(0, len(mf), 1500):
        G = mf[i:i + 1500, None] * r[None, :]
        au_sum += float(np.sum(tf[i:i + 1500] * (G * (G >= c)).mean(axis=1)))
        t_sum += float(np.sum(tf[i:i + 1500] * (G >= c).mean(axis=1)))
    return au_sum / TROY, t_sum


def route_C(p, pl, c=NEW_CUT):
    """The same with the ratios read as log-normal (their log standard deviation)."""
    s = float(np.log(p["gc"] / p["au"]).std())
    mf, tf = pl["au"].values, pl["t"].values
    au = float(np.sum(tf * mf * norm.cdf((np.log(mf / c) + s * s / 2) / s))) / TROY
    t = float(np.sum(tf * norm.cdf((np.log(mf / c) - s * s / 2) / s)))
    return au, t, s


def route_B(p, pl, c=NEW_CUT, width=0.1):
    """Binned conditional means: the record's blocks grouped by the log of their model grade."""
    edges = np.arange(-7, 3.0001, width)
    bh, bf = np.digitize(np.log(p["au"].values), edges), np.digitize(np.log(pl["au"].values), edges)
    g = p["gc"].values
    n = len(edges) + 1
    num = np.bincount(bh, weights=g * (g >= c), minlength=n)
    numt = np.bincount(bh, weights=(g >= c) * 1.0, minlength=n)
    den = np.bincount(bh, minlength=n)
    with np.errstate(invalid="ignore", divide="ignore"):
        e_au, e_t = num / den, numt / den
    tf = pl["t"].values
    a, t = e_au[bf], e_t[bf]
    miss = np.isnan(a)
    a[miss] = pl["au"].values[miss] * (pl["au"].values[miss] >= c)
    t[miss] = (pl["au"].values[miss] >= c) * 1.0
    return float(np.sum(tf * a)) / TROY, float(np.sum(tf * t))


def main_call(target, **kw):
    p = paired(target, **kw)
    pl = plan(target)
    msel = pl["au"] >= NEW_CUT
    plan_oz = oz(pl["t"][msel], pl["au"][msel])
    plan_t = float(pl["t"][msel].sum())
    f05, f09 = factor(p, OLD_CUT), factor(p, NEW_CUT)
    sel = p["au"] >= NEW_CUT
    calib = oz(p["t"][sel], p["gc"][sel]) / oz(p["t"][sel], p["au"][sel])
    D_oz, D_t = route_D(p, pl)
    C_oz, C_t, s = route_C(p, pl)
    B = {w: route_B(p, pl, width=w) for w in (0.05, 0.1, 0.2)}
    res = dict(plan_oz=plan_oz, plan_t=plan_t, f05=f05, f09=f09, calib=calib, s=s,
               R0=plan_oz, R1=plan_oz * f05, R2=plan_oz * calib,
               A=route_A(p, pl), A_t=route_A_tonnes(p, pl), D=D_oz, D_t=D_t, C=C_oz, C_t=C_t,
               B05=B[0.05][0], B10=B[0.1][0], B20=B[0.2][0], B05_t=B[0.05][1], B10_t=B[0.1][1], B20_t=B[0.2][1],
               n_pairs=len(p), n_plan=len(pl))
    res["golden"] = res["D"]
    res["golden_t"] = res["D_t"]
    return res


# ---------------------------------------------------------------------------------------------------------------
# Asks
# ---------------------------------------------------------------------------------------------------------------

def _dst(y):
    a = dt.datetime(y, 3, 8)
    while a.weekday() != 6:
        a += dt.timedelta(days=1)
    b = dt.datetime(y, 11, 1)
    while b.weekday() != 6:
        b += dt.timedelta(days=1)
    return a.replace(hour=2), b.replace(hour=2)


def utc_to_local(u):
    loc = u - dt.timedelta(hours=5)
    a, b = _dst(loc.year)
    if a <= loc < b:
        loc = u - dt.timedelta(hours=4)
    return loc


def fleet(target):
    wb = load_workbook(os.path.join(target, "haul_fleet_register_2026-10.xlsx"), read_only=True, data_only=True)
    units = []
    for sheet in ("Fleet", "Disposals"):
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = rows[0]
        for r in rows[1:]:
            d = dict(zip(hdr, r))
            if not str(d["UNIT"]).startswith("T-"):
                continue
            ins = d["IN_SERVICE"].date() if hasattr(d["IN_SERVICE"], "date") else d["IN_SERVICE"]
            out = d.get("DISPOSED")
            out = (out.date() if hasattr(out, "date") else out) if out else dt.date(2099, 1, 1)
            units.append((d["UNIT"], float(d["NOMINAL_PAYLOAD_T"]), ins, out, sheet))
    return units


def stockpile(target, dedup=True, asof=True, local=True):
    d = _csv(os.path.join(target, "dispatch_loads_to_lgsp_2023-2026.csv"))
    d["u"] = pd.to_datetime(d["TIME_UTC"].str.replace("Z", ""), format="%Y-%m-%dT%H:%M:%S")
    d["t"] = [utc_to_local(x.to_pydatetime()) for x in d["u"]] if local else [x.to_pydatetime() for x in d["u"]]
    d["g"] = d["SOURCE_AU_GPT"].astype(float)
    if dedup:
        d = d.sort_values(["TRUCK", "u"]).reset_index(drop=True)
        prev_t = d.groupby("TRUCK")["u"].shift(1)
        prev_s = d.groupby("TRUCK")["SOURCE"].shift(1)
        gap = (d["u"] - prev_t).dt.total_seconds() / 60.0
        dupe = (gap < 10) & (prev_s == d["SOURCE"])
        d = d[~dupe.fillna(False)]
    units = fleet(target)
    pay = []
    for no, t in zip(d["TRUCK"], d["t"]):
        day = t.date()
        if asof:
            c = [u[1] for u in units if u[0] == no and u[2] <= day < u[3]]
        else:
            c = [u[1] for u in units if u[0] == no and u[4] == "Fleet"]
        pay.append(c[0] if c else np.nan)
    d["pay"] = pay
    inv = _csv(os.path.join(target, "stockpile_inventory_2022-12-31.csv"))
    row = inv[inv["STOCKPILE"].str.startswith("LGSP")].iloc[0]
    t0 = float(row["TONNES"].replace(",", ""))
    au0 = t0 * float(row["AU_GPT"])
    out = {}
    for label, end in (("2023", dt.datetime(2024, 1, 1)), ("2024", dt.datetime(2025, 1, 1)),
                       ("2025", dt.datetime(2026, 1, 1)), ("2026-10", dt.datetime(2026, 11, 1))):
        s = d[d["t"] < end]
        out[label] = (t0 + s["pay"].sum(), (au0 + (s["pay"] * s["g"]).sum()) / TROY)
    return out


def _quarters():
    q = []
    for y in (2025, 2026):
        for k in range(4):
            a = dt.datetime(y, 3 * k + 1, 1)
            b = dt.datetime(y + (1 if k == 3 else 0), (3 * k + 4) if k < 3 else 1, 1)
            if a >= dt.datetime(2026, 10, 1):
                continue
            q.append(("%d Q%d" % (y, k + 1), a, b))
    return q


def mill_hours(target, use_cmms=True, tags="both", local=True, dedup=True):
    e = _csv(os.path.join(target, "dcs_event_export_grinding_2025-2026.csv"))
    names = {"both": ("BM101.RUNNING", "GRD.BM01.RUN_STS"), "old": ("BM101.RUNNING",), "new": ("GRD.BM01.RUN_STS",)}[tags]
    e = e[e["TAG"].isin(names)].copy()
    if dedup:
        e = e.drop_duplicates()
    e["u"] = pd.to_datetime(e["TIME_UTC"], format="%Y-%m-%d %H:%M:%S")
    e = e.sort_values(["u"], kind="stable")
    conv = (lambda x: utc_to_local(x)) if local else (lambda x: x - dt.timedelta(hours=5))
    start = conv(dt.datetime(2025, 1, 1, 5, 0))
    end = conv(dt.datetime(2026, 11, 1, 4, 0))
    down, state, since = [], None, None
    for t, v in zip(e["u"], e["VALUE"].astype(int)):
        t = conv(t.to_pydatetime())
        if state is None:
            state, since = v, t
            continue
        if v == state:
            continue
        if state == 0:
            down.append((since, t))
        state, since = v, t
    if state == 0:
        down.append((since, end))
    if use_cmms:
        w = _csv(os.path.join(target, "cmms_work_orders_grinding_2025-2026.csv"))
        w = w[w["WO_TYPE"] == "SD"]
        for a, b in zip(w["ACTUAL_START"], w["ACTUAL_FINISH"]):
            down.append((dt.datetime.strptime(a, "%Y-%m-%d %H:%M"), dt.datetime.strptime(b, "%Y-%m-%d %H:%M")))
    # union of downtime
    down.sort()
    merged = []
    for a, b in down:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    out = {}
    for label, a, b in _quarters():
        tot = (b - a).total_seconds() / 3600.0
        dn = sum(max(0.0, (min(b, y) - max(a, x)).total_seconds() / 3600.0) for x, y in merged)
        out[label] = tot - dn
    return out


def fine_gold(target, allocate=True, by="pour"):
    bars = _csv(os.path.join(target, "goldroom_bar_register_2025-2026.csv"))
    bars["seq"] = bars["BAR_NO"].str.split("-").str[1].astype(int)
    bars["day"] = pd.to_datetime(bars["POUR_DATE"]).dt.date
    bars["gross"] = bars["GROSS_OZT"].astype(float)
    ref = _csv(os.path.join(target, "refinery_outturn_statements_2025-2026.csv"))
    ref["seq"] = ref["CLIENT_REF"].str.replace("KL", "").str.strip().astype(int)
    ref["rec"] = pd.to_datetime(ref["RECEIVED_DATE"]).dt.date
    ref["stmt"] = pd.to_datetime(ref["STATEMENT_DATE"]).dt.date
    match = []
    for s, rec in zip(ref["seq"], ref["rec"]):
        c = bars[(bars["seq"] == s) & (bars["day"] <= rec) & (bars["day"] >= rec - dt.timedelta(days=60))]
        match.append(c.index[0] if len(c) else -1)
    ref["bar"] = match
    ref["gross"] = [bars.loc[b, "gross"] if b >= 0 else np.nan for b in ref["bar"]]
    ref["lot_fine"] = ref["LOT_FINE_AU_OZT"].astype(float)
    if allocate:
        ref["fine"] = ref["lot_fine"] * ref["gross"] / ref.groupby("LOT_NO")["gross"].transform("sum")
    else:
        ref["fine"] = ref["lot_fine"]
    ref["day"] = [bars.loc[b, "day"] if b >= 0 else None for b in ref["bar"]]
    out = {}
    for label, a, b in _quarters():
        key = ref["day"] if by == "pour" else ref["stmt"]
        sel = [(x is not None) and (a.date() <= x < b.date()) for x in key]
        out[label] = float(ref.loc[sel, "fine"].sum())
    return out


def compute(target):
    r = dict(main=main_call(target))
    r["stockpile"] = stockpile(target)
    r["hours"] = mill_hours(target)
    r["fine"] = fine_gold(target)
    return r
