"""Every rung and every graded figure, computed from the shipped files under target/ alone."""
import collections
import datetime as dt
import heapq
import math
import os
import re

import io_util as IO

FILES = {
    "journeys": "RVB_metro_ritten_20261001_20261104.csv",
    "network": "RVB_metronet_planningsmodel_2026.xlsx",
    "products": "RVB_productcodes.csv",
    "rate_card": "Spoorbeeld_tariefkaart_2027.pdf",
    "terms": "Spoorbeeld_algemene_voorwaarden_2026.pdf",
    "register": "schermregister_2026-11-12.xlsx",
    "cms": "cms_player_status_20261001_20261104.csv",
    "bookings": "boekingen_najaar_2026.xlsx",
    "legacy": "facturen_oud_systeem_2026.csv",
    "billing": "billing_export_2026-10-15_2026-11-12.xlsx",
    "statements": "bureaucommissie_najaar_2026.pdf",
}
WIN_START, WIN_END = dt.date(2026, 10, 5), dt.date(2026, 11, 1)
SALE_DAY = dt.date(2027, 1, 1)
LINE = {"N": "M1", "S": "M1", "W": "M2", "E": "M2"}
SERVICE = {"N": "A", "E": "A", "W": "B", "S": "B"}


def p(target, key):
    return os.path.join(target, FILES[key])


# ---------------------------------------------------------------- loading
def load_network(target):
    path = p(target, "network")
    h, rows = IO.read_xlsx(path, "Stops")
    stops = {r[0]: {"name": r[1], "lines": str(r[2]).split(";")} for r in rows if r[0]}
    h, rows = IO.read_xlsx(path, "Run times")
    run, seqs = {}, collections.defaultdict(list)
    for ln, a, b, m in rows:
        if not ln:
            continue
        run[(ln, a, b)] = float(m)
        run[(ln, b, a)] = float(m)
        if not seqs[ln]:
            seqs[ln].append(a)
        seqs[ln].append(b)
    h, rows = IO.read_xlsx(path, "Halls")
    halls = {}
    for r in rows:
        if r[0]:
            halls[r[0]] = {"stop": r[1], "walk": {ln: float(v) for ln, v in zip(("M1", "M2", "M3"), r[3:6])
                                                  if v not in (None, "")}}
    h, rows = IO.read_xlsx(path, "Interchanges")
    inter = {r[0]: {"passage": r[1], "walk": float(r[4])} for r in rows if r[0]}
    h, rows = IO.read_xlsx(path, "Gates")
    gates = {r[0]: r[1] for r in rows if r[0]}
    h, rows = IO.read_xlsx(path, "Frequencies")
    freq = [(r[0], r[1], r[2], r[3], float(r[4])) for r in rows if r[0]]
    net = {"stops": stops, "run": run, "seq": dict(seqs), "halls": halls, "inter": inter, "gates": gates, "freq": freq}
    net["pos"] = {ln: {c: i for i, c in enumerate(s)} for ln, s in net["seq"].items()}
    net["lines_of"] = {c: [ln for ln, s in net["seq"].items() if c in s] for c in stops}
    # branches seen from Centraal: which side of CEN each M1/M2 stop lies on
    br = {}
    for c in stops:
        if c == "CEN":
            br[c] = "X"
            continue
        b = None
        for ln, side in (("M1", ("N", "S")), ("M2", ("W", "E"))):
            if c in net["pos"][ln]:
                b = side[0] if net["pos"][ln][c] < net["pos"][ln]["CEN"] else side[1]
        br[c] = b or "P"
    net["branch"] = br
    return net


def load_journeys(target):
    header, rows = IO.read_csv(p(target, "journeys"))
    idx = {k: i for i, k in enumerate(header)}
    out = []
    for r in rows:
        out.append({"card": r[idx["card_id"]], "product": r[idx["product_code"]],
                    "date": dt.date.fromisoformat(r[idx["travel_date"]]), "t_in": r[idx["check_in_time"]],
                    "o": r[idx["check_in_stop"]], "dev_in": r[idx["check_in_gate"]],
                    "t_out": r[idx["check_out_time"]], "d": r[idx["check_out_stop"]],
                    "dev_out": r[idx["check_out_gate"]]})
    return out


