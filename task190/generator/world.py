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
RANDOM_START = 121_750             # never stated; recovered from the tested set

GRAIN = 50_000                           # the misstatement is stated to the nearest fifty thousand

# programme: code, name, recorded value, payment lines, the contractor certificates it paid
PROGRAMMES = [
    ("CP-11", "Deepwater berth renewal", 13_874_318,
     [1_936_142, 1_207_885, 758_430, 454_216, 309_077, 223_461]),
    ("CP-14", "Quay 3 reconstruction", 10_612_744,
     [1_482_963, 903_117, 611_488, 387_204, 240_355]),
    ("CP-21", "Terminal roof and cladding", 8_386_509,
     [688_741, 401_326, 264_518, 195_882]),
    ("CP-23", "Rail siding and yard", 6_311_872, [541_093, 317_462, 206_735]),
    ("CP-31", "Dredging programme", 5_588_431, [1_117_406, 658_914, 394_208, 211_573]),
    ("CP-34", "Shore power installation", 4_713_286, [431_278, 253_641, 182_594]),
    ("CP-41", "Security and access systems", 3_492_617, [295_384, 187_619]),
    ("CP-44", "Pavement and surfacing", 3_307_958, [314_726, 200_843]),
    ("CP-47", "Welfare and offices fit-out", 3_192_683, [267_518, 180_726]),
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

# The defect: a wrong day-work labour rate, applied in seven of the nine programmes. The two
# largest, which are paid almost entirely on contractor certificates, carry none of it, and no
# certificate is overstated: every line certain of selection was found sound.
DEFECT = {"CP-41": (115, 0.58), "CP-23": (83, 0.49), "CP-47": (71, 0.52),
          "CP-34": (68, 0.41), "CP-21": (51, 0.37), "CP-44": (22, 0.44),
          "CP-31": (31, 0.46)}
TAINT_MUL = 0.98

# the payment release cut-off, which moved mid-year (ask A1)
CUTOFF = [("2026-01-01", "2026-06-30", "15:00"), ("2026-07-01", "", "14:00")]

# supplier risk categories, relabelled on 1 October 2026 (ask A2)
RISK_BANDS = ["1", "2", "3", "4", "5"]
RISK_NEW = {"1": "R-A", "2": "R-B", "3": "R-C", "4": "R-D", "5": "R-E"}
RISK_RELABEL = "2026-10-01"
