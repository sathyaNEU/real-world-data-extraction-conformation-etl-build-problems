"""Fixed facts of the world: dates, codes, names, rates."""
import datetime as dt

SEED = 31
AS_OF = dt.date(2026, 10, 2)            # the day the hub planning folder was put together
START = dt.date(2023, 4, 3)             # first clinic day in the record
REC_END = dt.date(2026, 9, 30)          # last day in the record
END = dt.date(2028, 3, 31)              # end of the planning year (truth only)
NEW_SYSTEM_LIVE = dt.date(2024, 11, 18) # new queue system's first day
OLD_SYSTEM_OFF = dt.date(2024, 11, 29)  # old system's last day (both systems hold 18 to 29 November 2024)
LOG_LAYOUT_B = dt.date(2025, 4, 1)      # reception log moves to the one-line-per-run-out layout
CODES_RENUMBERED = dt.date(2026, 4, 1)  # outpatient clinic codes reallocated at the PAS replacement
MERGER = dt.date(2025, 10, 1)           # Castle View Medical Centre merges into Fellside Health Centre
VACANCY = (dt.date(2025, 7, 14), dt.date(2025, 9, 12))
PAS_LIVE = dt.date(2026, 3, 16)         # request forms carry the new PAS's clinic codes from this date
TEMPLATES_FROM = dt.date(2026, 4, 1)    # the 2026-27 clinic templates: several clinics move to new weekdays
UNASSIGN_AFTER = 5                      # the e-roster unassigns a holder's line once a sickness passes five clinic days
VACANCY_SUCCESSOR = "21290455"          # the Band 2 post's new holder after the vacancy
GROWTH = 0.035
K_DETER = 0.8                           # practices with their own clinic: arrivals x exp(-K x the run-out share of the
DETER_WEEKS = 8                         # eight calendar weeks before)
DEMAND_SEED = 14                        # the demand stream's seed (staffing keeps SEED)
RECORDS_SEED = 33                       # who referred each visit, from which practice or clinic, and when
BASE_DAILY = 196.0
SHARES = {"P": 0.43, "N": 0.35, "H": 0.22}
POSTS = 7
PER_HEAD = 40
BANK_HEAD = 32
SHAPE = 120.0

HOSPITAL = "Hollinsfield General Hospital"
SATELLITE = "Brantmoor Community Hospital"
ICB = "Hollinsfield and Wyndale Integrated Care Board"
PEOPLE = {"manager": "Katherine Storey", "ops_lead": "Hugh Metcalfe", "reception": "Charlene Dale",
          "icb_lead": "Bethan Matthews", "outpatients": "Joseph Wood"}

# GP practices: code, name, list size at 1 April 2023, annual list growth, own phlebotomy clinic (LES)
PRACTICES = [
    ("K91014", "Brantmoor Road Surgery", 11840, 0.011, True),
    ("K91027", "Castle View Medical Centre", 6420, 0.009, True),
    ("K91031", "Fellside Health Centre", 14210, 0.010, True),
    ("K91046", "Mill Lane Practice", 7630, 0.016, False),
    ("K91052", "Northgate Group Practice", 16980, 0.012, True),
    ("K91068", "Orchard House Surgery", 6110, 0.007, False),
    ("K91073", "St Aidan's Medical Practice", 10350, 0.013, True),
    ("K91085", "Weir Bank Surgery", 8790, 0.010, False),
    ("K91090", "Kingsmead Surgery", 9260, 0.014, True),
    ("K91103", "Ashby Lane Medical Practice", 7480, 0.012, False),
    ("K91117", "The Elms Health Centre", 12620, 0.011, True),
    ("K91124", "Riverside Medical Group", 8150, 0.015, False),
]
MERGED_FROM, MERGED_INTO = "K91027", "K91031"

# Hospital clinics by specialty: clinic weekdays (0 Mon .. 4 Fri), share of hospital requests,
# the code in use to 31 March 2026 and the code from 1 April 2026 (allocated alphabetically by specialty)
SPECIALTIES = [
    # name,                     days,      share, old,     new
    ("Cardiology",              (1,),      0.13, "HG-C02", "HG-C01"),
    ("Diabetes and endocrinology", (0, 3), 0.22, "HG-C01", "HG-C02"),
    ("Gastroenterology",        (3,),      0.09, "HG-C04", "HG-C03"),
    ("General medicine",        (4,),      0.12, "HG-C06", "HG-C04"),
    ("Haematology",             (1, 2, 4), 0.16, "HG-C07", "HG-C05"),
    ("Renal medicine",          (0, 2),    0.14, "HG-C05", "HG-C06"),
    ("Rheumatology",            (2, 3),    0.14, "HG-C03", "HG-C07"),
]
# the new PAS's clinic codes and the 2026-27 clinic templates' weekdays
NEW_CLINIC = {"Cardiology": ("CAR01A", (3,)), "Diabetes and endocrinology": ("DIA01A", (0, 2)),
              "Gastroenterology": ("GAS01A", (4,)), "General medicine": ("GEN01A", (1, 2, 4)),
              "Haematology": ("HAE01A", (1,)), "Renal medicine": ("REN01A", (2, 3)), "Rheumatology": ("RHE01A", (0, 3))}
# hospital clinics' review and recall programmes: specialty, first day, last day, extra visits a clinic day
PROGRAMMES = [
    ("Diabetes and endocrinology", dt.date(2023, 9, 18), dt.date(2023, 10, 27), 110),
    ("Rheumatology", dt.date(2024, 2, 26), dt.date(2024, 3, 22), 100),
    ("Renal medicine", dt.date(2024, 6, 10), dt.date(2024, 7, 19), 120),
    ("Haematology", dt.date(2025, 1, 13), dt.date(2025, 2, 14), 110),
    ("Cardiology", dt.date(2025, 5, 12), dt.date(2025, 6, 13), 100),
    ("Diabetes and endocrinology", dt.date(2025, 10, 6), dt.date(2025, 11, 21), 130),
    ("Rheumatology", dt.date(2026, 2, 23), dt.date(2026, 3, 27), 110),
    ("Renal medicine", dt.date(2026, 6, 8), dt.date(2026, 7, 10), 110),
]
# long-term sickness spells HR records as one row per spell: post index, first day, last day
LONG_TERM_SICK = [(2, dt.date(2024, 9, 2), dt.date(2024, 10, 25)), (3, dt.date(2025, 5, 29), dt.date(2025, 7, 17)),
                  (5, dt.date(2025, 11, 17), dt.date(2026, 1, 21))]

BANK_HOLIDAYS = [(2023, 4, 7), (2023, 4, 10), (2023, 5, 1), (2023, 5, 8), (2023, 5, 29), (2023, 8, 28), (2023, 12, 25),
                 (2023, 12, 26), (2024, 1, 1), (2024, 3, 29), (2024, 4, 1), (2024, 5, 6), (2024, 5, 27), (2024, 8, 26),
                 (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 4, 18), (2025, 4, 21), (2025, 5, 5), (2025, 5, 26),
                 (2025, 8, 25), (2025, 12, 25), (2025, 12, 26), (2026, 1, 1), (2026, 4, 3), (2026, 4, 6), (2026, 5, 4),
                 (2026, 5, 25), (2026, 8, 31), (2026, 12, 25), (2026, 12, 28), (2027, 1, 1), (2027, 3, 26), (2027, 3, 29),
                 (2027, 5, 3), (2027, 5, 31), (2027, 8, 30), (2027, 12, 27), (2027, 12, 28), (2028, 1, 3)]
BH = {dt.date(*x) for x in BANK_HOLIDAYS}
BH_NAMES = {}
