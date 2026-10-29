"""task273 architecture 5: the clean truth.

Sixteen zone substations on the Saltgrass Coast, their customers, meters, controlled-load water heaters and rooftop
solar systems, the weather of spring 2026 and the half-hourly demand it produced, before any export is cut.
Everything the pack carries is rendered from this state by records.py; nothing here is read by a solver."""
from __future__ import annotations

import math
from datetime import date, datetime, timedelta

import numpy as np

import params as P

D0 = P.SPRING[0]
NDAY = (P.SPRING[1] - P.SPRING[0]).days + 1                       # 91
EXT0 = date(2026, 8, 10)                                          # reads reach back before spring
EXT1 = date(2026, 12, 12)
NEXT = (EXT1 - EXT0).days + 1


def offset_hours(utc):
    return 11 if utc >= P.DST_START_UTC else 10


def utc_of_local(d, hour):
    """UTC datetime of a local clock time (hours, may exceed 24) on local date d."""
    loc = datetime(d.year, d.month, d.day) + timedelta(hours=hour)
    off = 11 if loc >= datetime(2026, 10, 4, 2, 0) else 10
    return loc - timedelta(hours=off)


def eot_minutes(d):
    b = 2 * math.pi * (d.timetuple().tm_yday - 81) / 364.0
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def clear_kw_per_kw(d, aest_hour):
    """Clear-sky output per kW of inverter capacity at a standard-time hour on date d."""
    doy = d.timetuple().tm_yday
    noon = 11.93 - eot_minutes(d) / 60.0
    half = 6.25 + 0.62 * (doy - 244) / 90.0
    peak = 0.745 + 0.085 * (doy - 244) / 90.0
    x = (aest_hour - noon) / half
    if abs(x) >= 1:
        return 0.0
    return peak * math.cos(math.pi / 2 * x) ** 1.25


# Sundays of spring 2026: (clear-sky index at midday, maximum temperature); the 25 October Sunday is the one the
# coast's records produce as the lowest midday demand of the season
SUNDAY_WEATHER = {date(2026, 9, 6): (0.52, 17.0), date(2026, 9, 13): (0.93, 18.5), date(2026, 9, 20): (0.41, 15.5),
                  date(2026, 9, 27): (0.90, 21.0), date(2026, 10, 4): (0.71, 24.5), date(2026, 10, 11): (0.94, 28.5),
                  date(2026, 10, 18): (0.63, 19.5), date(2026, 10, 25): (0.995, 21.5), date(2026, 11, 1): (0.84, 25.0),
                  date(2026, 11, 8): (0.95, 33.5), date(2026, 11, 15): (0.48, 22.5), date(2026, 11, 22): (0.89, 31.5),
                  date(2026, 11, 29): (0.77, 27.0), date(2026, 10, 31): (0.83, 23.0),
                  date(2026, 10, 24): (0.88, 24.5)}


