"""task401 architecture 3: the generator's clean truth.

A GB domestic energy supplier. Customers who joined July to December 2024 answer the six-month survey
January to June 2025 (period 0, legacy billing platform); customers who joined July to December 2025 answer
January to June 2026 (period 1, every one billed on the new platform). From May 2025 the quote journey stopped
pre-filling each meter point's industry annual quantity (EAC, AQ): a customer was quoted on use they typed in,
or on Ofgem's medium typical values when they gave none. Six-month satisfaction responds to how far the cost of
the meter point's annual quantity runs above the cost the quote projected, at the quote's own rates (negative
disconfirmation, asymmetric), plus small real effects of the platform, the October 2025 variable-rate rise and
the November 2025 contact centre move. Files are cut from this truth by pack.py.
"""
import datetime as dt
from math import log
import numpy as np

SEED = 4012026
D = dt.date
TYPICAL_E, TYPICAL_G = 2700.0, 11500.0
# Ofgem region names with their distribution network operator ids (the first two MPAN core digits), weights
REGIONS = [('Eastern', 10, .10), ('East Midlands', 11, .08), ('London', 12, .09), ('North Wales and Mersey', 13, .05),
           ('West Midlands', 14, .08), ('North East', 15, .05), ('North West', 16, .09), ('North Scotland', 17, .03),
           ('South Scotland', 18, .06), ('South East', 19, .08), ('Southern', 20, .10), ('South Wales', 21, .04),
           ('South West', 22, .06), ('Yorkshire', 23, .09)]
SCOTLAND = {7, 8}
N_RESP = {0: 9150, 1: 9900}
N_JOIN = {0: 26140, 1: 28320}
CHANNELS = ['Direct web', 'Comparison site', 'Phone', 'Broker']
CH_P = {0: [.40, .32, .13, .15], 1: [.37, .36, .12, .15]}
B0, HALO = 1.30, 0.35
BETA_NEG, BETA_POS = 4.2, 1.0
ENGAGED = 0.10
PLATFORM, PRICE, CONTACT = -0.02, -0.03, -0.05
P_CUSTOMER = 0.55
CUST_BIAS, CUST_SD = -0.10, 0.28
REG_SD, SIX_SD = 0.10, 0.05
P_NOQTY0, PROP_SD = 0.05, 0.25
# standard variable rates: multipliers on each region's base, by effective date (the October 2025 step is +2 per cent)
SVT_STEPS = [(D(2024, 4, 1), 1.071), (D(2024, 7, 1), 1.000), (D(2024, 10, 1), 1.098), (D(2025, 1, 1), 1.112), (D(2025, 4, 1), 1.183),
             (D(2025, 7, 1), 1.101), (D(2025, 10, 1), 1.123), (D(2026, 1, 1), 1.125), (D(2026, 4, 1), 1.071)]
FIX_LAUNCH = [D(2024, 5, 1), D(2024, 9, 2), D(2024, 12, 2), D(2025, 3, 3), D(2025, 6, 2), D(2025, 9, 1), D(2025, 12, 1)]
PHASE1_START, PHASE1_END = D(2025, 9, 1), D(2025, 11, 2)
PHASE2_ASOF = D(2026, 11, 1)
# the extracts, each named for the span of the records it holds; the switching flows were pulled on 6 November 2026
F_QUOTES = 'quote_log_2024-05_2025-12.csv'
F_REGS = 'supply_registrations_2024-05_2025-12.csv'
F_FLOWS = 'switching_flows_2026-05-01_2026-11-05.csv'
FLOWS_LAST = D(2026, 11, 5)
F_DD = 'direct_debit_changes_2024-07_2026-06.csv'
DD_LAST = D(2026, 6, 30)


