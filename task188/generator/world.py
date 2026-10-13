"""Rindal County Vector Control District: the names, places, dates and fixed facts of the fiction.

The county lies on the public land survey grid: 30 sections west to east (ranges R52W to R48W) and 24 south to north
(townships T137N to T140N). A section is addressed by its grid cell (x from the west, y from the south) and written as
township, range and section number. The district treats eight zones, each a set of sections, redrawn on 1 May 2026."""
import datetime as dt
import hashlib

import numpy as np

SEED = 188
# draw variants for two zones, chosen so every graded figure sits inside one bin under each pooled estimator
SALT = {"Westbrook": 294, "South Prairie": 382}

STATE = "North Dakota"
COUNTY = "Rindal County"
DISTRICT = "Rindal County Vector Control District"
DISTRICT_SHORT = "RCVCD"
CITY = "Fjelstad"
HEALTH = "Rindal County Public Health"
COUNTY_LAB = "Rindal County Public Health Laboratory"
NEIGHBOUR_HEALTH = "Lindgaard County Health Department"
APPLICATOR = "Ostby Aviation"
AIRPORT = "Fjelstad Regional Airport"

PEOPLE = {
    "ops": ("Kristine Kirby", "Operations Manager"),
    "lab": ("Philip Orr", "Laboratory Supervisor"),
    "epi": ("Paige Watkins", "Epidemiologist, Rindal County Public Health"),
    "pilot": ("Ethan Ramirez", "Chief Pilot, Ostby Aviation"),
    "surv": ("Kyle Blair", "Surveillance Coordinator"),
}
CREWS = ["J. Vaughn", "M. Duncan", "K. Brock", "J. Arias", "C. Hardy", "J. Walters"]

AS_OF = dt.date(2026, 8, 17)
EXTRACT = dt.datetime(2026, 8, 17, 8, 20)          # Central Daylight Time, the database extract
MIGRATION = dt.date(2026, 6, 15)                   # field database moved to new site IDs
LEGACY_END = dt.date(2026, 6, 14)                  # last night entered in the legacy system
REIMPORT = dt.date(2026, 6, 22)                    # legacy June records re-imported into the new database
REZONE = dt.date(2026, 5, 1)                       # zones redrawn by section
FLIGHT = dt.date(2026, 8, 20)
WEEK32 = (dt.date(2026, 8, 9), dt.date(2026, 8, 15))
SEASON_2026 = (dt.date(2026, 6, 1), dt.date(2026, 8, 15))
ENHANCED = (dt.date(2026, 6, 17), dt.date(2026, 6, 18), dt.date(2026, 6, 24), dt.date(2026, 6, 25))
# Maple Ridge's extra Wednesday and Thursday nights, the fortnight after its first positive pool (set 9 June)
FIRST_POSITIVE = ("Maple Ridge", dt.date(2026, 6, 9))
HOLIDAY_WEEK_MONDAY = dt.date(2026, 7, 6)          # crews short after the holiday: some traps not set

ZONES = ["North Bottoms", "Maple Ridge", "Westbrook", "Old Town", "Riverside South", "South Prairie", "Coulee Hills",
         "Airport East"]
ZCODE = {"North Bottoms": "NB", "Maple Ridge": "MR", "Westbrook": "WB", "Old Town": "OT", "Riverside South": "RS",
         "South Prairie": "SP", "Coulee Hills": "CH", "Airport East": "AE"}
# northern zones' pools go to the district laboratory (up to 50 females a pool), southern zones' to the county
# laboratory under the interlocal agreement of 2019 (up to 10)
NORTH = ("North Bottoms", "Maple Ridge", "Westbrook", "Old Town")
SOUTH = ("Riverside South", "South Prairie", "Coulee Hills", "Airport East")
POOL_MAX = {"district": 50, "county": 10}


def lab_of(zone):
    return "district" if zone in NORTH else "county"


NX, NY = 30, 24
SW_LAT, SW_LON = 46.5522, -97.3489
DLAT, DLON = 0.014472, 0.021084       # one mile north, one mile east at 46.7 N


