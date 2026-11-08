"""task184 analysis on the shipped files: one reader of target/, then every route (the golden, its defensible family,
each rung of the ladder, the close-out and its cracker) computed from what the reader returns."""
import collections
import csv
import datetime as dt
import json
import os

import openpyxl

WINDOW = [dt.date(2027, 2, 10) + dt.timedelta(days=i) for i in range(5)]
LINE = 150
COURSE_FROM, COURSE_TO = dt.date(2025, 1, 1), dt.date(2026, 12, 31)
CLOSEOUT_FROM, CLOSEOUT_TO = dt.date(2027, 1, 18), dt.date(2027, 1, 31)
D = dt.date.fromisoformat


def _rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, target):
        self.t = target
        f = lambda n: os.path.join(target, n)
        names = sorted(os.listdir(target))
        pick = lambda prefix: f([n for n in names if n.startswith(prefix)][0])
        wb = openpyxl.load_workbook(pick("farm_register"), read_only=True)
        ws = wb.worksheets[0]
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        self.reg = [dict(zip(head, r)) for r in it if r and r[0]]
        self.by_name = {r["Farm"]: r["Farm code"] for r in self.reg}
        self.by_site = {r["Hatchery site"]: r["Farm code"] for r in self.reg}
        self.by_catcher = {r["Catcher site"]: r["Farm code"] for r in self.reg}
        self.house_by_gname = {(r["Farm code"], r["Grower's name for house"]): r["House"] for r in self.reg}
        self.grower_no = {int(r["Plant grower no"]): r["Farm code"] for r in self.reg}
        # daily returns: the app, then the paper sheets keyed before each farm moved to the app
        self.ret = {}
        for r in _rows(pick("grower_app_returns")):
            k = (r["farm_code"], r["house"], D(r["record_date"]))
            self.ret.setdefault(k, (int(r["found_dead"]), int(r["culled"])))
        self.paper_only = 0
        for r in _rows(pick("paper_record_sheets")):
            fc = self.by_name[r["Farm"]]
            hc = self.house_by_gname[(fc, r["Shed"])]
            d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
            k = (fc, hc, d)
            if k not in self.ret:
                self.ret[k] = (int(r["Mort"]), int(r["Culls"]))
                self.paper_only += 1
        # crops
        self.flock = {}
        for r in _rows(pick("flock_register")):
            self.flock[(r["crop_ref"], r["house"])] = dict(farm=r["farm_code"], house=r["house"], placed=D(r["placed_on"]))
        # chicks placed: the company hatchery's despatches; the bought-in chicks from Lindewaard for December
        self.chicks = collections.defaultdict(int)          # (farm, house, placed) -> chicks, each file read as written
        self.chicks_plain = collections.defaultdict(int)    # the same, chicks plus free on every row
        self.chicks_only = collections.defaultdict(int)     # the same, the chicks column alone on every row
        for r in _rows(pick("kirton_holme_despatches")):
            k = (self.by_site[r["customer_site"]], r["house"], D(r["delivered_on"]))
            self.chicks[k] += int(r["chicks"]) + int(r["free_chicks"])
            self.chicks_plain[k] += int(r["chicks"]) + int(r["free_chicks"])
            self.chicks_only[k] += int(r["chicks"])
        for r in _rows(pick("lindewaard_leveringen")):
            fc = self.by_name[r["bedrijf"]]
            k = (fc, self.house_by_gname[(fc, r["stal"])], dt.datetime.strptime(r["afleverdatum"], "%d-%m-%Y").date())
            boxes, per, kuikens, gratis = int(r["dozen"]), int(r["kuikens_per_doos"]), int(r["kuikens"]), int(r["gratis_kuikens"])
            # a box of 101 already counts its free chick; a box of 100 does not
            self.chicks[k] += kuikens if per == 101 else kuikens + gratis
            self.chicks_plain[k] += kuikens + gratis
            self.chicks_only[k] += kuikens
        # catches
        self.catch = collections.defaultdict(list)          # (farm, house) -> [(night, birds_caught)]
        for r in _rows(pick("wash_catching_sheets")):
            k = (self.by_catcher[r["site"]], "H" + r["shed"])
            self.catch[k].append((D(r["catch_night"]), int(r["birds_caught"])))
        for k in self.catch:
            self.catch[k].sort()
        self._hc = None
        self._ret_days = collections.defaultdict(list)
        for (fc, hc, d) in self.ret:
            self._ret_days[(fc, hc)].append(d)

    # ------------------------------------------------------------ house-crops with their life and their alive series
    def house_crops(self):
        if self._hc is not None:
            return self._hc
        by_house = collections.defaultdict(list)
        for (ref, house), v in self.flock.items():
            by_house[(v["farm"], house)].append((v["placed"], ref))
        out = []
        for (farm, house), lst in by_house.items():
            lst.sort()
            for i, (placed, ref) in enumerate(lst):
                nxt = lst[i + 1][0] if i + 1 < len(lst) else dt.date(2099, 1, 1)
                nights = [(n, b) for (n, b) in self.catch.get((farm, house), []) if placed < n < nxt]
                # the house is cleared on the catch night after which its returns stop; an earlier night thins it
                rdays = [d for d in self._ret_days.get((farm, house), []) if placed < d < nxt]
                lastret = max(rdays) if rdays else placed
                clears = [n for (n, b) in nights if n >= lastret]
                clear = clears[0] if clears else None
                thins = [(n, b) for (n, b) in nights if n < lastret]
                thin_night, thinned = (thins[0] if thins else (None, 0))
                chicks = self.chicks.get((farm, house, placed), 0)
                days = []
                alive = chicks
                last = clear if clear is not None else WINDOW[-1]
                d = placed + dt.timedelta(days=1)
                while d <= last:
                    k = (farm, house, d)
                    if k not in self.ret:
                        d += dt.timedelta(days=1)
                        continue
                    dead, culled = self.ret[k]
                    a = (d - placed).days
                    post = thin_night is not None and d > thin_night
                    days.append((d, a, alive, dead, culled, post))
                    alive -= dead + culled
                    if thin_night is not None and d == thin_night:
                        alive -= thinned
                    d += dt.timedelta(days=1)
                out.append(dict(farm=farm, house=house, ref=ref, placed=placed, clear=clear, thin=thin_night,
                                thin_age=(thin_night - placed).days if thin_night else None, thinned=thinned,
                                chicks=chicks, days=days))
        self._hc = out
        return out

    # ------------------------------------------------------------ the ordinary course
    def course(self, years=(2025, 2026), pooled=False, culls=False, midday=False, by=None):
        num, den = collections.defaultdict(float), collections.defaultdict(float)
        for hc in self.house_crops():
            if hc["clear"] is None or not (COURSE_FROM <= hc["clear"] <= COURSE_TO) or hc["clear"].year not in years:
                continue
            for (d, a, alive, dead, culled, post) in hc["days"]:
                key = (a, False if pooled else post) if by is None else (a, False if pooled else post, by(hc, d))
                num[key] += dead + (culled if culls else 0)
                den[key] += alive - (dead + culled) / 2.0 if midday else alive
        return num, den


