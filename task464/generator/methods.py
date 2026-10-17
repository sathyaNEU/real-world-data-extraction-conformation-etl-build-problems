"""Every route from a 2025 GLRA grade 8 score to an SLM performance level, computed from the bridge study's pairs, and
the counts of grade 9 and 10 students at each level in each district. Used by the calibration in sim.py's callers, by
golden.py for the deliverables and by checks.py for the ladder, the convergence and the mess."""
import math

import numpy as np

import world as W

FAMILY = ("kb", "quantile", "linear")    # the concordances that match the two tests' score distributions
RIVALS = ("regression", "inverse", "old_levels")


def _pr(scores, lo, hi):
    """Percentile ranks (in [0, 1]) of each integer score from lo to hi, mid-point convention, and the cumulative share."""
    v = np.arange(lo, hi + 1)
    f = np.array([np.sum(scores == k) for k in v], float) / len(scores)
    F = np.cumsum(f)
    pr = F - f / 2.0
    return v, pr, F


def kb_equivalents(old, new):
    """Equipercentile equivalents on the SLM scale of every GLRA integer score (percentile ranks with scores continuized
    half a point either side, the textbook construction)."""
    lo_o, hi_o = W.OLD["lo"], W.OLD["hi"]
    lo_n, hi_n = W.NEW["lo"], W.NEW["hi"]
    v, pr, _ = _pr(old, lo_o, hi_o)
    vn, _, Fn = _pr(new, lo_n, hi_n)
    # the SLM's continuized cumulative distribution: F at the upper edge of each score's half-point interval
    edges = np.concatenate([[lo_n - 0.5], vn + 0.5])
    cum = np.concatenate([[0.0], Fn])
    return dict(zip(v, np.interp(pr, cum, edges)))


def level_cut_points(old, new, method, cuts):
    """The GLRA score below which a result counts at each SLM level's lower boundary (a real number between two integer
    scores), under one route."""
    old, new = np.asarray(old, float), np.asarray(new, float)
    out = []
    if method == "kb":
        e = kb_equivalents(old.astype(int), new.astype(int))
        ks = sorted(e)
        for c in cuts:
            below = [k for k in ks if e[k] < c - 0.5]
            k = max(below)
            out.append(k + 0.5)                  # the crossing lies between k and k + 1
        return out, e
    if method == "quantile":
        for c in cuts:
            p = float(np.mean(new < c))
            out.append(float(np.quantile(old, p)))
        return out, None
    if method == "linear":
        mo, so, mn, sn = old.mean(), old.std(), new.mean(), new.std()
        return [mo + (c - 0.5 - mn) * so / sn for c in cuts], None
    if method == "regression":
        b, a = np.polyfit(old, new, 1)
        return [(c - 0.5 - a) / b for c in cuts], (a, b)
    if method == "inverse":
        d, c0 = np.polyfit(new, old, 1)
        return [c0 + d * (c - 0.5) for c in cuts], (c0, d)
    if method == "old_levels":
        return [k - 0.5 for k in W.OLD_CUTS[8]], None
    raise ValueError(method)


def level_from_old(score, cuts):
    lvl = 1
    for c in cuts:
        if score > c:
            lvl += 1
    return lvl


def level_from_new(score, cuts):
    lvl = 1
    for c in cuts:
        if score >= c:
            lvl += 1
    return lvl


def counts(population, cuts, new_cuts):
    """population: (district, grade, test, score) for each enrolled grade 9 or 10 student with a grade 8 result.
    Returns {(district, grade): [students at Level 1, 2, 3, 4]}."""
    out = {}
    for d, g, test, sc in population:
        lvl = level_from_new(sc, new_cuts) if test == "new" else level_from_old(sc, cuts)
        out.setdefault((d, g), [0, 0, 0, 0])[lvl - 1] += 1
    return out


def expected_level1(population, old, new, new_cuts):
    """The pooled conditional route: each GLRA score's chance of an SLM score below Level 2's boundary under the bridge's
    regression and its residual spread, summed (not a placement; a count's expectation)."""
    old, new = np.asarray(old, float), np.asarray(new, float)
    b, a = np.polyfit(old, new, 1)
    sd = float(np.std(new - (a + b * old)))
    out = {}
    for d, g, test, sc in population:
        if test == "new":
            p = 1.0 if sc < new_cuts[0] else 0.0
        else:
            z = (new_cuts[0] - 0.5 - (a + b * sc)) / sd
            p = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        out[(d, g)] = out.get((d, g), 0.0) + p
    return out


