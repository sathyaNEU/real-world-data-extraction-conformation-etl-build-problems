"""Writes target/: the council's and the public health service's own exports, from the clean truth.

Every record is cut from world.simulate(seed) plus per-file random streams, so two runs are byte-identical.
"""
import csv
import datetime as dt
import io
import json
import os
import zipfile

import numpy as np

import world

D0 = world.D0
EXPORT = dt.datetime(2027, 10, 19, 7, 40)
ZIP_DT = (2027, 10, 19, 7, 40, 0)
DST = dt.date(2027, 9, 26)          # NZDT from 02:00 on Sunday 26 September 2027

ZNAME = {'Z01': 'Northbrook', 'Z02': 'Kahikatea Heights', 'Z03': 'Harbourside', 'Z04': 'Millbank', 'Z05': 'Ferndale',
         'Z06': 'Glenholme', 'Z07': 'Tui Park', 'Z08': 'Riverbend', 'Z09': 'Southgate', 'Z10': 'Totara Downs',
         'Z11': 'Kowhai Hills', 'Z12': 'Matai Valley', 'Z13': 'Rimu Flat', 'Z14': 'Pohutukawa Point',
         'Z15': 'Ngaio Rise', 'Z16': 'Eastfield'}
# supply-zone codes as reissued on 16 August 2027; two zones renumbered (old codes retired)
ZCODE = {'Z01': 'SZ14', 'Z02': 'SZ03', 'Z03': 'SZ22', 'Z04': 'SZ07', 'Z05': 'SZ11', 'Z06': 'SZ18', 'Z07': 'SZ05',
         'Z08': 'SZ26', 'Z09': 'SZ09', 'Z10': 'SZ31', 'Z11': 'SZ16', 'Z12': 'SZ24', 'Z13': 'SZ12', 'Z14': 'SZ29',
         'Z15': 'SZ20', 'Z16': 'SZ02'}
ZCODE_OLD = {'Z10': 'SZ13', 'Z15': 'SZ28'}
RNAME = {'R1': 'Hillcrest Reservoir', 'R2': 'Ferndale Road Reservoir', 'R3': 'Riverbend Reservoir',
         'R4': 'Kowhai Hills Reservoir', 'R5': 'Southgate Reservoir', 'R6': 'Eastfield Reservoir'}
RNODE = {'R1': 'RES-HIL', 'R2': 'RES-FDR', 'R3': 'RES-RVB', 'R4': 'RES-KWH', 'R5': 'RES-STH', 'R6': 'RES-EFD'}
TOWN = 'Kotare'
OTHER_TOWNS = ['Christchurch', 'Dunedin', 'Auckland', 'Wellington', 'Timaru', 'Nelson', 'Invercargill', 'Hamilton',
               'Sydney', 'Melbourne', 'Brisbane']

STREETS = ['Kowhai Road', 'Matai Street', 'Rimu Avenue', 'Totara Crescent', 'Ngaio Place', 'Puriri Street',
           'Harbour View Road', 'Mill Road', 'Fern Grove', 'Glen Road', 'Tui Street', 'River Road', 'South Road',
           'Downs Road', 'Point Road', 'East Street', 'Hill Street', 'Station Road', 'Church Street', 'School Road',
           'Beach Road', 'Domain Road', 'Park Avenue', 'Rata Street', 'Miro Place', 'Kauri Drive', 'Manuka Lane',
           'Pukeko Way', 'Weka Street', 'Kereru Close', 'Harakeke Street', 'Raupo Road', 'Totara Street',
           'Kahikatea Drive', 'Northbrook Road', 'Ferndale Avenue', 'Valley Road', 'Flat Road', 'Rise Road',
           'Eastfield Road', 'Bridge Street', 'Wharf Street', 'Queen Street', 'King Street', 'Victoria Avenue',
           'Albert Street', 'Gordon Road', 'Russell Street', 'Ward Street', 'Clyde Street']


STEMS = ['Kowhai', 'Matai', 'Rimu', 'Totara', 'Ngaio', 'Puriri', 'Rata', 'Miro', 'Kauri', 'Manuka', 'Kanuka', 'Karaka',
         'Titoki', 'Tawa', 'Hinau', 'Kahikatea', 'Horoeka', 'Mahoe', 'Karamu', 'Akeake', 'Tarata', 'Houhere', 'Pukeko',
         'Weka', 'Kereru', 'Tui', 'Korimako', 'Kaka', 'Kea', 'Ruru', 'Piwakawaka', 'Toroa', 'Kotuku', 'Harakeke', 'Raupo',
         'Toetoe', 'Raumati', 'Hillcrest', 'Ferndale', 'Millbank', 'Glenholme', 'Riverbend', 'Southgate', 'Northbrook',
         'Harbour', 'Station', 'Church', 'School', 'Beach', 'Domain', 'Park', 'Bridge', 'Wharf', 'Queen', 'King',
         'Victoria', 'Albert', 'Gordon', 'Russell', 'Ward', 'Clyde', 'Ayr', 'Tweed', 'Tay', 'Dee', 'Esk', 'Forth', 'Severn',
         'Avon', 'Brunner', 'Rutherford', 'Seddon', 'Ballance', 'Grey', 'Fox', 'Vogel', 'Stout', 'Atkinson', 'Massey',
         'Coates', 'Sheppard', 'Batten', 'Hillary', 'Upham', 'Mackenzie', 'Cargill', 'Selwyn', 'Hobson', 'Fitzroy',
         'Wakefield', 'Tasman', 'Cook', 'Banks', 'Marsden', 'Kendall', 'Busby', 'Williams', 'Hadfield', 'Harper',
         'Thorndon', 'Kelburn', 'Brooklyn', 'Mornington', 'Roslyn', 'Maori Hill', 'Caversham', 'Opoho', 'Wakari',
         'Fairfield', 'Highgate', 'Glenpark', 'Larch', 'Rowan', 'Alder', 'Linden', 'Elm', 'Ash', 'Beech', 'Poplar',
         'Willow', 'Hazel', 'Chestnut', 'Oak', 'Maple', 'Cedar', 'Laurel', 'Holly', 'Wattle', 'Acacia', 'Jacaranda']
