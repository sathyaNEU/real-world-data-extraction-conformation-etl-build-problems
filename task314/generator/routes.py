"""The rungs, computed on a table of single-family bills (account, area, meter, bill month, billed use).

Used three ways: on the generator's clean truth (checks.py, R3), on the shipped bundle (verify.py), and by the
ceiling script for the cracker and the mirror.  Every function takes plain arrays, so the bundle reader and the
truth feed it the same way.
"""
import datetime as dt
import numpy as np
import world as W

SUMMER = (6, 7, 8, 9)
LIT_ETA = -0.40               # a summer marginal-price elasticity from the residential water literature


def rates_for(bdate, area, option=None):
    """The schedule and extras a bill dated bdate carries; option selects a 2027 Stage 2 option."""
    sched = W.sfr_schedule(bdate)
    cap = W.FM_CHARGE if (area == 'FMSA' and bdate >= W.CAPITAL_FROM) else 0.0
    ex = dict(adder=0.0, tier3=None, surcharge=0.0, tier1=None)
    if option == 'A':
        ex['tier3'] = W.OPT_A_TIER3
        ex['tier1'] = W.OPT_A_TIER1
    elif option == 'B':
        ex['adder'] = W.OPT_B_ADDER
    elif option == 'C':
        ex['surcharge'] = W.OPT_C_SURCHARGE
    return sched, cap, ex


def bill_at(q, meter, bdate, area, option=None):
    sched, cap, ex = rates_for(bdate, area, option)
    return W.sfr_bill(q, meter, sched, cap, ex['adder'], ex['tier3'], ex['surcharge'], ex['tier1'])


def vol_at(q, meter, bdate, area, option=None):
    sched, cap, ex = rates_for(bdate, area, option)
    _, vol, _, _ = W.sfr_charges(q, meter, sched, 0.0, ex['adder'], ex['tier3'], 0.0, ex['tier1'])
    return sum(vol)


def mp_at(q, bdate, area, option=None):
    sched, cap, ex = rates_for(bdate, area, option)
    return W.sfr_marginal(q, sched, ex['adder'], ex['tier3'], ex['tier1'])


def panel(rows):
    """rows: (acct, area, meter, y, m, use).  Returns {acct: {'area','meter', (y,m): use}}."""
    out = {}
    for acct, area, meter, y, m, q in rows:
        d = out.setdefault(acct, {'area': area, 'meter': meter})
        d[(y, m)] = d.get((y, m), 0.0) + q
    return out


def population(pan):
    """The plan's accounts: billed in each of the eight June to September bill months of 2025 and 2026."""
    need = [(y, m) for y in (2025, 2026) for m in SUMMER]
    return [a for a, d in pan.items() if all(k in d for k in need)]


def baseline(pan, accts):
    """Each account's baseline on each summer bill: the mean of its 2025 and 2026 June to September billed use."""
    return {a: {m: 0.5 * (pan[a][(2025, m)] + pan[a][(2026, m)]) for m in SUMMER} for a in accts}


REP_BDATE = {m: dt.date(2026, m, 12) for m in SUMMER}        # any 2026 summer bill date: one schedule all summer
OPT_BDATE = {m: dt.date(2027, m, 12) for m in SUMMER}


def respond(q, r, eta, form='log'):
    """The use taken out of q when its price moves by the ratio r: the constant-elasticity form, the linear form
    (q times the elasticity times the proportional price change) or the arc (midpoint) form."""
    if form == 'log':
        return q * (1.0 - r ** eta)
    if form == 'lin':
        return q * (-eta * (r - 1.0))
    x = (r - 1.0) / ((r + 1.0) / 2.0)
    d = eta * x
    return q * (-2.0 * d / (2.0 + d))


