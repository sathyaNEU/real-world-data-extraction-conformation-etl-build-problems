"""task308 constants: a regional bike-share operator's six station networks in 2025, the 2025 e-bike pilot on the
Harbour network, the 2027 deployment the board decides, and the seeds."""
import datetime as dt
from zoneinfo import ZoneInfo

ORG = "Brackenford Bikeshare Inc."
ORG_SHORT = "Brackenford Bikeshare"
CITY = "Brackenford"
VENDOR = "Harlan Velo Supply Co."
TZ = ZoneInfo("America/Chicago")
YEAR = 2025
AS_OF = dt.date(2026, 11, 6)                      # the board paper's working folder
BOARD_DATE = dt.date(2026, 12, 9)

SEED_WORLD = 3109        # requests, durations, destinations: the scratch scan's seed (t308/v2 pick.py)
SEED_VANS = 31091        # van run start times and the spacing of moves within a run
SEED_FALSE = 31092       # false starts
SEED_SHOP = 31093        # faults, repairs, road tests
SEED_PEOPLE = 31094      # riders, accounts, cards, home ZIP codes
SEED_CHARGE = 31095      # charging point registers, controller restarts
SEED_DOCS = 31096        # station names, coordinates, capacities, 2024 trips, open data

# networks: code -> (name, [(role, stations)])
NETWORKS = {"CEN": ("Central", [("edge", 11), ("core", 13)]),
            "UNI": ("University", [("dorm", 2), ("class", 3)]),
            "RIV": ("Riverside", [("water", 26)]),
            "OLD": ("Old Town", [("town", 12)]),
            "HIL": ("Hillcrest", [("top", 6), ("bottom", 6)]),
            "HBR": ("Harbour", [("quay", 36)])}
CANDIDATES = ["CEN", "UNI", "RIV", "OLD", "HIL"]
TARGET = {"CEN": 12, "UNI": 16, "RIV": 7, "OLD": 6, "HIL": 7, "HBR": 10}     # classic bikes a station after the night run
VANRUNS = {"CEN": (6, 10, 14, 18), "UNI": (6, 14), "RIV": (6, 14), "OLD": (6, 14), "HIL": (6, 14), "HBR": (6, 14)}
SCALE = {("UNI", "dorm"): 4.5, ("UNI", "class"): 3.75, "CEN": 1.0, "RIV": 1.0, "OLD": 1.0, "HIL": 1.0, "HBR": 0.7}
MONTH = [0.55, 0.6, 0.75, 0.9, 1.0, 1.1, 1.15, 1.1, 1.0, 0.9, 0.7, 0.55]
TERM = {1, 2, 3, 4, 9, 10, 11, 12}               # months the university teaches

# the pilot
PILOT_N, MATCHED_N = 24, 12
EB_PILOT = 8                                      # e-bikes a pilot station after the night restock (about 02:40)
POINTS = 14                                       # charging points a pilot station
SWITCH, INDUCE, SPEED = 0.42, 0.04, 0.74
EB_SPARES, CL_SPARES = 20, 60

# fares (USD), billed per started minute; rides under 60 seconds are false starts and are not charged
UNLOCK, PER_MIN_CLASSIC, PER_MIN_EBIKE = 1.00, 0.12, 0.17

# e-bike battery and charging
BATTERY_WH, USE_WH_MIN, CHARGE_WH_MIN, CHARGE_EFF = 500.0, 7.5, 4.0, 0.88

# the workshop
FAULT = {"classic": 0.0010, "ebike": 0.0030}
RETEST = 0.12                                     # repaired bikes failing the road test, booked as a new job
INTERMITTENT = 0.30                               # faults that come back after a few rides

DEPLOY_EBIKES = 300

PEOPLE = {"lead": "Joseph Graham", "ops": "Gina Wells"}

FILES = {"q1": "tripsys_export_2025Q1.csv", "q2": "tripsys_export_2025Q2.csv",
         "q3": "rides_2025Q3.csv", "q4": "rides_2025Q4.csv",
         "moves": "dispatch_moves_2025.csv", "audit": "audit_0300_2025.xlsx",
         "stations": "station_information.json", "regions": "system_regions.json",
         "accounts": "account_register_2025-12-31.csv",
         "charging": "charging_sessions_harbour_2025.csv", "workshop": "workshop_jobs_2025.csv",
         "board": "board_paper_2026-12_item7_extract.pdf", "pilot": "ebike_pilot_harbour_2025.pdf",
         "fares": "fare_schedule_2025.pdf", "dictionary": "data_dictionary.xlsx",
         "opendata": "open_data_bikeshare_trips_by_area_2025.csv", "quote": "vendor_quote_ebikes_2026.pdf"}
AREA_NAME = {"CEN": "Central", "UNI": "University", "RIV": "Riverside", "OLD": "Old Town", "HIL": "Hillcrest",
             "HBR": "Harbour", "OUT": "Outside Brackenford"}
