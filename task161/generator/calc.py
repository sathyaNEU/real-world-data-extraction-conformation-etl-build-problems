"""task161 calculations on the shipped view of the book: the golden and every rival route.

Input is a Book: per account, daily series indexed by calendar day (on-hand at each close, pallets
shipped, pallets received), the December booking notices in pallets, the duty step dates, and the
accounts in the book at the as-of. The same code runs on the generator's clean truth and on the
files read back from target/ (golden.py), so a rung computed here is the rung a solver computes.
"""
import datetime as dt
import numpy as np

ONE = dt.timedelta(days=1)
RACK_CAP = 40000
BLOCK = 4000
HURDLE = 0.75
SAT = 0.40          # a Saturday's shipments against a weekday's, the book's own ratio in 2025 and 2026
WINDOW = [(2027, m) for m in range(1, 7)]
CLEAN = None  # set in Book: months used for each account's normal cover


def mkeys(lo, hi):
    out, (y, m) = [], lo
    while (y, m) <= hi:
        out.append((y, m))
        y, m = (y + (m == 12), m % 12 + 1)
    return out


def nxt(k, n=1):
    y, m = k
    for _ in range(n):
        y, m = (y + (m == 12), m % 12 + 1)
    return (y, m)


def prv(k):
    y, m = k
    return (y - (m == 1), (m - 2) % 12 + 1)


def month_days(k):
    a = dt.date(k[0], k[1], 1)
    b = dt.date(*nxt(k), 1) - ONE
    out, d = [], a
    while d <= b:
        out.append(d)
        d += ONE
    return out


def blocks(monthly_positions, rack=RACK_CAP, test="each", month_days_n=None):
    """The space policy's block test: blocks fill in order, block k holding the overflow between
    4,000(k-1) and 4,000k positions each month; a block is taken when its use over the term is at
    least three quarters of its position-months. test="set" reads the line as the average use of the
    blocks taken together; month_days_n weights each month by its days (position-days)."""
    O = np.maximum(np.asarray(monthly_positions, float) - rack, 0.0)
    w = np.ones(len(O)) if month_days_n is None else np.asarray(month_days_n, float)
    U = [float((np.clip(O - BLOCK * k, 0, BLOCK) * w).sum() / (BLOCK * w.sum())) for k in range(6)]
    n = 0
    if test == "set":
        for k in range(1, 7):
            if np.mean(U[:k]) >= HURDLE:
                n = k
    else:
        for u in U:
            if u >= HURDLE:
                n += 1
            else:
                break
    return {"blocks": n, "use": U, "overflow": [float(x) for x in O], "positions": [float(x) for x in monthly_positions]}


class Book:
    """days: sorted list of dates with data (through the last close); acc[code] = dict of np arrays
    oh, ship, recv aligned to days; notices[code] = pallets due to arrive after the last close in
    December; steps = list of past duty-step dates; current = account codes in the book."""

    def __init__(self, days, acc, notices, steps, current, last_close, announced=None):
        self.announced = announced or []
        self.days = days
        self.idx = {d: i for i, d in enumerate(days)}
        self.acc = acc
        self.notices = notices
        self.steps = steps
        self.current = current
        self.last = last_close
        self.full_months = [k for k in mkeys((days[0].year, days[0].month), (last_close.year, last_close.month))
                            if dt.date(*nxt(k), 1) - ONE <= last_close]

    def monthly(self, code):
        a = self.acc[code]
        P, S, R = {}, {}, {}
        skip = getattr(self, "skip_day", None)
        for k in self.full_months:
            ii = [self.idx[d] for d in month_days(k) if d in self.idx and not (skip and skip(d))]
            P[k] = float(a["oh"][ii].mean())
            S[k] = float(a["ship"][ii].sum())
            R[k] = float(a["recv"][ii].sum())
        return P, S, R


# ----------------------------------------------------------------------------------- the pieces

def growth(S, end=(2026, 11)):
    last12 = mkeys(nxt(end, -11) if False else (end[0] - 1, end[1] % 12 + 1) if end[1] < 12 else (end[0], 1), end)
    prev12 = [(y - 1, m) for (y, m) in last12]
    a = sum(S.get(k, 0.0) for k in last12)
    b = sum(S.get(k, 0.0) for k in prev12)
    return a / b if b > 0 and all(k in S for k in prev12) else 1.0


