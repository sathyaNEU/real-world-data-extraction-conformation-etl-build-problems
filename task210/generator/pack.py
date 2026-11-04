"""task210 pack: the data files under target/, each in its producer's own form. Documents are in docs.py."""
import csv
import datetime as dt
import io
import json
import math
import os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import world as W

FILES = {
    'mp1': 'mp1_ulverthorpe_lane_15min_2026.csv',
    'telematics': 'adt_telematics_2026-05_2026-10.parquet',
    'survey': 'ravensby_topographic_survey_2026-04.geojson',
    'conditions': 'decision_notice_R-2019-0447_conditions.pdf',
    'nmp': 'ravensby_noise_management_plan_rev3.pdf',
    'scheme': 'phase4_working_scheme_2027-01_draft.docx',
    'register': 'ravensby_plant_register_2026.pdf',
    'weather': 'ravensby_weather_station_10min_2026.csv',
    'blasts': 'blast_register_2026.xlsx',
    'complaints': 'complaints_log_2026.xlsx',
    'shifts': 'daily_shift_report_2026.xlsx',
    'belt': 'primary_belt_scale_15min_2026.csv',
    'plc': 'primary_crusher_plc_events_2026.csv',
    'loader': 'wheel_loader_L150_payload_2026.csv',
    'dno': 'northfell_networks_interruption_notices_2026.pdf',
    'tickets': 'weighbridge_tickets_2026-01.xlsx',
    'portable': 'axle_weigher_RWP2_export_2026-01.csv',
    'orders': 'sales_orders_2025-12_2026-01.xlsx',
    'products': 'product_list_2026-06.csv',
}
DISTRACTORS = ['weather', 'blasts', 'complaints', 'shifts']


