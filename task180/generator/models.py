"""The main call, computed from the shipped files only: each plant's earthquakes of ML 1.0 or more within 5 km of an
injection well's open hole by local quarter, the injected volume from the hourly telemetry, and the 2027 forecast
each rung of the ladder makes from them."""
import json
import os
import re
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

import geo as G
import records as R
import world as W

QUIET = (23.5, 5.0)                 # local hours the town stations record every earthquake above ML 0.6
SHARE = (24 - QUIET[0] + QUIET[1]) / 24.0


def epoch(x):
    """UTC seconds (float) from ISO strings or a datetime series, whatever the stored resolution."""
    ts = pd.to_datetime(x, utc=True)
    return ((ts - pd.Timestamp(0, tz="UTC")) / pd.Timedelta(seconds=1)).to_numpy(dtype=float)


def load(target):
    cat = pd.read_csv(os.path.join(target, R.CAT))
    cat["t"] = epoch(cat["origin_time_utc"])
    wells = pd.read_csv(os.path.join(target, R.WELL_REG))
    hourly = pq.read_table(os.path.join(target, R.HOURLY)).to_pandas()
    sw = lzr_switch(target)
    sl = (pd.Timestamp(0, tz="UTC") + pd.Timedelta(seconds=sw)).tz_convert(W.LOCAL)
    first_full = (sl.year + (sl.month == 12), sl.month % 12 + 1)          # the first whole month on the new network
    return dict(cat=cat, wells=wells, hourly=hourly, switch=sw, months=report_months(target), lzr_month=first_full)


def holes(wells):
    out = {}
    for x in wells[wells["function"] == "injection"].itertuples():
        out.setdefault(x.plant, []).append(((x.oh_top_lat, x.oh_top_lon, x.oh_top_tvd_m),
                                            (x.oh_bottom_lat, x.oh_bottom_lon, x.oh_bottom_tvd_m)))
    return out


def zone(lat, lon, hole_map, radius=W.RADIUS_KM):
    """Each point's plant (its epicentre within radius of an injection open hole) and the distance to it."""
    lat, lon = np.asarray(lat, float), np.asarray(lon, float)
    plant = np.array([""] * len(lat), dtype=object)
    best = np.full(len(lat), 99.0)
    for p, segs in hole_map.items():
        d = np.min([G.dist_to_segment(lat, lon, s) for s in segs], axis=0)
        sel = (d <= radius) & (d < best)
        plant[sel] = p
        best = np.minimum(best, d)
    return plant, best


def local_parts(t):
    ts = (pd.Timestamp(0, tz="UTC") + pd.to_timedelta(np.asarray(t, dtype=float), unit="s")).tz_convert(W.LOCAL)
    return ts.year.to_numpy(), ts.quarter.to_numpy(), (ts.hour + ts.minute / 60 + ts.second / 3600).to_numpy()


def counted(d, ml=W.COUNT_ML):
    """The earthquakes the scheme counts, with their plant, local year, quarter and hour."""
    c = d["cat"]
    c = c[(c["event_type"] == "earthquake") & (c["ml"] >= ml)].copy()
    c["plant"], c["dist"] = zone(c["latitude"], c["longitude"], holes(d["wells"]))
    c = c[c["plant"] != ""].copy()
    c["y"], c["q"], c["h"] = local_parts(c["t"].to_numpy())
    return c


def quiet(h, window=QUIET):
    a, b = window
    return (h >= a) | (h < b) if a > b else (h >= a) & (h < b)


def table(c):
    """{plant: {(year, quarter): count}} over every quarter of the record."""
    out = {p: {k: 0 for k in W.record_quarters()} for p in W.PLANTS}
    for (p, y, q), n in c.groupby(["plant", "y", "q"]).size().items():
        out[p][(int(y), int(q))] = int(n)
    return out


def volumes(d):
    """Injected volume per plant and local quarter (m3) from the hourly telemetry, and per plant from a time on."""
    h = d["hourly"]
    t = epoch(h["time_utc"])
    y, q, _ = local_parts(t)
    v = h["flow_l_s"].to_numpy() * 3.6
    df = pd.DataFrame(dict(plant=h["plant"].to_numpy(), y=y, q=q, v=v, t=t))
    tab = {p: {} for p in W.PLANTS}
    for (p, yy, qq), s in df.groupby(["plant", "y", "q"])["v"].sum().items():
        tab[p][(int(yy), int(qq))] = float(s)
    return tab, df


def report_months(target):
    """Metered injection per plant and operating month (m3) from the operators' reports (scheme 6.2): the 2023 to 2025
    sheets file each report under the month it reports; the 2026 sheet (the authority's portal) under the month it was
    submitted, the month after, so each 2026 row counts for the month before its label. December 2025, filed again on
    the 2026 sheet, is counted once (the two filings carry the same volumes)."""
    from openpyxl import load_workbook
    reg = json.load(open(os.path.join(target, R.PLANT_REG), encoding="utf-8"))
    op = {p["operator"]: p["plant"] for p in reg["plants"]}
    wb = load_workbook(os.path.join(target, R.REPORTS), read_only=True, data_only=True)
    seen = {}
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = next(it)
        k = {h: i for i, h in enumerate(head)}
        for r in it:
            if r[0] is None or r[k["function"]] != "injection":
                continue
            y, m = int(r[0][:4]), int(r[0][5:7])
            if ws.title == "2026":
                y, m = (y - 1, 12) if m == 1 else (y, m - 1)
            key = (r[k["well"]], y, m)
            if key in seen:
                assert seen[key][1] == r[k["volume_m3"]], key
                continue
            seen[key] = (op[r[k["operator"]]], r[k["volume_m3"]])
    wb.close()
    out = {p: {} for p in W.PLANTS}
    for (_, y, m), (p, v) in seen.items():
        out[p][(y, m)] = out[p].get((y, m), 0) + v
    return out