SUFFIXES = ['Road', 'Street', 'Avenue', 'Crescent', 'Place', 'Drive', 'Lane', 'Terrace', 'Grove', 'Close', 'Way',
            'Rise', 'Court', 'Parade']


SUB = {'lab': 1, 'crm': 4, 'callouts': 13}      # per-ask stream offsets, fixed after the mid-bin search


def rng_for(seed, name):
    h = int.from_bytes(name.encode(), 'little') % 1_000_003
    sub = SUB.get(name.split('-')[0], 0)
    return np.random.default_rng([seed, h, sub] if sub else [seed, h])


def day(d):
    return D0 + dt.timedelta(days=int(d))


DST_LOCAL = dt.datetime(2027, 9, 26, 2, 0)     # clocks go forward to 03:00 NZDT


def offset_for(t):
    return '+13:00' if t >= DST_LOCAL else '+12:00'


def iso_local(t):
    return t.strftime('%Y-%m-%dT%H:%M:%S') + offset_for(t)


def to_utc(t):
    return t - dt.timedelta(hours=13 if t >= DST_LOCAL else 12)


def uniq_ints(rng, n, lo, hi):
    out = rng.choice(np.arange(lo, hi), size=n, replace=False)
    return [int(x) for x in out]


# ---------------------------------------------------------------- network model
def network(seed):
    rng = rng_for(seed, 'network')
    trunk = {}
    ids = iter(uniq_ints(rng, 2000, 10000, 99999))
    tags = iter(uniq_ints(rng, 3000, 1000, 9999))
    for z, (parent, link, *_r) in world.ZONES.items():
        frm = RNODE[parent] if parent in world.RES else ZCODE[parent] + '-INLET'
        trunk[link] = dict(main_id='WM%05d' % next(ids), cls='Trunk', frm=frm, to=ZCODE[z] + '-INLET', zone=ZCODE[z],
                           dia=int(rng.choice([225, 250, 300, 375])), mat=str(rng.choice(['DI', 'PVC-O', 'AC', 'PE100'])),
                           year=int(rng.integers(1962, 2016)), length=int(rng.integers(900, 4200)))
    for k, (a, b) in world.ICS.items():
        trunk[k] = dict(main_id='WM%05d' % next(ids), cls='Boundary', frm=ZCODE[a] + '-INLET', to=ZCODE[b] + '-INLET',
                        zone='', dia=int(rng.choice([150, 180, 200, 250])), mat=str(rng.choice(['PVC', 'AC', 'DI'])),
                        year=int(rng.integers(1971, 2012)), length=int(rng.integers(300, 2600)))
    mains = []
    for k, m in trunk.items():
        mains.append(dict(m, key=k))
    for z in world.ZONES:
        n = int(rng.integers(18, 42))
        nodes = ['N%05d' % next(ids) for _ in range(n + 1)]
        for i in range(n):
            mains.append(dict(main_id='WM%05d' % next(ids), cls='Distribution', frm=nodes[int(rng.integers(0, i + 1))] if i else ZCODE[z] + '-INLET',
                              to=nodes[i + 1], zone=ZCODE[z], dia=int(rng.choice([50, 63, 100, 100, 150, 150])),
                              mat=str(rng.choice(['PVC', 'PE', 'AC', 'CI', 'DI'])), year=int(rng.integers(1955, 2024)),
                              length=int(rng.integers(40, 640)), key=None))
    valves = []
    for m in mains:
        street = STREETS[int(rng.integers(len(STREETS)))]
        if m['cls'] == 'Trunk':
            for _ in range(2):
                valves.append(dict(valve_id='VA%05d' % next(ids), tag='KV%04d' % next(tags), main_id=m['main_id'],
                                   vtype='Isolation', normal='Open', street=street, key=m['key']))
            if rng.random() < 0.5:
                valves.append(dict(valve_id='VA%05d' % next(ids), tag='KV%04d' % next(tags), main_id=m['main_id'],
                                   vtype='Air release', normal='Open', street=street, key=None))
        elif m['cls'] == 'Boundary':
            valves.append(dict(valve_id='VA%05d' % next(ids), tag='KV%04d' % next(tags), main_id=m['main_id'],
                               vtype='Boundary', normal='Closed', street=street, key=m['key']))
            valves.append(dict(valve_id='VA%05d' % next(ids), tag='KV%04d' % next(tags), main_id=m['main_id'],
                               vtype='Air release', normal='Open', street=street, key=None))
        else:
            for _ in range(int(rng.choice([1, 1, 2, 2, 3]))):
                valves.append(dict(valve_id='VA%05d' % next(ids), tag='KV%04d' % next(tags), main_id=m['main_id'],
                                   vtype=str(rng.choice(['Isolation', 'Isolation', 'Isolation', 'Scour', 'Air release'])),
                                   normal='Open', street=street, key=None))
    order = rng.permutation(len(mains))
    mains = [mains[i] for i in order]
    vorder = rng.permutation(len(valves))
    valves = [valves[i] for i in vorder]
    return trunk, mains, valves


