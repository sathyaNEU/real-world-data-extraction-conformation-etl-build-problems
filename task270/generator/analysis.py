"""The golden on the cut pack: the second sitting's gain read within patients, each patient's own decline net of it,
each clinic's average and the two that recruit; the slope through every sitting beside it; and the sponsor's two
feasibility figures for every clinic."""
import datetime as dt
import numpy as np
import pandas as pd
import common as K
import pack as PK

YEAR = 365.25


def slopes(w, y):
    g = w.groupby("pid")
    tm = g.t.transform("mean")
    ym = g[y].transform("mean")
    return ((w.t - tm) * (w[y] - ym)).groupby(w.pid).sum() / ((w.t - tm) ** 2).groupby(w.pid).sum()


def endpoint(w, y):
    g = w.sort_values("t").groupby("pid")
    return (g[y].last() - g[y].first()) / (g.t.last() - g.t.first())


def gain(w, cols=("step",)):
    """Each patient's totals on time with their own intercept and slope, a step shared by all: the step's estimate.
    Patients with two sittings fit their own line exactly and carry nothing on the step."""
    v = w[w.groupby("pid").t.transform("size") >= 3]
    gg = v.groupby("pid")
    xt = v.t - gg.t.transform("mean")
    stt = (xt * xt).groupby(v.pid).transform("sum")

    def resid(col):
        ym = gg[col].transform("mean")
        return v[col] - ym - ((xt * (v[col] - ym)).groupby(v.pid).transform("sum") / stt) * xt
    X = np.column_stack([resid(c) for c in cols])
    return np.linalg.lstsq(X, resid("s").values, rcond=None)[0]


def clinic_of(w):
    return w.sort_values(["pid", "t"]).groupby("pid").clinic.last()


def clinic_means(w, b):
    return -(b.groupby(clinic_of(w)).mean())


def half(x):
    return float(np.floor(x * 2 + 0.5) / 2)


def call(w, P_gain=None):
    if P_gain is None:
        P_gain = gain(w)[0]
    v = w.copy()
    v["a"] = v.s - P_gain * v.step
    dec = clinic_means(v, slopes(v, "a"))
    order = list(dec.sort_values(ascending=False).index)
    return dict(gain=P_gain, decline=dec, order=order, sites=order[:2], below=order[2],
                naive=clinic_means(v, slopes(v, "s")))


def main(P):
    w = PK.frame(P)
    res = call(w)
    res["frame"] = w
    res["n"] = clinic_of(w).value_counts()
    res["gain_history"] = gain(PK.history(P))[0]
    nav = res["naive"].sort_values(ascending=False)
    res["naive_order"] = list(nav.index)
    # the paper's 3.1 applied the easy way: the test's change estimated on the period's sittings alone
    v = w.copy()
    v["wk"] = v.sort_values("t").groupby("pid").cumcount().reindex(v.index)
    v["step"] = (v.wk >= 1).astype(float)
    res["period_only_gain"] = gain(v)[0]
    v["a"] = v.s - res["period_only_gain"] * v.step
    res["period_only"] = clinic_means(v, slopes(v, "a"))
    return res


# ------------------------------------------------------------------ Ask A: under follow-up on 30 September 2026
def ask_a(P, day=K.WINDOW[1]):
    ep = P["episodes"].copy()
    ep["nhs"] = PK.digits(ep.nhs_number)
    ep["start"] = pd.to_datetime(ep.episode_start).dt.date
    ep["end"] = pd.to_datetime(ep.episode_end.replace("", None)).dt.date
    ep["clinic"] = ep.site_code.map(P["site2clinic"])
    open_ = ep[(ep.start <= day) & (ep.end.isna() | (ep.end > day))]
    # a discharge at a review the episode has not yet been closed for
    ap = P["appts"]
    ap = ap[ap.outcome.str.contains("discharged from service|care passed to")].copy()
    ap["nhs"] = PK.digits(ap.nhs_number)
    ap["date"] = pd.to_datetime(ap.appointment_start.str[:10]).dt.date
    open_ = open_.merge(ap[["nhs", "date"]], on="nhs", how="left")
    gone = open_[(open_.date >= open_.start) & (open_.date <= day)].nhs.unique()
    keep = open_[~open_.nhs.isin(gone)].drop_duplicates("episode_id")
    pmi = P["pmi"][P["pmi"].record_status == "Active"].set_index("nhs")
    dod = pd.to_datetime(pmi.date_of_death.replace("", None)).dt.date
    keep = keep[~keep.nhs.map(dod).apply(lambda d: d is not None and not pd.isna(d) and d <= day)]
    lat = PK.latest_dx(P, day)
    keep = keep[keep.nhs.map(lat).fillna("").map(PK.in_scope)]
    dob = pd.to_datetime(pmi.date_of_birth).dt.date
    age = keep.nhs.map(dob).apply(lambda b: K.TRIAL_ENTRY.year - b.year - ((K.TRIAL_ENTRY.month, K.TRIAL_ENTRY.day)
                                                                           < (b.month, b.day)))
    keep = keep.assign(age=age.values)
    out = {}
    for c in K.NAMES:
        k = keep[keep.clinic == c]
        out[c] = dict(under=int(k.nhs.nunique()), age_ok=int(k[k.age <= K.AGE_LIMIT].nhs.nunique()))
    return out, keep


# ------------------------------------------------------------------ Ask B: referral to diagnosis
def ask_b(P):
    tr = P["tracker"].copy()
    tr["nhs"] = PK.digits(tr["NHS number"])
    tr["ref"] = pd.to_datetime(tr["Referral date"]).dt.date
    ap = P["appts"]
    # the appointment that gave the referral's first diagnosis: one whose outcome records it, or, for a finding of
    # no dementia or of depression, the one that discharged the patient with it
    given = ap[ap.outcome.str.contains("diagnosis given") | ap.outcome.eq("Attended - discharged from service")].copy()
    given["nhs"] = PK.digits(given.nhs_number)
    given["date"] = pd.to_datetime(given.appointment_start.str[:10]).dt.date
    found = tr[["nhs", "ref"]].merge(given[["nhs", "date"]], on="nhs")
    found = found[found.date >= found.ref]
    first_given = found.sort_values("date").groupby(["nhs", "ref"]).date.first()
    tr["given"] = [first_given.get((n, r)) for n, r in zip(tr.nhs, tr.ref)]
    a0, a1 = K.ASK_YEAR
    t = tr[tr.given.notna()].copy()
    t = t[(t.given >= a0) & (t.given <= a1) & (t.given >= t.ref)]
    t["days"] = [(g - r).days for g, r in zip(t.given, t.ref)]
    out = {}
    for c in K.NAMES:
        k = t[t.Clinic == c]
        out[c] = dict(n=int(len(k)), share=100.0 * float((k.days <= K.SIX_WEEKS).mean()), mean=float(k.days.mean()))
    return out, t
