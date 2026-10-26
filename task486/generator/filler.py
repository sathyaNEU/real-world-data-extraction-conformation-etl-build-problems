"""The rest of Torvasay, which the call never reads but the pack must hold as the island's own records: employers
outside retail with their premises (cafes, restaurants, pubs, hotels, banks, garages, workshops, factories,
surgeries, schools, halls, care homes) or with none, traders with no employees, the landlords who own premises and
stand liable for them while they are empty, and the shop units the centres hold beyond the retail world. Nothing here
enters a retail employer's placement or a calibration pool (every premises is in a description outside retail or is
occupied by no employer), so the retail world's plan and tune stand."""
import numpy as np

import world as W

# sector: SIC 2007 subclass, description of its premises (None: works from no rated premises), share of the
# sector's employers that are multi-site, employer count, size of an employer with no premises (median, log sd)
SECTORS = [
    ("56101", "F1", 0.04, 520, None), ("56102", "F2", 0.05, 640, None), ("56103", "F2", 0.06, 330, None),
    ("56302", "F3", 0.10, 430, None), ("55100", "F4", 0.05, 140, None), ("64191", "B1", 1.0, 4, None),
    ("64192", "B1", 1.0, 2, None), ("45200", "M1", 0.03, 560, None), ("46710", "M2", 1.0, 3, None),
    ("10710", "W2", 0.0, 60, None), ("10890", "W2", 0.0, 90, None), ("16100", "W2", 0.0, 40, None),
    ("25110", "W2", 0.0, 120, None), ("25620", "W2", 0.0, 150, None), ("28990", "W2", 0.0, 70, None),
    ("33120", "W3", 0.0, 420, None), ("43320", "W3", 0.0, 380, None), ("74100", "W3", 0.0, 160, None),
    ("86210", "S1", 0.1, 42, None), ("86230", "S1", 0.08, 70, None), ("87300", "S5", 0.12, 95, None),
    ("93130", "S4", 0.1, 48, None), ("93110", "S4", 0.0, 30, None), ("94910", "S3", 0.0, 210, None),
    ("41201", None, 0.0, 520, (6, 0.9)), ("41202", None, 0.0, 780, (4, 0.8)), ("43210", None, 0.0, 950, (3, 0.7)),
    ("43220", None, 0.0, 1100, (3, 0.7)), ("43341", None, 0.0, 700, (2, 0.6)), ("43390", None, 0.0, 600, (2, 0.6)),
    ("49410", None, 0.0, 420, (5, 0.9)), ("49320", None, 0.0, 380, (2, 0.6)), ("62012", None, 0.0, 900, (2, 0.8)),
    ("62020", None, 0.0, 760, (2, 0.8)), ("66220", None, 0.0, 240, (3, 0.7)), ("70229", None, 0.0, 1300, (1.6, 0.7)),
    ("71111", None, 0.0, 300, (3, 0.7)), ("71129", None, 0.0, 450, (3, 0.8)), ("78200", None, 0.0, 120, (6, 1.0)),
    ("80100", None, 0.0, 90, (8, 1.0)), ("81210", None, 0.0, 520, (4, 0.9)), ("82990", None, 0.0, 800, (2, 0.8)),
    ("88100", None, 0.0, 380, (9, 0.9)), ("88990", None, 0.0, 300, (3, 0.9)), ("96090", None, 0.0, 600, (1.5, 0.6)),
    ("01110", None, 0.0, 700, (2, 0.7)), ("69102", None, 0.0, 260, (5, 0.8)), ("69201", None, 0.0, 330, (4, 0.8)),
    ("69202", None, 0.0, 280, (2, 0.6)), ("68310", None, 0.0, 120, (3, 0.6)), ("85200", None, 0.0, 40, (12, 0.6)),
]
PUBLIC = [  # the island's public employers, one scheme each, with premises across the island
    ("84110", "Torvasay Government", [("S3", 40), ("S4", 6)], 6800),
    ("85310", "Torvasay Education Service", [("S2", 74)], 4200),
    ("86101", "Torvasay Health Service", [("S1", 22), ("S5", 9)], 5600),
]
LOC_FOR = {"F1": "centre", "F2": "centre", "F3": "mixed", "F4": "mixed", "B1": "centre", "M1": "ind", "M2": "road",
           "W2": "ind", "W3": "ind", "S1": "mixed", "S2": "village", "S3": "mixed", "S4": "village", "S5": "village"}