# ---------------------------------------------------------------- operations
def operations(seed, W, trunk, valves):
    """Valve operations log (local time with offset, field tags) and the work orders behind the repairs."""
    rng = rng_for(seed, 'operations')
    iso = {}
    bnd = {}
    for v in valves:
        if v['key'] and v['vtype'] == 'Isolation':
            iso.setdefault(v['key'], []).append(v)
        if v['key'] and v['vtype'] == 'Boundary':
            bnd[v['key']] = v
    ops = []
    wos = []
    wo_ids = iter(uniq_ints(rng, 4000, 4400000, 4799999))
    for m, f, l, bf in W['reps']:
        start = dt.datetime.combine(day(f), dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 130)))
        end = dt.datetime.combine(day(l), dt.time(13, 30)) + dt.timedelta(minutes=int(rng.integers(0, 180)))
        wo = next(wo_ids)
        crew = str(rng.choice(['Network A', 'Network B', 'Network C', 'Contractor - Rata Civil']))
        isov = iso[m]
        t = start
        for v in isov:
            ops.append((t, v['tag'], 'Close', crew, 'WO%d' % wo))
            t += dt.timedelta(minutes=int(rng.integers(4, 15)))
        if bf:
            ops.append((t + dt.timedelta(minutes=int(rng.integers(3, 20))), bnd[bf]['tag'], 'Open', crew, 'WO%d' % wo))
        t = end
        if bf:
            ops.append((t, bnd[bf]['tag'], 'Close', crew, 'WO%d' % wo))
            t += dt.timedelta(minutes=int(rng.integers(5, 25)))
        for v in isov[::-1]:
            ops.append((t, v['tag'], 'Open', crew, 'WO%d' % wo))
            t += dt.timedelta(minutes=int(rng.integers(4, 15)))
        wos.append(dict(wo='WO%d' % wo, wtype='Reactive - main repair', main=trunk[m]['main_id'], street=isov[0]['street'],
                        start=start, finish=end + dt.timedelta(minutes=int(rng.integers(20, 90))), crew=crew))
    # routine valve exercising and flushing on distribution valves (no supply change)
    dist = [v for v in valves if not v['key'] and v['vtype'] in ('Isolation', 'Scour')]
    n_ex = int(rng.integers(1300, 1500))
    for _ in range(n_ex):
        v = dist[int(rng.integers(len(dist)))]
        d = int(rng.integers(0, world.NDAYS))
        if day(d).weekday() >= 5:
            continue
        t = dt.datetime.combine(day(d), dt.time(7, 30)) + dt.timedelta(minutes=int(rng.integers(0, 540)))
        crew = str(rng.choice(['Valve programme', 'Valve programme', 'Network A', 'Network C']))
        if v['vtype'] == 'Scour':
            ops.append((t, v['tag'], 'Open', crew, ''))
            ops.append((t + dt.timedelta(minutes=int(rng.integers(8, 45))), v['tag'], 'Close', crew, ''))
        else:
            ops.append((t, v['tag'], 'Exercise', crew, ''))
    ops.sort(key=lambda r: (r[0], r[1]))
    return ops, wos


def renewal_plan(seed, trunk, valves):
    """Planned operations for the FM11 renewal, 26 October to 6 November 2027."""
    iso = [v for v in valves if v['key'] == 'FM11' and v['vtype'] == 'Isolation']
    iso12 = [v for v in valves if v['key'] == 'LM12' and v['vtype'] == 'Isolation']
    bm = [v for v in valves if v['key'] == world.BAD and v['vtype'] == 'Boundary'][0]
    bm7 = [v for v in valves if v['key'] == 'BM7' and v['vtype'] == 'Boundary'][0]
    a = dt.datetime(2027, 10, 26, 8, 30)
    b = dt.datetime(2027, 11, 6, 15, 0)
    m = dt.timedelta(minutes=1)
    rows = [(a, iso12[0]['tag'], 'Close'), (a + 6 * m, iso12[1]['tag'], 'Close'), (a + 14 * m, bm7['tag'], 'Open'),
            (a + 35 * m, iso[0]['tag'], 'Close'), (a + 44 * m, iso[1]['tag'], 'Close'), (a + 58 * m, bm['tag'], 'Open'),
            (b, bm['tag'], 'Close'), (b + 12 * m, iso[1]['tag'], 'Open'), (b + 21 * m, iso[0]['tag'], 'Open'),
            (b + 40 * m, bm7['tag'], 'Close'), (b + 47 * m, iso12[1]['tag'], 'Open'), (b + 55 * m, iso12[0]['tag'], 'Open')]
    return rows


# ---------------------------------------------------------------- census and register
def census(seed):
    rng = rng_for(seed, 'census')
    res = world.residents()
    mb = []
    codes = iter(uniq_ints(rng, 600, 2610000, 2899999))
    for z in world.ZONES:
        n = int(rng.integers(9, 24))
        w = rng.dirichlet(np.full(n, 3.0))
        pops = np.maximum(3, np.round(res[z] * w / 3.0) * 3).astype(int)
        for p in pops:
            mb.append(dict(mb='%07d' % next(codes), zone=z, pop=int(p)))
    order = rng.permutation(len(mb))
    return [mb[i] for i in order]


