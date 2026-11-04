"""task211 independent verifier: recomputes every graded figure from target/ alone, with its own parsing, and
compares with figures.json. No generator module is imported. Exit 1 on any mismatch."""
import datetime as dt, json, re, sys
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm
from pypdf import PdfReader

TASK = Path(__file__).resolve().parent.parent
T = TASK / 'target'
PT = ZoneInfo('America/Los_Angeles')
WS, WE = dt.date(2026, 1, 1), dt.date(2026, 6, 30)
GENS = ['Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']
bad = []


def text(n):
    return ' '.join(p.extract_text() for p in PdfReader(str(T / n)).pages)


def asks(F):
    inv = pd.read_csv(T / 'wholesaler_invoice_lines.csv', dtype=str).fillna('')
    rec = pd.read_csv(T / 'dc_receiving_log.csv', dtype=str)
    acct = pd.read_csv(T / 'wholesaler_ship_to_accounts.csv', dtype=str).set_index('ship_to').centre
    reg = pd.read_csv(T / 'pack_register.csv', dtype=str)
    name = dict(zip(reg.ndc, reg['product']))
    rec['d'] = pd.to_datetime(rec.received).dt.date
    rec['b'] = rec.bottles.astype(int)
    rec['cq'] = [(x.year, (x.month - 1) // 3 + 1) for x in rec.d]
    q2026 = {(2026, 1): 1, (2026, 2): 2}
    sp = {}
    for r in inv.itertuples(index=False):
        p = name[r.ndc]
        if p not in GENS:
            continue
        if r.delivery_ref:
            g = rec[rec.delivery_no == r.delivery_ref[2:]]
            for cq, b in g.groupby('cq').b.sum().items():
                if cq in q2026:
                    sp[(p, q2026[cq])] = sp.get((p, q2026[cq]), 0) + float(r.amount) * b / g.b.sum()
        else:
            # walk back over the same ship-to's earlier lines of this NDC, newest first, until the bottles add up
            prior = inv[(inv.ship_to == r.ship_to) & (inv.ndc == r.ndc) & (inv.delivery_ref != '')].copy()
            prior['idate'] = pd.to_datetime(prior.invoice_date)
            prior = prior[prior.idate < pd.Timestamp(r.invoice_date)].sort_values(['idate', 'ship_date', 'delivery_ref'], ascending=False)
            need, used = int(r.bottles), []
            for x in prior.itertuples(index=False):
                if need <= 0:
                    break
                used.append(x); need -= int(x.bottles)
            if need != 0:
                bad.append('price amount on %s does not close on a delivery' % r.invoice_no)
                continue
            for x in used:
                g = rec[rec.delivery_no == x.delivery_ref[2:]]
                for cq, b in g.groupby('cq').b.sum().items():
                    if cq in q2026:
                        sp[(p, q2026[cq])] = sp.get((p, q2026[cq]), 0) + float(r.unit_price) * b
    for p in GENS:
        for q in (1, 2):
            if int(round(sp.get((p, q), 0) / 10.0) * 10) != F['spend']['%s Q%d' % (p, q)]:
                bad.append('spend %s Q%d: %.2f' % (p, q, sp.get((p, q), 0)))
    notes = pd.read_csv(T / 'wholesaler_backorder_notices.csv', dtype=str)
    items = pd.read_csv(T / 'wholesaler_item_list.csv', dtype=str).fillna('')
    cut = pd.Timestamp(items.effective.iloc[0]).date()
    each = dict(zip(reg.gtin, reg.ndc))
    def ndc_of(g):
        if g in each:
            return each[g]
        b = '0' + g[1:13]
        return each.get(b + str((10 - sum(int(ch) * (3 if k % 2 == 0 else 1) for k, ch in enumerate(b)) % 10) % 10))
    out = {}
    for s in json.loads((T / 'wholesaler_advance_ship_notices.json').read_text())['shipments']:
        for ln in s['lines']:
            out.setdefault(ndc_of(ln['gtin']), []).append(pd.Timestamp(s['shipTimeUtc']).tz_convert(PT).date())
    days = {}
    for r in notes.itertuples(index=False):
        start = pd.Timestamp(r.opened_utc).tz_convert(PT).date()
        if start >= cut:
            n = items.set_index('item_no').ndc[r.item_no]
        else:
            hit = items[items.former_item_no == r.item_no]
            if len(hit):
                n = hit.ndc.iloc[0]
            else:                            # of the products with no former number, the one that stopped shipping
                cands = list(items[items.former_item_no == ''].ndc)
                n = max(cands, key=lambda c: min(x for x in out[c] if x > start))
        end = min(x for x in out[n] if x > start)
        d = start
        while d < end:
            q = 1 if dt.date(2026, 1, 1) <= d <= dt.date(2026, 3, 31) else (2 if dt.date(2026, 4, 1) <= d <= WE else 0)
            if q:
                days[(name[n], q)] = days.get((name[n], q), 0) + 1
            d += dt.timedelta(days=1)
    for p in GENS:
        for q in (1, 2):
            if days.get((p, q), 0) != F['backorder_days']['%s Q%d' % (p, q)]:
                bad.append('backorder %s Q%d: %d' % (p, q, days.get((p, q), 0)))


def main():
    F = json.loads((TASK / 'generator' / 'figures.json').read_text())
    # the tablet each fill supplied
    reg = pd.read_excel(T / 'product_register.xlsx')
    looks = {p: list(g.sort_values('approved').description) for p, g in reg.groupby('product')}
    hal = text('halvorne_site_change_notice.pdf')
    centre_day = {m.group(1) + ' DC': dt.datetime.strptime(m.group(2), '%d %B %Y').date()
                  for m in re.finditer(r'([A-Z][A-Za-z ]+?) DC\s+(\d{1,2} [A-Z][a-z]+ \d{4})', hal)}
    cor_day = dt.datetime.strptime(re.search(r'from (\d{1,2} [A-Z][a-z]+ \d{4}) carries', text('corwen_film_coat_notice.pdf')).group(1), '%d %B %Y').date()
    c = pq.read_table(T / 'dispensing_claims_2025-04_to_2026-06.parquet').to_pandas()
    gone = set(c.loc[c.claim_status == 'REVERSED', 'reversal_of'])
    c = c[(c.claim_status == 'PAID') & ~c.claim_id.isin(gone)].copy()
    xw = pd.read_csv(T / 'claims_item_crosswalk.csv', dtype=str)
    prod_of = {**dict(zip(xw.ndc, xw['product'])), **dict(zip(xw.item_code, xw['product']))}
    c['p'] = c.product_code.map(prod_of)
    c['d'] = pd.to_datetime(c.service_date).dt.date
    centre = pd.read_csv(T / 'pharmacies.csv', dtype=str).set_index('pharmacy_id').distribution_centre
    c['cen'] = c.pharmacy_id.map(centre)

    def look(p, cen, d):
        if p == 'Halvorne':
            return looks[p][1] if d >= centre_day[cen] else looks[p][0]
        if p == 'Corwen':
            return looks[p][1] if d >= cor_day else looks[p][0]
        return looks[p][0]
    c['look'] = [look(p, k, d) for p, k, d in zip(c.p, c.cen, c.d)]
    c = c.sort_values(['member_id', 'd', 'claim_id'])
    origin = dt.date(2025, 4, 1)
    nd = (WE - origin).days + 1
    lo = (WS - origin).days
    mem = pd.read_csv(T / 'members.csv', dtype={'member_id': str})
    idx = {m: i for i, m in enumerate(mem.member_id)}
    prods = ['Levaril'] + GENS
    cov = np.full((len(mem), nd), -1, np.int8)
    first = np.zeros((len(mem), nd), bool)
    for m, g in c.groupby('member_id', sort=False):
        i = idx[m]; prev = None
        for r in g.itertuples(index=False):
            s = (r.d - origin).days
            e = min(s + int(r.days_supply), nd)
            cov[i, s:e] = prods.index(r.p)
            first[i, s:e] = prev is not None and r.look != prev
            prev = r.look
    cov, first = cov[:, lo:], first[:, lo:]
    # qualifying visits
    a = pd.read_csv(T / 'ed_encounters_larkhaven_hospitals.csv', dtype=str).fillna('')
    a['ts'] = pd.to_datetime(a.arrival).dt.tz_localize(PT, ambiguous=False, nonexistent='shift_forward')
    b = pd.DataFrame(json.loads((T / 'ed_encounters_partner_hospitals.json').read_text())['records'])
    b = pd.DataFrame(dict(facility=b.facilityName, mrn=b.patientMrn, ts=pd.to_datetime(b.arrivalUtc).dt.tz_convert(PT),
                          dx_1=b.diagnoses.str[0], disposition=b.disposition))
    e = pd.concat([a[['facility', 'mrn', 'ts', 'dx_1', 'disposition']], b], ignore_index=True)
    e['member'] = e.mrn.map(pd.read_csv(T / 'mrn_member_crosswalk.csv', dtype=str).set_index('mrn').member_id)
    e = e.sort_values(['member', 'ts']).reset_index(drop=True)
    dup = set()
    for m, g in e.groupby('member', sort=False):
        for x in g.itertuples():
            if x.disposition.startswith('TRANSFER:'):
                to = x.disposition[9:]
                nxt = g[(g.facility == to) & (g.ts > x.ts) & (g.ts <= x.ts + pd.Timedelta('24h'))]
                if len(nxt):
                    dup.add(nxt.index[0])
    e = e.drop(index=sorted(dup))
    e = e[(e.dx_1.str.startswith('G40') | (e.dx_1 == 'R56.9'))]
    e['day'] = e.ts.dt.date
    e = e[(e.day >= WS) & (e.day <= WE)]
    vis = np.zeros(cov.shape, np.int16)
    for m, d in zip(e.member, e.day):
        vis[idx[m], (d - WS).days] += 1
    for k, p in enumerate(prods[1:], start=1):
        on = cov == k
        pm, v = on.sum() / 30.4375, int(vis[on].sum())
        if int(round(pm / 10.0) * 10) != F['patient_months'][p] or v != F['visits'][p]:
            bad.append('counts %s: %.1f %d against %s %s' % (p, pm, v, F['patient_months'][p], F['visits'][p]))
    # the excess: product, a 90-day window after each appearance change, age band, drug-resistant epilepsy
    age = 2026 - mem.birth_year.to_numpy()
    band = np.where(age < 18, 0, np.where(age < 65, 1, 2))
    res = (mem.drug_resistant_epilepsy == 'Y').to_numpy().astype(int)
    on = cov >= 0
    key = (np.where(on, cov, 0).astype(np.int64) * 2 + first) * 6 + band[:, None] * 2 + res[:, None]
    E = np.bincount(key[on], minlength=72) / 30.4375
    O = np.bincount(key[on], weights=vis[on].astype(float), minlength=72)
    g = np.array([(k // 12, (k // 6) % 2, (k // 2) % 3, k % 2) for k in range(72)])
    keep = E > 0
    g, E, O = g[keep], E[keep], O[keep]
    X = np.column_stack([(g[:, 0] == p) for p in range(1, 6)] + [g[:, 1] == 1, g[:, 2] == 1, g[:, 2] == 2, g[:, 3] == 1]).astype(float)
    fit = sm.GLM(O, sm.add_constant(X), family=sm.families.Poisson(), offset=np.log(E)).fit()
    for p in range(1, 6):
        m = g[:, 0] == p
        X0 = X[m].copy(); X0[:, :5] = 0
        ex = (fit.predict(sm.add_constant(X, has_constant='add')[m], offset=np.log(E[m])).sum() -
              fit.predict(sm.add_constant(X0, has_constant='add'), offset=np.log(E[m])).sum()) / E[m].sum() * 1000
        if abs(ex - F['excess_raw'][prods[p]]) > 1e-6:
            bad.append('excess %s: %.6f against %.6f' % (prods[p], ex, F['excess_raw'][prods[p]]))
    asks(F)
    print('verify: %d mismatches' % len(bad))
    for x in bad:
        print('  ' + x)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
