"""System extracts, all read off the simulated book: the loan book at close of business on the reporting date, the loan
record, the hardship register, the June extract, the month-end scoring runs, write-offs and recoveries, the Collections
files, and the month-end arrears roll rates."""
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


def away_flags(S):
    """borrowers whose residential address on file is overseas: drawn for the September book's loans in book order (as the
    extract always has), and from their own stream for loans closed before then"""
    rows = np.nonzero(SM.open_at(S, S.R))[0]
    out = np.random.default_rng(W.SEED + 48).random(S.N) < W.OVERSEAS_ADDRESS
    out[rows] = np.random.default_rng(W.SEED + 8).random(len(rows)) < W.OVERSEAS_ADDRESS
    return out


def dpd_at_run(S, t, rows):
    """days past due as a job running early on day t + 1 reads them: the repayments made good by close of business on
    day t, counted to the run date, so a loan in arrears shows one day more than at close of business on day t (and a
    repayment due on day t and still unpaid shows one day)"""
    rows = np.asarray(rows)
    c = S.clear[rows]
    unpaid = (c > t) & (S.susp[rows] <= t)
    jstar = unpaid.argmax(1)
    d = S.due[rows, jstar]
    return np.where(unpaid.any(1) & (d <= t), t + 1 - d, 0)


def frame_at(S, t, score=None, arrears_at_run=False):
    """every loan open in the loan system at close of business on day t (after that day's month-end write-off batch), one
    row per loan, sorted by loan number, with the behaviour score column only when one is given; arrears_at_run gives
    days past due as the job read them before CHG-26-0418, at its 07:30 run the next morning"""
    L = S.L
    rows = np.nonzero(SM.open_at(S, t))[0]
    n = len(rows)
    dpd = dpd_at_run(S, t, rows) if arrears_at_run else SM.dpd_at(S, t, rows)
    bal = SM.balances(S, rows, np.full(n, t))
    first = np.array([SM.dd(x) for x in S.nom[rows, 0]])
    cols = dict(
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
    )
    if score is not None:
        cols["current_score_v4"] = score
    cols["state"] = np.array(W.STATES)[L["state"][rows]]
    cols["channel"] = np.array(W.CHANNELS)[L["channel"][rows]]
    bk = pd.DataFrame(cols)
    bk.loc[S.away[rows], "state"] = None
    bk["loan_key"] = rows + 1
    bk["_bal"] = np.round(bal, 2)
    bk["_dpd"] = dpd
    return bk.sort_values("loan_no", kind="stable").reset_index(drop=True)


def book(S, rng):
    """every loan open in the loan system at close of business on the reporting date, after the month-end write-off
    batch, with its behaviour score from the September month-end run. The score's parts are kept on S.score_parts, so the
    earlier month-end runs can be read off the same path"""
    R = S.R
    L = S.L
    rows = np.nonzero(SM.open_at(S, R))[0]
    n = len(rows)
    dpd = SM.dpd_at(S, R, rows)
    a = mob_at(S, rows, R)
    # behaviour score: the application score's drift since origination plus what the bureau and the account show now
    s0 = L["score_v3"][rows]
    drift = rng.normal(0.3 * np.minimum(a, 24), 10 + 3.0 * np.sqrt(a))
    e8 = rng.normal(0, 8, n)
    ev = np.select([dpd == 0, dpd < 30, dpd < 60, dpd < 90], [0.0, -12.0, -45.0, -60.0], -80.0) + np.where(dpd > 0, e8, 0)
    pos = {int(r): k for k, r in enumerate(rows)}
    hs_now = np.zeros(n)
    hs = {}
    for idx, x in enumerate(S.arr):
        k = pos.get(x["loan"])
        if k is None or x["received"] > R:
            continue
        cancelled = x["cancel"] is not None and x["cancel"] < R
        if x["start"] <= R <= x["end"] and not cancelled:
            hs[idx] = ("in", rng.normal(-22, 12))
        elif cancelled and x["outcome"] == "failed" and R - x["cancel"] < 365:
            hs[idx] = ("failed", rng.normal(-25, 12))
        elif x["end"] < R and R - x["end"] < 365 and x["outcome"] != "withdrawn":
            hs[idx] = ("ended", rng.normal(-14, 10))
        else:
            continue
        hs_now[k] = min(hs_now[k], hs[idx][1])
    onset = np.where(S.j0[rows] > 0, S.due[rows, np.maximum(S.j0[rows] - 1, 0)], SM.BIG)
    u_pre = rng.random(n)
    pre = (onset > R) & (onset <= R + 183) & (u_pre < 0.55)
    m_pre = rng.normal(-45, 18, n)
    ev += np.where(pre, m_pre, 0)
    m_cure = rng.normal(-40, 15, n)
    ev += np.where(S.cured[rows], m_cure, 0)
    recent = ((S.clear[rows] > S.due[rows]) & (S.due[rows] > R - 183) & (S.due[rows] <= R) & (S.clear[rows] < SM.BIG)
              & (S.susp[rows] <= R)).sum(1)
    ev += -9.0 * recent
    u_shock = rng.random(n)
    m_shock = rng.normal(-65, 22, n)
    ev += np.where(u_shock < 0.045, m_shock, 0)
    latent = s0 + drift + ev + hs_now
    sa, sb = W.SCORE_MAP
    e5 = rng.normal(0, 5, n)
    raw = sa * latent + sb + e5
    raw = np.where(raw > 880, 880 + 60 * np.tanh((raw - 880) / 60), raw)    # the points scale flattens at the top
    cur = np.rint(raw).astype(int)
    # until the first repayment has fallen due the behaviour score is the origination score, on v4
    o4 = np.where(L["v4"][rows], L["orig_score"][rows], np.floor(sa * L["orig_score"][rows] + sb + 0.5)).astype(int)
    cur = np.where(a == 0, o4, cur)
    S.score_parts = dict(rows=rows, a=a, D=drift - 0.3 * np.minimum(a, 24), e8=e8, hs=hs, u_pre=u_pre, m_pre=m_pre,
                         m_cure=m_cure, u_shock=u_shock, m_shock=m_shock, cur=cur)
    S.away = away_flags(S)
    return frame_at(S, R, score=cur)


