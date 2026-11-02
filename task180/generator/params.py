"""World parameters for task180 architecture 5: Tamarack Prairie Co-operative's gas bar tank systems and
cardlocks, east-central Saskatchewan and western Manitoba, January 2024 to the first business day of 2027.

Every figure the pack carries is computed forward from these parameters by world.py; nothing is fixed
first and reverse-engineered. The design note's ladder numbers are measured on the world these produce.
"""
import datetime as dt

SEED = 180_5
START = dt.date(2024, 1, 1)          # first business day in the record
END = dt.date(2026, 12, 31)          # last business day in the record
Q4 = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
AS_OF = dt.date(2027, 1, 5)          # the extracts are pulled on this day
THRESHOLD_LPH = 0.75                 # PD-07's line, litres an hour

# Meter drift: millilitres per 20-litre draft gained per 100,000 litres passed since the meter was last
# set, the same rate for every meter in the co-op's fleet of dispensers (one dispenser line), each meter's
# own rate scattered about it. A calibration sets a meter back to zero with a small as-left scatter.
DRIFT_ML_PER_100K = 6.0
DRIFT_METER_SD = 0.05                # relative scatter of each meter's own rate
AS_LEFT_SD_ML = 1.2                  # as-left scatter after a calibration, mean zero

ATG_NOISE_L = 2.0                    # tank gauge net-volume reading noise, litres
TERMINAL_SD = 0.0003                 # terminal meter scatter on a bill of lading (relative)

# ---------------------------------------------------------------- the gas bars
# code, town, province, fuelling points, regular, premium, diesel (litres a day at the season's mean),
# diesel fuelling points, regular and diesel tank capacities (litres), premium capacity
SITES = [
    ("GB-118", "Wynyard", "SK", 6, 6120, 694, 2560, 2, 50000, 50000, 25000),
    ("GB-121", "Foam Lake", "SK", 8, 9380, 902, 28700, 6, 50000, 90000, 25000),
    ("GB-124", "Wadena", "SK", 4, 5160, 483, 2170, 2, 50000, 40000, 25000),
    ("GB-127", "Kelvington", "SK", 4, 3630, 352, 1930, 2, 40000, 40000, 20000),
    ("GB-131", "Ituna", "SK", 4, 2790, 262, 1510, 2, 35000, 35000, 20000),
    ("GB-134", "Canora", "SK", 8, 7200, 700, 3110, 2, 50000, 50000, 25000),
    ("GB-139", "Preeceville", "SK", 4, 4220, 383, 1720, 2, 40000, 40000, 20000),
    ("GB-142", "Kamsack", "SK", 8, 13560, 1214, 3100, 2, 60000, 50000, 25000),
    ("GB-146", "Langenburg", "SK", 4, 3950, 361, 1640, 2, 40000, 40000, 20000),
    ("GB-153", "Russell", "MB", 6, 6830, 612, 2690, 2, 50000, 50000, 25000),
    ("GB-157", "Roblin", "MB", 4, 5570, 518, 2320, 2, 50000, 40000, 25000),
    ("GB-160", "Grandview", "MB", 4, 3320, 301, 1470, 2, 40000, 40000, 20000),
]

# Calibrations: the contractor proves and adjusts every meter at the gas bar on the day (the work order's
# date), or only the dispensers listed. Dates fall in 2024 to 2026 so every meter's litres since its last
# setting are in the sales record.
CALIBRATIONS = {
    "GB-118": ["2024-02-21", "2025-04-08", "2026-06-17"],
    "GB-121": ["2024-03-12", "2024-09-24", "2025-04-01", "2025-10-14", "2026-03-31", "2026-08-11"],
    "GB-124": ["2024-05-07", "2026-03-24"],
    "GB-127": ["2024-01-30", "2025-09-16"],
    "GB-131": ["2024-04-23", "2025-05-14"],
    "GB-134": ["2024-11-05", "2026-07-02"],
    "GB-139": ["2024-08-20", "2026-05-05"],
    "GB-142": ["2024-06-18", ("2025-04-15", [1, 2, 3, 4])],   # the diesel dispenser was not done in 2025
    "GB-146": ["2024-03-26", "2025-10-07"],
    "GB-153": ["2024-07-09", "2025-11-18"],
    "GB-157": ["2024-09-24", "2026-04-14"],
    "GB-160": ["2024-02-06", "2025-06-24"],
}
# single dispensers or meters replaced (new meters set at the factory)
DISPENSER_SWAPS = [("GB-124", 2, "2025-07-15")]     # Wadena dispenser 2 (fuelling points 3 and 4)
METER_SWAPS = [("GB-153", 4, "R", "2025-03-11"), ("GB-118", 2, "D", "2026-01-20")]

