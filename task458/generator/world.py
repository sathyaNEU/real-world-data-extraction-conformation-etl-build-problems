"""task458's world: Sandhollow Health Plan, a nonprofit Medicaid managed care plan serving adults in ten eastern
Washington counties, and its 2027 Prescriber Service Award Pilot. Every parameter the generator draws from lives here.

A county qualifies for the pilot when it fails at least two of Network Policy NP-31's three standards over the contract
year July 2025 to June 2026: practising behavioral-health prescribers per 1,000 adult members with a serious mental
illness, the same per 1,000 adult members with an opioid use disorder, and the share of adult members with a serious
mental illness who saw a behavioral-health prescriber. A member's condition reaches the claims only through services
billed while they are enrolled; the farm counties' expansion adults and parents enrol and leave with the seasons, and the
farmworkers who hold those short seasonal spells have a serious mental illness or an opioid use disorder about half as
often as the members of their eligibility group who stay enrolled."""
import datetime as dt

SEED = 458
D = dt.date

ORG = "Sandhollow Health Plan"
TEAM = "Network Development"
ANALYTICS = "Network Analytics"
PEOPLE = {"director": "Cameron Joyce", "analyst": "William Guerrero", "cmo": "Charles Schmidt"}
POLICY_ID = "NP-31"
POLICY_TITLE = "Prescriber Service Area Designation"
PILOT = "Prescriber Service Award Pilot"
STATE = "WA"

WINDOW_START = D(2025, 7, 1)
WINDOW_END = D(2026, 6, 30)
AS_OF = D(2026, 11, 1)               # practice locations are read on this day
PAID_THROUGH = D(2026, 10, 31)       # the claims extract's run-out
BOARD = D(2026, 11, 19)
EXTRACT = D(2026, 11, 12)          # Network Analytics pulls the files
NPPES_MONTHLY_THRU = D(2026, 10, 11)
WEEKS = [(D(2026, 10, 12), D(2026, 10, 18)), (D(2026, 10, 19), D(2026, 10, 25)), (D(2026, 10, 26), D(2026, 11, 1)),
         (D(2026, 11, 2), D(2026, 11, 8))]
DEACT_REPORT = D(2026, 11, 10)
MONTHS = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 7)]

# NP-31's thresholds
T_SMI = 16.5      # practising prescribers per 1,000 adult members with a serious mental illness
T_OUD = 23.0      # practising prescribers per 1,000 adult members with an opioid use disorder
T_SEEN = 0.68     # share of adult members with a serious mental illness who saw a behavioral-health prescriber

# eligibility groups: code, name, prevalence of each condition among members who are not seasonal workers (each county
# and group carries its own factor around it, members.py)
GROUPS = ["DSB", "EXP", "PCR", "AGD"]
GROUP_NAME = {"DSB": "Disabled adults (SSI-related)", "EXP": "Expansion adults 19 to 64",
              "PCR": "Parents and caretaker relatives", "AGD": "Aged 65 and over"}
PREV = {"SMI": {"DSB": 0.190, "EXP": 0.060, "PCR": 0.032, "AGD": 0.045},
        "OUD": {"DSB": 0.050, "EXP": 0.055, "PCR": 0.022, "AGD": 0.010}}
# the seasonal farmworkers' prevalence relative to the other members of their county and eligibility group
RHO = {"SMI": 0.50, "OUD": 0.55}

