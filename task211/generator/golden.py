"""task211 golden: everything computed from target/ alone (the shipped files), never from the generator's world.
load() rebuilds each patient's supply and clocks; excess() fits MS-12 2.6's comparison; asks() computes the asks."""
import datetime as dt, json, os, re, sys, zoneinfo
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm
from pypdf import PdfReader

TASK = Path(__file__).resolve().parent.parent
TARGET = Path(os.environ.get('T211_TARGET', str(TASK / 'target')))
SCREEN = 'T211_TARGET' in os.environ
PT = zoneinfo.ZoneInfo('America/Los_Angeles')
D0 = dt.date(2025, 4, 1)                     # first day of the claims extract
WS, WE = dt.date(2026, 1, 1), dt.date(2026, 6, 30)
NDAY = (WE - D0).days + 1
w0, w1 = (WS - D0).days, (WE - D0).days
REF = 'Levaril'
BIG = 10**6


def pdf_text(name):
    return '\n'.join(p.extract_text() for p in PdfReader(str(TARGET / name)).pages)


def facts():
    """The appearance facts the pack files: the register's descriptions and the two manufacturers' supply dates."""
    reg = pd.read_excel(TARGET / 'product_register.xlsx')
    hal = pdf_text('halvorne_site_change_notice.pdf')
    dc_dates = {}
    for m in re.finditer(r'([A-Z][A-Za-z ]+?) DC\s+(\d{1,2} [A-Z][a-z]+ \d{4})', hal):
        dc_dates[m.group(1).strip() + ' DC'] = dt.datetime.strptime(m.group(2), '%d %B %Y').date()
    cor = pdf_text('corwen_film_coat_notice.pdf')
    m = re.search(r'from (\d{1,2} [A-Z][a-z]+ \d{4}) carries the beige', cor.replace('\n', ' '))
    cor_date = dt.datetime.strptime(m.group(1), '%d %B %Y').date()
    desc = {}
    for r in reg.itertuples(index=False):
        desc.setdefault(r.product, []).append((r.manufactured_by, r.description.split(',')[0].strip().lower(), r.description))
    return reg, dc_dates, cor_date, desc


def appearance(product, centre, d, dc_dates, cor_date, desc):
    """The full description of the tablet a fill supplied (MS-12 reads colour, shape and debossing together)."""
    rows = desc[product]
    if product == 'Halvorne':
        return rows[1][2] if d >= dc_dates[centre] else rows[0][2]
    if product == 'Corwen':
        return rows[1][2] if d >= cor_date else rows[0][2]
    return rows[0][2]


def load_claims(keep_reversed=False):
    c = pq.read_table(TARGET / 'dispensing_claims_2025-04_to_2026-06.parquet').to_pandas()
    xw = pd.read_csv(TARGET / 'claims_item_crosswalk.csv', dtype=str)
    reversed_ids = set(c.loc[c.claim_status == 'REVERSED', 'reversal_of'])
    fills = c[(c.claim_status == 'PAID') & (keep_reversed | ~c.claim_id.isin(reversed_ids))].copy()
    code2prod = dict(zip(xw.item_code, xw['product'])) | dict(zip(xw.ndc, xw['product']))
    fills['product'] = fills.product_code.map(code2prod)
    fills['service_date'] = pd.to_datetime(fills.service_date).dt.date
    return c, fills


