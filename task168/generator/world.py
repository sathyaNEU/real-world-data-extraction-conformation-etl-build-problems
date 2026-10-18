"""The world of task168: an Italian domestic airline's summer network, its fleet and the demand behind it.

Everything here is a constant the simulation reads. Nothing is tuned after outcomes: the seed and these
parameters were fixed on paper (DESIGN_NOTE ## Draw and ## Ladder) before any pack was cut.
"""
import datetime as dt

SEED = 168

# ------------------------------------------------------------------ seasons (IATA summer)
def iata_summer(year):
    """Last Sunday of March to the Saturday before the last Sunday of October."""
    def last_sunday(y, m):
        d = dt.date(y, m + 1, 1) - dt.timedelta(days=1)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d
    a = last_sunday(year, 3)
    b = last_sunday(year, 10) - dt.timedelta(days=1)
    return a, b


SEASONS = {s: iata_summer(y) for s, y in (("S24", 2024), ("S25", 2025), ("S26", 2026))}
# S24 31 Mar 2024 - 26 Oct 2024, S25 30 Mar 2025 - 25 Oct 2025, S26 29 Mar 2026 - 24 Oct 2026: 210 days each.
ASOF = dt.date(2025, 12, 12)
RM_PULL = dt.date(2025, 12, 1)

# Easter Sundays and fixed holidays that move demand
EASTER = {2024: dt.date(2024, 3, 31), 2025: dt.date(2025, 4, 20), 2026: dt.date(2026, 4, 5)}
FIXED_HOLIDAYS = [(4, 25), (5, 1), (6, 2), (8, 15)]

# ------------------------------------------------------------------ fleet
SEATS = {"319": 144, "320": 180, "32N": 186, "321": 220, "32Q": 232}
TYPE_NAME = {"319": "A319", "320": "A320", "32N": "A320neo", "321": "A321", "32Q": "A321neo"}

# ------------------------------------------------------------------ booking curve
# Share of a departure's final bookings on hand t days before departure: exp(-(t / tau)^BETA).
# tau is the departure's booking-lead scale, a smooth function of the departure date: spring and autumn
# departures carry business and visiting-friends traffic that books a few weeks out, summer departures carry
# families who book months ahead. Anchored on the 15th of each month.
TAU = {2: 28.0, 3: 29.0, 4: 31.0, 5: 40.0, 6: 62.0, 7: 74.0, 8: 77.0, 9: 64.0, 10: 40.0, 11: 31.0}
BETA = 1.25
SIG_TAU = 0.04          # departure-level spread of the build scale
DOW_TAU = [1.0] * 7    # the build scale does not move with the weekday on these routes
HORIZON = 330           # first day the schedule is on sale, days before departure

# DCP sets of the two revenue management systems
DCP_NEW = ([330, 300, 270, 240, 210, 180, 160, 140] + list(range(120, 60, -5)) + list(range(60, 14, -2))
           + list(range(14, -1, -1)))
DCP_OLD = [330, 270, 210, 180, 150, 120, 90, 75, 60, 45, 35, 28, 21, 14, 10, 7, 3, 1, 0]

# ------------------------------------------------------------------ demand shape
MONTH_BASE = {2: 0.92, 3: 0.92, 4: 0.93, 5: 0.96, 6: 1.02, 7: 1.08, 8: 1.12, 9: 1.02, 10: 0.94, 11: 0.92}
DOW = [0.98, 0.95, 0.96, 1.00, 1.05, 0.99, 1.07]          # Monday .. Sunday
SIG_D = 0.07           # departure-level demand noise beyond Poisson
GROWTH = {"S24": 1.000, "S25": 1.000, "S26": 1.000}   # flat market (the 2026 budget's outlook)
DIRECTION = {True: {5: 1.0, 6: 1.0, 7: 1.03, 8: 1.00, 9: 0.97, 10: 1.0},
             False: {5: 1.0, 6: 1.0, 7: 0.97, 8: 1.01, 9: 1.03, 10: 1.0}}


