"""task202 constants: the Household Relief Grant of a corporate-endowed relief foundation in the
Philippines, its eight provinces of accredited community partners, the monthly claim returns, the
partner claim portal that two provinces have used since January 2025, and the fieldwork calendar.

Every figure the golden owes is computed from the pack; these only drive the simulation.
"""
import datetime as dt

SEED = 274

# ------------------------------------------------------------------ the foundation
FOUNDATION = "Banahaw Relief Foundation"
FOUNDATION_LEGAL = "Banahaw Relief Foundation, Inc."
SCHEME = "Household Relief Grant"
SCHEME_SHORT = "HRG"
DESK = "Relief Desk"
OFFICE = "Grants and Assurance Office"
DOMAIN = "banahawrelief.org"
# personas: guard.py names --geo PH --seed 202 (never typed by hand)
PEOPLE = {
    "assurance": ("Erica Costa", "e.costa", "Assurance and Standards Lead, Household Relief Grant"),
    "systems": ("Steven Espinoza", "s.espinoza", "Claims and Partner Systems Officer"),
    "director": ("Cheryl Chase", "c.chase", "Executive Director"),
}

# ------------------------------------------------------------------ the policy
COMMITTED_SHARE = 0.060          # clause 9, the share of awards that may be referred
REF_BAND = 4                     # the reference household size
ROUND_TO = 100                   # schedule B rounds each band ceiling up to the nearest PHP 100
# schedule E: the Board approves the reference-size ceiling from a filed list of whole thousands,
# because the figure is printed on the partner guidance and loaded into the portal validation table
CANDIDATE_STEP = 1000            # the spacing of schedule E
CANDIDATE_FROM = 3000
CANDIDATE_TO = 15000
BANDS = [1, 2, 3, 4, 5, 6]
BAND_LABEL = {1: "1 person", 2: "2 persons", 3: "3 persons", 4: "4 persons", 5: "5 persons",
              6: "6 or more persons"}
# schedule B, paragraph B.2: the square root of the band size over the reference size, three decimals
SCALE3 = {1: 500, 2: 707, 3: 866, 4: 1000, 5: 1118, 6: 1225}     # factor x 1000, exact integers
SCALE_TABULATED = [1, 2, 3, 4]   # the four bands schedule B prints; bands 5 and 6 come from B.2

# ------------------------------------------------------------------ the calendar
RETURNS_FROM = (2024, 7)         # the claim returns the foundation still holds
WINDOW_FROM = (2026, 4)          # clause 9: the twelve months to 31 March 2027
WINDOW_TO = (2027, 3)
PORTAL_FROM = (2025, 1)          # the partner claim portal went live in the two pilot provinces
PORTAL_TO = (2027, 3)
EXTRACT_DATE = dt.date(2027, 4, 30)
AS_OF = "2027-04-30"
REVISED_MONTHS = [(2026, 11), (2027, 2)]   # reopened after the partner reconciliation exercise
# the board added the two capital-item components to the eligible list from the 2025/26 year start,
# so every portal claim before this month is a living-cost, medical or transport award only
CAPITAL_FROM = (2025, 7)

# ------------------------------------------------------------------ the award process
BASE = 3253.4                    # the standard living-cost award at the reference band, pesos
# BASE is set, with schedule E's spacing, so that clause 9's crossing sits well inside one
# schedule step: the preceding entry fails the commitment by 0.85 points and the committed
# entry clears it by 0.41, and every graded share prints clear of its rounding boundary.
PROV_SD = 0.42                   # between-province spread of partner award level, log scale
WITHIN_PROV_SD = 0.12            # within-province spread
PILOT_RANKS = (1, 3)             # the two provinces that ran the portal pilot, by award level rank
P_UPPER = 0.09                   # share of awards carrying a one-off capital item
UPPER_MULT = 3.90                # the capital item's multiple of the standard award
LOG_SD_STD = 0.24                # spread of the standard award about its own band level
LOG_SD_UPPER = 0.28              # spread of the capital-item award
MED_AWARDS_YR = 520              # median awards a partner resolves in a year
VOL_SD = 0.50                    # spread of partner award volume, log scale
# the scheme's actual award level by band against schedule B's scale: fixed costs do not scale, so
# the smaller bands run above the scale and the larger below it
BAND_LEVEL_TILT = {1: 1.06, 2: 1.02, 3: 0.99, 4: 1.00, 5: 0.97, 6: 0.94}
SEASON = {1: 0.88, 2: 0.84, 3: 0.86, 4: 0.90, 5: 0.95, 6: 1.02,
          7: 1.08, 8: 1.12, 9: 1.14, 10: 1.18, 11: 1.12, 12: 0.96}   # typhoon season

COMPONENTS_STD = [("LIV", "Living cost support", 0.62), ("MED", "Medical assistance", 0.26),
                  ("TRN", "Transport and documents", 0.12)]
COMPONENTS_UPPER = [("SHL", "Shelter repair", 0.63), ("EQP", "Livelihood equipment replacement", 0.37)]

# ------------------------------------------------------------------ provinces
# foundation code, province, PSGC province code, region
PROVINCES = [
    ("P-ALB", "Albay", "050500", "Region V (Bicol Region)"),
    ("P-CSR", "Camarines Sur", "051700", "Region V (Bicol Region)"),
    ("P-ILI", "Iloilo", "063000", "Region VI (Western Visayas)"),
    ("P-NEC", "Negros Occidental", "064500", "Region VI (Western Visayas)"),
    ("P-CEB", "Cebu", "072200", "Region VII (Central Visayas)"),
    ("P-LEY", "Leyte", "083700", "Region VIII (Eastern Visayas)"),
    ("P-MSO", "Misamis Oriental", "104300", "Region X (Northern Mindanao)"),
    ("P-DVN", "Davao del Norte", "112300", "Region XI (Davao Region)"),
]
PARTNERS_PER_PROVINCE = 11

