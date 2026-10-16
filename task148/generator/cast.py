"""Borrowers, guarantors and places: the names the bank's systems hold for each loan's company and its guarantors.

Every borrower is its own company. A single business is guaranteed by its owners; an operator's units are each a
company of their own, guaranteed by the operator, often a spouse or partner, and often the operator's holding company.
The register stores each guarantor's name as typed on each guaranty, with the last four digits of the tax number."""
from __future__ import annotations

import numpy as np

import common as K

FIRST_M = ("James Robert John Michael David William Richard Joseph Thomas Christopher Charles Daniel Matthew Anthony Mark "
           "Donald Steven Paul Andrew Joshua Kenneth Kevin Brian George Timothy Ronald Edward Jason Jeffrey Ryan Jacob Gary "
           "Nicholas Eric Jonathan Stephen Larry Justin Scott Brandon Benjamin Samuel Gregory Alexander Frank Patrick Raymond "
           "Jack Dennis Jerry Tyler Aaron Jose Adam Nathan Henry Douglas Zachary Peter Kyle Ethan Walter Noah Jeremy Christian "
           "Keith Roger Terry Gerald Harold Sean Austin Carl Arthur Lawrence Dylan Jesse Jordan Bryan Billy Joe Bruce Gabriel "
           "Logan Albert Willie Alan Juan Wayne Elijah Randy Roy Vincent Ralph Eugene Russell Bobby Mason Philip Louis Carlos "
           "Luis Miguel Rajesh Vikram Hung Minh Wei Jun Sanjay Ahmed Omar Hector Ramon Victor").split()
FIRST_F = ("Mary Patricia Jennifer Linda Elizabeth Barbara Susan Jessica Sarah Karen Lisa Nancy Betty Margaret Sandra Ashley "
           "Kimberly Emily Donna Michelle Carol Amanda Dorothy Melissa Deborah Stephanie Rebecca Sharon Laura Cynthia Kathleen "
           "Amy Angela Shirley Anna Brenda Pamela Emma Nicole Helen Samantha Katherine Christine Debra Rachel Carolyn Janet "
           "Catherine Maria Heather Diane Ruth Julie Olivia Joyce Virginia Victoria Kelly Lauren Christina Joan Evelyn Judith "
           "Megan Andrea Cheryl Hannah Jacqueline Martha Gloria Teresa Ann Sara Madison Frances Kathryn Janice Jean Abigail "
           "Alice Judy Sophia Grace Denise Amber Doris Marilyn Danielle Beverly Isabella Theresa Diana Natalie Brittany "
           "Charlotte Marie Kayla Alexis Lori Priya Anjali Mei Lan Thuy Yolanda Rosa Carmen Leticia Monica").split()
