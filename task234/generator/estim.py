"""Every owed figure from the shipped files: the week-3 escalations under the golden construction and under each easy
route, each stream's week-2 completeness (Ask A) and each laboratory's week-3 specimens (Ask B)."""
import datetime as dt
import os

import numpy as np
import pandas as pd

TZ = pd.Timedelta(hours=6)                                  # county time is UTC-6 in January
W1_2027 = dt.date(2027, 1, 3)                               # MMWR 2027 week 1 starts Sunday 3 January
CUTOFF_W2 = pd.Timestamp("2027-01-18 08:00")                # county time, the Monday after week 2
MIGRATION = pd.Timestamp("2027-01-19 06:00")                # county time, the state hub's broker migration
LINE = 0.80


def mmwr_start(y):
    j4 = dt.date(y, 1, 4)
    return j4 - dt.timedelta(days=(j4.weekday() + 1) % 7)


def holiday_week(label):
    """an MMWR week holding Thanksgiving Day, Christmas Day or New Year's Day"""
    y, w = label
    a = mmwr_start(y) + dt.timedelta(weeks=w - 1)
    days = [a + dt.timedelta(days=i) for i in range(7)]
    for d in days:
        if (d.month, d.day) in ((12, 25), (1, 1)):
            return True
        if d.month == 11 and d.weekday() == 3 and 22 <= d.day <= 28:
            return True
    return False


def load(target, files):
    p = lambda k: os.path.join(target, files[k])
    res = pd.read_csv(p("results"), dtype=str, keep_default_na=False)
    res = res.rename(columns={"released_utc": "released", "specimen_collected_utc": "specimen_collected"})   # the extract names its UTC columns
    agg = pd.read_csv(p("agg"))
    labs = pd.read_excel(p("reg"), sheet_name="Laboratories", dtype=str)
    streams = pd.read_excel(p("reg"), sheet_name="Streams", dtype=str)
    codes = pd.read_csv(p("codes"), dtype=str)
    return dict(res=res, agg=agg, labs=labs, streams=streams, codes=codes)


def mmwr_week_2027(d):
    return (d - W1_2027).days // 7 + 1


# ---------------------------------------------------------------------------------------------- conform
def conform(D, receipt_clock="switch"):
    """collapse the result messages to tests (FCP-2 s.2): one per laboratory, accession and virus; influenza A and B
    rows one influenza test; the corrected result in place of the one it corrects; cancelled orders out; the week by
    the county date of the first release. receipt_clock: 'switch' reads receipt times as county time before the state
    hub's broker migration and UTC from it; 'utc' reads every receipt time as UTC, like the extract's two _utc columns."""
    res, labs, codes = D["res"], D["labs"], D["codes"]
    fac = {}
    for r in labs.itertuples():
        for f in str(r.sending_facility_ids).split(","):
            fac[f.strip()] = r.lab_id
    vmap = dict(zip(codes.test_code, codes.virus))
    d = res[res.result_status != "X"].copy()
    d["lab_id"] = d.sending_facility.map(fac)
    d["virus"] = d.test_code.map(vmap)
    assert d.lab_id.notna().all() and d.virus.notna().all()
    d["rel_local"] = pd.to_datetime(d.released) - TZ
    rec = pd.to_datetime(d.received)
    if receipt_clock == "switch":
        d["rec_local"] = rec.where(rec < MIGRATION, rec - TZ)
    else:
        d["rec_local"] = rec - TZ
    d["coll_local"] = pd.to_datetime(d.specimen_collected) - TZ
    d = d.sort_values(["lab_id", "accession", "test_code", "rel_local", "result_status"], kind="mergesort")
    # the latest result per code stands (a correction replaces the result it corrects)
    last = d.groupby(["lab_id", "virus", "accession", "test_code"], sort=False).tail(1)
    pos = last.assign(p=(last.result == "DETECTED")).groupby(["lab_id", "virus", "accession"]).p.any()
    g = d.groupby(["lab_id", "virus", "accession"])
    t = pd.DataFrame({"first_release": g.rel_local.min(), "first_received": g.rec_local.min(),
                      "patient": g.patient_mrn.first(), "collected": g.coll_local.first()})
    t["positive"] = pos
    t["week"] = [mmwr_week_2027(x.date()) for x in t.first_release]
    return t.reset_index()


def week_counts(tests, week):
    w = tests[tests.week == week]
    g = w.groupby(["lab_id", "virus"])
    return pd.DataFrame({"tests": g.size(), "positives": g.positive.sum()})


