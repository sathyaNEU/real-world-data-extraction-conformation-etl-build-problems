"""Every route to the eligible households, computed from conformed inputs: the two surveys' weighted division-by-band
shares, the published households, and the screening pilot's complete screens by band. Used by the centring in
build.py, by golden.py for the deliverables and by checks.py for the ladder, the convergence and the mess."""
import math

import world as W

# the fusions that keep both surveys' shares; each must file the golden's cells, totals and staffing
FAMILY = ("or_band", "or_mh", "or_mh_div", "or_pooled", "rr_equipment", "or_div", "or_div_mh", "or_div_mean")


def joint(p, q, psi):
    if abs(psi - 1) < 1e-12:
        return p * q
    a = psi - 1
    b = -(1 + (psi - 1) * (p + q))
    c = psi * p * q
    return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)


def ipf(p, q, seed, iters=2000, tol=1e-13):
    """Rake a 2x2 seed table (both, burden only, equipment only, neither) to margins p and q; returns the both-cell."""
    t = [float(v) for v in seed]
    s = sum(t)
    t = [v / s for v in t]
    for _ in range(iters):
        r1 = t[0] + t[1]
        t[0], t[1] = t[0] * p / r1, t[1] * p / r1
        r0 = t[2] + t[3]
        t[2], t[3] = t[2] * (1 - p) / r0, t[3] * (1 - p) / r0
        c1 = t[0] + t[2]
        t[0], t[2] = t[0] * q / c1, t[2] * q / c1
        c0 = t[1] + t[3]
        t[1], t[3] = t[1] * (1 - q) / c0, t[3] * (1 - q) / c0
        if abs(t[0] + t[1] - p) < tol:
            break
    return t[0]


def odds(t):
    return t[0] * t[3] / (t[1] * t[2])


def mantel_haenszel(tabs):
    return sum(t[0] * t[3] / sum(t) for t in tabs) / sum(t[1] * t[2] / sum(t) for t in tabs)


def routes(N, p, q, tabs, tabs_div=None):
    """N, p, q: {(division, band): value} over the eligible bands; tabs: {band: (both, burden only, equipment only,
    neither)} from the pilot's complete screens. Returns {route: {(division, band): eligible households}}."""
    out = {}
    pooled = [sum(tabs[b][k] for b in W.ELIGIBLE_BANDS) for k in range(4)]
    psi_b = {b: odds(tabs[b]) for b in W.ELIGIBLE_BANDS}
    psi_mh = mantel_haenszel([tabs[b] for b in W.ELIGIBLE_BANDS])
    psi_mhd = mantel_haenszel(list(tabs_div.values())) if tabs_div else psi_mh
    psi_c = odds(pooled)
    psi_d, psi_dm, psi_gm = {}, {}, {}
    if tabs_div:
        for d in {k[0] for k in tabs_div}:
            psi_dm[d] = mantel_haenszel([tabs_div[(d, b)] for b in W.ELIGIBLE_BANDS])
            for b in W.ELIGIBLE_BANDS:
                psi_d[(d, b)] = odds(tabs_div[(d, b)])
        for b in W.ELIGIBLE_BANDS:
            ls = [math.log(v) for (d, bb), v in psi_d.items() if bb == b]
            psi_gm[b] = math.exp(sum(ls) / len(ls))
    for key in N:
        d, b = key
        pp, qq, n, t = p[key], q[key], N[key], tabs[b]
        tt = sum(t)
        y1x1 = t[0] / (t[0] + t[1])
        y1x0 = t[2] / (t[2] + t[3])
        x1y1 = t[0] / (t[0] + t[2])
        x1y0 = t[1] / (t[1] + t[3])
        lift = (t[0] / tt) / (((t[0] + t[1]) / tt) * ((t[0] + t[2]) / tt))
        rr = y1x1 / y1x0
        p0 = qq / (pp * rr + 1 - pp)
        vals = {
            "golden": ipf(pp, qq, t),                       # the pilot's band table raked to both surveys' shares
            "independence": pp * qq,                         # the default path: the two shares multiplied
            "pilot_shares": t[0] / tt,                       # the pilot's own share with both traits
            "energy_x_pilot": pp * y1x1,                     # energy survey's burden share x pilot's equipment rate
            "health_x_pilot": qq * x1y1,                     # health survey's equipment share x pilot's burden rate
            "lift": pp * qq * lift,                          # the product scaled by the pilot's joint over its product
            "or_band": joint(pp, qq, psi_b[b]),
            "or_mh": joint(pp, qq, psi_mh),
            "or_mh_div": joint(pp, qq, psi_mhd),
            "or_pooled": joint(pp, qq, psi_c),
            "rr_equipment": pp * rr * p0,                    # the pilot's equipment rate ratio kept, both shares kept
        }
        if tabs_div:                                         # each pilot division on its own odds ratio, the rest on
            own = key in psi_d                               # the band's (or the two divisions' mean)
            vals["or_div"] = joint(pp, qq, psi_d[key]) if own else vals["golden"]
            vals["or_div_mh"] = joint(pp, qq, psi_dm[d]) if own else vals["golden"]
            vals["or_div_mean"] = joint(pp, qq, psi_d[key]) if own else joint(pp, qq, psi_gm[b])
        for k, v in vals.items():
            out.setdefault(k, {})[key] = n * v
    return out, dict(psi_band=psi_b, psi_mh=psi_mh, psi_mh_div=psi_mhd, psi_pooled=psi_c, psi_div=psi_d,
                     psi_div_mh=psi_dm)


def division_totals(cell_values):
    out = {d: 0.0 for d in W.DIV_NAMES}
    for (d, b), v in cell_values.items():
        out[d] += v
    return out


def caseworkers(total):
    return int(math.ceil(total / W.CASELOAD - 1e-9))


def independence_by_division(N, p, q):
    """The cruder default: each division's pooled burden and equipment shares multiplied (bands collapsed)."""
    out = {}
    for d in W.DIV_NAMES:
        n = sum(N[(d, b)] for b in W.ELIGIBLE_BANDS)
        pp = sum(N[(d, b)] * p[(d, b)] for b in W.ELIGIBLE_BANDS) / n
        qq = sum(N[(d, b)] * q[(d, b)] for b in W.ELIGIBLE_BANDS) / n
        out[d] = n * pp * qq
    return out
