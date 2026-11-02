"""World parameters for task449 architecture 2 (the Province of Laurentide's 2027 in-demand occupations order).

Every number the generator draws from lives here; nothing downstream is typed by hand.
"""
import datetime as dt

SEED = 449002

SIM_START = dt.date(2024, 9, 1)            # burn-in for the job board and the jobseeker register
ACTIVITY_FROM = dt.date(2025, 10, 1)       # first day the board activity export covers
MIGRATION = dt.date(2026, 2, 2)            # the board's new platform went live; postings renumbered
EXTRACT = dt.date(2026, 11, 14)            # the Bureau's extracts were pulled on this day
FICTION_DATE = dt.date(2026, 11, 16)       # the briefing is written on this day
ORDER_DUE = dt.date(2026, 12, 1)

REF_DATES = [dt.date(2025, 12, 31), dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30)]
SNAP_DATES = [dt.date(2025, 7, 31), dt.date(2025, 8, 31), dt.date(2025, 9, 30), dt.date(2025, 10, 31),
              dt.date(2025, 11, 30), dt.date(2025, 12, 31), dt.date(2026, 1, 31), dt.date(2026, 2, 28),
              dt.date(2026, 3, 31), dt.date(2026, 4, 30), dt.date(2026, 5, 31), dt.date(2026, 6, 30),
              dt.date(2026, 7, 31), dt.date(2026, 8, 31), dt.date(2026, 9, 30)]

TERM_DAYS = 42                 # a self-service posting's term on the board, renewable
THRESHOLD = 1.5                # the order: at most 1.5 registered jobseekers per vacancy

# QEVS sector groups: code, title, NAICS 2017 sectors, Workshore coverage (share of the sector's vacancies posted
# on the board), sampling coefficient of variation of the survey estimate.
SECTORS = [
    ("AGR", "Agriculture, forestry, fishing and hunting", "11", 0.42, 0.071),
    ("CON", "Construction", "23", 0.47, 0.044),
    ("MFG", "Manufacturing", "31-33", 0.52, 0.041),
    ("TRD", "Wholesale and retail trade", "41, 44-45", 0.34, 0.038),
    ("TRW", "Transportation and warehousing", "48-49", 0.45, 0.052),
    ("PBA", "Professional, business and administrative services", "51-56", 0.40, 0.046),
    ("EDU", "Educational services", "61", 0.66, 0.057),
    ("HCS", "Health care and social assistance", "62", 0.50, 0.033),
    ("AFS", "Accommodation and food services", "72", 0.33, 0.042),
    ("OSP", "Other services and public administration", "71, 81, 91", 0.48, 0.049),
]
SECTOR_CODES = [s[0] for s in SECTORS]