def forecast_shipments(S, months, how="same_month"):
    """Each month as the same month a year earlier grown at the account's growth over the latest
    twelve months against the twelve before (how="two_year": the mean of the same month in the two
    years before, grown for one and a half years; how="flat": the same month a year earlier)."""
    g = growth(S)
    out = {}
    for k in months:
        ref = (k[0] - 1, k[1])
        ref2 = (k[0] - 2, k[1])
        if how == "flat":
            out[k] = S[ref] if ref in S else None
        elif how == "two_year" and ref in S and ref2 in S:
            out[k] = 0.5 * (S[ref] * g + S[ref2] * g * g)
        else:
            out[k] = S[ref] * g if ref in S else None
    return out


def rush_and_burn_months(steps):
    """Months touched by a build or a burn: the three months before each step and the five after."""
    bad = set()
    for st in steps:
        k = (st.year, st.month)
        for j in range(-3, 6):
            kk = k
            if j < 0:
                for _ in range(-j):
                    kk = prv(kk)
            else:
                kk = nxt(kk, j)
            bad.add(kk)
    return bad


def normal_cover(P, S, months):
    vals = []
    for k in months:
        if k in P and k in S and nxt(k) in S and S[k] > 0:
            vals.append(P[k] / (0.5 * (S[k] + S[nxt(k)])))
    return float(np.median(vals)) if len(vals) >= 6 else None


def daily_normal(book, code, cover, S_ext):
    """Normal stock by day: cover x the mean of this and next month's shipments, set at mid-month and
    interpolated. S_ext holds actual months and forecast months."""
    ks = sorted(S_ext)
    mids, vals = [], []
    for k in ks:
        if nxt(k) in S_ext and S_ext[k] is not None and S_ext[nxt(k)] is not None:
            mids.append(dt.date(k[0], k[1], 15))
            vals.append(cover * 0.5 * (S_ext[k] + S_ext[nxt(k)]))
    base = mids[0]
    x = np.array([(m - base).days for m in mids], float)

    def at(d):
        return float(np.interp((d - base).days, x, vals))
    return at


def burn_share(book, code, cover, P, S):
    """Each past step: the account's excess over normal by day from the step until it first runs out,
    against its cumulative shipments; the share is the slope (pallets of excess gone per pallet
    shipped). Returns the per-episode shares and their pooled value."""
    a = book.acc[code]
    at = daily_normal(book, code, cover, dict(S))
    eps = []
    for st in book.steps:
        if st not in book.idx:
            continue
        i0 = book.idx[st]
        later = [d for d in book.announced if d > st]
        stop = book.idx.get(min(later)) if later else None
        pre = [book.days[i] for i in range(max(0, i0 - 7), i0)]
        n0 = np.mean([at(d) for d in pre])
        e0 = np.mean([a["oh"][book.idx[d]] - at(d) for d in pre])
        if e0 < 0.12 * n0:
            continue
        xs, ys, cum = [], [], 0.0
        for i in range(i0, min(len(book.days), i0 + 240, stop if stop is not None else 10 ** 9)):
            d = book.days[i]
            cum += a["ship"][i]
            e = a["oh"][i] - at(d)
            if e <= 0.25 * e0:
                break
            xs.append(cum)
            ys.append(e0 - e)
        if len(xs) >= 15:
            xs, ys = np.array(xs), np.array(ys)
            s = float(np.polyfit(xs, ys, 1)[0])
            eps.append((st, s, float(e0), len(xs), float(xs[-1])))
    return eps


def _open_w(d, hol):
    return 0.0 if d.weekday() == 6 or d in hol else (SAT if d.weekday() == 5 else 1.0)


DEC_HOL = {dt.date(2026, 12, 24), dt.date(2026, 12, 25)}
WIN_HOL = {dt.date(2027, 1, 1), dt.date(2027, 5, 31)}


