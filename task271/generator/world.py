"""The world before any export is written: every residential parcel in the seven townships with its dwelling and
water zone, the homes Halverstead Mutual insured over 2023 to 2025 with their policy terms, every claim by peril
with its payments, and the authority's hydrants with their flow tests. Nothing here is mess; records.py writes the
exports the systems produce."""
import datetime as dt
import math

import numpy as np

import common as K
import geo

D0 = dt.date(2022, 1, 1)


def day(d):
    return (d - D0).days


def date(n):
    return D0 + dt.timedelta(int(n))


# per township: residential parcels, owner-occupied single-family share, Valley share of homes, year-built
# profile (low, high, skew), basement share, the mutual's share of owner-occupied single-family homes
PROFILE = {
    "WYV": dict(n=13800, sfd_oo=0.68, valley=0.44, yb=(1895, 2024, 0.75), bsmt=0.63, insured=0.62),
    "HLT": dict(n=12600, sfd_oo=0.71, valley=0.28, yb=(1895, 2024, 0.85), bsmt=0.62, insured=0.60),
    "VRN": dict(n=10400, sfd_oo=0.73, valley=0.05, yb=(1895, 2024, 0.90), bsmt=0.61, insured=0.61),
    "MRV": dict(n=9600, sfd_oo=0.70, valley=0.25, yb=(1895, 2024, 0.85), bsmt=0.63, insured=0.60),
    "DOR": dict(n=3900, sfd_oo=0.71, valley=0.06, yb=(1895, 2024, 0.80), bsmt=0.90, insured=0.0),
    "BRK": dict(n=3400, sfd_oo=0.76, valley=0.86, yb=(1895, 2024, 0.90), bsmt=0.16, insured=0.0),
    "SAL": dict(n=4300, sfd_oo=0.72, valley=0.40, yb=(1895, 2024, 0.85), bsmt=0.55, insured=0.0),
}
LAND_USE_OTHER = [("R-TWN", 0.34), ("R-DUP", 0.18), ("R-MH", 0.10), ("R-APT", 0.06), ("R-SFD", 0.32)]


