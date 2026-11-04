"""task285 shipped geometry: the storage-area and warning-area outlines and the road-link polylines, drawn the way the
partnership's, the agency's and the highways authority's GIS carry them (many vertices, irregular, metre precision),
with every membership the analysis reads kept exactly: each address and each surveyed carriageway point stays in the
storage area the model puts it in, with a margin, and every link keeps its two nodes. Deterministic.
"""
import math
import random

import numpy as np

import world as W

MARGIN = 0.004          # km: no address or surveyed point within 4 m of a storage-area outline
POLY_GAP = 0.0005       # km: neighbouring outlines kept apart, never crossing, where they do not share an edge
SPACING = (0.022, 0.042)


def _area(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2


def _key(p):
    return (round(p[0], 4), round(p[1], 4))


def _densify(poly, step):
    out = []
    for i in range(len(poly)):
        a = np.array(poly[i], float)
        b = np.array(poly[(i + 1) % len(poly)], float)
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / step)))
        for k in range(n):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def contains(polys, P):
    """for each point, the first polygon (in dict order) that contains it, by ray casting, or None."""
    res = np.array([None] * len(P), dtype=object)
    X, Y = P[:, 0], P[:, 1]
    for sa, poly in polys.items():
        V = np.asarray(poly, float)
        inside = np.zeros(len(P), bool)
        x1, y1 = V[:, 0], V[:, 1]
        x2, y2 = np.roll(x1, -1), np.roll(y1, -1)
        for i in range(len(V)):
            cond = (y1[i] > Y) != (y2[i] > Y)
            with np.errstate(divide="ignore", invalid="ignore"):
                xc = x1[i] + (Y - y1[i]) * (x2[i] - x1[i]) / (y2[i] - y1[i])
            inside ^= cond & (xc > X)
        free = np.array([r is None for r in res])
        res[free & inside] = sa
    return res


def boundary_distance(polys, P):
    """distance from each point to the nearest outline segment of any polygon."""
    best = np.full(len(P), np.inf)
    for poly in polys.values():
        V = np.asarray(poly, float)
        A, B = V, np.roll(V, -1, axis=0)
        lo, hi = V.min(0) - 0.2, V.max(0) + 0.2
        sel = np.where((P[:, 0] > lo[0]) & (P[:, 0] < hi[0]) & (P[:, 1] > lo[1]) & (P[:, 1] < hi[1]))[0]
        if not len(sel):
            continue
        Q = P[sel]
        AB = B - A
        L2 = (AB ** 2).sum(1)
        for i in range(len(A)):
            t = np.clip(((Q - A[i]) @ AB[i]) / L2[i], 0, 1)
            d = np.hypot(*(Q - (A[i] + t[:, None] * AB[i])).T)
            best[sel] = np.minimum(best[sel], d)
    return best


def _seg_cross(a, b, c, d):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0) and o1 * o2 < 0 and o3 * o4 < 0


def simple(poly):
    """no two non-adjacent edges of the outline cross."""
    V = np.asarray(poly, float)
    n = len(V)
    A, B = V, np.roll(V, -1, axis=0)
    lo = np.minimum(A, B)
    hi = np.maximum(A, B)
    for i in range(n):
        cand = np.where((lo[:, 0] <= hi[i, 0]) & (hi[:, 0] >= lo[i, 0]) & (lo[:, 1] <= hi[i, 1]) & (hi[:, 1] >= lo[i, 1]))[0]
        for j in cand:
            if j <= i + 1 or (i == 0 and j == n - 1):
                continue
            if _seg_cross(A[i], B[i], A[j], B[j]):
                return False
    return True


