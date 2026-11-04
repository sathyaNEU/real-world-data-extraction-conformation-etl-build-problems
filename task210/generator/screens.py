"""The go/no-go screens on the clean truth: the golden family and every rival route, per redraw.

python3 screens.py [n] writes screens.json (n redraws from SEED, 24 by default). checks.py asserts it and re-runs it
when a generator source has changed since it was written. Each redraw is the whole world drawn again from its own seed
(the record's stochastic processes and the physics within its narrow ranges); the record is apportioned on the movements'
observable tip times, as the cut pack shows them.

Families written per redraw:
  golden, v_*   the golden's own method and every defensible treatment of it: the baseline (free intercept; plant
                plus the filed residual; hour or weekday effects on either; the lunch hour out), wind, blast hours,
                trimming, lumped other routes, route-resolved standard calibration, and the physical-scaling reader
                (Haul road 2's per-movement energy carried to the Phase 4 road by every geometry measure);
  o_*           the plant-only and plant-plus-night-ambient baselines, which NMP 5.2's residual rules out;
  r_*, x_*      every rival route and the coordinator's readers."""
import hashlib
import json
import math
import os
import sys
import numpy as np
import world as W
import pack
import geometry

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE = 10 ** 4.4 * 3600.0
CYCLE = 4.5
PLANT_DB = 37.5
SRC = ['world.py', 'pack.py', 'screens.py', 'geometry.py']


def src_hash():
    h = hashlib.sha256()
    for f in SRC:
        h.update(open(os.path.join(HERE, f), 'rb').read())
    return h.hexdigest()[:16]


def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def centred(labels):
    """Effects that average to zero over the record (the fixed baseline keeps its level)."""
    lv = sorted(set(labels))
    D = (labels[:, None] == np.array(lv)[None, :]).astype(float)
    return (D - D.mean(axis=0))[:, 1:]


