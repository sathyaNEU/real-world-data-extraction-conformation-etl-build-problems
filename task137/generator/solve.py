"""The golden and every rung, computed from the shipped files alone."""
import datetime as dt
import os
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
import docs as DC
import params as P

F = DC.FILES
G2 = (1 + P.GROWTH) ** 2
ROUND = 2500
FY0, FY1 = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
TEMPLATES = dt.date(2026, 4, 1)
WINDOWS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12)
LAGS = 26


def rnd(x, u=ROUND):
    return int(round(x / float(u)) * u)


def load_seen(target):
    leg = pd.read_csv(os.path.join(target, F["legacy"]), dtype=str)
    leg = leg[leg.Outcome == "Seen"].copy()
    leg["d"] = pd.to_datetime(leg.Date, format="%d/%m/%Y").dt.date
    leg = leg[leg.d < P.NEW_SYSTEM_LIVE]
    leg["g"] = np.where(leg.Request == "GP form", "GP", "HOSP")
    ev = pd.read_csv(os.path.join(target, F["events"]), dtype=str)
    ci = ev[ev.event_type == "CHECKED_IN"].copy()
    ci["d"] = pd.to_datetime(ci.event_utc, utc=True).dt.tz_convert("Europe/London").dt.date
    ci["g"] = ci.request_type
    s1 = leg.groupby(["d", "g"]).size().unstack(fill_value=0)
    s2 = ci.groupby(["d", "g"]).size().unstack(fill_value=0)
    return pd.concat([s1, s2]).fillna(0).astype(int), ci, ev


def load_log(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, F["log"]), data_only=True)
    out = {}
    for ws in wb.worksheets:
        hdr = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Date":
                hdr = row
                continue
            if hdr is None or not row or row[0] is None:
                continue
            d = row[0]
            if isinstance(d, str):
                try:
                    d = dt.datetime.strptime(d.strip(), "%d/%m/%Y")
                except ValueError:
                    continue
            if isinstance(d, dt.datetime):
                d = d.date()
            if not isinstance(d, dt.date):
                continue
            if "GP form AM" in hdr:
                gp = (row[3] or 0) + (row[4] or 0)
                h = (row[5] or 0) + (row[6] or 0)
                if gp + h > 0:
                    out[d] = (gp, h)
            else:
                out[d] = (row[2] or 0, row[3] or 0)
    return out


def daily(target):
    seen, ci, ev = load_seen(target)
    log = load_log(target)
    D = pd.DataFrame({"d": seen.index, "seen_gp": seen["GP"].values, "seen_h": seen["HOSP"].values})
    D["away_gp"] = [log.get(d, (0, 0))[0] for d in D.d]
    D["away_h"] = [log.get(d, (0, 0))[1] for d in D.d]
    D["ro"] = [1 if d in log else 0 for d in D.d]
    D["arr"] = D.seen_gp + D.away_gp
    D["wd"] = [d.weekday() for d in D.d]
    D["mo"] = [d.month for d in D.d]
    D["t"] = [(d - P.START).days / 365.25 for d in D.d]
    gaps = [1] + [(D.d.iloc[i] - D.d.iloc[i - 1]).days for i in range(1, len(D))]
    D["pbh"] = [1 if g not in (1, 3) else 0 for g in gaps]
    D["wk"] = [d - dt.timedelta(d.weekday()) for d in D.d]
    D["fy"] = [d.year - (d.month < 4) for d in D.d]
    # the kiosk's allocation: a day whose check-ins reached it had nothing left to issue
    k = pd.read_csv(os.path.join(target, F["kiosk"]), dtype=str)
    cap = dict(zip(pd.to_datetime(k.Date, format="%d/%m/%Y").dt.date, k.Tickets.astype(int)))
    D["full"] = [int(a + b >= cap.get(d, 10 ** 6)) for d, a, b in zip(D.d, D.seen_gp, D.seen_h)]
    # each earlier calendar week's run-out share (its logged run-out days over its clinic days), and their means
    wk = D.groupby("wk").ro.agg(["sum", "size"])
    share = (wk["sum"] / wk["size"]).to_dict()
    for j in range(1, LAGS + 1):
        D["w%d" % j] = [share.get(w - dt.timedelta(7 * j), 0.0) for w in D.wk]
    for L in range(1, 13):
        D["s%d" % L] = D[["w%d" % j for j in range(1, L + 1)]].mean(axis=1)
    D["p1"], D["p2"] = D.s1, D.s2
    ro = D.ro.values
    for W in (5, 10, 20, 40):
        D["r%d" % W] = [ro[max(0, i - W):i].mean() if i > 0 else 0 for i in range(len(ro))]
    return D.reset_index(drop=True), ci, ev


