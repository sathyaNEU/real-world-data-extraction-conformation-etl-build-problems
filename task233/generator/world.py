"""The clean truth for task233 architecture 3: outlets, quotes, daily shelf-price paths, the
contractor's monthly collection with each collector's recording, and the Field Quality Team's
third-quarter back-checks. Nothing here is written to target/; pack.py writes the exports."""
import bisect
import datetime as dt
import math

import numpy as np

import params as P
from items import ITEMS, KIND_ITEMS

ITEM = {c: dict(code=c, group=g, desc=d, unit=u, base=b) for c, g, d, u, b in ITEMS}


def stream(k):
    return np.random.default_rng([P.SEED, k])


def day(d):
    return (d - P.PATH_START).days


def date_of(n):
    return P.PATH_START + dt.timedelta(days=int(n))


def is_workday(d):
    return d.weekday() < 5 and d not in P.HOLIDAYS


def next_workday(d):
    while not is_workday(d):
        d += dt.timedelta(days=1)
    return d


def index_day(y, m):
    d = dt.date(y, m, 1)
    tues = [d + dt.timedelta(days=i) for i in range(31)
            if (d + dt.timedelta(days=i)).month == m and (d + dt.timedelta(days=i)).weekday() == 1]
    return tues[1]


def window(y, m):
    d = index_day(y, m)
    out = []
    while len(out) < P.WINDOW_WORKDAYS:
        if is_workday(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def after_window(y, m, k):
    """the k-th working day after the window closes"""
    d = window(y, m)[-1]
    n = 0
    while n < k:
        d += dt.timedelta(days=1)
        if is_workday(d):
            n += 1
    return d


def fqt_date(region, y, m):
    return next_workday(index_day(y, m) + dt.timedelta(days=P.FQT_OFFSET[region]))


def snap(p):
    """a shelf price on the retail grid: x.x9 under 20 dollars, x.99 or x.49 above"""
    if p < 20:
        return max(0.49, math.floor(p * 10) / 10 + 0.09)
    if p < 60:
        return math.floor(p * 2) / 2 + 0.49 if (p * 2) % 2 < 1 else math.floor(p) + 0.99
    return math.floor(p) + 0.99


class World:
    def __init__(self, err_scale=None):
        self.regions = [dict(code=r[0], name=r[1], cname=r[2], ring=r[3], nm=r[4], ni=r[5]) for r in P.REGIONS]
        self.months = P.MONTHS
        self.err_scale = err_scale or {}
        self._outlets()
        self._quotes()
        self._paths()
        self._visits()
        self._collection()
        self._backchecks()

    # outlets -------------------------------------------------------------------------------
    def _outlets(self):
        rng = stream(1)
        kinds_m = [k for k, v in P.KINDS.items() if v[0] == "M"]
        kinds_i = [k for k, v in P.KINDS.items() if v[0] == "I"]
        pm = np.array([P.KINDS[k][1] for k in kinds_m]); pm /= pm.sum()
        pi = np.array([P.KINDS[k][1] for k in kinds_i]); pi /= pi.sum()
        self.outlets = []
        codes = rng.choice(np.arange(10000, 99999), size=600, replace=False)
        tnums = rng.choice(np.arange(1000, 9999), size=600, replace=False)
        n = 0
        for r in self.regions:
            for stratum, count, kinds, probs in (("M", r["nm"], kinds_m, pm), ("I", r["ni"], kinds_i, pi)):
                for j in range(count):
                    kind = kinds[rng.choice(len(kinds), p=probs)]
                    self.outlets.append(dict(oid=n, nso_code="OT%05d" % codes[n], tnum="T%04d" % tnums[n],
                                             region=r["code"], stratum=stratum, kind=kind,
                                             factor=float(np.exp(rng.normal(0.0, 0.05)) * (1.12 if kind == "convenience" else 1.0))))
                    n += 1

    # quotes ----------------------------------------------------------------------------------
    def _quotes(self):
        rng = stream(2)
        self.quotes = []
        qcodes = rng.choice(np.arange(100000, 999999), size=8000, replace=False)
        n = 0
        for o in self.outlets:
            kind = P.KINDS[o["kind"]]
            pool = KIND_ITEMS.get(o["kind"]) or [c for c, it in ITEM.items() if it["group"] in kind[3]]
            k = int(rng.integers(kind[2][0], kind[2][1] + 1))
            k = min(k, len(pool))
            chosen = sorted(rng.choice(pool, size=k, replace=False).tolist())
            for c in chosen:
                self.quotes.append(dict(qid=n, quote_id="%06d" % qcodes[n], oid=o["oid"], item=c,
                                        group=ITEM[c]["group"], stratum=o["stratum"], region=o["region"]))
                n += 1

    # daily shelf prices ----------------------------------------------------------------------
    def hazard(self, group, stratum):
        f = P.GROUPS[group][1 if stratum == "M" else 2]
        return -math.log(1.0 - f) / 30.4

    def _paths(self):
        rng = stream(3)
        span = day(P.PATH_END) + 1
        self.path_days = []
        self.path_prices = []
        for q in self.quotes:
            o = self.outlets[q["oid"]]
            base = ITEM[q["item"]]["base"] * o["factor"] * float(np.exp(rng.normal(0.0, 0.07)))
            p = snap(base)
            h = self.hazard(q["group"], q["stratum"])
            nev = int(rng.poisson(h * span))
            ev = sorted(set(int(x) for x in rng.integers(1, span, size=nev)))
            days_, prices = [0], [p]
            for d in ev:
                mult = float(np.exp(rng.normal(0.012, 0.055)))
                newp = snap(prices[-1] * mult)
                if abs(newp - prices[-1]) < 0.005:
                    newp = snap(prices[-1] * (1.08 if rng.random() < 0.7 else 0.92))
                if abs(newp - prices[-1]) < 0.005:
                    newp = round(prices[-1] + 0.10, 2)
                days_.append(d)
                prices.append(round(newp, 2))
            self.path_days.append(days_)
            self.path_prices.append(prices)

    def true_price(self, qid, d):
        i = bisect.bisect_right(self.path_days[qid], d) - 1
        return self.path_prices[qid][i]

    def changed_between(self, qid, d0, d1):
        """whether the shelf price moved after day d0 and on or before day d1"""
        dd = self.path_days[qid]
        return bisect.bisect_right(dd, d1) - bisect.bisect_right(dd, d0) > 0

    # monthly visits ------------------------------------------------------------------------
    def _visits(self):
        rng = stream(4)
        self.visits = []
        self.vis_index = {}
        for (y, m) in self.months:
            win = window(y, m)
            for o in self.outlets:
                u_late, u_day, u_k, u_split = rng.random(4)
                wts = np.array(P.VISIT_WEIGHTS[o["stratum"]])
                if u_late < P.LATE_VISIT:
                    vday = after_window(y, m, 1 + int(u_k * 3))
                else:
                    vday = win[int(np.searchsorted(np.cumsum(wts), u_day * wts.sum()))]
                vdays = [vday]
                if o["kind"] == "supermarket" and u_split < P.SPLIT_VISIT:
                    vdays.append(next_workday(vday + dt.timedelta(days=1)))
                v = dict(oid=o["oid"], y=y, m=m, days=vdays, win=win)
                self.visits.append(v)
                self.vis_index[(o["oid"], y, m)] = v

    # monthly collection ----------------------------------------------------------------------
    def _collection(self):
        rng = stream(6)
        self.records = []      # quote-month records
        last = {}              # qid -> (recorded price, true price at the time) for the pre-fill
        rescale = {}           # qid -> factor applied after a variety replacement
        for (y, m) in self.months:
            for q in self.quotes:
                v = self.vis_index[(q["oid"], y, m)]
                u = rng.random(8)
                vd = v["days"][0] if len(v["days"]) == 1 else v["days"][int(u[0] < 0.5)]
                sc = self.err_scale.get(q["region"], 1.0)
                key, size, stale = (x * sc for x in P.ERRORS[q["region"]])
                rec = dict(qid=q["qid"], y=y, m=m, vday=vd, status="P", price=None, true=None, err=None)
                if u[1] < P.STATUS_UNAVAILABLE:
                    rec["status"] = "U"
                    self.records.append(rec)
                    continue
                if u[1] < P.STATUS_UNAVAILABLE + P.STATUS_REPLACED:
                    rec["status"] = "R"
                    rescale[q["qid"]] = rescale.get(q["qid"], 1.0) * float(np.exp(0.12 * _norm(u[2])))
                f = rescale.get(q["qid"], 1.0)
                tp = round(snap(self.true_price(q["qid"], day(vd)) * f), 2) if f != 1.0 else self.true_price(q["qid"], day(vd))
                rec["true"], rec["scale"] = tp, f
                price, err = tp, None
                prev = last.get(q["qid"])
                if rec["status"] == "P" and prev is not None and abs(prev[1] - tp) > 0.004 and u[3] < stale:
                    price, err = prev[0], "stale"
                elif u[4] < key:
                    price, err = self._slip(tp, u[5], u[6]), "keying"
                elif u[4] < key + size:
                    price, err = round(snap(tp * [0.55, 0.7, 1.4, 1.8][int(u[7] * 4)]), 2), "variety"
                if err is not None and abs(price - tp) < 0.005:
                    price, err = tp, None
                rec["price"], rec["err"] = round(price, 2), err
                last[q["qid"]] = (rec["price"], tp)
                self.records.append(rec)
        self.rescale = rescale
        self.rec_index = {(r["qid"], r["y"], r["m"]): r for r in self.records}

    @staticmethod
    def _slip(p, kind, pos):
        s = "%.2f" % p
        digits = [i for i, ch in enumerate(s) if ch.isdigit()]
        if kind < 0.45 and len(digits) >= 2:
            i = int(pos * (len(digits) - 1))
            a, b = digits[i], digits[i + 1]
            lst = list(s)
            lst[a], lst[b] = lst[b], lst[a]
            v = float("".join(lst))
        elif kind < 0.85:
            v = p + [-1.0, -0.1, 0.1, 1.0][int(pos * 4)]
        else:
            v = p * 10 if p < 10 else p / 10
        return round(max(v, 0.09), 2)

    # back-checks -----------------------------------------------------------------------------
    def expected_change(self, qid, d0, d1):
        q = self.quotes[qid]
        return 1.0 - math.exp(-self.hazard(q["group"], q["stratum"]) * max(0, d1 - d0))

    def _backchecks(self):
        self.backchecks = []
        qs_by_outlet = {}
        for q in self.quotes:
            qs_by_outlet.setdefault(q["oid"], []).append(q)
        for (y, m) in P.QUARTER:
            for ri, r in enumerate(self.regions):
                fd = fqt_date(r["code"], y, m)
                best = None
                for attempt in range(P.FQT_TRIES):
                    rng = np.random.default_rng([P.SEED, 7, y, m, ri, attempt])
                    rows, dev = [], 0.0
                    for stratum, k in (("M", P.FQT_MULTIPLES), ("I", P.FQT_INDEPENDENTS)):
                        elig = []
                        for o in self.outlets:
                            if o["region"] != r["code"] or o["stratum"] != stratum:
                                continue
                            v = self.vis_index[(o["oid"], y, m)]
                            if len(v["days"]) == 1 and v["days"][0] in v["win"][:P.FQT_DRAW_DAYS] and v["days"][0] <= fd:
                                elig.append(o)
                        pick = rng.choice(len(elig), size=min(k, len(elig)), replace=False)
                        for j in sorted(pick.tolist()):
                            o = elig[j]
                            for q in qs_by_outlet[o["oid"]]:
                                rec = self.rec_index[(q["qid"], y, m)]
                                if rec["status"] == "U":
                                    continue
                                found = rng.random() > P.FQT_NOT_FOUND
                                f = rec["scale"]
                                tp = self.true_price(q["qid"], day(fd))
                                fp = (round(snap(tp * f), 2) if f != 1.0 else tp) if found else None
                                ch = self.changed_between(q["qid"], day(rec["vday"]), day(fd))
                                ex = self.expected_change(q["qid"], day(rec["vday"]), day(fd))
                                if found:
                                    dev += ch - ex
                                rows.append(dict(qid=q["qid"], oid=o["oid"], region=r["code"], y=y, m=m,
                                                 fqt=fd, vday=rec["vday"], rec_price=rec["price"],
                                                 fqt_price=fp, err=rec["err"], changed=ch, expected=ex))
                    if best is None or abs(dev) < best[0]:
                        best = (abs(dev), rows)
                self.backchecks.extend(best[1])


def _norm(u):
    """a standard normal quantile from one uniform (Acklam's rational approximation)"""
    u = min(max(u, 1e-9), 1 - 1e-9)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    pl, ph = 0.02425, 1 - 0.02425
    if u < pl:
        qq = math.sqrt(-2 * math.log(u))
        return (((((c[0]*qq+c[1])*qq+c[2])*qq+c[3])*qq+c[4])*qq+c[5]) / ((((d[0]*qq+d[1])*qq+d[2])*qq+d[3])*qq+1)
    if u > ph:
        qq = math.sqrt(-2 * math.log(1 - u))
        return -(((((c[0]*qq+c[1])*qq+c[2])*qq+c[3])*qq+c[4])*qq+c[5]) / ((((d[0]*qq+d[1])*qq+d[2])*qq+d[3])*qq+1)
    qq = u - 0.5
    rr = qq * qq
    return (((((a[0]*rr+a[1])*rr+a[2])*rr+a[3])*rr+a[4])*rr+a[5])*qq / (((((b[0]*rr+b[1])*rr+b[2])*rr+b[3])*rr+b[4])*rr+1)


if __name__ == "__main__":
    w = World()
    print(len(w.outlets), "outlets", len(w.quotes), "quotes", len(w.records), "records", len(w.backchecks), "back-checks")
