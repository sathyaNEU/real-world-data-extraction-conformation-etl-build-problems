"""Every route to the redesign's effect on the published unemployment rate, read on month x region x rotation group
cells, and the restated trigger, the designation, the back series and the fourth-quarter dwelling count built on it.

The design-implied route: each month in sample on the redesigned questionnaire against the same month in sample on
the previous one (month and region held fixed, the previous questionnaire's month-in-sample pattern estimated from
every month before July 2025), the six month-in-sample effects averaged as the published estimate averages the six
rotation groups."""
import numpy as np

import world as W

NEWM = np.array([[1 if W.redesigned(t, g) else 0 for g in range(6)] for t in range(W.T)])
MISM = np.array([[W.mis(t, g) for g in range(6)] for t in range(W.T)])


def cells_from(une, lab):
    """month x region x group rate (per cent) and weighted labour force from weighted counts"""
    une, lab = np.asarray(une, float), np.asarray(lab, float)
    t, r, g = np.meshgrid(np.arange(W.T), np.arange(W.R), np.arange(6), indexing="ij")
    return dict(t=t.ravel(), r=r.ravel(), g=g.ravel(), y=(100.0 * une / lab).ravel(), w=lab.ravel(),
                new=NEWM[t, g].ravel(), m=MISM[t, g].ravel())


def arm_gap(F, months=None):
    """January to May of the phase-in (July to November 2025): the groups on the redesigned questionnaire against
    those still on the previous one, month by month, averaged"""
    months = months or range(W.PHASE, W.PHASE + 5)
    out = []
    for k in months:
        a = F["t"] == k
        n1, n0 = a & (F["new"] == 1), a & (F["new"] == 0)
        out.append((F["y"][n1] * F["w"][n1]).sum() / F["w"][n1].sum() - (F["y"][n0] * F["w"][n0]).sum() / F["w"][n0].sum())
    return float(np.mean(out))


def fe(F, cols, use, weighted=True, mis_fe=True, by_region=True):
    t, r = F["t"][use], F["r"][use]
    key = t * W.R + r if by_region else t
    _, idx = np.unique(key, return_inverse=True)
    X = [np.eye(idx.max() + 1)[idx]]
    if mis_fe:
        X.append(np.column_stack([(F["m"][use] == j) for j in range(2, 7)]).astype(float))
    X += [np.asarray(c)[use][:, None].astype(float) for c in cols]
    X = np.hstack(X)
    sw = np.sqrt(F["w"][use] / F["w"][use].mean()) if weighted else np.ones(int(use.sum()))
    beta = np.linalg.lstsq(X * sw[:, None], F["y"][use] * sw, rcond=None)[0]
    return beta[-len(cols):]


def mis_effects(F, use=None, weighted=True, by_region=True):
    """the redesign's effect at each month in sample (1 to 6)"""
    use = np.ones(len(F["y"]), bool) if use is None else use
    return fe(F, [F["new"] * (F["m"] == j) for j in range(1, 7)], use, weighted, by_region=by_region)


def golden_break(F):
    e = mis_effects(F)
    return float(e.mean()), e


def variants(F):
    """the design-implied break under every reasonable implementation: the months before the phase-in that set the
    month-in-sample pattern (24, 36 or all 42), December 2025 kept or left out, weighted or unweighted cells, region
    and month or month alone held fixed, each month-in-sample effect free or the second to sixth sharing one"""
    out = {}
    for pre in (24, 36, 42):
        for dec in (True, False):
            use = F["t"] >= W.PHASE - pre
            if not dec:
                use = use & (F["t"] != W.PHASE + 5)
            for wt in (True, False):
                for byr in (True, False):
                    e = mis_effects(F, use, wt, byr)
                    out[(pre, dec, wt, byr, "each")] = float(e.mean())
                    b = fe(F, [F["new"], F["new"] * (F["m"] >= 2)], use, wt, by_region=byr)
                    out[(pre, dec, wt, byr, "first/later")] = float(b[0] + 5.0 / 6.0 * b[1])
    return out


