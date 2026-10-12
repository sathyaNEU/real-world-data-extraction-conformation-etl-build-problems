"""The campus water system and its calendar: five wells, four tanks in two pressure zones, the booster station,
the buildings and their meters, the academic year and the clocks (UTC in the historian, Eastern on the campus)."""
import datetime as dt
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc

ORG = "Kettle Ridge University"
DEPT = "Facilities and Operations, Campus Utilities"
SYSTEM = "Kettle Ridge University Campus Water System"
PWSID = "4149327"
STATE = "Pennsylvania Department of Environmental Protection"
STATE_PROGRAM = "Safe Drinking Water Program, Northcentral District"

EVAL0, EVAL1 = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
T0 = dt.datetime(2025, 10, 1, 4, 0, tzinfo=UTC)          # local midnight opening 1 October 2025 (EDT)
T1 = dt.datetime(2026, 10, 12, 4, 0, tzinfo=UTC)         # local midnight opening 12 October 2026, the log's last row
STEP = 15                                                # minutes
EXTRACT = dt.date(2026, 10, 12)

# wells: tested capacity in the most recent pump test, nameplate, and the delivered fraction of tested
WELLS = ["W1", "W2", "W3", "W4", "W5"]
WELL_NAMES = {"W1": "Well 1 (Field House)", "W2": "Well 2 (Orchard)", "W3": "Well 3 (Recreation Fields)",
              "W4": "Well 4 (South Farm)", "W5": "Well 5 (Poultry Lane)"}
NAMEPLATE = {"W1": 1100, "W2": 850, "W3": 800, "W4": 750, "W5": 700}
W1_OUT = (dt.date(2026, 8, 10), dt.date(2026, 8, 28))    # rehabilitation, both days included
W4_OUT = dt.date(2026, 2, 11)                            # check valve replaced
BPS_P1_OUT = (dt.date(2026, 8, 12), dt.date(2026, 8, 25))  # booster pump 1 seal replacement, both days included
# pump tests: (well, date, gpm); the most recent for W2 to W5 are spring 2026, before the peak
PUMP_TESTS = [
    ("W1", dt.date(2021, 5, 11), 1120), ("W1", dt.date(2022, 5, 17), 1098), ("W1", dt.date(2023, 5, 9), 1093),
    ("W1", dt.date(2024, 5, 14), 1061), ("W1", dt.date(2025, 5, 13), 1050), ("W1", dt.date(2026, 4, 21), 1010),
    ("W1", dt.date(2026, 9, 15), 1090),
    ("W2", dt.date(2021, 5, 12), 845), ("W2", dt.date(2022, 5, 18), 834), ("W2", dt.date(2023, 5, 10), 842),
    ("W2", dt.date(2024, 5, 15), 828), ("W2", dt.date(2025, 5, 14), 827), ("W2", dt.date(2026, 4, 22), 820),
    ("W3", dt.date(2021, 6, 2), 790), ("W3", dt.date(2022, 6, 7), 779), ("W3", dt.date(2023, 6, 6), 786),
    ("W3", dt.date(2024, 6, 4), 770), ("W3", dt.date(2025, 6, 3), 766), ("W3", dt.date(2026, 5, 12), 760),
    ("W4", dt.date(2021, 6, 3), 726), ("W4", dt.date(2022, 6, 8), 719), ("W4", dt.date(2023, 6, 7), 721),
    ("W4", dt.date(2024, 6, 5), 708), ("W4", dt.date(2025, 6, 4), 707), ("W4", dt.date(2026, 4, 28), 700),
    ("W5", dt.date(2021, 6, 9), 668), ("W5", dt.date(2022, 6, 14), 664), ("W5", dt.date(2023, 6, 13), 655),
    ("W5", dt.date(2024, 6, 11), 657), ("W5", dt.date(2025, 6, 10), 646), ("W5", dt.date(2026, 5, 13), 640),
]


def latest_tests(asof=dt.date(2026, 10, 12)):
    out = {}
    for w, d, g in PUMP_TESTS:
        if d <= asof and (w not in out or d > out[w][0]):
            out[w] = (d, g)
    return {w: g for w, (d, g) in out.items()}


