"""The aircraft: register reference tables (models, engines), N-numbers and their 24-bit addresses, owners, the based
fleet at each field and its hidden attributes (broadcasts ADS-B Out or not, school or charter use), and the register's
history in 2026 (N-number changes, a charter operator moving its fleet numbers to new aircraft, exports).
"""
import datetime as dt

import numpy as np

import world as W

CHARSET = "ABCDEFGHJKLMNPQRSTUVWXYZ"
DIGITSET = "0123456789"
_SUFFIX = 1 + len(CHARSET) * (1 + len(CHARSET))
_B4 = 1 + len(CHARSET) + len(DIGITSET)
_B3 = len(DIGITSET) * _B4 + _SUFFIX
_B2 = len(DIGITSET) * _B3 + _SUFFIX
_B1 = len(DIGITSET) * _B2 + _SUFFIX


def _suffix_offset(s):
    if not s:
        return 0
    off = CHARSET.index(s[0]) * (len(CHARSET) + 1) + 1
    if len(s) == 2:
        off += CHARSET.index(s[1]) + 1
    return off


def icao_hex(n):
    """The US civil 24-bit address of an N-number (A00001 for N1 to ADF7C7 for N99999)."""
    n = n.upper()
    if n.startswith("N"):
        n = n[1:]
    out = 0xA00001 + (int(n[0]) - 1) * _B1
    rest = n[1:]
    buckets = [_B2, _B3, _B4]
    for i, c in enumerate(rest):
        if c in CHARSET:
            if i == 3:
                return "%06X" % (out + CHARSET.index(c) + 1)
            return "%06X" % (out + _suffix_offset(rest[i:]))
        if i == 3:
            return "%06X" % (out + 1 + len(CHARSET) + int(c))
        out += _SUFFIX + int(c) * buckets[i]
    return "%06X" % out


assert icao_hex("N1") == "A00001" and icao_hex("N99999") == "ADF7C7" and icao_hex("N12345") == "A061D9"

# engines: code, manufacturer, model, type (1 reciprocating, 2 turbo-prop, 3 turbo-shaft, 5 turbo-fan), hp, thrust
ENGINES = [
    ("17003", "CONT MOTOR", "A-65 SERIES", 1, 65, 0), ("17005", "CONT MOTOR", "C-85-12", 1, 85, 0),
    ("17008", "CONT MOTOR", "O-200-A", 1, 100, 0), ("17026", "CONT MOTOR", "IO-550-N", 1, 310, 0),
    ("17030", "CONT MOTOR", "IO-550-C", 1, 300, 0), ("17012", "CONT MOTOR", "O-470-U", 1, 230, 0),
    ("41514", "LYCOMING", "O-320-D2J", 1, 160, 0), ("41520", "LYCOMING", "O-360-A4M", 1, 180, 0),
    ("41525", "LYCOMING", "IO-360-L2A", 1, 180, 0), ("41531", "LYCOMING", "IO-540-K1G5", 1, 300, 0),
    ("41536", "LYCOMING", "TIO-540-A2C", 1, 310, 0), ("41541", "LYCOMING", "O-360-A1H6", 1, 180, 0),
    ("41544", "LYCOMING", "O-290-D2", 1, 135, 0), ("41503", "LYCOMING", "O-235-L2C", 1, 118, 0),
    ("41548", "LYCOMING", "IO-390-A3A6", 1, 210, 0), ("71106", "ROTAX", "912 ULS", 1, 100, 0),
    ("52012", "P&W CANADA", "PT6A-42", 2, 850, 0), ("52020", "P&W CANADA", "PT6A-67P", 2, 1200, 0),
    ("52031", "P&W CANADA", "PT6A-114A", 2, 675, 0), ("52044", "P&W CANADA", "PW535A", 5, 0, 3360),
    ("78005", "WILLIAMS", "FJ44-3A", 5, 0, 2820), ("62040", "ROLLS-ROYC", "250-C47B", 3, 650, 0),
    ("29501", "TURBOMECA", "ARRIEL 2B1", 3, 847, 0),
]
ENGINE_BY_CODE = {e[0]: e for e in ENGINES}

