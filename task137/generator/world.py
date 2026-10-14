"""task137 constants and helpers shared by every generator module.

Kaimai Building Society (fictional), a mutual deposit-taker in Tauranga, New Zealand: its term deposit maturity calls,
made since December 2024 by Harbourline Contact Services (fictional, Palmerston North) under a statement of work that
bills agent time per event against a quarterly take-or-pay block. The January to March 2027 list (18,400 deposits) was
cut on 2 November 2026; the block is due on 20 November 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1370411

# ---------------------------------------------------------------------------------------------------------------
# Calendar of the fiction
REQUEST = dt.date(2026, 11, 4)
CUT_FWD = dt.date(2026, 11, 2)
CARD_APPROVED = dt.date(2026, 10, 27)
BLOCK_DUE = dt.date(2026, 11, 20)
LAST_CLOSEOUT = dt.date(2026, 10, 21)
SOW_START = dt.date(2024, 12, 1)
CORE_UPGRADE = dt.date(2026, 1, 12)          # the society's core banking upgrade (list layout, account format)
KIP_FROZEN = dt.date(2026, 6, 30)            # legacy investment platform's final full register
EVENTS_FROM, EVENTS_TO = dt.date(2025, 1, 1), dt.date(2026, 10, 31)
EXPORT_STAMP = dt.datetime(2026, 11, 3, 20, 35, tzinfo=dt.timezone.utc)   # 9.35 am on 4 November in Tauranga

COMPANY = "Kaimai Building Society"
VENDOR = "Harbourline Contact Services"
SOW_REF = "HCS-KBS-2025-01"

PEOPLE = {
    "product": "Hazel Johnstone",      # term deposits product manager (the requester; never named in the prompt)
    "head": "Stuart Waller",           # head of deposits, signs the block order
    "vendor": "Suzanne Wallis",        # Harbourline account manager
    "data": "Joseph Herd",             # customer data steward, keeps the do-not-call register
    "treasury": "Sienna Stewart",      # treasury pricing analyst, prepares the quarterly card for ALCO
    "wfm": "Ashton Findlay",           # Harbourline workforce planner
}

# ---------------------------------------------------------------------------------------------------------------
# Quarters
def q_of(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def q_add(q, n):
    y, k = int(q[:4]), int(q[-1])
    idx = y * 4 + (k - 1) + n
    return "%dQ%d" % (idx // 4, idx % 4 + 1)


def q_start(q):
    return dt.date(int(q[:4]), 3 * (int(q[-1]) - 1) + 1, 1)


def q_end(q):
    return q_start(q_add(q, 1)) - dt.timedelta(days=1)


def q_label(q):
    names = {1: "January to March", 2: "April to June", 3: "July to September", 4: "October to December"}
    return "%s %s" % (names[int(q[-1])], q[:4])


PAST = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
FWD = "2027Q1"
FWD_LIST_SIZE = 18400
CUTS = {"2025Q1": dt.date(2024, 11, 1), "2025Q2": dt.date(2025, 2, 3), "2025Q3": dt.date(2025, 5, 2),
        "2025Q4": dt.date(2025, 8, 1), "2026Q1": dt.date(2025, 11, 3), "2026Q2": dt.date(2026, 2, 2),
        "2026Q3": dt.date(2026, 5, 1), "2026Q4": dt.date(2026, 8, 3), "2027Q1": CUT_FWD}
TERMS = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------------------------------------------------------
# The posted term deposit card (per cent a year), set by ALCO each quarter for the quarter.
ONE_YEAR = {
    "2019Q1": 3.30, "2019Q2": 3.20, "2019Q3": 3.00, "2019Q4": 2.95,
    "2020Q1": 2.90, "2020Q2": 2.40, "2020Q3": 1.80, "2020Q4": 1.40,
    "2021Q1": 1.25, "2021Q2": 1.35, "2021Q3": 1.60, "2021Q4": 2.10,
    "2022Q1": 2.75, "2022Q2": 3.40, "2022Q3": 4.20, "2022Q4": 4.90,
    "2023Q1": 5.40, "2023Q2": 5.75, "2023Q3": 6.00, "2023Q4": 6.00,
    "2024Q1": 5.90, "2024Q2": 5.85, "2024Q3": 5.45, "2024Q4": 4.95,
    "2025Q1": 4.50, "2025Q2": 4.15, "2025Q3": 3.85, "2025Q4": 3.65,
    "2026Q1": 3.40, "2026Q2": 3.30, "2026Q3": 3.20, "2026Q4": 3.15,
    "2027Q1": 3.20,
}


def spread(q):
    y, k = int(q[:4]), int(q[-1])
    if q == "2027Q1":
        return [0, .30, .55, .80, 1.00]
    if y == 2026:
        return [0, .25, .50, .75, .95]
    if y <= 2021:
        return [0, .15, .30, .45, .55]
    if y == 2022 and k <= 2:
        return [0, .30, .50, .60, .95]
    if y == 2022:
        return [0, .20, .25, .25, .25]
    if y == 2023 and k == 1:
        return [0, -.05, -.15, -.25, -.30]
    if (y == 2023) or (y == 2024 and k <= 2):
        return [0, -.20, -.50, -.70, -.80]
    if y == 2024:
        return [0, -.25, -.45, -.55, -.55]
    if y == 2025 and k == 1:
        return [0, -.10, -.15, -.15, -.10]
    return [0, .10, .25, .40, .55]


def card(q, term):
    return round(ONE_YEAR[q] + spread(q)[term - 1], 2)


# New-money specials: (opening quarter, term) -> rate, and the share of that cohort's new deposits taken at it.
SPECIALS = {("2023Q3", 3): (6.00, 0.35), ("2023Q4", 2): (6.30, 0.35), ("2024Q2", 1): (6.35, 0.35),
            ("2024Q4", 1): (5.45, 0.22),
            ("2023Q1", 4): (5.65, 0.0)}   # the 2023Q1 four-year special: its volume is set separately
WINDOW_SPECIALS = {("2025Q1", 1): (5.10, 0.50), ("2025Q2", 1): (4.75, 0.50), ("2025Q3", 1): (4.45, 0.50)}
SPECIAL_NAMES = {("2023Q3", 3): "Three-year special", ("2023Q4", 2): "Two-year special",
                 ("2024Q2", 1): "One-year special", ("2023Q1", 4): "Four-year special"}

# ---------------------------------------------------------------------------------------------------------------
# Harbourline's dialling calendar: weekdays, less New Zealand public holidays, Wellington Anniversary Day
# (Harbourline is in the Wellington province) and its close-down from 24 December to 3 January.
def _easter(y):
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def _mondayise(d):
    if d.weekday() == 5:
        return d + dt.timedelta(days=2)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def _nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    while d.weekday() != wd:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


MATARIKI = {2022: dt.date(2022, 6, 24), 2023: dt.date(2023, 7, 14), 2024: dt.date(2024, 6, 28),
            2025: dt.date(2025, 6, 20), 2026: dt.date(2026, 7, 10), 2027: dt.date(2027, 6, 25)}


def _pair(first, second):
    """Two consecutive holidays (New Year, Christmas): a day falling on a weekend is observed on the next weekday not
    already taken."""
    out = set()
    for d in (first, second):
        k = d
        while k.weekday() >= 5 or k in out:
            k += dt.timedelta(days=1)
        out.add(k)
    return out


def holidays(y):
    e = _easter(y)
    out = {e - dt.timedelta(days=2), e + dt.timedelta(days=1), _mondayise(dt.date(y, 2, 6)),
           _mondayise(dt.date(y, 4, 25)), _nth_weekday(y, 6, 0, 1), _nth_weekday(y, 10, 0, 4),
           } | ({MATARIKI[y]} if y in MATARIKI else set())
    out |= _pair(dt.date(y, 1, 1), dt.date(y, 1, 2)) | _pair(dt.date(y, 12, 25), dt.date(y, 12, 26))
    # Wellington Anniversary: the Monday nearest 22 January
    d = dt.date(y, 1, 22)
    mon = d - dt.timedelta(days=d.weekday())
    if (d - mon).days > 3:
        mon += dt.timedelta(days=7)
    out.add(mon)
    return out


_HOL = set()
for _y in range(2019, 2028):
    _HOL |= holidays(_y)


def closedown(d):
    return (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 3)


def dialling_day(d):
    return d.weekday() < 5 and d not in _HOL and not closedown(d)


def dialling_days(release, maturity):
    """Days Harbourline may dial a case: from its release date to the day before maturity."""
    out, d = [], release
    while d < maturity:
        if dialling_day(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def business_day(d):
    return d.weekday() < 5 and d not in _HOL


# ---------------------------------------------------------------------------------------------------------------
# The SOW: billing and dispositions
MIN_NOT_REACHED = 1.5
MIN_CONVERSATION = 8.0
MIN_RETENTION = 22.0
NOT_REACHED = ("NOA", "BSY", "VML", "DIS", "WNG")
CONVERSATION = ("RNW", "CHG", "DEC")
RETENTION = ("RTK", "RTW")
DEAD_CODE, WRONG_CODE = "DIS", "WNG"
CODES = {
    "NOA": "No answer", "BSY": "Busy", "VML": "Voicemail reached, no message left",
    "DIS": "Number disconnected or not in service", "WNG": "Answered by someone other than the holder",
    "RNW": "Holder reached: reinvestment confirmed as notified", "CHG": "Holder reached: other instructions taken",
    "DEC": "Holder reached: declined to discuss", "RTK": "Holder reached: retention offer, deposit kept",
    "RTW": "Holder reached: retention offer, funds to be withdrawn or moved",
}


def billed_minutes(code):
    if code in NOT_REACHED:
        return MIN_NOT_REACHED
    if code in RETENTION:
        return MIN_RETENTION
    return MIN_CONVERSATION


# ---------------------------------------------------------------------------------------------------------------
# The process (the data's generating parameters; none ships)
P_ANSWER = {"M": 0.22, "H": 0.13, "W": 0.085}
P_DEAD = {"M": 0.02, "H": 0.06, "W": 0.08}
P_WRONG = {"M": 0.03, "H": 0.02, "W": 0.05}
NONANSWER = (("NOA", 0.72), ("BSY", 0.08), ("VML", 0.20))
DIALS_PER_NUMBER = 6
WITHDRAW_PER_DAY = 0.004
PRE_RELEASE_INSTRUCTED = 0.046
RET_SLOPE, RET_MID = 1.8, 2.20
SPEC_LEVEL, SPEC_SLOPE, SPEC_MID = 0.87, 6.0, 0.30
RETENTION_KEPT = 0.55
PLAIN = (("RNW", 0.70), ("CHG", 0.22), ("DEC", 0.08))


def p_retention(drop, special=False):
    if special:
        return SPEC_LEVEL / (1.0 + math.exp(-SPEC_SLOPE * (drop - SPEC_MID)))
    return 1.0 / (1.0 + math.exp(-RET_SLOPE * (drop - RET_MID)))


# ---------------------------------------------------------------------------------------------------------------
# Identifiers and formats
BANK_BRANCH = "86-0410"
TD_SUFFIXES = ("030", "031", "032", "033", "034", "035")
SAV_SUFFIXES = ("000", "001", "002")
KIC_SUFFIX = "060"
SETTLEMENT = "8604109000017099"     # the society's term deposit maturity settlement account (payments system)


def acct_dashed(body, suffix):
    return "%s-%07d-%s" % (BANK_BRANCH, body, suffix)


def acct_plain(body, suffix):
    return "%s%07d%s" % (BANK_BRANCH.replace("-", ""), body, suffix)


def norm_acct(s):
    return "".join(ch for ch in str(s) if ch.isdigit())


def e164(digits_nat):
    """'0274123456' or '075781234' (national, leading zero) to '+64274123456'."""
    return "+64" + digits_nat[1:]


def norm_phone(s):
    d = "".join(ch for ch in str(s) if ch.isdigit())
    if d.startswith("64"):
        d = d[2:]
    if d.startswith("0"):
        d = d[1:]
    return "+64" + d


# ---------------------------------------------------------------------------------------------------------------
# Deterministic random streams: one per named purpose, independent of call order elsewhere.
def rng(name):
    h = int(hashlib.sha256(("%d/%s" % (SEED, name)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def write_csv(path, cols, rows, crlf=False, quote_all=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n",
                   quoting=csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL)
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def money(x):
    return "%.2f" % x


# ---------------------------------------------------------------------------------------------------------------
# File names in the pack (target/)
F_LIST_FWD = "kbs_td_retention_list_2027Q1.csv"
F_LISTS_2025 = "kbs_td_retention_lists_2025.csv"
F_LISTS_2026 = "kbs_td_retention_lists_2026.csv"
F_RELEASE = "kbs_case_release_log_2025q1-2026q3.csv"
F_DIALS = "harbourline_dial_log_2025q1-2026q3.csv"
F_CLOSEOUT = "harbourline_case_closeouts_2025q1-2026q3.csv"
F_CONTACTS = "kbs_contact_points_2026-11-02.csv"
F_DNC = "kbs_do_not_call_register_2026-11-02.csv"
F_SOW = "harbourline_sow_HCS-KBS-2025-01.pdf"
F_PROCEDURE = "kbs_td_retention_procedure_v4.docx"
F_THREAD = "harbourline_q1_2027_block_order.eml"
F_EVENTS = "kbs_td_account_events_2025-01_2026-10.csv"
F_TRANSFERS = "kbs_member_transfers_2025-01_2026-10.csv"
F_HOLDINGS = "kbs_term_holdings_2026-11-02.csv"
F_KIP = "kip_certificate_register_2026-06-30.csv"
F_BATCHES = "kip_migration_batches_2026.csv"
F_NOTES = "kbs_extract_notes_2026-11.txt"
F_OUTLOOK = "kbs_treasury_funding_outlook_fy2027.xlsx"
F_PROPOSAL = "harbourline_2027_staffing_proposal.pdf"


def brief_name(q):
    return "harbourline_campaign_brief_%s.pdf" % q


DISTRACTORS = [F_OUTLOOK, F_PROPOSAL]
