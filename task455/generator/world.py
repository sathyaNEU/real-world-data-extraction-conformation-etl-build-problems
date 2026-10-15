"""The Lornock Valley's private employers, 2024Q4 to 2026Q4: counties, ZIP codes, industries, the 2025 and 2026
events the data carries, the people and the files. Every number the simulation realises is set here."""
import datetime as dt

SEED = 455_2027
EXTRACT = dt.date(2027, 5, 14)
WIN0 = dt.date(2024, 10, 1)           # first day of the extract's first quarter
WIN1 = dt.date(2026, 12, 31)
GEOCODE_FROM = (2025, 3)              # quarterly reports from 2025Q3 carry the geocoded county
LEGACY_CUTOVER = dt.date(2025, 1, 1)  # the UI tax system's replacement went live; accounts opened before are legacy
TAXABLE_BASE = 14_500                 # state taxable wage base per worker per account per calendar year
QUARTERS = [(2024, 4)] + [(y, q) for y in (2025, 2026) for q in (1, 2, 3, 4)]

ORG_LMI = "Department of Workforce Services, Labor Market Information Bureau"
ORG_UI = "Department of Workforce Services, Unemployment Insurance Tax Unit"
ORG_COMMERCE = "Department of Commerce, Office of Business Development"
PEOPLE = {"economist": "Kristy Townsend", "director": "Brandon Compton", "supervisor": "Chelsey Hensley"}

FILES = {
    "register": "ui_employer_register_extract_2027-05-14.csv",
    "qcew": "qcew_private_establishments_2024q4_2026q4.csv",
    "wages": "ui_wage_records_2024q4_2026q4.txt",
    "guideline": "formation_counties_program_guideline_2027.pdf",
    "dict": "lmi_research_extract_dictionary.xlsx",
    "manifest": "extract_manifest_2027-05-14.csv",
    "counties": "lornock_county_codes.csv",
    "pop": "lornock_county_population_estimates_2020_2026.csv",
    "sos": "sos_new_entity_filings_2025_2026.csv",
    "grants": "formation_grant_disbursements_fy2026.xlsx",
}
DISTRACTORS = ["pop", "sos", "grants"]

# county code, name, seat, ZIP codes (ZIP, postal town); codes are the state's three-digit county codes
COUNTIES = [
    ("011", "Brennock", "Brennock", [("56801", "Brennock"), ("56803", "Brennock"), ("56807", "Halloway"),
                                      ("56809", "Corriston")]),
    ("019", "Caldmere", "Caldmere", [("56821", "Caldmere"), ("56824", "Wexley"), ("56826", "Pruitt Crossing")]),
    ("027", "Dunrath", "Dunrath", [("56831", "Dunrath"), ("56833", "Hollin"), ("56836", "Dunrath"),
                                    ("56838", "Marrow")]),
    ("041", "Eskwell", "Eskwell", [("56842", "Eskwell"), ("56845", "Larkin Bay"), ("56847", "Tindall")]),
    ("053", "Fennamore", "Fennamore", [("56852", "Fennamore"), ("56854", "Oakridge"), ("56857", "Bellmont")]),
    ("077", "Quarrin", "Quarrin", [("56861", "Quarrin"), ("56863", "Saddler"), ("56866", "Northam")]),
    ("089", "Tolbeck", "Tolbeck", [("56871", "Tolbeck"), ("56874", "Grissom"), ("56878", "Ardley")]),
]
CODE = {name: code for code, name, _, _ in COUNTIES}
NAME = {code: name for code, name, _, _ in COUNTIES}
ORDER = [name for _, name, _, _ in COUNTIES]

