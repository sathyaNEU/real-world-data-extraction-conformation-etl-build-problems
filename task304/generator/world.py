"""task304 architecture 5: the clean truth of Ardleshire's road network. Junction nodes with traffic by year, injury
collisions 2016 to 2025 from a safety performance by layout and each junction's own spread beyond chance, the six
junctions the 2026 screening lists, and the county's 2026 provisional collisions with their casualties and vehicles.
Everything downstream (pack, analysis, checks) reads from here or from target/; nothing here is written for a reader."""
import datetime as dt
from collections import defaultdict

import numpy as np

import params as P

FIRST = ["Alan", "Brian", "Carol", "Diane", "Edward", "Fiona", "Gareth", "Helen", "Ian", "Janet", "Keith", "Linda"]
MINOR_NAMES = ["Mill Lane", "Church Street", "Station Road", "Fen Lane", "Holt Lane", "Coppice Way", "Tollgate Road",
               "Back Lane", "Moor Road", "Park Lane", "School Lane", "Green Lane", "Chapel Street", "Main Street",
               "Grange Road", "Hall Lane", "Westfield Road", "Brook Street", "Manor Road", "Kiln Lane", "Pinfold Lane",
               "Sandy Lane", "Ings Lane", "Carr Lane", "Field Lane", "Wold Road", "Low Road", "High Street",
               "Bridge Street", "Mere Lane", "Common Lane", "Hollow Lane", "Barn Close", "Priory Road", "Long Lane",
               "Cross Lane", "Gravel Pit Lane", "Thorn Lane", "Ash Grove", "Willow Road", "Beck Lane", "Marsh Lane"]
A_ROADS = [("A5207", "Ardle Road"), ("A5207", "London Road"), ("A6118", "Brindham Road"), ("A6118", "Station Road"),
           ("A4560", "Kestermoor Road"), ("A5340", "Hessle Road"), ("A6075", "Sutton Road"), ("A4600", "Ardle Bypass"),
           ("A6510", "Wold Road")]
B_ROADS = [("B4419", "Saxby Road"), ("B4421", "Mill Lane"), ("B4433", "Kestermoor Road"), ("B4450", "Thorpe Road"),
           ("B4467", "Ings Road"), ("B4480", "Carlby Road"), ("B4492", "Hollin Road"), ("B4512", "Stow Road")]
TRUNK = {"A4600": None, "A6510": None}   # A6510 trunk throughout; A4600 trunk west of its Brindham East node (the
#                                          section east of that node was detrunked to the county in 2019); set by World
DISTRICT_BOX = {"Ardle Vale": (440000, 456000), "Brindham": (456000, 470000), "Kestermoor": (470000, 486000)}


def district_of(e):
    for d, (lo, hi) in DISTRICT_BOX.items():
        if lo <= e < hi:
            return d
    return "Kestermoor"


