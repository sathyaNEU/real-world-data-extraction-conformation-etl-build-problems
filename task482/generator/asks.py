"""task482 asks: the pay stations at Wellhaven's bike-share stations, from 24 September 2026 to the 11 January 2027
extract. Nothing here reads or moves a bike, a dock or the station status feed.

Every station has a pay station where a casual rider can buy a single ride or a day pass by card. The pay-station
vendor refurbished the card terminals in the autumn: from 26 October each pay station's terminal was replaced by one
from the vendor's pool of refurbished terminals, and the terminal taken out went to the vendor's workshop and back into
the pool. The vendor's sales export names each sale's pay station from the terminal's present (or, for a terminal in
stock, its last) pay station.

A pay station takes no card while its modem has no connection or its card reader is faulted. It restarts every night
at 3:00 and, when its connection has been down for an hour, on its own watchdog; a restart clears every alarm and the
pay station raises again, at the same second, any fault still present.
"""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import world as W

UTC = dt.timezone.utc
T0 = W.START                                    # 24 September 2026 00:00 local
T1 = W.END                                      # the 11 January 2027 extract
SINGLE, DAYPASS = 3.25, 11.50                   # fares in CAD, HST included
SWAP_FROM = dt.date(2026, 10, 26)
SPARES = 8
MODEL = "Corlund CK-310"
TERMINAL_MODEL = "PX-200"
REGISTER_DAY = dt.date(2027, 1, 8)
# each pay station's alarm stream, chosen so its Q4 service hours without card payments sit inside a whole hour
SALT = {16: 1, 17: 1}


def city_no(sid):
    """the City's station number for a feed station id (Linden Avenue keeps W-17 across its move)"""
    return 17 if sid == W.RELOCATION["new"] else sid - 100


def utc_s(m, sec=0):
    """the absolute instant (aware UTC) of sim minute m plus seconds"""
    return T0 + dt.timedelta(minutes=int(m), seconds=int(sec))


def local_of(t):
    return W.to_local(t)


def local_day_start(d):
    return W.utc_of_local(dt.datetime(d.year, d.month, d.day))


def rng(*key):
    return np.random.default_rng([W.SEED, 4820] + [int(k) for k in key])


# ------------------------------------------------------------------------------------------------- event seconds
def event_seconds(f):
    """the second inside its minute of every recorded event, increasing with the simulation's own order so that
    the pack's clock times keep the order the fleet moved in. The night crew's moves (before 6:00) carry the
    manifest's minute with no seconds, and so does anything the fleet did before them in that minute; a minute's
    other events take distinct seconds 1 to 59."""
    per_min = defaultdict(list)
    manifest = defaultdict(int)
    for t in f.trips:
        per_min[t["start_minute"]].append(t["start_seq"])
        if "end_seq" in t:
            per_min[t["end_minute"]].append(t["end_seq"])
    for mv in f.moves:
        per_min[mv["minute"]].append(mv["seq"])
        if W.LOCAL_MOD[mv["minute"]] < W.SERVICE[0]:
            manifest[mv["minute"]] = max(manifest[mv["minute"]], mv["seq"])
    for fl in f.flags:
        per_min[fl["minute"]].append(fl["seq"])
    sec = {}
    for m, seqs in per_min.items():
        seqs = sorted(seqs)
        rest = [q for q in seqs if q > manifest.get(m, 0)]
        for q in seqs:
            if q <= manifest.get(m, 0):
                sec[q] = 0
        r = rng(1, m)
        k = len(rest)
        assert k <= 59, (m, k)
        picks = np.sort(r.choice(np.arange(1, 60), size=k, replace=False))
        for s_, p in zip(rest, picks):
            sec[s_] = int(p)
    return sec


# ------------------------------------------------------------------------------------------------- terminals
def serial(k):
    r = rng(2, k)
    return "PX2-%04d-%03d" % (int(r.integers(1000, 9999)), int(r.integers(100, 999)))


