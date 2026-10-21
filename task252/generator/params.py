"""task252 constants: Fernvale District Council's eight water treatment plants, their three-stream ammonia
analysers, the fourth quarter of 2027 in New Zealand time, and the seeds."""
import datetime as dt
from zoneinfo import ZoneInfo

ORG = "Fernvale District Council"
UNIT = "Water Services"
LAB = "Kowhai Bay Analytical"
NZ = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc

SEED_WORLD = 45            # the analysers and the water (prototype cw12, seed 45)
SEED_OPS = 2521            # faults, telemetry, checks' dates, the sampling round, the laboratory
SEED_DOCS = 2522           # distractors' values
SEED_LAB = 2560            # the sampling round, the courier and the laboratory's bench
SEED_TELEM = 2523          # the telemetry renewal: each plant's outstation change in November
SEED_REPAIR = 2524         # the technicians' checks on the standard after clearing a fault
SEED_DUP = 2525            # the laboratory's second logging of the delayed 7 December round
SEED_SIGNAL = 2526         # signal faults: a port's reading lost between the analyser and the PLC
SEED_BENCH = 2527          # the bench's start each morning and the release of each run's results
SEED_TRIP = 2528           # the storm nights: each analyser's supply tripping and the operator's reset

PLANTS = [("ASH", "Ashcombe"), ("BRN", "Brannock"), ("CAL", "Calderwood"), ("DUN", "Dunmere"), ("ELS", "Elstow"),
          ("FEN", "Fenwick"), ("GAR", "Garrick"), ("HOL", "Holmedale")]
CODES = [c for c, _ in PLANTS]
NAME = dict(PLANTS)
WORN = {"BRN", "DUN", "ELS", "GAR", "HOL"}          # cell and sample valve worn: carryover from the two ports before
WEAK = {"ASH", "DUN", "FEN"}                         # raw-water ammonia passes through to treated water
HIGH = {"CAL", "GAR", "HOL"}                         # dairy catchments: raw ammonia two to three times the others'
ZERO = {"HOL": -0.0085}                              # contaminated zero water: reads low by a constant
GAIN = {"CAL": 0.91}                                 # weak reagent: reads low in proportion
FOUL = {"CAL": (0.65, 2.0), "HOL": (0.95, 2.0)}      # unchlorinated filtered sample line's nitrifying film: share of
                                                     # the ammonia it takes when grown, days to grow back after a flush
FIL_LIFT = {"HOL": 0.0035}                            # Holmedale's filtered water a little above the others'
STORMS = {(2027, 10, 26): ("ASH", "CAL", "DUN", "GAR"),       # nights whose lightning tripped four analysers' supply
          (2027, 12, 3): ("BRN", "ELS", "FEN", "HOL")}
ORDER = {"ASH": "rnf", "BRN": "rnf", "CAL": "rfn", "DUN": "rnf", "ELS": "rnf", "FEN": "rnf", "GAR": "rfn",
         "HOL": "rfn"}
STREAM = {"r": "raw", "f": "fil", "n": "fin"}
SP = {"raw": "RW1", "fil": "FI1", "fin": "FW1"}
WATER = {"raw": "Raw", "fil": "Filtered", "fin": "Final"}

SLOT_MIN = 10
DAYS = 92
NS = DAYS * 144                                       # ten-minute port slots in the quarter
Q_START = dt.datetime(2027, 10, 1, tzinfo=NZ)         # 2027-09-30 11:00 UTC
Q_END = dt.datetime(2028, 1, 1, tzinfo=NZ)            # 2027-12-31 11:00 UTC
T0 = Q_START.astimezone(UTC)

THRESH = 0.005             # WQ-DS-04 section 4
CHECK_STD = 0.100
CHECK_TOL = 0.10
LOD = 0.030
HOLD_H = 24                # holding time, hours from collection to analysis
DOSE_HOLD_H = 2            # the dose controller holds the last good filtered reading this long
CL_PER_N = 7.6             # mg/l chlorine per mg/l ammonia as N (process summary, the feed-forward)


def tag(code):
    return "AQ-%s-NH3" % code


def point(code, stream):
    return "%s-%s" % (code, SP[stream])


def slot_end(i):
    """the UTC end of slot i (the reading's timestamp)"""
    return T0 + dt.timedelta(minutes=SLOT_MIN * (i + 1))


def slot_of(t):
    """the slot whose ten minutes contain the instant t (aware datetime)"""
    return int((t.astimezone(UTC) - T0).total_seconds() // (60 * SLOT_MIN))
