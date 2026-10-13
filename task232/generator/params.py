"""task232 parameters: the Coast and Ranges public health unit, its childcare enteric investigations from July 2021
and the laboratory notification feeds into the state's notifiable-conditions platform, October 2022 to October 2026."""
from datetime import date

SEED = 744641
STAMP_SALT = 140                       # the minute stamp of each authorisation
FINE_SALT = 23                         # the minute-level sign-in and sign-out record
REC_SEED = 23277                       # the records layer (message ids, timestamps, the asks' records)

# Windows
EPI_FROM = date(2021, 7, 1)            # first index onset in the investigation register
EPI_TO = date(2026, 10, 31)            # last index onset simulated (investigations still open at the extract)
LOG_FROM = date(2022, 10, 1)           # the platform's message log extract starts
LOG_TO = date(2026, 10, 31)            # and ends (extract taken 13 November 2026)
BASIS_FROM = date(2023, 10, 1)         # the SLA basis: three years to 30 September 2026
BASIS_TO = date(2026, 9, 30)
YEAR_FROM = date(2025, 10, 1)          # the asks' year to 30 September 2026
YEAR_TO = date(2026, 9, 30)
EXTRACT = date(2026, 11, 13)
REQUEST = date(2026, 11, 16)
RELEASE = date(2026, 12, 1)            # NCP 4.2 goes live with per-feed SLA alerts
CODESET_FROM = date(2025, 7, 1)        # the platform's condition code-set update
ACQUISITION = date(2024, 3, 1)         # the regional laboratory joins Larkspur; its sending facility code changes

SETTINGS = [1, 2, 4, 6, 8, 12, 24]     # allowed SLA lateness settings, hours after authorisation
TOLERANCE = 1.0                        # expected secondary cases a year at a feed's setting
CALL_FROM, CALL_TO = 7.0, 21.0         # the unit calls families and centres from 07:00 to 21:00, every day
LEAVE_AFTER = 1.0                      # a case at the centre leaves an hour after the unit's call

# Conditions on the urgent childcare list.
# key: (name, incubation shortest d, longest d, median d, log-sd, transmission per pair-hour of contact, symptomatic
#       share, days a secondary case attends while shedding before the centre sends them home, background cases per
#       contact-day, P(earlier cases in the room), index episodes a year, P(a later chain or introduction))
COND = {
    "SHIG": ("Shigellosis", 0.5, 7.0, 2.0, 0.45, 0.0100, 0.75, 0.90, 0.00055, 0.378, 16.0, 0.30),
    "STEC": ("Shiga toxin-producing E. coli infection", 1.0, 10.0, 3.5, 0.40, 0.0069, 0.60, 0.80, 0.00035, 0.0576, 8.0, 0.10),
    "CRYP": ("Cryptosporidiosis", 1.0, 12.0, 7.0, 0.30, 0.0126, 0.65, 1.10, 0.00064, 0.126, 28.0, 0.05),
}
COND_KEYS = ["SHIG", "STEC", "CRYP"]
FOLLOWUP_DAYS = {"SHIG": 14, "STEC": 20, "CRYP": 24}   # follow-up after the exclusion: twice the longest incubation
SOURCE_LOOKBACK = 21                   # the investigation asks about illness in the room from 21 days before onset
SUMMER = {"SHIG": 1.5, "STEC": 1.2, "CRYP": 1.9}       # December to March multiplier (other months 0.8)

# Feeds (laboratories): share of urgent childcare first notifications by condition, for centres away from the border.
FEEDS = ["CRBH", "LPG", "HDN", "KES", "HPS", "SERL"]
FEED_SHARE = {
    "SHIG": {"CRBH": 0.16, "LPG": 0.36, "HDN": 0.30, "HPS": 0.15, "SERL": 0.03},
    "STEC": {"CRBH": 0.34, "LPG": 0.20, "HDN": 0.16, "HPS": 0.14, "SERL": 0.16},
    "CRYP": {"CRBH": 0.16, "LPG": 0.32, "HDN": 0.32, "HPS": 0.17, "SERL": 0.03},
}
FEED_WEIGHT = {"CRBH": 0.979, "LPG": 1.0, "HDN": 1.04, "HPS": 0.824, "SERL": 1.102}
BORDER_WEIGHT = 1.235                  # a border centre's chance of an investigation against another centre's
BORDER_KES = 0.78                      # border centres' families use the Queensland laboratory this often

# Childcare: centres, rooms, people.
N_CENTRES = 64
BORDER_CENTRES = 9                     # centres in the border towns, whose families mostly use the Queensland laboratory
STAFF_SHARE_INDEX = 0.12               # index cases who are educators
