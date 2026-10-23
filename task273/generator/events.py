"""The region's crashes, 2021 to 2025, drawn from the miles in world.py: each crash's kind, place, local time, vehicles
and their uses, the driver who caused it, who fled, who was hurt and who died within 30 days. Truth only; records.py
writes what the state's crash reports and the other offices' files would hold."""
import datetime as dt

import numpy as np

import common as K
import roads as RD
import world as W

KINDS = ("MV", "SV", "PK", "PED", "CYC")

# the commission's licensed operators and platforms, by use: (register name, the names officers write, share)
OPERATORS = {
    "TX": [("Kelderwick Cab Company", ["KELDERWICK CAB CO", "Kelderwick Cab", "KW CAB CO"], 0.34),
           ("Valleywide Taxi", ["VALLEYWIDE TAXI", "Valley Wide Taxi"], 0.22),
           ("Fairhollow City Cab", ["FAIRHOLLOW CITY CAB", "FH City Cab"], 0.17),
           ("Stonereach Taxi Cooperative", ["STONEREACH TAXI COOP", "Stonereach Taxi Co-op"], 0.13),
           ("Bluegate Taxi", ["BLUEGATE TAXI"], 0.08),
           ("Orchard Cab", ["ORCHARD CAB LLC", "Orchard Cab"], 0.06)],
    "RH": [("Vinca", ["VINCA", "Vinca Rides"], 0.63),
           ("Tallo", ["TALLO", "Tallo Ride"], 0.37)],
    "LM": [("Silverline Chauffeured Cars", ["SILVERLINE", "Silverline Chauffeured"], 0.21),
           ("Crownridge Limousine", ["CROWNRIDGE LIMO", "Crownridge Limousine"], 0.16),
           ("Evening Star Limousine", ["EVENING STAR LIMO"], 0.14),
           ("Halcyon Car Service", ["HALCYON CAR SVC", "Halcyon Car Service"], 0.13),
           ("Meridian Black Car", ["MERIDIAN BLACK CAR"], 0.12),
           ("Stonereach Executive Sedans", ["STONEREACH EXEC SEDANS"], 0.10),
           ("Night Owl Limousine", ["NIGHT OWL LIMO"], 0.08),
           ("Velvet Road Limousine", ["VELVET ROAD LIMO"], 0.06)],
    "AS": [("Kelderwick Airport Shuttle", ["KW AIRPORT SHUTTLE", "Kelderwick Airport Shuttle"], 0.33),
           ("Skyway Valley Shuttle", ["SKYWAY VALLEY SHUTTLE", "Skyway Shuttle"], 0.25),
           ("HotelLink Shuttles", ["HOTELLINK", "Hotel Link Shuttles"], 0.18),
           ("Runway Express Shuttle", ["RUNWAY EXPRESS"], 0.14),
           ("Valley Transit Charters", ["VALLEY TRANSIT CHARTERS"], 0.10)],
    "PT": [("CareRide Transport", ["CARERIDE", "CareRide Transport"], 0.36),
           ("Access Valley Paratransit", ["ACCESS VALLEY PARATRANSIT", "Access Valley"], 0.30),
           ("MediMove Transport", ["MEDIMOVE", "MediMove NEMT"], 0.20),
           ("Kindway Transport", ["KINDWAY TRANSPORT"], 0.14)],
    "PD": [("Rapidline Parcel", ["RAPIDLINE PARCEL", "Rapidline"], 0.27),
           ("Valley Courier Express", ["VALLEY COURIER EXPRESS", "Valley Courier"], 0.19),
           ("Lastmile Logistics", ["LASTMILE LOGISTICS", "Last Mile Logistics"], 0.17),
           ("Parcelwise Delivery", ["PARCELWISE"], 0.14),
           ("Swiftbox Couriers", ["SWIFTBOX COURIERS", "Swiftbox"], 0.12),
           ("Northgate Parcel Service", ["NORTHGATE PARCEL SVC"], 0.11)],
    "AD": [("Forkfleet", ["FORKFLEET", "Forkfleet Delivery"], 0.46),
           ("Basketrun", ["BASKETRUN"], 0.33),
           ("Nibbly", ["NIBBLY", "Nibbly Couriers"], 0.21)],
}
OTHER_CARRIERS = ["GRANITE FREIGHT", "VALLEY READY MIX", "STONEREACH UTILITIES", "CASCADE BUILDERS SUPPLY",
                  "ORCHARD LINEN SERVICE", "HIGHLINE MOVING", "PACIFIC PRODUCE HAULERS", "ALDER PLUMBING",
                  "TRI-COUNTY ELECTRIC", "BIGHORN TOWING"]