def report_quarters(months_):
    return {p: {k: sum(v for (y, m), v in months_[p].items() if (y, (m - 1) // 3 + 1) == k) for k in W.record_quarters()}
            for p in W.PLANTS}


def lzr_switch(target):
    """When Lanzenried's network changed: the start of LZR5's first epoch in the inventory (UTC seconds)."""
    root = ET.parse(os.path.join(target, R.INVENTORY)).getroot()
    ns = {"s": "http://www.fdsn.org/xml/station/1"}
    for st in root.iter("{http://www.fdsn.org/xml/station/1}Station"):
        if st.get("code") == "LZR5":
            return pd.Timestamp(st.get("startDate")).timestamp()
    raise ValueError("LZR5 not in the inventory")


def plan_volume(vol):
    """The 2027 operating plans: each quarter at its 2026 volume, the fourth at 2025's."""
    return {p: {q: vol[p][(2026, q) if q < 4 else (2025, 4)] for q in (1, 2, 3, 4)} for p in W.PLANTS}


def plan_reports(d):
    return plan_volume(report_quarters(d["months"]))


def rates(c, d, years=(2023, 2024, 2025, 2026), quiet_plants=("PFB",), window=QUIET, lzr_from=True, source="reports",
          night_volume=False):
    """Earthquakes of ML 1.0 or more per m3 injected for each plant over its complete record: Pfeilbrunn's from the
    quiet hours scaled to the day, Lanzenried's from the first whole month on its new network. source "reports" takes
    the scheme's reported volumes (6.2) by month; "telemetry" the hourly flows (then Lanzenried from the switch itself).
    night_volume divides the quiet-hour count by the volume injected in those hours instead of scaling it."""
    vol, vdf = volumes(d)
    a, b = window
    share = ((24 - a + b) if a > b else (b - a)) / 24.0
    out = {}
    for p in W.PLANTS:
        e = c[(c["plant"] == p) & c["y"].isin(years)]
        if source == "reports":
            mv = {k: v for k, v in d["months"][p].items() if k[0] in years and k <= (2026, 9)}
            if p == "LZR" and lzr_from:
                start = d["lzr_month"]
                e = e[e["t"] >= W.dt.datetime(start[0], start[1], 1, tzinfo=W.LOCAL).timestamp()]
                mv = {k: v for k, v in mv.items() if k >= start}
            vtot = float(sum(mv.values()))
        else:
            v = vdf[(vdf["plant"] == p) & vdf["y"].isin(years)]
            if p == "LZR" and lzr_from:
                e = e[e["t"] >= d["switch"]]
                v = v[v["t"] >= d["switch"]]
            vtot = float(v["v"].sum())
        if p in quiet_plants:
            q = quiet(e["h"].to_numpy(), window).sum()
            if night_volume:
                v = vdf[(vdf["plant"] == p) & vdf["y"].isin(years)]
                h0 = local_parts(v["t"].to_numpy())[2]                  # each telemetry hour's local start
                inside = np.clip(np.minimum(h0 + 1, 24) - np.maximum(h0, a), 0, 1) + np.clip(np.minimum(h0 + 1, b) - h0, 0, 1)
                out[p] = q / float((v["v"].to_numpy() * inside).sum())
                continue
            n = q / share
        else:
            n = float(len(e))
        out[p] = n / vtot
    return out


def forecast_from_rates(r, plan):
    return {p: {q: r[p] * plan[p][q] for q in (1, 2, 3, 4)} for p in W.PLANTS}


def golden(d, c=None, **kw):
    c = counted(d) if c is None else c
    if kw.get("source") == "telemetry":
        vol, _ = volumes(d)
        plan = plan_volume(vol)
    else:
        plan = plan_reports(d)
    return forecast_from_rates(rates(c, d, **kw), plan)


def rung0(c):
    t = table(c)
    return {p: {q: float(t[p][(2026, q) if q < 4 else (2025, 4)]) for q in (1, 2, 3, 4)} for p in W.PLANTS}


def rung1(c):
    """The same quarter carried forward at its growth over the year before."""
    t = table(c)
    out = {}
    for p in W.PLANTS:
        out[p] = {}
        for q in (1, 2, 3, 4):
            y1, y0 = ((2026, 2025) if q < 4 else (2025, 2024))
            a, b = t[p][(y1, q)], t[p][(y0, q)]
            out[p][q] = a * a / b if b else float(a)
    return out


def rung2(c, d):
    """Rate per volume over the record on every hour, Lanzenried's from its network change."""
    return forecast_from_rates(rates(c, d, quiet_plants=()), plan_reports(d))


def over(f, line=W.AMBER):
    return sorted((p, q) for p in f for q in f[p] if f[p][q] > line)


def maxc(ml, step=0.1):
    """Maximum-curvature completeness: the magnitude bin holding the most events (bins of 0.1, left-closed)."""
    b = np.floor(np.asarray(ml) / step + 1e-9) * step
    vals, n = np.unique(np.round(b, 1), return_counts=True)
    return float(vals[np.argmax(n)])


def bvalue(ml, mc, dm=0.01):
    """Aki's maximum-likelihood b above mc for magnitudes given to two decimals."""
    m = np.asarray(ml)
    m = m[m >= mc - 1e-9]
    return float(np.log10(np.e) / (m.mean() - (mc - dm / 2))), len(m)
