"""task243 constants: the Province of Kalinawan's 12 LGUs, their demography, the movement of their oldest residents and
young adults, the two censuses and the civil registry's death registration. Everything the simulator draws from is
here; nothing below is read by the solver."""
import datetime as dt

SEED = 243

START = dt.date(2014, 7, 1)          # simulation start (one year of deaths before the window opens)
END = dt.date(2023, 3, 31)           # the civil registry extract
CENSUS1 = dt.date(2015, 8, 1)        # 2015 POPCEN reference date
CENSUS2 = dt.date(2020, 5, 1)        # 2020 CPH reference date
FIVE_YEARS_AGO = dt.date(2015, 5, 1)  # the 2020 census's residence five years earlier

PROVINCE = "Kalinawan"

# code, name as the 2020 census writes it, kind, 2020 household population (target), completeness of adult death
# registration (true), elderly mover rate as a multiple of the place's own mortality (origin side), labour-move level,
# mortality level (multiplier on the senescent hazard), total fertility
LGUS = [
    # code      name                 kind          pop2020  c_true  kappa_out  labour  mort  tfr
    ("KLW-01", "Kalinawan City",      "city",       240000,  0.870,  0.00,      0.0,    0.90, 2.3),
    ("KLW-02", "City of Santa Cruz",  "periurban",  190000,  0.600,  0.00,      0.0,    0.95, 2.6),
    ("KLW-03", "San Isidro",          "periurban",  160000,  0.610,  0.00,      0.0,    0.97, 2.7),
    ("KLW-04", "Esperanza",           "farming",    140000,  0.920,  0.34,      0.7,    1.02, 3.0),
    ("KLW-05", "Magsaysay",           "farming",    135000,  0.900,  0.30,      0.7,    1.05, 3.1),
    ("KLW-06", "Mabini",              "farming",    130000,  0.900,  0.32,      0.7,    1.04, 3.1),
    ("KLW-07", "Libertad",            "remote",      85000,  0.580,  0.22,      0.5,    1.25, 3.6),
    ("KLW-08", "San Luis",            "remote",     100000,  0.620,  0.20,      0.5,    1.18, 3.4),
    ("KLW-09", "Del Carmen",          "remote",     110000,  0.520,  0.18,      0.5,    1.12, 3.3),
    ("KLW-10", "Quezon",              "town",       125000,  0.870,  0.00,      0.3,    0.98, 2.8),
    ("KLW-11", "Rizal",               "town",       100000,  0.870,  0.00,      0.3,    1.00, 2.9),
    ("KLW-12", "San Miguel",          "town",       115000,  0.870,  0.00,      0.3,    0.99, 2.8),
]
CODES = [x[0] for x in LGUS]
NAME = {x[0]: x[1] for x in LGUS}
KIND = {x[0]: x[2] for x in LGUS}
POP2020 = {x[0]: x[3] for x in LGUS}
C_TRUE = {x[0]: x[4] for x in LGUS}
KAPPA_OUT = {x[0]: x[5] for x in LGUS}
LABOUR = {x[0]: x[6] for x in LGUS}
MORT = {x[0]: x[7] for x in LGUS}
TFR = {x[0]: x[8] for x in LGUS}

# where an origin's oldest movers go (OUT is outside the province, in the Philippines)
ELDER_DEST = {
    "KLW-04": {"OUT": 0.88, "KLW-01": 0.12},
    "KLW-05": {"OUT": 0.85, "KLW-01": 0.15},
    "KLW-06": {"OUT": 0.85, "KLW-01": 0.15},
    "KLW-07": {"KLW-10": 0.25, "KLW-01": 0.10, "OUT": 0.65},
    "KLW-08": {"KLW-11": 0.20, "KLW-01": 0.10, "OUT": 0.70},
    "KLW-09": {"KLW-12": 0.20, "KLW-01": 0.10, "OUT": 0.70},
}
# the oldest arriving from other provinces (a multiple of the destination's own deaths)
KAPPA_IN_EXT = {"KLW-01": 0.02, "KLW-02": 0.02, "KLW-03": 0.02, "KLW-10": 0.015, "KLW-11": 0.015, "KLW-12": 0.015}
ELDER_MIN_AGE = 45.0
ELDER_CAP_AGE = 78.0                 # movers' rates follow mortality up to here, then stay at its level

