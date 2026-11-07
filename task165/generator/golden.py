"""task165 architecture 2: the golden, read back from the shipped pack alone (no world state).

    the call     Outfall 014's 15-minute overflow record (both loggers on UTC, cubic feet per second converted),
                 replayed through each TM-7 tank that fills from the overflow and, once the overflow has stopped, is
                 pumped back at the lesser of its station's firm capacity and the Southside plant's room (its 140 MGD
                 headworks capacity less the historian's hourly influent, the hour held over its four quarter hours);
                 events counted with Appendix C's 24-hour rule over the twelve years.
    ask 1        each gauge's 2025 rainfall by local month: duplicate re-sent tips dropped, each calibration pour (a
                 steady run of tips on a visit the field log says carried a cal check) removed, every logger's clock
                 taken to local time (Eastern Standard Time on the original loggers, UTC on the cellular ones), RG-4's
                 tips at 0.2 mm after the mechanism swap.
    ask 2        the Northside tank's returned volume by local year, a mass balance on each quarter hour a pump ran:
                 the fall in storage (the level transducer through the O&M manual's stage-storage table, the
                 re-mounted transducer's 0.45 ft taken off from its re-installation) plus the inflow FIT-600 metered
                 into the tank meanwhile (storm tails, and the dry weather flow SG-600 passed while its seals failed)."""
import csv
import datetime as dt
import os
import re
import sys
import zoneinfo

import numpy as np
import openpyxl
import pyarrow.parquet as pq

NY = zoneinfo.ZoneInfo("America/New_York")
UTC = dt.timezone.utc
EST = dt.timezone(dt.timedelta(hours=-5))
T0 = dt.datetime(2014, 1, 1, 5, 0, tzinfo=UTC)
N = 420768
NH = N // 4
CAP = 140.0
ALTS = [("A", 19.0, 23.0), ("B", 26.0, 31.0), ("C", 38.0, 45.0), ("D", 50.0, 60.0)]
YEARS = 12
CFS = 0.646317


