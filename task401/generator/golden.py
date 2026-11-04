"""task401 golden solution, computed from the shipped files in target/ alone."""
import csv, os
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

UK = ZoneInfo('Europe/London')
UTC = ZoneInfo('UTC')
WIN = (date(2025, 11, 1), date(2026, 3, 31))
PRIOR = (date(2024, 11, 1), date(2025, 3, 31))
CY = (date(2025, 4, 1), date(2026, 3, 31))
STANDARD = 0.6


def rows(T, fn):
    with open(os.path.join(T, fn), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def monitor_days(T, use_flagged=False):
    acc = defaultdict(list)
    for r in rows(T, 'allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv'):
        if r['qc_flag'] and not use_flagged:
            continue
        t = datetime.strptime(r['datetime_utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=UTC).astimezone(UK)
        acc[t.date()].append(float(r['ammonium_mg_l_as_n']))
    return {d: sum(v) / len(v) for d, v in acc.items() if len(v) >= 72}


def exceedances(days, lo, hi):
    return sorted(d for d, m in days.items() if lo <= d <= hi and m > STANDARD)


def dairy_events(T, ph_max=6.5, flow_min=6.0, hours=(20, 24)):
    ev = set()
    for r in rows(T, 'thornlea_dairy_discharge_monitor_15min.csv'):
        t = datetime.strptime(r['logger_time'], '%Y-%m-%d %H:%M')
        if hours[0] <= t.hour < hours[1] and float(r['ph']) < ph_max and float(r['flow_m3']) > flow_min:
            ev.add(t.date())
    return ev


def reach(exc, events, lags=(1, 2)):
    return [d for d in exc if any((d - timedelta(days=L)) in events for L in lags)]


def historian_fe(T):
    acc = defaultdict(list)
    for r in rows(T, 'coldmere_wrc_historian_hourly_2024-10_2026-03.csv'):
        v = r['FE_NH4'] or r['FE_NH4N_AIT301']
        acc[datetime.strptime(r['timestamp'], '%d/%m/%Y %H:%M').date()].append(float(v))
    return {d: sum(v) / len(v) for d, v in acc.items()}


# ---------------------------------------------------------------- Ask A
RATES = dict(R=0.4421, V=0.5248, Bv=0.0986, B=0.6133, S=0.4387, Os=470.0, Ss=330.0)


def consents(T):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(T, 'trade_effluent_consents_register.xlsx'), read_only=True)
    v = list(wb['Consents'].iter_rows(values_only=True))
    return [dict(zip(v[0], r)) for r in v[1:]]


def chargeable_volume(T, c, exchanges=True):
    """The advance of each meter at the meter point while it was in service, between the 00:00 reads on 1 April."""
    rd = [r for r in rows(T, 'te_meter_reads_2025-26.csv') if r['meter_point'] == c['meter_point']]
    start = [int(r['register_read']) for r in rd if r['read_date'] == '2025-03-31' and r['read_type'] == 'AMR 00:00'][0]
    end = [int(r['register_read']) for r in rd if r['read_date'] == '2026-03-31' and r['read_type'] == 'AMR 00:00'][0]
    adv = end - start
    if exchanges:
        for f, i in zip([r for r in rd if r['read_type'].startswith('Exchange: final')],
                        [r for r in rd if r['read_type'].startswith('Exchange: initial')]):
            adv -= int(i['register_read']) - int(f['register_read'])
    return adv * int(c['register_multiplier']) * (1 - float(c['non_returned_allowance_pct']) / 100)


def composites(T, point, dating='collected', merge='volume'):
    """Each composite sample at a sampling point: the bottles one round collected there, weighted by the volume the
    sampler's download log records for each bottle. dating='reported' dates each result by the laboratory's report;
    merge='plain' takes the plain mean of a composite's bottles, merge='each' counts every bottle as a composite."""
    sheets = [r for r in rows(T, 'te_sampling_rounds_2025-01_2026-04.csv') if r['sampling_point'] == point]
    vols = {(r['sampling_point'], r['run_end'], int(r['bottle'])): float(r['volume_ml'])
            for r in rows(T, 'te_sampler_downloads_2025-01_2026-04.csv')}
    res = defaultdict(dict)
    rep = {}
    for r in rows(T, 'lims_trade_effluent_results_2025-01_2026-04.csv'):
        res[r['client_ref']][r['determinand']] = float(r['result'])
        rep[r['client_ref']] = datetime.strptime(r['reported_on'], '%d/%m/%Y').date()
    visits = defaultdict(list)
    for r in sheets:
        visits[r['collected_at']].append((int(r['bottle']), r['bottle_ref']))
    out = []
    for when, pairs in visits.items():
        pairs.sort()
        refs = [ref for _, ref in pairs]
        if any(ref not in res for ref in refs):
            continue                                  # collected after the extract's last report
        if merge == 'drop2':
            refs = refs[:1]
        if merge == 'each':
            for ref in refs:
                d = rep[ref] if dating == 'reported' else datetime.strptime(when, '%d/%m/%Y %H:%M').date()
                out.append((d, res[ref]['COD settled'], res[ref]['Suspended solids']))
            continue
        if merge == 'volume':
            w = [vols[(point, when, b)] for b, _ in pairs]
        else:
            w = [1.0] * len(refs)
        cod = sum(wi * res[ref]['COD settled'] for wi, ref in zip(w, refs)) / sum(w)
        ss = sum(wi * res[ref]['Suspended solids'] for wi, ref in zip(w, refs)) / sum(w)
        d = rep[refs[0]] if dating == 'reported' else datetime.strptime(when, '%d/%m/%Y %H:%M').date()
        out.append((d, cod, ss))
    return out


def strengths(T, c, dating='collected', merge='volume'):
    comp = [x for x in composites(T, c['sampling_point'], dating, merge) if CY[0] <= x[0] <= CY[1]]
    return sum(x[1] for x in comp) / len(comp), sum(x[2] for x in comp) / len(comp), len(comp)


def ask_a(T):
    out = {}
    for c in consents(T):
        vol = chargeable_volume(T, c)
        ot, st, n = strengths(T, c)
        out[c['discharger']] = dict(volume=vol, ot=ot, st=st, n=n)
    return out


def solve(T):
    days = monitor_days(T)
    exc_w = exceedances(days, *WIN)
    exc_p = exceedances(days, *PRIOR)
    ev = dairy_events(T)
    reached = reach(exc_w, ev)
    fe = historian_fe(T)
    F = dict(exc_window=len(exc_w), exc_prior=len(exc_p), dairy_reach=len(reached), other=len(exc_w) - len(reached),
             exc_days=[d.isoformat() for d in exc_w], exc_days_prior=[d.isoformat() for d in exc_p], events_window=len([e for e in ev if WIN[0] - timedelta(days=2) <= e <= WIN[1]]),
             fe_on_exc=sum(fe[d] for d in exc_w) / max(1, len(exc_w)),
             ask_a=ask_a(T))
    return F
