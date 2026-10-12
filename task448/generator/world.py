"""The world behind task448: the Prairie Lantern Housing Fund's eight-county rural service area in central Kansas,
the lenders that make home-purchase mortgages there, how each one's mortgages reach the county recorder, and the
dates and files of the October 2026 pull. Every figure the pack carries is simulated from these parameters."""
import datetime as dt

import numpy as np

SEED = 448
ORG = "Prairie Lantern Housing Fund"
VENDOR = "Venridge Property Data, LLC"
PULL = dt.date(2026, 10, 9)                 # the research desk's pull for the December board

# Kansas counties, alphabetical; FIPS 20001 to 20209 by odd numbers; the Kansas county number is the position
KS_COUNTIES = [
    "Allen", "Anderson", "Atchison", "Barber", "Barton", "Bourbon", "Brown", "Butler", "Chase", "Chautauqua",
    "Cherokee", "Cheyenne", "Clark", "Clay", "Cloud", "Coffey", "Comanche", "Cowley", "Crawford", "Decatur",
    "Dickinson", "Doniphan", "Douglas", "Edwards", "Elk", "Ellis", "Ellsworth", "Finney", "Ford", "Franklin",
    "Geary", "Gove", "Graham", "Grant", "Gray", "Greeley", "Greenwood", "Hamilton", "Harper", "Harvey",
    "Haskell", "Hodgeman", "Jackson", "Jefferson", "Jewell", "Johnson", "Kearny", "Kingman", "Kiowa", "Labette",
    "Lane", "Leavenworth", "Lincoln", "Linn", "Logan", "Lyon", "McPherson", "Marion", "Marshall", "Meade",
    "Miami", "Mitchell", "Montgomery", "Morris", "Morton", "Nemaha", "Neosho", "Ness", "Norton", "Osage",
    "Osborne", "Ottawa", "Pawnee", "Phillips", "Pottawatomie", "Pratt", "Rawlins", "Reno", "Republic", "Rice",
    "Riley", "Rooks", "Rush", "Russell", "Saline", "Scott", "Sedgwick", "Seward", "Shawnee", "Sheridan",
    "Sherman", "Smith", "Stafford", "Stanton", "Stevens", "Sumner", "Thomas", "Trego", "Wabaunsee", "Wallace",
    "Washington", "Wichita", "Wilson", "Woodson", "Wyandotte"]
FIPS = {n: "20%03d" % (2 * i + 1) for i, n in enumerate(KS_COUNTIES)}
KSNO = {n: i + 1 for i, n in enumerate(KS_COUNTIES)}
MSA = {}
for _c in ("Butler", "Harvey", "Sedgwick", "Sumner"):
    MSA[_c] = "48620"
for _c in ("Johnson", "Leavenworth", "Linn", "Miami", "Wyandotte"):
    MSA[_c] = "28140"
for _c in ("Jackson", "Jefferson", "Osage", "Shawnee", "Wabaunsee"):
    MSA[_c] = "45820"
MSA["Douglas"] = "29940"
for _c in ("Geary", "Pottawatomie", "Riley"):
    MSA[_c] = "31740"
MSA["Doniphan"] = "41140"
MSA_INCOME = {"48620": (86900, 90100), "28140": (104200, 108400), "45820": (88700, 92300), "29940": (101800, 106100),
              "31740": (80600, 83900), "41140": (78900, 81700), "99999": (76800, 79400)}
# rough shares of Kansas mortgage applications; every county not named takes a share of the remainder by size class
BIG = {"Johnson": 23.0, "Sedgwick": 17.0, "Shawnee": 5.6, "Wyandotte": 4.6, "Douglas": 3.9, "Leavenworth": 2.9,
       "Butler": 2.6, "Riley": 1.9, "Reno": 1.9, "Miami": 1.4, "Harvey": 1.0, "Franklin": 0.9, "Pottawatomie": 0.9,
       "Geary": 1.0, "Lyon": 0.9, "Finney": 0.8, "Ford": 0.8, "Cowley": 0.9, "Sumner": 0.7, "Jefferson": 0.6,
       "Ellis": 0.8, "Crawford": 0.9, "Montgomery": 0.7, "Barton": 0.7, "Seward": 0.5, "Jackson": 0.4, "Osage": 0.4}

