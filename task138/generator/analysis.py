"""Every graded figure of task138 computed from target/ alone: the weather-normal peak, the voltage cut's relief at
the planning peak and the rungs below it, the planning peaks and transfers, and the two asks.

    python3 task138/generator/analysis.py
"""
import math
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import io_util as IO  # noqa: E402

FEEDERS = ["DUN-%d" % i for i in range(1, 9)]
CDT = pd.Timedelta(hours=5)          # summer local time is UTC less five hours
PLAN_YEARS = [2027, 2028, 2029, 2030, 2031]


def fpath(target, name):
    return os.path.join(target, name)


# ------------------------------------------------------------------ filed values
class Filed:
    """The criteria's numbers for Dunraith, the pilot's feeders and the forecast's growth, read from the pack."""

    def __init__(self, target):
        crit = IO.pdf_text(fpath(target, "BEC_distribution_planning_criteria_rev4.pdf"))
        crit = re.sub(r"\s+", " ", crit)
        m = re.search(r"Dunraith 2 x 75/100/125 MVA (\d+\.\d) Mossford Municipal Airport (\d+) F", crit)
        self.firm = float(m.group(1))
        self.design = float(m.group(2))
        self.block = float(re.search(r"Switching block (\d+\.\d) MW", crit).group(1))
        self.threshold = float(re.search(r"maximum temperature was (\d+) F or more", crit).group(1))
        wb = openpyxl.load_workbook(fpath(target, "BEC_load_forecast_2025.xlsx"), read_only=True)
        for row in wb["Substations"].iter_rows(values_only=True):
            if row[0] == "Dunraith":
                self.growth = float(row[2]) / 100.0
        tp = re.sub(r"\s+", " ", IO.pdf_text(fpath(target, "CVR_pilot_plan_Dunraith_2025.pdf")))
        self.pilot = re.findall(r"DUN-\d", re.search(r"Pilot feeders: (.*?)\.", tp).group(1))
        self.comparison = [f for f in FEEDERS if f not in self.pilot]
        self.pilot_start = pd.Timestamp("2025-06-02 00:00")
        self.pilot_end = pd.Timestamp("2025-09-29 00:00")


# ------------------------------------------------------------------ loads and temperatures
def feeder_loads(target, old_shift=True):
    """Hourly feeder MW in local time, each hour labelled at its start; Bad hours left out."""
    old = pd.read_csv(fpath(target, "DUNRAITH_FDR_KW_2022-2023.csv"))
    ts = pd.to_datetime(old["Date/Time"], format="%m/%d/%Y %H:%M")
    if old_shift:
        ts = ts - pd.Timedelta(hours=1)
    a = pd.DataFrame({"DUN-%d" % i: old["DUNRAITH F%d KW" % i].values / 1000.0 for i in range(1, 9)})
    a.index = ts.values
    new = pd.read_csv(fpath(target, "dunraith_feeder_mw_2024-2026.csv"))
    new = new[new.Quality == "Good"]
    new = new.assign(feeder=new.TagName.str.split(".").str[0], ts=pd.to_datetime(new.TimeStamp))
    b = new.pivot(index="ts", columns="feeder", values="Value")[FEEDERS]
    out = pd.concat([a, b]).sort_index()
    out.index = pd.DatetimeIndex(out.index)
    return out


def observations(target):
    """Airport observations; the export's clock is local standard time, an hour behind summer local time."""
    w = pd.read_csv(fpath(target, "mossford_ap_obs_2022-2026.csv"))
    w = w.dropna(subset=["DRY_BULB_C"])
    lst = pd.to_datetime(w["DATE_LST"], format="%Y-%m-%dT%H:%M:%S")
    return pd.DataFrame({"lst": lst.values, "local": (lst + pd.Timedelta(hours=1)).values,
                         "utc": (lst + pd.Timedelta(hours=6)).values, "kind": w["REPORT_TYPE"].values,
                         "f": w["DRY_BULB_C"].values * 9.0 / 5.0 + 32.0})


