"""task485's world: Lorrimere District's dwellings, households and their electors on the registers published each
1 December from 2014 to 2032, the council's completions to 30 September 2026 and its housing trajectory beyond.

A dwelling's household has a number of eligible adults; each adult who registers joins the register at one of the
canvasses after the dwelling is first in use on 31 August (or on rolling registration before the first published
register), and households turn over, the incoming one joining the same way. Everything downstream (the pack, the
golden, the checks) reads build()."""
import numpy as np

SEED = 485
FIRST_REG, LAST_SHIP, HORIZON = 2014, 2025, 2032
CUT = (2026, 9)                       # completions monitoring and trajectory to 30 September 2026
ADULTS = {"house": ([0, 1, 2, 3, 4, 5], [0.03, 0.18, 0.45, 0.22, 0.10, 0.02]),
          "flat": ([0, 1, 2, 3, 4], [0.04, 0.42, 0.42, 0.10, 0.02])}
P_REGISTER = 0.92                     # an eligible adult who ever registers at the address
DELAY = [0.40, 0.25, 0.15, 0.09, 0.06, 0.03, 0.02]   # the canvass (1st, 2nd, ...) at which a registering adult joins
ROLLING = 0.07                        # in use after 31 August: share of registering adults on the next 1 December register
TURNOVER = {"house": 0.07, "flat": 0.14}             # households moving out a year
COUNCIL_SIZE = 43

# ward code, name, councillors, role in the design (A: estates finished 2024-2026 still joining; B: sites due 2030-2032;
# C1/C2: outside the line on every route; E: inside on every route), polling districts
WARDS = [
    ("LAB", "Lorrimere Abbey", 3, "E", 3), ("LCA", "Lorrimere Castle", 2, "E", 2), ("LNO", "Lorrimere North", 2, "B", 3),
    ("LWE", "Lorrimere West", 3, "A", 3), ("CCE", "Caldenstow Central", 2, "E", 2), ("CPK", "Caldenstow Park", 2, "A", 3),
    ("QUE", "Quenbrook", 1, "A", 2), ("TIB", "Tibberfield", 1, "B", 2), ("EBB", "Ebborby", 1, "C1", 2),
    ("KET", "Kettermere", 3, "C2", 4), ("SEL", "Selwarstow", 2, "E", 2), ("VEL", "Vellanridge", 2, "E", 3),
    ("OST", "Ostenworth", 2, "E", 2), ("HAR", "Harnwick", 1, "E", 2), ("BRE", "Brenningholme", 3, "E", 3),
    ("FAU", "Faulcott", 1, "E", 2), ("GRI", "Griselbrook", 2, "E", 3), ("DOR", "Dorranford", 3, "E", 3),
    ("PEL", "Pellanham", 1, "E", 2), ("ROT", "Rothenridge", 2, "E", 3), ("STE", "Stellfield", 2, "E", 3),
    ("VAR", "Vardonham", 1, "E", 2), ("YAR", "Yarnmere", 1, "E", 2)]