def working_days(d0, n):
    out, d = [], d0
    while len(out) < n:
        if d.weekday() < 5 and d not in (dt.date(2026, 11, 11),):      # Remembrance Day: no field work
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def swaps():
    """the refurbishment: one pay station a working day from 26 October, in the vendor's route order, each taking
    the pool's longest-ready terminal; a terminal taken out is back in the pool 7 to 10 days later"""
    nos = list(range(1, 25))
    order = list(rng(3).permutation(nos))
    serials = {}
    for k, no in enumerate(nos):
        serials[no] = serial(k)
    spares = [serial(100 + j) for j in range(SPARES)]
    pool = [(dt.datetime(2026, 10, 20, 8, 0), s) for s in spares]        # ready (local), serial
    days = working_days(SWAP_FROM, 40)
    out, di = [], 0
    for no in order:
        while True:
            d = days[di]
            r = rng(4, no)
            start = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(r.integers(9 * 60 + 20, 14 * 60 + 40)),
                                                                       seconds=int(r.integers(0, 60)))
            ready = sorted(x for x in pool if x[0] <= start)
            if ready:
                break
            di += 1
        di += 1
        pool.remove(ready[0])
        installed = ready[0][1]
        removed = serials[no]
        took = int(r.integers(26 * 60, 68 * 60))
        boot = int(r.integers(40, 95))
        back = start + dt.timedelta(days=int(r.integers(7, 11)))
        pool.append((dt.datetime(back.year, back.month, back.day, 8, 0), removed))
        serials[no] = installed
        out.append(dict(no=no, start=start, removed=removed, installed=installed, install=start + dt.timedelta(seconds=took),
                        restart=start + dt.timedelta(seconds=took + boot), tech=1 + int(r.integers(0, 4))))
    stock = [(s, ready) for ready, s in sorted(pool)]
    return out, serials, stock


def terminal_at():
    """each pay station's terminal over time: (start local, end local, serial)"""
    sw, final, stock = swaps()
    first = {no: serial(no - 1) for no in range(1, 25)}
    spans = defaultdict(list)
    by_no = {s["no"]: s for s in sw}
    for no in range(1, 25):
        s = by_no[no]
        spans[no].append((None, s["start"], first[no]))
        spans[no].append((s["install"], None, s["installed"]))
    return spans, sw, final, stock


# ------------------------------------------------------------------------------------------------- weather
def daily_weather():
    """Wellhaven's daily weather, 24 September 2026 to 10 January 2027: (max C, min C, rain mm, snow cm); the
    fleet's demand factors (world.weather) set the wet days"""
    wx = W.weather(W.SEED)
    r = np.random.default_rng([W.SEED, 12])
    out = {}
    d = W.DAY0
    while d <= dt.date(2027, 1, 10):
        doy = (d - dt.date(2026, 1, 1)).days
        mean = 8.5 - 13.5 * math.cos(2 * math.pi * (doy - 15) / 365.0) + float(r.normal(0, 2.4))
        spread = 6.0 + float(r.uniform(0, 5))
        f = wx[d]
        rain = snow = 0.0
        if f == 0.65:
            rain = round(float(r.gamma(2.0, 4.0)), 1)
        elif f == 0.45:
            if mean < 1.0:
                snow = round(float(r.gamma(2.0, 3.5)), 1)
            else:
                rain = round(float(r.gamma(2.0, 3.0)), 1)
                snow = round(float(r.gamma(1.2, 1.5)), 1)
        elif r.random() < 0.15:
            rain = round(float(r.uniform(0.2, 1.6)), 1)
        out[d] = (round(mean + spread / 2, 1), round(mean - spread / 2, 1), rain, snow)
        d += dt.timedelta(days=1)
    return out


WEATHER = daily_weather()