def _smooth(anchors):
    """A smooth function of the date through values anchored on the 15th of each month (monotone cubic)."""
    from scipy.interpolate import PchipInterpolator
    cache = {}

    def f(d):
        y = d.year
        if y not in cache:
            xs = [(dt.date(y, m, 15) - dt.date(y, 1, 1)).days for m in sorted(anchors)]
            cache[y] = PchipInterpolator(xs, [anchors[m] for m in sorted(anchors)], extrapolate=True)
        return float(cache[y]((d - dt.date(y, 1, 1)).days))
    return f


tau_of = _smooth(TAU)            # booking-lead scale of a departure on this date, days
base_of = _smooth(MONTH_BASE)    # seasonal demand level of a departure on this date
direction_of = {True: _smooth(DIRECTION[True]), False: _smooth(DIRECTION[False])}

# ------------------------------------------------------------------ routes
# (origin, destination) with the base first. freq = departures per day each way.
# The nine Linate routes that change gauge for summer 2026.
TARGETS = [
    # station, freq, df (season-mean demand over 144 seats), seasonal amplitude, no-show share
    ("CTA", 3, 1.169, 1.05, 0.031),
    ("PMO", 3, 1.154, 1.10, 0.029),
    ("NAP", 2, 1.129, 0.80, 0.036),
    ("BRI", 2, 1.144, 0.90, 0.033),
    ("BDS", 2, 1.164, 1.00, 0.030),
    ("SUF", 2, 1.139, 0.95, 0.028),
    ("REG", 1, 1.189, 0.95, 0.027),
    ("CAG", 2, 1.154, 1.20, 0.032),
    ("TPS", 1, 1.184, 1.25, 0.026),
]
TARGET_SWITCH = {"BDS": dt.date(2026, 6, 1), "SUF": dt.date(2026, 6, 1)}   # A321neo from this date

# Routes that changed gauge for summer 2025 (S24 old gauge -> S25 new gauge).
PAST = [
    # base, station, freq, S24 type, S25 type, df over S24 seats, amplitude, no-show
    ("TRN", "CTA", 2, "319", "32N", 1.44, 1.05, 0.030),
    ("TRN", "PMO", 2, "320", "321", 1.19, 1.10, 0.031),
    ("TRN", "NAP", 2, "319", "32N", 1.17, 0.85, 0.035),
    ("VRN", "CTA", 2, "320", "321", 1.46, 1.05, 0.029),
    ("VRN", "PMO", 2, "319", "32N", 1.50, 1.10, 0.030),
    ("VRN", "NAP", 1, "319", "32N", 1.21, 0.85, 0.034),
    ("VCE", "CTA", 2, "320", "321", 1.16, 1.05, 0.030),
    ("VCE", "PMO", 2, "319", "32N", 1.53, 1.10, 0.028),
    ("VCE", "NAP", 2, "320", "321", 1.39, 0.85, 0.036),
    ("VCE", "BRI", 1, "319", "32N", 1.18, 0.90, 0.032),
    ("BLQ", "CTA", 2, "319", "32N", 1.48, 1.05, 0.031),
    ("BLQ", "PMO", 2, "320", "321", 1.22, 1.10, 0.029),
    ("BLQ", "CAG", 1, "319", "32N", 1.43, 1.20, 0.030),
    ("LIN", "AHO", 1, "319", "32N", 1.20, 1.30, 0.027),
    ("LIN", "CRV", 1, "319", "32N", 1.41, 0.90, 0.026),
    ("LIN", "PSR", 1, "319", "32N", 1.15, 0.75, 0.033),
]

