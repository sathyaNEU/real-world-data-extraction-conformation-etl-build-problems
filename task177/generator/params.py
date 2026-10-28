"""Constants for task177 (architecture 4): Prachi Valley Microfinance's joint-liability book, the pool offered to
Tamralipta Bank at the 31 December 2026 cut-off, and the asks' records. Every figure the write-up states is
computed from these and the generated records; nothing here is typed into a deliverable."""
import datetime as dt

SEED = 4                  # the book's meeting-by-meeting simulation
SEED_GEO = 177_401
SEED_BUREAU = 177_402
SEED_PACK = 177_403

# the calendar
HIST_START = dt.date(2023, 7, 1)          # the data room's ledger opens with the first meeting on or after this
MIGRATION = dt.date(2025, 4, 1)           # Kshetra core goes live; CollectPro is read-only from this date
CYCLONE = dt.date(2026, 10, 16)           # landfall
CUTOFF = dt.date(2026, 12, 31)            # the pool cut-off
OUTCOME = dt.date(2027, 6, 30)            # the date the forecast is about
SIM_END = dt.date(2027, 7, 31)            # the simulation runs on past the outcome date (truth only, never shipped)
HORIZON_DAYS = (OUTCOME - CUTOFF).days    # 181
DPD_LINE = 90

# the book: districts, branches, coastal exposure (the cyclone's onset multiplier on the background)
BRANCHES = [
    # code, name, district, groups, cyclone peak onset per member-meeting
    ("KND", "Kendrapara", "Kendrapara", 270, 0.160),
    ("PTM", "Pattamundai", "Kendrapara", 250, 0.150),
    ("RJN", "Rajnagar", "Kendrapara", 230, 0.180),
    ("JSP", "Jagatsinghpur", "Jagatsinghpur", 260, 0.140),
    ("TRT", "Tirtol", "Jagatsinghpur", 240, 0.130),
    ("ERS", "Ersama", "Jagatsinghpur", 220, 0.170),
    ("BDK", "Bhadrak", "Bhadrak", 260, 0.070),
    ("CHB", "Chandbali", "Bhadrak", 230, 0.090),
    ("BLS", "Balasore", "Balasore", 270, 0.050),
    ("BST", "Basta", "Balasore", 220, 0.060),
    ("JJR", "Jajpur Road", "Jajpur", 260, 0.0),
    ("BNJ", "Binjharpur", "Jajpur", 220, 0.0),
    ("SLP", "Salepur", "Cuttack", 250, 0.0),
    ("NIA", "Niali", "Cuttack", 230, 0.0),
]
DISTRICTS = ["Kendrapara", "Jagatsinghpur", "Bhadrak", "Balasore", "Jajpur", "Cuttack"]
GROUPS_PER_CENTRE = (3, 5)
GROUP_SIZE = 5

# the shortfall process, per member and fortnightly meeting
ONSET = 0.0050            # a member falls short (illness, a lost day's wage, a failed catch)
RECOVER = 0.20            # a short member recovers (a shortfall lasts five meetings on average)
CYCLONE_DECAY = 1.5       # meetings; the cyclone's added onset decays from its peak at the first meeting after landfall
CYCLONE_SPAN = 8          # meetings after landfall in which the added onset applies

# the group's capacity: it pays one short member's instalment at a meeting; two at once, rarely for long
STOP_ONE = 0.004          # a group carrying one member stops paying at a meeting
STOP_TWO = 0.20           # carrying two
STOP_MORE = 0.50          # carrying three or more

# loans
INSTALMENTS = 52
RATE_PA = 0.242           # reducing balance, fortnightly instalments
RENEW = 0.93              # a member who completes a loan takes the next one
CYCLE_AMOUNTS = {1: (40000, 50000), 2: (50000, 65000), 3: (60000, 80000)}
REFORM_GAP = (4, 8)       # meetings before a stopped group's place in the centre is taken by a new group
WRITE_OFF_DPD = 360

# the pool's selection criteria (the direct-assignment term sheet)
MHP_DAYS = 91             # disbursed on or before 1 October 2026 (the minimum holding period)
