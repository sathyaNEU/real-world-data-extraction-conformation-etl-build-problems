"""task458 architecture 3: the world's fixed facts (Ashlund Home Group, FY2026 close)."""
import datetime as dt

SEED = 45803
TASK = "task458"

# calendar
FY = 2026
YEAR_END = dt.date(2026, 12, 31)
ASOF = dt.date(2027, 1, 22)          # the close pack is assembled
COMMITTEE = dt.date(2027, 2, 10)     # audit committee
WEEK0 = dt.date(2021, 1, 4)          # first Monday of the outlet's trading record

# entities
SUBS = ["AHL", "AHI", "AHB"]
SUB_NAME = {"AHL": "Ashlund Home Ltd", "AHI": "Ashlund Home Ireland Ltd", "AHB": "Ashlund Home B.V."}
SUB_CCY = {"AHL": "GBP", "AHI": "EUR", "AHB": "EUR"}
GROUP = "Ashlund Home Group plc"
OUTLET = "Valuehall Stores Ltd"

DIVISIONS = ["KD", "SL", "LE", "TH", "GO"]
DIV_NAME = {"KD": "Kitchen and Dining", "SL": "Storage and Laundry", "LE": "Lighting and Electrical",
            "TH": "Tools and Hardware", "GO": "Garden and Outdoor"}

# Valuehall's stores: opening Monday of each
STORES = [("VH01", "Leicester Fosse Park", dt.date(2021, 3, 15)),
          ("VH02", "Nottingham Castle Marina", dt.date(2022, 5, 9)),
          ("VH03", "Derby Kingsway", dt.date(2023, 4, 3)),
          ("VH04", "Coventry Arena", dt.date(2024, 6, 3)),
          ("VH05", "Northampton Riverside", dt.date(2025, 4, 7))]

# the outlet's physics (the generator's truth; nothing below ships as a number)
THROUGHPUT = 9640.0      # cost value of clearance stock a fully stocked store sells in a full trading week
THROUGHPUT_SD = 0.035    # week-to-week noise on a stocked week
COVER_FULL = 3.0         # weeks of throughput on hand at which a store sells at its throughput
OUTLET_RECOVERY = 0.618  # ex-VAT proceeds over cost at the outlet's standard clearance pricing
JOBBER_RECOVERY = 0.102  # bulk-lot price over cost

# 2027 plan: five stores, Leicester shut two weeks for a refit in February
PLAN_2027_WEEKS = {"VH01": 50, "VH02": 52, "VH03": 52, "VH04": 52, "VH05": 52}

# money and covenant
FX_CLOSE = 0.8648       # GBP per EUR at 31 December 2026, the group rate table
FX_AVG_2025 = 0.8573    # the group's 2025 average rate
FX_AVG_2026 = 0.8691
BB_ADVANCE = 0.625      # borrowing base advance rate on inventories
DRAWN = 25_120_000      # drawn on the revolving facility at 31 December 2026
FACILITY = 32_000_000

# the AHI unit conversion in the old ERP: lines before this date carry cases (the export labels every line EA)
AHI_UOM_SWITCH = dt.date(2025, 7, 7)
# AHL served Corrib Home & Garden from Leicester, invoicing in euro, until AHI took the account over
CORRIB_HANDOVER = dt.date(2025, 9, 1)

# people (guard.py names --geo "United Kingdom" --seed 458)
CONTROLLER = "Caroline Burns"
OUTLET_OPS = "Liam Elliott"
