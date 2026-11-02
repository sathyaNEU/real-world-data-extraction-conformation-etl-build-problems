"""World for task459 (architecture 2): Pinyon Valley Health Plan's Senior Choice members in Arizona.

Builds the clean truth: members, their enrollment, their notified addresses, where each one actually
lived on every day of 2025, the providers, pharmacies and home-support agencies, and every service the
plan paid for in 2025. Nothing here is messy; pack.py writes the files the plan's systems would export.
Every random draw comes from one named stream so a change to one part of the world leaves the rest alone.
"""
import datetime as dt
import hashlib

import numpy as np

SEED = 4592026
YEAR_START = dt.date(2025, 1, 1)
YEAR_END = dt.date(2025, 12, 31)
NDAYS = 365
EXTRACT_DATE = dt.date(2026, 1, 2)      # the year-end membership snapshot
DIRECTORY_DATE = dt.date(2026, 10, 1)
BUDGET_2027 = 14_630_000


def stream(name):
    h = int(hashlib.sha256(("%d:%s" % (SEED, name)).encode()).hexdigest()[:12], 16)
    return np.random.default_rng(h)


def day(i):
    return YEAR_START + dt.timedelta(days=int(i))


def doy(d):
    return (d - YEAR_START).days


# ---------------------------------------------------------------------------------------------------------
# Geography. Regions follow Schedule B of the 2027 In-Home Support Agreement; counties and ZIP codes are
# Arizona's own.
REGIONS = [
    ("COC", "Coconino", ["Coconino"]),
    ("YAV", "Yavapai", ["Yavapai"]),
    ("RIM", "Rim Country", ["Gila", "Navajo", "Apache"]),
    ("MAR", "Maricopa", ["Maricopa"]),
    ("PIN", "Pinal", ["Pinal"]),
    ("SAZ", "Southern Arizona", ["Pima", "Santa Cruz", "Cochise"]),
    ("CRV", "Colorado River", ["Mohave", "La Paz", "Yuma"]),
]
REGION_CODES = [r[0] for r in REGIONS]
HIGH = ["COC", "YAV", "RIM"]
DESERT = ["MAR", "PIN", "SAZ", "CRV"]
COUNTY_FIPS = {
    "Apache": "04001", "Cochise": "04003", "Coconino": "04005", "Gila": "04007", "La Paz": "04012",
    "Maricopa": "04013", "Mohave": "04015", "Navajo": "04017", "Pima": "04019", "Pinal": "04021",
    "Santa Cruz": "04023", "Yavapai": "04025", "Yuma": "04027",
}
COUNTY_REGION = {c: code for code, _, cs in REGIONS for c in cs}