REGION = ["Saline", "McPherson", "Dickinson", "Marion", "Rice", "Ottawa", "Ellsworth", "Lincoln"]
FOUR = ["Saline", "McPherson", "Dickinson", "Marion"]
OTHER_FOUR = ["Rice", "Ottawa", "Ellsworth", "Lincoln"]
COUNTY_W = {"Saline": 0.44, "McPherson": 0.23, "Dickinson": 0.13, "Marion": 0.055, "Rice": 0.058,
            "Ottawa": 0.036, "Ellsworth": 0.035, "Lincoln": 0.016}
TRACTS = {"Saline": 14, "McPherson": 8, "Dickinson": 6, "Marion": 4, "Rice": 3, "Ottawa": 2, "Ellsworth": 2,
          "Lincoln": 1}
# each county's recording office numbers its documents in its own series, restarting each year
DOC_FORMAT = {"Saline": "{y}-{n:06d}", "McPherson": "{y}{n:05d}", "Dickinson": "{yy}-{n:05d}", "Marion": "{y}R{n:05d}",
              "Rice": "{y}-{n:05d}", "Ottawa": "{y}{n:04d}", "Ellsworth": "{y}-{n:04d}", "Lincoln": "{yy}{n:04d}"}
DOCS_PER_DAY = {"Saline": 46, "McPherson": 24, "Dickinson": 16, "Marion": 11, "Rice": 9, "Ottawa": 6, "Ellsworth": 6,
                "Lincoln": 3}
TOWNS = {"Saline": ["Salina", "Assaria", "Brookville", "Gypsum"],
         "McPherson": ["McPherson", "Lindsborg", "Inman", "Moundridge", "Galva", "Canton"],
         "Dickinson": ["Abilene", "Herington", "Solomon", "Chapman"],
         "Marion": ["Hillsboro", "Marion", "Peabody", "Goessel", "Durham"],
         "Rice": ["Lyons", "Sterling", "Little River", "Geneseo"],
         "Ottawa": ["Minneapolis", "Bennington", "Delphos", "Tescott"],
         "Ellsworth": ["Ellsworth", "Kanopolis", "Wilson"],
         "Lincoln": ["Lincoln", "Beverly", "Sylvan Grove"]}
TOWN_W = {"Saline": [0.90, 0.03, 0.03, 0.04], "McPherson": [0.62, 0.15, 0.08, 0.08, 0.04, 0.03],
          "Dickinson": [0.62, 0.17, 0.12, 0.09], "Marion": [0.36, 0.25, 0.18, 0.14, 0.07],
          "Rice": [0.48, 0.32, 0.12, 0.08], "Ottawa": [0.66, 0.16, 0.10, 0.08], "Ellsworth": [0.64, 0.22, 0.14],
          "Lincoln": [0.60, 0.16, 0.24]}
CITY_COUNTY = {t: c for c, ts in TOWNS.items() for t in ts}
ZIP = {"Salina": "67401", "Assaria": "67416", "Brookville": "67425", "Gypsum": "67448", "McPherson": "67460",
       "Lindsborg": "67456", "Inman": "67546", "Moundridge": "67107", "Galva": "67443", "Canton": "67428",
       "Abilene": "67410", "Herington": "67449", "Solomon": "67480", "Chapman": "67431", "Marion": "66861",
       "Hillsboro": "67063", "Peabody": "66866", "Goessel": "67053", "Durham": "67438", "Lyons": "67554",
       "Sterling": "67579", "Little River": "67457", "Geneseo": "67444", "Minneapolis": "67467",
       "Bennington": "67422", "Delphos": "67436", "Tescott": "67484", "Ellsworth": "67439", "Kanopolis": "67454",
       "Wilson": "67490", "Lincoln": "67455", "Beverly": "67423", "Sylvan Grove": "67481"}
# rural homes whose postal city lies in the next county, by the county the home stands in
MAIL_ACROSS = {"Ottawa": ("Salina", 0.22), "Lincoln": ("Salina", 0.26), "Ellsworth": ("Salina", 0.12),
               "Dickinson": ("Salina", 0.07), "McPherson": ("Salina", 0.04), "Rice": ("McPherson", 0.14),
               "Marion": ("McPherson", 0.09)}
