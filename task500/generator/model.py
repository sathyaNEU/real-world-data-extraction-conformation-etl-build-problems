"""The state's lodging filers and their monthly taxable receipts, generated forward from each property's own demand.

Every property has a business-travel dependence that no register column carries; it sets the shape of the property's
year (business stays fall away in July and December, leisure stays peak in summer) and it sets how hard the fiscal 2026
business-travel slump hits it. The changes of each year act only on the filers they touch: the convention center
closure takes a small share of downtown receipts while it is shut, the long-stay exemption takes long-stay receipts at
extended-stay hotels out of the base, the county option cut changes the rate, platform collection moves short-term
rental receipts onto the facilitators' returns, and the airline hub reduction trims the airport hotels."""
import datetime as dt

import numpy as np

import world as W

BUSINESS = np.array([0.80, 0.84, 1.08, 1.13, 1.04, 0.76, 0.92, 1.01, 1.09, 1.09, 1.07, 0.97])   # Jul..Jun
LEISURE = {
    "default": np.array([1.56, 1.50, 1.05, 0.98, 0.70, 0.76, 0.63, 0.70, 0.84, 0.90, 1.10, 1.38]),
    "North Woods": np.array([1.58, 1.52, 1.12, 1.26, 0.58, 0.82, 0.86, 0.86, 0.64, 0.55, 0.90, 1.31]),
    "Hill Country": np.array([1.40, 1.36, 1.10, 1.18, 0.86, 0.80, 0.62, 0.70, 0.90, 1.00, 1.12, 1.26]),
}
for k in LEISURE:
    LEISURE[k] = LEISURE[k] / LEISURE[k].mean()
BUSINESS = BUSINESS / BUSINESS.mean()

# filers by region and class: (count, rooms range, business dependence range, ADR)
LAYOUT = {
    "Capital City Downtown": {"FS": (24, (220, 720), (0.80, 0.93), 185), "LS": (18, (80, 190), (0.74, 0.90), 128),
                              "BB": (4, (6, 14), (0.25, 0.45), 160), "STR": (24, (1, 3), (0.2, 0.5), 150)},
    "Capital City North": {"FS": (12, (140, 420), (0.40, 0.70), 150), "LS": (30, (70, 180), (0.40, 0.80), 112),
                           "ES": (10, (90, 150), (0.60, 0.82), 104), "MO": (10, (30, 70), (0.30, 0.55), 76),
                           "BB": (6, (5, 12), (0.20, 0.40), 140), "STR": (40, (1, 3), (0.15, 0.45), 130)},
    "Lakeshore": {"FS": (16, (150, 520), (0.08, 0.28), 210), "LS": (50, (60, 160), (0.20, 0.55), 118),
                  "ES": (8, (80, 130), (0.55, 0.75), 102), "MO": (40, (25, 60), (0.10, 0.35), 88),
                  "BB": (40, (4, 12), (0.05, 0.25), 165), "CG": (20, (40, 160), (0.0, 0.05), 46),
                  "STR": (140, (1, 4), (0.05, 0.25), 175)},
    "North Woods": {"FS": (6, (90, 220), (0.06, 0.20), 170), "LS": (30, (50, 130), (0.25, 0.60), 102),
                    "MO": (60, (20, 50), (0.15, 0.50), 72), "BB": (30, (4, 10), (0.05, 0.25), 150),
                    "CG": (25, (40, 140), (0.0, 0.05), 40), "STR": (100, (1, 4), (0.05, 0.20), 160)},
    "River Valley": {"FS": (14, (120, 360), (0.55, 0.92), 150), "LS": (70, (60, 170), (0.35, 0.92), 110),
                     "ES": (20, (80, 160), (0.62, 0.88), 100), "MO": (30, (25, 60), (0.25, 0.60), 74),
                     "BB": (15, (4, 10), (0.10, 0.30), 135), "STR": (30, (1, 3), (0.10, 0.35), 120)},
    "Airport Corridor": {"FS": (8, (150, 380), (0.72, 0.90), 150), "LS": (30, (80, 180), (0.65, 0.90), 116),
                         "MO": (6, (30, 60), (0.40, 0.60), 80), "STR": (5, (1, 2), (0.20, 0.40), 110)},
    "Southern Plains": {"FS": (6, (100, 260), (0.45, 0.85), 135), "LS": (45, (50, 140), (0.35, 0.90), 98),
                        "ES": (14, (70, 140), (0.60, 0.88), 94), "MO": (40, (20, 50), (0.25, 0.60), 68),
                        "BB": (10, (4, 10), (0.10, 0.30), 120), "STR": (20, (1, 3), (0.10, 0.30), 105)},
    "Hill Country": {"FS": (10, (120, 400), (0.06, 0.25), 220), "LS": (30, (50, 140), (0.15, 0.55), 108),
                     "ES": (8, (70, 120), (0.55, 0.75), 98), "MO": (30, (20, 50), (0.10, 0.40), 78),
                     "BB": (30, (4, 12), (0.05, 0.20), 175), "CG": (15, (40, 140), (0.0, 0.05), 48),
                     "STR": (80, (1, 4), (0.05, 0.20), 185)},
}
OCC = {"FS": 0.70, "LS": 0.68, "ES": 0.78, "MO": 0.55, "BB": 0.52, "CG": 0.45, "STR": 0.48}

