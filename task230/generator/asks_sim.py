"""The records the asks read: September's second-pass sessions, the client audits of delivered claims and
the delivery manifests. None of these files is read by the main call."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

DAY = dt.timedelta(days=1)
SP_BADGES = [f"Q{2204 + i * 5}" for i in range(14)]

# delivery transmissions in IST: (hour, minute, days after the shift-day)
BATCH_TIMES = {
    "US": [(23, 40, 0), (2, 35, 1), (5, 50, 1)],
    "AU": [(12, 10, 0), (16, 45, 0), (20, 20, 0)],
    "UK": [(13, 5, 0), (17, 25, 0), (4, 50, 1)],
}
CLIENT_SAMPLE = {"KBA": 0.012, "NDS": 0.020, "BMC": 0.030, "HPB": 0.015, "WBH": 0.008, "CIP": 0.020, "WPC": 0.015, "TCM": 0.010}
CAPTURE_CODES = {
    "KBA": ["D01", "D02", "D04"], "NDS": ["KE", "KT"], "BMC": ["DE-1", "DE-2"], "HPB": ["E10", "E11"],
    "WBH": ["CAPT", "KEY"], "CIP": ["C1"], "WPC": ["DATA", "TRANS"], "TCM": ["01", "02"],
}
BUSINESS_CODES = {
    "KBA": ["E20", "E31", "DUP"], "NDS": ["EL", "CV", "DP"], "BMC": ["EL-1", "CV-2", "DUP"], "HPB": ["E40", "E52", "E60"],
    "WBH": ["ELIG", "COVR", "DUPL"], "CIP": ["E2", "C3", "D4"], "WPC": ["ELIG", "EXCL", "DUP"], "TCM": ["11", "12", "19"],
}


def second_pass_sessions(S, rng):
    """one line per document worked in a second-pass session in September 2026 (and the pilot's typed claims);
    a session crossing the half-shift handover is logged as two parts under one session id"""
    docs = S["docs"]
    sel = docs[(pd.to_datetime(docs.day).dt.month == 9) & (docs.code.isin(W.Q3_SECOND_PASS + ["D6"]))]
    lines = []
    sid = 880214
    for (d, code), g in sel.groupby(["day", "code"], sort=True):
        fam = W.STREAMS[code]["family"]
        q = W.STREAMS[code]["q3"] or "D"
        ids = g.doc_id.values
        i = 0
        while i < len(ids):
            n = int(min(len(ids) - i, 1 + rng.poisson(10)))
            chunk = ids[i:i + n]
            i += n
            mins = np.exp(rng.normal(math.log(W.SP_MIN[fam]) - 0.06, 0.35, size=n))
            start = rng.uniform(0, 520)
            cum = start + np.concatenate([[0], np.cumsum(mins)[:-1]])
            part = np.where(cum < 270, 1, 2)
            if start >= 270:
                part[:] = 2
            badge = SP_BADGES[int(rng.integers(len(SP_BADGES)))]
            sid += int(rng.integers(1, 4))
            for p in (1, 2):
                m = part == p
                if not m.any():
                    continue
                tot = round(float(mins[m].sum()), 1)
                for j in np.where(m)[0]:
                    lines.append((f"SP{sid}", d, q, p, badge, code, chunk[j], round(float(cum[j]), 2), tot))
    L = pd.DataFrame(lines, columns=["session", "day", "queue", "part", "badge", "code", "doc_id", "offset_min", "minutes"])
    return L


def delivered_rate(S):
    """each stream's delivered key-field error rate in the closed quarter (second pass catches 88 per cent)"""
    F = S["F"]
    out = {}
    for code, g in F.groupby("code"):
        r = (g.miss.sum() + g.fa.sum()) / len(g)
        if code in W.Q3_SECOND_PASS:
            r *= 0.12
        out[code] = r
    return out


def boundary_days():
    return [dt.date(2026, 6, 25) + DAY * i for i in range(0, 101)]


def deliveries(S, rng):
    """delivery batches for every stream and shift-day from 25 June to 3 October 2026"""
    vol = S["vol"].set_index(["code", "day"]).docs
    rows = []
    for code, s in W.STREAMS.items():
        if code == "D6":
            continue
        c = s["client"]
        region = W.CLIENTS[c]["region"]
        for d in boundary_days():
            if (code, d) in vol.index:
                n = int(vol[(code, d)])
            elif W.Q3[0] <= d <= W.Q3[1] or d.weekday() == 6:
                continue
            else:
                if d.weekday() == 5 and code not in W.SAT_KF:
                    continue
                kf = W.SAT_KF[code] if d.weekday() == 5 else s["kf"]
                n = int(round(kf / W.kfpd(code, d) * math.exp(rng.normal(0, 0.15))))
            parts = np.array([0.22, 0.20, 0.58])
            k = np.floor(parts * n).astype(int)
            k[-1] = n - k[:-1].sum()
            for b, (hh, mm, plus) in enumerate(BATCH_TIMES[region]):
                t = dt.datetime(d.year, d.month, d.day, hh, mm) + DAY * plus + dt.timedelta(minutes=int(rng.integers(0, 9)))
                rows.append(dict(code=code, client=c, day=d, batch=b + 1, sent_ist=t, records=int(k[b])))
    D = pd.DataFrame(rows)
    D["file"] = [f"TDS_{W.SID[c]}_{d:%Y%m%d}_{b}.dat" for c, d, b in zip(D.code, D.day, D.batch)]
    D["sent_utc"] = D.sent_ist - dt.timedelta(hours=5, minutes=30)
    return D


def client_audits(S, D, rng):
    """each client's audit of sampled delivered claims: one row per finding round, a clean claim as one row"""
    rate = delivered_rate(S)
    rows = []
    seq = {}
    for r in D.itertuples():
        c = r.client
        k = rng.binomial(r.records, CLIENT_SAMPLE[c])
        for j in range(k):
            seq[c] = seq.get(c, 0) + int(rng.integers(1, 40))
            claim = seq[c]
            kf = W.kfpd(r.code, r.day)
            nerr = rng.binomial(kf, rate[r.code])
            biz = rng.random() < 0.045
            rows.append(dict(code=r.code, client=c, file=r.file, day=r.day, claim=claim, kf=kf, nerr=int(nerr), biz=bool(biz)))
    return pd.DataFrame(rows)


def findings(A, rng):
    """expand sampled claims into finding rows with client codes, re-review rounds and outcomes"""
    out = []
    for r in A.itertuples():
        c = r.client
        f = []
        for e in range(r.nerr):
            f.append(("CAP", rng.choice(CAPTURE_CODES[c])))
        if r.biz:
            f.append(("BIZ", rng.choice(BUSINESS_CODES[c])))
        if not f:
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, seq=0, kind="", reason="",
                            rnd=1, final=True))
            continue
        for i, (kind, reason) in enumerate(f, start=1):
            rereview = rng.random() < (0.10 if kind == "CAP" else 0.06)
            if not rereview:
                out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, seq=i, kind=kind,
                                reason=reason, rnd=1, final=True))
                continue
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, seq=i, kind=kind,
                            reason=reason, rnd=1, final=False))
            u = rng.random()
            if kind == "CAP":
                k2, r2 = ("NONE", "WD") if u < 0.5 else (("BIZ", rng.choice(BUSINESS_CODES[c])) if u < 0.7 else ("CAP", reason))
            else:
                k2, r2 = ("CAP", rng.choice(CAPTURE_CODES[c])) if u < 0.35 else ("BIZ", reason)
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, seq=i, kind=k2,
                            reason=r2, rnd=2, final=True))
    return pd.DataFrame(out)


def delivered_stamp(sent_utc, claim):
    """the client's delivery stamp: the gateway's transmission time in UTC plus the client's ingest lag"""
    return sent_utc + dt.timedelta(seconds=int(37 + (int(claim) * 13) % 1500))
