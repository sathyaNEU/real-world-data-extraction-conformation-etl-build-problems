"""Constants for task275: the Wrayburn Coast Fish Producers' Organisation, its eight fleet segments, the five grounds,
the species, the ports, the buyers, the people, the dates and the pack's file names."""
import datetime as dt

SEED = 6
YEAR = 2025
PO = "Wrayburn Coast Fish Producers' Organisation"
PO_SHORT = "WCFPO"
COMPANY = PO
SCHEME = "Wrayburn Coast At-Sea Observer Scheme"
ASSEMBLED = dt.datetime(2026, 11, 6, 10, 30)
REQUEST_DATE = dt.date(2026, 11, 9)
BOARD_DATE = dt.date(2026, 12, 8)
TERMS_DATE = dt.date(2026, 10, 14)
THRESHOLD = 10.0

# code, name, gear code, length class, towed
SEGMENTS = [
    ("TR1", "Demersal otter trawl, 18 m and over", "OTB", "18m+", True),
    ("TR2", "Demersal otter trawl, 12 m to under 18 m", "OTB", "12-18m", True),
    ("NEP", "Nephrops trawl", "OTB", "12m+", True),
    ("BT", "Beam trawl", "TBB", "12m+", True),
    ("SN", "Seine", "SDN", "12m+", True),
    ("GN", "Set gillnet", "GNS", "10m+", False),
    ("LL", "Set longline", "LLS", "10m+", False),
    ("POT", "Pots and creels", "FPO", "10m+", False),
]
SEG = [s[0] for s in SEGMENTS]
SEG_NAME = {s[0]: s[1] for s in SEGMENTS}

# code, name, depth band, sediment, distance offshore (nm), centre (lat, lon), half-size (lat, lon)
GROUNDS = [
    ("WC11", "Dunsellan Bank", "60-90 m", "gravel and coarse sand", 28, (53.46, -11.86), (0.09, 0.14)),
    ("WC12", "Marrowbank", "40-60 m", "sand and shell", 14, (53.06, -11.43), (0.08, 0.12)),
    ("WC13", "Ravensker Deep", "90-140 m", "mud", 41, (53.24, -12.16), (0.10, 0.15)),
    ("WC14", "Ashcombe Bay", "10-25 m", "fine sand", 4, (53.56, -11.12), (0.05, 0.07)),
    ("WC15", "Corrieness", "15-35 m", "muddy sand", 7, (52.86, -11.19), (0.05, 0.08)),
]
GR = [g[0] for g in GROUNDS]
GR_NAME = {g[0]: g[1] for g in GROUNDS}
NURSERY = ("WC14", "WC15")      # the generator's own knowledge; no shipped file flags them

# FAO code, name, quota species under the landing obligation, MCRS in cm, survivability exemption, conversion
# factor of the usual presentation, presentation, price (GBP a kg of product weight, grade 2, mid-year)
SPECIES = {
    "COD": ("Cod", True, 35, False, 1.17, "GUT", 3.10),
    "HAD": ("Haddock", True, 30, False, 1.17, "GUT", 1.85),
    "WHG": ("Whiting", True, 27, False, 1.18, "GUT", 1.25),
    "HKE": ("Hake", True, 27, False, 1.11, "GUT", 2.40),
    "PLE": ("Plaice", True, 27, False, 1.00, "WHL", 1.70),
    "SOL": ("Sole", True, 24, False, 1.00, "WHL", 9.80),
    "MON": ("Anglerfish", True, 0, False, 1.22, "GUT", 4.60),
    "MEG": ("Megrim", True, 25, False, 1.00, "WHL", 2.75),
    "LEM": ("Lemon sole", True, 25, False, 1.00, "WHL", 4.20),
    "POK": ("Saithe", True, 35, False, 1.19, "GUT", 1.05),
    "POL": ("Pollack", True, 30, False, 1.17, "GUT", 3.40),
    "LIN": ("Ling", True, 63, False, 1.14, "GUT", 1.95),
    "NEP": ("Norway lobster", True, 25, True, 1.00, "WHL", 6.30),
    "DAB": ("Dab", False, 0, False, 1.00, "WHL", 0.60),
    "GUR": ("Gurnards", False, 0, False, 1.00, "WHL", 0.85),
    "SYC": ("Lesser spotted dogfish", False, 0, False, 1.00, "WHL", 0.45),
    "CRE": ("Edible crab", False, 140, True, 1.00, "WHL", 2.15),
    "LBE": ("European lobster", False, 87, True, 1.00, "WHL", 16.50),
    "WHE": ("Whelk", False, 45, False, 1.00, "WHL", 1.10),
}
QUOTA = tuple(s for s, v in SPECIES.items() if v[1])