def is_trunk(road, easting, boundary=None):
    if road == "A6510":
        return True
    if road == "A4600":
        return easting < boundary
    return False


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)            # the network
        self.rc = np.random.default_rng(seed + 1)         # the junctions' collision counts
        self.rr = np.random.default_rng(seed + 2)         # the records' details
        self.rp = np.random.default_rng(seed + 3)         # the 2026 provisional data
        self.junctions = []
        self._network()
        a46 = sorted((j for j in self.junctions if j["road"] == "A4600"), key=lambda j: abs(j["easting"] - 470000))
        self.boundary_node = a46[0]
        self.trunk_boundary = a46[0]["easting"]
        self._counts()
        self.collisions = []
        self._records()
        self.prov = []
        self._provisional()

    # ---------------- network
    def _network(self):
        rng = self.rng
        jid = 100
        used = set()
        layouts = []
        for lay, n in P.N_LAYOUT.items():
            layouts += [lay] * n
        order = rng.permutation(len(layouts))
        for k in order:
            lay = layouts[k]
            jid += int(rng.integers(1, 6))
            e = int(rng.integers(441000, 485000))
            n_ = int(rng.integers(291000, 329000))
            if lay in ("RB", "SIG"):
                maj = float(np.exp(rng.normal(np.log(11000), 0.45)))
            else:
                maj = float(np.exp(rng.normal(np.log(6300), 0.55)))
            maj = min(max(maj, 1400.0), 29000.0)
            mmed = {"T": 900, "ST": 1000, "X": 1250}.get(lay, 2600)
            mnr = min(max(float(np.exp(rng.normal(np.log(mmed), 0.65))), 140.0), 0.72 * maj)
            if maj >= 7500 or lay in ("RB", "SIG"):
                road = A_ROADS[int(rng.integers(0, len(A_ROADS)))]
            else:
                road = B_ROADS[int(rng.integers(0, len(B_ROADS)))] if rng.random() < 0.6 else (
                    "C%d" % int(rng.integers(101, 399)), MINOR_NAMES[int(rng.integers(0, len(MINOR_NAMES)))])
            minor = MINOR_NAMES[int(rng.integers(0, len(MINOR_NAMES)))]
            name = "%s / %s" % (road[1], minor)
            tries = 0
            while (name in used or minor == road[1]) and tries < 200:
                minor = MINOR_NAMES[int(rng.integers(0, len(MINOR_NAMES)))]
                name = "%s / %s" % (road[1], minor)
                tries += 1
            if name in used:
                name = "%s (%s) / %s" % (road[1], road[0], minor)
                k2 = 2
                while name in used:
                    name = "%s (%s) / %s %d" % (road[1], road[0], minor, k2)
                    k2 += 1
            used.add(name)
            ctrl = {"RB": "RBT", "MR": "RBT", "SIG": "SIG"}.get(lay, "STOP" if rng.random() < 0.12 else "GW")
            growth = np.cumprod(np.r_[1.0, 1 + rng.normal(0.007, 0.010, len(P.YEARS) - 1)])
            growth = growth / growth[P.YEARS.index(P.PRESENT)]
            self.junctions.append(dict(node="J%04d" % jid, name=name, layout=lay, control=ctrl, road=road[0],
                                       road_name=road[1], minor=minor, easting=e, northing=n_, district=district_of(e),
                                       maj=maj * growth, mnr=mnr * growth * (1 + rng.normal(0, 0.01)),
                                       theta=float(rng.gamma(1 / P.K_TRUE, P.K_TRUE)), cand=None))
        # the six screened junctions
        for (name, dist, lay, ctrl, major, minor, maj26, mnr26, theta, rec) in P.CANDIDATES:
            jid += int(rng.integers(1, 6))
            lo, hi = DISTRICT_BOX[dist]
            e = int(rng.integers(lo + 1500, hi - 1500))
            n_ = int(rng.integers(293000, 327000))
            growth = np.cumprod(np.r_[1.0, 1 + rng.normal(0.007, 0.006, len(P.YEARS) - 1)])
            growth = growth / growth[P.YEARS.index(P.PRESENT)]
            road_no, road_name = major.split(" ", 1)
            mgrowth = growth.copy()
            if name in P.MINOR_STEP:
                # a traffic regulation order on the minor road took part of its through traffic from the year given
                yr, keep = P.MINOR_STEP[name]
                mgrowth = np.array([g / keep if y < yr else g for y, g in zip(P.YEARS, growth)])
            self.junctions.append(dict(node="J%04d" % jid, name=name, layout=lay, control=ctrl, road=road_no,
                                       road_name=road_name, minor=minor, easting=e, northing=n_, district=dist,
                                       maj=maj26 * growth, mnr=mnr26 * mgrowth, theta=theta, cand=name, rec=list(rec)))
        # node numbers follow the inventory's own order (the 2019 recode numbered nodes along each road), with the
        # pre-2019 numbers kept beside them; neither tracks the screening
        order = sorted(range(len(self.junctions)), key=lambda i: (self.junctions[i]["road"], self.junctions[i]["easting"]))
        nid = 1000
        olds = rng.choice(np.arange(2000, 9999), size=len(self.junctions), replace=False)
        for k, i in enumerate(order):
            nid += int(rng.integers(1, 8))
            self.junctions[i]["node"] = "J%04d" % nid
            self.junctions[i]["former"] = "N%05d" % int(olds[k])

    def mu(self, j, year):
        b0, b1, b2 = P.SPF[j["layout"]]
        t = P.YEARS.index(year)
        return float(np.exp(b0 + b1 * np.log(j["maj"][t]) + b2 * np.log(j["mnr"][t]))) * P.YEAR_FACTOR[year]

    def _counts(self):
        rng = self.rc
        win = P.WINDOW
        for j in self.junctions:
            for attempt in range(60):
                n = {y: int(rng.poisson(self.mu(j, y) * j["theta"])) for y in P.REC_YEARS + [2026]}
                if j["cand"]:
                    for y, c in zip(win, j["rec"]):
                        n[y] = c
                    break
                ref = j["layout"] in ("T", "ST", "X")
                if not ref or sum(n[y] for y in win) < P.SCREEN_MIN or not getattr(P, "REDRAW_TAIL", True):
                    break
                j["theta"] = float(rng.gamma(1 / P.K_TRUE, P.K_TRUE))
            j["n"] = n
        if getattr(P, "STEADY_YEARS", True):
            self._steady_years()

    def _steady_years(self):
        """The network's give-way junction collisions held near the window's year-on-year level: a few collisions
        moved between years within background junctions so 2022 to 2025 run level and 2021 at its lower level."""
        rng = self.rc
        ref = [j for j in self.reference() if not j["cand"]]
        win = P.WINDOW
        f = {y: P.YEAR_FACTOR[y] for y in win}
        for _ in range(4000):
            tot = {y: sum(j["n"][y] for j in self.reference()) for y in win}
            all_ = sum(tot.values())
            target = {y: all_ * f[y] / sum(f.values()) for y in win}
            gap = {y: tot[y] - target[y] for y in win}
            hi = max(win, key=lambda y: gap[y])
            lo = min(win, key=lambda y: gap[y])
            if gap[hi] < 1.5 and gap[lo] > -1.5:
                break
            pool = [j for j in ref if j["n"][hi] > 0]
            j = pool[int(rng.integers(0, len(pool)))]
            j["n"][hi] -= 1
            j["n"][lo] += 1

    def reference(self):
        """Give-way or stop-controlled T, staggered and crossroads junctions: the screening's population."""
        return [j for j in self.junctions if j["layout"] in ("T", "ST", "X") and j["control"] in ("GW", "STOP")]

    def candidates(self):
        return [j for j in self.junctions if j["cand"]]

    # ---------------- validated collision records 2016 to 2025
    def _when(self, year):
        rng = self.rr
        start = dt.date(year, 1, 1)
        days = (dt.date(year + 1, 1, 1) - start).days
        d = start + dt.timedelta(days=int(rng.integers(0, days)))
        hour = int(rng.choice(np.arange(24), p=HOUR_P))
        return d, hour, int(rng.integers(0, 60))

    def _severity(self):
        r = self.rr.random()
        return 1 if r < P.SEVERITY_SHARE[0] else (2 if r < P.SEVERITY_SHARE[0] + P.SEVERITY_SHARE[1] else 3)

    def _records(self):
        rng = self.rr
        recs = []
        for j in self.junctions:
            for y in P.REC_YEARS:
                for _ in range(j["n"][y]):
                    d, h, m = self._when(y)
                    recs.append(self._collision(d, h, m, j=j))
        for y in P.REC_YEARS:
            nl = int(rng.poisson(P.LINK_COLLISIONS * P.YEAR_FACTOR[y]))
            for _ in range(nl):
                d, h, m = self._when(y)
                recs.append(self._collision(d, h, m, j=None))
        recs.sort(key=lambda r: (r["date"], r["hour"], r["minute"], r["easting"]))
        seq = defaultdict(int)
        for r in recs:
            y = r["date"].year
            seq[y] += int(rng.integers(1, 4))
            r["ref"] = ("AR/%02d/%06d" % (y % 100, 4000 + seq[y] * 7)) if y < 2020 else ("%d/47/%07d" % (y, 1200 + seq[y] * 5))
        self.collisions = recs

    def _collision(self, d, h, m, j=None):
        rng = self.rr
        if j is not None:
            e = j["easting"] + int(rng.integers(-14, 15))
            n_ = j["northing"] + int(rng.integers(-14, 15))
            road1, road2 = j["road"], (j["minor"] if not j["minor"].startswith("B") else j["minor"].split(" ")[0])
            jd = {"T": 3, "ST": 3, "X": 6, "MR": 2, "RB": 1, "SIG": 6}[j["layout"]]
            jc = {"GW": 4, "STOP": 3, "SIG": 2, "RBT": 4}[j["control"]]
            speed = 30 if j["maj"][-1] < 8000 and rng.random() < 0.6 else int(rng.choice([40, 50, 60]))
        else:
            e = int(rng.integers(441000, 485000))
            n_ = int(rng.integers(291000, 329000))
            rr = A_ROADS + B_ROADS
            road1 = rr[int(rng.integers(0, len(rr)))][0] if rng.random() < 0.7 else "U"
            road2 = ""
            jd = int(rng.choice([0, 3, 6, 8, 9], p=[0.56, 0.24, 0.08, 0.07, 0.05]))
            jc = 0 if jd == 0 else int(rng.choice([4, 3, 2], p=[0.86, 0.06, 0.08]))
            if jd:
                road2 = "U" if rng.random() < 0.7 else "C%d" % int(rng.integers(101, 399))
            speed = int(rng.choice([20, 30, 30, 30, 40, 50, 60, 60, 70]))
        vehicles = int(rng.choice([1, 2, 3, 4], p=[0.28, 0.5, 0.17, 0.05]))
        cas = 1 + int(rng.poisson(0.32))
        return dict(date=d, hour=h, minute=m, easting=e, northing=n_, road1=road1, road2=road2, jd=jd, jc=jc,
                    severity=self._severity(), vehicles=vehicles, casualties=cas, speed=speed,
                    light=int(rng.choice([1, 4, 6], p=[0.72, 0.2, 0.08])), weather=int(rng.choice([1, 2, 3, 8], p=[0.8, 0.13, 0.02, 0.05])),
                    surface=int(rng.choice([1, 2, 4], p=[0.7, 0.27, 0.03])), node=(j["node"] if j else ""),
                    former=(j["former"] if j else ""), district=district_of(e))

    # ---------------- 2026 provisional data (the annex asks)
    def _provisional(self):
        """The county's provisional 2026 collisions January to September, each with its casualties and vehicles and
        the true severity on the national 30-day definition. Trunk-road collisions are in the police data too."""
        rng = self.rp
        out = []
        d0 = P.PROV_START
        days = (P.PROV_END - d0).days + 1
        n = int(rng.poisson(2050))
        for i in range(n):
            d = d0 + dt.timedelta(days=int(rng.integers(0, days)))
            hour = int(rng.choice(np.arange(24), p=HOUR_P))
            minute = int(rng.integers(0, 60))
            rr = A_ROADS + B_ROADS
            if rng.random() < 0.09:
                road = "A4600" if rng.random() < 0.7 else "A6510"
                e = int(rng.integers(452000, 486000)) if road == "A4600" else int(rng.integers(441000, 470000))
            else:
                rr = [r for r in rr if r[0] not in TRUNK]
                road = rr[int(rng.integers(0, len(rr)))][0] if rng.random() < 0.72 else "U"
                e = int(rng.integers(441000, 485000))
            nn = int(rng.integers(291000, 329000))
            nveh = int(rng.choice([1, 2, 3, 4], p=[0.27, 0.55, 0.14, 0.04]))
            vehicles = []
            for v in range(1, nveh + 1):
                vt = str(rng.choice(VTYPES, p=VTYPE_P))
                vehicles.append(dict(ref=v, type=vt))
            cas = []
            struck = [v for v in vehicles if v["type"] in ("Car", "Taxi or private hire car", "Van or light goods")]
            if struck and rng.random() < 0.16:
                cas.append(dict(cls="Pedestrian", vehicle=struck[0]["ref"], age=int(rng.integers(5, 90)),
                                sex=str(rng.choice(["Male", "Female"]))))
                n_occ = int(rng.poisson(0.25))
            else:
                n_occ = 1 + int(rng.poisson(0.3))
            for _ in range(n_occ):
                v = vehicles[int(rng.integers(0, len(vehicles)))]
                solo = v["type"] in ("Pedal cycle", "E-scooter")
                cls = "Driver or rider" if (solo or rng.random() < 0.72) else "Passenger"
                cas.append(dict(cls=cls, vehicle=v["ref"], age=int(rng.integers(16, 88)), sex=str(rng.choice(["Male", "Female"]))))
            for c in cas:
                r = rng.random()
                c["sev"] = 1 if r < 0.012 else (2 if r < 0.22 else 3)
                c["recorded"] = c["sev"]
            out.append(dict(date=d, hour=hour, minute=minute, road=road, easting=e, northing=nn, vehicles=vehicles,
                            casualties=cas, trunk=is_trunk(road, e, self.trunk_boundary), district=district_of(e)))
        # deaths within 30 days that came after the police record was made (serious in the police data), two serious
        # casualties who died after 30 days (not killed on the national definition), and one 30-day death on a trunk road
        late = [c for c in out if not c["trunk"] and any(k["sev"] == 2 for k in c["casualties"])]
        pick = sorted(int(x) for x in rng.choice(len(late), size=11, replace=False))
        for k, i in enumerate(pick):
            cas = [x for x in late[i]["casualties"] if x["sev"] == 2][0]
            if k < 9:
                cas["sev"] = 1
                cas["died_day"] = int(rng.integers(3, 29))
            else:
                cas["died_day"] = int(rng.integers(34, 61))
        trunk = [c for c in out if c["trunk"] and any(k["sev"] == 2 for k in c["casualties"])]
        cas = [x for x in trunk[int(rng.integers(0, len(trunk)))]["casualties"] if x["sev"] == 2][0]
        cas["sev"] = 1
        cas["died_day"] = int(rng.integers(3, 25))
        for c in out:
            for k in c["casualties"]:
                if k["recorded"] == 1:
                    k["died_day"] = int(rng.integers(0, 3))
        # collisions before the migration that were amended after it and re-sent under the new system's references
        pre = [c for c in out if c["date"] < P.MIGRATION]
        for c in pre:
            worst = min(k["recorded"] for k in c["casualties"])
            # fatal and serious files stay open longest (investigations, inquests), so more of them were amended
            # after the new system went live and came across under its references
            if rng.random() >= {1: 0.45, 2: 0.12, 3: 0.05}[worst]:
                continue
            c["resent"] = dict(dmin=int(rng.choice([0, 0, 0, 2, 5, 9, 14])), de=int(rng.integers(-22, 23)),
                               dn=int(rng.integers(-22, 23)), sev_change=bool(rng.random() < 0.18))
            if c["resent"]["sev_change"]:
                worst = min(c["casualties"], key=lambda k: k["sev"])
                if worst["sev"] == 2 and worst["recorded"] == 2:
                    worst["recorded"] = 3          # first submitted as slight, reclassified serious on amendment
                else:
                    c["resent"]["sev_change"] = False
        out.sort(key=lambda c: (c["date"], c["hour"], c["minute"], c["easting"]))
        self.prov = out

    def prov_truth(self):
        """Ask A: collisions on the county's roads by quarter of the collision and 30-day severity; ask B: casualties by
        road user group and quarter (pedestrian, pedal cyclist, motorcyclist, car occupant)."""
        a = defaultdict(int)
        b = defaultdict(int)
        for c in self.prov:
            if c["trunk"]:
                continue
            q = (c["date"].month - 1) // 3 + 1
            sev = min(k["sev"] for k in c["casualties"])
            a[(q, sev)] += 1
            vt = {v["ref"]: v["type"] for v in c["vehicles"]}
            for k in c["casualties"]:
                g = road_user(k["cls"], vt[k["vehicle"]])
                if g:
                    b[(q, g)] += 1
        return dict(a), dict(b)


