"""The fixed world of task182: Kelvale Mine and its groundwater monitoring network. Everything here is a
parameter the fiction chose (places, bores, owners, measuring points, loggers, dates, people) or a parameter
of the simulation that is never shipped (each bore's response to the climate and to the mine's take)."""
import datetime as dt
import zlib
from zoneinfo import ZoneInfo

import numpy as np

AEST = ZoneInfo("Australia/Brisbane")          # Queensland: UTC+10, no daylight saving
UTC = dt.timezone.utc
SEED = 18226

COMPANY = "Tarrabool Resources"
MINE = "Kelvale Mine"
CREEK = "Mundoora Creek"
PEOPLE = {"hydro": "Rebecca Quinn", "gm": "Stephen Anderson", "env": "Erika Martin", "tech": "Noah Carrillo",
          "walker": "Ernest Walker", "lewis": "Clarence Lewis"}

SPINUP = dt.date(1965, 1, 1)              # the simulation runs from here; the shipped climate starts in 1990
CLIMATE_START = dt.date(1990, 1, 1)
LAST_DAY = dt.date(2026, 9, 30)           # water levels to the end of September 2026
TAKE_START = dt.date(2022, 7, 4)          # pit dewatering began
BASELINE_MONTHS = (dt.date(2022, 4, 1), dt.date(2022, 6, 30))
EIS_ROUNDS = [(2012, 3), (2012, 6), (2012, 9), (2012, 12), (2013, 3), (2013, 6), (2013, 9), (2013, 12), (2014, 3),
              (2014, 6)]
MONTHLY_FROM = dt.date(2014, 7, 1)
LOGGERS_FROM = dt.date(2015, 5, 12)
FORTNIGHTLY_FROM = dt.date(2026, 8, 10)   # after the first complaint, landholder bores dipped every fortnight
DOWNLOAD_FINAL = (dt.date(2026, 10, 1), dt.date(2026, 10, 6))
EXTRACT_DAY = dt.date(2026, 10, 9)        # Friday: the network extract went to the hydrogeologist
REQUEST_DAY = dt.date(2026, 10, 13)
EXEC_DAY = dt.date(2026, 10, 26)
MG02_EFFECTIVE = dt.date(2026, 3, 1)
FT = 0.3048
KPA_PER_M = 9.80665

# Rainfall factor for each water year (October to September) against the long-run mean; the years before
# 1990 are drawn in the simulation. Wet 2010 to 2011, dry 2013 to 2015, average 2016 to 2017, dry 2018 to
# 2019, wet 2020 and 2021 with an average 2021-22 season, failed seasons from 2022-23 and a dry 2026.
RAIN_YEAR = {1990: 1.22, 1991: 1.31, 1992: 0.82, 1993: 0.74, 1994: 0.79, 1995: 0.88, 1996: 1.08, 1997: 1.1,
             1998: 1.25, 1999: 1.06, 2000: 1.15, 2001: 0.97, 2002: 0.78, 2003: 0.75, 2004: 0.96, 2005: 0.88,
             2006: 0.84, 2007: 0.9, 2008: 1.12, 2009: 0.9, 2010: 1.1, 2011: 1.2, 2012: 0.95, 2013: 0.85,
             2014: 0.82, 2015: 0.86, 2016: 1.02, 2017: 1.1, 2018: 0.86, 2019: 0.84, 2020: 1.45, 2021: 1.65,
             2022: 0.95, 2023: 0.58, 2024: 0.56, 2025: 0.55, 2026: 0.6}
RAIN_MONTH = {1: 105, 2: 98, 3: 68, 4: 28, 5: 27, 6: 24, 7: 17, 8: 13, 9: 12, 10: 30, 11: 62, 12: 96}
WET_DAYS = {1: 9, 2: 9, 3: 7, 4: 4, 5: 3.5, 6: 3.5, 7: 2.5, 8: 2, 9: 2, 10: 4, 11: 6, 12: 8}
APET_MONTH = {1: 200, 2: 170, 3: 168, 4: 133, 5: 100, 6: 80, 7: 87, 8: 115, 9: 150, 10: 186, 11: 202, 12: 212}