def wrong_routes(F, nat):
    """the default and the other easy routes, each a number of points"""
    out = {"R0 none": 0.0, "R1 arm gap": arm_gap(F)}
    use = F["t"] >= W.PHASE - 36
    out["R1 rotation letter held fixed"] = float(
        fe(F, [F["new"]] + [(F["g"] == j) for j in range(1, 6)], use, True, mis_fe=False)[0])
    single = {}
    for pre in (24, 36, 42):
        for wt in (True, False):
            for byr in (True, False):
                u = F["t"] >= W.PHASE - pre
                single[(pre, wt, byr)] = float(fe(F, [F["new"]], u, wt, by_region=byr)[0])
    out["R2 one effect"] = single
    later = {}
    for pre in (24, 36, 42):
        for wt in (True, False):
            u = F["t"] >= W.PHASE - pre
            later[(pre, wt)] = float(mis_effects(F, u, wt)[1:].mean())
    out["R3 continuing households"] = later
    out["event 2026 against 2024"] = float(np.mean(nat[W.Y26:]) - np.mean(nat[W.Y26 - 24:W.Y26 - 12]))
    out["event second half 2025 against 2024"] = None
    return out


def restated(break_points):
    return round(W.TRIGGER + round(break_points + 1e-9, 1), 1)


def averages_2026(reg_published_1dp):
    """each region's 2026 average: the mean of its twelve monthly rates as published (one decimal place)"""
    return np.asarray(reg_published_1dp)[W.Y26:].mean(0)


def designated(avg, trigger):
    return [W.RCODE[i] for i in range(W.R) if avg[i] >= trigger - 1e-9]


def back_series(reg_published_1dp, nat_published_1dp, break_1dp):
    """the series on the redesigned basis (the note's section 4): months before July 2025 restated by adding the change
    as determined (one decimal place) to the rate as published, every region alike; July to November 2025, both
    questionnaires in the field, carried as published; from December 2025 as published"""
    reg = np.asarray(reg_published_1dp, float)
    nat = np.asarray(nat_published_1dp, float)
    add = np.where(np.arange(W.T) < W.PHASE, break_1dp, 0.0)
    return np.round(reg + add[:, None], 1), np.round(nat + add, 1), add


def dwellings_q4(rows, psu_region):
    """responding dwellings in October to December 2026, each dwelling once: a dwelling is its slot together with the
    month it entered the sample; responding means a complete (11) or partial (12) interview"""
    seen = set()
    for r in rows:
        if r["outcome"] in (11, 12):
            seen.add((r["dwelling_ref"], r["in_sample_from"], psu_region[r["psu"]]))
    by = {c: 0 for c in W.RCODE}
    for _, _, c in seen:
        by[c] += 1
    by["all"] = sum(by[c] for c in W.RCODE)
    return by


def dwellings_q4_stops(rows, psu_region):
    """the ask's wrong stops: slots counted as dwellings; responding interviews counted; every dwelling counted
    whether it responded or not; complete interviews only"""
    def count(keyf, keep):
        s = set()
        for r in rows:
            if keep(r):
                s.add(keyf(r))
        by = {c: 0 for c in W.RCODE}
        for k in s:
            by[k[-1]] += 1
        by["all"] = sum(by[c] for c in W.RCODE)
        return by
    reg = lambda r: psu_region[r["psu"]]
    return {
        "slots": count(lambda r: (r["dwelling_ref"], reg(r)), lambda r: r["outcome"] in (11, 12)),
        "interviews": count(lambda r: (r["dwelling_ref"], r["contact_month"], reg(r)), lambda r: r["outcome"] in (11, 12)),
        "every dwelling": count(lambda r: (r["dwelling_ref"], r["in_sample_from"], reg(r)), lambda r: True),
        "complete only": count(lambda r: (r["dwelling_ref"], r["in_sample_from"], reg(r)), lambda r: r["outcome"] == 11),
        "eligible": count(lambda r: (r["dwelling_ref"], r["in_sample_from"], reg(r)), lambda r: r["outcome"] not in (31, 32, 33)),
    }