def calX(D, extra=(), month=True, trend=True):
    Z = pd.get_dummies(D[["wd", "mo"] if month else ["wd"]].astype(str), drop_first=True).astype(float)
    if trend:
        Z["t"] = D.t.values
    Z["pbh"] = D.pbh.values
    for c in extra:
        Z[c] = D[c].values
    return sm.add_constant(Z, has_constant="add")


def window(D, y="arr"):
    """The run-out window the record's fit picks: the mean run-out share of the previous L calendar weeks, L from one
    to twelve, by AIC."""
    aic = {L: sm.GLM(D[y], calX(D, ["s%d" % L]), family=sm.families.Poisson()).fit().aic for L in WINDOWS}
    return min(aic, key=aic.get), aic


def deterred(D, col=None, fam=None, y="arr"):
    col = col or "s%d" % window(D, y)[0]
    fam = fam or sm.families.Poisson()
    m = sm.GLM(D[y], calX(D, [col]), family=fam).fit()
    b = m.params[col]
    fy = (D.fy == 2025).values
    base = float((D[y].values[fy] * np.exp(-b * D[col].values[fy])).sum())
    return base, float(b), float(m.bse[col]), float(m.aic)


def golden(D):
    L, aic = window(D)
    col = "s%d" % L
    base, b, se, a = deterred(D, col)
    fy = (D.fy == 2025).values
    return {"base": base, "b": b, "se": se, "aic": aic, "L": L, "col": col, "plan": base * G2, "plan_r": rnd(base * G2),
            "seen_gp": int(D.seen_gp[fy].sum()), "away_gp": int(D.away_gp[fy].sum()),
            "kept": base - float(D.arr[fy].sum()), "ro_days": int(D.ro[fy].sum()), "days": int(fy.sum())}


def _undo(D, X, cols):
    m = sm.GLM(D.arr, X, family=sm.families.Poisson()).fit()
    fy = (D.fy == 2025).values
    eta = sum(m.params[c] * D[c].values for c in cols)
    return float((D.arr.values[fy] * np.exp(-eta[fy])).sum()), float(m.aic)


def distributed(D, n=10):
    """Each of the previous n weeks' run-out shares with its own coefficient."""
    cols = ["w%d" % j for j in range(1, n + 1)]
    return _undo(D, calX(D, cols), cols)


def kernel(D, weights):
    Q = D.copy()
    w = np.asarray(weights, float) / np.sum(weights)
    Q["kx"] = sum(w[j - 1] * Q["w%d" % j].values for j in range(1, len(w) + 1))
    return _undo(Q, calX(Q, ["kx"]), ["kx"])


def geometric(D):
    """A geometric decay over the previous 26 weeks, its rate chosen by AIC."""
    fits = {round(r, 2): kernel(D, [r ** (j - 1) for j in range(1, LAGS + 1)]) for r in np.arange(0.60, 0.981, 0.02)}
    r = min(fits, key=lambda k: fits[k][1])
    return fits[r][0], r, fits[r][1]


def linear(D):
    """A linearly declining weight over the previous n weeks, n chosen by AIC."""
    fits = {n: kernel(D, [n - j + 1 for j in range(1, n + 1)]) for n in range(4, 25)}
    n = min(fits, key=lambda k: fits[k][1])
    return fits[n][0], n, fits[n][1]


def weekly_totals(D, col):
    W = D.groupby("wk").agg(arr=("arr", "sum"), n=("d", "size"), x=(col, "first"), fy=("fy", "first"),
                            mo=("mo", "first"), t=("t", "mean")).reset_index()
    Z = pd.get_dummies(W[["mo"]].astype(str), drop_first=True).astype(float)
    Z["t"] = W.t.values
    Z["x"] = W.x.values
    b = sm.GLM(W.arr, sm.add_constant(Z), family=sm.families.Poisson(), offset=np.log(W.n)).fit().params["x"]
    fw = (W.fy == 2025).values
    return float((W.arr.values[fw] * np.exp(-b * W.x.values[fw])).sum())


