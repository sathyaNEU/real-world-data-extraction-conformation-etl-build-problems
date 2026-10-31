"""task156 constants: the Rauwhero District Council's wastewater network, the Riverbank Road pump station (PS03) and the
Ngaio Road subdivision.

Rauwhero is a river terrace town on the Kahuwera River. Its wastewater drains by gravity to six pump stations, each with
an engineered overflow to the river under the Kahuwera Regional Council's network discharge consent AUTH-2024-0418,
granted in March 2024 on the hourly rainfall record of 2004 to 2023. PS03 at Riverbank Road takes the low terrace and
part of the upper terrace and pumps to the treatment plant. The developer of the Ngaio Road subdivision (260 dwellings
in three stages) has asked to connect from 2027; the council's PS03 storage upgrade is in its Long-Term Plan for 2029.
The officers' report goes to the council's 10 December 2026 meeting; every export was pulled on 3 or 4 November 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 1561104

COUNCIL = "Rauwhero District Council"
REGIONAL = "Kahuwera Regional Council"
TOWN = "Rauwhero"
RIVER = "Kahuwera River"
STATION = "PS03"
STATION_NAME = "Riverbank Road"
SUBDIVISION = "Ngaio Road"
CONSENT = "AUTH-2024-0418"
SUB_RM = "RM26-0187"
CLIMATE_SITE = "Rauwhero at Treatment Plant"
CLIMATE_ID = "KRC 1187"
BORE = "72_1043"
BORE_NAME = "Rauwhero Terrace"

PEOPLE = {
    "consents": "Aaliyah Beattie",      # the regional council's consents officer who signed the consent
    "engineer": "Benjamin Gilbert",     # the developer's consulting engineer, author of the servicing report
    "network": "Anaru Boyce",           # the council's wastewater network engineer, owner of the station data sheet
}

UTC = dt.timezone.utc
NZST = dt.timezone(dt.timedelta(hours=12))

# ------------------------------------------------------------------------------------------------- calendar
REPLAY_Y0, REPLAY_Y1 = 2004, 2023          # the consent's record years
METER_D0 = dt.date(2024, 1, 1)             # the station's SCADA export starts
METER_D1 = dt.date(2026, 10, 31)           # last day in every export (NZ time)
PULL = dt.date(2026, 11, 3)
ASOF = dt.date(2026, 11, 4)
MEETING = dt.date(2026, 12, 10)
CONSENT_DATE = dt.date(2024, 3, 18)
COP_DATE = dt.date(2022, 7, 1)
REPORT_DATE = dt.date(2026, 9, 21)         # the developer's servicing report
BRIEF_DATE = dt.date(2026, 8, 12)          # the upgrade project brief
DATASHEET_DATE = dt.date(2023, 11, 7)
POLICY_DATE = dt.date(2023, 7, 1)          # the water metering and billing policy
H0 = dt.datetime(2003, 12, 31, 12, tzinfo=UTC)      # 2004-01-01 00:00 NZST
H1 = dt.datetime(2026, 10, 31, 11, tzinfo=UTC)      # 2026-11-01 00:00 NZDT

# ------------------------------------------------------------------------------------------------- PS03
QP = 112.0                 # L/s, both pumps together, the 2023 drawdown test
STORE = 350.0             # m3 from the duty pump's start level to the overflow weir crest
WET_WELL_STORE = 38.0     # m3 of that in the wet well, the rest in the emergency storage chamber
UPGRADE = 1100.0          # m3 the 2029 tank adds below the weir crest
WEIR_ABOVE_FLOOR = 4.20   # m, the overflow weir crest above the wet well floor
FLOOR_RL = 10.85          # m NZVD2016, the wet well floor
DUTY_START = 1.10         # m above the floor where the duty pump starts
SPILL_SEP_H = 24          # overflows less than 24 hours apart are one overflow (consent condition 3)

# ------------------------------------------------------------------------------------------------- catchment
DWELLINGS_EXISTING = 2151          # PS03 catchment dwellings, steady through the meter
PERSONS_PER_DWELLING = 2.63        # the catchment's own occupancy (census meshblocks); the code of practice uses 2.7
LPD_ACTUAL = 196.0                 # litres per person per day returned to the sewer
SUB_DWELLINGS = (96, 88, 76)       # Ngaio Road stages 1, 2, 3
SUB_YEARS = (2027, 2028, 2029)
COP_LPD = 200.0
COP_OCC = 2.7

# the true response (generator only; nothing ships these)
C0 = 2.1          # L/s of infiltration that never dries (upper terrace, perched water)
G = 4.5           # L/s per km of sewer below the water table
RF = 30.0         # m3 per mm of rain, the fast inflow
RS = 6.0          # m3 per mm of rain per km of sewer below the water table, the rain-induced infiltration
UH_FAST = (1.0, 6)
UH_SLOW = (9.0, 72)


def rng(*keys):
    h = hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def token(*keys, n=6):
    return hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).hexdigest()[:n]


def round_half_up(x, nd=0):
    q = 10 ** nd
    return np.floor(x * q + 0.5) / q
