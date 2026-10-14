"""The golden's computations from the generator's records, kept to what the shipped files hold: the operators the
standard counts at their latest DOT physical, each configuration's accommodation under the survey's within-sex joint
normal carried to each operator through stature and weight, the rungs a lazier model files, and the ask's option
maintenance and twelve-year costs."""
import datetime as dt
import math

import numpy as np
from scipy import stats
from scipy.stats import qmc

import world as W

FIT = W.FIT_DIMS
COND_ON = ["S", "W"]
INF = math.inf


def world_state():
    ppl = W.employees()
    enc = W.encounters(ppl)
    buses = W.fleet()
    wos = W.work_orders(buses)
    W.off_the_first(buses)
    return {"people": ppl, "enc": enc, "buses": buses, "wos": wos,
            "comfort": W.comfort_survey(ppl), "claims": W.comp_claims(ppl), "trial": W.fit_trial(ppl)}


# ---------------------------------------------------------------- the operators the standard counts
def counted(st, latest=True, active_only=False):
    """Every Bus Operator on the 30 September 2026 roster with sex and the stature (mm) and weight (kg) of the
    latest DOT physical on or before that date (or the mean of all physicals)."""
    phys = {}
    for e in st["enc"]:
        if e["type"] == "PHYS":
            phys.setdefault(e["emp"], []).append(e)
    out = []
    for p in st["people"]:
        if p["left"] is not None or p["job"] != "BUS OPERATOR":
            continue
        if active_only and p["status"] != "ACTIVE":
            continue
        ex = sorted(phys[p["emp"]], key=lambda e: e["date"])
        if latest:
            s, w = ex[-1]["h_in"] * W.IN_TO_MM, ex[-1]["w_lb"] * W.LB_TO_KG
        else:
            s = float(np.mean([e["h_in"] for e in ex])) * W.IN_TO_MM
            w = float(np.mean([e["w_lb"] for e in ex])) * W.LB_TO_KG
        out.append({"emp": p["emp"], "sex": p["sex"], "s": s, "w": w, "pt": p["pt"], "status": p["status"],
                    "division": p["division"]})
    return out


def bounds(env):
    lo = np.array([env[d][0] if env[d][0] is not None else -INF for d in FIT], float)
    hi = np.array([env[d][1] if env[d][1] is not None else INF for d in FIT], float)
    return lo, hi


_PTS = {}


def normal_points(n_log2=15):
    if n_log2 not in _PTS:
        u = qmc.Sobol(d=5, scramble=True, seed=np.random.default_rng([W.SEED, 5])).random_base2(n_log2)
        _PTS[n_log2] = stats.norm.ppf(np.clip(u, 1e-12, 1 - 1e-12))
    return _PTS[n_log2]


def conditional(sx, given=COND_ON):
    """The survey's within-sex conditional normal of the five fit dimensions given the named measurements:
    a regression matrix, its intercept and the residual covariance."""
    mu, cov = W.survey_params(sx, FIT + given)
    k = len(FIT)
    s11, s12, s22 = cov[:k, :k], cov[:k, k:], cov[k:, k:]
    beta = s12 @ np.linalg.inv(s22)
    return mu[:k], mu[k:], beta, s11 - beta @ s12.T


def prob_inside(means, resid, lo, hi, n_log2=15):
    """Each row's probability that the five dimensions, normal about its mean with the residual covariance,
    all lie in [lo, hi]: quasi-Monte Carlo on one fixed point set."""
    x = normal_points(n_log2) @ np.linalg.cholesky(resid).T
    out = np.empty(len(means))
    for i in range(0, len(means), 24):
        m = means[i:i + 24]
        ins = np.all((x[None] >= (lo - m)[:, None]) & (x[None] <= (hi - m)[:, None]), axis=2)
        out[i:i + 24] = ins.mean(axis=1)
    return out


SEH = FIT.index("SEH")


def _seh_pred(sx, x, given=COND_ON):
    mfit, mgiv, beta, _ = conditional(sx, given)
    return mfit[SEH] + (np.asarray(x)[:, :len(given)] - mgiv) @ beta[SEH]


def trial_offsets(trial, how="per_sex", given=COND_ON):
    """How far the operators Halvard measured sit from the survey's within-sex normal given their own stature and
    weight (or stature alone): the mean departure of their sitting eye heights by sex (pooled over both sexes, or
    its median), the shift the survey's eye height takes for this workforce; the other four dimensions unmoved."""
    dev = {}
    for sx in ("M", "F"):
        tr = [t for t in trial if t["sex"] == sx]
        dev[sx] = np.array([t["seh"] for t in tr]) - _seh_pred(sx, [[t["s"], t["w"]] for t in tr], given)
    if how == "pooled":
        m = float(np.mean(np.r_[dev["M"], dev["F"]]))
        val = {sx: m for sx in dev}
    elif how == "median":
        val = {sx: float(np.median(dev[sx])) for sx in dev}
    else:
        val = {sx: float(np.mean(dev[sx])) for sx in dev}
    return {sx: np.where(np.arange(len(FIT)) == SEH, val[sx], 0.0) for sx in dev}