def family(D, ci, L):
    """Every reasonable implementation of the decisive step, at the window the record's fit picks."""
    col = "s%d" % L
    fy = (D.fy == 2025).values
    out = {}
    out["the chosen window's share, negative binomial"] = deterred(D, col, sm.families.NegativeBinomial(alpha=0.01))[0] * G2
    for l in (L - 1, L + 1):
        out["the mean run-out share of the previous %d weeks" % l] = deterred(D, "s%d" % l)[0] * G2
    out["the run-out share of the previous 40 clinic days"] = deterred(D, "r40")[0] * G2
    out["ten weekly lags of the run-out share, each its own coefficient"] = distributed(D, 10)[0] * G2
    out["twelve weekly lags of the run-out share, each its own coefficient"] = distributed(D, 12)[0] * G2
    out["weekly totals on the chosen window's share"] = weekly_totals(D, col) * G2
    out["a geometric decay over 26 weeks, its rate by AIC"] = geometric(D)[0] * G2
    out["a linear decay, its length by AIC"] = linear(D)[0] * G2
    # instrument: the window's hospital-clinic arrivals for the window's run-out share
    wh = D.assign(ah=D.seen_h + D.away_h).groupby("wk").ah.mean()
    D2 = D.copy()
    D2["ph"] = [np.mean([wh.get(w - dt.timedelta(7 * j), np.nan) for j in range(1, L + 1)]) for w in D2.wk]
    M = D2.dropna(subset=["ph"])
    Zm = calX(M, ["ph"])
    biv = sm.GLM(M.arr, Zm, family=sm.families.Poisson()).fit().params["ph"] / sm.OLS(M[col], Zm).fit().params["ph"]
    out["the chosen window's share instrumented by its hospital-clinic arrivals"] = float((D.arr.values[fy] * np.exp(-biv * D[col].values[fy])).sum()) * G2
    out["practices with a clinic against practices without, the chosen window"] = _did(D, ci, col) * G2
    return out


def family_more(D, target, L):
    """The window's other specifications a judge or a careful solver might fit: added covariates, other estimators,
    other fitting spans, and the quiet-period fits that leave out the days a run-out could have reached."""
    col = "s%d" % L
    fy = (D.fy == 2025).values
    out = {}
    Q = D.copy()
    Q["vac"] = [1 if P.VACANCY[0] <= d <= P.VACANCY[1] else 0 for d in Q.d]
    r = roster(target)
    on = r[(r.Absence.isna() | (r.Absence == "")) & (r.Hours > 0)].groupby("d").size()
    Q["heads"] = Q.d.map(on).fillna(0).values
    Q["H"] = (Q.seen_h + Q.away_h).values / 100.0
    Q["Hwk"] = Q.groupby("wk").H.transform("mean").values

    def undo(extra, M=None):
        M = Q if M is None else M
        m = sm.GLM(M.arr, calX(M, [col] + extra), family=sm.families.Poisson()).fit()
        return float((Q.arr.values[fy] * np.exp(-m.params[col] * Q[col].values[fy])).sum()) * G2
    for lab, ex in (("with a vacancy dummy", ["vac"]), ("with the phlebotomists on the floor", ["heads"]),
                    ("with the day's hospital-form arrivals", ["H"]), ("with the week's hospital-form arrivals", ["Hwk"]),
                    ("with the previous week's share as well", ["s1"])):
        out["the chosen window, " + lab] = undo(ex)
    out["the chosen window, fitted from April 2024"] = undo([], Q[Q.fy >= 2024])
    out["the chosen window, fitted on the new system's days"] = undo([], Q[Q.d >= P.NEW_SYSTEM_LIVE])
    m = sm.GLM(Q.arr, calX(Q, [col]), family=sm.families.Poisson()).fit()
    X0 = calX(Q, [col]).copy()
    X0[col] = 0
    out["the chosen window, the fitted mean at a share of nil"] = float(m.predict(X0)[fy].sum()) * G2
    b = sm.OLS(np.log(Q.arr.clip(lower=1)), calX(Q, [col])).fit().params[col]
    out["the chosen window, least squares on log arrivals"] = float((Q.arr.values[fy] * np.exp(-b * Q[col].values[fy])).sum()) * G2
    b = sm.OLS(Q.arr, calX(Q, [col])).fit().params[col]
    out["the chosen window, least squares on arrivals"] = float((Q.arr.values[fy] - b * Q[col].values[fy]).sum()) * G2
    return out


