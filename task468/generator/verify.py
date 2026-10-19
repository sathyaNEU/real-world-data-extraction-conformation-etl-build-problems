"""An independent verifier for task468: reads only the shipped bundle (target/) and the goldens, with its own readers and
arithmetic (no generator module), and recomputes the call, the verdicts, the call at the stop-hour grain and every
shelter count.

    python3 task468/generator/verify.py
"""
import csv
import datetime as dt
import io
import os
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CT = ZoneInfo("America/Chicago")
NAMES = {"q1": "avl_stop_events_2026q1_arbor.csv", "q2": "avl_stop_events_2026q2_quinnell.csv",
         "review": "trip_matching_review_2026h1.csv", "fleet": "fleet_roster_2026.csv",
         "jan": "larkhaven_gtfs_20260101.zip", "apr": "larkhaven_gtfs_20260405.zip",
         "ride": "ridership_by_route_2026h1.xlsx", "guide": "dot_ftc_program_guidance_fy2027.pdf",
         "cand": "ftc_candidate_routes_fy2027.csv", "amen": "facilities_bus_stop_amenities_20260710.csv",
         "wo": "capital_projects_shelter_work_orders.xlsx"}
GOLD = {"wb": "larkhaven_frequent_corridor_nominations_fy2027.xlsx"}


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def feed(path, name):
    with zipfile.ZipFile(path) as z:
        return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))


def mins(s):
    h, m, x = (int(v) for v in s.split(":"))
    return h * 60 + m + x / 60.0


