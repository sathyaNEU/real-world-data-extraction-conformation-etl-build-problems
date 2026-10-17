"""task152 constants and helpers shared by every generator module.

Marden-Vail Building Products, a Phoenix maker of gypsum wallboard and joint compound, owns Hadley Ranch Solar, a
40 MWac fixed-tilt plant in Pinal County, Arizona (commercial operation 20 November 2015). Its energy and commodities
desk sells each calendar year's output forward at the plant's one-year P90 under the treasury's energy risk policy.
The original modules are being replaced with bifacial modules on the existing tables and inverters from 5 October to
18 December 2026. The SCADA history runs to 30 September 2026 and was pulled on 6 October 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math
from zoneinfo import ZoneInfo

import numpy as np

SEED = 1520417

COMPANY = "Marden-Vail Building Products"
COMPANY_SHORT = "Marden-Vail"
PLANT = "Hadley Ranch Solar"
CONTRACTOR = "Tresco Field Services"
DISTRICT = "Vado Seco Irrigation and Power District"
DISTRICT_SHORT = "VSIPD"
PROVIDER = "Clearfield Solar Resource"
OLD_MAKER = "Kellerman Solar"
NEW_MAKER = "Corvane Solar"
COUNTERPARTY = "Westmark Power Trading LLC"

PEOPLE = {
    "desk": "Kristopher Lara",       # energy and commodities manager, brings the request (not in the prompt)
    "asset": "Selena Sloan",         # solar asset manager, the SCADA exports and the README
    "treasurer": "Caroline Barnett",  # treasurer, owner of the energy risk policy
    "site": "John Davila",           # Tresco's site supervisor, the work orders
    "test": "Laurie Howell",         # Corvane's field test engineer, the side-by-side report
    "meter": "Isabel Shaw",          # the district's meter data analyst
    "trader": "Felicia Powers",      # Westmark's origination director, the confirmations
    "tech1": "Ruben Yang",           # Tresco technician (ryang)
    "tech2": "Howard Stout",         # Tresco technician (hstout)
    "control": "Sonia Whitehead",    # Tresco control room (swhitehead)
}

TZ = ZoneInfo("America/Phoenix")    # Arizona: mountain standard time all year, UTC-7
UTC = dt.timezone.utc
LAT, LON = 32.94, -111.62           # the plant's site, Pinal County
TILT, AZIMUTH = 25.0, 180.0
ALBEDO = 0.27                       # bare desert soil and caliche between the rows

COD = dt.date(2015, 11, 20)
SCADA_CUTOVER = dt.date(2020, 3, 3)          # the replacement SCADA's first day
INV07_SWAP = dt.date(2021, 4, 15)            # inverter 07 replaced after a power-stage fire
STATION_SERVICE_END = dt.date(2024, 4, 17)   # the district's 12 kV station-service supply retired
LT_START, LT_END = dt.date(2001, 1, 1), dt.date(2025, 12, 31)   # the long-term record
HIST_END = dt.date(2026, 9, 30)              # last SCADA day
EXPORT_DATE = dt.date(2026, 10, 6)
EXPORT_STAMP = dt.datetime(2026, 10, 6, 17, 18, tzinfo=UTC)      # 10.18 am Arizona time
RIG_START, RIG_END = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
WORKS_START, WORKS_END = dt.date(2026, 10, 5), dt.date(2026, 12, 18)

# ---------------------------------------------------------------------------------------------------- the plant
N_INV = 16
INV_AC_KW = 2500.0
OLD_MOD_W = 315.0
OLD_MODS_PER_INV = 8000             # 400 strings of 20
OLD_KWP_INV = OLD_MOD_W * OLD_MODS_PER_INV / 1000.0      # 2,520 kWp
DC_OLD_KWP = OLD_KWP_INV * N_INV                          # 40,320 kWp
NEW_MOD_W = 450.0
NEW_MODS_PER_INV = 5184             # 288 strings of 18
NEW_KWP_INV = NEW_MOD_W * NEW_MODS_PER_INV / 1000.0      # 2,332.8 kWp
DC_NEW_KWP = NEW_KWP_INV * N_INV                          # 37,324.8 kWp
GAMMA_OLD = -0.0042                 # per degree C, the original modules' datasheet coefficient
GAMMA_NEW = -0.0029
BIFACIALITY = 0.80

OLD_TAGS = ["INV%02d" % (i + 1) for i in range(N_INV)]
NEW_TAGS = ["B%d-INV%d" % (i // 4 + 1, i % 4 + 1) for i in range(N_INV)]
INV07 = 6                           # index of inverter 07 (B2-INV3)
NEW_TAG_07R = "B2-INV3R"            # its replacement's tag
BLOCK_OF = [i // 4 for i in range(N_INV)]

POLICY_Z = 1.2816                   # the policy's one-year P90 multiplier
VOLUME_STEP = 1000                  # MWh, the volume is rounded down to it


def new_tag(i, d):
    if i == INV07 and d >= INV07_SWAP:
        return NEW_TAG_07R
    return NEW_TAGS[i]


# ---------------------------------------------------------------------------------------------------- helpers
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
    """Every date from a to b inclusive."""
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def us_date(d):
    """October 6, 2026."""
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)
