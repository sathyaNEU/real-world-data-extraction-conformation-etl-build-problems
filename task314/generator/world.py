"""task314's world: the City of Ardley Springs Water Department.

Accounts and premises, the rate schedules in force by bill date, daily weather, every water bill issued from
June 2022 to October 2026, and the supply-side records for 2026 (the district's turnout deliveries, the city's
wells, the fill station, the city's own unbilled meters, the meter shop's work orders).

The clean truth: a household's billed use answers the average price of its whole bill (fixed charges included)
at the use it would otherwise have, with one summer elasticity ETA.  No household answers its marginal block price.
"""
import datetime as dt
import math
import numpy as np

SEED = 314
ETA = -0.32                      # elasticity of use on the whole bill's average price
P_REF = 6.00                     # reference price, dollars a thousand gallons (sets the level only)
AF_KGAL = 325.851                # thousand gallons in an acre-foot
CCF_KGAL = 0.748052              # thousand gallons in a hundred cubic feet
CAPITAL_FROM = dt.date(2024, 7, 1)
RESTRUCTURE_FROM = dt.date(2023, 7, 1)
FM_CHARGE = 14.00
NCYC = 20


def ym_range(a, b):
    out, (y, m) = [], a
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


BILL_MONTHS = ym_range((2022, 6), (2026, 10))
READ_MONTHS = ym_range((2022, 5), (2026, 10))        # May 2022 gives June 2022's opening read


