"""task229 generator: the world. Stations, ratings (superseded and current), plants, telemetry, the 2027 outlook.

Everything here is the design's fixed structure; truth.py makes the record from it."""
from datetime import date

import numpy as np

import params as P

M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# number, name, river, river km from the mouth, drainage area km2, regime, water-level resolution (m),
# field unit, new platform, cut-over (first day on the new platform), GOES slot (UTC hh:mm)
STATIONS = [
    ("C101", "Ashlin River above Lake Ashlin", "Ashlin River", 14.6, 212.0, "snow", 0.001, "m3/s", "cellular", date(2026, 2, 17), "04:37"),
    ("C102", "Lake Ashlin at the outlet weir", "Ashlin River", 9.8, 268.0, "lake", 0.01, "m3/s", "cellular", date(2026, 3, 10), "01:12"),
    ("C103", "Wren Creek near Corriston", "Wren Creek", 2.1, 64.0, "snow", 0.001, "m3/s", "cellular", date(2026, 4, 21), "05:48"),
    ("C104", "Corriston River below Talbot Canyon", "Corriston River", 30.6, 498.0, "talbot", 0.001, "m3/s", "Iridium", date(2026, 6, 16), "02:23"),
    ("C105", "Corriston River at Hollis Bridge", "Corriston River", 28.8, 526.0, "talbot", 0.001, "m3/s", "Iridium", date(2026, 6, 17), "00:41"),
    ("C106", "Tolley Creek at the highway", "Tolley Creek", 1.4, 88.0, "rainsnow", 0.001, "m3/s", "cellular", date(2026, 5, 5), "03:06"),
    ("C107", "Sable Creek near the mouth", "Sable Creek", 0.9, 46.0, "flashy", 0.001, "m3/s", "cellular", date(2026, 9, 23), "05:15"),
    ("C108", "Marrock River at Brandt Flats", "Marrock River", 11.3, 377.0, "glacier", 0.001, "m3/s", "cellular", date(2026, 7, 8), "01:54"),
    ("C109", "Fenn Creek below the powerhouse", "Fenn Creek", 3.6, 121.0, "snow", 0.001, "m3/s", "cellular", date(2026, 3, 24), "04:02"),
    ("C110", "Mattin Creek at the gravel pit", "Mattin Creek", 6.1, 81.0, "snow", 0.001, "m3/s", "cellular", date(2026, 2, 10), "00:58"),
    ("C111", "Pellam Creek at the springs", "Pellam Creek", 4.0, 9.5, "spring", 0.01, "L/s", "cellular", date(2026, 8, 11), "02:46"),
    ("C112", "Merrin Creek below Merrin Falls", "Merrin Creek", 7.1, 214.0, "merrin", 0.001, "m3/s", "Iridium", date(2026, 6, 23), "05:31"),
    ("C113", "Merrin Creek at Dunlop Road", "Merrin Creek", 4.8, 225.0, "merrin", 0.001, "m3/s", "Iridium", date(2026, 6, 24), "03:39"),
    ("C114", "Hallam Creek near the mouth", "Hallam Creek", 0.6, 152.0, "glacier", 0.001, "m3/s", "cellular", date(2026, 7, 29), "01:27"),
    ("C115", "Garrow Creek at the springs", "Garrow Creek", 2.7, 6.8, "spring", 0.01, "L/s", "cellular", date(2026, 8, 12), "04:20"),
    ("C116", "Cawdell Creek above the intake", "Cawdell Creek", 5.5, 58.0, "snow", 0.001, "m3/s", "cellular", date(2026, 9, 21), "00:19"),
    ("C117", "Whitlow Creek at Marsh Road", "Whitlow Creek", 3.3, 97.0, "rain", 0.001, "m3/s", "cellular", date(2026, 4, 28), "02:09"),
    ("C118", "Ostrey Creek near Hendry", "Ostrey Creek", 8.2, 133.0, "rainsnow", 0.001, "m3/s", "cellular", date(2026, 5, 19), "05:57"),
    ("C119", "Fallon River at the old bridge", "Fallon River", 15.7, 412.0, "snow", 0.001, "m3/s", "cellular", date(2026, 6, 2), "03:22"),
    ("C120", "Keddie Creek near Stowe", "Keddie Creek", 2.2, 71.0, "rain", 0.001, "m3/s", "cellular", date(2026, 9, 28), "01:03"),
    ("C121", "Rusk Creek at the fish fence", "Rusk Creek", 1.1, 39.0, "rainsnow", 0.001, "m3/s", "cellular", date(2026, 2, 24), "04:44"),
    ("C122", "Mattin Creek at Quarry Road", "Mattin Creek", 6.4, 80.0, "snow", 0.001, "m3/s", "cellular", P.RELOC_START, ""),
    ("C123", "Dorran Creek above the canyon", "Dorran Creek", 9.1, 104.0, "glacier", 0.001, "m3/s", "cellular", date(2026, 3, 31), "02:58"),
    ("C124", "Merrin Creek near the mouth", "Merrin Creek", 0.9, 652.0, "merrin", 0.001, "m3/s", "cellular", date(2026, 5, 12), "03:51"),
]
COLS = ["no", "name", "river", "km", "area", "regime", "res", "unit", "new_platform", "cutover", "slot"]
ST = {s[0]: dict(zip(COLS, s)) for s in STATIONS}
CURRENT = [s[0] for s in STATIONS if s[0] != "C110"]       # the 22 stations of 2027
assert len(CURRENT) == 23
OLD_SITE = {"C122": "C110"}
ESTABLISHED = {"C101": 1998, "C102": 1987, "C103": 2004, "C104": 2009, "C105": 1979, "C106": 2001, "C107": 2011,
               "C108": 1994, "C109": 2012, "C110": 2006, "C111": 2015, "C112": 2003, "C113": 1991, "C114": 2008,
               "C115": 2016, "C116": 1999, "C117": 1996, "C118": 2005, "C119": 1983, "C120": 2010, "C121": 2013,
               "C122": 2026, "C123": 2002, "C124": 1985}
