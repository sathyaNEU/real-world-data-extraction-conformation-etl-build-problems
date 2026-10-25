"""task303 constants: Shenmore Valley Electric's Valley district (18 feeders on six substations), its outage records
2019 to 2025, the storm crews' status records 2023 to 2025, the 2027 storm hardening plan and the seeds."""
import datetime as dt

ORG = "Shenmore Valley Electric"
DISTRICT = "Valley district"
PLANNER = "Zachary Sanders"

SEED = 154                 # the outage process (scratch p303uo/world6.py, scan6b.py seed 154)
SEED_STORM = 382           # the storm days' faults (their own stream; set so every storm figure sits mid-bin)
GROWTH = 0.0062            # customers a year (set so every call and tap figure sits mid-bin, edges2.py)
SEED_REC = 30301           # ticket numbers, who closed each legacy ticket, transformer numbers
SEED_CREW = 30302          # the storm crews, their status times, the storm desk's closing
SEED_DOCS = 30303          # the inventory's other columns and the distractors' values

SIM0 = dt.date(2014, 1, 1)         # the process runs from here so the record has a past; nothing before 2019 ships
REC0 = dt.date(2019, 1, 1)
CUTOVER = dt.date(2023, 1, 1)      # the current outage management system
END = dt.date(2026, 1, 1)
YEARS = list(range(2019, 2026))
NY = len(YEARS)
EXPORTED = dt.date(2026, 9, 18)    # the outage exports and the crew export were pulled
PLAN_ISSUED = dt.date(2026, 10, 6)
FILING_DUE = dt.date(2026, 12, 1)

# internal code: name, legacy code
SUBS = {"PLC": ("Pell Creek", "PLC"), "SRH": ("Sorrel Hill", "SRH"), "BYM": ("Byers Mill", "BYM"),
        "HLF": ("Hollow Fork", "HLF"), "KTR": ("Kettle Run", "KTR"), "WYX": ("Willow Crossing", "WLC")}

# the system's major event day thresholds (minutes of daily system SAIDI), set each year by the 2.5 beta method
TMED = {2019: 9.8, 2020: 10.3, 2021: 10.1, 2022: 11.0, 2023: 11.4, 2024: 11.9, 2025: 12.6}

# the commission's incentive and the conversion
INCENTIVE = 2.10            # USD a customer-minute a year
PREVENTED = 0.9             # nine in ten of the addressed faults on the converted backbone
COST_PER_MILE = 0.42        # USD million a backbone mile
ADDRESSED = ("tree", "wind", "animal")

LEG_CAUSE = {"tree": "TREE", "wind": "WIND", "animal": "ANML", "lightning": "LTNG", "equipment": "EQUP",
             "vehicle": "VEH", "unknown": "UNK"}
NEW_CAUSE = {"tree": "Vegetation", "wind": "Wind", "animal": "Wildlife", "lightning": "Lightning",
             "equipment": "Equipment failure", "vehicle": "Vehicle / public", "unknown": "Unknown"}
LEG_DEV = {"breaker": "CB", "recloser": "RCL", "fuse": "FUS", "transformer": "TX"}
NEW_DEV = {"breaker": "Feeder breaker", "recloser": "Line recloser", "fuse": "Fuse", "transformer": "Transformer"}

# the legacy system: tap and transformer tickets closed from the trouble crews' handhelds (the rest by the control room)
HANDHELD = 0.6
HANDHELD_STORM = 0.06        # on storm days the control room closed nearly every tap ticket itself
PBL_SPAN = 100              # the contract crews take the longer repairs

# the storm desk (current system, major event days): restored jobs closed in batches at the top of every third hour
BATCH_HOURS = (1, 4, 7, 10, 13, 16, 19, 22)
BATCH_SHARE = 0.62
BATCH_LAG = 15              # minutes: the paperwork reaches the desk at the earliest a quarter hour after the restore
TWO_CREW = 0.12             # storm jobs a first crew made safe and left for a second crew
OTHER_JOBS = 0.11           # storm jobs with no outage ticket (wires down, damage assessment)

FILES = {"legacy": "oms_interruptions_2019_2022.csv",
         "current": "oms_interruptions_2023_2025.csv",
         "crews": "storm_crew_status_2023_2025.csv",
         "meds": "major_event_days_2019_2025.csv",
         "inventory": "feeder_inventory_2026.xlsx",
         "plan": "storm_hardening_plan_2027.docx",
         "notes": "oms_export_notes.txt",
         "crew_notes": "mobile_workforce_export_notes.txt",
         "order": "commission_order_reliability_2024.pdf",
         "veg": "vegetation_work_orders_2017_2026.csv",
         "settings": "line_recloser_settings_2026.xlsx"}