# code, port letters, name, harbour (lat, lon), port limit radius (nm), fish market auction
PORTS = [("KMH", "KE", "Kestlemouth", (53.618, -10.981), 2.0, True),
         ("PNW", "PM", "Penmarrow", (53.409, -11.028), 1.5, False),
         ("BRS", "BE", "Brindlesea", (53.177, -10.952), 2.0, True),
         ("CWK", "CW", "Cauldwick", (52.968, -11.061), 1.2, False),
         ("GLB", "GL", "Gullsby", (52.741, -10.993), 1.5, False)]
PORT = {p[0]: p for p in PORTS}

# registered buyers: code, name, kind (auction, merchant, shellfish), ports bought at
BUYERS = [
    ("RB0412", "Kestlemouth Harbour Fish Market", "auction", ("KMH",)),
    ("RB0437", "Brindlesea Fish Market Ltd", "auction", ("BRS",)),
    ("RB1186", "Barlow & Hobbs (Fish Merchants) Ltd", "merchant", ("PNW", "CWK")),
    ("RB1203", "Daly Seafoods Ltd", "merchant", ("PNW", "GLB")),
    ("RB1255", "Gullsby Fish Selling Co.", "merchant", ("GLB", "CWK")),
    ("RB1311", "Macdonald Fish Ltd", "merchant", ("CWK", "PNW", "GLB")),
    ("RB2040", "Penmarrow Shellfish Ltd", "shellfish", ("PNW", "KMH", "BRS", "CWK", "GLB")),
    ("RB2077", "Cauldwick Crab Company Ltd", "shellfish", ("CWK", "GLB", "BRS")),
]
DEVICE_BUYER = "RB1186"                 # files its auction purchases as sales notes from June (Ask A)
DEVICE_FROM = dt.date(2025, 8, 4)

PEOPLE = {
    "manager": "Aimee Hutchinson",       # science and compliance manager, the request's author
    "coordinator": "Graham James",       # the observer scheme's coordinator
    "data": "Ellie Arnold",               # data officer
    "ceo": "Connor Rogers",
    "chair": "Samantha Weston",
}
REQUESTER = PEOPLE["manager"]

FILES = {
    "contents": "README_files.txt",
    "terms": "selectivity_programme_terms_2027.pdf",
    "manual": "observer_scheme_manual_2025.pdf",
    "dictionary": "wcfpo_data_dictionary_2025.pdf",
    "register": "vessel_register.csv",
    "trips": "elogbook_trips_2025.csv",
    "landings": "elogbook_landings_2025.csv",
    "deploy": "observer_deployments_2025.csv",
    "hauls": "observer_hauls_2025.csv",
    "grounds": "fishing_grounds.csv",
    "species": "species_list.csv",
    "sales": "sales_notes_2025.csv",
    "vms": "vms_positions_2025.csv",
    "transponders": "vms_transponders.csv",
    "ports": "port_limits.csv",
    "quota": "quota_uptake_2025.xlsx",
    "gear": "gear_specifications_2025.csv",
}
DISTRACTORS = ("quota", "gear")
GOLDEN = "segment_discards_2025.xlsx"
CHART = "segment_discards_2025.png"
DELIVERABLES = (GOLDEN, CHART)