class World:
    def __init__(self, seed=P.SEED, outlook_kw=None, thresholds=None):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.codes = [s[0] for s in P.SUBS]
        self.sub = {s[0]: dict(code=s[0], name=s[1], n=s[2], pen=s[3], kw=s[4], u=s[5], com=s[6], scl=s[7], ts=s[8],
                               grow=s[9], role=s[10]) for s in P.SUBS}
        self._clock()
        self._weather()
        self._population()
        self._heaters()
        self._solar()
        self._spine()
        self._sample()
        self._clear_ask_edges()
        self.outlook_kw = outlook_kw or self._outlook()
        self.thresholds = thresholds

    # ------------------------------------------------------------------------------------------ the clock
    def _clock(self):
        start = datetime(2026, 8, 31, 14, 30)          # interval ending 00:30 AEST on 1 September
        end = datetime(2026, 11, 30, 13, 0)            # interval ending 00:00 AEDT on 1 December
        t, ends = start, []
        while t <= end:
            ends.append(t)
            t += timedelta(minutes=30)
        self.utc_end = ends
        self.K = len(ends)
        loc_start, day, hour, aest = [], [], [], []
        for u in ends:
            off = offset_hours(u - timedelta(minutes=30))
            ls = u - timedelta(minutes=30) + timedelta(hours=off)
            loc_start.append(ls)
            day.append((ls.date() - D0).days)
            hour.append(ls.hour + ls.minute / 60.0)
            aest.append((u - timedelta(minutes=15) + timedelta(hours=10)))
        self.loc_start = loc_start
        self.kday = np.array(day)
        self.khour = np.array(hour)                     # local clock hour at interval start
        self.kmid_aest = np.array([a.hour + a.minute / 60.0 for a in aest])
        self.kdate = [D0 + timedelta(days=int(d)) for d in day]
        wd = np.array([d.weekday() for d in self.kdate])
        self.kdow = wd                                  # 6 is Sunday

    # ------------------------------------------------------------------------------------------ weather
    def _weather(self):
        r = self.rng
        clear, tmax = np.zeros(NDAY), np.zeros(NDAY)
        for i in range(NDAY):
            d = D0 + timedelta(days=i)
            if d in SUNDAY_WEATHER:
                clear[i], tmax[i] = SUNDAY_WEATHER[d]
            else:
                clear[i] = float(np.clip(r.beta(2.6, 1.15), 0.18, 0.99))
                tmax[i] = float(np.clip(17.0 + 9.5 * i / NDAY + r.normal(0, 3.4), 13.0, 35.5))
        self.clear, self.tmax = clear, tmax
        # half-hourly cloud factor per day: smooth, deeper and more variable on broken days
        cf = np.ones((NDAY, 48))
        for i in range(NDAY):
            sig = 0.01 if clear[i] > 0.985 else 0.05 + 0.32 * (1 - clear[i])
            e = np.zeros(48)
            for s in range(1, 48):
                e[s] = 0.78 * e[s - 1] + r.normal(0, sig)
            cf[i] = np.clip(clear[i] * (1 + e), 0.04, 1.015)
        self.cloud = cf

    def pv_per_kw(self, i, aest_mid):
        d = D0 + timedelta(days=int(i))
        s = int(min(47, max(0, math.floor(aest_mid * 2))))
        return clear_kw_per_kw(d, aest_mid) * self.cloud[i, s]

    # ------------------------------------------------------------------------------------------ customers
    def _population(self):
        r = self.rng
        blocks = {}
        pool = list(range(4301, 4399))
        r.shuffle(pool)
        for j, c in enumerate(self.codes):
            blocks[c] = pool[3 * j: 3 * j + 3]
        self.new_block = pool[60]
        used = set()

        def new_nmi(block):
            while True:
                v = "%04d%06d" % (block, int(r.integers(0, 1000000)))
                if v not in used:
                    used.add(v)
                    return v
        self._new_nmi = new_nmi
        feeders = {}
        for c in self.codes:
            nf = int(r.integers(6, 12))
            nums = sorted(r.choice(np.arange(1, 19), size=nf, replace=False).tolist())
            feeders[c] = ["%s-%02d" % (c, k) for k in nums]
        # feeders that came over in the 2025 reconfiguration keep a renumbered code in the new substation
        self.moved_feeders = {}
        for frm, to, nfeed, share in P.RECONFIG_MOVES:
            taken = feeders[to][-nfeed:]
            self.moved_feeders[to] = (frm, taken, share)
        self.feeders = feeders
        cust = []
        for c in self.codes:
            s = self.sub[c]
            fl = feeders[c]
            moved = self.moved_feeders.get(c)
            for k in range(s["n"]):
                if moved and r.random() < moved[2]:
                    fd = moved[1][int(r.integers(0, len(moved[1])))]
                else:
                    pool_f = [f for f in fl if not (moved and f in moved[1])]
                    fd = pool_f[int(r.integers(0, len(pool_f)))]
                cust.append(dict(nmi=new_nmi(blocks[c][int(r.integers(0, 3))]), sub=c, feeder=fd,
                                 old_sub=(moved[0] if moved and fd in moved[1] else c)))
        self.cust = cust
        for cu in cust:
            s = self.sub[cu["sub"]]
            cu["cl"] = bool(r.random() < s["scl"])
            cu["solar"] = bool(r.random() < s["pen"])
            cu["three"] = bool(r.random() < 0.03)
        serials = set()

        def serial(maker, year):
            while True:
                if maker == "Hexwell":
                    v = "HXW%07d" % int(r.integers(0, 10 ** 7))
                elif maker == "Norvane":
                    v = "NV%02d%06d" % (year % 100, int(r.integers(0, 10 ** 6)))
                else:
                    v = "CM%08d" % int(r.integers(0, 10 ** 8))
                if v not in serials:
                    serials.add(v)
                    return v
        self._serial = serial
        self.models = {m[0]: dict(code=m[0], maker=m[1], desc=m[2], data=m[3], phases=m[4], regs=m[5], cls=m[6],
                                  y0=m[7], y1=m[8]) for m in P.MODELS}

    def _fit(self, code, lo=None, hi=None):
        r = self.rng
        m = self.models[code]
        y0 = max(m["y0"], lo or m["y0"])
        y1 = min(m["y1"], hi or m["y1"])
        if y1 < y0:
            y1 = y0
        y = int(r.integers(y0, y1 + 1))
        d = date(y, 1, 1) + timedelta(days=int(r.integers(0, 365)))
        if d > date(2026, 8, 20):
            d = date(2026, 8, 20) - timedelta(days=int(r.integers(0, 200)))
        return d

    # ------------------------------------------------------------------------------------------ heaters and meters
    def _heaters(self):
        r = self.rng
        self.meters = []          # dicts: nmi, sub, feeder, serial, model, installed, removed
        self.heaters = []
        for c in self.codes:
            s = self.sub[c]
            gp = r.dirichlet([26, 24, 23, 22, 21])
            cl_idx = [i for i, cu in enumerate(self.cust) if cu["sub"] == c and cu["cl"]]
            nts = int(round(s["ts"] * len(cl_idx)))
            ts_set = set(r.choice(cl_idx, size=nts, replace=False).tolist())
            for i in cl_idx:
                cu = self.cust[i]
                ts = i in ts_set
                cu["ts"] = ts
                if ts:
                    if cu["solar"]:
                        model = "NV-5100T"
                    else:
                        model = ["HX-A27T", "CM-200T", "NV-5100T"][int(r.choice(3, p=[0.38, 0.27, 0.35]))]
                else:
                    if cu["solar"]:
                        model = ["NV-5300R", "CM-610R", "HX-I440R"][int(r.choice(3, p=[0.36, 0.34, 0.30]))]
                    else:
                        model = ["HX-A31R", "CM-240R", "NV-5300R", "CM-610R", "HX-I440R"][
                            int(r.choice(5, p=[0.27, 0.21, 0.19, 0.17, 0.16]))]
                cu["model"] = model
                g = int(r.choice(5, p=gp))
                kw = float(r.choice(P.ELEMENT_KW, p=P.ELEMENT_P))
                sc = {1.8: 0.72, 2.4: 0.86, 3.6: 1.0, 4.8: 1.18}[kw]
                e = float(np.clip(r.gamma(6.2, 1.38) * sc, 2.2, 17.5))
                litres = {1.8: 125, 2.4: 160, 3.6: 250, 4.8: 315}[kw]
                if r.random() < 0.25:
                    litres = {125: 80, 160: 125, 250: 315, 315: 400}[litres]
                since = date(int(r.integers(1996, 2026)), 1, 1) + timedelta(days=int(r.integers(0, 365)))
                if since > date(2026, 7, 31):
                    since = date(2026, 7, 31) - timedelta(days=int(r.integers(0, 300)))
                self.heaters.append(dict(idx=i, nmi=cu["nmi"], sub=c, group=g, kw=kw, e=e, litres=litres,
                                         since=since, ts=ts))
        self._meter_histories()

    def _meter_histories(self):
        r = self.rng
        cl_models_ts_old = ["HX-A27T", "CM-200T"]
        for cu in self.cust:
            hist = []
            if cu["cl"]:
                cur = cu["model"]
                inst = self._fit(cur)
                # some current meters replaced an older one before spring 2026
                if r.random() < 0.30 and inst.year >= 2004:
                    if self.models[cur]["cls"] == "R" and self.models[cur]["data"] == "interval" and r.random() < 0.22:
                        old = cl_models_ts_old[int(r.integers(0, 2))]
                    elif self.models[cur]["cls"] == "R":
                        old = ["HX-A31R", "CM-240R"][int(r.integers(0, 2))]
                    else:
                        old = cl_models_ts_old[int(r.integers(0, 2))]
                    oinst = self._fit(old, hi=inst.year - 1)
                    if oinst >= inst:
                        oinst = inst - timedelta(days=int(r.integers(900, 4000)))
                    hist.append([old, oinst, inst])
                hist.append([cur, inst, None])
            else:
                if cu["three"]:
                    cur = "CM-830"
                elif cu["solar"]:
                    cur = ["NV-4100", "CM-600"][int(r.integers(0, 2))]
                else:
                    cur = ["HX-A10", "NV-4100", "CM-600"][int(r.choice(3, p=[0.38, 0.30, 0.32]))]
                inst = self._fit(cur)
                if r.random() < 0.28 and inst.year >= 2009 and cur != "HX-A10":
                    oinst = self._fit("HX-A10", hi=inst.year - 1)
                    if oinst >= inst:
                        oinst = inst - timedelta(days=int(r.integers(900, 4000)))
                    hist.append(["HX-A10", oinst, inst])
                hist.append([cur, inst, None])
            cu["hist"] = hist
        # a few like-for-like exchanges during spring 2026 on interval meters with a receiver (a failed
        # communications module), and some after it
        for c in self.codes:
            cands = [cu for cu in self.cust if cu["sub"] == c and cu["cl"] and not cu["ts"]
                     and self.models[cu["model"]]["data"] == "interval"]
            k = int(r.integers(2, 6))
            for cu in r.choice(cands, size=k, replace=False):
                d = D0 + timedelta(days=int(r.integers(12, 80)))
                old = cu["hist"][-1]
                old[2] = d
                cu["hist"].append([old[0], d, None])
        for cu in self.cust:
            for mdl, a, b in cu["hist"]:
                self.meters.append(dict(nmi=cu["nmi"], sub=cu["sub"], feeder=cu["feeder"],
                                        serial=self._serial(self.models[mdl]["maker"], a.year), model=mdl,
                                        installed=a, removed=b))

    # ------------------------------------------------------------------------------------------ rooftop solar
    def _solar(self):
        """Each solar customer's connection history: one chain per AC connection, each link an application."""
        r = self.rng
        years = np.arange(2009, 2027)
        wy = np.array([2, 4, 6, 6, 5, 5, 5, 6, 7, 9, 10, 11, 11, 10, 9, 9, 9, 7], float)
        wy /= wy.sum()
        self.chains = []
        self.abolished = []

        def size_for(y):
            if y <= 2012:
                return float(r.choice([1.5, 2.0, 2.5, 3.0, 3.0, 4.0]))
            if y <= 2017:
                return float(r.choice([3.0, 4.0, 4.6, 5.0, 5.0, 5.0]))
            if y <= 2022:
                return float(r.choice([5.0, 5.0, 6.0, 8.2, 5.0, 10.0, 6.0]))
            return float(r.choice([5.0, 6.0, 8.2, 10.0, 10.0, 8.0, 6.0, 13.2]))

        def chain_for(cu, y=None, after=None):
            if y is None:
                y = int(r.choice(years, p=wy))
            d = date(y, 1, 1) + timedelta(days=int(r.integers(0, 365)))
            if after and d <= after:
                d = after + timedelta(days=int(r.integers(20, 200)))
            if d > date(2026, 12, 4):
                d = date(2026, 12, 4) - timedelta(days=int(r.integers(0, 40)))
            inv = size_for(d.year)
            pan = round(inv * float(r.uniform(1.04, 1.36)), 2)
            links = [dict(kind="New connection", work=None, inv=inv, pan=pan, approved=d,
                          commissioned=d + timedelta(days=int(r.integers(9, 75))), status="Commissioned",
                          inverter=True)]
            # later alterations
            last = links[-1]["commissioned"]
            age_years = (date(2026, 10, 25) - last).days / 365.25
            n_alt = 0
            if age_years > 1.5:
                p_alt = min(0.42, 0.028 * age_years + 0.05)
                while r.random() < p_alt and n_alt < 3:
                    n_alt += 1
                    p_alt *= 0.35
            for _ in range(n_alt):
                a = last + timedelta(days=int(r.integers(200, 2600)))
                if a > date(2026, 12, 3):
                    break
                work = str(r.choice(["Inverter replacement", "Additional panels", "Inverter and panel upgrade",
                                     "Export limit change"], p=[0.33, 0.24, 0.25, 0.18]))
                prev = links[-1]
                inv, pan = prev["inv"], prev["pan"]
                if work == "Inverter replacement":
                    inv = max(inv, size_for(a.year)) if r.random() < 0.6 else inv
                elif work == "Additional panels":
                    pan = round(pan + float(r.choice([1.32, 1.98, 2.64, 3.3])), 2)
                elif work == "Inverter and panel upgrade":
                    inv = max(inv + 1.0, size_for(a.year))
                    pan = round(inv * float(r.uniform(1.08, 1.33)), 2)
                links.append(dict(kind="Alteration", work=work, inv=inv, pan=pan, approved=a,
                                  commissioned=a + timedelta(days=int(r.integers(7, 60))), status="Commissioned",
                                  inverter=work in ("Inverter replacement", "Inverter and panel upgrade")))
                last = links[-1]["commissioned"]
            return links

        for cu in self.cust:
            if not cu["solar"]:
                continue
            nch = 2 if r.random() < 0.028 else 1
            first = None
            for k in range(nch):
                links = chain_for(cu, after=first)
                first = links[0]["approved"]
                self.chains.append(dict(nmi=cu["nmi"], cust=cu, links=links, abolished=None))
        # knock-down rebuilds: a solar customer's old site connection abolished, the new house on a new NMI
        for c in self.codes:
            cands = [ch for ch in self.chains if ch["cust"]["sub"] == c and not ch["cust"]["cl"]
                     and ch["cust"]["old_sub"] == c and ch["links"][0]["commissioned"] < date(2022, 6, 1)]
            order = list(r.permutation(len(cands)))
            k_late, k_early = int(r.integers(2, 5)), int(r.integers(4, 9))
            for j in order:
                if k_late == 0 and k_early == 0:
                    break
                ch = cands[j]
                cu = ch["cust"]
                if any(x["nmi"] == cu["nmi"] and x is not ch for x in self.chains):
                    continue
                late = k_late > 0
                if ch["links"][-1]["inv"] < (5.0 if late else 3.0):
                    continue
                x = (date(2026, 10, 29) + timedelta(days=int(r.integers(0, 32)))) if late else \
                    (date(2023, 2, 1) + timedelta(days=int(r.integers(0, 1300))))
                if x > date(2026, 9, 25) and not late:
                    x = date(2026, 9, 25) - timedelta(days=int(r.integers(0, 120)))
                if ch["links"][-1]["commissioned"] >= x:
                    continue
                if late:
                    k_late -= 1
                else:
                    k_early -= 1
                ch["abolished"] = x
                for m in self.meters:
                    if m["nmi"] == cu["nmi"] and m["removed"] is None:
                        m["removed"] = x
                cu["abolished"] = x
                build = x + timedelta(days=int(r.integers(140, 330)))
                if build > P.METER_REG_PULL - timedelta(days=10):
                    self.abolished.append((cu["nmi"], None, x))
                    continue
                newn = self._new_nmi(self.new_block)
                nc = dict(nmi=newn, sub=cu["sub"], feeder=cu["feeder"], old_sub=cu["old_sub"], cl=False, solar=True,
                          three=False, rebuilt=True, hist=[["CM-600", build, None]])
                self.cust.append(nc)
                self.meters.append(dict(nmi=newn, sub=nc["sub"], feeder=nc["feeder"],
                                        serial=self._serial("Calder Metering", build.year), model="CM-600",
                                        installed=build, removed=None))
                self.abolished.append((cu["nmi"], newn, x))
                if build < date(2026, 11, 20):
                    links = chain_for(nc, y=build.year, after=build)
                    links = links[:1]
                    if links[0]["approved"] < build:
                        links[0]["approved"] = build + timedelta(days=int(r.integers(5, 40)))
                        links[0]["commissioned"] = links[0]["approved"] + timedelta(days=int(r.integers(9, 60)))
                    self.chains.append(dict(nmi=newn, cust=nc, links=links, abolished=None))
        # after the backstop started, panel additions and export-limit changes on older systems (the inverter stays)
        for c in self.codes:
            cands = [ch for ch in self.chains if ch["cust"]["sub"] == c and not ch["abolished"]
                     and not ch["cust"].get("rebuilt") and ch["links"][-1]["commissioned"] < date(2025, 5, 1)
                     and ch["links"][-1]["inv"] >= 3.0]
            for j in r.choice(len(cands), size=int(r.integers(4, 10)), replace=False):
                ch = cands[int(j)]
                prev = ch["links"][-1]
                a = date(2025, 8, 1) + timedelta(days=int(r.integers(0, 420)))
                work = str(r.choice(["Additional panels", "Export limit change"], p=[0.55, 0.45]))
                pan = round(prev["pan"] + float(r.choice([1.32, 1.98, 2.64])), 2) if work == "Additional panels" \
                    else prev["pan"]
                ch["links"].append(dict(kind="Alteration", work=work, inv=prev["inv"], pan=pan, approved=a,
                                        commissioned=min(a + timedelta(days=int(r.integers(7, 50))),
                                                         date(2026, 10, 20)), status="Commissioned",
                                        inverter=False))
        makers = (("SLX", 10), ("KVT", 8), ("HYD", 9), ("AUR", 10), ("TSN", 8))
        seen = set()

        def inv_serial():
            while True:
                pre, n = makers[int(r.choice(5, p=[0.28, 0.22, 0.2, 0.17, 0.13]))]
                v = pre + "".join(str(int(x)) for x in r.integers(0, 10, n))
                if v not in seen:
                    seen.add(v)
                    return v
        for ch in self.chains:
            cur = None
            for ln in ch["links"]:
                if ln["kind"] == "New connection" or ln["inverter"]:
                    cur = inv_serial()
                ln["serial"] = cur
        # applications that never became links: duplicates withdrawn, upgrades lapsed, approvals not yet built,
        # and links commissioned after the reference day are already in the chains
        self.ghosts = []
        for ch in self.chains:
            if r.random() < 0.045:
                base = ch["links"][int(r.integers(0, len(ch["links"])))]
                kind = str(r.choice(["dup", "lapsed", "pending"], p=[0.45, 0.35, 0.20]))
                if kind == "dup":
                    g = dict(base)
                    g.update(status="Withdrawn", commissioned=None,
                             approved=base["approved"] + timedelta(days=int(r.integers(0, 4))))
                    if base["approved"] > date(2026, 12, 4):
                        continue
                elif kind == "lapsed":
                    a = ch["links"][-1]["approved"] + timedelta(days=int(r.integers(60, 900)))
                    if a > date(2026, 6, 30):
                        a = date(2026, 6, 30) - timedelta(days=int(r.integers(0, 90)))
                    prev = ch["links"][-1]
                    if a <= prev["commissioned"]:
                        continue
                    g = dict(kind="Alteration", work="Inverter and panel upgrade", inv=prev["inv"] + 3.0,
                             pan=round((prev["inv"] + 3.0) * 1.25, 2), approved=a, commissioned=None,
                             status="Lapsed", inverter=True, serial=None)
                else:
                    a = date(2026, 9, 20) + timedelta(days=int(r.integers(0, 75)))
                    prev = ch["links"][-1]
                    if a <= prev["approved"]:
                        continue
                    g = dict(kind="Alteration", work=str(r.choice(["Inverter replacement", "Additional panels"])),
                             inv=prev["inv"] + float(r.choice([0.0, 2.0, 3.0])), pan=round(prev["pan"] + 2.64, 2),
                             approved=a, commissioned=None, status="Approved", inverter=True, serial=None)
                self.ghosts.append(dict(chain=ch, link=g))

    # ------------------------------------------------------------------------------------------ truth at a date
    def in_service(self, ch, on):
        """(inverter kW, inverter install date) of a chain on a date, from the physical history."""
        if ch["abolished"] and ch["abolished"] <= on:
            return 0.0, None
        kw, inst, ser = 0.0, None, None
        for ln in ch["links"]:
            if ln["status"] == "Commissioned" and ln["commissioned"] <= on:
                kw = ln["inv"]
                if ln["serial"] != ser:
                    ser, inst = ln["serial"], ln["commissioned"]
        return kw, inst

    def solar_truth(self, on):
        cap = {c: 0.0 for c in self.codes}
        bs = {c: 0.0 for c in self.codes}
        for ch in self.chains:
            cu = ch["cust"]
            if cu.get("rebuilt") and ch["links"][0]["commissioned"] > on:
                continue
            kw, inst = self.in_service(ch, on)
            cap[cu["sub"]] += kw
            if inst and inst >= P.BACKSTOP_FROM:
                bs[cu["sub"]] += kw
        return cap, bs

    def _clear_ask_edges(self):
        """Keep every substation's in-service and backstop totals at least 0.5 kW from a printed hundredth of a MW: a
        tie on the boundary would print differently under different rounding rules. One in-service system per
        substation is recorded at its true nameplate (a 0.1 kW larger inverter) until both totals clear."""
        for _ in range(12):
            cap, bs = self.solar_truth(P.REF_DAY)
            moved = False
            for c in self.codes:
                for tot, capable in ((cap[c], False), (bs[c], True)):
                    rem = tot % 10.0
                    if abs(rem - 5.0) < 0.5:
                        for ch in self.chains:
                            if ch["cust"]["sub"] != c:
                                continue
                            kw, inst = self.in_service(ch, P.REF_DAY)
                            ok_cap = inst is not None and inst >= P.BACKSTOP_FROM
                            if kw > 0 and ok_cap == capable and len(ch["links"]) == 1:
                                ch["links"][0]["inv"] = round(ch["links"][0]["inv"] + 0.9, 2)
                                moved = True
                                break
                        break
            if not moved:
                return

    # ------------------------------------------------------------------------------------------ heater energy
    def heater_days(self):
        """Per heater, the energy taken each day of the extended reads window (kWh)."""
        r = np.random.default_rng(self.seed + 17)
        days = np.arange(NEXT)
        dates = [EXT0 + timedelta(days=int(i)) for i in days]
        season = np.array([1.10 - 0.19 * ((dd - date(2026, 8, 10)).days / 124.0) for dd in dates])
        wk = np.array([1.06 if dd.weekday() >= 5 else 0.98 for dd in dates])
        E = np.array([h["e"] for h in self.heaters])
        noise = r.normal(0, 0.11, size=(len(self.heaters), NEXT))
        self.hday = np.clip(E[:, None] * season[None, :] * wk[None, :] * (1 + noise), 0.3, 24.0)
        self.hday_dates = dates
        return self.hday

    # ------------------------------------------------------------------------------------------ the spine
    def _base_profile(self, hour, dow, tmax, com):
        """Per-customer kW of everything but controlled load and solar, at a local clock hour."""
        h = hour + 0.25
        sunday = dow == 6
        sat = dow == 5
        res = (0.40 + 0.38 * math.exp(-((h - (8.9 if sunday else 7.6)) / 1.25) ** 2)
               + 0.62 * math.exp(-((h - 18.9) / 1.9) ** 2) + 0.12 * math.exp(-((h - 13.0) / 3.0) ** 2) * (1.6 if sunday else 1.0))
        if h < 5.5:
            res -= 0.06 * (5.5 - h) / 5.5
        heat = max(0.0, 15.5 - tmax) * 0.045 * (math.exp(-((h - 7.5) / 1.6) ** 2) + math.exp(-((h - 19.5) / 2.2) ** 2))
        cool = max(0.0, tmax - 25.0) * 0.07 * math.exp(-((h - 16.0) / 3.4) ** 2)
        if sunday:
            cm = 0.45 + 0.35 * math.exp(-((h - 12.5) / 3.2) ** 2)
        elif sat:
            cm = 0.45 + 0.95 * math.exp(-((h - 12.0) / 3.5) ** 2)
        else:
            cm = 0.42 + 1.75 * (1 / (1 + math.exp(-(h - 7.8) * 2.2))) * (1 / (1 + math.exp((h - 17.8) * 1.8)))
        return (1 - com) * (res + heat + cool) + com * cm * 2.2

    def _spine(self):
        r = np.random.default_rng(self.seed + 29)
        self.heater_days()
        K = self.K
        # each substation's overnight controlled load in UTC intervals
        ends = np.array([(u - self.utc_end[0]).total_seconds() / 3600.0 for u in self.utc_end])
        t1 = ends
        t0 = ends - 0.5
        cl = {c: np.zeros(K) for c in self.codes}
        hk = np.array([h["kw"] for h in self.heaters])
        hg = np.array([h["group"] for h in self.heaters])
        hs = np.array([self.codes.index(h["sub"]) for h in self.heaters])
        first_utc = self.utc_end[0]
        for n in range(-1, NDAY):
            d = D0 + timedelta(days=n)
            di = (d - EXT0).days
            en = self.hday[:, di]
            rel = np.array([(utc_of_local(d, P.NIGHT_RELEASE[g]) - first_utc).total_seconds() / 3600.0 for g in range(5)])
            st = rel[hg]
            dur = np.minimum(en / hk, P.NIGHT_OFF - P.NIGHT_RELEASE[0])
            fn = st + dur
            lo = np.searchsorted(t1, st.min())
            hi = np.searchsorted(t0, fn.max())
            for k in range(max(0, lo), min(K, hi + 1)):
                ov = np.clip(np.minimum(fn, t1[k]) - np.maximum(st, t0[k]), 0, 0.5) / 0.5
                if ov.any():
                    v = np.bincount(hs, weights=hk * ov, minlength=len(self.codes))
                    for j, c in enumerate(self.codes):
                        cl[c][k] += v[j] / 1000.0
        self.cl_night = cl
        # solar capacity in service each day (truth) and the spine
        caps = {c: np.zeros(NDAY) for c in self.codes}
        for i in range(NDAY):
            cp, _ = self.solar_truth(D0 + timedelta(days=i)) if i % 7 == 0 or i == NDAY - 1 or (D0 + timedelta(days=i)) == P.REF_DAY else (None, None)
            if cp is not None:
                for c in self.codes:
                    caps[c][i] = cp[c]
        for c in self.codes:
            a = caps[c]
            idx = [i for i in range(NDAY) if a[i] > 0]
            caps[c] = np.interp(np.arange(NDAY), idx, a[idx])
        self.caps = caps
        pvk = np.array([self.pv_per_kw(self.kday[k], self.kmid_aest[k]) for k in range(K)])
        self.pvk_true = pvk
        mw = {}
        for j, c in enumerate(self.codes):
            s = self.sub[c]
            loc = r.normal(0, 0.012, NDAY)
            cloud_loc = np.ones(K)
            e = 0.0
            for k in range(K):
                e = 0.7 * e + r.normal(0, 0.04 * (1 - self.clear[self.kday[k]]) + 0.002)
                cloud_loc[k] = 1 + e
            base = np.array([self._base_profile(self.khour[k], self.kdow[k], self.tmax[self.kday[k]], s["com"])
                             for k in range(K)]) * s["n"] / 1000.0
            scale = s["u"] / (self._base_profile(12.0, 6, 21.5, s["com"]))
            base *= scale
            noise = np.zeros(K)
            e = 0.0
            for k in range(K):
                e = 0.85 * e + r.normal(0, 0.006)
                noise[k] = e
            pv = caps[c][self.kday] / 1000.0 * pvk * (1 + loc[self.kday]) * np.clip(cloud_loc, 0.6, 1.25)
            mw[c] = base * (1 + noise) + cl[c] - pv
        self.mw = mw

    # ------------------------------------------------------------------------------------------ the sample
    def _sample(self):
        r = np.random.default_rng(self.seed + 41)
        self.sample = np.round(np.clip(self.pvk_true * (1 + r.normal(0, 0.006, self.K)), 0, None), 3)

    # ------------------------------------------------------------------------------------------ the outlook
    def _outlook(self):
        cap, _ = self.solar_truth(P.REF_DAY)
        return {c: int(round(cap[c] * self.sub[c]["grow"] / 10.0)) * 10 for c in self.codes}


