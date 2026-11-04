"""Build task314's pack (target/), metadata.json, the goldens, figures.json and target.zip.

    python3 task314/generator/build.py
"""
import csv
import datetime as dt
import io
import json
import math
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
EXPORT = dt.datetime(2026, 11, 3, 8, 17)             # the pack's compile time
STAMP = (2026, 11, 3, 8, 17, 0)
ASOF = '2026-11-03'

F_BILLS = 'cis_water_bills_2022-06_to_2026-10.csv'
F_ACCTS = 'cis_water_accounts_2026-11-02.csv'
F_R2144 = 'RES 2021-44.pdf'
F_R2312 = 'RES 2023-12.pdf'
F_R2417 = 'RES 2024-17.pdf'
F_DCP = 'Drought Contingency Plan Rev 2 (2025).pdf'
F_UBB = 'UBBWCD Notice 2026-07 Dry-Year Allocation 2027.pdf'
F_STAFF = 'Agenda Report Stage 2 Drought Rate Options DRAFT 2026-10-27.docx'
F_FILL = 'fill_station_transactions_2026-01-01_2026-10-31.csv'
F_FILLM = 'corvane_bws_monthly_activity_2026.xlsx'
F_READS = 'city_facility_meter_reads_2025-09_2026-10.csv'
F_FACS = 'city_facility_meters_2026-10-30.csv'
F_WO = 'meter_shop_completed_work_orders_2025-2026.xlsx'
F_WX = 'bvw03_daily_weather_2022-04-01_2026-10-31.csv'
F_STATE = 'state_pws_water_use_2025.xlsx'
F_REB = 'conservation_rebates_2022-2026.csv'
DISTRACTORS = [F_WX, F_STATE, F_REB]
ROWS = {}


