"""The fixed world for task447: places, carriers and products, systems and facilities, practices,
physicians, the ownership history, the price book and the behaviour parameters. Everything here is
invented; the counties, ZIP codes, CPT codes, NUCC taxonomy codes and place-of-service codes are
the real public vocabularies.
"""
import hashlib
from datetime import date

SEED = 447

# ---------------------------------------------------------------- dates
AS_OF = date(2025, 10, 21)            # the analyst's working date
EXTRACT_PULL = date(2025, 9, 15)      # APCD extract run date
PAID_THROUGH = date(2025, 6, 30)      # runout for the 2024 baseline
NOTICE_FILED = date(2025, 10, 8)
REVIEW_CLOSES = date(2025, 11, 7)
CLOSING = date(2026, 1, 1)
HIST_START = date(2021, 1, 1)
HIST_END = date(2024, 12, 31)
BASE_YEAR = 2024
THRESHOLD = 3_300_000                 # regulation 4.06, set at build after the ladder was measured

# ---------------------------------------------------------------- places (real Wisconsin ZIPs)
ZIPS = {
    "Brown": ["54301", "54302", "54303", "54304", "54311", "54313", "54115"],
    "Outagamie": ["54911", "54913", "54914", "54136", "54140"],
    "Winnebago": ["54901", "54902", "54904", "54956", "54952"],
    "Fond du Lac": ["54935", "54937"],
    "Manitowoc": ["54220", "54241", "54228", "53042", "54230"],
    "Kewaunee": ["54216", "54201", "54217"],
    "Sheboygan": ["53081", "53083", "53073"],
    "Calumet": ["53014", "54129"],
}
ZIP_COUNTY = {z: c for c, zs in ZIPS.items() for z in zs}
ZIP_CITY = {
    "54301": "Green Bay", "54302": "Green Bay", "54303": "Green Bay", "54304": "Green Bay",
    "54311": "Green Bay", "54313": "Green Bay", "54115": "De Pere", "54911": "Appleton",
    "54913": "Appleton", "54914": "Appleton", "54136": "Kimberly", "54140": "Little Chute",
    "54901": "Oshkosh", "54902": "Oshkosh", "54904": "Oshkosh", "54956": "Neenah", "54952": "Menasha",
    "54935": "Fond du Lac", "54937": "Fond du Lac", "54220": "Manitowoc", "54241": "Two Rivers",
    "54228": "Mishicot", "53042": "Kiel", "54230": "Reedsville", "54216": "Kewaunee", "54201": "Algoma",
    "54217": "Luxemburg", "53081": "Sheboygan", "53083": "Sheboygan", "53073": "Plymouth",
    "53014": "Chilton", "54129": "Hilbert",
}

# ---------------------------------------------------------------- carriers and products
# tiers: system -> 1 (preferred) or 2 (second tier); a product with no tiers places every
# in-network facility on one level of cost sharing.
CARRIERS = {
    "C1": {"name": "Cedarbrook Health Plan", "submitter": "WI0412", "funding": "fully insured"},
    "C2": {"name": "Bayfield Mutual Health", "submitter": "WI0587", "funding": "fully insured"},
    "C3": {"name": "Norbridge Health Insurance", "submitter": "WI0633", "funding": "fully insured"},
    "C4": {"name": "Lakefront Benefit Administrators", "submitter": "WI0709", "funding": "self insured (TPA)"},
    "C5": {"name": "Heartland Cooperative Health", "submitter": "WI0751", "funding": "fully insured"},
}
PRODUCTS = {
    # product_id: carrier, plan name, product type, tiered network
    "CBH-PPO1": ("C1", "Cedarbrook Open Access PPO", "PPO", False),
    "CBH-TPO2": ("C1", "Cedarbrook Choice Tiered PPO", "PPO", True),
    "CBH-HMO1": ("C1", "Cedarbrook Select HMO", "HMO", False),
    "BMH-PPO1": ("C2", "Bayfield Mutual PPO", "PPO", False),
    "BMH-VTP3": ("C2", "Bayfield Value Tier PPO", "PPO", True),
    "BMH-HMO2": ("C2", "Bayfield Community HMO", "HMO", False),
    "NBH-PPO1": ("C3", "Norbridge PPO", "PPO", False),
    "NBH-TEP4": ("C3", "Norbridge Tiered EPO", "EPO", True),
    "LBA-PPO7": ("C4", "Lakefront Network PPO", "PPO", False),
    "LBA-TPO9": ("C4", "Lakefront Tiered Choice", "PPO", True),
    "HCH-PPO1": ("C5", "Heartland Cooperative PPO", "PPO", False),
}
# hospital-system placements in the tiered products, by plan year (first plan year a placement
# applies). Freestanding imaging centres, surgery centres and laboratories sit in tier 1 in every
# tiered product; a product with no tiers puts every in-network facility on one level of cost sharing.
TIER_PLACEMENTS = {
    "CBH-TPO2": {"LDG": [(2019, 2)], "WRH": [(2019, 1)], "KNK": [(2019, 1)]},
    "BMH-VTP3": {"LDG": [(2019, 2), (2025, 1)], "WRH": [(2019, 2)], "KNK": [(2019, 2)]},
    "NBH-TEP4": {"LDG": [(2019, 2)], "WRH": [(2019, 2), (2024, 1)], "KNK": [(2019, 1)]},
    "LBA-TPO9": {"LDG": [(2019, 2)], "WRH": [(2019, 1)], "KNK": [(2019, 1)]},
}
FIRST_PLAN_YEAR, LAST_PLAN_YEAR = 2020, 2026


