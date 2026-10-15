"""The world before any extract is cut: customs exchange rates by day, each gateway's inbound international
shipments by month, the routing of every shipment, and the high-value check population of the twelve months to
September 2026 shipment by shipment. Everything downstream (records, documents, the golden) reads from here."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

import numpy as np

import common as K

# ---------------------------------------------------------------------------------------------------- rates by day
FED_HOLIDAYS = set()
for y in range(2021, 2028):
    FED_HOLIDAYS |= {dt.date(y, 1, 1), dt.date(y, 7, 1), dt.date(y, 12, 25), dt.date(y, 12, 26)}
    # Good Friday (computus), Victoria Day, Labour Day, Thanksgiving, Remembrance Day
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = ((h + l_ - 7 * m + 114) % 31) + 1
    FED_HOLIDAYS.add(dt.date(y, month, day) - dt.timedelta(days=2))
    v = dt.date(y, 5, 24)
    while v.weekday() != 0:
        v -= dt.timedelta(days=1)
    FED_HOLIDAYS.add(v)
    lab = dt.date(y, 9, 1)
    while lab.weekday() != 0:
        lab += dt.timedelta(days=1)
    FED_HOLIDAYS.add(lab)
    th = dt.date(y, 10, 1)
    while th.weekday() != 0:
        th += dt.timedelta(days=1)
    FED_HOLIDAYS.add(th + dt.timedelta(days=7))
    FED_HOLIDAYS.add(dt.date(y, 11, 11))


def business_day(d):
    return d.weekday() < 5 and d not in FED_HOLIDAYS


def daily_rates():
    """The customs exchange rate in force on each calendar day, by currency: one published each business day around
    the month's average (a slow wander inside the month), carried over weekends and holidays."""
    out = {c: {} for c in K.CURRENCIES}
    for c in K.CURRENCIES:
        r = K.rng("rates", c)
        last = None
        for i, (y, m) in enumerate(K.HIST_MONTHS):
            n = K.days_in(y, m)
            target = K.monthly_rate(c, i)
            walk = np.cumsum(r.normal(0, 0.0016, n))
            walk = walk - walk.mean()
            for d0 in range(n):
                day = dt.date(y, m, d0 + 1)
                if c == "CAD":
                    out[c][day] = 1.0
                    continue
                if business_day(day) or last is None:
                    v = K.round_dp(target * math.exp(walk[d0]), K.RATE_DP[c])
                    last = v
                out[c][day] = last
        # the first days of the plan's base carry into October 2026 for the pull
        day = K.HIST_END + dt.timedelta(days=1)
        while day <= dt.date(2026, 10, 9):
            out[c][day] = out[c][K.HIST_END] if c != "CAD" else 1.0
            day += dt.timedelta(days=1)
    return out


# ---------------------------------------------------------------------------------------------------- the routing
def segment_formal_prob(g, seg, rate):
    """Share of a segment's shipments routed to a formal entry at one rate (OGD shipments always): the goods priced in
    the invoice currency cross the line with the rate, the goods priced in CAD hold their CAD value."""
    lam = K.lcp_share(g, seg["cur"])
    x = K.LINE_CAD / rate
    if seg["kind"] == "ln":
        mu, s = seg["p"]
        p_inv = 1.0 - K.phi((math.log(x) - mu) / s)
        p_cad = 1.0 - K.phi((math.log(K.LINE_CAD) - mu - math.log(K.ref_rate(seg["cur"]))) / s) if lam else 0.0
    else:
        tot = sum(w for _, w in seg["p"])
        p_inv = sum(w for v, w in seg["p"] if v * rate > K.LINE_CAD) / tot
        tc = sum(w for _, w in seg["cp"])
        p_cad = sum(w for v, w in seg["cp"] if v > K.LINE_CAD) / tc
    p_val = (1.0 - lam) * p_inv + lam * p_cad
    return seg["ogd"] + (1.0 - seg["ogd"]) * p_val


