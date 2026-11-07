"""task490 clean truth: the season's boats through every summit lock (cycle by cycle), the reservoirs' releases and
the abstraction meters. Nothing here is a shipped file; records.py writes those from this truth."""
import heapq
import math
from datetime import datetime, timedelta, date

import numpy as np

import world as W

MIN = timedelta(minutes=1)


def rng(tag):
    return np.random.default_rng(abs(hash_tag(tag)) % (2 ** 32))


def hash_tag(tag):
    h = 2166136261
    for ch in "task490:" + tag:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


# ------------------------------------------------------------------------------------------------- boats
NAME_A = ["Kingfisher", "Dunlin", "Mallard", "Heron", "Otter", "Wren", "Curlew", "Teal", "Swift", "Merlin", "Plover",
          "Linnet", "Skylark", "Moorhen", "Dipper", "Redshank", "Kestrel", "Sandpiper", "Bittern", "Grebe", "Avocet",
          "Fieldfare", "Siskin", "Nuthatch", "Lapwing", "Whimbrel", "Shelduck", "Goldcrest", "Stonechat", "Yellowhammer"]
NAME_B = ["Evening Star", "Morning Mist", "Quiet Waters", "Second Wind", "Slow Lane", "Water Gypsy", "Free Spirit",
          "Lazy Days", "Dragonfly", "Willow", "Bramble", "Hawthorn", "Rowan", "Foxglove", "Harebell", "Meadowsweet",
          "Celandine", "Primrose", "Clementine", "Matilda", "Rosie Lee", "Old Faithful", "Pipe Dream", "Tranquility",
          "Persistence", "Ad Lib", "Nomad", "Wanderlust", "Contentment", "Serendipity", "Jubilee", "Hesperus",
          "Ariadne", "Calypso", "Halcyon", "Odyssey", "Brief Encounter", "Last Chance", "Silver Birch", "Sloe Gin"]
NAME_C = ["II", "III", "of Ludford", "Rose", "Belle", "Lady", "Spirit", "Dream"]


def boat_pool():
    r = rng("boats")
    boats = []
    used_idx, used_name = set(), set()
    for i in range(5200):
        while True:
            idx = "%06d" % r.integers(500100, 539990)
            if idx not in used_idx:
                break
        used_idx.add(idx)
        kind = r.random()
        if kind < 0.09:
            typ, length, beam = "cruiser", int(r.integers(21, 36)), round(float(r.uniform(7.0, 9.5)), 1)
        elif kind < 0.15:
            typ, length, beam = "wide beam", int(r.integers(50, 66)), round(float(r.uniform(10.0, 12.5)), 1)
        else:
            typ, length, beam = "narrowboat", int(min(70, max(30, round(r.normal(57, 7))))), 6.8
        if typ == "cruiser":
            beam = min(beam, 6.9) if r.random() < 0.55 else beam
        for _ in range(50):
            p = r.random()
            if p < 0.45:
                nm = NAME_B[r.integers(len(NAME_B))]
            elif p < 0.8:
                nm = NAME_A[r.integers(len(NAME_A))]
            else:
                nm = NAME_A[r.integers(len(NAME_A))] + " " + NAME_C[r.integers(len(NAME_C))]
            if nm not in used_name or r.random() < 0.35:
                break
        used_name.add(nm)
        visitor = r.random() < 0.055
        boats.append(dict(idx=idx, name=nm, type=typ, length=length, beam=beam, visitor=visitor,
                          vp="VP26-%05d" % r.integers(10000, 39999) if visitor else ""))
    fleet = []
    hire_names = ["Kelsby Kestrel", "Kelsby Lapwing", "Kelsby Curlew", "Kelsby Merlin", "Kelsby Plover",
                  "Kelsby Heron", "Kelsby Swift", "Kelsby Wren", "Kelsby Teal", "Kelsby Dunlin", "Kelsby Grebe",
                  "Kelsby Linnet", "Kelsby Siskin", "Kelsby Redwing", "Kelsby Otter", "Kelsby Moorhen",
                  "Kelsby Dipper", "Kelsby Avocet", "Kelsby Bittern", "Kelsby Stonechat", "Kelsby Skylark",
                  "Kelsby Whimbrel"]
    for nm in hire_names[:W.TRAFFIC["Kelsby"]["hire_fleet"]]:
        while True:
            idx = "%06d" % r.integers(500100, 539990)
            if idx not in used_idx:
                break
        used_idx.add(idx)
        fleet.append(dict(idx=idx, name=nm, type="narrowboat", length=int(r.choice([45, 50, 55, 58, 62, 66, 68])),
                          beam=6.8, visitor=False, vp="", hire=True))
    return boats, fleet


