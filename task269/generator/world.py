"""The world behind task269's pack: Pellbrook Metro's eight frequent routes, their corridors, branches, stops and timing
points; the timetable as two feeds (the 17 August feed changes running times); the census fortnight simulated stop by
stop (buses dwell for the riders they pick up, early buses hold at timing points, a bus never passes the one ahead on
a shared section) with every rider arriving at random and boarding the first bus that serves where they are going;
and the 2026 pilot's shifts and accounts. Everything is drawn from SEED, so a rebuild is byte-identical."""
import datetime as dt
import math

import numpy as np

import common as K

SEED = 269031

# ------------------------------------------------------------------------------------------------- the network
# Each route: corridor timing points from the City interchange outward (names), stops between consecutive timing
# points, scheduled minutes per segment (off-peak), the peak headway (peak direction) and the counter-peak headway;
# branched routes: two branches beyond the last corridor timing point (the junction), each with its own timing points.
NET = {
    "3": dict(road="Dunstan Road", tps=["City Interchange", "Fenwick Street", "Dunstan Road Shops", "Lockhart Park",
                                        "Dunstan"], stops=[4, 4, 5, 3], run=[5, 5, 6, 4], s_pk=5.0, s_ct=7.5),
    "9": dict(road="Tolland Street", tps=["City Interchange", "Market Square", "Tolland Hospital", "Tolland"],
              stops=[4, 5, 4], run=[5, 6, 5], s_pk=6.0, s_ct=10.0),
    "22": dict(road="Mardale Road", tps=["City Interchange", "Brewery Lane", "Mardale Institute", "Mardale Plaza",
                                         "Mardale"], stops=[4, 4, 4, 4], run=[5, 5, 5, 5], s_pk=5.0, s_ct=7.5),
    "40": dict(road="Harrowby Road", tps=["City Interchange", "Railway Parade", "Harrowby Road Junction",
                                          "Wexcombe Shops", "Harrowby Station", "Harrowby"],
               stops=[4, 4, 4, 4, 3], run=[5, 5, 5, 5, 4], s_pk=4.0, s_ct=6.0),
    "7": dict(road="Hollins Road", tps=["City Interchange", "Carver Street", "Hollins Road Shops", "Kerrigan Corner",
                                        "Hollins Junction"], stops=[4, 4, 4, 4], run=[5, 5, 5, 5], s_pk=5.0, s_ct=7.5,
              branches={"A": dict(name="Hollins Creek", tps=["Hollins Creek School", "Hollins Creek"], stops=[4, 4],
                                  run=[5, 5]),
                        "B": dict(name="Tallis Park", tps=["Tallis Park Shops", "Tallis Park"], stops=[4, 3],
                                  run=[5, 4])}),
    "14": dict(road="Corran Road", tps=["City Interchange", "Corran Road Markets", "Quarry Street", "Corran Hospital",
                                        "Ridgeline Avenue", "Corran Junction"], stops=[4, 4, 4, 4, 3],
               run=[5, 5, 5, 5, 4], s_pk=5.0, s_ct=7.5,
               branches={"A": dict(name="Corran Heights", tps=["Corran Heights Shops", "Corran Heights"],
                                   stops=[4, 3], run=[5, 4]),
                         "B": dict(name="Merrow Downs", tps=["Merrow Downs Station", "Merrow Downs"], stops=[4, 4],
                                   run=[5, 5])}),
    "31": dict(road="Ellery Road", tps=["City Interchange", "Ellery Road Shops", "Bayview Terrace", "Ellery Junction"],
               stops=[5, 4, 4], run=[6, 5, 5], s_pk=6.0, s_ct=10.0,
               branches={"A": dict(name="Ellery Bay", tps=["Ellery Bay Foreshore", "Ellery Bay"], stops=[4, 3],
                                   run=[5, 4]),
                         "B": dict(name="Penhallow", tps=["Penhallow Shops", "Penhallow"], stops=[4, 4],
                                   run=[5, 5])}),
    "52": dict(road="Barrow Road", tps=["City Interchange", "Saltworks Road", "Barrow Road Shops", "Linfield Avenue",
                                        "Barrow Junction"], stops=[4, 4, 4, 4], run=[5, 5, 5, 5], s_pk=5.0, s_ct=7.5,
               branches={"A": dict(name="Barrow Point", tps=["Barrow Point Wharf", "Barrow Point"], stops=[4, 3],
                                   run=[5, 4]),
                         "B": dict(name="Kelland", tps=["Kelland Shops", "Kelland"], stops=[4, 4], run=[5, 5])}),
}

