"""World constants for task276: the Shires Transport Board's 2027 level crossing replacement choice."""
import datetime as dt

SEED = "task276-architecture-2"
D0, D1 = dt.date(2025, 9, 1), dt.date(2026, 8, 31)
EXPORT = dt.date(2026, 9, 14)
BOARD = "Shires Transport Board"
RAIL = "Route Asset Management, Shires route"
HIGHWAYS = "Shires Highways Partnership"
LEAD, PM = "Andrew Stevens", "Gareth Davis"

# BST on these dates' 05:00 to 21:00 local window (both clock changes fall on Sundays before 05:00)
BST_ENDS, BST_STARTS = dt.date(2025, 10, 26), dt.date(2026, 3, 29)

BANK_HOLIDAYS = [dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3),
                 dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31)]

# (term, start, half term first day, half term last day, end)
TERMS = {
    "Northshire": [("Autumn 2025", "2025-09-03", "2025-10-27", "2025-10-31", "2025-12-19"),
                   ("Spring 2026", "2026-01-05", "2026-02-16", "2026-02-20", "2026-03-27"),
                   ("Summer 2026", "2026-04-13", "2026-05-25", "2026-05-29", "2026-07-22")],
    "Southshire": [("Autumn 2025", "2025-09-04", "2025-10-27", "2025-10-31", "2025-12-19"),
                   ("Spring 2026", "2026-01-05", "2026-02-16", "2026-02-20", "2026-03-27"),
                   ("Summer 2026", "2026-04-14", "2026-05-25", "2026-05-29", "2026-07-21")],
    "Eastshire": [("Autumn 2025", "2025-09-03", "2025-10-20", "2025-10-24", "2025-12-19"),
                  ("Spring 2026", "2026-01-05", "2026-02-09", "2026-02-13", "2026-03-27"),
                  ("Summer 2026", "2026-04-13", "2026-05-25", "2026-05-29", "2026-07-22")],
    "Westshire": [("Autumn 2025", "2025-09-02", "2025-10-27", "2025-10-31", "2025-12-18"),
                  ("Spring 2026", "2026-01-06", "2026-02-16", "2026-02-20", "2026-04-02"),
                  ("Summer 2026", "2026-04-20", "2026-05-25", "2026-05-29", "2026-07-21")],
}

# the shortlist; q = peak-hour flow per direction (dir 0, dir 1), closures per hour by band, closure length (mean, sd)
CROSSINGS = {
    "A": dict(name="Station Road", elr="NSB", miles=12, chains=47, county="Northshire", type="MCB",
              grid=(438214, 361902), axis="NS", dirs=("northbound", "southbound"), lanes=1, q=(440, 400),
              rate={"early": 2, "peak": 4, "day": 3, "pm": 4, "late": 2.5}, dm=294, ds=55, hgv=(0.054, 0.058),
              asset="LXB/2271", speed=30),
    "B": dict(name="Mill Lane", elr="WVL", miles=31, chains=8, county="Westshire", type="MCB-CCTV",
              grid=(401876, 352130), axis="EW", dirs=("westbound", "eastbound"), lanes=1, q=(434, 394),
              rate={"early": 2, "peak": 4, "day": 3, "pm": 4, "late": 2}, dm=250, ds=50, hgv=(0.071, 0.074),
              asset="LXB/2285", speed=30),
    "C": dict(name="Common Road", elr="WVL", miles=26, chains=55, county="Westshire", type="AHB",
              grid=(406522, 349870), axis="EW", dirs=("westbound", "eastbound"), lanes=2, q=(700, 650),
              rate={"early": 4, "peak": 6, "day": 5, "pm": 6, "late": 4}, dm=98, ds=15, hgv=(0.061, 0.060),
              asset="LXB/2264", speed=40),
    "D": dict(name="Long Drove", elr="EFL", miles=7, chains=71, county="Eastshire", type="MCB-CCTV",
              grid=(471340, 339212), axis="NS", dirs=("northbound", "southbound"), lanes=1, q=(500, 430),
              rate={"early": 2, "peak": 3, "day": 2, "pm": 3, "late": 2}, dm=240, ds=55, hgv=(0.083, 0.081),
              asset="LXB/2290", speed=40, renewed=("2026-02-10", "LXB/5203")),
    "E": dict(name="Church Lane", elr="SCL", miles=18, chains=23, county="Southshire", type="AHB",
              grid=(452107, 301884), axis="EW", dirs=("westbound", "eastbound"), lanes=1, q=(520, 560),
              rate={"early": 3, "peak": 5, "day": 4, "pm": 5, "late": 3}, dm=115, ds=20, hgv=(0.047, 0.049),
              asset="LXB/2302", speed=30),
    "F": dict(name="Moor Road", elr="NSB", miles=16, chains=2, county="Northshire", type="MCB-CCTV",
              grid=(434980, 366415), axis="NS", dirs=("northbound", "southbound"), lanes=1, q=(520, 470),
              rate={"early": 2, "peak": 4, "day": 3, "pm": 4, "late": 2}, dm=205, ds=45, hgv=(0.066, 0.068),
              asset="LXB/2278", speed=40),
}
ORDER = ["A", "B", "C", "D", "E", "F"]

# crossings on the same lines that are not shortlisted (register rows only)
OTHER_CROSSINGS = [
    ("NSB", 9, 66, "Hall Farm", "UWC-T", "Northshire", (440630, 357118), "LXB/2269", 50, 18, 34, "C8"),
    ("WVL", 28, 40, "Kiln Lane", "AHB", "Westshire", (404910, 350688), "LXB/2266", 60, 46, 1630, "D5"),
    ("EFL", 11, 12, "Fen Bank", "AOCL+B", "Eastshire", (474018, 343377), "LXB/2294", 45, 22, 410, "C6"),
    ("SCL", 21, 48, "Sandpit Lane", "MCB", "Southshire", (455240, 303016), "LXB/2305", 60, 61, 2240, "D3"),
]

# Mill Lane's westbound side: the single-track river bridge and its shuttle signals
BRIDGE = dict(stop_gap_m=42.0, span_m=28.0, site="SS 2207", cycle=100, wb_green=32, ig1=10, eb_green=48, ig2=10,
              sat=1800, plan_start="06:00:00", plan="06:00-11:00")
SAT = 1800
VEH_LEN = 5.75
COUNT_SITE_M = 300

# heavy-vehicle column: the older counter writes a whole-number share of the interval's vehicles
QT40_ALL_YEAR = {"C": 1, "D": 0, "F": 0}            # crossing: approach index with the older counter all year
QT40_SWITCHED = {"C": 0, "E": 1}                    # changed to the newer counter on SWITCH_DATE
SWITCH_DATE = "2026-04-08"

# stream salts per crossing (closures, faults, heavy-vehicle draws), chosen so that every graded figure sits clear of
# its rounding edge
SALTS = {"A": dict(cl=2, flt=4, hgv=0), "B": dict(cl=2, flt=4, hgv=3), "C": dict(cl=1, flt=2, hgv=4),
         "D": dict(cl=1, flt=2, hgv=1), "E": dict(cl=1, flt=5, hgv=1), "F": dict(cl=1, flt=0, hgv=4)}
