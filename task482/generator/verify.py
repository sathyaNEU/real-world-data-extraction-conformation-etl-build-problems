"""task482's independent verifier: reads only the shipped bundle (target/), the golden deliverables and
generator/figures.json, recomputes every graded figure with its own code (pandas and numpy, no generator module), and
compares.

    python3 task482/generator/verify.py
"""
import datetime as dt
import json
import os
import re
import sys
import warnings
from collections import defaultdict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
FAILS = []
UTC = dt.timezone.utc
FALL = pd.Timestamp("2026-11-01 06:00")             # UTC, naive: every instant below is naive UTC


def say(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def half_up(x, d=0):
    q = 10 ** d
    return np.floor(x * q + 0.5) / q


def to_utc(s, later=False):
    """Eastern wall-clock strings to UTC; in the repeated hour the first reading unless later"""
    t = pd.to_datetime(s)
    a = t + pd.Timedelta(hours=4)
    b = t + pd.Timedelta(hours=5)
    first = a.where(a < FALL, b)
    if not later:
        return first
    return b.where((a < FALL) & (b >= FALL), first)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    st = pd.read_excel(os.path.join(T, "wellhaven_bike_share_station_list.xlsx"), sheet_name="Stations")
    city = {int(r["Feed station ID"]): int(str(r["Station"])[2:]) for _, r in st.iterrows()}
    name = {int(str(r["Station"])[2:]): r["Name"] for _, r in st.iterrows()}
    nos = sorted(name)

    # ------------------------------------------------------------------------------------------ the records
    tr = pd.read_csv(os.path.join(T, "northlane_trips_2026q4.csv"))
    n0 = len(tr)
    tr = tr.drop_duplicates()
    say("the trips' repeated rows dropped (%d of %d)" % (n0 - len(tr), n0), n0 - len(tr) > 3000 and tr.trip_id.is_unique)
    a1, a2 = to_utc(tr.start_time), to_utc(tr.start_time, True)
    b1, b2 = to_utc(tr.end_time), to_utc(tr.end_time, True)
    dur = pd.to_timedelta(tr.duration_s, unit="s")
    start = a1.copy()
    end = b1.copy()
    for (x, y) in ((a1, b1), (a1, b2), (a2, b1), (a2, b2)):
        m = (y - x) == dur
        start = start.where(~m, x)
        end = end.where(~m, y)
    say("every trip's start and end resolve on its duration", ((end - start) == dur).all())
    mv = pd.read_csv(os.path.join(T, "northlane_fleet_moves_2026q4.csv"))
    mv["t"] = to_utc(mv.logged_at)
    mv["bike_no"] = mv.bike.str.replace("WHB-", "", regex=False).astype(int)
    ev = pd.concat([
        pd.DataFrame({"bike": tr.bike_id.values, "t": start.values, "o": 2, "kind": "rent", "s": tr.start_station_id.values}),
        pd.DataFrame({"bike": tr.bike_id.values, "t": end.values, "o": 1, "kind": "dock", "s": tr.end_station_id.values}),
        pd.DataFrame({"bike": mv.bike_no.values, "t": mv.t.values, "o": np.where(mv.action == "Pick up", 0, 1),
                      "kind": np.where(mv.action == "Pick up", "pickup", "drop"), "s": mv.station_id.values}),
    ], ignore_index=True)
    ev["k"] = np.arange(len(ev))
    ev = ev.sort_values(["bike", "t", "o", "k"]).reset_index(drop=True)
    origin = pd.Timestamp("2026-09-24 00:00")
    extract = pd.Timestamp("2027-01-11 01:00")
    grid = int((extract - origin).total_seconds() // 60) + 2

    def idx(t):
        s = (t - origin).total_seconds()
        k = int(s // 60)
        return k if s == k * 60 else k + 1

    spells = []
    for b, g in ev.groupby("bike", sort=False):
        rows = list(zip(g.t, g.kind, g.s))
        cur, a = (rows[0][2], origin) if rows[0][1] in ("rent", "pickup") else (None, None)
        for i, (t, kind, s) in enumerate(rows):
            if kind in ("rent", "pickup"):
                if cur is not None:
                    back = None
                    if kind == "pickup":
                        back = next((x[0] for x in rows[i + 1:] if x[1] in ("drop", "dock")), None)
                    spells.append((b, cur, a, t, kind, back))
                cur, a = None, None
            else:
                cur, a = s, t
        if cur is not None:
            spells.append((b, cur, a, None, "open", None))
    starts = defaultdict(list)
    for s, t in zip(tr.start_station_id, start):
        starts[s].append(t)
    for s in starts:
        starts[s] = np.array(sorted(starts[s]), dtype="datetime64[ns]")

    def passed(s, a, z):
        arr = starts.get(s)
        if arr is None or z is None:
            return False
        lo = np.searchsorted(arr, np.datetime64(a), side="right")
        hi = np.searchsorted(arr, np.datetime64(z), side="left")
        return hi > lo

    def broken(x):
        b, s, a, z, kind, back = x
        if kind != "pickup":
            return False
        if back is not None and (back - z) < pd.Timedelta(hours=20):
            return False
        return passed(s, a, z)

    work = {no: np.zeros(grid + 1, dtype=np.int32) for no in nos}
    for x in spells:
        if broken(x):
            continue
        b, s, a, z, kind, back = x
        i, j = idx(a), (idx(z) if z is not None else grid)
        if j > i:
            work[city[s]][i] += 1
            work[city[s]][j] -= 1
    work = {no: np.cumsum(v)[:grid] for no, v in work.items()}

    def service(mo):
        out = []
        d = dt.date(2026, mo, 1)
        while d.month == mo:
            a = to_utc(pd.Series([str(dt.datetime(d.year, d.month, d.day, 6, 0))])).iloc[0]
            b = to_utc(pd.Series([str(dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1))])).iloc[0]
            out.append(np.arange(idx(a), idx(b)))
            d += dt.timedelta(days=1)
        return np.concatenate(out)
    svc = {mo: service(mo) for mo in (10, 11, 12)}
    av = {no: {mo: 100.0 * float((work[no][svc[mo]] >= 1).mean()) for mo in svc} for no in nos}
    pr = sorted(no for no in nos if min(av[no].values()) < 90)
    gs = fig["stations"]
    say("the priority stations recompute: %s" % pr,
        ["W-%02d %s" % (no, name[no]) for no in pr] == fig["call"]["priority"])
    say("each station's lowest month recomputes in whole per cent",
        all(int(half_up(min(av[no].values()))) == gs["W-%02d" % no]["lowest"] for no in nos))
    clear = sorted((min(av[no].values()), no) for no in nos if min(av[no].values()) >= 90)
    v, nb = clear[0]
    say("the nearest station above the line and its margin recompute (W-%02d, %.1f)" % (nb, half_up(v - 90, 1)),
        fig["components"]["nearest"]["station"] == "W-%02d" % nb and
        abs(fig["components"]["nearest"]["margin_points"] - half_up(v - 90, 1)) < 1e-9)

    # the default: the archive's available count taken as the bikes in working order
    ss = pd.read_csv(os.path.join(T, "wellhaven_station_status_archive_2026q4.csv"))
    ss["k"] = ((ss.polled_at - int((origin - pd.Timestamp("1970-01-01")).total_seconds())) // 60).astype(int)
    feed = {no: np.zeros(grid, dtype=np.int32) for no in nos}
    first = ss.groupby("station_id").k.min().to_dict()
    for sid, g in ss.groupby("station_id"):
        later = [first[x] for x in first if x != sid and city[x] == city[sid] and first[x] > first[sid]]
        stop = min(later) if later else grid
        ks = g.k.values
        vs = g.num_bikes_available.values
        for i in range(len(ks)):
            hi = min(ks[i + 1] if i + 1 < len(ks) else grid, stop)
            if hi > ks[i]:
                feed[city[sid]][ks[i]:hi] += vs[i]
    dav = {no: {mo: 100.0 * float((feed[no][svc[mo]] >= 1).mean()) for mo in svc} for no in nos}
    dpr = sorted(no for no in nos if min(dav[no].values()) < 90)
    say("the default path (the feed's available count) recomputes to W-16 alone", dpr == [16])

    # ------------------------------------------------------------------------------------------ ask A
    sa = pd.read_csv(os.path.join(T, "paystation_sales_2026q4.csv"))
    wo = pd.read_excel(os.path.join(T, "paystation_work_orders_2026q4.xlsx"))
    sw = wo[wo["Work type"].str.startswith("Card terminal")].sort_values("Opened")
    hist = defaultdict(list)
    for _, r in sw.iterrows():
        no = int(r["Pay station"][2:])
        if not hist[r["Terminal removed"]]:
            hist[r["Terminal removed"]].append((pd.Timestamp.min, no))
        hist[r["Terminal installed"]].append((r["Closed"], no))
    sa["u"] = pd.to_datetime(sa.sold_at, utc=True).dt.tz_convert(None)
    off = np.where(sa.u < FALL, 4, 5)
    sa["loc"] = sa.u - pd.to_timedelta(off, unit="h")
    voided = set(sa.loc[sa.transaction == "VOID", "original_sale"])
    q = sa[(sa.transaction == "SALE") & (~sa.sale_id.isin(voided)) & (sa["loc"] >= "2026-10-01") & (sa["loc"] < "2027-01-01")]

    def where(r):
        found = None
        for since, no in hist[r["terminal"]]:
            if since <= r["loc"]:
                found = no
        return found
    q = q.assign(no=q.apply(where, axis=1))
    say("every fourth-quarter sale has a pay station from its terminal's history", q.no.notna().all())
    tot = q.groupby("no").amount.sum().round(2).to_dict()
    say("each station's pay-station card sales recompute to the cent",
        all(abs(tot.get(no, 0.0) - gs["W-%02d" % no]["sales_cad"]) < 0.005 for no in nos))

    # ------------------------------------------------------------------------------------------ ask B
    al = pd.read_csv(os.path.join(T, "paystation_alarm_log_2026q4.csv"))
    al["u"] = pd.to_datetime(al.event_time, utc=True).dt.tz_convert(None)
    al = al.sort_values(["pay_station", "u", "event_id"])
    windows = []
    d = dt.date(2026, 10, 1)
    while d <= dt.date(2026, 12, 31):
        a = to_utc(pd.Series([str(dt.datetime(d.year, d.month, d.day, 6, 0))])).iloc[0]
        b = to_utc(pd.Series([str(dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1))])).iloc[0]
        windows.append((a, b))
        d += dt.timedelta(days=1)
    clears = {"COMMS_RESTORED": "COMMS_LOST", "READER_OK": "READER_FAULT"}
    hours = {}
    for ps, g in al.groupby("pay_station"):
        spans, open_ = [], {}
        for t, e in zip(g.u, g.event):
            if e == "RESTART":
                spans += [(a, t) for a in open_.values()]
                open_ = {}
            elif e in ("COMMS_LOST", "READER_FAULT"):
                open_.setdefault(e, t)
            elif e in clears and clears[e] in open_:
                spans.append((open_.pop(clears[e]), t))
        spans += [(a, extract) for a in open_.values()]
        merged = []
        for a, b in sorted(spans):
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        s = 0.0
        for a, b in merged:
            for x, y in windows:
                lo, hi = max(a, x), min(b, y)
                if hi > lo:
                    s += (hi - lo).total_seconds()
        hours[int(ps[2:])] = s / 3600.0
    say("each station's service hours without card payments recompute in whole hours",
        all(int(half_up(hours[no])) == gs["W-%02d" % no]["hours_no_card"] for no in nos))

    # ------------------------------------------------------------------------------------------ the golden files
    wb = pd.read_excel(os.path.join(GOLD, "priority_stations_2027q1.xlsx"), sheet_name="Priority stations", header=3)
    wb = wb[wb["Station"].astype(str).str.match(r"W-\d\d$")]
    say("the golden workbook carries every station's lowest month and designation",
        all(int(r["Lowest month (%)"]) == gs[r["Station"]]["lowest"] and (r["Priority station for Q1 2027"] == "Yes")
            == gs[r["Station"]]["priority"] for _, r in wb.iterrows()) and len(wb) == 24)
    ps = pd.read_excel(os.path.join(GOLD, "priority_stations_2027q1.xlsx"), sheet_name="Pay stations", header=3)
    ps = ps[ps["Station"].astype(str).str.match(r"W-\d\d$")]
    say("the golden workbook carries every station's sales and hours",
        all(abs(r["Card sales (CAD)"] - gs[r["Station"]]["sales_cad"]) < 0.005 and
            int(r["Service hours unable to take a card"]) == gs[r["Station"]]["hours_no_card"] for _, r in ps.iterrows()))
    page = open(os.path.join(GOLD, "station_availability_2026q4.html"), encoding="utf-8").read()
    say("the golden page names the priority stations' count and carries an inline chart",
        "<svg" in page and "90 per cent" in page and page.count('class="p"') == len(pr))
    print("\n%d FAIL" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
