"""The impaired-driving arrests with a blood specimen, 2023 to 2025 and the days around them: the census's arrested
drivers and the arrests away from fatal crashes, each with its agency, county, time and first specimen's result. The
county courts' cases are cut from them (court.py). The laboratory's own specimen extract no longer ships, so its
writers are gone; the arrests are drawn exactly as they were."""
import datetime as dt
import math

import agencies as AG
import geo as G
import truth as T
import world as W

SERUM_FREE = (0.140, 0.163)                   # whole-blood values no serum result carries (any ratio 1.10 to 1.25)
CORONER_ID = {c["fips"]: "CO%s00" % c["fips"] for c in W.COUNTIES}
ME_ID = "ME00000"
ME_COUNTIES = ("013", "011", "023")          # the medical examiner takes these counties' deaths
# impaired-driving arrests with a blood specimen to the laboratory, per 100 million vehicle miles a year
ARREST_RATE = {"001": 7.36, "003": 9.6, "005": 8.1, "007": 6.9, "009": 6.2, "011": 8.8, "013": 7.14, "015": 7.9,
               "017": 8.3, "019": 7.6, "021": 6.6, "023": 6.4, "025": 7.0, "027": 12.9}


class Arrest:
    __slots__ = ("agency", "fips", "when", "case", "bac", "drug_only", "screen", "second", "site", "serum", "tube2",
                 "reanalysis", "cancel", "crash", "kind", "subject")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def _trunc3(v):
    return math.floor(v * 1000 + 1e-9) / 1000.0


def _arrest_bac(rng, h):
    if rng.random() < 0.09:
        return 0.0 if rng.random() < 0.40 else _trunc3(float(rng.uniform(0.010, 0.0799)))
    if rng.random() < h:
        return T.avoid_edges(_trunc3(min(0.150 + float(rng.gamma(2.0, 0.042)), 0.398)))
    return T.avoid_edges(_trunc3(float(rng.uniform(0.080, 0.1499))))


def _hi_share(fips, group):
    k = T.knobs(fips)
    if group == "SP":
        return 0.56
    return min(0.80, max(0.30, 0.22 + 0.58 * k["hiL"]))


def _arrest_time(rng, year):
    while True:
        d = dt.date(year, 1, 1) + dt.timedelta(days=int(rng.integers(0, 366 if year % 4 == 0 else 365)))
        wk = 1.6 if d.weekday() in (4, 5) else (1.15 if d.weekday() == 6 else 0.8)
        if rng.random() < wk / 1.6:
            break
    h = int(rng.choice([17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 10, 13, 15],
                       p=[0.03, 0.04, 0.05, 0.07, 0.09, 0.12, 0.14, 0.13, 0.12, 0.09, 0.05, 0.02, 0.01, 0.02, 0.02]))
    return dt.datetime(d.year, d.month, d.day, h, int(rng.integers(0, 60)))


def _site(rng, fips, group, univ=False):
    own, nb = G.draw_sites(fips)
    hosp = G.HOSPITALS.get(fips, [])
    if univ:
        return G.HOSPITALS["027"][0]
    if group == "SP":
        u = rng.random()
        if u < 0.17 and nb:
            return nb[int(rng.integers(0, len(nb)))]
        if u < 0.42 or not hosp:
            return G.JAILS[fips]
        return hosp[int(rng.integers(0, len(hosp)))]
    if not hosp:
        return G.JAILS[fips] if rng.random() < 0.5 else nb[int(rng.integers(0, len(nb)))]
    u = rng.random()
    if u < 0.06 and nb:
        return nb[int(rng.integers(0, len(nb)))]
    if u < 0.46:
        return G.JAILS[fips]
    return hosp[int(rng.integers(0, len(hosp)))]


