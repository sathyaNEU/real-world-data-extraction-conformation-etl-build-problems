"""The Merrimont network, its 2028 trip tables and the user-equilibrium assignment."""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

# Volume-delay functions by facility type (model documentation, table 4.2): t = t0 * (1 + alpha * (v/c)^beta)
VDF = {"freeway": (0.15, 6.0), "bridge": (0.80, 6.0), "ramp": (0.80, 6.0), "arterial": (0.60, 4.0),
       "collector": (0.75, 4.0), "connector": (0.0, 1.0)}
LANE_CAP = {"freeway": 1900, "bridge": 1800, "ramp": 1700, "arterial": 850, "collector": 650, "connector": 9999}


def build_network(P):
    """Links of the 2028 no-build network: (link_id, a, b, name, ftype, lanes, length_mi, speed_mph)."""
    L = []
    def add(a, b, name, ftype, lanes, length, speed, both=True):
        L.append([a, b, name, ftype, lanes, length, speed])
        if both:
            L.append([b, a, name, ftype, lanes, length, speed])
    # Route 9 northbound and southbound mainline on the west bank, F1 (south) to F4, then the bridge
    for i, (ln, length) in enumerate([(3, 1.6), (P["millbrook_lanes"], 1.9), (3, 1.4)], start=1):
        add(f"F{i}", f"F{i+1}", "Route 9", "freeway" if i != 2 else "freeway_bottleneck", ln, length, 60)
    add("F4", "BN", "Route 9 Ashkettle Bridge", "bridge", P["r9_bridge_lanes"], 0.9, 55)
    add("BN", "FX", "Route 9", "freeway", 3, 0.4, 55)
    add("FX", "DT1", "Ferry Street exit", "ramp", P["ferry_lanes"], 0.5, 35)
    add("FX", "EF", "Route 9", "freeway", 3, 2.2, 60)
    # west arterial spine A1..A4 (Millbrook Road) with on-ramps to Route 9
    for i in range(1, 4):
        add(f"A{i}", f"A{i+1}", "Millbrook Road", "arterial", 2, 1.6, 35)
    for i in range(1, 5):
        add(f"A{i}", f"F{i}", "Route 9 ramp", "ramp", 2, 0.3, 40)
    # crossings
    add("A3", "C3", "Center Street Bridge", "arterial", P["center_lanes"], 1.2, 30)
    add("A1", "C1", "Southport Bridge", "arterial", 2, 1.4, 30)
    # east bank arterials and downtown
    for i in range(1, 4):
        add(f"C{i}", f"C{i+1}", "Harbor Avenue", "arterial", 2, 1.3, 30)
    add("C3", "DT1", "Center Street", "arterial", P["center_dt_lanes"], 0.6, 25)
    add("C2", "DT2", "Southport Avenue", "arterial", 2, 0.8, 25)
    add("DT1", "DT2", "Downtown grid", "collector", 3, 0.5, 20)
    add("C4", "EF", "Lakeview Parkway", "arterial", 2, 1.5, 40)
    # zone connectors
    for z, n in P["connectors"]:
        add(z, n, "connector", "connector", 9, 0.2, 30)
    out = []
    for k, (a, b, name, ft, ln, length, sp) in enumerate(L):
        base_ft = "freeway" if ft == "freeway_bottleneck" else ft
        out.append(dict(link_id=1000 + k, a=a, b=b, name=name, ftype=base_ft, bottleneck=(ft == "freeway_bottleneck"),
                        lanes=ln, length_mi=length, speed_mph=sp))
    return out


def link_arrays(links, cap_override=None):
    cap = np.array([l["lanes"] * LANE_CAP[l["ftype"]] for l in links], float)
    t0 = np.array([60.0 * l["length_mi"] / l["speed_mph"] for l in links])
    al = np.array([VDF["bridge" if l["bottleneck"] else l["ftype"]][0] for l in links])
    be = np.array([VDF["bridge" if l["bottleneck"] else l["ftype"]][1] for l in links])
    if cap_override is not None:
        cap = cap_override
    return cap, t0, al, be


