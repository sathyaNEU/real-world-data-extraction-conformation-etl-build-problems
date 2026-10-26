"""Esklett's Population Register from its opening on 1 January 2014 to the 31 August 2026 cut: every person who arrived
to work, every stay from arrival to departure, the legacy register to the move of 13 March 2023 and the current system
after it. This is the clean truth; pack.py cuts the register's files from it and golden.py never reads it."""
import datetime as dt

import numpy as np

D = dt.date
TD = dt.timedelta
SEED = 3
OPEN = D(2014, 1, 1)
MOVE = D(2023, 3, 13)          # the current register system's first day; the legacy register closed on 12 March
CUT = D(2026, 8, 31)
EXTRACT = D(2026, 9, 30)
SWITCH = D(2025, 10, 31)       # agency placements ending after this are re-placed after a short break
CODES26 = D(2026, 1, 1)        # registrations from this day carry the 2026 sector list
MERGE = D(2025, 4, 1)          # Haldervoe and Ivarsby merged

SECTORS = [("HOS", "Hospitality and tourism"), ("AGR", "Agriculture, fishing and food"), ("CON", "Construction"),
           ("FIN", "Financial and professional services"), ("HSC", "Health and social care"),
           ("RET", "Retail and distribution"), ("DIG", "Digital and e-gaming"), ("OTH", "Public and other services")]
SECT = [s for s, _ in SECTORS]
ACT14 = [("01", "Accommodation", "HOS"), ("02", "Restaurants, bars and catering", "HOS"),
         ("03", "Agriculture and horticulture", "AGR"), ("04", "Fishing and aquaculture", "AGR"),
         ("05", "Food and drink manufacturing", "AGR"), ("06", "Construction and building trades", "CON"),
         ("07", "Banking", "FIN"), ("08", "Insurance and fund management", "FIN"),
         ("09", "Legal, accounting and professional services", "FIN"), ("10", "Hospital and medical services", "HSC"),
         ("11", "Residential and domiciliary care", "HSC"), ("12", "Retail trade", "RET"),
         ("13", "Wholesale, warehousing and distribution", "RET"), ("14", "Information technology", "DIG"),
         ("15", "E-gaming and online services", "DIG"), ("16", "Public administration and education", "OTH"),
         ("17", "Other services", "OTH")]
TO26 = {c: s for c, _, s in ACT14}
PARISHES = [("PES", "Port Esklett"), ("RAV", "Ravelsay"), ("DRU", "Drumskea"), ("HAL", "Haldervoe"),
            ("DUN", "Dunvallow"), ("IVA", "Ivarsby"), ("PEN", "Pennaval"), ("COR", "Corvanagh"),
            ("THO", "Thornavick"), ("BRA", "Brackmuir"), ("STR", "Strathvenny"), ("ARD", "Ardvollan"),
            ("FER", "Fernhaskey"), ("ELL", "Elloravon")]
PARISH_W = [.27, .09, .06, .05, .07, .04, .08, .06, .05, .06, .05, .04, .04, .04]

# yearly first arrivals at the 2019 level, by sector and kind
VOL = {"HOS": dict(contract=150, settler=100, seasonal=150, circular=70),
       "AGR": dict(contract=40, settler=40, seasonal=50),
       "CON": dict(contract=120, settler=60, circular=200),
       "FIN": dict(contract=150, settler=200),
       "HSC": dict(contract=140, settler=190, circular=300),
       "RET": dict(contract=60, settler=60, seasonal=30, circular=190),
       "DIG": dict(contract=90, settler=110),
       "OTH": dict(contract=110, settler=140)}
GROWTH = {2014: .85, 2015: .88, 2016: .91, 2017: .94, 2018: .97, 2019: 1.0, 2020: .55, 2021: .85, 2022: 1.0,
          2023: 1.02, 2024: 1.04, 2025: 1.06, 2026: 1.08}
