"""task122 generator: every fixed constant of the fiction and of the build.

The per-cell effects below were solved once, offline, as a constrained least-squares problem
(session-weighted, render-weighted and replay estimators, the eight-cell guardrail, the coarse cuts,
the young-to-old spread the traffic restatement needs) and are frozen here, so a build never runs an
optimiser. Everything the pack states is computed forward from records generated with these numbers.
"""
import zlib
from datetime import date, datetime, timedelta

import numpy as np

SEED = 122

# ------------------------------------------------------------------ dates of the fiction
LOG_START = date(2026, 6, 22)          # first logged session (Monday)
LOG_END = date(2026, 9, 20)            # last logged session (Sunday)
LOG_DAYS = 91
HALF_SPLIT = date(2026, 8, 6)          # first half 22 Jun - 5 Aug, second half 6 Aug - 20 Sep
ORDERS_FROM = date(2026, 6, 1)         # orders extract starts
EXTRACT = date(2026, 10, 11)           # orders, payments, offers pulled through this date
TARIFF_CHANGE = date(2026, 9, 1)       # 0.70 + 5% until 31 Aug, 0.80 + 5% from 1 Sep
PACK_DATE = date(2026, 10, 14)         # the review folder as assembled (file mtimes)
AS_OF = date(2026, 10, 28)             # the planning meeting
SLOT_START = date(2027, 1, 4)
SLOT_END = date(2027, 3, 28)
APP_FIRST_RELEASE_2027 = date(2027, 1, 18)

# ------------------------------------------------------------------ cells
PLATFORMS = ("app", "web")
BANDS = ("<30", "30-179", "180-729", "730+")
BAND_DAYS = ((0, 29), (30, 179), (180, 729), (730, 3900))
CELL_NAMES = ["app <30", "app 30-179", "app 180-729", "app 730+",
              "web <30", "web 30-179", "web 180-729", "web 730+"]
N_CELL = np.array([11100, 20800, 29500, 35900, 6200, 12300, 16400, 18200])
BLOCK = N_CELL // 100                  # one block of sessions; each arm takes whole blocks
NBAR = np.array([4.4, 3.2, 2.5, 2.0] * 2)
NMAX = 14

# rankers: the incumbent and the six registered policies (internal letters are build-side only)
RANKERS = ["HC-24", "HC-31", "HC-33", "HC-34", "HC-36", "HC-37", "HC-39"]
LETTER = {"HC-24": "R0", "HC-31": "A", "HC-33": "B", "HC-34": "C", "HC-36": "D", "HC-37": "E", "HC-39": "F"}
POLICIES = RANKERS[1:]
NAMES = {"HC-24": "Blend v7 (production)", "HC-31": "Two-tower personaliser", "HC-33": "Velocity boost",
         "HC-34": "Session-sequence model", "HC-36": "Local pickup boost",
         "HC-37": "Sequence ranker with fresh-listing interleave", "HC-39": "Seller-diversity re-ranker"}
ANSWER = "HC-37"
STUMP = "HC-33"

# logger allocation (propensity of each ranker in each cell); rows = cells, cols = RANKERS
PI = np.array([
    [.27, .14, .12, .11, .07, .16, .13],
    [.29, .13, .12, .11, .07, .13, .15],
    [.34, .07, .10, .11, .19, .08, .11],
    [.34, .07, .10, .11, .19, .08, .11],
    [.26, .15, .12, .11, .07, .16, .13],
    [.29, .15, .12, .11, .07, .13, .13],
    [.32, .15, .12, .11, .07, .08, .15],
    [.32, .15, .12, .11, .07, .08, .15],
])
# pooled borrowed orders per 1,000 sessions the velocity boost's pinned watched listings carry, against
# the incumbent (no other ranker reads saves, so no other ranker shows a watched listing)
BORROWED_TARGET = {"HC-33": 4.73}

# incumbent in-session carousel orders per 1,000 sessions by cell, and its profile over renders
KAPPA = np.array([57, 61, 70, 74, 42, 47, 53, 57], float)
ALPHA = 0.45

# in-session lift per (cell, renders): a[c] + b * (n - nbar[c]); A has no slope in web 730+
LIFT = {
    "HC-31": ([7.159, 7.698, 7.866, 8.236, 6.889, 7.276, 7.225, -1.567], 2.7035),
    "HC-34": ([-0.200, 10.400, 11.000, 11.399, 9.300, 9.700, 10.000, 10.100], -0.6461),
    "HC-36": ([6.699, 6.936, 5.504, 5.318, 4.179, 4.353, 3.480, 3.356], 0.1507),
    "HC-37": ([7.632, 6.660, 5.585, 5.104, 7.318, 6.336, 5.347, 4.853], -0.1128),
    "HC-39": ([2.547, 2.076, 1.109, 0.910, 2.382, 1.863, 1.005, 0.805], 0.2260),
}
NO_SLOPE = {("HC-31", 7)}
# velocity boost: new-listing orders a_new[c] + b_new * (n - nbar[c]), and pinned watched-listing
# purchases B_R * pinned_per_session[c] * g(n) / E_c[g]
B_ANEW = [3.612, 3.223, -0.868, -1.061, 3.507, 3.113, -0.882, -1.080]
B_BNEW_YOUNG, B_BNEW_OLD = 3.8303, 1.6356
B_R = 19.4607
G_OF_N = {1: 1.0, 2: 0.3}              # pinned purchases happen in one- and two-render sessions

