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
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, nd=getattr(r, 'ndocs', 1), seq=0, kind="", reason="",
                            rnd=1, final=True))
            continue
        for i, (kind, reason) in enumerate(f, start=1):
            rereview = rng.random() < (0.10 if kind == "CAP" else 0.06)
            if not rereview:
                out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, nd=getattr(r, 'ndocs', 1), seq=i, kind=kind,
                                reason=reason, rnd=1, final=True))
                continue
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, nd=getattr(r, 'ndocs', 1), seq=i, kind=kind,
                            reason=reason, rnd=1, final=False))
            u = rng.random()
            if kind == "CAP":
                k2, r2 = ("NONE", "WD") if u < 0.5 else (("BIZ", rng.choice(BUSINESS_CODES[c])) if u < 0.7 else ("CAP", reason))
            else:
                k2, r2 = ("CAP", rng.choice(CAPTURE_CODES[c])) if u < 0.35 else ("BIZ", reason)
            out.append(dict(claim=r.claim, code=r.code, client=c, file=r.file, day=r.day, kf=r.kf, nd=getattr(r, 'ndocs', 1), seq=i, kind=k2,
                            reason=r2, rnd=2, final=True))
    return pd.DataFrame(out)


def delivered_stamp(sent_utc, claim):
    """the client's delivery stamp: the gateway's transmission time in UTC plus the client's ingest lag"""
    return sent_utc + dt.timedelta(seconds=int(37 + (int(claim) * 13) % 1500))


# ----------------------------------------------------------------------------------------------- the rebuilt ask records
def _next_day(d):
    return d + DAY


def second_pass_v2(S, rng):
    """September's second-pass work as the workflow tool logs it: one line per document worked in a session, with the
    seconds the document was open. A session is logged against the basket it opened on; a session whose basket runs dry
    is fed from the next basket in the tool's feed order and keeps its basket. The day team works the Hollings & Pryce
    pilot's basket and picks up the night's carry-over the same way. A document reopened after a client query is worked
    again in a later session."""
    docs = S["docs"]
    sep = docs[pd.to_datetime(docs.day).dt.month == 9]
    night = ["N1", "N2", "N3", "N4", "N5"]
    by = {k: list(g.doc_id.values) for k, g in sep[sep.code.isin(night + ["D6"])].groupby(["code", "day"])}
    days = sorted(sep.day.unique())
    sessions = []          # (session id, day, queue, badge, basket code, [(doc_id, true code)])
    sid = 611204
    carry = {}

    def new_sid():
        nonlocal sid
        sid += int(rng.integers(1, 4))
        return f"S2-{sid}"

    for d in days:
        pools = {}
        for c in night:
            ids = list(by.get((c, d), []))
            rng.shuffle(ids)
            k = int(rng.binomial(len(ids), W.SP_CARRY[c])) if ids else 0
            if k:
                carry.setdefault(_next_day(d), []).extend((i, c) for i in ids[-k:])
                ids = ids[:-k]
            pools[c] = [(i, c) for i in ids]
        nsess = {c: max(1, int(math.ceil(len(pools[c]) / 13.0))) if pools[c] else 0 for c in night}
        foreign = {c: [[] for _ in range(nsess[c])] for c in night}
        for c in night:
            f = W.SP_FEED[c]
            for s in range(nsess[c]):
                if rng.random() < W.SP_DRY[c] and pools[f]:
                    k = min(len(pools[f]), 1 + int(rng.poisson(4)))
                    foreign[c][s] = [pools[f].pop() for _ in range(k)]
        for c in night:
            own = pools[c]
            if not own and not any(foreign[c]):
                continue
            parts = np.array_split(np.arange(len(own)), max(1, nsess[c]))
            for s, idx in enumerate(parts):
                items = [own[i] for i in idx] + (foreign[c][s] if s < len(foreign[c]) else [])
                if items:
                    sessions.append((new_sid(), d, "N", SP_BADGES[int(rng.integers(len(SP_BADGES)))], c, items))
        # day team: the pilot's basket, fed from the night's carry-over once it runs dry
        hp = [(i, "D6") for i in by.get(("D6", d), [])]
        rng.shuffle(hp)
        co = list(carry.pop(d, []))
        rng.shuffle(co)
        if hp:
            n = max(1, int(math.ceil(len(hp) / 13.0)))
            for idx in np.array_split(np.arange(len(hp)), n):
                items = [hp[i] for i in idx]
                if co and rng.random() < W.SP_DAY_DRY:
                    k = min(len(co), 1 + int(rng.poisson(5)))
                    items += [co.pop() for _ in range(k)]
                sessions.append((new_sid(), d, "D", SP_BADGES[int(rng.integers(len(SP_BADGES)))], "D6", items))
        for c in night:
            mine = [x for x in co if x[1] == c]
            if mine:
                sessions.append((new_sid(), d, "D", SP_BADGES[int(rng.integers(len(SP_BADGES)))], c, mine))
    # rework: a document reopened after a client query is worked again in a later session on its own basket
    worked = [(x[0], x[1], s[1]) for s in sessions for x in s[5]]
    cand = [w for w in worked if w[2] <= dt.date(2026, 9, 24)]
    pick = rng.choice(len(cand), size=int(round(len(cand) * W.SP_REWORK)), replace=False)
    by_basket_day = {}
    for j, s in enumerate(sessions):
        by_basket_day.setdefault((s[4], s[1]), []).append(j)
    for p in sorted(pick):
        doc, code, d0 = cand[p]
        d1 = d0 + DAY * int(rng.integers(2, 7))
        for _ in range(10):
            js = by_basket_day.get((code, d1))
            if js:
                j = js[int(rng.integers(len(js)))]
                sessions[j][5].append((doc, code))
                break
            d1 += DAY
    rows = []
    for s_id, d, q, badge, basket, items in sessions:
        start = rng.uniform(0, 470 if q == "N" else 500)
        t = start
        for doc, code in items:
            fam = W.STREAMS[code]["family"]
            secs = int(round(60 * math.exp(rng.normal(math.log(W.SP_MIN[fam]) - 0.06, 0.35))))
            rows.append((s_id, d, q, badge, basket, doc, code, round(t, 2), secs))
            t += secs / 60.0 + float(rng.uniform(0.05, 0.4))
    L = pd.DataFrame(rows, columns=["session", "day", "queue", "badge", "basket", "doc_id", "code", "offset_min", "secs"])
    return L


