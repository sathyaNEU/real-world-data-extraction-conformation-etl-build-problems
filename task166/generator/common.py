"""task166 constants and helpers shared by every generator module.

Plinthwise, Inc. (Denver, Colorado) sells construction project-management software (daily logs, RFIs, submittals,
the field app) to contractors through six regional sales teams. Its FY2028 plan funds one more onboarding pod, which
sits with one regional team for all of calendar 2027: the region expected to add the most new paying customers in
2027. Every system was exported on Thursday 1 October 2026, covering activity to 30 September 2026.

Months are indexed from January 2019 (t = 0); the world runs from January 2015 (t = -48) to December 2027 (t = 107)."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os

import numpy as np

SEED = int(os.environ.get("T166_SEED", 159))

COMPANY = "Plinthwise"
COMPANY_LEGAL = "Plinthwise, Inc."
PEOPLE = {
    "vp": "Jeff Guzman",          # VP Customer Onboarding: the memo
    "mops": "Joseph Clay",        # Marketing Operations: the spend workbook
    "fpa": "Guy Morrison",        # FP&A: the FY2028 planning basis
}

# ------------------------------------------------------------------------------------------------- calendar
PULL = dt.date(2026, 10, 1)          # every export
DATA_END = dt.date(2026, 9, 30)
BASIS_DATE = dt.date(2026, 10, 2)    # FP&A's FY2028 planning basis
MEMO_DATE = dt.date(2026, 10, 20)
T0 = -48                             # January 2015
T_OBS = 92                           # September 2026
T_END = 107                          # December 2027
Y27 = list(range(96, 108))
N_T = T_END - T0 + 1                 # 156 months


def ym(t):
    """(year, month) of month index t (t = 0 is January 2019)."""
    return 2019 + (t // 12), t % 12 + 1


def tindex(d):
    return (d.year - 2019) * 12 + d.month - 1


def days_in(y, m):
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days


def month_start(t):
    y, m = ym(t)
    return dt.date(y, m, 1)


def month_end(t):
    y, m = ym(t)
    return dt.date(y, m, days_in(y, m))


def fiscal_label(t):
    """Plinthwise's fiscal year runs February to January and is named for the calendar year it ends in."""
    y, m = ym(t)
    fy = y + 1 if m >= 2 else y
    p = (m - 2) % 12 + 1
    return fy, p


# ------------------------------------------------------------------------------------------------- regions
REGIONS = ["Southwest", "Southeast", "Texas & Gulf", "Midwest", "Northeast", "Pacific"]
SW, SE, TX, MW, NE, PA = range(6)
STATES = {
    "Southwest": [("AZ", 0.52), ("NV", 0.16), ("NM", 0.10), ("UT", 0.14), ("CO", 0.08)],
    "Southeast": [("GA", 0.27), ("FL", 0.31), ("NC", 0.17), ("SC", 0.11), ("AL", 0.08), ("MD", 0.06)],
    "Texas & Gulf": [("TX", 0.78), ("LA", 0.12), ("OK", 0.10)],
    "Midwest": [("OH", 0.19), ("IL", 0.21), ("MI", 0.13), ("IN", 0.11), ("WI", 0.10), ("MN", 0.10), ("TN", 0.11), ("KY", 0.05)],
    "Northeast": [("NY", 0.30), ("PA", 0.24), ("NJ", 0.18), ("MA", 0.18), ("CT", 0.10)],
    "Pacific": [("CA", 0.66), ("WA", 0.20), ("OR", 0.14)],
}
STATE_NAMES = {"AZ": "Arizona", "NV": "Nevada", "NM": "New Mexico", "UT": "Utah", "CO": "Colorado", "GA": "Georgia",
               "FL": "Florida", "NC": "North Carolina", "SC": "South Carolina", "AL": "Alabama", "MD": "Maryland",
               "TX": "Texas", "LA": "Louisiana", "OK": "Oklahoma", "OH": "Ohio", "IL": "Illinois", "MI": "Michigan",
               "IN": "Indiana", "WI": "Wisconsin", "MN": "Minnesota", "TN": "Tennessee", "KY": "Kentucky", "NY": "New York",
               "PA": "Pennsylvania", "NJ": "New Jersey", "MA": "Massachusetts", "CT": "Connecticut", "CA": "California",
               "WA": "Washington", "OR": "Oregon"}
