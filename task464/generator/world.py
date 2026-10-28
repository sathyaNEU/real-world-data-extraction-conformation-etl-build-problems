"""task464 architecture 9: the world.

The Hensey Vale Primary Care Network's seven practices issue repeat medicines on authorisations of a fixed number
of issues. When a repeat's last authorised issue is used, or a practice's review season comes round, the next
request waits for a clinician to re-authorise it at a review, and that is where nearly every patient who stops a
statin stops. Two practices re-authorised large parts of their lists in 2026 for their own reasons: Marrick House
moved its stable repeat patients to 56-day issues in February and March, re-authorising each converted repeat as
six issues, and Fennbridge switched its simvastatin patients to atorvastatin in June and July.

Nothing here states an expected count, a rate read off the record or a ranking of the practices. Those are
computed from the shipped files in answers.py and asserted in checks.py.
"""
import datetime as dt

NETWORK = "Hensey Vale Primary Care Network"
NETWORK_SHORT = "Hensey Vale PCN"
ICB = "the integrated care board"
CURRENCY = "GBP"

D0 = dt.date(2019, 1, 1)


def day(s):
    return (dt.date.fromisoformat(s) - D0).days


def date_of(n):
    return D0 + dt.timedelta(days=int(n))


def iso(n):
    return date_of(n).isoformat()


ASOF = day("2026-11-30")          # the extracts run to the end of this day
PULL = "2026-12-01"               # the network's searches ran the next morning
EXTRACT_FROM = day("2024-01-01")  # issue and change extracts start here
OUT = day("2027-06-30")           # outcome date
W0 = day("2027-03-01")            # outcome window opens
POP_FROM = day("2026-09-01")      # "issued a statin from 1 September to 30 November 2026"
SIM_START = day("2020-01-01")     # the simulated world starts four years before the extracts
KEEP_FROM = day("2023-01-01")     # issue rows before this are counted on their repeat but not kept
BRIEF_DATE = "2026-12-03"
BOARD_DATE = "2026-12-10"
SPEC_DATE = "2026-07-15"          # the ICB's return specification for calendar 2025, version 1.1
RETURN_YEAR = 2025

PEOPLE = {
    "clinical_director": "Dorothy Mitchell",
    "lead_pharmacist": "Hollie Kirk",
    "data_lead": "Stuart Newman",
}

# The seven practices. `season` is the months whose first request meets a review (a practice that reviews its
# repeat patients in fixed months); `drive` is a 2026 batch re-authorisation done without a review.
PRACTICES = [
    dict(key="A", code="P81402", name="Fennbridge Medical Centre", system="A", list_size=15240,
         L=28, M=13, season=(), drive=("switch", "2026-06-01", "2026-07-31", 0.42), n=2250, incid=0.155),
    dict(key="B", code="P81719", name="Cobbet Street Surgery", system="B", list_size=9380,
         L=28, M=6, season=(), drive=None, n=1300, incid=0.27),
    dict(key="C", code="P81066", name="Thistlecombe Surgery", system="A", list_size=8115,
         L=28, M=13, season=(), drive=None, n=1020, incid=0.155),
    dict(key="D", code="P81555", name="Marrick House Surgery", system="B", list_size=13610,
         L=28, M=13, season=(), drive=("length", "2026-02-02", "2026-03-27", 0.88), n=1690, incid=0.155),
    dict(key="E", code="P81283", name="Larkspur Road Practice", system="A", list_size=7290,
         L=28, M=13, season=(), drive=None, n=850, incid=0.155),
    dict(key="F", code="P81940", name="Wyndhollow Health Centre", system="B", list_size=9805,
         L=56, M=6, season=(), drive=None, n=1180, incid=0.16),
    dict(key="G", code="P81177", name="Pellow Green Surgery", system="A", list_size=6870,
         L=28, M=13, season=(), drive=None, n=780, incid=0.155),
]
BY_KEY = {p["key"]: p for p in PRACTICES}
BY_CODE = {p["code"]: p for p in PRACTICES}
KEYS = [p["key"] for p in PRACTICES]

# The repeat process.
Q_FAIL = 0.12            # share of reviews at which a patient's repeats are not re-authorised
BG_EARLY = 0.012         # chance a patient stops one medicine at a request, per 28 days, first 182 days on it
BG_LATE = 0.0024         # after that
DEREG_Y = 0.025          # leaving the list, a year
RETURN = 0.22            # a patient who stopped restarts later
RET_MIN, RET_MAX = 270, 520
SWITCH_STOP = 0.02       # stops at Fennbridge's switch
MOVE_Y = 0.004           # moves to another network practice, a year

# Patients on an ACE inhibitor or ARB alone whose practice issues them other lengths: (share, days) by the
# practice's usual issue length.
OWN_LENGTH = {28: [(0.10, 84), (0.12, 56)], 56: [(0.15, 28), (0.10, 84)]}

# How late patients habitually order: most order as their supply runs low, some days or weeks late.
LATE_TYPES = [(0.68, 0, 0), (0.20, 4, 11), (0.12, 9, 24)]   # (share, extra days low, extra days high)

