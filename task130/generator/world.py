"""Red Cedar Valley School District's health plan: the fixed facts of the world (dates, people, plan
design, the provider and drug vocabularies). Everything stochastic lives in sim.py."""
import datetime as dt

SEED = 101005

D = dt.date
SIM_START = D(2024, 1, 1)
SIM_END = D(2028, 3, 31)
CONVERSION = D(2025, 1, 1)            # Ellery Benefit Administrators takes over from Bramwell Plan Services
PAID_THROUGH = D(2027, 2, 28)         # the extracts' paid cut-off
DRAFT_PAID = D(2026, 12, 31)
LETTER_PAID = D(2027, 1, 31)          # the renewal letter's experience cut-off
BID_PAID = D(2024, 12, 31)            # data book: 2024 incurred, paid through December 2024
BID_ELIG = D(2025, 1, 1)
DRAFT_ELIG = D(2027, 1, 1)
FINAL_ELIG = D(2027, 3, 1)
PROG_START, PROG_END = D(2027, 4, 1), D(2028, 3, 31)
ANALOG_START, ANALOG_END = D(2025, 4, 1), D(2026, 3, 31)
ASOF = D(2027, 3, 12)
BOARD = D(2027, 3, 25)

TREND_MED, TREND_RX = 1.065, 1.09
LIST_SIZE = 140
TIERS = ((1, 53.5), (2, 45.5), (3, 40.0), (4, 0.0))   # tier t holds scores at or above its floor

DISTRICT = "Red Cedar Valley School District"
DISTRICT_SHORT = "Red Cedar Valley Schools"
DISTRICT_NO = "ISD 2817"
VENDOR = "Northcourt Care Partners"
CONSULT = "Lindqvist Benefits Consulting"
TPA_OLD = "Bramwell Plan Services"
TPA_NEW = "Ellery Benefit Administrators"
PBM = "Quarrystone Rx"
STOPLOSS = "Wyecliff Life Assurance Company"

PEOPLE = {
    "requester": "Joyce Salinas",        # director of risk management and benefits
    "chair": "Deborah Johnson",          # school board chair
    "cfo": "Anthony Olsen",              # chief financial officer
    "actuary": "Michael Perry",          # consulting actuary, Lindqvist
    "vendor_lead": "Allison Santiago",   # Northcourt account lead
    "analyst": "Tiffany Barrett",        # benefits analyst
    "vendor_officer": "Phillip Alvarado",  # Northcourt chief operating officer, signs the agreement
    "vendor_analyst": "Amy Kelley",      # Northcourt clinical analytics
    "pbm_rep": "Michelle Peterson",      # Quarrystone Rx client account executive
    "carrier_officer": "Jonathan Hoffman",  # Wyecliff, vice president, stop-loss underwriting
    "superintendent": "Sandra Lopez",    # superintendent, countersigns the agreement
}

# plan design (per member, plan year 1 July to 30 June)
PLANS = {
    "PPO": dict(ded=500.0, coins=0.20, oop=3600.0, pcp_copay=25.0, spec_copay=40.0, er_copay=200.0, uc_copay=50.0,
                rx=dict(G=10.0, P=40.0, N=70.0, S=(0.20, 250.0))),
    "HDHP": dict(ded=3300.0, coins=0.10, oop=6500.0, pcp_copay=None, spec_copay=None, er_copay=None, uc_copay=None,
                 rx=None),
}
PLAN_CODE = {"PPO": "RCV-PPO", "HDHP": "RCV-HSA"}


def month_index(d):
    return (d.year - SIM_START.year) * 12 + d.month - 1


def month_start(i):
    y, m = divmod(SIM_START.month - 1 + i, 12)
    return D(SIM_START.year + y, m + 1, 1)


def month_end(i):
    return month_start(i + 1) - dt.timedelta(days=1)


N_MONTHS = month_index(SIM_END) + 1


def add_months(d, k):
    y, m = divmod(d.month - 1 + k, 12)
    return D(d.year + y, m + 1, 1)


def npi_check(base9):
    """Luhn check digit over the NPI with its 80840 prefix."""
    digits = "80840" + base9
    total = 0
    for i, ch in enumerate(reversed(digits)):
        v = int(ch)
        if i % 2 == 0:
            v *= 2
            if v > 9:
                v -= 9
        total += v
    return str((10 - total % 10) % 10)


def make_npi(base9):
    return base9 + npi_check(base9)


