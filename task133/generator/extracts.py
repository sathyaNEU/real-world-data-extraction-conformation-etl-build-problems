"""System extracts and model-team files, all read off the simulated book: the loan book at close of business on the
reporting date, the hardship register, the PD curve and its development sample, write-offs and recoveries, and the
month-end arrears roll rates."""
import datetime as dt

import numpy as np
import pandas as pd

import sim as SM
import world as W

BUCKETS = ["Current", "1-29", "30-59", "60-89", "90+"]


def bucket(d):
    return np.select([d == 0, d < 30, d < 60, d < 90], [0, 1, 2, 3], 4)


def mob_at(S, rows, t):
    """repayments fallen due on or before day t"""
    T = S.T[rows]
    due = S.due[rows]
    k = np.arange(SM.J)[None, :] < T[:, None]
    return ((due <= t) & k).sum(1)


def book(S, rng):
    """every loan open in the loan system at close of business on the reporting date, after the month-end write-off
    batch, with its behaviour score that night"""
    R = S.R
    L = S.L
    rows = np.nonzero(SM.open_at(S, R))[0]
    n = len(rows)
    dpd = SM.dpd_at(S, R, rows)
    bal = SM.balances(S, rows, np.full(n, R))
    a = mob_at(S, rows, R)
    # behaviour score: the application score's drift since origination plus what the bureau and the account show now
    s0 = L["score_v3"][rows]
    drift = rng.normal(0.3 * np.minimum(a, 24), 10 + 3.0 * np.sqrt(a))
    ev = np.select([dpd == 0, dpd < 30, dpd < 60, dpd < 90], [0.0, -12.0, -45.0, -60.0], -80.0) + np.where(dpd > 0, rng.normal(0, 8, n), 0)
    pos = {int(r): k for k, r in enumerate(rows)}
    hs_now = np.zeros(n)
    for x in S.arr:
        k = pos.get(x["loan"])
        if k is None or x["received"] > R:
            continue
        cancelled = x["cancel"] is not None and x["cancel"] < R
        if x["start"] <= R <= x["end"] and not cancelled:
            hs_now[k] = min(hs_now[k], rng.normal(-22, 12))
        elif cancelled and x["outcome"] == "failed" and R - x["cancel"] < 365:
            hs_now[k] = min(hs_now[k], rng.normal(-25, 12))
        elif x["end"] < R and R - x["end"] < 365 and x["outcome"] != "withdrawn":
            hs_now[k] = min(hs_now[k], rng.normal(-14, 10))
    onset = np.where(S.j0[rows] > 0, S.due[rows, np.maximum(S.j0[rows] - 1, 0)], SM.BIG)
    pre = (onset > R) & (onset <= R + 183) & (rng.random(n) < 0.55)
    ev += np.where(pre, rng.normal(-45, 18, n), 0)
    ev += np.where(S.cured[rows], rng.normal(-40, 15, n), 0)
    recent = ((S.clear[rows] > S.due[rows]) & (S.due[rows] > R - 183) & (S.due[rows] <= R) & (S.clear[rows] < SM.BIG)
              & (S.susp[rows] <= R)).sum(1)
    ev += -9.0 * recent
    ev += np.where(rng.random(n) < 0.045, rng.normal(-65, 22, n), 0)
    latent = s0 + drift + ev + hs_now
    sa, sb = W.SCORE_MAP
    raw = sa * latent + sb + rng.normal(0, 5, n)
    raw = np.where(raw > 880, 880 + 60 * np.tanh((raw - 880) / 60), raw)    # the points scale flattens at the top
    cur = np.rint(raw).astype(int)
    # until the first repayment has fallen due the behaviour score is the origination score, on v4
    o4 = np.where(L["v4"][rows], L["orig_score"][rows], np.floor(sa * L["orig_score"][rows] + sb + 0.5)).astype(int)
    cur = np.where(a == 0, o4, cur)
    first = np.array([SM.dd(x) for x in S.nom[rows, 0]])
    bk = pd.DataFrame(dict(
        loan_no=L["loan_no"][rows],
        product=np.where(L["pl60"][rows], "PL60", "PL36"),
        risk_grade=np.array(W.GRADES)[L["grade"][rows]],
        drawdown_date=[SM.dd(x).isoformat() for x in L["draw"][rows]],
        first_repayment_date=[d.isoformat() for d in first],
        term_months=S.T[rows],
        contract_rate=["%.4f" % x for x in L["rate"][rows]],
        original_amount=L["financed"][rows],
        current_balance=["%.2f" % x for x in np.round(bal, 2)],
        days_past_due=dpd,
        origination_score=L["orig_score"][rows],
        origination_scorecard=np.where(L["v4"][rows], "v4", "v3"),
        current_score_v4=cur,
        state=np.array(W.STATES)[L["state"][rows]],
        channel=np.array(W.CHANNELS)[L["channel"][rows]],
    ))
    bk["loan_key"] = rows + 1
    bk["_bal"] = np.round(bal, 2)
    bk = bk.sort_values("loan_no", kind="stable").reset_index(drop=True)
    return bk


