"""task285 world: the Quarnell valley, its 2025 river model, its roads and its parishes (clean truth).

Everything here is deterministic (seed 285). build.py writes the pack from it; checks.py asserts on it.
"""
import math
import random

SEED = 285
HOURS = list(range(0, 121))
DEPTH_LIMIT = 0.25          # metres of water on the carriageway an emergency ambulance will not enter
DEFAULT_THRESHOLD = 0.15    # PFR scheme: floor level taken as ground level plus 0.15 m where unsurveyed
DATUM_SHIFT = 0.42          # Quarnell Navigation Datum lies 0.42 m above Ordnance Datum Newlyn: its levels read 0.42 m low
E0, N0 = 412000, 456000     # local km grid origin on the national grid


def bng(x, y):
    return int(round(E0 + x * 1000)), int(round(N0 + y * 1000))


# ----------------------------------------------------------------------------------------------- hydrology
# storage area -> name, peak hour, rise and fall widths (hours), base stage and peak stage (mAOD, 2025 run)
SA = {
    "SA-HB1": ("Hollin Beck lower", 15, 6.0, 8.0, 41.05, 43.62),
    "SA-SB1": ("Ravelsby Brook lower", 18, 6.0, 8.0, 37.10, 39.43),
    "SA-MW1": ("Lunnerby Beck lower", 20, 7.0, 8.0, 33.20, 35.51),
    "SA-HB2": ("Hollin Beck upper", 13, 5.0, 7.0, 47.30, 48.42),
    "SA-SB2": ("Ravelsby Brook upper", 16, 5.0, 7.0, 43.90, 44.86),
    "SA-LD1": ("Quarnell at Whinnerby", 36, 10.0, 12.0, 30.15, 32.88),
    "SA-LD2": ("Quarnell at Nettlecote", 38, 10.0, 12.0, 29.10, 31.79),
    "SA-LD3": ("Quarnell at Yarrowcote", 40, 10.0, 12.0, 28.05, 30.83),
    "SA-LD4": ("Quarnell at Burnishaw", 42, 10.0, 12.0, 27.00, 29.66),
    "SA-LD5": ("Quarnell at Hepplewick", 44, 10.0, 12.0, 26.10, 28.74),
    "SA-LD6": ("Quarnell at Quernby", 46, 10.0, 12.0, 25.05, 27.58),
    "SA-LD7": ("Quarnell at Tolmarsh", 48, 10.0, 12.0, 24.10, 26.71),
    "SA-LD8": ("Quarnell at Wrennick", 50, 10.0, 12.0, 23.15, 25.63),
    "SA-LD9": ("Quarnell at Hawkesbridge", 52, 10.0, 13.0, 22.20, 24.37),
}
# the 2023 run (superseded): same structure, peaks a little lower and a little earlier
SA23_SHIFT = {"lev": -0.11, "hr": -1}


def stage(sa, h, run=2025):
    _n, tp, wr, wf, base, peak = SA[sa]
    if run == 2023:
        tp, peak = tp + SA23_SHIFT["hr"], peak + SA23_SHIFT["lev"]
    w = wr if h <= tp else wf
    return base + (peak - base) * math.exp(-0.5 * ((h - tp) / (w / 1.6)) ** 2)


def peak_stage(sa, run=2025):
    return max(stage(sa, h, run) for h in HOURS)


# storage area polygons (local km): axis-aligned boxes are too regular, so each is a quadrilateral
SA_POLY = {
    "SA-HB1": [(6.2, 3.9), (7.9, 3.8), (8.1, 5.9), (6.0, 6.1)],
    "SA-HB2": [(6.0, 6.1), (8.1, 5.9), (8.6, 8.8), (6.3, 9.0)],
    "SA-SB1": [(14.1, 3.8), (15.9, 3.7), (16.2, 5.8), (13.9, 6.0)],
    "SA-SB2": [(13.9, 6.0), (16.2, 5.8), (16.5, 8.7), (14.2, 8.9)],
    "SA-MW1": [(22.1, 3.7), (23.9, 3.6), (24.2, 5.9), (21.9, 6.0)],
    "SA-LD1": [(0.0, -1.3), (4.4, -1.4), (4.6, 3.0), (0.0, 3.1)],
    "SA-LD2": [(4.4, -1.4), (8.2, -1.5), (8.3, 1.4), (4.6, 1.5)],
    "SA-LD3": [(8.2, -1.5), (12.3, -1.6), (12.4, 3.0), (8.3, 3.1)],
    "SA-LD4": [(12.3, -1.6), (16.4, -1.5), (16.5, 1.3), (12.4, 1.4)],
    "SA-LD5": [(16.4, -1.5), (20.3, -1.6), (20.4, 3.0), (16.5, 3.1)],
    "SA-LD6": [(20.3, -1.6), (24.6, -1.5), (24.7, 1.4), (20.4, 1.5)],
    "SA-LD7": [(24.6, -1.5), (28.4, -1.6), (28.5, 2.9), (24.7, 3.0)],
    "SA-LD8": [(28.4, -1.6), (30.9, -1.5), (31.0, 1.2), (28.5, 1.3)],
    "SA-LD9": [(30.9, -1.5), (32.0, -1.4), (32.1, 0.4), (31.0, 0.5)],
}


