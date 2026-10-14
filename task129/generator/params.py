"""task129 parameters: a rural electric cooperative's overhead primary network in three districts, its right-of-way
trimming history and contractors, the weather, and the processes that raise tree-caused outages"""
from datetime import date

SEED = 129227

DISTRICTS = ("North", "East", "South")
DCODE = {"North": "N", "East": "E", "South": "S"}
SUBSTATIONS = {"North": ("Alder Flats", "Kessel Road", "Pine Lick", "Upper Marsh"),
               "East": ("Brannock", "Holloway Mill", "Teal Creek"),
               "South": ("Dunmore Bend", "Five Oaks", "Lyle Junction")}
MILES = {"North": 1800.0, "East": 1250.0, "South": 1150.0}       # overhead primary at the start of 2016
UNIT_MILES = 0.5                                                 # a trim unit is about half a mile of line
UNITS_PER_CIRCUIT = 56
MEMBERS_2025 = {"North": 7914, "East": 5609, "South": 5127}      # members served at the end of 2025
MEMBER_GROWTH = 0.0087
SPANS_PER_MILE = 17.6

# dates
HIST_START = date(2012, 1, 1)        # trimming history kept from
OUT_START = date(2016, 1, 1)         # outage export from
OUT_END = date(2025, 12, 31)
EXPORT = date(2026, 1, 13)
BASE_YEARS = (2021, 2022, 2023)
YEAR = 2025
CYCLE = 4.0

# contractors and handovers
OUTGOING = "Hollenbeck Line Clearance, Inc."
INCOMING = "Garrity Vegetation Services, LLC"
HANDOVER = {"North": date(2024, 1, 1), "East": date(2025, 4, 1)}
NORTH_OPEN_ORDERS = 0.48             # share of North's 2024 campaigns the outgoing firm had been ordered before the handover
NORTH_OPEN_END = date(2024, 12, 20)
EAST_LAST_ORDER = date(2024, 12, 31)
EAST_SLIP_DAYS = (190, 330)          # East campaigns due in 2025 start this many days late

# hazards, per mile-year at a wind multiplier of one
G_AVG = 0.071                        # growth-in, averaged over a four-year cycle
G_POW = 3.2                          # regrowth curve: G_AVG * (G_POW + 1) * (t / 4) ** G_POW
F_BASE = 0.029                       # trees falling in from beyond the right-of-way, before the ash mortality
F_ASH = 0.42                         # added by ash mortality per unit of ash share, at full mortality
ASH_MEAN = {"North": 0.31, "East": 0.12, "South": 0.05}
MORTALITY_ONSET = {"North": date(2024, 3, 4), "East": date(2025, 11, 1), "South": None}
MORTALITY_RAMP_DAYS = 290
MORTALITY_MAX = 1.15
WIND_G, WIND_F = 0.026, 0.048        # exp(k * max(0, gust - 35 mph))
SEASON_G = 0.45                      # growth-in leaf-on season, peak in late July

# other causes (per mile-year unless stated)
OTHER = {"ANIMAL": 0.058, "EQUIPMENT": 0.046, "LIGHTNING": 0.027, "VEHICLE": 0.011, "UNKNOWN": 0.024}
SECONDARY_PER_MEMBER = 0.036         # secondary and service outages per member-year
PLANNED_PER_MILE = 0.045
MOMENTARY_SHARE = 0.09               # recloser operations that clear inside five minutes

# storms: system-wide events that become major event days, and South's 2025 gusty days below them
STORMS = [(date(2016, 7, 21), 140), (date(2017, 3, 8), 95), (date(2017, 11, 18), 120), (date(2018, 6, 29), 175),
          (date(2019, 1, 23), 110), (date(2019, 8, 9), 150), (date(2020, 4, 13), 135), (date(2020, 8, 27), 90),
          (date(2021, 2, 16), 160), (date(2021, 7, 29), 115), (date(2022, 6, 14), 185), (date(2022, 12, 23), 130),
          (date(2023, 4, 1), 105), (date(2023, 7, 12), 150), (date(2024, 5, 8), 140), (date(2024, 10, 30), 100),
          (date(2025, 6, 18), 210), (date(2025, 12, 9), 125)]
SOUTH_GUSTY_2025 = 13
NORTH_WET_2024 = 1.65                # May to September 2024 rainfall in North against normal

DISTRACTORS = ("benchmark", "ami")