def level1_totals(cnt, districts):
    return {d: cnt.get((d, 9), [0] * 4)[0] + cnt.get((d, 10), [0] * 4)[0] for d in districts}


def slate(totals, k=W.GRANTS):
    order = sorted(totals, key=lambda d: (-totals[d], d))
    return order[:k], order[k]


def _kb_inverse(p, cnt, lo):
    """Kolen and Brennan's continuized inverse: the score at which a distribution, each integer spread half a point
    either side, reaches the share p."""
    cnt = np.asarray(cnt, float)
    F = np.cumsum(cnt) / cnt.sum()
    p = np.atleast_1d(np.asarray(p, float))
    i = np.clip(np.searchsorted(F, p, side="right"), 0, len(cnt) - 1)
    below = np.where(i > 0, F[np.maximum(i - 1, 0)], 0.0)
    f = cnt[i] / cnt.sum()
    return lo + i - 0.5 + np.where(f > 0, (p - below) / np.where(f > 0, f, 1.0), 0.0)


def _loglinear(cnt, degree):
    """Log-linear presmoothing (Holland and Thayer): the frequencies a polynomial of the given degree in the score
    index fits to the observed ones, preserving the first `degree` moments."""
    cnt = np.asarray(cnt, float)
    z = np.arange(len(cnt), dtype=float)
    z = (z - z.mean()) / z.std()
    X = np.column_stack([z ** k for k in range(degree + 1)])
    X, _ = np.linalg.qr(X)
    X *= np.sqrt(len(cnt))
    beta = np.zeros(degree + 1)
    beta[0] = np.log(cnt.mean() + 1e-9) / X[0, 0] if X[0, 0] else 0.0
    for _ in range(200):
        mu = np.exp(np.clip(X @ beta, -50, 50))
        g = X.T @ (cnt - mu)
        H = X.T @ (X * mu[:, None])
        step = np.linalg.solve(H + 1e-9 * np.eye(len(beta)), g)
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return np.exp(np.clip(X @ beta, -50, 50))


