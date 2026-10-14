"""task456: the world every file is computed from.

The Ridgeline Hospital Alliance, a statewide alliance of Tennessee hospitals, runs the Ridgeline ICU Surge Compact:
at each Tuesday review its operations committee activates the compact, for the four weeks from the next Monday, in
every surge region where at least one in three of the region's hospital-days in the 28 days to the Sunday before the
review were full days (every staffed adult intensive care bed occupied at some time that day). Three feeds record
full days, none completely and none only: the alliance's daily capacity survey (the census at 07:00), the regional
bed-status board (the status each hospital sets for its adult ICU, logged in UTC) and the Ridgeline Transfer
Center's call log (each hospital called for each ICU placement and its answer, in Central time). The alliance, its
hospitals, feeds and people are fictional; the counties and their time zones are Tennessee's.
"""
import datetime as dt

SEED = 456

ALLIANCE = "Ridgeline Hospital Alliance"
COMPACT = "Ridgeline ICU Surge Compact"
CENTER = "Ridgeline Transfer Center"
BOARD = "regional bed-status board"
PEOPLE = {"chair": "Abigail Floyd", "data": "Kaitlin Levy", "center": "Ryan Bauer"}

SEASON_START = dt.date(2025, 11, 1)
SEASON_END = dt.date(2026, 1, 19)           # the extract runs to the Monday before the review
WINDOW_START = dt.date(2025, 12, 22)        # Monday
WINDOW_END = dt.date(2026, 1, 18)           # Sunday: the 28 days the review counts
REVIEW = dt.date(2026, 1, 20)               # Tuesday
ACTIVATION = (dt.date(2026, 1, 26), dt.date(2026, 2, 22))
EXTRACT = "2026-01-20"
SURVEY_FORM_CHANGE = dt.date(2025, 12, 1)   # the survey form's new layout (one column renamed)
CODE_CHANGE = dt.date(2025, 12, 1)          # the transfer center's new decline-reason code list
HOLIDAYS = (dt.date(2025, 12, 25), dt.date(2026, 1, 1))
THRESHOLD = 1 / 3

# the eight surge regions: (code, name, time zone of most of its hospitals, hospitals with adult ICUs, the
# region's planned share of full days in the window)
REGIONS = [
    ("NE", "Northeast", "Eastern", 9, 0.48),
    ("ET", "East", "Eastern", 12, 0.19),
    ("SE", "Southeast", "Eastern", 10, 0.12),
    ("UC", "Upper Cumberland", "Central", 5, 0.56),
    ("MS", "Mid-State", "Central", 14, 0.15),
    ("SC", "South Central", "Central", 6, 0.62),
    ("WT", "West", "Central", 7, 0.71),
    ("MD", "Memphis Delta", "Central", 12, 0.10),
]
RCODE = [r[0] for r in REGIONS]
RNAME = {r[0]: r[1] for r in REGIONS}

# counties of each region (FIPS county codes within Tennessee, 47xxx) and the counties on Eastern time
COUNTIES = {
    "NE": ["Sullivan", "Washington", "Carter", "Johnson", "Unicoi", "Greene", "Hawkins", "Hancock"],
    "ET": ["Knox", "Blount", "Anderson", "Sevier", "Jefferson", "Hamblen", "Cocke", "Loudon", "Roane", "Campbell",
           "Claiborne", "Union", "Grainger", "Morgan", "Scott", "Monroe"],
    "SE": ["Hamilton", "Bradley", "McMinn", "Polk", "Meigs", "Rhea", "Marion", "Grundy", "Sequatchie", "Bledsoe"],
    "UC": ["Putnam", "Cumberland", "White", "Warren", "Overton", "Fentress", "Jackson", "Clay", "Pickett", "DeKalb",
           "Smith", "Macon", "Van Buren"],
    "MS": ["Davidson", "Williamson", "Rutherford", "Sumner", "Wilson", "Montgomery", "Robertson", "Dickson",
           "Cheatham", "Stewart", "Houston", "Humphreys", "Trousdale"],
    "SC": ["Maury", "Marshall", "Bedford", "Coffee", "Franklin", "Lincoln", "Giles", "Lawrence", "Wayne", "Lewis",
           "Hickman", "Perry", "Moore"],
    "WT": ["Madison", "Gibson", "Weakley", "Obion", "Dyer", "Lake", "Henry", "Carroll", "Benton", "Decatur",
           "Henderson", "Chester", "McNairy", "Hardin", "Hardeman", "Haywood", "Crockett", "Lauderdale"],
    "MD": ["Shelby", "Fayette", "Tipton"],
}
EASTERN_COUNTIES = {"Sullivan", "Washington", "Carter", "Johnson", "Unicoi", "Greene", "Hawkins", "Hancock", "Knox",
                    "Blount", "Anderson", "Sevier", "Jefferson", "Hamblen", "Cocke", "Loudon", "Roane", "Campbell",
                    "Claiborne", "Union", "Grainger", "Morgan", "Scott", "Monroe", "Hamilton", "Bradley", "McMinn",
                    "Polk", "Meigs", "Rhea"}