# models: code, manufacturer, model, type-acft (1 glider, 4 single, 5 multi, 6 rotorcraft), type-eng, engines,
# seats, build certification (0 type certificated, 1 experimental, 2 light sport), engine code, family, broadcast
# probability for a private owner, year range
MODELS = [
    ("2072738", "CESSNA", "172S", 4, 1, 1, 4, 0, "41520", "modern", 0.94, (1999, 2019)),
    ("2072706", "CESSNA", "172N", 4, 1, 1, 4, 0, "41514", "modern", 0.90, (1977, 1980)),
    ("2073006", "CESSNA", "182T", 4, 1, 1, 4, 0, "17012", "modern", 0.95, (2001, 2018)),
    ("2071206", "CESSNA", "152", 4, 1, 1, 2, 0, "41503", "modern", 0.88, (1978, 1985)),
    ("2073505", "CESSNA", "T210N", 4, 1, 1, 6, 0, "17026", "modern", 0.95, (1979, 1985)),
    ("7102810", "PIPER", "PA-28-181", 4, 1, 1, 4, 0, "41520", "modern", 0.92, (1976, 2016)),
    ("7102805", "PIPER", "PA-28-161", 4, 1, 1, 4, 0, "41514", "modern", 0.90, (1977, 1998)),
    ("7103215", "PIPER", "PA-32R-301", 4, 1, 1, 6, 0, "41531", "modern", 0.95, (1980, 2006)),
    ("1150120", "CIRRUS DESIGN CORP", "SR20", 4, 1, 1, 4, 0, "17030", "modern", 0.99, (2001, 2021)),
    ("1150122", "CIRRUS DESIGN CORP", "SR22", 4, 1, 1, 4, 0, "17026", "modern", 0.99, (2002, 2022)),
    ("0560416", "BEECH", "A36", 4, 1, 1, 6, 0, "17026", "modern", 0.96, (1972, 2004)),
    ("6070105", "MOONEY", "M20J", 4, 1, 1, 4, 0, "41525", "modern", 0.93, (1977, 1997)),
    ("1351408", "DIAMOND", "DA 40", 4, 1, 1, 4, 0, "41525", "modern", 0.99, (2002, 2020)),
    ("05628KW", "VANS", "RV-7A", 4, 1, 1, 2, 1, "41541", "modern", 0.92, (2004, 2021)),
    ("7100210", "PIPER", "J3C-65", 4, 1, 1, 2, 0, "17003", "vintage", 0.18, (1938, 1947)),
    ("0182001", "AERONCA", "7AC", 4, 1, 1, 2, 0, "17003", "vintage", 0.22, (1946, 1948)),
    ("8640011", "TAYLORCRAFT", "BC12-D", 4, 1, 1, 2, 0, "17003", "vintage", 0.20, (1941, 1947)),
    ("5320006", "LUSCOMBE", "8A", 4, 1, 1, 2, 0, "17003", "vintage", 0.25, (1946, 1948)),
    ("2070104", "CESSNA", "140", 4, 1, 1, 2, 0, "17005", "vintage", 0.33, (1946, 1950)),
    ("2070102", "CESSNA", "120", 4, 1, 1, 2, 0, "17005", "vintage", 0.30, (1946, 1949)),
    ("3770102", "ERCO", "415-C", 4, 1, 1, 2, 0, "17005", "vintage", 0.28, (1946, 1948)),
    ("8310108", "STINSON", "108-3", 4, 1, 1, 4, 0, "17012", "vintage", 0.40, (1947, 1949)),
    ("7101822", "PIPER", "PA-18-150", 4, 1, 1, 2, 0, "41541", "vintage", 0.55, (1955, 1982)),
    ("7102205", "PIPER", "PA-22-150", 4, 1, 1, 4, 0, "41544", "vintage", 0.45, (1955, 1960)),
    ("7104402", "PIPER", "PA-44-180", 5, 1, 2, 4, 0, "41520", "twin", 0.97, (1979, 2015)),
    ("0566012", "BEECH", "58", 5, 1, 2, 6, 0, "17026", "twin", 0.97, (1976, 2010)),
    ("7103405", "PIPER", "PA-34-200T", 5, 1, 2, 6, 0, "17026", "twin", 0.95, (1975, 1981)),
    ("7103106", "PIPER", "PA-31-350", 5, 1, 2, 8, 0, "41536", "twin", 0.99, (1975, 1984)),
    ("2073905", "CESSNA", "310R", 5, 1, 2, 6, 0, "17026", "twin", 0.94, (1975, 1981)),
    ("0569020", "BEECH", "B200", 5, 2, 2, 9, 0, "52012", "turbine", 1.0, (1985, 2010)),
    ("6440012", "PILATUS", "PC-12/47E", 4, 2, 1, 9, 0, "52020", "turbine", 1.0, (2008, 2021)),
    ("2074520", "CESSNA", "208B", 4, 2, 1, 11, 0, "52031", "turbine", 1.0, (1995, 2019)),
    ("2075340", "CESSNA", "525B", 5, 5, 2, 8, 0, "78005", "turbine", 1.0, (2005, 2019)),
    ("1370512", "EMBRAER", "EMB-505", 5, 5, 2, 9, 0, "52044", "turbine", 1.0, (2010, 2021)),
    ("0313004", "AIRBUS HELICOPTERS", "AS350B3", 6, 3, 1, 6, 0, "29501", "helo", 1.0, (2004, 2020)),
    ("1182010", "BELL", "407", 6, 3, 1, 7, 0, "62040", "helo", 1.0, (1998, 2018)),
    ("0670038", "SCHWEIZER", "SGS 2-33A", 1, 0, 0, 2, 0, "", "glider", 0.10, (1967, 1980)),
    ("7102508", "PIPER", "PA-25-235", 4, 1, 1, 1, 0, "41531", "towplane", 0.98, (1965, 1978)),
]
MODEL_BY_CODE = {m[0]: m for m in MODELS}
FAMILY = {}
for m in MODELS:
    FAMILY.setdefault(m[9], []).append(m[0])

