"""The records the cooperative's systems hold, made from the clean truth: the planning load table, the outage event
log, the tie's outage log, the offers' modelled profiles, and the 2025 member metering with its field work."""
import numpy as np
import pandas as pd

import params as P

CAUSE = {
    "nuclear": [3110, 3410, 3620, 4260, 4290],
    "hydro": [7040, 7110, 7300, 7400],
    "coal": [1000, 1005, 1060, 1455, 3410, 3620, 4290, 1795],
    "combined cycle": [5000, 5040, 5250, 5300, 3620, 4290, 6500],
    "combustion turbine": [5000, 5040, 5110, 5250, 5300, 4800, 4290, 3620],
    "reciprocating engine": [4400, 4410, 4420, 3620, 4290],
}
LACK_OF_FUEL = 9130
PLANNED_CAUSE = [1999, 4990, 5099, 7999]


def runs(down):
    """start and end indices (end exclusive) of every run of True"""
    d = np.diff(np.concatenate([[0], down.astype(np.int8), [0]]))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def _stamp(utc, i, minute):
    if i >= len(utc):
        return utc[-1] + pd.Timedelta(hours=1, minutes=int(minute))
    return utc[i] + pd.Timedelta(minutes=int(minute))


def events(W):
    rng = np.random.default_rng(P.SEED + 11)
    utc = W["utc"]
    n = len(utc)
    rows = []
    seq = {}

    def add(code, etype, s, e, avail, cause, rev_ok=True):
        y = s.tz_convert(P.TZ).year
        seq[(code, y)] = seq.get((code, y), 0) + 1
        eid = "%s-%d-%03d" % (code, y, seq[(code, y)])
        rep = (e + pd.Timedelta(days=int(rng.integers(2, 25)))).tz_convert(P.TZ).date()
        rows.append(dict(event_id=eid, revision=0, unit_code=code, event_type=etype, start=s, end=e,
                         net_available_mw=avail, cause_code=cause, report_date=rep))
        if rev_ok and etype in ("U1", "U2", "SF", "D1") and rng.random() < 0.08:
            # a revised report: the first report's end was the planned return, the revision the actual one
            e0 = e - pd.Timedelta(minutes=int(rng.integers(90, 900)))
            if e0 <= s:
                e0 = s + pd.Timedelta(minutes=30)
            rows[-1]["end"] = e0
            rows[-1]["report_date"] = (e0 + pd.Timedelta(days=int(rng.integers(1, 6)))).tz_convert(P.TZ).date()
            rows.append(dict(event_id=eid, revision=1, unit_code=code, event_type=etype, start=s, end=e,
                             net_available_mw=avail, cause_code=cause,
                             report_date=(e + pd.Timedelta(days=int(rng.integers(20, 70)))).tz_convert(P.TZ).date()))

    curt_runs = runs(W["curt"])
    for code, plant, unit, cls, mw, efor, mttr, gas in P.UNITS + P.RETIRED:
        st = W["state"][code]
        for a, b in runs(~st):
            s = _stamp(utc, a, rng.integers(0, 60))
            e = _stamp(utc, b, rng.integers(0, 60))
            etype = rng.choice(["U1", "U1", "U1", "U2", "SF"]) if cls == "combustion turbine" else rng.choice(["U1", "U1", "U2"])
            add(code, str(etype), s, e, np.nan, int(rng.choice(CAUSE[cls])))
        # forced derates
        dstate = np.ones(n, dtype=bool)
        lam, mu = 0.012 / (0.988 * 10), 0.1
        r = rng.random(n)
        up = True
        for i in range(n):
            if up and r[i] < lam:
                up = False
            elif (not up) and r[i] < mu:
                up = True
            dstate[i] = up
        for a, b in runs(~dstate):
            s = _stamp(utc, a, rng.integers(0, 60))
            e = _stamp(utc, b, rng.integers(0, 60))
            add(code, "D1", s, e, float(round(mw * rng.uniform(0.45, 0.85))), int(rng.choice(CAUSE[cls])))
        # planned and maintenance work in the shoulder months
        for y in P.YEARS:
            m = int(rng.choice([4, 5, 9, 10]))
            s = pd.Timestamp(y, m, int(rng.integers(1, 20)), int(rng.integers(6, 10)), tz=P.TZ).tz_convert("UTC")
            add(code, "PO", s, s + pd.Timedelta(days=int(rng.integers(8, 28)), hours=int(rng.integers(0, 12))),
                np.nan, int(rng.choice(PLANNED_CAUSE)), rev_ok=False)
            for _ in range(int(rng.integers(0, 3))):
                m = int(rng.choice([3, 4, 5, 6, 9, 10, 11]))
                s = pd.Timestamp(y, m, int(rng.integers(1, 26)), int(rng.integers(0, 24)), tz=P.TZ).tz_convert("UTC")
                add(code, "MO", s, s + pd.Timedelta(hours=int(rng.integers(6, 72))), np.nan,
                    int(rng.choice(CAUSE[cls])), rev_ok=False)
        # the pipeline's curtailments of interruptible transport take the peakers off together
        if gas == "interruptible":
            for k, (a, b) in enumerate(curt_runs):
                # the pipeline's notice takes effect, and is lifted, at a clock hour: every unit goes out with it
                s = _stamp(utc, a, 0)
                e = _stamp(utc, b, 0)
                add(code, "U1", s, e, np.nan, LACK_OF_FUEL)
    ev = pd.DataFrame(rows)
    return ev


