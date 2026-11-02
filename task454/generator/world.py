"""The fixed world of task454 (architecture 2): an unnamed Australian state, its Tourism Commission and the Commission's
Regional Visitor Infrastructure Fund. The Fund's 2027 round goes to the five tourism regions outside the capital with
the highest 2026 domestic visitor spending per resident. The Commission measures visitor spending from a card scheme's
de-identified research sample (one row per sampled card, region and month), and residents from the statistics
office's preliminary estimated resident population at 30 June 2026 by statistical area."""
import datetime as dt

SEED = 2
COMMISSION = "Tourism Commission"
FUND = "Regional Visitor Infrastructure Fund"
SCHEME = "Austral Payments Network"
PROGRAM = "Regional Tourism Infrastructure Program"
PEOPLE = {"research": "Samantha Mooney", "fund": "Tina Garza", "scheme": "Jose Gardner", "ceo": "William Gonzalez"}
YEAR = 2026
EXTRACT_DATE = dt.date(2027, 1, 22)       # the scheme's research sample delivery
BOARD_DATE = dt.date(2027, 2, 18)          # the board meeting that adopts the round
GUIDELINES_DATE = dt.date(2026, 11, 9)     # the 2027 round's guidelines
CLOSURE_DATE = dt.date(2026, 12, 31)       # the older program closes
ROUND_BUDGET = 12_000_000                  # the 2027 appropriation for the round
N_FUNDED = 5

# region code, name, eligible, ERP 30 June 2026 (preliminary), ERP 30 June 2025 (revised)
REGIONS = [
    ("WST", "Westhaven", False, 1_420_000, 1_398_600),
    ("JAB", "Jabiru Coast", True, 52_000, 51_420),
    ("LYR", "Lyrebird Peninsula", True, 68_000, 67_150),
    ("YAL", "Yallambee Valley", True, 31_000, 30_770),
    ("SPX", "Spinifex Gorges", True, 9_800, 9_740),
    ("TNG", "Tingle Ranges", True, 24_000, 23_690),
    ("PEL", "Pelican Coast", True, 74_000, 72_880),
    ("GID", "Gidgee Basin", True, 21_500, 21_610),
    ("CAR", "Carisbrook Tablelands", True, 46_000, 45_310),
    ("WOL", "Lower Wollomby", True, 39_000, 38_820),
    ("MUL", "Mulga Plains", True, 28_000, 28_090),
    ("KEL", "Port Kelburn", True, 61_000, 60_540),
]
# the statistics office's release: each region's level against the round planning figures above
RELEASE = {"WST": 1.0121, "JAB": 0.9870, "LYR": 1.0052, "YAL": 0.9930, "SPX": 1.0053, "TNG": 1.0130, "PEL": 0.9865,
           "GID": 1.0061, "CAR": 0.9860, "WOL": 0.9941, "MUL": 1.0027, "KEL": 1.0145}
CODES = [r[0] for r in REGIONS]
NAME = {r[0]: r[1] for r in REGIONS}
ELIGIBLE = [r[0] for r in REGIONS if r[2]]
ERP26 = {r[0]: r[3] for r in REGIONS}
ERP25 = {r[0]: r[4] for r in REGIONS}

