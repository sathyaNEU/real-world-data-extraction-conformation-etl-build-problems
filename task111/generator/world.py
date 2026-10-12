"""World simulation for task111: the Scotland field region of a home heating repair and cover company.

Everything shipped in target/ is written from the structures this module returns. Nothing here is read by the
independent verifier; the golden figures are recomputed from the shipped files in golden.py.
"""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

D = dt.date
T = dt.datetime

START = D(2025, 7, 1)
END = D(2026, 9, 30)
EXTRACT = D(2026, 10, 5)
ROUTING_GO_LIVE = D(2026, 7, 1)
CHECKLIST_FROM = D(2026, 4, 6)
VANSTOCK_FROM = D(2026, 7, 1)
OOH_END = D(2026, 10, 4)          # out-of-hours export runs to the night before the pull
REBALANCE = D(2026, 8, 1)
MERGE_DAY = D(2026, 8, 18)

# Scottish bank holidays (gov.uk) inside the window
BANK_HOLIDAYS = {
    D(2025, 8, 4), D(2025, 12, 1), D(2025, 12, 25), D(2025, 12, 26),
    D(2026, 1, 1), D(2026, 1, 2), D(2026, 4, 3), D(2026, 5, 4), D(2026, 5, 25), D(2026, 8, 3),
}

PATCHES = ["GNW", "GSE", "LAN", "ARF", "EDL", "FFV"]
PATCH_NAME = {
    "GNW": "Glasgow North & West", "GSE": "Glasgow South & East", "LAN": "Lanarkshire",
    "ARF": "Ayrshire & Renfrewshire", "EDL": "Edinburgh & Lothians", "FFV": "Fife & Forth Valley",
}
DISTRICTS_OLD = {
    "GNW": ["G11", "G12", "G13", "G14", "G15", "G20", "G21", "G22", "G23", "G61", "G62", "G81", "G82"],
    "GSE": ["G31", "G32", "G33", "G34", "G40", "G41", "G42", "G43", "G44", "G45", "G46", "G51", "G52",
            "G53", "G72", "G73", "G74"],
    "LAN": ["ML1", "ML2", "ML3", "ML4", "ML5", "ML6", "ML7", "ML8", "ML9", "G71", "G75"],
    "ARF": ["PA1", "PA2", "PA3", "PA4", "PA5", "PA6", "PA14", "PA15", "PA16", "KA1", "KA3", "KA7", "KA8",
            "KA11", "KA12", "KA13"],
    "EDL": ["EH3", "EH4", "EH5", "EH6", "EH7", "EH8", "EH9", "EH10", "EH11", "EH12", "EH13", "EH14", "EH15",
            "EH16", "EH17", "EH21", "EH22", "EH26", "EH30", "EH47", "EH48", "EH52", "EH53", "EH54", "EH55"],
    "FFV": ["KY1", "KY2", "KY3", "KY5", "KY6", "KY7", "KY8", "KY11", "KY12", "KY16", "FK1", "FK2", "FK3",
            "FK5", "FK7", "FK8", "FK9", "G66"],
}
MOVES = {"G72": ("GSE", "LAN"), "G73": ("GSE", "LAN"), "G74": ("GSE", "LAN"), "G71": ("LAN", "GSE"),
         "ML7": ("LAN", "EDL"), "ML5": ("LAN", "GSE"), "EH30": ("EDL", "FFV"), "EH52": ("EDL", "LAN"),
         "EH54": ("EDL", "LAN"), "G66": ("FFV", "GNW"), "FK1": ("FFV", "EDL"), "PA4": ("ARF", "GNW"),
         "PA3": ("ARF", "GNW"), "G82": ("GNW", "ARF")}
ADJ = {("GNW", "GSE"), ("GNW", "ARF"), ("GNW", "FFV"), ("GSE", "LAN"), ("GSE", "ARF"), ("LAN", "EDL"),
       ("LAN", "FFV"), ("EDL", "FFV")}


def adjacent(a, b):
    return (a, b) in ADJ or (b, a) in ADJ


def patch_of(district, on):
    """Reporting patch of a postcode district on a date (structure in force that day)."""
    for p, ds in DISTRICTS_OLD.items():
        if district in ds:
            old = p
            break
    if district in MOVES and on >= REBALANCE:
        return MOVES[district][1]
    return old


def working_days():
    d, out = START, []
    while d <= END:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def mins(t):
    return t.hour * 60 + t.minute


def at(d, m):
    """datetime on day d at minute m after midnight (m may exceed 1440)."""
    return T(d.year, d.month, d.day) + dt.timedelta(minutes=int(m))


