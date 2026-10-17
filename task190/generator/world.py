"""Carrowmore Port Authority: the world the pack is cut from."""

AUTHORITY = "Carrowmore Port Authority"
GEO = "Ireland"
CCY = "EUR"

YEAR = "2026"
YEAR_LO, YEAR_HI = "2026-01-01", "2026-12-31"
PRIOR_LO, PRIOR_HI = "2025-01-01", "2025-12-31"
LEDGER_EXTRACT = "2027-01-14"            # the day the payment ledger was pulled
TESTING_DONE = "2027-02-26"              # the day the testing was completed
CERTIFY_BY = "2027-06-30"                # the statements' certification date

HEAD_OF_AUDIT = "Tanya McCrea"           # head of internal audit
SENIOR_AUDITOR = "Colm Shaffrey"         # the auditor who performed the testing
FINANCE = "Marc O'Reardon"               # head of finance

# What the plan states, and only these two figures ship.
TOLERABLE = 1_160_000.00                 # tolerable misstatement for the population
CAPITAL_BUDGET = 58_000_000.00           # the base the 2.0 per cent was taken on
CONFIDENCE = 95                          # per cent

# What the plan does NOT state, and what no shipped file states.
EXPECTED_MISSTATEMENT = 387_500.00       # the allowance used in planning; note only
EXPANSION_FACTOR = 1.60                  # note only
RELIABILITY_0 = 3.00                     # note only
INTERVAL = 180_000                       # the selection interval; recovered, never stated
RANDOM_START = 123_455                   # the selection's start; never stated

GRAIN = 50_000                           # the misstatement is stated to the nearest fifty thousand

# programme: code, name, recorded value, payment lines, the contractor certificates it paid
PROGRAMMES = [
    ("CP-11", "Deepwater berth renewal", 13_900_000,
     [1_940_000, 1_210_000, 760_000, 455_000, 310_000, 224_000]),
    ("CP-14", "Quay 3 reconstruction", 10_600_000,
     [1_480_000, 905_000, 612_000, 388_000, 241_000]),
    ("CP-21", "Terminal roof and cladding", 8_400_000,
     [690_000, 402_000, 265_000, 196_000]),
    ("CP-23", "Rail siding and yard", 6_300_000, [540_000, 318_000, 207_000]),
    ("CP-31", "Dredging programme", 5_600_000, [1_120_000, 660_000, 395_000, 212_000]),
    ("CP-34", "Shore power installation", 4_700_000, [430_000, 254_000, 183_000]),
    ("CP-41", "Security and access systems", 3_500_000, [296_000, 188_000]),
    ("CP-44", "Pavement and surfacing", 3_300_000, [315_000, 201_000]),
    ("CP-47", "Welfare and offices fit-out", 3_200_000, [268_000, 181_000]),
]
PROG_CODES = [p[0] for p in PROGRAMMES]
PROG_NAME = {p[0]: p[1] for p in PROGRAMMES}

# the payment lines per programme, and the mean day-work variation invoice
LINES = {"CP-11": 3100, "CP-14": 2650, "CP-21": 3550, "CP-23": 3000, "CP-31": 1750,
         "CP-34": 3350, "CP-41": 3450, "CP-44": 2700, "CP-47": 3100}
DAYWORK_MEAN = {"CP-11": 4900.0, "CP-14": 4600.0, "CP-21": 4100.0, "CP-23": 4300.0,
                "CP-31": 5200.0, "CP-34": 3900.0, "CP-41": 3500.0, "CP-44": 3700.0,
                "CP-47": 3300.0}
DW_SHARE = 0.27                          # of a programme's non-certificate value
INT_SHARE = 0.34
INTERIM_MEAN = 56_000.0

# the defect: a wrong day-work labour rate, applied in six of the nine programmes
DEFECT = {"CP-41": (193, 0.58), "CP-23": (140, 0.49), "CP-47": (120, 0.52),
          "CP-34": (113, 0.41), "CP-21": (87, 0.37), "CP-44": (36, 0.44)}
TAINT_MUL = 0.98
CERT_ERROR = ("CP-31", 660_000, 62_400.00)   # one certificate overstated

# the payment release cut-off, which moved mid-year (ask A1)
CUTOFF = [("2026-01-01", "2026-06-30", "15:00"), ("2026-07-01", "", "14:00")]

# supplier risk categories, relabelled on 1 October 2026 (ask A2)
RISK_BANDS = ["1", "2", "3", "4", "5"]
RISK_NEW = {"1": "R-A", "2": "R-B", "3": "R-C", "4": "R-D", "5": "R-E"}
RISK_RELABEL = "2026-10-01"