# the dynamics and demand that make each route's record; lag_f is the late branch's lateness as a share of the
# headway, out (leaving the City) and in (reaching the junction); share_late its share of the branch riders
DYN = {
    "3": dict(sig0=2.8, dwell=0.065, rate=1.00),
    "9": dict(sig0=2.55, dwell=0.050, rate=0.80),
    "22": dict(sig0=2.0, dwell=0.045, rate=0.85),
    "40": dict(sig0=2.95, dwell=0.065, rate=1.25),
    "7": dict(lag_out=0.76, late_out="B", lag_in=0.60, late_in="A", trunk_only=0.68, share_late=0.12, dwell=0.055,
              rate=0.95),
    "14": dict(lag_out=0.79, late_out="B", lag_in=0.53, late_in="A", trunk_only=0.15, share_late=0.88, dwell=0.055,
               rate=1.10),
    "31": dict(lag_out=0.80, late_out="B", lag_in=0.74, late_in="A", trunk_only=0.42, share_late=0.50, dwell=0.055,
               rate=0.80),
    "52": dict(lag_out=0.45, late_out="B", lag_in=0.38, late_in="A", trunk_only=0.36, share_late=0.50, dwell=0.045,
               rate=0.85),
}

CROSS = ["Albert Street", "Ashby Road", "Beacon Street", "Birch Avenue", "Bowen Street", "Bramley Road", "Bridge Road",
         "Canning Street", "Cedar Street", "Church Street", "Clifton Road", "Coach Lane", "Collins Way", "Cooper Street",
         "Craig Avenue", "Dalby Street", "Denham Road", "Drummond Street", "Eastwood Road", "Elgin Street",
         "Exeter Road", "Fairview Avenue", "Fenton Street", "Garden Street", "Gilbert Road", "Glebe Street",
         "Grafton Street", "Granville Road", "Hamlyn Street", "Harbour Street", "Hawthorn Avenue", "Heath Road",
         "Hill Street", "Holt Avenue", "Hope Street", "Hughes Road", "Irving Street", "James Street", "Jarvis Road",
         "Keats Street", "Kent Road", "King Street", "Lacey Avenue", "Lambert Street", "Laurel Grove", "Lindsay Road",
         "Lisle Street", "Lyon Street", "Main Street", "Malvern Road", "Manning Street", "Maple Avenue", "Mill Road",
         "Milton Street", "Moore Road", "Nelson Street", "Norfolk Road", "North Terrace", "Oak Street", "Orchard Road",
         "Osborne Street", "Palmer Road", "Park Road", "Parry Street", "Pearce Street", "Percy Road", "Pine Street",
         "Pitt Lane", "Pratt Street", "Prospect Road", "Quay Street", "Queen Street", "Raleigh Road", "Reid Street",
         "River Road", "Robson Avenue", "Rose Street", "Russell Road", "School Road", "Seaton Street", "Short Street",
         "Sinclair Road", "Smith Street", "Somerset Road", "South Street", "Spring Street", "Stanley Road",
         "Station Street", "Sturt Street", "Sutton Road", "Talbot Street", "Tennyson Road", "Thomas Street",
         "Tower Road", "Union Street", "Vale Road", "Vernon Street", "Victoria Road", "Wade Street", "Walker Road",
         "Warren Avenue", "Water Street", "Wattle Avenue", "Wellington Road", "West Street", "White Street",
         "William Street", "Willow Grove", "Wilson Road", "Windsor Road", "York Street"]