FIRST = ["James", "Mary", "Robert", "Patricia", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara",
         "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
         "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley", "Steven",
         "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle", "Kenneth", "Carol", "Kevin", "Amanda",
         "Gary", "Melissa", "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
         "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Larry", "Amy", "Frank", "Shirley", "Scott",
         "Angela", "Eric", "Helen", "Stephen", "Anna", "Raymond", "Pamela", "Gregory", "Nicole", "Samuel", "Emma",
         "Benjamin", "Samantha", "Patrick", "Katherine", "Dennis", "Christine", "Jerry", "Debra", "Walter", "Rachel",
         "Harold", "Carolyn", "Douglas", "Janet", "Henry", "Catherine", "Carl", "Maria", "Arthur", "Heather"]
LAST = ["Abernathy", "Ackerly", "Aldridge", "Ambler", "Ashworth", "Bancroft", "Barlow", "Beckett", "Birchall",
        "Blackwood", "Bradshaw", "Brennan", "Calloway", "Carver", "Chandler", "Colburn", "Corrigan", "Cutler",
        "Dalton", "Davenport", "Delacroix", "Dempsey", "Draper", "Eastman", "Ellery", "Emerson", "Farrell",
        "Fenwick", "Finley", "Fletcher", "Garland", "Gentry", "Goodwin", "Grantham", "Hadley", "Halloran",
        "Hargrove", "Hawthorne", "Hollister", "Holloway", "Ingram", "Jarvis", "Keating", "Kendrick", "Kingsley",
        "Lambert", "Langford", "Larkin", "Lockwood", "Lowell", "Maddox", "Mallory", "Marlow", "Merritt", "Monroe",
        "Nash", "Norwood", "Oakley", "Osborne", "Pembroke", "Prescott", "Quinlan", "Radcliffe", "Rainier",
        "Redmond", "Rhodes", "Rowland", "Sanderson", "Sawyer", "Selwyn", "Shelby", "Sinclair", "Stanton",
        "Sterling", "Talbot", "Thackeray", "Thornton", "Underwood", "Vance", "Wakefield", "Whitaker", "Winslow",
        "Wolcott", "Yardley", "Yates"]


