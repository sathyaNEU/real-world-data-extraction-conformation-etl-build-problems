"""The clean truth of the Ravelmond world: the metro network and its service, the riders, every journey with
the itinerary it really took, and the screens. Nothing here is written to the pack; pack.py does that."""
import datetime as dt
import heapq
import random

import params as P

BRANCH_LINE = {"N": "M1", "S": "M1", "W": "M2", "E": "M2"}
BRANCH_SERVICE = {"N": "A", "E": "A", "W": "B", "S": "B"}      # the weekday peak service through Centraal


class Network:
    def __init__(self, rng):
        self.st = {c: {"code": c, "name": n, "branch": b} for c, n, b in P.STATIONS}
        self.lines_of = {c: [] for c in self.st}
        for ln, seq in P.LINES.items():
            for c in seq:
                self.lines_of[c].append(ln)
        self.pos = {ln: {c: i for i, c in enumerate(seq)} for ln, seq in P.LINES.items()}
        self.run = {}
        for ln, seq in P.LINES.items():
            for a, b in zip(seq, seq[1:]):
                t = round(rng.uniform(1.4, 2.6), 1)
                self.run[(ln, a, b)] = t
                self.run[(ln, b, a)] = t
        self.halls = {}
        for c in self.st:
            if c == "CEN":
                self.halls["CEN-HN"] = {"station": "CEN", "walk": {"M1": 1.6, "M2": 3.1}, "name": "Hal Noord"}
                self.halls["CEN-HZ"] = {"station": "CEN", "walk": {"M1": 2.9, "M2": 1.7}, "name": "Hal Zuid"}
            else:
                self.halls[c + "-H"] = {"station": c, "name": "Stationshal",
                                        "walk": {ln: round(rng.uniform(1.1, 2.4), 1) for ln in self.lines_of[c]}}
        self.passages = {k + "-OV": k for k in P.INTERCHANGES}
        self.station_halls = {}
        for h, v in self.halls.items():
            self.station_halls.setdefault(v["station"], []).append(h)

    def branch(self, c):
        return self.st[c]["branch"]

    def ride(self, ln, a, b):
        seq = P.LINES[ln]
        i, j = self.pos[ln][a], self.pos[ln][b]
        step = 1 if j > i else -1
        return round(sum(self.run[(ln, seq[k], seq[k + step])] for k in range(i, j, step)), 1)

    def line_map_route(self, o, d):
        """Minimal transfers, then minimal in-vehicle time, over the published lines: a list of (line, a, b)."""
        best = None
        heap = []
        for ln in self.lines_of[o]:
            heapq.heappush(heap, (0, 0.0, o, ln, ((ln, o),)))
        seen = {}
        while heap:
            nch, t, c, ln, path = heapq.heappop(heap)
            key = (c, ln)
            if key in seen and seen[key] <= (nch, t):
                continue
            seen[key] = (nch, t)
            if c == d:
                best = path
                break
            seq = P.LINES[ln]
            i = self.pos[ln][c]
            for j in (i - 1, i + 1):
                if 0 <= j < len(seq):
                    nxt = seq[j]
                    heapq.heappush(heap, (nch, t + self.run[(ln, c, nxt)], nxt, ln, path))
            for ln2 in self.lines_of[c]:
                if ln2 != ln:
                    heapq.heappush(heap, (nch + 1, t + P.PASSAGE_WALK.get(c, 5.0), c, ln2, path + ((ln2, c),)))
        legs = []
        starts = list(best)
        for k, (ln, a) in enumerate(starts):
            b = starts[k + 1][1] if k + 1 < len(starts) else d
            legs.append((ln, a, b))
        return [lg for lg in legs if lg[1] != lg[2]]


