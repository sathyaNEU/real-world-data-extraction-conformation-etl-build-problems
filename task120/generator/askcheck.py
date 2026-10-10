"""Every ask figure computed from shipped frames only, under the golden handling and under each
mishandling, so the generator can assert the stops, the composed-subset deltas and the
separation. Tier membership comes from the household construction over the shipped return
file and schedule (or the filing-unit construction for the S4 stop)."""
import itertools

import numpy as np
import pandas as pd

from common import k_top, round_thousand

DUE = {1: "2025-04-15", 2: "2025-06-16", 3: "2025-09-15", 4: "2026-01-15"}
NOMINAL = {1: "2025-04-15", 2: "2025-06-15", 3: "2025-09-15", 4: "2026-01-15"}


def membership(R, S, unit="household"):
    """(return tier by return_id, TIN -> tier, tier AGI, floors) for TY2025 residents."""
    r = R[R.residency_code == 1]
    s = S[S.claimant_return_id.isin(r.return_id)]
    key = r.federal_primary_tin.to_numpy().copy()
    if unit == "household":
        is_dep = r.filer_tin.isin(s.dependent_tin).to_numpy()
        claim = s.set_index("dependent_tin").claimant_return_id
        fp = r.set_index("return_id").federal_primary_tin
        key[is_dep] = fp.loc[claim.loc[r.filer_tin.to_numpy()[is_dep]].to_numpy()].to_numpy()
    tot = pd.Series(r.federal_agi.to_numpy().astype(np.int64)).groupby(key).sum()
    v = np.sort(tot.to_numpy())[::-1]
    floors = [round_thousand(v[k_top(len(v), p) - 1]) for p in (10, 5, 1)]
    t = np.zeros(len(tot), np.int8)
    a = tot.to_numpy()
    t[a >= floors[0]] = 3
    t[a >= floors[1]] = 2
    t[a >= floors[2]] = 1
    tier_of_key = pd.Series(t, index=tot.index)
    rt = tier_of_key.loc[key].to_numpy()
    ret_tier = pd.Series(rt, index=r.return_id.to_numpy())
    tin_tier = dict(zip(r.filer_tin.to_numpy().astype(np.int64).tolist(), rt.tolist()))
    sp = (r.filing_status.to_numpy() == 2) & (r.spouse_tin.to_numpy() > 0)
    tin_tier.update(zip(r.spouse_tin.to_numpy()[sp].astype(np.int64).tolist(), rt[sp].tolist()))
    tier_agi = {k: int(a[t == k].sum()) for k in (1, 2, 3)}
    return ret_tier, tin_tier, tier_agi, floors


def _resolve(tins, tin_tier, reg, use_register):
    out = np.zeros(len(tins), np.int8)
    rmap = {}
    if use_register:
        ok = reg[reg.case_status == "RESOLVED"]
        rmap = dict(zip(ok.reported_tin.to_numpy().astype(np.int64).tolist(), ok.resolved_tin.to_numpy().astype(np.int64).tolist()))
    for i, t in enumerate(tins.tolist()):
        if t in tin_tier:
            out[i] = tin_tier[t]
        elif t in rmap and rmap[t] in tin_tier:
            out[i] = tin_tier[rmap[t]]
    return out


def instalment(ts_utc, clock_ok):
    t = pd.to_datetime(pd.Series(ts_utc), utc=True)
    out = np.full(len(t), 4, np.int8)
    if clock_ok:
        loc = t.dt.tz_convert("America/Chicago").dt.tz_localize(None)
        for k in (3, 2, 1):
            cut = pd.Timestamp(DUE[k]) + pd.Timedelta(hours=23, minutes=59, seconds=59)
            out[(loc <= cut).to_numpy()] = k
    else:
        d = t.dt.tz_localize(None).dt.normalize()
        for k in (3, 2, 1):
            out[(d <= pd.Timestamp(NOMINAL[k])).to_numpy()] = k
    return out


