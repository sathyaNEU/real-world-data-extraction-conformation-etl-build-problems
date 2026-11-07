"""Clean-truth prototype v2: two mountain crossings that look alike, one exposed.

P1 exposed plateau (shorter, lower climb) and P2 sheltered pass (longer, higher) both sit between
existing chargers; package A infills a lowland gap, B puts a site on P1, C on P2. Prices every
route a solver could take and prints the trips each package makes completable in 2027.
"""

MONTHS = list(range(1, 13))
VALLEY_T = {1: -7, 2: -6, 3: -2, 4: 3, 5: 8, 6: 12, 7: 14, 8: 13, 9: 8, 10: 3, 11: -2, 12: -6}
# fleet: (name, usable kWh, base kWh/km mild flat at 80 km/h, share)
MODELS = [
    ("M1", 50, 0.160, 0.08), ("M2", 57, 0.168, 0.11), ("M3", 62, 0.172, 0.13),
    ("M4", 70, 0.178, 0.14), ("M5", 75, 0.182, 0.14), ("M6", 79, 0.195, 0.12),
    ("M7", 72, 0.188, 0.10), ("M8", 92, 0.210, 0.08), ("M9", 98, 0.205, 0.06),
    ("M10", 59, 0.158, 0.04),
]
SH = sum(m[3] for m in MODELS)

def tf(t):
    return 1.0 + 0.015 * max(0.0, 15 - t)

# stretch: km, climb W-bound, climb E-bound, summit metres above the valley, exposed flag
STRETCH = {
    "P1": dict(km=112, climb=620, desc=560, rise=650, exposed=True),
    "P2": dict(km=150, climb=880, desc=820, rise=900, exposed=False),
    "L":  dict(km=196, climb=120, desc=120, rise=60, exposed=False),
}
SPLIT = {"A": ("L", 0.5), "B": ("P1", 0.5), "C": ("P2", 0.5)}

# trips 2027 needing each stretch (both directions) and month profile
TRIPS = {"P1": 3000, "P2": 1600, "L": 1500}
PROF = {
    "P1": {1: .9, 2: 1.4, 3: 1.4, 4: 1.1, 5: .6, 6: .8, 7: 1.3, 8: 1.0, 9: .6, 10: .5, 11: .5, 12: 1.0},
    "P2": {1: .7, 2: .9, 3: 1.0, 4: .9, 5: .8, 6: 1.1, 7: 1.5, 8: 1.3, 9: 1.0, 10: .8, 11: .6, 12: .8},
    "L":  {1: .8, 2: .8, 3: .9, 4: 1.0, 5: 1.0, 6: 1.2, 7: 1.4, 8: 1.2, 9: 1.0, 10: .9, 11: .8, 12: 1.0},
}

def exposed_mult(month):
    # wind, drifting snow and the plateau's own cold, beyond what the valley stations show
    return {12: 1.55, 1: 1.6, 2: 1.55, 3: 1.35, 11: 1.25, 4: 1.1}.get(month, 1.0)

def e_true(model, km, climb, desc, rise, exposed, m):
    t = VALLEY_T[m] - 0.0065 * rise * (1 if exposed else 0.6)
    e = km * model[2] * tf(t) + 0.0027 * climb - 0.0017 * desc
    if exposed:
        e *= exposed_mult(m)
    return e

def legs(stretch, pkg):
    s = STRETCH[stretch]
    if pkg and SPLIT[pkg][0] == stretch:
        f = SPLIT[pkg][1]
        # summit site: each half climbs or descends most of the rise
        return [dict(km=s["km"] * f, climb=s["climb"] * 0.8, desc=s["desc"] * 0.2, rise=s["rise"], exposed=s["exposed"]),
                dict(km=s["km"] * (1 - f), climb=s["climb"] * 0.2, desc=s["desc"] * 0.8, rise=s["rise"], exposed=s["exposed"])]
    return [s]

def ok(model, e):
    return e <= model[1] * 0.70  # charge to 80, arrive at 10

def completable(stretch, pkg, fn):
    tot = 0.0
    for m in MONTHS:
        tr = TRIPS[stretch] * PROF[stretch][m] / sum(PROF[stretch].values())
        for d in (0, 1):
            share = 0.0
            for mod in MODELS:
                good = True
                for lg in legs(stretch, pkg):
                    cl, de = (lg["climb"], lg["desc"]) if d == 0 else (lg["desc"], lg["climb"])
                    if not ok(mod, fn(mod, lg["km"], cl, de, lg["rise"], lg["exposed"], m)):
                        good = False
                        break
                if good:
                    share += mod[3] / SH
            tot += tr / 2 * share
    return tot

def gains(fn):
    return {p: completable(SPLIT[p][0], p, fn) - completable(SPLIT[p][0], None, fn) for p in SPLIT}

def show(name, fn):
    g = gains(fn)
    order = sorted(g, key=g.get, reverse=True)
    print(f"{name:44s} A {g['A']:6.0f}  B {g['B']:6.0f}  C {g['C']:6.0f}  -> {order[0]} ({g[order[0]]/max(g[order[1]],1):.2f}x)")

def r_rated(mod, km, cl, de, rise, ex, m):
    return km * mod[2] * 1.06
def r_derate(mod, km, cl, de, rise, ex, m):
    return km * mod[2] * (1.30 if m in (11, 12, 1, 2, 3) else 1.06)
def r_valley_phys(mod, km, cl, de, rise, ex, m):
    return km * mod[2] * tf(VALLEY_T[m]) + 0.0027 * cl - 0.0017 * de
def r_lapse_phys(mod, km, cl, de, rise, ex, m):
    return km * mod[2] * tf(VALLEY_T[m] - 0.0065 * rise) + 0.0027 * cl - 0.0017 * de
def r_mountain_derate(mod, km, cl, de, rise, ex, m):
    f = tf(VALLEY_T[m])
    if rise > 300 and m in (11, 12, 1, 2, 3):
        f *= 1.25
    return km * mod[2] * f + 0.0027 * cl - 0.0017 * de
# pooled measured by month: the network-wide kWh per km each month (plateau km a small share)
def r_pooled_month(mod, km, cl, de, rise, ex, m):
    share_exposed_km = 0.06
    f = tf(VALLEY_T[m]) * (1 + share_exposed_km * (exposed_mult(m) - 1))
    return km * mod[2] * f * 1.02
def r_truth(mod, km, cl, de, rise, ex, m):
    return e_true(mod, km, cl, de, rise, ex, m)

for nm, fn in [("rated", r_rated), ("uniform winter derate", r_derate),
               ("physics, valley temperature", r_valley_phys), ("physics, lapse-rate temperature", r_lapse_phys),
               ("mountain derate on high stretches", r_mountain_derate), ("pooled measured by month", r_pooled_month),
               ("stretch by month measured (truth)", r_truth)]:
    show(nm, fn)

# arrival signal: winter energy per crossing (kWh) for a mid model, both crossings
mid = MODELS[4]
for s in ("P1", "P2"):
    st = STRETCH[s]
    print(s, "Jan crossing kWh mid model:", round(e_true(mid, st["km"], st["climb"], st["desc"], st["rise"], st["exposed"], 1), 1),
          "per km:", round(e_true(mid, st["km"], st["climb"], st["desc"], st["rise"], st["exposed"], 1) / st["km"], 3))