SURNAMES = ("Smith Johnson Williams Brown Jones Garcia Miller Davis Rodriguez Martinez Hernandez Lopez Gonzalez Wilson "
            "Anderson Thomas Taylor Moore Jackson Martin Lee Perez Thompson White Harris Sanchez Clark Ramirez Lewis Robinson "
            "Walker Young Allen King Wright Scott Torres Nguyen Hill Flores Green Adams Nelson Baker Hall Rivera Campbell "
            "Mitchell Carter Roberts Gomez Phillips Evans Turner Diaz Parker Cruz Edwards Collins Reyes Stewart Morris Morales "
            "Murphy Cook Rogers Gutierrez Ortiz Morgan Cooper Peterson Bailey Reed Kelly Howard Ramos Kim Cox Ward Richardson "
            "Watson Brooks Chavez Wood James Bennett Gray Mendoza Ruiz Hughes Price Alvarez Castillo Sanders Patel Myers Long "
            "Ross Foster Jimenez Powell Jenkins Perry Russell Sullivan Bell Coleman Butler Henderson Barnes Gonzales Fisher "
            "Vasquez Simmons Romero Jordan Patterson Alexander Hamilton Graham Reynolds Griffin Wallace Moreno West Cole Hayes "
            "Bryant Herrera Gibson Ellis Tran Medina Aguilar Stevens Murray Ford Castro Marshall Owens Harrison Fernandez "
            "McDonald Woods Washington Kennedy Wells Vargas Henry Chen Freeman Webb Tucker Guzman Burns Crawford Olson Simpson "
            "Porter Hunter Gordon Mendez Silva Shaw Snyder Mason Dixon Munoz Hunt Hicks Holmes Palmer Wagner Black Robertson "
            "Boyd Rose Stone Salazar Fox Warren Mills Meyer Rice Schmidt Garza Daniels Ferguson Nichols Stephens Soto Weaver "
            "Ryan Gardner Payne Grant Dunn Kelley Spencer Hawkins Arnold Pierce Vazquez Hansen Peters Santos Hart Bradley Knight "
            "Elliott Cunningham Duncan Armstrong Hudson Carroll Lane Riley Andrews Alvarado Ray Delgado Berry Perkins Hoffman "
            "Johnston Matthews Pena Richards Contreras Willis Carpenter Lawrence Sandoval Guerrero George Chapman Rios Estrada "
            "Ortega Watkins Greene Nunez Wheeler Valdez Harper Burke Larson Santiago Maldonado Morrison Franklin Carlson Austin "
            "Dominguez Carr Lawson Jacobs OBrien Lynch Singh Vega Bishop Montgomery Oliver Jensen Harvey Williamson Gilbert "
            "Dean Sims Espinoza Howell Li Wong Reid Hanson Le McCoy Garrett Burton Fuller Wang Weber Welch Rojas Lucas Marquez "
            "Park Yang Little Banks Padilla Day Walsh Bowman Schultz Luna Fowler Mejia Davidson Acosta Brewer May Holland "
            "Juarez Newman Pearson Curtis Cortez Douglas Schneider Joseph Barrett Navarro Figueroa Keller Avila Wade Molina "
            "Stanley Hopkins Campos Barnett Bates Chambers Caldwell Beck Lambert Miranda Byrd Craig Ayala Lowe Frazier Powers "
            "Neal Leonard Gregory Carrillo Sutton Fleming Rhodes Shelton Schwartz Norris Jennings Watts Duran Walters Cohen "
            "McDaniel Moran Parks Steele Vaughn Becker Holt DeLeon Barker Terry Hale Leon Hines Kaur Shah Desai Mehta Huang "
            "Zhang Pham Vo Dang Bui Okafor Adeyemi Haddad Khoury Nasser Rahman Kowalski Novak Lindqvist Petrov Russo Romano "
            "Esposito Bianchi Murillo Cardenas Ochoa Serrano Ibarra Zamora Velasquez Kessler Brennan Gallagher Doyle Quinn "
            "Fitzgerald Hogan Callahan Donovan Kowalczyk Dvorak Hartman Lindgren Sorensen Halvorsen Mueller Fischer Becker "
            "Hofmann Kaiser Stein Weiss Hirsch Levy Goldberg Kaplan Friedman Ashford Pembrook Whitfield Langley Thornton").split()
SURNAMES = list(dict.fromkeys(SURNAMES))
EXCLUDE_FULL = {tuple(n.split()) for n in K.PEOPLE.values()}