P = dict(slump=0.235, slump_power=2.0, closure=0.055, exemption=0.40, airline=0.05, platform_gain=0.04,
         highway=0.16, stadium=0.17, growth=0.03, growth_sd=0.025, month_sd=0.035, new_openings=9,
         renovations=40)


def county_for(region, rng):
    counties = [c for c, r in W.COUNTIES.items() if r == region]
    return counties[int(rng.integers(0, len(counties)))]


class State:
    def __init__(self, params=None, seed=W.SEED):
        self.p = dict(P)
        if params:
            self.p.update(params)
        self.seed = seed

    # ------------------------------------------------------------------ the register
    def filers(self):
        rng = np.random.default_rng([self.seed, 31])
        ids = rng.permutation(np.arange(100000, 999999, 37))
        out, k = [], 0
        for region, classes in LAYOUT.items():
            for cls, (n, rooms, brange, adr) in classes.items():
                for _ in range(n):
                    f = dict(filer_id="LT%06d" % ids[k], region=region, cls=cls,
                             rooms=int(rng.integers(rooms[0], rooms[1] + 1)),
                             b=float(rng.uniform(*brange)), adr=adr * float(rng.uniform(0.85, 1.18)),
                             occ=OCC[cls] * float(rng.uniform(0.88, 1.10)), opened=W.MONTHS[0], closed=None,
                             county=county_for(region, rng), drift=float(rng.normal(self.p["growth"],
                                                                                   self.p["growth_sd"])))
                    # county rules: no extended-stay property in the two counties that cut their option rate
                    if cls == "ES" and f["county"] in W.CUT_COUNTIES:
                        f["county"] = [c for c, r in W.COUNTIES.items() if r == region and c not in W.CUT_COUNTIES][0]
                    out.append(f)
                    k += 1
        # flags the changes key on
        for f in out:
            f["highway14"] = f["region"] == "North Woods" and f["cls"] in ("MO", "LS") and rng.random() < 0.55
            f["stadium"] = f["region"] == "Capital City North" and f["cls"] in ("FS", "LS", "ES") and rng.random() < 0.45
        # openings and closures over the four years
        lodging = [f for f in out if f["cls"] in ("FS", "LS")]
        for f in rng.choice(lodging, size=self.p["new_openings"], replace=False):
            f["opened"] = W.MONTHS[int(rng.integers(26, 34))]          # opened in fiscal 2025 (Sep 2024 .. Apr 2025)
        for f in rng.choice([f for f in out if f["cls"] in ("MO", "BB")], size=14, replace=False):
            f["closed"] = W.MONTHS[int(rng.integers(8, 44))]
        # renovation closures: no returns for two to four months, in fiscal 2023 or fiscal 2024
        for f in out:
            f["gap"] = None
        pool = [f for f in out if f["cls"] in ("FS", "LS", "MO") and not f["highway14"] and not f["stadium"]
                and f["opened"] == W.MONTHS[0] and not f["closed"]]
        for f in rng.choice(pool, size=self.p["renovations"], replace=False):
            start = int(rng.integers(2, 22))
            f["gap"] = (start, start + int(rng.integers(2, 5)))
        # two marketplace facilitators register in July 2025
        for name_k in range(2):
            out.append(dict(filer_id="LT%06d" % ids[k], region="Statewide", cls="PF", rooms=0, b=0.0, adr=0.0, occ=0.0,
                            opened=dt.date(2025, 8, 1), closed=None, county="Statewide", drift=0.0,
                            highway14=False, stadium=False))
            k += 1
        self.register = out
        return out

    # ------------------------------------------------------------------ monthly receipts
    def receipts(self):
        rng = np.random.default_rng([self.seed, 32])
        p = self.p
        rows = []
        str_hosts = [f for f in self.register if f["cls"] == "STR"]
        platforms = [f for f in self.register if f["cls"] == "PF"]
        share = {}
        for f in str_hosts:
            share[f["filer_id"]] = int(rng.integers(0, 2))           # which facilitator a host lists on
        platform_receipts = {}          # (facilitator, county) -> monthly receipts
        for f in self.register:
            if f["cls"] == "PF":
                continue
            leis = LEISURE.get(f["region"], LEISURE["default"])
            shape = f["b"] * BUSINESS + (1 - f["b"]) * leis
            base = f["rooms"] * f["adr"] * f["occ"] * 30.4
            if f["cls"] == "STR":
                base = f["rooms"] * f["adr"] * f["occ"] * 30.4 * 0.9
            eps = rng.normal(0, p["month_sd"], 48)
            series = np.zeros(48)
            for i, m in enumerate(W.MONTHS):
                if m < f["opened"] or (f["closed"] and m >= f["closed"]):
                    continue
                if f.get("gap") and f["gap"][0] <= i < f["gap"][1]:
                    continue
                t = i / 12.0
                v = base * shape[i % 12] * (1 + f["drift"]) ** t * np.exp(eps[i])
                # ramp-up in a new property's first year
                age = (m.year - f["opened"].year) * 12 + m.month - f["opened"].month
                if f["opened"] > W.MONTHS[0] and age < 12:
                    v *= 0.55 + 0.45 * age / 12
                # campgrounds shut from November to April
                if f["cls"] == "CG" and m.month in (11, 12, 1, 2, 3, 4):
                    v = 0.0
                # fiscal 2024: Highway 14 reconstruction from March 2024
                if f["highway14"] and dt.date(2024, 3, 1) <= m <= dt.date(2024, 10, 1):
                    v *= 1 - p["highway"]
                # fiscal 2025 onward: the stadium district
                if f["stadium"] and m >= dt.date(2024, 9, 1):
                    v *= 1 + p["stadium"]
                # fiscal 2026: the business-travel slump from September 2025
                if m >= dt.date(2025, 9, 1):
                    v *= 1 - p["slump"] * f["b"] ** p["slump_power"]
                # the convention center is shut September 2025 to February 2026
                if f["region"] == "Capital City Downtown" and f["cls"] in ("FS", "LS") and \
                        dt.date(2025, 9, 1) <= m < dt.date(2026, 3, 1):
                    v *= 1 - p["closure"]
                # long stays leave the base at extended-stay hotels from January 2026
                if f["cls"] == "ES" and m >= dt.date(2026, 1, 1):
                    v *= 1 - p["exemption"]
                # the airline hub reduction trims airport hotels from November 2025
                if f["region"] == "Airport Corridor" and f["cls"] in ("FS", "LS") and m >= dt.date(2025, 11, 1):
                    v *= 1 - p["airline"]
                series[i] = v
            if f["cls"] == "STR":
                # from August 2025 the facilitators collect and file for their hosts
                for i, m in enumerate(W.MONTHS):
                    if m >= dt.date(2025, 8, 1):
                        key = (platforms[share[f["filer_id"]]]["filer_id"], f["county"])
                        platform_receipts.setdefault(key, np.zeros(48))[i] += series[i] * (1 + p["platform_gain"])
                        series[i] = 0.0
            for i, m in enumerate(W.MONTHS):
                if series[i] > 0 or (f["cls"] == "CG" and f["opened"] <= m and not (f["closed"] and m >= f["closed"])
                                     and m.month in (11, 12, 1, 2, 3, 4)):
                    if f["cls"] == "STR" and m >= dt.date(2025, 8, 1):
                        continue
                    rows.append(self._row(f, m, series[i], f["county"]))
        pf_by_id = {pf["filer_id"]: pf for pf in platforms}
        for (pid, county), arr in sorted(platform_receipts.items()):
            for i, m in enumerate(W.MONTHS):
                if arr[i] > 0:
                    rows.append(self._row(pf_by_id[pid], m, arr[i], county))
        self.returns = rows
        return rows

    @staticmethod
    def rate(county, m):
        if county in W.CUT_COUNTIES:
            return W.STATE_RATE + (W.CUT_OLD if m < dt.date(2025, 10, 1) else W.CUT_NEW)
        return W.STATE_RATE + W.COUNTY_RATE

    def _row(self, f, m, receipts, county):
        r = round(float(receipts), 2)
        rate = self.rate(county, m)
        return dict(filer_id=f["filer_id"], period=m, county=county, taxable_receipts=r, rate=rate,
                    tax=round(r * rate, 2))

    def build(self):
        self.filers()
        self.receipts()
        return self
