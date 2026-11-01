"""Every constant the world, the pack and the figures share. One seed; the world is a function of it."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 122
NZ = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc

# The trial: 1 April to 30 September 2026, New Zealand time (NZDT to 5 April, NZST to 27 September, NZDT after).
T0 = dt.datetime(2026, 4, 1, tzinfo=NZ).astimezone(UTC)          # 2026-03-31 11:00 UTC
T1 = dt.datetime(2026, 10, 1, tzinfo=NZ).astimezone(UTC)         # 2026-09-30 11:00 UTC
MINUTES = int((T1 - T0).total_seconds() // 60)                    # 263,520
MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]

SECTORS = ["KPA", "HKI", "WKO", "TKI", "TPO", "KPT"]
SECTOR_NAMES = {"KPA": "KAIPARA", "HKI": "HAURAKI", "WKO": "WAIKATO", "TKI": "TARANAKI", "TPO": "TAUPO",
                "KPT": "KAPITI"}
PAIRS = [("KPA", "HKI"), ("WKO", "TKI"), ("TPO", "KPT")]           # combined overnight
NEXT = {"KPA": "HKI", "HKI": "KPA", "WKO": "TPO", "TKI": "WKO", "TPO": "KPT", "KPT": "TPO"}

# The probe and the activation risk (the truth the golden recovers).
R_TRUE = 0.694           # the probe's multiplier on the activation intensity, the same at every traffic level
BETA = 0.60              # log intensity per climbing or descending aircraft, on top of the aircraft pairs present
CAPACITY = 10            # a sector's declared capacity, aircraft at once (flow management holds the rest)
TARGET = 800             # expected activations per sector over the trial (sets each sector's scale; STCA is tuned
                         # sector by sector)
PROBE_ON_BASE = 0.004    # per-minute switch-on hazard with no climbing or descending traffic beyond one aircraft
PROBE_ON_T = 0.10        # added per climbing or descending aircraft beyond the first
PROBE_ON_N = 0.0         # added per aircraft beyond four
PROBE_BUSY = 0.40        # a busy planner switches the probe on less often (per aircraft beyond five, log scale)
PROBE_OFF_BASE = 0.06
PROBE_OFF_T0 = 0.40      # added when no aircraft is climbing or descending
PROBE_OFF_T1 = 0.15      # added when one is
KEEN_SD = 0.8            # each watch's own habit with the probe (log scale), unrecorded

# Record mess.
P_TIME_REVISION = 0.045  # flights whose plan is revised for time only
P_REROUTE = 0.018        # flights rerouted through another sector by a later revision
P_REENTRY = 0.020        # flights whose route leaves a sector and comes back into it
P_CONTINUATION = 0.08    # activations that carry into the next sector (a second record opens there)
P_INHIBITED = 0.05       # activations inside the approach inhibition volumes (logged, not presented)
PAIR_GAP = 243           # seconds between one pair's alerts, in any sector, other than a hand-over record
ALERT_REACH = 132        # seconds: the furthest an alert's records run past its start, its hand-over record included

ASOF = dt.date(2026, 10, 9)