def q_index(u):
    return int((u - T0).total_seconds() // 900)


# ----------------------------------------------------------------------------------------------- readers
def read_meter(target):
    t = pq.read_table(os.path.join(target, "outfall_014_flow_monitoring_2014-2025.parquet")).to_pydict()
    o = np.full(N, np.nan)
    for lg, ts, v, un in zip(t["logger_id"], t["reading_time"], t["flow"], t["flow_unit"]):
        if un == "cfs":
            u = dt.datetime.strptime(ts, "%m/%d/%Y %H:%M").replace(tzinfo=EST).astimezone(UTC)
            val = v * CFS
        else:
            u = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
            val = v
        i = q_index(u)
        if 0 <= i < N:
            if np.isnan(o[i]) or val > o[i]:
                o[i] = val
    assert not np.isnan(o).any(), "every quarter hour metered"
    return o


def local_to_utc_rows(times):
    """Local wall times in file order to UTC: a repeated hour's second pass is the standard-time one."""
    out = []
    seen = {}
    for s in times:
        d = dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
        k = seen.get(s, 0)
        seen[s] = k + 1
        out.append(d.replace(tzinfo=NY, fold=1 if k else 0).astimezone(UTC))
    return out


def read_plant(target, prefix="SS", bad="interpolate"):
    times, vals, qual = [], [], []
    with open(os.path.join(target, "wrp_influent_hourly_2014-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["tag"].startswith(prefix):
                times.append(r["time_local"])
                vals.append(float(r["value_mgd"]))
                qual.append(r["quality"])
    us = local_to_utc_rows(times)
    h = np.full(NH, np.nan)
    for u, v, q in zip(us, vals, qual):
        k = int((u - T0).total_seconds() // 3600)
        if 0 <= k < NH:
            h[k] = v if (q == "GOOD" or bad == "zero") else np.nan
    if np.isnan(h).any():
        idx = np.arange(NH)
        ok = ~np.isnan(h)
        h = np.interp(idx, idx[ok], h[ok])
    return h


# ----------------------------------------------------------------------------------------------- replay
def replay(inflow, vol, pump, room=None, during=False):
    dtd = 15 / 1440.0
    out = np.zeros(len(inflow))
    s = 0.0
    lim = np.full(len(inflow), pump) if room is None else np.minimum(pump, np.maximum(0.0, room))
    for i in range(len(inflow)):
        q = inflow[i] * dtd
        if q > 0:
            take = min(vol - s, q)
            s += take
            out[i] = (q - take) / dtd
            if during and s > 0:
                s -= min(s, lim[i] * dtd)
        elif s > 0:
            s -= min(s, lim[i] * dtd)
    return out


def events(series, gap_steps=96):
    on = np.flatnonzero(series > 1e-9)
    if len(on) == 0:
        return 0
    return 1 + int((np.diff(on) > gap_steps).sum())


def event_volumes(series, gap_steps=96):
    on = np.flatnonzero(series > 1e-9)
    if len(on) == 0:
        return []
    cut = np.flatnonzero(np.diff(on) > gap_steps)
    starts = [on[0]] + [on[c + 1] for c in cut]
    ends = [on[c] for c in cut] + [on[-1]]
    return [series[a:b + 1].sum() / 96 for a, b in zip(starts, ends)]


def solve_call(target, room_hours=None, shift=0, cap=CAP, during=False):
    o = read_meter(target)
    ss = read_plant(target) if room_hours is None else room_hours
    room = np.repeat(cap - np.roll(ss, shift), 4)
    res = {}
    for lab, v, p in ALTS:
        res[lab] = events(replay(o, v, p, room, during)) / YEARS
    pick = next((lab for lab, _, _ in ALTS if res[lab] <= 4.0), None)
    return pick, res


def ladder(target):
    o = read_meter(target)
    vols = event_volumes(o)
    r0 = {lab: sum(1 for x in vols if x > v) / YEARS for lab, v, _ in ALTS}
    r1 = {lab: events(replay(o, v, p)) / YEARS for lab, v, p in ALTS}
    r1b = {lab: events(replay(o, v, p, during=True)) / YEARS for lab, v, p in ALTS}
    return dict(raw=events(o) / YEARS, r0=r0, r1=r1, r1b=r1b)


# ----------------------------------------------------------------------------------------------- ask 1
GAUGE_NEW = {"RG-3": dt.datetime(2024, 5, 7), "RG-4": dt.datetime(2024, 5, 8)}
TIP_02MM = 0.2 / 25.4


def read_visits(target):
    wb = openpyxl.load_workbook(os.path.join(target, "rain_gauge_field_service_2014-2025.xlsx"), read_only=True)
    ws = wb["Visits"]
    out = []
    for r in list(ws.iter_rows(values_only=True))[1:]:
        d, g, tech, a, b, note = r
        d = d if isinstance(d, dt.datetime) else dt.datetime.combine(d, dt.time())
        ha, ma = map(int, a.split(":"))
        hb, mb = map(int, b.split(":"))
        out.append(dict(gauge=g, arrive=d.replace(hour=ha, minute=ma), depart=d.replace(hour=hb, minute=mb), note=note))
    return out


def tips_local(target, handle_clock=True, dedupe=True):
    """Each gauge's tips as local wall times, in file order."""
    rows = []
    with open(os.path.join(target, "rain_gauge_tips_2014-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            rows.append((r["gauge_id"], r["tip_time"]))
    if dedupe:
        rows = list(dict.fromkeys(rows))
    out = {}
    for g, s in rows:
        d = dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        if handle_clock:
            new = GAUGE_NEW.get(g)
            # the cellular loggers stamp UTC; their first tip comes after the install visit
            if new is not None and d >= new.replace(hour=12):
                loc = d.replace(tzinfo=UTC).astimezone(NY).replace(tzinfo=None)
            else:
                loc = d.replace(tzinfo=EST).astimezone(NY).replace(tzinfo=None)
        else:
            loc = d
        out.setdefault(g, []).append(loc)
    for g in out:
        out[g].sort()
    return out


def pour_runs(times, lo, hi, min_len=20, gmin=5.0, gmax=20.0):
    """Indices of steady runs of tips (every gap between gmin and gmax seconds, at least min_len tips) starting in
    [lo, hi]."""
    idx = []
    j = 0
    n = len(times)
    while j < n:
        if times[j] < lo:
            j += 1
            continue
        if times[j] > hi:
            break
        k = j
        while k + 1 < n and gmin <= (times[k + 1] - times[k]).total_seconds() <= gmax:
            k += 1
        if k - j + 1 >= min_len:
            idx.extend(range(j, k + 1))
            j = k + 1
        else:
            j += 1
    return idx


def ask1(target, handle_clock=True, dedupe=True, pours="steady", bucket=True):
    tips = tips_local(target, handle_clock, dedupe)
    visits = read_visits(target)
    out = {}
    for g, ts in tips.items():
        drop = set()
        if pours != "keep":
            for v in visits:
                if v["gauge"] != g or "cal check" not in v["note"].lower() or "no cal check" in v["note"].lower():
                    continue
                if pours == "steady":
                    lo = v["arrive"] - dt.timedelta(hours=6)
                    hi = v["depart"] + dt.timedelta(hours=6)
                    drop.update(pour_runs(ts, lo, hi))
                else:   # the visit window as logged
                    drop.update(j for j, t in enumerate(ts) if v["arrive"] <= t <= v["depart"])
        # a gauge's 0.2 mm mechanism counts from the visit the field log records it on
        swaps = [v["arrive"] for v in visits if v["gauge"] == g and "0.2mm" in v["note"].replace(" mm", "mm")]
        swap = min(swaps) if (swaps and bucket) else dt.datetime(2100, 1, 1)
        m = np.zeros(12)
        for j, t in enumerate(ts):
            if j in drop or t.year != 2025:
                continue
            b = TIP_02MM if t >= swap else 0.01
            m[t.month - 1] += b
        out[g] = m
    return out


# ----------------------------------------------------------------------------------------------- ask 2
def stage_table(target):
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, "northside_tank_om_manual_section4.pdf")).pages)
    tail = txt.split("Table 4-1. Tank stage-storage")[-1]
    pairs = re.findall(r"(\d+\.\d\d)\s+(\d+\.\d{4})", tail)
    h = np.array([float(a) for a, _ in pairs])
    v = np.array([float(b) for _, b in pairs])
    return h, v


def ask2(target, offset=True, inflow=True, years=range(2021, 2026)):
    h_tab, v_tab = stage_table(target)
    rows = []
    with open(os.path.join(target, "northside_tank_scada_2020-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    remount = dt.datetime(2023, 8, 23, 11, 0)
    # the re-mounted transducer's reading of an empty tank
    floor = min(float(r["NT_LIT601_FT"]) for r in rows
                if r["NT_LIT601_FT"] and r["Timestamp"] >= remount.strftime("%Y-%m-%d %H:%M"))
    tot = {y: 0.0 for y in years}
    prev = None
    for r in rows:
        if not r["NT_LIT601_FT"]:
            prev = None
            continue
        t = dt.datetime.strptime(r["Timestamp"], "%Y-%m-%d %H:%M")
        lv = float(r["NT_LIT601_FT"])
        if offset and t >= remount:
            lv -= floor
        pumping = r["NT_P1_RUN"] == "1" or r["NT_P2_RUN"] == "1" or r["NT_P3_RUN"] == "1"
        if prev is not None and pumping and t.year in tot:
            # what the pumps returned is the fall in storage plus what flowed in meanwhile (FIT-600)
            d = float(np.interp(prev, h_tab, v_tab)) - float(np.interp(lv, h_tab, v_tab))
            if inflow:
                d += float(r["NT_FIT600_MGD"]) / 96.0
            elif d < 0:
                d = 0.0
            tot[t.year] += d
        prev = lv
    return tot, floor


def solve(target):
    pick, ev = solve_call(target)
    return dict(pick=pick, events=ev, ladder=ladder(target), ask1=ask1(target), ask2=ask2(target)[0])


if __name__ == "__main__":
    tg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    r = solve(tg)
    print("pick", r["pick"], {k: round(v, 2) for k, v in r["events"].items()})
    print("ladder", {k: ({a: round(b, 2) for a, b in v.items()} if isinstance(v, dict) else round(v, 2)) for k, v in r["ladder"].items()})
    for g, m in r["ask1"].items():
        print(g, np.round(m, 3))
    print("ask2", {y: round(v, 2) for y, v in r["ask2"].items()})
