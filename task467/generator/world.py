"""The world of task467: Velmont International Airport, the Velmont Airport Authority's per-trip taxi pickup fee, the
City of Velmont Vehicle-for-Hire Office's taxi trip records, Velmont Transit's Airport Line and the temporary taxi rank
the forecourt reconstruction put on the parkade road from 4 November 2024 to the end of 2026."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 467
TZ = ZoneInfo("America/Toronto")
UTC = dt.timezone.utc

# ---------------------------------------------------------------- dates
FIRST_DAY = dt.date(2023, 1, 1)
LAST_DAY = dt.date(2026, 8, 31)            # the August 2026 drop, published 2 October 2026
CHANGE = dt.date(2024, 11, 4)              # the Airport Line opens; taxis move to the temporary rank
RETURN = dt.date(2027, 1, 1)               # the forecourt rank reopens
AS_OF = "2026-10-16"                       # the finance manager's memo; the folder assembled
BASE_YEAR, BUDGET_YEAR = 2025, 2027
FILE_2024_BUILT = dt.date(2025, 2, 3)      # the Office's annual files, built after each year closed
FILE_2025_BUILT = dt.date(2026, 2, 6)
UTC_FROM = dt.date(2026, 1, 1)             # meter firmware 8.1: meter times in UTC from the January 2026 drop
FEE_COL_RENAMED = (2026, 6)                # the June 2026 drop writes the fee column as Airport_Fee

# ---------------------------------------------------------------- the fee
FEES = {2019: 4.50, 2020: 4.50, 2021: 4.75, 2022: 5.00, 2023: 5.25, 2024: 5.50, 2025: 5.75, 2026: 6.75}
FEE_STEP = 0.25
MENU = [5.50 + 0.25 * i for i in range(8)]  # the settings the memo tables, $5.50 to $7.25

# ---------------------------------------------------------------- the city's taxi zones (the Office's zone map)
# (id, name, district, km from the airport by road)
ZONES = [
    (1, "Velmont International Airport", "Airport", 0.0),
    (2, "Commerce Park", "Airport", 5.8),
    (3, "Airport Industrial", "Airport", 4.1),
    (4, "Westbrook", "West", 9.6),
    (5, "Fairview", "West", 11.2),
    (6, "Elmdale", "West", 13.9),
    (7, "Hillcrest", "West", 15.3),
    (8, "Riverside West", "West", 16.8),
    (9, "Kingsway", "North", 12.4),
    (10, "Orchard Heights", "North", 18.7),
    (11, "Bayview", "North", 22.5),
    (12, "Glenmore", "North", 20.1),
    (13, "Lakeshore", "South", 24.6),
    (14, "University", "Central", 13.2),
    (15, "Parkhurst", "Central", 15.8),
    (16, "Stonebridge", "South", 19.4),
    (17, "Maplewood", "East", 23.7),
    (18, "Cedar Grove", "East", 26.9),
    (19, "Northfield", "North", 25.3),
    (20, "Eastview", "East", 21.8),
    (21, "Midtown", "Central", 16.6),
    (22, "Old Town", "Central", 19.9),
    (23, "Harbourfront", "Central", 21.4),
    (24, "Downtown Central", "Central", 20.3),
    (25, "Market District", "Central", 19.1),
    (26, "Wexley", "South", 17.2),
    (27, "Briarwood", "South", 28.4),
    (28, "Ashford", "East", 30.2),
    (29, "Thornhill Park", "North", 27.6),
    (30, "Sandpoint", "South", 31.8),
    (31, "Greystone", "East", 33.5),
    (32, "Millbrook", "West", 26.1),
    (33, "Ridgeview", "West", 29.7),
    (34, "Beacon Hill", "South", 22.9),
    (35, "Pinecrest", "North", 34.6),
    (36, "Foxborough", "East", 37.2),
    (37, "Kettle Creek", "West", 38.9),
    (38, "Outside Velmont", "Outside", 45.0),
]
ZONE = {z: (name, district, km) for z, name, district, km in ZONES}
AIRPORT = 1
# the Airport Line's city stations and the zones they stand in (the bulletin names stations; the zone file names zones)
STATIONS = {"Commerce Park": 2, "University": 14, "Midtown": 21, "Central": 24}
STATION_ZONES = sorted(STATIONS.values())
CITY_ZONES = [z for z, *_ in ZONES if z != AIRPORT]
OTHER_ZONES = [z for z in CITY_ZONES if z not in STATION_ZONES]

# ---------------------------------------------------------------- the travel the trips come from (the clean truth)
P_DAY = 261.0          # taxi pickups at the airport a day, at the July 2024 level, before the change
D_DAY = 261.0 * 214 / 262   # taxi drop-offs at the airport a day
GROWTH = 0.030         # a year, both directions (passenger traffic)
SEAS = [0.90, 0.86, 1.00, 1.01, 1.00, 1.04, 1.12, 1.10, 1.00, 1.01, 0.94, 1.02]
DOW_P = [1.06, 0.95, 0.93, 1.02, 1.07, 0.88, 1.09]     # Monday to Sunday, pickups (arrivals)
DOW_D = [1.08, 0.97, 0.95, 1.04, 1.10, 0.86, 1.00]     # drop-offs (departures)
# the month's lean toward arrivals (+) or departures (-): returns after the holidays, March break and August,
# departures before them; pickups carry it, drop-offs the opposite, the same each year (it nets to nothing over
# January to October and over November and December)
TILT = [0.020, 0.000, 0.010, -0.005, -0.010, -0.020, -0.005, 0.020, 0.000, -0.010, 0.015, -0.015]
STATION_SHARE_P = 0.43  # the share of pickups bound for the line's station zones
STATION_SHARE_D = 0.62  # the share of drop-offs coming from them
# within the station zones: Central, Midtown, University, Commerce Park
STATION_SPLIT_P = {24: 0.48, 21: 0.21, 14: 0.12, 2: 0.19}
STATION_SPLIT_D = {24: 0.50, 21: 0.19, 14: 0.09, 2: 0.22}
LINE = 0.662           # taxi trips to and from a station zone once the Airport Line runs, both directions
RANK = 0.890           # taxi pickups while taxis load at the temporary rank
VOID_RATE = 0.0035     # voided trips (a reversal row beside the original), both directions
LATE_RATE = 0.012      # store-and-forward trips sent days late
RESEND_RATE = 0.040    # Corvane meters: trips re-sent after a dropped connection

# ---------------------------------------------------------------- organisations, people, files
CITY = "Velmont"
AUTHORITY = "Velmont Airport Authority"
AIRPORT_NAME = "Velmont International Airport"
OFFICE = "City of Velmont Vehicle-for-Hire Office"
TRANSIT = "Velmont Transit"
LINE_NAME = "Airport Line"
BYLAW = "Ground Transportation Fees By-law GT-3"
POLICY = "Finance Policy FP-07"
NOTICE = "Ground Transportation Notice GT-2024-11"
PEOPLE = {"finance": "Olivia White", "director": "Joseph Heath", "opendata": "Johnny Houston"}
TITLES = {"finance": "Manager, Ground Transportation Finance, Velmont Airport Authority",
          "director": "Director, Ground Transportation, Velmont Airport Authority",
          "opendata": "Open Data Coordinator, City of Velmont Vehicle-for-Hire Office"}
BROKERAGES = {1: "Kestrel Cabs", 2: "Northgate Taxi", 3: "Lakeside Cabs", 4: "Velmont City Cab",
              5: "Harbour Taxi", 6: "Westbrook Taxi"}
VENDORS = {1: "Orlan Metering", 2: "Corvane Systems"}

FILES = {
    "trips2024": "vfh_taxi_trips_airport_2024.parquet",
    "trips2025": "vfh_taxi_trips_airport_2025.parquet",
    **{"drop%02d" % m: "vfh_taxi_trips_airport_2026-%02d.parquet" % m for m in range(1, 9)},
    "archive": "vfh_od_daily_archive_2023.csv",
    "zones": "vfh_taxi_zones.csv",
    "brokerages": "vfh_brokerages.csv",
    "affiliations": "vfh_vehicle_affiliations.csv",
    "dictionary": "vfh_trip_records_data_dictionary.pdf",
    "bylaw": "vaa_ground_transportation_fees_bylaw_gt3.pdf",
    "policy": "vaa_finance_policy_fp07_user_fee_revenue.pdf",
    "budget": "vaa_2027_ground_transportation_budget.xlsx",
    "notice": "vaa_notice_gt-2024-11_temporary_taxi_rank.pdf",
    "bulletin": "velmont_transit_airport_line_service_bulletin.pdf",
    "passengers": "vaa_passenger_statistics_2023_2026.xlsx",
    "survey": "vaa_ground_access_survey_2023.pdf",
    "index": "folder_contents.csv",
}
DROP_KEYS = ["drop%02d" % m for m in range(1, 9)]
GOLDEN = {"memo": "velmont_2027_taxi_pickup_fee.docx", "ledger": "velmont_taxi_fee_ledger_2025_2026.csv"}
DISTRACTORS = ["passengers", "survey"]
AMOUNT_2027 = 535027.00     # the 2027 budget's amount assigned to the taxi pickup fee (the 2027 budget workbook, line 12)


def fee(d):
    """The scheduled fee on a trip begun on date d."""
    return FEES[d.year]


def month_key(d):
    return (d.year, d.month)


def months(a=FIRST_DAY, b=LAST_DAY):
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        y, m = (y + (m == 12), m % 12 + 1)
    return out