# counties: FIPS, adult persons by group, the share of expansion and parent adults in short seasonal spells,
# practising prescribers on 1 November 2026 (NP-31's count), prescriber access (monthly rate of a prescriber visit for a
# member with a serious mental illness), each condition's prevalence relative to the group's, farm county
COUNTIES = {
    "Adams":       {"fips": "53001", "persons": {"DSB": 420, "EXP": 4100, "PCR": 1350, "AGD": 260}, "short": 0.66,
                    "prescribers": 4, "access": 0.12, "f_smi": 1.141, "f_oud": 1.207, "farm": True},
    "Benton":      {"fips": "53005", "persons": {"DSB": 2500, "EXP": 10000, "PCR": 4200, "AGD": 1300}, "short": 0.10,
                    "prescribers": 30, "access": 0.26, "f_smi": 0.959, "f_oud": 0.968, "farm": False},
    "Chelan":      {"fips": "53007", "persons": {"DSB": 1000, "EXP": 4600, "PCR": 1900, "AGD": 600}, "short": 0.14,
                    "prescribers": 12, "access": 0.23, "f_smi": 1.0265, "f_oud": 0.97, "farm": False},
    "Douglas":     {"fips": "53017", "persons": {"DSB": 640, "EXP": 2700, "PCR": 1150, "AGD": 320}, "short": 0.14,
                    "prescribers": 3, "access": 0.08, "f_smi": 1.038, "f_oud": 1.0, "farm": False},
    "Franklin":    {"fips": "53021", "persons": {"DSB": 1100, "EXP": 9200, "PCR": 3600, "AGD": 600}, "short": 0.60,
                    "prescribers": 10, "access": 0.17, "f_smi": 0.9855, "f_oud": 1.0785, "farm": True},
    "Grant":       {"fips": "53025", "persons": {"DSB": 1300, "EXP": 9600, "PCR": 3500, "AGD": 800}, "short": 0.62,
                    "prescribers": 10, "access": 0.175, "f_smi": 1.0042, "f_oud": 1.099, "farm": True},
    "Kittitas":    {"fips": "53037", "persons": {"DSB": 600, "EXP": 2400, "PCR": 800, "AGD": 300}, "short": 0.12,
                    "prescribers": 7, "access": 0.24, "f_smi": 0.9575, "f_oud": 0.8945, "farm": False},
    "Okanogan":    {"fips": "53047", "persons": {"DSB": 900, "EXP": 3600, "PCR": 1400, "AGD": 500}, "short": 0.12,
                    "prescribers": 4, "access": 0.08, "f_smi": 1.0555, "f_oud": 1.1, "farm": False},
    "Walla Walla": {"fips": "53071", "persons": {"DSB": 620, "EXP": 5200, "PCR": 1500, "AGD": 300}, "short": 0.10,
                    "prescribers": 10, "access": 0.128, "f_smi": 1.03, "f_oud": 0.983, "farm": False},
    "Yakima":      {"fips": "53077", "persons": {"DSB": 5200, "EXP": 22000, "PCR": 8800, "AGD": 2600}, "short": 0.45,
                    "prescribers": 41, "access": 0.14, "f_smi": 0.998, "f_oud": 1.1345, "farm": True},
}
ALLOC_DRAW = 0      # which draw of the exact allocation the build uses
ID_DRAW = 0         # which draw of the first-identification allocation the build uses
LAM_SMI = 0.35    # monthly rate of a service carrying a serious mental illness diagnosis (prescriber visits included)
LAM_OUD = 0.33    # monthly rate of a service carrying an opioid use disorder diagnosis
# the chance a member with the condition has a first service carrying it in any one enrolled month (the same for every
# member, whatever their county, group or spell): F(k), the share first identified within k enrolled months, follows it,
# conditioned on identification within twelve
Q_FIRST = {"SMI": 0.30, "OUD": 0.28}


def capture(cond, k):
    """F(k): the share of members with the condition enrolled k months whom a service identifies within them (a member
    enrolled all twelve months is always identified)."""
    q = Q_FIRST[cond]
    return (1 - (1 - q) ** k) / (1 - (1 - q) ** 12)
FIPS_NAME = {v["fips"]: k for k, v in COUNTIES.items()}

# ZIP codes by county (real ZIPs); a few span two counties, split by the residential and business address shares the
# plan's ZIP-county file records
ZIPS = {
    "Adams": ["99169", "99341", "99344", "99371", "99105"],
    "Benton": ["99336", "99337", "99338", "99350", "99352", "99353", "99354", "99320"],
    "Chelan": ["98801", "98815", "98816", "98826", "98828", "98831", "98847", "98822"],
    "Douglas": ["98802", "98830", "98843", "98845", "98850", "98858"],
    "Franklin": ["99301", "99326", "99330", "99335", "99343"],
    "Grant": ["98823", "98824", "98832", "98837", "98848", "98851", "98857", "99115", "99123", "99133", "99135",
              "99349", "99357"],
    "Kittitas": ["98922", "98925", "98926", "98934", "98940", "98941", "98946"],
    "Okanogan": ["98812", "98819", "98827", "98829", "98833", "98834", "98840", "98841", "98844", "98846", "98849",
                 "98855", "98856", "98862"],
    "Walla Walla": ["99324", "99328", "99329", "99348", "99360", "99361", "99362", "99363"],
    "Yakima": ["98901", "98902", "98903", "98908", "98921", "98930", "98932", "98933", "98935", "98936", "98937",
               "98938", "98942", "98944", "98947", "98948", "98951", "98952", "98953"],
}
# split ZIPs: zip -> [(county, residential share, business share)]
SPLIT = {
    "99344": [("Adams", 0.712604, 0.861357), ("Grant", 0.168231, 0.090522), ("Franklin", 0.119165, 0.048121)],
    "98813": [("Douglas", 0.583092, 0.307446), ("Okanogan", 0.416908, 0.692554)],
    "99357": [("Adams", 0.561873, 0.171952), ("Grant", 0.438127, 0.828048)],
    "98822": [("Chelan", 0.879514, 0.948211), ("Douglas", 0.120486, 0.051789)],
}
# ZIP codes with a sliver of their addresses across a county line: zip -> (other county, residential, business share)
SLIVER = {"99301": ("Benton", 0.003019, 0.001102), "98944": ("Benton", 0.005873, 0.002311),
          "99350": ("Yakima", 0.012684, 0.004927), "98848": ("Douglas", 0.007260, 0.000000),
          "98802": ("Chelan", 0.001446, 0.003871), "99362": ("Columbia", 0.000918, 0.000000)}
