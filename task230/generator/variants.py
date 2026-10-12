"""Every candidate method on the shipped files: the ladder's rungs, the attribute family the default path
picks from, the own-rate and mix models, the rigorous family that must converge, and the form 1 separation
(slopes, held-out shift-days, the shares test, support, the collapsing terms)."""
import copy
import itertools

import numpy as np
import pandas as pd
from scipy.stats import chi2

import analysis as AN
import glm
import world as W


def spec(base, **kw):
    s = copy.deepcopy(base)
    s.update(kw)
    return s


def with_terms(base, add=(), drop=()):
    s = copy.deepcopy(base)
    s["terms"] = [t for t in s["terms"] if t[1] not in drop] + [("cat", a) for a in add]
    s["name"] = base["name"] + "".join(f" +{a}" for a in add) + "".join(f" -{d}" for d in drop)
    return s


# ----------------------------------------------------------------------------------------------- special fits
def fixed_slope(Qr, slope, C=None):
    """the golden model refitted with its slope held at a value (the corridor's ends)"""
    base = spec(AN.GOLDEN, x=None)
    m = AN.fit_spec(Qr, base, C=C, offset=lambda c: slope * c.lp)
    names = ["const", "lp"] + m["names"][1:]
    b = np.concatenate([[m["b"][0], slope], m["b"][1:]])
    return dict(m, names=names, b=b, spec=AN.GOLDEN)


def decile_forecast(Qr, sc):
    C = Qr.C.copy()
    days = np.log(Qr.pool.values)
    edges = np.quantile(days, np.linspace(0, 1, 11))
    C["dec"] = np.clip(np.searchsorted(edges, C.lp, side="right") - 1, 0, 9)
    centres = pd.Series(days).groupby(np.clip(np.searchsorted(edges, days, side="right") - 1, 0, 9)).median().values
    s = dict(name="deciles", x=None, terms=[("cat", "dec")] + AN.GOLDEN["terms"], link="logit")
    X, names, lv = glm.design(C, AN._terms(s))
    m = glm.fit(X, C.y, C.n)
    coef = np.concatenate([[0.0], [m["b"][names.index(f"dec={d}")] for d in lv["dec"][1:]]])

    def xfun(D):
        return np.interp(D.lp.values, centres, coef)
    # the decile effect enters as an offset-like numeric column named 'dfx' with coefficient 1
    base_names = [n for n in names if not n.startswith("dec=")]
    keep = [i for i, n in enumerate(names) if not n.startswith("dec=")]
    b = np.concatenate([[m["b"][0], 1.0], m["b"][keep[1:]]])
    mm = dict(m, names=["const", "dfx"] + base_names[1:], b=b, lv=lv, spec=dict(s, x="dfx", terms=AN.GOLDEN["terms"]))
    return AN.forecast(Qr, sc, mm, xfun=xfun)


def experienced_rate(Qr):
    """each verifier's own experienced OCR error rate over the last 500 key fields screened, from field edits"""
    scr = Qr.scr.sort_values(["emp", "closed_at"])
    a = Qr.a
    mbar = a.miss.sum() / a.err.sum()
    fa = Qr.fa_rate
    for e, g in scr.groupby("emp", sort=False):
        kf = g.key_fields.values.astype(float)
        ek = g.fields_keyed_over.values.astype(float)
        ck = np.concatenate([[0], np.cumsum(kf)])
        ce = np.concatenate([[0], np.cumsum(ek)])
        j = np.searchsorted(ck, ck[1:] - 500, side="left")
        j = np.maximum(j, 0)
        fields = ck[1:] - ck[j]
        edits = ce[1:] - ce[j]
        r = (edits / np.maximum(fields, 1) - fa) / (1 - mbar)
        scr.loc[g.index, "xr"] = np.clip(r, 0.002, 0.2)
    return scr.set_index("document_id").xr


def exp500_forecast(Qr, sc):
    xr = experienced_rate(Qr)
    E = Qr.E.copy()
    E["lx"] = np.log(E.document_id.map(xr).values)
    keys = ["queue", "day", "code", "fam", "ftype", "emp", "ten", "lx"]
    C = E.groupby(keys).agg(y=("miss", "sum"), n=("miss", "size")).reset_index()
    s = dict(name="experienced 500", x="lx", terms=AN.GOLDEN["terms"], link="logit")
    X, names, lv = glm.design(C, AN._terms(s))
    m = glm.fit(X, C.y, C.n)
    m.update(names=names, lv=lv, spec=s)
    return AN.forecast(Qr, sc, m, xfun=lambda D: D.lp.values), m


