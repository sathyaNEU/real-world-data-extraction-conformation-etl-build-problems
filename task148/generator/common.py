"""task148 constants and helpers shared by every generator module.

Tavish County Emergency Communications Agency is the county's consolidated primary PSAP. Its fiscal year runs from
1 July to 30 June. A state 911 surcharge grant has paid a fifth call-taker on the Friday and Saturday late shift
(22:00 to 02:00) since July 2024; it ends on 30 June 2027 and the FY2028 budget funds four. Halvorsen Township's 911
service moves from Wexley County Emergency Communications to the agency on 1 July 2027. The ACD export runs from
1 January 2025 to 30 September 2026 and was pulled on 6 October 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math
from zoneinfo import ZoneInfo

import numpy as np

SEED = 1482611

AGENCY = "Tavish County Emergency Communications Agency"
AGENCY_SHORT = "Tavish County ECA"
COUNTY = "Tavish County"
BOARD = "Tri-County Regional 911 Board"
TOWNSHIP = "Halvorsen Township"
NEIGHBOUR = "Wexley County Emergency Communications"

PEOPLE = {
    "ops": "Leon Carpenter",        # operations manager, brings the FY2028 late-shift request (not in the prompt)
    "qa": "Regina Holder",          # quality assurance and data analyst; the ACD exports and the README
    "planner": "William Braun",     # the regional board's planner; the volume forecast
    "finance": "Carol Bender",      # finance director; the FY2028 budget
    "callback": "Gary Dennis",      # training and callback supervisor
}

TZ = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc

HIST_START = dt.datetime(2025, 1, 1, 0, 0, tzinfo=TZ)      # first hour of the export
HIST_END = dt.datetime(2026, 10, 1, 0, 0, tzinfo=TZ)       # exclusive
CUT_WIRELESS = dt.datetime(2025, 5, 13, 6, 0, tzinfo=TZ)   # wireless, VoIP and telematics move to i3
CUT_WIRELINE = dt.datetime(2025, 5, 16, 6, 0, tzinfo=TZ)   # wireline calls leave the CAMA trunks
# planned works on the main floor in fiscal 2026: the agency answered from its backup centre, whose call-handling
# system files a call's location records under the ESInet's incident identifier rather than the call identifier
BACKUP_WINDOWS = [(dt.datetime(2025, 8, 19, 7, 0, tzinfo=TZ), dt.datetime(2025, 8, 21, 19, 0, tzinfo=TZ)),
                  (dt.datetime(2025, 11, 3, 7, 0, tzinfo=TZ), dt.datetime(2025, 11, 7, 7, 0, tzinfo=TZ)),
                  (dt.datetime(2026, 2, 9, 7, 0, tzinfo=TZ), dt.datetime(2026, 2, 14, 7, 0, tzinfo=TZ)),
                  (dt.datetime(2026, 5, 12, 7, 0, tzinfo=TZ), dt.datetime(2026, 5, 14, 7, 0, tzinfo=TZ))]


def at_backup(ts):
    return any(a.timestamp() <= ts < b.timestamp() for a, b in BACKUP_WINDOWS)


EXPORT_DATE = dt.date(2026, 10, 6)
EXPORT_STAMP = dt.datetime(2026, 10, 6, 16, 42, tzinfo=UTC)  # 11.42 am Central on 6 October 2026

# ---------------------------------------------------------------------------------------------------- the world's laws
AHT = 227.0          # mean busy time per answered call, seconds (answer to ready), exponential
# mean caller patience, seconds, exponential: the call mix of Friday and Saturday nights from 22:00 to 06:00 (bar
# districts, disturbances, third parties who give up) against the rest of the week's (traffic, alarms, medical calls
# from people who hold on)
PATIENCE_WEEKEND_NIGHT = 120.0
PATIENCE_OTHER = {"day": 630.0, "evening": 580.0, "night": 540.0}   # 06:00-18:00, 18:00-22:00, 22:00-06:00
PATIENCE = PATIENCE_WEEKEND_NIGHT    # the late shift's (the one the decision turns on)
TALK_BETA = (7.0, 3.0)
REDIAL_P = 0.20      # a hang-up is followed by a redial from the same number
REDIAL_DELAY = (4.0, 30.0)   # seconds after the hang-up: fixed part, exponential mean

# staffing blocks (local hour start, end) and the floor plan's call-takers
BLOCKS = [(2, 6, "0200-0600", 3), (6, 10, "0600-1000", 4), (10, 14, "1000-1400", 6), (14, 18, "1400-1800", 6),
          (18, 22, "1800-2200", 5)]
LATE_BLOCK = "2200-0200"
LATE_C_HIST = {"weekday": 4, "frisat": 5}   # FY2025 to FY2027: the grant pays the fifth on Friday and Saturday nights
LATE_C_FY2028 = 4

# hourly arrival model, fiscal 2026 level (calls presented per clock hour)
WEEKDAY = [15.2, 13.1, 12.4, 10.6, 9.1, 9.3, 12.2, 17.1, 23.0, 27.2, 31.1, 33.8, 35.2, 36.1, 37.9, 40.2, 41.8, 43.1,
           41.9, 38.8, 35.1, 30.2, 20.3, 17.1]
SEAS = {1: 0.902, 2: 0.861, 3: 0.913, 4: 0.958, 5: 1.041, 6: 1.122, 7: 1.183, 8: 1.152, 9: 1.047, 10: 0.968,
        11: 0.921, 12: 0.957}
HOUR_PROFILE = {22: 0.975, 23: 1.040, 0: 1.030, 1: 0.955}   # within the Friday and Saturday late shift
NIGHT_FACTOR = {4: 0.975, 5: 1.025}                          # night starting Friday (4) or Saturday (5)
GROWTH = 0.015       # a year


def trend(d):
    """Volume trend against fiscal 2026's level (1.0 in July 2025), d a date."""
    return 1.0 + GROWTH * ((d.year - 2025) + (d.month - 7) / 12.0)


