"""The fiction: a university environmental radioactivity laboratory runs a regional ambient gamma dose-rate
network for a joint committee of three county councils in the north of England. Every name below is invented;
personas come from `guard.py names --geo uk --seed 211`."""
import datetime as dt

SEED = 211_2026

# organisation
LAB = "Northvale University Environmental Radioactivity Laboratory"
LAB_SHORT = "NUERL"
UNIVERSITY = "Northvale University"
NETWORK = "Moorland and Vale Gamma Dose-Rate Network"
NETWORK_SHORT = "MVGN"
COMMITTEE = "Moorland and Vale Joint Radiation Monitoring Committee"
COUNCILS = ("North Moors County Council", "Mid Vale County Council", "Saltmarsh Coast County Council")
REGULATOR = "Environment Agency"
WATER_CO = "Northvale Water"
GAUGE_OPERATOR = "Northvale Water telemetry"
LAB_GB = "Northvale University Radiochemistry Services"

PEOPLE = {
    "manager": "Cameron Brown",          # Network Manager
    "duty": "Hazel Lambert",             # Duty Radiation Scientist
    "eng_a": "Julia French",             # Field Engineer
    "eng_b": "Antony Connolly",          # Field Engineer
    "chem": "Frances Stevens",           # Radiochemistry Services, reporting analyst
    "clerk": "Katie Clarke",             # Clerk to the Joint Committee
}

# window: Q3 2026, ten-minute intervals labelled by their start, UTC; British Summer Time throughout
Q_START = dt.datetime(2026, 7, 1, 0, 0)
Q_END = dt.datetime(2026, 10, 1, 0, 0)
DAYS = 92
N10 = DAYS * 144
BST = dt.timedelta(hours=1)
EXPORT_DATE = dt.datetime(2026, 10, 9, 8, 40)     # the duty scientist's quarter-end export (local)

# physics
T_PB214_MIN = 26.8
T_BI214_MIN = 19.9
CS137_HALF_LIFE_Y = 30.05
COUNTS_PER_10MIN_AT_100 = 2000  # probe sensitivity: counts in ten minutes at 100 nSv/h

# stations: (code, name, kind, easting, northing, altitude_m, county index)
# kind: upland (granite moor), coastal, lowland (vale)
STATIONS = [
    ("MV214", "Moor Top Mast", "upland", 436120, 498240, 412, 0),
    ("MV231", "Upper Reservoir", "upland", 441870, 491530, 356, 0),
    ("MV207", "High Quarry", "upland", 449350, 502610, 389, 0),
    ("MV243", "Fell Road Cairn", "upland", 455820, 495170, 301, 0),
    ("MV226", "Summit Transmitter", "upland", 432650, 489410, 437, 0),
    ("MV318", "North Pier", "coastal", 401440, 474380, 9, 2),
    ("MV305", "Coastguard Hut", "coastal", 403980, 486920, 22, 2),
    ("MV327", "Harbour Office", "coastal", 398870, 462150, 6, 2),
    ("MV311", "Dune Car Park", "coastal", 405230, 496730, 14, 2),
    ("MV334", "Headland Lookout", "coastal", 400170, 455480, 31, 2),
    ("MV142", "University Campus", "lowland", 428450, 468930, 58, 1),
    ("MV118", "Mill Lane Depot", "lowland", 437960, 461240, 41, 1),
    ("MV157", "River Bridge", "lowland", 446310, 470850, 64, 1),
    ("MV103", "Grange Farm", "lowland", 419740, 476420, 73, 1),
    ("MV166", "Carr Lane Allotments", "lowland", 452870, 463390, 37, 1),
    ("MV129", "Old Brickworks", "lowland", 423180, 459870, 49, 1),
    ("MV171", "Village Green", "lowland", 458640, 478120, 88, 1),
    ("MV135", "Moor Road", "lowland", 431570, 481260, 112, 0),
    ("MV184", "Riverside Depot", "lowland", 441090, 455730, 33, 1),
    ("MV149", "Home Farm", "lowland", 414860, 466570, 66, 2),
    ("MV192", "Water Treatment Works", "lowland", 463470, 467940, 52, 1),
    ("MV112", "School Playing Field", "lowland", 426930, 472640, 61, 1),
    ("MV176", "Beck Side", "lowland", 449920, 457380, 29, 1),
    ("MV158", "Crossroads", "lowland", 417250, 483050, 96, 0),
]
# the stations the pipeline's weld radiography passes, in turn (generator truth only; never shipped)
RADIOGRAPHY = {"MV334": (dt.date(2026, 7, 6), dt.date(2026, 8, 13)),
               "MV129": (dt.date(2026, 8, 18), dt.date(2026, 9, 25))}