def gateway_formal_share(g, rates_by_cur):
    return sum(seg["share"] * segment_formal_prob(g, seg, rates_by_cur[seg["cur"]]) for seg in K.SEGMENTS[g])


WEEKDAY_W = [1.14, 1.12, 1.10, 1.10, 1.08, 0.36, 0.10]


@dataclass
class Shipment:
    waybill: str
    gw: str
    local: dt.datetime            # local release time at the gateway
    utc: dt.datetime
    cur: str
    value: float                  # value for duty in the invoice currency
    rate: float                   # customs rate of the date
    vfd_cad: float
    ogd: str                      # OGD program code, '' where none
    hs: str
    origin: str
    importer: str
    seg: int
    route: str                    # FORMAL or CLVS
    entry: str = ""
    cad_priced: bool = False      # the truth, never shipped: the goods' price is set in CAD (the value in CAD holds)
    price_cad: float = 0.0        # that CAD price


@dataclass
class World:
    rates: dict = field(default_factory=dict)
    volume: dict = field(default_factory=dict)        # (g, y, m) -> inbound international shipments
    formal_hist: dict = field(default_factory=dict)   # (g, y, m) -> formal entries released in the month
    ships: list = field(default_factory=list)         # the high-value check population, base year
    prior: list = field(default_factory=list)         # the same, the year before the base
    amended: list = field(default_factory=list)


def monthly_volume():
    out = {}
    centre = K.HIST_MONTHS.index((2026, 3)) + 0.5
    for g in K.GATEWAYS:
        r = K.rng("volume", g)
        for i, (y, m) in enumerate(K.HIST_MONTHS):
            t = (i - centre) / 12.0
            covid = 1.0
            if (y, m) <= (2021, 6):
                covid = 0.97
            lvl = K.BASE_LEVEL[g] * (1 + K.TREND[g]) ** t * K.season(m) * covid
            out[(g, y, m)] = int(round(lvl * math.exp(r.normal(0, 0.012))))
    return out


def day_weights(y, m):
    n = K.days_in(y, m)
    w = np.array([WEEKDAY_W[dt.date(y, m, d + 1).weekday()] *
                  (0.25 if dt.date(y, m, d + 1) in FED_HOLIDAYS else 1.0) for d in range(n)])
    return w / w.sum()


def expected_formal(g, y, m, rates):
    w = day_weights(y, m)
    n = K.days_in(y, m)
    tot = 0.0
    for d in range(n):
        day = dt.date(y, m, d + 1)
        rb = {c: rates[c][day] for c in K.CURRENCIES}
        tot += w[d] * gateway_formal_share(g, rb)
    return tot


# ---------------------------------------------------------------------------------------------------- goods and people
HS = {
    "US": [("8471.30.00.00", ""), ("8473.30.10.00", ""), ("8517.62.00.90", ""), ("8481.80.00.90", ""),
           ("8483.40.90.00", ""), ("8708.99.99.90", ""), ("9018.90.90.90", ""), ("8504.40.90.90", ""),
           ("9506.91.00.90", ""), ("8414.59.00.90", "")],
    "EU": [("8516.71.00.00", ""), ("8711.60.00.00", ""), ("4202.21.00.00", ""), ("6110.11.00.00", ""),
           ("9102.11.00.00", ""), ("8509.40.00.00", ""), ("9403.60.00.90", ""), ("6403.99.00.00", "")],
    "GB": [("6109.10.00.10", ""), ("4202.22.00.00", ""), ("9506.31.00.00", ""), ("8518.30.00.00", "")],
    "CN": [("8517.13.00.00", ""), ("8543.70.00.90", ""), ("8504.40.90.90", ""), ("9405.42.00.00", ""),
           ("8528.52.00.00", ""), ("8471.60.00.90", "")],
    "JP": [("9006.59.00.00", ""), ("8525.89.00.00", ""), ("9002.11.00.00", ""), ("8542.31.00.00", "")],
    "AS": [("9006.59.00.00", ""), ("8525.89.00.00", ""), ("8471.30.00.00", ""), ("8528.52.00.00", "")],
}
OGD_GOODS = [("2101.11.00.00", "CFIA"), ("1905.90.90.00", "CFIA"), ("0901.21.00.00", "CFIA"),
             ("3304.99.00.00", "HC-COS"), ("3004.90.00.99", "HC-DRUG"), ("2106.90.99.00", "HC-NHP"),
             ("0602.90.00.00", "CFIA"), ("3808.94.90.00", "HC-PMRA"), ("9504.50.00.00", "HC-CPS"),
             ("8517.62.00.90", "ISED-RE")]
