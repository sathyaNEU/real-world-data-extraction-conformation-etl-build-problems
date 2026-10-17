"""The clean truth for task264: every adult who visited the Authority's parks in the 2025-26 survey year (where they
live, how often they came, when and to which parks), the exit survey drawn from their visits, and the contractor's
expansion weights. Nothing here is written to the pack; records.py turns it into the contractor's and the
Authority's files."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

import common as K


# each council's streams keep the key they were first drawn under, so renaming an area code never redraws its people
STREAM = {"KDM": "KVH", "RVW": "TVS", "SNG": "JKL", "LKS": "LVB", "GRB": "GLV", "HNM": "VVC", "CHD": "TKF", "WDS": "EKD",
          "FNC": "CVL", "OUT": "OUT"}


def rng(*keys):
    """One stable stream per purpose, so a change in one part of the world never reshuffles another."""
    h = hashlib.sha256("/".join(str(k) for k in ("task264",) + keys).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# residents aged 16 and over at mid-2025, and the share of them who visited at least once in 2025-26
ADULTS = {"KDM": 84270, "RVW": 112640, "SNG": 71880, "LKS": 138410, "GRB": 96230, "HNM": 121690,
          "CHD": 64830, "WDS": 103470, "FNC": 88120}
REACH = {"KDM": .514, "RVW": .468, "SNG": .493, "LKS": .208, "GRB": .231, "HNM": .184, "CHD": .262,
         "WDS": .191, "FNC": .219}
N_OUTSIDE = 158400          # adults from outside the member councils who came at least once
REGULAR_SHARE = {"KDM": .142, "RVW": .121, "SNG": .133}      # the valley's dog walkers, runners and daily walkers

# which park a visitor's favourite is, by where they live
PARK_PREF = {
    "KDM": {"BW": .44, "CC": .36, "GF": .09, "DW": .04, "LM": .04, "TH": .03},
    "RVW": {"GF": .39, "DW": .24, "CC": .11, "BW": .08, "LM": .10, "TH": .08},
    "SNG": {"LM": .41, "TH": .29, "GF": .12, "BW": .06, "CC": .04, "DW": .08},
    "LKS": {"GF": .31, "DW": .27, "LM": .16, "TH": .14, "BW": .07, "CC": .05},
    "GRB": {"GF": .28, "DW": .22, "LM": .20, "TH": .18, "BW": .07, "CC": .05},
    "HNM": {"GF": .25, "DW": .30, "LM": .15, "TH": .18, "BW": .07, "CC": .05},
    "CHD": {"LM": .35, "TH": .25, "GF": .20, "DW": .12, "BW": .05, "CC": .03},
    "WDS": {"DW": .35, "GF": .30, "TH": .15, "LM": .12, "BW": .05, "CC": .03},
    "FNC": {"TH": .30, "LM": .25, "GF": .22, "DW": .15, "BW": .05, "CC": .03},
    "OUT": {"DW": .31, "LM": .29, "TH": .22, "GF": .14, "BW": .02, "CC": .02},
}
# when each kind of visitor comes: share of their visits by season and day type
PROFILE = {
    "reg": {("SP", "WD"): .17, ("SP", "WE"): .08, ("SU", "WD"): .17, ("SU", "WE"): .08, ("AU", "WD"): .17,
            ("AU", "WE"): .08, ("WI", "WD"): .17, ("WI", "WE"): .08},
    "loc": {("SP", "WD"): .15, ("SP", "WE"): .10, ("SU", "WD"): .15, ("SU", "WE"): .11, ("AU", "WD"): .14,
            ("AU", "WE"): .09, ("WI", "WD"): .15, ("WI", "WE"): .11},
    "occ": {("SP", "WD"): .05, ("SP", "WE"): .20, ("SU", "WD"): .12, ("SU", "WE"): .38, ("AU", "WD"): .03,
            ("AU", "WE"): .12, ("WI", "WD"): .02, ("WI", "WE"): .08},
    "trip": {("SP", "WD"): .08, ("SP", "WE"): .18, ("SU", "WD"): .20, ("SU", "WE"): .36, ("AU", "WD"): .03,
             ("AU", "WE"): .08, ("WI", "WD"): .02, ("WI", "WE"): .05},
}
SAMPLED_DAYS = {("SP", "WD"): 4, ("SP", "WE"): 3, ("SU", "WD"): 4, ("SU", "WE"): 4, ("AU", "WD"): 4,
                ("AU", "WE"): 3, ("WI", "WD"): 4, ("WI", "WE"): 3}
SHIFT = (25.4, 4.6, 14, 32)    # completed interviews one interviewer manages in a shift: mean, spread, fewest, most
SHIFT_SHARE, EVERY, RESPONSE = .6, 8, .68


def frequencies(code, n):
    r = rng("freq", STREAM[code])
    if code == "OUT":
        typ = np.array(["trip"] * n)
        f = np.round(r.lognormal(np.log(1.4), .55, n))
        return np.clip(f, 1, 12).astype(int), typ
    if code in K.VALLEY:
        reg = r.random(n) < REGULAR_SHARE[code]
        typ = np.where(reg, "reg", "loc")
        f = np.where(reg, np.round(r.lognormal(np.log(55), .55, n)), np.round(r.lognormal(np.log(4.0), .85, n)))
        f = np.where(reg, np.clip(f, 12, 400), np.clip(f, 1, 60))
        return f.astype(int), typ
    typ = np.array(["occ"] * n)
    f = np.round(r.lognormal(np.log(2.0), .6, n))
    return np.clip(f, 1, 30).astype(int), typ


def people():
    """Every adult visitor: home (council code or OUT), kind, true visits in the year, and visits per stratum."""
    rows = []
    for code in K.CODES + ["OUT"]:
        n = N_OUTSIDE if code == "OUT" else int(round(ADULTS[code] * REACH[code]))
        f, typ = frequencies(code, n)
        r = rng("parks", STREAM[code])
        pref = np.array([PARK_PREF[code][p] for p in K.PARK_CODES])
        pref = pref / pref.sum()
        fav1 = r.choice(len(K.PARK_CODES), n, p=pref)
        fav2 = r.choice(len(K.PARK_CODES), n, p=pref)
        share1 = np.where(typ == "reg", .9, .75)
        ra = rng("alloc", STREAM[code])
        for i in range(n):
            prof = PROFILE[typ[i]]
            p = np.zeros(len(K.STRATA))
            for j, (pk, s, d) in enumerate(K.STRATA):
                pi = K.PARK_CODES.index(pk)
                w = (share1[i] if pi == fav1[i] else 0) + ((1 - share1[i]) if pi == fav2[i] else 0)
                p[j] = w * prof[(s, d)]
            p /= p.sum()
            cnt = ra.multinomial(f[i], p)
            nz = np.nonzero(cnt)[0]
            rows.append((code, typ[i], int(f[i]), nz.astype(np.int16), cnt[nz].astype(np.int32)))
    return rows


def report(f, r):
    """What a visitor says when asked how many times in the last 12 months, including today: small counts as
    they are, larger ones rounded the way people round them."""
    if f <= 6:
        return f if r.random() < .9 else max(1, f + int(r.choice([-1, 1])))
    nice = [7, 8, 10, 12, 15, 20, 24, 25, 30, 36, 40, 50, 52, 60, 70, 75, 80, 100, 104, 120, 150, 156, 180, 200, 250,
            260, 300, 350, 365, 400]
    if r.random() < .62:
        return int(min(nice, key=lambda x: (abs(x - f), x)))
    return int(max(1, round(f * r.lognormal(0, .08))))


def survey(P):
    """Sampled days per stratum, completed interviews per day, the interviewed visits (an equal chance for every
    visit in the stratum), and the contractor's estimate of each stratum's adult visits."""
    nst = len(K.STRATA)
    V = np.zeros(nst)
    for _, _, _, nz, cnt in P:
        V[nz] += cnt
    pools = [[] for _ in range(nst)]
    for idx, (_, _, _, nz, cnt) in enumerate(P):
        for j, c in zip(nz, cnt):
            pools[j].append(np.full(int(c), idx, dtype=np.int32))
    pools = [np.concatenate(x) if x else np.zeros(0, np.int32) for x in pools]
    days, m_day, picks = {}, {}, {}
    for j, (pk, s, d) in enumerate(K.STRATA):
        r = rng("survey", pk, s, d)
        alld = K.days_of(s, d)
        k = SAMPLED_DAYS[(s, d)]
        chosen = sorted(r.choice(len(alld), k, replace=False))
        dd = [alld[c] for c in chosen]
        per_day = V[j] / len(alld)
        md = [int(min(np.clip(round(r.normal(SHIFT[0], SHIFT[1])), SHIFT[2], SHIFT[3]),
                      round(per_day * r.lognormal(0, .25) * SHIFT_SHARE / EVERY * RESPONSE))) for _ in dd]
        md = [max(m, 2) for m in md]
        sel = r.choice(len(pools[j]), sum(md), replace=False)
        days[j], m_day[j], picks[j] = dd, md, pools[j][sel]
    est = np.round(V * np.exp(rng("frame").normal(0, .03, nst)), -1)
    return dict(V=V, est=est, days=days, m_day=m_day, picks=picks)


BAND_P = {"GF": [.20, .38, .30, .12], "DW": [.10, .25, .35, .30], "LM": [.15, .30, .33, .22],
          "TH": [.12, .35, .38, .15]}
BAND_MIN = {"1H": (20, 60), "2H": (61, 120), "4H": (121, 240), "DAY": (241, 470)}


def utc_offset(d):
    """Hours local time is ahead of UTC in the UK on date d (British Summer Time from the last Sunday of March to
    the last Sunday of October)."""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return 1 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 0


def gates(d):
    """Car-park gate hours, local time: 07:00 to 20:00 from April to September, 08:00 to 18:00 otherwise."""
    return (7 * 60, 20 * 60) if 4 <= d.month <= 9 else (8 * 60, 18 * 60)


def tariff(park, d):
    if park in TARIFF_HIGH_ and K.HIGH_SEASON[0] <= d <= K.HIGH_SEASON[1]:
        return K.TARIFF_HIGH[park]
    return K.TARIFF[park]


TARIFF_HIGH_ = set(K.TARIFF_HIGH)


def machines_on(cp, d):
    out = []
    for mid, site, a, b in K.MACHINES:
        if site == cp and (a is None or d >= a) and (b is None or d <= b):
            out.append(mid)
    return out


CARS_SALT = 5                 # keys the car-park stream; chosen so each park's parking income sits clear of a half pound


def car_parks(S):
    """Every vehicle that entered a charging park's car park in the survey year: when it came and left (local
    minutes), its tariff band, whether it paid and how, and at which machine."""
    days = []
    d = K.YEAR0
    while d <= K.YEAR1:
        days.append(d)
        d += dt.timedelta(days=1)
    n_days = {(s, dtp): len(K.days_of(s, dtp)) for s in K.SEASON_CODES for dtp in K.DAYTYPES}
    rows = {k: [] for k in ("date", "cp", "park", "arrive", "leave", "band", "payer", "app", "machine")}
    for park in K.CHARGING:
        r = rng("cars", park, CARS_SALT)
        cps = [c for c in K.CP_CODES if K.CP_PARK[c] == park]
        for d in days:
            s, dtp = K.season(d), K.daytype(d)
            j = K.SI[(park, s, dtp)]
            adults = S["V"][j] / n_days[(s, dtp)] * r.lognormal(-.024, .22)
            veh = int(r.poisson(adults * K.CAR_SHARE[park] / K.OCCUPANCY[park]))
            n1 = int(r.binomial(veh, K.CP_SPLIT[cps[0]])) if len(cps) > 1 else veh
            g0, g1 = gates(d)
            for cp, n in zip(cps, (n1, veh - n1)):
                arrive = np.clip(np.round(r.normal(12.5 * 60, 2.4 * 60, n)), g0, g1 - 25).astype(int)
                band = r.choice(4, n, p=BAND_P[park])
                lo = np.array([BAND_MIN[K.BANDS[b]][0] for b in band], dtype=int)
                hi = np.array([BAND_MIN[K.BANDS[b]][1] for b in band], dtype=int)
                stay = (lo + r.random(n) * (hi - lo)).astype(int)
                leave = np.minimum(arrive + stay, g1 - 2)
                payer = r.random(n) < .86
                app = payer & (r.random(n) < K.APP_SHARE[park])
                ms = machines_on(cp, d)
                pick = np.array(ms)[r.integers(0, len(ms), n)] if n else np.array([], dtype=str)
                mach = np.where(payer & ~app, pick, "")
                rows["date"].extend([d] * n)
                rows["cp"].extend([cp] * n)
                rows["park"].extend([park] * n)
                for k, v in (("arrive", arrive), ("leave", leave), ("band", band), ("payer", payer), ("app", app),
                             ("machine", mach)):
                    rows[k].extend(v.tolist())
    return {k: (v if k == "date" else np.array(v)) for k, v in rows.items()}


# usual residents, all ages, at mid-year (the county research team's estimates); 16 and over at mid-2025 is ADULTS
POP = {"KDM": (103610, 104120, 104680), "RVW": (138870, 139540, 140210), "SNG": (88410, 88790, 89130),
       "LKS": (171240, 172380, 173460), "GRB": (119050, 119620, 120310), "HNM": (150480, 151330, 152170),
       "CHD": (80230, 80470, 80740), "WDS": (128110, 128690, 129380), "FNC": (109060, 109540, 110090)}


def apportion(total, basis):
    """A levy split in proportion to a basis, each council's amount rounded to the pound."""
    t = sum(basis.values())
    return {c: int(round(total * basis[c] / t)) for c in K.CODES}