# The two releases the quarter carries. Ituna's 1987 steel regular tank has corroded through near the
# bottom and loses product whatever it sells; Canora's regular line was disturbed when its submersible
# pump was replaced on the calibration visit of 2 July 2026 and weeps at the pump's discharge union
# while the line is under pressure, which is only while the pump runs, so in step with the litres sold.
TANK_LEAK = {("GB-131", "R"): (dt.date(2026, 7, 3), 1.21)}          # litres an hour, from the date
LINE_LEAK = {("GB-134", "R"): (dt.date(2026, 7, 2), 0.0035)}     # share of litres pumped

# ---------------------------------------------------------------- carriers and terminals
CARRIERS_GB = {"Prairie Lake Haulage": 0.62, "Touchwood Tank Lines": 0.38}
TERMINALS = ["Regina", "Saskatoon", "Brandon"]

# ---------------------------------------------------------------- the cardlocks (the ask)
# code, town, province, diesel pumps, regular pumps, diesel litres a day, regular litres a day,
# diesel tank, regular tank
CARDLOCKS = [
    ("CL-401", "Wynyard", "SK", 3, 1, 12600, 2150, 60000, 30000),
    ("CL-404", "Canora", "SK", 3, 1, 13600, 1850, 60000, 30000),
    ("CL-407", "Kamsack", "SK", 4, 1, 15900, 2400, 80000, 30000),
    ("CL-412", "Russell", "MB", 3, 1, 11900, 2050, 60000, 30000),
]
CARRIERS_CL = {"Whitesand Tankline": 0.74, "Touchwood Tank Lines": 0.26}
# Whitesand's cardlock route driver keeps product back on some drops at the unattended sites
SHORT_DROP = {"carrier": "Whitesand Tankline", "share": 0.38, "litres": (110, 330)}
# a power cut at the Kamsack cardlock while a Whitesand diesel drop went in off the truck's own pump
OUTAGE = {"site": "CL-407", "start": dt.datetime(2026, 11, 19, 9, 40), "end": dt.datetime(2026, 11, 19, 15, 5)}

PRODUCTS = {"R": "Regular 87", "P": "Premium 91", "D": "Diesel"}
# the cardlock consoles keep their last ten delivery reports per tank; the controller's office pulls them
# through the monitoring service at each month-end close
REPORT_DEPTH = 10
REPORT_PULLS = [dt.datetime(2026, 11, 2, 8, 34), dt.datetime(2026, 12, 1, 8, 27), dt.datetime(2027, 1, 5, 8, 41)]
# the monitoring service could not reach two consoles on the October pull; nobody pulled them again
PULL_MISSED = {(dt.datetime(2026, 11, 2, 8, 34), "CL-401"), (dt.datetime(2026, 11, 2, 8, 34), "CL-412")}

# Spring water draw-offs by the vacuum truck (water and some product, litres); recorded only on the hauler's
# manifest. site, product, date, water, product
VACUUM_PUMPOUTS = [
    ("GB-127", "R", "2024-05-14", 212, 46), ("GB-127", "D", "2024-05-14", 158, 61),
    ("GB-139", "D", "2025-05-06", 241, 38), ("GB-146", "R", "2025-05-06", 117, 52),
    ("GB-160", "R", "2026-04-28", 186, 44), ("GB-124", "D", "2026-04-28", 133, 57),
]

