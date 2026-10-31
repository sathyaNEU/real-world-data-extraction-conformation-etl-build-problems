"""The fixed facts of the Tamarack County world: the municipalities and their building history, the census dates,
the post offices, the group quarters, the people and the file names."""
import datetime as dt

SEED = 4803
STATE_FIPS, COUNTY_FIPS = "57", "041"
COUNTY = "Tamarack County"
CENTER = "State Data Center"
OFFICE = "Office of the State Demographer"
DEPT = "Department of Administration"
DOT = "Department of Transportation"
PEOPLE = {"demographer": ("Laura Rubio", "State Demographer"),
          "estimates": ("Chad Neal", "Population Estimates Program Manager")}

C2000, C2010, C2020 = dt.date(2000, 4, 1), dt.date(2010, 4, 1), dt.date(2020, 4, 1)
EST = dt.date(2026, 7, 1)
ROLL = dt.date(2026, 1, 1)                  # the assessor's roll date
CO_FROM, CO_TO = dt.date(2020, 1, 1), dt.date(2026, 6, 30)
VITAL_FROM, VITAL_TO = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
EDRS_SWITCH = dt.date(2026, 1, 1)           # the death registration system's new release, coding residence by address
LINE = 10000

# persons in a dwelling's household by its type and age in years: a household life cycle shared by every type
BASE = {"SF": 2.12, "TH": 1.86, "AP": 1.52, "MH": 2.05}
LIFT, TAU, HUMP = 0.92, 12.0, 1 / 7.0
OCC = {"SF": 0.962, "TH": 0.952, "AP": 0.930, "MH": 0.900}

# code, name, kind, postal service (share of the stock by post office), eras (first year, last year, units a year,
# main type), the 2026 scale of each era
MUNIS = [
    ("21400", "City of Dunmore", "city", [(1890, 1950, 85, "SF"), (1950, 1972, 70, "AP"), (1985, 2004, 38, "AP"), (2015, 2025, 22, "AP")]),
    ("39050", "City of Juniper", "city", [(1890, 1955, 78, "SF"), (1955, 1978, 62, "AP"), (2006, 2026, 28, "AP")]),
    ("13200", "Town of Cedar Run", "town", [(1955, 1978, 70, "SF"), (1985, 1998, 66, "SF"), (2019, 2026, 232, "SF")]),
    ("49875", "Town of Maple Ford", "town", [(1960, 1980, 25, "SF"), (1997, 2011, 203, "SF"), (2011, 2015, 55, "TH")]),
    ("03450", "Town of Ashgrove", "town", [(1955, 1975, 32, "SF"), (1990, 2008, 45, "SF"), (2014, 2026, 70, "SF")]),
    ("04875", "Village of Barrow", "village", [(1890, 1960, 20, "SF"), (1960, 1990, 26, "SF"), (2000, 2012, 22, "TH")]),
    ("23800", "Town of Elk Prairie", "town", [(1965, 1990, 32, "SF"), (2001, 2012, 62, "SF")]),
    ("25600", "Village of Fallon", "village", [(1910, 1960, 40, "SF"), (1966, 1983, 50, "AP"), (1984, 2003, 80, "SF"), (2005, 2012, 28, "TH")]),
    ("29975", "Town of Glenmoor", "town", [(1972, 1995, 40, "SF"), (2008, 2018, 60, "SF"), (2020, 2026, 55, "TH")]),
    ("33100", "Town of Harwick", "town", [(1958, 1980, 46, "SF"), (1998, 2010, 72, "SF"), (2018, 2026, 135, "SF")]),
    ("37600", "Village of Ivydale", "village", [(1905, 1960, 30, "SF"), (1988, 2002, 48, "SF")]),
    ("40150", "Town of Kessler", "town", [(1978, 2000, 62, "SF"), (2000, 2010, 92, "SF")]),
    ("46225", "Village of Lorne", "village", [(1925, 1970, 26, "SF"), (1975, 1995, 30, "MH")]),
    ("57650", "Town of Northfield", "town", [(1968, 1990, 40, "SF"), (2011, 2026, 70, "SF")]),
]
SCALE = {"Town of Cedar Run": {0: 1.115, 1: 1.115, 2: 1.2}, "Town of Maple Ford": {"all": 1.095}, "Village of Fallon": {1: 1.3}}
CODE = {m[1]: m[0] for m in MUNIS}
NAME = {m[0]: m[1] for m in MUNIS}
SHORT = {m[1]: m[1].split(" of ", 1)[1] for m in MUNIS}