# ------------------------------------------------------------------------------------------------- locks
class Lock:
    def __init__(self, spec):
        self.s = spec
        self.asset = spec["asset"]
        self.broad = spec["broad"]
        self.state = "L"            # every summit chamber is left empty when the flights reopen on 1 April
        self.free_at = None
        self.hold_until = None
        self.top = []               # boats waiting to go down (on the summit pound)
        self.bot = []               # boats waiting to come up
        self.cycles = []
        self.closures = W.CLOSURES.get(self.asset, [])
        self.last_start = None
        self.reset_done = set()

    def closed(self, t):
        return any(a <= t < b for a, b in self.closures)

    def reopen_after(self, t):
        for a, b in self.closures:
            if a <= t < b:
                return b
        return None

    def allowed_start(self, t):
        """the earliest time at or after t at which a cycle may start."""
        b = self.reopen_after(t)
        if b is not None:
            t = b
        if self.asset == "TC/L08":
            a, z = W.TILSEY_RESTRICTION
            if a <= t < z:
                h0, h1 = W.RESTRICTED_HOURS
                day0 = t.replace(hour=h0, minute=0, second=0, microsecond=0)
                day1 = t.replace(hour=h1, minute=0, second=0, microsecond=0)
                if t < day0:
                    t = day0
                elif t >= day1:
                    t = day0 + timedelta(days=1)
                if t >= z:
                    t = max(t, z)
        return t


def can_pair(lock, a, b):
    if lock.broad:
        return a["beam"] <= 7.0 and b["beam"] <= 7.0
    return a["beam"] <= 7.0 and b["beam"] <= 7.0 and a["length"] + b["length"] <= 70


