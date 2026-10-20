"""The simulation behind task471: candidates and their attempt history, the two forms, the June 2025 and June 2026
administrations scored read by read, and the 2026 validity papers. Everything is drawn from one seeded generator per
part, so a parameter change in one part leaves the others' draws where they were."""
import datetime as dt

import numpy as np

import world as W

THR = np.array(W.THRESHOLDS)


def rng(seed, part):
    return np.random.default_rng([seed, part])


def rating(lat):
    return 1 + (np.asarray(lat)[..., None] > THR).sum(-1)


# ------------------------------------------------------------------------------------------------------------ forms
def forms(seed, p):
    r = rng(seed, 1)

    def mc(n, shift=0.0):
        return dict(a=r.uniform(0.7, 1.5, n), b=r.normal(W.MC_B_MEAN, W.MC_B_SD, n) + shift, c=r.uniform(0.15, 0.25, n))
    shared = mc(W.N_SHARED)
    own25 = mc(W.N_MC - W.N_SHARED)
    own26 = mc(W.N_MC - W.N_SHARED, p["dmc"])
    wa_shared = r.normal(-0.15, 0.25)
    wa25 = r.normal(-0.15, 0.25, 2)
    wa26 = r.normal(-0.15, 0.25, 2) + p["dwa"]
    # positions: the shared items sit at different positions on the two forms
    pos25 = r.permutation(W.N_MC)
    pos26 = r.permutation(W.N_MC)
    f25 = {"mc": {k: np.concatenate([shared[k], own25[k]]) for k in shared}, "wa": np.array([wa25[0], wa_shared, wa25[1]]),
           "pos": pos25}
    f26 = {"mc": {k: np.concatenate([shared[k], own26[k]]) for k in shared}, "wa": np.array([wa26[0], wa_shared, wa26[1]]),
           "pos": pos26}
    return f25, f26


def mc_scores(theta1, items, r=None, U=None):
    a, b, c = items["a"], items["b"], items["c"]
    pr = c + (1 - c) / (1 + np.exp(-1.7 * a * (theta1[:, None] - b)))
    U = r.random(pr.shape) if U is None else U
    return (U < pr).astype(np.int8)


def wa_reads(theta2, d, sev, r=None, Z=None):
    """two operational reads per response, a scoring leader's resolution read where they differ by more than one
    point; the assignment score is the sum of the two reads, or twice the resolution read"""
    base = theta2[:, None] - d[None, :]
    if Z is None:
        Z = (r.normal(0, 1, base.shape), r.normal(0, 1, base.shape), r.normal(0, 1, base.shape))
    r1 = rating(base + sev + W.RATER_SD * Z[0])
    r2 = rating(base + sev + W.RATER_SD * Z[1])
    res = rating(base + sev + W.LEADER_SD * Z[2])
    need = np.abs(r1 - r2) > 1
    score = np.where(need, 2 * res, r1 + r2)
    return r1, r2, np.where(need, res, 0), score


def raw_of(form, yr, t1, t2, U, Z, sev=None):
    mc = mc_scores(t1, form["mc"], U=U)
    sev = W.SEVERITY[yr] if sev is None else sev
    return mc.sum(1) + W.WA_WEIGHT * wa_reads(t2, form["wa"], sev, Z=Z)[3].sum(1)


# ------------------------------------------------------------------------------------------------------- candidates
def people(seed, p):
    """every candidate who makes a first attempt in June 2025 or June 2026, plus the 2025-26 completers who have not
    yet tested, plus the repeat candidates of both Junes with their earlier attempts"""
    r = rng(seed, 2)
    rows = []

    def ability(n, s1, s2, cohort):
        c1, c2 = p["cohort"][cohort]
        t1 = r.normal(c1 + s1, 0.95, n)
        t2 = W.RHO * (t1 - c1 - s1) + np.sqrt(1 - W.RHO ** 2) * r.normal(0, 0.95, n) + c2 + s2
        return t1, t2
    # 2025-26 completers of the sixteen programs
    for k, (name, code, kind, n, s1, s2, early, untested) in enumerate(W.PROGRAMS):
        t1, t2 = ability(n, s1, s2, "new")
        u = r.random(n)
        for i in range(n):
            first = None if u[i] < untested else (2025 if u[i] < untested + early else 2026)
            rows.append(dict(group="completer", program=k, cohort="new", t1=t1[i], t2=t2[i], first=first))
    # 2024-25 completers testing first in June 2025, by program in proportion to size
    sizes = np.array([pp[3] for pp in W.PROGRAMS], float)
    ks = r.choice(len(W.PROGRAMS), W.EARLIER_COMPLETERS_2025, p=sizes / sizes.sum())
    for k in ks:
        t1, t2 = ability(1, W.PROGRAMS[k][4], W.PROGRAMS[k][5], "pre")
        rows.append(dict(group="earlier", program=int(k), cohort="pre", t1=t1[0], t2=t2[0], first=2025))
    # other first attempts: out-of-state completers, experience-route permit holders, earlier completers testing late
    for yr, n in ((2025, W.OTHERS_2025), (2026, W.OTHERS_2026)):
        t1, t2 = ability(n, -0.05, -0.05, "pre" if yr == 2025 else "other26")
        for i in range(n):
            rows.append(dict(group="other", program=None, cohort="pre" if yr == 2025 else "other26", t1=t1[i],
                             t2=t2[i], first=yr))
    # repeat candidates: earlier failures who test again (their first attempt between 2019 and 2024)
    for yr, n in ((2025, p["rep25"]), (2026, p["rep26_old"])):
        t1, t2 = ability(n, -0.75, -0.65, "pre")
        fy = r.choice([2019, 2020, 2021, 2022, 2023, 2024], n, p=[0.05, 0.07, 0.10, 0.16, 0.25, 0.37])
        for i in range(n):
            hist = [int(fy[i])] + [y for y in range(int(fy[i]) + 1, 2025) if r.random() < 0.45]
            rows.append(dict(group="repeat", program=None, cohort="pre", t1=t1[i], t2=t2[i], first=int(fy[i]),
                             history=hist))
            rows[-1]["sits"] = [yr]
    for x in rows:
        x.setdefault("history", [])
        if "sits" not in x:
            x["sits"] = [] if x["first"] is None else [x["first"]]
    return rows


