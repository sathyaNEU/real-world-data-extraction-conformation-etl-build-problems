"""The docket's estimate and every rival, computed from the conformed bundle.

A faculty member's estimate for a year is the largest, over the manufacturers named in that year's disclosure, of
the amount disclosed divided by a correction factor c (and, for a disclosure submitted before the year was out, by
the share of the year's payments made by its submission). The family of corrections:
    grain     "line": the faculty member's amount-reporting ratio on the manufacturer-years both sources carry
              "all":  the share of the register's remuneration in the years they disclosed that they disclosed
              "pair": the ratio on the same manufacturer's earlier lines, falling back to "line" or "all"
    handling  "face" (c = 1), "pool" (the faculty-wide ratio), "own" (the person's ratio), "n"/"usd"/"yrs"
              (credibility weighting toward the faculty-wide ratio by matched lines, dollars or years with K),
              "thr" (own ratio from K lines, else the pool), "cap" (the ratio floored at K)
    form      "sum" (dollar-weighted), "mean", "geo", "med"
    align     "none": every disclosure read as covering the whole year
              "hist": the register's side of each earlier matched line counted to the day the disclosure in force was
                      submitted (a December submission cannot carry the payments made after it)
              "target": the year estimated grossed up for a December submission by the share of the year's payments
                      made by that day
              "both": both
    cover     how that share is taken: "pair" (the same manufacturer's payments to the faculty member the year before,
              else the faculty-wide share), "fw" (the faculty-wide share of a year's remuneration paid by that day),
              "add" (adding the same manufacturer's payments after that day the year before)
The filed criterion compares each correction's 2025 estimates (from 2025's disclosures and the years before) with
the register's largest 2025 single-manufacturer remuneration of each faculty member estimated, by the total of the
absolute differences."""
import math
import statistics
from collections import defaultdict

import conform as C

GRIDS = {"n": [0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 20], "usd": [2e3, 5e3, 1e4, 2e4, 4e4, 8e4],
         "yrs": [0.5, 1, 2, 3, 5], "thr": [2, 3, 4, 5, 6], "cap": [0.4, 0.5, 0.6]}
HANDLINGS = ["face", "pool", "own", "n", "usd", "yrs", "thr", "cap"]
FORMS = ["sum", "mean", "geo", "med"]
ALIGNS = ["none", "hist", "target", "both"]
COVERS = ["pair", "fw", "add"]


