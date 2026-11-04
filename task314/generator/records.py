"""The records the city's systems keep, cut from the world.

The billing system's export of every water bill and its account master; for 2026 the bulk fill station's card
transactions and its vendor's monthly summary, the read log and meter list of the city's own facility meters,
and the meter shop's completed work orders.
"""
import datetime as dt
import math
import numpy as np
import world as W

AREA_NAME = {'CITY': 'ARDLEY SPRINGS', 'FMSA': 'FENWICK MESA'}
CLASS_CODE = {'SFR': ('RES-SF', 'W10'), 'MFR': ('RES-MF', 'W20'), 'COM': ('COMM', 'W30'), 'IRR': ('IRRG', 'W40')}
EXPORT_DATE = dt.date(2026, 11, 2)


def meter_text(m):
    return {0.75: '0.75', 1.0: '1', 1.5: '1.5', 2.0: '2'}[m]


# ---------------------------------------------------------------- the bill export
def _uom(p, d1):
    if p.area == 'FMSA' and p.legacy_until is not None and d1 < p.legacy_until:
        return 'CCF'
    return 'KGAL'


def _in_uom(kgal, uom):
    """Consumption as the register shows it: whole hundred cubic feet, or gallons (thousands to three places)."""
    if uom == 'CCF':
        return float(int(round(kgal / W.CCF_KGAL)))
    return round(kgal, 3)


def _kgal(cons, uom):
    return cons * W.CCF_KGAL if uom == 'CCF' else cons


def _charges(p, kg, bd, m):
    base, vol, cap = W.charges_as_billed(dict(prem=p, q=kg, bdate=bd, m=m))
    return round(base, 2), [round(v, 2) for v in vol], round(cap, 2)


def export_bills(bills):
    """Rows of the customer information system's bill export.  An estimated read is caught up on the next actual
    read, a misread caught after the run is cancelled and rebilled in the same month, and the register's own
    precision is carried from bill to bill."""
    rng = np.random.default_rng([W.SEED, 11])
    by_acct = {}
    for b in bills:
        by_acct.setdefault(b['acc'].acct, []).append(b)
    out = []
    for acct in sorted(by_acct):
        bl = sorted(by_acct[acct], key=lambda x: x['t'])
        owe = 0.0                         # kgal billed ahead of use (an estimate or the register's rounding)
        hist = []
        for i, b in enumerate(bl):
            p = b['prem']
            uom = _uom(p, b['d1'])
            true_q = b['q']
            rtype = 'A'
            if 3 <= i < len(bl) - 1 and rng.random() < 0.008:
                target = max(0.0, float(np.mean(hist[-3:])) * float(rng.uniform(0.85, 1.10)))
                rtype = 'E'
            else:
                target = max(0.0, true_q - owe)
            cons = _in_uom(target, uom)
            kg = _kgal(cons, uom)
            owe += kg - true_q
            hist.append(kg)
            base, vol, cap = _charges(p, kg, b['bdate'], b['m'])
            cls, rate = CLASS_CODE[p.cls]
            row = dict(account_no=acct, premise_id=p.pid, service_area=AREA_NAME[p.area], customer_class=cls,
                       rate_code=rate, meter_size_in=meter_text(p.meter), read_cycle='%02d' % (p.cycle + 1),
                       bill_date=b['bdate'], read_date_prev=b['d0'], read_date=b['d1'], read_type=rtype, uom=uom,
                       consumption=cons, base_charge=base, block1_charge=vol[0], block2_charge=vol[1],
                       block3_charge=vol[2], capital_recovery_charge=cap, bill_status='BILLED', replaces_bill_no='',
                       _kgal=kg, _cls=p.cls, _area=p.area, _meter=p.meter, _y=b['y'], _m=b['m'], _true=true_q, _t=b['t'])
            row['total_charge'] = round(base + sum(vol) + cap, 2)
            if rtype == 'A' and cons > 0 and rng.random() < 0.003:
                # a misread the high-low edit caught after the bill went out: cancelled and rebilled in the month
                bad = _in_uom(kg * float(rng.uniform(1.6, 3.2)) + float(rng.uniform(2, 9)), uom)
                bkg = _kgal(bad, uom)
                bb, bv, bc = _charges(p, bkg, b['bdate'], b['m'])
                canc = dict(row)
                canc.update(consumption=bad, base_charge=bb, block1_charge=bv[0], block2_charge=bv[1],
                            block3_charge=bv[2], capital_recovery_charge=bc, total_charge=round(bb + sum(bv) + bc, 2),
                            bill_status='CANCELLED', _kgal=bkg)
                reb = dict(row)
                rd = b['bdate'] + dt.timedelta(days=int(rng.integers(2, 7)))
                while rd.weekday() >= 5:
                    rd += dt.timedelta(days=1)
                if rd.month != b['bdate'].month:
                    rd = b['bdate'] + dt.timedelta(days=1)
                    while rd.weekday() >= 5 and rd.month == b['bdate'].month:
                        rd += dt.timedelta(days=1)
                reb.update(bill_status='REBILL', bill_date=rd)
                out.append(canc)
                out.append(reb)
            else:
                out.append(row)
    # bill numbers in run order: by bill date, then cycle and account, with the gaps other services' bills leave
    out.sort(key=lambda r: (r['bill_date'], r['read_cycle'], r['account_no'], r['bill_status'] == 'REBILL'))
    n = 6100000 + int(rng.integers(1000, 9000))
    for r in out:
        n += int(rng.integers(1, 4))
        r['bill_no'] = '%08d' % n
    canc_no = {(r['account_no'], r['read_date']): r['bill_no'] for r in out if r['bill_status'] == 'CANCELLED'}
    for r in out:
        if r['bill_status'] == 'REBILL':
            r['replaces_bill_no'] = canc_no[(r['account_no'], r['read_date'])]
    return out


