"""task127 generator: fixed parameters of the fiction and the design.

Every value here is a choice the fiction made (a parameter), never a figure the analysis derived.
The figures the analysis derives are computed from the written files by ladder.py and checks.py.
"""
from datetime import date

import numpy as np

SEED = 20271217
AS_OF = date(2026, 12, 11)          # the fund's working date for the trustees' paper
PACK_DATE = date(2026, 12, 11)      # export date of the bundle
MEETING = date(2026, 12, 17)

COOPS = ["NS", "VA", "LA", "UP", "RB", "PW"]
COOP_NAME = {"NS": "North Shore", "VA": "Valley", "LA": "Lakes", "UP": "Uplands", "RB": "Riverbend",
             "PW": "Pinewood"}
COOP_LONG = {"NS": "North Shore Electric Cooperative", "VA": "Valley Rural Electric Cooperative",
             "LA": "Lakes Country Electric Cooperative", "UP": "Uplands Electric Cooperative",
             "RB": "Riverbend Electric Cooperative", "PW": "Pinewood Electric Cooperative"}
CREW = {"NS": "NS-MTR", "VA": "VA-MTR", "LA": "LA-MTR", "UP": "UP-MTR", "RB": "RB-MTR", "PW": "PW-MTR"}
FOUR_DAY = {"LA", "UP"}             # crews on four ten-hour days, Monday to Thursday

# people, drawn with guard.py names --geo "United States, Minnesota" --seed 127 (en_US pool)
PEOPLE = {
    "director": "Stephanie O'Connor",     # programme director, the requester
    "outreach": "Sara Duncan",            # outreach director
    "chair": "Elizabeth Villa",           # chair of the trustees
    "lakes_ops": "Kyle Bean",             # field operations superintendent, Lakes
    "installers": "Larry Woodward",       # chair of the participating installers' group
    "grid": "Brian Robbins",              # grid liaison, compiles the hosting filings
    "finance": "Sandra Rodriguez",        # finance director
    "survey": "Christopher Vargas",       # survey office lead
}

FUND = "Minnesota Clean Heat Fund"

# ------------------------------------------------------------------ heating systems and rates
SYS = ["D", "E", "H"]                # ducted propane furnace, electric resistance, hydronic propane boiler
SYS_LABEL = {"D": "propane furnace (ducted)", "E": "electric resistance", "H": "propane boiler (hydronic)"}
# a unit block of qualifying households and the pilot installs it produced (the system rates)
UNIT = {"D": (38, 3), "E": (32, 1), "H": (95, 1)}

# pilot neighbourhoods: unit blocks per system (D, E, H), split across the two eligible income bands
PILOT_UNITS = {
    "NS": (32, 2, 2), "VA": (28, 2, 2), "LA": (8, 10, 6),
    "UP": (6, 9, 5), "RB": (29, 3, 2), "PW": (10, 18, 12),
}
PILOT_INSTALLS = {"NS": 100, "VA": 88, "LA": 40, "UP": 32, "RB": 92, "PW": 60}

NBHD = {
    "NS": ["Agate Hill", "Elm Park", "Split Creek", "Cobble Bay", "Spruce Lookout", "Ore Dock Flats",
           "Heron Narrows", "Larch Hollow"],
    "VA": ["Mill Coulee", "Birch Hollow", "Willow Coulee", "Oxbow Flats", "Cottonwood Draw", "Sumac Terrace",
           "Kettle Bottoms", "Ash Grove", "Plover Bend"],
    "LA": ["Bass Inlet", "Loon Point", "Walleye Shores", "Sunfish Bay", "Pickerel Run", "Bulrush Neck",
           "Rice Bed Point"],
    "UP": ["Granite Crest", "Kestrel Ridge", "Fieldstone Heights", "Boulder Rise", "Quarry Knob", "Upper Pasture",
           "Juneberry Hill", "Flint Prairie", "Rockpile Corners", "Windbreak Flats"],
    "RB": ["Ferry Landing", "Sauk Flats", "Mussel Shoals", "Eddy Bend", "Towpath Bottoms", "Sandbar Acres",
           "Ox Ford"],
    "PW": ["Red Pine Hollow", "Jack Pine Flats", "Needle Ridge", "Sawmill Corners", "Pitch Pine Hill",
           "Cone Valley"],
}
PILOT_NBHD = {c: NBHD[c][0] for c in COOPS}

