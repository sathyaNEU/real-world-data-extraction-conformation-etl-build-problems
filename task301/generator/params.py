"""task301 constants: Fenmore Solar Income plc, its fourteen operating solar farms in southern England, the four
consented candidates for the 2027 build, the 2016 to 2025 weather record and the seeds."""
import datetime as dt

ORG = "Fenmore Solar Income plc"
ADVISER = "Fenmore Renewables Advisory Ltd"

SEED_WORLD = 3024          # weather, the fleet's output, the deposit (scratch prototype t301i, seed 3024)
SEED_ENV = 30101           # the environs listing
SEED_MET = 30102           # ask A: pyranometers, their swaps and their certificates
SEED_OM = 30103            # ask B: alarms, work orders, vans and their arrivals
SEED_DOCS = 30104          # documents and distractors

W0, W1 = dt.date(2016, 1, 1), dt.date(2025, 12, 31)      # the weather record
F0 = dt.date(2022, 1, 1)                                  # the fleet's metered record starts
AS_OF = dt.date(2026, 11, 2)                              # the folder for the December investment committee
Y_ASK = 2025                                              # the year both asks read

# module generations: base performance ratio at 25 C cell, temperature coefficient per C, degradation a year
MOD = {"A": (0.808, -0.0045, 0.0060), "B": (0.836, -0.0040, 0.0050), "C": (0.861, -0.0034, 0.0040)}
MODN = {"A": "Polycrystalline 250 W (2012-14 supply)", "B": "Monocrystalline PERC 320 W",
        "C": "Monocrystalline PERC 410 W bifacial"}

# name, DC MWp, commissioned, module, irradiation factor, wet-day shift, rain amount factor, air temperature offset,
# centroid easting, northing
SITES = [("Ashcombe",        9.8, dt.date(2013, 6, 21), "A", 0.992, -0.08, 1.22, -0.4, 291440, 112380),
         ("Bramble Hill",    6.4, dt.date(2012, 9, 14), "A", 1.004, -0.02, 1.15, -0.2, 318720, 104960),
         ("Wexcombe",       31.8, dt.date(2013, 3, 28), "A", 0.998, -0.18, 1.42, -0.5, 302150, 121870),
         ("Coldharbour",     6.1, dt.date(2014, 3, 31), "A", 1.010,  0.05, 1.05,  0.0, 352880, 131220),
         ("Brindle Moor",   12.4, dt.date(2015, 3, 27), "B", 0.985,  0.10, 1.00, -0.3, 371460, 148830),
         ("Dunsford Lane",  14.9, dt.date(2016, 3, 30), "B", 1.018,  0.30, 0.78,  0.4, 548350, 212670),
         ("Elmstead",       10.6, dt.date(2016, 6, 29), "B", 1.026,  0.38, 0.72,  0.5, 603910, 224150),
         ("Fairoak",         7.9, dt.date(2017, 3, 24), "B", 0.996,  0.06, 1.04, -0.1, 418830, 118420),
         ("Greystoke Barns", 7.4, dt.date(2018, 5, 18), "B", 1.002,  0.14, 0.95,  0.1, 452760, 137790),
         ("Hartsfield",     11.8, dt.date(2018, 9, 7),  "B", 0.989,  0.00, 1.10, -0.2, 339680, 142330),
         ("Ivy Cross",       9.1, dt.date(2019, 4, 12), "C", 1.021,  0.34, 0.75,  0.4, 571220, 196480),
         ("Furzedown",      10.2, dt.date(2019, 10, 4), "C", 0.981, -0.05, 1.18, -0.3, 286970, 98840),
         ("Jessop's Farm",  13.3, dt.date(2020, 7, 23), "C", 1.012,  0.22, 0.86,  0.2, 502180, 165540),
         ("Knowle Park",    12.0, dt.date(2024, 1, 16), "C", 1.000,  0.12, 0.97,  0.0, 436520, 151290)]
