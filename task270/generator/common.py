"""Constants shared by the task270 generator: the mutual, its eight rating regions and their postcode districts, the
no-claims step scale, the dates of the 2025 platform move, Step Protection and the extract, and the shipped file
names."""
import datetime as dt

SOCIETY = "Fennacre Mutual Insurance Society"
SHORT = "Fennacre Mutual"
PEOPLE = {"actuary": "Jayne Gallagher", "chair": "Antony Evans"}

# the eight rating regions: code, name, postcode districts (the region map before 1 April 2025)
REGIONS = [
    ("NEC", "North East and Cumbria",
     ["NE1", "NE2", "NE3", "NE4", "NE5", "NE6", "NE9", "NE12", "NE15", "NE23", "NE28", "NE31", "SR3", "SR4", "DH1",
      "DH3", "TS5", "TS7", "TS17", "DL1", "CA1", "CA2", "CA11", "LA9"]),
    ("NWE", "North West",
     ["M14", "M20", "M21", "M33", "M41", "WA4", "WA5", "WN3", "WN6", "PR1", "PR2", "BL1", "BL3", "L4", "L15", "L18",
      "CH43", "CH46", "SK4", "SK8", "OL1", "BB2", "FY1", "LA1"]),
    ("YHU", "Yorkshire and the Humber",
     ["LS6", "LS8", "LS17", "LS28", "BD3", "BD9", "HD1", "HD2", "HX1", "WF1", "WF10", "S2", "S10", "S11", "S35",
      "HU5", "HU7", "YO10", "YO24", "DN4", "DN15", "DN35", "HG1", "LS25"]),
    ("EMI", "East Midlands",
     ["NG1", "NG5", "NG7", "NG9", "NG16", "NG31", "LE2", "LE3", "LE4", "LE11", "LE18", "DE1", "DE21", "DE22", "DE24",
      "LN1", "LN6", "NN1", "NN3", "NN5", "S40", "S41", "PE9", "NG18"]),
    ("WMI", "West Midlands",
     ["B13", "B14", "B23", "B29", "B31", "B44", "B73", "B90", "CV1", "CV5", "CV31", "WV3", "WV10", "WS1", "WS9",
      "DY1", "DY8", "ST1", "ST4", "ST5", "WR5", "TF1", "HR1", "SY1"]),
    ("EOE", "East of England",
     ["CB1", "CB4", "CB22", "NR2", "NR4", "NR31", "IP1", "IP4", "IP33", "CO1", "CO4", "CM1", "CM2", "SS2", "SS9",
      "LU2", "LU4", "PE1", "PE2", "AL1", "SG1", "MK40", "MK41", "CB6"]),
    ("SEA", "South East",
     ["RG1", "RG2", "RG30", "RG41", "OX1", "OX4", "GU1", "GU14", "BN1", "BN2", "BN3", "ME7", "ME15", "CT1", "TN1",
      "PO4", "PO19", "SO15", "SO17", "HP13", "SL1", "KT1", "RH1", "MK9"]),
    ("SWW", "South West and Wales",
     ["BS3", "BS7", "BS16", "BS34", "EX1", "EX4", "PL1", "PL4", "TQ2", "BA1", "BA2", "GL1", "GL50", "SN1", "TA1",
      "CF5", "CF14", "CF23", "NP20", "SA1", "SA2", "LL11", "BH1", "TR1"]),
]
CODES = [r[0] for r in REGIONS]
NAME = {r[0]: r[1] for r in REGIONS}
# two districts moved region on 1 April 2025
REMAP_DATE = dt.date(2025, 4, 1)
REMAP = {"S40": ("EMI", "YHU"), "MK40": ("EOE", "SEA")}

# the no-claims step scale (2024 revision): premium relativity on each step, 0 the lowest
STEPS = list(range(10))
REL = [1.20, 1.00, 0.88, 0.78, 0.70, 0.63, 0.57, 0.52, 0.48, 0.45]
DROP = 3               # an at-fault or split claim paid in a policy year moves the policy three steps down at renewal
EXCESS = 250           # the compulsory accidental damage excess, pounds
IPT = 0.12             # insurance premium tax

PILOT_START = dt.date(2024, 1, 1)       # Step Protection sold at renewal on steps 6 to 9 from this day
PILOT_STEPS = (6, 7, 8, 9)
MIGRATION = dt.date(2025, 7, 1)         # policy administration and claims move to the new platform
EXTRACT = dt.date(2026, 9, 30)          # the actuary's data cut
ASSEMBLED = dt.datetime(2026, 10, 5, 16, 20)
COMMITTEE = dt.date(2026, 10, 21)       # the pricing committee adopts the 2027 basis
WORDING_2027 = dt.date(2027, 1, 1)      # step protection on every policy from the renewals on this day

ACC_YEARS = (2024, 2025)
FIRST_INCEPTION = dt.date(2023, 1, 1)

FILES = {
    "pol_legacy": "policy_terms_legacy_export_2023_2025.csv",
    "pol_platform": "policy_terms_platform_export_2025_2026.csv",
    "crosswalk": "policy_number_crosswalk_2025.csv",
    "mta": "mid_term_adjustments_2023_2026.csv",
    "clm_legacy": "claims_legacy_export_2023_2025.csv",
    "clm_platform": "claims_platform_export_2025_2026.csv",
    "glass": "glass_partner_jobs_2025.csv",
    "salvage": "salvage_sales_statements_2025_2026.xlsx",
    "regions": "rating_region_postcode_map.csv",
    "scale": "no_claims_step_scale_2024.pdf",
    "basis": "rating_basis_2027_note.pdf",
    "guide": "claims_and_policy_data_guide.pdf",
    "industry": "industry_private_motor_statistics_2025.xlsx",
    "complaints": "customer_complaints_log_2025.csv",
    "contents": "contents.txt",
}

PARTNER = "Clearvane Auto Glass"                 # the glass partner
SALVAGE = "Tremlow Vehicle Remarketing"        # the salvage agent
