"""The independent verifier: every graded figure recomputed from target/ with the standard library only (no pandas,
no numpy, none of figs.py), event by event, and compared with figures.json.

    python3 task122/generator/verify.py
"""
import bisect
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
NZ = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
START = dt.datetime(2026, 4, 1, tzinfo=NZ).astimezone(UTC)
END = dt.datetime(2026, 10, 1, tzinfo=NZ).astimezone(UTC)
SECTORS = ["KPA", "HKI", "WKO", "TKI", "TPO", "KPT"]


def u(s):
    return int((dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC) - START).total_seconds())


def loc(s):
    t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=NZ)
    return int((t.astimezone(UTC) - START).total_seconds())


def rows(name):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    minutes = int((END - START).total_seconds() // 60)
    # flown crossings: each flight's highest plan revision
    cr = rows("fdps_sector_crossings_2026-04_2026-09.csv")
    top = {}
    for r in cr:
        top[r["ifps_id"]] = max(top.get(r["ifps_id"], 0), int(r["plan_revision"]))
    flown = [r for r in cr if int(r["plan_revision"]) == top[r["ifps_id"]]]
    # occupancy by events: a crossing is in a minute when the minute's midpoint is inside it
    ev = {s: defaultdict(int) for s in SECTORS}
    evt = {s: defaultdict(int) for s in SECTORS}
    where = defaultdict(list)
    for r in flown:
        a, b = u(r["entry_utc"]), u(r["exit_utc"])
        lo, hi = -(-(a - 30) // 60), -(-(b - 30) // 60)
        ev[r["sector"]][lo] += 1
        ev[r["sector"]][hi] -= 1
        if r["entry_fl"] != r["exit_fl"]:
            evt[r["sector"]][lo] += 1
            evt[r["sector"]][hi] -= 1
        where[r["callsign"]].append((a, b, r["sector"]))

    def walk(d):
        out = [0] * minutes
        run = 0
        for m in range(minutes):
            run += d.get(m, 0)
            out[m] = run
        return out
    n = {s: walk(ev[s]) for s in SECTORS}
    T = {s: walk(evt[s]) for s in SECTORS}
    # probe minutes
    pe = {s: defaultdict(int) for s in SECTORS}
    for r in rows("probe_m_planner_workstation_log_2026-04_2026-09.csv"):
        a, b = loc(r["display_on"]), loc(r["display_off"])
        lo, hi = -(-(a - 30) // 60), -(-(b - 30) // 60)
        for s in r["sector"].split("/"):
            pe[s][lo] += 1
            pe[s][hi] -= 1
    on = {s: [x > 0 for x in walk(pe[s])] for s in SECTORS}
    # activations, counted once per event where they began
    st = [r for r in rows("stca_activations_2026-04_2026-09.csv") if r["status"] == "LIVE"]
    st.sort(key=lambda r: (u(r["start_utc"]), r["alert_id"]))
    last = {}
    counted = []
    for r in st:
        pair = tuple(sorted((r["callsign_1"], r["callsign_2"])))
        a, b = u(r["start_utc"]), u(r["end_utc"])
        p = last.get(pair)
        last[pair] = (b, r["sector"])
        if p and p[1] != r["sector"] and 0 <= a - p[0] <= 3:
            continue
        sec = r["sector"]
        if "/" in sec:
            hit = [x[2] for x in where[r["callsign_1"]] if x[0] <= a < x[1] and x[2] in sec.split("/")]
            if not hit:
                continue
            sec = hit[0]
        counted.append((sec, a))
    al = {s: defaultdict(int) for s in SECTORS}
    for s, a in counted:
        al[s][a // 60] += 1
    # the share prevented at like sector, count and climbing count
    cell = defaultdict(lambda: [0, 0, 0, 0])
    for s in SECTORS:
        for m in range(minutes):
            k = (s, n[s][m], T[s][m])
            x = cell[k]
            if on[s][m]:
                x[0] += 1
                x[1] += al[s].get(m, 0)
            else:
                x[2] += 1
                x[3] += al[s].get(m, 0)
    O = sum(x[1] for x in cell.values() if x[0] and x[2])
    E = sum(x[0] * x[3] / x[2] for x in cell.values() if x[0] and x[2])
    share = 1 - O / E
    ok = True

    def eq(name, a, b, tol=0.0):
        nonlocal ok
        good = abs(a - b) <= tol
        ok &= good
        print("%-4s %-46s %s against %s" % ("PASS" if good else "FAIL", name, a, b))
    eq("activations counted", len(counted), fig["activations_counted"])
    eq("raised in the probe's running time", sum(x[1] for x in cell.values()), fig["observed_all"])
    eq("of them in matched minutes", O, fig["observed"])
    eq("the probe's minutes without a match", sum(x[0] for x in cell.values() if not x[2]), fig["unmatched_minutes"])
    eq("expected without the probe", round(E, 1), fig["expected"], 0.05)
    eq("share prevented, nearest five per cent", int(5 * round(100 * share / 5)), fig["share_prevented_pct_nearest5"])
    # the asks
    edges = [int((dt.datetime(2026, mo, 1, tzinfo=NZ).astimezone(UTC) - START).total_seconds()) for mo in range(4, 11)]
    bad = 0
    for s in SECTORS:
        for k in range(6):
            lo, hi = edges[k], edges[k + 1]
            secs = sum(max(0, min(u(r["exit_utc"]), hi) - max(u(r["entry_utc"]), lo)) for r in flown if r["sector"] == s)
            hrs = secs / 3600.0
            cnt = sum(1 for x, a in counted if x == s and lo <= a < hi)
            bad += round(hrs) != fig["flight_hours"][s][k]
            bad += round(1000.0 * cnt / hrs, 1) != fig["stca_rate"][s][k]
        bad += len({r["ifps_id"] for r in flown if r["sector"] == s}) != fig["flights_handled"][s]
    eq("ask figures that differ (of 78)", bad, 0)
    print("verify: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