TOWNS = [
    ("Ocala", "FL"), ("Gainesville", "FL"), ("Lakeland", "FL"), ("Sarasota", "FL"), ("Port St. Lucie", "FL"),
    ("Tallahassee", "FL"), ("Pensacola", "FL"), ("Melbourne", "FL"), ("Clearwater", "FL"), ("Naples", "FL"),
    ("Savannah", "GA"), ("Macon", "GA"), ("Augusta", "GA"), ("Marietta", "GA"), ("Athens", "GA"), ("Valdosta", "GA"),
    ("Greenville", "SC"), ("Spartanburg", "SC"), ("Columbia", "SC"), ("Charleston", "SC"), ("Rock Hill", "SC"),
    ("Charlotte", "NC"), ("Raleigh", "NC"), ("Wilmington", "NC"), ("Asheville", "NC"), ("Fayetteville", "NC"),
    ("Greensboro", "NC"), ("Hickory", "NC"), ("Richmond", "VA"), ("Roanoke", "VA"), ("Norfolk", "VA"),
    ("Fredericksburg", "VA"), ("Lynchburg", "VA"), ("Knoxville", "TN"), ("Chattanooga", "TN"), ("Murfreesboro", "TN"),
    ("Clarksville", "TN"), ("Jackson", "TN"), ("Huntsville", "AL"), ("Mobile", "AL"), ("Tuscaloosa", "AL"),
    ("Dothan", "AL"), ("Gulfport", "MS"), ("Hattiesburg", "MS"), ("Baton Rouge", "LA"), ("Lafayette", "LA"),
    ("Shreveport", "LA"), ("Lake Charles", "LA"), ("Tyler", "TX"), ("Waco", "TX"), ("Abilene", "TX"),
    ("Lubbock", "TX"), ("Amarillo", "TX"), ("McAllen", "TX"), ("Corpus Christi", "TX"), ("Killeen", "TX"),
    ("Round Rock", "TX"), ("Frisco", "TX"), ("Midland", "TX"), ("San Marcos", "TX"), ("Beaumont", "TX"),
    ("Denton", "TX"), ("Oklahoma City", "OK"), ("Tulsa", "OK"), ("Norman", "OK"), ("Lawton", "OK"),
    ("Little Rock", "AR"), ("Fort Smith", "AR"), ("Springdale", "AR"), ("Wichita", "KS"), ("Topeka", "KS"),
    ("Overland Park", "KS"), ("Springfield", "MO"), ("Columbia", "MO"), ("Joplin", "MO"), ("Lee's Summit", "MO"),
    ("Omaha", "NE"), ("Lincoln", "NE"), ("Des Moines", "IA"), ("Cedar Rapids", "IA"), ("Davenport", "IA"),
    ("Sioux Falls", "SD"), ("Fargo", "ND"), ("Rochester", "MN"), ("St. Cloud", "MN"), ("Duluth", "MN"),
    ("Madison", "WI"), ("Green Bay", "WI"), ("Appleton", "WI"), ("Eau Claire", "WI"), ("Peoria", "IL"),
    ("Rockford", "IL"), ("Naperville", "IL"), ("Champaign", "IL"), ("Joliet", "IL"), ("Fort Wayne", "IN"),
    ("Evansville", "IN"), ("South Bend", "IN"), ("Carmel", "IN"), ("Lansing", "MI"), ("Grand Rapids", "MI"),
    ("Kalamazoo", "MI"), ("Traverse City", "MI"), ("Ann Arbor", "MI"), ("Toledo", "OH"), ("Dayton", "OH"),
    ("Akron", "OH"), ("Canton", "OH"), ("Mansfield", "OH"), ("Erie", "PA"), ("Allentown", "PA"), ("Lancaster", "PA"),
    ("Harrisburg", "PA"), ("Scranton", "PA"), ("State College", "PA"), ("Albany", "NY"), ("Syracuse", "NY"),
    ("Rochester", "NY"), ("Buffalo", "NY"), ("Poughkeepsie", "NY"), ("Utica", "NY"), ("Edison", "NJ"),
    ("Toms River", "NJ"), ("Cherry Hill", "NJ"), ("Stamford", "CT"), ("New Haven", "CT"), ("Hartford", "CT"),
    ("Worcester", "MA"), ("Springfield", "MA"), ("Lowell", "MA"), ("Manchester", "NH"), ("Nashua", "NH"),
    ("Portland", "ME"), ("Burlington", "VT"), ("Warwick", "RI"), ("Wilmington", "DE"), ("Frederick", "MD"),
    ("Hagerstown", "MD"), ("Annapolis", "MD"), ("Charleston", "WV"), ("Morgantown", "WV"), ("Lexington", "KY"),
    ("Bowling Green", "KY"), ("Louisville", "KY"), ("Boise", "ID"), ("Idaho Falls", "ID"), ("Spokane", "WA"),
    ("Tacoma", "WA"), ("Yakima", "WA"), ("Bellingham", "WA"), ("Salem", "OR"), ("Eugene", "OR"), ("Medford", "OR"),
    ("Bend", "OR"), ("Fresno", "CA"), ("Bakersfield", "CA"), ("Modesto", "CA"), ("Stockton", "CA"), ("Riverside", "CA"),
    ("Temecula", "CA"), ("Santa Rosa", "CA"), ("Chico", "CA"), ("Visalia", "CA"), ("Redding", "CA"), ("Ventura", "CA"),
    ("Reno", "NV"), ("Henderson", "NV"), ("Mesa", "AZ"), ("Tucson", "AZ"), ("Flagstaff", "AZ"), ("Yuma", "AZ"),
    ("Albuquerque", "NM"), ("Las Cruces", "NM"), ("Colorado Springs", "CO"), ("Fort Collins", "CO"), ("Pueblo", "CO"),
    ("Grand Junction", "CO"), ("Provo", "UT"), ("Ogden", "UT"), ("St. George", "UT"), ("Billings", "MT"),
    ("Missoula", "MT"), ("Cheyenne", "WY"), ("Casper", "WY"), ("Anchorage", "AK"), ("Honolulu", "HI"),
]
WORDS = ("Summit Harbor Cedar Oak Pine Maple Willow Prairie River Lakeside Ridge Valley Heritage Liberty Pioneer Keystone "
         "Cornerstone Northstar Bluebird Redwood Granite Copper Silverline Golden Coastal Bayside Highland Meadow Sunrise "
         "Evergreen Brookside Stonegate Westfield Eastgate Crossroads Landmark Frontier Horizon Magnolia Juniper Aspen Sterling "
         "Patriot Gateway Riverbend Clearwater Fairway Lighthouse Timberline Sandstone Bridgewater Canyon Mesa Orchard").split()
