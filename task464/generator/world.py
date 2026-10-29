"""task464 architecture 10: the world. Marchway Power Networks' Copsewell Cross 33/11 kV primary, eight 11 kV feeders.

Every name, identifier, rating and load level the simulation and the pack use is fixed here. The feeders are written
out by hand (trunk sections from the busbar outward, what is connected at each trunk node, and the project's old
sections), because the losses each project removes depend on where along its feeder every load and generator sits.
"""
import datetime as dt

SEED = 46410                      # the world's master seed (sim.py derives one stream per process from it)
UTC0 = dt.datetime(2025, 3, 31, 23, 0)   # 1 April 2025 00:00 BST, the first half-hour of the regulatory year
NHH = 17520                       # half-hours in 2025/26 (365 days)
YEAR_LABEL = "2025/26"
V_NOM_KV = 11.0
LOSSES_VALUE_GBP_MWH = 64.80      # the operator's 2027/28 losses value, filed in the programme brief
EXTRACT_DATE = dt.date(2026, 6, 12)   # the losses analysis extract (after the year closed)
BRIEF_DATE = dt.date(2026, 11, 18)
PANEL_DATE = dt.date(2026, 12, 9)

DNO = "Marchway Power Networks"
PRIMARY = "Copsewell Cross"
PRIMARY_CODE = "WXC"
NEIGHBOUR = "Feltmoor"            # the neighbouring primary whose substations share the monitoring export
LAT, LON = 52.58, -2.62

PEOPLE = {"losses_lead": "Gail Dobson", "planning_engineer": "Ricky Fisher", "data_lead": "Tracy Parkes"}

# Conductor catalogue: code -> (description, construction, resistance ohm/km per phase at 20 C, summer rating A)
CONDUCTORS = {
    "UG-PILC-0.1CU":  ("0.1 sq in copper, paper-insulated lead-covered, 3-core", "UG", 0.276, 255),
    "UG-PILC-0.15CU": ("0.15 sq in copper, paper-insulated lead-covered, 3-core", "UG", 0.184, 315),
    "UG-PILC-0.2CU":  ("0.2 sq in copper, paper-insulated lead-covered, 3-core", "UG", 0.138, 365),
    "UG-PILC-0.3CU":  ("0.3 sq in copper, paper-insulated lead-covered, 3-core", "UG", 0.0915, 445),
    "UG-XLPE-95AL":   ("95 mm2 aluminium, XLPE, triplex", "UG", 0.320, 230),
    "UG-XLPE-185AL":  ("185 mm2 aluminium, XLPE, triplex", "UG", 0.164, 335),
    "UG-XLPE-300AL":  ("300 mm2 aluminium, XLPE, triplex", "UG", 0.100, 430),
    "OH-CU-0.04":     ("0.04 sq in hard-drawn copper", "OH", 0.690, 160),
    "OH-CU-0.1":      ("0.1 sq in hard-drawn copper", "OH", 0.276, 300),
    "OH-ACSR-50":     ("50 mm2 ACSR (Rabbit)", "OH", 0.543, 185),
    "OH-ACSR-100":    ("100 mm2 ACSR (Dog)", "OH", 0.273, 300),
    "OH-AAAC-100":    ("100 mm2 AAAC (Oak)", "OH", 0.307, 290),
    "OH-AAAC-150":    ("150 mm2 AAAC (Ash)", "OH", 0.215, 375),
    "OH-AAAC-200":    ("200 mm2 AAAC (Elm)", "OH", 0.164, 445),
}
# how the network model writes the same code (the asset system's own spelling, shipped as is)
MODEL_CODE = {
    "UG-PILC-0.1CU": "PILC 0.1 CU", "UG-PILC-0.15CU": "PILC 0.15 CU", "UG-PILC-0.2CU": "PILC 0.2 CU",
    "UG-PILC-0.3CU": "PILC 0.3 CU", "UG-XLPE-95AL": "XLPE 95 AL", "UG-XLPE-185AL": "XLPE 185 AL",
    "UG-XLPE-300AL": "XLPE 300 AL", "OH-CU-0.04": "OHL 0.04 CU", "OH-CU-0.1": "OHL 0.1 CU",
    "OH-ACSR-50": "OHL ACSR RABBIT", "OH-ACSR-100": "OHL ACSR DOG", "OH-AAAC-100": "OHL AAAC OAK",
    "OH-AAAC-150": "OHL AAAC ASH", "OH-AAAC-200": "OHL AAAC ELM",
}

