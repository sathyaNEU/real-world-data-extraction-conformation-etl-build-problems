"""The independent verifier: recomputes every graded figure from target/ on its own code path (minute grids for the
outage replay, hand-rolled clock arithmetic for the planning table, a pivot for the meters) and compares it with
figures.json at the stated rounding. Exit 0 with no failure.

    python3 task308/generator/verify.py [target dir]
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "table": "weather_years_2027_hourly.csv", "events": "outage_event_log_2016_2025.csv",
    "fleet": "fleet_list_2027.xlsx", "tie": "red_willow_tie_outages_2016_2025.csv",
    "profiles": "offer_profiles_2016_2025.parquet", "meter": "mdm_interval_export_2025.parquet",
    "dps": "delivery_point_register_2025.xlsx", "orders": "meter_service_orders_2025.csv",
}
T0 = datetime(2016, 1, 1, 6, 0)          # the first hour, UTC
NH = 87672
NM = NH * 60


def dst_bounds(y):
    """second Sunday of March 02:00 local standard, first Sunday of November 02:00 local daylight, as UTC"""
    mar = datetime(y, 3, 8)
    mar += timedelta(days=(6 - mar.weekday()) % 7)
    nov = datetime(y, 11, 1)
    nov += timedelta(days=(6 - nov.weekday()) % 7)
    return mar + timedelta(hours=8), nov + timedelta(hours=7)


def table_utc(tb):
    out = []
    for d, he in zip(tb.local_date, tb.hour_ending):
        y, mo, da = map(int, d.split("-"))
        h = int(he.rstrip("*")) - 1
        wall = datetime(y, mo, da) + timedelta(hours=h)
        a, b = dst_bounds(y)
        # standard time is UTC-6, daylight UTC-5; the 2* row is the second, standard-time 01:00
        utc_std = wall + timedelta(hours=6)
        utc_dst = wall + timedelta(hours=5)
        if he.endswith("*"):
            out.append(utc_std)
        elif a <= utc_dst < b:
            out.append(utc_dst)
        else:
            out.append(utc_std)
    return out


def minute_avail(cap, events):
    a = np.full(NM, cap, dtype=np.float32)
    for s, e, left in events:
        i = max(int((s - T0).total_seconds() // 60), 0)
        j = min(int((e - T0).total_seconds() // 60), NM)
        if j > i:
            np.minimum(a[i:j], left, out=a[i:j])
    return a.reshape(NH, 60).mean(axis=1, dtype=np.float64)


def main(target):
    fails = []
    F = json.load(open(os.path.join(HERE, "figures.json")))
    tb = pd.read_csv(os.path.join(target, FILES["table"]), dtype={"hour_ending": str})
    tb["utc"] = table_utc(tb)
    tb = tb.sort_values("utc").reset_index(drop=True)
    if len(tb) != NH or tb.utc.iloc[0] != T0:
        fails.append("planning table clock")
    load = tb.load_2027_mw.values.astype(float)
    load = np.where(load > 50000, load / 1000.0, load)
    fl = pd.read_excel(os.path.join(target, FILES["fleet"]), sheet_name="Units")
    fl = fl[fl["Retirement date"].isna()]
    ev = pd.read_csv(os.path.join(target, FILES["events"]))
    ev = ev.loc[ev.groupby("event_id").revision.idxmax()]
    ev = ev[ev.event_type.isin(["U1", "U2", "U3", "SF", "D1", "D2", "D3"])]
    parse = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%MZ")  # noqa: E731
    gen = np.zeros(NH)
    ct = np.zeros(NH)
    ctcap = 0.0
    for _, u in fl.iterrows():
        code, cap = u["GADS unit code"], float(u["Net winter capability (MW)"])
        e = ev[ev.unit_code == code]
        lst = [(parse(r.start_utc), parse(r.end_utc), (r.net_available_mw if r.event_type.startswith("D") else 0.0))
               for r in e.itertuples()]
        av = minute_avail(cap, lst)
        gen += av
        if u["Technology"] == "Combustion Turbine":
            ct += av
            ctcap += cap
    tl = pd.read_csv(os.path.join(target, FILES["tie"]))

    def tparse(x):
        m = re.match(r"(\d\d)/(\d\d)/(\d{4}) (\d\d):(\d\d) (C[SD]T)", x)
        mo, da, y, hh, mm, z = m.groups()
        return datetime(int(y), int(mo), int(da), int(hh), int(mm)) + timedelta(hours=6 if z == "CST" else 5)
    tie = minute_avail(1.0, [(tparse(a), tparse(b), 0.0) for a, b in zip(tl.out_of_service, tl.returned_to_service)])
    short = load - tb.wind_mw.values - tb.solar_mw.values - gen - 200.0 * tie
    pr = pd.read_parquet(os.path.join(target, FILES["profiles"]))
    pr = pr.set_index(pd.to_datetime(pr.hour_beginning_utc)).reindex(pd.to_datetime(tb.utc))
    eue = lambda add: float(np.clip(short - add, 0, None).sum()) / 10.0  # noqa: E731
    base = eue(0)
    rem = {"Ketchum Ridge": base - eue(300 * ct / ctcap), "Red Willow import": base - eue(300 * tie),
           "Sandhill Draw": base - eue(450 * pr.sandhill_draw_mw_per_mw.values),
           "Coulee Flats": base - eue(500 * pr.coulee_flats_mw_per_mw.values)}
    pay = {"Ketchum Ridge": 6.45 * 12 * 300e3, "Red Willow import": 327 * 365 * 300,
           "Sandhill Draw": 5.25 * 12 * 450e3, "Coulee Flats": 51.60 * 500e3}
    net = {o: (rem[o] * 20000 - pay[o]) / 1e6 for o in rem}
    if max(net, key=net.get) != F["award"]:
        fails.append("award")
    if int(round(base / 100) * 100) != F["base_eue_mwh"]:
        fails.append("base EUE %.1f" % base)
    for o in rem:
        if int(round(rem[o] / 100) * 100) != F["removed_mwh"][o]:
            fails.append("removed %s %.1f" % (o, rem[o]))
        if int(round(net[o])) != F["net_musd"][o]:
            fails.append("net %s %.2f" % (o, net[o]))
    # ------------------------------------------------------------ the asks, on a pivot
    ex = pd.read_parquet(os.path.join(target, FILES["meter"]))
    ex["ts"] = pd.to_datetime(ex.interval_start, utc=True)
    ex = ex.sort_values(["dp_id", "ts", "version"]).groupby(["dp_id", "ts"], as_index=False).last()
    od = pd.read_csv(os.path.join(target, FILES["orders"]))
    ex["k"] = 1.0
    for r in od[od.work_type == "Current transformer replacement"].itertuples():
        new = float(re.search(r"multiplier \d+ to (\d+)", r.notes).group(1))
        when = pd.Timestamp(r.completed).tz_localize("America/Chicago")
        sel = (ex.dp_id == r.dp_id) & (ex.ts >= when)
        ex.loc[sel, "k"] = new / ex.loc[sel, "multiplier"]
    ex["net"] = (ex.kwh_del - ex.kwh_rec) * ex.k
    hist = pd.read_excel(os.path.join(target, FILES["dps"]), sheet_name="Assignment history")
    ex["member"] = None
    for r in hist.itertuples():
        lo = pd.Timestamp(r[3]).tz_localize("America/Chicago")
        sel = (ex.dp_id == r[1]) & (ex.ts >= lo)
        if isinstance(r[4], str) and r[4]:
            sel &= ex.ts < pd.Timestamp(r[4]).tz_localize("America/Chicago") + pd.Timedelta(days=1)
        ex.loc[sel, "member"] = r[2]
    A = ex.groupby("member").net.sum() / 1000.0
    for k, v in F["ask_a_mwh"].items():
        if int(round(A[k])) != v:
            fails.append("ask A %s %.2f" % (k, A[k]))
    # clock: a meter found on standard time ran an hour early from the spring change to its reset
    cl = ex.copy()
    start = pd.Timestamp("2025-03-09 08:00", tz="UTC")
    for r in od[od.notes.str.contains("standard time", na=False)].itertuples():
        reset = pd.Timestamp(r.completed).tz_localize("America/Chicago").tz_convert("UTC").ceil("h")
        sel = (cl.dp_id == r.dp_id) & (cl.ts >= start) & (cl.ts < reset - pd.Timedelta(hours=1))
        cl.loc[sel, "ts"] = cl.loc[sel, "ts"] + pd.Timedelta(hours=1)
        cl = cl[~((cl.dp_id == r.dp_id) & (cl.ts == reset - pd.Timedelta(hours=1)) & (cl.quality == "E"))]
    tot = cl.groupby("ts").net.sum()
    month = tot.index.tz_convert("America/Chicago").month
    peaks = [tot[month == mth].idxmax() for mth in range(1, 13)]
    B = cl[cl.ts.isin(peaks)].groupby("member").net.sum() / 12 / 1000.0
    for k, v in F["ask_b_mw"].items():
        if round(float(B[k]), 1) != v:
            fails.append("ask B %s %.3f" % (k, B[k]))
    print("verify: %d failures" % len(fails))
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