def administer(seed, p, rows, f25, f26):
    """score both Junes; a June 2025 candidate who fails tests again in June 2026 at the repeat rate"""
    out = {}
    for yr, form, part in ((2025, f25, 3), (2026, f26, 4)):
        r = rng(seed, part)
        idx = [i for i, x in enumerate(rows) if yr in x["sits"]]
        t1 = np.array([rows[i]["t1"] for i in idx])
        t2 = np.array([rows[i]["t2"] for i in idx])
        U = r.random((len(idx), W.N_MC))
        Z = (r.normal(0, 1, (len(idx), W.N_WA)), r.normal(0, 1, (len(idx), W.N_WA)), r.normal(0, 1, (len(idx), W.N_WA)))
        mc = mc_scores(t1, form["mc"], U=U)
        r1, r2, res, score = wa_reads(t2, form["wa"], p["sev"][yr], Z=Z)
        out[yr] = dict(idx=np.array(idx), mc=mc, r1=r1, r2=r2, res=res, wa=score, U=U, Z=Z,
                       raw=mc.sum(1) + W.WA_WEIGHT * score.sum(1),
                       anchor=mc[:, :W.N_SHARED].sum(1) + W.WA_WEIGHT * score[:, 1],
                       first=np.array([rows[i]["first"] == yr for i in idx]))
        if yr == 2025:
            failed = out[2025]["raw"] < W.PASS_RAW_25A
            back = r.random(len(idx)) < W.REPEAT_RATE
            for j, i in enumerate(idx):
                if failed[j] and back[j]:
                    rows[i]["sits"].append(2026)
    return out


def validity(seed, p, rows, f25, scored):
    """the 2026 validity papers: for WA2, 2025 responses drawn at random from the June 2025 responses whose two reads
    agreed, each with the score both 2025 reads gave it; for WA1 and WA3, responses from the 2026 rangefinding with
    the 2026 leaders' consensus scores; each paper read by several 2026 raters"""
    r = rng(seed, 51)
    s25 = scored[2025]
    papers, reads = [], []
    t2_25 = np.array([rows[i]["t2"] for i in s25["idx"]])
    sev = p["sev"][2026]
    for wa, n in W.N_VALIDITY.items():
        if wa == "WA2":
            agreed = np.flatnonzero(s25["r1"][:, 1] == s25["r2"][:, 1])
            pick = r.choice(agreed, n, replace=False)
            base = t2_25[pick] - f25["wa"][1]
            cons = s25["r1"][pick, 1]                   # the score both June 2025 reads gave (the 2025 raters)
            src = "2025"
        else:
            # rangefinding responses: 2026 candidates' responses, consensus at the 2026 standard
            j = 0 if wa == "WA1" else 2
            t2_26 = r.normal(-0.10, 1.0, n)
            base = t2_26 - p["wa26"][j]
            cons = rating(base + sev)
            src = "2026"
        k = r.integers(W.VALIDITY_READS[0], W.VALIDITY_READS[1] + 1, n)
        for i in range(n):
            lat = base[i] + sev + r.normal(0, W.RATER_SD, k[i])
            papers.append(dict(wa=wa, src=src, consensus=int(cons[i]), n=int(k[i])))
            for v in rating(lat):
                reads.append((len(papers) - 1, int(v)))
    return papers, reads


def world(seed=W.SEED, **kw):
    p = dict(dmc=W.DMC_26A, dwa=W.DWA_26A, cohort=dict(W.COHORT_SHIFT), rep25=720, rep26_old=420,
             sev=dict(W.SEVERITY))
    p.update(kw)
    f25, f26 = forms(seed, p)
    p["wa26"] = f26["wa"]
    rows = people(seed, p)
    scored = administer(seed, p, rows, f25, f26)
    papers, vreads = validity(seed, p, rows, f25, scored)
    return dict(seed=seed, p=p, f25=f25, f26=f26, rows=rows, scored=scored, papers=papers, vreads=vreads)