BILL_COLS = ['account_no', 'premise_id', 'service_area', 'customer_class', 'rate_code', 'meter_size_in', 'read_cycle',
             'bill_no', 'bill_date', 'read_date_prev', 'read_date', 'read_type', 'uom', 'consumption', 'base_charge',
             'block1_charge', 'block2_charge', 'block3_charge', 'capital_recovery_charge', 'total_charge', 'bill_status',
             'replaces_bill_no']


def account_master(prems):
    rng = np.random.default_rng([W.SEED, 12])
    rows = []
    for p in prems:
        cls, rate = CLASS_CODE[p.cls]
        for a in p.accounts:
            if a.start > dt.date(2022, 5, 1):
                opened = a.start
            elif p.area == 'FMSA':
                opened = dt.date(2021, 10, 1)       # converted from the Fenwick Mesa Water Company's system
            else:
                opened = dt.date(1996, 1, 1) + dt.timedelta(days=int(rng.integers(0, 9500)))
            rows.append(dict(account_no=a.acct, premise_id=p.pid, service_area=AREA_NAME[p.area], customer_class=cls,
                             rate_code=rate, meter_size_in=meter_text(p.meter), read_cycle='%02d' % (p.cycle + 1),
                             service_address=p.addr, dwelling_units=p.units if p.cls == 'MFR' else '',
                             open_date=opened, close_date=a.end or '', account_status='FINALED' if a.end else 'ACTIVE'))
    rows.sort(key=lambda r: (r['read_cycle'], r['premise_id'], r['account_no']))
    return rows


MASTER_COLS = ['account_no', 'premise_id', 'service_area', 'customer_class', 'rate_code', 'meter_size_in', 'read_cycle',
               'service_address', 'dwelling_units', 'open_date', 'close_date', 'account_status']


# ---------------------------------------------------------------- the city's own facility meters
D0, D1 = dt.date(2025, 9, 1), dt.date(2026, 10, 31)
FDAYS = [D0 + dt.timedelta(days=i) for i in range((D1 - D0).days + 1)]