def register(seed, mbs):
    """Rating database export: networked connections by zone, plus rural-scheme and private-supply properties."""
    rng = rng_for(seed, 'register')
    vals = iter(uniq_ints(rng, 90000, 100000, 999999))
    by_zone = {}
    for m in mbs:
        by_zone.setdefault(m['zone'], []).append(m)
    rows = []
    zone_streets = {}
    pool = [s + ' ' + x for s in STEMS for x in SUFFIXES]
    pool = [pool[i] for i in rng.permutation(len(pool))]
    cursor = 0
    for z, (_, _, props, *_r) in world.ZONES.items():
        k = max(8, props // 68 + int(rng.integers(-4, 5)))
        zone_streets[z] = pool[cursor:cursor + k]
        cursor += k
    for z, (_, _, props, *_r) in world.ZONES.items():
        mlist = by_zone[z]
        mw = np.array([m['pop'] for m in mlist], float)
        mw = mw / mw.sum()
        streets = zone_streets[z]
        counts = rng.multinomial(props, rng.dirichlet(np.full(len(streets), 2.0)))
        addresses = []
        for st, c in zip(streets, counts):
            if c:
                nums = rng.choice(np.arange(1, 2 * c + 12), size=int(c), replace=False)
                addresses += ['%d %s' % (int(n), st) for n in sorted(nums)]
        for a_ in addresses:
            st, num = a_.split(' ', 1)[1], int(a_.split(' ', 1)[0])
            cat = str(rng.choice(['Residential'] * 17 + ['Commercial', 'Lifestyle', 'Community']))
            new = None
            if z == 'Z15' and rng.random() < 0.09:
                new = dt.date(2027, 10, 14)
            elif rng.random() < 0.004:
                new = day(int(rng.integers(0, world.NDAYS)))
            rows.append(dict(valuation='%05d/%03d.%02d' % (next(vals) // 10, int(rng.integers(1, 999)), int(rng.choice([0, 0, 0, 10, 20]))),
                             address='%d %s' % (num, st), suburb=ZNAME[z], supply='Networked', zone=ZCODE[z],
                             connection='WC%06d' % next(vals), connected=new, category=cat,
                             mb=mlist[int(rng.choice(len(mlist), p=mw))]['mb'], zkey=z))
    # rural scheme and private supplies: never in a supply zone
    for _ in range(int(rng.integers(1150, 1350))):
        sup = str(rng.choice(['Restricted rural scheme', 'Restricted rural scheme', 'Private bore', 'Rainwater tank']))
        rd = int(rng.integers(1, 7))
        road = str(rng.choice(['Settlement Road', 'Gorge Road', 'Back Road', 'Valley Road', 'Hill Road', 'Ridge Road',
                               'Old Coach Road', 'Swamp Road', 'Flaxmill Road']))
        rows.append(dict(valuation='%05d/%03d.%02d' % (next(vals) // 10, int(rng.integers(1, 999)), 0),
                         address='%d %s' % (int(rng.integers(100, 3800)), road), suburb='RD %d' % rd, supply=sup,
                         zone='', connection='WC%06d' % next(vals) if sup.startswith('Restricted') else '',
                         connected=None, category=str(rng.choice(['Lifestyle', 'Rural', 'Rural', 'Residential'])),
                         mb='', zkey=None))
    order = rng.permutation(len(rows))
    return [rows[i] for i in order], zone_streets


# ---------------------------------------------------------------- people
def faker_for(seed, name):
    from faker import Faker
    f = Faker('en_NZ')
    f.seed_instance(int(rng_for(seed, name).integers(1, 2 ** 31)))
    return f


def nhi(rng, new=False):
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    s = ''.join(letters[int(rng.integers(len(letters)))] for _ in range(3))
    if new:
        return s + '%02d' % int(rng.integers(0, 100)) + ''.join(letters[int(rng.integers(len(letters)))] for _ in range(2))
    return s + '%04d' % int(rng.integers(0, 10000))


def age_dob(rng, ref):
    a = float(rng.choice([rng.uniform(0.5, 5), rng.uniform(5, 15), rng.uniform(15, 45), rng.uniform(45, 85)],
                         p=[0.27, 0.13, 0.42, 0.18]))
    return ref - dt.timedelta(days=int(a * 365.25 + rng.integers(0, 365)))


def cases(seed, W, reg):
    """The public health service's line list: confirmed and probable cases, residents and visitors."""
    rng = rng_for(seed, 'cases')
    fk = faker_for(seed, 'cases-names')
    props = {}
    for r in reg:
        if r['zkey']:
            props.setdefault(r['zkey'], []).append(r)
    out = []
    ids = iter(uniq_ints(rng, 3000, 210000, 289999))
    for c in sorted(W['cases'], key=lambda c: (c['report'], c['zone'], c['onset'])):
        p = props[c['zone']][int(rng.integers(len(props[c['zone']])))]
        onset = day(c['onset'])
        spec = onset + dt.timedelta(days=int(rng.integers(1, 6)))
        rep = day(c['report'])
        if spec > rep:
            spec = rep
        tap = int(rng.choice([0, 1, 2, 3, 4, 5, 6, 8], p=[.05, .1, .17, .2, .18, .13, .1, .07])) if c['kind'] == 'outbreak' \
            else int(rng.choice([0, 1, 2, 3, 4, 5, 6, 8], p=[.12, .18, .2, .2, .13, .09, .05, .03]))
        out.append(dict(case='EPI%d' % next(ids), nhi=nhi(rng, rng.random() < 0.3), surname=fk.last_name(),
                        given=fk.first_name(), dob=age_dob(rng, onset), sex=str(rng.choice(['F', 'M'])),
                        address=p['address'], suburb=p['suburb'], mb=p['mb'], onset=onset, specimen=spec, report=rep,
                        status='Confirmed', hosp='Y' if rng.random() < 0.09 else 'N', tap=tap,
                        pool='Y' if rng.random() < 0.14 else 'N', animal='Y' if rng.random() < (0.22 if c['kind'] == 'background' else 0.08) else 'N',
                        childcare='Y' if rng.random() < 0.08 else 'N', travel='Y' if rng.random() < (0.12 if c['kind'] == 'background' else 0.02) else 'N',
                        kind=c['kind'], zkey=c['zone']))
    # probable cases (household members epidemiologically linked, no specimen) and visitors notified here
    conf = [o for o in out if o['onset'] >= dt.date(2027, 9, 1)]
    for o in list(conf):
        if rng.random() < 0.22:
            onset = o['onset'] + dt.timedelta(days=int(rng.integers(-2, 6)))
            rep = max(o['report'], onset + dt.timedelta(days=int(rng.integers(2, 7))))
            if rep >= world.SETTING:
                continue
            out.append(dict(o, case='EPI%d' % next(ids), nhi=nhi(rng), given=fk.first_name(), dob=age_dob(rng, onset),
                            sex=str(rng.choice(['F', 'M'])), onset=onset, specimen=None, report=rep, status='Probable',
                            hosp='N', kind='probable'))
    for _ in range(int(rng.integers(5, 10))):
        d = int(rng.integers(55, world.NDAYS - 6))
        onset = day(d)
        rep = onset + dt.timedelta(days=int(rng.integers(3, 8)))
        if rep >= world.SETTING:
            continue
        town = OTHER_TOWNS[int(rng.integers(len(OTHER_TOWNS)))]
        out.append(dict(case='EPI%d' % next(ids), nhi=nhi(rng), surname=fk.last_name(), given=fk.first_name(),
                        dob=age_dob(rng, onset), sex=str(rng.choice(['F', 'M'])),
                        address='%d %s' % (int(rng.integers(1, 300)), STREETS[int(rng.integers(len(STREETS)))]),
                        suburb=town, mb='', onset=onset, specimen=onset + dt.timedelta(days=2), report=rep,
                        status='Confirmed', hosp='N', tap=int(rng.integers(0, 4)), pool='N', animal='N', childcare='N',
                        travel='N', kind='visitor', zkey=None))
    out.sort(key=lambda o: (o['report'], o['case']))
    return out


# ---------------------------------------------------------------- ask 1: laboratory
MONTHS = [(dt.date(2027, 7, 1), dt.date(2027, 7, 31), 'July'), (dt.date(2027, 8, 1), dt.date(2027, 8, 31), 'August'),
          (dt.date(2027, 9, 1), dt.date(2027, 9, 30), 'September'), (dt.date(2027, 10, 1), dt.date(2027, 10, 17), '1-17 October')]


def laboratory(seed, case_rows, reg):
    """Community laboratory faecal parasite results and the reference laboratory's typing report."""
    rng = rng_for(seed, 'lab')
    fk = faker_for(seed, 'lab-names')
    addr = [r for r in reg if r['zkey']]
    specimens = []
    persons = []
    acc = iter(uniq_ints(rng, 40000, 100000, 999999))
    # people with confirmed notifications have their positive specimens here
    for c in case_rows:
        if c['status'] != 'Confirmed' or c['specimen'] is None:
            continue
        persons.append(dict(nhi=c['nhi'], surname=c['surname'], given=c['given'], dob=c['dob'], sex=c['sex'],
                            address=c['address'], town=TOWN if c['zkey'] else c['suburb'], resident=bool(c['zkey']),
                            pos_date=c['specimen'], species='C. parvum' if c['kind'] == 'outbreak' else
                            ('C. hominis' if c['travel'] == 'Y' else str(rng.choice(['C. parvum', 'C. hominis'], p=[0.7, 0.3]))),
                            dormant=None))
    # visitors tested positive here and referred (never residents)
    for _ in range(int(rng.integers(5, 9))):
        cd = dt.date(2027, 7, 1) + dt.timedelta(days=int(rng.integers(0, 108)))
        persons.append(dict(nhi=nhi(rng, rng.random() < 0.3), surname=fk.last_name(), given=fk.first_name(),
                            dob=age_dob(rng, cd), sex=str(rng.choice(['F', 'M'])),
                            address='%d %s' % (int(rng.integers(1, 300)), STREETS[int(rng.integers(len(STREETS)))]),
                            town=OTHER_TOWNS[int(rng.integers(len(OTHER_TOWNS)))], resident=False, pos_date=cd,
                            species=str(rng.choice(['C. parvum', 'C. hominis'])), dormant=None))
    # people tested negative, by month, with a September and October rise
    base = {7: 118, 8: 126, 9: 151, 10: 133}
    for (a, b, _), mo in zip(MONTHS, (7, 8, 9, 10)):
        n = int(rng.poisson(base[mo]))
        for _ in range(n):
            res = rng.random() > 0.07
            p = addr[int(rng.integers(len(addr)))]
            persons.append(dict(nhi=nhi(rng, rng.random() < 0.3), surname=fk.last_name(), given=fk.first_name(),
                                dob=age_dob(rng, a), sex=str(rng.choice(['F', 'M'])), address=p['address'] if res else
                                '%d %s' % (int(rng.integers(1, 300)), STREETS[int(rng.integers(len(STREETS)))]),
                                town=TOWN if res else OTHER_TOWNS[int(rng.integers(len(OTHER_TOWNS)))], resident=res,
                                pos_date=None, test_date=a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1))),
                                species=None, dormant=None))
    # device D7: some repeat testers carry a dormant NHI on one specimen
    for p in persons:
        if p['pos_date'] is None and p['resident'] and rng.random() < 0.075:
            p['dormant'] = nhi(rng, True)
    rows = []
    practices = ['Kotare Medical Centre', 'Harbourside Health', 'Millbank Family Doctors', 'Tui Park Medical',
                 'Eastfield Health Centre', 'Riverbend GP', 'Kotare Hospital ED', 'Southgate Medical']
    for p in persons:
        if p['pos_date'] is not None:
            dates = [p['pos_date']]
            if rng.random() < 0.3:
                dates = sorted({dates[0], min(p['pos_date'] + dt.timedelta(days=int(rng.integers(1, 4))), dt.date(2027, 10, 18))})
        else:
            k = int(rng.choice([1, 1, 1, 2, 2, 3])) if p['dormant'] is None else int(rng.choice([2, 2, 3]))
            dates = sorted({min(p['test_date'] + dt.timedelta(days=int(rng.integers(0, 4)) * i), dt.date(2027, 10, 17)) for i in range(k)})
            if p['dormant'] is not None and len(dates) < 2:
                dates.append(min(dates[0] + dt.timedelta(days=1), dt.date(2027, 10, 17)))
                dates = sorted(set(dates))
        for i, cd in enumerate(dates):
            recv = dt.datetime.combine(cd, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(0, 600)))
            if p['pos_date'] is not None and i == 0:
                result = 'Cryptosporidium antigen DETECTED. Referred to reference laboratory for confirmation and typing.'
            else:
                result = str(rng.choice(['No Cryptosporidium or Giardia antigen detected.'] * 14 +
                                        ['Giardia antigen DETECTED. Cryptosporidium antigen not detected.']))
            use_dormant = p['dormant'] is not None and i == len(dates) - 1
            acc_s = 'C%02d%06d' % (cd.month, next(acc))
            requester = practices[int(rng.integers(len(practices)))]
            rep = recv + dt.timedelta(hours=int(rng.integers(20, 70)))
            cap = EXPORT - dt.timedelta(minutes=95)
            if rep > cap:
                # reported before the export: somewhere between receipt and the export, never one batch time
                rep = recv + dt.timedelta(minutes=int((cap - recv).total_seconds() / 60 * (0.3 + 0.65 * int(acc_s[-3:]) / 1000)))
            rows.append(dict(acc=acc_s, nhi=p['dormant'] if use_dormant else p['nhi'],
                             surname=p['surname'].upper(), given=p['given'], dob=p['dob'], sex=p['sex'],
                             address=p['address'], town=p['town'], requester=requester,
                             collected=cd, received=recv, result=result, reported=rep, person=p, first=(i == 0)))
    # a few amended reports re-issued with the same accession
    am = [r for r in rows if r['result'].startswith('No ') and rng.random() < 0.012]
    for r in am:
        rows.append(dict(r, reported=min(r['reported'] + dt.timedelta(days=1), EXPORT - dt.timedelta(minutes=50)), amended=True))
    rows.sort(key=lambda r: (r['received'], r['acc']))
    # reference laboratory typing report: referred antigen positives typed by 18 October
    ref = []
    racc = iter(uniq_ints(rng, 5000, 1000, 9999))
    for r in rows:
        p = r['person']
        if p['pos_date'] is None or not r['first'] or r.get('amended'):
            continue
        typed = r['collected'] + dt.timedelta(days=int(rng.integers(3, 10)))
        if typed >= world.SETTING:
            continue
        num = r['acc'][1:]
        fmt = int(rng.integers(0, 5))
        refs = ['C' + num, num, 'C ' + num, 'Your ref C' + num, 'CL' + num][fmt]
        conf = rng.random() > 0.05
        rcvd = min(r['collected'] + dt.timedelta(days=int(rng.integers(2, 5))), typed - dt.timedelta(days=1))
        ref.append(dict(racc='RL27-%04d' % next(racc), referrer='Kotare Community Laboratory', refs=refs,
                        name='%s, %s' % (p['surname'].upper(), p['given']), dob=p['dob'],
                        nhi=p['nhi'] if rng.random() < 0.55 else '',
                        collected=r['collected'] if rng.random() < 0.7 else rcvd, received=rcvd,
                        result=('Cryptosporidium parvum' if p['species'] == 'C. parvum' else 'Cryptosporidium hominis') if conf
                        else 'Cryptosporidium not detected by PCR (antigen result not confirmed)',
                        gp60=('IIaA15G2R1' if p['species'] == 'C. parvum' else 'IbA10G2') if conf else '',
                        reported=typed, person=p, true_collected=r['collected']))
    ref.sort(key=lambda x: (x['reported'], x['racc']))
    return rows, ref