def project(book, code, s, cover, P, S, fc, opt=None):
    """Daily projection from the last close: December's remaining notices in, forecast shipments out,
    the excess over normal burned at s x shipments until it is gone. Returns monthly positions (the
    mean of each day's close unless opt["reading"] says the month-end close or the peak day)."""
    opt = opt or {}
    a = book.acc[code]
    S_ext = dict(S)
    S_ext.update({k: v for k, v in fc.items() if v is not None})
    at = daily_normal(book, code, cover, S_ext)
    last = book.last + dt.timedelta(days=opt.get("close_shift", 0))
    oh = float(a["oh"][book.idx[last]])
    dec_k = (book.last.year, book.last.month)
    dec_days = [d for d in month_days(dec_k) if d > last]
    open_w = np.array([_open_w(d, DEC_HOL) for d in month_days(dec_k)])
    rem = np.array([_open_w(d, DEC_HOL) for d in dec_days])
    dec_ship = fc[dec_k] * rem.sum() / open_w.sum()
    if opt.get("dec_rest") == "last_year":
        # the rest of December at last year's net flow over the same days
        i0, i1 = book.idx[last.replace(year=last.year - 1) + ONE], book.idx[dt.date(last.year - 1, 12, 31)]
        oh_dec31 = oh + float(a["recv"][i0:i1 + 1].sum() - a["ship"][i0:i1 + 1].sum())
    else:
        oh_dec31 = oh + book.notices.get(code, 0.0) - dec_ship
    e = max(0.0, oh_dec31 - at(dt.date(2026, 12, 31)))
    out = []
    reading = opt.get("reading", "mean")
    for k in WINDOW:
        ds = month_days(k)
        w = np.array([_open_w(d, WIN_HOL) for d in ds])
        daily = fc[k] * w / w.sum()
        vals = []
        for d, sh in zip(ds, daily):
            e = max(0.0, e - s * sh)
            vals.append(at(d) + e)
        out.append(float(np.mean(vals)) if reading == "mean" else (vals[-1] if reading == "month_end" else max(vals)))
    return out, oh_dec31, e


def normal_cover_mean(P, S, months):
    vals = [P[k] / (0.5 * (S[k] + S[nxt(k)])) for k in months if k in P and k in S and nxt(k) in S and S[k] > 0]
    return float(np.mean(vals)) if len(vals) >= 6 else None


def golden(book, return_parts=False, opt=None):
    """The golden: each account's excess over its normal stock at 31 December burned at the share of
    its own forecast shipments its own earlier rushes showed, until its excess is gone.

    opt holds the grid's and the fork table's variants (none of them is the golden's default):
    share in weighted (default), mean, median, latest, pooled, with scale a multiplier; cover in
    median (default) or mean_2024; forecast in same_month (default), two_year, flat; steps, a subset
    of the earlier steps; population current (default) or all; and project()'s and blocks()' keys."""
    opt = opt or {}
    steps = opt.get("steps", book.steps)
    bad = rush_and_burn_months(list(book.steps) + [dt.date(2027, 1, 1)])
    parts = {}
    pooled = []
    codes = list(book.current)
    if opt.get("population") == "all":
        codes = [c for c in book.acc if c in book.current or book.acc[c]["oh"][book.idx[book.last]] > 0]
    saved = book.steps
    book.steps = list(steps)
    try:
        for code in codes:
            P, S, R = book.monthly(code)
            if opt.get("cover") == "mean_2024":
                clean = [k for k in book.full_months if k not in bad and k >= (2024, 1) and nxt(k) in S]
                cover = normal_cover_mean(P, S, clean)
            else:
                clean = [k for k in book.full_months if k not in bad and k >= (2023, 7) and nxt(k) in S]
                cover = normal_cover(P, S, clean)
            eps = burn_share(book, code, cover, P, S)
            parts[code] = {"cover": cover, "episodes": eps, "P": P, "S": S}
            pooled += [e[1] for e in eps]
    finally:
        book.steps = saved
    s_pool = float(np.median(pooled))
    total = np.zeros(6)
    how = opt.get("share", "weighted")
    for code in codes:
        p = parts[code]
        eps = p["episodes"]
        if not eps or how == "pooled":
            s = s_pool
        elif how == "mean":
            s = float(np.mean([e[1] for e in eps]))
        elif how == "median":
            s = float(np.median([e[1] for e in eps]))
        elif how == "latest":
            s = float(eps[-1][1])
        else:
            w = np.array([e[4] for e in eps])
            s = float(np.dot(w, [e[1] for e in eps]) / w.sum())
        s *= opt.get("scale", 1.0)
        fc = forecast_shipments(p["S"], [(2026, 12)] + WINDOW + [(2027, 7)], how=opt.get("forecast", "same_month"))
        path, oh31, e_end = project(book, code, s, p["cover"], p["P"], p["S"], fc, opt)
        p.update(s=s, fc=fc, path=path, oh_dec31=oh31, e_jun=e_end)
        total += np.array(path)
    days_n = [len(month_days(k)) for k in WINDOW] if opt.get("test") == "days" else None
    res = blocks(total, rack=opt.get("rack", RACK_CAP), test="set" if opt.get("test") == "set" else "each",
                 month_days_n=days_n)
    res["s_pool"] = s_pool
    if return_parts:
        return res, parts
    return res


