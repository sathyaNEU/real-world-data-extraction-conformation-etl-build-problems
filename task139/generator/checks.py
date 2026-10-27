"""task139's generator assertions, run on the cut pack and on the world's clean truth.

    python3 task139/generator/checks.py

The three-rules block (R1 to R3c, the analyst test executed on the clean truth), every semantic fork of the fork table
(SF1 to SF12, the live ones as a cross product), the standing family and the default path's routes, the ladder floors,
each Layer 1 item mishandled, the asks' fairness (each golden equals the world truth) and their rival handlings (every
cracker and mirror route off every figure), the input gates, and figures.json against a fresh computation."""
from __future__ import annotations

import datetime as dt
import itertools
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as AK          # noqa: E402
import common as K         # noqa: E402
import golden as G         # noqa: E402
import pack as PK          # noqa: E402
import world as WD         # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
N_OK = [0]
GOLD_CALL = "renew with the maximum high-use surcharge"


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N_OK[0] += 1


def read_variant(xwalk=True, reversals=True, goodwill=False, deductible=True, feed=True):
    """the pack read with one Layer 1 item handled each way"""
    P = {}
    reg = {r['contract_number']: r for r in G.rd(TARGET, K.REGISTER)}
    P['reg'] = reg
    xw = {r['old_contract_number']: r['new_contract_number'] for r in G.rd(TARGET, K.CROSSWALK)}
    fl_vin = {r['vin']: k for k, r in reg.items() if r['channel'] == "FARELINE"}

    def to_new(ref):
        if ref.startswith("DP-"):
            return xw[ref] if xwalk else None
        if ref.startswith("CV"):
            return ref
        return fl_vin.get(ref) if feed else None
    claims = defaultdict(lambda: dict(net=0.0))
    for r in G.rd(TARGET, K.CLAIMS):
        k = to_new(r['contract_number'])
        if k is None:
            continue
        c = claims[r['claim_number']]
        c['contract'], c['date'], c['odo'] = k, G.D(r['repair_order_date']), int(r['repair_odometer'])
        a = float(r['amount'])
        if r['line_type'] == "GOODWILL" and not goodwill:
            continue
        if r['line_type'] == "DEDUCTIBLE" and not deductible:
            continue
        if a < 0 and r['line_type'] != "DEDUCTIBLE" and not reversals:
            continue
        c['net'] += a
    P['claims'] = list(claims.values())
    pts = defaultdict(set)
    for r in G.rd(TARGET, K.READINGS):
        k = to_new(r['reference'])
        if k is not None:
            pts[k].add((G.D(r['reading_date']), int(r['odometer'])))
    P['pts'] = {k: sorted(v) for k, v in pts.items()}
    return P


def clean_truth(C):
    """the world before any mess: every contract, its exact claims and its odometer at each month end in cover"""
    P = {'reg': {}, 'claims': [], 'pts': {}}
    for c in C:
        P['reg'][c.new_no] = dict(contract_number=c.new_no, vin=c.vin, channel=c.dealer, sale_date=str(c.sale),
                                  odometer_at_sale=str(int(c.o0)), contract_price="%.2f" % c.price,
                                  lienholder=c.lien or "")
        for (d, o, pay) in c.claims:
            P['claims'].append(dict(contract=c.new_no, date=d, odo=o, net=pay))
        pts = []
        d = c.sale + dt.timedelta(days=7)
        while d < c.end:
            pts.append((d, int(round(min(WD.path_odo(c, d), c.o0 + K.LIMIT)))))
            d += dt.timedelta(days=7 if c.channel == "FARELINE" else 30)
        pts.append((c.end, int(round(min(WD.path_odo(c, c.end), c.o0 + K.LIMIT)))))
        P['pts'][c.new_no] = pts
    return P


def golden_with(P, cost_from=None, pop='feed', ratio='means', rate='last', width=10000, tail=False, how='total'):
    """the golden with one reading of a convention changed: the book the cost per mile is read from, the 2026
    contracts that stand for 2027's, the loss ratio's form and the annual mileage's estimator"""
    src = cost_from or P
    edges, miles, cost, count = G.band_costs(src, width, tail)
    if how == 'freq_sev':
        cpm = np.divide(count, miles, out=np.zeros_like(miles), where=miles > 0) * \
            np.divide(cost, count, out=np.zeros_like(cost), where=count > 0)
    else:
        cpm = np.divide(cost, miles, out=np.zeros_like(miles), where=miles > 0)
    fl = G.fareline(P)
    if rate == 'fit':
        for f in fl:
            p = [(d, o) for d, o in P['pts'].get(f['k'], []) if d > f['sale']]
            if len(p) >= 2:
                x = np.array([(d - f['sale']).days for d, o in p], float)
                y = np.array([o for d, o in p], float)
                f['rate'] = float(np.polyfit(x, y, 1)[0] * 365.25)
    known = [f for f in fl if f['rate']]
    if pop == 'all':
        mean_rate = float(np.mean([f['rate'] for f in known]))
        for f in fl:
            f['rate'] = f['rate'] or mean_rate
        known = fl
    life = np.array([G.lifetime(cpm, edges, f['o0'], f['rate']) for f in known])
    price = np.array([f['price'] for f in known])
    lr = 100 * (np.mean(life / price) if ratio == 'per_contract' else life.mean() / price.mean())
    return float(lr)


