"""The operator's records, cut from the world: the station register, the trip exports (the old trip system to 30 June,
the new platform from 1 July), riders and their accounts, the dispatch log, the 03:00 audit, the charging points'
sessions and the workshop's jobs. Each function returns rows and, where a figure is owed, its truth."""
import datetime as dt
import heapq
import itertools

import numpy as np

import params as P

MIGRATION = dt.datetime(P.YEAR, 7, 1, tzinfo=P.TZ)
SIZES = [15, 19, 23, 27, 31, 35, 39, 43, 47, 55, 63, 71, 79]


def loc(t):
    return dt.datetime.fromtimestamp(int(t), P.TZ)


def utc(t):
    return dt.datetime.fromtimestamp(int(t), dt.timezone.utc)


# ---------------------------------------------------------------------------------------------------- stations
STREETS = {
    "CEN": ["Main St", "Court St", "Wabash Ave", "2nd St", "3rd St", "4th St", "5th St", "State St", "Mercer Ave",
            "Bridge St", "Canal St", "Fulton Ave", "Grand Ave", "Monroe St", "Union Sq"],
    "RIV": ["River Rd", "Willow Ln", "Mill Race Trl", "Oxbow Dr", "Ferry Rd", "Elm Bend", "Boathouse Rd",
            "Sycamore Ave", "Levee St", "Heron Way", "Fisher Park", "Locust St", "Weir St"],
    "OLD": ["Market Sq", "Chapel St", "Tanner St", "Cobble Ln", "Founders Pl", "Ash St", "Brewery Ln", "Gable St",
            "Linden Ave", "Pump House Sq"],
    "HIL": ["Summit Ave", "Crest Rd", "Ridge Dr", "Vista Ln", "Overlook Pl", "Hollow Rd", "Quarry St", "Terrace Ave",
            "Bluff Rd", "Lookout Ct"],
    "HBR": ["Quay St", "Pier 1", "Pier 2", "Pier 3", "Ferry Terminal", "Marina Dr", "Wharf Rd", "Lighthouse Ln",
            "Anchor St", "Dock St", "Harbor Walk", "Customs House", "Tug Basin", "Net Loft Ln", "Breakwater Rd"]}
UNI_NAMES = {"dorm": ["Lakeside Residence Halls", "North Residence Halls"],
             "class": ["Science Quad", "Library Mall", "Student Union Plaza"]}
CENTRE = {"CEN": (43.052, -88.911), "UNI": (43.071, -88.935), "RIV": (43.038, -88.884), "OLD": (43.061, -88.893),
          "HIL": (43.024, -88.928), "HBR": (43.047, -88.866)}


def stations(W):
    rs = np.random.default_rng([P.SEED_DOCS, 1])
    rows = []
    ids = rs.permutation(np.arange(1001, 1001 + W.ND + 40))[: W.ND]
    used = set()
    seq = {a: itertools.count(1) for a in P.NETWORKS}
    uni = {"dorm": iter(UNI_NAMES["dorm"]), "class": iter(UNI_NAMES["class"])}
    for k in range(W.ND):
        a, r = W.docks[k]
        code = "%s-%02d" % (a, next(seq[a]))
        if a == "UNI":
            name = next(uni[r])
        else:
            place = ("Sq", "Pl", "Terminal", "House", "Park", "Walk", "Basin", "Pier 1", "Pier 2", "Pier 3")
            streets = [s for s in STREETS[a] if not s.endswith(place)]
            while True:
                s1 = str(rs.choice(STREETS[a]))
                name = s1 if s1.endswith(place) else "%s & %s" % (s1, rs.choice([s for s in streets if s != s1]))
                if name not in used:
                    break
        used.add(name)
        lat0, lon0 = CENTRE[a]
        peak = int(W.maxstock[k]) + 2
        cap = next(s for s in SIZES if s >= peak)
        pts = P.POINTS if W.pilot[k] else 0
        rows.append({"k": k, "station_id": str(int(ids[k])), "code": code, "name": name, "network": a,
                     "lat": round(lat0 + rs.normal(0, 0.006), 6), "lon": round(lon0 + rs.normal(0, 0.008), 6),
                     "capacity": cap, "charging_points": pts,
                     "programme": "e-bike pilot" if W.pilot[k] else ("pilot comparison" if W.matched[k] else "")})
    return rows


