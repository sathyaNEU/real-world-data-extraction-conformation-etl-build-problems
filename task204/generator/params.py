"""Fixed parameters of the Carvale world (task204, architecture v2).

Everything the generator draws comes from SEED and the constants below; nothing is read from the
environment, so two runs write identical bytes.
"""
import datetime as dt

SEED = 20402
TZ = "America/Edmonton"

# Review windows (Monday to Sunday, local dates). The directive's review period is the twelve completed
# weeks before the assessment date.
W26 = (dt.date(2026, 2, 9), dt.date(2026, 5, 3))
W25 = (dt.date(2025, 2, 10), dt.date(2025, 5, 4))
# Extract windows (one week either side of each review window).
X26 = (dt.date(2026, 2, 2), dt.date(2026, 5, 10))
X25 = (dt.date(2025, 2, 3), dt.date(2025, 5, 11))
PULL_LOCAL = dt.datetime(2026, 5, 11, 6, 14, 52)        # RMS extract pulled
TPO_PULL_LOCAL = dt.datetime(2026, 5, 11, 9, 40, 11)    # transit occurrence log exported
ASSESS_DATE = dt.date(2026, 5, 4)
PLAN_SIGN = dt.date(2026, 5, 28)
FICTION_ASOF = dt.date(2026, 5, 15)                      # every file dated on or before this

# GTFS service periods.
SERVICE = {
    "W25": (dt.date(2025, 1, 5), dt.date(2025, 5, 17)),
    "W26": (dt.date(2026, 1, 4), dt.date(2026, 3, 28)),
    "S26": (dt.date(2026, 3, 29), dt.date(2026, 6, 27)),
}
HOLIDAYS = {dt.date(2025, 2, 17): "Family Day", dt.date(2025, 4, 18): "Good Friday",
            dt.date(2026, 2, 16): "Family Day", dt.date(2026, 4, 3): "Good Friday"}
SPRING_CHANGE = dt.date(2026, 3, 29)

# Stations: code, name, line, easting, northing (UTM zone 12N, metres). Inbound = toward Centre Square.
# The Eastline is listed outbound order from Westgate; Fairgrounds opens with the spring service change.
EAST = [
    ("WG", "Westgate", 326180, 5934620),
    ("CS", "Centre Square", 330020, 5935010),
    ("UY", "Union Yards", 332140, 5935330),
    ("MB", "Millbrook", 334230, 5935790),
    ("FG", "Fairgrounds", 335290, 5936120),
    ("CB", "Cobb Street", 336420, 5936410),
    ("AR", "Ashford Road", 338530, 5937080),
    ("RV", "Ridgeview", 340610, 5937920),
    ("PG", "Prairie Gate", 342790, 5938640),
]
NORTH = [
    ("CS", "Centre Square", 330020, 5935010),
    ("SH", "Station Hill", 329720, 5937010),
    ("KP", "Kerr Park", 329410, 5939030),
    ("HL", "Hollin", 329120, 5941110),
    ("LM", "Larchmont", 328880, 5943240),
]
UNIVERSITY = (334320, 5937260)   # centre of the corridor north of Millbrook