def _helpers(order):
    """grid points 15 m apart wherever two storage areas lie within 450 m of each other, labelled by the model's own
    membership: they keep each outline out of its neighbour's ground, and out of the slivers two model polygons share."""
    pts = []
    for ia, za in enumerate(order):
        A = np.asarray(W.SA_POLY[za], float)
        for zb in order[ia + 1:]:
            B = np.asarray(W.SA_POLY[zb], float)
            lo = np.maximum(A.min(0), B.min(0)) - 0.45
            hi = np.minimum(A.max(0), B.max(0)) + 0.45
            if (lo > hi).any():
                continue
            xs = np.arange(lo[0], hi[0], 0.015)
            ys = np.arange(lo[1], hi[1], 0.015)
            X, Y = np.meshgrid(xs, ys)
            Q = np.stack([X.ravel(), Y.ravel()], 1)
            da = boundary_distance({za: [tuple(v) for v in A]}, Q)
            db = boundary_distance({zb: [tuple(v) for v in B]}, Q)
            keep = (da < 0.45) & (db < 0.45)
            pts.append(Q[keep])
    # and a line 0.6 m inside every model outline, 5 m apart, so no neighbour's drawn outline reaches into its ground
    for z in order:
        V = np.asarray(W.SA_POLY[z], float)
        sgn = 1.0 if _area(W.SA_POLY[z]) > 0 else -1.0
        for i in range(len(V)):
            a, b = V[i], V[(i + 1) % len(V)]
            L = float(np.hypot(*(b - a)))
            d = (b - a) / L
            inward = np.array([-d[1], d[0]]) * sgn
            n = max(2, int(L / 0.005))
            s_ = np.linspace(0.004 / L, 1 - 0.004 / L, n)
            pts.append(a + np.outer(s_, b - a) + inward * 0.0006)
    H = np.concatenate(pts) if pts else np.zeros((0, 2))
    lab = contains({z: [tuple(v) for v in W.SA_POLY[z]] for z in order}, H)
    sel = np.array([x is not None for x in lab], bool)
    return H[sel], lab[sel]


def crossings(polys):
    """where two outlines cross, or a vertex of one lies inside another (off its boundary): the places, in km."""
    out = []
    names = list(polys)
    for ia, za in enumerate(names):
        A_ = np.asarray(polys[za], float)
        for zb in names[ia + 1:]:
            B_ = np.asarray(polys[zb], float)
            if (np.maximum(A_.min(0), B_.min(0)) > np.minimum(A_.max(0), B_.max(0)) + 1e-9).any():
                continue
            Bn = np.roll(B_, -1, axis=0)
            blo, bhi = np.minimum(B_, Bn), np.maximum(B_, Bn)
            for i in range(len(A_)):
                a1, a2 = A_[i], A_[(i + 1) % len(A_)]
                lo, hi = np.minimum(a1, a2), np.maximum(a1, a2)
                cand = np.where((blo[:, 0] <= hi[0]) & (bhi[:, 0] >= lo[0]) & (blo[:, 1] <= hi[1]) & (bhi[:, 1] >= lo[1]))[0]
                for j in cand:
                    if _seg_cross(a1, a2, B_[j], Bn[j]):
                        out.append((a1 + a2) / 2)
            for X_, Y_, zy in ((A_, B_, zb), (B_, A_, za)):
                ins = contains({zy: [tuple(v) for v in Y_]}, X_)
                on = boundary_distance({zy: [tuple(v) for v in Y_]}, X_) < 0.00001
                out += [X_[k] for k in range(len(X_)) if ins[k] is not None and not on[k]]
    return np.array(out) if out else np.zeros((0, 2))


