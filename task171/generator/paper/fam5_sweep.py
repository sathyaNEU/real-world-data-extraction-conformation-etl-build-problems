"""Sweep: over worlds, does every standing member call 300 and every default-path member call 900 under the
three-dose rule (lowest dose within THR points of the highest forecast)? Emax left out for speed."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sim_er4 as S
import fam5 as F

args = sys.argv[1:]
if args and args[0].startswith('{'):
    S.P.update(json.loads(args[0]))
    args = args[1:]
n = int(args[0]) if args else 40
thr = float(args[1]) if len(args) > 1 else 5.0
standing_ok = late_ok = both = 0
spread300 = []
gap_clean = []
gap_late = []
for seed in range(1, n + 1):
    w = S.world(seed)
    w['s']['posthoc'] = S.posthoc_cavg(w)
    s = w['s']
    clean = {('tr28', c): F.fit_logit(w, s['tr28'], c) for c in ('none', 'strat', 'full')}
    clean[('tr28', 'tvalb')] = F.fit_logit(w, s['tr28'], 'tvalb', w['alb_at']['tr28'])
    clean[('tr28', 'lin')] = F.fit_logit_lin(w, s['tr28'])
    clean[('iv', 'tr28')] = F.fit_iv(w)
    late = {(m, c): F.fit_logit(w, s[m], c) for m in ('tr56', 'd84', 'mean_tr', 'posthoc') for c in ('none', 'strat', 'full')}
    late[('d84', 'tvalb')] = F.fit_logit(w, s['d84'], 'tvalb', w['alb_at']['d84'])
    cc = [F.call(v, thr) for v in clean.values()]
    lc = [F.call(v, thr) for v in late.values()]
    sok = all(c == 300 for c in cc)
    lok = all(c != 300 for c in lc)
    standing_ok += sok
    late_ok += lok
    both += sok and lok
    v300 = [v[300] for v in clean.values()]
    spread300.append(max(v300) - min(v300))
    gap_clean.append(max(max(v.values()) - v[300] for v in clean.values()))
    gap_late.append(min(max(v.values()) - v[300] for v in late.values()))
print('worlds %d  standing all 300: %d  default all off 300: %d  both: %d' % (n, standing_ok, late_ok, both))
print('standing 300 mg spread median %.2f max %.2f' % (np.median(spread300), max(spread300)))
print('standing worst gap to top: median %.2f p90 %.2f max %.2f' % (np.median(gap_clean), np.quantile(gap_clean, 0.9), max(gap_clean)))
print('default best gap to top: median %.2f p10 %.2f min %.2f' % (np.median(gap_late), np.quantile(gap_late, 0.1), min(gap_late)))