def load_products(target):
    header, rows = IO.read_csv(p(target, "products"))
    return {r[0]: r[2] for r in rows}


def load_packages(target):
    """Annex A of the rate card: each package's halls and interchange passages, read from the shipped PDF."""
    txt = IO.pdf_text(p(target, "rate_card"))
    annex = txt[txt.index("Annex A"):]
    pk = collections.OrderedDict()
    for m in re.finditer(r"([A-Z][a-z]+)\s+([A-Z]{3})\s+((?:[A-Z]{3}-(?:H|HN|HZ|OV)\s*\([^)]*\);?\s*)+)", annex):
        pk[m.group(2)] = (m.group(1), re.findall(r"([A-Z]{3}-(?:HN|HZ|OV|H))\s*\(", m.group(3)))
    return pk


def tmin(s):
    h, m, sec = (int(x) for x in s.split(":"))
    return h * 60 + m + sec / 60.0


# ---------------------------------------------------------------- the network's line map
def route(net, o, d, _cache={}):
    key = (id(net), o, d)
    if key in _cache:
        return _cache[key]
    heap = []
    for ln in net["lines_of"][o]:
        heapq.heappush(heap, (0, 0.0, o, ln, ((ln, o),)))
    seen = {}
    best = None
    while heap:
        nch, t, c, ln, path = heapq.heappop(heap)
        if (c, ln) in seen and seen[(c, ln)] <= (nch, t):
            continue
        seen[(c, ln)] = (nch, t)
        if c == d:
            best = path
            break
        s = net["seq"][ln]
        i = net["pos"][ln][c]
        for j in (i - 1, i + 1):
            if 0 <= j < len(s):
                heapq.heappush(heap, (nch, t + net["run"][(ln, c, s[j])], s[j], ln, path))
        for ln2 in net["lines_of"][c]:
            if ln2 != ln:
                walk = net["inter"].get(c, {"walk": 5.0})["walk"]
                heapq.heappush(heap, (nch + 1, t + walk, c, ln2, path + ((ln2, c),)))
    legs = []
    for k, (ln, a) in enumerate(best):
        b = best[k + 1][1] if k + 1 < len(best) else d
        if a != b:
            legs.append((ln, a, b))
    _cache[key] = legs
    return legs


def route_variant(net, o, d, mode, h_in=None, h_out=None):
    """The route under another costing: 'halls' adds the journey's own halls' walks at both ends, 'waits_peak' and
    'waits_quiet' add the expected wait at every boarding, 'fastest' drops the preference for fewer changes."""
    if mode == "fewest":
        return route(net, o, d)
    fewest = mode != "fastest"
    waits = None
    if mode.startswith("waits"):
        pk = mode == "waits_peak"
        waits = {"M1": 1.5 if pk else 2.5, "M2": 1.5 if pk else 2.5, "M3": 2.5 if pk else 5.0}
    heap = []
    for ln in net["lines_of"][o]:
        t0 = (net["halls"][h_in]["walk"].get(ln, 99.0) if mode == "halls" else 0.0) + (waits[ln] if waits else 0.0)
        heapq.heappush(heap, (0, t0, o, ln, ((ln, o),)))
    seen, best = {}, None
    while heap:
        nch, t, c, ln, path = heapq.heappop(heap)
        if c == d:
            tt = t + (net["halls"][h_out]["walk"].get(ln, 99.0) if mode == "halls" else 0.0)
            if best is None or (nch, tt) < best[0]:
                best = ((nch, tt), path)
            continue
        if (c, ln) in seen and seen[(c, ln)] <= (nch, t):
            continue
        seen[(c, ln)] = (nch, t)
        s = net["seq"][ln]
        i = net["pos"][ln][c]
        for j in (i - 1, i + 1):
            if 0 <= j < len(s):
                heapq.heappush(heap, (nch, t + net["run"][(ln, c, s[j])], s[j], ln, path))
        for ln2 in net["lines_of"][c]:
            if ln2 != ln:
                extra = net["inter"][c]["walk"] + (waits[ln2] if waits else 0.0)
                heapq.heappush(heap, ((nch + 1) if fewest else 0, t + extra, c, ln2, path + ((ln2, c),)))
    path = best[1]
    legs = []
    for k, (ln, a) in enumerate(path):
        b = path[k + 1][1] if k + 1 < len(path) else d
        if a != b:
            legs.append((ln, a, b))
    return legs


