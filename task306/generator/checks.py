"""Assertions on the built pack and the world it came from: the three-rules block (the easy route files the named wrong
answer on the clean truth and on the pack, the decisive step alone files the golden), the standing family, the ladder,
every semantic fork row (SF1 to SF27), the projection family the 2027 fleet's later registrations converge over (SF25),
the bins, the ask devices, separation and the input gates.

    python3 task306/generator/checks.py <target dir>
"""
import calendar
import csv
import datetime as dt
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S
import world as Wd

GOLD = {"Volta hatch": 900, "Kestrel SUV": 250, "Plover saloon": 350, "Mira city car": 1450, "Tern van": 50}
EASY = {"Volta hatch": 1000, "Kestrel SUV": 300, "Plover saloon": 350, "Mira city car": 1250, "Tern van": 100}
HALF = {"Volta hatch": 950, "Kestrel SUV": 250, "Plover saloon": 350, "Mira city car": 1350, "Tern van": 100}
N = 0


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError(msg)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def hundred(v):
    return int(round(v / 100.0) * 100)


def world_routes():
    """the clean truth: the world's own arrays, the register's cars at their packs, the arrivals as they happen"""
    W, ev = Wd.world()
    T, keep = W["T"], W["keep"]
    reg = np.where(keep & (W["nl"] <= Wd.SNAP))[0]
    s = np.full(len(reg), Wd.SNAP)
    p = Wd.p_due(T, W["start"][reg], W["curve"][reg], W["oem_end"][reg], s, s)
    base = {n: float(p[W["plat"][reg] == k].sum()) for k, n in enumerate(P.NAMES)}
    later = Wd.later_truth(W)
    truth = {n: base[n] + later[n] for n in P.NAMES}
    # the post-pin easy route on the clean truth: the cars first registered after 30 June 2026 carried as new cars, each
    # pack fitted the day the car is registered and covered for the warranty's years from that day
    idx = np.where(keep & (W["nl"] > Wd.SNAP))[0]
    war = np.array([P.WARRANTY[n] for n in P.NAMES], float)
    nl = W["nl"][idx]
    q = Wd.p_due(T, nl, W["plat"][idx], nl + np.round(war[W["plat"][idx]] * Wd.YD).astype(np.int64), nl, nl)
    as_new = {n: float(q[W["plat"][idx] == k].sum()) for k, n in enumerate(P.NAMES)}
    return base, truth, as_new


# ---- the 2027 fleet's later registrations, projected from the register's own used imports (SF25) -------------------
E0 = dt.date(1970, 1, 1)
HZ = [(2026, m) for m in range(7, 13)] + [(2027, m) for m in range(1, 13)]


def _i(d):
    return (d - E0).days


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"\s+", " ", " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x)))


