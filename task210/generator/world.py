"""World constants for task210 architecture 2: Ashcombe Regional Transit's streetcar.

Everything the generator needs to build the clean truth is here: the network, the service, the effects behind the
firm-brake record, the operators, the fleet, the windows and the seed. Nothing here ships.
"""
import math

SEED = 21019            # shipped seed (selected on the corrected-sun screens, asserted in checks.py)
LAT0, LON0 = 38.700, -104.905   # Civic Center, Ashcombe (fictional city on the Front Range, America/Denver)
TZ = "America/Denver"

OBS_START, OBS_END = "2026-04-01", "2026-10-31"      # recorder record (new recorders commissioned in March)
PICK_START, PICK_END = "2027-01-04", "2027-02-26"    # January pick, weekdays, federal holidays run Sunday service
PICK_HOLIDAYS = ["2027-01-18", "2027-02-15"]          # Martin Luther King Jr. Day, Presidents' Day
OBS_HOLIDAYS = ["2026-05-25", "2026-07-03", "2026-09-07"]  # Memorial Day, Independence Day observed, Labor Day
PEAKS = {"AM": (6 * 60 + 30, 9 * 60), "PM": (16 * 60, 18 * 60 + 30)}   # SRM-07 weekday peak windows, minutes local
CAP = 4                                               # restricted-speed slots the January pick's running times carry
# The January pick's revised running times: seconds added to each section's base time, (outbound, inbound), from the
# scheduling department's direction-by-direction review (grades, signal phasing, stop positions)
PICK_RUN_ADJ = {"J1": (6, -2), "J2": (-3, 4), "J3": (0, 5), "J4": (4, -4), "J5": (-2, 3), "J6": (5, 1),
                "F1": (-4, 3), "F2": (2, -3), "F3": (5, 1), "F4": (-1, 6), "F5": (3, -2), "F6": (1, 4), "F7": (-5, 2)}

# Network: (section, line, from stop, to stop, outbound bearing in degrees true, length m, track type)
LINES = {
    "J": ("Juniper Line", "Mesa Park", "Union Yard"),
    "F": ("Foundry Line", "Northfield", "Foundry Loop"),
}
SECTIONS = [
    ("J1", "J", "Mesa Park", "Laurel Street", 165, 980, "street"),
    ("J2", "J", "Laurel Street", "Civic Center", 92, 760, "street"),
    ("J3", "J", "Civic Center", "Market Square", 99, 690, "street"),
    ("J4", "J", "Market Square", "Harlan Avenue", 125, 820, "street"),
    ("J5", "J", "Harlan Avenue", "Sandoval Street", 131, 740, "street"),
    ("J6", "J", "Sandoval Street", "Union Yard", 128, 1460, "reserved"),
    ("F1", "F", "Northfield", "Garnet Street", 182, 910, "street"),
    ("F2", "F", "Garnet Street", "Pike Street", 197, 700, "street"),
    ("F3", "F", "Pike Street", "Arsenal Road", 264, 780, "street"),
    ("F4", "F", "Arsenal Road", "Tallow Street", 272, 720, "street"),
    ("F5", "F", "Tallow Street", "Kiln Avenue", 231, 860, "street"),
    ("F6", "F", "Kiln Avenue", "Smelter Row", 237, 790, "street"),
    ("F7", "F", "Smelter Row", "Foundry Loop", 268, 1380, "reserved"),
]
# Each line's first stop offset from the origin (metres east, metres north); the lines cross downtown on parallel
# streets (Laurel and Market for the Juniper, Pike and Arsenal for the Foundry).
LINE_START = {"J": (-1200.0, 1100.0), "F": (300.0, 1700.0)}
SPEED_KMH = {"street": 19.0, "reserved": 38.0}       # scheduled running speed between stops
DWELL_S = 25

# Service: headway minutes by day type and period (local); 06:00 to 24:00
HEADWAY = {"weekday": [(6 * 60, 6 * 60 + 30, 10.0), (6 * 60 + 30, 19 * 60, 7.5), (19 * 60, 24 * 60, 10.0)],
           "saturday": [(6 * 60, 24 * 60, 10.0)],
           "sunday": [(7 * 60, 23 * 60, 15.0)]}
TWO_CAR = {"J": [(6 * 60 + 30, 9 * 60 + 30), (15 * 60 + 30, 18 * 60 + 45)]}  # Juniper peak strengthening, weekdays
TWO_CAR_BLOCKS = ["J01", "J02"]                       # 11 Juniper cars: 9 leads and the 2 trailing cars

# Effects behind the firm-brake (FB) record, per pass
BASE = {"street": 20.0, "reserved": 8.0}             # per 1,000 passes
HOUR_F = {6: 1.0, 7: 1.0, 8: 1.0, 16: 1.08, 17: 1.08, 18: 1.08, 21: 0.8, 22: 0.8, 23: 0.8}  # others 0.9
WEEKEND_F = 0.85
DARK = {"street": 0.30, "reserved": 0.15}            # multiplier minus one when the sun is below -3 degrees
NEW_OP = 0.30                                        # first 60 days in revenue service
SCHOOL = 0.10                                        # street, weekday mornings 06:30-09:00 on school days
SCHOOL_TERMS = [("2026-04-01", "2026-05-22"), ("2026-08-17", "2026-10-31"), ("2027-01-05", "2027-03-12")]
SCHOOL_BREAKS = [("2026-03-30", "2026-04-03"), ("2026-10-12", "2026-10-16")]
SECTION_SD = 0.05                                    # lognormal spread of each section direction's base
G_TRUE = 2.2                                         # full-alignment, full-sun glare multiplier minus one
CONE, E_FULL, E_ZERO = 25.0, 12.0, 25.0              # cone half-width; full below E_FULL, zero at E_ZERO degrees

# Sunshine: percent of possible, monthly normals for the airport station (1991-2020), and sky-cover mapping
SUN_NORM = {1: 68, 2: 68, 3: 66, 4: 64, 5: 62, 6: 70, 7: 66, 8: 66, 9: 72, 10: 71, 11: 66, 12: 66}
SKY_SUN = {"CLR": 1.0, "FEW": 1.0, "SCT": 1.0, "BKN": 0.0, "OVC": 0.0}   # sun visible below scattered cloud

# Other recorder events (per 1,000 passes): emergency loop (EB), overspeed (OS)
EB_RATE = {"street": 1.2, "reserved": 0.5}
OS_RATE = {"street": 1.6, "reserved": 2.4}
OS_NEW_F = 1.9                                       # overspeed multiplier in an operator's first 90 days

# Fleet and operators
CARS = {"J": list(range(101, 112)), "F": list(range(121, 131))}
OPERATORS_N = 128
TRAINING_CLASSES = [("26-1", "2026-02-16", 9), ("26-2", "2026-05-11", 10), ("26-3", "2026-08-31", 11)]
BADGE_MIGRATION = "2026-07-13"                       # HR system migration: 4-digit badges become 6-digit

SWAP_P = 0.42                                        # Foundry weekdays with a car bad-ordered in service
LOOP_SLOW_P = 0.3                                    # outbound F7 applications made at walking pace in Foundry Loop
ASK_B_DAYS = 30                                      # ask B's window from each operator's first solo revenue run

# Distractor and context drivers
ARENA_EVENTS_N = 46