def rate_fn(num, den):
    def r(a, post):
        k = (a, post)
        if den.get(k, 0) <= 0:
            k = (a, False)
        if den.get(k, 0) <= 0:
            k = (min(a, 42), post) if den.get((min(a, 42), post), 0) > 0 else (min(a, 42), False)
        return num[k] / den[k]
    return r


def window_houses(p):
    out = []
    for hc in p.house_crops():
        win = [x for x in hc["days"] if x[0] in WINDOW]
        if len(win) == 0:
            continue
        out.append((hc, win))
    return out


FAMILY = ("golden", "y2026", "y2025", "farm_effect", "house_effect", "month", "weather", "midday", "thin_factor")


def _weather(p):
    """Mean of the two stations' daily minimum temperature, by date."""
    path = os.path.join(p.t, [n for n in os.listdir(p.t) if n.startswith("met_daily_weather")][0])
    acc = collections.defaultdict(list)
    for r in _rows(path):
        acc[D(r["date"])].append(float(r["min_temp_c"]))
    return {d: sum(v) / len(v) for d, v in acc.items()}


def _course_days(p):
    for hc in p.house_crops():
        if hc["clear"] is None or not (COURSE_FROM <= hc["clear"] <= COURSE_TO):
            continue
        for x in hc["days"]:
            yield hc, x


