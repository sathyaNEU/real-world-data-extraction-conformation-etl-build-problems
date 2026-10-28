"""task270 world: the county's villages, routing network, addresses and output areas, its stations and engines, and the
all-pairs drive times the operations and the checks run on. Geometry is in a local km frame (x east, y north) and
shipped as metres on the county's grid (E0, N0)."""
from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import Delaunay, cKDTree

import common as K

W_KM, H_KM = 64.0, 50.0
DXY = np.array([(32, 25), (11, 9), (53, 9), (53, 41), (11, 41), (32, 45), (32, 5)], float)
DWT = np.array([40.0, 0, 0, 0, 0, 0, 0])
WTXY = [(s[2], s[3]) for s in K.WT_STATIONS]

# geometry dials (calibrated in tune.py; see the design note's ladder)
DIALS = dict(
    VILL_HOMES={"Calderstow": 10000, "Tollesham": 8000, "Wrenfold": 8000, "Hollinbury": 8000, "Pelmarsh": 8000,
                "Altmoor": 11000, "Skirwold": 11000},
    KEYSH={"Calderstow": 0.45, "Tollesham": 0.45, "Wrenfold": 0.54, "Hollinbury": 0.50, "Pelmarsh": 0.45,
           "Altmoor": 0.75, "Skirwold": 0.84},
    REMSH={"Calderstow": 0.12, "Tollesham": 0.155, "Wrenfold": 0.33, "Hollinbury": 0.05, "Pelmarsh": 0.27,
           "Altmoor": 0.04, "Skirwold": 0.03},
    NSAT={"Calderstow": 12, "Tollesham": 12, "Wrenfold": 12, "Hollinbury": 12, "Pelmarsh": 12, "Altmoor": 18,
          "Skirwold": 18},
    NREM={d: 7 for d in K.DISTRICTS},
    SAT_R=2.6,
    COMMERCIAL={"Calderstow": 4200, "Tollesham": 1300, "Wrenfold": 1200, "Hollinbury": 1300, "Pelmarsh": 1210,
                "Altmoor": 600, "Skirwold": 600},
    VACANT={"Calderstow": 4, "Tollesham": 3, "Wrenfold": 4, "Hollinbury": 3, "Pelmarsh": 3, "Altmoor": 3, "Skirwold": 9},
)
SPEED = {"A road": 75.0, "A road (urban)": 40.0, "Minor road": 46.0, "Local street": 26.0}
WIND = {"A road": 1.08, "A road (urban)": 1.08, "Minor road": 1.28, "Local street": 1.15}


def district_of(xy):
    xy = np.atleast_2d(xy)
    return np.argmin(((xy[:, None, :] - DXY[None]) ** 2).sum(2) - DWT[None], 1)


def in_town(p):
    return any((p[0] - tx) ** 2 + (p[1] - ty) ** 2 <= (r * 1.05) ** 2 for tx, ty, r, _ in K.TOWNS.values())


class World:
    pass


