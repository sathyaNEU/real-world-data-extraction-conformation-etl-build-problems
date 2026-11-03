"""The clean-truth computation of the call and the ladder's rungs, from the world (not the files)."""
import datetime as dt
import numpy as np
import world as Wm
from world import UNITS, RATED, QUOTE_MNOK, LIMIT, OSLO, L, local, NH

WINTER_W = [(y, 12, 1) for y in range(2021, 2026)]   # outage weeks valued over the last five winters
OUT_WEEKS = 14


def unit_year_stats(W):
    yrs = W['year']
    gen, starts, run, rz = {}, {}, {}, {}
    for u in UNITS:
        o = W['out'][u]; on = o > 0
        st = np.zeros(NH, bool); st[1:] = on[1:] & ~on[:-1]
        for y in range(2016, 2027):
            m = yrs == y
            gen[(u, y)] = float(o[m].sum()); starts[(u, y)] = int(st[m].sum()); run[(u, y)] = int(on[m].sum())
            rz[(u, y)] = int(W['inz'][u][m].sum())
    return gen, starts, run, rz


def totals(W):
    """Each unit's generation (MWh) and starts over the whole record, 2016-01-01 to 2026-12-31 local."""
    gen, starts = {}, {}
    for u in UNITS:
        o = W['out'][u]; on = o > 0
        gen[u] = float(o.sum()); starts[u] = int((on[1:] & ~on[:-1]).sum())
    return gen, starts


def counter_readings(W):
    """The governors' running-hour and start counters (totals since commissioning), read when each overhaul begins and
    when the unit returns to service."""
    rows = []
    for u in UNITS:
        on = W['out'][u] > 0
        st = np.zeros(NH, bool); st[1:] = on[1:] & ~on[:-1]
        age = 2016 - Wm.COMMISSIONED[u]
        h0 = int(age * (2600 if u == 'SDL-G3' else 7150) + 37 * (Wm.COMMISSIONED[u] % 7))
        s0 = int(age * (780 if u == 'SDL-G3' else 27) + 3 * (Wm.COMMISSIONED[u] % 5))
        for (s, e) in Wm.OVERHAULS[u]:
            i0, i1 = L(*s), L(*e)
            for d, i, kind in ((s, i0, 'overhaul start'), (e, i1, 'return to service')):
                rows.append({'date': dt.date(*d), 'unit': u, 'kind': kind, 'hours': h0 + int(on[:i].sum()),
                             'starts': s0 + int(st[:i].sum()), 'i': i})
    return rows


def counter_pairs(W):
    """Consecutive inspections of a runner at consecutive overhauls of one unit, with the counters' running hours and
    starts between the return to service after the first and the start of the second: (runner, unit, start pitting,
    found, hours, starts). Pre-period inspections have no reading to difference against."""
    reads = counter_readings(W)
    out = []
    for p in pairs(W):
        rn, i0, start, i1, found = p
        u = [f['unit'] for f in W['found'] if f['runner'] == rn and f['i'] == i1][0]
        a = [r for r in reads if r['unit'] == u and r['kind'] == 'return to service' and r['i'] >= i0]
        b = [r for r in reads if r['unit'] == u and r['kind'] == 'overhaul start' and r['i'] <= i1]
        if a and b:
            a, b = a[0], b[-1]
            out.append((rn, u, start, found, b['hours'] - a['hours'], b['starts'] - a['starts']))
    return out


def winter_generation(W, u):
    o = W['out'][u]; tot = 0.0
    for (y, mth, d) in WINTER_W:
        s = L(y, mth, d); e = s + OUT_WEEKS * 7 * 24
        e = Wm.hidx(dt.datetime(y, mth, d, tzinfo=OSLO) + dt.timedelta(weeks=OUT_WEEKS))
        tot += o[s:e].sum()
    return tot / len(WINTER_W)


def current_runner(u):
    return Wm.RUNNER_IN[u][-1][1]


def last_inspection(W, rn):
    fs = [f for f in W['found'] if f['runner'] == rn]
    return fs[-1]


def pairs(W):
    """Consecutive in-period inspections of one runner with no repair between: (runner, i0, start pitting, i1, found)."""
    out = []
    by = {}
    for f in W['found']:
        by.setdefault(f['runner'], []).append(f)
    for rn, fs in by.items():
        for a, b in zip(fs, fs[1:]):
            start = a['repaired_to'] if a['repaired_to'] is not None else a['found']
            out.append((rn, a['i'], start, b['i'], b['found']))
    return out


