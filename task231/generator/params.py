"""task231 architecture 2: the Sawyer Divide Highway District's road weather stations, winter 2026/27.
Every constant the world, the pack, the goldens and the checks share."""
import datetime as dt

SEED = 7
NOISE_KEY = 35         # the stations' own air (offsets, hour-to-hour noise): drawn so no share sits on a rounding edge
ORG = "Sawyer Divide Highway District"
ORG_SHORT = "SDHD"
VENDOR = "Quillan Road Weather Systems"
DOMAIN = "sdhd.mt.gov"
VENDOR_DOMAIN = "quillanrws.com"
PEOPLE = {"manager": ("Melissa Hayden", "mhayden"), "engineer": ("Lynn Dalton", "ldalton"),
          "vendor": ("Robyn Reeves", "rreeves")}

# the winter the standard reads: 1 October 2026 00:00 to 1 May 2027 00:00 Mountain time (MDT both ends)
WIN_START_UTC = dt.datetime(2026, 10, 1, 6)
WIN_END_UTC = dt.datetime(2027, 5, 1, 6)
NH = int((WIN_END_UTC - WIN_START_UTC).total_seconds() // 3600)          # 5,088 hours
DST_OFF_UTC = dt.datetime(2026, 11, 1, 8)     # 02:00 MDT becomes 01:00 MST
DST_ON_UTC = dt.datetime(2027, 3, 14, 9)      # 02:00 MST becomes 03:00 MDT
SETTING = dt.date(2027, 5, 18)

# the vendor's air-temperature tests (configuration v4.3)
SPATIAL_RADIUS_KM = 45.0
SPATIAL_LAPSE_C_PER_KM = 6.5
SPATIAL_TOL_C = 6.0
SPATIAL_MIN_NEIGHBOURS = 2
STEP_LIMIT_C = 10.0
PERSIST_HOURS = 6
RANGE_C = (-45.0, 50.0)
RETUNE_LINE_PCT = 2.0
SENSOR_ACCURACY_C = 0.3          # the standard's "within the sensor's stated accuracy"
SLA_GRACE_MIN = 20               # Schedule B: received no later than 20 minutes after the hour ended

# stations: tag, site code, RPU id, name, route, milepost, x km, y km, elevation m, group, section, travel-lane
# pavement sensor model, a second pavement sensor's lane (or "")
# groups: a basin floor (K, L, M, N, P, Q), a slope above a basin ("Kslope" ...), a windy gap (G), a pass or
# ridge (R), the open plateau (T)
STATIONS = [
    ("K1", "SD-118", "ESS4417", "Halvorsen Meadow", "MT 271", 14.6, 10.0, 20.0, 1118, "K", "Sawyer 2", "IRS-31", ""),
    ("K2", "SD-131", "ESS4492", "Teller Junction", "MT 271", 22.3, 18.5, 24.0, 1142, "K", "Sawyer 2", "IRS-31", "bridge deck"),
    ("K3", "SD-122", "ESS4459", "Bitterbrush Flat", "US 487", 61.8, 25.0, 29.5, 1106, "K", "Sawyer 2", "SCAN-16", ""),
    ("K4", "SD-147", "ESS4503", "Larkspur Grade", "US 487", 55.1, 16.0, 31.0, 1560, "Kslope", "Sawyer 2", "IRS-31", ""),
    ("L1", "SD-109", "ESS4386", "Lone Tree Siding", "MT 271", 6.9, 21.5, 10.0, 1176, "L", "Sawyer 1", "IRS-31", ""),
    ("L2", "SD-113", "ESS4398", "Wister Bridge", "MT 309", 31.4, 27.0, 18.0, 1193, "L", "Sawyer 1", "IRS-31", "bridge deck"),
    ("L3", "SD-158", "ESS4547", "Sapphire Hill", "MT 309", 39.0, 30.0, 9.0, 1655, "Lslope", "Sawyer 1", "SCAN-16", ""),
    ("M1", "SD-204", "ESS4612", "Cutler Meadow", "US 487", 88.7, 52.0, 40.0, 1418, "M", "Sawyer 3", "IRS-31", ""),
    ("M2", "SD-211", "ESS4630", "Ransom Creek", "US 487", 97.2, 61.0, 46.0, 1441, "M", "Sawyer 3", "IRS-31", "bridge deck"),
    ("M3", "SD-226", "ESS4671", "Antimony Grade", "MT 52", 18.3, 57.0, 52.0, 1878, "Mslope", "Sawyer 3", "IRS-31", ""),
    ("N1", "SD-219", "ESS4655", "Dutchman Flat", "MT 52", 4.1, 58.0, 33.0, 1462, "N", "Sawyer 3", "IRS-31", ""),
    ("N2", "SD-233", "ESS4688", "Hollis Junction", "MT 52", 11.6, 67.0, 37.0, 1449, "N", "Sawyer 3", "SCAN-16", ""),
    ("N3", "SD-240", "ESS4702", "Notch Grade", "MT 52", 25.9, 72.0, 29.0, 1902, "Nslope", "Sawyer 3", "IRS-31", ""),
    ("P1", "SD-307", "ESS4815", "Upper Antler", "US 33", 142.5, 91.0, 73.0, 1688, "P", "Sawyer 4", "IRS-31", ""),
    ("P2", "SD-312", "ESS4829", "Corrigan Lake", "US 33", 149.8, 95.0, 76.0, 1707, "P", "Sawyer 4", "IRS-31", ""),
    ("P3", "SD-318", "ESS4843", "Ptarmigan Grade", "US 33", 156.2, 99.0, 68.0, 2082, "Pslope", "Sawyer 4", "SCAN-16", ""),
    ("Q1", "SD-402", "ESS4904", "Maple Bend", "US 487", 121.4, 30.0, 62.0, 1008, "Q", "Sawyer 1", "IRS-31", ""),
    ("Q2", "SD-405", "ESS4917", "Riverside Rest Area", "US 487", 129.9, 40.0, 66.0, 992, "Q", "Sawyer 1", "IRS-31", "bridge deck"),
    ("Q3", "SD-411", "ESS4933", "Fenwick", "US 487", 138.6, 49.0, 71.0, 1031, "Q", "Sawyer 1", "IRS-31", ""),
    ("Q4", "SD-416", "ESS4946", "Garnet View", "MT 309", 52.7, 38.0, 78.0, 1424, "Qslope", "Sawyer 1", "SCAN-16", ""),
    ("G1", "SD-127", "ESS4476", "Bridger Narrows", "MT 309", 44.8, 38.0, 30.0, 1238, "G", "Sawyer 2", "IRS-31", ""),
    ("G2", "SD-251", "ESS4729", "Coyote Gap", "MT 52", 33.2, 75.0, 55.0, 1362, "G", "Sawyer 3", "IRS-31", ""),
    ("G3", "SD-138", "ESS4518", "Ashby Crossing", "MT 271", 37.5, 20.0, 52.0, 1052, "G", "Sawyer 2", "IRS-31", "bridge deck"),
    ("R1", "SD-163", "ESS4560", "Cedar Summit", "MT 309", 58.4, 42.0, 18.0, 1984, "R", "Sawyer 2", "IRS-31", ""),
    ("R2", "SD-262", "ESS4744", "Ironcap Summit", "MT 52", 41.7, 70.0, 18.0, 2164, "R", "Sawyer 3", "SCAN-16", ""),
    ("R3", "SD-277", "ESS4768", "Monument Pass", "US 33", 101.3, 82.0, 47.0, 2311, "R", "Sawyer 4", "IRS-31", ""),
    ("R4", "SD-171", "ESS4579", "Sheep Ridge", "MT 271", 45.2, 24.0, 42.0, 2048, "R", "Sawyer 2", "IRS-31", ""),
    ("R5", "SD-336", "ESS4871", "Thunder Saddle", "US 33", 171.9, 108.0, 85.0, 2422, "R", "Sawyer 4", "IRS-31", ""),
    ("R6", "SD-289", "ESS4787", "Elkhorn Divide", "MT 52", 63.5, 55.0, 82.0, 1941, "R", "Sawyer 3", "SCAN-16", ""),
    ("T1", "SD-344", "ESS4888", "Big Prairie", "US 33", 118.0, 80.0, 92.0, 1562, "T", "Sawyer 4", "IRS-31", ""),
    ("T2", "SD-351", "ESS4899", "Antelope Bench", "US 33", 126.4, 92.0, 100.0, 1611, "T", "Sawyer 4", "IRS-31", ""),
]
TAGS = [s[0] for s in STATIONS]
SITE = {s[0]: s[1] for s in STATIONS}
RPU = {s[0]: s[2] for s in STATIONS}
NAME = {s[0]: s[3] for s in STATIONS}
GROUP = {s[0]: s[9] for s in STATIONS}
ELEV = {s[0]: s[8] for s in STATIONS}
LAT0, LON0 = 46.205, -113.940
KM_LAT, KM_LON = 0.008993, 0.012965

# basin cold pools: the deficit at the floor at full strength (C), the pool's depth (m), the share of still clear
# nights it forms, whether it persists through the day in a long still spell
BASIN = {"K": (11.5, 330, 0.75, True), "L": (2.5, 110, 0.25, False), "M": (9.6, 250, 0.70, False),
         "N": (6.0, 140, 0.70, False), "P": (10.5, 190, 0.32, False), "Q": (6.5, 210, 0.80, False)}

# sensor faults over the winter (the readings are the sensor's; the air is the generator's truth)
ICING_PASSES = ("R3", "R5")
WET_FILTER = "Q3"
CONNECTOR = ("L3", 3150)        # from this hour index, intermittent spikes
SHIELD = ("T1", 1950)           # from this hour index, sun heating on still days

FILES = {
    "feed": "sdhd_ess_atmospheric_2026_27.csv",
    "qc": "quillan_qc_withheld_log_2026_27.csv",
    "register": "sdhd_rwis_site_register.xlsx",
    "standard": "sdhd_road_weather_data_quality_standard_rev2.pdf",
    "qcconfig": "quillan_air_temperature_qc_configuration_v4_3.pdf",
    "sla": "quillan_service_agreement_schedule_b.pdf",
    "messages": "sdhd_central_server_message_log_2026_27.csv",
    "modems": "sdhd_cellular_modem_register.xlsx",
    "outages": "sdhd_rwis_planned_outage_notices_2026_27.csv",
    "pavement": "sdhd_pavement_sensor_readings_2026_27.csv",
    "preseason": "sdhd_rwis_preseason_checks_oct2026.xlsx",
    "nwp": "hrrr_point_forecasts_sdhd_2026_27.csv",
    "traffic": "sdhd_atr_daily_volumes_2026.csv",
    "email": "rwis_winter_review_request.eml",
}
DISTRACTORS = ("nwp", "traffic")
DELIVERABLES = ("rwis_spatial_check_review_2027.xlsx", "spatial_check_retune_memo_2027.docx")
