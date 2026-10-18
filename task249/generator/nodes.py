"""The 36 nodes: sites, installation, model, moves, and each head's span and zero at the window."""
import datetime as dt
import numpy as np
import params as P

TOWNS = [  # municipality, analyser it sits around (index) or None, number of nodes
    ("Alcorna", 0, 6), ("Alcorna", 1, 4), ("Torralba del Campo", 2, 5), ("Villarejo de Mencia", 3, 5),
]
VILLAGES = ["Navalcuerno", "Valdeolmos del Llano", "Hontanar de la Vega", "Fresnedilla del Campo",
            "Villanueva de Alcorna", "Santa Cruz de Alcorna", "Campillo de Mencia", "Quintanar de Alcorna"]
SITE_TYPES = ["school roof", "town hall roof", "health centre roof", "sports hall roof", "library roof"]


def layout():
    """[(code, municipality, x, y)] for the 36 nodes as installed."""
    r = np.random.default_rng(21)
    an = [(a[2], a[3]) for a in P.ANALYSERS]
    out = []
    for town, k, n in TOWNS:
        for _ in range(n):
            while True:
                a, rad = r.uniform(0, 2 * np.pi), r.uniform(1.5, 7.0)
                x, y = an[k][0] + rad * np.cos(a), an[k][1] + rad * np.sin(a)
                if min(np.hypot(x - bx, y - by) for bx, by in an) > 1.2:
                    break
            out.append((town, round(x, 2), round(y, 2)))
    centres = [(-24, 10), (-8, 19), (10, 21), (27, -4), (12, -16), (-6, -24), (-27, -22), (24, 19)]
    for v, (cx, cy) in zip(VILLAGES, centres):
        for _ in range(2):
            while True:
                x, y = cx + r.uniform(-3, 3), cy + r.uniform(-3, 3)
                if 9 <= min(np.hypot(x - bx, y - by) for bx, by in an) <= 26:
                    break
            out.append((v, round(x, 2), round(y, 2)))
    return [("OZ%02d" % (i + 1), m, x, y) for i, (m, x, y) in enumerate(out)]


NODES = layout()
HILL = {"Navalcuerno": 0.72, "Santa Cruz de Alcorna": 0.68, "Campillo de Mencia": 0.75, "Quintanar de Alcorna": 0.70}
ALT = {"Alcorna": 702, "Torralba del Campo": 688, "Villarejo de Mencia": 731, "Valdeolmos del Llano": 694,
       "Hontanar de la Vega": 676, "Fresnedilla del Campo": 712, "Villanueva de Alcorna": 705,
       "Navalcuerno": 948, "Santa Cruz de Alcorna": 905, "Campillo de Mencia": 962, "Quintanar de Alcorna": 921}
CODES = [c for c, _, _, _ in NODES]
MODEL_B = {"OZ03", "OZ08", "OZ12", "OZ15", "OZ19", "OZ22", "OZ24", "OZ27", "OZ29", "OZ31", "OZ33", "OZ35"}  # half-hourly
# two nodes moved at the March cleaning round to a better roof in the same municipality: (new x, new y, date)
MOVES = {"OZ14": (21.4, 6.1, dt.date(2028, 3, 15)), "OZ30": (11.8, -15.2, dt.date(2028, 3, 16))}


REPLACED = ("OZ19", dt.datetime(2028, 1, 6, 14), dt.datetime(2028, 1, 9, 11), dt.datetime(2028, 1, 25, 10))
# OZ19's unit failed (local time), a spare (hourly, firmware 4.2) went up, reporting as OZ19B until the register moved
SPARE_ID = "OZ19B"
# firmware 4.2 rollout, local dates: status 1 changed from warm-up (rejected) to humidity-compensated (accepted)
FW_DATES = {}
_fw = np.random.default_rng(612)
for _i, _c in enumerate(["OZ%02d" % (k + 1) for k in range(36)]):
    # the contractor took the update round by round: the towns first, then the villages, a few nodes a day
    _base = 0 if _i < 10 else (2 if _i < 20 else 4)
    FW_DATES[_c] = dt.date(2028, 1, 10) + dt.timedelta(days=int(_base + _fw.integers(0, 4 if _i < 20 else 6)))


_INST = np.random.default_rng(613).integers(0, 30, 36)


def install_date(i):
    # installed after its bench week; the bench took up to eight nodes a week from 12 September
    return dt.date(2027, 9, 20) + dt.timedelta(days=int(sorted(_INST)[i] + (i // 8)))


# each head's span and zero (ppb) at the middle of the window, set by the design (tuned on the realised field)
_TOWN = [1.02, 0.99, 0.95, 0.98, 0.99, None, 1.01, 0.97, 1.03, 1.03, 0.97, 0.98, 0.98, 1.02, 0.99, 0.99, None, 1.01, 0.97, 1.03]
SPAN = {"OZ%02d" % (i + 1): s for i, s in enumerate(_TOWN) if s is not None}
SPAN.update({"OZ06": 0.74, "OZ17": 0.77, "OZ25": 0.75, "OZ32": 0.78, "OZ21": 0.72,       # drifted low
             "OZ34": 1.27, "OZ29": 1.23, "OZ33": 1.25,                                     # drifted high, far out
             "OZ22": 0.99, "OZ24": 1.03, "OZ26": 0.95, "OZ28": 0.99, "OZ31": 1.00, "OZ35": 1.02,
             "OZ36": 1.00, "OZ27": 0.98, "OZ23": 1.00, "OZ30": 0.98})
_z = __import__("numpy").random.default_rng(31).normal(0, 1.5, 36)
ZERO = {"OZ%02d" % (i + 1): round(float(_z[i]), 2) for i in range(36)}
ZERO.update({"OZ25": 6.0, "OZ21": 5.5, "OZ34": -5.0, "OZ09": -5.5, "OZ13": -5.5})
