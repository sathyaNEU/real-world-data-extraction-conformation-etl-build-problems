"""task481 world: the City of Ellsmere, an unnamed US state, its police department's move from summary crime returns
(SRS Return A) to incident-based reporting (NIBRS), and the University of Ellsmere's Public Safety Lab, which writes the
crime chapter of the city's Public Safety Scorecard under a data-sharing agreement with the department.

The department's new records system went live at local midnight on 1 October 2024. For October to December 2024 the
Records Division kept producing the monthly Return A from it, so every victim reported in those three months carries both
the Return A line the clerks scored it under and its NIBRS offense; from 1 January 2025 the state program takes NIBRS
only. The scorecard's 2026 edition reports aggravated assault as NIBRS offense 13A, one offense per victim, by the month
the offense was reported, and restates 2024 as NIBRS would have counted it.

Assaults come in kinds the two systems treat differently. NIBRS counts as aggravated every assault with a weapon or force
(strangulation is weapon/force 85, asphyxiation) or with a serious injury, and every assault victim in an incident the
summary returns scored as a robbery or a homicide. The department's legacy practice scored strangulation and most
domestic assaults without a weapon as simple assaults (line 4e), and scored a share of hands-and-feet assaults with minor
injuries as aggravated (line 4d). Domestic assaults are steady through the year with a holiday rise; street assaults
swell in spring and summer and fall away in winter, so domestic assaults are a far larger share of simple assaults in
October to December than in January to September."""
import datetime as dt
import zoneinfo

SEED = 500
TZ = zoneinfo.ZoneInfo("America/Chicago")
CITY = "Ellsmere"
DEPT = "Ellsmere Police Department"
LAB = "University of Ellsmere Public Safety Lab"
STATE_PROGRAM = "State UCR Program"
PEOPLE = {"lab": "Darlene Ford",          # director of the city partnership, the Lab
          "records": "Steven Barnett"}    # NIBRS coordinator, Records Division

GO_LIVE = dt.date(2024, 10, 1)            # new records system, local midnight
DUAL_FIRST, DUAL_LAST = dt.date(2024, 10, 1), dt.date(2024, 12, 31)
NIBRS_ONLY = dt.date(2025, 1, 1)
EXTRACT_LAST = dt.date(2026, 9, 30)       # incidents reported to the end of September 2026
EXTRACT_RUN = dt.datetime(2026, 10, 5, 7, 42, 13)
FIRST_YEAR = 2021                         # Return A workbooks from 2021
SIM_FIRST = dt.date(2021, 1, 1)

# Seasonal factors by calendar month (Jan..Dec). Street assaults follow the warm months; domestic assaults are steady
# with a rise over the holidays; robbery peaks in the dark months.
STREET = [0.75, 0.77, 0.92, 1.02, 1.14, 1.26, 1.34, 1.29, 1.11, 0.98, 0.80, 0.70]
DV = [0.98, 0.95, 0.98, 1.00, 1.02, 1.05, 1.07, 1.05, 1.00, 0.98, 1.06, 1.18]
ROB = [1.05, 0.95, 0.95, 0.95, 1.00, 1.00, 1.02, 1.00, 0.98, 1.02, 1.05, 1.12]
HOM = [0.85, 0.80, 0.90, 0.95, 1.05, 1.15, 1.25, 1.20, 1.05, 0.95, 0.90, 0.95]

# Expected victims a month at seasonal factor 1 in 2024. Street kinds scale with STREET, domestic with DV.
BASE = {
    "fire_hit": 34.0,      # street firearm assault, victim struck
    "fire_miss": 84.0,     # street firearm assault, shot at or threatened with a gun, not struck
    "knife": 47.0,
    "other_weapon": 61.0,
    "pw_serious": 41.0,    # hands, fists, feet; serious injury
    "pw_minor": 1080.0,    # hands, fists, feet; minor or no injury
    "threat": 225.0,       # intimidation
    "dv_weapon": 31.0,
    "dv_serious": 16.0,
    "dv_strang": 110.0,    # strangulation, weapon/force 85, no other weapon, injury minor or none
    "dv_minor": 380.0,
    "dv_threat": 82.0,
    "robbery": 172.0,      # robbery incidents
    "homicide": 5.2,       # homicide incidents
}
STREET_KINDS = ("fire_hit", "fire_miss", "knife", "other_weapon", "pw_serious", "pw_minor", "threat")
DV_KINDS = ("dv_weapon", "dv_serious", "dv_strang", "dv_minor", "dv_threat")
# How strongly each street kind follows the street season (1 = fully).
SEASON_POWER = {"fire_hit": 0.75, "fire_miss": 0.75, "knife": 0.6, "other_weapon": 0.7, "pw_serious": 1.0,
                "pw_minor": 1.0, "threat": 1.0}