# hours behind UTC in standard time and whether the state keeps daylight time (Arizona does not)
STATE_UTC = {"AZ": (7, False), "NV": (8, True), "NM": (7, True), "UT": (7, True), "CO": (7, True), "GA": (5, True),
             "FL": (5, True), "NC": (5, True), "SC": (5, True), "AL": (6, True), "MD": (5, True), "TX": (6, True),
             "LA": (6, True), "OK": (6, True), "OH": (5, True), "IL": (6, True), "MI": (5, True), "IN": (5, True),
             "WI": (6, True), "MN": (6, True), "TN": (6, True), "KY": (5, True), "NY": (5, True), "PA": (5, True),
             "NJ": (5, True), "MA": (5, True), "CT": (5, True), "CA": (8, True), "WA": (8, True), "OR": (8, True)}
AREA = {"AZ": [480, 602, 623, 520, 928], "NV": [702, 725, 775], "NM": [505, 575], "UT": [801, 385, 435], "CO": [303, 720, 719, 970],
        "GA": [404, 678, 470, 770, 912], "FL": [305, 786, 407, 321, 813, 727, 904, 954, 561], "NC": [704, 980, 919, 984, 336],
        "SC": [803, 843, 864], "AL": [205, 251, 256, 334], "MD": [410, 443, 301], "TX": [214, 469, 972, 512, 737, 713, 281, 832, 210, 817],
        "LA": [504, 225, 337], "OK": [405, 918], "OH": [614, 216, 513, 330, 419, 937], "IL": [312, 773, 630, 847, 217],
        "MI": [313, 248, 616, 517], "IN": [317, 219, 260, 812], "WI": [414, 608, 920], "MN": [612, 651, 952, 763],
        "TN": [615, 629, 901, 865, 423], "KY": [502, 859, 270], "NY": [212, 718, 917, 516, 585, 716], "PA": [215, 267, 412, 717, 610],
        "NJ": [201, 973, 732, 908], "MA": [617, 508, 781, 413], "CT": [203, 860], "CA": [213, 310, 415, 408, 619, 714, 916, 951],
        "WA": [206, 253, 425, 509], "OR": [503, 541, 971]}
REALIGN = dt.date(2024, 3, 1)        # Tennessee moved from Southeast to Midwest


def region_of_state(st, on=None):
    """The sales region of a billing state under the map in force on a date (the current map when on is None)."""
    if st == "TN" and on is not None and on < REALIGN:
        return "Southeast"
    for r, sts in STATES.items():
        if any(s == st for s, _ in sts):
            return r
    raise KeyError(st)


# ------------------------------------------------------------------------------------------------- people and companies
FIRST = ("James John Robert Michael William David Richard Joseph Thomas Christopher Charles Daniel Matthew Anthony Mark Donald Steven "
         "Paul Andrew Joshua Kenneth Kevin Brian George Timothy Ronald Jason Edward Jeffrey Ryan Jacob Gary Nicholas Eric Jonathan "
         "Stephen Larry Justin Scott Brandon Benjamin Samuel Gregory Alexander Patrick Frank Raymond Jack Dennis Jerry Tyler Aaron "
         "Jose Adam Nathan Henry Zachary Douglas Peter Kyle Noah Ethan Jeremy Christian Walter Keith Austin Roger Terry Sean Gerald "
         "Carl Dylan Harold Jordan Jesse Bryan Lawrence Arthur Gabriel Bruce Logan Billy Joe Alan Juan Elijah Willie Albert Wayne "
         "Randy Mason Vincent Liam Roy Bobby Caleb Bradley Russell Lucas Mary Patricia Jennifer Linda Elizabeth Barbara Susan Jessica "
         "Sarah Karen Lisa Nancy Betty Sandra Margaret Ashley Kimberly Emily Donna Michelle Carol Amanda Melissa Deborah Stephanie "
         "Rebecca Sharon Laura Cynthia Dorothy Amy Kathleen Angela Shirley Emma Brenda Pamela Nicole Anna Samantha Katherine Christine "
         "Debra Rachel Carolyn Janet Maria Olivia Heather Helen Catherine Diane Julie Victoria Joyce Lauren Kelly Christina Ruth Joan "
         "Virginia Judith Evelyn Hannah Andrea Megan Cheryl Jacqueline Madison Teresa Abigail Sophia Martha Sara Gloria Janice Kathryn "
         "Ann Isabella Judy Charlotte Julia Grace Amber Alice Jean Denise Frances Danielle Marilyn Natalie Beverly Diana Brittany "
         "Theresa Kayla Alexis Doris Lori Tiffany Luis Carlos Miguel Jorge Ricardo Manuel Alejandro Fernando Javier Diego Rafael Hector "
         "Marco Eduardo Sergio Andres Armando Oscar Ruben Victor Raul Ana Rosa Elena Lucia Gabriela Veronica Adriana Monica Claudia").split()