def _var(a):
    return (10 + 3.0 * np.sqrt(a)) ** 2


def score_runs(S, ends):
    """the month-end behaviour scoring runs for the month ends in `ends` (each before the reporting date): every loan open
    at close of business that day whose first repayment has fallen due, scored on that night's position. The path runs
    back from the September run in the book extract: the drift since origination is a random walk on the variance clock
    of the September draw, read back as a bridge; arrears, hardship arrangements, the months before a default, cures,
    recent late repayments and bureau events enter as they stand at each month end, with the September draws reused for
    the same event and fresh draws (their own stream) for an event the September run did not see"""
    P = S.score_parts
    L = S.L
    N = getattr(S, "N_own", S.N)                # the runs score loans open in 2026: the loan system's own loans
    rng = np.random.default_rng(W.SEED + 41)
    sa, sb = W.SCORE_MAP
    rows_R = P["rows"]
    e8 = rng.normal(0, 8, N)
    u_pre = rng.random(N)
    m_pre = rng.normal(-45, 18, N)
    m_cure = rng.normal(-40, 15, N)
    u_shock = rng.random(N)
    m_shock = rng.normal(-65, 22, N)
    e8[rows_R], u_pre[rows_R], m_pre[rows_R] = P["e8"], P["u_pre"], P["m_pre"]
    m_cure[rows_R], u_shock[rows_R], m_shock[rows_R] = P["m_cure"], P["u_shock"], P["m_shock"]
    # a bureau event weighs on the score for a year: the September run's events began in the year before it, and loans
    # without one may have carried an earlier event that had lapsed by September
    shock_day = S.R - rng.integers(0, 731, N)
    u_old = rng.random(N)
    on_R = np.zeros(N, bool)
    on_R[rows_R] = P["u_shock"] < 0.045
    shock_day[rows_R] = np.where(on_R[rows_R], S.R - rng.integers(0, 365, len(rows_R)), shock_day[rows_R] - 365)
    u_shock = np.where(on_R, 0.0, np.where(np.isin(np.arange(N), rows_R), np.where(u_old < 0.047, 0.0, 1.0),
                                           np.where(u_old < 0.09, 0.0, 1.0)))
    onset = np.where(S.j0[:N] > 0, S.due[np.arange(N), np.maximum(S.j0[:N] - 1, 0)], SM.BIG)
    D = np.full(N, np.nan)
    aD = np.full(N, -1)
    D[rows_R], aD[rows_R] = P["D"], P["a"]
    hs_cache = {(idx, kind): val for idx, (kind, val) in P["hs"].items()}
    out = {}
    for t in sorted(ends, reverse=True):
        rows = np.nonzero(SM.open_at(S, t))[0]
        assert (rows < N).all(), "a loan taken over at the go-live is still open in 2026"
        a = mob_at(S, rows, t)
        rows, a = rows[a >= 1], a[a >= 1]
        n = len(rows)
        z = rng.standard_normal(N)[rows]
        v_t = _var(a)
        known = aD[rows] >= 0
        prev_a = np.where(known, aD[rows], a)
        v_p = _var(prev_a)
        shrink = np.where(known & (prev_a > a), v_t / v_p, 1.0)
        sd = np.sqrt(np.where(known, v_t * (1 - shrink), v_t))
        Dt = np.where(known, np.nan_to_num(D[rows]) * shrink, 0.0) + sd * z
        D[rows], aD[rows] = Dt, a
        dpd = SM.dpd_at(S, t, rows)
        ev = np.select([dpd == 0, dpd < 30, dpd < 60, dpd < 90], [0.0, -12.0, -45.0, -60.0], -80.0) + np.where(dpd > 0, e8[rows], 0)
        ev += np.where((onset[rows] > t) & (onset[rows] <= t + 183) & (u_pre[rows] < 0.55), m_pre[rows], 0)
        ev += np.where(S.cured[rows] & (S.res_day[rows] <= t), m_cure[rows], 0)
        recent = ((S.clear[rows] > S.due[rows]) & (S.due[rows] > t - 183) & (S.due[rows] <= t) & (S.clear[rows] < SM.BIG)
                  & (S.susp[rows] <= t)).sum(1)
        ev += -9.0 * recent
        ev += np.where((u_shock[rows] < 0.045) & (shock_day[rows] <= t) & (t < shock_day[rows] + 365), m_shock[rows], 0)
        pos = {int(r): k for k, r in enumerate(rows)}
        hs_t = np.zeros(n)
        for idx, x in enumerate(S.arr):
            k = pos.get(x["loan"])
            if k is None or x["received"] > t:
                continue
            cancelled = x["cancel"] is not None and x["cancel"] <= t
            if x["start"] <= t <= x["end"] and not cancelled:
                kind, mu, sdv = "in", -22, 12
            elif cancelled and x["outcome"] == "failed" and t - x["cancel"] < 365:
                kind, mu, sdv = "failed", -25, 12
            elif x["end"] < t and t - x["end"] < 365 and x["outcome"] != "withdrawn":
                kind, mu, sdv = "ended", -14, 10
            else:
                continue
            if (idx, kind) not in hs_cache:
                hs_cache[(idx, kind)] = rng.normal(mu, sdv)
            hs_t[k] = min(hs_t[k], hs_cache[(idx, kind)])
        latent = L["score_v3"][rows] + 0.3 * np.minimum(a, 24) + Dt + ev + hs_t
        raw = sa * latent + sb + rng.normal(0, 5, N)[rows]
        raw = np.where(raw > 880, 880 + 60 * np.tanh((raw - 880) / 60), raw)
        out[t] = (rows, np.rint(raw).astype(int))
    return out