RURAL = {"Saline": 0.10, "McPherson": 0.22, "Dickinson": 0.25, "Marion": 0.33, "Rice": 0.30, "Ottawa": 0.38,
         "Ellsworth": 0.30, "Lincoln": 0.45}
PRICE = {"Saline": 189000, "McPherson": 182000, "Dickinson": 161000, "Marion": 133000, "Rice": 118000,
         "Ottawa": 139000, "Ellsworth": 121000, "Lincoln": 104000}

MONTH_W = np.array([0.055, 0.060, 0.081, 0.090, 0.101, 0.110, 0.100, 0.098, 0.085, 0.080, 0.064, 0.076])
YEAR_W = {2024: 0.484, 2025: 0.516}
GROWTH_2026 = 1.035                          # 2026 closings against 2025, month for month

CAPTURE = {"P": 0.965, "S": 0.600}
SWITCH = dt.date(2026, 4, 6)                 # in-house lenders' closings from this date record with the deed
FEED_FIRST = dt.date(2024, 1, 1)
FEED_LAST = dt.date(2026, 8, 31)
SIM_FIRST = dt.date(2023, 10, 2)             # closings simulated from here so January 2024 recordings are whole
RERECORD = {"P": 0.004, "S": 0.021}          # mortgages re-recorded later to correct the record
SELLER_FIN = 0.013                           # seller-carried notes against lender mortgages, by count

