"""The golden, computed from the shipped files only: the spring forecast at each set length and the two asks.
Every route a check or a ladder rung needs is a function here, run on the same cleaned frame."""
import csv
import datetime as dt
import os
import zoneinfo

import numpy as np
import openpyxl
from scipy.optimize import minimize, minimize_scalar
from scipy.special import expit

import params as P
from pack import FILES

EAST = zoneinfo.ZoneInfo(P.TZ)
SB_ORDER = [b[0] for b in P.SKILL_BUILDERS]
SBI = {b: i for i, b in enumerate(SB_ORDER)}
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(31)
GH_W = GH_W / GH_W.sum()


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, target):
        self.t = target
        self.f = {k: os.path.join(target, v) for k, v in FILES.items()}
        self._load()

    def _load(self):
        link = read_csv(self.f["link"])
        self.student_of = {r["pellmore_user_id"]: r["student_id"] for r in link}
        asg = read_csv(self.f["assignments"])
        self.sb_of_legacy = {r["legacy_assignment_id"]: r["skill_builder"] for r in asg if r["legacy_assignment_id"]}
        self.sb_of_ref = {r["assignment_ref"]: r["skill_builder"] for r in asg}
        self.year_of_ref = {r["assignment_ref"]: r["school_year"] for r in asg}
        rows = []      # (student, year, sb, local datetime, correct, school_code_in_export)
        for r in read_csv(self.f["log_legacy"]):
            rows.append((r["user_id"], "2025-26", self.sb_of_legacy[r["assignment_id"]],
                         dt.datetime.fromisoformat(r["start_time"]), int(r["correct"]), r["school"]))
        for key in ("log_2026", "log_fall"):
            for r in read_csv(self.f[key]):
                t = dt.datetime.fromisoformat(r["started_utc"].replace("Z", "+00:00")).astimezone(EAST).replace(tzinfo=None)
                rows.append((r["student_user_id"], self.year_of_ref[r["assignment_ref"]], self.sb_of_ref[r["assignment_ref"]],
                             t, int(r["first_attempt_score"]), r["school_code"]))
        self.raw = rows
        wb = openpyxl.load_workbook(self.f["roster"], read_only=True)
        self.on_roll = [r[0] for r in list(wb["On roll 23 Oct 2026"].iter_rows(values_only=True))[1:] if r and r[0]]

    def frame(self, sitting="gap", gap_hours=3.0):
        """first attempts at original problems by students, ordered within student and skill builder, with the count
        of the student's earlier problems in the current sitting and in earlier sittings"""
        keep = [(self.student_of[u], y, sb, t, c) for (u, y, sb, t, c, sch) in self.raw if u in self.student_of]
        keep.sort(key=lambda x: (x[0], x[2], x[3]))
        self.sid = {}
        S, B, NALL, ECUR, EPREV, Y, FIRST = [], [], [], [], [], [], []
        prev_key, last_t, n, ecur, eprev, nsit = None, None, 0, 0, 0, 0
        for s, y, sb, t, c in keep:
            key = (s, sb)
            if key != prev_key:
                prev_key, n, ecur, eprev, nsit, last_t = key, 0, 0, 0, 0, None
            elif (t.date() != last_t.date()) if sitting == "date" else ((t - last_t).total_seconds() > gap_hours * 3600):
                eprev += ecur
                ecur = 0
                nsit += 1
            S.append(self.sid.setdefault(s, len(self.sid)))
            B.append(SBI[sb])
            NALL.append(n)
            ECUR.append(ecur)
            EPREV.append(eprev)
            Y.append(c)
            FIRST.append(nsit == 0)
            n += 1
            ecur += 1
            last_t = t
        self.S, self.B = np.array(S), np.array(B)
        self.NALL, self.ECUR, self.EPREV = np.array(NALL, float), np.array(ECUR, float), np.array(EPREV, float)
        self.Y, self.FIRST = np.array(Y, float), np.array(FIRST)
        self.nst = len(self.sid)
        return self


def fit(pk, counts, sigma=1.0, student=True, rows=None, x0=None):
    """penalised fit of logit P(right) = theta_student + a_sb + sum_k slope_k,sb * count_k (theta ~ N(0, sigma^2)).
    counts: list of arrays aligned with the frame; returns parameters and the Laplace log marginal likelihood"""
    S, B, Y = pk.S, pk.B, pk.Y
    X = list(counts)
    if rows is not None:
        S, B, Y, X = S[rows], B[rows], Y[rows], [x[rows] for x in X]
    nst, nb, k = pk.nst, len(SB_ORDER), len(X)
    inv = 0.0 if not student else 1.0 / sigma ** 2

    def unpack(par):
        th = par[:nst] if student else np.zeros(nst)
        a = par[nst:nst + nb]
        sl = [par[nst + nb * (1 + j):nst + nb * (2 + j)] for j in range(k)]
        return th, a, sl

    def f(par):
        th, a, sl = unpack(par)
        z = th[S] + a[B]
        for j in range(k):
            z = z + sl[j][B] * X[j]
        p = expit(z)
        ll = np.sum(Y * np.log(p + 1e-300) + (1 - Y) * np.log(1 - p + 1e-300)) - 0.5 * inv * np.sum(th ** 2)
        r = Y - p
        g = [np.bincount(S, r, nst) - inv * th if student else np.zeros(nst), np.bincount(B, r, nb)]
        for j in range(k):
            g.append(np.bincount(B, r * X[j], nb))
        return -ll, -np.concatenate(g)

    x0 = np.zeros(nst + nb * (1 + k)) if x0 is None else x0
    res = minimize(f, x0, jac=True, method="L-BFGS-B", options={"maxiter": 3000, "maxcor": 20, "ftol": 1e-13, "gtol": 1e-7})
    th, a, sl = unpack(res.x)
    z = th[S] + a[B]
    for j in range(k):
        z = z + sl[j][B] * X[j]
    p = expit(z)
    info = np.bincount(S, p * (1 - p), nst)
    out = {"theta": th, "a": a, "slopes": sl, "info": info, "sigma": sigma, "student": student, "x": res.x,
           "loglik": float(np.sum(Y * np.log(p + 1e-300) + (1 - Y) * np.log(1 - p + 1e-300)))}
    if student:
        out["laplace"] = float(-res.fun - 0.5 * np.sum(np.log1p(sigma ** 2 * info)))
    return out


