import sys, time, datetime as dt
from collections import Counter, defaultdict
sys.path.insert(0, '.')
import world, days
D = dt.date
t0 = time.time()
W, rng = world.build_world(111)
calls = world.simulate_ooh(W, rng, {})
print('calls', len(calls), Counter(c['cover'] for c in calls))
late = defaultdict(int)
for (eid, n), r in W.callouts_by_eng_night.items():
    if r['cleared_m'] > 21*60+10:
        late[(n.year, n.month)] += 1
print('day-engineer late clears by month', sorted(late.items()))
days.simulate_days(W, rng, {})
print('rest days', len(W.rest_days), Counter((k[1].year, k[1].month) for k in W.rest_days))
for lab, a, b in [('Q3 2025', D(2025,7,1), D(2025,9,30)), ('Q4 2025', D(2025,10,1), D(2025,12,31)),
                  ('Q1 2026', D(2026,1,1), D(2026,3,31)), ('Q2 2026', D(2026,4,1), D(2026,6,30)),
                  ('Q3 2026', D(2026,7,1), D(2026,9,30))]:
    tot, att, fam = days.tally(W, a, b)
    print(lab, 'missed', tot, 'attended', att, 'rate %.2f%%' % (100*tot/att), dict(sorted(fam.items(), key=lambda x: -x[1])))
print('secs', round(time.time()-t0,1))
import collections
mon = collections.defaultdict(lambda: [0,0])
for r in W.day_records:
    k=(r['date'].year, r['date'].month); mon[k][0]+=len(r['missed']); mon[k][1]+=len(r['jobs'])
print('monthly', [(f"{k[0]}-{k[1]:02d}", round(100*v[0]/v[1],2)) for k,v in sorted(mon.items())])
