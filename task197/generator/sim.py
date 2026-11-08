"""task197 architecture 2: the clean truth of the world.

The poison data network's watched over-the-counter products. Each product's packs are bought day by day
(the retail scan sales), sit in households and leave them at the product's own pace (finished by dosing or
thrown out), and a young child's accidental exposure arises from a pack that is in the home. A packaging
change alters the risk a pack carries from the day the changed pack is on sale; the packs already in homes
keep their old packaging.

Nothing here is shipped. build.py cuts the pack from these arrays.
"""
import datetime as dt
import numpy as np
from scipy.signal import lfilter

SEED = 1970418                      # the pack's own streams (cases, scan splits, antidotes, lookups)
TRUTH_SEED = 13                     # the clean truth's purchases and exposures
DAY0 = dt.date(2008, 1, 6)          # a Sunday: the scan provider's period 1 of 2008 opens here
END = dt.date(2026, 10, 31)         # last day the enquiry export covers
NDAYS = (END - DAY0).days + 1
MONTH_DAYS = 30.4375
EXPORT_FROM = dt.date(2019, 1, 1)   # first day the enquiry export carries
AS_OF = dt.date(2026, 11, 6)        # the referral's working date (a Friday)
PULL = dt.date(2026, 11, 2)         # the enquiry export and the scan delivery were pulled on this Monday
CHANGE_FROM, CHANGE_TO = dt.date(2024, 1, 1), dt.date(2025, 9, 30)   # the procedure's change range
REFERRAL_CLOSE = dt.date(2026, 11, 27)

DAYS = np.array([DAY0 + dt.timedelta(days=i) for i in range(NDAYS)])
DOY = np.array([d.timetuple().tm_yday for d in DAYS])
YEARS = np.array([d.year for d in DAYS])
MONTHS = np.array([d.month for d in DAYS])


def day_index(d):
    return (d - DAY0).days


def month_key(d):
    return d.year * 12 + d.month - 1


MKEY = np.array([month_key(d) for d in DAYS])

# Products on the watch list. L: mean months a pack stays in a home (geometric drain); base: packs a month
# at full distribution before any market event; amp/peak: seasonal swing of sales and the month it peaks;
# expo: under-six accidental exposures a month the product carries at its base level (sets the per-pack risk);
# change: the date the changed pack was first on retail sale; m: the risk a changed pack carries against an
# old one; lift: the sales step that came with the change. Market events: a "boom" multiplies sales between
# two dates (a value under one is a supply gap); "growth" and "decline" move sales linearly and hold.
PRODUCTS = [
    # junior fever medicine: a 2017-18 production stoppage, a competitor's 2021-22 winter stock-out, and a
    # quarter more packs sold with the new cap
    dict(code="FKJ", L=17.0, base=60000, amp=0.45, peak=1, expo=320.0, launch=dt.date(2009, 4, 20),
         change=dt.date(2024, 9, 16), m=1.85, lift=1.25,
         events=[("boom", dt.date(2017, 10, 1), dt.date(2018, 9, 30), 0.5),
                 ("boom", dt.date(2021, 10, 1), dt.date(2022, 1, 31), 1.4)]),
    # sleep aid: the 2020 insomnia surge; the blister pack sold far fewer packs than the bottle
    dict(code="DOZ", L=16.0, base=40000, amp=0.15, peak=12, expo=500.0, launch=dt.date(2011, 8, 1),
         change=dt.date(2024, 3, 11), m=1.0, lift=0.55,
         events=[("boom", dt.date(2020, 3, 15), dt.date(2021, 2, 28), 1.9)]),
    dict(code="GUM", L=5.0, base=80000, amp=0.25, peak=9, expo=300.0, launch=dt.date(2016, 5, 2),
         change=dt.date(2025, 2, 3), m=1.00, lift=1.00,
         events=[("growth", dt.date(2019, 1, 1), dt.date(2022, 12, 31), 0.36),
                 ("growth", dt.date(2023, 1, 1), dt.date(2025, 12, 31), 0.55)]),
    dict(code="EYE", L=3.0, base=35000, amp=0.45, peak=5, expo=350.0, launch=dt.date(2008, 10, 13),
         change=dt.date(2024, 11, 4), m=1.00, lift=1.00,
         events=[("decline", dt.date(2023, 9, 1), dt.date(2023, 11, 30), -0.66)]),
    # nicotine lozenge: a 2022 supply gap; the pocket blister pack holds fewer lozenges, so packs sold tripled
    dict(code="NIC", L=3.0, base=70000, amp=0.30, peak=1, expo=400.0, launch=dt.date(2012, 2, 6),
         change=dt.date(2025, 4, 14), m=1.12, lift=3.0,
         events=[("boom", dt.date(2022, 3, 1), dt.date(2022, 6, 30), 0.5)]),
    dict(code="IBC", L=12.0, base=65000, amp=0.28, peak=1, expo=500.0, launch=dt.date(2010, 6, 14),
         change=dt.date(2025, 6, 23), m=1.00, lift=0.75, events=[]),
    # chest rub: the 2022-23 respiratory winter
    dict(code="VAP", L=12.0, base=30000, amp=0.45, peak=1, expo=450.0, launch=dt.date(2013, 3, 4),
         change=dt.date(2024, 6, 10), m=1.00, lift=0.75,
         events=[("boom", dt.date(2022, 11, 1), dt.date(2023, 1, 31), 1.8)]),
    dict(code="CGH", L=10.0, base=45000, amp=0.55, peak=1, expo=400.0, launch=dt.date(2009, 7, 27),
         change=dt.date(2025, 8, 25), m=1.00, lift=1.00,
         events=[("decline", dt.date(2017, 1, 1), dt.date(2026, 10, 31), -0.30)]),
    dict(code="FKI", L=16.0, base=50000, amp=0.25, peak=1, expo=190.0, launch=dt.date(2009, 4, 20),
         change=None, m=1.0, lift=1.0, events=[]),
    dict(code="ALC", L=14.0, base=40000, amp=0.45, peak=5, expo=80.0, launch=dt.date(2014, 9, 8),
         change=None, m=1.0, lift=1.0, events=[]),
    dict(code="IBT", L=24.0, base=90000, amp=0.10, peak=1, expo=120.0, launch=dt.date(2010, 6, 14),
         change=None, m=1.0, lift=1.0, events=[]),
    dict(code="FER", L=3.0, base=45000, amp=0.00, peak=1, expo=75.0, launch=dt.date(2011, 11, 21),
         change=None, m=1.0, lift=1.0, events=[]),
]
BYCODE = {p["code"]: p for p in PRODUCTS}
CANDIDATES = [p["code"] for p in PRODUCTS if p["change"] is not None]
CHANGEOVER_DAYS = 42      # old packs on the shelf sell through over six weeks after the first sale