# ---------------------------------------------------------------- the operating record around the tanks
# Service contractors: which gas bars each one covers, and its technicians (guard.py names, seed 180)
CONTRACTORS = {
    "Quill Lakes Petroleum Service": dict(sites=["GB-118", "GB-121", "GB-124", "GB-127", "GB-131", "GB-134"],
                                          techs=["Antonio Schwartz", "Arthur Curtis"]),
    "Spirit Creek Pump & Meter": dict(sites=["GB-139", "GB-142", "GB-146", "GB-153", "GB-157", "GB-160"],
                                       techs=["Benjamin Bautista"]),
}
# submersible pump replacements (site, product, date): routine, at several sites
STP_REPLACEMENTS = [("GB-160", "D", "2024-07-16"), ("GB-121", "D", "2024-12-03"), ("GB-142", "R", "2025-08-27"),
                    ("GB-139", "R", "2025-10-21"), ("GB-127", "R", "2026-04-07"), ("GB-134", "R", "2026-07-02")]
# a gauge probe replaced, with a small step in the gauge's net reading after it (litres)
PROBE_REPLACEMENTS = [("GB-139", "D", "2025-02-18", -31), ("GB-153", "P", "2026-03-03", 22)]
# terminals by site (gas bars and cardlocks)
TERMINAL_OF = {"GB-118": "Saskatoon", "GB-121": "Saskatoon", "GB-124": "Saskatoon", "GB-127": "Saskatoon",
               "GB-131": "Regina", "GB-134": "Regina", "GB-139": "Regina", "GB-142": "Regina", "GB-146": "Regina",
               "GB-153": "Brandon", "GB-157": "Brandon", "GB-160": "Brandon",
               "CL-401": "Saskatoon", "CL-404": "Regina", "CL-407": "Regina", "CL-412": "Brandon"}
# the December point-of-sale export was taken twice: a preliminary on 2 January and the re-export on
# 5 January after Roblin's forecourt controller posted the sales it held through a comms fault on 14 December
POS_REEXPORT = dict(site="GB-157", day=dt.date(2026, 12, 14), held_share=0.19)
PEOPLE = dict(controller="Leah Haynes", petroleum_manager="Roy Turner",
              vac_driver="Jimmy Contreras", lld_tech="Joshua Kirk", cp_tech="Julia Peterson")
# tank construction by site: (construction, installed, piping); exceptions by (site, product)
TANK_BUILD = {
    "GB-118": ("Double-wall fibreglass", 2008, "Flexible double-wall"),
    "GB-121": ("Double-wall fibreglass", 2012, "Flexible double-wall"),
    "GB-124": ("Double-wall fibreglass", 2004, "Flexible double-wall"),
    "GB-127": ("STI-P3 steel", 1993, "Fibreglass single-wall"),
    "GB-131": ("STI-P3 steel", 1995, "Fibreglass single-wall"),
    "GB-134": ("Single-wall fibreglass", 1994, "Fibreglass single-wall"),
    "GB-139": ("Double-wall fibreglass", 2010, "Flexible double-wall"),
    "GB-142": ("Double-wall fibreglass", 2006, "Flexible double-wall"),
    "GB-146": ("STI-P3 steel", 1997, "Fibreglass single-wall"),
    "GB-153": ("Double-wall fibreglass", 2014, "Flexible double-wall"),
    "GB-157": ("Double-wall fibreglass", 2009, "Flexible double-wall"),
    "GB-160": ("Double-wall fibreglass", 2001, "Flexible double-wall"),
}
TANK_BUILD_EXCEPT = {("GB-131", "R"): ("Single-wall steel, galvanic anodes", 1987, "Fibreglass single-wall"),
                     ("GB-160", "D"): ("STI-P3 steel", 1998, "Flexible double-wall")}
