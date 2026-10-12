"""The corridor, the calendars and the trip constructions: the shuttle's sixteen northbound segments from the
Cedar Grove on-ramp to the Brook Street stop, the operator's southbound deadhead route, the I-264 ramps and the
other corridor segments in the vendor's export, under the 2025 and 2026 network releases."""
import datetime as dt

import numpy as np

# the export's epochs: 05:30 to 09:25 local time, five minutes each
E0 = 5 * 60 + 30
NE = 48
EPOCHS = E0 + 5 * np.arange(NE)

START, END = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
RELEASE_2026 = dt.date(2026, 4, 1)          # the vendor's 2026 network release takes effect
HOLIDAYS = [(dt.date(2025, 11, 27), "Thanksgiving Day"), (dt.date(2025, 11, 28), "Day after Thanksgiving"),
            (dt.date(2025, 12, 25), "Christmas Day"), (dt.date(2026, 1, 1), "New Year's Day"),
            (dt.date(2026, 1, 19), "Martin Luther King Jr. Day"), (dt.date(2026, 5, 25), "Memorial Day"),
            (dt.date(2026, 6, 19), "Juneteenth"), (dt.date(2026, 7, 3), "Independence Day (observed)"),
            (dt.date(2026, 9, 7), "Labor Day")]
HOLIDAYS_2027 = [(dt.date(2027, 1, 1), "New Year's Day"), (dt.date(2027, 1, 18), "Martin Luther King Jr. Day"),
                 (dt.date(2027, 5, 31), "Memorial Day"), (dt.date(2027, 6, 18), "Juneteenth (observed)"),
                 (dt.date(2027, 7, 5), "Independence Day (observed)"), (dt.date(2027, 9, 6), "Labor Day"),
                 (dt.date(2027, 11, 25), "Thanksgiving Day"), (dt.date(2027, 11, 26), "Day after Thanksgiving"),
                 (dt.date(2027, 12, 24), "Christmas Day (observed)")]

LOT_LEG, STOP_LEG = 4.0, 3.0                # minutes: boarding bay to on-ramp; last segment to the stop's bay
SB_LEG_IN, SB_LEG_OUT = 4.0, 6.0            # minutes: stop to the southbound on-ramp; Exit 128 to the yard
BAR_TIME = 8 * 60                           # 8:00 a.m.
DEPARTURES = [6 * 60 + 30 + 5 * i for i in range(11)]       # 6:30 to 7:20


def days():
    out, d = [], START
    while d <= END:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def working(d, hol=None):
    hol = {h for h, _ in (hol or HOLIDAYS)}
    return d.weekday() < 5 and d not in hol


def working_days_2027():
    hol = {h for h, _ in HOLIDAYS_2027}
    d, n = dt.date(2027, 1, 1), 0
    while d.year == 2027:
        n += d.weekday() < 5 and d not in hol
        d += dt.timedelta(days=1)
    return n


def school_day(d):
    """In session for the county's public schools (which set the morning peak's size)."""
    if d < dt.date(2025, 8, 13) or dt.date(2026, 5, 22) < d < dt.date(2026, 8, 12):
        return False
    if dt.date(2025, 12, 22) <= d <= dt.date(2026, 1, 2) or dt.date(2026, 3, 30) <= d <= dt.date(2026, 4, 3):
        return False
    if dt.date(2025, 10, 6) <= d <= dt.date(2025, 10, 10):          # fall break
        return False
    return True


