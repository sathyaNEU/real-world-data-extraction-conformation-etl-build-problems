"""The fixed world of task125: Merrowland Statistics' Household Labour Survey (HLS), its regions, its rotation and
the parameters of the households it samples. Every other module reads its constants from here."""
import datetime as dt

SEED = 125
SALT = 13                                # realisation of the sampling noise (chosen once, see the design note)
AS_OF = dt.date(2026, 10, 20)            # data lock for the July to September 2026 processing run
NOTE_DATE = dt.date(2026, 10, 23)        # the methods note the goldens are dated
OFFICE = "Merrowland Statistics"
SURVEY = "Household Labour Survey"

# regions: code, name, share of the population aged 15 and over, share of out-by-day households
REGIONS = [
    ("VEL", "Velmouth", 0.31, 0.43),
    ("CAR", "Carrowdene", 0.19, 0.37),
    ("PEL", "Pellard", 0.15, 0.33),
    ("HAS", "Haskvale", 0.13, 0.30),
    ("TIR", "Tirrin", 0.12, 0.28),
    ("DUN", "Dunmarrow", 0.10, 0.25),
]
RCODES = [r[0] for r in REGIONS]
RNAME = {r[0]: r[1] for r in REGIONS}
# districts per region (area codes on the call records), used to place an address
DISTRICTS = {"VEL": 9, "CAR": 6, "PEL": 5, "HAS": 5, "TIR": 4, "DUN": 4}

AGE_GROUPS = ["15-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
AGE_EDGES = [15, 25, 35, 45, 55, 65, 75, 200]

# quarters are (year, q); the person file runs 2023Q1 to 2026Q3, intakes from 2022Q1
FIRST_Q = (2023, 1)
LAST_Q = (2026, 3)
FIRST_INTAKE = (2022, 1)
CALLS_FROM = (2024, 1)                   # call records ship for the intakes of 2024Q1 to 2026Q3
LIMIT_FROM = (2026, 3)                   # first interviews capped at three visits from 1 July 2026
LIMIT_TO = (2026, 4)                     # ... to 31 December 2026; six visits again from January 2027
TEMPLATE_Q = (2026, 2)                   # the last full quarter collected before the limit
WAVES = 5
MAX_VISITS = 6
CAP_VISITS = 3

ISSUED_PER_INTAKE = 6400                 # addresses issued per quarterly intake
INELIGIBLE = 0.075                       # vacant, demolished or non-residential
REFUSAL = 0.17                           # at contact, wave 1
POP15 = 4_118_000                        # population 15 and over, 2023Q1
POP_GROWTH_Q = 0.0029                    # per quarter

# contact at each wave-1 visit: someone at home by day, else by household class
P_CONTACT_HOME = 0.60
P_CONTACT_AWAY = {"A": 0.150, "R": 0.240}
P_HOME_U = 0.86                          # an unemployed member is at home by day
P_HOME_I = 0.90                          # an inactive member is at home by day
# telephone waves: response given the previous wave answered
P_TEL_HOME = 0.935
P_TEL_AWAY = 0.875

# labour market: macro multiplier on the employed-to-unemployed hazard, by quarter index from FIRST_INTAKE - 8
MACRO = {
    (2020, 1): 1.00, (2020, 2): 1.00, (2020, 3): 1.00, (2020, 4): 1.00,
    (2021, 1): 0.98, (2021, 2): 0.97, (2021, 3): 0.96, (2021, 4): 0.95,
    (2022, 1): 0.94, (2022, 2): 0.94, (2022, 3): 0.95, (2022, 4): 0.96,
    (2023, 1): 0.97, (2023, 2): 0.99, (2023, 3): 1.01, (2023, 4): 1.03,
    (2024, 1): 1.05, (2024, 2): 1.07, (2024, 3): 1.09, (2024, 4): 1.10,
    (2025, 1): 1.11, (2025, 2): 1.12, (2025, 3): 1.12, (2025, 4): 1.11,
    (2026, 1): 1.11, (2026, 2): 1.11, (2026, 3): 1.14, (2026, 4): 1.13,
    (2027, 1): 1.13, (2027, 2): 1.13, (2027, 3): 1.13, (2027, 4): 1.13,
}

# quarterly transition probabilities by age group (E to U base, U to E base)
E_TO_U = {"15-24": 0.034, "25-34": 0.016, "35-44": 0.012, "45-54": 0.011, "55-64": 0.012, "65-74": 0.010, "75+": 0.010}
U_TO_E = {"15-24": 0.30, "25-34": 0.36, "35-44": 0.36, "45-54": 0.33, "55-64": 0.27, "65-74": 0.20, "75+": 0.15}
E_TO_I = {"15-24": 0.040, "25-34": 0.012, "35-44": 0.010, "45-54": 0.010, "55-64": 0.022, "65-74": 0.090, "75+": 0.150}
I_TO_E = {"15-24": 0.070, "25-34": 0.060, "35-44": 0.050, "45-54": 0.040, "55-64": 0.020, "65-74": 0.008, "75+": 0.002}
U_TO_I = 0.11
I_TO_U = {"15-24": 0.040, "25-34": 0.025, "35-44": 0.020, "45-54": 0.015, "55-64": 0.010, "65-74": 0.002, "75+": 0.001}
CLASS_EU = {"A": 0.40, "R": 1.00}        # out-by-day households lose jobs less often
CLASS_UE = {"A": 1.20, "R": 1.00}

PEOPLE = {
    "head": ("Raewyn Bailey", "Head of Labour Market Statistics"),
    "field": ("Jane Phillips", "Manager, Field Operations"),
    "methods": ("Aaron Tucker", "Principal Methodologist"),
    "data": ("Dylan Fletcher", "Survey Data Office"),
    "field_2024": ("Anna Bishop", "Manager, Field Operations"),
}


def qlabel(q):
    return "%dQ%d" % q


def qnext(q, k=1):
    y, n = q
    i = y * 4 + (n - 1) + k
    return (i // 4, i % 4 + 1)


def qindex(q):
    return q[0] * 4 + q[1] - 1


def qrange(a, b):
    out, q = [], a
    while qindex(q) <= qindex(b):
        out.append(q)
        q = qnext(q)
    return out


def qmonths(q):
    return [3 * (q[1] - 1) + m for m in (1, 2, 3)]


def qname(q):
    return {1: "January to March", 2: "April to June", 3: "July to September", 4: "October to December"}[q[1]] + " %d" % q[0]


def capped(intake):
    return qindex(LIMIT_FROM) <= qindex(intake) <= qindex(LIMIT_TO)


def age_group(age):
    for g, lo, hi in zip(AGE_GROUPS, AGE_EDGES, AGE_EDGES[1:]):
        if lo <= age < hi:
            return g
    raise ValueError(age)