# ---------------------------------------------------------------------------------------------- the reports
def reports_of_record(agg):
    a = agg.sort_values(["lab_id", "virus", "mmwr_year", "mmwr_week", "version"])
    return a.groupby(["lab_id", "virus", "mmwr_year", "mmwr_week"]).tail(1).reset_index(drop=True)


def series(rep):
    """per stream, the weekly tests and positives in week order (MMWR 2022-W40 to 2027-W02)"""
    wk = rep[["mmwr_year", "mmwr_week"]].drop_duplicates().sort_values(["mmwr_year", "mmwr_week"])
    labels = [(int(a), int(b)) for a, b in wk.values]
    idx = {k: i for i, k in enumerate(labels)}
    S = {}
    for (lab, v), g in rep.groupby(["lab_id", "virus"]):
        T = np.zeros(len(labels)); Pp = np.zeros(len(labels))
        for r in g.itertuples():
            T[idx[(r.mmwr_year, r.mmwr_week)]] = r.tests
            Pp[idx[(r.mmwr_year, r.mmwr_week)]] = r.positives
        S[(lab, v)] = (T, Pp)
    return labels, S


# ---------------------------------------------------------------------------------------------- estimates of week 3
def season_of(lbl):
    y, w = lbl
    return y if w >= 40 else y - 1


def est_persist(labels, S, recv):
    return {k: T[-1] for k, (T, Pp) in S.items()}


def est_mean3(labels, S, recv):
    return {k: T[-3:].mean() for k, (T, Pp) in S.items()}


def est_trend(labels, S, recv):
    return {k: T[-1] * T[-1] / T[-2] for k, (T, Pp) in S.items()}


def est_calendar(labels, S, recv, half=2, seasons=3):
    """the seasonal baseline: the same MMWR weeks (week 3 and two either side) of the three earlier winters, scaled by
    this season's level against theirs over the season's first seven weeks"""
    cur_season = 2026
    want = set(range(3 - half, 3 + half + 1))
    hist = [i for i, l in enumerate(labels) if season_of(l) in range(cur_season - seasons, cur_season)
            and l[0] == season_of(l) + 1 and l[1] in want]
    early_now = [i for i, l in enumerate(labels) if season_of(l) == cur_season and 40 <= l[1] <= 46]
    early_then = [i for i, l in enumerate(labels) if season_of(l) in range(cur_season - seasons, cur_season)
                  and 40 <= l[1] <= 46]
    return {k: T[hist].mean() * T[early_now].mean() / T[early_then].mean() for k, (T, Pp) in S.items()}


def est_peers(labels, S, recv, how="pooled"):
    """last week's tests moved by the other laboratories' change this week on the same virus"""
    out = {}
    for k, (T, Pp) in S.items():
        lab, v = k
        others = [k2 for k2 in S if k2[1] == v and k2[0] != lab]
        if how == "pooled":
            f = sum(recv[k2][0] for k2 in others) / sum(S[k2][0][-1] for k2 in others)
        else:
            f = float(np.median([recv[k2][0] / S[k2][0][-1] for k2 in others]))
        out[k] = T[-1] * f
    return out


def est_poscount(labels, S, recv):
    """the week's positives over last week's positivity"""
    return {k: recv[k][1] / (Pp[-1] / T[-1]) for k, (T, Pp) in S.items()}


