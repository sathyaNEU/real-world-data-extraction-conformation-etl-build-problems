"""Constants for task264: the Daskbeck Valley Regional Park Authority, its six parks, its nine member councils and
their settlements, the 2025-26 visitor survey's calendar and strata, the levy figures and the pack's file names."""
import datetime as dt

AUTH = "Daskbeck Valley Regional Park Authority"
AUTH_SHORT = "DVRPA"
CONTRACTOR = "Ellshaw Research"
PEOPLE = {"finance": "Claire Foster", "contractor": "Toby Houghton", "clerk": "Rachael Rowley"}

# code, council, its main town, valley council (holds parks)
COUNCILS = [
    ("KDM", "Keldmere District Council", "Keldmere", True),
    ("RVW", "Ravenwick Borough Council", "Ravenwick", True),
    ("SNG", "Snelgarth District Council", "Snelgarth", True),
    ("LKS", "Larkstead Borough Council", "Larkstead", False),
    ("GRB", "Grinbury District Council", "Grinbury", False),
    ("HNM", "Hornmere District Council", "Hornmere", False),
    ("CHD", "Chaldale District Council", "Chaldale", False),
    ("WDS", "Wendstow District Council", "Wendstow", False),
    ("FNC", "Ferncote Borough Council", "Ferncote", False),
]
CODES = [c[0] for c in COUNCILS]
NAME = {c[0]: c[1] for c in COUNCILS}
SHORT = {c[0]: c[2] for c in COUNCILS}
VALLEY = [c[0] for c in COUNCILS if c[3]]
OUTER = [c[0] for c in COUNCILS if not c[3]]

# park code, name, host council, charging car park
PARKS = [
    ("BW", "Brathden Woods", "KDM", False),
    ("CC", "Crowside Common", "KDM", False),
    ("GF", "Gorthfield Country Park", "RVW", True),
    ("DW", "Daskbeck Water Park", "RVW", True),
    ("LM", "Lockshaw Moor", "SNG", True),
    ("TH", "Thruscote Hall", "SNG", True),
]
PARK_CODES = [p[0] for p in PARKS]
PARK_NAME = {p[0]: p[1] for p in PARKS}
PARK_HOST = {p[0]: p[2] for p in PARKS}
CHARGING = [p[0] for p in PARKS if p[3]]

# settlements: the main town first, then villages; the gazetteer and the survey's home places use these
SETTLEMENTS = {
    "KDM": ["Keldmere", "Elmthwaite", "Hobside", "Ackhope", "Plumbeck", "Rogcote"],
    "RVW": ["Ravenwick", "Oakthwaite", "Shelhaugh", "Pudmere", "Hepsett", "Clunside"],
    "SNG": ["Snelgarth", "Fernsett", "Keldcote", "Ostshaw", "Wendkirk", "Garnhope"],
    "LKS": ["Larkstead", "Brambeck", "Tibmere", "Swalbeck", "Oxgarth", "Lockstow"],
    "GRB": ["Grinbury", "Horngate", "Polshaw", "Ridmoor", "Quenstead", "Dibhope"],
    "HNM": ["Hornmere", "Larkcote", "Eldgarth", "Thruswick", "Quenwold", "Bixgarth"],
    "CHD": ["Chaldale", "Rushgarth", "Wilhaugh", "Brockcote", "Fawthwaite", "Haghope"],
    "WDS": ["Wendstow", "Clunbeck", "Ockstead", "Sowgarth", "Galhaugh", "Yarbeck"],
    "FNC": ["Ferncote", "Tibhope", "Melsett", "Carlhope", "Ravenmere", "Snelwold"],
}
# where visitors from outside the member councils say they live (real places, as respondents give them)
OUTSIDE_PLACES = ["Leeds", "York", "Harrogate", "Bradford", "Manchester", "Sheffield", "Wakefield", "Huddersfield",
                  "Halifax", "Lancaster", "Preston", "Darlington", "Durham", "Newcastle upon Tyne", "Middlesbrough",
                  "Hull", "Doncaster", "Liverpool", "Nottingham", "Birmingham", "London", "Skipton", "Ripon",
                  "Scarborough", "Kendal", "Edinburgh", "Glasgow", "Lincoln", "Chester", "Stockport"]

