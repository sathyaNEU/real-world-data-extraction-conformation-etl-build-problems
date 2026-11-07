"""Go/no-go screens on the clean truth over redraws: one summary line per screen.

python3 screens.py SEED_FROM SEED_TO OUT.json
"""
import json
import sys

import world
import method


def evaluate(seed):
    W = world.simulate(seed)
    n_out = sum(1 for c in W['cases'] if c['kind'] == 'outbreak' and method.in_window(c))
    n_bg = sum(1 for c in W['cases'] if c['kind'] == 'background' and method.in_window(c))
    g, A, S = method.golden(W)
    gtop, glead, gsecond = method.top(g)
    variants = {}
    for name, kw in (('u1_12', dict(kmin=1, kmax=12, weights='flat')), ('u2_14', dict(kmin=2, kmax=14, weights='flat')),
                     ('u3_10', dict(kmin=3, kmax=10, weights='flat')), ('pmf_1_14', dict()),
                     ('pmf_lo_aug', dict(lo=31)), ('u1_14', dict(kmin=1, kmax=14, weights='flat'))):
        r, _, _ = method.golden(W, **kw)
        t, l, s = method.top(r)
        variants[name] = (t, round(l, 2))
    reg = method.register_rates(W)
    rtop, rlead, _ = method.top(reg)
    onset = method.top(method.onset_path(W))
    report = method.top(method.report_path(W))
    return dict(seed=seed, outbreak_cases=n_out, background_cases=n_bg, golden=gtop, golden_lead=round(glead, 2),
                golden_second=gsecond, golden_rate=round(g[gtop], 2), second_rate=round(g[gsecond], 2),
                variants=variants, first_look=method.first_look(W), register=rtop, register_lead=round(rlead, 2),
                onset_path=onset[0], report_path=report[0], dated_event=method.dated_event(W),
                nearest=method.nearest_reservoir(W), cluster_nearest=method.cluster_nearest(W),
                per_record=method.per_record_cells(W), literal_what=rtop)


def main():
    a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rows = [evaluate(s) for s in range(a, b + 1)]
    json.dump(rows, open(out, 'w'), indent=1)
    truth = world.BAD
    n = len(rows)
    def cnt(key):
        return sum(1 for r in rows if r[key] == truth)
    print('screen1 golden=truth %d/%d; lead>=1.2 %d/%d; min lead %.2f; median lead %.2f; outbreak cases %d-%d; background %d-%d'
          % (cnt('golden'), n, sum(1 for r in rows if r['golden_lead'] >= 1.2), n, min(r['golden_lead'] for r in rows),
             sorted(r['golden_lead'] for r in rows)[n // 2], min(r['outbreak_cases'] for r in rows),
             max(r['outbreak_cases'] for r in rows), min(r['background_cases'] for r in rows), max(r['background_cases'] for r in rows)))
    vk = rows[0]['variants'].keys()
    print('screen2 golden variants at truth: ' + ', '.join('%s %d/%d' % (k, sum(1 for r in rows if r['variants'][k][0] == truth), n) for k in vk))
    print('screen3 first look wrong %d/%d (names %s)' % (n - cnt('first_look'), n, sorted({r['first_look'] for r in rows})))
    for key in ('register', 'onset_path', 'report_path', 'dated_event', 'nearest', 'cluster_nearest', 'per_record', 'literal_what'):
        print('screen4 %-15s wrong %d/%d (names %s)' % (key, n - cnt(key), n, sorted({r[key] for r in rows})))


if __name__ == '__main__':
    main()
