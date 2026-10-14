"""The accounting area as it is: each district's land split by its true 2024-2025 class (D deforested, F stable
forest, N non-forest), the class the preliminary map gave it (PD, PF, PN) and the class the final map gives it
(FD, FF, FN). Areas in hectares. The reference sample is drawn on the preliminary classes."""
import numpy as np

import world as W


def cells():
    """{(district, true, preliminary, final): hectares} over the twelve program districts"""
    out = {}
    for code, _, area, forest, defo, cloud in W.DISTRICTS:
        true = {"D": float(defo), "F": float(forest - defo), "N": float(area - forest)}
        prelim = {
            "D": {"PD": 1 - W.PRELIM_OMIT * (0.8 + 0.2 * cloud) - W.PRELIM_OMIT_N,
                  "PF": W.PRELIM_OMIT * (0.8 + 0.2 * cloud), "PN": W.PRELIM_OMIT_N},
            "F": {"PD": W.PRELIM_FALSE_F * cloud, "PF": 1 - W.PRELIM_FALSE_F * cloud - 0.003, "PN": 0.003},
            "N": {"PD": W.PRELIM_FALSE_N * cloud, "PF": W.PRELIM_N_AS_F, "PN": 1 - W.PRELIM_FALSE_N * cloud -
                  W.PRELIM_N_AS_F}}
        for t, a in true.items():
            for p, q in prelim[t].items():
                for f, r in W.FINAL[(t, p)].items():
                    if q * r > 0:
                        out[(code, t, p, f)] = a * q * r
    return out


def strata_areas(C=None):
    C = C or cells()
    return {s: sum(v for (d, t, p, f), v in C.items() if p == pc) for s, pc, _ in W.STRATA}


def final_areas(C=None):
    """the final map's classes by program district"""
    C = C or cells()
    out = {}
    for (d, t, p, f), v in C.items():
        out[(d, f)] = out.get((d, f), 0.0) + v
    return out


def prelim_areas(C=None):
    C = C or cells()
    out = {}
    for (d, t, p, f), v in C.items():
        out[(d, p)] = out.get((d, p), 0.0) + v
    return out


def draw_sample(seed=W.SEED, C=None):
    """the reference points: n_h drawn at random in each preliminary stratum, with probability proportional to area
    across the stratum's districts and classes; returns a list of (stratum, district, true, final)"""
    C = C or cells()
    rng = np.random.default_rng(seed)
    pts = []
    for s, pc, _ in W.STRATA:
        keys = sorted(k for k in C if k[2] == pc)
        pr = np.array([C[k] for k in keys])
        pr = pr / pr.sum()
        idx = rng.choice(len(keys), size=W.N_SAMPLE[s], p=pr)
        pts += [(s, keys[i][0], keys[i][1], keys[i][3]) for i in idx]
    order = rng.permutation(len(pts))            # point numbers are not in stratum order
    return [pts[i] for i in order]