def sales_rate(p):
    """Expected packs bought per day, before Poisson noise."""
    t = np.arange(NDAYS)
    launch = day_index(p["launch"])
    ramp = np.clip((t - launch) / 365.0, 0.0, 1.0) * 0.8 + 0.2
    ramp[t < launch] = 0.0
    season = 1.0 + p["amp"] * np.cos(2 * np.pi * (DOY - (p["peak"] * 30.4 - 15)) / 365.25)
    path = np.ones(NDAYS)
    for kind, a, b, x in p["events"]:
        ia, ib = day_index(a), day_index(min(b, END))
        if kind == "boom":
            path[(t >= ia) & (t <= ib)] *= x
        else:   # growth or decline: linear in time between a and b, held after b
            frac = np.clip((t - ia) / max(ib - ia, 1), 0.0, 1.0)
            path *= 1.0 + x * frac
    if p["change"] is not None:
        ic = day_index(p["change"])
        step = np.clip((t - ic) / CHANGEOVER_DAYS, 0.0, 1.0)
        path *= 1.0 + (p["lift"] - 1.0) * step
    # a small weekly scan pattern (weekend shopping); four-weekly periods hold whole weeks so it washes out
    wd = np.array([d.weekday() for d in DAYS])
    week = np.where(wd == 5, 1.28, np.where(wd == 6, 1.12, 0.92))
    return p["base"] / MONTH_DAYS * ramp * season * path * week


def new_share(p):
    """Share of a day's purchases that carry the changed packaging."""
    if p["change"] is None:
        return np.zeros(NDAYS)
    t = np.arange(NDAYS)
    ic = day_index(p["change"])
    return np.clip((t - ic + 1) / CHANGEOVER_DAYS, 0.0, 1.0)


def drain(L):
    return np.exp(-1.0 / (L * MONTH_DAYS))


def stock_from(purchases, L):
    """Packs in homes at the end of each day: geometric drain at the product's own pace, nothing before launch."""
    return lfilter([1.0], [1.0, -drain(L)], purchases)


def simulate(seed=TRUTH_SEED):
    rng = np.random.default_rng(seed)
    world = {}
    for p in PRODUCTS:
        r = sales_rate(p)
        buys = rng.poisson(r).astype(float)
        share = new_share(p)
        buys_new = rng.binomial(buys.astype(int), share).astype(float)
        buys_old = buys - buys_new
        s_old = stock_from(buys_old, p["L"])
        s_new = stock_from(buys_new, p["L"])
        # per-pack daily risk set from the product's base level: base packs a month held for L months
        h = p["expo"] / (p["base"] * p["L"] * MONTH_DAYS)
        lam = h * (s_old + p["m"] * s_new)
        expo = rng.poisson(lam)
        world[p["code"]] = dict(rate=r, buys=buys, buys_new=buys_new, s_old=s_old, s_new=s_new, h=h,
                                lam=lam, expo=expo, cf_lam=h * (s_old + s_new))
    return world


def months_between(a_key, b_key):
    return list(range(a_key, b_key + 1))


def window(code):
    """The twelve calendar months after the month the changed pack first reached retail sale."""
    c = BYCODE[code]["change"]
    k0 = month_key(c) + 1
    return list(range(k0, k0 + 12))


def key_to_date(k):
    return dt.date(k // 12, k % 12 + 1, 1)