# (zip, city, county, weight for members living there)
ZIPS = [
    ("86001", "Flagstaff", "Coconino", 9), ("86004", "Flagstaff", "Coconino", 8), ("86005", "Flagstaff", "Coconino", 5),
    ("86046", "Williams", "Coconino", 2), ("86040", "Page", "Coconino", 1), ("86336", "Sedona", "Coconino", 3),
    ("86301", "Prescott", "Yavapai", 9), ("86303", "Prescott", "Yavapai", 8), ("86305", "Prescott", "Yavapai", 7),
    ("86314", "Prescott Valley", "Yavapai", 8), ("86315", "Prescott Valley", "Yavapai", 6),
    ("86323", "Chino Valley", "Yavapai", 4), ("86326", "Cottonwood", "Yavapai", 6), ("86322", "Camp Verde", "Yavapai", 3),
    ("86351", "Sedona", "Yavapai", 4), ("86333", "Mayer", "Yavapai", 1), ("85332", "Congress", "Yavapai", 1),
    ("85541", "Payson", "Gila", 9), ("85501", "Globe", "Gila", 3), ("85544", "Pine", "Gila", 1),
    ("85901", "Show Low", "Navajo", 7), ("85935", "Pinetop", "Navajo", 4), ("85929", "Lakeside", "Navajo", 3),
    ("85928", "Heber", "Navajo", 2), ("85937", "Snowflake", "Navajo", 2), ("85938", "Springerville", "Apache", 1),
    ("85936", "Saint Johns", "Apache", 1),
    ("85351", "Sun City", "Maricopa", 9), ("85375", "Sun City West", "Maricopa", 8), ("85374", "Surprise", "Maricopa", 6),
    ("85387", "Surprise", "Maricopa", 4), ("85382", "Peoria", "Maricopa", 5), ("85383", "Peoria", "Maricopa", 3),
    ("85308", "Glendale", "Maricopa", 4), ("85032", "Phoenix", "Maricopa", 4), ("85048", "Phoenix", "Maricopa", 3),
    ("85251", "Scottsdale", "Maricopa", 4), ("85255", "Scottsdale", "Maricopa", 3), ("85268", "Fountain Hills", "Maricopa", 3),
    ("85206", "Mesa", "Maricopa", 6), ("85209", "Mesa", "Maricopa", 6), ("85212", "Mesa", "Maricopa", 3),
    ("85248", "Chandler", "Maricopa", 4), ("85295", "Gilbert", "Maricopa", 3), ("85395", "Goodyear", "Maricopa", 3),
    ("85390", "Wickenburg", "Maricopa", 2),
    ("85122", "Casa Grande", "Pinal", 5), ("85132", "Florence", "Pinal", 3), ("85140", "San Tan Valley", "Pinal", 4),
    ("85118", "Gold Canyon", "Pinal", 3), ("85119", "Apache Junction", "Pinal", 4), ("85120", "Apache Junction", "Pinal", 3),
    ("85138", "Maricopa", "Pinal", 2), ("85128", "Coolidge", "Pinal", 1),
    ("85704", "Tucson", "Pima", 4), ("85710", "Tucson", "Pima", 5), ("85715", "Tucson", "Pima", 3), ("85718", "Tucson", "Pima", 3),
    ("85730", "Tucson", "Pima", 3), ("85737", "Oro Valley", "Pima", 4), ("85755", "Oro Valley", "Pima", 3),
    ("85614", "Green Valley", "Pima", 6), ("85622", "Green Valley", "Pima", 4), ("85629", "Sahuarita", "Pima", 2),
    ("85658", "Marana", "Pima", 2), ("85635", "Sierra Vista", "Cochise", 4), ("85650", "Sierra Vista", "Cochise", 2),
    ("85602", "Benson", "Cochise", 1), ("85621", "Nogales", "Santa Cruz", 1), ("85648", "Rio Rico", "Santa Cruz", 1),
    ("86403", "Lake Havasu City", "Mohave", 5), ("86404", "Lake Havasu City", "Mohave", 4), ("86406", "Lake Havasu City", "Mohave", 3),
    ("86442", "Bullhead City", "Mohave", 3), ("86426", "Fort Mohave", "Mohave", 2), ("86401", "Kingman", "Mohave", 3),
    ("85344", "Parker", "La Paz", 1), ("85346", "Quartzsite", "La Paz", 1), ("85365", "Yuma", "Yuma", 3),
    ("85367", "Yuma", "Yuma", 4), ("85364", "Yuma", "Yuma", 2),
]
ZIP_INFO = {z: (city, county) for z, city, county, _ in ZIPS}
# ZIP codes whose delivery area crosses a county line: (zip, [(county, residential share)]).
STRADDLE = {
    "86336": [("Coconino", 0.58), ("Yavapai", 0.42)],
    "86351": [("Yavapai", 1.00)],
    "85390": [("Maricopa", 0.71), ("Yavapai", 0.29)],
    "85118": [("Pinal", 0.94), ("Maricopa", 0.06)],
    "85119": [("Pinal", 0.97), ("Maricopa", 0.03)],
    "85120": [("Pinal", 0.88), ("Maricopa", 0.12)],
    "85737": [("Pima", 0.97), ("Pinal", 0.03)],
}