def sdt_forecast(Qr, sc):
    """equal-variance signal detection: per-verifier sensitivity, a criterion moving with the log odds of the
    shift-day's OCR error rate, misses and false alarms fitted together (probit)"""
    C = Qr.C.copy()
    a = Qr.a.join(Qr.pool, on=["day", "queue"])
    ok = a[~a.err]
    Fa = ok.groupby(["queue", "day", "emp", "pool"]).agg(y=("fa", "sum"), n=("fa", "size")).reset_index()
    Xm, names, lv = glm.design(C, AN._terms(spec(AN.GOLDEN, x="lgt")))
    Xm = np.column_stack([Xm[:, :1], np.zeros(len(C)), Xm[:, 1:]])
    lg = np.log(Fa.pool / (1 - Fa.pool)).values
    Xf = np.zeros((len(Fa), Xm.shape[1]))
    Xf[:, 1] = 1.0
    Xf[:, 2] = -lg
    X = np.vstack([Xm, Xf])
    y = np.concatenate([C.y.values, Fa.y.values])
    n = np.concatenate([C.n.values, Fa.n.values])
    m0 = glm.fit(Xm[:, [0] + list(range(2, Xm.shape[1]))], C.y.values, C.n.values, link="probit")
    from scipy.stats import norm
    init = np.insert(m0["b"], 1, norm.ppf(max(Fa.y.sum() / Fa.n.sum(), 1e-6)))
    init[2] = m0["b"][1]
    m = glm.fit(X, y, n, link="probit", b0=init)
    # forecast with the miss half: drop the false-alarm intercept column
    b = np.delete(m["b"], 1)
    mm = dict(m, b=b, names=names, lv=lv, spec=spec(AN.GOLDEN, x="lgt", link="probit"))
    res = AN.forecast(Qr, sc, mm)
    return res, m


def own_rate_model(Qr):
    a = Qr.a
    st = a.groupby(["day", "code"]).agg(e=("err", "sum"), n=("err", "size"))
    own = np.log((st.e + 0.5) / (st.n + 1)).rename("lo")
    C = Qr.C.join(own, on=["day", "code"])
    s = dict(name="own stream rate", x="lo", terms=AN.GOLDEN["terms"] + [("cat", "queue")], link="logit")
    return s, C


def mix_test(Qr):
    """the stream shares of the shift-day's key fields add nothing once the OCR error rate is in"""
    f = Qr.scr.groupby(["day", "queue", "code"]).key_fields.sum().unstack(fill_value=0)
    sh = f.div(f.sum(axis=1), axis=0)
    cols = [c for c in W.ORDER if c not in ("N1", "D1")]
    sh = sh.reindex(columns=cols, fill_value=0.0)
    sh.columns = [f"sh_{c}" for c in cols]
    C = Qr.C.join(sh, on=["day", "queue"])
    base = AN.fit_spec(Qr, AN.GOLDEN, C=C)
    X, names, lv = glm.design(C, AN._terms(AN.GOLDEN) + list(sh.columns))
    mf = glm.fit(X, C.y, C.n)
    lr = 2 * (mf["ll"] - base["ll"])
    return dict(lr=lr, df=len(sh.columns), p=float(chi2.sf(lr, len(sh.columns))))


def heldout(Qr, specs, folds=5, C=None):
    """squared error of each model's predicted audited misses per queue and shift-day, shift-days held out"""
    C = Qr.C if C is None else C
    days = sorted(C.day.unique())
    fold = {d: i % folds for i, d in enumerate(days)}
    f = C.day.map(fold).values
    out = {}
    for s in specs:
        se = 0.0
        for k in range(folds):
            tr, te = C[f != k], C[f == k]
            X, names, lv = glm.design(tr, AN._terms(s))
            m = glm.fit(X, tr.y, tr.n, link=s.get("link", "logit"))
            Xt, _, _ = glm.design(te, AN._terms(s), lv)
            p = glm.predict(dict(m, link=s.get("link", "logit")), Xt)
            t = te.assign(pr=p * te.n).groupby(["queue", "day"])[["y", "pr"]].sum()
            se += float(((t.y - t.pr) ** 2).sum())
        out[s["name"]] = se
    return out


def within_queue(Qr, sc):
    out, slopes = {}, {}
    for q in ("D", "N"):
        C = Qr.C[Qr.C.queue == q]
        m = AN.fit_spec(Qr, AN.GOLDEN, C=C)
        j = m["names"].index("lp")
        slopes[q] = (float(m["b"][j]), float(m["se"][j]))
        r = AN.forecast(Qr, sc, m)
        for c in W.ORDER:
            if sc.nov_queue[c] == q:
                out[c] = r[c]
    return out, slopes