PIT = (641850.0, 7604320.0)               # MGA zone 55 (GDA2020), centre of the pit

UNITS = {"alluvium": ("Mundoora Creek alluvium (Quaternary)", "unconsolidated"),
         "basalt": ("Tertiary basalt", "consolidated"),
         "coal": ("Permian coal measures", "consolidated")}


def rng(name):
    """One seeded stream per component, so a change in one part of the world does not re-roll another."""
    return np.random.default_rng([SEED, zlib.crc32(name.encode())])


def d(s):
    return dt.date.fromisoformat(s)


# ---------------------------------------------------------------------------------------------------------
# Bores. label: the build's own name, never shipped. code: the company's monitoring code. rn: the state
# registered number. kind: landholder, reference or mine. Response parameters (never shipped):
#   n, mean_d   gamma response to rainfall less f times areal potential evaporation (mean response time, days)
#   f           evaporation factor
#   clim        the decline the climate alone makes from the bore's baseline date to September 2026, m
#   dd          the mine's drawdown at the September 2026 assessment level, m
#   r_km        distance from the pit; lag_d, leak: the Hantush-type response to the take (time scale, leakage)
#   sigma, phi  AR(1) noise (marginal sd, m; daily autocorrelation)
# ---------------------------------------------------------------------------------------------------------

