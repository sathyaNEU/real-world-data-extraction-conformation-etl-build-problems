"""task271 constants and helpers shared by every generator module.

The Pelloran Plateau Fisheries Society, a non-profit, raises rainbow trout at its Quillet Creek Hatchery and stocks the
lakes of the Pelloran Plateau in the British Columbia interior. Each summer it runs a creel survey: Vellacott Air flies
two count loops over every lake on the survey days, and summer clerks interview anglers as they leave a lake. The
society's stocking allocation policy puts a lake into the high-use tier for a stocking year when anglers fished it for
500 or more angler-hours per hectare in the open-water season before. The board approves the 2027 plan on 19 November
2026 and the society files its 2027 stocking application with the province by 1 December 2026.

The seed was fixed by rule before any data was generated: the task number, then the plan's month and day."""
from __future__ import annotations

import csv
import datetime as dt
import io
import math

import numpy as np

SEED = 2711119

SOCIETY = "Pelloran Plateau Fisheries Society"
SOCIETY_SHORT = "PPFS"
HATCHERY = "Quillet Creek Hatchery"
OPERATOR = "Vellacott Air"
PLATEAU = "Pelloran Plateau"

PEOPLE = {
    "stocking": "Katrina Newman",   # stocking program manager: the requester, takes the 2027 plan to the board
    "creel": "Luis Thomas",         # creel survey coordinator: the protocol, the counts and the interviews
    "hatchery": "Robin Fields",     # hatchery manager: trip sheets, raceway samples, the drop crew
}
CLERKS = ["JMK", "SRP", "AWT", "NLB"]   # the 2026 creel clerks' initials as their tablets record them
OBSERVERS = ["L. Thomas", "D. Okafor"]

# ------------------------------------------------------------------------------------------------- calendar
SEASON_START = dt.date(2026, 5, 15)
SEASON_END = dt.date(2026, 8, 31)
SEASON_DAYS = [SEASON_START + dt.timedelta(d) for d in range((SEASON_END - SEASON_START).days + 1)]
HOLIDAYS = {dt.date(2026, 5, 18), dt.date(2026, 7, 1), dt.date(2026, 8, 3)}   # Victoria Day, Canada Day, BC Day
DAY_OPEN = 5.0      # the plateau's angling day runs 05:00 to 22:00
DAY_CLOSE = 22.0
DAY_HOURS = DAY_CLOSE - DAY_OPEN
THRESHOLD = 500     # angler-hours per hectare for the high-use tier
EXPORT_DATE = dt.date(2026, 10, 23)          # the creel survey's season files were exported
ASOF = dt.date(2026, 10, 26)                 # the stocking program manager's working date
BOARD_DATE = dt.date(2026, 11, 19)
FILING_DATE = dt.date(2026, 12, 1)
POLICY_DATE = dt.date(2026, 3, 12)           # the board adopted the allocation policy's 2026 revision
PROTOCOL_DATE = dt.date(2026, 4, 28)
RACEWAY_RENUMBER = dt.date(2026, 7, 6)       # the hatchery's new raceway bank came into use
TRIPSHEET_SWITCH = dt.date(2026, 8, 17)      # the drivers' trip sheet template took the new raceway numbers
PDT = dt.timezone(dt.timedelta(hours=-7))
UTC = dt.timezone.utc
LAT, LON = 50.62, -120.48                    # the plateau's centre, for sunrise and sunset


def day_type(d):
    return "weekend" if (d.weekday() >= 5 or d in HOLIDAYS) else "weekday"


def stratum(d):
    return (d.month, day_type(d))


def sun_times(d):
    """Sunrise and sunset in PDT decimal hours (NOAA's simple solar position, refraction included)."""
    n = d.timetuple().tm_yday
    g = 2 * math.pi / 365.0 * (n - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g)
                    - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lat = math.radians(LAT)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl))
                                - math.tan(lat) * math.tan(decl)))
    sunrise_utc = 720 - 4 * (LON + ha) - eqt
    sunset_utc = 720 - 4 * (LON - ha) - eqt
    return (sunrise_utc / 60.0 - 7.0, sunset_utc / 60.0 - 7.0)


# ------------------------------------------------------------------------------------------------- helpers
def half_up(x, nd=0):
    q = 10 ** nd
    return math.floor(x * q + 0.5) / q


def hm(x):
    """decimal hours to HH:MM, rounding to the minute"""
    m = int(round(x * 60))
    return "%02d:%02d" % (m // 60, m % 60)


def parse_hm(s):
    h, m = s.split(":")[:2]
    return int(h) + int(m) / 60.0


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def rng_for(*keys):
    """one independent stream per purpose, so adding a draw in one place never moves another"""
    s = SEED
    for k in keys:
        for ch in str(k):
            s = (s * 131 + ord(ch)) % (2 ** 32)
    return np.random.default_rng(s)