CAND = [("Hallam Down",     11.0, None, "C", 1.04066, 0.40, 0.72, 0.6, 584630, 207350),
        ("Kingsley Fields", 11.0, None, "C", 0.9943, 0.10, 1.00, 0.0, 437870, 139660),
        ("Larkhill Common", 11.0, None, "C", 0.9661, 0.02, 1.08, -0.2, 412390, 146120),
        ("Marston Vale",    11.0, None, "C", 0.95926, -0.06, 1.16, -0.3, 368540, 145380)]
OPERATING = [s[0] for s in SITES]
CANDIDATES = [c[0] for c in CAND]
BIFACIAL = [s[0] for s in SITES if s[3] == "C"]
# mounting: Knowle Park was the first farm built on the raised two-in-portrait frame at a wide pitch that the 2027 build
# repeats; the earlier bifacial farms sit on the lower frame of the 320 W farms
LAYOUT = {"A": "fixed tilt 30 deg, 2 modules in landscape, 1.0 m clearance, 6.2 m pitch",
          "B": "fixed tilt 25 deg, 2 modules in portrait, 0.8 m clearance, 7.4 m pitch",
          "C": "fixed tilt 25 deg, 2 modules in portrait, 0.8 m clearance, 7.4 m pitch",
          "KP": "fixed tilt 25 deg, 2 modules in portrait, 1.3 m clearance, 9.0 m pitch"}

# balance of system: wiring, inverter and mismatch losses particular to each farm
BOS = {"Ashcombe": 0.993, "Bramble Hill": 0.988, "Wexcombe": 1.004, "Coldharbour": 1.002, "Brindle Moor": 0.991,
       "Dunsford Lane": 1.006, "Elmstead": 0.996, "Fairoak": 1.012, "Greystoke Barns": 0.984, "Hartsfield": 1.003,
       "Ivy Cross": 0.986, "Furzedown": 0.991, "Jessop's Farm": 0.989, "Knowle Park": 1.000}
EXPORT_LOSS = 0.984        # inverter AC to the export meter: transformer and cable

# the deposit: broiler litter dust settling on dry days, washed partly by 4 mm of rain and almost wholly by 10 mm
LO, HI, CAP = 4.0, 10.0, 0.25
WASH_LO, WASH_HI = 0.55, 0.08
BG = 0.00035               # ordinary field dust, every site
R0, DL, D0 = 0.0165, 120.0, 60.0     # a dry day's deposit at D0 m from the sheds, falling off over DL m
OFF_PLUME = 0.35           # the share of that deposit on a day the wind does not blow from the sheds
PLUME_HALF_ANGLE = 45.0
# broiler units whose sheds lie close upwind of blocks: distance m and bearing from the centroid, sheds
SOURCES = {"Wexcombe": (545, 252, 10), "Hallam Down": (105, 229, 10)}

# the build
BUILD_MWP = 11.0
BUILD_YEAR, FIRST_FULL_YEAR = 2027, 2028

FILES = {
    "note": "build_decision_note_2027.docx",
    "terms": "candidate_site_terms_2027.xlsx",
    "register": "site_register.csv",
    "weather": "site_weather_daily_2016-2025.csv",
    "export": "fleet_daily_export_2022-2025.csv",
    "scada": "inverter_daily_energy_2022-2025.parquet",
    "layout": "array_layout_blocks.csv",
    "environs": "site_environs_2km.csv",
    "omlog": "om_event_log_2022-2025.csv",
    "datasheets": "module_datasheets.pdf",
    "met": "met_station_daily_2025.csv",
    "pyrreg": "pyranometer_register.csv",
    "certs": "pyranometer_calibration_certificates.xlsx",
    "alarms": "scada_alarm_log_2025.csv",
    "workorders": "cmms_work_orders_2025.csv",
    "geofence": "van_tracker_site_visits_2025.csv",
    "vans": "technician_vans_2025.csv",
}
