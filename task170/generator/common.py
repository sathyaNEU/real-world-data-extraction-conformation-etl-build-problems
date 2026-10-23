"""task170 constants shared by every generator module.

Ruvari County is a fictional lakeshore county in Kenya. Its health department and Tulivu Health Partners, the
implementing non-profit, distribute LulaNet R repellent sleeping nets (one net to two people) county-wide in March
2027 against Ombeni fever, a fictional mosquito-borne protozoal fever whose vector is the fictional Anopheles
ruvariensis. The Arnbridge Foundation approves the campaign grant in December 2026 on Tulivu's forecast of the cases
the nets will avert among the people sleeping under them from April to December 2027. Every record is invented.

The seed was fixed by rule before any data was generated: the task number, then the pull's month and day."""
from __future__ import annotations

import datetime as dt
import os

SEED = 1701012

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")
GOLDEN = os.path.join(TASK_DIR, "golden")

D = dt.date
PULL = D(2026, 10, 12)              # every file pulled for the forecast
HLC_START, HLC_END = D(2024, 1, 1), D(2026, 9, 30)
REG_MAIN = (D(2026, 9, 7), D(2026, 9, 26))
REG_MOPUP = (D(2026, 10, 1), D(2026, 10, 9))
KHIS_START, KHIS_END = (2024, 1), (2026, 9)
BOUNDARY = D(2026, 7, 1)            # the county's ward realignment: Lwala ward moves from Kendagi to Oyamo
SAT_START = (2026, 1)               # satellite clinics reporting under their own codes from January 2026
SAT_PARENT_UNTIL = (2026, 3)        # the parents' returns still carried the satellites' OPD to March 2026
WINDOW = [(2027, m) for m in range(4, 13)]   # April to December 2027
NET_RULE = (2, 4)                   # one net for every two usual members, rounded up, at most four a household

ORG = "Tulivu Health Partners"
COUNTY = "Ruvari County"
CHD = "Ruvari County Department of Health"
DONOR = "Arnbridge Foundation"
PEOPLE = {
    "me": "Dorcas Kagwiria",        # monitoring and evaluation lead, Tulivu Health Partners
    "vbd": "Elkana Karanja",        # county vector-borne disease control coordinator
    "ento": "Amos Simiyu",          # county entomologist
}

# sub-counties as the county's realignment of 1 July 2026 draws them
SUBCOUNTIES = [("RTN", "Ruvari Town"), ("MWR", "Mwiri"), ("KDG", "Kendagi"), ("OYM", "Oyamo"), ("NDR", "Ndira"),
               ("KBR", "Kobura"), ("WKL", "Wakula")]
SC_NAME = dict(SUBCOUNTIES)
SC_CODES = [c for c, _ in SUBCOUNTIES]
WARDS = {
    "RTN": ["Ruvari Central", "Bondo Gate", "Kamwala"],
    "MWR": ["Mwiri North", "Mwiri South", "Siala", "Kadero"],
    "KDG": ["Kendagi", "Ombogo", "Kitere"],
    "OYM": ["Oyamo", "Got Oyuga", "Masala", "Lwala"],     # Lwala sat in Kendagi until 30 June 2026
    "NDR": ["Ndira", "Ugowe", "Kalanya"],
    "KBR": ["Kobura", "Rabondo", "Wiga", "Nyakadho"],
    "WKL": ["Wakula", "Sirongo", "Ndhuru"],
}
MOVED_WARD = ("Lwala", "KDG", "OYM")

# the night's collection hours, 18:00 to 06:00
HOURS = list(range(12))             # bin h covers 18+h to 19+h, wrapping past midnight


def hour_label(h, style):
    a, b = (18 + h) % 24, (19 + h) % 24
    if style == "colon":
        return "%02d:00-%02d:00" % (a, b)
    if style == "compact":
        return "%02d00-%02d00" % (a, b)
    def twelve(x):
        return "%d%s" % (x % 12 or 12, "pm" if 12 <= x < 24 else "am")
    return "%s-%s" % (twelve(a), twelve(b))


def months(a, b):
    y, m = a
    out = []
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out
