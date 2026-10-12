"""Engineer-day simulation: planned schedule, actual timeline, at most one large delay event per day."""
import datetime as dt
from collections import defaultdict

import numpy as np

from world import (ADJ, CHECKLIST_FROM, DISTRICTS_OLD, MOVES, PATCHES, REBALANCE, ROUTING_GO_LIVE,
                   VANSTOCK_FROM, adjacent, patch_of)

WINDOWS = [(480, 600), (600, 720), (720, 840), (840, 960), (960, 1080)]
JOBS = [("Repair", 60, 0.55), ("Annual service", 45, 0.33), ("Follow-on repair", 75, 0.12)]

EV_P = {"late": 0.025, "travel_pre": 0.050, "travel_post": 0.058, "overrun": 0.032, "parts_pre": 0.017,
        "parts_post": 0.072, "access": 0.028, "other": 0.006}


def districts_on(patch, d):
    out = [x for x in DISTRICTS_OLD[patch] if not (x in MOVES and d >= REBALANCE)]
    if d >= REBALANCE:
        out += [x for x, (a, b) in MOVES.items() if b == patch]
    return out


def window_for(arr_plan):
    """The window the customer was offered: the grid window holding the planned arrival, or the next one
    when the plan would sit in the last quarter-hour of it."""
    for i, w in enumerate(WINDOWS):
        if w[0] <= arr_plan < w[1]:
            if w[1] - arr_plan >= 15:
                return w
            return WINDOWS[i + 1] if i + 1 < len(WINDOWS) else None
    return None


def leg_km(rng, a_d, b_d, a_p, b_p):
    if a_d == b_d:
        return float(rng.uniform(1.5, 5.0))
    if a_p == b_p:
        return float(rng.uniform(5.0, 15.0))
    return float(rng.uniform(17.0, 33.0))


def plan_day(rng, W, e, d, prefs):
    """The scheduler's plan of record for engineer e on day d."""
    hp = e["home_patch"]
    own = districts_on(hp, d)
    nbr = [p for p in PATCHES if adjacent(p, hp)]
    njobs = 7 if rng.random() < 0.55 else 6
    jobs = []
    prev_d, prev_p = e["home_district"], hp
    for k in range(njobs):
        if rng.random() < 0.20:
            p = nbr[int(rng.integers(len(nbr)))]
            pool = districts_on(p, d)
        else:
            p = hp
            pool = own
        dist = pool[int(rng.integers(len(pool)))]
        jt = JOBS[int(rng.choice(3, p=[j[2] for j in JOBS]))]
        km = leg_km(rng, prev_d, dist, prev_p, patch_of(dist, d))
        jobs.append({"district": dist, "job_type": jt[0], "booked": jt[1], "km": km})
        prev_d, prev_p = dist, patch_of(dist, d)
    t = 480 + 4
    for k, j in enumerate(jobs):
        old = int(round(4 + 1.7 * j["km"]))
        j["ptravel_old"] = old
        long_leg = j["km"] > 16.5
        j["long"] = long_leg
        j["ptravel"] = int(round(old * 0.85)) if (long_leg and d >= ROUTING_GO_LIVE) else old
        j["en_route_plan"] = t
        j["arr_plan"] = t + j["ptravel"]
        j["start_plan"] = j["arr_plan"] + 3
        j["dep_plan"] = j["start_plan"] + j["booked"]
        buf = int(rng.integers(5, 12)) + (20 if k == 2 else 0)
        t = j["dep_plan"] + buf
    keep = []
    for j in jobs:
        w = window_for(j["arr_plan"])
        if w is None:
            break
        j["window"] = w
        keep.append(j)
    return keep


def run_day(rng, jobs, d, logon, event, after_checklist):
    """Actual timeline. event = None or (kind, index, size). Returns per-job actual dicts."""
    out = []
    en_route = logon + jobs[0]["lag0"]
    for k, j in enumerate(jobs):
        if k > 0:
            en_route = max(out[-1]["dep"] + j["paperwork"], j["en_route_plan"] - 5)
        trav = j["ptravel_old"] + j["tnoise"]
        ttype = "Direct"
        if event and event[1] == k and event[0] == "travel":
            trav += event[2]
        if event and event[1] == k and event[0] == "parts":
            trav += event[2]
            ttype = "Via merchant"
        if event and event[1] == k and event[0] == "other":
            trav += event[2]
            ttype = "Vehicle recovery"
        arr = en_route + trav
        st = arr + j["startlag"]
        if event and event[1] == k and event[0] == "access":
            st += event[2]
        dur = j["booked"] + j["dnoise"]
        if j["job_type"] == "Annual service" and after_checklist:
            dur += j["chk"]
        if event and event[1] == k and event[0] == "overrun":
            dur += event[2]
        if j.get("no_access"):
            st = None
            dep = arr + int(j["na_wait"])
        else:
            dep = st + dur
        out.append({"en_route": en_route, "arr": arr, "start": st, "dep": dep, "travel_type": ttype,
                    "travel": trav})
    return out


def misses(jobs, acts):
    return [k for k, (j, a) in enumerate(zip(jobs, acts)) if a["arr"] > j["window"][1]]


def margins_ok(jobs, acts):
    for j, a in zip(jobs, acts):
        late = a["arr"] - j["window"][1]
        if late > 0 and late < 15:
            return False
        if -3 < late <= 0:
            return False
    return True