def load(keep_reversed=False, overlap='later', utc_partner=False, transfers_once=True, age_year=2026, merged_linked=True):
    """The golden reading by default; each keyword is one operationalisation the variant table in checks.py measures."""
    reg, dc_dates, cor_date, desc = facts()
    c, fills = load_claims(keep_reversed)
    ph = pd.read_csv(TARGET / 'pharmacies.csv', dtype=str).set_index('pharmacy_id')['distribution_centre']
    fills['centre'] = fills.pharmacy_id.map(ph)
    fills['look'] = [appearance(p, cn, d, dc_dates, cor_date, desc) for p, cn, d in
                     zip(fills['product'], fills['centre'], fills['service_date'])]
    fills['colour'] = fills['look'].str.split(',').str[0].str.lower()
    fills = fills.sort_values(['member_id', 'service_date', 'claim_id']).reset_index(drop=True)
    members = pd.read_csv(TARGET / 'members.csv', dtype={'member_id': str})
    mids = members.member_id.tolist()
    midx = {m: i for i, m in enumerate(mids)}
    prods = [REF, 'Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']
    pidx = {p: i for i, p in enumerate(prods)}
    N = len(mids)
    cover = np.full((N, NDAY), -1, dtype=np.int8)
    clocks = {k: np.full((N, NDAY), BIG, dtype=np.int32) for k in ('tcol', 'tcolour_only', 'tsw', 'tnew', 'tnsf', 'tnaive')}
    newsite = np.zeros((N, NDAY), dtype=bool)
    first = np.zeros((N, NDAY), dtype=bool)
    first_colour = np.zeros((N, NDAY), dtype=bool)
    supply = np.zeros((N, NDAY), dtype=np.int16)
    ar = np.arange(NDAY)
    hal_reg = dt.date(2025, 9, 15)           # the register's approval date of the Fort Wayne description
    for m, g in fills.groupby('member_id', sort=False):
        i = midx[m]
        prev = None
        last = {k: -BIG for k in clocks}
        seen = {}
        end = -BIG
        for r in g.itertuples(index=False):
            s = (r.service_date - D0).days
            if overlap == 'carry' and s < end:
                s = end
            if s >= NDAY:
                continue
            e = min(s + int(r.days_supply), NDAY)
            end = e
            p = pidx[r.product]
            if prev is not None:
                if r.look != prev.look: last['tcol'] = s
                if r.colour != prev.colour: last['tcolour_only'] = s
                if r.product != prev.product: last['tsw'] = s
                nv = lambda x: ('pink' if x.service_date >= hal_reg else 'white') if x.product == 'Halvorne' else x.colour
                if nv(r) != nv(prev): last['tnaive'] = s
            if r.product not in seen:
                seen[r.product] = s if prev is not None else -BIG
            last['tnew'] = seen[r.product]
            ns = r.product == 'Halvorne' and r.colour == 'pink'
            if ns and last['tnsf'] == -BIG:
                last['tnsf'] = s
            cover[i, s:e] = p
            newsite[i, s:e] = ns
            first[i, s:e] = prev is not None and r.look != prev.look
            first_colour[i, s:e] = prev is not None and r.colour != prev.colour
            supply[i, s:e] = int(r.days_supply)
            for k in clocks:
                if last[k] > -BIG:
                    clocks[k][i, s:e] = ar[s:e] - last[k]
            prev = r
    # encounters: both feeds, Pacific dates, transfers once, first-listed qualifying diagnosis
    lk = pd.read_csv(TARGET / 'ed_encounters_larkhaven_hospitals.csv', dtype=str).fillna('')
    lk['t'] = pd.to_datetime(lk.arrival).dt.tz_localize(PT, ambiguous=False, nonexistent='shift_forward')
    lk['dx'] = lk.dx_1
    lk['src'] = 'own'
    pj = json.loads((TARGET / 'ed_encounters_partner_hospitals.json').read_text())['records']
    pt = pd.DataFrame(pj)
    pt = pd.DataFrame(dict(encounter_id=pt.encounterId, facility=pt.facilityName, mrn=pt.patientMrn,
                           t=pd.to_datetime(pt.arrivalUtc).dt.tz_convert(PT), dx=pt.diagnoses.str[0], disposition=pt.disposition, src='partner'))
    enc = pd.concat([lk[['encounter_id', 'facility', 'mrn', 't', 'dx', 'disposition', 'src']], pt], ignore_index=True)
    mx = pd.read_csv(TARGET / 'mrn_member_crosswalk.csv', dtype=str)
    if not merged_linked:
        mx = mx[mx.record_status != 'MERGED']
    mx = mx.set_index('mrn')['member_id']
    enc['member_id'] = enc.mrn.map(mx)
    enc = enc.sort_values(['member_id', 't']).reset_index(drop=True)
    drop = set()
    for m, g in enc.groupby('member_id', sort=False):
        rows = list(g.itertuples())
        for a in rows:
            if a.disposition.startswith('TRANSFER:'):
                dest = a.disposition.split(':', 1)[1]
                for b in rows:
                    if b.Index != a.Index and b.facility == dest and a.t < b.t <= a.t + pd.Timedelta(hours=24):
                        drop.add(b.Index)
                        break
    if transfers_once:
        enc = enc.drop(index=sorted(drop))
    enc['qual'] = enc.dx.str.startswith('G40') | (enc.dx == 'R56.9')
    enc['date'] = enc.t.dt.date
    if utc_partner:
        enc.loc[enc.src == 'partner', 'date'] = enc.loc[enc.src == 'partner', 't'].dt.tz_convert('UTC').dt.date
    q = enc[enc.qual & (enc.date >= WS) & (enc.date <= WE)]
    visits = np.zeros((N, NDAY), dtype=np.int16)
    q = q[q.member_id.notna()]
    for m, d in zip(q.member_id, q.date):
        visits[midx[m], (d - D0).days] += 1
    age = age_year - members.birth_year.to_numpy()
    band = np.where(age < 18, 0, np.where(age < 65, 1, 2))
    res = (members.drug_resistant_epilepsy == 'Y').to_numpy().astype(int)
    sl = slice(w0, w1 + 1)
    pack = dict(prods=prods, cover=cover[:, sl], visits=visits[:, sl], band=band, res=res, newsite=newsite[:, sl],
                first=first[:, sl], first_colour=first_colour[:, sl], supply=supply[:, sl],
                centre=None, fills=fills, enc=enc, mids=mids, dc_dates=dc_dates, cor_date=cor_date)
    for k in clocks:
        pack[k] = clocks[k][:, sl]
    # each member's distribution centre for the letter-date reader: the centre of the pharmacy of each Halvorne fill
    tlet = np.full((N, NDAY), BIG, dtype=np.int32)
    for r in fills[fills['product'] == 'Halvorne'].itertuples(index=False):
        i = midx[r.member_id]; s = (r.service_date - D0).days; e = min(s + int(r.days_supply), NDAY)
        sw = (dc_dates[r.centre] - D0).days
        seg = ar[s:e] - sw
        tlet[i, s:e] = np.where(seg >= 0, seg, BIG)
    pack['tlet'] = tlet[:, sl]
    return pack