ZIPS["Douglas"].append("98813")
CITY = {
    "99169": "Ritzville", "99341": "Lind", "99344": "Othello", "99371": "Washtucna", "99105": "Benge",
    "99336": "Kennewick", "99337": "Kennewick", "99338": "Kennewick", "99350": "Prosser", "99352": "Richland",
    "99353": "West Richland", "99354": "Richland", "99320": "Benton City", "98801": "Wenatchee", "98815": "Cashmere",
    "98816": "Chelan", "98826": "Leavenworth", "98828": "Malaga", "98831": "Manson", "98847": "Peshastin",
    "98822": "Entiat", "98802": "East Wenatchee", "98830": "Mansfield", "98843": "Orondo", "98845": "Palisades",
    "98850": "Rock Island", "98858": "Waterville", "98813": "Bridgeport", "99301": "Pasco", "99326": "Connell",
    "99330": "Eltopia", "99335": "Kahlotus", "99343": "Mesa", "98823": "Ephrata", "98824": "George",
    "98832": "Marlin", "98837": "Moses Lake", "98848": "Quincy", "98851": "Soap Lake", "98857": "Warden",
    "99115": "Coulee City", "99123": "Electric City", "99133": "Grand Coulee", "99135": "Hartline",
    "99349": "Mattawa", "99357": "Royal City", "98922": "Cle Elum", "98925": "Easton", "98926": "Ellensburg",
    "98934": "Kittitas", "98940": "Ronald", "98941": "Roslyn", "98946": "Thorp", "98812": "Brewster",
    "98819": "Conconully", "98827": "Loomis", "98829": "Malott", "98833": "Mazama", "98834": "Methow",
    "98840": "Okanogan", "98841": "Omak", "98844": "Oroville", "98846": "Pateros", "98849": "Riverside",
    "98855": "Tonasket", "98856": "Twisp", "98862": "Winthrop", "99324": "College Place", "99328": "Dayton",
    "99329": "Dixie", "99348": "Prescott", "99360": "Touchet", "99361": "Waitsburg", "99362": "Walla Walla",
    "99363": "Wallula", "98901": "Yakima", "98902": "Yakima", "98903": "Yakima", "98908": "Yakima",
    "98921": "Buena", "98930": "Grandview", "98932": "Granger", "98933": "Harrah", "98935": "Mabton",
    "98936": "Moxee", "98937": "Naches", "98938": "Outlook", "98942": "Selah", "98944": "Sunnyside",
    "98947": "Tieton", "98948": "Toppenish", "98951": "Wapato", "98952": "White Swan", "98953": "Zillah",
}
# the ZIP's main county (the one holding most of its addresses), for ZIPs listed under a county they mainly belong to
OTHER_WA = [("Spokane", "99201"), ("Spokane", "99204"), ("Seattle", "98104"), ("Seattle", "98122"),
            ("Tacoma", "98405"), ("Everett", "98201"), ("Olympia", "98501"), ("Vancouver", "98664"),
            ("Bellevue", "98004"), ("Pullman", "99163"), ("Clarkston", "99403"), ("Ellensburg", "98926")]
OUT_OF_STATE = [("Portland", "OR", "97210"), ("Hermiston", "OR", "97838"), ("Pendleton", "OR", "97801"),
                ("Boise", "ID", "83702"), ("Lewiston", "ID", "83501"), ("Missoula", "MT", "59801")]
