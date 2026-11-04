"""task210 golden: every graded figure computed from target/ alone, and the two deliverables."""
import datetime as dt
import io
import json
import math
import os
import zoneinfo
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

LON = zoneinfo.ZoneInfo('Europe/London')
SHARE_DB = 44.0
CYCLE = 4.5
MONTHS = ['2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']
WEEKS = [('2025-12-29', '2026-01-01', '2026-01-04'), ('2026-01-05', '2026-01-05', '2026-01-11'),
         ('2026-01-12', '2026-01-12', '2026-01-18'), ('2026-01-19', '2026-01-19', '2026-01-25'),
         ('2026-01-26', '2026-01-26', '2026-01-31')]


def find(tgt, prefix):
    for f in sorted(os.listdir(tgt)):
        if f.startswith(prefix):
            return os.path.join(tgt, f)
    raise FileNotFoundError(prefix)


# ------------------------------------------------------------------------------------------------ readers

def read_mp1(tgt):
    raw = open(find(tgt, 'mp1_'), newline='').read().splitlines()
    k = [i for i, l in enumerate(raw) if l.startswith('Period end')][0]
    df = pd.read_csv(io.StringIO('\n'.join(raw[k:])))
    df.columns = ['end', 'LAeq', 'LA90', 'LA10', 'LAFmax']
    df['end_utc'] = pd.to_datetime(df['end']).dt.tz_localize('UTC')
    df['start_local'] = (df['end_utc'] - pd.Timedelta(minutes=15)).dt.tz_convert(LON)
    return df


def read_survey(tgt):
    fc = json.load(open(find(tgt, 'ravensby_topographic_survey')))
    out = {'roads': {}, 'faces': {}, 'points': {}}
    for f in fc['features']:
        p = f['properties']; g = f['geometry']
        if p['layer'] in ('HAUL_ROAD', 'PROPOSED'):
            out['roads'][p['name']] = g['coordinates']
        elif p['layer'] == 'FACE':
            out['faces'][p['name']] = g['coordinates']
        elif p['layer'] in ('PLANT', 'MONITORING') and g['type'] == 'Point':
            out['points'][p['name']] = g['coordinates']
        elif p['layer'] == 'STOCKPILE':
            ring = np.array(g['coordinates'][0])
            out['points'][p['name']] = list(ring[:-1, :2].mean(axis=0))
    return out


def local_xy(lat, lon, ref):
    lat0, lon0 = ref[1], ref[0]
    y = (np.asarray(lat) - lat0) * 111132.0
    x = (np.asarray(lon) - lon0) * 111320.0 * math.cos(math.radians(lat0))
    return x, y


def trips(tgt, survey):
    """One row per loaded trip: truck, where it loaded, where it tipped, the tip time (UTC)."""
    t = pq.read_table(find(tgt, 'adt_telematics')).to_pandas()
    ref = survey['points']['MP1 Ulverthorpe Lane']
    t['x'], t['y'] = local_xy(t['lat'], t['lon'], ref)
    faces = {n: local_xy(c[1], c[0], ref) for n, c in survey['faces'].items()}
    hop = survey['points']['Primary crusher feed hopper']; hx, hy = local_xy(hop[1], hop[0], ref)
    stk = survey['points']['Run-of-mine stockpile']; sx, sy = local_xy(stk[1], stk[0], ref)
    rows = []
    for unit, g in t.sort_values(['unit_id', 'fix_utc']).groupby('unit_id', sort=True):
        st = g['payload_state'].to_numpy(); x = g['x'].to_numpy(); y = g['y'].to_numpy(); tm = g['fix_utc'].to_numpy()
        n = len(st); i = 0
        while i < n:
            if st[i] == 'LOADED' and i > 0 and st[i - 1] == 'EMPTY':
                j = i
                while j < n and st[j] == 'LOADED':
                    j += 1
                if j < n and (tm[j] - tm[j - 1]) <= np.timedelta64(5, 'm') and (tm[i] - tm[i - 1]) <= np.timedelta64(5, 'm'):
                    lx, ly = x[i - 1], y[i - 1]
                    face = min(faces, key=lambda f: (faces[f][0] - lx) ** 2 + (faces[f][1] - ly) ** 2)
                    ex, ey = x[j], y[j]
                    tip = 'hopper' if (ex - hx) ** 2 + (ey - hy) ** 2 < (ex - sx) ** 2 + (ey - sy) ** 2 else 'stockpile'
                    rows.append((unit, face, tip, pd.Timestamp(tm[j - 1]), pd.Timestamp(tm[j])))
                i = j
            else:
                i += 1
    tr = pd.DataFrame(rows, columns=['unit', 'face', 'tip', 'last_loaded', 'first_empty'])
    tr['tip_utc'] = tr['first_empty'].dt.tz_localize('UTC') if tr['first_empty'].dt.tz is None else tr['first_empty']
    tr['route'] = np.where((tr['face'] == 'North face') & (tr['tip'] == 'hopper'), 'haul road 2', 'other')
    return tr


