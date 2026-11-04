"""The ask side of task211's world: the wholesaler's deliveries, invoices, price adjustments, backorder notices and
shipment notices, and the distribution centres' receiving log. Clean truth; device rows placed so each moves only
its own block of figures."""
import datetime as dt
import numpy as np
import pandas as pd
from world import SEED, DCS

GENERICS = [1, 2, 3, 4, 5]
PRICE_OLD = {1: 8.40, 2: 7.95, 3: 9.65, 4: 6.85, 5: 7.20}        # per bottle of 100, invoiced to 2026-03-31
PRICE_NEW = {1: 8.15, 2: 8.35, 3: 9.35, 4: 7.25, 5: 7.55}        # amended contract prices (2, 4, 5 rose; 1, 3 fell)
SHIP_WEEKDAY = {1: 0, 3: 1, 2: 2, 4: 3, 5: 3}                    # Halvorne ships Mondays, Corwen Tuesdays ...
MIGRATION = dt.date(2026, 3, 2)                                   # the wholesaler's ERP cut-over
# wholesaler backorders: (product, opened local datetime, next shipment date, that shipment is a full case)
WBO = [(1, dt.datetime(2026, 1, 12, 9, 40), dt.date(2026, 1, 26), True),
       (4, dt.datetime(2026, 1, 5, 11, 15), dt.date(2026, 1, 15), True),
       (5, dt.datetime(2026, 1, 15, 8, 20), dt.date(2026, 1, 27), False),
       (2, dt.datetime(2026, 2, 1, 19, 10), dt.date(2026, 5, 4), False),
       (4, dt.datetime(2026, 2, 26, 21, 30), dt.date(2026, 4, 10), True),
       (3, dt.datetime(2026, 3, 9, 14, 5), dt.date(2026, 3, 20), True),
       (5, dt.datetime(2026, 4, 20, 10, 55), dt.date(2026, 5, 7), True),
       (1, dt.datetime(2026, 5, 18, 7, 50), dt.date(2026, 6, 1), True),
       (3, dt.datetime(2026, 6, 1, 16, 45), dt.date(2026, 6, 12), True)]
# wholesaler item numbers before the cut-over and after it: 448193 is reissued from Pellbrook to Wynfield
ITEM_OLD = {1: '447120', 2: '448193', 3: '446507', 4: '449028', 5: '447650'}
ITEM_NEW = {1: '552318', 2: '552901', 3: '447120', 4: '553082', 5: '448193'}    # 447120 and 448193 reissued
MEAN_PACKS = {1: 360, 2: 264, 3: 156, 4: 324, 5: 204}          # bottles a size-1 centre orders a week
# while a generic is out, its pharmacies dispense the look-alike, and the centres order it in its place
SUBS = [(2, 1, dt.date(2026, 2, 2), dt.date(2026, 5, 4)), (4, 5, dt.date(2026, 2, 27), dt.date(2026, 4, 10))]
DC_SIZE = [1.25, 0.8, 1.1, 1.0, 0.9, 0.7, 0.7]
HOLIDAYS = {dt.date(2025, 12, 25), dt.date(2026, 1, 1), dt.date(2026, 5, 25)}
# each amendment reaches back to deliveries dispatched from AMEND_FROM; invoices from PRICE_SWITCH carry the new price,
# and the first of them carries the catch-up for the bottles invoiced at the old price since AMEND_FROM
AMEND_FROM = {1: dt.date(2026, 2, 9), 2: dt.date(2025, 12, 1), 3: dt.date(2026, 2, 9), 4: dt.date(2025, 12, 1), 5: dt.date(2025, 12, 1)}
PRICE_SWITCH = {1: dt.date(2026, 6, 15), 2: dt.date(2026, 5, 25), 3: dt.date(2026, 6, 15), 4: dt.date(2026, 4, 27),
                5: dt.date(2026, 4, 27)}
ADJ_DATE = {p: d + dt.timedelta(days=4) for p, d in PRICE_SWITCH.items()}


