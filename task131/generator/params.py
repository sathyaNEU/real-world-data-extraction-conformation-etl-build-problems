"""task131 generator: fixed parameters of the Murrandi world (the summer pricing trial 2025-26 and the 2026
demand forecast). Everything tuned lives in knobs.py."""
from datetime import date, timedelta

ORG = "Murrandi Regional Power"
ORG_SHORT = "MRP"
MDP = "Murrandi Regional Power Metering Services"
TOWN = "Murrandi"

SEED = 131

# the trial
ARMS = ["CTRL", "A", "B", "C"]
DESIGNS = ["A", "B", "C"]
PER_ARM = 400
N_HH = PER_ARM * len(ARMS)
LETTERS = date(2025, 11, 10)
START, END = date(2025, 12, 1), date(2026, 2, 28)
DATA_FROM, DATA_TO = date(2025, 11, 1), date(2026, 2, 28)
HOLIDAYS = {date(2025, 12, 25): "Christmas Day", date(2025, 12, 26): "Boxing Day",
            date(2026, 1, 1): "New Year's Day", date(2026, 1, 26): "Australia Day"}
LAST_HOT = date(2026, 2, 11)

DAYS = [DATA_FROM + timedelta(i) for i in range((DATA_TO - DATA_FROM).days + 1)]
NDAY = len(DAYS)
SPD = 48


def workday(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def trial_day(d):
    return START <= d <= END


# tariff codes in the billing system
CODE = {"HOME": "RH1", "A": "TRA", "B": "TRB", "C": "TRC", "CL": "RC2", "DS": "RT3"}
NAME = {"HOME": "Home Plan", "A": "Design A (Evening 3 to 9)", "B": "Design B (Evening 4 to 8)",
        "C": "Design C (Stepped)", "CL": "Hot Water Off-Peak", "DS": "Daytime Saver"}

# gazetted prices for 2025-26, GST inclusive (cents per kWh, cents per day)
PRICES = {
    "HOME": {"flat": 31.9145, "supply": 108.2367},
    "A": {"peak": 58.4127, "off": 21.6352, "supply": 112.4381},
    "B": {"peak": 66.0418, "off": 22.8193, "supply": 112.4381},
    "C": {"peak": 60.1260, "shoulder": 36.5471, "off": 21.0386, "supply": 112.4381},
    "CL": {"flat": 18.4316, "supply": 0.0},
    "BUYBACK": 7.1350,
}
import knobs as _K
for _d, _v in _K.OFFPEAK_NUDGE.items():
    PRICES[_d]["off"] = round(PRICES[_d]["off"] + _v, 4)
# windows in half-hour indices from midnight (index i covers i/2 to (i+1)/2 hours)
WIN = {
    "A": {"peak": (30, 42)},
    "B": {"peak": (32, 40)},
    "C": {"peak": (32, 40), "shoulder": [(28, 32), (40, 44)]},
}

# the 2026 forecast
N_FLAT_2728 = 41860
N_DS_2728 = 2940
N_RES_2728 = 44800
MD50 = 214.6
DESIGN_TMAX = 44.6
DESIGN_TMIN = 30.1
DESIGN_DAY_LABEL = "a working weekday in late January"