def township_range(x, y):
    t = 137 + y // 6
    r = 52 - x // 6
    cx, cy = x % 6, y % 6
    row = 5 - cy
    sec = 6 * row + 6 - cx if row % 2 == 0 else 6 * row + 1 + cx
    return t, r, sec


def section_label(x, y):
    t, r, s = township_range(x, y)
    return "T%dN R%dW S%02d" % (t, r, s)


def zone2026(x, y):
    if 18 <= x <= 21 and 12 <= y <= 14:
        return "Old Town"
    if 18 <= x <= 22 and 8 <= y <= 11:
        return "Riverside South"
    if 13 <= x <= 17 and 11 <= y <= 16:
        return "Westbrook"
    if (y >= 17 and x >= 10) or (15 <= y <= 16 and x >= 18):
        return "North Bottoms"
    if x <= 12 and y >= 11:
        return "Maple Ridge"
    if (x >= 23 and y <= 14) or (x == 22 and 12 <= y <= 14):
        return "Airport East"
    if 13 <= x <= 22 and 2 <= y <= 10:
        return "South Prairie"
    return "Coulee Hills"


# sections the 1 May 2026 redraw moved, as (x, y) -> zone under the 2025 map
MOVED_2025 = {}
for _x in (13, 14):
    for _y in (2, 3, 4):
        MOVED_2025[(_x, _y)] = "Coulee Hills"          # now South Prairie
for _x in (18, 19):
    MOVED_2025[(_x, 8)] = "South Prairie"              # now Riverside South
for _y in (9, 10, 11):
    MOVED_2025[(22, _y)] = "Airport East"              # now Riverside South
for _x in (18, 19, 20):
    MOVED_2025[(_x, 15)] = "Old Town"                  # now North Bottoms
for _x in (8, 9):
    for _y in (17, 18, 19):
        MOVED_2025[(_x, _y)] = "North Bottoms"         # now Maple Ridge
for _y in (13, 14, 15, 16):
    MOVED_2025[(13, _y)] = "Maple Ridge"               # now Westbrook
for _x in (23, 24):
    MOVED_2025[(_x, 15)] = "Airport East"              # now North Bottoms, no residents affected
for _y in (5, 6):
    MOVED_2025[(12, _y)] = "South Prairie"             # now Coulee Hills


def zone2025(x, y):
    return MOVED_2025.get((x, y), zone2026(x, y))


def centroid(x, y):
    return SW_LAT + (y + 0.5) * DLAT, SW_LON + (x + 0.5) * DLON


def rng(*keys):
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "little"))


def residents():
    """Residents by section, 2025 county estimates."""
    out = {}
    for x in range(NX):
        for y in range(NY):
            g = rng("residents", x, y)
            z = zone2026(x, y)
            if z == "Old Town":
                v = g.uniform(2400, 4100)
            elif z == "Riverside South":
                v = g.uniform(1500, 3100)
            elif z == "Westbrook":
                v = g.uniform(700, 2100) if x >= 14 else g.uniform(250, 700)
            elif z == "North Bottoms":
                v = g.uniform(300, 950) if (15 <= y <= 16) else g.uniform(4, 38)
            elif z == "South Prairie":
                v = g.uniform(550, 1500) if y >= 7 else g.uniform(9, 45)
            elif z == "Airport East":
                v = g.uniform(90, 420) if (9 <= y <= 14 and x <= 25) else g.uniform(6, 30)
            elif z == "Maple Ridge":
                v = g.uniform(500, 900) if (x, y) in ((4, 16), (5, 16), (4, 17), (5, 17)) else g.uniform(7, 40)
            else:
                v = g.uniform(260, 420) if (x, y) in ((5, 4), (6, 4)) else g.uniform(5, 32)
            out[(x, y)] = int(round(v))
    return out