# Year levels relative to 2024 (street, domestic, robbery, homicide); the 2025 street rise is in the warm months.
LEVEL = {
    2021: {"street": 1.02, "fire": 1.18, "dv": 1.05, "rob": 1.12, "hom": 1.30},
    2022: {"street": 1.00, "fire": 1.12, "dv": 1.03, "rob": 1.08, "hom": 1.20},
    2023: {"street": 0.99, "fire": 1.05, "dv": 1.01, "rob": 1.04, "hom": 1.08},
    2024: {"street": 1.00, "fire": 1.00, "dv": 1.00, "rob": 1.00, "hom": 1.00},
    2025: {"street": 1.00, "fire": 0.98, "dv": 1.00, "rob": 0.92, "hom": 0.88},
    2026: {"street": 1.02, "fire": 0.91, "dv": 0.98, "rob": 0.90, "hom": 0.85},
}
WARM_2025 = [1.00, 1.00, 1.024, 1.061, 1.122, 1.183, 1.22, 1.196, 1.122, 1.037, 1.00, 0.988]   # 2025 street, by month

# Legacy (Return A) scoring of each kind: line shares. NIBRS: 13A for weapons, force 85 and serious injury; 13B minor;
# 13C intimidation. The two minor kinds are scored 4d at the same rate within 4d's mix, so 4d converts alike for
# domestic and street victims.
LEGACY = {
    "fire_hit": {"4A": 1.0}, "fire_miss": {"4A": 1.0}, "knife": {"4B": 1.0}, "other_weapon": {"4C": 1.0},
    "pw_serious": {"4D": 0.90, "4E": 0.10},
    "pw_minor": {"4D": 0.065, "4E": 0.935},
    "threat": {"4E": 1.0},
    "dv_weapon": {"4A": 0.40, "4B": 0.35, "4C": 0.25},
    "dv_serious": {"4D": 0.90, "4E": 0.10},
    "dv_strang": {"4D": 0.04, "4E": 0.96},
    "dv_minor": {"4D": 0.0941, "4E": 0.9059},
    "dv_threat": {"4E": 1.0},
}
NIBRS = {"fire_hit": "13A", "fire_miss": "13A", "knife": "13A", "other_weapon": "13A", "pw_serious": "13A",
         "pw_minor": "13B", "threat": "13C", "dv_weapon": "13A", "dv_serious": "13A", "dv_strang": "13A",
         "dv_minor": "13B", "dv_threat": "13C"}
ROB_EXTRA = 0.08          # robbery incidents with an assault victim besides the robbery
HOM_EXTRA = 0.30          # homicide incidents with a wounded victim besides the dead

DV_RELATIONSHIPS = ("SE", "CS", "PA", "SB", "CH", "GP", "GC", "IL", "SP", "SC", "SS", "OF", "BG", "XS", "XR", "CF")
OTHER_RELATIONSHIPS = ("AQ", "FR", "NE", "OK", "ST", "RU", "EE", "ER")


def season(kind, month):
    m = month - 1
    if kind in DV_KINDS:
        return DV[m]
    if kind == "robbery":
        return ROB[m]
    if kind == "homicide":
        return HOM[m]
    return STREET[m] ** SEASON_POWER[kind]


def level(kind, year, month):
    lv = LEVEL[year]
    if kind in DV_KINDS:
        return lv["dv"]
    if kind == "robbery":
        return lv["rob"]
    if kind == "homicide":
        return lv["hom"]
    base = lv["fire"] if kind.startswith("fire") else lv["street"]
    if year == 2025:
        base *= WARM_2025[month - 1] ** (SEASON_POWER[kind] if not kind.startswith("fire") else 0.3)
    return base


def expected(kind, year, month):
    return BASE[kind] * season(kind, month) * level(kind, year, month)


def local(dt_utc):
    return dt_utc.astimezone(TZ)
