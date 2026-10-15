"""The fiction's fixed facts: Marrowfield University Health (an academic medical center in Ohio), its Office of
Research Integrity and Conflicts of Interest, the clinical faculty's departments and the July 2025 reorganisation,
Open Payments' natures of payment, the manufacturers that pay the faculty, the companies outside Open Payments,
and the dates the pack is cut on. Everything else is drawn in people.py from these."""
import datetime as dt

import numpy as np

SEED = 457_317
SPLIT_SALT = 35         # the register's record stream (natures, blank NPIs, third-party fees), chosen so no 2025 total by nature sits near a rounding edge

ORG = "Marrowfield University Health"
HOSPITAL = "Marrowfield University Hospital"
OFFICE = "Office of Research Integrity and Conflicts of Interest"
COMMITTEE = "Conflict of Interest Committee"
CITY, STATE, ZIP = "Marrowfield", "OH", "43952"
STREET = "1400 Collegiate Avenue"
CCN = "360241"
TEACHING_HOSPITAL_ID = "8231"

PEOPLE = {"director": "Karen Shea", "chair": "Herbert Dean", "analyst": "Diana Hickman"}

# dates
YEARS = list(range(2021, 2027))           # disclosure years; the register holds 2021 to 2025
REGISTER_YEARS = list(range(2021, 2026))
JUNE_PUB = dt.date(2026, 6, 30)           # first publication of program year 2025
JAN_REFRESH = dt.date(2027, 1, 15)        # the refresh every extract year carries
OP_PULL = dt.date(2027, 1, 19)            # the office's pull of the refreshed register
OP_PULL_JUNE = dt.date(2026, 7, 7)        # the office's pull of the June publication
HR_PULL = dt.date(2027, 1, 20)
COI_PULL = dt.date(2027, 1, 21)
DOCKET_DATE = dt.date(2027, 1, 27)        # the docket memo
MEETING = dt.date(2027, 2, 11)
DEADLINE_LOCAL = dt.datetime(2027, 1, 15, 23, 59, 59)  # Eastern
REORG = dt.date(2025, 7, 1)
FORM_CHANGE = 2024                        # the disclosure form's 2024 edition (years 2024 on)

# departments of the clinical faculty after the reorganisation, with their shares of the faculty
DEPTS = [
    ("ANES", "Anesthesiology", 0.085), ("CARD", "Cardiovascular Medicine", 0.058), ("DERM", "Dermatology", 0.025),
    ("EMED", "Emergency Medicine", 0.062), ("GAST", "Gastroenterology and Hepatology", 0.034),
    ("HEON", "Hematology and Oncology", 0.058), ("IMED", "Internal Medicine", 0.128), ("NEUR", "Neurology", 0.052),
    ("OBGY", "Obstetrics and Gynecology", 0.060), ("OPHT", "Ophthalmology", 0.031),
    ("ORTH", "Orthopaedic Surgery", 0.050), ("PEDS", "Pediatrics", 0.121), ("PSYC", "Psychiatry", 0.060),
    ("RADI", "Radiology", 0.070), ("SURG", "Surgery", 0.083), ("UROL", "Urology", 0.023),
]
DEPT_NAME = {c: n for c, n, _ in DEPTS}
# the Department of Medicine's divisions became departments on 1 July 2025
MED = ("MED", "Medicine")
MED_DIVISIONS = {"CARD": "CARD", "GAST": "GAST", "HEON": "HEON", "GIM": "IMED"}
DIVISION_NAME = {"CARD": "Division of Cardiovascular Medicine", "GAST": "Division of Gastroenterology and Hepatology",
                 "HEON": "Division of Hematology and Oncology", "GIM": "Division of General Internal Medicine"}
SUCCESSOR_OF = {v: k for k, v in MED_DIVISIONS.items()}       # CARD -> division CARD, IMED -> division GIM