def hardship(S, rng):
    """the hardship register: every arrangement recorded since go-live, one row per arrangement, case numbers in the
    order requests were received (requests declined at assessment take a number and do not appear)"""
    R = S.R
    L = S.L
    # arrangement_status as the 1 October extract shows it: Completed only once the weekly batch (Tuesday nights) has run
    # after the end date, so an arrangement that ended since the last run still shows Active
    last_run = SM.dn(W.REPORT) - (W.REPORT.weekday() - W.STATUS_RUN_WEEKDAY) % 7
    rows = []
    live = SM.dn(W.GO_LIVE)
    for x in S.arr:
        if x["received"] > R or x["received"] >= S.close[x["loan"]] or x["received"] < live:
            continue                            # the register starts at the go-live: earlier requests stayed behind
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
        elif x["reason"] == "COVID-19":
            # the 2020 deferrals and the 2021 lockdown pauses were loaded in bulk outside the hardship workflow, so the
            # weekly batch never moved them on: they still read Active (every one sits on a loan closed before 2026)
            status, cancel = "Active", None
        else:
            status = "Approved" if x["start"] > R else ("Active" if x["end"] >= last_run else "Completed")
            cancel = None
        rows.append((x["received"], L["loan_no"][x["loan"]], x["reason"], x["kind"], x["start"], x["end"],
                     x["reduced"], status, cancel))
    rows.sort(key=lambda r: (r[0], r[1]))
    seq = 10230 + np.cumsum(1 + rng.poisson(0.22, len(rows)))
    # the reason was optional before it became a required field; a few early cases were saved without one
    gap = np.random.default_rng(W.SEED + 9)
    rows = [r[:2] + ((None if (SM.dd(r[0]) < W.REASON_REQUIRED and r[2] != "COVID-19" and gap.random() < W.REASON_MISSING)
                      else r[2]),) + r[3:] for r in rows]
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