class Conformed:
    """Published and disclosed remuneration under one set of readings."""

    def __init__(self, data, **kw):
        pub_kw = {k: kw[k] for k in ("attribution", "personal", "natures", "vintage") if k in kw}
        dis_kw = {k: kw[k] for k in ("version", "typed", "listed") if k in kw}
        self.pub = C.published(data, **pub_kw)
        self.dis = C.disclosed(data, **dis_kw)
        self.fac = C.faculty(data)
        self.pay = C.payments(data, **{k: kw[k] for k in ("attribution", "personal", "natures") if k in kw})
        self.day = C.in_force_day(data, "first" if kw.get("version") == "first" else "latest")
        self.kw = kw
        self.filed = {(d["emp_id"], int(d["disclosure_year"])) for d in data["disc"]}
        self._mcache, self._ocache = {}, {}
        self.by_person_year = defaultdict(dict)
        for (e, m, y), d in self.dis.items():
            self.by_person_year[(e, y)][m] = d
        self.pub_by_person_year = defaultdict(dict)
        for (e, m, y), a in self.pub.items():
            self.pub_by_person_year[(e, y)][m] = a
        self._fw = {}

    def to_day(self, e, m, y):
        """The register's remuneration from m to e in year y made by the day the disclosure in force was submitted."""
        day = self.day.get((e, y))
        full = self.pub_by_person_year.get((e, y), {}).get(m, 0.0)
        if day is None or day.year > y:
            return full
        return sum(a for d, a in self.pay.get((e, m, y), []) if d <= day)

    def matched(self, e, before, aligned=False):
        """[(published, disclosed, manufacturer, year)] on the manufacturer-years both sources carry."""
        key = (e, before, aligned)
        if key in self._mcache:
            return self._mcache[key]
        out = []
        for y in range(2021, before):
            for m, d in self.by_person_year.get((e, y), {}).items():
                a = self.pub_by_person_year.get((e, y), {}).get(m)
                if a and d:
                    if aligned:
                        a = self.to_day(e, m, y)
                        if a <= 0:
                            continue
                    out.append((a, d, m, y))
        self._mcache[key] = out
        return out

    def overall(self, e, before, aligned=False):
        """Published and disclosed totals over the years the faculty member disclosed for."""
        key = (e, before, aligned)
        if key in self._ocache:
            return self._ocache[key]
        a_sum = d_sum = 0.0
        years = set()
        for y in range(2021, before):
            if (e, y) not in self.filed:
                continue
            years.add(y)
            if aligned:
                a_sum += sum(self.to_day(e, m, y) for m in self.pub_by_person_year.get((e, y), {}))
            else:
                a_sum += sum(self.pub_by_person_year.get((e, y), {}).values())
            d_sum += sum(self.by_person_year.get((e, y), {}).values())
        self._ocache[key] = (a_sum, d_sum, years)
        return a_sum, d_sum, years

    def fw_share(self, year, day):
        """The faculty-wide share of a year's remuneration the register shows paid by the day's month and day, in the
        year before `year`."""
        key = (year, day.month, day.day)
        if key not in self._fw:
            got = tot = 0.0
            for (e, m, y), pays in self.pay.items():
                if y != year - 1:
                    continue
                for d, a in pays:
                    tot += a
                    if (d.month, d.day) <= (day.month, day.day):
                        got += a
            self._fw[key] = got / tot if tot else 1.0
        return self._fw[key]

    def coverage(self, e, m, year, cover):
        """The share of the year's payments from m that a disclosure submitted on its day could carry."""
        day = self.day.get((e, year))
        if day is None or day.year > year:
            return 1.0
        if cover == "pair":
            prev = self.pay.get((e, m, year - 1), [])
            tot = sum(a for _, a in prev)
            got = sum(a for d, a in prev if (d.month, d.day) <= (day.month, day.day))
            if tot > 0 and got > 0:
                return got / tot
        return self.fw_share(year, day)

    def tail(self, e, m, year):
        """The same manufacturer's payments to the faculty member after the submission's month and day, the year
        before."""
        day = self.day.get((e, year))
        if day is None or day.year > year:
            return 0.0
        return sum(a for d, a in self.pay.get((e, m, year - 1), []) if (d.month, d.day) > (day.month, day.day))


def _agg(pairs, form):
    if not pairs:
        return None
    if form == "sum":
        den = sum(a for a, d, *_ in pairs)
        return sum(d for a, d, *_ in pairs) / den if den else None
    rs = [d / a for a, d, *_ in pairs]
    if form == "mean":
        return sum(rs) / len(rs)
    if form == "geo":
        return math.exp(sum(math.log(x) for x in rs) / len(rs))
    return statistics.median(rs)


def pools(cf, year, form, aligned=False):
    key = ("pools", year, form, aligned)
    if key not in cf._ocache:
        all_m = [p for e in cf.fac for p in cf.matched(e, year, aligned)]
        a_tot = d_tot = 0.0
        for e in cf.fac:
            a, d, _ = cf.overall(e, year, aligned)
            a_tot += a
            d_tot += d
        cf._ocache[key] = (_agg(all_m, form), d_tot / a_tot)
    return cf._ocache[key]