MONTH_W = [1.2, .9, 1.0, 1.1, 1.0, .9, .9, .9, 1.2, 1.0, .9, .8]
SEASON_W = [.1, .3, 1.2, 1.6, 1.5, 1.0, .3, .1, .05, .05, .05, .05]
# activity codes by sector and kind (the agencies place care, building and warehouse staff)
CODE_W = {"HOS": (("01", .45), ("02", .55)), "AGR": (("03", .45), ("04", .2), ("05", .35)),
          "CON": (("06", 1.0),), "FIN": (("07", .35), ("08", .35), ("09", .3)),
          "HSC": (("10", .55), ("11", .45)), "RET": (("12", .6), ("13", .4)),
          "DIG": (("14", .55), ("15", .45)), "OTH": (("16", .6), ("17", .4))}
CIRC_CODE = {"HOS": (("01", .5), ("02", .5)), "CON": (("06", 1.0),), "HSC": (("11", 1.0),),
             "RET": (("12", .5), ("13", .5))}
# a change of employment notified to the legacy register: yearly rate out of the sector, and where people went
EXIT = {"HOS": .12, "AGR": .10, "CON": .07, "FIN": .05, "HSC": .05, "RET": .10, "DIG": .06, "OTH": .04}
DEST = {"HOS": (("RET", .35), ("OTH", .35), ("FIN", .15), ("HSC", .15)), "AGR": (("CON", .4), ("OTH", .3), ("RET", .3)),
        "CON": (("OTH", .5), ("RET", .3), ("AGR", .2)), "FIN": (("DIG", .4), ("OTH", .6)),
        "HSC": (("OTH", .7), ("FIN", .3)), "RET": (("HOS", .3), ("OTH", .4), ("FIN", .3)),
        "DIG": (("FIN", .7), ("OTH", .3)), "OTH": (("FIN", .5), ("HSC", .3), ("DIG", .2))}
FEMALE = {"HOS": .55, "AGR": .3, "CON": .08, "FIN": .45, "HSC": .78, "RET": .55, "DIG": .3, "OTH": .5}
OTHER_NAT = ["ESP", "ITA", "FRA", "DEU", "NLD", "HUN", "SVK", "CZE", "BRA", "NZL", "CAN", "CHN", "MYS", "PAK", "LKA",
             "NPL", "GHA", "GRC", "SWE", "USA", "AUS", "MLT", "UKR", "HRV"]
NAT = {"HOS": dict(GBR=.25, IRL=.06, POL=.08, ROU=.08, PRT=.07, LVA=.05, LTU=.05, PHL=.06, IND=.05, ZAF=.04,
                   BGR=.04),
       "AGR": dict(GBR=.30, IRL=.10, POL=.15, ROU=.15, LVA=.08, LTU=.08, BGR=.06),
       "CON": dict(GBR=.30, IRL=.10, POL=.14, ROU=.12, LTU=.07, LVA=.06, BGR=.05, PRT=.04),
       "FIN": dict(GBR=.55, IRL=.10, ZAF=.07, USA=.04, AUS=.03, IND=.05, FRA=.03, DEU=.03),
       "HSC": dict(GBR=.30, IRL=.06, PHL=.14, IND=.14, ZWE=.05, NGA=.05, ZAF=.05, KEN=.03, POL=.04, ROU=.04),
       "RET": dict(GBR=.32, IRL=.06, POL=.10, ROU=.10, LVA=.06, LTU=.06, PRT=.05, PHL=.04, IND=.04),
       "DIG": dict(GBR=.40, IRL=.06, IND=.10, POL=.06, UKR=.05, BGR=.04, ZAF=.04, MLT=.04),
       "OTH": dict(GBR=.45, IRL=.10, ZAF=.05, USA=.04, AUS=.04, POL=.05, IND=.05)}


