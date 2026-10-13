"""The fixed world of task453: an unnamed Canadian province whose Bureau of Statistics and Economic Analysis builds
each economic region's monthly payroll jobs from the employer returns the Provincial Revenue Agency collects, and
certifies to the Minister which regions the Regional Rapid Response Program Regulation designates each quarter.

From the January 2026 reference month the Agency's returns carry a workplace schedule, and its statistics place each
job at the workplace; before, a multi-workplace employer's jobs all sat at the municipality of its account address
(for most, the head office in Wickmoor or Saltmere). The province's total did not move; the regions did."""
import datetime as dt

SEED = 4532044

BUREAU = "Bureau of Statistics and Economic Analysis"
AGENCY = "Provincial Revenue Agency"
MINISTRY = "Ministry of Labour and Economic Development"
PROGRAM = "Regional Rapid Response Program"
REGULATION = "Regional Rapid Response Program Regulation"

PEOPLE = {
    "minister": ("Joel Ferguson", "Minister of Labour and Economic Development"),
    "chief": ("Heidi Bond", "Chief Statistician"),
    "liaison": ("Jacqueline Chaney", "Statistical Liaison, Revenue Statistics Unit"),
    "manager": ("Ryan Bentley", "Manager, Regional Labour Statistics"),
}

# the months the Agency's statistics cover, and the change of placement
FIRST = (2021, 1)
LAST = (2027, 3)
BREAK = (2026, 1)
EXTRACT_DATE = dt.date(2027, 4, 23)       # the monthly statistics file, January to March 2027 preliminary
REVISION_DATE = dt.date(2027, 5, 7)       # the revision file and the workplace extract
RELEASE_NOTE_DATE = dt.date(2026, 2, 16)
CERT_DATE = dt.date(2027, 5, 13)

# economic regions: code, name, census divisions, post-2026 jobs (thousands), account address region of its branch
# workplaces' employers, branch share of its post-2026 jobs, seasonal amplitude, irregular (sd of log), target (true
# seasonally adjusted Q1 2027 against the 2026 average, per cent), slope of the seasonally adjusted path from July 2025
# (per cent a year), a turn from August 2026 to March 2027 (per cent)
REGIONS = [
    ("E01", "Capital",         ("01", "02"), 85.13, None,                      0.000, 0.020, 0.0025, -1.70, -2.0,  0.0),
    ("E02", "Saltmere Coast",  ("03",),      50.0, None,                      0.000, 0.032, 0.0040,  1.00,  1.2,  0.0),
    ("E03", "Brennick Valley", ("04", "05"), 26.0, {"E01": 1.0},              0.060, 0.030, 0.0070, -2.00, -3.0,  0.0),
    ("E04", "Dunfallow Bay",      ("06",),      20.0, {"E01": 0.3, "E02": 0.7},  0.100, 0.040, 0.0070,  0.90,  1.0,  0.0),
    ("E05", "Quillon Plain",   ("07", "08"), 30.0, {"E01": 1.0},              0.095, 0.030, 0.0070,  1.30,  1.5,  0.0),
    ("E06", "Hethervale Lakes",   ("09",),      17.0, {"E01": 0.25, "E02": 0.75}, 0.120, 0.045, 0.0080,  1.10,  1.2,  0.0),
    ("E07", "Ardvane Uplands", ("10",),      15.0, {"E01": 1.0},              0.130, 0.030, 0.0080,  1.80,  2.2,  0.0),
    ("E08", "Kestrow North",   ("11", "12"), 19.0, {"E01": 1.0},              0.220, 0.022, 0.0080, -0.20,  0.0,  0.0),
    ("E09", "Pellmarsh Hills", ("13",),      23.0, {"E01": 1.0},              0.085, 0.028, 0.0070, -2.10, -2.6,  0.0),
    ("E10", "Varrenby Shore",     ("14",),      15.0, {"E01": 0.9, "E02": 0.1},  0.180, 0.035, 0.0090, -0.10,  0.2,  0.0),
]
RCODE = [r[0] for r in REGIONS]
RNAME = {r[0]: r[1] for r in REGIONS}
NAME2CODE = {r[1]: r[0] for r in REGIONS}