def build_world(seed=W.SEED):
    P = W.params(seed)
    events, fixes, loads, days = W.simulate_haul(seed, P)
    dset = W.pilot_days()
    run_ev, outages, belt, buckets, running = W.plant_records(seed, P, loads, dset, {r[0]: r[4] for r in days})
    ends = W.period_ends()
    ws, wd = W.weather(seed, ends)
    plant_on = []
    for e in ends:
        mid_local = (e - dt.timedelta(minutes=7, seconds=30) + dt.timedelta(hours=W.bst_offset(e))).replace(tzinfo=None)
        on = False
        for (a, b) in running.get(mid_local.date(), []):
            if a <= mid_local < b:
                on = True
                break
        plant_on.append(on)
    plant_on = np.array(plant_on)
    blasts = blast_days(seed, dset)
    mp1 = W.mp1_record(seed, P, events, ends, ws, wd, plant_on)
    # blasts at 12:15 local add a short airborne event to that quarter hour
    for (d, tl, face, bench) in blasts:
        tu = W.local_to_utc(tl)
        k = int((tu - (ends[0] - dt.timedelta(minutes=15))).total_seconds() // 900)
        e = 10 ** (mp1['laeq'][k] / 10) + 10 ** (float(np.random.default_rng(seed + 9 + k).uniform(44, 49)) / 10) * 8 / 900
        mp1['laeq'][k] = 10 * math.log10(e)
        mp1['lamax'][k] = max(mp1['lamax'][k], 78.0 + (k % 7))
    coll, orders = W.january_sales(seed)
    return dict(P=P, events=events, fixes=fixes, loads=loads, days=days, run_ev=run_ev, outages=outages, belt=belt,
                buckets=buckets, running=running, ends=ends, ws=ws, wd=wd, plant_on=plant_on, mp1=mp1, blasts=blasts,
                coll=coll, orders=orders, seed=seed)


def blast_days(seed, dset):
    rng = np.random.default_rng(seed + 6)
    out = []
    by_week = {}
    for d in dset:
        by_week.setdefault(d.isocalendar()[1], []).append(d)
    for wk in sorted(by_week):
        if rng.random() < 0.85:
            d = by_week[wk][int(rng.integers(0, len(by_week[wk])))]
            face = ['North face', 'West face', 'South face'][int(rng.integers(0, 3))]
            bench = int(rng.integers(1, 4))
            out.append((d, dt.datetime.combine(d, dt.time(12, 15)) + dt.timedelta(minutes=int(rng.integers(0, 6))), face, bench))
    return out


# ------------------------------------------------------------------------------------------------- writers

def write_mp1(path, Wd):
    m, ends = Wd['mp1'], Wd['ends']
    rng = np.random.default_rng(Wd['seed'] + 11)
    # the logger's battery was changed on two Saturday mornings; it recorded nothing while the case was open
    gaps = [(dt.datetime(2026, 7, 18, 8, 30, tzinfo=W.GMT), dt.datetime(2026, 7, 18, 10, 45, tzinfo=W.GMT)),
            (dt.datetime(2026, 9, 19, 9, 0, tzinfo=W.GMT), dt.datetime(2026, 9, 19, 9, 45, tzinfo=W.GMT))]
    buf = io.StringIO()
    buf.write('Location,MP1 Ulverthorpe Lane\r\nInstrument,SLM-1 Class 1 with outdoor microphone kit\r\n'
              'Serial,24318\r\nLogger clock,UTC\r\nLogging period,15 min\r\n'
              'Period end,LAeq dB,LA90 dB,LA10 dB,LAFmax dB\r\n')
    for i, e in enumerate(ends):
        if any(a < e <= b for (a, b) in gaps):
            continue
        buf.write('%s,%.1f,%.1f,%.1f,%.1f\r\n' % (e.strftime('%Y-%m-%d %H:%M'), m['laeq'][i], m['la90'][i],
                                                  m['la10'][i], m['lamax'][i]))
    open(path, 'w', newline='').write(buf.getvalue())


def write_telematics(path, Wd):
    fx = Wd['fixes']
    lat, lon = zip(*[W.to_latlon(f[2], f[3]) for f in fx])
    tbl = pa.table({
        'fix_utc': pa.array([f[0].replace(tzinfo=None) for f in fx], type=pa.timestamp('s', tz='UTC')),
        'unit_id': pa.array([f[1] for f in fx]),
        'lat': pa.array(np.round(lat, 6)), 'lon': pa.array(np.round(lon, 6)),
        'alt_m': pa.array(np.round([f[4] for f in fx], 1)),
        'speed_kmh': pa.array(np.round([f[5] for f in fx], 1)),
        'payload_state': pa.array([f[6] for f in fx]),
    })
    order = np.lexsort((np.array([f[0].timestamp() for f in fx]), np.array([f[1] for f in fx])))
    tbl = tbl.take(pa.array(order))
    pq.write_table(tbl, path, compression='zstd', use_dictionary=['unit_id', 'payload_state'],
                   write_statistics=False, store_schema=False)
    scrub_parquet(path)


def scrub_parquet(path, new=b'parquet-mr version 1.12.3 (build f8dced182c4c1fbdec6ccb3185537b5a01e6ed6b)'):
    """Replace the writer string in the footer (a single-byte thrift length) and re-close the file."""
    b = open(path, 'rb').read()
    flen = int.from_bytes(b[-8:-4], 'little')
    foot = b[-8 - flen:-8]
    i = foot.find(b'parquet-cpp-arrow version')
    L = foot[i - 1]
    assert i > 0 and L < 128 and len(new) < 128
    foot2 = foot[:i - 1] + bytes([len(new)]) + new + foot[i + L:]
    open(path, 'wb').write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, 'little') + b'PAR1')


def _ll(x, y, z=None, nd=6):
    la, lo = W.to_latlon(x, y)
    return [round(lo, nd), round(la, nd)] + ([round(z, 1)] if z is not None else [])