# Lenders. kind R reports HMDA, N does not; charter NB nonbank, RB regional bank, CB community bank, CU credit union;
# route P records the mortgage with the deed (closings at a title company), S records its own mortgage after the
# deed. total: home-purchase first liens on homes in the eight counties closed 2024 and 2025 (for reporters, the
# HMDA count). home: county weights (None: the market's). qc: refinances recorded with a quitclaim deed to the owner's
# trust, per purchase mortgage. dup: farmstead mortgages recorded in two counties, over the two years. pig: purchase
# mortgages with a second lien recorded in the same package. buy: loans bought from other lenders in the eight
# counties (HMDA purchased loans). off: the lender's capture against its route's. rows: statewide HMDA records a year.
L = [
    dict(id="BIG1", name="Corvane Home Loans, LLC", kind="R", ch="NB", route="P", total=311, home=None,
         hq=("Troy", "MI"), qc=0.008, mers=0.97, off=0.003, rows=3100, short_list=True, label="National mortgage company"),
    dict(id="BIG2", name="Halverd Mortgage Company", kind="R", ch="NB", route="P", total=228, home=None,
         hq=("Irving", "TX"), qc=0.008, mers=0.96, off=-0.004, rows=2400, short_list=True,
         label="National mortgage company"),
    dict(id="BIG3", name="Tessaline Home Lending, Inc.", kind="R", ch="NB", route="P", total=141, home=None,
         hq=("Irvine", "CA"), qc=0.006, mers=0.98, off=0.001, rows=1500, short_list=True,
         label="National mortgage company"),
    dict(id="REG1", name="Arkhaven Bank, N.A.", kind="R", ch="RB", route="P", total=182,
         home={"Saline": 0.50, "McPherson": 0.22, "Dickinson": 0.10, "Marion": 0.05, "Rice": 0.06, "Ottawa": 0.03,
               "Ellsworth": 0.03, "Lincoln": 0.01}, hq=("Wichita", "KS"), qc=0.012, mers=0.55, off=-0.002, pig=0.025,
         rows=2600, short_list=True, label="Regional bank"),
    dict(id="REG2", name="Shunga Valley Bank", kind="R", ch="RB", route="P", total=151,
         home={"Saline": 0.55, "McPherson": 0.12, "Dickinson": 0.18, "Marion": 0.04, "Rice": 0.03, "Ottawa": 0.04,
               "Ellsworth": 0.03, "Lincoln": 0.01}, hq=("Topeka", "KS"), qc=0.012, mers=0.40, off=0.004, pig=0.02,
         rows=1900, short_list=True, label="Regional bank"),
    dict(id="CUR2", name="Ninnescah Federal Credit Union", kind="R", ch="CU", route="P", total=133,
         home={"Saline": 0.58, "McPherson": 0.18, "Dickinson": 0.08, "Marion": 0.04, "Rice": 0.05, "Ottawa": 0.03,
               "Ellsworth": 0.03, "Lincoln": 0.01}, hq=("Wichita", "KS"), qc=0.010, mers=0.30, off=-0.001, rows=1300,
         short_list=True, label="Credit union"),
    dict(id="CBR1", name="Saltfork State Bank", kind="R", ch="CB", route="S", total=138,
         home={"Saline": 0.74, "McPherson": 0.12, "Dickinson": 0.05, "Ottawa": 0.06, "Lincoln": 0.03},
         hq=("Salina", "KS"), qc=0.040, mers=0.0, off=-0.004, rows=170, short_list=True, label="Community bank"),
    dict(id="N1", name="Weyrauch State Bank", kind="N", ch="CB", route="S", total=257,
         home={"Saline": 0.74, "McPherson": 0.08, "Dickinson": 0.07, "Ottawa": 0.07, "Lincoln": 0.02, "Ellsworth": 0.02},
         hq=("Salina", "KS"), qc=0.045, mers=0.0, off=-0.003, short_list=True, label="Community bank"),
    dict(id="N2", name="Mennwell Credit Union", kind="N", ch="CU", route="S", total=200,
         home={"Saline": 0.33, "McPherson": 0.41, "Marion": 0.11, "Rice": 0.10, "Ellsworth": 0.05},
         hq=("McPherson", "KS"), qc=0.035, mers=0.0, off=0.004, short_list=True, label="Credit union"),
    dict(id="N3", name="Heidebrecht State Bank", kind="N", ch="CB", route="S", total=137,
         home={"Marion": 0.66, "McPherson": 0.15, "Saline": 0.05, "Dickinson": 0.06, "Rice": 0.08},
         hq=("Hillsboro", "KS"), qc=0.530, mers=0.0, off=-0.006, dup=2, short_list=True, label="Community bank"),
    dict(id="N4", name="Kessinger Federal Credit Union", kind="N", ch="CU", route="P", total=83,
         home={"Saline": 0.70, "McPherson": 0.10, "Dickinson": 0.08, "Ottawa": 0.07, "Lincoln": 0.05},
         hq=("Salina", "KS"), qc=0.010, mers=0.25, off=0.002, short_list=True, label="Credit union"),
    dict(id="N5", name="Eisenbrandt State Bank", kind="N", ch="CB", route="S", total=78,
         home={"Dickinson": 0.82, "Saline": 0.12, "Marion": 0.06}, hq=("Abilene", "KS"), qc=0.050, mers=0.0,
         off=0.002, dup=2, short_list=True, label="Community bank"),
    # reporters that close in-house
    dict(id="CBR2", name="Kroeker State Bank", kind="R", ch="CB", route="S", total=112,
         home={"Marion": 0.50, "McPherson": 0.22, "Dickinson": 0.18, "Saline": 0.10}, hq=("Peabody", "KS"), qc=0.035,
         mers=0.0, off=0.009, rows=150),
    dict(id="CUR1", name="Strobel Federal Credit Union", kind="R", ch="CU", route="S", total=81,
         home={"Dickinson": 0.48, "Saline": 0.44, "Ottawa": 0.08}, hq=("Junction City", "KS"), qc=0.030, mers=0.0,
         off=-0.008, rows=420),
    dict(id="NBR4", name="Plainsridge Mortgage, LLC", kind="R", ch="NB", route="S", total=64,
         home={"Saline": 0.32, "McPherson": 0.30, "Rice": 0.26, "Ellsworth": 0.12}, hq=("Salina", "KS"), qc=0.020,
         mers=0.0, off=0.006, rows=95),
    # reporters that close through title companies
    dict(id="CBR3", name="Tolliver State Bank", kind="R", ch="CB", route="P", total=101,
         home={"Saline": 0.62, "McPherson": 0.30, "Ottawa": 0.08}, hq=("Salina", "KS"), qc=0.012, mers=0.20,
         off=0.001, pig=0.02, rows=180),
    dict(id="CUR3", name="Harlowe Federal Credit Union", kind="R", ch="CU", route="P", total=67, home=None,
         hq=("Hutchinson", "KS"), qc=0.010, mers=0.35, off=-0.003, rows=600),
    dict(id="P01", name="Dellwyn Mortgage Corp.", kind="R", ch="NB", route="P", total=53, home=None,
         hq=("Charlotte", "NC"), qc=0.005, mers=0.97, off=0.002, rows=1150),
    dict(id="P02", name="Quillon Home Finance, LLC", kind="R", ch="NB", route="P", total=43, home=None,
         hq=("Plano", "TX"), qc=0.005, mers=0.98, off=-0.002, rows=900),
    dict(id="P03", name="Ravensted Lending Corporation", kind="R", ch="NB", route="P", total=37, home=None,
         hq=("Overland Park", "KS"), qc=0.005, mers=0.95, off=0.0, dup=1, rows=1250),
    dict(id="P04", name="Marrowfield Mortgage, Inc.", kind="R", ch="NB", route="P", total=32, home=None,
         hq=("Omaha", "NE"), qc=0.004, mers=0.96, off=0.003, rows=640),
    dict(id="P05", name="Brisbin Mortgage Services, LLC", kind="R", ch="NB", route="P", total=26, home=None,
         hq=("Denver", "CO"), qc=0.004, mers=0.97, off=-0.001, rows=520),
    dict(id="P06", name="Caddoc Home Loans, Inc.", kind="R", ch="NB", route="P", total=21, home=None,
         hq=("Tempe", "AZ"), qc=0.004, mers=0.98, off=0.0, rows=380),
    dict(id="P07", name="Cairnsley Bank", kind="R", ch="RB", route="P", total=29,
         home={"McPherson": 0.55, "Rice": 0.25, "Marion": 0.20}, hq=("Hutchinson", "KS"), qc=0.010, mers=0.45,
         off=0.002, rows=520),
    dict(id="P08", name="Ludgate National Bank", kind="R", ch="RB", route="P", total=23, home=None,
         hq=("Kansas City", "MO"), qc=0.008, mers=0.60, off=-0.002, rows=730),
    dict(id="P09", name="Fenwold Financial Mortgage, LLC", kind="R", ch="NB", route="P", total=18, home=None,
         hq=("Columbus", "OH"), qc=0.004, mers=0.98, off=0.001, rows=330),
    dict(id="P10", name="Wexcombe Mortgage Corporation", kind="R", ch="NB", route="P", total=15, home=None,
         hq=("Tulsa", "OK"), qc=0.004, mers=0.97, off=0.0, rows=290),
    dict(id="P11", name="Ambry Lending Group, LLC", kind="R", ch="NB", route="P", total=12, home=None,
         hq=("Scottsdale", "AZ"), qc=0.004, mers=0.98, off=0.0, rows=240),
    dict(id="AGG", name="Ostrander Bank, N.A.", kind="R", ch="RB", route="P", total=10, home=None,
         hq=("Sioux Falls", "SD"), qc=0.004, mers=0.90, off=0.0, buy=26, rows=880),
    # lenders HMDA does not cover, off the shortlist
    dict(id="N6", name="Kanbrook State Bank", kind="N", ch="CB", route="S", total=43,
         home={"Ellsworth": 0.72, "Lincoln": 0.12, "Saline": 0.10, "Rice": 0.06}, hq=("Ellsworth", "KS"), qc=0.06,
         mers=0.0, off=0.005, dup=2),
    dict(id="N7", name="Stueckemann State Bank", kind="N", ch="CB", route="S", total=32,
         home={"Rice": 0.80, "McPherson": 0.12, "Ellsworth": 0.08}, hq=("Lyons", "KS"), qc=0.05, mers=0.0, off=-0.004,
         dup=1),
    dict(id="N8", name="Brauneck State Bank", kind="N", ch="CB", route="S", total=19,
         home={"Lincoln": 0.70, "Ottawa": 0.18, "Ellsworth": 0.12}, hq=("Lincoln", "KS"), qc=0.05, mers=0.0, off=0.003,
         dup=1),
    dict(id="N9", name="Vogelsang Credit Union", kind="N", ch="CU", route="S", total=17,
         home={"Marion": 0.62, "Dickinson": 0.38}, hq=("Marion", "KS"), qc=0.03, mers=0.0, off=-0.002, dup=1),
    dict(id="N10", name="Cindercone Mortgage, LLC", kind="N", ch="NB", route="P", total=14,
         home={"Saline": 0.80, "McPherson": 0.20}, hq=("Salina", "KS"), qc=0.0, mers=0.90, off=0.0),
]
# small reporters with a handful of home-purchase loans in the eight counties: the first eight lend in one county each
# (closings in 2024, 2025 and January to June 2026), the rest across the market (a two-year total)
TAIL = [("Brevlin Home Mortgage, Inc.", "NB", ("Bloomington", "MN"), "Saline", (8, 6, 9)),
        ("Gaskell Lending, LLC", "NB", ("Frisco", "TX"), "McPherson", (5, 4, 0)),
        ("Tasveld Mortgage Company", "NB", ("Boise", "ID"), "Dickinson", (4, 4, 3)),
        ("Durlock Federal Credit Union", "CU", ("Emporia", "KS"), "Marion", (3, 3, 3)),
        ("Vantrell Home Loans, LLC", "NB", ("Chandler", "AZ"), "Rice", (0, 2, 2)),
        ("Merrowgate Financial, Inc.", "NB", ("Raleigh", "NC"), "Ottawa", (1, 1, 1)),
        ("Fallowmere Bank", "RB", ("Hays", "KS"), "Ellsworth", (2, 2, 1)),
        ("Dunleavy Mortgage Corp.", "NB", ("Tampa", "FL"), "Lincoln", (1, 1, 1)),
        ("Oskerry Bank", "RB", ("Lincoln", "NE"), None, 7),
        ("Haskett Lending Group, LLC", "NB", ("Salt Lake City", "UT"), None, 6),
        ("Corliss Mortgage, LLC", "NB", ("Fort Worth", "TX"), None, 6),
        ("Isley Home Finance, Inc.", "NB", ("Columbia", "MD"), None, 5),
        ("Graumont Bank", "RB", ("Joplin", "MO"), None, 5),
        ("Lorvick Mortgage Services, LLC", "NB", ("Edina", "MN"), None, 4),
        ("Ashveld Lending, Inc.", "NB", ("Reno", "NV"), None, 4),
        ("Bramlett Home Loans, LLC", "NB", ("Franklin", "TN"), None, 3),
        ("Wendrake Mortgage, Inc.", "NB", ("Coppell", "TX"), None, 3),
        ("Garrity Financial Mortgage, LLC", "NB", ("Cincinnati", "OH"), None, 2),
        ("Quarles Home Lending, LLC", "NB", ("Pasadena", "CA"), None, 2),
        ("Selden Mortgage Corp.", "NB", ("Jacksonville", "FL"), None, 2),
        ("Treadway Lending, LLC", "NB", ("Madison", "WI"), None, 1),
        ("Upshaw Mortgage, Inc.", "NB", ("Oklahoma City", "OK"), None, 1)]
BY = {x["id"]: x for x in L}
SHORTLIST = [x["id"] for x in L if x.get("short_list")]

OFFICES = {"BIG1": "none (loan officers in Salina)", "BIG2": "none", "BIG3": "none",
           "REG1": "Salina, McPherson", "REG2": "Salina, Abilene", "CUR2": "Salina",
           "CBR1": "Salina (2), Lindsborg", "N1": "Salina (3), Minneapolis", "N2": "McPherson, Salina, Lyons",
           "N3": "Hillsboro, Marion, Goessel", "N4": "Salina", "N5": "Abilene, Chapman"}

PEOPLE = {"research": "Laura Cohen", "director": "Maxwell Ewing"}


def lei(rng):
    """An ISO 17442 legal entity identifier: a four-character prefix, two zeros, twelve characters and two
    MOD 97-10 check digits."""
    alnum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    base = "549300" + "".join(alnum[i] for i in rng.integers(0, 36, 12))
    num = int("".join(str(int(ch, 36)) for ch in base + "00"))
    return base + "%02d" % (98 - num % 97)


def lei_ok(s):
    return len(s) == 20 and int("".join(str(int(ch, 36)) for ch in s)) % 97 == 1
