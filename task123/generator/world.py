"""The world for task123 (architecture 3): a coastal union of comuni, its accommodation establishments, the
guest nights they really hosted from January 2025 to September 2026, and the records three systems kept of
them: the region's monthly guest-movement returns (with returns never filed and corrected resubmissions),
each comune's quarterly tourist-tax declarations, and the regional register of establishments. Everything is
drawn from one seed; nothing here is written to the pack (pack.py does that).
"""
import datetime as dt
import numpy as np

SEED = 20261123
MONTHS = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]
DIM = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
SURVEY_FROM = (2025, 7)          # the extract runs from the July 2025 returns
MIGRATION = (2026, 5)            # returns for reference months from May 2026 carry the CIN and ISO country codes
MIGRATION_DAY = dt.date(2026, 5, 4)
AS_OF = dt.date(2026, 11, 20)    # the union's planning office prepares the assembly paper
EXTRACT_DAY = dt.datetime(2026, 11, 17, 6, 0)   # the region's extract

# (key, ISTAT code, name, zone, residents 1 Jan 2025, residents 1 Jan 2026, establishments, levies tourist tax)
COMUNI = [
    ("PLV", "112001", "Porto Levarna", "town", 23861, 23794, 74, True),
    ("MCE", "112002", "Marina di Cervessa", "coast", 7306, 7280, 118, True),
    ("SEM", "112003", "Sant'Elvira a Mare", "coast", 3454, 3437, 90, True),
    ("CFE", "112004", "Capo Ferrino", "coast", 2290, 2276, 68, True),
    ("LAR", "112005", "Lido di Arzena", "coast", 7101, 7074, 74, True),
    ("TAL", "112006", "Torre Alvea", "coast", 2934, None, 53, True),
    ("SMA", "112007", "Salvina Marina", "coast", 3376, None, 61, True),
    ("CLR", "112008", "Calarossa", "coast", 3017, 3000, 57, True),
    ("ANM", "112009", "Acquanera Marina", "coast", 4482, 4461, 63, True),
    ("BSE", "112010", "Borgo Sant'Elmo", "hill", 3104, 3093, 27, True),
    ("RFE", "112011", "Roccaferrata", "hill", 1418, 1406, 18, True),
    ("MLU", "112012", "Montelusa", "hill", 2236, 2219, 22, True),
    ("CPI", "112013", "Castelpieno", "hill", 5611, 5583, 21, True),
    ("SDU", "112014", "Serra d'Ulmo", "hill", 917, 903, 13, True),
    ("PVE", "112015", "Poggio Ventoso", "hill", 1262, 1251, 16, True),
    ("CBR", "112016", "Collebruno", "inland", 7433, 7409, 11, False),
    ("SGA", "112017", "San Gaudenzio", "inland", 3318, 3297, 8, False),
    ("PFO", "112018", "Pievefosca", "inland", 1702, 1688, 9, True),
    ("FCU", "112019", "Fontecupa", "inland", 2504, 2489, 8, False),
]
MERGED = ("ASV", "112020", "Alvea Salvina", "coast")   # Torre Alvea and Salvina Marina from 1 January 2026
MERGER_PARTS = ("TAL", "SMA")
ASV_RES2026 = 6205

PROFILE = {
    "coast": [.07, .08, .11, .22, .30, .50, .62, .62, .45, .22, .07, .06],
    "town": [.36, .40, .45, .55, .58, .62, .70, .78, .64, .55, .42, .37],
    "hill": [.13, .13, .18, .30, .36, .45, .55, .58, .40, .30, .16, .18],
    "inland": [.16, .16, .20, .28, .33, .40, .48, .57, .40, .30, .18, .20],
}
TYPES = ["albergo", "campeggio", "casa vacanze", "bed and breakfast", "agriturismo", "affittacamere"]
TCODE = {"albergo": "ALB", "campeggio": "CAM", "casa vacanze": "CAV", "bed and breakfast": "BEB",
         "agriturismo": "AGR", "affittacamere": "AFF"}
TYPE_MIX = {
    "coast": [.25, .07, .24, .21, .05, .18],
    "town": [.46, .00, .14, .22, .00, .18],
    "hill": [.22, .03, .18, .24, .27, .06],
    "inland": [.18, .00, .20, .26, .30, .06],
}
ALOS = {"albergo": 3.6, "campeggio": 6.2, "casa vacanze": 6.8, "bed and breakfast": 2.4,
        "agriturismo": 3.9, "affittacamere": 2.7}