def weekday_on_or_near(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


# nominal read day of each cycle (3rd to 24th), and a fixed small wobble per cycle and month
_cyc_rng = np.random.default_rng(SEED + 1)
CYCLE_DAY = [3 + c + (1 if c >= 10 else 0) for c in range(NCYC)]
_WOBBLE = {(y, m): _cyc_rng.integers(-1, 2, size=NCYC) for (y, m) in READ_MONTHS}


def read_date(cycle, y, m):
    d = dt.date(y, m, min(28, max(2, CYCLE_DAY[cycle] + int(_WOBBLE[(y, m)][cycle]))))
    return weekday_on_or_near(d)


def bill_date(rd):
    d = rd + dt.timedelta(days=3)
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


# ---------------------------------------------------------------- weather (one co-op station, daily)
W_START, W_END = dt.date(2022, 4, 1), dt.date(2026, 10, 31)


def make_weather():
    rng = np.random.default_rng(SEED + 2)
    days = [W_START + dt.timedelta(days=i) for i in range((W_END - W_START).days + 1)]
    year_heat = {2022: 0.5, 2023: 0.7, 2024: 0.1, 2025: 0.5, 2026: 0.8}      # degrees C on the summer
    out = []
    ar = 0.0
    for d in days:
        doy = d.timetuple().tm_yday
        seas = math.sin(2 * math.pi * (doy - 105) / 365.25)
        ar = 0.7 * ar + rng.normal(0, 2.4)
        summer = max(0.0, seas)
        tmax = 17.0 + 15.5 * seas + ar + year_heat[d.year] * summer
        tmin = tmax - 14.0 - 2.0 * summer + rng.normal(0, 1.6)
        # spring storms and a July to August monsoon
        p_wet = 0.16 + 0.06 * math.cos(2 * math.pi * (doy - 110) / 365.25) + (0.12 if 190 <= doy <= 245 else 0.0)
        precip = 0.0
        if rng.random() < p_wet:
            precip = float(rng.gamma(1.6, 2.9))
        et0 = max(0.4, 0.0023 * ((tmax + tmin) / 2 + 17.8) * math.sqrt(max(tmax - tmin, 1.0)) * (11.0 + 9.5 * seas) * 0.408 * 2.2
                  + rng.normal(0, 0.25))
        if precip > 3:
            et0 *= 0.75
        out.append((d, round(tmax, 1), round(tmin, 1), round(precip, 1), round(et0, 2)))
    return out


WEATHER = make_weather()
_WIDX = {w[0]: i for i, w in enumerate(WEATHER)}
_ET = np.array([w[4] for w in WEATHER])
_PR = np.array([w[3] for w in WEATHER])


def irrigation_index(d0, d1):
    """Irrigation demand over the service period (d0, d1]: evapotranspiration less effective rain, per day,
    scaled so that a normal July day is about 1."""
    i0, i1 = _WIDX[d0] + 1, _WIDX[d1] + 1
    et, pr = _ET[i0:i1].sum(), _PR[i0:i1].sum()
    n = max(i1 - i0, 1)
    return max(0.0, (et - 0.62 * pr) / n - 1.25) / 5.4


# ---------------------------------------------------------------- rates
SFR_OLD = dict(base={0.75: 24.00, 1.0: 33.60}, tiers=[(8.0, 3.40), (20.0, 4.40), (None, 7.20)])
SFR_NEW = dict(base={0.75: 19.25, 1.0: 27.40}, tiers=[(6.0, 3.20), (15.0, 4.50), (None, 10.80)])
MFR_OLD = dict(base=30.00, vol=4.10)
MFR_NEW = dict(base=31.50, vol=4.30)
COM_BASE_OLD = {1.0: 26.50, 1.5: 53.00, 2.0: 84.80}
COM_BASE_NEW = {1.0: 27.40, 1.5: 54.80, 2.0: 87.70}
COM_VOL = (4.40, 4.60)
IRR_VOL = (5.10, 5.40)

# the drought plan's Stage 2 rate options for 2027 (bills issued 1 May to 31 October 2027)
OPT_A_TIER1 = 2.70               # Option A, conservation blocks: a cheaper first block and a dearer third
OPT_A_TIER3 = 14.80
OPT_B_ADDER = 0.60               # Option B, a drought adder on every thousand gallons
OPT_C_SURCHARGE = 13.60          # Option C, a drought surcharge on every bill


def sfr_schedule(bdate):
    return SFR_NEW if bdate >= RESTRUCTURE_FROM else SFR_OLD


def tier_volumes(q, tiers):
    vols, lo = [], 0.0
    for hi, _ in tiers:
        top = q if hi is None else min(q, hi)
        vols.append(max(0.0, top - lo))
        if hi is not None:
            lo = hi
    return vols


def sfr_charges(q, meter, sched, fm_capital=0.0, adder=0.0, tier3=None, surcharge=0.0, tier1=None):
    tiers = list(sched['tiers'])
    if tier3 is not None:
        tiers[2] = (None, tier3)
    if tier1 is not None:
        tiers[0] = (tiers[0][0], tier1)
    vols = tier_volumes(q, tiers)
    vol_chg = [v * (p + adder) for v, (_, p) in zip(vols, tiers)]
    base = sched['base'][meter]
    return base, vol_chg, fm_capital, surcharge


def sfr_bill(q, meter, sched, fm_capital=0.0, adder=0.0, tier3=None, surcharge=0.0, tier1=None):
    base, vol_chg, cap, sur = sfr_charges(q, meter, sched, fm_capital, adder, tier3, surcharge, tier1)
    return base + sum(vol_chg) + cap + sur


def sfr_marginal(q, sched, adder=0.0, tier3=None, tier1=None):
    tiers = list(sched['tiers'])
    if tier3 is not None:
        tiers[2] = (None, tier3)
    if tier1 is not None:
        tiers[0] = (tiers[0][0], tier1)
    lo = 0.0
    for hi, p in tiers:
        if hi is None or q <= hi:
            return p + adder
    return tiers[-1][1] + adder


# ---------------------------------------------------------------- streets and premises
STREETS_CITY = ['Alder', 'Bannock', 'Cottonwood', 'Delmar', 'Edgewater', 'Farrier', 'Gilchrist', 'Hollyhock', 'Ironstone',
                'Juniper', 'Kingsway', 'Larkspur', 'Mesquite', 'Northgate', 'Orchard', 'Pinyon', 'Quarry', 'Redbank',
                'Sagebrush', 'Tamarisk', 'Upland', 'Vista', 'Westbrook', 'Yarrow', 'Bluestem', 'Canyon Rim', 'Dry Creek',
                'Elkhorn', 'Foothill', 'Granary', 'Harvest', 'Indian Paintbrush', 'Kestle', 'Lodgepole', 'Millrace']
SUFFIX = ['St', 'Ave', 'Dr', 'Ct', 'Ln', 'Way', 'Pl', 'Cir']
STREETS_FM = ['Fenwick Mesa', 'Caprock', 'Sandstone', 'Rimrock', 'Saltgrass', 'Antelope', 'Buttes', 'Chamisa', 'Desert Willow',
              'Gambel Oak', 'Ridgeline', 'Shale', 'Tableland', 'Windmill']

N_SFR_CITY, N_SFR_FM = 3300, 1500
N_MFR, N_COM, N_IRR = 72, 214, 88


class Premise:
    __slots__ = ('pid', 'area', 'cls', 'meter', 'cycle', 'lot', 'addr', 'outdoor', 'units', 'legacy_until',
                 'accounts', 'com_level', 'com_season')


class Account:
    __slots__ = ('acct', 'pid', 'start', 'end', 'indoor', 'hh', 'bills')


def _premise_ids(rng, n, prefix):
    """Premise numbers as the billing system assigned them: in the order the services were set up, with the gaps
    that retired and never-built premises leave."""
    pool = np.sort(rng.choice(np.arange(100000, 999999), size=n, replace=False))
    return ['%s%06d' % (prefix, int(x)) for x in pool]


def make_premises():
    rng = np.random.default_rng(SEED + 3)
    prems = []
    ids = _premise_ids(rng, N_SFR_CITY + N_SFR_FM + N_MFR + N_COM + N_IRR, 'PR')
    k = 0

    def street(area):
        names = STREETS_FM if area == 'FMSA' else STREETS_CITY
        return '%d %s %s' % (int(rng.integers(100, 4900)), names[int(rng.integers(len(names)))], SUFFIX[int(rng.integers(len(SUFFIX)))])

    for area, n in (('CITY', N_SFR_CITY), ('FMSA', N_SFR_FM)):
        for _ in range(n):
            p = Premise()
            p.pid, p.area, p.cls = ids[k], area, 'SFR'
            k += 1
            p.lot = float(np.exp(np.log(8300) + 0.42 * rng.standard_normal()))
            p.meter = 1.0 if (p.lot > 11500 and rng.random() < 0.62) or rng.random() < 0.05 else 0.75
            p.cycle = int(rng.integers(NCYC))
            p.addr = street(area)
            # outdoor use per unit of irrigation demand, kgal a month: lot size, a garden habit, a lawn share
            p.outdoor = float(11.5 * (p.lot / 8400) ** 0.85 * np.exp(0.40 * rng.standard_normal()))
            p.units = 1
            # Fenwick Mesa's legacy hundred-cubic-foot meters: two thirds replaced in the 2022 to 2023 change-out
            p.legacy_until = None
            if area == 'FMSA':
                if rng.random() < 0.66:
                    p.legacy_until = dt.date(2022, 3, 7) + dt.timedelta(days=int(rng.integers(0, 470)))
                else:
                    p.legacy_until = dt.date(2099, 1, 1)
            p.accounts = []
            prems.append(p)
    for cls, n in (('MFR', N_MFR), ('COM', N_COM), ('IRR', N_IRR)):
        for _ in range(n):
            p = Premise()
            p.pid, p.cls = ids[k], cls
            k += 1
            p.area = 'FMSA' if rng.random() < 0.24 else 'CITY'
            p.cycle = int(rng.integers(NCYC))
            p.addr = street(p.area)
            p.lot = float(np.exp(np.log(30000) + 0.6 * rng.standard_normal()))
            p.units = int(rng.integers(3, 48)) if cls == 'MFR' else 1
            p.meter = float(rng.choice([1.0, 1.5, 2.0], p=[0.45, 0.35, 0.20])) if cls != 'MFR' else 1.5
            p.outdoor = float(np.exp(np.log(14.0 if cls == 'MFR' else (18.0 if cls == 'COM' else 42.0)) + 0.55 * rng.standard_normal()))
            p.com_level = float(np.exp(np.log(34.0) + 0.85 * rng.standard_normal()))
            p.com_season = float(rng.uniform(0.2, 1.0))
            p.legacy_until = dt.date(2099, 1, 1) if p.area == 'FMSA' and rng.random() < 0.3 else None
            p.accounts = []
            prems.append(p)
    return prems


def _acct_no(route, p, seq):
    return '%02d%02d-%05d-%02d' % (p.cycle + 1, route, int(p.pid[2:]) % 100000, seq)


def make_accounts(prems):
    """Occupancy spells: most premises keep one account through the window; some change hands, once or twice."""
    rng = np.random.default_rng(SEED + 4)
    w0, w1 = dt.date(2022, 5, 1), dt.date(2026, 11, 1)
    for p in prems:
        cuts = []
        route = int(rng.integers(10, 99))
        rate = 0.085 if p.cls == 'SFR' else 0.03
        d = w0
        while True:
            gap = int(rng.exponential(365.0 / rate))
            d = d + dt.timedelta(days=gap)
            if d >= w1:
                break
            cuts.append(d)
        starts = [w0] + cuts
        ends = cuts + [None]
        for s, (a, b) in enumerate(zip(starts, ends)):
            acc = Account()
            acc.pid = p.pid
            acc.start, acc.end = a, b
            acc.acct = _acct_no(route, p, s + 1)
            acc.indoor = float(np.exp(np.log(4.3) + 0.38 * rng.standard_normal())) * (1.0 if p.cls == 'SFR' else 1.0)
            acc.hh = float(np.exp(0.10 * rng.standard_normal()))
            acc.bills = []
            p.accounts.append(acc)
    return prems


# ---------------------------------------------------------------- the bill simulation
def account_in_period(acc, d0, d1):
    """The account's share of the service period (d0, d1] it occupied."""
    a = acc.start
    b = acc.end or dt.date(2100, 1, 1)
    lo, hi = max(a, d0), min(b, d1)
    return max(0, (hi - lo).days) / max(1, (d1 - d0).days)


def simulate_bills(prems):
    """Every bill from June 2022 to October 2026, the truth's use on each, and its charges as billed."""
    rng = np.random.default_rng(SEED + 5)
    bills = []
    for p in prems:
        # a household-year shock and a persistent premise effect
        prem_eff = float(np.exp(0.06 * rng.standard_normal()))
        yr_eff = {y: float(np.exp(0.03 * rng.standard_normal())) for y in range(2022, 2027)}
        for t, (y, m) in enumerate(BILL_MONTHS):
            py, pm = READ_MONTHS[t]
            d0 = read_date(p.cycle, py, pm)
            d1 = read_date(p.cycle, y, m)
            bd = bill_date(d1)
            days = (d1 - d0).days
            irr = irrigation_index(d0, d1)
            for acc in p.accounts:
                share = account_in_period(acc, d0, d1)
                if share <= 0:
                    continue
                if p.cls == 'SFR':
                    qn = (acc.indoor * acc.hh * days / 30.4 + p.outdoor * irr) * prem_eff * yr_eff[y] * share
                    sched = sfr_schedule(bd)
                    cap = FM_CHARGE if (p.area == 'FMSA' and bd >= CAPITAL_FROM) else 0.0
                    ap = sfr_bill(max(qn, 0.5), p.meter, sched, cap) / max(qn, 0.5)
                    q = qn * (ap / P_REF) ** ETA * float(np.exp(0.07 * rng.standard_normal()))
                    u = rng.random()
                    summer = m in (6, 7, 8, 9)
                    if u < (0.003 if summer else 0.006):
                        q += float(rng.uniform(4.0, 22.0))            # a running toilet or a broken line
                    elif u < (0.004 if summer else 0.014):
                        q *= float(rng.uniform(0.05, 0.25))           # away for most of the period
                elif p.cls == 'MFR':
                    qn = (p.units * 3.1 * days / 30.4 + p.outdoor * irr) * prem_eff * yr_eff[y] * share
                    q = qn * float(np.exp(0.10 * rng.standard_normal()))
                elif p.cls == 'COM':
                    qn = p.com_level * (1 - p.com_season + p.com_season * (0.45 + 1.1 * irr)) * days / 30.4 * prem_eff * yr_eff[y] * share
                    q = qn * float(np.exp(0.14 * rng.standard_normal()))
                else:  # IRR: meters locked off from November to March
                    on = m in (4, 5, 6, 7, 8, 9, 10)
                    qn = p.outdoor * irr * 1.9 * prem_eff * yr_eff[y] * share if on else 0.0
                    q = qn * float(np.exp(0.12 * rng.standard_normal())) if on else 0.0
                q = max(0.0, q)
                bills.append(dict(prem=p, acc=acc, t=t, y=y, m=m, d0=d0, d1=d1, bdate=bd, q=q))
    return bills


def charges_as_billed(b):
    """The charges the city's billing system put on the bill, by schedule, meter, area and bill date."""
    p, q, bd = b['prem'], b['q'], b['bdate']
    cap = FM_CHARGE if (p.area == 'FMSA' and bd >= CAPITAL_FROM) else 0.0
    if p.cls == 'SFR':
        sched = sfr_schedule(bd)
        base, vol, _, _ = sfr_charges(q, p.meter, sched)
        return base, vol, cap
    if p.cls == 'MFR':
        s = MFR_NEW if bd >= RESTRUCTURE_FROM else MFR_OLD
        return s['base'] * max(1, p.units // 4), [q * s['vol'], 0.0, 0.0], cap
    if p.cls == 'COM':
        bs = COM_BASE_NEW if bd >= RESTRUCTURE_FROM else COM_BASE_OLD
        v = COM_VOL[1] if bd >= RESTRUCTURE_FROM else COM_VOL[0]
        return bs[p.meter], [q * v, 0.0, 0.0], cap
    bs = COM_BASE_NEW if bd >= RESTRUCTURE_FROM else COM_BASE_OLD
    v = IRR_VOL[1] if bd >= RESTRUCTURE_FROM else IRR_VOL[0]
    on = b['m'] in (4, 5, 6, 7, 8, 9, 10)
    return (bs[p.meter] if on else 0.0), [q * v, 0.0, 0.0], cap


PRICE_FILL_2026 = 0.0095          # dollars a gallon at the fill station
