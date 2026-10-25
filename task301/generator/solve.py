"""The golden route and its licensed family, from the shipped files only.

Golden: each sub-region's recorded smokers' chance of still smoking when called in 2027 (calls spread evenly through
the year), from a two-state continuous-time Markov process (smoker, ex-smoker) fitted by maximum likelihood to that
sub-region's own consecutive status recordings, times the 2025 team's quits per patient still smoking when called (its
reach times its quits per smoker reached). A quit is a four-week 'Not smoking'; lost to follow-up counts as smoking."""
import datetime as dt

import numpy as np
import pandas as pd
from scipy.optimize import minimize

SMOKER = {"Daily smoker", "Weekly smoker", "Irregular smoker", "Smoker"}
EX = {"Ex-smoker"}
NEVER = {"Never smoked", "Non-smoker"}
CANDS = ["Coastal Hinterland", "Inner South", "Northern Corridor", "Western Plains"]
YD = 365.25
Y0 = dt.date(2027, 1, 1)


def code(s):
    s = pd.Series(s)
    return np.where(s.isin(SMOKER), "S", np.where(s.isin(EX), "E", np.where(s.isin(NEVER), "N", "")))


def load(folder):
    import os
    ext = pd.read_csv(os.path.join(folder, "active_patients_2026-09-30.csv"), dtype=str, keep_default_na=False)
    hist = pd.read_parquet(os.path.join(folder, "smoking_status_history_2012-2026.parquet"))
    log = pd.read_csv(os.path.join(folder, "quit_outreach_calls_eastern_shore_2025.csv"), dtype=str,
                      keep_default_na=False)
    return ext, hist, log


def day_level(hist, ext):
    """One status per patient per day (the day's last entry), with the patient's sub-region."""
    h = hist.sort_values(["patient_key", "recorded_at"], kind="stable").copy()
    h["date"] = h.recorded_at.str[:10]
    h = h.groupby(["patient_key", "date"], sort=False).tail(1)
    h["c"] = code(h.smoking_status.values)
    h["t"] = (pd.to_datetime(h.date) - pd.Timestamp("2012-01-01")).dt.days.values / YD
    sub = ext.set_index("patient_key").sub_region
    h["sub_region"] = h.patient_key.map(sub).values
    return h


def pairs_of(h):
    h = h.reset_index(drop=True)
    nxt = h.groupby("patient_key").c.shift(-1)
    nt = h.groupby("patient_key").t.shift(-1)
    pr = pd.DataFrame({"sub_region": h.sub_region, "c0": h.c, "c1": nxt, "dt": nt - h.t})
    pr = pr[pr.c1.notna() & pr.c0.isin(["S", "E"]) & (pr.dt > 0)]
    return pr


def fit_ctmc(pr):
    """MLE of (quit, relapse) a year from consecutive pairs: P(smoker at the next record | the state now)."""
    s0 = (pr.c0 == "S").values
    s1 = (pr.c1 == "S").values
    d = pr.dt.values

    def nll(x):
        q, r = np.exp(x)
        pi = r / (q + r)
        e = np.exp(-(q + r) * d)
        p = np.where(s0, pi + (1 - pi) * e, pi * (1 - e))
        p = np.clip(p, 1e-12, 1 - 1e-12)
        return -(s1 * np.log(p) + (~s1) * np.log(1 - p)).sum()
    best = None
    for x0 in ([0.07, 0.02], [0.03, 0.005], [0.15, 0.05]):
        res = minimize(nll, np.log(x0), method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 6000})
        if best is None or res.fun < best.fun:
            best = res
    return tuple(np.exp(best.x)), best.fun


def p_still(age_y, q, r, grid=53):
    """Chance a patient recorded as a smoker age_y years before 1 January 2027 still smokes when called, the call
    falling evenly through 2027."""
    pi = r / (q + r)
    u = (np.arange(grid) + 0.5) / grid
    return np.mean([pi + (1 - pi) * np.exp(-(q + r) * (age_y + x)) for x in u], axis=0)


def conversion(log):
    n = len(log)
    reached = (log.outcome != "Not reached").sum()
    stopped = (log.outcome == "Not a current smoker").sum()
    quits = (log.four_week_status == "Not smoking").sum()
    return dict(listed=n, reached=int(reached), stopped=int(stopped), quit_dates=int((log.outcome == "Quit date set").sum()),
                quits=int(quits), reach=reached / n, per_smoker_reached=quits / (reached - stopped),
                k=(reached / n) * quits / (reached - stopped), per_listed=quits / n)