# municipalities: code, name, census division, weight within its region (post-2026 own jobs), valid from, valid to
# (1 January 2025: Wexleigh and Dorran amalgamated as Wexleigh-Dorran, code 0814)
MUNIS = [
    ("0101", "Wickmoor", "01", 0.70, None, None),
    ("0102", "Tallisford", "01", 0.09, None, None),
    ("0103", "Askerby", "01", 0.05, None, None),
    ("0201", "Brenlow", "02", 0.10, None, None),
    ("0202", "Lindmere Park", "02", 0.06, None, None),
    ("0301", "Saltmere", "03", 0.74, None, None),
    ("0302", "Grisport", "03", 0.12, None, None),
    ("0303", "Sealwick Cove", "03", 0.08, None, None),
    ("0304", "Gorsedge", "03", 0.06, None, None),
    ("0401", "Brennick", "04", 0.46, None, None),
    ("0402", "Dowrie", "04", 0.14, None, None),
    ("0403", "Fallow Creek", "04", 0.10, None, None),
    ("0501", "Thornmoor", "05", 0.19, None, None),
    ("0502", "Ivory Crossing", "05", 0.11, None, None),
    ("0601", "Dunfallow", "06", 0.52, None, None),
    ("0602", "Sallow Point", "06", 0.18, None, None),
    ("0603", "Gannet Cove", "06", 0.17, None, None),
    ("0604", "Wrayburn", "06", 0.13, None, None),
    ("0701", "Quillon", "07", 0.41, None, None),
    ("0702", "Cobbleford Flats", "07", 0.15, None, None),
    ("0703", "Tarnbury", "07", 0.12, None, None),
    ("0803", "Wexleigh", "08", 0.11, None, "2024-12-31"),
    ("0806", "Dorran", "08", 0.07, None, "2024-12-31"),
    ("0814", "Wexleigh-Dorran", "08", 0.18, "2025-01-01", None),
    ("0807", "Brackenholt", "08", 0.14, None, None),
    ("0901", "Hethervale", "09", 0.48, None, None),
    ("0902", "Loon Narrows", "09", 0.20, None, None),
    ("0903", "Ambrel Lake", "09", 0.17, None, None),
    ("0904", "Skerrow Falls", "09", 0.15, None, None),
    ("1001", "Ardvane", "10", 0.50, None, None),
    ("1002", "Corriemoor", "10", 0.21, None, None),
    ("1003", "High Tolland", "10", 0.16, None, None),
    ("1004", "Rushby", "10", 0.13, None, None),
    ("1101", "Kestrow", "11", 0.47, None, None),
    ("1102", "Blackrill", "11", 0.17, None, None),
    ("1201", "Ingrey", "12", 0.21, None, None),
    ("1202", "Sorrel Lake", "12", 0.15, None, None),
    ("1301", "Pellmarsh", "13", 0.44, None, None),
    ("1302", "Haverleigh", "13", 0.22, None, None),
    ("1303", "Coldmarsh Ridge", "13", 0.19, None, None),
    ("1304", "Brockmere", "13", 0.15, None, None),
    ("1401", "Varrenby", "14", 0.45, None, None),
    ("1402", "Port Garra", "14", 0.24, None, None),
    ("1403", "Selkie Bay", "14", 0.18, None, None),
    ("1404", "Rossmuir", "14", 0.13, None, None),
]
CD_REGION = {cd: r[0] for r in REGIONS for cd in r[2]}
MUNI_REGION = {m[0]: CD_REGION[m[2]] for m in MUNIS}
MUNI_NAME = {m[0]: m[1] for m in MUNIS}
AMALGAMATED = {"0803": "0814", "0806": "0814"}
HEAD_OFFICE_MUNI = {"E01": "0101", "E02": "0301"}      # the account addresses of the branch employers