def est_positivity(labels, S, recv, form="logtr", window=None, holidays=True):
    """the week's tests from the stream's own positivity this week, through the testing response fitted on the
    stream's reports: log(tests) on positivity (and time), or a variant"""
    n = len(labels)
    t_all = np.arange(n + 1) / 52.18
    keep = np.array([holidays or not holiday_week(l) for l in labels])
    if window:
        keep &= np.arange(n) >= n - window
    out = {}
    for k, (T, Pp) in S.items():
        x3 = recv[k][1] / recv[k][0]
        pi = Pp[keep] / T[keep]
        y = T[keep]
        tt = t_all[:n][keep]
        one = np.ones(len(pi))
        if form == "log":
            b = np.linalg.lstsq(np.c_[one, pi], np.log(y), rcond=None)[0]
            out[k] = float(np.exp(b[0] + b[1] * x3))
        elif form == "logtr":
            b = np.linalg.lstsq(np.c_[one, pi, tt], np.log(y), rcond=None)[0]
            out[k] = float(np.exp(b[0] + b[1] * x3 + b[2] * t_all[n]))
        elif form == "lin":
            b = np.linalg.lstsq(np.c_[one, pi], y, rcond=None)[0]
            out[k] = float(b[0] + b[1] * x3)
        elif form == "lintr":
            b = np.linalg.lstsq(np.c_[one, pi, tt], y, rcond=None)[0]
            out[k] = float(b[0] + b[1] * x3 + b[2] * t_all[n])
        elif form == "quad":
            b = np.linalg.lstsq(np.c_[one, pi, pi ** 2], np.log(y), rcond=None)[0]
            out[k] = float(np.exp(b[0] + b[1] * x3 + b[2] * x3 ** 2))
        elif form == "ratio":
            b = np.linalg.lstsq(np.c_[one, pi, tt], np.log(y), rcond=None)[0]
            p2 = Pp[-1] / T[-1]
            out[k] = float(T[-1] * np.exp(b[1] * (x3 - p2) + b[2] / 52.18))
        elif form == "poisson":
            X = np.c_[one, pi, tt]
            b = np.linalg.lstsq(X, np.log(y), rcond=None)[0]
            for _ in range(25):
                mu = np.exp(X @ b)
                b = b + np.linalg.solve(X.T @ (X * mu[:, None]), X.T @ (y - mu))
            out[k] = float(np.exp(b[0] + b[1] * x3 + b[2] * t_all[n]))
        elif form == "lag":
            # last week's tests and this week's positivity together
            lagT = np.r_[np.nan, T[:-1]][keep]
            ok = ~np.isnan(lagT)
            X = np.c_[np.ones(ok.sum()), pi[ok], np.log(lagT[ok])]
            b = np.linalg.lstsq(X, np.log(y[ok]), rcond=None)[0]
            out[k] = float(np.exp(b[0] + b[1] * x3 + b[2] * np.log(T[-1])))
        else:
            raise ValueError(form)
    return out


POSITIVITY_VARIANTS = [(f, w, h) for f in ("log", "logtr", "lin", "lintr", "quad", "ratio", "poisson", "lag")
                       for w in (None, 60, 17) for h in (True, False)
                       if not (f in ("quad", "lag", "poisson") and w == 17)]
GOLDEN_MODEL = ("poisson", None, False)


def completeness(recv, est):
    return {k: recv[k][0] / est[k] for k in est}


def escalated(comp):
    return {k for k, c in comp.items() if c < LINE}


# ---------------------------------------------------------------------------------------------- the asks
def ask_a_counts(tests, rep, week=2):
    """each stream's week-2 tests whose result reached the platform by 08:00 county time on Monday 18 January, and
    the tests the week's report of record counts (FCP-2 s.3, s.5)"""
    w = tests[tests.week == week]
    n = w[w.first_received <= CUTOFF_W2].groupby(["lab_id", "virus"]).size()
    r = rep[(rep.mmwr_year == 2027) & (rep.mmwr_week == week)].set_index(["lab_id", "virus"]).tests
    return {k: (int(n.get(k, 0)), int(r[k])) for k in r.index}


def ask_a(tests, rep, week=2):
    """each stream's week-2 completeness"""
    return {k: a / b for k, (a, b) in ask_a_counts(tests, rep, week).items()}


def ask_b(tests, week=3, key="specimen"):
    """each laboratory's specimens tested in week 3 with results on the platform: one collection from one patient
    (FCP-2 s.6), the patient's number and the collection time"""
    w = tests[tests.week == week]
    if key == "specimen":
        return w.groupby("lab_id").apply(lambda g: len(set(zip(g.patient, g.collected)))).to_dict()
    if key == "accession":
        return w.groupby("lab_id").accession.nunique().to_dict()
    if key == "patient":
        return w.groupby("lab_id").patient.nunique().to_dict()
    raise ValueError(key)


