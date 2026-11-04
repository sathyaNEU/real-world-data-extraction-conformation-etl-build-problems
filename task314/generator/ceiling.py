"""The cracker and the mirror, run as code on the cut pack (target/), scored figure by figure against figures.json.

The cracker lands the call and runs the hygiene battery on the asks: local dates, the later read of a visit, the
meter exchanges walked through the work orders with their register units, every meter on the list counted, the
fill station's rows summed and counted as the vendor's report sums them.  The mirror stops on the block-price rung
for the call and reads the asks the natural way: the rows summed, each meter differenced on its own register.

    python3 task314/generator/ceiling.py
"""
import hashlib
import json
import math
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
AF_GAL = 325851.0
CCF_GAL = 748.052
MONTHS = ((6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'))


def fill_rows():
    fs = pd.read_csv(os.path.join(TGT, 'fill_station_transactions_2026-01-01_2026-10-31.csv'))
    fs['month'] = pd.to_datetime(fs.txn_start.str[:10]).dt.month
    return {nm: (int(math.floor(fs[fs.month == m].gallons.sum() / 1000.0 + 0.5)), int((fs.month == m).sum()))
            for m, nm in MONTHS}


def facilities(walk_exchanges):
    rd = pd.read_csv(os.path.join(TGT, 'city_facility_meter_reads_2025-09_2026-10.csv'))
    rd['d'] = pd.to_datetime(rd.read_date, format='%m/%d/%Y')
    rd = rd.sort_values(['facility_id', 'd', 'read_time']).groupby(['facility_id', 'd'], as_index=False).last()
    fl = pd.read_csv(os.path.join(TGT, 'city_facility_meters_2026-10-30.csv'))
    wo = pd.read_excel(os.path.join(TGT, 'meter_shop_completed_work_orders_2025-2026.xlsx'))
    wf = wo[wo.location_type == 'CITY FACILITY']
    unit = dict(zip(fl.meter_id, fl.register_unit))
    for _, w in wf.iterrows():
        unit.setdefault(w.old_meter_id, w.old_register_unit)
        unit.setdefault(w.new_meter_id, w.new_register_unit)
    out = {m: 0.0 for m, _ in MONTHS}
    for fid, g in rd.groupby('facility_id'):
        g = g.sort_values('d')
        prev = None
        for _, r in g.iterrows():
            if prev is not None and r.d.year == 2026 and r.d.month in out:
                if r.meter_id == prev.meter_id:
                    f = (CCF_GAL if unit[r.meter_id] == 'CCF' else 1.0) if walk_exchanges else 1.0
                    out[r.d.month] += (r.register - prev.register) * f
                elif walk_exchanges:
                    w = wf[(wf.location_id == fid) & (wf.new_meter_id == r.meter_id)].iloc[0]
                    f = CCF_GAL if w.new_register_unit == 'CCF' else 1.0
                    out[r.d.month] += (w.old_final_read - prev.register) + (r.register - w.new_initial_read) * f
            prev = r
    return {nm: round(out[m] / AF_GAL + 1e-9, 1) for m, nm in MONTHS}


def score(fill, fac, fig):
    rows = []
    for m, nm in MONTHS:
        rows.append(('fill station water, %s' % nm, fill[nm][0], fig['ask']['fill_kgal'][nm]))
        rows.append(('fill station fills, %s' % nm, fill[nm][1], fig['ask']['fills'][nm]))
        rows.append(('city facilities, %s' % nm, fac[nm], fig['ask']['facilities_af'][nm]))
    return rows


def main():
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    digest = hashlib.sha256(open(os.path.join(TASK, 'target.zip'), 'rb').read()).hexdigest()
    fill = fill_rows()
    crack = score(fill, facilities(True), fig)
    mirror = score(fill, facilities(False), fig)
    kc = sum(1 for _, a, g in crack if a == g) / len(crack)
    km = sum(1 for _, a, g in mirror if a == g) / len(mirror)
    c = 38 + 7 + 55 * kc
    s = 5 + 7 + 55 * km
    print('pack target.zip sha256 %s' % digest)
    print('%-34s %10s %10s %10s' % ('ask figure', 'cracker', 'mirror', 'golden'))
    for (n, a, g), (_, b, _) in zip(crack, mirror):
        print('%-34s %10s %10s %10s  %s %s' % (n, a, b, g, 'hit' if a == g else 'miss', 'hit' if b == g else 'miss'))
    print('cracker keeps %.1f per cent of the ask weight, on the call: %.1f' % (100 * kc, c))
    print('mirror keeps %.1f per cent of the ask weight, off the call: %.1f' % (100 * km, s))
    print('pair ceiling %.1f' % ((c + s) / 2))
    return 0


if __name__ == '__main__':
    main()