def zips_in(region):
    return [(z, c, k, w) for z, c, k, w in ZIPS if COUNTY_REGION[k] == region]


# ---------------------------------------------------------------------------------------------------------
# Identifiers.
def luhn_npi(base9):
    """NPI check digit: Luhn over the prefix 80840 and the first nine digits."""
    digits = [int(c) for c in "80840" + base9]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return base9 + str((10 - total % 10) % 10)


def npi_list(rng, n, first):
    out, seen = [], set()
    while len(out) < n:
        b = str(first) + "".join(str(x) for x in rng.integers(0, 10, 8))
        if b in seen:
            continue
        seen.add(b)
        out.append(luhn_npi(b))
    return out


SURNAMES = ["Alvarez", "Baker", "Begay", "Benally", "Brennan", "Castaneda", "Chee", "Delgado", "Dunlap", "Esposito",
            "Fairchild", "Galvan", "Haskie", "Holbrook", "Iverson", "Jaramillo", "Kessler", "Lindqvist", "Lucero",
            "Marchetti", "Moreno", "Nakai", "Okafor", "Pacheco", "Quintero", "Ramaswamy", "Redhouse", "Sandoval",
            "Saenz", "Tsosie", "Underhill", "Valenzuela", "Whitfield", "Yazzie", "Zamora", "Abernathy", "Brightwater",
            "Coldwell", "Dorsey", "Ellingson", "Farrow", "Gutierrez", "Hadley", "Ibarra", "Jessup", "Kowalczyk",
            "Lowery", "Mendoza", "Norquist", "Olivas", "Prentice", "Rasmussen", "Sorensen", "Tafoya", "Ulrich",
            "Villalobos", "Wendt", "Yoder", "Archuleta", "Bustamante", "Calloway", "Duarte", "Engstrom"]
GIVEN = ["Amelia", "Arturo", "Beth", "Carlos", "Dana", "Deepa", "Elena", "Farid", "Gloria", "Hector", "Irene", "Jamal",
         "Karen", "Leon", "Marisol", "Naveen", "Olga", "Pedro", "Rachel", "Ruben", "Selina", "Tomas", "Uma", "Victor",
         "Wendell", "Ximena", "Yusuf", "Zoe", "Anil", "Bruce", "Cora", "Desmond", "Esther", "Felipe", "Grace", "Howard"]


def person_name(rng):
    return "%s %s" % (GIVEN[rng.integers(0, len(GIVEN))], SURNAMES[rng.integers(0, len(SURNAMES))])


# ---------------------------------------------------------------------------------------------------------
# Providers.
class Provider:
    __slots__ = ("npi", "name", "kind", "region", "zip", "city", "county", "pos", "moves", "agency")

    def __init__(self, npi, name, kind, zipcode, pos):
        self.npi = npi
        self.name = name
        self.kind = kind
        self.zip = zipcode
        self.city, self.county = ZIP_INFO[zipcode]
        self.region = COUNTY_REGION[self.county]
        self.pos = pos
        self.moves = []  # (effective date, new zip)
        self.agency = None

    def region_on(self, d):
        z = self.zip_on(d)
        return COUNTY_REGION[ZIP_INFO[z][1]]

    def zip_on(self, d):
        z = self.zip
        for when, nz in self.moves:
            if d >= when:
                z = nz
        return z


AGENCIES = [
    ("COC", "Coconino Home Support Services"),
    ("YAV", "Yavapai Senior In-Home Care"),
    ("RIM", "Rim Country Visiting Nurses Association"),
    ("MAR", "Valley Home Support Partners"),
    ("PIN", "Pinal Community Home Care"),
    ("SAZ", "Desert Willow Caregivers of Southern Arizona"),
    ("CRV", "River Region Home Health Cooperative"),
]

PRACTICE_STEMS = ["Family Medicine", "Internal Medicine Associates", "Primary Care", "Senior Health Center",
                  "Medical Group", "Health Partners", "Family Practice", "Clinic", "Physicians", "Primary Care Group"]
