"""task166 constants and helpers shared by every generator module.

Carrick Valley Bancorp, Pittsburgh (bank subsidiary Carrick Valley Bank), about $38 billion of assets, footprint
western Pennsylvania, Ohio and West Virginia. ALCO approved one $1.2 billion four-year pay-fixed swap overlay at its
November 2026 meeting; the hedge designation memo is due on Monday 14 December 2026, the swap trades on Tuesday
15 December 2026 and is effective on Monday 4 January 2027. Every position is as of the close on Monday 30 November
2026; every file was pulled for the memo on Thursday 3 December 2026.

The seed was fixed by rule before any data was generated: the task number, then the memo's month and day
(14 December)."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np

SEED = 1661214

BANK = "Carrick Valley Bank"
HOLDCO = "Carrick Valley Bancorp"
PEOPLE = {
    "bsm": "Guy Morrison",        # head of balance sheet management: the requester (in no file the prompt names)
    "alm": "Sheri Roberts",       # ALM manager: the quarterly ALM report, the planning rate file
    "analyst": "Cody Li",         # ALM analyst: the position extracts and their notes
    "credit": "Jeff Guzman",      # commercial real estate credit administration: the maturity log, the extension terms
    "treasurer": "Joshua Boyd",   # treasurer, ALCO secretary: the hedge policy's owner
}

# ------------------------------------------------------------------------------------------------- calendar
AS_OF = dt.date(2026, 11, 30)      # Monday: positions as of the close
PULL = dt.date(2026, 12, 3)        # Thursday: every extract pulled for the memo
MEMO_DUE = dt.date(2026, 12, 14)   # Monday
TRADE = dt.date(2026, 12, 15)      # Tuesday
EFFECTIVE = dt.date(2027, 1, 4)    # Monday
MATURITY = dt.date(2031, 1, 6)     # 4 January 2031 is a Saturday: modified following, Monday 6 January
NOTIONAL = 1_200_000_000

# months are integer ordinals: year * 12 + (month - 1); month-end m holds the cash flows paid in month m
def mo(y, m):
    return y * 12 + (m - 1)


def ym(o):
    return o // 12, o % 12 + 1


def month_end(o):
    y, m = ym(o)
    nxt = dt.date(y + (m // 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


ASOF_M = mo(2026, 11)
MEASURE_MONTHS = [mo(2027, k) for k in range(1, 13)]     # the twelve month-ends of the swap's first year
PROJ_START = ASOF_M + 1                                   # December 2026: first projected month
HORIZON = 360                                             # months projected from the as-of


# ------------------------------------------------------------------------------------------------- the planning cycle
# ALCO's September 2026 planning cycle (the 2027 plan): the base case. Zero rates are continuously compounded,
# by tenor in years; linear interpolation in time between tenors, flat beyond 30 years.
CURVE_TENORS = [1 / 12, 0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
CURVE_ZEROS = [3.86, 3.81, 3.72, 3.57, 3.41, 3.39, 3.44, 3.52, 3.67, 3.87, 4.06, 4.16, 4.13]   # per cent
PLAN_MORTGAGE = 6.25      # 30-year portfolio jumbo rate, every month from December 2026
PLAN_MORTGAGE_15 = 5.55   # 15-year conforming rate (the agency pools' borrowers)
PLAN_CRE = 6.95           # five-year fixed CRE rate, every month from December 2026
SHOCK = 0.02


def zero(t):
    t = np.asarray(t, float)
    return np.interp(t, CURVE_TENORS, CURVE_ZEROS) / 100.0


def discount(t, shift=0.0):
    t = np.asarray(t, float)
    return np.exp(-(zero(t) + shift) * t)


# ------------------------------------------------------------------------------------------------- writers
def write_csv(path, cols, rows, crlf=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def write_json(path, obj, indent=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, sort_keys=False)
        f.write("\n")


def money(x, nd=2):
    return ("%." + str(nd) + "f") % x


def rng(stream):
    """One RNG per component, so a change in one never moves another's draws."""
    return np.random.default_rng([SEED, stream])