# ------------------------------------------------------------------ drug file (11-digit NDC, 5-4-2)
# name, ndc, quantity, allowed in mid-2025 dollars, brand/generic, specialty. Generics: quantity and price per 30
# days (scaled to the days supplied). Brands: quantity (billing units, mL for injectables) and price per fill.
DRUGS = {
    "atorvastatin": ("ATORVASTATIN CALCIUM 20 MG TAB", "16729-0045-15", 30, 15.04, "G", False),
    "metformin": ("METFORMIN HCL 500 MG TAB", "53746-0218-01", 60, 12.48, "G", False),
    "metformin_er": ("METFORMIN HCL ER 500 MG TAB", "70010-0491-01", 60, 17.92, "G", False),
    "lisinopril": ("LISINOPRIL 10 MG TAB", "68180-0980-01", 30, 9.76, "G", False),
    "losartan": ("LOSARTAN POTASSIUM 50 MG TAB", "59746-0334-90", 30, 14.24, "G", False),
    "amlodipine": ("AMLODIPINE BESYLATE 5 MG TAB", "67877-0901-90", 30, 10.24, "G", False),
    "sertraline": ("SERTRALINE HCL 50 MG TAB", "70010-0204-03", 30, 13.12, "G", False),
    "escitalopram": ("ESCITALOPRAM OXALATE 10 MG TAB", "59746-0280-30", 30, 14.56, "G", False),
    "levothyroxine": ("LEVOTHYROXINE SODIUM 50 MCG TAB", "00480-8687-98", 30, 19.68, "G", False),
    "montelukast": ("MONTELUKAST SODIUM 10 MG TAB", "65162-0732-03", 30, 16.96, "G", False),
    "omeprazole": ("OMEPRAZOLE DR 20 MG CAP", "60505-0065-00", 30, 15.52, "G", False),
    "albuterol": ("ALBUTEROL SULFATE HFA 90 MCG INH", "66993-0019-68", 8.5, 31.50, "G", False),
    "amoxicillin": ("AMOXICILLIN 500 MG CAP", "50090-1810-00", 30, 13.76, "G", False),
    "tacrolimus": ("TACROLIMUS 1 MG CAP", "00378-2046-01", 120, 182.00, "G", False),
    "ondansetron": ("ONDANSETRON HCL 4 MG TAB", "55111-0153-30", 30, 24.00, "G", False),
    "enoxaparin": ("ENOXAPARIN 40 MG/0.4 ML SYRINGE", "63323-0564-65", 4, 168.00, "G", False),
    "mycophenolate": ("MYCOPHENOLATE MOFETIL 500 MG TAB", "00054-0166-25", 120, 64.00, "G", False),
    "eliquis": ("ELIQUIS 5 MG TAB", "00003-0894-21", 60, 612.00, "B", False),
    "trelegy": ("TRELEGY ELLIPTA 100-62.5-25 MCG INH", "00173-0887-10", 1, 705.00, "B", False),
    "entresto": ("ENTRESTO 49-51 MG TAB", "00078-0777-20", 60, 688.00, "B", False),
    "jardiance": ("JARDIANCE 10 MG TAB", "00597-0152-30", 30, 598.00, "B", False),
    "lantus": ("LANTUS SOLOSTAR 100 UNIT/ML PEN", "00088-2219-05", 15, 118.00, "B", False),
    "ozempic_05": ("OZEMPIC 0.25-0.5 MG/DOSE PEN", "00169-4181-13", 3, 968.00, "B", False),
    "ozempic_1": ("OZEMPIC 1 MG/DOSE PEN", "00169-4130-13", 3, 968.00, "B", False),
    "ozempic_2": ("OZEMPIC 2 MG/DOSE PEN", "00169-4772-12", 3, 968.00, "B", False),
    "mounjaro_5": ("MOUNJARO 5 MG/0.5 ML PEN", "00002-1495-80", 2, 1052.00, "B", False),
    "mounjaro_10": ("MOUNJARO 10 MG/0.5 ML PEN", "00002-1471-80", 2, 1052.00, "B", False),
    "humira": ("HUMIRA PEN 40 MG/0.4 ML", "00074-0554-02", 0.8, 6745.00, "B", True),
    "hyrimoz": ("HYRIMOZ PEN 40 MG/0.4 ML", "61314-0473-20", 0.8, 6402.00, "B", True),
    "enbrel": ("ENBREL SURECLICK 50 MG/ML", "58406-0032-04", 4, 7410.00, "B", True),
    "stelara": ("STELARA 45 MG/0.5 ML SYRINGE", "57894-0060-03", 0.5, 24990.00, "B", True),
    "dupixent": ("DUPIXENT 300 MG/2 ML PEN", "00024-5915-02", 4, 3720.00, "B", True),
    "biktarvy": ("BIKTARVY 50-200-25 MG TAB", "61958-2501-01", 30, 4105.00, "B", True),
    "epclusa": ("EPCLUSA 400-100 MG TAB", "61958-2201-01", 28, 23100.00, "B", True),
    "mavyret": ("MAVYRET 100-40 MG TAB", "00074-2625-28", 84, 12880.00, "B", True),
    "trikafta": ("TRIKAFTA 100-50-75 MG/150 MG TAB", "51167-0331-01", 84, 25260.00, "B", True),
    "imbruvica": ("IMBRUVICA 420 MG TAB", "57962-0420-28", 28, 16210.00, "B", True),
    "ibrance": ("IBRANCE 125 MG CAP", "00069-0189-21", 21, 15120.00, "B", True),
    "xtandi": ("XTANDI 40 MG CAP", "00469-0125-99", 120, 13980.00, "B", True),
    "hemlibra": ("HEMLIBRA 105 MG/0.7 ML VIAL", "50242-0922-01", 2.8, 41800.00, "B", True),
}