def _nnumbers(rng, n, taken):
    out = []
    while len(out) < n:
        k = rng.random()
        if k < 0.30:
            s = "%d%d%d%d" % (rng.integers(1, 10), rng.integers(0, 10), rng.integers(0, 10), rng.integers(0, 10))
            s += CHARSET[rng.integers(0, 24)]
        elif k < 0.65:
            s = "%d%d%d" % (rng.integers(1, 10), rng.integers(0, 10), rng.integers(0, 10))
            s += CHARSET[rng.integers(0, 24)] + CHARSET[rng.integers(0, 24)]
        elif k < 0.85:
            s = "%d%d%d%d%d" % tuple([rng.integers(1, 10)] + [rng.integers(0, 10) for _ in range(4)])
        else:
            s = "%d%d" % (rng.integers(1, 10), rng.integers(0, 10)) + CHARSET[rng.integers(0, 24)] + \
                CHARSET[rng.integers(0, 24)]
        n_ = "N" + s
        if n_ not in taken:
            taken.add(n_)
            out.append(n_)
    return out


def _serial(rng, model):
    mfr = MODEL_BY_CODE[model][1]
    if mfr == "CESSNA":
        return "%d%05d" % (rng.integers(17, 21), rng.integers(10000, 99999))
    if mfr == "PIPER":
        return "%d-%d%04d" % (rng.integers(28, 45), rng.integers(7, 9), rng.integers(1000, 9999))
    if mfr.startswith("CIRRUS"):
        return "%d" % rng.integers(1000, 9999)
    return "%d" % rng.integers(1000, 99999)




# maximum takeoff weight (lb) and cruise speed (mph) by model, for the reference file and the emitter category
WEIGHT = {"2072738": 2550, "2072706": 2300, "2073006": 3100, "2071206": 1670, "2073505": 4000, "7102810": 2550,
          "7102805": 2440, "7103215": 3600, "1150120": 3050, "1150122": 3600, "0560416": 3650, "6070105": 2740,
          "1351408": 2646, "05628KW": 1800, "7100210": 1220, "0182001": 1300, "8640011": 1500, "5320006": 1260,
          "2070104": 1450, "2070102": 1450, "3770102": 1400, "8310108": 2400, "7101822": 1750, "7102205": 2000,
          "7104402": 3800, "0566012": 5500, "7103405": 4750, "7103106": 7000, "2073905": 5500, "0569020": 12500,
          "6440012": 10450, "2074520": 8750, "2075340": 13870, "1370512": 17968, "0313004": 4961, "1182010": 5250,
          "0670038": 1040, "7102508": 2900}
SPEED = {"2072738": 140, "2072706": 135, "2073006": 165, "2071206": 120, "2073505": 195, "7102810": 145,
         "7102805": 140, "7103215": 185, "1150120": 175, "1150122": 210, "0560416": 200, "6070105": 175,
         "1351408": 160, "05628KW": 190, "7100210": 75, "0182001": 90, "8640011": 95, "5320006": 105, "2070104": 105,
         "2070102": 100, "3770102": 110, "8310108": 120, "7101822": 115, "7102205": 125, "7104402": 185,
         "0566012": 230, "7103405": 220, "7103106": 245, "2073905": 230, "0569020": 310, "6440012": 310,
         "2074520": 210, "2075340": 480, "1370512": 520, "0313004": 155, "1182010": 150, "0670038": 55,
         "7102508": 115}


def emitter(model):
    m = MODEL_BY_CODE[model]
    if m[3] == 6:
        return "A7"
    if m[3] == 1:
        return "B1"
    return "A1" if WEIGHT[model] < 15500 else "A2"


def weight_class(model):
    w = WEIGHT[model]
    return "CLASS 1" if w < 12500 else ("CLASS 2" if w < 20000 else "CLASS 3")


def _day(rng, lo, hi):
    return lo + dt.timedelta(days=int(rng.integers(0, (hi - lo).days + 1)))


