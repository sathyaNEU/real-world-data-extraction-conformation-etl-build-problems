"""Fixed parameters of the Kessock Lake world (task159, architecture 2). Every random draw is seeded from here."""
import datetime as dt

SEED = 15902

# Block model geometry, mine grid (metres; mine RL = metres above sea level + 1000)
BX, BY, BZ = 10.0, 10.0, 5.0
X0, Y0, ZTOP = 10000.0, 20000.0, 1300.0
NX, NY, NZ = 112, 52, 50          # 1120 m x 520 m x 250 m model extent
BLOCK_VOL = BX * BY * BZ           # 500 m3

# Grade model of the Main Zone (log-normal pieces); the model is right on average at every estimate
MODEL_MEDIAN = 0.45                # g/t
MODEL_LOG_SD = 0.75
FIELD_RANGES = (24.0, 15.0, 10.0)  # metres along x, y, z
BLOCK_LOG_SD = 0.42                # true block grade about the model estimate
HOLE_LOG_SD = 0.50                 # one blast-hole assay about its block's true grade
P_HOLES = ((1, 0.05), (2, 0.55), (3, 0.40))

# Mining sequence
HIST_BENCH_FLOORS = list(range(1295, 1215, -5))   # 1295 .. 1220, mined Jan 2023 to Oct 2026
PLAN_BENCH_FLOORS = list(range(1215, 1185, -5))   # 1215 .. 1190, the 2027 schedule
HIST_START = dt.date(2023, 1, 1)
HIST_MONTHS = 46                                  # Jan 2023 .. Oct 2026

# Cut-offs (g/t on grade control)
OLD_ORE_CUT = 0.50
LG_LOW_CUT = 0.30
NEW_ORE_CUT = 0.90

TROY = 31.1034768

# Survey: mine grid <-> UTM NAD83(CSRS) zone 17N
ROT_DEG = 31.25          # mine grid north is UTM grid north rotated 31.25 degrees east (clockwise)
SCALE = 0.999620         # UTM grid distance per mine-grid (ground) metre
E_ORIGIN, N_ORIGIN = 471_836.420, 5_372_118.905   # UTM of mine grid (10000, 20000)

# Dates in the fiction
LIMS_PULL = dt.date(2026, 11, 5)
PLAN_DATE = dt.date(2026, 11, 9)
BASIS_DATE = dt.date(2026, 11, 12)
BOARD_DATE = dt.date(2026, 12, 8)
EXPORT_MTIME = dt.datetime(2026, 11, 13, 9, 30, 0)

# The 2027 schedule ends partway along bench 1185 (planned face position, mine grid easting)
PLAN_1185_FACE_X = 10_150.0

# Dispatch: share of hauls the dispatch system logged a second time (auto-assigned while a truck's GNSS dropped out)
PHANTOM_RATE = 0.043

# Low-grade stockpile at the 2022 year-end survey
LGSP_OPEN_T = 2_164_310
LGSP_OPEN_G = 0.39