def receipts(led, ret_items, reg, tin_tier, clock=True, xfer=True, returned=True, register=True, overclean=False):
    """{(tier, instalment): dollars}. clock: Central time against the rolled due dates;
    xfer: a transfer citing a payment is cash dated by that payment, one citing a return is not a
    receipt; returned: items returned and not paid are out, re-presented and paid stay;
    register: resolved register rows link a TIN as reported to its filer."""
    L = led[led.tax_year == 2025]
    es = L[L.txn_type == "ES"]
    tr = L[L.txn_type == "TRF"]
    if overclean:
        tr = tr.iloc[0:0]
        es = es[~es.txn_id.isin(ret_items.txn_id)]
    elif returned:
        bad = ret_items[ret_items.represented_result != "PAID"].txn_id
        es = es[~es.txn_id.isin(bad)]
    ts = es.txn_utc.to_numpy()
    tins = es.account_tin.to_numpy().astype(np.int64)
    amt = es.amount.to_numpy().astype(np.int64)
    if len(tr):
        if xfer:
            pay_ref = tr[tr.source_ref.str.len() == 11]
            orig = led.set_index(led.txn_id.astype(str)).txn_utc
            ts = np.concatenate([ts, orig.loc[pay_ref.source_ref].to_numpy()])
            tins = np.concatenate([tins, pay_ref.account_tin.to_numpy().astype(np.int64)])
            amt = np.concatenate([amt, pay_ref.amount.to_numpy().astype(np.int64)])
        else:
            ts = np.concatenate([ts, tr.txn_utc.to_numpy()])
            tins = np.concatenate([tins, tr.account_tin.to_numpy().astype(np.int64)])
            amt = np.concatenate([amt, tr.amount.to_numpy().astype(np.int64)])
    tier = _resolve(tins, tin_tier, reg, register)
    inst = instalment(ts, clock)
    out = {}
    for t in (1, 2, 3):
        for k in (1, 2, 3, 4):
            out[(t, k)] = int(amt[(tier == t) & (inst == k)].sum())
    return out


def gains(ext, log, ret_tier, versions=True, loss_limit=True, original=False):
    """{tier: dollars}: the capital gain entering AGI on the version of record."""
    col = "amount_in_agi" if loss_limit else "net_gain_loss"
    x = ext.set_index("return_id")[col].astype("int64").copy()
    if versions or original:
        lg = log[log.net_gain_loss.notna()]
        if original:
            pick = lg[lg.amendment_seq == 0]
        else:
            acc = lg[lg.disposition == "ACCEPTED"]
            pick = acc.sort_values(["return_id", "amendment_seq"]).groupby("return_id").tail(1)
        pick = pick[pick.return_id.isin(x.index)]
        x.loc[pick.return_id.to_numpy()] = pick[col].astype("int64").to_numpy()
    t = ret_tier.reindex(x.index).fillna(0).astype(int).to_numpy()
    return {k: int(x.to_numpy()[t == k].sum()) for k in (1, 2, 3)}


def withholding(ef, paper, reg, tin_tier, paper_on=True, register=True, overclean=False):
    parts = [ef[["employer_ein", "employee_tin", "state_tax_withheld"]]]
    if paper_on:
        p = paper
        if overclean:
            p = p[~p.employer_ein.isin(ef.employer_ein)]
        parts.append(p[["employer_ein", "employee_tin", "state_tax_withheld"]])
    d = pd.concat(parts, ignore_index=True)
    tier = _resolve(d.employee_tin.to_numpy().astype(np.int64), tin_tier, reg, register)
    w = d.state_tax_withheld.to_numpy().astype(np.int64)
    return {k: int(w[tier == k].sum()) for k in (1, 2, 3)}


def share(g, a):
    return {k: round(100.0 * g[k] / a[k], 1) for k in (1, 2, 3)}


def share_exact(g, a):
    return {k: 100.0 * g[k] / a[k] for k in (1, 2, 3)}


A1_DEVICES = ("clock", "xfer", "returned", "register")
A2_DEVICES = ("versions", "loss_limit")
A3_DEVICES = ("paper_on", "register")


def subsets(devs):
    for r in range(1, len(devs) + 1):
        for c in itertools.combinations(devs, r):
            yield c
