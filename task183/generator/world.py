"""The fiction's fixed facts: the utility, its eight underground feeders, the dates the pack is cut on, and the
people. Everything else is generated from these."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 183
COMPANY = "Tamsin Valley Electric"
DISTRICT = "Tamsin Valley underground district"
LOCAL = ZoneInfo("America/New_York")
UTC = dt.timezone.utc

CUT = dt.date(2026, 9, 30)                 # GIS export, work order and outage extracts run through this day
EXTRACT_DAY = dt.date(2026, 10, 6)         # the day the pack was pulled
ARCHIVE_START = dt.date(2012, 1, 1)        # the work order archive starts with the 2012 system conversion
WINDOW5 = (dt.date(2021, 10, 1), dt.date(2026, 9, 30))
RY_ASK = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
OMS_START = dt.date(2020, 10, 1)
ADMS_CUTOVER = dt.datetime(2026, 3, 17, 6, 0, tzinfo=LOCAL)   # first ADMS-recorded outage starts after this
LATERAL_MOVE = dt.date(2026, 6, 14)
CATCHUP = (dt.date(2019, 3, 4), dt.date(2020, 11, 20))
REPLACE_AT_SECOND_FROM = dt.date(2019, 1, 1)

SUBSTATIONS = [
    ("HRD", "Harrow Road", ["HR12", "HR14"]),
    ("MLN", "Mill Lane", ["ML03", "ML07"]),
    ("QHL", "Quarry Hill", ["QH21", "QH22"]),
    ("SPK", "Sutter Park", ["SP05", "SP09"]),
]
FEEDERS = ["HR12", "HR14", "ML03", "ML07", "QH21", "QH22", "SP05", "SP09"]
NAME = {"HR12": "Harrow Road 12", "HR14": "Harrow Road 14", "ML03": "Mill Lane 3", "ML07": "Mill Lane 7",
        "QH21": "Quarry Hill 21", "QH22": "Quarry Hill 22", "SP05": "Sutter Park 5", "SP09": "Sutter Park 9"}
SUB_OF = {f: s for s, _, fs in SUBSTATIONS for f in fs}
CIRCUIT_NO = {"HR12": "13-2412", "HR14": "13-2414", "ML03": "13-3103", "ML07": "13-3107", "QH21": "13-4421",
              "QH22": "13-4422", "SP05": "13-5505", "SP09": "13-5509"}

# personas drawn with guard.py names --geo "United States" --seed 183 (on the card)
PEOPLE = {"asset": "Samantha Werner", "reliability": "Jeffrey Roth", "gis": "Charles Weber"}

ANSWER = "QH21"
