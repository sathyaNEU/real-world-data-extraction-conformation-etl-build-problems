"""Tuning probe on the clean truth: per stream truth s, the rungs' estimates and sets."""
import os, sys, datetime as dt, collections
import numpy as np
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import params as P, world as Wm

W = Wm.build()
occ = W['occ']
DAYS = 365
LINE = P.LINE

def doy_of(m, d):
    if m == 2 and d == 29:
        return 59  # treat as 1 March position
    return (dt.date(2025, m, d) - dt.date(2025, 1, 1)).days

recs = []
for j, a in enumerate(occ):
    if not W['resp'][j]:
        continue
    si = W['addr_survey'][a]; code = P.SURVEYS[si][0]; md = P.MODES[W['mode'][j]]
    letter = W['addr_letter'][a]
    mem = W['hh_members'][j]; r = W['respondent'][j]
    f, ag, bm, bd, by = mem[r]
    D = Wm.next_birthday_days(bm, bd, letter)
    recs.append(dict(code=code, mode=md, k=len(mem), D=D, letter=letter, is_min=bool(W['is_min'][j]),
                     conf=int(W['confirm'][j]), resp_f=f, resp_age=ag,
                     hh_f=np.mean([m[0] for m in mem]), hh_age=np.mean([m[1] for m in mem]),
                     mixed=(len(mem) == 2 and mem[0][0] != mem[1][0]), bdoy=doy_of(bm, bd)))

single = [r for r in recs if r['k'] == 1]
emp = np.bincount([r['bdoy'] for r in single], minlength=DAYS).astype(float)[:DAYS]
def smooth(v, w):
    ext = np.concatenate([v[-w:], v, v[:w]])
    k = np.ones(2 * w + 1) / (2 * w + 1)
    return np.convolve(ext, k, mode='valid')
emp_s = smooth(emp, 10); emp_s /= emp_s.sum()
true_d = W['dens']

def null_f(dens, letter):
    l = (letter - dt.date(letter.year, 1, 1)).days
    order = (np.arange(1, DAYS + 1) + l) % DAYS
    f = dens[order]
    return f, np.cumsum(f)

def mle(rows, dens_fn):
    m = [r for r in rows if r['k'] >= 2]
    k = np.array([r['k'] for r in m]); D = np.clip(np.array([r['D'] for r in m]), 1, DAYS)
    comp = np.empty(len(m))
    cache = {}
    for i, r in enumerate(m):
        key = r['letter']
        if key not in cache:
            cache[key] = dens_fn(r['letter'])
        f, F = cache[key]
        Fm = F[D[i] - 1] - f[D[i] - 1]
        comp[i] = k[i] * (1 - Fm) ** (k[i] - 1)
    nll = lambda c: -np.sum(np.log(c * comp + (1 - c)))
    c = minimize_scalar(nll, bounds=(0, 1), method='bounded').x
    return c + (1 - c) * np.mean(1 / k)

cells = collections.OrderedDict()
for r in recs:
    cells.setdefault((r['code'], r['mode']), []).append(r)

uni = lambda letter: (np.full(DAYS, 1 / DAYS), np.arange(1, DAYS + 1) / DAYS)
empf = lambda letter: null_f(emp_s, letter)
truef = lambda letter: null_f(true_d, letter)
sets = collections.defaultdict(list)
print('%-5s %-5s %5s %6s | %6s %7s %7s | %6s %6s %6s %6s' % ('surv', 'mode', 'n2+', 'truth', 'conf', 'femexc', 'ageexc', 'unif', 'emp', 'true', 'own'))
for (code, md), rows in cells.items():
    m = [r for r in rows if r['k'] >= 2]
    truth = np.mean([r['is_min'] for r in m])
    conf = np.mean([r['conf'] != 2 for r in m])
    femexc = np.mean([r['resp_f'] - r['hh_f'] for r in m])
    ageexc = np.mean([r['resp_age'] - r['hh_age'] for r in m])
    zf = femexc / (np.std([r['resp_f'] - r['hh_f'] for r in m]) / np.sqrt(len(m)))
    za = ageexc / (np.std([r['resp_age'] - r['hh_age'] for r in m]) / np.sqrt(len(m)))
    u = mle(rows, uni); e = mle(rows, empf); t = mle(rows, truef)
    s1 = [r for r in rows if r['k'] == 1]
    own = np.bincount([r['bdoy'] for r in s1], minlength=DAYS).astype(float)[:DAYS]
    own_s = smooth(own, 30); own_s /= own_s.sum()
    o = mle(rows, lambda letter: null_f(own_s, letter))
    print('%-5s %-5s %5d %6.3f | %6.3f %+7.3f %+7.2f | %6.3f %6.3f %6.3f %6.3f  zf %+5.1f za %+5.1f n1 %d' % (code, md, len(m), truth, conf, femexc, ageexc, u, e, t, o, zf, za, len(s1)))
    for lab, v in (('truth', truth), ('unif', u), ('emp', e), ('true', t), ('own', o), ('conf', conf)):
        if v < LINE: sets[lab].append(code + '-' + md)
    if abs(zf) > 3 or abs(za) > 3: sets['grid'].append(code + '-' + md)
for lab in ('truth', 'conf', 'grid', 'unif', 'emp', 'true', 'own'):
    print('%-6s %s' % (lab, sets[lab]))
print('E[1/k | k>=2]', np.mean([1 / r['k'] for r in recs if r['k'] >= 2]), 'single n', len(single), 'multi n', sum(1 for r in recs if r['k'] >= 2))
