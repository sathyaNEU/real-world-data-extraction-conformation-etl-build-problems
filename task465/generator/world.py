"""The fixed world of task465: Callowmere Electric's service divisions and counties, the state agencies and surveys, the
HEMA plan's standard, the people and the pack's file names. Everything random lives in sim.py."""

ORG = "Callowmere Electric Company"
ORG_SHORT = "Callowmere Electric"
PROGRAMME = "Home Energy Medical Assistance"
PROG = "HEMA"
REGULATOR = "State Utility Commission"
ENERGY_OFFICE = "State Energy Office"
HEALTH_DEPT = "State Department of Health"
DEMOGRAPHER = "State Demographer's Office"
SURVEY_A = "Household Energy Affordability Survey 2025"
SURVEY_B = "State Health Survey 2025"

AS_OF = "2026-11-16"          # the folder as the programme manager assembled it
FILING = "2026-12-01"         # the 2027 plan is due at the Commission
PLAN_YEAR = 2027
DATA_YEAR = 2025
ENROL_DATE = "2026-10-31"     # the enrolment and battery extracts run to the end of October 2026

CASELOAD = 400                # one caseworker for every 400 eligible households in a division, or part of that number
BURDEN = 0.06                 # annual home energy costs above 6 per cent of household income
INCOME_LIMIT = 50000          # household income under $50,000

BANDS = ["Under $25,000", "$25,000 to $49,999", "$50,000 to $74,999", "$75,000 and over"]
BAND_EDGES = [0, 25000, 50000, 75000, None]
ELIGIBLE_BANDS = [0, 1]
# The health survey's eight income categories, nested in the demographer's four bands.
INCCAT = [(1, "Less than $10,000", 0), (2, "$10,000 to $14,999", 0), (3, "$15,000 to $24,999", 0),
          (4, "$25,000 to $34,999", 1), (5, "$35,000 to $49,999", 1), (6, "$50,000 to $74,999", 2),
          (7, "$75,000 to $99,999", 3), (8, "$100,000 or more", 3)]
INCCAT_BOUNDS = {1: (6000, 9999), 2: (10000, 14999), 3: (15000, 24999), 4: (25000, 34999), 5: (35000, 49999),
                 6: (50000, 74999), 7: (75000, 99999), 8: (100000, 260000)}

# name, burden multiplier, equipment multiplier, households (thousands), counties, income mix by band
DIVISIONS = [
    ("Northern", 1.40, 0.80, 66, ["Alderwold", "Brackmere", "Corthorpe", "Kellingwold"], (0.31, 0.30, 0.20, 0.19)),
    ("Lakeshore", 1.30, 0.86, 52, ["Garrowmere", "Hethercombe", "Ivythorpe", "Shelmere"], (0.29, 0.30, 0.22, 0.19)),
    ("River Valley", 1.18, 1.00, 92, ["Ambercombe", "Dellingholme", "Fernthorpe", "Ravenwold"], (0.25, 0.28, 0.24, 0.23)),
    ("High Plains", 1.06, 1.10, 78, ["Brindlewold", "Melthorpe", "Quarrowby"], (0.23, 0.27, 0.25, 0.25)),
    ("Central", 1.00, 0.94, 128, ["Coltholme", "Elderholme", "Gorsecombe", "Kestrelmere", "Nettlethorpe"],
     (0.20, 0.26, 0.25, 0.29)),
    ("Southern Hills", 0.92, 1.20, 58, ["Thistlecombe", "Ullswold"], (0.23, 0.27, 0.25, 0.25)),
    ("Southwest", 0.84, 1.30, 146, ["Lindenholme", "Oakenholme", "Reedcombe", "Wickthorpe"], (0.18, 0.24, 0.26, 0.32)),
    ("North Metro", 0.76, 1.12, 205, ["Pellingmere", "Vetchmere"], (0.14, 0.22, 0.26, 0.38)),
    ("South Metro", 0.70, 1.36, 170, ["Quillholme", "Tarnholme"], (0.16, 0.23, 0.25, 0.36)),
]
DIV_NAMES = [d[0] for d in DIVISIONS]
PILOT_DIVISIONS = ["North Metro", "South Metro"]
# Counties outside the service territory (other utilities), in the state surveys and the demographer's release.
OUTSIDE = [("Glasswold", 1.10, 0.95, 38), ("Marlowcombe", 0.95, 1.05, 52), ("Ostercombe", 1.05, 1.00, 29),
           ("Pinewold", 1.25, 0.90, 24), ("Thornwold", 0.85, 1.15, 61), ("Umberholme", 0.90, 1.10, 47),
           ("Wendlecombe", 1.15, 1.00, 33), ("Willowcombe", 0.80, 1.20, 44)]