BRAIDED = {"C108", "C119"}
SPRING = {"C111", "C115"}

# Plants (Corriston Hydro Ltd.)
TALBOT = {"name": "Talbot Canyon Generating Station", "river": "Corriston River", "tailrace_km": 31.2,
          "fmin": 1.8, "cap": 64.0, "node_area": 478.0, "since": 2017}
MERRIN = {"name": "Merrin Falls Generating Station", "river": "Merrin Creek", "tailrace_km": 7.9,
          "fmin": 0.7, "cap": 28.0, "node_area": 205.0, "in_service": date(2027, 6, 1)}
FENN = {"name": "Fenn Creek Generating Station", "river": "Fenn Creek", "tailrace_km": 4.1}
CONTINUOUS_MONTHS = {5, 6}              # freshet: continuous generation 1 May to 30 June
PLANT_OF = {"C104": "talbot", "C105": "talbot", "C112": "merrin", "C113": "merrin", "C124": "merrin"}
# the Vardy River joins Merrin Creek 2.6 km above its mouth, unregulated and ungauged (glacier and rain)
VARDY_AREA = 412.0
VARDY = [2.55, 2.25, 2.40, 3.45, 6.10, 8.30, 9.10, 4.70, 3.55, 4.20, 4.60, 2.95]   # m3/s per 100 km2

