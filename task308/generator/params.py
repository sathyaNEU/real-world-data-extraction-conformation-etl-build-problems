"""task308 architecture 3: Prairie Hollow Power Cooperative's 2027 capacity award. Every constant the world, the pack
and the checks share lives here."""

SEED = 30804
TZ = "America/Chicago"
YEARS = list(range(2016, 2026))           # the ten recorded weather years the standard replays
N_YEARS = len(YEARS)
START_UTC = "2016-01-01 06:00"            # local midnight, 1 January 2016 (CST)
END_UTC = "2026-01-01 05:00"              # the last hour of 2025, local

# ---------------------------------------------------------------------------------------------- weather and load
LOAD_SCALE = 0.95
COOL_COEF = 40.0
CURT_TEMP_F = -10.0       # Northgate declares interruptible curtailment after three hours below this at the hub
CURT_PERSIST_H = 3
CURT_TAIL_H = 6           # and lifts it six hours after the hub warms past it
WIND_EX_MW = 800.0
SOLAR_EX_MW = 400.0

# ---------------------------------------------------------------------------------------------- the 2027 fleet
# unit_code, plant, unit, class, MW (net winter), forced outage rate, mean repair hours, gas transport
UNITS = [
    ("PH-101", "Hollow Creek", "Nuclear share", "nuclear", 520, 0.020, 140, ""),
    ("PH-110", "Big Bend", "Hydro", "hydro", 140, 0.010, 20, ""),
    ("PH-122", "Sandoval", "Unit 2", "coal", 450, 0.060, 60, ""),
    ("PH-131", "Marsh Lake", "CC1", "combined cycle", 380, 0.035, 30, "firm"),
    ("PH-132", "Marsh Lake", "CC2", "combined cycle", 380, 0.035, 30, "firm"),
    ("PH-141", "Elk Prairie", "CT1", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-142", "Elk Prairie", "CT2", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-143", "Elk Prairie", "CT3", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-144", "Elk Prairie", "CT4", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-145", "Torrance", "CT1", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-146", "Torrance", "CT2", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-147", "Torrance", "CT3", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-148", "Torrance", "CT4", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-149", "Wexford", "CT1", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-150", "Wexford", "CT2", "combustion turbine", 90, 0.042, 18, "interruptible"),
    ("PH-161", "Coldwater", "Engine 1", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
    ("PH-162", "Coldwater", "Engine 2", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
    ("PH-163", "Coldwater", "Engine 3", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
    ("PH-164", "Coldwater", "Engine 4", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
    ("PH-165", "Coldwater", "Engine 5", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
    ("PH-166", "Coldwater", "Engine 6", "reciprocating engine", 18, 0.030, 12, "firm (LDC), diesel backup"),
]
# in the log, not in the 2027 fleet: Sandoval 1 retires on 31 December 2026
RETIRED = [("PH-121", "Sandoval", "Unit 1", "coal", 420, 0.07, 60, "")]
CT_CLASS = [u[0] for u in UNITS if u[3] == "combustion turbine"]

IMPORT_EX_MW = 200.0      # Red Willow firm import already contracted over the tie
TIE_FOR = 0.012
TIE_MTTR = 26

# ---------------------------------------------------------------------------------------------- the four offers
VOLL = 20000.0            # dollars per MWh unserved, the standard's value of lost load
OFFERS = ["Ketchum Ridge", "Red Willow import", "Sandhill Draw", "Coulee Flats"]
OFFER_MW = {"Ketchum Ridge": 300.0, "Red Willow import": 300.0, "Sandhill Draw": 450.0, "Coulee Flats": 500.0}
# annual capacity payment for 2027, dollars (each offer quotes in its own unit, docs.py)
PRICE = {"Ketchum Ridge": ("USD per kW-month", 6.45), "Red Willow import": ("USD per MW-day", 327.0),
         "Sandhill Draw": ("USD per kW-month", 5.30), "Coulee Flats": ("USD per kW-year", 51.60)}
CT_RATED_EFORD = 0.045    # the manufacturer's figure in the Ketchum Ridge offer


def annual_payment(o):
    unit, v = PRICE[o]
    mw = OFFER_MW[o]
    if unit == "USD per kW-month":
        return v * 12 * mw * 1000
    if unit == "USD per MW-day":
        return v * 365 * mw
    return v * mw * 1000


# ---------------------------------------------------------------------------------------------- members (asks)
MEMBERS = ["Bluestem Valley Electric", "Copper Ridge REA", "Lone Elm Cooperative", "Marais Electric",
           "Old Mill Power Association", "Sweetgrass Rural Electric", "Tamarack Electric Cooperative",
           "Wapsi Prairie Electric"]
MEMBER_SHARE = [0.17, 0.09, 0.14, 0.11, 0.08, 0.16, 0.13, 0.12]
DP_PER_MEMBER = [6, 4, 5, 5, 4, 6, 5, 5]
METER_YEAR = 2025