# --------------------------------------------------------------------------------------------- the call

def hourly(mp1, tr):
    w = mp1[(mp1['start_local'].dt.weekday < 5)]
    w = w[(w['start_local'].dt.hour >= 7) & (w['start_local'].dt.hour < 17)]
    w = w.assign(hour=w['start_local'].dt.floor('h'), E=10 ** (w['LAeq'] / 10.0) * 900.0)
    days = set(tr['tip_utc'].dt.tz_convert(LON).dt.date)
    w = w[w['start_local'].dt.date.isin(days)]
    H = w.groupby('hour').agg(E=('E', 'sum'), n=('E', 'size'))
    H = H[H['n'] == 4]
    th = tr['tip_utc'].dt.floor('h').dt.tz_convert(LON)
    for (f, tp), g in tr.groupby(['face', 'tip']):
        H[f + '|' + tp] = th[g.index].value_counts().reindex(H.index).fillna(0).to_numpy()
    c2 = th[tr['route'] == 'haul road 2'].value_counts(); co = th[tr['route'] == 'other'].value_counts()
    H['n2'] = c2.reindex(H.index).fillna(0).to_numpy(); H['no'] = co.reindex(H.index).fillna(0).to_numpy()
    return H


def fit(H, cols):
    X = np.c_[np.ones(len(H))] if not cols else np.c_[np.ones(len(H)), H[cols].to_numpy()]
    b = np.linalg.lstsq(X, H['E'].to_numpy(), rcond=None)[0]
    return dict(zip(['a'] + cols, b))


def call_from(e_mov):
    nmax = 10 ** (SHARE_DB / 10.0) * 3600.0 / e_mov
    adts = int(math.floor(nmax / CYCLE))
    dial = [(k, k * CYCLE, 10 * math.log10(k * CYCLE * e_mov / 3600.0)) for k in range(1, 13)]
    return nmax, adts, dial


# ---------------------------------------------------------------------------------------------- the asks

def read_belt(tgt):
    raw = open(find(tgt, 'primary_belt_scale')).read().splitlines()
    k = [i for i, l in enumerate(raw) if l.startswith('Timestamp')][0]
    b = pd.read_csv(io.StringIO('\n'.join(raw[k:])))
    b['t'] = pd.to_datetime(b['Timestamp'], format='%d/%m/%Y %H:%M')
    return b


def read_loader(tgt):
    raw = open(find(tgt, 'wheel_loader')).read().splitlines()
    k = [i for i, l in enumerate(raw) if l.startswith('Date,Time')][0]
    L = pd.read_csv(io.StringIO('\n'.join(raw[k:])), keep_default_na=False)
    L['t'] = pd.to_datetime(L['Date'] + ' ' + L['Time'], format='%d/%m/%Y %H:%M:%S')
    return L


