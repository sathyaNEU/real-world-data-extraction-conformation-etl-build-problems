"""The truth behind the pack: Sandpiper Mutual's territory, its policies and their roofs, its storms since 2008 and
what each did to each insured home, its wind and hail claims outside named storms, its FORTIFIED certificates, the
2024 book transfer, and the hurricane model vendor's 2027 event set for the four candidate counties.

Nothing here is shipped. records.py turns it into the files the company's own systems would hold.
"""
import datetime as dt

import numpy as np

SEED = 309
DED = 0.02            # named-storm deductible, share of Coverage A
K = 8.0               # beta concentration of a home's damage ratio around its mean
YEARS = range(2006, 2027)

# Counties: (code, name, x-range km along the coast, y-range km inland, coastal?)
COUNTIES = [
    ("MRS", "Marlin Shoals", (0, 45), (0, 9), True),
    ("HRB", "Heron Bay", (45, 100), (5, 30), True),
    ("CLF", "Calloway Flats", (100, 150), (30, 65), True),
    ("CYR", "Cypress Ridge", (150, 210), (8, 30), True),
    ("PNH", "Pine Hollow", (0, 70), (40, 110), False),
    ("SUM", "Sumner", (70, 140), (70, 130), False),
    ("BRK", "Bracken", (140, 210), (65, 125), False),
]
CANDIDATES = ["MRS", "HRB", "CLF", "CYR"]
COUNTY_VALUE = {"MRS": 262000, "HRB": 248000, "CLF": 236000, "CYR": 292000}


def gu_mean(w):
    """Mean ground-up damage ratio of a standard-roof home at peak gust w (mph)."""
    return 0.50 / (1.0 + np.exp(-(np.asarray(w, float) - 129.0) / 11.5))


def gross_cut(w):
    """The FORTIFIED roof's cut in a home's paid loss (after the deductible): the sealed deck and ring-shank nailing
    keep the cover and deck on below the design gust; above it the walls, openings and roof-to-wall connection go
    regardless."""
    w = np.asarray(w, float)
    return np.where(w < 130, 0.63, np.where(w > 133, 0.10, 0.63 - (w - 130) * (0.53 / 3.0)))


_FT = {}


def _fort_table():
    """The FORTIFIED home's mean damage ratio at each gust (1 mph grid) that gives the paid-loss cut above."""
    if _FT:
        return _FT["g"], _FT["m"]
    from scipy.stats import beta as B
    qs = np.linspace(0.00025, 0.99975, 1500)

    def eg(m):
        m = float(np.clip(m, 1e-6, 0.95))
        return float(np.maximum(B.ppf(qs, m * K, (1 - m) * K) - DED, 0.0).mean())
    grid = np.arange(30.0, 191.0, 1.0)
    ms = []
    for g in grid:
        ms_ = float(gu_mean(g))
        target = (1.0 - float(gross_cut(g))) * eg(ms_)
        lo, hi = 1e-6, ms_
        for _ in range(26):
            mid = 0.5 * (lo + hi)
            if eg(mid) < target:
                lo = mid
            else:
                hi = mid
        ms.append(0.5 * (lo + hi))
    _FT["g"], _FT["m"] = grid, np.array(ms)
    return _FT["g"], _FT["m"]


def fort_mean(w):
    g, m = _fort_table()
    return np.interp(np.asarray(w, float), g, m)


def footprint(peak, x0, xs, ys, rmw=28.0, heading=0.0):
    """Peak 3-second gust (mph) at points (xs, ys) for a storm of peak gust `peak` making landfall at x0."""
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    dx = np.abs(xs - x0 - ys * heading)
    radial = np.where(dx <= rmw, 1.0, (rmw / np.maximum(dx, rmw)) ** 0.55)
    inland = np.exp(-np.maximum(ys, 0) / 140.0)
    return np.maximum(peak * radial * inland, 38.0)


