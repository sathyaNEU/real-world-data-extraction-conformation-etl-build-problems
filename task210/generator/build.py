"""task210 build: python3 build.py writes target/, golden/, generator/figures.json, metadata.json and target.zip."""
import datetime as dt
import json
import os
import shutil
import sys
import time
import zipfile
import numpy as np
import world as W
import pack
import docs
import golden

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
GLD = os.path.join(TASK, 'golden')
PACK_MTIME = time.mktime((2026, 11, 30, 9, 15, 0, 0, 0, -1))
GOLD_MTIME = time.mktime((2026, 12, 4, 15, 40, 0, 0, 0, -1))
ZIP_DATE = (2026, 11, 30, 9, 15, 0)


def cut_zip(src_dir, path):
    """target.zip: the pack's files at the root, sorted, deflated, one fixed date and mode, so two builds match."""
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src_dir)):
            zi = zipfile.ZipInfo(f, ZIP_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src_dir, f), 'rb').read())


def p(key):
    return os.path.join(TGT, pack.FILES[key])


def blasts_xlsx(path, Wd):
    rng = np.random.default_rng(Wd['seed'] + 20)
    rows = []
    for i, (d, tl, face, bench) in enumerate(Wd['blasts']):
        holes = int(rng.integers(14, 31))
        mic = round(float(rng.uniform(68, 112)), 1)
        rows.append(('B26-%03d' % (i + 31), tl.strftime('%d/%m/%Y'), tl.strftime('%H:%M'), '%s, bench %d' % (face, bench),
                     holes, mic, round(float(rng.uniform(0.6, 3.9)), 2), round(float(rng.uniform(0.4, 2.6)), 2),
                     round(float(rng.uniform(104, 119)), 1)))
    docs.xlsx(path, [('Blasts', ['Blast', 'Date', 'Time', 'Location', 'Holes', 'MIC (kg)', 'PPV Ulverthorpe Lane (mm/s)',
                                 'PPV Ravensby Farm (mm/s)', 'Air overpressure (dB lin)'], rows)],
              'Shotfirer', 'Calderwick Stone Ltd', '2026-01-06T07:48:00Z|2026-11-03T08:10:00Z', 'Blast register 2026',
              widths={'Blasts': [9, 11, 7, 22, 7, 9, 12, 12, 12]})


