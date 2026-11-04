"""task401 ask sheet as code on the cut pack: the cracker, the full includer in two variants, the no-repair reader and
the mirror, each scored figure by figure against figures.json (a hit is within half a unit of the stated rounding).
Reads the shipped files only and shares no code with the generator's golden.

  cracker    lands the call, runs the hygiene battery and executes the filed conventions: the 00:00 1 April reads at
             the consent's meter point, the consent's multiplier and allowance, results at the consented sampling point,
             settled COD; it dates each result by the laboratory record's own date and takes each analysed bottle as a
             composite.
  full       the full includer reads every file and acts on every stated fact: it walks each meter point's reads through
             the exchange reads, dates each composite by the round sheet's collection and takes the bottles of one round
             as one composite (the scheme's unit). Variant plain: it combines a composite's bottles by a plain mean.
             Variant weighted: it weights them by the volumes in the samplers' download log (the golden's route).
  norepair   every row as it stands: the 1 April reads at no multiplier, results by the consent's customer code, dated
             by report, each bottle a composite.
  mirror     the best response off the call; the ask does not turn on the call, so it handles it as the cracker does.

    python3 ceiling.py [target dir] [figures.json]       exit 1 if the pair ceiling is over 60
"""
import csv, hashlib, json, os, sys
from collections import defaultdict
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CY = (date(2025, 4, 1), date(2026, 3, 31))


def rows(T, fn):
    with open(os.path.join(T, fn), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def consents(T):
    from openpyxl import load_workbook
    v = list(load_workbook(os.path.join(T, 'trade_effluent_consents_register.xlsx'), read_only=True)['Consents']
             .iter_rows(values_only=True))
    return [dict(zip(v[0], r)) for r in v[1:]]


def route(T, multiplier=True, walk=False, dating='reported', key='point', merge='each'):
    reads = rows(T, 'te_meter_reads_2025-26.csv')
    sheets = rows(T, 'te_sampling_rounds_2025-01_2026-04.csv')
    by_ref = {r['bottle_ref']: r for r in sheets}
    vol = {(r['sampling_point'], r['run_end'], r['bottle']): float(r['volume_ml'])
           for r in rows(T, 'te_sampler_downloads_2025-01_2026-04.csv')}
    lab = defaultdict(dict)
    meta = {}
    for r in rows(T, 'lims_trade_effluent_results_2025-01_2026-04.csv'):
        lab[r['client_ref']][r['determinand']] = float(r['result'])
        meta[r['client_ref']] = (r['customer_code'], r['sample_point'], datetime.strptime(r['reported_on'], '%d/%m/%Y').date())
    out = {}
    for c in consents(T):
        rd = [r for r in reads if r['meter_point'] == c['meter_point']]
        a = [int(r['register_read']) for r in rd if r['read_date'] == '2025-03-31'][0]
        b = [int(r['register_read']) for r in rd if r['read_date'] == '2026-03-31'][0]
        adv = b - a
        if walk:
            fin = [int(r['register_read']) for r in rd if 'final read' in r['read_type']]
            ini = [int(r['register_read']) for r in rd if 'initial read' in r['read_type']]
            adv -= sum(i - f for f, i in zip(fin, ini))
        volume = adv * (int(c['register_multiplier']) if multiplier else 1) * (1 - float(c['non_returned_allowance_pct']) / 100)
        mine = [ref for ref, (code, pt, rep) in meta.items()
                if (pt == c['sampling_point'] if key == 'point' else code == c['customer_code'])]
        groups = defaultdict(list)
        for ref in mine:
            if merge == 'each':
                groups[ref].append(ref)
            else:
                sh = by_ref[ref]
                groups[(sh['sampling_point'], sh['collected_at'])].append(ref)
        cod, ss = [], []
        for g, refs in groups.items():
            if dating == 'reported':
                d = meta[refs[0]][2]
            else:
                d = datetime.strptime(by_ref[refs[0]]['collected_at'], '%d/%m/%Y %H:%M').date()
            if not (CY[0] <= d <= CY[1]):
                continue
            if merge == 'weighted':
                w = [vol[(by_ref[r]['sampling_point'], by_ref[r]['collected_at'], by_ref[r]['bottle'])] for r in refs]
            else:
                w = [1.0] * len(refs)
            cod.append(sum(wi * lab[r]['COD settled'] for wi, r in zip(w, refs)) / sum(w))
            ss.append(sum(wi * lab[r]['Suspended solids'] for wi, r in zip(w, refs)) / sum(w))
        out[c['discharger']] = dict(volume=volume, ot=sum(cod) / len(cod), st=sum(ss) / len(ss))
    return out


def kept(prof, F):
    n = 0
    for k, v in F['ask_a'].items():
        p = prof[k]
        n += sum(abs(round(p[f]) - v[f]) < 0.5 for f in ('volume', 'ot', 'st'))
    return n


def main():
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'target')
    F = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'figures.json')))
    N = 3 * len(F['ask_a'])
    cracker = route(T)
    profiles = dict(cracker=cracker,
                    full_plain=route(T, walk=True, dating='collected', merge='plain'),
                    full_weighted=route(T, walk=True, dating='collected', merge='weighted'),
                    norepair=route(T, multiplier=False, key='code'),
                    mirror=cracker)
    zp = os.path.join(os.path.dirname(HERE), 'target.zip')
    if os.path.exists(zp):
        print('pack digest %s' % hashlib.sha256(open(zp, 'rb').read()).hexdigest()[:12])
    share = {}
    for k, p in profiles.items():
        share[k] = kept(p, F) / float(N)
        print('%-14s keeps %2d of %d (%.1f%% of ask weight)%s' % (k, kept(p, F), N, 100 * share[k],
              ('; row: miss' if kept(p, F) <= N // 3 else '; row: KEEPS') if k == 'cracker' else ''))
    on = lambda L: 38 + 7 + 55 * L
    off = lambda L: 5 + 7 + 55 * L
    pc = (on(share['cracker']) + off(share['mirror'])) / 2
    print('pair ceiling, cracker on the call %.1f and the mirror off it %.1f: %.1f' % (on(share['cracker']), off(share['mirror']), pc))
    for v in ('full_plain', 'full_weighted'):
        both = (on(share['cracker']) + on(share[v])) / 2
        one_a = (on(share[v]) + off(share['cracker'])) / 2
        one_b = (on(share['cracker']) + off(share[v])) / 2
        print('%s: both on the call %.1f; it on and the cracker off %.1f; the cracker on and it off %.1f'
              % (v, both, one_a, one_b))
    print('mirror leakage: %.1f%% of ask weight' % (100 * share['mirror']))
    return 0 if (pc <= 60 and kept(profiles['full_weighted'], F) == N) else 1


if __name__ == '__main__':
    sys.exit(main())
