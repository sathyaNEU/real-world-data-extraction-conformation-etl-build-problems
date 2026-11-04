"""task211 generator: writes target/ from the clean truth, then metadata.json and target.zip (sorted entries, one
fixed date and mode). Run: python3 build.py"""
import datetime as dt, json, os, sys, zipfile, zoneinfo
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa, pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import world as W
import askworld as A
import docs

TASK = HERE.parent
TARGET = Path(os.environ.get('T211_TARGET', str(TASK / 'target')))
PT = zoneinfo.ZoneInfo('America/Los_Angeles')
UTC = dt.timezone.utc
CUTOVER = dt.date(2025, 10, 6)                     # Larkhaven's claims platform go-live
CITIES = {0: ['Portland', 'Gresham', 'Troutdale', 'Fairview'], 1: ['Vancouver', 'Camas', 'Battle Ground', 'Longview'],
          2: ['Beaverton', 'Hillsboro', 'Tigard', 'Lake Oswego'], 3: ['Salem', 'Keizer', 'Albany', 'Woodburn'],
          4: ['Eugene', 'Springfield', 'Corvallis', 'Cottage Grove'], 5: ['Medford', 'Ashland', 'Grants Pass'],
          6: ['Bend', 'Redmond', 'Prineville', 'Sisters']}
HOSP = {0: ('LKH', 'Larkhaven Portland Medical Center'), 1: ('LKH', 'Larkhaven Vancouver Hospital'),
        2: ('LKH', 'Larkhaven Westside Hospital'), 3: ('LKH', 'Larkhaven Salem Hospital'),
        4: ('LKH', 'Larkhaven Eugene Hospital'), 5: ('PTN', 'Rogue Valley Regional Medical Center'),
        6: ('PTN', 'High Desert Medical Center')}
ENC_FROM = dt.datetime(2025, 12, 1)
SEIZ = ['G40.909', 'G40.909', 'G40.909', 'G40.919', 'G40.209', 'G40.309', 'G40.901', 'R56.9', 'R56.9', 'G40.409']
OTHER = ['S06.0X0A', 'J06.9', 'N39.0', 'R51.9', 'S01.01XA', 'R55', 'J18.9', 'K59.00', 'T42.6X1A', 'S52.501A',
         'R11.2', 'M54.50', 'J45.901', 'R07.9', 'E86.0']


def uniq_ints(rng, n, lo, hi):
    out = set()
    while len(out) < n:
        out.update(int(x) for x in rng.integers(lo, hi, size=n - len(out)))
    arr = np.array(sorted(out))
    rng.shuffle(arr)
    return arr


