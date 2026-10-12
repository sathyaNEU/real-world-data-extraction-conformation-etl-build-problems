"""Every figure the build owes, computed on the generator's side from the world and the fitted model."""
import math

import numpy as np

import asks as A
import core
import model as M

Z90 = 1.2815515655446004


def rungs_and_grid(fd):
    n, ybar, SSW, N, sq, p, mean, var = (fd[k] for k in ("n", "ybar", "SSW", "N", "sq", "p", "mean", "var"))
    f = fd["fit"]
    out = {}
    G = float(p.sum())
    nn = n.sum(1)
    raw = (n * ybar).sum(1) / nn
    s_pool = math.sqrt(f["s2"])
    out["golden_sum"] = G
    out["R0_raw_points"] = int((raw < 480).sum())
    out["R1_points"] = int((mean < 480).sum())
    out["R2_bound90"] = int((mean + Z90 * np.sqrt(var) < 480).sum())
    # no model: 90 per cent bound and flat-prior probabilities on the raw averages (student SD pooled)
    se = s_pool / np.sqrt(nn)
    out["raw_bound90"] = int((raw + Z90 * se < 480).sum())
    out["raw_probs"] = float(M.prob_below(raw, se ** 2).sum())
    # school level only, sittings pooled
    sw_within = float(sq.sum() + ((n * (ybar - raw[:, None]) ** 2).sum()))
    t2, m2, v2 = M.two_level(nn, raw, sw_within, N)
    out["R3_points"] = int((m2 < 480).sum())
    out["R3_probs"] = float(M.prob_below(m2, v2).sum())
    out["R3_bound90"] = int((m2 + Z90 * np.sqrt(v2) < 480).sum())
    out["R3_fit"] = t2
    # 2026 only
    n6, y6 = n[:, 2], ybar[:, 2]
    out["y26_raw_points"] = int((y6 < 480).sum())
    out["y26_raw_probs"] = float(M.prob_below(y6, s_pool ** 2 / n6).sum())
    t6, m6, v6 = M.two_level(n6, y6, float(sq[:, 2].sum()), float(n6.sum()))
    out["y26_school_points"] = int((m6 < 480).sum())
    out["y26_school_probs"] = float(M.prob_below(m6, v6).sum())
    # 2025 and 2026 only
    n56, y56 = n[:, 1:], ybar[:, 1:]
    f56 = M.fit(n56, y56, float(sq[:, 1:].sum()), float(n56.sum()))
    m56, v56 = M.school_posterior(n56, y56, f56["tu"], f56["tv"], f56["s2"], f56["beta"][0])
    raw56 = (n56 * y56).sum(1) / n56.sum(1)
    out["y2526_raw_points"] = int((raw56 < 480).sum())
    out["y2526_points"] = int((m56 < 480).sum())
    out["y2526_probs"] = float(M.prob_below(m56, v56).sum())
    # the decomposition of the golden against the point count
    below = mean < 480
    out["mass_above_among_below"] = float((1 - p[below]).sum())
    out["mass_below_among_above"] = float(p[~below].sum())
    out["sd_predictions"] = float(np.std(mean))
    out["sd_underlying"] = math.sqrt(f["tu"])
    out["sd_raw"] = float(np.std(raw))
    out["corr_p_size"] = float(np.corrcoef(p, nn)[0, 1])
    return out


def family(fd):
    n, ybar, SSW, N, sq = (fd[k] for k in ("n", "ybar", "SSW", "N", "sq"))
    f, mean, var, fam, fm, fs = M.family(n, ybar, SSW, N, sq)
    out = {k: float(v.sum()) for k, v in fam.items()}
    out["population_share"] = M.population_share(f, n.shape[0])
    out["median"], out["mode"] = M.median_mode(fam["reml"])
    out["ml_fit"] = {"tu": fm["tu"], "tv": fm["tv"], "s2": fm["s2"]}
    return out, fam


def asks(W, p, points):
    reg, plan, road, census = W["region"], W["plan"], W["road"], W["census"]
    G = float(p.sum())
    stu = A.students(census)
    out = {"places": int(round(G)), "places_exact": G}
    out["shares"] = {r: 100 * float(p[reg == r].sum()) / G for r in core.REGIONS}
    out["students_region"] = A.by_region(p, stu, reg)
    out["students_total"] = float((p * stu).sum())
    out["students_hub"] = A.by_hub(p, stu, plan)
    out["km_hub"] = A.hub_km(p, road, plan)
    out["km_total"] = float(sum(out["km_hub"].values()))
    k = out["km_hub"]
    out["chart_order"] = sorted(k, key=lambda h: -k[h])
    out["chart_title_hub"] = out["chart_order"][0]
    return out


def stops(W, p, points):
    """Each ask figure under each mishandling and under the point count, for the separation assertions."""
    reg, plan, road, census, dh = W["region"], W["plan"], W["road"], W["census"], W["dir_hub"]
    res = {}
    G = float(p.sum())
    for read in ("golden", "natural", "half", "over"):
        st = A.students(census, read)
        for hubs_name, hubs in (("plan", plan), ("directory", dh)):
            for wname, wt in (("probs", p), ("points", points)):
                for km_mult in (2, 1):
                    key = (read, hubs_name, wname, km_mult)
                    kmh = A.hub_km(wt, road, hubs)
                    res[key] = {
                        "students_region": A.by_region(wt, st, reg),
                        "students_total": float((wt * st).sum()),
                        "students_hub": A.by_hub(wt, st, hubs),
                        "km_hub": {h: v * km_mult / 2 for h, v in kmh.items()},
                    }
                    res[key]["km_total"] = float(sum(res[key]["km_hub"].values()))
                    kk = res[key]["km_hub"]
                    res[key]["chart_order"] = sorted(kk, key=lambda h: -kk[h])
    res["points_shares"] = {r: 100 * float(points[reg == r].sum()) / max(1.0, float(points.sum()))
                            for r in core.REGIONS}
    return res