TESTED = latest_tests()
FIRM = sum(TESTED.values()) - max(TESTED.values())               # 2,920 gpm
LARGEST = max(TESTED, key=TESTED.get)
DELIVERED = {"W1": 0.981, "W2": 0.986, "W3": 0.983, "W4": 0.985, "W5": 0.982}   # of the tested rate, typical day
W3_REGISTER = 100_000_000                                        # 8-digit register, gallons
TOT0 = {"W1": 141_208_330, "W2": 277_402_115, "W3": None, "W4": 112_550_870, "W5": 230_115_220}   # W3 set by its rollover
W3_ROLLOVER = dt.datetime(2026, 3, 4, 15, 0)                      # local; the register passes 99,999,999

# tanks: gallons per foot of level, the elevation of level zero, height to overflow (feet), zone
TANKS = ["A", "B", "C", "D"]
TANK_NAMES = {"A": "Standpipe No. 1 (Physical Plant)", "B": "Stadium Elevated Tank",
              "C": "North Campus Reservoir", "D": "North Campus Elevated Tank"}
GPF = {"A": 21100, "B": 16200, "C": 9400, "D": 7600}
BASE = {"A": 1040.0, "B": 1120.0, "C": 1230.0, "D": 1232.0}
HEIGHT = {"A": 120.0, "B": 40.0, "C": 32.0, "D": 30.0}
ZONE_OF_TANK = {"A": "main", "B": "main", "C": "hill", "D": "hill"}
MAIN_OVF, HILL_OVF = 1160.0, 1262.0
BOOSTER_RATE = 905.0                                              # gpm per pump, duty and standby


def nominal(t):
    return int(GPF[t] * HEIGHT[t])


# academic calendar
def season(d):
    if dt.date(2025, 11, 22) <= d <= dt.date(2025, 11, 30):
        return "thanks"
    if dt.date(2025, 12, 20) <= d <= dt.date(2026, 1, 10):
        return "winter"
    if dt.date(2026, 3, 7) <= d <= dt.date(2026, 3, 15):
        return "spring"
    if dt.date(2026, 5, 9) <= d <= dt.date(2026, 8, 18):
        return "summer"
    if dt.date(2026, 8, 19) <= d <= dt.date(2026, 8, 23):
        return "movein"
    if dt.date(2025, 12, 13) <= d <= dt.date(2025, 12, 19) or dt.date(2026, 5, 2) <= d <= dt.date(2026, 5, 8):
        return "finals"
    return "term"


HOME_GAMES = [dt.date(2025, 10, 4), dt.date(2025, 10, 18), dt.date(2025, 11, 1), dt.date(2025, 11, 15),
              dt.date(2026, 9, 5), dt.date(2026, 9, 19), dt.date(2026, 10, 3)]
MAIN_BREAKS = [(dt.datetime(2026, 1, 22, 13, 10), dt.datetime(2026, 1, 22, 22, 40), 610.0, "main",
                "6-in main break, College Avenue at Fraser Street"),
               (dt.datetime(2026, 2, 26, 6, 30), dt.datetime(2026, 2, 26, 11, 50), 380.0, "hill",
                "4-in main break, Reservoir Road")]
FLUSHING = [dt.date(2026, 4, 13) + dt.timedelta(k) for k in range(12)
            if (dt.date(2026, 4, 13) + dt.timedelta(k)).weekday() < 5]
WINTER_SETPOINTS = (dt.date(2025, 11, 17), dt.date(2026, 3, 29))   # main zone band lowered 5 ft
FALL_SETPOINT = dt.date(2026, 9, 28)                               # main zone band lowered 3 ft


def local(t):
    return t.astimezone(ET)


def eval_days():
    out, d = [], EVAL0
    while d <= EVAL1:
        out.append(d)
        d += dt.timedelta(1)
    return out


# buildings: number, name, category, zone, weight within category (share of the category's water), service lines
# (one meter each), year built; the categories are the space inventory's primary use
B = []


