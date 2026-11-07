"""Independent verifier: recomputes every graded figure from target/ alone.  python3 verify.py [target_dir]"""
import csv
import datetime as dt
import json
import os
import re
import statistics
import sys
from collections import defaultdict, deque

import pyarrow.parquet as pq
from openpyxl import load_workbook
from pypdf import PdfReader

TGT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'target')


def path(stem):
    hits = [os.path.join(dp, f) for dp, _, fs in os.walk(TGT) for f in fs if f.startswith(stem)]
    assert len(hits) == 1, (stem, hits)
    return hits[0]


def rows_csv(stem):
    with open(path(stem), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def rows_xlsx(stem, sheet):
    ws = load_workbook(path(stem), read_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def pdf_text(stem):
    return ' '.join((p.extract_text() or '') for p in PdfReader(path(stem)).pages)


def D(s):
    return dt.date.fromisoformat(str(s)[:10])


def local_wall(s):
    return dt.datetime.fromisoformat(s[:19])


# ------------------------------------------------------------------ the call
def day_states(valves, ops, first, last):
    """Per day, the valves closed (isolation) or open (boundary) for most of the day, local wall clock."""
    pos = {t: v['normal_position'] for t, v in valves.items()}
    by_tag = defaultdict(list)
    for o in ops:
        by_tag[o['field_tag']].append((local_wall(o['operation_time']), o['operation']))
    out = {}
    days = [first + dt.timedelta(days=i) for i in range((last - first).days + 1)]
    timeline = {}
    for tag, seq in by_tag.items():
        seq.sort()
        cur = valves[tag]['normal_position']
        tl = [(dt.datetime.combine(first, dt.time(0)), cur)]
        for t, op in seq:
            if op == 'Close':
                cur = 'Closed'
            elif op == 'Open':
                cur = 'Open'
            tl.append((t, cur))
        timeline[tag] = tl
    for dday in days:
        a = dt.datetime.combine(dday, dt.time(0))
        b = a + dt.timedelta(days=1)
        state = {}
        for tag, tl in timeline.items():
            closed = 0.0
            for i, (t, p) in enumerate(tl):
                t2 = tl[i + 1][0] if i + 1 < len(tl) else b
                lo, hi = max(t, a), min(t2, b)
                if hi > lo and p == 'Closed':
                    closed += (hi - lo).total_seconds()
            state[tag] = 'Closed' if closed > 43200 else 'Open'
        out[dday] = state
    return out, pos


def supply_paths(mains, valves, state):
    """Each zone's supply on a day: the reservoir and the mains its water passed through."""
    adj = defaultdict(list)
    on_main = defaultdict(list)
    for tag, v in valves.items():
        on_main[v['main_id']].append(v)
    for m in mains.values():
        if m['class'] == 'Trunk':
            shut = any(state.get(v['field_tag'], v['normal_position']) == 'Closed' for v in on_main[m['main_id']]
                       if v['valve_type'] == 'Isolation')
            if not shut:
                adj[m['from_node']].append((m['to_node'], m['main_id']))
                adj[m['to_node']].append((m['from_node'], m['main_id']))
        elif m['class'] == 'Boundary':
            bv = [v for v in on_main[m['main_id']] if v['valve_type'] == 'Boundary']
            if bv and state.get(bv[0]['field_tag'], bv[0]['normal_position']) == 'Open':
                adj[m['from_node']].append((m['to_node'], m['main_id']))
                adj[m['to_node']].append((m['from_node'], m['main_id']))
    out = {}
    zones = sorted({m['to_node'][:-6] for m in mains.values() if m['class'] == 'Trunk'})
    for z in zones:
        start = z + '-INLET'
        prev = {start: None}
        q = deque([start])
        found = []
        while q:
            n = q.popleft()
            if n.startswith('RES-'):
                found.append(n)
                continue
            for nb, mid in adj[n]:
                if nb not in prev:
                    prev[nb] = (n, mid)
                    q.append(nb)
        assert len(found) <= 1, (z, found)
        if not found:
            out[z] = None
            continue
        assets = [found[0]]
        n = found[0]
        while prev[n] is not None:
            n, mid = prev[n]
            assets.append(mid)
        out[z] = tuple(assets)
    return out


def main_call():
    mains = {r['main_id']: r for r in rows_xlsx('network_model_export', 'Mains')}
    valves = {r['field_tag']: r for r in rows_xlsx('network_model_export', 'Valves')}
    ops = rows_csv('valve_operations')
    census = rows_csv('meshblock_usually_resident')
    zres = defaultdict(int)
    mb_zone = {}
    for r in census:
        zres[r['supply_zone']] += int(r['usually_resident_population_2023'])
        mb_zone[r['meshblock_2023']] = r['supply_zone']
    tor = pdf_text('outbreak_control_team_terms')
    for phrase in ('1 to 12 days before their onset', 'fewer than five cases', '20 August to 17 October 2027',
                   'per 100,000 resident-days', 'onset from 1 September to 18 October 2027'):
        assert phrase in ' '.join(tor.split()), phrase
    first, last = dt.date(2027, 7, 1), dt.date(2027, 10, 18)
    states, _ = day_states(valves, ops, first, last)
    paths = {d: supply_paths(mains, valves, s) for d, s in states.items()}
    assets = sorted({p[0] for d in paths for p in paths[d].values() if p} |
                    {m['main_id'] for m in mains.values() if m['class'] == 'Boundary'})
    assets = [a for a in assets if a.startswith('RES-') or mains.get(a, {}).get('class') == 'Boundary']
    rd = defaultdict(int)
    for dday in [dt.date(2027, 8, 20) + dt.timedelta(days=i) for i in range(59)]:
        for z, p in paths[dday].items():
            for a in (p or ()):
                if a in assets:
                    rd[a] += zres[z]
    cases = defaultdict(int)
    lines = rows_xlsx('case_line_list', 'Line list')
    for c in lines:
        if c['Case status'] != 'Confirmed' or not c['Meshblock 2023']:
            continue
        onset = D(c['Onset date'])
        if not (dt.date(2027, 9, 1) <= onset <= dt.date(2027, 10, 18)):
            continue
        z = mb_zone[str(c['Meshblock 2023'])]
        hit = set()
        for k in range(1, 13):
            p = paths.get(onset - dt.timedelta(days=k), {}).get(z)
            hit.update(a for a in (p or ()) if a in assets)
        for a in hit:
            cases[a] += 1
    rate = {a: cases[a] / rd[a] * 1e5 for a in assets if rd[a]}
    ranked = sorted([a for a in rate if cases[a] >= 5], key=lambda a: -rate[a])
    call, runner = ranked[0], ranked[1]
    # the renewal's planned operations, read from the plan
    plan = ' '.join(pdf_text('kowhai_hills_feed_main_renewal').split())
    pops = re.findall(r'(\d{2} [A-Z][a-z]{2} 2027 \d{2}:\d{2}) (KV\d{4}) (Close|Open)', plan)
    assert len(pops) >= 6, pops
    st = {}
    t0 = dt.datetime.strptime('29 Oct 2027 12:00', '%d %b %Y %H:%M')
    for ts, tag, op in sorted(pops, key=lambda x: dt.datetime.strptime(x[0], '%d %b %Y %H:%M')):
        if dt.datetime.strptime(ts, '%d %b %Y %H:%M') <= t0:
            st[tag] = 'Closed' if op == 'Close' else 'Open'
    rp = supply_paths(mains, valves, st)
    fwd = sum(zres[z] for z, p in rp.items() if p and call in p)
    res_rates = {a: (cases[a], rate.get(a, 0.0)) for a in assets if a.startswith('RES-')}
    return dict(call=call, call_rate=rate[call], runner=runner, runner_rate=rate[runner], forward=fwd,
                reservoirs=res_rates, cases=dict(cases), rd=dict(rd))


# ------------------------------------------------------------------ ask 1
def lab():
    rows = rows_csv('community_lab_faecal')
    ref = rows_xlsx('reference_lab_cryptosporidium', 'Typing results')
    tor = ' '.join(pdf_text('outbreak_control_team_terms').split())
    assert 'counted once in a month however many specimens' in tor
    months = [(dt.date(2027, 7, 1), dt.date(2027, 7, 31)), (dt.date(2027, 8, 1), dt.date(2027, 8, 31)),
              (dt.date(2027, 9, 1), dt.date(2027, 9, 30)), (dt.date(2027, 10, 1), dt.date(2027, 10, 17))]
    person = lambda r: (r['surname'].strip().upper(), r['given_name'].strip(), r['dob'])
    tested = []
    for a, b in months:
        tested.append(len({person(r) for r in rows if r['town'] == 'Kotare' and a <= D(r['collected']) <= b}))
    by_acc = {r['accession']: r for r in rows}
    by_person = defaultdict(list)
    for r in rows:
        by_person[person(r)].append(r)
    periods = [(dt.date(2027, 7, 1), dt.date(2027, 10, 17))]
    par = [0]
    hom = [0]
    for x in ref:
        m = re.search(r'(\d{8})', str(x['Referrer reference']))
        src = by_acc.get('C' + m.group(1)) if m else None
        if src is None:
            sur, given = [s.strip() for s in str(x['Patient']).split(',', 1)]
            cand = [r for r in by_person.get((sur.upper(), given, str(x['DOB'])[:10]), []) if 'DETECTED' in r['result'] and 'Cryptosporidium antigen DETECTED' in r['result']]
            src = cand[0] if cand else None
        assert src is not None, x
        if src['town'] != 'Kotare':
            continue
        cd = D(src['collected'])
        for i, (a, b) in enumerate(periods):
            if a <= cd <= b:
                if x['Result'] == 'Cryptosporidium parvum':
                    par[i] += 1
                elif x['Result'] == 'Cryptosporidium hominis':
                    hom[i] += 1
    return dict(tested=tested, parvum=par, hominis=hom)


# ------------------------------------------------------------------ ask 2
ABBR = [(' rd', ' road'), (' st', ' street'), (' ave', ' avenue'), (' cres', ' crescent')]


def norm_addr(a):
    a = str(a).lower().split(',')[0].strip()
    a = re.sub(r'^flat \d+/', '', a)
    for k, v in ABBR:
        if a.endswith(k):
            a = a[: -len(k)] + v
    return re.sub(r'\s+', ' ', a)


def complaints():
    reg = pq.read_table(path('rating_connections')).to_pylist()
    by_val = {r['valuation_ref']: r for r in reg}
    by_addr = defaultdict(list)
    for r in reg:
        by_addr[norm_addr(r['property_address'])].append(r)
    meas = ' '.join(pdf_text('water_services_performance').split())
    assert 'counted in the period in which the customer made it' in meas
    crm = rows_csv('crm_water_contacts')
    web = rows_csv('website_water_quality')
    cats = {'Water - Clarity': 'Clarity', 'Water - Taste': 'Taste', 'Water - Odour': 'Odour',
            'Water - Pressure or flow': 'Pressure or flow', 'Water - Continuity of supply': 'Continuity of supply'}
    webcat = {'Discoloured water': 'Clarity', 'Taste': 'Taste', 'Smell': 'Odour'}

    def prop(c):
        if c['valuation_ref']:
            return by_val[c['valuation_ref']]
        hits = by_addr.get(norm_addr(c['address_as_given']), [])
        net = [h for h in hits if h['supply_type'] == 'Networked']
        if hits and not net:
            return hits[0]
        assert len(net) == 1, (c['address_as_given'], len(hits))
        return net[0]

    events = []
    rekeyed = set()
    for w in web:
        if w['crm_case']:
            continue
        cat = webcat[w['issue']]
        t = dt.datetime.fromisoformat(w['submitted'])
        twin = [c for c in crm if cats.get(c['category']) == cat and c['description'] == w['details']
                and norm_addr(c['address_as_given']) == norm_addr(w['address'])
                and dt.timedelta(0) < dt.datetime.fromisoformat(c['received']) - t <= dt.timedelta(days=10)]
        assert len(twin) <= 1
        if twin:
            rekeyed.add(twin[0]['contact_id'])
        events.append((cat, t))
    for c in crm:
        cat = cats.get(c['category'])
        if not cat or c['contact_id'] in rekeyed:
            continue
        p = prop(c)
        if p['supply_type'] != 'Networked':
            continue
        events.append((cat, dt.datetime.fromisoformat(c['received'])))
    out = {}
    for a, b, label in ((dt.date(2027, 7, 1), dt.date(2027, 9, 30), 'July to September'),):
        conn = sum(1 for r in reg if r['supply_type'] == 'Networked' and (not r['connected_date'] or D(r['connected_date']) <= b))
        out[label] = {k: sum(1 for c, t in events if c == k and a <= t.date() <= b) / conn * 1000.0
                      for k in ('Clarity', 'Taste', 'Odour', 'Pressure or flow', 'Continuity of supply')}
    return out


# ------------------------------------------------------------------ ask 3
def utc_to_local(s):
    t = dt.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    return t + dt.timedelta(hours=13 if t >= dt.datetime(2027, 9, 25, 14, 0) else 12)


def callouts():
    srs = rows_csv('service_requests')
    jobs = {r['job_no']: r for r in rows_xlsx('crew_job_times', 'Jobs')}
    ah = rows_csv('afterhours_service_calls')
    wos = [w for w in rows_csv('work_orders') if w['type'] == 'Planned maintenance']
    meas = ' '.join(pdf_text('water_services_performance').split())
    assert 'reaches the council or its after-hours service' in meas
    out = defaultdict(lambda: defaultdict(list))
    for s in srs:
        recv = dt.datetime.fromisoformat(s['received'])
        notice = recv
        if s['closure_note'] == 'Imported from after-hours service':
            cand = [a for a in ah if norm_addr(a['caller_address']) == norm_addr(s['address'])
                    and dt.timedelta(0) < recv - local_wall(a['call_received']) <= dt.timedelta(hours=16)]
            assert len(cand) == 1, (s['request_id'], len(cand))
            notice = local_wall(cand[0]['call_received'])
        if s['job_no']:
            j = jobs[s['job_no']]
            att, res = utc_to_local(j['on_site_utc']), utc_to_local(j['completed_utc'])
        else:
            street = s['address'].split(',')[0].split(' ', 1)[1]
            nxt = sorted([w for w in wos if w['street'] == street and
                          dt.datetime.strptime(w['started'], '%d/%m/%Y %H:%M') > recv],
                         key=lambda w: dt.datetime.strptime(w['started'], '%d/%m/%Y %H:%M'))
            assert nxt, s['request_id']
            att = dt.datetime.strptime(nxt[0]['started'], '%d/%m/%Y %H:%M')
            res = dt.datetime.strptime(nxt[0]['completed'], '%d/%m/%Y %H:%M')
        if notice.date() > dt.date(2027, 9, 30):
            continue
        m = notice.strftime('%B')
        a_min, r_min = (att - notice).total_seconds() / 60, (res - notice).total_seconds() / 60
        if s['priority'] == 'Urgent':
            out[m]['ua'].append(a_min)
            out[m]['ur'].append(r_min)
        else:
            out[m]['na'].append(a_min / 60)
            out[m]['nr'].append(r_min / 60)
    return {m: {k: statistics.median(v) for k, v in d.items()} for m, d in out.items()}


def run():
    return dict(main=main_call(), lab=lab(), complaints=complaints(), callouts=callouts())


if __name__ == '__main__':
    r = run()
    print(json.dumps(r, indent=1, default=str)[:3000])