def trial_refit(trial, cols=2):
    """Each sex's sitting eye height regressed on stature and weight (or stature alone) among the operators
    measured; the eye height mean it gives each operator, in place of the survey's."""
    out = {}
    for sx in ("M", "F"):
        tr = [t for t in trial if t["sex"] == sx]
        X = np.c_[np.ones(len(tr)), [[t["s"], t["w"]][:cols] for t in tr]]
        b = np.linalg.lstsq(X, np.array([t["seh"] for t in tr]), rcond=None)[0]
        out[sx] = (lambda b, sx: (lambda x: np.outer(np.c_[np.ones(len(x)), np.asarray(x)[:, :cols]] @ b
                                                     - _seh_pred(sx, x), np.eye(len(FIT))[SEH])))(b, sx)
    return out


def trial_ratio(trial, pure=False):
    """Ratio scaling: the operators measured's mean ratio of sitting eye height to stature against the survey's
    ratio of means, the difference times each operator's stature added to the survey's eye height (or, pure, each
    operator's eye height their stature times the measured ratio)."""
    out = {}
    for sx in ("M", "F"):
        mu, _ = W.survey_params(sx, FIT + ["S"])
        e_v = float(np.mean([t["seh"] / t["s"] for t in trial if t["sex"] == sx]))
        de = e_v - mu[SEH] / mu[len(FIT)]
        if pure:
            out[sx] = (lambda e_v, sx: (lambda x: np.outer(e_v * np.asarray(x)[:, 0] - _seh_pred(sx, x),
                                                           np.eye(len(FIT))[SEH])))(e_v, sx)
        else:
            out[sx] = (lambda de: (lambda x: np.outer(de * np.asarray(x)[:, 0], np.eye(len(FIT))[SEH])))(de)
    return out


def trial_marginal(trial, ops=None):
    """The operators measured's mean sitting eye height by sex against the survey's mean (or, given the roster,
    against the mean the survey carried through stature and weight gives the counted operators): a shift read off
    the raw means, the volunteers' own build left in it."""
    out = {}
    for sx in ("M", "F"):
        v = float(np.mean([t["seh"] for t in trial if t["sex"] == sx]))
        if ops is None:
            mu, _ = W.survey_params(sx, FIT)
            ref = float(mu[SEH])
        else:
            ref = float(np.mean(_seh_pred(sx, [[o["s"], o["w"]] for o in ops if o["sex"] == sx])))
        out[sx] = np.where(np.arange(len(FIT)) == SEH, v - ref, 0.0)
    return out


def trial_weights(trial, ops):
    """Each operator measured weighted to the counted operators of the same sex on stature and weight: the odds of
    a logistic model of being measured against being on the roster, inverted."""
    w = {}
    for sx in ("M", "F"):
        xo = np.array([[o["s"], o["w"]] for o in ops if o["sex"] == sx])
        tr = [t for t in trial if t["sex"] == sx]
        xt = np.array([[t["s"], t["w"]] for t in tr])
        X = np.r_[xo, xt]
        mu, sd = X.mean(axis=0), X.std(axis=0)
        Xd = np.c_[np.ones(len(X)), (X - mu) / sd]
        y = np.r_[np.zeros(len(xo)), np.ones(len(xt))]
        b = np.zeros(Xd.shape[1])
        for _ in range(100):
            pr = 1 / (1 + np.exp(-Xd @ b))
            step = np.linalg.solve((Xd * (pr * (1 - pr))[:, None]).T @ Xd, Xd.T @ (y - pr))
            b += step
            if np.max(np.abs(step)) < 1e-10:
                break
        pt = 1 / (1 + np.exp(-Xd[len(xo):] @ b))
        w[sx] = (tr, (1 - pt) / pt)
    return w


def acc_carried(ops, env, given=COND_ON, plug=False, n_log2=15, per_op=False, offset=None):
    """Accommodation of the counted operators: each operator's probability of fitting under the survey's
    conditional normal given the named measurements, its means shifted by the workforce's offsets when given (a
    shift by sex, or one worked out from each operator's stature and weight), or, plugged, whether the conditional
    mean fits; averaged."""
    lo, hi = bounds(env)
    probs = []
    for sx in ("M", "F"):
        rows = [o for o in ops if o["sex"] == sx]
        mfit, mgiv, beta, resid = conditional(sx, given)
        x = np.array([[o["s"], o["w"]][:len(given)] if given == COND_ON else [o["s"]] for o in rows])
        means = mfit + (x - mgiv) @ beta.T
        if offset is not None:
            means = means + (offset[sx](np.array([[o["s"], o["w"]] for o in rows])) if callable(offset[sx])
                             else offset[sx])
        if plug:
            p = np.all((means >= lo) & (means <= hi), axis=1).astype(float)
        else:
            p = prob_inside(means, resid, lo, hi, n_log2)
        probs.extend(zip([o["emp"] for o in rows], p))
    if per_op:
        return dict(probs)
    return float(np.mean([p for _, p in probs]))