def _route(net, o, d, fewest=True, halls=None, waits=None):
    """Boardings (line, station) of the best route under one costing: fewest changes first (or time only), with the
    halls' walks at both ends when given (a pair of halls), and the expected wait at every boarding when given."""
    h_o, h_d = halls if halls else (None, None)
    heap = []
    for ln in net.lines_of[o]:
        t0 = (net.halls[h_o]["walk"].get(ln, 0.0) if h_o else 0.0) + (waits[ln] if waits else 0.0)
        heapq.heappush(heap, (0 if fewest else 0, t0, o, ln, ((ln, o),)))
    seen = {}
    best = None
    while heap:
        nch, t, c, ln, path = heapq.heappop(heap)
        if c == d:
            tt = t + (net.halls[h_d]["walk"].get(ln, 99.0) if h_d else 0.0)
            if best is None or (nch, tt) < best[0]:
                best = ((nch, tt), path)
            continue
        if (c, ln) in seen and seen[(c, ln)] <= (nch, t):
            continue
        seen[(c, ln)] = (nch, t)
        seq = P.LINES[ln]
        i = net.pos[ln][c]
        for j in (i - 1, i + 1):
            if 0 <= j < len(seq):
                heapq.heappush(heap, (nch, t + net.run[(ln, c, seq[j])], seq[j], ln, path))
        for ln2 in net.lines_of[c]:
            if ln2 != ln:
                extra = P.PASSAGE_WALK.get(c, 5.0) + (waits[ln2] if waits else 0.0)
                heapq.heappush(heap, ((nch + 1) if fewest else 0, t + extra, c, ln2, path + ((ln2, c),)))
    return tuple(best[1])


def route_signatures(net, o, d):
    """Every route a defensible costing picks between two stations: fewest changes then time (the line map), each
    pair of halls' walks added, the expected waits of the peak and of the quiet hours added, and time alone."""
    sigs = {_route(net, o, d)}
    for h_o in net.station_halls[o]:
        for h_d in net.station_halls[d]:
            sigs.add(_route(net, o, d, halls=(h_o, h_d)))
    for band in ("peak", "quiet"):
        wt = {"M1": 1.5 if band == "peak" else 2.5, "M2": 1.5 if band == "peak" else 2.5,
              "M3": (P.M3_HEADWAY["peak"] if band == "peak" else P.M3_HEADWAY["weekend"]) / 2.0}
        sigs.add(_route(net, o, d, waits=wt))
    sigs.add(_route(net, o, d, fewest=False))
    return sigs


_AMBIG = {}


def unsettled(net, o, d):
    """True when the stations' route is not the same under every costing, or when it crosses Centraal on a ring
    line journey: a regular rider makes neither trip."""
    key = (o, d)
    if key not in _AMBIG:
        legs = net.line_map_route(o, d)
        ring_cross = any(lg[0] == "M3" for lg in legs) and any(
            k == "MM" and crosses_centraal(net, u, v) for k, u, v, lg in movements(net, legs))
        _AMBIG[key] = ring_cross or len(route_signatures(net, o, d)) > 1
    return _AMBIG[key]


def headway(line, day, minute):
    wd = day.weekday()
    if line == "M3":
        if wd >= 5 or minute >= 1320:
            return P.M3_HEADWAY["weekend"]
        if 390 <= minute < 600 or 930 <= minute < 1140:
            return P.M3_HEADWAY["peak"]
        return P.M3_HEADWAY["day"]
    bands = P.WEEKDAY_BANDS if wd < 5 else (P.SAT_BANDS if wd == 5 else P.SUN_BANDS)
    for a, b, h in bands:
        if a <= minute < b:
            return h
    return bands[-1][2]


def interworked(day, minute):
    return day.weekday() < 5 and any(a <= minute < b for a, b in P.INTERWORK)


