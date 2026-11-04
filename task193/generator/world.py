"""task193 architecture 3: the fixed world of the closed Marten Creek Landfill's groundwater detection monitoring.

Every constant the simulation, the pack, the golden and the checks share lives here, so a change is made once.
The site grid is in feet from the south-west corner of the property; groundwater flows west to east, from the
background wells across the waste to the compliance wells, except at the western boundary in the seasons when
the gradient there reverses."""
import datetime as dt

SEED = 193301
DISTRICT = "Kettle Prairie Solid Waste District"
SITE = "Marten Creek Landfill"
CONSULTANT = "Fieldstone Hydrogeology"
LAB_A = "Tamarack Analytical Services"
LAB_B = "Ridgeline Environmental Laboratories"
PEOPLE = {"manager": "Kathryn Bonilla", "hydrogeologist": "Wendy Cantu"}
EXPORT_DATE = dt.date(2026, 11, 3)

# ---------------------------------------------------------------- monitoring points
# point: (role, easting_ft, northing_ft, ground_elev_ft_ngvd29, stick_up_ft, screen_top_bgs, screen_bot_bgs, dia_in,
#         installed)
POINTS = {
    "MW-1": ("background", 250, 800, 836.42, 2.71, 38.0, 48.0, 2, "2014-06-11"),
    "MW-2": ("background", 330, 1400, 835.88, 2.94, 37.5, 47.5, 2, "2014-06-12"),
    "MW-3": ("background", 300, 150, 837.10, 2.58, 39.0, 49.0, 2, "2014-06-12"),
    "MW-4": ("compliance", 1720, 1350, 831.64, 2.83, 33.0, 43.0, 2, "2014-06-16"),
    "MW-5": ("compliance", 1760, 1050, 830.97, 2.66, 32.0, 42.0, 2, "2014-06-16"),
    "MW-5R": ("compliance", 1765, 1030, 831.05, 2.90, 32.5, 42.5, 2, "2022-05-24"),
    "MW-6": ("compliance", 1780, 780, 830.55, 2.77, 31.5, 41.5, 2, "2014-06-17"),
    "MW-7": ("compliance", 1760, 520, 830.81, 2.62, 32.0, 42.0, 2, "2014-06-17"),
    "MW-8": ("compliance", 1700, 250, 831.37, 3.05, 32.5, 42.5, 2, "2014-06-18"),
    "MW-9": ("compliance", 1450, 120, 832.48, 2.69, 34.0, 44.0, 2, "2017-08-29"),
    "MW-10": ("compliance", 1100, 1480, 833.96, 2.88, 35.5, 45.5, 2, "2017-08-29"),
    "MW-11": ("compliance", 900, 100, 834.73, 2.74, 36.0, 46.0, 2, "2017-08-30"),
    "PZ-1": ("piezometer", 450, 800, 836.10, 2.52, 36.0, 41.0, 1, "2014-06-13"),
    "PZ-2": ("piezometer", 520, 1330, 835.47, 2.61, 36.0, 41.0, 1, "2014-06-13"),
    "PZ-3": ("piezometer", 500, 260, 836.79, 2.47, 37.0, 42.0, 1, "2014-06-13"),
    "PZ-4": ("piezometer", 1620, 800, 831.20, 2.55, 31.0, 36.0, 1, "2014-06-16"),
}
BACKGROUND = ["MW-1", "MW-2", "MW-3"]
COMPLIANCE = ["MW-4", "MW-5R", "MW-6", "MW-7", "MW-8", "MW-9", "MW-10", "MW-11"]
# the boundary piezometer each background well's gradient is read against (the nearest point on the waste edge)
BOUNDARY = {"MW-1": "PZ-1", "MW-2": "PZ-2", "MW-3": "PZ-3"}
MW5_ABANDONED = dt.date(2022, 5, 10)
DATUM_SHIFT = -0.18          # NAVD 88 minus NGVD 29 over the site (feet), applied at the 2022 resurvey
MW8_TRIM = 0.42              # riser trimmed at MW-8 after frost heave, May 2024 (feet)

# ---------------------------------------------------------------- events
def _nth_weekday(year, month, n, weekday=1):
    d = dt.date(year, month, 1)
    while d.weekday() != weekday:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


EVENTS = []
for _y in range(2018, 2027):
    for _m, _n in ((4, 2), (10, 1)):
        _d0 = _nth_weekday(_y, _m, _n)
        EVENTS.append({"label": "%d-%s" % (_y, "APR" if _m == 4 else "OCT"), "year": _y, "month": _m,
                       "days": [_d0, _d0 + dt.timedelta(days=1), _d0 + dt.timedelta(days=2)]})
EVAL = len(EVENTS) - 1                                  # the October 2026 event, the one evaluated
BG_EVENTS = list(range(0, EVAL))                         # April 2018 to April 2026, the plan's background window
LAB_SWITCH = 7                                           # events 0..6 Tamarack (to April 2021), 7.. Ridgeline

