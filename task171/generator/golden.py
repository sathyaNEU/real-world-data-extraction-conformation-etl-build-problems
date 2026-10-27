"""The golden forecasts and the call, and the exposure-response family around them, computed on the pack."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

import common as K


def logistic_fit(X, y):
    nll = lambda b: np.sum(np.logaddexp(0, X @ b)) - y @ (X @ b)
    grad = lambda b: X.T @ (1 / (1 + np.exp(-(X @ b))) - y)
    return minimize(nll, np.zeros(X.shape[1]), jac=grad, method='BFGS').x


def forecast(rows, key, cov='strat', nonremit_missing=False):
    """logistic exposure-response of week-12 remission on log exposure, exposure scaled in proportion to dose; the
    forecast at each dose is the mean predicted remission over the 600 mg patients, a patient with no exposure value
    left out (the charter's exposure-response analysis set)"""
    use = [r for r in rows if r[key] is not None and r[key] > 0]
    miss = len(rows) - len(use)
    y = np.array([r['rem'] for r in use], float)
    x = np.array([r[key] for r in use])
    cols = [np.ones(len(use)), np.log(x)]
    if cov in ('strat', 'full'):
        cols.append(np.array([r['prior'] for r in use], float))
    if cov == 'full':
        cols += [np.log(np.array([r['wt'] for r in use]) / 72), np.array([r['mayo'] for r in use], float) - 7]
    X = np.column_stack(cols)
    b = logistic_fit(X, y)
    out = {}
    for d in K.DOSES:
        Xd = X.copy()
        Xd[:, 1] = np.log(x * d / 600.0)
        p = 1 / (1 + np.exp(-(Xd @ b)))
        out[d] = (p.sum() / (len(use) + (miss if nonremit_missing else 0))) * 100
    return out, b


def family(rows):
    """the standing family (exposure the dose set: the week-4 trough) and the default path's late-exposure family"""
    fam = {}
    for cov in ('none', 'strat', 'full'):
        fam[('week-4 trough', cov)] = forecast(rows, 'tr4', cov)[0]
        fam[('week-4 trough', cov, 'missing as non-remitters')] = forecast(rows, 'tr4', cov, nonremit_missing=True)[0]
    late = {}
    for key, name in (('tr8', 'week-8 trough'), ('c12', 'week-12 concentration')):
        for cov in ('none', 'strat', 'full'):
            late[(name, cov)] = forecast(rows, key, cov)[0]
    return fam, late


def golden(rows):
    fc, b = forecast(rows, 'tr4', 'strat')
    return dict(fc=fc, call=K.call(fc), coef=b, n=sum(1 for r in rows if r['tr4']), rows=len(rows))


def compute(target):
    import pack_read as PR
    import asks as AK
    P = PR.read(target)
    rows = PR.analysis_set(P)
    g = golden(rows)
    fam, late = family(rows)
    std = [v for k, v in fam.items() if len(k) == 2]
    use = [r for r in rows if r['tr4']]
    x = np.array([r['tr4'] for r in use])
    y = np.array([r['rem'] for r in use])
    qs = np.quantile(x, [0.25, 0.5, 0.75])
    grp = np.digitize(x, qs)
    quart = [dict(lo=float(x[grp == k].min()), hi=float(x[grp == k].max()), n=int((grp == k).sum()),
                  rate=float(y[grp == k].mean() * 100)) for k in range(4)]
    gmr = {}
    for key in ('tr4', 'tr8', 'c12'):
        rr = np.array([r[key] for r in rows if r[key]])
        yy = np.array([r['rem'] for r in rows if r[key]])
        gmr[key] = float(np.exp(np.log(rr[yy == 1]).mean() - np.log(rr[yy == 0]).mean()))
    lw = late[('week-8 trough', 'strat')]
    F = dict(fc=g['fc'], call=g['call'], n=g['n'], n_arm=g['rows'], obs_set=float(y.mean() * 100), quartiles=quart,
             gmr=gmr, late_300=lw[300], late_900=lw[900], std_lo=min(v[300] for v in std),
             std_hi=max(v[300] for v in std), late=P['late_by'].get(('Week 4', 'dovikizumab'), 0),
             late4=P['late_by'].get(('Week 4', 'dovikizumab'), 0), late8=P['late_by'].get(('Week 8', 'dovikizumab'), 0), fam=fam, late_fam=late,
             ask_a=AK.ask_a(P, target), ask_b=AK.ask_b(P, target), ask_c=AK.ask_c(P, target))
    F['ask_a']['dovikizumab']['n'] = sum(1 for a in P['arm'].values() if a == 'dovikizumab')
    F['ask_a']['placebo']['n'] = sum(1 for a in P['arm'].values() if a == 'placebo')
    return F


def flat(F):
    out = {"call.dose_mg": F['call'], "analysis_set.patients": F['n'], "arm.dovikizumab_patients": F['n_arm'],
           "predose.after_start.week4_dovikizumab": F['late4'], "predose.after_start.week8_dovikizumab": F['late8'],
           "observed.remission_in_set_pct": round(F['obs_set'], 1)}
    for d in K.DOSES:
        out["forecast.%d_mg_pct" % d] = round(F['fc'][d], 1)
        out["below_highest.%d_mg_points" % d] = round(max(F['fc'].values()) - F['fc'][d], 1)
    for k, nm in (('tr4', 'week4'), ('tr8', 'week8'), ('c12', 'week12')):
        out["gmr.remitters_to_nonremitters.%s" % nm] = round(F['gmr'][k], 2)
    for j, q in enumerate(F['quartiles']):
        out["quartile.%d.remission_pct" % (j + 1)] = round(q['rate'], 0)
    out["standing.widest_gap_300_mg_points"] = round(max(max(v.values()) - v[300] for k, v in F['fam'].items() if len(k) == 2), 2)
    # the stated inputs the write-up cites beside its figures (candidates, the charter's rule, the unit conversion,
    # the diary reference days, the rate's base, the documents' section numbers)
    out["inputs.candidate_doses_mg"] = list(K.DOSES)
    out["inputs.charter_rule_points"] = K.THR
    out["inputs.ng_per_ug"] = 1000
    out["inputs.diary_reference_days"] = [ref + 1 for _, ref in K.DIARY_WEEKS]
    out["inputs.rate_per_patient_years"] = 100
    out["inputs.sections_cited"] = ["5.2", "6.2", "6.6", "6.7", "6.8", "6.10"]
    out["rung.late_exposure.300_mg_pct"] = round(F['late_300'], 0)
    out["rung.late_exposure.900_mg_pct"] = round(F['late_900'], 0)
    for arm in ('dovikizumab', 'placebo'):
        a = F['ask_a'][arm]
        out["askA.%s.patients_serious_infection" % arm] = a['pts_si']
        out["askA.%s.patients_infusion_reaction" % arm] = a['pts_irr']
        out["askA.%s.serious_infections_per_100py" % arm] = round(a['rate_si'], 1)
        for vis in ('Week 4', 'Week 8', 'Week 12'):
            out["askB.%s.%s.te_ada_pct" % (arm, vis.replace(' ', '').lower())] = round(F['ask_b'][arm][vis]['pct'], 1)
        for w, _ in K.DIARY_WEEKS:
            out["askC.%s.week%d.symptomatic_remission_patients" % (arm, w)] = F['ask_c'][arm][w]['rem']
    return out