# ZIP codes that cross a county line: (ZIP, the ZIP's county, the county its minority part lies in, establishments in
# the minority part reporting employment in 2024Q4)
BORDER = [
    ("56809", "Brennock", "Caldmere", 22), ("56803", "Brennock", "Dunrath", 30), ("56833", "Dunrath", "Eskwell", 5),
    ("56838", "Dunrath", "Brennock", 8), ("56847", "Eskwell", "Quarrin", 24), ("56866", "Quarrin", "Tolbeck", 4),
    ("56863", "Quarrin", "Eskwell", 4), ("56874", "Tolbeck", "Fennamore", 20), ("56857", "Fennamore", "Brennock", 10),
    ("56826", "Caldmere", "Fennamore", 6),
]

# 2025 births opening and 2025 closures last employing in the first half of 2025 in each border ZIP's minority part
BORDER_BIRTHS = {"56809": 0, "56803": 1, "56833": 3, "56838": 0, "56847": 2, "56866": 3, "56863": 1, "56874": 0,
                 "56857": 4, "56826": 2}
BORDER_DEATHS = dict(BORDER_BIRTHS)
# closures added last, from their own random stream: (closing in 2024Q4, closing in the first nine months of 2025)
NUDGE = {"Brennock": (0, 1), "Caldmere": (0, 0), "Dunrath": (0, 1), "Eskwell": (0, 2), "Fennamore": (0, 0),
         "Quarrin": (0, 0), "Tolbeck": (0, 0)}
# 2024Q4 closures and births per county (texture for the extract's first quarter)
Q424 = {"Brennock": (37, 36), "Caldmere": (15, 15), "Dunrath": (26, 27), "Eskwell": (16, 17), "Fennamore": (23, 24),
        "Quarrin": (18, 19), "Tolbeck": (13, 13)}
# incumbents adding positions (expansions) and positions left unfilled (contractions), 2025 and 2026
EXPAND = 0.24
CONTRACT = 0.09

# Industries: (NAICS 2022, NAICS 2017, short noun for names, mean monthly wage, mean tenure in months, size profile,
# relative weight by county family). Size profiles: micro, small, mid.
INDUSTRIES = [
    ("236118", "236118", "Remodeling", 4650, 30, "small"), ("238220", "238220", "Plumbing & Heating", 5250, 40, "small"),
    ("238210", "238210", "Electric", 5420, 40, "small"), ("238990", "238990", "Contracting", 4480, 28, "small"),
    ("332710", "332710", "Machine", 5080, 44, "mid"), ("332322", "332322", "Sheet Metal", 4760, 40, "mid"),
    ("337110", "337110", "Cabinetry", 4120, 36, "mid"), ("311811", "311811", "Bakery", 2640, 16, "small"),
    ("424410", "424410", "Foods", 4870, 36, "mid"), ("423830", "423830", "Equipment", 5660, 48, "mid"),
    ("445110", "445110", "Grocery", 2530, 18, "mid"), ("445131", "445120", "Corner Store", 2310, 12, "small"),
    ("457110", "447110", "Fuel", 2420, 12, "small"), ("444140", "444130", "Hardware", 2740, 22, "small"),
    ("441330", "441310", "Auto Parts", 3050, 26, "small"), ("459110", "451110", "Outfitters", 2330, 18, "small"),
    ("455219", "452319", "Variety", 2210, 14, "small"), ("456110", "446110", "Pharmacy", 3620, 34, "small"),
    ("459999", "453998", "Goods", 2290, 20, "micro"), ("459420", "453220", "Gifts", 2120, 18, "micro"),
    ("459510", "453310", "Resale", 2010, 20, "micro"), ("458110", "448140", "Clothing", 2040, 16, "micro"),
    ("459210", "451211", "Books", 1930, 24, "micro"), ("811111", "811111", "Auto Repair", 3810, 36, "small"),
    ("811310", "811310", "Machinery Repair", 4920, 42, "small"), ("812112", "812112", "Salon", 2030, 26, "micro"),
    ("812111", "812111", "Barbers", 2110, 30, "micro"), ("722511", "722511", "Grill", 1930, 10, "small"),
    ("722513", "722513", "Kitchen", 1720, 8, "small"), ("722515", "722515", "Coffee", 1640, 9, "micro"),
    ("713940", "713940", "Fitness", 1810, 14, "micro"), ("621111", "621111", "Family Medicine", 7240, 54, "small"),
    ("621210", "621210", "Dental", 5630, 50, "small"), ("624120", "624120", "Home Care", 2630, 14, "mid"),
    ("541110", "541110", "Law", 6540, 60, "micro"), ("541211", "541211", "Accounting", 5810, 56, "micro"),
    ("531210", "531210", "Realty", 4210, 40, "micro"), ("484121", "484121", "Freight", 5020, 30, "small"),
    ("561730", "561730", "Landscaping", 2920, 18, "small"),
]
# industry codes a re-registered business reported for itself at registration (the old account carried the code the
# bureau's review had settled)
ALT_CODE = {"332710": "332721", "332322": "332313", "337110": "337212", "238220": "238290", "238210": "238290",
            "423830": "423840", "484121": "484110", "424410": "424490", "236118": "236115", "811310": "811490",
            "457110": "445131"}
