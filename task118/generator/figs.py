"""Every graded figure, rung and ask, computed from the shipped files alone (never from world.py).

    import figs; fig = figs.compute("task118/target")
"""
import csv
import datetime as dt
import json
import math
import os
import re
from collections import defaultdict

import numpy as np

import build as B

MST_OFFSET = dt.timedelta(hours=7)
PROGS = ("Cool Credit", "Peak Time Rewards", "Business Demand Partners", "Home Battery Network")
SHORT = {"Cool Credit": "CC", "Peak Time Rewards": "PTR", "Business Demand Partners": "BDP",
         "Home Battery Network": "HBN"}
UNIT_NAME = {"Cool Credit": "premise", "Peak Time Rewards": "customer", "Business Demand Partners": "site",
             "Home Battery Network": "battery"}


def _rows(target, key):
    with open(os.path.join(target, B.FILES[key]), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _d(s):
    return dt.date.fromisoformat(s)


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- shared reads

def costs(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, B.FILES["costs"]), data_only=True)
    ws = wb["2027 expansion"]
    out, budget = {}, None
    for row in ws.iter_rows(values_only=True):
        if row and row[2] == "Total, all in":
            out[row[0]] = int(row[3])
        if row and isinstance(row[0], str) and row[0].startswith("2027 expansion line"):
            budget = int(row[3])
    return out, budget


def calendar(target):
    """Event dates from the event log (one row per programme per event) and each date's run day."""
    dates = sorted({_d(r["event_date"]) for r in _rows(target, "log")})
    s = set(dates)
    pos = {}
    for d in dates:
        k, x = 1, d - dt.timedelta(days=1)
        while x in s:
            k, x = k + 1, x - dt.timedelta(days=1)
        pos[d] = k
    return dates, pos


def calendar_by_log_order(target):
    """The run day read off the log's order with calendar gaps ignored (a rival construction, SF10)."""
    dates = sorted({_d(r["event_date"]) for r in _rows(target, "log")})
    pos, k = {}, 0
    for i, d in enumerate(dates):
        if i and dates[i - 1].year == d.year and (d - dates[i - 1]).days <= 3 and d.weekday() == 0 \
                and dates[i - 1].weekday() == 4:
            k += 1
        elif i and (d - dates[i - 1]).days == 1:
            k += 1
        else:
            k = 1
        pos[d] = k
    return pos


def weather(target):
    return {_d(r["DATE"]): (float(r["TMAX"]), float(r["TMIN"])) for r in _rows(target, "weather")}


def design(target):
    rows = _rows(target, "design")
    peak = max(rows, key=lambda r: int(r["forecast_system_load_mw"]))
    ts = dt.datetime.strptime(peak["hour_beginning_mst"], "%Y-%m-%d %H:%M")
    daily = defaultdict(float)
    for r in rows:
        t = dt.datetime.strptime(r["hour_beginning_mst"], "%Y-%m-%d %H:%M")
        daily[t.date()] = max(daily[t.date()], float(r["dry_bulb_f"]))
    hol = {dt.date(2027, 7, 5), dt.date(2027, 9, 6)}

    def called(d):
        return d.weekday() < 5 and d not in hol and daily.get(d, 0) >= 110.0
    k, x = 0, ts.date()
    while called(x):
        k, x = k + 1, x - dt.timedelta(days=1)
    prev3 = float(np.mean([daily[ts.date() - dt.timedelta(days=i)] for i in (1, 2, 3)]))
    lows = {}
    for r in rows:
        t = dt.datetime.strptime(r["hour_beginning_mst"], "%Y-%m-%d %H:%M")
        lows[t.date()] = min(lows.get(t.date(), 999.0), float(r["dry_bulb_f"]))
    return dict(peak=ts, peak_load=int(peak["forecast_system_load_mw"]), peak_temp=float(peak["dry_bulb_f"]),
                high=daily[ts.date()], low=lows[ts.date()], prev3=prev3, run_day=k,
                called=[d for d in sorted(daily) if called(d)])


# ---------------------------------------------------------------- per-event reductions per enrolled unit

