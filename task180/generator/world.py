"""The fixed world of task180: the Agency's pharmacovigilance unit, the six medicines and their packages, the
registry calendar, the hospital departments, the people and every rate the simulation draws from. Each value
here is a choice the fiction made, not a figure the data gave."""
import datetime as dt
import hashlib

import numpy as np

SEED = 1802026

EPOCH = dt.date(2018, 1, 1)            # first day of the extract
END = dt.date(2026, 6, 30)             # last day of registry data in the extract
LPR3_START = dt.date(2019, 2, 4)       # the patient registry records contacts (LPR3) from this date
CODE_CHANGE = dt.date(2024, 1, 1)      # corinurad moves from its provisional M04AX07 to M04AB09
EXTRACT_DELIVERED = dt.date(2026, 9, 4)
SCREEN_RUN = dt.date(2026, 10, 6)
REQUEST = dt.date(2026, 10, 12)
COMMITTEE = dt.date(2026, 10, 22)
PREV_COMMITTEE = dt.date(2026, 7, 9)
NOTE_DATE = dt.date(2026, 10, 16)
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))


def day(d):
    return (d - EPOCH).days


def date_of(n):
    return EPOCH + dt.timedelta(days=int(n))


D_END = day(END)
D_LPR3 = day(LPR3_START)
D_CODE = day(CODE_CHANGE)

# ------------------------------------------------------------------ the Danish calendar
EASTER = {2016: (3, 27), 2017: (4, 16), 2018: (4, 1), 2019: (4, 21), 2020: (4, 12), 2021: (4, 4), 2022: (4, 17),
          2023: (4, 9), 2024: (3, 31), 2025: (4, 20), 2026: (4, 5), 2027: (3, 28)}


def _holidays():
    """Public holidays on which pharmacies close (duty pharmacies apart): New Year, Maundy Thursday to Easter Monday,
    Great Prayer Day (abolished from 2024), Ascension, Whitsun, Christmas Eve to Boxing Day."""
    out = set()
    for y, (m, d0) in EASTER.items():
        e = day(dt.date(y, m, d0))
        out |= {e - 3, e - 2, e, e + 1, e + 39, e + 49, e + 50}
        if y <= 2023:
            out.add(e + 26)
        out |= {day(dt.date(y, 1, 1)), day(dt.date(y, 12, 24)), day(dt.date(y, 12, 25)), day(dt.date(y, 12, 26))}
    return np.array(sorted(out), np.int64)


HOLIDAYS = _holidays()


def closed(days):
    """Sundays and public holidays (1 January 2018 was a Monday)."""
    days = np.asarray(days, np.int64)
    return (days % 7 == 6) | np.isin(days, HOLIDAYS)


def next_weekday(days):
    """The day itself if it is a working day (Monday to Friday, not a holiday), else the next one."""
    d = np.asarray(days, np.int64).copy()
    need = closed(d) | (d % 7 == 5)
    for _ in range(8):
        d = np.where(need, d + 1, d)
        need = need & (closed(d) | (d % 7 == 5))
    return d


def pharmacy_days(days, stream):
    """Move dispensing days onto days a pharmacy serves them: a Sunday or holiday goes to one of the next working
    days (a duty pharmacy serves a few on the day), and part of the Saturday trade comes early in the next week."""
    d = np.asarray(days, np.int64).copy()
    r = rng("pharmacy days", stream)
    u, u2, u3 = r.random(len(d)), r.random(len(d)), r.random(len(d))
    shut = closed(d) & (u < 0.93)
    sat = ~closed(d) & (d % 7 == 5) & (u < 0.4)
    off = np.where(shut, np.where(u2 < 0.45, 1, np.where(u2 < 0.75, 2, 3)), 0)
    off = np.where(sat, np.where(u3 < 0.5, 2, 3), off)
    d = d + off
    need = (shut | sat) & closed(d)
    for _ in range(8):
        d = np.where(need, d + 1, d)
        need = need & closed(d)
    return d