# storefront trades: the lines of business that take over a vacated downtown storefront
STOREFRONT = ["311811", "444140", "459110", "455219", "456110", "459999", "459420", "459510", "458110", "459210",
              "812112", "812111", "722511", "722513", "722515", "713940", "541110", "541211", "531210", "621210"]
SEASONAL_INDUSTRIES = [("713990", "713990", "Recreation", 1730), ("721211", "721211", "Campground", 1910),
                       ("722515", "722515", "Ice Cream", 1580), ("713930", "713930", "Marina", 2240),
                       ("561730", "561730", "Lawn & Garden", 2810)]
TITLES = {
    "236118": "Residential Remodelers", "238220": "Plumbing, Heating, and Air-Conditioning Contractors",
    "238210": "Electrical Contractors and Other Wiring Installation Contractors",
    "238990": "All Other Specialty Trade Contractors", "332710": "Machine Shops", "332322": "Sheet Metal Work Manufacturing",
    "337110": "Wood Kitchen Cabinet and Countertop Manufacturing", "311811": "Retail Bakeries",
    "424410": "General Line Grocery Merchant Wholesalers",
    "423830": "Industrial Machinery and Equipment Merchant Wholesalers",
    "445110": "Supermarkets and Other Grocery Retailers (except Convenience Retailers)", "445131": "Convenience Retailers",
    "457110": "Gasoline Stations with Convenience Stores", "444140": "Hardware Retailers",
    "441330": "Automotive Parts and Accessories Retailers", "459110": "Sporting Goods Retailers",
    "455219": "All Other General Merchandise Retailers", "456110": "Pharmacies and Drug Retailers",
    "459999": "All Other Miscellaneous Retailers", "459420": "Gift, Novelty, and Souvenir Retailers",
    "459510": "Used Merchandise Retailers", "458110": "Clothing and Clothing Accessories Retailers",
    "459210": "Book Retailers and News Dealers", "811111": "General Automotive Repair",
    "811310": "Commercial and Industrial Machinery and Equipment (except Automotive and Electronic) Repair and Maintenance",
    "812112": "Beauty Salons", "812111": "Barber Shops", "722511": "Full-Service Restaurants",
    "722513": "Limited-Service Restaurants", "722515": "Snack and Nonalcoholic Beverage Bars",
    "713940": "Fitness and Recreational Sports Centers", "621111": "Offices of Physicians (except Mental Health Specialists)",
    "621210": "Offices of Dentists", "624120": "Services for the Elderly and Persons with Disabilities",
    "541110": "Offices of Lawyers", "541211": "Offices of Certified Public Accountants",
    "531210": "Offices of Real Estate Agents and Brokers", "484121": "General Freight Trucking, Long-Distance, Truckload",
    "561730": "Landscaping Services", "713990": "All Other Amusement and Recreation Industries",
    "721211": "RV (Recreational Vehicle) Parks and Campgrounds", "713930": "Marinas",
    "332721": "Precision Turned Product Manufacturing", "332313": "Plate Work Manufacturing",
    "337212": "Custom Architectural Woodwork and Millwork Manufacturing",
    "238290": "Other Building Equipment Contractors", "423840": "Industrial Supplies Merchant Wholesalers",
    "484110": "General Freight Trucking, Local", "424490": "Other Grocery and Related Products Merchant Wholesalers",
    "236115": "New Single-Family Housing Construction (except For-Sale Builders)",
    "811490": "Other Personal and Household Goods Repair and Maintenance",
}

