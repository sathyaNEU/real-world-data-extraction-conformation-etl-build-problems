"""The fixed world: calendar, managers, issuers, the watchlist design table.

Everything here is deterministic from SEED. Names are invented from word lists (no real firm or
issuer is depicted); CUSIPs carry a valid check digit; CIKs and accession numbers follow EDGAR's
shapes.
"""
import datetime as dt
import numpy as np

SEED = 445

# ---------------------------------------------------------------- calendar
PERIODS = {
    "Q2": dt.date(2022, 6, 30),
    "Q3": dt.date(2022, 9, 30),
    "Q4": dt.date(2022, 12, 31),
}
DEADLINE = {"Q2": dt.date(2022, 8, 15), "Q3": dt.date(2022, 11, 14), "Q4": dt.date(2023, 2, 14)}
EXTRACT_DATE = dt.date(2023, 2, 3)           # last EDGAR acceptance day in the daily build
CUT_DAY = (EXTRACT_DATE - PERIODS["Q4"]).days  # 34
UNIT_SWITCH = dt.date(2023, 1, 3)            # VALUE in dollars for filings on or after this date
DROPS = [  # (folder, first submission date, last submission date)
    ("form13f_2022q3", dt.date(2022, 7, 1), dt.date(2022, 9, 30)),
    ("form13f_2022q4", dt.date(2022, 10, 1), dt.date(2022, 12, 31)),
    ("edgar13f_daily_20230103_20230203", dt.date(2023, 1, 1), EXTRACT_DATE),
]
HOLIDAYS = {dt.date(2022, 7, 4), dt.date(2022, 9, 5), dt.date(2022, 10, 10), dt.date(2022, 11, 11),
            dt.date(2022, 11, 24), dt.date(2022, 12, 26), dt.date(2023, 1, 2), dt.date(2023, 1, 16),
            dt.date(2023, 2, 20)}


def business_day_on_or_after(d):
    while d.weekday() >= 5 or d in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def sec_date(d):
    return d.strftime("%d-%b-%Y").upper()


# ---------------------------------------------------------------- CUSIP
def cusip_check(base8):
    total = 0
    for i, ch in enumerate(base8):
        if ch.isdigit():
            v = int(ch)
        elif ch.isalpha():
            v = ord(ch.upper()) - ord("A") + 10
        else:
            v = {"*": 36, "@": 37, "#": 38}[ch]
        if i % 2 == 1:
            v *= 2
        total += v // 10 + v % 10
    return str((10 - total % 10) % 10)


def make_cusip(issuer6, issue="10"):
    b = issuer6 + issue
    return b + cusip_check(b)


# ---------------------------------------------------------------- name stock
_STEMS = """Ashgrove Bellmere Calder Dunmore Eastlake Fairhaven Glenrock Harrowgate Ironbridge Juniper
Kestrel Larchfield Marlowe Northcote Oakhurst Pemberton Quarry Redfern Saltmarsh Thornbury Upland
Varden Westbourne Yarrow Alder Birchall Copperline Dovecote Elmstead Foxley Granger Hollin Inverleigh
Kittering Lowther Mossgiel Netherby Orchard Pendle Quayside Rainford Stonecrest Tamsin Underhill
Vale Whitcombe Ambleside Brackley Carrow Delmont Edgewater Farrier Gilmour Halcyon Ingleby Jessop
Kinloch Lindell Merriman Norland Ottery Prescott Ravenna Selwood Tolland Ulverston Verity Wickham
Abbotsford Blakeney Cairnwood Dunleavy Ellery Fenwick Gresham Hartwell Islay Kellerman Langdale
Mortlake Newhall Osgood Pellham Radley Sherwin Thackeray Wexley Brantwood Corrigan Davenant Eversley
Fallowfield Greystone Holloway Kingsmere Lockhart Millbrook Northgate Ormond Pascoe Riverside
Sandford Tilbury Waverly Ashby Barrowden Coldharbour Drummond Esk Falkland Galloway Highmoor
Kirkby Lismore Moorcroft Nethercott Oldfield Penrose Rothwell Skelton Tregaron Wyndham Arden
Bramley Cheswick Dalby Exmoor Fernhill Glenmore Hawthorn Ivers Lanyon Medway Norbury Otterburn
Pryor Rosedale Stanwick Trevose Wolcott Ainsley Bexford Chilton Dorrance Eldon Fulbrook Garland
Hensley Ilford Knowle Lytham Marsden Nantwich Overton Poynter Ramsay Shelby Tavener Whitby""".split()
_MGR_WORDS = ["Capital", "Asset", "Investment", "Wealth", "Partners", "Advisors", "Trust", "Fund",
              "Global", "Point", "Street", "Ridge", "Harbor", "Peak", "Square", "Bridge", "Lane"]
