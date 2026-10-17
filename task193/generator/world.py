"""Laegemiddeltilsynet's 2026Q3 signal run: the fixed world behind the assessment desk's list."""
import datetime as dt

SEED = 193
AS_OF = dt.date(2026, 10, 8)              # the extract was pulled
TRIAGE = dt.date(2026, 10, 12)            # the desk's next triage
Q_FROM = dt.date(2026, 7, 1)              # the run's window, on receipt date
Q_TO = dt.date(2026, 9, 30)
DICT_REVISION = dt.date(2026, 7, 20)      # the July revision of the reaction dictionary
TRANSFER = dt.date(2026, 8, 17)           # the licence transfer that renamed a product
CAPACITY = 16                             # assessments the desk can run next quarter
CODED_BY = dt.date(2026, 10, 7)           # the backlog was cleared the day before the pull

AGENCY = "Laegemiddeltilsynet"
PEOPLE = {"coordinator": "Cirkeline Gregersen",   # signal assessment coordinator
          "ingest": "Malthe Danielsen"}           # case processing lead

# the standard's criteria
PRR_MIN = 2.0
CHI_MIN = 4.0
N_MIN = 15

BG_SCALE = 1.75          # reports name two or three reactions, so the marginal rates scale together
CHANNELS = ["clinician", "licence holder", "patient", "pharmacy"]
REGIONS = ["Hovedstaden", "Midtjylland", "Nordjylland", "Sjaelland", "Syddanmark"]
AGE_BANDS = ["0 to 17", "18 to 39", "40 to 64", "65 and over"]
REPORTERS = ["physician", "nurse", "pharmacist", "patient", "other health professional"]

# the 26 preferred terms the run reads, with the share of ordinary reports naming each, and
# whether the dictionary marks it serious
REACTIONS = [
    ("Pyrexia", .072, False), ("Headache", .094, False), ("Fatigue", .086, False),
    ("Myalgia", .050, False), ("Injection site pain", .016, False),
    ("Lymphadenopathy", .010, True), ("Nausea", .076, False), ("Dizziness", .059, False),
    ("Rash", .053, False), ("Pruritus", .036, False), ("Urticaria", .022, False),
    ("Diarrhoea", .044, False), ("Vomiting", .032, False), ("Abdominal pain", .038, False),
    ("Arthralgia", .030, False), ("Paraesthesia", .016, False), ("Syncope", .012, True),
    ("Palpitations", .018, False), ("Hypertension", .014, False), ("Tachycardia", .011, False),
    ("Dyspnoea", .024, True), ("Alopecia", .010, False), ("Dry mouth", .015, False),
    ("Insomnia", .021, False), ("Hepatic enzyme increased", .013, True),
    ("Thrombocytopenia", .006, True),
]
# the reactions the booster's own reactogenicity floods
CAMPAIGN = {"Pyrexia": .460, "Headache": .520, "Fatigue": .500, "Myalgia": .400,
            "Injection site pain": .330, "Lymphadenopathy": .130}

# the dominant product: an autumn 2026 booster given through the regional campaign
DOMINANT = "DK-7120"
DOM_NAME = "Vaxelva"
DOM_REPORTS = 3010