def network():
    """Stops and patterns. Every stop has a number (six digits, one a side of the road), a name and whether it is a
    timing point. A route-direction-variant's pattern is its stop numbers in travel order; corridor stops are the
    City interchange to the junction (branched) or to the outer terminus (unbranched)."""
    r = np.random.default_rng([SEED, 1])
    cross = list(CROSS)
    r.shuffle(cross)
    ci = iter(cross * 3)
    stops, patterns, corridor = {}, {}, {}
    stand = {"3": "B3", "9": "A9", "22": "C2", "40": "D4", "7": "B7", "14": "A1", "31": "C3", "52": "D5"}
    for k, rt in enumerate(K.ROUTES):
        N = NET[rt]
        base = 200000 + int(rt) * 1000

        def mk(code, name, tp):
            stops[code] = dict(stop=code, name=name, tp=tp)
            return code

        def segment_names(tp_names, counts, road):
            out = []
            for i, n in enumerate(counts):
                out.append((tp_names[i], True))
                for _ in range(n - 1):
                    out.append(("%s near %s" % (road, next(ci)), False))
            out.append((tp_names[-1], True))
            return out

        cor = segment_names(N["tps"], N["stops"], N["road"])
        # outbound corridor stops (odd last digit), inbound (even), the City interchange a stand of its own
        out_c, in_c = [], []
        for j, (nm, tp) in enumerate(cor):
            if j == 0:
                code_o = mk(100100 + k * 2 + 1, "City Interchange, stand %s" % stand[rt], True)
                code_i = mk(100100 + k * 2 + 2, "City Interchange, arrivals %s" % stand[rt], True)
            else:
                code_o = mk(base + 100 + 2 * j + 1, nm, tp)
                code_i = mk(base + 100 + 2 * j + 2, nm, tp)
            out_c.append(code_o)
            in_c.append(code_i)
        corridor[(rt, "out")] = out_c[:]
        corridor[(rt, "in")] = in_c[::-1]
        if "branches" in N:
            for v, B in N["branches"].items():
                bn = segment_names([N["tps"][-1]] + B["tps"], B["stops"], N["road"] if False else B["name"] + " Road")
                bo, bi = [], []
                for j, (nm, tp) in enumerate(bn[1:], start=1):
                    off = 400 if v == "A" else 600
                    bo.append(mk(base + off + 2 * j + 1, nm, tp))
                    bi.append(mk(base + off + 2 * j + 2, nm, tp))
                patterns[(rt, "out", v)] = out_c + bo
                patterns[(rt, "in", v)] = bi[::-1] + in_c[::-1]
        else:
            patterns[(rt, "out", "")] = out_c
            patterns[(rt, "in", "")] = in_c[::-1]
    return dict(stops=stops, patterns=patterns, corridor=corridor)


# ------------------------------------------------------------------------------------------------- the timetable
BANDS = [(5 * 60 + 30, 6 * 60 + 45, "early"), (6 * 60 + 45, 9 * 60 + 15, "am"), (9 * 60 + 15, 15 * 60 + 15, "inter"),
         (15 * 60 + 15, 18 * 60 + 15, "pm"), (18 * 60 + 15, 23 * 60 + 30, "evening")]


def band(t):
    for a, b, nm in BANDS:
        if a <= t < b:
            return nm
    return "evening"


def headway(rt, direction, t):
    N = NET[rt]
    b = band(t)
    if b == "am":
        return N["s_pk"] if direction == "in" else N["s_ct"]
    if b == "pm":
        return N["s_pk"] if direction == "out" else N["s_ct"]
    if b == "inter":
        return 10.0 if N["s_pk"] <= 5 else 12.0
    return 15.0


def seg_runs(rt, variant, direction, t, feed):
    """Scheduled minutes for each segment between consecutive timing points along the trip's pattern, for a trip whose
    reference time is t. Peak bands run 20 per cent longer; the 17 August feed adds a minute to the corridor's second
    and third segments in the peak bands."""
    N = NET[rt]
    cor = list(N["run"])
    br = list(N["branches"][variant]["run"]) if variant else []
    peak = band(t) in ("am", "pm")
    f = 1.2 if peak else 1.0
    cor = [x * f for x in cor]
    br = [x * f for x in br]
    if feed == 2 and peak:
        for i in (1, 2):
            if i < len(cor):
                cor[i] += 1.0
    if direction == "out":
        return cor + br
    return br[::-1] + cor[::-1]