def complaints_xlsx(path, Wd):
    """Complaints come mostly on the louder working afternoons; ordinary wording, no route or view."""
    rng = np.random.default_rng(Wd['seed'] + 21)
    m, ends = Wd['mp1'], Wd['ends']
    addrs = ['3 Ulverthorpe Lane', '7 Ulverthorpe Lane', '12 Ulverthorpe Lane', 'Rose Cottage, Ulverthorpe Lane',
             '2 Low Green', '5 Low Green', 'The Old Forge, Low Green', '1 Back Lane', '9 Back Lane', 'Garth House, Back Lane']
    texts = ['Noise from the quarry again this afternoon.', 'Engine noise most of the afternoon, could hear it indoors.',
             'Constant revving from about half one, windows shut and still hear it.', 'Reversing alarms going all morning.',
             'Very noisy today, worse than last week.', 'Heavy diesel noise on and off since 8.',
             'Rumbling from the quarry over lunch time.', 'Can the quarry keep it down please, we have a new baby.',
             'Loud engines, could not sit out in the garden.', 'Banging and engine noise from about 2 until they stopped.',
             'Dust on the cars and windowsills again.', 'Grinding noise from the crusher all day.',
             'Lorries revving hard, very wearing.', 'Noisy from first thing, heard it over the radio.',
             'Same as Tuesday, engine noise most of the day.', 'Is something different going on? Much louder today.',
             'Beeping and engines, on and off.', 'Woken at 7 by engine noise.', 'Heavy plant noise late afternoon.',
             'Droning noise, worse when the wind is this way.', 'Noise carried right across Low Green this afternoon.',
             'Very loud this morning, quieter after lunch.', 'Constant drone from the quarry, it gives me a headache.',
             'Engine noise all day, the dog will not settle.', 'Worse than usual today, the plant and the trucks.',
             'Asked about working hours, says noise heard after 5.', 'Revving and clanking from about 10.',
             'Louder than it has been for months.', 'Can hear the quarry with the windows closed.',
             'Wanted to know if the quarry is working Saturdays now.']
    actions = [('Acknowledged by email.', 6), ('Phoned back, MP1 record checked for the afternoon.', 4),
               ('Letter sent with the quarterly monitoring summary.', 3), ('Called back and explained the working hours.', 3),
               ('Visited caller; period to be looked at on the MP1 record.', 2), ('Acknowledged; passed to Garry Fry.', 3),
               ('No answer on callback, email sent.', 3), ('MP1 data checked for the hour given; caller informed.', 4),
               ('Logged, MP1 download pending.', 2), ('Spoke to caller; reversing alarm on T41 to be changed to a white-noise type.', 1),
               ('Bowser out; dust reported to the manager.', 1), ('Acknowledged; caller to keep a diary for two weeks.', 2),
               ('Phoned, caller satisfied with the explanation.', 2), ('Acknowledged by letter within two days.', 3),
               ('Visited; noise audible at the gate, noted in the site diary.', 1)]
    aw = np.array([w for _a, w in actions], float); aw = aw / aw.sum()
    rows = []
    ref = 233
    hourly = {}
    for i, e in enumerate(ends):
        loc = e - dt.timedelta(minutes=15) + dt.timedelta(hours=W.bst_offset(e))
        if loc.weekday() < 5 and 8 <= loc.hour < 17:
            hourly.setdefault((loc.date(), loc.hour), []).append(m['laeq'][i])
    for (d, hr), vals in sorted(hourly.items()):
        L = 10 * np.log10(np.mean(10 ** (np.array(vals) / 10)))
        pr = 0.004 + 0.06 * max(0.0, L - 43.0)
        if rng.random() < pr:
            ref += 1
            recv = dt.datetime.combine(d, dt.time(hr, 0)) + dt.timedelta(minutes=float(rng.uniform(20, 300)))
            txt = texts[int(rng.integers(0, len(texts)))]
            act = actions[int(rng.choice(len(actions), p=aw))][0]
            if 'dust' in txt.lower():
                act = 'Bowser out; dust reported to the manager.'
            rows.append(('CR-26-%03d' % ref, recv.strftime('%d/%m/%Y'), recv.strftime('%H:%M'),
                         ['Phone', 'Email', 'Email', 'Web form'][int(rng.integers(0, 4))], addrs[int(rng.integers(0, len(addrs)))],
                         txt, act))
    docs.xlsx(path, [('Log', ['Ref', 'Received', 'Time', 'Method', 'Address', 'Description', 'Action'], rows)],
              docs.MANAGER, 'Calderwick Stone Ltd', '2026-01-02T09:12:00Z|2026-11-02T10:05:00Z', 'Complaints log 2026',
              widths={'Log': [11, 11, 7, 9, 28, 60, 30]})


def shifts_xlsx(path, Wd):
    rng = np.random.default_rng(Wd['seed'] + 22)
    code = {'north': 'N', 'west': 'W', 'south': 'S'}
    blast_on = {b[0]: b for b in Wd['blasts']}
    rows = []
    for (d, faces, trucks, off, sd) in Wd['days']:
        fw = code[faces[0]] if faces[0] == faces[1] else '%s, %s' % (code[faces[0]], code[faces[1]])
        rem = []
        for tk in sorted(off):
            rem.append('%s %s %s' % (['Service on', 'Tyre change on', 'Brakes on', 'Fitter on'][int(rng.integers(0, 4))], tk, off[tk]))
        if sd:
            rem.append('Haul stopped %s to %s, rain' % (sd[0].strftime('%H:%M'), sd[1].strftime('%H:%M')))
        if d in blast_on:
            rem.append('Blast %s %s' % (blast_on[d][1].strftime('%H:%M'), blast_on[d][2]))
        if rng.random() < 0.12:
            rem.append(['Grader on haul roads', 'Bowser out from 10:00', 'Fitter called to primary', 'Wheel wash blocked am',
                        'Visitor on site'][int(rng.integers(0, 5))])
        wx = 'Heavy rain' if sd else ['Dry', 'Dry', 'Dry, breezy', 'Showers', 'Rain pm', 'Overcast'][int(rng.integers(0, 6))]
        rows.append((d.strftime('%d/%m/%Y'), fw, ' '.join(trucks), round(float(rng.uniform(6.5, 10.5)), 1), wx, '; '.join(rem)))
    docs.xlsx(path, [('Shifts', ['Date', 'Faces worked', 'ADTs on haul', 'Loader hours', 'Weather', 'Remarks'], rows)],
              docs.MANAGER, 'Calderwick Stone Ltd', '2026-04-30T15:20:00Z|2026-11-02T16:30:00Z', 'Daily shift report 2026',
              widths={'Shifts': [11, 12, 30, 12, 12, 44]})