def ride(net, ln, a, b):
    s = net["seq"][ln]
    i, j = net["pos"][ln][a], net["pos"][ln][b]
    st = 1 if j > i else -1
    return sum(net["run"][(ln, s[k], s[k + st])] for k in range(i, j, st))


def movements(legs):
    mv, k = [], 0
    while k < len(legs):
        ln, a, b = legs[k]
        if ln in ("M1", "M2") and b == "CEN" and k + 1 < len(legs) and legs[k + 1][0] in ("M1", "M2") \
                and legs[k + 1][1] == "CEN" and legs[k + 1][0] != ln:
            mv.append(("MM", a, legs[k + 1][2]))
            k += 2
        else:
            mv.append(("MM" if ln in ("M1", "M2") else "M3", a, b))
            k += 1
    return mv


def crosses(net, u, v):
    bu, bv = net["branch"][u], net["branch"][v]
    return bu in "NSWE" and bv in "NSWE" and bu != bv


# ---------------------------------------------------------------- passes
class Main:
    pass


_CACHE = {}


def _loaded(target):
    if target not in _CACHE:
        _CACHE[target] = (load_network(target), load_journeys(target), load_products(target), load_packages(target))
    return _CACHE[target]


def main_call(target, interwork_rule="duration", halls="gates", staff=False, open_journeys="checkin",
              dating="checkin", count="place", clock_shift=False, weeks_rule="calendar", routing="fewest",
              windows=None):
    """interwork_rule: 'none' (the gates only), 'linemap' (changes where the line map puts them),
    'duration' (each Centraal change read from the journey's own duration, the golden),
    'allday' (the peak pattern assumed for every weekday hour), 'stationpass' (every journey through Centraal).
    The other options are the conventions the closure and the mess checks run: halls from the gate list or from the
    stop alone; staff and service cards kept; a journey without a check-out kept at its check-in or dropped; a
    journey dated by its check-in or its check-out; passes counted per place or per journey; the times after the
    clock change read an hour off; a week as a calendar week or a seven-day block from the window's start."""
    net, js, prod, pk = _loaded(target)
    M = Main()
    M.net, M.packages = net, pk
    M.gap = change_gap(target)
    opts = {"routing": routing, "windows": windows or PEAK_WINDOWS, "gap": M.gap}

    def jdate(j):
        if dating == "checkout" and j["t_out"] and tmin(j["t_out"]) < tmin(j["t_in"]):
            return j["date"] + dt.timedelta(days=1)
        return j["date"]
    win = [j for j in js if WIN_START <= jdate(j) <= WIN_END and (staff or prod.get(j["product"]) == "reiziger")]
    if open_journeys == "drop":
        win = [j for j in win if j["t_out"]]
    weeks = collections.defaultdict(set)
    for j in win:
        d = jdate(j)
        weeks[j["card"]].add(d.isocalendar()[1] if weeks_rule == "calendar" else (d - WIN_START).days // 7)
    reg = {c for c, s in weeks.items() if len(s) == 4}
    M.regular = reg
    M.window_journeys = win
    ps = collections.Counter()
    jp = collections.defaultdict(list)
    M.classified = collections.Counter()

    def hall(gate, stop):
        if halls == "station":
            return "CEN-H*" if stop == "CEN" else stop + "-H"
        return net["gates"][gate]
    for j in win:
        if j["card"] not in reg:
            continue
        jj = j
        if clock_shift and j["date"] >= dt.date(2026, 10, 25):
            jj = dict(j)
            jj["t_in"] = shift_hhmmss(j["t_in"], 60)
            jj["t_out"] = shift_hhmmss(j["t_out"], 60) if j["t_out"] else ""
        locs = [hall(j["dev_in"], j["o"])]
        if j["t_out"]:
            hin, hout = net["gates"][j["dev_in"]], net["gates"][j["dev_out"]]
            locs.append(hall(j["dev_out"], j["d"]))
            if interwork_rule != "none":
                locs += changes(net, jj, hin, hout, interwork_rule, M.classified, opts)
        if count == "journey":
            jp[j["card"]].append(set(locs))
        for loc in locs:
            ps[(j["card"], loc)] += 1
    M.passes = ps
    M.reach = {}
    for code, (name, places) in pk.items():
        places = set(places)
        if halls == "station":
            places = {("CEN-H*" if l in ("CEN-HN", "CEN-HZ") else l) for l in places}
        if count == "journey":
            n = sum(1 for c in reg if sum(1 for s in jp[c] if s & places) >= 3)
        else:
            n = sum(1 for c in reg if sum(ps[(c, l)] for l in places) >= 3)
        M.reach[code] = 100.0 * n / len(reg)
    M.tier = [c for c in pk if M.reach[c] >= 40.0]
    return M


def shift_hhmmss(s, minutes):
    h, m, sec = (int(x) for x in s.split(":"))
    t = (h * 60 + m + minutes) % 1440
    return "%02d:%02d:%02d" % (t // 60, t % 60, sec)


PEAK_WINDOWS = ((420, 570), (960, 1110))


def changes(net, j, hin, hout, rule, tally, opts=None):
    opts = opts or {"routing": "fewest", "windows": PEAK_WINDOWS, "gap": None}
    legs = route_variant(net, j["o"], j["d"], opts["routing"], hin, hout)
    mv = movements(legs)
    out = []
    for i, (kind, u, v) in enumerate(mv):
        if i > 0:
            out.append(net["inter"][u]["passage"])
        if kind != "MM" or not crosses(net, u, v):
            continue
        bu, bv = net["branch"][u], net["branch"][v]
        linemap = LINE[bu] != LINE[bv]
        if rule == "linemap":
            ch = linemap
        elif rule == "stationpass":
            ch = True
        elif rule == "allday":
            ch = (SERVICE[bu] != SERVICE[bv]) if j["date"].weekday() < 5 else linemap
        elif rule.startswith("clock"):
            ch = clock_reading(net, j, hin, hout, mv, i, linemap, rule, opts["windows"])
        else:
            ch = read_change(net, j, hin, hout, mv, i, linemap, tally, rule, opts["gap"])
        if ch:
            out.append("CEN-OV")
    return out


def excess_at_centraal(net, j, hin, hout, u, v):
    """Minutes a journey took over its walks and runs (check-out less check-in, less the hall walks and the run
    times of its one movement through Centraal)."""
    lu, lv = LINE[net["branch"][u]], LINE[net["branch"][v]]
    t_in, t_out = tmin(j["t_in"]), tmin(j["t_out"])
    dur = t_out - t_in if t_out >= t_in else t_out + 1440 - t_in
    base = net["halls"][hin]["walk"][lu] + ride(net, lu, u, "CEN") + ride(net, lv, "CEN", v) + \
        net["halls"][hout]["walk"][lv]
    return dur - base


def change_gap(target):
    """The empty band in the excess of every journey that crosses Centraal in one movement: below it riders stayed on
    their train, above it they changed. Returns (lower edge, upper edge)."""
    net, js, prod, pk = _loaded(target)
    key = ("gap", target)
    if key in _CACHE:
        return _CACHE[key]
    xs = []
    for j in js:
        if not j["t_out"]:
            continue
        mv = movements(route(net, j["o"], j["d"]))
        if len(mv) == 1 and mv[0][0] == "MM" and crosses(net, mv[0][1], mv[0][2]):
            xs.append(excess_at_centraal(net, j, net["gates"][j["dev_in"]], net["gates"][j["dev_out"]], mv[0][1], mv[0][2]))
    xs.sort()
    best = max(((b - a), a, b) for a, b in zip(xs, xs[1:]) if 2.0 <= a <= 15.0)
    _CACHE[key] = (best[1], best[2])
    return _CACHE[key]


def read_change(net, j, hin, hout, mv, i, linemap, tally, rule="duration", gap=None):
    """The golden: a journey through Centraal in one movement changed trains there when its own duration exceeds its
    walks and runs by more than the empty band in the record's excesses (a change adds the passage walk and a
    second wait; a ride through adds only the wait for the first train). A ring-line journey through Centraal (none
    among the regular riders) keeps the line map."""
    kind, u, v = mv[i]
    if len(mv) != 1:
        tally["ring journey: line map"] += 1
        return linemap
    x = excess_at_centraal(net, j, hin, hout, u, v)
    lo, hi = gap
    cut = {"duration": (lo + hi) / 2.0, "duration_lo": lo + 0.05, "duration_hi": hi - 0.05}[rule]
    ch = x > cut
    tally["read: change" if ch else "read: no change"] += 1
    return ch


def clock_reading(net, j, hin, hout, mv, i, linemap, rule, windows):
    """The service pattern read off the clock: the peak pattern on weekdays inside the windows, the line map at every
    other time, with the minute taken at check-in, at Centraal (from the check-in forward or from the check-out
    back) or at check-out."""
    kind, u, v = mv[i]
    bu, bv = net["branch"][u], net["branch"][v]
    lu, lv = LINE[bu], LINE[bv]
    t_in = tmin(j["t_in"])
    t_out = tmin(j["t_out"]) if j["t_out"] else t_in
    if t_out < t_in:
        t_out += 1440
    if rule == "clock_checkin":
        m = t_in
    elif rule == "clock_checkout":
        m = t_out
    elif rule == "clock_cen_forward":
        m = t_in + net["halls"][hin]["walk"][lu] + 1.5 + ride(net, lu, u, "CEN")
    else:
        m = t_out - net["halls"][hout]["walk"][lv] - ride(net, lv, "CEN", v) - 1.0
    pk = j["date"].weekday() < 5 and any(a <= m % 1440 < b for a, b in windows)
    return (SERVICE[bu] != SERVICE[bv]) if pk else linemap


def first_line(mv, net, u):
    kind, a, b = mv[0]
    return "M3" if kind == "M3" else LINE[net["branch"][a]] if net["branch"][a] in LINE else (
        "M1" if a in net["pos"]["M1"] else "M2")


def headway_at(net, day, minute):
    days = "ma-vr" if day.weekday() < 5 else ("za" if day.weekday() == 5 else "zo")
    for ln, dd, a, b, tph in net["freq"]:
        if ln == "M1" and dd == days and tmin(a + ":00") <= minute < tmin(b + ":00") + (1440 if b < a else 0):
            return 60.0 / tph
    return 10.0


# ---------------------------------------------------------------- ask A: make-good per autumn booking
def opening(day):
    wd = day.weekday()
    start = {5: dt.time(6, 30), 6: dt.time(7, 0)}.get(wd, dt.time(5, 45))
    return dt.datetime.combine(day, start), dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0, 30))