# watch lists: live watched listings at session start, Poisson means by tenure band
WATCH_LAMBDA = np.array([0.08, 0.45, 0.95, 1.30] * 2)
ANYWAY_NUM, ANYWAY_DEN = 5, 8          # share of watched listings their watcher buys within 6 days
ANYWAY_DAY_P = np.array([0.12, 0.17, 0.20, 0.30, 0.13, 0.08])   # calendar day 1..6 after the session

# background orders per buyer per day, by tenure band
BG_RATE = np.array([0.010, 0.012, 0.014, 0.016] * 2)
WINDOW_DAYS = 21                       # template-balanced orders sit within 21 days either side

# come-back tile orders: a buyer leaves the home screen open, the session closes (30 minutes without
# activity), and the buyer comes back and orders straight from a tile still on screen. The order is placed
# in the new home session the return opened, so the orders extract credits it there and the render log's
# ordered_tiles (orders placed in the session) never sees it; only the listing ties it to the tile the
# logged session served. Per 1,000 sessions, by cell, for the incumbent and every policy but the
# session-sequence model, whose buyers come back to the item through favourites or search instead. They
# are drawn from background orders the block template already places on the session's own day after it
# ends, so no order enters or leaves any window.
COMEBACK_PER_1000 = np.array([1.6, 1.5, 1.6, 1.7, 1.2, 1.2, 1.3, 1.4])
COMEBACK_NONE = ("HC-34",)
COMEBACK_MAX_S = 4 * 3600              # come-back orders land 2 minutes to 4 hours after the session closed

# purchases paid from a Vouwlijn balance: covered and charged the fee, but not captured by the payment
# provider, so they are absent from the payments export (shipped orders only)
WALLET_SHARE = 0.07
VAT_RATE = 0.21                        # VAT on the buyer-protection fee; fee income is booked excluding it

# fresh tiles: share of the six tiles on listings under 48 hours old, per served ranking
FRESH_SHARE = {"HC-24": 0.130, "HC-31": 0.136, "HC-33": 0.141, "HC-34": 0.139, "HC-37": 0.214, "HC-39": 0.152}
# the local pickup boost: fresh share by renders (its fresh local listings surface in long sessions)
D_FRESH_BY_N = {1: 0.030, 2: 0.045, 3: 0.090, 4: 0.180, 5: 0.300}

# ------------------------------------------------------------------ fee path
CATEGORIES = ["womenswear", "menswear", "kids", "shoes", "bags & accessories"]
CAT_P = [0.42, 0.17, 0.15, 0.16, 0.10]
PRICE_POINTS = np.array([4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 60, 75])
PRICE_W = np.array([2, 4, 3, 4, 7, 3, 9, 7, 5, 9, 5, 8, 3, 6, 2, 4, 3, 3, 1, 2, 1, 1], float)
SHIPPING = {"womenswear": 4.65, "menswear": 4.65, "kids": 3.25, "shoes": 6.95, "bags & accessories": 4.65}
TARIFFS = [  # (effective from, fixed EUR, per cent)
    (date(2024, 3, 1), 0.70, 5.0),
    (date(2026, 9, 1), 0.80, 5.0),
    (date(2027, 1, 4), 0.95, 5.0),
]
SLOT_FIXED_CENTS, SLOT_PCT = 80, 5     # the tariff in force for the slot (the January row was deferred)
OFFER_SHARE = 0.38                     # carousel orders bought on an accepted offer
OFFER_LAPSE = 0.22                     # accepted offers that lapsed before checkout (asking paid)
OFFER_DISC = (0.12, 0.30)              # discount range on accepted offers
PICKUP_INPERSON = {"default": 0.11, "HC-36": 0.30}   # share of orders collected and paid in person
PICKUP_INAPP = {"default": 0.04, "HC-36": 0.06}      # collected but paid in the app (fee charged)
BG_OFFER_SHARE = 0.24                  # orders away from the carousel bought on an accepted offer

# ------------------------------------------------------------------ slot traffic
SLOT_SHARE = 0.10
JAN_SURGE = (0.020, 0.010)             # extra share of the two younger bands at the January peak
ISO_WEEKS_SLOT = list(range(1, 13))    # 2027-W01..W12, planned on the same weeks of 2026
APP_WEEKS = list(range(3, 13))         # app arm starts with the 18 January release (W03)
R2_MOVED_SHARE = 0.062                 # sessions R2 moves from the two younger bands to the two older


def stream(name):
    """A generator seeded from the build seed and a stable name, so adding a stream never moves
    another one."""
    return np.random.default_rng([SEED, zlib.crc32(name.encode())])


def band_of_days(d):
    for i, (lo, hi) in enumerate(BAND_DAYS):
        if lo <= d <= hi:
            return i
    raise ValueError(d)


def render_dist(mu, nmax=NMAX):
    """Truncated geometric renders-per-session distribution tilted to mean mu."""
    n = np.arange(1, nmax + 1)
    p = 1.0 / mu
    P = p * (1 - p) ** (n - 1)
    P /= P.sum()
    for _ in range(400):
        m = (P * n).sum()
        if abs(m - mu) < 1e-12:
            break
        t = np.exp(0.5 * (mu - m) * (n - m) / ((P * (n - m) ** 2).sum()))
        P = P * t
        P /= P.sum()
    return P


def at(d, seconds):
    """A naive local datetime from a date and seconds after its midnight."""
    return datetime(d.year, d.month, d.day) + timedelta(seconds=int(seconds))