def tier_for(product_id, system, plan_year):
    """1 = preferred (or no tiers), 2 = second tier, for a hospital system in a product's plan year."""
    if system is None or not PRODUCTS[product_id][3]:
        return 1
    t = None
    for y, tt in TIER_PLACEMENTS[product_id][system]:
        if plan_year >= y:
            t = tt
    return t


def plan_year_of(d, renew_month):
    """Plan year (named by its starting calendar year) in force on date d for an employer renewing
    on the first of renew_month."""
    return d.year if d.month >= renew_month else d.year - 1


# member product mixes (shares of members) by population
MIX_BRIGHTWATER = {"CBH-PPO1": .170, "CBH-TPO2": .030, "BMH-PPO1": .055, "BMH-VTP3": .420,
                   "BMH-HMO2": .020, "NBH-PPO1": .115, "NBH-TEP4": .020, "LBA-PPO7": .120,
                   "HCH-PPO1": .050}
MIX_METRO = {"CBH-PPO1": .080, "CBH-TPO2": .260, "CBH-HMO1": .040, "BMH-PPO1": .060, "BMH-VTP3": .040,
             "BMH-HMO2": .020, "NBH-PPO1": .070, "NBH-TEP4": .170, "LBA-PPO7": .130, "LBA-TPO9": .110,
             "HCH-PPO1": .020}
MIX_OSHKOSH = {"CBH-PPO1": .140, "CBH-TPO2": .120, "CBH-HMO1": .090, "BMH-PPO1": .100, "BMH-VTP3": .160,
               "BMH-HMO2": .030, "NBH-PPO1": .110, "NBH-TEP4": .080, "LBA-PPO7": .120, "LBA-TPO9": .030,
               "HCH-PPO1": .020}
MIX_LAKESHORE_OTHER = {"CBH-PPO1": .180, "CBH-TPO2": .060, "CBH-HMO1": .020, "BMH-PPO1": .080,
                       "BMH-VTP3": .250, "BMH-HMO2": .030, "NBH-PPO1": .150, "NBH-TEP4": .060,
                       "LBA-PPO7": .120, "HCH-PPO1": .050}

# ---------------------------------------------------------------- systems and facilities
SYSTEMS = {"LDG": "Ledgestone Health", "WRH": "Wolf River Health", "KNK": "Kinnickinnic Health"}

# service families a facility offers
SVC_IMG = ["70551", "72148", "73721", "74177", "71250", "71046", "73562", "76700", "77067"]
SVC_ECHO = ["93306"]
SVC_ENDO = ["45378", "45380", "43239"]
SVC_ARTH = ["29881"]
SVC_LAB = ["80053", "85025", "80061", "83036", "84443"]
SVC_SLEEP = ["95810"]
SVC_NUC = ["78452"]
SVC_LAB_EXTRA = ["82947", "87086"]       # basket-only lab codes billed in units by some labs