def runner_counts(W, rn, i0, i1, what):
    tot = 0
    for u in UNITS:
        occ = W['occ'][u][i0:i1] == rn
        if what == 'rz':
            tot += int((W['inz'][u][i0:i1] & occ).sum())
        elif what == 'run':
            tot += int(((W['out'][u][i0:i1] > 0) & occ).sum())
        elif what == 'starts':
            o = W['out'][u] > 0
            st = np.zeros(NH, bool); st[1:] = o[1:] & ~o[:-1]
            tot += int((st[i0:i1] & occ).sum())
    return tot


def project(W, rate_of, unit_rate_2026):
    """rate_of(u) -> pitting per counted quantity; unit_rate_2026(u) -> quantity counted in 2026."""
    res = {}
    for u in UNITS:
        rn = current_runner(u); f = last_inspection(W, rn)
        p0 = f['found'] if f['repaired_to'] is None else f['repaired_to']
        res[u] = p0
    return res


def call(W, mode):
    """mode: 'rz' (golden), 'run_pooled' (R0, peaker set aside), 'run_pooled_all', 'run_own' (R1), 'starts' (R2)."""
    P = pairs(W)
    base = [p for p in P if p[0] not in ('R-207',)]
    if mode == 'rz':
        num = sum(p[4] - p[2] for p in P); den = sum(runner_counts(W, p[0], p[1], p[3], 'rz') for p in P)
        rate = {rn: num / den for rn in Wm.PIT0}; what = 'rz'
    elif mode in ('run_pooled', 'run_pooled_all'):
        use = base if mode == 'run_pooled' else P
        num = sum(p[4] - p[2] for p in use); den = sum(runner_counts(W, p[0], p[1], p[3], 'run') for p in use)
        rate = {rn: num / den for rn in Wm.PIT0}; what = 'run'
    elif mode == 'run_own':
        num = sum(p[4] - p[2] for p in base); den = sum(runner_counts(W, p[0], p[1], p[3], 'run') for p in base)
        rate = {rn: num / den for rn in Wm.PIT0}
        for rn in Wm.PIT0:
            mine = [p for p in P if p[0] == rn]
            if mine:
                p = mine[-1]; rate[rn] = (p[4] - p[2]) / runner_counts(W, rn, p[1], p[3], 'run')
        what = 'run'
    elif mode == 'counters':
        cp = [p for p in counter_pairs(W) if p[0] != 'R-207']
        num = sum(p[3] - p[2] for p in cp); den = sum(p[4] for p in cp)
        rate = {rn: num / den for rn in Wm.PIT0}; what = 'run'
    elif mode == 'starts':
        num = sum(p[4] - p[2] for p in base); den = sum(runner_counts(W, p[0], p[1], p[3], 'starts') for p in base)
        rate = {rn: num / den for rn in Wm.PIT0}; what = 'starts'
    rows = {}
    end = NH
    for u in UNITS:
        rn = current_runner(u); f = last_inspection(W, rn)
        p0 = f['found'] if f['repaired_to'] is None else f['repaired_to']
        q = runner_counts(W, rn, f['i'], end, what)
        now = p0 + rate[rn] * q
        q26 = runner_counts(W, rn, L(2026, 1, 1), end, what)
        cross = None; p = now
        for y in range(2027, 2032):
            p += rate[rn] * q26
            if p >= LIMIT and cross is None:
                cross = y
        # a runner already past the limit at the cut counts as passing in 2027
        if now >= LIMIT:
            cross = 2027
        gen = winter_generation(W, u) if cross is not None else 0.0
        rows[u] = {'runner': rn, 'last_date': local(f['i']).date(), 'last_pitting': p0, 'now': now, 'cross': cross,
                   'gen_mwh': gen, 'per_mnok': gen / QUOTE_MNOK[u], 'rate': rate[rn]}
    order = sorted(UNITS, key=lambda u: -rows[u]['per_mnok'])
    return rows, order


if __name__ == '__main__':
    W = Wm.build()
    for mode in ('run_pooled', 'run_pooled_all', 'run_own', 'counters', 'starts', 'rz'):
        rows, order = call(W, mode)
        print(mode, 'pick', order[0], 'second', order[1], ' '.join(f"{u}:{rows[u]['now']:.0f}/{rows[u]['cross']}/{rows[u]['per_mnok']:.0f}" for u in UNITS))
