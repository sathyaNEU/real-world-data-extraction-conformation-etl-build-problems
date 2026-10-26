"""Torvasay's retail world in March 2022 and March 2026: the 31 designated town centres, the premises retail employers
occupy (by valuation list description, floor area and rateable value), the employers, and the staff each occupied
premises holds in each March. The chains carry the decisive structure: between the Marches some open retail park units
and distribution warehouses and close small town centre shops, and a premises' staff follow its floor area times its
description's density. The independents set each centre's level, and the planner sets their closures and openings so
every golden-family member and the truth clear the 8 per cent line and each rung crosses it where the chains allow.

Everything shipped is cut from this world (filler.py adds the rest of the island, timeline.py the accounts, lists,
PAYE schemes and companies); the golden is computed from the cut pack, never from here."""
import datetime as dt

import numpy as np

import names as N

SEED = 486
TH = -0.08
M22, M26 = dt.date(2022, 3, 31), dt.date(2026, 3, 31)
# description code: text, measurement basis, staff per 100 m2, rateable value per m2 in the 2017 list (None: by
# place), factor to the 2023 list, area median (m2), area log sd
DESC = {
    "R1": ("Shop and premises", "NIA", 6.2, None, 0.90, 112, 0.5),
    "R2": ("Department store and premises", "GIA", 2.7, 105, 0.82, 6800, 0.3),
    "R3": ("Supermarket and premises", "GIA", 4.3, 158, 0.97, 2100, 0.55),
    "R4": ("Retail warehouse and premises", "GIA", 1.4, 118, 0.93, 2200, 0.4),
    "O1": ("Offices and premises", "NIA", 6.8, None, 1.04, 520, 0.6),
    "W1": ("Warehouse and premises", "GIA", 0.95, 52, 1.24, 8500, 0.5),
    "W2": ("Factory and premises", "GIA", 1.6, 40, 1.18, 1500, 0.7),
    "W3": ("Workshop and premises", "GIA", 2.4, 55, 1.15, 260, 0.6),
    "F1": ("Restaurant and premises", "NIA", 5.6, None, 0.92, 180, 0.4),
    "F2": ("Cafe and premises", "NIA", 6.4, None, 0.93, 95, 0.4),
    "F3": ("Public house and premises", "GIA", 2.9, 70, 0.95, 420, 0.4),
    "F4": ("Hotel and premises", "GIA", 1.3, 45, 1.0, 2500, 0.6),
    "B1": ("Bank and premises", "NIA", 4.8, None, 0.88, 300, 0.4),
    "M1": ("Vehicle repair workshop and premises", "GIA", 1.8, 45, 1.1, 320, 0.5),
    "M2": ("Petrol filling station and premises", "GIA", 2.0, 60, 1.05, 210, 0.3),
    "S1": ("Surgery and premises", "NIA", 4.0, 90, 1.02, 400, 0.4),
    "S2": ("School and premises", "GIA", 2.2, 25, 1.0, 5200, 0.5),
    "S3": ("Hall and premises", "GIA", 0.6, 20, 1.0, 420, 0.5),
    "S4": ("Sports centre and premises", "GIA", 1.0, 35, 0.98, 2100, 0.6),
    "S5": ("Care home and premises", "GIA", 2.6, 30, 1.0, 1500, 0.4),
}
RETAIL_DESC = ("R1", "R2", "R3", "R4", "O1", "W1")
TIER_SHOP_RV = dict(city=255, large=200, district=180, town=165, small=150)
TIER_IND = dict(city=260, large=125, district=80, town=66, small=46)


