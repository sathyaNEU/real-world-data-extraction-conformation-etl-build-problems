"""Fixed facts of the task110 world. Everything the generator draws at random is seeded from SEED."""
import datetime as dt

SEED = 110

ORG = "Quandong Imaging Group"
PRACTICE = "Yacaaba Radiology"
PRACTICE_CODE = "YCB"

# the fiction's calendar
ACQUIRED_BY_GROUP = dt.date(2024, 3, 1)
REPLAY_FIRST = (2025, 7)
REPLAY_LAST = (2026, 9)
COUNT_OPENS = dt.date(2026, 9, 28)
COUNT_CUTOFF_LOCAL = dt.datetime(2026, 10, 9, 17, 0)      # 5:00 pm local, Friday 9 October
DST_STARTS_UTC = dt.datetime(2026, 10, 3, 16, 0)         # 2:00 am AEST Sunday 4 October = 16:00Z Saturday
REGISTER_EXPORT = dt.date(2026, 10, 2)
TB_PRELIM_RUN = dt.date(2026, 10, 3)
RECLASS_POSTED = dt.date(2026, 10, 8)
TB_FINAL_RUN = dt.date(2026, 10, 9)
PACK_DATE = dt.date(2026, 10, 13)
CUTOVER = dt.date(2027, 1, 1)

SITES = {
    "CHA": "Charlestown",
    "MAI": "Maitland",
    "CES": "Cessnock",
    "RAY": "Raymond Terrace",
}

# Yacaaba's legacy chart (MYOB-style codes): category -> (cost account, accumulated account, expense account)
ACCOUNTS = {
    "Medical imaging equipment": ("1-6110", "1-6115", "6-2110"),
    "Equipment upgrades": ("1-6110", "1-6115", "6-2110"),
    "Options & accessories": ("1-6110", "1-6115", "6-2110"),
    "Ultrasound": ("1-6120", "1-6125", "6-2120"),
    "Computer equipment": ("1-6130", "1-6135", "6-2130"),
    "Leasehold improvements": ("1-6140", "1-6145", "6-2140"),
    "Furniture & fittings": ("1-6150", "1-6155", "6-2150"),
    "Motor vehicles": ("1-6160", "1-6165", "6-2160"),
}
ACCOUNT_NAMES = {
    "1-6110": "Medical Imaging Equipment at Cost",
    "1-6115": "Medical Imaging Equip Accum Dep",
    "1-6120": "Ultrasound Equipment at Cost",
    "1-6125": "Ultrasound Equipment Accum Dep",
    "1-6130": "Computer Equipment at Cost",
    "1-6135": "Computer Equipment Accum Dep",
    "1-6140": "Leasehold Improvements at Cost",
    "1-6145": "Leasehold Improvements Accum Dep",
    "1-6150": "Furniture & Fittings at Cost",
    "1-6155": "Furniture & Fittings Accum Dep",
    "1-6160": "Motor Vehicles at Cost",
    "1-6165": "Motor Vehicles Accum Dep",
    "6-2110": "Depreciation - Medical Imaging Equip",
    "6-2120": "Depreciation - Ultrasound",
    "6-2130": "Depreciation - Computer Equipment",
    "6-2140": "Depreciation - Leasehold Improvements",
    "6-2150": "Depreciation - Furniture & Fittings",
    "6-2160": "Depreciation - Motor Vehicles",
}

# the accountant's rate card (the register workbook's "Rates" tab)
LIFE_MONTHS = {
    "Medical imaging equipment": 120,
    "Options & accessories": 60,
    "Ultrasound": 72,
    "Computer equipment": 48,          # 36 months before 1 July 2025, applied prospectively
    "Leasehold improvements": 180,
    "Furniture & fittings": 120,
    "Motor vehicles": 72,
}
IT_OLD_LIFE = 36
IT_CHANGE = (2025, 7)
CAP_THRESHOLD = 1500

# group asset classes and the mapping versions (legacy account -> group class)
GROUP_CLASSES_V2 = ["Imaging equipment", "Clinical equipment", "Computer equipment",
                    "Leasehold improvements", "Furniture and fittings", "Motor vehicles"]
MAP_V2 = {"1-6110": "Imaging equipment", "1-6120": "Clinical equipment", "1-6130": "Computer equipment",
          "1-6140": "Leasehold improvements", "1-6150": "Furniture and fittings", "1-6160": "Motor vehicles"}

PEOPLE = {
    "audit": ("Cynthia Rice", "Internal Audit Manager"),
    "cfo": ("Timothy Hill", "Chief Financial Officer"),
    "accountant": ("Lorraine Wright", "Wright Accounting Partners"),
    "migration": ("Ronald Lawrence", "Finance Systems Lead"),
    "practice": ("Donna Ramirez", "Practice Manager, Yacaaba Radiology"),
}
# v3, issued for review on 30 September 2026 and not approved: ultrasound folds into imaging and the
# vehicles fold into furniture
MAP_V3 = {"1-6110": "Imaging equipment", "1-6120": "Imaging equipment", "1-6130": "Computer equipment",
          "1-6140": "Leasehold improvements", "1-6150": "Furniture, fittings and vehicles",
          "1-6160": "Furniture, fittings and vehicles"}