def loan_record(S):
    """the loan system's record of every loan it has held, one row per loan, as at close of business on the reporting
    date: its own loans from the go-live and the earlier platform's loans it took over that day. The default month is the
    first month end at which the loan system saw the loan 90 or more days past due (so never before the go-live), and a
    closed loan carries the day it closed and how: repaid in full (by its final repayment or ahead of its term),
    settled for less than it owed, or written off"""
    L, R = S.L, S.R
    rows = np.arange(S.N)
    dme = collections(S)["dme"]
    closed = S.close <= R
    reason = np.select([S.close_type == 3, S.close_type == 4], ["Written off", "Settled"], "Repaid in full")
    first = np.array([SM.dd(x) for x in S.nom[rows, 0]])
    df = pd.DataFrame(dict(
        loan_no=L["loan_no"],
        product=np.where(L["pl60"], "PL60", "PL36"),
        risk_grade=np.array(W.GRADES)[L["grade"]],
        drawdown_date=[SM.dd(x) for x in L["draw"]],
        first_repayment_date=first,
        term_months=S.T.astype(np.int64),
        contract_rate=np.round(L["rate"], 4),
        original_amount=L["financed"].astype(np.int64),
        default_month=[SM.dd(x).strftime("%Y-%m") if x < SM.BIG else None for x in dme],
        status=np.where(closed, "Closed", "Open"),
        closed_date=[SM.dd(x) if c else None for x, c in zip(S.close, closed)],
        closure_reason=np.where(closed, reason, None),
    ))
    df["_i"] = rows
    return df.sort_values("loan_no", kind="stable").reset_index(drop=True)


def recoveries(S, rng):
    """what each written-off loan pays after write-off, through the R + 3 year horizon: a payment plan with the
    collection agency (monthly amounts, some months missed, until the plan lapses or the debt is cleared), a lump-sum
    settlement, a few odd payments, or nothing. Returns the written-off loans, their balances and the flows."""
    cal, R = S.cal, S.R
    wo = np.nonzero((S.close_type == 3) & (S.close <= R))[0]
    bal = SM.balances(S, wo, S.close[wo])
    plan, settle, odd = W.RECOVERY_MIX
    lo, hi, floor, afford, stop = W.RECOVERY_PLAN
    s_lo, s_hi = W.RECOVERY_SETTLE
    flows = []                                   # (position in wo, day, amount, kind)
    for k, i in enumerate(wo):
        b = float(bal[k])
        w = int(S.close[i])
        u = rng.random()
        if u < plan:
            m = float(max(floor, np.round(min(b * rng.uniform(lo, hi), np.exp(rng.normal(np.log(afford), 0.55))) / 5) * 5))
            d = w + int(rng.integers(25, 160))
            total = 0.0
            for _ in range(48):
                if rng.random() >= 0.13:         # a month missed now and then
                    a = min(m, round(b - total, 2))
                    flows.append((k, int(cal.next_bd[d]), a, "plan"))
                    total += a
                if b - total < 1 or rng.random() < stop:
                    break
                d = SM.add_months(d, 1)
        elif u < plan + settle:
            d = w + int(rng.integers(45, 760))
            flows.append((k, int(cal.next_bd[d]), float(np.round(b * rng.uniform(s_lo, s_hi) / 50) * 50), "settle"))
        elif u < plan + settle + odd:
            for _ in range(int(rng.integers(1, 5))):
                flows.append((k, int(cal.next_bd[w + int(rng.integers(30, 900))]),
                              float(rng.choice([20, 25, 30, 40, 50, 50, 75, 100, 100, 150, 200])), "odd"))
    return wo, bal, flows