# ------------------------------------------------------------------------------------------------- the network
# (code, road, direction, description, miles, free-flow seconds, functional class)
ROUTE = [
    ("121P04501", "I-65", "NORTHBOUND", "KY-480/Cedar Grove Rd (Exit 121) to KY-1526/Brooks Rd (Exit 125)", 3.71, 205, "Interstate"),
    ("121P04502", "I-65", "NORTHBOUND", "KY-1526/Brooks Rd (Exit 125) on-ramp merge", 0.66, 37, "Interstate"),
    ("121P04503", "I-65", "NORTHBOUND", "Brooks Rd (Exit 125) to KY-1065/Outer Loop (Exit 127)", 1.62, 90, "Interstate"),
    ("121P04504", "I-65", "NORTHBOUND", "Outer Loop (Exit 127) interchange", 0.48, 27, "Interstate"),
    ("121P04505", "I-65", "NORTHBOUND", "Outer Loop (Exit 127) to Fern Valley Rd (Exit 128)", 1.12, 62, "Interstate"),
    ("121P04506", "I-65", "NORTHBOUND", "Fern Valley Rd (Exit 128) interchange", 0.55, 31, "Interstate"),
    ("121P04507", "I-65", "NORTHBOUND", "Fern Valley Rd (Exit 128) to Grade Ln (Exit 130)", 1.38, 77, "Interstate"),
    ("121P04508", "I-65", "NORTHBOUND", "Grade Ln (Exit 130) interchange", 0.42, 24, "Interstate"),
    ("121P04509", "I-65", "NORTHBOUND", "Grade Ln (Exit 130) to I-264 (Exit 131)", 0.92, 51, "Interstate"),
    ("121P04510", "I-65", "NORTHBOUND", "I-264 interchange, collector-distributor split", 0.64, 36, "Interstate"),
    ("121P04511", "I-65", "NORTHBOUND", "I-264 interchange, ramp merge from I-264 E and W", 0.58, 32, "Interstate"),
    ("121P04512", "I-65", "NORTHBOUND", "I-264 merge to Crittenden Dr (Exit 132)", 1.04, 64, "Interstate"),
    ("121P04513", "I-65", "NORTHBOUND", "Crittenden Dr (Exit 132) to Eastern Pkwy (Exit 133)", 1.31, 90, "Interstate"),
    ("121P04514", "S Brook St", "NORTHBOUND", "I-65 Exit 133 ramp terminal to E Kentucky St", 0.41, 75, "Principal Arterial"),
    ("121P04515", "S Brook St", "NORTHBOUND", "E Kentucky St to E Breckinridge St", 0.47, 95, "Principal Arterial"),
    ("121P04516", "S Brook St", "NORTHBOUND", "E Breckinridge St to E Chestnut St", 0.52, 110, "Principal Arterial"),
]
QUEUE_SEGS = [5, 6, 7, 8, 9]       # spillback upstream of the merge (index into ROUTE)
BOTTLENECK = 10                    # the merge itself
ARTERIAL = [13, 14, 15]

# the operator's deadhead route, as it set it up in October 2025 (2025 release codes)
DEADHEAD = [
    ("121N04630", "I-65", "SOUTHBOUND", "Broadway on-ramp to Eastern Pkwy (Exit 133)", 1.36, 76, "Interstate"),
    ("121N04631", "I-65", "SOUTHBOUND", "Eastern Pkwy (Exit 133) to Crittenden Dr (Exit 132)", 1.29, 72, "Interstate"),
    ("121N04632", "I-65", "SOUTHBOUND", "Crittenden Dr (Exit 132) interchange", 0.44, 25, "Interstate"),
    ("121N04633", "I-65", "SOUTHBOUND", "Crittenden Dr (Exit 132) to I-264 (Exit 131)", 0.97, 54, "Interstate"),
    ("121N04634", "I-65", "SOUTHBOUND", "I-264 interchange, ramp diverge to I-264 E and W", 0.61, 34, "Interstate"),
    ("121N04637", "I-65", "SOUTHBOUND", "I-264 (Exit 131) to Grade Ln (Exit 130)", 1.21, 75, "Interstate"),
    ("121N04638", "I-65", "SOUTHBOUND", "Grade Ln (Exit 130) interchange", 0.43, 24, "Interstate"),
    ("121N04639", "I-65", "SOUTHBOUND", "Grade Ln (Exit 130) to Fern Valley Rd (Exit 128)", 1.37, 76, "Interstate"),
    ("121N04640", "I-65", "SOUTHBOUND", "Fern Valley Rd (Exit 128) off-ramp diverge", 0.38, 22, "Interstate"),
]
T1_INDEX = 5                       # the deadhead code the 2026 release re-cuts and reissues
T1_OLD = "121N04637"
T1_NEW = [("121N05212", "I-65", "SOUTHBOUND", "I-264 (Exit 131) to Standiford Field connector", 0.66, 41, "Interstate"),
          ("121N05213", "I-65", "SOUTHBOUND", "Standiford Field connector to Grade Ln (Exit 130)", 0.55, 34, "Interstate")]