def fit_sigma(pk, counts, lo=0.5, hi=1.6):
    """the student spread by Laplace maximum likelihood (a one-dimensional search over sigma)"""
    cache = {}
    warm = [None]

    def neg(sig):
        key = round(sig, 4)
        if key not in cache:
            cache[key] = fit(pk, counts, sigma=sig, x0=warm[0])
            warm[0] = cache[key]["x"]
        return -cache[key]["laplace"]
    r = minimize_scalar(neg, bounds=(lo, hi), method="bounded", options={"xatol": 2e-3})
    return cache[round(r.x, 4)]


def p_short(z):
    """chance of fewer than PASS_AT right among the check problems, z: (n, CHECK) logits"""
    p = expit(z)
    dp = np.zeros((len(p), P.CHECK + 1))
    dp[:, 0] = 1.0
    for k in range(p.shape[1]):
        pk = p[:, k:k + 1]
        new = dp * (1 - pk)
        new[:, 1:] += dp[:, :-1] * pk
        dp = new
    return dp[:, :P.PASS_AT].sum(1)


def forecast(pk, m, N, slope_index=0, integrate=True):
    """expected failed checks for every seventh grader on roll, each spring skill builder, after a set of N problems
    done in one sitting (no earlier sitting's problems): returns {sb: expected count}"""
    th, a, sl = m["theta"], m["a"], m["slopes"]
    sig = m["sigma"]
    ids = np.array([pk.sid.get(s, -1) for s in pk.on_roll])
    have = ids >= 0
    mu = np.where(have, th[np.maximum(ids, 0)], 0.0) if m["student"] else np.zeros(len(ids))
    if m["student"] and integrate:
        post = 1.0 / np.sqrt(m["info"][np.maximum(ids, 0)] + 1.0 / sig ** 2)
        sd = np.where(have, post, sig)
    else:
        sd = np.zeros(len(ids)) if not m["student"] else np.where(have, 0.0, 0.0)
    out = {}
    steps = np.arange(N, N + P.CHECK, dtype=float)
    for sb in P.SPRING:
        b = SBI[sb]
        base = a[b] + sl[slope_index][b] * steps
        if integrate and m["student"]:
            acc = np.zeros(len(ids))
            for x, wgt in zip(GH_X, GH_W):
                acc += wgt * p_short((mu + sd * x)[:, None] + base[None, :])
        else:
            acc = p_short(mu[:, None] + base[None, :])
        out[sb] = float(acc.sum())
    return out


def golden_model(pk):
    pk.frame("gap", 3.0)
    return fit_sigma(pk, [pk.ECUR, pk.EPREV])


def call(pk, m):
    by_len = {N: forecast(pk, m, N) for N in P.LENGTHS}
    tot = {N: sum(v.values()) for N, v in by_len.items()}
    fits = [N for N in P.LENGTHS if tot[N] <= P.PLACES]
    chosen = min(fits) if fits else None
    return by_len, tot, chosen


# the asks ---------------------------------------------------------------------------------------------------------
def spells(pk):
    out = {}
    for r in read_csv(pk.f["archive"]):
        out.setdefault(r["student_id"], []).append((r["school_code"], dt.date.fromisoformat(r["first_day_on_roll"]),
                                                    dt.date.fromisoformat(r["last_day_on_roll"])))
    return out


def ask_problems(pk):
    """each school's 2025-26 skill-builder problems on Units 4 to 7, counted at the school the student attended on
    the (Eastern) day the problem was started"""
    sp = spells(pk)
    count = {s[0]: {sb: 0 for sb in P.SPRING} for s in P.SCHOOLS}
    for r in read_csv(pk.f["log_2026"]):
        sb = pk.sb_of_ref[r["assignment_ref"]]
        if sb not in P.SPRING:
            continue
        sid = pk.student_of.get(r["student_user_id"])
        if sid is None:
            continue
        day = dt.datetime.fromisoformat(r["started_utc"].replace("Z", "+00:00")).astimezone(EAST).date()
        for code, a, b in sp.get(sid, []):
            if a <= day <= b:
                count[code][sb] += 1
                break
    return count


def solve(target):
    pk = Pack(target)
    m = golden_model(pk)
    by_len, tot, chosen = call(pk, m)
    return {"pack": pk, "model": m, "by_len": by_len, "tot": tot, "chosen": chosen, "problems": ask_problems(pk)}


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    out = solve(sys.argv[1])
    m = out["model"]
    print("sigma %.3f  loglik %.0f" % (m["sigma"], m["loglik"]))
    for N in P.LENGTHS:
        print("N=%2d total %.1f  %s" % (N, out["tot"][N], {k: round(v, 1) for k, v in out["by_len"][N].items()}))
    print("chosen", out["chosen"])
    print("problems", out["problems"])
    print("%.1fs" % (time.time() - t0))