def _b(no, name, cat, zone, w, lines=1, built=1970, gsf=60000):
    B.append(dict(no=no, name=name, cat=cat, zone=zone, w=w, lines=lines, built=built, gsf=gsf))


# residence halls (weights by beds; North Commons carries the north campus dining hall)
for no, name, zone, w, lines, built, gsf in [
    (101, "Hemlock Hall", "hill", 820, 2, 1966, 213880), (102, "Tamarack Hall", "hill", 610, 1, 1966, 157559),
    (103, "Sycamore Hall", "hill", 790, 2, 1969, 204609), (104, "Buttonwood Hall", "hill", 430, 1, 1971, 112285),
    (105, "Sassafras Hall", "hill", 390, 1, 1971, 101176), (106, "Ridgecrest Hall", "hill", 455, 1, 1988, 118718),
    (107, "Old North Hall", "hill", 300, 1, 1958, 78182), (108, "Quarry View Hall", "hill", 520, 1, 1993, 136341),
    (109, "Hillside Hall", "hill", 470, 1, 2004, 124313), (110, "Overlook Hall", "hill", 505, 1, 2011, 130746),
    (111, "North Commons", "hill", 1180, 1, 1999, 188129),
    (121, "College Avenue Hall", "main", 360, 1, 1955, 92048), (122, "Ironwood Hall", "main", 410, 1, 1962, 106690),
    (123, "Elm Court Hall", "main", 380, 1, 1962, 99338), (124, "Redbud Hall", "main", 440, 1, 2001, 115961),
    (125, "South Quad Hall", "main", 350, 1, 1957, 90210), (126, "Hornbeam Hall", "main", 495, 1, 2015, 128908),
    (47, "Larch Hall", "main", 640, 1, 2026, 167749)]:
    _b(no, name, "Residence Hall", zone, w, lines, built, gsf)
for no, name, zone, w, built, gsf in [
    (201, "Agricultural Sciences Building", "main", 160, 1961, 117799), (202, "Biology Building", "main", 210, 1964, 131665),
    (203, "Chemistry Building", "main", 260, 1967, 151126), (204, "Physics Building", "main", 130, 1965, 98419),
    (205, "Mathematics Building", "main", 70, 1972, 64316), (206, "Engineering Hall", "main", 240, 1979, 176101),
    (207, "Earth Sciences Building", "main", 95, 1974, 70749), (208, "Business Building", "main", 120, 2006, 112285),
    (209, "Education Building", "main", 75, 1968, 68911), (210, "Humanities Building", "main", 80, 1970, 76344),
    (211, "Social Sciences Building", "main", 85, 1973, 80020), (212, "Nursing Building", "main", 90, 2009, 73506),
    (213, "Computer Science Building", "main", 95, 2013, 88372), (214, "Music Building", "hill", 70, 1977, 60559),
    (215, "Library", "main", 140, 1984, 212042), (216, "Learning Commons", "main", 60, 2018, 54126),
    (217, "Forestry Building", "hill", 85, 1963, 66154), (218, "Architecture Building", "main", 65, 1990, 57802),
    (219, "Communications Building", "main", 60, 1997, 52288), (220, "Health Sciences Building", "main", 115, 2016, 96500),
    (221, "Kinesiology Building", "main", 105, 1981, 82777), (222, "Psychology Building", "main", 70, 1976, 59640),
    (223, "Veterinary Science Building", "main", 175, 1983, 102095), (224, "Food Science Building", "main", 150, 1987, 89291),
    (225, "Agricultural Engineering Building", "main", 90, 1975, 69830), (226, "Classroom Building East", "main", 55, 1999, 47612),
    (227, "Classroom Building West", "main", 50, 2000, 45774), (228, "Visual Arts Building", "hill", 60, 1979, 56883)]:
    _b(no, name, "Academic", zone, w, 1, built, gsf)
