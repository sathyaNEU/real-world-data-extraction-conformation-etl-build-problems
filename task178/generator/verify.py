"""task178 independent verifier: reads only the shipped bundle, on its own code path (csv module, its own reading of
the tide-table layouts and the PDFs), and recomputes the deck elevation, its two expected counts, the default path,
the five survival tides and the street closures against generator/figures.json. Exit 1 on any difference.

    python3 task178/generator/verify.py task178/target"""
from __future__ import annotations

import bisect
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FT = 0.3048
BAD = []


def chk(label, cond, detail=""):
    print("%s  %-56s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        BAD.append(label)


def text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def sunday(y, m, n=1, last=False):
    if last:
        d = dt.date(y, m + 1, 1) - dt.timedelta(days=1)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def to_utc(loc):
    y = loc.year
    a, b = (sunday(y, 3, 2), sunday(y, 11, 1)) if y >= 2007 else (sunday(y, 4, 1), sunday(y, 10, last=True))
    a = dt.datetime(a.year, a.month, a.day, 2); b = dt.datetime(b.year, b.month, b.day, 1)
    return loc + dt.timedelta(hours=4 if a <= loc < b else 5)


def utc_to_local(u):
    for off in (4, 5):
        loc = u - dt.timedelta(hours=off)
        if to_utc(loc) == u:
            return loc
    return u - dt.timedelta(hours=5)


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    names = {f.split("_")[0] + f.split("_")[1]: f for f in os.listdir(target)}
    f_ver = next(f for f in os.listdir(target) if "verified" in f)
    f_tel = next(f for f in os.listdir(target) if "telemetry" in f)
    f_tab = next(f for f in os.listdir(target) if "tide_tables" in f)
    f_dat = next(f for f in os.listdir(target) if "datum_sheet" in f)
    f_slr = next(f for f in os.listdir(target) if "sea_level" in f)
    f_bas = next(f for f in os.listdir(target) if "design_basis" in f)
    f_clo = next(f for f in os.listdir(target) if "closures" in f)
    f_log = next(f for f in os.listdir(target) if "station_log" in f)

    dtxt = text(os.path.join(target, f_dat))
    stnd95 = float(re.search(r"STND \(1995\) is ([\d.]+) ft below MLLW", dtxt).group(1))
    stnd26 = float(re.search(r"STND 2026 is ([\d.]+) ft below MLLW", dtxt).group(1))
    msl_epoch = float(re.search(r"\n\s*MSL\s+[\d.]+\s+([\d.]+)", dtxt).group(1))
    lev = re.search(r"2018-03-12\s+brought forward\s+(-?[\d.]+) ft", dtxt)
    chk("datum sheet read (positive control)", stnd95 > 0 and lev is not None, "%s %s %s" % (stnd95, stnd26, msl_epoch))
    offset_2018 = -float(lev.group(1))
    wb = openpyxl.load_workbook(os.path.join(target, f_log), read_only=True)
    log = {str(r[0]): str(r[2]) for r in list(wb.active.iter_rows(values_only=True))[1:]}
    m = re.search(r"re-secured (\d\d)(\d\d)", log["2017-10-30"]); m2 = re.search(r"reference (\d\d)(\d\d)", log["2018-03-12"])
    t_fail = dt.datetime(2017, 10, 30, int(m.group(1)), int(m.group(2)))
    t_reset = dt.datetime(2018, 3, 12, int(m2.group(1)), int(m2.group(2)))
    stxt = text(os.path.join(target, f_slr))
    annual = {}
    for a, b, c, d in re.findall(r"^\s*(\d{4})\s+(\d\.\d\d)(?:\s+(\d{4})\s+(\d\.\d\d))?\s*$", stxt, re.M):
        annual[int(a)] = float(b)
        if c:
            annual[int(c)] = float(d)
    design = float(re.search(r"mean sea level of ([\d.]+) ft MLLW", stxt).group(1))
    btxt = text(os.path.join(target, f_bas))
    sched = [float(x) for x in re.findall(r"\b(1[0-2]\.\d\d)\b", btxt.split("pile schedule:")[1].split("ft MLLW")[0])]
    chk("basis read: nine schedule elevations", len(sched) == 9, str(sched))

    # gauge readings, ft MLLW, UTC minutes
    times, levels = [], []
    with open(os.path.join(target, f_ver), encoding="utf-8") as fh:
        rd = csv.reader(line for line in fh if not line.startswith("#"))
        next(rd)
        for ts, v, q in rd:
            if q != "V" or not v:
                continue
            t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
            x = float(v) - stnd95
            if t_fail <= t < t_reset:
                x += offset_2018
            times.append(t); levels.append(x)
    last_ver = times[-1]
    with open(os.path.join(target, f_tel), encoding="utf-8") as fh:
        rd = csv.reader(fh); next(rd)
        for ts, v, q in rd:
            t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
            if t > last_ver:
                times.append(t); levels.append(float(v) / FT - stnd26)
    chk("gauge series read", len(times) > 1000000, "%d readings" % len(times))

    # high waters from the tables
    hws = []
    wbt = openpyxl.load_workbook(os.path.join(target, f_tab), read_only=True)
    for ws in wbt.worksheets:
        y = int(ws.title)
        rows = list(ws.iter_rows(values_only=True))
        h0 = [i for i, r in enumerate(rows) if r and r[0] == "Date"][0]
        cols = rows[h0]
        for r in rows[h0 + 1:]:
            if not r or r[0] is None:
                continue
            day = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
            if "H/L" in cols:
                if r[4] != "H":
                    continue
                u = dt.datetime(day.year, day.month, day.day, int(r[2][:2]), int(r[2][2:])) + dt.timedelta(hours=5)
                hws.append((u, float(r[3]), utc_to_local(u).date()))
            elif "High/Low" in cols:
                if r[1] != "High":
                    continue
                tm = dt.datetime.strptime(r[2], "%I:%M %p")
                u = to_utc(dt.datetime(day.year, day.month, day.day, tm.hour, tm.minute))
                hws.append((u, float(r[3]), day))
            else:
                if r[4] != "H":
                    continue
                hh, mm = map(int, r[2].split(":"))
                u = to_utc(dt.datetime(day.year, day.month, day.day, hh, mm))
                hws.append((u, float(r[3]), day))
    hws.sort()

    def tmax(u, w=3):
        a = bisect.bisect_left(times, u - dt.timedelta(hours=w)); b = bisect.bisect_right(times, u + dt.timedelta(hours=w))
        return max(levels[a:b]) if b > a else None

    ys = sorted(annual)
    n = len(ys); mx = sum(ys) / n + 0.5; my = sum(annual.values()) / n
    slope = sum((y + 0.5 - mx) * (annual[y] - my) for y in ys) / sum((y + 0.5 - mx) ** 2 for y in ys)
    def ymsl(y):
        return annual[y] if y in annual else my + slope * (y + 0.5 - mx)
    surges, season_hw = [], []
    for u, h, ld in hws:
        if ld.month in (4, 5) and 1995 <= ld.year <= 2026:
            o = tmax(u)
            if o is not None:
                surges.append(o - h - (ymsl(ld.year) - msl_epoch))
                season_hw.append((ld.year, o - ymsl(ld.year) + design))
    fwd = [h for u, h, ld in hws if dt.date(2027, 4, 1) <= ld <= dt.date(2027, 5, 31)]
    chk("forward window high waters", len(fwd) == figs["window_high_waters"], str(len(fwd)))
    surges.sort(); ns = len(surges)
    E = []
    for L in sched:
        tot = 0.0
        for h in fwd:
            need = L - h - (design - msl_epoch)
            tot += (ns - bisect.bisect_left(surges, need)) / ns
        E.append(tot)
    pick = next(L for L, e in zip(sched, E) if e <= 1.0)
    k = sched.index(pick)
    chk("deck elevation", abs(pick - figs["call_deck_ft"]) < 1e-9, "%.2f" % pick)
    chk("expected tides at the deck", "%.1f" % E[k] == "%.1f" % figs["call_expected_at_deck"], "%.3f" % E[k])
    chk("expected tides one elevation down", "%.1f" % E[k - 1] == "%.1f" % figs["call_expected_below"], "%.3f" % E[k - 1])
    years = range(1995, 2027)
    clim = [sum(1 for y, v in season_hw if v >= L) / len(years) for L in sched]
    dpick = next(L for L, e in zip(sched, clim) if e <= 1.0)
    chk("default path's elevation", abs(dpick - figs["default_deck_ft"]) < 1e-9, "%.2f" % dpick)

    # survival tides
    cand = []
    for u, h, ld in hws:
        if dt.date(2016, 11, 1) <= ld <= dt.date(2026, 11, 30):
            o = tmax(u)
            if o is not None:
                cand.append((o, u, ld))
    cand.sort(key=lambda r: -r[0])
    top = []
    for o, u, ld in cand:
        if all(abs((u - x[1]).total_seconds()) > 72 * 3600 for x in top):
            top.append((o, u, ld))
        if len(top) == 5:
            break
    for i, (o, u, ld) in enumerate(top):
        want = figs["ask_a"][i]
        chk("survival tide %d" % (i + 1), want["date"] == ld.isoformat() and "%.2f" % o == "%.2f" % want["level_ft"],
            "%s %.3f" % (ld, o))

    # street closures
    rows = []
    with open(os.path.join(target, f_clo), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if "FRONT ST" not in r["location"].upper() or r["reason"] != "FLOOD":
                continue
            if r["system"] == "WOMS":
                o = dt.datetime.strptime(r["opened"], "%m/%d/%Y %H:%M"); c = dt.datetime.strptime(r["closed"], "%m/%d/%Y %H:%M")
            else:
                o = to_utc(dt.datetime.strptime(r["opened"], "%Y-%m-%d %H:%M"))
                c = to_utc(dt.datetime.strptime(r["closed"], "%Y-%m-%d %H:%M"))
            rows.append((o, c))
    rows.sort()
    clos, end = [], None
    for o, c in rows:
        if clos and o <= end + dt.timedelta(hours=3):
            end = max(end, c); continue
        clos.append(o); end = c
    for y in range(2017, 2023):
        cs = [o for o in clos if utc_to_local(o).year == y]
        hit = sum(1 for o in cs if (tmax(o) or -9) >= 11.80 - 1e-9)
        want = figs["ask_b"][str(y)]
        chk("closures %d" % y, len(cs) == want["closures"] and hit == want["at_street_level"], "%d %d" % (len(cs), hit))
    print("%d failed" % len(BAD))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
