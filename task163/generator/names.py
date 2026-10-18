"""Names, identifiers and attributes for Kilbourne's businesses, built the way a small-business book looks: owners'
surnames, the towns and rivers of each state, trades and professions, the entity suffixes each state's filers use,
sole proprietors filed under the owner's name with a trade name beside it. Nothing here is drawn from one visible pool:
every name mixes several independent parts, and common names repeat across businesses as they do in a real book."""
from __future__ import annotations

SURNAMES = """Smith Johnson Williams Brown Jones Miller Davis Garcia Rodriguez Wilson Martinez Anderson Taylor Thomas
Hernandez Moore Martin Jackson Thompson White Lopez Lee Gonzalez Harris Clark Lewis Robinson Walker Perez Hall Young
Allen Sanchez Wright King Scott Green Baker Adams Nelson Hill Ramirez Campbell Mitchell Roberts Carter Phillips Evans
Turner Torres Parker Collins Edwards Stewart Flores Morris Nguyen Murphy Rivera Cook Rogers Morgan Peterson Cooper Reed
Bailey Bell Gomez Kelly Howard Ward Cox Diaz Richardson Wood Watson Brooks Bennett Gray James Reyes Cruz Hughes Price
Myers Long Foster Sanders Ross Morales Powell Sullivan Russell Ortiz Jenkins Gutierrez Perry Butler Barnes Fisher
Henderson Coleman Simmons Patterson Jordan Reynolds Hamilton Graham Kim Gonzales Alexander Ramos Wallace Griffin West
Cole Hayes Chavez Gibson Bryant Ellis Stevens Murray Ford Marshall Owens McDonald Harrison Ruiz Kennedy Wells Alvarez
Woods Mendoza Castillo Olson Webb Washington Tucker Freeman Burns Henry Vasquez Snyder Simpson Crawford Jimenez Porter
Mason Shaw Gordon Wagner Hunter Romero Hicks Dixon Hunt Palmer Robertson Black Holmes Stone Meyer Boyd Mills Warren Fox
Rose Rice Moreno Schmidt Patel Ferguson Nichols Herrera Medina Ryan Fernandez Weaver Daniels Stephens Gardner Payne
Kelley Dunn Pierce Arnold Tran Spencer Peters Hawkins Grant Hansen Castro Hoffman Hart Elliott Cunningham Knight
Bradley Kowalski Nowak Wisniewski Schneider Becker Schultz Hoffmann Kaminski Lewandowski Yoder Hostetler Troyer Miller
Stoltzfus Beachy Zook Kruse Lindqvist Halvorsen Nyberg Lund Dahl Brandt Vogel Krause Novak Horvath Szabo Varga Petrov
Ivanov Popescu DeLuca Russo Romano Esposito Ricci Marino Greco Bruno Gallo Conti Costa Mancini Moretti Lombardi
Sullivan Doyle Brennan Quinn Gallagher Fitzgerald Byrne Walsh Nolan Kavanagh Okafor Adeyemi Mensah Boateng Haddad
Khoury Nasser Saleh Hussain Rahman Chowdhury Ahmed Singh Kaur Shah Mehta Desai Joshi Iyer Chen Wang Liu Zhang Yang Huang
Zhao Wu Zhou Xu Sun Ma Zhu Hu Lin Guo He Luo Pham Le Hoang Vu Dang Bui Do Ho Ngo Duong Ly""".split()

FIRST = """Mike Dave Steve Tony Joe Rick Linda Maria Rosa Jim Bob Tom Dan Sam Lisa Karen Angela Brenda Carl Frank Gus
Hector Ivan Jorge Kenny Larry Marco Nick Omar Paul Ray Sal Ted Vic Wes Amy Beth Cindy Dee Gina Holly Jill Kim Lori
Nina Patty Rhonda Tina Val Wendy Ahmed Priyanka Mei Hoang Kwame Tasha Darnell Jamal Keisha Shonda Luis Ana Pedro Elena
Rafael Sofia Diego Carmen""".split()

