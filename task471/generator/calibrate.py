"""Seed search for the world: the dual-system allocation and the golden must differ in several regions, the golden's
largest-remainder cut must clear its neighbours, and every reading of the golden must agree.

    python3 task471/generator/calibrate.py 471          one seed, the full report
    python3 task471/generator/calibrate.py 471 520      a search, one line a seed
"""
import sys

import methods as M
import sim as S
import world as W


def world_data(seed):
    nat = S.national(seed)
    reg = S.regional(nat, seed)
    cov = S.coverage(seed)
    cnt = S.counts(reg, cov, seed)
    rl = S.roll(reg, cov, seed)
    return data_from(nat, cnt, rl), nat, reg, cov, cnt


def data_from(nat, cnt, rl):
    """the estimators' data structure (methods.py) straight from the simulation, before any file is written"""
    d = {"census": {}, "e": {}, "p": {}, "roll": {c: 0 for c in W.CODES}}
    for k, v in cnt["census"].items():
        d["census"][k] = (v["correct"] + v["erroneous"] + v["imputed"], v["imputed"])
    for (c, mb, s, a, cls, inc, inp, pid) in cnt["p_sample"]:
        if inc:
            e = d["e"].setdefault((c, s, a), [0, 0])
            e[0] += 1
            e[1] += 1
        if inp:
            p = d["p"].setdefault((c, s, a), [0, 0])
            p[0] += 1
            p[1] += int(inc)
    for (c, mb, s, a, pid) in cnt["e_sample"]:
        e = d["e"].setdefault((c, s, a), [0, 0])
        e[0] += 1
    for (c, s, a), k in rl.items():
        d["roll"][c] += k
    d["births"], d["deaths"] = nat["births"], nat["deaths"]
    d["departures"], d["arrivals"] = nat["departures"], nat["arrivals"]
    return d


def by_miss(d, est, fac):
    """the national extra men of each young age group shared out in proportion to each region's men the census missed
    on the dual-system estimate"""
    cells = M.cells(d)
    out = M.adults(est)
    for g in W.YOUNG_GROUPS:
        extra = sum(v for (c, s, gg), v in est.items() if s == "M" and gg == g) * (fac[g] - 1)
        missed = {c: est[(c, "M", g)] - (cells[(c, "M", g)][0] - cells[(c, "M", g)][1]) for c in W.CODES}
        tot = sum(missed.values())
        for c in W.CODES:
            out[c] += extra * missed[c] / tot
    return out


def single_years(d, est, lo=18, hi=49):
    """the correction by single year of age: each cell's estimate shared over its single years by the census counts,
    and the men of each year brought to demographic analysis's sex ratio for that year against the women's"""
    cells = M.cells(d)
    da = M.demographic(d)
    by_age = {(c, s, a): cnt * est[(c, s, W.age_group(a))] / cells[(c, s, W.age_group(a))][0]
              for (c, s, a), (cnt, imp) in d["census"].items()}
    out = M.adults(est)
    for a in range(lo, hi + 1):
        m = sum(v for (c, s, aa), v in by_age.items() if s == "M" and aa == a)
        f = sum(v for (c, s, aa), v in by_age.items() if s == "F" and aa == a)
        fac = da[("M", a)] / da[("F", a)] * f / m
        for c in W.CODES:
            out[c] += by_age[(c, "M", a)] * (fac - 1)
    return out


def pooled(d, key):
    """dual-system estimates on pooled adult cells: each cell's census count raised by its pool's estimate over its
    pool's count"""
    cells = M.cells(d)
    pools = {}
    for (c, s, g), v in cells.items():
        if g[0] < 18:
            continue
        o = pools.setdefault(key(c, s, g), [0] * 6)
        for i in range(6):
            o[i] += v[i]
    return {(c, s, g): v[0] * M.dse(pools[key(c, s, g)]) / pools[key(c, s, g)][0]
            for (c, s, g), v in cells.items() if g[0] >= 18}


def census_counts(d):
    return {k: float(v[0]) for k, v in M.cells(d).items()}


def national_ratio(d):
    return pooled(d, lambda c, s, g: (s, g))


def rungs(d):
    """adults per region on each rung: R0 the census counts, R1 one national dual-system ratio per sex and age group,
    R2 dual-system estimates within the survey's cells (the default path), R3 the golden"""
    est = M.dse_cells(d)
    return {"R0 census counts": M.adults(census_counts(d)), "R1 one national ratio": M.adults(national_ratio(d)),
            "R2 dual-system cells": M.adults(est), "R3 golden": M.adults(est, M.factors(d, est))}