LAST = ("Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez Martinez Hernandez Lopez Gonzalez Wilson Anderson Thomas "
        "Taylor Moore Jackson Martin Lee Perez Thompson White Harris Sanchez Clark Ramirez Lewis Robinson Walker Young Allen King "
        "Wright Scott Torres Nguyen Hill Flores Green Adams Nelson Baker Hall Rivera Campbell Mitchell Carter Roberts Gomez Phillips "
        "Evans Turner Diaz Parker Cruz Edwards Collins Reyes Stewart Morris Morales Murphy Cook Rogers Gutierrez Ortiz Morgan Cooper "
        "Peterson Bailey Reed Kelly Howard Ramos Kim Cox Ward Richardson Watson Brooks Chavez Wood James Bennett Gray Mendoza Ruiz "
        "Hughes Price Alvarez Castillo Sanders Patel Myers Long Ross Foster Jimenez Powell Jenkins Perry Russell Sullivan Bell "
        "Coleman Butler Henderson Barnes Gonzales Fisher Vasquez Simmons Romero Jordan Patterson Alexander Hamilton Graham Reynolds "
        "Griffin Wallace Moreno West Cole Bryant Herrera Gibson Ellis Tran Medina Aguilar Stevens Murray Ford Castro Marshall "
        "Owens Harrison Fernandez McDonald Woods Washington Kennedy Wells Vargas Henry Chen Freeman Webb Tucker Burns Crawford "
        "Olson Simpson Hunter Gordon Mendez Silva Shaw Snyder Mason Dixon Munoz Hunt Hicks Holmes Palmer Wagner Black Robertson "
        "Rose Stone Salazar Fox Warren Mills Meyer Rice Schmidt Garza Daniels Ferguson Nichols Stephens Soto Weaver Ryan Gardner "
        "Payne Grant Dunn Kelley Spencer Hawkins Arnold Pierce Vazquez Hansen Peters Santos Hart Bradley Knight Elliott Cunningham "
        "Duncan Armstrong Hudson Carroll Lane Riley Andrews Alvarado Ray Delgado Berry Perkins Hoffman Johnston Matthews Pena Richards "
        "Contreras Willis Carpenter Lawrence Sandoval Guerrero George Chapman Rios Estrada Ortega Watkins Greene Nunez Wheeler Valdez "
        "Harper Burke Larson Santiago Maldonado Franklin Carlson Austin Dominguez Carr Lawson Jacobs Obrien Lynch Singh Vega "
        "Bishop Montgomery Oliver Jensen Harvey Williamson Gilbert Dean Sims Espinoza Howell Li Wong Reid Hanson Le McCoy Garrett "
        "Burton Fuller Wang Weber Welch Rojas Lucas Marquez Fields Park Yang Little Banks Padilla Day Walsh Bowman Schultz Luna Fowler").split()
NICK = {"Robert": "Bob", "William": "Bill", "Richard": "Rick", "Joseph": "Joe", "Thomas": "Tom", "Christopher": "Chris", "Daniel": "Dan",
        "Matthew": "Matt", "Anthony": "Tony", "Michael": "Mike", "James": "Jim", "Steven": "Steve", "Andrew": "Andy", "Kenneth": "Ken",
        "Timothy": "Tim", "Ronald": "Ron", "Edward": "Ed", "Jeffrey": "Jeff", "Nicholas": "Nick", "Jonathan": "Jon", "Gregory": "Greg",
        "Alexander": "Alex", "Patrick": "Pat", "Elizabeth": "Liz", "Jennifer": "Jen", "Katherine": "Kate", "Rebecca": "Becky",
        "Samantha": "Sam", "Deborah": "Debbie", "Kimberly": "Kim", "Benjamin": "Ben", "Samuel": "Sam", "Zachary": "Zach"}
CO_A = ("Desert Ridge|Copper Canyon|Red Rock|Saguaro|Mesa Verde|High Plains|Lone Star|Gulf Coast|Bayou|Riverbend|Lakeshore|Prairie|"
        "Northstar|Ironwood|Granite Peak|Summit|Keystone|Harbor|Pinecrest|Oak Hollow|Cedar Point|Bluebonnet|Magnolia|Palmetto|"
        "Coastal|Tidewater|Piedmont|Blue Ridge|Great Lakes|Heartland|Frontier|Sierra|Cascade|Pacific Crest|Golden State|Bay Area|"
        "Evergreen|Silverline|Stonebridge|Ridgeline|Westgate|Eastport|Southpoint|Crossroads|Landmark|Cornerstone|Benchmark|Plumbline|"
        "Trailhead|Canyon State|Valley|Sun Country|Delta|Brazos|Pecos|Wasatch|Front Range|Ozark|Cumberland|Chattahoochee|Ironhorse|"
        "Blackrock|Clearwater|Redstone|Highline|Bridgewater|Fairway|Kingsway|Millstone|Northgate|Old Mill|Pioneer|Quarry|Sandstone|"
        "Timberline|Union|Victory|Windmill").split("|")