# Routes that kept their gauge and seldom sell out (the network the build curves are read from).
REF = [
    # base, station, freq, type (all seasons), df over seats, amplitude, no-show
    ("TRN", "BRI", 1, "320", 0.86, 0.90, 0.032),
    ("TRN", "BDS", 1, "319", 0.82, 1.00, 0.030),
    ("TRN", "SUF", 1, "319", 0.79, 0.95, 0.029),
    ("TRN", "CAG", 1, "320", 0.84, 1.20, 0.031),
    ("VRN", "BRI", 1, "319", 0.88, 0.90, 0.033),
    ("VRN", "SUF", 1, "319", 0.81, 0.95, 0.028),
    ("VRN", "REG", 1, "319", 0.77, 0.95, 0.027),
    ("VRN", "CAG", 1, "320", 0.83, 1.20, 0.030),
    ("VRN", "OLB", 1, "319", 0.74, 1.35, 0.029),
    ("VCE", "BDS", 1, "319", 0.85, 1.00, 0.031),
    ("VCE", "SUF", 1, "319", 0.80, 0.95, 0.029),
    ("VCE", "REG", 1, "319", 0.76, 0.95, 0.028),
    ("VCE", "CAG", 1, "32N", 0.87, 1.20, 0.030),
    ("VCE", "TPS", 1, "319", 0.78, 1.25, 0.027),
    ("BLQ", "BRI", 2, "320", 0.83, 0.90, 0.034),
    ("BLQ", "SUF", 1, "319", 0.85, 0.95, 0.030),
    ("BLQ", "REG", 1, "319", 0.80, 0.95, 0.028),
    ("BLQ", "TPS", 1, "319", 0.75, 1.25, 0.026),
    ("LIN", "CIY", 1, "320", 0.82, 1.05, 0.030),
    ("LIN", "OLB", 1, "32N", 0.79, 1.40, 0.031),
    ("TRN", "OLB", 1, "319", 0.72, 1.40, 0.028),
    ("BLQ", "OLB", 1, "319", 0.73, 1.40, 0.029),
]

# Departure times (local) for the first, second and third daily rotation, base outbound and return.
OUT_TIMES = {1: ["07:05"], 2: ["06:50", "18:40"], 3: ["06:40", "12:55", "19:20"]}
RET_TIMES = {1: ["09:35"], 2: ["09:20", "21:15"], 3: ["09:10", "15:25", "21:50"]}
TOD = {1: [1.00], 2: [0.99, 1.01], 3: [0.99, 1.01, 1.00]}

DISTANCE_KM = {
    ("LIN", "CTA"): 942, ("LIN", "PMO"): 886, ("LIN", "NAP"): 657, ("LIN", "BRI"): 762, ("LIN", "BDS"): 862,
    ("LIN", "SUF"): 876, ("LIN", "REG"): 987, ("LIN", "CAG"): 696, ("LIN", "TPS"): 877, ("LIN", "AHO"): 578,
    ("LIN", "CRV"): 967, ("LIN", "PSR"): 538, ("LIN", "CIY"): 997, ("LIN", "OLB"): 470,
    ("TRN", "CTA"): 1035, ("TRN", "PMO"): 957, ("TRN", "NAP"): 760, ("TRN", "BRI"): 889, ("TRN", "BDS"): 995,
    ("TRN", "SUF"): 977, ("TRN", "CAG"): 696, ("TRN", "OLB"): 487,
    ("VRN", "CTA"): 914, ("VRN", "PMO"): 873, ("VRN", "NAP"): 626, ("VRN", "BRI"): 676, ("VRN", "SUF"): 830,
    ("VRN", "REG"): 945, ("VRN", "CAG"): 754, ("VRN", "OLB"): 538,
    ("VCE", "CTA"): 887, ("VCE", "PMO"): 867, ("VCE", "NAP"): 596, ("VCE", "BRI"): 610, ("VCE", "BDS"): 705,
    ("VCE", "SUF"): 818, ("VCE", "REG"): 925, ("VCE", "CAG"): 809, ("VCE", "TPS"): 905,
    ("BLQ", "CTA"): 776, ("BLQ", "PMO"): 730, ("BLQ", "CAG"): 637, ("BLQ", "BRI"): 545, ("BLQ", "SUF"): 664,
    ("BLQ", "REG"): 781, ("BLQ", "TPS"): 766, ("BLQ", "OLB"): 449,
}
