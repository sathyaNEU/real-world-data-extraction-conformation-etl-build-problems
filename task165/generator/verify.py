"""task165 architecture 2: the independent verifier. Recomputes the call and every graded figure from the pack with
pandas, sharing no code with golden.py, and compares with generator/figures.json.

    python3 task165/generator/verify.py [target]"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
TZ = "America/New_York"
BAD = []


def ok(name, cond, detail=""):
    print("%s %-60s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        BAD.append(name)


def meter():
    d = pd.read_parquet(os.path.join(T, "outfall_014_flow_monitoring_2014-2025.parquet"))
    old = d[d.flow_unit == "cfs"].copy()
    new = d[d.flow_unit == "MGD"].copy()
    old["t"] = pd.to_datetime(old.reading_time, format="%m/%d/%Y %H:%M") + pd.Timedelta(hours=5)
    old["q"] = old.flow * 0.646317
    new["t"] = pd.to_datetime(new.reading_time, format="%Y-%m-%d %H:%M:%S")
    new["q"] = new.flow
    s = pd.concat([old[["t", "q"]], new[["t", "q"]]]).groupby("t").q.max()
    idx = pd.date_range("2014-01-01 05:00", "2026-01-01 04:45", freq="15min")
    s = s.reindex(idx)
    assert s.notna().all()
    return s.to_numpy()


def southside():
    d = pd.read_csv(os.path.join(T, "wrp_influent_hourly_2014-2025.csv"))
    d = d[d.tag.str.startswith("SS")].copy()
    loc = pd.to_datetime(d.time_local)
    d["t"] = loc.dt.tz_localize(TZ, ambiguous="infer").dt.tz_convert("UTC").dt.tz_localize(None)
    d.loc[d.quality != "GOOD", "value_mgd"] = np.nan
    idx = pd.date_range("2014-01-01 05:00", "2026-01-01 04:00", freq="h")
    s = d.set_index("t").value_mgd.reindex(idx).interpolate(limit_direction="both")
    return s.to_numpy()


def tm7_alternatives():
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "TM-7_clay_street_storage_alternatives.pdf")).pages)
    alts = re.findall(r"\b([ABCD])\s+(\d+)\s+(\d+)\s+(?:Clay|Former)", txt)
    return [(a, float(v), float(p)) for a, v, p in alts]


def spill_events(o, vol, pump, room):
    lim = np.minimum(pump, np.clip(room, 0, None)) / 96.0
    s = 0.0
    spill = np.zeros(len(o), dtype=bool)
    for i, q in enumerate(o / 96.0):
        if q > 0:
            room_t = vol - s
            if q > room_t:
                spill[i] = True
                s = vol
            else:
                s += q
        elif s > 0:
            s = max(0.0, s - lim[i])
    on = np.flatnonzero(spill)
    return 0 if len(on) == 0 else 1 + int((np.diff(on) > 96).sum())


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    o = meter()
    room = np.repeat(140.0 - southside(), 4)
    alts = tm7_alternatives()
    ok("TM-7 lists four alternatives", len(alts) == 4, str(alts))
    ev = {a: spill_events(o, v, p, room) / 12 for a, v, p in alts}
    for a in ev:
        ok("events a year, Alternative %s" % a, round(ev[a], 1) == f["events_%s" % a], "%.2f" % ev[a])
    pick = next(a for a, _, _ in alts if ev[a] <= 4)
    ok("the call", pick == f["pick"], pick)
    rated = {a: spill_events(o, v, p, np.full(len(o), 1e9)) / 12 for a, v, p in alts}
    for a in rated:
        ok("at the rating, Alternative %s" % a, round(rated[a], 1) == f["rated_%s" % a], "%.2f" % rated[a])

    # ask 1
    tips = pd.read_csv(os.path.join(T, "rain_gauge_tips_2014-2025.csv")).drop_duplicates()
    tips["t"] = pd.to_datetime(tips.tip_time)
    inv = pd.read_csv(os.path.join(T, "rain_gauge_inventory.csv")).set_index("gauge_id")
    utc_from = {g: pd.Timestamp(inv.loc[g, "logger_installed"]) + pd.Timedelta(hours=12)
                for g in inv.index if inv.loc[g, "logger_model"].startswith("TipLink")}
    def to_local(g, t):
        utc = t + pd.Timedelta(hours=5)                     # Eastern Standard Time stamps
        if g in utc_from:
            utc = utc.where(t < utc_from[g], t)             # the cellular logger's UTC stamps
        return utc.dt.tz_localize("UTC").dt.tz_convert(TZ).dt.tz_localize(None)
    vis = pd.read_excel(os.path.join(T, "rain_gauge_field_service_2014-2025.xlsx"))
    vis = vis[vis.Notes.str.contains("Cal check", case=False) & ~vis.Notes.str.contains("No cal check", case=False)]
    for g in ["RG-1", "RG-2", "RG-3", "RG-4"]:
        x = tips[tips.gauge_id == g].copy()
        x["loc"] = to_local(g, x.t).to_numpy()
        x = x.sort_values("loc").reset_index(drop=True)
        gap = x["loc"].diff().dt.total_seconds()
        steady = gap.between(5, 20)
        run_id = (~steady).cumsum()
        x["run"] = run_id
        x["run_len"] = x.groupby("run")["loc"].transform("size")
        x["pour"] = False
        for d in pd.to_datetime(vis[vis.Gauge == g].Date).dt.date:
            same = x["loc"].dt.date == d
            x.loc[same & (x.run_len >= 20), "pour"] = True
        swap = pd.Timestamp("2025-05-15 09:35")
        x["inch"] = np.where((g == "RG-4") & (x["loc"] >= swap), 0.2 / 25.4, 0.01)
        y = x[(~x.pour) & (x["loc"].dt.year == 2025)]
        m = y.groupby(y["loc"].dt.month).inch.sum().reindex(range(1, 13), fill_value=0.0)
        for k in range(1, 13):
            ok("rainfall %s month %02d" % (g, k), round(m[k] + 1e-9, 2) == f["rain_%s_%02d" % (g, k)],
               "%.3f" % m[k])

    # ask 2
    sc = pd.read_csv(os.path.join(T, "northside_tank_scada_2020-2025.csv"))
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, "northside_tank_om_manual_section4.pdf")).pages)
    tab = re.findall(r"(\d+\.\d)\s+(\d+\.\d{3})", txt.split("Table 4-1. Tank stage-storage")[-1])
    hh = np.array([float(a) for a, _ in tab])
    vv = np.array([float(b) for _, b in tab])
    sc["t"] = pd.to_datetime(sc.Timestamp)
    lv = sc.NT_LIT601_FT.copy()
    after = sc.t >= pd.Timestamp("2023-08-23 11:00")
    lv[after] = lv[after] - lv[after].min()
    vol = pd.Series(np.interp(lv.fillna(0), hh, vv)).where(lv.notna())
    run = (sc.NT_P1_RUN + sc.NT_P2_RUN + sc.NT_P3_RUN) > 0
    drop = (vol.shift(1) - vol).where(run & (vol < vol.shift(1)) & vol.notna() & vol.shift(1).notna(), 0.0)
    yr = drop.groupby(sc.t.dt.year).sum()
    for y in range(2021, 2026):
        ok("Northside returns %d" % y, int(round(yr[y])) == f["nt_%d" % y], "%.2f" % yr[y])
    print("%d FAIL" % len(BAD))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
