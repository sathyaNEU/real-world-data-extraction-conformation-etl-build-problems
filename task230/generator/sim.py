"""The closed quarter as it happened: volumes, the workforce, every key field's OCR value, first-pass
detection, timeouts, the blind re-key audit, second-pass sessions and the client audits.

The detection truth: the miss logit on an OCR error is a constant plus the field family, the field type,
the verifier's skill, tenure, a small time-on-shift and time-of-night term, minus 0.6 times the log of the
OCR error rate of every key field the shift-day's queue carried. Nothing here is shipped directly; pack.py
writes the exports from it."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

DAY = dt.timedelta(days=1)


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += DAY
    return out


def logit(x):
    return math.log(x / (1 - x))


ALPHA = logit(W.TRUTH["base_miss"]) + W.TRUTH["g"] * math.log(W.TRUTH["base_pool"])


# ----------------------------------------------------------------------------------------------- volumes
def cycle_day(d):
    """the last two and the first working days of a month, when hospitals' cycle billing reaches Kessington"""
    nxt = d + DAY
    while nxt.weekday() >= 5:
        nxt += DAY
    nxt2 = nxt + DAY
    while nxt2.weekday() >= 5:
        nxt2 += DAY
    prv = d - DAY
    while prv.weekday() >= 5:
        prv -= DAY
    return nxt.month != d.month or nxt2.month != d.month or prv.month != d.month


def q3_key_fields(rng, scale=None):
    """daily key fields by stream for every Q3 shift-day (and the pilot), before conversion to documents"""
    scale = scale or {}
    rows = []
    for d in days(*W.Q3):
        wd = d.weekday()
        if wd == 6:
            continue
        for code, s in W.STREAMS.items():
            c = s["client"]
            region = W.CLIENTS[c]["region"]
            if code == "D6":
                if W.PILOT[0] <= d <= W.PILOT[1]:
                    kf = W.PILOT_KF * (0.85 if wd == 5 else 1.0) * math.exp(rng.normal(0, 0.15))
                else:
                    continue
            elif wd == 5:
                if code not in W.SAT_KF:
                    continue
                kf = W.SAT_KF[code] * math.exp(rng.normal(0, 0.16))
            else:
                if region == "US" and d in W.US_HOLIDAYS_Q3:
                    if code not in W.SAT_KF:
                        continue
                    kf = W.SAT_KF[code] * 1.1 * math.exp(rng.normal(0, 0.12))
                elif region == "UK" and d in W.UK_HOLIDAYS_Q3:
                    continue
                else:
                    prof = W.PROFILE.get(code, W.PROFILE["TCM" if code == "D5" else region])[wd]
                    sd = W.DAILY_SD.get(code, 0.22)
                    kf = s["kf"] * scale.get(code, 1.0) * prof * math.exp(rng.normal(0, sd) - sd * sd / 2)
                    if code in W.CYCLE and cycle_day(d):
                        kf *= W.CYCLE[code]
            rows.append((d, code, W.STREAMS[code]["q3"] or "D", kf))
    df = pd.DataFrame(rows, columns=["day", "code", "queue", "kf_raw"])
    df["version"] = [W.version_on(c, d) for c, d in zip(df.code, df.day)]
    df["kfpd"] = [len(W.fields(c, v)) for c, v in zip(df.code, df.version)]
    df["docs"] = np.maximum(1, np.round(df.kf_raw / df.kfpd)).astype(int)
    df["kf"] = df.docs * df.kfpd
    return df.drop(columns="kf_raw")