# Medicines in the network's CVD repeat search.
STATINS = [
    # (drug, strength, share among starts before 2025, share among starts from 2025)
    ("Simvastatin", "40mg", 0.36, 0.06),
    ("Simvastatin", "20mg", 0.10, 0.02),
    ("Atorvastatin", "20mg", 0.30, 0.62),
    ("Atorvastatin", "40mg", 0.08, 0.10),
    ("Atorvastatin", "80mg", 0.07, 0.11),
    ("Rosuvastatin", "10mg", 0.05, 0.06),
    ("Pravastatin", "40mg", 0.04, 0.03),
]
STATIN_NAMES = ("Atorvastatin", "Simvastatin", "Rosuvastatin", "Pravastatin", "Fluvastatin")
ACE_ARB = [
    ("Ramipril", "2.5mg", "capsules", 0.16), ("Ramipril", "5mg", "capsules", 0.20), ("Ramipril", "10mg", "capsules", 0.12),
    ("Lisinopril", "10mg", "tablets", 0.10), ("Lisinopril", "20mg", "tablets", 0.07),
    ("Perindopril erbumine", "4mg", "tablets", 0.05),
    ("Losartan", "50mg", "tablets", 0.12), ("Losartan", "100mg", "tablets", 0.05),
    ("Candesartan", "8mg", "tablets", 0.08), ("Irbesartan", "150mg", "tablets", 0.05),
]
ACE_NAMES = ("Ramipril", "Lisinopril", "Perindopril erbumine", "Enalapril")
ARB_NAMES = ("Losartan", "Candesartan", "Irbesartan", "Valsartan", "Olmesartan")
DOACS = [("Apixaban", "5mg", 2, 0.52), ("Apixaban", "2.5mg", 2, 0.12), ("Edoxaban", "60mg", 1, 0.20),
         ("Rivaroxaban", "20mg", 1, 0.16)]
P2Y12 = [("Ticagrelor", "90mg"), ("Clopidogrel", "75mg")]

# Directions as each clinical system's prescribers write them.
DIRECTIONS_ONE = ["ONE daily", "ONE to be taken each day", "1 daily", "Take ONE tablet daily", "one a day"]
DIRECTIONS_NIGHT = ["ONE at night", "1 at night", "Take ONE tablet at night", "ONE to be taken at night", "1 nocte"]
DIRECTIONS_TWO = ["TWO daily", "TWO to be taken each day", "2 daily", "Take TWO tablets daily"]
DIRECTIONS_BD = ["ONE twice a day", "ONE twice daily", "1 bd", "Take ONE tablet twice a day"]
DIRECTIONS_HALF = ["HALF a tablet daily", "half daily"]

# Ask A: 2025 titrations of ACE inhibitors and ARBs edited in place on the repeat (same product, tablets a day
# changed), and the 2025 out-of-stock reissues.
TITRATE_2025 = 0.15            # share of 2025 ACE/ARB patients whose repeat directions were edited in 2025
TITRATE_UP = 0.62              # of which, one to two a day (quantity per issue doubled)
SHORTAGES = [("Losartan", "2025-03-10", "2025-05-23"), ("Ramipril", "2025-09-01", "2025-10-24")]
REISSUE_P = 0.22               # share of issues of a short line in its window cancelled and reissued
TWIN_P = 0.012                 # duplicate requests both dispensed, any non-statin repeat
REPRINT_P = 0.004              # spoilt or lost paper prescriptions reprinted, non-statin repeats

# Ask A, how each system's records carry a dose. Some prescribers write an ACE inhibitor or ARB dose in milligrams
# ("5mg once daily"), which on a repeat of half that strength is two a day; system B's repeat search reports each
# repeat as it was authorised, with later edits only in the change log; system A's audit export files every change
# against the drug line's current repeat.
MG_SHARE = 0.30
MG_TWO_OK = {("Ramipril", "2.5mg"), ("Ramipril", "5mg"), ("Lisinopril", "10mg"), ("Lisinopril", "20mg"),
             ("Perindopril erbumine", "4mg"), ("Losartan", "50mg"), ("Candesartan", "8mg"), ("Irbesartan", "150mg")}
MG_ONCE = ["%s once daily", "%s daily", "Take %s once a day", "%s each day"]


def units_per_dose(text):
    """Tablets or capsules per dose in the simulator's own direction wording."""
    s = " %s " % text.lower()
    if " two " in s or " 2 " in s: return 2
    if " half " in s: return 0.5
    return 1


def mg_text(text, strength, variant):
    """The same directions with the dose written in milligrams."""
    mg = units_per_dose(text) * float(strength[:-2])
    dose = ("%g" % mg) + "mg"
    s = text.lower()
    if "twice" in s or " bd" in " " + s: return "%s twice daily" % dose
    if "morning" in s: return "%s in the morning" % dose
    if "night" in s or "nocte" in s: return "%s at night" % dose
    return MG_ONCE[variant % len(MG_ONCE)] % dose


# Ask B, how the hospitals code the event on a discharge summary: a heart attack as an infarction, a STEMI, an NSTEMI
# or the synonym 'Heart attack'; unstable angina is not an infarction, and its summaries often carry the patient's
# earlier infarction as a history code dated the day it was coded.
MI_FAMILY = {"22298006": "Myocardial infarction", "401303003": "Acute ST segment elevation myocardial infarction",
             "401314000": "Acute non-ST segment elevation myocardial infarction"}
HEART_ATTACK = ("22298006", "Heart attack")
UNSTABLE_ANGINA = ("4557003", "Unstable angina")
OLD_MI = ("1755008", "Old myocardial infarction")

# Ask B: ticagrelor 90mg after a heart attack.
MI_Y = 0.012                   # heart attacks a year among the network's statin patients (plus new presentations)
TICAGRELOR_ISSUES = 13         # the GP repeat after discharge: thirteen 28-day issues
TICAG_OVERRUN = 0.18           # carried on past the thirteenth issue
TICAG_PEGASUS = 0.10           # moved to 60mg at the end
DISCHARGE_SUPPLY = (14, 28)

# The governing figures the documents state.
ROUND_TO = 10                  # expected numbers to the nearest 10 patients
PDC_LINE = 0.80
