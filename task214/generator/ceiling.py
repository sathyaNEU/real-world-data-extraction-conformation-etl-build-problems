"""Ask-layer ceiling on the cut pack: three responses scored figure by figure against figures.json.

Shares no code with the generator. Each response is a complete pipeline over target/:
  cracker       lands the call, runs the hygiene battery, executes every filed rule and joins every key it holds;
  full includer reads every file in full, acts on every stated fact, runs the standard checks (orphan keys,
                duplicates, unit and clock checks, values against a stated maximum);
  mirror        stops at the register's reservoir and computes the asks the way the files first present them.
python3 ceiling.py [target_dir]
"""
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
from collections import defaultdict

import pyarrow.parquet as pq
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'target')


def f(stem):
    return [os.path.join(dp, x) for dp, _, xs in os.walk(TGT) for x in xs if x.startswith(stem)][0]


def csvrows(stem):
    return list(csv.DictReader(open(f(stem), encoding='utf-8')))


def xlrows(stem, sheet):
    it = load_workbook(f(stem), read_only=True)[sheet].iter_rows(values_only=True)
    h = next(it)
    return [dict(zip(h, r)) for r in it]


def day(s):
    return dt.date.fromisoformat(str(s)[:10])


MONTHS = [(dt.date(2027, 7, 1), dt.date(2027, 7, 31)), (dt.date(2027, 8, 1), dt.date(2027, 8, 31)),
          (dt.date(2027, 9, 1), dt.date(2027, 9, 30)), (dt.date(2027, 10, 1), dt.date(2027, 10, 17))]
PERIODS = [(dt.date(2027, 7, 1), dt.date(2027, 9, 30))]
TYPE_PERIOD = [(dt.date(2027, 7, 1), dt.date(2027, 10, 17))]
CATS = {'Water - Clarity': 'Clarity', 'Water - Taste': 'Taste', 'Water - Odour': 'Odour',
        'Water - Pressure or flow': 'Pressure or flow', 'Water - Continuity of supply': 'Continuity of supply'}
WEBCAT = {'Discoloured water': 'Clarity', 'Taste': 'Taste', 'Smell': 'Odour'}


# ------------------------------------------------------------------ ask 1 readers
def ask1(reader):
    lab = csvrows('community_lab_faecal')
    ref = xlrows('reference_lab_cryptosporidium', 'Typing results')
    tested = [len({r['nhi'] for r in lab if r['town'] == 'Kotare' and a <= day(r['collected']) <= b}) for a, b in MONTHS]
    by_nhi = defaultdict(list)
    for r in lab:
        by_nhi[r['nhi']].append(r)
    par, hom = [0], [0]
    for x in ref:
        src = None
        if x['NHI']:
            pos = [r for r in by_nhi.get(x['NHI'], []) if 'Cryptosporidium antigen DETECTED' in r['result']]
            src = pos[0] if pos else None
        if src is None:
            if reader == 'mirror':
                cd, resident = day(x['Date collected']), True     # the typing report taken as it stands
            else:
                continue                                          # an orphan: residence cannot be shown
        else:
            cd, resident = day(src['collected']), src['town'] == 'Kotare'
        if not resident:
            continue
        for i, (a, b) in enumerate(TYPE_PERIOD):
            if a <= cd <= b:
                if x['Result'] == 'Cryptosporidium parvum':
                    par[i] += 1
                elif x['Result'] == 'Cryptosporidium hominis':
                    hom[i] += 1
    return dict(tested=tested, parvum=par, hominis=hom)


# ------------------------------------------------------------------ ask 2 readers
def ask2(reader):
    reg = pq.read_table(f('rating_connections')).to_pylist()
    by_val = {r['valuation_ref']: r for r in reg}
    by_addr = {}
    for r in reg:
        by_addr.setdefault(r['property_address'], r)
    crm = csvrows('crm_water_contacts')
    web = csvrows('website_water_quality')
    ev = []
    for c in crm:
        cat = CATS.get(c['category'])
        if not cat:
            continue
        if reader != 'mirror':
            p = by_val.get(c['valuation_ref']) if c['valuation_ref'] else by_addr.get(c['address_as_given'].split(',')[0].strip())
            if p is None and reader == 'full':
                continue                                          # orphan key dropped
            if p is not None and p['supply_type'] != 'Networked':
                continue
        ev.append((cat, dt.datetime.fromisoformat(c['received'])))
    if reader in ('cracker', 'full'):
        linked = {c['contact_id'] for c in crm}
        for w in web:
            if w['crm_case'] and w['crm_case'] in linked:
                continue                                          # already in the CRM under its case number
            ev.append((WEBCAT[w['issue']], dt.datetime.fromisoformat(w['submitted'])))
    out = []
    for a, b in PERIODS:
        conn = sum(1 for r in reg if r['supply_type'] == 'Networked' and (not r['connected_date'] or day(r['connected_date']) <= b))
        if reader == 'mirror':
            conn = sum(1 for r in reg if r['water_connection'])
        for k in ('Clarity', 'Taste', 'Odour', 'Pressure or flow', 'Continuity of supply'):
            out.append(sum(1 for c, t in ev if c == k and a <= t.date() <= b) / conn * 1000.0)
    return out