# Load classes: (power factor, rooftop solar share of mean kW at a clear midsummer noon, weekday profile key)
CLASSES = {
    "dom": (0.975, 0.0, "dom"), "domPV": (0.975, 0.55, "dom"), "com": (0.93, 0.0, "com"),
    "ind": (0.88, 0.0, "ind"), "agr": (0.91, 0.0, "agr"), "hosp": (0.92, 0.0, "hosp"), "cold": (0.86, 0.0, "cold"),
    "quarry": (0.84, 0.0, "quarry"), "retail": (0.94, 0.0, "com"),
}

# A trunk is a list of segments [(metres, conductor)] from the busbar outward; trunk node k is the far end of
# segment k-1 (node 0 is the busbar). attach maps a trunk node to what is connected there:
#   ("S", name, kva, class, mean_kw, spur)          a secondary substation with an LV monitor
#   ("H", name, kind, params, spur)                 an HV-connected customer metered for settlement
#   ("B", segments, attach)                         a branch: a further trunk teed off at this node
# spur is (metres, conductor) or None (the substation sits in the RMU's own switchroom)
# project lists the trunk segment indices the 2027/28 project replaces; new is the replacement conductor.
FEEDERS = [
    dict(code="F01", name="Copsewell Town", breaker="CB 3", area="town",
         trunk=[(380, "UG-XLPE-185AL"), (560, "UG-PILC-0.1CU"), (620, "UG-PILC-0.1CU"), (480, "UG-XLPE-185AL"),
                (700, "UG-XLPE-185AL"), (590, "UG-XLPE-185AL")],
         project=[1, 2], new="UG-XLPE-300AL", cost_k=412,
         attach={1: [("S", "Market Street", 1500, "dom", 340, (60, "UG-XLPE-185AL")),
                     ("S", "Castle Street", 500, "dom", 150, None)],
                 2: [("S", "Bridge Street", 1500, "com", 400, None)],
                 3: [("S", "Gaol Lane", 1000, "dom", 290, (140, "UG-XLPE-95AL")),
                     ("B", [(260, "UG-XLPE-95AL"), (310, "UG-XLPE-95AL")],
                      {1: [("S", "Mill Race", 500, "domPV", 150, None)], 2: [("S", "Tanners Row", 500, "dom", 110, None)]})],
                 4: [("S", "Cattle Market", 800, "dom", 250, (90, "UG-XLPE-185AL"))],
                 5: [("S", "Copsewell Retail Park", 1500, "retail", 400, None)],
                 6: [("S", "Abbey Close", 800, "domPV", 230, (120, "UG-XLPE-95AL"))]}),
    dict(code="F02", name="Ashlade", breaker="CB 4", area="industrial",
         trunk=[(820, "UG-XLPE-185AL"), (1080, "UG-PILC-0.15CU"), (942, "UG-PILC-0.15CU"), (690, "UG-XLPE-185AL")],
         project=[1, 2], new="UG-XLPE-300AL", cost_k=538,
         attach={1: [("S", "Ashlade Works No 1", 1000, "ind", 420, (110, "UG-XLPE-185AL")),
                     ("S", "Ashlade Works No 2", 1000, "ind", 380, (110, "UG-XLPE-185AL"))],
                 2: [("S", "Ashlade Road", 1500, "com", 360, None)],
                 3: [("H", "Ashlade Community Hospital", "chp", dict(site_kw=760, chp_kw=1200), (180, "UG-XLPE-185AL"))],
                 4: [("S", "Ashlade Green", 1000, "dom", 280, (70, "UG-XLPE-95AL"))]}),
    dict(code="F03", name="Oxenford Lane", breaker="CB 6", area="rural",
         trunk=[(1210, "OH-ACSR-100"), (1580, "OH-ACSR-100"), (2230, "OH-CU-0.04"), (1910, "OH-CU-0.04"),
                (1900, "OH-ACSR-100")],
         project=[2, 3], new="OH-AAAC-150", cost_k=356,
         attach={1: [("S", "Oxenford", 1500, "dom", 410, (40, "UG-XLPE-185AL")),
                     ("S", "Oxenford Church", 1500, "dom", 380, None)],
                 2: [("S", "Oxenford Lane Works", 1500, "com", 390, None),
                     ("S", "Lambs Close", 500, "domPV", 140, (420, "OH-AAAC-100")),
                     ("S", "Oxenford Mill", 800, "com", 160, None)],
                 3: [("S", "Hanley Farm", 315, "agr", 120, None)],
                 4: [("S", "Coldhurst", 200, "agr", 85, (650, "OH-ACSR-50"))],
                 5: [("S", "Pikes End", 315, "dom", 70, None)]}),
    dict(code="F04", name="Kestle", breaker="CB 7", area="mixed",
         trunk=[(880, "UG-XLPE-185AL"), (1020, "UG-XLPE-185AL"), (1480, "OH-CU-0.1"), (1350, "OH-CU-0.1"),
                (1121, "OH-CU-0.1")],
         project=[2, 3, 4], new="OH-AAAC-200", cost_k=377,
         attach={1: [("S", "Kestle Park No 1", 1000, "com", 300, None),
                     ("S", "Kestle Park No 5", 1000, "com", 245, (90, "UG-XLPE-185AL")),
                     ("S", "Kestle Park No 3", 1000, "com", 290, (210, "UG-XLPE-185AL")),
                     ("S", "Kestle Park No 6", 1000, "com", 265, (120, "UG-XLPE-185AL")),
                     ("H", "Kestle Park Cold Store", "demand", dict(cls="cold", mean_kw=980), (160, "UG-XLPE-185AL"))],
                 2: [("S", "Kestle Park No 2", 1500, "ind", 540, None),
                     ("S", "Kestle Park No 4", 1500, "ind", 520, (140, "UG-XLPE-185AL"))],
                 3: [("S", "Kestle Village", 500, "dom", 140, (300, "OH-AAAC-100"))],
                 4: [("S", "Brockhurst Farm", 200, "agr", 80, None)],
                 5: [("H", "Hob Moor Solar Park", "solar", dict(cap_kw=5500, anm_floor_kw=250), (240, "UG-XLPE-185AL")),
                     ("S", "Hob Moor", 200, "dom", 55, None)]}),
    dict(code="F05", name="Pennick Hill", breaker="CB 9", area="mixed",
         trunk=[(610, "UG-XLPE-185AL"), (790, "UG-XLPE-185AL"), (2300, "UG-PILC-0.1CU"), (1800, "UG-PILC-0.1CU")],
         project=[2, 3], new="UG-XLPE-300AL", cost_k=604,
         attach={1: [("S", "Pennick", 1500, "dom", 420, None),
                     ("S", "Pennick Square", 1500, "dom", 400, (80, "UG-XLPE-95AL")),
                     ("S", "Pennick Fields", 1500, "dom", 380, (150, "UG-XLPE-95AL"))],
                 2: [("S", "Pennick Hill Road", 1500, "com", 400, (130, "UG-XLPE-185AL")),
                     ("S", "Pennick Hill School", 1000, "com", 300, None)],
                 3: [("S", "Pennick Business Park No 1", 1500, "com", 165, None),
                     ("S", "Pennick Business Park No 4", 1500, "com", 90, (60, "UG-XLPE-185AL"))],
                 4: [("S", "Pennick Business Park No 2", 1500, "ind", 150, (90, "UG-XLPE-185AL")),
                     ("S", "Pennick Business Park No 3", 1500, "com", 120, None),
                     ("S", "Pennick Business Park No 5", 1000, "com", 60, (110, "UG-XLPE-185AL"))]}),
    dict(code="F06", name="Redburn", breaker="CB 10", area="residential",
         trunk=[(700, "UG-XLPE-185AL"), (820, "UG-XLPE-185AL"), (2400, "UG-PILC-0.1CU"), (1650, "UG-PILC-0.1CU")],
         project=[2, 3], new="UG-XLPE-300AL", cost_k=471,
         attach={1: [("S", "Redburn Road", 1500, "dom", 380, (60, "UG-XLPE-95AL")),
                     ("S", "Redburn Close", 1500, "dom", 360, None)],
                 2: [("S", "Redburn Green", 1500, "domPV", 400, None),
                     ("S", "Ferrers Way", 1500, "domPV", 380, (110, "UG-XLPE-95AL")),
                     ("S", "Redburn Park", 1000, "dom", 300, (90, "UG-XLPE-95AL"))],
                 3: [("S", "Sandpits", 1000, "dom", 320, (200, "UG-XLPE-95AL"))],
                 4: [("S", "Low Street", 1000, "com", 255, None),
                     ("S", "Redburn Meadows", 800, "domPV", 210, (240, "UG-XLPE-185AL"))]}),
    dict(code="F07", name="Stowmere", breaker="CB 12", area="rural",
         trunk=[(1490, "OH-ACSR-100"), (2010, "OH-ACSR-50"), (2420, "OH-ACSR-50"), (1770, "OH-ACSR-100")],
         project=[1, 2], new="OH-AAAC-150", cost_k=318,
         attach={1: [("S", "Stowmere", 1000, "dom", 290, None)],
                 2: [("H", "Crane Hill wind turbine", "wind", dict(cap_kw=800, anm_floor_kw=150), (520, "OH-AAAC-100")),
                     ("S", "Crane Hill Farm", 800, "agr", 230, None)],
                 3: [("S", "Mere End", 500, "dom", 150, (310, "OH-ACSR-50"))],
                 4: [("H", "Stowmere Quarry", "demand", dict(cls="quarry", mean_kw=130), (180, "OH-AAAC-100"))]}),
    dict(code="F08", name="Ingle Road", breaker="CB 13", area="residential",
         trunk=[(590, "UG-XLPE-185AL"), (880, "UG-PILC-0.2CU"), (1010, "UG-PILC-0.2CU"), (790, "UG-XLPE-185AL")],
         project=[1, 2], new="UG-XLPE-300AL", cost_k=446,
         attach={1: [("S", "Ingle Road", 1000, "dom", 300, None),
                     ("S", "Ingle Lane", 1000, "dom", 290, (70, "UG-XLPE-95AL"))],
                 2: [("S", "Ingle Court", 1500, "com", 400, (110, "UG-XLPE-185AL"))],
                 3: [("S", "Thornfield", 1500, "domPV", 370, None)],
                 4: [("S", "Ingle Park", 800, "dom", 255, (150, "UG-XLPE-95AL"))]}),
]