def acc_survey(env, mix):
    """The survey's own workers: the joint probability by sex, weighted to a sex mix."""
    lo, hi = bounds(env)
    tot = 0.0
    for sx in ("M", "F"):
        mu, cov = W.survey_params(sx, FIT)
        x = normal_points(17) @ np.linalg.cholesky(cov).T + mu
        tot += mix[sx] * float(np.mean(np.all((x >= lo) & (x <= hi), axis=1)))
    return tot


def marginals(env, mix):
    lo, hi = bounds(env)
    out = np.zeros(len(FIT))
    for sx in ("M", "F"):
        mu, cov = W.survey_params(sx, FIT)
        sd = np.sqrt(np.diag(cov))
        out += mix[sx] * (stats.norm.cdf(hi, mu, sd) - stats.norm.cdf(lo, mu, sd))
    return out


def f5m95(env):
    lo, hi = bounds(env)
    muf, covf = W.survey_params("F", FIT)
    mum, covm = W.survey_params("M", FIT)
    f5 = muf - 1.6449 * np.sqrt(np.diag(covf))
    m95 = mum + 1.6449 * np.sqrt(np.diag(covm))
    return bool(np.all(lo <= f5) and np.all(hi >= m95))


def pick(values):
    for c, _, _ in W.CONFIGS:
        if values[c] >= W.LINE:
            return c
    return None


def rungs(st, ops=None):
    ops = ops or counted(st)
    mix = {sx: sum(1 for o in ops if o["sex"] == sx) / len(ops) for sx in ("M", "F")}
    off = trial_offsets(st["trial"])
    marg = trial_marginal(st["trial"])
    out = {"G": {}, "R4": {}, "Rmarg": {}, "R1": {}, "R2": {}, "R3": {}, "R0a": {}, "Rind": {}, "R0b": {}}
    for c, opts, _ in W.CONFIGS:
        env = W.ENVELOPES[c]
        out["G"][c] = acc_carried(ops, env, offset=off)
        out["R4"][c] = acc_carried(ops, env)
        out["Rmarg"][c] = acc_carried(ops, env, offset=marg)
        out["R1"][c] = acc_survey(env, mix)
        out["R2"][c] = acc_carried(ops, env, given=["S"])
        out["R3"][c] = acc_carried(ops, env, plug=True)
        mg = marginals(env, mix)
        out["R0a"][c] = float(mg.min())
        out["Rind"][c] = float(np.prod(mg))
        out["R0b"][c] = 1.0 if f5m95(env) else 0.0
    picks = {k: pick(v) for k, v in out.items()}
    return out, picks, mix


# ---------------------------------------------------------------- the ask: what each option costs to maintain
def bus_months(buses, opt, roster_only=False, todays_options=False):
    """Months in the ask's years in which a bus was in the fleet and carried the option on the month's first day;
    the lazier paths keep only the buses on today's roster, or read today's options into every month."""
    n = 0
    for b in buses:
        if roster_only and b["disposed"] is not None:
            continue
        for d in W.month_starts(*W.ASK_YEARS):
            if not W.in_fleet(b, d):
                continue
            on = W.options_on(b, W.AS_OF) if todays_options else W.options_on(b, d)
            if opt in on:
                n += 1
    return n


def option_costs(wos, labour_per_line=False):
    """Parts and labour on the operator-area orders billed to the Authority and closed in the ask's years, by
    option component."""
    comp_of = {v[1]: k for k, v in W.COMPONENTS.items() if v[1]}
    cost = {o: 0.0 for o in W.OPTION_ORDER}
    for wo in wos:
        opt = W.COMPONENTS[wo["comp"]][1]
        if not opt or wo["bill"] != "TVRTA" or not (W.ASK_YEARS[0] <= wo["closed"].year <= W.ASK_YEARS[1]):
            continue
        parts = sum(round(ln["qty"] * ln["unit"], 2) for ln in wo["lines"])
        labour = round(wo["hours"] * wo["rate"], 2)
        cost[opt] += parts + labour * (len(wo["lines"]) if labour_per_line else 1)
    return {o: round(v, 2) for o, v in cost.items()}


def option_maintenance(st, labour_per_line=False, roster_only=False, todays_options=False):
    cost = option_costs(st["wos"], labour_per_line)
    out = {}
    for o in W.OPTION_ORDER:
        bm = bus_months(st["buses"], o, roster_only=roster_only, todays_options=todays_options)
        out[o] = {"cost": cost[o], "bus_months": bm, "bus_years": bm / 12.0, "rate": cost[o] / (bm / 12.0)}
    return out