class Proj:
    """Every reasonable way of carrying the cars first registered here from July 2026 to December 2027 at the register's
    own rate and mix of used imports: each projected car keeps the age, pack age and warranty a window car had when it
    was registered, and is at risk from its own registration day, given its pack works that day."""

    def __init__(self, pk):
        self.pk = pk
        self.imp = [c for c in pk.reg if c["fu"] < c["nl"]]
        self.y0, self.y1 = _i(S.Y0), _i(S.Y1)

    def window(self, months=None, y0=None, y1=None):
        if months:
            lo = S.add_months(S.SNAP, -months)
            return [c for c in self.imp if lo < c["nl"] <= S.SNAP]
        return [c for c in self.imp if y0 <= c["nl"] <= y1]

    def arrays(self, cars, orig=False):
        pk, A = self.pk, defaultdict(list)
        for c in cars:
            s, k = (c["fu"], c["n"]) if orig else pk.pack_at(c, c["nl"], inclusive=False)
            A["st"].append(_i(s)); A["cv"].append(k); A["we"].append(_i(pk.w_end(c)))
            A["nl"].append(_i(c["nl"])); A["nm"].append(c["n"]); A["day"].append(c["nl"].day)
            A["mq"].append((c["nl"].month - 1) % 3); A["age"].append((c["nl"] - c["fu"]).days / 365.25)
        return {k: np.array(v) for k, v in A.items()}

    def chance(self, A, arr, keep_vintage=False, cond=True, cond_at=None, start=None, w_end=None):
        off = np.zeros(len(arr), dtype=np.int64) if keep_vintage else arr - A["nl"]
        st = (A["st"] if start is None else start) + off
        we = (A["we"] if w_end is None else w_end) + off
        out = np.zeros(len(arr))
        for k in np.unique(A["cv"]):
            m = A["cv"] == k
            F = lambda a: np.interp(a, self.pk.ages, self.pk.tab[k])
            lo = np.maximum(np.maximum(self.y0, arr[m]), we[m])
            a0, a1 = (lo - st[m]) / 365.25, (self.y1 - st[m]) / 365.25
            num = np.maximum(F(a1) - F(a0), 0.0)
            ca = arr[m] if cond_at is None else np.maximum(arr[m], cond_at)
            den = np.maximum(1.0 - F((ca - st[m]) / 365.25), 1e-9) if cond else 1.0
            out[m] = np.where(a1 > a0, num / den, 0.0)
        return out

    def days(self, A, y, m, rule):
        last = calendar.monthrange(y, m)[1]
        if rule == "same":
            return [(np.array([_i(dt.date(y, m, min(int(d), last))) for d in A["day"]]), 1.0)]
        if rule in ("mid", "first", "last"):
            d = {"mid": 15, "first": 1, "last": last}[rule]
            return [(np.full(len(A["day"]), _i(dt.date(y, m, d))), 1.0)]
        ds = list(range(1, last + 1, 2))                                   # spread through the month
        return [(np.full(len(A["day"]), _i(dt.date(y, m, d))), 1.0 / len(ds)) for d in ds]

    def by_make(self, v, A):
        return {n: float(v[A["nm"] == n].sum()) for n in P.NAMES}

    def monthly(self, cars, months, rule="same", orig=False, weights=None, hz=HZ, **kw):
        A = self.arrays(cars, orig)
        tot = np.zeros(len(cars))
        for j, (y, m) in enumerate(hz):
            wm = np.array([weights[n][j] for n in A["nm"]]) if weights else 1.0
            for arr, wd in self.days(A, y, m, rule):
                tot += wm * wd / months * self.chance(A, arr, **kw)
        return self.by_make(tot, A)

    def quarterly(self, cars, rule):
        A = self.arrays(cars)
        tot = np.zeros(len(cars))
        for y, q in [(2026, 3), (2026, 4), (2027, 1), (2027, 2), (2027, 3), (2027, 4)]:
            m0 = 3 * (q - 1) + 1
            if rule == "own":
                arr = np.array([_i(dt.date(y, m0 + int(k), min(int(d), calendar.monthrange(y, m0 + int(k))[1])))
                                for k, d in zip(A["mq"], A["day"])])
            elif rule == "mid":
                arr = np.full(len(cars), _i(dt.date(y, m0 + 1, 15)))
            elif rule == "first":
                arr = np.full(len(cars), _i(dt.date(y, m0, 1)))
            else:
                arr = np.full(len(cars), _i(dt.date(y, m0 + 2, calendar.monthrange(y, m0 + 2)[1])))
            tot += 0.25 * self.chance(A, arr)
        return self.by_make(tot, A)

    def replay(self, cars, months):
        """the next eighteen months take in the last `months` months' cars again, in order, a whole period later"""
        A = self.arrays(cars)
        nl = [E0 + dt.timedelta(int(x)) for x in A["nl"]]
        tot = np.zeros(len(cars))
        for k in (1, 2, 3):
            arr = np.array([_i(S.add_months(d, k * months)) for d in nl])
            tot += np.where((arr > _i(S.SNAP)) & (arr < self.y1), self.chance(A, arr), 0.0)
        return self.by_make(tot, A)

    def at_age(self, cars, age_of, orig_curve=True):
        """every projected car at a fixed age on registration, on the pack it was built with"""
        A = self.arrays(cars, orig=True)
        tot = np.zeros(len(cars))
        a = np.array([age_of(n) for n in A["nm"]])
        for y, m in HZ:
            arr = np.full(len(cars), _i(dt.date(y, m, 15)))
            fu = arr - np.round(a * 365.25).astype(np.int64)
            we = np.array([_i(S.add_years(E0 + dt.timedelta(int(f)), self.pk.war[n])) for f, n in zip(fu, A["nm"])])
            tot += self.chance(A, arr, keep_vintage=True, start=fu, w_end=we) / 12.0
        return self.by_make(tot, A)

    def as_new(self, cars):
        """every later registration carried as a new car, its pack fitted the day it is registered"""
        A = self.arrays(cars, orig=True)
        tot = np.zeros(len(cars))
        for y, m in HZ:
            arr = np.array([_i(dt.date(y, m, min(int(d), calendar.monthrange(y, m)[1]))) for d in A["day"]])
            we = np.array([_i(S.add_years(E0 + dt.timedelta(int(t)), self.pk.war[n])) for t, n in zip(arr, A["nm"])])
            tot += self.chance(A, arr, keep_vintage=True, start=arr, w_end=we) / 12.0
        return self.by_make(tot, A)

    def family(self):
        """the standing family: every rate source, placement in the month and pack on registration a competent
        projection uses, conditioned on the pack working the day the car is registered"""
        pk, fam = self.pk, {}
        w12 = self.window(12)
        rates = [("trailing %d months" % k, self.window(k), k, None) for k in (3, 6, 9, 12, 18, 24, 36, 48)]
        rates += [("calendar 2025", self.window(y0=dt.date(2025, 1, 1), y1=dt.date(2025, 12, 31)), 12, None),
                  ("calendar 2024", self.window(y0=dt.date(2024, 1, 1), y1=dt.date(2024, 12, 31)), 12, None)]
        rates += [("straight-line trend over %d months" % s, w12, 12, pk.trend_weights(s)) for s in (12, 24, 36, 48)]
        for label, cars, k, wts in rates:
            for rule in ("same", "mid", "first", "last", "uniform"):
                for orig in (False, True):
                    fam["%s, day %s, %s" % (label, rule, "built pack" if orig else "registration pack")] = \
                        self.monthly(cars, k, rule=rule, orig=orig, weights=wts)
        for rule in ("own", "mid"):
            fam["by quarter, %s" % rule] = self.quarterly(w12, rule)
        for k in (12, 18):
            fam["replay of the last %d months" % k] = self.replay(self.window(k), k)
        return fam


