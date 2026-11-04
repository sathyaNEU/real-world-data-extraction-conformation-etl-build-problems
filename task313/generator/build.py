"""Build task313's pack (target/), metadata.json, the goldens, figures.json and target.zip.

    python3 task313/generator/build.py
"""
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import zipfile
import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import world as W
import records as R

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
GOLD = os.path.join(TASK, 'golden')
EXPORT = dt.datetime(2026, 11, 2, 7, 40)            # the planning pack's compile time
STAMP = (2026, 11, 2, 7, 40, 0)

F_A = 'rk_maternity_postnatal_discharges_2024-04_2026-10.csv'
F_B = 'sw_maternity_postnatal_discharges.xlsx'
F_N = 'community_midwifery_notifications_2024-04_2026-10.csv'
F_ADM = 'neonatal_paediatric_admissions_2024-04_2026-10.csv'
F_MPI = 'mpi_baby_hospital_numbers.csv'
F_TF = 'copperfield_trial_randomisation_final.xlsx'
F_C = 'copperfield_outreach_contacts.csv'
F_REP = 'Copperfield neonatal outreach trial final report.pdf'
F_SPEC = 'Neonatal outreach service specification 2027-28.pdf'
F_SITES = 'site_codes.csv'
F_REAS = 'newborn_risk_reasons.csv'
F_CT = 'outreach_contact_types.csv'
F_AM = 'admission_method_codes.csv'
F_DASH = 'lmns_maternity_dashboard_2025-26.xlsx'
F_EST = 'community_midwifery_establishment_2026-10.csv'
DISTRACTORS = [F_DASH, F_EST]


def write_csv(name, header, rows):
    with open(os.path.join(TGT, name), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(rows)


def normalise_zip(path, producer_app=None):
    """Re-pack an OOXML file with fixed member timestamps and the issuing organisation's properties."""
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            ni = zipfile.ZipInfo(info.filename, date_time=STAMP)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = 0o644 << 16
            if info.filename == 'docProps/app.xml':
                # the issuing system's own application name, not the writing library's
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>' + (producer_app or 'Microsoft Excel').encode()
                              + b'</Application>', data)
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
            if info.filename == 'docProps/core.xml':
                # the library stamps the save clock as modified; the file was last saved when it was created
                m = re.search(rb'<dcterms:created[^>]*>([^<]*)</dcterms:created>', data)
                data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', lambda x: x.group(1) + m.group(1) + x.group(2), data)
            z.writestr(ni, data)
    with open(path, 'wb') as f:
        f.write(buf.getvalue())


def book(creator, created):
    wb = openpyxl.Workbook()
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = created
    return wb


def sheet_rows(ws, header, rows, widths=None, fmt=None):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    ws.freeze_panes = 'A2'
    for i, h in enumerate(header, start=1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(10, min(34, len(str(h)) + 3)))
    if fmt:
        for col, nf in fmt.items():
            if col not in header:
                continue
            j = header.index(col) + 1
            for row in ws.iter_rows(min_row=2, min_col=j, max_col=j):
                for c in row:
                    c.number_format = nf


# ---------------------------------------------------------------- maternity systems

def maternity_a(B):
    rng = np.random.default_rng([W.SEED, 301])
    rows = []
    for b in B:
        if W.SYSTEM[b['unit']] != 'A':
            continue
        nhs = b['nhs'] if rng.random() > 0.004 else ''
        rows.append([R.SITE_A[b['unit']], b['hosp'], nhs, b['mother'], b['birth'].strftime('%d/%m/%Y %H:%M'),
                     '%d+%d' % (b['gest'], b['gest_d']), b['bw'], 'Y' if b['multiple'] else 'N', R.FEED_A[b['feed']],
                     b['disch'].strftime('%d/%m/%Y %H:%M'), 'Home', 'Y' if b['eligible'] else 'N', ';'.join(b['reasons_rec'])])
    write_csv(F_A, ['SITE', 'MRN', 'NHS_NUMBER', 'MOTHER_NHS_NUMBER', 'BABY_DOB_DTTM', 'GEST_AT_BIRTH', 'BIRTH_WEIGHT_G',
                    'MULTIPLE_BIRTH', 'FEEDING_AT_DISCHARGE', 'DISCHARGE_DTTM', 'DISCHARGE_DEST', 'NB_RISK_FLAG',
                    'NB_RISK_CODES'], rows)
    return len(rows)