def tp_positions(rt, variant, direction, pattern, stops):
    return [i for i, s in enumerate(pattern) if stops[s]["tp"]]


def schedule_trip(rt, variant, direction, ref_time, feed, net):
    """Scheduled time (minutes) at every stop of the pattern. ref_time is the time at the City (outbound) or at the
    junction or outer terminus (inbound). Timing points fall on whole minutes; stops between are spread evenly."""
    pat = net["patterns"][(rt, direction, variant)]
    stops = net["stops"]
    tps = tp_positions(rt, variant, direction, pat, stops)
    runs = seg_runs(rt, variant, direction, ref_time, feed)
    assert len(runs) == len(tps) - 1, (rt, variant, direction, len(runs), len(tps))
    times = np.zeros(len(pat))
    if direction == "out":
        t0 = ref_time
    else:
        # inbound: the reference is the junction (branched) or the outer terminus (unbranched)
        nbr = len(NET[rt]["branches"][variant]["run"]) if variant else 0
        t0 = ref_time - sum(runs[:nbr])
    cum = [t0]
    for x in runs:
        cum.append(cum[-1] + x)
    cum = [round(c) for c in cum]
    for k in range(len(tps) - 1):
        a, b = tps[k], tps[k + 1]
        for i in range(a, b + 1):
            times[i] = cum[k] + (cum[k + 1] - cum[k]) * (i - a) / (b - a)
    return np.round(times)


def timetable(feed, net):
    """Every weekday trip of the feed: (trip_id, route, direction, variant, scheduled times at its stops)."""
    trips = []
    for rt in K.ROUTES:
        variants = ["A", "B"] if rt in K.BRANCHED else [""]
        for direction in ("out", "in"):
            t, k = 5 * 60 + 30 + (0 if direction == "out" else 7), 0
            while t < 23 * 60 + 30:
                v = variants[k % len(variants)]
                times = schedule_trip(rt, v, direction, t, feed, net)
                hh, mm = divmod(int(round(t)), 60)
                tid = "%s%s%s-%02d%02d" % (rt, "O" if direction == "out" else "I", v, hh, mm)
                trips.append(dict(trip=tid, route=rt, direction=direction, variant=v, ref=t, times=times))
                t += headway(rt, direction, t)
                k += 1
    return trips


def feed_for(day):
    return 2 if day >= K.CHANGE else 1


# ------------------------------------------------------------------------------------------------- the census
def _rate(t, direction):
    """Riders arriving at a corridor stop a minute, relative: the peak direction's two-hour wave, the counter-peak
    lighter, a floor through the shoulders."""
    am = t < 12 * 60
    peakdir = (am and direction == "in") or ((not am) and direction == "out")
    centre = 8 * 60 if am else 16 * 60 + 45
    wave = math.exp(-0.5 * ((t - centre) / 70.0) ** 2)
    return (1.0 if peakdir else 0.38) * (0.18 + 0.82 * wave)


def simulate(net, seed=SEED, dyn=None):
    """The census fortnight, day by day: every trip of the extract windows run stop by stop, and every rider who
    boarded. Returns departures {(day, trip): array of actual times at the pattern's stops} and riders as a list of
    tuples (day, route, direction, trip, variant, board_index, alight_index, cls)."""
    tt = {1: timetable(1, net), 2: timetable(2, net)}
    deps, riders, sched = {}, [], {}
    for day in K.CENSUS:
        feed = feed_for(day)
        di = K.CENSUS.index(day)
        for rt in K.ROUTES:
            D = (dyn or DYN)[rt]
            day_eff = 1.0 + 0.16 * math.sin(1.7 * di + int(rt))
            rng = np.random.default_rng([seed, 7, di, int(rt)])
            for direction in ("out", "in"):
                trips = [x for x in tt[feed] if x["route"] == rt and x["direction"] == direction
                         and (5 * 60 + 15 <= x["times"][0] <= 10 * 60 + 15 or 13 * 60 + 45 <= x["times"][0] <= 19 * 60)]
                _run_dir(rng, net, rt, direction, trips, D, day, day_eff, deps, riders, sched)
    return dict(deps=deps, riders=riders, sched=sched, timetable=tt)