def simulate_summit(summit, boats, fleet):
    """event-driven simulation of one summit's two locks over the season. Returns {asset: [cycle, ...]}."""
    r = rng("traffic:" + summit)
    p = W.TRAFFIC[summit]
    la, lb = [Lock(l) for l in W.LOCKS if l["summit"] == summit]
    locks = {la.asset: la, lb.asset: lb}
    other = {la.asset: lb.asset, lb.asset: la.asset}
    heap, seq = [], [0]

    def push(t, kind, payload):
        seq[0] += 1
        heapq.heappush(heap, (t, seq[0], kind, payload))

    transit = {"Kelsby": (55, 95), "Harnock": (35, 70), "Tilsey": (25, 50)}[summit]
    pool = [b for b in boats if (summit == "Harnock" or b["beam"] <= 7.0)]
    pool_w = np.array([1.0 + (3.0 if i % 7 == 0 else 0.0) for i in range(len(pool))])
    pool_w /= pool_w.sum()

    def pick_boat():
        return pool[int(r.choice(len(pool), p=pool_w))]

    def day_time(d, lo=8.0, hi=19.5):
        while True:
            c = 10.6 if r.random() < 0.52 else 14.6
            h = r.normal(c, 1.9)
            if lo <= h <= hi:
                return datetime(d.year, d.month, d.day) + timedelta(hours=float(h))

    # journeys
    for d in W.DAYS:
        w = W.MONTH_W[d.month] * W.DOW_W[d.weekday()]
        n = int(r.poisson(p["through"] * w))
        for _ in range(n):
            b = pick_boat()
            if summit == "Kelsby":
                first = p["ring_main"] if r.random() < p["ring_share"] else other[p["ring_main"]]
            else:
                first = la.asset if r.random() < 0.5 else lb.asset
            t = day_time(d)
            u = r.random()
            if u < p["moor"]:
                plan = ("moor", other[first] if r.random() < 0.7 else first)
            else:
                plan = ("cross", other[first])
            push(t, "arrive", dict(boat=b, lock=first, side="bot", plan=plan))
            if p.get("company") and b["beam"] <= 7.0 and r.random() < p["company"]:
                # boats travelling in company arrive at the lock together
                while True:
                    mate = pick_boat()
                    if mate["beam"] <= 7.0 and mate is not b:
                        break
                push(t + timedelta(minutes=float(r.uniform(0.4, 2.5))), "arrive",
                     dict(boat=mate, lock=first, side="bot", plan=plan))
        nt = int(r.poisson(p["turn"] * w))
        for _ in range(nt):
            b = pick_boat()
            first = la.asset if r.random() < 0.5 else lb.asset
            push(day_time(d, 9.0, 17.5), "arrive", dict(boat=b, lock=first, side="bot", plan=("turn", first)))
        if summit == "Kelsby":
            occ = {4: 0.55, 5: 0.75, 6: 0.86, 7: 0.95, 8: 1.0, 9: 0.85, 10: 0.5}[d.month]
            k = int(round(p["hire_fleet"] * occ * float(r.uniform(0.85, 1.0))))
            if d.weekday() == 4:      # Friday returns, mostly up Kelsby Top Lock to the wharf
                start = datetime(d.year, d.month, d.day) + timedelta(hours=float(r.uniform(13.0, 14.5)))
                for i in range(k):
                    b = fleet[(i * 5 + d.toordinal()) % len(fleet)]
                    lk = p["ring_main"] if r.random() < 0.86 else other[p["ring_main"]]
                    start += timedelta(minutes=float(r.uniform(3.0, 16.0)))
                    push(start, "arrive", dict(boat=b, lock=lk, side="bot", plan=("home", None)))
            if d.weekday() == 5:      # Saturday departures, mostly down Wharf Lock to start the ring
                start = datetime(d.year, d.month, d.day) + timedelta(hours=float(r.uniform(14.0, 15.0)))
                for i in range(k):
                    b = fleet[(i * 3 + d.toordinal()) % len(fleet)]
                    lk = other[p["ring_main"]] if r.random() < 0.86 else p["ring_main"]
                    start += timedelta(minutes=float(r.uniform(4.0, 18.0)))
                    push(start, "arrive", dict(boat=b, lock=lk, side="top", plan=("away", None)))

    def try_start(lock, now):
        if lock.free_at is not None and now < lock.free_at:
            return
        if not lock.top and not lock.bot:
            return
        t0 = lock.allowed_start(now)
        if t0 > now:
            push(t0, "free", dict(lock=lock.asset))
            return
        for a, b in lock.closures:
            # a lock closed for works is left empty when it reopens
            if a not in lock.reset_done and lock.last_start is not None and lock.last_start < a and now >= b:
                lock.state = "L"
                lock.reset_done.add(a)
        # choose side: a chamber already set for a waiting boat first, otherwise the boat that has waited longest
        if lock.state == "H" and lock.top:
            side = "top"
        elif lock.state == "L" and lock.bot:
            side = "bot"
        elif lock.top and (not lock.bot or lock.top[0][0] <= lock.bot[0][0]):
            side = "top"
        else:
            side = "bot"
        q = lock.top if side == "top" else lock.bot
        opp = lock.bot if side == "top" else lock.top
        if (lock.broad and len(q) == 1 and not opp and q[0][1]["beam"] <= 7.0 and lock.hold_until is None
                and W.TRAFFIC[lock.s["summit"]].get("partner_wait")):
            lock.hold_until = now + timedelta(minutes=float(r.uniform(4.0, W.TRAFFIC[lock.s["summit"]]["partner_wait"])))
            push(lock.hold_until, "free", dict(lock=lock.asset))
            return
        if lock.hold_until is not None and now < lock.hold_until and len(q) == 1 and not opp:
            return
        lock.hold_until = None
        lock.last_start = now
        first = q.pop(0)
        group = [first]
        for j, item in enumerate(q):
            if can_pair(lock, first[1], item[1]):
                group.append(q.pop(j))
                break
        spec = lock.s
        turn = 0.0
        filled = False
        if side == "top" and lock.state == "L":
            turn = spec["fill"] + float(r.uniform(0.5, 1.5))
            filled = True
        elif side == "bot" and lock.state == "H":
            turn = spec["empty"] + float(r.uniform(0.5, 1.5))
        if side == "bot":
            filled = True
        t_in = now + timedelta(minutes=turn + float(r.uniform(0.8, 2.0)))
        recs = []
        if side == "bot":
            t = t_in
            for g in group:
                recs.append(t)
                t += timedelta(minutes=float(r.uniform(0.35, 1.1)))
            work = spec["fill"] + float(r.uniform(-0.6, 1.2))
            t_out = t + timedelta(minutes=work + float(r.uniform(1.0, 2.2)))
            lock.state = "H"
            lock.free_at = t_out + timedelta(minutes=float(r.uniform(0.4, 1.0)))
        else:
            work = spec["empty"] + float(r.uniform(-0.5, 1.0))
            t_out = t_in + timedelta(minutes=(len(group) - 1) * 0.6 + work + float(r.uniform(1.0, 2.2)))
            t = t_out
            for g in group:
                recs.append(t)
                t += timedelta(minutes=float(r.uniform(0.35, 1.1)))
            lock.state = "L"
            lock.free_at = t + timedelta(minutes=float(r.uniform(0.4, 1.0)))
        cyc = dict(lock=lock.asset, direction="up" if side == "bot" else "down", start=now, entry=t_in,
                   boats=[g[1] for g in group], times=recs, filled=filled, turned=turn > 0)
        lock.cycles.append(cyc)
        for g, tt in zip(group, recs):
            plan = g[2]
            if side == "bot":
                # now on the summit pound: carry on as planned
                kind, dest = plan
                if kind == "cross":
                    push(t_out + timedelta(minutes=float(r.uniform(*transit))), "arrive",
                         dict(boat=g[1], lock=dest, side="top", plan=("away", None)))
                elif kind == "moor":
                    nd = (t_out + timedelta(days=1)).date()
                    leave = datetime(nd.year, nd.month, nd.day) + timedelta(hours=float(r.uniform(8.4, 11.2)))
                    if leave.date() <= W.SEASON_END:
                        push(leave, "arrive", dict(boat=g[1], lock=dest, side="top", plan=("away", None)))
                elif kind == "turn":
                    push(t_out + timedelta(minutes=float(r.uniform(70, 230))), "arrive",
                         dict(boat=g[1], lock=dest, side="top", plan=("away", None)))
        push(lock.free_at, "free", dict(lock=lock.asset))

    while heap:
        t, _, kind, pl = heapq.heappop(heap)
        if t.date() > W.SEASON_END:
            continue
        lock = locks[pl["lock"]]
        if kind == "arrive":
            if lock.closed(t) or (lock.closures and any(a <= t < b for a, b in lock.closures)):
                # Steward's Lock shut: crews bound for it turn back or wait for the reopening
                if pl["side"] == "top":
                    alt = locks[other[lock.asset]]
                    alt.top.append((t, pl["boat"], pl["plan"]))
                    try_start(alt, t)
                continue
            (lock.top if pl["side"] == "top" else lock.bot).append((t, pl["boat"], pl["plan"]))
            try_start(lock, t)
        else:
            try_start(lock, t)
    for lk in (la, lb):
        for c in lk.cycles:
            assert W.SEASON_START <= c["start"].date() <= W.SEASON_END
    return {la.asset: la.cycles, lb.asset: lb.cycles}


