"""World parameters for Hallowfen Ambulance Service's 2027 cab specification. Every figure the pack, the goldens and
the write-up state is computed from these by the generator; nothing graded is typed anywhere else."""
import datetime as dt

SEED = 276
YEAR_STREAM = 156                # the fleet year's random stream
ROSTER_DATE = dt.date(2026, 10, 1)            # the front-line driving roster the order is bought for
PACK_DATE = dt.date(2026, 10, 9)              # the day the committee pack was assembled
FY = (dt.date(2025, 4, 1), dt.date(2026, 3, 31))
QUARTERS = [("Q1", dt.date(2025, 4, 1), dt.date(2025, 6, 30)), ("Q2", dt.date(2025, 7, 1), dt.date(2025, 9, 30)),
            ("Q3", dt.date(2025, 10, 1), dt.date(2025, 12, 31)), ("Q4", dt.date(2026, 1, 1), dt.date(2026, 3, 31))]
HR_MIGRATION = dt.date(2025, 9, 1)            # Vennerley staff numbers replaced by service numbers
IMPERIAL_FORMS_UNTIL = dt.date(2025, 8, 1)    # Vennerley OH paper forms (feet, inches, stones, pounds)
WORKSHOP_CUTOVER = dt.date(2025, 7, 1)        # Vennerley workshop system closed, vehicles renumbered
PROGRAMME = (dt.date(2025, 3, 3), dt.date(2026, 9, 25))   # the cab fit measurement programme

# hubs: code, name, area, drivers on the October 2026 roster (drawn around these)
HUBS = [
    ("BQY", "Strakemoor Quay", "Strakemoor", 318), ("BMG", "Tollmarsh", "Strakemoor", 276), ("BFL", "Hallowfen MRC", "Strakemoor", 341),
    ("BLA", "Hallowfen Moor", "Strakemoor", 247), ("BBX", "Beacon Cross", "Strakemoor", 296), ("VWB", "Weir Bank", "Vennerley", 304),
    ("VCF", "Vennerley Central", "Vennerley", 262), ("VSC", "Vennerley Bridge", "Vennerley", 329), ("VOM", "Old Mill Yard", "Vennerley", 271),
]
WOMEN_SHARE = 0.47
ROLES = [("Paramedic", 0.44), ("Emergency Medical Technician", 0.31), ("Ambulance Support Worker", 0.25)]

# bodies: stature mean and sd by sex, body mass index (lognormal), sitting eye height as a share of stature
STATURE = {"F": (1631.0, 63.0), "M": (1760.0, 69.0)}
BMI = {"F": 27.4, "M": 28.1}
BMI_SPREAD = 0.16
SEH_RATIO = {"F": 0.468, "M": 0.462}
SEH_SPREAD = 0.011

# the service's driver posture model (Ellisand Human Factors, July 2025); x is aft of the accelerator heel point,
# z above it, millimetres; the torso angle is from vertical, degrees
POSTURE = {"hx0": 792.0, "hx_s": 0.61, "hx_b": 2.6, "hx_h": -0.95, "s0": 1700.0, "b0": 27.0, "h0": 400.0,
           "t0": 19.0, "t_s": 0.011, "t_b": 0.09, "ex": -18.0, "ez": 0.955}

# the seat every converter fits (Brevin AS-7), as its maker's sheet states it in inches
SEAT_IN = {"backrest_along": 30.31, "backrest_behind": 3.74, "recline_min": 8.0, "recline_max": 34.0,
           "slide_standard": 9.45, "slide_long": 9.84, "slide_extended": 10.55}

# the standard's vision zone, the same for every cab
VISION = {"up_deg": 11.0, "down_deg": 5.0}

# chassis vision points (x, z from the heel point): windscreen header, lowest visible road edge over the bonnet
CHASSIS = {"FD35": {"header": (110, 1440), "bonnet": (-310, 960)},
           "RD43": {"header": (95, 1418), "bonnet": (-290, 980)}}

# the five shortlisted cabs: converter, chassis, seat height, slide, hip-point travel, bulkhead trim face line
CABS = [
    {"id": "PEN-FD35", "converter": "Pennick Coachbuild", "chassis": "FD35", "h30": 408, "slide": "long",
     "travel": (700, 950), "bulkhead": (1445, 1392)},
    {"id": "PEN-RD43", "converter": "Pennick Coachbuild", "chassis": "RD43", "h30": 421, "slide": "long",
     "travel": (712, 962), "bulkhead": (1460, 1405)},
    {"id": "WRE-FD35", "converter": "Wrenfold Bodies", "chassis": "FD35", "h30": 405, "slide": "extended",
     "travel": (690, 958), "bulkhead": (1300, 1160)},
    {"id": "WRE-RD43", "converter": "Wrenfold Bodies", "chassis": "RD43", "h30": 406, "slide": "extended",
     "travel": (694, 962), "bulkhead": (1305, 1168)},
    {"id": "OST-FD35", "converter": "Ostrel Vehicle Conversions", "chassis": "FD35", "h30": 414, "slide": "standard",
     "travel": (712, 952), "bulkhead": (1415, 1330)},
]
BULKHEAD_TOP_Z = 1700            # the drawings give the trim face at the floor and 1,700 mm above it
WRENFOLD_SGRP = {"FD35": (845, 405), "RD43": (851, 406)}   # Wrenfold dimensions from each cab's SgRP
DEAD_ZONE_MM = 1.5               # no driver's hip point or backrest corner within this of a limit
DEAD_ZONE_DEG = 0.05             # no driver's sight line within this of the vision angle

# the current front-line fleet in 2025-26: converter, chassis, vehicles in service at 1 April 2025
FLEET = [("Pennick Coachbuild", "FD35", 44), ("Pennick Coachbuild", "RD43", 27), ("Ostrel Vehicle Conversions", "FD35", 36),
         ("Corvane Coachworks", "FD35", 29), ("Corvane Coachworks", "RD43", 25)]
NEW_IN_FY = [("Ostrel Vehicle Conversions", "FD35", 9), ("Pennick Coachbuild", "RD43", 6)]
DISPOSALS_IN_FY = 15
REISSUED_NUMBERS = 6              # disposed vehicles' fleet numbers given to new vehicles
UNIT_SWAPS = 21                   # telematics units replaced during the year
DAILY_MILES = (95.0, 0.32)        # lognormal median and spread of a front-line vehicle's day
# seat and cab-structure jobs per vehicle-year, and all other jobs per vehicle-year, by converter
SEAT_CAB_RATE = {"Pennick Coachbuild": 3.9, "Ostrel Vehicle Conversions": 3.4, "Corvane Coachworks": 5.8}
OTHER_JOB_RATE = 30.0
VOR_SHARE = 0.22                  # share of jobs that take the vehicle off the road
