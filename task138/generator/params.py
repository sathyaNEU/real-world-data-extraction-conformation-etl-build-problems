"""World constants for task138 architecture 2: the Orrinsford levee and the Tamsen River.

Everything the world draws from a seed sits here, so a rebuild from these numbers is the same pack byte for byte.
"""

SEED = 1445            # the annual-peak world (chosen by search against the ladder conditions, see the design note)
SURVEY_SEED = 1380322   # crown surveys and benchmark shots
TELEM_SEED = 1380423    # hourly telemetry at both gauges
OTHER_SEED = 1380524    # the other basin gauges, distractors

AS_OF = "2026-11-09"    # the fiction's date: the district engineer's review for the 2027 capital plan
FIRST_WY, LAST_WY = 1962, 2026

# drainage areas, square miles
DA = {"ASH": 3880.0, "COY": 4930.0, "GALE": 412.0, "HAL": 6480.0, "FEN": 7050.0}

# Coyle Bridge annual peak distribution (log10 cfs); the realised record is the seed's draw
COY_LOG_MEAN, COY_LOG_SD, COY_LOG_SKEW = 4.475, 0.205, 0.0

# the intervening area's contribution at Orrinsford's crest, as a share of the Coyle Bridge peak
# (the intervening tributaries crest a day before the main-stem flood reaches the town, so the town's crest carries
# their recession flow, a share of the Coyle Bridge peak that changes little from flood to flood)
LOCAL_MEAN, LOCAL_SD, LOCAL_LO, LOCAL_HI = 0.065, 0.009, 0.035, 0.130
# the old agricultural levees overtopped above about the five-year flood at Coyle Bridge; the floodplain behind
# them then held back this share of every cfs above that level
OVERTOP_CFS = 46000.0
ATTEN = 0.56
ATTEN_SPREAD = 0.20     # flood-to-flood variation in the share held back (longer floods fill more of the storage)
NOISE_T = 0.0055        # Orrinsford's peak against the two-gauge relation, relative
LOCAL_EVENT_P = 0.16    # years whose Orrinsford peak came from a storm on the intervening area alone

# the agricultural levee districts between Coyle Bridge (RM 41.0) and Orrinsford (RM 12.6); raise = calendar year
# the crown raise was completed (in force from the next water year)
DISTRICTS = [
    # (id, sponsor, bank, from_rm, to_rm, year_built, raise_year, protected_acres)
    ("TR-L-07", "Pelham Bottoms Drainage and Levee District", "Left", 39.6, 34.1, 1951, 1996, 9420),
    ("TR-R-06", "Krenz Island Levee District", "Right", 38.2, 31.7, 1956, 1998, 7860),
    ("TR-L-08", "Gale Creek Drainage District No. 4", "Left", 33.6, 27.4, 1949, 2001, 11380),
    ("TR-R-07", "Lindley Bottoms Levee District", "Right", 31.1, 23.9, 1958, 2003, 8940),
    ("TR-L-09", "Orchard Point Levee District", "Left", 26.8, 20.2, 1953, 2005, 6710),
    ("TR-R-08", "Mill Slough Drainage District No. 2", "Right", 23.5, 15.8, 1961, 2008, 10230),
]
# districts outside the Coyle Bridge to Orrinsford reach (rows in the inventory, no effect on Orrinsford's peaks)
OTHER_LEVEES = [
    ("TR-L-04", "Ashby Flats Levee District", "Left", 58.4, 52.9, 1955, None, 5120),
    ("TR-R-03", "Cutler Bend Drainage District No. 1", "Right", 49.7, 44.6, 1962, None, 3380),
    ("TR-R-11", "Fenwick Lowlands Levee District", "Right", 9.8, 4.1, 1957, 2002, 6940),
    ("TR-L-12", "Sugar Grove Levee District", "Left", 7.6, 1.2, 1966, None, 2860),
]

# the Orrinsford levee (left bank, RM 14.0 to 10.6); 2024 stationing from the north tie-in built in 2019
LEVEE_LEN_FT = 18000
# the 2019 north tie-in realignment took the levee's first 650 ft out of service: a station on the stationing in use
# before 2019 sits at the present station 650 ft lower
OLD_STATION_SHIFT = 700
BRIDGES = {"Main Street bridge": 6240, "Prairie and Western Railroad bridge": 11870}
TABLE4_STATIONS = [0, 1000, 2000, 3000, 4000, 5000, 6000, 6240, 7000, 8000, 9000, 10000, 11000, 11870,
                   12000, 13000, 14000, 15000, 16000, 17000, 18000]
TABLE4_Q = [65000, 75000, 85000, 95000, 105000, 115000, 125000, 135000, 145000, 155000]
# design water surface: WSE = BASE_Z + SLOPE*(L - sta) + C*(Q/10000)**EXP, plus bridge afflux at the bridge faces
WS_BASE_Z, WS_SLOPE, WS_C, WS_EXP = 601.20, 0.000215, 6.80, 0.58
AFFLUX = {6240: (0.42, 0.85), 11870: (0.55, 1.40)}   # afflux = a + b*(Q/100000)**2 at the upstream face
FREEBOARD = 3.0
FREEBOARD_BRIDGE = 4.0     # within 100 ft of a bridge
FREEBOARD_UPSTREAM_EXTRA = 0.5  # at station 0+00, tapering to nothing at the downstream end
RAISES_FT = [0, 1, 2, 3, 4]

REGIONAL_SKEW, REGIONAL_SKEW_MSE = -0.08, 0.14
AEP = 0.01

# vertical datum: NAVD 88 = NGVD 29 + this, along the Orrinsford levee (from the benchmark pairs)
NGVD_TO_NAVD = 0.27
# Coyle Bridge gauge datum lowered 2.00 ft on 22 October 2019 (stage reads 2.00 ft higher for the same water)
COY_DATUM_CHANGE = "2019-10-22 15:00"   # UTC
COY_DATUM_SHIFT = 2.00
# Orrinsford logger: Central Standard Time stamps until the upgrade, UTC stamps after
HAL_LOGGER_UPGRADE_UTC = "2021-06-08 15:00"
HAL_OLD_LOGGER_OFF_UTC = "2021-06-11 15:00"   # the old logger ran beside the new one for three days
HAL_GAUGE_DATUM = 600.00     # ft NAVD 88 (599.73 ft NGVD 29), below the lowest water the gauge sees
WARNING_STAGE_OLD = 21.0     # Coyle Bridge, the 2014 procedure's stage (gauge datum before October 2019)
MAIN_ST_SILL = 616.95        # ft NAVD 88, the Main Street closure sill (about 30,700 cfs at Orrinsford)
# Coyle Bridge rating on the old datum: stage = a + b * Q**c (24,000 cfs at the warning stage)
COY_RATING = (3.6, 0.0122, 0.72)
COY_DATUM_OLD = 640.00       # ft NGVD 29, the Coyle Bridge gauge datum until October 2019 (638.00 after)

# the crown at the railroad bridge station sits this far below the present river's design water surface plus its
# freeboard (a world parameter, set so every graded figure clears its rounding edge; the design note's search)
NEED_11870 = 1.500

TELEM_START, TELEM_END = "2016-10-01 00:00", "2026-09-30 23:00"
