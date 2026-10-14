"""Independent verifier for task459: reads only the shipped bundle (target/) and the goldens, on its own code path
(pandas), and recomputes the call (the complying offers and the slate filling the need), every plant's rate, the
default route's slate, and both asks."""
import os
import re
import sys

import numpy as np
import pandas as pd

STANDARD = 925.0
NEED = 1000.0


def f(target, pat):
    return os.path.join(target, next(x for x in sorted(os.listdir(target)) if re.search(pat, x)))


def plant_codes(target):
    off = pd.read_excel(f(target, r"offers_received\.xlsx$"), header=1)
    gen = pd.read_excel(f(target, r"^eia860_.*\.xlsx$"), header=1)
    plants = gen.drop_duplicates("Plant Code")[["Plant Code", "Plant Name", "County", "State"]]
    codes = {}
    for _, o in off.iterrows():
        if pd.notna(o["EIA plant code"]):
            codes[o["Offer ID"]] = int(o["EIA plant code"])
            continue
        words = str(o["Resource"]).split()[:2]
        m = plants[plants["Plant Name"].str.split().str[:2].apply(lambda w: w == words) &
                   (plants["County"] == o["County"]) & (plants["State"] == o["State"])]
        assert len(m) == 1, (o["Offer ID"], m)
        codes[o["Offer ID"]] = int(m["Plant Code"].iloc[0])
    return off.set_index("Offer ID"), codes


def hourly(target):
    cm = pd.read_csv(f(target, r"^camd_hourly"), usecols=["Facility ID", "Date", "Hour", "Operating Time",
                                                         "CO2 Mass (short tons)", "Heat Input Measure Indicator"])
    cm = cm[cm["Operating Time"] > 0].copy()
    cm["t"] = pd.to_datetime(cm["Date"]) + pd.to_timedelta(cm["Hour"], unit="h") + pd.Timedelta(hours=8)   # to UTC
    cm["t"] = cm["t"].dt.tz_localize("UTC")
    cm["partial"] = cm["Operating Time"] < 1.0
    cm["sub"] = cm["Heat Input Measure Indicator"] == "Substitute"
    g = cm.groupby(["Facility ID", "t"]).agg(co2=("CO2 Mass (short tons)", "sum"), partial=("partial", "any"),
                                            sub=("sub", "any")).reset_index()
    me = pd.read_csv(f(target, r"meter_data"))
    me["t"] = pd.to_datetime(me["interval_start"], utc=True)
    return g, me