class World:
    pass


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    w = World()
    w.rng_seed = seed
    w.centres = [dict(code=c, name=n, district=d, tier=t, k=i) for i, (c, n, d, t) in enumerate(N.CENTRES)]
    w.tier = [c["tier"] for c in w.centres]
    NC = w.NC = len(w.centres)
    size = np.array([TIER_IND[t] for t in w.tier], float) * rng.lognormal(0, 0.18, NC)
    size[0] = TIER_IND["city"]
    w.size = size
    w.zone = np.array([TIER_SHOP_RV[t] for t in w.tier], float) * rng.lognormal(0, 0.05, NC)
    w.P, w.E = [], {}
    w.ind = {k: [] for k in range(NC)}
    w.chains = []
    P, E = w.P, w.E

    def emp(kind, hq, **kw):
        k = len(E)
        E[k] = dict(eid=k, kind=kind, hq=hq, **kw)
        return k

    def area(d, med=None, sd=None):
        return float(np.exp(np.log(med or DESC[d][5]) + (DESC[d][6] if sd is None else sd) * rng.standard_normal()))

    def rv(d, centre, zone, a):
        if d == "R1":
            base = w.zone[centre] if centre is not None else (120.0 if zone == "parade" else 100.0)
        elif d == "O1":
            base = 205.0 if centre == 0 else (150.0 if zone == "biz" else 140.0)
        elif d in ("F1", "F2", "B1"):
            base = (w.zone[centre] if centre is not None else 110.0) * dict(F1=0.9, F2=0.95, B1=1.1)[d]
        else:
            base = DESC[d][3]
        r17 = a * base * float(np.exp(0.12 * rng.standard_normal()))
        return r17, r17 * DESC[d][4] * float(np.exp(0.05 * rng.standard_normal()))

    def staff(d, a):
        return max(1, int(round(a / 100 * DESC[d][2] * np.exp(0.2 * rng.standard_normal()))))

    def prem(e22, e26, centre, zone, d, a=None, built=True):
        a = area(d) if a is None else a
        r17, r23 = rv(d, centre, zone, a)
        s = staff(d, a)
        s26 = 0
        if e26 is not None:
            s26 = max(1, int(round(s * np.exp(0.05 * rng.standard_normal())))) if e26 == e22 else staff(d, a)
        P.append(dict(pid=len(P), centre=centre, zone=zone, d=d, a=a, rv17=r17 if built else None, rv23=r23,
                      built=built, o22=e22, o26=e26, s22=s if e22 is not None else 0, s26=s26))
        return P[-1]

    w.prem, w.emp, w.staff_of = prem, emp, staff
    # independents: single-site shops in the centres (the plan sets their closures and openings) and on parades
    for k in range(NC):
        for _ in range(int(round(size[k]))):
            e = emp("ind", k)
            w.ind[k].append(prem(e, e, k, "centre", "R1"))
    for _ in range(950):
        e = emp("ind_out", None)
        r = rng.random()
        prem(e if r > 0.06 else None, e if r < 0.92 else None, None, "parade", "R1")
    # single-site retailers with a supermarket, a department store, a retail warehouse, a warehouse or an office
    for d, n in [("R3", 34), ("R2", 3), ("R4", 48), ("W1", 45), ("O1", 30)]:
        for _ in range(n):
            if d == "R2":
                c, z = int(rng.integers(1, 6)), "centre"
            elif d in ("R3", "O1") and rng.random() < 0.5:
                c, z = int(rng.integers(1, NC)), "centre"
            else:
                c, z = None, dict(R3="edge", R4="park", W1="ind", O1="biz")[d]
            e = emp("single", c)
            r = rng.random()
            med = dict(W1=1400, O1=260).get(d)
            prem(e if r > 0.05 else None, e if r < 0.95 else None, c, z, d, a=area(d, med) if med else None)

    # single-site employers outside retail in the same descriptions (an all-sector calibration pool): offices and
    # warehouses across the island, and the hairdressers, estate agents and the like in the centres' shop units
    for d, n, z in [("O1", 1500, "biz"), ("W1", 320, "ind"), ("R4", 20, "park")]:
        for _ in range(n):
            e = emp("nonretail", None, cal=True)
            r = rng.random()
            c = int(rng.choice(NC, p=size / size.sum())) if d == "O1" and rng.random() < 0.45 else None
            med = dict(O1=240, W1=1300).get(d)
            prem(e if r > 0.06 else None, e if r < 0.93 else None, c, "centre" if c is not None else z, d,
                 a=area(d, med) if med else None)
    for k in range(NC):
        for _ in range(int(round(size[k] * 0.22))):
            e = emp("nonretail", k, cal=True)
            r = rng.random()
            prem(e if r > 0.07 else None, e if r < 0.91 else None, k, "centre", "R1", a=area("R1", 95))
    for _ in range(260):
        e = emp("nonretail", None, cal=True)
        r = rng.random()
        prem(e if r > 0.07 else None, e if r < 0.92 else None, None, "parade", "R1", a=area("R1", 95))
    # employers outside retail with several shop units: bookmakers and estate agents, and the charities whose shops
    # run on a paid manager and volunteers
    w.r1_groups = []
    for kind, n_firms, shops, dens in [("bookmaker", 2, (8, 16), 6.2), ("estate_agent", 3, (3, 7), 6.2),
                                        ("charity", 6, (2, 7), 2.2)]:
        for _ in range(n_firms):
            e = emp("nonretail", None, group=kind)
            w.r1_groups.append(e)
            for k in [int(x) for x in rng.choice(NC, size=int(rng.integers(*shops)), replace=False, p=size / size.sum())]:
                a = area("R1", 100)
                r17, r23 = rv("R1", k, "centre", a)
                s = max(1, int(round(a / 100 * dens * np.exp(0.2 * rng.standard_normal()))))
                gone = rng.random() < (0.3 if kind == "bookmaker" else 0.1)
                P.append(dict(pid=len(P), centre=k, zone="centre", d="R1", a=a, rv17=r17, rv23=r23, built=True,
                              o22=e, o26=None if gone else e, s22=s,
                              s26=0 if gone else max(1, int(round(s * np.exp(0.05 * rng.standard_normal()))))))

    def pick(n, bias):
        wts = size ** bias
        wts = wts / wts.sum()
        return [int(x) for x in rng.choice(NC, size=min(n, NC), replace=False, p=wts)]

    def chain(kind, shops, bias, hq=None, close_small=0.0, close_n=0, open_shops=0, extra=(), open_extra=(),
              close_extra=(), brand=None):
        if hq is None:
            hq = 0 if rng.random() < 0.12 else ("biz" if rng.random() < 0.85 else int(rng.integers(1, 6)))
        e = emp("chain", hq if isinstance(hq, int) else None, ckind=kind, brand=brand, hq_zone=hq)
        w.chains.append(e)
        prem(e, e, hq if isinstance(hq, int) else None, "centre" if isinstance(hq, int) else "biz", "O1",
             a=float(rng.uniform(250, 1400)))
        mine = pick(shops, bias)
        closing = set(k for k in mine if w.tier[k] in ("town", "small") and rng.random() < close_small)
        for k in list(rng.permutation(mine))[:close_n]:
            closing.add(int(k))
        for k in mine:
            prem(e, None if k in closing else e, k, "centre", "R1")
        for k in pick(open_shops, 0.4):
            prem(None, e, k, "centre", "R1")
        for d, n, where in extra:
            for _ in range(n):
                c = pick(1, 1.0)[0] if where == "centre" else None
                prem(e, e, c, "centre" if c is not None else where, d)
        for d, n, where in open_extra:
            for _ in range(n):
                c = pick(1, 1.0)[0] if where == "centre" else None
                prem(None, e, c, "centre" if c is not None else where, d, built=False)
        for d, n, where in close_extra:
            for _ in range(n):
                c = pick(1, 1.0)[0] if where == "centre" else None
                prem(e, None, c, "centre" if c is not None else where, d)
        return e

    brands = {k: [b for b in N.CHAINS if b[0] == k] for k in ("grocer", "fashion", "health", "home")}
    g = brands["grocer"]
    chain("grocer", 18, 0.3, hq="biz", extra=[("R3", 5, "edge"), ("R3", 2, "centre"), ("W1", 1, "ind")], open_shops=7,
          close_n=2, open_extra=[("W1", 1, "ind")], brand=g[0])
    chain("grocer", 24, 0.1, hq=1, extra=[("R3", 3, "centre"), ("W1", 1, "ind")], close_small=0.25,
          open_extra=[("W1", 1, "ind")], brand=g[1])
    chain("grocer", 0, 0.6, hq="biz", extra=[("R3", 7, "edge"), ("W1", 1, "ind")], open_extra=[("R3", 2, "edge")],
          brand=g[2])
    chain("grocer", 6, 0.5, hq=2, extra=[("R3", 4, "centre"), ("W1", 1, "ind")], close_extra=[("R3", 1, "centre")],
          brand=g[3])
    for b in brands["fashion"]:
        r = rng.random()
        chain("fashion", int(rng.integers(5, 16)), 1.0, close_small=0.5 if r < 0.55 else 0.05,
              extra=[("W1", 1, "ind")] if rng.random() < 0.5 else [],
              open_extra=([("R4", int(rng.integers(1, 3)), "park")] if rng.random() < 0.45 else []) +
                         ([("W1", 1, "ind")] if rng.random() < 0.2 else []), brand=b)
    for b in brands["health"]:
        chain("health", int(rng.integers(8, 24)), 0.2, extra=[("W1", 1, "ind")], close_small=0.15, brand=b)
    for b in brands["home"]:
        chain("home", int(rng.integers(2, 6)), 0.7, extra=[("R4", int(rng.integers(3, 7)), "park")],
              close_small=0.6 if rng.random() < 0.6 else 0.0, close_n=1 if rng.random() < 0.4 else 0,
              open_extra=[("R4", 1, "park")] if rng.random() < 0.4 else [], brand=b)
    for i in range(16):
        chain("small", int(rng.integers(2, 7)), 0.6, close_small=0.2, brand=("small", None, None, N.SMALL_CHAIN_TRADES[i]))
    return w