BODY = {
    "PV": (("PC", 0.45), ("SUV", 0.33), ("PU", 0.15), ("VAN", 0.07)),
    "TX": (("PC", 0.55), ("VAN", 0.30), ("SUV", 0.15)),
    "RH": (("PC", 0.50), ("SUV", 0.40), ("VAN", 0.10)),
    "LM": (("PC", 0.40), ("SUV", 0.45), ("VAN", 0.15)),
    "AS": (("VAN", 0.55), ("MB", 0.45)),
    "PT": (("VAN", 0.60), ("MB", 0.40)),
    "PD": (("CV", 0.80), ("SUT", 0.20)),
    "AD": (("PC", 0.55), ("SUV", 0.30), ("PU", 0.10), ("VAN", 0.05)),
    "OC": (("PU", 0.20), ("CV", 0.20), ("SUT", 0.30), ("TT", 0.30)),
    "TB": (("BUS", 1.0),), "SB": (("BUS", 1.0),),
    "GV": (("PC", 0.30), ("SUV", 0.30), ("PU", 0.30), ("SUT", 0.10)),
    "EM": (("SUV", 0.40), ("PC", 0.30), ("SUT", 0.30)),
    "MC": (("MC", 1.0),),
}
MARKED = {"TX", "LM", "AS", "PT", "PD", "TB", "SB", "GV", "EM"}
AT_FAULT_CODES = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "12", "14"]
NM_FAULT_CODES = ["31", "32", "33", "34"]


def pick(rng, pairs):
    names = [p[0] for p in pairs]
    w = np.array([p[1] for p in pairs], float)
    return names[int(rng.choice(len(names), p=w / w.sum()))]


def occupants(rng, u):
    if u in ("PD", "AD", "MC"):
        return 1
    if u == "TX":
        return 1 + (int(rng.random() < 0.6) * (1 + int(rng.poisson(0.3))))
    if u == "RH":
        return 1 + (int(rng.random() < 0.55) * (1 + int(rng.poisson(0.4))))
    if u == "LM":
        return 1 + (int(rng.random() < 0.6) * (1 + int(rng.poisson(0.8))))
    if u == "AS":
        return 1 + int(rng.poisson(3.0))
    if u == "PT":
        return 1 + int(rng.poisson(1.2))
    if u == "TB":
        return 1 + int(rng.poisson(7.0))
    if u == "SB":
        return 1 + int(rng.poisson(9.0)) * int(rng.random() < 0.6)
    if u == "OC":
        return 1 + int(rng.poisson(0.2))
    return 1 + int(rng.poisson(0.45))


def severity(rng, kind, g, h, role, body):
    """KABCO as the officer recorded it at the scene."""
    s = {"UF": 1.25, "UA": 1.0, "UL": 0.85, "RF": 1.7, "RA": 1.6, "RL": 1.35}[g] * (1.25 if h in W.NIGHT else 1.0)
    if role == "PED":
        p = [0.045 * s, 0.19 * s, 0.33, 0.30]
    elif role == "CYC":
        p = [0.011 * s, 0.10 * s, 0.37, 0.34]
    elif body == "MC":
        p = [0.035 * s, 0.16 * s, 0.30, 0.20]
    elif kind == "SV":
        p = [0.007 * s, 0.035 * s, 0.085, 0.11]
    elif kind == "PK":
        p = [0.0004, 0.003, 0.02, 0.05] if role == "STRIKE" else [0.0, 0.002, 0.03, 0.08]
    else:
        p = [0.0009 * s * s, 0.0075 * s, 0.030, 0.068]
        if body == "BUS":
            p = [x * 0.3 for x in p]
        elif body in ("SUT", "TT"):
            p = [x * 0.5 for x in p]
    r = rng.random()
    acc = 0.0
    for code, q in zip("KABC", p):
        acc += q
        if r < acc:
            return code
    return "O"