def placements(S, wo, wbal, flows_by, sold):
    """Wirraway's placements: Bellbird places every written-off account with the agency a few business days after the
    write-off. The placement closes when the plan clears the debt (paid in full), when the borrower settles with
    Bellbird (settled), when the agency hands it back once nothing more is coming (returned: about six months after the
    last remittance, or about a year after placement if nothing came), or when Bellbird recalls it for the March 2026
    sale (recalled at the cut-off); open otherwise. Each placement takes the agency's next reference, except that from
    its platform move the agency reissues, to some new placements, the reference of a placement it closed at least
    AGENCY_REISSUE_GAP days earlier, the most recently freed first. Returns the placements in the order made and, for
    each reference, the loan of the first placement that carried it (where the receipts loader posts its remittances)"""
    cal, R = S.cal, S.R
    rng = np.random.default_rng(W.AGENCY_SEED)
    cut = SM.dn(W.SALE_CUTOFF)
    rows = []
    for k, i in enumerate(wo):
        i = int(i)
        w = int(S.close[i])
        placed = int(cal.next_bd[w + int(rng.integers(5, 21))])
        fl = flows_by.get(i, [])
        plan = [(d, a) for d, a, kind in fl if kind == "plan"]
        settle = [d for d, a, kind in fl if kind == "settle"]
        if plan:
            last = max(d for d, a in plan)
            if sum(a for d, a in plan) >= float(wbal[k]) - 1:
                closed, why = int(cal.next_bd[last + int(rng.integers(3, 11))]), "Paid in full"
            else:
                closed, why = int(cal.next_bd[last + int(rng.integers(150, 211))]), "Returned"
        elif settle:
            closed, why = int(settle[0]), "Settled"
        else:
            closed, why = int(cal.next_bd[placed + int(rng.integers(330, 401))]), "Returned"
        if i in sold and placed <= cut < closed:
            closed, why = cut, "Recalled"
        if placed > R:
            continue
        rows.append([placed, i, closed if closed <= R else SM.BIG, why if closed <= R else "", float(wbal[k])])
    rows.sort(key=lambda r: (r[0], S.L["loan_no"][r[1]]))
    start = SM.dn(W.AGENCY_REISSUE_FROM)
    nxt = W.AGENCY_REF_START
    cur = {}                                     # each reference: the closing day of the placement now carrying it
    first = {}
    for r in rows:
        t = r[0]
        ref = None
        if t >= start and rng.random() < W.AGENCY_REISSUE:
            free = [(c, x) for x, c in cur.items() if c <= t - W.AGENCY_REISSUE_GAP]
            if free:
                ref = max(free)[1]
        if ref is None:
            nxt += 1 + int(rng.poisson(0.35))
            ref = nxt
        r.append(ref)
        first.setdefault(ref, r[1])
        cur[ref] = r[2]
    pl = pd.DataFrame(rows, columns=["placed", "i", "closed", "why", "bal", "ref"])
    return pl, first


def month_end_defaults(S):
    """the first month end at which each loan stood 90 or more days past due while open: the month Collections records
    the default in (CRM-ECL-04 1.2). A loan made good inside the month it reached 90 days is not a default"""
    cal, R = S.cal, S.R
    cand = np.nonzero(S.j0 > 0)[0]
    first = np.full(S.N, SM.BIG, np.int64)
    for k in range(int(cal.mi_of[SM.dn(W.GO_LIVE)]), int(cal.mi_of[R]) + 1):
        t = int(cal.me[k])
        rows = cand[(first[cand] == SM.BIG) & (S.L["draw"][cand] <= t) & (S.close[cand] > t)]
        if len(rows):
            first[rows[SM.dpd_at(S, t, rows) >= 90]] = t
    return first


