"""task471 world: an unnamed EU country's population register and the National Bureau of Statistics' Register Coverage
Audit 2026. The Municipal Fund Regulation 2027 pays the small-municipality supplement to municipalities whose adjusted
resident population on 1 January 2026 is below 5,000: the persons registered there that day, less those estimated from
the audit not to have been living there. The register records an internal move when the new municipality registers
the person, and a departure abroad only when somebody reports it, so the records left behind belong to people who left
the country unreported."""
import datetime as dt

SEED = 471
BUREAU = "National Bureau of Statistics"
DIVISION = "Population Statistics Division"
MINISTRY = "Ministry of the Interior"
DIRECTORATE = "Directorate of Municipal Finance"
REGISTER = "Population Register"
AUDIT = "Register Coverage Audit 2026"
REGULATION = "Municipal Fund Regulation 2027"
SUPPLEMENT = "small-municipality supplement"
PEOPLE = {"head": "Ilse Spreeuw",          # head of population statistics, the Bureau
          "method": "Luka Bosman",         # the audit's methodologist
          "ministry": "Kay Wolfswinkel"}   # analyst, the ministry's municipal finance directorate

REF = dt.date(2026, 1, 1)            # the reference date of the register count and the audit
LINE = 5000                          # adjusted resident population below which a municipality qualifies
IN_PLAY = (4500, 6000)               # register counts the ministry asked the Bureau to adjust
NATIONAL_REGISTER = 9412736          # persons on the national register on 1 January 2026
N_AUDIT = 12000
FIELD_START, FIELD_END = dt.date(2026, 2, 2), dt.date(2026, 5, 29)
EXTRACT_DATE = dt.date(2026, 1, 5)   # the register extract as the register stood at the start of 1 January 2026
MSG_CUTOFF = dt.date(2026, 1, 31)    # the Bureau's population account counts a year's events sent by 31 January
AS_OF = dt.date(2026, 10, 19)

# The register's absence process. Silent departures follow the person's current stay in the country (completed years
# since the latest settlement from abroad) and whether the person has left the country before; people born in the
# country who never left have a small flat rate. Nothing else bears on absence.
NEVER = 0.0036
STAY = {0: 0.030, 1: 0.112, 2: 0.112, 3: 0.112, 4: 0.112, 5: 0.046, 6: 0.046, 7: 0.046, 8: 0.046, 9: 0.046}
STAY_10 = 0.014
LEFT_BEFORE = 2.4
CAP = 0.65
# of the absent, the share recorded in the audit as died abroad (older people) or living elsewhere in the country
DIED_SHARE_OLD, ELSEWHERE_SHARE = 0.18, 0.06


def p_absent(stay, left_before):
    """chance a registered person was not living in the municipality on the reference date"""
    if stay is None:
        return NEVER
    return min(CAP, STAY.get(stay, STAY_10) * (LEFT_BEFORE if left_before else 1.0))


def stay_band(stay):
    return None if stay is None else 0 if stay == 0 else 1 if stay <= 4 else 2 if stay <= 9 else 3


# Municipalities in play: (name, 2026 code, type). The two former municipalities merged into Ravenmeer on 1 January
# 2026; the register's history carries their codes for every event before that day.
MERGED = ("Ravenmeer", "1987")
FORMER = (("Ravensloot", "0731"), ("Meerdijk", "0744"))
MUNICIPALITIES = [
    ("Aldewolde", "0402", "T"), ("Borgermeer", "0417", "T"), ("Bremvoort", "0426", "T"), ("Dalmeer", "0438", "S"),
    ("Dornhaghe", "0451", "T"), ("Eekhorst", "0465", "G"), ("Haverstede", "0473", "G"), ("Heukelveen", "0488", "T"),
    ("Hilderloo", "0496", "U"), ("Koudenbeek", "0509", "G"), ("Lemdorp", "0514", "T"), ("Linterdam", "0527", "T"),
    ("Molenrade", "0533", "O"), ("Nijdorp", "0546", "O"), ("Oosterzand", "0552", "T"), ("Ravenmeer", "1987", "T"),
    ("Reitsloo", "0568", "T"), ("Sloterwaard", "0571", "T"), ("Steenwoude", "0584", "T"), ("Tienhaven", "0599", "T"),
    ("Uffeldijk", "0603", "T"), ("Velderkamp", "0615", "T"), ("Westerwierde", "0628", "T"), ("Zandloo", "0636", "T"),
]
CODES = [m[1] for m in MUNICIPALITIES]
NAME = {m[1]: m[0] for m in MUNICIPALITIES}
NAME.update({c: n for n, c in FORMER})
TYPE = {m[1]: m[2] for m in MUNICIPALITIES}