def season_traffic():
    boats, fleet = boat_pool()
    cycles = {}
    for s in W.SUMMITS:
        cycles.update(simulate_summit(s, boats, fleet))
    return boats, fleet, cycles


# ------------------------------------------------------------------------------------------------ reservoirs
def release_schedule(name):
    """piecewise-constant release, (start_local, end_local, rate_Ml_per_day), changes on quarter hours."""
    r = rng("res:" + name)
    cfg = {"Upper Kelsby Reservoir": dict(rate=(2.6, 5.4), on=(2, 6), off=(1, 5), summer=1.2),
           "Lower Kelsby Reservoir": dict(rate=(8.2, 14.6), on=(3, 9), off=(0.25, 1.6), summer=1.15),
           "Coldmere Reservoir": dict(rate=(24.0, 38.0), on=(2, 7), off=(0, 0), summer=1.12),
           "Tilsey Reservoir": dict(rate=(4.2, 8.8), on=(3, 8), off=(1, 4), summer=1.18)}[name]
    t = datetime(2026, 3, 31, 14, 0) if name != "Coldmere Reservoir" else datetime(2026, 3, 30, 9, 0)
    if name == "Lower Kelsby Reservoir":
        t = datetime(2026, 3, 31, 15, 45)
    end = datetime(2026, 11, 2, 9, 0)
    out = []
    while t < end:
        dur = timedelta(hours=float(r.uniform(*cfg["on"])) * 24)
        dur = timedelta(minutes=15 * max(8, round(dur.total_seconds() / 900)))
        m = (t + dur / 2).month
        lift = cfg["summer"] if m in (6, 7, 8) else 1.0
        rate = round(float(r.uniform(*cfg["rate"])) * lift, 1)
        out.append((t, min(t + dur, end), rate))
        t = t + dur
        if cfg["off"][1] > 0:
            gap = timedelta(hours=float(r.uniform(*cfg["off"])) * 24)
            gap = timedelta(minutes=15 * max(4, round(gap.total_seconds() / 900)))
            t = t + gap
            if name == "Lower Kelsby Reservoir":
                # the keeper never opens the valve again inside the water day in which it was shut
                shut = out[-1][1]
                nine = datetime(shut.year, shut.month, shut.day, 9)
                if shut > nine:
                    nine += timedelta(days=1)
                if t <= nine:
                    t = nine + timedelta(minutes=15 * int(r.integers(2, 40)))
    return out