TRADES = [
    # (trade name, NAICS, typical first-employer headcount bias, pay frequency)
    ("Plumbing", "238220", 1.0, "w"), ("Heating & Cooling", "238220", 1.1, "w"), ("Electric", "238210", 1.0, "w"),
    ("Roofing", "238160", 1.2, "w"), ("Painting", "238320", 0.9, "w"), ("Remodeling", "236118", 1.0, "w"),
    ("Construction", "236220", 1.3, "w"), ("Concrete", "238110", 1.2, "w"), ("Landscaping", "561730", 1.1, "w"),
    ("Lawn Care", "561730", 0.9, "w"), ("Tree Service", "561730", 1.1, "w"), ("Cleaning", "561720", 1.2, "b"),
    ("Janitorial", "561720", 1.3, "b"), ("Auto Repair", "811111", 0.9, "w"), ("Auto Body", "811121", 1.0, "w"),
    ("Tire & Service", "811198", 1.0, "w"), ("Trucking", "484110", 1.0, "w"), ("Moving", "484210", 1.1, "w"),
    ("Pizzeria", "722513", 1.6, "w"), ("Grill", "722511", 1.8, "w"), ("Cafe", "722515", 1.4, "b"),
    ("Bakery", "311811", 1.2, "b"), ("Catering", "722320", 1.3, "b"), ("Tavern", "722410", 1.5, "w"),
    ("Salon", "812112", 1.1, "b"), ("Barbershop", "812111", 0.8, "b"), ("Nail Studio", "812113", 1.0, "b"),
    ("Day Spa", "812199", 1.1, "b"), ("Family Dentistry", "621210", 1.4, "s"), ("Chiropractic", "621310", 0.9, "s"),
    ("Physical Therapy", "621340", 1.2, "s"), ("Family Medicine", "621111", 1.5, "s"), ("Home Care", "621610", 1.7, "b"),
    ("Child Care", "624410", 1.6, "b"), ("Learning Center", "611691", 1.0, "b"), ("Tax & Accounting", "541211", 0.8, "s"),
    ("Bookkeeping", "541219", 0.7, "s"), ("Law Office", "541110", 0.8, "s"), ("Insurance Agency", "524210", 0.7, "s"),
    ("Realty", "531210", 0.6, "s"), ("Property Management", "531311", 0.9, "s"), ("Engineering", "541330", 0.9, "s"),
    ("Design Studio", "541430", 0.7, "s"), ("Marketing", "541810", 0.7, "s"), ("IT Services", "541512", 0.8, "s"),
    ("Machine & Tool", "332710", 1.2, "w"), ("Fabrication", "332312", 1.3, "w"), ("Welding", "811310", 1.0, "w"),
    ("Veterinary Clinic", "541940", 1.3, "b"), ("Pet Grooming", "812910", 0.9, "b"), ("Fitness", "713940", 1.0, "b"),
    ("Hardware", "444140", 1.2, "b"), ("Market", "445110", 1.4, "w"), ("Florist", "459310", 0.9, "b"),
    ("Pharmacy", "456110", 1.4, "b"), ("Optometry", "621320", 1.1, "s"), ("Staffing", "561320", 1.0, "w"),
    ("Security", "561612", 1.2, "w"), ("Pest Control", "561710", 0.9, "w"), ("Excavating", "238910", 1.2, "w"),
]

PLACES = {
    "OH": "Maumee Scioto Olentangy Cuyahoga Muskingum Hocking Sandusky Miami Licking Mahoning Tuscarawas Portage Lorain "
          "Medina Fairfield Delaware Clermont Butler Greene Wayne Stark Summit Ashtabula Marietta Zanesville Findlay "
          "Lima Mansfield Canton Kent Westerville Dublin Hilliard Grove City Worthington Bexley Gahanna".split(),
    "PA": "Susquehanna Allegheny Monongahela Lehigh Schuylkill Juniata Lancaster Chester Bucks Berks Erie Cumberland "
          "Dauphin Lebanon York Centre Blair Luzerne Lackawanna Westmoreland Beaver Butler Washington Mercer "
          "Altoona Reading Scranton Hershey Carlisle Doylestown Media Wyomissing".split(),
    "MI": "Huron Saginaw Kalamazoo Grand River Thunder Bay Traverse Lakeshore Muskegon Oakland Macomb Washtenaw "
          "Ingham Kent Ottawa Genesee Livingston Monroe Jackson Calhoun Midland Bay Petoskey Holland Ann Arbor "
          "Ypsilanti Novi Troy Lansing Okemos Marquette".split(),
    "IN": "Wabash Tippecanoe Hoosier Kankakee Whitewater Hamilton Marion Allen Elkhart Monroe Vigo Delaware Porter "
          "Lake Carmel Fishers Noblesville Bloomington Lafayette Muncie Kokomo Valparaiso".split(),
    "MN": "Mississippi Minnetonka Superior Itasca Hennepin Dakota Anoka Stearns Olmsted Wright Scott Duluth "
          "Rochester Mankato Edina Bloomington Woodbury Eagan".split(),
    "WI": "Fox River Kettle Moraine Door Dane Waukesha Brown Outagamie Racine Kenosha Marathon Rock La Crosse "
          "Eau Claire Oshkosh Appleton Sheboygan Madison Brookfield".split(),
    "KY": "Bluegrass Licking Kentucky River Cumberland Green River Boone Kenton Fayette Jefferson Warren Daviess "
          "Hardin Madison Bowling Green Florence Covington Frankfort Paducah".split(),
    "WV": "Kanawha Greenbrier Monongalia Cabell Berkeley Raleigh Wood Harrison Mercer Marion Huntington Morgantown "
          "Charleston Parkersburg Beckley Wheeling".split(),
    "TN": "Cumberland Smoky Mountain Volunteer Davidson Knox Shelby Hamilton Rutherford Williamson Sumner Sevier "
          "Franklin Murfreesboro Chattanooga Knoxville Johnson City Jackson Clarksville".split(),
    "MO": "Ozark Gateway Meramec Show-Me Jackson Boone Greene Jefferson Cass Platte Clay Joplin Columbia "
          "Springfield Branson Lee's Summit Chesterfield Kirkwood".split(),
    "IA": "Hawkeye Cedar Des Moines Raccoon Polk Linn Scott Johnson Story Dubuque Woodbury Ames Ankeny Davenport "
          "Iowa City Waterloo Cedar Falls".split(),
    "VA": "Shenandoah Blue Ridge Rappahannock James River Piedmont Tidewater Fairfax Loudoun Henrico Chesterfield "
          "Roanoke Albemarle Augusta Prince William Arlington Leesburg Fredericksburg Lynchburg Harrisonburg".split(),
}