# ---------------------------------------------------------------------------------------------------- riders
HOME = {"CEN": {"CEN": .55, "OLD": .12, "RIV": .10, "HIL": .07, "UNI": .03, "HBR": .05, "OUT": .08},
        "UNI": {"UNI": .80, "CEN": .07, "OLD": .03, "RIV": .02, "HIL": .01, "HBR": .01, "OUT": .06},
        "RIV": {"RIV": .50, "CEN": .10, "OLD": .08, "HIL": .04, "UNI": .03, "HBR": .05, "OUT": .20},
        "OLD": {"OLD": .62, "CEN": .10, "RIV": .06, "HIL": .04, "UNI": .02, "HBR": .04, "OUT": .12},
        "HIL": {"HIL": .74, "CEN": .08, "OLD": .04, "RIV": .03, "UNI": .02, "HBR": .02, "OUT": .07},
        "HBR": {"HBR": .50, "CEN": .14, "RIV": .06, "OLD": .05, "HIL": .03, "UNI": .02, "OUT": .20}}
ANNUAL = {"CEN": .40, "UNI": .65, "RIV": .20, "OLD": .35, "HIL": .45, "HBR": .25}


def people(W, rides):
    """riders and the accounts they ride on: the realised rides of each network are dealt to the riders active that
    day who are not already out on a bike. A few riders re-register mid-year (same card, a new account, the old one
    left open); a few households pay for two riders' accounts with one card."""
    rs = np.random.default_rng([P.SEED_PEOPLE, 1])
    y0 = dt.date(P.YEAR, 1, 1)
    persons = []
    by_net = {}
    for a in P.NETWORKS:
        idx = [j for j, r in enumerate(rides) if W.area[r[2]] == a]
        by_net[a] = idx
        n_r = len(idx)
        mean = ANNUAL[a] * 55 + (1 - ANNUAL[a]) * 4.0
        N = int(n_r / mean * 1.05)
        for _ in range(N):
            ann = rs.random() < ANNUAL[a]
            if ann:
                rate = rs.lognormal(np.log(50), 0.7) / 365.0
                if rs.random() < 0.7:
                    s, e = 0, 364
                else:
                    s = int(rs.integers(0, 300)); e = int(min(364, s + rs.integers(60, 365)))
                    if rs.random() < 0.5:
                        s, e = 0, int(rs.integers(60, 364))
            else:
                rate = rs.lognormal(np.log(4), 0.8) / 30.0
                L = int(rs.integers(1, 90)); s = int(rs.integers(0, 365 - min(L, 364))); e = min(364, s + L)
            home = rs.choice(list(HOME[a]), p=np.array(list(HOME[a].values())) / sum(HOME[a].values()))
            persons.append({"net": a, "annual": bool(ann), "rate": rate, "s": s, "e": e, "home": str(home), "rides": []})
    # deal the rides
    for a in P.NETWORKS:
        pids = [i for i, p in enumerate(persons) if p["net"] == a]
        busy = {i: -1 for i in pids}
        idx = sorted(by_net[a], key=lambda j: rides[j][0])
        days = {}
        for j in idx:
            days.setdefault((loc(rides[j][0]).date() - y0).days, []).append(j)
        for d, js in sorted(days.items()):
            act = [i for i in pids if persons[i]["s"] <= d <= persons[i]["e"]]
            w = np.array([persons[i]["rate"] for i in act])
            draw = list(rs.choice(len(act), size=len(js) * 4 + 20, p=w / w.sum()))
            for j in js:
                t0, t1 = rides[j][0], rides[j][1]
                while True:
                    if not draw:
                        draw = list(rs.choice(len(act), size=50, p=w / w.sum()))
                    i = act[draw.pop()]
                    if busy[i] < t0:
                        break
                busy[i] = t1 + 60
                persons[i]["rides"].append(j)
    persons = [p for p in persons if p["rides"]]
    # accounts: one per rider, created before the first ride; re-registrations and shared cards on top
    accounts = []
    cards = itertools.count(1)
    for pi, p in enumerate(persons):
        first = min(rides[j][0] for j in p["rides"])
        if p["s"] == 0 and p["annual"]:
            created = dt.datetime(int(rs.integers(2019, 2025)), int(rs.integers(1, 13)), int(rs.integers(1, 28)),
                                  int(rs.integers(7, 23)), int(rs.integers(0, 60)), tzinfo=P.TZ)
        elif rs.random() < 0.35:
            created = dt.datetime(int(rs.integers(2021, 2025)), int(rs.integers(1, 13)), int(rs.integers(1, 28)),
                                  int(rs.integers(7, 23)), int(rs.integers(0, 60)), tzinfo=P.TZ)
        else:
            created = loc(first - int(rs.integers(120, 86400 * int(rs.integers(1, 20)))))
        p["card"] = "fp_%012x" % int(rs.integers(16 ** 11, 16 ** 12))
        accounts.append({"pid": pi, "created": created, "rides": sorted(p["rides"], key=lambda j: rides[j][0]),
                         "plan": "annual" if p["annual"] else "payg", "home": p["home"], "card": p["card"]})
    # re-registrations: a rider with at least eight rides starts a new account in a gap of two days or more
    rereg = []
    for acc in list(accounts):
        p = persons[acc["pid"]]
        if len(acc["rides"]) < 8 or rs.random() > 0.06:
            continue
        ts = [rides[j][0] for j in acc["rides"]]
        gaps = [g for g in range(2, len(ts) - 2) if ts[g] - rides[acc["rides"][g - 1]][1] > 2 * 86400]
        if not gaps:
            continue
        g = int(rs.choice(gaps))
        last_old = rides[acc["rides"][g - 1]][1]
        new_created = loc(int(last_old + rs.uniform(0.3, 0.9) * (ts[g] - last_old)))
        new = {"pid": acc["pid"], "created": new_created, "rides": acc["rides"][g:], "plan": acc["plan"],
               "home": acc["home"], "card": acc["card"]}
        acc["rides"] = acc["rides"][:g]
        accounts.append(new); rereg.append((acc, new))
    # households: two year-round annual riders of one network and one home area pay with one card
    pool = {}
    for acc in accounts:
        p = persons[acc["pid"]]
        if p["annual"] and p["s"] == 0 and p["e"] == 364 and acc["created"].year < P.YEAR and len(acc["rides"]) >= 12 \
                and acc not in [x for pr in rereg for x in pr]:
            pool.setdefault((p["net"], acc["home"]), []).append(acc)
    house = []
    for key in sorted(pool):
        lst = pool[key]
        rs.shuffle(lst)
        for q in range(0, len(lst) - 1, 2):
            if rs.random() < 0.07:
                lst[q + 1]["card"] = lst[q]["card"]; house.append((lst[q], lst[q + 1]))
    # dormant accounts nobody rode in 2025
    for _ in range(int(len(accounts) * 0.3)):
        home = str(rs.choice(list(P.AREA_NAME), p=[.24, .12, .18, .1, .08, .1, .18]))
        accounts.append({"pid": None, "created": dt.datetime(int(rs.integers(2019, 2025)), int(rs.integers(1, 13)),
                                                              int(rs.integers(1, 28)), int(rs.integers(7, 23)),
                                                              int(rs.integers(0, 60)), tzinfo=P.TZ),
                         "rides": [], "plan": str(rs.choice(["annual", "payg"], p=[.2, .8])),
                         "home": home, "card": "fp_%012x" % int(rs.integers(16 ** 11, 16 ** 12))})
    # ids: legacy numbers for accounts that existed before the platform switch, new ids for every account
    accounts.sort(key=lambda x: (x["created"], x["card"]))
    legacy = int(rs.integers(310000, 330000))
    seen = set()
    for acc in accounts:
        if acc["created"] < MIGRATION:
            legacy += int(rs.integers(1, 4))
            acc["legacy"] = str(legacy)
        else:
            acc["legacy"] = ""
        while True:
            nid = "acct_%08x" % int(rs.integers(16 ** 7, 16 ** 8))
            if nid not in seen:
                break
        seen.add(nid); acc["id"] = nid
    return persons, accounts, rereg, house


