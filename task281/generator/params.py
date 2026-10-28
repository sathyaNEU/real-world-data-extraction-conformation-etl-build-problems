"""Constants for task281: Tallisford Power & Light's 2027 group driver replacement program.

The world: an investor-owned electric utility in north-central Ohio owns its company streetlights in eight towns and
converted them from high-pressure sodium to LED cobra-heads in ten phases (January 2021 to September 2025) under one
installation contract, all luminaires from one maker in one catalog family. The maker built each delivery lot with
drivers from one of two driver makers. The record closes on 31 December 2026; the program is decided in January 2027."""
import datetime as dt

SEED = 2895
RECORD_END = dt.date(2026, 12, 31)       # the last day the work-management record covers
AS_OF = dt.date(2027, 1, 1)              # the program's population date
HORIZON_Y = 12.0                         # the twelfth anniversary of installation
TRIGGER = 0.45                           # a phase enters when the expected share exceeds 45 per cent
YEAR_D = 365.25
CUTOVER = dt.date(2023, 7, 1)            # the work-management system cutover (legacy to June 2023)
ASSEMBLED = dt.datetime(2027, 1, 14, 16, 20)

UTILITY = "Tallisford Power & Light"
UTIL_SHORT = "TP&L"
MAKER = "Halberd Lighting Company"
INSTALLER = "Brayle Electric, Inc."
# driver makers: A wears out (the lifetime the fleet shows), B does not within any horizon here
DRV = {"A": "Vantrel Power Systems", "B": "Corvane Electronics"}
# each maker supplies one programmable driver, set at the factory to the luminaire's output
DRV_PART = {"A": "VT-PD150", "B": "CV-P150"}
DRV_REV = {"A": "B3", "B": "03"}
CATALOG = {40: "HRX-2-40W-40K", 70: "HRX-3-70W-40K", 110: "HRX-4-110W-40K"}

# truth: source-A drivers wear out on a two-parameter Weibull in years of service; source-B drivers fail at a low
# constant rate (component defects); every luminaire also leaves service on knockdowns, warranty luminaire swaps
# and pole removals, and has outages that need no driver (photocontrols, wiring faults, blown fuses)
K_A, LAM_A = 3.2, 10.04
RATE_B = 0.0002                          # per year
EXIT = {"knockdown": 0.0060, "luminaire": 0.0018, "pole_removed": 0.0012}
OTHER = {"photocontrol": 0.030, "wiring": 0.011, "fuse": 0.009}
OTHER_HPS = {"lamp": 0.15, "ballast": 0.02, "photocontrol": 0.030, "wiring": 0.011, "fuse": 0.009}
REPROG_2026 = 0.040                      # share of 110 W luminaires reprogrammed to 70 W in 2026 (glare complaints)
REPROG_2025 = 0.008
SHIELD_RATE = 0.012                      # glare complaints answered with a house-side shield instead
UG_SHARE = 0.30                          # share of streets fed by underground circuits
UG_FAULT_RATE = 0.10                     # cable faults per circuit-year

# towns: code, name, NLC-dimmed (networked controls dim 00:00 to 05:00)
TOWNS = [("AMB", "Ambrosine", False), ("CRV", "Corrinvale", True), ("DLW", "Dalwinter", False),
         ("FLM", "Fallowmere", False), ("GRH", "Garrick Hollow", False), ("HLB", "Halverne Bend", False),
         ("KST", "Kesterbrook", False), ("LKH", "Larkhaven", False)]
TOWN_CODES = [t[0] for t in TOWNS]
TOWN_NAME = {t[0]: t[1] for t in TOWNS}
TOWN_NLC = {t[0]: t[2] for t in TOWNS}

# phases: code, first install, last install, luminaires, source-A share, towns (weights)
PHASES = [
    ("P1", "2021-01-11", "2021-06-25", 4320, 0.70, {"CRV": .55, "AMB": .45}),
    ("P2", "2021-06-28", "2021-12-10", 3921, 0.42, {"DLW": .60, "AMB": .40}),
    ("P3", "2022-01-10", "2022-06-24", 5139, 0.82, {"FLM": .50, "CRV": .30, "GRH": .20}),
    ("P4", "2022-06-27", "2022-12-09", 4465, 0.44, {"GRH": .55, "HLB": .45}),
    ("P5", "2023-01-09", "2023-06-23", 4025, 0.68, {"KST": .70, "DLW": .30}),
    ("P6", "2023-06-26", "2023-12-08", 5540, 0.16, {"LKH": .60, "HLB": .40}),
    ("P7", "2024-01-08", "2024-06-21", 4264, 0.76, {"FLM": .45, "KST": .55}),
    ("P8", "2024-06-24", "2024-12-06", 3674, 0.18, {"AMB": .35, "LKH": .65}),
    ("P9", "2025-01-13", "2025-06-20", 4918, 0.72, {"GRH": .40, "CRV": .30, "DLW": .30}),
    ("P10", "2025-06-23", "2025-09-26", 3420, 0.14, {"HLB": .50, "KST": .50}),
]
PHASE_CODES = [p[0] for p in PHASES]
LOT_SIZE = (260, 380)
WATT_MIX = {40: 0.52, 70: 0.33, 110: 0.15}
HPS_FOR = {40: [(70, .55), (100, .45)], 70: [(100, .40), (150, .60)], 110: [(150, .35), (250, .65)]}

# tariff (Schedule SL): input watts per fixture and the dusk-to-dawn burning hours by month
INPUT_W = {("HPS", 70): 95, ("HPS", 100): 128, ("HPS", 150): 188, ("HPS", 250): 297,
           ("LED", 40): 41, ("LED", 70): 72, ("LED", 110): 113}
BURN_H = [443, 374, 360, 315, 285, 262, 274, 304, 331, 375, 404, 436]   # January to December, 4,163 a year
DIM_LEVEL = 0.50                          # NLC luminaires burn at half input from 00:00 to 05:00
DIM_H_PER_NIGHT = 5.0

# the tariff's repair standard: an outage repaired within three days of its first report
REPAIR_STD_H = 72

PEOPLE = {"asset_engineer": "Andrew King", "wms_admin": "Shawn Hoover", "purchasing": "Sabrina Mccarthy",
          "installer_pm": "Ebony Rivera"}

FILES = {
    "note": "tpl_streetlight_lifecycle_model_note.pdf",
    "register": "streetlight_register_2026-12-31.csv",
    "install": "brayle_install_logs_2021-2025.xlsx",
    "coc": "halberd_certificates_of_conformance_2020-2025.pdf",
    "wo_legacy": "wms_legacy_work_orders_2021-01_2023-06.csv",
    "wo_new": "work_orders_2023-07_2026-12.csv",
    "reports": "customer_outage_reports_2026.csv",
    "tariff": "schedule_sl_street_lighting_tariff_2026.pdf",
    "nlc": "corrinvale_nlc_dimming_profiles_2026.csv",
    "billing": "sl_billing_lines_dec2026.csv",
    "weather": "tpl_ops_center_daily_temperature_2021-2026.csv",
    "vegetation": "vegetation_clearance_patrols_2025-2026.csv",
}
DISTRACTORS = ["billing", "weather", "vegetation"]
GOLDEN_XLSX = "2027_group_driver_replacement.xlsx"
GOLDEN_PNG = "driver_failure_projection_by_phase.png"
DELIVERABLES = [GOLDEN_XLSX, GOLDEN_PNG]