# ----------------------------------------------------------------------------------------------- workforce
def workforce(rng):
    """persons, badges (with reissues), hire dates, skills, and the monthly group rotation"""
    persons = []
    base_hires = sorted(rng.choice(np.arange(0, 2400), size=30, replace=False))
    for i in range(30):
        hire = dt.date(2026, 6, 15) - dt.timedelta(days=int(base_hires[i]) + 40)
        persons.append(dict(emp=f"E{41207 + i * 37}", badge=f"V{3101 + i * 7:04d}", hire=hire, leave=None,
                            group="ABC"[i % 3], skill=float(rng.normal(0, W.TRUTH["skill_sd"]))))
    # three leavers in July; their badges are reissued to three August joiners in the same group
    leavers = [4, 13, 23]
    leave_days = [dt.date(2026, 7, 10), dt.date(2026, 7, 24), dt.date(2026, 7, 31)]
    join_days = [dt.date(2026, 8, 3), dt.date(2026, 8, 10), dt.date(2026, 8, 17)]
    for k, (i, ld, jd) in enumerate(zip(leavers, leave_days, join_days)):
        persons[i]["leave"] = ld
        persons.append(dict(emp=f"E{43350 + k * 11}", badge=persons[i]["badge"], hire=jd, leave=None,
                            group="B" if persons[i]["group"] == "C" else persons[i]["group"],
                            skill=float(rng.normal(0, W.TRUTH["skill_sd"]))))
    # two late-August joiners on new badges, four October joiners for November
    for k, (jd, g) in enumerate([(dt.date(2026, 8, 24), "B"), (dt.date(2026, 8, 24), "A")]):
        persons.append(dict(emp=f"E{43402 + k * 13}", badge=f"V{3340 + k * 9:04d}", hire=jd, leave=None, group=g,
                            skill=float(rng.normal(0, W.TRUTH["skill_sd"]))))
    for k in range(4):
        persons.append(dict(emp=f"E{43511 + k * 17}", badge=f"V{3372 + k * 6:04d}", hire=dt.date(2026, 10, 12), leave=None,
                            group="O", skill=float(rng.normal(0, W.TRUTH["skill_sd"]))))
    P = pd.DataFrame(persons)
    P["pid"] = np.arange(len(P))
    return P


ROTATION = {7: {"A": "D", "B": "D", "C": "N"}, 8: {"A": "D", "B": "N", "C": "D"}, 9: {"A": "N", "B": "D", "C": "D"}}


def on_shift(P, d):
    """(pid, queue) for every verifier working shift-day d: the group's queue for the month, one rest day a week"""
    out = []
    for r in P.itertuples():
        if r.group not in ROTATION.get(d.month, {}):
            continue
        if d < r.hire or (r.leave and d > r.leave):
            continue
        if d.weekday() == (r.pid % 6):
            continue
        out.append((r.pid, ROTATION[d.month][r.group]))
    return out


def tenure_term(days_in):
    if days_in < 90:
        return W.TRUTH["ten_new"]
    if days_in < 180:
        return W.TRUTH["ten_mid"]
    return 0.0


# ----------------------------------------------------------------------------------------------- the quarter
def shift_start(d, q):
    h, m = W.SHIFT[q][:2]
    return dt.datetime(d.year, d.month, d.day, h, m)


