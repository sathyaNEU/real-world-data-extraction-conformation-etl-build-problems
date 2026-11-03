"""Arnvale Water: the fixed world every other script reads."""
import datetime as dt

SEED = 194
UTC0 = dt.datetime(2026, 8, 1, 0, 0)          # first historian stamp, UTC
DAYS = 94                                     # to 2026-11-02 23:45 UTC
BST_END = dt.datetime(2026, 10, 25, 1, 0)     # UTC instant British Summer Time ends
EXPORT = dt.datetime(2026, 11, 3, 6, 12, 0)   # in-fiction export time (local = UTC in November)

BASE_NIGHTS = (dt.date(2026, 9, 7), dt.date(2026, 10, 4))
COMP_NIGHTS = (dt.date(2026, 10, 12), dt.date(2026, 11, 1))

HH_NU = 1.7      # l per household property per hour (LP04 4.2)
NHH_NU = 6.0     # l per unlogged non-household property per hour (LP04 4.3)
N1 = 1.15        # leakage-pressure exponent (LP04 5.1)

# code, name, inlet tags [(tag, unit)], household props, small non-household props, mains km,
# AZNP logger, night pressure (m), baseline own leakage at night (m3/h)
AREAS = [
    ("D4117", "Kestle Hill",        [("KH01_FT", "m3/h")],                    2312, 41, 21.4, "PL-2208", 47.2, 4.36),
    ("D4123", "Moorend Low",        [("MLW_INLET_FT1", "l/s")],              1738, 22, 15.9, "PL-2211", 41.8, 3.12),
    ("D4130", "Barrowfold",        [("BF-FLOW-01", "m3/h")],                3105, 77, 28.3, "PL-1984", 44.1, 6.84),
    ("D4136", "Hennick",            [("HEN_FM1", "l/s"), ("HEN_FM2", "l/s")], 4087, 96, 36.0, "PL-2290", 39.5, 7.91),
    ("D4142", "Upper Sowden",       [("US01_FT", "m3/h")],                    1194, 18, 12.7, "PL-2017", 52.6, 2.48),
    ("D4149", "Calvert Rise",        [("CR_INLET_FT", "m3/h")],                3471, 63, 33.8, "PL-2125", 38.0, 18.40),
    ("D4155", "Thrushgate",         [("THR01_FT", "l/s")],                    2668, 52, 24.1, "PL-2240", 45.9, 5.07),
    ("D4161", "Lidden Common",        [("LC-FT-1", "m3/h")],                    986, 9, 10.3, "PL-1901", 49.3, 1.94),
    ("D4168", "Netherby Road",      [("NR01_FT", "m3/h")],                    2049, 118, 17.6, "PL-2063", 43.0, 4.71),
    ("D4174", "Oakshaw",            [("OAK_FM1", "l/s")],                     1563, 27, 19.2, "PL-2174", 50.8, 3.66),
    ("D4180", "Stanecroft",          [("SG-INLET", "m3/h"), ("SG-INLET-2", "m3/h")], 3760, 141, 31.5, "PL-2009", 41.2, 8.37),
    ("D4187", "Pellow Bridge",      [("PB01_FT", "m3/h")],                    1872, 88, 18.8, "PL-2236", 46.4, 3.89),
    ("D4193", "Crake Bank",             [("CRK_FM1", "l/s")],                     1407, 31, 16.4, "PL-2151", 44.7, 3.21),
    ("D4205", "Ashworth Fold",      [("AF01_FT", "m3/h")],                    2216, 46, 22.9, "PL-1977", 42.5, 5.58),
    ("D4211", "Whinlow Moor",           [("WHM-FT01", "m3/h")],                   2934, 59, 27.0, "PL-2102", 48.0, 6.12),
    ("D3341", "Gorsey Bank",        [("GB01_FT", "l/s")],                     1689, 37, 15.1, "PL-2219", 45.3, 3.47),
    ("D4224", "Ravensclough",       [("RVC_FM1", "m3/h")],                    1251, 14, 13.8, "PL-2088", 53.1, 2.29),
    ("D4230", "Tollbar",            [("TB-FT-01", "m3/h")],                   2480, 104, 20.5, "PL-2193", 40.6, 5.36),
]
CODE = {a[1]: a[0] for a in AREAS}
NAME = {a[0]: a[1] for a in AREAS}
OLD_CODE = {"D3341": "D3305"}   # Gorsey Bank renumbered at the April 2025 boundary change
# large users whose site moved to a neighbouring area at the April 2025 boundary change; the billing account
# still carries the area it was opened in
ACCOUNT_AREA_2019 = {"Hollin Dairies Ltd": "D4136", "Netherby Road Health Centre": "D4180", "OAKSHAW GOLF CLUB": "D4187",
                     "Crake Bank Garden Centre": "D4211", "Upper Sowden Farm Shop": "D4149",
                     "Lidden Common Primary School": "D4123"}

# valve-sharing neighbours (GIS boundary valves, all status CLOSED in GIS)
BOUNDARY = [
    ("BV-0412", "D4117", "D4123"), ("BV-0418", "D4117", "D4130"), ("BV-0433", "D4123", "D4161"),
    ("BV-0447", "D4130", "D4136"), ("BV-0451", "D4136", "D4142"), ("BV-0466", "D4142", "D4149"),
    ("BV-0470", "D4149", "D4155"), ("BV-0485", "D4155", "D4168"), ("BV-0489", "D4161", "D4174"),
    ("BV-0502", "D4168", "D4180"), ("BV-0517", "D4174", "D4187"), ("BV-0523", "D4180", "D4193"),
    ("BV-0538", "D4187", "D4205"), ("BV-0541", "D4193", "D4211"), ("BV-0556", "D4205", "D3341"),
    ("BV-0560", "D4211", "D4224"), ("BV-0575", "D3341", "D4230"), ("BV-0581", "D4224", "D4230"),
    ("BV-0594", "D4155", "D4136"), ("BV-0608", "D4117", "D4161"),
]

# fractional start of a meter's register, as read off the meter at its last exchange
REG_TRIM = {"Ashworth Fold Medical Practice": 0.06}

# the events (UTC instants)
VALVE_OPEN = dt.datetime(2026, 10, 6, 9, 40)      # BV-0412 opened for the Moorend Low valve job, left open
TRANSFER_SHARE = 0.495                            # share of Moorend Low's draw carried through Kestle Hill
BURST = ("D4155", dt.datetime(2026, 10, 11, 20, 50), 2.21)   # Thrushgate, m3/h at baseline night pressure
NEW_USER = ("D4187", dt.datetime(2026, 10, 1, 5, 0), 6.27)   # Pellow Bridge depot, m3/h at night
PRV = ("D4149", dt.datetime(2026, 9, 29, 13, 0), 38.0, 47.0) # Calvert Rise PRV set point raised

# each other area's own leakage change between the periods, litres a second (repairs and new small leaks)
WANDER_LS = {"D4205": 0.3, "D4130": 0.2, "D4161": 0.1, "D4142": 0.0, "D3341": 0.1, "D4168": 0.0, "D4180": 0.0,
             "D4174": -0.1, "D4193": 0.0, "D4211": -0.1, "D4230": -0.1, "D4136": -0.2, "D4224": -0.2}