# trap sites: zone -> list of (x, y, habitat, trap type); CO2-baited light traps and, in the two town zones, gravid traps
SITES = {
    "North Bottoms": [(11, 20, "river bottom woods", "CO2"), (14, 21, "oxbow slough", "CO2"), (17, 19, "river bottom woods", "CO2"),
                      (20, 18, "cattail marsh", "CO2"), (23, 20, "farmstead shelterbelt", "CO2"), (26, 22, "river bottom woods", "CO2"),
                      (28, 19, "drainage ditch", "CO2"), (19, 16, "riverside park", "CO2"), (24, 16, "sewage lagoon", "CO2"),
                      (12, 23, "oxbow slough", "CO2"), (21, 21, "flooded pasture", "CO2"), (27, 17, "farmstead shelterbelt", "CO2")],
    "Maple Ridge": [(2, 20, "farmstead shelterbelt", "CO2"), (5, 17, "town park", "CO2"), (8, 22, "prairie pothole", "CO2"),
                    (1, 14, "drainage ditch", "CO2"), (6, 12, "prairie pothole", "CO2"), (10, 14, "farmstead shelterbelt", "CO2"),
                    (4, 23, "cattail marsh", "CO2"), (9, 18, "prairie pothole", "CO2"), (11, 12, "drainage ditch", "CO2"),
                    (3, 16, "town lagoon", "CO2")],
    "Westbrook": [(13, 14, "stormwater pond", "CO2"), (14, 11, "golf course pond", "CO2"), (14, 16, "greenway creek", "CO2"),
                  (15, 13, "greenway creek", "CO2"), (15, 15, "neighbourhood park", "CO2"), (16, 12, "stormwater pond", "CO2"),
                  (16, 14, "greenway creek", "CO2"), (17, 16, "school grounds", "CO2"), (17, 11, "stormwater pond", "CO2"),
                  (13, 12, "farmstead shelterbelt", "CO2"), (16, 16, "cemetery", "CO2"), (14, 13, "stormwater pond", "CO2"),
                  (13, 15, "greenway creek", "CO2"), (17, 13, "school grounds", "CO2"), (15, 11, "neighbourhood park", "CO2")],
    "Old Town": [(18, 12, "riverside park", "CO2"), (19, 13, "alley", "CO2"), (20, 14, "rail yard", "CO2"), (21, 12, "park", "CO2"),
                 (18, 14, "cemetery", "CO2"), (20, 12, "tire yard", "CO2"), (19, 12, "storm drain outfall", "CO2"),
                 (21, 14, "backyard", "CO2"), (18, 13, "riverside park", "CO2"), (21, 13, "alley", "CO2"),
                 (18, 12, "storm drain outfall", "gravid"), (19, 13, "backyard", "gravid"), (20, 13, "alley", "gravid"),
                 (21, 12, "catch basin", "gravid"), (19, 14, "backyard", "gravid"), (20, 12, "tire yard", "gravid"),
                 (18, 14, "catch basin", "gravid"), (21, 14, "backyard", "gravid")],
    "Riverside South": [(18, 8, "riverside park", "CO2"), (19, 10, "backyard", "CO2"), (20, 9, "stormwater pond", "CO2"),
                        (21, 11, "alley", "CO2"), (22, 10, "drainage ditch", "CO2"), (18, 11, "riverside park", "CO2"),
                        (20, 11, "school grounds", "CO2"), (21, 8, "storm drain outfall", "CO2"), (22, 9, "park", "CO2"),
                        (19, 9, "backyard", "CO2"),
                        (18, 9, "catch basin", "gravid"), (19, 11, "backyard", "gravid"), (20, 10, "alley", "gravid"),
                        (21, 9, "catch basin", "gravid"), (22, 11, "backyard", "gravid"), (18, 10, "storm drain outfall", "gravid"),
                        (20, 8, "catch basin", "gravid"), (21, 10, "backyard", "gravid")],
    "South Prairie": [(13, 3, "prairie pothole", "CO2"), (15, 5, "drainage ditch", "CO2"), (17, 7, "stormwater pond", "CO2"),
                      (19, 6, "farmstead shelterbelt", "CO2"), (21, 4, "prairie pothole", "CO2"), (14, 9, "greenway creek", "CO2"),
                      (16, 10, "park", "CO2"), (20, 7, "stormwater pond", "CO2"), (22, 6, "drainage ditch", "CO2"),
                      (18, 3, "cattail marsh", "CO2"), (16, 8, "school grounds", "CO2"), (13, 7, "farmstead shelterbelt", "CO2")],
    "Coulee Hills": [(2, 2, "coulee woods", "CO2"), (5, 4, "village park", "CO2"), (8, 1, "stock pond", "CO2"),
                     (11, 6, "coulee woods", "CO2"), (3, 8, "farmstead shelterbelt", "CO2"), (7, 9, "stock pond", "CO2"),
                     (10, 3, "coulee woods", "CO2"), (1, 6, "drainage ditch", "CO2"), (15, 1, "farmstead shelterbelt", "CO2")],
    "Airport East": [(23, 12, "airport drainage", "CO2"), (25, 10, "industrial pond", "CO2"), (27, 13, "farmstead shelterbelt", "CO2"),
                     (24, 6, "drainage ditch", "CO2"), (26, 3, "prairie pothole", "CO2"), (28, 8, "farmstead shelterbelt", "CO2"),
                     (24, 14, "industrial pond", "CO2"), (29, 1, "drainage ditch", "CO2"), (25, 12, "airport drainage", "CO2")],
}