def villages(Wd, dials):
    vill, vw, vd, vrole = [], [], [], []

    def spot(r, di, near=None, rmin=1.1, rmax=None, sep=1.1, gap=2.0):
        rmax = dials["SAT_R"] if rmax is None else rmax
        for _ in range(50000):
            if near is None:
                p = np.array([r.uniform(2.0, W_KM - 2.0), r.uniform(2.0, H_KM - 2.0)])
            else:
                rr = r.uniform(rmin, rmax); a = r.uniform(0, 2 * np.pi)
                p = near + rr * np.array([np.cos(a), np.sin(a)])
                if not (1.0 < p[0] < W_KM - 1.0 and 1.0 < p[1] < H_KM - 1.0):
                    continue
            if district_of(p)[0] != di:
                continue
            if any(np.hypot(*(p - np.array(t[:2]))) < t[2] + gap for t in K.TOWNS.values()):
                continue
            if vill and min(np.hypot(*(p - q)) for q in vill) < sep:
                continue
            return p
        return None

    for di, dname in enumerate(K.DISTRICTS):
        r = K.rng("villages", dname)
        noc = len(K.OC_STATIONS[dname])
        keys = []
        while len(keys) < noc:
            p = spot(r, di, sep=2.0)
            if all(np.hypot(*(p - q)) > 6.5 for q in keys) and all(np.hypot(*(p - np.array(w))) > 7.0 for w in WTXY):
                keys.append(p); vill.append(p); vw.append(r.uniform(0.85, 1.15)); vd.append(di); vrole.append(0)
        for k in range(dials["NSAT"][dname]):
            p = spot(r, di, near=keys[k % len(keys)])
            if p is None:
                p = spot(r, di)
            vill.append(p); vw.append(float(np.exp(r.normal(0, 0.6)))); vd.append(di); vrole.append(1)
        for k in range(dials["NREM"][dname]):
            p = spot(r, di, sep=1.6)
            vill.append(p); vw.append(float(np.exp(r.normal(0, 0.5)))); vd.append(di); vrole.append(2)
    vill = np.array(vill); vw = np.array(vw); vd = np.array(vd); vrole = np.array(vrole)
    vh = np.zeros(len(vill))
    for di, dname in enumerate(K.DISTRICTS):
        tgt = dials["VILL_HOMES"][dname]
        for role, share in ((0, dials["KEYSH"][dname]), (2, dials["REMSH"][dname]),
                            (1, 1 - dials["KEYSH"][dname] - dials["REMSH"][dname])):
            m = (vd == di) & (vrole == role)
            vh[m] = tgt * share * vw[m] / vw[m].sum()
    Wd.vill, Wd.vw, Wd.vd, Wd.vrole, Wd.vh = vill, vw, vd, vrole, np.round(vh).astype(int)


def network(Wd):
    r = K.rng("network")
    pts = []
    for name, (tx, ty, rr, h) in K.TOWNS.items():
        n = int(np.pi * rr * rr / 0.12)
        rad = rr * np.sqrt(r.uniform(0, 1, n)); ang = r.uniform(0, 2 * np.pi, n)
        pts += list(np.c_[tx + rad * np.cos(ang), ty + rad * np.sin(ang)])
    for i, v in enumerate(Wd.vill):
        k = 1 + int(Wd.vrole[i] == 0) + int(Wd.vrole[i] == 0 and Wd.vw[i] > 1.0)
        pts += list(v + r.normal(0, 0.25, (k, 2)))
    pts = np.array(pts)
    rpts = np.c_[r.uniform(0, W_KM, 2600), r.uniform(0, H_KM, 2600)]
    tree = cKDTree(pts)
    rpts = np.array([p for p in rpts if not tree.query_ball_point(p, 0.75)])
    pts = np.vstack([pts, rpts])
    tree = cKDTree(pts)
    drop = set()
    for i, j in sorted(tree.query_pairs(0.12)):
        if i not in drop:
            drop.add(j)
    pts = np.delete(pts, sorted(drop), 0)
    tri = Delaunay(pts)
    edges = set()
    for s in tri.simplices:
        for a, b in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])):
            edges.add((min(a, b), max(a, b)))
    edges = np.array(sorted(edges))
    tree = cKDTree(pts)
    mid = (pts[edges[:, 0]] + pts[edges[:, 1]]) / 2
    rad = np.hypot(*(pts[edges[:, 0]] - pts[edges[:, 1]]).T) / 2
    gab = np.array([len(tree.query_ball_point(m, rr * 0.999)) <= 2 for m, rr in zip(mid, rad)])
    edges = edges[gab]
    L = np.hypot(*(pts[edges[:, 0]] - pts[edges[:, 1]]).T)
    mid = (pts[edges[:, 0]] + pts[edges[:, 1]]) / 2
    town_e = np.array([in_town(m) for m in mid])
    apairs = [("Calderstow", t) for t in ("Tollesham", "Wrenfold", "Hollinbury", "Pelmarsh")] + \
             [("Tollesham", "Wrenfold"), ("Hollinbury", "Pelmarsh"), ("Tollesham", "Pelmarsh"), ("Wrenfold", "Hollinbury")]

    def seg_dist(p, a, b):
        a, b = np.array(a[:2]), np.array(b[:2]); d = b - a
        t = np.clip(((p - a) @ d) / (d @ d), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T)

    aroad = np.zeros(len(edges), bool)
    for a, b in apairs:
        aroad |= seg_dist(mid, K.TOWNS[a], K.TOWNS[b]) < 0.55
    minor = ~aroad & ~town_e
    dropm = minor & (r.random(len(edges)) < 0.22) & (L > 0.6)
    edges, L, mid, town_e, aroad = edges[~dropm], L[~dropm], mid[~dropm], town_e[~dropm], aroad[~dropm]
    cls = np.where(aroad, np.where(town_e, "A road (urban)", "A road"), np.where(town_e, "Local street", "Minor road"))
    # keep the connected network
    N = len(pts)
    G0 = csr_matrix((np.ones(2 * len(edges)), (np.r_[edges[:, 0], edges[:, 1]], np.r_[edges[:, 1], edges[:, 0]])),
                    shape=(N, N))
    _, lab = connected_components(G0, directed=False)
    big = np.bincount(lab).argmax()
    keep = np.where(lab == big)[0]
    remap = -np.ones(N, int); remap[keep] = np.arange(len(keep))
    ok = (remap[edges[:, 0]] >= 0) & (remap[edges[:, 1]] >= 0)
    edges = remap[edges[ok]]; L = L[ok]; cls = cls[ok]
    pts = pts[keep]
    # one-way streets in the town centres: a link whose reverse can be driven round, chosen until strong connectivity
    # would break
    oneway = np.zeros(len(edges), bool)
    cand = [i for i in np.where(np.array([c == "Local street" for c in cls]))[0]
            if min(np.hypot(*(pts[edges[i]].mean(0) - np.array(t[:2]))) for t in K.TOWNS.values()) < 1.0]
    r.shuffle(cand)
    for i in cand[:90]:
        oneway[i] = True
        if not _strong(pts, edges, oneway):
            oneway[i] = False
    Wd.nodes, Wd.edges, Wd.L, Wd.cls, Wd.oneway = pts, edges, L * 1000.0, cls, oneway
    Wd.drive_s = np.round(np.array([L[i] * WIND[c] / SPEED[c] * 3600.0 for i, c in enumerate(cls)]), 1)
    Wd.N = len(pts)


