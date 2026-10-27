"""The asks' golden figures from the cut pack, and the rival handlings each ask's natural routes land on (the ladder
never ships).

Ask A: retail contracts cancelled in each quarter of 2026 to 30 September and the refunds owed on them.
Ask B: for retail contracts sold in each quarter of 2025, the premium received from the dealers to 30 September 2026
and the premium still outstanding."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import openpyxl

import common as K
import golden as G

QA = ("2026Q1", "2026Q2", "2026Q3")
QB = ("2025Q1", "2025Q2", "2025Q3", "2025Q4")


def refund(price, sale, cancel, miles, claimed):
    days = (cancel - sale).days
    if days <= K.FREE_LOOK and not claimed:
        return price
    used = max(days / K.TERM_DAYS, miles / K.LIMIT)
    return max(0.0, price * (1 - used) - K.FEE)


def ask_a(P, target, how='golden'):
    reg = P['reg']
    by_vin = defaultdict(list)
    for k, r in reg.items():
        by_vin[r['vin']].append(k)
    claim_dates = defaultdict(list)
    for c in P['claims']:
        claim_dates[c['contract']].append(c['date'])
    reqs = G.rd(target, K.CANCELS)
    cancel = {}
    for q in sorted(reqs, key=lambda z: (z['received_date'], z['request_id'])):
        d = G.D(q['received_date'])
        if q['contract_number']:
            k = q['contract_number']
        elif how == 'drop_unmatched':
            continue
        else:
            cands = [x for x in by_vin[q['vin']] if G.D(reg[x]['sale_date']) <= d]
            if how == 'golden':
                cands = [x for x in cands if reg[x]['lienholder'] == q['lienholder']]
            if not cands:
                continue
            k = max(cands, key=lambda x: reg[x]['sale_date'])
        key = (k, q['request_id']) if how == 'per_request' else k
        if key not in cancel:
            cancel[key] = dict(k=k, date=d, odo=q['odometer_stated'])
    out = {qq: dict(n=0, refund=0.0, lien=0.0) for qq in QA}
    for x in cancel.values():
        qq = K.quarter(x['date'])
        if qq not in out:
            continue
        r = reg[x['k']]
        if r['channel'] == "FARELINE":
            continue
        sale, o0, price = G.D(r['sale_date']), int(r['odometer_at_sale']), float(r['contract_price'])
        if x['odo'] != "":
            odo = int(x['odo'])
        else:
            pts = [o for dd, o in P['pts'].get(x['k'], []) if dd <= x['date']]
            odo = max(pts) if pts else o0
        claimed = any(cd <= x['date'] for cd in claim_dates.get(x['k'], []))
        amt = refund(price, sale, x['date'], max(odo - o0, 0), claimed)
        out[qq]['n'] += 1
        out[qq]['refund'] += amt
        if r['lienholder']:
            out[qq]['lien'] += amt
    return out


def bordereau_rows(target):
    wb = openpyxl.load_workbook("%s/%s" % (target, K.BORDEREAUX), read_only=True)
    rows = []
    for ws in wb.worksheets:
        vals = list(ws.iter_rows(values_only=True))
        for v in vals[1:]:
            if ws.title == "Trinity Motor Group":
                rows.append(dict(dealer=v[1], contract=v[2], vin=None, sale=None, amount=float(v[4]), ref=v[5],
                                 month=dt.datetime.strptime(v[0], "%Y-%m").date()))
            elif ws.title == "Brazos Auto Partners":
                rows.append(dict(dealer=v[1], contract=v[3], vin=None, sale=None, amount=int(v[4]) / 100.0, ref=v[5],
                                 cents=int(v[4]), month=dt.datetime.strptime(v[0], "%b %Y").date()))
            else:
                dd, mm, yy = v[2].split("/")
                rows.append(dict(dealer=v[0], contract=None, vin=v[1], sale=dt.date(int(yy), int(mm), int(dd)),
                                 amount=float(v[3]), ref=v[5], raw_sale=v[2],
                                 month=dt.datetime.strptime(v[4], "%m/%Y").date()))
    return rows


def returned_refs(target, how='golden'):
    """a returned payment is the dealer-month bordereau whose lines sum to the returned amount: the bank's report names
    the originator as its account holder and carries its own trace number"""
    code = {r['dealer_name'].upper(): r['dealer_code'] for r in G.rd(target, K.DEALERS)}
    pay = defaultdict(float)
    for x in bordereau_rows(target):
        pay[(x['dealer'], x['month'], x['ref'])] += x['amount']
    out = set()
    for r in G.rd(target, K.RETURNS):
        d = code.get(r['originator_name'])
        amt = float(r['amount'])
        s = G.D(r['settlement_date'])
        if how == 'match_any_month':          # dealer and amount, the re-sent bordereau's month not told apart
            hits = [ref for (dl, m, ref), v in pay.items() if dl == d and abs(v - amt) < 0.005]
        else:
            hits = [ref for (dl, m, ref), v in pay.items()
                    if dl == d and (m.year, m.month) == (s.year, s.month) and abs(v - amt) < 0.005]
        out.update(hits)
    return out


def ask_b(P, target, how='golden'):
    reg = P['reg']
    returned = returned_refs(target, 'match_any_month' if how == 'match_any_month' else 'golden')
    by_vin_sale = {(r['vin'], r['sale_date']): k for k, r in reg.items()}
    by_vin = defaultdict(list)
    for k, r in reg.items():
        by_vin[r['vin']].append(k)
    got = defaultdict(float)
    seen = set()
    for x in bordereau_rows(target):
        if x['contract']:
            k = x['contract']
        elif how == 'vin_only':
            k = max(by_vin[x['vin']], key=lambda z: reg[z]['sale_date'])
        else:
            k = by_vin_sale.get((x['vin'], str(x['sale'])))
            if k is None:
                continue
        if how == 'dedupe_first':             # a contract's second line dropped as a duplicate, then returns removed
            if k in seen:
                continue
            seen.add(k)
        if how not in ('include_returned', 'dedupe_naive') and x['ref'] in returned:
            continue
        if how in ('dedupe_contract', 'dedupe_naive'):
            if k in seen:
                continue
            seen.add(k)
        amt = x['amount']
        if how == 'cents_as_dollars' and 'cents' in x:
            amt = float(x['cents'])
        got[k] += amt
    out = {qq: dict(owed=0.0, received=0.0) for qq in QB}
    for k, r in reg.items():
        if r['channel'] == "FARELINE":
            continue
        qq = K.quarter(G.D(r['sale_date']))
        if qq in out:
            out[qq]['owed'] += float(r['contract_price'])
            out[qq]['received'] += got.get(k, 0.0)
    for v in out.values():
        v['outstanding'] = v['owed'] - v['received']
    return out
