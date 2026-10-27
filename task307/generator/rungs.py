"""The cheap routes to the call, measured on the clean truth."""
import numpy as np
import params as P, world, net, solve


def fw_k(links, od, cap, t0, al, be, k):
    asg = net.Assign(links)
    agg = solve.aggregate(od)
    tt = lambda v: t0 * (1 + al * (v / cap) ** be)
    v = asg.aon(tt(np.zeros(len(t0))), agg)
    for _ in range(k):
        y = asg.aon(tt(v), agg)
        lo, hi = 0.0, 1.0
        for _ in range(50):
            m = (lo + hi) / 2
            if np.sum((y - v) * tt(v + m * (y - v))) > 0:
                hi = m
            else:
                lo = m
        v = v + (lo + hi) / 2 * (y - v)
    return v, tt(v)


def msa_k(links, od, cap, t0, al, be, k):
    asg = net.Assign(links); agg = solve.aggregate(od)
    tt = lambda v: t0 * (1 + al * (v / cap) ** be)
    v = asg.aon(tt(np.zeros(len(t0))), agg)
    for n in range(1, k + 1):
        y = asg.aon(tt(v), agg)
        v = v + (y - v) / (n + 1)
    return v, tt(v)


def routes(o=None):
    o = o or solve.run()
    links, cap, t0, al, be, tabs = o["links"], o["cap"], o["t0"], o["al"], o["be"], o["tabs"]
    out = {}
    out["fixed no-build volumes"] = {c: r["annual_fixed"] for c, r in o["proj"].items()}
    out["equilibrium (golden)"] = {c: r["annual"] for c, r in o["proj"].items()}
    out["equilibrium, AM peak only"] = {c: r["AM"]["saved"] * P.ANNUAL_FACTOR for c, r in o["proj"].items()}
    asg = net.Assign(links)
    # one all-or-nothing re-route at no-build times on the build network
    aon = {}
    for pr in P.PROJECTS:
        c2 = solve.project_caps(links, cap, pr); s = 0
        for per, od in tabs.items():
            nb = o["nobuild"][per]
            tt2 = t0 * (1 + al * (nb["v"] / c2) ** be)
            y = asg.aon(tt2, solve.aggregate(od))
            s += nb["vht"] - solve.vht(y, t0 * (1 + al * (y / c2) ** be), sum(od.values()))
        aon[pr["code"]] = s * P.ANNUAL_FACTOR
    out["one all-or-nothing re-route"] = aon
    for name, f, k in [("Frank-Wolfe, 3 iterations", fw_k, 3), ("Frank-Wolfe, 10 iterations", fw_k, 10),
                       ("Frank-Wolfe, 50 iterations", fw_k, 50), ("MSA, 10 iterations", msa_k, 10), ("MSA, 50 iterations", msa_k, 50)]:
        res = {}
        base = {}
        for per, od in tabs.items():
            v, t = f(links, od, cap, t0, al, be, k); base[per] = solve.vht(v, t, sum(od.values()))
        for pr in P.PROJECTS:
            c2 = solve.project_caps(links, cap, pr); s = 0
            for per, od in tabs.items():
                v, t = f(links, od, c2, t0, al, be, k); s += base[per] - solve.vht(v, t, sum(od.values()))
            res[pr["code"]] = s * P.ANNUAL_FACTOR
        out[name] = res
    cost = {p["code"]: p["cost_m"] for p in P.PROJECTS}
    out["fixed volumes, per million dollars"] = {c: v / cost[c] for c, v in out["fixed no-build volumes"].items()}
    return out


if __name__ == "__main__":
    for name, r in routes().items():
        best = max(r, key=r.get)
        print("%-38s -> %s   %s" % (name, best, "  ".join("%s %.0f" % (c, v) for c, v in r.items())))