def maternity_b(B):
    wb = book('Sedgefold and Wennby NHS Trust, Maternity Information', dt.datetime(2026, 11, 1, 18, 5))
    wb.remove(wb.active)
    years = [('2024-25', dt.datetime(2024, 4, 1), dt.datetime(2025, 4, 1)),
             ('2025-26', dt.datetime(2025, 4, 1), dt.datetime(2026, 4, 1)),
             ('2026-27 (Apr-Oct)', dt.datetime(2026, 4, 1), dt.datetime(2026, 11, 1))]
    twin_no = {}
    n = 0
    for name, a, z in years:
        ws = wb.create_sheet(name)
        new = name.startswith('2026')
        if not new:
            header = ['Hospital', 'Hospital No', 'NHS No', 'Mother NHS No', 'Date of birth', 'Time of birth',
                      'Gestation (weeks)', 'Gestation (days)', 'Birth weight (kg)', 'Multiple birth', 'Feeding on discharge',
                      'Discharge date', 'Discharge time', 'Discharged to', 'Feeding/jaundice risk', 'Risk reasons']
        else:
            header = ['Hospital', 'Hospital No', 'NHS No', 'Mother NHS No', 'Date of birth', 'Time of birth',
                      'Gestation', 'Birth weight (kg)', 'Multiple birth', 'Feeding on discharge', 'Discharged',
                      'Discharged to', 'Newborn risk flag', 'Newborn risk reasons']
        rows = []
        for b in B:
            if W.SYSTEM[b['unit']] != 'B' or not (a <= b['disch'] < z):
                continue
            mb = ''
            if b['multiple']:
                k = twin_no.get(b['mother'], 0) + 1
                twin_no[b['mother']] = k
                mb = 'Twin %d' % k
            reasons = '; '.join(R.REASON_LABEL[r] for r in b['reasons_rec'])
            if not new:
                rows.append([R.SITE_B[b['unit']], b['hosp'], R.fmt_nhs_spaced(b['nhs']), R.fmt_nhs_spaced(b['mother']),
                             b['birth'].date(), b['birth'].strftime('%H:%M'), b['gest'], b['gest_d'], round(b['bw'] / 1000.0, 3),
                             mb, R.FEED_B[b['feed']], b['disch'].date(), b['disch'].strftime('%H:%M'), 'Home',
                             'Yes' if b['eligible'] else 'No', reasons])
            else:
                rows.append([R.SITE_B[b['unit']], b['hosp'], R.fmt_nhs_spaced(b['nhs']), R.fmt_nhs_spaced(b['mother']),
                             b['birth'].date(), b['birth'].strftime('%H:%M'), '%d+%d' % (b['gest'], b['gest_d']),
                             round(b['bw'] / 1000.0, 3), mb, R.FEED_B[b['feed']], b['disch'], 'Home',
                             'Y' if b['eligible'] else 'N', reasons])
        sheet_rows(ws, header, rows, fmt={'Date of birth': 'DD/MM/YYYY', 'Discharge date': 'DD/MM/YYYY', 'Discharged': 'DD/MM/YYYY HH:MM'})
        n += len(rows)
    p = os.path.join(TGT, F_B)
    wb.save(p)
    normalise_zip(p)
    return n


# ---------------------------------------------------------------- community office, PAS, MPI

def notifications_file(B):
    rows = R.notifications(B)
    out = []
    for r in rows:
        out.append([W.to_utc(r['t']).strftime('%Y-%m-%dT%H:%M:%SZ'), R.OFFICE[r['site']], r['nhs'], r['hosp'], r['kind'], r['ref']])
    write_csv(F_N, ['received_utc', 'from_site', 'nhs_number', 'hospital_number', 'notification', 'office_ref'], out)
    return len(out)


ADM_SITE = {'RRI': 'Ravensby Royal Infirmary', 'KUH': 'Kellingworth University Hospital', 'SDH': 'Sedgefold Hospital',
            'SAH': "St Aldric's Hospital", 'WCH': 'Wennby Community Hospital', 'CFH': 'Copperfield Hospital'}


def admissions_file(B):
    rows, cross = R.admissions(B)
    out = []
    for r in rows:
        out.append(['RK' if W.SYSTEM[r['site']] == 'A' else 'SW', ADM_SITE[r['site']], r['ward'], r['nhs'], r['hosp'],
                    r['adm'].strftime('%Y-%m-%d %H:%M'), r['method'], r['dx'], r['disc'].strftime('%Y-%m-%d %H:%M') if r['disc'] else ''])
    write_csv(F_ADM, ['pas_trust', 'admitting_hospital', 'ward_type', 'nhs_number', 'hospital_number', 'admitted',
                      'admission_method', 'primary_diagnosis_icd10', 'discharge_datetime'], out)
    return len(out), rows, cross