def tickets_xlsx(path, rows):
    out = [(r['ticket'], r['when'].strftime('%d/%m/%Y %H:%M'), r['account'], r['reg'], r['order'], r['code'],
            r['gross'], r['tare'], r['net'], r['price'], r['value']) for r in rows]
    docs.xlsx(path, [('Tickets', ['Ticket', 'Date/time', 'Account', 'Vehicle', 'Order no', 'Product', 'Gross (t)', 'Tare (t)',
                                  'Net (t)', 'Price (GBP/t)', 'Value (GBP)'], out)],
              'Weighbridge', 'Calderwick Stone Ltd', '2026-02-02T17:20:00Z', 'Ticket listing 01/01/2026 to 31/01/2026',
              widths={'Tickets': [8, 16, 9, 11, 9, 8, 9, 9, 9, 11, 11]})


def orders_xlsx(path, orders, seed):
    rng = np.random.default_rng(seed + 23)
    rows = []
    for (onum, acc, cust, prod, placed, qty, delivery) in sorted(orders):
        rows.append((onum, placed.strftime('%d/%m/%Y'), acc, cust, prod, qty, delivery))
    docs.xlsx(path, [('Orders', ['Order no', 'Placed', 'Account', 'Customer', 'Product', 'Quantity (t)', 'Delivery'], rows)],
              'Sales office', 'Calderwick Stone Ltd', '2026-02-03T09:00:00Z', 'Sales orders December 2025 to January 2026',
              widths={'Orders': [9, 11, 9, 28, 18, 12, 10]})


def main(seed=W.SEED):
    for d in (TGT, GLD):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    Wd = pack.build_world(seed)
    pack.write_mp1(p('mp1'), Wd)
    pack.write_telematics(p('telematics'), Wd)
    pack.write_survey(p('survey'))
    pack.write_weather(p('weather'), Wd)
    pack.write_belt(p('belt'), Wd)
    pack.write_plc(p('plc'), Wd)
    pack.write_loader(p('loader'), Wd)
    rows, port = pack.sales_tables(Wd)
    pack.write_portable(p('portable'), port, seed)
    pack.write_products(p('products'))
    tickets_xlsx(p('tickets'), rows)
    orders_xlsx(p('orders'), Wd['orders'], seed)
    blasts_xlsx(p('blasts'), Wd)
    complaints_xlsx(p('complaints'), Wd)
    shifts_xlsx(p('shifts'), Wd)
    docs.conditions(p('conditions'))
    docs.nmp(p('nmp'), round(W.filed_residual(Wd['mp1'], Wd['ends']), 1))
    docs.scheme(p('scheme'))
    docs.register(p('register'))
    docs.dno(p('dno'), Wd['outages'])
    for f in os.listdir(TGT):
        os.utime(os.path.join(TGT, f), (PACK_MTIME, PACK_MTIME))
    G = golden.compute(TGT)
    golden.write(G, GLD)
    for f in os.listdir(GLD):
        os.utime(os.path.join(GLD, f), (GOLD_MTIME, GOLD_MTIME))
    json.dump(golden.figures(G), open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True)
    meta = {
        'task': 'task210',
        'decision': 'how many articulated dump trucks haul from the Phase 4 extension in January 2027 within the noise '
                    'management plan\'s haulage share at MP1',
        'deliverables': ['extension_haul_dial.csv', 'extension_scheme_note.pdf'],
        'distractor_files': ['target/' + pack.FILES[k] for k in pack.DISTRACTORS],
        'files': {pack.FILES[k]: {'source': 'constructed operating record of a fictional quarry', 'licence': 'CC BY 4.0',
                                  'date': '2026-11-30'} for k in pack.FILES},
    }
    json.dump(meta, open(os.path.join(TASK, 'metadata.json'), 'w'), indent=1, sort_keys=True)
    cut_zip(TGT, os.path.join(TASK, 'target.zip'))
    return Wd, G


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else W.SEED)