def read_dno(tgt):
    from pypdf import PdfReader
    txt = '\n'.join(pg.extract_text() for pg in PdfReader(find(tgt, 'northfell')).pages)
    import re
    out = []
    for m in re.finditer(r'NF-\d{4}-\d{4}\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})', txt):
        d = dt.datetime.strptime(m.group(1), '%d/%m/%Y').date()
        out.append((dt.datetime.combine(d, dt.datetime.strptime(m.group(2), '%H:%M').time()),
                    dt.datetime.combine(d, dt.datetime.strptime(m.group(3), '%H:%M').time())))
    return out


def run_intervals(tgt, dno):
    ev = pd.read_csv(find(tgt, 'primary_crusher_plc'))
    ev = ev[ev['event'].isin(['CRUSHER START', 'CRUSHER STOP'])].copy()
    ev['t'] = pd.to_datetime(ev['event_time_local'])
    ev = ev.sort_values('t').reset_index(drop=True)
    runs = []
    for i, r in ev.iterrows():
        if r['event'] != 'CRUSHER START':
            continue
        nxt = ev.iloc[i + 1] if i + 1 < len(ev) else None
        end = nxt['t'] if nxt is not None else None
        cut = [a for (a, b) in dno if r['t'] < a and (end is None or a < end)]
        if cut:
            end = min(cut)
        elif nxt is None or nxt['event'] != 'CRUSHER STOP':
            raise ValueError('unclosed run at %s' % r['t'])
        runs.append((r['t'].to_pydatetime(), end.to_pydatetime() if hasattr(end, 'to_pydatetime') else end))
    return runs


def asks_plant(tgt, tr):
    belt = read_belt(tgt); L = read_loader(tgt)
    belt['month'] = belt['t'].dt.strftime('%Y-%m')
    flow = belt.set_index('t')['Tonnes']
    L['bin'] = L['t'].dt.floor('15min')
    blank = L[L['Order'] == '']
    reclaim = blank[blank['bin'].map(lambda b: flow.get(b, 0.0) > 0)]
    reclaim = reclaim.assign(month=reclaim['t'].dt.strftime('%Y-%m'))
    loads = tr[tr['tip'] == 'hopper'].copy()
    loads['month'] = loads['tip_utc'].dt.tz_convert(LON).dt.strftime('%Y-%m')
    dno = read_dno(tgt); runs = run_intervals(tgt, dno)
    hrs = {}
    for (a, b) in runs:
        hrs[a.strftime('%Y-%m')] = hrs.get(a.strftime('%Y-%m'), 0.0) + (b - a).total_seconds() / 3600.0
    out = {}
    for m in MONTHS:
        bt = belt.loc[belt['month'] == m, 'Tonnes'].sum()
        rc = reclaim.loc[reclaim['month'] == m, 'Bucket t'].sum()
        n = int((loads['month'] == m).sum())
        out[m] = dict(belt=bt, reclaim=rc, loads=n, t_per_load=(bt - rc) / n, hours=hrs[m], t_per_hour=bt / hrs[m])
    return out