SPECIALTY = {
    "ANES": "Allopathic & Osteopathic Physicians|Anesthesiology",
    "CARD": "Allopathic & Osteopathic Physicians|Internal Medicine|Cardiovascular Disease",
    "DERM": "Allopathic & Osteopathic Physicians|Dermatology",
    "EMED": "Allopathic & Osteopathic Physicians|Emergency Medicine",
    "GAST": "Allopathic & Osteopathic Physicians|Internal Medicine|Gastroenterology",
    "HEON": "Allopathic & Osteopathic Physicians|Internal Medicine|Hematology & Oncology",
    "IMED": "Allopathic & Osteopathic Physicians|Internal Medicine",
    "NEUR": "Allopathic & Osteopathic Physicians|Psychiatry & Neurology|Neurology",
    "OBGY": "Allopathic & Osteopathic Physicians|Obstetrics & Gynecology",
    "OPHT": "Allopathic & Osteopathic Physicians|Ophthalmology",
    "ORTH": "Allopathic & Osteopathic Physicians|Orthopaedic Surgery",
    "PEDS": "Allopathic & Osteopathic Physicians|Pediatrics",
    "PSYC": "Allopathic & Osteopathic Physicians|Psychiatry & Neurology|Psychiatry",
    "RADI": "Allopathic & Osteopathic Physicians|Radiology|Diagnostic Radiology",
    "SURG": "Allopathic & Osteopathic Physicians|Surgery",
    "UROL": "Allopathic & Osteopathic Physicians|Urology",
}
APP_SPECIALTY = {"NP": "Physician Assistants & Advanced Practice Nursing Providers|Nurse Practitioner",
                 "PA": "Physician Assistants & Advanced Practice Nursing Providers|Physician Assistant"}

# Open Payments' natures of payment; the policy's remuneration is the first five
NATURES_REMUN = [
    "Consulting Fee",
    "Compensation for services other than consulting, including serving as faculty or as a speaker at a venue other "
    "than a continuing education program",
    "Honoraria",
    "Compensation for serving as faculty or as a speaker for an accredited or certified continuing education program",
    "Compensation for serving as faculty or as a speaker for an unaccredited and non-certified continuing education "
    "program",
]
NATURE_SHORT = {NATURES_REMUN[0]: "Consulting fees", NATURES_REMUN[1]: "Services other than consulting",
                NATURES_REMUN[2]: "Honoraria", NATURES_REMUN[3]: "Accredited continuing education faculty or speaker",
                NATURES_REMUN[4]: "Unaccredited continuing education faculty or speaker"}
NATURES_OTHER = ["Food and Beverage", "Travel and Lodging", "Education", "Gift", "Royalty or License",
                 "Charitable Contribution", "Space rental or facility fees", "Entertainment"]

# the docket region's names: distinct first names and surnames, none used by an earlier build
REGION_NAMES = [
    ('Kirsten', 'Middleton'),
    ('Adam', 'Andersen'),
    ('Kyle', 'Avery'),
    ('Henry', 'Grimes'),
    ('Alexis', 'Drake'),
    ('Traci', 'Ware'),
    ('Johnathan', 'Kaiser'),
    ('Ruth', 'Rosario'),
    ('Vickie', 'Nolan'),
    ('Fernando', 'Baldwin'),
    ('Kerry', 'Leach'),
    ('Stacie', 'Black'),
    ('Pedro', 'Hampton'),
    ('Judith', 'Valenzuela'),
    ('Jillian', 'Luna'),
    ('Angelica', 'Gentry'),
    ('Cory', 'Harper'),
    ('Hector', 'Mahoney'),
    ('Carly', 'Singleton'),
    ('Melvin', 'Blackwell'),
    ('Dave', 'Horne'),
    ('Cameron', 'Sanford'),
    ('Leah', 'Armstrong'),
    ('Jasmin', 'Rosales'),
    ('Grace', 'Brooks'),
    ('Loretta', 'Cooke'),
    ('Rodney', 'Larsen'),
    ('Brent', 'Fitzgerald'),
    ('Mason', 'Hebert'),
    ('Kimberly', 'Moon'),
    ('Melissa', 'Compton'),
    ('Collin', 'Valentine'),
    ('Shirley', 'Pratt'),
    ('Michaela', 'Barber'),
    ('Dale', 'Lucas'),
    ('Ricky', 'Becker'),
    ('Suzanne', 'Ayala'),
    ('Sally', 'Duffy'),
    ('Ralph', 'Huerta'),
    ('Bryan', 'Dillon'),
    ('Lydia', 'Whitaker'),
    ('Jamie', 'Ochoa'),
    ('Gabriella', 'Krueger'),
    ('Tamara', 'Robbins'),
    ('Allen', 'Hensley'),
    ('Troy', 'Langley'),
    ('Dominic', 'Griffin'),
    ('Erica', 'Gray'),
    ('Vincent', 'Newman'),
    ('Kathryn', 'Hawkins'),
    ('Alan', 'Ayers'),
    ('Jackson', 'Sandoval'),
]