# County industry tilt: multipliers on the base weights by industry group
TILT = {
    "Brennock": {"621": 1.4, "541": 1.5, "531": 1.3, "423": 1.2},
    "Caldmere": {"457": 1.6, "445": 1.3, "441": 1.2, "484": 1.3},
    "Dunrath": {"236": 1.2, "238": 1.2, "722": 1.1, "624": 1.3},
    "Eskwell": {"722": 1.5, "713": 1.6, "459": 1.3, "812": 1.1},
    "Fennamore": {"332": 1.6, "337": 1.4, "484": 1.4, "811": 1.2},
    "Quarrin": {"722": 1.4, "459": 1.5, "458": 1.5, "812": 1.3},
    "Tolbeck": {"332": 1.5, "238": 1.3, "423": 1.3, "561": 1.2},
}

# 2026: the year the call reads. T true births (re-lets among them R, of which adjacent, a different industry and the
# old tenant stopping the quarter before), F filed successors, Us unfiled continuations at the same address (Caldmere's
# include the nineteen stores), Um unfiled continuations that moved into the county, B the 2025Q4 base.
Y26 = {
    "Brennock":  dict(B=1618, T=113, R=6,  Radj=2, F=14, Us=7,  Um=2),
    "Caldmere":  dict(B=702,  T=55,  R=2,  Radj=1, F=6,  Us=23, Um=0),
    "Dunrath":   dict(B=1236, T=121, R=4,  Radj=1, F=9,  Us=4,  Um=1),
    "Eskwell":   dict(B=759,  T=86,  R=3,  Radj=1, F=7,  Us=4,  Um=1),
    "Fennamore": dict(B=1104, T=73,  R=4,  Radj=1, F=10, Us=4,  Um=1),
    "Quarrin":   dict(B=863,  T=82,  R=24, Radj=11, F=5, Us=3,  Um=0),
    "Tolbeck":   dict(B=612,  T=44,  R=1,  Radj=0, F=5,  Us=1,  Um=21),
}
CHAIN = 19                       # Caldmere's fuel and convenience stores, sold at the end of 2026Q1
# Tolbeck's enterprise park: the counties the relocated businesses came from, and the quarter each moved in
PARK_FROM = {"Brennock": 8, "Dunrath": 4, "Fennamore": 5, "Caldmere": 2, "Quarrin": 1, "Eskwell": 1}
PARK_QUARTERS = [1] * 8 + [2] * 7 + [3] * 6
# the other moved continuations: (county the successor is in, county the source was in)
MOVED_OTHER = [("Brennock", "Brennock"), ("Brennock", "Dunrath"), ("Dunrath", "Brennock"), ("Eskwell", "Quarrin"),
               ("Fennamore", "Fennamore")]
# 2026 births that changed hands within 2026 (the successor is among the county's Us)
RESOLD_2026 = ["Brennock", "Dunrath"]
D26 = {"Brennock": 117, "Caldmere": 52, "Dunrath": 88, "Eskwell": 49, "Fennamore": 84, "Quarrin": 61, "Tolbeck": 42}
NEVER_EMPLOYED_2026 = {"Brennock": 4, "Caldmere": 1, "Dunrath": 3, "Eskwell": 2, "Fennamore": 2, "Quarrin": 1,
                       "Tolbeck": 1}

