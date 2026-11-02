"""The clean truth for task233 architecture 3: outlets, quotes, daily shelf-price paths, the
contractor's monthly collection with each collector's recording, the Field Quality Team's
third-quarter back-checks, the contractor's quarterly schedule and the commodity team's
replacement reviews. Nothing here is written to target/; pack.py writes the exports."""
import bisect
import datetime as dt
import math

import numpy as np

import params as P
from items import ITEMS, KIND_ITEMS
from names import LOCALITIES, STREETS, SHOP_NAMES

ITEM = {c: dict(code=c, group=g, desc=d, unit=u, base=b) for c, g, d, u, b in ITEMS}


def stream(*k):
    return np.random.default_rng([P.SEED, *k])


def day(d):
    return (d - P.PATH_START).days


def is_workday(d):
    return d.weekday() < 5 and d not in P.HOLIDAYS


def next_workday(d):
    while not is_workday(d):
        d += dt.timedelta(days=1)
    return d


def add_workdays(d, k):
    n = 0
    while n < k:
        d += dt.timedelta(days=1)
        if is_workday(d):
            n += 1
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


def fqt_date(region, y, m):
    return next_workday(index_day(y, m) + dt.timedelta(days=P.FQT_OFFSET[region]))


def snap(p):
    """a shelf price on the retail grid: x.x9 under 20 dollars, x.49 or x.99 under 60, x.99 above"""
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
        self._forced_repeats()
        self._collection()
        self._backchecks()
        self._reviews()

    # outlets -------------------------------------------------------------------------------
    def _outlets(self):
        rng = stream(1)
        kinds_m = [k for k, v in P.KINDS.items() if v[0] == "M"]
        kinds_i = [k for k, v in P.KINDS.items() if v[0] == "I"]
        pm = np.array([P.KINDS[k][1] for k in kinds_m]); pm /= pm.sum()
        pi = np.array([P.KINDS[k][1] for k in kinds_i]); pi /= pi.sum()
        self.outlets = []
        codes = rng.choice(np.arange(10000, 99999), size=700, replace=False)
        tnums = rng.choice(np.arange(1000, 9999), size=700, replace=False)
        shop_order = rng.permutation(len(SHOP_NAMES))
        n = shop = 0
        for r in self.regions:
            locs = LOCALITIES[r["code"]]
            region_outlets = []
            for stratum, count, kinds, probs in (("M", r["nm"], kinds_m, pm), ("I", r["ni"], kinds_i, pi)):
                for j in range(count):
                    kind = kinds[rng.choice(len(kinds), p=probs)]
                    region_outlets.append(dict(stratum=stratum, kind=kind))
            # every region carries at least one branch of the pharmacy chain sold in August
            if not any(o["kind"] == "pharmacy_chain" for o in region_outlets):
                last_m = [i for i, o in enumerate(region_outlets) if o["stratum"] == "M"][-1]
                region_outlets[last_m]["kind"] = "pharmacy_chain"
            lifeline_done = False
            for o in region_outlets:
                kind = o["kind"]
                loc = locs[int(rng.integers(0, len(locs)))]
                street = STREETS[int(rng.integers(0, len(STREETS)))]
                number = int(rng.integers(1, 420))
                if kind in P.CHAINS:
                    if kind == "pharmacy_chain" and not lifeline_done:
                        chain = "Lifeline Chemists"
                        lifeline_done = True
                    else:
                        chain = P.CHAINS[kind][int(rng.integers(0, len(P.CHAINS[kind])))]
                    name = "%s %s" % (chain, loc)
                else:
                    chain = ""
                    name = SHOP_NAMES[shop_order[shop % len(SHOP_NAMES)]] % dict(loc=loc)
                    shop += 1
                self.outlets.append(dict(
                    oid=n, nso_code="OT%05d" % codes[n], tnum="T%04d" % tnums[n], region=r["code"],
                    stratum=o["stratum"], kind=kind, chain=chain, name=name, locality=loc,
                    address="%d %s, %s" % (number, street, loc),
                    factor=float(np.exp(rng.normal(0.0, 0.05)) * (1.12 if kind == "convenience" else 1.0)),
                    successor=None, predecessor=None,
                    added=dt.date(2019 + int(rng.integers(0, 6)), int(rng.integers(1, 13)), 1), removed=None))
                n += 1
        # the August sale of Lifeline Chemists' branches to CareMed Pharmacy: same store, new outlet
        for o in [x for x in self.outlets if x["chain"] == "Lifeline Chemists"]:
            succ = dict(o)
            succ.update(oid=n, nso_code="OT%05d" % codes[n], tnum="T%04d" % tnums[n], chain="CareMed Pharmacy",
                        name="CareMed Pharmacy %s" % o["locality"], successor=None, predecessor=o["oid"],
                        added=P.REBRAND_DATE, removed=None)
            o["successor"] = n
            o["removed"] = P.REBRAND_DATE - dt.timedelta(days=1)
            self.outlets.append(succ)
            n += 1
        self.base_outlets = [o for o in self.outlets if o["predecessor"] is None]

    def outlet_for(self, oid, y, m):
        """the outlet a quote sits at in a month (a sold branch's successor from the sale on)"""
        o = self.outlets[oid]
        if o["successor"] is not None and dt.date(y, m, 1) >= P.REBRAND_DATE:
            return self.outlets[o["successor"]]
        return o

    # quotes ----------------------------------------------------------------------------------
    def _quotes(self):
        rng = stream(2)
        self.quotes = []
        qcodes = rng.choice(np.arange(100000, 999999), size=8000, replace=False)
        n = 0
        for o in self.base_outlets:
            kind = P.KINDS[o["kind"]]
            pool = KIND_ITEMS.get(o["kind"]) or [c for c, it in ITEM.items() if it["group"] in kind[3]]
            k = min(int(rng.integers(kind[2][0], kind[2][1] + 1)), len(pool))
            chosen = sorted(rng.choice(pool, size=k, replace=False).tolist())
            for c in chosen:
                self.quotes.append(dict(qid=n, quote_id="%06d" % qcodes[n], oid=o["oid"], item=c,
                                        group=ITEM[c]["group"], stratum=o["stratum"], region=o["region"]))
                n += 1
        self.qid_of = {q["quote_id"]: q["qid"] for q in self.quotes}

    # daily shelf prices ----------------------------------------------------------------------
    def hazard(self, group, stratum):
        f = P.GROUPS[group][1 if stratum == "M" else 2]
        return -math.log(1.0 - f) / 30.4

    def _paths(self):
        rng = stream(3)
        span = day(P.PATH_END) + 1
        self.path_days, self.path_prices = [], []
        for q in self.quotes:
            o = self.outlets[q["oid"]]
            base = ITEM[q["item"]]["base"] * o["factor"] * float(np.exp(rng.normal(0.0, 0.07)))
            p = snap(base)
            h = self.hazard(q["group"], q["stratum"])
            nev = int(rng.poisson(h * span))
            ev = sorted(set(int(x) for x in rng.integers(1, span, size=nev)))
            days_, prices = [0], [p]
            for d in ev:
                newp = snap(prices[-1] * float(np.exp(rng.normal(0.012, 0.055))))
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
        dd = self.path_days[qid]
        return bisect.bisect_right(dd, d1) - bisect.bisect_right(dd, d0) > 0

    # monthly visits ------------------------------------------------------------------------
    def _visits(self):
        rng = stream(4)
        self.visits = []
        self.vis_index = {}
        for (y, m) in self.months:
            win = window(y, m)
            for o in self.base_outlets:
                u_miss, u_late, u_day, u_k, u_split = rng.random(5)
                wts = np.array(P.VISIT_WEIGHTS[o["stratum"]])
                if u_miss < P.MISSED_VISIT:
                    v = dict(oid=o["oid"], y=y, m=m, days=[], win=win)
                else:
                    if u_late < P.LATE_VISIT:
                        vday = add_workdays(win[-1], 1 + int(u_k * 3))
                    else:
                        vday = win[int(np.searchsorted(np.cumsum(wts), u_day * wts.sum()))]
                    vdays = [vday]
                    if o["kind"] == "supermarket" and u_split < P.SPLIT_VISIT:
                        vdays.append(next_workday(vday + dt.timedelta(days=1)))
                    v = dict(oid=o["oid"], y=y, m=m, days=vdays, win=win)
                self.visits.append(v)
                self.vis_index[(o["oid"], y, m)] = v

    def fqt_eligible(self, o, y, m):
        v = self.vis_index[(o["oid"], y, m)]
        return (o["chain"] != "Lifeline Chemists" and o["oid"] not in getattr(self, "fqt_excluded", ())
                and len(v["days"]) == 1
                and v["days"][0] in v["win"][:P.FQT_DRAW_DAYS] and v["days"][0] <= fqt_date(o["region"], y, m))

    def _forced_repeats(self):
        """one quote per region whose variety the collector replaces twice in the quarter, in two
        months when the Field Quality Team cannot draw its outlet"""
        self.forced = {}
        self.fqt_excluded = set()
        pairs = [((2026, 7), (2026, 9)), ((2026, 7), (2026, 8)), ((2026, 8), (2026, 9))]
        for r in self.regions:
            pick = None
            for m1, m2 in pairs:
                cands = []
                for q in self.quotes:
                    o = self.outlets[q["oid"]]
                    if q["region"] != r["code"] or o["chain"] == "Lifeline Chemists":
                        continue
                    v1, v2 = self.vis_index[(o["oid"],) + m1], self.vis_index[(o["oid"],) + m2]
                    if len(v1["days"]) != 1 or len(v2["days"]) != 1:
                        continue
                    if o["kind"] in ("supermarket", "pharmacy_chain", "clothing_chain"):
                        continue
                    cands.append(q)
                if cands:
                    pick = (sorted(cands, key=lambda x: x["quote_id"])[len(cands) // 2], m1, m2)
                    break
            if pick is None:
                raise RuntimeError("no repeat-replacement candidate in %s" % r["code"])
            q, m1, m2 = pick
            self.fqt_excluded.add(q["oid"])
            first = "Comparable" if int(r["code"][2:]) % 2 else "Not comparable"
            second = "Not comparable" if first == "Comparable" else "Comparable"
            self.forced[(q["qid"],) + m1] = first
            self.forced[(q["qid"],) + m2] = second

    # monthly collection ----------------------------------------------------------------------
    def _collection(self):
        rng = stream(6)
        self.records = []
        last, rescale = {}, {}
        for (y, m) in self.months:
            for q in self.quotes:
                v = self.vis_index[(q["oid"], y, m)]
                u = rng.random(9)
                if not v["days"]:
                    continue
                vd = v["days"][0] if len(v["days"]) == 1 else v["days"][int(u[0] < 0.5)]
                sc = self.err_scale.get(q["region"], 1.0)
                key, size, stale = (x * sc for x in P.ERRORS[q["region"]])
                rec = dict(qid=q["qid"], y=y, m=m, vday=vd, status="P", price=None, true=None, err=None,
                           scale=rescale.get(q["qid"], 1.0), variety_no=int(u[8] * 1000))
                forced = (q["qid"], y, m) in self.forced
                if u[1] < P.STATUS_UNAVAILABLE and not forced:
                    rec["status"] = "U"
                    self.records.append(rec)
                    continue
                if u[1] < P.STATUS_UNAVAILABLE + P.STATUS_REPLACED or forced:
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
        for ri, r in enumerate(self.regions):
            cands = []
            for (y, m) in P.QUARTER:
                fd = fqt_date(r["code"], y, m)
                month_c = []
                for attempt in range(P.FQT_TRIES):
                    rng = np.random.default_rng([P.SEED, 7, y, m, ri, attempt])
                    rows, dev = [], 0.0
                    for stratum, k in (("M", P.FQT_MULTIPLES), ("I", P.FQT_INDEPENDENTS)):
                        elig = []
                        for o in self.base_outlets:
                            if o["region"] != r["code"] or o["stratum"] != stratum:
                                continue
                            if self.fqt_eligible(o, y, m):
                                elig.append(o)
                        pick = rng.choice(len(elig), size=min(k, len(elig)), replace=False)
                        for j in sorted(pick.tolist()):
                            o = elig[j]
                            for q in qs_by_outlet[o["oid"]]:
                                rec = self.rec_index.get((q["qid"], y, m))
                                if rec is None or rec["status"] == "U":
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
                    month_c.append((dev, rows))
                cands.append(month_c)
            pop = [x for x in self.records if self.quotes[x["qid"]]["region"] == r["code"]
                   and (x["y"], x["m"]) in P.QUARTER and x["price"] is not None]
            prate = sum(x["err"] is not None for x in pop) / len(pop)
            stats = [[(c[0], sum(1 for x in c[1] if x["fqt_price"] is not None),
                       sum(1 for x in c[1] if x["fqt_price"] is not None and x["err"] is not None)) for c in mc]
                     for mc in cands]
            best = None
            for ia, a in enumerate(stats[0]):
                for ib, b in enumerate(stats[1]):
                    for ic, c in enumerate(stats[2]):
                        n = a[1] + b[1] + c[1]
                        dev = abs(a[0] + b[0] + c[0]) + abs(a[2] + b[2] + c[2] - n * prate)
                        if best is None or dev < best[0] - 1e-12:
                            best = (dev, (ia, ib, ic))
            ia, ib, ic = best[1]
            self.backchecks.extend(cands[0][ia][1] + cands[1][ib][1] + cands[2][ic][1])

    # replacement reviews ---------------------------------------------------------------------
    def _reviews(self):
        """the commodity team's decisions on the variety replacements collectors made from June on; the
        stream is the first whose regional acceptance shares all sit clear of a rounding edge"""
        for k in range(50):
            self._draw_reviews(k)
            if self._acceptance_clear():
                self.review_stream = k
                return
        raise RuntimeError("no review stream leaves every acceptance share clear of a rounding edge")

    def _acceptance_clear(self):
        latest = {}
        for rv in sorted(self.reviews, key=lambda x: x["date"]):
            if rv["decision"] != "Query to contractor":
                latest[(rv["qid"], rv["y"], rv["m"])] = rv["decision"]
        tot, acc = {}, {}
        for r in self.records:
            if r["status"] == "R" and (r["y"], r["m"]) in P.QUARTER:
                reg = self.quotes[r["qid"]]["region"]
                tot[reg] = tot.get(reg, 0) + 1
                acc[reg] = acc.get(reg, 0) + (latest.get((r["qid"], r["y"], r["m"])) == "Comparable")
        for reg, n in tot.items():
            v = 100.0 * acc[reg] / n
            if abs(abs(v - round(v, 1)) - 0.05) < 0.002 or abs(v * 20 - round(v * 20)) < 1e-9 and round(v * 20) % 2 == 1 and abs(v * 10 - round(v * 10)) > 1e-9:
                return False
        return True

    def _draw_reviews(self, k):
        rng = stream(8, k)
        self.reviews = []
        reps = [r for r in self.records if r["status"] == "R" and (r["y"], r["m"]) >= (2026, 6)]
        for r in sorted(reps, key=lambda x: (x["vday"], x["qid"])):
            u = rng.random(7)
            first = add_workdays(r["vday"], 2 + int(u[0] * 9))
            final_date = first
            fk = (r["qid"], r["y"], r["m"])
            if fk in self.forced:
                if first <= P.EXTRACT_DATE:
                    self.reviews.append(dict(qid=r["qid"], y=r["y"], m=r["m"], decision=self.forced[fk], date=first, final=True))
                continue
            if u[1] < P.REVIEW_QUERY:
                self.reviews.append(dict(qid=r["qid"], y=r["y"], m=r["m"], decision="Query to contractor", date=first, final=False))
                final_date = add_workdays(first, 3 + int(u[2] * 8))
            dec = "Comparable" if u[3] < P.REVIEW_COMPARABLE else "Not comparable"
            if final_date > P.EXTRACT_DATE:
                continue
            self.reviews.append(dict(qid=r["qid"], y=r["y"], m=r["m"], decision=dec, date=final_date, final=True))
            if u[4] < P.REVIEW_RECHECK:
                chk = add_workdays(final_date, 2 + int(u[5] * 6))
                if chk <= P.EXTRACT_DATE:
                    dec2 = dec if u[6] < 0.6 else ("Not comparable" if dec == "Comparable" else "Comparable")
                    self.reviews[-1]["final"] = False
                    self.reviews.append(dict(qid=r["qid"], y=r["y"], m=r["m"], decision=dec2, date=chk, final=True))


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
    print(len(w.outlets), "outlets", len(w.quotes), "quotes", len(w.records), "records",
          len(w.backchecks), "back-checks", len(w.reviews), "reviews")
