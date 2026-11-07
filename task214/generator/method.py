"""The replay of the backup scheme on the first half's nights, for the golden and every rival reader.

Input is a canonical instance table (one completed attempt per row) and a job-run table, either from the
clean truth (world.py) or parsed back from the shipped records (verify.py builds its own copy).
"""
import itertools

import numpy as np

TRIGGER = 1.5           # policy 3.2: a copy once an attempt has run 1.5 times its expected runtime
HISTORY = 14            # policy 3.3: median over the job's previous 14 nightly runs
CAP = 0.05              # policy 2.1: backups launched may add at most 5 per cent to instances run
BANDS = ((30, 1.0), (90, 2.5), (None, 5.0))


def credit(base, late):
    late = np.asarray(late, float)
    return base * np.where(late <= 0, 0.0, np.where(late <= 30, 1.0, np.where(late <= 90, 2.5, 5.0)))


def expected_runtime(T, runs_by_job):
    """Median runtime of the job's instances over its previous HISTORY nightly runs (completed attempts)."""
    exp = np.full(len(T['start']), np.nan)
    for jid, nights in runs_by_job.items():
        hist = []
        for night, ids in nights:
            if hist:
                exp[ids] = np.median(np.concatenate(hist[-HISTORY:]))
            hist.append(T['end'][ids] - T['start'][ids])
    return exp


class Host:
    def __init__(self, T):
        self.T = T
        self.by_start = {}
        self.by_end = {}
        for h in np.unique(T['host']):
            ids = np.where(T['host'] == h)[0]
            self.by_start[h] = ids[np.argsort(T['start'][ids], kind='stable')]
            self.by_end[h] = ids[np.argsort(T['end'][ids], kind='stable')]
        self.maxrt = float((T['end'] - T['start']).max())

    def overlapping(self, i):
        T = self.T
        seg = self.by_start[T['host'][i]]
        s = T['start'][seg]
        c = seg[np.searchsorted(s, T['start'][i] - self.maxrt):np.searchsorted(s, T['end'][i])]
        c = c[T['end'][c] > T['start'][i]]
        return c[c != i]

    def ended_in(self, i, lo, hi):
        seg = self.by_end[self.T['host'][i]]
        e = self.T['end'][seg]
        c = seg[np.searchsorted(e, lo):np.searchsorted(e, hi)]
        return c[c != i]

    def started_in(self, i, lo, hi):
        seg = self.by_start[self.T['host'][i]]
        s = self.T['start'][seg]
        c = seg[np.searchsorted(s, lo, side='right'):np.searchsorted(s, hi, side='right')]
        return c[c != i]


def features(T, exp, cand, H=None, wins=(30, 60, 120)):
    """Per candidate instance: the host's co-tenants before, during and after its run."""
    H = H or Host(T)
    ratio = (T['end'] - T['start']) / exp
    F = {k: np.zeros(len(cand)) for k in ['ov_med', 'ov_max', 'n_ov']}
    for w in wins:
        for k in ('bef', 'aft', 'pool', 'nb', 'na'):
            F['%s%d' % (k, w)] = np.zeros(len(cand))
    for c in (0.3, 0.5, 0.8):
        F['cover%.1f' % c] = np.zeros(len(cand), bool)
    for k, i in enumerate(cand):
        si, ei = T['start'][i], T['end'][i]
        ov = H.overlapping(i)
        r = ratio[ov]
        r = r[np.isfinite(r)]
        F['n_ov'][k] = len(r)
        F['ov_med'][k] = np.median(r) if len(r) else 1.0
        F['ov_max'][k] = r.max() if len(r) else 0.0
        if len(ov):
            cov = np.minimum(T['end'][ov], ei) - np.maximum(T['start'][ov], si)
            slower = (ratio[ov] > ratio[i])
            for c in (0.3, 0.5, 0.8):
                F['cover%.1f' % c][k] = bool(np.any(slower & (cov >= c * (ei - si))))
        for w in wins:
            b = ratio[H.ended_in(i, si - w, si)]
            a = ratio[H.started_in(i, ei, ei + w)]
            b, a = b[np.isfinite(b)], a[np.isfinite(a)]
            F['bef%d' % w][k] = np.median(b) if len(b) else 0.0
            F['aft%d' % w][k] = np.median(a) if len(a) else 0.0
            p = np.concatenate([b, a])
            F['pool%d' % w][k] = np.median(p) if len(p) else 0.0
            F['nb%d' % w][k] = len(b)
            F['na%d' % w][k] = len(a)
    return F