FACILITIES = [
    # key, name, system or None, type, city zip, ccn, services
    ("LMC", "Ledgestone Medical Center", "LDG", "HOPD", "54301", "520147", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB + SVC_LAB_EXTRA),
    ("LFC", "Ledgestone Fox Cities Hospital", "LDG", "HOPD", "54911", "520216", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB + SVC_LAB_EXTRA),
    ("LMN", "Ledgestone Manitowoc Outpatient Center", "LDG", "HOPD", "54220", "520147", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB),
    ("WRO", "Wolf River Hospital Oshkosh", "WRH", "HOPD", "54901", "520198", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB + SVC_NUC + SVC_LAB_EXTRA),
    ("WRF", "Wolf River Fond du Lac Hospital", "WRH", "HOPD", "54935", "520240", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_LAB + SVC_NUC),
    ("KLH", "Kinnickinnic Lakeshore Hospital", "KNK", "HOPD", "54220", "520171", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB + SVC_NUC + SVC_LAB_EXTRA),
    ("KSM", "Kinnickinnic Sheboygan Medical Center", "KNK", "HOPD", "53081", "520035", SVC_IMG + SVC_ECHO + SVC_ENDO + SVC_ARTH + SVC_LAB + SVC_NUC),
    ("MOI", "Manitowoc Open MRI & Imaging", None, "IDTF", "54220", "", SVC_IMG),
    ("TRE", "Two Rivers Endoscopy Center", None, "ASC", "54241", "", SVC_ENDO),
    ("MOS", "Manitowoc Orthopedic Surgery Center", None, "ASC", "54220", "", SVC_ARTH),
    ("NCL", "Northeast Clinical Laboratories", None, "LAB", "54304", "", SVC_LAB + SVC_LAB_EXTRA),
    ("MSD", "Manitowoc Sleep Disorders Center", None, "IDTF", "54220", "", SVC_SLEEP),
    ("FCI", "Fox Cities Imaging Center", None, "IDTF", "54914", "", SVC_IMG),
    ("BAE", "Danz Avenue Endoscopy Center", None, "ASC", "54311", "", SVC_ENDO),
    ("TSC", "Mason Street Surgery Center", None, "ASC", "54304", "", SVC_ARTH),
    ("OIA", "Oshkosh Imaging Associates", None, "IDTF", "54904", "", SVC_IMG),
    ("EDI", "Eastshore Diagnostic Imaging", None, "IDTF", "53083", "", SVC_IMG),
    ("GBS", "Green Bay Sleep Health", None, "IDTF", "54303", "", SVC_SLEEP),
    ("CIC", "Cardiac Imaging Center of Northeast Wisconsin", None, "IDTF", "54311", "", SVC_NUC + SVC_ECHO),
    ("OHL", "Oshkosh Heart & Vascular Imaging", None, "IDTF", "54904", "", SVC_NUC + SVC_ECHO),
]
FAC = {f[0]: f for f in FACILITIES}

# ---------------------------------------------------------------- price book (2024 allowed, carrier C1, independent site)
CPT = {
    # code: (description, family, base price)
    "70551": ("MRI brain without contrast", "IMG", 520.0),
    "72148": ("MRI lumbar spine without contrast", "IMG", 545.0),
    "73721": ("MRI lower extremity joint without contrast", "IMG", 530.0),
    "74177": ("CT abdomen and pelvis with contrast", "IMG", 455.0),
    "71250": ("CT thorax without contrast", "IMG", 290.0),
    "71046": ("Radiologic exam, chest, 2 views", "IMG", 52.0),
    "73562": ("Radiologic exam, knee, 3 views", "IMG", 58.0),
    "76700": ("Ultrasound, abdominal, complete", "IMG", 160.0),
    "77067": ("Screening mammography, bilateral", "IMG", 175.0),
    "93306": ("Transthoracic echocardiography, complete", "ECHO", 395.0),
    "45378": ("Colonoscopy, diagnostic", "ENDO", 960.0),
    "45380": ("Colonoscopy with biopsy", "ENDO", 1020.0),
    "43239": ("Upper GI endoscopy with biopsy", "ENDO", 870.0),
    "29881": ("Knee arthroscopy with meniscectomy", "ARTH", 2300.0),
    "80053": ("Comprehensive metabolic panel", "LAB", 11.20),
    "85025": ("Complete blood count with differential", "LAB", 8.30),
    "80061": ("Lipid panel", "LAB", 14.60),
    "83036": ("Hemoglobin A1c", "LAB", 10.10),
    "84443": ("Thyroid stimulating hormone", "LAB", 17.40),
    "82947": ("Glucose, quantitative, blood", "LAB", 5.40),
    "87086": ("Culture, bacterial, urine, quantitative", "LAB", 9.80),
    "95810": ("Polysomnography, attended", "SLEEP", 1100.0),
    "78452": ("Myocardial perfusion imaging, SPECT, multiple", "NUC", 820.0),
}
CARRIER_FACTOR = {"C1": 1.00, "C2": 0.94, "C3": 1.06, "C4": 1.12, "C5": 0.90}
# site multipliers over the independent price, by system and service family
SITE_MULT = {
    "LDG": {"IMG": 3.30, "ECHO": 2.70, "ENDO": 2.30, "ARTH": 2.15, "LAB": 2.85},
    "WRH": {"IMG": 2.75, "ECHO": 2.35, "ENDO": 2.05, "ARTH": 1.95, "LAB": 2.40, "NUC": 1.45},
    "KNK": {"IMG": 2.55, "ECHO": 2.20, "ENDO": 1.95, "ARTH": 1.90, "LAB": 2.30, "NUC": 1.40},
    None: {"IMG": 1.0, "ECHO": 1.0, "ENDO": 1.0, "ARTH": 1.0, "LAB": 1.0, "SLEEP": 1.0, "NUC": 1.0},
}
# Ledgestone's 2025 agreement with Bayfield (Value Tier placement from plan year 2025) prices its
# outpatient services as a percent of the Medicare amount, by service category
LDG_C2_PCT_2025 = {"IMG": 4.05, "ECHO": 1.55, "ENDO": 1.60, "ARTH": 1.15, "LAB": 2.30}
# code-level differences in Ledgestone's chargemaster against the family multiplier
LDG_RATE_TWEAK = {"93306": 1.0195, "43239": 1.0132}