ADJ = """Precision Summit Premier Reliable Quality Advanced Superior Pioneer Heritage Liberty Keystone Frontier
Riverside Northside Southside Eastside Westside Hometown Main Street Lakeview Valley Ridge Prairie Cardinal
Buckeye Golden Silver Oak Maple Cedar Pine Elm Willow Stonebridge Brookside Harbor Crossroads Allied United
Integrity Northstar Trailhead Bright Clear Fresh Green Blue Red Iron Copper Granite""".split()

SUFFIX = {"LLC": ["LLC", "LLC", "LLC", "L.L.C.", "Llc", "LLC"], "INC": ["Inc.", "Inc", "Inc.", "Corporation", "Corp."],
          "PLLC": ["PLLC", "PLLC", "P.L.L.C."], "LP": ["LP", "Ltd."]}

PROFESSIONAL = {"Family Dentistry", "Chiropractic", "Physical Therapy", "Family Medicine", "Tax & Accounting",
                "Law Office", "Engineering", "Veterinary Clinic", "Optometry"}

PREV_PROVIDERS = ["national payroll provider", "national payroll provider", "national payroll provider",
                  "online payroll software", "online payroll software", "accounting firm", "accounting firm",
                  "bank payroll service", "regional payroll bureau", "self-run (desktop software)",
                  "self-run (manual checks)", "PEO"]
CHANNELS = ["accountant referral", "accountant referral", "web sign-up", "web sign-up", "web sign-up",
            "bank partner", "outbound", "partner marketplace"]


def _pick(r, seq):
    return seq[int(r.integers(0, len(seq)))]


def _trade(r):
    return TRADES[int(r.integers(0, len(TRADES)))]


def _entity(r, kind, trade):
    u = r.random()
    if trade[0] in PROFESSIONAL and u < 0.45:
        return "PLLC"
    if kind == "first":
        return "LLC" if u < 0.66 else ("SOLE" if u < 0.86 else ("INC" if u < 0.97 else "LP"))
    if kind == "inhouse":
        return "LLC" if u < 0.50 else ("SOLE" if u < 0.78 else ("INC" if u < 0.96 else "LP"))
    return "LLC" if u < 0.52 else ("INC" if u < 0.82 else ("SOLE" if u < 0.95 else "LP"))


def _core(r, state, trade):
    """The business's trading name, from one of several independent constructions."""
    u = r.random()
    t = trade[0]
    if u < 0.30:
        return "%s %s" % (_pick(r, SURNAMES), t)
    if u < 0.48:
        return "%s %s" % (_pick(r, PLACES[state]), t)
    if u < 0.58:
        a, b = _pick(r, "ABCDEFGHJKLMNPRSTW"), _pick(r, "ABCDEFGHJKLMNPRSTW")
        return ("%s&%s %s" % (a, b, t)) if r.random() < 0.6 else ("%s%s%s %s" % (a, b, _pick(r, "ABCDEFGHJKLMNPRSTW"), t))
    if u < 0.70:
        return "%s's %s" % (_pick(r, FIRST), t)
    if u < 0.88:
        return "%s %s" % (_pick(r, ADJ), t)
    if u < 0.95:
        return "%s & %s %s" % (_pick(r, SURNAMES), _pick(r, SURNAMES), t)
    return "%s %s %s" % (_pick(r, SURNAMES), "Family", t)


