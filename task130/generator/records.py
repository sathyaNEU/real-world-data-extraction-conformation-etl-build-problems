"""The clean truth: Elkhorn County's establishments, permits, staff calendars and every visit from 2015 to 2026,
the 2027 redraw and schedule, and the truth's expected 2027 count. Nothing here is shipped as is; pack.py writes
the exports from it."""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import world as W

TYPES = [  # type, risk category, weight, seasonal share
    ("Full-service restaurant", 3, 0.24, 0.02),
    ("Quick-service restaurant", 2, 0.16, 0.00),
    ("Tavern or bar with food", 2, 0.07, 0.00),
    ("Bakery or coffee shop", 2, 0.09, 0.01),
    ("Grocery with deli", 3, 0.05, 0.00),
    ("Market or grocery, packaged food", 1, 0.10, 0.00),
    ("Convenience store", 1, 0.11, 0.00),
    ("School kitchen", 2, 0.06, 0.00),
    ("Care facility kitchen", 3, 0.04, 0.00),
    ("Caterer or commissary", 3, 0.03, 0.00),
    ("Espresso stand", 1, 0.03, 0.10),
    ("Resort or camp kitchen", 2, 0.02, 0.85),
]
FREQ = {1: 1, 2: 2, 3: 3}
N_NEW = 760                  # permits opened 2015 to 2026
COVER_POSTPONE = 0.65        # a leave day's routine visit waits for the district inspector this often

STREETS = ["Main St", "Front St", "Harbor Ave", "Cedar St", "Pine St", "Alder Way", "Commercial Ave", "Lake Rd",
           "Mill St", "Railroad Ave", "Kessing Hwy", "Valley View Rd", "1st St", "2nd St", "3rd St", "4th Ave",
           "5th Ave", "Ocean Beach Hwy", "Marine Dr", "Fir St", "Maple Ave", "Birch Ln", "Bridge St", "Market St",
           "Sunset Blvd", "Highland Dr", "Orchard Ave", "Depot St", "College Way", "Fairgrounds Rd", "Ardell Rd",
           "Wexby Loop", "Torvik Pass Rd", "Elsby Grade", "Callan Creek Rd", "Norrow Ferry Rd", "Baker Ave",
           "Division St", "Grant St", "Lincoln Ave", "Washington St", "Chestnut St", "Hemlock St", "Spruce St"]
PREFIX = ["Golden", "Blue Heron", "Red Barn", "Summit", "Harbor", "Cedar", "Evergreen", "Lucky", "Twin Rivers",
          "Old Mill", "Riverside", "Lakeside", "Northwind", "Copper", "Iron Horse", "Silver", "Jade", "Pacific",
          "Mountain View", "Sunrise", "Little", "Big Sky", "Wild Rose", "Stone", "Kettle", "Grey Gull", "Bluebird",
          "Timberline", "Juniper", "Salt", "Driftwood", "Crow's Nest", "Brick", "Morning", "Union", "Garden"]
CUISINE = ["Grill", "Bistro", "Diner", "Cafe", "Kitchen", "Taqueria", "Pho", "Pizza", "Sushi", "Thai Kitchen",
           "Burger Bar", "Brewing Co.", "Smokehouse", "Teriyaki", "Noodle House", "Bakery", "Deli", "Tavern",
           "Pub", "Cantina", "Wok", "Steakhouse", "Fish House", "Creamery", "Bagels", "Espresso"]
CHAINS = [("Sound Sub Co. #", 2), ("Kettle Burger #", 2), ("Tidewater Coffee #", 2), ("Cascadia Fresh Market #", 3),
          ("Ridgeline Mart #", 1), ("Pennock's Market #", 3), ("Glacier Cone #", 2), ("Casa Verde Taco #", 2),
          ("Northline Food Mart #", 1), ("Summit Fuel Mart #", 1), ("Papa Ferrante's #", 2), ("Hearthstone Pizza #", 2),
          ("Bayside Drug #", 1)]
