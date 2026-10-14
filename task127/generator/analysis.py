"""Every rung of the main call and both asks, computed from the pack as shipped (load.py).

The book: accident quarters 2017 Q1 to 2026 Q4 (index 0 to 39), evaluated at quarter ends on Central time; the cell
(i, j) is accident quarter i at age j + 1, the end of calendar quarter i + j."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import load as L

NQ = K.N_AQ
Y0 = K.FIRST_AQ[0]


def qidx(t: pd.Series) -> np.ndarray:
    """The calendar-quarter index (0 is 2017 Q1) of each datetime."""
    return ((t.dt.year - Y0) * 4 + (t.dt.month - 1) // 3).to_numpy()


def _noon(d: pd.Series) -> pd.Series:
    return d + pd.Timedelta(hours=12)


# ------------------------------------------------------------------ the book as recorded

def book(target):
    """Payments, claimant features and their closing histories from both systems."""
    lc, lp = L.legacy_claims(target), L.legacy_payments(target)
    pf, ev, pp = L.features(target), L.events(target), L.payments(target)
    # payments: legacy by transaction date, platform by issue and void times, each on its accident quarter
    acc_of = dict(zip(pf.feature_id, pf.acc))
    pays = pd.concat([
        pd.DataFrame({"acc": lp.acc, "t": _noon(lp.date), "amount": lp.amount, "fid": lp.key, "sys": "legacy"}),
        pd.DataFrame({"acc": pp.feature_id.map(acc_of), "t": pp.issued, "amount": pp.amount, "fid": pp.feature_id,
                      "sys": "platform", "method": pp.method}),
        pd.DataFrame({"acc": pp.feature_id.map(acc_of)[pp.voided.notna()], "t": pp.voided[pp.voided.notna()],
                      "amount": -pp.amount[pp.voided.notna()], "fid": pp.feature_id[pp.voided.notna()],
                      "sys": "platform", "method": pp.method[pp.voided.notna()]}),
    ], ignore_index=True)
    pays["aq"] = qidx(pays.acc)
    pays["tq"] = qidx(pays.t)
    # claimant features: the legacy archive without its converted and opened-in-error rows, the platform register
    # without its duplicates, a re-entered legacy feature once
    keep_l = lc[~lc.DISP.isin(["CV", "XD"])]
    real_p = pf[pf.disposition != "DUPLICATE"]
    cv_keys = set(lc.key[lc.DISP == "CV"])
    re_keys = set(real_p.legacy_ref[(real_p.legacy_ref != "") & ~real_p.legacy_ref.isin(cv_keys)])
    trans = []          # (feature, time, +1 closing or -1 reopening)
    for k, t in zip(keep_l.key, keep_l.cls):
        trans.append((k, t + pd.Timedelta(hours=12), 1))
    evx = ev[ev.event.isin(["CLOSED", "REOPENED"])]
    fid_key = dict(zip(real_p.feature_id, np.where(real_p.legacy_ref.isin(re_keys), real_p.legacy_ref,
                                                    real_p.feature_id)))
    evx = evx[evx.feature_id.isin(fid_key)]
    for fid, e, t in zip(evx.feature_id, evx.event, evx["at"]):
        trans.append((fid_key[fid], t, 1 if e == "CLOSED" else -1))
    feats = pd.concat([
        pd.DataFrame({"key": keep_l.key, "acc": keep_l.acc, "rep": keep_l.rep, "sys": "legacy"}),
        pd.DataFrame({"key": real_p.feature_id[~real_p.legacy_ref.isin(re_keys)],
                      "acc": real_p.acc[~real_p.legacy_ref.isin(re_keys)],
                      "rep": real_p.rep[~real_p.legacy_ref.isin(re_keys)], "sys": "platform"}),
    ], ignore_index=True)
    feats["aq"] = qidx(feats.acc)
    feats["rq"] = qidx(feats.rep)
    tr = pd.DataFrame(trans, columns=["key", "t", "d"])
    tr["aq"] = tr.key.map(dict(zip(feats.key, feats.aq)))
    tr["tq"] = qidx(tr.t)
    return dict(pays=pays, feats=feats, trans=tr, lc=lc, lp=lp, pf=pf, ev=ev, pp=pp, re_keys=re_keys, cv_keys=cv_keys)


def _cum(aq, tq, w):
    m = np.zeros((NQ, NQ))
    ok = (tq < NQ) & (aq >= 0) & (aq < NQ)
    np.add.at(m, (aq[ok], np.maximum(tq[ok], aq[ok])), w[ok])
    c = np.cumsum(m, axis=1)
    out = np.full((NQ, NQ), np.nan)
    for i in range(NQ):
        out[i, :NQ - i] = c[i, i:]
    return out


def triangles(b):
    P = _cum(b["pays"].aq.to_numpy(), b["pays"].tq.to_numpy(), b["pays"].amount.to_numpy())
    f = b["feats"]
    R = _cum(f.aq.to_numpy(), f.rq.to_numpy(), np.ones(len(f)))
    tr = b["trans"]
    C = _cum(tr.aq.to_numpy(), tr.tq.to_numpy(), tr.d.to_numpy().astype(float))
    return P, C, R


# ------------------------------------------------------------------ development

LAST = np.array([NQ - 1 - i for i in range(NQ)])


def latest(T):
    return np.array([T[i, LAST[i]] for i in range(NQ)])


def factors(T, ok=None, average="weighted"):
    f = []
    for j in range(NQ - 1):
        rows = [i for i in range(NQ) if not np.isnan(T[i, j + 1]) and (ok is None or ok(i, j))]
        if not rows:
            f.append(1.0)
        elif average == "weighted":
            f.append(sum(T[i, j + 1] for i in rows) / sum(T[i, j] for i in rows))
        else:
            f.append(float(np.mean([T[i, j + 1] / T[i, j] for i in rows if T[i, j] > 0])))
    return np.array(f)


def project(f, base):
    return np.array([base[i] * np.prod(f[LAST[i]:]) for i in range(NQ)])


def chain_ladder(P, ok=None, average="weighted"):
    lat = latest(P)
    return project(factors(P, ok, average), lat) - lat


def ultimate_counts(R):
    return project(factors(R), latest(R))


def restate(P, D, interp="linear"):
    """The paid history restated at the latest diagonal's closure ratio for each age (Berquist and Sherman): each
    accident quarter's paid at the ratio the latest diagonal shows, read off its own paid-against-ratio history."""
    target = {LAST[i]: D[i, LAST[i]] for i in range(NQ)}
    out = P.copy()
    for i in range(NQ):
        xs = np.r_[0.0, D[i, :LAST[i] + 1]]
        ys = np.r_[0.0, P[i, :LAST[i] + 1]]
        for j in range(LAST[i]):
            tg = target[j]
            k = int(np.searchsorted(xs, tg))
            k = min(max(k, 1), len(xs) - 1)
            x0, x1, y0, y1 = xs[k - 1], xs[k], ys[k - 1], ys[k]
            if x1 <= x0:
                out[i, j] = y1
                continue
            w = (tg - x0) / (x1 - x0)
            if interp == "linear" or y0 <= 0 or y1 <= 0:
                out[i, j] = y0 + (y1 - y0) * w
            else:
                out[i, j] = y0 * (y1 / y0) ** w
    return out


