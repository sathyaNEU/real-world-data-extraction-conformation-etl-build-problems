"""task141 constants and helpers shared by every generator module.

Okelan County (fictional, in an unnamed state on Central time) supervises its felony and misdemeanor probationers
through the Okelan County Adult Probation Department. Under the State's 2019 realignment a felony probation term
begins with the county jail time the court orders as its condition, supervision begins on release, and a revocation
term is served in the county of supervision, so every felony revocation is a commitment to the Okelan County
Detention Center. Senate Bill 26-118, the Felony Probation Term Act, takes effect on 1 January 2027: a felony
probationer may not be supervised for more than 24 months, and a felony term in effect on that day ends on the
earlier of its scheduled expiration and the day 24 months after supervision began, but not before 31 March 2027.
The Sheriff's Office files the 2027 Jail Operations Plan with the State Jail Standards Board by 1 December 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1410327
M = 30.4375                                   # days in an average month
DAY0 = dt.date(2016, 1, 1)


def day(d):
    """date or 'YYYY-MM-DD' to an integer day count from DAY0"""
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return (d - DAY0).days


def date_of(n):
    return DAY0 + dt.timedelta(days=int(n))


def months(n):
    return int(round(n * M))


def add_months(n, k):
    """the day k calendar months after day n (the same day of the month, or the month's last day)"""
    import calendar
    d = date_of(n)
    m = d.month - 1 + k
    y, m = d.year + m // 12, m % 12 + 1
    return day(dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1])))


# ---------------------------------------------------------------------------------------------------- calendar
BURN = day("2008-01-01")               # the world runs from here so the record opens on a settled caseload
RECORD_START = day("2016-07-01")       # the extracts' first day: terms closed, petitions filed, orders made from here
CMS2_LIVE = day("2023-06-12")          # the Department's CMS 2 from this day; open cases moved across
JMS_LIVE = day("2025-02-04")           # the Sheriff's new jail management system from this day (times in UTC)
BOOKINGS_FROM = day("2019-01-01")      # the bookings extract: every probation booking in custody on or after this day
EXTRACT = day("2026-09-30")            # every record to the end of this day
PULL = dt.date(2026, 10, 2)            # the extracts were pulled
ACT_SIGNED = dt.date(2026, 5, 14)
ACT = day("2027-01-01")                # SB 26-118 takes effect
TRANS = day("2027-03-31")              # no felony term in effect on 1 January 2027 ends before this day
Y0, Y1 = day("2027-01-01"), day("2027-12-31")
PLAN_DUE = dt.date(2026, 12, 1)
POD_SIZE = 210                         # the county's filed standard: one violator pod per 210 projected admissions
POD_BEDS = 64
PODS_2026 = 5                          # violator pods the Detention Center staffs in 2026
EXT_MONTHS = 12                        # the projection's extension of a term with room, before the Act's cap

# ---------------------------------------------------------------------------------------------------- the process
P = dict(
    fel_rate=218.0, mis_rate=150.0,
    jail_share=0.85, jail_med=110.0, jail_sig=0.70, jail_term_elast=0.8, jail_lo=8, jail_hi=330,
    intake_lo=3, intake_hi=28,
    h0=0.026, h_inf=0.0060, h_tau=8.0, score_beta=0.075,
    conv_ord=0.48, conv_rev=0.48, conv_abs=0.72,
    p_rev=0.235, rev_window=90, rev_lo=7, rev_mode=30,
    lag_mean=70.0, lag_shape=3.0,
    abs_hazard=0.0022, abs_lag_mean=150.0, abs_lag_shape=2.0,
    p_ext=0.35, ext_months=(6, 12, 12, 12, 18, 24), p_ext_rev=0.30,
    et_hazard=0.006, et_after=18,
    # misdemeanor terms: twelve months, a lighter jail condition, the same two clocks
    m_term=12, m_jail_share=0.30, m_jail_med=20.0, m_jail_sig=0.6, m_jail_lo=2, m_jail_hi=60,
    m_h0=0.030, m_h_inf=0.013, m_h_tau=5.0, m_conv=0.42, m_p_rev=0.15, m_abs=0.0020,
    m_p_ext=0.25, m_ext_months=(3, 6, 6, 12), m_et_hazard=0.004, m_et_after=6,
    m_on_felony=0.10,                  # misdemeanor terms of people already on felony probation
    m_intermittent=0.07,               # misdemeanor revocations ordered served on weekends
    # the end-of-term review: a matter still open as the term runs out is met by an extension where the term has
    # room under its class maximum (and, from 2027, under the Act's cap), otherwise by a petition or not at all
    q_open=0.75, a_pet=0.03, b_ext=0.75, s_sub=0.63,
    ext_end_months=(6, 6, 12, 12, 12, 18), ext_lo=7, ext_hi=60,
    m_q_open=0.40, m_a_pet=0.25, m_b_ext=0.45, m_s_sub=0.45, m_class2=0.45,
    # the Department's offices and officers (only the asks read them)
    move_rate=0.05,                    # a probationer's move to another district, a year
    spec_fel=0.10, spec_mis=0.03, spec_lo=14, spec_hi=60,   # specialized caseloads move to Central after intake
    tenure_years=8.0, vacancy_lo=14, vacancy_hi=75,
    # the jail reclassifies a probationer it already holds when the commitment order reaches it
    order_same_day=0.30, order_next_day=0.45,
)
# felony classes and the longest probation term the State's sentencing code lets a court impose or extend to
CLASSES = (("F2", 96), ("F3", 84), ("F4", 60), ("F5", 48), ("F6", 36), ("DF4", 24))
MIS_CLASSES = (("M1", 24), ("M2", 12))
FEL_CELLS = [('DF4', 18, 0.0984), ('DF4', 24, 0.0216), ('F6', 18, 0.0984), ('F6', 24, 0.0984), ('F6', 36, 0.0432), ('F5', 36, 0.1804), ('F5', 48, 0.0396), ('F4', 48, 0.164), ('F4', 60, 0.036), ('F3', 60, 0.082), ('F3', 84, 0.018), ('F2', 60, 0.038), ('F2', 84, 0.082)]                     # (class, imposed months, share of felony terms)