# the disclosure form's relationship types: the 2021 edition, then the 2024 edition
TYPES_2021 = ["Consulting", "Speaking", "Advisory board", "Honoraria", "Other paid services"]
TYPES_2024 = ["Consulting or advisory board", "Speaking or teaching", "Expert testimony", "Other paid services"]
TYPES_NONREMUN = ["Equity", "Royalties or licensing"]


def form_type(kind, year):
    """The relationship type a faculty member picks for a relationship of this kind on the year's form."""
    if year < FORM_CHANGE:
        return {"consulting": "Consulting", "speaking": "Speaking", "advisory": "Advisory board",
                "honoraria": "Honoraria", "other": "Other paid services", "expert": "Other paid services"}[kind]
    return {"consulting": "Consulting or advisory board", "speaking": "Speaking or teaching",
            "advisory": "Consulting or advisory board", "honoraria": "Speaking or teaching",
            "other": "Other paid services", "expert": "Expert testimony"}[kind]


# fictional manufacturers that pay the faculty: name, Open Payments ID, state, specialties they deal with
_ROOTS = ["Aldermont", "Ambrell", "Arvessa", "Aubrecht", "Belcastle", "Brannoch", "Brisbury", "Caddow", "Calbreth",
          "Carrowmore", "Castellane", "Celadine", "Cheswick", "Clevedon", "Corvane", "Crestholm", "Dalvern", "Delmora",
          "Dunmere", "Elsworth", "Farrowdale", "Fennick", "Garnell", "Halbrook", "Harrowgate", "Haverlund", "Hollinby",
          "Ilvane", "Isenbrook", "Kelward", "Lanholt", "Larkmoor", "Lorvain", "Marbeck", "Merriden", "Morvanne",
          "Norvell", "Oakhurst", "Oberline", "Pallister", "Pellion", "Penhallow", "Quarrell", "Quillon", "Ravelston",
          "Redmarsh", "Rosling", "Saltmere", "Selbourne", "Stanmere", "Tarrant", "Tessick", "Thornbury", "Torvane",
          "Trevail", "Ulverby", "Valdane", "Varrick", "Vellacott", "Wexmoor", "Whitcombe", "Wildmere", "Wyvernton",
          "Yarrowby", "Ashcombe", "Bellmoor", "Carbury", "Darrowby", "Edgerton", "Fairholt", "Glenarde", "Hartwell",
          "Inverlee", "Kirkwold", "Linmouth", "Meldrum", "Netherby", "Orwell Ridge", "Pembrey", "Rathmore",
          "Shalford", "Tolworth", "Upcott", "Vexford", "Wellsby", "Amberleigh", "Briarcombe", "Coldharbour",
          "Dornoch Vale", "Eastwick", "Foxmoor", "Greywell", "Hambledon", "Ickworth", "Kingsmere", "Lowestead",
          "Mapleton Ridge", "Northcote", "Oxenford", "Pinewold", "Quenby", "Rookhill", "Sedgemoor", "Tilbrook",
          "Underwood Vale", "Westerley", "Yelverton", "Alnmouth", "Bramling", "Charlbury", "Dinmore", "Eskdale",
          "Fallowfield", "Gransden", "Hexworth", "Kelsall", "Lindhurst", "Morland", "Netherwood", "Ormesby", "Penrose"]
