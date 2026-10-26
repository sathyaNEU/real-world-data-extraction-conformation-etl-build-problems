"""Vennholt Energy's Kesmere field from 15 December 2025 to 12 January 2027: 180 tank batteries on twelve lease
operator routes, every site visit, every release event with its true start, the tank pressure alarm journal, daily
production and the tank vapour analyses, with the pneumatic devices and the vented wells the return's routine schedule
reports. This is the clean truth; pack.py cuts the operator's files from it and golden.py never reads it.

Times are hours since 15 December 2025 00:00 UTC (floats); pack.py writes them as each system writes them."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

SEED = 4877
TZ = ZoneInfo("America/Edmonton")
UTC = dt.timezone.utc
EPOCH = dt.datetime(2025, 12, 15, tzinfo=UTC)
FIRST = dt.date(2025, 12, 15)       # first local day the world runs
LAST = dt.date(2027, 1, 12)         # last local day of visits (the apps were pulled on 13 January 2027)
YEAR = 2026
MIGRATE = dt.date(2026, 7, 1)       # the check-in app replaced the route app on 1 July
PILOT = dt.date(2026, 6, 15)        # two routes ran the check-in app beside the route app from 15 June
PILOT_ROUTES = ("R03", "R09")
REDRAW_27 = dt.date(2027, 1, 4)     # the 2027 runs, in the battery register from its 8 January export
HOL = {dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3),
       dt.date(2026, 5, 18), dt.date(2026, 7, 1), dt.date(2026, 8, 3), dt.date(2026, 9, 7), dt.date(2026, 10, 12),
       dt.date(2026, 11, 11), dt.date(2026, 12, 25), dt.date(2026, 12, 26), dt.date(2027, 1, 1)}
BAN = (dt.date(2026, 4, 6), dt.date(2026, 5, 8))   # spring road bans: ban-road batteries on Mondays and Thursdays
CH4_DENSITY = 0.6785                                 # kg per m3 at 15 C and 101.325 kPa

ROUTES = ["R%02d" % i for i in range(1, 13)]
SAT_ROUTES = ("R03", "R08")
# release events: a share the departing visit starts (hatch only) and a per-hour rate between visits
P_VISIT = {"TH": 0.0080, "CP": 0.0, "PV": 0.0}
RATE = {"TH": 0.00070, "CP": 0.00008, "PV": 0.00012}
OIL = {"twice": 44.0, "daily": 13.5, "mwf": 4.2}     # m3 a day at the start of 2026
GOR = 4.15                                           # flash gas, m3 per m3 of oil, field mean
RENAMED = ("BT-0907", "BT-0907A", dt.date(2026, 8, 17))   # re-licensed after its tank replacement


def h_of(local):
    """local wall-clock datetime (naive) -> hours since the epoch"""
    return (local.replace(tzinfo=TZ).astimezone(UTC) - EPOCH).total_seconds() / 3600


def utc_of(h):
    return EPOCH + dt.timedelta(hours=float(h))


def local_of(h):
    return utc_of(h).astimezone(TZ).replace(tzinfo=None)


def day_of(h):
    """the local calendar day an instant falls in"""
    return local_of(h).date()


def days(a=FIRST, b=LAST):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


class World:
    def __init__(self, seed=SEED):
        self.rng = np.random.default_rng(seed)
        self.bats = []
        self.visits = {}
        self.events = []
        self.alarms = []
        self.outages = []
        self.prod = {}
        self.analyses = {}

    # ------------------------------------------------------------ batteries
    def batteries(self):
        r = self.rng
        n = 0
        for ri, route in enumerate(ROUTES):
            order = r.permutation(15)
            classes = ["twice"] * 3 + ["daily"] * 9 + ["mwf"] * 3
            r.shuffle(classes)
            for k in range(15):
                n += 1
                cls = classes[k]
                code = "BT-%02d%02d" % (ri + 1, k + 1)
                tel = r.random() < .40
                b = dict(code=code, route=route, cls=cls, sat=route in SAT_ROUTES, ban=r.random() < .25, tel=tel,
                         comb=r.random() < .65, slot=7.0 + order[k] * 0.55, pos=int(order[k]),
                         oil=float(OIL[cls] * r.lognormal(0, .33)), gor=float(GOR * r.lognormal(0, .22)),
                         ch4=float(np.clip(r.normal(64, 6), 48, 80)), lic="F%07d" % (4400000 + int(r.integers(1, 99999))),
                         tanks=int(r.choice([2, 3, 4], p=[.45, .4, .15])) if cls != "mwf" else int(r.choice([1, 2])))
                self.bats.append(b)
        self.by = {b["code"]: b for b in self.bats}
        self.history()

    def history(self):
        """battery codes carry the area a battery was built in; the lease operator runs have been redrawn since, so a
        few batteries ran on another area's run all through 2026 (each traded with the battery at the same place in
        that run's day). The leak survey crews still work area by area."""
        r = np.random.default_rng(SEED + 5)
        for b in self.bats:
            b["area"] = b["route"]
        pool = [rt for rt in ROUTES if rt not in PILOT_ROUTES]
        for _ in range(4):
            ra, rb = [pool[int(i)] for i in r.choice(len(pool), 2, replace=False)]
            pos = int(r.integers(0, 15))
            a = next(b for b in self.bats if b["route"] == ra and b["pos"] == pos)
            c = next(b for b in self.bats if b["route"] == rb and b["pos"] == pos)
            if a["code"] == RENAMED[0] or c["code"] == RENAMED[0] or a["area"] != ra or c["area"] != rb:
                continue
            a["route"], c["route"] = rb, ra

    # ------------------------------------------------------------ visits and events
    def schedule(self, b):
        """planned arrivals (local datetimes) and on-site minutes"""
        r = self.rng
        out = []
        for day in days():
            wd = day.weekday()
            if day in HOL or wd == 6 or (wd == 5 and not b["sat"]):
                continue
            if b["cls"] == "mwf" and wd not in (0, 2, 4):
                continue
            if b["ban"] and BAN[0] <= day <= BAN[1] and wd not in (0, 3):
                continue
            if r.random() < .02:
                continue
            base = dt.datetime.combine(day, dt.time()) + dt.timedelta(hours=b["slot"] + r.normal(0, .35))
            out.append((base, r.uniform(15, 40), "sched"))
            if b["cls"] == "twice" and wd < 5:
                out.append((base + dt.timedelta(hours=6.3 + r.normal(0, .35)), r.uniform(12, 26), "sched"))
        return out

    def run_battery(self, b):
        """walk a battery's visits in order: each window from one departure to the next arrival may hold an event,
        which the arrival finds and the visit closes before it leaves"""
        r = self.rng
        plan = self.schedule(b)
        vis = []
        i = 0
        prev_dep = None
        while i < len(plan):
            local, minutes, kind = plan[i]
            arr = h_of(local)
            if vis and arr <= vis[-1]["dep"] + .1:
                i += 1
                continue
            dep = arr + minutes / 60
            v = dict(arr=arr, dep=dep, kind=kind, user=None)
            if prev_dep is not None:
                self.window(b, prev_dep, v)
            vis.append(v)
            prev_dep = v["dep"]
            # a return later the same morning or afternoon (a hauler to meet, a pump to watch)
            if r.random() < .015:
                back = dict(arr=v["dep"] + r.uniform(1.0, 3.0), dep=None, kind="return", user=None)
                back["dep"] = back["arr"] + r.uniform(8, 22) / 60
                nxt = h_of(plan[i + 1][0]) if i + 1 < len(plan) else 1e9
                if back["dep"] + .5 < nxt:
                    self.window(b, prev_dep, back)
                    vis.append(back)
                    prev_dep = back["dep"]
            i += 1
        self.visits[b["code"]] = vis

    def window(self, b, dep, v):
        r = self.rng
        w = v["arr"] - dep
        starts = {}
        if r.random() < P_VISIT["TH"]:
            starts["TH"] = 0.0
        else:
            t = r.exponential(1 / RATE["TH"])
            if t < w:
                starts["TH"] = t
        if b["comb"]:
            t = r.exponential(1 / RATE["CP"])
            if t < w:
                starts["CP"] = t
        t = r.exponential(1 / RATE["PV"])
        if t < w:
            starts["PV"] = t
        if not starts:
            return
        kind = min(starts, key=lambda k: (starts[k], k))     # one event a window: the first to begin
        st = dep + starts[kind]
        found = v["arr"] + r.uniform(1, 9) / 60
        fix = {"TH": r.uniform(.05, .35), "CP": r.uniform(.1, .6),
               "PV": r.uniform(.2, 1.2) if r.random() > .08 else r.uniform(1.2, 3.0)}[kind]
        closed = found + fix
        v["dep"] = max(v["dep"], closed + r.uniform(4, 12) / 60)
        self.events.append(dict(bat=b["code"], kind=kind, start=st, dep=dep, arr=v["arr"], found=found,
                                closed=closed, visit_started=(kind == "TH" and starts["TH"] == 0.0),
                                tank=int(r.integers(1, b["tanks"] + 1))))

    # ------------------------------------------------------------ lease operators
    def users(self):
        regular = {rt: "lop%03d" % (110 + i * 7) for i, rt in enumerate(ROUTES)}
        relief = ["lop%03d" % k for k in (201, 214, 222, 237)]
        self.regular, self.relief = regular, relief
        for b in self.bats:
            for v in self.visits[b["code"]]:
                d = day_of(v["arr"])
                rt = run_on(b, d)
                off = (d.toordinal() + ROUTES.index(rt)) % 14 in (4, 11) or d.weekday() == 5
                v["user"] = relief[(d.toordinal() + ROUTES.index(rt)) % 4] if off else regular[rt]

    # ------------------------------------------------------------ alarm journal
    def alarm_journal(self):
        """tank pressure high alarms at the telemetered batteries (set at the relief valves' pressure): routine lifts
        that reseat, the lift that left a valve open (the journal shows nothing after it until the valve is closed),
        and radio outages the RTU rides through with its own buffer"""
        r = self.rng
        stuck = {}
        for e in self.events:
            if e["kind"] == "PV" and self.by[e["bat"]]["tel"]:
                stuck.setdefault(e["bat"], []).append((e["start"], e["closed"]))
        h_end = h_of(dt.datetime.combine(LAST, dt.time(23, 59)))
        for b in self.bats:
            if not b["tel"]:
                continue
            spans = sorted(stuck.get(b["code"], []))
            # radio outages: a repeater or a site's power now and then, and summer afternoon storms
            outs = []
            t = r.uniform(0, 400)
            while t < h_end:
                ln = r.uniform(.4, 7.5)
                outs.append((t, t + ln))
                t += ln + r.exponential(1500)
            for day in days(dt.date(2026, 6, 1), dt.date(2026, 8, 31)):
                if r.random() < .06:
                    a = h_of(dt.datetime.combine(day, dt.time()) + dt.timedelta(hours=float(r.uniform(13, 18))))
                    outs.append((a, a + r.uniform(.7, 5.0)))
            outs = sorted(o for o in outs if not any(o[0] - .5 <= s <= o[1] + .5 for s, c in spans))
            self.outages += [(b["code"], a, c) for a, c in outs]
            # stuck lifts: one alarm burst at the start
            for a, c in spans:
                self.lift(b, a, None, stuck=True)
            # routine lifts: afternoons, more in summer and at bigger producers
            lam = .55 * (b["oil"] / 14) ** .35
            for day in days():
                m = day.month
                season = 1.0 + .9 * np.cos((m - 7.2) / 12 * 2 * np.pi)
                for _ in range(r.poisson(lam * season)):
                    tl = dt.datetime.combine(day, dt.time()) + dt.timedelta(hours=float(np.clip(r.normal(15.0, 2.2), 9, 21)))
                    a = h_of(tl)
                    ln = r.uniform(2, 26) / 60
                    if any(s - .2 <= a <= c + .2 for s, c in spans):
                        continue        # a valve held open keeps the tank at atmospheric
                    self.lift(b, a, ln, stuck=False)
        self.alarms.sort(key=lambda x: (x["t"], x["bat"], x["seq"]))
        # an alarm the RTU raised during a radio outage reaches the host when the link returns
        out_by = {}
        for code, a, c in self.outages:
            out_by.setdefault(code, []).append((a, c))
        for x in self.alarms:
            x["rx"] = x["t"]
        for code, spans_ in out_by.items():
            mine = [x for x in self.alarms if x["bat"] == code and x["state"] != "ACK"]
            for a, c in spans_:
                held = sorted((x for x in mine if a <= x["t"] < c), key=lambda x: (x["t"], x["seq"]))
                t = c + r.uniform(1, 4) / 3600
                for x in held:              # the RTU's buffer, sent in order when the link returns
                    x["rx"] = t
                    t += r.uniform(.2, 1.5) / 3600
        # one transmitter is in one state at a time: a routine lift that would begin before the battery's previous
        # excursion returned to normal was never a second alarm, so it is dropped (after the buffer has drawn)
        by_lift = {}
        for x in self.alarms:
            by_lift.setdefault((x["bat"], x["lift"]), []).append(x)
        spans = {}
        for (code, a), xs in by_lift.items():
            ts = [x["t"] for x in xs if x["state"] != "ACK"]
            spans.setdefault(code, []).append((min(ts), max(ts), xs[0]["stuck"], a))
        drop = set()
        for code, ss in spans.items():
            kept = [(s, e) for s, e, stuck, a in ss if stuck]
            for s, e, stuck, a in sorted(ss):
                if stuck:
                    continue
                if any(s <= e2 + 1 / 60 and s2 <= e + 1 / 60 for s2, e2 in kept):
                    drop.add((code, a))
                else:
                    kept.append((s, e))
        self.alarms = [x for x in self.alarms if (x["bat"], x["lift"]) not in drop]

    def lift(self, b, a, ln, stuck):
        r = self.rng
        sp = 15.8 if b["tanks"] > 1 else 16.2       # relief set pressure, kPa (gauge, 1 psi = 6.9 kPa) plus margin
        seq = len(self.alarms)
        n_flutter = int(r.choice([0, 0, 0, 1, 2])) if stuck else int(r.choice([0, 0, 0, 0, 1]))
        t = a
        for k in range(n_flutter + 1):
            hold = r.uniform(4, 40) / 3600 if k < n_flutter else (r.uniform(.5, 4) / 60 if stuck else ln)
            self.alarms.append(dict(bat=b["code"], t=t, state="ALM", val=round(sp + r.uniform(.1, 1.4), 1), seq=seq,
                                    stuck=stuck, lift=a))
            self.alarms.append(dict(bat=b["code"], t=t + hold, state="RTN", val=round(sp - r.uniform(.2, 2.5), 1) if not
                                    stuck else round(r.uniform(.0, .6), 1), seq=seq + 1, stuck=stuck, lift=a))
            seq += 2
            t = t + hold + (r.uniform(5, 50) / 3600 if k < n_flutter else 0)
        self.alarms.append(dict(bat=b["code"], t=a + r.uniform(1, 95) / 60, state="ACK", val=None, seq=seq,
                                stuck=stuck, lift=a))

    # ------------------------------------------------------------ production and analyses
    def production(self):
        r = self.rng
        for b in self.bats:
            rows = []
            down = set()
            for _ in range(int(r.poisson(2.5))):
                d0 = FIRST + dt.timedelta(days=int(r.integers(0, (LAST - FIRST).days)))
                for k in range(int(r.integers(1, 4))):
                    down.add(d0 + dt.timedelta(days=k))
            for day in days(FIRST, dt.date(2026, 12, 31)):
                age = (day - dt.date(2026, 1, 1)).days / 365
                hrs = 24.0
                if day in down:
                    hrs = 0.0 if r.random() < .5 else round(float(r.uniform(2, 20)), 1)
                elif r.random() < .03:
                    hrs = round(float(r.uniform(14, 23.5)), 1)
                oil = b["oil"] * (1 - .08 * age) * r.normal(1, .06) * hrs / 24
                wcut = np.clip(r.normal(.55, .15), .1, .9)
                rows.append(dict(day=day, oil=max(0.0, round(float(oil), 1)), hours=hrs,
                                 water=round(float(oil * wcut / (1 - wcut)), 1),
                                 gas=round(float(oil * r.uniform(35, 140) / 1000), 2)))
            self.prod[b["code"]] = rows

    def vapour_analyses(self):
        r = self.rng
        for b in self.bats:
            s = []
            d = dt.date(2025, 6, 1) + dt.timedelta(days=int(r.integers(0, 160)))
            s.append(d)
            for lo, hi in ((dt.date(2026, 3, 2), dt.date(2026, 6, 26)), (dt.date(2026, 8, 3), dt.date(2026, 11, 20))):
                if r.random() < (.85 if lo.month == 3 else .5):
                    s.append(lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days))))
            self.analyses[b["code"]] = [dict(date=x, gor=round(float(b["gor"] * r.lognormal(0, .07)), 2),
                                             ch4=round(float(np.clip(b["ch4"] + r.normal(0, 1.6), 45, 82)), 2))
                                        for x in s]

    def build(self):
        self.batteries()
        for b in self.bats:
            self.run_battery(b)
        self.users()
        self.events.sort(key=lambda e: (e["found"], e["bat"]))
        self.alarm_journal()
        self.production()
        self.vapour_analyses()
        import asks
        asks.build(self)
        self.users()        # the runs were redrawn twice (asks.redraw): each visit goes to the run of its day
        return self