# statistical areas: region -> list of (SA3 name, [SA2 names]); SA2 codes are built from the SA3 code
SA3S = {
    "WST": [("Westhaven Inner", ["Westhaven City", "Harbourside", "Kingsley", "Marlowe Park", "Eastbank", "Collins Rise"]),
            ("Westhaven North", ["Northmead Heights", "Glenroy Vale", "Bellvue", "Ashworth", "Carlow", "Norwood Downs"]),
            ("Westhaven South", ["Southport Flats", "Kirkby", "Dunmara", "Elstree Park", "Mallard Point", "Rosslyn"]),
            ("Westhaven East", ["Fernleigh", "Stanmore Hill", "Oakdene", "Pembury", "Lindfield Rise", "Hartwell"]),
            ("Westhaven West", ["Westmere", "Thornbury Gardens", "Copeland", "Bayswater Flats", "Riverina Park", "Langley"]),
            ("Westhaven Bayside", ["Bayview", "Sandgate Shores", "Kittiwake", "Shoalwater", "Mariners Rest", "Tern Point"]),
            ("Westhaven Hills", ["Highbury", "Glen Osmond Rise", "Kurralta Hill", "Wattle Glen", "Tamarind Heights", "Cedar Ridge"]),
            ("Westhaven Outer", ["Brookfield", "Merrivale", "Greystanes Park", "Lowood Plains", "Kinross", "Avondale Fields"])],
    "JAB": [("Jabiru Coast", ["Jabiru Heads", "Coral Strand", "Pandanus Beach", "Mudlark Creek", "Cassia Point"])],
    "LYR": [("Lyrebird Peninsula", ["Lyrebird Point", "Cape Merrow", "Shelly Sands", "Tidewater Hill", "Gannet Rocks", "Saltmarsh"])],
    "YAL": [("Yallambee Valley", ["Yallambee", "Cellar Ridge", "Brightvale", "Quince Hill"])],
    "SPX": [("Spinifex Gorges", ["Spinifex Crossing", "Ochre Bluff"])],
    "TNG": [("Tingle Ranges", ["Tingle", "Blackwood Falls", "Mossvale", "Karri Gully"])],
    "PEL": [("Pelican Coast North", ["Pelican Bay", "Driftwood", "Corella Heads", "Seacliff"]),
            ("Pelican Coast South", ["Mullet Creek", "Sandpiper Flats", "Bream Point", "Coastview"])],
    "GID": [("Gidgee Basin", ["Gidgee", "Coalridge", "Dragline", "Moura Creek"])],
    "CAR": [("Carisbrook", ["Carisbrook Central", "University Park", "Carisbrook East", "Ridgeway", "Carisbrook West"]),
            ("Tablelands", ["Glen Avon", "Stonehenge Flat"])],
    "WOL": [("Lower Wollomby", ["Wollomby", "Riverbend", "Floodgate", "Paddle Steamer Bend", "Willowmere"])],
    "MUL": [("Mulga Plains", ["Mulga", "Saltbush Downs", "Bore Flat", "Highway Junction"])],
    "KEL": [("Port Kelburn", ["Port Kelburn", "Wharf Hill", "Smelter Flat", "Kelburn North", "Shiploader"])],
}
# SA2s the 2027 round's region schedule shares between two regions: SA2 name -> {region: share of its population}
SHARED = {
    "Karri Gully": {"TNG": 0.64, "LYR": 0.36},
    "Willowmere": {"WOL": 0.71, "PEL": 0.29},
    "Stonehenge Flat": {"CAR": 0.58, "MUL": 0.42},
    "Moura Creek": {"GID": 0.83, "MUL": 0.17},
}
ADJ = {("WST", "LYR"), ("WST", "YAL"), ("WST", "TNG"), ("WST", "PEL"), ("LYR", "YAL"), ("YAL", "TNG"), ("YAL", "CAR"),
       ("TNG", "PEL"), ("TNG", "WOL"), ("PEL", "KEL"), ("PEL", "WOL"), ("WOL", "KEL"), ("WOL", "CAR"), ("CAR", "MUL"),
       ("MUL", "GID"), ("MUL", "SPX"), ("KEL", "GID"), ("KEL", "JAB"), ("GID", "SPX"), ("GID", "JAB"), ("SPX", "JAB")}

# the research sample: strata are the statement region at selection (1 January 2026) and one interstate stratum
CARDS_PER_RESIDENT = 0.80
INTERSTATE_CARDS = 480_000
SAMPLING_FRACTION = {"WST": 1 / 250, "IS": 1 / 300}
for _c in ELIGIBLE:
    SAMPLING_FRACTION[_c] = 1 / 60