def next_business(d):
    while d.weekday() >= 5 or d in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def simulate_asks(seed=SEED):
    rng = np.random.default_rng(seed + 7)
    used = set()

    def new_dn():
        while True:
            n = int(rng.integers(3100000, 4999999))
            if n not in used:
                used.add(n)
                return n
    out = {p: [(o.date(), nxt) for (q, o, nxt, c) in WBO if q == p] for p in GENERICS}
    rows = []
    d = dt.date(2025, 10, 1)
    while d <= dt.date(2026, 7, 3):
        if d.weekday() < 5 and d not in HOLIDAYS:
            for p in GENERICS:
                if d.weekday() != SHIP_WEEKDAY[p] or any(a <= d <= b for (a, b) in out[p]):
                    continue
                for k in range(len(DCS)):
                    mean = MEAN_PACKS[p] + sum(MEAN_PACKS[q] for (q, sub, a, b) in SUBS if sub == p and a <= d < b)
                    packs = int(rng.poisson(mean * DC_SIZE[k]))
                    if packs:
                        recv = next_business(d + dt.timedelta(days=1 if k < 4 else 2))
                        rows.append(dict(p=p, dc=k, dispatch=d, delivery=new_dn(), packs=packs, recv=recv, recv2=None,
                                         packs2=0, first_after=False, case=False))
        d += dt.timedelta(days=1)
    for (p, opened, nxt, case) in WBO:                 # the first shipment after each backorder
        k = int(rng.integers(0, 4))
        packs = 12 * int(rng.integers(20, 51)) if case else int(rng.integers(110, 230))
        rows.append(dict(p=p, dc=k, dispatch=nxt, delivery=new_dn(), packs=packs,
                         recv=next_business(nxt + dt.timedelta(days=1)), recv2=None, packs2=0, first_after=True, case=case))
    dl = pd.DataFrame(rows)
    # Corwen's deliveries dispatched 2026-03-31 to the two nearest centres arrive in two parts, the first that day
    for j in dl.index[(dl.p == 3) & (dl.dispatch == dt.date(2026, 3, 31)) & (dl.dc.isin([0, 2]))]:
        n = int(dl.loc[j, 'packs'])
        dl.loc[j, 'recv'] = dt.date(2026, 3, 31)
        dl.loc[j, 'recv2'] = dt.date(2026, 4, 2)
        dl.loc[j, 'packs2'] = n - n // 2 - 3
    # ordinary two-part receipts inside a quarter, every product
    ok = dl.index[(dl.dispatch > dt.date(2026, 1, 12)) & (dl.dispatch < dt.date(2026, 6, 10)) & ~dl.first_after
                  & dl.recv2.isna()]
    for j in rng.choice(ok, size=34, replace=False):
        r = dl.loc[j, 'recv']
        r2 = next_business(r + dt.timedelta(days=int(rng.integers(1, 4))))
        if (r.month - 1) // 3 == (r2.month - 1) // 3 and r2.year == r.year and dl.loc[j, 'packs'] >= 6:
            dl.loc[j, 'recv2'] = r2
            dl.loc[j, 'packs2'] = int(rng.integers(1, dl.loc[j, 'packs'] // 2 + 1))
    dl = dl.sort_values(['dispatch', 'dc', 'p', 'delivery']).reset_index(drop=True)
    dl['packs1'] = dl['packs'] - dl['packs2']
    # three placements settle together: every spend figure of Halvorne and Corwen moves at least four bins between
    # invoice and receipt dating, each centre's first-quarter receipts of a generic whose price rose differ from its
    # other quarters' receipts, and every quarter's spend sits clear of a ten-dollar edge
    for _ in range(600):
        mv = d8_moves(dl)
        small = [k for k, v in sorted(mv.items()) if abs(v) < 40]
        if small:
            p, q = small[0]
            sign = 1 if mv[(p, q)] >= 0 else -1
            cand = boundary_rows(dl, p, q, sign) or boundary_rows(dl, p, q, -sign)
            j = cand[0]
            dl.loc[j, 'packs'] += 3
            dl.loc[j, 'packs1'] += 3
            continue
        col = collisions(dl)
        if col:
            p, k, (y, qq) = col[0]
            lo = dt.date(y, 3 * qq - 2, 1) + dt.timedelta(days=10)
            hi = (dt.date(y, 3 * qq, 1) + dt.timedelta(days=20))
            free = [j for j, r in zip(dl.index, dl.itertuples(index=False)) if r.p == p and r.dc == k and not r.first_after
                    and r.recv2 is None and lo <= r.recv <= hi and not covered(r)]
            if not free:            # every bottle of that quarter is covered: a covered December delivery takes one more
                free = [j for j, r in zip(dl.index, dl.itertuples(index=False)) if r.p == p and r.dc == k and covered(r)
                        and r.recv2 is None and r.recv < dt.date(2026, 1, 1)]
            dl.loc[free[0], 'packs'] += 1
            dl.loc[free[0], 'packs1'] += 1
            continue
        sp = spend_world(dl)
        off = [k for k, v in sorted(sp.items()) if abs(v - round(v / 10.0) * 10) > 4.3]
        if off:
            p, q = off[0]
            lo, hi = (dt.date(2026, 1, 12), dt.date(2026, 3, 20)) if q == 1 else (dt.date(2026, 4, 13), dt.date(2026, 6, 19))
            j = dl.index[(dl.p == p) & ~dl.first_after & dl.recv2.isna() & (dl.recv >= lo) & (dl.recv <= hi)][0]
            dl.loc[j, 'packs'] += 1
            dl.loc[j, 'packs1'] += 1
            continue
        break
    else:
        raise AssertionError('the ask placements did not settle')
    return dl


def receipt_parts(dl):
    for r in dl.itertuples(index=False):
        for d, pk in ((r.recv, r.packs1), (r.recv2, r.packs2)):
            if d is not None and pk:
                yield r, d, int(pk)


def covered(r):
    """A delivery the price amendment reaches: a generic whose price rose, dispatched from AMEND_FROM and invoiced at
    the old price."""
    return r.dispatch >= AMEND_FROM[r.p] and invoice_date(r.dispatch) < PRICE_SWITCH[r.p]


def collisions(dl):
    """(generic, centre, quarter) where the bottles a centre's catch-up covers equal its receipts of that generic in a
    calendar quarter, a reading that would place the catch-up in one quarter."""
    tot, cov = {}, {}
    for r, d, pk in receipt_parts(dl):
        if True:
            t = tot.setdefault((r.p, r.dc), {})
            cq = (d.year, (d.month - 1) // 3 + 1)
            t[cq] = t.get(cq, 0) + pk
    for r in dl.itertuples(index=False):
        if covered(r):
            cov[(r.p, r.dc)] = cov.get((r.p, r.dc), 0) + int(r.packs)
    out = []
    for key, t in sorted(tot.items()):
        for cq, b in sorted(t.items()):
            if b == cov.get(key):
                out.append((key[0], key[1], cq))
    return out


def d8_moves(dl):
    """Spend by invoice date less spend by receipt day, for the two generics whose price did not move."""
    inv = {(p, q): 0.0 for p in (1, 3) for q in (1, 2)}
    rec = dict(inv)
    for r in dl.itertuples(index=False):
        if r.p not in (1, 3):
            continue
        amt = round(r.packs * (PRICE_OLD[r.p] if invoice_date(r.dispatch) < PRICE_SWITCH[r.p] else PRICE_NEW[r.p]), 2)
        qi = quarter(invoice_date(r.dispatch))
        if qi:
            inv[(r.p, qi)] += amt
        for d, pk in ((r.recv, r.packs1), (r.recv2, r.packs2)):
            if d is not None and pk and quarter(d):
                rec[(r.p, quarter(d))] += amt * pk / r.packs
    return {k: inv[k] - rec[k] for k in inv}


def boundary_rows(dl, p, q, sign):
    """Ordinary deliveries of p whose invoice quarter is q and receipt quarter is not (sign 1), or the reverse."""
    out = []
    for j, r in zip(dl.index, dl.itertuples(index=False)):
        if r.p != p or r.first_after:
            continue
        qi, qr = quarter(invoice_date(r.dispatch)), quarter(r.recv)
        if (sign > 0 and qi == q and qr != q) or (sign < 0 and qr == q and qi != q):
            out.append(j)
    return out


def invoice_date(d):
    return next_business(d - dt.timedelta(days=d.weekday()) + dt.timedelta(days=4))


def quarter(d):
    if dt.date(2026, 1, 1) <= d <= dt.date(2026, 3, 31):
        return 1
    if dt.date(2026, 4, 1) <= d <= dt.date(2026, 6, 30):
        return 2
    return 0


def spend_world(dl):
    """Each delivery's invoiced amount and its share of the catch-up, in the quarters its bottles were received in."""
    sp = {(p, q): 0.0 for p in GENERICS for q in (1, 2)}
    for r in dl.itertuples(index=False):
        idate = invoice_date(r.dispatch)
        price = PRICE_OLD[r.p] if idate < PRICE_SWITCH[r.p] else PRICE_NEW[r.p]
        amt = round(r.packs * price, 2)
        if covered(r):
            amt += r.packs * round(PRICE_NEW[r.p] - PRICE_OLD[r.p], 2)
        for d, pk in ((r.recv, r.packs1), (r.recv2, r.packs2)):
            if d is not None and pk and quarter(d):
                sp[(r.p, quarter(d))] += amt * pk / r.packs
    return sp