_MGR_SUFFIX = ["Management LLC", "Management LP", "Advisors LLC", "Partners LP", "Capital LLC",
               "Group Inc", "Investment Counsel Inc", "Wealth Advisors LLC", "& Co LLC", "LLC"]
_ISS_WORDS = ["Thermal", "Biosciences", "Holdings", "Systems", "Industries", "Therapeutics", "Logistics",
              "Software", "Materials", "Energy", "Financial", "Brands", "Networks", "Medical",
              "Semiconductor", "Foods", "Realty", "Robotics", "Aerospace", "Water", "Pharma",
              "Payments", "Labs", "Outdoor", "Packaging", "Mobility", "Analytics", "Instruments"]
_ISS_SUFFIX = ["Inc", "Corp", "Inc", "Co", "Holdings Inc", "Group Inc", "Ltd", "Corporation"]
_REAL = {"Vanguard", "Fidelity", "BlackRock", "Wellington", "Bridgewater", "Citadel", "Renaissance",
         "Two Sigma", "Millennium", "Point72", "State Street", "Invesco", "Northern Trust", "Geode",
         "Dimensional", "Schwab", "Goldman", "Morgan", "Capital Group", "T. Rowe", "Jane Street",
         "Susquehanna", "Balyasny", "Elliott", "Baupost", "Viking", "Tiger", "Coatue", "Lone Pine",
         "Hawthorn", "Riverside", "Kingsmere", "Granger", "Galloway", "Medway", "Exmoor", "Esk"}

STATES = ["NY", "NY", "NY", "CT", "MA", "CA", "CA", "IL", "TX", "PA", "NJ", "FL", "GA", "CO", "WA",
          "MN", "OH", "MD", "VA", "NC", "MO", "WI", "TN", "AZ"]
CITY = {"NY": "NEW YORK", "CT": "GREENWICH", "MA": "BOSTON", "CA": "SAN FRANCISCO", "IL": "CHICAGO",
        "TX": "DALLAS", "PA": "PHILADELPHIA", "NJ": "PRINCETON", "FL": "MIAMI", "GA": "ATLANTA",
        "CO": "DENVER", "WA": "SEATTLE", "MN": "MINNEAPOLIS", "OH": "COLUMBUS", "MD": "BALTIMORE",
        "VA": "RICHMOND", "NC": "CHARLOTTE", "MO": "ST. LOUIS", "WI": "MILWAUKEE", "TN": "NASHVILLE",
        "AZ": "SCOTTSDALE"}

# manager types: (key, register label, count, habit-day range, size lognormal mu)
MGR_TYPES = [
    ("passive", "Index and ETF sponsor", 7, None, 23.0),
    ("multistrat", "Multi-strategy and hedge fund", 64, (36, 45), 20.6),
    ("longonly", "Long-only investment adviser", 58, (14, 44), 20.9),
    ("banktrust", "Bank trust and wealth department", 96, (7, 29), 20.1),
    ("ria", "Registered investment adviser", 150, (9, 45), 18.9),
    ("instit", "Pension, insurance and endowment", 34, (18, 41), 20.3),
    ("dealer", "Broker-dealer", 8, (24, 38), 20.0),
]
# passive complexes: two large ones file early, five file at the deadline
PASSIVE_DAYS = [21, 27, 41, 42, 43, 44, 44]
PASSIVE_SIZE = [25.4, 25.0, 23.9, 23.6, 23.4, 23.0, 22.8]

