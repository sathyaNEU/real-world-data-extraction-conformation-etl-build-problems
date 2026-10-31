"""task482 architecture 16: the world's constants. Brackwell Alloys (a fictional secondary aluminium works in the
West Midlands) and Velden (a fictional German car maker); every figure here is synthetic."""
import datetime as dt

SEED = 48216
YEAR = 2026
TZ = "Europe/London"

# product families: code, name on the works' records, melt yield (tonnes melted per tonne passing inspection)
FAMILIES = [
    ("BIL6063", "6063 extrusion billet", 1.075),
    ("BIL6082", "6082 extrusion billet", 1.080),
    ("INGLM25", "LM25 foundry ingot", 1.020),
    ("CSTLM25", "LM25-TF sand castings", 1.650),
]
FAM_CODES = [f[0] for f in FAMILIES]
FAM_NAME = {f[0]: f[1] for f in FAMILIES}
YIELD = {f[0]: f[2] for f in FAMILIES}
CASTHOUSE_MIX = {"BIL6063": 0.52, "BIL6082": 0.19, "INGLM25": 0.29}   # share of casthouse heats

# the gas each process burns (kWh): the world's truth, never shipped
MELT_KWH_PER_T = 820.0        # casthouse reverberatory furnaces M1, M2, per tonne melted
M3_KWH_PER_T = 611.1          # foundry tower melter M3, per tonne melted
H1_KW = 1500.0                # homogenizing furnace, while a load cycles
T1_KW = 550.0                 # solution and ageing oven, while a batch cycles
PILOT_KW = 100.0              # burners' pilots and the launder heaters' standing flames, all year
SPACE_KW_PER_K = 45.0         # the works' radiant tube heaters, per kelvin below 15.5 C outdoors
SPACE_BASE_C = 15.5

# process timing
HEAT_T = (38.0, 1.6)          # casthouse charge, tonnes (mean, sd)
HEAT_MELT_H = (5.6, 0.35)     # charge to melt complete, hours
HEAT_CYCLE_H = (9.3, 0.7)     # charge to next charge on the same furnace
M3_CHARGE_T = (1.55, 0.12)    # foundry tower melter charge, tonnes
M3_RATE_T_PER_H = 1.0
H1_LOAD_T = (50.0, 1.2)
H1_CYCLE_H = {"BIL6063": (6.0, 0.25), "BIL6082": (15.0, 0.4)}
H1_TURN_H = 0.75              # unload and reload between loads
T1_BATCH_T = (6.0, 0.35)
T1_CYCLE_H = (16.0, 0.4)

# SCR-2 (filed in Velden's requirement)
CO2_KG_PER_KWH = 0.18296      # natural gas, gross calorific value
LIMIT_T_PER_T = 0.235
PREMIUM_EUR_PER_T = 38
CALLOFF_2027 = {"BIL6063": 7200, "BIL6082": 3000, "INGLM25": 1800, "CSTLM25": 650}

# the gas bill
VCF = 1.02264                 # the volume correction factor UK suppliers bill at
HCF_M3 = 2.83                 # the bill's imperial conversion: hundreds of cubic feet to cubic metres
METER_EXCHANGE_LOCAL = dt.datetime(2026, 4, 14, 10, 30)
OLD_METER = "G4 22197 7H"
NEW_METER = "E6S 88420 01"

# the works' calendar (local): days the whole works is shut
SHUT_DAYS = set()
for d0, d1 in [((2026, 1, 1), (2026, 1, 4)), ((2026, 4, 3), (2026, 4, 6)), ((2026, 5, 4), (2026, 5, 4)),
               ((2026, 5, 25), (2026, 5, 25)), ((2026, 8, 3), (2026, 8, 14)), ((2026, 8, 31), (2026, 8, 31)),
               ((2026, 12, 24), (2026, 12, 31))]:
    d = dt.date(*d0)
    while d <= dt.date(*d1):
        SHUT_DAYS.add(d)
        d += dt.timedelta(days=1)

WORKS = "Brackwell Alloys Ltd, Moorcroft Works, Tipton"
BUYER = "Velden Automobil AG"
PEOPLE = {"energy": "Rosemary Kent", "buyer": "Tony Coleman", "works": "Reece Parker"}