SURNAMES = ["Nguyen", "Garcia", "Johnson", "Kim", "Patel", "Olsen", "Martinez", "Larsen", "Chen", "Hernandez",
            "Sorensen", "Lopez", "Tran", "Park", "Silva", "Andersen", "Reyes", "Novak", "Haugen", "Ortiz"]


def _name(r, typ, risk):
    u = r.random()
    if typ in ("School kitchen",):
        return "%s %s" % (r.choice(["Lincoln", "Hillcrest", "Ridgeview", "Cedar Park", "Harbor", "Valley",
                                     "Pine Grove", "Westside", "Eastview", "Lakewood", "Fairview", "Northshore"]),
                          r.choice(["Elementary School", "Middle School", "High School", "Elementary"]))
    if typ == "Care facility kitchen":
        return "%s %s" % (r.choice(["Evergreen", "Harbor View", "Cedar Court", "Willow Creek", "Marlow", "Sound"]),
                          r.choice(["Assisted Living", "Care Center", "Senior Living", "Health & Rehab"]))
    if typ == "Resort or camp kitchen":
        return "%s %s" % (r.choice(["Lake Elkhorn", "Torvik Pass", "Callan Creek", "Pine Point", "Kettle Lake"]),
                          r.choice(["Lodge", "Resort", "Camp", "Bible Camp", "RV Park Store"]))
    if u < 0.16:
        base, rk = CHAINS[r.integers(len(CHAINS))]
        return base + str(int(r.integers(1000, 39999)))
    if u < 0.30:
        return "%s's %s" % (r.choice(SURNAMES), r.choice(CUISINE))
    if typ in ("Market or grocery, packaged food", "Grocery with deli"):
        return "%s %s" % (r.choice(PREFIX), r.choice(["Market", "Grocery", "Foods", "Mercado", "Asian Market",
                                                      "Food Center", "Natural Foods"]))
    if typ == "Convenience store":
        return "%s %s" % (r.choice(PREFIX), r.choice(["Mini Mart", "Food Mart", "Quick Stop", "Gas & Grocery"]))
    if typ == "Espresso stand":
        return "%s %s" % (r.choice(PREFIX), r.choice(["Espresso", "Coffee", "Java Hut", "Drive-Thru Espresso"]))
    return "%s %s" % (r.choice(PREFIX), r.choice(CUISINE))


def _leave(r, years):
    """Each staff member's leave days: two blocks of annual leave a year and a few single days."""
    out = set()
    days = [W.START + dt.timedelta(days=i) for i in range((W.END - W.START).days + 1)]
    work = [d for d in days if W.working(d)]
    by_year = defaultdict(list)
    for d in work:
        by_year[d.year].append(d)
    for y in years:
        wd = by_year.get(y, [])
        if not wd:
            continue
        for _ in range(2):
            n = int(r.integers(5, 11))
            i = int(r.integers(0, max(1, len(wd) - n)))
            out.update(wd[i:i + n])
        for _ in range(int(r.integers(3, 9))):
            out.add(wd[int(r.integers(0, len(wd)))])
    return out