def quiet(D, L):
    """Quiet-period fits: calendar terms fitted on the days the window leaves untouched, predicted for every 2025-26 day;
    with the months those days never reach."""
    fy = (D.fy == 2025).values
    out = {}
    for lab, mask in (("days whose previous %d weeks did not run out" % L, D["s%d" % L].values == 0),
                      ("days whose previous four weeks did not run out", D.s4.values == 0)):
        mm = sm.GLM(D.arr[mask], calX(D)[mask], family=sm.families.Poisson()).fit()
        missing = sorted(set(range(1, 13)) - set(D.mo[mask]))
        out["quiet-period fit on " + lab] = (float(mm.predict(calX(D))[fy].sum()) * G2, int(mask.sum()), missing)
    return out


def family_extra(D, L):
    """Other exposure forms of the window's run-outs, and fits with fewer calendar controls."""
    col = "s%d" % L
    fy = (D.fy == 2025).values
    Q = D.copy()
    wk = Q.groupby("wk").agg(ro=("ro", "sum"), away=("away_gp", "sum"), awayh=("away_h", "sum"))
    back = lambda c: np.array([np.mean([wk[c].get(w - dt.timedelta(7 * j), 0) for j in range(1, L + 1)]) for w in Q.wk], dtype=float)
    Q["cntL"] = back("ro")
    Q["awayL"] = back("away") / 100.0
    Q["awayallL"] = (back("away") + back("awayh")) / 100.0
    Q["anyL"] = np.mean([(Q["w%d" % j].values > 0) for j in range(1, L + 1)], axis=0)
    Q["s0"] = Q.groupby("wk").ro.transform("mean")
    out = {}

    def undo(c, X):
        return _undo(Q, X, [c])[0] * G2
    for lab, c in (("the window's run-out days", "cntL"), ("the window's GP-form patients turned away", "awayL"),
                   ("the window's patients turned away", "awayallL"), ("the window's weeks with any run-out", "anyL")):
        out[lab] = undo(c, calX(Q, [c]))
    out["the window's share with the same week's share as a control"] = undo(col, calX(Q, [col, "s0"]))
    return out


def reduced(D, L):
    """Fits that drop the calendar terms the record's fit keeps (AIC against the golden's model)."""
    col = "s%d" % L
    full = sm.GLM(D.arr, calX(D, [col]), family=sm.families.Poisson()).fit().aic
    out = {}
    for lab, X in (("no trend", calX(D, [col], trend=False)), ("no month terms", calX(D, [col], month=False)),
                   ("weekday terms only", sm.add_constant(pd.get_dummies(D[["wd"]].astype(str), drop_first=True).astype(float).assign(**{col: D[col].values})))):
        v, a = _undo(D, X, [col])
        out[lab] = (v * G2, a - full)
    return out


