"""task462 world: Tarvane Methane Ratings' 2027 low-methane rating of the Tollaver Basin's twelve gas producers, on
the methane their sites emitted over the rating year (1 October 2025 to 30 September 2026) as Talmora Aerial's four
basin-wide campaigns measured it, against the methane their wells produced."""
import datetime as dt

SEED = 4622070

ORG = "Tarvane Methane Ratings, LLC"
ORG_SHORT = "Tarvane"
PROVIDER = "Talmora Aerial, Inc."
PROVIDER_SHORT = "Talmora"
AGENCY = "State Oil and Gas Commission"
BASIN = "Tollaver Basin"
PEOPLE = {"ratings": "Aaron Watkins", "provider": "Kimberly Clements"}

RATING_START = dt.date(2025, 10, 1)
RATING_END = dt.date(2026, 9, 30)
HOURS = (RATING_END - RATING_START).days * 24 + 24            # 8,760
LIMIT = 0.20                                                  # per cent
FLOOR = 5.0                                                   # kg/h, the standard's floor
KG_PER_MCF = 19.2                                             # methane, 14.73 psia and 60 F
STATE_PSIA = 14.65
STD_PSIA = 14.73
ISSUE_DATE = dt.date(2026, 12, 9)
PACK_DATE = dt.date(2026, 11, 18)

# the four campaigns: name, first and last flight day
CAMPAIGNS = [("TB-2511", dt.date(2025, 11, 10), dt.date(2025, 11, 14)),
             ("TB-2602", dt.date(2026, 2, 9), dt.date(2026, 2, 13)),
             ("TB-2605", dt.date(2026, 5, 11), dt.date(2026, 5, 15)),
             ("TB-2608", dt.date(2026, 8, 10), dt.date(2026, 8, 14))]

# the instrument as the world runs it: a pass detects a plume of rate q (kg/h) with probability
# 1 / (1 + exp(-(ln q - ln Q50) / POD_S)); a detected plume is quantified with lognormal error QUANT_SD
POD_Q50 = 7.5
POD_S = 0.50
QUANT_SD = 0.22
WITHIN_SD = 0.15             # a source's rate from one pass to the next
ATTRIB_M = 150.0             # Talmora attributes a plume to the nearest facility within 150 m

# producers: name, operator number, type, sites, gas Bcf in the rating year, fields (name, share), target intensity
# (per cent), shares of persistent leaks, tank dumps and episodes, leak median kg/h, tank rate kg/h, tank duty
PRODUCERS = [
    ("Calbrent Energy",          "OP-21407", "C", 70, 320, (("Fenholt Bend", .7), ("East Tollaver", .3)), .120, .55, .45, 0, 8.5, 110, .24),
    ("Pinyon Draw Production",   "OP-23318", "M", 95, 290, (("Pinyon Draw", 1.0),), .250, .88, .12, 0, 6.6, 100, .22),
    ("Brushy Mesa Operating",    "OP-19852", "T", 60, 260, (("Brushy Mesa", .8), ("Fenholt Bend", .2)), .145, .22, .78, 0, 8.5, 120, .25),
    ("Lechuza Creek Resources",  "OP-24631", "S", 80, 450, (("Lechuza Creek", .6), ("East Tollaver", .4)), .340, .45, .25, .30, 8.5, 110, .24),
    ("Anchell Oil & Gas",        "OP-17765", "M", 70, 205, (("Anchell Flats", 1.0),), .265, .90, .10, 0, 6.4, 100, .22),
    ("Corrandale Petroleum",     "OP-22094", "T", 55, 235, (("Brushy Mesa", .5), ("Corran Ridge", .5)), .150, .20, .80, 0, 8.5, 125, .25),
    ("Marrowind Operating",      "OP-25510", "S", 50, 140, (("Corran Ridge", 1.0),), .450, .40, .30, .30, 8.5, 110, .24),
    ("Ostrel Energy",            "OP-20389", "C", 85, 375, (("East Tollaver", .6), ("Lechuza Creek", .4)), .135, .55, .45, 0, 8.5, 110, .24),
    ("Pellisto Gas Partners",    "OP-26147", "M", 85, 250, (("Sotol Wash", .7), ("Anchell Flats", .3)), .280, .88, .12, 0, 6.5, 100, .22),
    ("Ruskmoor Exploration",     "OP-18820", "T", 30, 110, (("Sotol Wash", 1.0),), .390, .25, .75, 0, 9.0, 120, .26),
    ("Ashmund Production",      "OP-27703", "S", 95, 525, (("Fenholt Bend", .5), ("Pinyon Draw", .5)), .310, .45, .25, .30, 8.5, 110, .24),
    ("Sunmere Natural Gas",      "OP-21976", "C", 60, 230, (("Sunmere Dome", 1.0),), .270, .60, .40, 0, 9.5, 110, .24),
]
NAMES = [p[0] for p in PRODUCERS]