def storage_area_outlines(P, member, seed=W.SEED + 31):
    """P: (N, 2) points in km; member: the storage area each point is in (or None), the model's truth. Returns the
    outlines and a record of what was checked."""
    member = np.asarray(member, dtype=object)
    order = list(W.SA_POLY)
    old = {z: [tuple(v) for v in W.SA_POLY[z]] for z in order}
    ccw = {z: _area(W.SA_POLY[z]) > 0 for z in order}
    H, hlab = _helpers(order)
    # every constraint point: the data (kept on their side, MARGIN clear) and the helpers (only ever kept out)
    Q = np.concatenate([P, H])
    qlab = np.concatenate([member, hlab])
    is_data = np.r_[np.ones(len(P), bool), np.zeros(len(H), bool)]
    in_old = {z: np.array([x == z for x in contains({z: old[z]}, Q)], bool) for z in order}

    def nearest_edge(z, pts_):
        V = np.asarray(W.SA_POLY[z], float)
        ds = []
        for e in range(len(V)):
            a_, b_ = V[e], V[(e + 1) % len(V)]
            ab = b_ - a_
            tt = np.clip(((pts_ - a_) @ ab) / (ab @ ab), 0, 1)
            ds.append(np.hypot(*(pts_ - (a_ + tt[:, None] * ab)).T))
        return np.argmin(np.stack(ds), axis=0)
    near_edge = {z: nearest_edge(z, Q) for z in order}
    damp = {}
    corner_scale = {}
    flawed = []
    for attempt in range(14):
        rnd = random.Random(seed)
        corner = {}
        for z in order:
            for c in W.SA_POLY[z]:
                k = _key(c)
                if k not in corner:
                    jx = rnd.uniform(0.006, 0.017) * rnd.choice((-1, 1))
                    jy = rnd.uniform(0.006, 0.017) * rnd.choice((-1, 1))
                    s = corner_scale.get(k, 1.0)
                    corner[k] = (c[0] + jx * s, c[1] + jy * s)
        edges = {}
        new_bound = {}
        for sa in order:
            poly = W.SA_POLY[sa]
            for i in range(len(poly)):
                c1, c2 = poly[i], poly[(i + 1) % len(poly)]
                ek = frozenset((_key(c1), _key(c2)))
                if ek in edges:
                    continue
                other = [z for z in order if z != sa and any(
                    frozenset((_key(W.SA_POLY[z][q]), _key(W.SA_POLY[z][(q + 1) % 4]))) == ek for q in range(4))]
                a = np.array(corner[_key(c1)])
                b = np.array(corner[_key(c2)])
                L = float(np.hypot(*(b - a)))
                ts = [0.0]
                while True:
                    nt = ts[-1] + rnd.uniform(*SPACING) / L
                    if nt >= 1 - 0.5 * SPACING[0] / L:
                        break
                    ts.append(nt)
                ts.append(1.0)
                t = np.array(ts)
                d = (b - a) / L
                nrm = np.array([d[1], -d[0]]) if ccw[sa] else np.array([-d[1], d[0]])     # outward for sa
                s_arc = t * L
                A1, A2, A3 = rnd.uniform(0.10, 0.22), rnd.uniform(0.035, 0.07), rnd.uniform(0.006, 0.012)
                l1, l2, l3 = rnd.uniform(0.9, 1.8), rnd.uniform(0.25, 0.5), rnd.uniform(0.06, 0.12)
                p1, p2, p3 = rnd.uniform(0, 6.283), rnd.uniform(0, 6.283), rnd.uniform(0, 6.283)
                noise = (A1 * np.sin(6.2832 * s_arc / l1 + p1) + A2 * np.sin(6.2832 * s_arc / l2 + p2)
                         + A3 * np.sin(6.2832 * s_arc / l3 + p3))
                taper = np.minimum(1.0, np.minimum(t, 1 - t) * L / 0.25) ** 1.5
                dmp = damp.get(ek)
                noise = noise * taper * (dmp if dmp is not None and len(dmp) == len(t) else 1.0)
                lower = np.full(len(t), -np.inf)
                upper = np.full(len(t), np.inf)
                o1, o2 = np.array(c1, float), np.array(c2, float)
                od = (o2 - o1) / np.hypot(*(o2 - o1))
                onrm = np.array([od[1], -od[0]]) if ccw[sa] else np.array([-od[1], od[0]])
                rel = Q - a
                tp = rel @ d / L
                sp = rel @ nrm
                so = (Q - o1) @ onrm
                band = (tp > -0.02) & (tp < 1.02) & (np.abs(sp) < 0.4)
                mine = qlab == sa
                # a data point of sa stays inside; any point of another area, or of none, stays outside when this
                # edge is what holds it out, or when it sits in a sliver sa's model outline shares with another
                keep_in = band & mine & is_data
                keep_out = band & ~mine & ((so > 0) | (in_old[sa] & np.array([x is not None for x in qlab])
                                                       & (near_edge[sa] == i)))
                for sel, is_in in ((keep_in, True), (keep_out, False)):
                    idx = np.where(sel)[0]
                    if not len(idx):
                        continue
                    jj = np.clip(np.searchsorted(t, tp[idx]), 1, len(t) - 1)
                    # a data point of another storage area is left room for that area's own outline as well
                    other_area = np.array([x is not None for x in qlab[idx]], bool) & (not is_in)
                    marg = np.where(is_data[idx], np.where(other_area, 2 * MARGIN, MARGIN), POLY_GAP)
                    for q in (jj - 1, jj):
                        if is_in:
                            np.maximum.at(lower, q, sp[idx] + marg)
                        else:
                            np.minimum.at(upper, q, sp[idx] - marg)
                # the outlines already drawn: never crossed, POLY_GAP clear
                for z in order:
                    if z == sa or z in other or z not in new_bound:
                        continue
                    Bz = _densify(new_bound[z], 0.006)
                    relq = Bz - a
                    tq = relq @ d / L
                    sq = relq @ nrm
                    # a drawn neighbour is kept out: beyond this edge, and where it has reached into sa's own ground
                    inside_sa = np.array([x is not None for x in contains({sa: old[sa]}, Bz)], bool)
                    inside_sa &= nearest_edge(sa, Bz) == i
                    nq = (tq > 0.0) & (tq < 1.0) & (sq < 0.4) & ((sq > 0) | (inside_sa & (sq > -0.4)))
                    if nq.any():
                        jq = np.clip(np.searchsorted(t, tq[nq]), 1, len(t) - 1)
                        for q in (jq - 1, jq):
                            np.minimum.at(upper, q, sq[nq] - POLY_GAP)
                delta = np.clip(noise, lower, upper)
                bad = lower > upper
                delta[bad] = (lower[bad] + upper[bad]) / 2
                sm = delta.copy()
                sm[1:-1] = (delta[:-2] + 2 * delta[1:-1] + delta[2:]) / 4
                delta = np.where(bad, delta, np.clip(sm, lower, upper))
                # near a corner an edge never swings further than 0.6 of its distance from it, so two edges meeting
                # at a corner cannot cross
                env = 0.6 * np.minimum(s_arc, L - s_arc) + 0.002
                delta = np.clip(delta, -env, env)
                delta[0] = delta[-1] = 0.0
                verts = a + np.outer(t, b - a) + np.outer(delta, nrm)
                edges[ek] = (_key(c1), verts)
            out = []
            for i in range(len(poly)):
                c1, c2 = poly[i], poly[(i + 1) % len(poly)]
                k1, verts = edges[frozenset((_key(c1), _key(c2)))]
                vv = verts if k1 == _key(c1) else verts[::-1]
                out.extend([tuple(v) for v in vv[:-1]])
            new_bound[sa] = out
        # round the corners no other storage area shares, where no membership moves
        shared = {}
        for z in order:
            for c in W.SA_POLY[z]:
                shared[_key(c)] = shared.get(_key(c), 0) + 1
        for sa in order:
            V = np.asarray(new_bound[sa])
            for c in W.SA_POLY[sa]:
                if shared[_key(c)] > 1:
                    continue
                ci = int(np.argmin(np.hypot(*(V - np.array(corner[_key(c)])).T)))
                n = len(V)
                for half in (5, 4, 3, 2):
                    seg = [(ci + q) % n for q in range(-half, half + 1)]
                    W2 = V.copy()
                    pts_ = V[seg]
                    for _ in range(3):
                        sm = pts_.copy()
                        sm[1:-1] = 0.25 * pts_[:-2] + 0.5 * pts_[1:-1] + 0.25 * pts_[2:]
                        pts_ = sm
                    W2[seg] = pts_
                    around = np.where(np.hypot(*(Q - V[ci]).T) < 0.45)[0]
                    trial = {sa: [tuple(v) for v in W2]}
                    if len(around):
                        g2 = contains(trial, Q[around])
                        was = contains({sa: [tuple(v) for v in V]}, Q[around])
                        d2 = boundary_distance(trial, Q[around][is_data[around]]) if is_data[around].any() else np.array([1.0])
                        if any(x != y for x, y in zip(g2, was)) or d2.min() < 0.0015:
                            continue
                    V = W2
                    break
            new_bound[sa] = [tuple(v) for v in V]
        masks = {z: np.array([x is not None for x in contains({z: new_bound[z]}, Q)], bool) for z in order}
        count = sum(masks[z].astype(int) for z in order)
        got = np.array([None] * len(Q), dtype=object)
        for z in order[::-1]:
            got[masks[z]] = z
        wrong_data = np.where(is_data & np.array([x != y for x, y in zip(got, qlab)]))[0]
        overlap = np.where(count > 1)[0]
        dist = boundary_distance(new_bound, P)
        tight = np.where(dist < 0.0015)[0]
        flawed = sorted(set(wrong_data.tolist()) | set(overlap.tolist()) | set(tight.tolist()))
        ok_simple = all(simple(v) for v in new_bound.values())
        crossed = crossings(new_bound)
        if not flawed and ok_simple and not len(crossed):
            return new_bound, {"attempts": attempt + 1, "min_distance_m": round(float(dist.min()) * 1000, 2),
                               "vertices": sum(len(v) for v in new_bound.values()), "helpers": int(len(H))}
        near_pts = np.concatenate([Q[flawed] if flawed else np.zeros((0, 2)), crossed])
        for ek, (k1, verts) in edges.items():
            V = np.asarray(verts)
            dmp = damp.get(ek, np.ones(len(V)))
            if len(dmp) != len(V):
                dmp = np.ones(len(V))
            if len(near_pts):
                dd = np.min(np.hypot(V[:, None, 0] - near_pts[None, :, 0], V[:, None, 1] - near_pts[None, :, 1]), axis=1)
                dmp = np.where(dd < 0.15, dmp * 0.5, dmp)
            if not ok_simple:
                dmp = dmp * 0.85
            damp[ek] = dmp
            for ck in ek:
                cp = np.array(ck)
                if len(near_pts) and np.min(np.hypot(*(near_pts - cp).T)) < 0.06:
                    corner_scale[ck] = corner_scale.get(ck, 1.0) * 0.5
    globals()["LAST"] = new_bound
    raise AssertionError("storage-area outlines: %d crossings; memberships could not be kept: %s" % (len(crossed), [
        (int(i), tuple(np.round(Q[i], 4)), qlab[i], got[i], int(count[i]),
         round(float(dist[i]) * 1000, 2) if i < len(P) else None) for i in flawed[:20]]))