def main(target, golden):
    p = lambda k: os.path.join(target, NAMES[k])
    guide = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-raw", p("guide"), "-"], capture_output=True, text=True,
                                               check=True).stdout)
    hol = [dt.date(2026, {"January": 1, "February": 2, "May": 5}[m], int(d)) for m, d in
           re.findall(r"\((January|February|May) (\d+)\)", guide)]
    assert len(hol) == 4, hol
    days, d = [], dt.date(2026, 1, 1)
    while d <= dt.date(2026, 6, 30):
        if d.weekday() < 5 and d not in hol:
            days.append(d)
        d += dt.timedelta(days=1)
    dayset = set(days)
    n_days = len(days)
    # stops, buses and the five designated stops' routes
    code = {}
    for k in ("jan", "apr"):
        for s in feed(p(k), "stops.txt"):
            code[s["stop_id"]] = s["stop_code"]
    tag = {r["asset_tag"]: r["fleet_no"] for r in rows(p("fleet"))}
    # conform: (source, id, bus, code, departure local, service day, trip, route, scheduled minutes)
    ev = []
    for r in rows(p("q1")):
        dep = dt.datetime.strptime(r["dep_time"], "%Y-%m-%d %H:%M:%S")
        ev.append(("A", r["event_id"], r["veh_no"], code[r["stop_id"]], dep, dt.date.fromisoformat(r["svc_date"]),
                   r["trip_id"], r["route"], mins(r["sched_dep"]) if r["sched_dep"] else None, None))
    seen, q = set(), []
    for r in rows(p("q2")):
        u = dt.datetime.strptime(r["ActualDepartureUTC"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        dep = u.astimezone(CT).replace(tzinfo=None)
        key = (r["VehicleID"], r["StopCode"], r["ActualDepartureUTC"])
        if key in seen:
            continue
        seen.add(key)
        sch = mins(r["ScheduledDeparture"]) if r["ScheduledDeparture"] else None
        if sch is not None:
            base = dep - dt.timedelta(minutes=sch)
            sday = (base + dt.timedelta(hours=12)).date()
        else:
            sday = dep.date() - dt.timedelta(days=1 if dep.hour < 3 else 0)
        q.append(("Q", r["EventID"], tag[r["VehicleID"]], r["StopCode"], dep, sday, r["TripID"], r["Route"], sch,
                  r["DeviationSec"]))
    ev += [e for e in q if e[5] >= dt.date(2026, 4, 1)]
    # the candidates and their designated stops, from Planning's list
    clist = rows(p("cand"))
    cand = [r["route"] for r in clist]
    stop_of = {r["route"]: r["designated_stop_code"] for r in clist}
    # the review's weights
    unm = defaultdict(int)
    for e in ev:
        if not e[6]:
            unm[(e[2], e[5])] += 1
    listed = defaultdict(int)
    for (b, sd) in unm:
        listed[sd.month] += 1
    rv = rows(os.path.join(target, NAMES["review"]))
    drawn = defaultdict(int)
    for r in rv:
        drawn[int(r["service_date"][5:7])] += 1
    mix = defaultdict(lambda: defaultdict(float))
    rawmix = defaultdict(lambda: defaultdict(float))
    mixh = defaultdict(lambda: defaultdict(float))
    for r in rv:
        sd = dt.date.fromisoformat(r["service_date"])
        u = unm[(r["bus"], sd)]
        assert u >= 1
        w = u * listed[sd.month] / drawn[sd.month]
        lab = "NIS" if r["route_operated"] == "Not in service" else r["route_operated"]
        mix[r["stop_code"]][lab] += w
        rawmix[r["stop_code"]][lab] += 1
        mixh[(r["stop_code"], int(r["event_time"][:2]))][lab] += w
    for m in (mix, rawmix, mixh):
        for s in m:
            tot = sum(m[s].values())
            for k in m[s]:
                m[s][k] /= tot
    # the counting hours: attributed by route and hour, unattributed by stop and hour
    att, una = defaultdict(int), defaultdict(int)
    for e in ev:
        if e[5] in dayset and 6 <= e[4].hour <= 18 and e[4].date() == e[5]:
            if e[6]:
                att[(e[7], e[4].hour)] += 1
            else:
                una[(e[3], e[4].hour)] += 1

    def estimate(sh, by_hour=False):
        est = defaultdict(float)
        for k, v in att.items():
            est[k] += v
        for (s, h), n in una.items():
            for r, w in sh[(s, h) if by_hour else s].items():
                if r != "NIS":
                    est[(r, h)] += n * w
        return {k: v / n_days for k, v in est.items()}

    est = estimate(mix)
    lowest = {r: min(est.get((r, h), 0.0) for h in range(6, 19)) for r in cand}
    from openpyxl import load_workbook
    ws = load_workbook(p("ride"), data_only=True)["Weekday average"]
    ride = {str(r[0]): r[-1] for r in ws.iter_rows(values_only=True) if r and isinstance(r[0], int)}
    qual = sorted([r for r in cand if lowest[r] >= 4.0], key=lambda r: -ride[r])
    five, below = qual[:5], qual[5] if len(qual) > 5 else None
    raw = estimate(rawmix)
    raw_low = {r: min(raw.get((r, h), 0.0) for h in range(6, 19)) for r in cand}
    raw_five = sorted([r for r in cand if raw_low[r] >= 4.0], key=lambda r: -ride[r])[:5]
    est_h = estimate(mixh, by_hour=True)
    low_h = {r: min(est_h.get((r, h), 0.0) for h in range(6, 19)) for r in cand}
    five_h = sorted([r for r in cand if low_h[r] >= 4.0], key=lambda r: -ride[r])[:5]
    # the shelters: each candidate's outbound stops in the spring feed, Facilities' inventory, Capital Projects' orders
    def m_between(a, b):
        import math
        return math.hypot((a[0] - b[0]) * 111320.0, (a[1] - b[1]) * 111320.0 * math.cos(math.radians(a[0])))

    st_apr = feed(p("apr"), "stops.txt")
    code_apr = {x["stop_id"]: x["stop_code"] for x in st_apr}
    pos_apr = {x["stop_code"]: (float(x["stop_lat"]), float(x["stop_lon"])) for x in st_apr}
    dir0 = {x["trip_id"]: x["route_id"] for x in feed(p("apr"), "trips.txt") if x["direction_id"] == "0"}
    served = defaultdict(set)
    for x in feed(p("apr"), "stop_times.txt"):
        if x["trip_id"] in dir0:
            served[dir0[x["trip_id"]]].add(code_apr[x["stop_id"]])
    inv = {r["stop_code"]: r for r in rows(p("amen"))}
    wsw = load_workbook(p("wo"), data_only=True)["Work orders"]
    orders = []
    for r in wsw.iter_rows(min_row=5, values_only=True):
        if r and r[0] and r[4] == "Completed" and r[3] in ("Install shelter", "Remove shelter", "Relocate shelter"):
            orders.append(("%04d" % int(r[1]), r[3], r[6].date() if hasattr(r[6], "date") else r[6]))
    cut, spring = dt.date(2026, 6, 30), dt.date(2026, 4, 5)
    shelter = {}
    for code, r in inv.items():
        if code not in pos_apr:
            continue
        here = m_between((float(r["latitude"]), float(r["longitude"])), pos_apr[code]) > 30.0
        insp = dt.date.fromisoformat(r["last_inspected"])
        on = r["shelter"] == "Y"
        mine = sorted((d_, w_) for c_, w_, d_ in orders if c_ == code)
        if here:
            on = False
            for d_, w_ in mine:
                if spring <= d_ <= cut:
                    on = w_ != "Remove shelter"
        else:
            for d_, w_ in mine:
                if insp < d_ <= cut:
                    on = w_ != "Remove shelter"
                elif cut < d_ <= insp:
                    on = w_ == "Remove shelter"
        shelter[code] = on
    bare = {r: sum(1 for c_ in served[r] if not shelter[c_]) for r in cand}
    # against the goldens
    wb = load_workbook(os.path.join(golden, GOLD["wb"]), data_only=True)
    nom = {str(r[0]): r for r in wb["Nominations"].iter_rows(min_row=6, values_only=True) if isinstance(r[0], int)}
    shw = {str(r[0]): r for r in wb["Shelters"].iter_rows(min_row=5, values_only=True) if isinstance(r[0], int)}
    r1 = lambda v: int(v * 10 + 0.5) / 10.0
    checks = {
        "the five": [r for r in nom if str(nom[r][7] or "").startswith("Nominated")] == sorted(five, key=lambda r: -ride[r])
        and five == ["2", "4", "6", "17", "22"],
        "the first left out": below == "11" and "First qualifying" in str(nom[below][7]),
        "the verdicts": all((nom[r][5] == "Yes") == (lowest[r] >= 4.0) and nom[r][3] == r1(lowest[r]) for r in cand),
        "the raw mix's five": raw_five == ["2", "4", "6", "22", "11"],
        "the stop-hour grain's five": five_h == five,
        "the shelters": all(shw[r][3] == bare[r] for r in cand) and sorted(cand) == sorted(
            ["2", "4", "6", "9", "11", "14", "17", "22", "31", "40", "51"]),
    }
    for k, v in checks.items():
        print("%s  verify: %s" % ("PASS" if v else "FAIL", k))
    print("verify: %d counting days, %d qualifying (%s), five %s, first left out %s; no shelter %s" % (
        n_days, len(qual), ", ".join(qual), ", ".join(five), below, bare))
    if not all(checks.values()):
        raise SystemExit("verify failed")


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