def build():
    r = W.rng("establishments")
    # ------------------------------------------------------------ premises and permits
    premises = []
    n0 = 2760
    n_new = N_NEW
    types, risks, weights, seasonal = zip(*[(t[0], t[1], t[2], t[3]) for t in TYPES])
    weights = np.array(weights) / sum(weights)
    town_w = np.array([t[3] for t in W.TOWNS])
    town_w = town_w / town_w.sum()
    used_addr = set()
    for i in range(n0 + n_new):
        k = int(r.choice(len(TYPES), p=weights))
        typ, risk, seas = types[k], risks[k], seasonal[k]
        ti = int(r.choice(len(W.TOWNS), p=town_w))
        tname, tx, ty, _, spread = W.TOWNS[ti]
        x = float(np.clip(tx + r.normal(0, spread), 0.5, 59.5))
        y = float(np.clip(ty + r.normal(0, spread), 0.5, 44.5))
        while True:
            addr = "%d %s" % (int(r.integers(100, 9900)), r.choice(STREETS))
            if addr not in used_addr:
                used_addr.add(addr)
                break
        city = tname if tname else ("Marlow" if r.random() < 0.5 else W.TOWNS[int(r.integers(1, 8))][0])
        zipc = r.choice(W.ZIP[tname])
        if i < n0:
            opened = W.START - dt.timedelta(days=int(r.integers(30, 9000)))
        else:
            opened = W.START + dt.timedelta(days=int(r.integers(30, (W.END - W.START).days - 20)))
        closed = None
        if r.random() < 0.30:
            c = opened + dt.timedelta(days=int(r.integers(200, 6000)))
            if W.START < c <= W.END:
                closed = c
            elif c <= W.START:
                continue
        is_seasonal = r.random() < seas
        premises.append(dict(pid=len(premises), type=typ, risk=risk, x=x, y=y, addr=addr, city=city, zip=zipc,
                             opened=opened, closed=closed, seasonal=is_seasonal,
                             d26=W.nearest(W.SEEDS_2026, x, y), d27=W.nearest(W.SEEDS_2027, x, y),
                             name=_name(r, typ, risk)))
    # permits: an ownership change issues a new permit with a new operator
    permits = []
    rp = W.rng("permits")
    for p in premises:
        start = max(p["opened"], dt.date(2008, 1, 1))
        end = p["closed"]
        cur = start
        names = [p["name"]]
        while True:
            hold = int(rp.integers(700, 9000))
            nxt = cur + dt.timedelta(days=hold)
            if (end is not None and nxt >= end) or nxt > W.END or rp.random() > 0.55:
                permits.append(dict(prem=p["pid"], start=cur, end=end, name=names[-1]))
                break
            if nxt > W.START:
                permits.append(dict(prem=p["pid"], start=cur, end=nxt - dt.timedelta(days=1), name=names[-1]))
                cur = nxt
                if rp.random() < 0.6:
                    names.append(_name(rp, p["type"], p["risk"]))
            else:
                cur = nxt
    rt = W.rng("theta")
    for j, pm in enumerate(permits):
        pm["id"] = j
        pm["theta"] = float(rt.normal(0, W.THETA_SD))
    # identifiers: legacy permit numbers for permits held before the cutover, new numbers for every permit
    # active at or after it (the migration renumbered the live ones)
    ri = W.rng("ids")
    legacy_pool = ri.permutation(np.arange(100000, 189999))
    new_pool = ri.permutation(np.arange(10000, 69999))
    li = ni = 0
    for pm in permits:
        pm["legacy"] = pm["new"] = None
        if pm["start"] < W.CUTOVER + dt.timedelta(days=25) and (pm["end"] is None or pm["end"] >= W.RECORD):
            pm["legacy"] = "FP-%06d" % legacy_pool[li]
            li += 1
        if pm["end"] is None or pm["end"] >= W.RECORD:      # the new system kept every permit's number
            if pm["legacy"]:
                pm["new"] = pm["legacy"]
            else:
                pm["new"] = "EH%02d-%05d" % (pm["start"].year % 100, new_pool[ni])
                ni += 1
    # ------------------------------------------------------------ staff
    rg = W.rng("gamma")
    gamma = {s[3]: float(rg.normal(0, W.GAMMA_SD)) for s in W.STAFF}
    rl = W.rng("leave")
    leave = {s[3]: _leave(rl, range(2015, 2027)) for s in W.STAFF}
    return dict(premises=premises, permits=permits, gamma=gamma, leave=leave)


def assign_2027(premises):
    """Each 2027 district goes to the remaining inspector whose 2026 district shares most of its establishments
    (the plan's Appendix A), taken greedily from the largest overlap down."""
    active = [p for p in premises if p["closed"] is None]
    staying = {d: W.district_holder(d, W.END) for d in W.SEEDS_2026 if d not in W.RETIRING_2026}
    overlap = defaultdict(int)
    for p in active:
        if p["d26"] in staying:
            overlap[(p["d27"], p["d26"])] += 1
    pairs = sorted(overlap.items(), key=lambda kv: -kv[1])
    out, used_d, used_i = {}, set(), set()
    for (d27, d26), n in pairs:
        if d27 in out or d26 in used_i:
            continue
        out[d27] = staying[d26]
        used_i.add(d26)
    rest_d = [d for d in W.SEEDS_2027 if d not in out]
    rest_i = [staying[d] for d in staying if d not in used_i]
    for d, e in zip(sorted(rest_d), sorted(rest_i)):
        out[d] = e
    return out