def build(seed=4700):
    """Every aircraft in the story: based on the 30 fields and the valley's private strips, visiting from outside the
    valley, and the other aircraft registered in the four counties; with the register's history (N-numbers moved or
    changed in 2026, exports, a lapsed registration, N-numbers reissued to another aircraft years ago)."""
    rng = np.random.default_rng(seed)
    taken = set()
    aircraft = []

    def new(model, home, role, broadcasts, owner_kind="individual"):
        m = MODEL_BY_CODE[model]
        y0, y1 = m[11]
        if m[3] == 6:
            cls = "rotor"
        elif m[3] == 1:
            cls = "glider"
        elif m[4] == 1:
            cls = "single" if m[3] == 4 else "multi"
        else:
            cls = "turbine"
        a = dict(id=len(aircraft), model=model, family=m[9], home=home, role=role, broadcasts=broadcasts, cls=cls,
                 piston_airplane=(m[4] == 1 and m[3] in (4, 5)), year=int(rng.integers(y0, y1 + 1)),
                 serial=_serial(rng, model), owner_kind=owner_kind, active=True)
        aircraft.append(a)
        return a

    for f in W.F:
        lid = f["lid"]
        b, nd, sch = f["B"], f["ND"], f["school"]
        kind = f["kind"]
        # based piston airplanes that never broadcast: older airplanes on the vintage fields, a mix elsewhere
        for i in range(nd):
            fam = "vintage" if (kind == "vint" or rng.random() < 0.55) else "modern"
            if fam == "modern" and rng.random() < 0.08:
                fam = "twin"
            model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
            new(model, lid, "private", False)
        # school fleets: broadcasting trainers (a twin trainer at the larger schools)
        for i in range(sch):
            fam = "twin" if (i == 0 and sch >= 10) else "modern"
            pool = ["2072738", "7102810", "2071206", "1351408"] if fam == "modern" else ["7104402"]
            new(pool[int(rng.integers(0, len(pool)))], lid, "school", True, owner_kind="school")
        # broadcasting private piston airplanes
        for i in range(b - nd - sch):
            r = rng.random()
            if kind == "vint" and r < 0.22:
                fam = "vintage"
            elif r < 0.09:
                fam = "twin"
            else:
                fam = "modern"
            model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
            new(model, lid, "private", True)
        for i in range(f["turbines"]):
            model = FAMILY["turbine"][int(rng.integers(0, len(FAMILY["turbine"])))]
            new(model, lid, "charter" if (lid in ("CRV", "HWK") and i < 4) else "private", True,
                owner_kind="company")
        for i in range(f["helos"]):
            model = FAMILY["helo"][int(rng.integers(0, len(FAMILY["helo"])))]
            new(model, lid, "private", True, owner_kind="company")
    # a glider operation at Lanthorne: two gliders and the tow plane
    for i in range(2):
        new("0670038", "L08", "glider", i == 0, owner_kind="club")
    new("7102508", "L08", "towplane", True, owner_kind="club")
    # visiting aircraft based outside the valley
    for i in range(140):
        r = rng.random()
        fam = "turbine" if r < 0.22 else ("twin" if r < 0.32 else "modern")
        model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
        a = new(model, None, "visitor", True, owner_kind="individual" if fam != "turbine" else "company")
        a["charter"] = fam == "turbine" and rng.random() < 0.3
    # aircraft on the valley's private strips: those that broadcast fly into the fields now and then, the others
    # keep to their strips
    for lid, name, county in W.STRIPS:
        for i in range(int(rng.integers(8, 16))):
            fam = "vintage" if rng.random() < 0.3 else "modern"
            model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
            new(model, lid, "strip", rng.random() < 0.7)
    # owners and operators at the towered fields who moved their N-number from a piston airplane to the turbine
    # aircraft that replaced it in 2026: the piston airplane leaves under a new number, the newcomer arrives under its
    # delivery number and takes the old one on the day of the move
    MOVES = [("CRV", "7103106", "0569020", dt.date(2026, 7, 14), "charter"),
             ("CRV", "7103106", "0569020", dt.date(2026, 7, 14), "charter"),
             ("CRV", "7103106", "0569020", dt.date(2026, 7, 14), "charter"),
             ("HWK", "2073905", "2075340", dt.date(2026, 6, 3), "charter"),
             ("OSY", "0566012", "6440012", dt.date(2026, 8, 19), "mover"),
             ("VNL", "7103405", "6440012", dt.date(2026, 5, 27), "mover"),
             ("KTY", "2073505", "2074520", dt.date(2026, 9, 8), "survey"),
             ("DMR", "0566012", "0569020", dt.date(2026, 7, 29), "mover")]
    movers = []
    for home, pm, tm, day, role in MOVES:
        p_ = new(pm, home, role, True, owner_kind="company" if role != "mover" else "individual")
        t_ = new(tm, home, "charter" if role == "charter" else "private", True,
                 owner_kind="company" if role != "mover" else "individual")
        p_["mover"] = True
        movers.append((p_, t_, day))
    # the other aircraft registered to addresses in the four counties (kept in hangars elsewhere or not flown)
    for i in range(650):
        r = rng.random()
        fam = "modern" if r < 0.70 else ("vintage" if r < 0.85 else ("twin" if r < 0.92 else
                                                                      ("turbine" if r < 0.97 else "helo")))
        model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
        a = new(model, None, "filler", False, owner_kind="individual" if fam not in ("turbine", "helo") else "company")
        a["active"] = False
    nn = _nnumbers(rng, len(aircraft) + 60, taken)
    for a, n in zip(aircraft, nn):
        a["n"] = n
    spare = nn[len(aircraft):]
    events = []
    for p_, t_, day in movers:
        moved = p_["n"]
        p_["n_after"] = spare.pop()          # the piston airplane leaves the valley under a new number
        p_["changed_on"] = day
        p_["leaves_on"] = day
        t_["n_before"] = t_["n"]             # the newcomer flies under its delivery number until the move
        t_["n"] = moved
        t_["arrives_on"] = day - dt.timedelta(days=int(rng.integers(12, 30)))
        t_["changed_on"] = day
        t_["delivered_on"] = t_["arrives_on"] - dt.timedelta(days=int(rng.integers(20, 60)))
        events.append(("moved_number", moved, p_["id"], t_["id"], day))
    # owners who took a new N-number in 2026 (the transponder reprogrammed the same day)
    changers = [a for a in aircraft if a["home"] in W.BY_LID and a["broadcasts"] and a["role"] == "private"
                and a["piston_airplane"] and a["home"] not in W.COUNTED]
    pick = rng.choice(len(changers), 9, replace=False)
    for j in pick:
        a = changers[int(j)]
        a["n_before"] = a["n"]
        a["n"] = spare.pop()
        a["changed_on"] = dt.date(2026, int(rng.integers(3, 9)), int(rng.integers(1, 28)))
        a["stale_flight_id"] = rng.random() < 0.25     # the flight ID left at the old number
        events.append(("vanity", a["n"], a["id"], a["id"], a["changed_on"]))
    # airplanes sold abroad during 2026: broadcasting privates whose registration was cancelled for export
    exporters = [a for a in aircraft if a["home"] in W.BY_LID and a["broadcasts"] and a["role"] == "private"
                 and a["piston_airplane"] and "n_before" not in a]
    pick = rng.choice(len(exporters), 6, replace=False)
    for j in pick:
        a = exporters[int(j)]
        a["exported_on"] = dt.date(2026, int(rng.integers(8, 12)), int(rng.integers(1, 28)))
        a["exp_country"] = ["CA", "MX", "BR", "AU", "CA", "NZ"][int(j) % 6]
        events.append(("export", a["n"], a["id"], None, a["exported_on"]))
    # registrations that lapsed late in 2026 while the airplane stayed on its field (still on the based list)
    lapsers = [a for a in aircraft if a["home"] in W.UNTOWERED and a["broadcasts"] and a["role"] == "private"
               and a["piston_airplane"] and "n_before" not in a and "exported_on" not in a]
    pick = rng.choice(len(lapsers), 2, replace=False)
    for j in pick:
        a = lapsers[int(j)]
        a["cancelled_on"] = dt.date(2026, int(rng.integers(11, 13)), int(rng.integers(1, 28)))
        events.append(("lapsed", a["n"], a["id"], None, a["cancelled_on"]))
    for a in aircraft:
        a["hex"] = icao_hex(a["n"])
        if "n_before" in a:
            a["hex_before"] = icao_hex(a["n_before"])
        if "n_after" in a:
            a["hex_after"] = icao_hex(a["n_after"])
    registry(rng, aircraft)
    return dict(aircraft=aircraft, register_events=events, rng_state=int(rng.integers(0, 2 ** 31)))