# Current ratings (in force from 1 April 2026; C122 from 4 June 2026): Q = C (h - e)^b, Q in m3/s, h in m.
RATING = {
    "C101": (14.2, 0.284, 1.72), "C102": (31.5, 0.912, 1.58), "C103": (5.35, 0.163, 1.84),
    "C104": (8.40, 0.210, 1.80), "C105": (11.2, 0.340, 1.95), "C106": (6.10, 0.241, 1.69),
    "C107": (3.95, 0.118, 2.06), "C108": (19.8, 0.402, 1.63), "C109": (7.75, 0.196, 1.91),
    "C110": (6.62, 0.233, 1.78), "C111": (0.610, 0.214, 1.92), "C112": (6.10, 0.120, 1.75),
    "C113": (7.70, 0.180, 1.90), "C114": (12.6, 0.355, 1.67), "C115": (0.455, 0.188, 2.11),
    "C116": (4.88, 0.146, 1.98), "C117": (6.95, 0.266, 1.74), "C118": (8.15, 0.301, 1.81),
    "C119": (17.4, 0.448, 1.62), "C120": (5.60, 0.207, 1.88), "C121": (3.40, 0.131, 2.02),
    "C122": (6.34, 0.198, 1.83), "C123": (9.90, 0.278, 1.76), "C124": (22.6, 0.515, 1.68),
}
RATING_NO = {k: "%s-R%d" % (k, n) for k, n in zip(sorted(RATING), [6, 4, 5, 7, 9, 5, 3, 8, 3, 4, 2, 5, 8, 4, 2, 6, 7, 5, 9, 3, 2, 1, 5, 11])}
# Superseded ratings (the 2019 review's, in force until 31 March 2026): the refit moved each by 1.5 to 6 per cent
# at its winter flows, with a small tilt over the range; the water level of zero flow is surveyed and did not move.
OLD_TARGET = {  # per cent at the station's January flow, and the tilt in the exponent
    "C101": (3.1, -0.03), "C102": (-2.4, 0.02), "C103": (4.2, -0.02), "C104": (-3.3, 0.03), "C105": (4.8, -0.03),
    "C106": (-2.9, 0.02), "C107": (5.1, -0.04), "C108": (-1.9, 0.03), "C109": (2.6, -0.02), "C110": (3.7, 0.02),
    "C111": (-2.2, 0.02), "C112": (1.8, -0.03), "C113": (-3.9, 0.04), "C114": (2.3, -0.02), "C115": (2.7, -0.03),
    "C116": (-3.6, 0.03), "C117": (4.4, -0.02), "C118": (-4.6, 0.03), "C119": (2.1, -0.04), "C120": (-3.1, 0.02),
    "C121": (3.4, -0.03), "C123": (-2.8, 0.02), "C124": (2.9, -0.02),
}


def _old(no):
    C, e, b = RATING[no]
    pct, db = OLD_TARGET[no]
    q_jan = clim_hist(no, 1)
    x0 = (q_jan / C) ** (1.0 / b)
    C0 = C * (1 + pct / 100.0) * x0 ** (-db)
    return (round(C0, 5), e, round(b + db, 3))




def q_of_h(par, h):
    C, e, b = par
    return C * np.clip(np.asarray(h, float) - e, 0, None) ** b


def h_of_q(par, q):
    C, e, b = par
    return e + (np.asarray(q, float) / C) ** (1.0 / b)


