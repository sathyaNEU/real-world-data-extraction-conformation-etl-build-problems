"""Computations read from the shipped pack only: the conformed daily spreads at the hub and the node, the 2027
cycling threshold and every rung of the ladder, and the asks on the battery's 2026 operation (the warranty's full cycles
by month, the day-ahead net after MPI's fees by month and per cycle)."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

LAST_DAY = dt.date(2026, 11, 2)
MENU = [5, 10, 15, 20, 25, 30, 35, 40]
LIMIT = 300
RATED = 400.0
TO_DC = 0.975
OPS_MONTHS = list(range(1, 11))


def find(target, stem):
    hits = [f for f in os.listdir(target) if f.startswith(stem)]
    assert len(hits) == 1, (stem, hits)
    return os.path.join(target, hits[0])


# --------------------------------------------------------------------------------------------- prices and spreads
def read_prices(path):
    """One row per operating day, hour and settlement point, the operator's two archive formats read alike."""
    p = pd.read_csv(path, dtype=str)
    iso = p["DeliveryDate"].str.contains("-")
    day = pd.to_datetime(p["DeliveryDate"].where(iso), format="%Y-%m-%d", errors="coerce")
    day = day.fillna(pd.to_datetime(p["DeliveryDate"].where(~iso), format="%m/%d/%Y", errors="coerce"))
    he = p["HourEnding"].str.replace(":00", "", regex=False).astype(int)
    rep = p["RepeatedHourFlag"].str.lower().isin(["y", "true"])
    out = pd.DataFrame({"day": day.dt.date, "he": he, "rep": rep, "point": p["SettlementPoint"],
                        "price": p["SettlementPointPrice"].astype(float)})
    return out


def tb4(prices):
    s = np.sort(np.asarray(prices, dtype=float))
    return s[-4:].mean() - s[:4].mean()


def daily_spreads(target):
    """The conformed daily record: each operating day's spread at the hub and, where MPI priced it, at the node
    (its two names joined), with the days MPI priced the node at the hub marked."""
    points = pd.read_csv(find(target, "mpi_settlement_point_list"), dtype=str).fillna("")
    hub = read_prices(find(target, "mpi_dam_settlement_point_prices_north_hub"))
    node = read_prices(find(target, "mpi_dam_settlement_point_prices_redrock"))
    succ = {r.predecessor: r.settlement_point for r in points.itertuples() if r.predecessor}
    node["point"] = node["point"].replace(succ)
    assert node["point"].nunique() == 1
    hs = hub.groupby("day")["price"].apply(tb4).rename("hub_spread")
    ns = node.groupby("day")["price"].apply(tb4).rename("node_spread")
    nh = hub.groupby("day").size().rename("hours")
    d = pd.concat([nh, hs, ns], axis=1).reset_index().rename(columns={"index": "day"})
    # the days the node was priced at the hub (the settlement point list's note), identical hour by hour
    j = node.merge(hub, on=["day", "he", "rep"], suffixes=("_n", "_h"))
    same = j.groupby("day").apply(lambda g: bool((g["price_n"] == g["price_h"]).all()), include_groups=False)
    d["at_hub_price"] = d["day"].map(same).fillna(False).astype(bool)
    return d


def overlap(d):
    return d[d["node_spread"].notna() & ~d["at_hub_price"]]


def expected_days(series, menu=MENU):
    v = np.asarray(series, dtype=float)
    return {s: 365.0 * float((v >= s).mean()) for s in menu}


def pick(exp):
    ok = [s for s in MENU if exp[s] <= LIMIT]
    return min(ok) if ok else None


def golden(d):
    """The node's record extended over the hub's: the overlap's proportional relationship carried to every day,
    the node's own spreads where MPI priced it, and the expected cycling days over the full record."""
    ov = overlap(d)
    k = float(ov["node_spread"].sum() / ov["hub_spread"].sum())
    carried = k * d["hub_spread"]
    series = carried.where(~(d["node_spread"].notna() & ~d["at_hub_price"]), d["node_spread"])
    exp = expected_days(series)
    return dict(k=k, series=series, exp=exp, call=pick(exp))


def rungs(d):
    """Every rung and reflex: its construction, the expected days per setting and the setting it picks."""
    ov = overlap(d)
    x, y = ov["hub_spread"].to_numpy(), ov["node_spread"].to_numpy()
    H = d["hub_spread"].to_numpy()
    k = y.sum() / x.sum()
    b = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
    a = y.mean() - b * x.mean()
    out = {}
    node_all = d.loc[d["node_spread"].notna(), "node_spread"]
    out["R0 the node's own record"] = node_all
    out["R0 the node's record, the hub-priced days dropped"] = ov["node_spread"]
    out["R0 the node's 2026"] = d.loc[pd.to_datetime(d["day"]).dt.year.eq(2026) & d["node_spread"].notna(), "node_spread"]
    out["R1 the hub plus the node's average spread premium"] = H + (y - x).mean()
    out["Rx the hub's record alone"] = H
    out["Rx the node's record scaled by the hub's long-run mean"] = ov["node_spread"] * (H.mean() / x.mean())
    out["G proportional (ratio of sums)"] = k * H
    out["G regression with intercept"] = a + b * H
    years = pd.to_datetime(d["day"]).dt.year
    out["G full years 2019 to 2025"] = (k * H)[years.le(2025).to_numpy()]
    return {name: dict(exp=expected_days(v), call=pick(expected_days(v))) for name, v in out.items()}, dict(k=k, a=a, b=b)