class World:
    pass


P_ON = 3


def build_world(seed=111, P=None):
    P = P or {}
    rng = np.random.default_rng(seed)
    W = World()
    W.P = P
    W.days = working_days()
    W.dayset = set(W.days)

    # ---------------------------------------------------------------- geography
    W.district_patch_old = {d: p for p, ds in DISTRICTS_OLD.items() for d in ds}
    W.districts = list(W.district_patch_old)
    W.dweight = {d: float(rng.uniform(0.55, 1.45)) for d in W.districts}

    # ---------------------------------------------------------------- workforce
    day_ids = sorted(set(int(x) for x in rng.choice(np.arange(4100, 4999), 160, replace=False)))[:84]
    rng.shuffle(day_ids)
    W.engineers = []
    k = 0
    for p in PATCHES:
        own = [d for d in DISTRICTS_OLD[p] if d not in MOVES]
        for i in range(14):
            eid = "E%d" % day_ids[k]
            k += 1
            W.engineers.append({
                "engineer_id": eid, "role": "Field engineer", "home_patch": p,
                "home_district": own[int(rng.integers(len(own)))],
                "callout_list": i < 6, "start_date": D(int(rng.integers(2012, 2024)), int(rng.integers(1, 13)), 1),
            })
    W.eng = {e["engineer_id"]: e for e in W.engineers}
    sb_ids = sorted(int(x) for x in rng.choice(np.arange(5100, 5899), 17, replace=False))
    W.standby = []
    leavers = {0: D(2025, 11, 28), 3: D(2026, 2, 27), 5: D(2026, 4, 24), 7: D(2026, 6, 12), 8: D(2026, 6, 26),
               9: D(2026, 7, 6), 11: D(2026, 7, 6), 12: D(2026, 7, 20), 13: D(2026, 8, 17), 15: D(2026, 9, 4),
               16: D(2026, 8, 28)}
    for i, s in enumerate(sb_ids):
        W.standby.append({"engineer_id": "E%d" % s, "role": "Standby engineer", "home_patch": PATCHES[i % 6],
                          "end_date": leavers.get(i)})
    pays = rng.choice(np.arange(2041000, 2199999), 101, replace=False)
    for e, pn in zip(W.engineers + W.standby, pays):
        e["payroll_no"] = "%07d" % int(pn)
    W.payroll_to_eid = {e["payroll_no"]: e["engineer_id"] for e in W.engineers + W.standby}

    # ---------------------------------------------------------------- day-engineer roster (D / AL / TR / SK)
    W.roster = {}
    for e in W.engineers:
        status = {d: "D" for d in W.days}
        # annual leave blocks
        nblocks = int(rng.integers(5, 8))
        for _ in range(nblocks):
            i0 = int(rng.integers(0, len(W.days) - 6))
            for j in range(int(rng.integers(3, 6))):
                status[W.days[i0 + j]] = "AL"
        for _ in range(int(rng.integers(3, 8))):
            status[W.days[int(rng.integers(len(W.days)))]] = "TR"
        for _ in range(int(rng.integers(2, 7))):
            status[W.days[int(rng.integers(len(W.days)))]] = "SK"
        W.roster[e["engineer_id"]] = status

    # ---------------------------------------------------------------- standby rota (nights)
    W.nights = []
    d = START - dt.timedelta(days=1)
    while d <= OOH_END:
        W.nights.append(d)
        d += dt.timedelta(days=1)
    W.standby_on = defaultdict(list)       # night date -> [engineer ids on duty]
    for i, s in enumerate(W.standby):
        offset = i % 7
        for n in W.nights:
            if s["end_date"] and n >= s["end_date"]:
                continue
            # each standby engineer works a 7-day cycle of 4 nights on, 3 off, staggered
            if (n.toordinal() + offset) % 7 < P_ON:
                if rng.random() < 0.93:       # leave and sickness
                    W.standby_on[n].append(s["engineer_id"])
    return W, rng


# ------------------------------------------------------------------------------------------------ OOH desk
LAMBDA = {7: 16.5, 8: 17.0, 9: 18.5, 10: 18.0, 11: 22.0, 12: 26.0, 1: 27.0, 2: 24.0, 3: 18.5, 4: 13.5, 5: 10.5,
          6: 10.0}
CATS = [("No heating", 0.34), ("No hot water", 0.22), ("Leak", 0.22), ("Boiler lockout", 0.14), ("Other", 0.08)]


def winter_cover(n):
    return n.month >= 10 or n.month <= 5


