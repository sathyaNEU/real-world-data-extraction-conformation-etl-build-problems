"""task126 world parameters. One seeded, deterministic docket world; every figure is computed forward from it.

Time is held as proleptic ordinals (datetime.date.toordinal). Months are days / 30.4375 (the charter's divisor).
"""
import datetime as dt

SEED = 126
EXTRACT = dt.date(2026, 9, 30).toordinal()
EXTRACT_2025 = dt.date(2025, 9, 30).toordinal()     # last year's report was cut on this extract
AS_OF = dt.date(2026, 11, 23)
FIRST_FY, LAST_FY, SHIP_FROM_FY = 2003, 2026, 2016
P1_FROM_FY = 2006
M = 30.4375


def fy_bounds(fy):
    return dt.date(fy - 1, 10, 1).toordinal(), dt.date(fy, 9, 30).toordinal()


def fy_of(o):
    d = dt.date.fromordinal(o)
    return d.year + 1 if d.month >= 10 else d.year


FY22 = fy_bounds(2022)

# Filings: first dockets per fiscal year, easing about 2 per cent a year over the decade.
N0, GROWTH = 61500, -0.02
# Durations from docketing to the docket's decision notice, lognormal around a median (days).
D1_MED, D1_SIG = 673.5, 0.42          # first dockets, CN and DV children
D2_MED, D2_SIG = 400, 0.40           # CX successor dockets
P_ALW, P_REF = 0.44, 0.48            # first-docket outcomes (rest abandoned)
P2_ALW, P2_REF = 0.58, 0.42          # successor outcomes
REF_MULT, ALW_MULT = 1.06, 1.18
P_CX1, P_CX2, MAX_DEPTH = 0.92, 0.49, 3
P_CONT = 0.27                        # share of transfers that carry a continuing application
P_CNDV = 0.05
GRANT_LAG = (97, 180)
CX_GAP = (5, 60)
SUCC_FA_GAP = (20, 50)               # successor docketing to its first action on the merits
P_PROG, PROG_FY = 0.028, (2019, 2022)
P_XFER = 0.12

# Technology groups (codes and names are the same eight labels before and after the 1 October 2023 re-cut).
GROUPS = ["1600", "1700", "2100", "2400", "2600", "2800", "3600", "3700"]
GROUP_NAMES = {
    "1600": "Biotechnology and Organic Chemistry",
    "1700": "Chemical and Materials Engineering",
    "2100": "Computing and Software",
    "2400": "Networks and Communications",
    "2600": "Electrical Systems and Imaging",
    "2800": "Semiconductors and Optics",
    "3600": "Transport, Construction and Commerce",
    "3700": "Mechanical Engineering and Medical Devices",
}
GMULT = {"1600": 0.82, "1700": 0.90, "2100": 0.95, "2400": 1.00, "2600": 1.04, "2800": 1.10, "3600": 1.16,
         "3700": 1.24}
GWEIGHT = {"1600": 0.10, "1700": 0.11, "2100": 0.16, "2400": 0.14, "2600": 0.12, "2800": 0.12, "3600": 0.12,
           "3700": 0.13}
RECUT = dt.date(2023, 10, 1).toordinal()
AUS_PER_GROUP = 8
EXAMINERS_PER_AU = (9, 14)
GROUP_SEED = 7                       # the art unit structure and every group-related draw

# The twin pair: two FY2022 applications identical on every docket, action and continuity column.
TWIN = dict(start=dt.date(2022, 3, 3), fa=dt.date(2022, 10, 14), mid=dt.date(2023, 1, 26),
            ref=dt.date(2023, 5, 18), succ=dt.date(2023, 6, 2), succ_fa=dt.date(2023, 7, 6),
            noa=dt.date(2024, 8, 12), grant=dt.date(2024, 11, 19))

# Partner office corpus (work-sharing programme applications filed FY2019 to FY2022).
CORPUS_FY = (2019, 2022)