class Gen:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        self.rng = np.random.default_rng(seed * 1000 + 17)
        self.rng2 = np.random.default_rng(seed * 1000 + 19)
        self.segs = RD.network(seed)
        self.cells, self.E, self.m = W.miles_table()
        self.by_class = {}
        for s in self.segs:
            self.by_class.setdefault((s["fc"], s["ur"]), []).append(s)
        self.seg_w = {k: np.array([s["vmt"] for s in v], float) / sum(s["vmt"] for s in v)
                      for k, v in self.by_class.items()}
        self.days = {y: W.days_of(y) for y in K.YEARS}
        self.day_w = {}
        for y in K.YEARS:
            for d in ("wd", "we"):
                for ur in ("U", "R"):
                    w = np.array([W.MONTH[ur][x.month - 1] for x in self.days[y][d]], float)
                    self.day_w[(y, d, ur)] = w / w.sum()
        self.gaps = {}
        for y in K.YEARS:
            mar = [dt.date(y, 3, x) for x in range(8, 15) if dt.date(y, 3, x).weekday() == 6][0]
            self.gaps[y] = mar
        self.ops = {u: ([o[0] for o in v], np.array([o[2] for o in v], float) / sum(o[2] for o in v))
                    for u, v in OPERATORS.items()}

    def when(self, y, d, h, ur):
        rng = self.rng
        while True:
            day = self.days[y][d][int(rng.choice(len(self.days[y][d]), p=self.day_w[(y, d, ur)]))]
            if h == 2 and day == self.gaps[y]:
                continue
            return day, int(rng.integers(0, 60))

    def vehicle(self, u, role="MV"):
        rng = self.rng
        v = dict(type=role, use=u, body=pick(rng, BODY[u]), op=None, fault=False, fled=False, contrib="00")
        if u in self.ops:
            names, w = self.ops[u]
            v["op"] = names[int(rng.choice(len(names), p=w))]
        v["occ"] = occupants(rng, u) if role != "PK" else int(rng.random() < 0.08)
        v["age"] = int(np.clip(rng.normal(44 if u != "PV" else 41, 13), 16, 88))
        v["vyear"] = int(np.clip(round(rng.normal(2017 if u in ("PV", "MC", "AD", "RH") else 2019, 4)), 1994, 2026))
        return v

    def draw_use(self, c, weights):
        w = np.array([weights[u] * self.m[(u, c)] for u in W.ALL_USES], float)
        return W.ALL_USES[int(self.rng.choice(len(w), p=w / w.sum()))]

    def crashes(self):
        rng = self.rng
        out = []
        lam = {kind: {} for kind in KINDS}
        for c in self.cells:
            g = K.GROUP_OF[(c[1], c[2])]
            for kind in KINDS:
                rh = W.RHO if kind in ("MV", "PK") else (W.RHO_SV if kind == "SV" else W.RHO_NM)
                lam[kind][c] = W.intensity(kind, g, c[3], c[4]) * sum(rh[u] * self.m[(u, c)] for u in W.ALL_USES)
        for kind in KINDS:
            tot = sum(lam[kind].values())
            for c in self.cells:
                n = int(rng.poisson(W.TARGET[kind] * lam[kind][c] / tot))
                for _ in range(n):
                    out.append(self.one(kind, c))
        out.sort(key=lambda x: (x["date"], x["minute"], x["seg"]))
        return out

    def one(self, kind, c):
        rng = self.rng
        y, fc, ur, d, h = c
        g = K.GROUP_OF[(fc, ur)]
        day, minute = self.when(y, d, h, ur)
        segs = self.by_class[(fc, ur)]
        seg = segs[int(rng.choice(len(segs), p=self.seg_w[(fc, ur)]))]
        mp = round(float(rng.uniform(seg["b"], seg["e"])), 2)
        if mp <= seg["b"]:
            mp = round(seg["b"] + 0.01, 2)
        if mp >= seg["e"]:
            mp = round(seg["e"] - 0.01, 2)
        cr = dict(kind=kind, year=y, fc=fc, ur=ur, group=g, dtype=d, hour=h, date=day, minute=h * 60 + minute,
                  seg=seg["i"], route=seg["route"], mp=mp, agency=seg["agency"], city=seg["city"],
                  located=bool(rng.random() > 0.012), units=[], undetermined=False)
        night = h in W.NIGHT
        if kind == "MV":
            nveh = 2 + int(rng.random() < (0.20 if g in ("UF", "RF") else 0.11)) \
                + int(rng.random() < (0.05 if g in ("UF", "RF") else 0.02))
            a = self.vehicle(self.draw_use(c, W.RHO))
            a["fault"] = True
            hr = (0.06 if night else 0.025) * (0.25 if a["use"] in MARKED else 1.0)
            a["fled"] = bool(rng.random() < hr)
            others = [self.vehicle(self.draw_use(c, {u: 1.0 for u in W.ALL_USES})) for _ in range(nveh - 1)]
            units = [a] + others
            if rng.random() > 0.70:
                rng.shuffle(units)
            cr["undetermined"] = bool(rng.random() < 0.03)
            cr["both"] = bool((not cr["undetermined"]) and rng.random() < 0.05)
            if cr["both"]:
                others[int(rng.integers(0, len(others)))]["fault2"] = True
        elif kind == "SV":
            a = self.vehicle(self.draw_use(c, W.RHO_SV))
            a["fault"] = True
            units = [a]
            cr["undetermined"] = bool(rng.random() < 0.08)
            cr["both"] = False
        elif kind == "PK":
            a = self.vehicle(self.draw_use(c, W.RHO))
            a["fault"] = True
            a["fled"] = bool(rng.random() < 0.30 * (0.3 if a["use"] in MARKED else 1.0))
            npk = 1 + int(rng.random() < 0.15)
            pk = [self.vehicle(self.draw_use(c, W.PARKED), role="PK") for _ in range(npk)]
            units = [a] + pk
            cr["undetermined"] = bool(rng.random() < 0.05)
            cr["both"] = False
        else:
            a = self.vehicle(self.draw_use(c, W.RHO_NM))
            nm = dict(type=kind, use=None, body=None, op=None, fault=False, fled=False, contrib="00", occ=1,
                      age=int(np.clip(rng.normal(38, 19), 4, 92)), vyear=None)
            r = rng.random()
            pdrv = 0.58 if kind == "PED" else 0.55
            if r < pdrv:
                a["fault"] = True
            elif r < 0.95:
                nm["fault"] = True
            else:
                cr["undetermined"] = True
            a["fled"] = bool(rng.random() < (0.12 if kind == "PED" else 0.10) * (0.3 if a["use"] in MARKED else 1.0))
            units = [a, nm]
            cr["both"] = False
        for i, v in enumerate(units, 1):
            v["no"] = i
        cr["units"] = units
        # who was hurt
        persons = []
        for v in units:
            if v["type"] in ("PED", "CYC"):
                persons.append(dict(unit=v["no"], role=v["type"], seat="00", age=v["age"],
                                    sex="M" if rng.random() < (0.62 if v["type"] == "PED" else 0.8) else "F",
                                    sev=severity(rng, kind, g, h, v["type"], None)))
                continue
            if v["fled"]:
                continue
            role = "STRIKE" if (kind == "PK" and v["type"] == "MV") else v["type"]
            for k in range(v["occ"]):
                if k == 0 and v["type"] != "PK":
                    age, seat, prole = v["age"], "01", "DRIVER"
                else:
                    age = int(np.clip(rng.normal(36, 20), 1, 90))
                    seat, prole = "%02d" % (k + 1 if v["type"] != "PK" else 1 + k), "PASSENGER"
                persons.append(dict(unit=v["no"], role=prole, seat=seat, age=age,
                                    sex="M" if rng.random() < 0.52 else "F",
                                    sev=severity(rng, kind, g, h, role, v["body"])))
        seen = set()
        for p in persons:
            while (p["unit"], p["role"], p["age"], p["sex"]) in seen:
                p["age"] += 1
            seen.add((p["unit"], p["role"], p["age"], p["sex"]))
        for p in persons:
            p["died30"] = False
            p["died_after"] = None
            if p["sev"] == "K":
                p["died30"] = True
                p["death_day"] = 0
            elif p["sev"] == "A" and rng.random() < 0.07:
                p["died30"] = True
                p["death_day"] = int(min(30, 1 + rng.geometric(0.12)))
            elif p["sev"] == "B" and rng.random() < 0.005:
                p["died30"] = True
                p["death_day"] = int(min(30, 1 + rng.geometric(0.12)))
            elif p["sev"] == "A" and rng.random() < 0.02:
                p["died_after"] = int(31 + rng.integers(0, 40))
        self.revise(persons)
        cr["persons"] = persons
        return cr

    def revise(self, persons):
        """What the agency learned after the report: the final severity, and whether it filed a supplement that lists
        the person again with it. A death within 30 days is final K; the state's register lists every one."""
        r = self.rng2
        for p in persons:
            sev = p["sev"]
            p["final"], p["supp"] = sev, False
            if p["died30"] and sev != "K":
                p["final"], p["supp"] = "K", bool(r.random() < 0.55)
            elif sev == "A":
                if r.random() < 0.03:
                    p["final"], p["supp"] = "B", True
            elif sev == "B":
                x = r.random()
                if x < 0.025:
                    p["final"], p["supp"] = "A", True
                elif x < 0.045:
                    p["final"], p["supp"] = "C", True
            elif sev == "C":
                x = r.random()
                if x < 0.02:
                    p["final"], p["supp"] = "B", True
                elif x < 0.04:
                    p["final"], p["supp"] = "O", True
            elif sev == "O" and r.random() < 0.004:
                p["final"], p["supp"] = "C", True


def world(seed=K.SEED):
    g = Gen(seed)
    cr = g.crashes()
    return dict(segs=g.segs, crashes=cr, cells=g.cells, E=g.E, m=g.m, gen=g)


if __name__ == "__main__":
    import collections
    import time
    t = time.time()
    w = world()
    cr = w["crashes"]
    print(len(cr), "crashes in %.1f s" % (time.time() - t))
    print(collections.Counter(x["kind"] for x in cr))
    print("units", sum(len(x["units"]) for x in cr), "persons", sum(len(x["persons"]) for x in cr))
    inj = [x for x in cr if any(p["sev"] != "O" for p in x["persons"])]
    print("injury crashes", len(inj), "persons in them", sum(len(x["persons"]) for x in inj))
