"""Family screen on several paper worlds: truth, the one-clock family, the two-clock family."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sim_rev as S
import routes as R

seeds = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [1, 2, 3]
over = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
S.P.update(over)
for seed in seeds:
    cases, log, states = S.record(seed)
    fel, pet, close = R.visible(cases, log, states)
    R.CASE.clear(); R.CASE.update({c['id']: c for c in fel})
    ids = set(R.CASE)
    pet = [p for p in pet if p['case'] in ids]
    pers = sum(1 for p in pet if p['revoked'] and S.EXTRACT - 365 < p['decided'] <= S.EXTRACT)
    t, sd = S.truth(seed, cases, log, states, reps=8)
    oc = R.one_clock(fel, pet, close)
    ob = R.one_clock(fel, pet, close, by_term=True)
    fam = {}
    for w in (60, 90, 120):
        for sa in (True, False):
            v, parts, est = R.two_clock(fel, pet, close, window=w, score_adjust=sa)
            fam[(w, sa)] = v
    r3, _, _ = R.two_clock(fel, pet, close, skip_transition=True)
    ov, _, _ = R.two_clock(fel, pet, close, double_count=True)
    vals = np.array(list(fam.values()))
    print('   rung: two-clock without the transition reviews %.0f (%.2fx); over-correction %.0f (%.2fx); persistence %d, one-clock %.0f' % (r3, r3 / t, ov, ov / t, pers, oc))
    print('seed %d truth %.0f (sd %.0f) | persistence %.2fx | one-clock %.2fx, by term %.2fx | two-clock %.3fx to %.3fx (w90 %.3fx)' % (
        seed, t, sd, pers / t, oc / t, ob / t, vals.min() / t, vals.max() / t, fam[(90, True)] / t))
    print('   EXACT seed %d: truth %.0f persistence %d one-clock %.0f by-term %.0f no-transition %.0f golden %.0f (members %.0f to %.0f) over %.0f' % (
        seed, t, pers, oc, ob, r3, fam[(90, True)], vals.min(), vals.max(), ov))
    print('   two-clock members', {('w%d' % k[0]) + ('s' if k[1] else 'n'): round(v) for k, v in fam.items()})
