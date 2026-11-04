"""The records the asks read: trade effluent metering and sampling (Ask A), the blower meters (Ask B) and the homes
connected to the catchment (Ask C). Truth first; the files are cut from it in pack.py."""
from datetime import date, datetime, timedelta
import numpy as np
from world import UK, UTC, SEED

CY = (date(2025, 4, 1), date(2026, 3, 31))          # charging year 2025-26
QDATES = [date(2025, 3, 31), date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31), date(2026, 3, 31)]

# ---------------------------------------------------------------- Ask A: trade effluent
DISCHARGERS = [
    # name, code, consent, LIMS code, sampling point, m3 a day, allowance, settled COD, suspended solids
    ('Thornlea Dairy', 'TED-017', 'TE/C/0417', 'THL01', 'TH-SC1', 248.0, 0.04, 2350.0, 610.0),
    ('Wyecote Brewery', 'TED-022', 'TE/C/0522', 'WYB02', 'WY-SC1', 78.0, 0.06, 3120.0, 455.0),
    ('Kestry Linen Services', 'TED-031', 'TE/C/0631', 'KLS03', 'KL-SC1', 86.0, 0.03, 905.0, 148.0),
    ('Allery Springs Bottling', 'TED-034', 'TE/C/0734', 'ASB04', 'AS-SC2', 61.0, 0.08, 1790.0, 118.0),
    ('Pellow Meats', 'TED-040', 'TE/C/0840', 'PLM05', 'PM-SC1', 49.0, 0.05, 2690.0, 790.0),
]
RATES = dict(R=0.4421, V=0.5248, Bv=0.0986, B=0.6133, S=0.4387, Os=470.0, Ss=330.0)
EXCHANGES = {'Wyecote Brewery': (date(2025, 8, 14), 2516), 'Pellow Meats': (date(2025, 12, 3), 3804)}   # opening register above the old meter's final read
TEN_REGISTER = 'Kestry Linen Services'
LEGACY_CODE = ('Allery Springs Bottling', 'ASB-LEG', date(2025, 10, 6))


def trade_effluent(seed=SEED):
    """Meters, quarter-end reads by meter point (the automatic reading at midnight), the reads taken when a meter was
    exchanged, and the true chargeable advances."""
    rng = np.random.default_rng(seed + 101)
    start, end = date(2025, 3, 31), date(2026, 3, 31)
    meters, reads, truth = [], [], {}
    for k, (name, code, consent, lims_code, point, daily, allow, ot, st) in enumerate(DISCHARGERS):
        mp = 'MP-%s' % code[-3:]
        mult = 10 if name == TEN_REGISTER else 1
        days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
        vol = {d: daily * float(rng.lognormal(0, 0.18)) * (0.55 if d.weekday() == 6 else 1.0) for d in days[1:]}
        serial = 'TE%07d' % rng.integers(1000000, 9999999)
        reg0 = float(rng.integers(14000, 26000)) if mult == 1 else float(rng.integers(1500, 2600))
        meter = dict(meter_point=mp, discharger=name, serial=serial, installed=date(2019, 5, 2 + k), removed='',
                     initial_read='', final_read='', multiplier=mult)
        meters.append(meter)
        reg = reg0
        ex = EXCHANGES.get(name)
        advance = 0.0
        for d in days:
            if d > start:
                if ex and d == ex[0]:
                    # the exchange is made at 11:00: the morning's flow goes through the old meter, the rest through
                    # the new one, whose register was not set back to the old meter's
                    share = 11 / 24
                    reg += vol[d] * share / mult
                    meter['removed'] = ex[0]
                    meter['final_read'] = int(round(reg))
                    reads.append(dict(meter_point=mp, read_date=ex[0], read=int(round(reg)),
                                      kind='Exchange: final read of removed meter'))
                    opening = int(round(reg)) + ex[1]
                    reads.append(dict(meter_point=mp, read_date=ex[0], read=opening,
                                      kind='Exchange: initial read of fitted meter'))
                    reg = float(opening)
                    new_serial = 'TE%07d' % rng.integers(1000000, 9999999)
                    meter = dict(meter_point=mp, discharger=name, serial=new_serial, installed=ex[0], removed='',
                                 initial_read=opening, final_read='', multiplier=1)
                    meters.append(meter)
                    reg += vol[d] * (1 - share) / mult
                else:
                    reg += vol[d] / mult
                advance += vol[d]
            if d in QDATES:
                reads.append(dict(meter_point=mp, read_date=d, read=int(round(reg)), kind='AMR 00:00'))
        truth[name] = dict(volume_true=advance, meter_point=mp, mult=mult)
    reads.sort(key=lambda r: (r['meter_point'], r['read_date'], r['kind'] != 'Exchange: final read of removed meter'))
    return meters, reads, truth