PEOPLE = {
    "head": "Helge Jørgensen",          # head of the pharmacovigilance unit, the requester
    "data": "Janni Nielsen",            # registry data manager, wrote the extract notes
    "assessor": "Frida Clausen",        # signal assessor, owner of SOP-PV-14
    "secretary": "Kåre Holst",          # secretary to the medicines safety committee
    "epi": "Iben Pedersen",             # pharmacoepidemiologist, author of the note
    "medical": "Esben Olesen",          # medical assessor
}
AGENCY = "the Agency"
UNIT = "Pharmacovigilance Unit"
COMMITTEE_NAME = "Medicines Safety Committee"
MAH = "Halvmåne Pharma A/S"


def rng(*names):
    """One random stream per component, so a change in one component never re-rolls another."""
    h = hashlib.sha256(("%d:" % SEED + ":".join(str(n) for n in names)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ------------------------------------------------------------------ medicines and packages
# substance -> (brand, ATC codes with validity, launch, daily dose in units of the package strength)
SUBSTANCES = {
    "tasorexant": dict(brand="Somnevo", launch=dt.date(2022, 2, 1), codes=[("N05CJ05", dt.date(2022, 2, 1), None)],
                       ddd=50.0, ddd_unit="mg", route="O", group="Hypnotics and sedatives, orexin receptor antagonists"),
    "corinurad": dict(brand="Uralexa", launch=dt.date(2021, 11, 1),
                      codes=[("M04AX07", dt.date(2021, 11, 1), dt.date(2023, 12, 31)), ("M04AB09", CODE_CHANGE, None)],
                      ddd=200.0, ddd_unit="mg", route="O", group="Preparations increasing uric acid excretion"),
    "velaglutide": dict(brand="Gravera", launch=dt.date(2022, 4, 1), codes=[("A10BJ09", dt.date(2022, 4, 1), None)],
                        ddd=0.3, ddd_unit="mg", route="P", group="Glucagon-like peptide-1 (GLP-1) analogues"),
    "zopiclone": dict(brand=None, launch=None, codes=[("N05CF01", None, None)], ddd=7.5, ddd_unit="mg", route="O",
                      group="Benzodiazepine related drugs"),
    "allopurinol": dict(brand=None, launch=None, codes=[("M04AA01", None, None)], ddd=400.0, ddd_unit="mg", route="O",
                        group="Preparations inhibiting uric acid production"),
    "orlistat": dict(brand=None, launch=None, codes=[("A08AB01", None, None)], ddd=360.0, ddd_unit="mg", route="O",
                     group="Peripherally acting antiobesity products"),
}
NEW = ("tasorexant", "corinurad", "velaglutide")
ACTIVE = {"tasorexant": "zopiclone", "corinurad": "allopurinol", "velaglutide": "orlistat"}
EVENT_OF = {"tasorexant": "fall", "corinurad": "aki", "velaglutide": "pancreatitis"}

# vnr, substance, strength, unit, pack size (units), days one package lasts at the usual dose
PACKAGES = [
    ("412087", "tasorexant", 25, "mg", 30, 30), ("412098", "tasorexant", 50, "mg", 30, 30),
    ("186311", "corinurad", 100, "mg", 30, 15), ("186322", "corinurad", 200, "mg", 30, 30),
    ("186333", "corinurad", 200, "mg", 90, 90),
    ("503318", "velaglutide", 0.25, "mg", 4, 28), ("503329", "velaglutide", 0.5, "mg", 4, 28),
    ("503330", "velaglutide", 1.0, "mg", 4, 28), ("503341", "velaglutide", 1.7, "mg", 4, 28),
    ("503352", "velaglutide", 2.4, "mg", 4, 28),
    ("027516", "zopiclone", 7.5, "mg", 10, 10), ("027527", "zopiclone", 7.5, "mg", 30, 30),
    ("027538", "zopiclone", 3.75, "mg", 30, 30),
    ("054712", "allopurinol", 100, "mg", 100, 50), ("054723", "allopurinol", 300, "mg", 100, 100),
    ("093245", "orlistat", 120, "mg", 84, 28),
    ("115034", "ibuprofen", 400, "mg", 100, 33), ("115045", "ibuprofen", 600, "mg", 100, 50),
    ("118216", "naproxen", 500, "mg", 50, 25), ("111528", "diclofenac", 50, "mg", 100, 33),
    ("129437", "celecoxib", 200, "mg", 30, 30), ("131648", "etoricoxib", 90, "mg", 28, 28),
]
NSAIDS = {"ibuprofen": ("M01AE01", 1200.0), "naproxen": ("M01AE02", 500.0), "diclofenac": ("M01AB05", 100.0),
          "celecoxib": ("M01AH01", 200.0), "etoricoxib": ("M01AH05", 60.0)}
NSAID_PACKS = {"ibuprofen": ["115034", "115045"], "naproxen": ["118216"], "diclofenac": ["111528"],
               "celecoxib": ["129437"], "etoricoxib": ["131648"]}
NSAID_WEIGHTS = {"ibuprofen": 0.46, "naproxen": 0.2, "diclofenac": 0.12, "celecoxib": 0.12, "etoricoxib": 0.10}
PACK = {p[0]: dict(vnr=p[0], substance=p[1], strength=p[2], unit=p[3], size=p[4], days=p[5]) for p in PACKAGES}


def atc_on(substance, d):
    """The ATC code the prescription registry carries for a dispensing of the substance on day d."""
    if substance == "corinurad":
        return "M04AX07" if d < D_CODE else "M04AB09"
    if substance in NSAIDS:
        return NSAIDS[substance][0]
    return SUBSTANCES[substance]["codes"][0][0]


def ddd_per_pack(vnr):
    p = PACK[vnr]
    s = p["substance"]
    ddd = SUBSTANCES[s]["ddd"] if s in SUBSTANCES else NSAIDS[s][1]
    return p["strength"] * p["size"] / ddd


# ------------------------------------------------------------------ cohorts
# n: persons with a first dispensing; ages at the start; uptake by year (relative); latent multipliers
COHORTS = {
    "tasorexant": dict(n=16873, age=(74.5, 8.0, 50, 97), female=0.63,
                       uptake={2022: 0.55, 2023: 0.95, 2024: 1.08, 2025: 1.05, 2026: 1.0}),
    "zopiclone": dict(n=33962, age=(72.0, 10.5, 40, 97), female=0.6,
                      uptake={2022: 1.0, 2023: 1.0, 2024: 0.97, 2025: 0.95, 2026: 0.93}),
    "corinurad": dict(n=57841, age=(67.0, 10.0, 35, 95), female=0.17,
                      uptake={2021: 0.55, 2022: 0.9, 2023: 1.04, 2024: 1.08, 2025: 1.03, 2026: 1.0}),
    "allopurinol": dict(n=29118, age=(68.0, 10.5, 35, 96), female=0.22,
                        uptake={2022: 1.0, 2023: 0.97, 2024: 0.93, 2025: 0.9, 2026: 0.9}),
    "velaglutide": dict(n=73688, age=(51.0, 11.0, 20, 85), female=0.66,
                        uptake={2022: 0.08, 2023: 0.25, 2024: 0.75, 2025: 1.8, 2026: 2.6}),
    "orlistat": dict(n=74231, age=(49.0, 11.5, 20, 85), female=0.70,
                     uptake={2022: 1.0, 2023: 0.95, 2024: 0.9, 2025: 0.85, 2026: 0.82}),
}
COMPARATOR_PER_USER = 2

# latent multipliers on each event rate (gamma, mean, shape); never a column anywhere
LATENT = {
    "tasorexant": dict(fall=3.18, aki=1.05, pancreatitis=1.0),
    "zopiclone": dict(fall=1.66, aki=1.0, pancreatitis=1.0),
    "corinurad": dict(fall=1.05, aki=0.59, pancreatitis=1.05),
    "allopurinol": dict(fall=1.1, aki=1.17, pancreatitis=1.05),
    "velaglutide": dict(fall=0.95, aki=0.9, pancreatitis=1.36),
    "orlistat": dict(fall=0.95, aki=0.9, pancreatitis=1.46),
    "comparator": dict(fall=1.0, aki=1.0, pancreatitis=1.0),
}
LATENT_SHAPE = dict(fall=3.0, aki=8.0, pancreatitis=4.0)

# ------------------------------------------------------------------ recorded conditions
# name: (prevalence at 70 in the general population, age slope, female factor, codes, specialty)
CONDITIONS = {
    "mi": (0.06, 0.04, 0.5, ["DI219", "DI214", "DI252"], "Kardiologi"),
    "chf": (0.055, 0.06, 0.8, ["DI500", "DI509", "DI110"], "Kardiologi"),
    "pvd": (0.035, 0.05, 0.7, ["DI702", "DI739"], "Karkirurgi"),
    "stroke": (0.065, 0.06, 0.9, ["DI639", "DI619", "DG459"], "Neurologi"),
    "dementia": (0.03, 0.12, 1.2, ["DF009", "DF019", "DG309", "DF039"], "Geriatri"),
    "copd": (0.075, 0.03, 1.0, ["DJ449", "DJ441", "DJ459"], "Lungemedicin"),
    "ctd": (0.025, 0.02, 2.0, ["DM059", "DM069", "DM353"], "Reumatologi"),
    "ulcer": (0.022, 0.02, 0.8, ["DK259", "DK269"], "Mave- og tarmkirurgi"),
    "liver": (0.018, 0.0, 0.7, ["DK700", "DK760", "DB182"], "Hepatologi"),
    "diabetes": (0.12, 0.02, 0.8, ["DE119", "DE109", "DE110"], "Endokrinologi"),
    "diabcomp": (0.04, 0.02, 0.8, ["DE112", "DE113", "DE115"], "Endokrinologi"),
    "ckd": (0.04, 0.07, 0.9, ["DN183", "DN184", "DN189"], "Nefrologi"),
    "cancer": (0.11, 0.03, 0.9, ["DC189", "DC509", "DC619", "DC349", "DC449"], "Onkologi"),
    "hypertension": (0.28, 0.03, 0.95, ["DI109"], "Intern medicin"),
    "osteoporosis": (0.035, 0.06, 2.8, ["DM819", "DM800"], "Endokrinologi"),
    "parkinson": (0.012, 0.08, 0.7, ["DG209"], "Neurologi"),
    "depression": (0.05, -0.01, 1.6, ["DF329", "DF331"], "Psykiatri"),
    "alcohol": (0.025, -0.02, 0.35, ["DF102", "DF101"], "Intern medicin"),
    "gallstones": (0.045, 0.02, 1.7, ["DK802", "DK800"], "Mave- og tarmkirurgi"),
    "obesity": (0.035, -0.015, 1.3, ["DE669", "DE668"], "Endokrinologi"),
    "af": (0.075, 0.06, 0.8, ["DI489", "DI481"], "Kardiologi"),
    "gout": (0.02, 0.02, 0.3, ["DM109", "DM100"], "Reumatologi"),
    "insomnia": (0.01, 0.0, 1.3, ["DG470", "DF510"], "Neurologi"),
}
COND_NAMES = list(CONDITIONS)

# prevalence multipliers in each cohort against the general population of the same age and sex
COHORT_COND = {
    "tasorexant": dict(dementia=2.1, parkinson=2.4, stroke=1.6, depression=2.1, osteoporosis=1.7, alcohol=1.2,
                       chf=1.3, copd=1.3, cancer=1.1, insomnia=7.0, af=1.15),
    "zopiclone": dict(depression=2.2, dementia=1.4, stroke=1.3, parkinson=1.4, alcohol=1.5, osteoporosis=1.25,
                      cancer=1.3, copd=1.3, insomnia=6.0),
    "corinurad": dict(gout=28.0, hypertension=1.55, diabetes=1.45, diabcomp=1.3, chf=1.3, ckd=1.0, mi=1.3,
                      obesity=1.8, af=1.1),
    "allopurinol": dict(gout=28.0, hypertension=1.6, diabetes=1.45, diabcomp=1.3, chf=1.35, ckd=1.05, mi=1.3,
                        obesity=1.6, af=1.12),
    "velaglutide": dict(obesity=6.0, diabetes=1.8, diabcomp=1.4, hypertension=1.4, gallstones=1.6, depression=1.3,
                        alcohol=0.8),
    "orlistat": dict(obesity=5.5, diabetes=1.6, diabcomp=1.3, hypertension=1.3, gallstones=1.5, depression=1.3),
    "comparator": {},
}

# event-rate multipliers of each condition (present, whether or not yet recorded)
EVENT_MULT = {
    "fall": dict(dementia=1.9, parkinson=1.8, stroke=1.5, osteoporosis=1.3, alcohol=1.5, depression=1.2,
                 diabetes=1.15, chf=1.2, af=1.1),
    "aki": dict(ckd=1.8, chf=1.7, diabetes=1.3, diabcomp=1.5, hypertension=1.15, liver=1.5, cancer=1.2),
    "pancreatitis": dict(gallstones=2.5, alcohol=2.5, diabetes=1.25, obesity=1.2),
}

# ------------------------------------------------------------------ event base rates (per person-year)
# rate = exp(a + b * (age - ref)), men times the factor
BASE = {
    "fall": dict(a=np.log(0.0185), b=0.05, ref=70.0, male=0.72),
    "aki": dict(a=np.log(0.0080), b=0.035, ref=70.0, male=1.35),
    "pancreatitis": dict(a=np.log(0.0011), b=0.018, ref=50.0, male=1.2),
}
RR_CORINURAD = 1.7                      # days 1 to 30 after a new user's first dispensing
FALL_START_FACTOR = 1.6                 # a fall raises the chance of starting a sleep medicine (3 to 33 days after)
AKI_START_FACTOR = 0.3                  # an acute kidney injury lowers the chance of starting corinurad
AKI_START_DAYS = 30                     # for the 30 days after it
# velaglutide is not started after a pancreatitis: of the would-be starters with a pancreatitis admission before their
# start, only this share is prescribed it anyway (the rest of the cohort are people with none before their start), and
# a user with a pancreatitis while on it is restarted only at this rate
PANCREATITIS_HISTORY_STARTS = 0.1


def base_rate(event, age, female):
    p = BASE[event]
    r = np.exp(p["a"] + p["b"] * (np.asarray(age, float) - p["ref"]))
    return r * np.where(np.asarray(female, bool), 1.0, p["male"])


def mortality(age):
    return np.exp(-10.3 + 0.092 * np.asarray(age, float))


MORTALITY_FACTOR = {"tasorexant": 1.6, "zopiclone": 1.35, "corinurad": 1.0, "allopurinol": 1.3, "velaglutide": 0.85,
                    "orlistat": 0.9, "comparator": 1.0}

# ------------------------------------------------------------------ hospitals and departments
REGIONS = ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland"]
REGION_W = [0.32, 0.14, 0.21, 0.23, 0.10]
# per region: hospitals (4-digit SHAK prefix); each has these departments (3-digit suffix, specialty)
HOSPITALS = {
    "Hovedstaden": ["1306", "1311", "1324", "1340", "1351"],
    "Sjælland": ["3802", "3811", "3830"],
    "Syddanmark": ["4202", "5001", "5501", "6008"],
    "Midtjylland": ["6620", "6630", "7002", "7027"],
    "Nordjylland": ["8001", "8003"],
}
DEPARTMENTS = [("010", "Akutmedicin"), ("040", "Intern medicin"), ("050", "Kardiologi"), ("060", "Nefrologi"),
               ("070", "Endokrinologi"), ("080", "Lungemedicin"), ("090", "Geriatri"), ("100", "Neurologi"),
               ("120", "Ortopædisk kirurgi"), ("130", "Mave- og tarmkirurgi"), ("140", "Reumatologi"),
               ("150", "Onkologi"), ("160", "Psykiatri"), ("170", "Hepatologi"), ("180", "Karkirurgi")]
SPECIALTY_DEPT = {s: c for c, s in DEPARTMENTS}


def sor_code(shak):
    """The SOR identifier the patient registry uses for the department from 2019 (stable per department)."""
    h = int(hashlib.sha256(("sor:" + shak).encode()).hexdigest()[:10], 16)
    return "%d%07d" % (1000016000 + h % 899, int(shak) % 10000000)


# ------------------------------------------------------------------ diagnosis codes
FALL_INJURY = ["DS060", "DS000", "DS010", "DS220", "DS324", "DS420", "DS525", "DS720", "DS721", "DS800",
               "DS934", "DT140", "DS022", "DS301"]
FALL_INJURY_W = [0.10, 0.10, 0.10, 0.07, 0.03, 0.05, 0.12, 0.12, 0.06, 0.10, 0.05, 0.04, 0.03, 0.03]
FALL_CODES = ["DW019", "DW069", "DW109", "DW189", "DW199"]
FALL_CODES_W = [0.3, 0.12, 0.13, 0.2, 0.25]
OTHER_INJURY_CAUSE = ["DW229", "DW259", "DW549", "DX599"]
AKI_CODES = ["DN179", "DN170", "DN178"]
AKI_CODES_W = [0.86, 0.06, 0.08]
PANC_CODES = ["DK859", "DK851", "DK852", "DK850"]
PANC_CODES_W = [0.45, 0.3, 0.15, 0.1]
ACUTE_POOL = [("DJ189", "Intern medicin"), ("DN390", "Intern medicin"), ("DR074", "Kardiologi"),
              ("DR559", "Intern medicin"), ("DE869", "Intern medicin"), ("DA419", "Intern medicin"),
              ("DA099", "Intern medicin"), ("DL039", "Intern medicin"), ("DK590", "Mave- og tarmkirurgi"),
              ("DR101", "Mave- og tarmkirurgi"), ("DJ209", "Lungemedicin"), ("DI269", "Intern medicin")]
ACUTE_POOL_W = [0.17, 0.13, 0.12, 0.08, 0.07, 0.06, 0.07, 0.07, 0.05, 0.08, 0.06, 0.04]
OUTPATIENT_POOL = [("DZ034", "Kardiologi"), ("DM171", "Ortopædisk kirurgi"), ("DH251", "Intern medicin"),
                   ("DR104", "Mave- og tarmkirurgi"), ("DZ038", "Intern medicin"), ("DM545", "Ortopædisk kirurgi"),
                   ("DR229", "Intern medicin"), ("DZ016", "Intern medicin"), ("DK573", "Mave- og tarmkirurgi"),
                   ("DM751", "Ortopædisk kirurgi"), ("DR060", "Lungemedicin"), ("DZ098", "Intern medicin")]
OUTPATIENT_POOL_W = [0.12, 0.11, 0.06, 0.08, 0.12, 0.09, 0.07, 0.06, 0.05, 0.08, 0.07, 0.09]


def pseudonym(i, salt="pnr"):
    """A pseudonymised personal number: ten characters from an alphabet without look-alikes."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    h = hashlib.sha256(("%s:%d:%d" % (salt, SEED, i)).encode()).digest()
    n = int.from_bytes(h[:8], "little")
    out = []
    for _ in range(10):
        out.append(alphabet[n % 32])
        n //= 32
    return "".join(out)