COUNTRIES = [("Germania", "Z112", "DE", .31), ("Francia", "Z110", "FR", .14), ("Regno Unito", "Z114", "GB", .11),
             ("Paesi Bassi", "Z126", "NL", .10), ("Svizzera", "Z133", "CH", .09), ("Austria", "Z102", "AT", .07)]
OTHER = ("Altri paesi esteri", "Z999", "XX", .18)
ITALIAN_SHARE = {"coast": .58, "town": .62, "hill": .55, "inland": .71}
TAX_CAT = ("alberghiero 1-3 stelle", "alberghiero 4-5 stelle", "extralberghiero")
# share of each comune's establishments that are family holiday houses filling around Ferragosto
FERRAGOSTO_SHARE = {"MCE": .40, "SEM": .26, "CFE": .62, "LAR": .62, "TAL": .30, "SMA": .30, "CLR": .28, "ANM": .50,
                    "BSE": .22, "RFE": .18, "MLU": .24, "CPI": .15, "SDU": .20, "PVE": .22, "PLV": .06}


def tax_cat(e):
    if e["typ"] == "albergo":
        return TAX_CAT[1] if e["stars"] >= 4 else TAX_CAT[0]
    return TAX_CAT[2]


def _season(rng, typ, zone):
    """(first month, last month, last day of the last month) the establishment opens each year."""
    if typ == "campeggio":
        u = rng.random()
        return (4, 10, 31) if u < .45 else ((4, 10, 15) if u < .75 else (5, 9, 30))
    if zone == "coast" and typ in ("albergo", "casa vacanze", "affittacamere") and rng.random() < .55:
        start = int(rng.choice([3, 4, 4, 5]))
        end = int(rng.choice([9, 10, 10, 11]))
        last = DIM[end]
        if end == 10 and rng.random() < .35:
            last = 15
        return (start, end, last)
    return (1, 12, 31)


def _beds(rng, typ):
    lo, hi = {"albergo": (24, 190), "campeggio": (180, 900), "casa vacanze": (4, 36), "bed and breakfast": (4, 12),
              "agriturismo": (8, 32), "affittacamere": (5, 18)}[typ]
    return int(rng.integers(lo, hi + 1))


def open_days(e, y, m):
    """Days the establishment was open and not suspended in month (y, m)."""
    if e.get("ceased") and (y, m) > (e["ceased"].year, e["ceased"].month):
        return 0
    if e.get("opened") and (y, m) < (e["opened"].year, e["opened"].month):
        return 0
    first, last, lastday = e["season"]
    if not (first <= m <= last):
        return 0
    d = lastday if m == last else DIM[m]
    if e.get("ceased") and (y, m) == (e["ceased"].year, e["ceased"].month):
        d = min(d, e["ceased"].day)
    if e.get("suspended") == (y, m):
        return 0
    return d


def beds_on(e, day):
    """Bed-places in force on a date (the register's variations apply from their effective day)."""
    b = e["beds"]
    for (when, new) in e.get("bed_changes", []):
        if day >= when:
            b = new
    return b


def bed_days(e, y, m):
    """Bed-places times open days in a month, following any change of bed-places inside it."""
    n = open_days(e, y, m)
    return sum(beds_on(e, dt.date(y, m, d)) for d in range(1, n + 1))


class World:
    pass