def collections(S):
    """Collections' records, all read off the simulated book: every default from its month end on, how each was
    resolved (caught up, put on a collections hardship arrangement, settled for less, or written off), every amount
    received on a loan in collections, the March 2026 sale of written-off accounts, and the dishonoured direct debits
    that were taken again. Cached on S."""
    if getattr(S, "_coll", None) is not None:
        return S._coll
    cal, R, L = S.cal, S.R, S.L
    dme = month_end_defaults(S)
    rng = np.random.default_rng(W.SEED + 31)
    wo, wbal, flows = recoveries(S, np.random.default_rng(W.SEED + 3))
    wpos = {int(i): k for k, i in enumerate(wo)}
    flows_by = {}
    for k, d, a, kind in flows:
        flows_by.setdefault(int(wo[k]), []).append((int(d), float(a), kind))
    extras_by = {}
    for l, x, a in S.extras:
        if S.j0[l] > 0:
            extras_by.setdefault(int(l), []).append((int(x), float(a)))
    cut, settled = SM.dn(W.SALE_CUTOFF), SM.dn(W.SALE_SETTLED)
    # the sale: written off by the end of August 2025, not settled, nothing received in the six months to the cut-off
    sold = {}
    for i in wo:
        i = int(i)
        if S.close[i] > SM.dn(W.SALE_WRITTEN_OFF_BY):
            continue
        fl = flows_by.get(i, [])
        if any(kind == "settle" and d <= cut for d, a, kind in fl):
            continue
        if any(cut - W.SALE_QUIET_DAYS < d <= cut for d, a, kind in fl):
            continue
        face = round(float(wbal[wpos[i]]) - sum(a for d, a, kind in fl if d <= cut), 2)
        if face >= 1:
            sold[i] = face
    price = W.SALE_PRICE_CENTS / 100.0
    consideration = round(sum(sold.values()) * price, 2)
    pl, first = placements(S, wo, wbal, flows_by, sold)
    ref_of = dict(zip(pl["i"].tolist(), pl["ref"].tolist()))
    rec = []                                     # (day, loan or -1, amount, source, narrative, loan posted to)

    def pay_source(mix):
        u = rng.random()
        return "Direct debit" if u < mix[0] else ("BPAY" if u < mix[0] + mix[1] else "Card")

    rows = np.nonzero(dme < SM.BIG)[0]
    for i in rows:
        i = int(i)
        t0 = int(dme[i])
        kind, rday = int(S.res_kind[i]), int(S.res_day[i])
        if kind and rday <= t0:
            kind, rday = 0, SM.BIG
        stop = min(rday, R)
        for x, a in extras_by.get(i, []):
            if t0 < x <= stop and not (kind in (3, 4) and x >= rday):
                rec.append((x, i, a, pay_source(W.PART_PAY_MIX), "", i))
        if kind == 1:
            j0, T = int(S.j0[i]), int(S.T[i])
            caught = (S.clear[i, :T] == rday) & (np.arange(T) >= j0 - 1) & (S.cash[i, :T] > 0)
            rec.append((rday, i, round(float(S.cash[i, :T][caught].sum()), 2), pay_source(W.CATCH_UP_MIX), "", i))
        elif kind == 4:
            b = float(SM.balances(S, [i], [rday])[0])
            rec.append((rday, i, float(np.round(b * rng.uniform(*W.SETTLEMENT_SHARE) / 50) * 50), "Settlement",
                        "Settlement in full and final", i))
        elif kind == 3:
            for d, a, fk in flows_by.get(i, []):
                if d > R or (i in sold and d > cut):
                    continue
                if fk == "plan":
                    ref = ref_of[i]
                    rec.append((d, i, a, "Agency remittance", "%s remittance %s ref %d" % (
                        W.COLLECTION_AGENCY, SM.dd(d).strftime("%b %Y"), ref), first[ref]))
                elif fk == "settle":
                    rec.append((d, i, a, "Settlement", "Settlement in full and final", i))
                else:
                    rec.append((d, i, a, "BPAY" if rng.random() < 0.6 else "Card", "", i))
    rec.append((settled, -1, consideration, "Debt sale",
                "%s: purchase of written-off accounts, sale %s" % (W.SALE_BUYER, W.SALE_REF), -1))
    lo = SM.dn(dt.date(2023, 7, 1))
    rec = [r for r in rec if lo <= r[0] <= R]
    rec.sort(key=lambda r: (r[0], r[1]))
    # a direct debit taken a few days before and dishonoured: the attempt and its reversal fall in one month, before the
    # payment that followed it
    out = []
    for r in rec:
        if r[3] == "Direct debit" and rng.random() < W.DD_DISHONOUR:
            x = int(cal.prev_bd[r[0] - int(rng.integers(4, 9))])
            back = int(cal.next_bd[x + 2])
            if cal.mi_of[x] == cal.mi_of[back] == cal.mi_of[r[0]] and x > int(dme[r[1]]):
                out.append((x, r[1], r[2], "Direct debit", "", r[5], "attempt"))
                out.append((back, r[1], -r[2], "Direct debit", "", r[5], "reversal"))
                r = (r[0], r[1], r[2], "BPAY", "", r[5])
        out.append(r + ("",))
    out.sort(key=lambda r: (r[0], r[1], r[6] == "reversal"))
    seq = 4411870 + np.cumsum(1 + np.random.default_rng(W.SEED + 32).poisson(0.6, len(out)))
    refs = ["RC%07d" % q for q in seq]
    last_attempt = {}
    narr = []
    for ref, r in zip(refs, out):
        if r[6] == "attempt":
            last_attempt[(r[1], r[2])] = ref
            narr.append("")
        elif r[6] == "reversal":
            narr.append("Dishonour of %s" % last_attempt[(r[1], -r[2])])
        else:
            narr.append(r[4])
    ledger = pd.DataFrame(dict(
        receipt_ref=refs,
        loan_no=[L["loan_no"][r[5]] if r[5] >= 0 else None for r in out],
        received_date=[SM.dd(r[0]).isoformat() for r in out],
        amount_aud=["%.2f" % r[2] for r in out],
        source=[r[3] for r in out],
        narrative=narr,
    ))
    ledger["_i"] = [r[1] for r in out]
    ledger["_post"] = [r[5] for r in out]
    ledger["_d"] = [r[0] for r in out]
    ledger["_amt"] = [r[2] for r in out]
    S._coll = dict(dme=dme, sold=sold, consideration=consideration, ledger=ledger, wo=wo, wbal=wbal,
                   flows_by=flows_by, placements=pl, first_holder=first)
    return S._coll