def hourly_frame(Wd):
    """Working hours (Mon-Fri 07-17 local, haul days, four quarters) with their energy and route counts by the hour of
    each movement's observable tip (the payload sensor's first EMPTY fix)."""
    ends = Wd['ends']; laeq = np.round(Wd['mp1']['laeq'], 1)
    t0 = ends[0] - W.dt.timedelta(minutes=15)
    hours = {}
    night = []
    for i, e in enumerate(ends):
        s = e - W.dt.timedelta(minutes=15)
        loc = s + W.dt.timedelta(hours=W.bst_offset(s))
        hours.setdefault(int((s - t0).total_seconds() // 3600), []).append((loc, 10 ** (laeq[i] / 10) * 900))
        if loc.hour >= 22 or loc.hour < 6:
            night.append(10 ** (laeq[i] / 10))
    haul_days = set((tu + W.dt.timedelta(hours=W.bst_offset(tu))).date() for (tu, *_r) in Wd['loads'])
    keys = sorted(k for k, v in hours.items() if len(v) == 4 and v[0][0].weekday() < 5 and 7 <= v[0][0].hour < 17
                  and v[0][0].date() in haul_days)
    idx = {k: j for j, k in enumerate(keys)}
    E = np.array([sum(x[1] for x in hours[k]) for k in keys])
    l90 = np.round(Wd['mp1']['la90'], 1)
    h90 = {}
    for i, e in enumerate(ends):
        h90.setdefault(int((e - W.dt.timedelta(minutes=15) - t0).total_seconds() // 3600), []).append(10 ** (l90[i] / 10) * 900)
    la90 = np.array([sum(h90[k]) for k in keys])
    routes = sorted(set((f, d) for (_t, _k, f, d, _p, _fl) in Wd['loads']))
    C = np.zeros((len(keys), len(routes)))
    for (_tu, truck, face, dest, pay, tu) in Wd['loads']:
        j = idx.get(int((tu - t0).total_seconds() // 3600))
        if j is not None:
            C[j, routes.index((face, dest))] += 1
    hod = np.array([hours[k][0][0].hour for k in keys])
    wkd = np.array([hours[k][0][0].weekday() for k in keys])
    # the same hours at the logger's own grain: each quarter's energy against the tips in that quarter
    qE, qrow = [], {}
    for k in keys:
        for j in range(4):
            qrow[4 * k + j] = len(qE); qE.append(hours[k][j][1])
    Cq = np.zeros((len(qE), len(routes)))
    for (_tu, truck, face, dest, pay, tu) in Wd['loads']:
        jq = qrow.get(int((tu - t0).total_seconds() // 900))
        if jq is not None:
            Cq[jq, routes.index((face, dest))] += 1
    wt = W.wind_toward(Wd['ws'], Wd['wd'])
    wind = np.array([wt[k] if k < len(wt) else 0.0 for k in keys])
    blast = set(int((W.local_to_utc(tl) - t0).total_seconds() // 3600) for (_d, tl, _f, _b) in Wd['blasts'])
    nob = np.array([k not in blast for k in keys])
    return dict(E=E, C=C, routes=routes, hod=hod, wkd=wkd, wind=wind, nob=nob, keys=keys, la90=la90, Eq=np.array(qE), Cq=Cq,
                night_db=10 * math.log10(float(np.mean(night))))


def rival_geometry(P, lwa, abar, agr, aatm):
    Q = dict(P, agr=agr, aatm=aatm, abar_open=abar['open'], abar_crest=abar['crest'], abar_bund=abar['bund'],
             abar_pit=abar['pit'], abar_plant=abar['plant'])
    out = {}
    for (face, dest), roads in W.ROUTES.items():
        e = 0.0
        for k in roads:
            e += 10 ** ((lwa[0] + W.passage_geometry(k, Q, P['v_loaded'])) / 10) + \
                 10 ** ((lwa[1] + W.passage_geometry(k, Q, P['v_empty'])) / 10)
        out[(face, dest)] = e
    return out


_GEO = {}


def geo_scalings():
    if not _GEO:
        _GEO.update(geometry.scalings(geometry.world_geometry(W)))
    return _GEO


def screen(seed):
    Wd = pack.build_world(seed, gps=False)
    P = Wd['P']
    F = hourly_frame(Wd)
    E, C, R = F['E'], F['C'], F['routes']
    k = R.index(('north', 'crusher'))
    one = np.ones((len(E), 1))
    est = {}
    b = ols(np.c_[one, C], E); est['golden'] = b[1 + k]
    # the baseline family: free intercept (the golden), plant plus the filed residual, hour or weekday effects on either
    resid = round(W.filed_residual(Wd['mp1'], Wd['ends']), 1)
    B = 3600.0 * (10 ** (PLANT_DB / 10) + 10 ** (resid / 10))
    D = (F['hod'][:, None] == np.arange(7, 17)[None, :]).astype(float)
    Dw = (F['wkd'][:, None] == np.arange(5)[None, :]).astype(float)
    Hc, Wc = centred(F['hod']), centred(F['wkd'])
    est['v_fixed_baseline'] = ols(C, E - B)[k]
    est['v_hourFE'] = ols(np.c_[D, C], E)[10 + k]
    est['v_weekdayFE'] = ols(np.c_[Dw, C], E)[5 + k]
    est['v_fixed_hour'] = ols(np.c_[Hc, C], E - B)[Hc.shape[1] + k]
    est['v_fixed_weekday'] = ols(np.c_[Wc, C], E - B)[Wc.shape[1] + k]
    m12 = F['hod'] != 12
    est['v_free_no_lunch_hour'] = ols(np.c_[one, C][m12], E[m12])[1 + k]
    est['v_fixed_no_lunch_hour'] = ols(C[m12], (E - B)[m12])[k]
    est['o_plant_only'] = ols(C, E - 3600.0 * 10 ** (PLANT_DB / 10))[k]
    est['o_plant_night'] = ols(C, E - 3600.0 * (10 ** (PLANT_DB / 10) + 10 ** (F['night_db'] / 10)))[k]
    # the golden's other conventions
    est['v_wind'] = ols(np.c_[one, C, F['wind']], E)[1 + k]
    est['v_noblast'] = ols(np.c_[one, C][F['nob']], E[F['nob']])[1 + k]
    r = E - np.c_[one, C] @ b; keep = np.abs(r) < 3 * r.std()
    est['v_trim'] = ols(np.c_[one, C][keep], E[keep])[1 + k]
    est['v_quarter_hours'] = ols(np.c_[np.ones((len(F['Eq']), 1)), F['Cq']], F['Eq'])[1 + k]
    n2 = C[:, k]; no = C.sum(axis=1) - n2
    est['v_pooled_other'] = ols(np.c_[one, n2, no], E)[1]
    # the physical-scaling reader: Haul road 2's energy carried to the Phase 4 road by each geometry measure
    for name, ratio in geo_scalings().items():
        est['v_geo_' + name] = est['golden'] * ratio
    # rivals
    T = C.sum(axis=1)
    est['r_pooled_all'] = ols(np.c_[one, T], E)[1]
    hop = sum(C[:, j] for j, rr in enumerate(R) if rr[1] == 'crusher'); stk = T - hop
    est['r_crusher_tips'] = ols(np.c_[one, hop, stk], E)[1]
    faces = sorted(set(f for f, d in R))
    Cf = np.c_[[sum(C[:, j] for j, rr in enumerate(R) if rr[0] == f) for f in faces]].T
    est['r_face'] = ols(np.c_[one, Cf], E)[1 + faces.index('north')]
    std = {'open': 0.0, 'crest': 10.0, 'bund': 10.0, 'pit': 10.0, 'plant': 10.0}
    iso = {'open': 0.0, 'crest': 11.5, 'bund': 8.0, 'pit': 11.5, 'plant': 12.0}
    fleet = [W.DECLARED_LWA[m] for (_f, _u, m) in W.FLEET]
    decl = {'': P['lwa_declared'], '_110': 110.0, '_111': 111.0,
            '_fleet': 10 * math.log10(float(np.mean([10 ** (x / 10) for x in fleet])))}
    for suf, lw in decl.items():
        est['r_bs5228_declared' + suf] = rival_geometry(P, (lw, lw), std, 0.0, 0.0)[('north', 'crusher')]
        est['r_bs5228_declared_soft' + suf] = rival_geometry(P, (lw, lw), std, 4.5, 1.9)[('north', 'crusher')]
    for name, ab in (('v_bs5228_routecal', std), ('v_iso9613_routecal', iso)):
        g = rival_geometry(P, (P['lwa_declared'], P['lwa_declared']), ab, 3.0, 1.9)
        pred = C @ np.array([g[rr] for rr in R])
        kcal = ols(np.c_[one, pred], E)[1]
        est[name] = kcal * g[('north', 'crusher')]
    # calibration on the pooled record: measured haulage energy over the pilot (each hour less its LA90 background)
    # against the energy the per-road screening predicts for the pilot's movements
    la90 = F['la90']
    for name, ab in (('r_bs5228_ratio', std), ('r_iso9613_ratio', iso)):
        g = rival_geometry(P, (P['lwa_declared'], P['lwa_declared']), ab, 3.0, 1.9)
        pred = C @ np.array([g[rr] for rr in R])
        kcal = (E.sum() - la90.sum()) / pred.sum()
        est[name] = kcal * g[('north', 'crusher')]
    # the additive reader: face and tip as separate main effects, no interaction
    tips = sorted(set(d for f, d in R))
    Ct = np.c_[[sum(C[:, j] for j, rr in enumerate(R) if rr[1] == t) for t in tips]].T
    ba = ols(np.c_[one, Cf, Ct[:, [tips.index('crusher')]]], E)
    est['r_additive_face_tip'] = ba[1 + faces.index('north')] + ba[1 + len(faces)]
    # the loudest-hours reader: the loudest 3 per cent of working hours against the rest, on every feature a reader
    # can record or read per hour; per-movement calibration on the feature that separates them best
    day_of = {}
    for (d, fcs, trucks, off, sd) in Wd['days']:
        day_of[d] = (fcs, len(trucks))
    loc = [W.dt.datetime(2026, 1, 1) for _ in F['keys']]
    t00 = Wd['ends'][0] - W.dt.timedelta(minutes=15)
    for i, kh in enumerate(F['keys']):
        tu = t00 + W.dt.timedelta(hours=kh)
        loc[i] = tu + W.dt.timedelta(hours=W.bst_offset(tu))
    north_day = np.array([1.0 if 'north' in day_of.get(x.date(), (('', ''), 0))[0] else 0.0 for x in loc])
    trucks_day = np.array([float(day_of.get(x.date(), ((), 0))[1]) for x in loc])
    n_north = Cf[:, faces.index('north')]; n_hop = Ct[:, tips.index('crusher')]
    feats = {'wind toward MP1': F['wind'], 'north face worked (shift report)': north_day, 'trucks on the haul': trucks_day,
             'north face movements': n_north, 'hopper tips': n_hop, 'hopper share of tips': n_hop / np.maximum(T, 1),
             'movements': T, 'blast hour': (~F['nob']).astype(float), 'hour of day': F['hod'].astype(float),
             'north face to hopper movements (route state)': C[:, k]}
    def auc(x, top):
        from scipy.stats import rankdata
        rk = rankdata(x); n1 = top.sum(); n0 = len(x) - n1
        return (rk[top].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    picks = {}
    for share in (0.02, 0.03, 0.05):
        top = E >= np.quantile(E, 1 - share)
        sep = {nm: abs(auc(x, top) - 0.5) for nm, x in feats.items() if np.std(x) > 0}
        picks[share] = max(sep, key=sep.get)
    top3 = E >= np.quantile(E, 0.97)
    sep_menu = {nm: abs(auc(x, top3) - 0.5) for nm, x in feats.items() if np.std(x) > 0 and 'route state' not in nm}
    picks['menu_without_route_state'] = max(sep_menu, key=sep_menu.get)
    pick = picks[0.03]
    cls = {'north face movements': n_north, 'hopper tips': n_hop,
           'north face to hopper movements (route state)': C[:, k], 'north face worked (shift report)': n_north}
    for name, pk in (('x_loudest_hours', pick), ('r_loudest_hours_menu', picks['menu_without_route_state'])):
        if pk in cls:
            x = cls[pk]
            est[name] = ols(np.c_[one, x, T - x], E)[1]
        else:
            est[name] = ols(np.c_[one, T], E)[1]
    nmax = {n: SHARE / v if v > 0 else float('inf') for n, v in est.items()}
    calls = {n: int(math.floor(x / CYCLE)) for n, x in nmax.items()}
    # first look: the busiest pilot hour MP1 kept within 45 dB, at 4.5 movements a truck
    L1h = 10 * np.log10(E / 3600)
    ok = L1h <= 45.0
    calls['r_first_look'] = int(math.floor(T[ok].max() / CYCLE)) if ok.any() else 0
    nmax['r_first_look'] = float(T[ok].max()) if ok.any() else 0.0
    # clean truth: the expected energy of one Haul road 2 movement (its ramp and the road, loaded and empty) under the
    # pilot's wind
    sel = W.passage_sel(P)
    wdb = P['wind_coef'] * np.tanh(F['wind'] / 3.0)
    wf = float(np.mean(10 ** (wdb / 10)))
    me = lambda s, sd: 10 ** (s / 10) * math.exp((sd * math.log(10) / 10) ** 2 / 2)
    e_true = sum(me(sel[rd][0], 1.8) + me(sel[rd][1], 1.5) for rd in W.ROUTES[('north', 'crusher')]) * wf
    e_ext = sum(me(sel[rd][0], 1.8) + me(sel[rd][1], 1.5) for rd in W.EXT_ROUTE) * wf
    nmax['truth'] = SHARE / e_true; calls['truth'] = int(math.floor(nmax['truth'] / CYCLE))
    nmax['truth_phase4'] = SHARE / e_ext; calls['truth_phase4'] = int(math.floor(nmax['truth_phase4'] / CYCLE))
    t0 = Wd['ends'][0] - W.dt.timedelta(minutes=15)
    rq = {}
    for i, e in enumerate(Wd['ends']):
        rq.setdefault(int((e - W.dt.timedelta(minutes=15) - t0).total_seconds() // 3600), []).append(10 ** (Wd['mp1']['res'][i] / 10) * 900)
    Er = np.array([sum(rq[kk]) for kk in F['keys']])
    spec = 10 * np.log10(np.maximum(E - Er, 1.0) / 3600)
    lv = dict(laeq_work_median=float(np.median(L1h)), laeq_work_p90=float(np.percentile(L1h, 90)),
              laeq_work_p5=float(np.percentile(L1h, 5)), laeq_work_p95=float(np.percentile(L1h, 95)),
              specific_over_45=int((spec > 45.0).sum()), specific_p99=float(np.percentile(spec, 99)),
              hours=int(len(E)), hours_over_45=int((L1h > 45.0).sum()), sel_hr2=float(10 * math.log10(est['golden'])),
              filed_residual=resid, night_db=F['night_db'], intercept_db=float(10 * math.log10(b[0] / 3600)))
    return dict(seed=seed, nmax=nmax, calls=calls, levels=lv, loudest_pick={str(k2): v for k2, v in picks.items()})


def run(seeds):
    out = dict(hash=src_hash(), seeds=[screen(s) for s in seeds])
    json.dump(out, open(os.path.join(HERE, 'screens.json'), 'w'), indent=1, sort_keys=True)
    return out


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    res = run([W.SEED + i for i in range(n)])
    for r in res['seeds']:
        c = r['calls']
        print(r['seed'], 'golden %d (%.2f) truth %d' % (c['golden'], r['nmax']['golden'] / CYCLE, c['truth']),
              ' '.join('%s=%d' % (k[2:] if k[:2] in ('r_', 'v_', 'o_', 'x_') else k, v) for k, v in sorted(c.items())
                       if k not in ('golden', 'truth') and not k.startswith('v_geo_')))
