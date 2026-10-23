"""task170 constants shared by every generator module.

Tarnland is a fictional country and Vindeholm County a fictional county in it. The county council's hospital group,
Vindeholm County Hospitals, employs about 9,000 staff in six hospitals and runs a supplementary savings plan that
staff have had to opt into since 2012: an employee contribution of 1 to 10 per cent of basic pay, matched by the
employer at 100 per cent of the first 3 per cent and 50 per cent of the next 3. From 1 January 2027 every new hire is
enrolled automatically at 3 per cent from the first payroll and may opt out. The reward and pensions team forecasts
the FY2027 employer match on the 2027 intake for the budget the executive team approves in December 2026. Every
record is invented.

The seed was fixed by rule before any data was generated: the task number, then the pull's month and day."""
from __future__ import annotations

import datetime as dt
import os

SEED = 1701109

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")
GOLDEN = os.path.join(TASK_DIR, "golden")

D = dt.date
PULL = D(2026, 11, 9)                   # every file pulled for the forecast
HIST_START = (2019, 1)                  # the first intake auto-enrolled into the income protection cover
LAST_PAYROLL = (2026, 10)               # the last payroll in the pull
MIGRATION = (2026, 2)                   # the payroll and HR system cutover: new employee numbers from February 2026
DEDUCT_START = (2025, 11)               # the deduction export's first payroll
FY = 2027
DEFAULT_RATE = 3                        # the auto-enrolment rate, per cent of basic pay
CUTOFF_DAY = 10                         # elections received by the 10th apply to that month's payroll

ORG = "Vindeholm County Hospitals"
COUNTRY = "Tarnland"
COUNTY = "Vindeholm County"
CURRENCY = "TNK"
PLAN = "VCH Supplementary Savings Plan"
ADMIN = "Ledstrand Pension Administration"
INSURER = "Tarnmark Mutual"
PEOPLE = {
    "me": "Caroline Hagman",            # reward and pensions manager
    "fd": "Erik Palm",                  # director of finance
    "pay": "Alfred Sundberg",           # payroll services lead
}

# the six hospitals; Lidmark Rehabilitation Centre (LRC) was merged into Lidmark Hospital on 1 July 2024
HOSPITALS = [("VCS", "Vindeholm Central Hospital"), ("RDH", "Rendholm Hospital"), ("ASK", "Askvik Hospital"),
             ("OSV", "Ostervall Hospital"), ("BRB", "Brannby Hospital"), ("LDM", "Lidmark Hospital")]
H_NAME = dict(HOSPITALS)
H_CODES = [c for c, _ in HOSPITALS]
MERGED = ("LRC", "LDM", D(2024, 7, 1))

GRADES = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]
SCALE_2027 = {"G1": 24900, "G2": 27300, "G3": 30100, "G4": 33800, "G5": 38600, "G6": 44900, "G7": 52700, "G8": 63400}
SCALE_2026 = {"G1": 24150, "G2": 26480, "G3": 29190, "G4": 32780, "G5": 37440, "G6": 43550, "G7": 51120, "G8": 61500}
SCALE_2025 = {"G1": 23450, "G2": 25710, "G3": 28340, "G4": 31830, "G5": 36350, "G6": 42280, "G7": 49630, "G8": 59710}
IPC_PREMIUM = 0.004                     # the cover's premium, a share of basic pay


def match_pct(rate):
    """The employer's match, per cent of basic pay, on an employee rate in whole per cent."""
    r = float(rate)
    return min(r, 3.0) + 0.5 * min(max(r - 3.0, 0.0), 3.0)


def months(a, b):
    y, m = a
    out = []
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def mindex(ym):
    return ym[0] * 12 + ym[1] - 1


def ym_of(i):
    return (i // 12, i % 12 + 1)


def first_working_day(y, m):
    d = D(y, m, 1)
    while d.weekday() >= 5 or (d.month == 1 and d.day == 1):
        d += dt.timedelta(days=1)
    return d


def month_end(y, m):
    nxt = D(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def pay_day(y, m):
    """Salaries are paid on the 25th, the working day before when the 25th falls on a weekend."""
    d = D(y, m, 25)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d