_SUFFIX = {
    "CARD": ["Cardiovascular, Inc.", "Cardio Systems, Inc.", "Vascular, LLC", "Heart Technologies, Inc."],
    "ORTH": ["Orthopedics, Inc.", "Spine, LLC", "Surgical, Inc.", "Joint Technologies, Inc."],
    "HEON": ["Oncology, Inc.", "Therapeutics, Inc.", "Biologics, Inc.", "Pharmaceuticals, Inc."],
    "NEUR": ["Neuroscience, Inc.", "Neurotherapeutics, Inc.", "Pharmaceuticals, Inc."],
    "PSYC": ["Neuroscience, Inc.", "Pharmaceuticals, Inc.", "Therapeutics, Inc."],
    "GAST": ["Gastroenterology, Inc.", "Therapeutics, Inc.", "Endoscopy, Inc.", "Pharmaceuticals, Inc."],
    "DERM": ["Dermatology, Inc.", "Aesthetics, LLC", "Pharmaceuticals, Inc."],
    "OPHT": ["Ophthalmics, Inc.", "Vision, Inc.", "Eye Care, LLC"],
    "UROL": ["Urology, Inc.", "Medical, Inc.", "Pharmaceuticals, Inc."],
    "IMED": ["Pharmaceuticals, Inc.", "Therapeutics, Inc.", "Biosciences, Inc.", "Health, Inc."],
    "OBGY": ["Women's Health, Inc.", "Pharmaceuticals, Inc.", "Medical, Inc."],
    "ANES": ["Medical, Inc.", "Anesthesia Systems, LLC", "Pharmaceuticals, Inc."],
    "RADI": ["Imaging, Inc.", "Diagnostics, Inc.", "Medical Systems, Inc."],
    "SURG": ["Surgical, Inc.", "Medical, Inc.", "Wound Care, LLC"],
    "PEDS": ["Pharmaceuticals, Inc.", "Biologics, Inc.", "Therapeutics, Inc."],
    "EMED": ["Medical, Inc.", "Pharmaceuticals, Inc."],
}
_MFR_STATES = ["NJ", "NJ", "NJ", "PA", "PA", "MA", "MA", "MA", "CA", "CA", "CA", "MN", "MN", "IN", "IL", "NC", "NY",
               "TX", "OH", "OH", "CT", "DE", "FL", "TN", "GA", "CO", "WA", "UT", "MD", "MI"]


def manufacturers():
    """About 120 fictional applicable manufacturers: (id, name, state, departments served). Each holds its Open
    Payments ID for good; three were renamed in early 2025 (RENAMED)."""
    r = np.random.default_rng([SEED, 1])
    out = []
    used = set()
    depts = [c for c, _, _ in DEPTS]
    weights = np.array([1.0, 2.2, 0.9, 0.5, 1.2, 2.0, 1.6, 1.6, 0.9, 0.9, 2.2, 1.0, 1.3, 0.7, 1.3, 0.9])
    weights = weights / weights.sum()
    ids = 100000000000 + np.cumsum(r.integers(17, 2900, size=len(_ROOTS)))
    for k, root in enumerate(_ROOTS):
        d1 = depts[r.choice(len(depts), p=weights)]
        d2 = depts[r.choice(len(depts), p=weights)]
        suf = _SUFFIX[d1][r.integers(len(_SUFFIX[d1]))]
        name = "%s %s" % (root, suf)
        if name in used:
            continue
        used.add(name)
        out.append({"id": "%d" % ids[k], "name": name, "state": _MFR_STATES[r.integers(len(_MFR_STATES))],
                    "depts": sorted({d1, d2}), "primary": d1, "index": len(out)})
    nid = int(ids[-1])
    for k, name in enumerate(NOW_REPORTING):
        nid += int(r.integers(4000, 9000))
        out.append({"id": "%d" % nid, "name": name, "state": NOW_REPORTING_STATE[name],
                    "depts": ["NEUR", "PSYC"] if k == 0 else ["GAST", "HEON"], "primary": "PSYC" if k == 0 else "HEON",
                    "index": len(out), "now_reporting": True})
    pr = np.random.default_rng([SEED, 1, 1])
    for m in out:
        m["products"] = products(m, pr)
    return out