# qualifying households (D, E, H) per non-pilot neighbourhood, and the feeder each sits on
# feeders: (feeder id, substation, filed headroom kW); a neighbourhood sits on exactly one feeder
QUAL = {
    "NS": {"Elm Park": (700, 160, 300), "Split Creek": (2341, 300, 420), "Cobble Bay": (1650, 260, 380),
           "Spruce Lookout": (760, 150, 260), "Ore Dock Flats": (300, 140, 200),
           "Heron Narrows": (520, 120, 170), "Larch Hollow": (249, 110, 150)},
    "VA": {"Birch Hollow": (700, 160, 300), "Willow Coulee": (2001, 650, 800), "Oxbow Flats": (1170, 300, 480),
           "Cottonwood Draw": (180, 200, 300), "Sumac Terrace": (90, 180, 380), "Kettle Bottoms": (80, 150, 330),
           "Ash Grove": (60, 140, 230), "Plover Bend": (105, 80, 114)},
    "LA": {"Loon Point": (700, 160, 300), "Walleye Shores": (1101, 230, 380), "Sunfish Bay": (1040, 200, 360),
           "Pickerel Run": (900, 170, 300), "Bulrush Neck": (640, 140, 189), "Rice Bed Point": (550, 100, 140)},
    "UP": {"Kestrel Ridge": (590, 520, 700), "Fieldstone Heights": (610, 600, 800), "Boulder Rise": (420, 450, 640),
           "Quarry Knob": (360, 420, 600), "Upper Pasture": (380, 380, 520), "Juneberry Hill": (300, 360, 470),
           "Flint Prairie": (300, 300, 420), "Rockpile Corners": (243, 260, 300),
           "Windbreak Flats": (110, 210, 237)},
    "RB": {"Sauk Flats": (700, 160, 300), "Mussel Shoals": (490, 200, 330), "Eddy Bend": (760, 180, 300),
           "Towpath Bottoms": (620, 150, 240), "Sandbar Acres": (560, 120, 216), "Ox Ford": (744, 90, 140)},
    "PW": {"Jack Pine Flats": (771, 420, 600), "Needle Ridge": (560, 400, 560), "Sawmill Corners": (300, 300, 420),
           "Pitch Pine Hill": (180, 210, 320), "Cone Valley": (89, 170, 300)},
}

FEEDERS = {
    # co-op: list of (feeder, substation, headroom kW, [neighbourhoods])
    "NS": [("NS-411", "Silver Cliff Rd", 175, ["Split Creek", "Cobble Bay"]),
           ("NS-414", "Silver Cliff Rd", 125, ["Elm Park", "Spruce Lookout"]),
           ("NS-420", "Taconite Jct", 2890, ["Ore Dock Flats", "Heron Narrows", "Larch Hollow"]),
           ("NS-427", "Taconite Jct", 2465, ["Agate Hill"])],
    "VA": [("VA-205", "Coulee", 75, ["Willow Coulee"]),
           ("VA-206", "Coulee", 125, ["Oxbow Flats"]),
           ("VA-211", "Mill Creek", 1815, ["Birch Hollow", "Cottonwood Draw"]),
           ("VA-214", "Mill Creek", 1600, ["Sumac Terrace", "Kettle Bottoms", "Ash Grove", "Plover Bend"]),
           ("VA-218", "Mill Creek", 2140, ["Mill Coulee"])],
    "LA": [("LA-302", "Pelican", 390, ["Walleye Shores"]),
           ("LA-305", "Pelican", 1475, ["Loon Point", "Sunfish Bay"]),
           ("LA-309", "Rush Lake", 1630, ["Pickerel Run", "Bulrush Neck", "Rice Bed Point"]),
           ("LA-311", "Rush Lake", 1335, ["Bass Inlet"])],
    "UP": [("UP-101", "Quarry", 180, ["Kestrel Ridge", "Boulder Rise"]),
           ("UP-104", "Quarry", 200, ["Fieldstone Heights"]),
           ("UP-108", "Highland", 1300, ["Quarry Knob", "Upper Pasture", "Juneberry Hill"]),
           ("UP-112", "Highland", 1210, ["Flint Prairie", "Rockpile Corners", "Windbreak Flats"]),
           ("UP-115", "Highland", 1125, ["Granite Crest"])],
    "RB": [("RB-501", "Ferry", 200, ["Mussel Shoals"]),
           ("RB-503", "Ferry", 1650, ["Sauk Flats", "Eddy Bend"]),
           ("RB-507", "Eddy", 1720, ["Towpath Bottoms", "Sandbar Acres", "Ox Ford"]),
           ("RB-510", "Eddy", 1520, ["Ferry Landing"])],
    "PW": [("PW-601", "Sawmill", 110, ["Jack Pine Flats", "Needle Ridge"]),
           ("PW-603", "Sawmill", 90, ["Sawmill Corners"]),
           ("PW-606", "Cone", 1385, ["Pitch Pine Hill", "Cone Valley"]),
           ("PW-609", "Cone", 1015, ["Red Pine Hollow"])],
}
KW_PER_HP = 5