class World:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.zoner = geo.Zoner()
        self.parcels = []      # dicts
        self.homes = {}        # parcel_id -> home dict (owner-occupied single-family detached)
        self._parcels()
        self.hydrants = []
        self._hydrants(np.random.default_rng(seed + 101))
        self._protection()
        self.book = []         # insured homes: dict with parcel_id, policy_no, terms
        self.terms = []
        self._book()
        self.claims = []
        self._claims(np.random.default_rng(seed + 202), np.random.default_rng(seed + 303))

    # ---- parcels and dwellings
    def _parcels(self):
        rng = self.rng
        seq = 0
        for town, _, _ in K.TOWNS:
            p = PROFILE[town]
            n_sfd = int(round(p["n"] * p["sfd_oo"]))
            pts = geo.place(rng, self.zoner, town, p["n"], p["valley"] * 0.96 + 0.02,
                            other_zones=["PZ-2"])
            for i, (x, y, z) in enumerate(pts):
                seq += 1
                lo, hi, sk = p["yb"]
                yb = int(lo + (hi - lo) * rng.beta(1.4 * sk, 1.4))
                oo_sfd = i < n_sfd
                if oo_sfd:
                    lu, homestead = "R-SFD", "Y"
                else:
                    lu = rng.choice([a for a, _ in LAND_USE_OTHER], p=[b for _, b in LAND_USE_OTHER])
                    homestead = "N" if lu == "R-SFD" else rng.choice(["Y", "N"], p=[0.45, 0.55])
                bsmt = rng.random() < p["bsmt"]
                if bsmt:
                    found = "BSMT FULL" if rng.random() < 0.78 else "BSMT PART"
                else:
                    found = "SLAB" if (town == "BRK" or rng.random() < 0.55) else rng.choice(["CRAWL", "PIERS"],
                                                                                          p=[0.85, 0.15])
                area = int(np.clip(rng.lognormal(math.log(1750 if yb < 1990 else 2250), 0.28), 760, 6200))
                full = int(np.clip(round(area / 900 + rng.normal(0, 0.55)), 1, 5))
                half = int(rng.random() < (0.55 if area > 1800 else 0.25))
                stories = rng.choice([1.0, 1.5, 2.0], p=[0.38, 0.17, 0.45])
                wall = rng.choice(["FRAME", "BRICK VENEER", "MASONRY", "STONE"], p=[0.58, 0.24, 0.13, 0.05])
                land = int(rng.lognormal(math.log(48000), 0.35))
                bldg = int(area * rng.lognormal(math.log(118.0 if yb < 1990 else 146.0), 0.18))
                pid = "%02d-%03d-%04d" % (K.CANDIDATES.index(town) + 31 if town in K.CANDIDATES else
                                          K.BOOK_TOWNS.index(town) + 11, (seq // 1000) % 1000, seq % 10000)
                rec = dict(parcel_id=pid, town=town, x=x, y=y, zone=z, land_use=lu, homestead=homestead,
                           year_built=yb, foundation=found, basement=bsmt, area=area, full=full, half=half,
                           stories=float(stories), wall=wall, land=land, bldg=bldg)
                self.parcels.append(rec)
                if oo_sfd:
                    self.homes[pid] = rec

    # ---- the mutual's book
    def true_rate(self, h):
        return K.BASE_RATE * (K.BASEMENT_FACTOR if h["basement"] else 1.0) * K.ZONE_FACTOR[h["zone"]]

    def _book(self):
        rng = self.rng
        pno = 410000
        for town in K.BOOK_TOWNS:
            homes = [h for h in self.homes.values() if h["town"] == town]
            k = int(round(len(homes) * PROFILE[town]["insured"]))
            pick = rng.choice(len(homes), size=k, replace=False)
            for j in sorted(pick):
                h = homes[j]
                pno += int(rng.integers(1, 4))
                anniv = int(rng.integers(0, 365))            # day of 2022 the policy renews on
                first = date(anniv)
                kind = rng.random()
                start, end = first, None
                if kind < 0.10:                                # new business during 2023 to 2025
                    start = date(int(rng.integers(365, 365 * 4 - 30)))
                    anniv = (start - dt.date(start.year, 1, 1)).days
                lo = max(day(start) + 40, 365)
                if rng.random() < 0.085 and lo < 365 * 4 - 1:   # sold or cancelled during 2023 to 2025
                    end = date(int(rng.integers(lo, 365 * 4)))
                ded = int(rng.choice([500, 1000, 2500], p=[0.22, 0.58, 0.20]))
                cov = int(round(h["area"] * rng.normal(214, 14) / 1000.0)) * 1000
                b = dict(parcel_id=h["parcel_id"], policy_no="HM%d" % pno, start=start, end=end, deductible=ded,
                         coverage_a=cov, home=h)
                self.book.append(b)
                t0 = start
                n = 0
                while t0 <= K.EXPERIENCE[1]:
                    t1 = dt.date(t0.year + 1, t0.month, min(t0.day, 28)) if (t0.month, t0.day) == (2, 29) else \
                        dt.date(t0.year + 1, t0.month, t0.day)
                    n += 1
                    stop = end if (end is not None and t0 <= end < t1) else None
                    if t1 > K.EXPERIENCE[0]:
                        cov = int(round(cov * rng.normal(1.045, 0.006) / 1000.0)) * 1000 if n > 1 else cov
                        self.terms.append(dict(policy_no=b["policy_no"], term=n, start=t0, end=t1, cancel=stop,
                                               deductible=ded, coverage_a=cov, home=h))
                    if stop is not None:
                        break
                    t0 = t1

    def exposure(self, term, year):
        """house-years the term earned in the calendar year"""
        a = max(term["start"], dt.date(year, 1, 1))
        b = min(term["cancel"] or term["end"], dt.date(year + 1, 1, 1))
        return max(0, (b - a).days) / (366.0 if year == 2024 else 365.0)

    # ---- claims, every peril
    def _claims(self, rw, ro):
        """non-weather water claims from their own stream (rw), every other peril from another (ro), so the water
        record does not move when another peril's process is changed"""
        cats = [(dt.date(2023, 6, 27), 0.020), (dt.date(2024, 5, 9), 0.016), (dt.date(2025, 7, 30), 0.012)]
        cold = sorted({dt.date(2023, 2, 3), dt.date(2023, 2, 4), dt.date(2024, 1, 16), dt.date(2024, 1, 17),
                       dt.date(2024, 1, 21), dt.date(2025, 1, 21), dt.date(2025, 1, 22), dt.date(2025, 2, 19)})
        for t in self.terms:
            h = t["home"]
            a = max(t["start"], K.EXPERIENCE[0])
            b = min(t["cancel"] or t["end"], dt.date(2026, 1, 1))
            span = (b - a).days
            if span <= 0:
                continue
            yrs = span / 365.25
            # non-weather water: the zone's supply pressure and the basement
            for _ in range(rw.poisson(self.true_rate(h) * yrs)):
                self._claim(rw, t, a + dt.timedelta(int(rw.integers(0, span))),
                            str(rw.choice(["PLUMB", "APPL"], p=[0.64, 0.36])))
            # freezing: cold snaps, no zone effect
            for c in cold:
                if a <= c < b and ro.random() < (0.0022 if h["basement"] else 0.0012):
                    self._claim(ro, t, c + dt.timedelta(int(ro.integers(0, 3))), "FREEZE")
            for kind, rate in (("BACKUP", 0.0026), ("SEEPAGE", 0.0019), ("THEFT", 0.0021), ("LIAB", 0.0012),
                               ("OTHER", 0.0030)):
                for _ in range(ro.poisson(rate * yrs)):
                    self._claim(ro, t, a + dt.timedelta(int(ro.integers(0, span))), kind)
            fire = 0.0019 * (1.0 if h["protected"] else 2.4)
            for _ in range(ro.poisson(fire * yrs)):
                self._claim(ro, t, a + dt.timedelta(int(ro.integers(0, span))), "FIRE")
            for _ in range(ro.poisson(0.0052 * yrs)):
                self._claim(ro, t, a + dt.timedelta(int(ro.integers(0, span))), "WIND")
            for d, p in cats:
                if a <= d < b and ro.random() < p * (1.4 if h["town"] in ("WYV", "MRV") else 1.0):
                    self._claim(ro, t, d, "HAIL")

    def _claim(self, rng, t, loss, kind):
        if loss > K.EXPERIENCE[1]:
            return
        lag = int(rng.choice([rng.integers(0, 6), rng.integers(6, 45), rng.integers(45, 240)], p=[0.70, 0.25, 0.05]))
        rep = loss + dt.timedelta(lag)
        sev = {"PLUMB": (9.05, 0.95), "APPL": (8.75, 0.85), "FREEZE": (9.25, 0.9), "BACKUP": (8.6, 0.8),
               "SEEPAGE": (8.4, 0.7), "THEFT": (8.1, 0.9), "LIAB": (9.4, 1.1), "OTHER": (7.9, 0.9),
               "FIRE": (10.4, 1.2), "WIND": (8.6, 0.8), "HAIL": (9.3, 0.6)}[kind]
        loss_amt = float(np.exp(rng.normal(*sev)))
        self.claims.append(dict(policy_no=t["policy_no"], term=t["term"], parcel_id=t["home"]["parcel_id"], kind=kind,
                                loss=loss, reported=rep, amount=round(loss_amt, 2), deductible=t["deductible"],
                                home=t["home"]))

    # ---- the authority's hydrants, their flow tests and the guide's protection test
    def _hydrants(self, rng):
        """hydrants stand on the mains of the hydranted neighbourhoods (cells of about 2,400 feet); outlying lanes are
        served by small mains without hydrants"""
        cells = {}
        for p in self.parcels:
            cells.setdefault((int(p["x"] // 2400), int(p["y"] // 2400)), []).append(p)
        sel = []
        for key in sorted(cells):
            ps = cells[key]
            if rng.random() < (0.80 if len(ps) > 25 else 0.45):
                k = max(1, int(round(len(ps) / rng.uniform(11, 16))))
                sel += [ps[i] for i in rng.choice(len(ps), size=min(k, len(ps)), replace=False)]
        for p in sel:
            x, y = p["x"] + rng.normal(0, 220), p["y"] + rng.normal(0, 220)
            z = self.zoner.zone(x, y)
            if z is None:
                continue
            lo, hi = K.psi_range([q for q in K.ZONES if q[0] == z][0])
            h = dict(n=len(self.hydrants), x=round(x, 1), y=round(y, 1), zone=z,
                     static=float(rng.uniform(lo + 2, hi - 2)), main=int(rng.choice([4, 6, 8, 12],
                                                                                    p=[0.22, 0.50, 0.21, 0.07])),
                     installed=int(rng.integers(1958, 2026)), town=p["town"],
                     status=str(rng.choice(["IN SERVICE", "OUT OF SERVICE", "ABANDONED"], p=[0.952, 0.033, 0.015])),
                     owner="PRIVATE" if rng.random() < 0.04 else "TCWA")
            # flow tests on a five-year cycle, some retested after a main replacement or a complaint
            first = int(rng.integers(2018, 2023))
            years = [first] + ([first + 5] if first + 5 <= 2026 else [])
            if rng.random() < 0.18:
                years.append(int(rng.integers(2024, 2027)))
            boost, tests = 1.0, []
            for k, yv in enumerate(sorted(set(v for v in years if v >= max(2018, h["installed"])))):
                d = dt.date(yv, int(rng.integers(4, 11)), int(rng.integers(1, 29)))
                if d > K.HYDRANT_DATE:
                    continue
                if k > 0 and rng.random() < 0.35:
                    boost *= rng.uniform(1.15, 1.6)
                static = int(round(h["static"] + rng.normal(0, 2)))
                cap = {4: 430, 6: 760, 8: 1500, 12: 2700}[h["main"]] * boost * rng.lognormal(0, 0.25)
                resid = int(round(static * rng.uniform(0.45, 0.82)))
                flow = int(round(cap * ((static - resid) / max(static - 20.0, 5.0)) ** 0.54))
                tests.append(dict(date=d, static=static, resid=resid, flow=flow,
                                  crew=str(rng.choice(["TCWA CREW 2", "TCWA CREW 4", "ALDERSON FIRE PROTECTION"],
                                                      p=[0.45, 0.4, 0.15]))))
            h["tests"] = tests
            self.hydrants.append(h)

    @staticmethod
    def q20(t):
        """flow available at 20 psi residual from a flow test (NFPA 291)"""
        return t["flow"] * ((t["static"] - 20.0) / (t["static"] - t["resid"])) ** 0.54

    def _protection(self):
        """the guide's test: an in-service authority hydrant within 1,000 feet whose latest test shows 500 gpm
        available at 20 psi"""
        from scipy.spatial import cKDTree
        good = [h for h in self.hydrants if h["status"] == "IN SERVICE" and h["owner"] == "TCWA" and h["tests"]
                and self.q20(max(h["tests"], key=lambda t: t["date"])) >= 500]
        tree = cKDTree(np.array([[h["x"], h["y"]] for h in good]))
        for p in self.parcels:
            dd, _ = tree.query([p["x"], p["y"]])
            p["protected"] = bool(dd <= 1000.0)
