"""Araglen Regional Water Authority: the fixed world behind the 2025/26 MCPA compliance return."""
import datetime as dt

SEED = 2189
AS_OF = dt.date(2026, 11, 16)          # the authority's extract date
RETURN_DUE = dt.date(2026, 11, 30)
YEAR_FROM, YEAR_TO = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
STANDARD = 0.05                        # Schedule 2, MCPA, annual average, ug/L
NITRATE_TRIGGER = 37.5                 # mg/L NO3, the source protection report's level
NO3_FACTOR = 4.426802                  # mg/L N -> mg/L NO3

AUTHORITY = "Araglen Regional Water Authority"
REGULATOR = "National Water Quality Office"
DISTRICT = "Araglen River Basin District"
PEOPLE = {"monitoring_lead": "Emmet McQuillen",       # the authority's catchment monitoring lead
          "assessor": "Katie Enright",                # the regulator's water quality assessor
          "lab_manager": "George Twohey",     # Tirneevin
          "kgl_contact": "Shay Caldwell"}      # Kilgarron             # Tirneevin's laboratory manager

# --- laboratories and methods ---------------------------------------------------------------
LABS = {
    "TAS": {"name": "Tirneevin Analytical Services", "town": "Tirneevin",
            "inab": "T-0184", "contact": "George Twohey"},
    "KGL": {"name": "Kilgarron Laboratories", "town": "Kilgarron",
            "inab": "T-0266", "contact": "Shay Caldwell"},
}
METHODS = {
    "TAS-LC-PHX-04": {"lab": "TAS", "analytes": ["MCPA", "2,4-D", "MECOPROP", "TRICLOPYR"],
                      "technique": "SPE LC-MS/MS", "rl": 0.005, "units": "ng/l",
                      "from": dt.date(2021, 1, 1)},
    "KGL-GC-PHX-07": {"lab": "KGL", "analytes": ["MCPA", "2,4-D", "MECOPROP", "TRICLOPYR"],
                      "technique": "derivatisation GC-ECD", "rl": 0.10, "units": "ug/l",
                      "from": dt.date(2014, 4, 1)},
    "TAS-IC-ANI-02": {"lab": "TAS", "analytes": ["NO3", "CL", "SO4", "OPO4"],
                      "technique": "ion chromatography", "rl": 0.10, "units": "mg/l",
                      "from": dt.date(2019, 1, 1)},
    "KGL-CF-NUT-03": {"lab": "KGL", "analytes": ["NO3N", "NH4N", "OPO4", "TON"],
                      "technique": "continuous flow colorimetry", "rl": 0.01, "units": "mg/l",
                      "from": dt.date(2016, 1, 1)},
    "TAS-FLD-PHY-01": {"lab": "TAS", "analytes": ["COND", "PH", "DO", "TEMP", "SS", "ALK", "TURB", "COLOUR"],
                       "technique": "field probe and gravimetry", "rl": 0.00, "units": "mixed",
                       "from": dt.date(2019, 1, 1)},
}
PESTICIDES = ["MCPA", "2,4-D", "MECOPROP", "TRICLOPYR"]

DETERMINANDS = {
    "MCPA": ("MCPA", "ug/l", "4-chloro-2-methylphenoxyacetic acid"),
    "2,4-D": ("2,4-D", "ug/l", "2,4-dichlorophenoxyacetic acid"),
    "MECOPROP": ("Mecoprop", "ug/l", "mecoprop and mecoprop-P"),
    "TRICLOPYR": ("Triclopyr", "ug/l", "triclopyr"),
    "NO3": ("Nitrate as NO3", "mg/l", "nitrate expressed as nitrate ion"),
    "NO3N": ("Nitrate as N", "mg/l", "nitrate expressed as nitrogen"),
    "NH4N": ("Ammonium as N", "mg/l", "ammonium expressed as nitrogen"),
    "TON": ("Total oxidised nitrogen as N", "mg/l", "nitrate plus nitrite as nitrogen"),
    "OPO4": ("Ortho-phosphate as P", "mg/l", "molybdate reactive phosphorus as phosphorus"),
    "CL": ("Chloride", "mg/l", "chloride ion"),
    "SO4": ("Sulphate", "mg/l", "sulphate ion"),
    "COND": ("Conductivity at 25C", "uS/cm", "electrical conductivity"),
    "PH": ("pH", "pH units", "pH at 25C"),
    "DO": ("Dissolved oxygen", "mg/l", "dissolved oxygen"),
    "TEMP": ("Water temperature", "deg C", "water temperature at sampling"),
    "SS": ("Suspended solids", "mg/l", "solids retained on a 0.45 um filter"),
    "ALK": ("Total alkalinity as CaCO3", "mg/l", "total alkalinity"),
    "TURB": ("Turbidity", "NTU", "turbidity, nephelometric"),
    "COLOUR": ("Colour", "mg/l Pt-Co", "apparent colour"),
}