BORES = [
    # coal measures near the pit (the answer's four) and one far out
    dict(label="CM1", code="KV-LB04", rn="13040719", kind="landholder", unit="coal", prop="Yarrowmere",
         owner="Yarrowmere Pastoral Co Pty Ltd", name="house bore", pump="electric submersible", logged=True,
         xy=(638710, 7602980), gl=241.62, depth=86.0, screen=(62.0, 80.0), base=d("2022-04-06"),
         n=16, mean_d=6.5 * 365.25, f=0.33, clim=-6.3, dd=8.73, lag_d=55, leak=0.55, sigma=0.05, phi=0.995),
    dict(label="CM2", code="KV-LB07", rn="13040788", kind="landholder", unit="coal", prop="Tondara",
         owner="Tondara Grazing Pty Ltd", name="Tondara bore", pump="solar submersible", logged=False,
         xy=(637440, 7606790), gl=236.10, depth=92.5, screen=(70.0, 88.0), base=d("2022-04-13"),
         n=16, mean_d=6.2 * 365.25, f=0.33, clim=-5.9, dd=8.33, lag_d=80, leak=0.6, sigma=0.05, phi=0.995),
    dict(label="CM3", code="KV-LB05", rn="13040733", kind="landholder", unit="coal", prop="Yarrowmere",
         owner="Yarrowmere Pastoral Co Pty Ltd", name="Ten Mile bore", pump="windmill", logged=True,
         xy=(639250, 7600710), gl=244.85, depth=78.0, screen=(55.0, 74.0), base=d("2022-04-07"),
         n=16, mean_d=6.8 * 365.25, f=0.33, clim=-6.8, dd=9.37, lag_d=60, leak=0.5, sigma=0.05, phi=0.995),
    dict(label="CM4", code="KV-LB10", rn="13040812", kind="landholder", unit="coal", prop="Bluebush Downs",
         owner="Bluebush Downs Pty Ltd", name="dam bore", pump="electric submersible", logged=False,
         xy=(636520, 7600180), gl=247.30, depth=95.0, screen=(73.0, 91.0), base=d("2022-04-20"),
         n=16, mean_d=6.4 * 365.25, f=0.33, clim=-5.9, dd=8.11, lag_d=110, leak=0.65, sigma=0.05, phi=0.995),
    dict(label="CM5", code="KV-LB16", rn="13041207", kind="landholder", unit="coal", prop="Kurrajong Park",
         owner="Kurrajong Park Grazing Co", name="Kurrajong bore", pump="electric submersible", logged=False,
         xy=(631260, 7597020), gl=252.40, depth=101.0, screen=(80.0, 97.0), base=d("2022-05-11"),
         n=16, mean_d=6.6 * 365.25, f=0.33, clim=-4.0, dd=2.28, lag_d=420, leak=1.2, sigma=0.05, phi=0.995),
    # the alluvium: A1 sits above the coal-measure subcrop at the pit's eastern end
    dict(label="A1", code="KV-LB12", rn="13030561", kind="landholder", unit="alluvium", prop="Cypress Ridge",
         owner="Cypress Ridge Pastoral Trust", name="creek bore", pump="windmill", logged=True,
         xy=(643920, 7604980), gl=226.18, depth=21.0, screen=(14.0, 20.0), base=d("2022-06-08"),
         n=2.0, mean_d=190, f=0.36, clim=4.4, dd=4.5, lag_d=160, leak=0.9, sigma=0.09, phi=0.985),
    dict(label="A2", code="KV-LB01", rn="13030502", kind="landholder", unit="alluvium", prop="Saltbush Flat",
         owner=PEOPLE["walker"], name="house bore", pump="electric submersible", logged=False,
         xy=(646210, 7609140), gl=221.54, depth=18.5, screen=(12.5, 17.5), base=d("2022-06-14"),
         n=1.5, mean_d=200, f=0.36, clim=4.2, dd=0.43, lag_d=300, leak=1.6, sigma=0.09, phi=0.985),
    dict(label="A3", code="KV-LB02", rn="13030518", kind="landholder", unit="alluvium", prop="Brolga Plains",
         owner="Brolga Plains Cattle Co", name="yards bore", pump="windmill", logged=True,
         xy=(648330, 7607260), gl=219.07, depth=19.5, screen=(13.0, 18.5), base=d("2022-06-15"),
         n=2.0, mean_d=180, f=0.36, clim=4.5, dd=0.82, lag_d=300, leak=1.6, sigma=0.09, phi=0.985),
    dict(label="A4", code="KV-LB03", rn="13030524", kind="landholder", unit="alluvium", prop="Wilga Vale",
         owner="Wilga Vale Grazing Trust", name="top bore", pump="solar submersible", logged=False,
         xy=(650740, 7605810), gl=216.90, depth=19.0, screen=(13.0, 18.0), base=d("2022-06-16"),
         n=2.0, mean_d=200, f=0.36, clim=3.9, dd=0.76, lag_d=320, leak=1.7, sigma=0.09, phi=0.985),
    dict(label="A5", code="KV-LB06", rn="13030547", kind="landholder", unit="alluvium", prop="Ghost Gum",
         owner=PEOPLE["lewis"], name="garden bore", pump="electric submersible", logged=False,
         xy=(645080, 7611520), gl=223.66, depth=19.0, screen=(12.5, 18.0), base=d("2022-06-21"),
         n=1.5, mean_d=190, f=0.36, clim=4.6, dd=0.21, lag_d=300, leak=1.6, sigma=0.09, phi=0.985),
    dict(label="A6", code="KV-LB08", rn="13030583", kind="landholder", unit="alluvium", prop="Lancewood Flat",
         owner="Lancewood Flat Pty Ltd", name="windmill bore", pump="solar submersible", logged=False,
         xy=(652960, 7603440), gl=214.28, depth=20.0, screen=(14.0, 19.0), base=d("2022-06-22"),
         n=2.0, mean_d=200, f=0.36, clim=4.1, dd=0.49, lag_d=340, leak=1.8, sigma=0.09, phi=0.985),
    dict(label="A7", code="KV-LB09", rn="13030596", kind="landholder", unit="alluvium", prop="Bellbird Downs",
         owner="Bellbird Downs Pastoral Co", name="No. 2 bore", pump="electric submersible", logged=False,
         xy=(655410, 7601870), gl=211.75, depth=18.0, screen=(12.0, 17.0), base=d("2022-06-23"),
         n=1.5, mean_d=200, f=0.36, clim=4.3, dd=0.47, lag_d=360, leak=1.9, sigma=0.09, phi=0.985),
    dict(label="A8", code="KV-LB13", rn="13030612", kind="landholder", unit="alluvium", prop="Coolibah Springs",
         owner="Coolibah Springs Pastoral Co", name="waterhole bore", pump="electric submersible", logged=False,
         xy=(659870, 7599620), gl=207.42, depth=12.0, screen=(6.0, 11.0), base=d("2022-06-28"),
         n=1.5, mean_d=150, f=0.36, clim=0.9, dd=0.15, lag_d=380, leak=2.0, sigma=0.05, phi=0.98),
    dict(label="A9", code="KV-LB14", rn="13030628", kind="landholder", unit="alluvium", prop="Coolibah Springs",
         owner="Coolibah Springs Pastoral Co", name="lagoon bore", pump="windmill", logged=False,
         xy=(661150, 7598730), gl=206.85, depth=11.5, screen=(5.5, 10.5), base=d("2022-06-28"),
         n=1.5, mean_d=140, f=0.36, clim=0.8, dd=0.12, lag_d=400, leak=2.0, sigma=0.05, phi=0.98),
    # the basalt on the ridges; B4 is the ridge bore
    dict(label="B1", code="KV-LB11", rn="13050311", kind="landholder", unit="basalt", prop="Gidgee Creek",
         owner="Gidgee Creek Holdings Pty Ltd", name="north bore", pump="electric submersible", logged=False,
         xy=(644330, 7614270), gl=262.40, depth=48.0, screen=(30.0, 46.0), base=d("2022-05-04"),
         n=1.5, mean_d=450, f=0.34, clim=1.6, dd=1.16, lag_d=200, leak=1.1, sigma=0.08, phi=0.99),
    dict(label="B2", code="KV-LB15", rn="13050327", kind="landholder", unit="basalt", prop="Gidgee Creek",
         owner="Gidgee Creek Holdings Pty Ltd", name="shed bore", pump="windmill", logged=True,
         xy=(640120, 7613080), gl=268.95, depth=52.0, screen=(34.0, 50.0), base=d("2022-05-05"),
         n=2.0, mean_d=560, f=0.34, clim=1.4, dd=1.65, lag_d=180, leak=1.0, sigma=0.08, phi=0.99),
    dict(label="B3", code="KV-LB17", rn="13050354", kind="landholder", unit="basalt", prop="Kurrajong Park",
         owner="Kurrajong Park Grazing Co", name="ridge paddock bore", pump="solar submersible", logged=False,
         xy=(633780, 7608550), gl=274.10, depth=55.0, screen=(38.0, 53.0), base=d("2022-05-12"),
         n=1.5, mean_d=650, f=0.34, clim=1.9, dd=1.0, lag_d=260, leak=1.3, sigma=0.08, phi=0.99),
    dict(label="B4", code="KV-LB18", rn="13050362", kind="landholder", unit="basalt", prop="Bottletree",
         owner="Bottletree Holdings Pty Ltd", name="ridge bore", pump="windmill", logged=True,
         xy=(648960, 7615640), gl=271.35, depth=44.0, screen=(26.0, 42.0), base=d("2022-05-18"),
         n=1.0, mean_d=300, f=0.34, clim=7.2, dd=1.48, lag_d=220, leak=1.2, sigma=0.08, phi=0.99),
    # state reference bores outside the predicted drawdown (two in the alluvium, one in the basalt)
    dict(label="RA1", code="KV-RF01", rn="13030150", kind="reference", unit="alluvium", prop="road reserve",
         owner="State of Queensland", name="", pump="none", logged=True,
         xy=(664210, 7619380), gl=203.95, depth=19.0, screen=(12.0, 18.0), base=None,
         n=2.0, mean_d=190, f=0.36, clim=4.9, dd=0.0, lag_d=0, leak=0, sigma=0.08, phi=0.985),
    dict(label="RA2", code="KV-RF02", rn="13030177", kind="reference", unit="alluvium", prop="stock route",
         owner="State of Queensland", name="", pump="none", logged=False,
         xy=(668870, 7588450), gl=199.60, depth=17.5, screen=(11.0, 17.0), base=None,
         n=1.5, mean_d=200, f=0.36, clim=5.0, dd=0.0, lag_d=0, leak=0, sigma=0.08, phi=0.985),
    dict(label="RB1", code="KV-RF03", rn="13050102", kind="reference", unit="basalt", prop="road reserve",
         owner="State of Queensland", name="", pump="none", logged=True,
         xy=(622540, 7622860), gl=281.70, depth=50.0, screen=(32.0, 48.0), base=None,
         n=1.0, mean_d=420, f=0.34, clim=5.2, dd=0.0, lag_d=0, leak=0, sigma=0.08, phi=0.99),
    # the mine's own monitoring bores near the pit
    dict(label="MA1", code="KV-MB01", rn="13030701", kind="mine", unit="alluvium", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=True,
         xy=(643020, 7605510), gl=225.40, depth=26.0, screen=(13.0, 25.0), base=None,
         n=2.0, mean_d=190, f=0.36, clim=4.4, dd=6.2, lag_d=90, leak=0.6, sigma=0.09, phi=0.985),
    dict(label="MA2", code="KV-MB02", rn="13030702", kind="mine", unit="alluvium", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=False,
         xy=(641110, 7606180), gl=228.85, depth=19.5, screen=(12.5, 18.5), base=None,
         n=1.5, mean_d=200, f=0.36, clim=4.2, dd=4.1, lag_d=110, leak=0.7, sigma=0.09, phi=0.985),
    dict(label="MC1", code="KV-MB03", rn="13040901", kind="mine", unit="coal", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=True,
         xy=(641230, 7603650), gl=238.70, depth=95.0, screen=(70.0, 90.0), base=None,
         n=16, mean_d=6.5 * 365.25, f=0.33, clim=-6.0, dd=42.0, lag_d=12, leak=0.2, sigma=0.06, phi=0.995),
    dict(label="MC2", code="KV-MB04", rn="13040902", kind="mine", unit="coal", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=False,
         xy=(640480, 7604820), gl=236.95, depth=98.0, screen=(72.0, 93.0), base=None,
         n=16, mean_d=6.5 * 365.25, f=0.33, clim=-5.9, dd=35.5, lag_d=18, leak=0.25, sigma=0.06, phi=0.995),
    dict(label="MC3", code="KV-MB05", rn="13040903", kind="mine", unit="coal", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=False,
         xy=(642640, 7602790), gl=240.15, depth=96.0, screen=(71.0, 91.0), base=None,
         n=16, mean_d=6.5 * 365.25, f=0.33, clim=-6.1, dd=31.0, lag_d=22, leak=0.3, sigma=0.06, phi=0.995),
    dict(label="MC4", code="KV-MB06", rn="13040904", kind="mine", unit="coal", prop="mining lease",
         owner=COMPANY, name="", pump="none", logged=False,
         xy=(639900, 7602110), gl=242.80, depth=97.0, screen=(73.0, 92.0), base=None,
         n=16, mean_d=6.5 * 365.25, f=0.33, clim=-5.8, dd=27.5, lag_d=30, leak=0.35, sigma=0.06, phi=0.995),
]
BY_LABEL = {b["label"]: b for b in BORES}
LANDHOLDER = [b["label"] for b in BORES if b["kind"] == "landholder"]
REFERENCE = [b["label"] for b in BORES if b["kind"] == "reference"]
MINE_BORES = [b["label"] for b in BORES if b["kind"] == "mine"]
LOGGED = [b["label"] for b in BORES if b["logged"]]