# operators in the basin outside the rating (the commission's list carries them; the plant takes their gas)
OTHER_OPERATORS = [("Mossreed Oil Co.", "OP-15512", 14), ("Kelterra Gas Gathering LLC", "OP-29014", 0),
                   ("Penwarden Petroleum Corp.", "OP-16677", 9), ("Thistle Run Energy", "OP-28351", 6),
                   ("Okafor Royalty Operating", "OP-30472", 4)]
LEGAL = {"Calbrent Energy": "Calbrent Energy, LLC", "Pinyon Draw Production": "Pinyon Draw Production Company",
         "Brushy Mesa Operating": "Brushy Mesa Operating, LP", "Lechuza Creek Resources": "Lechuza Creek Resources, Inc.",
         "Anchell Oil & Gas": "Anchell Oil & Gas, LLC", "Corrandale Petroleum": "Corrandale Petroleum Corporation",
         "Marrowind Operating": "Marrowind Operating, LLC", "Ostrel Energy": "Ostrel Energy Partners, LP",
         "Pellisto Gas Partners": "Pellisto Gas Partners, LP", "Ruskmoor Exploration": "Ruskmoor Exploration, Inc.",
         "Ashmund Production": "Ashmund Production Company", "Sunmere Natural Gas": "Sunmere Natural Gas, LLC"}

PLANT = "Tollaver Gas Processing Plant"
MIDSTREAM = "Kelterra Gas Gathering LLC"
EXTRACT_FIRST = (2025, 7)          # the commission's extract starts with July 2025 production
STATEMENT_MONTHS = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 11)]
CODE_SWITCH = (2026, 1)            # the commission's routine-flaring code FR, from January 2026 reports
PLANT_STREAM = 741                 # the random streams of the ask-only files, off the main call's
FLARING_STREAM = 351

FILES = {
    "plumes": "talmora_plume_detections_tollaver_2025_2026.csv",
    "coverage": "talmora_flight_line_coverage_tollaver_2025_2026.csv",
    "releases": "talmora_controlled_release_study_2025.xlsx",
    "methods": "talmora_survey_methods_note_2026.pdf",
    "standard": "tarvane_low_methane_rating_standard_2026.pdf",
    "sites": "tarvane_tollaver_site_register_2026.csv",
    "production": "ogc_well_production_tollaver_2025_2026.csv",
    "operators": "ogc_operator_list_2026.csv",
    "gas": "tollaver_gas_composite_analyses_2024_2026.csv",
    "flaring": "ogc_flaring_venting_reports_tollaver_2025_2026.csv",
    "leases": "ogc_lease_register_tollaver_2026.csv",
    "basin": "ogc_basin_flaring_summary_2025_2026.csv",
    "statements": "tollaver_plant_allocation_statements_2025_2026.csv",
    "stations": "tollaver_plant_meter_stations_2026.csv",
    "heating": "tollaver_plant_station_heating_values_2025_2026.csv",
    "ghgrp": "ghgrp_subpart_w_tollaver_facilities_2023_2025.csv",
    "satellite": "tollaver_basin_satellite_methane_2025_2026.json",
    "dict": "tarvane_rating_folder_data_dictionary.xlsx",
    "manifest": "tarvane_rating_folder_manifest.csv",
}
GOLDEN = {"workbook": "tollaver_producer_methane_ratings_2027.xlsx",
          "plumes": "talmora_plumes_conformed_2025_2026.csv"}
DISTRACTORS = ["ghgrp", "satellite"]
MAIN_FILES = ["plumes", "coverage", "releases", "methods", "standard", "sites", "production", "operators", "gas"]
ASK_FILES = ["flaring", "leases", "basin", "statements", "stations", "heating", "operators"]