# ------------------------------------------------------------------ ask 3 readers
def utc_local(s):
    t = dt.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    return t + dt.timedelta(hours=13 if t >= dt.datetime(2027, 9, 25, 14) else 12)


def ask3(reader):
    srs = csvrows('service_requests')
    jobs = {r['job_no']: r for r in xlrows('crew_job_times', 'Jobs')}
    ah = csvrows('afterhours_service_calls')
    groups = defaultdict(lambda: defaultdict(list))
    for s in srs:
        notice = dt.datetime.fromisoformat(s['received'])
        if reader == 'full' and s['closure_note'] == 'Imported from after-hours service':
            same = [a for a in ah if a['caller_address'] == s['address'] and
                    dt.timedelta(0) < notice - dt.datetime.fromisoformat(a['call_received'][:19]) <= dt.timedelta(hours=16)]
            if same:
                notice = dt.datetime.fromisoformat(same[0]['call_received'][:19])
        if not s['job_no'] or s['job_no'] not in jobs:
            continue                                              # no crew times on file
        j = jobs[s['job_no']]
        att = utc_local(j['on_site_utc']) if reader != 'mirror' else dt.datetime.strptime(j['on_site_utc'], '%Y-%m-%dT%H:%M:%SZ')
        res = utc_local(j['completed_utc']) if reader != 'mirror' else dt.datetime.strptime(j['completed_utc'], '%Y-%m-%dT%H:%M:%SZ')
        a_min, r_min = (att - notice).total_seconds() / 60, (res - notice).total_seconds() / 60
        if reader != 'mirror' and a_min < 0:
            continue                                              # impossible row dropped
        if notice.date() > dt.date(2027, 9, 30):
            continue
        m = notice.strftime('%B')
        if s['priority'] == 'Urgent':
            groups[m]['ua'].append(a_min)
            groups[m]['ur'].append(r_min)
        else:
            groups[m]['na'].append(a_min / 60)
            groups[m]['nr'].append(r_min / 60)
    out = []
    for m in ('July', 'August', 'September'):
        for k in ('ua', 'ur', 'na', 'nr'):
            out.append(statistics.median(groups[m][k]))
    return out


# ------------------------------------------------------------------ scoring
def golden_asks():
    FIG = json.load(open(os.path.join(HERE, 'figures.json')))
    L, C, O = FIG['asks']['lab'], FIG['asks']['complaints'], FIG['asks']['callouts']
    g1 = L['tested'] + L['parvum'] + L['hominis']
    g2 = [C[p][k] for p in ('July to September',)
          for k in ('Clarity', 'Taste', 'Odour', 'Pressure or flow', 'Continuity of supply')]
    g3 = [O[m][k] for m in ('July', 'August', 'September') for k in ('urgent_attend', 'urgent_resolve', 'nonurgent_attend', 'nonurgent_resolve')]
    return g1, g2, g3


def hits(resp, gold, units):
    return [abs(round(r / u) * u - round(g / u) * u) < u / 2 for r, g, u in zip(resp, gold, units)]


def score():
    g1, g2, g3 = golden_asks()
    u1 = [1] * len(g1)
    u2 = [0.01] * len(g2)
    u3 = [1, 1, 0.1, 0.1] * 3
    sheet = {}
    for reader in ('cracker', 'full', 'mirror'):
        a1 = ask1(reader)
        r1 = a1['tested'] + a1['parvum'] + a1['hominis']
        r2 = ask2(reader)
        r3 = ask3(reader)
        h = hits(r1, g1, u1) + hits(r2, g2, u2) + hits(r3, g3, u3)
        sheet[reader] = dict(ask1=sum(hits(r1, g1, u1)), ask2=sum(hits(r2, g2, u2)), ask3=sum(hits(r3, g3, u3)),
                             kept=sum(h), of=len(h))
    n = sheet['cracker']['of']
    lc = sheet['cracker']['kept'] / n
    lm = sheet['mirror']['kept'] / n
    lf = sheet['full']['kept'] / n
    on_call = 38 + 7 + 55 * lc
    off_call = 5 + 7 + 55 * lm
    sheet['pair_one_on_one_off'] = round((on_call + off_call) / 2, 1)
    sheet['pair_both_on'] = round((on_call + 38 + 7 + 55 * lf) / 2, 1)
    sheet['full_includer_keep_share'] = round(lf, 3)
    sheet['mirror_leakage_pct'] = round(100 * lm, 1)
    return sheet


if __name__ == '__main__':
    print(json.dumps(score(), indent=1))