# the outstations still on the old firmware report microsieverts per hour
MICRO_UNIT_STATIONS = {"MV226", "MV305", "MV231"}
# a probe exchange: station, local date, new probe's response relative to the old until the factor is applied
PROBE_EXCHANGE = ("MV157", dt.datetime(2026, 8, 11, 10, 20), 1.042, dt.datetime(2026, 8, 19, 9, 0))
# re-ingested days in the export (identical duplicate rows): (station, date)
REINGEST = [("MV214", dt.date(2026, 7, 22)), ("MV311", dt.date(2026, 8, 3)), ("MV184", dt.date(2026, 8, 27)),
            ("MV243", dt.date(2026, 9, 14))]

# 2025 platform migration: old outstation codes
OLD_CODES = {
    "MV214": "NMR-07", "MV231": "NMR-12", "MV207": "NMR-03", "MV243": "NMR-15", "MV226": "NMR-09",
    "MV318": "SMC-04", "MV305": "SMC-02", "MV327": "SMC-06", "MV311": "SMC-03", "MV334": "SMC-08",
    "MV142": "MDV-01", "MV118": "MDV-05", "MV157": "MDV-11", "MV103": "MDV-02", "MV166": "MDV-14",
    "MV129": "MDV-07", "MV171": "MDV-16", "MV135": "NMR-18", "MV184": "MDV-09", "MV149": "SMC-11",
    "MV192": "MDV-19", "MV112": "MDV-04", "MV176": "MDV-12", "MV158": "NMR-21",
}

# rain gauges (Northvale Water telemetry): (id, name, easting, northing)
GAUGES = [
    ("NVW-RG-0412", "Low Moor STW", 438420, 462010),
    ("NVW-RG-0457", "Vale Road WTW", 445980, 471940),
    ("NVW-RG-0391", "Grange Pumping Station", 420510, 475830),
    ("NVW-RG-0528", "East Reservoir", 462240, 466010),
    ("NVW-RG-0466", "Flood Storage Basin", 424670, 457880),
    ("NVW-RG-0503", "Beck Intake", 430980, 482370),
]

# air samplers: (sampler, station, set flow m3/h, record style)
AIR = [("AS1", "MV142", 10.0, "elapsed"), ("AS2", "MV231", 8.0, "hourmeter"), ("AS3", "MV327", 10.0, "elapsed")]

# check sources (Cs-137): serial -> list of certificates (cert no, reference date, issued, reading per jig nSv/h)
SOURCES = {
    "CS-0417": [("HCX-CAL-19-0233", dt.date(2019, 3, 14), dt.date(2019, 3, 21), {"J1": 2364.0, "J2": 1641.0})],
    "CS-0583": [("HCX-CAL-20-0118", dt.date(2020, 6, 2), dt.date(2020, 6, 9), {"J1": 2187.0, "J2": 1519.0}),
                ("HCX-CAL-26-0164", dt.date(2026, 8, 20), dt.date(2026, 8, 27), {"J1": 1940.0, "J2": 1348.0})],
    "CS-0729": [("HCX-CAL-22-0071", dt.date(2022, 1, 25), dt.date(2022, 2, 1), {"J1": 2491.0, "J2": 1729.0})],
}
# field kits: engineer -> (kit, check source, jig)
KITS = {"eng_a": ("KIT-2", "CS-0583", "J1"), "eng_b": ("KIT-3", "CS-0729", "J2"), "spare": ("KIT-1", "CS-0417", "J1")}
# CS-0583 went to the metrology unit for recalibration; KIT-2 carried the spare CS-0417 from dispatch to return
CS0583_AWAY = (dt.date(2026, 8, 5), dt.date(2026, 9, 4))     # dispatched, back in the store
SPARE_IN_KIT2 = CS0583_AWAY
RMU = "Radiation Metrology Unit"
RMU_RECEIVED = dt.date(2026, 8, 6)
RPS = "Rosemary Wood"                                   # the university's radiation protection supervisor
# a batch of probe cable glands fitted in the 2025 refurbishment lets water in after heavy rain: the probe stops
# counting and the outstation sends a fault record (no dose rate) until the gland dries or is reseated
GLAND_BATCH = ["MV214", "MV207", "MV305", "MV311", "MV142", "MV118", "MV166", "MV103", "MV184", "MV149", "MV176"]