def _run_dir(rng, net, rt, direction, trips, D, day, day_eff, deps, riders, sched):
    stops = net["stops"]
    branched = rt in K.BRANCHED
    s_of = lambda t: headway(rt, direction, t)
    for x in trips:
        sched[(day, x["trip"])] = x["times"]
    if not branched:
        dev0 = rng.normal(0.4, D["sig0"], len(trips))
        pat = net["patterns"][(rt, direction, "")]
        seq = [dict(trip=x["trip"], variant="", times=x["times"], start=x["times"][0] + dev0[i], pat=pat, offset=0)
               for i, x in enumerate(trips)]
        _corridor(rng, rt, direction, seq, len(pat), stops, D, day, deps, riders)
        return
    if direction == "out":
        late = D["late_out"]
        seq = []
        for x in trips:
            s = s_of(x["times"][0])
            lag = D["lag_out"] * s * day_eff + rng.normal(0, 0.6) if x["variant"] == late else 0.0
            seq.append(dict(trip=x["trip"], variant=x["variant"], times=x["times"],
                            start=x["times"][0] + lag + rng.normal(0, 0.7),
                            pat=net["patterns"][(rt, "out", x["variant"])], offset=0))
        ncor = len(net["corridor"][(rt, "out")])
        _corridor(rng, rt, "out", seq, ncor, stops, D, day, deps, riders)
        for v in ("A", "B"):
            sub = [b for b in seq if b["variant"] == v]
            pat = net["patterns"][(rt, "out", v)]
            _branch(rng, rt, "out", v, sub, list(range(ncor - 1, len(pat))), pat, stops, D, day, deps, riders)
    else:
        late = D["late_in"]
        pats = {v: net["patterns"][(rt, "in", v)] for v in ("A", "B")}
        ncor = len(net["corridor"][(rt, "in")])
        seq = []
        for x in trips:
            s = s_of(x["times"][len(pats[x["variant"]]) - ncor])
            lag = D["lag_in"] * s * day_eff + rng.normal(0, 0.6) if x["variant"] == late else 0.0
            seq.append(dict(trip=x["trip"], variant=x["variant"], times=x["times"],
                            start=x["times"][0] + lag + rng.normal(0, 0.7)))
        for v in ("A", "B"):
            sub = [b for b in seq if b["variant"] == v]
            pat = pats[v]
            nb = len(pat) - ncor
            _branch(rng, rt, "in", v, sub, list(range(0, nb + 1)), pat, stops, D, day, deps, riders)
        # the corridor from the junction: each bus starts there at its branch run's time
        for b in seq:
            nb = len(pats[b["variant"]]) - ncor
            b["start"] = deps[(day, b["trip"])][nb]
            b["offset"] = nb
            b["pat"] = pats[b["variant"]]
        _corridor(rng, rt, "in", seq, ncor, stops, D, day, deps, riders)


def _dwell(D, n):
    return 0.10 + D["dwell"] * n


