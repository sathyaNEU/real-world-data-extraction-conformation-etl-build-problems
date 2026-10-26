"""Ardenmoor Mutual's world, 2010 to 2025: four regional home books by postcode district, the repair panel each
region's repairs go through, the national rebuild cost index, and the windstorm, flood and freeze catastrophes with
their regional footprints.

What a repair costs rises with the claims each panel firm has to take on at once (post-event demand surge): past a
free level of claims per firm, firms subcontract, materials run short and customers wait in alternative
accommodation. Pennine's book doubled with the Calder and Colne transfer on 1 January 2021 while its panel stayed at
about thirty firms."""
import datetime as dt
import math
import zlib

import numpy as np

YEARS = list(range(2010, 2026))
REGIONS = ["Fenland", "Pennine", "Severn Vale", "Coastal North"]

DISTRICTS = {
    "Fenland": ["PE1", "PE2", "PE3", "PE4", "PE6", "PE7", "PE11", "PE12", "PE13", "PE14", "PE15", "PE16", "PE19",
                "PE26", "PE27", "PE28", "PE38", "CB6", "CB7", "IP28"],
    "Pennine": ["HX1", "HX2", "HX3", "HX4", "HX5", "HX6", "HX7", "HD1", "HD2", "HD3", "HD4", "HD5", "HD6", "HD7",
                "HD8", "HD9", "OL13", "OL14", "BB4", "BD13", "BD22", "LA2"],
    "Severn Vale": ["GL1", "GL2", "GL3", "GL4", "GL10", "GL11", "GL13", "GL15", "GL19", "GL20", "GL50", "GL51",
                    "GL52", "GL53", "WR1", "WR2", "WR3", "WR4", "WR5", "WR8", "WR9", "WR10", "WR11", "WR13", "WR14"],
    "Coastal North": ["NE24", "NE25", "NE26", "NE27", "NE29", "NE30", "NE61", "NE63", "NE64", "NE65", "NE66",
                      "NE68", "NE70", "NE71", "TD15", "CA7", "CA14", "CA15", "CA25", "CA28"],
}
# the Calder and Colne book sits in the upper Calder and Colne valleys
ACQ = {"HX6": 0.16, "HX7": 0.18, "OL14": 0.15, "HD7": 0.12, "HD8": 0.11, "HD9": 0.14, "OL13": 0.08, "BB4": 0.06}


def book_path(region, y):
    """policies in force at mid-year, thousands"""
    if region == "Severn Vale":
        return 352 + 2.6 * (y - 2010)
    if region == "Pennine":
        base = 128 + 2.2 * (y - 2010)
        return base + (96 if y >= 2021 else 0) + (6 if y >= 2022 else 0)
    if region == "Coastal North":
        return 196 + 3.4 * (y - 2010)
    return 168 + 3.8 * (y - 2010)


PLAN_2027 = {"Severn Vale": 398.0, "Pennine": 268.0, "Coastal North": 252.0, "Fenland": 236.0}

SHARE = {}
for _rg, _ds in DISTRICTS.items():
    _r = np.random.default_rng(len(_rg) * 977)
    _s = _r.gamma(4.0, 1.0, len(_ds))
    SHARE[_rg] = _s / _s.sum()


def policies(region, d, y):
    tot = book_path(region, y) * 1000
    if region == "Pennine" and y >= 2021:
        base = (128 + 2.2 * (y - 2010)) * 1000
        return base * SHARE[region][DISTRICTS[region].index(d)] + (tot - base) * ACQ.get(d, 0.0)
    return tot * SHARE[region][DISTRICTS[region].index(d)]


def weights(region, kind):
    """a peril's district hazard weights (floodplain share, exposed older housing)"""
    ds = DISTRICTS[region]
    r = np.random.default_rng(zlib.crc32((region + "|" + kind).encode()))
    if kind == "flood":
        w = r.gamma(0.6, 1.0, len(ds))
    elif kind == "freeze":
        w = r.gamma(3.0, 1.0, len(ds))
    else:
        w = r.gamma(5.0, 1.0, len(ds))
    return w / w.mean()


def panel_path(region, y):
    """repair panel firms working in the region that year"""
    if region == "Severn Vale":
        return int(round(330 + 4 * (y - 2010)))
    if region == "Pennine":
        return int(round(30 + 0.25 * (y - 2010)))
    if region == "Coastal North":
        return int(round(118 + 2 * (y - 2010)))
    return int(round(104 + 2.2 * (y - 2010)))


PANEL = {}
for _rg in REGIONS:
    _code = {"Fenland": "FN", "Pennine": "PN", "Severn Vale": "SV", "Coastal North": "CN"}[_rg]
    PANEL[_rg] = ["RP-%s-%03d" % (_code, i) for i in range(1, panel_path(_rg, 2025) + 9)]


def panel_in(region, y):
    """the year's panel: a sliding window over the firm list, older firms leaving as newer ones join"""
    n = panel_path(region, y)
    lo = (2025 - y) // 3
    return PANEL[region][lo:lo + n]


# what a claim costs at 2015 prices, by peril
BASE_SEV = {"windstorm": 2600.0, "flood": 31000.0, "freeze": 7800.0}
SURGE_FREE = 18.0
SURGE_SLOPE = 0.038