# ---------------------------------------------------------------------------------------------------- calendar helpers
def night_of(loc):
    """The date of the evening a late-shift hour belongs to (00:00 and 01:00 belong to the night before)."""
    return (loc - dt.timedelta(days=1)).date() if loc.hour < 2 else loc.date()


def is_late(loc):
    return loc.hour >= 22 or loc.hour < 2


def is_frisat_late(loc):
    return is_late(loc) and night_of(loc).weekday() in (4, 5)


def is_weekend_night(loc):
    """22:00 to 06:00 of a night that starts on a Friday or a Saturday."""
    if loc.hour >= 22:
        return loc.weekday() in (4, 5)
    if loc.hour < 6:
        return (loc - dt.timedelta(days=1)).weekday() in (4, 5)
    return False


def patience_mean(loc):
    """The world's mean caller patience (seconds) for a call presented at local time loc."""
    if is_weekend_night(loc):
        return PATIENCE_WEEKEND_NIGHT
    if 6 <= loc.hour < 18:
        return PATIENCE_OTHER["day"]
    if 18 <= loc.hour < 22:
        return PATIENCE_OTHER["evening"]
    return PATIENCE_OTHER["night"]


def block_of(loc):
    """(date the block is filed under, block name) of a local datetime."""
    h = loc.hour
    if h >= 22 or h < 2:
        return night_of(loc), LATE_BLOCK
    for a, b, name, _ in BLOCKS:
        if a <= h < b:
            return loc.date(), name
    raise ValueError(loc)


def plan_c(d, block):
    if block == LATE_BLOCK:
        return LATE_C_HIST["frisat"] if d.weekday() in (4, 5) else LATE_C_HIST["weekday"]
    return {name: c for _, _, name, c in BLOCKS}[block]


def fiscal_year(d):
    return d.year + 1 if d.month >= 7 else d.year


def fiscal_quarter(d):
    return (fiscal_year(d), ((d.month - 7) % 12) // 3 + 1)


def fy_months(fy):
    return [(fy - 1, m) for m in range(7, 13)] + [(fy, m) for m in range(1, 7)]


MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def late_nights(y, m):
    """The Friday and Saturday nights that start in month (y, m), as dates."""
    out, d = [], dt.date(y, m, 1)
    while d.month == m:
        if d.weekday() in (4, 5):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def night_hours(nd):
    """The clock hours of the late shift starting on the evening of date nd, as aware local datetimes (UTC-stepped,
    so the November night carries 01:00 twice and the March night skips nothing before 02:00)."""
    start = dt.datetime(nd.year, nd.month, nd.day, 22, 0, tzinfo=TZ).astimezone(UTC)
    nxt = nd + dt.timedelta(days=1)
    end = dt.datetime(nxt.year, nxt.month, nxt.day, 2, 0, tzinfo=TZ).astimezone(UTC)
    out, t = [], start
    while t < end:
        out.append(t.astimezone(TZ))
        t += dt.timedelta(hours=1)
    return out


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


def iso_utc_ms(ts):
    """ISO 8601 UTC with milliseconds, from epoch seconds."""
    d = dt.datetime.fromtimestamp(ts, UTC)
    return d.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (d.microsecond // 1000)


def local_str(ts, fmt="%m/%d/%Y %H:%M:%S"):
    return dt.datetime.fromtimestamp(ts, UTC).astimezone(TZ).strftime(fmt)


def to_local(ts):
    return dt.datetime.fromtimestamp(ts, UTC).astimezone(TZ)