def avail_hours(ev, utc, codes, caps):
    """available MW per unit per hour from the forced events' latest revisions, a part hour counting for its part"""
    t0 = utc[0]
    nh = len(utc)
    ev = ev.sort_values("revision").drop_duplicates("event_id", keep="last")
    ev = ev[ev.event_type.isin(["U1", "U2", "U3", "SF", "D1", "D2", "D3"])]
    out = {}
    for code in codes:
        cap = caps[code]
        e = ev[ev.unit_code == code]
        if e.empty:
            out[code] = np.full(nh, float(cap))
            continue
        s = ((e.start - t0).dt.total_seconds() / 3600.0).values
        f = ((e.end - t0).dt.total_seconds() / 3600.0).values
        a = np.where(e.event_type.isin(["D1", "D2", "D3"]), e.net_available_mw.fillna(0).values, 0.0)
        pts = np.unique(np.clip(np.concatenate([s, f, [0.0, float(nh)]]), 0, nh))
        lost = np.zeros(len(pts) - 1)
        mid = (pts[:-1] + pts[1:]) / 2
        for k in range(len(s)):
            on = (mid > s[k]) & (mid < f[k])
            lost = np.where(on, np.maximum(lost, cap - a[k]), lost)
        cum = np.concatenate([[0.0], np.cumsum(lost * np.diff(pts))])
        grid = np.arange(nh + 1, dtype=float)
        F = np.interp(grid, pts, cum)
        out[code] = cap - np.diff(F)
    return out


def tie_events(W):
    rng = np.random.default_rng(P.SEED + 12)
    utc = W["utc"]
    rows = []
    k = 0
    for a, b in runs(~W["tie"]):
        k += 1
        rows.append(dict(outage_no="RW-%05d" % (1000 + k), kind="Forced", start=_stamp(utc, a, rng.integers(0, 60)),
                         end=_stamp(utc, b, rng.integers(0, 60))))
    for y in P.YEARS:
        k += 1
        s = pd.Timestamp(y, int(rng.choice([4, 5, 10])), int(rng.integers(2, 25)), 7, tz=P.TZ).tz_convert("UTC")
        rows.append(dict(outage_no="RW-%05d" % (1000 + k), kind="Planned", start=s,
                         end=s + pd.Timedelta(hours=int(rng.integers(8, 60)))))
    return pd.DataFrame(rows).sort_values("start").reset_index(drop=True)