# ---------------------------------------------------------------------------------------------------- people
PEOPLE = dict(
    analyst="Gina Yoder", cpo="Larry Pugh", commander="Colleen Cameron", research="Donald Russo",
    clerk="Megan Chambers", budget="Gloria Lynch",
)
COUNTY = "Okelan County"
DEPT = "Okelan County Adult Probation Department"
JAIL = "Okelan County Detention Center"
COURT = "Okelan County Circuit Court"
BOARD = "State Jail Standards Board"

OFFICES = (("CEN", "Central", "C"), ("NGT", "Northgate", "N"), ("RVS", "Riverside", "R"), ("EFD", "Eastfield", "E"))
OFFICE_W = (0.38, 0.22, 0.24, 0.16)    # a term's district; the eastern townships (EFD) from Central or Riverside
EFD_OPEN = day("2025-06-02")           # Eastfield opens and takes over the eastern townships' open terms
POOLS = dict(CEN=(58, 45), NGT=(29, 29), RVS=(40, 32), EFD=(0, 23))   # line officers before and after Eastfield
EFD_FROM = dict(CEN=13, RVS=8)         # officers moved to Eastfield on its opening
REDISTRICT = day("2026-10-01")         # the Department's caseload redistribution, entered before the export of 2 October
REDISTRICT_MOVES = (("CEN", "EFD", 3), ("CEN", "NGT", 2), ("RVS", "EFD", 1), ("NGT", "RVS", 1))

# ---------------------------------------------------------------------------------------------------- the pack
CMS1 = "cms1_supervision_cases_2016_2023.csv"
CMS2 = "cms2_supervision_cases_2023_2026.csv"
ORDERS = "circuit_court_term_orders_2016_2026.csv"
PETITIONS = "circuit_court_violation_petitions_2016_2026.csv"
BOOKINGS = "detention_probation_bookings_2019_2026.csv"
PERSONS = "person_id_crosswalk.csv"
JAIL_CODES = "jms_booking_codes.csv"
COURT_CODES = "circuit_court_codes.xlsx"
OFFICE_CODES = "apd_office_codes.csv"
ROSTER = "apd_officer_assignments_2016_2026.csv"
ACT_PDF = "sb26_118_felony_probation_term_act.pdf"
PLAN_PDF = "jail_operations_plan_instructions_2027.pdf"
REPORT = "apd_annual_report_2025.pdf"
HEADCOUNT = "detention_daily_headcount_2025_2026.csv"
DISTRACTORS = [REPORT, HEADCOUNT]

GOLD_BOOK = "violator_housing_plan_2027.xlsx"
GOLD_MEMO = "violator_housing_memo_2027.docx"
GOLD_CHART = "felony_revocation_admissions_2019_2027.png"

QUARTERS = (("2025-10-01", "2025-12-31", "October to December 2025"), ("2026-01-01", "2026-03-31", "January to March 2026"),
            ("2026-04-01", "2026-06-30", "April to June 2026"), ("2026-07-01", "2026-09-30", "July to September 2026"))
TERM_BANDS = (("up to 24 months", 0, 24), ("25 to 36 months", 25, 36), ("37 to 60 months", 37, 60), ("over 60 months", 61, 999))
SUP_BANDS = (("under 12 months", 0, 12), ("12 to 24 months", 12, 24), ("over 24 months", 24, 9999))


# ---------------------------------------------------------------------------------------------------- Central time
def _nth_sunday(y, month, n):
    d = dt.date(y, month, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def central_offset(t_local):
    """hours from local (naive) Central wall time to UTC: CDT from the second Sunday of March 02:00 to the first Sunday
    of November 02:00 (the repeated hour taken as its first, daylight, instance), CST otherwise"""
    y = t_local.year
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(2, 0))
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(1, 0)) + dt.timedelta(hours=1)
    return 5 if start <= t_local < end else 6


def to_utc(t_local):
    return t_local + dt.timedelta(hours=central_offset(t_local))


def from_utc(t_utc):
    y = t_utc.year
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(8, 0))       # 02:00 CST = 08:00 UTC
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(7, 0))        # 02:00 CDT = 07:00 UTC
    return t_utc - dt.timedelta(hours=5 if start <= t_utc < end else 6)


def at(n, minutes):
    """an integer day and minutes past local midnight to a naive local datetime"""
    return dt.datetime.combine(date_of(n), dt.time(0, 0)) + dt.timedelta(minutes=int(minutes))


# ---------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """an independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)"""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_to(x, step):
    """half away from zero to a multiple of step (the deliverables' convention)"""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round1(x):
    return math.floor(x * 10 + 0.5) / 10 if x >= 0 else -math.floor(-x * 10 + 0.5) / 10


def pods(admissions):
    """the county's filed standard: one pod for each 210 projected admissions or part of 210"""
    return int(math.ceil(admissions / POD_SIZE - 1e-12))


def font_path(rel):
    """a font file by its Linux path under /usr/share/fonts/truetype/, or by its file name in the user's fonts folder
    (the same Carlito and Liberation files, laid out flat on macOS)"""
    import os
    for p in ("/usr/share/fonts/truetype/" + rel, os.path.expanduser("~/Library/Fonts/" + os.path.basename(rel))):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(rel)