def bst(t):
    """True when a UTC datetime falls in British Summer Time (last Sunday of March to last Sunday of October, 01:00
    UTC)."""
    def last_sunday(y, m):
        d = dt.date(y, m, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    a = dt.datetime.combine(last_sunday(t.year, 3), dt.time(1))
    b = dt.datetime.combine(last_sunday(t.year, 10), dt.time(1))
    return a <= t < b


def to_local(t):
    return t + dt.timedelta(hours=1) if bst(t) else t


def to_utc(t_local):
    """local (UK) wall time to UTC; a wall time in the autumn's repeated hour is read as the first (BST) one"""
    u = t_local - dt.timedelta(hours=1)
    return u if bst(u) else t_local

SCIENTIFIC = {
    "COD": "Gadus morhua", "HAD": "Melanogrammus aeglefinus", "WHG": "Merlangius merlangus",
    "HKE": "Merluccius merluccius", "PLE": "Pleuronectes platessa", "SOL": "Solea solea", "MON": "Lophiidae",
    "MEG": "Lepidorhombus whiffiagonis", "LEM": "Microstomus kitt", "POK": "Pollachius virens",
    "POL": "Pollachius pollachius", "LIN": "Molva molva", "NEP": "Nephrops norvegicus", "DAB": "Limanda limanda",
    "GUR": "Triglidae", "SYC": "Scyliorhinus canicula", "CRE": "Cancer pagurus", "LBE": "Homarus gammarus",
    "WHE": "Buccinum undatum",
}

VESSEL_NAMES = [
    "Accord", "Adoration", "Amity", "Arcturus", "Aspire", "Atlantic Dawn", "Benarty", "Boy Callum", "Boy Daniel",
    "Boy Lewis", "Bountiful", "Brighter Morn", "Caledonia", "Carinthia", "Celtic Mist", "Chrysolite", "Comrades",
    "Concord", "Constant Friend", "Coral Strand", "Crimson Arrow", "Daystar", "Deliverance", "Dovetail", "Eilidh May",
    "Elizabeth Anne", "Emma Louise", "Endurance", "Enterprise", "Excelsior", "Fair Morn", "Faithful Friend",
    "Fidelity", "Fortitude", "Fortuna", "Fram", "Gemini", "Girl Ailsa", "Girl Carol", "Girl Jacqueline",
    "Girl Rachel", "Golden Fleece", "Good Design", "Good Fortune", "Good Intent", "Grateful", "Guiding Light",
    "Harvest Hope", "Harvester", "Heather Belle", "Heritage", "Horizon", "Imogen", "Incentive", "Isabella",
    "Jasper", "Jenna Louise", "Karen Ann", "Kestrel", "Kingfisher", "Kirsty Anne", "Lapwing", "Lindisfarne",
    "Lisa Marie", "Lodestar", "Lynn Marie", "Maid Marion", "Marigold", "Marina", "Mayflower", "Meridian",
    "Minerva", "Morning Dew", "Morning Star", "Nancy Glen", "Navigator", "New Dawn", "Northern Star", "Ocean Bounty",
    "Ocean Crest", "Ocean Harvest", "Ocean Reward", "Ocean Venture", "Onward", "Orion", "Our Hazel", "Our Lass",
    "Our Margaret", "Pathfinder", "Pelagia", "Perseverance", "Pilgrim", "Pioneer", "Polaris", "Prevail",
    "Prospect", "Prosperity", "Provider", "Quiet Waters", "Radiant Star", "Rebecca Jane", "Reliance", "Resolute",
    "Rose of Sharon", "Sapphire", "Sea Harvester", "Sea Spray", "Seagull", "Serene", "Shalimar", "Silver Chord",
    "Silver Dawn", "Silver Spray", "Sincerity", "Sophie Grace", "Spes Bona", "Spindrift", "Starlight",
    "Steadfast", "Sunbeam", "Sustain", "Tranquility", "Trident", "Trust", "Unity", "Valiant", "Vanguard",
    "Venture", "Vigilant", "Wanderer", "Westward", "Wild Rose", "Willing Boys", "Zephyr",
]
