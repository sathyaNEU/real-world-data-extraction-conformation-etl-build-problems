"""The region and its people: output areas with households and spend, the chain's stores, the competitors, the
six sites and the holiday parks; the spend-share model's shares; the true trade of every store."""
import math

import numpy as np

import params as P


def build(seed=P.SEED):
    rs = np.random.default_rng(seed)
    oas = []
    for name, x, y, n, hh, nsec in P.TOWNS:
        for i in range(n):
            r = abs(rs.normal(0, 1.4 if n > 15 else 1.0))
            a = rs.uniform(0, 2 * math.pi)
            h = max(40, int(rs.normal(hh, 18)))
            oas.append(dict(town=name, x=x + r * math.cos(a), y=y + r * math.sin(a), hh=h, sec=i % nsec))
    for i in range(P.N_VILL):
        oas.append(dict(town="", x=rs.uniform(0, 72), y=rs.uniform(0, 46), hh=max(30, int(rs.normal(95, 25))),
                        sec=None))
    for o in oas:
        o["spend"] = round(max(55.0, rs.normal(96, 14)), 2)
        o["res"] = int(round(o["hh"] * rs.uniform(2.05, 2.5)))
    return rs, oas


def stores_now():
    s = [dict(id=i, kind="own", town=t, x=x, y=y, area=a) for i, t, x, y, a, _ in P.OWN]
    s += [dict(id="C%02d" % k, kind="comp", fascia=f, town=t, x=x, y=y, area=a) for k, (f, t, x, y, a) in
          enumerate(P.COMP)]
    return s


def site_store(site):
    sid, addr, town, x, y, a, _ = site
    return dict(id=sid, kind="own", town=town, x=x, y=y, area=a)


def shares(px, py, stores):
    X = np.array([s["x"] for s in stores]); Y = np.array([s["y"] for s in stores])
    A = np.array([s["area"] for s in stores], float) ** P.ALPHA
    w = A * np.exp(-P.BETA * P.ROADF * np.hypot(X - px, Y - py))
    return w / w.sum()


def resident_spend(o):
    return o["hh"] * o["spend"] * 52 * P.INSTORE


def flows(oas, stores, parks=True):
    """resident and guest in-store spend each store wins in a year"""
    res = np.zeros(len(stores)); vis = np.zeros(len(stores))
    for o in oas:
        res += resident_spend(o) * shares(o["x"], o["y"], stores)
    if parks:
        for name, x, y, n, _ in P.PARKS:
            vis += n * P.V_PITCH * shares(x, y, stores)
    return res, vis


def appraise(oas, with_parks=True, stores=None):
    """each site's addition to the chain's contribution: 26 per cent of its sales less 26 per cent of what it takes
    from the ten stores, less its running costs"""
    st = stores or stores_now()
    own = [k for k, s in enumerate(st) if s["kind"] == "own"]
    r0, v0 = flows(oas, st, with_parks)
    out = {}
    for site in P.SITES:
        s2 = st + [site_store(site)]
        r1, v1 = flows(oas, s2, with_parks)
        new = r1[-1] + v1[-1]
        took = sum((r0[k] + v0[k]) - (r1[k] + v1[k]) for k in own)
        cost = sum(site[6])
        out[site[0]] = dict(new=new, took=took, cost=cost, add=P.MARGIN * (new - took) - cost,
                            new_res=r1[-1], new_vis=v1[-1])
    return out


def truth():
    rs, oas = build()
    st = stores_now()
    r0, v0 = flows(oas, st)
    ers = np.random.default_rng(P.SEED + 1000)
    eps = {s["id"]: float(ers.normal(0, 0.045)) for s in st if s["kind"] == "own"}
    card = {s["id"]: round(float(ers.uniform(0.93, 0.96)), 3) for s in st if s["kind"] == "own"}
    capture = {s["id"]: float(ers.normal(0, 0.03)) for s in st if s["kind"] == "own"}
    own = [k for k, s in enumerate(st) if s["kind"] == "own"]
    sales = {st[k]["id"]: r0[k] * (1 + eps[st[k]["id"]]) * (1 + P.VFR) + v0[k] for k in own}
    return dict(oas=oas, stores=st, res=r0, vis=v0, eps=eps, card=card, sales=sales, capture=capture,
                golden=appraise(oas, True), resident=appraise(oas, False))