def asks_sales(tgt):
    import itertools
    tk = pd.read_excel(find(tgt, 'weighbridge_tickets'))
    od = pd.read_excel(find(tgt, 'sales_orders'))
    pt = pd.read_csv(find(tgt, 'axle_weigher'), skiprows=1)
    tk['when'] = pd.to_datetime(tk['Date/time'], format='%d/%m/%Y %H:%M')
    # the product a ticket loaded: its code, read through the code-to-product pairing the order book shows for most
    # tickets (the June 2026 list numbers the products differently)
    tk['ordered'] = tk['Order no'].map(dict(zip(od['Order no'], od['Product'])))
    pair = tk.groupby(['Product', 'ordered']).size().reset_index(name='n')
    code = pair.sort_values('n').groupby('Product').tail(1).set_index('Product')['ordered'].to_dict()
    tk['product'] = tk['Product'].map(code)
    # the day each lorry was weighed: tickets keyed from the portable weigher's records carry the keying time
    pt['weighed'] = pd.to_datetime(pt['Date'] + ' ' + pt['Time'], format='%d/%m/%Y %H:%M')
    pt['t'] = (pt['Net kg'] / 1000.0).round(2)
    used = set()
    tk['weighed'] = tk['when']
    for i, r in tk[tk['when'].dt.weekday == 0].iterrows():
        cand = pt[(pt['Vehicle'] == r['Vehicle']) & (pt['weighed'] < r['when']) &
                  (pt['weighed'] > r['when'] - pd.Timedelta(days=7))]
        hits = []
        for day, g in cand.groupby(cand['weighed'].dt.date):
            idx = list(g.index)
            for k in range(1, 4):
                for sub in itertools.combinations(idx, k):
                    if abs(pt.loc[list(sub), 't'].sum() - r['Net (t)']) < 0.005:
                        hits.append(sub)
        hits = [h for h in hits if not used & set(h)]
        if hits:
            assert len(set(pt.loc[list(h), 'weighed'].dt.date.min() for h in hits)) == 1, (r['Ticket'], hits)
            used |= set(hits[0])
            tk.loc[i, 'weighed'] = pt.loc[list(hits[0]), 'weighed'].min()
    assert used == set(pt.index)
    jan = tk[(tk['weighed'] >= '2026-01-01') & (tk['weighed'] < '2026-02-01')]
    products = jan.groupby('product')['Net (t)'].sum().to_dict()
    weeks = []
    for (lab, a, b) in WEEKS:
        s = jan[(jan['weighed'] >= a) & (jan['weighed'] < pd.Timestamp(b) + pd.Timedelta(days=1))]['Net (t)'].sum()
        weeks.append((lab, s))
    return dict(products=products, weeks=weeks, n_tickets=len(tk), n_redated=int((tk['weighed'] != tk['when']).sum()),
                code=code)


# --------------------------------------------------------------------------------------------- compute

def compute(tgt):
    survey = read_survey(tgt)
    mp1 = read_mp1(tgt)
    tr = trips(tgt, survey)
    H = hourly(mp1, tr)
    routes = sorted(c for c in H.columns if '|' in c)
    b = fit(H, routes)
    e_mov = b['North face|hopper']
    b['no'] = float(np.average([b[c] for c in routes if c != 'North face|hopper'],
                               weights=[H[c].sum() for c in routes if c != 'North face|hopper']))
    nmax, adts, dial = call_from(e_mov)
    G = dict(e_mov=e_mov, e_other=b['no'], intercept=b['a'], nmax=nmax, adts=adts, dial=dial,
             sel_in=10 * math.log10(e_mov), sel_other=10 * math.log10(max(b['no'], 1e-9)),
             n_trips=len(tr), n_hr2=int((tr['route'] == 'haul road 2').sum()), hours=len(H),
             plant=asks_plant(tgt, tr), sales=asks_sales(tgt), H=H, trips=tr, mp1=mp1)
    lv = lambda k: dial[k - 1][2]
    G['level_call'] = lv(adts); G['level_next'] = lv(adts + 1)
    return G


def figures(G):
    """The graded figures: the call, the first count over the share, each setting's verdict, and the asks."""
    f = {'call_adts': G['adts'], 'first_adts_over_share': G['adts'] + 1, 'haulage_share_db': SHARE_DB,
         'cycle_movements_per_adt_hour': CYCLE, 'call_movements_per_hour': G['adts'] * CYCLE,
         'next_movements_per_hour': (G['adts'] + 1) * CYCLE,
         'product_names': sorted(G['sales']['products'])}
    for (k, n, L) in G['dial']:
        f['dial_%02d_within_share' % k] = 'yes' if L <= SHARE_DB else 'no'
        f['dial_%02d_movements_per_hour' % k] = round(n, 1)
    for m, v in G['plant'].items():
        f['t_per_load_%s' % m] = round(v['t_per_load'], 1)
        f['t_per_running_hour_%s' % m] = round(v['t_per_hour'], 1)
    for pname, v in sorted(G['sales']['products'].items()):
        f['jan2026_t_%s' % pname.replace(' ', '_').replace('-', '_')] = int(round(v))
    for (lab, v) in G['sales']['weeks']:
        f['jan2026_week_%s_t' % lab] = int(round(v))
    return f