def per_event(target, hour=18):
    """{programme: {event_date: kW per enrolled unit in the hour beginning `hour` MST}}; the batteries also carry
    their dispatch setting."""
    out = {p: {} for p in PROGS}
    sums = defaultdict(lambda: [0.0, 0, 0.0, 0])
    with open(os.path.join(target, B.FILES["cc_panel"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            t = _t(r["interval_start_utc"]) - MST_OFFSET
            if t.hour != hour:
                continue
            a = sums[t.date()]
            if r["assigned_group"] == "holdout":
                a[0] += float(r["kwh"]); a[1] += 1
            else:
                a[2] += float(r["kwh"]); a[3] += 1
    for d, a in sums.items():
        out["Cool Credit"][d] = a[0] / a[1] - a[2] / a[3]
    g = defaultdict(dict)
    for r in _rows(target, "ptr"):
        if int(r["hour_beginning_mst"][:2]) == hour:
            g[_d(r["event_date"])][r["group"]] = float(r["mean_kw"])
    for d, x in g.items():
        out["Peak Time Rewards"][d] = x["holdout"] - x["alerted"]
    s = defaultdict(list)
    for r in _rows(target, "bdp"):
        if int(r["hour_beginning_mst"][:2]) == hour:
            s[_d(r["event_date"])].append(float(r["verified_reduction_kw"]))
    for d, v in s.items():
        out["Business Demand Partners"][d] = float(np.mean(v))
    setting = {}
    for r in _rows(target, "fleet"):
        if int(r["hour_beginning_mst"][:2]) == hour:
            d = _d(r["event_date"])
            out["Home Battery Network"][d] = float(r["discharge_kw_ac"]) / int(r["batteries_enrolled"])
            setting[d] = float(r["dispatch_setting_kw"])
    return out, setting


def in_force(p, d, setting):
    """The rows a programme's 2027 figure may read: the batteries under the 3.0 kW setting in force for 2027."""
    return p != "Home Battery Network" or setting.get(d) == 3.0


def units(target):
    c, budget = costs(target)
    return {p: budget // c[p] for p in PROGS}, c, budget


def mw(per_unit_kw, n):
    return per_unit_kw * n / 1000.0


# ---------------------------------------------------------------- the rungs and every reflex route

def _fit(x, y, at):
    A = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in x])
    b = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)[0]
    return float(b[0] + np.dot(b[1:], at))


def routes(target, ev=None, setting=None, pos=None, wx=None, des=None):
    if ev is None:
        ev, setting = per_event(target)
    pos = pos or calendar(target)[1]
    wx = wx or weather(target)
    des = des or design(target)
    n = units(target)[0]
    prev3 = {}
    for d in pos:
        prev3[d] = float(np.mean([wx[d - dt.timedelta(days=i)][0] for i in (1, 2, 3) if d - dt.timedelta(days=i) in wx]))
    R = {}

    def per(p, f):
        return {p: f(p) for p in PROGS}

    def sel(p, all_years=False):
        return sorted(d for d in ev[p] if all_years or in_force(p, d, setting))
    R["R0 ex post, every event"] = {p: mw(np.mean([ev[p][d] for d in sel(p, True)]), n[p]) for p in PROGS}
    R["R0b ex post, rows in force"] = {p: mw(np.mean([ev[p][d] for d in sel(p)]), n[p]) for p in PROGS}
    R["R1 ex ante on the day's high"] = {p: mw(_fit([[wx[d][0] for d in sel(p)]], [ev[p][d] for d in sel(p)],
                                                    [des["high"]]), n[p]) for p in PROGS}
    R["R1b ex ante on the 18:00 temperature proxy (high)"] = R["R1 ex ante on the day's high"]
    R["R2 ex ante with the low and three days' heat"] = {
        p: mw(_fit([[wx[d][0] for d in sel(p)], [wx[d][1] for d in sel(p)], [prev3[d] for d in sel(p)]],
                   [ev[p][d] for d in sel(p)], [des["high"], des["low"], des["prev3"]]), n[p]) for p in PROGS}
    R["R2b ex ante with the low"] = {p: mw(_fit([[wx[d][0] for d in sel(p)], [wx[d][1] for d in sel(p)]],
                                                [ev[p][d] for d in sel(p)], [des["high"], des["low"]]), n[p])
                                     for p in PROGS}
    R["R2c ex ante with the three days' heat"] = {p: mw(_fit([[wx[d][0] for d in sel(p)], [prev3[d] for d in sel(p)]],
                                                             [ev[p][d] for d in sel(p)], [des["high"], des["prev3"]]),
                                                        n[p]) for p in PROGS}
    R["X hottest event days (115F and over)"] = {p: mw(np.mean([ev[p][d] for d in sel(p) if wx[d][0] >= 115.0]), n[p])
                                                 for p in PROGS}
    R["X day after an event"] = {p: mw(_fit([[wx[d][0] for d in sel(p)], [float(pos[d] > 1) for d in sel(p)]],
                                            [ev[p][d] for d in sel(p)], [des["high"], 1.0]), n[p]) for p in PROGS}
    R["X tenth percentile of events"] = {p: mw(float(np.percentile([ev[p][d] for d in sel(p)], 10)), n[p])
                                         for p in PROGS}
    R["X most recent season"] = {p: mw(np.mean([ev[p][d] for d in sel(p) if d.year == 2026]), n[p]) for p in PROGS}
    R["F run day as a count"] = {p: mw(_fit([[wx[d][0] for d in sel(p)], [pos[d] for d in sel(p)]],
                                            [ev[p][d] for d in sel(p)], [des["high"], des["run_day"]]), n[p])
                                 for p in PROGS}
    R["F run-day indicators with the high"] = {
        p: mw(_fit([[wx[d][0] for d in sel(p)]] + [[float(pos[d] == k) for d in sel(p)] for k in (2, 3, 4)],
                   [ev[p][d] for d in sel(p)], [des["high"], 0, 0, 1]), n[p]) for p in PROGS}
    R["F ratio model on run days"] = {}
    for p in PROGS:
        ds = sel(p)
        y = np.log(np.maximum([ev[p][d] for d in ds], 1e-6))
        A = np.column_stack([np.ones(len(ds)), [wx[d][0] for d in ds]] + [[float(pos[d] == k) for d in ds]
                                                                          for k in (2, 3, 4)])
        b = np.linalg.lstsq(A, y, rcond=None)[0]
        R["F ratio model on run days"][p] = mw(float(np.exp(b[0] + b[1] * des["high"] + b[4])), n[p])
    R["G fourth-day mean (golden)"] = {p: mw(np.mean([ev[p][d] for d in sel(p) if pos[d] == des["run_day"]]), n[p])
                                       for p in PROGS}
    R["F fourth-day mean, rows in force pooled for the batteries"] = dict(R["G fourth-day mean (golden)"])
    R["F fourth-day mean, rows in force pooled for the batteries"]["Home Battery Network"] = \
        R["R0b ex post, rows in force"]["Home Battery Network"]
    return R


def winner(d):
    r = sorted(d.items(), key=lambda kv: -kv[1])
    return r[0][0], r[0][1] / r[1][1], r


# ---------------------------------------------------------------- ask A: Cool Credit premises online at 16:00

ABBR = {"W": "WEST", "E": "EAST", "N": "NORTH", "S": "SOUTH", "DR": "DRIVE", "RD": "ROAD", "LN": "LANE",
        "ST": "STREET", "AVE": "AVENUE", "CT": "COURT", "PL": "PLACE", "BLVD": "BOULEVARD", "TRL": "TRAIL"}


def norm_address(a):
    a = a.upper().replace("#", " UNIT ").replace(",", " ")
    toks = [ABBR.get(t, t) for t in a.split()]
    return " ".join(toks)


def _status(target):
    st = defaultdict(list)
    with open(os.path.join(target, B.FILES["status"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            st[r["serial"]].append((_t(r["changed_at_utc"]), r["status"]))
    for k in st:
        st[k].sort()
    return st


def ask_a(target, link="address", idle="switch", data=None):
    cis = data["cis"] if data else _rows(target, "cis")
    reg = data["reg"] if data else json.load(open(os.path.join(target, B.FILES["registry"]), encoding="utf-8"))["devices"]
    st = data["st"] if data else _status(target)
    switch = None
    if idle == "switch":
        switch = idle_switch(target, st)
    by_addr = defaultdict(list)
    for d in reg:
        by_addr[norm_address(d["install_address"]) if link == "address" else d["install_address"]].append(d)
    by_serial = {d["serial"]: d for d in reg}
    dates = [d for d in calendar(target)[0] if d.year == 2026]
    out = {}
    for d in dates:
        t = dt.datetime(d.year, d.month, d.day, 16) + MST_OFFSET
        n = 0
        for c in cis:
            if _d(c["enrolled_on"]) > d or (c["unenrolled_on"] and _d(c["unenrolled_on"]) <= d):
                continue
            devs = [by_serial[c["thermostat_serial"]]] if c["thermostat_serial"] in by_serial else []
            if link != "serial":
                key = norm_address(c["service_address"]) if link == "address" else c["service_address"]
                devs = devs + [x for x in by_addr.get(key, []) if x["serial"] != c["thermostat_serial"]]
            on = False
            for x in devs:
                if _t(x["registered_at"]) > t or (x["retired_at"] and _t(x["retired_at"]) <= t):
                    continue
                last = None
                for ts, s in st.get(x["serial"], []):
                    if ts <= t:
                        last = (ts, s)
                    else:
                        break
                if last is None:
                    continue
                if last[1] == "ONLINE" or (last[1] == "IDLE" and (idle == "online" or
                                                                   (idle == "switch" and last[0].date() >= switch))):
                    on = True
                    break
            n += on
        out[d] = n
    return out


def idle_switch(target, st=None):
    """The first 2026 event date on which a device whose standing status was IDLE at the 14:00 command did not
    appear on Halvern's unreachable report: the day IDLE starts meaning connected."""
    st = st or _status(target)
    un = defaultdict(set)
    for r in _rows(target, "unreachable"):
        un[_d(r["event_date"])].add(r["serial"])
    dates = sorted(un)
    for d in dates:
        t = dt.datetime(d.year, d.month, d.day, 14) + MST_OFFSET
        idle, answered = 0, 0
        for ser, seq in st.items():
            last = None
            for ts, s in seq:
                if ts <= t:
                    last = s
                else:
                    break
            if last == "IDLE":
                idle += 1
                answered += ser not in un[d]
        if idle and answered / idle > 0.5:
            return d
    return None


# ---------------------------------------------------------------- ask B: Home Battery Network incentives

def schedule2(target):
    """The event incentive and the season cap, read off schedule 2 of the participation agreement."""
    from pypdf import PdfReader
    txt = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in
                                        PdfReader(os.path.join(target, B.FILES["hbn_terms"])).pages))
    earn = int(re.search(r"the premise earns USD (\d+)", txt).group(1))
    cap = int(re.search(r"at most USD (\d+) in a season", txt).group(1))
    return earn, cap


def ask_b(target, split="combine", month="event", dedupe=True, premise="register", count="event"):
    EARN, CAP = schedule2(target)
    recs = _rows(target, "dispatch")
    if count == "record":
        months, per_key = defaultdict(int), defaultdict(int)
        for r in recs:
            s, e = _t(r["dispatch_start_utc"]), _t(r["dispatch_end_utc"])
            if (e - s).total_seconds() / 3600.0 >= 3.0 and per_key[r["enrolment_no"]] + EARN <= CAP:
                per_key[r["enrolment_no"]] += EARN
                months[(s - MST_OFFSET).month] += EARN
        return {m: months.get(m, 0) for m in (6, 7, 8, 9)}, sum(v >= CAP for v in per_key.values())
    if dedupe:
        seen, keep = set(), []
        for r in recs:
            k = tuple(r.values())
            if k not in seen:
                seen.add(k)
                keep.append(r)
        recs = keep
    reg = _rows(target, "interconnect")
    prem = {r["battery_serial"]: r["premise_id"] for r in reg}
    dates = [d for d in calendar(target)[0] if d.year == 2026]
    per = defaultdict(lambda: defaultdict(list))        # (battery) -> event date -> [hours]
    settled = {}
    for r in recs:
        s, e = _t(r["dispatch_start_utc"]), _t(r["dispatch_end_utc"])
        d = (s - MST_OFFSET).date()
        per[r["battery_serial"]][d].append((s, (e - s).total_seconds() / 3600.0))
        settled[(r["battery_serial"], d)] = _d(r["settled_on"])
    qual = defaultdict(set)                              # premise or battery key -> event dates qualifying
    for bat, evs in per.items():
        key = prem.get(bat, bat) if premise == "register" else bat
        for d, parts in evs.items():
            parts.sort()
            if split == "combine":
                ok = sum(h for _, h in parts) >= 3.0
            elif split == "keep_first":
                ok = parts[0][1] >= 3.0
            else:
                ok = any(h >= 3.0 for _, h in parts)
            if ok:
                qual[key].add((d, settled[(bat, d)]))
    months = defaultdict(int)
    capped = 0
    for key, evs in qual.items():
        paid = 0
        for d, sd in sorted(evs):
            if paid + EARN > CAP:
                continue
            paid += EARN
            months[(sd if month == "settled" else d).month] += EARN
        capped += paid >= CAP
    return {m: months.get(m, 0) for m in (6, 7, 8, 9)}, capped


# ---------------------------------------------------------------- ask C: Business Demand Partners nominations

def ask_c(target, dedupe="meter", territory="register"):
    rows = _rows(target, "nominations")
    meters = {r["meter_no"] for r in _rows(target, "meters")}
    out = {}
    for m in (6, 7, 8, 9):
        mr = [r for r in rows if r["month"] == "2026-%02d" % m]
        if territory == "register":
            mr = [r for r in mr if r["meter_no"] in meters]
        if dedupe == "none":
            out[m] = sum(float(r["nominated_kw"]) for r in mr)
            continue
        key = "meter_no" if dedupe == "meter" else "arroyo_site_ref"
        last = {}
        for r in sorted(mr, key=lambda r: r["submitted_at_utc"]):
            last[r[key]] = float(r["nominated_kw"])
        out[m] = sum(last.values())
    return out


# ---------------------------------------------------------------- everything the write-up and goldens state

def compute(target):
    dates, pos = calendar(target)
    ev, setting = per_event(target)
    wx = weather(target)
    des = design(target)
    n, c, budget = units(target)
    R = routes(target, ev, setting, pos, wx, des)
    fourth = {p: [d for d in sorted(ev[p]) if pos[d] == des["run_day"] and in_force(p, d, setting)] for p in PROGS}
    per_unit = {p: float(np.mean([ev[p][d] for d in fourth[p]])) for p in PROGS}
    first = {p: float(np.mean([ev[p][d] for d in sorted(ev[p]) if pos[d] == 1 and in_force(p, d, setting)]))
             for p in PROGS}
    mwv = {p: mw(per_unit[p], n[p]) for p in PROGS}
    call, lead, ranked = winner(mwv)
    a = ask_a(target)
    b_month, b_cap = ask_b(target)
    cm = ask_c(target)
    earn, cap = schedule2(target)
    fig = {
        "budget_usd": budget,
        "budget_usd_millions": round(budget / 1e6, 1),
        "hbn_incentive_usd": earn,
        "hbn_cap_usd": cap,
        "cost_usd": c,
        "units": n,
        "design_peak": des["peak"].strftime("%Y-%m-%d %H:%M"),
        "design_peak_load_mw": des["peak_load"],
        "design_peak_temp_f": des["peak_temp"],
        "design_day_high_f": des["high"],
        "design_run_day": des["run_day"],
        "design_called_days": [d.isoformat() for d in des["called"] if (des["peak"].date() - d).days in range(0, 7)],
        "fourth_days": {p: [d.isoformat() for d in fourth[p]] for p in PROGS},
        "per_unit_kw_fourth_day": {p: round(per_unit[p], 4) for p in PROGS},
        "per_unit_kw_first_day": {p: round(first[p], 4) for p in PROGS},
        "fourth_over_first": {p: round(per_unit[p] / first[p], 3) for p in PROGS},
        "mw_exact": {p: round(mwv[p], 3) for p in PROGS},
        "mw": {p: int(round(mwv[p])) for p in PROGS},
        "call": call,
        "runner_up": ranked[1][0],
        "lead": round(lead, 3),
        "gap_mw": int(round(mwv[call])) - int(round(mwv[ranked[1][0]])),
        "ladder": {k: {p: round(v, 2) for p, v in d.items()} for k, d in R.items()},
        "ask_a": {d.isoformat(): a[d] for d in sorted(a)},
        "ask_b_months": {"2026-%02d" % m: v for m, v in b_month.items()},
        "ask_b_capped": b_cap,
        "ask_c_months": {"2026-%02d" % m: round(v, 1) for m, v in cm.items()},
        "ask_c_months_whole": {"2026-%02d" % m: int(round(v)) for m, v in cm.items()},
        "events_by_season": {str(y): sum(1 for d in dates if d.year == y) for y in (2024, 2025, 2026)},
        "battery_pooled_kw": round(float(np.mean([ev["Home Battery Network"][d] for d in ev["Home Battery Network"]
                                                  if in_force("Home Battery Network", d, setting)])), 4),
    }
    return fig


def write(fig, path):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=False, default=str)
        fh.write("\n")