def main(target, golden_dir):
    off, codes = plant_codes(target)
    g, me = hourly(target)
    res = {}
    for oid, code in codes.items():
        cap = float(off.loc[oid, "Contract Capacity (MW)"])
        m = me[me["offer_id"] == oid][["t", "net_mwh"]]
        x = m.merge(g[g["Facility ID"] == code], on="t", how="left")
        x["co2"] = x["co2"].fillna(0.0)
        x["partial"] = x["partial"].fillna(False).astype(bool)
        run = x["co2"] > 0
        at = run & ~x["partial"] & ((x["net_mwh"] - cap).abs() <= 0.02 * cap)
        rate = x.loc[at, "co2"].sum() * 2000.0 / x.loc[at, "net_mwh"].sum()
        y25 = x["t"] >= pd.Timestamp("2025-01-01 08:00", tz="UTC")
        default = x.loc[y25, "co2"].sum() * 2000.0 / x.loc[y25, "net_mwh"].sum()
        # substitute hours in 2025 (standard-time year)
        gg = g[(g["Facility ID"] == code) & (g["t"] >= pd.Timestamp("2025-01-01 08:00", tz="UTC"))]
        res[oid] = dict(cap=cap, rate=rate, default=default, sub=int(gg["sub"].sum()))
    # forced outages from the GADS records
    ev = pd.read_csv(f(target, r"gads_events"), dtype={"event_number": str})
    # one outage's entries on a unit share its start; the latest entered is the current one
    ev = ev.sort_values("entered_utc", kind="stable").drop_duplicates(["offer_id", "unit", "start_utc"], keep="last")
    ev = ev[ev["event_type"].isin(["U1", "U2", "U3", "SF"])].copy()
    ev["a"] = pd.to_datetime(ev["start_utc"], utc=True)
    ev["b"] = pd.to_datetime(ev["end_utc"], utc=True)
    allu = pd.read_csv(f(target, r"gads_events")).groupby("offer_id")["unit"].unique()
    y0, y1 = pd.Timestamp("2025-01-01 08:00", tz="UTC"), pd.Timestamp("2026-01-01 08:00", tz="UTC")
    for oid in res:
        drivers = [u for u in allu[oid] if u.startswith(("CT", "CS"))]
        # minute grid over 2025 and the edges: the plant is out where every driver unit is out
        grid = pd.date_range(y0 - pd.Timedelta(days=3), y1 + pd.Timedelta(days=3), freq="min")
        out = np.ones(len(grid), bool)
        for u in drivers:
            mask = np.zeros(len(grid), bool)
            for _, r in ev[(ev["offer_id"] == oid) & (ev["unit"] == u)].iterrows():
                i = grid.searchsorted(r["a"])
                j = grid.searchsorted(r["b"])
                mask[i:j] = True
            out &= mask
        inside = (grid >= y0) & (grid < y1)
        hours = out[inside].sum() / 60.0
        o = out.astype(int)
        starts = np.flatnonzero(np.diff(np.concatenate([[0], o])) == 1)
        ends = np.flatnonzero(np.diff(np.concatenate([o, [0]])) == -1)
        count = sum(1 for s_, e_ in zip(starts, ends) if grid[e_] >= y0 and grid[s_] < y1)
        res[oid]["fo_hours"], res[oid]["fo_count"] = hours, count
    gw = pd.read_excel(os.path.join(golden_dir, "offered_plants_eps_2027.xlsx"))
    gw = gw[gw["Offer ID"].astype(str).str.startswith("BL26")].set_index("Offer ID")
    fails = 0

    def chk(cond, msg):
        nonlocal fails
        print(("ok    " if cond else "FAIL  ") + msg)
        fails += 0 if cond else 1

    price = off["Capacity price ($/kW-month, 2027)"].astype(float)

    def fill(ok_):
        take, tot = [], 0.0
        for o in sorted(ok_, key=lambda o: price[o]):
            if tot + res[o]["cap"] <= NEED:
                take.append(o)
                tot += res[o]["cap"]
        return take, tot

    comply = sorted(o for o in res if res[o]["rate"] <= STANDARD)
    chk(int(sum(res[o]["cap"] for o in comply)) == 2375, "verify: %d offers comply, %d MW" % (
        len(comply), sum(res[o]["cap"] for o in comply)))
    signed, mw = fill(comply)
    names = {o: off.loc[o, "Resource"] for o in res}
    chk(int(mw) == 990 and len(signed) == 3, "verify: the slate is %s, %d MW" % ([names[o] for o in signed], mw))
    RATE = "CO2 rate under the commitment (lb per net MWh)"
    FOH, FOC, SUB = "2025 forced outage hours", "2025 forced outages", "2025 clock hours operated with CO2 resting on substitute data"
    chk(sorted(comply) == sorted(o for o in gw.index if float(gw.loc[o, RATE]) <= STANDARD),
        "verify: the golden workbook's rates put the same offers at or under 925")
    for o in sorted(res):
        r = res[o]
        chk(abs(r["rate"] - float(gw.loc[o, RATE])) <= 1.0, "verify %s: rate %.1f (golden %s)" % (o, r["rate"], gw.loc[o, RATE]))
        chk(int(round(r["fo_hours"])) == int(gw.loc[o, FOH]) and r["fo_count"] == int(gw.loc[o, FOC]),
            "verify %s: %.2f forced outage hours in %d outages" % (o, r["fo_hours"], r["fo_count"]))
        chk(r["sub"] == int(gw.loc[o, SUB]), "verify %s: %d substitute-data hours" % (o, r["sub"]))
    dflt = sorted(o for o in res if res[o]["default"] <= STANDARD)
    dslate, dmw = fill(dflt)
    chk(len(dflt) == 5 and sorted(dslate) != sorted(signed) and int(dmw) == 905,
        "verify: on the 2025 annual averages five comply and the slate is %s, %d MW" % ([names[o] for o in dslate], dmw))
    print("verify: %d failed" % fails)
    return fails == 0


if __name__ == "__main__":
    T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(0 if main(os.path.join(T, "target"), os.path.join(T, "golden")) else 1)