# ---------------------------------------------------------------- ask 2: complaints
CATS = ['Clarity', 'Taste', 'Odour', 'Pressure or flow', 'Continuity of supply']
PERIODS = [(dt.date(2027, 7, 1), dt.date(2027, 9, 30), 'July to September')]
OUTAGES = [(dt.date(2027, 8, 16), dt.date(2027, 9, 3)), (dt.date(2027, 10, 4), dt.date(2027, 10, 13))]


def complaints(seed, reg):
    rng = rng_for(seed, 'crm')
    fk = faker_for(seed, 'crm-names')
    net = [r for r in reg if r['supply'] == 'Networked']
    rural = [r for r in reg if r['supply'] != 'Networked']
    crm = []
    web = []
    cid = iter(uniq_ints(rng, 20000, 1000000, 9999999))
    wid = iter(uniq_ints(rng, 5000, 10000, 99999))
    descs = {'Clarity': ['Brown water from kitchen tap', 'Discoloured water this morning', 'Water cloudy and dirty',
                         'Dirty water in bath', 'Rusty colour in water'],
             'Taste': ['Water tastes of chlorine', 'Metallic taste', 'Strange taste in drinking water', 'Tastes earthy'],
             'Odour': ['Water smells of chlorine', 'Musty smell from tap', 'Smell like rotten eggs', 'Odd smell in water'],
             'Pressure or flow': ['Very low pressure', 'Pressure dropping in evenings', 'Poor flow at shower', 'Low flow'],
             'Continuity of supply': ['No water at property', 'Water off without notice', 'Supply cut out', 'No water since 6am']}
    other = ['Billing query', 'Leak in berm', 'Meter reading query', 'Toby lid broken', 'Hydrant leaking']

    def addr_variant(a):
        r = rng.random()
        if r < 0.4:
            return a
        num, rest = a.split(' ', 1)
        rest2 = rest.replace(' Road', ' Rd').replace(' Street', ' St').replace(' Avenue', ' Ave').replace(' Crescent', ' Cres')
        if r < 0.8:
            return num + ' ' + rest2
        if r < 0.92:
            return 'Flat %d/%s %s' % (int(rng.integers(1, 6)), num, rest)
        return (num + ' ' + rest).lower()

    def add(t, cat, prop, channel, desc, vref=True):
        crm.append(dict(cid='CRM-%07d' % next(cid), received=t, channel=channel, category='Water - ' + cat if cat in CATS else cat,
                        desc=desc, address=addr_variant(prop['address']) + (', ' + prop['suburb'] if rng.random() < 0.7 else ''),
                        vref=prop['valuation'] if vref else '', status=str(rng.choice(['Closed', 'Closed', 'Closed', 'Resolved'])),
                        prop=prop, cat=cat, rekey_of=None))

    for d in range(world.NDAYS - 1):
        date = day(d)
        f = 1.0 if date < dt.date(2027, 10, 1) else 2.3
        for cat, lam in (('Clarity', 0.55), ('Taste', 0.22), ('Odour', 0.18), ('Pressure or flow', 0.42), ('Continuity of supply', 0.30)):
            n = int(rng.poisson(lam * f))
            for _ in range(n):
                t = dt.datetime.combine(date, dt.time(7, 0)) + dt.timedelta(minutes=int(rng.integers(0, 840)))
                rur = cat in ('Pressure or flow', 'Continuity of supply') and rng.random() < 0.38
                prop = (rural if rur else net)[int(rng.integers(len(rural if rur else net)))]
                web_ok = cat in ('Clarity', 'Taste', 'Odour') and rng.random() < 0.42
                in_outage = any(a <= date <= b for a, b in OUTAGES)
                if web_ok:
                    w = dict(wid='WF%05d' % next(wid), submitted=t, name=fk.name(), email='', address=prop['address'] + ', ' + prop['suburb'],
                             issue={'Clarity': 'Discoloured water', 'Taste': 'Taste', 'Odour': 'Smell'}[cat],
                             details=descs[cat][int(rng.integers(len(descs[cat])))], crm='', prop=prop, cat=cat)
                    if not in_outage:
                        add(t + dt.timedelta(minutes=int(rng.integers(1, 6))), cat, prop, 'Web form', w['details'], vref=rng.random() < 0.8)
                        w['crm'] = crm[-1]['cid']
                    elif rng.random() < 0.66:
                        # re-keyed by hand after the integration came back: a new contact days later, not an exact copy
                        lag = dt.timedelta(days=int(rng.integers(1, 6)), minutes=int(rng.integers(0, 400)))
                        add(t + lag, cat, prop, str(rng.choice(['Email', 'Phone'])), w['details'], vref=rng.random() < 0.6)
                        crm[-1]['rekey_of'] = w['wid']
                    web.append(w)
                else:
                    ch = str(rng.choice(['Phone', 'Phone', 'Phone', 'Email', 'After-hours', 'Counter']))
                    add(t, cat, prop, ch, descs[cat][int(rng.integers(len(descs[cat])))], vref=rng.random() < 0.5)
        for _ in range(int(rng.poisson(2.2))):
            t = dt.datetime.combine(date, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(0, 540)))
            prop = net[int(rng.integers(len(net)))]
            add(t, other[int(rng.integers(len(other)))], prop, 'Phone', 'Customer called', vref=rng.random() < 0.8)
    crm.sort(key=lambda r: (r['received'], r['cid']))
    web.sort(key=lambda r: (r['submitted'], r['wid']))
    return crm, web


