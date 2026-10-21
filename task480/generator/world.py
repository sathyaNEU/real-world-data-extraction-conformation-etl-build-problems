"""The fiction and its constants: a state environmental quality department's Mobile Sources Section, the twelve
counties of a fictional ozone nonattainment area, the area's first biennial inspection cycle (2024 and 2025) and
the 2027 Vehicle Retirement Program. Every number the generator draws from lives here."""
import datetime as dt

SEED = 480
STATE_AGENCY = "Department of Environmental Quality"
DIVISION = "Air Quality Division"
SECTION = "Mobile Sources Section"
DMV = "Division of Motor Vehicles"
DOT = "Department of Transportation"
AREA = "Halvering Basin"
EIP = "Halvering Basin Enhanced Inspection Program"
PROGRAM = "Vehicle Retirement Program"
PEOPLE = {"chief": ("Bridget Palmer", "Chief, Mobile Sources Section"),
          "director": ("Jacqueline Aguilar", "Director, Air Quality Division")}

# county: DMV county number (the state's alphabetical numbering), FIPS county code, seat and other towns
COUNTIES = [
    ("Copperleaf", 14, "027", ["Grisdale"]),
    ("Dunmarsh", 17, "033", ["Calderwick", "Brindlemoor"]),
    ("Elkhollow", 21, "041", ["Oakhaven", "Ashborough"]),
    ("Halvering", 29, "057", ["Tessaly", "Hartsview"]),
    ("Kinnard", 35, "069", ["Tarnholt"]),
    ("Larkhaven", 38, "075", ["Thistlebury"]),
    ("Linnmere", 40, "079", ["Corvenna", "Yarrowdale"]),
    ("Marlbank", 44, "087", ["Wyecombe"]),
    ("Quarrybrook", 58, "115", ["Ravensby"]),
    ("Sallowford", 63, "125", ["Belvane"]),
    ("Thorncastle", 71, "141", ["Pennyfield"]),
    ("Wexmoor", 79, "157", ["Port Ashby", "Quillmont"]),
]
NAMES = [c[0] for c in COUNTIES]
CNO = {c[0]: c[1] for c in COUNTIES}
NAME_OF = {c[1]: c[0] for c in COUNTIES}
FIPS = {c[0]: c[2] for c in COUNTIES}
TOWNS = {c[0]: c[3] for c in COUNTIES}

# the fleet: vehicles on file (gasoline-family and other fuels), fleet-age shift in years against the area's
# age profile, and the county's driving intensity (long commutes and rural distances above 1)
FLEET = {
    "Wexmoor": (59567, -2.4, 0.8166), "Linnmere": (29330, -0.8, 1.0833), "Halvering": (33236, -0.3, 0.9452),
    "Elkhollow": (16629, 0.8, 1.3246), "Dunmarsh": (18009, 1.6, 0.8412), "Quarrybrook": (14789, 0.4, 1.1340),
    "Marlbank": (14393, 2.2, 1.1919), "Larkhaven": (12600, 2.8, 0.9042), "Copperleaf": (9275, 1.6, 1.4606),
    "Thorncastle": (9948, 3.2, 0.8195), "Sallowford": (8574, 1.0, 1.1399), "Kinnard": (6243, 3.8, 1.0037),
}
# the random draw each county's vehicles come from (0 is the county's first stream)
DRAW = {"Linnmere": 4, "Halvering": 6, "Elkhollow": 9, "Quarrybrook": 13, "Marlbank": 2, "Larkhaven": 13,
        "Copperleaf": 11, "Sallowford": 12, "Kinnard": 3}
SIGMA_K = 0.33          # vehicle-to-vehicle spread of driving intensity (log scale)
LT_SHARE = 0.46

# yearly miles by age since first sale: a straight decline to a floor (the truth the cross-section traces)
ACC_NEW, ACC_SLOPE, ACC_FLOOR = 15400.0, -375.0, 2400.0
YEAR_NOISE = 0.08

# the inspection program
EIP_START = dt.date(2024, 1, 2)
CYCLE_END = dt.date(2025, 12, 31)
FIRST_OBD_MY = 1996
EXEMPT_NEWEST = 3        # tested only if model year <= test year - 3 (the four newest model years exempt)
COMPLIANCE = 0.955

# the program
SNAPSHOT = dt.date(2026, 7, 1)
ELIG_MY = (2005, 2014)
THRESHOLD_TONS = 10.0
GRAMS_PER_TON = 907184.74
VOUCHER = 1000

# Table 2: running exhaust NOx, grams per mile, calendar year 2027, by model year and class (PC car, LT light truck)
RATES = {
    1996: (1.68, 2.21), 1997: (1.59, 2.10), 1998: (1.47, 1.96), 1999: (1.31, 1.78), 2000: (1.09, 1.49),
    2001: (0.92, 1.25), 2002: (0.81, 1.10), 2003: (0.70, 0.95), 2004: (0.52, 0.80), 2005: (0.42, 0.62),
    2006: (0.34, 0.50), 2007: (0.26, 0.40), 2008: (0.20, 0.30), 2009: (0.16, 0.22), 2010: (0.12, 0.16),
    2011: (0.110, 0.150), 2012: (0.098, 0.136), 2013: (0.087, 0.121), 2014: (0.078, 0.108), 2015: (0.069, 0.095),
    2016: (0.061, 0.083), 2017: (0.046, 0.062), 2018: (0.037, 0.049), 2019: (0.030, 0.040), 2020: (0.024, 0.032),
    2021: (0.020, 0.026), 2022: (0.017, 0.022), 2023: (0.015, 0.019), 2024: (0.013, 0.017), 2025: (0.012, 0.015),
    2026: (0.011, 0.014), 2027: (0.010, 0.013),
}

# the 2025 pilot
PILOT_COUNTIES = ["Elkhollow", "Dunmarsh", "Larkhaven", "Kinnard"]
PILOT_MY = (2001, 2010)
PILOT_START, PILOT_END = dt.date(2025, 6, 2), dt.date(2025, 12, 19)

FILES = {
    "registrations": "vehicle_registrations_2026-07-01.csv",
    "inspections": "eip_inspections_2024_2025.csv",
    "stations": "eip_station_register_2026-06-30.xlsx",
    "rates": "nox_running_rates_cy2027.xlsx",
    "guidelines": "vehicle_retirement_program_guidelines_2027.pdf",
    "counties": "county_codes.csv",
    "body": "registration_body_codes.csv",
    "vouchers": "vrp_pilot_vouchers_2025.xlsx",
    "invoices": "vrp_pilot_dismantler_invoices_2025.csv",
    "closeout": "vrp_pilot_close_out_2025.pdf",
    "annual": "eip_annual_report_2024.pdf",
    "dictionary": "extract_notes_and_dictionary.pdf",
    "hpms": "dot_county_vmt_2025.csv",
    "fuel": "gasoline_sales_by_county_2025.csv",
    "population": "county_population_estimates_2025.csv",
}
GOLDEN = {"workbook": "retirement_program_county_nox_2027.xlsx", "memo": "intake_counties_2027_memo.docx"}
DISTRACTORS = ["dot_county_vmt_2025.csv", "gasoline_sales_by_county_2025.csv", "county_population_estimates_2025.csv"]