# the western boundary's state each event, set by the village well field's pumping that season (not by rain):
# q is the well field's draw in drawdown units; reversal at MW-1 where q > about 0.5, at MW-2 where q > 1.33
PUMPING = {
    "2018-APR": 0.10, "2018-OCT": 2.05, "2019-APR": 0.95, "2019-OCT": 0.32, "2020-APR": 0.05, "2020-OCT": 0.91,
    "2021-APR": 2.21, "2021-OCT": 0.97, "2022-APR": 0.12, "2022-OCT": 2.34, "2023-APR": 2.02, "2023-OCT": 1.96,
    "2024-APR": 0.08, "2024-OCT": 0.36, "2025-APR": 0.88, "2025-OCT": 2.12, "2026-APR": 0.14, "2026-OCT": 0.18,
}
# dry seasons (low regional water table): two of them carry no reversal and three reversals fall in wet seasons
DRY = {"2018-OCT", "2019-OCT", "2020-OCT", "2022-OCT", "2024-OCT", "2025-OCT"}
# head drop per unit of well-field draw at each point (feet); the west of the site sits nearest the well field
DRAW_K = {"MW-1": 0.75, "PZ-1": 0.05, "MW-2": 0.33, "PZ-2": 0.03, "MW-3": 0.14, "PZ-3": 0.02,
          "MW-4": 0.00, "MW-5": 0.00, "MW-5R": 0.00, "MW-6": 0.00, "MW-7": 0.00, "MW-8": 0.00, "MW-9": 0.00,
          "MW-10": 0.00, "MW-11": 0.00, "PZ-4": 0.00}
GRADIENT = 0.0021            # natural head fall per foot eastward
HEAD_WEST = 815.60           # head at easting 0 in an average season (feet NGVD 29)

# ---------------------------------------------------------------- chemistry
INDICATORS = ["chloride", "sodium", "boron"]
UNITS = {"chloride": "mg/L", "sodium": "mg/L", "boron": "ug/L"}
LEACHATE = {"chloride": 1100.0, "sodium": 760.0, "boron": 2300.0}
# natural medians at each well (chloride and sodium mg/L, boron ug/L)
NATURAL = {
    "MW-1": (16.6, 9.9, 33.5), "MW-2": (27.4, 16.1, 48.6), "MW-3": (21.9, 12.7, 41.1),
    "MW-4": (19.4, 11.6, 35.8), "MW-5": (18.1, 10.8, 34.1), "MW-5R": (18.1, 10.8, 34.1),
    "MW-6": (21.2, 12.5, 37.9), "MW-7": (23.3, 13.4, 30.6), "MW-8": (20.3, 11.9, 36.7),
    "MW-9": (17.2, 10.1, 37.4), "MW-10": (28.6, 18.1, 39.2), "MW-11": (20.6, 11.7, 51.0),
}
LOG_SD = {"chloride": 0.125, "sodium": 0.125, "boron": 0.135}
EVENT_SD = 0.025
DRY_LIFT = 0.05
# leachate fraction drawn into a background well in a reversed season
F_MW1 = {"moderate": 0.0090, "strong": 0.0140}
F_MW2 = 0.0160
F_SD = 0.10
# the release at the compliance wells: MW-6 newly reached in 2026, MW-7 and MW-9 long-standing
PLUME_MW6 = {"2026-APR": 0.0085}                 # October 2026 placed (place())
PLUME_STEADY = {"MW-7": 0.0105, "MW-9": 0.0072}  # history level; October 2026 placed (place())
# the October 2026 deciding results, placed as ratios to the golden limit (the generator asserts each margin)
PLACE = {
    ("MW-7", "chloride"): 1.085,
    ("MW-9", "boron"): 1.090,
    ("MW-6", "chloride"): 1.25,
}
RL = {"chloride": 1.0, "sodium": 0.5, "boron": 10.0}

# ---------------------------------------------------------------- the plan's filed method
ALPHA = 0.01                 # one-sided, per comparison: the 99th percentile of Student's t
MISSED = {("2019-APR", "MW-3"): "no sample, access road flooded"}
BORON_NOT_RUN = {("2023-APR", "MW-3")}   # boron container broken in transit, not analysed

# ---------------------------------------------------------------- field records (asks)
RENTAL_UNCOMP = "R-4471"     # rental meter recording uncompensated conductivity in the specific conductance field
RENTAL_OK = "R-4468"
OWN_METER = "21C0847"
TEMP_COEF = 0.0191
L_PER_GAL = 3.785411784
SAMPLING_ORDER = [["MW-1", "MW-2", "MW-3", "MW-4"], ["MW-5R", "MW-8", "MW-11", "MW-10"], ["MW-9", "MW-7", "MW-6"]]
OCT_METERS = {0: RENTAL_UNCOMP, 1: RENTAL_OK, 2: RENTAL_UNCOMP}
METER_UNPAIRED = ("MW-7", "MW-6")
