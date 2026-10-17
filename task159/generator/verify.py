"""task159 independent verifier: reads only the shipped bundle (no generator import) and recomputes the call, the
shifts by weekday, the posting schedule, the default path and both asks on its own code path.

    python3 verify.py <target folder>"""
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
FIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
NY = "America/New_York"
WD = ["Mon", "Tue", "Wed", "Thu", "Fri"]
fails = 0


def ok(label, cond, detail=""):
    global fails
    print("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        fails += 1


def days(a, b):
    return [d.date() for d in pd.date_range(a, b)]


# federal holidays in the windows read (the calendar; the service plans name the holiday-timetable days)
FED = set(pd.to_datetime(["2025-05-26", "2025-06-19", "2025-09-01", "2025-10-13", "2025-11-11", "2025-11-27",
                          "2025-11-28", "2026-05-25", "2026-06-19", "2026-10-12", "2026-11-11", "2026-11-26",
                          "2026-11-27"]).date)

# ------------------------------------------------------------------------------------------------ fare mornings
fare = pd.read_parquet(os.path.join(T, "vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet"))
loc = fare.hour_utc.dt.tz_convert(NY)
fare = fare.assign(d=loc.dt.date, h=loc.dt.hour)
mor = fare[fare.h.between(6, 9)].groupby(["complex_id", "d"]).entries.sum()
cx = pd.read_csv(os.path.join(T, "complex_reference.csv"))
cid = dict(zip(cx.complex, cx.complex_id))


def weekdays(a, b):
    return [d for d in days(a, b) if d.weekday() < 5 and d not in FED]


aut = weekdays("2026-09-08", "2026-12-18")
idx = {}
for c in cx.complex_id:
    s = mor.loc[c]
    by = {w: np.mean([s[d] for d in aut if d.weekday() == i and d in s.index]) for i, w in enumerate(WD)}
    mid = np.mean([s[d] for d in aut if d.weekday() in (1, 2, 3) and d in s.index])
    idx[c] = {w: by[w] / mid for w in WD}
    idx[c]["mid"] = mid
net = mor.groupby(level=1).sum()
spring = (np.mean([net[d] for d in weekdays("2026-03-01", "2026-06-25")]) /
          np.mean([net[d] for d in weekdays("2025-09-08", "2025-12-18")]))

# ------------------------------------------------------------------------------------------------ census flows
cen = pd.read_excel(os.path.join(T, "station_census_2026-10.xlsx"), sheet_name="Counts")
cen["d"] = pd.to_datetime(cen["Census date"]).dt.date
cen["norm"] = [idx[c]["mid"] / mor.loc[(c, d)] for c, d in zip(cen["Complex ID"], cen.d)]
cen["q"] = cen["Quarter-hour"].map(lambda x: int(x[:2]) * 60 + int(x[3:]))
DIRS = {"1": "SN", "4": "SN", "5": "WE", "2": "EW", "3": "SN", "6": "EW"}
WORD = {"southbound": "S", "northbound": "N", "eastbound": "E", "westbound": "W"}


def platform(text):
    w = text.split()
    return w[1], (None if w[2] == "island" else WORD[w[2]])


flow = defaultdict(lambda: np.zeros(361))     # (station, line, dir, 'on'|'off') per minute from 05:00
for r in cen.itertuples():
    v = r.People * r.norm / 15.0
    i = r.q - 300
    if r.Direction in ("to platform", "from platform"):
        line, d = platform(r.Location.split(",")[0])
        tag = "on" if r.Direction == "to platform" else "off"
        targets = [(d, 1.0)] if d else [(DIRS[line][0], 0.5), (DIRS[line][1], 0.5)]
        for dd, sh in targets:
            arr = flow[(r.Station, line, dd, tag)]
            arr[i:i + 15] += v * sh
            if r.q == 360:
                arr[30:60] += v * sh * 0.5
                arr[0:30] += v * sh * 0.2
            if r.q == 585:
                arr[300:361] += v * sh
    else:
        body = r.Location[len("Passage, "):]
        trains = None
        if "(" in body:
            body, trains = body[:body.index("(")].strip(), body[body.index("(") + 1:-1].replace(" trains", "")
        a, b = body.split(" to ")
        (la, da), (lb, db) = platform(a), platform(b)
        if trains:
            ta, tb = trains.split(" to ")
            da, db = da or WORD[ta], db or WORD[tb]
        for (ln, dd, tag) in ((la, da, "off"), (lb, db, "on")):
            arr = flow[(r.Station, ln, dd, tag)]
            arr[i:i + 15] += v
            if r.q == 360:
                arr[30:60] += v * 0.5
                arr[0:30] += v * 0.2
            if r.q == 585:
                arr[300:361] += v

# ------------------------------------------------------------------------------------------------ trains
tt = pd.read_csv(os.path.join(T, "weekday_timetables_aut26_spr27.csv"))
tt["m"] = tt.arrive.map(lambda x: int(x[:2]) * 60 + int(x[3:5]) + int(x[6:8]) / 60.0)
fleet = pd.read_csv(os.path.join(T, "fleet_register.csv"))
MAXLOAD = int(fleet.max_load_per_car.iloc[0])


def crowds(plan, wd, mult):
    """{(station, line, dir): [(t, crowd, left)]}"""
    res = {}
    for (line, d), g in tt[tt.plan == plan].groupby(["line", "direction"]):
        line = str(line)
        cap = int(g.cars.iloc[0]) * MAXLOAD
        trips = sorted(g.groupby("trip"), key=lambda kv: kv[1].m.min())
        carry, last = defaultdict(float), {}
        out = defaultdict(list)
        for trip, gg in trips:
            gg = gg.sort_values("m")
            if gg.m.min() > 660 or gg.m.max() < 300:
                continue
            load = 0.0
            for st, t in zip(gg.station, gg.m):
                f = idx[cid[st]][wd] * mult
                t0 = last.get(st, t - 6.0)

                def integ(arr, a, b):
                    c = np.concatenate([[0], np.cumsum(arr)])
                    def at(x):
                        x = min(max(x - 300.0, 0.0), 361.0)
                        k = int(x)
                        return c[-1] if k >= len(c) - 1 else c[k] + (c[k + 1] - c[k]) * (x - k)
                    return max(0.0, at(b) - at(a))
                n = integ(flow[(st, line, d, "on")], t0, t) * f
                x = integ(flow[(st, line, d, "off")], t0, t) * f
                a = min(load, x)
                crowd = carry[st] + n
                b = min(crowd, cap - (load - a))
                carry[st] = crowd - b
                load += b - a
                out[st].append((t, crowd, carry[st]))
                last[st] = t
        for st, ev in out.items():
            res[(st, line, d)] = ev
    return res


cap = pd.read_csv(os.path.join(T, "platform_capacity_register.csv"), dtype=str)
pick = dt.date(2027, 3, 1)


def capacity(code):
    for r in cap[cap.platform_code == code].itertuples():
        a = dt.date.fromisoformat(r.effective_from)
        b = dt.date.fromisoformat(r.effective_to) if isinstance(r.effective_to, str) else dt.date(2100, 1, 1)
        if a <= pick <= b:
            return int(r.rated_capacity)


WATCH = {"GAR-2": ("Garnett Street", "2", None), "GAR-3S": ("Garnett Street", "3", "S"),
         "SAL-1S": ("Sallow Park", "1", "S"), "SAL-1N": ("Sallow Park", "1", "N"), "SAL-4S": ("Sallow Park", "4", "S"),
         "HES-1S": ("Hesper Avenue", "1", "S"), "HES-3": ("Hesper Avenue", "3", None),
         "COR-5W": ("Corran Junction", "5", "W"), "COR-2": ("Corran Junction", "2", None),
         "FER-5W": ("Ferrier Square", "5", "W"), "FER-4S": ("Ferrier Square", "4", "S"),
         "FER-4N": ("Ferrier Square", "4", "N"), "ALB-3S": ("Albrecht Place", "3", "S"),
         "ALB-3N": ("Albrecht Place", "3", "N"), "ALB-6": ("Albrecht Place", "6", None),
         "QUA-1S": ("Quarry Road", "1", "S"), "QUA-6": ("Quarry Road", "6", None)}


def waiting(ev, t):
    prev = [e for e in ev if e[0] <= t]
    nxt = [e for e in ev if e[0] > t]
    if not prev:
        return 0.0
    p = prev[-1]
    if not nxt:
        return p[2]
    n = nxt[0]
    return p[2] + max(0.0, (n[1] - p[2]) * (t - p[0]) / (n[0] - p[0]))


def peak(series):
    best = 0.0
    for q in range(420, 571, 15):
        xs = [c for t, c in series if q <= t < q + 15]
        if xs:
            best = max(best, sum(xs) / len(xs))
    return best


posts = {}
for w in WD:
    cr = crowds("SPR27", w, spring)
    for code, (st, line, d) in WATCH.items():
        if d:
            ser = [(t, c) for t, c, _l in cr[(st, line, d)]]
        else:
            d1, d2 = DIRS[line]
            e1, e2 = cr[(st, line, d1)], cr[(st, line, d2)]
            ser = sorted([(t, c + waiting(e2, t)) for t, c, _l in e1] + [(t, c + waiting(e1, t)) for t, c, _l in e2])
        if peak(ser) > 0.85 * capacity(code):
            posts.setdefault(code, []).append(w)
per = {w: sum(1 for c in posts if w in posts[c]) for w in WD}
total = sum(per.values())
ok("call: shifts a week", total == FIG["shifts_per_week"], "%d" % total)
ok("components: shifts by weekday", all(per[w] == FIG["shifts_%s" % w] for w in WD), str(per))
ok("posting schedule", all(posts.get(c, []) == FIG["posted_%s" % c] for c in WATCH), "")

# ------------------------------------------------------------------------------------------------ default path
xl = pd.ExcelFile(os.path.join(T, "platform_counts_autumn_2026.xlsx"))
r0 = 0
for code, (st, line, d) in WATCH.items():
    sh = xl.parse(st, dtype={"Arrived": str})
    lab = "Line %s island" % line if d is None else "Line %s %s" % (line, {"S": "Southbound", "N": "Northbound",
                                                                         "E": "Eastbound", "W": "Westbound"}[d])
    sh = sh[sh.Platform == lab]
    sh["m"] = sh.Arrived.map(lambda x: int(x[:2]) * 60 + int(x[3:5]))
    pks = []
    for day, g in sh.groupby("Date"):
        if pd.Timestamp(day).weekday() in (1, 2, 3):
            pks.append(peak(list(zip(g.m, g.People))))
    for w in WD:
        r0 += np.mean(pks) * idx[cid[st]][w] * spring > 0.85 * capacity(code)
ok("default path: proportional carry", r0 == FIG["rival_R0"], "%d" % r0)

# ------------------------------------------------------------------------------------------------ ask A
inv = pd.read_csv(os.path.join(T, "station_elements_inventory.csv"))
ast_ = pd.read_csv(os.path.join(T, "escalator_asset_register.csv")).set_index("unit")
log = pd.read_csv(os.path.join(T, "escalator_controller_log_2026-09-01_2026-12-31.csv"))
lt = pd.to_datetime(log.event_utc).dt.tz_localize("UTC").dt.tz_convert(NY)
log = log.assign(d=lt.dt.date, m=lt.dt.hour * 60 + lt.dt.minute + lt.dt.second / 60.0)
autset = set(d for d in days("2026-09-08", "2026-12-18") if d.weekday() < 5 and
             d not in {dt.date(2026, 11, 26), dt.date(2026, 11, 27)})
runs = log[log.event.str.startswith("RUN") & log.d.isin(autset)]
COMPLEXES = ["Garnett Street", "Sallow Park", "Hesper Avenue", "Corran Junction", "Ferrier Square", "Albrecht Place",
             "Quarry Road"]
flowtab = {600: 40, 800: 60, 1000: 80}
esc = inv[(inv.type == "escalator") & inv.complex.isin(COMPLEXES) & inv.to_area.str.contains("platform")]
good = True
for c in COMPLEXES:
    tot = {"down": 0.0, "up": 0.0}
    for r in esc[esc.complex == c].itertuples():
        u = runs[runs.unit == r.unit]
        dirs = set()
        for d, g in u.groupby("d"):
            pre = g[g.m <= 420]
            if len(pre):
                dirs.add(pre.event.iloc[-1][4:].lower())
            dirs.update(e[4:].lower() for e in g[(g.m > 420) & (g.m < 570)].event)
        good &= len(dirs) == 1
        mm = r.width * (25.4 if r.width_unit == "in" else 1)
        stepw = 1000 if mm >= 1000 else (800 if mm >= 800 else 600)
        tot[dirs.pop()] += flowtab[stepw] * ast_.loc[r.unit, "speed_mps"] / 0.5
    good &= round(tot["down"]) == FIG["esc_down_%s" % c] and round(tot["up"]) == FIG["esc_up_%s" % c]
ok("ask A: escalators by direction, 07:00 to 09:30", good)

# ------------------------------------------------------------------------------------------------ ask B
wo = pd.read_csv(os.path.join(T, "elevator_work_orders_2026-09-01_2026-12-31.csv"))
mon = pd.read_csv(os.path.join(T, "elevator_monitoring_2026-09-01_2026-12-31.csv"))
mon["t"] = pd.to_datetime(mon.event_utc).dt.tz_localize("UTC")
wins = [(pd.Timestamp("%s 07:00" % d, tz=NY), pd.Timestamp("%s 09:45" % d, tz=NY)) for d in sorted(autset)]
iv = defaultdict(list)
for u, g in mon.groupby("unit"):
    g = g.sort_values("t").reset_index(drop=True)
    for i in range(len(g)):
        if g["mode"][i] != "NORMAL":
            iv[u].append((g.t[i], g.t[i + 1] if i + 1 < len(g) else pd.Timestamp("2027-01-01", tz="UTC")))
for r in wo[wo.type == "PM"].itertuples():
    iv[r.unit].append((pd.Timestamp(r.out_of_service_at, tz="UTC"), pd.Timestamp(r.in_service_at, tz="UTC")))
unit_cx = dict(zip(wo.unit, wo.complex))
hours = defaultdict(float)
for u, ivs in iv.items():
    ivs.sort()
    merged = []
    for a, b in ivs:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    for a, b in merged:
        for x, y in wins:
            lo, hi = max(a, x), min(b, y)
            if hi > lo:
                hours[unit_cx[u]] += (hi - lo).total_seconds() / 3600
ok("ask B: elevator-hours out of service", all(abs(round(hours[c], 1) - FIG["lift_hours_%s" % c]) < 1e-9
                                              for c in COMPLEXES), str({c: round(hours[c], 1) for c in COMPLEXES}))

print("verify: %d failed" % fails)
sys.exit(1 if fails else 0)