def build_main(S, rng):
    N, NPH = W.P['N'], W.P['NP']
    mids = ['M%08d' % x for x in uniq_ints(rng, N, 10_000_000, 99_999_999)]
    by = np.where(S['ageband'] == 0, rng.integers(2009, 2022, N), np.where(S['ageband'] == 1, rng.integers(1962, 2008, N),
                  rng.integers(1934, 1962, N)))
    members = pd.DataFrame(dict(member_id=mids, birth_year=by, sex=rng.choice(['F', 'M'], N),
                                drug_resistant_epilepsy=np.where(S['resistant'], 'Y', 'N')))
    # record numbers: one per member, a second for the members whose two charts were merged
    mrn = uniq_ints(rng, int(N * 1.04), 2_000_000, 9_999_999)
    second = rng.random(N) < 0.035
    rows, mrn_of, k = [], [], 0
    for i in range(N):
        a = int(mrn[k]); k += 1
        rows.append((str(a), mids[i], 'ACTIVE'))
        if second[i]:
            b = int(mrn[k]); k += 1
            rows.append((str(b), mids[i], 'MERGED'))
            mrn_of.append((str(a), str(b)))
        else:
            mrn_of.append((str(a), None))
    mrn_x = pd.DataFrame(rows, columns=['mrn', 'member_id', 'record_status']).sort_values('mrn').reset_index(drop=True)
    # pharmacies
    pids = ['RX%04d' % x for x in uniq_ints(rng, NPH, 1000, 9999)]
    names, cities = [], []
    for j in range(NPH):
        c = CITIES[int(S['ph_dc'][j])][int(rng.integers(0, len(CITIES[int(S['ph_dc'][j])])))]
        cities.append(c)
    count = {}
    for j in range(NPH):
        count[cities[j]] = count.get(cities[j], 0) + 1
        names.append('Larkhaven Pharmacy %s %d' % (cities[j], count[cities[j]]))
    pharm = pd.DataFrame(dict(pharmacy_id=pids, pharmacy_name=names, city=cities,
                              state=['WA' if S['ph_dc'][j] == 1 else 'OR' for j in range(NPH)],
                              distribution_centre=[W.DCS[int(S['ph_dc'][j])] + ' DC' for j in range(NPH)]))
    # claims: fills from 2025-04-01, reversals and resubmissions
    f = S['fills']
    f = f[f.day >= W.SHIP0].sort_values(['day', 'm']).reset_index(drop=True)
    tpd = np.where(rng.random(N) < 0.7, 2, 4)
    ids = uniq_ints(rng, int(len(f) * 1.08), 100_000_000_000, 999_999_999_999)
    k = 0; out = []
    rev = rng.random(len(f)) < 0.03
    for r, row in enumerate(f.itertuples(index=False)):
        d = W.date_of(row.day)
        src = 'RXL' if d < CUTOVER else 'LHC'
        code = W.PRODUCTS[row.p]['ndc'] if src == 'RXL' else W.PRODUCTS[row.p]['item']
        q = int(row.days_supply * tpd[row.m])
        base = dict(service_date=d, member_id=mids[row.m], pharmacy_id=pids[row.ph], source_system=src, product_code=code)
        if rev[r]:
            wrong_days = 30 if row.days_supply == 90 else 90
            orig = str(ids[k]); k += 1
            out.append(dict(base, claim_id=orig, quantity=int(wrong_days * tpd[row.m]), days_supply=wrong_days,
                            claim_status='PAID', reversal_of=None))
            out.append(dict(base, claim_id=str(ids[k]), quantity=-int(wrong_days * tpd[row.m]), days_supply=-wrong_days,
                            claim_status='REVERSED', reversal_of=orig)); k += 1
        out.append(dict(base, claim_id=str(ids[k]), quantity=q, days_supply=int(row.days_supply), claim_status='PAID',
                        reversal_of=None)); k += 1
    claims = pd.DataFrame(out)[['claim_id', 'source_system', 'service_date', 'member_id', 'pharmacy_id', 'product_code',
                                'quantity', 'days_supply', 'claim_status', 'reversal_of']]
    # emergency encounters, two feeds
    ev, oth = S['ev'], S['other']
    home_dc = S['ph_dc'][S['home']]
    hour_p = np.array([2, 1.5, 1.2, 1, 1, 1.2, 2, 3, 4, 5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.8, 6, 6, 5.5, 5, 4.5, 3.5, 2.5])
    hour_p = hour_p / hour_p.sum()
    enc = []
    for kind, arr in (('S', ev), ('O', oth)):
        ii, dd = np.nonzero(arr)
        for i, d0 in zip(ii, dd):
            for _ in range(int(arr[i, d0])):
                day_n = int(d0) + W.ENC0
                h = int(rng.choice(24, p=hour_p)); mi = int(rng.integers(0, 60))
                hdc = int(home_dc[i]) if rng.random() > 0.12 else int(rng.integers(0, 7))
                dd_ = W.date_of(day_n)
                # boundary days (the window's edges, and a day whose next day is covered by another product or another
                # fill's tablet): arrivals in the daytime, clear of every clock reading of the day
                turn = day_n + 1 < W.DAYS and (S['cover_prod'][i, day_n] != S['cover_prod'][i, day_n + 1] or
                                               S['first_new'][i, day_n] != S['first_new'][i, day_n + 1])
                if (dd_.month, dd_.day) in ((12, 31), (6, 30), (1, 1), (7, 1)) or turn:
                    h = 9 + h % 6
                loc = dt.datetime.combine(dd_, dt.time(h, mi))
                a, b = mrn_of[i]
                m_use = b if (b and rng.random() < 0.3) else a
                if kind == 'S':
                    dx = [SEIZ[int(rng.integers(0, len(SEIZ)))]] + list(rng.choice(OTHER, size=int(rng.integers(0, 3)), replace=False))
                else:
                    dx = [OTHER[int(rng.integers(0, len(OTHER)))]]
                    if rng.random() < 0.18:
                        dx.append(SEIZ[int(rng.integers(0, len(SEIZ)))])
                tr = kind == 'S' and rng.random() < 0.06
                enc.append(dict(i=i, mrn=m_use, local=loc, hdc=hdc, dx=dx, disp='TRANSFER' if tr else
                                str(rng.choice(['DISCHARGED', 'ADMITTED'], p=[0.72, 0.28])), kind=kind))
                if tr:
                    to = int(rng.choice([0, 3, 4])) if hdc not in (0, 3, 4) else int(rng.choice([x for x in (0, 3, 4) if x != hdc]))
                    enc[-1]['to'] = HOSP[to][1]
                    enc.append(dict(i=i, mrn=m_use, local=loc + dt.timedelta(minutes=int(rng.integers(150, 520))), hdc=to,
                                    dx=dx[:1] + list(rng.choice(OTHER, size=1)), disp='ADMITTED', kind='T'))
    eid_a = uniq_ints(rng, len(enc), 100_000_000, 999_999_999)
    lk, pt = [], []
    for n, e in enumerate(sorted(enc, key=lambda e: (e['local'], e['mrn']))):
        if e['local'] < ENC_FROM:          # the feeds are extracted from 1 December 2025
            continue
        sys_, fac = HOSP[e['hdc']]
        disp = e['disp'] + (':' + e['to'] if e['disp'] == 'TRANSFER' else '')
        if sys_ == 'LKH':
            lk.append(dict(encounter_id='E%09d' % eid_a[n], facility=fac, mrn=e['mrn'],
                           arrival=e['local'].strftime('%Y-%m-%d %H:%M'), dx_1=e['dx'][0],
                           dx_2=e['dx'][1] if len(e['dx']) > 1 else '', dx_3=e['dx'][2] if len(e['dx']) > 2 else '',
                           disposition=disp))
        else:
            u = e['local'].replace(tzinfo=PT).astimezone(UTC)
            pt.append(dict(encounterId='PV-%d' % eid_a[n], facilityName=fac, patientMrn=e['mrn'],
                           arrivalUtc=u.strftime('%Y-%m-%dT%H:%M:%SZ'), diagnoses=list(e['dx']), disposition=disp))
    return dict(members=members, mrn_x=mrn_x, pharm=pharm, claims=claims, enc_lk=pd.DataFrame(lk), enc_pt=pt,
                mids=mids, pids=pids)


