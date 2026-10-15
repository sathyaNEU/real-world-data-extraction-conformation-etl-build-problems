"""Every route to the certified change: the golden (the review's error by the medical examiner's drug class, each
year's classes solved from its three certificate categories) and each wrong rung the ladder names."""
import numpy as np

import conform as C
import world as W

CATS = ("OL", "SO", "N")


def table(recs, when=None, by=None):
    """year -> certificate category -> resident overdose deaths, as the file stood (None: at the extract)."""
    out = {}
    for v in C.resident_overdoses(recs, when):
        y = C.year_of(v)
        k = (y, by(v)) if by else y
        out.setdefault(k, {c: 0 for c in CATS})
        out[k][C.category(v)] += 1
    return out


def review_matrix(recs, review, by=None):
    """(stratum) -> true class -> certificate category counts, the 2025 certificates as they stand at the extract."""
    final = {v["state_file_no"]: v for v in C.as_of(recs)}
    m = {}
    for r in review:
        v = final[r["state_file_no"]]
        k = by(v) if by else None
        m.setdefault(k, {c: {x: 0 for x in CATS} for c in "OSR"})
        m[k][C.review_class(r)][C.category(v)] += 1
    return m


def probs(m):
    return np.array([[m[c][x] / max(1, sum(m[c].values())) for x in CATS] for c in "OSR"])


def solve(P, counts):
    """True class counts (O, S, R) from certificate category counts through the classification probabilities."""
    return np.linalg.solve(P.T, np.array([counts[x] for x in CATS], dtype=float))


def change(est):
    base = np.mean([est[y] for y in W.BASE])
    return 100 * (1 - est[W.TARGET] / base), base


def golden(recs, review):
    P = probs(review_matrix(recs, review)[None])
    t = table(recs)
    est = {y: solve(P, t[y]) for y in t}
    return {y: e[0] for y, e in est.items()}, est, P, t


def stratified(recs, review, by):
    ms = review_matrix(recs, review, by)
    t = table(recs, by=by)
    est = {}
    for (y, k), counts in t.items():
        if k not in ms:
            continue
        est[y] = est.get(y, 0) + solve(probs(ms[k]), counts)[0]
    return est


def certified(recs):
    t = table(recs)
    return {y: t[y]["OL"] for y in t}


def two_by_two(recs, review):
    m = review_matrix(recs, review)[None]
    sens = m["O"]["OL"] / sum(m["O"].values())
    fp = (m["S"]["OL"] + m["R"]["OL"]) / (sum(m["S"].values()) + sum(m["R"].values()))
    t = table(recs)
    return {y: (t[y]["OL"] - fp * sum(t[y].values())) / (sens - fp) for y in t}, sens, fp


def two_by_two_strata(recs, review, by):
    ms = review_matrix(recs, review, by)
    t = table(recs, by=by)
    est = {}
    for (y, k), c in t.items():
        m = ms[k]
        sens = m["O"]["OL"] / sum(m["O"].values())
        fp = (m["S"]["OL"] + m["R"]["OL"]) / (sum(m["S"].values()) + sum(m["R"].values()))
        est[y] = est.get(y, 0) + (c["OL"] - fp * sum(c.values())) / (sens - fp)
    return est


def predictive(recs, review):
    m = review_matrix(recs, review)[None]
    ppv = m["O"]["OL"] / sum(m[c]["OL"] for c in "OSR")
    npv_miss = m["O"]["N"] / sum(m[c]["N"] for c in "OSR")
    so = m["O"]["SO"] / max(1, sum(m[c]["SO"] for c in "OSR"))
    t = table(recs)
    net = sum(m["O"].values()) / sum(m[c]["OL"] for c in "OSR")
    return ({y: ppv * t[y]["OL"] + so * t[y]["SO"] + npv_miss * t[y]["N"] for y in t},
            {y: net * t[y]["OL"] for y in t})


def _pattern(v):
    cs = [C.dotted(c) for c in v["record_axis"].split()]
    op = any(c.startswith(C.OPIOID) for c in cs)
    st = any(c.startswith(C.STIM) for c in cs)
    return "OS" if op and st else ("OA" if op else ("SO" if st else "N"))


def pattern_routes(recs, review):
    """Rates conditioned on the certificate's drug pattern: the predictive value per pattern, a false-listing rate per
    certificate naming an opioid and a stimulant, and per certificate naming a stimulant."""
    final = {v["state_file_no"]: v for v in C.as_of(recs)}
    cls = {r["state_file_no"]: C.review_class(r) for r in review}
    pat = {}
    for sfn, c in cls.items():
        p = _pattern(final[sfn])
        pat.setdefault(p, {"O": 0, "S": 0, "R": 0})
        pat[p][c] += 1
    ppv = {p: pat[p]["O"] / sum(pat[p].values()) for p in pat}
    fp = sum(pat[p]["S"] + pat[p]["R"] for p in ("OS", "OA"))
    o = {p: pat.get(p, {"O": 0})["O"] for p in ("OS", "OA", "SO", "N")}
    sens = (o["OS"] + o["OA"]) / sum(o.values())
    per_os = fp / sum(pat["OS"].values())
    per_stim = fp / (sum(pat["OS"].values()) + sum(pat["SO"].values()))
    yt = {}
    for v in C.resident_overdoses(recs):
        y = C.year_of(v)
        yt.setdefault(y, {"OS": 0, "OA": 0, "SO": 0, "N": 0})
        yt[y][_pattern(v)] += 1
    pv4 = {y: sum(ppv.get(p, 0) * c[p] for p in c) for y, c in yt.items()}
    fos = {y: (c["OS"] + c["OA"] - per_os * c["OS"]) / sens for y, c in yt.items()}
    fst = {y: (c["OS"] + c["OA"] - per_stim * (c["OS"] + c["SO"])) / sens for y, c in yt.items()}
    return pv4, fos, fst


def half_class(recs, review):
    """The class idea with the stimulant deaths certified with no drug left out of the stimulant count."""
    m = review_matrix(recs, review)[None]
    sens = m["O"]["OL"] / sum(m["O"].values())
    fps = m["S"]["OL"] / sum(m["S"].values())
    t = table(recs)
    return {y: (t[y]["OL"] - fps * t[y]["SO"] / (1 - fps)) / sens for y in t}


def all_routes(recs, review):
    g, _, P, _ = golden(recs, review)
    rg, sens, fp = two_by_two(recs, review)
    pv, net = predictive(recs, review)
    pv4, fos, fst = pattern_routes(recs, review)
    routes = {"golden": g, "certified": certified(recs), "net_ratio": net, "predictive": pv, "rogan_gladen": rg,
              "pv_by_pattern": pv4, "fp_per_opioid_stimulant_cert": fos, "fp_per_stimulant_cert": fst,
              "class_without_unspecified_stimulant": half_class(recs, review),
              "rg_by_band": two_by_two_strata(recs, review, band),
              "rg_by_sex": two_by_two_strata(recs, review, lambda v: v["sex"])}
    return {k: (change(v)[0], v) for k, v in routes.items()}


def band(v):
    a = int(v["age_years"])
    return 0 if a < 35 else (1 if a < 45 else (2 if a < 55 else 3))