def daily_tmax(obs, clock="local", routine_only=False, whole_f=False, snap=None):
    o = obs[obs.kind == "FM-15"] if routine_only else obs
    t = o[clock]
    if snap == "round":
        t = t.dt.round("h")
    f = o["f"].round(0) if whole_f else o["f"]
    return f.groupby(t.dt.normalize().values).max()


def weather_normal(target, filed, loads=None, obs=None, clock="local", whole_f=False, drop_pilot_on=False,
                   add_back=None, years=(2022, 2023, 2024, 2025, 2026)):
    """3.2: the line of each day's highest hourly substation load on its maximum temperature, days at or above the
    threshold, read at the design temperature."""
    loads = feeder_loads(target) if loads is None else loads
    obs = observations(target) if obs is None else obs
    sub = loads.dropna().sum(axis=1)
    if add_back is not None:
        on = pilot_states(target, sub.index)
        frac = sum(loads.loc[sub.index, f] for f in filed.pilot) / sub
        sub = sub.where(~on, sub / (1 - add_back * frac))
    if drop_pilot_on:
        on = pilot_states(target, sub.index)
        days_on = set(sub.index[on].normalize())
        sub = sub[~sub.index.normalize().isin(list(days_on))]
    dmax = sub.groupby(sub.index.normalize()).max()
    tmax = daily_tmax(obs, clock=clock, whole_f=whole_f)
    df = pd.DataFrame({"load": dmax, "tmax": tmax}).dropna()
    df = df[df.index.year.isin(list(years)) & df.index.month.isin([6, 7, 8, 9])]
    hot = df[df.tmax >= filed.threshold]
    slope, icpt = np.polyfit(hot.tmax.values, hot.load.values, 1)
    return {"B": icpt + slope * filed.design, "slope": slope, "icpt": icpt, "n_days": len(hot),
            "top_days": hot[hot.tmax >= filed.design - 1]}


# ------------------------------------------------------------------ the pilot
def switch_events(target):
    lg = pd.read_csv(fpath(target, "VR_event_log_DUN_2025.csv"))
    lg = lg[lg.Event.isin(["CVR ON", "CVR OFF"])].copy()
    lg["feeder"] = lg.Equipment.str.split(" ").str[0]
    lg["t"] = pd.to_datetime(lg.EventTime)
    return lg.sort_values("t")


def feeder_state(events, feeder, idx, at_end=False):
    ev = events[events.feeder == feeder]
    times = ev.t.values
    on = (ev.Event == "CVR ON").values
    probe = idx + (pd.Timedelta(minutes=59, seconds=59) if at_end else pd.Timedelta(0))
    k = np.searchsorted(times, probe.values, side="right") - 1
    st = np.where(k >= 0, on[np.clip(k, 0, None)], False)
    return st


def pilot_states(target, idx, filed=None):
    """True for an hour in which every pilot feeder ran CVR for the whole hour."""
    filed = filed or Filed(target)
    ev = switch_events(target)
    st = np.ones(len(idx), bool)
    for f in filed.pilot:
        st &= feeder_state(ev, f, idx) & feeder_state(ev, f, idx, at_end=True)
    return pd.Series(st, index=idx)


