"""Pencarrow Mutual Bank: the fixed world behind the February 2027 review placement."""
import datetime as dt

SEED = 190
AS_OF = dt.date(2027, 1, 18)              # the extract date
COMMITTEE = dt.date(2027, 1, 28)
REVIEW_FROM = dt.date(2027, 2, 15)        # the review date clause 6.2 names
REVIEW_TO = dt.date(2027, 2, 26)
CLOSED_FROM = dt.date(2021, 1, 1)         # the resolved onset cohorts the longest observed delay implies
CLOSED_TO = dt.date(2024, 1, 31)
SPAN_FROM = dt.date(2020, 7, 1)           # the register's own earliest onset
DELAY_CAP = 34                            # months: no case in the bank's record has gone longer unseen
CAPACITY = 3                              # clause 6.4

BANK = "Pencarrow Mutual Bank"
SUPERVISOR = "the Financial Transactions Supervisor"
CONTRACTOR = "Haldane Reid Forensic"
PEOPLE = {"head": "Bruce Wheeler",            # head of financial crime
          "review_lead": "Kayla Burr"}        # the contractor's review lead

# (line, cases per quarter by onset, customers in thousands, mean months unseen, unreviewed alerts)
LINES = [
    ("Retail payments",       "RP", 72, 240.0, 0.8, 4100),
    ("Cards",                 "CD", 55, 180.0, 1.0, 2800),
    ("Deposits",              "DP", 38,  95.0, 1.6, 5600),
    ("Business lending",      "BL", 26,  18.4, 5.0,  310),
    ("FX and remittance",     "FX", 21,  31.0, 6.6, 7900),
    ("Trade finance",         "TF", 13,   2.1, 9.0,   95),
    ("Private wealth",        "PW",  7,   1.2, 11.5,  60),
    ("Correspondent banking", "CB",  3,   0.3, 12.5,  20),
]
TYPOLOGIES = ["structuring", "third party layering", "trade mispricing", "mule network",
              "sanctions evasion", "unexplained wealth", "invoice fraud", "account takeover"]
# what each line actually sees: a payments line is mules and takeovers, a trade line is mispricing
TYPOLOGY_MIX = {
    "RP": [22, 9, 1, 34, 3, 2, 5, 24],
    "CD": [11, 6, 1, 28, 2, 1, 6, 45],
    "DP": [31, 14, 1, 22, 4, 9, 3, 16],
    "BL": [12, 17, 14, 4, 5, 13, 33, 2],
    "FX": [19, 28, 9, 14, 21, 6, 2, 1],
    "TF": [4, 13, 46, 2, 17, 5, 12, 1],
    "PW": [9, 31, 6, 2, 11, 38, 2, 1],
    "CB": [7, 29, 18, 3, 36, 5, 2, 0],
}
# the year each line had, against its own normal: volumes move with the business, not evenly
YEAR_FACTOR = {
    "RP": {2020: 0.86, 2021: 0.94, 2022: 1.03, 2023: 1.09, 2024: 1.14, 2025: 1.07, 2026: 0.98, 2027: 0.95},
    "CD": {2020: 0.79, 2021: 0.88, 2022: 1.11, 2023: 1.18, 2024: 1.04, 2025: 0.93, 2026: 0.91, 2027: 0.9},
    "DP": {2020: 1.14, 2021: 1.08, 2022: 0.96, 2023: 0.89, 2024: 0.93, 2025: 1.02, 2026: 1.12, 2027: 1.16},
    "BL": {2020: 0.91, 2021: 0.97, 2022: 1.12, 2023: 1.06, 2024: 0.94, 2025: 0.98, 2026: 1.09, 2027: 1.11},
    "FX": {2020: 1.08, 2021: 1.13, 2022: 0.92, 2023: 0.87, 2024: 1.04, 2025: 1.11, 2026: 1.06, 2027: 1.02},
    "TF": {2020: 0.88, 2021: 0.93, 2022: 1.07, 2023: 1.14, 2024: 1.09, 2025: 0.96, 2026: 0.89, 2027: 0.87},
    "PW": {2020: 1.16, 2021: 1.04, 2022: 0.91, 2023: 0.95, 2024: 1.08, 2025: 1.13, 2026: 0.97, 2027: 0.94},
    "CB": {2020: 0.93, 2021: 1.11, 2022: 1.06, 2023: 0.9, 2024: 0.97, 2025: 1.09, 2026: 1.04, 2027: 1.0},
}
# the months a confirmed case waits between being seen and being accepted, by line
CONFIRM_LAG = {"RP": 0.4, "CD": 0.5, "DP": 0.7, "BL": 1.6, "FX": 1.3, "TF": 2.1, "PW": 2.4, "CB": 2.6}

# the July 2026 reorganisation: two lines merged into one and one renamed, with effective dates
REORG = dt.date(2026, 7, 1)
# the codes the records carried before the reorganisation, and the line each now maps to
OLD_LINES = [("FXL", "Foreign exchange", "FX", "merged into FX and remittance on 1 July 2026"),
             ("RMT", "Remittance services", "FX", "merged into FX and remittance on 1 July 2026"),
             ("TXB", "Transaction banking", "CB", "renamed Correspondent banking on 1 July 2026")]

ALERT_QUEUES = ["card disputes", "payment screening", "trade documents", "onboarding",
                "transaction monitoring", "sanctions screening"]
WORKING_STANDARD = 5                       # business days clause 7.2 measures an alert against
# the days the bank is closed, shipped as bank_closed_days.csv and read by the golden from the pack
HOLIDAYS = [(dt.date(2026, 1, 1), "New Year's Day"), (dt.date(2026, 1, 2), "day after New Year's Day"),
            (dt.date(2026, 1, 19), "Wellington Anniversary"), (dt.date(2026, 2, 6), "Waitangi Day"),
            (dt.date(2026, 4, 3), "Good Friday"), (dt.date(2026, 4, 6), "Easter Monday"),
            (dt.date(2026, 4, 27), "Anzac Day observed"), (dt.date(2026, 6, 1), "King's Birthday"),
            (dt.date(2026, 6, 29), "Matariki"), (dt.date(2026, 10, 26), "Labour Day"),
            (dt.date(2026, 12, 25), "Christmas Day"), (dt.date(2026, 12, 28), "Boxing Day observed"),
            (dt.date(2027, 1, 1), "New Year's Day"), (dt.date(2027, 1, 4), "day after New Year's Day observed")]
TARGET_ROWS = 25000