def arrests(order, vmt):
    """Every impaired-driving arrest with a blood specimen, 2023 to 2025, plus the last days of 2022 and the first of
    2026 that the extract's received dates reach: the census's arrested drivers and the arrests away from crashes."""
    out = []
    # the census's arrested drivers (fatal crashes), with the crash's report number as the case number
    for cr in order:
        for p in cr.persons:
            if p.is_driver and p.identified and not p.killed and p.arrested:
                rng = T.rng_for("crash_arrest", cr.cid, p.unit)
                when = dt.datetime(cr.date.year, cr.date.month, cr.date.day, cr.hour, cr.minute)
                grp = cr.group
                out.append(Arrest(agency=cr.agency, fips=cr.fips, when=when, case=cr.report, bac=p.bac,
                                  drug_only=False, screen=rng.random() < 0.45, second=False,
                                  site=_site(rng, cr.fips, grp, cr.agency.kind == "University Police"),
                                  serum=False, tube2=rng.random() < 0.05, reanalysis=None, cancel=False, crash=cr,
                                  kind="DUI"))
    # arrests away from fatal crashes
    for c in W.COUNTIES:
        f = c["fips"]
        k = T.knobs(f)
        for y in (2022, 2023, 2024, 2025, 2026):
            rng = T.rng_for("arrests", f, y)
            vy = vmt[f] / 3.0 / 1e8
            n = int(round(ARREST_RATE[f] * vy * (1.0 + 0.035 * (y - 2024)) * float(rng.uniform(0.95, 1.05))))
            for i in range(n):
                when = _arrest_time(rng, y)
                if (y == 2022 and when.date() < dt.date(2022, 12, 24)) or (y == 2026 and when.date() > dt.date(2026, 1, 12)):
                    continue
                out.append(_one(rng, f, k, when))
            # New Year's Eve saturation patrols
            for i in range(int(rng.integers(2, 6)) if y < 2026 else 0):
                when = dt.datetime(y, 12, 31, int(rng.choice([18, 19, 20, 21, 22, 23])), int(rng.integers(0, 60)))
                out.append(_one(rng, f, k, when))
    _place_shares(out)
    return out


def _edge(v, unit=0.1):
    return unit / 2 - abs(v - round(v / unit) * unit)


def _place_shares(arrests_, need=0.012):
    """Each county's 2025 per cent at .15 or more away from the edge of its one-decimal cell: the fewest arrests away
    from crashes whose first specimen sits just either side of .15 are read on the other side of it."""
    for c in W.COUNTIES:
        f = c["fips"]
        mine = [a for a in arrests_ if a.fips == f and a.kind == "DUI" and a.when.year == 2025]
        n = len(mine)
        h = sum(1 for a in mine if not a.drug_only and not a.cancel and a.bac >= 0.150)
        if _edge(100.0 * h / n) >= need:
            continue
        free = [a for a in mine if a.crash is None and not a.drug_only and not a.cancel and not a.serum]
        up = sorted([a for a in free if 0.136 <= a.bac < 0.150], key=lambda a: T.rng_for("pu", a.case or "", a.when).random())
        down = sorted([a for a in free if 0.150 <= a.bac <= 0.164], key=lambda a: T.rng_for("pd", a.case or "", a.when).random())
        for k in (1, -1, 2, -2, 3, -3):
            if _edge(100.0 * (h + k) / n) >= need:
                break
        moved = up[:k] if k > 0 else down[:-k]
        for a in moved:
            a.bac = 0.150 + (0.150 - a.bac) if k > 0 else 0.149 - (a.bac - 0.150)
            a.bac = _trunc3(min(max(a.bac, 0.080), 0.398))
        h2 = sum(1 for a in mine if not a.drug_only and not a.cancel and a.bac >= 0.150)
        assert h2 == h + k and _edge(100.0 * h2 / n) >= need, (f, h, h2, n)


def _one(rng, f, k, when):
    u = rng.random()
    sp_share = 0.12 + 0.65 * k["sp"]
    so_share = 0.85 * k["so"]
    if u < sp_share:
        a, grp = AG.patrol_post(f), "SP"
    elif u < sp_share + so_share:
        a, grp = AG.sheriff(f), "SO"
    else:
        a, grp = AG.city_pd(f, rng), "PD"
    drug_only = rng.random() < 0.062
    bac = None if drug_only else _arrest_bac(rng, _hi_share(f, grp))
    site = _site(rng, f, grp, a.kind == "University Police")
    # a hospital's serum result is never one whose class at .15 turns on the serum ratio (1.10 to 1.25 agree)
    serum = site.kind == "Hospital" and not drug_only and rng.random() < 0.035 and not (SERUM_FREE[0] <= bac <
                                                                                      SERUM_FREE[1])
    re = None
    if not drug_only and rng.random() < 0.026:
        re = round(float(rng.choice([-1, 1])) * float(rng.uniform(0.004, 0.011)), 3)
    return Arrest(agency=a, fips=f, when=when, case=None, bac=bac, drug_only=drug_only,
                  screen=drug_only or rng.random() < 0.28, second=(not drug_only) and rng.random() < 0.036,
                  site=site, serum=serum, tube2=(not drug_only) and rng.random() < 0.05, reanalysis=re,
                  cancel=rng.random() < 0.007 and when.year != 2025, crash=None, kind="DUI")