def wrong_paths(d):
    """the default path's other cuts and slips, each alone and with the correction on top: none may land on the golden"""
    out = {}
    cuts = (("cells pooled by region", lambda c, s, g: c), ("cells pooled by region and sex", lambda c, s, g: (c, s)),
            ("cells pooled by region and age", lambda c, s, g: (c, g)))
    for nm, key in cuts:
        e = pooled(d, key)
        out[nm] = M.adults(e)
        out[nm + ", corrected"] = M.adults(e, M.factors(d, e))
    for nm, kw in (("errors kept", {"erroneous": False}), ("imputed kept", {"imputed": False}),
                   ("errors and imputed kept", {"erroneous": False, "imputed": False})):
        e = M.dse_cells(d, **kw)
        out[nm] = M.adults(e)
        out[nm + ", corrected"] = M.adults(e, M.factors(d, e))
    for nm, e in (("census counts", census_counts(d)), ("one national ratio", national_ratio(d))):
        out[nm + ", corrected"] = M.adults(e, M.factors(d, e))
    return out


def variants(d):
    """the golden's readings (SF11 to SF15 and the bands corrected): each must file the golden"""
    est = M.dse_cells(d)
    fac = M.factors(d, est)
    band = M.factors(d, est, groups=[(18, 49)])[(18, 49)]
    return {
        "the men's demographic total (SF13)": M.adults(est, M.factors(d, est, mode="total")),
        "every adult age but 65 and over (SF14)": M.adults(est, M.factors(d, est, groups=W.ADULT_GROUPS[:-1])),
        "every adult age (SF14)": M.adults(est, M.factors(d, est, groups=W.ADULT_GROUPS)),
        "one band 18 to 49": M.adults(est, {g: band for g in W.YOUNG_GROUPS}),
        "the end of 2024 (SF12)": M.adults(est, M.factors(d, est, to_census_day=False)),
        "nobody born before 4 March (SF15)": M.adults(est, M.factors(d, est, born_before=0.0)),
        "half born before 4 March (SF15)": M.adults(est, M.factors(d, est, born_before=0.5)),
        "the extra men shared on the census's misses (SF11)": by_miss(d, est, fac),
        "single years of age 18 to 49": single_years(d, est),
        "single years of age 20 to 44": single_years(d, est, 20, 44),
    }


def allocation(d, adults):
    return M.allocate({c: adults[c] - d["roll"][c] for c in W.CODES})


def run(seed, quiet=False):
    d, nat, reg, cov, cnt = world_data(seed)
    roll = d["roll"]
    est = M.dse_cells(d)
    fac = M.factors(d, est)
    truth = {c: sum(int(reg["pop"][c][s][18:].sum()) for s in ("M", "F")) for c in W.CODES}
    rg, wrong, var = rungs(d), wrong_paths(d), variants(d)
    alloc = {}
    for k, a in list(rg.items()) + list(var.items()) + list(wrong.items()) + [("truth", truth)]:
        alloc[k] = allocation(d, a)
    gold, gq = alloc["R3 golden"]
    mg = M.margin(gq, gold)
    differ = {k: sum(1 for c in W.CODES if alloc[k][0][c] != gold[c]) for k in alloc}
    var_ok = all(differ[k] == 0 for k in var)
    wrong_min = min(differ[k] for k in list(wrong) + [k for k in rg if k != "R3 golden"])
    if not quiet:
        f_dse = sum(v for (c, s, g), v in est.items() if s == "F" and g in W.YOUNG_GROUPS)
        m_dse = sum(v for (c, s, g), v in est.items() if s == "M" and g in W.YOUNG_GROUPS)
        f_true = sum(int(reg["pop"][c]["F"][18:50].sum()) for c in W.CODES)
        m_true = sum(int(reg["pop"][c]["M"][18:50].sum()) for c in W.CODES)
        print("seed %d: men 18-49 DSE/true %.4f, women %.4f; factors %s" % (
            seed, m_dse / m_true, f_dse / f_true, {W.group_label(g): round(v, 4) for g, v in fac.items()}))
        r = M.da_ratio(d)
        print("  DA sex ratios", {W.group_label(g): round(v, 4) for g, v in r.items()})
        for k in alloc:
            print("  %-52s differ %2d  %s" % (k, differ[k], " ".join("%2d" % alloc[k][0][c] for c in W.CODES)))
        print("  golden margin %.3f; variants agree: %s" % (mg, var_ok))
        gap = {c: rg["R3 golden"][c] - roll[c] for c in W.CODES}
        print("  golden gaps (k):", " ".join("%.1f" % (gap[c] / 1000) for c in W.CODES))
        print("  enrolment (roll/golden adults):", " ".join("%.3f" % (roll[c] / rg["R3 golden"][c]) for c in W.CODES))
        print("  nearest wrong path differs in %d regions" % wrong_min)
    return differ, mg, var_ok, wrong_min, differ["the extra men shared on the census's misses (SF11)"]


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]] or [W.SEED]
    if len(a) == 1:
        run(a[0])
    else:
        for s in range(a[0], a[1]):
            differ, mg, ok, wm, bmd = run(s, quiet=True)
            print("%d dse-differ %d r1 %d census %d margin %.3f variants %s nearest-wrong %d by-miss %d" % (
                s, differ["R2 dual-system cells"], differ["R1 one national ratio"], differ["R0 census counts"], mg, ok, wm, bmd))