def pilot_frame(target, filed, loads=None, obs=None, schedule=False, clock="local"):
    """The pilot summer hour by hour: pilot and comparison feeders' load, CVR state, the day's maximum temperature."""
    loads = feeder_loads(target) if loads is None else loads
    obs = observations(target) if obs is None else obs
    L = loads[(loads.index >= filed.pilot_start) & (loads.index < filed.pilot_end)].dropna()
    idx = L.index
    if schedule:
        wk = ((idx - filed.pilot_start).days // 7)
        on = pd.Series(np.asarray(wk % 2 == 0), index=idx)
        off = ~on
    else:
        ev = switch_events(target)
        s0 = {f: feeder_state(ev, f, idx) for f in filed.pilot}
        s1 = {f: feeder_state(ev, f, idx, at_end=True) for f in filed.pilot}
        on = pd.Series(np.all([s0[f] & s1[f] for f in filed.pilot], axis=0), index=idx)
        off = pd.Series(np.all([~s0[f] & ~s1[f] for f in filed.pilot], axis=0), index=idx)
    tmax = daily_tmax(obs, clock=clock)
    hourly_t = obs.set_index(obs["local"].dt.round("h"))["f"]
    hourly_t = hourly_t[~hourly_t.index.duplicated(keep="first")]
    return pd.DataFrame({"pil": L[filed.pilot].sum(axis=1), "com": L[filed.comparison].sum(axis=1),
                         "on": on.values, "off": off.values,
                         "tmax": tmax.reindex(idx.normalize()).values,
                         "t": hourly_t.reindex(idx).values,
                         "hour": idx.hour, "dow": idx.dayofweek}, index=idx)


def relief(P, mask=None, control=True):
    """1 less the ratio of the pilot feeders' load (to the comparison feeders') in CVR hours to that in normal
    hours, over the hours the mask keeps."""
    m = pd.Series(True, index=P.index) if mask is None else mask
    if control:
        r = P.pil / P.com
    else:
        r = P.pil
    return 1.0 - r[m & P.on].mean() / r[m & P.off].mean()


def daily_peak_mask(P, loads):
    sub = loads.loc[P.index].sum(axis=1)
    pk = sub.groupby(sub.index.normalize()).idxmax()
    m = pd.Series(False, index=P.index)
    m[pk.values] = True
    return m


def relief_rungs(target, filed, loads=None, obs=None):
    loads = feeder_loads(target) if loads is None else loads
    obs = observations(target) if obs is None else obs
    P = pilot_frame(target, filed, loads, obs)
    hot = (P.tmax >= filed.design - 2) & (P.hour >= 16) & (P.hour <= 20)
    return {"P": P,
            "golden": relief(P, hot),
            "all_hours": relief(P),
            "daily_peak_hour": relief(P, daily_peak_mask(P, loads)),
            "no_control_all": relief(P, control=False),
            "no_control_hot": relief(P, hot, control=False),
            "n_hot_on": int((hot & P.on).sum()), "n_hot_off": int((hot & P.off).sum())}


def relief_by_band(P, bands=((75, 85), (85, 90), (90, 95), (95, 99), (99, 104))):
    out = []
    for lo, hi in bands:
        m = (P.tmax >= lo) & (P.tmax < hi) & (P.hour >= 16) & (P.hour <= 20)
        out.append((lo, hi, relief(P, m), int((m & P.on).sum()), int((m & P.off).sum())))
    return out


# ------------------------------------------------------------------ planning peaks and transfers
def transfer(peak, filed):
    if peak <= filed.firm:
        return 0.0
    return math.ceil(round((peak - filed.firm) / filed.block, 9)) * filed.block


def planning(B, r, filed, base_year=2024):
    rows = []
    for y in PLAN_YEARS:
        wn = B * (1 + filed.growth) ** (y - base_year)
        pk = wn * (1 - r)
        rows.append({"year": y, "weather_normal": wn, "relief_mw": wn - pk, "peak": pk, "transfer": transfer(pk, filed)})
    return rows


# ------------------------------------------------------------------ ask A: members' energy by feeder
def register(target):
    wb = openpyxl.load_workbook(fpath(target, "DUN_transformer_register_2026-10.xlsx"), read_only=True)
    t = list(wb["Transformers"].iter_rows(values_only=True))
    d = list(wb["Devices"].iter_rows(values_only=True))
    return pd.DataFrame(t[1:], columns=t[0]), pd.DataFrame(d[1:], columns=d[0])


def moved_sections(target):
    """(switch opened, from feeder, to feeder) for each section SO-2026-114 moved."""
    txt = re.sub(r"\s+", " ", IO.pdf_text(fpath(target, "SO-2026-114_Dunraith.pdf")))
    return re.findall(r"(S-\d+) \((DUN-\d)\) Open(?: \(SCADA\))? Section beyond S-\d+ fed from (DUN-\d)", txt)


def downstream(dev, root, depth=None):
    kids = {}
    for d, u in zip(dev.DEVICE_ID, dev.UPSTREAM_DEVICE):
        kids.setdefault(u, []).append(d)
    out, todo = set(), [(root, 0)]
    while todo:
        x, k = todo.pop()
        if depth is not None and k >= depth:
            continue
        for c in kids.get(x, []):
            out.add(c)
            todo.append((c, k + 1))
    return out


def feeder_energy(target, use_mult=True, mult_from_set=True, reassign=True, depth=None, prorate_june30=False,
                  june30_new=False):
    """Each feeder's members' energy, June to September 2026, MWh: a transformer's daily kWh times its meter
    multiplier from the day the present meter was set (whole kWh before), counted on the feeder that served it
    that day (the sections the switching order moved belong to their old feeder until 30 June)."""
    md = pd.read_csv(fpath(target, "mdms_xfmr_daily_kwh_20260601_20260930.csv"))
    md["date"] = pd.to_datetime(md.READ_DATE, format="%m/%d/%Y")
    tx, dev = register(target)
    mult = dict(zip(tx.XFMR_ID, tx.METER_MULT))
    mset = dict(zip(tx.XFMR_ID, pd.to_datetime(tx.METER_SET)))
    m = md.XFMR_ID.map(mult) if use_mult else pd.Series(1, index=md.index)
    if use_mult and mult_from_set:
        m = m.where(md.date >= md.XFMR_ID.map(mset), 1)
    md["kwh"] = md.KWH * m
    md["feeder"] = md.FEEDER
    if reassign:
        prot = dict(zip(tx.XFMR_ID, tx.PROTECTIVE_DEVICE))
        old = {}
        for sw, a, b in moved_sections(target):
            under = downstream(dev, sw, depth)
            for t, p in prot.items():
                if p in under:
                    old[t] = a
        before = md.date < pd.Timestamp("2026-06-30" if june30_new else "2026-07-01")
        o = md.XFMR_ID.map(old)
        md.loc[before & o.notna(), "feeder"] = o[before & o.notna()]
        if prorate_june30:
            # the minutes each section ran paralleled before midnight, counted on the new feeder
            mins = {"DUN-4": 4, "DUN-6": 3, "DUN-1": 2}
            j30 = (md.date == pd.Timestamp("2026-06-30")) & o.notna()
            extra = md[j30].copy()
            frac = extra.feeder.map(mins) / 1440.0
            md.loc[j30, "kwh"] = md.loc[j30, "kwh"] * (1 - frac)
            extra["kwh"] = extra["kwh"] * frac
            extra["feeder"] = extra.FEEDER
            md = pd.concat([md, extra])
    return (md.groupby("feeder")["kwh"].sum() / 1000.0).reindex(FEEDERS)


# ------------------------------------------------------------------ ask B: the feeders' demand on the hottest days
def hottest_days(target, n=10, clock="local", obs=None):
    obs = observations(target) if obs is None else obs
    tm = daily_tmax(obs, clock=clock)
    tm = tm[(tm.index >= pd.Timestamp("2026-06-01")) & (tm.index <= pd.Timestamp("2026-09-30"))]
    return tm.sort_values(ascending=False, kind="mergesort").head(n), tm.sort_values(ascending=False).iloc[n]


def mv90(target, realign=True):
    """The supplier's 15-minute kWh by recorder, each interval keyed by its local start. The T2 cabinet's
    replacement recorder stamps intervals at their start: its first stamp repeats the old recorder's last one, and
    from there on its stamps move up 15 minutes."""
    mv = pd.read_csv(fpath(target, "MV90_DP0417_202606-202609.csv"), dtype={"RECORDER": str})
    mv["stamp"] = pd.to_datetime(mv.INTERVAL_END_UTC, format="%Y-%m-%d %H:%M")
    mv["end"] = mv["stamp"]
    if realign:
        for rec, g in mv.groupby("RECORDER", sort=False):
            dup = g.stamp.duplicated(keep="first")
            if dup.any():
                first = g.index[dup.values][0]
                k = g.index[g.index >= first]
                mv.loc[k, "end"] = mv.loc[k, "stamp"] + pd.Timedelta(minutes=15)
    return mv


def demand_peaks(target, days, meters=("41-2207", "41-2208"), clock="local", realign=True, dedupe=False,
                 ending=True, offset_h=5):
    mv = mv90(target, realign)
    mv = mv[mv.RECORDER.isin(list(meters))]
    if dedupe:
        mv = mv.drop_duplicates(["RECORDER", "stamp"], keep="first")
    end = mv["end"]
    if clock == "local":
        end = end - pd.Timedelta(hours=offset_h)
    start = end - pd.Timedelta(minutes=15) if ending else end
    s = mv.assign(start=start.values).groupby("start")["VALUE"].sum() * 4.0 / 1000.0
    day = s.index.normalize()
    out = {}
    for d in days.index:
        x = s[day == d]
        out[d] = (float(x.max()), x.idxmax())
    return out


def scada_tie(target, realign=True, loads=None):
    """The two transformer recorders' hourly energy against the historian's hourly feeder total for summer 2026:
    the ratio's mean and its scatter over the hours both systems hold."""
    loads = feeder_loads(target) if loads is None else loads
    sub = loads[(loads.index >= pd.Timestamp("2026-06-01")) & (loads.index < pd.Timestamp("2026-10-01"))]
    sub = sub.dropna().sum(axis=1)
    mv = mv90(target, realign)
    mv = mv[mv.RECORDER.isin(["41-2207", "41-2208"])].drop_duplicates(["RECORDER", "end"], keep="first")
    start = mv["end"] - CDT - pd.Timedelta(minutes=15)
    hr = mv.assign(h=start.dt.floor("h").values).groupby("h")["VALUE"].agg(["sum", "count"])
    hr = hr[hr["count"] == 8]["sum"] / 1000.0
    r = (hr / sub).dropna()
    return float(r.mean()), float(r.std()), len(r)


def solve(target=None):
    target = target or TARGET
    filed = Filed(target)
    loads = feeder_loads(target)
    obs = observations(target)
    wn = weather_normal(target, filed, loads, obs)
    rr = relief_rungs(target, filed, loads, obs)
    rungs = {"R0_no_cvr": 0.0, "R1_all_hours": rr["all_hours"], "R2_daily_peak_hour": rr["daily_peak_hour"],
             "golden": rr["golden"]}
    plans = {k: planning(wn["B"], v, filed) for k, v in rungs.items()}
    energy = feeder_energy(target)
    days, eleventh = hottest_days(target, obs=obs)
    peaks = demand_peaks(target, days)
    return {"filed": filed, "wn": wn, "relief": rr, "rungs": rungs, "plans": plans, "energy": energy,
            "days": days, "eleventh": eleventh, "peaks": peaks, "loads": loads, "obs": obs}


def main(target=None):
    S = solve(target)
    f, wn = S["filed"], S["wn"]
    print("firm %.1f MW, design %.0f F, block %.1f MW, growth %.2f%%, threshold %.0f F" %
          (f.firm, f.design, f.block, 100 * f.growth, f.threshold))
    print("weather-normal peak (2024 level) %.2f MW: slope %.3f MW/F over %d days" % (wn["B"], wn["slope"], wn["n_days"]))
    rr = S["relief"]
    print("relief: golden %.4f (hot hours on %d off %d), all hours %.4f, daily peak hour %.4f, no control %.4f / hot %.4f"
          % (rr["golden"], rr["n_hot_on"], rr["n_hot_off"], rr["all_hours"], rr["daily_peak_hour"],
             rr["no_control_all"], rr["no_control_hot"]))
    for lo, hi, r, a, b in relief_by_band(rr["P"]):
        print("  daily max %d-%d F, 16:00-21:00: relief %.4f (%d on, %d off)" % (lo, hi, r, a, b))
    for k, rows in S["plans"].items():
        print("%-20s" % k, " ".join("%d %.2f/%.1f" % (r["year"], r["peak"], r["transfer"]) for r in rows))
    print("feeder energy MWh:", {k: round(v, 2) for k, v in S["energy"].items()})
    print("hottest days:", [(d.strftime("%Y-%m-%d"), round(t, 2)) for d, t in S["days"].items()], "11th %.2f" % S["eleventh"])
    print("demand peaks:", [(d.strftime("%m-%d"), round(v, 3), t.strftime("%H:%M")) for d, (v, t) in S["peaks"].items()])


if __name__ == "__main__":
    main()