# facility id, name, service address, kind, base kgal a day, kgal a day per unit of irrigation demand, read cycle,
# service type, meter size
FACILITIES = [
    ('GC-MUNI', 'Ardley Springs Municipal Golf Course', '2200 N Canyon Rim Rd', 'irr', 6.0, 118.0, 6, 'Irrigation', '2'),
    ('PK-RIVR', 'Riverside Park', '410 Orchard Ave', 'irr', 1.2, 26.0, 3, 'Irrigation', '2'),
    ('PK-CTWD', 'Cottonwood Park', '1875 Cottonwood St', 'irr', 0.8, 19.0, 11, 'Irrigation', '1.5'),
    ('CEM-MSV', 'Mesa View Cemetery', '3300 Foothill Dr', 'irr', 1.8, 34.0, 9, 'Irrigation', '2'),
    ('CH-LIB', 'City Hall and Library', '100 E Main St', 'bldg', 2.6, 1.5, 0, 'Domestic', '2'),
    ('FS-1', 'Fire Station 1', '215 Northgate Way', 'bldg', 1.4, 0.6, 2, 'Domestic', '1.5'),
    ('FS-2', 'Fire Station 2', '960 Caprock Dr', 'bldg', 1.1, 0.5, 14, 'Domestic', '1.5'),
    ('PW-YARD', 'Public Works Yard', '1220 Quarry Rd', 'bldg', 3.1, 2.0, 7, 'Domestic', '2'),
    ('WB-PAV', 'Westbrook Park Pavilion and Pool Building', '1450 Westbrook Dr', 'bldg', 2.2, 1.0, 12, 'Domestic', '2'),
    ('WB-POOL', 'Westbrook Aquatic Center Pool Fill', '1450 Westbrook Dr', 'pool', 0.0, 0.0, 12, 'Pool fill', '1.5'),
    ('WB-FLD', 'Westbrook Sports Complex Fields', '1450 Westbrook Dr', 'irr', 0.3, 64.0, 12, 'Irrigation', '2'),
    ('PK-FMTH', 'Fenwick Mesa Trailhead Park', '45 Rimrock Ct', 'irr', 0.5, 12.0, 15, 'Irrigation', '1'),
    ('WWTP-PS', 'Water Reclamation Facility', '5100 S Dry Creek Rd', 'bldg', 4.2, 1.0, 18, 'Domestic', '2'),
    ('SR-CTR', 'Senior Center', '622 Larkspur Ln', 'bldg', 1.3, 1.8, 1, 'Domestic', '1'),
    ('MED-MAIN', 'Main Street Medians', 'Main St, 1st Ave to 9th Ave', 'irr', 0.2, 11.0, 4, 'Irrigation', '1'),
]
FAC = {f[0]: f for f in FACILITIES}
SUBMETER = 'WB-POOL'            # on the pavilion's service: its water also passes the pavilion's meter
PARENT = 'WB-PAV'
POOL_OPEN, POOL_CLOSE = dt.date(2026, 5, 22), dt.date(2026, 9, 7)
POOL_FILL = [(dt.date(2026, 5, 15), 118.4), (dt.date(2026, 5, 16), 131.7), (dt.date(2026, 5, 17), 112.6)]
POOL_REFILL = (dt.date(2026, 7, 28), 127.9)
GOLF_SWAP = dt.date(2026, 6, 2)
CEM_SWAP = dt.date(2026, 8, 4)


def _dem(day):
    i = W._WIDX[day]
    return max(0.0, (W._ET[i] - 0.62 * W._PR[i] - 1.25) / 5.4)


def facility_daily():
    """Each facility's own use each day, kgal (the pool's water is the pool fill meter's; it reaches the pool through
    the pavilion's service)."""
    rng = np.random.default_rng([W.SEED, 21])
    out = {}
    for fid, name, addr, kind, base, irr, cyc, stype, size in FACILITIES:
        scale = float(np.exp(0.15 * rng.standard_normal()))
        s = {}
        for day in FDAYS:
            if kind == 'pool':
                if POOL_OPEN <= day <= POOL_CLOSE:
                    v = (4.0 + 2.5 * _dem(day)) * float(np.exp(0.10 * rng.standard_normal()))
                else:
                    v = 0.15 * float(np.exp(0.3 * rng.standard_normal()))
                for fd, amt in POOL_FILL:
                    if day == fd:
                        v += amt
                if day == POOL_REFILL[0]:
                    v += POOL_REFILL[1]
            else:
                dem = _dem(day)
                if kind == 'irr' and day.month in (11, 12, 1, 2, 3):
                    dem = 0.0
                if kind == 'irr' and day.month == 4 and day.day < 12:
                    dem *= 0.4               # systems charged and tested in early April
                v = (base + irr * dem) * scale * float(np.exp(0.12 * rng.standard_normal()))
            s[day] = v
        out[fid] = s
    return out