# ------------------------------------------------------------------------------------------ routes on the world

def occupied(w, yr, kinds=None):
    out = {}
    for p in w.P:
        e = p["o" + yr]
        if e is not None and (kinds is None or w.E[e]["kind"] in kinds):
            out.setdefault(e, []).append(p)
    return out


RETAIL_KINDS = ("chain", "ind", "ind_out", "single")
CAL_ALL = RETAIL_KINDS + ("nonretail",)


def rvk(yr):
    return "rv17" if yr == "22" else "rv23"


def densities(w, yr, kind="tot", pool="retail", basis="area"):
    occ = occupied(w, yr, RETAIL_KINDS if pool == "retail" else CAL_ALL)
    D = {}
    for d in RETAIL_DESC:
        ss = [ps[0] for e, ps in occ.items() if len(ps) == 1 and ps[0]["d"] == d]
        x = np.array([p["a"] if basis == "area" else p[rvk(yr)] for p in ss])
        s = np.array([p["s" + yr] for p in ss], float)
        D[d] = dict(tot=s.sum() / x.sum(), mean=np.mean(s / x), median=np.median(s / x))[kind]
    return D


def regression(w, yr, pool="retail"):
    occ = occupied(w, yr, RETAIL_KINDS if pool == "retail" else CAL_ALL)
    ds = list(RETAIL_DESC)
    X, y = [], []
    for e, ps in occ.items():
        if any(p["d"] not in ds for p in ps):
            continue
        X.append([sum(p["a"] for p in ps if p["d"] == d) for d in ds])
        y.append(sum(p["s" + yr] for p in ps))
    b = np.linalg.lstsq(np.array(X), np.array(y, float), rcond=None)[0]
    return dict(zip(ds, b))