# --------------------------------------------------------------------------------------- the battery's 2026 operation
def local_from_utc(ts):
    """Central prevailing time from UTC (DST from 2:00 on the second Sunday of March to 2:00 on the first Sunday of
    November)."""
    ts = pd.to_datetime(ts, utc=True).dt.tz_convert(None)
    yr = ts.dt.year
    out = []
    for t, y in zip(ts, yr):
        m = dt.date(y, 3, 1)
        spring = m + dt.timedelta(days=(6 - m.weekday()) % 7 + 7)
        n = dt.date(y, 11, 1)
        fall = n + dt.timedelta(days=(6 - n.weekday()) % 7)
        s_utc = dt.datetime(spring.year, spring.month, spring.day, 8)
        f_utc = dt.datetime(fall.year, fall.month, fall.day, 7)
        out.append(t + dt.timedelta(hours=-5 if s_utc <= t < f_utc else -6))
    return pd.Series(out, index=ts.index)


TEST_WINDOWS = None


def test_windows(target):
    """The capacity tests' discharge windows from Cordell's reports (local prevailing time)."""
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(find(target, "cordell_capacity_tests")).pages)
    txt = re.sub(r"\s+", " ", txt)
    out = []
    for m in re.finditer(r"Discharge: (\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) to (\d{2}):(\d{2})", txt):
        d = dt.date.fromisoformat(m.group(1))
        a = dt.datetime(d.year, d.month, d.day, int(m.group(2)), int(m.group(3)))
        b = dt.datetime(d.year, d.month, d.day, int(m.group(4)), int(m.group(5)))
        out.append((a, b))
    return out


def bms(target):
    b = pd.read_csv(find(target, "redrock_draw_bms_hourly_export"))
    b["start_utc"] = pd.to_datetime(b["interval_start_utc"], utc=True).dt.tz_convert(None)
    b["local"] = local_from_utc(b["interval_start_utc"])
    return b


def meter(target):
    m = pd.read_csv(find(target, "redrock_draw_revenue_meter"))
    m["end_utc"] = pd.to_datetime(m["interval_ending_utc"], utc=True).dt.tz_convert(None)
    m["hour_utc"] = (m["end_utc"] - pd.Timedelta(minutes=15)).dt.floor("h")
    return m


def dropped_hours(b):
    """The hours the portal filled with the last state it saw: zero energy in and out, the state of charge and the
    mode held, inside spans where the next reading shows the battery moved."""
    zero = (b["dc_charge_kwh"] == 0) & (b["dc_discharge_kwh"] == 0)
    held = (b["soc_pct"] == b["soc_pct"].shift(1)) & (b["operating_mode"] == b["operating_mode"].shift(1))
    return zero & held


def warranty_cycles(target):
    """Full cycles by contract month (local prevailing time), January to October 2026: the BMS's DC discharge, the
    meter's delivered energy over 0.975 in the hours the BMS export lost, the capacity tests' discharge left out."""
    b = bms(target)
    m = meter(target)
    lost_hours = set(b.loc[dropped_hours(b) & b["start_utc"].isin(set(m.loc[m["mwh_delivered"] > 0, "hour_utc"])),
                           "start_utc"])
    # a lost span runs from the first held hour; take every held zero hour in a span the meter shows energy in
    held = dropped_hours(b)
    span_id = (~held).cumsum()
    spans = b[held].groupby(span_id[held])["start_utc"].agg(list)
    lost = set()
    for hrs in spans:
        if any(h in lost_hours for h in hrs):
            lost.update(hrs)
    dlv = m.groupby("hour_utc")["mwh_delivered"].sum()
    dc = b["dc_discharge_kwh"] / 1000.0
    sub = b["start_utc"].map(dlv).fillna(0.0) / TO_DC
    b["dc_counted"] = np.where(b["start_utc"].isin(lost), sub, dc)
    for a, z in test_windows(target):
        inwin = (b["local"] >= a.replace(minute=0)) & (b["local"] < z)
        b.loc[inwin, "dc_counted"] = 0.0
    b["month"] = b["local"].dt.month
    yr = b["local"].dt.year
    sel = yr.eq(2026) & b["month"].isin(OPS_MONTHS)
    out = (b[sel].groupby("month")["dc_counted"].sum() / RATED).reindex(OPS_MONTHS)
    lost_dis = sorted(t for t in lost if dlv.get(t, 0.0) > 0)
    return out, lost_dis


def dam_net(target):
    """The battery's day-ahead net after MPI's fees by operating month: the latest statement's line for each hour and
    charge type, MPI's sign reversed, the administrative fee once per operating day."""
    s = pd.read_csv(find(target, "redrock_draw_dam_settlement_statement_lines"))
    s["operating_date"] = pd.to_datetime(s["operating_date"])
    s["issue_date"] = pd.to_datetime(s["issue_date"])
    s = s[s["operating_date"].dt.year.eq(2026) & s["operating_date"].dt.month.isin(OPS_MONTHS)]
    latest = s.sort_values("issue_date").groupby(["operating_date", "hour_ending", "repeated_hour", "charge_type"]).tail(1)
    energy = latest[latest["charge_type"] != "DAAF"]
    fee = latest[latest["charge_type"] == "DAAF"].groupby("operating_date").head(1)
    tot = pd.concat([energy, fee])
    tot["month"] = tot["operating_date"].dt.month
    return (-tot.groupby("month")["amount_usd"].sum()).reindex(OPS_MONTHS)