BOTTLE_ML = 2500
LIMS_OFFSET = 205


def lims(seed=SEED):
    """Weekly composites, Wednesday 09:00 to Thursday 09:00, taken by each site's flow-proportional sampler, collected
    on the Thursday round and reported by the laboratory one to three weeks later. On a high-flow day the sampler fills
    its 2.5-litre bottle and runs on into a second, which fills over the night and early morning on weaker effluent;
    the sampler collects each bottle under its own pre-printed label and the laboratory analyses each one. Returns
    (round sheet rows, one per bottle; LIMS result rows, one per bottle and determinand; sampler download rows, one per
    bottle; the true composites)."""
    rng = np.random.default_rng(seed + LIMS_OFFSET)
    sheets, results, downloads, composites = [], [], [], []
    n = {}
    label = 418000
    d = date(2025, 1, 2)
    while d <= date(2026, 4, 30):
        if d.weekday() == 3:
            minute = 60
            for k, (name, code, consent, lims_code, point, daily, allow, ot, st) in enumerate(DISCHARGERS):
                minute += int(rng.integers(6, 14))
                taken = datetime(d.year, d.month, d.day, 8 + minute // 60, minute % 60, tzinfo=UK)
                start = datetime(d.year, d.month, d.day, 9, 0, tzinfo=UK) - timedelta(days=1, minutes=-int(rng.integers(0, 3)))
                lag = int(rng.choice([6, 7, 8, 12, 13, 14, 15, 19, 20], p=[.08, .12, .1, .1, .16, .16, .12, .08, .08]))
                reported = d + timedelta(days=lag)
                total_ml = 2400.0 * float(rng.lognormal(0, 0.22))
                vols = [total_ml] if total_ml <= BOTTLE_ML + 150 else [float(BOTTLE_ML), total_ml - BOTTLE_ML]
                cod1 = float(ot * rng.lognormal(0, 0.16))
                ss1 = float(st * rng.lognormal(0, 0.22))
                conc = [(cod1, ss1)]
                if len(vols) == 2:
                    conc.append((cod1 * float(rng.uniform(0.45, 0.65)), ss1 * float(rng.uniform(0.45, 0.65))))
                tot = sum(vols)
                composites.append(dict(discharger=name, point=point, collected=taken,
                                       cod=sum(v * c[0] for v, c in zip(vols, conc)) / tot,
                                       ss=sum(v * c[1] for v, c in zip(vols, conc)) / tot, bottles=len(vols)))
                site_t = float(rng.normal(21.0, 3.0))
                for b, (v, (cod, ss)) in enumerate(zip(vols, conc)):
                    label += int(rng.integers(1, 3))
                    ref = 'TE%06d' % label
                    yy = d.strftime('%y')
                    n[yy] = n.get(yy, 0) + 1
                    sno = 'S%s-%05d' % (yy, 10000 + n[yy])
                    site_ph = float(np.clip(rng.normal(7.6, 0.35), 6.6, 9.4))
                    sheets.append(dict(bottle_ref=ref, discharger=name, sampling_point=point, collected_at=taken,
                                       bottle=b + 1, site_ph=site_ph, site_temp=site_t + float(rng.normal(0, 0.4))))
                    downloads.append(dict(point=point, run_start=start,
                                          run_end=taken, bottle=b + 1, aliquots=int(round(v / 25.0)),
                                          volume_ml=int(round(v))))
                    lc = LEGACY_CODE[1] if (name == LEGACY_CODE[0] and reported < LEGACY_CODE[2]) else lims_code
                    for det, val in (('COD settled', cod), ('COD total', cod * float(rng.uniform(1.22, 1.45))),
                                     ('Suspended solids', ss)):
                        results.append(dict(sample_no=sno, client_ref=ref, lims_code=lc, point=point, determinand=det,
                                            result=int(round(val)), units='mg/l', reported=reported))
        d += timedelta(days=1)
    results.sort(key=lambda r: (r['reported'], r['sample_no'], r['determinand']))
    return sheets, results, downloads, composites


# ---------------------------------------------------------------- Ask B: blower electricity
E0 = datetime(2024, 10, 1, 0, 0, tzinfo=UK)
E1 = datetime(2026, 4, 1, 0, 0, tzinfo=UK)
CT_SWAP = datetime(2025, 10, 20, 10, 30, tzinfo=UK)
ROLL = 1_000_000


def blowers(seed=SEED):
    """Half-hourly advances (meter units) for the two blower-house meters, the monthly billing snapshots at midnight UK
    time, and the read taken when BH-B's current transformers were changed."""
    rng = np.random.default_rng(seed + 303)
    t = E0.astimezone(UTC)
    end = E1.astimezone(UTC)
    rows = []
    cum = {'BH-A': 987_412.0, 'BH-B': 412_876.0, 'MCC-7': 0.0, 'INL-1': 228_514.0, 'SLG-1': 517_093.0}
    snaps = []
    swap_done = False
    tb_on = datetime(2025, 10, 27, 0, 0, tzinfo=UK)
    site_reads = [('INL-1', datetime(2025, 3, 12, 11, 20, tzinfo=UK)), ('SLG-1', datetime(2025, 6, 4, 14, 0, tzinfo=UK)),
                  ('BH-A', datetime(2025, 10, 20, 10, 15, tzinfo=UK))]
    while t < end:
        lt = t.astimezone(UK)
        if lt.day == 1 and lt.hour == 0 and lt.minute == 0:
            for m in ('BH-A', 'BH-B', 'MCC-7', 'INL-1', 'SLG-1'):
                if m != 'MCC-7' or lt >= tb_on:
                    snaps.append(dict(meter=m, read_at=lt, register=int(cum[m]) % ROLL, kind='monthly snapshot'))
        for m, at in list(site_reads):
            if lt >= at:
                snaps.append(dict(meter=m, read_at=at, register=int(cum[m]) % ROLL, kind='site read'))
                site_reads.remove((m, at))
        if not swap_done and lt >= CT_SWAP:
            snaps.append(dict(meter='BH-B', read_at=CT_SWAP, register=int(cum['BH-B']) % ROLL, kind='site read'))
            swap_done = True
        if lt == tb_on:
            snaps.append(dict(meter='MCC-7', read_at=tb_on, register=0, kind='commissioning read'))
        h = lt.hour + lt.minute / 60
        winter = 1 + 0.10 * np.cos(2 * np.pi * (lt.timetuple().tm_yday - 15) / 365)
        new = lt >= tb_on
        loads = (('BH-A', 118 * (0.92 if new else 1.0), 9), ('BH-B', 104 * (0.14 if new else 1.0), 10)) + \
                ((('MCC-7', 78, 11),) if new else ()) + (('INL-1', 46, 8), ('SLG-1', 61, 13))
        for m, base, ph in loads:
            kw = max(6.0, (base + 0.19 * base * np.sin(2 * np.pi * (h - ph) / 24)) * winter * float(rng.lognormal(0, 0.07)))
            mult = 80 if (m == 'BH-B' and lt >= CT_SWAP) else (40 if m in ('BH-A', 'BH-B') else 1)
            units = round(kw / 2 / mult, 3)
            cum[m] += units
            rows.append(dict(meter=m, start_utc=t, units=units, kwh=units * mult))
        t += timedelta(minutes=30)
    for m in ('BH-A', 'BH-B', 'MCC-7', 'INL-1', 'SLG-1'):
        snaps.append(dict(meter=m, read_at=E1, register=int(cum[m]) % ROLL, kind='monthly snapshot'))
    return rows, snaps


# ---------------------------------------------------------------- Ask C: homes connected
DEVELOPMENTS = [('Coldmere Fields', 'CF'), ('Brook Farm Rise', 'BF'), ('Allery Meadows', 'AM'),
                ('Station Quarter', 'SQ'), ('Holloway Grange', 'HG')]


def connections(seed=SEED):
    rng = np.random.default_rng(seed + 404)
    phases, laterals, uprns = [], [], []
    u = 100023400000
    for di, (dev, pre) in enumerate(DEVELOPMENTS):
        start = date(2023, 2, 1) + timedelta(days=int(rng.integers(0, 140)))
        ph = 0
        while start < date(2025, 11, 1):
            ph += 1
            p_conn = start + timedelta(days=int(rng.integers(20, 70)))
            approved = int(rng.integers(30, 66))
            nb = int(approved * float(rng.uniform(0.72, 0.94)))
            bdate = p_conn + timedelta(days=int(rng.integers(25, 70)))
            for b in range(nb):
                homes = int(rng.choice([1] * 9 + [6, 8, 9, 12])) if pre != 'BF' else 1
                bref = '%s%d-%03d' % (pre, ph, b + 1)
                lat_date = bdate
                bdate = bdate + timedelta(days=int(rng.integers(2, 13)))
                laterals.append(dict(lateral='%s/%d/%03d' % (pre, ph, b + 1), development=dev, building=bref,
                                     connected=lat_date))
                for f in range(homes):
                    u += int(rng.integers(1, 30))
                    uprns.append(dict(uprn=u, development=dev, building=bref, flat=(f + 1 if homes > 1 else 0)))
            phases.append(dict(development=dev, phase=ph, plots_approved=approved, phase_connected=p_conn))
            start = bdate + timedelta(days=int(rng.integers(30, 120)))
    return phases, laterals, uprns