# mid-2022 populations, the basis of the 2024-25 levy (not shipped; only the 2024-25 instalments reach the pack)
POP_2022 = {"KDM": 103180, "RVW": 138260, "SNG": 88090, "LKS": 170310, "GRB": 118540, "HNM": 149730, "CHD": 80010,
            "WDS": 127560, "FNC": 108620}


def instalments(amt):
    """Four instalments: the first three a quarter each, rounded down to the pound, the fourth the balance."""
    out = {}
    for c in K.CODES:
        q = amt[c] // 4
        out[c] = [q, q, q, amt[c] - 3 * q]
    return out


def levy_2025():
    """The 2025-26 levy on the old basis (mid-2023 population, all ages) and its four instalments."""
    amt = apportion(K.LEVY_2025, {c: POP[c][0] for c in K.CODES})
    return amt, instalments(amt)


def levy_2024():
    """The 2024-25 levy (mid-2022 population) and its instalments."""
    amt = apportion(K.LEVY_2024, POP_2022)
    return amt, instalments(amt)


def world():
    P = people()
    S = survey(P)
    C = car_parks(S)
    return dict(P=P, S=S, C=C)


if __name__ == "__main__":
    import collections
    T = world()
    P, S = T["P"], T["S"]
    m = np.array([sum(S["m_day"][j]) for j in range(len(K.STRATA))])
    w = S["est"] / m
    r = rng("report")
    rows = []
    for j in range(len(K.STRATA)):
        for idx in S["picks"][j]:
            code, typ, f, _, _ = P[idx]
            rows.append((code, report(f, r), w[j], j))
    truth = collections.Counter(p[0] for p in P)

    def sh(d):
        t = sum(d[c] for c in K.CODES)
        return {c: 100 * d[c] / t for c in K.CODES}
    R0, R1, R3, G, WF = (collections.defaultdict(float) for _ in range(5))
    for code, f, wi, j in rows:
        R0[code] += 1; R1[code] += wi; R3[code] += 1 / f; G[code] += wi / f; WF[code] += wi * f
    R2 = {c: R1[c] / (WF[c] / R1[c]) for c in K.CODES}
    out = [sh(truth), sh(R0), sh(R1), sh(R2), sh(R3), sh(G)]
    print("visits %.0f  interviews %d  people %d" % (S["V"].sum(), m.sum(), len(P)))
    print("code   truth    R0     R1     R2     R3      G")
    for c in K.CODES:
        print("%-4s " % c + " ".join("%6.2f" % o[c] for o in out))
    print("valley " + " ".join("%6.2f" % sum(o[c] for c in K.VALLEY) for o in out))
    print("G members %.0f truth %d" % (sum(G[c] for c in K.CODES), sum(truth[c] for c in K.CODES)))
    print("1/r range", (S["est"] / m).min(), (S["est"] / m).max())