YEAR0 = dt.date(2025, 4, 1)
YEAR1 = dt.date(2026, 3, 31)
SEASONS = [("SP", "Spring", dt.date(2025, 4, 1), dt.date(2025, 6, 30)),
           ("SU", "Summer", dt.date(2025, 7, 1), dt.date(2025, 9, 30)),
           ("AU", "Autumn", dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
           ("WI", "Winter", dt.date(2026, 1, 1), dt.date(2026, 3, 31))]
SEASON_CODES = [s[0] for s in SEASONS]
DAYTYPES = ["WD", "WE"]                      # weekday; weekend or bank holiday
BANK_HOLIDAYS = {dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5), dt.date(2025, 5, 26),
                 dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
STRATA = [(p, s, d) for p in PARK_CODES for s in SEASON_CODES for d in DAYTYPES]
SI = {st: i for i, st in enumerate(STRATA)}


def daytype(d):
    return "WE" if d.weekday() >= 5 or d in BANK_HOLIDAYS else "WD"


def season(d):
    for code, _, a, b in SEASONS:
        if a <= d <= b:
            return code
    raise ValueError(d)


def days_of(s, d):
    a, b = [(x[2], x[3]) for x in SEASONS if x[0] == s][0]
    out, x = [], a
    while x <= b:
        if daytype(x) == d:
            out.append(x)
        x += dt.timedelta(days=1)
    return out


# car parks at the four charging parks; the share of a park's vehicles each takes
CAR_PARKS = [("GF-M", "Gorthfield main car park", "GF", .68), ("GF-L", "Gorthfield lakeside car park", "GF", .32),
             ("DW-1", "Daskbeck Water Park car park", "DW", 1.0), ("LM-S", "Lockshaw Moor summit car park", "LM", .57),
             ("LM-V", "Lockshaw Moor valley car park", "LM", .43), ("TH-1", "Thruscote Hall car park", "TH", 1.0)]
CP_CODES = [c[0] for c in CAR_PARKS]
CP_NAME = {c[0]: c[1] for c in CAR_PARKS}
CP_PARK = {c[0]: c[2] for c in CAR_PARKS}
CP_SPLIT = {c[0]: c[3] for c in CAR_PARKS}
CAR_SHARE = {"GF": .78, "DW": .86, "LM": .81, "TH": .88}       # adult visits arriving by car
OCCUPANCY = {"GF": 2.2, "DW": 2.5, "LM": 2.1, "TH": 2.3}       # adults per car
APP_SHARE = {"GF": .52, "DW": .61, "LM": .43, "TH": .55}       # paying vehicles that paid through the app
BANDS = ["1H", "2H", "4H", "DAY"]
BAND_NAME = {"1H": "Up to 1 hour", "2H": "Up to 2 hours", "4H": "Up to 4 hours", "DAY": "All day"}
# tariffs including VAT; the Water Park charges more in its high season (1 July to 31 August)
TARIFF = {"GF": [1.50, 3.00, 4.50, 6.50], "DW": [2.00, 3.50, 5.50, 8.00], "LM": [1.50, 2.80, 4.20, 6.00],
          "TH": [2.00, 3.50, 5.00, 7.00]}
TARIFF_HIGH = {"DW": [2.50, 4.00, 6.50, 9.50]}
HIGH_SEASON = (dt.date(2025, 7, 1), dt.date(2025, 8, 31))
VAT = 0.20
# pay machines: the car park each stood in, and when
MACHINES = [("PM-2101", "GF-M", None, None), ("PM-2102", "GF-M", None, None),
            ("PM-2103", "GF-M", None, dt.date(2025, 8, 31)), ("PM-2103", "DW-1", dt.date(2025, 9, 1), None),
            ("PM-2104", "GF-L", None, None), ("PM-2201", "DW-1", None, None), ("PM-2202", "DW-1", None, None),
            ("PM-2203", "DW-1", None, dt.date(2025, 8, 31)), ("PM-2301", "LM-S", None, None),
            ("PM-2302", "LM-V", None, None), ("PM-2401", "TH-1", None, None), ("PM-2402", "TH-1", None, None)]
# vehicle counters at the car-park entrances, the car park each stood at, and when
COUNTERS = [("C-01", "GF-M", None, None, "SX-1"), ("C-05", "GF-L", None, dt.date(2026, 2, 24), "SX-1"),
            ("C-10", "GF-L", dt.date(2026, 2, 3), None, "SX-2"), ("C-04", "DW-1", None, dt.date(2025, 8, 18), "SX-1"),
            ("C-09", "DW-1", dt.date(2025, 8, 18), None, "BX-2"), ("C-06", "LM-S", None, None, "SX-1"),
            ("C-08", "LM-V", None, dt.date(2025, 10, 14), "SX-1"), ("C-07", "TH-1", None, dt.date(2025, 10, 14), "SX-1"),
            ("C-07", "LM-V", dt.date(2025, 10, 14), None, "SX-1"), ("C-11", "TH-1", dt.date(2025, 10, 14), None, "SX-2")]

LEVY_2027 = 7416300          # the 2027-28 levy requirement, pounds
LEVY_2026 = 7190800          # 2026-27, apportioned by population (the last year on the old basis)
LEVY_2025 = 6982400          # 2025-26, apportioned by population
LEVY_2024 = 6783700          # 2024-25, apportioned by population

FILES = {
    "wave1": "dvrpa_visitor_survey_2025-26_wave1.xlsx",
    "wave2": "dvrpa_visitor_survey_2025-26_wave2.csv",
    "weights": "survey_weights_2025-26.csv",
    "fieldnote": "fieldwork_and_weighting_note_2025-26.pdf",
    "codebook": "survey_codebook_2025-26.xlsx",
    "gazetteer": "dvrpa_settlement_gazetteer.csv",
    "levypapers": "levy_papers_2027-28.pdf",
    "machines": "pay_machine_transactions_2025-26.csv",
    "app": "parking_app_statements_2025-26.xlsx",
    "tariffs": "car_park_tariffs_2025-26.xlsx",
    "assets": "car_park_asset_register.csv",
    "counts": "car_park_counts_hourly_2025-26.csv",
    "invoices": "levy_invoices_2025-26.csv",
    "receipts": "bank_receipts_2025-26.csv",
    "remittances": "remittance_advices_2025-26.csv",
    "payments": "supplier_payments_2025-26.csv",
    "permits": "annual_permits_2025-26.csv",
    "population": "population_estimates_mid-2025.xlsx",
    "manifest": "export_manifest.csv",
}
