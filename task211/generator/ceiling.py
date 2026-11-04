"""task211 ask ceiling, measured on the cut pack. Shares no code with the generator: it reads target/ and the golden
figures in figures.json and rebuilds each modelled response's ask figures with its own parsing.

The cracker lands the call, executes every filed rule (the purchasing manual's receipt-day rule, the service schedule's
backorder rule, the item list) and runs the whole hygiene battery, decoding case-level barcodes it cannot join.
The full includer reads every file and acts on every stated fact, and runs the standard checks (orphan keys,
duplicates, units, clocks, stated maxima): a barcode no register lists is an orphan and is set aside.
Both place a price correction that names no delivery in the quarter before its invoice, 7.3 read on its face.
The mirror stops at the most attractive wrong rung: invoice dates, and the notices' expected release dates."""
import datetime as dt, json, os, sys
from pathlib import Path
import pandas as pd
from zoneinfo import ZoneInfo

TASK = Path(__file__).resolve().parent.parent
T = Path(os.environ.get('T211_TARGET', str(TASK / 'target')))
PT = ZoneInfo('America/Los_Angeles')
GENS = ['Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']
Q = {1: (dt.date(2026, 1, 1), dt.date(2026, 3, 31)), 2: (dt.date(2026, 4, 1), dt.date(2026, 6, 30))}


def quarter(d):
    for q, (a, b) in Q.items():
        if a <= d <= b:
            return q
    return 0


def spend(mode):
    inv = pd.read_csv(T / 'wholesaler_invoice_lines.csv', dtype=str).fillna('')
    rec = pd.read_csv(T / 'dc_receiving_log.csv', dtype=str)
    reg = pd.read_csv(T / 'pack_register.csv', dtype=str)
    name = dict(zip(reg.ndc, reg['product']))
    out = {(p, q): 0.0 for p in GENS for q in (1, 2)}
    rec['d'] = pd.to_datetime(rec.received).dt.date
    parts = {k: g for k, g in rec.groupby('delivery_no')}
    for r in inv.itertuples(index=False):
        p = name[r.ndc]
        if p not in GENS:
            continue
        amt = float(r.amount)
        idate = pd.Timestamp(r.invoice_date).date()
        if mode == 'mirror':
            q = quarter(idate)          # every line by its invoice date
            if q:
                out[(p, q)] += amt
            continue
        if not r.delivery_ref:
            # 7.3 read on its face: a price correction for bottles already received belongs to the quarter before the one
            # it is invoiced in, where the bottles invoiced at the old price were received
            q = quarter(idate) - 1
            if q >= 1:
                out[(p, q)] += amt
            continue
        g = parts.get(r.delivery_ref.replace('DN', '', 1))
        tot = g.bottles.astype(int).sum()
        for d, b in zip(g.d, g.bottles.astype(int)):
            q = quarter(d)
            if q:
                out[(p, q)] += amt * b / tot
    return {('%s Q%d' % k): int(round(v / 10.0) * 10) for k, v in out.items()}


def gtin_each(g):
    body = '0' + g[1:13]
    s = sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(body))
    return body + str((10 - s % 10) % 10)


def backorder(mode):
    notes = pd.read_csv(T / 'wholesaler_backorder_notices.csv', dtype=str)
    items = pd.read_csv(T / 'wholesaler_item_list.csv', dtype=str).fillna('')
    reg = pd.read_csv(T / 'pack_register.csv', dtype=str)
    name = dict(zip(reg.ndc, reg['product']))
    g2n = dict(zip(reg.gtin, reg.ndc))
    lookup = dict(zip(items.item_no, items.ndc))
    if mode != 'mirror':
        lookup.update({f: n for f, n in zip(items.former_item_no, items.ndc) if f and f not in lookup})
    ships = {}
    for s in json.loads((T / 'wholesaler_advance_ship_notices.json').read_text())['shipments']:
        d = pd.Timestamp(s['shipTimeUtc']).tz_convert(PT).date()
        for ln in s['lines']:
            g = ln['gtin']
            n = g2n.get(g)
            if n is None and mode == 'cracker':
                n = g2n.get(gtin_each(g))
            if n is not None:
                ships.setdefault(n, []).append(d)
    out = {(p, q): 0 for p in GENS for q in (1, 2)}
    for r in notes.itertuples(index=False):
        n = lookup.get(r.item_no)
        if n is None:
            continue
        start = pd.Timestamp(r.opened_utc).tz_convert(PT).date()
        if mode == 'mirror':
            end = pd.Timestamp(r.expected_release).date()
        else:
            end = min(d for d in ships.get(n, [dt.date(2026, 7, 1)]) if d > start)
        d = start
        while d < end:
            q = quarter(d)
            if q:
                out[(name[n], q)] += 1
            d += dt.timedelta(days=1)
    return {('%s Q%d' % k): v for k, v in out.items()}


def score(resp, gold, unit):
    hits = [k for k in gold if abs(resp[k] - gold[k]) < unit / 2.0]
    return hits


def main():
    F = json.loads((TASK / 'generator' / 'figures.json').read_text())
    gs, gb = F['spend'], F['backorder_days']
    rows = {}
    for mode in ('cracker', 'full_includer', 'mirror'):
        s, b = spend(mode), backorder('cracker' if mode == 'cracker' else mode)
        hs, hb = score(s, gs, 10), score(b, gb, 1)
        rows[mode] = dict(spend_hits=hs, backorder_hits=hb, keep=(len(hs) + len(hb)) / (len(gs) + len(gb)))
    C = 38 + 7 + 55 * rows['cracker']['keep']
    S = 5 + 7 + 55 * rows['full_includer']['keep']
    both = (C + 38 + 7 + 55 * rows['full_includer']['keep']) / 2
    print('ask figures: spend %d, backorder days %d' % (len(gs), len(gb)))
    for m, r in rows.items():
        print('%-14s keeps %2d of %d (%.0f per cent)  spend kept: %s  backorder kept: %s' % (
            m, len(r['spend_hits']) + len(r['backorder_hits']), len(gs) + len(gb), 100 * r['keep'],
            ', '.join(r['spend_hits']) or 'none', ', '.join(r['backorder_hits']) or 'none'))
    print('pair ceiling (cracker on the call, full includer off it): %.1f' % ((C + S) / 2))
    print('pair with both on the call: %.1f' % both)
    print('pair with two crackers on the call: %.1f' % C)
    print('mirror leakage: %.1f per cent of ask weight' % (100 * rows['mirror']['keep']))
    print('cracker misses ask 1: %s; misses ask 2: %s' % (len(rows['cracker']['spend_hits']) < len(gs),
                                                          len(rows['cracker']['backorder_hits']) < len(gb)))
    return rows


if __name__ == '__main__':
    main()