FIPS = {"Anderson": "001", "Bedford": "003", "Benton": "005", "Bledsoe": "007", "Blount": "009", "Bradley": "011",
        "Campbell": "013", "Carroll": "017", "Carter": "019", "Cheatham": "021", "Chester": "023",
        "Claiborne": "025", "Clay": "027", "Cocke": "029", "Coffee": "031", "Crockett": "033", "Cumberland": "035",
        "Davidson": "037", "Decatur": "039", "DeKalb": "041", "Dickson": "043", "Dyer": "045", "Fayette": "047",
        "Fentress": "049", "Franklin": "051", "Gibson": "053", "Giles": "055", "Grainger": "057", "Greene": "059",
        "Grundy": "061", "Hamblen": "063", "Hamilton": "065", "Hancock": "067", "Hardeman": "069", "Hardin": "071",
        "Hawkins": "073", "Haywood": "075", "Henderson": "077", "Henry": "079", "Hickman": "081", "Houston": "083",
        "Humphreys": "085", "Jackson": "087", "Jefferson": "089", "Johnson": "091", "Knox": "093", "Lake": "095",
        "Lauderdale": "097", "Lawrence": "099", "Lewis": "101", "Lincoln": "103", "Loudon": "105", "McMinn": "107",
        "McNairy": "109", "Macon": "111", "Madison": "113", "Marion": "115", "Marshall": "117", "Maury": "119",
        "Meigs": "121", "Monroe": "123", "Montgomery": "125", "Moore": "127", "Morgan": "129", "Obion": "131",
        "Overton": "133", "Perry": "135", "Pickett": "137", "Polk": "139", "Putnam": "141", "Rhea": "143",
        "Roane": "145", "Robertson": "147", "Rutherford": "149", "Scott": "151", "Sequatchie": "153",
        "Sevier": "155", "Shelby": "157", "Smith": "159", "Stewart": "161", "Sullivan": "163", "Sumner": "165",
        "Tipton": "167", "Trousdale": "169", "Unicoi": "171", "Union": "173", "Van Buren": "175", "Warren": "177",
        "Washington": "179", "Wayne": "181", "Weakley": "183", "White": "185", "Williamson": "187",
        "Wilson": "189"}

# each feed's chance of flagging a full day (s) and an ordinary day (f); the same in every region, every hospital
# and every day of the season: the census at 07:00 (A), the board's Closed at any time of the local day (B), a
# transfer call declined for no ICU bed on the local day (C)
FEED_S = (0.31, 0.93, 0.23)
FEED_F = (0.009, 0.34, 0.017)

# the systems' own changes during the season
DST_END = dt.datetime(2025, 11, 2, 2, 0)            # local clocks back an hour
BOARD_MIGRATION_UTC = dt.datetime(2025, 12, 8, 9, 0)   # the board vendor's migration (03:00 Central): codes renumbered
ED_SWITCH_UTC = dt.datetime(2026, 1, 5, 12, 0)      # the board retires Divert for emergency departments (06:00 Central)
TC_CUTOVER = dt.datetime(2026, 1, 5, 0, 0)          # the transfer center's new call system (Central)
PRIOR_START = dt.date(2025, 11, 24)                 # the 28 days before the window
PRIOR_END = dt.date(2025, 12, 21)

# Annex A lists every Tennessee county; Cannon County (Upper Cumberland) has no compact hospital
FIPS["Cannon"] = "015"
REGION_FILE_EXTRA = {"UC": ["Cannon"]}
