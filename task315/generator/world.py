"""task315's world: the Selkirk Valley Regional District's charging network and its 2027 site package.

An invented regional district in British Columbia's southern Interior. Three highways cross it: the Sable
Highway over the Sable Plateau (exposed above the treeline for most of the crossing), the Cedar Pass Highway
over Cedar Pass (higher and longer, forested and sheltered), and the Sorrel Valley Road north through a long
lowland valley. Fast chargers stand in the towns; the 2027 budget funds one of three site packages.

The clean truth: a car's energy on a stretch is its rated consumption times the stretch's length times an
as-driven factor that depends on the stretch, the month and the direction of travel. On every stretch but the
plateau the factor follows the valley air temperature, the climb and the descent; on the plateau the cold
months add the wind and drifting snow of the exposed crossing, which no weather station in the pack records.
"""
import datetime as dt
import math

SEED = 315

# ---------------------------------------------------------------- the network
# node: (name, elevation m, highway position notes)
NODES = {
    'HAL': ('Halston', 610),
    'COR': ('Corran', 1020),
    'SAB': ('Sable Summit', 1645),
    'FEN': ('Fenwick', 980),
    'CAL': ('Calder', 540),
    'CED': ('Cedar Pass', 1885),
    'TAM': ('Tamarack', 930),
    'BRE': ('Brennan', 700),
    'ASH': ('Ashby', 575),
    'KES': ('Kestrel Flats', 600),
    'HVB': ('Halvorsen Bridge', 640),
    'MIR': ('Mirren', 575),
    'RUT': ('Rutherford', 620),
}

# stretch id: (from, to, highway, km, climb going from->to m, descent going from->to m, exposed share)
STRETCHES = {
    'W1': ('HAL', 'COR', 'Sable Highway', 64.2, 520, 110, 0.0),
    'W2a': ('COR', 'SAB', 'Sable Highway', 66.3, 700, 75, 0.78),
    'W2b': ('SAB', 'FEN', 'Sable Highway', 63.7, 60, 725, 0.66),
    'W3': ('FEN', 'CAL', 'Sable Highway', 51.6, 40, 480, 0.0),
    'E1a': ('CAL', 'CED', 'Cedar Pass Highway', 72.0, 1390, 45, 0.0),
    'E1b': ('CED', 'TAM', 'Cedar Pass Highway', 64.0, 55, 1010, 0.0),
    'E2': ('TAM', 'BRE', 'Cedar Pass Highway', 57.7, 90, 320, 0.0),
    'N1': ('CAL', 'ASH', 'Sorrel Valley Road', 40.8, 75, 40, 0.0),
    'N2a': ('ASH', 'KES', 'Sorrel Valley Road', 61.9, 90, 65, 0.0),
    'N2b': ('KES', 'HVB', 'Sorrel Valley Road', 57.1, 110, 70, 0.0),
    'N2c': ('HVB', 'MIR', 'Sorrel Valley Road', 58.9, 55, 120, 0.0),
    'N3': ('MIR', 'RUT', 'Sorrel Valley Road', 71.8, 95, 50, 0.0),
}

# highway sequences of nodes, west to east and south to north
HIGHWAYS = {
    'Sable Highway': ['HAL', 'COR', 'SAB', 'FEN', 'CAL'],
    'Cedar Pass Highway': ['CAL', 'CED', 'TAM', 'BRE'],
    'Sorrel Valley Road': ['CAL', 'ASH', 'KES', 'HVB', 'MIR', 'RUT'],
}

# existing fast-charging sites in service at 31 October 2026 (node -> count of sites)
EXISTING_NODES = ['HAL', 'COR', 'FEN', 'CAL', 'TAM', 'BRE', 'ASH', 'MIR', 'RUT']
PACKAGES = {
    'A': {'name': 'Sorrel Valley infill', 'nodes': ['KES', 'HVB']},
    'B': {'name': 'Sable Summit', 'nodes': ['SAB']},
    'C': {'name': 'Cedar Pass', 'nodes': ['CED']},
}