def in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def sa_at(x, y):
    for sa, poly in SA_POLY.items():
        if in_poly(x, y, poly):
            return sa
    return None


# ------------------------------------------------------------------------------------------------ network
# node -> (x, y, highways node reference)
NODES = {
    "H": (33.6, 1.6), "T": (32.2, 0.9), "TN": (32.6, 2.5), "TS": (32.7, -0.9), "TW": (31.5, 1.9),
    "B0": (0.4, 5.3), "Bx3": (3.0, 5.0), "Bw7": (6.4, 5.1), "V1": (7.0, 4.6), "Be7": (7.6, 5.0),
    "Bx11": (11.0, 5.2), "Bw15": (14.3, 5.0), "V2": (15.0, 4.5), "Be15": (15.7, 4.9), "Bx19": (19.0, 5.1),
    "Bw23": (22.4, 5.0), "V3": (23.0, 4.4), "Be23": (23.6, 4.8), "Bx27": (27.0, 4.9), "B30": (30.2, 4.0),
    "N1": (3.0, 2.2), "N2": (11.0, 2.4), "N3": (19.0, 2.3), "N4": (27.0, 2.1),
    "A0": (0.4, -0.5), "Ax3": (3.0, -0.6), "Ax5": (5.0, -0.7), "Aw10": (9.6, -0.6), "Ae10": (10.4, -0.6),
    "Ax11": (11.0, -0.6), "Ax13": (13.0, -0.7), "Aw18": (17.6, -0.6), "Ae18": (18.4, -0.6),
    "Ax19": (19.0, -0.6), "Ax21": (21.0, -0.7), "Aw26": (25.6, -0.6), "Ae26": (26.4, -0.6),
    "Ax27": (27.0, -0.6), "Wy": (27.9, -0.5), "Ax29": (29.0, -0.6), "Aw30": (29.8, -0.5), "A31": (31.1, -0.2),
    "S1": (5.0, -3.0), "S2": (13.0, -3.2), "S3": (21.0, -3.1), "S4": (29.0, -3.0),
    "M5": (5.0, -5.0), "M21": (21.0, -5.2), "M31": (31.0, -4.6), "M13": (13.4, -5.6),
    "UL": (0.6, 2.0), "HF": (9.6, 7.6), "CE": (26.2, 7.1), "FB": (17.2, -6.6), "HFj": (10.8, 5.3),
}

