"""Constants for task273: the Stonereach Valley Regional Transportation Commission's Commercial Fleet Safety
Programme. Every name, date and parameter the world, the records, the documents and the analysis share lives here."""
import datetime as dt

SEED = 18
YEARS = (2021, 2022, 2023, 2024, 2025)
FORM_V2 = dt.date(2023, 1, 1)               # the state crash report's second version, crashes from this date
THRESHOLD = 1.5                             # the coverage rule: at least 1.5 times private drivers' rate per mile
VOTE = dt.date(2026, 12, 9)
START = dt.date(2027, 7, 1)
ASSEMBLED = dt.datetime(2026, 11, 16, 15, 20, 0)
TZ = "America/Los_Angeles"

REGION = "Stonereach Valley"
COMMISSION = "Stonereach Valley Regional Transportation Commission"
COMMISSION_SHORT = "the Commission"
PROGRAMME = "Commercial Fleet Safety Programme"
COUNTY = "Stonereach County"
CITY_A = "Kelderwick"
CITY_B = "Fairhollow"
REQUESTER = "Thomas Moyer"                  # policy adviser
OWNER = "Amanda Barrera"                    # director of safety programmes
DOT = "Department of Transportation"
COMPANY = COMMISSION

# the seven commercial uses the coverage rule names, in the rule's order: (code, rule name, short label)
USES = [
    ("TX", "Taxicabs", "Taxi"),
    ("RH", "Ride-hail vehicles (transportation network companies)", "Ride-hail"),
    ("LM", "Limousines and chauffeured cars", "Limousine"),
    ("AS", "Airport and hotel shuttles", "Airport shuttle"),
    ("PT", "Paratransit and non-emergency medical transport", "Paratransit"),
    ("PD", "Parcel and courier delivery vans", "Parcel delivery"),
    ("AD", "App-based delivery (delivery network company couriers)", "App delivery"),
]
CODES = [u[0] for u in USES]
RULE_NAME = {u[0]: u[1] for u in USES}
LABEL = {u[0]: u[2] for u in USES}

# the report's form codes for a vehicle's use. Version 1 (crashes to 31 December 2022) and version 2 (from 1 January
# 2023). Version 1 has one code for every passenger service for hire and one for every delivery; the operator's name
# on the report says which.
USE_V2 = {"PV": "00", "TX": "11", "RH": "12", "LM": "13", "AS": "14", "PT": "15", "PD": "21", "AD": "22",
          "OC": "30", "TB": "41", "SB": "42", "GV": "50", "EM": "60", "UNK": "99"}
USE_V1 = {"PV": "0", "TX": "1", "RH": "1", "LM": "1", "AS": "1", "PT": "1", "PD": "2", "AD": "2",
          "OC": "3", "TB": "4", "SB": "4", "GV": "5", "EM": "6", "UNK": "9"}
PRIVATE_BODIES = ("PC", "SUV", "PU", "VAN")   # private drivers: these bodies in personal use (the rule)

# road classes: the state's functional system (1 to 7) in urban and rural areas, and the factor group the
# Department's continuous count programme assigns each to
FCLASS = [
    (1, "U", "UF"), (2, "U", "UF"), (3, "U", "UA"), (4, "U", "UA"), (5, "U", "UL"), (7, "U", "UL"),
    (1, "R", "RF"), (2, "R", "RF"), (3, "R", "RA"), (4, "R", "RA"), (5, "R", "RL"), (6, "R", "RL"), (7, "R", "RL")]
GROUPS = ("UF", "UA", "UL", "RF", "RA", "RL")
GROUP_NAME = {"UF": "Urban interstates, freeways and expressways", "UA": "Urban arterials",
              "UL": "Urban collectors and local roads", "RF": "Rural interstates, freeways and expressways",
              "RA": "Rural arterials", "RL": "Rural collectors and local roads"}
GROUP_OF = {(fc, ur): g for fc, ur, g in FCLASS}

AGENCIES = {
    "SP6": "State Patrol, District 6",
    "SCSO": "Stonereach County Sheriff's Office",
    "KPD": "Kelderwick Police Department",
    "FPD": "Fairhollow Police Department",
}

# the pack, as the systems and offices that keep them name their exports
FILES = {
    "contents": "README_pack_contents.txt",
    "rule": "cfsp_coverage_rule_2026.pdf",
    "crashes": "crash_extract_2021_2025_crashes.csv",
    "units": "crash_extract_2021_2025_units.csv",
    "persons": "crash_extract_2021_2025_persons_injury_crashes.csv",
    "dictionary": "crash_extract_data_dictionary.pdf",
    "inventory": "lrs_road_inventory_2025.xlsx",
    "tmr": "travel_monitoring_report_2025.pdf",
    "atr": "ccs_hourly_volumes_2025.csv",
    "stations": "ccs_stations_2025.csv",
    "operators": "commission_operator_register_2026.xlsx",
    "platforms": "platform_vehicle_reports_2025.csv",
    "deaths": "road_fatality_register_2021_2025.csv",
    "costs": "dot_crash_unit_costs_2025.pdf",
    "registrations": "dmv_registrations_stonereach_2021_2025.xlsx",
    "weather": "noaa_daily_weather_kelderwick_2021_2025.csv",
    "workzones": "work_zone_log_2021_2025.csv",
}
DISTRACTORS = ("weather", "workzones", "registrations", "platforms")
DELIVERABLES = ("fleet_safety_programme_2027.xlsx", "fleet_safety_programme_2027.pptx")