def _strong(pts, edges, oneway):
    N = len(pts)
    a = np.r_[edges[:, 0], edges[~oneway, 1]]
    b = np.r_[edges[:, 1], edges[~oneway, 0]]
    G = csr_matrix((np.ones(len(a)), (a, b)), shape=(N, N))
    n, _ = connected_components(G, directed=True, connection="strong")
    return n == 1


def graph(Wd):
    a = np.r_[Wd.edges[:, 0], Wd.edges[~Wd.oneway, 1]]
    b = np.r_[Wd.edges[:, 1], Wd.edges[~Wd.oneway, 0]]
    w = np.r_[Wd.drive_s, Wd.drive_s[~Wd.oneway]]
    return csr_matrix((w, (a, b)), shape=(Wd.N, Wd.N))


def addresses(Wd, dials):
    """Residential and commercial address points (km frame), each with a district; homes from towns and villages."""
    xy, kind = [], []
    for name, (tx, ty, rr, h) in K.TOWNS.items():
        q = K.rng("town-homes", name)
        n = h
        rad = rr * np.sqrt(q.beta(1.4, 1.0, n)); ang = q.uniform(0, 2 * np.pi, n)
        xy.append(np.c_[tx + rad * np.cos(ang), ty + rad * np.sin(ang)]); kind += ["R"] * n
    for i, (v, h) in enumerate(zip(Wd.vill, Wd.vh)):
        q = K.rng("village-homes", i)
        centres = v + q.normal(0, 0.30, (40, 2))
        w = q.dirichlet(np.ones(40))
        c = np.floor(w * h).astype(int); c[np.argmax(c)] += h - c.sum()
        pts = np.repeat(centres, c, axis=0) + q.normal(0, 0.05, (h, 2))
        xy.append(pts); kind += ["R"] * h
    q = K.rng("farms")
    nf = 700
    farm_xy = np.c_[q.uniform(1.0, W_KM - 1.0, nf), q.uniform(1.0, H_KM - 1.0, nf)]
    farm_n = q.integers(1, 5, nf)
    xy.append(np.repeat(farm_xy, farm_n, axis=0) + q.normal(0, 0.03, (farm_n.sum(), 2))); kind += ["R"] * int(farm_n.sum())
    # commercial premises: town centres and village cores, farms' agricultural units
    for di, dname in enumerate(K.DISTRICTS):
        q = K.rng("commercial", dname)
        n = dials["COMMERCIAL"][dname]
        if dname in K.TOWNS:
            tx, ty, rr, _ = K.TOWNS[dname]
            k = int(n * 0.75)
            rad = rr * np.sqrt(q.beta(1.0, 1.6, k)); ang = q.uniform(0, 2 * np.pi, k)
            xy.append(np.c_[tx + rad * np.cos(ang), ty + rad * np.sin(ang)]); kind += ["C"] * k
            n -= k
        vi = np.where(Wd.vd == di)[0]
        pick = q.choice(vi, n, p=Wd.vh[vi] / Wd.vh[vi].sum())
        xy.append(Wd.vill[pick] + q.normal(0, 0.25, (n, 2))); kind += ["C"] * n
    # vacant commercial units on the town and village industrial estates: in the register, never the scene of a call
    for di, dname in enumerate(K.DISTRICTS):
        n = dials["VACANT"][dname]
        if n <= 0:
            continue
        q = K.rng("vacant", dname)
        if dname in K.TOWNS:
            tx, ty, rr, _ = K.TOWNS[dname]
            ang = q.uniform(0, 2 * np.pi, n)
            rad = rr * q.uniform(0.7, 0.95, n)
            pts = np.c_[tx + rad * np.cos(ang), ty + rad * np.sin(ang)]
        else:
            vi = np.where((Wd.vd == di) & (Wd.vrole == 0))[0]
            pts = Wd.vill[q.choice(vi, n)] + q.normal(0, 0.3, (n, 2))
        keep = district_of(pts) == di
        xy.append(pts[keep]); kind += ["V"] * int(keep.sum())
    xy = np.vstack(xy)
    kind = np.array(kind)
    xy[:, 0] = np.clip(xy[:, 0], 0.2, W_KM - 0.2); xy[:, 1] = np.clip(xy[:, 1], 0.2, H_KM - 0.2)
    Wd.axy, Wd.akind = xy, kind
    Wd.adist = district_of(xy)