def _corridor(rng, rt, direction, seq, ncor, stops, D, day, deps, riders):
    """Run buses along the shared corridor in order of their start there, no passing; riders board the first bus
    that serves them: corridor-bound riders (and every inbound rider) any bus, branch-bound riders their branch's.
    Each bus carries its pattern ("pat") and the index at which its corridor run starts ("offset")."""
    branched = rt in K.BRANCHED
    order = sorted(seq, key=lambda b: b["start"])
    last_any = np.full(ncor, -1e9)
    last_v = {"A": np.full(ncor, -1e9), "B": np.full(ncor, -1e9), "": np.full(ncor, -1e9)}
    prev = None
    t_only = D.get("trunk_only", 1.0) if (branched and direction == "out") else 1.0
    late = D.get("late_out", "B")
    share = {late: D.get("share_late", 0.5), ("A" if late == "B" else "B"): 1 - D.get("share_late", 0.5)}
    for b in order:
        key = (day, b["trip"])
        if key not in deps:
            deps[key] = np.full(len(b["times"]), np.nan)
        arr, p, off = deps[key], b["pat"], b["offset"]
        t = b["start"]
        for j in range(ncor):
            gi = off + j
            if j > 0:
                t = t + (b["times"][gi] - b["times"][gi - 1]) * (1 + rng.normal(0, 0.035))
                if stops[p[gi]]["tp"] and t < b["times"][gi] and rng.random() < 0.3:
                    t = b["times"][gi]
            if prev is not None and t < prev[j] + 0.08:
                t = prev[j] + 0.08
            r = _rate(t, direction) * 0.16 * D["rate"]
            last_stop = j == ncor - 1
            gap_any = min(t - last_any[j], 30.0)
            nb = 0
            if branched and direction == "out":
                n_t = 0 if last_stop else int(rng.poisson(max(0.0, r * t_only * gap_any)))
                gap_own = min(t - last_v[b["variant"]][j], 40.0)
                n_v = int(rng.poisson(max(0.0, r * (1 - t_only) * share[b["variant"]] * gap_own)))
                riders.extend([(day, rt, direction, b["trip"], b["variant"], gi, "C")] * n_t)
                riders.extend([(day, rt, direction, b["trip"], b["variant"], gi, b["variant"])] * n_v)
                nb = n_t + n_v
            elif not last_stop:
                nb = int(rng.poisson(max(0.0, r * gap_any)))
                riders.extend([(day, rt, direction, b["trip"], b["variant"], gi, "C")] * nb)
            t = t + _dwell(D, nb)
            arr[gi] = t
            last_any[j] = t
            last_v[b["variant"]][j] = t
        prev = arr[off:off + ncor].copy()


def _branch(rng, rt, direction, v, sub, idx, pat, stops, D, day, deps, riders):
    """A branch's own buses on the branch: outbound from the junction to the terminus (riders there go on along the
    branch), inbound from the terminus to the junction (riders bound for the junction, the corridor or the City)."""
    order = sorted(sub, key=lambda b: (deps[(day, b["trip"])][idx[0]] if direction == "out" else b["start"]))
    last = np.full(len(idx), -1e9)
    prev = None
    for b in order:
        key = (day, b["trip"])
        if key not in deps:
            deps[key] = np.full(len(b["times"]), np.nan)
        arr = deps[key]
        if direction == "out":
            t = arr[idx[0]]
        else:
            t = b["start"]
        for jj, gi in enumerate(idx):
            if jj == 0 and direction == "out":
                last[jj] = t
                continue
            if jj > 0:
                t = t + (b["times"][gi] - b["times"][gi - 1]) * (1 + rng.normal(0, 0.035))
            if jj > 0 and stops[pat[gi]]["tp"] and t < b["times"][gi] and rng.random() < 0.3:
                t = b["times"][gi]
            if prev is not None and t < prev[jj] + 0.08:
                t = prev[jj] + 0.08
            nb = 0
            end = (direction == "out" and gi == len(pat) - 1) or (direction == "in" and jj == len(idx) - 1)
            if not end:
                r = _rate(t, direction) * 0.10 * D["rate"]
                nb = rng.poisson(max(0.0, r * min(t - last[jj], 40.0)))
                riders.extend([(day, rt, direction, b["trip"], v, gi, "V")] * int(nb))
            t = t + _dwell(D, nb)
            arr[gi] = t
            last[jj] = t
        prev = np.array([arr[g] for g in idx])


# ------------------------------------------------------------------------------------------------- the journeys
FARES = (("Adult", 0.57), ("Concession", 0.21), ("Tertiary", 0.09), ("Secondary student", 0.08), ("Senior", 0.05))