# ---------------------------------------------------------------------------------------------- everything
def solve(target, files):
    D = load(target, files)
    tests = conform(D)
    rep = reports_of_record(D["agg"])
    labels, S = series(rep)
    wc = week_counts(tests, 3)
    recv = {k: (float(wc.loc[k, "tests"]), float(wc.loc[k, "positives"])) for k in S}
    routes = {"persist": est_persist, "mean3": est_mean3, "trend": est_trend, "calendar": est_calendar,
              "peers": est_peers, "peers_median": lambda l, s, r: est_peers(l, s, r, "median"),
              "poscount": est_poscount}
    R = {}
    for name, fn in routes.items():
        est = fn(labels, S, recv)
        c = completeness(recv, est)
        R[name] = dict(est=est, comp=c, esc=escalated(c))
    V = {}
    for var in POSITIVITY_VARIANTS:
        est = est_positivity(labels, S, recv, *var)
        c = completeness(recv, est)
        V[var] = dict(est=est, comp=c, esc=escalated(c))
    gold = V[GOLDEN_MODEL]
    A = ask_a(tests, rep)
    B = ask_b(tests)
    return dict(D=D, tests=tests, rep=rep, labels=labels, S=S, recv=recv, routes=R, variants=V, gold=gold, A=A, B=B,
                A_counts=ask_a_counts(tests, rep))


# ---------------------------------------------------------------------------------------------- the bench
def backtest(labels, S, first=(2023, 10)):
    """one week ahead over the closed weeks of the reports (holiday weeks and the two weeks after one left out): each
    week's tests predicted from last week's count, from last week's growth, and from the week's own positivity through
    the response fitted on the weeks before it. Returns the absolute errors per method, and whether the stream's
    positivity moved by 3 points or more that week."""
    n = len(labels)
    t = np.arange(n) / 52.18
    out = {"persist": [], "trend": [], "positivity": [], "moved": []}
    for i, l in enumerate(labels):
        if l < first or any(holiday_week(labels[i - j]) for j in (0, 1, 2)):
            continue
        keep = np.array([j < i and not holiday_week(labels[j]) for j in range(n)])
        for k, (T, Pp) in S.items():
            pi = Pp[keep] / T[keep]
            b = np.linalg.lstsq(np.c_[np.ones(keep.sum()), pi, t[keep]], np.log(T[keep]), rcond=None)[0]
            pos = np.exp(b[0] + b[1] * Pp[i] / T[i] + b[2] * t[i])
            out["persist"].append(abs(T[i - 1] / T[i] - 1))
            out["trend"].append(abs(T[i - 1] ** 2 / T[i - 2] / T[i] - 1))
            out["positivity"].append(abs(pos / T[i] - 1))
            out["moved"].append(abs(Pp[i] / T[i] - Pp[i - 1] / T[i - 1]) >= 0.03)
    return {k: np.array(v) for k, v in out.items()}


# ---------------------------------------------------------------------------------------------- the week-2 check (FCP-2 s.5)
def est_received(labels, S, recv):
    """the week's results on the platform taken as its tests"""
    return {k: recv[k][0] for k in S}


def week2_check(X, clock="switch", extra=True):
    """each way of estimating week 2's tests, made from the reports of the weeks before and the week-2 results as the
    platform held them at 08:00 on Monday 18 January, against the week-2 reports of record: each way's largest and
    average miss across the streams, as a share of the reported tests"""
    D, S, labels = X["D"], X["S"], X["labels"]
    t = conform(D, clock)
    held = t[(t.week == 2) & (t.first_received <= CUTOFF_W2)]
    wc = held.groupby(["lab_id", "virus"]).agg(tests=("positive", "size"), positives=("positive", "sum"))
    recv = {k: (float(wc.loc[k, "tests"]), float(wc.loc[k, "positives"])) for k in S}
    S1 = {k: (T[:-1], Pp[:-1]) for k, (T, Pp) in S.items()}
    lab1 = labels[:-1]
    T2 = {k: S[k][0][-1] for k in S}
    ways = {"persist": est_persist, "trend": est_trend, "mean3": est_mean3, "calendar": est_calendar,
            "peers": est_peers, "peers_median": lambda l, s, r: est_peers(l, s, r, "median"),
            "poscount": est_poscount, "received": est_received}
    out = {}
    for name, fn in ways.items():
        est = fn(lab1, S1, recv)
        m = [abs(est[k] / T2[k] - 1) for k in S]
        out[name] = (max(m), sum(m) / len(m))
    variants = list(POSITIVITY_VARIANTS)
    if extra:
        variants += [(f, w, h) for f in ("log", "logtr", "lin", "lintr", "quad", "poisson", "ratio", "lag")
                     for w in (26, 39, 52, 120) for h in (True, False)]
    for var in variants:
        est = est_positivity(lab1, S1, recv, *var)
        m = [abs(est[k] / T2[k] - 1) for k in S]
        out[("pos",) + var] = (max(m), sum(m) / len(m))
    return out
