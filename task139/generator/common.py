"""task139 constants and helpers shared by every generator module.

Copperline Vehicle Protection (fictional, Fort Worth, Texas) has sold Copperline Drive Plus vehicle service contracts
through franchised and independent dealers in Texas and Oklahoma since 2019 and administers its own claims; Tarrant
Mutual Casualty's contractual liability policy insures its obligations. Drive Plus covers a used car's powertrain and
major systems for 60 months or 75,000 miles from the sale date and odometer, whichever comes first, with a 100 dollar
deductible a repair visit. Since April 2026 Copperline has sold Drive Plus to Fareline rideshare drivers at the class
price with a 20 per cent commercial-use loading; the agreement renews on 1 January 2027 and Copperline elects by
1 December 2026 to renew at current rates, to renew with the rate manual's maximum high-use surcharge of 40 per cent,
or to let the channel lapse. The records run to 30 September 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

SEED = 1390327
WORLD_SALT = 1                   # the keyed draws the built world was chosen on

# the calendar
RETAIL_START = dt.date(2019, 1, 2)
MIGRATION = dt.date(2024, 3, 4)  # first day on the new administration system (contract numbers re-keyed)
RS_START = dt.date(2026, 4, 1)   # the Fareline channel's first sale
VALUATION = dt.date(2026, 9, 30)
REQUEST = dt.date(2026, 10, 19)

# the cover
TERM_MONTHS = 60
TERM_DAYS = 1826
LIMIT = 75000
DEDUCTIBLE = 100.0
LOADING = 0.20
SURCHARGE = 0.40
STANDARD = 70.0                  # per cent, the channel review standard
FEE = 50.0                       # the cancellation fee
FREE_LOOK = 30                   # days

CLASSES = ("A", "B", "C")
CLASS_PRICE = {"A": 1180.0, "B": 1390.0, "C": 1645.0}      # the rate manual's base price, odometer at sale under 50,000
ODO_BANDS = ((0, 50000, 1.00), (50000, 100000, 3.08), (100000, 125001, 4.45))   # the odometer-at-sale relativities

# the world's claims process (per mile at the odometer)
P = dict(a=0.012, hk=0.5, k=2.0, knee=70000.0, sk=0.6, sev=350.0, tcomp=0.0, ret_rate=12500.0, rs_rate=44000.0,
         n_ret=14000, n_rs=6000, o_ret=(15000, 55000), ret_hi_share=0.2, ret_hi=(60000, 115000), o_rs=(50000, 100000),
         sev_sd=0.7, cancel_rate=0.09, recontract=0.25, financed=0.55)

# file names (the pack)
REGISTER = "drive_plus_contract_register.csv"
CROSSWALK = "contract_number_crosswalk_2024.csv"
CLAIMS = "claim_lines_2019-01_to_2026-09.csv"
READINGS = "odometer_readings_2019-01_to_2026-09.csv"
CANCELS = "cancellation_requests_2025-2026.csv"
BORDEREAUX = "dealer_remittance_bordereaux_2025.xlsx"
RETURNS = "ach_returns_report_2025-2026.csv"
FACILITIES = "repair_facility_directory.csv"
DEALERS = "dealer_directory.csv"
RATE_MANUAL = "drive_plus_rate_manual_2026.pdf"
TERMS = "drive_plus_contract_terms.pdf"
AGREEMENT = "fareline_channel_agreement_summary.pdf"
CLIP = "tarrant_mutual_clip_summary.pdf"

# goldens
DECK = "fareline_channel_renewal_2027.pptx"
BOOK = "drive_plus_channel_review_2027.xlsx"

BANKS = ("Brazos Federal Credit Union", "Trinity Valley Bank", "Red River Auto Finance", "Lone Star Lending Group",
         "Cross Timbers Credit Union", "Panhandle Motor Credit")


def rng(*keys):
    h = hashlib.sha256(("%d|%d|" % (SEED, WORLD_SALT) + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def haz(o):
    """expected claims per mile at odometer o"""
    return P['a'] / 1000.0 * (1 + P['hk'] * (np.maximum(o - P['knee'], 0) / 20000.0) ** P['k'])


def sev(o):
    """expected payment per claim (net of the deductible) at odometer o"""
    return P['sev'] * (1 + P['sk'] * np.maximum(o - P['knee'], 0) / 20000.0)


def base_price(cls, o0):
    rel = next(f for lo, hi, f in ODO_BANDS if lo <= o0 < hi)
    return round(CLASS_PRICE[cls] * rel, 0)


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    for r in rows:
        w.writerow([("" if r.get(c) is None else r.get(c)) for c in cols])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def add_months(d, m):
    y, mo = d.year + (d.month - 1 + m) // 12, (d.month - 1 + m) % 12 + 1
    last = (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, mo, min(d.day, last))


def quarter(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def election(lr_current):
    if lr_current <= STANDARD:
        return "renew at current rates"
    if lr_current / (1 + SURCHARGE) <= STANDARD:
        return "renew with the maximum high-use surcharge"
    return "lapse"
