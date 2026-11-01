"""Fixed inputs of the Harrowmere world: the wards, their stock and their true constant-quality price paths, the
turnover and the building work, the developers' 2024 to 2026 resales in Pellbury, the programme and the dates."""
import datetime as dt

SEED = 468
YEARS = list(range(2015, 2027))
LAST = 2026
EXTRACT = dt.date(2026, 12, 31)      # the yearly files as published on this date
UPDATE_END = dt.date(2027, 1, 29)    # the January 2027 monthly update: registered up to this date
LINE = 5.0                           # per cent, the programme's pressured-ward line
POT = 12_000_000                     # GBP, the 2027-28 uplift
PY0, PY1 = dt.date(2027, 4, 1), dt.date(2028, 3, 31)

TOWN = "HARROWMERE"
# Ward: code (May 2023), name, dwellings, mix (detached, semi, terraced, flat), log price level of a terraced house,
# the true annual constant-quality change (per cent) for 2016..2026, the house works hazard per year, postcode district.
WARDS = [
    ("E05015401", "Abbots Hollow", 11850, (0.10, 0.34, 0.38, 0.18), 12.32,
     [3.4, 4.1, 2.6, 1.7, 3.9, 7.2, 5.6, 1.2, 2.3, 3.1, 8.75], 0.0095, "HW2"),
    ("E05015402", "Brindley Moor", 12600, (0.18, 0.42, 0.26, 0.14), 12.41,
     [3.1, 3.6, 2.4, 1.2, 4.1, 6.8, 4.9, 0.6, 1.9, 2.7, 2.2], 0.0120, "HW7"),
    ("E05015403", "Calder Bank", 12150, (0.04, 0.16, 0.44, 0.36), 12.05,
     [3.9, 4.6, 3.3, 2.4, 3.5, 7.9, 6.2, 1.8, 3.4, 4.6, 8.3], 0.0070, "HW1"),
    ("E05015404", "Dunmore", 11400, (0.22, 0.45, 0.21, 0.12), 12.52,
     [2.8, 3.3, 2.1, 1.0, 4.4, 6.4, 4.4, 0.2, 1.4, 2.2, 2.6], 0.0130, "HW8"),
    ("E05015405", "Eastholme", 12450, (0.08, 0.30, 0.40, 0.22), 12.18,
     [3.6, 3.9, 2.8, 1.6, 3.7, 7.0, 5.1, 0.9, 2.0, 2.9, 3.5], 0.0090, "HW5"),
    ("E05015406", "Fennick", 11550, (0.05, 0.20, 0.50, 0.25), 11.96,
     [3.3, 4.4, 3.1, 2.2, 3.2, 6.9, 5.8, 1.5, 2.6, 3.6, 3.7], 0.0080, "HW4"),
    ("E05015407", "Gorsey Hill", 12000, (0.26, 0.46, 0.18, 0.10), 12.61,
     [2.6, 3.0, 1.9, 0.8, 4.6, 6.1, 4.0, -0.3, 1.1, 1.9, 2.2], 0.0140, "HW8"),
    ("E05015408", "Hollin Edge", 11700, (0.12, 0.38, 0.34, 0.16), 12.27,
     [3.2, 3.7, 2.5, 1.4, 3.8, 6.6, 4.8, 0.7, 1.8, 2.6, 2.95], 0.0105, "HW6"),
    ("E05015409", "Kestrel Rise", 12300, (0.06, 0.24, 0.38, 0.32), 12.10,
     [3.7, 4.3, 3.0, 2.0, 3.4, 7.6, 6.0, 1.6, 3.0, 4.2, 8.85], 0.0080, "HW3"),
    ("E05015410", "Moss Brow", 12000, (0.14, 0.40, 0.30, 0.16), 12.22,
     [3.0, 3.5, 2.3, 1.3, 3.9, 6.7, 4.7, 0.5, 1.7, 2.5, 3.0], 0.0110, "HW5"),
    ("E05015411", "Pellbury", 11700, (0.03, 0.12, 0.70, 0.15), 11.92,
     [3.5, 4.0, 2.7, 1.9, 3.3, 7.1, 5.4, 1.0, 2.2, 3.0, 3.7], 0.0085, "HW4"),
    ("E05015412", "Wexley", 11400, (0.16, 0.36, 0.30, 0.18), 12.36,
     [2.9, 3.4, 2.2, 1.1, 4.0, 6.5, 4.6, 0.4, 1.6, 2.4, 2.9], 0.0115, "HW7"),
]
WARD_CODES_2019 = {c: c.replace("E050154", "E050099") for c, *_ in WARDS}   # the 2019 codes, same names
FLIP_WARD = "Pellbury"
TYPE_PREMIUM = {"D": 0.48, "S": 0.17, "T": 0.0, "F": -0.30}
SALE_HAZARD = {"D": 0.035, "S": 0.042, "T": 0.050, "F": 0.062}
NOISE_SD = 0.058                     # log price noise of a sale at a given quality
DRIFT_SD = 0.036                     # a dwelling drifts about its ward path, per root year
COMPANY_SHARE = 0.045                # ordinary transfers to companies (category B)
COMPANY_BY_WARD = {"Calder Bank": 0.105, "Fennick": 0.08, "Eastholme": 0.07, "Wexley": 0.065, "Hollin Edge": 0.06}
REPO_SHARE = 0.004                   # sales under a power of sale (category B)

# The developers' wave in Pellbury: tired terraces bought in 2024 and 2025, a loft room and a rear extension
# completed under building regulations, sold on in 2026 (a few in late 2025).
FLIPS = {"Pellbury": 78, "Fennick": 3, "Calder Bank": 3, "Eastholme": 3, "Hollin Edge": 2}
FLIP_COMPANY = 0.84                  # the share bought through a company (an additional price paid entry)
FLIP_TIRED = -0.07                   # the log value a tired house carries before the works
FLIP_ADDED = (0.14, 0.23)            # the log value the loft room, the extension and the refit add

WORK_TYPES = [   # (work type, value added range, share of house works)
    ("Extension (single storey)", (0.05, 0.10), 0.42),
    ("Extension (two storey)", (0.09, 0.15), 0.14),
    ("Loft conversion", (0.08, 0.13), 0.30),
    ("Garage conversion", (0.03, 0.06), 0.14),
]