# --- the reporting year's months ------------------------------------------------------------
MONTHS = [(2025, m) for m in range(4, 13)] + [(2026, m) for m in range(1, 4)]
# MCPA pressure by month: the herbicide goes on rush-infested pasture from late April to early July
SEASON = {4: 0.9, 5: 4.2, 6: 5.6, 7: 2.4, 8: 0.7, 9: 0.35, 10: 0.22,
          11: 0.16, 12: 0.12, 1: 0.11, 2: 0.13, 3: 0.30}

# --- water bodies: (name, code, pre-2024 code, catchment, area km2, target annual mean, points) ---
# a point is (suffix, lab, within-body factor, place name)
A = "TAS"
B = "KGL"
WATER_BODIES = [
    ("Cloonfad",         "IE_AR_18_0410", "AR_0074", "Cloonfad", 41.8, 0.0660,
     [("0411", A, 1.00, "Cloonfad Bridge"), ("0412", A, 1.00, "Cloonfad at Ardlahan"),
      ("0413", B, 1.00, "Cloonfad at Bohernacrusha")]),
    ("Glasheen",         "IE_AR_18_0520", "AR_0081", "Glasheen", 33.1, 0.0640,
     [("0521", A, 1.00, "Glasheen at Rathvilly Weir"), ("0522", B, 1.00, "Glasheen at Coolnakilly"),
      ("0523", B, 0.95, "Glasheen at Garraunbaun")]),
    ("Kilcrohane",       "IE_AR_18_0630", "AR_0095", "Kilcrohane", 22.4, 0.0610,
     [("0631", A, 1.00, "Kilcrohane at Shanacloon"), ("0632", A, 1.00, "Kilcrohane at the Mill Race")]),
    ("Owenbeg",          "IE_AR_18_0210", "AR_0038", "Owenbeg", 57.6, 0.0600,
     [("0211", A, 0.62, "Owenbeg at Drumlosh Bridge"), ("0212", B, 1.05, "Owenbeg at Lisnagorman"),
      ("0213", B, 1.10, "Owenbeg at Clooncunny"), ("0214", B, 1.10, "Owenbeg at Carrickaneena")]),
    ("Ballynure",        "IE_AR_18_0320", "AR_0052", "Ballynure", 48.9, 0.0345,
     [("0321", A, 1.00, "Ballynure at Tooreen"), ("0322", B, 1.25, "Ballynure at Knockatober"),
      ("0323", B, 1.15, "Ballynure at Moneylea"), ("0324", B, 1.05, "Ballynure at Sheskin")]),
    ("Derryvore",        "IE_AR_18_0740", "AR_0103", "Derryvore", 29.7, 0.0368,
     [("0741", A, 1.55, "Derryvore at Aghnablaney"), ("0742", B, 1.30, "Derryvore at Keeldra"),
      ("0743", B, 1.20, "Derryvore at Tullynamoyle")]),
    ("Tirneevin Stream", "IE_AR_18_0850", "AR_0117", "Tirneevin", 18.2, 0.0364,
     [("0851", A, 1.52, "Tirneevin Stream at Boherboy"), ("0852", B, 1.35, "Tirneevin Stream at Lackaroe"),
      ("0853", B, 1.10, "Tirneevin Stream at Gortnalicka")]),
    ("Knockanure",       "IE_AR_18_0930", "AR_0126", "Knockanure", 35.5, 0.0255,
     [("0931", A, 1.00, "Knockanure at Dromadda"), ("0932", B, 1.00, "Knockanure at Tonlegee"),
      ("0933", B, 1.05, "Knockanure at Barnacullia")]),
    ("Carrowbeg",        "IE_AR_18_1040", "AR_0131", "Carrowbeg", 44.3, 0.0210,
     [("1041", A, 1.00, "Carrowbeg at Ballinaboy"), ("1042", A, 1.00, "Carrowbeg at Srahnalong"),
      ("1043", B, 1.05, "Carrowbeg at Kilmeena")]),
    ("Aghavannagh",      "IE_AR_18_1120", "AR_0144", "Aghavannagh", 26.8, 0.0190,
     [("1121", A, 1.00, "Aghavannagh at Ballinacor"), ("1122", B, 1.00, "Aghavannagh at Greenane")]),
    ("Moneycashen",      "IE_AR_18_1250", "AR_0158", "Moneycashen", 21.5, 0.0175,
     [("1251", A, 1.00, "Moneycashen at Dromavally"), ("1252", B, 1.20, "Moneycashen at Lisselton")]),
    ("Drominagh",        "IE_AR_18_1360", "AR_0162", "Drominagh", 31.9, 0.0130,
     [("1361", A, 1.00, "Drominagh at Ballyfinboy"), ("1362", B, 1.15, "Drominagh at Terryglass"),
      ("1363", B, 1.00, "Drominagh at Kilbarron")]),
    ("Lisheenaguile",    "IE_AR_18_1470", "AR_0171", "Lisheenaguile", 16.4, 0.0085,
     [("1471", A, 1.00, "Lisheenaguile at Coolbaun"), ("1472", A, 1.00, "Lisheenaguile at Ballingarry")]),
]

