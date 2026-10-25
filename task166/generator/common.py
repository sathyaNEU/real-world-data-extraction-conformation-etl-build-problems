"""task166 constants and helpers shared by every generator module.

Hollowell Community Credit Union, a state-chartered credit union in West Michigan (about $4.1 billion of assets),
lends from four regional lending centers: Grand Rapids, the Lakeshore, Kalamazoo and Battle Creek, and Muskegon and
the north. Its management lending committee meets on Wednesday 9 December 2026 to choose the region where a
payoff-retention pilot opens on Monday 4 January 2027. Every position is as of the close on Monday 30 November 2026;
every file was pulled on Thursday 3 December 2026.

The seed was fixed by rule before any data was generated: the task number, then the pilot's opening month and day."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os

import numpy as np

SEED = int(os.environ.get("T166_SEED", 1660104))

CU = "Hollowell Community Credit Union"
CU_SHORT = "Hollowell"
CU_BUREAU = "HOLLOWELL COMM CU"          # the credit union's subscriber name on a credit report
PEOPLE = {
    "analytics": "Sherri Bautista",      # lending analytics manager: prepares the pilot's regional payoff forecast
    "clo": "Brandon Coffey",             # chief lending officer, chairs the management lending committee
    "alm": "Joel Singh",                 # ALM and finance manager: the planning cycle and the quarterly ALM report
    "servicing": "Cody Li",              # loan servicing supervisor: the payoff desk
}

# ------------------------------------------------------------------------------------------------- calendar
AS_OF = dt.date(2026, 11, 30)
PULL = dt.date(2026, 12, 3)
COMMITTEE = dt.date(2026, 12, 9)
PILOT = dt.date(2027, 1, 4)
CONVERSION = dt.date(2024, 9, 1)        # the new core opened its books on 1 September 2024


def mo(y, m):
    return y * 12 + (m - 1)


def ym(o):
    return o // 12, o % 12 + 1


def month_end(o):
    y, m = ym(o)
    nxt = dt.date(y + (m // 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def month_start(o):
    y, m = ym(o)
    return dt.date(y, m, 1)


ASOF_M = mo(2026, 11)
REC0 = mo(2019, 1)                      # the first month of the legacy extract
CONV_M = mo(2024, 9)                    # the new core's first month
FORE = [mo(2026, 12)] + [mo(2027, k) for k in range(1, 13)]   # December 2026 then the pilot year
YEAR = [mo(2027, k) for k in range(1, 13)]

REGIONS = ["Grand Rapids", "The Lakeshore", "Kalamazoo and Battle Creek", "Muskegon and the North"]
RCODE = {"Grand Rapids": "GR", "The Lakeshore": "LS", "Kalamazoo and Battle Creek": "KB", "Muskegon and the North": "MN"}
# collateral county -> regional lending center (the county of the property, as the lending policy files it)
COUNTIES = {
    "GR": [("Kent", 0.78), ("Ionia", 0.07), ("Barry", 0.08), ("Montcalm", 0.07)],
    "LS": [("Ottawa", 0.74), ("Allegan", 0.26)],
    "KB": [("Kalamazoo", 0.58), ("Calhoun", 0.30), ("Van Buren", 0.12)],
    "MN": [("Muskegon", 0.55), ("Newaygo", 0.16), ("Oceana", 0.15), ("Mason", 0.14)],
}
CITIES = {
    "Kent": ["Grand Rapids", "Wyoming", "Kentwood", "Walker", "Grandville", "Rockford", "Cedar Springs", "Lowell",
             "Byron Center", "Comstock Park", "Ada", "Caledonia", "Sparta"],
    "Ionia": ["Ionia", "Belding", "Portland", "Saranac"],
    "Barry": ["Hastings", "Middleville", "Nashville", "Delton"],
    "Montcalm": ["Greenville", "Stanton", "Howard City", "Carson City"],
    "Ottawa": ["Holland", "Grand Haven", "Zeeland", "Hudsonville", "Allendale", "Jenison", "Spring Lake", "Coopersville"],
    "Allegan": ["Allegan", "Otsego", "Plainwell", "Wayland", "Saugatuck", "Fennville", "Hamilton"],
    "Kalamazoo": ["Kalamazoo", "Portage", "Vicksburg", "Schoolcraft", "Richland", "Galesburg", "Oshtemo"],
    "Calhoun": ["Battle Creek", "Marshall", "Albion", "Springfield", "Homer"],
    "Van Buren": ["South Haven", "Paw Paw", "Lawton", "Bangor", "Hartford"],
    "Muskegon": ["Muskegon", "Norton Shores", "Muskegon Heights", "North Muskegon", "Whitehall", "Montague",
                 "Fruitport", "Ravenna"],
    "Newaygo": ["Fremont", "Newaygo", "White Cloud", "Grant"],
    "Oceana": ["Hart", "Shelby", "Pentwater", "New Era"],
    "Mason": ["Ludington", "Scottville", "Custer"],
}


# ------------------------------------------------------------------------------------------------- writers
def write_csv(path, cols, rows, crlf=False, quoting=csv.QUOTE_MINIMAL, delimiter=","):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n", quoting=quoting, delimiter=delimiter)
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


def rng(*stream):
    """One RNG per component and key, so a change in one never moves another's draws."""
    return np.random.default_rng([SEED] + [int(s) for s in stream])


def skey(text):
    """a stable integer key for a string"""
    h = 0
    for ch in text:
        h = (h * 131 + ord(ch)) % 2147483647
    return h


def business_day(d, back=False):
    while d.weekday() >= 5 or d in HOLIDAYS:
        d = d - dt.timedelta(days=1) if back else d + dt.timedelta(days=1)
    return d


def _holidays():
    out = set()
    for y in range(2008, 2028):
        out.add(dt.date(y, 1, 1))
        out.add(dt.date(y, 7, 4))
        out.add(dt.date(y, 12, 25))
        # Memorial Day (last Monday of May), Labor Day (first Monday of September), Thanksgiving (fourth Thursday)
        d = dt.date(y, 5, 31)
        while d.weekday() != 0:
            d -= dt.timedelta(days=1)
        out.add(d)
        d = dt.date(y, 9, 1)
        while d.weekday() != 0:
            d += dt.timedelta(days=1)
        out.add(d)
        d = dt.date(y, 11, 1)
        k = 0
        while True:
            if d.weekday() == 3:
                k += 1
                if k == 4:
                    break
            d += dt.timedelta(days=1)
        out.add(d)
    return out


HOLIDAYS = _holidays()