def family_slopes(Qr):
    C = Qr.C.copy()
    rows = {}
    for fam in ("printed", "mixed", "handwritten", "typed"):
        C[f"lp_{fam}"] = np.where(C.fam == fam, C.lp, 0.0)
    s = dict(name="slope by family", x=None, terms=[f"lp_{f}" for f in ("printed", "mixed", "handwritten", "typed")] + AN.GOLDEN["terms"], link="logit")
    X, names, lv = glm.design(C, AN._terms(s))
    m = glm.fit(X, C.y, C.n)
    for f in ("printed", "mixed", "handwritten", "typed"):
        j = names.index(f"lp_{f}")
        rows[f] = (float(m["b"][j]), float(m["se"][j]))
    return rows


def collapsing_terms(Qr):
    """the queue, Saturday and holiday terms of the best attribute model, with and without the OCR error rate"""
    att = AN.ATTRIBUTE[4]
    m0 = AN.fit_spec(Qr, att)
    m1 = AN.fit_spec(Qr, spec(att, x="lp"))
    out = {}
    for nm in m0["names"]:
        if nm.startswith("qdow="):
            j0 = m0["names"].index(nm)
            j1 = m1["names"].index(nm)
            out[nm] = dict(without=float(m0["b"][j0]), z_without=float(m0["b"][j0] / m0["se"][j0]),
                           with_rate=float(m1["b"][j1]), z_with=float(m1["b"][j1] / m1["se"][j1]))
    return out


def monthly_backtest(Qr, s):
    """month by month: each stream-month's audited misses against the model's prediction, in standard errors
    inflated by the model's own overdispersion over stream and shift-day"""
    C = Qr.C
    m = AN.fit_spec(Qr, s)
    X, _, _ = glm.design(C, AN._terms(s), m["lv"])
    p = glm.predict(m, X)
    od = max(1.0, overdispersion(Qr, s))
    t = C.assign(pr=p * C.n, v=p * (1 - p) * C.n).groupby(["code", "month"])[["y", "pr", "v"]].sum()
    rows = [(c, mo, float((r.y - r.pr) / np.sqrt(r.v * od))) for (c, mo), r in t.iterrows()]
    return max(abs(z) for _, _, z in rows), rows


def overdispersion(Qr, s, grain=("code", "day")):
    m = AN.fit_spec(Qr, s)
    X, _, _ = glm.design(Qr.C, AN._terms(s), m["lv"])
    p = glm.predict(m, X)
    t = Qr.C.assign(pr=p * Qr.C.n, v=p * (1 - p) * Qr.C.n).groupby(list(grain))[["y", "pr", "v"]].sum()
    return float(((t.y - t.pr) ** 2 / t.v).sum() / max(1, len(t) - len(m["b"])))