# ---------------------------------------------------------------- the fleet
# model key: (display, register name, usable kWh, rated kWh/100 km, kerb mass kg, register count)
FLEET = {
    'MY': ('Tesla Model Y Long Range AWD', 'TESLA MODEL Y LR AWD', 75.0, 16.9, 1980, 1265),
    'M3L': ('Tesla Model 3 Long Range AWD', 'TESLA MODEL 3 LR AWD', 75.0, 15.4, 1830, 691),
    'M3S': ('Tesla Model 3 RWD', 'TESLA MODEL 3 RWD', 57.5, 14.3, 1760, 437),
    'IQ5': ('Hyundai IONIQ 5 Long Range AWD', 'HYUNDAI IONIQ 5 LR AWD', 74.0, 19.6, 2100, 423),
    'EV6': ('Kia EV6 Long Range AWD', 'KIA EV6 LR AWD', 74.0, 19.1, 2090, 299),
    'BLT': ('Chevrolet Bolt EUV', 'CHEVROLET BOLT EUV', 65.0, 17.6, 1670, 452),
    'LF4': ('Nissan LEAF (40 kWh)', 'NISSAN LEAF', 39.0, 17.4, 1530, 325),
    'LFP': ('Nissan LEAF PLUS', 'NISSAN LEAF PLUS', 59.0, 18.6, 1700, 175),
    'NIR': ('Kia Niro EV', 'KIA NIRO EV', 64.8, 17.8, 1740, 350),
    'KON': ('Hyundai Kona Electric', 'HYUNDAI KONA ELECTRIC', 64.0, 16.9, 1700, 292),
    'ID4': ('Volkswagen ID.4 Pro AWD', 'VOLKSWAGEN ID.4 PRO AWD', 77.0, 20.7, 2210, 278),
    'MME': ('Ford Mustang Mach-E Extended Range AWD', 'FORD MUSTANG MACH-E ER AWD', 88.0, 21.4, 2230, 221),
    'EQX': ('Chevrolet Equinox EV 2LT', 'CHEVROLET EQUINOX EV', 85.0, 18.4, 2160, 360),
    'PS2': ('Polestar 2 Long Range Dual Motor', 'POLESTAR 2 LR DUAL', 75.0, 20.4, 2110, 150),
    'F15': ('Ford F-150 Lightning Extended Range', 'FORD F-150 LIGHTNING ER', 131.0, 30.2, 2950, 180),
    'R1S': ('Rivian R1S Large Pack', 'RIVIAN R1S LARGE', 128.0, 27.8, 3110, 122),
}
# registered models under 50 kWh that appear only in the register extract (the drivers above include the LEAF)
SMALL_MODELS = {
    'MX3': ('Mazda MX-30', 'MAZDA MX-30', 29.0, 19.5, 1650, 48),
    'IQE': ('Hyundai IONIQ Electric', 'HYUNDAI IONIQ ELECTRIC', 38.3, 15.5, 1600, 96),
    'MSE': ('MINI Cooper SE', 'MINI COOPER SE HARDTOP', 28.9, 17.9, 1440, 139),
    'LF3': ('Nissan LEAF (30 kWh)', 'NISSAN LEAF S 30', 28.0, 18.6, 1520, 61),
}
FLEET_KEYS = list(FLEET)
FLEET_TOTAL = sum(v[5] for v in FLEET.values())

# the scoring rules' battery bands: each band is one reference car carrying the band's register-weighted mean
# usable battery and rated consumption from the model sheet. band: (label, lower kWh, upper kWh)
BAND_LIMITS = {
    'B2': ('50 to 69.9 kWh', 50.0, 70.0),
    'B3': ('70 to 79.9 kWh', 70.0, 80.0),
    'B4': ('80 to 99.9 kWh', 80.0, 100.0),
    'B5': ('100 kWh and over', 100.0, 999.0),
}
BAND_KEYS = list(BAND_LIMITS)
SMALL_BAND = ('under 50 kWh', 0.0, 50.0)   # registered, outside the scoring rules' long-distance fleet


def band_of(model):
    cap = FLEET[model][2]
    for b, v in BAND_LIMITS.items():
        if v[1] <= cap < v[2]:
            return b
    return None


def _ref(b):
    ks = [k for k in FLEET if band_of(k) == b]
    n = sum(FLEET[k][5] for k in ks)
    cap = sum(FLEET[k][2] * FLEET[k][5] for k in ks) / n
    rated = sum(FLEET[k][3] * FLEET[k][5] for k in ks) / n
    return n, cap, rated


BANDS = {}
for _b, (_lab, _lo, _hi) in BAND_LIMITS.items():
    _n, _cap, _rt = _ref(_b)
    BANDS[_b] = (_lab, _lo, _hi, _cap, _rt)
BAND_COUNT = {b: _ref(b)[0] for b in BAND_LIMITS}
SCORED_TOTAL = sum(BAND_COUNT.values())


def share(b):
    return BAND_COUNT[b] / SCORED_TOTAL


# scoring rules: a trip leaves its origin at 80 per cent, as it leaves every fast charger, and arrives nowhere
# below 10 per cent
START_SOC = 0.80
CHARGE_TO = 0.80
RESERVE = 0.10

# ---------------------------------------------------------------- climate
# valley daily mean air temperature by month (deg C), Calder; other valley towns offset
VALLEY_T = {1: -9.4, 2: -8.4, 3: 0.4, 4: 6.1, 5: 11.0, 6: 15.2, 7: 18.4, 8: 17.9, 9: 12.6, 10: 5.8, 11: 0.0, 12: -8.2}
LAPSE = 0.0058          # deg C per metre in the cold months' mean


def stretch_temp(sid, m):
    a, b = STRETCHES[sid][0], STRETCHES[sid][1]
    mean_elev = 0.5 * (NODES[a][1] + NODES[b][1])
    if sid in ('W2a', 'W2b'):
        mean_elev = 0.35 * (NODES[a][1] + NODES[b][1]) + 0.3 * NODES['SAB'][1]
    if sid in ('E1a', 'E1b'):
        mean_elev = 0.35 * (NODES[a][1] + NODES[b][1]) + 0.3 * NODES['CED'][1]
    return VALLEY_T[m] - LAPSE * (mean_elev - NODES['CAL'][1])