# ------------------------------------------------------------------------------------------------- alarms
def whole(t):
    """an instant to the whole second, as the pay station's log writes it"""
    return t.replace(microsecond=0)


def next_working(d):
    d = d + dt.timedelta(days=1)
    while d.weekday() >= 5 or d == dt.date(2026, 11, 11):
        d += dt.timedelta(days=1)
    return d


def alarms(sw):
    """each pay station's alarm and restart events (aware UTC instants, whole seconds), the spans it could take no
    card, and the technicians' visits (reader repairs and receipt paper)"""
    nights = []
    d = dt.date(2026, 9, 24)
    while d <= dt.date(2027, 1, 10):
        nights.append(d)
        d += dt.timedelta(days=1)
    events = {no: [] for no in range(1, 25)}
    down = {no: [] for no in range(1, 25)}
    visits = {no: [] for no in range(1, 25)}
    swap_of = {s["no"]: s for s in sw}
    for no in range(1, 25):
        r = rng(5, no, SALT.get(no, 0))
        rd = rng(10, no)
        ev = events[no]
        restarts = {}
        for d in nights:
            t = W.utc_of_local(dt.datetime(d.year, d.month, d.day, 3, 0)) + dt.timedelta(seconds=int(r.integers(20, 75)))
            restarts[t] = "nightly"
        s = swap_of[no]
        swap_rm = W.utc_of_local(s["start"])
        swap_up = W.utc_of_local(s["restart"])
        restarts[swap_up] = "swap"
        quiet = (swap_rm - dt.timedelta(hours=3), swap_up + dt.timedelta(hours=1))
        conds = []
        busy = {"COMMS": T0, "READER": T0}
        t = T0 + dt.timedelta(hours=float(r.uniform(2, 40)))
        while True:
            mo = W.to_local(t).month
            rate = {9: 0.10, 10: 0.11, 11: 0.16, 12: 0.24, 1: 0.24}[mo]     # outages a day, more in the cold
            t = whole(t + dt.timedelta(days=float(r.exponential(1.0 / rate))))
            if t >= T1:
                break
            dur = float(np.exp(r.normal(math.log(26 * 60), 1.05)))
            conds.append((t, whole(t + dt.timedelta(seconds=max(70.0, dur))), "COMMS"))
        t = T0 + dt.timedelta(days=float(r.uniform(3, 30)))
        while t < T1:
            t = whole(t)
            ld = next_working(W.to_local(t).date())
            fix = W.utc_of_local(dt.datetime(ld.year, ld.month, ld.day) + dt.timedelta(
                minutes=int(r.integers(9 * 60, 15 * 60)), seconds=int(r.integers(0, 60))))
            conds.append((t, fix, "READER"))
            t = t + dt.timedelta(days=float(r.exponential(32.0)))
        for (a, b, kind) in sorted(conds, key=lambda x: x[0]):
            if a < busy[kind] or (a < quiet[1] and b > quiet[0]) or b >= T1:
                continue
            code, ok, pfix = (("COMMS_LOST", "COMMS_RESTORED", 0.5) if kind == "COMMS"
                              else ("READER_FAULT", "READER_OK", 0.6))
            ev.append((a, code))
            end, last_raise, cur = None, a, a
            while end is None:
                cands = [x for x in restarts if cur < x < b]
                if kind == "COMMS" and last_raise + dt.timedelta(minutes=60) < b:
                    cands.append(last_raise + dt.timedelta(minutes=60))
                nxt = min(cands) if cands else None
                if nxt is None:
                    end = b
                    ev.append((b, ok))
                    if kind == "READER":
                        visits[no].append((b, "reader"))
                        ev.append((b - dt.timedelta(seconds=int(rd.integers(6 * 60, 26 * 60))), "DOOR_OPEN"))
                        ev.append((b + dt.timedelta(seconds=int(rd.integers(60, 240))), "DOOR_CLOSED"))
                    break
                if nxt not in restarts:
                    restarts[nxt] = "watchdog"
                if r.random() < pfix:
                    end = nxt
                else:
                    ev.append((nxt, code))
                    last_raise = nxt
                cur = nxt
            down[no].append((a, end))
            busy[kind] = end
        # the swap: the terminal is taken out (reader alarm) and the pay station restarts once the new one is in
        ev.append((swap_rm, "READER_FAULT"))
        down[no].append((swap_rm, swap_up))
        ev.append((swap_rm - dt.timedelta(seconds=int(r.integers(15, 50))), "DOOR_OPEN"))
        ev.append((swap_up + dt.timedelta(seconds=int(r.integers(20, 80))), "DOOR_CLOSED"))
        # receipt paper runs low every one to three weeks and is refilled at a technician's visit
        t = T0 + dt.timedelta(days=float(r.uniform(1, 12)))
        while t < T1:
            t = whole(t)
            ev.append((t, "PAPER_LOW"))
            ld = W.to_local(t).date() + dt.timedelta(days=int(r.integers(1, 4)))
            while ld.weekday() >= 5:
                ld += dt.timedelta(days=1)
            fix = W.utc_of_local(dt.datetime(ld.year, ld.month, ld.day) + dt.timedelta(
                minutes=int(r.integers(9 * 60, 16 * 60)), seconds=int(r.integers(0, 60))))
            if fix < T1:
                ev.append((fix - dt.timedelta(seconds=int(r.integers(30, 120))), "DOOR_OPEN"))
                ev.append((fix, "PAPER_OK"))
                ev.append((fix + dt.timedelta(seconds=int(r.integers(30, 120))), "DOOR_CLOSED"))
                visits[no].append((fix, "paper"))
            t = t + dt.timedelta(days=float(r.uniform(7, 20)))
        rt = rng(9, no)
        last = T0
        for d, (tmax, tmin, rain, snow) in sorted(WEATHER.items()):
            if tmin > -2.0:
                continue
            k = int(rt.poisson(1.2 + 0.35 * (-2.0 - tmin)))
            for t in sorted(W.utc_of_local(dt.datetime(d.year, d.month, d.day)) +
                            dt.timedelta(seconds=int(x)) for x in rt.integers(0, 86400, size=k)):
                if t <= last or t >= T1:
                    continue
                ok = t + dt.timedelta(seconds=int(rt.integers(18 * 60, 110 * 60)))
                ev.append((t, "TEMP_LOW"))
                ev.append((ok, "TEMP_OK"))
                last = ok
        for x in restarts:
            if T0 <= x < T1:
                ev.append((x, "RESTART"))
        # a restart comes first in its second; the faults still present are raised again after it
        ev.sort(key=lambda e: (e[0], 0 if e[1] == "RESTART" else 1))
        down[no] = merge(down[no])
    return events, down, visits


