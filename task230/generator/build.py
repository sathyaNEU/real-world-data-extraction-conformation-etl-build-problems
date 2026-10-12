"""Build the pack under target/: simulate, write the exports, set the limits, write the filed documents."""
import datetime as dt
import os
import shutil

import numpy as np
import pandas as pd

import analysis as AN
import asks_sim as AS
import docs as DC
import nov
import pack as PK
import sim
import tune
import world as W


def _stream_rates(Fk, dd, rcv, capture):
    """one stream's client-audited residual three ways: golden (delivery date, every document of the claim), the
    received business date read as the delivery date, and one document per claim"""
    out = []
    for clock, per_claim in (("delivered", "index"), ("received", "index"), ("delivered", "one")):
        if clock == "delivered":
            ld = Fk.file.map(dd)
        else:
            ld = pd.Series([rcv[(f, c)] for f, c in zip(Fk.file, Fk.claim)], index=Fk.index)
        df = Fk[(ld >= W.Q3[0]) & (ld <= W.Q3[1])]
        cl = df.drop_duplicates("claim")
        den = (cl.kf if per_claim == "index" else cl.kf / cl.nd).sum()
        f = df[df.seq > 0]
        last = f.groupby(["claim", "seq"]).rnd.transform("max")
        f = f[(f.rnd == last) & f.reason.isin(capture)]
        out.append(len(f) / den * 1000)
    return out


def _clear(g, r, o):
    edge = abs((g * 100) % 1 - 0.5) < 0.05
    bad_r = abs(r - g) < 0.008 or round(r, 2) == round(g, 2)
    bad_o = round(o, 2) == round(g, 2)
    return not (edge or bad_r or bad_o)


def tune_client_audits(Fd, D, I, log=None):
    """the client audit device and its hazard, stream by stream: the golden residual clear of its two-decimal edge,
    the one-document reading off the golden, and the received business date read as the delivery date moving the
    residual by more than its decimal. Each stream is settled by the smallest change to what the client sampled:
    a clean boundary claim that carries a capture finding, or clean claims sampled or not in mid-quarter files."""
    import asks
    from zoneinfo import ZoneInfo
    utc = D.set_index("file").sent_utc
    dd = {f: pd.Timestamp(t).tz_localize("UTC").tz_convert(ZoneInfo(W.CLIENTS[c]["tz"])).date()
          for f, t, c in zip(D.file, D.sent_utc, D.client)}
    claims = I.groupby(["file", "code", "client", "day", "claim"], sort=True).size().rename("nd").reset_index()
    rcv = {(f, cl): AS.received_business_date(utc[f], c, cl) for f, c, cl in zip(Fd.file, Fd.client, Fd.claim)}
    q3 = lambda x: W.Q3[0] <= x <= W.Q3[1]
    mid = lambda d: W.Q3[0] + dt.timedelta(days=4) < d < W.Q3[1] - dt.timedelta(days=4)
    changed = 0
    parts = []
    for k in [c for c in W.ORDER if c != "D6"]:
        Fk = Fd[Fd.code == k].copy()
        cap = asks.CAPTURE[W.STREAMS[k]["client"]]
        if _clear(*_stream_rates(Fk, dd, rcv, cap)):
            parts.append(Fk)
            continue
        clean = Fk[Fk.seq == 0]
        boundary = [i for i, f, c in zip(clean.index, clean.file, clean.claim) if q3(dd[f]) != q3(rcv[(f, c)])]
        have = set(Fk.claim)
        pool = claims[(claims.code == k) & claims.day.map(mid) & ~claims.claim.isin(have)]
        for r in pool.itertuples():
            rcv[(r.file, r.claim)] = AS.received_business_date(utc[r.file], r.client, r.claim)
        inner_clean = [i for i, d in zip(clean.index, clean.day) if mid(d)]
        trials = [("finding", [i]) for i in boundary[:30]]
        for n in range(1, 41):
            trials += [("add", n), ("drop", n)]
        done = False
        for kind, arg in trials:
            if kind == "finding":
                G = Fk.copy()
                for i in arg:
                    G.loc[i, ["seq", "kind", "reason", "rnd", "final"]] = [1, "CAP", AS.CAPTURE_CODES[W.STREAMS[k]["client"]][0], 1, True]
            elif kind == "add":
                if arg > len(pool):
                    continue
                pick = pool.iloc[np.linspace(0, len(pool) - 1, arg).astype(int)]
                extra = pd.DataFrame([dict(claim=int(r.claim), code=r.code, client=r.client, file=r.file, day=r.day,
                                           kf=int(r.nd) * W.kfpd(r.code, r.day), nd=int(r.nd), seq=0, kind="", reason="",
                                           rnd=1, final=True) for r in pick.itertuples()])
                G = pd.concat([Fk, extra], ignore_index=True)
            else:
                if arg > len(inner_clean):
                    continue
                G = Fk.drop(index=inner_clean[:arg])
            if _clear(*_stream_rates(G, dd, rcv, cap)):
                parts.append(G)
                changed += arg if isinstance(arg, int) else len(arg)
                done = True
                break
        if not done:
            raise AssertionError(f"client audit tuning: no clear setting for {k}")
    Fd = pd.concat(parts, ignore_index=True)
    if log is not None:
        log.append(changed)
    return Fd