def forecast(pan, base, model, eta, option, form='log', cap=True):
    """Kgal taken out of the baseline by an option under a price model.

    model: 'AP' the whole bill's average price, 'VAP' the volumetric charges' average price,
           'MP' the marginal block price.  Prices are read at each account's baseline use on each bill.
    form: how the elasticity is applied (respond).  cap=False leaves the Fenwick Mesa charge out of the bill."""
    tot = {m: 0.0 for m in SUMMER}
    for a, bm in base.items():
        area, meter = pan[a]['area'], pan[a]['meter']
        ar = area if cap else 'CITY'
        for m, q in bm.items():
            if q <= 0:
                continue
            if model == 'AP':
                p0 = bill_at(q, meter, REP_BDATE[m], ar) / q
                p1 = bill_at(q, meter, OPT_BDATE[m], ar, option) / q
            elif model == 'VAP':
                p0 = vol_at(q, meter, REP_BDATE[m], area) / q
                p1 = vol_at(q, meter, OPT_BDATE[m], area, option) / q
            else:
                p0 = mp_at(q, REP_BDATE[m], area)
                p1 = mp_at(q, OPT_BDATE[m], area, option)
            tot[m] += respond(q, p1 / p0, eta, form)
    return tot


def _bd(y, m):
    return dt.date(y, m, 12)


def eta_fm(pan, pre=(2023, (7, 8, 9)), post=(2025, (7, 8, 9)), price='AP_sim', at_mean=False, screen=False,
           extra_post=None):
    """The Fenwick Mesa capital recovery charge read as a natural experiment: the difference in the change of
    mean log summer use between Fenwick Mesa and the rest of the city, over the same difference in log price.

    price 'AP_sim' prices each account's own pre-period use under both periods' rates; 'AP_billed' takes the bills'
    own average prices.  at_mean prices the account's mean pre-period use; screen drops accounts with a summer bill
    under a third of their own summer mean (an empty house); extra_post pools a second post year."""
    dq = {'FMSA': [], 'CITY': []}
    dp = {'FMSA': [], 'CITY': []}
    posts = [post] + ([extra_post] if extra_post else [])
    for a, d in pan.items():
        k0 = [(pre[0], m) for m in pre[1]]
        k1s = [[(py, m) for m in pm] for (py, pm) in posts]
        k1 = [k for ks in k1s for k in ks]
        if not all(k in d and d[k] > 0.3 for k in k0 + k1):
            continue
        if screen:
            mu = np.mean([d[k] for k in k0 + k1])
            if min(d[k] for k in k0 + k1) < mu / 3.0:
                continue
        area, meter = d['area'], d['meter']
        lq0 = np.mean([np.log(d[k]) for k in k0])
        lq1 = np.mean([np.log(d[k]) for k in k1])
        if price == 'AP_sim':
            if at_mean:
                qm = np.mean([d[k] for k in k0])
                lp0 = np.log(bill_at(qm, meter, _bd(*k0[0]), area) / qm)
                lp1 = np.log(bill_at(qm, meter, _bd(*k1[0]), area) / qm)
            else:
                lp0 = np.mean([np.log(bill_at(d[k], meter, _bd(*k), area) / d[k]) for k in k0])
                lp1 = np.mean([np.log(bill_at(d[k0[i % len(k0)]], meter, _bd(*k1[i]), area) / d[k0[i % len(k0)]])
                               for i in range(len(k1))])
        else:
            lp0 = np.mean([np.log(bill_at(d[k], meter, _bd(*k), area) / d[k]) for k in k0])
            lp1 = np.mean([np.log(bill_at(d[k], meter, _bd(*k), area) / d[k]) for k in k1])
        dq[area].append(lq1 - lq0)
        dp[area].append(lp1 - lp0)
    did_q = np.mean(dq['FMSA']) - np.mean(dq['CITY'])
    did_p = np.mean(dp['FMSA']) - np.mean(dp['CITY'])
    return did_q / did_p, did_q, did_p, len(dq['FMSA']), len(dq['CITY'])


VARIANTS = [
    dict(),
    dict(post=(2024, (7, 8, 9))),
    dict(pre=(2023, (7, 8, 9)), post=(2024, (7, 8, 9)), price='AP_billed'),
    dict(price='AP_billed'),
    dict(post=(2026, (7, 8, 9))),
    dict(post=(2025, (6, 7, 8, 9))),
    dict(pre=(2023, (8, 9)), post=(2025, (8, 9))),
    dict(post=(2026, (6, 7, 8, 9))),
    dict(extra_post=(2026, (7, 8, 9))),
    dict(at_mean=True),
    dict(screen=True),
    dict(at_mean=True, extra_post=(2026, (7, 8, 9))),
    dict(price='AP_billed', extra_post=(2026, (7, 8, 9))),
]


