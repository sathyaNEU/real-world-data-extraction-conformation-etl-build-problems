"""Shared constants and helpers for the task166 generator (architecture 4): Marrowgate Books Ltd, an independent
London trade publisher, and its returns allowance at the 31 October 2026 year end."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os

import numpy as np

SEED = 166
COMPANY = "Marrowgate Books Ltd"
DISTRIBUTOR = "Tallowmere Book Distribution Ltd"
DAY0 = dt.date(2020, 11, 2)                 # Monday; week 0 of the simulation
YEAR_END = dt.date(2026, 10, 31)            # the financial year end the allowance is struck at
LAST_DATA = dt.date(2026, 10, 30)           # last working day with records in the pack
WEEKS = 384                                 # simulation weeks, to 2028-03
W_CUT = (YEAR_END - DAY0).days // 7         # week holding the year end (Mon 26 Oct 2026)
EXTRACT_FROM = dt.date(2021, 11, 1)         # FY2022 opens: the ledger extract's first day
ELIG_MIN_W, ELIG_MAX_W = 13, 52             # a return may quote an invoice 3 to 12 months old (in weeks)
ELIG_MIN_D, ELIG_MAX_D = 91, 365            # the same in days, as the terms of trade file it

PEOPLE = {"controller": "Hilary Singh", "salesops": "Marc Hudson", "dist_returns": "Jade Hewitt"}

CHANNELS = ["Chain", "Online", "Wholesale", "Supermarket", "Independent", "Export"]
FORMATS = ["Hardback", "Trade paperback", "Paperback"]


def date_of(week, weekday=0):
    return DAY0 + dt.timedelta(days=7 * int(week) + int(weekday))


def week_of(d):
    return (d - DAY0).days // 7


def fy_of(d):
    """Marrowgate's financial year runs 1 November to 31 October; FY2026 is Nov 2025 to Oct 2026."""
    return d.year + 1 if d.month >= 11 else d.year


def fy_quarter(d):
    """Q1 Nov-Jan, Q2 Feb-Apr, Q3 May-Jul, Q4 Aug-Oct."""
    m = d.month
    return {11: 1, 12: 1, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4}[m]


def add_months(d, months):
    y, m = d.year, d.month - 1 + int(months)
    y += m // 12
    m = m % 12 + 1
    last = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return dt.date(y, m, min(d.day, last))


def thursday_on_or_after(d):
    return d + dt.timedelta(days=(3 - d.weekday()) % 7)


WORLD = os.environ.get("T166_WORLD", "s110")   # the world drawn for the pack; other values only for sweeps


def rng(*stream):
    """One independent numpy stream per named purpose, so a change in one part of the world moves no other."""
    h = hashlib.sha256(("task166-v4|" + WORLD + "|".join(str(s) for s in stream)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def isbn13(stem12):
    """stem12: 12 digits as a string; returns the ISBN-13 with its check digit."""
    s = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(stem12))
    return stem12 + str((10 - s % 10) % 10)


def hyphenate(isbn):
    """978-1-8469-nnnn-c: prefix, group, registrant, publication, check."""
    return "%s-%s-%s-%s-%s" % (isbn[:3], isbn[3], isbn[4:8], isbn[8:12], isbn[12])


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write("\n")


def money(x):
    return float(round(float(x) + 1e-9, 2))