TRADE = {
    "722511": [("{s}'s Kitchen", 3), ("{p} Grill", 3), ("{w} Bistro", 2), ("{s} Family Restaurant", 2), ("Casa {s}", 1),
               ("{w} Tavern", 2), ("{p} Diner", 2)],
    "722513": [("{p} Burger Co.", 2), ("{s}'s Sandwich Shop", 2), ("{w} Chicken", 1), ("{p} Pizza", 3), ("{s} Subs", 1)],
    "722515": [("{w} Coffee", 3), ("{p} Smoothie Bar", 1), ("{s}'s Donuts", 2), ("{w} Bakery Cafe", 1)],
    "721110": [("{p} Inn & Suites", 3), ("{s} Lodging", 2), ("{w} Motor Lodge", 1), ("{p} Hospitality", 2)],
    "812112": [("{f}'s Salon", 2), ("{w} Hair Studio", 2), ("{p} Salon & Spa", 2)],
    "812111": [("{f}'s Barber Shop", 2), ("{p} Barber Co.", 2)],
    "812320": [("{p} Cleaners", 3), ("{s} Dry Cleaning", 2)],
    "713940": [("{p} Fitness", 3), ("{w} Strength & Conditioning", 1), ("{w} Athletic Club", 1)],
    "611691": [("{p} Learning Academy", 2), ("{w} Tutoring", 2)],
    "624410": [("{w} Learning Center", 3), ("{p} Child Care", 2), ("Little {w} Preschool", 1)],
    "621210": [("{s} Family Dentistry", 3), ("{p} Dental Group", 2), ("{w} Dental Care", 2)],
    "621111": [("{p} Medical Associates", 2), ("{s} Family Medicine", 2)],
    "621340": [("{p} Physical Therapy", 3), ("{w} Rehab & Sports Medicine", 1)],
    "541110": [("{s} & {s2}", 2), ("{s} Law Group", 2), ("Law Office of {f} {s}", 1)],
    "541211": [("{s} CPA Group", 2), ("{s} & {s2} CPAs", 2)],
    "541330": [("{s} Engineering", 2), ("{p} Engineering Associates", 1)],
    "238220": [("{s} Plumbing & Heating", 3), ("{p} Air Conditioning", 2), ("{w} Mechanical", 2)],
    "238210": [("{s} Electric", 3), ("{p} Electrical Contractors", 2)],
    "236118": [("{s} Builders", 2), ("{p} Remodeling", 2), ("{w} Home Improvement", 1)],
    "811111": [("{s} Auto Repair", 3), ("{p} Auto Care", 2), ("{w} Automotive", 2)],
    "811121": [("{p} Collision Center", 3), ("{s} Body Shop", 2)],
    "811192": [("{p} Car Wash", 3), ("{w} Express Wash", 2)],
    "445110": [("{s} Market", 2), ("{p} Fresh Foods", 2)],
    "445120": [("{p} Food Mart", 3), ("{w} Corner Store", 1)],
    "453910": [("{p} Pet Supply", 2), ("{w} Pet Center", 1)],
    "484121": [("{s} Trucking", 3), ("{i} Transport", 2), ("{w} Freight Lines", 1)],
    "484110": [("{s} Hauling", 2), ("{p} Delivery Services", 1), ("{i} Logistics", 2)],
    "423830": [("{p} Industrial Supply", 2), ("{s} Equipment", 2)],
    "332710": [("{s} Machine & Tool", 3), ("{p} Precision", 2)],
    "311811": [("{s} Bakery", 2), ("{w} Bread Co.", 1)],
    "312120": [("{p} Brewing Company", 2), ("{w} Brewery", 2)],
    "561730": [("{s} Landscaping", 3), ("{w} Lawn & Garden", 2)],
    "561720": [("{p} Cleaning Services", 2), ("{w} Janitorial", 2)],
    "531130": [("{p} Self Storage", 3), ("{w} Storage", 2)],
    "623110": [("{p} Care Center", 2), ("{w} Health & Rehabilitation", 1)],
    "624120": [("{p} Home Care", 2), ("{w} Senior Services", 2)],
    "448140": [("{s} Clothiers", 1), ("{w} Apparel", 2)],
    "451110": [("{p} Outfitters", 2), ("{w} Sports", 2)],
    "485310": [("{p} Cab Co.", 2), ("{w} Taxi", 1)],
    "532111": [("{p} Car Rental", 2), ("{w} Rent-A-Car", 1)],
    "512131": [("{p} Cinema", 2), ("{w} Theatres", 1)],
    "713110": [("{p} Family Fun Center", 2), ("{w} Adventure Park", 1)],
}
ENTITY = [("LLC", 9), ("Inc.", 3), ("Inc", 2), ("Corp.", 1), ("LLC", 3), ("L.L.C.", 1)]
PRO = {"621210": ["PLLC", "PC", "DDS PC"], "621111": ["PA", "PLLC"], "541110": ["PLLC", "PC"], "541211": ["PC", "PLLC"]}
OP_BASE = [("{s} Hospitality Group", 3), ("{i} Restaurants", 2), ("{s} Foods", 2), ("{p} QSR Holdings", 1),
           ("{s} Enterprises", 2), ("{s} Family Ventures", 1), ("{w} Brands", 2), ("{i} Management", 1),
           ("{s} & {s2} Partners", 1), ("{w} Operating Group", 1)]
