"""task231 world: the Brevland Central Bank's Business Conditions Survey (BCS), its regions, industry groups, size bands,
company numbers, clocks and the people who own the files."""
from datetime import date, datetime, timedelta, timezone

import params as P

ORG = "Brevland Central Bank"
UNIT = "Business Surveys Unit, Economic Statistics Department"
REGISTER = "Brevland Business Register"

PEOPLE = {
    "head": "Wenche Myklebust",          # head of the business survey unit
    "director": "Håkon Abrahamsen",  # director of economic statistics
    "cc": "Stein Thomassen",             # contact centre manager
    "analyst": "Turid Rønning",     # survey analyst
}

REGS = [r[0] for r in P.REGIONS]
NAME = {r[0]: r[1] for r in P.REGIONS}

# Before the 2023 regional review the survey used the bank's older numeric region codes, and two regions had shorter
# names. The review gave every region an R code and renamed those two; no boundary moved.
OLD_CODE = {"R01": "01", "R10": "02", "R02": "03", "R08": "04", "R09": "05", "R11": "06",
            "R12": "07", "R05": "08", "R06": "09", "R03": "10", "R07": "11", "R04": "12"}
OLD_NAME = dict(NAME)
OLD_NAME["R06"] = "Uplands"
OLD_NAME["R09"] = "Lakes"
REVIEW_EFFECTIVE = date(2023, 4, 1)

# The survey's nine industry groups are NACE Rev. 2 sections. The business register moved to NACE Rev. 2.1 on
# 1 January 2025; firms recruited since then carry Rev. 2.1 sections.
GROUPS = [(c, n) for c, n, _ in P.INDUSTRIES]
GROUP_NAME = dict(GROUPS)
REV21_FROM = date(2025, 1, 1)
REV2_TO_REV21 = {"A": "A", "C": "C", "F": "F", "G": "G", "H": "H", "I": "I", "J": "J", "M": "N", "N": "O"}
REV21_TO_GROUP = {"A": "A", "C": "C", "F": "F", "G": "G", "H": "H", "I": "I", "J": "J", "K": "J", "N": "M", "O": "N"}
REV21_NAME = {"A": "Agriculture, forestry and fishing", "C": "Manufacturing", "F": "Construction",
              "G": "Wholesale and retail trade", "H": "Transportation and storage", "I": "Accommodation and food service activities",
              "J": "Publishing, broadcasting, and content production and distribution",
              "K": "Telecommunication, computer programming, consulting, computing infrastructure, and other information service activities",
              "N": "Professional, scientific and technical activities", "O": "Administrative and support service activities"}
SIZE_NAME = {s[0]: s[1] for s in P.SIZES}

# Company numbers: six digits until 1 March 2021, when the register added a check digit (weights 7 to 2, modulus 11,
# remainder 10 never issued). The register and the bank's panel files show the current form; lists built before the
# change can still carry the six-digit form.
NUMBER_CHANGE = date(2021, 3, 1)
WEIGHTS = (7, 6, 5, 4, 3, 2)


def check_digit(core):
    s = sum(int(d) * w for d, w in zip("%06d" % core, WEIGHTS))
    r = (11 - s % 11) % 11
    return None if r == 10 else r


def company_number(core):
    return "%06d-%d" % (core, check_digit(core))


def old_number(core):
    return "%06d" % core


# Clocks: every timestamp in the files is UTC. Brevland time is UTC+1, and UTC+2 from 01:00 UTC on the last Sunday of
# March to 01:00 UTC on the last Sunday of October.
def _last_sunday(y, m):
    d = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


def offset_hours(utc_dt):
    y = utc_dt.year
    start = datetime(y, 3, _last_sunday(y, 3).day, 1, 0, tzinfo=timezone.utc)
    end = datetime(y, 10, _last_sunday(y, 10).day, 1, 0, tzinfo=timezone.utc)
    return 2 if start <= utc_dt < end else 1


def local_to_utc(d, hh, mm, ss=0):
    """a Brevland wall-clock time on date d, as an aware UTC datetime"""
    naive = datetime(d.year, d.month, d.day, hh, mm, ss, tzinfo=timezone.utc)
    guess = naive - timedelta(hours=1)
    off = offset_hours(guess)
    out = naive - timedelta(hours=off)
    if offset_hours(out) != off:
        out = naive - timedelta(hours=offset_hours(out))
    return out


def utc_to_local(utc_dt):
    return (utc_dt + timedelta(hours=offset_hours(utc_dt))).replace(tzinfo=None)


def iso(utc_dt):
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def close_utc(close_date):
    """the main close, 17:00 Brevland time on the close date"""
    return local_to_utc(close_date, 17, 0)


# Round labels: the calendar and the contact centre's records use 2026-09, the survey database uses 2026Q3.
def round_code(frame):
    return "%d-%02d" % (frame.year, frame.month)


def round_quarter(frame):
    return "%dQ%d" % (frame.year, (frame.month - 1) // 3 + 1)


def round_name(frame):
    return frame.strftime("%B %Y")