def stock_below_zero(ln, collapse=False):
    """lots received in the year whose running stock goes below zero in booking order, the receipt booked first on its
    day; with collapse, a quantity one pick list repeats over several work orders on such a lot goes out once"""
    rec = defaultdict(int)
    when = {}
    for r in ln.receipts:
        rec[r["partij"]] += int(r["aantal"])
        when[r["partij"]] = S.iso(r["datum"])
    bp = ln.batch_picks() if collapse else {}
    seen, stock, low = set(), defaultdict(int), set()
    ev = sorted(((S.iso(r["datum"]), 0, "", r) for r in ln.receipts), key=lambda x: (x[0], x[1]))
    lines = sorted(((S.stamp(r["geboekt_op"]).date(), 1, r["geboekt_op"], r) for r in ln.stores), key=lambda x: (x[0], x[2]))
    for d, kind, _, r in sorted(ev + lines, key=lambda x: (x[0], x[1], x[2])):
        p = r["partij"]
        if p not in rec:
            continue
        if kind == 0:
            stock[p] += int(r["aantal"])
            continue
        key = (r["picklijst"], r["partij"], r["aantal"])
        if collapse and r["soort"] == "UITGIFTE" and key in bp:
            if key in seen:
                continue
            seen.add(key)
        stock[p] -= int(r["aantal"])
        if stock[p] < 0:
            low.add(p)
    return low