def holder_on(d26, day):
    return W.district_holder(d26, day)


def simulate(R):
    """Every visit from 2015 to 2026, in date order, with its performer, the performer's earlier inspected visits
    to the permit, and its outcome."""
    premises, permits, gamma, leave = R["premises"], R["permits"], R["gamma"], R["leave"]
    prem = {p["pid"]: p for p in premises}
    rv = W.rng("visits")
    plan = defaultdict(list)          # day -> list of (kind, permit id, extra)
    # routine visits, planned per permit-year
    for pm in permits:
        p = prem[pm["prem"]]
        n = 1 if p["seasonal"] else FREQ[p["risk"]]
        anchor = float(rv.random())
        for y in range(W.START.year, W.END.year + 1):
            a = max(pm["start"], dt.date(y, 1, 1))
            b = min(pm["end"] or W.END, dt.date(y, 12, 31))
            if a > b:
                continue
            for j in range(n):
                if p["seasonal"]:
                    day = dt.date(y, 5, 15) + dt.timedelta(days=int(rv.integers(0, 110)))
                else:
                    frac = (anchor + j / n + rv.normal(0, 0.035)) % 1.0
                    day = dt.date(y, 1, 1) + dt.timedelta(days=int(frac * 364))
                if not (a <= day <= b):
                    continue
                if W.COVID_STOP[0] <= day <= W.COVID_STOP[1]:
                    continue
                while not W.working(day):
                    day += dt.timedelta(days=1)
                if day <= (pm["end"] or W.END) and day <= W.END:
                    plan[day].append(("routine", pm["id"], None))
    # complaint incidents
    rc = W.rng("complaints")
    incidents = []
    last_start = {}
    for pm in permits:
        lam = 0.085 * math.exp(1.1 * pm["theta"])
        a, b = max(pm["start"], W.START), min(pm["end"] or W.END, W.END)
        span = (b - a).days
        if span <= 0:
            continue
        k = int(rc.poisson(lam * span / 365.0))
        starts = sorted(dt.datetime.combine(a + dt.timedelta(days=int(rc.integers(0, span))), dt.time(0)) +
                        dt.timedelta(minutes=int(rc.integers(6 * 60, 23 * 60))) for _ in range(k))
        for t0 in starts:
            cat = rc.choice(["Illness", "Pests", "Sanitation", "Temperature", "Other"], p=[0.22, 0.2, 0.33, 0.1, 0.15])
            pri = 1 if cat == "Illness" else (2 if cat in ("Pests", "Temperature") else 3)
            m = int(rc.choice([1, 2, 3, 4], p=[0.38, 0.32, 0.20, 0.10]))
            times = sorted([t0 + dt.timedelta(seconds=int(rc.integers(0, 60)))] + [t0 + dt.timedelta(seconds=int(rc.integers(20 * 60, 56 * 3600))) for _ in range(m - 1)])
            delay_h = {1: rc.uniform(3, 26), 2: rc.uniform(16, 70), 3: rc.uniform(40, 200)}[pri]
            start = times[0] + dt.timedelta(hours=float(delay_h))
            # the inspector arrives during working hours on a working day
            s = start
            if s.hour < 8:
                s = dt.datetime.combine(s.date(), dt.time(8, int(rc.integers(0, 50))))
            elif s.hour >= 16:
                s = dt.datetime.combine(s.date() + dt.timedelta(days=1), dt.time(8, int(rc.integers(0, 50))))
            while not W.working(s.date()):
                s = dt.datetime.combine(s.date() + dt.timedelta(days=1), dt.time(8, int(rc.integers(0, 50))))
            s = s.replace(microsecond=0)
            times = [t for t in times if t < s - dt.timedelta(minutes=30)] or [times[0]]
            if s.date() > W.END:
                continue
            if last_start.get(pm["id"]) and times[0] <= last_start[pm["id"]] + dt.timedelta(days=1):
                continue
            last_start[pm["id"]] = s
            inc = dict(permit=pm["id"], times=times, cat=str(cat), pri=pri, start=s, channel=[
                str(rc.choice(["Phone", "Online", "Email"], p=[0.45, 0.45, 0.10])) for _ in times])
            incidents.append(inc)
            plan[s.date()].append(("complaint", pm["id"], len(incidents) - 1))
    # pre-opening inspections by the plan reviewer
    for pm in permits:
        if pm["start"] > W.START:
            d = pm["start"] - dt.timedelta(days=int(rv.integers(4, 21)))
            while not W.working(d):
                d -= dt.timedelta(days=1)
            if d >= W.START:
                plan[d].append(("preopen", pm["id"], None))

    # ------------------------------------------------------------ process day by day
    pair = defaultdict(int)          # (performer, permit) -> earlier inspected visits
    visits = []
    ro = W.rng("outcomes")
    rr = W.rng("returns")
    open_seq = {}                    # permit -> a return sequence is still open (no routine visit until it closes)
    day = W.START
    while day <= W.END:
        todays = plan.pop(day, [])
        for kind, pid, extra in todays:
            pm = permits[pid]
            p = prem[pm["prem"]]
            if kind in ("return", "complaint") and pm["end"] is not None and day > pm["end"]:
                continue
            if kind == "preopen":
                who = W.PLAN_REVIEWER
                visits.append(dict(day=day, kind="preopen", permit=pid, who=who, k=pair[(who, pid)], result="Approved",
                                   unsat=False, red=0, blue=int(ro.integers(0, 4)), seq=None, incident=None,
                                   time=dt.time(int(ro.integers(8, 15)), int(ro.integers(0, 60)))))
                pair[(who, pid)] += 1
                continue
            if kind == "return":
                who = extra["who"]
                seq = extra
            else:
                holder = holder_on(p["d26"], day)
                who = holder
                if day in leave[holder]:
                    order = W.covering_order(p["d26"])
                    pick = list(ro.choice(len(order), size=len(order), replace=False, p=W.COVER_WEIGHTS))
                    covers = [holder_on(order[i], day) for i in pick]
                    covers = [c for c in covers if day not in leave[c]]
                    if kind == "routine" and (not covers or ro.random() < COVER_POSTPONE):
                        nd = W.add_working(day, 1)
                        while nd in leave[holder]:
                            nd = W.add_working(nd, 1)
                        if nd <= W.END:
                            plan[nd].append((kind, pid, extra))
                        continue
                    if covers:
                        who = covers[0]
                seq = None
            if kind == "routine" and open_seq.get(pid):
                nd = W.add_working(day, 10)
                if nd <= W.END:
                    plan[nd].append((kind, pid, extra))
                continue
            k = pair[(who, pid)]
            t = dt.time(int(ro.integers(8, 16)), int(ro.integers(0, 60)), int(ro.integers(0, 60)))
            if kind == "routine":
                if ro.random() < 0.015:
                    visits.append(dict(day=day, kind="routine", permit=pid, who=who, k=k, result="No access",
                                       unsat=False, red=None, blue=None, seq=None, incident=None, time=t))
                    nd = W.add_working(day, int(ro.integers(1, 6)))
                    if nd <= W.END:
                        plan[nd].append(("routine", pid, None))
                    continue
                f = W.F0 if k == 0 else (W.F1 if k == 1 else 0.0)
                reopen = W.REOPEN_2021 if (day.year == 2021 and day.month <= 6) else 0.0
                pr = W.expit(W.lg(W.BASE[p["risk"]]) + pm["theta"] + gamma[who] + f + reopen)
                unsat = bool(ro.random() < pr)
                red = _red(ro, unsat)
                ihh = unsat and ro.random() < 0.01
                visits.append(dict(day=day, kind="routine", permit=pid, who=who, k=k, p=pr, unsat=unsat,
                                   result=("IHH" if ihh else ("Unsatisfactory" if unsat else "Satisfactory")),
                                   red=red, blue=int(ro.integers(0, 13)), seq=None, incident=None, time=t))
                pair[(who, pid)] += 1
                if unsat:
                    open_seq[pid] = True
                    _schedule_return(plan, rr, day, pid, p, len(visits) - 1, 1)
            elif kind == "complaint":
                inc = incidents[extra]
                t = inc["start"].time()
                unsat = bool(ro.random() < 0.18)
                visits.append(dict(day=day, kind="complaint", permit=pid, who=who, k=k, unsat=unsat,
                                   result="Unsatisfactory" if unsat else "Satisfactory", red=_red(ro, unsat),
                                   blue=int(ro.integers(0, 10)), seq=None, incident=extra, time=t))
                pair[(who, pid)] += 1
            elif kind == "return":
                if rr.random() < 0.17:
                    visits.append(dict(day=day, kind="return", permit=pid, who=who, k=k, result="No access",
                                       unsat=False, red=None, blue=None, seq=seq, incident=None, time=t))
                    if seq["n"] < 5:
                        _schedule_return(plan, rr, day, pid, p, seq["routine"], seq["n"] + 1, gap=(2, 7))
                    else:
                        open_seq[pid] = False
                    continue
                unsat = bool(rr.random() < 0.16)
                visits.append(dict(day=day, kind="return", permit=pid, who=who, k=k, unsat=unsat,
                                   result="Unsatisfactory" if unsat else "Satisfactory", red=_red(rr, unsat),
                                   blue=int(rr.integers(0, 9)), seq=seq, incident=None, time=t))
                if who not in W.RETURN_OFFICER.values():
                    pair[(who, pid)] += 1
                if unsat and seq["n"] < 5:
                    _schedule_return(plan, rr, day, pid, p, seq["routine"], seq["n"] + 1, gap=(5, 13))
                else:
                    open_seq[pid] = False
        day += dt.timedelta(days=1)
    R["visits"] = visits
    R["incidents"] = incidents
    R["pair_end"] = dict(pair)
    return R


