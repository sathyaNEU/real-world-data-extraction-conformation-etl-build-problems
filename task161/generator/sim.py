"""task161 daily simulation: the clean truth of the book (shipments, container receipts, on-hand).

One RNG stream per account so a change to one account never re-rolls another. Nothing here ships;
pack.py writes the files from these arrays.
"""
import datetime as dt
import numpy as np
import world as W

ONE = dt.timedelta(days=1)


def us_holidays(year):
    """Days the buildings are shut (no receipts, no shipments)."""
    def nth(weekday, n, month):
        d = dt.date(year, month, 1)
        while d.weekday() != weekday:
            d += ONE
        return d + dt.timedelta(days=7 * (n - 1))

    def last(weekday, month):
        d = dt.date(year, month + 1, 1) - ONE if month < 12 else dt.date(year, 12, 31)
        while d.weekday() != weekday:
            d -= ONE
        return d
    return {dt.date(year, 1, 1), last(0, 5), dt.date(year, 7, 4), nth(0, 1, 9), nth(3, 4, 11),
            nth(3, 4, 11) + ONE, dt.date(year, 12, 24), dt.date(year, 12, 25)}


HOLIDAYS = set()
for _y in range(2019, 2028):
    HOLIDAYS |= us_holidays(_y)

WEEKDAY_SHIP = [1.12, 1.08, 1.05, 1.04, 1.00, 0.42, 0.0]   # Mon..Sun
WEEKDAY_RECV = [1.10, 1.08, 1.04, 1.02, 1.00, 0.55, 0.0]


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += ONE
    return out


ALL_DAYS = days(W.HIST_START, dt.date(2027, 12, 31))
DIDX = {d: i for i, d in enumerate(ALL_DAYS)}
ND = len(ALL_DAYS)


def frac_year(d):
    return d.year + (d.timetuple().tm_yday - 0.5) / 365.25


def demand_shock(d):
    """Book-wide consumption shock: the spring 2020 lockdown dip and the 2020-21 goods boom."""
    ym = (d.year, d.month)
    table = {(2020, 3): 0.93, (2020, 4): 0.76, (2020, 5): 0.82, (2020, 6): 0.95, (2020, 7): 1.04,
             (2020, 8): 1.08, (2020, 9): 1.09, (2020, 10): 1.10, (2020, 11): 1.10, (2020, 12): 1.09}
    if ym in table:
        return table[ym]
    if (2021, 1) <= ym <= (2021, 12):
        return 1.08
    if (2022, 1) <= ym <= (2022, 6):
        return 1.04
    return 1.0


def cover_mult(d):
    """Customers held more cover through the 2021-22 port congestion, back to normal by mid 2023."""
    t = frac_year(d)
    if t < 2021.2:
        return 1.0
    if t < 2021.8:
        return 1.0 + 0.20 * (t - 2021.2) / 0.6
    if t < 2022.75:
        return 1.20
    if t < 2023.45:
        return 1.20 - 0.20 * (t - 2022.75) / 0.7
    return 1.0


def open_day(d):
    return d not in HOLIDAYS and d.weekday() != 6


class Account:
    def __init__(self, code):
        (self.cat, self.level, self.cover, self.s, self.g, self.m, start, end, self.ppc) = W.ACCOUNTS[code]
        self.code = code
        self.start = dt.date.fromisoformat(start)
        self.end = dt.date.fromisoformat(end) if end else None
        prof = np.array(W.PROFILE[self.cat], float)
        self.prof = prof / prof.mean()
        self.rng = np.random.default_rng([W.SEED, int(code[1:]) + (100 if code[0] == "F" else 0)])
        self.month_noise = {}

    def active(self, d):
        return d >= self.start and (self.end is None or d <= self.end)

    def month_level(self, y, m):
        """Expected pallets shipped in month (y, m) before the daily noise."""
        key = (y, m)
        if key not in self.month_noise:
            self.month_noise[key] = float(np.exp(self.rng.normal(0, 0.025)))
        mid = dt.date(y, m, 15)
        base = self.level * (1 + self.g) ** (frac_year(mid) - 2026.5) * self.prof[m - 1]
        # the projection window carries no month noise: the truth there is what the record supports
        noise = 1.0 if (y, m) >= (2027, 1) else self.month_noise[key]
        ramp = 1.0
        if mid - self.start < dt.timedelta(days=150) and self.start > W.HIST_START:
            ramp = 0.45 + 0.55 * (mid - self.start).days / 150.0
        return base * noise * demand_shock(mid) * ramp


def month_open_weights(y, m):
    ds = [d for d in days(dt.date(y, m, 1), (dt.date(y + (m == 12), m % 12 + 1, 1) - ONE))]
    return ds, np.array([WEEKDAY_SHIP[d.weekday()] if open_day(d) else 0.0 for d in ds])