def draw_noise(rng, jobs, d):
    post_go = d >= ROUTING_GO_LIVE
    for j in jobs:
        j["tnoise"] = int(rng.integers(-3, 4))
        if j["long"] and post_go:
            # the plan of record was cut 15 per cent on long legs; the road did not change
            pass
        j["startlag"] = int(rng.integers(2, 6))
        j["dnoise"] = int(rng.integers(-4, 5))
        j["chk"] = int(rng.integers(6, 11))
        j["paperwork"] = int(rng.integers(6, 13))
    jobs[0]["lag0"] = int(rng.integers(2, 7))


def choose_event(rng, jobs, d, P):
    ev = dict(EV_P)
    ev.update(P.get("ev", {}))
    post_go = d >= ROUTING_GO_LIVE
    longs = [k for k, j in enumerate(jobs) if j["long"]]
    probs = [("late", ev["late"]),
             ("travel", (ev["travel_post"] if post_go else ev["travel_pre"]) if longs else 0.0),
             ("overrun", ev["overrun"]),
             ("parts", ev["parts_post"] if d >= VANSTOCK_FROM else ev["parts_pre"]),
             ("access", ev["access"]), ("other", ev["other"])]
    u = rng.random()
    acc = 0.0
    for kind, p in probs:
        acc += p
        if u < acc:
            if kind == "late":
                if rng.random() < 0.22:
                    return (kind, 0, int(rng.integers(95, 211)))
                return (kind, 0, int(rng.integers(30, 96)))
            if kind == "travel":
                return (kind, longs[int(rng.integers(len(longs)))], int(rng.integers(35, 76)))
            if kind == "overrun":
                ks = [k for k, j in enumerate(jobs[:-1]) if j["job_type"] != "Annual service"]
                if not ks:
                    return None
                return (kind, ks[int(rng.integers(len(ks)))], int(rng.integers(40, 111)))
            if kind == "parts":
                if len(jobs) < 2:
                    return None
                return (kind, int(rng.integers(1, len(jobs))), int(rng.integers(45, 91)))
            if kind == "access":
                return (kind, int(rng.integers(0, len(jobs))), int(rng.integers(25, 51)))
            if kind == "other":
                return (kind, int(rng.integers(0, len(jobs))), int(rng.integers(60, 151)))
    return None


def simulate_days(W, rng, P):
    P = P or {}
    W.day_records = []          # one per engineer-day worked
    rest_log = {}
    for (eid, n), rec in W.callouts_by_eng_night.items():
        clr = rec["cleared_m"]
        nxt = n + dt.timedelta(days=1)
        if clr > 21 * 60 + 10 and nxt in W.dayset and W.roster[eid].get(nxt) == "D":
            rest_log[(eid, nxt)] = clr - 1440            # minutes after midnight on the working day (may be <0)
    W.rest_days = rest_log
    seed = P.get("seed", 111)
    for d in W.days:
        after_chk = d >= dt.date(2026, 4, 6)
        for e in W.engineers:
            eid = e["engineer_id"]
            if W.roster[eid][d] != "D":
                continue
            rng = np.random.default_rng([seed, 2, int(eid[1:]), d.toordinal()])
            jobs = plan_day(rng, W, e, d, None)
            # statuses decided before the day: none of these remove a routed job
            for j in jobs:
                j["no_access"] = rng.random() < 0.02
                j["na_wait"] = int(rng.integers(8, 14))
            forced = (eid, d) in rest_log
            if forced:
                logon_forced = rest_log[(eid, d)] + 660
            for attempt in range(400):
                if attempt and attempt % 25 == 0:
                    jobs = plan_day(rng, W, e, d, None)
                    for j in jobs:
                        j["no_access"] = rng.random() < 0.02
                        j["na_wait"] = int(rng.integers(8, 14))
                draw_noise(rng, jobs, d)
                l0 = 480 + int(rng.integers(0, 4))
                base = run_day(rng, jobs, d, l0, None, after_chk)
                if misses(jobs, base) or not margins_ok(jobs, base):
                    continue
                if forced:
                    logon = logon_forced + int(rng.integers(0, 5))
                    event = ("rest", 0, logon - 480)
                    acts = run_day(rng, jobs, d, logon, None, after_chk)
                else:
                    event = choose_event(rng, jobs, d, P) if attempt < 300 else None
                    logon = l0 + (event[2] if event and event[0] == "late" else 0)
                    acts = run_day(rng, jobs, d, logon, event if (event and event[0] != "late") else None,
                                   after_chk)
                if not margins_ok(jobs, acts):
                    continue
                break
            else:
                raise RuntimeError("could not place day %s %s" % (eid, d))
            W.day_records.append({"engineer_id": eid, "date": d, "jobs": jobs, "acts": acts, "logon": logon,
                                  "event": event, "missed": misses(jobs, acts)})
    return W.day_records


def tally(W, d0, d1):
    fam = defaultdict(int)
    tot = 0
    attended = 0
    for r in W.day_records:
        if not (d0 <= r["date"] <= d1):
            continue
        attended += len(r["jobs"])
        if not r["missed"]:
            continue
        kind = r["event"][0] if r["event"] else "NONE"
        fam[kind] += len(r["missed"])
        tot += len(r["missed"])
    return tot, attended, dict(fam)