for no, name, zone, w, lines, built, gsf in [
    (301, "Life Sciences Building", "main", 420, 1, 2003, 196338), (302, "Materials Research Laboratory", "main", 300, 2, 1992, 133503),
    (303, "Water Resources Laboratory", "main", 110, 1, 1986, 41179), (304, "Greenhouse Complex", "main", 190, 1, 1978, 63397),
    (305, "Animal Science Research Center", "main", 260, 1, 1984, 88372), (306, "Plant Pathology Laboratory", "main", 95, 1, 1972, 39341),
    (307, "Food Pilot Plant", "main", 180, 1, 1995, 46693), (308, "Energy Research Building", "main", 120, 1, 2012, 71668)]:
    _b(no, name, "Research", zone, w, lines, built, gsf)
for no, name, zone, w, built, gsf in [
    (401, "University Stadium", "main", 260, 1964, 309961), (402, "Natatorium", "main", 310, 1990, 95724),
    (403, "Field House", "main", 180, 1959, 141855), (404, "Ice Arena", "main", 140, 1987, 88372),
    (405, "Tennis Center", "main", 40, 2008, 52288), (406, "Athletics Practice Complex", "main", 230, 2014, 60559),
    (407, "Baseball and Softball Complex", "main", 90, 2010, 28232)]:
    _b(no, name, "Athletics", zone, w, 1, built, gsf)
_b(501, "Central Energy Plant", "Utilities", "main", 1, 1, 1968, 73506)
_b(502, "Facilities Services Building", "Utilities", "main", 1, 1, 1974, 80939)
_b(503, "Grounds Shop", "Utilities", "main", 1, 1, 1981, 21718)
for no, name, cat, zone, w, lines, built, gsf in [
    (601, "Old Main", "Administrative", "main", 120, 1, 1911, 98419), (602, "Alumni Center", "Administrative", "main", 35, 1, 1994, 26394),
    (603, "Police and Safety Building", "Administrative", "main", 40, 1, 2002, 23556),
    (604, "Admissions Center", "Administrative", "main", 25, 1, 2010, 18042),
    (605, "Human Resources Building", "Administrative", "main", 30, 1, 1971, 21718),
    (701, "Student Union", "Student Life", "main", 260, 1, 1972, 188129), (702, "Health Center", "Student Life", "hill", 70, 1, 1997, 41179),
    (703, "Student Wellness Center", "Student Life", "main", 230, 1, 2007, 131665),
    (704, "South Dining Hall", "Student Life", "main", 310, 1, 1964, 57802),
    (705, "University Chapel", "Student Life", "hill", 12, 1, 1931, 14366),
    (706, "Child Care Center", "Student Life", "main", 25, 1, 2012, 15285),
    (801, "Conference Center and Inn", "Auxiliary", "main", 330, 2, 1989, 153883),
    (802, "University Bookstore", "Auxiliary", "main", 30, 1, 1998, 38422),
    (803, "Parking Deck East", "Auxiliary", "main", 10, 1, 2005, 289724),
    (901, "Performing Arts Center", "Arts and Culture", "main", 90, 1, 1980, 120556),
    (902, "Art Museum", "Arts and Culture", "main", 30, 1, 1972, 33746)]:
    _b(no, name, cat, zone, w, lines, built, gsf)
# the Science Annex, building 47 until its removal for the Larch Hall project
ANNEX = dict(no=47, name="Science Annex", cat="Research", zone="main", w=95, lines=1, built=1968, gsf=37964)
ANNEX_REMOVED = dt.datetime(2025, 12, 19, 9, 30)          # local; meter removed, building demolished in January
ANNEX_WINDDOWN = dt.date(2025, 12, 6)                     # vacated after the fall classes ended
LARCH_INSTALL = dt.datetime(2026, 7, 14, 13, 15)          # local; meter set at the new hall
LARCH_RAS = dt.date(2026, 8, 14)                          # resident assistants
LARCH_OCCUPIED = dt.date(2026, 8, 17)

CATS = ["Residence Hall", "Academic", "Research", "Athletics", "Utilities", "Administrative", "Student Life",
        "Auxiliary", "Arts and Culture"]
