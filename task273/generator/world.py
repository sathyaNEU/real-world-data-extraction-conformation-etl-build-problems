"""The world behind task273: the Stonereach Valley's roads, the miles each kind of vehicle drives on each class of road
in each hour of the week, and the crashes those miles produce. Everything here is truth the pack never states; the
records, the documents and the analysis read it only through the files the pack ships."""
import calendar
import datetime as dt

import numpy as np

import common as K

H = np.arange(24)
NIGHT = set(range(0, 6)) | {21, 22, 23}

# share of the region's annual vehicle miles on each road class (2025), and its drift a year (2021 to 2025)
VMT_SHARE = {(1, "U"): 0.165, (2, "U"): 0.060, (3, "U"): 0.140, (4, "U"): 0.130, (5, "U"): 0.070, (7, "U"): 0.075,
             (1, "R"): 0.100, (2, "R"): 0.020, (3, "R"): 0.070, (4, "R"): 0.060, (5, "R"): 0.050, (6, "R"): 0.020,
             (7, "R"): 0.040}
VMT_TOTAL = {2021: 11.62e9, 2022: 11.93e9, 2023: 12.14e9, 2024: 12.31e9, 2025: 12.42e9}
DRIFT = {(1, "U"): 0.004, (2, "U"): 0.002, (3, "U"): -0.002, (4, "U"): -0.001, (5, "U"): 0.000, (7, "U"): 0.001,
         (1, "R"): 0.002, (2, "R"): 0.000, (3, "R"): -0.002, (4, "R"): -0.001, (5, "R"): -0.001, (6, "R"): -0.001,
         (7, "R"): -0.001}


def bump(h, c, w):
    d = np.minimum(np.abs(h - c), 24 - np.abs(h - c))
    return np.exp(-d ** 2 / (2.0 * w * w))


def days_of(year):
    """Every date of the year by day type (weekday Monday to Friday, weekend Saturday and Sunday)."""
    out = {"wd": [], "we": []}
    d = dt.date(year, 1, 1)
    while d.year == year:
        out["we" if d.weekday() >= 5 else "wd"].append(d)
        d += dt.timedelta(days=1)
    return out


NDAYS = {y: {k: len(v) for k, v in days_of(y).items()} for y in K.YEARS}


# ---------------------------------------------------------------------------------------------------------------
# traffic by road class: within-day hourly shares (weekday, weekend day) and the weekend day's volume
def group_hours(g):
    urban = g[0] == "U"
    if urban:
        wk = 0.35 + 3.2 * bump(H, 7.6, 1.2) + 3.4 * bump(H, 16.8, 1.7) + 2.2 * bump(H, 12.5, 3.5) \
            + 0.9 * bump(H, 20.5, 2.0)
        we = 0.45 + 2.6 * bump(H, 13.5, 4.0) + 0.9 * bump(H, 20.5, 2.5)
    else:
        wk = 0.30 + 1.6 * bump(H, 7.8, 1.6) + 2.0 * bump(H, 16.5, 2.0) + 2.4 * bump(H, 12.5, 3.8)
        we = 0.35 + 2.9 * bump(H, 13.0, 4.0)
    if g in ("UF", "RF"):
        wk = wk + 0.25
        we = we + 0.25
    return {"wd": wk / wk.sum(), "we": we / we.sum()}, (0.86 if urban else 1.02)


GROUP_HOURS = {g: group_hours(g) for g in K.GROUPS}
MONTH = {   # each road class group's monthly volume against its average month
    "U": [0.94, 0.96, 0.99, 1.00, 1.02, 1.03, 1.02, 1.03, 1.02, 1.01, 0.99, 0.99],
    "R": [0.86, 0.89, 0.95, 0.99, 1.05, 1.10, 1.14, 1.13, 1.06, 1.00, 0.93, 0.90]}


def cell_share(hours, wef, year):
    """Share of a year's miles in each (day type, hour), given within-day hourly shares and the weekend factor."""
    n = NDAYS[year]
    wk = hours["wd"] * n["wd"]
    we = hours["we"] * n["we"] * wef
    t = wk.sum() + we.sum()
    return {"wd": wk / t, "we": we / t}


def vmt(year, fc_ur):
    sh = VMT_SHARE[fc_ur] * (1.0 + DRIFT[fc_ur] * (year - 2025))
    tot = sum(VMT_SHARE[k] * (1.0 + DRIFT[k] * (year - 2025)) for k in VMT_SHARE)
    return VMT_TOTAL[year] * sh / tot