class Assign:
    def __init__(self, links):
        self.links = links
        nodes = sorted({l["a"] for l in links} | {l["b"] for l in links})
        self.ix = {n: i for i, n in enumerate(nodes)}
        self.A = np.array([self.ix[l["a"]] for l in links])
        self.B = np.array([self.ix[l["b"]] for l in links])
        self.N = len(nodes)
        self.LI = {(a, b): k for k, (a, b) in enumerate(zip(self.A, self.B))}

    def aon(self, t, od):
        G = csr_matrix((t, (self.A, self.B)), shape=(self.N, self.N))
        f = np.zeros(len(self.links))
        by_o = {}
        for (o, d), q in od.items():
            by_o.setdefault(o, []).append((d, q))
        for o, lst in by_o.items():
            _, pred = dijkstra(G, indices=self.ix[o], return_predecessors=True)
            for d, q in lst:
                cur = self.ix[d]
                while cur != self.ix[o]:
                    p = pred[cur]
                    f[self.LI[(p, cur)]] += q
                    cur = p
        return f

    def ue(self, od, cap, t0, al, be, iters=4000, tol=1e-7):
        tt = lambda v: t0 * (1 + al * (v / cap) ** be)
        v = self.aon(tt(np.zeros(len(t0))), od)
        gap = 1.0
        for it in range(iters):
            t = tt(v)
            y = self.aon(t, od)
            gap = (v @ t - y @ t) / (v @ t)
            if gap < tol:
                break
            lo, hi = 0.0, 1.0
            for _ in range(60):
                m = (lo + hi) / 2
                if np.sum((y - v) * tt(v + m * (y - v))) > 0:
                    hi = m
                else:
                    lo = m
            v = v + (lo + hi) / 2 * (y - v)
        return v, tt(v), gap, it


def ue_paths(links, od, cap, t0, al, be, tol=1e-12, iters=5000):
    """Path-based user equilibrium (gradient projection with column generation, Jayakrishnan et al.).
    od: {(origin_node, dest_node): trips}. Returns link flows, link times, relative gap, iterations."""
    asg = Assign(links)
    n = len(links)
    tt = lambda v: t0 * (1 + al * (v / cap) ** be)
    dtt = lambda v: t0 * al * be * (v / cap) ** (be - 1) / cap
    G0 = None
    paths = {k: [] for k in od}        # list of (tuple(link idx), flow)

    def sp(t):
        G = csr_matrix((t, (asg.A, asg.B)), shape=(asg.N, asg.N))
        out = {}
        for o in sorted({k[0] for k in od}):
            dist, pred = dijkstra(G, indices=asg.ix[o], return_predecessors=True)
            for k in od:
                if k[0] != o:
                    continue
                cur, seq = asg.ix[k[1]], []
                while cur != asg.ix[o]:
                    p = pred[cur]
                    seq.append(asg.LI[(p, cur)])
                    cur = p
                out[k] = (tuple(reversed(seq)), dist[asg.ix[k[1]]])
        return out
    v = np.zeros(n)
    for k, (p, _) in sp(tt(v)).items():
        paths[k].append([p, od[k]])
        for e in p:
            v[e] += od[k]
    gap = 1.0
    for it in range(iters):
        t = tt(v)
        best = sp(t)
        tot = sum(f * t[list(p)].sum() for k in paths for p, f in paths[k])
        low = sum(od[k] * best[k][1] for k in od)
        gap = (tot - low) / tot
        if gap < tol:
            break
        for k in od:
            bp = best[k][0]
            if all(p != bp for p, _ in paths[k]):
                paths[k].append([bp, 0.0])
            t = tt(v)
            d = dtt(v)
            costs = [t[list(p)].sum() for p, _ in paths[k]]
            j = int(np.argmin(costs))
            pj = set(paths[k][j][0])
            for i, (p, f) in enumerate(paths[k]):
                if i == j or f <= 0:
                    continue
                diff = set(p) ^ pj
                s = d[list(diff)].sum()
                shift = min(f, (costs[i] - costs[j]) / s) if s > 0 else f
                if shift <= 0:
                    continue
                paths[k][i][1] -= shift
                paths[k][j][1] += shift
                for e in p:
                    v[e] -= shift
                for e in paths[k][j][0]:
                    v[e] += shift
                t = tt(v); d = dtt(v)
                costs = [t[list(pp)].sum() for pp, _ in paths[k]]
            paths[k] = [pf for pf in paths[k] if pf[1] > 1e-12 or pf[0] == paths[k][j][0]]
    v = np.maximum(v, 0)
    return v, tt(v), gap, it