def family_member(p, variant):
    """One defensible background: returns ex(farm, house, day) giving that day's ordinary deaths, and whether culls
    are counted."""
    v = variant
    if v in ("y2026", "y2025"):
        num, den = p.course(years=(int(v[1:]),))
    else:
        num, den = p.course(midday=(v == "midday"))
    rate = rate_fn(num, den)
    if v == "thin_factor":
        # one age course for unthinned flocks and a single factor for the birds left after a thin
        un = rate_fn(*p.course(pooled=False))
        o = e = 0.0
        for hc, (d, a, alive, dead, culled, post) in _course_days(p):
            if post:
                o += dead
                e += un(a, False) * alive
        fac = o / e
        rate = lambda a, post: un(a, False) * (fac if post else 1.0)
    base = lambda farm, house, x: rate(x[1], x[5]) * (x[2] - (x[3] + x[4]) / 2.0 if v == "midday" else x[2])
    if v in ("farm_effect", "house_effect", "month"):
        o, e = collections.defaultdict(float), collections.defaultdict(float)
        for hc, x in _course_days(p):
            key = {"farm_effect": hc["farm"], "house_effect": (hc["farm"], hc["house"]), "month": x[0].month}[v]
            o[key] += x[3]
            e[key] += base(hc["farm"], hc["house"], x)
        k = {"farm_effect": 2000.0, "house_effect": 800.0, "month": 0.0}[v]
        sc = {key: (o[key] + k) / (e[key] + k) for key in o}
        if v == "farm_effect":
            return (lambda farm, house, x: base(farm, house, x) * sc.get(farm, 1.0)), False
        if v == "house_effect":
            return (lambda farm, house, x: base(farm, house, x) * sc.get((farm, house), 1.0)), False
        return (lambda farm, house, x: base(farm, house, x) * sc[x[0].month]), False
    if v == "weather":
        # a log-linear term in the day's minimum temperature, fitted by Poisson likelihood on the course's days
        tmin = _weather(p)
        pts = [(x[3], base(hc["farm"], hc["house"], x), tmin[x[0]]) for hc, x in _course_days(p) if x[0] in tmin]
        tbar = sum(e * t for _, e, t in pts) / sum(e for _, e, _ in pts)
        b = 0.0
        import math
        for _ in range(8):
            g = sum((o - e * math.exp(b * (t - tbar))) * (t - tbar) for o, e, t in pts)
            h = sum(e * math.exp(b * (t - tbar)) * (t - tbar) ** 2 for o, e, t in pts)
            b += g / h
        return (lambda farm, house, x: base(farm, house, x) * math.exp(b * (tmin[x[0]] - tbar))), False
    return base, v == "culls"


def expected(member, farm, house, days):
    ex = member[0]
    return sum(ex(farm, house, x) for x in days)


def infection_deaths(p, variant="golden"):
    """Per house and per farm: deaths in the window less the ordinary course for that house's birds."""
    member = family_member(p, variant)
    culls = member[1]
    houses, farms = {}, collections.defaultdict(float)
    obs_f = collections.defaultdict(int)
    for hc, win in window_houses(p):
        o = sum(x[3] + (x[4] if culls else 0) for x in win)
        ex = expected(member, hc["farm"], hc["house"], win)
        houses[(hc["farm"], hc["house"])] = o - ex
        farms[hc["farm"]] += o - ex
        obs_f[hc["farm"]] += o
    return houses, dict(farms), dict(obs_f)