# NAICS 2022 sectors, as the Agency's statistics have coded them from January 2024
SECTORS = [
    ("11", "Agriculture, forestry, fishing and hunting"),
    ("21", "Mining, quarrying, and oil and gas extraction"),
    ("22", "Utilities"),
    ("23", "Construction"),
    ("31-33", "Manufacturing"),
    ("41", "Wholesale trade"),
    ("44-45", "Retail trade"),
    ("48-49", "Transportation and warehousing"),
    ("51", "Information and cultural industries"),
    ("52", "Finance and insurance"),
    ("53", "Real estate and rental and leasing"),
    ("54", "Professional, scientific and technical services"),
    ("55", "Management of companies and enterprises"),
    ("56", "Administrative and support, waste management and remediation services"),
    ("61", "Educational services"),
    ("62", "Health care and social assistance"),
    ("71", "Arts, entertainment and recreation"),
    ("72", "Accommodation and food services"),
    ("81", "Other services (except public administration)"),
    ("91", "Public administration"),
]
SECTOR_CODES = [s[0] for s in SECTORS]

# the Agency's industry groups before 2024 (its own grouping of employer activity codes)
GROUPS = [
    ("A", "Primary industries", ("11", "21")),
    ("B", "Utilities and construction", ("22", "23")),
    ("C", "Manufacturing", ("31-33",)),
    ("D", "Trade", ("41", "44-45")),
    ("E", "Transportation, warehousing and information", ("48-49", "51")),
    ("F", "Finance, insurance and real estate", ("52", "53")),
    ("G", "Professional, management and support services", ("54", "55", "56")),
    ("H", "Education, health care and social assistance", ("61", "62")),
    ("J", "Accommodation, food, arts and recreation", ("71", "72")),
    ("K", "Other services and public administration", ("81", "91")),
]
SECTOR_GROUP = {s: g[0] for g in GROUPS for s in g[2]}

# sector mix by kind of region (shares of own jobs), before the regional variation the simulation adds
MIX = {
    "city": {"11": 0.4, "21": 0.3, "22": 1.0, "23": 6.0, "31-33": 4.0, "41": 4.0, "44-45": 11.0, "48-49": 4.0,
             "51": 2.8, "52": 4.5, "53": 1.8, "54": 6.5, "55": 1.2, "56": 4.5, "61": 8.5, "62": 15.0, "71": 1.6,
             "72": 7.5, "81": 4.0, "91": 10.0},
    "coast": {"11": 6.5, "21": 0.6, "22": 0.8, "23": 6.0, "31-33": 11.0, "41": 2.5, "44-45": 12.5, "48-49": 4.5,
              "51": 0.9, "52": 2.0, "53": 1.0, "54": 2.2, "55": 0.2, "56": 3.0, "61": 8.0, "62": 16.0, "71": 1.8,
              "72": 9.0, "81": 4.0, "91": 7.5},
    "farm": {"11": 9.0, "21": 1.2, "22": 1.0, "23": 7.0, "31-33": 9.5, "41": 4.5, "44-45": 13.0, "48-49": 5.5,
             "51": 0.7, "52": 2.2, "53": 0.9, "54": 2.0, "55": 0.2, "56": 2.5, "61": 8.5, "62": 15.5, "71": 1.0,
             "72": 6.5, "81": 4.0, "91": 5.0},
    "resource": {"11": 7.5, "21": 9.0, "22": 1.5, "23": 8.0, "31-33": 12.0, "41": 2.5, "44-45": 11.0, "48-49": 6.0,
                 "51": 0.6, "52": 1.6, "53": 0.8, "54": 2.2, "55": 0.2, "56": 2.8, "61": 7.5, "62": 13.5, "71": 0.8,
                 "72": 6.5, "81": 3.5, "91": 5.5},
    "lakes": {"11": 4.0, "21": 1.0, "22": 1.0, "23": 7.0, "31-33": 5.0, "41": 2.0, "44-45": 13.5, "48-49": 4.0,
              "51": 0.8, "52": 1.8, "53": 1.4, "54": 2.0, "55": 0.2, "56": 2.8, "61": 7.5, "62": 15.0, "71": 4.5,
              "72": 15.0, "81": 4.0, "91": 6.0},
}
KIND = {"E01": "city", "E02": "coast", "E03": "farm", "E04": "coast", "E05": "farm", "E06": "lakes",
        "E07": "resource", "E08": "resource", "E09": "farm", "E10": "coast"}
