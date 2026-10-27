"""task157 (architecture 2) constants and helpers shared by every generator module.

The world: the Arizona Secretary of State's elections division holds a filed initiative petition, serial
I-18-2028, a constitutional initiative for the 7 November 2028 general election. The committee filed 44,360
petition sheets on Thursday 6 July 2028; the office struck 240 sheets two firms had already filed and
receipted the rest, which carry 540,000 signature lines between them. The required number is 384,924,
fifteen per cent of the 2,566,154 votes cast for Governor in 2026. The office drew the statutory five per
cent random sample of the signatures filed, 27,000 lines, on Tuesday 11 July 2028 and transmitted it to the
fifteen county recorders, whose returns closed on Wednesday 2 August 2028. The division's own consolidation
check closed on 3 August and the projection is due on Friday 4 August 2028, which is the as-of date of every
file in the pack.

The world seed is fixed by rule and is the task number: the design note's ladder, bin and convergence tables
are measured at seed 157 and swept over 157 to 162."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 157
SWEEP_SEEDS = (157, 158, 159, 160, 161, 162)

OFFICE = "Arizona Secretary of State"
DIVISION = "Elections Division"
SERIAL = "I-18-2028"
MEASURE_SHORT = "Arizona Water Security and Groundwater Protection Act"

# Personas: guard.py names --geo "United States" --seed 157, screened to zero people.* warnings.
PEOPLE = {
    "director": "Philip James",     # State Elections Director, signs the filing and sample record
    "analyst": "Laura Davis",       # Elections Division data unit, the division's own consolidation check
    "recorder": "Tony Lynch",       # Navajo County Recorder, signs the 2019 disposition code list
}

# ------------------------------------------------------------------------------------------------- calendar
ELECTION_2026 = dt.date(2026, 11, 3)
GOV_VOTES_2026 = 2_566_154
SERIAL_ISSUED = dt.date(2027, 12, 6)
EARLY_SNAPSHOT = dt.date(2027, 12, 20)          # the last monthly AVID snapshot before circulation opened
WINDOW_OPEN = dt.date(2028, 1, 3)               # Monday
WINDOW_CLOSE = dt.date(2028, 6, 30)             # Friday
LIST_MAINTENANCE = dt.date(2028, 3, 14)         # the statewide list-maintenance run, inside the window
FILED = dt.date(2028, 7, 6)                     # Thursday, the committee filed
RECEIPT_CLOSED = dt.date(2028, 7, 7)
LATE_SNAPSHOT = dt.date(2028, 7, 10)            # Monday
SAMPLE_DRAWN = dt.date(2028, 7, 11)             # Tuesday
RETURNS_OPEN = dt.date(2028, 7, 14)
RETURNS_CLOSE = dt.date(2028, 8, 2)             # Wednesday, fifteen business days
CORRECTIONS_CLOSE = dt.date(2028, 8, 3)
AS_OF = dt.date(2028, 8, 4)                     # Friday, the division pulls and the projection is due
EXPORT_RUN = dt.datetime(2028, 8, 4, 9, 20)     # local Arizona time (MST, UTC-7 all year)
ELECTION_2028 = dt.date(2028, 11, 7)
INSTRUCTION_DATE = dt.date(2027, 11, 18)        # the recorders' current verification instruction
OLD_CODES_DATE = dt.date(2019, 4, 15)           # Navajo County's own disposition code list
PRIOR_MEASURE = "I-04-2024"
PRIOR_ORDERED = dt.date(2024, 7, 12)
PRIOR_OPENED = dt.date(2024, 7, 15)
PRIOR_CLOSEOUT = dt.date(2024, 8, 23)
PRIOR_CERTIFIED = dt.date(2024, 8, 29)
PRIOR_LINES = 403_920
PRIOR_DAYS = 30
PRIOR_STAFF = 14
PRIOR_REQUIRED = 372_366          # fifteen per cent of the 2,482,440 votes cast for Governor in 2022
PRIOR_GOV_VOTES = 2_482_440
FULL_COUNT_START = dt.date(2028, 8, 7)    # Monday, the first examination day a full count could open on
CERTIFY_BY = dt.date(2028, 9, 8)          # the office certifies the measures for the 2028 ballot

MST = dt.timezone(dt.timedelta(hours=-7))       # Arizona does not observe daylight saving

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September",
               "October", "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
UMON3 = ["", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# ------------------------------------------------------------------------------------------------- statute
SHEETS = 44_120                                 # petition sheets receipted
SHEETS_STRUCK = 240                             # sheets two firms had already filed, struck at receipt
SHEETS_PRESENTED = SHEETS + SHEETS_STRUCK       # what the committee handed over
LINES_PER_SHEET = 15                            # the signature lines an Arizona petition sheet carries
LINES_FILED = 540_000                           # signature lines filed, the office's own count on receipt
SAMPLE_DIVISOR = 20                             # the statutory five per cent
SAMPLE_LINES = LINES_FILED // SAMPLE_DIVISOR    # 27,000
P_LINE = 1.0 / SAMPLE_DIVISOR                   # 0.05
REQUIRED = math.ceil(GOV_VOTES_2026 * 0.15)     # 384,924
BAND_LO = int(round(REQUIRED * 0.95))           # 365,678
BAND_HI = int(round(REQUIRED * 1.05))           # 404,170
BIN = 5_000                                     # the asking sentence's rounding on the graded figure

# ------------------------------------------------------------------------------------------------- counties
COUNTIES = [
    ("01", "Apache", 0.0085), ("02", "Cochise", 0.0185), ("03", "Coconino", 0.0200),
    ("04", "Gila", 0.0095), ("05", "Graham", 0.0050), ("06", "Greenlee", 0.0015),
    ("07", "La Paz", 0.0035), ("08", "Maricopa", 0.6180), ("09", "Mohave", 0.0300),
    ("10", "Navajo", 0.0135), ("11", "Pima", 0.1480), ("12", "Pinal", 0.0580),
    ("13", "Santa Cruz", 0.0055), ("14", "Yavapai", 0.0400), ("15", "Yuma", 0.0205),
]
COUNTY_CODES = [c for c, _, _ in COUNTIES]
COUNTY_NAME = {c: n for c, n, _ in COUNTIES}
OLD_CODE_COUNTY = "10"          # Navajo, whose recorder still files on its own 2019 disposition codes
DMY_COUNTY = "09"               # Mohave, whose return carries day-first signature dates

# ------------------------------------------------------------------------------------------------- firms
FIRMS = [
    ("SPS", "Sonoran Petition Services LLC", 0.3950, "C-2027-0114"),
    ("CSS", "Copper State Signature Group LLC", 0.2720, "C-2027-0186"),
    ("VFO", "Verde Petition Operations Inc", 0.1980, "C-2027-0203"),
    ("MCO", "Mesquite Civic Outreach LLC", 0.1350, "C-2027-0247"),
]
FIRM_NAME = {k: n for k, n, _, _ in FIRMS}
FIRM_RENAMED = "CSS"
FIRM_NEW_NAME = "Copper State Civic Services LLC"
FIRM_RENAME_DATE = dt.date(2028, 4, 3)

# ------------------------------------------------------------------------------------------------- codes
# The current disposition set, the recorders' 2027 verification instruction. One disposition per sampled
# signature line, applied in the instruction's order.
CODES = [
    ("V", "signature counted"),
    ("NR", "signer not registered"),
    ("CA", "registration cancelled before the date signed"),
    ("AD", "residence address does not match the registration record"),
    ("SG", "signature does not match the registration record"),
    ("NC", "signer not registered in the county shown"),
    ("NQ", "signer is not a qualified elector"),
    ("DU", "signature of a signer already counted on this petition"),
    ("IL", "line incomplete or illegible"),
    ("MD", "date missing or outside the circulation period"),
    ("WS", "signature struck through by the signer"),
]
CODE_KEYS = [c for c, _ in CODES]
CODE_TEXT = {c: t for c, t in CODES}
SINGLE_CODES = ["NR", "CA", "AD", "SG", "NC", "NQ", "IL", "MD", "WS"]   # one signature, one ground
LINE_CODES = ["IL", "MD", "WS"]                                         # properties of the line
REG_CODES = ["NR", "CA", "AD", "SG", "NC", "NQ"]                        # properties of the signer

# Navajo County's own 2019 code list. 02 folds "not registered" and "cancelled", both of which are single
# signature grounds, so no reading of the fold moves any projected class total or the call.
OLD_CODES = [
    ("01", "counted"), ("02", "not registered or registration cancelled"),
    ("03", "address does not match"), ("04", "signature does not match"),
    ("05", "not registered in county shown"), ("06", "not a qualified elector"),
    ("07", "duplicate of a signature already counted"), ("08", "line incomplete or illegible"),
    ("09", "date missing or outside circulation"), ("10", "struck through by signer"),
]
OLD_TO_NEW = {"01": ["V"], "02": ["NR", "CA"], "03": ["AD"], "04": ["SG"], "05": ["NC"], "06": ["NQ"],
              "07": ["DU"], "08": ["IL"], "09": ["MD"], "10": ["WS"]}

# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys, seed=None):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    s = SEED if seed is None else seed
    h = hashlib.blake2b(("%d|" % s + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12, alphabet="0123456789abcdef", seed=None):
    s = SEED if seed is None else seed
    h = hashlib.blake2b(("%d|" % s + "|".join(str(k) for k in keys)).encode(), digest_size=32).digest()
    return "".join(alphabet[b % len(alphabet)] for b in h[:n])


# ------------------------------------------------------------------------------------------------- writing
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


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def round_to(x, step):
    return int(step * math.floor(x / step + 0.5))


def cell_centre_distance(x, step=BIN):
    """Distance from x to the centre of the step-wide cell it prints into."""
    return abs(x - round_to(x, step))


def bin_edge(x, step=BIN):
    """Distance from x to the nearest rounding edge of the cell it prints into."""
    return step / 2.0 - cell_centre_distance(x, step)


def band(valid):
    """The statutory disposition the projection files: strict above 105 per cent, strict below 95."""
    if valid < BAND_LO:
        return "insufficient"
    if valid > BAND_HI:
        return "sufficient"
    return "full count"


def iso(d):
    return d.strftime("%Y-%m-%d")


def us_date(d):
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)


def long_date(d):
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)


def utc_stamp(local):
    """An Arizona local naive datetime as the UTC timestamp the office's systems write."""
    return (local.replace(tzinfo=MST)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def months_of_window():
    out, y, m = [], WINDOW_OPEN.year, WINDOW_OPEN.month
    while (y, m) <= (WINDOW_CLOSE.year, WINDOW_CLOSE.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


WINDOW_MONTHS = months_of_window()
WINDOW_DAYS = (WINDOW_CLOSE - WINDOW_OPEN).days + 1
