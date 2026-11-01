"""Fixed parameters of the Ravelmond world (architecture 2). Everything the generator draws comes from SEED."""
import datetime as dt

SEED = 25502
ASKS_SALT = 298                             # the commercial records' own stream
HEALTH_SALT = 187                           # the season's operations (failures, outages, swaps, player log)
TASK = "task255"
AS_OF = dt.date(2026, 11, 13)            # the head of audience research's request date (fiction)
WIN_START = dt.date(2026, 10, 5)          # Monday
WIN_END = dt.date(2026, 11, 1)            # Sunday (inclusive)
EXTRACT_START = dt.date(2026, 10, 1)      # the operator's extract starts and ends a few days either side
EXTRACT_END = dt.date(2026, 11, 4)
DST_END = dt.date(2026, 10, 25)           # CEST to CET at 03:00 local
TIER_LINE = 40.0                          # Tier G: effective reach of 40.0 per cent or more
EFFECTIVE_FREQ = 3                        # three passes or more

# ---------------------------------------------------------------- network
# station code, name; branch letter; a station on two lines carries both
STATIONS = [
    # M1 north, terminus first
    ("KVA", "Kievitsakker", "N"), ("WLH", "Wilgenhof", "N"), ("MZT", "Molenzicht", "N"),
    ("BKW", "Boekweitstraat", "N"), ("LDO", "Lindeoord", "N"), ("TRV", "Torenveld", "N"),
    ("RHB", "Raadhuisbrug", "N"),
    ("CEN", "Centraal", "X"),
    # M1 south
    ("STP", "Stadspoort", "S"), ("GHP", "Gasthuisplein", "S"), ("RVP", "Ravelpark", "S"),
    ("UNI", "Universiteit", "S"), ("ZDV", "Zuiderveld", "S"), ("ZHV", "Zuidhaven", "S"),
    # M2 west, terminus first
    ("WKD", "Westerkade", "W"), ("ZTP", "Zoutpannen", "W"), ("TWB", "Touwbaan", "W"),
    ("VSW", "Visserswijk", "W"), ("HTM", "Houtmarkt", "W"), ("KST", "Kaaistraat", "W"),
    # M2 east
    ("WSK", "Wisselkwartier", "E"), ("KNO", "Kanaaloever", "E"), ("OSP", "Oosterpoort", "E"),
    ("HDH", "Handelshaven", "E"), ("KCP", "Kenniscampus", "E"), ("OGD", "Oostergaarde", "E"),
    ("OSE", "Oostereind", "E"),
    # M3 only
    ("ZDW", "Zuidwijk", "P"), ("TNS", "Tuinstede", "P"), ("SPL", "Sportlaan", "P"),
    ("VLH", "Veldhuizen", "P"), ("PDZ", "Polderzicht", "P"), ("NOP", "Noordoostpunt", "P"),
]
LINES = {
    "M1": ["KVA", "WLH", "MZT", "BKW", "LDO", "TRV", "RHB", "CEN", "STP", "GHP", "RVP", "UNI", "ZDV", "ZHV"],
    "M2": ["WKD", "ZTP", "TWB", "VSW", "HTM", "KST", "CEN", "WSK", "KNO", "OSP", "HDH", "KCP", "OGD", "OSE"],
    "M3": ["ZDW", "TNS", "RVP", "SPL", "VLH", "HDH", "PDZ", "NOP"],
}
INTERCHANGES = {"CEN": ("M1", "M2"), "RVP": ("M1", "M3"), "HDH": ("M2", "M3")}
PASSAGE_WALK = {"CEN": 8.0, "RVP": 9.0, "HDH": 8.0}      # minutes, platform to platform through the passage
# (the M3 platforms at Ravelpark and Handelshaven lie across the square, so no two-change route is ever faster)

# weekday frequency bands (start minute after midnight, end, headway minutes) for M1 and M2
WEEKDAY_BANDS = [(345, 390, 5.0), (390, 600, 3.0), (600, 930, 4.0), (930, 1140, 3.0), (1140, 1320, 4.0),
                 (1320, 1470, 5.0)]
SAT_BANDS = [(390, 1470, 5.0)]
SUN_BANDS = [(420, 1470, 5.0)]
M3_HEADWAY = {"peak": 5.0, "day": 7.5, "weekend": 10.0, "late": 10.0}
# the weekday peak service: trains passing Centraal in these windows run M1 north <-> M2 east and M2 west <-> M1 south
INTERWORK = [(420, 570), (960, 1110)]

PACKAGES = {
    "CEN": ("Centraal", ["CEN-HN", "CEN-HZ", "CEN-OV"]),
    "BNS": ("Binnenstad", ["CEN-OV", "RHB-H", "STP-H", "WSK-H"]),
    "OVP": ("Overstappunten", ["CEN-OV", "RVP-OV", "HDH-OV"]),
    "NRD": ("Noordtak", ["KVA-H", "WLH-H", "MZT-H", "BKW-H", "LDO-H", "TRV-H"]),
    "OST": ("Oosttak", ["KNO-H", "OSP-H", "HDH-H", "HDH-OV", "KCP-H", "OGD-H", "OSE-H"]),
    "WST": ("Westtak", ["WKD-H", "ZTP-H", "TWB-H", "VSW-H", "HTM-H"]),
    "ZDT": ("Zuidtak", ["STP-H", "GHP-H", "RVP-H", "RVP-OV", "UNI-H", "ZDV-H", "ZHV-H"]),
    "RNG": ("Ringlijn", ["ZDW-H", "TNS-H", "SPL-H", "VLH-H", "PDZ-H", "NOP-H"]),
    "EIN": ("Eindhaltes", ["KVA-H", "ZHV-H", "WKD-H", "OSE-H", "ZDW-H", "NOP-H"]),
}
PACKAGE_ORDER = ["CEN", "BNS", "OVP", "NRD", "OST", "WST", "ZDT", "RNG", "EIN"]

# ---------------------------------------------------------------- riders
N_REGULAR = 2183
N_OCCASIONAL = 3200
N_STAFF = 34
HOME_W = {"N": 0.27, "S": 0.14, "W": 0.16, "E": 0.12, "P": 0.27, "X": 0.04}
# work branch given home branch
WORK_W = {
    "N": {"X": 0.12, "E": 0.64, "S": 0.02, "W": 0.03, "N": 0.16},
    "S": {"X": 0.11, "W": 0.58, "E": 0.04, "N": 0.02, "P": 0.11, "S": 0.14},
    "W": {"X": 0.11, "S": 0.63, "E": 0.02, "N": 0.03, "W": 0.18},
    "E": {"X": 0.13, "N": 0.56, "S": 0.03, "W": 0.03, "P": 0.11, "E": 0.14},
    "P": {"X": 0.12, "E": 0.37, "S": 0.40, "P": 0.06},
    "X": {"E": 0.30, "S": 0.25, "N": 0.15, "W": 0.15, "P": 0.15},
}
PATTERN_W = {"peak": 0.88, "shift": 0.05, "mixed": 0.07}
