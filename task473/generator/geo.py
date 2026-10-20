"""Where things are: each county's place on the map, its neighbours, its roads, and the places blood is drawn (the
hospitals, the county jails and the coroners' and medical examiner's offices), with the laboratory's site codes."""
import world as W

# the counties on a grid of rows (north to south) and columns (west to east)
GRID = {"001": (0, 0), "003": (0, 1), "005": (0, 2), "007": (0, 3),
        "017": (1, 0), "011": (1, 1), "015": (1, 2), "013": (1, 3),
        "009": (2, 0), "019": (2, 1), "021": (2, 2), "023": (2, 3),
        "025": (3, 0), "027": (3, 1)}
LAT0, LON0, DLAT, DLON = 40.42, -95.36, 0.58, 0.74


def box(fips):
    r, c = GRID[fips]
    north = LAT0 - DLAT * r
    west = LON0 + DLON * c
    return north - DLAT, north, west, west + DLON


def neighbours(fips):
    r, c = GRID[fips]
    return sorted(f for f, (r2, c2) in GRID.items() if f != fips and abs(r - r2) + abs(c - c2) == 1)


# state highways through each county (route numbers), the interstates first
INTERSTATES = {"001": ["I-29"], "017": ["I-29"], "009": ["I-29"], "025": ["I-29"],
               "011": ["I-70"], "015": ["I-70"], "013": ["I-70", "I-435"],
               "019": ["I-49"], "027": ["I-49"], "003": ["I-49"]}
US_ROUTES = {"001": ["US 136"], "003": ["US 136", "US 69"], "005": ["US 136", "US 65"], "007": ["US 63"],
             "017": ["US 36"], "011": ["US 36", "US 69"], "015": ["US 36", "US 65"], "013": ["US 36", "US 24"],
             "009": ["US 50"], "019": ["US 50", "US 71"], "021": ["US 50", "US 65"], "023": ["US 63", "US 54"],
             "025": ["US 160"], "027": ["US 160", "US 71"]}
STATE_ROUTES = {f: ["SR %d" % (10 + 7 * i + k) for k in range(3)] for i, f in enumerate(sorted(GRID))}
STREETS = ["Main St", "Market St", "Oak St", "Elm St", "Washington Ave", "Broadway", "College Ave", "Grand Ave",
           "Lincoln Ave", "Maple St", "Park Ave", "Church St", "Walnut St", "Pine St", "2nd St", "3rd St", "4th St",
           "5th St", "Front St", "Water St", "Highland Ave", "Jackson St", "Locust St", "Mill St", "Spring St",
           "Union St", "Vine St", "Center St", "Railroad Ave", "Cedar St"]
COUNTY_ROADS = ["CR %d" % n for n in (110, 125, 140, 155, 170, 210, 235, 250, 275, 310, 340, 360, 410, 455)]


def state_highways(fips):
    return INTERSTATES.get(fips, []) + US_ROUTES[fips] + STATE_ROUTES[fips]


# ---------------------------------------------------------------------------------------------------------------
# The laboratory's collection sites: every hospital that draws blood for the police, every county jail, and the
# offices that submit death investigation specimens. Aldous and Kittredge have no hospital: their arrests are drawn
# at the jail or across the line.
# ---------------------------------------------------------------------------------------------------------------
class Site:
    def __init__(self, code, name, kind, fips, city):
        self.code, self.name, self.kind, self.fips, self.city = code, name, kind, fips, city


SITES = []
HOSPITALS = {}
JAILS = {}
CORONERS = {}
for i, c in enumerate(W.COUNTIES):
    f = c["fips"]
    city = c["cities"][0]
    if c["hospital"]:
        h = Site("%04d" % (1100 + 17 * i), c["hospital"], "Hospital", f, city)
        SITES.append(h)
        HOSPITALS[f] = [h]
    j = Site("%04d" % (3100 + 13 * i), "%s County Detention Center" % c["name"], "Jail", f, city)
    SITES.append(j)
    JAILS[f] = j
    co = Site("%04d" % (5100 + 11 * i), "%s County Coroner" % c["name"], "Coroner", f, city)
    SITES.append(co)
    CORONERS[f] = co
# second hospitals in the larger counties
for f, name, city in (("013", "Ludlow Park Community Hospital", "Ludlow Park"),
                      ("009", "Westmark Regional Medical Center", "Westmark"),
                      ("021", "Linn Grove Hospital", "Linn Grove"),
                      ("007", "Sauls Ferry Medical Center", "Sauls Ferry")):
    h = Site("%04d" % (1400 + len(SITES)), name, "Hospital", f, city)
    SITES.append(h)
    HOSPITALS[f].append(h)
ME = Site("5900", "Office of the State Medical Examiner", "Medical Examiner", "013", "Kessington")
SITES.append(ME)
BY_CODE = {s.code: s for s in SITES}


def draw_sites(fips):
    """Where an arrest in the county is drawn: its own hospitals and jail, or a neighbour's hospital."""
    own = HOSPITALS.get(fips, []) + [JAILS[fips]]
    nb = [h for n in neighbours(fips) for h in HOSPITALS.get(n, [])]
    return own, nb