def tie_hours(te, utc):
    """share of each hour the tie is in service"""
    t0 = utc[0]
    nh = len(utc)
    s = ((te.start - t0).dt.total_seconds() / 3600.0).values
    f = ((te.end - t0).dt.total_seconds() / 3600.0).values
    pts = np.unique(np.clip(np.concatenate([s, f, [0.0, float(nh)]]), 0, nh))
    mid = (pts[:-1] + pts[1:]) / 2
    out_ = np.zeros(len(mid))
    for k in range(len(s)):
        out_ = np.where((mid > s[k]) & (mid < f[k]), 1.0, out_)
    cum = np.concatenate([[0.0], np.cumsum(out_ * np.diff(pts))])
    F = np.interp(np.arange(nh + 1, dtype=float), pts, cum)
    return 1.0 - np.diff(F)


# ------------------------------------------------------------------------------------------------ pack tables
def planning_table(W):
    """the load forecasting group's 2027 table: one row per hour ending in local prevailing time"""
    loc = W["local"]
    he = (loc.hour + 1).astype(str).values.astype(object)
    # the repeated hour on the autumn change is the second 01:00 to 02:00, marked 2*
    off = np.array([t.utcoffset().total_seconds() for t in loc])
    rep = (loc.hour == 1) & (off == -6 * 3600) & (np.roll(off, 1) == -5 * 3600)
    he[rep] = "2*"
    load = W["load"].astype(float).copy()
    yrs = loc.year.values
    # 2019's extract came from the old forecasting tool in kW
    load[yrs == 2019] = np.round(load[yrs == 2019] * 1000.0, 0)
    df = pd.DataFrame(dict(weather_year=yrs, local_date=loc.strftime("%Y-%m-%d"), hour_ending=he,
                           hub_air_deg_f=W["temp"], load_2027_mw=load, wind_mw=W["wind_ex"], solar_mw=W["solar_ex"]))
    return df


def event_log(ev):
    df = ev.copy()
    df["start_utc"] = df.start.dt.strftime("%Y-%m-%dT%H:%MZ")
    df["end_utc"] = df.end.dt.strftime("%Y-%m-%dT%H:%MZ")
    df["report_date"] = pd.to_datetime(df.report_date).dt.strftime("%Y-%m-%d")
    df = df.sort_values(["start", "unit_code", "revision"]).reset_index(drop=True)
    return df[["event_id", "revision", "unit_code", "event_type", "start_utc", "end_utc", "net_available_mw",
               "cause_code", "report_date"]]


def tie_log(te):
    def fmt(t):
        lt = t.tz_convert(P.TZ)
        return lt.strftime("%m/%d/%Y %H:%M ") + ("CDT" if lt.utcoffset().total_seconds() == -18000 else "CST")
    return pd.DataFrame(dict(outage_no=te.outage_no, facility="345 kV Red Willow - Hollow Junction",
                             kind=te.kind, out_of_service=[fmt(t) for t in te.start],
                             returned_to_service=[fmt(t) for t in te.end]))


def profiles(W):
    return pd.DataFrame(dict(hour_beginning_utc=W["utc"].tz_convert(None),
                             sandhill_draw_mw_per_mw=W["wcf_new"], coulee_flats_mw_per_mw=W["scf_new"]))


