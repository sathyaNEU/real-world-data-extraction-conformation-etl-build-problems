"""The state's law enforcement agencies as the crash records system knows them: the State Patrol and its posts, the
14 sheriffs' offices, the city police departments and the university police. Each has the four-digit code the 2011
crash report used and the agency number the 2024 report uses."""
import world as W

PATROL_ID = "SPHQ000"          # the State Patrol submits to the laboratory under its headquarters number


def _old_code(fips, k):
    return "%02d%02d" % (int(fips) // 2 + 1, k)


class Agency:
    def __init__(self, aid, old, name, kind, fips, post=None, city=None):
        self.aid, self.old, self.name, self.kind, self.fips, self.post, self.city = aid, old, name, kind, fips, post, city

    def __repr__(self):
        return "Agency(%s, %s)" % (self.aid, self.name)


AGENCIES = []
POSTS = {}
SHERIFFS = {}
CITIES = {}

for c in W.COUNTIES:
    f = c["fips"]
    post = W.POST_OF[f]
    a = Agency("SP%02d%03d" % (post, int(f)), "90%02d" % post, "State Patrol Post %d" % post, "State Patrol", f,
               post=post)
    AGENCIES.append(a)
    POSTS[f] = a
    s = Agency("SO%s00" % f, _old_code(f, 1), "%s County Sheriff's Office" % c["name"], "Sheriff", f)
    AGENCIES.append(s)
    SHERIFFS[f] = s
    CITIES[f] = []
    for i, city in enumerate(c["cities"]):
        name = "%s Police Department" % city
        p = Agency("PD%s%02d" % (f, i + 1), _old_code(f, 11 + i), name, "Police Department", f, city=city)
        AGENCIES.append(p)
        CITIES[f].append(p)
UNIV = Agency("UP02701", _old_code("027", 31), "Merrivale State University Police Department, Tanager Campus",
              "University Police", "027", city="Tanager")
AGENCIES.append(UNIV)
CITIES["027"].append(UNIV)

# the city share of each county's city crashes (the first, larger city first)
CITY_WEIGHTS = {2: (0.68, 0.32), 3: (0.55, 0.28, 0.17), 1: (1.0,)}


def patrol_post(fips):
    return POSTS[fips]


def sheriff(fips):
    return SHERIFFS[fips]


def city_pd(fips, rng):
    pds = CITIES[fips]
    if fips == "027":                               # Tanager: the city, Wister, and the campus police
        w = (0.62, 0.26, 0.12)
    else:
        w = CITY_WEIGHTS[len(pds)]
    return pds[int(rng.choice(len(pds), p=w))]


def by_id():
    return {a.aid: a for a in AGENCIES}


def report_prefix(a):
    """The agency's report and case number prefix as its records system writes it: the State Patrol's posts number
    their own (P07), the sheriffs and police departments carry a five-letter prefix."""
    if a.kind == "State Patrol":
        return "P%02d" % a.post
    if a.kind == "Sheriff":
        return W.NAMES[a.fips][:3].upper() + "SO"
    if a.kind == "University Police":
        return "MSUPD"
    return a.city.replace(" ", "")[:3].upper() + "PD"


def case_number(a, year, seq):
    """An agency's report or case number: P07-25-01234 at a State Patrol post, CORSO-25-001234 elsewhere."""
    if a.kind == "State Patrol":
        return "%s-%02d-%05d" % (report_prefix(a), year % 100, seq)
    return "%s-%02d-%06d" % (report_prefix(a), year % 100, seq)


PER_YEAR = {"State Patrol": 2600, "Sheriff": 900, "Police Department": 1500, "University Police": 140}


class Numbers:
    """Each agency numbers every incident it opens through the year (crashes, arrests, other cases) in one sequence;
    a number is drawn near the share of the year gone and never given twice."""
    def __init__(self):
        self.taken = {}

    def next(self, a, day, jitter=0):
        key = (a.aid, day.year)
        seq = max(1, int(PER_YEAR[a.kind] * day.timetuple().tm_yday / 366.0) + jitter)
        used = self.taken.setdefault(key, set())
        while seq in used:
            seq += 1
        used.add(seq)
        return case_number(a, day.year, seq)
