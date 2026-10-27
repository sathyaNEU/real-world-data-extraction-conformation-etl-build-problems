"""Reads the cut pack back the way the golden does: every figure the golden reports comes from target/, never from
the world. Each reading is the handling the SAP and the systems' documents support."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np

import common as K


def rd(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def utc_of_local(zone, s):
    return K.local_to_utc(zone, dt.datetime.strptime(s, "%Y-%m-%d %H:%M"))


def read(target):
    P = {}
    site_rows = rd(target, K.SITES)
    sites = {int(r['site_number']): r['country'] for r in site_rows}
    zones = {int(r['site_number']): r['time_zone'] for r in site_rows}
    rand = rd(target, K.RAND)
    P['rno2ss'] = {r['randomisation_number']: r['site_subject'] for r in rand}
    P['arm'] = {r['site_subject']: ('dovikizumab' if r['treatment'].startswith('dovikizumab') else 'placebo') for r in rand}
    P['country'] = {ss: sites[int(ss.split('-')[0])] for ss in P['arm']}
    P['zone'] = {ss: zones[int(ss.split('-')[0])] for ss in P['arm']}
    P['base'] = {r['site_subject']: r for r in rd(target, K.BASE)}
    P['inf'] = {}
    for r in rd(target, K.DOSE):
        P['inf'][(r['site_subject'], r['visit'])] = r
    P['conc'] = rd(target, K.CONC)
    P['eff'] = {r['site_subject']: r for r in rd(target, K.EFF_LOCK)}
    P['lab'] = rd(target, K.LAB)
    return P


def troughs(P):
    """valid pre-dose concentrations by subject and visit, in ug/mL: the reportable result of each sample, a sample
    valid only when collected before the infusion started (the laboratory's UTC against the eCRF's local start)"""
    out = {}
    late = 0
    for r in P['conc']:
        if r['reportable'] != 'Y' or r['timepoint'] != 'PRE':
            continue
        ss = P['rno2ss'][r['randomisation_number']]
        inf = P['inf'].get((ss, r['visit']))
        if inf is None:
            continue
        start = utc_of_local(P['zone'][ss], inf['infusion_start_local'])
        coll = dt.datetime.strptime(r['collected_utc'], "%Y-%m-%dT%H:%MZ")
        if coll >= start:
            late += 1
            P.setdefault('late_by', {})
            P['late_by'][(r['visit'], P['arm'][ss])] = P['late_by'].get((r['visit'], P['arm'][ss]), 0) + 1
            continue
        v = r['result']
        if v.startswith('<'):
            x = 0.0
        else:
            x = float(v) / (1000.0 if r['unit'] == 'ng/mL' else 1.0)
        out[(ss, r['visit'])] = x
    P['late_predose'] = late
    return out


def wk12(P):
    out = {}
    for r in P['conc']:
        if r['reportable'] == 'Y' and r['visit'] == 'Week 12':
            ss = P['rno2ss'][r['randomisation_number']]
            v = r['result']
            out[ss] = 0.0 if v.startswith('<') else float(v) / (1000.0 if r['unit'] == 'ng/mL' else 1.0)
    return out


def analysis_set(P):
    """600 mg patients with a valid week-4 trough, their week-8 and week-12 concentrations, remission and covariates"""
    T = troughs(P)
    C12 = wk12(P)
    rows = []
    for ss, arm in P['arm'].items():
        if arm != 'dovikizumab':
            continue
        e = P['eff'].get(ss)
        rem = 1 if (e and e['clinical_remission'] == 'Y') else 0
        b = P['base'][ss]
        rows.append(dict(ss=ss, rem=rem, tr4=T.get((ss, 'Week 4')), tr8=T.get((ss, 'Week 8')), c12=C12.get(ss),
                         prior=1 if b['prior_advanced_therapy_failure'] == 'Y' else 0, wt=float(b['weight_kg']),
                         mayo=int(b['modified_mayo_score'])))
    return rows
