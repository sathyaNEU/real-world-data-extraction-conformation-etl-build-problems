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
RANDOM_START = 89_000             # the random start the selection ran from

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
# the capital programme board's approved budget per programme, in euro: a judgement made when
# the programme was approved, so it does not equal the year's spend and is not derivable from it
APPROVED_BUDGET = {"CP-11": 14_420_000, "CP-14": 10_250_000, "CP-21": 8_940_000,
                   "CP-23": 6_080_000, "CP-31": 5_925_000, "CP-34": 4_460_000,
                   "CP-41": 3_680_000, "CP-44": 3_140_000, "CP-47": 3_355_000}
# each programme's start and planned completion: nine programmes approved over two years
PROG_DATES = {"CP-11": ("2024-02-19", "2028-09-29"), "CP-14": ("2024-04-08", "2027-11-30"),
              "CP-21": ("2024-09-02", "2028-03-31"), "CP-23": ("2025-01-13", "2028-06-30"),
              "CP-31": ("2023-11-06", "2027-05-31"), "CP-34": ("2025-04-07", "2029-01-31"),
              "CP-41": ("2024-06-17", "2027-08-31"), "CP-44": ("2025-02-24", "2028-02-29"),
              "CP-47": ("2024-11-11", "2027-12-17")}

# Irish public holidays falling on a Tuesday or a Friday in 2026 and 2025: no payment run goes out
HOLIDAYS = {"2026-01-01", "2026-03-17", "2026-04-03", "2026-05-01", "2026-12-25",
            "2025-01-01", "2025-03-17", "2025-04-18", "2025-05-02", "2025-12-26"}
# runs that did not go out: the August bank holiday week was covered by the Tuesday run, and the
# finance system upgrade took the first Friday in November
MISSED_RUNS = {"2026-08-07", "2026-11-06", "2025-08-08"}

# the funder caps its contribution to any one programme; only the largest reaches it
GRANT_CAP = {"CP-11": 3_900_000}

PROG_CODES = [p[0] for p in PROGRAMMES]
PROG_NAME = {p[0]: p[1] for p in PROGRAMMES}

# the payment lines per programme, and the mean day-work variation invoice
LINES = {"CP-11": 3083, "CP-14": 2671, "CP-21": 3542, "CP-23": 2987, "CP-31": 1764,
         "CP-34": 3361, "CP-41": 3438, "CP-44": 2713, "CP-47": 3094}
DAYWORK_MEAN = {"CP-11": 4900.0, "CP-14": 4600.0, "CP-21": 4100.0, "CP-23": 4300.0,
                "CP-31": 5200.0, "CP-34": 3900.0, "CP-41": 3500.0, "CP-44": 3700.0,
                "CP-47": 3300.0}
DW_SHARE = 0.27                          # of a programme's non-certificate value
INT_SHARE = 0.34
INTERIM_MEAN = 56_000.0

# The defect: a wrong day-work labour rate, applied in seven of the nine programmes. The two
# largest, which are paid almost entirely on contractor certificates, carry none of it, and no
# certificate is overstated: every line certain of selection was found sound.
DEFECT = {"CP-41": (9999, 0.23), "CP-23": (9999, 0.20), "CP-47": (9999, 0.21),
          "CP-34": (9999, 0.17), "CP-21": (9999, 0.15), "CP-44": (9999, 0.18)}
TAINT_MUL = 0.94

# the payment release cut-off, which moved mid-year (ask A1)
CUTOFF = [("2026-01-01", "2026-06-30", "15:00"), ("2026-07-01", "", "14:00")]

# supplier risk categories, relabelled on 1 October 2026 (ask A2)
RISK_BANDS = ["1", "2", "3", "4", "5"]
RISK_NEW = {"1": "R-A", "2": "R-B", "3": "R-C", "4": "R-D", "5": "R-E"}
RISK_RELABEL = "2026-10-01"
