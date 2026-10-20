"""task249 world constants: a Western Norwegian hydropower company's 14 suspended-sediment stations on the rivers
feeding its three reservoirs, the field team, the contract laboratory and the documents' dates."""
import datetime as dt

ORG = "Vasslia Miljørådgiving AS"          # the environmental consultancy that runs the programme under contract
CLIENT = "Fjellbrekke Kraft AS"            # the hydropower company that owns the stations and the reservoirs
PROGRAMME = "Fjellbrekke sediment monitoring programme"
DOMAIN = "vasslia.no"
LAB = "Sogn Miljøanalyse AS"
LAB_DOMAIN = "sognmiljoanalyse.no"

# people, from guard.py names --geo Norway --seed 249
DATA_MANAGER = ("Marianne Lunde", "marianne.lunde")      # the programme's data manager, asks
LAB_QA = ("Laila Pedersen", "laila.pedersen")            # the laboratory's quality manager
FIELD_LEAD = ("Lise Pettersen", "lise.pettersen")        # field team lead

AS_OF = dt.date(2028, 3, 6)            # Monday: the review starts
REPORT_DATE = dt.date(2028, 2, 15)     # the 2027 sediment report went out
PLAN_DATE = dt.date(2028, 3, 20)       # the flushing plan is fixed

YEARS = (2025, 2026, 2027)
T0 = dt.datetime(2025, 1, 1, tzinfo=dt.timezone.utc)

OLD_SENSOR = "Turbitek TS-10"
OLD_LIMIT = 1000.0
NEW_SENSOR = "Turbitek TS-40W"
NEW_LIMIT = 4000.0

REVIEW_TOLERANCE = 15.0   # per cent, either way

# kind, sand, crew_lag_h, crew_sd_h, callouts_per_year, routine_hour_utc, winter_routine, extra
SPEC = {
    "G1": ("glacier", 1.25, 4, 2, 5, 11.0, False, {}),
    "G2": ("glacier", 0.10, 5, 2, 6, 11.0, False, {}),
    "G3": ("glacier", 0.25, 5, 2, 4, 11.0, True, {}),
    "G4": ("glacier", 1.80, 30, 10, 0, 10.5, False, {"rounds_per_month": 2}),
    "G5": ("glacier", 0.20, 6, 3, 6, 11.0, True, {}),
    "G6": ("glacier", 1.20, 5, 2, 6, 10.5, False, {}),
    "R1": ("rain", 1.30, 3, 1.5, 9, 11.0, True, {}),
    "R2": ("rain", 1.20, 16, 13, 10, 11.0, True, {}),
    "R3": ("rain", 0.15, 4, 2, 8, 11.0, True, {}),
    "R4": ("rain", 0.00, 5, 2, 8, 11.0, True, {}),
    "R5": ("rain", 1.30, 22, 10, 10, 11.0, True, {}),
    "L1": ("lake", 0.05, 5, 2, 6, 11.0, True, {}),
    "L2": ("lake", 0.10, 20, 8, 6, 11.0, True, {}),
    "L3": ("lake", 0.00, 6, 3, 6, 11.0, True, {}),
}
SEED = {"G1": 5014, "G2": 5100, "G3": 5210, "G4": 5359, "G5": 5401, "G6": 5509, "R1": 5600, "R2": 5700,
        "R3": 5800, "R4": 5900, "R5": 6002, "L1": 6100, "L2": 6200, "L3": 6300}

# station register: model key -> (code, name, river, reservoir, catchment km2, glacier per cent, turbidity scale FNU)
STATIONS = [
    ("G1", "SKB", "Skardbreelvi ved Fossbru", "Skardbreelvi", "Breiavatn", 46.2, 38, 45.0),
    ("G2", "KVF", "Kvitfonnelvi ovf. inntak", "Kvitfonnelvi", "Breiavatn", 31.8, 44, 30.0),
    ("G3", "MKE", "Morkaelvi ved Steinbru", "Morkaelvi", "Breiavatn", 58.4, 21, 36.0),
    ("G4", "JVB", "Juvbreelvi ved Juvstøl", "Juvbreelvi", "Kvitstølvatn", 27.5, 52, 60.0),
    ("G5", "HGE", "Hogstølelvi", "Hogstølelvi", "Kvitstølvatn", 39.0, 17, 40.0),
    ("G6", "FND", "Fonnadalselvi ved Bruhaug", "Fonnadalselvi", "Djupevatn", 64.7, 29, 50.0),
    ("R1", "ESK", "Eskelandselvi", "Eskelandselvi", "Breiavatn", 22.3, 0, 36.0),
    ("R2", "TVE", "Tverrelvi ved Lid", "Tverrelvi", "Kvitstølvatn", 18.6, 0, 26.0),
    ("R3", "GRV", "Grovelvi", "Grovelvi", "Djupevatn", 25.1, 0, 22.0),
    ("R4", "SVK", "Sandvikelvi", "Sandvikelvi", "Djupevatn", 14.9, 0, 18.0),
    ("R5", "HSD", "Haugsdalselvi", "Haugsdalselvi", "Breiavatn", 29.7, 0, 28.0),
    ("L1", "BLU", "Blåvatn utløp", "Blåvatnelvi", "Breiavatn", 41.3, 6, 6.0),
    ("L2", "SLU", "Svartevatn utløp", "Svartevatnelvi", "Kvitstølvatn", 36.0, 3, 5.0),
    ("L3", "LLU", "Langevatn utløp", "Langevatnelvi", "Djupevatn", 52.6, 9, 4.0),
]
KEYS = [s[0] for s in STATIONS]
CODE = {s[0]: s[1] for s in STATIONS}
NAME = {s[0]: s[2] for s in STATIONS}
TSCALE = {s[0]: s[7] for s in STATIONS}
AREA = {s[0]: s[5] for s in STATIONS}
KIND_LABEL = {"glacier": "glacier-fed", "rain": "rain-fed", "lake": "lake outlet"}