def temp_factor(t):
    """Heating and battery losses: 1.25 per cent per degree below 18 C."""
    return 1.0 + 0.0125 * max(0.0, 18.0 - t)


# the plateau's exposed crossing in the cold months: wind, drifting snow and road condition
EXPOSURE = {1: 1.62, 2: 1.60, 3: 1.40, 4: 1.08, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.05, 11: 1.38, 12: 1.63}
HIGHWAY_REAL = 1.12     # real highway consumption over the rated combined figure at mild temperature
G = 9.81
REGEN = 0.58


def climb_kwh(mass, climb, descent):
    up = mass * G * climb / 3.6e6 / 0.90
    down = mass * G * descent / 3.6e6 * REGEN
    return up - down


def oriented(sid, direction):
    """(climb, descent) for a stretch driven in direction 'F' (from->to) or 'R' (to->from)."""
    s = STRETCHES[sid]
    return (s[4], s[5]) if direction == 'F' else (s[5], s[4])


MASS_PER_RATED = 116.0   # kg of car per kWh/100 km of rated consumption, so the climb scales with consumption


def true_factor(sid, m, direction):
    """The as-driven factor on a stretch: a car's energy over its rated consumption times the length.

    It is the same for every car (the climb enters through the mass a car of that consumption carries)."""
    s = STRETCHES[sid]
    km = s[3]
    f = HIGHWAY_REAL * temp_factor(stretch_temp(sid, m))
    if s[6] > 0:
        f *= 1.0 + (EXPOSURE[m] - 1.0) * s[6] / 0.72
    cl, de = oriented(sid, direction)
    climb_per_rated = climb_kwh(MASS_PER_RATED * 100.0, cl, de) / km   # kWh per km per (kWh/km rated)
    return f + climb_per_rated


def true_energy_rated(rated, sid, m, direction):
    """kWh a car of this rated consumption (kWh/100 km) uses on a stretch in the month's long-run mean."""
    return true_factor(sid, m, direction) * rated / 100.0 * STRETCHES[sid][3]


def true_energy(model, sid, m, direction):
    return true_energy_rated(FLEET[model][3], sid, m, direction)


MONTHS = list(range(1, 13))
MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
               'October', 'November', 'December']

# ---------------------------------------------------------------- the 2027 projection
# seasonal profiles of long-distance trips (relative, normalised inside each pair)
PROFILES = {
    'ski': [1.85, 2.02, 1.68, 0.62, 0.38, 0.55, 0.86, 0.79, 0.47, 0.41, 0.63, 1.74],
    'lakes': [0.52, 0.57, 0.66, 0.81, 1.02, 1.43, 1.91, 1.77, 1.16, 0.79, 0.58, 0.63],
    'regional': [0.86, 0.84, 0.96, 1.01, 1.06, 1.14, 1.24, 1.21, 1.04, 0.95, 0.86, 0.93],
    'through': [0.71, 0.74, 0.86, 0.97, 1.08, 1.29, 1.46, 1.41, 1.12, 0.92, 0.74, 0.79],
    'resort': [1.38, 1.52, 1.27, 0.74, 0.69, 0.98, 1.36, 1.29, 0.82, 0.61, 0.57, 1.31],
}
# two-way 2027 trips by battery-electric car between district towns, and the profile they follow
OD = [
    ('HAL', 'FEN', 1830, 'regional'), ('HAL', 'CAL', 4210, 'regional'), ('HAL', 'TAM', 940, 'lakes'),
    ('HAL', 'BRE', 2620, 'through'), ('HAL', 'MIR', 710, 'regional'), ('COR', 'FEN', 1760, 'ski'),
    ('COR', 'CAL', 5310, 'ski'), ('COR', 'TAM', 1080, 'ski'), ('COR', 'BRE', 1240, 'ski'),
    ('COR', 'MIR', 1170, 'ski'), ('COR', 'ASH', 820, 'ski'), ('FEN', 'TAM', 1110, 'lakes'),
    ('FEN', 'BRE', 2110, 'resort'), ('CAL', 'TAM', 6190, 'resort'), ('CAL', 'BRE', 8430, 'resort'),
    ('CAL', 'MIR', 3910, 'regional'), ('ASH', 'MIR', 1480, 'regional'), ('TAM', 'MIR', 790, 'lakes'),
    ('BRE', 'MIR', 1390, 'resort'), ('FEN', 'MIR', 690, 'regional'), ('ASH', 'BRE', 1120, 'resort'),
    ('ASH', 'TAM', 640, 'lakes'), ('CAL', 'RUT', 2380, 'regional'), ('ASH', 'RUT', 870, 'regional'),
    ('COR', 'RUT', 510, 'ski'), ('FEN', 'RUT', 420, 'regional'), ('BRE', 'RUT', 380, 'resort'),
]


def od_month_trips(a, b, annual, prof, m):
    p = PROFILES[prof]
    return annual * p[m - 1] / sum(p)