def place(w, yr, how, D=None, kinds=RETAIL_KINDS):
    occ = occupied(w, yr, kinds)
    out = np.zeros(w.NC)
    for e, ps in occ.items():
        T = sum(p["s" + yr] for p in ps)
        if how == "truth":
            for p in ps:
                if p["centre"] is not None:
                    out[p["centre"]] += p["s" + yr]
            continue
        if how == "postcode":
            if w.E[e]["hq"] is not None:
                out[w.E[e]["hq"]] += T
            continue
        if how == "count":
            wt = np.ones(len(ps))
        elif how == "area":
            wt = np.array([p["a"] for p in ps])
        elif how == "rv":
            wt = np.array([p[rvk(yr)] for p in ps])
        elif how == "rv23":
            wt = np.array([p["rv23"] for p in ps])
        elif how == "rvd":
            wt = np.array([p[rvk(yr)] * D[p["d"]] for p in ps])
        else:
            wt = np.array([p["a"] * D[p["d"]] for p in ps])
        wt = wt / wt.sum()
        for p, x in zip(ps, wt):
            if p["centre"] is not None:
                out[p["centre"]] += T * x
    return out


def family_specs(w):
    """(name, how, D22, D26): the golden and every licensed member that takes the density step"""
    S = [("golden", "d", densities(w, "22"), densities(w, "26"))]
    for kind in ["mean", "median"]:
        S.append(("d_" + kind, "d", densities(w, "22", kind), densities(w, "26", kind)))
    S.append(("d_all", "d", densities(w, "22", pool="all"), densities(w, "26", pool="all")))
    D26 = densities(w, "26")
    S.append(("d_pooled26", "d", D26, D26))
    S.append(("d_reg", "d", regression(w, "22"), regression(w, "26")))
    S.append(("d_reg_all", "d", regression(w, "22", "all"), regression(w, "26", "all")))
    S.append(("d_rv", "rvd", densities(w, "22", basis="rv"), densities(w, "26", basis="rv")))
    return S


STANDING = ("golden", "d_mean", "d_median", "d_all", "d_pooled26", "d_reg", "d_reg_all")


def chain_parts(w):
    parts = {}
    for name, how, D22, D26 in family_specs(w):
        parts[name] = (place(w, "22", how, D22, ("chain",)), place(w, "26", how, D26, ("chain",)))
    for r in ["area", "rv", "count", "truth"]:
        parts[r] = (place(w, "22", r, None, ("chain",)), place(w, "26", r, None, ("chain",)))
    parts["single"] = (place(w, "22", "truth", None, ("single",)), place(w, "26", "truth", None, ("single",)))
    return parts