# sites: ward, site name, houses, flats, completions by monitoring year (April to March) as shares; past years are built
SITES = [
    ("CPK", "Caldenstow Park phase 2", 700, 160, {2024: .35, 2025: .40, 2026: .25}),
    ("LWE", "Mill Lane, Lorrimere", 760, 0, {2024: .30, 2025: .40, 2026: .30}),
    ("LWE", "The Wharf, Lorrimere", 0, 300, {2025: 1.0}),
    ("QUE", "Quenbrook Farm", 420, 0, {2024: .45, 2025: .55}),
    ("LNO", "North Lorrimere urban extension", 640, 0, {2030: .30, 2031: .40, 2032: .30}),
    ("TIB", "Tibberfield Fields", 380, 0, {2031: .50, 2032: .50}),
    ("KET", "Kettermere Grange", 900, 180, {2026: .15, 2027: .35, 2028: .35, 2029: .15}),
    ("LAB", "Station Quarter", 0, 180, {2028: 1.0}),
    ("DOR", "Dorranford Road", 200, 0, {2027: .5, 2028: .5}),
    ("STE", "Stellfield Meadows", 140, 60, {2026: .5, 2027: .5}),
    ("BRE", "Brenningholme Lea", 220, 0, {2029: .5, 2030: .5}),
    ("ROT", "Rothenridge Way", 160, 0, {2021: .5, 2022: .5}),
    ("VEL", "Vellan Court", 0, 90, {2023: 1.0}),
    ("SEL", "Selwar Green", 120, 0, {2020: .6, 2021: .4}),
    ("GRI", "Griselbrook Park", 260, 40, {2016: .4, 2017: .6}),
    ("CCE", "Caldenstow Gate", 180, 120, {2018: .5, 2019: .5}),
    ("OST", "Ostenworth Rise", 150, 0, {2015: .5, 2016: .5}),
    ("LCA", "Castle Mews", 0, 110, {2019: 1.0}),
    ("HAR", "Harnwick Close", 60, 0, {2022: 1.0}),
    ("DOR", "Dorran Fields", 240, 0, {2014: .5, 2015: .5}),
    ("LAB", "Abbey Gardens", 90, 70, {2017: 1.0}),
    ("VAR", "Vardon Orchard", 70, 0, {2020: 1.0}),
    ("PEL", "Pellan View", 40, 0, {2023: 1.0}),
    ("FAU", "Faulcott Barns", 24, 0, {2024: 1.0}),
    ("YAR", "Yarnmere Lane", 36, 0, {2021: 1.0}),
    ("KET", "Kettermere Road", 130, 0, {2018: .5, 2019: .5}),
    ("CPK", "Caldenstow Park phase 1", 520, 90, {2019: .3, 2020: .4, 2021: .3}),
]
# target variance of each ward on the settled-ratio route (the default path), which fixes each ward's settled stock
TARGET_DEFAULT = {"LAB": -2.0, "LCA": -5.5, "LNO": 14.5, "LWE": 7.0, "CCE": -3.5, "CPK": 4.5, "QUE": 4.0, "TIB": 15.5,
                  "EBB": -13.0, "KET": 16.5, "SEL": -6.0, "VEL": -4.5, "OST": -5.5, "HAR": 0.0, "BRE": -3.0, "FAU": -8.0,
                  "GRI": -4.0, "DOR": -3.0, "PEL": -1.5, "ROT": -5.0, "STE": -3.5, "VAR": -1.0, "YAR": -7.0}
FLAT_SHARE = {"LAB": .30, "LCA": .34, "LNO": .14, "LWE": .20, "CCE": .28, "CPK": .16, "QUE": .12, "TIB": .10, "EBB": .08,
              "KET": .17, "SEL": .15, "VEL": .25, "OST": .12, "HAR": .09, "BRE": .18, "FAU": .07, "GRI": .22, "DOR": .16,
              "PEL": .11, "ROT": .18, "STE": .21, "VAR": .10, "YAR": .09}

# each ward's dwellings in use before 2014, sized by design_tune.py so the default route lands each ward at its target
SETTLED = {
    "LAB": {"house": 3150, "flat": 1350},
    "LCA": {"house": 1995, "flat": 1028},
    "LNO": {"house": 2509, "flat": 409},
    "LWE": {"house": 3472, "flat": 868},
    "CCE": {"house": 2036, "flat": 792},
    "CPK": {"house": 1722, "flat": 328},
    "QUE": {"house": 1158, "flat": 158},
    "TIB": {"house": 1288, "flat": 143},
    "EBB": {"house": 1196, "flat": 104},
    "KET": {"house": 3500, "flat": 717},
    "SEL": {"house": 2356, "flat": 416},
    "VEL": {"house": 2241, "flat": 747},
    "OST": {"house": 2385, "flat": 325},
    "HAR": {"house": 1313, "flat": 130},
    "BRE": {"house": 3523, "flat": 773},
    "FAU": {"house": 1258, "flat": 95},
    "GRI": {"house": 2124, "flat": 599},
    "DOR": {"house": 3387, "flat": 645},
    "PEL": {"house": 1290, "flat": 159},
    "ROT": {"house": 2280, "flat": 500},
    "STE": {"house": 2251, "flat": 598},
    "VAR": {"house": 1288, "flat": 143},
    "YAR": {"house": 1209, "flat": 120},
}


def months_of(my):
    """(year, month) of each month of monitoring year my, April my to March my + 1"""
    return [(my, m) for m in range(4, 13)] + [(my + 1, m) for m in range(1, 4)]


def mindex(y, m):
    return y * 12 + (m - 1)


def ym(i):
    return i // 12, i % 12 + 1


def first_canvass(i):
    """the first canvass a household in residence from month index i is canvassed at (in residence by 31 August)"""
    y, m = ym(i)
    return y if m <= 8 else y + 1


class Household:
    __slots__ = ("arrive", "leave", "adults", "fc")

    def __init__(self, arrive, leave, adults, fc):
        self.arrive, self.leave, self.adults, self.fc = arrive, leave, adults, fc


