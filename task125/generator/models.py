"""The office's estimator and the analyses: the quarter's sample, raking to the population controls, the published
rates, and the visit limit's gap path under each construction a solver can make (the golden and the ladder's rungs).
Works on the simulation (for the build and its checks) through the same functions the verifier re-implements on the
shipped files."""
import numpy as np

import world as W

AGE_SHARE = np.array([0.156, 0.171, 0.160, 0.153, 0.146, 0.115, 0.099])
FEMALE = np.array([0.490, 0.500, 0.505, 0.510, 0.515, 0.525, 0.575])


def controls(q):
    """Population aged 15 and over by region and by age group and sex (persons), quarter q."""
    t = W.qindex(q) - W.qindex(W.FIRST_Q)
    total = W.POP15 * (1 + W.POP_GROWTH_Q) ** t
    if W.qindex(q) >= W.qindex((2026, 1)):          # the 2025-based estimates from 2026
        total *= 1.0062
    shares = np.array([r[2] for r in W.REGIONS])
    region = np.round(total * shares / shares.sum())
    cells = []
    for a, f in zip(AGE_SHARE, FEMALE):
        cells += [total * a * (1 - f), total * a * f]
    cells = np.round(np.array(cells))
    cells[-1] += region.sum() - cells.sum()           # the two margins agree to the person
    return region, cells


def rake(region, cell, q, base=None, iters=200):
    """Iterative proportional fitting of person weights to the region and age-sex margins."""
    rt, ct = controls(q)
    w = np.ones(region.size) if base is None else base.astype(float).copy()
    for _ in range(iters):
        s = np.bincount(region, w, len(rt))
        w *= (rt / s)[region]
        s = np.bincount(cell, w, len(ct))
        f = ct / s
        w *= f[cell]
        if np.max(np.abs(f - 1)) < 1e-12:
            break
    return w


def rates(status, w):
    e = w[status == 0].sum()
    u = w[status == 1].sum()
    return 100 * u / (e + u), 100 * e / w.sum()


def cell_index(age, sex):
    g = np.searchsorted(np.array(W.AGE_EDGES[1:]), age, side="right")
    return 2 * g + (sex - 1)


def quarter_sample(intakes, q, drop_waves=(), drop_rule=None):
    """Persons of quarter q's five intakes; households of the intakes at the waves in drop_waves are removed where
    drop_rule(intake) is true (the households a three-visit limit would not have recruited)."""
    parts = []
    for w in range(1, W.WAVES + 1):
        c = W.qnext(q, -(w - 1))
        d = intakes.get(c)
        if d is None:
            continue
        keep_hh = d["resp"][w - 1].copy()
        if w in drop_waves:
            keep_hh &= ~drop_rule(d)
        m = keep_hh[d["hh"]] & d["present"][w - 1]
        age = d["ages_q"][w - 1][m]
        parts.append(dict(region=d["region"][d["hh"][m]], cell=cell_index(age, d["sex"][m]),
                          status=d["statuses"][w - 1][m], wave=np.full(m.sum(), w), late=(d["need"] > 3)[d["hh"][m]],
                          intake=np.full(m.sum(), W.qindex(c)), person=np.nonzero(m)[0]))
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}


def published(intakes, q, **kw):
    s = quarter_sample(intakes, q, **kw)
    return rates(s["status"], rake(s["region"], s["cell"], q))


LATE = lambda d: d["need"] > W.CAP_VISITS


def positions(k):
    """Waves the two capped intakes (July to September and October to December 2026) occupy k quarters after
    July to September 2026."""
    a = 1 + k                       # the July to September 2026 intake
    b = k                           # the October to December 2026 intake (from k = 1)
    return tuple(x for x in (a, b) if 1 <= x <= W.WAVES)


FORWARD = [W.qnext(W.LIMIT_FROM, k) for k in range(5)]     # 2026Q3 .. 2027Q3


def gap_path(intakes, template=W.TEMPLATE_Q, reweight="rake", carry="panel", wave1_only=False):
    """Each forward quarter's gap (published less six-visit), unemployment and employment rate, points.
    reweight: 'rake' re-rakes after dropping, 'keep' keeps the template's final weights.
    carry: 'panel' drops the late households in every wave a capped intake occupies; wave1_only drops them only in
    the wave-1 position while the limit runs."""
    s = quarter_sample(intakes, template)
    w0 = rake(s["region"], s["cell"], template)
    base = rates(s["status"], w0)
    out = []
    for k, q in enumerate(FORWARD):
        pos = positions(k)
        if wave1_only:
            pos = (1,) if W.capped(q) else ()
        drop = np.isin(s["wave"], pos) & s["late"]
        if reweight == "rake":
            w = rake(s["region"][~drop], s["cell"][~drop], template)
            r = rates(s["status"][~drop], w)
        else:
            r = rates(s["status"][~drop], w0[~drop])
        out.append((r[0] - base[0], r[1] - base[1]))
    return out


def constant_gap_path(intakes, template=W.TEMPLATE_Q):
    """Rung 1: the wave-1 gap of the template, carried unchanged into each later wave a capped intake occupies,
    each wave weighted by its share of the quarter's economically active (or population)."""
    s = quarter_sample(intakes, template)
    w0 = rake(s["region"], s["cell"], template)
    base = rates(s["status"], w0)
    w1 = s["wave"] == 1
    act = (s["status"] <= 1)
    share_act = np.array([(w0 * act)[s["wave"] == w].sum() for w in range(1, 6)]) / (w0 * act).sum()
    share_pop = np.array([w0[s["wave"] == w].sum() for w in range(1, 6)]) / w0.sum()
    # the wave-1 rates with and without the late households, on the wave's own weights
    def wrates(mask):
        return rates(s["status"][mask], w0[mask])
    full, cut = wrates(w1), wrates(w1 & ~s["late"])
    du, de = cut[0] - full[0], cut[1] - full[1]
    out = []
    for k, q in enumerate(FORWARD):
        pos = positions(k)
        out.append((sum(du * share_act[p - 1] for p in pos), sum(de * share_pop[p - 1] for p in pos)))
    return out