def hardship(S, rng):
    """the hardship register: every arrangement recorded since go-live, one row per arrangement, case numbers in the
    order requests were received (requests declined at assessment take a number and do not appear)"""
    R = S.R
    L = S.L
    rows = []
    for x in S.arr:
        if x["received"] > R or x["received"] >= S.close[x["loan"]]:
            continue
        x = dict(x)
        shut = int(S.close[x["loan"]])
        if shut <= R and x["end"] > shut and not (x["cancel"] is not None and x["cancel"] <= shut):
            if shut <= x["start"]:
                continue                        # repaid before the varied repayments began: the request lapsed
            # the loan was repaid while the arrangement ran: it ends with the loan
            x["end"], x["cancel"], x["outcome"] = min(shut, R - 1), None, "complete"
        if x["outcome"] == "withdrawn":
            if x["cancel"] < R:
                status, cancel = "Cancelled", x["cancel"]
            else:
                status, cancel = "Approved", None
        elif x["outcome"] == "failed":
            if x["cancel"] < R:
                status, cancel = "Cancelled", x["cancel"]
            elif x["start"] > R:
                status, cancel = "Approved", None
            else:
                status, cancel = "Active", None
        else:
            status = "Approved" if x["start"] > R else ("Active" if x["end"] >= R else "Completed")
            cancel = None
        rows.append((x["received"], L["loan_no"][x["loan"]], x["reason"], x["kind"], x["start"], x["end"],
                     x["reduced"], status, cancel))
    rows.sort(key=lambda r: (r[0], r[1]))
    seq = 10230 + np.cumsum(1 + rng.poisson(0.22, len(rows)))
    out = pd.DataFrame(dict(
        case_ref=["HS-%06d" % q for q in seq],
        loan_no=[r[1] for r in rows],
        received_date=[SM.dd(r[0]) for r in rows],
        hardship_reason=[r[2] for r in rows],
        arrangement_type=[r[3] for r in rows],
        arrangement_start=[SM.dd(r[4]) for r in rows],
        arrangement_end=[SM.dd(r[5]) for r in rows],
        agreed_repayment_aud=[(r[6] if r[3] == "Reduced repayments" else 0.0) for r in rows],
        arrangement_status=[r[7] for r in rows],
        cancelled_date=[SM.dd(r[8]) if r[8] is not None else None for r in rows],
    ))
    return out


def curve(S):
    """the model team's cumulative default curve by month on book: the expected share of a new loan's cohort that
    has reached 90 days past due at a month end by each month on book, over the development loans' own repayment
    calendars, all grades pooled at the development mix, payouts not counted as an exit"""
    cal = S.cal
    dev = S.L["draw"] < SM.dn(W.DEV_CUTOFF)
    out = {}
    for p, T in W.PRODUCTS.items():
        rows = np.nonzero(dev & (S.L["pl60"] == (p == "PL60")))[0]
        h = S.haz[rows, :T]
        surv = np.exp(-np.cumsum(-np.log1p(-h), 1))
        before = np.hstack([np.ones((len(rows), 1)), surv[:, :-1]])
        pj = h * before
        due = S.due[rows, :T]
        e = cal.me[cal.mi_of[due + 90]]
        m = np.zeros_like(due)
        for k in range(T):
            m += due[:, k:k + 1] <= e
        C = np.zeros(T + 1)
        for mm in range(1, T + 1):
            C[mm] = (pj * (m <= mm)).sum(1).mean()
        out[p] = np.round(C, 6)
    return out