def conventions(old, new, c, grade=8):
    """Every mainstream way of reading a retiring-test score at the new test's boundary c through a concordance that
    matches the two score distributions, with the highest retiring score each places below c and its margin. Mapping
    conventions report margins in new-test points, count conventions in students, cut conventions in retiring points."""
    old, new = np.asarray(old, int), np.asarray(new, int)
    lo_o, hi_o, lo_n, hi_n = W.OLD["lo"], W.OLD["hi"], W.NEW["lo"], W.NEW["hi"]
    A = W.glra_attainable(grade)
    co = np.bincount(old - lo_o, minlength=hi_o - lo_o + 1).astype(float)
    cn = np.bincount(new - lo_n, minlength=hi_n - lo_n + 1).astype(float)
    n_o, n_n = co.sum(), cn.sum()
    Fo, Fn = np.cumsum(co) / n_o, np.cumsum(cn) / n_n
    out = {}

    def record(name, s, unit):
        """s: one value per attainable score, negative where the score is placed below c."""
        s = np.asarray(s, float)
        below = A[s < 0]
        K = int(below.max())
        j = int(np.where(A == K)[0][0])
        out[name] = (K, float(min(-s[j], s[j + 1])), unit)

    def mapping(prefix, cnt_o, cnt_n):
        F_at = (np.cumsum(cnt_o) / cnt_o.sum())[A - lo_o]
        f_at = cnt_o[A - lo_o] / cnt_o.sum()
        for nm, p in (("mid", F_at - f_at / 2), ("aob", F_at)):
            e = _kb_inverse(p, cnt_n, lo_n)
            record("%s_%s_round" % (prefix, nm), e - (c - 0.5), "points")
            record("%s_%s_raw" % (prefix, nm), e - c, "points")
        return F_at, f_at

    F_at, f_at = mapping("kb", co, cn)
    for deg in (4, 6):
        cs_o = np.zeros_like(co)
        raw = np.array([np.sum(old == a) for a in A], float)
        cs_o[A - lo_o] = _loglinear(raw, deg)
        mapping("smooth%d" % deg, cs_o, _loglinear(cn, deg))
    for nm, p in (("mid", F_at - f_at / 2), ("aob", F_at)):
        q = np.quantile(new, np.clip(p, 0, 1))
        record("qmap_%s_raw" % nm, q - c, "points")
        record("qmap_%s_round" % nm, q - (c - 0.5), "points")
        record("ecdf_%s" % nm, (p - Fn[c - 1 - lo_n]) * n_n + 1e-9, "students")
        Pn = Fn - cn / n_n / 2
        y = np.array([lo_n + int(np.argmin(np.abs((Pn if nm == "mid" else Fn) - v))) for v in p])
        record("nearest_%s" % nm, y - c + 0.5, "points")
    def cut_record(name, p):
        """A cut convention: the boundary c carried to the retiring scale at share p. Its margin is the number of
        bridge students p could move before the retiring score next to the boundary changes level."""
        F_all = np.cumsum(co) / n_o
        K = int(A[F_all[A - lo_o] < p].max())
        Kn = int(A[A > K].min())
        mid_K = F_all[K - lo_o] - co[K - lo_o] / n_o / 2
        mid_Kn = F_all[Kn - lo_o] - co[Kn - lo_o] / n_o / 2
        F_K, F_Kn = F_all[K - lo_o], F_all[Kn - lo_o]
        xs = float(_kb_inverse(p, co, lo_o)[0])
        out[name] = (int(A[A < xs].max()), float(min(p - mid_K, mid_Kn - p) * n_o), "students")
        out[name + "_rounded"] = (int(A[A < round(xs)].max()), float(min(p - F_K, F_Kn - p) * n_o), "students")
        return K, F_K

    p_e = float(np.mean(new < c))
    K_e, F_Ke = cut_record("kbcut_edge", p_e)
    cut_record("kbcut_mid", Fn[c - 1 - lo_n] + cn[c - lo_n] / n_n / 2)
    xq = float(np.quantile(old, p_e))
    out["qcut_lt"] = (int(A[A < xq].max()), float((p_e - F_Ke) * n_o), "students")
    out["qcut_le"] = (int(A[A <= xq].max()), 0.0, "students")
    mo, so, mn, sn = old.mean(), old.std(), new.mean(), new.std()
    lin = mn + (A - mo) * sn / so
    record("linear_raw", lin - c, "points")
    record("linear_round", lin - (c - 0.5), "points")
    for nm, t in (("edge", c - 0.5), ("mid", c)):
        xl = mo + (t - mn) * so / sn
        K = int(A[A < round(xl)].max())
        Kn = int(A[A > K].min())
        out["lincut_%s_rounded" % nm] = (K, float(min(xl - K - 0.5, Kn + 0.5 - xl)), "retiring")
    return out


def agree(conv, need=None):
    """Whether every convention places the same retiring score highest below the boundary, each with room to spare."""
    need = need or {"points": 1.0, "students": 5.0, "retiring": 0.4}
    ks = {k: v[0] for k, v in conv.items() if k != "qcut_le"}
    if len(set(ks.values())) != 1:
        return False
    return all(v[1] >= need[v[2]] for k, v in conv.items() if k != "qcut_le" and not k.startswith("nearest"))


def regression_boundary(old, new, c, grade=8):
    b, a = np.polyfit(old, new, 1)
    A = W.glra_attainable(grade)
    return int(A[a + b * A < c - 0.5].max()), int(A[a + b * A < c].max())


def inverse_boundary(old, new, c, grade=8):
    d, c0 = np.polyfit(new, old, 1)
    A = W.glra_attainable(grade)
    return int(A[A < c0 + d * (c - 0.5)].max())


# ------------------------------------------------------------------------------------------- the grant population
def on_count_day(sp):
    return sp["entry"] <= W.COUNT_DAY and (sp["exit"] == "" or sp["exit"] >= W.COUNT_DAY)


def result(r):
    """A record's score if it produced one: the score itself, or the make-up session's after an invalidation."""
    if r["status"] == "scored":
        return r["score"]
    if r["status"] == "invalid" and r["retake"]:
        return r["retake_score"]
    return None


def latest_grade8(s):
    best = None
    for r in s.get("records", []):
        sc = result(r) if r["grade"] == 8 else None
        if sc is not None and (best is None or r["year"] > best[1]):
            best = (r["test"], r["year"], sc)
    return best


