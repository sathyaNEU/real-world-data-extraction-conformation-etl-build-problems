"""task128 world: Ferncliffe Trust Bank's early-stage card collections, five centres, the 2025-26 lists."""
import datetime as dt

SEED = 128
BANK = "Ferncliffe Trust Bank"
N_ACCOUNTS = 1600000

# centre code, name, province, time zone offset from Eastern (hours)
CENTRES = [("TBY", "Thunder Bay", "ON"), ("SUD", "Sudbury", "ON"), ("KGN", "Kingston", "ON"),
           ("LON", "London", "ON"), ("WPG", "Winnipeg", "MB")]
CODES = [c[0] for c in CENTRES]
NAMES = {c[0]: c[1] for c in CENTRES}
SHARE = [0.11, 0.14, 0.19, 0.31, 0.25]             # share of the card book serviced by each centre
CAMP = [0.13, 0.12, 0.15, 0.26, 0.13]              # share of each centre's accounts from the 2024 student-card campaign
CAP = [140, 160, 320, 250, 340]                   # each team's accounts dialled a day
DELTA = [0.047593, 0.068313, 0.09367, 0.13322, 0.076468]     # effect of a right-party contact on the roll probability
REACH_C = [-0.107073, 0.064778, 0.201237, -0.168793, 0.020193]     # each team's contact skill (logit shift)
PTP_SHARE = [0.409094, 0.365134, 0.381198, 0.372939, 0.406018]       # promises among right-party contacts
ARR_K = [0.994741, 0.995259, 0.998882, 0.998078, 0.997722]   # balance placed on an arrangement against the statement balance
DNC = [0.050, 0.055, 0.052, 0.060, 0.064]          # accounts on the do-not-call file
NDN = [0.110, 0.125, 0.118, 0.140, 0.156]          # accounts with no diallable number

N_CYCLES = 19
CAMPAIGN_CYCLES = (4, 13)

# the bank's collections calendar: weekdays less these holidays (federal and the provinces' shared ones)
HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 2, 17), dt.date(2025, 4, 18), dt.date(2025, 5, 19), dt.date(2025, 7, 1),
            dt.date(2025, 8, 4), dt.date(2025, 9, 1), dt.date(2025, 9, 30), dt.date(2025, 10, 13), dt.date(2025, 11, 11),
            dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3),
            dt.date(2026, 5, 18), dt.date(2026, 7, 1), dt.date(2026, 8, 3), dt.date(2026, 9, 7), dt.date(2026, 9, 30),
            dt.date(2026, 10, 12), dt.date(2026, 11, 11), dt.date(2026, 12, 25), dt.date(2026, 12, 28)}
MONTHS = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 13)]
LIST_MONTHS = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]   # lists in the export
YEAR_FROM, YEAR_TO = dt.date(2025, 7, 1), dt.date(2026, 6, 30)                        # the review year
PULL = dt.date(2026, 10, 9)
UPGRADE = {"TBY": dt.date(2025, 10, 20), "SUD": dt.date(2025, 10, 20), "KGN": dt.date(2025, 10, 20),
           "LON": dt.date(2025, 10, 20), "WPG": dt.date(2025, 11, 17)}
NEW_TEAM_DIALS = 400
BAR = 694
TEAM_COST = 1183000
LOSS_PER_ROLL = 1705


def bdays(y, m):
    d = dt.date(y, m, 1)
    out = []
    while d.month == m:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(1)
    return out


def collections_day(y, m, cycle):
    return bdays(y, m)[cycle - 1]


def add_months(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


assert all(len(bdays(y, m)) >= N_CYCLES for (y, m) in MONTHS)
assert -(-TEAM_COST // LOSS_PER_ROLL) == BAR and TEAM_COST % LOSS_PER_ROLL