def output_areas(Wd):
    """Output areas by recursive bisection of each district's homes (about 125 homes each); commercial addresses
    take the output area of the nearest home."""
    res = np.where(Wd.akind == "R")[0]
    oa = -np.ones(len(Wd.axy), int)
    cells = []
    for di in range(len(K.DISTRICTS)):
        idx = res[Wd.adist[res] == di]
        stack = [idx]
        while stack:
            s = stack.pop()
            if len(s) <= 180:
                cells.append(s)
                continue
            p = Wd.axy[s]
            ax = int(np.ptp(p[:, 1]) > np.ptp(p[:, 0]))
            o = s[np.argsort(p[:, ax], kind="stable")]
            h = len(o) // 2
            stack += [o[:h], o[h:]]
    cells.sort(key=lambda s: (Wd.adist[s[0]], round(float(Wd.axy[s, 1].mean()), 3), round(float(Wd.axy[s, 0].mean()), 3)))
    for k, s in enumerate(cells):
        oa[s] = k
    com = np.where(Wd.akind != "R")[0]
    t = cKDTree(Wd.axy[res])
    for j in com:
        cand = res[t.query(Wd.axy[j], k=8)[1]]
        same = [c for c in cand if Wd.adist[c] == Wd.adist[j]]
        oa[j] = oa[same[0] if same else cand[0]]
    Wd.aoa = oa
    Wd.n_oa = len(cells)
    Wd.oa_district = np.array([Wd.adist[s[0]] for s in cells])
    r = K.rng("oa-codes")
    codes = set()
    out = []
    while len(out) < Wd.n_oa:
        c = "E00%06d" % r.integers(160000, 189999)
        if c not in codes:
            codes.add(c); out.append(c)
    Wd.oa21 = np.array(sorted(out))
    # 2011 vintage: most areas kept their code; a few 2021 pairs were one 2011 area, split at the 2021 census
    oa11 = Wd.oa21.copy()
    by_d = {}
    for k in range(Wd.n_oa):
        by_d.setdefault(Wd.oa_district[k], []).append(k)
    split = []
    for di, ks in by_d.items():
        rr = K.rng("oa-split", di)
        pick = rr.choice(len(ks) - 1, max(3, len(ks) // 30), replace=False)
        for p in sorted(pick):
            a, b = ks[p], ks[p + 1]
            if a in split or b in split:
                continue
            old = "E00%06d" % (100000 + len(split) * 7 + int(rr.integers(0, 7)))
            while old in codes:
                old = "E00%06d" % (int(old[3:]) + 1)
            codes.add(old)
            oa11[a] = old; oa11[b] = old
            split += [a, b]
    Wd.oa11 = oa11


def stations(Wd):
    St = []
    node_tree = cKDTree(Wd.nodes)
    for code, name, x, y, n in K.WT_STATIONS:
        St.append(dict(code=code, name=name, duty="Wholetime", xy=np.array([x, y]), engines=n,
                       district=K.DISTRICTS[int(district_of(np.array([x, y]))[0])]))
    for di, dname in enumerate(K.DISTRICTS):
        keys = np.where((Wd.vd == di) & (Wd.vrole == 0))[0]
        for (code, name), i in zip(K.OC_STATIONS[dname], keys):
            St.append(dict(code=code, name=name, duty="On-call", xy=Wd.vill[i].copy(), engines=1, district=dname))
    for s in St:
        s["node"] = int(node_tree.query(s["xy"])[1])
        s["e"] = int(round(K.E0 + s["xy"][0] * 1000)); s["n"] = int(round(K.N0 + s["xy"][1] * 1000))
    Wd.stations = St
    r = K.rng("registrations")
    letters = "ABCDEFGHJKLMNOPRSTUVWXY"
    E = []
    used = set()
    for si, s in enumerate(St):
        for k in range(s["engines"]):
            while True:
                reg = "Y%s%02d %s" % (letters[r.integers(len(letters))], int(r.choice([16, 17, 18, 19, 20, 21, 22, 23])),
                                      "".join(letters[r.integers(len(letters))] for _ in range(3)))
                if reg not in used:
                    used.add(reg); break
            E.append(dict(call_sign="%sP%d" % (s["code"], k + 1), registration=reg, station=si, crew=s["duty"],
                          home=s["node"]))
    Wd.engines = E
    Wd.nE = len(E)
    Wd.home = np.array([e["home"] for e in E])
    Wd.ewt = np.array([e["crew"] == "Wholetime" for e in E])
    Wd.turn_s = np.where(Wd.ewt, K.TURNOUT["Wholetime"] * 60.0, K.TURNOUT["On-call"] * 60.0)
    Wd.training_node = int(node_tree.query(np.array(K.TRAINING_CENTRE[1:]))[1])


def build(dials=None):
    dials = dict(DIALS if dials is None else dials)
    Wd = World()
    villages(Wd, dials)
    network(Wd)
    addresses(Wd, dials)
    output_areas(Wd)
    stations(Wd)
    G = graph(Wd)
    D, PRED = dijkstra(G, directed=True, return_predecessors=True)
    Wd.D = D.astype(np.float32)
    Wd.PRED = PRED.astype(np.int32)
    t = cKDTree(Wd.nodes)
    Wd.anode = t.query(Wd.axy)[1]
    return Wd


def path(Wd, a, b):
    out = [b]
    while out[-1] != a:
        out.append(int(Wd.PRED[a, out[-1]]))
    return out[::-1]
