"""task401: cut the data files of the pack from the world (world.py, world_asks.py). Documents are in docs.py."""
import csv, os
from datetime import date, datetime, timedelta
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import world as W
import world_asks as A

UK, UTC = W.UK, W.UTC


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(rows)


def f3(x):
    return '%.3f' % x


def river_monitor(out, P, rng):
    """The downstream monitor: 15-minute ammonium (mg/l as N), temperature and pH, UTC timestamps, the maintenance
    visit readings flagged, ratified to 31 December 2025 and provisional after."""
    rows = []
    visits = set()
    d = date(2024, 10, 2)
    while d <= W.D1:
        visits.add(d)
        d += timedelta(days=14)
    t = datetime(2024, 10, 1, 0, 0, tzinfo=UK).astimezone(UTC)
    end = datetime(2026, 4, 1, 0, 0, tzinfo=UK).astimezone(UTC)
    shape = {h: 1 + 0.16 * np.sin(2 * np.pi * (h - 9.5) / 24) for h in range(24)}
    while t < end:
        lt = t.astimezone(UK)
        i = W.idx(lt.date())
        m = P['river'][i] * shape[lt.hour] * float(rng.lognormal(0, 0.035))
        temp = P['temp'][i] - 3.2 + float(rng.normal(0, 0.15))
        ph = 7.85 + float(rng.normal(0, 0.05))
        flag = ''
        if lt.date() in visits and 10 <= lt.hour < 12:
            flag = 'M'
            m = float(rng.uniform(0.0, 0.03))
        status = 'Ratified' if lt.date() <= date(2025, 12, 31) else 'Provisional'
        rows.append((t.strftime('%Y-%m-%dT%H:%M:%SZ'), f3(m), '%.2f' % temp, '%.2f' % ph, status, flag))
        t += timedelta(minutes=15)
    write_csv(os.path.join(out, 'allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv'),
              ['datetime_utc', 'ammonium_mg_l_as_n', 'water_temperature_c', 'ph', 'data_status', 'qc_flag'], rows)


def gauge(out, P, rng):
    rows = [(d.isoformat(), '%.3f' % P['q_up'][W.idx(d)], 'Good' if rng.random() > 0.02 else 'Estimated') for d in W.DAYS]
    write_csv(os.path.join(out, 'allery_at_hollins_bridge_daily_flow.csv'), ['date', 'mean_flow_m3s', 'quality'], rows)


def scada(out, P, rng):
    """Coldmere's hourly historian export, UK local time, tags renamed when the aeration control went in."""
    slug_day1 = {s['day'] + timedelta(days=1) for s in P['slugs']}
    # the blowers run flat out and the oxygen sags for a few hours on many days: storm first flushes, a blower trip, the
    # new control hunting after go-live; the morning after a whey discharge is one of them
    dip = {}
    for d in W.DAYS:
        i = W.idx(d)
        live = d >= W.AER_GO_LIVE
        p_dip = (0.48 if live else 0.12) + (0.25 if P['rain'][i] > 10 else 0.0)
        if d in slug_day1:
            dip[d] = (int(rng.integers(0, 3)), int(rng.integers(7, 12)))
        elif rng.random() < p_dip:
            if rng.random() < (0.75 if live else 0.4):
                # the control turns the air down on the night's low load and the morning load arrives before it
                # recovers
                dip[d] = (int(rng.integers(0, 3)), int(rng.integers(7, 12)))
            else:
                h0 = int(rng.integers(0, 20))
                dip[d] = (h0, min(24, h0 + int(rng.integers(4, 12))))
    rows = []
    t = datetime(2024, 10, 1, 0, 0, tzinfo=UK).astimezone(UTC)
    end = datetime(2026, 4, 1, 0, 0, tzinfo=UK).astimezone(UTC)
    fe_shape = {h: 1 + 0.22 * np.sin(2 * np.pi * (h - 12) / 24) for h in range(24)}
    q_shape = {h: 1 + 0.34 * np.sin(2 * np.pi * (h - 8) / 24) for h in range(24)}
    while t < end:
        lt = t.astimezone(UK)
        d = lt.date()
        i = W.idx(d)
        fe = P['eff'][i] * fe_shape[lt.hour] * float(rng.lognormal(0, 0.06))
        inflow = P['q_eff'][i] / 24 * q_shape[lt.hour] * float(rng.lognormal(0, 0.04))
        new = d >= W.AER_GO_LIVE
        base_do = (1.45 if new else 2.05) + float(rng.normal(0, 0.18))
        air = (3150 if new else 3600) * (1 + 0.12 * np.sin(2 * np.pi * (lt.hour - 11) / 24)) * float(rng.lognormal(0, 0.05))
        if d in dip and dip[d][0] <= lt.hour < dip[d][1]:
            base_do = float(rng.uniform(0.3, 0.9))
            air = float(rng.uniform(4450, 4800))
        mlss = 3150 + 160 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 30) / 365) + float(rng.normal(0, 40))
        temp = P['temp'][i] + float(rng.normal(0, 0.1))
        cells = ['%.1f' % inflow, '%.2f' % fe, '%.2f' % max(base_do, 0.02), '%.2f' % max(base_do + float(rng.normal(0, 0.12)), 0.02),
                 '%.0f' % air, '%.0f' % mlss, '%.1f' % temp]
        if new:
            row = [lt.strftime('%d/%m/%Y %H:%M'), cells[0]] + [''] * 4 + cells[1:5] + cells[5:]
        else:
            row = [lt.strftime('%d/%m/%Y %H:%M'), cells[0]] + cells[1:5] + [''] * 4 + cells[5:]
        rows.append(row)
        t += timedelta(hours=1)
    write_csv(os.path.join(out, 'coldmere_wrc_historian_hourly_2024-10_2026-03.csv'),
              ['timestamp', 'INLET_FLOW_M3H', 'FE_NH4', 'AL1_DO', 'AL2_DO', 'AIR_TOT', 'FE_NH4N_AIT301', 'AB1_DO_AIT110',
               'AB2_DO_AIT210', 'BLW_AIR_TOTAL_FIT400', 'MLSS_AL1', 'WWT_TT120'], rows)