# ---------------------------------------------------------------- ask 3: call-outs
def callouts(seed, wos_repairs, reg):
    rng = rng_for(seed, 'callouts')
    net = [r for r in reg if r['supply'] == 'Networked']
    srs, jobs, ah, wos = [], [], [], []
    sid = iter(uniq_ints(rng, 20000, 1000000, 9999999))
    jid = iter(uniq_ints(rng, 20000, 300000, 699999))
    aid = iter(uniq_ints(rng, 5000, 100000, 999999))
    woid = iter(uniq_ints(rng, 5000, 4800000, 4999999))
    probs_u = ['Burst main', 'No water', 'Burst main', 'Leak - main (major)']
    probs_n = ['Leak - service line', 'Low pressure', 'Toby/valve repair', 'Meter leaking', 'Hydrant damaged', 'Leak - berm']
    planned = []

    def street_of(prop):
        return prop['address'].split(' ', 1)[1]

    def planned_on(street, after):
        """The street's next planned maintenance after a time, created when none is booked within 14 days."""
        for p in planned:
            if p['street'] == street and abs((p['start'] - after).days) < 14:
                return p if p['start'] > after + dt.timedelta(hours=20) else None
        sd = after.date() + dt.timedelta(days=int(rng.integers(2, 7)))
        while sd.weekday() >= 5:
            sd += dt.timedelta(days=1)
        st = dt.datetime.combine(sd, dt.time(7, 30)) + dt.timedelta(minutes=int(rng.integers(0, 150)))
        p = dict(wo='WO%d' % next(woid), wtype='Planned maintenance', start=st,
                 finish=st + dt.timedelta(hours=float(rng.uniform(4, 9)) + 24 * int(rng.choice([0, 0, 1]))), street=street)
        planned.append(p)
        return p

    # planned maintenance with no customer request behind it
    for d in range(0, world.NDAYS - 1, 4):
        st = net[int(rng.integers(len(net)))]
        planned_on(street_of(st), dt.datetime.combine(day(d), dt.time(9, 0)))
    for d in range(world.NDAYS - 1):
        date = day(d)
        for urgent, lam in ((True, 1.15), (False, 2.6)):
            for _ in range(int(rng.poisson(lam))):
                prop = net[int(rng.integers(len(net)))]
                if urgent:
                    after = rng.random() < 0.47
                    if after:
                        t = dt.datetime.combine(date, dt.time(17, 30)) + dt.timedelta(minutes=int(rng.integers(0, 810)))
                    else:
                        t = dt.datetime.combine(date, dt.time(7, 30)) + dt.timedelta(minutes=int(rng.integers(0, 590)))
                    att = dt.timedelta(minutes=float(rng.gamma(4.0, 14.0 if after else 9.0)))
                    res = att + dt.timedelta(minutes=float(rng.gamma(2.2, 95.0)))
                    sr_time = t
                    ext = ''
                    note = ''
                    if after:
                        a_ref = 'AH%06d' % next(aid)
                        caller = prop['address'] if rng.random() < 0.25 else prop['address'].replace(' Road', ' Rd').replace(' Street', ' St').replace(' Avenue', ' Ave')
                        ah.append(dict(ref=a_ref, call=t, address=caller + (', ' + prop['suburb'] if rng.random() < 0.6 else ''),
                                       problem=probs_u[int(rng.integers(len(probs_u)))], priority='P1 - urgent',
                                       paged=t + dt.timedelta(minutes=int(rng.integers(2, 9)))))
                        nxt = dt.datetime.combine(t.date() + dt.timedelta(days=1 if t.hour >= 12 else 0), dt.time(7, 25))
                        sr_time = nxt + dt.timedelta(minutes=int(rng.integers(0, 70)))
                        note = 'Imported from after-hours service'
                    elif rng.random() < 0.18:
                        note = str(rng.choice(['Imported from website fault form', 'Imported from email']))
                    j = 'J%d' % next(jid)
                    s = 'SR%07d' % next(sid)
                    srs.append(dict(sr=s, received=sr_time, priority='Urgent', problem=probs_u[int(rng.integers(len(probs_u)))],
                                    address=prop['address'] + ', ' + prop['suburb'], job=j, ext=ext, note=note, true_notice=t,
                                    attend=t + att, resolve=t + res))
                    jobs.append(dict(job=j, sr=s, crew=str(rng.choice(['Network A', 'Network B', 'Network C', 'On-call'])),
                                     dispatched=t + dt.timedelta(minutes=int(rng.integers(3, 12))), onsite=t + att, done=t + res))
                else:
                    if date.weekday() >= 5:
                        continue
                    t = dt.datetime.combine(date, dt.time(7, 45)) + dt.timedelta(minutes=int(rng.integers(0, 560)))
                    s = 'SR%07d' % next(sid)
                    bundled = rng.random() < 0.24
                    if bundled:
                        w = planned_on(street_of(prop), t)
                        if w is None:
                            bundled = False
                    if bundled:
                        srs.append(dict(sr=s, received=t, priority='Non-urgent', problem=probs_n[int(rng.integers(len(probs_n)))],
                                        address=prop['address'] + ', ' + prop['suburb'], job='', ext='',
                                        note=str(rng.choice(['Completed with planned works on the street', 'Done with scheduled maintenance',
                                                             'Attended with planned maintenance crew'])), true_notice=t,
                                        attend=w['start'], resolve=w['finish']))
                    else:
                        att = dt.timedelta(hours=float(rng.gamma(3.0, 7.5)))
                        res = att + dt.timedelta(hours=float(rng.gamma(2.0, 6.0)))
                        j = 'J%d' % next(jid)
                        srs.append(dict(sr=s, received=t, priority='Non-urgent', problem=probs_n[int(rng.integers(len(probs_n)))],
                                        address=prop['address'] + ', ' + prop['suburb'], job=j, ext='', note='', true_notice=t,
                                        attend=t + att, resolve=t + res))
                        jobs.append(dict(job=j, sr=s, crew=str(rng.choice(['Network A', 'Network B', 'Network C', 'Maintenance'])),
                                         dispatched=t + dt.timedelta(hours=float(rng.uniform(0.5, 6))), onsite=t + att, done=t + res))
    wos = [dict(w, main='', crew=str(rng.choice(['Maintenance', 'Network C', 'Contractor - Rata Civil']))) for w in planned]
    srs.sort(key=lambda r: (r['received'], r['sr']))
    jobs.sort(key=lambda r: (r['dispatched'], r['job']))
    ah.sort(key=lambda r: (r['call'], r['ref']))
    return srs, jobs, ah, wos