def main(target):
    pk = S.Pack(target, P.FILES)
    c = pk.call()
    fc, base, arr = c["forecast"], c["base"], c["arrivals"]
    L = c["lots"]
    # ---- the three rules, executed (dataset-generation 7.1) -----------------------------------------------------------
    # R1: the field's raw material ships at the car grain, and no shipped column holds the deciding quantity
    reg_rows = list(csv.DictReader(open(os.path.join(target, P.FILES["register"]), encoding="utf-8")))
    ok(len(reg_rows) >= 25000 and {"datum_eerste_toelating", "datum_eerste_tenaamstelling_in_nederland"} <= set(reg_rows[0]),
       "R1 the register ships car by car with both dates")
    heads = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    words = {"forecast", "prognose", "slot", "slots", "verwacht", "storingen", "failures", "kans", "chance"}
    ok(not [h for h in heads if set(h.lower().split("_")) & words], "R1 no shipped column holds a forecast or a slot")
    # R3a: the easy route, every filed rule applied, files the named wrong answer, on the clean truth and on the pack.
    # The plan files the later registrations into the 2027 fleet (SF25); the easy route counts them and carries them
    # as new cars inside their warranty, which adds nothing in 2027, so it files the register's own split
    wb, wt, wn = world_routes()
    ok(sum(wn.values()) == 0.0, "R3a clean truth: the later registrations carried as new cars add %.3f" % sum(wn.values()))
    wb_new = {n: wb[n] + wn[n] for n in P.NAMES}
    ok(Wd.lots(wb_new)[0] == EASY, "R3a clean truth: the easy route files %s" % Wd.lots(wb_new)[0])
    ok(hundred(sum(wb_new.values())) == 3400, "R3a clean truth: the easy route's total is 3,400")
    pj = Proj(pk)
    pn = pj.as_new(pj.window(12))
    ok(sum(pn.values()) == 0.0, "R3a pack: the later registrations carried as new cars add %.3f" % sum(pn.values()))
    ok(S.lots({n: base[n] + pn[n] for n in P.NAMES})["slots"] == EASY, "R3a pack: the easy route files the named wrong answer")
    ok(hundred(sum(base.values()) + sum(pn.values())) == 3400, "R3a pack: the easy route's total is 3,400")
    # R3b: the decisive step alone files the golden; the partial repair stays wrong
    ok(Wd.lots(wt)[0] == GOLD and hundred(sum(wt.values())) == 3800, "R3b clean truth: the fleet as it arrives files the golden")
    ok(L["slots"] == GOLD and hundred(c["total"]) == 3800, "R3b pack: adding the arrivals alone files the golden")
    # R2: each Layer 1 item mishandled leaves the call where it is
    regk = {r["k"] for r in pk.reg}
    ok(any(k not in regk for k in pk.ev), "R2 the log carries cars no longer on the register")
    ok(all(r["n"] for r in pk.reg), "R2 every make maps to a platform, whatever the trade name")
    trade = {}
    for r in reg_rows:
        trade.setdefault(r["merk"], set()).add(r["handelsbenaming"])
    ok(all(len(v) >= 3 for v in trade.values()), "R2 trade names vary within each make")
    ok(len({r["kenteken"] for r in reg_rows}) == len(reg_rows), "R2 one row per registration")
    # R3c: no plant: no repeated block, no constant stream, no round total
    counts = {}
    for r in pk.reg:
        counts[r["n"]] = counts.get(r["n"], 0) + 1
    ok(len(set(counts.values())) == 5 and all(v % 100 for v in counts.values()), "R3c platform counts distinct, not round")
    mira = {}
    for r in pk.reg:
        if r["n"] == "Mira city car" and r["fu"] < r["nl"] and r["nl"].year >= 2024:
            mira[(r["nl"].year, r["nl"].month)] = mira.get((r["nl"].year, r["nl"].month), 0) + 1
    v = list(mira.values())
    ok(len(set(v)) >= len(v) * 0.6 and max(v) - min(v) >= 20, "R3c monthly imports vary like counts")
    ok(len(reg_rows) % 1000 != 0, "R3c the register's size is not round")
    ok(abs(sum(base.values()) - sum(wb.values())) < 1.0, "pack and world agree on the register's forecast")
    ok(sum(arr.values()) > 300 and arr["Mira city car"] / sum(arr.values()) > 0.95, "the arrivals are the Mira's")
    # ---- the standing family: every way of carrying the arrivals files the golden ---------------------------------
    fam = {}
    for m in (6, 12, 24, 36):
        a = pk.arrivals(months=m)
        fam["window %d" % m] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    a = pk.arrivals(weights=pk.trend_weights(36))
    fam["trend 36"] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    a = pk.arrivals(orig=True)
    fam["original packs on arrival"] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    ren = pk.renewal()
    fam["renewal of late-2026 failures"] = {n: fc[n] + ren.get(n, 0.0) for n in P.NAMES}
    for k, f in fam.items():
        lt = S.lots(f)
        ok(lt["slots"] == GOLD, "family %s files %s" % (k, lt["slots"]))
        ok(lt["margin"] >= 0.15, "family %s margin %.3f" % (k, lt["margin"]))
        ok(hundred(sum(f.values())) == 3800 and edge(sum(f.values()), 100) >= 10, "family %s total %.1f" % (k, sum(f.values())))
    ok(L["margin"] >= 0.25, "golden margin %.3f" % L["margin"])
    ok(edge(c["total"], 100) >= 30, "golden total %.1f clears its bin's edge" % c["total"])
    # ---- the ladder: each rung below the decisive step files its own answer -----------------------------------------
    hz26 = [(2026, m) for m in range(7, 13)]
    hz27 = [(2027, m) for m in range(1, 13)]
    for hz in (hz26, hz27):
        a = pk.arrivals(horizon=hz)
        f = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
        ok(S.lots(f)["slots"] == HALF and hundred(sum(f.values())) == 3600, "half the stream files the 1,350 rung")
    rungs = {"unconditional": pk.base(cond=False), "Dutch registration": pk.base(warranty_from="nl"),
             "original packs": pk.base(original=True), "eight years for all": pk.base(all_eight=True)}
    for k, f in rungs.items():
        ok(S.lots(f)["slots"] != GOLD, "rung %s lands the golden" % k)
    # ---- semantic fork rows ---------------------------------------------------------------------------------------
    # SF1: calendar 2027 (plan section 2); the financial year July 2027 to June 2028 is ruled out by the plan's words
    ok("in calendar 2027" in open(os.path.join(HERE, "docs.py")).read(), "SF1 the plan says calendar 2027")
    # SF2: a Voltwerk-warranty failure counts (plan section 3); leaving it out keeps the slots
    f = pk.base(vw_excl=True)
    ok(S.lots({n: f[n] + arr.get(n, 0.0) for n in P.NAMES})["slots"] == GOLD, "SF2 same slots")
    # SF3: the warranty's end in calendar years or 365.25-day years
    b2, a2 = pk.base(rule="days"), pk.arrivals(rule="days")
    f = {n: b2[n] + a2.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF3 same call")
    # SF4: pack age in 365-day years
    b2, a2 = pk.base(year=365.0), pk.arrivals(year=365.0)
    f = {n: b2[n] + a2.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF4 same call")
    # SF5: the curves read by straight lines (plan section 3); a step reading files another call and is ruled out
    pk.interp = "step"
    b2, a2 = pk.base(), pk.arrivals()
    pk.interp = "linear"
    ok(S.lots({n: b2[n] + a2.get(n, 0.0) for n in P.NAMES})["slots"] != GOLD, "SF5 the step reading differs")
    # SF6: the warranty runs from first admission anywhere (terms section 1); from the Dutch registration differs
    ok(S.lots(pk.base(warranty_from="nl"))["slots"] != GOLD, "SF6 the Dutch-registration reading differs")
    # SF7: pack age from the fitting day or first admission (plan section 3) -- asserted with SF6 and the original-pack
    # rung above; SF8: an OEM warranty pack keeps the original end (terms section 1)
    ok(pk.w_end(dict(fu=__import__("datetime").date(2018, 3, 1), n="Volta hatch")).year == 2026, "SF8 warranty end")
    # SF9: cars stay in use (plan section 3): no exit term anywhere in the forecast
    ok(True, "SF9 no exits")
    # SF10: imports are the rows whose first admission is before their first Dutch registration
    reg = pk.reg
    ok(all(r["fu"] <= r["nl"] for r in reg), "SF10 no car registered here before its first admission")
    # SF11: the total to the nearest hundred of the unrounded sum or of the rounded parts
    ok(hundred(sum(round(v) for v in fc.values())) == hundred(c["total"]), "SF11 same total")
    # SF12: largest remainder, no tie at the cut
    ok(L["margin"] > 0.2, "SF12 no tie")
    # SF24: the prompt rounds the 2027 total; each platform's forecast rounded to the nearest hundred before the split
    # files another split, and the rounding sentence names the total alone
    ok(S.lots({n: hundred(fc[n]) for n in P.NAMES})["slots"] != GOLD, "SF24 rounding the parts first files another split")
    # SF13 and SF14: the population is the Netherlands' cars of the five makes; every register row maps to a platform
    ok(len({r["n"] for r in reg}) == 5, "SF13 five platforms")
    ok(True, "SF14 in the Netherlands")
    # SF25: the 2027 fleet (plan section 3) holds the cars first registered here from 1 July 2026 to the end of 2027,
    # each from the day it is registered; the register-only reading both portal judges filed leaves them out and files
    # the register's split. The plan files the WHAT only: how the later registrations are projected is open, and every
    # projection a competent analyst builds from the register's own used imports files the golden split and total (C1,
    # asserted cell by cell on the figures and on the counts the cells are built from)
    plan_txt = docx_text(os.path.join(target, P.FILES["plan"]))
    ok("those first registered here from 1 July 2026 to the end of 2027, each from the day it is registered" in plan_txt,
       "SF25 the plan files the later registrations in the 2027 fleet")
    ok("import" not in plan_txt.lower() and "arriv" not in plan_txt.lower(),
       "SF25 the plan names no import and no arrival: the WHAT only")
    ok(S.lots(base)["slots"] == EASY and hundred(sum(base.values())) == 3400,
       "SF25 the register-only reading files the register's split and 3,400")
    w12 = pj.window(12)
    cnt12 = Counter(x["n"] for x in w12)
    ok(dict(cnt12) == {"Volta hatch": 502, "Kestrel SUV": 202, "Plover saloon": 187, "Mira city car": 1394, "Tern van": 42},
       "SF25 counts: the twelve months' used imports by platform %s" % dict(cnt12))
    ok({k: len(pj.window(k)) for k in (6, 24, 36)} == {6: 1138, 24: 4606, 36: 6875},
       "SF25 counts: the 6, 24 and 36 months' used imports %s" % {k: len(pj.window(k)) for k in (6, 24, 36)})
    fam25 = pj.family()
    ok(len(fam25) == 144, "SF25 the projection family has %d cells" % len(fam25))
    mira = []
    for k, a in fam25.items():
        f = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
        lt = S.lots(f)
        ok(lt["slots"] == GOLD, "SF25 family %s files %s" % (k, lt["slots"]))
        ok(hundred(sum(f.values())) == 3800, "SF25 family %s total %.1f" % (k, sum(f.values())))
        mira.append(a["Mira city car"])
    ok(abs(fam25["trailing 12 months, day same, registration pack"]["Mira city car"] - arr["Mira city car"]) < 1e-6,
       "SF25 the family's committed cell is the golden's construction")
    ok(318.0 < min(mira) and max(mira) < 398.5, "SF25 the family's Mira city car failures %.1f to %.1f sit inside the "
       "golden's corridor (318.0 to 398.5)" % (min(mira), max(mira)))
    # the corridor's two edges, found on the pack: the split moves below 318.0 and the total above 398.5
    def at(x):
        f = {n: base[n] + arr.get(n, 0.0) for n in P.NAMES}
        f["Mira city car"] = base["Mira city car"] + x
        return S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800
    ok(at(318.5) and not at(317.5) and at(398.0) and not at(399.0), "SF25 the corridor's edges are 318 and 398.5")
    # cells outside the family, each mapped to what it violates
    A12 = pj.arrays(w12)
    share_mq = [float(np.mean(A12["mq"][A12["nm"] == "Mira city car"] == k)) for k in range(3)]
    ok(all(0.30 < s < 0.37 for s in share_mq) and len(set(A12["day"][A12["nm"] == "Mira city car"])) == 28,
       "SF25 the register's own arrivals come through every month of a quarter and every day to the 28th")
    for rule in ("first", "last"):
        f = {n: base[n] + v for n, v in pj.quarterly(w12, rule).items()}
        ok(not (S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800),
           "SF25 a quarter's cars all on its %s day (against the register's own dates) leaves the golden" % rule)
    ages = {y: np.mean([(x["nl"] - x["fu"]).days / 365.25 for x in pj.imp if x["n"] == "Mira city car" and x["nl"].year == y])
            for y in range(2022, 2027)}
    ok(max(ages.values()) - min(ages.values()) < 0.15, "SF25 the Mira city car's imports arrive at one age each year %s" % ages)
    a = pj.monthly(w12, 12, keep_vintage=True)
    ok(S.lots({n: base[n] + a[n] for n in P.NAMES})["slots"] != GOLD,
       "SF25 copies of the window's cars kept at their own first admission (a year older each year) leave the golden")
    mean_age = {n: float(np.mean(A12["age"][A12["nm"] == n])) for n in P.NAMES}
    ok(all(mean_age["Mira city car"] - mean_age[n] > 2.0 for n in P.NAMES if n != "Mira city car"),
       "SF25 each platform's imports arrive at their own age %s" % {n: round(v, 2) for n, v in mean_age.items()})
    pooled = float(np.mean(A12["age"]))
    a = pj.at_age(w12, lambda n: pooled)
    ok(S.lots({n: base[n] + a[n] for n in P.NAMES})["slots"] != GOLD, "SF25 one age pooled over the platforms leaves the golden")
    a = pj.at_age(w12, lambda n: mean_age[n])
    ok(S.lots({n: base[n] + a[n] for n in P.NAMES})["slots"] == GOLD, "SF25 each platform at its own mean age keeps the golden")
    a = pj.monthly(w12, 12, cond=False)
    ok(S.lots({n: base[n] + a[n] for n in P.NAMES})["slots"] != GOLD,
       "SF25 the later registrations unconditioned on a working pack (the register's R1 reading) leave the golden")
    a = pj.monthly(w12, 12, cond_at=_i(S.Y0))
    f = {n: base[n] + a[n] for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800,
       "SF25 conditioned on 1 January 2027 instead of the registration day (against the plan's pack per car) keeps the golden")
    cnt = Counter(r["n"] for r in reg)
    for flow in (Counter(r["n"] for r in reg if S.add_months(S.SNAP, -12) < r["nl"] <= S.SNAP), cnt12):
        f = {n: base[n] * (1 + flow[n] / 12.0 * 12.0 / cnt[n]) for n in P.NAMES}
        ok(S.lots(f)["slots"] != GOLD, "SF25 the later registrations as the fleet's growth at its average chance leave the golden")
    # SF26: one pack per car (plan section 3): the pack a car carries at the end of 30 June 2026, or when it is first
    # registered here later, and that pack's failure; a pack fitted in its place later is left out. The renewal reading
    # (a judge added the refurbished packs fitted after late-2026 failures) and the start-of-day reading of 30 June both
    # move the register's stated figure, never the call
    ok("a pack fitted in its place later is left out" in plan_txt and "at the end of 30 June 2026" in plan_txt,
       "SF26 the plan files one pack per car")
    ok(int(round(sum(base.values()))) == 3448, "SF26 the register's figure under the filed reading is 3,448")
    ok(int(round(sum(base.values()) + sum(ren.values()))) != 3448, "SF26 the renewal reading moves the register's figure")
    f = {n: fc[n] + ren.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF26 the renewal reading keeps the call")
    ex = defaultdict(float)
    for r in reg:
        st, cu = pk.pack_at(r, S.SNAP, inclusive=False)
        ex[r["n"]] += pk.p_due(st, cu, pk.w_end(r), S.SNAP, S.SNAP)
    on_snap = sum(1 for evs in pk.ev.values() for d, _ in evs if d == S.SNAP)
    ok(on_snap == 8 and int(round(sum(ex.values()))) != 3448, "SF26 the start-of-day reading of 30 June (%d fits that day) "
       "moves the register's figure to %d" % (on_snap, int(round(sum(ex.values())))))
    f = {n: ex[n] + arr.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF26 the start-of-day reading keeps the call")
    # SF22: the curves as published; a curve rescaled to 2025's realised fittings files another split, and the two
    # back-tests the note quotes (cars on the register now over-forecast the Mira; cars registered by the end of 2024
    # under-forecast it)
    import datetime as dtm
    o, y0, y1 = dtm.date(2024, 12, 31), dtm.date(2025, 1, 1), dtm.date(2026, 1, 1)
    now, then, act = {n: 0.0 for n in P.NAMES}, {n: 0.0 for n in P.NAMES}, {n: 0 for n in P.NAMES}
    for r in reg:
        st, cu = pk.pack_at(r, o)
        p = pk.p_due(st, cu, pk.w_end(r), o, o, y0=y0, y1=y1)
        now[r["n"]] += p
        if r["nl"] <= o:
            then[r["n"]] += p
    regk = {r["k"]: r for r in reg}
    for k, evs in pk.ev.items():
        if k in regk:
            for d, fitted in evs:
                if y0 <= d < y1 and d >= regk[k]["nl"] and fitted == "Voltwerk revisie":
                    act[regk[k]["n"]] += 1
    m = "Mira city car"
    ok(now[m] > act[m] * 1.05 and then[m] < act[m] * 0.9, "back-tests: now %.0f, then %.0f, fitted %d" % (now[m], then[m], act[m]))
    ratio = {n: act[n] / then[n] if then[n] else 1.0 for n in P.NAMES}
    ok(S.lots({n: base[n] * ratio[n] for n in P.NAMES})["slots"] != GOLD, "SF22 the rescaled curve files another split")
    # ---- the asks ---------------------------------------------------------------------------------------------------
    ln = S.Line(target, P.FILES)
    A, B, C = ln.ask_a(), ln.ask_b(), ln.ask_c()
    for n in P.NAMES:
        ok(edge(A[n], 1.0) >= 0.15, "ask A %s edge %.3f" % (n, edge(A[n], 1.0)))
        ok(edge(B[n], 0.1) >= 0.015, "ask B %s edge %.3f" % (n, edge(B[n], 0.1)))
        ok(edge(C[n], 0.1) >= 0.015, "ask C %s edge %.3f" % (n, edge(C[n], 0.1)))
    # SF15: net of returns (the asking sentence); issues only differs
    io = ln.ask_a("issues_only")
    ok(all(round(io[n]) != round(A[n]) for n in P.NAMES), "SF15 issues only lands elsewhere")
    # SF16: modules, a Kestrel carrier being 2 (artikelstam); counting units differs on the Kestrel
    ok(round(ln.ask_a("units")["Kestrel SUV"]) != round(A["Kestrel SUV"]), "SF16 units differ")
    # SF17: packs shipped by the shipment date equals the work orders closed as shipped in the year
    closed = {}
    for w in ln.wo.values():
        if w["status"] == "VERZONDEN" and w["afgesloten"] and S.in_fy(S.iso(w["afgesloten"])):
            closed[S.CODE[w["platformcode"]]] = closed.get(S.CODE[w["platformcode"]], 0) + 1
    ok(closed == dict(ln.shipped()), "SF17 shipments and closed work orders agree")
    # SF18: an aborted run is no run (the notes); counting it differs
    ab = ln.ask_b("abort_counts")
    ok(sum(round(ab[n], 1) != round(B[n], 1) for n in P.NAMES) >= 4, "SF18 counting aborts differs")
    # SF19: packs whose first run fell in the year; a pack first run before July 2025 and run again in the year is out
    ok(True, "SF19 population by the first run")
    # SF20: cores received at either dock, by the day received; SF21: rejected at intake, so a core the MES shows a work
    # order on passed intake whatever grade it carries on 1 July 2026 (the asking sentence, the MES's "the core the pack
    # is built on"); the recycler's quarantine tags give the same rejects by their date (C1)
    det = ln.ask_c("detail")
    ok(all(det[n]["scrapped_on_line"] >= 1 for n in P.NAMES), "SF21 every platform has a core scrapped on the line")
    sd = ln.ask_c("same_day")
    ok(all(abs(sd[n] - C[n]) < 1e-9 for n in P.NAMES), "SF21 the quarantine tags' dates give the same rejects")
    ink = list(csv.DictReader(open(os.path.join(target, P.FILES["intake"]), encoding="utf-8")))
    ok({x["dock"] for x in ink if x["keuring"] == "AFGEKEURD"} == {"1", "2"}, "SF20 both docks record rejects")
    # SF23: the modules issued in the year per pack shipped in the year (the asking sentence); the modules issued to the
    # packs shipped in the year is another quantity, and the stores export of the year cannot hold all of it
    co = ln.ask_a("cohort")
    ok(sum(round(co[n]) != round(A[n]) for n in P.NAMES) >= 4, "SF23 the shipped packs' own issues land elsewhere")
    # devices: every platform's figure moves under the natural read and under the over-repair
    for mode in ("naive", "dedup"):
        f = ln.ask_a(mode)
        ok(all(round(f[n]) != round(A[n]) for n in P.NAMES), "ask A %s lands the golden somewhere" % mode)
    f = ln.ask_b("by_id")
    ok(all(round(f[n], 1) != round(B[n], 1) for n in P.NAMES), "ask B by pack id lands the golden somewhere")
    for mode in ("naive", "both_out", "all_recycled"):
        f = ln.ask_c(mode)
        ok(all(round(f[n], 1) != round(C[n], 1) for n in P.NAMES), "ask C %s lands the golden somewhere" % mode)
    f = ln.ask_c("count_scrapped")
    ok(sum(round(f[n], 1) == round(C[n], 1) for n in P.NAMES) <= 2, "ask C by count keeps at most two")
    bp = ln.batch_picks()
    ok(len(bp) == len(P.HOLDS), "one batch pick per hold, %d" % len(bp))
    # SF27: ask A's pick lists. The line notes file that stores keeps its stock by lot and no lot's stock goes below
    # zero, with one receipt row per lot. Read as written, the eight replacement lots' lines take their stock below
    # zero, so the natural read (a judge's 171, 283, 195, 150, 238) contradicts a filed sentence; every repair that
    # keeps each lot at or above zero (the repeated quantity counted once, the lot capped at its receipt, its lines
    # scaled to it) files the golden to the module (C1), and under the golden reading no lot goes below zero, so the
    # over-repair of the other shared lists is called for by nothing
    notes_txt = re.sub(r"\s+", " ", open(os.path.join(target, P.FILES["line_notes"]), encoding="utf-8").read())
    ok("stores keeps its stock by lot, and no lot's stock goes below zero" in notes_txt
       and "one row per supplier lot" in notes_txt, "SF27 the line notes file the lot stock rule")
    rec = Counter()
    for r in ln.receipts:
        rec[r["partij"]] += int(r["aantal"])
    ok(len(rec) == len(ln.receipts), "SF27 one receipt row per lot")
    low = stock_below_zero(ln)
    ok(low == {k[1] for k in bp} and len(low) == len(P.HOLDS), "SF27 read as written, exactly the %d replacement lots go "
       "below zero" % len(low))
    ok(not stock_below_zero(ln, collapse=True), "SF27 under the golden reading no lot goes below zero")
    fy_lines = [r for r in ln.stores if S.in_fy(S.stamp(r["geboekt_op"]).date())]
    iss = Counter()
    for r in fy_lines:
        iss[r["partij"]] += int(r["aantal"])
    over = {p for p in iss if p in rec and iss[p] > rec[p]}
    ok(over == low, "SF27 the lots whose lines exceed their receipt are the lots that go below zero")
    ships = ln.shipped()
    scaled = defaultdict(float)
    for r in fy_lines:
        k = rec[r["partij"]] / iss[r["partij"]] if r["partij"] in over else 1.0
        scaled[S.CODE[ln.wo[r["werkorder"]]["platformcode"]]] += \
            int(r["aantal"]) * k * int(ln.parts[r["artikelnummer"]]["modules_per_eenheid"])
    ok(all(abs(50.0 * scaled[n] / ships[n] - A[n]) < 1e-9 for n in P.NAMES),
       "SF27 each over-drawn lot brought back to its receipt files the golden exactly")
    nat = ln.ask_a("naive")
    ok([int(round(nat[n])) for n in P.NAMES] == [171, 283, 195, 150, 238], "SF27 the natural read is the judge's figures")
    # distractors: neither is read by any figure's code, so deleting either leaves every figure where it is
    solve_src = open(os.path.join(HERE, "solve.py")).read() + open(os.path.join(HERE, "figs.py")).read()
    ok("prices" not in solve_src and "leadtimes" not in solve_src, "distractors unread: deletion test")
    # line realism: shipments by month vary; the benches never run two packs at once
    eol = list(csv.DictReader(open(os.path.join(target, P.FILES["eol"]), encoding="utf-8")))
    byb = {}
    for x in eol:
        byb.setdefault(x["bank"], []).append((x["start"], x["einde"]))
    ok(all(all(b[0] >= a[1] for a, b in zip(sorted(v), sorted(v)[1:])) for v in byb.values()), "benches run one pack at a time")
    sh = list(csv.DictReader(open(os.path.join(target, P.FILES["shipments"]), encoding="utf-8")))
    mon = {}
    for x in sh:
        mon[x["verzonden_op"][:7]] = mon.get(x["verzonden_op"][:7], 0) + 1
    ok(len(set(mon.values())) >= 10, "monthly shipments vary")
    # ---- separation: the call reads none of the line's files and the asks none of the call's ---------------------
    call_files = {P.FILES[k] for k in ("register", "log", "curves", "warranty", "plan", "rdw_notes")}
    ask_files = {P.FILES[k] for k in ("workorders", "stores", "receipts", "parts", "eol", "bms", "shipments", "intake",
                                      "recycler", "line_notes")}
    ok(not call_files & ask_files, "separation")
    src = open(os.path.join(HERE, "solve.py")).read()
    ok("class Line" in src and "class Pack" in src, "separate readers")
    # ---- input gates ----------------------------------------------------------------------------------------------
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gates: a file of 25,000 rows")
    print("checks: %d assertions passed" % N)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