# ----------------------------------------------------------------------------------- rival routes

def book_series(book, codes=None):
    """Book-level monthly positions, shipments, receipts summed over the given accounts (default all
    accounts in the history, current and former)."""
    codes = codes or list(book.acc)
    P, S, R = {}, {}, {}
    for c in codes:
        p, s, r = book.monthly(c)
        for k in p:
            P[k] = P.get(k, 0.0) + p[k]
            S[k] = S.get(k, 0.0) + s[k]
            R[k] = R.get(k, 0.0) + r[k]
    return P, S, R


def _book_parts(book):
    """Book-level normal and excess for the current accounts, as a solver working with totals sees
    them: one cover for the book, the book's own forecast shipments."""
    bad = rush_and_burn_months(book.steps + [dt.date(2027, 1, 1)])
    P, S, R = book_series(book, book.current)
    clean = [k for k in book.full_months if k not in bad and k >= (2023, 7) and nxt(k) in S]
    cover = normal_cover(P, S, clean)
    fc = forecast_shipments(S, [(2026, 12)] + WINDOW + [(2027, 7)])
    S_ext = dict(S)
    S_ext.update(fc)
    at = daily_normal(book, None, cover, S_ext)
    oh = sum(float(book.acc[c]["oh"][book.idx[book.last]]) for c in book.current)
    dec_k = (book.last.year, book.last.month)
    allw = [d for d in month_days(dec_k)]
    def w(d):
        return 0.0 if d.weekday() == 6 or d in (dt.date(2026, 12, 24), dt.date(2026, 12, 25)) else (SAT if d.weekday() == 5 else 1.0)
    frac = sum(w(d) for d in allw if d > book.last) / sum(w(d) for d in allw)
    oh31 = oh + sum(book.notices.get(c, 0.0) for c in book.current) - fc[dec_k] * frac
    E = max(0.0, oh31 - at(dt.date(2026, 12, 31)))
    Nm = [float(np.mean([at(d) for d in month_days(k)])) for k in WINDOW]
    return {"P": P, "S": S, "cover": cover, "fc": fc, "at": at, "E": E, "N": Nm, "oh31": oh31}


def _book_excess_daily(book, at_book, codes):
    oh = np.zeros(len(book.days))
    sh = np.zeros(len(book.days))
    for c in codes:
        oh += book.acc[c]["oh"]
        sh += book.acc[c]["ship"]
    return oh, sh


def past_book_episodes(book):
    """Book-level excess after each past step (all accounts present at the time), from the step to the
    next announcement or until it first falls under a quarter of its size: daily excess, shipments."""
    bad = rush_and_burn_months(book.steps + [dt.date(2027, 1, 1)])
    codes = list(book.acc)
    P, S, R = book_series(book, codes)
    clean = [k for k in book.full_months if k not in bad and nxt(k) in S]
    cover = normal_cover(P, S, clean)
    at = daily_normal(book, None, cover, dict(S))
    oh, sh = _book_excess_daily(book, at, codes)
    out = []
    for st in book.steps:
        i0 = book.idx[st]
        later = [d for d in book.announced if d > st]
        stop = book.idx.get(min(later)) if later else len(book.days)
        pre = range(max(0, i0 - 7), i0)
        e0 = float(np.mean([oh[i] - at(book.days[i]) for i in pre]))
        es, cs, ds, cum = [], [], [], 0.0
        for i in range(i0, min(stop, i0 + 240)):
            cum += sh[i]
            e = oh[i] - at(book.days[i])
            es.append(e); cs.append(cum); ds.append(book.days[i])
            if e <= 0.05 * at(book.days[i]):
                break
        out.append({"step": st, "e0": e0, "e": np.array(es), "cum": np.array(cs), "days": ds})
    return out


