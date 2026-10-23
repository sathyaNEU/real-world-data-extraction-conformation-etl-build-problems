"""task176 world: Allerton's family child care homes from 2004 to 2026, their providers, the children who count
toward each home's capacity, and each home's closure. Monthly discrete time. The closure hazard is a tenure
baseline (higher in a home's first six months), a summer lift, a retirement term at 63 and 68, and a spike in
June to August of the year the provider's youngest own child starts kindergarten (a much smaller one for a
grandmother's youngest grandchild). Nothing else in the world moves closure: the grant cohort differs only in
who its providers are."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C

P = dict(
    inflow={2004: 330, 2005: 325, 2006: 320, 2007: 318, 2008: 312, 2009: 300, 2010: 296, 2011: 290, 2012: 284,
            2013: 280, 2014: 276, 2015: 272, 2016: 268, 2017: 262, 2018: 258, 2019: 255, 2020: 188, 2021: 228,
            2022: 297, 2023: 1224, 2024: 333, 2025: 287, 2026: 271},
    share_norm=dict(parent=0.38, grand=0.12), share_grant=dict(parent=0.74, grand=0.06),
    yc_norm=(0.8, 4.4), yc_grant=(0.4, 1.4),
    nkids=(0.46, 0.37, 0.13, 0.04), nkids_grant=(0.72, 0.21, 0.06, 0.01), gap=(1.5, 4.5),
    b0=0.0110, b1=0.0058, early=6, summer=1.25, frail_var=0.05,
    grant_hold=0.45, grant_hold_months=12,          # the grant's service condition: repay if closed in 12 months
    pandemic=1.20,                                  # April to December 2020
    retire1=(63, 0.010), retire2=(68, 0.016),
    kx=0.189, kg=0.040, kmonths=(6, 7, 8),
    birth_parent=0.07, birth_other=0.02,
    foster_p=0.04, relative_p=0.03, school_age_other=0.25,
    lfcc_p=0.18,
)
END_M = C.mi(2026, 12)
NAMES = "ABCDEFGHIJKLMNOPRSTVWY"


class Home:
    __slots__ = ("hid", "lic", "lic_m", "county", "ltype", "cap", "ptype", "pbirth", "kids", "frail", "grant",
                 "close", "close_m", "cause", "ceff", "seq")

    def youngest_own(self, d):
        b = [k["birth"] for k in self.kids if k["rel"] == "OWN" and k["birth"] <= d]
        return max(b) if b else None

    def youngest_grand(self, d):
        b = [k["birth"] for k in self.kids if k["rel"] == "GRANDCHILD" and k["start"] <= d and
             (k["end"] is None or k["end"] >= d)]
        return max(b) if b else None


def _day_in(rng, m):
    s, e = C.month_start(m), C.month_end(m)
    return s + dt.timedelta(days=int(rng.integers(0, (e - s).days + 1)))


def _initials(rng):
    return NAMES[int(rng.integers(0, len(NAMES)))] + NAMES[int(rng.integers(0, len(NAMES)))]


def hazard(h, m, p=P):
    t = m - h.lic_m
    y, mon = C.ym_of(m)
    base = (p["b0"] if t < p["early"] else p["b1"]) * h.frail * h.ceff
    if h.grant and t < p["grant_hold_months"]:
        base *= p["grant_hold"]
    if (y == 2020 and mon >= 4):
        base *= p["pandemic"]
    if mon in (6, 7, 8):
        base *= p["summer"]
    d = C.month_start(m)
    age = (d - h.pbirth).days / 365.25
    ret = p["retire2"][1] if age >= p["retire2"][0] else (p["retire1"][1] if age >= p["retire1"][0] else 0.0)
    k = 0.0
    if mon in p["kmonths"]:
        yo = h.youngest_own(C.month_end(m))
        if yo is not None and C.kyear(yo) == y:
            k += p["kx"]
        yg = h.youngest_grand(C.month_end(m))
        if yg is not None and C.kyear(yg) == y:
            k += p["kg"]
    return min(base + ret + k, 0.95), (ret > 0, k > 0)


def simulate(p=P):
    rng = C.stream("world")
    ceff = {c[0]: float(x) for c, x in zip(C.COUNTIES, C.stream("county_eff").uniform(0.90, 1.10, len(C.COUNTIES)))}
    codes = [c[0] for c in C.COUNTIES]
    wts = np.array([c[3] for c in C.COUNTIES])
    wts = wts / wts.sum()
    homes = []
    hid = 0
    for year, n in sorted(p["inflow"].items()):
        for _ in range(n):
            grant_window = year == 2023 and rng.random() < 0.94
            if grant_window:
                m = C.mi(2023, 2) + int(rng.integers(0, 10))
            else:
                m = C.mi(year, 1) + int(rng.integers(0, 12))
            h = Home()
            h.hid, h.lic_m, h.seq = hid, m, hid
            hid += 1
            h.lic = _day_in(rng, m)
            h.county = codes[int(rng.choice(len(codes), p=wts))]
            h.ceff = ceff[h.county]
            h.grant = bool(grant_window)
            sh = p["share_grant"] if h.grant else p["share_norm"]
            u = rng.random()
            h.ptype = "parent" if u < sh["parent"] else ("grand" if u < sh["parent"] + sh["grand"] else "other")
            if h.ptype == "parent":
                age = rng.uniform(23, 41)
            elif h.ptype == "grand":
                age = rng.uniform(45, 64)
            else:
                age = rng.uniform(27, 62)
            h.pbirth = h.lic - dt.timedelta(days=int(age * 365.25))
            h.ltype = "LFCC" if (h.ptype == "other" and rng.random() < p["lfcc_p"] * 2.2) or rng.random() < 0.04 else "SFCC"
            h.cap = 12 if h.ltype == "LFCC" else (6 if rng.random() < 0.2 else 8)
            h.kids = []
            if h.ptype == "parent":
                lo, hi = p["yc_grant"] if h.grant else p["yc_norm"]
                yb = h.lic - dt.timedelta(days=int(rng.uniform(lo, hi) * 365.25))
                nk = int(rng.choice(4, p=p["nkids_grant"] if h.grant else p["nkids"])) + 1
                b = yb
                for j in range(nk):
                    h.kids.append(dict(birth=b, rel="OWN", start=b, end=None, ini=_initials(rng)))
                    b = b - dt.timedelta(days=int(rng.uniform(*p["gap"]) * 365.25))
            elif h.ptype == "grand":
                for j in range(int(rng.integers(1, 4))):
                    b = h.lic - dt.timedelta(days=int(rng.uniform(0.2, 4.5) * 365.25))
                    end = b + dt.timedelta(days=int(365.25 * 6))
                    h.kids.append(dict(birth=b, rel="GRANDCHILD", start=max(b, h.lic), end=end, ini=_initials(rng)))
            else:
                if rng.random() < p["school_age_other"] and age < 50:
                    for j in range(int(rng.integers(1, 3))):
                        b = h.lic - dt.timedelta(days=int(rng.uniform(6, 12.5) * 365.25))
                        h.kids.append(dict(birth=b, rel="OWN", start=b, end=None, ini=_initials(rng)))
            if rng.random() < p["foster_p"]:
                s = h.lic + dt.timedelta(days=int(rng.integers(30, 2000)))
                b = s - dt.timedelta(days=int(rng.uniform(0.1, 11) * 365.25))
                h.kids.append(dict(birth=b, rel="FOSTER", start=s, end=s + dt.timedelta(days=int(rng.integers(90, 800))),
                                   ini=_initials(rng)))
            if rng.random() < p["relative_p"]:
                s = h.lic + dt.timedelta(days=int(rng.integers(0, 1500)))
                b = s - dt.timedelta(days=int(rng.uniform(0.5, 9) * 365.25))
                h.kids.append(dict(birth=b, rel="RELATIVE", start=s, end=s + dt.timedelta(days=int(rng.integers(180, 1500))),
                                   ini=_initials(rng)))
            h.frail = float(rng.gamma(1 / p["frail_var"], p["frail_var"]))
            h.close = h.close_m = h.cause = None
            homes.append(h)
    # the monthly process, one stream per home so a home's path does not depend on the others
    for h in homes:
        r = C.stream("home/%d" % h.hid)
        for m in range(h.lic_m, END_M + 1):
            hz, (ret, k) = hazard(h, m, p)
            if m > h.lic_m and r.random() < hz:
                h.close_m = m
                h.close = _day_in(r, m)
                if h.close <= h.lic:
                    h.close = h.lic + dt.timedelta(days=20)
                h.cause = "K" if k else ("RETIRE" if ret else "BASE")
                break
            age = (C.month_start(m) - h.pbirth).days / 365.25
            rate = p["birth_parent"] if h.ptype == "parent" else (p["birth_other"] if age < 36 else 0)
            if age < 41 and rate and r.random() < rate / 12:
                b = _day_in(r, m)
                h.kids.append(dict(birth=b, rel="OWN", start=b, end=None, ini=_initials(r)))
    return homes


def truth_2027(homes, p=P):
    """expected closures in 2027 among the homes open at the end of 2026, on the world's own hazard and each
    home's true family (births up to the end of 2026)"""
    tot = 0.0
    for h in homes:
        if h.close is not None:
            continue
        s = 1.0
        for m in range(C.mi(2027, 1), C.mi(2027, 12) + 1):
            s *= 1 - hazard(h, m, p)[0]
        tot += 1 - s
    return tot


if __name__ == "__main__":
    hs = simulate()
    op = [h for h in hs if h.close is None]
    print("homes", len(hs), "open at end 2026", len(op), "grant open", sum(h.grant for h in op))
    print("truth 2027", round(truth_2027(hs), 1))
