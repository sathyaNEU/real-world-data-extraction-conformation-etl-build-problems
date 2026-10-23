"""task177 shared constants and helpers: the cooperative, the pack's file names, the in-fiction calendar, the random
streams, the month arithmetic, the writers that make the files reproduce byte for byte and the rounding the prompt
asks for."""
from __future__ import annotations

import calendar
import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

ORG = "Cooperativa Servidores de Valdemora"
SHORT = "Coopservir"
COUNTRY = "Republica de Valdemora"
CUR = "VMP"

# ------------------------------------------------------------------------------------------------ the pack's files
F_LOANS = "payroll_loans_public_2017_2026.csv"
F_XWALK = "legacy_core_crosswalk_2021.csv"
F_RETURNS = "treasury_deduction_returns_2017_2026.csv"
F_DEFAULTS = "default_register_2017_2026.csv"
F_REGISTERS = "employer_payroll_registers_2025_2026.csv"
F_AGREE = "deduction_agreements_register.xlsx"
F_LAUNCH = "libranza_empresarial_disbursement_file_2027-02-01.csv"
F_SCHED = "savings_contribution_schedules_2025_2026.csv"
F_STMT = "collection_account_statement_2025_2026.csv"
F_RECEIPTS = "defaulted_loan_receipts_2023_2026.csv"
F_SAVINGS = "member_savings_ledger_2023_2026.csv"
F_RULES = "libranza_empresarial_product_rules_2026.pdf"
F_DICT = "data_dictionary.xlsx"
F_SUPER = "supervisor_annual_return_2025.pdf"
F_LABOUR = "labour_market_bulletin_2026q3.csv"
ALL_FILES = (F_LOANS, F_XWALK, F_RETURNS, F_DEFAULTS, F_REGISTERS, F_AGREE, F_LAUNCH, F_SCHED, F_STMT, F_RECEIPTS,
             F_SAVINGS, F_RULES, F_DICT, F_SUPER, F_LABOUR)
DISTRACTORS = (F_SUPER, F_LABOUR)

# ------------------------------------------------------------------------------------------- the in-fiction calendar
HIST_FROM = (2017, 1)            # first disbursement month in the public book extract
DATA_END = (2026, 12)            # the last month every extract covers
CORE_MOVE = (2021, 7)            # the new core's first month; legacy loans migrated under new numbers
RET_LAYOUT = (2023, 4)           # the treasury's new return layout from the April 2023 payroll
PORTAL_UPGRADE = (2026, 7)       # the intake portal stores employee ids without the document prefix from here
PULL = dt.date(2027, 1, 22)      # the pull for the launch file and every extract
DISBURSE = dt.date(2027, 2, 1)   # every launch loan is disbursed on this day
HORIZON = dt.date(2028, 1, 31)   # the forecast window ends at this month-end
N_LAUNCH = 2400
ROUND_TOTAL = 50            # the prompt: the total to the nearest 50 loans
ROUND_SHARE = 5             # each sector share to the nearest 5 per cent
ROUND_AMOUNT = 1000         # every amount to the nearest VMP 1,000

MONTH_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}

AGENCY_TYPES = ("national", "territorial", "health", "education")
SECTORS = ("contact centres", "retail chains", "security services", "logistics and courier", "food processing",
           "private clinics")


def mi(y, m):
    """month index"""
    return y * 12 + (m - 1)


def ym(i):
    return i // 12, i % 12 + 1


def month_end(i):
    y, m = ym(i)
    return dt.date(y, m, calendar.monthrange(y, m)[1])


def month_start(i):
    y, m = ym(i)
    return dt.date(y, m, 1)


def stream(name):
    """an independent, reproducible random stream for one part of the world"""
    h = int.from_bytes(hashlib.sha256(("task177v3/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


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


def nearest(v, unit):
    """v printed to the nearest unit, halves away from zero"""
    return int(unit * math.floor(v / unit + 0.5))


def edge(v, unit):
    """distance from v to the nearest edge of the printed cell it falls in"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def annuity(principal, rate, n):
    return principal * rate / (1 - (1 + rate) ** -n)


def balance_after(principal, rate, n, k):
    """scheduled balance after k instalments of an n-month annuity"""
    if k <= 0:
        return principal
    if k >= n:
        return 0.0
    a = annuity(principal, rate, n)
    return principal * (1 + rate) ** k - a * ((1 + rate) ** k - 1) / rate


def nit_check(base):
    """the check digit of a Valdemoran tax number (the modulus-11 weights the tax office publishes)"""
    w = (3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71)
    s = sum(int(d) * w[i] for i, d in enumerate(reversed(base)))
    r = s % 11
    return r if r < 2 else 11 - r


def fmt_nit(base):
    b = str(base)
    return "%s.%s.%s-%d" % (b[:3], b[3:6], b[6:], nit_check(b))


def money(v):
    return int(math.floor(v + 0.5))


HOLIDAYS = {(1, 1), (5, 1), (7, 20), (8, 7), (12, 8), (12, 25)}


def business_day(d, back=False):
    """the next (or previous) business day on or after (before) d: weekends and the fixed national holidays"""
    step = dt.timedelta(days=-1 if back else 1)
    while d.weekday() >= 5 or (d.month, d.day) in HOLIDAYS:
        d = d + step
    return d


def dotted(x):
    """a national id or number with thousands dots, as Valdemoran forms print it"""
    return "{:,}".format(int(x)).replace(",", ".")