# ------------------------------------------------------------------ medical code sets
ICD = {
    "well_adult": ["Z00.00", "Z00.01"], "well_child": ["Z00.129", "Z00.121"],
    "acute": ["J06.9", "J02.9", "J20.9", "H66.90", "N39.0", "R10.9", "M54.50", "M25.561", "S93.401A", "R51.9",
              "L03.115", "A08.4", "J01.90", "R05.9", "K21.9", "J30.9", "B34.9", "R53.83"],
    "er": ["R07.9", "R10.9", "S52.501A", "S01.81XA", "J18.9", "N20.0", "R55", "J45.901", "S06.0X0A", "R11.2"],
    "diabetes": ["E11.9", "E11.65", "E11.22"], "htn": ["I10"], "lipid": ["E78.5"], "asthma": ["J45.40"],
    "depression": ["F33.1", "F32.A", "F41.1"], "thyroid": ["E03.9"], "obesity": ["E66.01"],
    "esrd": ["N18.6", "Z99.2", "I12.0"], "hiv": ["B20"], "ra": ["M06.9"], "psoriasis": ["L40.0", "L40.50"],
    "crohns": ["K50.90"], "atopic": ["L20.9"], "hemophilia": ["D66"], "cf": ["E84.0"], "hepc": ["B18.2"],
    "afib": ["I48.91"], "cad": ["I25.10", "Z95.5"], "liver": ["K74.60"], "chf": ["I50.22"], "copd": ["J44.1", "J44.9"],
    "breast": ["C50.911", "C50.912"], "colon": ["C18.7"], "lung": ["C34.11"], "lymphoma": ["C83.30"],
    "cll": ["C91.10"], "prostate": ["C61"], "cancer_hx": ["Z85.3", "Z08"],
    "chemo": ["Z51.11"], "radiation": ["Z51.0"],
    "kidney_tx": ["Z94.0"], "liver_tx": ["Z94.4"],
    "preterm": ["P07.33", "P07.32", "P07.34", "P22.0"], "newborn": ["Z38.00", "Z38.01"],
    "trauma": ["S72.001A", "S82.201A", "S27.0XXA", "S32.009A", "S06.5X0A"],
    "trauma_cause": ["V43.52XA"],
    "oa_knee": ["M17.11", "M17.12"], "oa_hip": ["M16.11", "M16.12"], "jr_after": ["Z47.1"],
    "mi": ["I21.4", "I21.19"], "pregnancy": ["Z34.80", "Z3A.39", "O24.410"], "delivery": ["O80", "O82"],
    "postpartum": ["Z39.2"], "admit_misc": ["J18.9", "K35.80", "K80.20", "L03.115", "N10", "E11.10", "F33.2", "K57.32"],
    "pt": ["M54.50", "M25.561", "M75.101"],
}

# a provider directory: kind -> list of 9-digit bases (check digit added by make_npi)
PROVIDER_BASES = {
    "hospital": ["136722841", "184360211", "155498723", "102639957", "166374528"],
    "asc": ["127459832", "149915266"],
    "lab": ["130642179", "195507413"],
    "imaging": ["158247760", "119874652"],
    "primary": ["124563398", "171802934", "116659045", "193345870", "145820096", "180277348", "113906582"],
    "specialist": ["162733150", "107294468", "188650317", "134418265", "176036941", "129587704"],
    "oncology": ["150973216", "117408539"],
    "dialysis": ["143268095"],
    "behavioral": ["169940327", "128371054"],
    "therapy": ["192205668", "137766415"],
    "anesthesia": ["111854730"],
    "ambulance": ["154021866"],
    "urgent": ["181639574"],
    "obgyn": ["122957183"],
    "neonatal": ["147613972"],
    "transplant": ["133580647"],
    "postacute": ["161409283", "139752216"],
    "homehealth": ["118237764"],
}
PHARMACY_BASES = ["134279116", "178036524", "106654381", "159824037", "142290865", "121187504", "175590428"]
NCPDP_IDS = ["2431856", "2427093", "2440518", "2433701", "2419648", "2438827", "2425164"]
SPECIALTY_PHARMACY = 6
PER_FILL = ("albuterol", "enoxaparin")   # generics priced and counted per package, not per 30 days      # index of the mail-order specialty pharmacy (out of state in reality, kept simple)
