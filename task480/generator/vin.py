"""Vehicle identification numbers as the federal standard writes them (49 CFR 565): the world manufacturer
identifier, the descriptor section, the check digit, the model-year character, the plant and the serial, plus the
make and model table the fleet is drawn from."""
import numpy as np

TRANS = {**{str(d): d for d in range(10)}, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "J": 1,
         "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9, "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9}
WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
ALLOWED = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
YEAR_CODE = {}
_codes = "ABCDEFGHJKLMNPRSTVWXY123456789"
for i, y in enumerate(range(1980, 2010)):
    YEAR_CODE[y] = _codes[i]
for i, y in enumerate(range(2010, 2040)):
    YEAR_CODE[y] = _codes[i]

# make (DMV abbreviation), model as the DMV titles it, body code, class, world manufacturer identifiers, model years
# sold, weight, fuels it was sold with (G gasoline, F flex-fuel, H gasoline-electric hybrid, D diesel, E electric)
MODELS = [
    ("FORD", "TAURUS", "4D", "PC", ["1FA", "1FA"], (1990, 2019), 3.0, "GF"),
    ("FORD", "FOCUS", "4D", "PC", ["1FA", "1FA"], (2000, 2018), 3.5, "G"),
    ("FORD", "FUSION", "4D", "PC", ["3FA", "3FA"], (2006, 2020), 3.0, "GH"),
    ("FORD", "MUSTANG", "2D", "PC", ["1ZV", "1FA"], (1990, 2027), 1.2, "G"),
    ("FORD", "ESCAPE", "UT", "LT", ["1FM", "1FM"], (2001, 2027), 3.4, "GH"),
    ("FORD", "EXPLORER", "UT", "LT", ["1FM", "1FM"], (1991, 2027), 3.2, "GF"),
    ("FORD", "F150", "PK", "LT", ["1FT", "1FT"], (1990, 2027), 6.0, "GF"),
    ("CHEV", "MALIBU", "4D", "PC", ["1G1", "1G1"], (1997, 2024), 3.4, "G"),
    ("CHEV", "IMPALA", "4D", "PC", ["2G1", "2G1"], (2000, 2020), 2.6, "GF"),
    ("CHEV", "CRUZE", "4D", "PC", ["1G1", "1G1"], (2011, 2019), 2.2, "G"),
    ("CHEV", "EQUINOX", "UT", "LT", ["2GN", "2CN"], (2005, 2027), 3.4, "G"),
    ("CHEV", "TAHOE", "UT", "LT", ["1GN", "1GN"], (1995, 2027), 1.8, "GF"),
    ("CHEV", "SILVERADO 1500", "PK", "LT", ["1GC", "2GC"], (1999, 2027), 5.2, "GF"),
    ("CHEV", "BOLT EV", "HB", "PC", ["1G1", "1G1"], (2017, 2023), 0.5, "E"),
    ("GMC", "SIERRA 1500", "PK", "LT", ["1GT", "2GT"], (1999, 2027), 2.2, "GF"),
    ("TOYT", "CAMRY", "4D", "PC", ["4T1", "JTN"], (1990, 2027), 5.2, "GH"),
    ("TOYT", "COROLLA", "4D", "PC", ["1NX", "2T1"], (1990, 2027), 4.8, "G"),
    ("TOYT", "PRIUS", "HB", "PC", ["JTD", "JTD"], (2001, 2022), 1.4, "H"),
    ("TOYT", "RAV4", "UT", "LT", ["JTM", "2T3"], (1996, 2027), 4.0, "GH"),
    ("TOYT", "TACOMA", "PK", "LT", ["5TE", "3TM"], (1995, 2027), 2.6, "G"),
    ("TOYT", "SIENNA", "MV", "LT", ["4T3", "5TD"], (1998, 2027), 1.6, "G"),
    ("HOND", "ACCORD", "4D", "PC", ["1HG", "1HG"], (1990, 2027), 4.6, "G"),
    ("HOND", "CIVIC", "4D", "PC", ["2HG", "19X"], (1990, 2027), 4.6, "GH"),
    ("HOND", "CR-V", "UT", "LT", ["JHL", "5J6"], (1997, 2027), 3.8, "G"),
    ("HOND", "ODYSSEY", "MV", "LT", ["5FN", "5FN"], (1996, 2027), 1.6, "G"),
    ("NISS", "ALTIMA", "4D", "PC", ["1N4", "1N4"], (1993, 2027), 3.6, "G"),
    ("NISS", "SENTRA", "4D", "PC", ["3N1", "3N1"], (1990, 2027), 2.6, "G"),
    ("NISS", "ROGUE", "UT", "LT", ["JN8", "5N1"], (2008, 2027), 2.6, "G"),
    ("NISS", "LEAF", "HB", "PC", ["1N4", "1N4"], (2011, 2025), 0.5, "E"),
    ("DODG", "CARAVAN", "MV", "LT", ["2B4", "2D4"], (1990, 2020), 2.4, "GF"),
    ("DODG", "RAM 1500", "PK", "LT", ["1D7", "1C6"], (1994, 2027), 3.4, "GFD"),
    ("JEEP", "GRAND CHEROKEE", "UT", "LT", ["1J4", "1C4"], (1993, 2027), 2.6, "GD"),
    ("JEEP", "WRANGLER", "UT", "LT", ["1J4", "1C4"], (1997, 2027), 1.8, "G"),
    ("HYUN", "ELANTRA", "4D", "PC", ["KMH", "5NP"], (1996, 2027), 2.8, "G"),
    ("HYUN", "SANTA FE", "UT", "LT", ["5NM", "5NM"], (2001, 2027), 1.8, "G"),
    ("KIA", "SORENTO", "UT", "LT", ["5XY", "KND"], (2003, 2027), 1.6, "G"),
    ("KIA", "OPTIMA", "4D", "PC", ["KNA", "5XX"], (2001, 2020), 1.6, "GH"),
    ("SUBA", "OUTBACK", "SW", "PC", ["4S4", "4S4"], (1995, 2027), 2.2, "G"),
    ("SUBA", "FORESTER", "UT", "LT", ["JF2", "JF2"], (1998, 2027), 1.8, "G"),
    ("CHRY", "TOWN & COUNTRY", "MV", "LT", ["2A4", "2C4"], (1996, 2016), 1.2, "GF"),
    ("VOLK", "JETTA", "4D", "PC", ["3VW", "3VW"], (1996, 2027), 2.0, "GD"),
    ("MAZD", "MAZDA3", "4D", "PC", ["JM1", "3MZ"], (2004, 2027), 1.6, "G"),
    ("BMW", "3 SERIES", "4D", "PC", ["WBA", "WBA"], (1990, 2027), 1.0, "G"),
    ("TSLA", "MODEL 3", "4D", "PC", ["5YJ", "5YJ"], (2018, 2027), 0.9, "E"),
    ("TSLA", "MODEL Y", "UT", "LT", ["7SA", "5YJ"], (2020, 2027), 0.7, "E"),
]


