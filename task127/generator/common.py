"""Constants for task127: Ninebark Mutual's motor bodily injury book, its two claims systems and its ledger.
Times are local (America/Chicago) unless a name says UTC; the simulation clock is days since 1 January 2017,
00:00 local."""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

CENTRAL = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
EPOCH = dt.datetime(2017, 1, 1)                         # local midnight, the simulation's day 0

SEED = 20270106
ORG = "Ninebark Mutual Insurance Company"
ORG_SHORT = "Ninebark Mutual"
PEOPLE = {"actuary": "Brian Robbins", "systems": "Ricky Evans", "controller": "Kyle Bean"}
STATES = ("IA", "NE", "SD")
STATE_SHARE = (0.52, 0.31, 0.17)

# the book
FIRST_AQ = (2017, 1)
N_AQ = 40                                               # accident quarters 2017 Q1 to 2026 Q4
VAL = dt.datetime(2027, 1, 1)                           # the valuation instant: the end of 31 December 2026, local
RUN = dt.datetime(2027, 1, 6, 6, 10)                    # the extracts ran at 06:10 local on 6 January 2027
CUTOVER = dt.datetime(2024, 6, 29)                      # features open at the start of the conversion weekend moved
PLATFORM_LIVE = dt.datetime(2024, 7, 1)                 # payments and new features on the platform from here
BASE_FEATURES = 1500                                    # claimant features a quarter in 2017 Q1
GROWTH = 1.015                                          # a year
TREND = 1.055                                           # severity trend a year, by accident date

# claimant kinds (latent: no column carries them)
P_CNP, P_FAST = 0.15, 0.50                              # the rest (0.35) are represented claims
WORK = {"cnp": (0.25, 0.60), "fast": (0.30, 0.50), "rep": (2.5, 0.55)}   # median years of work, log sd
SEV = {"fast": 5920.0, "rep": 24660.0}                  # median severity at 2017 cost
SEV_SIGMA = 0.70
SEV_WORK_POWER = 0.30                                   # a represented claim's severity grows with its work
SPEED = 0.75                                            # represented claims' pace once on the platform
MAX_WORK = 7.6                                          # every feature settles inside ten years
REPORT_MEAN_DAYS = 5.0
LONG_REPORT_SHARE, LONG_REPORT_MEAN_DAYS = 0.003, 180.0

# payments and events
ADVANCE_SHARE, ADVANCE_FRACTION = 0.05, 0.22            # represented claims with an advance, its share of severity
ADVANCE_THEN_NO_SETTLEMENT = 0.10                       # advanced claims later withdrawn or denied
SETTLED_UNDER_PD = 0.005                                # represented claims settled with the vehicle claim's payment
REOPEN = {"rep": 0.035, "fast": 0.01}
REOPEN_WITHDRAWN = 0.03                                # withdrawn claims reopened when counsel is retained
LIEN_SPLIT = 0.12                                       # settlements split with a medical lienholder
VOID_REISSUE, VOID_ONLY = 0.015, 0.002
WIRE_FROM = 75000.0                                     # settlements of this size go by wire
DUPLICATE_SHARE = 0.010
CHECK_RUN = (19, 30)                                    # the platform prints checks at 19:30 local
FEED_RUN = (1, 30)                                      # the ledger feed runs at 01:30 local

# files
F = {
    "basis": "ninebark_reserving_basis_2026.pdf",
    "legacy_claims": "legacy_bi_claims_archive.csv",
    "legacy_pay": "legacy_bi_payments_2017-2024.csv",
    "codes": "legacy_disposition_codes.txt",
    "conversion": "claims_conversion_notes_2024.md",
    "features": "platform_bi_features_2027-01-06.csv",
    "events": "platform_feature_events_2027-01-06.csv",
    "pay": "platform_bi_payments_2024-2027.csv",
    "notes": "platform_extract_notes.md",
    "gl": "gl_5311_bi_paid_loss_2026.csv",
    "gl_notes": "ledger_extract_notes_2026.md",
    "calendar": "finance_close_calendar_2026.xlsx",
    "register": "year_end_2026_preliminary_reserves.xlsx",
    "exposure": "earned_car_years_2017-2026.csv",
    "pd": "motor_pd_paid_by_accident_quarter.csv",
}
DISTRACTORS = ("exposure", "pd")
DELIVERABLES = ("bi_reserve_ye2026.md", "bi_claim_counts_ye2026.csv", "bi_unpaid_ye2026.png")
BOOKED = 344.6e6                                        # finance's preliminary year-end figure for bodily injury loss


def day(t: dt.datetime) -> float:
    """Days since the epoch for a local datetime."""
    return (t - EPOCH).total_seconds() / 86400.0


def at(d: float) -> dt.datetime:
    """The local datetime for a simulation day, to the second."""
    return EPOCH + dt.timedelta(seconds=int(round(d * 86400.0)))


def utc_text(d: float) -> str:
    """A simulation day as the platform writes it: an ISO timestamp in UTC."""
    return at(d).replace(tzinfo=CENTRAL).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def quarter_start(i: int) -> dt.datetime:
    """The local start of accident quarter i (0 is 2017 Q1)."""
    y, q = FIRST_AQ[0] + i // 4, i % 4
    return dt.datetime(y, 3 * q + 1, 1)


def aq_label(i: int) -> str:
    return "%d Q%d" % (FIRST_AQ[0] + i // 4, i % 4 + 1)
