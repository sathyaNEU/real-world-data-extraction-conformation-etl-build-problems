"""task177 shared constants and helpers: the file names, the in-fiction calendar, the UK clock, the prices, the random
streams and the writers that make the files reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

ORG = "Daily Lantern Media"
TITLE = "The Daily Lantern"

# ------------------------------------------------------------------------------------------------ the pack's files
F_ASSIGN = "retention_campaign_2026-01_assignment.csv"
F_PROFILE = "subscriber_profile_2026-01-31.csv"
F_LIST = "at_risk_list_2027-01-26.csv"
F_LBS = "legacy_billing_invoices.csv"
F_SPINV = "subscriptions_platform_invoices.csv"
F_XWALK = "subscription_id_crosswalk.csv"
F_EVENTS = "subscription_events.csv"
F_OFFERS = "offers_engine_acceptances_2026.csv"
F_EMAIL = "email_campaign_log_2026-01.csv"
F_NOTE = "billing_move_note_2026.pdf"
F_PLAN = "retention_offer_plan_2027.docx"
F_DICT = "data_dictionary.xlsx"
F_SURVEY = "reader_survey_2026_q4.csv"
F_VALID = "retention_model_validation_2026-12.pdf"
ALL_FILES = (F_ASSIGN, F_PROFILE, F_LIST, F_LBS, F_SPINV, F_XWALK, F_EVENTS, F_OFFERS, F_EMAIL, F_NOTE,
             F_PLAN, F_DICT, F_SURVEY, F_VALID)
DISTRACTORS = (F_SURVEY, F_VALID)

# ------------------------------------------------------------------------------------------- the in-fiction calendar
LY_LIST = dt.date(2026, 1, 31)          # last year's list, cut and sent on this Saturday
LY_SEND = dt.datetime(2026, 1, 31, 9, 30)
LY_HORIZON = dt.date(2026, 3, 31)
LBS_FROM = dt.date(2025, 12, 1)         # the legacy invoices in the pull start with December 2025's bills
MOVE = dt.date(2026, 10, 1)             # the subscriptions platform's first bill run (00:05 UK time)
LBS_LAST = dt.date(2026, 10, 1)         # the legacy system's last run (02:00, day-1 subscriptions it still held)
CREDIT_DAY = dt.date(2026, 10, 14)      # the platform's credit notes for the bills both systems raised for October
PULL = dt.datetime(2027, 1, 25, 18, 40) # the extract, UK time
TY_LIST = dt.date(2027, 1, 26)
TY_SEND = dt.datetime(2027, 1, 26, 9, 30)
TY_HORIZON = dt.date(2027, 3, 31)
ASK_A_MONTHS = ((2026, 2), (2026, 3), (2026, 4))
ASK_B_MONTHS = ((2026, 10), (2026, 11), (2026, 12), (2027, 1))
MONTH_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}

# British Summer Time: UTC+1 from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October
BST = {2025: (dt.datetime(2025, 3, 30, 1), dt.datetime(2025, 10, 26, 1)),
       2026: (dt.datetime(2026, 3, 29, 1), dt.datetime(2026, 10, 25, 1)),
       2027: (dt.datetime(2027, 3, 28, 1), dt.datetime(2027, 10, 31, 1))}


def to_utc(local):
    """UK local wall time to UTC (the autumn's repeated hour read as its first, BST, pass)"""
    a, b = BST[local.year]
    a_loc, b_loc = a, b + dt.timedelta(hours=1)
    return local - dt.timedelta(hours=1) if a_loc + dt.timedelta(hours=1) <= local < b_loc else local


def to_local(utc):
    a, b = BST[utc.year]
    return utc + dt.timedelta(hours=1) if a <= utc < b else utc


# --------------------------------------------------------------------------------------------------------- the plans
PLANS = ("Digital", "Digital Plus", "Family")
PLAN_CODE = {"Digital": "DIG-M", "Digital Plus": "DGP-M", "Family": "FAM-M"}
PRICE = {"Digital": 9.99, "Digital Plus": 13.99, "Family": 17.99}       # monthly, zero-rated for VAT
ADDON = "Puzzles"
ADDON_CODE = "PUZ-M"
ADDON_PRICE = 3.49
OFFER_SHARE = 0.5                        # half price on the next two monthly bills
OFFER_CODE_WEB = "STAY50"                # the code the offers engine applied to web and email acceptances
OFFER_CODE_APP = "LNT-APP-JAN26"         # the code the app team set up for in-app acceptances of the same offer
DESK_CODE = "STAY50"                     # the save desk's discretionary half price uses the same billing code
LOYAL_CODE = "LOYAL-CR"                  # goodwill credits on a bill (service apologies)
RATE_CODE = {"Digital": "DIG-MA", "Digital Plus": "DGP-MA", "Family": "FAM-MA"}   # the app's two-bill half-price rates


def stream(name):
    """an independent, reproducible random stream for one part of the world"""
    h = int.from_bytes(hashlib.sha256(("task177v2/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def add_months(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return y, m


def month_day(y, m, dom):
    """the bill day of a subscription anniversary-billed on day dom, in month (y, m): days 29 to 31 fall back to the
    month's last day"""
    import calendar
    return dt.date(y, m, min(dom, calendar.monthrange(y, m)[1]))


def next_bill_after(dom, day):
    """the first anniversary bill strictly after `day` for a subscription billed on day dom"""
    b = month_day(day.year, day.month, dom)
    if b > day:
        return b
    y, m = add_months(day, 1)
    return month_day(y, m, dom)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def edge(v, unit):
    """distance from v to the nearest edge of the printed cell it falls in"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


FORECAST_UNIT = 5                        # the prompt asks for the share to the nearest 5 per cent


def pct5(v):
    """a share printed to the nearest 5 per cent, halves away from zero"""
    return int(FORECAST_UNIT * math.floor(v * 100 / FORECAST_UNIT + 0.5))


def hundred(v):
    """an amount in pounds printed to the nearest hundred, halves away from zero"""
    return int(100 * math.floor(v / 100 + 0.5))


def money(v):
    return "%.2f" % (math.floor(v * 100 + 0.5) / 100)