def journeys(net, S, seed=SEED):
    """Every rider as the ticketing system keeps the journey: the card, the trip, the stop and time tapped on and,
    unless the rider forgot, the stop and time tapped off. Destinations: corridor-bound riders a stop further along
    the corridor, branch-bound riders a stop on their branch, branch-stop riders further along their way, inbound
    riders mostly the City. Cards: each route's riders draw from a pool of cards weighted like a commuter base."""
    rng = np.random.default_rng([seed, 11])
    pats, cor = net["patterns"], net["corridor"]
    out = []
    for (day, rt, direction, trip, v, gi, cls) in S["riders"]:
        pat = pats[(rt, direction, v)]
        ncor = len(cor[(rt, direction)])
        n = len(pat)
        if direction == "out":
            if cls == "C":
                lo, hi = gi + 1, ncor - 1 if rt in K.BRANCHED else n - 1
            elif cls in ("A", "B"):
                lo, hi = ncor, n - 1
            else:
                lo, hi = gi + 1, n - 1
            k = int(rng.integers(lo, hi + 1))
        else:
            k = n - 1 if rng.random() < 0.55 else int(rng.integers(gi + 1, n))
        out.append((day, rt, direction, trip, v, gi, k, cls))
    order = sorted(range(len(out)), key=lambda i: (out[i][0], out[i][3], out[i][5], i))
    cards = {}
    for rt in K.ROUTES:
        idx = [i for i in order if out[i][1] == rt]
        pool = rng.integers(10 ** 15, 10 ** 16, max(50, len(idx) // 5))
        w = np.minimum(rng.gamma(0.8, 1.0, len(pool)), 4.0)
        pick = rng.choice(len(pool), size=len(idx), p=w / w.sum())
        for i, c in zip(idx, pick):
            cards[i] = int(pool[c])
    fare_names = [f for f, _ in FARES]
    fare_p = np.array([p for _, p in FARES])
    fares = rng.choice(len(fare_names), size=len(out), p=fare_p)
    miss = rng.random(len(out)) < 0.036
    u_on = rng.uniform(0.05, 0.5, len(out))
    u_off = rng.uniform(0.0, 0.3, len(out))
    rows = []
    for n_, i in enumerate(order):
        day, rt, direction, trip, v, gi, k, cls = out[i]
        times = S["deps"][(day, trip)]
        pat = pats[(rt, direction, v)]
        rows.append(dict(day=day, route=rt, direction=direction, trip=trip, variant=v, board=pat[gi],
                         alight=None if miss[n_] else pat[k], on=float(times[gi] - u_on[n_]),
                         off=None if miss[n_] else float(times[k] - u_off[n_]), card=cards[i],
                         fare=fare_names[fares[n_]], cls=cls, alight_true=pat[k]))
    return rows


# ------------------------------------------------------------------------------------------------- the 2026 pilot
HOLIDAYS_2026 = [dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 6, 8)]   # Good Friday, Easter Monday, King's Birthday
POSTS = {"3": ("HP03", "Dunstan Road Shops"), "7": ("HP07", "Hollins Road Shops"), "9": ("HP09", "Tolland Hospital"),
         "14": ("HP14", "Corran Hospital"), "22": ("HP22", "Mardale Institute"), "31": ("HP31", "Ellery Road Shops"),
         "40": ("HP40", "Wexcombe Shops"), "52": ("HP52", "Barrow Road Shops")}
DEPOT_POSTS = {"DSN": "Northern Depot", "DSS": "Southern Depot"}
SHIFTS = {"AM": ((6, 45), (9, 15)), "PM": ((15, 15), (18, 15))}
CANCEL = {"3": 0.030, "7": 0.041, "9": 0.022, "14": 0.036, "22": 0.047, "31": 0.033, "40": 0.028, "52": 0.052}
STAFF = [("Ortega", "Lena"), ("Whitlam", "Craig"), ("Nguyen", "Thi Hoa"), ("Brennan", "Kieran"), ("Sutherland", "Ava"),
         ("Kowalski", "Marek"), ("Ferreira", "Daniela"), ("Okafor", "Chidi"), ("Lindqvist", "Ebba"), ("Rahman", "Faisal"),
         ("Delaney", "Bridget"), ("Petrakis", "Nikos"), ("Halvorsen", "Ingrid"), ("Moana", "Tevita"),
         ("Castellano", "Rocco"), ("Yamada", "Keiko")]


def pilot(seed=SEED):
    """The pilot's shifts as they happened: one post a route, an AM and a PM shift each weekday from the route's wave
    to 26 June (public holidays off), a few shifts with no cover (cancelled) and a few peaks split between two
    supervisors on relief; plus the operator's depot supervisors, who are not the pilot. Returns the staff and the
    shifts (one row a supervisor a post a peak a day)."""
    rng = np.random.default_rng([seed, 21])
    staff = []
    used = set()
    for i, (sur, given) in enumerate(STAFF):
        emp = int(rng.integers(41000, 48999))
        while emp in used:
            emp += 7
        used.add(emp)
        app = "u%04d" % int(rng.integers(2000, 9999))
        role = "Depot Supervisor" if i >= 13 else "Network Supervisor"
        staff.append(dict(emp=emp, app=app, surname=sur, given=given, role=role,
                          depot="Northern" if i % 2 == 0 else "Southern",
                          start=dt.date(2014, 1, 6) + dt.timedelta(days=int(rng.integers(0, 4200)))))
    net_sup = [s for s in staff if s["role"] == "Network Supervisor"]
    dep_sup = [s for s in staff if s["role"] == "Depot Supervisor"]
    start = {}
    for d0, rts in K.WAVES.items():
        for rt in rts:
            start[rt] = d0
    regular = {rt: net_sup[i % len(net_sup)] for i, rt in enumerate(K.ROUTES)}
    regular_pm = {rt: net_sup[(i + 5) % len(net_sup)] for i, rt in enumerate(K.ROUTES)}
    shifts = []
    day = K.PILOT_START
    while day <= K.PILOT_END:
        if day.weekday() < 5 and day not in HOLIDAYS_2026:
            for rt in K.ROUTES:
                if day < start[rt]:
                    continue
                for pk in ("AM", "PM"):
                    who = regular[rt] if pk == "AM" else regular_pm[rt]
                    u = rng.random()
                    if u < CANCEL[rt]:
                        shifts.append(dict(day=day, route=rt, peak=pk, who=None, status="Cancelled"))
                        continue
                    if rng.random() < 0.12:
                        who = net_sup[int(rng.integers(0, len(net_sup)))]
                    if u > 0.97 or (u > 0.9 and rt in ("9", "31", "52") and day.month >= 5):
                        other = net_sup[int(rng.integers(0, len(net_sup)))]
                        if other["emp"] == who["emp"]:
                            other = net_sup[(net_sup.index(who) + 3) % len(net_sup)]
                        shifts.append(dict(day=day, route=rt, peak=pk, who=who, status="Worked", part=1))
                        shifts.append(dict(day=day, route=rt, peak=pk, who=other, status="Worked", part=2))
                    else:
                        shifts.append(dict(day=day, route=rt, peak=pk, who=who, status="Worked", part=0))
            for code in DEPOT_POSTS:
                if rng.random() < 0.6:
                    shifts.append(dict(day=day, route=None, depot=code, peak="AM" if rng.random() < 0.5 else "PM",
                                       who=dep_sup[int(rng.integers(0, len(dep_sup)))], status="Worked", part=0))
        day += dt.timedelta(days=1)
    return dict(staff=staff, shifts=shifts, start=start)


def post_days(P):
    """Each route's pilot weekdays by month (its wave to 26 June, public holidays off): what the operator charges."""
    out = {}
    day = K.PILOT_START
    while day <= K.PILOT_END:
        if day.weekday() < 5 and day not in HOLIDAYS_2026:
            for rt in K.ROUTES:
                if day >= P["start"][rt]:
                    out.setdefault(day.month, {}).setdefault(rt, 0)
                    out[day.month][rt] += 1
        day += dt.timedelta(days=1)
    return out


def pilot_truth(P):
    """Ask A's and Ask B's answers: each route's shifts worked at its pilot post, and the pilot's cost on it (the
    operator's charge for each of the route's post-days plus each month's coordination fee shared by the month's
    shifts worked)."""
    worked = [s for s in P["shifts"] if s.get("route") and s["status"] == "Worked"]
    shifts = {rt: sum(1 for s in worked if s["route"] == rt) for rt in K.ROUTES}
    monthly = {}
    for s in worked:
        monthly.setdefault(s["day"].month, {}).setdefault(s["route"], 0)
        monthly[s["day"].month][s["route"]] += 1
    pdays = post_days(P)
    cost = {}
    for rt in K.ROUTES:
        c = sum(pdays[m].get(rt, 0) for m in pdays) * K.POST_DAY
        for m, fee in K.FEE.items():
            tot = sum(monthly[m].values())
            c += fee * monthly[m].get(rt, 0) / tot
        cost[rt] = c
    return dict(shifts=shifts, cost=cost, monthly=monthly, post_days=pdays)