def dairy(out, P, rows, rng):
    """Thornlea Dairy's discharge monitor at its sampling chamber, logged in clock time with logger gaps."""
    slug_keys = set()
    for s in P['slugs']:
        for k in range(-2, s['intervals'] + 3):
            slug_keys.add((s['start'] + timedelta(minutes=15 * k)).astimezone(UTC))
    gaps = []
    for _ in range(7):
        g0 = datetime(2024, 10, 3, tzinfo=UK) + timedelta(hours=int(rng.integers(0, 24 * 540)))
        g1 = g0 + timedelta(hours=int(rng.integers(2, 10)))
        if not any(g0.astimezone(UTC) <= k <= g1.astimezone(UTC) for k in slug_keys):
            gaps.append((g0.astimezone(UTC), g1.astimezone(UTC)))
    out_rows = []
    for lt, flow, ph, tc in rows:
        tu = lt.astimezone(UTC)
        if any(a <= tu < b for a, b in gaps):
            continue
        out_rows.append((lt.strftime('%Y-%m-%d %H:%M'), '%.2f' % flow, '%.2f' % ph, '%.1f' % tc))
    write_csv(os.path.join(out, 'thornlea_dairy_discharge_monitor_15min.csv'),
              ['logger_time', 'flow_m3', 'ph', 'temperature_c'], out_rows)


def trade_effluent(out, rng):
    meters, reads, truth = A.trade_effluent()
    write_csv(os.path.join(out, 'te_meter_reads_2025-26.csv'), ['meter_point', 'read_date', 'register_read', 'read_type'],
              [(r['meter_point'], r['read_date'].isoformat(), r['read'], r['kind']) for r in reads])
    sheets, res, downloads, comps = A.lims()
    samplers = ['K. Hughes', 'B. Hurst', 'J. Evans']
    rounds = []
    who = {}
    for s in sheets:
        day = s['collected_at'].date()
        if day not in who:
            who[day] = samplers[int(rng.integers(0, 3))]
        rounds.append((s['bottle_ref'], s['discharger'], s['sampling_point'], s['collected_at'].strftime('%d/%m/%Y %H:%M'),
                       s['bottle'], who[day], '%.1f' % s['site_ph'], '%.1f' % s['site_temp']))
    write_csv(os.path.join(out, 'te_sampling_rounds_2025-01_2026-04.csv'),
              ['bottle_ref', 'discharger', 'sampling_point', 'collected_at', 'bottle', 'sampler', 'site_ph',
               'site_temperature_c'], rounds)
    write_csv(os.path.join(out, 'lims_trade_effluent_results_2025-01_2026-04.csv'),
              ['sample_no', 'client_ref', 'customer_code', 'sample_point', 'determinand', 'result', 'units', 'reported_on'],
              [(r['sample_no'], r['client_ref'], r['lims_code'], r['point'], r['determinand'], r['result'], r['units'],
                r['reported'].strftime('%d/%m/%Y')) for r in res if r['reported'] <= date(2026, 4, 30)])
    write_csv(os.path.join(out, 'te_sampler_downloads_2025-01_2026-04.csv'),
              ['sampling_point', 'run_start', 'run_end', 'bottle', 'aliquots', 'volume_ml'],
              [(d['point'], d['run_start'].strftime('%d/%m/%Y %H:%M'), d['run_end'].strftime('%d/%m/%Y %H:%M'), d['bottle'],
                d['aliquots'], d['volume_ml']) for d in sorted(downloads, key=lambda x: (x['point'], x['run_end'], x['bottle']))])
    return dict(truth=truth, meters=meters, composites=comps)