def mpan_core(dno, rng):
    body = [int(c) for c in '%02d' % dno] + list(rng.integers(0, 10, 10))
    w = [3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    chk = sum(a * b for a, b in zip(body, w)) % 11 % 10
    return ''.join(map(str, body)) + str(chk)


def region_bases(rng):
    out = []
    for i, (name, dno, _) in enumerate(REGIONS):
        out.append(dict(e_unit=round(22.40 * (1 + rng.uniform(-.035, .045)), 2),
                        e_sc=round(48.0 + rng.uniform(-6, 14), 2),
                        g_unit=round(5.81 * (1 + rng.uniform(-.03, .03)), 2),
                        g_sc=round(29.9 + rng.uniform(-1.2, 2.4), 2)))
    return out


def tariff_table(bases, rng):
    """Every tariff row: code, name, region index, effective from, to, the four rates (pence)."""
    rows = []
    for ri, b in enumerate(bases):
        for k, (start, m) in enumerate(SVT_STEPS):
            end = SVT_STEPS[k + 1][0] - dt.timedelta(days=1) if k + 1 < len(SVT_STEPS) else D(2026, 6, 30)
            rows.append(dict(code='SVT', name='Standard Variable', region=ri, start=start, end=end,
                             e_unit=round(b['e_unit'] * m, 2), e_sc=round(b['e_sc'] * m, 2),
                             g_unit=round(b['g_unit'] * m, 2), g_sc=round(b['g_sc'] * m, 2)))
    fix_factor = rng.uniform(0.985, 1.035, len(FIX_LAUNCH))
    for j, launch in enumerate(FIX_LAUNCH):
        m = svt_mult(launch) * fix_factor[j]
        code = 'FIX12-%s' % launch.strftime('%y%m')
        for ri, b in enumerate(bases):
            rows.append(dict(code=code, name='Fixed 12 %s' % launch.strftime('%b %Y'), region=ri, start=launch,
                             end=(FIX_LAUNCH[j + 1] - dt.timedelta(days=1)) if j + 1 < len(FIX_LAUNCH) else D(2026, 3, 1),
                             e_unit=round(b['e_unit'] * m, 2), e_sc=round(b['e_sc'] * m, 2),
                             g_unit=round(b['g_unit'] * m, 2), g_sc=round(b['g_sc'] * m, 2)))
    return rows


def svt_mult(day):
    m = SVT_STEPS[0][1]
    for start, mm in SVT_STEPS:
        if day >= start:
            m = mm
    return m


_INDEX = {}


def rates_for(table, code, region, day):
    """The rates of `code` for `region` in force on `day`; a fixed product keeps its launch rates."""
    key = id(table)
    if key not in _INDEX:
        idx = {}
        for r in table:
            idx.setdefault((r['code'], r['region']), []).append(r)
        for v in idx.values():
            v.sort(key=lambda r: r['start'])
        _INDEX.clear(); _INDEX[key] = idx
    best = None
    for r in _INDEX[key][(code, region)]:
        if r['start'] <= day and (code != 'SVT' or day <= r['end']):
            best = r
    return best


def cost_gbp(e, g, dual, r):
    return (e * r['e_unit'] + 365 * r['e_sc'] + dual * (g * r['g_unit'] + 365 * r['g_sc'])) / 100.0


def rand_date(rng, a, b, n):
    span = (b - a).days + 1
    return [a + dt.timedelta(days=int(k)) for k in rng.integers(0, span, n)]


def build(seed=SEED, beta_neg=BETA_NEG, beta_pos=BETA_POS, p_customer=P_CUSTOMER,
          cust_bias=CUST_BIAS, cust_sd=CUST_SD, n_scale=1.0, universe=False):
    """Respondent arrays (and, with universe=True, every joiner and the tariff table)."""
    rng = np.random.default_rng(seed)
    bases = region_bases(rng)
    table = tariff_table(bases, rng)
    reg_w = np.array([w for _, _, w in REGIONS]); reg_w = reg_w / reg_w.sum()
    joiners = []
    for t in (0, 1):
        nj = int(round(N_JOIN[t] * n_scale)); nr = int(round(N_RESP[t] * n_scale))
        y = 2024 + t
        start = rand_date(rng, D(y, 7, 1), D(y, 12, 31), nj)
        dual = rng.random(nj) < 0.74
        region = rng.choice(len(REGIONS), nj, p=reg_w)
        channel = rng.choice(len(CHANNELS), nj, p=CH_P[t])
        variable = rng.random(nj) < 0.55
        qdate = [s - dt.timedelta(days=int(k)) for s, k in zip(start, rng.integers(16, 31, nj))]
        e = rng.lognormal(log(2700), 0.50, nj)
        g = np.where(dual, rng.lognormal(log(11000), 0.45, nj), 0.0)
        e_reg = e * rng.lognormal(0, REG_SD, nj); g_reg = g * rng.lognormal(0, REG_SD, nj)
        e_six = e * rng.lognormal(0, SIX_SD, nj); g_six = g * rng.lognormal(0, SIX_SD, nj)
        if t == 0:
            noqty = rng.random(nj) < P_NOQTY0
            basis = np.where(noqty, 'property', 'industry')
            pe = rng.lognormal(0, PROP_SD, nj)
            qe = np.where(noqty, e * pe, e_reg); qg = np.where(noqty, g * pe, g_reg)
        else:
            cust = rng.random(nj) < p_customer
            basis = np.where(cust, 'customer', 'typical')
            ce = rng.lognormal(cust_bias, cust_sd, nj)
            qe = np.where(cust, e * ce, TYPICAL_E); qg = np.where(cust, g * ce, np.where(dual, TYPICAL_G, 0.0))
        qe = np.round(qe); qg = np.round(qg)
        tariff = []
        for i in range(nj):
            if variable[i]:
                tariff.append('SVT')
            else:
                launch = max(l for l in FIX_LAUNCH if l <= qdate[i])
                tariff.append('FIX12-%s' % launch.strftime('%y%m'))
        quoted = np.zeros(nj); cost6 = np.zeros(nj); cost_reg = np.zeros(nj)
        for i in range(nj):
            r = rates_for(table, tariff[i], int(region[i]), qdate[i])
            quoted[i] = round(cost_gbp(qe[i], qg[i], dual[i], r), 2)
            cost6[i] = cost_gbp(round(e_six[i]), round(g_six[i]), dual[i], r)
            cost_reg[i] = cost_gbp(round(e_reg[i]), round(g_reg[i]), dual[i], r)
        x = np.log(cost6 / quoted)
        x_cf = np.log(cost6 / cost_reg)
        resp = np.zeros(nj, bool); resp[rng.choice(nj, nr, replace=False)] = True
        joiners.append(dict(t=np.full(nj, t), start=np.array(start, dtype=object), qdate=np.array(qdate, dtype=object),
                            dual=dual, region=region, channel=channel, variable=variable, tariff=np.array(tariff),
                            e=e, g=g, e_reg=e_reg, g_reg=g_reg, e_six=e_six, g_six=g_six, basis=basis,
                            qe=qe, qg=qg, quoted=quoted, cost6=cost6, cost_reg=cost_reg, x=x, x_cf=x_cf, resp=resp))
    J = {k: np.concatenate([j[k] for j in joiners]) for k in joiners[0]}
    # respondents: satisfaction truth
    m = J['resp']; n = int(m.sum())
    R = {k: v[m] for k, v in J.items()}
    t = R['t']
    lat = rng.normal(0, 1, n)
    dis = beta_neg * np.maximum(R['x'], 0) + beta_pos * np.minimum(R['x'], 0)
    dis_cf = beta_neg * np.maximum(R['x_cf'], 0) + beta_pos * np.minimum(R['x_cf'], 0)
    engaged = (R['basis'] == 'customer')
    newplat = (t == 1)
    contacted = rng.random(n) < np.where(t == 0, 0.30, 0.34)
    price_hit = R['variable'] & (t == 1)
    other = PLATFORM * newplat + PRICE * price_hit + CONTACT * (contacted & (t == 1))
    z = B0 + HALO * lat + ENGAGED * engaged - dis + other
    P = lambda zz: 1 / (1 + np.exp(-zz))
    p = P(z); sat = rng.random(n) < p
    R.update(lat=lat, engaged=engaged, newplat=newplat, contacted=contacted, z=z, p=p, sat=sat,
             p_cf_quote=np.where(t == 1, P(z + dis - dis_cf - ENGAGED * engaged), p),
             p_cf_plat=P(z - PLATFORM * newplat), p_cf_price=P(z - PRICE * price_hit),
             p_cf_contact=P(z - CONTACT * (contacted & (t == 1))))
    over = np.maximum(R['x'], 0)
    def rate5(mu, sd=0.55):
        v = mu + 0.45 * lat + rng.normal(0, sd, n)
        return np.clip(np.rint(v), 1, 5).astype(int)
    R.update(bill_accuracy=rate5(4.0 - 2.4 * over - 0.10 * newplat),
             bill_clarity=rate5(3.9 - 0.8 * over - 0.15 * newplat),
             value=rate5(3.5 - 1.7 * over - 0.15 * price_hit),
             contact_ease=rate5(3.8 - 0.35 * (contacted & (t == 1))),
             resolution=rate5(3.7 - 0.25 * (contacted & (t == 1)) - 0.4 * over),
             app=rate5(3.7 - 0.08 * newplat))
    # overall answer on the 1 to 5 scale, consistent with sat (4 or 5 when satisfied)
    u = rng.random(n)
    R['overall'] = np.where(sat, np.where(u < 0.42 + 0.25 * P(lat), 5, 4), np.where(u < 0.55, 3, np.where(u < 0.82, 2, 1)))
    # response dates: six months after supply start, inside the half-year window
    rd = []
    for s, tt in zip(R['start'], t):
        d0 = s + dt.timedelta(days=182 + int(rng.integers(0, 22)))
        lo, hi = D(2025 + int(tt), 1, 1), D(2025 + int(tt), 6, 30)
        rd.append(min(max(d0, lo), hi))
    R['response'] = np.array(rd, dtype=object)
    # Direct Debit: first payment from the industry quantity at registration, review about five months on
    R['dd0'] = np.round(R['cost_reg'] / 12)
    R['dd1'] = np.zeros(n)
    for i in range(n):
        rv = R['start'][i] + dt.timedelta(days=150)
        r = rates_for(table, R['tariff'][i], int(R['region'][i]), rv)
        R['dd1'][i] = round(cost_gbp(round(R['e_six'][i]), round(R['g_six'][i]), R['dual'][i], r) / 12)
    if universe:
        return dict(R=R, J=J, table=table, bases=bases, rng=rng)
    return R