def actual_legs(net, legs, day, minute_at_cen):
    """The legs as the service ran: an M1/M2 movement through Centraal splits or merges by the service in force."""
    out = []
    k = 0
    while k < len(legs):
        ln, a, b = legs[k]
        if ln in ("M1", "M2"):
            # gather the whole M1/M2 movement (a line-map change at CEN joins two legs)
            u, v = a, b
            j = k
            if b == "CEN" and k + 1 < len(legs) and legs[k + 1][0] in ("M1", "M2") and legs[k + 1][1] == "CEN":
                v = legs[k + 1][2]
                j = k + 1
            bu, bv = net.branch(u), net.branch(v)
            crosses = "X" not in (bu, bv) and bu != bv and not (BRANCH_LINE.get(bu) == BRANCH_LINE.get(bv) and
                                                                 _same_side(net, u, v))
            if not crosses or u == "CEN" or v == "CEN":
                if j == k:
                    out.append(legs[k])
                else:
                    out.extend(legs[k:j + 1])
            else:
                if interworked(day, minute_at_cen):
                    change = BRANCH_SERVICE[bu] != BRANCH_SERVICE[bv]
                else:
                    change = BRANCH_LINE[bu] != BRANCH_LINE[bv]
                lu = BRANCH_LINE[bu]
                lv = BRANCH_LINE[bv]
                if change:
                    out.append((lu, u, "CEN"))
                    out.append((lv, "CEN", v))
                else:
                    out.append(("THRU" if lu != lv else lu, u, v))
            k = j + 1
        else:
            out.append(legs[k])
            k += 1
    return out


def _same_side(net, u, v):
    """Two stations of one branch are on the same side of Centraal (no Centraal passing between them)."""
    return net.branch(u) == net.branch(v)


def ride_time(net, leg):
    ln, a, b = leg
    if ln == "THRU":
        return round(net.ride(BRANCH_LINE[net.branch(a)], a, "CEN") + net.ride(BRANCH_LINE[net.branch(b)], "CEN", b), 1)
    return net.ride(ln, a, b)


def leg_line(net, leg, end):
    ln, a, b = leg
    if ln != "THRU":
        return ln
    return BRANCH_LINE[net.branch(a)] if end == "first" else BRANCH_LINE[net.branch(b)]


def minute_of(t):
    return t.hour * 60 + t.minute + t.second / 60.0


def movements(net, legs):
    """Group line-map legs into movements: an M1/M2 movement from u to v (a line-map change at Centraal between
    M1 and M2 is inside one movement), or an M3 leg."""
    mv = []
    k = 0
    while k < len(legs):
        ln, a, b = legs[k]
        if ln in ("M1", "M2") and b == "CEN" and k + 1 < len(legs) and legs[k + 1][0] in ("M1", "M2") \
                and legs[k + 1][1] == "CEN" and legs[k + 1][0] != ln:
            mv.append(("MM", a, legs[k + 1][2], (legs[k], legs[k + 1])))
            k += 2
        elif ln in ("M1", "M2"):
            mv.append(("MM", a, b, (legs[k],)))
            k += 1
        else:
            mv.append(("M3", a, b, (legs[k],)))
            k += 1
    return mv


def crosses_centraal(net, u, v):
    bu, bv = net.branch(u), net.branch(v)
    return bu in "NSWE" and bv in "NSWE" and bu != bv


def line_map_changes_at_cen(net, u, v):
    return crosses_centraal(net, u, v) and BRANCH_LINE[net.branch(u)] != BRANCH_LINE[net.branch(v)]