def draw_household(rng, typ, arrive):
    """eligible adults with the register year each joins (None: never registers at this address)"""
    vals, probs = ADULTS[typ]
    n = int(rng.choice(vals, p=probs))
    fc = first_canvass(arrive)
    ay, am = ym(arrive)
    adults = []
    for _ in range(n):
        if rng.random() >= P_REGISTER:
            adults.append(None)
            continue
        if am >= 9 and am <= 10 and rng.random() < ROLLING:
            adults.append(ay)               # on rolling registration before the next published register
            continue
        j = int(rng.choice(len(DELAY), p=DELAY))
        adults.append(fc + j)
    q = TURNOVER[typ]
    pm = 1.0 - (1.0 - q) ** (1.0 / 12.0)
    tenure = int(rng.geometric(pm))
    return Household(arrive, arrive + tenure, adults, fc)


def history(rng, typ, first_in_use, end_year=HORIZON):
    """the households of one dwelling from its first month in use to the end of end_year"""
    end = mindex(end_year, 12)
    hh = []
    t = first_in_use
    while t <= end:
        h = draw_household(rng, typ, t)
        hh.append(h)
        t = h.leave + int(rng.integers(1, 4))            # a void of one to three months between households
    return hh


def count_on(hh, year):
    """electors of the household in residence in October (applications determined by 31 October reach the register
    published 1 December)"""
    ref = mindex(year, 10)
    for h in hh:
        if h.arrive <= ref < h.leave:
            return sum(1 for a in h.adults if a is not None and a <= year)
    return 0


def windfall_sites(seed=SEED + 9):
    """small sites (infill, conversions, a barn or two): completed each monitoring year from 2014/15, and with
    permission for 2026/27 to 2028/29; (ward, name stem, houses, flats, {monitoring year: 1.0})"""
    rng = np.random.default_rng(seed)
    codes = [w[0] for w in WARDS]
    out = []
    for my in range(2014, 2029):
        for _ in range(int(rng.integers(5, 10)) if my <= 2025 else int(rng.integers(3, 7))):
            c = codes[int(rng.integers(0, len(codes)))]
            if rng.random() < 0.25:
                nh, nf = 0, int(rng.integers(2, 9))
                kind = "conversion"
            else:
                nh, nf = int(rng.integers(1, 10)), 0
                kind = ["infill", "infill", "former garage site", "barn conversion"][int(rng.integers(0, 4))]
            out.append((c, kind, nh, nf, {my: 1.0}))
    return out


def all_sites():
    return list(SITES) + windfall_sites()


def site_plan(phasing, n):
    """the trajectory's dwellings by monitoring year, whole numbers summing to n (largest remainders)"""
    yrs = sorted(phasing)
    raw = [phasing[y] * n for y in yrs]
    base = [int(np.floor(x)) for x in raw]
    rest = n - sum(base)
    order = sorted(range(len(yrs)), key=lambda i: -(raw[i] - base[i]))
    for i in order[:rest]:
        base[i] += 1
    return dict(zip(yrs, base))


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    dw = []                                # one dict per dwelling
    years = list(range(FIRST_REG, HORIZON + 1))
    for code, name, cl, role, npd in WARDS:
        pd_share = rng.dirichlet(np.full(npd, 6.0))
        for typ in ("house", "flat"):
            n = SETTLED[code][typ]
            pds = rng.choice(npd, size=n, p=pd_share)
            for i in range(n):
                start = mindex(1980, 1) - int(rng.integers(0, 120))
                hh = history(rng, typ, start)
                dw.append(dict(ward=code, pd=int(pds[i]), type=typ, site=None, done=None, inuse=None, hh=hh))
    for si, (code, sname, nh, nf, phasing) in enumerate(all_sites()):
        npd = [w for w in WARDS if w[0] == code][0][4]
        pd = int(rng.integers(0, npd)) if si % 3 else npd - 1
        for typ, n in (("house", nh), ("flat", nf)):
            if n == 0:
                continue
            plan = site_plan(phasing, n)
            for my, k in plan.items():
                mlist = months_of(my)
                for j in range(k):
                    y, m = mlist[int(rng.integers(0, 12))] if my <= 2025 else mlist[(j * 12) // max(k, 1)]
                    done = mindex(y, m)
                    lag = int(rng.choice([0, 0, 1, 1, 2, 3]))
                    inuse = done + lag
                    built = (y, m) <= CUT
                    hh = history(rng, typ, inuse) if inuse <= mindex(HORIZON, 12) else []
                    dw.append(dict(ward=code, pd=pd, type=typ, site=si, done=done, inuse=inuse, hh=hh,
                                   built=built, plan_year=my))
    for d in dw:
        d["count"] = {Y: (count_on(d["hh"], Y) if (d["inuse"] is None or d["inuse"] <= mindex(Y, 10)) else 0)
                      for Y in years}
        d.setdefault("built", True)
    return dict(dwellings=dw, years=years)
