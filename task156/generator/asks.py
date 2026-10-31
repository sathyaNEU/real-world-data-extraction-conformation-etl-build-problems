"""The asks, computed from target/ alone, with a switch for each handling a response might take.

Ask A, the catchment's residential water use per dwelling per day in each quarter, January 2024 to September 2026:
the Water Metering and Billing Policy's measure, each meter's consumption between consecutive actual readings spread
evenly over the days between them, over the quarter's days and the dwellings the meters supplied on average over the
quarter. dwellings="dated" counts each rating unit's separately used or inhabited parts as they stood each day (the
rating snapshot less the parts whose code compliance certificate came later); "snapshot" carries the 31 October 2026
counts back over every quarter.

Ask B, each pump station's wet weather overflows and spill hours in 2024 and 2025 apart from PS03, and the network's
emergency overflows in each year: the consent's conditions 3 and 5 executed on the overflow monitors' messages, the
monitors' installation history and the lines company's outages. icps="all" matches outages to a station through every
ICP the council's electricity site list gives its address; "current" through the asset register's current ICP."""
from __future__ import annotations

import csv
import datetime as dt
import functools
import os
import re
import zoneinfo

import numpy as np

AKL = zoneinfo.ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
NZST = dt.timezone(dt.timedelta(hours=12))
QUARTERS = [(y, q) for y in (2024, 2025, 2026) for q in (1, 2, 3, 4) if (y, q) <= (2026, 3)]
STATIONS_B = ["PS01", "PS02", "PS04", "PS05", "PS06"]
YEARS_B = (2024, 2025)


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.reader(f))


def qbounds(y, q):
    a = dt.date(y, 3 * q - 2, 1)
    b = dt.date(y + (q == 4), 1 if q == 4 else 3 * q + 1, 1)
    return a, b


@functools.lru_cache(maxsize=8)
def ask_a(target, dwellings="dated", spread="from_read_day", estimates=False):
    return water_use(rows(os.path.join(target, "water_accounts_2026-11.csv"))[1:],
                     rows(os.path.join(target, "rating_information_2026-10-31.csv"))[1:],
                     rows(os.path.join(target, "building_consents_2023-2026.csv"))[1:],
                     rows(os.path.join(target, "water_meter_reads_2023-2026.csv"))[1:],
                     dwellings=dwellings, spread=spread, estimates=estimates)


def water_use(accts, rating_rows, bcs, read_rows, dwellings="dated", spread="from_read_day", estimates=False,
              with_dwellings=False):
    rating = {r[0]: (r[2], int(r[3])) for r in rating_rows}
    later = {}
    for c, v, a, w, n, gr, ccc in bcs:
        if n == "1" and ccc:
            later.setdefault(v, []).append(dt.date.fromisoformat(ccc))
    meter_rus = {}
    for a, v, m, s, o, c in accts:
        meter_rus.setdefault(m, set()).add(v)
    res_meters = {m for m, vs in meter_rus.items() if all(rating.get(v, ("", 0))[0] == "Residential" for v in vs)}
    reads = {}
    for no, serial, d, val, t in read_rows:
        if no not in res_meters:
            continue
        if t == "E" and not estimates:
            continue
        reads.setdefault(no, []).append((dt.datetime.strptime(d, "%d/%m/%Y").date(), t, float(val)))
    d0 = dt.date(2024, 1, 1)
    d1 = dt.date(2026, 10, 1)
    n = (d1 - d0).days
    use = np.zeros(n)
    for no, rs in reads.items():
        rs.sort(key=lambda r: (r[0], {"A": 0, "E": 0, "R": 1, "I": 2}[r[1]]))
        for (da, ta, va), (db, tb, vb) in zip(rs, rs[1:]):
            if ta == "R" and tb == "I":
                continue
            days = (db - da).days
            if days <= 0:
                continue
            per = (vb - va) * 1000.0 / days
            a0, b0 = (da, db) if spread == "from_read_day" else (da + dt.timedelta(days=1), db + dt.timedelta(days=1))
            i0 = max(0, (a0 - d0).days)
            i1 = min(n, (b0 - d0).days)
            if i1 > i0:
                use[i0:i1] += per
    dw = np.zeros(n)
    for m in res_meters:
        for v in meter_rus[m]:
            s_now = rating[v][1]
            adds = sorted(later.get(v, []))
            if dwellings == "snapshot":
                dw += s_now
            else:
                arr = np.full(n, float(s_now))
                for a in adds:
                    j = (a - d0).days
                    if j > 0:
                        arr[:min(j, n)] -= 1
                dw += np.maximum(arr, 0)
    out = {}
    for y, q in QUARTERS:
        a, b = qbounds(y, q)
        i0, i1 = (a - d0).days, (b - d0).days
        val = float(use[i0:i1].sum() / (i1 - i0) / dw[i0:i1].mean())
        out["%d Q%d" % (y, q)] = (val, i1 - i0, float(dw[i0:i1].mean()), a, b) if with_dwellings else val
    return out