def write_csv(name, header, rows):
    with open(os.path.join(TGT, name), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(rows)


def normalise_zip(path, producer_app=None, keep_modified=False, total_time=None):
    """Re-pack an OOXML file with fixed member timestamps and the issuing organisation's application properties."""
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    stats = None
    body = dict(items_ for items_ in ((i.filename, d) for i, d in items)).get('word/document.xml')
    if body is not None:
        paras = re.findall(rb'<w:p[ >].*?</w:p>', body, re.S)
        texts = [re.sub(rb'<[^>]+>', b'', p_).decode('utf-8') for p_ in paras]
        words = sum(len(t.split()) for t in texts)
        chars = sum(len(t.replace(' ', '')) for t in texts)
        chars_sp = sum(len(t) for t in texts)
        npara = sum(1 for t in texts if t.strip())
        stats = dict(Pages=max(1, words // 430 + 1), Words=words, Characters=chars, CharactersWithSpaces=chars_sp,
                     Paragraphs=npara, Lines=npara + words // 14, TotalTime=total_time or 37 + (words % 23))
        # the template's thumbnail is a blank page, and Word saves none unless asked to
        items = [(i, d) for i, d in items if i.filename != 'docProps/thumbnail.jpeg']
        items = [(i, re.sub(rb'<Relationship [^>]*metadata/thumbnail[^>]*/>', b'', d) if i.filename == '_rels/.rels' else d)
                 for i, d in items]
        if not any(i.filename.lower().endswith(('.jpeg', '.jpg')) for i, _ in items):
            items = [(i, re.sub(rb'<Default Extension="jpeg"[^>]*/>', b'', d) if i.filename == '[Content_Types].xml' else d)
                     for i, d in items]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            ni = zipfile.ZipInfo(info.filename, date_time=STAMP)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = 0o644 << 16
            if info.filename == 'docProps/app.xml':
                if b'<Application>' in data:
                    data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>' + (producer_app or 'Microsoft Excel').encode()
                                  + b'</Application>', data)
                else:
                    data = data.replace(b'</Properties>', b'<Application>' + (producer_app or 'Microsoft Office Word').encode()
                                        + b'</Application></Properties>')
                if b'<AppVersion>' in data:
                    data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
                if stats:
                    for k, v in stats.items():
                        data = re.sub(rb'<%s>[^<]*</%s>' % (k.encode(), k.encode()), b'<%s>%d</%s>' % (k.encode(), v, k.encode()), data)
            if info.filename == 'docProps/core.xml':
                m = re.search(rb'<dcterms:created[^>]*>([^<]*)</dcterms:created>', data)
                if m and not keep_modified:
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


def sheet_rows(ws, header, rows, widths=None, fmt=None, start=1):
    for j, h in enumerate(header, start=1):
        c = ws.cell(row=start, column=j, value=h)
        c.font = Font(bold=True)
    for i, r in enumerate(rows, start=start + 1):
        for j, v in enumerate(r, start=1):
            ws.cell(row=i, column=j, value=v)
    ws.freeze_panes = ws.cell(row=start + 1, column=1).coordinate
    for i, h in enumerate(header, start=1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(10, min(34, len(str(h)) + 3)))
    if fmt:
        for col, nf in fmt.items():
            if col not in header:
                continue
            j = header.index(col) + 1
            for row in ws.iter_rows(min_row=start + 1, min_col=j, max_col=j):
                for c in row:
                    c.number_format = nf


def pdf_stamp(path, stamp):
    """The writer's fixed 2000-01-01 dates replaced by the document's own, byte for byte at equal length so the
    cross-reference offsets stand, and the writer's comment lines blanked."""
    fixed = b"D:20000101000000+00'00'"
    assert len(stamp) == len(fixed)
    with open(path, 'rb') as f:
        data = f.read()
    assert data.count(fixed) == 2, path
    data = data.replace(fixed, stamp)
    for sig in (b' ReportLab Generated PDF document (opensource)', b' ReportLab generated PDF document -- digest (opensource)'):
        assert data.count(sig) == 1, (path, sig)
        data = data.replace(sig, b' ' * len(sig))
    with open(path, 'wb') as f:
        f.write(data)


# ---------------------------------------------------------------- the pack's record files
def bills_file(export):
    def cons(r):
        return '%d' % int(r['consumption']) if r['uom'] == 'CCF' else '%.3f' % r['consumption']
    rows = []
    for r in export:
        rows.append([r['account_no'], r['premise_id'], r['service_area'], r['customer_class'], r['rate_code'],
                     r['meter_size_in'], r['read_cycle'], r['bill_no'], r['bill_date'].isoformat(),
                     r['read_date_prev'].isoformat(), r['read_date'].isoformat(), r['read_type'], r['uom'], cons(r),
                     '%.2f' % r['base_charge'], '%.2f' % r['block1_charge'], '%.2f' % r['block2_charge'],
                     '%.2f' % r['block3_charge'], '%.2f' % r['capital_recovery_charge'], '%.2f' % r['total_charge'],
                     r['bill_status'], r['replaces_bill_no']])
    write_csv(F_BILLS, R.BILL_COLS, rows)
    return len(rows)


def accounts_file(master):
    rows = [[r['account_no'], r['premise_id'], r['service_area'], r['customer_class'], r['rate_code'], r['meter_size_in'],
             r['read_cycle'], r['service_address'], r['dwelling_units'], r['open_date'].isoformat(),
             r['close_date'].isoformat() if r['close_date'] else '', r['account_status']] for r in master]
    write_csv(F_ACCTS, R.MASTER_COLS, rows)
    return len(rows)


def reads_file(rows):
    out = [[r['facility_id'], r['meter_id'], r['read_date'].strftime('%m/%d/%Y'), r['read_time'], r['register'],
            r['read_method'], r['reader']] for r in rows]
    write_csv(F_READS, R.READ_COLS, out)
    return len(out)


def facilities_file(rows):
    out = [[r['facility_id'], r['facility'], r['service_address'], r['service_type'], r['meter_id'], r['meter_size_in'],
            r['register_unit'], r['installed'].strftime('%m/%d/%Y'), r['read_cycle']] for r in rows]
    write_csv(F_FACS, R.FAC_COLS, out)
    return len(out)


def fill_files(rows):
    write_csv(F_FILL, R.FILL_COLS, [R.fill_row(r) for r in rows])
    mon = R.fill_monthly(rows)
    wb = book('Corvane BWS', dt.datetime(2026, 11, 1, 6, 14, 52))
    ws = wb.active
    ws.title = 'Monthly activity'
    ws['A1'] = 'Corvane Fill Systems  |  Bulk Water Station Manager'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = 'Site: Ardley Springs Bulk Water Station, 1220 Quarry Rd (site 0417)'
    ws['A3'] = 'Report: Monthly activity by bay, 01/01/2026 to 10/31/2026'
    ws['A4'] = 'Generated: 11/01/2026 06:14 MST'
    header = ['Month', 'Bay', 'Transactions', 'Gallons dispensed', 'Sales (USD)']
    out = []
    for y, m in [(2026, k) for k in range(1, 11)]:
        tt = [0, 0, 0.0]
        for bay in (1, 2):
            t = mon.get((y, m, bay), [0, 0, 0.0])
            out.append(['%s %d' % (dt.date(y, m, 1).strftime('%b'), y), 'Bay %d' % bay, t[0], t[1], round(t[2], 2)])
            tt = [tt[0] + t[0], tt[1] + t[1], tt[2] + t[2]]
        out.append(['%s %d' % (dt.date(y, m, 1).strftime('%b'), y), 'Site total', tt[0], tt[1], round(tt[2], 2)])
    sheet_rows(ws, header, out, widths={'Month': 12, 'Bay': 12, 'Transactions': 14, 'Gallons dispensed': 18,
                                         'Sales (USD)': 14}, fmt={'Gallons dispensed': '#,##0', 'Sales (USD)': '#,##0.00'},
               start=6)
    p = os.path.join(TGT, F_FILLM)
    wb.save(p)
    normalise_zip(p, 'Microsoft Excel')
    return len(rows), len(out)


def work_orders_file(rows):
    wb = book('Meter Shop', dt.datetime(2026, 10, 30, 15, 42, 7))
    ws = wb.active
    ws.title = 'Completed'
    header = R.WO_COLS
    out = []
    for r in rows:
        out.append([r['work_order'], r['completed'], r['location_type'], r['location_id'], r['action'], r['old_meter_id'],
                    r['old_final_read'], r['old_register_unit'], r['new_meter_id'], r['new_initial_read'],
                    r['new_register_unit'], r['technician'], r['notes']])
    sheet_rows(ws, header, out, widths={'work_order': 13, 'completed': 12, 'location_type': 15, 'location_id': 12,
                                         'notes': 44}, fmt={'completed': 'mm/dd/yyyy'})
    p = os.path.join(TGT, F_WO)
    wb.save(p)
    normalise_zip(p, 'Microsoft Excel')
    return len(out)


# ---------------------------------------------------------------- distractors
def weather_file():
    rng = np.random.default_rng([W.SEED, 51])
    rows = []
    for d, tmax, tmin, pr, et in W.WEATHER:
        miss = rng.random() < 0.006
        rows.append([d.isoformat(), 'BVW03', '' if miss else '%.1f' % (tmax * 9 / 5 + 32), '' if miss else '%.1f' % (tmin * 9 / 5 + 32),
                     '%.2f' % (pr / 25.4), '' if miss else '%.2f' % (et / 25.4)])
    write_csv(F_WX, ['date', 'station', 'tmax_f', 'tmin_f', 'precip_in', 'eto_in'], rows)
    return len(rows)


STATE_SYSTEMS = [
    ('Ardley Springs, City of', None), ('Sagecrest Water Works, Town of', 6240), ('Hollis Ranch Mutual Water Co', 1890),
    ('Antelope Flats Water District', 3410), ('Cedar Breaks Water Users Assn', 860), ('Pine Hollow Improvement District', 2290),
    ('Sagebrush Estates MHP', 410), ('Kestle Canyon Water Co', 1170), ('Granite Point, Town of', 4980),
    ('Lodgepole Village Water', 720), ('Millrace Springs Water District', 2730), ('North Fork Domestic Water Assn', 1340),
    ('Red Butte, City of', 11820), ('Tamarisk Bend Water Co-op', 560), ('Upland Mesa Water District', 8460),
    ('Westfork, Town of', 3920), ('Yarrow Creek Ranches HOA', 380), ('Bluestem Water Improvement Dist', 1610),
    ('Dry Lake Water Works', 940), ('Elkhorn Ridge Utilities', 2140), ('Foothill Acres Water Co', 650),
    ('Harvest Valley Water District', 5320), ('Ironstone, City of', 27360), ('Juniper Hills Water Assn', 1020),
    ('Larkspur Meadows Water', 470), ('Mesquite Junction Water', 590), ('Orchard Valley Water District', 7140),
    ('Pinyon Ridge Mutual', 830), ('Quarry Hill Water Co', 1260), ('Saltgrass Flats Water District', 2050),
    ('Sandstone, Town of', 3680), ('Shale Creek Water Users', 690), ('Tableland Water Co-op', 1480),
    ('Vista Grande Water District', 9870), ('Windmill Ranch Estates', 310), ('Caprock Water Improvement Dist', 1730),
    ('Chamisa Hills Water Co', 1150), ('Desert Willow Utilities', 2560), ('Gambel Oak Water Assn', 540),
]


def state_file(export):
    rng = np.random.default_rng([W.SEED, 52])
    # the city's own row from its 2025 bills: residential deliveries (single-family and multi-family), total sales
    res = sum((r['consumption'] * W.CCF_KGAL if r['uom'] == 'CCF' else r['consumption'])
              for r in export if r['bill_status'] != 'CANCELLED' and r['bill_date'].year == 2025
              and r['customer_class'] in ('RES-SF', 'RES-MF'))
    tot = sum((r['consumption'] * W.CCF_KGAL if r['uom'] == 'CCF' else r['consumption'])
              for r in export if r['bill_status'] != 'CANCELLED' and r['bill_date'].year == 2025)
    conns = len({r['account_no'] for r in export if r['bill_status'] != 'CANCELLED' and r['bill_date'].year == 2025
                 and r['bill_date'].month == 12})
    rows = []
    for name, pop in STATE_SYSTEMS:
        if pop is None:
            pop_s = 19240
            res_af = round(res / W.AF_KGAL)
            prod_af = round(tot / W.AF_KGAL / 0.885)
            conn = conns
        else:
            pop_s = pop
            gpcd = float(rng.normal(132, 24))
            res_af = round(pop * gpcd * 365 / 325851.0)
            prod_af = round(res_af / float(rng.uniform(0.58, 0.78)))
            conn = int(pop / float(rng.uniform(2.3, 2.8)))
        rows.append([name, pop_s, conn, prod_af, res_af, round(res_af * 325851.0 / pop_s / 365), round(prod_af * 325851.0 / pop_s / 365)])
    rows.sort(key=lambda r: r[0])
    wb = book('Water Use Program', dt.datetime(2026, 6, 19, 10, 3, 38))
    ws = wb.active
    ws.title = 'CY2025'
    ws['A1'] = 'Division of Water Rights, Water Use Program'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = 'Public water system water use, calendar year 2025 (as reported by the systems; not audited)'
    ws['A3'] = 'Region 4 (Upper Brennan Basin and Upper Fork). Published June 19, 2026.'
    header = ['System', 'Population served', 'Service connections', 'Total production (acre-feet)',
              'Residential deliveries (acre-feet)', 'Residential GPCD', 'Total GPCD']
    tot_row = ['Region total', sum(r[1] for r in rows), sum(r[2] for r in rows), sum(r[3] for r in rows),
               sum(r[4] for r in rows), round(sum(r[4] for r in rows) * 325851.0 / sum(r[1] for r in rows) / 365),
               round(sum(r[3] for r in rows) * 325851.0 / sum(r[1] for r in rows) / 365)]
    sheet_rows(ws, header, rows + [tot_row], widths={'System': 36}, fmt={'Population served': '#,##0',
                                                                       'Total production (acre-feet)': '#,##0',
                                                                       'Residential deliveries (acre-feet)': '#,##0'}, start=5)
    ws.cell(row=5 + len(rows) + 1, column=1).font = Font(bold=True)
    p = os.path.join(TGT, F_STATE)
    wb.save(p)
    normalise_zip(p, 'Microsoft Excel')
    return len(rows) + 1


def rebates_file(prems):
    rng = np.random.default_rng([W.SEED, 53])
    progs = [('Turf replacement', 0.22), ('Smart irrigation controller', 0.31), ('High-efficiency toilet', 0.33),
             ('Rain sensor', 0.14)]
    pw = np.array([p[1] for p in progs])
    rows = []
    sfr = [p for p in prems if p.cls == 'SFR']
    n = 0
    for p in sfr:
        if rng.random() < 0.19:
            k = int(rng.choice(len(progs), p=pw))
            prog = progs[k][0]
            app = dt.date(2022, 3, 1) + dt.timedelta(days=int(rng.integers(0, 1690)))
            while app.weekday() >= 5:
                app += dt.timedelta(days=1)
            acc = [a for a in p.accounts if a.start <= app and (a.end is None or a.end > app)]
            if not acc:
                continue
            done = app + dt.timedelta(days=int(rng.integers(12, 95)))
            if done > dt.date(2026, 10, 30):
                done = None
            if prog == 'Turf replacement':
                qty = int(rng.integers(3, 30)) * 50
                amt, unit = min(3000, 1.5 * qty), 'sq ft'
            elif prog == 'Smart irrigation controller':
                qty, amt, unit = 1, 150.0, 'each'
            elif prog == 'High-efficiency toilet':
                qty = int(rng.choice([1, 1, 2, 2, 3]))
                amt, unit = 75.0 * qty, 'each'
            else:
                qty, amt, unit = 1, 40.0, 'each'
            n += 1
            rows.append([app, acc[0].acct, p.pid, R.AREA_NAME[p.area], prog, qty, unit, done, amt if done else ''])
    rows.sort(key=lambda r: (r[0], r[1]))
    out = []
    seq = 2200 + int(rng.integers(10, 90))
    for r in rows:
        seq += int(rng.integers(1, 4))
        out.append(['R%02d-%04d' % (r[0].year % 100, seq), r[1], r[2], r[3], r[4], r[0].isoformat(), r[5], r[6],
                    r[7].isoformat() if r[7] else '', ('%.2f' % r[8]) if r[8] != '' else '',
                    'PAID' if r[7] else 'OPEN'])
    write_csv(F_REB, ['rebate_no', 'account_no', 'premise_id', 'service_area', 'program', 'application_date', 'quantity',
                      'unit', 'completion_date', 'rebate_usd', 'status'], out)
    return len(out)


# ---------------------------------------------------------------- provenance
SOURCES = {
    F_BILLS: "the billing system's bill export, every water bill issued June 2022 to October 2026",
    F_ACCTS: "the billing system's account master as at the export date",
    F_R2144: 'City Council resolution setting water rates from January 2022',
    F_R2312: 'City Council resolution setting water rates from July 2023',
    F_R2417: 'City Council resolution establishing the Fenwick Mesa capital recovery charge from July 2024',
    F_DCP: "the Water Department's drought contingency plan, revision 2",
    F_UBB: "the wholesale district's notice of its 2027 dry-year allocation",
    F_STAFF: "the department's draft council agenda report on the Stage 2 rate options",
    F_FILL: "the bulk fill station controller's card transaction export, January to October 2026",
    F_FILLM: "the fill station vendor's monthly activity report",
    F_READS: "the read log of the City's own facility meters",
    F_FACS: "the meter list of the City's own facility services",
    F_WO: "the meter shop's completed work orders, 2025 and 2026",
    F_WX: "a regional agricultural weather station's daily record",
    F_STATE: "the state water use program's 2025 public water system table for the region",
    F_REB: "the conservation program's rebate register",
}


def metadata(counts):
    files = []
    for n in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, n)
        ext = n.rsplit('.', 1)[1]
        files.append(dict(path=n, format=ext, bytes=os.path.getsize(p), rows=ROWS.get(n), source=SOURCES[n],
                          date=ASOF, license='CC0 (original work, constructed for this task)'))
    big = max((f for f in files if f['rows']), key=lambda f: f['rows'])
    origin = ("constructed for this task by task314/generator/build.py (seeded, deterministic) in the layouts of a small "
              "city water utility's billing export and account master, its council's rate resolutions, its drought "
              "plan and draft agenda report, a wholesale water district's allocation notice, a bulk fill station's "
              "transaction export and vendor report, a facility meter read log and meter list, a meter shop's work "
              "orders, a weather station record, a state water use table and a rebate register; the city, the district, "
              "the companies and the people are fictional.")
    meta = {
        'task': 'task314', 'architecture': 1,
        'title': ('Which Stage 2 drought rate option takes the most water off Ardley Springs single-family bills in '
                  'summer 2027, and the 2026 base for the City\'s own Stage 2 measures'),
        'domain': 'Economics & Econometrics', 'subdomain': 'elasticity-welfare-policy-impact-estimation',
        'client_task_type': 'elasticity-welfare-policy-impact-estimation', 'objective': 'Opportunity Sizing & Decision Support',
        'prompt_shape': '07 grid of cells', 'as_of': ASOF,
        'deliverables': ['stage2_drought_rates_2027.xlsx', 'stage2_rate_recommendation.docx', 'summer_2027_savings.png'],
        'distractor_files': DISTRACTORS,
        'wrong_basis_distractors': [],
        'stated_inputs': ['Stage 2', 'June to September', '2027', '2026'],
        'field_terms': [],
        'input_gates': {'files': len(files), 'formats': sorted({f['format'] for f in files}), 'largest_file': big['path'],
                        'largest_file_rows': big['rows']},
        'sources': [{'files': 'all files under target/', 'origin': origin, 'date': ASOF, 'license': 'CC0 (original work)'}],
        'created': ASOF, 'generator': 'task314/generator/build.py', 'files': files,
    }
    with open(os.path.join(TASK, 'metadata.json'), 'w') as f:
        json.dump(meta, f, indent=1)


def zip_target():
    path = os.path.join(TASK, 'target.zip')
    names = sorted(os.listdir(TGT))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:
            info = zipfile.ZipInfo(n, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(TGT, n), 'rb') as f:
                z.writestr(info, f.read())
    return path


def set_mtimes():
    ts = EXPORT.timestamp()
    for n in os.listdir(TGT):
        os.utime(os.path.join(TGT, n), (ts, ts))


def world():
    prems = W.make_accounts(W.make_premises())
    bills = W.simulate_bills(prems)
    export = R.export_bills(bills)
    fdaily = R.facility_daily()
    reads, swaps, meter, unit = R.facility_reads(fdaily)
    facs = R.facility_list(meter, unit)
    fill_rows, sessions, cards = R.fill_station()
    wos = R.work_orders(prems, swaps)
    return dict(prems=prems, bills=bills, export=export, fdaily=fdaily, reads=reads, swaps=swaps, facs=facs,
                fill=fill_rows, sessions=sessions, wos=wos)


def main():
    import docs
    import golden
    w = world()
    accts = [a.acct for p in w['prems'] for a in p.accounts]
    assert len(accts) == len(set(accts)), 'account numbers repeat'
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    counts = {}
    counts['bills'] = bills_file(w['export'])
    counts['accounts'] = accounts_file(R.account_master(w['prems']))
    counts['reads'] = reads_file(w['reads'])
    counts['facilities'] = facilities_file(w['facs'])
    counts['fill'], counts['fill_monthly'] = fill_files(w['fill'])
    counts['work_orders'] = work_orders_file(w['wos'])
    counts['weather'] = weather_file()
    counts['state'] = state_file(w['export'])
    counts['rebates'] = rebates_file(w['prems'])
    docs.two_pass(docs.resolution_2021_44, os.path.join(TGT, F_R2144))
    docs.two_pass(docs.resolution_2023_12, os.path.join(TGT, F_R2312))
    docs.two_pass(docs.resolution_2024_17, os.path.join(TGT, F_R2417))
    docs.two_pass(docs.drought_plan, os.path.join(TGT, F_DCP))
    docs.two_pass(docs.district_notice, os.path.join(TGT, F_UBB))
    pdf_stamp(os.path.join(TGT, F_R2144), b"D:20211215101233-07'00'")
    pdf_stamp(os.path.join(TGT, F_R2312), b"D:20230524143908-06'00'")
    pdf_stamp(os.path.join(TGT, F_R2417), b"D:20240612091547-06'00'")
    pdf_stamp(os.path.join(TGT, F_DCP), b"D:20250327155214-06'00'")
    pdf_stamp(os.path.join(TGT, F_UBB), b"D:20261015112736-06'00'")
    docs.staff_report(os.path.join(TGT, F_STAFF), dt.datetime(2026, 10, 21, 9, 14, 37), dt.datetime(2026, 10, 27, 14, 52, 19))
    normalise_zip(os.path.join(TGT, F_STAFF), 'Microsoft Office Word', keep_modified=True, total_time=186)
    set_mtimes()
    golden.main(w['export'], w['fill'], w['reads'], w['wos'], w['facs'], normalise_zip)
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