def eta_redesign_mp(pan, pre=(2022, (7, 8, 9)), post=(2023, (7, 8, 9)), area_only='CITY', price='MP'):
    """The July 2023 redesign read the block-rate way: each account's change in mean log summer use on its change
    in log marginal block price at its own pre-period use, by least squares with a constant."""
    xs, ys = [], []
    for a, d in pan.items():
        if area_only and d['area'] != area_only:
            continue
        k0 = [(pre[0], m) for m in pre[1]]
        k1 = [(post[0], m) for m in post[1]]
        if not all(k in d and d[k] > 0.3 for k in k0 + k1):
            continue
        area, meter = d['area'], d['meter']
        lq0 = np.mean([np.log(d[k]) for k in k0])
        lq1 = np.mean([np.log(d[k]) for k in k1])
        if price == 'MP':
            x0 = np.mean([np.log(mp_at(d[k], _bd(*k), area)) for k in k0])
            x1 = np.mean([np.log(mp_at(d[k0[i]], _bd(*k1[i]), area)) for i in range(len(k0))])
        elif price == 'VAP':
            x0 = np.mean([np.log(vol_at(d[k], meter, _bd(*k), area) / d[k]) for k in k0])
            x1 = np.mean([np.log(vol_at(d[k0[i]], meter, _bd(*k1[i]), area) / d[k0[i]]) for i in range(len(k0))])
        else:
            x0 = np.mean([np.log(bill_at(d[k], meter, _bd(*k), area) / d[k]) for k in k0])
            x1 = np.mean([np.log(bill_at(d[k0[i]], meter, _bd(*k1[i]), area) / d[k0[i]]) for i in range(len(k0))])
        xs.append(x1 - x0)
        ys.append(lq1 - lq0)
    X = np.column_stack([np.ones(len(xs)), xs])
    coef = np.linalg.lstsq(X, np.array(ys), rcond=None)[0]
    return float(coef[1]), len(xs)


def eta_fm_annual(pan):
    """The simple comparison on a year of bills each side of the charge (July 2023 to June 2024 against July 2024 to
    June 2025): Fenwick Mesa's change in log annual use against the rest of the city's, over the same difference in
    the log of the year's whole bill per thousand gallons at the account's own first-year use."""
    k0 = [(2023, m) for m in range(7, 13)] + [(2024, m) for m in range(1, 7)]
    k1 = [(2024, m) for m in range(7, 13)] + [(2025, m) for m in range(1, 7)]
    dq = {'FMSA': [], 'CITY': []}
    dp = {'FMSA': [], 'CITY': []}
    for a, d in pan.items():
        if not all(k in d and d[k] > 0.3 for k in k0 + k1):
            continue
        area, meter = d['area'], d['meter']
        q0 = sum(d[k] for k in k0)
        q1 = sum(d[k] for k in k1)
        b0 = sum(bill_at(d[k], meter, _bd(*k), area) for k in k0)
        b1 = sum(bill_at(d[k0[i]], meter, _bd(*k1[i]), area) for i in range(12))
        dq[area].append(np.log(q1 / q0))
        dp[area].append(np.log(b1 / b0))
    did_q = np.mean(dq['FMSA']) - np.mean(dq['CITY'])
    did_p = np.mean(dp['FMSA']) - np.mean(dp['CITY'])
    return did_q / did_p, len(dq['FMSA']), len(dq['CITY'])