# 2025: the asks' year. T true births (R re-lets), F filed successors, U unfiled same-address continuations, Um moved,
# D true deaths among the incumbents (2025 births that close within 2025 come on top), S summer employers, Dr dormant
# accounts resuming in 2025, Sx summer employers that did not reopen in 2026.
Y25 = {
    "Brennock":  dict(T=118, R=3, F=12, U=4, Um=1, D=104, S=16, Dr=3, Sx=2),
    "Caldmere":  dict(T=52,  R=1, F=5,  U=2, Um=0, D=49,  S=9,  Dr=1, Sx=1),
    "Dunrath":   dict(T=104, R=2, F=9,  U=3, Um=1, D=82,  S=15, Dr=2, Sx=1),
    "Eskwell":   dict(T=77,  R=2, F=6,  U=3, Um=0, D=47,  S=21, Dr=2, Sx=2),
    "Fennamore": dict(T=81,  R=2, F=9,  U=3, Um=1, D=80,  S=11, Dr=2, Sx=1),
    "Quarrin":   dict(T=63,  R=3, F=7,  U=2, Um=0, D=77,  S=17, Dr=1, Sx=2),
    "Tolbeck":   dict(T=47,  R=1, F=4,  U=2, Um=0, D=41,  S=8,  Dr=1, Sx=1),
}
# share of 2025 births that close within 2025, and share of births of either year closing in 2026
SHORT_LIVED_25 = 0.07
CLOSE_26_OF_25 = 0.08
CLOSE_26_OF_26 = 0.04

# Quarrin's downtown: share of its 2026 births (three workers or more) that hired one worker from an account that
# stopped reporting the quarter before; elsewhere the share is lower
DISPLACED_HIRE = {"Quarrin": 0.42, "default": 0.06}

STREETS = ["Main", "Mill", "Church", "Elm", "Oak", "Maple", "Cedar", "Lake", "River", "Ridge", "Hill", "Park",
           "Center", "Depot", "Market", "Union", "Spring", "Walnut", "Pine", "Juniper", "Grange", "Railroad",
           "School", "Commerce", "Industrial", "Prairie", "Orchard", "Willow", "Birch", "Granite", "Quarry",
           "Harbor", "Bluff", "Meadow", "Fairground", "Courthouse", "Canal", "Summit", "Frontage", "Airport"]
STREET_TYPES = [("Street", "ST"), ("Road", "RD"), ("Avenue", "AVE"), ("Drive", "DR"), ("Lane", "LN"),
                ("Boulevard", "BLVD"), ("Court", "CT"), ("Way", "WAY"), ("Parkway", "PKWY")]
DIRECTIONS = [("North", "N"), ("South", "S"), ("East", "E"), ("West", "W")]
PLACE_WORDS = ["Lakeside", "Ridgeline", "Creekside", "Cedar", "Juniper", "Granite", "Prairie", "Northfork", "Valley",
               "Bluewater", "Timberline", "Ironwood", "Stonegate", "Riverbend", "Highland", "Fieldstone", "Kestrel",
               "Copperleaf", "Westgate", "Elk Run", "Pinecrest", "Larchmont", "Brookside", "Millrace", "Sandbar",
               "Heron", "Foxglove", "Clearwater", "Saltlick", "Redtail", "Silverleaf", "Oxbow", "Tamarack", "Wren",
               "Basin", "Summit", "Hollow", "Bramble", "Gristmill", "Lantern"]
PARK_STREET = ("Kessler", "Way", "WAY")      # Tolbeck Enterprise Park's main street
DOWNTOWN = {"Quarrin": [("Main", "Street", "ST"), ("Depot", "Street", "ST"), ("Market", "Street", "ST"),
                        ("Courthouse", "Square", "SQ")]}
