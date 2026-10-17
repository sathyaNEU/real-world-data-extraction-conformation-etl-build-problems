"""task153 constants and helpers shared by every generator module.

Keeble Supply Co., a Nashville wholesale distributor of janitorial, paper and foodservice-disposable supplies, runs six
yards in Tennessee: Memphis and Jackson (the West, from the 2019 purchase of Delta Paper & Chemical), Nashville and
Cookeville (the Central, Keeble's own) and Knoxville and Blountville (the East, from the 2022 purchase of Holston
Sanitary Supply). Each yard has a 20,000-gallon diesel tank and a self-serve island kept on standby since the fleet
moved to fleet cards in 2023. Overton Petroleum Co. offers up to 32 transport loads of 8,000 net gallons for
14 September to 8 November 2026. The data were pulled on Friday 28 August 2026 and run to Thursday 27 August.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math
from zoneinfo import ZoneInfo

import numpy as np

SEED = 1530828

COMPANY = "Keeble Supply Co."
WEST_CO = "Delta Paper & Chemical"
EAST_CO = "Holston Sanitary Supply"
JOBBER = "Overton Petroleum Co."
JOBBER_SHORT = "Overton"
WEST_NET = "Riverbend Travel Plazas"          # the truck-stop chain behind Delta's direct-bill account
CENTRAL_NET = "Crossroads Fleet Card"         # Keeble's network fleet card
EAST_NET = "Smoky Mountain Petroleum Marketers"  # the marketers' group behind Holston's card
RACK_SERVICE = "TriState Rack Report"          # the published contract rack average both sides quote

PEOPLE = {
    "jobber": "Theresa Mercado",     # Overton's commercial account manager: the offer and the 2025 letters
    "fleet": "Gabriel Wyatt",        # Keeble's fleet services manager: the unit list, the yard notes, the README
    "controller": "Dennis Stewart",  # Keeble's controller: the card agreements' cover notes
}

CENTRAL = ZoneInfo("America/Chicago")
EASTERN = ZoneInfo("America/New_York")
UTC = dt.timezone.utc

HIST_START = dt.date(2024, 9, 1)
HIST_END = dt.date(2026, 8, 27)
EXPORT_DATE = dt.date(2026, 8, 28)
EXPORT_STAMP = dt.datetime(2026, 8, 28, 13, 42, tzinfo=UTC)       # 8.42 am Central
OFFER_DATE = dt.date(2026, 8, 26)
COUNT_DUE = dt.date(2026, 9, 4)
WIN_START, WIN_END = dt.date(2026, 9, 14), dt.date(2026, 11, 8)
GEO_START = dt.date(2026, 3, 1)               # the telematics service keeps 180 days of geofence history
BASE_END = dt.date(2026, 8, 23)               # the last complete week before the pull (Monday 17 to Sunday 23 August)
PROG = {                                      # the two 2025 island programmes
    "JXN": (dt.date(2025, 3, 10), dt.date(2025, 5, 29)),
    "KNX": (dt.date(2025, 6, 9), dt.date(2025, 8, 22)),
}
ASK_MONTHS = [(2026, 5), (2026, 6), (2026, 7)]  # Ask A: May, June and July 2026

LOAD_NET = 8000.0
OFFER_MAX = 32
OFFER_ADDER = 0.019                            # dollars per net gallon over the rack average, delivered
TANK_CAP = 20000.0
TANK_FILL_LIMIT = 18000.0                      # 90 per cent, the overfill alarm
TANK_HEEL = 600.0

# card agreement terms, dollars per gallon over the rack average for the site's terminal (taxes billed at cost)
TERMS = {
    "West": {"margin": 0.119, "fee": 0.0},
    "Central": {"margin": 0.084, "fee": 0.015},
    "East": {"margin": 0.127, "fee": 0.0},
}
PROMO_2025 = {"JXN": 0.024, "KNX": 0.016}      # 2025 promotional adders over Overton's posting in effect at lifting
SPLIT_DROP_CHARGE = 62.50
FREIGHT_ZONE_ERR = 0.012                       # the July 2025 freight-zone charge billed in error at Knoxville

# ------------------------------------------------------------------------------------------------- yards and lots
YARDS = ["MEM", "JXN", "NSH", "CKV", "KNX", "TRI"]
YARD = {
    "MEM": dict(branch=21, city="Memphis", name="Memphis", account="West", terminal="Memphis", tz=CENTRAL,
                lat=35.0412, lon=-89.9631, addr="4410 Getwell Rd, Memphis, TN 38118"),
    "JXN": dict(branch=24, city="Jackson", name="Jackson", account="West", terminal="Memphis", tz=CENTRAL,
                lat=35.6352, lon=-88.8713, addr="117 Industrial Park Dr, Jackson, TN 38301"),
    "NSH": dict(branch=31, city="Nashville", name="Nashville", account="Central", terminal="Nashville", tz=CENTRAL,
                lat=36.1107, lon=-86.7202, addr="2650 Couchville Pike, Nashville, TN 37217"),
    "CKV": dict(branch=35, city="Cookeville", name="Cookeville", account="Central", terminal="Nashville", tz=CENTRAL,
                lat=36.1384, lon=-85.4612, addr="1290 Interstate Dr, Cookeville, TN 38501"),
    "KNX": dict(branch=41, city="Knoxville", name="Knoxville", account="East", terminal="Knoxville", tz=EASTERN,
                lat=35.9783, lon=-83.8842, addr="5320 Middlebrook Pike, Knoxville, TN 37921"),
    "TRI": dict(branch=46, city="Blountville", name="Blountville", account="East", terminal="Knoxville", tz=EASTERN,
                lat=36.4687, lon=-82.4021, addr="1915 Hwy 75, Blountville, TN 37617"),
}
LOTS = {
    "SPARTA": dict(name="Sparta lot", lat=35.9358, lon=-85.4652, yard="CKV"),
    "CROSSVILLE": dict(name="Crossville lot", lat=35.9512, lon=-85.0286, yard="CKV"),
}
ACCOUNTS = ["West", "Central", "East"]
ACCOUNT_YARDS = {"West": ["MEM", "JXN"], "Central": ["NSH", "CKV"], "East": ["KNX", "TRI"]}

# ------------------------------------------------------------------------------------------------- vehicle specs
# model code: (make and model, body, fuel tank gallons, typical reserve on a run that outlasts a tankful)
MODELS = {
    "SPR25": ("Mercedes-Benz Sprinter 2500 cargo 170", "van", 24.5, 3.0),
    "NRR19": ("Isuzu NRR 19,500 GVW 20 ft box", "box", 40.0, 6.0),
    "M2B26": ("Freightliner M2 106 26 ft box", "box", 56.0, 7.0),
    "CAS1D": ("Freightliner Cascadia 116 day cab", "daycab", 200.0, 25.0),
    "T68SL": ("Kenworth T680 76 in sleeper", "sleeper", 300.0, 32.0),
}

# yard -> list of (count, model, duty, base gallons per driving day)
FLEET = {
    "MEM": [(18, "SPR25", "metro", 14.0), (5, "NRR19", "metro", 23.0), (6, "M2B26", "metro", 26.6)],
    "JXN": [(4, "NRR19", "metro", 21.0), (6, "M2B26", "metro", 22.6), (9, "CAS1D", "dayrun", 86.5),
            (2, "T68SL", "loop3", 92.0)],
    "NSH": [(6, "NRR19", "metro", 23.0), (7, "M2B26", "metro", 25.0), (15, "T68SL", "dbl2", 94.5)],
    "CKV": [(32, "SPR25", "sat", 16.0), (8, "M2B26", "metro", 22.0)],
    "KNX": [(14, "SPR25", "metro", 13.0), (8, "T68SL", "loop1x2", 84.0), (2, "T68SL", "loop4", 112.0)],
    "TRI": [(4, "M2B26", "metro", 22.0), (11, "T68SL", "loop4", 112.0)],
}
SPARES = {"NSH": [(2, "M2B26")]}              # spare box trucks, on the list, no runs in 2026

# company holidays (no runs)
HOLIDAYS = {
    dt.date(2024, 9, 2), dt.date(2024, 11, 28), dt.date(2024, 11, 29), dt.date(2024, 12, 24), dt.date(2024, 12, 25),
    dt.date(2025, 1, 1), dt.date(2025, 5, 26), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 11, 27),
    dt.date(2025, 11, 28), dt.date(2025, 12, 24), dt.date(2025, 12, 25), dt.date(2026, 1, 1), dt.date(2026, 5, 25),
    dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 11, 26), dt.date(2026, 11, 27),
}

# monthly fuel factor (cold mornings and summer air conditioning, small)
SEASON = {1: 1.028, 2: 1.022, 3: 1.006, 4: 0.994, 5: 0.996, 6: 1.008, 7: 1.016, 8: 1.014, 9: 1.000, 10: 0.992,
          11: 1.004, 12: 1.020}

STATE_TAX = {"TN": 0.274, "MS": 0.18, "AR": 0.285, "KY": 0.246, "VA": 0.303, "NC": 0.405, "GA": 0.369, "AL": 0.31,
             "WV": 0.357, "MO": 0.245}
FET = 0.244


# ------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=16).hexdigest()[:n]


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def floor_clearance(x, step):
    """For a figure rounded down to step: the distance from x to the nearer edge of its floor bin, share of step."""
    f = x / step - math.floor(x / step)
    return min(f, 1.0 - f)


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def working(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def local_dt(d, hours, tz):
    """A local datetime on date d at a fractional hour (may run past 24 into the next day)."""
    base = dt.datetime(d.year, d.month, d.day, tzinfo=tz)
    return base + dt.timedelta(seconds=round(hours * 3600))


def to_utc(t):
    return t.astimezone(UTC)


MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def us_date(d):
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)


def haversine_mi(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