def write(G, gld):
    import csv
    with open(os.path.join(gld, 'extension_haul_dial.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['adts_on_phase4_haul_road', 'loaded_movements_per_hour', 'within_44_0_dB_haulage_share'])
        for (k, n, L) in G['dial']:
            w.writerow([k, '%.1f' % n, 'yes' if L <= SHARE_DB else 'no'])
    note(G, os.path.join(gld, 'extension_scheme_note.pdf'))


def note(G, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    import calendar, re
    fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=110)
    ks = [k for (k, n, L) in G['dial']]; ls = [L for (k, n, L) in G['dial']]
    ax.plot(ks, ls, marker='o', color='#2B5C8A', lw=1.6)
    ax.axhline(SHARE_DB, color='#B03A2E', lw=1.1, ls='--')
    ax.text(12.2, SHARE_DB + 0.15, 'haulage share 44.0 dB', ha='right', va='bottom', fontsize=7.5, color='#B03A2E')
    ax.scatter([G['adts']], [G['level_call']], s=70, facecolor='none', edgecolor='#B03A2E', lw=1.4, zorder=3)
    ax.set_xticks(ks); ax.set_xlabel('ADTs allocated to the Phase 4 haul road'); ax.set_ylabel('dB LAeq,1h at MP1')
    ax.set_title('A fourth truck takes Phase 4 haulage over the 44.0 dB share at MP1', fontsize=9)
    ax.grid(alpha=0.3); fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', metadata={'Software': None}); plt.close(fig); buf.seek(0)
    ss = getSampleStyleSheet()
    body = ParagraphStyle('b', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.3, leading=12.2, spaceAfter=4)
    h = ParagraphStyle('h', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=10.4, spaceBefore=6, spaceAfter=2)
    t = ParagraphStyle('t', parent=ss['Title'], fontName='Helvetica-Bold', fontSize=13, alignment=0, spaceAfter=2)
    ts = TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 8), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
                     ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
                     ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')), ('ALIGN', (1, 1), (-1, -1), 'RIGHT')])
    P = G['plant']; S = G['sales']
    story = [Paragraph('Three trucks on the Phase 4 haul road in January', t),
             Paragraph('To: Maurice Russell, Minerals and Waste Planning, Holmeshire County Council<br/>'
                       'From: Garry Fry, Quarry Manager, Ravensby Quarry<br/>'
                       'Date: 4 December 2026<br/>'
                       'Ref: R/2019/0447, condition 19, January 2027 working scheme (Phase 4)', body),
             Paragraph('Allocation', h),
             Paragraph('Three articulated dump trucks go on the Phase 4 haul road in January. At the scheme\'s 4.5 loaded '
                       'movements a truck an hour that is %.1f movements an hour, which holds haulage at MP1 inside the '
                       '44.0 dB share in NMP 5.2. A fourth truck (%.1f movements an hour) takes it over the share, so the '
                       'scheme goes in at three.' % (G['adts'] * CYCLE, (G['adts'] + 1) * CYCLE)
                       if G['adts'] == 3 else 'Allocate %d trucks.' % G['adts'], body),
             Paragraph('Why three, when the pilot ran up to seven', h),
             Paragraph('The loud hours at MP1 between May and October were not the busy hours. They came when north face '
                       'loads went to the primary up Haul road 2, which climbs out on the original ground towards '
                       'Ulverthorpe Lane. North face loads tipped on the run-of-mine stockpile stay in the pit, and south '
                       'and west face loads to the primary come up Haul road 1 and behind the plant compound bund. Each '
                       'working hour\'s sound energy at MP1 was split across that hour\'s movements by where each truck '
                       'loaded and where it tipped, from the trucks\' GPS tracks against the April survey. One Haul road 2 '
                       'movement puts several times the energy of any other movement on MP1. The Phase 4 haul road runs '
                       'on the same kind of ground at the same distances from the Lane, so every Phase 4 movement counts at '
                       'the Haul road 2 rate, not at the site average that would allow far more trucks.', body),
             Image(buf, width=150 * mm, height=70 * mm)]
    rows = [['Month', 'Tonnes per haul load to the primary', 'Primary tonnes per running hour']]
    for m in MONTHS:
        rows.append([dt.date(int(m[:4]), int(m[5:]), 1).strftime('%B %Y'), '%.1f' % P[m]['t_per_load'], '%.1f' % P[m]['t_per_hour']])
    tb = Table(rows, colWidths=[35 * mm, 60 * mm, 60 * mm]); tb.setStyle(ts)
    src = ParagraphStyle('s', parent=body, fontSize=7.4, leading=9, textColor=colors.HexColor('#555555'))
    story += [Paragraph('Primary crusher feed, May to October 2026', h), tb,
              Paragraph('Source: PRI-BW-01 belt scale, primary crusher PLC log, L150H onboard payload log, ADT '
                        'telematics, Northfell interruption notices. Loader feed from the run-of-mine stockpile is '
                        'taken off the belt tonnes before dividing by the haul loads tipped into the hopper.', src)]
    rows = [['Product', 'Tonnes sold, January 2026']] + [[k, '{:,.0f}'.format(v)] for k, v in sorted(S['products'].items())]
    tb2 = Table(rows, colWidths=[50 * mm, 45 * mm]); tb2.setStyle(ts)
    wlab = {'2025-12-29': '1 to 4 January', '2026-01-05': '5 to 11 January', '2026-01-12': '12 to 18 January',
            '2026-01-19': '19 to 25 January', '2026-01-26': '26 to 31 January'}
    rows = [['Week (Monday to Sunday)', 'Tonnes sold']] + [[wlab[l], '{:,.0f}'.format(v)] for (l, v) in S['weeks']]
    tb3 = Table(rows, colWidths=[50 * mm, 35 * mm]); tb3.setStyle(ts)
    story += [Paragraph('January 2026 sales, by the day each lorry was weighed', h), tb2, Spacer(1, 4), tb3,
              Paragraph('Source: weighbridge ticket listing, RW-P2 portable weigher export, sales order book. Products '
                        'as charged on the ticket; codes are the ones in use before the June 2026 system change. Week '
                        'one is 1 to 4 January only.', src)]
    import os as _os
    old = _os.environ.get('SOURCE_DATE_EPOCH'); _os.environ['SOURCE_DATE_EPOCH'] = str(calendar.timegm((2026, 12, 4, 15, 30, 0, 0, 1, 0)))
    def deco(c, d):
        c.saveState(); c.setFont('Helvetica', 7); c.setFillColor(colors.HexColor('#666666'))
        c.drawString(18 * mm, 10 * mm, 'Ravensby Quarry, Calderwick Stone Ltd. January 2027 working scheme, Phase 4.')
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, 'Page %d' % d.page); c.restoreState()
        c._doc.info.producer = 'Microsoft Word for Microsoft 365'; c._doc.info.creator = 'Microsoft Word for Microsoft 365'
        c._doc.info.subject = ''; c._doc.info.author = 'Garry Fry'; c._doc.info.title = 'Phase 4 haulage January 2027'
    try:
        SimpleDocTemplate(path, pagesize=A4, invariant=1, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                          bottomMargin=16 * mm).build(story, onFirstPage=deco, onLaterPages=deco)
    finally:
        if old is None:
            del _os.environ['SOURCE_DATE_EPOCH']
        else:
            _os.environ['SOURCE_DATE_EPOCH'] = old
    raw = open(path, 'rb').read()
    out = re.sub(rb'(%[^\n]*?)( ?ReportLab[^\n]*)', lambda m: m.group(1) + b' ' * len(m.group(2)), raw)
    for tag in (rb'/Trapped /False', rb'/Keywords ()', rb'/Subject ()', rb'/Subject (\(unspecified\))'):
        out = out.replace(tag, b' ' * len(tag))
    open(path, 'wb').write(out)