ORIGIN = {"US": [("US", 1.0)],
          "EU": [("DE", 0.31), ("FR", 0.24), ("IT", 0.21), ("NL", 0.12), ("ES", 0.12)],
          "GB": [("GB", 1.0)],
          "CN": [("CN", 0.86), ("HK", 0.14)],
          "JP": [("JP", 1.0)],
          "AS": [("TW", 0.38), ("KR", 0.27), ("CN", 0.22), ("HK", 0.13)]}


def importer_pool(g, r):
    """Importers by gateway: business numbers (nine digits, the RM import account suffix) the clearance system bills
    duties to; a few large accounts and a long tail."""
    n = {"YYZ": 2600, "YUL": 1500, "YVR": 1700, "YYC": 900, "YWG": 1000}[g]
    base = {"YYZ": 7, "YUL": 1, "YVR": 8, "YYC": 4, "YWG": 2}[g]
    out = set()
    while len(out) < n:
        bn = "%d%08d" % (base, int(r.integers(0, 10 ** 8)))
        out.add("%sRM%04d" % (bn, int(r.choice([1, 1, 1, 2, 3]))))
    pool = sorted(out)
    w = 1.0 / (np.arange(1, n + 1) ** 0.95)
    return pool, w / w.sum()


def waybill_check(digits9):
    return str(int(digits9) % 7)


def sample_lognorm_above(r, mu, s, lo, size):
    """Values of a lognormal above lo (inverse cdf on the truncated tail)."""
    from scipy.special import ndtri
    if size == 0:
        return np.zeros(0)
    p0 = K.phi((math.log(lo) - mu) / s)
    u = r.uniform(p0, 1.0, size)
    return np.exp(mu + s * ndtri(np.clip(u, 1e-12, 1 - 1e-12)))


def local_to_utc(g, t_local):
    tz = ZoneInfo(K.TZ[g])
    return t_local.replace(tzinfo=tz).astimezone(dt.timezone.utc).replace(tzinfo=None)


RELEASE_HOURS = np.array([0.6, 0.4, 0.3, 0.3, 0.6, 1.4, 3.2, 5.0, 6.4, 7.0, 7.2, 7.0, 6.4, 6.6, 6.8, 6.6, 6.0, 5.2, 4.4,
                          3.6, 2.8, 2.2, 1.6, 1.0])
RELEASE_HOURS = RELEASE_HOURS / RELEASE_HOURS.sum()


def cur_round(cur, x):
    return np.round(x) if cur == "JPY" else np.round(x, 2)


def invoice_of(price_cad, rate, cur):
    """The invoice value of goods priced in CAD: the price converted at the day's rate, to the currency's unit."""
    v = price_cad / rate
    return float(K.round_dp(v, 0)) if cur == "JPY" else K.round_dp(v, 2)


def off_line(vals, rr):
    """Values moved two units of CAD clear of the line where they land within CAD 0.75 of it at the rate rr."""
    near = np.abs(vals * rr - K.LINE_CAD) < 0.75
    return np.where(near, vals + np.where(vals * rr >= K.LINE_CAD, 2.0, -2.0) / rr, vals)