def call_of(lr):
    return K.election(lr)


def main():
    P = G.read(TARGET)
    F = G.compute(TARGET)
    g = F['g']

    # ---- the call on the cut pack ----
    ok(g['call'] == GOLD_CALL, "the golden files %s (%s)" % (GOLD_CALL, g['call']))
    ok(G.r5(g['lr']) == 75 and G.r5(g['lr_s']) == 55, "loss ratios 75 and 55 at the nearest 5 (%.2f, %.2f)" % (g['lr'], g['lr_s']))
    ok(72.5 + 1.0 < g['lr'] < 77.5 - 1.0, "the current-price loss ratio sits a point inside its 5-point bin (%.2f)" % g['lr'])
    ok(52.5 + 0.5 < g['lr_s'] < 57.5 - 1.0, "the surcharged loss ratio sits inside its bin (%.2f)" % g['lr_s'])
    ok(g['lr'] > K.STANDARD + 3 and g['lr_s'] < K.STANDARD - 10, "the call clears both edges of the standard")

    # ---- SF1 to SF3, the standing family as a cross product: band width, the last reading's tail, frequency and
    # severity apart or together, interpolation between band midpoints ----
    fam = {}
    for w, tail, how in itertools.product((5000, 10000, 20000), (False, True), ('total', 'freq_sev', 'interp')):
        r = G.golden(P, w, tail, how)
        fam[(w, tail, how)] = r['lr']
        ok(r['call'] == GOLD_CALL, "SF1 SF2 SF3 width %d tail %s %s files the golden (%.2f)" % (w, tail, how, r['lr']))
        ok(G.r5(r['lr']) == 75 and G.r5(r['lr_s']) == 55, "SF1 SF2 SF3 width %d tail %s %s rounds to 75 and 55" % (w, tail, how))
    ok(max(fam.values()) - min(fam.values()) < 1.5, "the standing family spans under 1.5 points (%.2f)" %
       (max(fam.values()) - min(fam.values())))

    # ---- SF4 the population standing for 2027, SF5 the book the cost is read from, SF6 the loss ratio's form,
    # SF7 the annual mileage estimator, as a cross product with the band width ----
    retail = dict(P)
    retail['reg'] = {k: r for k, r in P['reg'].items() if r['channel'] != "FARELINE"}
    retail['claims'] = [c for c in P['claims'] if c['contract'] in retail['reg']]
    for pop, src, ratio, rate, w in itertools.product(('feed', 'all'), (None, retail), ('means', 'per_contract'),
                                                       ('last', 'fit'), (5000, 10000, 20000)):
        lr = golden_with(P, src, pop, ratio, rate, w)
        tag = "SF4 %s SF5 %s SF6 %s SF7 %s width %d" % (pop, 'retail' if src else 'whole', ratio, rate, w)
        ok(call_of(lr) == GOLD_CALL and G.r5(lr) == 75 and G.r5(lr / 1.4) == 55, "%s files the golden (%.2f)" % (tag, lr))

    # ---- SF8 goodwill, SF9 reversed lines, SF10 the deductible line, SF11 the crosswalk (R2, each Layer 1 item
    # mishandled leaves the call) ----
    for tag, kw in (("SF8 goodwill counted", dict(goodwill=True)), ("SF9 reversals ignored", dict(reversals=False)),
                    ("SF10 deductible not netted", dict(deductible=False)), ("SF11 crosswalk unused", dict(xwalk=False))):
        Pv = read_variant(**kw)
        if tag.startswith("SF11"):
            # the contracts the old numbers cannot be mapped for are left out whole, their claims, readings and
            # exposure together (dropping their claims while keeping the miles they ran is the unmatched join the
            # hygiene battery flags: 37.8 per cent of the claims carry a pre-2024 number)
            Pv['reg'] = {k: r for k, r in Pv['reg'].items() if G.D(r['sale_date']) >= K.MIGRATION}
            Pv['claims'] = [c for c in Pv['claims'] if c['contract'] in Pv['reg']]
        lr = G.golden(Pv)['lr']
        ok(call_of(lr) == GOLD_CALL, "R2 %s leaves the call (%.2f)" % (tag, lr))
    Pd = read_variant()
    ok(abs(G.golden(Pd)['lr'] - g['lr']) < 1e-9, "the variant reader reproduces the golden")
    # duplicate maintenance uploads: a repeated reading adds no miles
    ok(len(P['pts']) > 0 and all(len(v) == len(set(v)) for v in P['pts'].values()), "R2 duplicate uploads collapse")
    # SF12 the cover's 60 months as calendar months or 1,826 days: no 2026 contract reaches either before 75,000 miles
    fl = [f for f in G.fareline(P) if f['rate']]
    near = sum(1 for f in fl if K.LIMIT / f['rate'] > 4.9)
    ok(near < 0.02 * len(fl), "SF12 under 2 per cent of contracts run near the time limit (%d)" % near)

    # ---- the default path's routes, each on the wrong side of the standard (R3a on the pack) ----
    R = F['routes']
    for k, v in R.items():
        ok(v <= K.STANDARD - 10, "route %s files renew at current rates, 10 points clear (%.1f)" % (k, v))

    # ---- R1: the field's raw material ships, the deciding quantity does not ----
    heads = set()
    for nm in os.listdir(TARGET):
        if nm.endswith(".csv"):
            heads |= set(open(os.path.join(TARGET, nm), encoding="utf-8").readline().strip().split(","))
    ok(not any(("loss" in h or "per_mile" in h or "ratio" in h) for h in heads), "R1 no shipped column holds a loss ratio "
       "or a cost per mile")
    ok(sum(1 for _ in open(os.path.join(TARGET, K.READINGS))) > 25000, "R1 the odometer readings ship at row level")
    ok(len(P['claims']) > 5000, "R1 the claims ship at line level (%d claims)" % len(P['claims']))

    # ---- R3, the analyst test on the clean truth ----
    C = WD.simulate()
    M = PK.ids(C)
    T = WD.truth_lifetime(C)
    ok(call_of(T['lr']) == GOLD_CALL and G.r5(T['lr']) == 75, "the world's own loss ratio files the golden (%.2f)" % T['lr'])
    ok(abs(T['lr'] - g['lr']) < 2.0, "the golden sits within 2 points of the world's truth (%.2f against %.2f)" % (g['lr'], T['lr']))
    CT = clean_truth(C)
    Rc = G.routes(CT)
    for k, v in Rc.items():
        ok(call_of(v) == "renew at current rates", "R3a route %s on the clean truth files renew at current rates (%.1f)" % (k, v))
    gc = G.golden(CT)
    ok(gc['call'] == GOLD_CALL, "R3b the decisive step alone files the golden on the clean truth (%.2f)" % gc['lr'])
    # the lower rungs' single corrections: per mile but pooled, per mile by odometer with one average claim, the
    # retail clock sped up by the mileage ratio, all stay on renew
    for k in ('pooled_per_mile', 'freq_band_x_avg_claim', 'retail_age_accelerated', 'own_age_linear_trend'):
        ok(Rc[k] < K.STANDARD, "R3b the single correction %s stays on renew (%.1f)" % (k, Rc[k]))
    ok(Rc['own_month_x_60'] < K.STANDARD, "the 60-month reading of the channel's months stays on renew")
    # R3c: no plant ships (no memo, prior review or stated figure; the repeated-block sweep: no claim duplicated)
    seen = defaultdict(int)
    for c in C:
        for cl in c.claims:
            seen[(c.cid, cl)] += 1
    ok(max(seen.values()) == 1, "R3c no claim is copied")
    for nm in os.listdir(TARGET):
        ok(not nm.endswith((".docx", ".pptx", ".md", ".txt")), "R3c no memo or briefing ships (%s)" % nm)

    # ---- the asks equal the world truth ----
    dealers = PK.dealer_rows(C)
    out, returns = PK.remittances(C, dealers)
    bad = {x['ref'] for x in returns}
    got = defaultdict(float)
    for x in out:
        if x['ref'] not in bad:
            got[x['c'].cid] += x['c'].price
    tb = {q: [0.0, 0.0] for q in AK.QB}
    for c in C:
        if c.channel == "DEALER" and K.quarter(c.sale) in tb:
            tb[K.quarter(c.sale)][0] += c.price
            tb[K.quarter(c.sale)][1] += got.get(c.cid, 0.0)
    for q in AK.QB:
        ok(abs(F['ask_b'][q]['received'] - tb[q][1]) < 0.01, "ask B %s received equals the truth" % q)
        ok(abs(F['ask_b'][q]['outstanding'] - (tb[q][0] - tb[q][1])) < 0.01, "ask B %s outstanding equals the truth" % q)
        ok(F['ask_b'][q]['outstanding'] > 0, "ask B %s has premium outstanding" % q)
    reqs = PK.cancellation_requests(C)
    first = {}
    for q in sorted(reqs, key=lambda z: (z['received_date'], z['request_id'])):
        first.setdefault(q['cid'], q)
    key2 = {}
    for c in C:
        key2[c.new_no] = c.cid
        if c.old_no:
            key2[c.old_no] = c.cid
    pts = defaultdict(list)
    for r in PK.reading_rows(C):
        cid = key2.get(r['reference'])
        if cid:
            pts[cid].append((G.D(r['reading_date']), int(r['odometer'])))
    ta = {q: [0, 0.0, 0.0] for q in AK.QA}
    for cid, q in first.items():
        c = M[cid]
        d = q['received_date']
        qq = K.quarter(d)
        if qq not in ta:
            continue
        odo = q['odometer_stated'] if q['odometer_stated'] != "" else max([o for dd, o in pts[cid] if dd <= d] or [c.o0])
        claimed = any(cd <= d for cd, _, _ in c.claims)
        amt = AK.refund(c.price, c.sale, d, max(odo - c.o0, 0), claimed)
        ta[qq][0] += 1
        ta[qq][1] += amt
        ta[qq][2] += amt if c.lien else 0.0
    for q in AK.QA:
        a = F['ask_a'][q]
        ok(a['n'] == ta[q][0], "ask A %s contracts cancelled equal the truth (%d, %d)" % (q, a['n'], ta[q][0]))
        ok(abs(a['refund'] - ta[q][1]) < 0.01, "ask A %s refunds equal the truth" % q)
        ok(abs(a['lien'] - ta[q][2]) < 0.01, "ask A %s lienholder refunds equal the truth" % q)

    # ---- the asks' rival handlings miss every figure ----
    def figs_a(x):
        return {(q, k): x[q][k] for q in AK.QA for k in ('n', 'refund', 'lien')}

    def figs_b(x):
        return {(q, k): x[q][k] for q in AK.QB for k in ('received', 'outstanding')}
    ga, gb = figs_a(F['ask_a']), figs_b(F['ask_b'])
    for how in ('per_request', 'vin_asof', 'drop_unmatched'):
        alt = figs_a(AK.ask_a(P, TARGET, how))
        for key, v in ga.items():
            ok(abs(alt[key] - v) > 0.5, "ask A %s misses %s (%s against %s)" % (how, key, alt[key], v))
    for how in ('include_returned', 'dedupe_naive', 'dedupe_first', 'match_any_month', 'vin_only', 'cents_as_dollars'):
        alt = figs_b(AK.ask_b(P, TARGET, how))
        for key, v in gb.items():
            ok(abs(alt[key] - v) > 0.5, "ask B %s misses %s (%s against %s)" % (how, key, alt[key], v))
    alt = figs_b(AK.ask_b(P, TARGET, 'dedupe_contract'))
    ok(all(abs(alt[k] - v) < 0.005 for k, v in gb.items()), "ask B: returns removed before a re-sent duplicate is the golden")
    # the asks are decoupled: no ask file is read by the call, and the call's population carries no ask device row
    ok(all(r['channel'] != "FARELINE" for r in G.rd(TARGET, K.REGISTER) if r['lienholder']), "the Fareline contracts carry no lienholder")
    call_src = open(os.path.join(HERE, "golden.py")).read().split("def compute")[0]
    for nm in ("K.CANCELS", "K.BORDEREAUX", "K.RETURNS", "K.DEALERS"):
        ok(nm not in call_src, "the call never reads %s" % nm)

    # ---- the input gates ----
    files = os.listdir(TARGET)
    ok(len(files) >= 10, "10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta['distractor_files']) >= 2, "two or more distractors named")
    sol = open(os.path.join(HERE, "golden.py")).read() + open(os.path.join(HERE, "asks.py")).read()
    for const, nm in (("K.CLIP", K.CLIP), ("K.FACILITIES", K.FACILITIES)):
        ok("target/" + nm in meta['distractor_files'] and const not in sol, "distractor %s is unused by the solution" % nm)

    # ---- figures.json is the computation ----
    stored = json.load(open(os.path.join(HERE, "figures.json")))
    fresh = json.loads(json.dumps(G.flat(F), sort_keys=True))
    ok(stored == fresh, "figures.json matches a fresh computation")
    print("checks: %d passed" % N_OK[0])


if __name__ == "__main__":
    main()