# young adults' labour moves: destinations by kind of origin
LABOUR_DEST = {"OUT": 0.60, "KLW-01": 0.20, "KLW-02": 0.12, "KLW-03": 0.08}
LABOUR_PEAK = 0.014                  # annual rate at the Rogers-Castro peak, scaled by each origin's labour level
EXT_YOUNG_IN = {"KLW-01": 0.005, "KLW-02": 0.003, "KLW-03": 0.003}   # annual in-moves from outside, ages 16 to 30
BACKGROUND_MOVE = 0.0025             # annual rate of family moves between LGUs, every age

# census coverage (share of the household population enumerated), uniform by age within a census
K2015 = {c: 0.990 for c in CODES}
K2020 = {c: 0.982 for c in CODES}
for c, d in [("KLW-01", -0.004), ("KLW-02", -0.006), ("KLW-07", -0.005), ("KLW-08", -0.003)]:
    K2020[c] += d

# death registration
TIMELY = 0.83                        # registered within 30 days, among deaths eventually registered
LOCKDOWN = (dt.date(2020, 3, 16), dt.date(2020, 5, 31))
HOSPITAL_CITY = {"city": 0.46, "periurban": 0.36, "farming": 0.24, "remote": 0.15, "town": 0.22}
DUP_RATE = 0.07                      # hospital-office registrations also entered at the residence office
NONRES_PER_YEAR = 260                # deaths of other provinces' residents in the city's hospitals
AGE_UNSTATED = 0.011
INFANT_REG_FACTOR = 0.72             # infants' deaths are registered less often than adults'

# ------------------------------------------------------------------ registration of births (ask A)
BIRTH_REG = 0.93                     # live births registered by the extract
BIRTH_TIMELY = {"KLW-01": 0.86, "KLW-02": 0.74, "KLW-03": 0.71, "KLW-04": 0.83, "KLW-05": 0.80, "KLW-06": 0.82,
                "KLW-07": 0.58, "KLW-08": 0.63, "KLW-09": 0.67, "KLW-10": 0.84, "KLW-11": 0.79, "KLW-12": 0.81}
BIRTH_HOSP_CITY = {"city": 0.62, "periurban": 0.48, "farming": 0.30, "remote": 0.18, "town": 0.27}
BIRTH_DOUBLE = 0.085                 # hospital-office births registered again by the parents at their own office
BIRTH_DOUBLE_SAME = 0.025            # the city's own mothers registering again at the city office
NONRES_BIRTHS_PER_YEAR = 900         # births in the city's hospitals to mothers from other provinces
LATE_OLD_BIRTHS_2022 = 1600          # births of earlier years registered in 2022 (the late registration drives)

# ------------------------------------------------------------------ certification of deaths (ask B)
ATTENDED_HOME = 0.10                 # home deaths attended by a private physician
MAYOR_CERT = {"city": 0.0, "periurban": 0.01, "farming": 0.03, "remote": 0.08, "town": 0.02}   # unattended deaths certified by the mayor
OFFICER_SIGNS = {"city": 0.82, "periurban": 0.70, "farming": 0.66, "remote": 0.45, "town": 0.64}   # unattended deaths the health officer signs in person
DEATH_DOUBLE_2022 = 0.13             # 2022 hospital-office deaths registered again at the residence office
DEATH_DOUBLE_WINDOW = 0.006          # the same in 2015 to 2020
# health officer posts vacant in 2022, a nurse in charge signing the certificates of unattended deaths
VACANT = {"KLW-01": (dt.date(2022, 1, 1), dt.date(2022, 6, 30)),
          "KLW-07": (dt.date(2022, 1, 1), dt.date(2022, 9, 30)),
          "KLW-08": (dt.date(2022, 4, 1), dt.date(2022, 12, 31)),
          "KLW-06": (dt.date(2022, 6, 1), dt.date(2022, 12, 31))}
EXTRACT_DUP_BATCHES = [("KLW-05", dt.date(2018, 3, 1), dt.date(2018, 3, 31)), ("KLW-10", dt.date(2022, 5, 1), dt.date(2022, 5, 31))]
CITYHOOD = dt.date(2019, 3, 16)      # Santa Cruz converted to a component city