def catalogue(g, si, seg, rates, pool, pw, big):
    """An importer's standing consignments in one segment: the same goods sent again and again at the same price.
    Goods priced in the invoice currency keep their invoice value; goods priced in CAD keep their CAD price and are
    invoiced at it converted at the day's rate. A background segment's values come from its own distribution above the
    check's floor (at the two years' average rate for the invoice-currency prices: a consignment under the floor on a
    day of a lower rate is released unchecked), clear of the line at the plan's rate; a price-point segment's from its
    lists, most of them the gateway's large accounts. Both kinds of price recur at the same rate per consignment."""
    r = K.rng("catalogue", g, si)
    cur = seg["cur"]
    lam = K.lcp_share(g, cur)
    lane = seg["lane"]
    ocs = ORIGIN[lane]

    def items(vals, pp=False):
        n = len(vals)
        if pp:
            # an importer's price-point goods are one line of goods under one tariff item
            idx = [int(r.integers(0, len(big))) if r.random() < 0.7 else int(r.choice(len(pool), p=pw))
                   for _ in range(n)]
            imps = [pool[i] for i in idx]
            hss = [HS[lane][(i * 7 + si) % len(HS[lane])][0] for i in idx]
        else:
            imps = [pool[i] for i in r.choice(len(pool), size=n, p=pw)]
            hss = [HS[lane][i][0] for i in r.integers(0, len(HS[lane]), n)]
        ors = [ocs[i][0] for i in r.choice(len(ocs), size=n, p=[x for _, x in ocs])]
        w = 1.0 / (np.arange(1, n + 1) + 4.0) ** 0.55
        w = w[r.permutation(n)]
        return dict(vals=vals, imps=imps, hss=hss, ors=ors, w=w / w.sum())

    out = {}
    if seg["kind"] == "pp":
        vol2 = sum(W_VOL_HINT[g][m] for m in range(12)) * 2.0 * seg["share"]
        for key, plist, part in (("inv", seg["p"], 1.0 - lam), ("cad", seg["cp"], lam)):
            if part <= 0:
                continue
            n = max(2, int(round(vol2 * part / K.REPEATS_PER_ITEM)))
            pv = np.array([v for v, _ in plist], float)
            pw_ = np.array([w_ for _, w_ in plist], float)
            out[key] = items(r.choice(pv, size=n, p=pw_ / pw_.sum()), pp=True)
        return out
    days = [d for d in rates[cur] if K.PRIOR_START <= d <= K.BASE_END]
    r_mean = sum(rates[cur][d] for d in days) / len(days)
    mu, s_ = seg["p"]
    vol2 = sum(W_VOL_HINT[g][m] for m in range(12)) * 2.0 * seg["share"] * (1 - seg["ogd"])
    lo = K.CHECK_FLOOR_CAD / r_mean
    mid = vol2 * (1 - lam) * (1.0 - K.phi((math.log(lo) - mu) / s_))
    n = max(2, int(round(K.REPEAT_SHARE * mid / K.REPEATS_PER_ITEM)))
    vals = cur_round(cur, sample_lognorm_above(r, mu, s_, lo, n))
    vals = cur_round(cur, off_line(vals, K.PLAN_RATE[cur]))
    out["inv"] = items(vals)
    if lam:
        muc = mu + math.log(K.ref_rate(cur))
        mid = vol2 * lam * (1.0 - K.phi((math.log(K.CHECK_FLOOR_CAD) - muc) / s_))
        n = max(2, int(round(K.REPEAT_SHARE * mid / K.REPEATS_PER_ITEM)))
        pc = np.round(sample_lognorm_above(r, muc, s_, K.CHECK_FLOOR_CAD + 1.0, n), 2)
        pc = np.round(off_line(pc, 1.0), 2)
        out["cad"] = items(pc)
    return out