def population(x, districts=None):
    """(district, grade, test, year, score, sid) for each grade 9 or 10 student on the roll on the count day whose
    latest grade 8 state reading result exists."""
    out = []
    for sp in x["spells"]:
        if sp["grade"] not in (9, 10) or not on_count_day(sp):
            continue
        if districts is not None and sp["district"] not in districts:
            continue
        res = latest_grade8(sp["who"])
        if res:
            out.append((sp["district"], sp["grade"], res[0], res[1], res[2], sp["who"]["sid"]))
    return out


def level1_counts(pop, K, c=None, districts=None):
    """Each district's grade 9 and 10 students at Level 1: a new-test score below c, a retiring-test score at or
    below K (the highest retiring score placed below c)."""
    c = c or W.NEW_CUTS[8][0]
    out = {d: [0, 0] for d in (districts or sorted(set(p[0] for p in pop)))}
    for d, g, test, year, sc, sid in pop:
        if d in out and ((test == "new" and sc < c) or (test == "old" and sc <= K)):
            out[d][g - 9] += 1
    return out


def placement(x, c=None):
    """The highest retiring-test score each route places below the new test's Level 2 boundary."""
    c = c or W.NEW_CUTS[8][0]
    rows = x["bridge"]["rows"]
    old = np.array([r["old"] for r in rows])
    new = np.array([r["new"] for r in rows])
    conv = conventions(old, new, c)
    ks = set(v[0] for k, v in conv.items() if k != "qcut_le")
    A = W.glra_attainable(8)
    K = dict(concordance=ks.pop() if len(ks) == 1 else None, regression=regression_boundary(old, new, c)[0],
             inverse=inverse_boundary(old, new, c), old_levels=int(A[A < W.OLD_CUTS[8][0]].max()))
    xr = W.OLD["lo"] + (c - 0.5 - W.NEW["lo"]) * (W.OLD["hi"] - W.OLD["lo"]) / (W.NEW["hi"] - W.NEW["lo"])
    K["scale_range"] = int(A[A < xr].max())
    g25, s26 = [], []
    for s in x["students"]:
        for r in s["records"]:
            if r["grade"] == 8 and result(r) is not None:
                (g25 if r["test"] == "old" else s26).append(result(r))
    cc = conventions(np.array(g25), np.array(s26), c)
    kc = set(v[0] for k, v in cc.items() if k != "qcut_le")
    K["cohort_percentiles"] = kc.pop() if len(kc) == 1 else None
    g25, s26 = np.array(g25, float), np.array(s26, float)
    xl = g25.mean() + (c - 0.5 - s26.mean()) * g25.std() / s26.std()
    K["cohort_z"] = int(A[A < xl].max())
    return K, conv


def slate_of(counts, k=W.GRANTS):
    tot = {d: sum(v) for d, v in counts.items()}
    order = sorted(tot, key=lambda d: (-tot[d], d))
    return order[:k], order[k], tot


# ------------------------------------------------------------------------- the incoming cohort (grade 7, spring 2026)
def directory_district(school):
    """The district a public middle school belongs to in the 2026 directory, None for a school outside it."""
    for code, schools in DIRECTORY_MID.items():
        if school in schools:
            return code
    return None


DIRECTORY_MID = {}


def grade7_rows(x):
    """Every spring 2026 grade 7 record on the new test, public and nonpublic: (school, vendor district, record)."""
    out = []
    for s in x["younger"] + x["np_only"] + [t for t in x["students"] if t.get("nonpublic")]:
        for r in s["records"]:
            if r["test"] == "new" and r["year"] == 2026 and r["grade"] == 7:
                out.append((s["school"], s["tested_in"], r))
    return out


def june_level(sc, grade):
    return level_from_new(sc, W.NEW_CUTS_JUNE[grade])


def grade7_ask(x, by="directory", cuts="adopted"):
    """Each applicant's grade 7 students with a spring 2026 score on the new test, at Level 1 and in all: by the 2026
    directory's schools (the golden) or by the vendor's district code; Level 1 on the adopted or the June cut."""
    merged = {sub: new for new, parts in W.MERGER.items() for sub, _, _ in parts}
    out = {d: [0, 0] for d in W.APPLICANTS}
    for school, vendor, r in grade7_rows(x):
        sc = result(r)
        if sc is None:
            continue
        d = directory_district(school) if by == "directory" else merged.get(vendor, vendor)
        if d not in out:
            continue
        lvl1 = sc < W.NEW_CUTS[7][0] if cuts == "adopted" else june_level(sc, 7) == 1
        out[d][0] += int(lvl1)
        out[d][1] += 1
    return out