SPECIES = {  # field database code -> laboratory name
    "CXTA": "Culex tarsalis", "CXPI": "Culex pipiens", "CXSP": "Culex sp.", "AEVE": "Aedes vexans",
    "AEDO": "Aedes dorsalis", "CUIN": "Culiseta inornata", "ANEA": "Anopheles earlei", "AETR": "Aedes trivittatus",
}
VECTORS = ("CXTA", "CXPI")
STATUS = {"OK": "ran set to pickup", "FAN": "fan stopped", "CO2": "dry ice gone before dusk", "BAT": "battery failed",
          "STOLEN": "trap missing at pickup", "NS": "not set"}
FAILED = ("FAN", "CO2", "BAT", "STOLEN")


def site_table():
    """Every trap site with its new ID, legacy code, zone, type, habitat, section and coordinates."""
    rows = []
    g = rng("site-ids")
    ids = list(range(101, 101 + sum(len(v) for v in SITES.values())))
    g.shuffle(ids)
    k = 0
    legacy_no = {}
    for z in ZONES:
        for (x, y, hab, typ) in SITES[z]:
            z25 = zone2025(x, y)
            legacy_no[z25] = legacy_no.get(z25, 0) + 1
            lat, lon = centroid(x, y)
            gg = rng("site-offset", z, x, y, typ)
            lat += gg.uniform(-0.3, 0.3) * DLAT
            lon += gg.uniform(-0.3, 0.3) * DLON
            rows.append(dict(site_id="RC-%d" % ids[k], legacy=("%s-%02d" % (ZCODE[z25], legacy_no[z25])), zone=z, zone2025=z25,
                             trap_type=typ, habitat=hab, x=x, y=y, section=section_label(x, y),
                             lat=round(lat, 5), lon=round(lon, 5)))
            k += 1
    return rows


def week_nights(year, week):
    """The Monday and Tuesday set dates of MMWR week `week` of `year`."""
    jan1 = dt.date(year, 1, 1)
    start = jan1 - dt.timedelta(days=(jan1.weekday() + 1) % 7)
    if (jan1 - start).days > 3:
        start += dt.timedelta(days=7)
    sun = start + dt.timedelta(weeks=week - 1)
    return sun + dt.timedelta(days=1), sun + dt.timedelta(days=2)


def mmwr_week(d):
    jan1 = dt.date(d.year, 1, 1)
    start = jan1 - dt.timedelta(days=(jan1.weekday() + 1) % 7)
    if (jan1 - start).days > 3:
        start += dt.timedelta(days=7)
    return (d - start).days // 7 + 1
