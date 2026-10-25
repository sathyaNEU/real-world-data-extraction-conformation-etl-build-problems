"""Constants for task269: Tillford County's 2026 residential roll against the State Tax Commission's ratio study rule.

    The world: 30 single-family neighbourhoods in six market areas and 18 condominium projects, a 2025 roll from the
    county's retired appraisal system and a 2026 roll from its replacement, the Recorder's 2025 deeds, the building
    department's 2025 permits and the Board of Review's 2025 hearings."""
import datetime as dt

SEED = 391                       # the single-family world (main call)
SEED_CONDO = 1417                # the condominium class
SEED_REC = 2391                  # record keeping: identifiers, addresses, dates, transfers, hearings
SEED_CPERMIT = 2034              # condominium renovation permits (Ask A)
SEED_PETITION = 2452             # petitions listing several parcels, and rehearings (Ask B)
N_SF = 26000                     # single-family parcels drawn on the 2025 roll before the 2025 splits and combinations
N_SPLIT = 45                     # single-family parcels split in 2025 (each into two)
N_COMBINE = 12                   # pairs of single-family parcels combined in 2025

ASSESS_2025 = dt.date(2025, 1, 1)
ASSESS_2026 = dt.date(2026, 1, 1)
CERT_2025 = dt.date(2025, 6, 2)
CERT_2026 = dt.date(2026, 6, 1)
REDECLARED = dt.date(2025, 7, 1)  # Wexley Commons' amended declaration, recorded and effective
MEMO_DATE = dt.date(2026, 9, 14)
WORK_SESSION = dt.date(2026, 10, 6)
ASSEMBLED = dt.datetime(2026, 9, 18, 15, 25)
INDEX_JAN2026 = 108.5

COUNTY = "Tillford County"
STATE_BODY = "State Tax Commission"
DIVISION = "Property Tax Division"
PEOPLE = {
    "administrator": "David Griffin",      # County Administrator
    "assessor": "Justin Saunders",          # County Assessor
    "division": "Nicole Rodgers",           # Director, Property Tax Division, State Tax Commission
    "bor_chair": "Russell Evans",           # Chair, Tillford County Board of Review
    "recorder": "Paul Parker",              # County Recorder
    "board_chair": "Kristen Valdez",        # Chair, Board of Commissioners
}

STANDARD = {"level_lo": 0.900, "level_hi": 1.100, "cod_max": 15.0, "prd_lo": 0.98, "prd_hi": 1.03}

# market areas and their neighbourhoods; w4's neighbourhood k sits in area k // 5
AREAS = [(1, "North"), (2, "Old Town"), (3, "Riverside"), (4, "East Prairie"), (5, "Lakes"), (6, "South")]
NBHD = [  # (code, name), in the world's neighbourhood order
    ("1104", "Gannet Ridge"), ("1117", "Dorrance Park"), ("1121", "Birchmont"), ("1135", "Hollins Corner"),
    ("1142", "Pruitt Heights"),
    ("2203", "Tannery Row"), ("2210", "Courthouse Square"), ("2216", "Garrison Hill"), ("2228", "Weir Street"),
    ("2233", "Calder Park"),
    ("3302", "Cobble Ford"), ("3311", "Ferry Landing"), ("3319", "Sumac Bend"), ("3324", "Haddow"),
    ("3340", "Netley Flats"),
    ("4406", "Ransome Acres"), ("4413", "Flintlock Hill"), ("4418", "Hawley Fields"), ("4425", "Hayrick Hollow"),
    ("4437", "Thistlewood"),
    ("5501", "Grebe Lake"), ("5509", "Vireo Shores"), ("5514", "Yarrow Point"), ("5522", "Cranmoor"),
    ("5531", "Tamarack Bay"),
    ("6605", "Linnet Farms"), ("6612", "Cinder Ridge"), ("6620", "Eastwick Farms"), ("6627", "Stillwater Glen"),
    ("6639", "Orchard Vale"),
]
# condominium projects: (name, neighbourhood index, units, street). Wexley Commons is the last, re-declared in 2025.
CONDO_PROJECTS = [
    ("Mercer Lofts", 6, 64, "Mercer St"), ("Halsey Court", 7, 48, "Halsey Ct"), ("Cobalt Yards", 5, 92, "Foundry Ave"),
    ("Larkspur Terrace", 21, 56, "Larkspur Dr"), ("Fenwick Place", 12, 72, "Fenwick Pl"),
    ("Orrin Square", 8, 110, "Orrin Sq"), ("Quillon House", 9, 44, "Quillon Way"), ("Arbor Mews", 2, 58, "Arbor Ln"),
    ("Brightwater Lofts", 11, 126, "Water St"), ("Ferrin Court", 27, 52, "Ferrin Ct"), ("Gilder Row", 5, 40, "Gilder Row"),
    ("Hartsell Square", 16, 88, "Hartsell Sq"), ("Inman Terrace", 23, 66, "Inman Rd"), ("Kittredge Lofts", 10, 98,
                                                                                         "Kittredge St"),
    ("Lindell Court", 26, 60, "Lindell Ct"), ("Norcott House", 13, 76, "Norcott Ave"), ("Pomeroy Flats", 18, 84,
                                                                                      "Pomeroy St"),
    ("Wexley Commons", 7, 420, "Wexley Blvd"),
]

FILES = {
    "roll26": "assessor_roll_2026_certified.csv",
    "roll25": "assessor_roll_2025_certified.xlsx",
    "crosswalk": "neighborhood_crosswalk.csv",
    "changes": "parcel_change_log_2025.csv",
    "deeds": "recorder_deeds_2025.csv",
    "index": "residential_price_index_tillford.csv",
    "permits": "building_permits_2025.csv",
    "bor": "board_of_review_hearings_2025.csv",
    "rule": "str_rule_18-7_residential_ratio_studies.pdf",
    "memo": "reappraisal_offer_memo.pdf",
    "dictionary": "data_dictionary.txt",
    "homestead": "homestead_credits_2026.csv",
    "levy": "levy_and_rates_fy2026.xlsx",
}
DISTRACTORS = ("homestead", "levy")
GOLDEN_MEMO = "reappraisal_recommendation.docx"
GOLDEN_BOOK = "ratio_study_2026_roll.xlsx"
DELIVERABLES = ("golden/" + GOLDEN_MEMO, "golden/" + GOLDEN_BOOK)
