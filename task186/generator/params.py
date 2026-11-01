"""Fixed world parameters for task186 (architecture 2). Every random draw comes from SEED through world.py."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 186
TZ = ZoneInfo("Australia/Sydney")
UTC = dt.timezone.utc

DAY0 = dt.date(2025, 7, 1)          # domestic CT lanes commissioned
INTL_CT = dt.date(2025, 9, 1)       # international CT lanes commissioned
WIN0 = dt.date(2025, 12, 1)         # assessment window opens (local date)
WIN1 = dt.date(2026, 11, 30)        # assessment window closes (local date, inclusive)
AS_OF = dt.date(2026, 12, 2)        # extracts pulled
STAMP = (2026, 12, 2, 9, 10, 0)     # zip entry time of every shipped file

DOM = ["D1", "D2", "D3", "D4", "D5"]
INTL = ["I1", "I2"]
LANES = DOM + INTL

# Opening hours, local, minutes after midnight, per day type. Each list holds open intervals.
HOURS = {
    "D1": {"wk": [(270, 1290)], "we": [(270, 1290)]},
    "D2": {"wk": [(270, 1290)], "we": [(270, 1290)]},
    "D3": {"wk": [(300, 1230)], "we": [(300, 1230)]},
    "D4": {"wk": [(330, 810), (900, 1200)], "we": [(330, 810), (900, 1200)]},
    "D5": {"wk": [(360, 660), (930, 1170)], "we": [(420, 720)]},
    "I1": {"wk": [(300, 780), (1020, 1380)], "we": [(300, 780), (1020, 1380)]},
    "I2": {"wk": [(450, 930), (1140, 1410)], "we": [(450, 930), (1140, 1410)]},
}
# Mean passenger bags an hour at a lane's busiest time; shaped by hour, weekday and month in world.py.
LANE_BASE = {"D1": 205, "D2": 198, "D3": 176, "D4": 160, "D5": 132, "I1": 150, "I2": 138}

TIP_RATE = 0.013         # projected threat images per bag, every CT lane
SLOT_MIN = 20            # officers on a lane take the X-ray screen in turn, twenty minutes each
MEMORY = 0.12            # each earlier showing of an object leaves this share of the miss probability
VIEWS = 3                # scans of each threat object in the library
N_OBJ = 360              # threat objects in the CT library
CATS = [("FA", "GUN", "Firearms and parts", 0.45, 0.21),
        ("KB", "KNF", "Knives and bladed items", 0.00, 0.30),
        ("IE", "IED", "Improvised explosive device components", -0.40, 0.25),
        ("OP", "OTH", "Other prohibited items", -0.15, 0.24)]
STANDARD = 0.80          # detection performance below this takes an officer off X-ray duty
CURRENCY_H = 20.0        # monthly hours at an X-ray screen an endorsed officer must reach

# Scanner serials and their history (the register only knows where each unit stands now).
SCANNERS0 = {"D1": "KX6-0412", "D2": "KX6-0413", "D3": "KX6-0414", "D4": "KX6-0415", "D5": "KX6-0416",
             "I1": "KX6-0471", "I2": "KX6-0472"}
D2_FAULT = dt.date(2026, 3, 3)       # KX6-0413 fails on D2; D2 closed 3 and 4 March
D2_NEW = dt.date(2026, 3, 5)         # KX6-0590 commissioned on D2
D5_SWAP = dt.date(2026, 4, 20)       # repaired KX6-0413 replaces KX6-0416 on D5; 0416 becomes the spare
NEW_D2 = "KX6-0590"
RETROFIT = [("D1", dt.date(2026, 6, 9)), ("D3", dt.date(2026, 6, 23)), ("D4", dt.date(2026, 7, 7)),
            ("I1", dt.date(2026, 7, 21)), ("I2", dt.date(2026, 8, 4)), ("D2", dt.date(2026, 8, 18)),
            ("D5", dt.date(2026, 9, 1))]     # each lane's own unit out two days, the spare in its place
TEST_IMAGES = (34, 46)                       # daily performance-test images a unit counts after its retrofit
SERVER_MERGE = dt.date(2026, 3, 1)           # international TIP server folded into the domestic one
RESEND_DAY = dt.date(2026, 2, 17)            # D3's TIP records for this day re-sent after a network outage

DEF_FT = (0.64, 0.72)    # detection of an unseen item, full-time officers below standard
DEF_PT = (0.58, 0.64)    # detection of an unseen item, casual officers endorsed in 2025, below standard
CA_T = (0.90, 0.93)      # casual officers at standard
COMP_T = (0.89, 0.95)    # full-time and part-time officers at standard
N_CA_D, N_CA_I = 10, 4