TOWN_PREFIX = {"Flagstaff": "Peaks", "Prescott": "Granite Creek", "Prescott Valley": "Lynx Creek", "Payson": "Rim View",
               "Show Low": "White Mountain", "Sun City": "Bell Road", "Mesa": "East Valley", "Tucson": "Santa Rita",
               "Lake Havasu City": "Havasu Shores", "Casa Grande": "Pinal Central", "Green Valley": "Canoa"}


def build_providers():
    rng = stream("providers")
    provs = {}
    by_region = {r: {"pcp": [], "spec": [], "uc": [], "hosp": [], "pt": [], "img": [], "home": []} for r in REGION_CODES}
    counts = {"COC": (14, 10, 3, 2, 3, 2), "YAV": (30, 18, 4, 3, 5, 3), "RIM": (16, 9, 3, 2, 3, 2),
              "MAR": (44, 34, 9, 6, 8, 6), "PIN": (14, 8, 3, 2, 3, 2), "SAZ": (24, 18, 5, 4, 5, 3),
              "CRV": (11, 7, 3, 2, 2, 2)}
    total = sum(sum(v) for v in counts.values()) + 14
    npis = npi_list(rng, total + 40, 1)
    k = 0
    for r in REGION_CODES:
        zs = zips_in(r)
        zw = np.array([w for *_, w in zs], float)
        zw /= zw.sum()
        npcp, nspec, nuc, nhosp, npt, nimg = counts[r]
        for kind, n, pos in (("pcp", npcp, "11"), ("spec", nspec, "11"), ("uc", nuc, "20"), ("hosp", nhosp, "22"),
                             ("pt", npt, "11"), ("img", nimg, "24")):
            for _ in range(n):
                z = zs[rng.choice(len(zs), p=zw)][0]
                city = ZIP_INFO[z][0]
                if kind == "pcp":
                    if rng.random() < 0.55:
                        name = "%s %s" % (TOWN_PREFIX.get(city, city), PRACTICE_STEMS[rng.integers(0, len(PRACTICE_STEMS))])
                    else:
                        name = "%s, MD" % person_name(rng) if rng.random() < 0.6 else "%s, DO" % person_name(rng)
                elif kind == "spec":
                    sp = ["Cardiology", "Orthopedics", "Ophthalmology", "Urology", "Dermatology", "Pulmonology",
                          "Endocrinology", "Gastroenterology", "Neurology", "Oncology"][rng.integers(0, 10)]
                    name = "%s %s" % (city, sp) if rng.random() < 0.5 else "%s, MD (%s)" % (person_name(rng), sp)
                elif kind == "uc":
                    name = "%s Urgent Care" % city if rng.random() < 0.6 else "%s Walk-In Clinic" % city
                elif kind == "hosp":
                    name = "%s Regional Medical Center Outpatient" % city if rng.random() < 0.5 else "%s Community Hospital" % city
                elif kind == "pt":
                    name = "%s Physical Therapy" % city if rng.random() < 0.6 else "%s Rehab & Sports Therapy" % city
                else:
                    name = "%s Imaging Center" % city if rng.random() < 0.6 else "%s Diagnostic Radiology" % city
                p = Provider(npis[k], name, kind, z, pos)
                k += 1
                provs[p.npi] = p
                by_region[r][kind].append(p)
    # Home-support agencies: one per region, each with a second rendering NPI for its branch office.
    for r, aname in AGENCIES:
        zs = zips_in(r)
        z = zs[0][0]
        p = Provider(npis[k], aname, "home", z, "12")
        k += 1
        p.agency = r
        provs[p.npi] = p
        by_region[r]["home"].append(p)
        z2 = zs[min(len(zs) - 1, 3)][0]
        p2 = Provider(npis[k], aname + " - Branch", "home", z2, "12")
        k += 1
        p2.agency = r
        provs[p2.npi] = p2
        by_region[r]["home"].append(p2)
    # The independent reference laboratory bills from its Phoenix headquarters wherever the draw was taken.
    lab = Provider(npis[k], "Sonoran Reference Laboratories", "lab", "85032", "81")
    k += 1
    provs[lab.npi] = lab
    # Mid-2025 practice relocations across a region line (the provider change log records them).
    movers = []
    for src, dst, when in (("YAV", "MAR", dt.date(2025, 7, 14)), ("PIN", "MAR", dt.date(2025, 4, 1)),
                           ("MAR", "PIN", dt.date(2025, 9, 2)), ("SAZ", "PIN", dt.date(2025, 6, 9)),
                           ("COC", "YAV", dt.date(2025, 8, 18))):
        cand = by_region[src]["spec"]
        p = cand[len(cand) // 2]
        nz = zips_in(dst)[1][0]
        p.moves.append((when, nz))
        movers.append(p.npi)
    return provs, by_region, lab, movers


# ---------------------------------------------------------------------------------------------------------
# Pharmacies.
class Pharmacy:
    __slots__ = ("ncpdp", "name", "kind", "zip", "city", "state", "region")

    def __init__(self, ncpdp, name, kind, zipcode, city, state):
        self.ncpdp = ncpdp
        self.name = name
        self.kind = kind
        self.zip = zipcode
        self.city = city
        self.state = state
        self.region = COUNTY_REGION[ZIP_INFO[zipcode][1]] if state == "AZ" else None


def build_pharmacies():
    rng = stream("pharmacies")
    out = {}
    by_region = {r: [] for r in REGION_CODES}
    used = set()

    def ncpdp(prefix):
        while True:
            v = prefix + "".join(str(x) for x in rng.integers(0, 10, 5))
            if v not in used:
                used.add(v)
                return v

    chains = ["Saguaro Drug", "Canyon Pharmacy", "Mesa Verde Apothecary", "Copper State Pharmacy", "Vista Family Pharmacy"]
    nper = {"COC": 7, "YAV": 14, "RIM": 8, "MAR": 26, "PIN": 8, "SAZ": 14, "CRV": 7}
    for r in REGION_CODES:
        zs = zips_in(r)
        for i in range(nper[r]):
            zw = np.array([x[3] for x in zs], float)
            z, city, county, _ = zs[int(rng.choice(len(zs), p=zw / zw.sum()))]
            if rng.random() < 0.6:
                name = "%s #%d" % (chains[rng.integers(0, len(chains))], 100 + int(rng.integers(0, 880)))
            else:
                name = "%s %s" % (city, ["Pharmacy", "Drug", "Apothecary", "Rx"][rng.integers(0, 4)])
            ph = Pharmacy(ncpdp("03"), name, "retail", z, city, "AZ")
            out[ph.ncpdp] = ph
            by_region[r].append(ph)
    mail = [Pharmacy(ncpdp("17"), "Heartland Mail Service Pharmacy", "mail", "66214", "Lenexa", "KS"),
            Pharmacy(ncpdp("36"), "Lakeshore Home Delivery Pharmacy", "mail", "43017", "Dublin", "OH")]
    spec = [Pharmacy(ncpdp("45"), "Meridian Specialty Pharmacy", "specialty", "75063", "Irving", "TX")]
    for ph in mail + spec:
        out[ph.ncpdp] = ph
    return out, by_region, mail, spec


# ---------------------------------------------------------------------------------------------------------
# Members.
class Member:
    __slots__ = ("mid", "dob", "sex", "kind", "home", "home_zip", "away", "away_zip", "timeline", "addr_hist",
                 "enroll", "pcp", "pcp_hist", "mail_order", "notes", "dod", "moves2026")


def birth_date(rng, age_at_end_lo, age_at_end_hi):
    # Age on 31 Dec 2025 drawn from a declining senior age profile.
    ages = np.arange(age_at_end_lo, age_at_end_hi + 1)
    w = np.exp(-(ages - age_at_end_lo) / 9.0)
    a = int(rng.choice(ages, p=w / w.sum()))
    y = 2025 - a
    d = dt.date(y, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
    return d


def pick_zip(rng, region):
    zs = zips_in(region)
    w = np.array([x[3] for x in zs], float)
    return zs[rng.choice(len(zs), p=w / w.sum())][0]


# 75+ home-region sizes (members aged 75 or older on 31 Dec 2025 enrolled all year, by the address they held
# on 1 Jan 2025), and the movement groups among them.
HOME_SIZES = {"COC": 830, "YAV": 2420, "RIM": 1140, "MAR": 3330, "PIN": 960, "SAZ": 1610, "CRV": 660}
LONG_STAYERS = {"COC": 82, "YAV": 236, "RIM": 104}      # live October to May in the desert, address kept at home
LONG_DEST = {"MAR": 0.44, "PIN": 0.17, "SAZ": 0.23, "CRV": 0.16}
SHORT_WINTER = {"COC": 60, "YAV": 170, "RIM": 75}       # December to March in the desert
SUMMERERS = {"MAR": 260, "PIN": 70, "SAZ": 120, "CRV": 45}  # desert address, June to September in the pines
UNNOTIFIED = {}                                          # (none: every address on file is the member's notified home)
LATE_MOVERS = 74                                        # notified moves between September and November 2025
EARLY_MOVERS = 112                                      # notified moves between January and April 2025


def build_members(provs_by_region):
    rng = stream("members")
    members = []
    seq = [0]

    def new_id():
        seq[0] += 1
        n = 100000 + seq[0] * 37 + int(rng.integers(0, 37))
        body = "%08d" % n
        chk = sum((i + 1) * int(c) for i, c in enumerate(body)) % 10
        return "PVS" + body + str(chk)

    def assign_pcp(region):
        lst = provs_by_region[region]["pcp"]
        w = np.linspace(1.6, 0.4, len(lst))
        return lst[rng.choice(len(lst), p=w / w.sum())].npi

    def base(kind, home, age_lo=75, age_hi=99):
        m = Member()
        m.mid = new_id()
        m.dob = birth_date(rng, age_lo, age_hi)
        m.sex = "F" if rng.random() < 0.56 else "M"
        m.kind = kind
        m.home = home
        m.home_zip = pick_zip(rng, home)
        m.away = None
        m.away_zip = None
        m.timeline = np.full(NDAYS, REGION_CODES.index(home), dtype=np.int8)
        m.enroll = [(dt.date(2015 + int(rng.integers(0, 9)), 1 + int(rng.integers(0, 12)), 1), None)]
        m.addr_hist = [(m.enroll[0][0], m.home_zip, "ENR")]
        m.pcp = assign_pcp(home)
        m.pcp_hist = [(m.enroll[0][0], m.pcp)]
        m.mail_order = rng.random() < 0.18
        m.notes = {}
        m.dod = None
        m.moves2026 = None
        return m

    def set_span(m, start, end, region_idx):
        m.timeline[max(0, start):min(NDAYS, end + 1)] = region_idx

    # Stayers and the groups.
    for home, n in HOME_SIZES.items():
        groups = []
        groups += ["long"] * LONG_STAYERS.get(home, 0)
        groups += ["short"] * SHORT_WINTER.get(home, 0)
        groups += ["summer"] * SUMMERERS.get(home, 0)
        groups += ["unnotified"] * UNNOTIFIED.get(home, 0)
        groups += ["stay"] * (n - len(groups))
        for g in groups:
            m = base(g, home)
            if g == "long":
                dest = list(LONG_DEST)[rng.choice(len(LONG_DEST), p=np.array(list(LONG_DEST.values())))]
                m.away = dest
                m.away_zip = pick_zip(rng, dest)
                # Back home between about 30 May and 12 June, down again between about 18 September and 4 October.
                back = doy(dt.date(2025, 5, 30)) + int(rng.integers(0, 14))
                down = doy(dt.date(2025, 9, 18)) + int(rng.integers(0, 17))
                set_span(m, 0, back - 1, REGION_CODES.index(dest))
                set_span(m, down, NDAYS - 1, REGION_CODES.index(dest))
                m.notes = {"back": back, "down": down}
                m.mail_order = rng.random() < 0.72
            elif g == "short":
                dest = DESERT[rng.choice(4, p=[0.45, 0.17, 0.24, 0.14])]
                m.away = dest
                m.away_zip = pick_zip(rng, dest)
                back = doy(dt.date(2025, 3, 18)) + int(rng.integers(0, 20))
                down = doy(dt.date(2025, 12, 6)) + int(rng.integers(0, 14))
                set_span(m, 0, back - 1, REGION_CODES.index(dest))
                set_span(m, down, NDAYS - 1, REGION_CODES.index(dest))
                m.notes = {"back": back, "down": down}
            elif g == "summer":
                dest = HIGH[rng.choice(3, p=[0.30, 0.45, 0.25])]
                m.away = dest
                m.away_zip = pick_zip(rng, dest)
                up = doy(dt.date(2025, 6, 2)) + int(rng.integers(0, 14))
                down = doy(dt.date(2025, 9, 6)) + int(rng.integers(0, 16))
                set_span(m, up, down - 1, REGION_CODES.index(dest))
                m.notes = {"up": up, "down": down}
            elif g == "unnotified":
                dest = DESERT[rng.choice(4, p=[0.48, 0.18, 0.22, 0.12])]
                m.away = dest
                m.away_zip = pick_zip(rng, dest)
                set_span(m, 0, NDAYS - 1, REGION_CODES.index(dest))
                if rng.random() < 0.55:
                    when = dt.date(2024, 6, 1) + dt.timedelta(days=int(rng.integers(0, 200)))
                    m.pcp = assign_pcp(dest)
                    m.pcp_hist.append((when, m.pcp))
            members.append(m)

    # Notified movers (75+, enrolled all year): early movers spend most of 2025 at the new address, late movers
    # most of it at the old one.
    for i in range(EARLY_MOVERS + LATE_MOVERS):
        late = i >= EARLY_MOVERS
        frm = REGION_CODES[rng.choice(7, p=np.array([0.08, 0.2, 0.1, 0.3, 0.09, 0.15, 0.08]))]
        to = REGION_CODES[rng.choice(7, p=np.array([0.06, 0.14, 0.07, 0.38, 0.12, 0.16, 0.07]))]
        while to == frm:
            to = REGION_CODES[rng.choice(7)]
        m = base("late_mover" if late else "early_mover", frm)
        if late:
            mv = doy(dt.date(2025, 9, 15)) + int(rng.integers(0, 76))
        else:
            mv = doy(dt.date(2025, 1, 10)) + int(rng.integers(0, 80))
        m.away = to
        m.away_zip = pick_zip(rng, to)
        set_span(m, mv, NDAYS - 1, REGION_CODES.index(to))
        notified = day(mv + int(rng.integers(6, 44)))
        if late and notified > dt.date(2025, 12, 20):
            notified = dt.date(2025, 12, 20) - dt.timedelta(days=int(rng.integers(0, 10)))
        m.addr_hist.append((notified, m.away_zip, "MBR"))
        m.notes = {"move": mv}
        if rng.random() < 0.7:
            m.pcp = assign_pcp(to)
            m.pcp_hist.append((day(mv + int(rng.integers(10, 60))) if not late else day(min(NDAYS - 1, mv + int(rng.integers(10, 30)))), m.pcp))
        members.append(m)

    # Members aged 65 to 74 on 31 Dec 2025 (the asks' population), some who turn 75 during 2025 sit above.
    n_young = 5600
    for i in range(n_young):
        home = REGION_CODES[rng.choice(7, p=np.array([0.07, 0.19, 0.09, 0.33, 0.1, 0.15, 0.07]))]
        m = base("young", home, 65, 74)
        if rng.random() < 0.05:
            # a notified move during 2025
            to = REGION_CODES[rng.choice(7)]
            if to != home:
                mv = int(rng.integers(20, 340))
                m.away = to
                m.away_zip = pick_zip(rng, to)
                set_span(m, mv, NDAYS - 1, REGION_CODES.index(to))
                m.addr_hist.append((day(min(NDAYS - 1, mv + int(rng.integers(5, 40)))), m.away_zip, "MBR"))
                m.notes = {"move": mv}
        members.append(m)

    # Members not counted: enrolled part of 2025 (new in 2025, left, or died in 2025).
    for i in range(1350):
        home = REGION_CODES[rng.choice(7, p=np.array([0.07, 0.2, 0.09, 0.32, 0.09, 0.16, 0.07]))]
        m = base("partial", home, 66, 99)
        r = rng.random()
        if r < 0.45:
            start = dt.date(2025, 2 + int(rng.integers(0, 10)), 1)
            m.enroll = [(start, None)]
            m.pcp_hist = [(start, m.pcp)]
            m.addr_hist = [(start, m.home_zip, "ENR")]
        elif r < 0.75:
            m.dod = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(20, 350)))
            m.enroll = [(m.enroll[0][0], m.dod)]
        else:
            end = dt.date(2025, 1 + int(rng.integers(0, 11)), 28)
            m.enroll = [(m.enroll[0][0], end)]
        members.append(m)

    rng2 = stream("members_gaps")
    # A handful of 75+ stayers left the plan for a month or two in 2025 and came back (not enrolled every day).
    stayers = [m for m in members if m.kind == "stay" and m.dod is None and m.enroll[-1][1] is None]
    for i in rng2.choice(len(stayers), size=34, replace=False):
        m = stayers[int(i)]
        off = dt.date(2025, 2 + int(rng2.integers(0, 8)), 28)
        back = dt.date(off.year, off.month, 1) + dt.timedelta(days=int(rng2.choice([35, 63])))
        back = dt.date(back.year, back.month, 1)
        m.enroll = [(m.enroll[0][0], off), (back, None)]
        m.notes = {"gap": (off, back)}
    return members