# Depth to water below ground at each bore's baseline (or on 1 May 2022 for the network's other bores), m;
# the simulation sets each bore's constant so the level sits here.
SWL_BGL = {"CM1": 31.4, "CM2": 38.2, "CM3": 27.9, "CM4": 41.6, "CM5": 44.3, "A1": 7.9, "A2": 7.40, "A3": 8.60,
           "A4": 7.4, "A5": 9.20, "A6": 8.2, "A7": 7.90, "A8": 4.10, "A9": 4.10, "B1": 21.7, "B2": 24.6, "B3": 28.3,
           "B4": 16.9, "RA1": 7.2, "RA2": 6.6, "RB1": 23.8, "MA1": 8.4, "MA2": 7.7, "MC1": 29.6, "MC2": 30.8,
           "MC3": 28.7, "MC4": 32.5}

# Measuring points: (in force from, elevation m AHD, description). The headworks at two bores were rebuilt
# after the baseline assessments and the new measuring point surveyed.
MP_STICKUP = {"CM1": 0.46, "CM2": 0.52, "CM3": 0.38, "CM4": 0.61, "CM5": 0.44, "A1": 0.55, "A2": 0.41, "A3": 0.63,
              "A4": 0.37, "A5": 0.48, "A6": 0.42, "A7": 0.57, "A8": 0.66, "A9": 0.51, "B1": 0.45, "B2": 0.39,
              "B3": 0.53, "B4": 0.47, "RA1": 0.72, "RA2": 0.68, "RB1": 0.75, "MA1": 0.81, "MA2": 0.78, "MC1": 0.84,
              "MC2": 0.79, "MC3": 0.82, "MC4": 0.86}
