"""Reads the cut pack and computes the call: the lifetime loss ratio of next year's Fareline contracts, costed per
mile at the odometer from the whole book and carried along each contract's mileage path to its limit; beside it the
default path's routes and the standing family, which checks.py asserts."""
from __future__ import annotations

import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np

import common as K


def r5(x):
    return int(5 * round(x / 5.0))


def rd(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def D(s):
    return dt.date.fromisoformat(s)


def read(target):
    P = {}
    reg = {r['contract_number']: r for r in rd(target, K.REGISTER)}
    P['reg'] = reg
    xw = {r['old_contract_number']: r['new_contract_number'] for r in rd(target, K.CROSSWALK)}
    fl_vin = {r['vin']: k for k, r in reg.items() if r['channel'] == "FARELINE"}
    def to_new(ref):
        if ref.startswith("DP-"):
            return xw[ref]
        if ref.startswith("CV"):
            return ref
        return fl_vin.get(ref)
    P['to_new'] = to_new
    claims = defaultdict(lambda: dict(net=0.0))
    for r in rd(target, K.CLAIMS):
        c = claims[r['claim_number']]
        c['contract'] = to_new(r['contract_number'])
        c['date'] = D(r['repair_order_date'])
        c['odo'] = int(r['repair_odometer'])
        if r['line_type'] != "GOODWILL":
            c['net'] += float(r['amount'])
    P['claims'] = list(claims.values())
    pts = defaultdict(set)
    for r in rd(target, K.READINGS):
        k = to_new(r['reference'])
        if k is not None:
            pts[k].add((D(r['reading_date']), int(r['odometer'])))
    P['pts'] = {k: sorted(v) for k, v in pts.items()}
    return P


def cover_end_date(r):
    return K.add_months(D(r['sale_date']), K.TERM_MONTHS)


def exposure(P, width=10000, top=200000, tail=False):
    """miles driven under cover in each odometer band: each contract's path through its readings, from the sale to
    its last reading in cover (or, with tail, on to the valuation date at its own rate), stopped at 75,000 miles"""
    edges = np.arange(0, top + width, width)
    miles = np.zeros(len(edges) - 1)
    for k, r in P['reg'].items():
        s, o0 = D(r['sale_date']), int(r['odometer_at_sale'])
        lim, end = o0 + K.LIMIT, min(cover_end_date(r), K.VALUATION)
        path = [(s, o0)] + [(d, o) for d, o in P['pts'].get(k, []) if s <= d <= end]
        if tail and len(path) > 1 and path[-1][0] < end and (end - path[-1][0]).days <= 62:
            d1, o1 = path[-1]
            rate = (o1 - o0) / max((d1 - s).days, 1)
            path.append((end, o1 + rate * (end - d1).days))
        for (d1, o1), (d2, o2) in zip(path[:-1], path[1:]):
            a, b = min(o1, lim), min(o2, lim)
            if b > a:
                miles += np.clip(np.minimum(edges[1:], b) - np.maximum(edges[:-1], a), 0, None)
    return edges, miles


def band_costs(P, width=10000, tail=False):
    edges, miles = exposure(P, width, tail=tail)
    cost = np.zeros(len(miles))
    count = np.zeros(len(miles))
    for c in P['claims']:
        b = min(int(c['odo'] // width), len(cost) - 1)
        cost[b] += c['net']
        count[b] += 1
    return edges, miles, cost, count


def fareline(P):
    """each 2026 Fareline contract: odometer at sale, annual mileage from the weekly feed, price"""
    out = []
    for k, r in P['reg'].items():
        if r['channel'] != "FARELINE":
            continue
        s, o0 = D(r['sale_date']), int(r['odometer_at_sale'])
        p = [(d, o) for d, o in P['pts'].get(k, []) if d > s]
        rate = (p[-1][1] - o0) / (p[-1][0] - s).days * 365.25 if p else None
        out.append(dict(k=k, sale=s, o0=o0, rate=rate, price=float(r['contract_price'])))
    return out


def lifetime(rates_per_mile, edges, o0, rate):
    """claims cost over a contract's cover at the given cost per mile by band: from o0 to the earlier of 75,000 miles
    and 60 months at the contract's annual mileage"""
    b = o0 + min(K.LIMIT, rate * 5.0)
    seg = np.clip(np.minimum(edges[1:], b) - np.maximum(edges[:-1], o0), 0, None)
    return float(np.sum(seg * rates_per_mile))


def golden(P, width=10000, tail=False, how='total'):
    edges, miles, cost, count = band_costs(P, width, tail)
    with np.errstate(invalid='ignore', divide='ignore'):
        if how in ('total', 'interp'):
            cpm = np.where(miles > 0, cost / miles, 0.0)
        else:                                    # frequency per mile by band times the band's own average claim
            cpm = np.where(miles > 0, count / miles, 0.0) * np.where(count > 0, cost / np.maximum(count, 1), 0.0)
    fl = [f for f in fareline(P) if f['rate']]
    if how == 'interp':                          # cost per mile interpolated linearly between band midpoints
        mids = (edges[:-1] + edges[1:]) / 2
        ok = miles > 0
        fine = np.arange(0, edges[-1] + 1000, 1000)
        rate = np.interp((fine[:-1] + fine[1:]) / 2, mids[ok], cpm[ok])
        life = [lifetime(rate, fine, f['o0'], f['rate']) for f in fl]
    else:
        life = [lifetime(cpm, edges, f['o0'], f['rate']) for f in fl]
    cost_ = float(np.mean(life))
    price = float(np.mean([f['price'] for f in fl]))
    lr = 100 * cost_ / price
    under = edges[1:] <= 70000
    return dict(lr=lr, lr_s=lr / (1 + K.SURCHARGE), cost=cost_, price=price, n=len(fl), cpm=cpm, edges=edges,
                miles=miles, call=K.election(lr), rate=float(np.mean([f['rate'] for f in fl])),
                o0=float(np.mean([f['o0'] for f in fl])),
                months=float(np.mean([min(K.LIMIT / f['rate'] * 12, K.TERM_MONTHS) for f in fl])),
                flat=float(cost[under].sum() / miles[under].sum()))


def routes(P):
    """the default path's routes, each a lifetime loss ratio at the current price"""
    fl = [f for f in fareline(P) if f['rate']]
    price = float(np.mean([f['price'] for f in fl]))
    cover_m = np.array([min(K.LIMIT / f['rate'] * 12, K.TERM_MONTHS) for f in fl])
    out = {}
    # the channel's own claims cost per contract-month in force, over the months of cover
    cm = sum((K.VALUATION - f['sale']).days / 30.4375 for f in fl)
    fk = {f['k'] for f in fl}
    cc = sum(c['net'] for c in P['claims'] if c['contract'] in fk)
    out['own_month_x_cover'] = cc / cm * cover_m.mean()
    out['own_month_x_60'] = cc / cm * K.TERM_MONTHS
    # the channel's own cost per contract-month by month of age, a linear trend carried over the cover
    num, den = np.zeros(60), np.zeros(60)
    for f in fl:
        for a in range(int((K.VALUATION - f['sale']).days // 30.4375)):
            den[a] += 1
    for c in P['claims']:
        if c['contract'] in fk:
            f = next(x for x in fl if x['k'] == c['contract'])
            a = int((c['date'] - f['sale']).days // 30.4375)
            if a < 60 and den[a] > 0:
                num[a] += c['net']
    ok = den > 50
    ages = np.arange(60)[ok]
    b = np.polyfit(ages, num[ok] / den[ok], 1, w=np.sqrt(den[ok]))
    out['own_age_linear_trend'] = float(np.mean([sum(max(b[1] + b[0] * a, 0) for a in range(int(round(m)))) for m in cover_m]))
    # the retail book's cost per contract-month by month of age over 60 months, with the 20 per cent loading
    num, den = np.zeros(60), np.zeros(60)
    ret = {k: r for k, r in P['reg'].items() if r['channel'] != "FARELINE"}
    for k, r in ret.items():
        s = D(r['sale_date'])
        last = min(cover_end_date(r), K.VALUATION)
        pts = P['pts'].get(k, [])
        stop = max([d for d, o in pts if d <= last], default=s)
        for a in range(min(int((stop - s).days // 30.4375) + 1, 60)):
            den[a] += 1
    for c in P['claims']:
        if c['contract'] in ret:
            a = int((c['date'] - D(ret[c['contract']]['sale_date'])).days // 30.4375)
            if a < 60:
                num[a] += c['net']
    cr = num / np.maximum(den, 1)
    out['retail_age_x1.2'] = 1.2 * cr.sum()
    ratio = np.mean([f['rate'] for f in fl]) / 12500.0
    out['retail_age_accelerated'] = float(np.mean([sum(cr[min(int(a * ratio), 59)] * ratio for a in range(int(round(m))))
                                                   for m in cover_m]))
    # cost per mile at the odometer, but every contract's miles run on at its own rate to its 60 months or the
    # valuation date, as if no cover had ended early
    edges, miles, cost, count = band_costs(P)
    m2 = np.zeros(len(miles))
    for k, r in P['reg'].items():
        s, o0 = D(r['sale_date']), int(r['odometer_at_sale'])
        end = min(cover_end_date(r), K.VALUATION)
        p = [(d, o) for d, o in P['pts'].get(k, []) if s < d <= end]
        if not p:
            continue
        rt = (p[-1][1] - o0) / max((p[-1][0] - s).days, 1)
        b = min(o0 + rt * (end - s).days, o0 + K.LIMIT)
        m2 += np.clip(np.minimum(edges[1:], b) - np.maximum(edges[:-1], o0), 0, None)
    c2 = np.divide(cost, m2, out=np.zeros_like(m2), where=m2 > 0)
    out['per_mile_odometer_in_force_to_term'] = float(np.mean([lifetime(c2, edges, f['o0'], f['rate']) for f in fl]))
    # the book's pooled cost per mile over 75,000 miles
    edges, miles, cost, count = band_costs(P)
    out['pooled_per_mile'] = cost.sum() / miles.sum() * K.LIMIT
    # frequency per mile by band at the book's average claim
    fpm = np.divide(count, miles, out=np.zeros_like(miles), where=miles > 0)
    avg = cost.sum() / count.sum()
    out['freq_band_x_avg_claim'] = float(np.mean([lifetime(fpm * avg, edges, f['o0'], f['rate']) for f in fl]))
    return {k: 100 * v / price for k, v in out.items()}


def compute(target):
    import asks as AK
    P = read(target)
    g = golden(P)
    fam = {}
    for w in (5000, 10000, 20000):
        for tail in (False, True):
            for how in ('total', 'freq_sev'):
                fam[(w, tail, how)] = golden(P, w, tail, how)['lr']
    F = dict(g=g, fam=fam, routes=routes(P), ask_a=AK.ask_a(P, target), ask_b=AK.ask_b(P, target))
    return F


def flat(F):
    g = F['g']
    fam = list(F['fam'].values())
    out = {"call.election": g['call'], "lr.current_price_pct": round(g['lr'], 1),
           "lr.surcharged_price_pct": round(g['lr_s'], 1), "lr.current_price_pct_nearest_5": r5(g['lr']),
           "lr.surcharged_price_pct_nearest_5": r5(g['lr_s']), "lifetime.claims_cost_usd": round(g['cost'], 0),
           "lifetime.claims_cost_usd_nearest_100": int(round(g['cost'], -2)),
           "lifetime.average_price_usd": round(g['price'], 0), "lifetime.average_price_usd_nearest_10": int(round(g['price'], -1)),
           "fareline.contracts_2026": g['n'], "fareline.annual_miles_nearest_1000": int(round(g['rate'], -3)),
           "fareline.odometer_at_sale_nearest_1000": int(round(g['o0'], -3)),
           "fareline.months_to_limit_nearest_1": int(round(g['months'])),
           "standing.lr_min_pct": round(min(fam), 1), "standing.lr_max_pct": round(max(fam), 1),
           "cpm_per_1000.under_70000_usd": round(g['flat'] * 1000, 1)}
    out.update({"inputs.standard_pct": K.STANDARD, "inputs.surcharge_pct": int(100 * K.SURCHARGE),
                "inputs.surcharge_factor": 1 + K.SURCHARGE, "inputs.term_months": K.TERM_MONTHS,
                "inputs.limit_miles": K.LIMIT, "inputs.flat_to_miles": 70000, "inputs.band_miles": 10000,
                "inputs.cost_per_miles": 1000})
    for k, v in F['routes'].items():
        out["route.%s.lr_pct" % k] = round(v, 1)
    for j in range(len(g['cpm'])):
        lo = int(g['edges'][j])
        if g['miles'][j] > 0:
            out["cost_per_mile.%06d" % lo] = round(float(g['cpm'][j]), 3)
    for k, v in F['ask_a'].items():
        out["askA.%s.contracts_cancelled" % k] = v['n']
        out["askA.%s.refunds_usd" % k] = round(v['refund'], 0)
        out["askA.%s.refunds_to_lienholders_usd" % k] = round(v['lien'], 0)
    for k, v in F['ask_b'].items():
        out["askB.%s.premium_received_usd" % k] = round(v['received'], 0)
        out["askB.%s.premium_outstanding_usd" % k] = round(v['outstanding'], 0)
    return out