def blowers(out):
    rows, snaps = A.blowers()
    tbl = pa.table({'meter_id': [r['meter'] for r in rows],
                    'interval_start_utc': pa.array([r['start_utc'].replace(tzinfo=None) for r in rows], pa.timestamp('s')),
                    'advance_units': [r['units'] for r in rows]})
    tbl = tbl.replace_schema_metadata(None)
    path = os.path.join(out, 'coldmere_site_meters_halfhourly.parquet')
    pq.write_table(tbl, path, compression='snappy', use_dictionary=True, write_statistics=True, store_schema=False)
    scrub_parquet(path)
    return snaps


def scrub_parquet(path, new=b'parquet-mr version 1.12.3 (build f8dced182c4c1fbdec6ccb3185537b5a01e6ed6b)'):
    b = open(path, 'rb').read()
    flen = int.from_bytes(b[-8:-4], 'little')
    foot = b[-8 - flen:-8]
    i = foot.find(b'parquet-cpp-arrow version')
    L = foot[i - 1]
    foot2 = foot[:i - 1] + bytes([len(new)]) + new + foot[i + L:]
    open(path, 'wb').write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, 'little') + b'PAR1')


def connections(out, rng):
    phases, laterals, uprns = A.connections()
    write_csv(os.path.join(out, 'developer_services_phases.csv'),
              ['development', 'phase', 'plots_approved', 'phase_sewer_connected'],
              [(p['development'], p['phase'], p['plots_approved'], p['phase_connected'].strftime('%d/%m/%Y')) for p in phases])


def distractors(out, P, rng):
    # the storm tank's event duration monitoring
    ev = []
    for d in W.DAYS:
        i = W.idx(d)
        if P['spill'][i]:
            s = datetime(d.year, d.month, d.day, int(rng.integers(0, 20)), int(rng.integers(0, 60)), tzinfo=UK)
            e = s + timedelta(minutes=int(P['spill_vol'][i] / 9.0))
            ev.append(('CSO-COLD-ST01', s.astimezone(UTC).strftime('%Y-%m-%d %H:%M'), e.astimezone(UTC).strftime('%Y-%m-%d %H:%M')))
    write_csv(os.path.join(out, 'edm_coldmere_storm_tank_events.csv'), ['asset_id', 'spill_start_utc', 'spill_end_utc'], ev)
    # customer contacts about the river and the works
    cats = ['Odour - works', 'Discoloured river', 'Foam on river', 'Dead fish reported', 'Noise - works']
    rows = []
    n = 0
    for d in W.DAYS:
        k = int(rng.poisson(0.22))
        for _ in range(k):
            n += 1
            rows.append(('CN%06d' % (481200 + n), d.strftime('%d/%m/%Y'), str(rng.choice(cats, p=[.46, .18, .14, .06, .16])),
                         str(rng.choice(['Coldmere', 'Hollins Bridge', 'Allery Meadows', 'Station Quarter']))))
    write_csv(os.path.join(out, 'customer_contacts_river_and_works.csv'), ['contact_ref', 'date', 'category', 'locality'], rows)


def cut(out, seed=W.SEED):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(seed + 9)
    P = W.daily_process(seed)
    drows = W.dairy_15min(P, seed)
    river_monitor(out, P, rng)
    gauge(out, P, rng)
    scada(out, P, rng)
    dairy(out, P, drows, rng)
    te_truth = trade_effluent(out, rng)
    snaps = blowers(out)
    connections(out, rng)
    distractors(out, P, rng)
    return dict(P=P, te_truth=te_truth, snaps=snaps)
