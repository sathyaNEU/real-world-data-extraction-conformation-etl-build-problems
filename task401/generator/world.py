"""task401 world: Wendmoor Water's Coldmere Water Recycling Centre, the River Allery below it, Thornlea Dairy's
discharge, and the records the asks read. One seeded simulation; every file is cut from it in pack.py.

Levels (design note, Draw and Ladder): good status for total ammonia in a lowland, high-alkalinity river is 0.6 mg/l as N
(90th percentile, the Water Environment (Water Framework Directive) (England and Wales) Directions 2015); a nitrifying
activated sludge works runs its final effluent at about 0.5 to 2 mg/l; acid whey carries about 50 to 80 g/l COD at pH
about 4.5; domestic load is about 120 g COD a person a day; nitrifiers need dissolved oxygen above about 1 mg/l and clear an
oxygen-limited backlog over one to two days once the demand passes."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np

UK = ZoneInfo('Europe/London')
UTC = ZoneInfo('UTC')
D0 = date(2024, 10, 1)
D1 = date(2026, 3, 31)
DAYS = [D0 + timedelta(days=i) for i in range((D1 - D0).days + 1)]
N = len(DAYS)
AER_GO_LIVE = date(2025, 10, 27)
NEW_LINE = date(2025, 11, 3)
CT_SWAP = datetime(2025, 10, 20, 10, 30, tzinfo=UK)
WIN = (date(2025, 11, 1), date(2026, 3, 31))
PRIOR = (date(2024, 11, 1), date(2025, 3, 31))
STANDARD = 0.6
SEED = 4012026


def idx(d):
    return (d - D0).days


def daily_process(seed=SEED):
    """The daily truth: river, works, dairy slugs. Returns arrays over DAYS and the slug list."""
    rng = np.random.default_rng(seed)
    doy = np.array([d.timetuple().tm_yday for d in DAYS])
    temp = 14.8 + 4.6 * np.cos(2 * np.pi * (doy - 225) / 365) + rng.normal(0, 0.45, N)
    wet = rng.random(N) < np.where(np.cos(2 * np.pi * (doy - 15) / 365) > 0, 0.55, 0.38)
    rain = np.where(wet, rng.gamma(1.2, 4.2, N), 0.0)
    noise = np.zeros(N)
    for i in range(1, N):
        noise[i] = 0.82 * noise[i - 1] + rng.normal(0, 0.18)
    resp = np.zeros(N)
    for i in range(N):
        resp[i] = (resp[i - 1] * 0.62 if i else 0) + 0.035 * rain[i]
    q_up = (0.62 + 0.48 * np.cos(2 * np.pi * (doy - 20) / 365)) * np.exp(noise) + resp      # m3/s, upstream gauge
    q_up = np.maximum(q_up, 0.16)
    c_up = np.clip(0.042 + 0.0035 * rain + rng.lognormal(np.log(0.012), 0.45, N), 0.02, 0.13)
    growth = 1 + 0.045 * np.arange(N) / N
    q_eff = 9300 * growth * (1 + 0.012 * np.minimum(rain, 25)) * np.exp(rng.normal(0, 0.03, N))   # m3/d
    load = growth * np.exp(rng.normal(0, 0.035, N))
    ctrl = np.array([0.04 if d >= AER_GO_LIVE else 0.0 for d in DAYS])
    normal = (0.60 + 0.052 * np.clip(14.0 - temp, 0, None) + 0.35 * (load - 1.0) + ctrl
              + rng.lognormal(np.log(0.10), 0.55, N))
    normal = np.minimum(normal, 2.05)

    # whey discharges: the old line's occasional losses, and the new line's from 3 November 2025, on the evenings
    # after a missed tanker collection and always before midnight; the strained line stands every Wednesday for its
    # weekly deep clean, so it makes no whey that day and none is run to the drain on a Wednesday evening
    slugs = []
    old_dates = [date(2024, 11, 21), date(2024, 12, 14), date(2025, 1, 30), date(2025, 2, 22),
                 date(2025, 5, 17), date(2025, 7, 10), date(2025, 9, 13)]
    for d in old_dates:
        slugs.append(d)
    d = NEW_LINE
    while d <= D1 - timedelta(days=2):
        if d.weekday() != 2 and rng.random() < 0.24:
            slugs.append(d)
        d += timedelta(days=1)
    slugs = sorted(set(slugs))
    slug_rows = []
    eff = normal.copy()
    for s in slugs:
        i = idx(s)
        vol = float(rng.uniform(17, 31))
        cod = float(rng.uniform(55, 76))
        kg = vol * cod
        start = datetime(s.year, s.month, s.day, 21, 30, tzinfo=UK) + timedelta(minutes=15 * int(rng.integers(0, 4)))
        dur = int(rng.integers(3, 7))
        day1 = 3.2 + 0.0058 * kg * (1 + 0.035 * max(0.0, 12.5 - temp[i + 1])) + rng.normal(0, 0.6)
        day2 = 0.34 * day1 + rng.normal(0, 0.25)
        if i + 1 < N:
            eff[i + 1] = max(eff[i + 1], day1)
        if i + 2 < N:
            eff[i + 2] = max(eff[i + 2], day2)
        slug_rows.append(dict(day=s, start=start, intervals=dur, volume=vol, cod=cod, kg=kg))

    spill = (rain > 14) & (rng.random(N) < 0.7)
    spill_vol = np.where(spill, rng.uniform(600, 2500, N), 0.0)
    def mix(e):
        return (q_up * 86400 * c_up + q_eff * e + spill_vol * 7.0) / (q_up * 86400 + q_eff + spill_vol)
    river = mix(eff)
    # a day's mean never sits within 0.07 of the standard, so no reading of the monitor's validity rules moves a day
    # across it: a recovering works' second day is either still well up or already back
    for i in range(N):
        if 0.53 < river[i] < 0.67:
            target = 0.71 if river[i] >= 0.60 else 0.50
            denom = q_up[i] * 86400 + q_eff[i] + spill_vol[i]
            eff[i] = max(normal[i], (target * denom - q_up[i] * 86400 * c_up[i] - spill_vol[i] * 7.0) / q_eff[i])
    river = mix(eff)
    return dict(temp=temp, rain=rain, q_up=q_up, c_up=c_up, q_eff=q_eff, load=load, normal=normal, eff=eff,
                river=river, spill=spill, spill_vol=spill_vol, slugs=slug_rows, ctrl=ctrl)


def exceedance_days(P, lo, hi):
    return [d for d in DAYS if lo <= d <= hi and P['river'][idx(d)] > STANDARD]


def reach_forms(P, lo, hi):
    """Every natural operationalisation of 'the exceedance days a discharge sets off'. Returns {form: count}."""
    exc = exceedance_days(P, lo, hi)
    big = {s['day'] for s in P['slugs']}
    small = set(P.get('acid_nights', []))
    out = {}
    for name, lags, src in [('1-2', (1, 2), big), ('1-3', (1, 2, 3), big), ('1-4', (1, 2, 3, 4), big),
                            ('1-5', (1, 2, 3, 4, 5), big), ('0-3', (0, 1, 2, 3), big),
                            ('any 1-3', (1, 2, 3), big | small), ('any 0-5', (0, 1, 2, 3, 4, 5), big | small)]:
        out[name] = sum(1 for d in exc if any((d - timedelta(days=L)) in src for L in lags))
    # episode-based: runs of days whose works effluent is above three times its normal running level, started within a
    # day of a discharge
    ep = 0
    for d in exc:
        i = idx(d)
        j = i
        while j > 0 and P['eff'][j] > 3.0:
            j -= 1
        if any((DAYS[j] - timedelta(days=L)) in big for L in (0, 1)) or DAYS[j] in big:
            ep += 1
    out['episode'] = ep
    return out


def dairy_15min(P, seed=SEED):
    """Thornlea Dairy's own discharge monitor at its sampling chamber: local time, 15-minute flow, pH and temperature."""
    rng = np.random.default_rng(seed + 11)
    rows = []
    slug_at = {}
    for s in P['slugs']:
        for k in range(s['intervals']):
            slug_at[s['start'] + timedelta(minutes=15 * k)] = s
    acid_nights = []
    t = datetime(D0.year, D0.month, D0.day, 0, 0, tzinfo=UK)
    end = datetime(D1.year, D1.month, D1.day, 23, 45, tzinfo=UK) + timedelta(minutes=15)
    t_utc = t.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    acid_today = {}
    while t_utc < end_utc:
        lt = t_utc.astimezone(UK)
        dd = lt.date()
        if dd not in acid_today:
            acid_today[dd] = (rng.random() < 0.16) and dd.weekday() in (0, 1, 2, 3, 4)
            if acid_today[dd]:
                acid_nights.append(dd)
        h = lt.hour + lt.minute / 60
        prod = 6.0 <= h < 22.5 and dd.weekday() != 6
        # the strained line runs six days a week and stands every Wednesday for its weekly deep clean and maintenance,
        # so from 3 November the chamber carries its flow on every day but Wednesday (and no whey is made that day)
        line = 1.18 if (dd >= NEW_LINE and dd.weekday() != 2) else 1.0
        flow = (rng.uniform(5.5, 11.5) if prod else rng.uniform(0.8, 2.6)) * line
        if prod:
            ph = float(6.75 + rng.gamma(4.0, 0.27))
            while ph > 10.3:                        # the dairy doses its caustic rinses back below the consent's 11
                ph = float(6.75 + rng.gamma(4.0, 0.27))
        else:
            ph = float(6.85 + rng.gamma(6.0, 0.09))
        tc = float(rng.normal(27 if prod else 19, 2.2))
        key = lt.replace(second=0, microsecond=0)
        if key in slug_at:
            flow = float(rng.uniform(8.2, 11.4))
            ph = float(rng.uniform(6.08, 6.42))
            tc = float(rng.uniform(17.5, 21.5))
        elif acid_today[dd] and 1.0 <= h < 1.75:
            flow = float(rng.uniform(2.0, 3.6))
            ph = float(rng.uniform(6.35, 6.65))
        rows.append((lt, round(flow, 2), round(ph, 2), round(tc, 1)))
        t_utc += timedelta(minutes=15)
    P['acid_nights'] = acid_nights
    return rows
