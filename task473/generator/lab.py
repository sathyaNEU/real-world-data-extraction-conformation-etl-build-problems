"""The State Toxicology Laboratory's specimens: every impaired-driving arrest whose blood the laboratory received, the
fatal crash procedure's draws from surviving drivers who were not arrested, the coroners' and the medical examiner's
death investigations, and the other criminal cases; as the laboratory's information system exports them (one row per
analysis, collection times in UTC). The census's tested drivers are among them, with the same results."""
import datetime as dt
import math

import agencies as AG
import geo as G
import truth as T
import world as W

EXTRACT_FROM = dt.date(2023, 1, 1)           # received dates covered by the extract
EXTRACT_TO = dt.date(2026, 1, 15)
SERUM = 1.16                                  # the laboratory's serum to whole-blood ratio
COLS = ["lab_number", "case_type", "submitting_agency", "agency_case_number", "collection_site", "collected_utc",
        "received_date", "specimen", "tube", "analyte", "result", "units", "report_status", "report_date"]
CORONER_ID = {c["fips"]: "CO%s00" % c["fips"] for c in W.COUNTIES}
ME_ID = "ME00000"
ME_COUNTIES = ("013", "011", "023")          # the medical examiner takes these counties' deaths
# impaired-driving arrests with a blood specimen to the laboratory, per 100 million vehicle miles a year
ARREST_RATE = {"001": 7.4, "003": 9.6, "005": 8.1, "007": 6.9, "009": 6.2, "011": 8.8, "013": 7.14, "015": 7.9,
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
    serum = site.kind == "Hospital" and not drug_only and rng.random() < 0.035 and abs(bac - 0.150) > 0.004
    re = None
    if not drug_only and rng.random() < 0.026:
        re = round(float(rng.choice([-1, 1])) * float(rng.uniform(0.004, 0.011)), 3)
    return Arrest(agency=a, fips=f, when=when, case=None, bac=bac, drug_only=drug_only,
                  screen=drug_only or rng.random() < 0.28, second=(not drug_only) and rng.random() < 0.036,
                  site=site, serum=serum, tube2=(not drug_only) and rng.random() < 0.05, reanalysis=re,
                  cancel=rng.random() < 0.007, crash=None, kind="DUI")


def _number_cases(arrests_, numbers):
    """Each agency numbers its cases through the year; a fatal crash's arrest keeps the crash report's number."""
    for a in sorted(arrests_, key=lambda a: (a.when, a.fips, a.agency.aid)):
        if not a.case:
            a.case = numbers.next(a.agency, a.when.date(), int(T.rng_for("caseno", a.agency.aid, a.when.isoformat())
                                                               .integers(0, 4)))


def _utc(local):
    return local.replace(tzinfo=W.CENTRAL).astimezone(W.UTC)


def specimens(order, arrests_, numbers):
    """Every specimen kit the laboratory received, with its analyses: one row per analysis and tube."""
    _number_cases(arrests_, numbers)
    kits = []
    for a in arrests_:
        rng = T.rng_for("kit", a.agency.aid, a.case)
        # the draw: 20 to 110 minutes after the arrest, and never past midnight on New Year's Eve
        lag = int(rng.integers(20, 111))
        coll = a.when + dt.timedelta(minutes=lag)
        if a.when.month == 12 and a.when.day == 31 and coll.date() != a.when.date():
            coll = a.when.replace(hour=23, minute=59) if a.when.hour == 23 else a.when + dt.timedelta(minutes=15)
            if coll.date() != a.when.date():
                coll = a.when.replace(hour=23, minute=59)
        agency = AG.PATROL_ID if a.agency.kind == "State Patrol" else a.agency.aid
        kits.append(dict(arrest=a, case_type=a.kind, agency=agency, case=a.case, coll=coll, site=a.site,
                         specimen="SER" if a.serum else "WB", bac=a.bac, drug_only=a.drug_only, screen=a.screen,
                         tube2=a.tube2, re=a.reanalysis, cancel=a.cancel, first=True))
        if a.second:
            coll2 = coll + dt.timedelta(minutes=int(rng.integers(50, 85)))
            if not (a.when.month == 12 and a.when.day == 31 and coll2.date() != a.when.date()):
                drop = 0.017 * (coll2 - coll).total_seconds() / 3600.0 + float(rng.uniform(-0.003, 0.003))
                kits.append(dict(arrest=a, case_type=a.kind, agency=agency, case=a.case, coll=coll2, site=a.site,
                                 specimen="SER" if a.serum else "WB", bac=_trunc3(max(0.0, a.bac - drop)),
                                 drug_only=False, screen=False, tube2=False, re=None, cancel=False, first=False))
    # the fatal crash procedure's draws from surviving drivers not arrested, and the death investigations
    for cr in order:
        for p in cr.persons:
            rng = T.rng_for("crashkit", cr.cid, p.unit, p.pno)
            when = dt.datetime(cr.date.year, cr.date.month, cr.date.day, cr.hour, cr.minute)
            if p.is_driver and p.identified and not p.killed and p.tested and not p.arrested:
                agency = AG.PATROL_ID if cr.group == "SP" else cr.agency.aid
                site = _site(rng, cr.fips, "SP")
                kits.append(dict(arrest=None, case_type="FATAL CRASH", agency=agency, case=cr.report,
                                 coll=when + dt.timedelta(minutes=int(rng.integers(35, 150))), site=site,
                                 specimen="WB", bac=p.bac, drug_only=False, screen=rng.random() < 0.6, tube2=False,
                                 re=None, cancel=False, first=True, crash=cr))
            tested_dead = p.killed and (p.is_driver or getattr(p, "nm_tested", False))
            if tested_dead:
                off = ME_ID if cr.fips in ME_COUNTIES else CORONER_ID[cr.fips]
                site = G.ME if off == ME_ID else G.CORONERS[cr.fips]
                dday = cr.date + dt.timedelta(days=p.death_days)
                coll = dt.datetime(dday.year, dday.month, dday.day, int(rng.integers(8, 18)), int(rng.integers(0, 60)))
                if p.death_days == 0:
                    coll = max(coll, when + dt.timedelta(hours=3))
                spec = "VH" if p.test_type == "Vitreous" else "WB"
                kits.append(dict(arrest=None, case_type="DEATH INVESTIGATION", agency=off, case=None, coll=coll,
                                 site=site, specimen=spec, bac=p.bac, drug_only=False, screen=rng.random() < 0.85,
                                 tube2=False, re=None, cancel=False, first=True, crash=cr, person=p))
    # the death investigations and other criminal cases away from crashes
    for c in W.COUNTIES:
        f = c["fips"]
        rng = T.rng_for("other_cases", f)
        off = ME_ID if f in ME_COUNTIES else CORONER_ID[f]
        site = G.ME if off == ME_ID else G.CORONERS[f]
        for y in (2023, 2024, 2025):
            vy = T.knobs(f)["vmt3"] / 3.0
            for i in range(int(round(vy * 1.32 * float(rng.uniform(0.9, 1.1))))):
                d = dt.date(y, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
                coll = dt.datetime(d.year, d.month, d.day, int(rng.integers(8, 18)), int(rng.integers(0, 60)))
                bac = 0.0 if rng.random() < 0.78 else _trunc3(float(rng.uniform(0.01, 0.31)))
                kits.append(dict(arrest=None, case_type="DEATH INVESTIGATION", agency=off, case=None, coll=coll,
                                 site=site, specimen="WB" if rng.random() < 0.93 else "VH", bac=bac, drug_only=False,
                                 screen=rng.random() < 0.9, tube2=False, re=None, cancel=False, first=True))
            for i in range(int(round(vy * 0.41 * float(rng.uniform(0.9, 1.1))))):
                d = dt.date(y, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
                coll = dt.datetime(d.year, d.month, d.day, int(rng.integers(0, 24)), int(rng.integers(0, 60)))
                u = rng.random()
                a = AG.patrol_post(f) if u < 0.2 else AG.sheriff(f) if u < 0.5 else AG.city_pd(f, rng)
                agency = AG.PATROL_ID if a.kind == "State Patrol" else a.aid
                kits.append(dict(arrest=None, case_type="OTHER CRIMINAL", agency=agency,
                                 case=numbers.next(a, d, int(rng.integers(0, 3))), coll=coll,
                                 site=G.JAILS[f] if rng.random() < 0.6 else (G.HOSPITALS.get(f) or [G.JAILS[f]])[0],
                                 specimen="WB" if rng.random() < 0.7 else "UR", bac=None, drug_only=True, screen=True,
                                 tube2=False, re=None, cancel=False, first=True))
    # the extract: received from 1 January 2023 through 15 January 2026
    for k in kits:
        rng = T.rng_for("recv", k["agency"], k["case"] or "", k["coll"].isoformat())
        k["received"] = k["coll"].date() + dt.timedelta(days=int(rng.integers(1, 10)))
        k["rng"] = rng
    kits = [k for k in kits if EXTRACT_FROM <= k["received"] <= EXTRACT_TO]
    kits.sort(key=lambda k: (k["received"], k["coll"], k["agency"], k["case"] or ""))
    seq = {}
    for k in kits:
        y = k["received"].year
        seq[y] = seq.get(y, 0) + 1
        k["lab_no"] = "T%02d-%06d" % (y % 100, seq[y])
        k["utc"] = _utc(k["coll"])
    # coroner and medical examiner case numbers
    cseq = {}
    for k in kits:
        if k["case_type"] == "DEATH INVESTIGATION":
            key = (k["agency"], k["coll"].year)
            cseq[key] = cseq.get(key, 0) + 1
            k["case"] = "%s-%02d-%04d" % ("ME" if k["agency"] == ME_ID else "C" + k["agency"][2:5], k["coll"].year % 100,
                                         cseq[key])
    return kits


def rows(kits):
    out = []
    for k in kits:
        rng = k["rng"]
        rep = k["received"] + dt.timedelta(days=int(rng.integers(3, 26)))
        base = [k["lab_no"], k["case_type"], k["agency"], k["case"], k["site"].code,
                k["utc"].strftime("%Y-%m-%dT%H:%M:%SZ"), k["received"].isoformat(), k["specimen"]]
        if k["cancel"]:
            out.append(base + ["1", "ETHANOL", "", "g/100 mL", "CANCELLED", rep.isoformat()])
            continue
        if not k["drug_only"]:
            v = k["bac"] * SERUM if k["specimen"] == "SER" else k["bac"]
            res = "%.3f" % _trunc3(v)
            tubes = ["1", "2"] if k["tube2"] else ["1"]
            for t in tubes:
                if k["re"] is not None:
                    v2 = max(0.0, k["bac"] + k["re"])
                    v2 = v2 * SERUM if k["specimen"] == "SER" else v2
                    rep2 = rep + dt.timedelta(days=int(rng.integers(40, 160)))
                    out.append(base + [t, "ETHANOL", "%.3f" % _trunc3(v2), "g/100 mL", "SUPERSEDED", rep.isoformat()])
                    out.append(base + [t, "ETHANOL", res, "g/100 mL", "AMENDED", rep2.isoformat()])
                else:
                    out.append(base + [t, "ETHANOL", res, "g/100 mL", "FINAL", rep.isoformat()])
        if k["screen"]:
            pos = rng.random() < (0.46 if k["case_type"] in ("DUI", "OTHER CRIMINAL") else 0.38)
            rep3 = rep + dt.timedelta(days=int(rng.integers(5, 30)))
            out.append(base + ["1", "DRUG SCREEN", "POSITIVE" if pos else "NEGATIVE", "", "FINAL", rep3.isoformat()])
    return out