def check_digit(v17):
    s = sum(TRANS[c] * w for c, w in zip(v17, WEIGHTS))
    r = s % 11
    return "X" if r == 10 else str(r)


def make_vin(rng, wmi, my, serial):
    vds = "".join(rng.choice(list(ALLOWED[:23]), 4)) + str(int(rng.integers(0, 10)))
    plant = rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ0123456789"))
    body = wmi + vds + "0" + YEAR_CODE[my] + plant + "%06d" % serial
    return body[:8] + check_digit(body) + body[9:]


def valid(v):
    return len(v) == 17 and all(c in ALLOWED for c in v) and check_digit(v) == v[8]


CONFUSE = {"0": "O", "1": "I", "5": "S", "8": "B", "2": "Z", "B": "8", "S": "5", "G": "6", "6": "G", "D": "0"}


def mistype(rng, v):
    """One slip at a keyboard: a look-alike character typed for another (an O for a zero, an I for a one)."""
    v = list(v)
    cand = [i for i, c in enumerate(v) if c in CONFUSE and i != 8]
    i = int(rng.choice(cand)) if cand else 11
    v[i] = CONFUSE.get(v[i], "0" if v[i] != "0" else "1")
    return "".join(v)


def plate(rng):
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    return "".join(rng.choice(list(letters), 3)) + "%04d" % int(rng.integers(0, 10000))


def model_table():
    w = np.array([m[6] for m in MODELS], float)
    return MODELS, w / w.sum()