SMS_RE = re.compile(r"^(OM-\d{4}) (SPILL START|SPILL STOP) EO (\d\d:\d\d) (\d\d/\d\d/\d\d)$")


@functools.lru_cache(maxsize=8)
def ask_b(target, icps="all", attribution="dated", clock="message"):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, "rauwhero_wastewater_assets_2026-10.xlsx"), read_only=True)
    mons = []
    cur_icp, addr = {}, {}
    for i, r in enumerate(wb["Overflow monitors"].iter_rows(values_only=True)):
        if i and r[0]:
            mons.append((r[0], r[1], dt.date.fromisoformat(r[2]), dt.date.fromisoformat(r[3]) if r[3] else None))
    for i, r in enumerate(wb["Pump stations"].iter_rows(values_only=True)):
        if i and r[0]:
            cur_icp[r[0]] = r[4]
            addr[r[0]] = r[2]
    site_icps = {s: {cur_icp[s]} for s in cur_icp}
    if icps == "all":
        for icp, site, ad, a, b, cat in rows(os.path.join(target, "council_electricity_sites_2026-10.csv"))[1:]:
            for s, a_ in addr.items():
                if ad.startswith(a_ + ","):
                    site_icps[s].add(icp)
    outages = []
    for nid, icp, typ, a, b, cause in rows(os.path.join(target, "kahuwera_lines_outage_notices_2024-2026.csv"))[1:]:
        ta = dt.datetime.strptime(a, "%Y-%m-%d %H:%M").replace(tzinfo=AKL).astimezone(UTC)
        tb = dt.datetime.strptime(b, "%Y-%m-%d %H:%M").replace(tzinfo=AKL).astimezone(UTC)
        for s, ic in site_icps.items():
            if icp in ic:
                outages.append((s, ta, tb))

    def station_of(serial, d):
        if attribution == "dated":
            for ser, s, a, b in mons:
                if ser == serial and a <= d and (b is None or d < b):
                    return s
        else:
            cands = [m for m in mons if m[0] == serial]
            return cands[-1][1]
        return None

    events = {}
    for rec, frm, msg in rows(os.path.join(target, "overflow_monitor_sms_log_2024-2026.csv"))[1:]:
        m = SMS_RE.match(msg)
        if not m:
            continue
        if clock == "message":
            t = dt.datetime.strptime(m.group(3) + " " + m.group(4), "%H:%M %d/%m/%y").replace(tzinfo=NZST).astimezone(UTC)
        else:
            t = dt.datetime.strptime(rec, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        s = station_of(m.group(1), t.astimezone(NZST).date())
        events.setdefault(s, []).append((t, m.group(2)))
    runs = {}
    for s, evs in events.items():
        evs.sort()
        cur = None
        for t, w in evs:
            if w == "SPILL START":
                cur = t
            elif cur is not None:
                runs.setdefault(s, []).append((cur, t))
                cur = None
    res = {}
    emerg = {y: 0 for y in YEARS_B}
    for s, rs in runs.items():
        ovf = []
        for a, b in rs:
            if ovf and (a - ovf[-1]["end"]) < dt.timedelta(hours=24):
                ovf[-1]["end"] = max(ovf[-1]["end"], b)
                ovf[-1]["hours"] += (b - a).total_seconds() / 3600
            else:
                ovf.append(dict(start=a, end=b, hours=(b - a).total_seconds() / 3600))
        for o in ovf:
            o["emergency"] = any(x == s and ta <= o["start"] < tb for x, ta, tb in outages)
            y = o["start"].astimezone(NZST).year
            if y in YEARS_B:
                if o["emergency"]:
                    emerg[y] += 1
                elif s in STATIONS_B:
                    k = (s, y)
                    c, h = res.get(k, (0, 0.0))
                    res[k] = (c + 1, h + o["hours"])
    out = {}
    for s in STATIONS_B:
        for y in YEARS_B:
            c, h = res.get((s, y), (0, 0.0))
            out["%s %d overflows" % (s, y)] = c
            out["%s %d spill hours" % (s, y)] = h
    for y in YEARS_B:
        out["network %d emergency overflows" % y] = emerg[y]
    return out