def development_sample(S):
    """loans drawn October 2019 to September 2023 and what had become of each by 31 May 2026"""
    obs = SM.dn(W.DEV_OBS_END)
    L = S.L
    rows = np.nonzero(L["draw"] < SM.dn(W.DEV_CUTOFF))[0]
    T = S.T[rows]
    due = S.due[rows]
    inside = np.arange(SM.J)[None, :] < T[:, None]
    close, ct = S.close[rows], S.close_type[rows]
    dflt = S.e_def[rows] <= obs
    mob_close = ((due <= close[:, None]) & inside).sum(1)
    mob_obs = ((due <= obs) & inside).sum(1)
    shut = (close <= obs) & ~dflt
    mat = shut & (ct == 2) & (mob_close >= T)
    pre = shut & ((ct == 1) | ((ct == 2) & (mob_close < T)))
    outcome = np.select([dflt, pre, mat], ["default", "prepaid", "matured"], "open")
    month = np.select([dflt, pre, mat], [S.m_def[rows], mob_close, T], mob_obs)
    return pd.DataFrame(dict(
        loan_key=(rows + 1).astype(np.int64),
        product=np.where(L["pl60"][rows], "PL60", "PL36"),
        risk_grade=np.array(W.GRADES)[L["grade"][rows]],
        drawdown_month=[SM.dd(x).strftime("%Y-%m") for x in L["draw"][rows]],
        term_months=T.astype(np.int64),
        outcome=outcome,
        outcome_month_on_book=month.astype(np.int64),
    ))


def recoveries(S, rng):
    """what each written-off loan pays after write-off, through the R + 3 year horizon: a payment plan with the
    collection agency (monthly amounts, some months missed, until the plan lapses or the debt is cleared), a lump-sum
    settlement, a few odd payments, or nothing. Returns the written-off loans, their balances and the flows."""
    cal, R = S.cal, S.R
    wo = np.nonzero((S.close_type == 3) & (S.close <= R))[0]
    bal = SM.balances(S, wo, S.close[wo])
    plan, settle, odd = W.RECOVERY_MIX
    lo, hi, floor, cap, stop = W.RECOVERY_PLAN
    s_lo, s_hi = W.RECOVERY_SETTLE
    flows = []                                   # (position in wo, day, amount)
    for k, i in enumerate(wo):
        b = float(bal[k])
        w = int(S.close[i])
        u = rng.random()
        if u < plan:
            m = float(np.clip(np.round(b * rng.uniform(lo, hi) / 5) * 5, floor, cap))
            d = w + int(rng.integers(25, 160))
            total = 0.0
            for _ in range(48):
                if rng.random() >= 0.13:         # a month missed now and then
                    a = min(m, round(b - total, 2))
                    flows.append((k, int(cal.next_bd[d]), a))
                    total += a
                if b - total < 1 or rng.random() < stop:
                    break
                d = SM.add_months(d, 1)
        elif u < plan + settle:
            d = w + int(rng.integers(45, 760))
            flows.append((k, int(cal.next_bd[d]), float(np.round(b * rng.uniform(s_lo, s_hi) / 50) * 50)))
        elif u < plan + settle + odd:
            for _ in range(int(rng.integers(1, 5))):
                flows.append((k, int(cal.next_bd[w + int(rng.integers(30, 900))]),
                              float(rng.choice([20, 25, 30, 40, 50, 50, 75, 100, 100, 150, 200]))))
    return wo, bal, flows


def write_offs(S, rng):
    """loans written off in each month-end batch, July 2025 to September 2026, the balance written off, and
    recoveries received in the month on loans written off in any earlier month"""
    wo, bal, flows = recoveries(S, rng)
    fl = pd.DataFrame(flows, columns=["k", "d", "amt"])
    fl = fl[fl["d"] <= S.R]
    fl["m"] = [SM.dd(x).strftime("%Y-%m") for x in fl["d"]]
    wm = pd.Series([SM.dd(x).strftime("%Y-%m") for x in S.close[wo]])
    rows = []
    for per in pd.period_range("2025-07", "2026-09", freq="M"):
        m = str(per)
        sel = (wm == m).values
        rows.append(dict(month=m, loans_written_off=int(sel.sum()), gross_write_off_aud="%.2f" % round(float(bal[sel].sum()), 2),
                         recoveries_aud="%.2f" % round(float(fl.loc[fl["m"] == m, "amt"].sum()), 2)))
    return pd.DataFrame(rows)


def roll_rates(S):
    """month-end roll rates between arrears buckets, July 2025 to June 2026, by loan count"""
    cal = S.cal
    out = []
    k0 = int(cal.mi_of[SM.dn(dt.date(2025, 6, 30))])
    for k in range(k0 + 1, k0 + 13):
        t0, t1 = int(cal.me[k - 1]), int(cal.me[k])
        o0 = SM.open_at(S, t0)
        rows = np.nonzero(o0)[0]
        b0 = bucket(SM.dpd_at(S, t0, rows))
        still = S.close[rows] > t1
        b1 = np.where(still, bucket(SM.dpd_at(S, t1, rows)), -1)

        def rr(x, y):
            return float(((b0 == x) & (b1 == y)).sum()) / float((b0 == x).sum())
        out.append((SM.dd(t1), rr(0, 1), rr(1, 2), rr(2, 3), rr(3, 4), rr(1, 0)))
    return out