def mpi_file(B, cross):
    rows = []
    for b in B:
        rows.append(['RK' if W.SYSTEM[b['unit']] == 'A' else 'SW', b['hosp'], b['nhs'], b['birth'].date().isoformat()])
    for (nhs, trust), num in cross.items():
        b_dob = None
        rows.append(['RK' if trust == 'A' else 'SW', num, nhs, ''])
    dob = {b['nhs']: b['birth'].date().isoformat() for b in B}
    rows = [[r[0], r[1], r[2], r[3] or dob.get(r[2], '')] for r in rows]
    rows.sort(key=lambda r: (r[0], r[1]))
    write_csv(F_MPI, ['trust', 'hospital_number', 'nhs_number', 'date_of_birth'], rows)
    return len(rows)


# ---------------------------------------------------------------- the trial

def trial_files(B):
    final, interim = R.trial_lists(B)
    wb = book('Copperfield Neonatal Outreach Trial (data manager)', dt.datetime(2026, 4, 30, 16, 12))
    ws = wb.active
    ws.title = 'Randomised'
    sheet_rows(ws, ['Study ID', 'Hospital No', 'NHS No', 'Date randomised', 'Arm', 'Primary risk reason', 'Status'],
               [[r['sid'], r['hosp'], r['nhs'], r['date'], r['arm'], r['reason'], r['status']] for r in final],
               fmt={'Date randomised': 'DD/MM/YYYY'})
    p = os.path.join(TGT, F_TF)
    wb.save(p)
    normalise_zip(p)
    rows = R.contacts(B)
    write_csv(F_C, ['contact_id', 'sync_id', 'nhs_number', 'contact_datetime', 'contact_type', 'staff_id', 'minutes'],
              [[r['cid'], r['sync'], r['nhs'], r['t'].strftime('%Y-%m-%d %H:%M'), r['kind'], r['nurse'], r['mins']] for r in rows])
    return len(final), len(rows)


# ---------------------------------------------------------------- lookups and distractors

def lookups():
    write_csv(F_SITES, ['site', 'trust', 'maternity_system_code', 'maternity_system_name', 'community_office_code', 'pas_hospital_name'],
              [['Ravensby Royal Infirmary', 'Ravensby and Kellingworth Hospitals NHS Foundation Trust', 'RVY', '', 'RVY01', 'Ravensby Royal Infirmary'],
               ['Kellingworth University Hospital', 'Ravensby and Kellingworth Hospitals NHS Foundation Trust', 'KLW', '', 'KLW02', 'Kellingworth University Hospital'],
               ['Sedgefold Hospital', 'Sedgefold and Wennby NHS Trust', '', 'Sedgefold', 'SDF03', 'Sedgefold Hospital'],
               ["St Aldric's Hospital", 'Sedgefold and Wennby NHS Trust', '', "St Aldric's", 'STA04', "St Aldric's Hospital"],
               ['Wennby Community Hospital', 'Sedgefold and Wennby NHS Trust', '', 'Wennby', 'WNB05', 'Wennby Community Hospital'],
               ['Copperfield Hospital', 'Sedgefold and Wennby NHS Trust', '', 'Copperfield', 'CPF06', 'Copperfield Hospital']])
    write_csv(F_REAS, ['code', 'label'], [[k, v] for k, v in R.REASON_LABEL.items()])
    write_csv(F_CT, ['code', 'description', 'in_use_from'], [['TEL', 'Telephone contact with the family', '2024-03-18'],
                                                              ['HV', 'Home visit', '2024-03-18'],
                                                              ['NA', 'Home visit attempted, no access', '2025-01-06'],
                                                              ['TNA', 'Telephone call, no answer', '2025-01-06']])
    write_csv(F_AM, ['code', 'description'], [['11', 'Elective, from waiting list'], ['12', 'Elective, booked'],
                                               ['13', 'Elective, planned'], ['21', 'Emergency, via emergency department'],
                                               ['22', 'Emergency, via general practitioner'], ['28', 'Emergency, other means'],
                                               ['81', 'Transfer from another hospital provider (not emergency)']])


