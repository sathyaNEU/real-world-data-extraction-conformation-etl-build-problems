"""World parameters for task248 (Highbank Marinas, 2026). Everything the world draws comes from SEED."""
import datetime as dt

SEED = 248_2026
YEAR = 2026
TZ = "America/Chicago"
SEASON_START = dt.date(2026, 4, 1)
SEASON_END = dt.date(2026, 10, 31)
AS_OF = dt.date(2027, 1, 12)
EXPORT_STAMP = dt.datetime(2027, 1, 11, 16, 40, 0)   # file mtimes (local), after the latest record
LIMIT_GAL = 25.0
GAL_IN3 = 231.0

GROUP = "Highbank Marinas"
LAKES = {"W": "Lake Wenning", "T": "Tolliver Lake"}
# code: (name, lake, consoleserial-prefix, open in winter (sells fuel Nov-Mar))
MARINAS = {
    "AH": ("Ashby Hollow Marina", "W", True),
    "BP": ("Brannock Point Marina", "W", False),
    "CF": ("Cedar Fork Boat Dock", "W", False),
    "DH": ("Dellwood Harbor", "W", True),
    "EB": ("Elkhorn Bend Marina", "T", False),
    "FL": ("Foxtail Landing Resort & Marina", "T", False),
    "GC": ("Gilliam Creek Marina", "T", True),
    "HS": ("Hackett Shoals Dock", "T", False),
}
# relative season sales level per marina
MARINA_LEVEL = {"AH": 1.05, "BP": 1.25, "CF": 0.85, "DH": 1.15, "EB": 0.95, "FL": 1.10, "GC": 1.0, "HS": 0.9}

# tank geometry by nominal capacity: (diameter in, length in) -> horizontal cylinder, flat-end equivalent
GEOM = {6000: (96.0, 191.5), 8000: (96.0, 255.3), 10000: (96.0, 319.1), 12000: (120.0, 245.1)}
PRODUCTS = {"REC90": "REC-90 ethanol-free", "E10": "E10 unleaded", "DSL": "Diesel"}
BETA = {"REC90": 0.00068, "E10": 0.00069, "DSL": 0.00046}   # per deg F, filed in FS-3 Table 1

# tank: (marina, product, capacity, probe offset in, chart scale eps (chart overstates by eps), meter error (frac), hoses)
TANKS = {
    "AH-1": ("AH", "REC90", 10000, 0.06, 0.0002, +0.0050, 3),
    "AH-2": ("AH", "DSL", 6000, -0.08, -0.0003, -0.0006, 2),
    "AH-3": ("AH", "E10", 8000, 0.04, 0.0004, 0.0004, 2),
    "BP-1": ("BP", "REC90", 12000, -0.05, -0.0002, 0.0007, 3),
    "BP-2": ("BP", "E10", 10000, 2.070, 0.0001, -0.0004, 2),
    "BP-3": ("BP", "DSL", 6000, 0.07, 0.0003, -0.0008, 2),
    "CF-1": ("CF", "DSL", 8000, -0.06, -0.0004, 0.0005, 2),
    "CF-2": ("CF", "REC90", 10000, 0.05, 0.0075, 0.0013, 3),
    "DH-1": ("DH", "REC90", 10000, -1.782, -0.0002, 0.0003, 2),
    "DH-2": ("DH", "REC90", 12000, 0.45, 0.0001, -0.0050, 3),
    "EB-1": ("EB", "REC90", 12000, 0.45, 0.0002, -0.0050, 3),
    "EB-2": ("EB", "E10", 10000, -0.07, 0.0002, 0.0050, 2),
    "EB-3": ("EB", "DSL", 6000, 0.05, -0.0004, 0.0006, 2),
    "FL-1": ("FL", "REC90", 12000, 2.034, -0.0001, 0.0002, 3),
    "FL-2": ("FL", "DSL", 6000, -0.04, 0.0003, -0.0007, 2),
    "GC-1": ("GC", "REC90", 10000, -0.05, -0.00739, -0.0050, 3),
    "GC-2": ("GC", "E10", 8000, 0.08, -0.0002, 0.0008, 2),
    "GC-3": ("GC", "DSL", 6000, -0.03, 0.0004, -0.0005, 2),
    "HS-1": ("HS", "REC90", 10000, 0.05, -0.0003, -0.0050, 3),
    "HS-2": ("HS", "E10", 8000, 1.852, 0.0002, 0.0005, 2),
}
PRODUCT_SHARE = {"REC90": 1.0, "E10": 0.46, "DSL": 0.42}   # relative daily draw by product

# register heights as fractions of diameter (rounded to whole inches in the register)
REORDER_FRAC = 0.21
FILL_FRAC = 0.75          # the register's normal fill height
DELIVER_TO = (0.81, 0.845)  # true product height a delivery stops at, fraction of diameter

# January ice storm: consoles whose clocks reset (marina: reset hours after the cut, days until the tech re-set)
STORM_DAY = dt.date(2026, 1, 24)
CLOCK_RESETS = {"AH": 6.0, "CF": 3.0, "EB": 8.0, "GC": 4.0, "HS": 2.0}
CONSOLE_SWAP = ("DH", dt.date(2026, 2, 17))
POS_SHADOW = (dt.date(2026, 11, 9), dt.date(2026, 11, 15))
POS_GOLIVE = dt.datetime(2026, 11, 16, 6, 0)
READ_EVERY_H = 2