W_VOL_HINT = {}


def _window(W, g, months_, r, pool, pw, big, cats, out, seen=None):
    """Every shipment the high-value check covers (CAD 2,500 or more, or OGD) at gateway g over the months given.
    seen: the year before's consignment keys (importer, tariff item, currency, and the invoice value or the CAD value);
    a shipment of the base year that would repeat one on both (the same goods on a day of the same rate) is not drawn,
    so a repeat consignment shows one price or the other."""
    rates = W.rates
    for (y, m) in months_:
        vol = W.volume[(g, y, m)]
        w = day_weights(y, m)
        for d in range(K.days_in(y, m)):
            day = dt.date(y, m, d + 1)
            n_day = vol * w[d]
            for si, seg in enumerate(K.SEGMENTS[g]):
                cur = seg["cur"]
                rate = rates[cur][day]
                pr = K.PLAN_RATE[cur]
                lo = K.CHECK_FLOOR_CAD / rate
                lam = K.lcp_share(g, cur)
                vals, ogds, rep, cadp = [], [], [], []
                if seg["kind"] == "ln":
                    mu, s = seg["p"]
                    # goods priced in the invoice currency
                    p_hv = 1.0 - K.phi((math.log(lo) - mu) / s)
                    k = int(r.poisson(n_day * seg["share"] * (1 - seg["ogd"]) * (1 - lam) * p_hv))
                    k_rep = int(r.binomial(k, K.REPEAT_SHARE)) if k else 0
                    fresh = cur_round(cur, sample_lognorm_above(r, mu, s, lo, k - k_rep))
                    for rr in (rate, pr):
                        fresh = cur_round(cur, off_line(fresh, rr))
                    vals += list(fresh)
                    ogds += [""] * len(fresh)
                    rep += [-1] * len(fresh)
                    cadp += [0.0] * len(fresh)
                    if k_rep:
                        c = cats[si]["inv"]
                        for i in r.choice(len(c["vals"]), size=k_rep, p=c["w"]):
                            v = float(c["vals"][i])
                            if K.round_dp(v * rate, 2) == K.LINE_CAD:
                                continue
                            vals.append(v)
                            ogds.append("")
                            rep.append(int(i))
                            cadp.append(0.0)
                    # goods priced in CAD, invoiced at the price converted at the day's rate
                    if lam:
                        muc = mu + math.log(K.ref_rate(cur))
                        p_hc = 1.0 - K.phi((math.log(K.CHECK_FLOOR_CAD + 1.0) - muc) / s)
                        kc = int(r.poisson(n_day * seg["share"] * (1 - seg["ogd"]) * lam * p_hc))
                        kc_rep = int(r.binomial(kc, K.REPEAT_SHARE)) if kc else 0
                        pf = np.round(sample_lognorm_above(r, muc, s, K.CHECK_FLOOR_CAD + 1.0, kc - kc_rep), 2)
                        pf = np.round(off_line(pf, 1.0), 2)
                        for P in pf:
                            vals.append(invoice_of(float(P), rate, cur))
                            ogds.append("")
                            rep.append(-1)
                            cadp.append(float(P))
                        if kc_rep:
                            c = cats[si]["cad"]
                            for i in r.choice(len(c["vals"]), size=kc_rep, p=c["w"]):
                                P = float(c["vals"][i])
                                vals.append(invoice_of(P, rate, cur))
                                ogds.append("")
                                rep.append(int(i))
                                cadp.append(P)
                    ko = int(r.poisson(n_day * seg["share"] * seg["ogd"]))
                    omu, os_ = seg["ogd_ln"]
                    ov = np.exp(r.normal(omu, os_, ko))
                    vals += list(cur_round(cur, ov))
                    ogds += ["OGD"] * ko
                    rep += [-1] * ko
                    cadp += [0.0] * ko
                else:
                    k = int(r.poisson(n_day * seg["share"]))
                    kc = int(r.binomial(k, lam)) if (k and lam) else 0
                    if k - kc:
                        c = cats[si]["inv"]
                        for i in r.choice(len(c["vals"]), size=k - kc, p=c["w"]):
                            vals.append(float(c["vals"][i]))
                            rep.append(int(i))
                            cadp.append(0.0)
                    if kc:
                        c = cats[si]["cad"]
                        for i in r.choice(len(c["vals"]), size=kc, p=c["w"]):
                            P = float(c["vals"][i])
                            vals.append(invoice_of(P, rate, cur))
                            rep.append(int(i))
                            cadp.append(P)
                    ogds += [""] * k
                if not vals:
                    continue
                vals = np.array(vals, float)
                ogd_mask = np.array([o == "OGD" for o in ogds])
                rep = np.array(rep)
                cadp = np.array(cadp, float)
                cads = np.array([K.round_dp(v * rate, 2) for v in vals])
                keep = ogd_mask | (cads >= K.CHECK_FLOOR_CAD)
                vals, cads, ogd_mask, rep, cadp = vals[keep], cads[keep], ogd_mask[keep], rep[keep], cadp[keep]
                k = len(vals)
                if k == 0:
                    continue
                hours = r.choice(24, size=k, p=RELEASE_HOURS)
                mins = r.integers(0, 60, k)
                secs = r.integers(0, 60, k)
                lane = seg["lane"]
                hs_i = r.integers(0, len(HS[lane]), k)
                og_i = r.integers(0, len(OGD_GOODS), k)
                ocs = ORIGIN[lane]
                or_i = r.choice(len(ocs), size=k, p=[x for _, x in ocs])
                imp_i = r.choice(len(pool), size=k, p=pw)
                for j in range(k):
                    t_local = dt.datetime(y, m, d + 1, int(hours[j]), int(mins[j]), int(secs[j]))
                    lc = cadp[j] > 0
                    if ogd_mask[j]:
                        hs, prog = OGD_GOODS[int(og_i[j])]
                        org, imp = ocs[int(or_i[j])][0], pool[int(imp_i[j])]
                    elif rep[j] >= 0:
                        c = cats[si]["cad" if lc else "inv"]
                        hs, prog, org, imp = c["hss"][rep[j]], "", c["ors"][rep[j]], c["imps"][rep[j]]
                    else:
                        hs, prog = HS[lane][int(hs_i[j])][0], ""
                        org = ocs[int(or_i[j])][0]
                        imp = pool[int(imp_i[j])]
                    v, cad = float(vals[j]), float(cads[j])
                    if lc and not prog and abs(K.round_dp(v * pr, 2) - K.LINE_CAD) < 0.75:
                        continue
                    if seen is not None and not prog and cur != "CAD" and (
                            ((imp, hs, cur, v) in seen["inv"] and (imp, hs, cur, cad) in seen["cad"]) or
                            ((imp, cur, v) in seen["inv"] and (imp, cur, cad) in seen["cad"])):
                        continue
                    route = "FORMAL" if (prog or cad > K.LINE_CAD) else "CLVS"
                    out.append(Shipment(waybill="", gw=g, local=t_local, utc=local_to_utc(g, t_local),
                                        cur=cur, value=v, rate=rate, vfd_cad=cad, ogd=prog, hs=hs, origin=org,
                                        importer=imp, seg=si, route=route, cad_priced=bool(lc and not prog),
                                        price_cad=float(cadp[j]) if lc else 0.0))