# (code, name, licence holder, ATC, reports, {reaction: rate})
# the four pairs the booster hides sit on Headache, Pyrexia, Myalgia and Fatigue
PRODUCTS = [
    ("DK-1043", "Doranzil", "Aurelind Pharma A/S", "L04AB", 452, {"Hepatic enzyme increased": .092}),
    ("DK-1118", "Keltaprin", "Brynholm Laegemidler ApS", "N06AX", 398, {"Headache": .492}),
    ("DK-1204", "Serovane", "Castellan Nordic A/S", "C09AA", 352, {"Fatigue": .466}),
    ("DK-1266", "Imbracor", "Aurelind Pharma A/S", "B01AC", 318, {"Thrombocytopenia": .062}),
    ("DK-1331", "Noralvex", "Dalberg Therapeutics A/S", "J01MA", 286, {"Pyrexia": .390}),
    ("DK-1407", "Thelbarin", "Brynholm Laegemidler ApS", "R06AX", 262, {"Urticaria": .105}),
    ("DK-1462", "Ravistan", "Elvershoj Biotek A/S", "M01AE", 248, {"Myalgia": .320}),
    ("DK-1519", "Culavret", "Castellan Nordic A/S", "A10BJ", 232, {"Nausea": .330}),
    ("DK-1588", "Mestoran", "Fjeldgaard Pharma A/S", "A02BC", 214, {"Diarrhoea": .210}),
    ("DK-1634", "Ardelpha", "Dalberg Therapeutics A/S", "N05AH", 198, {"Dizziness": .270}),
    ("DK-1702", "Pelgorane", "Elvershoj Biotek A/S", "L01XE", 182, {"Alopecia": .115}),
    ("DK-1775", "Vintorel", "Granvig Medical A/S", "J05AE", 168, {"Rash": .250}),
    ("DK-1813", "Hestramyl", "Fjeldgaard Pharma A/S", "C07AB", 154, {"Syncope": .110}),
    ("DK-1869", "Quorendal", "Granvig Medical A/S", "H03AA", 142, {"Arthralgia": .135}),
    ("DK-1924", "Brazivane", "Hvidsten Laboratorier A/S", "C01BD", 131, {"Palpitations": .125}),
    ("DK-1987", "Oskelvin", "Dalberg Therapeutics A/S", "D07AC", 120, {}),
    ("DK-2041", "Tandrevil", "Elvershoj Biotek A/S", "N03AX", 112, {}),
    ("DK-2108", "Lirmantol", "Hvidsten Laboratorier A/S", "N06AB", 104, {}),
    ("DK-2163", "Jervanex", "Aurelind Pharma A/S", "G04CA", 96, {}),
    ("DK-2217", "Welnoprid", "Brynholm Laegemidler ApS", "A03FA", 88, {}),
    ("DK-2284", "Carvistol", "Castellan Nordic A/S", "C08CA", 80, {}),
    ("DK-2339", "Ebrantil", "Fjeldgaard Pharma A/S", "M05BA", 72, {}),
    ("DK-2401", "Marvelind", "Granvig Medical A/S", "S01EC", 64, {}),
]
# the product renamed when its licence transferred inside the quarter
RENAMED = ("DK-1702", "Pelgorane", "Pelgorane Nordic", "Elvershoj Biotek A/S", "Kvistgaard Onkologi A/S")

HOLDERS = sorted(set(p[2] for p in PRODUCTS))
# the two verbatim terms the July revision merged into one preferred term
MERGED = ("Tiredness", "Lassitude", "Fatigue")

# the reactions each product's own product information already describes, which paragraph 3.3 keeps
# out of the run. The booster's six are its known reactogenicity.
LISTED = {
    "DK-7120": ["Pyrexia", "Headache", "Fatigue", "Myalgia", "Injection site pain", "Lymphadenopathy"],
    "DK-1043": ["Nausea", "Diarrhoea", "Fatigue"],
    "DK-1118": ["Insomnia", "Dry mouth", "Nausea"],
    "DK-1204": ["Dizziness", "Headache", "Hypertension"],
    "DK-1266": ["Pruritus", "Rash"],
    "DK-1331": ["Diarrhoea", "Nausea", "Rash"],
    "DK-1407": ["Fatigue", "Dry mouth"],
    "DK-1462": ["Abdominal pain", "Nausea", "Dyspnoea"],
    "DK-1519": ["Diarrhoea", "Vomiting", "Abdominal pain"],
    "DK-1588": ["Headache", "Nausea"],
    "DK-1634": ["Insomnia", "Dry mouth", "Fatigue"],
    "DK-1702": ["Nausea", "Vomiting", "Fatigue", "Myalgia"],
    "DK-1775": ["Headache", "Nausea", "Fatigue"],
    "DK-1813": ["Fatigue", "Dizziness", "Palpitations"],
    "DK-1869": ["Insomnia", "Palpitations", "Pyrexia"],
    "DK-1924": ["Dizziness", "Headache"],
    "DK-1987": ["Pruritus", "Rash", "Urticaria"],
    "DK-2041": ["Dizziness", "Fatigue", "Paraesthesia"],
    "DK-2108": ["Insomnia", "Dry mouth", "Headache"],
    "DK-2163": ["Dizziness", "Dry mouth"],
    "DK-2217": ["Diarrhoea", "Dry mouth"],
    "DK-2284": ["Headache", "Dizziness", "Pyrexia"],
    "DK-2339": ["Arthralgia", "Myalgia", "Abdominal pain"],
    "DK-2401": ["Pruritus", "Dry mouth"],
}