# Feltmoor primary: substations sharing the monitoring export and HV customers sharing the settlement extract.
NEIGHBOUR_SUBS = [("Feltmoor Square", 1500, "com", 390), ("Feltmoor Mill", 800, "dom", 230), ("Chapel Fields", 800, "domPV", 210),
                  ("Furnace Lane", 1500, "ind", 520), ("Feltmoor Station", 500, "com", 120), ("Westbrook", 500, "dom", 150),
                  ("Holly Bank", 1000, "dom", 260), ("Feltmoor Leisure Centre", 1000, "com", 300), ("Pool Head", 200, "agr", 70),
                  ("Barnfield", 800, "domPV", 240), ("Quarry Bank", 500, "dom", 130), ("Hollins End", 200, "agr", 60),
                  ("Feltmoor Business Centre", 1500, "com", 350), ("Saltbrook", 800, "dom", 160)]
NEIGHBOUR_HV = [("Feltmoor Sewage Treatment Works", "demand", dict(cls="ind", mean_kw=410)),
                ("Saltbrook Garden Centre", "demand", dict(cls="com", mean_kw=95))]

# The LV monitors replaced part-way through the year: (substation, replacement date, days with no record)
MONITOR_SWAPS = {"Ingle Road": (dt.date(2025, 7, 14), 4), "Feltmoor Mill": (dt.date(2025, 9, 2), 3)}
# Substations whose first-generation monitors recorded kVA and power factor until the vendor change
VENDOR_A_UNTIL = dt.date(2025, 11, 4)
VENDOR_A_SUBS = ["Market Street", "Bridge Street", "Ashlade Works No 1", "Oxenford", "Kestle Park No 1", "Pennick",
                 "Redburn Road", "Stowmere", "Ingle Court", "Feltmoor Square", "Furnace Lane", "Holly Bank"]
REDBURN_MEADOWS_ENERGISED = dt.date(2025, 10, 6)   # the new estate's substation came on load during the year

# normally-open interconnectors between feeder ends: (feeder, other feeder, metres, conductor)
NOP_LINKS = [("F01", "F08", 420, "UG-XLPE-185AL"), ("F05", "F06", 560, "UG-XLPE-185AL"), ("F02", "F05", 690, "UG-XLPE-185AL"),
             ("F03", "F07", 1480, "OH-ACSR-50")]

# the interruption record's stream tag (rel.py)
REL_SALT = ":13"