def simulate(net, rng, day, t_in, o, d, h_in, h_out):
    """One journey from the check-in minute t_in. Returns (duration minutes, list of passages passed,
    list of passages the line map puts, number of Centraal decisions at a peak window)."""
    legs = net.line_map_route(o, d)
    mv = movements(net, legs)
    t = t_in
    first = mv[0]
    first_line = first[3][0][0]
    t += net.halls[h_in]["walk"][first_line] + rng.uniform(-0.2, 0.2)
    passed, linemap, peak_flag = [], [], False
    last_line = None
    for i, (kind, u, v, lg) in enumerate(mv):
        if i > 0:
            # a change between movements at u (an interchange)
            t += P.PASSAGE_WALK[u] + rng.uniform(-0.3, 0.3)
            passed.append(u + "-OV")
            linemap.append(u + "-OV")
        if kind == "M3":
            t += rng.uniform(0, headway("M3", day, t % 1440)) + net.ride("M3", u, v)
            last_line = "M3"
            continue
        lu = lg[0][0]
        if not crosses_centraal(net, u, v):
            # an M1 or M2 movement that does not pass Centraal, or starts or ends there
            if len(lg) == 2:      # the line map changes at CEN between M1 and M2 with u or v at CEN: not possible
                raise ValueError("unexpected")
            t += rng.uniform(0, headway(lu, day, t % 1440)) + net.ride(lu, u, v)
            last_line = lu
            continue
        bu, bv = net.branch(u), net.branch(v)
        line_u, line_v = BRANCH_LINE[bu], BRANCH_LINE[bv]
        if line_map_changes_at_cen(net, u, v):
            linemap.append("CEN-OV")
        t += rng.uniform(0, headway(line_u, day, t % 1440))
        t_cen = t + net.ride(line_u, u, "CEN")
        pk = interworked(day, t_cen % 1440)
        peak_flag = peak_flag or pk
        change = (BRANCH_SERVICE[bu] != BRANCH_SERVICE[bv]) if pk else (line_u != line_v)
        t = t_cen
        if change:
            t += P.PASSAGE_WALK["CEN"] + rng.uniform(-0.3, 0.3)
            passed.append("CEN-OV")
            t += rng.uniform(0, headway(line_v, day, t % 1440))
        else:
            t += 0.5
        t += net.ride(line_v, "CEN", v)
        last_line = line_v
    t += net.halls[h_out]["walk"][last_line] + rng.uniform(-0.2, 0.2)
    return t - t_in, passed, linemap, peak_flag


# ---------------------------------------------------------------- riders and journeys
WORK_PULL = {"CEN": 10.0, "KNO": 3.0, "OSP": 3.5, "KCP": 4.5, "OGD": 1.2, "WSK": 2.4, "HDH": 2.0, "OSE": 0.8,
             "GHP": 3.4, "UNI": 4.2, "STP": 1.6, "RVP": 1.4, "ZDV": 0.9, "ZHV": 0.8,
             "TWB": 2.6, "VSW": 2.2, "HTM": 1.8, "KST": 1.9, "ZTP": 1.0, "WKD": 0.9,
             "RHB": 1.6, "TRV": 0.9, "LDO": 0.8, "BKW": 0.7, "MZT": 0.7, "WLH": 0.6, "KVA": 0.7,
             "SPL": 1.7, "VLH": 1.3, "TNS": 1.0, "ZDW": 0.9, "PDZ": 1.2, "NOP": 0.8}
HOME_PULL = {"KVA": 2.2, "WLH": 1.8, "MZT": 1.6, "BKW": 1.4, "LDO": 1.3, "TRV": 1.1, "RHB": 0.9, "CEN": 1.0,
             "STP": 0.8, "GHP": 1.0, "RVP": 1.2, "UNI": 1.1, "ZDV": 1.5, "ZHV": 1.9,
             "WKD": 1.9, "ZTP": 1.6, "TWB": 1.0, "VSW": 1.2, "HTM": 1.0, "KST": 0.8,
             "WSK": 0.8, "KNO": 0.9, "OSP": 1.0, "HDH": 1.1, "KCP": 0.8, "OGD": 1.6, "OSE": 2.0,
             "ZDW": 1.8, "TNS": 1.6, "SPL": 1.2, "VLH": 1.3, "PDZ": 1.5, "NOP": 1.7}


def pick(rng, weights):
    keys = sorted(weights)
    tot = sum(weights[k] for k in keys)
    x = rng.uniform(0, tot)
    for k in keys:
        x -= weights[k]
        if x <= 0:
            return k
    return keys[-1]


def station_in(net, rng, branch, pull):
    cand = {c: pull[c] for c in net.st if net.branch(c) == branch}
    return pick(rng, cand)