# Monthly climatology of daily mean natural flow, m3/s per 100 km2 (Jan..Dec), by regime.
CLIM = {
    "snow":     [0.95, 0.86, 1.05, 2.40, 7.80, 9.40, 4.10, 1.85, 1.40, 1.85, 2.10, 1.25],
    "flashy":   [1.10, 1.00, 1.30, 3.10, 9.90, 10.8, 3.60, 1.50, 1.20, 2.00, 2.40, 1.40],
    "glacier":  [0.70, 0.62, 0.74, 1.40, 4.90, 9.80, 12.1, 10.2, 5.40, 2.60, 1.60, 0.90],
    "rain":     [6.10, 5.20, 4.60, 3.60, 2.70, 1.90, 0.95, 0.62, 0.88, 3.80, 7.40, 6.90],
    "rainsnow": [3.90, 3.40, 3.30, 3.70, 5.30, 4.60, 1.90, 0.95, 1.10, 3.10, 5.10, 4.40],
    "spring":   [0.52, 0.51, 0.51, 0.53, 0.58, 0.62, 0.60, 0.56, 0.54, 0.53, 0.53, 0.52],
    "lake":     [1.05, 0.96, 1.02, 1.80, 5.30, 7.40, 4.60, 2.20, 1.55, 1.85, 2.05, 1.35],
}
# the plants' forebay inflow nodes and the local drainage use the snow regime, scaled to these 2027 flows
TALBOT_2027 = [5.6, 5.1, 6.4, 11.8, 38.0, 46.0, 19.5, 9.8, 7.4, 8.9, 9.6, 6.8]
MERRIN_2027 = [2.1, 1.9, 2.5, 5.2, 17.0, 21.5, 8.6, 4.1, 3.0, 3.8, 4.2, 2.6]
# Talbot's history runs above its 2027 outlook outside the freshet (a dry autumn and winter forecast for the
# Corriston), so its published record, low by the swing, sits near the outlook (the masking line)
TALBOT_HIST = [t / f for t, f in zip(TALBOT_2027, [0.899, 0.917, 0.830, 0.777, 0.98, 0.99, 0.911, 0.707, 0.778, 0.809, 0.709, 0.764])]
MERRIN_HIST = [m / f for m, f in zip(MERRIN_2027, [1.03, 1.05, 1.01, 0.97, 0.96, 0.98, 1.04, 1.06, 1.02, 0.99, 1.02, 1.04])]
# local inflow per km2 relative to the node's (the canyon walls drain steep, wet ground)
LOCAL_YIELD = {"C104": 0.90, "C105": 0.95, "C112": 0.88, "C113": 0.92, "C124": 0.92}
# station yield multipliers on its regime's climatology (history)
YIELD = {"C101": 1.08, "C102": 1.00, "C103": 0.92, "C106": 1.05, "C107": 1.00, "C108": 0.97, "C109": 1.04,
         "C110": 0.96, "C111": 1.00, "C114": 1.02, "C115": 0.95, "C116": 1.10, "C117": 0.98, "C118": 1.03,
         "C119": 0.99, "C120": 1.01, "C121": 1.06, "C122": 0.96, "C123": 1.00}
# 2027 outlook factors on history by regime-month (sub-basin spread), chosen so the regulated stations'
# outlook-to-record ratios sit inside the unregulated spread
F2027 = {
    "C101": [1.12, 1.08, 1.04, 0.96, 0.94, 0.97, 1.05, 1.10, 1.14, 1.18, 1.15, 1.10],
    "C102": [1.08, 1.06, 1.03, 0.97, 0.95, 0.98, 1.03, 1.07, 1.10, 1.12, 1.10, 1.06],
    "C103": [0.92, 0.90, 0.93, 0.98, 1.02, 1.01, 0.95, 0.90, 0.88, 0.86, 0.89, 0.91],
    "C106": [0.95, 0.94, 0.97, 1.02, 1.04, 1.00, 0.93, 0.90, 0.92, 0.94, 0.96, 0.97],
    "C107": [1.02, 1.00, 1.03, 1.06, 1.90, 1.90, 1.18, 1.10, 1.05, 1.03, 1.02, 1.01],
    "C108": [0.88, 0.86, 0.90, 0.95, 1.00, 1.03, 1.06, 1.02, 0.96, 0.90, 0.87, 0.88],
    "C109": [1.06, 1.05, 1.02, 0.99, 0.97, 0.98, 1.01, 1.04, 1.07, 1.09, 1.08, 1.06],
    "C111": [1.01, 1.01, 1.00, 1.00, 1.01, 1.02, 1.02, 1.01, 1.00, 1.00, 1.01, 1.01],
    "C114": [0.90, 0.88, 0.91, 0.96, 1.01, 1.04, 1.07, 1.05, 0.98, 0.92, 0.89, 0.90],
    "C115": [0.99, 0.99, 0.99, 1.00, 1.00, 1.01, 1.01, 1.00, 1.00, 0.99, 0.99, 0.99],
    "C116": [1.15, 1.13, 1.09, 1.02, 0.97, 0.99, 1.06, 1.12, 1.17, 1.21, 1.19, 1.16],
    "C117": [1.10, 1.07, 1.04, 1.01, 0.98, 0.96, 0.92, 0.90, 0.95, 1.05, 1.11, 1.12],
    "C118": [0.86, 0.85, 0.88, 0.93, 0.97, 0.95, 0.90, 0.87, 0.89, 0.91, 0.88, 0.87],
    "C119": [0.97, 0.96, 0.98, 1.00, 1.02, 1.03, 1.00, 0.97, 0.96, 0.96, 0.97, 0.97],
    "C120": [1.18, 1.14, 1.10, 1.05, 1.00, 0.95, 0.90, 0.88, 0.94, 1.08, 1.16, 1.20],
    "C121": [0.94, 0.93, 0.95, 0.99, 1.02, 0.99, 0.94, 0.91, 0.92, 0.95, 0.96, 0.95],
    "C122": [1.03, 1.02, 1.00, 0.98, 0.97, 0.99, 1.02, 1.05, 1.06, 1.07, 1.06, 1.04],
    "C123": [0.84, 0.83, 0.86, 0.92, 0.98, 1.02, 1.05, 1.03, 0.95, 0.89, 0.85, 0.84],
}