def _legal(r, core, entity, state):
    if entity == "SOLE":
        return "%s %s" % (_pick(r, FIRST), _pick(r, SURNAMES)), core
    suf = _pick(r, SUFFIX[entity if entity in SUFFIX else "LLC"])
    joiner = ", " if r.random() < 0.35 and suf in ("LLC", "Inc.", "Inc") else " "
    legal = "%s%s%s" % (core, joiner, suf)
    dba = "" if r.random() < 0.7 else core
    return legal, dba


def business(r, state, kind):
    tr = _trade(r)
    ent = _entity(r, kind, tr)
    core = _core(r, state, tr)
    legal, dba = _legal(r, core, ent, state)
    if kind == "first":
        emp = 1 + int(r.geometric(0.62) - 1) + (1 if r.random() < 0.18 * tr[2] else 0)
        growth = 0.10 + 0.12 * r.random()
    elif kind == "inhouse":
        # a small employer that ran its own payroll on desktop software or by hand
        emp = 1 + int(r.geometric(0.45) - 1) + (1 if r.random() < 0.25 * tr[2] else 0)
        growth = 0.02 + 0.07 * r.random()
    else:
        emp = max(2, int(round(r.lognormal(1.75, 0.65) * tr[2])))
        growth = 0.01 + 0.05 * r.random()
    wage = float(round(r.lognormal(9.15, 0.22), 2))           # quarterly gross wages per employee, about $9,400
    return {"name": legal, "dba": dba, "entity": ent, "naics": tr[1], "employees": int(emp), "wage": wage,
            "growth": growth, "trade": tr[0]}


def successor_of(r, b):
    """The new entity a business forms: a sole proprietor incorporates under the trade name, a partnership becomes an
    LLC, an LLC or a corporation changes its form under the same name. About one in eight moves the business into a
    new holding entity under another name, and the trade name carries over."""
    trade_name = b.dba or (b.name.split(",")[0].rsplit(" ", 1)[0] if b.entity != "SOLE" else b.name)
    basis = "change of entity"
    if b.entity == "SOLE":
        ent = "LLC" if r.random() < 0.7 else "INC"
        core = b.dba or b.name
    elif b.entity == "LP":
        ent = "LLC"
        core = trade_name
    else:
        ent = "INC" if b.entity == "LLC" else "LLC"
        if r.random() < 0.88:
            core = trade_name
        else:
            core = "%s %s" % (_pick(r, SURNAMES), _pick(r, ["Holdings", "Group", "Enterprises", "Partners"]))
            basis = "reorganisation"
    suf = _pick(r, SUFFIX[ent])
    legal = "%s %s" % (core, suf)
    if basis == "reorganisation":
        dba = trade_name
    else:
        dba = (b.dba or core) if r.random() < 0.6 else ""
    return {"name": legal, "dba": dba, "entity": ent, "basis": basis}


ONLINE_PREFIX = ["88", "92", "93", "99", "87", "86", "85", "84", "83", "82", "81", "47", "46", "45", "27", "26", "20",
                 "30", "32", "33", "36", "37", "38", "39"]
OLD_PREFIX = ["31", "34", "35", "38", "61", "62", "20", "26", "27", "35", "36", "41", "42", "43", "47", "51", "52",
              "54", "55", "56", "57", "58", "59", "65", "71", "72", "73", "74", "75", "76", "77", "80", "90", "91",
              "94", "95", "98", "04", "06", "01", "02"]


def ein(r, b, old=False):
    """Nine digits. A new entity applies online almost always; an established business may hold a number a campus
    issued from a mailed or faxed application."""
    recent = b.kind in ("first", "successor", "succ_ext")
    online = r.random() < ((0.95 if recent else 0.64) if not old else 0.55)
    pref = _pick(r, ONLINE_PREFIX if online else OLD_PREFIX)
    return "%s%07d" % (pref, int(r.integers(0, 10 ** 7)))


def legacy_number(r, bid, k):
    return "%d%05d" % (4 + (bid % 5), (bid * 37 + k * 11) % 100000)


def account_id(r, bid, k):
    return "KP%07d" % (1000000 + (bid * 7919 + k * 104729) % 9000000)


def provider(r, b, k):
    if k > 0:
        return "Kilbourne (prior account)"
    return _pick(r, PREV_PROVIDERS)


def channel(r, b):
    return _pick(r, CHANNELS)


FREQ = {t[0]: t[3] for t in TRADES}


def frequency(b):
    # derived from the trade's usual pay schedule; the trade is not stored, so read it from the NAICS map
    for t in TRADES:
        if t[1] == b.naics:
            return t[3]
    return "b"
