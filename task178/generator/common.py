"""task178 shared constants: the pack's file names, the in-fiction calendar and clocks, the random streams and the
writers that make every file reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

BANK = "Banco Central de Tamarquia"
BANK_SHORT = "BCT"
DESK_BANK = "Banco Cordillera"
COUNTRY = "Republic of Tamarquia"
CCY = "TQP"                     # the tamarquian peso
COMPANY = DESK_BANK

# ------------------------------------------------------------------------------------------------ the pack's files
F_OPS = "bct_spot_operations_2024-2026.csv"
F_FLOWS = "dealer_customer_flows_hourly_2024-2026.csv"
F_MID = "platform_hourly_mid_2024-2026.csv"
F_DEALERS = "bct_reporting_dealers.csv"
F_CAL = "platform_trading_calendar_2024-2026.csv"
F_ANNOUNCE = "bct_press_release_2026-10-01_spot_operations.pdf"
F_NOTE = "bct_hourly_data_release_note.pdf"
F_POLICY = "cordillera_fx_options_pricing_policy_2027.pdf"
F_CONF = "platform_confirmations_cordillera_2026.csv"
F_FWD = "cordillera_fx_forward_deals_2025-2026.xlsx"
F_CLIENTS = "cordillera_corporate_client_register.csv"
F_TRM = "bct_trm_daily_2024-2026.csv"
F_STATS = "bct_monthly_fx_market_statistics_2024-2026.xlsx"
ALL_FILES = (F_OPS, F_FLOWS, F_MID, F_DEALERS, F_CAL, F_ANNOUNCE, F_NOTE, F_POLICY, F_CONF, F_FWD, F_CLIENTS, F_TRM,
             F_STATS)
DISTRACTORS = (F_TRM, F_STATS)

G_BOOK = "usd_options_vol_2027.xlsx"
G_CHART = "free_float_vol_2027.png"

# ------------------------------------------------------------------------------------------------ calendar and clocks
FIRST_DAY = dt.date(2024, 1, 2)
LAST_DAY = dt.date(2026, 12, 29)          # the last session in the release
RELEASE = dt.date(2026, 12, 30)           # the Bank's release of the hourly record
OPS_END = dt.date(2026, 12, 31)           # the last day of spot operations (announced 1 October 2026)
ANNOUNCED = dt.date(2026, 10, 1)
LAUNCH = dt.date(2027, 1, 4)
AS_OF = dt.date(2026, 12, 30)
UTC_OFFSET = -5                            # Tamarquia keeps UTC-5 all year
OPEN_H, CLOSE_H = 8, 16                    # the platform's session, local time
HOURS = tuple(range(OPEN_H, CLOSE_H))      # each trading hour by its starting hour, 08 to 15
ANN = 252                                  # the pricing policy's annualisation

MERGER_DATE = dt.date(2025, 7, 1)          # Financiera Tres Valles merged into Banco del Salitral
CONF_YEAR = 2026
GRID = tuple(range(8, 14))                 # the settings the prompt asks to mark, whole per cent
QUARTERS_2027 = ((1, dt.date(2027, 1, 1), dt.date(2027, 3, 31)), (2, dt.date(2027, 4, 1), dt.date(2027, 6, 30)),
                 (3, dt.date(2027, 7, 1), dt.date(2027, 9, 30)), (4, dt.date(2027, 10, 1), dt.date(2027, 12, 31)))
SIZE_BANDS = (("under 1m", 0, 1000), ("1m to 3m", 1000, 3000), ("3m to 10m", 3000, 10000), ("10m and over", 10000, 10 ** 9))


def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def _next_monday(d):
    return d + dt.timedelta(days=(7 - d.weekday()) % 7)


def _nth(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def _last(y, m, wd):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def national_holidays(y):
    e = _easter(y)
    return {dt.date(y, 1, 1): "Año Nuevo", _next_monday(dt.date(y, 1, 6)): "Reyes (trasladado)",
            e - dt.timedelta(days=3): "Jueves Santo", e - dt.timedelta(days=2): "Viernes Santo",
            dt.date(y, 5, 1): "Día del Trabajo", dt.date(y, 6, 14): "Día de la Independencia",
            _next_monday(dt.date(y, 8, 15)): "Asunción (trasladado)", _next_monday(dt.date(y, 11, 1)): "Todos los Santos (trasladado)",
            dt.date(y, 12, 8): "Inmaculada Concepción", dt.date(y, 12, 25): "Navidad"}


def us_holidays(y):
    def obs(d):
        return d - dt.timedelta(days=1) if d.weekday() == 5 else (d + dt.timedelta(days=1) if d.weekday() == 6 else d)
    return {obs(dt.date(y, 1, 1)): "US New Year's Day", _nth(y, 1, 0, 3): "US Martin Luther King Jr. Day",
            _nth(y, 2, 0, 3): "US Presidents Day", _last(y, 5, 0): "US Memorial Day",
            obs(dt.date(y, 6, 19)): "US Juneteenth", obs(dt.date(y, 7, 4)): "US Independence Day",
            _nth(y, 9, 0, 1): "US Labor Day", _nth(y, 10, 0, 2): "US Columbus Day",
            obs(dt.date(y, 11, 11)): "US Veterans Day", _nth(y, 11, 3, 4): "US Thanksgiving",
            obs(dt.date(y, 12, 25)): "US Christmas Day"}


def closed_days():
    out = {}
    for y in (2024, 2025, 2026):
        for d, n in us_holidays(y).items():
            out.setdefault(d, []).append(n)
        for d, n in national_holidays(y).items():
            out.setdefault(d, []).append(n)
    return out


def trading_days():
    shut = closed_days()
    d, out = FIRST_DAY, []
    while d <= LAST_DAY:
        if d.weekday() < 5 and d not in shut:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def local_to_utc(t):
    return t - dt.timedelta(hours=UTC_OFFSET)


def utc_to_local(t):
    return t + dt.timedelta(hours=UTC_OFFSET)


def quarter(d):
    return (d.month - 1) // 3 + 1


# ------------------------------------------------------------------------------------------------ randomness
SALT = "d"


def stream(name):
    """one independent generator per named purpose, so editing one file's draws never moves another's"""
    seed = int.from_bytes(hashlib.sha256(("task178-v3/%s/" % SALT + name).encode()).digest()[:8], "little")
    return np.random.default_rng(seed)


# ------------------------------------------------------------------------------------------------ writers
def write_csv(path, head, rows, crlf=True, preamble=None):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    if preamble:
        for line in preamble:
            buf.write(line + ("\r\n" if crlf else "\n"))
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def edge(v, unit):
    """the distance from v to the nearest edge of its printed cell at the given unit"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def ceil_edge(v):
    """for a value rounded up to the next whole number: the distance to the nearer integer"""
    import math
    return min(v - math.floor(v), math.ceil(v) - v) if v != int(v) else 0.0