# ----------------------------------------------------------------------------------------------- the run
def run(pk, quiet=True):
    Qr = AN.Quarter(pk)
    sc = AN.Scenario(pk, Qr)
    L = pk.limits
    R = {}
    g = AN.fit_spec(Qr, AN.GOLDEN)
    j = g["names"].index("lp")
    slope, se = float(g["b"][j]), float(g["se"][j])
    R["golden"] = AN.forecast(Qr, sc, g)
    R["R0"] = Qr.q3_measured()
    R["R2"] = AN.forecast(Qr, sc, g, night_fx=False)
    R["R3"] = dict(AN.forecast(Qr, sc, g), D6=Qr.q3_measured()["D6"])
    att = {}
    aic = {}
    for a in AN.ATTRIBUTE:
        m = AN.fit_spec(Qr, a)
        att[a["name"]] = AN.forecast(Qr, sc, m)
        aic[a["name"]] = m["aic"]
    best = min(aic, key=aic.get)
    R["R1"] = att[best]
    # grid: roster, day effect, night effect, the new client inside the model
    grid = {}
    for ro, dfx, nfx, hp in itertools.product([0, 1], [0, 1], [0, 1], [0, 1]):
        r = AN.forecast(Qr, sc, g, night_fx=bool(nfx), day_fx=bool(dfx), hp_in_model=bool(hp), roster=bool(ro))
        if not hp:
            r = dict(r, D6=R["R0"]["D6"])
        grid[(ro, dfx, nfx, hp)] = r
    # the rigorous family
    V = {}
    lin = AN.fit_spec(Qr, spec(AN.GOLDEN, name="linear probability", x="lin", link="identity"))
    V["linear probability in the rate"] = AN.forecast(Qr, sc, lin)
    V["rate in deciles, interpolated"] = decile_forecast(Qr, sc)
    V["verifier's experienced rate, last 500 fields"], _ = exp500_forecast(Qr, sc)
    V["signal detection, misses and false alarms"], _ = sdt_forecast(Qr, sc)
    Qe = AN.Quarter(pk, pool_mode="edit")
    V["rate from field edits plus audited misses"] = AN.forecast(Qe, AN.Scenario(pk, Qe), AN.fit_spec(Qe, AN.GOLDEN))
    Qp = AN.Quarter(pk, pool_mode="plain")
    V["rate from the audit unstratified"] = AN.forecast(Qp, AN.Scenario(pk, Qp), AN.fit_spec(Qp, AN.GOLDEN))
    for add, drop in [(("tos",), ()), (("tos", "ton", "wlb", "qdow"), ()), ((), ("ten",)), ((), ("emp",)), (("queue",), ())]:
        s = with_terms(AN.GOLDEN, add, drop)
        V["golden " + s["name"][7:]] = AN.forecast(Qr, sc, AN.fit_spec(Qr, s))
    wq, slopes = within_queue(Qr, sc)
    V["fitted within each queue"] = wq
    V["November rates as monthly averages"] = AN.forecast(Qr, sc, g, monthly=True)
    lo, hi = slope - 1.96 * se, slope + 1.96 * se
    V["slope at the interval's shallow end"] = AN.forecast(Qr, sc, fixed_slope(Qr, hi))
    V["slope at the interval's steep end"] = AN.forecast(Qr, sc, fixed_slope(Qr, lo))
    # main-path texture repaired or not (clean-data test) and the semantic forks that converge
    T = {}
    for nm, kw in [("timeouts kept", dict(keep_timeouts=True)), ("badges joined naively", dict(naive_badge=True)),
                   ("calendar-day attribution", dict(calendar_day=True)), ("verifier-introduced errors dropped", dict(drop_fa=True))]:
        Qx = AN.Quarter(pk, **kw)
        scx = AN.Scenario(pk, Qx)
        T[nm] = dict(golden=AN.forecast(Qx, scx, AN.fit_spec(Qx, AN.GOLDEN)),
                     default=AN.forecast(Qx, scx, AN.fit_spec(Qx, [a for a in AN.ATTRIBUTE if a["name"] == best][0])))
    T["closed-quarter roster"] = dict(golden=grid[(0, 1, 1, 1)], default=AN.forecast(Qr, sc, AN.fit_spec(Qr, [a for a in AN.ATTRIBUTE if a["name"] == best][0]), roster=False))
    # separation
    own_s, own_C = own_rate_model(Qr)
    own_m = AN.fit_spec(Qr, own_s, C=own_C)
    specs = [AN.GOLDEN] + AN.ATTRIBUTE
    ho = heldout(Qr, specs)
    ho_own = heldout(Qr, [own_s], C=own_C)
    ho.update(ho_own)
    gold_with_own = heldout(Qr, [AN.GOLDEN], C=own_C)
    mix = mix_test(Qr)
    fam_sl = family_slopes(Qr)
    coll = collapsing_terms(Qr)
    bt = {a["name"]: monthly_backtest(Qr, a)[0] for a in AN.ATTRIBUTE}
    od = {a["name"]: overdispersion(Qr, a) for a in AN.ATTRIBUTE}
    od_q = overdispersion(Qr, [a for a in AN.ATTRIBUTE if a["name"] == best][0], grain=("queue", "day"))
    # support and the November mix
    nov_rate = sc.monthly(Qr.p_hat)
    pr = Qr.pool.reset_index()
    support = {"D": int((pr[pr.queue == "D"].pool <= nov_rate["D"]).sum()), "N": int((pr[pr.queue == "N"].pool >= nov_rate["N"]).sum())}
    emp_q = Qr.E.groupby("emp").queue.nunique()
    ro_emps = sc.roster.emp.tolist()
    both = all(emp_q.get(e, 2) == 2 for e in ro_emps if e in emp_q.index)
    f = Qr.scr.groupby(["day", "queue", "code"]).key_fields.sum().unstack(fill_value=0)
    sh = f.div(f.sum(axis=1), axis=0)
    pl = sc.plan.groupby(["queue", "code"]).kf.sum()
    nov_share = {"D6": float(pl[("D", "D6")] / pl.xs("D").sum()), "D5": float(pl[("N", "D5")] / pl.xs("N").sum())}
    q3_max = {"D6": float(sh.xs("D", level="queue")["D6"].max()), "D5": float(sh.xs("N", level="queue").get("D5", pd.Series([0.0])).max())}
    return dict(Qr=Qr, sc=sc, limits=L, slope=(slope, se), golden_model=g, R=R, att=att, aic=aic, best=best, grid=grid, V=V,
                T=T, slopes_within=slopes, heldout=ho, heldout_own_base=gold_with_own, mix=mix, fam_slopes=fam_sl,
                collapse=coll, backtest=bt, od=od, od_queue_day=od_q, support=support, verifiers_both_queues=both,
                nov_share=nov_share, q3_max_share=q3_max, nov_rate=nov_rate, monthly_pool=Qr.monthly_pool(),
                own=AN.forecast(Qr, sc, own_m, xfun=lambda D: np.log(D.code.map(Qr.p_hat).values)))