def hall_for(net, rng, station, toward_line):
    hs = net.station_halls[station]
    if len(hs) == 1:
        return hs[0]
    # Centraal: riders mostly use the hall nearer their line, a share the other
    near = "CEN-HN" if toward_line == "M1" else "CEN-HZ"
    far = "CEN-HZ" if near == "CEN-HN" else "CEN-HN"
    return near if rng.random() < 0.8 else far


def days(start, end):
    d = start
    while d <= end:
        yield d
        d += dt.timedelta(days=1)


class Rider:
    def __init__(self, card, kind, home, work, pattern, dpw, am, pm, leisure):
        self.card, self.kind, self.home, self.work = card, kind, home, work
        self.pattern, self.dpw, self.am, self.pm, self.leisure = pattern, dpw, am, pm, leisure


def first_line_from(net, o, d):
    return net.line_map_route(o, d)[0][0]


def make_riders(net, rng):
    riders = []
    for i in range(P.N_REGULAR):
        hb = pick(rng, P.HOME_W)
        home = station_in(net, rng, hb, HOME_PULL)
        wb = pick(rng, P.WORK_W[hb])
        work = station_in(net, rng, wb, WORK_PULL)
        while work == home or unsettled(net, home, work) or unsettled(net, work, home):
            work = station_in(net, rng, pick(rng, P.WORK_W[hb]), WORK_PULL)
        pattern = pick(rng, P.PATTERN_W)
        if pattern == "peak":
            dpw = pick(rng, {5: 0.50, 4: 0.33, 3: 0.17})
            am = min(max(rng.gauss(8 * 60, 16), 7 * 60 + 8), 8 * 60 + 48)
            pm = min(max(rng.gauss(17 * 60 + 5, 18), 16 * 60 + 8), 17 * 60 + 50)
        elif pattern == "shift":
            dpw = pick(rng, {5: 0.35, 4: 0.40, 3: 0.25})
            am = rng.uniform(10 * 60 + 15, 14 * 60 + 30)
            pm = rng.uniform(19 * 60 + 20, 23 * 60 + 10)
        else:
            dpw = pick(rng, {4: 0.30, 3: 0.40, 2: 0.30})
            am = rng.uniform(6 * 60 + 40, 12 * 60)
            pm = rng.uniform(13 * 60, 20 * 60)
        leisure = rng.uniform(0.02, 0.22)
        riders.append(Rider(None, "regular", home, work, pattern, dpw, am, pm, leisure))
    return riders


def cen_window(net, o, d):
    """The earliest and latest minutes after check-in at which a journey can pass Centraal, or None."""
    legs = net.line_map_route(o, d)
    mv = movements(net, legs)
    lo = hi = 0.0
    first_line = mv[0][3][0][0]
    walks = [net.halls[h]["walk"][first_line] for h in net.station_halls[o]]
    lo += min(walks) - 0.2
    hi += max(walks) + 0.2
    for i, (kind, u, v, lg) in enumerate(mv):
        if i > 0:
            lo += P.PASSAGE_WALK[u] - 0.3
            hi += P.PASSAGE_WALK[u] + 0.3
        if kind == "M3":
            lo += net.ride("M3", u, v)
            hi += net.ride("M3", u, v) + P.M3_HEADWAY["weekend"]
            continue
        if crosses_centraal(net, u, v):
            lu = BRANCH_LINE[net.branch(u)]
            return lo + net.ride(lu, u, "CEN"), hi + 10.0 + net.ride(lu, u, "CEN")
        lu = lg[0][0]
        lo += net.ride(lu, u, v)
        hi += net.ride(lu, u, v) + 10.0
    return None