def line_values(cf, year, grain, handling, K=0.0, form="sum", fallback="line", filed=None, align="none", cover="pair",
                pool_form=None):
    """{emp_id: {manufacturer: corrected value}} for the faculty with remuneration disclosed for `year` (pool_form: the
    faculty-wide ratio formed another way than the person's)."""
    persons = sorted({e for (e, y) in cf.by_person_year if y == year})
    if filed is not None:
        persons = [e for e in persons if e in filed]
    ah = align in ("hist", "both")
    at = align in ("target", "both")
    pool_line, pool_all = pools(cf, year, pool_form or form, ah)

    def handle(c, n, usd, yrs, pool):
        if handling == "face":
            return 1.0
        if handling == "pool":
            return pool
        if c is None or c <= 0.02:
            return pool
        if handling == "own":
            return c
        if handling == "thr":
            return c if n >= K else pool
        if handling == "cap":
            return max(c, K)
        v = {"n": n, "usd": usd, "yrs": yrs}[handling]
        z = v / (v + K)
        return z * c + (1 - z) * pool

    def person_c(e, g):
        if g == "line":
            m = cf.matched(e, year, ah)
            return handle(_agg(m, form), len(m), sum(a for a, *_ in m), len({y for *_, y in m}), pool_line)
        a, d, yrs = cf.overall(e, year, ah)
        c = d / a if a else None
        return handle(c, len(cf.matched(e, year, ah)), a, len(yrs), pool_all)

    out = {}
    for e in persons:
        vals = {}
        cache = {}
        for m, dval in cf.by_person_year[(e, year)].items():
            if grain == "pair":
                pm = [p for p in cf.matched(e, year, ah) if p[2] == m]
                if pm:
                    c = handle(_agg(pm, form), len(pm), sum(a for a, *_ in pm), len(pm), pool_line)
                else:
                    c = cache.setdefault(fallback, person_c(e, fallback))
            else:
                c = cache.setdefault(grain, person_c(e, grain))
            v = dval / c
            if at:
                v = v + cf.tail(e, m, year) if cover == "add" else v / cf.coverage(e, m, year, cover)
            vals[m] = v
        out[e] = vals
    return out


def _best(vals):
    best = (0.0, None)
    for m in sorted(vals, key=str):
        if vals[m] > best[0]:
            best = (vals[m], m)
    return best


def estimates(cf, year, grain, handling, K=0.0, form="sum", fallback="line", filed=None, align="none", cover="pair",
              pool_form=None):
    """{emp_id: (estimate, manufacturer of the estimate)}: each faculty member's largest corrected line."""
    lv = line_values(cf, year, grain, handling, K, form, fallback, filed, align, cover, pool_form)
    return {e: _best(v) for e, v in lv.items()}


def hybrid_estimates(cf, year, mode, grain, handling, K=0.0, form="sum", align="none", cover="pair"):
    """Estimates that lean on the register too: for a manufacturer the register already shows paying the faculty member
    the year before, last year's published amount ("last"), its average with the corrected line ("avg") or the larger
    of the two ("max"); for a new manufacturer, the corrected line. The correction is the family's grain, handling and
    alignment."""
    lv = line_values(cf, year, grain, handling, K, form, align=align, cover=cover)
    out = {}
    for e, vals in lv.items():
        h = {}
        for m, corr in vals.items():
            last = cf.pub_by_person_year.get((e, year - 1), {}).get(m)
            if last and mode == "last":
                h[m] = last
            elif last and mode == "avg":
                h[m] = 0.5 * (last + corr)
            elif last and mode == "max":
                h[m] = max(last, corr)
            else:
                h[m] = corr
        out[e] = _best(h)
    return out


def truth(cf, year, persons):
    """The register's largest single-manufacturer remuneration of each faculty member in the year."""
    return {e: max(cf.pub_by_person_year.get((e, year), {}).values() or [0.0]) for e in persons}


def backtest(cf, grain, handling, K=0.0, form="sum", fallback="line", align="none", cover="pair", pool_form=None):
    est = estimates(cf, 2025, grain, handling, K, form, fallback, align=align, cover=cover, pool_form=pool_form)
    tr = truth(cf, 2025, est)
    return sum(abs(est[e][0] - tr[e]) for e in est)