def build(seed=SEED):
    return World(seed).build()


def run_on(b, d):
    """the lease operator run a battery was on that day: its route to 30 June 2026, the run redrawn with the check-in
    app from 1 July, and the 2027 run from 4 January 2027"""
    if d >= REDRAW_27:
        return b.get("run27", b["route"])
    if d >= MIGRATE:
        return b.get("run_h2", b["route"])
    return b["route"]


# ---------------------------------------------------------------- the clean truth's own methane
def rate_table(w):
    """kg of methane an hour by battery and local day, from that day's oil and the analysis in effect"""
    out = {}
    for b in w.bats:
        an = sorted(w.analyses[b["code"]], key=lambda a: a["date"])
        for p in w.prod[b["code"]]:
            cur = [a for a in an if a["date"] <= p["day"]]
            a = cur[-1] if cur else an[0]
            out[(b["code"], p["day"])] = p["oil"] * a["gor"] * a["ch4"] / 100 * CH4_DENSITY / 24
    return out


def methane(rates, bat, a, c):
    """kg vented from instant a to instant c at the battery's hourly rate by local day"""
    tot = 0.0
    t = a
    while t < c - 1e-9:
        loc = local_of(t)
        nxt_mid = dt.datetime.combine(loc.date() + dt.timedelta(days=1), dt.time())
        t2 = min(c, h_of(nxt_mid))
        tot += rates.get((bat, loc.date()), 0.0) * (t2 - t)
        t = t2
    return tot
