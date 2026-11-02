"""Fixed parameters of the task301 world (architecture 3): a fictional Spanish autonomous community, the
Comunidad de Valdemora, choosing which child poverty measure its 2027 budget funds."""
import datetime as dt

TASK = "task301"
SEED = 3013

AS_OF = dt.date(2026, 11, 6)          # the fiction's date; nothing in the pack is later
STAMP = dt.datetime(2026, 11, 6, 9, 15, 0)
REGISTER_PULL = dt.date(2026, 11, 2)  # the Complemento register extract
REGISTER_LAST_MONTH = (2026, 10)

# appraisal convention (filed in the department's guidance)
UPRATE_2025_2027 = 1.061              # survey 2025 disposable income to 2027
CHILD_BORN_FROM = 2009                # children: born 2009 or later
AGE_BASE_YEAR = 2026                  # a member's age on 1 January 2027 is 2026 less the birth year

# provinces (codes outside the real INE range)
PROVINCES = [("81", "Valdemora"), ("82", "Las Cuencas"), ("83", "Sierra del Alba")]
PROV_SHARE = [0.46, 0.33, 0.21]

# the Complemento Familiar (existing claimed benefit)
CFV_LAUNCH = dt.date(2022, 10, 1)
CFV_LIMIT_OLD = 7200.0                # computable income per equivalent adult, to 31 March 2024
CFV_LIMIT = 8400.0                    # from 1 April 2024
CFV_LIMIT_RISE = dt.date(2024, 4, 1)
CFV_RATES = [((2022, 10), 90.0), ((2024, 1), 95.0), ((2025, 7), 100.0)]   # per child per month
CFV_RATE_2027 = 100.0

# the five 2027 measures
A_RATE, A_INCOME_LIMIT = 28.0, 28000.0           # automatic through the regional tax agency
B_RATE = 36.0                  # new claimed child payment
C_LIMIT = 10800.0                                # widened Complemento limit, claimed by the newly entitled
D_RATE = 52.0                  # claimed rent supplement per child, renting families
E_RATE = 35.0                                    # automatic increase for current Complemento recipients

# survey
N_HOUSEHOLDS = 10420
TARGET_PERSONS = 1_690_000            # weighted population the household weights gross to (approx.)