def _meter_ids(rng):
    """Serials as the meter shop records them: the purchase year and the maker's serial, batch by batch."""
    yrs = {'GC-MUNI': 18, 'PK-RIVR': 14, 'PK-CTWD': 19, 'CEM-MSV': 11, 'CH-LIB': 16, 'FS-1': 16, 'FS-2': 21,
           'PW-YARD': 13, 'WB-PAV': 17, 'WB-POOL': 17, 'WB-FLD': 17, 'PK-FMTH': 22, 'WWTP-PS': 15, 'SR-CTR': 19,
           'MED-MAIN': 20}
    base = {11: 77003, 13: 140210, 14: 166873, 15: 190442, 16: 203117, 17: 231870, 18: 204380, 19: 266015,
            20: 288431, 21: 301977, 22: 330516}
    out = {}
    for fid in yrs:
        y = yrs[fid]
        base[y] += int(rng.integers(1, 60))
        out[fid] = '%02d-%06d' % (y, base[y])
    return out


def facility_reads(fdaily):
    """The read log: each facility read once a month on its cycle (drive-by radio reads or keyed visual reads), a
    keyed read the handheld rejected and the reader took again, and the two meters exchanged in 2026."""
    rng = np.random.default_rng([W.SEED, 22])
    ids = _meter_ids(rng)
    reg = {fid: float(rng.integers(30000, 3000000)) for fid in ids}
    unit = {fid: 'GAL' for fid in ids}
    meter = dict(ids)
    method = {fid: ('AMR' if rng.random() < 0.6 else 'VISUAL') for fid in ids}
    method['GC-MUNI'] = 'VISUAL'
    readers = ['KG', 'LB', 'BK', 'KG', 'LB']
    swaps = []
    rows = []
    months = [(2025, 9), (2025, 10), (2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 11)]
    last = {}
    for (y, m) in months:
        for fid, name, addr, kind, base, irr, cyc, stype, size in FACILITIES:
            rd = W.read_date(cyc, y, m)
            prev = last.get(fid)
            if prev is not None:
                days = [prev + dt.timedelta(days=i) for i in range(1, (rd - prev).days + 1)]
                own = fdaily[fid]
                for day in days:
                    q = own[day]
                    if fid == PARENT:
                        q += fdaily[SUBMETER][day]
                    sw = GOLF_SWAP if fid == 'GC-MUNI' else (CEM_SWAP if fid == 'CEM-MSV' else None)
                    if sw is not None and day == sw:
                        # the exchange at mid-morning: part of the day on the old meter, the rest on the new
                        frac = 0.42
                        reg[fid] += q * frac * 1000.0
                        old_id, old_final = meter[fid], int(math.floor(reg[fid]))
                        if fid == 'GC-MUNI':
                            new_id, init, nu = '26T-%05d' % 381, 0, 'CCF'
                        else:
                            new_id, init, nu = '26-%06d' % 412806, 37, 'GAL'
                        swaps.append(dict(fid=fid, date=sw, old=old_id, old_final=old_final, old_unit='GAL', new=new_id,
                                          new_init=init, new_unit=nu))
                        meter[fid], unit[fid], reg[fid] = new_id, nu, float(init)
                        q = q * (1 - frac)
                    reg[fid] += q / W.CCF_KGAL if unit[fid] == 'CCF' else q * 1000.0
            last[fid] = rd
            shown = int(math.floor(reg[fid]))
            meth = method[fid]
            hh = int(rng.integers(7, 15))
            mm = int(rng.integers(0, 60))
            if meth == 'VISUAL' and prev is not None and rng.random() < 0.07:
                s = str(shown)
                k = int(rng.integers(0, len(s) - 1))
                bad = s[:k] + s[k + 1] + s[k] + s[k + 2:] if s[k] != s[k + 1] else s[:k] + s[k + 1:]
                rows.append(dict(facility_id=fid, meter_id=meter[fid], read_date=rd, read_time='%02d:%02d' % (hh, mm),
                                 register=int(bad), read_method=meth, reader=readers[int(rng.integers(len(readers)))]))
                mm2 = mm + int(rng.integers(2, 9))
                hh, mm = (hh + 1, mm2 - 60) if mm2 >= 60 else (hh, mm2)
            rows.append(dict(facility_id=fid, meter_id=meter[fid], read_date=rd, read_time='%02d:%02d' % (hh, mm),
                             register=shown, read_method=meth, reader=readers[int(rng.integers(len(readers)))]))
    rows.sort(key=lambda r: (r['read_date'], r['read_time'], r['facility_id']))
    return rows, swaps, meter, unit


