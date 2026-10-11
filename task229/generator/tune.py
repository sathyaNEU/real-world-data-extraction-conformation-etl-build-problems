"""Pick the network salt (which nights which collectors fail) and a texture salt per build so the
design's margins hold and every two-decimal figure sits clear of its rounding edge. The salts re-draw
only random texture; the design parameters (rates, populations, topology) do not change. Run once;
the chosen salts are written into world.NET_SALT and world.SALT by hand.

    python3 task229/generator/tune.py [first_net_salt] [last_net_salt]
"""
import collections
import math
import sys

import numpy as np

import world as W
import sim as S

REF, K = W.REFERENCE, W.K_SE


def edge(x):
    """Distance from x to the nearest two-decimal rounding edge (the x.xx5 points)."""
    return abs((x * 100) % 1 - 0.5) / 100


def cr(Y, X, groups, R, small=True):
    g = collections.defaultdict(lambda: [0.0, 0.0])
    for y, x, k_ in zip(Y, X, groups):
        g[k_][0] += y
        g[k_][1] += x
    d = np.array([a - R * c for a, c in g.values()])
    k = len(d)
    f = k / (k - 1) if small else 1.0
    return 100 * math.sqrt(f * float((d ** 2).sum())) / float(X.sum())


def cr_mean(SH, groups, small=True):
    """Standard error of a mean of installation shares, from the groups' summed deviations."""
    mu = SH.mean()
    g = collections.defaultdict(float)
    for s_, k_ in zip(SH, groups):
        g[k_] += s_ - mu
    d = np.array(list(g.values()))
    k = len(d)
    f = k / (k - 1) if small else 1.0
    return math.sqrt(f * float((d ** 2).sum())) / len(SH)


def carve_margins(sel, events):
    """Margins under the outage carve-outs a solver might improvise (none is in the standard, which
    counts every expected interval): the failed node-days dropped for every installation behind the
    node, the node backlog counted as held, the installations behind a failed node dropped. Each with
    the installation-level error."""
    failed = {(p_, d) for p_, d, _, _ in events}
    nodes = {p_ for p_, _, _, _ in events}
    out = {}
    rows = {"drop_days": [], "backlog_held": [], "drop_nodes": []}
    for i in sel:
        dc = S.day_counts(i)
        keep = [x for d, x in enumerate(dc) if (i.parent, d) not in failed]
        rows["drop_days"].append(100.0 * sum(x[0] - x[2] - x[3] for x in keep) / sum(x[0] for x in keep))
        rows["backlog_held"].append(100.0 * sum((x[0] - x[3]) if (i.parent, d) in failed else (x[0] - x[2] - x[3])
                                                for d, x in enumerate(dc)) / sum(x[0] for x in dc))
        if i.parent not in nodes:
            rows["drop_nodes"].append(100.0 * sum(x[0] - x[2] - x[3] for x in dc) / sum(x[0] for x in dc))
    for k, v in rows.items():
        v = np.array(v)
        out[k] = v.mean() - (REF - K * v.std(ddof=1) / math.sqrt(len(v)))
    return out


def figures(sel):
    Y, X, Yl, P, SH, SHl, SHr = [], [], [], [], [], [], []
    for i in sel:
        k = len(W.PROFILES[i.profile][0])
        dc = S.day_counts(i)
        y = sum(x[0] - x[2] - x[3] for x in dc) * k
        x_ = sum(x[0] for x in dc) * k
        Y.append(y)
        X.append(x_)
        Yl.append(sum(x[0] - x[3] for x in dc) * k)
        pres = [x for x in dc if x[0] - x[2] - x[3] > 0]
        SHr.append(100.0 * sum(x[0] - x[2] - x[3] for x in pres) / max(1, sum(x[0] for x in pres)))
        P.append(i.parent)
        SH.append(100.0 * y / x_)
        SHl.append(100.0 * Yl[-1] / x_)
    Y, X, SH, SHl, SHr = (np.array(a, float) for a in (Y, X, SH, SHl, SHr))
    n = len(SH)
    rh = SH.mean()
    se = dict(col=cr_mean(SH, P), col0=cr_mean(SH, P, False), inst=float(SH.std(ddof=1) / math.sqrt(n)),
              bin=100 * math.sqrt((rh / 100) * (1 - rh / 100) / X.sum()))
    m = {k: rh - (REF - K * v) for k, v in se.items()}
    m["late"] = SHl.mean() - (REF - K * cr_mean(SHl, P))
    m["rows"] = SHr.mean() - (REF - K * cr_mean(SHr, P))
    pooled = 100 * Y.sum() / X.sum()
    m["pooled_inst"] = pooled - (REF - K * float(SH.std(ddof=1) / math.sqrt(n)))
    return dict(n=n, k=len(set(P)), rh=rh, se=se, m=m, lcl=REF - K * se["col"], pooled=pooled)