def simulate():
    """Return the clean truth per account: daily expected and actual shipments, receipts (containers),
    on-hand, normal target and bought-ahead excess, over ALL_DAYS (through the end of the window)."""
    out = {}
    # expected daily shipments per account
    for code in W.ACCOUNTS:
        acc = Account(code)
        exp_ship = np.zeros(ND)
        for y in range(2019, 2028):
            for m in range(1, 13):
                if (y, m) < (W.HIST_START.year, W.HIST_START.month) or (y, m) > (2027, 12):
                    continue
                ds, w = month_open_weights(y, m)
                lv = acc.month_level(y, m)
                w = w / w.sum()
                for d, wi in zip(ds, w):
                    if acc.active(d):
                        exp_ship[DIDX[d]] = lv * wi
        out[code] = {"acc": acc, "exp_ship": exp_ship}

    for code, rec in out.items():
        acc, es = rec["acc"], rec["exp_ship"]
        rng = acc.rng
        # normal target stock: cover x the mean of this and next month's expected shipments, set at each
        # mid-month and interpolated by day (cover in months of shipments)
        keys = month_keys(lo=(W.HIST_START.year, W.HIST_START.month), hi=(2028, 2))
        lv = {k: acc.month_level(*k) for k in keys}
        mids, vals = [], []
        for k, nk in zip(keys[:-1], keys[1:]):
            mid = dt.date(k[0], k[1], 15)
            mids.append((mid - W.HIST_START).days)
            vals.append(acc.cover * cover_mult(mid) * 0.5 * (lv[k] + lv[nk]))
        N = np.interp(np.arange(ND), mids, vals)
        if acc.start > W.HIST_START:
            N = N * np.array([1.0 if d >= acc.start else 0.0 for d in ALL_DAYS])
        # bought-ahead totals per rush: s x expected shipments over m months after the step
        E_total = {}
        for r, (b0, b1, step) in W.RUSHES.items():
            mm = acc.m.get(r, 0.0)
            if mm <= 0:
                continue
            i0 = DIDX.get(step)
            span = int(round(mm * 30.4))
            if i0 is None:
                continue
            E_total[r] = acc.s * es[i0:i0 + span].sum() if i0 + span <= ND else acc.s * es[i0:].sum()
        # build days and ramp weights per rush
        build_add = np.zeros(ND)
        in_build = np.zeros(ND, bool)
        for r, tot in E_total.items():
            b0, b1, step = W.RUSHES[r]
            bd = [d for d in days(b0, b1) if open_day(d)]
            # bought-ahead receipts spread evenly over the open days between the announcement and the step
            w = np.ones(len(bd))
            w = w / w.sum()
            for d, wi in zip(bd, w):
                build_add[DIDX[d]] += tot * wi
            for d in days(b0, b1):
                in_build[DIDX[d]] = True
        S = np.zeros(ND, int)
        R = np.zeros(ND, int)
        OH = np.zeros(ND, int)
        E = np.zeros(ND)
        Nt = np.zeros(ND)
        boxes = []      # (day index, size, pallets)
        oh = 0.0
        e = 0.0
        res, cur = 0.0, 0.0     # stock left from earlier rushes (burning) and the build under way (held)
        started = False
        for i, d in enumerate(ALL_DAYS):
            if not acc.active(d):
                if started and acc.end is not None and d > acc.end:
                    OH[i] = 0
                continue
            if not started:
                started = True
                oh = round(N[i])
            # shipments
            mu = es[i]
            sh = int(max(0, round(mu + rng.normal(0, 1.4 * np.sqrt(mu + 1)))) ) if mu > 0 else 0
            if acc.end is not None and d == acc.end:
                sh = int(oh)          # move-out on the last contract day
            sh = int(min(sh, max(0, oh)))
            # excess: build or burn
            if in_build[i]:
                cur += build_add[i]
            elif cur > 0:
                res += cur
                cur = 0.0
            if res > 0:
                res = max(0.0, res - acc.s * sh)
            e = res + cur
            target = N[i] + e
            after = oh - sh
            rcv = 0
            if open_day(d) and not (acc.end is not None and d >= acc.end - dt.timedelta(days=20)):
                desired = es[i] + 0.38 * (target - after)
                desired = max(0.0, desired)
                lam = desired / acc.ppc
                n = int(rng.poisson(lam)) if lam > 0 else 0
                for _ in range(n):
                    u = rng.random()
                    size = "40HC" if u < 0.68 else ("40" if u < 0.84 else ("20" if u < 0.95 else "45"))
                    base = acc.ppc * {"40HC": 1.0, "40": 0.88, "20": 0.47, "45": 1.12}[size]
                    p = int(max(4, round(base + rng.normal(0, 1.6))))
                    boxes.append((i, size, p))
                    rcv += p
            oh = after + rcv
            S[i], R[i], OH[i], E[i], Nt[i] = sh, rcv, int(oh), e, N[i]
        rec.update(S=S, R=R, OH=OH, E=E, N=Nt, boxes=boxes, E_total=E_total)
    return out


def month_keys(lo=(2019, 4), hi=(2026, 12)):
    ks, y, m = [], lo[0], lo[1]
    while (y, m) <= hi:
        ks.append((y, m))
        y, m = (y + (m == 12), m % 12 + 1)
    return ks


def monthly(truth, code, field, hi=(2026, 11), how="sum"):
    arr = truth[code][field]
    out = {}
    for (y, m) in month_keys(hi=hi):
        ds = [DIDX[d] for d in days(dt.date(y, m, 1), dt.date(y + (m == 12), m % 12 + 1, 1) - ONE)]
        out[(y, m)] = float(arr[ds].sum() if how == "sum" else arr[ds].mean())
    return out