def simulate_ooh(W, rng, P):
    rng = np.random.default_rng([P.get("seed", 111), 1])
    lam = dict(LAMBDA)
    lam.update(P.get("lambda", {}))
    resp_wait = P.get("resp_wait", 60)
    calls = []
    last_used = defaultdict(lambda: D(2000, 1, 1))
    W.callouts_by_eng_night = {}
    for n in W.nights:
        weekend_period = n.weekday() >= 5          # Sat/Sun evenings
        base = lam[n.month] * (1.15 if weekend_period else 1.0)
        nc = int(rng.poisson(base))
        times = []
        for _ in range(nc):
            u = rng.random()
            if u < 0.62:
                m = 17 * 60 + int(rng.integers(0, 300))          # 17:00-22:00
            elif u < 0.86:
                m = 22 * 60 + int(rng.integers(0, 180))          # 22:00-01:00
            else:
                m = 25 * 60 + int(rng.integers(0, 390))          # 01:00-07:30
            times.append(m)
        times.sort()
        free_at = {s: 17 * 60 for s in W.standby_on.get(n, [])}
        used_tonight = set()
        for m in times:
            cat = CATS[int(rng.choice(len(CATS), p=[c[1] for c in CATS]))][0]
            dist = W.districts[int(rng.choice(len(W.districts), p=np.array([W.dweight[x] for x in W.districts]) /
                                              sum(W.dweight.values())))]
            cpatch = patch_of(dist, n)
            travel = int(rng.integers(20, 46))
            onsite = int(rng.integers(50, 121))
            rec = {"night": n, "received_m": m, "category": cat, "district": dist, "patch": cpatch}
            # standby first
            best, best_start = None, None
            for s, f in free_at.items():
                st = max(m + 5, f)
                if best is None or st < best_start:
                    best, best_start = s, st
            if best is not None and best_start - m <= resp_wait:
                arr = best_start + travel
                clr = arr + onsite
                free_at[best] = clr + 10
                rec.update(cover="Standby rota", engineer=best, arrived_m=arr, cleared_m=clr)
                calls.append(rec)
                continue
            # overflow
            if winter_cover(n) and m >= 18 * 60:
                arr = m + int(rng.integers(55, 140))
                rec.update(cover="Contractor panel", engineer=None, arrived_m=arr, cleared_m=arr + onsite)
                calls.append(rec)
                continue
            if m > 22 * 60:
                # standby queue, attended when the first standby engineer frees up
                if best is not None:
                    arr = best_start + travel
                    clr = arr + onsite
                    free_at[best] = clr + 10
                    rec.update(cover="Standby rota", engineer=best, arrived_m=arr, cleared_m=clr)
                else:
                    arr = m + int(rng.integers(80, 160))
                    rec.update(cover="Contractor panel", engineer=None, arrived_m=arr, cleared_m=arr + onsite)
                calls.append(rec)
                continue
            # call-out list: day engineers who worked that day, on the list, not used tonight
            worked_today = n in W.dayset
            cands = []
            for e in W.engineers:
                if not e["callout_list"]:
                    continue
                eid = e["engineer_id"]
                if eid in used_tonight:
                    continue
                if worked_today and W.roster[eid].get(n) != "D":
                    continue
                if not worked_today and n.weekday() < 5:
                    continue
                if e["home_patch"] == cpatch:
                    pri = 0
                elif adjacent(e["home_patch"], cpatch):
                    pri = 1
                else:
                    continue
                cands.append((pri, last_used[eid], e.get("pref", 0.0), eid))
            if not cands:
                arr = m + int(rng.integers(80, 160))
                rec.update(cover="Contractor panel", engineer=None, arrived_m=arr, cleared_m=arr + onsite)
                calls.append(rec)
                continue
            cands.sort()
            eid = cands[0][3]
            used_tonight.add(eid)
            last_used[eid] = n
            arr = m + int(rng.integers(22, 40))
            clr = arr + onsite
            # in winter the list only sees calls received before 18:00, so it clears by 20:38 at the latest
            # construction gap: no day-engineer clear between 20:41 and 21:10
            if 20 * 60 + 40 < clr <= 21 * 60 + 10:
                if clr - (20 * 60 + 40) <= 15:
                    onsite -= clr - (20 * 60 + 40)
                else:
                    onsite += 21 * 60 + 11 - clr
                clr = arr + onsite
            rec.update(cover="Call-out list", engineer=eid, arrived_m=arr, cleared_m=clr)
            calls.append(rec)
            W.callouts_by_eng_night[(eid, n)] = rec
    W.calls = calls
    return calls