def withdrawn_arrangements(S):
    """collections hardship arrangements approved on 2023-24 defaults and withdrawn before they started (the borrower did
    not return the signed variation, or found the money elsewhere), drawn from their own random stream at the rate
    Collections sees and recorded in the register without touching any repayment history: on defaults that went on to be
    written off, settled for less, or caught up. Collections closes a default case as cured when it approves an
    arrangement, dated from the arrangement's start, and does not reopen the case when the arrangement is withdrawn:
    S.mi_cure maps each such loan to that date"""
    if getattr(S, "mi_cure", None) is not None:
        return S.mi_cure
    C = collections(S)
    cal = S.cal
    rng = np.random.default_rng(W.WITHDRAWN_SEED)
    dme = C["dme"]
    lo, hi = SM.dn(dt.date(2023, 7, 1)), SM.dn(dt.date(2024, 6, 30))
    rows = np.nonzero((dme >= lo) & (dme <= hi))[0]
    taken = {}
    for a in S.arr:
        taken.setdefault(int(a["loan"]), []).append((a["received"], a["end"]))

    def free(i, a, b):
        return all(b + 45 < x or a > y + 45 for x, y in taken.get(i, []))

    def first_due(i, after):
        T = int(S.T[i])
        js = np.nonzero(S.due[i, :T] >= after)[0]
        return (int(js[0]), int(S.due[i, js[0]])) if len(js) else (None, None)

    def place(i):
        """received while the case was open; a caught-up loan's arrangement was to start after the catch-up and was
        withdrawn when the arrears cleared, a written-off or settled loan's was withdrawn before its first varied
        repayment fell due"""
        t0, x = int(dme[i]), int(S.res_day[i])
        if int(S.res_kind[i]) == 1:
            days = cal.bdays(t0 + 3, x - 8)
            if len(days) == 0:
                return None
            r = int(days[int(rng.integers(len(days)))])
            d = int(cal.next_bd[r + int(rng.integers(2, 6))])
            if d >= x:
                return None
            js, st = first_due(i, max(d + 2, x + 1))
            if js is None:
                return None
            c = int(cal.next_bd[x + int(rng.integers(0, 4))])
        else:
            span = x - 50 - (t0 + 3)
            if span < 5:
                return None
            r = int(cal.next_bd[t0 + 3 + int(rng.integers(0, span))])
            d = int(cal.next_bd[r + int(rng.integers(2, 8))])
            js, st = first_due(i, d + 2)
            if js is None or st >= x - 20:
                return None
            gap = cal.bdays(d + 1, st - 1)
            if len(gap) == 0:
                return None
            c = int(gap[int(rng.integers(len(gap)))])
        if c >= st:
            return None
        return r, js, st, c

    S.mi_cure = {}
    plan = []
    for i in rows.tolist():
        if S.res_kind[i] not in W.WITHDRAWN_RATE or rng.random() >= W.WITHDRAWN_RATE[int(S.res_kind[i])]:
            continue
        made = None
        for attempt in range(4):
            made = place(i)
            if made is not None:
                break
        if made is None:
            continue
        r, js, st, c = made
        n = int(rng.choice([3, 4, 6]))
        end = min(SM.add_months(st, n) - 1, int(S.final_nom[i]))
        if not free(i, r, end):
            continue
        plan.append(dict(loan=i, received=r, start=st, end=end, kind="Reduced repayments", outcome="withdrawn",
                         reduced=SM.reduced_amount(rng, S, i, js), reason=SM.pick_reason(rng, r), cancel=c))
        taken.setdefault(i, []).append((r, end))
        S.mi_cure[i] = st
    S.arr.extend(plan)
    return S.mi_cure