def restated_unpaid(P, C, R, interp="linear", base="ultimate", ok=None, average="weighted"):
    n = ultimate_counts(R) if base == "ultimate" else latest(R)
    D = C / n[:, None]
    Rs = restate(P, D, interp)
    lat = latest(P)
    return project(factors(Rs, ok, average), lat) - lat, D


def by_year(per_q):
    return {Y0 + y: float(sum(per_q[4 * y:4 * y + 4])) for y in range(NQ // 4)}


# ------------------------------------------------------------------ the rungs

def main_call(target):
    b = book(target)
    P, C, R = triangles(b)
    lat = latest(P)
    out = dict(P=P, C=C, R=R, paid_to_date=float(lat.sum()), paid_by_year=by_year(lat))
    out["cl"] = chain_ladder(P)
    for n in (4, 8, 12):
        out["cl_last%d" % n] = chain_ladder(P, ok=lambda i, j, n=n: i + j + 1 >= NQ - n)
    out["bs"], out["D"] = restated_unpaid(P, C, R)
    out["bs_exp"], _ = restated_unpaid(P, C, R, interp="exponential")
    out["bs_rep"], _ = restated_unpaid(P, C, R, base="reported")
    out["bs_exp_rep"], _ = restated_unpaid(P, C, R, interp="exponential", base="reported")
    out["bs_simple"], _ = restated_unpaid(P, C, R, average="simple")
    out["bs_last12"], _ = restated_unpaid(P, C, R, ok=lambda i, j: i + j + 1 >= NQ - 12)
    out["n_ult"] = ultimate_counts(R)
    out["booked"] = L.booked(target)
    out["b"] = b
    return out


def closure_rows(D, ages=(4, 8, 12)):
    """The share of ultimate claimant features closed at each age: the accident quarters of 2018 to 2020 against
    the latest diagonal."""
    rows = {}
    for a in ages:
        j = a - 1
        hist = float(np.mean([D[i, j] for i in range(4, 16)]))
        rows[a] = (hist, float(D[NQ - 1 - j, j]), K.aq_label(NQ - 1 - j))
    return rows


def actual_vs_expected(P, k=4):
    """Payments in the latest k calendar quarters against what the all-quarter factors fitted to the triangle as it
    stood k quarters ago expected."""
    M = P.copy()
    for i in range(NQ):
        for j in range(NQ):
            if i + j > NQ - 1 - k:
                M[i, j] = np.nan
    f = factors(M)
    act = exp = 0.0
    for i in range(NQ):
        j0 = LAST[i] - k
        if j0 < 0:
            continue
        exp += P[i, j0] * (np.prod(f[j0:LAST[i]]) - 1.0)
        act += P[i, LAST[i]] - P[i, j0]
    return act, exp


def frequency_severity(b, n_ult, P, mature=12):
    """Two frequency-severity readings: each accident quarter's open and unreported features at the average paid on
    its closed features, and ultimate features at a severity trended from the most mature quarters."""
    lat = latest(P)
    pays, tr = b["pays"], b["trans"]
    paid_key = pays[pays.tq < NQ].groupby("fid").amount.sum()
    # closed at the valuation: net closings at or before the end of 2026 Q4
    closed = tr[tr.tq < NQ].groupby("key").d.sum()
    closed = closed[closed > 0].index
    f = b["feats"]
    naive = 0.0
    for i in range(NQ):
        keys = f.key[f.aq == i]
        ck = keys[keys.isin(closed)]
        sev = float(paid_key.reindex(ck).fillna(0.0).sum()) / max(len(ck), 1)
        naive += (n_ult[i] - len(ck)) * sev - (lat[i] - float(paid_key.reindex(ck).fillna(0.0).sum()))
    s = np.log([lat[i] / n_ult[i] for i in range(mature)])
    beta = np.polyfit(np.arange(mature), s, 1)
    trend = sum(n_ult[i] * np.exp(np.polyval(beta, i)) - lat[i] for i in range(mature, NQ))
    trend += float(chain_ladder(P)[:mature].sum())
    return naive, trend, float(np.exp(4 * beta[0]) - 1.0)


def annual(b, restated=True, interp="linear"):
    """Accident years at year-end ages (12, 24, ... months)."""
    pays, f, tr = b["pays"], b["feats"], b["trans"]
    NY = NQ // 4

    def tri(ay, ty, w):
        m = np.zeros((NY, NY))
        ok = (ty < NY) & (ay >= 0) & (ay < NY)
        np.add.at(m, (ay[ok], np.maximum(ty[ok], ay[ok])), w[ok])
        c = np.cumsum(m, axis=1)
        out = np.full((NY, NY), np.nan)
        for i in range(NY):
            out[i, :NY - i] = c[i, i:]
        return out
    P = tri(pays.aq.to_numpy() // 4, pays.tq.to_numpy() // 4, pays.amount.to_numpy())
    R = tri(f.aq.to_numpy() // 4, f.rq.to_numpy() // 4, np.ones(len(f)))
    C = tri(tr.aq.to_numpy() // 4, tr.tq.to_numpy() // 4, tr.d.to_numpy().astype(float))
    last = np.array([NY - 1 - i for i in range(NY)])

    def fac(T):
        return np.array([sum(T[i, j + 1] for i in range(NY) if not np.isnan(T[i, j + 1])) /
                         sum(T[i, j] for i in range(NY) if not np.isnan(T[i, j + 1])) for j in range(NY - 1)])
    lat = np.array([P[i, last[i]] for i in range(NY)])
    if not restated:
        f_ = fac(P)
        return float(sum(lat[i] * np.prod(f_[last[i]:]) for i in range(NY)) - lat.sum())
    n = np.array([R[i, last[i]] for i in range(NY)])
    fr = fac(R)
    n = np.array([n[i] * np.prod(fr[last[i]:]) for i in range(NY)])
    D = C / n[:, None]
    tg = {last[i]: D[i, last[i]] for i in range(NY)}
    Rs = P.copy()
    for i in range(NY):
        xs, ys = np.r_[0.0, D[i, :last[i] + 1]], np.r_[0.0, P[i, :last[i] + 1]]
        for j in range(last[i]):
            k = min(max(int(np.searchsorted(xs, tg[j])), 1), len(xs) - 1)
            x0, x1, y0, y1 = xs[k - 1], xs[k], ys[k - 1], ys[k]
            w = (tg[j] - x0) / (x1 - x0) if x1 > x0 else 1.0
            Rs[i, j] = y0 + (y1 - y0) * w if (interp == "linear" or y0 <= 0) else y0 * (y1 / y0) ** w
    f_ = fac(Rs)
    return float(sum(lat[i] * np.prod(f_[last[i]:]) for i in range(NY)) - lat.sum())


def round_to(x, unit):
    return int(np.floor(x / unit + 0.5) * unit)


# ------------------------------------------------------------------ Ask A: claimant features by accident year

def feature_payments(b, upto=NQ):
    """Net loss paid per claimant feature through the end of calendar quarter `upto` - 1, both ledgers, a converted
    or re-entered feature's legacy payments included."""
    pays = b["pays"]
    pf = b["pf"]
    key_of = {}
    for fid, ref in zip(pf.feature_id, pf.legacy_ref):
        if ref and ref in b["re_keys"]:
            key_of[fid] = ref                   # a re-entered feature is keyed by its legacy number
        elif ref and ref in b["cv_keys"]:
            key_of[ref] = fid                   # a converted feature is keyed by its platform number
    # a payment issued on a feature opened in error belongs to the claim's one real claimant feature
    lc = b["lc"]
    claim = lc.key.str.rsplit("-", n=1).str[0]
    mates_l = lc[lc.DISP != "XD"].groupby(claim[lc.DISP != "XD"]).key.agg(list)
    for k, cl in zip(lc.key[lc.DISP == "XD"], claim[lc.DISP == "XD"]):
        mates = mates_l.get(cl, [])
        if len(mates) == 1:
            key_of[k] = key_of.get(mates[0], mates[0])
    real = pf[pf.disposition != "DUPLICATE"]
    per_claim = real.groupby("claim_number").feature_id.agg(list)
    for fid, cn in zip(pf.feature_id[pf.disposition == "DUPLICATE"], pf.claim_number[pf.disposition == "DUPLICATE"]):
        mates = per_claim.get(cn, [])
        if len(mates) == 1:
            key_of[fid] = key_of.get(mates[0], mates[0])
    k = pays.fid.map(lambda x: key_of.get(x, x))
    ok = pays.tq < upto
    return pays.amount[ok].groupby(k[ok]).sum()


def counts_by_year(b):
    """For each accident year: claimant features closed at 31 December 2026 with a net loss payment, closed without
    one, and open."""
    f = b["feats"]
    f = f[(f.rq < NQ) & (f.aq >= 0)]
    net = b["trans"][b["trans"].tq < NQ].groupby("key").d.sum()
    closed = f.key.map(net).fillna(0) > 0
    paid = f.key.map(feature_payments(b)).fillna(0.0)
    ay = Y0 + f.aq.to_numpy() // 4
    out = {}
    for y in range(Y0, Y0 + NQ // 4):
        m = ay == y
        out[y] = dict(with_payment=int((m & closed & (paid > 0.005)).sum()),
                      without_payment=int((m & closed & (paid <= 0.005)).sum()),
                      open=int((m & ~closed).sum()))
    return out


# ------------------------------------------------------------------ Ask B: the 2026 ledger by quarter

def wire_value_date(t: pd.Timestamp, cutoff_hour=15) -> dt.date:
    """A wire's bank value date: its release day, or the next business day when released at or after the cutoff."""
    import world as W
    d = t.date()
    if t.hour >= cutoff_hour:
        d = W.next_business(d + dt.timedelta(days=1))
    return d


def ledger_lines(target, cutoff_hour=15):
    """Every 2026 line of account 5311 classified against the platform's payments: a feed batch carries one Central
    day's checks net of that day's voids (the first batch to carry a day's checks; a later batch with the same day's
    checks is a repeat), a Treasury journal carries one month's wires by bank value date, and whatever no payment
    accounts for is not a claims payment."""
    gl = L.ledger(target)
    pp = L.payments(target)
    pf = L.features(target)
    state = dict(zip(pf.feature_id, pf.state))
    pp["state"] = pp.feature_id.map(state)
    chk = pp[pp.method == "CHECK"]
    day_net = {}
    for d, st, a in zip(chk.issued.dt.date, chk.state, chk.amount):
        day_net[(d, st)] = day_net.get((d, st), 0.0) + a
    vv = chk[chk.voided.notna()]
    for d, st, a in zip(vv.voided.dt.date, vv.state, vv.amount):
        day_net[(d, st)] = day_net.get((d, st), 0.0) - a
    wires = pp[pp.method == "WIRE"].copy()
    wires["vdate"] = [wire_value_date(t, cutoff_hour) for t in wires.issued]
    wires["vm"] = [(d.year, d.month) for d in wires.vdate]
    rows = []
    carried = set()
    carried_st = set()
    for (pdate, ref), g in gl.groupby([gl.date, gl.batch_ref], sort=True):
        src = g.source.iloc[0]
        amts = {st: round(a, 2) for st, a in zip(g.state, g.amount)}
        if src == "CLAIMS FEED":
            day = None
            for k in range(1, 6):
                cand = (pdate - pd.Timedelta(days=k)).date()
                net = {st: round(float(day_net.get((cand, st), 0.0)), 2) for st in amts}
                if all(abs(net[st] - amts[st]) < 0.005 for st in amts):
                    day = cand
                    if cand not in carried:
                        break
            if day is not None and day not in carried:
                carried.add(day)
                for st, a in amts.items():
                    carried_st.add((day, st))
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=a, kind="checks",
                                     issued=day))
            else:
                for st, a in amts.items():
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=a, kind="repeat",
                                     issued=None))
        elif src == "TREASURY":
            prev = (pdate - pd.DateOffset(months=1))
            vm = (prev.year, prev.month)
            for st, a in amts.items():
                w = wires[(wires.vm == vm) & (wires.state == st)]
                for t, amt in zip(w.issued, w.amount):
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=round(amt, 2),
                                     kind="wire", issued=t.date()))
                rest = round(a - float(w.amount.sum()), 2)
                if abs(rest) >= 0.005:
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=rest, kind="unmatched",
                                     issued=None))
        else:
            # a manual line is a claims payment when it books a day's checks for its state that no feed line carried
            for st, a in amts.items():
                day = None
                for k in range(1, 6):
                    cand = (pdate - pd.Timedelta(days=k)).date()
                    if (cand, st) not in carried_st and abs(round(float(day_net.get((cand, st), 0.0)), 2) - a) < 0.005 \
                            and abs(a) > 0.005:
                        day = cand
                        break
                if day is not None:
                    carried_st.add((day, st))
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=a, kind="checks",
                                     issued=day))
                else:
                    rows.append(dict(date=pdate.date(), source=src, ref=ref, state=st, amount=a, kind="journal",
                                     issued=None))
    return pd.DataFrame(rows)


def ledger_quarters(target, cutoff_hour=15):
    """For each quarter of 2026: what account 5311 booked, how much of it was claims payments issued in an earlier
    quarter, and how much was not claims payments at all."""
    x = ledger_lines(target, cutoff_hour)
    out = {}
    for q in range(4):
        lo = dt.date(2026, 3 * q + 1, 1)
        hi = dt.date(2026, 3 * q + 4, 1) if q < 3 else dt.date(2027, 1, 1)
        g = x[(x.date >= lo) & (x.date < hi)]
        pay = g.kind.isin(["checks", "wire"])
        earlier = g[pay & (g.issued.map(lambda d: d is not None and d < lo))].amount.sum()
        other = g[~pay].amount.sum()
        out[q + 1] = dict(booked=round(float(g.amount.sum()), 2), earlier=round(float(earlier), 2),
                          other=round(float(other), 2))
    return out