# ---------------------------------------------------------------------------------------------------------------
# who drives where and when. Shares of the region's miles by year, road mix (relative to the class's miles), and
# within-day hours with the weekend day's volume against a weekday's.
SHARE = {
    "TX": {2021: 0.0085, 2022: 0.0080, 2023: 0.0076, 2024: 0.0072, 2025: 0.0069},
    "RH": {2021: 0.0215, 2022: 0.0268, 2023: 0.0301, 2024: 0.0322, 2025: 0.0338},
    "LM": {2021: 0.0036, 2022: 0.0041, 2023: 0.0043, 2024: 0.0044, 2025: 0.0045},
    "AS": {2021: 0.0042, 2022: 0.0051, 2023: 0.0055, 2024: 0.0057, 2025: 0.0058},
    "PT": {2021: 0.0058, 2022: 0.0061, 2023: 0.0062, 2024: 0.0063, 2025: 0.0064},
    "PD": {2021: 0.0171, 2022: 0.0174, 2023: 0.0176, 2024: 0.0178, 2025: 0.0181},
    "AD": {2021: 0.0158, 2022: 0.0151, 2023: 0.0149, 2024: 0.0150, 2025: 0.0153},
    "OC": {y: 0.0560 for y in K.YEARS},
    "TB": {y: 0.0042 for y in K.YEARS},
    "SB": {y: 0.0015 for y in K.YEARS},
    "GV": {y: 0.0128 for y in K.YEARS},
    "EM": {y: 0.0021 for y in K.YEARS},
    "MC": {y: 0.0068 for y in K.YEARS},
}
ROAD = {   # by road class group
    "TX": {"UF": 0.80, "UA": 1.70, "UL": 1.20, "RF": 0.15, "RA": 0.08, "RL": 0.04},
    "RH": {"UF": 0.55, "UA": 1.55, "UL": 1.65, "RF": 0.20, "RA": 0.10, "RL": 0.05},
    "LM": {"UF": 1.90, "UA": 0.80, "UL": 0.35, "RF": 1.20, "RA": 0.40, "RL": 0.15},
    "AS": {"UF": 2.90, "UA": 0.45, "UL": 0.15, "RF": 1.70, "RA": 0.30, "RL": 0.08},
    "PT": {"UF": 1.70, "UA": 0.75, "UL": 0.28, "RF": 1.30, "RA": 1.60, "RL": 0.55},
    "PD": {"UF": 0.40, "UA": 1.25, "UL": 2.90, "RF": 0.30, "RA": 0.50, "RL": 1.00},
    "AD": {"UF": 0.35, "UA": 1.70, "UL": 2.10, "RF": 0.10, "RA": 0.15, "RL": 0.15},
    "OC": {"UF": 1.40, "UA": 0.85, "UL": 0.55, "RF": 1.90, "RA": 1.10, "RL": 0.55},
    "TB": {"UF": 0.40, "UA": 2.20, "UL": 0.90, "RF": 0.20, "RA": 0.40, "RL": 0.10},
    "SB": {"UF": 0.20, "UA": 1.20, "UL": 1.40, "RF": 0.20, "RA": 1.00, "RL": 1.20},
    "GV": {"UF": 0.90, "UA": 1.10, "UL": 1.10, "RF": 0.80, "RA": 1.00, "RL": 1.00},
    "EM": {"UF": 0.90, "UA": 1.40, "UL": 1.10, "RF": 0.60, "RA": 0.70, "RL": 0.50},
    "MC": {"UF": 0.80, "UA": 1.00, "UL": 0.80, "RF": 1.00, "RA": 1.50, "RL": 1.10},
}