UNIT = [("{b} of {t}", 3), ("{b} {t}", 2), ("{i} {t}", 2), ("{b} {r}", 2), ("{b}-{t}", 1)]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII"]


def _pick(rg, pairs):
    w = np.array([p[1] for p in pairs], float)
    return pairs[int(rg.choice(len(pairs), p=w / w.sum()))][0]


class Person:
    __slots__ = ("first", "middle", "last", "suffix", "tin4", "kind", "party")

    def __init__(self, first, middle, last, suffix, tin4, kind="I", party=""):
        self.first, self.middle, self.last, self.suffix, self.tin4, self.kind = first, middle, last, suffix, tin4, kind
        self.party = party

    def full(self):
        return " ".join(x for x in (self.first, self.middle and self.middle + ".", self.last, self.suffix) if x)


class Cast:
    pass


def build(W):
    """Names for every group and loan of the world: deterministic, its own random stream."""
    rg = K.rng("cast")
    ns = len(SURNAMES)
    zipf = 1.0 / (np.arange(ns) + 8.0) ** 0.9
    zipf /= zipf.sum()
    used_tin = {}

    def person(last=None, female=None):
        while True:
            if female is None:
                female = rg.random() < 0.42
            first = (FIRST_F if female else FIRST_M)[int(rg.integers(0, len(FIRST_F if female else FIRST_M)))]
            last_ = last or SURNAMES[int(rg.choice(ns, p=zipf))]
            if (first, last_) not in EXCLUDE_FULL:
                break
            last = None
        middle = chr(65 + int(rg.integers(0, 26))) if rg.random() < 0.7 else ""
        suffix = ""
        if not female and rg.random() < 0.035:
            suffix = str(rg.choice(["Jr.", "Jr.", "Sr.", "II", "III"]))
        taken = used_tin.setdefault(last_, set())
        while True:
            t4 = "%04d" % int(rg.integers(0, 10000))
            if t4 not in taken:
                taken.add(t4)
                break
        return Person(first, middle, last_, suffix, t4, party=party())

    def town():
        return TOWNS[int(rg.integers(0, len(TOWNS)))]

    def initials(p, q=None):
        # an operator's monogram; a few spell words a reader would stop on, and those use the first and last initial
        if q is None:
            s = p.first[0] + (p.middle or "") + p.last[0]
            return s if s not in ("LLM", "GPT") else p.first[0] + p.last[0]
        s = p.last[0] + q.last[0]
        return s if s != "AI" else q.last[0] + p.last[0]

    def fmt(tmpl, **kw):
        out = tmpl.format(**kw)
        return out.replace("s's ", "s' ").replace("z's ", "z' ")

    pr = K.rng("party")
    party_seen = set()

    def party():
        while True:
            v = "C%08d" % int(pr.integers(10000000, 99999999))
            if v not in party_seen:
                party_seen.add(v)
                return v
    C = Cast()
    C.group_guarantors = {}        # gid -> list of (Person, scope) scope 'all' or a set of loan positions
    C.group_base = {}
    C.loan_name = [None] * W.n
    C.loan_town = [None] * W.n
    by_g = {}
    for i in range(W.n):
        by_g.setdefault(int(W.gid[i]), []).append(i)
    for g in sorted(by_g):
        loans = by_g[g]
        op = bool(W.is_op[g])
        home = town()
        if not op:
            n_g = int(rg.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
            p1 = person()
            ps = [p1]
            for _ in range(n_g - 1):
                if rg.random() < 0.45:
                    ps.append(person(last=p1.last, female=rg.random() < 0.8))
                else:
                    ps.append(person())
            C.group_guarantors[g] = [(p, "all") for p in ps]
            for i in loans:
                nc = W.naics[i]
                p2 = ps[1] if len(ps) > 1 and ps[1].last != p1.last else person()
                name = fmt(_pick(rg, TRADE[nc]), s=p1.last, s2=p2.last, f=p1.first, p=home[0], w=WORDS[int(rg.integers(0, len(WORDS)))],
                           i=initials(p1))
                suf = str(rg.choice(PRO[nc])) if nc in PRO and rg.random() < 0.8 else _pick(rg, ENTITY)
                C.loan_name[i] = "%s %s" % (name, suf)
                C.loan_town[i] = home
        else:
            p1 = person()
            ps = [(p1, "all")]
            spouse = None
            if rg.random() < 0.45:
                spouse = person(last=p1.last if rg.random() < 0.75 else None, female=rg.random() < 0.85)
                ps.append((spouse, "all"))
            q = spouse if spouse is not None and spouse.last != p1.last else person()
            base = fmt(_pick(rg, OP_BASE), s=p1.last, s2=q.last, i=initials(p1), p=home[0],
                       w=WORDS[int(rg.integers(0, len(WORDS)))])
            C.group_base[g] = base
            if rg.random() < 0.55:
                taken = used_tin.setdefault("E|" + base, set())
                while True:
                    t4 = "%04d" % int(rg.integers(0, 10000))
                    if t4 not in taken:
                        taken.add(t4)
                        break
                ent = Person("", "", base + " Holdings", "", t4, kind="E", party=party())
                ps.append((ent, "all"))
            if len(loans) >= 3 and rg.random() < 0.25:
                # a minority partner in some of the units
                part = person()
                pos = set(int(x) for x in rg.choice(len(loans), size=max(1, len(loans) // 3), replace=False))
                ps.append((part, pos))
            C.group_guarantors[g] = ps
            style = _pick(rg, UNIT)
            seen = set()
            for k, i in enumerate(loans):
                t = home if k == 0 or rg.random() < 0.35 else town()
                while True:
                    nm = fmt(style, b=base, t=t[0], i=initials(p1), r=ROMAN[min(k, len(ROMAN) - 1)])
                    if nm not in seen:
                        break
                    t = town()
                seen.add(nm)
                C.loan_name[i] = "%s %s" % (nm, _pick(rg, ENTITY[:3]))
                C.loan_town[i] = t
    C.by_g = by_g
    return C


def typed(rg, p):
    """A guarantor's name as typed on one guaranty: with or without the middle initial, the suffix's form, capitals."""
    if p.kind == "E":
        b = p.last
        return str(rg.choice([b + ", LLC", b + " LLC", b + " LLC", b + ", L.L.C."]))
    mid = p.middle
    form = rg.random()
    if form < 0.55:
        s = " ".join(x for x in (p.first, mid and mid + ".", p.last) if x)
    elif form < 0.80:
        s = "%s %s" % (p.first, p.last)
    elif form < 0.92:
        s = " ".join(x for x in (p.first, mid, p.last) if x)
    else:
        s = " ".join(x for x in (p.first, mid, p.last) if x).upper()
    if p.suffix:
        r = rg.random()
        if r < 0.5:
            s += " " + p.suffix
        elif r < 0.8:
            s += ", " + p.suffix
    return s