def _did(D, ci, col):
    target = ci.attrs["target"]
    pr = pd.read_csv(os.path.join(target, F["practices"]), dtype=str)
    own = dict(zip(pr.practice_code, pr["phlebotomy_les_2025-26"] == "Y"))
    g = ci[ci.request_type == "GP"].copy()
    g["own"] = g.request_org.map(own)
    g = g.dropna(subset=["own"])
    cnt = g.groupby(["d", "own"]).size().unstack(fill_value=0)
    Q = D[D.d >= P.NEW_SYSTEM_LIVE].copy().set_index("d")
    Q["yP"] = cnt.get(True, pd.Series(dtype=float)).reindex(Q.index).fillna(0)
    Q["yN"] = cnt.get(False, pd.Series(dtype=float)).reindex(Q.index).fillna(0)
    Q = Q.reset_index()
    QQ = pd.concat([Q.assign(y=Q.yP, grp=1), Q.assign(y=Q.yN, grp=0)])
    Z = calX(QQ)
    Z["grp"] = QQ.grp.values
    Z["gx"] = QQ.grp.values * QQ[col].values
    Z["x"] = QQ[col].values
    m = sm.GLM(QQ.y, Z, family=sm.families.Poisson()).fit()
    fy = (Q.fy == 2025).values
    # practices with a clinic, scaled from the coded GP arrivals to all GP arrivals of the day
    share_p = (Q.yP / (Q.yP + Q.yN).replace(0, np.nan)).fillna(0).values
    arr = D[D.d >= P.NEW_SYSTEM_LIVE].arr.values
    supp = (arr[fy] * share_p[fy] * (np.exp(-m.params["gx"] * Q[col].values[fy]) - 1)).sum()
    D25 = D[D.fy == 2025]
    _did.coef = (float(m.params["gx"]), float(m.params["x"]))
    return float(D25.arr.sum() + supp)


def lag_route(D, n=10, month=True, hosp=False, poisson=False):
    """The round 2 Opus reader's route: GP-referred visits on the days the kiosk did not fill, on weekday, financial
    year and calendar month terms and n daily lags of the days it filled, predicted for every 2025-26 day with no
    run-outs."""
    Q = D.copy()
    f = Q.full.values
    lags = []
    for j in range(1, n + 1):
        Q["l%d" % j] = np.r_[np.zeros(j), f[:-j]]
        lags.append("l%d" % j)
    Z = pd.get_dummies(Q[["wd", "mo", "fy"] if month else ["wd", "fy"]].astype(str), drop_first=True).astype(float)
    for c in lags + (["seen_h"] if hosp else []):
        Z[c] = Q[c].values
    Z = sm.add_constant(Z, has_constant="add")
    op = f == 0
    fit = (sm.GLM(Q.seen_gp[op], Z[op], family=sm.families.Poisson()) if poisson else sm.OLS(Q.seen_gp[op], Z[op])).fit()
    Z0 = Z.copy()
    Z0[lags] = 0
    fy = (Q.fy == 2025).values
    return float(fit.predict(Z0)[fy].sum()) * G2


def ladder(D, target, ci):
    fy = (D.fy == 2025).values
    r = {}
    r["R0 GP-referred patients seen"] = float(D.seen_gp[fy].sum()) * G2
    r["R1 seen plus GP-referred turned away (the default path; the round 1 Sonnet reader)"] = float(D.arr[fy].sum()) * G2
    r["R2 the run-out days completed from the GP ticket-issue curve (the round 1 Opus reader)"] = completion(D, target, ci)
    clean = D.ro == 0
    m = sm.GLM(D.arr[clean], calX(D)[clean], family=sm.families.Poisson()).fit()
    r["R2 demand fitted on the days that did not run out"] = float(m.predict(calX(D))[fy].sum()) * G2
    L = window(D)[0]
    D2 = D.assign(all_arr=D.arr + D.seen_h + D.away_h)
    m = sm.GLM(D2.all_arr, calX(D2, ["s%d" % L]), family=sm.families.Poisson()).fit()
    r["R3 all walk-in arrivals modelled together with the window's run-outs"] = float((D.arr.values[fy] * np.exp(-m.params["s%d" % L] * D["s%d" % L].values[fy])).sum()) * G2
    r["R4 the previous calendar week's run-out share (the round 2 golden)"] = deterred(D, "s1")[0] * G2
    r["R4 the run-out share of the previous ten clinic days"] = deterred(D, "r10")[0] * G2
    r["R5 ten daily lags of the kiosk's full days on open days (the round 2 Opus reader)"] = lag_route(D)
    return r