# non-qualifying households, as multiples of a neighbourhood's qualifying count, per co-op profile
# keys: other fuel owner detached in band (gas, oil, wood, heat pump), DEH out of band, mobile homes,
# renters detached, renters attached, owners attached
PROFILE = {
    # each household group as a multiple of the neighbourhood's qualifying count: other = owner, detached,
    # in band, another fuel; outband = owner, detached, propane or electric, income outside the band;
    # mobile = owner, mobile home, in band, propane or electric; rent_det = renter, detached, in band, propane or
    # electric; multi = renter, attached or multi-unit, outside the band, utility gas
    "NS": dict(other=0.45, outband=0.30, mobile=0.22, rent_det=0.22, multi=0.10),
    "VA": dict(other=0.30, outband=0.72, mobile=0.80, rent_det=0.70, multi=0.04),
    "LA": dict(other=0.40, outband=0.30, mobile=0.25, rent_det=0.22, multi=0.08),
    "UP": dict(other=0.10, outband=0.06, mobile=0.05, rent_det=0.05, multi=0.10),
    "RB": dict(other=0.40, outband=0.32, mobile=0.26, rent_det=0.24, multi=0.10),
    "PW": dict(other=0.25, outband=0.30, mobile=0.28, rent_det=0.22, multi=0.12),
}

INCOME = ["under 35,000", "35,000 to 74,999", "75,000 to 149,999", "150,000 and over"]
IN_BAND = INCOME[1:3]
TENURE = ["owner", "renter"]
STRUCT = ["single-family detached", "mobile home", "attached or multi-unit"]
FUEL_SURVEY = {  # survey heating-system codes and the published fuel each rolls up to
    "PF": ("propane furnace (ducted)", "bottled, tank or LP gas"),
    "PB": ("propane boiler (hydronic)", "bottled, tank or LP gas"),
    "ER": ("electric resistance (baseboard, wall or cable)", "electricity"),
    "HP": ("electric heat pump", "electricity"),
    "NG": ("natural gas furnace or boiler", "utility gas"),
    "FO": ("fuel oil furnace or boiler", "fuel oil, kerosene"),
    "WD": ("wood or pellet stove", "wood"),
    "OT": ("other or none", "other fuel or none"),
}
SYS_CODE = {"D": "PF", "E": "ER", "H": "PB"}

# ------------------------------------------------------------------ crews and the field record
# per-working-day standing completions (an eight-day block summing to the level x 8) and the
# per-day ceiling pattern of the two four-day crews
STANDING_BLOCK = {"LA": [7, 9, 8, 6, 10, 8, 9, 7, 8, 9, 7, 9, 8, 6, 10, 8, 9, 7, 8, 8],
                  "UP": [6, 8, 7, 5, 8, 7, 8, 7]}
CEILING_CYCLE = {"LA": [11, 10, 11, 10], "UP": [9, 9, 9, 8]}
STANDING_LEVEL = {"NS": 11.0, "VA": 12.0, "RB": 10.4, "PW": 7.0}   # five-day crews, per working day
BATCH = {"LA": 120, "UP": 84}        # meter exchanges requested on Monday 7 July 2025

ORDER_TYPES = ["HPRM", "MXCH", "NSVC", "MTST", "DISC", "RCON", "RELO"]
STANDING_MIX = {"MXCH": 0.08, "NSVC": 0.22, "MTST": 0.12, "DISC": 0.26, "RCON": 0.27, "RELO": 0.05}

# ------------------------------------------------------------------ 2027 programme
SLOTS_TOTAL = 1800
WINDOWS = {"spring": ((3, 1), (4, 30)), "autumn": ((9, 1), (10, 15))}
SPRING_SHARE = 0.25


def rng(name):
    """A named, independent random stream, so a change in one part of the build moves nothing else."""
    h = 0
    for ch in name:
        h = (h * 131 + ord(ch)) % (2 ** 31)
    return np.random.default_rng([SEED, h])

# ------------------------------------------------------------------ shipped file names
F = dict(
    orders="field_orders_2025_2026.csv",
    survey="heat_survey_2025_households.csv",
    tables="heat_survey_2025_tables.xlsx",
    pilot="pilot_rebates_2026.xlsx",
    hosting="hosting_capacity_nov2026.xlsx",
    fmap="area_feeder_map.csv",
    rules="heat_pump_programme_rules_2027.pdf",
    terms="cooperative_participation_terms.pdf",
    invoices="installer_invoices_2026.csv",
    ledger="rebate_payments_2026.csv",
    returns="bank_returns_2026.json",
    finance="finance_procedures.pdf",
    prices="installer_price_guide_2026.pdf",
    paper="trustees_paper_17dec2026.docx",
    dims="coops_and_installers.xlsx",
    fields="field_definitions.txt",
    wx="weatherization_grants_2026.csv",
    upgrades="feeder_upgrades_2027_2028.pdf",
    about="about_these_files.txt",
)
DISTRACTORS = [F["wx"], F["upgrades"]]
DELIVERABLES = ["slot_split_board_note_2027.docx", "coop_slot_split_2027.csv", "coop_slots_2027.svg"]