def docket(cf, grain, handling, K=0.0, form="sum", fallback="line", filed=None, n=15, align="none", cover="pair",
           pool_form=None):
    est = estimates(cf, 2026, grain, handling, K, form, fallback, filed=filed, align=align, cover=cover, pool_form=pool_form)
    ranked = sorted(est.items(), key=lambda kv: (-kv[1][0], kv[0]))
    return [e for e, _ in ranked[:n]], ranked


def _row(cf, grain, handling, K, form, fb, align, cover, filed=None):
    bt = backtest(cf, grain, handling, K, form, fb, align, cover)
    dk, ranked = docket(cf, grain, handling, K, form, fb, filed=filed, align=align, cover=cover)
    return (bt, grain, handling, K, form, fb, tuple(sorted(dk)), ranked[14][1][0] / ranked[15][1][0], align, cover)


def family(cf, filed=None, aligns=("none",), covers=("pair",)):
    """Every correction in the family at every weighting: rows of (total 2025 difference, grain, handling, K, form,
    fallback, docket tuple, fifteenth over sixteenth, align, cover)."""
    rows = []
    for align in aligns:
        for cover in (covers if align in ("target", "both") else ("pair",)):
            for grain, fallbacks in (("line", ["line"]), ("all", ["all"]), ("pair", ["line", "all"])):
                for fb in fallbacks:
                    for handling in HANDLINGS:
                        forms = ["sum"] if handling in ("face", "pool") or grain == "all" else FORMS
                        if handling == "face" and (grain != "line"):
                            continue
                        for form in forms:
                            for K in GRIDS.get(handling, [0.0]):
                                rows.append(_row(cf, grain, handling, K, form, fb, align, cover, filed))
    return rows


def hybrid_rows(cf, aligns=("none", "both"), covers=("pair",)):
    """The hybrid constructions over the main grains and handlings, each at every weighting."""
    rows = []
    for align in aligns:
        for cover in (covers if align in ("target", "both") else ("pair",)):
            for mode in ("last", "avg", "max"):
                for grain, handling, Ks, form in (("line", "face", [0.0], "sum"), ("line", "n", GRIDS["n"], "sum"),
                                                  ("line", "usd", GRIDS["usd"], "sum"), ("line", "thr", GRIDS["thr"], "sum"),
                                                  ("line", "own", [0.0], "sum"), ("all", "own", [0.0], "sum"),
                                                  ("all", "usd", GRIDS["usd"], "sum"), ("all", "n", GRIDS["n"], "sum")):
                    for K in Ks:
                        e25 = hybrid_estimates(cf, 2025, mode, grain, handling, K, form, align, cover)
                        tr = truth(cf, 2025, e25)
                        bt = sum(abs(e25[e][0] - tr[e]) for e in e25)
                        e26 = hybrid_estimates(cf, 2026, mode, grain, handling, K, form, align, cover)
                        ranked = sorted(e26.items(), key=lambda kv: (-kv[1][0], kv[0]))
                        rows.append((bt, "hyb-%s/%s" % (mode, grain), handling, K, form, grain,
                                     tuple(sorted(e for e, _ in ranked[:15])), ranked[14][1][0] / ranked[15][1][0],
                                     align, cover))
    return rows


GOLDEN = ("line", "n", "both", "pair")    # aligned matched-line ratio, credibility-weighted by matched lines


def golden(cf, filed=None):
    """The golden correction: the matched-line ratio (dollar-weighted), each earlier line's register side counted to the
    day its disclosure was submitted, credibility-weighted by the number of matched lines (K the grid value whose 2025
    total difference is smallest); a December submission grossed up by the share the same manufacturer had paid by that
    day the year before (else the faculty-wide share)."""
    best = min((backtest(cf, "line", "n", K, "sum", align="both", cover="pair"), K) for K in GRIDS["n"])
    dk, ranked = docket(cf, "line", "n", best[1], "sum", filed=filed, align="both", cover="pair")
    return {"K": best[1], "bt": best[0], "docket": dk, "ranked": ranked}
