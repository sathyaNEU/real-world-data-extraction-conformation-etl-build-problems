"""Each company's fiscal calendar, its quarterly results in economic per-share terms (before any split), and when
it announced and filed them: the press release's date and time of day, the 10-Q or 10-K filing date, and the
trading day the market first traded on the news."""
import datetime as dt

import numpy as np

import universe as U
import world as W

FYE_CHOICES = [12, 6, 9, 3, 1]
# revenue per dollar of market value by sector, relative to the median company
SALES_TO_PRICE = [1.25, 1.0, 1.1, 1.4, 1.6, 0.45, 0.35, 0.6, 0.7, 0.55, 0.18]
FYE_P = [0.75, 0.08, 0.06, 0.05, 0.06]


def _month_end(y, m):
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def _last_saturday(y, m):
    d = _month_end(y, m)
    return d - dt.timedelta(days=(d.weekday() - 5) % 7)


def period_ends(fye, retail, first_year=2016, last_year=2027):
    """[(fiscal_year_label, fiscal_quarter, period_end)] in order. Retailers on 52-53 week years end on the last
    Saturday of the month and label the fiscal year by the calendar year it starts in."""
    out = []
    for fy in range(first_year, last_year + 1):
        for q in (1, 2, 3, 4):
            m = (fye - 1 - 3 * (4 - q)) % 12 + 1
            end_year = fy if m <= fye else fy - 1
            if retail:
                end_year = fy + 1 if m <= fye else fy
                pe = _last_saturday(end_year, m)
            else:
                pe = _month_end(end_year, m)
            out.append((fy, q, pe))
    out.sort(key=lambda r: r[2])
    return out


def _trading_on_or_after(d):
    while d not in U.DIDX:
        d += dt.timedelta(days=1)
    return d


def schedule(secs):
    """Per security: its fiscal year end, its periods, and for each period reported while it was listed the press
    release (date, time, code), the filing (date, form), the reaction day and the economic results."""
    rng = U.rng_for(2)
    out = {}
    for s in secs:
        retail = s["sector"] in (3, 4) and rng.random() < 0.35
        fye = 1 if retail else int(rng.choice(FYE_CHOICES[:4], p=np.array(FYE_P[:4]) / sum(FYE_P[:4])))
        habit = str(rng.choice(["AMC", "BMO", "DMT"], p=[0.6, 0.36, 0.04]))
        lag_q = int(rng.integers(24, 40))
        lag_k = int(rng.integers(38, 62))
        first_day = U.DAYS[s["first"]] + dt.timedelta(days=20) if s["kind"] != "initial" else dt.date(2017, 1, 15)
        last_day = U.DAYS[s["last"]] if s["last"] is not None else W.FUND_PULLED
        rows = []
        for fy, q, pe in period_ends(fye, retail):
            lag = (lag_k if q == 4 else lag_q) + int(rng.integers(-4, 5))
            ann = pe + dt.timedelta(days=lag)
            while ann.weekday() >= 5:
                ann += dt.timedelta(days=1)
            if ann < first_day or ann > last_day or pe < dt.date(2016, 12, 1):
                continue
            code = habit if rng.random() < 0.9 else str(rng.choice(["AMC", "BMO"]))
            if code == "AMC":
                t = dt.time(16, int(rng.choice([1, 2, 3, 4, 5, 5, 5, 10, 15, 30])), 0)
            elif code == "BMO":
                t = dt.time(int(rng.choice([6, 7, 7, 7, 8])), int(rng.choice([0, 0, 0, 15, 30, 45])), 0)
            else:
                t = dt.time(12, 0, 0)
            if ann >= W.START and ann not in U.DIDX:   # a release due on an exchange holiday goes out the next day
                ann = _trading_on_or_after(ann)
            if ann < W.START:
                react = None
            elif code in ("BMO", "DMT"):
                react = ann
            else:
                react = _trading_on_or_after(ann + dt.timedelta(days=1)) if ann < W.END else None
            filing_gap = int(rng.integers(0, 14)) if q != 4 else int(rng.integers(4, 26))
            filed = ann + dt.timedelta(days=filing_gap)
            while filed.weekday() >= 5:
                filed += dt.timedelta(days=1)
            react_i = U.DIDX.get(react) if react is not None else None
            if s["last"] is not None and react_i is not None and react_i > s["last"]:
                react_i = None
            rows.append(dict(fy=fy, q=q, pe=pe, ann=ann, time=t, code=code, react=react_i, filed=filed,
                             form="10-K" if q == 4 else "10-Q"))
        out[s["k"]] = dict(fye=fye, retail=retail, habit=habit, periods=rows)
    _results(secs, out, rng)
    return out


def _results(secs, sched, rng):
    """Quarterly economic results per share: revenue, operating income, net income, and the standardised surprise
    the market reacts to (this quarter's EPS against the same quarter a year earlier, scaled by the spread of those
    changes)."""
    for s in secs:
        sc = sched[s["k"]]
        rows = sc["periods"]
        n = len(rows)
        if not n:
            continue
        price0 = s["price0"]
        loss = s["sector"] == 5 and rng.random() < 0.45
        pe0 = float(np.exp(rng.normal(np.log(19.0), 0.3)))
        eps_a = price0 / pe0 if not loss else -price0 * float(rng.uniform(0.04, 0.12))
        sales_a = price0 * float(np.exp(rng.normal(np.log(0.9), 0.55))) * SALES_TO_PRICE[s["sector"]]
        g = s["growth"]
        season = np.array([1.0, 1.0, 1.0, 1.0])
        if s["sector"] in (3, 4):
            season = np.array([0.93, 0.97, 0.98, 1.12])
        if sc["retail"]:
            season = np.array([0.96, 0.98, 0.94, 1.12])
        ar = 0.0
        for i, r in enumerate(rows):
            yrs = (r["pe"] - dt.date(2018, 1, 1)).days / 365.25
            ar = 0.6 * ar + rng.normal(0, 0.06)
            lvl = (1 + g) ** yrs * season[r["q"] - 1] * (1 + ar)
            rev = sales_a / 4 * lvl * float(np.exp(rng.normal(0, 0.025)))
            if s.get("distress"):
                d = s["distress"]
                st = U.DAYS[d["start"]]
                if r["pe"] >= st:
                    k = (r["pe"] - st).days / 365.25
                    rev *= float(np.exp(-0.45 * k))
            margin_base = eps_a / sales_a if sales_a else 0.0
            eps = rev * margin_base * (1 + rng.normal(0, 0.14)) + rng.normal(0, abs(eps_a) * 0.035)
            if s.get("distress") and r["pe"] >= U.DAYS[s["distress"]["start"]]:
                eps = -abs(eps) - abs(eps_a) * 0.12 * (1 + (r["pe"] - U.DAYS[s["distress"]["start"]]).days / 365.25)
            r["rev"] = rev
            r["eps"] = eps
            r["opi"] = eps * float(rng.uniform(1.25, 1.45)) if eps > 0 else eps * float(rng.uniform(0.75, 0.95))
        eps = np.array([r["eps"] for r in rows])
        for i, r in enumerate(rows):
            if i >= 4:
                d = eps[i] - eps[i - 4]
                hist = np.diff(eps[max(0, i - 12):i + 1], 4) if i >= 8 else eps[max(0, i - 8):i + 1] - eps.mean()
                sd = float(np.std(hist)) or abs(eps_a) * 0.05 or 0.01
                r["sue"] = float(np.clip(d / max(sd, abs(eps_a) * 0.02, 0.005), -4, 4))
            else:
                r["sue"] = 0.0