# ---------------------------------------------------------------- watchlist design
# id, target Dec IO on the completed set (A), share of it on file at the extract (f),
# target Sep IO (complete), shares outstanding (Oct-dated cover page), Q4 price
WATCH = [
    # id   A      f      sep    S_oct        P4
    ("W01", 88.4, 0.935, 86.3, 41_820_557, 74.18),
    ("W02", 84.1, 0.665, 83.2, 63_104_219, 38.62),
    ("W03", 83.4, 0.705, 79.0, 28_559_804, 112.41),
    ("W04", 76.2, 0.950, 75.1, 117_402_633, 23.07),
    ("W05", 74.4, 0.915, 77.2, 52_271_090, 56.90),
    ("W06", 86.1, 0.945, 84.4, 35_906_712, 141.55),
    ("W07", 77.3, 0.860, 81.6, 88_013_465, 31.34),
    ("W08", 62.26, 0.855, 61.1, 74_660_128, 47.73),
    ("W09", 71.1, 0.800, 70.2, 23_177_946, 88.26),
    ("W10", 91.6, 0.720, 90.3, 46_318_551, 64.09),
    ("W11", 55.2, 0.880, 53.8, 158_244_370, 18.44),
    ("W12", 67.3, 0.750, 66.4, 31_052_683, 52.80),
]


def rng(*salt):
    return np.random.default_rng([SEED] + [abs(hash_str(s)) for s in salt])


def hash_str(s):
    h = 0
    for ch in str(s):
        h = (h * 131 + ord(ch)) % 2_147_483_647
    return h


def build_managers():
    r = rng("managers")
    stems = [s for s in _STEMS if s not in _REAL]
    used, mgrs = set(), []
    cik_pool = r.choice(np.arange(1_040_000, 1_960_000), size=600, replace=False)
    k = 0
    for key, label, n, rngdays, mu in MGR_TYPES:
        for j in range(n):
            while True:
                a = stems[r.integers(len(stems))]
                if key == "passive":
                    nm = f"{a} {r.choice(['Index', 'Indexing', 'Funds', 'Investments'])} {r.choice(['Group Inc', 'Advisors LLC', 'Management LP'])}"
                elif key == "banktrust":
                    nm = f"{a} {r.choice(['Bank & Trust Co', 'Trust Co', 'National Bank Wealth Management', 'Savings Bank Trust Dept'])}"
                elif key == "dealer":
                    nm = f"{a} {r.choice(['Securities LLC', 'Markets LLC', 'Trading LLC'])}"
                elif key == "instit":
                    nm = f"{a} {r.choice(['Retirement System', 'Mutual Life Insurance Co', 'University Endowment', 'Employees Pension Fund'])}"
                else:
                    b = _MGR_WORDS[r.integers(len(_MGR_WORDS))]
                    nm = f"{a} {b} {_MGR_SUFFIX[r.integers(len(_MGR_SUFFIX))]}"
                if nm not in used and a not in {m['stem'] for m in mgrs if m['type'] in ('passive', 'dealer')}:
                    used.add(nm)
                    break
            if key == "passive":
                habit, size = PASSIVE_DAYS[j], PASSIVE_SIZE[j]
            else:
                lo, hi = rngdays
                habit = float(r.uniform(lo, hi))
                if key in ("multistrat",) and r.random() < 0.12:
                    habit = float(r.uniform(18, 33))
                size = float(r.normal(mu, 0.9))
            st = STATES[r.integers(len(STATES))]
            mgrs.append(dict(mid=f"M{k:03d}", cik=int(cik_pool[k]), name=nm.upper().replace("&", "&"),
                             disp=nm, stem=a, type=key, type_label=label, habit=habit, size=size,
                             state=st, city=CITY[st], family=None,
                             fileno=f"028-{int(r.integers(10000, 22999)):05d}"))
            k += 1
    return mgrs