def near_edge(net, o, d, day, t_in):
    """True when a weekday journey whose route crosses Centraal after or before an M3 leg could reach Centraal
    inside a peak service window or within 12 minutes of one: nobody rides the ring line through Centraal in the
    weekday peaks (the commuter flows between the ring and the north and west branches are nil), so such a trip
    by an occasional rider is placed outside them."""
    if day.weekday() >= 5:
        return False
    legs = net.line_map_route(o, d)
    if not any(lg[0] == "M3" for lg in legs):
        return False
    w = cen_window(net, o, d)
    if w is None:
        return False
    a, b = (t_in % 1440) + w[0], (t_in % 1440) + w[1]
    return any(a < e1 + 12 and b > e0 - 12 for e0, e1 in P.INTERWORK)


def place(net, rng, o, d, day, t):
    if not near_edge(net, o, d, day, t):
        return t
    first = rng.choice((-1, 1))
    for step in (first, -first):
        x = t
        while 350 <= x <= 1430:
            x += step * rng.uniform(15, 30)
            if 350 <= x <= 1430 and not near_edge(net, o, d, day, x):
                return x
    raise ValueError("could not place a ring-line trip outside the peak windows")


def single_crossing(net, o, d):
    legs = net.line_map_route(o, d)
    mv = movements(net, legs)
    if len(mv) == 1 and mv[0][0] == "MM" and crosses_centraal(net, mv[0][1], mv[0][2]):
        return mv[0][1], mv[0][2]
    return None


def duration_bound(net, o, d):
    u, v = single_crossing(net, o, d)
    lu, lv = BRANCH_LINE[net.branch(u)], BRANCH_LINE[net.branch(v)]
    walk_in = max(net.halls[h]["walk"][lu] for h in net.station_halls[o])
    walk_out = max(net.halls[h]["walk"][lv] for h in net.station_halls[d])
    return walk_in + 5.0 + net.ride(lu, u, "CEN") + P.PASSAGE_WALK["CEN"] + 0.3 + 5.0 + net.ride(lv, "CEN", v) + \
        walk_out + 0.4


def place_habit(net, rng, o, d, day, t):
    """A habitual rider's weekday trip straight through Centraal is made wholly before or wholly after each change of
    the service pattern (riders keep to the trains they know)."""
    t = place(net, rng, o, d, day, t)
    if day.weekday() >= 5 or single_crossing(net, o, d) is None:
        return t
    bound = duration_bound(net, o, d)
    edges = [e for a, b in P.INTERWORK for e in (a, b)]

    def clash(x):
        return any(x - 3 < e < x + bound + 3 for e in edges)
    if not clash(t):
        return t
    first = rng.choice((-1, 1))
    for step in (first, -first):
        x = t
        while 350 <= x <= 1430:
            x += step * rng.uniform(15, 30)
            if 350 <= x <= 1430 and not clash(x):
                return x
    raise ValueError("could not place a trip through Centraal clear of the service change")


def journeys_for(net, rng, r, start, end):
    """Journeys of one habitual rider from start to end (dates inclusive): (day, t_in_minute, o, d)."""
    out = []
    week_days = {}
    for day in days(start, end):
        week_days.setdefault(day.isocalendar()[1], []).append(day)
    for wk, ds in sorted(week_days.items()):
        wds = [x for x in ds if x.weekday() < 5]
        if rng.random() < 0.035:          # a week away
            continue
        k = min(len(wds), r.dpw)
        chosen = sorted(rng.sample(wds, k)) if wds else []
        for day in chosen:
            if r.pattern == "mixed":
                am = rng.uniform(6 * 60 + 40, 12 * 60)
                pm = am + rng.uniform(3 * 60, 9 * 60)
            else:
                am = r.am + rng.gauss(0, 4)
                pm = r.pm + rng.gauss(0, 5)
            out.append((day, place_habit(net, rng, r.home, r.work, day, am), r.home, r.work))
            if rng.random() < 0.97:
                pm = min(pm, 24 * 60 - 5)
                out.append((day, place_habit(net, rng, r.work, r.home, day, pm), r.work, r.home))
        for day in ds:
            if day.weekday() >= 5 and rng.random() < r.leisure:
                dest = pick(rng, {c: (1.6 if c == "CEN" else 1.0) for c in net.st
                                  if c != r.home and not unsettled(net, r.home, c) and not unsettled(net, c, r.home)})
                t0 = rng.uniform(10 * 60, 17 * 60)
                out.append((day, t0, r.home, dest))
                out.append((day, t0 + rng.uniform(90, 300), dest, r.home))
            elif day.weekday() < 5 and rng.random() < r.leisure * 0.18:
                dest = pick(rng, {c: (1.6 if c == "CEN" else 1.0) for c in net.st
                                  if c != r.home and not unsettled(net, r.home, c) and not unsettled(net, c, r.home)})
                t0 = rng.uniform(19 * 60 + 30, 21 * 60 + 30)
                out.append((day, t0, r.home, dest))
                out.append((day, min(t0 + rng.uniform(90, 200), 24 * 60 - 3), dest, r.home))
    return out