def tune_sessions(L, plan):
    """keep every stream's second-pass hours clear of its rounding edge: a few seconds on the family's longest lines"""
    fam = L.code.map(lambda c: W.STREAMS[c]["family"])
    docs = plan.groupby("code").docs.sum()
    L = L.copy()
    for f in ("printed", "mixed", "handwritten", "typed"):
        codes = [c for c in W.ORDER if W.STREAMS[c]["family"] == f]
        m = (fam == f).values
        n = L[m].doc_id.nunique()
        base = L[m].secs.sum()
        order = L[m].sort_values(["secs", "doc_id", "session"], ascending=[False, True, True]).index
        for step in [0] + [s * k for k in range(1, 400) for s in (60, -60)]:
            rate = (base + step) / 60.0 / n
            fr = [(docs[c] * rate / 60) % 1 for c in codes]
            if all(abs(x - 0.5) > 0.12 for x in fr):
                break
        else:
            raise AssertionError(f"no clear setting for {f}")
        if step:
            k = abs(step)
            idx = order[:k] if k <= len(order) else order
            per = 1 if step > 0 else -1
            L.loc[idx, "secs"] = L.loc[idx, "secs"] + per * (k // len(idx))
            rem = k - (k // len(idx)) * len(idx)
            if rem:
                L.loc[idx[:rem], "secs"] = L.loc[idx[:rem], "secs"] + per
    return L


def _fam_rates(L):
    fam = L.code.map(lambda c: W.STREAMS[c]["family"])
    lines = fam.value_counts()
    u = L.assign(fam=fam).drop_duplicates(["session", "part"])
    return (u.groupby("fam").minutes.sum() / lines).to_dict()


def _credit(plan):
    out = {}
    pl = plan.assign(client=plan.code.map(lambda c: W.STREAMS[c]["client"]))
    acct = pl.groupby("client").docs.sum()
    for c in W.ORDER:
        cl = W.STREAMS[c]["client"]
        b = W.BANDS[cl]
        bi = max(i for i, f in enumerate(b["floors"]) if acct[cl] >= f)
        base = b["price"][c][bi]
        amt = 0.0
        for r in pl[pl.code == c].itertuples():
            p = base
            if "index" in b and r.day >= b["index"][0]:
                p = round(base * (1 + b["index"][1] / 100.0), 4)
            amt += r.docs * p
        out[c] = W.CREDIT_PCT[c] / 100.0 * amt
    return out


def tune_volumes(fc, L):
    """keep every stream's hours and credit at stake off a rounding edge by a document or a bundle in the accepted
    forecast's first full November week"""
    rate = _fam_rates(L)
    for _ in range(300):
        plan = nov.plan_daily(fc)
        hrs = {c: plan[plan.code == c].docs.sum() * rate[W.STREAMS[c]["family"]] / 60 for c in W.ORDER}
        cr = _credit(plan)
        edge = [c for c in W.ORDER if abs(hrs[c] % 1 - 0.5) < 0.08 or abs(cr[c] % 1 - 0.5) < 0.04]
        if not edge:
            return fc, plan
        c = edge[0]
        idx = fc[(fc.code == c) & fc.accepted & (fc.week_start >= dt.date(2026, 11, 1))].index[0]
        fc.loc[idx, "units"] += 1
    raise AssertionError("volume tuning did not converge")


def build(target, quiet=False):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    S = sim.simulate()
    rng = np.random.default_rng(W.SEED + 5)
    L0 = AS.second_pass_sessions(S, rng)   # the sessions the plan of record's volumes were settled against; not shipped
    fc, plan = tune_volumes(nov.weekly_forecasts(), L0)
    roster = nov.roster(S["P"])
    sp, ed = PK.spine_and_edits(S, target)
    au = PK.audit(S, target)
    PK.workforce_register(S, target)
    PK.stream_register(target)
    PK.form_specs(target)
    PK.operating_plan(S, plan, roster, target)
    PK.forecasts(fc, target)
    L = AS.second_pass_v2(S, np.random.default_rng(W.SEED + 61))
    L = tune_sessions(L, plan)
    PK.sessions_export(L, target)
    D, I = AS.deliveries_v2(S, np.random.default_rng(W.SEED + 67))
    A = AS.client_audits_v2(S, D, I, np.random.default_rng(W.SEED + 71))
    Fd = AS.findings(A, np.random.default_rng(W.SEED + 73))
    added = []
    Fd = tune_client_audits(Fd, D, I, added)
    PK.manifests(D, target)
    PK.delivery_index(I, target)
    PK.client_audit_files(Fd, D, target)
    PK.ocr_summary(S, target)
    PK.keystroke_telemetry(sp, target)
    # limits from the closed quarter as the shipped audit measures it
    pk = AN.Pack.__new__(AN.Pack)
    pk.t = target
    pk.sp, pk.ed, pk.au = sp, ed, au
    pk.emp = AN._xl(os.path.join(target, PK.FILES["workforce"]), "Employees")
    pk.badge = AN._xl(os.path.join(target, PK.FILES["workforce"]), "Badge allocation")
    pk.streams = pd.read_csv(os.path.join(target, PK.FILES["streams"]))
    pk.kfields = AN._xl(os.path.join(target, PK.FILES["forms"]), "Key fields")
    Qr = AN.Quarter(pk)
    q3m = Qr.q3_measured()
    limits = tune.limits(q3m)
    DC.qcp04(target)
    DC.quality_schedules(target, limits)
    a = Qr.a[Qr.a.code == "D6"]
    s6 = Qr.scr[Qr.scr.code == "D6"]
    P = dict(days=int(s6.day.nunique()), docs=int(len(s6)), kf=int(s6.key_fields.sum()), audited=int(len(a)),
             ocr_pct=100 * a.err.mean(), residual=q3m["D6"], docs_per_day=int(round(len(s6) / s6.day.nunique(), -1)))
    DC.pilot_report(target, P)
    DC.labour_note(target)
    DC.notes(target, dict(spine=len(sp), edits=len(ed), audit=len(au), sessions=len(L)))
    return dict(S=S, limits=limits, q3m=q3m, findings_added=added[0], plan=plan)