CO_B = ["Builders", "Construction", "Contracting", "General Contractors", "Construction Group", "Constructors", "Homes",
        "Concrete", "Electric", "Mechanical", "Plumbing", "Roofing", "Framing", "Drywall", "Excavation", "Steel", "Glass & Glazing",
        "Interiors", "Civil", "Building Co", "Development", "Restoration", "Paving", "Fire Protection", "HVAC", "Masonry",
        "Site Services", "Industrial", "Utilities", "Millwork"]
TITLES = {"PM": ["Project Manager", "Sr. Project Manager", "Project Manager", "PM", "Project Mgr", "Senior PM", "Assistant Project Manager"],
          "SUPER": ["Superintendent", "Supt.", "General Superintendent", "Site Superintendent", "Asst. Superintendent", "Superintendent", "Super"],
          "PE": ["Project Engineer", "Project Engineer", "PE", "Field Engineer", "Project Engineer II", "Project Coordinator"],
          "OWNER": ["Owner", "President", "Principal", "CEO", "VP Operations", "Vice President"],
          "OFFICE": ["Office Manager", "Accounting", "Admin", "Estimator", "Controller", "Project Accountant", "Office Admin"],
          "FIELD": ["Foreman", "Field Lead", "Crew Lead", "Safety Manager", "Laborer", "Lead Carpenter"]}
LEAD_ORG = [("Inbound - free trial", 55), ("Outbound - SDR", 19), ("Trade show", 8), ("Partner - association", 7),
            ("Customer referral", 5), ("Other", 6)]
LEAD_CH = [("Inbound - free trial", 72), ("Outbound - SDR", 15), ("Trade show", 3), ("Other", 10)]
PLANS = {"Core": 349.0, "Pro": 889.0, "Enterprise": 2390.0}     # list price a month, before seats and discount


# ------------------------------------------------------------------------------------------------- helpers
def rng(*stream):
    """One RNG per component and key, so a change in one never moves another's draws."""
    return np.random.default_rng([SEED] + [int(s) for s in stream])


def skey(text):
    h = 0
    for ch in text:
        h = (h * 131 + ord(ch)) % 2147483647
    return h


def pick(r, items):
    a = [x for x, _ in items]
    w = np.array([y for _, y in items], float)
    return a[int(r.choice(len(a), p=w / w.sum()))]


def fmt_phone(digits, style):
    a, b, c = digits[:3], digits[3:6], digits[6:]
    return {0: f"({a}) {b}-{c}", 1: f"{a}-{b}-{c}", 2: f"+1{a}{b}{c}", 3: f"{a}.{b}.{c}", 4: f"{a}{b}{c}", 5: f"+1 {a}-{b}-{c}"}[style]


def is_dst(d):
    """US daylight time: second Sunday of March to first Sunday of November."""
    y = d.year
    m = dt.date(y, 3, 8)
    while m.weekday() != 6:
        m += dt.timedelta(days=1)
    n = dt.date(y, 11, 1)
    while n.weekday() != 6:
        n += dt.timedelta(days=1)
    return m <= d < n


def utc_offset(st, d):
    off, dst = STATE_UTC[st]
    return off - 1 if (dst and is_dst(d)) else off


def local_to_utc(st, d, hour, minute=0):
    return dt.datetime(d.year, d.month, d.day, hour, minute) + dt.timedelta(hours=utc_offset(st, d))


def write_csv(path, cols, rows, crlf=False, quoting=csv.QUOTE_MINIMAL):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n", quoting=quoting)
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def write_json(path, obj, indent=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, sort_keys=False)
        f.write("\n")


def holidays():
    out = set()
    for y in range(2014, 2028):
        out |= {dt.date(y, 1, 1), dt.date(y, 7, 4), dt.date(y, 12, 25), dt.date(y, 12, 24), dt.date(y, 12, 31)}
        d = dt.date(y, 5, 31)
        while d.weekday() != 0:
            d -= dt.timedelta(days=1)
        out.add(d)
        d = dt.date(y, 9, 1)
        while d.weekday() != 0:
            d += dt.timedelta(days=1)
        out.add(d)
        d = dt.date(y, 11, 1)
        k = 0
        while True:
            if d.weekday() == 3:
                k += 1
                if k == 4:
                    break
            d += dt.timedelta(days=1)
        out |= {d, d + dt.timedelta(days=1)}
    return out


HOLIDAYS = holidays()


def business_day(d, back=False):
    while d.weekday() >= 5 or d in HOLIDAYS:
        d = d - dt.timedelta(days=1) if back else d + dt.timedelta(days=1)
    return d