# manufacturers renamed in early 2025, their Open Payments IDs kept: index into manufacturers() -> former root
RENAMED = {8: "Westmarch", 21: "Corriedale", 49: "Dunraven"}


def former_name(m):
    """The name a renamed manufacturer carried before RENAMED_ON: its former root and its present suffix."""
    k = m["index"]
    return "%s %s" % (RENAMED[k], m["name"].split(" ", 1)[1]) if k in RENAMED else m["name"]


RENAMED_ON = dt.date(2025, 3, 1)

# companies that pay faculty and do not report to Open Payments (no covered product): name, kind
NONREPORTING = [
    ("Lumenset Health, Inc.", "consulting"), ("Brightwater Expert Network, LLC", "consulting"),
    ("Halden Clinical Insights, LLC", "consulting"), ("Pemberton Vail LLP", "expert"), ("Ashgrove & Rook LLP", "expert"),
    ("Northwake Capital Partners", "advisory"), ("Stillwater Care Analytics, Inc.", "advisory"),
    ("Tidewell Virtual Care, Inc.", "consulting"), ("Corran Medical Education, LLC", "speaking"),
    ("Fernbrook Health Ventures", "advisory"), ("Merrow Lane Publishing", "other"),
    ("Granary Point Advisors", "consulting"), ("Ellison Ward Medical-Legal Consulting", "expert"),
]

# companies the office's list has carried since 2022 as companies outside Open Payments (faculty disclosed equity in
# them), which became applicable manufacturers when a product was cleared and reported to Open Payments from program
# year 2025; their paid work with the faculty began in 2026
NOW_REPORTING = ["Quorvia Digital Therapeutics, Inc.", "Kilnworth Genomics, Inc."]
# Quorvia was Somnalis Health, Inc. until early 2026: it reported program year 2025 under that name, and the office
# renamed its entry on the list when faculty first named it as Quorvia
NOW_REPORTING_FORMER = {"Quorvia Digital Therapeutics, Inc.": "Somnalis Health, Inc."}
NOW_REPORTING_RENAMED_ON = dt.date(2026, 3, 2)
NOW_REPORTING_LINES = [
    ("Quorvia Digital Therapeutics, Inc.", "advisory", 4500, 8500),
    ("Quorvia Digital Therapeutics, Inc.", "consulting", 3500, 7000),
    ("Quorvia Digital Therapeutics, Inc.", "speaking", 2500, 6000),
    ("Quorvia Digital Therapeutics, Inc.", "speaking", 2000, 4500),
    ("Quorvia Digital Therapeutics, Inc.", "expert", 5000, 9000),
    ("Quorvia Digital Therapeutics, Inc.", "other", 1800, 4000),
    ("Kilnworth Genomics, Inc.", "consulting", 4000, 9000),
    ("Kilnworth Genomics, Inc.", "speaking", 2000, 5000),
]
NOW_REPORTING_STATE = {"Quorvia Digital Therapeutics, Inc.": "MA", "Kilnworth Genomics, Inc.": "OH"}

# the clinical departments' practice addresses (what manufacturers report as the business address)
CAMPUS = {"CARD": ("1460 Collegiate Avenue", "43952"), "ORTH": ("2215 Mercer Road", "43954"),
          "HEON": ("1520 Collegiate Avenue", "43952"), "NEUR": ("1400 Collegiate Avenue", "43952"),
          "GAST": ("1400 Collegiate Avenue", "43952"), "DERM": ("380 Larch Street", "43951"),
          "OPHT": ("1101 Linden Park Drive", "43954"), "UROL": ("2215 Mercer Road", "43954"),
          "PSYC": ("640 Wexley Avenue", "43951"), "IMED": ("1400 Collegiate Avenue", "43952"),
          "ANES": ("1400 Collegiate Avenue", "43952"), "EMED": ("1400 Collegiate Avenue", "43952"),
          "OBGY": ("1555 Collegiate Avenue", "43952"), "PEDS": ("900 Orchard Hill Road", "43953"),
          "RADI": ("1400 Collegiate Avenue", "43952"), "SURG": ("1400 Collegiate Avenue", "43952")}