def build():
    rng = np.random.default_rng(SEED)
    w = World()
    w.comuni = {c[0]: dict(key=c[0], istat=c[1], name=c[2], zone=c[3], res2025=c[4], res2026=c[5], n=c[6], tax=c[7])
                for c in COMUNI}
    w.comuni[MERGED[0]] = dict(key=MERGED[0], istat=MERGED[1], name=MERGED[2], zone=MERGED[3],
                               res2025=None, res2026=ASV_RES2026, n=0, tax=True)
    est = []
    serial = 100
    for c in COMUNI:
        key, istat, name, zone, r25, r26, n, tax = c
        mix = TYPE_MIX[zone]
        for i in range(n):
            serial += int(rng.integers(1, 9))
            typ = TYPES[int(rng.choice(len(TYPES), p=np.array(mix) / sum(mix)))]
            stars = int(rng.choice([1, 2, 3, 3, 3, 4, 4, 5])) if typ == "albergo" else None
            beds = _beds(rng, typ)
            season = _season(rng, typ, zone)
            eff = float(np.exp(rng.normal(0, .22)))
            if typ == "albergo" and zone in ("coast", "town"):
                eff *= 1.05
            # the holiday houses let by the week to families fill around Ferragosto far beyond their July
            ferr = bool(rng.random() < FERRAGOSTO_SHARE.get(key, .0))
            aug = float(np.exp(rng.normal(np.log(1.65), .08))) if ferr else float(np.exp(rng.normal(np.log(.97), .07)))
            prop = float(rng.beta(2, 4))
            u_aug = float(rng.random())
            comune_now = MERGED[0] if key in MERGER_PARTS else key
            est.append(dict(idx=len(est), serial=serial, comune0=key, comune=comune_now, zone=zone, typ=typ,
                            stars=stars, beds=beds, season=season, eff=eff, aug=aug, ferr=ferr, prop=prop, u_aug=u_aug))
    # life events: closures before the migration, openings after it, a month's suspension, bed-place changes
    for j in rng.permutation(len(est))[:52]:
        e = est[j]
        if e["season"] == (1, 12, 31):
            mo = int(rng.choice([3, 4, 4]))
            e["ceased"] = dt.date(2026, mo, int(rng.choice([15, DIM[mo]])))
    newcomers = []
    for c in COMUNI:
        if c[3] in ("coast", "hill") and rng.random() < .55:
            serial += int(rng.integers(1, 9))
            typ = str(rng.choice(["casa vacanze", "bed and breakfast", "affittacamere", "albergo"]))
            newcomers.append(dict(idx=len(est) + len(newcomers), serial=serial, comune0=c[0],
                                  comune=MERGED[0] if c[0] in MERGER_PARTS else c[0], zone=c[3], typ=typ,
                                  stars=int(rng.choice([3, 4])) if typ == "albergo" else None, beds=_beds(rng, typ),
                                  season=(1, 12, 31), eff=float(np.exp(rng.normal(0, .22))),
                                  aug=float(np.exp(rng.normal(0, .27))), prop=float(rng.beta(2, 4)),
                                  u_aug=float(rng.random()), opened=dt.date(2026, int(rng.choice([5, 6])), 1)))
    est.extend(newcomers)
    steady = [e for e in est if e["season"] == (1, 12, 31) and not e.get("ceased") and not e.get("opened")]
    for j in rng.permutation(len(steady))[:17]:
        steady[j]["suspended"] = (2025, 10)
    for j in rng.permutation(len(est))[:70]:
        e = est[j]
        if e.get("opened") or e.get("ceased"):
            continue
        y, mo = [(2025, 10), (2025, 10), (2025, 12), (2026, 2), (2026, 3), (2026, 4), (2026, 5), (2026, 6)][int(rng.integers(0, 8))]
        when = dt.date(y, mo, int(rng.choice([1, 16])))
        delta = int(round(e["beds"] * float(rng.choice([-.2, .15, .2, .3, .4]))))
        e["bed_changes"] = [(when, max(2, e["beds"] + (delta if delta else 2)))]
    w.est = est
    # true nights and arrivals per establishment-month
    true = {}
    for e in est:
        prof = np.array(PROFILE[e["zone"]])
        for (y, m) in MONTHS:
            bd = bed_days(e, y, m)
            if bd == 0:
                continue
            grow = 1.0 if y == 2025 else 1.03
            occ = prof[m - 1] * e["eff"] * grow * float(np.exp(rng.normal(0, .06)))
            if m == 8:
                occ *= e["aug"]
            if e["typ"] == "campeggio":
                occ *= 1.05
            occ = min(occ, 0.985)
            nights = int(round(bd * occ))
            alos = ALOS[e["typ"]] * float(np.exp(rng.normal(0, .08))) * (1.25 if m in (7, 8) else 1.0)
            arrivals = int(max(1, round(nights / alos))) if nights > 0 else 0
            true[(e["idx"], y, m)] = dict(occ=occ, nights=nights, arrivals=arrivals, bed_days=bd)
    w.true = true
    w.res_split = {}
    for e in est:
        it_share = ITALIAN_SHARE[e["zone"]] * float(np.exp(rng.normal(0, .12)))
        base = np.array([c[3] for c in COUNTRIES] + [OTHER[3]]) * np.exp(rng.normal(0, .5, len(COUNTRIES) + 1))
        base = base / base.sum()
        for (y, m) in MONTHS:
            t = true.get((e["idx"], y, m))
            if not t or t["nights"] == 0:
                continue
            its = min(.95, it_share * (1.12 if m in (7, 8) else .92))
            parts = [its] + list((1 - its) * base)
            w.res_split[(e["idx"], y, m)] = (rng.multinomial(t["nights"], parts), rng.multinomial(t["arrivals"], parts))
    # filing behaviour
    filed, resub = {}, {}
    for e in est:
        for (y, m) in MONTHS:
            k = (e["idx"], y, m)
            t = true.get(k)
            if e.get("ceased") and (y, m) > (e["ceased"].year, e["ceased"].month):
                continue
            if e.get("opened") and (y, m) < (e["opened"].year, e["opened"].month):
                continue
            if e.get("suspended") == (y, m):
                filed[k] = "suspended"
                continue
            if t is None:
                filed[k] = "closed"
                continue
            if m == 8:
                # the houses that fill only around Ferragosto are the ones whose August return goes unfiled
                p = (.50 + .45 * e["prop"]) if e.get("ferr") else .02
                p = min(p, .9)
                draw = e["u_aug"]
            elif (y, m) in ((2025, 10), (2026, 1), (2026, 2), (2026, 3), (2026, 4), (2026, 7), (2026, 9)):
                p, draw = 0.0, 1.0
            else:
                p, draw = .008, float(rng.random())
            if not w.comuni[e["comune0"]]["tax"]:
                p, draw = 0.0, 1.0
            filed[k] = "missing" if draw < p else "filed"
            if filed[k] == "filed" and rng.random() < .03:
                resub[k] = float(rng.choice([-1, 1]) * rng.uniform(.04, .16))
    w.filed, w.resub = filed, resub
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    for e in est:
        e["cir"] = None if e.get("opened") else "%s-%05d-%s" % (w.comuni[e["comune0"]]["istat"][3:], e["serial"],
                                                               TCODE[e["typ"]])
        tail = "".join(letters[int(x)] for x in rng.integers(0, len(letters), 6))
        e["cin"] = None if e.get("ceased") else "IT%s%s%02d%s" % (w.comuni[e["comune"]]["istat"],
                                                                  "A" if e["typ"] == "albergo" else "C",
                                                                  int(rng.integers(10, 99)), tail)
    # establishments that sent their April 2026 return again after the code change, under the CIN
    w.refiled_april = set()
    for e in est:
        if e.get("cin") and e.get("cir") and filed.get((e["idx"], 2026, 4)) == "filed" and rng.random() < .13:
            w.refiled_april.add(e["idx"])
    # supplementary 2025 declarations: a later filing adding nights the first filing left out
    w.submitted = {}
    for (k, v) in sorted(filed.items()):
        if v != "filed":
            continue
        idx, y, m = k
        base = dt.datetime(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1, 8, 0)
        lag = min(int(rng.gamma(2.0, 3.0)) + (int(rng.integers(0, 40)) if rng.random() < .08 else 0), 44)
        w.submitted[k] = base + dt.timedelta(days=lag, minutes=int(rng.integers(0, 600)))
    # tourist-tax declarations: nights by quarter and category, with the exempt part
    w.decl = {}
    for (y, q) in [(2025, 1), (2025, 2), (2025, 3), (2025, 4), (2026, 1), (2026, 2), (2026, 3)]:
        for e in est:
            if not w.comuni[e["comune0"]]["tax"]:
                continue
            com = e["comune0"] if y == 2025 else e["comune"]
            tot = sum(true.get((e["idx"], y, m), {"nights": 0})["nights"] for m in range(3 * q - 2, 3 * q + 1))
            if tot == 0:
                continue
            d = w.decl.setdefault((com, y, q, tax_cat(e)), dict(total=0))
            d["total"] += tot
    for key in sorted(w.decl):
        d = w.decl[key]
        ex = (.10 if key[3] != TAX_CAT[2] else .14) + (.07 if key[2] == 3 else 0) + float(rng.uniform(-.02, .02))
        d["exempt"] = int(round(d["total"] * ex))
        d["liable"] = d["total"] - d["exempt"]
    w.decl_supp = {}
    for key in [("MCE", 2025, 3, TAX_CAT[2]), ("ANM", 2025, 2, TAX_CAT[2]), ("PLV", 2025, 4, TAX_CAT[1]),
                ("CLR", 2025, 1, TAX_CAT[0]), ("TAL", 2025, 3, TAX_CAT[2]), ("MLU", 2025, 2, TAX_CAT[2])]:
        if key in w.decl:
            d = w.decl[key]
            share = float(rng.uniform(.05, .11))
            sup_total = int(round(d["total"] * share))
            sup_ex = int(round(sup_total * d["exempt"] / d["total"]))
            w.decl_supp[key] = dict(total=sup_total, exempt=sup_ex, liable=sup_total - sup_ex)
    w.decl_amend = {}
    for key in [("MCE", 2025, 1, TAX_CAT[2]), ("SEM", 2025, 2, TAX_CAT[1]), ("LAR", 2025, 3, TAX_CAT[2]),
                ("BSE", 2025, 4, TAX_CAT[2]), ("PLV", 2026, 3, TAX_CAT[0])]:
        if key in w.decl:
            d = w.decl[key]
            first_total = int(round(d["total"] * (1.11 if key[0] != "PLV" else 0.93)))
            w.decl_amend[key] = dict(total=first_total, exempt=d["exempt"], liable=first_total - d["exempt"])
    # tourist-tax rates per liable night (euros) by comune and category, with the dates they apply from
    w.rates = []
    for key in [c[0] for c in COMUNI] + [MERGED[0]]:
        if not w.comuni[key]["tax"]:
            continue
        base = {"coast": (1.50, 2.50, 1.20), "town": (2.00, 3.00, 1.50), "hill": (1.00, 2.00, 1.00),
                "inland": (0.80, 1.50, 0.80)}[w.comuni[key]["zone"]]
        start = dt.date(2025, 1, 1) if key != "ASV" else dt.date(2026, 1, 1)
        end = dt.date(2025, 12, 31) if key in MERGER_PARTS else None
        for cat, r in zip(TAX_CAT, base):
            w.rates.append(dict(comune=key, cat=cat, rate=r, start=start, end=end))
    bumps = [("SEM", TAX_CAT[1], dt.date(2025, 7, 1), 3.00), ("CFE", TAX_CAT[2], dt.date(2025, 4, 1), 1.50),
             ("PLV", TAX_CAT[0], dt.date(2025, 10, 1), 2.50), ("SMA", TAX_CAT[0], dt.date(2025, 7, 1), 2.00)]
    for (key, cat, when, r) in bumps:
        for row in list(w.rates):
            if row["comune"] == key and row["cat"] == cat and row["start"] < when and \
                    (row["end"] is None or row["end"] >= when):
                old_end = row["end"]
                row["end"] = when - dt.timedelta(days=1)
                w.rates.append(dict(comune=key, cat=cat, rate=r, start=when, end=old_end))
                break
    w.rng_tail = int(rng.integers(0, 2 ** 31))
    return w