def _monthly_from_daily_excess(parts, daily_e_fn):
    """Monthly mean positions: normal plus a daily excess path given by daily_e_fn(day_index_in_window)."""
    out = []
    j = 0
    for k in WINDOW:
        vals = []
        for d in month_days(k):
            vals.append(parts["at"](d) + daily_e_fn(j, d))
            j += 1
        out.append(float(np.mean(vals)))
    return out


def rival_decay(book, hl_months=None):
    """Rung 0, the default path: the rush's excess over the book's normal stock fades at the half-life
    the earlier rushes' excess faded at."""
    parts = _book_parts(book)
    if hl_months is None:
        hls = []
        for ep in past_book_episodes(book):
            e = ep["e"]
            t = np.arange(len(e)) / 30.4
            ok = e > 0.05 * max(e[0], 1)
            if ok.sum() >= 15:
                b = np.polyfit(t[ok], np.log(e[ok]), 1)[0]
                hls.append(np.log(0.5) / b if b < 0 else np.inf)
        hl_months = float(np.median(hls))
    lam = 0.5 ** (1.0 / hl_months)
    pos = _monthly_from_daily_excess(parts, lambda j, d: parts["E"] * lam ** ((j + 1) / 30.4))
    r = blocks(pos)
    r["half_life_months"] = hl_months
    return r


def rival_time_back(book):
    """The excess runs back to normal in a straight line over as long as the earlier rushes took."""
    parts = _book_parts(book)
    durs = [len(ep["e"]) / 30.4 for ep in past_book_episodes(book)]
    T = float(np.mean(durs))
    pos = _monthly_from_daily_excess(parts, lambda j, d: max(0.0, parts["E"] * (1 - (j + 1) / (T * 30.4))))
    r = blocks(pos)
    r["months_back"] = T
    return r


def rival_book_burn(book, how="slope"):
    """The book's excess burns at the share of the book's shipments the earlier rushes burned at."""
    parts = _book_parts(book)
    shares = []
    for ep in past_book_episodes(book):
        if len(ep["e"]) >= 15:
            if how == "slope":
                shares.append(float(np.polyfit(ep["cum"], ep["e0"] - ep["e"], 1)[0]))
            else:   # total excess over total shipments until it ran out
                shares.append(float((ep["e0"] - ep["e"][-1]) / ep["cum"][-1]))
    phi = float(np.median(shares))
    daily = []
    for k in WINDOW:
        ds = month_days(k)
        w = np.array([0.0 if d.weekday() == 6 or d in (dt.date(2027, 1, 1), dt.date(2027, 5, 31)) else
                      (SAT if d.weekday() == 5 else 1.0) for d in ds])
        daily += list(parts["fc"][k] * w / w.sum())
    state = {"e": parts["E"]}
    def fn(j, d):
        state["e"] = max(0.0, state["e"] - phi * daily[j])
        return state["e"]
    pos = _monthly_from_daily_excess(parts, fn)
    r = blocks(pos)
    r["phi"] = phi
    return r


def rival_monthly_fall(book):
    """The excess falls by as many pallets a month as the earlier rushes' excess fell by."""
    parts = _book_parts(book)
    rates = []
    for ep in past_book_episodes(book):
        if len(ep["e"]) >= 15:
            t = np.arange(len(ep["e"])) / 30.4
            rates.append(-float(np.polyfit(t, ep["e"], 1)[0]))
    rate = float(np.median(rates))
    pos = _monthly_from_daily_excess(parts, lambda j, d: max(0.0, parts["E"] - rate * (j + 1) / 30.4))
    r = blocks(pos)
    r["fall_per_month"] = rate
    return r


def rival_no_payback(book):
    """The rush's stock stays: receipts run at last year's pace against last year's shipments."""
    parts = _book_parts(book)
    pos = [n + parts["E"] for n in parts["N"]]
    return blocks(pos)