def build_issuers():
    r = rng("issuers")
    stems = [s for s in _STEMS if s not in _REAL]
    used, out = set(), []
    six = set()

    def new6(lead=None):
        while True:
            if lead == "0":
                s = "0" + "".join(str(r.integers(10)) for _ in range(5))
            elif lead == "alpha":
                s = "".join(str(r.integers(10)) for _ in range(3)) + "XY"[r.integers(2)] + "".join(str(r.integers(10)) for _ in range(2))
            else:
                s = str(r.integers(1, 10)) + "".join(str(r.integers(10)) for _ in range(5))
            if s not in six:
                six.add(s)
                return s

    leads = {"W04": "0", "W09": "0", "W12": "alpha", "W03": "0"}
    wstems = set()
    for wid, A, f, sep, S, P4 in WATCH:
        while True:
            a = stems[r.integers(len(stems))]
            b = _ISS_WORDS[r.integers(len(_ISS_WORDS))]
            sfx = _ISS_SUFFIX[r.integers(len(_ISS_SUFFIX))]
            if b == "Holdings" and "Holdings" in sfx:
                continue
            nm = f"{a} {b} {sfx}"
            if nm not in used and a not in wstems:
                used.add(nm)
                wstems.add(a)
                break
        out.append(dict(iid=wid, name=nm.upper(), watch=True, cusip=make_cusip(new6(leads.get(wid))),
                        A=A, f=f, sep=sep, S_oct=S, P4=P4))
    for j in range(236):
        while True:
            a = stems[r.integers(len(stems))]
            b = _ISS_WORDS[r.integers(len(_ISS_WORDS))]
            sfx = _ISS_SUFFIX[r.integers(len(_ISS_SUFFIX))]
            nm = f"{a} {b} {sfx}"
            if nm not in used and a not in wstems and not (b == "Holdings" and "Holdings" in sfx):
                used.add(nm)
                break
        A = float(r.uniform(32, 96))
        out.append(dict(iid=f"U{j:03d}", name=nm.upper(), watch=False,
                        cusip=make_cusip(new6("0" if r.random() < 0.08 else None)),
                        A=A, f=float(r.uniform(0.70, 0.95)), sep=A + float(r.normal(0, 2.5)),
                        S_oct=int(np.exp(r.uniform(np.log(1.2e7), np.log(1.6e9)))),
                        P4=float(np.round(np.exp(r.uniform(np.log(6), np.log(420))), 2))))
    # issuer master attributes
    rm = rng("issuer-master")
    ciks = rm.choice(np.arange(1_300_000, 1_920_000), size=len(out), replace=False)
    tick = set()
    sics = [2834, 2836, 3674, 3711, 3826, 4911, 5812, 6022, 7372, 7373, 2086, 3559, 1311, 4213, 6798, 3841, 5961, 3714]
    for k, i in enumerate(out):
        i["issuer_cik"] = int(ciks[k])
        i["sic"] = int(sics[rm.integers(len(sics))])
        st = STATES[rm.integers(len(STATES))]
        i["state"], i["city"] = st, CITY[st]
        i["afs"] = "1-LAF" if i["S_oct"] * i["P4"] > 2.5e9 else "2-ACC"
        words = [w for w in i["name"].split() if w not in ("INC", "CORP", "CO", "LTD", "GROUP", "HOLDINGS", "CORPORATION")]
        while True:
            t = (words[0][:2] + words[1][:1] + ("" if rm.random() < 0.5 else words[0][2:3])).upper() if len(words) > 1 else words[0][:4]
            if t in tick:
                t = t[:3] + "ABCDEFGHJKLMNPRSTVWXZ"[rm.integers(21)]
            if t not in tick and t not in ("COAL", "SAS", "GOLD", "OIL", "CASH", "FUND", "BANK", "ABB", "HAM", "JEM"):
                tick.add(t)
                break
        i["ticker"] = t
    return out