# Historical storms: (code, name, landfall date, landfall x km, peak gust mph, heading)
STORMS = [
    ("2008-03", "Hurricane Corwin", "2008-09-12", 160, 118, 0.10),
    ("2009-02", "Tropical Storm Della", "2009-08-27", 40, 86, -0.05),
    ("2011-04", "Hurricane Evander", "2011-09-03", 110, 104, 0.05),
    ("2012-05", "Hurricane Faye", "2012-08-29", 70, 126, 0.00),
    ("2013-03", "Tropical Storm Gideon", "2013-09-14", 180, 92, 0.08),
    ("2014-06", "Hurricane Halsey", "2014-10-02", 125, 108, -0.06),
    ("2016-04", "Hurricane Ines", "2016-09-07", 30, 154, 0.04),
    ("2017-07", "Hurricane Jessup", "2017-09-20", 150, 114, 0.02),
    ("2018-05", "Hurricane Kendra", "2018-10-10", 95, 145, -0.03),
    ("2019-03", "Tropical Storm Laszlo", "2019-08-19", 60, 94, 0.00),
    ("2020-08", "Hurricane Marisol", "2020-09-16", 120, 172, 0.06),
    ("2021-06", "Hurricane Nolan", "2021-08-30", 15, 110, -0.02),
    ("2022-04", "Hurricane Odile", "2022-09-28", 175, 136, 0.05),
    ("2023-05", "Hurricane Pryor", "2023-08-24", 85, 120, 0.00),
    ("2024-07", "Hurricane Quenby", "2024-10-09", 28, 168, 0.03),
    ("2025-03", "Hurricane Rosalind", "2025-09-02", 140, 116, -0.04),
]
KT = 1.150779          # mph per knot
KNOT_UNTIL = 2019      # footprints before the 2019 season came from the analysis service in knots
LEGACY_CUTOVER = 2012          # storms before this year were handled in the legacy claims system
TRANSFER_DATE = "2024-07-01"   # Gulfway Home Insurance's coastal book moves to Sandpiper
TRANSFER_COUNTIES = {"HRB": 0.22, "CYR": 0.18}   # share of each ZIP's in-force book that arrives by transfer
ASOF = dt.date(2026, 9, 30)


def _d(s):
    return dt.date.fromisoformat(s)


def add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:          # 29 February
        return d.replace(year=d.year + n, day=28)


def _holidays(y):
    """The office closures: New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving, Christmas."""
    def nth(month, wd, n):
        d = dt.date(y, month, 1)
        d += dt.timedelta(days=(wd - d.weekday()) % 7)
        return d + dt.timedelta(weeks=n - 1)
    may31 = dt.date(y, 5, 31)
    return {dt.date(y, 1, 1), may31 - dt.timedelta(days=may31.weekday()), dt.date(y, 7, 4), nth(9, 0, 1),
            nth(11, 3, 4), dt.date(y, 12, 25)}


def bday(d):
    """The next working day on or after `d` (offices and the claims system's payment runs)."""
    while d.weekday() >= 5 or d in _holidays(d.year):
        d += dt.timedelta(days=1)
    return d


def certified(home, day):
    """Whether the building holds a valid FORTIFIED Roof certificate on `day`."""
    for c in home["certs"]:
        end = c["void"] if c["void"] is not None and c["void"] < c["expiry"] else c["expiry"]
        if c["issued"] <= day < end:
            return True
    return False


STREETS = ["Heron Point", "Magnolia", "Bayou Ridge", "Live Oak", "Pelican Bend", "Sandhill", "Cedar Landing",
           "Marsh Hen", "Old Ferry", "Tidewater", "Saltgrass", "Pine Bluff", "Osprey", "Gulf Breeze", "Cypress Bend",
           "Oyster Shell", "Palmetto", "Shell Bank", "Driftwood", "Laurel Hill", "Sea Oats", "Dogwood", "Mullet Point",
           "Fort Dale", "Beacon", "Redfish", "Wax Myrtle", "Bay Vista", "Juniper", "Clearwater"]
STYPES = [("Road", "RD"), ("Drive", "DR"), ("Lane", "LN"), ("Street", "ST"), ("Court", "CT"), ("Avenue", "AVE"),
          ("Circle", "CIR"), ("Way", "WAY")]