def gtin(indicator, ndc11):
    lab, prod, pkg = ndc11.split('-')
    ndc10 = (lab + prod.lstrip('0').rjust(3, '0') + pkg) if prod.startswith('0') else (lab + prod + pkg[-1])
    body = str(indicator) + '03' + ndc10
    s = sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(body))
    return body + str((10 - s % 10) % 10)


def build_asks(dl, rng):
    dcs = ['LH-DC-%02d' % x for x in (11, 14, 17, 22, 26, 31, 35)]
    # invoices: one per centre per week, dated the week's Friday (or the next business day)
    dl = dl.copy()
    dl['week'] = dl['dispatch'].map(lambda d: d - dt.timedelta(days=d.weekday()))
    inv_no = {}
    nums = uniq_ints(rng, 400, 7_100_000, 7_999_999)
    lines, n = [], 0
    for (wk, k), g in dl.groupby(['week', 'dc'], sort=True):
        if (wk, k) not in inv_no:
            inv_no[(wk, k)] = int(nums[n]); n += 1
        idate = A.next_business(wk + dt.timedelta(days=4))
        for ln, r in enumerate(g.sort_values(['dispatch', 'p']).itertuples(index=False), start=1):
            price = A.PRICE_OLD[r.p] if idate < A.PRICE_SWITCH[r.p] else A.PRICE_NEW[r.p]
            lines.append(dict(invoice_no=str(inv_no[(wk, k)]), invoice_date=idate, ship_to=dcs[k], line=ln,
                              delivery_ref='DN%d' % r.delivery, ship_date=r.dispatch, ndc=W.PRODUCTS[r.p]['ndc'],
                              description='LEVETIRACETAM 500MG TAB 100', bottles=int(r.packs), unit_price=price,
                              amount=round(r.packs * price, 2)))
    inv = pd.DataFrame(lines)
    # the catch-up for the three contracts whose price the amendment raised, billed on the first new-price invoices
    rec_q1 = {}
    for r in dl.itertuples(index=False):
        if A.covered(r):
            rec_q1[(r.p, r.dc)] = rec_q1.get((r.p, r.dc), 0) + int(r.packs)
    adj = []
    for (p, k), b in sorted(rec_q1.items()):
        wk = A.ADJ_DATE[p] - dt.timedelta(days=A.ADJ_DATE[p].weekday())
        if (wk, k) not in inv_no:
            inv_no[(wk, k)] = int(nums[n]); n += 1
        diff = round(A.PRICE_NEW[p] - A.PRICE_OLD[p], 2)
        adj.append(dict(invoice_no=str(inv_no[(wk, k)]), invoice_date=A.ADJ_DATE[p], ship_to=dcs[k], line=90 + p,
                        delivery_ref='', ship_date=None, ndc=W.PRODUCTS[p]['ndc'], description='PRICE ADJUSTMENT THRU ' + (A.PRICE_SWITCH[p] - dt.timedelta(days=3)).strftime('%m/%d/%Y'),
                        bottles=b, unit_price=diff, amount=round(b * diff, 2)))
    inv = pd.concat([inv, pd.DataFrame(adj)], ignore_index=True).sort_values(['invoice_date', 'invoice_no', 'line'])
    # the centres' receiving log
    rid = uniq_ints(rng, len(dl) * 2, 600_000, 999_999)
    rec, j = [], 0
    for r in dl.itertuples(index=False):
        for dd, pk in ((r.recv, r.packs1), (r.recv2, r.packs2)):
            if dd is not None and pk:
                rec.append(dict(receipt_id='R%d' % rid[j], centre=W.DCS[r.dc] + ' DC', received=dd, delivery_no=str(r.delivery),
                                ndc=W.PRODUCTS[r.p]['ndc'], bottles=int(pk))); j += 1
    rec = pd.DataFrame(rec).sort_values(['received', 'centre', 'receipt_id'])
    # backorder notices: item numbers as the wholesaler's system held them on the day each opened
    bn = uniq_ints(rng, len(A.WBO), 210_000, 289_999)
    notices = []
    for t, (p, opened, nxt, case) in enumerate(A.WBO):
        item = A.ITEM_OLD[p] if opened.date() < A.MIGRATION else A.ITEM_NEW[p]
        u = opened.replace(tzinfo=PT).astimezone(UTC)
        eta = opened.date() + dt.timedelta(days=int(rng.integers(10, 25)))
        notices.append(dict(notice_no='BO%d' % bn[t], opened_utc=u.strftime('%Y-%m-%dT%H:%M:%SZ'), item_no=item,
                            item_description='LEVETIRACETAM 500MG TAB 100CT', expected_release=eta,
                            scope='ALL LARKHAVEN SHIP-TOS'))
    notices = pd.DataFrame(notices).sort_values('opened_utc')
    item_list = pd.DataFrame([dict(item_no=A.ITEM_NEW[p], former_item_no='' if p in (1, 2) else A.ITEM_OLD[p],
                                   ndc=W.PRODUCTS[p]['ndc'], description='LEVETIRACETAM 500MG TAB 100CT ' + W.PRODUCTS[p]['labeler'].upper(),
                                   effective=A.MIGRATION) for p in A.GENERICS]).sort_values('item_no')
    # advance ship notices: every delivery, UTC, each-level or case-level barcodes
    asn = []
    an = uniq_ints(rng, len(dl), 50_000_000, 89_999_999)
    for t, r in enumerate(dl.itertuples(index=False)):
        h = int(rng.integers(13, 23))
        u = dt.datetime.combine(r.dispatch, dt.time(h, int(rng.integers(0, 60)))).replace(tzinfo=PT).astimezone(UTC)
        if r.case:
            line = dict(gtin=gtin(1, W.PRODUCTS[r.p]['ndc']), uom='CS', qty=int(r.packs) // 12)
        else:
            line = dict(gtin=gtin(0, W.PRODUCTS[r.p]['ndc']), uom='EA', qty=int(r.packs))
        asn.append(dict(asnId='ASN%d' % an[t], shipTimeUtc=u.strftime('%Y-%m-%dT%H:%M:%SZ'), shipTo=dcs[r.dc],
                        deliveryNumber=str(r.delivery), lines=[line]))
    asn.sort(key=lambda x: x['shipTimeUtc'])
    packs = pd.DataFrame([dict(ndc=W.PRODUCTS[p]['ndc'], product=W.PRODUCTS[p]['name'], labeler=W.PRODUCTS[p]['labeler'],
                               strength='500 mg', tablets_per_bottle=100, bottles_per_case=12,
                               gtin=gtin(0, W.PRODUCTS[p]['ndc'])) for p in range(6)])
    shipto = pd.DataFrame(dict(ship_to=dcs, centre=[c + ' DC' for c in W.DCS]))
    return dict(inv=inv, rec=rec, notices=notices, item_list=item_list, asn=asn, packs=packs, shipto=shipto)


def write_csv(df, name):
    df.to_csv(TARGET / name, index=False, lineterminator='\n')


def main():
    TARGET.mkdir(exist_ok=True)
    for p in TARGET.iterdir():
        p.unlink()
    S = W.simulate()
    rng = np.random.default_rng(W.SEED + 101)
    M = build_main(S, rng)
    dl = A.simulate_asks()
    X = build_asks(dl, np.random.default_rng(W.SEED + 202))
    tbl = pa.Table.from_pandas(M['claims'], preserve_index=False)
    pq.write_table(tbl.replace_schema_metadata(None), TARGET / 'dispensing_claims_2025-04_to_2026-06.parquet',
                   compression='zstd', compression_level=19, write_statistics=False)
    write_csv(M['members'], 'members.csv')
    write_csv(M['mrn_x'], 'mrn_member_crosswalk.csv')
    write_csv(M['pharm'], 'pharmacies.csv')
    write_csv(pd.DataFrame([dict(item_code=p['item'], ndc=p['ndc'], product=p['name'], labeler=p['labeler'],
                                 strength='500 mg', form='tablet', live_from=CUTOVER) for p in W.PRODUCTS]),
              'claims_item_crosswalk.csv')
    write_csv(M['enc_lk'], 'ed_encounters_larkhaven_hospitals.csv')
    (TARGET / 'ed_encounters_partner_hospitals.json').write_text(json.dumps(
        dict(feed='partner emergency encounters', timeZone='UTC', records=M['enc_pt']), separators=(',', ':')) + '\n')
    write_csv(X['inv'], 'wholesaler_invoice_lines.csv')
    write_csv(X['rec'], 'dc_receiving_log.csv')
    write_csv(X['notices'], 'wholesaler_backorder_notices.csv')
    write_csv(X['item_list'], 'wholesaler_item_list.csv')
    write_csv(X['packs'], 'pack_register.csv')
    write_csv(X['shipto'], 'wholesaler_ship_to_accounts.csv')
    (TARGET / 'wholesaler_advance_ship_notices.json').write_text(json.dumps(dict(shipments=X['asn']), separators=(',', ':')) + '\n')
    docs.write_documents(TARGET, S, M, X)
    if 'T211_TARGET' not in os.environ:
        docs.write_metadata(TASK, TARGET)
        cut_zip()


def cut_zip():
    names = sorted(p.name for p in TARGET.iterdir())
    with zipfile.ZipFile(TASK / 'target.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo('target/' + n, date_time=(2026, 7, 20, 9, 0, 0))
            zi.external_attr = 0o644 << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, (TARGET / n).read_bytes())


if __name__ == '__main__':
    main()