def enrolled_all_2025(m):
    for s, e in m.enroll:
        if s <= YEAR_START and (e is None or e >= YEAR_END):
            return True
    return False


def age_on(dob, d):
    return d.year - dob.year - ((d.month, d.day) < (dob.month, dob.day))


def alive_end_2025(m):
    return m.dod is None or m.dod > YEAR_END


def counted(m):
    return enrolled_all_2025(m) and age_on(m.dob, YEAR_END) >= 75 and alive_end_2025(m)


def enrolled_on_mask(m):
    """Boolean per day of 2025: enrolled that day (and alive)."""
    mask = np.zeros(NDAYS, dtype=bool)
    for s, e in m.enroll:
        lo = max(0, doy(s)) if s > YEAR_START else 0
        hi = NDAYS - 1 if (e is None or e >= YEAR_END) else doy(e)
        if s > YEAR_END or hi < 0:
            continue
        mask[lo:hi + 1] = True
    if m.dod is not None and m.dod <= YEAR_END:
        mask[doy(m.dod) + 1:] = False
    return mask


def true_region(m):
    """Clean truth: the region in which the member lived on the most days of 2025."""
    c = np.bincount(m.timeline, minlength=7)
    return REGION_CODES[int(np.argmax(c))], c


def address_on(m, d):
    z = None
    for when, zz, _ in sorted(m.addr_hist):
        if when <= d:
            z = zz
    return z if z is not None else m.addr_hist[0][1]


def build_world():
    provs, by_region, lab, movers = build_providers()
    pharm, ph_by_region, mail, spec = build_pharmacies()
    members = build_members(by_region)
    return {"provs": provs, "by_region": by_region, "lab": lab, "movers": movers, "pharm": pharm,
            "ph_by_region": ph_by_region, "mail": mail, "spec": spec, "members": members}