def surge(u):
    return 1.0 + SURGE_SLOPE * max(0.0, u - SURGE_FREE)


def cost_index(y, m):
    """national rebuild cost index, monthly, 2015 = 100"""
    t = (y - 2015) + (m - 6.5) / 12.0
    base = 100.0 * math.exp(0.028 * t)
    if y >= 2021:
        t2 = (y - 2021) + (m - 1) / 12.0
        base *= math.exp(0.045 * min(t2, 2.0) - 0.01 * max(0.0, t2 - 2.0))
    return base


# ---------------------------------------------------------------- events
# (start date, peril, code or None, {region: claims per 1,000 policies}, flood districts share)
# Named-storm codes follow the claims team's practice: a code only for events it declared.
EVENTS = [
    ("2010-12-18", "freeze", "FRZ1012", {"Pennine": 5.8, "Coastal North": 7.5, "Fenland": 2.6, "Severn Vale": 2.2}),
    ("2011-12-08", "windstorm", None, {"Coastal North": 9.0, "Pennine": 2.6}),
    ("2012-04-29", "flood", None, {"Severn Vale": 0.9, "Fenland": 0.5}),
    ("2012-11-21", "flood", "FLD1211", {"Severn Vale": 1.45, "Pennine": 0.3}),
    ("2013-01-17", "freeze", "FRZ1301", {"Pennine": 5.4, "Coastal North": 2.0}),
    ("2013-10-28", "windstorm", "WND1310", {"Fenland": 11.0, "Severn Vale": 6.0}),
    ("2013-12-05", "windstorm", "WND1312", {"Coastal North": 19.0, "Fenland": 8.0, "Pennine": 3.1}),
    ("2013-12-05", "flood", "SRG1312", {"Fenland": 2.4, "Coastal North": 0.7}),
    ("2014-02-05", "flood", "FLD1402", {"Severn Vale": 1.65}),
    ("2014-02-12", "windstorm", "WND1402", {"Severn Vale": 12.0, "Fenland": 6.0}),
    ("2015-01-08", "windstorm", None, {"Coastal North": 12.0, "Pennine": 3.0}),
    ("2015-12-05", "flood", "DESMOND", {"Pennine": 0.42, "Coastal North": 1.3}),
    ("2015-12-26", "flood", "EVA", {"Pennine": 0.46}),
    ("2016-02-08", "windstorm", None, {"Fenland": 5.0, "Severn Vale": 4.0}),
    ("2017-10-16", "windstorm", None, {"Coastal North": 6.0, "Pennine": 2.6}),
    ("2017-12-10", "freeze", "FRZ1712", {"Pennine": 5.6, "Coastal North": 2.4}),
    ("2018-02-27", "freeze", "FRZ1803", {"Pennine": 5.55, "Coastal North": 9.0, "Fenland": 3.0, "Severn Vale": 3.4}),
    ("2019-06-12", "flood", None, {"Fenland": 0.9, "Severn Vale": 0.6}),
    ("2019-11-07", "flood", None, {"Pennine": 0.25, "Severn Vale": 0.7}),
    ("2020-02-08", "windstorm", "CIARA", {"Pennine": 3.3, "Coastal North": 9.0, "Severn Vale": 5.0}),
    ("2020-02-15", "flood", "DENNIS", {"Severn Vale": 1.6, "Pennine": 0.4}),
    ("2021-02-09", "freeze", None, {"Pennine": 2.2, "Coastal North": 3.0}),
    ("2021-11-26", "windstorm", "ARWEN", {"Coastal North": 21.0, "Pennine": 1.6}),
    ("2022-02-16", "windstorm", "DUDLEY", {"Pennine": 1.8, "Coastal North": 7.0}),
    ("2022-02-18", "windstorm", "EUNICE", {"Fenland": 15.0, "Severn Vale": 11.0}),
    ("2022-12-12", "freeze", "FRZ2212", {"Pennine": 1.9, "Coastal North": 6.5, "Severn Vale": 2.6, "Fenland": 2.0}),
    ("2023-10-19", "flood", "BABET", {"Fenland": 1.0, "Pennine": 0.45}),
    ("2024-01-02", "flood", "HENK", {"Severn Vale": 1.5, "Fenland": 0.8}),
    ("2024-01-21", "windstorm", "ISHA", {"Coastal North": 10.0, "Pennine": 1.7}),
    ("2024-01-08", "freeze", None, {"Pennine": 1.3, "Coastal North": 0.9}),
    ("2024-11-23", "windstorm", "BERT", {"Pennine": 1.6, "Severn Vale": 3.5}),
    ("2024-12-06", "windstorm", "DARRAGH", {"Severn Vale": 7.0, "Fenland": 5.0}),
    ("2025-01-24", "windstorm", "EOWYN", {"Coastal North": 13.0, "Pennine": 2.0}),
]

def event_list():
    out = []
    for i, (d, peril, code, rates) in enumerate(EVENTS):
        out.append({"i": i, "date": dt.date.fromisoformat(d), "peril": peril, "code": code, "rates": rates})
    return out