def _building(rng, zi, parcel, bldg, main=None):
    if main is not None:
        b = dict(main)
        b.update(bldg=1, certs=[], events=[], roof0=int(rng.integers(1985, 2006)))
        return b
    return dict(zi=zi, parcel=parcel, bldg=bldg, certs=[], events=[], roof0=int(rng.integers(1978, 2006)),
                num=int(rng.integers(100, 9900)), street=int(rng.integers(0, len(STREETS))),
                stype=int(rng.integers(0, len(STYPES))))


def build_world(seed=SEED):
    rng = np.random.default_rng(seed)
    zips, pol = [], []
    zc = 0
    used = set()
    for code, name, (x0, x1), (y0, y1), coastal in COUNTIES:
        n = 22 if coastal else 18
        for i in range(n):
            x = rng.uniform(x0, x1); y = rng.uniform(y0, y1)
            z = "%05d" % (36500 + zc * 3 + int(rng.integers(0, 3)))
            while z in used:
                z = "%05d" % (int(z) + 1)
            used.add(z)
            base = int(rng.integers(90, 450)) if coastal else int(rng.integers(70, 320))
            val = float(rng.normal(COUNTY_VALUE.get(code, 225000), 30000))
            zips.append(dict(zip=z, county=code, x=x, y=y, base=base, val=val, coastal=coastal,
                             fpref=float(rng.uniform(0.75, 1.25))))
            zc += 1
    # Policies: every home ever insured in each ZIP. A home is a building on a parcel; a parcel changes hands when a
    # policy lapses and a later policy in the ZIP takes the same building; a few parcels carry two insured buildings.
    pno = 0
    homes = []      # buildings: dict(zi, parcel, bldg, cert intervals)
    pcount = 0
    for zi, z in enumerate(zips):
        pool = int(z["base"] * 1.9)
        free = []   # buildings whose last policy has lapsed: (lapse date, home index)
        draws = []
        for k in range(pool):
            incept = 2006 + int(rng.integers(0, 4)) if k < z["base"] else 2006 + int(rng.integers(0, 20))
            month = int(rng.integers(1, 13)); day = int(rng.integers(1, 28))
            draws.append(dt.date(incept, month, day))
        draws.sort()
        for inc in draws:
            pno += 1
            life = int(rng.geometric(0.055))
            lapse = dt.date(min(inc.year + life, 2099), inc.month, inc.day)
            reuse = [j for j, (ld, h) in enumerate(free) if ld <= inc]
            if reuse and rng.random() < 0.5:
                j = reuse[int(rng.integers(0, len(reuse)))]
                h = free.pop(j)[1]
            else:
                pcount += 1
                h = len(homes)
                homes.append(_building(rng, zi, pcount, 0))
                if rng.random() < 0.03:     # a second insured building on the same parcel
                    homes.append(_building(rng, zi, pcount, 1, homes[-1]))
            p = dict(zi=zi, zip=z["zip"], county=z["county"], incept=inc, lapse=lapse,
                     val=float(np.clip(rng.normal(z["val"], 38000), 95000, 880000)), transfer=False, pno=pno, home=h)
            pol.append(p)
            free.append((lapse, h))
    # Second buildings get their own policies, running beside the main building's
    for h, hm in enumerate(homes):
        if hm["bldg"] == 1:
            z = zips[hm["zi"]]
            pno += 1
            inc = dt.date(2006 + int(rng.integers(0, 12)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            pol.append(dict(zi=hm["zi"], zip=z["zip"], county=z["county"], incept=inc,
                            lapse=dt.date(inc.year + int(rng.geometric(0.05)), inc.month, inc.day),
                            val=float(np.clip(rng.normal(z["val"] * 0.55, 25000), 80000, 500000)), transfer=False,
                            pno=pno, home=h))
    # Transfer book: homes arriving 1 July 2024 in Heron Bay and Cypress Ridge
    for zi, z in enumerate(zips):
        share = TRANSFER_COUNTIES.get(z["county"])
        if not share:
            continue
        for k in range(int(round(z["base"] * 1.5 * share))):
            pno += 1
            pcount += 1
            h = len(homes)
            homes.append(_building(rng, zi, pcount, 0))
            life = int(rng.geometric(0.06))
            pol.append(dict(zi=zi, zip=z["zip"], county=z["county"], incept=_d(TRANSFER_DATE),
                            lapse=dt.date(2024 + life, 7, 1), val=float(np.clip(rng.normal(z["val"], 38000), 95000, 880000)),
                            transfer=True, pno=pno, home=h))
    # FORTIFIED certification is on the building: issued once the roof is replaced to the standard, valid five years,
    # renewed by re-evaluation (usually in the two months before expiry) or left to lapse; a few are voided at audit.
    for hm in homes:
        z = zips[hm["zi"]]
        for y in range(2012, 2027):
            rate = min(0.042, 0.005 + 0.003 * (y - 2012)) * z["fpref"] * (1.1 if z["coastal"] else 0.9)
            if rng.random() < rate:
                c0 = bday(dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28))))
                while c0 <= ASOF + dt.timedelta(days=400):
                    exp = add_years(c0, 5)
                    void = None
                    if rng.random() < 0.02:
                        void = bday(c0 + dt.timedelta(days=int(rng.integers(90, 1500))))
                    hm["certs"].append(dict(issued=c0, expiry=exp, void=void))
                    if void is not None or rng.random() > 0.8:
                        break
                    c0 = bday(exp - dt.timedelta(days=int(rng.integers(0, 61))))
                break
    for p in pol:
        p["parcel"] = homes[p["home"]]["parcel"]
    # policy numbers are issued in the order the policies are written
    for k, p in enumerate(sorted(pol, key=lambda q: (q["incept"], q["pno"]))):
        p["seqno"] = k + 1
    bldg = homes
    w = dict(zips=zips, policies=pol, homes=homes, storms=[], seed=seed)

    # Storm outcomes, home by home
    xs = np.array([z["x"] for z in zips]); ys = np.array([z["y"] for z in zips])
    byzip = {}
    for i, p in enumerate(pol):
        byzip.setdefault(p["zi"], []).append(i)
    for code, name, date, x0, peak, hd in STORMS:
        sd = _d(date)
        year = sd.year
        g = footprint(peak, x0, xs, ys, heading=hd)
        outc = []
        if year < KNOT_UNTIL:
            g = np.round(g / KT, 1) * KT          # the older analyses were issued in knots to one decimal
        else:
            g = np.round(g)
        for zi, gz in enumerate(g):
            gz_r = float(gz)
            for i in byzip.get(zi, []):
                p = pol[i]
                if not (p["incept"] <= sd < p["lapse"]):
                    continue
                fort = int(certified(bldg[p["home"]], sd))
                cov = round(p["val"] * (1.0 + 0.03 * (year - 2008)) / 1000.0) * 1000.0
                if gz_r < 45:
                    outc.append((i, fort, cov, 0.0, 0.0, gz_r))
                    continue
                m = float(np.clip(fort_mean(gz_r) if fort else gu_mean(gz_r), 1e-5, 0.95))
                d = rng.beta(m * K, (1 - m) * K)
                gross = max(d - DED, 0.0) * cov
                b = bldg[p["home"]]
                if d > 0.15 and rng.random() < 0.85:
                    when = bday(sd + dt.timedelta(days=int(rng.integers(30, 300))))
                    if when.year == 2012:       # the 2012 roofs waited for the Faye backlog to clear
                        when = bday(dt.date(2013, 1, 15) + dt.timedelta(days=int(rng.integers(0, 120))))
                    b["events"].append((when, "RE-ROOF"))
                elif d > 0.03 and rng.random() < 0.4:
                    b["events"].append((bday(sd + dt.timedelta(days=int(rng.integers(20, 200)))), "ROOF REPAIR"))
                outc.append((i, fort, cov, d * cov, gross, gz_r))
        w["storms"].append(dict(code=code, name=name, date=sd, year=year, peak=peak, x0=x0, hd=hd,
                                gust={zips[zi]["zip"]: float(gz) for zi, gz in enumerate(g)},
                                homes=outc))

    # Roofs replaced for age, and the repairs that do not replace them
    for b in bldg:
        for y in range(2013, 2027):
            last = max([b["roof0"]] + [e[0].year for e in b["events"] if e[1] == "RE-ROOF" and e[0].year < y])
            if y - last > 18 and rng.random() < 0.05:
                b["events"].append((bday(dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))), "RE-ROOF"))
            elif rng.random() < 0.012:
                b["events"].append((bday(dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))), "ROOF REPAIR"))
        b["events"].sort()

    # Wind and hail claims outside named storms, 2012 to 2026-09
    nonstorm = []
    for i, p in enumerate(pol):
        lo = max(p["incept"], dt.date(2012, 1, 1)); hi = min(p["lapse"], ASOF)
        days = (hi - lo).days
        if days <= 0:
            continue
        lam = 0.016 * days / 365.25
        for _ in range(int(rng.poisson(lam))):
            ld = lo + dt.timedelta(days=int(rng.integers(0, days)))
            fort = int(certified(bldg[p["home"]], ld))
            sev = float(rng.lognormal(np.log(7800 if not fort else 5400), 0.8))
            nonstorm.append((i, ld, round(sev, 2), fort))
    # The transfer book's open claims assumed on 1 July 2024: losses from before Sandpiper insured the homes
    assumed = []
    for i, p in enumerate(pol):
        if not p["transfer"]:
            continue
        if rng.random() < 0.055:
            ld = dt.date(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 180)))
            assumed.append((i, ld, round(float(rng.lognormal(np.log(9000), 0.8)), 2), 0))
    w["nonstorm"] = nonstorm
    w["assumed"] = assumed
    return w