def distractors(B):
    rng = np.random.default_rng([W.SEED, 501])
    wb = book('Ravensby and Weald LMNS (performance team)', dt.datetime(2026, 10, 14, 9, 30))
    ws = wb.active
    ws.title = 'Monthly'
    rows = []
    months = [dt.date(2025, m, 1) for m in range(4, 13)] + [dt.date(2026, m, 1) for m in range(1, 4)]
    for u in W.UNITS:
        for m in months:
            nb = sum(1 for b in B if b['unit'] == u and b['birth'].year == m.year and b['birth'].month == m.month)
            births = int(round(nb / 0.94 + rng.normal(0, 3)))
            bf = round(float(np.clip(rng.normal(0.47 + (0.04 if u in ('WCH', 'SDH') else 0), 0.03), 0.3, 0.7)) * 100, 1)
            smoke = round(float(np.clip(rng.normal(0.085 + (0.02 if u in ('RRI', 'SAH') else 0), 0.012), 0.03, 0.2)) * 100, 1)
            atain = round(float(np.clip(rng.normal(0.052 if u in ('RRI', 'KUH') else 0.044, 0.008), 0.02, 0.09)) * 100, 1)
            cs = round(float(np.clip(rng.normal(0.36 if u in ('RRI', 'KUH') else 0.32, 0.025), 0.2, 0.5)) * 100, 1)
            rows.append([ADM_SITE[u], m, births, bf, smoke, atain, cs])
    sheet_rows(ws, ['Unit', 'Month', 'Births', 'Breastfeeding at discharge (%)', 'Smoking at delivery (%)',
                    'Term admissions to neonatal unit (%)', 'Caesarean births (%)'], rows, fmt={'Month': 'MMM YYYY'})
    p = os.path.join(TGT, F_DASH)
    wb.save(p)
    normalise_zip(p)
    teams = [('Ravensby North', 'RVY01'), ('Ravensby South', 'RVY01'), ('Kellingworth', 'KLW02'), ('Sedgefold', 'SDF03'),
             ("St Aldric's", 'STA04'), ('Wennby and Moorside', 'WNB05'), ('Copperfield', 'CPF06')]
    rows = []
    for t, code in teams:
        funded = round(float(rng.uniform(9.0, 21.0)) * 2) / 2
        inpost = round(max(funded - float(rng.uniform(0.0, 3.5)), 4) * 10) / 10
        rows.append([t, code, '%.1f' % funded, '%.1f' % inpost, '%.1f' % round(funded - inpost, 1), '%.1f' % round(float(rng.uniform(0.4, 2.6)), 1)])
    write_csv(F_EST, ['team_name', 'office_code', 'midwife_wte_funded', 'midwife_wte_in_post', 'vacancy_wte', 'maternity_support_worker_wte'], rows)


SOURCES = {
    F_A: 'Constructed: Ravensby and Kellingworth Hospitals NHS Foundation Trust maternity system, postnatal discharges home extract',
    F_B: 'Constructed: Sedgefold and Wennby NHS Trust maternity information system, postnatal discharges by financial year',
    F_N: 'Constructed: Ravensby and Weald Community Health NHS Trust community midwifery office, notification receipt log',
    F_ADM: "Constructed: Ravensby and Weald Integrated Care Board admissions extract (both trusts' patient administration systems)",
    F_MPI: 'Constructed: master patient index, hospital numbers to NHS numbers for babies',
    F_TF: 'Constructed: Copperfield neonatal outreach trial, final randomisation list',
    F_C: 'Constructed: Ravensby and Weald Community Health NHS Trust, outreach tablet application contact log',
    F_REP: 'Constructed: Copperfield neonatal outreach trial final report, version 1.0',
    F_SPEC: 'Constructed: Ravensby and Weald Integrated Care Board service specification SS-MAT-027 version 1.2',
    F_SITES: 'Constructed: site code crosswalk across the maternity systems, the community office and the PAS',
    F_REAS: 'Constructed: newborn feeding or jaundice risk reason codes',
    F_CT: 'Constructed: outreach contact type codes',
    F_AM: 'Constructed: admission method codes as used in the admissions extract',
    F_DASH: 'Constructed: local maternity and neonatal system monthly dashboard 2025/26',
    F_EST: 'Constructed: community midwifery establishment by team, October 2026',
}
DATES = {F_REP: '2026-06-26', F_SPEC: '2026-10-20', F_DASH: '2026-10-14', F_EST: '2026-10-31', F_TF: '2026-04-30'}
ROWS = {}