def occasional_journeys(net, rng, start, end):
    """Riders who use the metro now and then: a handful of journeys at any time over the extract."""
    allds = list(days(start, end))
    out = []
    for i in range(P.N_OCCASIONAL):
        home = station_in(net, rng, pick(rng, P.HOME_W), HOME_PULL)
        n = pick(rng, {1: 0.22, 2: 0.30, 3: 0.14, 4: 0.14, 5: 0.08, 6: 0.07, 7: 0.05})
        trips = []
        for _ in range((n + 1) // 2):
            day = rng.choice(allds)
            dest = pick(rng, {c: (2.2 if c == "CEN" else 1.0) for c in net.st if c != home})
            t0 = rng.uniform(7 * 60, 21 * 60)
            t0 = place(net, rng, home, dest, day, t0)
            trips.append((day, t0, home, dest))
            back = min(t0 + rng.uniform(60, 420), 24 * 60 - 4)
            trips.append((day, place(net, rng, dest, home, day, back), dest, home))
        trips = trips[:n]
        wk = {d.isocalendar()[1] for d, *_ in trips if P.WIN_START <= d <= P.WIN_END}
        if len(wk) == 4:
            drop = rng.choice(sorted(wk))
            trips = [x for x in trips if not (P.WIN_START <= x[0] <= P.WIN_END and x[0].isocalendar()[1] == drop)]
        out.append(trips)
    return out


def staff_journeys(net, rng, start, end):
    """Staff and service cards: gate engineers and station staff riding between stations on most working days."""
    codes = sorted(net.st)
    out = []
    for i in range(P.N_STAFF):
        base = rng.choice(codes)
        trips = []
        for day in days(start, end):
            if day.weekday() >= 5 and rng.random() < 0.8:
                continue
            if rng.random() < 0.12:
                continue
            t = rng.uniform(6 * 60 + 30, 9 * 60) if day.weekday() < 6 else rng.uniform(7 * 60 + 5, 9 * 60)
            here = base
            for _ in range(rng.randint(2, 5)):
                there = rng.choice([c for c in codes if c != here])
                t = place(net, rng, here, there, day, t)
                trips.append((day, t, here, there))
                here = there
                t += rng.uniform(40, 120)
            if here != base:
                trips.append((day, place(net, rng, here, base, day, t), here, base))
        out.append(trips)
    return out


# ---------------------------------------------------------------- the whole truth
PRODUCTS = {"MND": "Maandabonnement metro", "SAL": "Reizen op saldo", "STU": "Studentenreisproduct",
            "OUD": "Dal Voordeel 65+", "WRK": "Werkgeverskaart", "PER": "Personeelskaart RVB",
            "SRV": "Servicekaart (test en onderhoud)"}


def card_id(rng):
    return "%04X%04X%04X%04X" % tuple(rng.randrange(65536) for _ in range(4))


class World:
    pass


def build(seed=P.SEED):
    import asks_world as AW
    net = Network(random.Random(seed * 10 + 1))
    rng = random.Random(seed * 10 + 2)
    sim = random.Random(seed * 10 + 3)
    w = World()
    w.net = net
    regular = make_riders(net, rng)
    used = set()

    def new_card():
        while True:
            c = card_id(rng)
            if c not in used:
                used.add(c)
                return c
    journeys = []
    for r in regular:
        r.card = new_card()
        r.product = pick(rng, {"MND": 0.46, "SAL": 0.30, "STU": 0.10, "WRK": 0.10, "OUD": 0.04})
        for (day, t, o, d) in journeys_for(net, rng, r, P.EXTRACT_START, P.EXTRACT_END):
            journeys.append({"card": r.card, "product": r.product, "day": day, "t_in": t, "o": o, "d": d,
                             "group": "habitual"})
    for trips in occasional_journeys(net, rng, P.EXTRACT_START, P.EXTRACT_END):
        c = new_card()
        prod = pick(rng, {"SAL": 0.78, "STU": 0.08, "OUD": 0.10, "MND": 0.04})
        for (day, t, o, d) in trips:
            journeys.append({"card": c, "product": prod, "day": day, "t_in": t, "o": o, "d": d,
                             "group": "occasional"})
    for i, trips in enumerate(staff_journeys(net, rng, P.EXTRACT_START, P.EXTRACT_END)):
        c = new_card()
        prod = "PER" if i % 3 else "SRV"
        for (day, t, o, d) in trips:
            journeys.append({"card": c, "product": prod, "day": day, "t_in": t, "o": o, "d": d, "group": "staff"})
    journeys.sort(key=lambda j: (j["day"], j["t_in"], j["card"]))
    for j in journeys:
        legs = net.line_map_route(j["o"], j["d"])
        j["h_in"] = hall_for(net, sim, j["o"], legs[0][0])
        j["h_out"] = hall_for(net, sim, j["d"], legs[-1][0])
        dur, passed, lm, pk = simulate(net, sim, j["day"], j["t_in"], j["o"], j["d"], j["h_in"], j["h_out"])
        j["dur"] = dur
        j["passed"] = passed
        j["linemap"] = lm
        j["peak"] = pk
        j["checked_out"] = sim.random() > (0.012 if j["group"] != "staff" else 0.002)
    w.journeys = journeys
    w.regular_riders = regular
    A = AW.build(random.Random(seed * 10 + 4 + 1000 * P.ASKS_SALT), net)
    AW.bookings(A)
    AW.billing(A)
    w.asks = A
    return w


def passes(w, rule, cards=None, window=True):
    """Passes per (card, location) for the passenger cards in the window under a rule for the changes:
    'none' (the gates only), 'linemap' (changes where the line map puts them) or 'truth' (where they happened)."""
    import collections
    out = collections.Counter()
    for j in w.journeys:
        if window and not (P.WIN_START <= j["day"] <= P.WIN_END):
            continue
        if j["product"] in ("PER", "SRV"):
            continue
        if cards is not None and j["card"] not in cards:
            continue
        out[(j["card"], j["h_in"])] += 1
        if not j["checked_out"]:
            continue
        out[(j["card"], j["h_out"])] += 1
        locs = [] if rule == "none" else (j["linemap"] if rule == "linemap" else j["passed"])
        for l in locs:
            out[(j["card"], l)] += 1
    return out


def regular_cards(w):
    import collections
    weeks = collections.defaultdict(set)
    for j in w.journeys:
        if P.WIN_START <= j["day"] <= P.WIN_END and j["product"] not in ("PER", "SRV"):
            weeks[j["card"]].add(j["day"].isocalendar()[1])
    return {c for c, s in weeks.items() if len(s) == 4}


def reach(w, rule, reg=None):
    reg = reg if reg is not None else regular_cards(w)
    ps = passes(w, rule, reg)
    out = {}
    for code in P.PACKAGE_ORDER:
        locs = set(P.PACKAGES[code][1])
        n = sum(1 for c in reg if sum(ps[(c, l)] for l in locs) >= P.EFFECTIVE_FREQ)
        out[code] = 100.0 * n / len(reg)
    return out