# --- the raw-water abstraction points (the nitrate programme, outside the compliance network) ---
ABSTRACTIONS = [
    ("ARW-A101", "Ballynure Borehole 1", "Ballynure", 34.8, "KGL"),
    ("ARW-A102", "Cloonfad Spring Chamber", "Cloonfad", 22.1, "KGL"),
    ("ARW-A103", "Gortaleen Borehole", "Knockanure", 41.6, "KGL"),
    ("ARW-A104", "Moneycashen Intake", "Moneycashen", 18.4, "KGL"),
    ("ARW-A105", "Rathvilly Borehole 2", "Glasheen", 29.3, "TAS"),
    ("ARW-A106", "Sheskin Shallow Well", "Ballynure", 37.2, "KGL"),
]

# --- operational points: nutrients and physico-chemical only, no pesticide suite ---------------
OPERATIONAL_CATCHMENTS = ["Cloonfad", "Glasheen", "Kilcrohane", "Owenbeg", "Ballynure", "Derryvore",
                          "Tirneevin", "Knockanure", "Carrowbeg", "Aghavannagh", "Moneycashen",
                          "Drominagh", "Lisheenaguile"]
NUTRIENTS = ["NH4N", "TON", "OPO4", "CL", "SO4"]
PHYSICO = ["COND", "PH", "DO", "TEMP", "SS", "ALK", "TURB", "COLOUR"]

OP_PLACES = ["Ardnageeha", "Boleybeg", "Cappanalea", "Doonbeg", "Emlagh", "Formoyle", "Gortnahoo",
             "Hollyford", "Inchicronan", "Kilnamona", "Lackandarra", "Mullaghmore", "Newtownlow",
             "Oughterard", "Poulnasherry", "Rossinver", "Shanballymore", "Templenoe", "Urlingford",
             "Woodenbridge", "Aghadoe", "Ballyteige", "Clonkeen", "Drumsna", "Esker Riada",
             "Fairymount", "Glantane", "Horseleap", "Inver", "Kiltullagh", "Lisdoonan", "Monaincha",
             "Nurney", "Ovens", "Pallasgreen", "Rahugh", "Stradbally", "Tullaroan", "Valleymount",
             "Whitegate", "Annaghmore", "Bellanaleck", "Cuilcagh", "Doochary", "Errigal", "Ballinvarrig", "Clashmore", "Dunkerron"]

# sample points renumbered in the 2024 revision of the register (honest, documented)
RENUMBERED_FROM_2024 = {"ARW-0412": "ARW-0407", "ARW-0742": "ARW-0738",
                        "ARW-0932": "ARW-0928", "ARW-1252": "ARW-1248"}

# the sampling calendar's honest departures from twelve monthly rounds
POINT_FROM = {"ARW-1043": dt.date(2025, 10, 1)}     # joined the programme at the partnership's request
POINT_TO = {"ARW-0853": dt.date(2025, 9, 30)}       # the landowner withdrew access
MISSED = [("ARW-0324", 2025, 12), ("ARW-0742", 2026, 1), ("ARW-0213", 2026, 2),
          ("ARW-1121", 2025, 11), ("ARW-0931", 2026, 2)]

QC_TYPES = ["FIELD_BLANK", "EQUIP_BLANK", "FIELD_DUP", "LAB_DUP", "MATRIX_SPIKE"]
TARGET_ROWS = 25000
