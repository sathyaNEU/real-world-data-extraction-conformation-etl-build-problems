"""task471 world: an unnamed island country's 2025 Census of Population and Dwellings, its Post-Enumeration Survey,
the vital and border statistics, and the Electoral Commission's roll on census day. The Commission shares the 150
organisers of its 2027 enrolment campaign among the 16 regions in proportion to each region's adults not on the roll:
the people aged 18 and over usually resident in the region on census day, whether or not the census counted them, less
the electors enrolled at an address in the region that day.

The census misses people and counts some in error; the survey recounts a sample of meshblocks independently of the
census and is matched to it. For everyone but one group the two counts miss people independently within each of the
survey's estimation cells. Men aged 18 to 49 with no settled household (lodgers, crews, seasonal and shift workers,
men between addresses) are missed by both far more often, so within any cell the survey's match rate overstates the
census's coverage of them. Births, deaths and border movements fix how many men there are against women, and the women
are estimated right."""
import datetime as dt

SEED = 505
OFFICE = "National Statistics Office"
DIVISION = "Census and Population Estimates"
COMMISSION = "Electoral Commission"
CENSUS = "2025 Census of Population and Dwellings"
PES = "2025 Post-Enumeration Survey"
CAMPAIGN = "2027 enrolment campaign"
PEOPLE = {"estimates": "Chelsea Buckley",   # manager of population estimates, the Office
          "commission": "Bryan Tapp"}       # enrolment and outreach manager, the Commission

CENSUS_DAY = dt.date(2025, 3, 4)
PES_FIELD = (dt.date(2025, 4, 7), dt.date(2025, 6, 27))
AS_OF = dt.date(2026, 10, 14)
ORGANISERS = 200
FLOOR = 2
MB_SAMPLE = 30                      # the survey takes one meshblock in 30 within each region

# Regions: (code, name, type, usual residents on census day in thousands). Types shape the age structure, the share of
# men with no settled household, census and survey coverage and enrolment.
REGIONS = [
    ("01", "Ardenmere", "metro", 612),
    ("02", "Merriton", "metro", 468),
    ("03", "Westerby", "metro", 401),
    ("04", "Larchfield", "college", 336),
    ("05", "Glenwhite", "college", 298),
    ("06", "Hawksridge", "coastal", 287),
    ("07", "Fairholme", "rural", 266),
    ("08", "Eastwold", "coastal", 244),
    ("09", "Corran Valley", "resource", 231),
    ("10", "Drumlea", "rural", 218),
    ("11", "Orrinvale", "coastal", 204),
    ("12", "Inchgarry", "resource", 189),
    ("13", "Strathmuir", "rural", 176),
    ("14", "Rowanlea", "coastal", 161),
    ("15", "Kilraven", "resource", 148),
    ("16", "Nethermoor", "rural", 132),
]
CODES = [r[0] for r in REGIONS]
NAME = {r[0]: r[1] for r in REGIONS}
TYPE = {r[0]: r[2] for r in REGIONS}
SIZE = {r[0]: r[3] * 1000 for r in REGIONS}

# The survey's estimation cells: region by sex by these age groups.
AGE_GROUPS = [(0, 14), (15, 17), (18, 24), (25, 34), (35, 49), (50, 64), (65, 120)]
ADULT_GROUPS = [g for g in AGE_GROUPS if g[0] >= 18]
YOUNG_GROUPS = [(18, 24), (25, 34), (35, 49)]


def age_group(age):
    for lo, hi in AGE_GROUPS:
        if lo <= age <= hi:
            return (lo, hi)
    raise ValueError(age)


def group_label(g):
    return "%d-%d" % g if g[1] < 120 else "%d+" % g[0]


# Men aged 18 to 49 with no settled household, as a share of the men of that age, by region type, and their chance of
# being counted by the census and by the survey. Everyone else is counted independently by the two, at rates set by
# region and cell.
UNSETTLED = {"metro": 0.175, "college": 0.155, "coastal": 0.125, "rural": 0.13, "resource": 0.195}
P_CENSUS_UNSETTLED, P_PES_UNSETTLED = 0.47, 0.42
P_CENSUS = {"metro": 0.962, "college": 0.958, "coastal": 0.978, "rural": 0.972, "resource": 0.960}
P_PES = {"metro": 0.938, "college": 0.934, "coastal": 0.955, "rural": 0.950, "resource": 0.936}
YOUNG_ADULT_DROP = {(18, 24): 0.022, (25, 34): 0.014, (35, 49): 0.006}     # lower coverage of settled young adults
# Erroneous census enumerations per correct one, by age group, and the census records imputed for dwellings it could
# not contact (a share of each region's counted records).
EE_RATE = {(0, 14): 0.009, (15, 17): 0.014, (18, 24): 0.018, (25, 34): 0.013, (35, 49): 0.010, (50, 64): 0.010,
           (65, 120): 0.012}
