"""task149 constants and helpers shared by every generator module.

Ostrander Logistics, a privately held third-party logistics operator based in Columbus, Ohio, runs sixty dedicated
contract distribution centres (DCs) for grocery and consumer-goods retailers in eleven states. Its fiscal year is 52 or
53 weeks ending on the last Saturday of December, in 4-4-5 periods. For fiscal 2027 (27 December 2026 to 25 December
2027) Lindqvist Ergonomics Group runs an ergonomics programme at the twenty DCs with the largest planned growth, priced
per forecast OSHA recordable case at those DCs in fiscal 2027 on the FY2027 operating plan. The EHS, workforce-management
and WMS exports were pulled on Monday 2 November 2026 through fiscal 2026 week 44 (the week ending 31 October 2026)."""
from __future__ import annotations

import datetime as dt
import hashlib
import os

import numpy as np

SEED = 1492027
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

ORG = "Ostrander Logistics"
ORG_LEGAL = "Ostrander Logistics, LLC"
VENDOR = "Lindqvist Ergonomics Group"
VENDOR_SHORT = "Lindqvist"
HQ = "Columbus, Ohio"

PEOPLE = {
    "ehs_dir": "Sherri Newton",        # director of environmental health and safety (the requester; not in the prompt)
    "analytics": "Jesse Delgado",      # safety analytics manager, the EHS exports
    "ie": "Kurt Gilbert",              # industrial engineering manager, the engineered labour standards
    "planning": "Nichole Sandoval",    # operations planning manager (FP&A), the FY2027 operating plan
    "vendor": "Tracy Curtis",          # Lindqvist Ergonomics Group's account director
}

PULL_DATE = dt.date(2026, 11, 2)                 # exports pulled Monday 2 November 2026
PULL_STAMP = dt.datetime(2026, 11, 2, 14, 6)     # local time the EHS team built the folder
PLAN_APPROVED = dt.date(2026, 10, 23)            # FY2027 operating plan v3, approved by the executive team
SIGNING = dt.date(2026, 11, 16)                  # the Lindqvist agreement is signed on the forecast
MIGRATION = dt.date(2024, 7, 1)                  # EHS platform go-live; the legacy system's last day is 30 June 2024

# ---------------------------------------------------------------------------------------------------- fiscal calendar
FY_START = {
    2021: dt.date(2020, 12, 27), 2022: dt.date(2021, 12, 26), 2023: dt.date(2023, 1, 1), 2024: dt.date(2023, 12, 31),
    2025: dt.date(2024, 12, 29), 2026: dt.date(2025, 12, 28), 2027: dt.date(2026, 12, 27), 2028: dt.date(2027, 12, 26),
}
HIST_FY = [2021, 2022, 2023, 2024, 2025, 2026]
LAST_FY, LAST_WEEK = 2026, 44                    # the extract runs through fiscal 2026 week 44
PLAN_FY = 2027


def fy_weeks(fy):
    return (FY_START[fy + 1] - FY_START[fy]).days // 7


PERIOD_END = [4, 8, 13, 17, 21, 26, 30, 34, 39, 43, 47, 52]   # 4-4-5; a 53rd week joins period 12


def period_of(fy, wk):
    for i, e in enumerate(PERIOD_END):
        if wk <= e:
            return i + 1
    return 12


def period_weeks(fy, p):
    lo = 1 if p == 1 else PERIOD_END[p - 2] + 1
    hi = PERIOD_END[p - 1] if p < 12 else fy_weeks(fy)
    return list(range(lo, hi + 1))


def week_start(fy, wk):
    return FY_START[fy] + dt.timedelta(days=7 * (wk - 1))


def hist_weeks():
    """Every fiscal week in the history, (fy, wk, start date), FY2021 week 1 to FY2026 week 44."""
    out = []
    for fy in HIST_FY:
        n = fy_weeks(fy) if fy < LAST_FY else LAST_WEEK
        for wk in range(1, n + 1):
            out.append((fy, wk, week_start(fy, wk)))
    return out


def fiscal_of(d):
    """(fy, week, period) of a calendar date."""
    for fy in sorted(FY_START):
        if FY_START[fy] <= d < FY_START[fy + 1] if fy + 1 in FY_START else False:
            wk = (d - FY_START[fy]).days // 7 + 1
            return fy, wk, period_of(fy, wk)
    raise ValueError(d)


# ---------------------------------------------------------------------------------------------------- operations
CATS = ["AMB", "CHL", "FRZ", "HVB"]                      # WMS product categories (codes from FY2023 period 7)
CAT_NAMES = {"AMB": "Ambient grocery", "CHL": "Chilled (dairy, deli, produce)", "FRZ": "Frozen",
             "HVB": "Heavy and bulky (beverages, pet food, bulk paper, cleaning)"}
OLD_CATS = {"AMB": "DRYG", "CHL": "PERI", "FRZ": "FROZ", "HVB": "BULK"}   # the item hierarchy before the FY2023 recode
CAT_RECODE = (2023, 27)                                  # fiscal 2023 week 27 (period 7) the WMS hierarchy changed
FUNCS = ["RCV", "PUT", "SEL", "LOD"]                     # direct labour functions on engineered standards
FUNC_NAMES = {"RCV": "Receiving", "PUT": "Putaway and replenishment", "SEL": "Order selection", "LOD": "Loading"}
INDIRECT = ["INV", "MNT", "SAN", "TRN"]                  # hourly indirect departments
IND_NAMES = {"INV": "Inventory control", "MNT": "Maintenance", "SAN": "Sanitation", "TRN": "Training and safety"}
# engineered minutes per case by function and category (the 2019 library; a DC's layout factor scales PUT and SEL)
STD_BASE = {
    "RCV": {"AMB": 0.214, "CHL": 0.236, "FRZ": 0.281, "HVB": 0.352},
    "PUT": {"AMB": 0.296, "CHL": 0.331, "FRZ": 0.402, "HVB": 0.517},
    "SEL": {"AMB": 0.618, "CHL": 0.702, "FRZ": 0.853, "HVB": 1.247},
    "LOD": {"AMB": 0.177, "CHL": 0.198, "FRZ": 0.224, "HVB": 0.301},
}
FUNC_SHARE_NOISE = 0.03

# the injury process (the world's truth; nothing here ships)
GAMMA = 3.0          # the rate per hour rises as pace against standard to this power, within each DC
PACE_REF = 0.925     # the network's typical pace against standard
CONFOUND = -14.0     # DCs that run faster on average are better laid out and safer: base rate falls with long-run pace
SURGE_PACE = 0.30   # a busy week is worked faster: the share of the volume swing the crews absorb in pace
INDIRECT_RATE = 0.45  # indirect hours carry this share of a direct hour's recordable rate at the reference pace
TRIR_REF = 5.15       # recordables per 200,000 hours at the reference pace, network average
OVERDISP = 30.0      # gamma shape of the week-level rate noise


def rng(*keys):
    """An independent stream per purpose, so one change does not re-roll another stream."""
    h = hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def money(x):
    return "{:,.2f}".format(x)