# The vendor's 2027 event set for the four candidate counties' modeled portfolios
ELIGIBLE = {"MRS": (1480, 262000, (22, 4)), "HRB": (1530, 248000, (72, 15)),
            "CYR": (1510, 318000, (196, 16)), "CLF": (1460, 236000, (125, 45))}
VENDOR_EVENTS = 9000
VENDOR_RATE = 0.616      # landfalls a year on the 350 km of coast the set covers
MAJOR_X, MAJOR_SD = 35.0, 45.0
EAST_SHARE, EAST_X, EAST_SD = 0.85, 200.0, 35.0
P_TS, P_MOD = 0.40, 0.48


def expected_gross(mean_fn, w):
    """E[max(D - DED, 0)] for D ~ Beta with mean mean_fn(w), by quadrature on 4,000 quantiles."""
    from scipy.stats import beta as B
    m = float(np.clip(mean_fn(w), 1e-5, 0.95))
    q = B.ppf(np.linspace(0.000125, 0.999875, 4000), m * K, (1 - m) * K)
    return float(np.maximum(q - DED, 0.0).mean())


def vendor_set(seed=SEED + 1):
    """Each event's peak gust at each county's modeled-portfolio centroid and its rate."""
    rng = np.random.default_rng(seed)
    N = VENDOR_EVENTS
    u = rng.random(N)
    major = u >= P_TS + P_MOD
    east = rng.random(N) < EAST_SHARE
    x_weak = np.where(east, np.clip(rng.normal(EAST_X, EAST_SD, N), -70, 280), rng.uniform(-70, 280, N))
    x0 = np.where(major, np.clip(rng.normal(MAJOR_X, MAJOR_SD, N), -70, 280), x_weak)
    peak = np.where(u < P_TS, rng.uniform(62, 94, N),
                    np.where(u < P_TS + P_MOD, rng.uniform(94, 128, N), 128 + rng.gamma(2.2, 11.0, N)))
    peak = np.minimum(peak, 172)
    hd = rng.normal(0, 0.05, N)
    rate = np.full(N, VENDOR_RATE / N)
    out = {}
    for c, (n, val, (cx, cy)) in ELIGIBLE.items():
        g = footprint(peak, x0, np.full(N, cx), np.full(N, cy), heading=hd)
        out[c] = dict(gust=g, n=n, val=val)
    noise = rng.lognormal(-0.02, 0.2, (len(ELIGIBLE), N))
    return dict(x0=x0, peak=peak, rate=rate, counties=out, noise=noise)