def eta_fm_simple(pan):
    """The simplest comparison: the two areas' total use over a year each side of the charge, against the change in
    each area's whole bill per thousand gallons as billed (both sums over the same accounts)."""
    k0 = [(2023, m) for m in range(7, 13)] + [(2024, m) for m in range(1, 7)]
    k1 = [(2024, m) for m in range(7, 13)] + [(2025, m) for m in range(1, 7)]
    agg = {'FMSA': [0.0, 0.0, 0.0, 0.0], 'CITY': [0.0, 0.0, 0.0, 0.0]}
    for a, d in pan.items():
        if not all(k in d and d[k] > 0.3 for k in k0 + k1):
            continue
        g = agg[d['area']]
        g[0] += sum(d[k] for k in k0)
        g[1] += sum(d[k] for k in k1)
        g[2] += sum(bill_at(d[k], d['meter'], _bd(*k), d['area']) for k in k0)
        g[3] += sum(bill_at(d[k], d['meter'], _bd(*k), d['area']) for k in k1)
    f, c = agg['FMSA'], agg['CITY']
    dq = np.log(f[1] / f[0]) - np.log(c[1] / c[0])
    dp = np.log((f[3] / f[1]) / (f[2] / f[0])) - np.log((c[3] / c[1]) / (c[2] / c[0]))
    return dq / dp


def ap_ratios(pan, base, option, cap=True):
    """Each account-month's baseline use and the ratio of its whole bill under the option to its bill at the rates in
    force (the ratio of the two average prices, since the use is the same); cap=False leaves the Fenwick Mesa charge
    out of both bills."""
    qs, rs = [], []
    for a, bm in base.items():
        area, meter = pan[a]['area'], pan[a]['meter']
        ar = area if cap else 'CITY'
        for m, q in bm.items():
            if q <= 0:
                continue
            qs.append(q)
            rs.append(bill_at(q, meter, OPT_BDATE[m], ar, option) / bill_at(q, meter, REP_BDATE[m], ar))
    return np.array(qs), np.array(rs)


def panel_fe(pan, prices=('AP',), area=None, months=None, iters=60):
    """Log use on log price with account-by-calendar-month and bill-month effects; each bill's price is read at the
    account's own reference use for that calendar month (its mean use in that month over the record), so the price
    moves only with the schedule and the charges.  prices: any of 'AP' (whole bill per thousand gallons) and 'MP'
    (the block price of the last thousand gallons).  area: restrict to one service area; months: the bill months
    kept, as (year, month) pairs.  Returns the coefficients in the order asked."""
    rows = []
    ref = {}
    for a, d in pan.items():
        if area and d['area'] != area:
            continue
        for k, q in d.items():
            if not isinstance(k, tuple) or q <= 0.3:
                continue
            if months is not None and k not in months:
                continue
            rows.append((a, k, q))
            ref.setdefault((a, k[1]), []).append(q)
    ref = {key: float(np.mean(v)) for key, v in ref.items()}
    n = len(rows)
    y = np.empty(n)
    X = np.empty((n, len(prices)))
    g1 = np.empty(n, dtype=np.int64)
    g2 = np.empty(n, dtype=np.int64)
    ids1, ids2 = {}, {}
    for i, (a, k, q) in enumerate(rows):
        d = pan[a]
        qr = ref[(a, k[1])]
        y[i] = np.log(q)
        for j, p in enumerate(prices):
            if p == 'AP':
                X[i, j] = np.log(bill_at(qr, d['meter'], _bd(*k), d['area']) / qr)
            else:
                X[i, j] = np.log(mp_at(qr, _bd(*k), d['area']))
        g1[i] = ids1.setdefault((a, k[1]), len(ids1))
        g2[i] = ids2.setdefault(k, len(ids2))

    def demean(v):
        v = v.copy()
        for _ in range(iters):
            m1 = np.bincount(g1, weights=v, minlength=len(ids1)) / np.bincount(g1, minlength=len(ids1))
            v = v - m1[g1]
            m2 = np.bincount(g2, weights=v, minlength=len(ids2)) / np.bincount(g2, minlength=len(ids2))
            v = v - m2[g2]
        return v
    yd = demean(y)
    Xd = np.column_stack([demean(X[:, j]) for j in range(X.shape[1])])
    coef = np.linalg.lstsq(Xd, yd, rcond=None)[0]
    return [float(c) for c in coef]


def af(kgal):
    return kgal / W.AF_KGAL