def merge(spans):
    out = []
    for a, b in sorted(spans):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def is_down(spans, t):
    for a, b in spans:
        if a <= t < b:
            return True
        if a > t:
            return False
    return False


# ------------------------------------------------------------------------------------------------- sales
CASUAL = {"core": (0.30, 0.50), "campus": (0.20, 0.35), "hub": (0.25, 0.45), "res": (0.20, 0.40), "park": (0.55, 0.75)}


def rider_types(f):
    """member, casual or staff for each trip (the trips export's rider type)"""
    out = {}
    r = rng(6)
    for t in f.trips:
        if t["user"] == "staff":
            out[t["trip"]] = "staff"
            continue
        loc = W.to_local(utc_s(t["start_minute"]))
        kind = f.st[t["start_station"]]["kind"]
        p = CASUAL[kind][1 if loc.weekday() >= 5 else 0]
        out[t["trip"]] = "casual" if r.random() < p else "member"
    return out


def sales(f, sec, rtype, down):
    """the pay stations' card sales: some casual riders pay at the pay station a minute or three before they unlock"""
    r = rng(7)
    out = []
    for t in f.trips:
        if rtype[t["trip"]] != "casual":
            continue
        u = r.random()
        day = r.random()
        lead = int(r.integers(35, 211))
        if u >= 0.42:
            continue
        start = utc_s(t["start_minute"], sec[t["start_seq"]])
        when = start - dt.timedelta(seconds=lead)
        no = city_no(t["start_station"])
        if when < T0 or is_down(down[no], when):
            continue
        weekend = W.to_local(when).weekday() >= 5
        product = "Day pass" if day < (0.40 if weekend else 0.26) else "Single ride"
        out.append(dict(no=no, when=when, product=product, amount=DAYPASS if product == "Day pass" else SINGLE))
    out.sort(key=lambda x: x["when"])
    return out