# ---------------------------------------------------------------- distractors
def distractors(seed, W):
    rng = rng_for(seed, 'distractors')
    rain = []
    gauges = [('KDC-RG-04', 'Hillcrest'), ('KDC-RG-07', 'Southgate'), ('KDC-RG-11', 'Kowhai Hills')]
    for g, nm in gauges:
        f = float(rng.uniform(0.85, 1.15))
        for d in range(world.NDAYS - 1):
            v = W['rain'][d] * f * float(rng.uniform(0.8, 1.2))
            rain.append((day(d), g, nm, round(v, 1)))
    samples = []
    sites = {}
    for z in world.ZONES:
        sites[z] = ['DS-%s-%02d' % (ZCODE[z], k) for k in range(1, int(rng.integers(2, 4)) + 1)]
    sid = iter(uniq_ints(rng, 4000, 10000, 99999))
    for d in range(world.NDAYS - 1):
        if day(d).weekday() >= 5:
            continue
        for z in world.ZONES:
            if rng.random() < 0.24:
                st = sites[z][int(rng.integers(len(sites[z])))]
                t = dt.datetime.combine(day(d), dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 300)))
                samples.append(dict(sid='S%05d' % next(sid), site=st, zone=ZCODE[z], t=t, ecoli='<1', tc='<1' if rng.random() > 0.03 else str(int(rng.integers(1, 4))),
                                    fac=round(float(rng.normal(0.62, 0.12)), 2), turb=round(float(rng.gamma(2.0, 0.08)), 2)))
    plant = []
    for d in range(world.NDAYS - 1):
        for nm in ('Te Awa WTP', 'Hillcrest WTP'):
            plant.append((day(d), nm, round(float(rng.normal(14.2, 2.1)), 1), round(float(rng.gamma(3.0, 0.03)), 3),
                          round(float(rng.normal(52.0, 4.0)), 1), round(float(rng.normal(1.05, 0.07)), 2)))
    return rain, samples, plant