STREETS = ["W Yakima Ave", "N 1st St", "S 16th Ave", "W Clearwater Ave", "Columbia Center Blvd", "N Wenatchee Ave",
           "Valley Mall Pkwy", "W 4th Ave", "S Main St", "W Broadway Ave", "E Main St", "N Division St",
           "S Washington St", "Canyon Rd", "Memorial St", "W Court St", "N 20th Ave", "E Sunset Hwy", "S Alder St",
           "W Nob Hill Blvd", "N Oregon Ave", "E Lewis St", "W Pioneer Way", "Stratford Rd", "Sylvan Way"]
SUITES = ["", "", "", "Suite 100", "Suite 200", "Suite 210", "Ste 3", "Bldg B", "Suite 301", "Unit 4"]

# condition code lists (ICD-10-CM, as NP-31 lists them)
SMI_CODES = (["F20.0", "F20.1", "F20.2", "F20.3", "F20.5", "F20.81", "F20.89", "F20.9", "F21", "F22", "F25.0",
              "F25.1", "F25.8", "F25.9", "F28", "F29"] +
             ["F31.0", "F31.10", "F31.11", "F31.12", "F31.13", "F31.2", "F31.30", "F31.31", "F31.32", "F31.4",
              "F31.5", "F31.60", "F31.61", "F31.62", "F31.63", "F31.64", "F31.70", "F31.71", "F31.72", "F31.73",
              "F31.74", "F31.75", "F31.76", "F31.77", "F31.78", "F31.81", "F31.89", "F31.9", "F32.3", "F33.3"])
OUD_CODES = ["F11.10", "F11.11", "F11.120", "F11.121", "F11.122", "F11.129", "F11.13", "F11.14", "F11.150",
             "F11.151", "F11.159", "F11.181", "F11.182", "F11.188", "F11.19", "F11.20", "F11.21", "F11.220",
             "F11.221", "F11.222", "F11.229", "F11.23", "F11.24", "F11.250", "F11.251", "F11.259", "F11.281",
             "F11.282", "F11.288", "F11.29"]
# the codes the claims actually carry most (weights), and other behavioral-health codes
SMI_COMMON = [("F20.9", 6), ("F20.0", 3), ("F25.0", 3), ("F25.9", 2), ("F31.9", 5), ("F31.81", 2), ("F31.30", 1),
              ("F31.4", 1), ("F31.5", 1), ("F31.60", 1), ("F31.10", 1), ("F31.2", 1), ("F33.3", 1), ("F32.3", 1),
              ("F29", 1), ("F22", 1)]
OUD_COMMON = [("F11.20", 10), ("F11.21", 3), ("F11.23", 1), ("F11.24", 1), ("F11.10", 1), ("F11.129", 1),
              ("F11.288", 1)]
OTHER_BH = [("F32.1", 6), ("F32.A", 3), ("F33.1", 5), ("F33.2", 2), ("F41.1", 7), ("F41.9", 3), ("F43.10", 3),
            ("F43.23", 3), ("F90.0", 2), ("F10.20", 4), ("F12.20", 2), ("F15.20", 2), ("F17.210", 2), ("F11.90", 1),
            ("F60.3", 1), ("F42.2", 1), ("F31.9X", 0)]
OTHER_BH = [x for x in OTHER_BH if x[1] > 0]
GENERAL = [("Z00.00", 2), ("I10", 2), ("E11.9", 2), ("J45.909", 1), ("M54.50", 1), ("K21.9", 1), ("Z79.899", 2),
           ("G47.00", 1), ("R45.851", 1), ("Z91.19", 1)]

# behavioral-health prescriber taxonomy codes (NP-31's list) and the others NPPES carries for these clinicians
BH_TAXONOMY = {"2084P0800X": "Psychiatry & Neurology, Psychiatry", "2084P0804X": "Psychiatry & Neurology, Child & Adolescent Psychiatry",
               "2084P0802X": "Psychiatry & Neurology, Addiction Psychiatry", "2084P0805X": "Psychiatry & Neurology, Geriatric Psychiatry",
               "2084A0401X": "Psychiatry & Neurology, Addiction Medicine", "207QA0401X": "Family Medicine, Addiction Medicine",
               "207RA0401X": "Internal Medicine, Addiction Medicine", "363LP0808X": "Nurse Practitioner, Psych/Mental Health",
               "364SP0808X": "Clinical Nurse Specialist, Psych/Mental Health"}