# link: (a, b, road number, road name, class, storage area of its lowest point or None, depth of that
# lowest point below the 2025 peak stage in metres (its surveyed level is peak - this))
LINKS = [
    ("H", "T", "A6124", "Infirmary Road", "A", None, 0), ("TN", "H", "U3010", "Moorgate", "U", None, 0),
    ("TW", "T", "U3014", "St Mary's Road", "U", None, 0), ("TS", "T", "A6123", "Bridge Street", "A", None, 0),
    ("B30", "T", "A6124", "Ridgeway Road", "A", None, 0), ("A31", "T", "A6123", "Quarnell Road", "A", None, 0),
    ("M31", "T", "C2050", "Moor Road", "C", None, 0), ("TW", "TN", "U3016", "Chapel Lane", "U", None, 0),
    ("B0", "Bx3", "B5131", "Ridge Road", "B", None, 0), ("Bx3", "Bw7", "B5131", "Ridge Road", "B", None, 0),
    ("Bw7", "V1", "B5131", "Ridge Road", "B", "SA-HB1", 0.92), ("V1", "Be7", "B5131", "Ridge Road", "B", "SA-HB1", 1.04),
    ("Be7", "Bx11", "B5131", "Ridge Road", "B", None, 0), ("Bx11", "HFj", "B5131", "Ridge Road", "B", None, 0),
    ("HFj", "Bw15", "B5131", "Ridge Road", "B", None, 0),
    ("Bw15", "V2", "B5131", "Ridge Road", "B", "SA-SB1", 0.81), ("V2", "Be15", "B5131", "Ridge Road", "B", "SA-SB1", 0.93),
    ("Be15", "Bx19", "B5131", "Ridge Road", "B", None, 0), ("Bx19", "Bw23", "B5131", "Ridge Road", "B", None, 0),
    ("Bw23", "V3", "B5131", "Ridge Road", "B", "SA-MW1", 0.88), ("V3", "Be23", "B5131", "Ridge Road", "B", "SA-MW1", 0.79),
    ("Be23", "Bx27", "B5131", "Ridge Road", "B", None, 0), ("Bx27", "B30", "A6124", "Ridgeway Road", "A", None, 0),
    ("N1", "Bx3", "C2041", "Whinnerby Lane", "C", None, 0), ("N1", "Ax3", "C2041", "Whinnerby Bridge", "C", "SA-LD1", 1.02),
    ("N2", "Bx11", "C2043", "Yarrowcote Road", "C", None, 0), ("N2", "Ax11", "C2043", "Yarrowcote Bridge", "C", "SA-LD3", 0.98),
    ("N3", "Bx19", "C2045", "Hepplewick Road", "C", None, 0), ("N3", "Ax19", "C2045", "Hepplewick Bridge", "C", "SA-LD5", 1.01),
    ("N4", "Bx27", "C2047", "Tolmarsh Lane", "C", None, 0), ("N4", "Ax27", "C2047", "Tolmarsh Bridge", "C", "SA-LD7", 0.97),
    ("A0", "Ax3", "A6123", "Quarnell Road", "A", None, 0), ("Ax3", "Ax5", "A6123", "Quarnell Road", "A", "SA-LD2", -0.14),
    ("Ax5", "Aw10", "A6123", "Quarnell Road", "A", None, 0), ("Aw10", "Ae10", "A6123", "Quarnell Road", "A", "SA-LD3", 0.91),
    ("Ae10", "Ax11", "A6123", "Quarnell Road", "A", None, 0), ("Ax11", "Ax13", "A6123", "Quarnell Road", "A", None, 0),
    ("Ax13", "Aw18", "A6123", "Quarnell Road", "A", None, 0), ("Aw18", "Ae18", "A6123", "Quarnell Road", "A", "SA-LD5", 0.89),
    ("Ae18", "Ax19", "A6123", "Quarnell Road", "A", None, 0), ("Ax19", "Ax21", "A6123", "Quarnell Road", "A", None, 0),
    ("Ax21", "Aw26", "A6123", "Quarnell Road", "A", None, 0), ("Aw26", "Ae26", "A6123", "Quarnell Road", "A", "SA-LD7", 0.94),
    ("Ae26", "Ax27", "A6123", "Quarnell Road", "A", None, 0), ("Ax27", "Wy", "A6123", "Quarnell Road", "A", None, 0),
    ("Wy", "Ax29", "A6123", "Quarnell Road", "A", None, 0), ("Ax29", "Aw30", "A6123", "Quarnell Road", "A", None, 0),
    ("Aw30", "A31", "A6123", "Quarnell Road", "A", "SA-LD8", 0.90),
    ("S1", "Ax5", "C2052", "Nettle Gill Lane", "C", None, 0), ("S1", "M5", "U4105", "Nettlecote Lane", "U", None, 0),
    ("M5", "M13", "C2050", "Moor Road", "C", None, 0), ("M13", "M21", "C2050", "Moor Road", "C", None, 0),
    ("M21", "M31", "C2050", "Moor Road", "C", None, 0), ("FB", "M13", "U4112", "Kestlebeck Lane", "U", None, 0),
    ("S2", "Ax13", "C2054", "Burnishaw Lane", "C", None, 0), ("S3", "Ax21", "C2056", "Quernby Lane", "C", None, 0),
    ("S3", "M21", "U4118", "Quernby Moor Road", "U", None, 0), ("S4", "Ax29", "C2058", "Wrennick Lane", "C", None, 0),
    ("UL", "A0", "U4101", "Upper Quarnell Lane", "U", None, 0), ("UL", "B0", "U4102", "Quarnell Head Road", "U", None, 0),
    ("HF", "HFj", "U4108", "Highfold Road", "U", None, 0), ("CE", "Bx27", "U4122", "Owlthwaite Road", "U", None, 0),
    # wet but passable at the peak (shallow water on the carriageway)
    ("Ax21", "Ax19x", "U4115", "Mill Lane", "U", "SA-LD6", -0.13), ("Be23", "CEx", "U4124", "Scar Lane", "U", "SA-MW1", -0.19),
]
NODES["Ax19x"] = (20.0, 0.6)
NODES["CEx"] = (23.3, 5.6)