def twelve_year(maint, rounded=False):
    out = {}
    for c, opts, price in W.CONFIGS:
        r = sum((round(maint[o]["rate"]) if rounded else maint[o]["rate"]) for o in opts)
        out[c] = price + 12 * r
    return out


# ---------------------------------------------------------------- the figures the write-up and goldens carry
def figures(st):
    ops = counted(st)
    out, picks, mix = rungs(st, ops)
    acc = out["G"]
    call = picks["G"]
    order = [c for c, _, _ in W.CONFIGS]
    cheaper = order[:order.index(call)]
    near = max(cheaper, key=lambda c: acc[c])
    nxt = cheaper[-1]
    maint = option_maintenance(st)
    twelve = twelve_year(maint)
    men = sum(1 for o in ops if o["sex"] == "M")
    fig = {
        "call": {"config": call, "options": [W.OPTIONS[o] for o in dict((c, o) for c, o, _ in W.CONFIGS)[call]],
                 "price": W.PRICES[call], "acc_pct": round(100 * acc[call], 1),
                 "nearest_cheaper": near, "nearest_cheaper_pct": round(100 * acc[near], 1),
                 "next_cheaper": nxt, "next_cheaper_pct": round(100 * acc[nxt], 1)},
        "operators": {"n": len(ops), "men": men, "women": len(ops) - men,
                      "share_women_pct": round(100 * (len(ops) - men) / len(ops), 1)},
        "acc": {c: round(acc[c], 9) for c in order},
        "acc_pct": {c: round(100 * acc[c], 1) for c in order},
        "meets": {c: bool(acc[c] >= W.LINE) for c in order},
        "prices": {c: W.PRICES[c] for c in order},
        "rungs": {k: {c: round(v[c], 9) for c in order} for k, v in out.items()},
        "rung_pct": {k: {c: round(100 * v[c], 1) for c in order} for k, v in out.items() if k not in ("R0b",)},
        "rung_picks": picks,
        "maint": {o: {"cost": maint[o]["cost"], "cost_dollars": int(round(maint[o]["cost"])),
                      "bus_months": maint[o]["bus_months"],
                      "bus_years": round(maint[o]["bus_years"], 1), "rate": round(maint[o]["rate"])}
                  for o in W.OPTION_ORDER},
        "maint_exact": {o: {"rate": round(maint[o]["rate"], 9), "bus_years": round(maint[o]["bus_years"], 9)}
                        for o in W.OPTION_ORDER},
        "twelve": {c: int(round(twelve[c])) for c in order},
        "line_pct": 95,
        "units": {"in_to_mm": W.IN_TO_MM, "lb_to_kg": W.LB_TO_KG},
        "years": list(W.ASK_YEARS),
        "as_of": W.AS_OF.isoformat(),
        "roster": {"day": W.AS_OF.day, "year": W.AS_OF.year},
        "survey": {"men_n": W.SAMPLE["M"], "women_n": W.SAMPLE["F"], "year": W.SURVEY_YEAR},
    }
    # what Halvard measured: the operators, their build and how far their eye heights sit from the survey's normal
    tr = st["trial"]
    off = trial_offsets(tr)
    marg = trial_marginal(tr)
    fig["trial"] = {"n": len(tr), "men": sum(1 for t in tr if t["sex"] == "M"),
                    "women": sum(1 for t in tr if t["sex"] == "F"),
                    "eye_height_offset_mm": {sx: round(float(off[sx][SEH]), 1) for sx in ("M", "F")},
                    "eye_height_offset_exact": {sx: round(float(off[sx][SEH]), 9) for sx in ("M", "F")},
                    "raw_eye_height_gap_mm": {sx: round(float(marg[sx][SEH]), 1) for sx in ("M", "F")},
                    "stature_mean": {sx: round(float(np.mean([t["s"] for t in tr if t["sex"] == sx])), 1)
                                     for sx in ("M", "F")},
                    "weight_mean": {sx: round(float(np.mean([t["w"] for t in tr if t["sex"] == sx])), 1)
                                    for sx in ("M", "F")}}
    # the operators' build at their latest physical against the survey's workers (for the note, never graded)
    for sx in ("M", "F"):
        s = np.array([o["s"] for o in ops if o["sex"] == sx])
        w = np.array([o["w"] for o in ops if o["sex"] == sx])
        fig.setdefault("build", {})[sx] = {"stature_mean": round(float(s.mean()), 1), "stature_sd": round(float(s.std(ddof=1)), 1),
                                           "weight_mean": round(float(w.mean()), 1), "weight_sd": round(float(w.std(ddof=1)), 1)}
    return fig