def utc_to_local(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:00Z")
    # CEST (+2) until 01:00 UTC on 25 October 2026, CET (+1) after
    return t + dt.timedelta(hours=2 if t < dt.datetime(2026, 10, 25, 1, 0) else 1)


def load_register(target):
    path = p(target, "register")
    h, rows = IO.read_xlsx(path, "Schermen")
    scr = [dict(zip(h, r)) for r in rows if r[0]]
    h, rows = IO.read_xlsx(path, "Bekabeling")
    cab = []
    for r in rows:
        if r[0]:
            a = dt.datetime.strptime(r[2], "%Y-%m-%d %H:%M")
            b = dt.datetime.strptime(r[3], "%Y-%m-%d %H:%M") if r[3] else None
            cab.append((r[0], r[1], a, b))
    return scr, cab


def load_cms(target, clock="local"):
    h, rows = IO.read_csv(p(target, "cms"))
    ev = collections.defaultdict(list)
    for pl, kind, k, t in rows:
        tt = utc_to_local(t) if clock == "local" else dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:00Z")
        ev[pl].append((tt, kind, int(k) if k != "" else None))
    for pl in ev:
        ev[pl].sort()
    return ev


def load_spells(target, clock="local"):
    ev = load_cms(target, clock)
    spells = []
    for pl, lst in ev.items():
        cur = None
        for tt, stt, k in lst:
            if stt == "OFFLINE" and cur is None:
                cur = tt
            elif stt == "ONLINE" and cur is not None:
                spells.append((pl, cur, tt))
                cur = None
        if cur is not None:
            spells.append((pl, cur, None))
    return spells


def recabling_times(target, cab, clock="local"):
    """Where the register moves screens from a player that went offline for good to another player, the move
    happened at the receiving player's first report, after the old player went offline, of the displays it drives
    once the moved screens are added (the register enters a move when its work order is closed)."""
    ev = load_cms(target, clock)
    last_off = {}
    for pl, lst in ev.items():
        state = None
        for tt, kind, k in lst:
            if kind in ("OFFLINE", "ONLINE"):
                state = (kind, tt)
        if state and state[0] == "OFFLINE":
            last_off[pl] = state[1]
    by_tag = collections.defaultdict(list)
    for t, pl, a, b in cab:
        by_tag[t].append((a, pl, b))
    groups = collections.defaultdict(list)      # (old player, new player, register time) -> tags
    for t, lst in by_tag.items():
        lst.sort()
        for (a0, p0, b0), (a1, p1, b1) in zip(lst, lst[1:]):
            if p0 in last_off and b0 == a1:
                groups[(p0, p1, a1)].append(t)
    out = {}
    for (p0, p1, reg), tags in groups.items():
        before = sum(1 for t, pl, a, b in cab if pl == p1 and a < reg and (b is None or b >= reg) and t not in tags)
        when = None
        for tt, kind, k in ev.get(p1, []):
            if last_off[p0] <= tt <= reg and k == before + len(tags):
                when = tt
                break
        out[(p0, p1, reg)] = when
    return out


def load_bookings(target):
    path = p(target, "bookings")
    h, rows = IO.read_xlsx(path, "Boekingen")
    bk = [dict(zip(h, r)) for r in rows if r[0]]
    h, rows = IO.read_xlsx(path, "Geboekte schermen")
    lines = collections.defaultdict(list)
    for r in rows:
        if r[0]:
            lines[r[0]].append(r[1])
    for b in bk:
        b["tags"] = sorted(lines[b["booking_ref"]])
        b["start"] = dt.date.fromisoformat(str(b["flight_start"])[:10])
        b["end"] = dt.date.fromisoformat(str(b["flight_end"])[:10])
        b["booked"] = float(b["booked_screen_hours"])
    return bk


def make_good(target, mapping="cms", takedowns=True, clock="local", allowance=0.005):
    """mapping: 'cms' (the golden: each screen on the player it was cabled to, a re-cabling dated by the receiving
    player's display report), 'register' (the register's connection dates), 'first' (the first player each screen
    had), 'last' (the latest player each screen had, for the whole flight)."""
    scr, cab = load_register(target)
    spells = load_spells(target, clock)
    down = {}
    for s in scr:
        if s["taken_down"]:
            d = dt.date.fromisoformat(str(s["taken_down"])[:10])
            if s["asset_tag"] not in down or d < down[s["asset_tag"]]:
                down[s["asset_tag"]] = d
    # a screen comes down when its player reports no displays on the day the register gives (else at opening)
    cms = load_cms(target, clock)
    down_at = {}
    for tag, d in down.items():
        pls = {pl for t, pl, a, b in cab if t == tag}
        hits = [tt for pl in pls for tt, kind, k in cms.get(pl, []) if kind == "DISPLAYS" and k == 0 and tt.date() == d]
        down_at[tag] = min(hits) if hits else opening(d)[0]
    if mapping == "cms":
        moved = recabling_times(target, cab, clock)
        fix = {}
        for (p0, p1, reg), when in moved.items():
            if when is not None:
                fix[(p0, reg)] = when
                fix[(p1, reg)] = when
        cab = [(t, pl, fix.get((pl, a), a), fix.get((pl, b), b) if b is not None else None) for t, pl, a, b in cab]
    by_tag = collections.defaultdict(list)
    for t, pl, a, b in cab:
        by_tag[t].append((pl, a, b))
    by_pl = collections.defaultdict(list)
    for spl, s0, s1 in spells:
        by_pl[spl].append((s0, s1))
    out = {}
    end_of_time = dt.datetime(2027, 6, 1)
    for b in load_bookings(target):
        dark = 0.0
        for tag in b["tags"]:
            conns = sorted(by_tag[tag], key=lambda x: x[1])
            if mapping == "first":
                conns = [(conns[0][0], conns[0][1], None)]
            elif mapping == "last":
                conns = [(conns[-1][0], conns[0][1], None)]
            day = b["start"]
            while day <= b["end"]:
                o0, o1 = opening(day)
                if takedowns and tag in down:
                    td = down_at[tag]
                    if td < o1:
                        dark += max(0.0, (o1 - max(o0, td)).total_seconds() / 3600.0)
                        o1 = max(o0, td)
                for pl, a, bb in conns:
                    lo_c, hi_c = a, bb or end_of_time
                    for s0, s1 in by_pl[pl]:
                        lo = max(o0, s0, lo_c)
                        hi = min(o1, s1 or end_of_time, hi_c)
                        if lo < hi:
                            dark += (hi - lo).total_seconds() / 3600.0
                day += dt.timedelta(days=1)
        allow = allowance * b["booked"]
        mg = math.ceil(round(dark - allow, 6)) if dark > allow else 0
        out[b["booking_ref"]] = {"dark": dark, "make_good": mg, "booked": b["booked"]}
    return out


# ---------------------------------------------------------------- ask B: screens on sale on 1 January 2027
def screens_on_sale(target, rule="golden"):
    scr, cab = load_register(target)
    names = {code: name for code, (name, locs) in load_packages(target).items()}
    rows = []
    for s in scr:
        rows.append({"tag": s["asset_tag"], "loc": s["location_code"], "pos": s["position"], "pkg": s["package"],
                     "hung": dt.date.fromisoformat(str(s["hung"])[:10]),
                     "down": dt.date.fromisoformat(str(s["taken_down"])[:10]) if s["taken_down"] else None,
                     "status": s["status"]})
    if rule == "status":
        up = [r for r in rows if r["status"] == "in bedrijf"]
    elif rule == "dates_all_rows":
        up = [r for r in rows if r["hung"] <= SALE_DAY and (r["down"] is None or r["down"] > SALE_DAY)]
    else:
        latest = {}
        for r in rows:
            if r["hung"] <= SALE_DAY and (r["tag"] not in latest or r["hung"] > latest[r["tag"]]["hung"]):
                latest[r["tag"]] = r
        up = [r for r in latest.values() if r["down"] is None or r["down"] > SALE_DAY]
        if rule == "golden":
            by_pos = {}
            for r in up:
                k = (r["loc"], r["pos"])
                if k not in by_pos or r["hung"] > by_pos[k]["hung"]:
                    by_pos[k] = r
            up = list(by_pos.values())
    cnt = collections.Counter(r["pkg"] for r in up)
    return {code: cnt.get(code, 0) for code in names}


# ---------------------------------------------------------------- ask C: net revenue per package
def nl_num(s):
    return float(str(s).replace(".", "").replace(",", "."))


MONTHS_NL = {"januari": 1, "februari": 2, "maart": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7, "augustus": 8,
             "september": 9, "oktober": 10, "november": 11, "december": 12}


def load_statements(target):
    txt = IO.pdf_text(p(target, "statements"))
    out = []
    pat = (r"([A-Z][A-Za-z ]+?) \xb7 Commissienota.*?datum (\d+) ([a-z]+) (\d{4}).*?\(([^)]*)\).*?"
           r"Commissie najaarsboekingen 2026\s+([\d.,]+)")
    for m in re.finditer(pat, txt, re.S):
        out.append({"agency": m.group(1).strip(),
                    "date": dt.date(int(m.group(4)), MONTHS_NL[m.group(3)], int(m.group(2))),
                    "refs": [r.strip() for r in m.group(5).split(",")], "amount": nl_num(m.group(6))})
    return out


def net_revenue(target, vat="split", credits="both", commission="rate", parts=False):
    """commission: 'rate' (the golden: each agency's contract rate, recovered from its statement over the value it
    was struck on, applied to each booking's value net of every credit note), 'statements' (the statement's amount
    shared over its bookings by their value net of credit notes), 'standard' (the rate card's 15 per cent),
    'none'."""
    bk = {b["booking_ref"]: b for b in load_bookings(target)}
    pk_of_name = {name: code for code, (name, locs) in load_packages(target).items()}
    h, rows = IO.read_csv(p(target, "legacy"), delimiter=";")
    inv = {}
    for no, date, ref, debtor, gross in rows:
        g = nl_num(gross)
        inv[no] = {"ref": ref, "net": round(g / 1.21, 2) if vat == "split" else (g / 1.21 if vat == "split_exact" else g)}
    h, rows = IO.read_xlsx(p(target, "billing"), "Documents")
    docs = [dict(zip(h, r)) for r in rows if r[0]]
    for d in docs:
        if d["document_type"] == "invoice":
            inv[d["document_no"]] = {"ref": d["booking_ref"], "net": float(d["net_eur"])}
    invoiced = collections.Counter()
    for no, v in inv.items():
        invoiced[v["ref"]] += v["net"]
    cred = collections.defaultdict(list)      # booking -> [(date, amount)]
    for d in docs:
        if d["document_type"] != "credit note" or credits == "none":
            continue
        if credits == "new_only" and not str(d["reference"]).startswith("F"):
            continue
        if d["reference"] in inv:
            cred[inv[d["reference"]]["ref"]].append((dt.date.fromisoformat(str(d["document_date"])[:10]),
                                                    float(d["net_eur"])))
    if parts:
        return {"invoiced": invoiced, "credits": cred}
    net = {r: invoiced[r] + sum(a for _, a in cred[r]) for r in bk}
    comm = collections.Counter()
    if commission in ("rate", "statements"):
        for s in load_statements(target):
            if commission == "rate":
                base = sum(invoiced[r] + sum(a for d, a in cred[r] if d <= s["date"]) for r in s["refs"])
                rate = s["amount"] / base
                for r in s["refs"]:
                    comm[r] = rate * net[r]
            else:
                tot = sum(net[r] for r in s["refs"])
                for r in s["refs"]:
                    comm[r] = s["amount"] * net[r] / tot
    elif commission == "standard":
        for r, b in bk.items():
            if b["agency"]:
                comm[r] = 0.15 * net[r]
    out = collections.Counter()
    for ref, b in bk.items():
        out[pk_of_name[b["package"]]] += net[ref] - comm[ref]
    return {code: out.get(code, 0.0) for code in pk_of_name.values()}


def net_revenue_parts(target):
    """Each booking's invoiced value excluding VAT and its credit notes (date, amount), as the golden reads them."""
    return net_revenue(target, parts=True)