def metering(M):
    """the MDM export: one row per delivery point per interval, stamped in local prevailing time with the
    offset the MDM attaches, the multiplier the MDM applied, delivered and received kWh"""
    rng = np.random.default_rng(P.SEED + 61)
    utc = M["utc"]
    n = len(utc)
    rows = []
    swaps = {s["dp"]: s for s in M["swaps"]}
    stuck = {s["dp"]: s for s in M["stuck"]}
    dst_start = pd.Timestamp("2025-03-09 03:00", tz=P.TZ).tz_convert("UTC")
    for d in M["dps"]:
        dp = d["dp"]
        load = M["true"][dp]
        g = M["gen"].get(dp)
        net = load - (g if g is not None else 0.0)
        dl = np.clip(net, 0, None)
        rc = np.clip(-net, 0, None)
        mult_phys = np.full(n, 80.0)
        mult_app = np.full(n, 80.0)
        if dp in swaps:
            s = swaps[dp]
            ts = s["when"].tz_convert("UTC")
            tl = (s["when"] + pd.Timedelta(days=s["lag_days"])).tz_convert("UTC")
            mult_phys = np.where(utc >= ts, s["new"], s["old"]).astype(float)
            mult_app = np.where(utc >= tl, s["new"], s["old"]).astype(float)
        else:
            m0 = float(rng.choice([40, 60, 80, 120, 160]))
            mult_phys[:] = m0
            mult_app[:] = m0
        rep_dl = np.round(dl / mult_phys, 3) * mult_app
        rep_rc = np.round(rc / mult_phys, 3) * mult_app if g is not None else np.zeros(n)
        stamp = utc.copy()
        keep = np.ones(n, dtype=bool)
        if dp in stuck:
            r = stuck[dp]["reset"].tz_convert("UTC")
            win = (utc >= dst_start) & (utc < r)
            # the meter kept standard time, the MDM read its stamps as daylight time: an hour early
            stamp = pd.DatetimeIndex(np.where(win, utc - pd.Timedelta(hours=1), utc)).tz_localize("UTC") \
                if stamp.tz is None else pd.DatetimeIndex(np.where(win, (utc - pd.Timedelta(hours=1)).tz_convert(None),
                                                                       utc.tz_convert(None))).tz_localize("UTC")
            # the first stamp in the window falls in the hour the spring change skips: the MDM rejected it
            keep &= ~(utc == dst_start)
        for i in np.where(keep)[0]:
            pass
        df = pd.DataFrame(dict(dp_id=dp, t=stamp[keep], version=1, quality="A", multiplier=mult_app[keep],
                               kwh_del=np.round(rep_dl[keep], 1), kwh_rec=np.round(rep_rc[keep], 1)))
        if dp in stuck:
            # the stamp the reset skipped: the MDM estimated it from its neighbours
            r = stuck[dp]["reset"].tz_convert("UTC")
            miss = r - pd.Timedelta(hours=1)
            nb = df[(df.t == miss - pd.Timedelta(hours=1)) | (df.t == r)]
            df = pd.concat([df, pd.DataFrame(dict(dp_id=[dp], t=[miss], version=[1], quality=["E"],
                                                  multiplier=[nb.multiplier.iloc[-1]],
                                                  kwh_del=[round(nb.kwh_del.mean(), 1)],
                                                  kwh_rec=[round(nb.kwh_rec.mean(), 1)]))])
        rows.append(df)
    ex = pd.concat(rows, ignore_index=True)
    # comms failures: the MDM estimated the hour and never received the reading
    idx = rng.choice(len(ex), 60, replace=False)
    ex.loc[idx, "quality"] = "E"
    ex.loc[idx, "kwh_del"] = np.round(ex.loc[idx, "kwh_del"] * rng.uniform(0.85, 1.15, 60), 1)
    # first loads that were estimates, replaced a few days later by the meter's own reading (version 2)
    days = rng.choice(len(ex) // 24, 30, replace=False)
    add = []
    for dd in days:
        blk = ex.iloc[dd * 24:(dd + 1) * 24]
        if (blk.quality != "A").any() or blk.dp_id.nunique() > 1:
            continue
        v1 = blk.copy()
        v1["quality"] = "E"
        v1["kwh_del"] = np.round(v1.kwh_del * rng.uniform(0.9, 1.1), 1)
        v2 = blk.copy()
        v2["version"] = 2
        add.append((dd, v1, v2))
    for dd, v1, v2 in add:
        ex.loc[v1.index, ["quality", "kwh_del"]] = v1[["quality", "kwh_del"]].values
        ex = pd.concat([ex, v2])
    ex["interval_start"] = [t.tz_convert(P.TZ).isoformat(timespec="minutes") for t in ex.t]
    ex = ex.sort_values(["dp_id", "t", "version"]).reset_index(drop=True)
    return ex[["dp_id", "interval_start", "version", "quality", "multiplier", "kwh_del", "kwh_rec"]]
