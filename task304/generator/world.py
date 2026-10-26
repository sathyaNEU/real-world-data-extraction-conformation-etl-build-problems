"""The Society's four books, month by month from January 2010 to September 2026.

Borrowers miss payments at a hazard set by their budget headroom against the payment, their equity, the loan's age
and the economy. When a fixed rate ends the borrower redeems or takes a product transfer at the month's transfer rate;
from July 2023 an owner-occupier whose new payment breaks their budget asks for a term extension at the switch and
gets one (the Charter), which lowers the payment and keeps the account up to date, but the broken budget falls back
into arrears after a few months at a much higher hazard. Accounts five payments behind go to litigation (owner
occupiers) or to an LPA receiver (buy to let); a litigation spell ends in possession, a cure, a sale by the borrower or,
for shared ownership, a buy-back by the housing association. In 2024 the support team pilot worked
with half the borrowers who first fell two payments behind, allocated on the parity of the account number.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P


def ym(y, mo=1):
    return y * 12 + (mo - 1)


SNAP = ym(2026, 9)
HIST0 = ym(2019, 1)
START = ym(2010, 1)

PT_POINTS = [(ym(2010), 3.4), (ym(2014), 2.6), (ym(2017), 1.8), (ym(2020), 1.5), (ym(2021, 6), 1.2),
             (ym(2022, 1), 1.5), (ym(2022, 6), 2.6), (ym(2022, 10), 5.6), (ym(2023, 1), 4.8), (ym(2023, 7), 6.2),
             (ym(2023, 12), 5.0), (ym(2024, 6), 4.6), (ym(2025, 1), 4.2), (ym(2025, 12), 3.9), (ym(2026, 6), 3.8),
             (ym(2030), 3.8)]


def market_rate(m):
    """the two-year fix at 75 per cent loan to value, per cent a year, by month"""
    xs = np.array([p[0] for p in PT_POINTS], float)
    return np.interp(m, xs, np.array([p[1] for p in PT_POINTS]))


def hpi(m, region):
    """house price index by month and area (January 2019 = 100)"""
    base = np.interp(m, [ym(2010), ym(2015), ym(2019), ym(2020, 6), ym(2022, 9), ym(2023, 9), ym(2025, 1), ym(2030)],
                     [82, 88, 100, 102, 124, 118, 122, 133])
    tilt = np.array([1.00, 0.97, 1.03, 0.95, 1.01, 0.99])[region]
    return 100 + (base - 100) * tilt


def annuity(bal, rate_pct, n):
    r = rate_pct / 1200.0
    n = np.maximum(n, 1)
    return np.where(r > 0, bal * r / (1 - (1 + r) ** (-n)), bal / n)


FIX5 = dict(FTB=1.0, HLTV=0.85, SO=0.5, BTL=0.6)
OW = dict(FTB=[0.05, 0.10, 0.85])

PARAMS = dict(b0=0.0010, beta_s=3.0, sigma=0.35, d_rate=0.0006, d_mean=60, d_mult=26.0,
              ext_thresh=0.05, ext_p_d=0.97, ext_p_ok=0.01, coll_ext_p=0.06,
              ltv_k=3.0, slack_mu=1.42, slack_sd=0.16, sig0=0.8, beta_sig=4.0, ext_sig=1.0, hon=(8, 15),
              slack_2021=1.06, beta_s_btl=0.5, btl_h=0.4, btl_lit=0.45, oo_lit=0.45,
              book_h=(1.0, 2.0, 1.0, 1.0), pilot_rescue=0.3)


def originate(rng):
    rows = []

    def add(book, m0, m1, n, ltv_lo, ltv_hi, val_mu, terms, io_share, fix5_share):
        if book in OW:
            months = np.arange(m0, m1 + 1)
            w = np.array([OW[book][(mm // 12) - (m0 // 12)] for mm in months], float)
            om = rng.choice(months, n, p=w / w.sum())
        else:
            om = rng.integers(m0, m1 + 1, n)
        rows.append(pd.DataFrame(dict(
            book=book, orig_m=om, ltv0=rng.uniform(ltv_lo, ltv_hi, n),
            value0=np.exp(rng.normal(np.log(val_mu), 0.28, n)), term0=rng.choice(terms, n),
            io=rng.random(n) < io_share, fix5=rng.random(n) < fix5_share, region=rng.integers(0, 6, n),
            joint=rng.random(n) < (0.18 if book == "FTB" else 0.45 if book in ("HLTV", "BTL") else 0.30))))
    add("FTB", ym(2019, 1), ym(2021, 6), 28000, 0.89, 0.95, 205000, [360, 420, 420, 480], 0.0, FIX5["FTB"])
    add("HLTV", ym(2022, 7), ym(2024, 12), 19000, 0.90, 0.95, 245000, [300, 360, 420], 0.0, FIX5["HLTV"])
    add("SO", ym(2012, 1), ym(2026, 8), 17500, 0.70, 0.95, 95000, [300, 360], 0.0, FIX5["SO"])
    add("BTL", ym(2010, 1), ym(2026, 8), 28000, 0.55, 0.75, 210000, [240, 300], 0.86, FIX5["BTL"])
    df = pd.concat(rows, ignore_index=True)
    df["loan0"] = (df.ltv0 * df.value0 / 100).round() * 100
    return df.sort_values(["orig_m", "book"], kind="stable").reset_index(drop=True)


class World:
    def __init__(self, seed=P.SEED):
        self.p = dict(PARAMS)
        rng = self.rng = np.random.default_rng(seed)
        a = originate(rng)
        n = len(a)
        self.a, self.n = a, n
        s = self.p["sigma"]
        self.frail = np.exp(rng.normal(-s * s / 2, s, n))
        self.dist = np.zeros(n, bool)
        self.even = rng.random(n) < 0.5
        mu = np.where((a.book.to_numpy() == "FTB") & (a.orig_m.to_numpy() >= ym(2021, 1)), self.p["slack_2021"],
                      self.p["slack_mu"])
        self.slack = np.exp(rng.normal(np.log(mu), self.p["slack_sd"], n))
        self.d_end = np.full(n, -1)
        self.d_start = np.full(n, -1)
        self.book = a.book.map({b: i for i, b in enumerate(P.BOOKS)}).to_numpy()
        self.orig_m = a.orig_m.to_numpy()
        self.region = a.region.to_numpy()
        self.io = a.io.to_numpy()
        self.value0 = a.value0.to_numpy()
        self.loan0 = a.loan0.to_numpy().astype(float)
        self.term0 = a.term0.to_numpy()
        prem = np.select([self.book == 3, a.ltv0.to_numpy() > 0.9, a.ltv0.to_numpy() > 0.85, self.book == 2],
                         [0.7, 0.8, 0.4, 0.3], 0.0)
        self.rate = market_rate(self.orig_m) + prem
        self.rem = self.term0.astype(float)
        self.bal = self.loan0.copy()
        self.pay = np.where(self.io, self.bal * self.rate / 1200, annuity(self.bal, self.rate, self.rem))
        self.pay0 = self.pay.copy()
        self.fix_end = self.orig_m + np.where(a.fix5.to_numpy(), 60, 24)
        self.status = np.zeros(n, int)          # 0 live, 1 redeemed, 2 possessed
        self.k = np.zeros(n, int)
        self.lit = np.zeros(n, bool)
        self.lit_m = np.full(n, -1)
        self.poss_m = np.full(n, -1)
        self.close_m = np.full(n, -1)
        self.ext_m = np.full(n, -1)
        self.ext_kind = np.zeros(n, int)
        self.n_ext = np.zeros(n, int)
        self.prod = np.zeros(n, int)
        self.pip = np.zeros(n, bool)            # taken into possession, not yet sold
        self.poss_done_m = np.full(n, -1)
        self.poss_day = np.zeros(n, int)
        self.sale_m = np.full(n, -1)
        self.sale_day = np.zeros(n, int)
        self.cap_m = np.full(n, -1)
        self.pilot_ref = np.full(n, -1)
        self.pilot_team = np.zeros(n, bool)
        self.pilot_rescue = np.zeros(n, bool)
        self.events = []
        self.spells = []                        # (i, start, end, outcome, paying)
        self.hist = []

    def ltv_now(self, m):
        return self.bal / (self.value0 * hpi(m, self.region) / hpi(self.orig_m, self.region))

    def macro(self, m):
        return np.interp(m, [ym(2010), ym(2019), ym(2021), ym(2023), ym(2024, 6), ym(2026), ym(2030)],
                         [1.2, 0.9, 0.8, 1.15, 1.3, 1.3, 1.3])

    def _end_spell(self, idx, m, outcome):
        for i in idx:
            self.spells.append((int(i), int(self.lit_m[i]), int(m), outcome, bool(self.k[i] < 7)))
        self.lit_m[idx] = -1

    def step(self, m, rng):
        p = self.p
        live = (self.status == 0) & (self.orig_m <= m)
        nd = live & ~self.dist & (rng.random(self.n) < p["d_rate"] * self.macro(m))
        self.dist[nd] = True
        self.d_end[nd] = m + 1 + rng.geometric(1.0 / p["d_mean"], nd.sum())
        self.d_start[nd] = m
        self.dist[self.dist & (self.d_end <= m)] = False
        fe = live & (self.fix_end == m) & ~self.pip
        if fe.any():
            idx = np.where(fe)[0]
            ltv = self.ltv_now(m)[idx]
            dd = self.dist[idx]
            away = np.where((ltv < 0.85) & (self.k[idx] == 0) & ~dd, 0.30, 0.05)
            away = np.where(self.book[idx] == 3, away * 0.8, away)
            go = rng.random(len(idx)) < away
            g = idx[go]
            self.status[g] = 1
            self.close_m[g] = m
            st = idx[~go]
            band = np.select([ltv[~go] > 0.9, ltv[~go] > 0.85], [0.8, 0.4], 0.0)
            band = np.where(self.book[st] == 3, 0.7, np.where(self.book[st] == 2, band + 0.3, band))
            newrate = market_rate(m) + band
            oldpay = self.pay[st].copy()
            self.rate[st] = newrate
            self.prod[st] += 1
            newpay = np.where(self.io[st], self.bal[st] * newrate / 1200, annuity(self.bal[st], newrate, self.rem[st]))
            shock = newpay / np.maximum(oldpay, 1) - 1
            can = (~self.io[st]) & (m >= ym(2023, 7)) & (self.book[st] != 3) & (self.k[st] == 0)
            pe = np.where(self.dist[st], p["ext_p_d"], p["ext_p_ok"])
            yrs = (m - self.orig_m[st]) / 12.0
            sig_new = newpay / (self.pay0[st] * 1.03 ** yrs) / self.slack[st]
            broke = (sig_new > p["ext_sig"]) & (self.book[st] != 3)
            nb = st[broke & ~self.dist[st]]
            self.dist[nb] = True
            self.d_end[nb] = m + 1 + rng.geometric(1.0 / p["d_mean"], len(nb))
            self.d_start[nb] = m
            pe = np.where(broke, p["ext_p_d"], pe)
            ask = can & (shock > p["ext_thresh"]) & (rng.random(len(st)) < pe)
            e = st[ask]
            if len(e):
                # the term is extended by the fewest whole years (up to ten, and to no more than 40 years left) that
                # bring the payment back to about what it was
                cap = np.clip(480 - self.rem[e], 12, 120)
                add = cap.copy()
                for yrs_add in range(10, 0, -1):
                    pay_try = annuity(self.bal[e], self.rate[e], self.rem[e] + 12 * yrs_add)
                    ok = (pay_try <= oldpay[ask] * 1.02) & (12 * yrs_add <= cap)
                    add = np.where(ok, 12 * yrs_add, add)
                self.rem[e] = self.rem[e] + add
                self.ext_m[e] = m
                self.n_ext[e] += 1
                self.ext_kind[e] = 1
                hon = rng.integers(p["hon"][0], p["hon"][1] + 1, len(e))
                self.d_start[e] = np.maximum(self.d_start[e], m + hon)
                self.d_end[e] = np.maximum(self.d_end[e], self.d_start[e] + 1 + rng.geometric(1.0 / p["d_mean"], len(e)))
                newpay[ask] = annuity(self.bal[e], self.rate[e], self.rem[e])
            self.pay[st] = newpay
            self.fix_end[st] = m + np.where(rng.random(len(st)) < 0.45, 60, 24)
        live = (self.status == 0) & (self.orig_m <= m)
        idx = np.where(live)[0]
        yrs = (m - self.orig_m[idx]) / 12.0
        aff = self.pay[idx] / (self.pay0[idx] * 1.03 ** yrs)
        ltv = self.ltv_now(m)[idx]
        season = np.interp(m - self.orig_m[idx], [0, 6, 24, 60, 400], [0.2, 0.8, 1.2, 1.0, 0.8])
        dact = self.dist[idx] & (self.d_start[idx] <= m)
        mult = self.frail[idx] * np.where(dact, p["d_mult"], 1.0)
        bs = np.where(self.book[idx] == 3, p["beta_s_btl"], p["beta_s"])
        sig = aff / self.slack[idx]
        affterm = np.where(self.book[idx] == 3, np.exp(bs * np.maximum(aff - 1, 0)),
                           np.exp(p["beta_sig"] * np.maximum(sig - p["sig0"], 0)))
        h = p["b0"] * mult * affterm * np.exp(p["ltv_k"] * np.maximum(ltv - 0.8, 0)) * season * self.macro(m)
        h = h * np.array(p["book_h"])[self.book[idx]]
        h = np.where(self.book[idx] == 3, h * p["btl_h"], h)
        k = self.k[idx]
        u = rng.random(len(idx))
        miss0 = (k == 0) & (u < h)
        fr = self.frail[idx] ** 0.3
        roll = np.clip(0.40 * fr, 0, 0.85)
        cure = np.clip(0.32 / fr, 0, 0.9)
        inarr = (k > 0) & ~self.lit[idx]
        rolls = inarr & (u < roll)
        cures = inarr & (u >= roll) & (u < roll + cure)
        newk = k.copy()
        newk[miss0] = 1
        newk[rolls] += 1
        newk[cures] = 0
        # the 2024 pilot: the team's arrangements keep three in ten of its borrowers out of litigation for 18 months
        resc = self.pilot_rescue[idx] & (m - self.pilot_ref[idx] <= P.POSS_HORIZON) & (newk >= 4)
        newk[resc] = 0
        # collections capitalise the arrears once: added to the balance and spread over the remaining term
        ce = inarr & (newk >= 2) & (~self.io[idx]) & (self.book[idx] != 3) & (rng.random(len(idx)) < p["coll_ext_p"]) \
            & (self.cap_m[idx] < 0)
        if ce.any():
            e = idx[ce]
            self.bal[e] += k[ce] * self.pay[e]
            self.pay[e] = annuity(self.bal[e], self.rate[e], self.rem[e])
            self.cap_m[e] = m
            newk[ce] = 0
        litgo = (~self.lit[idx]) & (newk >= 5) & \
            (rng.random(len(idx)) < np.where(self.book[idx] == 3, p["btl_lit"], p["oo_lit"]))
        L = idx[litgo]
        self.lit[L] = True
        self.lit_m[L] = m
        delay = np.where(self.book[L] == 3, rng.integers(3, 7, len(L)), rng.integers(6, 13, len(L)))
        self.poss_m[L] = m + delay
        inl = self.lit[idx] & ~litgo & ~self.pip[idx]
        li = idx[inl]
        ltvl = ltv[inl]
        sell = rng.random(len(li)) < np.where(ltvl < 0.8, 0.07, np.where(ltvl < 0.95, 0.03, 0.005))
        buy = (self.book[li] == 2) & (rng.random(len(li)) < 0.09)
        lcure = rng.random(len(li)) < 0.04
        out = li[sell | buy]
        self._end_spell(li[sell], m, "sold")
        self._end_spell(li[buy & ~sell], m, "bought_back")
        self.status[out] = 1
        self.close_m[out] = m
        c = li[lcure & ~(sell | buy)]
        self._end_spell(c, m, "cured")
        self.lit[c] = False
        self.poss_m[c] = -1
        newk[np.isin(idx, c)] = 0
        pipi = self.pip[idx]
        newk[pipi] = k[pipi] + 1
        if P.PILOT[0] <= m <= P.PILOT[1]:
            hit = (newk >= 2) & (k < 2) & ~self.lit[idx] & (self.pilot_ref[idx] < 0)
            hi = idx[hit]
            self.pilot_ref[hi] = m
            self.pilot_team[hi] = self.even[hi]
            self.pilot_rescue[hi] = self.even[hi] & (rng.random(len(hi)) < p["pilot_rescue"])
        self.k[idx] = newk
        pm = (self.status == 0) & self.lit & (self.poss_m == m) & ~self.pip
        Pm = np.where(pm)[0]
        self._end_spell(Pm, m, "possession")
        self.pip[Pm] = True
        self.poss_done_m[Pm] = m
        self.poss_day[Pm] = rng.integers(1, 29, len(Pm))
        lag = rng.integers(70, 245, len(Pm))
        for i, d, g in zip(Pm, self.poss_day[Pm], lag):
            y, mo = divmod(int(m), 12)
            sd = dt.date(y, mo + 1, int(d)) + dt.timedelta(days=int(g))
            self.sale_m[i] = sd.year * 12 + sd.month - 1
            self.sale_day[i] = sd.day
            self.events.append((m, int(i), "possession", float(self.bal[i]), float(self.k[i] * self.pay[i])))
        sold = np.where((self.status == 0) & self.pip & (self.sale_m == m))[0]
        self.status[sold] = 2
        self.close_m[sold] = m
        self.lit[sold] = False
        self.pip[sold] = False
        idx2 = np.where((self.status == 0) & (self.orig_m <= m) & (self.k >= 2) & ~self.lit)[0]
        if len(idx2):
            l2 = self.ltv_now(m)[idx2]
            s = idx2[rng.random(len(idx2)) < np.where(l2 < 0.8, 0.03, 0.0)]
            self.status[s] = 1
            self.close_m[s] = m
        live3 = np.where((self.status == 0) & (self.orig_m <= m) & (self.k == 0))[0]
        r = live3[rng.random(len(live3)) < np.where(self.book[live3] == 3, 0.004, 0.0025)]
        self.status[r] = 1
        self.close_m[r] = m
        live4 = np.where((self.status == 0) & (self.orig_m <= m))[0]
        intr = self.bal[live4] * self.rate[live4] / 1200
        prin = np.where(self.io[live4] | self.pip[live4], 0.0, np.maximum(self.pay[live4] - intr, 0))
        self.bal[live4] = np.maximum(self.bal[live4] - prin, 0)
        self.rem[live4] = np.maximum(self.rem[live4] - 1, 1)

    def run(self, until=SNAP, record=True):
        rng = self.rng
        for m in range(START, until + 1):
            self.step(m, rng)
            if record and HIST0 <= m <= SNAP:
                live = np.where(((self.status == 0) & (self.orig_m <= m)) | (self.close_m == m))[0]
                self.hist.append((m, live, self.prod[live].copy(), self.rate[live].copy(), self.rem[live].copy(),
                                  self.pay[live].copy(), self.k[live].copy(), self.bal[live].copy(),
                                  self.status[live].copy(), self.lit[live].copy(), self.fix_end[live].copy(),
                                  self.pip[live].copy() | (self.close_m[live] == m) & (self.status[live] == 2),
                                  self.cap_m[live] == m))
        # spells still open at the as-of date
        open_ = np.where((self.status == 0) & self.lit & ~self.pip)[0]
        for i in open_:
            self.spells.append((int(i), int(self.lit_m[i]), -1, "open", bool(self.k[i] < 7)))
        return self
