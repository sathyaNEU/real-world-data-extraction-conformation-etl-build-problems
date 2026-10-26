"""The golden and every route on the ladder, computed from the pack as shipped (pack_read), never from the world.

The golden counts each 2025-26 arrival whose stay had reached its first anniversary at the 31 August 2026 cut, and
counts each stay still open at the cut at the share of the 2024-25 arrivals of the same sector and the same migration
history (whether the person's previous stay ended in the twelve months before this arrival) still on the island the
same whole months after arriving whose stays reached their anniversary."""
import collections
import datetime as dt

import numpy as np

import pack_read as PR

D = dt.date
CUT = D(2026, 8, 31)
Y25 = (D(2025, 7, 1), D(2026, 6, 30))
Y24 = (D(2024, 7, 1), D(2025, 6, 30))
Y23 = (D(2023, 7, 1), D(2024, 6, 30))
ALLOWANCE = {"HOS": 230, "AGR": 110, "CON": 210, "FIN": 350, "HSC": 420, "RET": 170, "DIG": 190, "OTH": 300}
BACK_YEARS = (2018, 2019, 2020, 2021, 2022)


def anniversary(a):
    return D(a.year + 1, 3, 1) if (a.month, a.day) == (2, 29) else D(a.year + 1, a.month, a.day)


def months(a, d):
    """whole calendar months from a to d"""
    return (d.year - a.year) * 12 + d.month - a.month - (d.day < a.day)


def in_year(a, y):
    return y[0] <= a <= y[1]


class Pack:
    def __init__(self, target=PR.TARGET):
        self.__dict__.update(PR.read(target))
        self.by_reg = collections.defaultdict(list)
        for r in self.cur:
            self.by_reg[r["reg"]].append(r)
        self.legacy_leaves = collections.defaultdict(list)    # stays closed before the move, by current number
        for a in self.arc:
            if a["closure"] == "LEFT":
                self.legacy_leaves[self.xw[a["legacy"]]].append(a["leave"])

    def history(self, r, window=365):
        """the person's previous stay, in either register system, ended within `window` days before this arrival"""
        for o in self.by_reg[r["reg"]]:
            if o is not r and o["leave"] is not None and o["leave"] < r["arrive"] and \
                    (r["arrive"] - o["leave"]).days <= window:
                return True
        return any(lv < r["arrive"] and (r["arrive"] - lv).days <= window for lv in self.legacy_leaves.get(r["reg"], ()))

    def cohort(self, y):
        return [r for r in self.cur if r["origin"] == "ARRIVAL" and in_year(r["arrive"], y)]


def state(r, cut=CUT):
    an = anniversary(r["arrive"])
    if r["leave"] is not None and r["leave"] < an:
        return "short"
    if an <= cut:
        return "long"
    return "open"


def resolved_long(r):
    return r["leave"] is None or r["leave"] >= anniversary(r["arrive"])


def present(r, m, unit="month"):
    if r["leave"] is None:
        return True
    if unit == "month":
        return months(r["arrive"], r["leave"]) >= m
    return (r["leave"] - r["arrive"]).days >= m * unit


def elapsed(r, unit="month", cut=CUT):
    return months(r["arrive"], cut) if unit == "month" else (cut - r["arrive"]).days // unit


def completion(P, key, ref=None, unit="month", cohort=None):
    """each sector's provisional count: resolved long stays plus each open stay at the reference's share long among
    those still present after the same elapsed time, within the cell `key` names"""
    ref = ref if ref is not None else P.cohort(Y24)
    cohort = cohort if cohort is not None else P.cohort(Y25)
    t = collections.defaultdict(lambda: [0, 0])
    top = 13 if unit == "month" else 400 // unit + 1
    for r in ref:
        lg = resolved_long(r)
        for m in range(top):
            if present(r, m, unit):
                c = t[key(r, m)]
                c[0] += 1
                c[1] += lg
            else:
                break
    out = collections.Counter({s: 0.0 for s in P.sectors})
    for r in cohort:
        st = state(r)
        if st == "long":
            out[r["sector"]] += 1
        elif st == "open":
            n, lg = t.get(key(r, elapsed(r, unit)), (0, 0))
            out[r["sector"]] += lg / n if n else 0.0
    return out