def rival_scaled(book, ref="nov"):
    """Last year's January to June positions, scaled by the latest positions against a year earlier."""
    P, S, R = book_series(book, book.current)
    if ref == "nov":
        r = P[(2026, 11)] / P[(2025, 11)]
    elif ref == "sepnov":
        r = sum(P[(2026, m)] for m in (9, 10, 11)) / sum(P[(2025, m)] for m in (9, 10, 11))
    else:   # the projected end of December against December 2025's mean
        parts = _book_parts(book)
        r = parts["oh31"] / P[(2025, 12)]
    pos = [P[(2026, m)] * r for m in range(1, 7)]
    out = blocks(pos)
    out["ratio"] = r
    return out


def rival_per_account_decay(book):
    """Each account's own excess fades at the half-life its own earlier rushes showed."""
    res, parts = golden(book, return_parts=True)
    total = np.zeros(6)
    for c in book.current:
        p = parts[c]
        hl = []
        for st, s, e0, n, cum in p["episodes"]:
            hl.append(max(0.25, (0.75 * e0) / max(1.0, s * cum / max(1, n) * 30.4) / 2.0))
        h = float(np.median(hl)) if hl else 1.0
        lam = 0.5 ** (1.0 / h)
        S_ext = dict(p["S"])
        S_ext.update({k: v for k, v in p["fc"].items() if v is not None})
        at = daily_normal(book, c, p["cover"], S_ext)
        E = max(0.0, p["oh_dec31"] - at(dt.date(2026, 12, 31)))
        j = 0
        for i, k in enumerate(WINDOW):
            vals = []
            for d in month_days(k):
                j += 1
                vals.append(at(d) + E * lam ** (j / 30.4))
            total[i] += np.mean(vals)
    return blocks(total)


def rival_per_account_monthly_fall(book):
    """Each account's own excess falls by as many pallets a month as its own earlier excess fell by."""
    res, parts = golden(book, return_parts=True)
    total = np.zeros(6)
    for c in book.current:
        p = parts[c]
        rates = []
        for st, s, e0, n, cum in p["episodes"]:
            # the episode's mean fall per month: its share times its shipments per month
            rates.append(s * cum / max(1, n) * 30.4)
        rate = float(np.median(rates)) if rates else 0.0
        S_ext = dict(p["S"])
        S_ext.update({k: v for k, v in p["fc"].items() if v is not None})
        at = daily_normal(book, c, p["cover"], S_ext)
        E = max(0.0, p["oh_dec31"] - at(dt.date(2026, 12, 31)))
        j = 0
        for i, k in enumerate(WINDOW):
            vals = []
            for d in month_days(k):
                j += 1
                vals.append(at(d) + max(0.0, E - rate * j / 30.4))
            total[i] += np.mean(vals)
    return blocks(total)


def rival_holt_winters(book):
    """Additive Holt-Winters on the book's monthly positions to November 2026, fitted through the rush."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    P, S, R = book_series(book, book.current)
    ks = [k for k in sorted(P) if k >= (2021, 1)]
    y = np.array([P[k] for k in ks])
    m = ExponentialSmoothing(y, trend="add", seasonal="add", seasonal_periods=12,
                             initialization_method="estimated").fit()
    f = m.forecast(8)        # Dec 2026 .. Jul 2027
    return blocks(list(f[1:7]))


def rival_trend(book):
    """The rush months' positions trended straight on."""
    P, S, R = book_series(book, book.current)
    ks = [(2026, 8), (2026, 9), (2026, 10), (2026, 11)]
    y = np.array([P[k] for k in ks])
    b = np.polyfit(np.arange(4), y, 1)
    pos = [float(np.polyval(b, 4 + 1 + i)) for i in range(6)]
    return blocks(pos)


def rival_dwell(book):
    """Positions as receipts times days on hand (Little's law): last year's receipts, this year's
    days on hand."""
    P, S, R = book_series(book, book.current)
    g = growth(S)
    dwell = sum(P[(2026, m)] for m in range(1, 12)) / sum(R[(2026, m)] for m in range(1, 12))   # months
    pos = [R[(2026, m)] * g * dwell for m in range(1, 7)]
    return blocks(pos)
