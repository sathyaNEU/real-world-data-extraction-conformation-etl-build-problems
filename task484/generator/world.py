"""The fixed world: a state's population unit, the twelve cities nearest the 50,000 line of the 2027 revenue-sharing
formula, their housing since the 2020 census, the apartment buildings completed since and how they fill after
opening, and the utility whose account history covers five of the cities. Every other module reads its parameters
from here."""
import datetime as dt

OFFICE = "State Office of Financial Planning, Population and Demographics Unit"
UTILITY = "Northern Valley Power"
PEOPLE = {"analyst": ("Kimberly Rogers", "Senior Demographer"),
          "director": ("Martin Booth", "State Demographer")}
SEED = 4840
CENSUS = dt.date(2020, 4, 1)
EST = dt.date(2026, 4, 1)                                  # the estimate date
LINE = 50000                                               # residents; at or above moves a city to the upper tier
RULES_DATE = "17 February 2026"
MEMO_DATE = "23 October 2026"

# cities: 2020 census housing units, stock occupancy (2020), persons per household (2020), group quarters residents,
# permit system, covered by the utility, multifamily units completed per year 2020-2026 (2020 from April, 2026 to
# March), single-family units completed per year
CITIES = {
    "Ashford":       (15647, .946, 2.41, 820, "metro", True, (120, 260, 480, 820, 1480, 1720, 380), (210, 260, 240, 230, 220, 200, 40)),
    "Bellmont":      (19582, .951, 2.33, 410, "metro", False, (60, 180, 240, 320, 380, 420, 90), (160, 210, 190, 170, 150, 160, 30)),
    "Carver Springs": (13827, .938, 2.47, 1450, "county", False, (90, 210, 420, 960, 1640, 1980, 430), (300, 340, 310, 280, 260, 250, 50)),
    "Dunmore":       (20716, .957, 2.29, 300, "county", True, (40, 90, 110, 160, 210, 240, 50), (140, 170, 160, 150, 140, 130, 30)),
    "Eastlake":      (15123, .949, 2.45, 600, "metro", False, (150, 330, 520, 760, 1330, 1560, 340), (260, 290, 270, 250, 240, 220, 45)),
    "Fairhaven":     (21390, .953, 2.31, 980, "civic", True, (70, 140, 200, 260, 330, 360, 80), (120, 150, 140, 130, 120, 110, 25)),
    "Glenridge":     (19218, .944, 2.39, 540, "civic", False, (50, 120, 160, 220, 260, 280, 60), (180, 220, 200, 190, 170, 160, 35)),
    "Harlow":        (15564, .942, 2.51, 1210, "county", True, (110, 240, 380, 640, 1060, 1210, 260), (240, 280, 260, 250, 230, 220, 45)),
    "Ironwood":      (21140, .955, 2.26, 350, "civic", False, (30, 70, 90, 130, 160, 170, 40), (110, 130, 120, 110, 100, 95, 20)),
    "Juniper Falls": (14151, .941, 2.52, 700, "county", False, (130, 290, 470, 880, 1520, 1840, 410), (280, 320, 300, 280, 260, 240, 50)),
    "Kestrel Bay":   (18990, .948, 2.36, 460, "metro", False, (80, 160, 230, 300, 360, 390, 85), (170, 200, 180, 170, 160, 150, 30)),
    "Linden":        (19369, .950, 2.40, 520, "civic", True, (90, 200, 300, 420, 560, 620, 130), (190, 230, 210, 200, 180, 170, 35)),
}
# the golden population each city is tuned to (tune.py scales each city's 2020 housing units)
DESIRED = {"Ashford": 49270, "Bellmont": 48910, "Carver Springs": 48830, "Dunmore": 49180, "Eastlake": 48620,
           "Fairhaven": 52310, "Glenridge": 48690, "Harlow": 49030, "Ironwood": 48470, "Juniper Falls": 48740,
           "Kestrel Bay": 48390, "Linden": 51630}
# how an apartment building fills after its certificate of occupancy: months to fill about 63 per cent of its units,
# and the share occupied once it has filled
FILL_MONTHS = (5.5, 10.5)
FILL_LEVEL = (.925, .965)
SF_FILL_MONTHS = 1.2

FILES = {
    "census": "census_2020_city_housing_base.xlsx",
    "acs": "acs_2020_2024_city_occupancy.xlsx",
    "metro": "metro_permits_export.csv",
    "county": "county_building_permits.xlsx",
    "civic": "civic_permit_records.csv",
    "demo": "demolition_permits_2020_2026.csv",
    "gq": "group_quarters_survey_2026.csv",
    "utility": "nvp_residential_accounts_monthly.csv",
    "codes": "building_type_code_table.xlsx",
    "rules": "revenue_sharing_tier_rules_2027.pdf",
    "notes": "data_notes.txt",
    "schools": "school_enrollment_oct2025.csv",
    "voters": "voter_registration_by_city_2026.csv",
}
GOLDEN = {"workbook": "city_population_estimates_2026.xlsx", "memo": "revenue_sharing_tiers_2027.pdf"}
