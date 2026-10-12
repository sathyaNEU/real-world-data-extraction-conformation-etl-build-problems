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


def tune_client_audits(Fd, D, log=None):
    """the client audit device: every stream's quarter moves by more than its decimal when the UTC stamps are read
    as the client's local date (the boundary batches carry findings in both directions as delivered)"""
    import asks
    n_added = 0
    for _ in range(120):
        g = asks.client_audit_rates(Fd, D)
        c = asks.client_audit_rates(Fd, D, clock="utc_as_local")
        bad = [k for k in g if abs(c[k] - g[k]) < 0.12 or round(c[k], 1) == round(g[k], 1)]
        edge = [k for k in g if abs((g[k] * 10) % 1 - 0.5) < 0.15]
        if not bad and edge:
            # move the stream's quarter off a rounding edge by the number of clean claims the client sampled
            k = edge[0]
            inc_c, inc_g = asks.boundary_batches(Fd, D, k)
            inner = Fd[(Fd.code == k) & ~Fd.file.isin(inc_c + inc_g) & (Fd.day > W.Q3[0] + dt.timedelta(days=3))
                       & (Fd.day < W.Q3[1] - dt.timedelta(days=3)) & (Fd.seq == 0)]
            r0 = g[k]
            u = (r0 * 10) % 1
            target = r0 - (u - 0.25) / 10 if u < 0.5 else r0 + (0.75 - u) / 10
            kf = float(inner.kf.mean())
            claims = Fd[Fd.code == k]
            den = claims.drop_duplicates("claim").kf.sum()
            num = r0 * den / 1000
            n = int(round((num * 1000 / target - den) / kf))
            if n > 0:
                extra = inner.iloc[:n].copy()
                extra["claim"] = Fd.claim.max() + 7 + np.arange(len(extra)) * 3
                Fd = pd.concat([Fd, extra], ignore_index=True)
            elif n < 0:
                Fd = Fd.drop(index=inner.index[:(-n)])
            n_added += abs(n)
            continue
        if not bad:
            if log is not None:
                log.append(n_added)
            return Fd
        k = bad[0]
        inc_c, inc_g = asks.boundary_batches(Fd, D, k)
        sign = 1 if c[k] >= g[k] else -1
        files = inc_c if sign > 0 else inc_g
        rows = Fd[(Fd.code == k) & Fd.file.isin(files) & (Fd.seq == 0)]
        if rows.empty:
            raise AssertionError(f"no clean sampled claim in the boundary batches of {k}")
        r = rows.iloc[0]
        Fd = Fd.drop(index=r.name)
        add = r.to_dict()
        add.update(seq=1, kind="CAP", reason=AS.CAPTURE_CODES[r.client][0], rnd=1, final=True)
        Fd = pd.concat([Fd, pd.DataFrame([add])], ignore_index=True)
        n_added += 1
    raise AssertionError("client audit device did not converge")


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
    L = AS.second_pass_sessions(S, rng)
    fc, plan = tune_volumes(nov.weekly_forecasts(), L)
    roster = nov.roster(S["P"])
    sp, ed = PK.spine_and_edits(S, target)
    au = PK.audit(S, target)
    PK.workforce_register(S, target)
    PK.stream_register(target)
    PK.form_specs(target)
    PK.operating_plan(S, plan, roster, target)
    PK.forecasts(fc, target)
    v = S["vol"]
    v = v[pd.to_datetime(v.day).dt.month == 9]
    sep = v.assign(client=v.code.map(lambda c: W.STREAMS[c]["client"])).groupby("client").docs.sum().to_dict()
    PK.billing_register(target, sep)
    PK.sessions_export(L, target)
    D = AS.deliveries(S, rng)
    A = AS.client_audits(S, D, rng)
    Fd = AS.findings(A, rng)
    added = []
    Fd = tune_client_audits(Fd, D, added)
    PK.manifests(D, target)
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
    DC.rate_cards(target)
    a = Qr.a[Qr.a.code == "D6"]
    s6 = Qr.scr[Qr.scr.code == "D6"]
    P = dict(days=int(s6.day.nunique()), docs=int(len(s6)), kf=int(s6.key_fields.sum()), audited=int(len(a)),
             ocr_pct=100 * a.err.mean(), residual=q3m["D6"], docs_per_day=int(round(len(s6) / s6.day.nunique(), -1)))
    DC.pilot_report(target, P)
    DC.labour_note(target)
    DC.notes(target, dict(spine=len(sp), edits=len(ed), audit=len(au)))
    return dict(S=S, limits=limits, q3m=q3m, findings_added=added[0])