def lists(ext):
    L = ext[ext.smoking_status.isin(SMOKER) & ext.sub_region.isin(CANDS)].copy()
    L["age_y"] = (pd.Timestamp(Y0) - pd.to_datetime(L.smoking_status_date)).dt.days.values / YD
    return L


def golden(folder):
    ext, hist, log = load(folder)
    h = day_level(hist, ext)
    pr = pairs_of(h)
    cv = conversion(log)
    L = lists(ext)
    out = {}
    for g in CANDS:
        (q, r), _ = fit_ctmc(pr[pr.sub_region == g])
        Lg = L[L.sub_region == g]
        ps = p_still(Lg.age_y.values, q, r)
        out[g] = dict(listed=len(Lg), quit_rate=q, relapse=r, still=ps.sum(), quits=ps.sum() * cv["k"])
    return out, cv, h, pr, L, log, ext


# ---------------------------------------------------------------------------------------------------------------
# The asks, from the shipped files.

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def norm_name(s):
    s = " ".join(str(s).replace(",", " ").split()).casefold()
    for a, b in ((" pty ltd", ""), (" med centre", " medical centre"), (" gp", " general practice")):
        if s.endswith(a) or (a + " ") in s:
            s = s.replace(a, b)
    return s.strip()


def ask_referrals(folder):
    """Quitline referrals in 2025 from each candidate sub-region's practices (the PHN register's sub-regions)."""
    import os
    q = pd.read_csv(os.path.join(folder, "quitline_referrals_2023-2025.csv"), dtype=str, keep_default_na=False)
    pr = pd.read_csv(os.path.join(folder, "practices.csv"), dtype=str, keep_default_na=False)
    reg = {norm_name(n): s for n, s in zip(pr.practice_name, pr.sub_region)}
    q["sub_region"] = q.referring_practice.map(lambda n: reg.get(norm_name(n)))
    assert q.sub_region.notna().all(), q[q.sub_region.isna()].referring_practice.unique()
    q = q[q.month.str[:4] == "2025"].copy()
    q["referrals"] = q.referrals.astype(int)
    return q[q.sub_region.isin(CANDS)].groupby("sub_region").referrals.sum().reindex(CANDS).astype(int)


def dialler_legs(folder):
    """The dialler's legs with the time each started: the dialler writes a leg's record when its line is released, so
    a leg started its duration before the record's time."""
    import os
    d = pd.read_csv(os.path.join(folder, "dialler_legs_2025.csv"), dtype={"patient_key": str})
    d["end"] = pd.to_datetime(d.date_time)
    d["start"] = d.end - pd.to_timedelta(d.duration_s, unit="s")
    return d


def ask_evening(folder):
    """The calls the team made to patients from 5 pm and the patients it reached in them, by the weekday the call
    started; a Transferred leg is the dialler's leg to Quitline, not a call to a patient."""
    d = dialler_legs(folder)
    c = d[d.result != "Transferred"]
    ev = c[c.start.dt.hour >= 17]
    out = pd.DataFrame({"calls": ev.groupby(ev.start.dt.day_name()).size(),
                        "reached": ev[ev.result == "Answered"].groupby(ev.start.dt.day_name()).patient_key.nunique()})
    return out.reindex(WEEKDAYS).fillna(0).astype(int)


AGENT_IDS = ["QO-C1", "QO-C2", "QO-N1"]


def ask_talk(folder):
    """Each team member's minutes on answered calls per patient they reached, by the month the call started: a
    transferred patient's leg stays open with the Quitline leg until the patient hangs up, so the member's minutes stop
    where that leg starts."""
    d = dialler_legs(folder)
    out = {}
    for ag in AGENT_IDS:
        a = d[(d.result == "Answered") & (d.agent_id == ag)]
        t = d[(d.result == "Transferred") & (d.agent_id == ag)]
        secs = a.groupby(a.start.dt.month).duration_s.sum().sub(t.groupby(t.start.dt.month).duration_s.sum(),
                                                                 fill_value=0)
        v = secs / 60.0 / a.groupby(a.start.dt.month).patient_key.nunique()
        v.index = [dt.date(2025, i, 1).strftime("%B") for i in v.index]
        out[ag] = v
    return pd.DataFrame(out)