# genuine visitor spending per resident the world is built to (the golden's quantity, before sampling noise)
VISITOR_TARGET = {"JAB": 10_000, "LYR": 5_900, "SPX": 5_150, "TNG": 4_250, "YAL": 4_050, "PEL": 3_150, "CAR": 2_500,
                  "GID": 2_250, "WOL": 1_500, "KEL": 1_150, "MUL": 950}
# share of each destination's visitor spending by origin stratum (the rest spread over the other regions)
ORIGIN = {"JAB": {"WST": 0.42, "IS": 0.40}, "SPX": {"WST": 0.40, "IS": 0.42}, "LYR": {"WST": 0.80, "IS": 0.06},
          "YAL": {"WST": 0.64, "IS": 0.16}, "TNG": {"WST": 0.40, "IS": 0.35}, "PEL": {"WST": 0.60, "IS": 0.14},
          "CAR": {"WST": 0.45, "IS": 0.20}, "GID": {"WST": 0.50, "IS": 0.20}, "WOL": {"WST": 0.45, "IS": 0.15},
          "KEL": {"WST": 0.45, "IS": 0.20}, "MUL": {"WST": 0.45, "IS": 0.20}}
# daily spend on trips (AUD, low and high) and the share of trips that are long stays at resort rates
TRIP_SPEND = {"JAB": (150, 280), "SPX": (150, 280), "LYR": (110, 220), "YAL": (140, 300)}
TRIP_SPEND_DEFAULT = (100, 200)
LONG_STAY = {"JAB": 0.18, "SPX": 0.15, "LYR": 0.10, "YAL": 0.26, "TNG": 0.20}
# travellers passing through on the highways: weighted card-visits a year and AUD per stop
STOPOVERS = {"MUL": 210_000, "GID": 150_000, "KEL": 30_000}
STOP_SPEND = (25, 85)

# people whose statement address lies in one region while their routine is in another
FIFO = {"WST": 8_200, "PEL": 2_100, "KEL": 1_150, "MUL": 800, "IS": 1_450}          # rostered to the Gidgee Basin mines
STUDENTS = {"WST": 5_600, "PEL": 850, "WOL": 700, "MUL": 650, "JAB": 400, "KEL": 600, "LYR": 300, "IS": 1_800}
MOVERS = [("WST", "CAR", 5_200), ("WST", "PEL", 2_400), ("WST", "TNG", 100), ("WST", "KEL", 1_500), ("WST", "LYR", 700),
          ("WOL", "CAR", 600), ("KEL", "PEL", 400), ("WST", "YAL", 200)]
COMMUTERS = [("MUL", "CAR", 2_000), ("WOL", "KEL", 1_500), ("LYR", "WST", 9_000), ("YAL", "WST", 3_000)]

# the older program, closed at the end of 2026: councils (name, region, first round funded)
COUNCILS = [
    ("Jabiru Shire Council", "JAB", 2019), ("Coral Coast Regional Council", "JAB", 2021),
    ("Lyrebird Peninsula Shire Council", "LYR", 2019), ("Yallambee Valley Council", "YAL", 2020),
    ("Shire of Spinifex", "SPX", 2019), ("Tingle Ranges Shire Council", "TNG", 2020),
    ("Pelican Coast Regional Council", "PEL", 2019), ("Corella Shire Council", "PEL", 2022),
    ("Gidgee Regional Council", "GID", 2019), ("Carisbrook City Council", "CAR", 2020),
    ("Tablelands Shire Council", "CAR", 2021), ("Wollomby Shire Council", "WOL", 2019),
    ("Mulga Shire Council", "MUL", 2020), ("Saltbush Shire Council", "MUL", 2022),
    ("City of Port Kelburn", "KEL", 2019),
]
PROJECT_WORDS = ["lookout and car park", "boardwalk", "amenities block", "RV dump point and rest area",
                 "visitor information bay", "foreshore path", "trailhead facilities", "jetty upgrade",
                 "campground amenities", "heritage walk signage", "picnic shelters", "coastal viewing platform"]