def flat(P, key):
    """each open stay at the share of all the 2024-25 arrivals in its cell that reached twelve months, time on the
    island set aside"""
    t = collections.defaultdict(lambda: [0, 0])
    for r in P.cohort(Y24):
        c = t[key(r)]
        c[0] += 1
        c[1] += resolved_long(r)
    out = collections.Counter({s: 0.0 for s in P.sectors})
    for r in P.cohort(Y25):
        st = state(r)
        if st == "long":
            out[r["sector"]] += 1
        elif st == "open":
            n, lg = t.get(key(r), (0, 0))
            out[r["sector"]] += lg / n if n else 0.0
    return out


def golden(P):
    return completion(P, lambda r, m: (r["sector"], P.history(r), m))


def designated(fig):
    return sorted(s for s, v in fig.items() if v > ALLOWANCE[s])


def logistic(P, with_history=True):
    """a logistic model of reaching the anniversary on the reference arrivals still present at each month: sector,
    months present, sex, age band, nationality group and parish, with and without the history flag"""
    def feats(r, m):
        age = r["arrive"].year - r["yob"]
        f = ["s:" + r["sector"], "m:%d" % m, "sex:" + r["sex"], "age:%d" % min(5, max(0, (age - 18) // 8)),
             "nat:" + (r["nat"] if r["nat"] in ("GBR", "IRL", "POL", "ROU", "PHL", "IND") else "other"),
             "par:" + r["parish"]]
        if with_history:
            f.append("h:%s:%d" % (r["sector"], P.history(r)))
        return f
    rows, ys = [], []
    for r in P.cohort(Y24):
        lg = resolved_long(r)
        for m in range(13):
            if not present(r, m):
                break
            rows.append(feats(r, m))
            ys.append(lg)
    vocab = sorted({f for fs in rows for f in fs})
    ix = {f: i for i, f in enumerate(vocab)}
    X = np.zeros((len(rows), len(vocab) + 1))
    X[:, -1] = 1
    for i, fs in enumerate(rows):
        for f in fs:
            X[i, ix[f]] = 1
    y = np.array(ys, float)
    b = np.zeros(X.shape[1])
    for _ in range(60):                       # Newton steps with a light ridge
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (p - y) + 1e-3 * b
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-3 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    out = collections.Counter({s: 0.0 for s in P.sectors})
    for r in P.cohort(Y25):
        st = state(r)
        if st == "long":
            out[r["sector"]] += 1
        elif st == "open":
            x = np.zeros(len(b))
            x[-1] = 1
            for f in feats(r, elapsed(r)):
                if f in ix:
                    x[ix[f]] = 1
            out[r["sector"]] += 1 / (1 + np.exp(-x @ b))
    return out


def km_pooled(P):
    """a Kaplan-Meier curve by sector on every arrival from 1 July 2024, censored at the cut, read as S(12)/S(m)"""
    out = collections.Counter({s: 0.0 for s in P.sectors})
    pool = [r for r in P.cur if r["origin"] == "ARRIVAL" and Y24[0] <= r["arrive"] <= Y25[1]]
    for s in P.sectors:
        rs = [r for r in pool if r["sector"] == s]
        S = [1.0]
        for m in range(12):
            at = [r for r in rs if months(r["arrive"], CUT) > m and present(r, m)]
            ex = [r for r in at if r["leave"] is not None and months(r["arrive"], r["leave"]) == m
                  and r["leave"] < anniversary(r["arrive"])]
            S.append(S[-1] * (1 - len(ex) / len(at)) if at else S[-1])
        for r in P.cohort(Y25):
            if r["sector"] != s:
                continue
            st = state(r)
            if st == "long":
                out[s] += 1
            elif st == "open":
                m = elapsed(r)
                out[s] += S[12] / S[m] if S[m] else 0.0
    return out


def routes(P):
    """every route on the ladder and every member of the two families, each sector's figure"""
    R = collections.OrderedDict()
    c25 = P.cohort(Y25)
    R["every_arrival"] = collections.Counter({s: sum(1 for r in c25 if r["sector"] == s) for s in P.sectors})
    R["resolved_only"] = collections.Counter({s: sum(1 for r in c25 if r["sector"] == s and state(r) == "long")
                                              for s in P.sectors})
    R["open_counted_long"] = collections.Counter({s: sum(1 for r in c25 if r["sector"] == s and state(r) != "short")
                                                  for s in P.sectors})
    R["flat_sector"] = flat(P, lambda r: (r["sector"],))
    R["flat_sector_history"] = flat(P, lambda r: (r["sector"], P.history(r)))
    R["sector"] = completion(P, lambda r, m: (r["sector"],))
    R["sector_months"] = completion(P, lambda r, m: (r["sector"], m))
    R["sector_arrival_month_months"] = completion(P, lambda r, m: (r["sector"], r["arrive"].month, m))
    R["sector_months_30day"] = completion(P, lambda r, m: (r["sector"], m), unit=30)
    R["sector_sex_months"] = completion(P, lambda r, m: (r["sector"], r["sex"], m))
    R["sector_months_ref_2023_25"] = completion(P, lambda r, m: (r["sector"], m), ref=P.cohort(Y23) + P.cohort(Y24))
    R["logistic_no_history"] = logistic(P, with_history=False)
    R["km_pooled_2024_26"] = km_pooled(P)
    R["golden"] = golden(P)
    R["history_6_months"] = completion(P, lambda r, m: (r["sector"], P.history(r, 183), m))
    R["history_any"] = completion(P, lambda r, m: (r["sector"], P.history(r, 99999), m))
    R["history_12_no_months"] = completion(P, lambda r, m: (r["sector"], P.history(r)))
    R["history_12_30day"] = completion(P, lambda r, m: (r["sector"], P.history(r), m), unit=30)
    R["history_12_weeks"] = completion(P, lambda r, m: (r["sector"], P.history(r), m), unit=7)
    R["history_12_days"] = completion(P, lambda r, m: (r["sector"], P.history(r), m), unit=1)
    R["logistic_with_history"] = logistic(P, with_history=True)
    return R


EASY = ("sector", "sector_months", "sector_arrival_month_months", "sector_months_30day", "sector_sex_months",
        "sector_months_ref_2023_25", "logistic_no_history", "km_pooled_2024_26")
STANDING = ("golden", "history_6_months", "history_any", "history_12_30day", "history_12_weeks", "history_12_days",
            "logistic_with_history")


# ------------------------------------------------------------------------------------------------ the ask

DECLARED = ("arrive", "sex", "yob", "nat", "code")


def back_stays(P, how="golden"):
    """the stays the back series counts, as (arrival date, sector, leaving date or None).

    golden: the legacy archive's records, each record open at the move taking the leaving date (and notice date) of
    the TRANSFER record its legacy number's current number holds, and one stay kept of any records identical in every
    declared particular whose stays ended on the same day on notices received the same day (the same stay registered
    at a second parish office, both records closed by its one leaving notice); and the current system's own arrivals.
    The other handlings are the ones a response is likely to take."""
    tr = {r["reg"]: r for r in P.cur if r["origin"] == "TRANSFER"}
    recs = []
    for a in P.arc:
        if a["closure"] == "LEFT":
            recs.append(dict(a, notice=a["closed"]))
        elif how != "current_transfer" and how != "current_transfer_twins" and how != "both":
            t = tr[P.xw[a["legacy"]]]
            d = dict(a, leave=t["leave"], notice=t["notice"])
            if how == "stitch_current_date":
                d["arrive"] = t["arrive"]
            if how == "stitch_current_activity":
                d["sector"] = t["sector"]
            recs.append(d)
        else:
            recs.append(dict(a, leave=a["closed"], notice=a["closed"]) if how == "both" else None)
    recs = [x for x in recs if x is not None]
    if how in ("current_transfer", "current_transfer_twins", "both"):
        recs += [dict(r, closure="TRANSFER") for r in P.cur if r["origin"] == "TRANSFER"]
    seen, stays = set(), []
    for x in recs:
        if how in ("golden", "current_transfer_twins", "stitch_current_activity", "stitch_current_date") \
                and x["leave"] is not None:
            k = tuple(x[f] for f in DECLARED) + (x["leave"], x["notice"])
            if k in seen:
                continue
            seen.add(k)
        elif how == "declared_dedupe":
            k = tuple(x[f] for f in DECLARED)
            if k in seen:
                continue
            seen.add(k)
        elif how == "open_pairs_once" or (how == "leave_only" and x["leave"] is not None):
            k = tuple(x[f] for f in DECLARED) + ((x["leave"], x["notice"]) if how == "open_pairs_once" else (x["leave"],))
            if k in seen:
                continue
            seen.add(k)
        stays.append((x["arrive"], x["sector"], x["leave"]))
    for r in P.cur:
        if r["origin"] == "ARRIVAL":
            stays.append((r["arrive"], r["sector"], r["leave"]))
    return stays


def back_series(P, how="golden"):
    """each sector's arrivals registered for work and final long-term immigration, years to 30 June 2019 to 2023"""
    stays = back_stays(P, how)
    arr, lng = {}, {}
    for y in BACK_YEARS:
        win = (D(y, 7, 1), D(y + 1, 6, 30))
        a = collections.Counter({s: 0 for s in P.sectors})
        lg = collections.Counter({s: 0 for s in P.sectors})
        for arrive, sector, leave in stays:
            if in_year(arrive, win):
                a[sector] += 1
                if leave is None or leave >= anniversary(arrive):
                    lg[sector] += 1
        arr[y], lng[y] = a, lg
    return arr, lng


# ------------------------------------------------------------------------------------------------ the filed back-test

CUT25, EXT25 = D(2025, 8, 31), D(2025, 9, 30)


def state25(r):
    an = anniversary(r["arrive"])
    if r["leave"] is not None and r["leave"] <= CUT25 and r["notice"] <= EXT25 and r["leave"] < an:
        return "short"
    if an <= CUT25:
        return "long"
    return "open"


def backtest(P, key, unit="month", flat=False):
    """the methods note's test: chances estimated in the same way from the 2023-24 arrivals, given to the 2024-25
    arrivals still open at 31 August 2025, scored against whether each reached its anniversary (Brier score)"""
    t = collections.defaultdict(lambda: [0, 0])
    top = 13 if unit == "month" else 400 // unit + 1
    for r in P.cohort(Y23):
        lg = resolved_long(r)
        if flat:
            c = t[key(r, 0)]
            c[0] += 1
            c[1] += lg
            continue
        for m in range(top):
            if not present(r, m, unit):
                break
            c = t[key(r, m)]
            c[0] += 1
            c[1] += lg
    scored = [r for r in P.cohort(Y24) if r["registered"] <= EXT25 and state25(r) == "open"]
    base = sum(map(resolved_long, scored)) / len(scored)
    err = 0.0
    for r in scored:
        m = 0 if flat else elapsed(r, unit, CUT25)
        n, lg = t.get(key(r, m), (0, 0))
        p = lg / n if n else base
        err += (p - resolved_long(r)) ** 2
    return err / len(scored), len(scored)


def backtests(P):
    """the candidates a compiler would try, scored on the filed test"""
    h = P.history
    out = collections.OrderedDict()
    out["flat_sector"] = backtest(P, lambda r, m: (r["sector"],), flat=True)
    out["flat_sector_history"] = backtest(P, lambda r, m: (r["sector"], h(r)), flat=True)
    out["sector_months"] = backtest(P, lambda r, m: (r["sector"], m))
    out["sector_months_30day"] = backtest(P, lambda r, m: (r["sector"], m), unit=30)
    out["sector_arrival_month_months"] = backtest(P, lambda r, m: (r["sector"], r["arrive"].month, m))
    out["sector_sex_months"] = backtest(P, lambda r, m: (r["sector"], r["sex"], m))
    out["golden"] = backtest(P, lambda r, m: (r["sector"], h(r), m))
    out["history_6_months"] = backtest(P, lambda r, m: (r["sector"], h(r, 183), m))
    out["history_any"] = backtest(P, lambda r, m: (r["sector"], h(r, 99999), m))
    out["history_12_30day"] = backtest(P, lambda r, m: (r["sector"], h(r), m), unit=30)
    out["history_12_weeks"] = backtest(P, lambda r, m: (r["sector"], h(r), m), unit=7)
    return out


def summary(target=PR.TARGET):
    P = Pack(target)
    return P, routes(P), back_series(P)
