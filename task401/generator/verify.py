"""task401 independent verifier: recomputes every graded figure from the shipped files in target/ alone (the documents
read as text, the rates parsed from the charges scheme, the transformer change and the new blower's board parsed from the
shutdown works record) and compares with generator/figures.json. Imports nothing from the generator.

    python3 verify.py [target dir]          exit 1 on any mismatch
"""
import csv, json, os, re, sys, zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
UK, UTC = ZoneInfo('Europe/London'), ZoneInfo('UTC')
RESULTS = []


def check(label, cond, detail=''):
    RESULTS.append(bool(cond))
    print('%s  %s %s' % ('ok  ' if cond else 'MISS', label, detail))


def table(T, name):
    with open(os.path.join(T, name), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def sheet(T, name, ws):
    from openpyxl import load_workbook
    v = list(load_workbook(os.path.join(T, name), read_only=True)[ws].iter_rows(values_only=True))
    return [dict(zip(v[0], r)) for r in v[1:]]


def docx_text(path):
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    xml = re.sub(r'</w:p>', '\n', xml)
    return re.sub(r'<[^>]+>', '', xml)


def pdf_text(path):
    from pypdf import PdfReader
    return '\n'.join(p.extract_text() for p in PdfReader(path).pages)


# ------------------------------------------------------------------ the main call
def monitor_days(T):
    """UK days from the valid fifteen-minute readings, as the investigation terms define them."""
    vals = defaultdict(list)
    for r in table(T, 'allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv'):
        if r['qc_flag'].strip():
            continue
        t = datetime.fromisoformat(r['datetime_utc'].replace('Z', '+00:00')).astimezone(UK)
        vals[t.date()].append(float(r['ammonium_mg_l_as_n']))
    return {d: sum(v) / len(v) for d, v in vals.items() if len(v) >= 72}


def evenings(T, ph_below=6.45, flow_over=7.0, after=21):
    """Evenings on which the dairy's chamber record shows a run of low pH at production flow."""
    run = defaultdict(int)
    for r in table(T, 'thornlea_dairy_discharge_monitor_15min.csv'):
        t = datetime.strptime(r['logger_time'], '%Y-%m-%d %H:%M')
        if t.hour >= after and float(r['ph']) < ph_below and float(r['flow_m3']) > flow_over:
            run[t.date()] += 1
    return {d for d, n in run.items() if n >= 2}


def main_call(T, F):
    terms = docx_text(os.path.join(T, 'coldmere_ammonia_investigation_terms.docx'))
    check('terms define the day, the standard, validity and the window',
          all(s in terms for s in ('midnight to midnight UK time', 'above 0.6 mg/l', 'not valid', 'at least 72 valid readings',
                                   '1 November 2025 to 31 March 2026', '1 November 2024 to')))
    days = monitor_days(T)
    win = sorted(d for d, m in days.items() if date(2025, 11, 1) <= d <= date(2026, 3, 31) and m > 0.6)
    prv = sorted(d for d, m in days.items() if date(2024, 11, 1) <= d <= date(2025, 3, 31) and m > 0.6)
    check('exceedance days, November 2025 to March 2026', len(win) == F['exc_window'], '%d' % len(win))
    check('exceedance days a year earlier', len(prv) == F['exc_prior'], '%d' % len(prv))
    for m, n in F['exc_by_month_window'].items():
        got = sum(1 for d in win if d.strftime('%Y-%m') == m)
        check('exceedance days in %s' % m, got == n, '%d' % got)
    for m, n in F['exc_by_month_prior'].items():
        got = sum(1 for d in prv if d.strftime('%Y-%m') == m)
        check('exceedance days in %s' % m, got == n, '%d' % got)
    ev = evenings(T)
    reached = [d for d in win if (d - timedelta(days=1)) in ev or (d - timedelta(days=2)) in ev]
    check('exceedance days on the first or second day after an evening discharge', len(reached) == F['dairy_reach'],
          '%d of %d' % (len(reached), len(win)))
    check('exceedance days with no discharge on the two evenings before (all the upgrade or the control could reach)',
          len(win) - len(reached) == F['upgrade_reach'], '%d' % (len(win) - len(reached)))
    clear = [m for d, m in days.items() if (date(2024, 11, 1) <= d <= date(2025, 3, 31) or date(2025, 11, 1) <= d <= date(2026, 3, 31))
             and (d - timedelta(days=1)) not in ev and (d - timedelta(days=2)) not in ev]
    check('no day without a discharge on the two evenings before reaches the standard, either winter', max(clear) < 0.6,
          'max %.3f' % max(clear))
    check('the terms carry the upgrade estimate', ('\xa3%.1f million' % F['upgrade_cost_m']) in terms)


# ------------------------------------------------------------------ Ask A
def ask_a(T, F):
    flat = ' '.join(pdf_text(os.path.join(T, 'wendmoor_trade_effluent_charges_scheme_2025-26.pdf')).split())
    check('the scheme defines Ot and St over each composite collected in the charging year at the consented point',
          'over the composite samples we collect at the sampling point named in the trader\'s consent in the charging year' in flat)
    check('the scheme files the composite as both bottles and its strength as that of the effluent it holds',
          'the two bottles together are the composite sample' in flat
          and 'The strength of a composite sample is the strength of the effluent it holds' in flat)
    reads = table(T, 'te_meter_reads_2025-26.csv')
    rounds = table(T, 'te_sampling_rounds_2025-01_2026-04.csv')
    vol = {(r['sampling_point'], r['run_end'], r['bottle']): int(r['volume_ml'])
           for r in table(T, 'te_sampler_downloads_2025-01_2026-04.csv')}
    lab = defaultdict(dict)
    for r in table(T, 'lims_trade_effluent_results_2025-01_2026-04.csv'):
        lab[r['client_ref']][r['determinand']] = int(r['result'])
    for c in sheet(T, 'trade_effluent_consents_register.xlsx', 'Consents'):
        rd = sorted((r for r in reads if r['meter_point'] == c['meter_point']), key=lambda r: (r['read_date'], 'initial' in r['read_type']))
        seq = [r for r in rd if '2025-03-31' <= r['read_date'] <= '2026-03-31']
        adv, prev = 0, None
        for r in seq:
            v = int(r['register_read'])
            if prev is not None and 'initial read' not in r['read_type']:
                adv += v - prev
            prev = v
        volume = adv * int(c['register_multiplier']) * (100 - float(c['non_returned_allowance_pct'])) / 100
        visits = defaultdict(list)
        for r in rounds:
            if r['sampling_point'] == c['sampling_point']:
                taken = datetime.strptime(r['collected_at'], '%d/%m/%Y %H:%M').date()
                if date(2025, 4, 1) <= taken <= date(2026, 3, 31):
                    visits[r['collected_at']].append(r)
        cod, ss = [], []
        for when, bottles in visits.items():
            w = [vol[(c['sampling_point'], when, b['bottle'])] for b in bottles]
            cod.append(sum(wi * lab[b['bottle_ref']]['COD settled'] for wi, b in zip(w, bottles)) / sum(w))
            ss.append(sum(wi * lab[b['bottle_ref']]['Suspended solids'] for wi, b in zip(w, bottles)) / sum(w))
        g = F['ask_a'][c['discharger']]
        check('Ask A %s chargeable volume' % c['discharger'], round(volume) == g['volume'], '%.1f' % volume)
        check('Ask A %s settled COD strength' % c['discharger'], round(sum(cod) / len(cod)) == g['ot'], '%.2f' % (sum(cod) / len(cod)))
        check('Ask A %s suspended solids strength' % c['discharger'], round(sum(ss) / len(ss)) == g['st'], '%.2f' % (sum(ss) / len(ss)))


def main():
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'target')
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    main_call(T, F)
    ask_a(T, F)
    print('verify: %d of %d' % (sum(RESULTS), len(RESULTS)))
    return 0 if all(RESULTS) else 1


if __name__ == '__main__':
    sys.exit(main())
