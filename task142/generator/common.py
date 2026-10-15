"""task142 constants and helpers shared by every generator module.

Ironbark Health Alliance Inc. (fictional) is a purchasing alliance of five public health services in Melbourne's
north and west. Each member runs a Hospital in the Home (HITH) program. Bellbird Home Nursing Pty Ltd (fictional)
holds the alliance's overflow nursing agreement; its Schedule 2 sets the January to March 2027 block at 850 visits,
booked by the members in lots of 25. The booking is lodged by Friday 6 November 2026."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 1420615

# ---------------------------------------------------------------------------------------------------- calendar
D0 = dt.date(2024, 4, 1)          # first admission date in the episode extract
D1 = dt.date(2026, 9, 30)         # the extract's close (data to the end of this day)
CENSUS0 = dt.date(2025, 7, 1)     # the census warehouse's first day
REVISION = dt.date(2025, 7, 1)    # the program streams revised (new codes for admissions from this day)
MERGER = dt.date(2025, 3, 1)      # Altona Park Health merged into Westmere Health; campus codes reissued
PATH = dt.date(2026, 10, 1)       # the bone and joint infection at home pathway opens at Northgate and Westmere
Q0 = dt.date(2027, 1, 1)          # the booked quarter
Q1 = dt.date(2027, 3, 31)
POOL_LAST_ADMISSION = dt.date(2026, 6, 30)   # the golden stays pool: completed episodes admitted to this day
FY0 = dt.date(2026, 7, 1)         # the 2026-27 financial year
FY1 = dt.date(2027, 6, 30)
Q3S = dt.date(2026, 7, 1)         # the asks' quarter
Q3E = dt.date(2026, 9, 30)
APP_RELEASE = dt.datetime(2026, 8, 3, 0, 0)          # Bellbird app 5.0, Melbourne time: new visit status codes
OUTAGE = (dt.datetime(2026, 8, 10, 6, 0), dt.datetime(2026, 8, 13, 15, 0))   # referral portal down (Melbourne)
OUTAGE_MAR = (dt.datetime(2026, 3, 17, 7, 30), dt.datetime(2026, 3, 17, 16, 45))
HOLIDAY_Q3 = dt.date(2026, 9, 25)                    # Friday before the AFL Grand Final, Victoria
SCHEDULE2_DATE = dt.date(2026, 10, 2)
CAPACITY_DATE = dt.date(2026, 10, 19)
PLAN_REVISION_DATE = dt.date(2026, 10, 14)
BOOKING_DUE = dt.date(2026, 11, 6)
PACK_STAMP = dt.datetime(2026, 11, 2, 22, 14, tzinfo=dt.timezone.utc)   # Tuesday 3 November 2026 09:14 Melbourne

MONTHS_FY = [dt.date(2026, m, 1) for m in range(7, 13)] + [dt.date(2027, m, 1) for m in range(1, 7)]
MONTH_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
MON3 = {k: v[:3] for k, v in MONTH_NAME.items()}


def days(a, b):
    """Dates from a to b, both included."""
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


def month_end(d):
    n = dt.date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)
    return n - dt.timedelta(days=1)


def melbourne(t_utc):
    """UTC (naive) to Melbourne wall time (naive). AEST +10; AEDT +11 from the first Sunday of October 02:00 AEST to
    the first Sunday of April 03:00 AEDT."""
    y = t_utc.year

    def first_sunday(month):
        d = dt.date(y, month, 1)
        while d.weekday() != 6:
            d += dt.timedelta(days=1)
        return d
    dst_on = dt.datetime.combine(first_sunday(10), dt.time(16, 0)) - dt.timedelta(days=1)    # 02:00 AEST in UTC
    dst_off = dt.datetime.combine(first_sunday(4), dt.time(16, 0)) - dt.timedelta(days=1)    # 03:00 AEDT in UTC
    off = 11 if (t_utc >= dst_on or t_utc < dst_off) else 10
    return t_utc + dt.timedelta(hours=off)


def to_utc(t_local):
    """Melbourne wall time (naive) to UTC (naive), for the dates the pack uses (no ambiguous hour arises)."""
    for off in (10, 11):
        u = t_local - dt.timedelta(hours=off)
        if melbourne(u) == t_local:
            return u
    raise ValueError(t_local)


# ---------------------------------------------------------------------------------------------------- the alliance
ALLIANCE = "Ironbark Health Alliance Inc."
ALLIANCE_SHORT = "Ironbark Health Alliance"
PROVIDER = "Bellbird Home Nursing Pty Ltd"
PROVIDER_SHORT = "Bellbird Home Nursing"
MEMBERS = ["NGH", "RBH", "WMH", "KDH", "HCH"]                 # Schedule 2's member order for 2026-27
NAME = {"NGH": "Northgate Health", "RBH": "Riverbend Health", "WMH": "Westmere Health", "KDH": "Kingsdale Health",
        "HCH": "Hillcrest Health"}
SHORT = {"NGH": "Northgate", "RBH": "Riverbend", "WMH": "Westmere", "KDH": "Kingsdale", "HCH": "Hillcrest"}
PATHWAY_MEMBERS = ["NGH", "WMH"]
BLOCK = 850
LOT = 25

PEOPLE = {
    "requester": "Joan Rogers",          # HITH program manager, the alliance (not in the prompt)
    "data": "Tony Tucker",               # alliance data officer: the warehouse and its extracts
    "finance": "Dennis McMahon",         # alliance finance, provider payments
    "ng_num": "Maureen Phillips",        # nurse unit manager, Northgate HITH
    "wm_mgr": "Miranda Medina",          # HITH manager, Westmere Health
    "id_lead": "George Grant",           # infectious diseases physician, pathway clinical lead
    "bellbird": "Timothy Cardenas",      # account manager, Bellbird Home Nursing
}

# ---------------------------------------------------------------------------------------------------- streams
STREAMS = ["H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08"]
SNAME = {"H01": "Skin and soft tissue infection", "H02": "Urinary tract infection", "H03": "Respiratory infection",
         "H04": "Bone and joint infection", "H05": "Endocarditis and other deep infection", "H06": "Wound care",
         "H07": "Venous thromboembolism", "H08": "Heart failure"}
OLD_PROGRAMS = {"AB": "Intravenous antibiotics", "WC": "Wound care", "AC": "Anticoagulation", "HF": "Heart failure"}
INFECTION = ["H01", "H02", "H03", "H04", "H05"]
VISIT_TYPE = {"H01": "IVT", "H02": "IVT", "H03": "IVT", "H04": "IVT", "H05": "IVT", "H06": "WND", "H07": "CLN",
              "H08": "CLN"}


def visits_on_day(stream, k):
    """Nurse visits on day k of a stay (0 = the admission day), by the visit schedule of July 2025."""
    if stream == "H06":
        return 1 if k % 2 == 0 else 0
    if stream == "H08":
        return 2 if k < 2 else 1
    return 1


# ---------------------------------------------------------------------------------------------------- the pack
EPISODES = "hith_episodes_2024-04-01_to_2026-09-30.csv"
CENSUS = "hith_census_daily_2025-07-01_to_2026-09-30.csv"
PLANS = "hith_operating_plans_2026-27_rev_oct2026.xlsx"
CAPACITY = "hith_inhouse_capacity_return_2027q1.xlsx"
SCHED2 = "bellbird_agreement_schedule2_2027q1_block.pdf"
STREAMDOC = "hith_program_streams_and_visit_schedule_2025-07.pdf"
CROSSWALK = "hith_program_stream_crosswalk_2025-07.csv"
CAMPUSES = "alliance_member_campuses.csv"
PATHWAY = "bji_at_home_pathway_northgate_westmere_2026.docx"
BB_VISITS = "bellbird_visits_2026-07-01_to_2026-09-30.jsonl"
PORTAL = "referral_portal_bellbird_2026-07-01_to_2026-09-30.csv"
REGISTER = "bellbird_intake_register_2026.xlsx"
SCHED34 = "bellbird_agreement_schedules3-4_fees_and_service_levels.pdf"
ACCOUNTS = "bellbird_client_accounts.csv"
CALENDAR = "alliance_finance_calendar_2026-27.csv"
DICTIONARY = "data_dictionary.xlsx"
MANIFEST = "export_manifest.csv"
SURVEY = "hith_patient_experience_survey_2025-26.xlsx"
BB_REPORT = "bellbird_service_report_2025-26.pdf"
DECLINED = "bellbird_declined_referrals_2025-26.csv"
DISTRACTORS = [SURVEY, BB_REPORT, DECLINED]
CALL_FILES = [EPISODES, CENSUS, PLANS, CAPACITY, SCHED2, STREAMDOC, CROSSWALK, CAMPUSES, PATHWAY]
ASK_FILES = [BB_VISITS, PORTAL, REGISTER, SCHED34, ACCOUNTS, CALENDAR]

GOLD_BOOK = "hith_overflow_block_2027q1.xlsx"
GOLD_CHART = "bellbird_weekly_visits_2026q3.png"

# Schedule 3 (fees from 1 July 2026, GST-free) and Schedule 4 (service levels)
FEE = {"IVT": 146.20, "WND": 121.80, "CLN": 129.40}
FEE_NAME = {"IVT": "Intravenous therapy visit", "WND": "Wound care visit", "CLN": "Clinical care visit"}
ATTEMPT_FEE = 68.40
LOAD_AFTER_HOURS = 0.25      # Monday to Friday, a visit starting before 07:00 or at or after 18:00
LOAD_SAT = 0.40
LOAD_SUN = 0.60
LOAD_HOLIDAY = 1.00
ACCEPT_HOURS = 2
FIRST_VISIT_HOURS = 24
VIC_HOLIDAYS = [(dt.date(2026, 9, 25), "Friday before the AFL Grand Final"), (dt.date(2026, 11, 3), "Melbourne Cup"),
                (dt.date(2026, 12, 25), "Christmas Day"), (dt.date(2026, 12, 26), "Boxing Day"),
                (dt.date(2026, 12, 28), "Additional day for Boxing Day"), (dt.date(2027, 1, 1), "New Year's Day"),
                (dt.date(2027, 1, 26), "Australia Day"), (dt.date(2027, 3, 8), "Labour Day"),
                (dt.date(2027, 3, 26), "Good Friday"), (dt.date(2027, 3, 27), "Saturday before Easter Sunday"),
                (dt.date(2027, 3, 28), "Easter Sunday"), (dt.date(2027, 3, 29), "Easter Monday"),
                (dt.date(2027, 4, 25), "ANZAC Day"), (dt.date(2027, 6, 14), "King's Birthday")]


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
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


def write_jsonl(path, cols, rows):
    """One JSON object a line, keys in the platform's order; a blank field is null."""
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as fh:
        for r in rows:
            obj = {c: (r.get(c) if r.get(c) != "" else None) for c in cols}
            fh.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
            n += 1
    return n


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round_half_up(x, nd=0):
    f = 10 ** nd
    return math.floor(x * f + 0.5) / f


def lots_for(excess):
    """The smallest number of lots of 25 whose visits cover the excess (none when there is no excess)."""
    if excess <= 0:
        return 0
    return int(math.ceil(excess / LOT - 1e-12))
