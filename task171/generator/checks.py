"""task171's generator assertions, run on the cut pack and on the world's clean truth.

    python3 task171/generator/checks.py

The three-rules block (the analyst test executed on the clean truth), every semantic fork of the fork table (SF1 to
SF9, single and as a cross product), the standing family and the default path's late family, the ladder floors, the
asks' fairness (each golden equals the world truth exactly) and their rival handlings (every cracker and mirror route
outside the bin), and figures.json against a fresh computation."""
from __future__ import annotations

import datetime as dt
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as AK          # noqa: E402
import common as K         # noqa: E402
import events as E         # noqa: E402
import golden as G         # noqa: E402
import pack as PK          # noqa: E402
import pack_read as PR     # noqa: E402
import world as WD         # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
N_OK = [0]


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N_OK[0] += 1


def gap300(fc):
    return max(fc.values()) - fc[300]


# ---- the pack read under each licensed reading of a convention ------------------------------------------------
def troughs_variant(P, start_check=True, reassay='reportable', blq='zero'):
    out = {}
    seen = {}
    for r in P['conc']:
        if r['timepoint'] != 'PRE':
            continue
        if reassay == 'reportable' and r['reportable'] != 'Y':
            continue
        ss = P['rno2ss'][r['randomisation_number']]
        inf = P['inf'].get((ss, r['visit']))
        if inf is None:
            continue
        if start_check:
            start = PR.utc_of_local(P['zone'][ss], inf['infusion_start_local'])
            if dt.datetime.strptime(r['collected_utc'], "%Y-%m-%dT%H:%MZ") >= start:
                continue
        v = r['result']
        if v.startswith('<'):
            if blq == 'drop':
                continue
            x = 0.0 if blq == 'zero' else 0.05
        else:
            x = float(v) / (1000.0 if r['unit'] == 'ng/mL' else 1.0)
        key = (ss, r['visit'])
        if reassay == 'first' and key in seen:
            continue
        seen[key] = True
        out[key] = x
    return out


def rows_variant(P, eff=None, **kw):
    T = troughs_variant(P, **kw)
    C12 = PR.wk12(P)
    effs = eff if eff is not None else P['eff']
    rows = []
    for ss, arm in P['arm'].items():
        if arm != 'dovikizumab':
            continue
        e = effs.get(ss)
        b = P['base'][ss]
        rows.append(dict(ss=ss, rem=1 if (e and e['clinical_remission'] == 'Y') else 0, tr4=T.get((ss, 'Week 4')),
                         tr8=T.get((ss, 'Week 8')), c12=C12.get(ss),
                         prior=1 if b['prior_advanced_therapy_failure'] == 'Y' else 0, wt=float(b['weight_kg']),
                         mayo=int(b['modified_mayo_score'])))
    return rows