def cells(pk, spec):
    shape = pk['cover'].shape
    on = pk['cover'] >= 0
    idx = np.zeros(shape, dtype=np.int64); mult = 1; sizes = []
    for name, arr, n in spec:
        idx += np.broadcast_to(arr, shape).astype(np.int64) * mult; mult *= n; sizes.append(n)
    E = np.bincount(idx[on], minlength=mult) / 30.4375
    O = np.bincount(idx[on], weights=pk['visits'][on].astype(float), minlength=mult)
    grid = np.array(np.unravel_index(np.arange(mult), sizes[::-1])).T[:, ::-1]
    m = E > 0
    return grid[m], E[m], O[m]


def base_spec(pk):
    return [('prod', np.where(pk['cover'] >= 0, pk['cover'], 0), 6), ('band', pk['band'][:, None], 3),
            ('res', pk['res'][:, None], 2)]


def excess(pk, extra=(), zero=('prod',)):
    """MS-12 2.6: observed visits less the visits the same patient-days would have had with the reference's tablets,
    per 1,000 patient-months of each product; terms in `extra` are held as they were."""
    spec = base_spec(pk) + list(extra)
    grid, E, O = cells(pk, spec)
    cols, names = [], []
    for j, (name, _, n) in enumerate(spec):
        for l in range(1, n):
            if (grid[:, j] == l).any():
                cols.append((grid[:, j] == l).astype(float)); names.append((name, l))
    X = sm.add_constant(np.column_stack(cols))
    fit = sm.GLM(O, X, family=sm.families.Poisson(), offset=np.log(E)).fit()
    out = {}
    for p in range(1, 6):
        m = grid[:, 0] == p
        Xcf = X[m].copy()
        for ci, (k, l) in enumerate(names):
            if k in zero:
                Xcf[:, ci + 1] = 0.0
        mu = fit.predict(X[m], offset=np.log(E[m])); mu0 = fit.predict(Xcf, offset=np.log(E[m]))
        out[pk['prods'][p]] = (mu.sum() - mu0.sum()) / E[m].sum() * 1000
    return out, fit