def add(w, seed=W.SEED + 1):
    """the island beyond the retail world; a separate stream so the retail world is the same whatever is added here"""
    rng = np.random.default_rng(seed)
    NC = w.NC
    size = w.size
    psize = size / size.sum()
    w.filler_premises = []

    def area(d, med=None):
        return float(np.exp(np.log(med or W.DESC[d][5]) + W.DESC[d][6] * rng.standard_normal()))

    def rv(d, centre, a):
        if d in ("F1", "F2", "B1"):
            base = (w.zone[centre] if centre is not None else 110.0) * dict(F1=0.9, F2=0.95, B1=1.1)[d]
        elif d == "R1":
            base = w.zone[centre] if centre is not None else 120.0
        elif d == "O1":
            base = 205.0 if centre == 0 else 140.0
        else:
            base = W.DESC[d][3]
        r17 = a * base * float(np.exp(0.12 * rng.standard_normal()))
        return r17, r17 * W.DESC[d][4] * float(np.exp(0.05 * rng.standard_normal()))

    def staff(d, a):
        return max(1, int(round(a / 100 * W.DESC[d][2] * np.exp(0.25 * rng.standard_normal()))))

    def where(d):
        z = LOC_FOR.get(d, "mixed")
        if z == "centre" or (z == "mixed" and rng.random() < 0.45):
            c = int(rng.choice(NC, p=psize))
            return c, "centre"
        return None, ("ind" if z == "ind" else ("village" if z in ("village", "mixed") else "road"))

    def prem(d, e22, e26, centre, zone, a=None, s22=None, s26=None):
        a = area(d) if a is None else a
        r17, r23 = rv(d, centre, a)
        s = staff(d, a)
        p = dict(pid=len(w.P), centre=centre, zone=zone, d=d, a=a, rv17=r17, rv23=r23, built=True, o22=e22, o26=e26,
                 s22=(s if s22 is None else s22) if e22 is not None else 0,
                 s26=(max(1, int(round(s * np.exp(0.05 * rng.standard_normal())))) if s26 is None else s26)
                 if e26 is not None else 0, filler=True)
        w.P.append(p)
        w.filler_premises.append(p)
        return p

    # employers outside retail with premises outside the retail descriptions, and those with none
    for sic, d, multi, n, nosize in SECTORS:
        for _ in range(int(round(n * (1.12 if d is None else 1.0) * rng.uniform(0.92, 1.08)))):
            live22, live26 = rng.random() > 0.09, rng.random() > 0.08
            if not (live22 or live26):
                live22 = True
            e = w.emp("nonretail", None, sic=sic, filler=True, live22=live22, live26=live26)
            if d is None:
                s = max(1, int(round(np.exp(np.log(nosize[0]) + nosize[1] * rng.standard_normal()))))
                w.E[e]["own_staff"] = (s if live22 else 0, max(1, int(round(s * np.exp(0.12 * rng.standard_normal())))) if live26 else 0)
                continue
            k = int(rng.integers(2, 9)) if rng.random() < multi else 1
            for _ in range(k):
                c, z = where(d)
                prem(d, e if live22 else None, e if live26 else None, c, z)
    nil_sics = ["41202", "43341", "56103", "70229", "82990", "96090", "01110", "49320", "62020", "68310", "93110"]
    for _ in range(2900):
        sic = nil_sics[int(rng.integers(0, len(nil_sics)))]
        a, b = rng.random() < 0.62, rng.random() < 0.62
        if not (a or b):
            a = True
        s = max(1, int(round(np.exp(np.log(2) + 0.6 * rng.standard_normal()))))
        e = w.emp("nonretail", None, sic=sic, filler=True, live22=True, live26=True, nil22=a, nil26=b)
        w.E[e]["own_staff"] = (0 if a else s, 0 if b else max(1, int(round(s * np.exp(0.1 * rng.standard_normal())))))
    for sic, name, estate, total in PUBLIC:
        e = w.emp("nonretail", None, sic=sic, filler=True, public=name, live22=True, live26=True)
        ps = []
        for d, n in estate:
            for _ in range(n):
                c, z = where(d)
                ps.append(prem(d, e, e, c, z))
        # the public employers' offices: the island's government buildings, one in each district town
        for c in range(0, 6):
            ps.append(prem("O1", e, e, c, "centre", a=area("O1", 2400)))
        placed = sum(p["s22"] for p in ps)
        w.E[e]["own_staff"] = (max(0, total - placed), max(0, int(total * rng.uniform(1.0, 1.06)) - sum(p["s26"] for p in ps)))
    # traders with no employees: shop units in the centres and on the parades, workshops, small offices
    w.nonemp = []
    for k in range(NC):
        for _ in range(int(round(size[k] * 0.12))):
            t = len(w.nonemp)
            w.nonemp.append(dict(tid=t, kind="trader"))
            prem("R1", None, None, k, "centre", a=area("R1", 52)).update(n22=t, n26=t)
    for _ in range(420):
        t = len(w.nonemp)
        w.nonemp.append(dict(tid=t, kind="trader"))
        prem("R1", None, None, None, "parade", a=area("R1", 60)).update(n22=t, n26=t)
    for d, n, med in [("W3", 1500, 120), ("O1", 900, 60)]:
        for _ in range(n):
            t = len(w.nonemp)
            w.nonemp.append(dict(tid=t, kind="trader"))
            p = prem(d, None, None, None, "ind" if d == "W3" else "biz", a=area(d, med))
            p.update(n22=t if rng.random() > 0.05 else None, n26=t if rng.random() > 0.06 else None)
    # the centres' shop units held by no employer at a March: the retail world's empties and the units its
    # employers left, each either empty or taken by a trader with no employees
    for p in w.P:
        if p["d"] != "R1" or p.get("filler"):
            continue
        for yr in ("22", "26"):
            if p["o" + yr] is None and p.get("n" + yr) is None:
                if rng.random() < 0.36:
                    t = len(w.nonemp)
                    w.nonemp.append(dict(tid=t, kind="trader"))
                    p["n" + yr] = t
                else:
                    p["n" + yr] = None
    # vacant units held empty in both Marches, small kiosks among them
    for k in range(NC):
        for _ in range(int(round(size[k] * 0.05))):
            prem("R1", None, None, k, "centre", a=area("R1", 90)).update(n22=None, n26=None)
        for _ in range(int(round(size[k] * 0.025))):
            prem("R1", None, None, k, "centre", a=area("R1", 42)).update(n22=None, n26=None)
    for d, n in [("O1", 380), ("W3", 300), ("W2", 90), ("F2", 60), ("F3", 40)]:
        for _ in range(n):
            c, z = where(d) if d not in ("O1", "W3") else (None, "biz" if d == "O1" else "ind")
            prem(d, None, None, c, z).update(n22=None, n26=None)
    return w