def _claim_ref(client, code, n):
    return {"KBA": f"K{n:09d}", "NDS": f"NG-{n:07d}", "BMC": f"BMC{n:08d}", "HPB": f"H{n:010d}", "WBH": f"W{n:08d}",
            "CIP": f"C{n:08d}", "WPC": f"WPC-{n:08d}", "TCM": f"TCM-{n:08d}"}[client]


CLAIM_BASE = {"N1": 100125, "N2": 535420, "N3": 22018, "N4": 3310402, "N5": 400002118, "D1": 7120055, "D2": 7860210,
              "D3": 2204811, "D4": 9180044, "D5": 5150700}
BATCH_TIMES_V2 = {"US": [(23, 40, 0), (2, 35, 1), (5, 50, 1)], "AU": [(12, 10, 0), (16, 45, 0), (20, 20, 0)],
                  "UK": [(11, 40, 0), (16, 20, 0), (22, 45, 0)]}


def deliveries_v2(S, rng):
    """delivery batches for every stream and shift-day from 25 June to 3 October 2026, and the delivery index: each
    batch's documents grouped into the claims they belong to"""
    docs = S["docs"]
    q3ids = {k: list(g.doc_id.values) for k, g in docs[docs.code != "D6"].groupby(["code", "day"])}
    rows, idx = [], []
    seqn = {}
    nclaim = dict(CLAIM_BASE)
    for d in boundary_days():
        for code, s in W.STREAMS.items():
            if code == "D6":
                continue
            c = s["client"]
            region = W.CLIENTS[c]["region"]
            q = s["q3"]
            if (code, d) in q3ids:
                ids = q3ids[(code, d)]
            elif W.Q3[0] <= d <= W.Q3[1] or d.weekday() == 6:
                continue
            else:
                if d.weekday() == 5 and code not in W.SAT_KF:
                    continue
                kf = W.SAT_KF[code] if d.weekday() == 5 else s["kf"]
                n = int(round(kf / W.kfpd(code, d) * math.exp(rng.normal(0, 0.15))))
                doy = d.timetuple().tm_yday
                k0 = seqn.get((d, q), 0)
                ids = [f"26{doy:03d}{q}{k0 + i:06d}" for i in range(n)]
                seqn[(d, q)] = k0 + n
            n = len(ids)
            parts = np.array([0.22, 0.20, 0.58])
            k = np.floor(parts * n).astype(int)
            k[-1] = n - k[:-1].sum()
            pos = 0
            for b, (hh, mm, plus) in enumerate(BATCH_TIMES_V2[region]):
                t = dt.datetime(d.year, d.month, d.day, hh, mm) + DAY * plus + dt.timedelta(minutes=int(rng.integers(0, 9)))
                f = f"TDS_{W.SID[code]}_{d:%Y%m%d}_{b + 1}.dat"
                bid = ids[pos:pos + k[b]]
                pos += k[b]
                rows.append(dict(code=code, client=c, day=d, batch=b + 1, sent_ist=t, records=len(bid), file=f))
                p = W.CLAIM_DOCS[code]
                i = 0
                while i < len(bid):
                    m = min(len(bid) - i, 1 + int(rng.choice(3, p=p)))
                    nclaim[code] += 1 + int(rng.integers(0, 3))
                    for j in range(m):
                        idx.append((f, code, c, d, nclaim[code], bid[i + j], j + 1))
                    i += m
    D = pd.DataFrame(rows)
    D["sent_utc"] = D.sent_ist - dt.timedelta(hours=5, minutes=30)
    I = pd.DataFrame(idx, columns=["file", "code", "client", "day", "claim", "doc_id", "sheet"])
    return D, I


def client_audits_v2(S, D, I, rng):
    """each client's audit of sampled delivered claims (every document of a sampled claim is audited)"""
    rate = delivered_rate(S)
    C = I.groupby(["file", "code", "client", "day", "claim"], sort=False).size().rename("ndocs").reset_index()
    rows = []
    for r in C.itertuples():
        if rng.random() >= CLIENT_SAMPLE[r.client]:
            continue
        kf = int(r.ndocs) * W.kfpd(r.code, r.day)
        nerr = rng.binomial(kf, rate[r.code])
        biz = rng.random() < 0.045
        rows.append(dict(code=r.code, client=r.client, file=r.file, day=r.day, claim=int(r.claim), ndocs=int(r.ndocs),
                         kf=kf, nerr=int(nerr), biz=bool(biz)))
    return pd.DataFrame(rows)


def received_business_date(sent_utc, client, claim):
    """the client's claims system dates a receipt by business day"""
    from zoneinfo import ZoneInfo
    t = pd.Timestamp(delivered_stamp(sent_utc, claim)).tz_localize("UTC").tz_convert(ZoneInfo(W.CLIENTS[client]["tz"]))
    d = t.date()
    if (t.hour, t.minute) >= W.RECEIPT_CUTOFF[client]:
        d += DAY
    hol = W.RECEIPT_HOLIDAYS[W.CLIENTS[client]["region"]]
    while d.weekday() >= 5 or d in hol:
        d += DAY
    return d