# Schedule A occupations (NOC 2021 unit groups).
# code21, title, code16, {sector: weight}, self-service share of posted vacancies, median days to end,
# true vacancy stock level (positions on an average day, all employers), seasonal profile key,
# registered jobseekers level (primary sought occupation, average over the year).
OCCUPATIONS = [
    ("31301", "Registered nurses and registered psychiatric nurses", "3012", {"HCS": 0.94, "OSP": 0.06}, 0.10, 57, 205, "flat", 214),
    ("32101", "Licensed practical nurses", "3233", {"HCS": 1.0}, 0.22, 43, 96, "flat", 112),
    ("33102", "Nurse aides, orderlies and patient service associates", "3413", {"HCS": 1.0}, 0.56, 19, 150, "flat", 283),
    ("44101", "Home support workers, caregivers and related occupations", "4412", {"HCS": 0.9, "OSP": 0.1}, 0.78, 12, 118, "flat", 268),
    ("42202", "Early childhood educators and assistants", "4214", {"HCS": 0.7, "EDU": 0.3}, 0.58, 27, 102, "school", 205),
    ("62200", "Chefs", "6321", {"AFS": 0.9, "HCS": 0.1}, 0.30, 41, 58, "summer", 69),
    ("63200", "Cooks", "6322", {"AFS": 0.82, "HCS": 0.08, "TRD": 0.10}, 0.55, 23, 104, "summer", 139),
    ("65201", "Food counter attendants, kitchen helpers and related support occupations", "6711", {"AFS": 0.85, "TRD": 0.15}, 0.86, 9, 92, "summer", 214),
    ("65200", "Food and beverage servers", "6513", {"AFS": 1.0}, 0.86, 11, 84, "summer", 196),
    ("62020", "Food service supervisors", "6311", {"AFS": 1.0}, 0.62, 21, 36, "summer", 88),
    ("72200", "Electricians (except industrial and power system)", "7241", {"CON": 0.8, "MFG": 0.1, "OSP": 0.1}, 0.32, 49, 92, "build", 103),
    ("72310", "Carpenters", "7271", {"CON": 1.0}, 0.60, 30, 80, "build", 171),
    ("72300", "Plumbers", "7251", {"CON": 1.0}, 0.40, 42, 48, "build", 60),
    ("75110", "Construction trades helpers and labourers", "7611", {"CON": 1.0}, 0.86, 10, 112, "build", 248),
    ("73400", "Heavy equipment operators", "7521", {"CON": 0.7, "AGR": 0.3}, 0.62, 26, 60, "build", 129),
    ("64100", "Retail salespersons and visual merchandisers", "6421", {"TRD": 1.0}, 0.84, 12, 104, "retail", 262),
    ("65100", "Cashiers", "6611", {"TRD": 1.0}, 0.90, 8, 72, "retail", 168),
    ("65102", "Store shelf stockers, clerks and order fillers", "6622", {"TRD": 1.0}, 0.82, 10, 68, "retail", 156),
    ("73300", "Transport truck drivers", "7511", {"TRW": 0.8, "TRD": 0.2}, 0.50, 34, 132, "flat", 146),
    ("75101", "Material handlers", "7452", {"TRW": 0.6, "TRD": 0.2, "MFG": 0.2}, 0.86, 11, 104, "flat", 232),
    ("94141", "Industrial butchers and meat cutters, poultry preparers and related workers", "9462", {"MFG": 1.0}, 0.48, 24, 44, "flat", 71),
    ("95106", "Labourers in food and beverage processing", "9617", {"MFG": 1.0}, 0.86, 9, 80, "flat", 171),
    ("72400", "Construction millwrights and industrial mechanics", "7311", {"MFG": 0.8, "CON": 0.2}, 0.30, 52, 56, "flat", 61),
    ("72106", "Welders and related machine operators", "7237", {"MFG": 0.6, "CON": 0.4}, 0.48, 33, 64, "flat", 103),
    ("21232", "Software developers and programmers", "2174", {"PBA": 1.0}, 0.46, 46, 88, "flat", 100),
    ("13110", "Administrative assistants", "1241", {"PBA": 0.6, "HCS": 0.2, "OSP": 0.2}, 0.70, 17, 76, "flat", 218),
    ("65310", "Light duty cleaners", "6731", {"PBA": 0.7, "AFS": 0.3}, 0.86, 10, 68, "flat", 159),
    ("41221", "Elementary school and kindergarten teachers", "4032", {"EDU": 1.0}, 0.05, 38, 60, "school", 80),
    ("85101", "Harvesting labourers", "8611", {"AGR": 1.0}, 0.90, 6, 48, "harvest", 98),
    ("72410", "Automotive service technicians, truck and bus mechanics and mechanical repairers", "7321", {"OSP": 0.8, "TRD": 0.2}, 0.50, 37, 64, "flat", 77),
]