def golden_excess(pk):
    """The days a patient spends on the first fill of a tablet that looks different from their previous fill are held as
    they were; everything else about the tablets is the reference's."""
    return excess(pk, [('fs', pk['first'].astype(int), 2)])[0]


def product_counts(pk):
    out = {}
    for p in range(1, 6):
        m = pk['cover'] == p
        out[pk['prods'][p]] = dict(patient_months=m.sum() / 30.4375, visits=int(pk['visits'][m].sum()))
    return out


# --------------------------------------------------------------------------------------------- the asks
def gtin_to_ndc(g, packs):
    each = dict(zip(packs.gtin.astype(str), packs.ndc))
    if g in each:
        return each[g]
    body = '0' + g[1:13]
    s = sum(int(ch) * (3 if i % 2 == 0 else 1) for i, ch in enumerate(body))
    return each.get(body + str((10 - s % 10) % 10))


def asks(by_invoice=False):
    inv = pd.read_csv(TARGET / 'wholesaler_invoice_lines.csv', dtype={'invoice_no': str, 'delivery_ref': str}).fillna({'delivery_ref': ''})
    rec = pd.read_csv(TARGET / 'dc_receiving_log.csv', dtype={'delivery_no': str})
    acct = pd.read_csv(TARGET / 'wholesaler_ship_to_accounts.csv').set_index('ship_to')['centre']
    packs = pd.read_csv(TARGET / 'pack_register.csv', dtype=str)
    ndc2p = dict(zip(packs.ndc, packs['product']))
    rec['received'] = pd.to_datetime(rec.received).dt.date
    inv['invoice_date'] = pd.to_datetime(inv.invoice_date).dt.date
    qtr = lambda d: 1 if WS <= d <= dt.date(2026, 3, 31) else (2 if dt.date(2026, 4, 1) <= d <= WE else 0)
    spend = {(p, q): 0.0 for p in ndc2p.values() for q in (1, 2)}
    rq = rec.assign(q=rec.received.map(qtr), cq=rec.received.map(lambda d: '%dQ%d' % (d.year, (d.month - 1) // 3 + 1)))
    by_dn = rq.groupby('delivery_no')
    deliv = inv[inv.delivery_ref != '']
    for r in deliv.itertuples(index=False):
        if by_invoice:                       # the receipt-day device's measure: each delivery line by its invoice date
            if qtr(r.invoice_date):
                spend[(ndc2p[r.ndc], qtr(r.invoice_date))] += r.amount
            continue
        g = by_dn.get_group(r.delivery_ref[2:])
        tot = g.bottles.sum()
        for q, b in g.groupby('q').bottles.sum().items():
            if q:
                spend[(ndc2p[r.ndc], q)] += r.amount * b / tot
    # later amounts for bottles already received (7.3): an adjustment line names a centre, a generic and a bottle count;
    # its bottles are that centre's last bottles of the generic invoiced before it, counted back line by line until they
    # make up its count exactly, and its amount goes with each of those bottles to the quarter it was received in
    recq = rq.groupby(['centre', 'ndc', 'cq']).bottles.sum()
    adj_q = {}
    for r in inv[inv.delivery_ref == ''].itertuples(index=False):
        cen = acct[r.ship_to]
        lines = deliv[(deliv.ship_to == r.ship_to) & (deliv.ndc == r.ndc) & (deliv.invoice_date < r.invoice_date)]
        lines = lines.sort_values(['invoice_date', 'ship_date', 'delivery_ref'], ascending=False)
        run = lines.bottles.cumsum()
        hit = int((run == r.bottles).sum())
        assert hit == 1, (r, hit)
        cov = lines[run <= r.bottles]
        assert int(cov.bottles.sum()) == r.bottles
        assert not [cq for (c2, n2, cq), b in recq.items() if c2 == cen and n2 == r.ndc and b == r.bottles], r
        adj_q[(cen, r.ndc)] = (str(cov.ship_date.min()), str(cov.ship_date.max()), len(cov))
        for c in cov.itertuples(index=False):
            g = by_dn.get_group(c.delivery_ref[2:])
            for q, b in g.groupby('q').bottles.sum().items():
                if q:
                    spend[(ndc2p[r.ndc], q)] += b * r.unit_price
    # backorder days
    notes = pd.read_csv(TARGET / 'wholesaler_backorder_notices.csv', dtype={'item_no': str})
    items = pd.read_csv(TARGET / 'wholesaler_item_list.csv', dtype=str).fillna('')
    eff = pd.to_datetime(items.effective.iloc[0]).date()
    cur = dict(zip(items.item_no, items.ndc))
    former = {f: n for f, n in zip(items.former_item_no, items.ndc) if f}
    no_former = [n for f, n in zip(items.former_item_no, items.ndc) if not f]
    asn = json.loads((TARGET / 'wholesaler_advance_ship_notices.json').read_text())['shipments']
    ships = {}
    for s in asn:
        d = pd.Timestamp(s['shipTimeUtc']).tz_convert(PT).date()
        for ln in s['lines']:
            ships.setdefault(gtin_to_ndc(ln['gtin'], packs), []).append(d)
    days = {(p, q): 0 for p in ndc2p.values() for q in (1, 2)}
    resolved = []
    for r in notes.itertuples(index=False):
        start = pd.Timestamp(r.opened_utc).tz_convert(PT).date()
        if start >= eff:
            ndc = cur[r.item_no]
        elif r.item_no in former:
            ndc = former[r.item_no]
        else:
            nxt_of = {n: min(d for d in ships[n] if d > start) for n in no_former}
            order = sorted(no_former, key=lambda n: nxt_of[n], reverse=True)
            assert nxt_of[order[0]] > nxt_of[order[1]] + dt.timedelta(days=6), (r, nxt_of)
            ndc = order[0]
        nxt = min(d for d in ships[ndc] if d > start)
        resolved.append((r.notice_no, ndc2p[ndc], start, nxt))
        d = start
        while d < nxt:
            q = qtr(d)
            if q:
                days[(ndc2p[ndc], q)] += 1
            d += dt.timedelta(days=1)
    return spend, days, adj_q, resolved


def main():
    pk = load()
    G = golden_excess(pk)
    counts = product_counts(pk)
    gens = ['Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']
    rank = sorted(gens, key=lambda p: -G[p])
    spend, days, adj_q, resolved = asks()
    F = dict(call=rank[0] if G[rank[0]] >= 2.0 else 'none', call_excess=int(round(G[rank[0]])), referral_bar=2.0,
             rate_base=1000, age_band_edges=[18, 64, 65], filed_sections=['2.3', '2.4', '2.5', '2.6', '3.1', '7.3'],
             excess_raw={p: G[p] for p in gens},
             patient_months={p: int(round(counts[p]['patient_months'] / 10.0) * 10) for p in gens},
             patient_months_raw={p: counts[p]['patient_months'] for p in gens},
             visits={p: counts[p]['visits'] for p in gens},
             spend={'%s Q%d' % k: int(round(v / 10.0) * 10) for k, v in sorted(spend.items()) if k[0] in gens},
             spend_raw={'%s Q%d' % k: v for k, v in sorted(spend.items()) if k[0] in gens},
             backorder_days={'%s Q%d' % k: v for k, v in sorted(days.items()) if k[0] in gens})
    if not SCREEN:
        (TASK / 'generator' / 'figures.json').write_text(json.dumps(F, indent=1, default=str) + '\n')
    return pk, F


if __name__ == '__main__':
    pk, F = main()
    print(json.dumps({k: v for k, v in F.items() if not k.endswith('_raw')}, indent=1, default=str))