def survey_rows(w):
    """The region's export: one row per establishment-month-residence group, every submission kept."""
    rows = []
    for e in w.est:
        for (y, m) in MONTHS:
            if (y, m) < SURVEY_FROM:
                continue
            k = (e["idx"], y, m)
            st = w.filed.get(k)
            if st in (None, "missing", "suspended"):
                continue
            new = (y, m) >= MIGRATION
            code = e["cin"] if new else e["cir"]
            if code is None:
                continue
            if st == "closed":
                rows.append(dict(code=code, y=y, m=m, state="CHIUSA", country="", arr=0, nights=0,
                                 sub=dt.datetime(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 3, 9, 0),
                                 ver=1, k=k))
                continue
            nn, aa = w.res_split.get(k, (None, None))
            sub = w.submitted[k]
            versions = [(1, sub, 0.0)]
            if k in w.resub:
                second = min(sub + dt.timedelta(days=9, hours=3), EXTRACT_DAY - dt.timedelta(days=1, hours=5))
                versions = [(1, sub, w.resub[k]), (2, second, 0.0)]
            if (y, m) == (2026, 4) and e["idx"] in w.refiled_april:
                versions = versions + [("CIN", max(dt.datetime(2026, 5, 6, 9, 0), sub + dt.timedelta(days=20)), 0.0)]
            for ver, when, err in versions:
                use_code = code
                if ver == "CIN":
                    use_code, ver = e["cin"], 1
                    new_codes = True
                else:
                    new_codes = new
                if nn is None:
                    rows.append(dict(code=use_code, y=y, m=m, state="APERTA", country="IT" if new_codes else "ITALIA",
                                     arr=0, nights=0, sub=when, ver=ver, k=k))
                    continue
                for j in range(len(nn)):
                    n_j, a_j = int(nn[j]), int(aa[j])
                    if n_j == 0 and a_j == 0:
                        continue
                    if err:
                        n_j = int(round(n_j * (1 + err)))
                        a_j = int(round(a_j * (1 + err * .5)))
                    if j == 0:
                        ctry = "IT" if new_codes else "ITALIA"
                    else:
                        cc = (COUNTRIES + [OTHER])[j - 1]
                        ctry = cc[2] if new_codes else cc[1]
                    rows.append(dict(code=use_code, y=y, m=m, state="APERTA", country=ctry, arr=a_j, nights=n_j,
                                     sub=when, ver=ver, k=k))
    return rows


if __name__ == "__main__":
    w = build()
    r = survey_rows(w)
    print(len(w.est), "establishments,", len(r), "survey rows,", len(w.decl), "declaration cells")