def everything():
    f = W.fleet()
    sec = event_seconds(f)
    rtype = rider_types(f)
    spans, sw, final, stock = terminal_at()
    events, down, visits = alarms(sw)
    sl = sales(f, sec, rtype, down)
    for s in sl:
        loc = W.to_local(s["when"])
        s["terminal"] = next(x[2] for x in spans[s["no"]] if (x[0] is None or x[0] <= loc) and (x[1] is None or loc < x[1]))
    r = rng(8)
    voids = []
    for i, s in enumerate(sl):
        if r.random() < 0.012:
            voids.append(dict(of=i, when=s["when"] + dt.timedelta(seconds=int(r.integers(25, 160)))))
    return dict(f=f, sec=sec, rtype=rtype, spans=spans, swaps=sw, final=final, stock=stock, events=events, down=down,
                visits=visits, sales=sl, voids=voids)


# ------------------------------------------------------------------------------------------------- truths
QA = W.utc_of_local(dt.datetime(2026, 10, 1))
QB = W.utc_of_local(dt.datetime(2027, 1, 1))


def sales_truth(E):
    """each station's Q4 2026 pay-station card sales: approved sales less voids, at the pay station the sale was made"""
    voided = {v["of"] for v in E["voids"]}
    tot = defaultdict(float)
    for i, s in enumerate(E["sales"]):
        if QA <= s["when"] < QB and i not in voided:
            tot[s["no"]] += s["amount"]
    return {no: round(tot[no], 2) for no in range(1, 25)}


def service_spans(d0, d1):
    """the service-hour spans (6:00 to midnight local) of every day from d0 to d1 inclusive, as aware UTC pairs"""
    out = []
    d = d0
    while d <= d1:
        a = W.utc_of_local(dt.datetime(d.year, d.month, d.day, 6, 0))
        b = W.utc_of_local(dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1))
        out.append((a, b))
        d += dt.timedelta(days=1)
    return out


SERVICE_Q4 = service_spans(dt.date(2026, 10, 1), dt.date(2026, 12, 31))


def overlap_s(spans, windows=SERVICE_Q4):
    tot = 0.0
    j = 0
    for a, b in spans:
        for (x, y) in windows:
            lo, hi = max(a, x), min(b, y)
            if hi > lo:
                tot += (hi - lo).total_seconds()
    return tot


def down_truth(E):
    """each station's Q4 2026 service hours with its pay station unable to take a card payment"""
    return {no: round(overlap_s(E["down"][no]) / 3600.0, 4) for no in range(1, 25)}


if __name__ == "__main__":
    E = everything()
    st = sales_truth(E)
    dn = down_truth(E)
    names = {s[0] - 100: s[1] for s in W.STATIONS}
    for no in range(1, 25):
        print("W-%02d %-20s sales %9.2f  down %7.2f h  events %d" % (no, names[no], st[no], dn[no], len(E["events"][no])))
    print("sales rows", len(E["sales"]), "voids", len(E["voids"]))
    for s in E["swaps"]:
        print(s["no"], s["start"], s["removed"], "->", s["installed"])
    print("stock", E["stock"])