def write_survey(path):
    S = W.SCALE
    feats = []
    def add(layer, name, geom_type, coords, **props):
        p = {'layer': layer, 'name': name}
        p.update(props)
        feats.append({'type': 'Feature', 'properties': p, 'geometry': {'type': geom_type, 'coordinates': coords}})
    add('MONITORING', 'MP1 Ulverthorpe Lane', 'Point', _ll(0, 0, W.MP1[2]), ground_aod=W.MP1[2], microphone_m=1.5)
    for key in ('ramp', 'north', 'floor', 'north_down', 'west_down'):
        r = W.ROADS[key]
        add('HAUL_ROAD', r['name'], 'LineString', [_ll(x, y, z) for (x, y, z) in r['pts']], surface='crushed limestone')
    r = W.ROADS['ext']
    add('PROPOSED', 'Phase 4 haul road', 'LineString', [_ll(x, y, z) for (x, y, z) in r['pts']], surface='to be laid')
    crest = []
    for k in range(0, 361, 15):
        a = math.radians(k)
        crest.append(_ll(-300 + 160 * math.cos(a), -250 + 128 * math.sin(a), 62.0 - (1.4 if 200 < k < 300 else 0.0)))
    add('CREST', 'Pit crest (survey 2026-04-08)', 'LineString', crest)
    add('TOE', 'Pit floor toe', 'LineString', [_ll(-300 + 82 * math.cos(math.radians(k)), -262 + 64 * math.sin(math.radians(k)), 24.0)
                                               for k in range(0, 361, 30)])
    add('BUND', 'Screening bund, plant compound south', 'LineString',
        [_ll(-222, -124, 67.4), _ll(-196, -127, 67.8), _ll(-168, -129, 67.6), _ll(-142, -131, 67.1)], crest_aod=67.4)
    add('PLANT', 'Processing plant compound', 'Polygon', [[_ll(-205, -60), _ll(-120, -62), _ll(-118, -128), _ll(-202, -132), _ll(-205, -60)]])
    add('PLANT', 'Primary crusher feed hopper', 'Point', _ll(W.HOPPER[0], W.HOPPER[1], W.HOPPER[2]))
    add('STOCKPILE', 'Run-of-mine stockpile', 'Polygon', [[_ll(-310, -275), _ll(-276, -272), _ll(-275, -250), _ll(-308, -248), _ll(-310, -275)]],
        top_aod=33.0)
    for k, nm in (('north', 'North face'), ('west', 'West face'), ('south', 'South face')):
        x, y, z = W.FACES[k]
        add('FACE', nm, 'Point', _ll(x, y, z), working_bench_aod=z)
    add('PHASE_4', 'Phase 4 extension (consented)', 'Polygon',
        [[_ll(-182, -430), _ll(-66, -428), _ll(-58, -300), _ll(-120, -296), _ll(-182, -430)]])
    fc = {'type': 'FeatureCollection', 'name': 'Ravensby topographic survey 2026-04',
          'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}},
          'features': feats}
    open(path, 'w').write(json.dumps(fc, separators=(',', ':')))


def write_weather(path, Wd):
    ws, wd, ends = Wd['ws'], Wd['wd'], Wd['ends']
    rng = np.random.default_rng(Wd['seed'] + 12)
    buf = io.StringIO()
    buf.write('Time (UTC),Wind speed m/s,Wind direction deg,Air temp C,Rain mm\n')
    t = dt.datetime(2026, 5, 1, 0, 10, tzinfo=W.GMT)
    i = 0
    while t <= dt.datetime(2026, 11, 1, 0, 0, tzinfo=W.GMT):
        h = int((t - dt.datetime(2026, 5, 1, 0, 0, tzinfo=W.GMT)).total_seconds() // 3600)
        doy = t.timetuple().tm_yday
        temp = 13.5 + 4.5 * math.sin((doy - 110) / 365 * 2 * math.pi) + 3.5 * math.sin((t.hour - 9) / 24 * 2 * math.pi) + rng.normal(0, 0.7)
        rain = max(0.0, rng.normal(-0.9, 0.6)) if rng.random() < 0.13 else 0.0
        buf.write('%s,%.1f,%d,%.1f,%.1f\n' % (t.strftime('%Y-%m-%dT%H:%MZ'), max(0.0, ws[h] + rng.normal(0, 0.5)),
                                             int((wd[h] + rng.normal(0, 9)) % 360), temp, rain))
        t += dt.timedelta(minutes=10)
    open(path, 'w').write(buf.getvalue())


def write_belt(path, Wd):
    rng = np.random.default_rng(Wd['seed'] + 13)
    tons = {}
    for (k, t) in Wd['belt']:
        tons[k] = tons.get(k, 0.0) + t
    buf = io.StringIO()
    buf.write('Tag,PRI-BW-01 primary feed conveyor belt scale\nUnits,tonnes per 15 minutes\nTimestamp,Tonnes\n')
    for d in W.pilot_days():
        t = dt.datetime.combine(d, dt.time(6, 0))
        while t < dt.datetime.combine(d, dt.time(19, 0)):
            v = tons.get(t, 0.0)
            buf.write('%s,%.1f\n' % (t.strftime('%d/%m/%Y %H:%M'), v))
            t += dt.timedelta(minutes=15)
    open(path, 'w').write(buf.getvalue())


def write_plc(path, Wd):
    rng = np.random.default_rng(Wd['seed'] + 14)
    rows = [(t, e) for (t, e) in Wd['run_ev']]
    # ordinary alarm noise the PLC also logs
    for d in W.pilot_days():
        for _ in range(int(rng.poisson(1.3))):
            t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=float(rng.uniform(0, 600)))
            rows.append((t, ['HOPPER LEVEL HIGH', 'HOPPER LEVEL HIGH', 'BELT ALIGN ALARM', 'DUST SUPPRESSION FAULT'][int(rng.integers(0, 4))]))
    rows.sort()
    buf = io.StringIO()
    buf.write('event_time_local,event,source\n')
    for (t, e) in rows:
        src = 'PRI-CR-01' if e in ('START', 'STOP') else ('PRI-HOP-01' if 'HOPPER' in e else 'PRI-CV-01')
        buf.write('%s,%s,%s\n' % (t.strftime('%Y-%m-%d %H:%M:%S'), 'CRUSHER ' + e if e in ('START', 'STOP') else e, src))
    open(path, 'w').write(buf.getvalue())