def warning_area_outline(poly, seed):
    """an agency warning area drawn round a storage area: its outline pushed out 12 to 35 m, smoothed."""
    rnd = random.Random(seed)
    V = np.asarray(poly, float)
    n = len(V)
    ccw = _area([tuple(v) for v in V]) > 0
    prev, nxt = np.roll(V, 1, axis=0), np.roll(V, -1, axis=0)
    tang = nxt - prev
    tang /= np.hypot(*tang.T)[:, None]
    nrm = np.stack([tang[:, 1], -tang[:, 0]], 1) * (1 if ccw else -1)
    s = np.cumsum(np.r_[0, np.hypot(*(V[1:] - V[:-1]).T)])
    l1, p1 = rnd.uniform(0.5, 1.1), rnd.uniform(0, 6.283)
    off = 0.0235 + 0.0115 * np.sin(6.2832 * s / l1 + p1)
    for scale in (1.0, 0.7, 0.5, 0.3):
        out = V + nrm * (off * scale)[:, None]
        out = out[::2] if n > 400 else out
        if simple([tuple(v) for v in out]):
            return [tuple(v) for v in out]
    return [tuple(v) for v in V]


def link_polylines(survey_by_link, sa_outlines, seed=W.SEED + 37):
    """each link from its start node to its end node: straight through its surveyed points on the floodplain, with
    bends where it runs outside the storage areas, the nodes set to the metre off the 100 m grid."""
    rnd = random.Random(seed)
    shift = {}
    for node in sorted(W.NODES):
        # off the 100 m grid by 8 to 17 m each way, so a node on the floodplain stays within 25 m of its survey
        shift[node] = (rnd.uniform(0.008, 0.017) * rnd.choice((-1, 1)), rnd.uniform(0.008, 0.017) * rnd.choice((-1, 1)))
    lines = {}
    for k, l in enumerate(W.LINKS):
        a, b = l[0], l[1]
        A = np.array(W.NODES[a], float)
        B = np.array(W.NODES[b], float)
        A2 = A + shift[a]
        B2 = B + shift[b]
        sv = sorted(survey_by_link.get(k, []))
        amp_scale = 1.0
        for attempt in range(6):
            pts = [tuple(A2)]
            stretches = []
            if sv:
                # the centreline is digitised a little off the surveyed line, as two systems' lines always are
                u = np.array(sv[-1][1:]) - np.array(sv[0][1:])
                un = np.array([-u[1], u[0]]) / max(float(np.hypot(*u)), 1e-9)
                ud = u / max(float(np.hypot(*u)), 1e-9)
                side = (un * rnd.uniform(0.00021, 0.00083) * rnd.choice((-1, 1))
                        + ud * rnd.uniform(0.00011, 0.00047) * rnd.choice((-1, 1)))
                stretches.append((A2, np.array(sv[0][1:]) + side, "pre"))
                stretches.append((np.array(sv[-1][1:]) + side, B2, "post"))
            else:
                stretches.append((A2, B2, "all"))
            body = []
            for P0, P1, kind in stretches:
                seg = P1 - P0
                ln = float(np.hypot(*seg))
                verts = []
                if ln > 0.06:
                    nrm = np.array([-seg[1], seg[0]]) / ln
                    amp = min(0.085, 0.07 * ln) * rnd.uniform(0.45, 1.0) * rnd.choice((-1, 1)) * amp_scale
                    f, ph = rnd.uniform(0.6, 1.6), rnd.uniform(0, 6.283)
                    n = max(2, int(ln / rnd.uniform(0.028, 0.05)))
                    for q in range(1, n):
                        u = q / n
                        bend = amp * math.sin(math.pi * u) * (0.65 + 0.35 * math.sin(2 * math.pi * f * u + ph))
                        verts.append(tuple(P0 + seg * u + nrm * bend))
                body.append((kind, verts))
            if sv:
                pts += body[0][1]
                pts += [tuple(np.array(s[1:]) + side) for s in sv]
                pts += body[1][1]
            else:
                pts += body[0][1]
            pts.append(tuple(B2))
            # a stretch that is not surveyed must stay off the floodplain, apart from its last 40 m into a survey
            V = np.array(pts)
            dense = []
            for i in range(len(V) - 1):
                m = max(1, int(np.hypot(*(V[i + 1] - V[i])) / 0.005))
                for j in range(m):
                    dense.append(V[i] + (V[i + 1] - V[i]) * j / m)
            D = np.array(dense)
            inside = contains(sa_outlines, D)
            S = np.array([s[1:] for s in sv]) if sv else np.zeros((0, 2))
            bad = False
            for p, s_ in zip(D, inside):
                if s_ is None:
                    continue
                if not len(S) or np.min(np.hypot(*(S - p).T)) > 0.04:
                    bad = True
                    break
            if not bad:
                break
            amp_scale *= 0.5
        assert not bad, ("a stretch of road on the floodplain is more than 40 m from its survey", k)
        lines[k] = pts
    return lines, shift


def polyline_length_m(pts):
    V = np.asarray(pts, float)
    return float(np.hypot(*(V[1:] - V[:-1]).T).sum() * 1000)