# the Ivydale consolidation of 1 January 2024: the Village of Ivydale's 1988 to 2002 era stood in the Town of Ivydale
IVY_TOWN = ("37625", "Town of Ivydale")
CONSOLIDATION = dt.date(2024, 1, 1)
# annexations: (effective date, from, to, era of the losing municipality, dwellings moved)
ANNEX = [(dt.date(2006, 9, 1), "Town of Kessler", "City of Juniper", 0, 64),
         (dt.date(2016, 5, 1), "Town of Maple Ford", "City of Dunmore", 0, 38),
         (dt.date(2021, 3, 1), "Town of Harwick", "City of Juniper", 0, 21)]

# post offices: postal city, ZIP
POST = {"DUNMORE": ["54701", "54703"], "JUNIPER": ["54720"], "FALLON": ["54735"], "BARROW": ["54741"],
        "LORNE": ["54750"], "IVYDALE": ["54762"], "CEDAR RUN": ["54728"]}
# each municipality's stock by era: the post office that serves it
POSTAL = {
    "City of Dunmore": ["DUNMORE"] * 4, "City of Juniper": ["JUNIPER"] * 3,
    "Town of Cedar Run": ["CEDAR RUN", "CEDAR RUN", "DUNMORE"], "Town of Maple Ford": ["JUNIPER", "DUNMORE", "DUNMORE"],
    "Town of Ashgrove": ["JUNIPER", "JUNIPER", "JUNIPER"], "Village of Barrow": ["BARROW"] * 3,
    "Town of Elk Prairie": ["FALLON", "FALLON"], "Village of Fallon": ["FALLON"] * 4,
    "Town of Glenmoor": ["BARROW", "DUNMORE", "DUNMORE"], "Town of Harwick": ["JUNIPER", "JUNIPER", "FALLON"],
    "Village of Ivydale": ["IVYDALE", "IVYDALE"], "Town of Kessler": ["JUNIPER", "IVYDALE"],
    "Village of Lorne": ["LORNE", "LORNE"], "Town of Northfield": ["LORNE", "LORNE"]}

# group quarters: facility, type, municipality, era whose streets hold it, residents at the 2000, 2010 and 2020 censuses
# and on the Center's 2026 survey
GQ = [
    ("Tamarack County Health Care Center", "Nursing facility", "City of Dunmore", 1, (176, 171, 168, 162)),
    ("Riverbend Rehabilitation and Nursing", "Nursing facility", "City of Dunmore", 2, (0, 118, 124, 121)),
    ("Tamarack County Jail", "Correctional facility for adults", "City of Dunmore", 0, (74, 88, 96, 92)),
    ("Northside Group Home", "Group home", "City of Dunmore", 0, (8, 8, 8, 7)),
    ("Juniper State University: Halverson Hall", "College residence hall", "City of Juniper", 1, (308, 312, 312, 309)),
    ("Juniper State University: Okafor Hall", "College residence hall", "City of Juniper", 1, (0, 0, 284, 281)),
    ("Juniper State University: North Quad", "College residence hall", "City of Juniper", 1, (342, 356, 356, 352)),
    ("Juniper State University: Pine Court", "College residence hall", "City of Juniper", 2, (0, 198, 198, 196)),
    ("Juniper Lutheran Home", "Nursing facility", "City of Juniper", 0, (104, 99, 96, 94)),
    ("Barrow Manor", "Nursing facility", "Village of Barrow", 1, (150, 155, 158, 154)),
    ("Fallon Care Center", "Nursing facility", "Village of Fallon", 2, (98, 96, 94, 91)),
    ("Brightwater Group Home", "Group home", "Town of Harwick", 1, (0, 6, 6, 6)),
]

FILES = {
    "roll": "tamarack_real_property_roll_2026.csv",
    "cos": "certificates_of_occupancy_2020-01_2026-06.csv",
    "demo": "demolition_permits_2000-2026.csv",
    "bg2020": "census2020_dhc_tamarack_block_groups.csv",
    "history": "decennial_census_tamarack_municipalities_2000-2020.xlsx",
    "boundary": "municipal_boundary_changes_since_2000.csv",
    "gq": "group_quarters_survey_2026.xlsx",
    "points": "tamarack_address_points_2026-07.csv",
    "births": "births_tamarack_residents_2025-2026.csv",
    "deaths": "deaths_tamarack_residents_2025-2026.csv",
    "act": "municipal_road_aid_act_excerpt.pdf",
    "method": "municipal_estimates_program_statement_2026.pdf",
    "roads": "dot_certified_local_road_miles_2026.xlsx",
    "vintage": "census_bureau_county_estimates_v2025.csv",
}
DISTRACTORS = ("roads", "vintage")