def write_loader(path, Wd):
    buf = io.StringIO()
    buf.write('Machine,L150H 3104\nScale,onboard payload\nDate,Time,Bucket t,Order\n')
    for (t, w, ref) in Wd['buckets']:
        buf.write('%s,%s,%.2f,%s\n' % (t.strftime('%d/%m/%Y'), t.strftime('%H:%M:%S'), w, ref))
    open(path, 'w').write(buf.getvalue())


def sales_tables(Wd):
    """The weighbridge's January 2026 ticket listing, the portable weigher's export, the order book and the current
    product list. Collections weighed on the portable on a fault day were keyed into the weighbridge system with the
    next Monday's batch, at the time they were keyed."""
    rng = np.random.default_rng(Wd['seed'] + 15)
    coll = sorted(Wd['coll'], key=lambda c: c['t'])
    old_code = {v: k for k, v in W.PRODUCTS_OLD.items()}
    tickets, port = [], []
    batch_clock = {}
    groups = {}
    for c in coll:
        if c['portable']:
            groups.setdefault((c['t'].date(), c['reg'], c['order']), []).append(c)
        else:
            tickets.append(dict(c, ticket_time=c['t'], gross=round(c['tare'] + c['net'], 2)))
    for key in sorted(groups, key=lambda k: min(c['t'] for c in groups[k])):
        runs = sorted(groups[key], key=lambda c: c['t'])
        port.extend(runs)
        d = key[0]
        monday = d + dt.timedelta(days=(7 - d.weekday()))
        clk = batch_clock.get(monday, dt.datetime.combine(monday, dt.time(8, 42)))
        batch_clock[monday] = clk + dt.timedelta(seconds=int(rng.integers(40, 95)))
        net = round(sum(c['net'] for c in runs), 2); tare = round(sum(c['tare'] for c in runs), 2)
        tickets.append(dict(runs[0], ticket_time=clk, net=net, tare=tare, gross=round(tare + net, 2)))
    tickets.sort(key=lambda r: r['ticket_time'])
    tno = 61873
    rows = []
    for r in tickets:
        tno += 1 if rng.random() > 0.02 else 2   # a voided ticket now and then
        prod = r['product']
        price = W.PRICE_JAN[prod]
        rows.append(dict(ticket=tno, when=r['ticket_time'], account=r['account'], reg=r['reg'], order=r['order'],
                         code=old_code[prod], gross=r['gross'], tare=r['tare'], net=r['net'], price=price,
                         value=round(price * r['net'], 2), product=prod, weighed=r['t'], portable=r['portable']))
    return rows, port


def write_portable(path, port, seed):
    rng = np.random.default_rng(seed + 16)
    buf = io.StringIO()
    buf.write('Unit,RW-P2 portable axle weigher\nRecord,Date,Time,Vehicle,Axles,Gross kg,Tare kg,Net kg\n')
    rec = 4410
    for c in sorted(port, key=lambda c: c['t']):
        rec += 1 if rng.random() > 0.08 else int(rng.integers(2, 4))   # check weighs between collections
        gross = int(round((c['tare'] + c['net']) * 1000))
        tare = int(round(c['tare'] * 1000))
        buf.write('%d,%s,%s,%s,%d,%d,%d,%d\n' % (rec, c['t'].strftime('%d/%m/%Y'), c['t'].strftime('%H:%M'), c['reg'],
                                                 int(rng.choice([4, 4, 4, 5])), gross, tare, gross - tare))
    open(path, 'w').write(buf.getvalue())


def write_products(path):
    buf = io.StringIO()
    buf.write('Code,Description,Price per tonne (GBP),VAT\n')
    newp = {'6F2 capping': 10.35, 'Type 1 sub-base': 14.10, '40 mm clean': 15.95, '20 mm clean': 17.55,
            '10 mm clean': 18.80, '0-4 mm dust': 9.05, 'Scalpings': 7.30}
    for code in sorted(W.PRODUCTS_NEW):
        buf.write('%s,%s,%.2f,S\n' % (code, W.PRODUCTS_NEW[code], newp[W.PRODUCTS_NEW[code]]))
    open(path, 'w').write(buf.getvalue())
