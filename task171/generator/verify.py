"""An independent recomputation of every graded figure from target/ alone, written apart from the generator (no
generator module imported): its own readers, its own time-zone conversion, its own logistic fit (Newton steps rather than
the golden's quasi-Newton), its own episode, draw and handset reconstructions. Each figure is compared with
generator/figures.json at the figure's rounding.

    python3 task171/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")


def rd(name):
    with open(os.path.join(T, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def newton_logit(X, y):
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-(X @ b)))
        g = X.T @ (y - p)
        H = (X * (p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-12:
            break
    return b


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    zone = {r['site_number']: r['time_zone'] for r in rd("cvn2184_201_site_list.csv")}
    rand = rd("cvn2184_201_randomisation_log.csv")
    ss_of = {r['randomisation_number']: r['site_subject'] for r in rand}
    arm = {r['site_subject']: ('dovikizumab' if r['treatment'].startswith('dovikizumab') else 'placebo') for r in rand}
    base = {r['site_subject']: r for r in rd("cvn2184_201_baseline_characteristics.csv")}
    inf = {(r['site_subject'], r['visit']): r for r in rd("cvn2184_201_infusion_records.csv")}
    lock = {r['site_subject']: r['clinical_remission'] == 'Y' for r in rd("cvn2184_201_efficacy_database_lock.csv")}
    out = {}

    # ---- the call ----
    tr, c12, late = {}, {}, {}
    for r in rd("cvn2184_201_serum_concentrations.csv"):
        if r['reportable'] != 'Y':
            continue
        ss = ss_of[r['randomisation_number']]
        v = r['result']
        x = 0.0 if v.startswith('<') else float(v) / (1000.0 if r['unit'] == 'ng/mL' else 1.0)
        if r['visit'] == 'Week 12':
            c12[ss] = x
            continue
        if r['timepoint'] != 'PRE' or (ss, r['visit']) not in inf:
            continue
        loc = dt.datetime.strptime(inf[(ss, r['visit'])]['infusion_start_local'], "%Y-%m-%d %H:%M")
        start = loc.replace(tzinfo=ZoneInfo(zone[ss.split('-')[0]])).astimezone(dt.timezone.utc).replace(tzinfo=None)
        if dt.datetime.strptime(r['collected_utc'], "%Y-%m-%dT%H:%MZ") >= start:
            if arm[ss] == 'dovikizumab':
                late[r['visit']] = late.get(r['visit'], 0) + 1
            continue
        tr[(ss, r['visit'])] = x
    out["predose.after_start.week4_dovikizumab"] = late.get('Week 4', 0)
    out["predose.after_start.week8_dovikizumab"] = late.get('Week 8', 0)
    act = [ss for ss in arm if arm[ss] == 'dovikizumab']
    out["arm.dovikizumab_patients"] = len(act)
    S = [ss for ss in act if tr.get((ss, 'Week 4'), 0) > 0]
    out["analysis_set.patients"] = len(S)
    y = np.array([1.0 if lock.get(ss) else 0.0 for ss in S])
    x = np.array([tr[(ss, 'Week 4')] for ss in S])
    st = np.array([1.0 if base[ss]['prior_advanced_therapy_failure'] == 'Y' else 0.0 for ss in S])
    X = np.column_stack([np.ones(len(S)), np.log(x), st])
    b = newton_logit(X, y)
    fc = {}
    for d in (300, 600, 900):
        Xd = X.copy()
        Xd[:, 1] = np.log(x * d / 600.0)
        fc[d] = float(np.mean(1 / (1 + np.exp(-(Xd @ b)))) * 100)
        out["forecast.%d_mg_pct" % d] = round(fc[d], 1)
        out["below_highest.%d_mg_points" % d] = round(max(fc.values()) - fc[d], 1) if d == 900 else None
    for d in (300, 600, 900):
        out["below_highest.%d_mg_points" % d] = round(max(fc.values()) - fc[d], 1)
    top = max(fc.values())
    out["call.dose_mg"] = min(d for d in fc if fc[d] >= top - 5.0)
    out["observed.remission_in_set_pct"] = round(y.mean() * 100, 1)
    q = np.quantile(x, [0.25, 0.5, 0.75])
    grp = np.digitize(x, q)
    for k in range(4):
        out["quartile.%d.remission_pct" % (k + 1)] = round(y[grp == k].mean() * 100, 0)
    for key, nm in (('Week 4', 'week4'), ('Week 8', 'week8'), ('Week 12', 'week12')):
        vals = [(c12.get(ss) if key == 'Week 12' else tr.get((ss, key)), lock.get(ss)) for ss in act]
        vals = [(v, r_) for v, r_ in vals if v]
        lr = np.array([np.log(v) for v, r_ in vals if r_])
        ln = np.array([np.log(v) for v, r_ in vals if not r_])
        out["gmr.remitters_to_nonremitters.%s" % nm] = round(float(np.exp(lr.mean() - ln.mean())), 2)
    # the standing family: the week-4 trough under each covariate set, over the set and with the missing counted
    wt = np.array([np.log(float(base[ss]['weight_kg']) / 72) for ss in S])
    my = np.array([float(base[ss]['modified_mayo_score']) - 7 for ss in S])
    gaps = []
    for cols in ((), (st,), (st, wt, my)):
        Xc = np.column_stack([np.ones(len(S)), np.log(x)] + list(cols))
        bc = newton_logit(Xc, y)
        for denom in (len(S), len(act)):
            f_ = {}
            for d in (300, 600, 900):
                Xd = Xc.copy()
                Xd[:, 1] = np.log(x * d / 600.0)
                f_[d] = float(np.sum(1 / (1 + np.exp(-(Xd @ bc)))) / denom * 100)
            gaps.append(max(f_.values()) - f_[300])
    out["standing.widest_gap_300_mg_points"] = round(max(gaps[0::2]), 2)
    # the stated inputs the write-up cites: the charter's candidates and rule, the unit conversion, SAP 6.10's
    # reference days, the rate's base and the sections cited
    out["inputs.candidate_doses_mg"] = [300, 600, 900]
    out["inputs.charter_rule_points"] = 5.0
    out["inputs.ng_per_ug"] = 1000
    out["inputs.diary_reference_days"] = [43, 57, 71]
    out["inputs.rate_per_patient_years"] = 100
    out["inputs.sections_cited"] = ["5.2", "6.2", "6.6", "6.7", "6.8", "6.10"]
    # the late rung: week-8 trough, stratum, same scaling
    S8 = [ss for ss in act if tr.get((ss, 'Week 8'), 0) > 0]
    y8 = np.array([1.0 if lock.get(ss) else 0.0 for ss in S8])
    x8 = np.array([tr[(ss, 'Week 8')] for ss in S8])
    X8 = np.column_stack([np.ones(len(S8)), np.log(x8),
                          [1.0 if base[ss]['prior_advanced_therapy_failure'] == 'Y' else 0.0 for ss in S8]])
    b8 = newton_logit(X8, y8)
    for d in (300, 900):
        Xd = X8.copy()
        Xd[:, 1] = np.log(x8 * d / 600.0)
        out["rung.late_exposure.%d_mg_pct" % d] = round(float(np.mean(1 / (1 + np.exp(-(Xd @ b8)))) * 100), 0)

    # ---- shared: infusion dates and the last visit ----
    first, last, days = {}, {}, defaultdict(set)
    for (ss, v), r in inf.items():
        d = dt.date.fromisoformat(r['infusion_start_local'][:10])
        first[ss] = min(first.get(ss, d), d)
        last[ss] = max(last.get(ss, d), d)
        days[ss].add(d)
    lastvis = {}
    for r in rd("cvn2184_201_visit_dates.csv"):
        d = dt.date.fromisoformat(r['visit_date'])
        lastvis[r['site_subject']] = max(lastvis.get(r['site_subject'], d), d)

    # ---- ask A: episodes chained review to review while ongoing, the form as it stood at the latest review ----
    order = {"Screening": 0, "Week 4": 1, "Week 8": 2, "Week 12": 3, "Early termination": 3}
    recs = sorted(rd("cvn2184_201_adverse_events.csv"),
                  key=lambda r: (r['site_subject'], order[r['recorded_at_visit']], int(r['ae_number'])))
    eps, live = [], {}
    for r in recs:
        k = (r['site_subject'], r['preferred_term'])
        e = live.get(k)
        if e is None or e['vis'] == order[r['recorded_at_visit']]:
            e = dict(ss=r['site_subject'], pt=r['preferred_term'], soc=r['system_organ_class'], serious=False)
            eps.append(e)
        e['onset'] = r['onset_date']
        e['vis'] = order[r['recorded_at_visit']]
        e['serious'] |= r['serious'] == 'Y'
        if r['ongoing'] == 'Y':
            live[k] = e
        else:
            live.pop(k, None)

    def onset(e):
        s = e['onset']
        if s.endswith('UN'):
            m = dt.date(int(s[:4]), int(s[5:7]), 1)
            f = first[e['ss']]
            return f if (f.year, f.month) == (m.year, m.month) else m
        return dt.date.fromisoformat(s)

    def window_end(ss):
        return min(last[ss] + dt.timedelta(days=30), lastvis[ss])
    irr_pts = {"Infusion related reaction", "Hypersensitivity", "Urticaria", "Flushing", "Chills", "Infusion site reaction"}
    for a in ('dovikizumab', 'placebo'):
        mine = [e for e in eps if arm.get(e['ss']) == a and e['ss'] in first]
        te = [e for e in mine if first[e['ss']] <= onset(e) <= window_end(e['ss'])]
        si = [e for e in te if e['soc'] == "Infections and infestations" and e['serious']]
        irr = [e for e in te if e['pt'] in irr_pts and any(0 <= (onset(e) - d).days <= 1 for d in days[e['ss']])]
        py = sum(((window_end(ss) - first[ss]).days + 1) / 365.25 for ss in arm if arm[ss] == a and ss in first)
        out["askA.%s.patients_serious_infection" % a] = len({e['ss'] for e in si})
        out["askA.%s.patients_infusion_reaction" % a] = len({e['ss'] for e in irr})
        out["askA.%s.serious_infections_per_100py" % a] = round(100 * len(si) / py, 1)

    # ---- ask B: a draw is the patient's blood on a collection date; each tier's latest accepted result ----
    runs = {r['run_id']: r for r in rd("brightwater_ada_run_log.csv")}
    res = rd("cvn2184_201_ada_results.csv")
    label = defaultdict(set)
    for r in res:
        if r['manifest_visit'] != 'Unscheduled':
            label[(r['randomisation_number'], r['collection_date'])].add(r['manifest_visit'])
    draws = defaultdict(list)
    for r in res:
        if runs[r['run_id']]['plate_acceptance'] == 'accepted' and label.get((r['randomisation_number'], r['collection_date'])):
            draws[(r['randomisation_number'], r['collection_date'])].append(r)
    status = {}
    for k, rr in draws.items():
        best = {}
        for r in sorted(rr, key=lambda z: (runs[z['run_id']]['run_date'], z['run_id'])):
            best[r['tier']] = r
        if 'screening' not in best:
            continue
        pos = (float(best['screening']['result']) >= 1.32 and 'confirmatory' in best
               and float(best['confirmatory']['result']) >= 18.5)
        titer = int(best['titer']['result'].split(':')[1]) if pos and 'titer' in best else 0
        (vis,) = label[k]
        status[(k[0], vis)] = (pos, titer)
    for a in ('dovikizumab', 'placebo'):
        for vis, nm in (('Week 4', 'week4'), ('Week 8', 'week8'), ('Week 12', 'week12')):
            n = te = 0
            for rno, ss in ss_of.items():
                if arm[ss] != a or (rno, 'Week 0') not in status or (rno, vis) not in status:
                    continue
                b0, bx = status[(rno, 'Week 0')], status[(rno, vis)]
                n += 1
                te += int((not b0[0] and bx[0]) or (b0[0] and bx[0] and bx[1] >= 4 * b0[1]))
            out["askB.%s.%s.te_ada_pct" % (a, nm)] = round(100.0 * te / n, 1)

    # ---- ask C: the handset's holder on the diary date, an unknown registration traced through the handover ----
    dev = rd("cvn2184_201_ediary_handset_log.csv")
    known = set(arm)
    alias = {}
    for _ in range(5):
        for r in dev:
            u = r['site_subject']
            if u in known or u in alias:
                continue
            for q in dev:
                w = alias.get(q['site_subject'], q['site_subject'])
                if q['handset_serial'] == r['handset_serial'] and q['returned_on'] == r['dispensed_on'] and w in known:
                    alias[u] = w
    hold = defaultdict(list)
    for r in dev:
        hold[r['handset_serial']].append((r['dispensed_on'], r['returned_on'], alias.get(r['site_subject'], r['site_subject'])))
    day = {}
    for r in rd("cvn2184_201_ediary_entries.csv"):
        for a0, b0, ss in hold[r['handset_serial']]:
            if a0 <= r['diary_date'] < b0:
                k = (ss, r['diary_date'])
                if k not in day or r['recorded_at'] > day[k][0]:
                    day[k] = (r['recorded_at'], int(r['stool_frequency']), int(r['rectal_bleeding']))
    for a in ('dovikizumab', 'placebo'):
        for w, ref in ((6, 42), (8, 56), (10, 70)):
            rem = 0
            for ss in arm:
                if arm[ss] != a or ss not in first:
                    continue
                refd = first[ss] + dt.timedelta(days=ref)
                if lastvis[ss] < refd:
                    continue
                got = [day[(ss, str(refd - dt.timedelta(days=k)))] for k in range(1, 8)
                       if (ss, str(refd - dt.timedelta(days=k))) in day][:3]
                if len(got) < 3:
                    continue
                sf = int(np.floor(np.mean([g[1] for g in got]) + 0.5)) - int(base[ss]['normal_stool_frequency'])
                sfs = 0 if sf <= 0 else (1 if sf <= 2 else (2 if sf <= 4 else 3))
                rbs = int(np.floor(np.mean([g[2] for g in got]) + 0.5))
                rem += int(sfs <= 1 and rbs == 0)
            out["askC.%s.week%d.symptomatic_remission_patients" % (a, w)] = rem

    bad = []
    for k, v in out.items():
        if k not in fig:
            bad.append("%s not in figures.json" % k)
        elif fig[k] != v:
            bad.append("%s: verify %s, figures.json %s" % (k, v, fig[k]))
    missing = [k for k in fig if k not in out]
    for k in missing:
        bad.append("%s in figures.json, not recomputed" % k)
    if bad:
        print("verify: %d of %d disagree" % (len(bad), len(fig)))
        for b_ in bad:
            print("  " + b_)
        raise SystemExit(1)
    print("verify: %d of %d figures recomputed and equal" % (len(out), len(fig)))


if __name__ == "__main__":
    main()