def volume_between(sched, a, b):
    v = 0.0
    for s, e, rate in sched:
        lo, hi = max(s, a), min(e, b)
        if hi > lo:
            v += rate * (hi - lo).total_seconds() / 86400.0
    return v


# ------------------------------------------------------------------------------------------------ abstraction
def last_working_day(y, m):
    d = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def daily_use(lic):
    r = rng("abs:" + lic["ref"])
    days = [date(2026, 3, 1) + timedelta(days=i) for i in range(260)]
    prof = []
    for d in days:
        m = d.month
        u = lic["use"]
        if u == "irrigation":
            base = {5: 0.6, 6: 1.4, 7: 2.1, 8: 1.8, 9: 0.6}.get(m, 0.0) * (1.0 if r.random() < 0.55 else 0.0)
        elif u == "greens":
            base = {3: 0.1, 4: 0.6, 5: 1.0, 6: 1.5, 7: 1.8, 8: 1.6, 9: 0.9, 10: 0.3}.get(m, 0.0)
        elif u == "marina":
            base = 0.7 + (0.6 if d.weekday() >= 4 else 0.0)
        elif u == "fishery":
            base = {3: 0.82, 4: 0.88, 5: 0.95, 6: 1.06, 7: 1.13, 8: 1.12, 9: 1.0, 10: 0.9}.get(m, 0.85)
        elif u == "process":
            base = 1.2 if d.weekday() < 5 else 0.15
        elif u == "lake":
            base = {5: 0.5, 6: 1.3, 7: 1.9, 8: 1.7, 9: 0.6}.get(m, 0.05)
        else:
            base = (1.3 if d.weekday() < 5 else 0.0) * {6: 1.3, 7: 1.5, 8: 1.4}.get(m, 0.9)
        prof.append(base * float(r.uniform(0.7, 1.3)))
    prof = np.array(prof)
    season = np.array([(date(2026, 3, 31) < d <= date(2026, 10, 30)) for d in days])
    scale = lic["scale"] / max(prof[season].sum(), 1e-9)
    return days, prof * scale


def meter_truth(lic):
    """cumulative take at every reading time, the exchange readings, and the dial readings."""
    r = rng("meter:" + lic["ref"])
    days, use = daily_use(lic)
    cum = np.concatenate([[0.0], np.cumsum(use)])

    def take_at(t):
        # use spread evenly through each day
        i = (t.date() - days[0]).days
        frac = (t - datetime(t.year, t.month, t.day)).total_seconds() / 86400.0
        return cum[i] + use[i] * frac
    reads = []
    for m in range(3, 11):
        d = last_working_day(2026, m)
        t = datetime(d.year, d.month, d.day) + timedelta(hours=float(r.uniform(9.0, 15.5)))
        t = t.replace(second=0, microsecond=0)
        reads.append(t)
    start_dial = float(r.uniform(12000, 88000)) if lic["digits"] == 6 else float(r.uniform(31000, 69000))
    serial_old = "%02d-%07d" % (r.integers(11, 48), r.integers(1000000, 9999999))
    serial_new = "%02d-%07d" % (r.integers(11, 48), r.integers(1000000, 9999999))
    ex = W.EXCHANGES.get(lic["ref"])
    rows = []
    mod = 10 ** lic["digits"]
    install = float(r.integers(3, 28)) if ex else None
    for t in reads:
        if ex and t > ex:
            dial = install + take_at(t) - take_at(ex)
            rows.append((serial_new, t, int(math.floor(dial)) % mod))
        else:
            dial = start_dial + take_at(t)
            rows.append((serial_old, t, int(math.floor(dial)) % mod))
    exch = None
    if ex:
        exch = dict(time=ex, old=serial_old, new=serial_new, removed=int(math.floor(start_dial + take_at(ex))) % mod,
                    installed=int(install))
    truth = take_at(reads[-1]) - take_at(reads[0])
    return dict(rows=rows, exchange=exch, serial_now=serial_new if ex else serial_old, truth=truth, reads=reads)