# Occupations outside Schedule A that post on the board (they share the sectors' survey totals).
# code21, title, code16, sector, self-service share, median days, stock level, seasonal key
OTHER_OCCUPATIONS = [
    ("12200", "Accounting technicians and bookkeepers", "1311", "PBA", 0.55, 24, 36, "flat"),
    ("14100", "General office support workers", "1411", "PBA", 0.65, 15, 44, "flat"),
    ("64409", "Other customer and information services representatives", "6552", "PBA", 0.72, 13, 40, "flat"),
    ("11200", "Human resources professionals", "1121", "PBA", 0.35, 40, 14, "flat"),
    ("65312", "Janitors, caretakers and heavy-duty cleaners", "6733", "OSP", 0.70, 16, 30, "flat"),
    ("43109", "Other instructors", "4216", "EDU", 0.40, 30, 14, "school"),
    ("41200", "University professors and lecturers", "4011", "EDU", 0.05, 70, 12, "school"),
    ("33103", "Pharmacy technical assistants and pharmacy assistants", "3414", "HCS", 0.45, 25, 22, "flat"),
    ("32120", "Medical laboratory technologists", "3211", "HCS", 0.12, 50, 18, "flat"),
    ("31102", "General practitioners and family physicians", "3112", "HCS", 0.08, 90, 10, "flat"),
    ("44100", "Home child care providers", "4411", "HCS", 0.80, 15, 20, "flat"),
    ("65210", "Support occupations in accommodation, travel and facilities set-up services", "6721", "AFS", 0.70, 14, 28, "summer"),
    ("64314", "Hotel front desk clerks", "6525", "AFS", 0.65, 16, 22, "summer"),
    ("75119", "Other trades helpers and labourers", "7612", "CON", 0.75, 14, 30, "build"),
    ("72402", "Heating, refrigeration and air conditioning mechanics", "7313", "CON", 0.42, 38, 16, "build"),
    ("94100", "Machine operators, mineral and metal processing", "9411", "MFG", 0.55, 22, 26, "flat"),
    ("94142", "Fish and seafood plant workers", "9463", "MFG", 0.80, 10, 24, "harvest"),
    ("64101", "Sales and account representatives - wholesale trade (non-technical)", "6411", "TRD", 0.50, 28, 26, "flat"),
    ("75201", "Delivery service drivers and door-to-door distributors", "7514", "TRW", 0.80, 12, 34, "flat"),
    ("85100", "Livestock labourers", "8431", "AGR", 0.80, 14, 22, "flat"),
    ("82030", "Agricultural service contractors and farm supervisors", "8252", "AGR", 0.50, 30, 10, "harvest"),
    ("63202", "Bakers", "6332", "TRD", 0.65, 18, 16, "flat"),
    ("42100", "Police officers (except commissioned)", "4311", "OSP", 0.02, 60, 12, "flat"),
    ("14400", "Shippers and receivers", "1521", "TRW", 0.70, 15, 24, "flat"),
    ("13100", "Administrative officers", "1221", "OSP", 0.40, 30, 30, "flat"),
]

# Seasonal multipliers on the inflow of new vacancies, by month (1..12).
SEASONAL = {
    "flat":    [1.00, 0.97, 1.00, 1.02, 1.03, 1.02, 0.98, 0.99, 1.02, 1.01, 0.99, 0.97],
    "summer":  [0.82, 0.84, 0.92, 1.05, 1.22, 1.30, 1.22, 1.08, 0.94, 0.88, 0.86, 0.87],
    "build":   [0.70, 0.74, 0.92, 1.18, 1.28, 1.24, 1.16, 1.12, 1.06, 0.96, 0.84, 0.80],
    "retail":  [0.84, 0.86, 0.92, 0.96, 1.00, 1.02, 0.98, 0.98, 1.04, 1.16, 1.22, 1.02],
    "school":  [0.86, 0.88, 1.00, 1.06, 1.22, 1.34, 1.18, 1.10, 0.86, 0.82, 0.84, 0.84],
    "harvest": [0.32, 0.30, 0.46, 0.80, 1.20, 1.46, 1.72, 1.82, 1.66, 1.18, 0.62, 0.46],
}
# jobseeker seasonality (registered jobseekers rise in the off-season)
JS_SEASONAL = {
    "flat":    [1.04, 1.05, 1.03, 1.00, 0.97, 0.97, 0.99, 0.99, 0.98, 0.98, 1.00, 1.02],
    "summer":  [1.10, 1.10, 1.06, 1.00, 0.92, 0.88, 0.90, 0.94, 1.00, 1.04, 1.06, 1.08],
    "build":   [1.22, 1.22, 1.14, 1.00, 0.88, 0.84, 0.86, 0.88, 0.92, 0.98, 1.06, 1.16],
    "retail":  [1.10, 1.08, 1.04, 1.00, 0.98, 0.98, 1.00, 1.00, 0.98, 0.94, 0.92, 0.98],
    "school":  [0.96, 0.96, 0.98, 1.00, 1.04, 1.10, 1.14, 1.08, 0.92, 0.94, 0.96, 0.96],
    "harvest": [1.34, 1.34, 1.24, 1.06, 0.90, 0.80, 0.74, 0.72, 0.76, 0.92, 1.12, 1.26],
}

WEIBULL_SHAPE = 1.3
EMPLOYER_SPEED_SD = 0.12        # employer-level multiplier on time to fill (lognormal sd)
DILIGENT_SHARE = 0.48           # self-service employers who take a filled posting down
DILIGENT_REMOVAL = 0.90
LAX_REMOVAL = 0.14
POSITIONS = [(1, 0.79), (2, 0.12), (3, 0.05), (4, 0.02), (5, 0.012), (6, 0.008)]
WITHDRAWN_SHARE = 0.08          # managed vacancies withdrawn rather than filled