def ind_staff(w, yr, k):
    return sum(p["s" + yr] for p in w.ind[k] if p["o" + yr] is not None)


def change_given(parts, name, k, i22, i26):
    s22, s26 = parts["single"][0][k], parts["single"][1][k]
    return (parts[name][1][k] + i26 + s26) / (parts[name][0][k] + i22 + s22) - 1


def plan(w, quota=dict(area=6, rv=4, count=4), gap=0.014, flip=0.006, share_e=0.36, seed=5):
    """each centre's golden change: rung flips to quota where the chains allow it, every family member and the truth
    clear of the line by max(gap, 8 employees), the other centres off the line on a side drawn at share_e"""
    rng = np.random.default_rng(seed)
    parts = chain_parts(w)
    fam = [s[0] for s in family_specs(w)] + ["truth"]
    grid = np.round(np.arange(-0.22, 0.045, 0.001), 3)
    opts = {}
    for k in range(w.NC):
        i22 = ind_staff(w, "22", k)
        G22 = parts["golden"][0][k] + i22 + parts["single"][0][k]
        rows, fallback = [], []
        need = max(gap, 8.0 / G22)
        for g in grid:
            i26 = (1 + g) * G22 - parts["golden"][1][k] - parts["single"][1][k]
            if not (0.66 * i22 <= i26 <= 1.18 * i22):
                continue
            fv = [change_given(parts, f, k, i22, i26) for f in fam]
            side = g <= TH
            mm = min((v - TH) * (-1 if side else 1) for v in fv)
            fallback.append((mm, float(g)))
            if mm < need:
                continue
            fl = [r for r in ["area", "rv", "count"]
                  if ((change_given(parts, r, k, i22, i26) <= TH) != side)
                  and abs(change_given(parts, r, k, i22, i26) - TH) >= max(flip, 3.0 / G22)]
            rows.append((float(g), fl))
        if not rows:
            rows = [(max(fallback)[1], [])] if fallback else [(float(TH + 0.03), [])]
        opts[k] = rows
    chosen, counts = {}, dict(area=0, rv=0, count=0)
    order = sorted(range(w.NC), key=lambda k: -max([len(fl) for g, fl in opts[k]] + [0]))
    for r in ["rv", "area", "count"]:
        for k in order:
            if k in chosen or counts[r] >= quota[r]:
                continue
            cand = [(g, fl) for g, fl in opts[k] if r in fl]
            if not cand:
                continue
            # anywhere in the range the rung still crosses, so the flipped centres do not bunch at the line
            g, fl = cand[int(rng.integers(0, len(cand)))]
            if any(counts[f] >= quota[f] + 1 for f in fl):
                continue
            chosen[k] = g
            for f in fl:
                counts[f] += 1
    for k in range(w.NC):
        if k in chosen:
            continue
        safe = [(g, fl) for g, fl in opts[k] if not fl] or list(opts[k])
        want_e = rng.random() < share_e
        side = [x for x in safe if (x[0] <= TH) == want_e] or safe
        g, fl = side[int(rng.integers(0, len(side)))]
        chosen[k] = g
        for f in fl:
            counts[f] += 1
    return chosen, counts, parts


def apply_plan(w, chosen, parts, seed=11):
    """close and open independents in each centre to reach the planned golden change"""
    rng = np.random.default_rng(seed)
    for k, g in sorted(chosen.items()):
        i22 = ind_staff(w, "22", k)
        G22 = parts["golden"][0][k] + i22 + parts["single"][0][k]
        want = (1 + g) * G22 - parts["golden"][1][k] - parts["single"][1][k]
        w.ind[k] = [p for p in w.ind[k] if p["o22"] is not None]
        shops = list(w.ind[k])
        for p in shops:
            p["o26"] = p["o22"]
            p["s26"] = max(1, int(round(p["s22"] * np.exp(0.05 * rng.standard_normal()))))
        have = sum(p["s26"] for p in shops)
        for i in rng.permutation(len(shops)):
            if have <= want + 1.5:
                break
            p = shops[i]
            if have - p["s26"] >= want - 1.5:
                have -= p["s26"]
                p["o26"], p["s26"] = None, 0
        while have < want - 4:
            e = w.emp("ind", k)
            a = float(np.exp(np.log(DESC["R1"][5]) + DESC["R1"][6] * rng.standard_normal()))
            s26 = max(1, int(round(a / 100 * DESC["R1"][2] * np.exp(0.2 * rng.standard_normal()))))
            if have + s26 > want + 2:
                del w.E[e]
                continue
            r17 = a * w.zone[k] * float(np.exp(0.12 * rng.standard_normal()))
            p = dict(pid=len(w.P), centre=k, zone="centre", d="R1", a=a, rv17=r17, rv23=r17 * 0.9, built=True,
                     o22=None, o26=e, s22=0, s26=s26, opened=True)
            w.P.append(p)
            w.ind[k].append(p)
            have += s26
        cont = [p for p in shops if p["o26"] is not None]
        j = 0
        while abs(have - want) >= 1 and j < 6 * len(cont):
            p = cont[j % len(cont)]
            step = 1 if want > have else -1
            if p["s26"] + step >= 1:
                p["s26"] += step
                have += step
            j += 1