def metadata(counts):
    files = []
    for n in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, n)
        ext = n.rsplit('.', 1)[1]
        files.append(dict(path=n, format=ext, bytes=os.path.getsize(p), rows=ROWS.get(n), source=SOURCES[n],
                          date=DATES.get(n, '2026-11-02'), license='CC0 (original work, constructed for this task)'))
    big = max((f for f in files if f['rows']), key=lambda f: f['rows'])
    origin = ("constructed for this task by task313/generator/build.py (seeded, deterministic) in the layouts of two NHS "
              "trusts' maternity discharge extracts, a community midwifery office's notification log, an integrated care "
              "board admissions extract and master patient index, a trial's randomisation list, contact log and final report, "
              "a commissioning service specification, code lists, a local maternity dashboard and a staffing establishment; "
              "the board, the trusts, the hospitals and the people are fictional.")
    meta = {
        'task': 'task313', 'architecture': 1,
        'title': ('How many of the 30 neonatal outreach nurse posts funded from April 2027 go to each maternity unit in the '
                  'Ravensby and Weald area, and how many readmissions of newborn babies the service avoids in 2027/28'),
        'domain': 'Healthcare Delivery & Health Economics', 'subdomain': 'patient-flow-beds-workforce-optimization',
        'client_task_type': 'patient-flow-beds-workforce-optimization', 'objective': 'Opportunity Sizing & Decision Support',
        'prompt_shape': '05 allocation to a fixed total', 'as_of': '2026-11-02',
        'deliverables': ['outreach_posts_2027-28.xlsx', 'outreach_posts_by_unit.svg'],
        'distractor_files': DISTRACTORS,
        'stated_inputs': ['30', 'April 2027', '2027/28', '28 days', '25'],
        'field_terms': [],
        'input_gates': {'files': len(files), 'formats': sorted({f['format'] for f in files}), 'largest_file': big['path'],
                        'largest_file_rows': big['rows']},
        'sources': [{'files': 'all files under target/', 'origin': origin, 'date': '2026-11-02', 'license': 'CC0 (original work)'}],
        'created': '2026-11-02', 'generator': 'task313/generator/build.py', 'files': files,
    }
    with open(os.path.join(TASK, 'metadata.json'), 'w') as f:
        json.dump(meta, f, indent=1)


def pdf_stamp(path, stamp):
    """The writer's fixed 2000-01-01 creation and modification dates replaced by the document's own date, byte for
    byte at equal length so the cross-reference offsets stand."""
    fixed = b"D:20000101000000+00'00'"
    assert len(stamp) == len(fixed)
    with open(path, 'rb') as f:
        data = f.read()
    assert data.count(fixed) == 2, path
    data = data.replace(fixed, stamp)
    # the writer's name in its two comment lines, blanked to spaces after the comment marker
    for sig in (b' ReportLab Generated PDF document (opensource)', b' ReportLab generated PDF document -- digest (opensource)'):
        assert data.count(sig) == 1, (path, sig)
        data = data.replace(sig, b' ' * len(sig))
    with open(path, 'wb') as f:
        f.write(data)


def zip_target():
    path = os.path.join(TASK, 'target.zip')
    names = sorted(os.listdir(TGT))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            info = zipfile.ZipInfo(n, date_time=STAMP)        # files at the archive root, no enclosing folder
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(TGT, n), 'rb') as f:
                z.writestr(info, f.read())
    return path


def set_mtimes():
    ts = EXPORT.timestamp()
    for n in os.listdir(TGT):
        os.utime(os.path.join(TGT, n), (ts, ts))


def main():
    import docs
    import golden
    B = W.build_world()
    R.apply_record_reasons(B)            # the discharge records as amended after discharge
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    counts = {}
    counts['maternity_a'] = maternity_a(B)
    counts['maternity_b'] = maternity_b(B)
    counts['notifications'] = notifications_file(B)
    counts['admissions'], adm_rows, cross = admissions_file(B)
    counts['mpi'] = mpi_file(B, cross)
    counts['trial_final'], counts['contacts'] = trial_files(B)
    lookups()
    distractors(B)
    stats = golden.trial_stats(B, golden.report_missed(B))      # the report as the trial team ran it
    docs.report(os.path.join(TGT, F_REP), stats)
    docs.spec(os.path.join(TGT, F_SPEC))
    pdf_stamp(os.path.join(TGT, F_REP), b"D:20260626093742+01'00'")
    pdf_stamp(os.path.join(TGT, F_SPEC), b"D:20261020141907+01'00'")
    set_mtimes()
    golden.main(B, counts)
    for n in os.listdir(TGT):
        p = os.path.join(TGT, n)
        if n.endswith('.csv'):
            with open(p, encoding='utf-8') as f:
                ROWS[n] = sum(1 for _ in f) - 1
        elif n.endswith('.xlsx'):
            wb = openpyxl.load_workbook(p, read_only=True)
            ROWS[n] = sum(ws.max_row - 1 for ws in wb.worksheets)
    metadata(counts)
    zip_target()
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
