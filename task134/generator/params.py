"""World parameters for task134 architecture 4: the Port of Fendmouth's maintenance dredging after the 2027 deepening."""
import datetime as dt

SEED = 134_2027
EXPORT_DATE = dt.datetime(2027, 1, 18, 9, 20, 0)      # the in-fiction export date: every file's mtime
ASOF = "2027-01-18"
ZIP_DT = (2027, 1, 18, 9, 20, 0)

ORG = "Fendmouth Borough Council"
DEPT = "Harbour Department, Fendmouth Borough Council"
PORT = "Port of Fendmouth"
CONTRACTOR = "Dunmarsh Dredging Ltd"
SURVEY_A = "Holmwood Hydrographic Ltd"
SURVEY_B = "Seaward Geodata Ltd"
LAB = "Aldern Analytical Ltd"
DREDGER = "Fend Endeavour"
HIRED = "Maasbank"
PEOPLE = {"manager": "Harriet Thorpe", "harbour_master": "Damian Davies", "finance": "Graham Ellis",
          "lab": "Zoe Dickinson", "contractor_pm": "Martyn Rogers", "dredge_master": "Garry Stephenson",
          "surveyor_b": "Liam O'Brien"}

CD_BELOW_ODN = 2.90          # chart datum lies 2.90 m below Ordnance Datum Newlyn at the port
DEPTH_NOW = 12.3             # maintained depth of the channel and basin, 2016 to 2027
DEPTH_NEW = 14.3             # from 1 October 2027
SLOPE = 4.0                  # side slopes 1 in 4 (horizontal per vertical)

# Centreline waypoints: chainage (km) and OSGB36 easting, northing (m). Reaches are straight between them.
WAYPOINTS = [(0.00, 652400.0, 296100.0), (2.60, 649957.0, 296989.0), (5.10, 647466.0, 297207.0),
             (7.70, 645215.0, 298507.0), (9.40, 643573.0, 298947.0), (10.20, 642800.0, 299154.0)]

# The dredged parts. half: half the maintained width (m); nat: natural bed depth below CD on the north and south
# margins; k: the infill coefficient (per year) of the relaxation law rate = k * (held depth - natural depth). Each
# part's k and natural bed are set so the record measures one coefficient across the parts and berths within a natural
# spread of under one per cent, so every model of the law (each part's own ratio, one pooled coefficient on absolute
# volumes or on the increment, a line with an intercept, a power law, the berths' own exponent or coefficient) puts
# every part inside its rounding bin.
PARTS = [
    # code, name, ch0, ch1, half, nat_n, nat_s, k
    ("OC", "Outer Channel", 0.00, 2.60, 100.0, 7.87, 7.99, 0.11384),
    ("FR", "Fend Roads", 2.60, 5.10, 90.0, 8.42, 8.50, 0.11479),
    ("MR", "Middle Reach", 5.10, 7.70, 85.0, 6.26, 6.40, 0.11237),
    ("IR", "Inner Reach", 7.70, 9.40, 80.0, 5.16, 5.32, 0.11267),
    ("TB", "Turning Basin", 9.40, 10.20, 210.0, 4.92, 4.92, 0.11387),
]
REACHES = ["OC", "FR", "MR", "IR"]
DEEPENED = ["OC", "FR", "MR", "IR", "TB"]

# Berth pockets on the basin's north side (offset +210 to +250 m) and its west end; s in km along the last reach. They
# open onto the basin floor and share its natural bed; Berth 2 relaxes toward it at the common coefficient.
BERTHS = [
    # code, name, s0, s1, t0, t1, depth (None = not maintained), nat, k
    ("NQ1", "North Quay Berth 1", 9.440, 9.680, 210.0, 250.0, 12.8, 4.87, 0.11314),
    ("NQ2", "North Quay Berth 2", 9.700, 9.920, 210.0, 250.0, None, 4.87, 0.11350),
    ("NQ3", "North Quay Berth 3", 9.940, 10.180, 210.0, 250.0, 12.8, 4.87, 0.11026),
    ("CT5", "Container Terminal Berth 5", 10.200, 10.255, -165.0, 165.0, 14.3, 4.87, 0.11481),
]
NQ2_LAST_DREDGED = dt.date(2019, 3, 22)
NQ2_LAST_DEPTH = 12.95

MARGIN = 300.0                # survey coverage beyond the maintained width (m)

# Licence years run 1 October to 30 September; the record is 2016-17 to 2025-26.
LY_FIRST, LY_LAST = 2016, 2025          # licence year y runs 1 Oct y to 30 Sep y+1
MONTH_WEIGHTS = {10: 0.095, 11: 0.100, 12: 0.105, 1: 0.110, 2: 0.100, 3: 0.090, 4: 0.075, 5: 0.065, 6: 0.060,
                 7: 0.060, 8: 0.065, 9: 0.075}
STORM_SD = 0.030              # year-to-year storminess (common to every part)
PART_SD = 0.015               # part-specific year-to-year noise

# Survey programme: contractor A every April and October 2016 to April 2023, contractor B from October 2023.
SURVEY_A_DATES = [dt.date(2016, 4, 12), dt.date(2016, 10, 18), dt.date(2017, 4, 11), dt.date(2017, 10, 10),
                  dt.date(2018, 4, 17), dt.date(2018, 10, 16), dt.date(2019, 4, 9), dt.date(2019, 10, 15),
                  dt.date(2020, 4, 21), dt.date(2020, 10, 13), dt.date(2021, 4, 13), dt.date(2021, 10, 19),
                  dt.date(2022, 4, 12), dt.date(2022, 10, 11), dt.date(2023, 4, 18)]
SURVEY_B_DATES = [dt.date(2023, 10, 17), dt.date(2024, 4, 16), dt.date(2024, 10, 15), dt.date(2025, 4, 15),
                  dt.date(2025, 10, 14), dt.date(2026, 4, 14), dt.date(2026, 10, 13)]
GRID_A, GRID_B = 50.0, 40.0

# Disposal sites (WGS84, degrees and decimal minutes as the licence gives them): corner points in order.
SITES = {
    "FS": ("Fend Spit", [(52, 29.650, 1, 47.525), (52, 29.650, 1, 48.475), (52, 29.150, 1, 48.475), (52, 29.150, 1, 47.525)]),
    "WD": ("Wenning Deep", [(52, 26.175, 1, 56.950), (52, 26.175, 1, 58.250), (52, 25.425, 1, 58.250), (52, 25.425, 1, 56.950)]),
}
FS_CLOSED_MONTHS = (12, 1, 2)            # Fend Spit closed 1 December to the end of February
ROUTE = {"OC": "WD", "FR": "WD", "MR": "FS", "IR": "FS", "TB": "FS", "NQ1": "FS", "NQ3": "FS", "CT5": "FS"}
CODES_2021 = {"OC": "A1", "FR": "A2", "MR": "A3", "IR": "A4", "TB": "B1", "NQ1": "B2", "NQ2": "B3", "NQ3": "B4", "CT5": "B5"}
LOAD_TDS = 1180.0
RHO_S, RHO_W = 2.65, 1.025
HIRE_FROM, HIRE_TO = (2025, 11, 17), (2025, 12, 21)
GAUGE_FAULT_FROM, GAUGE_FAULT_TO = (2026, 1, 7), (2026, 3, 27)
GAUGE_FACTOR = 1.068
SAMPLING = {2025: ((2025, 3, 11), (2025, 3, 13), (2025, 4, 2)), 2026: ((2026, 3, 10), (2026, 3, 12), (2026, 3, 27))}