def fy24_defaults(S):
    """Collections MI: every loan that defaulted in the quarters of 2023-24 (default month July 2023 to June 2024), its
    balance at the default month end and how Collections closed the default case (a case closed as cured on an approved
    collections arrangement keeps that resolution, dated from the arrangement's start, whatever followed)"""
    C = collections(S)
    cure = withdrawn_arrangements(S)
    dme = C["dme"]
    lo, hi = SM.dn(dt.date(2023, 7, 1)), SM.dn(dt.date(2024, 6, 30))
    rows = np.nonzero((dme >= lo) & (dme <= hi))[0]
    bal = SM.balances(S, rows, dme[rows])
    names = {1: "Cured", 2: "Cured", 3: "Written off", 4: "Settled"}
    assert all(S.res_kind[i] in names and S.res_day[i] > dme[i] for i in rows), "every 2023-24 default is resolved"
    df = pd.DataFrame(dict(
        loan_no=S.L["loan_no"][rows],
        product=np.where(S.L["pl60"][rows], "PL60", "PL36"),
        contract_rate=["%.4f" % x for x in S.L["rate"][rows]],
        default_month=[SM.dd(x).strftime("%Y-%m") for x in dme[rows]],
        balance_at_default=["%.2f" % x for x in np.round(bal, 2)],
        resolution=["Cured" if int(i) in cure else names[int(S.res_kind[i])] for i in rows],
        resolution_date=[SM.dd(cure.get(int(i), S.res_day[i])).isoformat() for i in rows],
    ))
    df["_i"] = rows
    df["_dme"] = dme[rows]
    return df.sort_values(["default_month", "loan_no"], kind="stable").reset_index(drop=True)


def sale_schedule(S):
    """the accounts sold in March 2026 and each one's face value at the cut-off"""
    C = collections(S)
    ids = sorted(C["sold"], key=lambda i: S.L["loan_no"][i])
    return pd.DataFrame(dict(
        loan_no=[S.L["loan_no"][i] for i in ids],
        product=["PL60" if S.L["pl60"][i] else "PL36" for i in ids],
        written_off=[SM.dd(S.close[i]).strftime("%Y-%m") for i in ids],
        face_value_aud=[C["sold"][i] for i in ids],
    ))


def placement_report(S):
    """Wirraway's client placement report for Bellbird as at 30 September 2026: every account placed since the loan
    system went live, in the order placed, with the agency's own column names and Australian dates"""
    C = collections(S)
    pl = C["placements"]
    L = S.L
    return pd.DataFrame({
        "Agency Ref": pl["ref"].astype(np.int64).values,
        "Client Ref": [L["loan_no"][i] for i in pl["i"]],
        "Placed": [SM.dd(x).strftime("%d/%m/%Y") for x in pl["placed"]],
        "Placed Balance": ["%.2f" % b for b in pl["bal"]],
        "Closed": [SM.dd(x).strftime("%d/%m/%Y") if x < SM.BIG else "" for x in pl["closed"]],
        "Close Reason": pl["why"].values,
    })


def write_offs(S, rng=None):
    """loans with a balance written off in each month, July 2025 to September 2026: the month-end batch at 180 days past
    due, and the shortfall left when a loan in default is settled for less than it owes; the amount written off; and
    recoveries received in the month on loans written off in any earlier month (the March 2026 sale included)"""
    C = collections(S)
    wo, bal = C["wo"], C["wbal"]
    led = C["ledger"]
    post = [(int(d), float(a)) for i, d, a in zip(led["_i"], led["_d"], led["_amt"])
            if i < 0 or (S.res_kind[i] == 3 and d > S.close[i])]
    fl = pd.DataFrame(post, columns=["d", "amt"])
    fl["m"] = [SM.dd(x).strftime("%Y-%m") for x in fl["d"]]
    wm = pd.Series([SM.dd(x).strftime("%Y-%m") for x in S.close[wo]])
    # settlements of loans in default: the balance on the settlement day less the amount agreed is written off then
    st = np.nonzero((S.close_type == 4) & (S.close <= S.R))[0]
    paid = {}
    for i, d, a, src in zip(led["_i"], led["_d"], led["_amt"], led["source"]):
        if src == "Settlement" and i >= 0 and S.close_type[i] == 4 and d == S.close[i]:
            paid[int(i)] = paid.get(int(i), 0.0) + float(a)
    keep = np.array([int(i) in paid for i in st], bool)
    st = st[keep]
    short = SM.balances(S, st, S.close[st]) - np.array([paid[int(i)] for i in st])
    sm = pd.Series([SM.dd(x).strftime("%Y-%m") for x in S.close[st]])
    rows = []
    for per in pd.period_range("2025-07", "2026-09", freq="M"):
        m = str(per)
        sel = (wm == m).values
        ss = (sm == m).values
        rows.append(dict(month=m, loans_written_off=int(sel.sum() + ss.sum()),
                         gross_write_off_aud="%.2f" % round(float(bal[sel].sum() + short[ss].sum()), 2),
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