def golden_escape(F, ratio_c, win=60, thr=1.5, rule='pooled', cover=0.5):
    """A copy escapes unless the straggler's own run brackets the host's slowdown.

    Escapes: the host was slow outside the straggler's run (a fault of the host), or a slower co-tenant
    covered most of the straggler's run (the straggler was the one slowed). Otherwise its slowness is its own.
    """
    if rule == 'pooled':
        outside = F['pool%d' % win] >= thr
    elif rule == 'either':
        outside = (F['bef%d' % win] >= thr) | (F['aft%d' % win] >= thr)
    else:
        outside = (F['bef%d' % win] >= thr) & (F['aft%d' % win] >= thr)
    covered = F['cover%.1f' % cover] if cover <= 1 else np.zeros(len(ratio_c), bool)
    return outside | covered


READERS = {
    'textbook': lambda F, r: np.ones(len(r), bool),
    'hostcheck': lambda F, r: (F['n_ov'] > 0) & (F['ov_med'] >= 1.25),
    'magnitude': lambda F, r: r / np.maximum(F['ov_med'], 1e-9) <= 1.6,
    'slowest': lambda F, r: (F['n_ov'] > 0) & (r < F['ov_max']),
    'outside_only': lambda F, r: F['pool60'] >= 1.5,
}


def replay(T, J, exp, cand, escape, dur_override=None):
    """Replay the scheme for every family. escape[k] says whether candidate k's copy runs at the expected
    runtime (True) or repeats the straggler's own run (False). Returns per-family figures."""
    run_t = T['end'] - T['start']
    trig = T['start'] + TRIGGER * exp
    pos = {i: k for k, i in enumerate(cand)}
    fin = T['end'].copy()
    backup_min = np.zeros(len(T['start']))
    for k, i in enumerate(cand):
        bs = trig[i] + T['delay'][i]
        if dur_override is not None:
            dur = dur_override[k]
        else:
            dur = exp[i] if escape[k] else run_t[i] + 1.0
        nf = min(T['end'][i], bs + dur)
        backup_min[i] = max(0.0, nf - bs)
        fin[i] = nf
    out = {}
    for fam in J['families']:
        out[fam] = dict(avoided=0.0, backup_hours=0.0, launched=0, rescued=0, late_runs=0)
    fam_of = T['family']
    for fam in J['families']:
        sel = fam_of == fam
        out[fam]['launched'] = int(np.isin(np.where(sel)[0], cand).sum())
        out[fam]['backup_hours'] = float(backup_min[sel].sum() / 60.0)
    for run in J['sla_runs']:
        ids = run['ids']
        late0 = T['end'][ids].max() + run['commit'] - run['deadline']
        late1 = fin[ids].max() + run['commit'] - run['deadline']
        c0, c1 = credit(run['credit'], late0), credit(run['credit'], late1)
        f = run['family']
        out[f]['avoided'] += float(c0 - c1)
        if late0 > 0:
            out[f]['late_runs'] += 1
            if late1 <= 0:
                out[f]['rescued'] += 1
    return out


def price_cost(out, price_eur_hour):
    for f, v in out.items():
        v['cost'] = v['backup_hours'] * price_eur_hour
        v['net'] = v['avoided'] - v['cost']
    return out


def pairs(out, instances_run, cap=CAP):
    """Every admissible set within the cap, best first. A family is admitted only with a positive net."""
    fams = sorted(out)
    res = []
    for r in (1, 2, 3):
        for S in itertools.combinations(fams, r):
            if sum(out[f]['launched'] for f in S) > cap * instances_run:
                continue
            if any(out[f]['net'] <= 0 for f in S):
                continue
            res.append((sum(out[f]['net'] for f in S), S))
    return sorted(res, reverse=True)