def main():
    P = PR.read(TARGET)
    F = G.compute(TARGET)
    rows = PR.analysis_set(P)
    import re
    describing = re.compile(r"dictionar|manifest|readme|read_me|field_?notes|field_?guide|codebook|schema|definition|"
                            r"extract_?notes|export_?notes|notes", re.I)
    ok(not [f_ for f_ in os.listdir(TARGET) if describing.search(f_)],
       "section 3: no file named as a dictionary, manifest, readme or notes ships")

    # ---- the call and the standing family ----
    ok(F['call'] == 300, "the golden call is 300 mg")
    ok(gap300(F['fc']) <= 1.0, "300 mg within a point of the highest forecast: %.2f" % gap300(F['fc']))
    for k, fc in F['fam'].items():
        ok(K.call(fc) == 300, "standing member %s files 300" % (k,))
        ok(gap300(fc) <= 3.0, "standing member %s keeps 300 mg within 3 points (%.2f)" % (k, gap300(fc)))
    # ---- the default path's late family (Ends on: 900 mg) ----
    for k, fc in F['late_fam'].items():
        ok(K.call(fc) == 900, "late member %s files 900" % (k,))
        ok(fc[900] - fc[300] >= 15.0, "late member %s: 300 mg at least 15 points under 900 mg" % (k,))
        ok(fc[900] - fc[600] >= 5.5, "late member %s: 600 mg over 5 points under 900 mg" % (k,))
    # the ruling-out group-by: remitters' to non-remitters' geometric mean concentration by visit
    ok(0.90 <= F['gmr']['tr4'] <= 1.15, "week-4 ratio flat: %.2f" % F['gmr']['tr4'])
    ok(F['gmr']['tr8'] >= 1.8 and F['gmr']['c12'] >= 2.5, "later ratios apart: %.2f, %.2f" % (F['gmr']['tr8'], F['gmr']['c12']))

    # ---- the semantic fork table ----
    # SF1 the forecast's population: the exposure-response analysis set (charter 4) against counting the patients
    # without a valid week-4 trough as non-remitters; same call
    alt = G.forecast(rows, 'tr4', 'strat', nonremit_missing=True)[0]
    ok(K.call(alt) == 300 and gap300(alt) <= 3.0, "SF1 same call")
    # SF2 dose scaling: in proportion to dose (investigator's brochure 5.2) against no scaling (every forecast equal,
    # so the lowest dose is within the rule); same call
    flat = {d: F['fc'][600] for d in K.DOSES}
    ok(K.call(flat) == 300, "SF2 same call")
    # SF3 the remission flags: database lock against the topline extract (local endoscopy reads); same call
    top = {r['site_subject']: r for r in PR.rd(TARGET, K.EFF_TOP)}
    alt = G.forecast(rows_variant(P, eff=top), 'tr4', 'strat')[0]
    ok(K.call(alt) == 300, "SF3 same call")
    # SF4 pre-dose validity: the laboratory's UTC collection against the infusion's local start converted to UTC
    # (SAP 6.8) against keeping every pre-dose sample as labelled; same call
    alt = G.forecast(rows_variant(P, start_check=False), 'tr4', 'strat')[0]
    ok(K.call(alt) == 300, "SF4 same call")
    # SF5 reassays: the reportable result against the first result delivered; same call
    alt = G.forecast(rows_variant(P, reassay='first'), 'tr4', 'strat')[0]
    ok(K.call(alt) == 300, "SF5 same call")
    # SF6 units: results reported in ng/mL are divided by 1,000 (the unit column); the reading is closed by the column
    ng = [r for r in P['conc'] if r['unit'] == 'ng/mL' and not r['result'].startswith('<')]
    ok(ng and all(1.0 <= float(r['result']) / 1000.0 <= 400.0 for r in ng) and
       all(float(r['result']) > 400.0 for r in ng), "SF6 the ng/mL rows sit in range only once converted")
    # SF7 below-limit results: zero, half the limit or left out; same call
    for blq in ('zero', 'half', 'drop'):
        alt = G.forecast(rows_variant(P, blq=blq), 'tr4', 'strat')[0]
        ok(K.call(alt) == 300, "SF7 %s same call" % blq)
    # SF8 the model's covariates: none, the randomisation stratum, the stratum with weight and modified Mayo; same call
    for cov in ('none', 'strat', 'full'):
        ok(K.call(G.forecast(rows, 'tr4', cov)[0]) == 300, "SF8 %s same call" % cov)
    # SF9 the rule compared on forecasts rounded to one decimal against unrounded (charter 5); same call
    ok(K.call({d: round(v, 1) for d, v in F['fc'].items()}) == 300, "SF9 same call")
    # SF10 the infusion start's clock: each site's own zone against every US site on Eastern time; same call
    P2 = dict(P)
    P2['zone'] = {ss: ('America/New_York' if z.startswith('America/') and P['country'][ss] == 'US' else z)
                  for ss, z in P['zone'].items()}
    alt = G.forecast(rows_variant(P2), 'tr4', 'strat')[0]
    ok(K.call(alt) == 300, "SF10 same call")
    # the live rows as a cross product
    for sf1, sf4, sf5, sf7, sf8 in itertools.product((False, True), (True, False), ('reportable', 'first'),
                                                     ('zero', 'half', 'drop'), ('none', 'strat', 'full')):
        rr = rows_variant(P, start_check=sf4, reassay=sf5, blq=sf7)
        fc = G.forecast(rr, 'tr4', sf8, nonremit_missing=sf1)[0]
        ok(K.call(fc) == 300, "cross product SF1 %s SF4 %s SF5 %s SF7 %s SF8 %s files 300" % (sf1, sf4, sf5, sf7, sf8))

    # ---- the three rules: the analyst test executed on the world's clean truth ----
    W = WD.simulate()
    PK.ids(W)
    clean = []
    for i in range(W.N):
        if not W.act[i]:
            continue
        clean.append(dict(ss=W.ssid[i], rem=int(W.rem[i]), tr4=WD.conc_at(W, i, 27.75), tr8=WD.conc_at(W, i, 55.75),
                          c12=WD.conc_at(W, i, 84.0), prior=int(W.biol[i]), wt=float(W.wt[i]), mayo=int(W.mmayo0[i])))
    for key in ('tr8', 'c12'):
        for cov in ('none', 'strat', 'full'):
            fc = G.forecast(clean, key, cov)[0]
            ok(K.call(fc) == 900, "analyst test on clean truth: %s %s files 900" % (key, cov))
    for cov in ('none', 'strat', 'full'):
        fc = G.forecast(clean, 'tr4', cov)[0]
        ok(K.call(fc) == 300, "golden construction on clean truth: tr4 %s files 300" % cov)
    # the world's own answer: the true remission at each dose puts 300 mg within the rule
    true = {300: W.rem300[W.act].mean() * 100, 600: W.rem[W.act].mean() * 100, 900: W.rem900[W.act].mean() * 100}
    ok(K.call(true) == 300, "the world's true remission files 300 (%s)" % {d: round(v, 1) for d, v in true.items()})

    # ---- the asks: fair (golden equals the world truth) ----
    eps = E.adverse_events(W)
    ta = E.truth_ae(W, eps)
    ga = AK.ask_a(P, TARGET)
    for arm in ga:
        for k in ('pts_si', 'pts_irr', 'events_si'):
            ok(ga[arm][k] == ta[arm][k], "ask A %s %s golden equals the truth" % (arm, k))
        ok(abs(ga[arm]['py'] - sum(E.exposure_years(W, i) for i in range(W.N)
                                   if bool(W.act[i]) == (arm == 'dovikizumab'))) < 1e-9, "ask A %s exposure" % arm)
    A = E.ada(W)
    tb = E.truth_ada(W, A)
    gb = AK.ask_b(P, TARGET)
    for arm in gb:
        for k, vis in ((1, 'Week 4'), (2, 'Week 8'), (3, 'Week 12')):
            ok((gb[arm][vis]['te'], gb[arm][vis]['n']) == (tb[arm][k]['te'], tb[arm][k]['n']),
               "ask B %s %s golden equals the truth" % (arm, vis))
    D = E.diaries(W)
    tc = E.truth_symptomatic(W, D)
    gc = AK.ask_c(P, TARGET)
    for arm in gc:
        for w, ref in K.DIARY_WEEKS:
            ok(gc[arm][w]['rem'] == tc[arm][ref]['rem'], "ask C %s week %d golden equals the truth" % (arm, w))

    # ---- the asks: every rival handling outside the bin ----
    def figs_a(a):
        return {(arm, k): (a[arm][k] if k != 'rate_si' else round(a[arm][k], 1)) for arm in a for k in ('pts_si', 'pts_irr', 'rate_si')}
    def figs_b(b):
        return {(arm, v): round(b[arm][v]['pct'], 1) for arm in b for v in b[arm]}
    def figs_c(c):
        return {(arm, w): c[arm][w]['rem'] for arm in c for w in c[arm]}
    gold = dict(A=figs_a(ga), B=figs_b(gb), C=figs_c(gc))
    rivals = dict(A=('onset_key', 'first_onset', 'records', 'by_term'), B=('by_visit', 'per_sample', 'latest'),
                  C=('drop_unmatched', 'current_holder'))
    fn = dict(A=(AK.ask_a, figs_a), B=(AK.ask_b, figs_b), C=(AK.ask_c, figs_c))
    for ask, hows in rivals.items():
        f, figs = fn[ask]
        for how in hows:
            alt = figs(f(P, TARGET, how))
            for key, g in gold[ask].items():
                if ask == 'A' and key[1] == 'pts_si' and how == 'records':
                    continue        # the record count keys episodes the same way for the patient count
                if ask == 'B' and how in ('latest', 'per_sample') and key == ('placebo', 'Week 12'):
                    continue        # the per-sample rungs' one kept figure (the mirror's row on the ask sheet)
                tol = 0.05 if isinstance(g, float) else 0.5
                ok(abs(alt[key] - g) > tol, "ask %s %s misses %s (%s against %s)" % (ask, how, key, alt[key], g))
    # the IRR rungs: the reaction term alone and the term list on any day
    for how in ('irr_term_only', 'irr_list_any_day'):
        alt = AK.ask_a(P, TARGET, how)
        for arm in alt:
            ok(alt[arm]['pts_irr'] != ga[arm]['pts_irr'], "ask A %s misses %s IRR patients" % (how, arm))

    # ---- figures.json is the computation ----
    stored = json.load(open(os.path.join(HERE, "figures.json")))
    fresh = G.flat(F)
    ok(stored == fresh, "figures.json matches a fresh computation")
    print("checks: %d passed" % N_OK[0])


if __name__ == "__main__":
    main()