# professional services billed by the practices (office-based physician services)
PROF = {
    # code: (description, base allowed C1 at Brightwater's current rates, POS)
    "99203": ("Office visit, new patient, low", 132.0, "11"),
    "99204": ("Office visit, new patient, moderate", 201.0, "11"),
    "99205": ("Office visit, new patient, high", 262.0, "11"),
    "99212": ("Office visit, established, straightforward", 74.0, "11"),
    "99213": ("Office visit, established, low", 109.0, "11"),
    "99214": ("Office visit, established, moderate", 158.0, "11"),
    "99215": ("Office visit, established, high", 213.0, "11"),
    "99385": ("Preventive visit, new, 18-39", 196.0, "11"),
    "99386": ("Preventive visit, new, 40-64", 221.0, "11"),
    "99395": ("Preventive visit, established, 18-39", 168.0, "11"),
    "99396": ("Preventive visit, established, 40-64", 183.0, "11"),
    "93000": ("Electrocardiogram with interpretation", 24.0, "11"),
    "36415": ("Routine venipuncture", 6.5, "11"),
    "96372": ("Therapeutic injection", 21.0, "11"),
    "20610": ("Arthrocentesis, major joint", 82.0, "11"),
    "69210": ("Removal impacted cerumen", 52.0, "11"),
    "11102": ("Tangential biopsy of skin", 98.0, "11"),
    "99243": ("Office consultation, low", 172.0, "11"),
    "99244": ("Office consultation, moderate", 236.0, "11"),
    "45378-P": ("Colonoscopy, diagnostic (professional)", 352.0, "24"),
    "45380-P": ("Colonoscopy with biopsy (professional)", 398.0, "24"),
    "43239-P": ("Upper GI endoscopy with biopsy (professional)", 318.0, "24"),
    "29881-P": ("Knee arthroscopy with meniscectomy (professional)", 842.0, "24"),
    "93306-26": ("Echocardiography interpretation", 96.0, "11"),
}
# Ledgestone's professional schedule over Brightwater's current rates, by carrier
LDG_PROF_UPLIFT = {"C1": 1.205, "C2": 1.1472, "C3": 1.215, "C4": 1.240, "C5": 1.180}

# ---------------------------------------------------------------- behaviour
CAPTURE = 0.86          # share of outside referrals a new owner draws in, where its sites are tier 1
# share of a practice's referrals already going to a system before it buys the practice (any tier)
PRE_SHARE = {"P1": 0.075, "P2": 0.085, "P3": 0.08, "P4": 0.08, "P5": 0.08, "W1": 0.08, "W2": 0.085,
             "BMG": 0.08}
STEADY = 0.08           # an owned group's share at its owner for patients it cannot steer (tier 2)

# ---------------------------------------------------------------- identifiers
def luhn_npi(base9):
    s = "80840" + base9
    total = 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check = (10 - (total % 10)) % 10
    return base9 + str(check)


def npi_from(key, kind="1"):
    h = int(hashlib.sha256(("npi|" + key).encode()).hexdigest(), 16)
    base = kind + "%08d" % (h % 10**8)
    return luhn_npi(base)


def tin_from(key):
    h = int(hashlib.sha256(("tin|" + key).encode()).hexdigest(), 16)
    return "39-%07d" % (1000000 + h % 8999999)