EE_TYPE = {   # region types where people are counted twice more often: students at term and home addresses in the
              # college regions, owners of a second home in the coastal ones
    "college": {(18, 24): 2.8, (25, 34): 1.5}, "coastal": {(50, 64): 1.8, (65, 120): 2.4},
    "metro": {}, "rural": {}, "resource": {}}
IMPUTED = {"metro": 0.007, "college": 0.008, "coastal": 0.014, "rural": 0.016, "resource": 0.009}

# Enrolment on census day of residents aged 18 and over, by region type; unsettled men enrol far less.
ENROL = {"metro": 0.925, "college": 0.900, "coastal": 0.968, "rural": 0.955, "resource": 0.948}
ENROL_AGE = {(18, 24): -0.085, (25, 34): -0.045, (35, 49): -0.012, (50, 64): 0.010, (65, 120): 0.018}
ENROL_UNSETTLED = 0.44
STALE_ROLL = 0.009                  # electors still on the roll at an address they had left the country from or died

# Electorates nest in regions: (code, name, region). Two were renamed at the 2024 boundary review; the roll uses the
# codes, which did not change.
ELECTORATES = [
    ("101", "Ardenmere Central", "01"), ("102", "Ardenmere North", "01"), ("103", "Ardenmere South", "01"),
    ("104", "Ardenmere West", "01"), ("105", "Bayhurst", "01"), ("106", "Colliers Bend", "01"), ("107", "Pinecrest", "01"),
    ("201", "Merriton Central", "02"), ("202", "Merriton East", "02"), ("203", "Harbourview", "02"),
    ("204", "Ashgrove", "02"), ("205", "Tollard", "02"),
    ("301", "Westerby", "03"), ("302", "Westerby Hills", "03"), ("303", "Calderhaugh", "03"), ("304", "Maple Reach", "03"),
    ("401", "Larchfield", "04"), ("402", "Larchfield East", "04"), ("403", "Brenton", "04"), ("404", "Coldwater", "04"),
    ("501", "Glenwhite", "05"), ("502", "Glenwhite Downs", "05"), ("503", "Arkley", "05"),
    ("601", "Hawksridge", "06"), ("602", "Selsey Point", "06"), ("603", "Marrow Bay", "06"),
    ("701", "Fairholme", "07"), ("702", "Upper Fairholme", "07"), ("703", "Dunstable Plains", "07"),
    ("801", "Eastwold", "08"), ("802", "Eastwold Coast", "08"), ("803", "Kettering Heads", "08"),
    ("901", "Corran", "09"), ("902", "Corran Valley South", "09"),
    ("1001", "Drumlea", "10"), ("1002", "Drumlea Hills", "10"),
    ("1101", "Orrinvale", "11"), ("1102", "Tarrant Sound", "11"),
    ("1201", "Inchgarry", "12"), ("1202", "Inchgarry Ranges", "12"),
    ("1301", "Strathmuir", "13"), ("1302", "Lowther", "13"),
    ("1401", "Rowanlea", "14"), ("1402", "Pellow Bay", "14"),
    ("1501", "Kilraven", "15"), ("1502", "Kilraven Coast", "15"),
    ("1601", "Nethermoor", "16"),
]
RENAMED = {"203": "Merriton Harbour", "902": "Corran South"}       # the names the electorates carried until 2024
ELECTORATE_REGION = {e[0]: e[2] for e in ELECTORATES}

# The roll platform. The old platform ran to 3 August 2025 and logged in the country's time; it handled a move to
# another electorate as a removal (reason 05) and an enrolment at the new address under a new elector number. The new
# platform, live from 4 August 2025, records a move as a change of address and stamps every transaction in UTC; it
# reused reason code 01 for a removal at the elector's own request, where the old platform's 01 was a death.
PLATFORM_SWITCH = dt.date(2025, 8, 4)
LOG_END = dt.date(2026, 6, 30)       # the asks' window closes at the end of 30 June 2026 in the country's time
DST_2025 = (dt.datetime(2025, 9, 28, 2), dt.datetime(2026, 4, 5, 3))   # local daylight time, UTC+13 between these