def use_hours(u):
    if u == "RH":
        wk = 0.9 + 1.0 * bump(H, 8.0, 1.5) + 1.2 * bump(H, 17.5, 2.0) + 2.6 * bump(H, 22.5, 2.6) + 1.8 * bump(H, 1.5, 1.6)
        we = 1.0 + 1.6 * bump(H, 13.0, 3.5) + 3.6 * bump(H, 23.0, 2.6) + 3.2 * bump(H, 1.8, 1.8)
        wef = 1.35
    elif u == "TX":
        wk = 0.5 + 1.6 * bump(H, 8.5, 2.0) + 1.5 * bump(H, 14.0, 3.5) + 1.3 * bump(H, 19.0, 2.5) + 0.9 * bump(H, 0.5, 2.0)
        we = 0.6 + 1.3 * bump(H, 13.0, 4.0) + 1.5 * bump(H, 22.5, 2.5) + 1.1 * bump(H, 1.5, 1.8)
        wef = 1.05
    elif u == "LM":
        wk = 0.25 + 1.3 * bump(H, 6.0, 1.5) + 1.0 * bump(H, 14.0, 4.0) + 1.9 * bump(H, 21.0, 2.0) + 1.3 * bump(H, 0.5, 1.6)
        we = 0.30 + 1.0 * bump(H, 13.0, 4.0) + 2.6 * bump(H, 21.5, 2.2) + 2.2 * bump(H, 1.0, 1.8)
        wef = 1.45
    elif u == "AS":
        wk = 0.06 + 2.2 * bump(H, 6.3, 1.2) + 1.9 * bump(H, 10.0, 2.5) + 1.5 * bump(H, 14.5, 3.0) + 0.8 * bump(H, 19.0, 1.8)
        we = 0.06 + 1.9 * bump(H, 6.8, 1.4) + 1.7 * bump(H, 11.0, 3.0) + 1.2 * bump(H, 16.5, 3.0)
        wef = 0.85
    elif u == "PT":
        wk = 0.02 + 2.2 * bump(H, 10.0, 2.0) + 2.0 * bump(H, 14.0, 2.0)
        we = 0.02 + 1.0 * bump(H, 12.0, 2.2)
        wef = 0.30
    elif u == "PD":
        wk = 0.05 + 2.2 * bump(H, 11.0, 2.8) + 1.9 * bump(H, 16.5, 2.2) + 1.0 * bump(H, 19.8, 1.5)
        we = 0.05 + 1.3 * bump(H, 12.5, 3.0) + 0.6 * bump(H, 19.0, 1.8)
        wef = 0.40
    elif u == "AD":
        wk = 0.3 + 2.0 * bump(H, 12.3, 1.3) + 3.2 * bump(H, 19.3, 1.8) + 0.9 * bump(H, 22.8, 1.6)
        we = 0.4 + 2.2 * bump(H, 12.8, 1.6) + 3.8 * bump(H, 19.0, 2.0) + 1.4 * bump(H, 23.0, 1.8)
        wef = 1.4
    elif u == "OC":
        wk = 0.35 + 1.9 * bump(H, 9.0, 3.0) + 1.6 * bump(H, 14.0, 3.0)
        we = 0.30 + 0.8 * bump(H, 12.0, 4.0)
        wef = 0.45
    elif u == "TB":
        wk = 0.05 + 1.6 * bump(H, 7.5, 2.0) + 1.2 * bump(H, 12.5, 4.0) + 1.6 * bump(H, 17.0, 2.0)
        we = 0.05 + 1.0 * bump(H, 13.0, 4.5)
        wef = 0.55
    elif u == "SB":
        wk = 0.01 + 3.0 * bump(H, 7.3, 0.9) + 2.6 * bump(H, 15.2, 1.0)
        we = 0.01 + 0.1 * bump(H, 12.0, 3.0)
        wef = 0.05
    elif u in ("GV", "EM"):
        wk = 0.20 + 1.8 * bump(H, 10.0, 3.5) + 1.2 * bump(H, 15.0, 2.5)
        we = 0.20 + 0.8 * bump(H, 12.0, 4.0)
        wef = 0.50 if u == "GV" else 0.95
    elif u == "MC":
        wk = 0.15 + 1.2 * bump(H, 8.0, 2.0) + 1.8 * bump(H, 16.5, 2.5)
        we = 0.15 + 2.6 * bump(H, 14.0, 3.5)
        wef = 1.60
    return {"wd": wk / wk.sum(), "we": we / we.sum()}, wef


USE_HOURS = {u: use_hours(u) for u in ROAD}
ALL_USES = ["PV"] + list(ROAD)

# conditional propensity to be the driver at fault in a crash between moving vehicles (private drivers 1), by use;
# single-vehicle crashes, parked vehicles struck and non-motorists struck use their own
RHO = {"PV": 1.00, "TX": 1.05, "RH": 1.05, "LM": 1.06, "AS": 1.74, "PT": 1.70, "PD": 1.42, "AD": 1.18,
       "OC": 1.10, "TB": 0.85, "SB": 0.70, "GV": 0.95, "EM": 1.30, "MC": 1.25}
RHO_SV = {"PV": 1.00, "TX": 0.55, "RH": 0.80, "LM": 0.60, "AS": 0.70, "PT": 0.50, "PD": 0.75, "AD": 1.10,
          "OC": 0.90, "TB": 0.30, "SB": 0.25, "GV": 0.60, "EM": 0.80, "MC": 4.50}
RHO_NM = {"PV": 1.00, "TX": 1.30, "RH": 1.20, "LM": 0.90, "AS": 0.90, "PT": 1.00, "PD": 1.45, "AD": 1.35,
          "OC": 1.00, "TB": 1.60, "SB": 0.60, "GV": 0.90, "EM": 0.90, "MC": 0.40}