def simulate(seed=W.SEED, scale=None):
    scale = W.Q3_SCALE if scale is None else scale
    rng = np.random.default_rng(seed)
    vol = q3_key_fields(rng, scale)
    P = workforce(rng)
    T = W.TRUTH
    skill = P.skill.values
    hire = P.hire.values

    # documents ---------------------------------------------------------------------------------
    doc_rows = []
    for r in vol.itertuples():
        doc_rows.append(pd.DataFrame({"code": r.code, "day": r.day, "queue": r.queue, "version": r.version,
                                      "kf": r.kfpd, "n": np.arange(r.docs)}))
    docs = pd.concat(doc_rows, ignore_index=True)
    docs["doc"] = np.arange(len(docs))
    # capture numbers: two-digit year, day of year, queue letter and the queue-day's capture sequence
    seqn = np.empty(len(docs), dtype=np.int64)
    for (d, q), g in docs.groupby(["day", "queue"], sort=True):
        seqn[g.doc.values] = 1 + rng.permutation(len(g))
    doy = pd.to_datetime(docs.day).dt.dayofyear.values
    docs["doc_id"] = [f"26{a:03d}{q}{n:06d}" for a, q, n in zip(doy, docs.queue.values, seqn)]
    # dispatch: every queue-day's documents shuffled across the verifiers on shift, times spread over the shift
    pid = np.empty(len(docs), dtype=np.int32)
    tmin = np.empty(len(docs))
    for (d, q), g in docs.groupby(["day", "queue"], sort=True):
        crew = [p for p, qq in on_shift(P, d) if qq == q]
        idx = g.doc.values
        pid[idx] = rng.choice(crew, size=len(idx))
        tmin[idx] = rng.uniform(4, 535, size=len(idx))
    docs["pid"] = pid
    docs["tmin"] = tmin
    docs["audited"] = False
    for (code, d), g in docs.groupby(["code", "day"], sort=True):
        share = W.audit_share(code)
        k = int(round(share * len(g)))
        docs.loc[rng.choice(g.doc.values, size=k, replace=False), "audited"] = True

    # fields ------------------------------------------------------------------------------------
    parts = []
    for (code, version), g in docs.groupby(["code", "version"], sort=True):
        flist = W.fields(code, version)
        mult = np.array([W.FIELD_TYPES[t][0] for _, t in flist])
        pr = W.STREAMS[code]["p"] * mult / mult.mean()
        n, k = len(g), len(flist)
        err = rng.random((n, k)) < pr
        parts.append(pd.DataFrame({"doc": np.repeat(g.doc.values, k), "fpos": np.tile(np.arange(k, dtype=np.int8), n),
                                   "err": err.ravel()}))
    F = pd.concat(parts, ignore_index=True)
    F = F.merge(docs[["doc", "code", "version", "day", "queue", "pid", "tmin", "audited"]], on="doc", how="left")
    pool = F.groupby(["day", "queue"]).err.mean().rename("pool")
    F = F.join(pool, on=["day", "queue"])
    F["ftype"] = _ftype_vec(F)
    fam = F.code.map({c: T["fam"][W.STREAMS[c]["family"]] for c in W.STREAMS}).values
    ftm = F.ftype.map({t: v[1] for t, v in W.FIELD_TYPES.items()}).values
    tenure_days = (pd.to_datetime(F.day).values - pd.to_datetime(hire[F.pid.values]).values).astype("timedelta64[D]").astype(int)
    ten = np.where(tenure_days < 90, T["ten_new"], np.where(tenure_days < 180, T["ten_mid"], 0.0))
    hours = F.tmin.values / 60.0
    tos = T["tos"] * np.maximum(0.0, hours - 5.0)
    ton = np.where((F.queue.values == "N") & (hours >= 5.5), T["ton"], 0.0)
    z = ALPHA + fam + ftm + skill[F.pid.values] + ten + tos + ton - T["g"] * np.log(F.pool.values)
    pm = 1 / (1 + np.exp(-z))
    u = rng.random(len(F))
    F["miss"] = F.err.values & (u < pm)
    F["fa"] = (~F.err.values) & (rng.random(len(F)) < T["fa"])
    F["pmiss"] = np.where(F.err.values, pm, np.nan)
    F["tenure_days"] = tenure_days

    # timeouts: an earlier screen that timed out, by a verifier on the same shift ---------------------
    to = rng.random(len(docs)) < 0.035
    docs["timeout"] = to
    docs["to_pid"] = -1
    docs["to_tmin"] = np.nan
    for (d, q), g in docs[to].groupby(["day", "queue"], sort=True):
        crew = [p for p, qq in on_shift(P, d) if qq == q]
        docs.loc[g.index, "to_pid"] = rng.choice(crew, size=len(g))
        docs.loc[g.index, "to_tmin"] = np.maximum(0.5, g.tmin.values - rng.uniform(18, 95, size=len(g)))
    return dict(vol=vol, P=P, docs=docs, F=F, pool=pool.reset_index(), rng=rng)


def _ftype_vec(F):
    out = np.empty(len(F), dtype=object)
    for (code, version), idx in F.groupby(["code", "version"], sort=True).indices.items():
        types = np.array([t for _, t in W.fields(code, version)], dtype=object)
        out[idx] = types[F.fpos.values[idx]]
    return out


def fname_vec(F):
    out = np.empty(len(F), dtype=object)
    for (code, version), idx in F.groupby(["code", "version"], sort=True).indices.items():
        names = np.array([n for n, _ in W.fields(code, version)], dtype=object)
        out[idx] = names[F.fpos.values[idx]]
    return out