# the pack
FILES = dict(
    meter="brackwell_site_gas_meter_2026.csv",
    invoices="brackwell_gas_invoices_2026.pdf",
    furnaces="brackwell_melting_furnace_logs_2026.xlsx",
    h1="brackwell_homogenizing_furnace_h1_2026.csv",
    t1="brackwell_heat_treatment_oven_t1_2026.csv",
    lots="brackwell_production_lots_2026.csv",
    scr2="velden_scr2_supplier_carbon_requirement.pdf",
    calloff="velden_2027_calloff_schedule.xlsx",
    email="brackwell_scr2_data_package.eml",
    weather="brackwell_works_weather_2026.csv",
    weighbridge="brackwell_weighbridge_2026.csv",
    goodsin="brackwell_scrap_goods_in_2026.csv",
    elec="brackwell_electricity_hh_2026.csv",
    assets="brackwell_plant_asset_register.xlsx",
    roster="brackwell_shift_roster_2026.csv",
)
DISTRACTORS = ("elec", "assets", "roster")
DELIVERABLES = ("velden_low_carbon_premium_2027.docx", "brackwell_scr2_figures_2026.csv")

# meter reads on the gas supplier's invoices (local); the exchange falls inside the April to May period
READS = [dt.datetime(2025, 12, 3, 9, 45), dt.datetime(2026, 1, 6, 10, 15), dt.datetime(2026, 2, 4, 9, 30),
         dt.datetime(2026, 3, 4, 11, 0), dt.datetime(2026, 4, 7, 9, 45), dt.datetime(2026, 5, 6, 10, 0),
         dt.datetime(2026, 6, 3, 9, 15), dt.datetime(2026, 7, 3, 10, 30), dt.datetime(2026, 8, 5, 9, 45),
         dt.datetime(2026, 9, 3, 10, 0), dt.datetime(2026, 10, 6, 9, 30), dt.datetime(2026, 11, 4, 10, 45),
         dt.datetime(2026, 12, 3, 9, 45), dt.datetime(2027, 1, 6, 10, 15)]
CV = [39.42, 39.37, 39.51, 39.28, 39.46, 39.33, 39.61, 39.55, 39.40, 39.48, 39.36, 39.52, 39.44]
UNIT_RATE_P = [4.412, 4.412, 4.412, 4.412, 4.412, 4.412, 4.412, 4.412, 4.412, 4.186, 4.186, 4.186, 4.186]
STANDING_GBP_DAY = 18.46
CCL_P_KWH = 0.775

# the weighbridge (ask files): the indicator replaced over the weekend of 27 June, its tickets restarting at 1
WB_RESET = dt.date(2026, 6, 29)
GRADES = [("CST", "Old cast aluminium"), ("EXT", "Extrusion offcuts 6000 series"), ("TRN", "Turnings and swarf"),
          ("UBC", "Used beverage cans, baled")]
TOLL = ("TOL", "Returned metal (toll), sows")
SUPPLIERS = [
    ("Tividale Metals Ltd", ["CST", "TRN", "UBC"], 0.20),
    ("Ocker Hill Non-Ferrous", ["CST", "EXT"], 0.15),
    ("Coseley Can Recycling", ["UBC"], 0.13),
    ("Great Bridge Metals", ["CST", "TRN"], 0.12),
    ("Kestrel Extrusions Ltd", ["EXT"], 0.11),
    ("Albion Profiles Ltd", ["EXT", "TRN"], 0.10),
    ("Princes End Metal Traders", ["CST", "UBC", "TRN"], 0.11),
    ("Wednesbury Scrap Metals", ["CST", "EXT", "UBC"], 0.08),
]
DROSS_HAULIER = "Midland Dross Recovery Ltd"
CUSTOMERS = [("Velden Automobil AG (Rhenus Logistics)", 0.42), ("Kestrel Extrusions Ltd", 0.21),
             ("Albion Profiles Ltd", 0.17), ("Hallam Castings Ltd", 0.12), ("Severn Diecast Ltd", 0.08)]