def rung(p, name):
    """The farm-level excess each wrong route files, in birds over the five days."""
    farms = collections.defaultdict(float)
    if name in FAMILY:
        return infection_deaths(p, name)[1]
    if name == "pooled":
        num, den = p.course(pooled=True)
        rate = rate_fn(num, den)
        for hc, win in window_houses(p):
            farms[hc["farm"]] += sum(x[3] - rate(x[1], False) * x[2] for x in win)
        return dict(farms)
    if name == "prev_week":
        for hc, win in window_houses(p):
            prv = [x for x in hc["days"] if WINDOW[0] - dt.timedelta(days=7) <= x[0] < WINDOW[0]]
            o = sum(x[3] for x in win)
            al = sum(x[2] for x in win)
            if prv and sum(x[2] for x in prv) > 0:
                rr = sum(x[3] for x in prv) / sum(x[2] for x in prv)
                farms[hc["farm"]] += o - rr * al
            else:
                farms[hc["farm"]] += 0.0
        return dict(farms)
    if name == "flat":
        num, den = p.course(pooled=True)
        rr = sum(num.values()) / sum(den.values())
        for hc, win in window_houses(p):
            farms[hc["farm"]] += sum(x[3] for x in win) - rr * sum(x[2] for x in win)
        return dict(farms)
    if name == "peers":
        # the same week's other farms at the same age, two days either side
        pool = collections.defaultdict(lambda: [0.0, 0.0])
        rows = []
        for hc, win in window_houses(p):
            for x in win:
                rows.append((hc["farm"], x))
        for hc, win in window_houses(p):
            o = sum(x[3] for x in win)
            ex = 0.0
            for x in win:
                n = dd = 0.0
                for (fm, y) in rows:
                    if fm != hc["farm"] and abs(y[1] - x[1]) <= 2:
                        n += y[3]
                        dd += y[2]
                ex += (n / dd) * x[2] if dd > 0 else 0.0
            farms[hc["farm"]] += o - ex
        return dict(farms)
    if name == "calendar":
        # each house's own deaths per bird on the same calendar days of the two earlier years
        for hc, win in window_houses(p):
            o = sum(x[3] for x in win)
            n = dd = 0.0
            for yrs in (1, 2):
                for x in win:
                    d0 = dt.date(x[0].year - yrs, x[0].month, x[0].day)
                    for hc2 in p.house_crops():
                        if hc2["farm"] == hc["farm"] and hc2["house"] == hc["house"]:
                            for y in hc2["days"]:
                                if y[0] == d0:
                                    n += y[3]
                                    dd += y[2]
            rr = n / dd if dd > 0 else 0.0
            farms[hc["farm"]] += o - rr * sum(x[2] for x in win)
        return dict(farms)
    raise KeyError(name)


def swab_set(farms):
    return sorted(f for f, v in farms.items() if v > LINE)


# ------------------------------------------------------------------ January close-out
def closeout(p, route="golden"):
    """Per crop cleared on a catch night from 4 to 17 January: chicks placed, birds sent to the plant (dead on
    arrival included), recorded deaths and culls, and birds unaccounted for."""
    intake = _rows(os.path.join(p.t, [n for n in os.listdir(p.t) if n.startswith("riverside_intake")][0]))
    line2 = json.load(open(os.path.join(p.t, [n for n in os.listdir(p.t) if n.startswith("riverside_line2")][0])))["loads"]
    hung2 = {int(r["ticket"]): r["birds_hung"] for r in line2}
    crops = collections.defaultdict(list)
    for hc in p.house_crops():
        if hc["clear"] is not None and CLOSEOUT_FROM <= hc["clear"] <= CLOSEOUT_TO:
            crops[hc["ref"]].append(hc)
    # a crop belongs to the close-out when every house's clearance night falls in the window
    out = {}
    switch = dt.date(2027, 1, 18)
    for ref, hcs in crops.items():
        farm = hcs[0]["farm"]
        if route == "golden":
            placed = sum(p.chicks[(h["farm"], h["house"], h["placed"])] for h in hcs)
        elif route in ("cracker", "repair_a"):
            placed = sum(p.chicks_plain[(h["farm"], h["house"], h["placed"])] for h in hcs)
        elif route == "overclean":
            placed = sum(p.chicks_only[(h["farm"], h["house"], h["placed"])] for h in hcs)
        elif route == "repair_b":
            placed = sum(p.chicks[(h["farm"], h["house"], h["placed"])] for h in hcs)
        sent = 0
        for r in intake:
            if r["flock_ref"] != ref:
                continue
            night = dt.datetime.fromisoformat(r["weighed_in_utc"].replace("Z", "")).date()
            birds, doa = int(r["birds"]), int(r["doa"])
            if route in ("golden", "repair_a"):
                sent += birds if night >= switch else birds + doa
            elif route in ("cracker", "repair_b"):
                sent += birds + doa
            elif route == "overclean":
                sent += birds
        dead = sum(x[3] for h in hcs for x in h["days"])
        culled = sum(x[4] for h in hcs for x in h["days"])
        out[ref] = dict(farm=farm, placed=placed, sent=sent, dead=dead, culled=culled,
                        unaccounted=placed - sent - dead - culled)
    return out
