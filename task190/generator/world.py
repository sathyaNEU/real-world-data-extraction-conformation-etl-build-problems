"""Pencarrow Mutual Bank: the fixed world behind the February 2027 review placement."""
import datetime as dt

SEED = 190
AS_OF = dt.date(2027, 1, 18)              # the extract date
COMMITTEE = dt.date(2027, 1, 28)
REVIEW_FROM = dt.date(2027, 2, 15)        # the review date clause 6.2 names
REVIEW_TO = dt.date(2027, 2, 26)
CLOSED_FROM = dt.date(2021, 1, 1)         # clause 6.3's closed onset window
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

# the July 2026 reorganisation: two lines merged into one and one renamed, with effective dates
REORG = dt.date(2026, 7, 1)
# the codes the records carried before the reorganisation, and the line each now maps to
OLD_LINES = [("FXL", "Foreign exchange", "FX", "merged into FX and remittance on 1 July 2026"),
             ("RMT", "Remittance services", "FX", "merged into FX and remittance on 1 July 2026"),
             ("TXB", "Transaction banking", "CB", "renamed Correspondent banking on 1 July 2026")]

ALERT_QUEUES = ["card disputes", "payment screening", "trade documents", "onboarding",
                "transaction monitoring", "sanctions screening"]
WORKING_STANDARD = 5                       # working days the operations report measures against
HOLIDAYS = [dt.date(2026, 1, 1), dt.date(2026, 1, 2), dt.date(2026, 2, 6), dt.date(2026, 4, 3),
            dt.date(2026, 4, 6), dt.date(2026, 4, 27), dt.date(2026, 6, 1), dt.date(2026, 10, 26),
            dt.date(2026, 12, 25), dt.date(2026, 12, 28), dt.date(2027, 1, 1), dt.date(2027, 1, 4)]
TARGET_ROWS = 25000