# the municipalities each province's partners work out of
TOWNS = {
    "P-ALB": ["Legazpi", "Tabaco", "Ligao", "Polangui", "Guinobatan", "Daraga", "Camalig", "Tiwi",
              "Malilipot", "Bacacay", "Oas"],
    "P-CSR": ["Naga", "Iriga", "Pili", "Calabanga", "Libmanan", "Nabua", "Bula", "Goa", "Tigaon",
              "Sipocot", "Baao"],
    "P-ILI": ["Iloilo City", "Passi", "Oton", "Pototan", "Dumangas", "Sara", "Barotac Nuevo",
              "Janiuay", "Miagao", "Cabatuan", "Santa Barbara"],
    "P-NEC": ["Bacolod", "Talisay", "Silay", "Cadiz", "Sagay", "Kabankalan", "Bago", "La Carlota",
              "Hinigaran", "Pontevedra", "Isabela"],
    "P-CEB": ["Cebu City", "Mandaue", "Danao", "Toledo", "Carcar", "Bogo", "Argao", "Barili",
              "Balamban", "Consolacion", "Naga"],
    "P-LEY": ["Tacloban", "Ormoc", "Baybay", "Palo", "Carigara", "Hilongos", "Abuyog", "Tanauan",
              "Alangalang", "Burauen", "Dulag"],
    "P-MSO": ["Cagayan de Oro", "Gingoog", "El Salvador", "Opol", "Villanueva", "Tagoloan",
              "Balingasag", "Medina", "Initao", "Jasaan", "Alubijid"],
    "P-DVN": ["Tagum", "Panabo", "Samal", "Carmen", "Asuncion", "Kapalong", "Santo Tomas",
              "New Corella", "Talaingod", "Braulio E. Dujali", "San Isidro"],
}
# the organisational forms the foundation accredits, in the order they are used per province
FORMS = [
    "{t} Parish Social Action Centre", "Samahan ng Mga Maralita ng {t}", "{t} Multi-Purpose Cooperative",
    "Bayanihan Kapatiran ng {t}", "{t} Community Development Foundation", "{t} Women's Association",
    "Tabang {t} Community Centre", "{t} Fisherfolk Association", "Kapisanan ng Mga Magsasaka ng {t}",
    "{t} Urban Poor Alliance", "{t} Barangay Health Partners",
]
PARTNER_NAME_ROTATE = 3          # the form each province starts from, so the pack is not a template

# ------------------------------------------------------------------ partner lifecycle
NEW_PARTNER = {"province": "P-LEY", "slot": 7, "accredited": dt.date(2026, 8, 1)}
EXIT_PARTNER = {"province": "P-CSR", "slot": 4, "withdrawn": dt.date(2026, 10, 31)}
LAPSED_CODES = 3                 # partners whose accreditation lapsed before the portal era
RECOVERY = {"province": "P-CEB", "slot": 2, "month": (2026, 6), "band": 3}  # a recovered award

# ------------------------------------------------------------------ the claim check (the ask layer)
# The Office ran a pre-payment claim check on every return until 31 December 2025, holding back
# amounts it could not pass; from 1 January 2026 returns are paid in full and reviewed afterwards,
# which is the control clause 7's Desk referral replaces from the 2027/28 scheme year.
CHECK_FROM = (2024, 7)
CHECK_TO = (2025, 12)
SCHEME_YEAR_START = 7            # the scheme year runs July to June, as the return workbooks label it
HOLD_RATE = 0.17                 # partner-months in which the check held an amount back
HOLD_AWARDS = (1, 4)             # awards held in such a month, low inclusive, high exclusive
HOLD_REASONS = ["Receipts incomplete", "Household record incomplete", "Duplicate application",
                "Component not eligible", "Arithmetic error on return"]
REASON_W = [0.31, 0.24, 0.17, 0.16, 0.12]
REASON_FROM = (2025, 4)          # the reason field became mandatory at the April 2025 release
REASON_EARLY = 0.45              # earlier holds a checker recorded a reason for anyway
# the reason was free text until the April 2025 release turned it into a list, so the earlier
# entries carry whatever case and punctuation the checker typed
REASON_STYLE = [lambda s: s.lower(), lambda s: s.upper(), lambda s: s.title(),
                lambda s: s + ".", lambda s: s.lower().replace(" ", "  ")]
CHECKERS = 6
RECHECK_RATE = 0.12              # 2024/25 partner-months the year-end reconciliation checked again
CONSOL_RATE = 0.085              # partner-months the Treasury settled on one payment instruction
DEFER_RATE = 0.022               # partner-months released in a run dated after the archive's cut-off
ARCHIVE_CUTOFF = dt.date(2026, 1, 31)
# three awards recovered inside the 2024/25 returns, each claimed back as its own negative line
# each is claimed back in the last month of a scheme quarter, so the run that carries the recovery
# falls in the quarter after the one the negative claim line sits in
ASK_RECOVERIES = [("P-ALB", 3, (2024, 9), 2), ("P-ILI", 9, (2024, 12), 4),
                  ("P-MSO", 5, (2025, 3), 3), ("P-LEY", 2, (2025, 6), 4)]