# Patrol districts, 2026 layout (in force 1 January 2026): rectangles in UTM metres (xmin, ymin, xmax, ymax).
BOX = (319000, 5929000, 347000, 5947000)
D26 = {
    "D1": [(327600, 5932800, 331300, 5936200)],
    "D2": [(319000, 5929000, 327600, 5942300)],
    "D3": [(327600, 5936200, 331300, 5940000)],
    "D4": [(331300, 5929000, 333600, 5940000), (327600, 5929000, 331300, 5932800)],
    "D5": [(327600, 5940000, 333600, 5942300)],
    "D6": [(333600, 5929000, 335800, 5940000)],
    "D7": [(337500, 5929000, 339600, 5942300)],
    "D8": [(335800, 5929000, 337500, 5942300), (333600, 5940000, 335800, 5942300)],
    "D9": [(339600, 5929000, 347000, 5947000)],
    "D10": [(319000, 5942300, 339600, 5947000)],
}
# 2025 layout: D10 did not exist (its ground was the north of D5 and D8) and the D6/D8 line ran 600 m west.
D25 = {
    "D1": [(327600, 5932800, 331300, 5936200)],
    "D2": [(319000, 5929000, 327600, 5942300)],
    "D3": [(327600, 5936200, 331300, 5940000)],
    "D4": [(331300, 5929000, 333600, 5940000), (327600, 5929000, 331300, 5932800)],
    "D5": [(319000, 5942300, 333600, 5947000), (327600, 5940000, 333600, 5942300)],
    "D6": [(333600, 5929000, 335200, 5940000)],
    "D7": [(337500, 5929000, 339600, 5942300)],
    "D8": [(335200, 5929000, 337500, 5942300), (333600, 5940000, 335200, 5942300),
           (333600, 5942300, 339600, 5947000)],
    "D9": [(339600, 5929000, 347000, 5947000)],
}

# Offender groups behind the 2026 rise (the clean truth; no file carries a group field).
GROUPS = {
    "G1": {"stations": ["RV", "AR", "MB", "UY"], "n_runs": 18},           # rides the Eastline inbound
    "G2": {"station": "CB", "n": 16},                                       # Cobb Street evenings
    "G3": {"station": "HL", "n": 18},                                       # Hollin after school
    "G4": {"centre": UNIVERSITY, "n": 14},                                  # university corridor, late night
}

# Background phone robberies and snatches per day by district (both windows; lone offenders mostly).
BG_RATE = {"D1": 0.42, "D2": 0.20, "D3": 0.18, "D4": 0.20, "D5": 0.12, "D6": 0.22, "D7": 0.12,
           "D8": 0.13, "D9": 0.12, "D10": 0.09}
ONTRAIN_RATE = 1.45      # on-train phone thefts per day across both lines (recorded by the transit officers)

# All-occurrence volume per day city-wide (other offence types fill the RMS extract).
OTHER_RATE = 134.0

# Fare gates: gate codes before and after the spring service change (codes were reissued when the
# infill station opened). Station -> list of (entrance, code_before, code_after).
GATES = {
    "WG": [("Main", "E01", "E01", "GA-1102")],
    "CS": [("Concourse", "C01", "C01", "GA-1007"), ("4 Street", "C02", "C02", "GA-1038")],
    "UY": [("Main", "E03", "E03", "GA-1215")],
    "MB": [("North", "E04", "E04", "GA-1311"), ("South", "E14", "E15", "GA-1349")],
    "FG": [("Main", None, "E05", "GA-2604"), ("Exhibition", None, "E17", "GA-2611")],
    "CB": [("Main", "E05", "E06", "GA-1426")],
    "AR": [("Main", "E06", "E07", "GA-1520")],
    "RV": [("Main", "E07", "E08", "GA-1633"), ("Park and Ride", "E17", "E14", "GA-1689")],
    "PG": [("Main", "E08", "E09", "GA-1702")],
    "SH": [("Main", "N02", "N02", "GA-3104")],
    "KP": [("Main", "N03", "N03", "GA-3151")],
    "HL": [("Main", "N04", "N04", "GA-3227"), ("School Lane", "N14", "N14", "GA-3260")],
    "LM": [("Main", "N05", "N05", "GA-3318")],
}
# Mean weekday entries per station per day (both entrances together); weekend factor applied in world.py.
ENTRIES = {"WG": 3100, "CS": 9800, "UY": 2700, "MB": 4300, "FG": 1500, "CB": 2400, "AR": 2200,
           "RV": 3900, "PG": 3300, "SH": 2600, "KP": 1900, "HL": 2900, "LM": 2300}

PEOPLE = {
    "deputy_chief": "Emily Wagner",
    "cau_supervisor": "Joel Jackson",
    "tpo_sergeant": "Steven House",
    "directive_owner": "Kristin Weber",
}