# Composition by type. mig: share of registered persons with a migration history (settled from abroad at least once);
# stay: their current stay in bands 0, 1-4, 5-9, 10+ years; left: share who had left the country before, by band;
# gap: years between the first settlement and the latest one for those who left before; mig_moved: share of migrants
# whose address date was reset by a move after they settled; nat_moved: the same for people born in the country;
# dep: 2025 reported departures abroad per registered person; repeat: departers who left twice in 2025.
TYPES = {
    "G": dict(mig=0.34, stay=(0.07, 0.66, 0.17, 0.10), left=(0.10, 0.50, 0.25, 0.05), gap=(8, 16), mig_moved=0.08,
              nat_moved=0.15, dep=0.052, repeat=0.06),
    "U": dict(mig=0.38, stay=(0.17, 0.78, 0.03, 0.02), left=(0.02, 0.02, 0.02, 0.02), gap=(1, 6), mig_moved=0.30,
              nat_moved=0.40, dep=0.060, repeat=0.012),
    "O": dict(mig=0.36, stay=(0.02, 0.06, 0.12, 0.80), left=(0.03, 0.04, 0.03, 0.03), gap=(1, 6), mig_moved=0.72,
              nat_moved=0.20, dep=0.010, repeat=0.012),
    "S": dict(mig=0.05, stay=(0.10, 0.30, 0.25, 0.35), left=(0.05, 0.10, 0.05, 0.03), gap=(1, 6), mig_moved=0.40,
              nat_moved=0.58, dep=0.009, repeat=0.012),
    "T": dict(mig=0.12, stay=(0.10, 0.28, 0.22, 0.40), left=(0.05, 0.12, 0.05, 0.03), gap=(1, 6), mig_moved=0.35,
              nat_moved=0.22, dep=0.012, repeat=0.012),
}
NATIONAL = dict(mig=0.24, stay=(0.12, 0.30, 0.22, 0.36), left=(0.06, 0.16, 0.06, 0.03), gap=(1, 14), mig_moved=0.35,
                nat_moved=0.24)

# Register counts on 1 January 2026, placed by calibrate.py (see the design note's Ladder).
COUNT = {'0402': 4612, '0417': 4728, '0426': 4846, '0438': 5068, '0451': 4912, '0465': 5220, '0473': 5210, '0488': 5152, '0496': 5157, '0509': 5203, '0514': 5241, '0527': 5333, '0533': 5098, '0546': 5096, '0552': 5412, '1987': 5561, '0568': 5487, '0571': 5634, '0584': 5702, '0599': 5768, '0603': 5821, '0615': 5889, '0628': 5944, '0636': 4561}

# Countries (national four-digit codes) by region, with the weights migrants come from in each municipality type.
HOME = ("6030", "Home country")
COUNTRIES = [
    ("5010", "Belgium", "EU"), ("5011", "Bulgaria", "EU"), ("5012", "Germany", "EU"), ("5013", "Spain", "EU"),
    ("5014", "France", "EU"), ("5015", "Italy", "EU"), ("5016", "Lithuania", "EU"), ("5017", "Poland", "EU"),
    ("5018", "Portugal", "EU"), ("5019", "Romania", "EU"), ("5020", "Hungary", "EU"), ("5021", "Greece", "EU"),
    ("5022", "Latvia", "EU"), ("5023", "Croatia", "EU"), ("5024", "Slovakia", "EU"),
    ("6001", "United Kingdom", "EUR"), ("6002", "Ukraine", "EUR"), ("6003", "Turkey", "EUR"),
    ("6004", "Serbia", "EUR"), ("6005", "Bosnia and Herzegovina", "EUR"),
    ("7001", "Morocco", "AFR"), ("7002", "Egypt", "AFR"), ("7003", "Nigeria", "AFR"), ("7004", "Eritrea", "AFR"),
    ("7005", "Somalia", "AFR"),
    ("8001", "India", "ASI"), ("8002", "China", "ASI"), ("8003", "Indonesia", "ASI"), ("8004", "Syria", "ASI"),
    ("8005", "Iran", "ASI"), ("8006", "Afghanistan", "ASI"), ("8007", "Philippines", "ASI"),
    ("9001", "United States", "AME"), ("9002", "Brazil", "AME"), ("9003", "Suriname", "AME"),
    ("9004", "Colombia", "AME"),
]
ORIGIN_WEIGHTS = {   # by the migrant's current stay band: recent stays draw more on labour and student flows
    "G": {"5017": 6, "5019": 5, "5011": 4, "5016": 3, "5022": 2, "5024": 1, "6002": 2, "5018": 1},
    "U": {"8001": 4, "8002": 4, "5012": 3, "5015": 2, "5013": 2, "6003": 1, "9001": 1, "8005": 1, "5021": 1},
    "O": {"6003": 6, "7001": 6, "9003": 3, "6004": 1, "6005": 1, "8004": 1, "5012": 1},
    "S": {"5012": 3, "5010": 2, "6001": 2, "9001": 1, "8001": 1, "5017": 1},
    "T": {"5017": 2, "5012": 2, "6003": 2, "7001": 2, "8004": 1, "5019": 1, "6002": 1, "5010": 1, "8007": 1},
    "N": {"5017": 3, "5012": 2, "6003": 2, "7001": 2, "8001": 2, "8004": 1, "5019": 2, "6002": 2, "9003": 1,
          "8002": 1, "5013": 1, "6001": 1, "5011": 1, "7004": 1, "9002": 1},
}
NATIONALITY_CODE = {"6030": "0001"}   # the register's nationality codes are the country codes with a 0 prefix
