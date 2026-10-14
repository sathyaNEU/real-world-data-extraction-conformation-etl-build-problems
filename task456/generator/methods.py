"""Every route from the conformed hospital-days to the regions the compact activates, and the three asks, all
computed from the bundle through conform.Pack.

The golden: a two-class latent class model of the three feeds (each feed's chance of flagging a full day and an
ordinary day the same for every hospital, the share of full days free by region), fitted by maximum likelihood;
each region's share is its estimated share of full days, and a region activates at one in three or more."""
import collections

import numpy as np

import conform as CF
import lca
import world as W

G = W.RCODE


def arrays(rows):
    Y = np.array([[np.nan if r[4] is None else r[4], r[5], r[6]] for r in rows], dtype=float)
    return Y, np.array([r[0] for r in rows]), np.array([r[1] for r in rows])


def activated(share):
    return [g for g in G if share[g] >= W.THRESHOLD]


def golden(pk):
    rows = pk.hospital_days(W.WINDOW_START, W.WINDOW_END)
    Y, reg, hosp = arrays(rows)
    m = lca.fit(Y, reg, G, True)
    return dict(rows=rows, Y=Y, reg=reg, hosp=hosp, share=m["share"], s=m["s"], f=m["f"], post=m["post"],
                loglik=m["loglik"], regions=activated(m["share"]))


def tenth(x):
    """to the nearest ten per cent, as a whole percentage"""
    return int(10 * np.floor(10 * x + 0.5))


def rules(gd):
    out = {}
    for r in lca.monotone_rules():
        sh = lca.rule_share(gd["Y"], gd["reg"], G, r)
        out[lca.rule_name(r)] = dict(share=sh, regions=activated(sh))
    return out


NAMED = {"any feed": "any feed shows the day full",
         "two of three": "two of the three feeds agree",
         "C+BC+A+AC+AB+ABC": "the census or a decline, the board only with one of them",
         "B+BC+AB+ABC": "the board alone",
         "A+AC+AB+ABC": "the census alone",
         "C+BC+AC+ABC": "the transfer center's declines alone"}


def variants(pk, gd):
    """the model's variants: hospital-level shares, one statewide share (posterior means by region), the most
    likely state per day counted (by region and statewide), a missing census report read as no flag, feed rates
    from the whole season with the window's shares free, Beta(2,2) priors"""
    Y, reg, hosp = gd["Y"], gd["reg"], gd["hosp"]
    out = {}
    mh = lca.fit(Y, hosp, sorted(set(hosp)), True)
    out["hospital-level shares"] = {g: float(mh["post"][reg == g].mean()) for g in G}
    mp = lca.fit(Y, reg, G, False)
    out["one statewide share, posterior means"] = {g: float(mp["post"][reg == g].mean()) for g in G}
    out["most likely state, by region"] = {g: float((gd["post"][reg == g] > 0.5).mean()) for g in G}
    out["most likely state, one statewide share"] = {g: float((mp["post"][reg == g] > 0.5).mean()) for g in G}
    Y0 = np.where(np.isnan(Y), 0, Y)
    out["missing census read as no flag"] = lca.fit(Y0, reg, G, True)["share"]
    srows = pk.hospital_days(W.SEASON_START, W.SEASON_END)
    Ys, sreg, _ = arrays(srows)
    per = np.array([r[0] + ("W" if W.WINDOW_START <= r[3] <= W.WINDOW_END else "P") for r in srows])
    ms = lca.fit(Ys, per, sorted(set(per)), True)
    out["season-wide feed rates"] = {g: ms["share"][g + "W"] for g in G}
    out["Beta(2,2) priors"] = fit_prior(Y, reg)
    return out


def fit_prior(Y, reg, a=2.0, b=2.0, iters=6000):
    pi = {g: 0.3 for g in G}
    s, f = np.array([0.5, 0.8, 0.4]), np.array([0.05, 0.2, 0.05])
    obs = ~np.isnan(Y)
    Yz = np.nan_to_num(Y)
    for _ in range(iters):
        l1 = np.prod(np.where(obs, np.where(Yz == 1, s, 1 - s), 1), 1)
        l0 = np.prod(np.where(obs, np.where(Yz == 1, f, 1 - f), 1), 1)
        pr = np.array([pi[g] for g in reg])
        w = pr * l1 / (pr * l1 + (1 - pr) * l0)
        pi = {g: float((w[reg == g].sum() + a - 1) / ((reg == g).sum() + a + b - 2)) for g in G}
        s = np.array([((w * Yz[:, j] * obs[:, j]).sum() + a - 1) / ((w * obs[:, j]).sum() + a + b - 2) for j in range(3)])
        f = np.array([(((1 - w) * Yz[:, j] * obs[:, j]).sum() + a - 1) / (((1 - w) * obs[:, j]).sum() + a + b - 2)
                      for j in range(3)])
    return pi


# ------------------------------------------------------------------------------------------------- the asks
def ask_a(pk, **kw):
    """adult ICU patients placed in a hospital outside their own region, requests opened in the 28 days, by the
    region they left"""
    pl = pk.placements(W.WINDOW_START, W.WINDOW_END, **kw)
    c = collections.Counter(p["sender_region"] for p in pl if p["sender_region"] and p["sender_region"] != p["to_region"])
    return {g: c.get(g, 0) for g in G}


def ask_a_patient_dedup(pk):
    pl = pk.placements(W.WINDOW_START, W.WINDOW_END)
    seen, c = set(), collections.Counter()
    for p in sorted(pl, key=lambda p: (p["opened"], p["case"])):
        if p["patient"] in seen:
            continue
        seen.add(p["patient"])
        if p["sender_region"] and p["sender_region"] != p["to_region"]:
            c[p["sender_region"]] += 1
    return {g: c.get(g, 0) for g in G}


def ask_a_receiving(pk):
    pl = pk.placements(W.WINDOW_START, W.WINDOW_END)
    c = collections.Counter(p["to_region"] for p in pl if p["sender_region"] and p["sender_region"] != p["to_region"])
    return {g: c.get(g, 0) for g in G}


def by_region(pk, hours):
    c = collections.defaultdict(float)
    for lic, v in hours.items():
        c[pk.region[lic]] += v
    return {g: c.get(g, 0.0) for g in G}


def diversion(s, r):
    return s == "Divert" or (s == "Advisory" and r == "EMS diversion")


def ask_b(pk, keep=diversion):
    """hours each region's emergency departments asked ambulances to divert in the 28 days"""
    return by_region(pk, pk.hours(CF.ED_LABELS, keep, W.WINDOW_START, W.WINDOW_END))


def ask_c(pk, keep=lambda s, r: s == "Closed"):
    """hours each region's adult ICU lines were Closed in the 28 days before the window"""
    return by_region(pk, pk.hours(CF.ICU_LABELS, keep, W.PRIOR_START, W.PRIOR_END))


def ask_c_current_code(pk):
    saved = pk.by_old
    pk.by_old, pk._events = pk.by_new, None
    try:
        return ask_c(pk)
    finally:
        pk.by_old, pk._events = saved, None


def whole(d):
    return {g: int(np.floor(v + 0.5)) for g, v in d.items()}