VTYPES = ["Car", "Taxi or private hire car", "Van or light goods", "Goods 7.5 tonnes and over", "Bus or coach",
          "Motorcycle 125cc and under", "Motorcycle over 500cc", "Motorcycle 125cc to 500cc", "Pedal cycle", "E-scooter",
          "Agricultural vehicle", "Other"]
VTYPE_P = [0.62, 0.03, 0.09, 0.03, 0.02, 0.035, 0.035, 0.02, 0.08, 0.015, 0.01, 0.015]
GROUP = {"Car": "Car occupant", "Taxi or private hire car": "Car occupant", "Pedal cycle": "Pedal cyclist",
         "Motorcycle 125cc and under": "Motorcyclist", "Motorcycle 125cc to 500cc": "Motorcyclist",
         "Motorcycle over 500cc": "Motorcyclist"}
GROUPS = ["Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"]
_h = np.array([0.6, 0.4, 0.3, 0.3, 0.4, 0.9, 2.2, 4.6, 6.4, 4.9, 4.6, 5.0, 5.6, 5.6, 5.9, 7.2, 8.4, 8.6, 7.0, 5.0,
               3.6, 2.8, 2.0, 1.2])
HOUR_P = _h / _h.sum()


def road_user(cls, vtype):
    if cls == "Pedestrian":
        return "Pedestrian"
    return GROUP.get(vtype)