# ---------------------------------------------------------------- writers
def norm_zip(path, app_fields=None, modified=None):
    """Rewrite an OOXML container with fixed entry dates and scrubbed document properties."""
    import re as _re
    word = path.endswith('.docx')
    zin = zipfile.ZipFile(path)
    items = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    fixed = []
    for name, data in items:
        if word and name == 'docProps/thumbnail.jpeg':
            continue
        if name == '_rels/.rels':
            data = _re.sub(rb'<Relationship [^>]*docProps/thumbnail\.jpeg"[^>]*/>', b'', data)
        if name == 'docProps/core.xml':
            m = _re.search(rb'<dcterms:created[^>]*>([^<]*)</dcterms:created>', data)
            if m:
                stamp = modified.encode() if modified else m.group(1)
                data = _re.sub(rb'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', rb'\g<1>' + stamp + rb'\g<2>', data)
            data = _re.sub(rb'<dc:description>[^<]*</dc:description>', b'<dc:description/>', data)
        if name == 'docProps/app.xml':
            app, ver = (b'Microsoft Office Word', b'16.0000') if word else (b'Microsoft Excel', b'16.0300')
            data = _re.sub(rb'<Application>[^<]*</Application>', b'<Application>' + app + b'</Application>', data)
            data = _re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>' + ver + b'</AppVersion>', data)
            for k, v in sorted((app_fields or {}).items()):
                kb = k.encode()
                data = _re.sub(rb'<' + kb + rb'>[^<]*</' + kb + rb'>', b'<' + kb + b'>' + str(v).encode() + b'</' + kb + b'>', data)
        fixed.append((name, data))
    items = fixed
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(items, key=lambda kv: (kv[0] != '[Content_Types].xml', kv[0])):
            zi = zipfile.ZipInfo(name, ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    open(path, 'wb').write(out.getvalue())


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def write_xlsx(path, sheets, creator, title, created, modified=None):
    """created and modified are UTC, as the writing application stamps them."""
    from openpyxl import Workbook
    wb = Workbook()
    wb.remove(wb.active)
    for name, header, rows in sheets:
        ws = wb.create_sheet(name)
        ws.append(header)
        for r in rows:
            ws.append(list(r))
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.title = title
    wb.properties.created = created
    wb.properties.modified = modified or created
    wb.save(path)
    norm_zip(path, modified=(modified or created).strftime('%Y-%m-%dT%H:%M:%SZ'))


def write_parquet(path, cols):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table(cols)
    t = t.replace_schema_metadata(None)
    pq.write_table(t, path, compression='snappy', use_dictionary=False, write_statistics=False)