# ---------------------------------------------------------------------------------------------- reads and the forecast
def cl_register(models, model):
    return models[model]["regs"][1]


def build_reads(w):
    """The consumption summary: one row per serial per register for every controlled-load customer, over the
    reads that fall in spring 2026 (interval meters to the day, accumulation meters between their two reads)."""
    r = np.random.default_rng(w.seed + 53)
    hmap = {h["nmi"]: k for k, h in enumerate(w.heaters)}
    by_nmi = {}
    for m in w.meters:
        by_nmi.setdefault(m["nmi"], []).append(m)
    rows = []
    for cu in w.cust:
        if not cu.get("cl"):
            continue
        k = hmap[cu["nmi"]]
        ms = [m for m in by_nmi[cu["nmi"]] if (m["removed"] is None or m["removed"] > P.SPRING[0])
              and m["installed"] <= P.SPRING[1]]
        ms.sort(key=lambda m: m["installed"])
        acc = w.models[ms[-1]["model"]]["data"] == "accumulation"
        if acc:
            a = P.SPRING[0] - timedelta(days=int(r.integers(2, 12)))
            b = P.SPRING[1] - timedelta(days=int(r.integers(3, 12)))
        else:
            a, b = P.SPRING[0], P.SPRING[1]
        for j, m in enumerate(ms):
            fa = max(a, m["installed"])
            fb = b if m["removed"] is None else min(b, m["removed"] - timedelta(days=1))
            days = (fb - fa).days + 1
            i0, i1 = (fa - EXT0).days, (fb - EXT0).days
            mdl = w.models[m["model"]]
            cl_kwh = float(w.hday[k, i0:i1 + 1].sum())
            gen_kwh = days * w.sub[cu["sub"]]["u"] * 24 * 0.78 * float(r.uniform(0.55, 1.45))
            exp_kwh = None
            if cu["solar"] and mdl["regs"][2]:
                exp_kwh = days * float(r.uniform(9.0, 26.0))
            dec = 0 if mdl["data"] == "accumulation" else 3
            for reg, v in zip(mdl["regs"], (gen_kwh, cl_kwh, exp_kwh)):
                if reg is None or v is None:
                    continue
                rows.append(dict(nmi=cu["nmi"], serial=m["serial"], register=reg, start=fa, end=fb, days=days,
                                 kwh=round(v, dec) if dec else float(int(round(v)))))
    w.reads = rows
    return rows