MP_RESURVEY = {"CM2": (d("2023-11-14"), 0.392, "new headworks and pump column after the pump was pulled; top of new casing"),
               "A6": (d("2025-08-27"), 0.527, "casing extended above the 2021 flood mark; top of extension")}

# A datum adjustment per bore (m), a few millimetres at most, set so that each graded figure sits in the middle
# of its rounding bin rather than near an edge.
SHIFT = {"CM4": 0.0036, "A3": -0.0001, "A5": 0.0015, "B1": 0.0029, "B2": 0.0025, "B4": 0.0002}

# Loggers: (serial, installed local, removed local or None, sensor depth below the measuring point, m)
LOGGER_INSTALLS = {
    "CM1": [("2041873", "2015-05-13 10:20", None, 41.50)],
    "CM3": [("2041881", "2015-05-13 13:05", "2019-02-26 11:40", 38.00), ("2190446", "2019-04-02 09:55", None, 37.75)],
    "A1": [("2041890", "2015-05-14 08:45", None, 20.20)],
    "A3": [("2041902", "2015-05-14 11:30", None, 18.40)],
    "B2": [("2041917", "2015-05-15 09:10", None, 35.20)],
    "B4": [("2041925", "2015-05-15 12:25", "2021-09-08 10:15", 30.40), ("2213378", "2021-09-08 10:40", None, 30.65)],
    "RA1": [("2041933", "2015-05-19 10:00", None, 17.60)],
    "RB1": [("2041948", "2015-05-19 14:35", None, 33.40)],
    "MA1": [("2041956", "2015-05-12 15:20", None, 24.80)],
    "MC1": [("2041964", "2015-05-12 16:10", None, 78.00)],
}
BARO_SERIAL = "2041972"
BARO_FROM = "2015-05-12 09:00"
LOGGER_GAPS = {"B2": [("2020-01-17 06:00", "2020-02-03 11:00")]}    # UTC; flat battery
BARO_GAPS = [("2018-03-21 02:00", "2018-03-21 10:00")]               # UTC

# The mine's take: pit sumps from 4 July 2022, advance dewatering bores from March 2023 (ML/day)
SOURCES = [("PS1", "Pit sump 1", "2022-07-04"), ("PS2", "Pit sump 2", "2023-01-16"),
           ("AD01", "Advance dewatering bore AD01", "2023-03-06"), ("AD02", "Advance dewatering bore AD02", "2023-03-20"),
           ("AD03", "Advance dewatering bore AD03", "2023-08-14"), ("AD04", "Advance dewatering bore AD04", "2024-02-12")]

# Complaints (MG-02 7.1): the owners of these bores said they were sucking air
COMPLAINTS = {"A2": d("2026-08-03"), "A3": d("2026-08-19"), "A5": d("2026-09-02"), "B4": d("2026-09-15")}