def intensity(kind, g, d, h):
    """Crashes per mile (relative) of each kind in a road class group, day type and hour."""
    if kind == "MV":
        base = {"UF": 0.52, "UA": 1.70, "UL": 1.40, "RF": 0.30, "RA": 0.88, "RL": 0.98}[g]
        f = 1.0 + 1.6 * bump(h, 2.2, 2.0) + 0.6 * bump(h, 22.0, 1.6) - 0.08 * bump(h, 11.5, 2.0)
        if d == "we":
            f *= 1.0 + 0.7 * bump(h, 2.0, 2.2)
        if d == "wd" and g in ("UF", "UA"):
            f *= 1.0 + 0.30 * bump(h, 8.0, 1.2) + 0.35 * bump(h, 17.2, 1.4)
        return base * f
    if kind == "SV":
        base = {"UF": 0.45, "UA": 0.55, "UL": 0.70, "RF": 0.65, "RA": 1.60, "RL": 2.30}[g]
        f = 1.0 + 3.0 * bump(h, 2.0, 2.2) + 0.9 * bump(h, 22.0, 1.8)
        if d == "we":
            f *= 1.0 + 0.9 * bump(h, 2.0, 2.2)
        return base * f
    if kind == "PK":
        base = {"UF": 0.02, "UA": 0.90, "UL": 2.20, "RF": 0.01, "RA": 0.15, "RL": 0.35}[g]
        return base * (1.0 + 0.8 * bump(h, 1.5, 2.5))
    if kind == "PED":
        base = {"UF": 0.03, "UA": 1.60, "UL": 1.20, "RF": 0.02, "RA": 0.25, "RL": 0.20}[g]
        return base * (1.0 + 1.4 * bump(h, 19.5, 2.2) + 0.8 * bump(h, 1.0, 2.0))
    if kind == "CYC":
        base = {"UF": 0.00, "UA": 1.40, "UL": 1.30, "RF": 0.00, "RA": 0.35, "RL": 0.40}[g]
        return base * (1.0 + 0.6 * bump(h, 17.0, 2.0))
    raise ValueError(kind)


# crashes of each kind over the five years (expected), the region's scale
TARGET = {"MV": 125000, "SV": 33000, "PK": 11000, "PED": 4200, "CYC": 3000}

# where parked vehicles stand: presence weight by use against private cars (curb time a mile driven)
PARKED = {"PV": 1.0, "TX": 2.4, "RH": 0.35, "LM": 1.2, "AS": 0.9, "PT": 1.6, "PD": 4.2, "AD": 1.6,
          "OC": 1.5, "TB": 0.2, "SB": 0.3, "GV": 1.0, "EM": 0.6, "MC": 0.8}


def miles_table():
    """Miles by (year, functional class, urban or rural, day type, hour, use): the truth every crash is drawn from.
    Returns cells (keys), E (all traffic) and m (by use, private as the remainder)."""
    cells, E, m = [], {}, {}
    for y in K.YEARS:
        tot = VMT_TOTAL[y]
        gshare = {g: cell_share(GROUP_HOURS[g][0], GROUP_HOURS[g][1], y) for g in K.GROUPS}
        ushare = {u: cell_share(USE_HOURS[u][0], USE_HOURS[u][1], y) for u in ROAD}
        rmix = {}
        for u in ROAD:
            w = {fu: vmt(y, fu) * ROAD[u][K.GROUP_OF[fu]] for fu in VMT_SHARE}
            t = sum(w.values())
            rmix[u] = {fu: v / t for fu, v in w.items()}
        for fu in VMT_SHARE:
            g = K.GROUP_OF[fu]
            v = vmt(y, fu)
            for d in ("wd", "we"):
                for h in range(24):
                    c = (y, fu[0], fu[1], d, h)
                    cells.append(c)
                    E[c] = v * gshare[g][d][h]
                    rest = E[c]
                    for u in ROAD:
                        x = SHARE[u][y] * tot * rmix[u][fu] * ushare[u][d][h]
                        m[(u, c)] = x
                        rest -= x
                    assert rest > 0.12 * E[c], (c, rest / E[c])
                    m[("PV", c)] = rest
    return cells, E, m


def expected_ratios():
    """Each use's true rate per mile of causing a crash between moving vehicles, against private drivers'."""
    cells, E, m = miles_table()
    af = {u: 0.0 for u in ALL_USES}
    mi = {u: 0.0 for u in ALL_USES}
    for c in cells:
        g = K.GROUP_OF[(c[1], c[2])]
        ci = intensity("MV", g, c[3], c[4])
        for u in ALL_USES:
            af[u] += ci * RHO[u] * m[(u, c)]
            mi[u] += m[(u, c)]
    return {u: (af[u] / mi[u]) / (af["PV"] / mi["PV"]) for u in ALL_USES}


if __name__ == "__main__":
    r = expected_ratios()
    for u in K.CODES:
        print("%s %.3f" % (u, r[u]))