def consignment_keys(ships, g):
    """The consignment keys of a year's shipments at gateway g, with the tariff item and without it."""
    inv, cad = set(), set()
    for s in ships:
        if s.gw == g and not s.ogd and s.cur != "CAD":
            inv |= {(s.importer, s.hs, s.cur, s.value), (s.importer, s.cur, s.value)}
            cad |= {(s.importer, s.hs, s.cur, s.vfd_cad), (s.importer, s.cur, s.vfd_cad)}
    return dict(inv=inv, cad=cad)


def simulate():
    W = World()
    W.rates = daily_rates()
    W.volume = monthly_volume()
    rates = W.rates
    # the history's formal entries before the extracts on file: every month from the routing at that month's rates
    for g in K.GATEWAYS:
        r = K.rng("formal_hist", g)
        for (y, m) in K.HIST_MONTHS:
            if (y, m) >= (K.PRIOR_START.year, K.PRIOR_START.month):
                continue
            lam = W.volume[(g, y, m)] * expected_formal(g, y, m, rates)
            W.formal_hist[(g, y, m)] = int(r.poisson(lam))
    # the two years on file shipment by shipment: the year before the base (the 2026 review's extracts) and the base
    W.prior = []
    for g in K.GATEWAYS:
        W_VOL_HINT[g] = [W.volume[(g, y, m)] for (y, m) in K.BASE_MONTHS]
        pool, pw = importer_pool(g, K.rng("importers", g))
        big = pool[:12]
        cats = {si: catalogue(g, si, seg, rates, pool, pw, big) for si, seg in enumerate(K.SEGMENTS[g])}
        _window(W, g, K.PRIOR_MONTHS, K.rng("ships_prior", g), pool, pw, big, cats, W.prior)
        _window(W, g, K.BASE_MONTHS, K.rng("ships", g), pool, pw, big, cats, W.ships,
                seen=consignment_keys(W.prior, g))
    # waybills: ten digits with a mod-7 check digit, in release order across the network
    allships = sorted(W.prior + W.ships, key=lambda s: (s.utc, s.gw, s.value))
    r = K.rng("waybills")
    used = set()
    for s in allships:
        while True:
            body = "%09d" % int(r.integers(100000000, 999999999))
            if body not in used:
                used.add(body)
                break
        s.waybill = body + waybill_check(body)
    # formal entry transaction numbers: Larchwood's 5-digit account and a 9-digit sequence, in release order per desk
    acct = "13947"
    seq = {"YYZ": 103800000, "YUL": 303800000, "YVR": 503800000, "YYC": 603800000, "YWG": 703800000}
    for s in allships:
        if s.route == "FORMAL":
            seq[s.gw] += 1 + int(r.random() < 0.02)
            s.entry = acct + "%09d" % seq[s.gw]
    W.ships.sort(key=lambda s: (s.utc, s.gw, s.value))
    W.prior.sort(key=lambda s: (s.utc, s.gw, s.value))
    # the gateway report counts the extracts' formal releases in the two years on file
    for g in K.GATEWAYS:
        cnt = {}
        for s in W.prior + W.ships:
            if s.gw == g and s.route == "FORMAL":
                key = (s.local.year, s.local.month)
                cnt[key] = cnt.get(key, 0) + 1
        for (y, m) in K.PRIOR_MONTHS + K.BASE_MONTHS:
            W.formal_hist[(g, y, m)] = cnt.get((y, m), 0)
    # a few shipments amended after release (a corrected invoice), route unchanged at every rate on file
    r = K.rng("amend")
    cand = [s for s in W.ships if not s.ogd and s.local.date() < dt.date(2026, 6, 20)]
    picks = r.choice(len(cand), size=14, replace=False)
    for k in sorted(picks):
        s = cand[k]
        f = float(r.choice([0.97, 0.98, 1.02, 1.03]))
        nv = round(s.value * f, 2)
        ok = all(((nv * rr > K.LINE_CAD) == (s.value * rr > K.LINE_CAD)) and abs(nv * rr - K.LINE_CAD) > 0.75
                 for rr in (s.rate, K.PLAN_RATE[s.cur])) and nv * s.rate >= K.CHECK_FLOOR_CAD
        if ok:
            W.amended.append((s, nv))
    return W