OTHER_TAXONOMY = {"207Q00000X": "Family Medicine", "207R00000X": "Internal Medicine", "363LF0000X": "Nurse Practitioner, Family",
                  "363LA2200X": "Nurse Practitioner, Adult Health", "363A00000X": "Physician Assistant",
                  "103T00000X": "Psychologist", "101YM0800X": "Counselor, Mental Health",
                  "1041C0700X": "Social Worker, Clinical", "101YA0400X": "Counselor, Addiction (Substance Use Disorder)",
                  "207P00000X": "Emergency Medicine", "208D00000X": "General Practice"}
ORG_TAXONOMY = {"261QM0801X": "Clinic/Center, Mental Health (Including Community Mental Health Center)",
                "261QM2800X": "Clinic/Center, Methadone", "324500000X": "Substance Abuse Rehabilitation Facility",
                "261QF0400X": "Clinic/Center, Federally Qualified Health Center (FQHC)", "282N00000X": "General Acute Care Hospital"}
PRESCRIBER_MIX = [("2084P0800X", 46), ("363LP0808X", 40), ("2084P0804X", 4), ("2084P0802X", 2), ("2084A0401X", 3),
                  ("207QA0401X", 3), ("207RA0401X", 1), ("364SP0808X", 1)]
CREDENTIAL = {"2084P0800X": "MD", "2084P0804X": "MD", "2084P0802X": "MD", "2084P0805X": "MD", "2084A0401X": "DO",
              "207QA0401X": "MD", "207RA0401X": "MD", "363LP0808X": "PMHNP-BC", "364SP0808X": "APRN, CNS"}

# procedure codes
VISIT_CODES = [("99213", 5), ("99214", 9), ("99215", 2), ("90792", 2), ("99204", 1), ("99205", 1)]
ADDON = "90833"
OTHER_PROC = {"therapy": [("90834", 4), ("90837", 3), ("90832", 2), ("90847", 1)],
              "case": [("H0036", 4), ("H0039", 2), ("H2015", 2), ("T1017", 1)],
              "sud": [("H0004", 3), ("H0005", 2), ("H0020", 3), ("H0001", 1)],
              "ed": [("99283", 3), ("99284", 4), ("99285", 2)],
              "assess": [("90791", 2), ("H0031", 1)]}
FEE = {"99213": 74.5, "99214": 108.2, "99215": 146.9, "90792": 182.4, "99204": 151.6, "99205": 199.8, "90833": 71.3,
       "90834": 92.1, "90837": 135.6, "90832": 61.8, "90847": 98.7, "H0036": 41.2, "H0039": 63.5, "H2015": 22.4,
       "T1017": 27.9, "H0004": 26.6, "H0005": 39.1, "H0020": 18.9, "H0001": 112.3, "99283": 121.4, "99284": 188.6,
       "99285": 276.2, "90791": 168.4, "H0031": 88.0}


def months_of(start, end):
    """The contract-year months a coverage period touches."""
    out = []
    for y, m in MONTHS:
        first = D(y, m, 1)
        last = (D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))
        if start <= last and end >= first:
            out.append((y, m))
    return out


def npi(r):
    """A ten-digit NPI with its Luhn check digit (computed with the 80840 prefix)."""
    base = "1" + "".join(str(x) for x in r.integers(0, 10, size=8))
    digits = [int(c) for c in "80840" + base]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check = (10 - total % 10) % 10
    return base + str(check)


def first_last_pools():
    """US first and last names from the faker en_US provider (fixed order)."""
    from faker.providers.person.en_US import Provider as P
    firsts_f = list(P.first_names_female.keys()) if isinstance(P.first_names_female, dict) else list(P.first_names_female)
    firsts_m = list(P.first_names_male.keys()) if isinstance(P.first_names_male, dict) else list(P.first_names_male)
    lasts = list(P.last_names.keys()) if isinstance(P.last_names, dict) else list(P.last_names)
    persona_last = {p.split()[1] for p in PEOPLE.values()}
    persona_first = {p.split()[0] for p in PEOPLE.values()}
    lasts = [n for n in lasts if n not in persona_last and n not in ("Benton", "Douglas", "Grant", "Franklin",
                                                                     "Adams", "Chelan", "Yakima")]
    firsts_f = [n for n in firsts_f if n not in persona_first]
    firsts_m = [n for n in firsts_m if n not in persona_first]
    return firsts_f, firsts_m, lasts


def county_of_zip(z, basis="business"):
    """The county a ZIP belongs to: the county holding the larger share of its business (or residential) addresses."""
    if z in SPLIT:
        k = 2 if basis == "business" else 1
        return max(SPLIT[z], key=lambda t: t[k])[0]
    for c, zs in ZIPS.items():
        if z in zs:
            return c
    return None