READ_COLS = ['facility_id', 'meter_id', 'read_date', 'read_time', 'register', 'read_method', 'reader']


def facility_list(meter, unit):
    rows = []
    installed = {'GC-MUNI': GOLF_SWAP, 'CEM-MSV': CEM_SWAP}
    rng = np.random.default_rng([W.SEED, 23])
    for fid, name, addr, kind, base, irr, cyc, stype, size in FACILITIES:
        yr = 2000 + int(meter[fid][:2])
        inst = installed.get(fid) or (dt.date(yr, 1, 1) + dt.timedelta(days=int(rng.integers(20, 340))))
        rows.append(dict(facility_id=fid, facility=name, service_address=addr, service_type=stype, meter_id=meter[fid],
                         meter_size_in='3' if fid == 'GC-MUNI' else size, register_unit=unit[fid], installed=inst,
                         read_cycle='%02d' % (cyc + 1)))
    return rows


FAC_COLS = ['facility_id', 'facility', 'service_address', 'service_type', 'meter_id', 'meter_size_in', 'register_unit',
            'installed', 'read_cycle']


# ---------------------------------------------------------------- the bulk fill station
Y0, Y1 = dt.date(2026, 1, 1), dt.date(2026, 10, 31)
DST0, DST1 = dt.date(2026, 3, 8), dt.date(2026, 11, 1)
FAULT0, FAULT1 = dt.date(2026, 6, 3), dt.date(2026, 9, 26)
RATE_100 = 0.95                 # dollars a hundred gallons, rounded up to the next hundred
HAULERS = [
    ('Dry Creek Water Hauling LLC', 9.0, (2500, 4000), 0.10, False),
    ('Mesa Top Construction', 6.0, (1800, 3500), 0.18, False),
    ('B and T Excavating', 4.0, (2000, 3800), 0.05, False),
    ('Sandoval Trucking', 5.5, (3000, 4200), 0.22, False),
    ('Ardley Springs Public Works', 3.5, (1500, 2600), 0.0, True),
    ('Pinyon Ridge Ranch', 1.6, (900, 1800), 0.0, False),
    ('Caprock Pool and Spa', 2.2, (2400, 3600), 0.30, False),
    ('Canyon Rim HOA', 0.9, (800, 1500), 0.0, False),
    ('Juniper Landscape Services', 2.8, (900, 1700), 0.12, False),
    ('Redbank Dust Control', 3.6, (3200, 4200), 0.08, False),
    ('Upper Fork Oilfield Services', 2.4, (3500, 4200), 0.15, False),
    ('Antelope Springs Livestock', 1.3, (1200, 2400), 0.0, False),
    ('Sagebrush County Road Department', 1.9, (2800, 4000), 0.06, False),
    ('Quarry Road Ready Mix', 2.1, (2600, 3900), 0.04, False),
    ('Harvest Lane Farms', 0.8, (700, 1400), 0.0, False),
]


def _offset(d):
    return '-06:00' if DST0 <= d < DST1 else '-07:00'


def _stamp(t):
    return t.strftime('%Y-%m-%dT%H:%M:%S') + _offset(t.date())