# the I-264 westbound collector ramp to I-65: 121N04702 in the 2025 release, 121N04637 in the 2026 release
RAMP_2025, RAMP_2026 = "121N04702", "121N04637"
RAMP = ("I-264", "WESTBOUND", "I-264 W collector-distributor ramp to I-65 S", 0.52, 45, "Interstate")
# other corridor segments in the export (never on either route)
OTHER = [
    ("121P04517", "I-65", "NORTHBOUND", "Eastern Pkwy (Exit 133) to St Catherine St (Exit 134)", 0.98, 55, "Interstate"),
    ("121P04518", "I-65", "NORTHBOUND", "St Catherine St (Exit 134) to Broadway/Brook St (Exit 135)", 0.71, 41, "Interstate"),
    ("121P04519", "I-65", "NORTHBOUND", "Broadway (Exit 135) to Jefferson St (Exit 136)", 0.86, 50, "Interstate"),
    ("121P04210", "I-264", "EASTBOUND", "Taylor Blvd to I-65", 1.14, 66, "Interstate"),
    ("121N04211", "I-264", "WESTBOUND", "I-65 to Taylor Blvd", 1.17, 67, "Interstate"),
    ("121P04212", "I-264", "EASTBOUND", "I-65 to Poplar Level Rd", 1.42, 81, "Interstate"),
    ("121N04213", "I-264", "WESTBOUND", "Poplar Level Rd to I-65", 1.40, 80, "Interstate"),
    ("121P04801", "KY-480", "EASTBOUND", "Cedar Grove park-and-ride to I-65 (Exit 121)", 0.84, 88, "Minor Arterial"),
]


def codes_for(day):
    """The codes in the export on a given day, each with its segment record, under that day's release."""
    seg = [r for r in ROUTE] + [r for r in OTHER]
    if day < RELEASE_2026:
        seg += DEADHEAD + [(RAMP_2025,) + RAMP]
    else:
        seg += [r for i, r in enumerate(DEADHEAD) if i != T1_INDEX] + T1_NEW + [(RAMP_2026,) + RAMP]
    return seg


ALL_CODES = sorted({r[0] for r in ROUTE + OTHER + DEADHEAD + T1_NEW} | {RAMP_2025, RAMP_2026})


# ----------------------------------------------------------------------------------------- trip constructions
def ix(t):
    """the epoch index containing minute t (t in minutes after midnight), clipped to the export"""
    return np.clip(((np.asarray(t) - E0) // 5).astype(int), 0, NE - 1)


def walk(tt, dep, mode="entry", lot=LOT_LEG, stop=STOP_LEG):
    """Each day's trip leaving at minute `dep`: the lot leg, then each segment at the epoch the shuttle is on it
    (mode entry: the epoch it enters; mid: the epoch of its midpoint; exit: the epoch it leaves; interp: linear
    between epoch centres), then the stop leg. tt: (days, NE, segments) seconds. Returns arrival minutes."""
    D, _, K = tt.shape
    t = np.full(D, dep + lot, float)
    r = np.arange(D)
    for k in range(K):
        if mode == "interp":
            x = (t - E0 - 2.5) / 5.0
            i0 = np.clip(np.floor(x).astype(int), 0, NE - 2)
            w = np.clip(x - i0, 0, 1)
            v = (1 - w) * tt[r, i0, k] + w * tt[r, i0 + 1, k]
        else:
            v = tt[r, ix(t), k]
            if mode in ("mid", "exit"):
                f = 0.5 if mode == "mid" else 1.0
                for _ in range(4):
                    v = tt[r, ix(t + f * v / 60.0), k]
        t = t + v / 60.0
    return t + stop


def at_departure(tt, dep, lot=LOT_LEG, stop=STOP_LEG):
    """The route's travel time for the departure's epoch: every segment read at the epoch the shuttle leaves in."""
    return dep + lot + tt[:, ix(dep), :].sum(1) / 60.0 + stop


def at_midpoint(tt, ff_total, dep, lot=LOT_LEG, stop=STOP_LEG):
    """Every segment read at the epoch of the trip's free-flow midpoint."""
    return dep + lot + tt[:, ix(dep + lot + ff_total / 120.0), :].sum(1) / 60.0 + stop


def profile_walk(prof, dep, lot=LOT_LEG, stop=STOP_LEG):
    return float(walk(prof[None], dep, lot=lot, stop=stop)[0])


def profile_at_departure(prof, dep, lot=LOT_LEG, stop=STOP_LEG):
    return dep + lot + prof[ix(dep)].sum() / 60.0 + stop


def clock(m):
    m = int(round(m))
    return "%d:%02d" % (m // 60, m % 60)