SUITES = ["", "", "", "Suite 200", "Suite 310", "Suite 4100", "Floor 3", "Suite 120", "Building B"]

# product names: drugs and biologics take one coined word, devices a coined word and a system noun
_SYL_A = ["Vel", "Ost", "Car", "Neu", "Zyl", "Tre", "Lor", "Ami", "Bel", "Cor", "Dex", "Ely", "Fen", "Gal", "Hal",
          "Ilo", "Jen", "Kal", "Lum", "Mer", "Nov", "Ory", "Pra", "Qui", "Rel", "Sor", "Tav", "Ulo", "Val", "Xel", "Zen",
          "Ar", "Bri", "Cel", "Dar", "Eva", "Fil", "Gly", "Hep", "Iso", "Ket", "Lev", "Mon", "Nex", "Opt", "Pel"]
_SYL_B = ["a", "e", "i", "o", "u", "ar", "en", "ix", "or", "an", "il", "ev", "um", "es"]
_SYL_C = ["tra", "vex", "zia", "lon", "dex", "pra", "rin", "max", "fen", "tis", "lix", "vant", "zor", "mira", "sta",
          "quel", "dra", "vo", "zen", "ria", "tor", "lyn", "cept", "mab"]
_DEV_A = ["Arc", "Stride", "Pulse", "Core", "Flex", "Vista", "Axis", "Clear", "True", "Keel", "Span", "Halo", "Crest",
          "Pivot", "Tandem", "Summit", "Meridian", "Beacon", "Anchor", "Lumen"]
_DEV_B = ["flex", "link", "guard", "line", "path", "loc", "fix", "view", "form", "lite", "sure", "grip"]
_DEV_C = ["System", "System", "Implant", "Catheter", "Stent", "Lens", "Monitor", "Device", "Platform"]


OWN_PRODUCTS = {"Quorvia Digital Therapeutics, Inc.": [("Somnara", "Device")],
                "Kilnworth Genomics, Inc.": [("KilnSeq Tumor Panel", "Device")]}


def _join(*parts):
    out = parts[0]
    for p in parts[1:]:
        if out[-1] in "aeiou" and p[0] in "aeiou":
            p = p[1:]
        out += p
    return out


def products(m, r):
    """Two or three product names for a manufacturer, by its kind."""
    if m["name"] in OWN_PRODUCTS:
        return OWN_PRODUCTS[m["name"]]
    bio = "Biologics" in m["name"]
    drug = bio or any(w in m["name"] for w in ("Pharmaceuticals", "Therapeutics", "Oncology", "Neuroscience",
                                               "Neurotherapeutics", "Biosciences", "Women's Health"))
    out = []
    for _ in range(int(r.integers(2, 4))):
        if drug:
            ends = ["mab", "cept"] if bio else [s for s in _SYL_C if s not in ("mab", "cept")]
            nm = _join(_SYL_A[int(r.integers(len(_SYL_A)))].lower(), _SYL_B[int(r.integers(len(_SYL_B)))],
                       ends[int(r.integers(len(ends)))]).capitalize()
            out.append((nm, "Biological" if bio else "Drug"))
        else:
            nm = _DEV_A[int(r.integers(len(_DEV_A)))] + _DEV_B[int(r.integers(len(_DEV_B)))]
            out.append(("%s %s" % (nm, _DEV_C[int(r.integers(len(_DEV_C)))]), "Device"))
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
    swap = {"Shea": "Sheehan", "Hickman": "Hickey", "Dean": "Deaton"}       # the personas' surnames stay theirs

    def fix(n):
        n = swap.get(n, n)
        if n.startswith("Mc") and len(n) > 2:
            n = "Mc" + n[2].upper() + n[3:]
        return n
    return sorted(set(firsts_f)), sorted(set(firsts_m)), [fix(n) for n in sorted(set(lasts))]