# the employers whose account address is in Wickmoor or Saltmere and whose workplaces reach other regions: account
# address region, sector, legal name, payroll accounts (reference and operating name), weight in its hq's branch jobs
BRANCH_EMPLOYERS = [
    ("E01", "62", "Northline Health Authority", (("0001", "Northline Health Authority"), ("0002", "Northline Health Authority - Hourly")), 25.0),
    ("E01", "21", "Blackrill Mining Corp.", (("0001", "Blackrill Mining"),), 9.0),
    ("E01", "21", "Upland Aggregates Ltd.", (("0001", "Upland Aggregates"),), 4.0),
    ("E01", "31-33", "Kestrow Forest Products Ltd.", (("0001", "Kestrow Forest Products"),), 10.0),
    ("E01", "11", "Kestrow Woodlands Ltd.", (("0001", "Kestrow Woodlands"),), 5.0),
    ("E01", "31-33", "Skerryvale Seafoods Ltd.", (("0001", "Skerryvale Seafoods"),), 6.0),
    ("E01", "44-45", "Larkmoor Foods Ltd.", (("0001", "Larkmoor Foods"), ("0002", "Larkmoor Express")), 9.0),
    ("E01", "44-45", "Provincial Spirits and Cannabis Retail Corp.", (("0001", "Provincial Spirits"),), 4.0),
    ("E01", "22", "Rillwater Power Corporation", (("0001", "Rillwater Power"),), 6.0),
    ("E01", "48-49", "Plainsway Grain Handling Co-operative Ltd.", (("0001", "Plainsway Grain"),), 4.0),
    ("E01", "52", "Tidewell Credit Union Ltd.", (("0001", "Tidewell Credit Union"),), 6.0),
    ("E01", "91", "Provincial Services Agency", (("0001", "Provincial Services Agency"), ("0002", "Provincial Services Agency - Seasonal")), 6.0),
    ("E02", "62", "Coastal Community Health Services", (("0001", "Coastal Community Health"), ("0002", "Coastal Community Health - Casual")), 30.0),
    ("E02", "31-33", "Coastline Seafoods Ltd.", (("0001", "Coastline Seafoods"),), 30.0),
    ("E02", "48-49", "Saltmere Ferries Ltd.", (("0001", "Saltmere Ferries"),), 12.0),
    ("E02", "44-45", "Shorecrest Hardware Co. Ltd.", (("0001", "Shorecrest Hardware"),), 14.0),
    ("E02", "52", "Coastal Savings Credit Union Ltd.", (("0001", "Coastal Savings"),), 8.0),
]

FILES = {
    "wide": "pra_payroll_jobs_by_municipality_2021-2023.xlsx",
    "long": "pra_payroll_jobs_monthly_2024-01_2027-03.csv",
    "rev": "pra_payroll_jobs_revisions_2027-05-07.csv",
    "work": "pra_workplace_returns_2026-03_2027-03.csv",
    "dict": "pra_statistics_field_descriptions.csv",
    "note": "pra_release_note_place_of_work_2026-02.pdf",
    "conc": "bsea_municipal_concordance.xlsx",
    "reg": "regional_rapid_response_program_regulation.pdf",
    "trans": "pra_transmittal_2027-05-07.txt",
    "lfs": "lfs_economic_region_estimates_2025-2027.csv",
    "pop": "bsea_population_estimates_2024-2026.xlsx",
}
DISTRACTORS = ("lfs", "pop")
DELIVERABLES = ("rapid_response_certification_2027q1.pdf", "regional_payroll_jobs_2027q1.csv")