VARDY_2027 = [1.02, 1.01, 0.99, 0.98, 0.99, 1.01, 1.03, 1.04, 1.02, 1.00, 1.01, 1.02]


def vardy(m):
    return VARDY[m - 1] * VARDY_AREA / 100.0


def node_hist(plant, m):
    return (TALBOT_HIST if plant == "talbot" else MERRIN_HIST)[m - 1]


def node_2027(plant, m):
    return (TALBOT_2027 if plant == "talbot" else MERRIN_2027)[m - 1]


def local_area(no):
    p = PLANT_OF[no]
    a = ST[no]["area"] - (TALBOT if p == "talbot" else MERRIN)["node_area"]
    return a - VARDY_AREA if no == "C124" else a


def local_share(no):
    """local inflow as a share of the node inflow (area ratio times the local yield)"""
    p = PLANT_OF[no]
    na = (TALBOT if p == "talbot" else MERRIN)["node_area"]
    return local_area(no) / na * LOCAL_YIELD[no]


def clim_hist(no, m):
    """historical mean natural flow (m3/s) of a station in calendar month m"""
    if no in PLANT_OF:
        p = PLANT_OF[no]
        v = node_hist(p, m) * (1 + local_share(no))
        return v + vardy(m) if no == "C124" else v
    rg = ST[no]["regime"]
    return CLIM[rg][m - 1] * ST[no]["area"] / 100.0 * YIELD[no]


def outlook_2027(no, m):
    """the 2027 water supply outlook's monthly mean flow (m3/s), rounded as published"""
    if no in PLANT_OF:
        p = PLANT_OF[no]
        v = node_2027(p, m) * (1 + local_share(no))
        if no == "C124":
            v += vardy(m) * VARDY_2027[m - 1]
    else:
        v = clim_hist(no, m) * F2027[no][m - 1]
    return float(sig(v, 3))


def sig(x, n):
    x = float(x)
    if x == 0:
        return 0.0
    d = int(np.floor(np.log10(abs(x))))
    return round(x, n - 1 - d)


OLD_RATING = {k: _old(k) for k in OLD_TARGET}
OLD_RATING_NO = {k: "%s-R%d" % (k, int(RATING_NO[k].split("R")[1]) - 1) for k in OLD_TARGET}


def install_lead(no, cut):
    """days between the new platform's installation and its first reporting day (the crew's schedule)"""
    return 1 + (int(no[1:]) * 7 + cut.day) % 9
