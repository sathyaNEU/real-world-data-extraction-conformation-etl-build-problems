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


def forecast(pan, base, model, eta, option):
    """Kgal taken out of the baseline by an option under a price model.

    model: 'AP' the whole bill's average price, 'VAP' the volumetric charges' average price,
           'MP' the marginal block price.  Prices are read at each account's baseline use on each bill."""
    tot = {m: 0.0 for m in SUMMER}
    for a, bm in base.items():
        area, meter = pan[a]['area'], pan[a]['meter']
        for m, q in bm.items():
            if q <= 0:
                continue
            if model == 'AP':
                p0 = bill_at(q, meter, REP_BDATE[m], area) / q
                p1 = bill_at(q, meter, OPT_BDATE[m], area, option) / q
            elif model == 'VAP':
                p0 = vol_at(q, meter, REP_BDATE[m], area) / q
                p1 = vol_at(q, meter, OPT_BDATE[m], area, option) / q
            else:
                p0 = mp_at(q, REP_BDATE[m], area)
                p1 = mp_at(q, OPT_BDATE[m], area, option)
            tot[m] += q * (1.0 - (p1 / p0) ** eta)
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


def af(kgal):
    return kgal / W.AF_KGAL
