"""The world of task180: five deep geothermal district-heating plants in the southern Molasse basin, the survey's
networks around them, their seismicity and the rules the mining authority files. Every figure the pack carries comes
from the simulation in sim.py, seeded from here; nothing in this file is a graded figure."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 180
LOCAL = ZoneInfo("Europe/Berlin")
UTC = dt.timezone.utc

SURVEY = "Landesdienst für Geologie"
SURVEY_SHORT = "LDG"
AUTHORITY = "Bergbehörde Süd"
NET = "LG"                                   # the survey's network code

RECORD_START = dt.datetime(2023, 1, 1, tzinfo=LOCAL)
RECORD_END = dt.datetime(2026, 10, 1, tzinfo=LOCAL)      # exclusive
YEAR_START_2026 = dt.datetime(2026, 1, 1, tzinfo=LOCAL)
EXTRACT_DATE = dt.date(2026, 10, 12)

AMBER = 120                                   # more than this many in a calendar quarter
COUNT_ML = 1.0                                # the scheme counts earthquakes of ML 1.0 or more
RADIUS_KM = 5.0
DESIGN_ML_2027 = 0.6                          # the 2026 ordinance's design completeness for the borehole networks

# plants: code, municipality, operator, wellhead (lat, lon), injection open hole (top lat, lon, depth m; bottom lat,
# lon, depth m), seismic response (earthquakes of ML 1.0 or more per 100,000 m3 injected, metered), b-value
PLANTS = ["MOS", "PFB", "LZR", "WDR", "OTM"]
NAME = {"MOS": "Moorstetten", "PFB": "Pfeilbrunn", "LZR": "Lanzenried", "WDR": "Wendelsried", "OTM": "Ottenmoos"}
OPERATOR = {"MOS": "Geowärme Moorstetten GmbH", "PFB": "Stadtwerke Pfeilbrunn",
            "LZR": "Erdwärme Lanzenried GmbH & Co. KG", "WDR": "Wendelsrieder Wärme eG",
            "OTM": "Ottenmoos Thermal GmbH"}
WELLHEAD = {"MOS": (47.9214, 11.4027), "PFB": (48.0818, 11.7193), "LZR": (47.9796, 11.6061),
            "WDR": (47.8607, 11.6236), "OTM": (48.0213, 11.9187)}
# open-hole section of each injection well (deviated): (lat, lon, depth_m) at top and bottom
OPEN_HOLE = {
    "MOS": [((47.9151, 11.4128, 3020), (47.9098, 11.4239, 3610)),       # MST-GT2
            ((47.9263, 11.3889, 3080), (47.9301, 11.3772, 3655))],      # MST-GT4 (second injector)
    "PFB": [((48.0809, 11.7322, 2890), (48.0796, 11.7461, 3470))],
    "LZR": [((47.9714, 11.6130, 3150), (47.9638, 11.6198, 3720))],
    "WDR": [((47.8689, 11.6301, 3310), (47.8752, 11.6377, 3880))],
    "OTM": [((48.0287, 11.9241, 2980), (48.0349, 11.9310, 3540))],
}
B_VALUE = {"MOS": 1.24, "PFB": 1.45, "LZR": 1.27, "WDR": 1.22, "OTM": 1.26}
# each reservoir's seismogenic response is set so that a first quarter at 2026's injection carries this many
# earthquakes of ML 1.0 or more (sim.py turns it into earthquakes per 100,000 m3 metered)
TARGET_Q1 = {"MOS": 80.0, "PFB": 210.0, "LZR": 78.0, "WDR": 40.0, "OTM": 48.0}
# the town's heat demand falls further in summer: its month factors are raised to this power
SEASON_SHARPNESS = {"MOS": 1.0, "PFB": 1.4, "LZR": 1.0, "WDR": 1.0, "OTM": 1.0}
# winter peak flow of each plant's injection (L/s); month factors give the heat-demand season
PEAK_FLOW = {"MOS": 105.0, "PFB": 113.0, "LZR": 101.0, "WDR": 98.0, "OTM": 106.0}
MONTH_FACTOR = {1: 1.00, 2: 0.95, 3: 0.79, 4: 0.53, 5: 0.37, 6: 0.28, 7: 0.27, 8: 0.28, 9: 0.39, 10: 0.73,
                11: 0.90, 12: 1.00}
YEAR_FACTOR = {2023: 0.97, 2024: 1.02, 2025: 0.99, 2026: 1.01}
REINJECTION_TEMP_C = {"MOS": 58.0, "PFB": 61.0, "LZR": 55.0, "WDR": 52.0, "OTM": 63.0}
# summer revision of each plant (injection stopped), by year: (month, first day, days)
REVISION = {"MOS": (8, 3, 12), "PFB": (7, 13, 14), "LZR": (8, 17, 10), "WDR": (7, 6, 12), "OTM": (8, 10, 13)}

# detection: the magnitude at which half the earthquakes are recorded, and its spread, by plant and local hour
RURAL_DETECT = {"night": (0.30, 0.12), "day": (0.42, 0.12)}
LZR_OLD_DETECT = (1.45, 0.15)                 # Lanzenried before its fourth station moved nearer the well
LZR_NEW_STATION = dt.datetime(2025, 7, 15, 11, 0, tzinfo=LOCAL)   # LZR4 off, LZR5 on
PFB_DETECT = {"quiet": (0.40, 0.12), "shoulder": (1.30, 0.18), "day": (1.95, 0.20), "day_free": (1.70, 0.20)}
QUIET_HOURS = (23.5, 5.0)                    # local, 23:30 to 05:00
SHOULDER = ((5.0, 7.0), (21.5, 23.5))

# induced sequences: a share of the earthquakes comes with a second one at the same spot seconds later
DOUBLET_SHARE = 0.03
DOUBLET_DELAY_S = (9.0, 30.0)
MIN_SEPARATION_S = 45.0                      # otherwise a plant's earthquakes are at least this far apart

# the two limestone quarries whose production blasts the networks record (nine kilometres or more from every
# open hole)
QUARRY = {"WDR": (47.8095, 11.5410), "OTM": (48.0164, 12.0511)}

# Bavarian public holidays in the record (the town's working-day noise drops on them)
HOLIDAYS = [dt.date(*d) for d in [
    (2023, 1, 1), (2023, 1, 6), (2023, 4, 7), (2023, 4, 10), (2023, 5, 1), (2023, 5, 18), (2023, 5, 29), (2023, 6, 8),
    (2023, 8, 15), (2023, 10, 3), (2023, 11, 1), (2023, 12, 25), (2023, 12, 26),
    (2024, 1, 1), (2024, 1, 6), (2024, 3, 29), (2024, 4, 1), (2024, 5, 1), (2024, 5, 9), (2024, 5, 20), (2024, 5, 30),
    (2024, 8, 15), (2024, 10, 3), (2024, 11, 1), (2024, 12, 25), (2024, 12, 26),
    (2025, 1, 1), (2025, 1, 6), (2025, 4, 18), (2025, 4, 21), (2025, 5, 1), (2025, 5, 29), (2025, 6, 9), (2025, 6, 19),
    (2025, 8, 15), (2025, 10, 3), (2025, 11, 1), (2025, 12, 25), (2025, 12, 26),
    (2026, 1, 1), (2026, 1, 6), (2026, 4, 3), (2026, 4, 6), (2026, 5, 1), (2026, 5, 14), (2026, 5, 25), (2026, 6, 4),
    (2026, 8, 15)]]


def quarter_bounds(year, q):
    a = dt.datetime(year, 3 * q - 2, 1, tzinfo=LOCAL)
    b = dt.datetime(year + (q == 4), 1 if q == 4 else 3 * q + 1, 1, tzinfo=LOCAL)
    return a, b


def record_quarters():
    out = []
    for y in (2023, 2024, 2025, 2026):
        for q in (1, 2, 3, 4):
            a, b = quarter_bounds(y, q)
            if b <= RECORD_END:
                out.append((y, q))
    return out