OUTSIDE_INC = (0.22, 0.27, 0.25, 0.26)

COUNTIES = sorted([c for d in DIVISIONS for c in d[4]] + [o[0] for o in OUTSIDE])
FIPS = {c: "%03d" % (2 * i + 1) for i, c in enumerate(COUNTIES)}
# On 1 July 2026 Kestrelmere County moved from the Central to the Southwest division; accounts opened before then keep
# the division they were set up under. DIVISION_OF is the current map, the one the 2027 plan staffs.
REORG = {"Kestrelmere": ("Central", "Southwest", "2026-07-01")}
HOME_OF = {c: d[0] for d in DIVISIONS for c in d[4]}
DIVISION_OF = {c: REORG[c][1] if c in REORG else HOME_OF[c] for c in HOME_OF}
# The health department's public health districts and the demographer's planning regions (their own groupings).
PHD = {}
for k, cs in enumerate([["Alderwold", "Brackmere", "Corthorpe", "Kellingwold", "Glasswold"],
                        ["Garrowmere", "Hethercombe", "Ivythorpe", "Shelmere", "Marlowcombe", "Brindlewold"],
                        ["Ambercombe", "Dellingholme", "Fernthorpe", "Ravenwold", "Melthorpe", "Quarrowby"],
                        ["Coltholme", "Elderholme", "Gorsecombe", "Kestrelmere", "Nettlethorpe", "Ostercombe"],
                        ["Pellingmere", "Vetchmere", "Pinewold", "Thornwold"],
                        ["Quillholme", "Tarnholme", "Lindenholme", "Umberholme"],
                        ["Thistlecombe", "Ullswold", "Oakenholme", "Reedcombe", "Wickthorpe", "Wendlecombe",
                         "Willowcombe"]], start=1):
    for c in cs:
        PHD[c] = k
REGION = {}
for k, cs in enumerate([["Alderwold", "Brackmere", "Corthorpe", "Kellingwold", "Glasswold", "Pinewold"],
                        ["Garrowmere", "Hethercombe", "Ivythorpe", "Shelmere", "Marlowcombe"],
                        ["Ambercombe", "Dellingholme", "Fernthorpe", "Ravenwold", "Brindlewold", "Melthorpe",
                         "Quarrowby", "Ostercombe"],
                        ["Coltholme", "Elderholme", "Gorsecombe", "Kestrelmere", "Nettlethorpe", "Thornwold"],
                        ["Pellingmere", "Vetchmere", "Quillholme", "Tarnholme", "Umberholme"],
                        ["Thistlecombe", "Ullswold", "Lindenholme", "Oakenholme", "Reedcombe", "Wickthorpe",
                         "Wendlecombe", "Willowcombe"]], start=1):
    for c in cs:
        REGION[c] = k
assert sorted(PHD) == COUNTIES and sorted(REGION) == COUNTIES

PEOPLE = {"manager": "Stacy Williams", "vp": "Shawn Taylor"}
TITLES = {"manager": "HEMA Programme Manager", "vp": "Vice President, Customer Programmes"}

FILES = {
    "heas": "heas_2025_household_puf.csv",
    "heas_methods": "heas_2025_technical_notes.pdf",
    "shs": "shs_2025_household_file.csv",
    "shs_codebook": "shs_2025_household_codebook.xlsx",
    "pilot": "hema_screening_pilot_2025.csv",
    "pilot_report": "hema_screening_pilot_report_2025.pdf",
    "estimates": "household_estimates_county_income_2025.xlsx",
    "divisions": "callowmere_service_divisions.csv",
    "plan": "callowmere_hema_plan_2027_draft.pdf",
    "baseline": "medical_baseline_enrolment_2026.csv",
    "batteries": "battery_placement_work_orders_2026.csv",
    "hvi": "heat_vulnerability_index_county_2025.csv",
    "liheap": "energy_assistance_applications_2025.csv",
    "dict": "data_dictionary.csv",
    "register": "file_register.csv",
}
DISTRACTORS = ["hvi", "liheap"]
GOLDEN = {"workbook": "hema_caseworkers_2027.xlsx", "table": "hema_eligible_households_2025.csv"}