def _red(r, unsat):
    if unsat:
        return 25 + int(r.choice([0, 5, 10, 15, 20, 25, 35], p=[0.24, 0.22, 0.18, 0.14, 0.1, 0.07, 0.05]))
    if r.random() < 0.42:
        return 0
    return int(r.choice([5, 10, 15, 20], p=[0.36, 0.32, 0.2, 0.12]))


def _schedule_return(plan, r, day, pid, p, routine_ix, n, gap=(3, 15)):
    d = W.add_working(day, int(r.integers(gap[0], gap[1])))
    if d > W.END:
        return
    if d >= W.RETURN_TEAM:
        who = W.RETURN_OFFICER["north" if p["d26"] in W.NORTH else "south"]
    else:
        who = W.district_holder(p["d26"], d)
    plan[d].append(("return", pid, dict(who=who, routine=routine_ix, n=n)))


def schedule_2027(R):
    """The plan's 2027 schedule: every permit active on 31 December 2026, its 2027 district and inspector and its
    required routine inspections; and the truth's expected unsatisfactory count over it."""
    prem = {p["pid"]: p for p in R["premises"]}
    insp = assign_2027(R["premises"])
    rows = []
    truth = 0.0
    pair = R["pair_end"]
    for pm in R["permits"]:
        if pm["end"] is not None:
            continue
        p = prem[pm["prem"]]
        n = 1 if p["seasonal"] else FREQ[p["risk"]]
        who = insp[p["d27"]]
        k0 = pair.get((who, pm["id"]), 0)
        for j in range(n):
            k = k0 + j
            f = W.F0 if k == 0 else (W.F1 if k == 1 else 0.0)
            truth += W.expit(W.lg(W.BASE[p["risk"]]) + pm["theta"] + R["gamma"][who] + f)
        rows.append(dict(permit=pm["id"], d27=p["d27"], who=who, n=n, k0=k0))
    R["schedule"] = rows
    R["insp27"] = insp
    R["truth27"] = truth
    return R