def fill_station():
    """Card sessions at the two-bay bulk fill station.  A trailer filled straight after its truck is a second
    session from the truck's closing register; when the bay 2 coupling faulted, the hauler swiped again and the
    controller resumed the session, writing its opening register and the session's whole volume on the new row."""
    rng = np.random.default_rng([W.SEED, 31])
    cards = {}
    used = set()
    for h in HAULERS:
        while True:
            c = '%04d %04d' % (int(rng.integers(1000, 9999)), int(rng.integers(1000, 9999)))
            if c not in used:
                used.add(c)
                cards[h[0]] = c
                break
    w = np.array([h[1] for h in HAULERS])
    w = w / w.sum()
    reg = {1: 4180334.0, 2: 3966012.0}
    rows = []
    sessions = []
    day = Y0
    while day <= Y1:
        season = {1: 0.40, 2: 0.42, 3: 0.55, 4: 0.75, 5: 1.0, 6: 1.08, 7: 1.10, 8: 1.05, 9: 0.95, 10: 0.80}[day.month]
        wf = 1.0 if day.weekday() < 5 else (0.45 if day.weekday() == 5 else 0.12)
        n = int(rng.poisson(8.4 * season * wf))
        # the station's evening hours end at 4:30 p.m. on the last day of a month, when the vendor's monthly close runs
        close = 16.5 * 60 if (day + dt.timedelta(days=1)).month != day.month else 20.9 * 60
        mins = sorted(float(np.clip(rng.normal(12.5 * 60, 3.3 * 60), 5 * 60, close)) for _ in range(n))
        free = {1: dt.datetime(day.year, day.month, day.day, 5, 0), 2: dt.datetime(day.year, day.month, day.day, 5, 0)}
        for tm in mins:
            arrive = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=tm, seconds=int(rng.integers(0, 60)))
            hi = int(rng.choice(len(HAULERS), p=w))
            name, _, (g_lo, g_hi), p2, city = HAULERS[hi]
            bay = 1 if free[1] <= free[2] else 2
            if free[1] <= arrive and free[2] <= arrive:
                bay = 1 if rng.random() < 0.56 else 2
            start = max(arrive, free[bay] + dt.timedelta(seconds=int(rng.integers(40, 200))))
            tanks = 2 if rng.random() < p2 else 1
            end = start
            for k in range(tanks):
                g = float(int(rng.integers(g_lo, g_hi)))
                if k == 1:
                    g = float(int(g * float(rng.uniform(0.55, 0.9))))
                s0 = reg[bay]
                dur = dt.timedelta(seconds=int(g / float(rng.uniform(125, 150)) * 60) + int(rng.integers(20, 75)))
                if bay == 2 and FAULT0 <= start.date() <= FAULT1 and rng.random() < 0.27:
                    g1 = float(int(g * float(rng.uniform(0.25, 0.75))))
                    e1 = start + dt.timedelta(seconds=int(dur.total_seconds() * g1 / g))
                    rows.append(dict(start=start, end=e1, bay=bay, card=cards[name], hauler=name, m0=int(s0),
                                     m1=int(s0 + g1), gal=int(g1), amt=0.0 if city else math.ceil(g1 / 100) * RATE_100))
                    s2 = e1 + dt.timedelta(seconds=int(rng.integers(55, 260)))
                    e2 = s2 + dt.timedelta(seconds=int(dur.total_seconds() * (g - g1) / g) + int(rng.integers(15, 50)))
                    rows.append(dict(start=s2, end=e2, bay=bay, card=cards[name], hauler=name, m0=int(s0),
                                     m1=int(s0 + g), gal=int(g),
                                     amt=0.0 if city else math.ceil((g - g1) / 100) * RATE_100))
                    end = e2
                else:
                    end = start + dur
                    rows.append(dict(start=start, end=end, bay=bay, card=cards[name], hauler=name, m0=int(s0),
                                     m1=int(s0 + g), gal=int(g), amt=0.0 if city else math.ceil(g / 100) * RATE_100))
                sessions.append(dict(date=start.date(), bay=bay, gal=int(s0 + g) - int(s0), hauler=name))
                reg[bay] = s0 + g
                start = end + dt.timedelta(seconds=int(rng.integers(70, 300)))
            free[bay] = end
        day += dt.timedelta(days=1)
    rows.sort(key=lambda r: (r['start'], r['bay']))
    n = 2650000 + int(rng.integers(100, 900))
    for r in rows:
        n += int(rng.integers(1, 4))
        r['txn_id'] = 'FS%07d' % n
    return rows, sessions, cards


FILL_COLS = ['txn_id', 'txn_start', 'txn_end', 'bay', 'card_no', 'account_name', 'meter_start_gal', 'meter_end_gal',
             'gallons', 'amount_usd']


def fill_row(r):
    return [r['txn_id'], _stamp(r['start']), _stamp(r['end']), r['bay'], r['card'], r['hauler'], r['m0'], r['m1'],
            r['gal'], '%.2f' % r['amt']]


def fill_monthly(rows):
    """The vendor's monthly activity report: transactions, gallons dispensed and sales, by bay."""
    out = {}
    for r in rows:
        k = (r['start'].year, r['start'].month, r['bay'])
        o = out.setdefault(k, [0, 0, 0.0])
        o[0] += 1
        o[1] += r['gal']
        o[2] += r['amt']
    return out