def levels(w):
    return {name: (place(w, "22", how, D22), place(w, "26", how, D26))
            for name, how, D22, D26 in family_specs(w) if name in STANDING}


def nudge(w, k, yr, delta, rng):
    shops = [p for p in w.ind[k] if p["o" + yr] is not None]
    left = int(round(delta))
    i = 0
    while left != 0 and i < 20 * len(shops):
        p = shops[int(rng.integers(0, len(shops)))]
        step = 1 if left > 0 else -1
        if p["s" + yr] + step >= 1:
            p["s" + yr] += step
            left -= step
        i += 1


UNIT = 50


def tune(w, passes=4, seed=3):
    """every standing member's employment inside one bin of 50 in each March and its change inside one whole per
    cent, by moving a centre's independents' staff a few employees"""
    rng = np.random.default_rng(seed)
    for _ in range(passes):
        L = levels(w)
        g22 = L["golden"][0]
        for k in range(w.NC):
            v22 = np.array([L[n][0][k] for n in L])
            m = np.round(g22[k] / UNIT) * UNIT
            lo = m - UNIT / 2 + 2 + (g22[k] - v22.min())
            hi = m + UNIT / 2 - 2 - (v22.max() - g22[k])
            if not (lo <= g22[k] <= hi):
                nudge(w, k, "22", (lo + hi) / 2 - g22[k], rng)
        L = levels(w)
        for k in range(w.NC):
            v22 = np.array([L[n][0][k] for n in L])
            v26 = np.array([L[n][1][k] for n in L])
            best = None
            for d in range(-40, 41):
                c26 = v26 + d
                cc = c26 / v22 - 1
                if len(set(np.round(c26 / UNIT))) > 1 or len(set(np.round(cc * 100))) > 1:
                    continue
                if np.min(np.abs(c26 - np.round(c26 / UNIT) * UNIT)) > UNIT / 2 - 3:
                    continue
                if np.max(np.abs(cc * 100 - np.round(cc * 100))) > 0.38:
                    continue
                side = cc[0] <= TH
                if any((x <= TH) != side for x in cc) or np.min(np.abs(cc - TH)) < max(0.013, 8.0 / v22.min()):
                    continue
                if best is None or abs(d) < abs(best):
                    best = d
            if best:
                nudge(w, k, "26", best, rng)


def figures_agree(w):
    L = levels(w)
    bad = []
    for k in range(w.NC):
        a = set(int(np.round(L[n][0][k] / UNIT)) for n in L)
        b = set(int(np.round(L[n][1][k] / UNIT)) for n in L)
        c = set(int(np.round((L[n][1][k] / L[n][0][k] - 1) * 100)) for n in L)
        if len(a) > 1 or len(b) > 1 or len(c) > 1:
            bad.append((k, len(a), len(b), len(c)))
    return bad


def changes(w):
    out = {}
    for name, how, D22, D26 in family_specs(w):
        out[name] = place(w, "26", how, D26) / place(w, "22", how, D22) - 1
    for r in ["truth", "area", "rv", "rv23", "count", "postcode"]:
        out[r] = place(w, "26", r) / place(w, "22", r) - 1
    return out


def retail_world(seed=SEED):
    """the retail world with the plan applied twice (the second time on the records' own densities) and tuned"""
    w = build(seed)
    for _ in range(2):
        chosen, counts, parts = plan(w)
        apply_plan(w, chosen, parts)
    tune(w)
    w.plan_counts = counts
    w.gchange = changes(w)["golden"]
    return w