# parishes: code, name, main village node, council tax dwellings (October 2026)
PARISHES = [
    ("E04014101", "Hollinside", "V1", 312), ("E04014102", "Ravelsby Bridge", "V2", 247),
    ("E04014103", "Lunnerby", "V3", 486), ("E04014104", "Whinnerby", "N1", 1138),
    ("E04014105", "Yarrowcote", "N2", 864), ("E04014106", "Hepplewick", "N3", 652),
    ("E04014107", "Tolmarsh", "N4", 931), ("E04014108", "Nettlecote", "S1", 1456),
    ("E04014109", "Burnishaw", "S2", 593), ("E04014110", "Quernby Moor", "S3", 778),
    ("E04014111", "Wrennick", "S4", 281), ("E04014112", "Cottergill", "Wy", 174),
    ("E04014113", "Highfold", "HF", 219), ("E04014114", "Owlthwaite", "CE", 163),
    ("E04014115", "Kestlebeck", "FB", 342), ("E04014116", "Upper Quarnell", "UL", 403),
    ("E04014117", "Hawkesbridge North", "TN", 9174), ("E04014118", "Hawkesbridge South", "TS", 7383),
]
PARISH_NODE = {p[1]: p[2] for p in PARISHES}
# Hawkesbridge West merged into Hawkesbridge North on 1 April 2025 (address register keeps some old codes)
OLD_PARISH = ("E04014119", "Hawkesbridge West")
HOSPITAL = "H"


def link_peak_level(link, run=2025):
    """surveyed level of the link's lowest point (mAOD)."""
    a, b, rn, name, cls, sa, d = link
    if sa is None:
        return None
    return round(peak_stage(sa, 2025) - d - DEPTH_LIMIT, 2)


def link_impassable(link, h, run=2025, limit=DEPTH_LIMIT):
    a, b, rn, name, cls, sa, d = link
    if sa is None:
        return False
    return stage(sa, h, run) - link_peak_level(link) > limit + 1e-9


def reach(open_links):
    adj = {}
    for l in open_links:
        adj.setdefault(l[0], set()).add(l[1])
        adj.setdefault(l[1], set()).add(l[0])
    seen, stack = {HOSPITAL}, [HOSPITAL]
    while stack:
        n = stack.pop()
        for m in adj.get(n, ()):
            if m not in seen:
                seen.add(m)
                stack.append(m)
    return seen


def cut_off_hours(run=2025, limit=DEPTH_LIMIT):
    out = {}
    for h in HOURS:
        r = reach([l for l in LINKS if not link_impassable(l, h, run, limit)])
        for code, name, node, _dw in PARISHES:
            if node not in r:
                out.setdefault(name, []).append(h)
    return out


def golden_set(run=2025):
    return sorted(cut_off_hours(run).keys(), key=lambda n: [p[1] for p in PARISHES].index(n))


def envelope_set(limit=DEPTH_LIMIT, run=2025):
    closed = []
    for l in LINKS:
        if l[5] is None:
            continue
        if any(link_impassable(l, h, run, limit) for h in HOURS):
            closed.append(l)
    r = reach([l for l in LINKS if l not in closed])
    return [p[1] for p in PARISHES if p[2] not in r]


def worst_hour(run=2025):
    counts = {h: sum(link_impassable(l, h, run) for l in LINKS) for h in HOURS}
    return max(HOURS, key=lambda h: (counts[h], -h))


def set_at_hour(h, run=2025):
    r = reach([l for l in LINKS if not link_impassable(l, h, run)])
    return [p[1] for p in PARISHES if p[2] not in r]


def dwellings(names):
    d = {p[1]: p[3] for p in PARISHES}
    return sum(d[n] for n in names)


BUDGET, BASE_GRANT = 30000, 3000


def grants(names):
    """the 2027 budget: a base grant to each qualifying parish, the rest shared in proportion to households, in whole
    pounds (guidance section 3)."""
    d = {p[1]: p[3] for p in PARISHES}
    rest = BUDGET - BASE_GRANT * len(names)
    tot = sum(d[n] for n in names)
    return {n: int(round(BASE_GRANT + rest * d[n] / tot)) for n in names}, rest / tot


if __name__ == "__main__":
    print("golden", golden_set(), dwellings(golden_set()))
    print("envelope 0.25", envelope_set(), dwellings(envelope_set()))
    print("envelope any water", envelope_set(limit=0.0))
    wh = worst_hour()
    print("worst hour", wh, set_at_hour(wh))
    print("2023 run golden", golden_set(2023), "envelope", envelope_set(run=2023))
    for n, hs in cut_off_hours().items():
        print(n, min(hs), max(hs), len(hs))