def registry(rng, aircraft):
    """The register's view: each aircraft's current registration (MASTER) and the cancelled ones (DEREG), as of the
    district's download of 1 February 2027."""
    uid = 1004211
    master, dereg = [], []

    def cert(model):
        m = MODEL_BY_CODE[model]
        if m[3] == 1:
            return "1G"
        if m[7] == 1:
            return "42"
        return "1N" if rng.random() < 0.8 else "1NU"

    def registrant(a):
        k = a["owner_kind"]
        if k == "individual":
            return "1" if rng.random() < 0.75 else ("4" if rng.random() < 0.5 else "7")
        if k == "club":
            return "2"
        return "3" if rng.random() < 0.6 else "7"

    for a in aircraft:
        a["air_worth"] = _day(rng, dt.date(max(a["year"], 1946), 1, 15), dt.date(max(a["year"], 1946), 12, 15))
        a["kind_code"] = registrant(a)
        a["cert"] = cert(a["model"])
        a["fract"] = "Y" if (a["cls"] == "turbine" and a["role"] == "private" and rng.random() < 0.15) else ""
        uid += int(rng.integers(3, 900))
        a["uid"] = "%08d" % uid
    for a in aircraft:
        lo = dt.date(2020, 3, 2)
        issued = _day(rng, lo, dt.date(2025, 11, 30))
        if a.get("delivered_on"):                       # a newcomer: its delivery registration, then the moved number
            dereg.append(dict(a=a, n=a["n_before"], issued=a["delivered_on"], cancel=a["changed_on"], exp=""))
            issued = a["changed_on"]
        elif "n_before" in a:                           # an owner's new N-number
            dereg.append(dict(a=a, n=a["n_before"], issued=issued, cancel=a["changed_on"], exp=""))
            issued = a["changed_on"]
        if a.get("mover"):                              # the piston airplane whose number moved: cancelled from it
            dereg.append(dict(a=a, n=a["n"], issued=issued, cancel=a["changed_on"], exp=""))
            continue
        if "exported_on" in a:
            dereg.append(dict(a=a, n=a["n"], issued=issued, cancel=a["exported_on"], exp=a["exp_country"]))
            continue
        if "cancelled_on" in a:
            dereg.append(dict(a=a, n=a["n"], issued=issued, cancel=a["cancelled_on"], exp=""))
            continue
        last = issued if rng.random() < 0.7 else _day(rng, issued, dt.date(2027, 1, 20))
        status = "R" if (a["role"] == "filler" and rng.random() < 0.07) else "V"
        master.append(dict(a=a, n=a["n"], issued=issued, last=max(last, issued), status=status))
    # N-numbers in MASTER reissued from an aircraft whose registration was cancelled years before
    reissued = [r for r in master if r["issued"] > dt.date(2020, 6, 1)]
    pick = rng.choice(len(reissued), 190, replace=False)
    for j in pick:
        r = reissued[int(j)]
        fam = ["vintage", "modern", "modern", "twin", "turbine", "helo"][int(rng.integers(0, 6))]
        model = FAMILY[fam][int(rng.integers(0, len(FAMILY[fam])))]
        m = MODEL_BY_CODE[model]
        y = int(rng.integers(m[11][0], m[11][1] + 1))
        old = dict(id=None, model=model, serial=_serial(rng, model), year=y, cls=None, cert=cert(model),
                   air_worth=_day(rng, dt.date(y, 1, 15), dt.date(y, 12, 15)), uid="", kind_code="1", fract="")
        cancel = _day(rng, dt.date(1996, 1, 1), min(r["issued"] - dt.timedelta(days=200), dt.date(2025, 6, 30)))
        issued = _day(rng, cancel - dt.timedelta(days=6000), cancel - dt.timedelta(days=400))
        dereg.append(dict(a=old, n=r["n"], issued=issued, cancel=cancel,
                          exp=["", "", "", "CA", "MX"][int(rng.integers(0, 5))]))
    for r in master:
        r["a"]["reg_issued"] = r["issued"]
    REG["master"] = master
    REG["dereg"] = dereg


REG = {}


if __name__ == "__main__":
    x = build()
    ac = x["aircraft"]
    print(len(ac), "aircraft;", sum(a["piston_airplane"] for a in ac), "piston airplanes;",
          sum(1 for a in ac if a["piston_airplane"] and not a["broadcasts"] and a["home"] in W.BY_LID),
          "based on the fields never broadcasting;", len(REG["master"]), "MASTER rows;", len(REG["dereg"]), "DEREG rows")
    for e in x["register_events"]:
        print(e)
