"""The fixed facts of the Kilcarrow world: places, the census basis, the station shares, the calendars."""
import datetime as dt

SEED = 149
AS_OF = "2027-12-06"
TZ = "Europe/Dublin"

# Panel weeks: Monday 6 September to Friday 26 November 2027 (stays that start on a local weekday).
PANEL_START = dt.date(2027, 9, 6)
PANEL_END = dt.date(2027, 11, 26)
BANK_HOLIDAYS_2027 = [dt.date(2027, 1, 1), dt.date(2027, 3, 17), dt.date(2027, 3, 29), dt.date(2027, 5, 3),
                      dt.date(2027, 6, 7), dt.date(2027, 8, 2), dt.date(2027, 10, 25)]
MIDTERM_2027 = [dt.date(2027, 10, 25) + dt.timedelta(days=i) for i in range(5)]
BANK_HOLIDAYS_2019 = [dt.date(2019, 1, 1), dt.date(2019, 3, 18), dt.date(2019, 4, 22), dt.date(2019, 5, 6),
                      dt.date(2019, 6, 3), dt.date(2019, 8, 5), dt.date(2019, 10, 28), dt.date(2019, 12, 25),
                      dt.date(2019, 12, 26)]
MIDTERM_2019 = [dt.date(2019, 10, 28) + dt.timedelta(days=i) for i in range(5)]

# Workplace zones of the census place-of-work table (final release codes) and the business case's station
# share of each destination's journeys to work from the catchment.
DEST = [
    # code, final-release name, provisional-release name, census commuters (final), station share
    ("KW01", "Kilcarrow city centre", "Kilcarrow City Central Area", 1430, 0.42),
    ("KW02", "Kilcarrow Docklands", "Docklands and North Quays", 1210, 0.46),
    ("KW03", "University Hospital campus", "Hospital Campus (Wilton Road)", 2000, 0.31),
    ("KW04", "Kilcarrow University", "University Campus", 540, 0.28),
    ("KW05", "Carrigboy business park", "Carrigboy Industrial Estate", 1330, 0.22),
    ("KW06", "Port of Kilcarrow, Ringcurran", "Ringcurran Port Area", 750, 0.07),
    ("KW07", "Ballymurragh retail park", "Ballymurragh", 630, 0.03),
    ("KW08", "Airport business park", "Airport and Environs", 420, 0.05),
    ("KW09", "Lisnagry and Ardnagree", "Lisnagry-Ardnagree", 510, 0.12),
    ("KW10", "Rathgarvan", "Rathgarvan", 670, 0.00),
    ("KW11", "Rest of County Kilcarrow", "Remainder of County", 490, 0.02),
]
SPECIAL = [("KX01", "Works mainly at or from home", 880), ("KX02", "No fixed place of work", 410),
           ("KX03", "Outside County Kilcarrow", 260)]
THRESHOLD = 1400

# Catchment small areas (census 2022 small-area codes as the authority's GIS holds them) and their worker shares.
SMALL_AREAS = [("177041001", 0.17), ("177041002", 0.12), ("177041003", 0.16), ("177041004", 0.13),
               ("177041005", 0.15), ("177042001", 0.14), ("177042002", 0.13)]

# Working regimes behind each destination's commuters: (regime, share). Office-hybrid weeks carry a day count
# distribution; rosters are worked over seven days.
REGIMES = {
    "KW01": [("hybrid_a", 0.60), ("fixed5", 0.15), ("parttime", 0.25)],
    "KW02": [("hybrid_b", 0.94), ("fixed5", 0.06)],
    "KW03": [("nurse3x12", 0.55), ("fixed5", 0.30), ("hybrid_a", 0.15)],
    "KW04": [("hybrid_c", 0.85), ("fixed5", 0.15)],
    "KW05": [("roster4on4off", 0.70), ("fixed5", 0.20), ("hybrid_a", 0.10)],
    "KW06": [("shift5of7", 0.50), ("fixed5", 0.40), ("roster4on4off", 0.10)],
    "KW07": [("shift5of7", 0.50), ("fixed5", 0.50)],
    "KW08": [("shift5of7", 0.60), ("fixed5", 0.40)],
    "KW09": [("fixed5", 0.80), ("hybrid_a", 0.20)],
    "KW10": [("fixed5", 0.90), ("parttime", 0.10)],
    "KW11": [("fixed5", 0.70), ("shift5of7", 0.30)],
}
HYBRID_DAYS = {"hybrid_a": {1: 0.12, 2: 0.38, 3: 0.33, 4: 0.13, 5: 0.04},
               "hybrid_b": {1: 0.18, 2: 0.42, 3: 0.28, 4: 0.09, 5: 0.03},
               "hybrid_c": {1: 0.10, 2: 0.30, 3: 0.35, 4: 0.20, 5: 0.05}}
HYBRID_DOW = [0.70, 1.25, 1.30, 1.20, 0.55]
TRAVEL_MIN = {"KW01": 34, "KW02": 38, "KW03": 31, "KW04": 36, "KW05": 44, "KW06": 47, "KW07": 22, "KW08": 41,
              "KW09": 18, "KW10": 9, "KW11": 39}

# Network cells: catchment home cells, and the cells of each workplace zone (one straddling the hospital and
# the university).
HOME_CELLS = [("RG%02d" % i, w) for i, w in enumerate([0.13, 0.11, 0.12, 0.10, 0.12, 0.11, 0.10, 0.11, 0.10], 1)]
WORK_CELLS = {"KW01": ["KC101", "KC102", "KC103"], "KW02": ["KD201", "KD202"], "KW03": ["KH301", "KH302", "KH309"],
              "KW04": ["KU401", "KU309"], "KW05": ["CB501", "CB502"], "KW06": ["RC601"], "KW07": ["BM701"],
              "KW08": ["AP801"], "KW09": ["LS901", "AR902"], "KW10": ["RG03", "RG07"], "KW11": ["CO111", "CO112"]}
STRADDLE = {"KH309": [("KW03", 0.58), ("KW04", 0.42)]}
LOCAL_CELLS = ["RG01", "RG02", "RG04", "RG05", "RG06", "RG08", "RG09", "BM701"]
OUTSIDE_CELLS = ["XO001", "XO002"]
SAMPLE = 0.09  # panel devices per resident commuter, about

# Existing stations on the Ardnagree line and their 2019 base and 2027 standing (ordinary weekday entries).
STATIONS = [
    # code, name, opened, closed, base weekday entries 2019, 2027 ratio, office profile
    ("ARD", "Ardnagree", dt.date(1994, 5, 9), None, 1650, 0.74, False),
    ("LSG", "Lisnagry", dt.date(2019, 9, 2), None, 1110, 0.71, False),
    ("KCN", "Kilcarrow Central", dt.date(1994, 5, 9), None, 6400, 0.66, True),
    ("KDK", "Kilcarrow Docklands", dt.date(2008, 11, 3), None, 4100, 0.57, True),
    ("UHK", "University Hospital", dt.date(2003, 2, 17), dt.date(2023, 2, 28), 2300, 0.83, False),
    ("KUH", "University Hospital", dt.date(2023, 3, 1), None, 2300, 0.83, False),
    ("CBH", "Carrigboy Halt", dt.date(2001, 9, 3), dt.date(2021, 6, 13), 1450, 0.79, False),
    ("CBY", "Carrigboy", dt.date(2021, 6, 14), None, 1450, 0.79, False),
]
LISNAGRY_FORECAST = 1140