def ok(b, f):
    m = f["m"]
    if min(edge(f["rh"]), edge(f["lcl"]), edge(f["se"]["col"]), edge(f["rh"] - f["lcl"])) < 0.0015:
        return False
    if round(round(f["rh"], 2) - round(f["lcl"], 2), 2) != round(f["rh"] - f["lcl"], 2):
        return False            # the distance to the limit reads the same from rounded or unrounded figures
    if (m["col"] < 0) != (m["col0"] < 0) or abs(m["col0"]) < 0.05:
        return False
    if f["se"]["col"] < 0.85 * f["se"]["inst"]:
        return False            # a build's comms-parent error does not undercut its installation error
    return {
        "EM3.10.9": m["col"] <= -0.15 and m["inst"] <= -0.15,
        "EM3.11.4": m["col"] >= 0.2 and m["inst"] >= 0.08,
        "EM3.12.0": m["col"] >= 0.3 and m["inst"] <= -0.5 and max(f.get("carve", {"x": -1}).values()) <= -0.08,
        "EM3.12.1": m["col"] <= -0.15 and m["inst"] <= -0.15,
        "EM3.12.2": m["col"] >= 0.5 and m["inst"] <= -0.2,
        "PX5.2.7": m["col"] <= -0.15 and m["inst"] <= -0.15 and m["late"] >= 0.1 and m["rows"] >= 0.1,
        "PX5.3.0": m["col"] >= 0.1 and m["inst"] >= 0.1,
        "PX5.3.1": m["col"] >= 0.3 and m["inst"] >= 0.3 and m["bin"] <= -0.1,
    }[b]


def fleet(net_salt):
    W.NET_SALT = net_salt
    insts = S.make_fleet()
    S.apply_events(insts, S.network_events())
    return insts


def run(insts, b, salt):
    W.SALT[b] = salt
    sel = sorted([i for i in insts if i.group == "full" and i.build_start == b], key=lambda x: x.nmi)
    for i in sel:
        i.blocks = S.own_blocks(i)
    if b == "PX5.3.1":
        sel[S.PILOT_DROP].blocks.append((int(2.6 * W.SLOTS_PER_DAY), int(4.9 * W.SLOTS_PER_DAY), 3))
    f = figures(sel)
    if b == "EM3.12.0":
        f["carve"] = carve_margins(sel, S.network_events())
    return f


def search(net_salt, max_salt=300, quiet=False):
    insts = fleet(net_salt)
    out, margins = {}, []
    for b in W.RELEASES:
        for salt in range(max_salt):
            f = run(insts, b, salt)
            if ok(b, f) and all(abs(f["m"]["col"] - x) >= 0.04 for x in margins):
                margins.append(f["m"]["col"])
                out[b] = salt
                if not quiet:
                    print("  %s salt %d n %d k %d rh %.3f se %s m %s" % (b, salt, f["n"], f["k"], f["rh"],
                          {k: round(v, 3) for k, v in f["se"].items()}, {k: round(v, 3) for k, v in f["m"].items()}))
                break
        else:
            if not quiet:
                print("  NO SALT", b)
            return None
    return out


def structure(net_salt):
    """The week's events have the shape the design names: exactly one pilot collector fails with most
    of its EM3.12.2 meters caught, one or two of the newer-suburb collectors fail, no collector in the
    older suburbs or on the Wave 8 list fails, and no access point carrying PX5 full-week meters fails."""
    W.NET_SALT = net_salt
    ids = S.network_ids()
    grp = {x: (fam, g) for (fam, g), lst in ids.items() for x in lst}
    ev = S.network_events()
    em = [e for e in ev if grp[e[0]][0] == "EM3"]
    px = [e for e in ev if grp[e[0]][0] == "PX5"]
    pil = [e for e in em if grp[e[0]][1] == "pilot"]
    new = [e for e in em if grp[e[0]][1] == "new"]
    bad = [e for e in em if grp[e[0]][1] in ("old", "w8")]
    pxo = [e for e in px if grp[e[0]][1] != "w7"]
    if not (len(pil) == 1 and pil[0][2] > 0.8 and 1 <= len(new) <= 2 and not bad and 3 <= len(em) <= 6 and not pxo and len(px) <= 1):
        return False
    insts = STRUCT_FLEET[0] or S.make_fleet()
    STRUCT_FLEET[0] = insts
    n22 = sum(1 for i in insts if i.group == "full" and i.build_start == "EM3.12.2" and i.parent == pil[0][0])
    return n22 >= 22


STRUCT_FLEET = [None]


if __name__ == "__main__":
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 3000)
    for ns in range(lo, hi):
        if not structure(ns):
            continue
        W.SALT.clear()
        print("net salt", ns)
        res = search(ns)
        if res:
            print("FOUND", ns, res)
            break