# ---------------------------------------------------------------------------------------------------- charging
def charging(W, st):
    """the controller's export: every session with the point's register at plug-in and plug-out. Three stations had
    their controller replaced (registers start again near zero); after a restart a controller re-sends the sessions
    still in its buffer, stamped from the clock it saved before the restart"""
    rs = np.random.default_rng([P.SEED_CHARGE, 1])
    pilot = [k for k in range(W.ND) if W.pilot[k]]
    swap = {}
    for k, (m, d) in zip(sorted(rs.choice(pilot, 3, replace=False)), [(1, 16), (6, 3), (9, 22)]):
        swap[int(k)] = int(dt.datetime(P.YEAR, m, d, 11, int(rs.integers(5, 50)), tzinfo=P.TZ).timestamp())
    reg = {(k, p): int(rs.integers(40000, 380000)) for k in pilot for p in range(1, P.POINTS + 1)}
    out = []
    for (k, p, e, t0, t1, wh) in sorted(W.sessions, key=lambda s: (s[3], s[0], s[1])):
        parts = [(t0, t1, wh)]
        if k in swap and t0 < swap[k] < t1:
            f = (swap[k] - t0) / max(1, t1 - t0)
            parts = [(t0, swap[k], wh * f), (swap[k] + 600, t1, wh * (1 - f))] if t1 > swap[k] + 600 else [(t0, swap[k], wh)]
        for a0, a1, w in parts:
            if k in swap and a0 >= swap[k] and reg.get(("new", k, p)) is None:
                reg[("new", k, p)] = True; reg[(k, p)] = int(rs.integers(0, 60))
            ms = reg[(k, p)]; me = ms + int(round(w)); reg[(k, p)] = me
            out.append({"k": k, "p": p, "e": e, "t0": int(a0), "t1": int(a1), "ms": ms, "me": me, "replay": False})
    # restarts: about one station-day in twelve; the buffer holds the sessions that ended in the day before
    days = range(365)
    replays = []
    ends = {}
    for s in out:
        ends.setdefault(s["k"], []).append(s)
    for k in pilot:
        lst = sorted(ends[k], key=lambda s: s["t1"])
        tl = np.array([s["t1"] for s in lst])
        for d in days:
            if rs.random() > 1 / 12:
                continue
            day = dt.date(P.YEAR, 1, 1) + dt.timedelta(days=d)
            r = int(dt.datetime(day.year, day.month, day.day, int(rs.integers(0, 24)), int(rs.integers(0, 60)), tzinfo=P.TZ).timestamp())
            lag = int(rs.integers(2 * 3600, 9 * 3600))
            lo, hi = np.searchsorted(tl, r - int(rs.integers(18, 31)) * 3600), np.searchsorted(tl, r)
            for s in lst[lo:hi]:
                if k in swap and s["t0"] < swap[k] <= r:
                    continue
                q = dict(s); q["t0"] = s["t0"] - lag; q["t1"] = s["t1"] - lag; q["replay"] = True; q["sent"] = r
                replays.append(q)
    allr = out + replays
    allr.sort(key=lambda s: (s.get("sent", s["t1"]), s["k"], s["p"], s["t0"]))
    for i, s in enumerate(allr):
        s["sid"] = 7100000 + i * 3 + int(rs.integers(0, 3))
    return allr, swap


# ---------------------------------------------------------------------------------------------------- the workshop
FAULT_TEXT = {"BRK": "Brakes", "CHN": "Chain / drivetrain", "TYR": "Tyre or wheel", "LCK": "Dock lock",
              "SAD": "Saddle / seatpost", "LGT": "Lights", "FRM": "Frame / fork", "BAT": "Battery",
              "MOT": "Motor / controller", "DSP": "Display / app link", "CON": "Charging contacts"}


def workshop(W):
    rs = np.random.default_rng([P.SEED_SHOP, 7])
    jobs = sorted(W.jobs, key=lambda j: (j[2], str(j[0])))
    rows = []
    for i, (b, typ, op, cl, code, outcome, retest) in enumerate(jobs):
        rows.append({"job": "WO-25-%05d" % (i + 1 + int(rs.integers(0, 1))), "bike": b, "typ": typ, "open": op,
                     "close": cl, "code": code, "outcome": outcome, "bay": int(rs.integers(1, 5)),
                     "tech": str(rs.choice(["JR", "MS", "AT", "KO", "DL", "PW"])), "retest": retest})
    return rows
