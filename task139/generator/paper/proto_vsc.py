import numpy as np, sys, json
P = dict(seed=1, a=0.020, k=2.2, tcomp=0.004, ret_rate=12500, rs_rate=44000, lim=75000, term=60, sev=1150.0, sevk=0.55,
         price=1850.0, knee=95000, rs_start=2026.5, ret_hi_share=0.2, ret_hi=(60000, 110000), hk=0.9, sk=0.45, o_ret=(20000, 70000), o_rs=(25000, 75000), n_ret=26000, n_rs=7000)
P.update(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
rng = np.random.default_rng(P['seed'])
VAL = 2026.75
haz = lambda o: P['a'] / 1000 * (1 + P['hk'] * (np.maximum(o - P['knee'], 0) / 20000.0) ** P['k'])           # claims per mile
sev = lambda o: P['sev'] * (1 + P['sk'] * np.maximum(o - P['knee'], 0) / 20000.0)               # mean cost per claim
C = []
for ch, n, y0, rate, (lo, hi) in (('RET', P['n_ret'], 2019.0, P['ret_rate'], P['o_ret']), ('RS', P['n_rs'], P['rs_start'], P['rs_rate'], P['o_rs'])):
    s = rng.uniform(y0, VAL, n); o0 = rng.uniform(lo, hi, n)
    if ch == 'RET':
        hiq = rng.random(n) < P['ret_hi_share']; o0[hiq] = rng.uniform(P['ret_hi'][0], P['ret_hi'][1], hiq.sum())
    r = rate * np.exp(rng.normal(0, 0.25, n))
    C += list(zip([ch] * n, s, o0, r))
dt = 1 / 12
H = []   # per contract list of (month index, odo mid, miles, claims cost, n claims)
for ch, s, o0, r in C:
    rows = []; t = s; o = o0; m = 0
    while t + dt <= VAL and m < P['term'] and o < o0 + P['lim']:
        miles = min(r * dt, o0 + P['lim'] - o); mid = o + miles / 2
        n = rng.poisson(haz(mid) * miles + P['tcomp'])
        cost = sum(sev(mid) * np.exp(rng.normal(-0.245, 0.7)) for _ in range(n))
        rows.append((m, mid, miles, cost, n)); t += dt; o += miles; m += 1
    H.append(rows)
idx = {'RET': [i for i, c in enumerate(C) if c[0] == 'RET'], 'RS': [i for i, c in enumerate(C) if c[0] == 'RS']}
# 2027 rideshare sales: same odometer-at-sale and mileage distribution as the 2025-26 rideshare sales
rs_new = [(C[i][2], C[i][3]) for i in idx['RS']]
def life_true(o0, r):
    tot = 0; o = o0; m = 0
    while m < P['term'] and o < o0 + P['lim']:
        miles = min(r * dt, o0 + P['lim'] - o); mid = o + miles / 2
        tot += (haz(mid) * miles + P['tcomp']) * sev(mid); o += miles; m += 1
    return tot
truth = np.mean([life_true(o0, r) for o0, r in rs_new])
out = {'truth': truth}
# r0: retail lifetime cost by contract age (cost per contract-month by age, summed over 60 months), x1.2 commercial loading
num = np.zeros(60); den = np.zeros(60)
for i in idx['RET']:
    for (m, mid, miles, cost, n) in H[i]: num[m] += cost; den[m] += 1
out['r0_retail_age_x1.2'] = 1.2 * np.sum(num / np.maximum(den, 1))
# r1: rideshare own cost per contract-month x months of coverage (75k / own mileage rate)
cm = sum(len(H[i]) for i in idx['RS']); cc = sum(x[3] for i in idx['RS'] for x in H[i])
mrate = np.mean([C[i][3] for i in idx['RS']])
out['r1_rs_month_x_cover'] = cc / cm * np.mean([min(P['lim'] / r * 12, P['term']) for o0, r in rs_new])
out['r3_rs_month_x60'] = cc / cm * 60
# r2: pooled cost per mile x 75k
tm = sum(x[2] for rows in H for x in rows); tc = sum(x[3] for rows in H for x in rows)
out['r2_pooled_per_mile'] = tc / tm * P['lim']
# r5: frequency per mile by odometer band x average severity ; r4 golden: cost per mile by odometer band
bands = np.arange(0, 200001, 10000)
mil = np.zeros(len(bands)); cost = np.zeros(len(bands)); cnt = np.zeros(len(bands))
for rows in H:
    for (m, mid, miles, c, n) in rows:
        b = np.searchsorted(bands, mid) - 1; mil[b] += miles; cost[b] += c; cnt[b] += n
cpm = cost / np.maximum(mil, 1); fpm = cnt / np.maximum(mil, 1); avsev = cost.sum() / cnt.sum()
def integ(rate):
    tot = []
    for o0, r in rs_new:
        o = o0; m = 0; s_ = 0
        while m < P['term'] and o < o0 + P['lim']:
            miles = min(r * dt, o0 + P['lim'] - o); mid = o + miles / 2; b = np.searchsorted(bands, mid) - 1
            s_ += rate[b] * miles; o += miles; m += 1
        tot.append(s_)
    return np.mean(tot)
out['r4_golden_cost_per_mile_band'] = integ(cpm)
out['r5_freq_band_x_avgsev'] = integ(fpm * avsev)
# r6: rideshare own cost per contract-month by contract age, linear trend in age extrapolated over the cover
num = np.zeros(60); den = np.zeros(60)
for i in idx['RS']:
    for (m, mid, miles, c_, n) in H[i]: num[m] += c_; den[m] += 1
ok = den > 50; ages = np.arange(60)[ok]; cpa = num[ok] / den[ok]
b = np.polyfit(ages, cpa, 1); bq = np.polyfit(ages, np.log(np.maximum(cpa, 1)), 1)
cover = [min(P['lim'] / r * 12, P['term']) for o0, r in rs_new]
out['r6_rs_age_linear_trend'] = np.mean([sum(max(b[1] + b[0] * a, 0) for a in range(int(round(cv)))) for cv in cover])
out['r6b_rs_age_exp_trend'] = np.mean([sum(np.exp(bq[1] + bq[0] * a) for a in range(int(round(cv)))) for cv in cover])
# r7: retail cost by contract age on an accelerated clock (age x mileage ratio)
ra = num_r = None
nr = np.zeros(60); dr = np.zeros(60)
for i in idx['RET']:
    for (m, mid, miles, c_, n) in H[i]: nr[m] += c_; dr[m] += 1
cr = nr / np.maximum(dr, 1); ratio = P['rs_rate'] / P['ret_rate']
out['r7_retail_age_accelerated'] = np.mean([sum(cr[min(int(a * ratio), 59)] * ratio for a in range(int(round(cv)))) for cv in cover])
top = max(bands[mil > 0]); print('max odometer band with exposure', top, 'miles in top bands', np.round(mil[-8:] / 1e6, 2))
g = out['r4_golden_cost_per_mile_band']; lr = {k: v / g * 84 for k, v in out.items()}
print(json.dumps({k: round(v, 1) for k, v in lr.items()}))
sys.exit()
print('  '.join('%s %.0f (LR %.0f)' % (k, v, lr[k]) for k, v in out.items()))