def completion(D, target, ci):
    """The round 1 Opus reader's route: each day the kiosk filled completed from the share of a day's GP-referred
    arrivals that comes before its last ticket, read off the GP-form ticket-issue times of the days it did not fill."""
    leg = pd.read_csv(os.path.join(target, F["legacy"]), dtype=str)
    leg = leg[(leg.Outcome == "Seen") & (leg.Request == "GP form")].copy()
    leg["d"] = pd.to_datetime(leg.Date, format="%d/%m/%Y").dt.date
    leg = leg[leg.d < P.NEW_SYSTEM_LIVE]
    leg["m"] = [int(x[:2]) * 60 + int(x[3:5]) for x in leg.Issued]
    g = ci[ci.request_type == "GP"]
    lt = pd.to_datetime(g.event_utc, utc=True).dt.tz_convert("Europe/London")
    c2 = pd.DataFrame({"d": g.d.values, "m": (lt.dt.hour * 60 + lt.dt.minute).values})
    tk = pd.concat([leg[["d", "m"]], c2])
    full = set(D.d[D.full == 1])
    clean = tk[~tk.d.isin(full)]
    grid = np.arange(420, 901)
    cdf = np.searchsorted(np.sort(clean.m.values), grid, side="right") / len(clean)
    # the day's last ticket of either form
    leg_all = pd.read_csv(os.path.join(target, F["legacy"]), dtype=str)
    leg_all = leg_all[leg_all.Outcome == "Seen"].copy()
    leg_all["d"] = pd.to_datetime(leg_all.Date, format="%d/%m/%Y").dt.date
    leg_all = leg_all[leg_all.d < P.NEW_SYSTEM_LIVE]
    leg_all["m"] = [int(x[:2]) * 60 + int(x[3:5]) for x in leg_all.Issued]
    la = pd.to_datetime(ci.event_utc, utc=True).dt.tz_convert("Europe/London")
    last = pd.concat([leg_all[["d", "m"]], pd.DataFrame({"d": ci.d.values, "m": (la.dt.hour * 60 + la.dt.minute).values})]).groupby("d").m.max()
    est = []
    for row in D.itertuples():
        if row.full:
            f = cdf[min(max(int(last[row.d]) - 420, 0), len(grid) - 1)]
            est.append(row.seen_gp / max(f, 0.05))
        else:
            est.append(row.seen_gp)
    fy = (D.fy == 2025).values
    return float(np.array(est)[fy].sum()) * G2


def _register(target):
    reg = pd.read_csv(os.path.join(target, F["clinics"]), dtype=str)
    dn = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}
    days_of = {r.clinic_code: frozenset(dn[x.strip()] for x in r.clinic_days.split(",")) for r in reg.itertuples()}
    return dict(zip(reg.clinic_code, reg.specialty)), days_of


def _hosp(ci):
    h = ci[ci.request_type == "HOSP"].copy()
    h["rd"] = pd.to_datetime(h.request_date).dt.date
    return h


def _table(h, spec_of, names):
    y = h[(h.d >= FY0) & (h.d <= FY1)].copy()
    y["spec"] = y.request_org.map(spec_of)
    y["q"] = [quarter(d) for d in y.d]
    tab = y.groupby(["spec", "q"]).size().unstack(fill_value=0)
    return {sp: {q: int(tab.loc[sp, q]) if (sp in tab.index and q in tab.columns) else 0 for q in ("Q1", "Q2", "Q3", "Q4")}
            for sp in sorted(names)}


def ask_hosp(ci, target):
    """Hospital-clinic visits in 2025-26 by specialty and financial quarter of the visit. Forms issued before the new PAS
    carry the old clinic codes, which the register does not hold; each old code is the new code issued on the same
    clinic weekdays in the last fortnight of March 2026, before the clinics moved to their 2026-27 templates on 1 April."""
    new_spec, days_of = _register(target)
    h = _hosp(ci)
    old_codes = sorted(set(h.request_org) - set(new_spec))
    wk_old = {c: frozenset(x.weekday() for x in h[h.request_org == c].rd) for c in old_codes}
    march = h[(h.rd < TEMPLATES) & h.request_org.isin(list(new_spec))]
    wk_new = {c: frozenset(x.weekday() for x in march[march.request_org == c].rd) for c in new_spec}
    link = {}
    for c in old_codes:
        m = [n for n, w in wk_new.items() if w == wk_old[c]]
        link[c] = m[0] if len(m) == 1 else None
    spec_of = dict(new_spec)
    spec_of.update({c: new_spec[n] for c, n in link.items() if n})
    return _table(h, spec_of, new_spec.values()), {c: spec_of.get(c) for c in old_codes}