def anniversary(a):
    """the first anniversary of an arrival date (1 March for an arrival on 29 February)"""
    return D(a.year + 1, 3, 1) if (a.month, a.day) == (2, 29) else D(a.year + 1, a.month, a.day)


class Stay:
    __slots__ = ("pid", "sector", "code", "kind", "arrive", "leave", "registered", "notice", "parish", "n", "move_code",
                 "dup_registered", "dup_parish")

    def __init__(self, pid, sector, code, kind, arrive, leave):
        self.pid, self.sector, self.code, self.kind, self.arrive, self.leave = pid, sector, code, kind, arrive, leave
        self.registered = self.notice = self.parish = self.move_code = None
        self.dup_registered = self.dup_parish = None
        self.n = 0

    def transferred(self):
        """open on the legacy register when it closed: registered before the move and no leaving notice in by then"""
        return self.registered < MOVE and not (self.leave < MOVE and self.notice < MOVE)

    def long(self):
        """the true twelve-month outcome (the world knows every departure)"""
        return self.leave >= anniversary(self.arrive)


class World:
    def __init__(self, seed=SEED):
        self.rng = np.random.default_rng(seed)
        self.stays = []
        self.people = {}

    # ---------------------------------------------------------------- draws
    def pick(self, pairs):
        keys = [k for k, _ in pairs]
        p = np.array([w for _, w in pairs], float)
        return keys[int(self.rng.choice(len(keys), p=p / p.sum()))]

    def day_in(self, year, weights):
        w = np.array(weights, float)
        if year == 2020:
            w = w * np.array([1, 1, .6, .15, .15, .3, .6, .7, .8, .8, .7, .7])
        m = int(self.rng.choice(12, p=w / w.sum())) + 1
        last = (D(year + (m == 12), m % 12 + 1, 1) - TD(days=1)).day
        return D(year, m, int(self.rng.integers(1, last + 1)))

    def person(self, sector):
        r = self.rng
        pid = len(self.people) + 1
        nat = dict(NAT[sector])
        rest = 1 - sum(nat.values())
        pairs = list(nat.items()) + [(c, rest / len(OTHER_NAT)) for c in OTHER_NAT]
        self.people[pid] = dict(sex="F" if r.random() < FEMALE[sector] else "M", nat=self.pick(pairs),
                                age=float(min(64, 18 + r.gamma(3.0, 4.6))))
        return pid

    def code(self, sector, kind):
        return self.pick(CIRC_CODE[sector] if kind == "circular" else CODE_W[sector])

    # ---------------------------------------------------------------- stays
    def add(self, pid, sector, kind, arrive, days, code=None):
        s = Stay(pid, sector, code or self.code(sector, kind), kind, arrive, arrive + TD(days=int(days)))
        self.stays.append(s)
        return s

    def length(self, kind):
        r = self.rng
        if kind == "contract":
            return r.integers(380, 1200) if r.random() < .80 else r.integers(30, 356)
        if kind == "settler":
            return r.integers(1000, 5000) if r.random() < .93 else r.integers(30, 356)
        if kind == "returning":
            return r.integers(700, 4000) if r.random() < .85 else r.integers(40, 356)
        raise ValueError(kind)

    def circular(self, pid, sector, arrive):
        """an agency worker's placements: under eleven and a half months each, then a break and, often, another"""
        r = self.rng
        code = self.code(sector, "circular")
        while arrive <= CUT:
            if r.random() < .03:
                self.add(pid, sector, "circular", arrive, r.integers(380, 1500), code)
                return
            s = self.add(pid, sector, "circular", arrive, r.integers(285, 351), code)
            new = s.leave > SWITCH
            if r.random() > (.92 if new else .25):
                return
            arrive = s.leave + TD(days=int(r.integers(25, 61) if new else r.integers(60, 151)))

    def seasonal(self, pid, sector, arrive):
        r = self.rng
        code = self.code(sector, "seasonal")
        while arrive <= CUT:
            s = self.add(pid, sector, "seasonal", arrive, r.integers(60, 201), code)
            if r.random() > .35:
                return
            arrive = D(arrive.year + 1, 1, 1) + TD(days=int((arrive - D(arrive.year, 1, 1)).days + r.integers(-30, 31)))
            if arrive <= s.leave:
                return

    def settle(self, pid, sector, kind, arrive):
        r = self.rng
        s = self.add(pid, sector, kind, arrive, self.length(kind))
        if s.leave <= CUT and r.random() < .05:
            back = s.leave + TD(days=int(r.integers(400, 2500)))
            if back <= CUT:
                sec = sector if r.random() < .6 else SECT[int(r.integers(0, len(SECT)))]
                self.add(pid, sec, "returning", back, self.length("returning"))

    def build(self):
        r = self.rng
        for year in range(2014, 2027):
            g = GROWTH[year]
            for sector in SECT:
                for kind, base in sorted(VOL[sector].items()):
                    w = list(SEASON_W if kind == "seasonal" else MONTH_W)
                    frac = 1.0
                    if year == 2026:
                        frac = sum(w[:8]) / sum(w)
                        w[8:] = [0.0] * 4
                    for _ in range(r.poisson(base * g * frac * 1.12)):
                        arrive = self.day_in(year, w)
                        pid = self.person(sector)
                        if kind == "circular":
                            self.circular(pid, sector, arrive)
                        elif kind == "seasonal":
                            self.seasonal(pid, sector, arrive)
                        else:
                            self.settle(pid, sector, kind, arrive)
        self.companions()
        self.stays = [s for s in self.stays if OPEN <= s.arrive <= CUT]
        self.stays.sort(key=lambda s: (s.arrive, s.pid))
        self.records()
        self.apart()
        return self

    def apart(self):
        """people who came over together and are still on the island at the extract differ in birth year, so no two
        legacy records still open at the extract share every declared particular"""
        def yob(s):
            first = self.by_person[s.pid][0].arrive
            return int(first.year - self.people[s.pid]["age"] - (first.timetuple().tm_yday / 366.0) + .5)
        while True:
            seen, moved = {}, False
            for s in self.stays:
                if s.registered >= MOVE or (s.leave <= CUT and s.notice <= EXTRACT):
                    continue
                p = self.people[s.pid]
                k = (s.arrive, p["sex"], yob(s), p["nat"], s.code)
                if k in seen and seen[k] != s.pid:
                    p["age"] += 1.0
                    moved = True
                else:
                    seen[k] = s.pid
            if not moved:
                return

    def companions(self):
        """people who came over together: an agency or employer bringing two to five workers from one country for one
        kind of work on one day, or a firm's graduate intake starting together, each on a contract of their own and of
        much the same age. Drawn from a stream of their own, so the rest of the world is untouched; legacy-era arrivals
        only, none of them returning"""
        r = np.random.default_rng(SEED + 101)
        leads = [s for s in self.stays if s.arrive < D(2022, 5, 1) and s.kind in ("contract", "seasonal", "settler")]
        for s in leads:
            if r.random() >= .15:
                continue
            lead = self.people[s.pid]
            for _ in range(int(r.integers(1, 5))):
                pid = len(self.people) + 1
                nat = lead["nat"] if r.random() < .85 else self.pick(list(NAT[s.sector].items()))
                self.people[pid] = dict(sex="F" if r.random() < FEMALE[s.sector] else "M", nat=nat,
                                        age=float(min(64, max(18, lead["age"] + r.uniform(-2.5, 2.5)))))
                if s.kind == "seasonal":
                    days = int(r.integers(60, 201))
                elif s.kind == "contract":
                    days = int(r.integers(380, 1200)) if r.random() < .8 else int(r.integers(30, 356))
                else:
                    days = int(r.integers(1000, 5000)) if r.random() < .93 else int(r.integers(30, 356))
                self.stays.append(Stay(pid, s.sector, s.code, s.kind, s.arrive, s.arrive + TD(days=days)))

    # ---------------------------------------------------------------- the register's own records
    def records(self):
        r = self.rng
        for s in self.stays:
            if s.arrive < MOVE:
                lag = min(90, int(r.exponential(24)))
            else:
                lag = min(45, int(r.exponential(4))) + (int(r.integers(15, 46)) if r.random() < .03 else 0)
            s.registered = s.arrive + TD(days=lag)
            nl = int(r.exponential(5)) + (int(r.integers(20, 121)) if r.random() < .04 else 0)
            s.notice = s.leave + TD(days=nl)
            s.parish = PARISHES[int(r.choice(len(PARISHES), p=np.array(PARISH_W) / sum(PARISH_W)))][0]
        for s in self.stays:
            if s.transferred():
                s.move_code = self.job_changes(s)
        all_stays = {}
        for s in self.stays:
            all_stays.setdefault(s.pid, []).append(s)
        for pid in sorted(all_stays):
            v = all_stays[pid]
            # registered a second time at another parish office, by an employer or by the person: the legacy register
            # held the person twice, and its leaving notice closed both records
            if len(v) != 1 or not (v[0].registered < MOVE and v[0].leave <= CUT and v[0].notice <= EXTRACT):
                continue
            if r.random() >= .06:
                continue
            s = v[0]
            d = s.registered + TD(days=int(r.integers(5, 61)))
            if d < s.leave:
                k = int(r.integers(0, len(PARISHES) - 1))
                if d < MOVE:
                    s.dup_registered = d
                    s.dup_parish = [c for c, _ in PARISHES if c != s.parish][k]
        # a few registrations made late: the legacy register's three months overrun, the current system's 14 days
        for s in self.stays:
            u = r.random()
            if s.arrive < MOVE and u < .02:
                d = s.arrive + TD(days=int(r.integers(91, 241)))
                if d < MOVE - TD(days=30) and d < s.leave and (s.dup_registered is None or d < s.dup_registered):
                    s.registered = d
            elif s.arrive >= MOVE and u < .01:
                d = s.arrive + TD(days=int(r.integers(46, 121)))
                if d < s.leave and d <= EXTRACT - TD(days=30):
                    s.registered = d
        # nobody is registered after the stay has ended: a registration still outstanding on the leaving day is made
        # the day before, and a stay that comes to be open on the legacy register at the move keeps its declared code
        for s in self.stays:
            if s.registered >= s.leave:
                s.registered = s.leave - TD(days=1)
                if s.transferred() and s.move_code is None:
                    s.move_code = s.code
        by = {}
        for s in self.stays:
            by.setdefault(s.pid, []).append(s)
        for v in by.values():
            v.sort(key=lambda s: s.arrive)
            for i, s in enumerate(v):
                s.n = i + 1
        self.by_person = by


    def job_changes(self, s):
        """the activity the legacy register held for the person on its last day: the code declared at registration,
        overwritten at each change of employment the person notified (three in ten within the same sector)"""
        r = self.rng
        code, sector, t = s.code, s.sector, s.registered
        while True:
            t = t + TD(days=int(r.exponential(365.25 * .7 / EXIT[sector])) + 1)
            if t >= MOVE or t >= s.leave:
                return code
            if r.random() < .3:
                others = [c for c, _ in CODE_W[sector] if c != code]
                if others:
                    code = others[int(r.integers(0, len(others)))]
                continue
            sector = self.pick(DEST[sector])
            code = self.pick(CODE_W[sector])


def build(seed=SEED):
    return World(seed).build()


def returner(stays_of_person, s, window=365):
    """true when the person's previous stay ended within `window` days before this arrival"""
    return any(o is not s and o.leave < s.arrive and (s.arrive - o.leave).days <= window for o in stays_of_person)
