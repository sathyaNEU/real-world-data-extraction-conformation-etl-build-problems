"""Fixed parameters of the Matiri Forest Products world (task133, architecture 4). Every script reads them from here."""
import datetime as dt

SEED = 133041

FY26 = (dt.date(2025, 7, 1), dt.date(2026, 6, 30))       # the recorded year
FY28 = (dt.date(2027, 7, 1), dt.date(2028, 6, 30))       # the forecast year
ROUTE_OPENS = dt.date(2027, 7, 1)
EXPORT_DATE = dt.datetime(2026, 10, 20, 8, 40, 0)        # every mtime in target/
OLD_GROSS = 44.0
NEW_GROSS = 50.0

# Export grades: length (m), mean density (green tonnes per JAS m3), mean JAS m3 per piece
GRADES = {
    "A":   dict(name="A grade",   length=12.1, density=1.000, piece=0.62),
    "P":   dict(name="Pruned",    length=5.9,  density=0.985, piece=0.71),
    "K":   dict(name="K grade",   length=5.9,  density=1.040, piece=0.34),
    "KI":  dict(name="KI grade",  length=3.9,  density=1.085, piece=0.19),
    "KIS": dict(name="KIS grade", length=3.9,  density=1.130, piece=0.11),
}
GRADE_ORDER = ["A", "P", "K", "KI", "KIS"]
LENGTH_CLASS = {12.1: "12.1 m", 5.9: "5.9 m", 3.9: "3.9 m"}

# Forests: annual export tonnes (FY2026 recorded), grade mix by tonnes, one-way km to the port
FORESTS = {
    "PKT": dict(name="Puketitiri Forest", tonnes=205000, km=74, mix={"A": .22, "P": .10, "K": .26, "KI": .24, "KIS": .18}),
    "TPH": dict(name="Te Pohue Forest",   tonnes=168000, km=48, mix={"A": .18, "P": .06, "K": .30, "KI": .26, "KIS": .20}),
    "ESK": dict(name="Esk Forest",        tonnes=142000, km=31, mix={"A": .26, "P": .14, "K": .24, "KI": .20, "KIS": .16}),
    "WTD": dict(name="Waitara Downs Forest", tonnes=131000, km=92, mix={"A": .14, "P": .04, "K": .28, "KI": .30, "KIS": .24}),
    "GLR": dict(name="Glenross Forest",   tonnes=118000, km=57, mix={"A": .20, "P": .08, "K": .27, "KI": .25, "KIS": .20}),
}

# The FY2028 harvest plan's export tonnes by forest (the plan's own figures; the grade split follows each forest's
# compartments). PLAN_SCALE sets the plan's size against FY2026.
PLAN_SCALE = 1.06
PLAN_MIX_SHIFT = {"A": -0.02, "P": 0.0, "K": 0.0, "KI": 0.01, "KIS": 0.01}
# the plan's compartment yields by grade against the FY2026 mix (set by tune.py so each graded figure sits mid-bin)
PLAN_GRADE_ADJ = {"A": 0.99928, "P": 1.00297, "K": 0.99934, "KI": 0.99775, "KIS": 0.99819}

CARRIERS = {
    "RLC": "Ruahine Log Cartage Ltd",
    "KRH": "Kereru Haulage Ltd",
    "TTT": "Tutaekuri Transport Ltd",
    "WHT": "Wilson & Heke Trucking Ltd",
    "KNC": "Kinross Contracting Ltd",
    "PLH": "Patoka Logging Haulage Ltd",
}
# subcontractor -> the head contractor that bills its loads
BILLED_BY = {"WHT": "RLC", "KNC": "KRH", "PLH": "TTT"}

MILLS = {"MSM": "Mohaka Sawmills", "AHT": "Ahuriri Timber Processors", "HBL": "Heretaunga Box and Lumber"}

# FY2026 cartage rate card (NZD per tonne = base + per-km rate x one-way km)
RATE_BASE = 4.21
RATE_PER_KM = 0.118
# FY2026 domestic mill deliveries (tonnes contracted)
MILL_TONNES = {"MSM": 51800, "AHT": 38000, "HBL": 21000}