def ask_hosp_weekday_route(ci, target):
    """The careful route: each old code named by matching the weekdays its 2025-26 requests were issued on to the
    register's clinic days."""
    new_spec, days_of = _register(target)
    h = _hosp(ci)
    old_codes = sorted(set(h.request_org) - set(new_spec))
    spec_of = dict(new_spec)
    for c in old_codes:
        w = frozenset(x.weekday() for x in h[(h.request_org == c) & (h.rd < TEMPLATES)].rd)
        m = [n for n, dd in days_of.items() if dd == w]
        if len(m) == 1:
            spec_of[c] = new_spec[m[0]]
    return _table(h, spec_of, new_spec.values()), {c: spec_of.get(c) for c in old_codes}


def quarter(d):
    return "Q%d" % (((d.month - 4) % 12) // 3 + 1)


def roster(target):
    r = pd.read_csv(os.path.join(target, F["roster"]), dtype={"Employee no": str})
    r["d"] = pd.to_datetime(r["Roster date"]).dt.date
    return r


def clinic_days_list(target):
    """Clinic days from the queue records: every day either system recorded a visit."""
    seen, ci, ev = load_seen(target)
    return sorted(seen.index)


def report_vacancy(target):
    """The vacant post the annual report names (section 4), as a date range."""
    import re
    from pypdf import PdfReader
    txt = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, F["report"])).pages))
    m = re.search(r"post was vacant from (\d+ \w+) to (\d+ \w+ \d{4})", txt)
    end = dt.datetime.strptime(m.group(2), "%d %B %Y").date()
    start = dt.datetime.strptime("%s %d" % (m.group(1), end.year), "%d %B %Y").date()
    return start, end


def _sick_counts(target, days, mode):
    r = roster(target)
    sub = r[r.Assignment != "Bank Phlebotomist"]
    v0, v1 = report_vacancy(target)
    out = {}
    for q in ("Q1", "Q2", "Q3", "Q4"):
        qd = [d for d in days if FY0 <= d <= FY1 and quarter(d) == q]
        x = sub[sub.d.isin(qd)]
        sick = int((x.Absence == "Sickness").sum())
        yrows = int((x["Vacant line"] == "Y").sum())
        nrows = int((x["Vacant line"] == "N").sum())
        vacd = sum(1 for d in qd if v0 <= d <= v1)
        if mode == "golden":        # unassigned lines are filled posts whose holder is off sick, bar the vacant post
            s_days, r_days = sick + yrows - vacd, nrows + yrows - vacd
        elif mode == "flag":        # every unassigned line read as a vacant post
            s_days, r_days = sick, nrows
        elif mode == "definition":  # filled posts from the report's vacancy, sickness from the rows
            s_days, r_days = sick, len(qd) * P.POSTS - vacd
        else:                        # every unassigned line read as sickness, the vacant post included
            s_days, r_days = sick + yrows, nrows + yrows
        out[q] = {"hours": round(7.5 * s_days, 1), "rate": round(100.0 * s_days / r_days, 2), "rostered": round(7.5 * r_days, 1)}
    return out


def ask_sick(target, days):
    """Working days lost to sickness and the sickness absence rate by financial quarter of 2025-26: a holder's sickness
    rows, and the lines the e-roster shows unassigned from the sixth clinic day of a sickness until the same holder
    returns, which are filled posts; the one vacant post is the one the annual report names."""
    return _sick_counts(target, days, "golden")


def ask_sick_flag(target, days):
    return _sick_counts(target, days, "flag")


def ask_sick_definition(target, days):
    return _sick_counts(target, days, "definition")


def ask_sick_overclean(target, days):
    return _sick_counts(target, days, "overclean")


def weekly(D, b, col):
    y = D[D.fy == 2025].copy()
    y["kept"] = y.arr * (np.exp(-b * y[col]) - 1)
    w = y.groupby("wk").agg(seen=("seen_gp", "sum"), away=("away_gp", "sum"), kept=("kept", "sum")).reset_index()
    return w


def solve(target):
    D, ci, ev = daily(target)
    ci.attrs["target"] = target
    g = golden(D)
    return D, ci, ev, g
