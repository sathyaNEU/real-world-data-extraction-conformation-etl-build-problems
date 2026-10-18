"""task170 constants shared by every generator module.

A southern African ministry of health (the country is never named in the pack) buys antiretrovirals through its
Central Medical Stores (CMS) on six-month cycles; C7 runs from January to June 2027. The national ART programme
files a monthly projection of the adults on tenofovir/lamivudine/dolutegravir (TLD); the paediatric and adolescent
ART register (the national EPR's paediatric module, the legacy register before June 2024) holds every child's clinic
visits, weighings and regimens. Children move from paediatric regimens onto the adult TLD tablet at the first clinic
weighing that reads 30 kg or more. CMS counted its stock on 31 August 2026, pulled every file on 2 September 2026 and
files the C7 order at the quantification review of 22 September 2026.

The seed was fixed by rule before any data was generated: the task number, then the count's month and day."""
from __future__ import annotations

import datetime as dt
import os

SEED = 1700831

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

D = dt.date
COUNT = D(2026, 8, 31)          # the stock count and the register's as-of
PULL = D(2026, 9, 2)            # every file pulled
REVIEW = D(2026, 9, 22)         # the quantification review files the C7 order
WINDOW = (D(2026, 9, 1), D(2027, 6, 30))
MAX_MONTHS = 6                  # the maximum stock level, months of the last month's forecast consumption
LOT = 5000                      # the call is rounded to the nearest 5,000 bottles
C4 = (D(2025, 7, 1), D(2025, 12, 31))     # the last two closed cycles
C5 = (D(2026, 1, 1), D(2026, 6, 30))
EPR_LIVE = D(2024, 6, 1)        # the EPR's paediatric module went live; legacy rows end 30 June 2024
LEGACY_END = D(2024, 6, 30)
SHIP_FROM = D(2023, 1, 1)       # the register extract's first visit
REALIGN = D(2026, 4, 1)         # the regional boundary change

ORG = "Central Medical Stores"
MOH = "Ministry of Health"
PROG = "National ART Programme"
PEOPLE = {
    "quant_lead": "Nomalanga Magubane",    # CMS quantification lead: the SOP, the stock status report
    "paed": "Thabisile Mahlinza",          # paediatric ART programme officer: the register extract
    "me": "Sibongile Sikhosana",           # ART programme monitoring officer: the adult projection
}

# ------------------------------------------------------------------------------------------------ months
# Month index from January 2004 (the simulation's clock), and helpers.
T0 = 2004


def mi(y, m):
    return (y - T0) * 12 + (m - 1)


def ym(i):
    return T0 + i // 12, i % 12 + 1


def month_end(i):
    y, m = ym(i)
    nxt = D(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def month_of(d):
    return mi(d.year, d.month)


M_COUNT = mi(2026, 8)
M_WIN = list(range(mi(2026, 9), mi(2027, 6) + 1))
M_JUNE = mi(2027, 6)
M_SHIP = mi(2023, 1)
M_END_SIM = mi(2027, 12)

# ------------------------------------------------------------------------------------------------ geography
# Regions as the Regional Boundaries Order of 1 April 2026 draws them, each district with the region it sat in
# before.
REGIONS = ["Capital", "Central", "Northern", "Eastern", "Southern", "Western"]
DISTRICTS = [
    # code, name, region from 1 April 2026, region before, share of the country's ART patients
    ("D01", "Capital North", "Capital", "Capital", 0.072),
    ("D02", "Capital South", "Capital", "Capital", 0.081),
    ("D03", "Woodlands", "Capital", "Central", 0.046),
    ("D04", "Midlands", "Central", "Central", 0.052),
    ("D05", "Central Hills", "Central", "Central", 0.041),
    ("D06", "River Junction", "Central", "Central", 0.044),
    ("D07", "Central Plains", "Central", "Central", 0.037),
    ("D08", "Upper Plains", "Central", "Northern", 0.033),
    ("D09", "Highlands", "Northern", "Northern", 0.039),
    ("D10", "Plateau", "Northern", "Northern", 0.035),
    ("D11", "Upper River", "Northern", "Northern", 0.031),
    ("D12", "Lowlands", "Eastern", "Eastern", 0.047),
    ("D13", "Border Hills", "Eastern", "Eastern", 0.034),
    ("D14", "Lakeside", "Eastern", "Eastern", 0.043),
    ("D15", "Eastern Valley", "Eastern", "Eastern", 0.036),
    ("D16", "Escarpment", "Eastern", "Northern", 0.029),
    ("D17", "Southern Hills", "Southern", "Southern", 0.040),
    ("D18", "Southern Plains", "Southern", "Southern", 0.038),
    ("D19", "Lower River", "Southern", "Southern", 0.035),
    ("D20", "Dry Valley", "Southern", "Western", 0.030),
    ("D21", "Western Ridge", "Western", "Western", 0.039),
    ("D22", "Western Plains", "Western", "Western", 0.036),
    ("D23", "Forest", "Western", "Western", 0.033),
    ("D24", "Savanna", "Western", "Southern", 0.029),
]

# ------------------------------------------------------------------------------------------------ products
# National regimen codes (the EPR's code list) and the legacy register's free-text regimen lines.
REG_TLD = "A1-TLD"
REGIMENS = [
    # code, line, regimen, weight band, legacy text
    ("P1-AB3D10", "first", "ABC/3TC 120/60 mg dispersible + DTG 10 mg dispersible", "3 to 19.9 kg",
     "ABC/3TC 120/60 disp + DTG 10mg disp"),
    ("P1-AB3D50", "first", "ABC/3TC 600/300 mg + DTG 50 mg", "20 to 29.9 kg", "ABC/3TC 600/300 + DTG 50mg"),
    ("P2-AZ3LR", "second", "AZT/3TC 60/30 mg + LPV/r 40/10 mg pellets or 100/25 mg tablets", "3 to 29.9 kg",
     "AZT/3TC + LPV/r"),
    (REG_TLD, "first", "TDF/3TC/DTG 300/300/50 mg (TLD)", "30 kg and over", "TDF/3TC/DTG 300/300/50"),
    ("A2-TD3DRV", "second", "TDF/3TC 300/300 mg + DRV/r 800/100 mg", "30 kg and over", "TDF/3TC + DRV/r"),
]