# ---------------------------------------------------------------- the meter shop
def work_orders(prems, fac_swaps):
    """Completed work orders, January 2025 to October 2026."""
    rng = np.random.default_rng([W.SEED, 41])
    rows = []
    techs = ['B. Macdonald', 'S. Clay', 'J. Williamson', 'T. Bryant', 'B. Roth']
    for p in prems:
        if p.area == 'FMSA' and p.legacy_until is not None and dt.date(2025, 1, 1) <= p.legacy_until <= dt.date(2026, 10, 30):
            d = p.legacy_until
            while d.weekday() >= 5:
                d -= dt.timedelta(days=1)
            rows.append(dict(completed=d, location_type='SERVICE', location_id=p.pid, action='REPLACE',
                             old_meter_id='FMW-%05d' % int(rng.integers(10000, 99999)),
                             old_final_read=int(rng.integers(900, 14000)), old_register_unit='CCF',
                             new_meter_id='%02d-%06d' % (d.year % 100, int(rng.integers(400000, 470000))),
                             new_initial_read=int(rng.integers(0, 30)), new_register_unit='GAL',
                             technician=techs[int(rng.integers(len(techs)))], notes='AMR change-out'))
        elif p.cls == 'SFR' and rng.random() < 0.016:
            d = dt.date(2025, 1, 6) + dt.timedelta(days=int(rng.integers(0, 660)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            note = str(rng.choice(['stopped register', 'frozen, body cracked', 'leaking at coupling', 'register fogged',
                                   'customer request, high bill', 'lid and register damaged']))
            rows.append(dict(completed=d, location_type='SERVICE', location_id=p.pid, action='REPLACE',
                             old_meter_id='%02d-%06d' % (int(rng.integers(8, 20)), int(rng.integers(30000, 290000))),
                             old_final_read=int(rng.integers(150000, 2400000)), old_register_unit='GAL',
                             new_meter_id='%02d-%06d' % (d.year % 100, int(rng.integers(400000, 470000))),
                             new_initial_read=int(rng.integers(0, 30)), new_register_unit='GAL',
                             technician=techs[int(rng.integers(len(techs)))], notes=note))
        elif p.cls in ('COM', 'IRR') and rng.random() < 0.3:
            d = dt.date(2025, 3, 3) + dt.timedelta(days=int(rng.integers(0, 600)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            rows.append(dict(completed=d, location_type='SERVICE', location_id=p.pid, action='TEST',
                             old_meter_id='%02d-%06d' % (int(rng.integers(8, 20)), int(rng.integers(30000, 290000))),
                             old_final_read='', old_register_unit='', new_meter_id='', new_initial_read='',
                             new_register_unit='', technician=techs[int(rng.integers(len(techs)))],
                             notes='low flow %.1f%%, intermediate %.1f%%, high %.1f%%' % (
                                 float(rng.uniform(91, 100.5)), float(rng.uniform(97, 101)), float(rng.uniform(98, 101.5)))))
    for s in fac_swaps:
        rows.append(dict(completed=s['date'], location_type='CITY FACILITY', location_id=s['fid'], action='REPLACE',
                         old_meter_id=s['old'], old_final_read=s['old_final'], old_register_unit=s['old_unit'],
                         new_meter_id=s['new'], new_initial_read=s['new_init'], new_register_unit=s['new_unit'],
                         technician='T. Bryant' if s['fid'] == 'GC-MUNI' else 'S. Clay',
                         notes='3-inch turbine, old PD meter to bench test' if s['fid'] == 'GC-MUNI' else 'register sticking'))
    rows.sort(key=lambda r: (r['completed'], r['location_type'], r['location_id']))
    n = 25000 + int(rng.integers(100, 900))
    for r in rows:
        n += int(rng.integers(1, 6))
        r['work_order'] = 'WO%d-%05d' % (r['completed'].year % 100, n)
    return rows


WO_COLS = ['work_order', 'completed', 'location_type', 'location_id', 'action', 'old_meter_id', 'old_final_read',
           'old_register_unit', 'new_meter_id', 'new_initial_read', 'new_register_unit', 'technician', 'notes']
