"""The county courts' criminal traffic cases as the Administrative Office of the Courts' statistical extract gives them
to the Center: every criminal traffic case a county court opened from 1 January 2025 to 28 February 2027, with its
lead charge and its disposition as recorded on 28 February 2027, and no party identifier. The impaired-driving cases
are the prosecutions of the impaired-driving arrests (lab.arrests, with the arrests of 2026 and 2027 the extract
reaches), less the arrests at fatal crashes, which are charged in the district court. A prosecution the prosecutor
dismissed and refiled under a new case number has both cases in the extract, the second opened on the day the first
was dismissed; nothing in the extract links them. Nothing here touches the census, the miles or the call."""
import datetime as dt
import math

import agencies as AG
import lab as L
import truth as T
import world as W

COLS = ["county_fips", "court", "case_number", "filed_date", "offense_date", "arresting_agency", "lead_charge_code",
        "lead_charge", "disposition", "disposition_date", "convicted_charge"]
FIRST_FILED = dt.date(2025, 1, 1)
CLOSE = W.COURT_CLOSE
DUI = {"DUI": ("MSC 42-1201(1)", "DRIVING UNDER THE INFLUENCE"),
       "DUI15": ("MSC 42-1201(2)", "DRIVING UNDER THE INFLUENCE, BAC .15 OR MORE"),
       "DUID": ("MSC 42-1201(3)", "DRIVING UNDER THE INFLUENCE OF DRUGS")}
DUI_CODES = {v[0] for v in DUI.values()}
OTHER = (("MSC 42-1310", "DRIVING WHILE LICENSE SUSPENDED", 0.37), ("MSC 42-1406", "NO PROOF OF INSURANCE", 0.22),
         ("MSC 42-1205", "RECKLESS DRIVING", 0.13), ("MSC 42-1312", "DRIVING WHILE LICENSE REVOKED", 0.12),
         ("MSC 42-1320", "LEAVING THE SCENE OF A CRASH", 0.09), ("MSC 42-1112", "FLEEING OR ELUDING AN OFFICER", 0.04),
         ("MSC 42-1218", "OPEN CONTAINER IN A MOTOR VEHICLE", 0.03))
RECKLESS = ("MSC 42-1205", "RECKLESS DRIVING")
GUILTY = ("GUILTY PLEA", "GUILTY VERDICT")
AMENDED = "GUILTY PLEA, AMENDED CHARGE"
OUTCOMES_DUI = (("GUILTY PLEA", 0.60), ("GUILTY VERDICT", 0.04), (AMENDED, 0.14), ("DEFERRED PROSECUTION", 0.07),
                ("DISMISSED", 0.13), ("NOT GUILTY", 0.02))
OUTCOMES_OTHER = (("GUILTY PLEA", 0.64), ("GUILTY VERDICT", 0.02), (AMENDED, 0.04), ("DEFERRED PROSECUTION", 0.06),
                  ("DISMISSED", 0.23), ("NOT GUILTY", 0.01))
REFILE_DUI = 0.08
REFILE_OTHER = 0.025


def court_name(fips):
    return "%s County Court" % W.NAMES[fips]


def agency_name(a):
    return "State Patrol" if a.kind == "State Patrol" else a.name


class Case:
    __slots__ = ("pid", "fips", "agency", "offense", "filed", "code", "charge", "counts", "disp", "dd", "conv", "number",
                 "dui", "refile_of")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def _pick(rng, table):
    u = rng.random() * sum(w for _, w in table)
    for v, w in table:
        u -= w
        if u < 0:
            return v
    return table[-1][0]


def _pending(rng, age, dui):
    p = (0.62 if age < 90 else 0.30 if age < 200 else 0.10 if age < 400 else 0.03) if dui else \
        (0.45 if age < 60 else 0.12 if age < 180 else 0.02)
    return rng.random() < p


def _disposed(rng, filed, dui):
    age = (CLOSE - filed).days
    if _pending(rng, age, dui):
        return None, None
    disp = _pick(rng, OUTCOMES_DUI if dui else OUTCOMES_OTHER)
    dd = filed + dt.timedelta(days=int(rng.integers(21, max(22, min(age, 420) + 1))))
    return disp, min(dd, CLOSE)


def _conv(disp, code, charge, dui):
    if disp in GUILTY:
        return code, charge
    if disp == AMENDED:
        return RECKLESS if dui else ("MSC 42-1406", "NO PROOF OF INSURANCE")
    return "", ""


def _court_arrests(vmt):
    """The impaired-driving arrests of 13 January 2026 to 27 February 2027, which the laboratory's arrests do not
    reach: the same agencies and the same weekly pattern."""
    out = []
    d0, d1 = dt.date(2026, 1, 13), dt.date(2027, 2, 27)
    for c in W.COUNTIES:
        f = c["fips"]
        k = T.knobs(f)
        rng = T.rng_for("court_arrests", f)
        per_day = L.ARREST_RATE[f] * vmt[f] / 3.0 / 1e8 * 1.07 / 365.0
        d = d0
        while d <= d1:
            wk = 1.6 if d.weekday() in (4, 5) else (1.15 if d.weekday() == 6 else 0.8)
            n = int(rng.poisson(per_day * wk / 1.0786))
            for _ in range(n):
                when = dt.datetime(d.year, d.month, d.day, int(rng.integers(0, 24)), int(rng.integers(0, 60)))
                out.append(L._one(rng, f, k, when))
            d += dt.timedelta(days=1)
    return out


def _other_cases(vmt):
    """Every other criminal traffic charge the county courts opened: suspended and revoked licences, no insurance,
    reckless driving, leaving the scene, eluding, open containers."""
    out = []
    d0, d1 = dt.date(2024, 11, 15), dt.date(2027, 2, 26)
    for c in W.COUNTIES:
        f = c["fips"]
        k = T.knobs(f)
        rng = T.rng_for("court_other", f)
        per_day = 2.05 * L.ARREST_RATE[f] * vmt[f] / 3.0 / 1e8 / 365.0
        d = d0
        while d <= d1:
            for _ in range(int(rng.poisson(per_day))):
                u = rng.random()
                a = AG.patrol_post(f) if u < 0.10 + 0.55 * k["sp"] else AG.sheriff(f) if u < 0.10 + 0.55 * k["sp"] + \
                    0.80 * k["so"] else AG.city_pd(f, rng)
                code, charge = _pick(rng, tuple(((cd, ch), w) for cd, ch, w in OTHER))
                lag = int(min(90, max(1, rng.lognormal(math.log(9), 0.6))))
                filed = d + dt.timedelta(days=lag)
                if FIRST_FILED <= filed <= CLOSE:
                    disp, dd = _disposed(rng, filed, False)
                    out.append(Case(pid=("O", f, len(out)), fips=f, agency=agency_name(a), offense=d, filed=filed,
                                    code=code, charge=charge, counts=1 + int(rng.random() < 0.25), disp=disp, dd=dd,
                                    dui=False))
                    _maybe_refile(rng, out, REFILE_OTHER)
            d += dt.timedelta(days=1)
    return out


def _maybe_refile(rng, out, p):
    """A prosecution dismissed and refiled under a new case number, the new case opened on the day of the dismissal."""
    a = out[-1]
    if a.disp in ("DISMISSED", "NOT GUILTY") or rng.random() >= p:
        a.conv = _conv(a.disp, a.code, a.charge, a.dui)
        return
    d = a.filed + dt.timedelta(days=int(rng.integers(14, 151)))
    if d > CLOSE - dt.timedelta(days=2):
        a.conv = _conv(a.disp, a.code, a.charge, a.dui)
        return
    outcome = a.disp
    code, charge = a.code, a.charge
    if a.dui and code == DUI["DUI"][0]:
        rng.random()                # the refile keeps the dismissed case's lead charge (the draw kept, so nothing else moves)
    age = (CLOSE - d).days
    if outcome is None or _pending(rng, age, a.dui):
        disp, dd = None, None
    else:
        disp = outcome
        dd = min(CLOSE, d + dt.timedelta(days=int(rng.integers(21, max(22, min(age, 300) + 1)))))
    a.disp, a.dd, a.conv = "DISMISSED", d, ("", "")
    b = Case(pid=a.pid, fips=a.fips, agency=a.agency, offense=a.offense, filed=d, code=code, charge=charge,
             counts=a.counts, disp=disp, dd=dd, dui=a.dui, refile_of=a)
    b.conv = _conv(disp, code, charge, a.dui)
    out.append(b)


def cases(arrests, vmt):
    """Every case in the extract, in filing order within each court, with its case number."""
    out = []
    for i, a in enumerate(list(arrests) + _court_arrests(vmt)):
        if a.kind != "DUI" or a.crash is not None:
            continue
        rng = T.rng_for("court", a.agency.aid, a.when.isoformat(), a.fips, i)
        if rng.random() < 0.07:
            continue                                            # declined by the prosecutor
        lag = int(min(120, max(2, rng.lognormal(math.log(18), 0.55))))
        filed = a.when.date() + dt.timedelta(days=lag)
        if not (FIRST_FILED <= filed <= CLOSE):
            continue
        key = "DUID" if a.drug_only else ("DUI15" if a.bac >= 0.150 and rng.random() < 0.75 else "DUI")
        code, charge = DUI[key]
        disp, dd = _disposed(rng, filed, True)
        out.append(Case(pid=("D", i), fips=a.fips, agency=agency_name(a.agency),
                        offense=a.when.date(), filed=filed, code=code, charge=charge,
                        counts=1 + int(rng.random() < 0.45) + int(rng.random() < 0.12), disp=disp, dd=dd, dui=True))
        _maybe_refile(rng, out, REFILE_DUI)
    out += _other_cases(vmt)
    _no_coincidence(out)
    _one_dismissal(out)
    _no_later_filing(out)
    _no_coincidence(out)
    _number(out)
    place_shares(out)
    return out


def _no_coincidence(out, slack=3):
    """No impaired-driving case opens within a few days of the day another impaired-driving prosecution of its court
    and offense date was dismissed, except the refile of that very prosecution, opened on the day: the relation between the two cases holds only where
    they are one, whether or not a reader also matches the arresting agency or allows a few days. A plain case is moved
    past the window; where the case is a refile, the other prosecution's dismissal is moved instead."""
    refile = {id(c.refile_of): c for c in out if c.refile_of is not None}
    window = dt.timedelta(days=slack)
    for _ in range(40):
        cells = {}
        for c in out:
            if c.dui:
                cells.setdefault((c.fips, c.offense), []).append(c)
        moved = 0
        for g in cells.values():
            for x in [c for c in g if c.disp == "DISMISSED"]:
                for c in g:
                    if c.pid == x.pid or abs(c.filed - x.dd) > window:
                        continue
                    if c.refile_of is None and c.filed <= CLOSE - window - dt.timedelta(days=2):
                        c.filed = x.dd + window + dt.timedelta(days=1)
                        if c.dd is not None and c.dd < c.filed + dt.timedelta(days=21):
                            c.dd = min(CLOSE, c.filed + dt.timedelta(days=21))
                        if c.disp == "DISMISSED" and id(c) in refile:
                            refile[id(c)].filed = c.dd
                    else:
                        later = c.filed + window + dt.timedelta(days=1)
                        x.dd = later if later <= CLOSE - dt.timedelta(days=2) else c.filed - window - \
                            dt.timedelta(days=1)
                        assert x.dd > x.filed, (x.pid, x.filed, x.dd)
                        if id(x) in refile:
                            refile[id(x)].filed = x.dd
                    moved += 1
        if not moved:
            return
    raise AssertionError("coincident dismissals and filings remain")


def _one_dismissal(out):
    """At most one dismissal among the impaired-driving prosecutions of a court and offense date of 2025 (co-arrested
    drivers are seldom both dismissed): a further refiled prosecution keeps one case, the refile's outcome on the
    first case, and a further plain dismissal is a deferred prosecution, so no dismissal of the cell precedes another
    prosecution's refile."""
    cells = {}
    for c in out:
        if c.dui and c.offense.year == 2025 and c.refile_of is None:
            cells.setdefault((c.fips, c.offense), []).append(c)
    refile = {id(c.refile_of): c for c in out if c.refile_of is not None}
    drop = set()
    for g in cells.values():
        ds = sorted((c for c in g if c.disp == "DISMISSED"), key=lambda c: (c.filed, c.pid))
        for x in ds[1:]:
            b = refile.get(id(x))
            if b is not None:
                x.disp, x.dd, x.conv = b.disp, b.dd, b.conv
                drop.add(id(b))
            else:
                x.disp = "DEFERRED PROSECUTION"
                x.conv = _conv(x.disp, x.code, x.charge, x.dui)
    out[:] = [c for c in out if id(c) not in drop]


def _no_later_filing(out, slack=3):
    """No impaired-driving case of a court and offense date is filed after, or within a few days before, the day another
    prosecution of that court and offense date was dismissed, except the dismissal's own refile, opened on the day: so a
    reader who links a dismissal to any later case of its court and offense date, with or without the arresting agency
    or a few days' slack, links exactly the refiles. A later case is moved to before the dismissal where its offense
    allows; otherwise the dismissal (and its refile's opening) moves past the later case."""
    refile = {id(c.refile_of): c for c in out if c.refile_of is not None}
    gap = dt.timedelta(days=slack + 1)
    for _ in range(60):
        cells = {}
        for c in out:
            if c.dui and c.offense.year == 2025:                # the offenses the guidelines' baselines count
                cells.setdefault((c.fips, c.offense), []).append(c)
        moved = 0
        for g in cells.values():
            for x in [c for c in g if c.disp == "DISMISSED"]:
                for c in g:
                    if c is x or c is refile.get(id(x)) or c.filed < x.dd - dt.timedelta(days=slack):
                        continue
                    early = x.dd - gap
                    if c.refile_of is None and early >= c.offense + dt.timedelta(days=2) and early >= FIRST_FILED:
                        c.filed = early
                    else:
                        later = c.filed + gap
                        assert later <= CLOSE - dt.timedelta(days=2), (x.pid, c.pid, c.filed)
                        x.dd = later
                        if id(x) in refile:
                            b = refile[id(x)]
                            b.filed = later
                            if b.dd is not None and b.dd < b.filed + dt.timedelta(days=21):
                                b.dd = min(CLOSE, b.filed + dt.timedelta(days=21))
                    moved += 1
        if not moved:
            return
    raise AssertionError("dismissals followed by later filings of their court and offense date remain")


def place_shares(cs, need=0.012):
    """Each county's per cent convicted away from the edge of its one-decimal cell: the fewest single-case 2025
    prosecutions still open at the close are read as convicted, or convicted ones as still open."""
    def edge(v):
        return 0.05 - abs(v - round(v / 0.1) * 0.1)
    for c0 in W.COUNTIES:
        f = c0["fips"]
        n, pct = ask(cs)[f]
        if edge(pct) >= need:
            continue
        h = round(pct * n / 100.0)
        pros = {}
        for c in cs:
            if c.dui and c.fips == f and c.offense.year == 2025:
                pros.setdefault(c.pid, []).append(c)
        single = [g[0] for g in pros.values() if len(g) == 1 and g[0].refile_of is None]
        up = sorted([c for c in single if c.disp is None and (CLOSE - c.filed).days > 30],
                    key=lambda c: T.rng_for("courtbin", c.number).random())
        down = sorted([c for c in single if c.disp in GUILTY and c.conv[0] in DUI_CODES],
                      key=lambda c: T.rng_for("courtbin", c.number).random())
        for k in (1, -1, 2, -2, 3, -3):
            if edge(100.0 * (h + k) / n) >= need:
                break
        for c in (up[:k] if k > 0 else down[:-k]):
            if k > 0:
                c.disp, c.dd = "GUILTY PLEA", min(CLOSE, c.filed + dt.timedelta(days=30))
            else:
                c.disp, c.dd = None, None
            c.conv = _conv(c.disp, c.code, c.charge, True)
        assert edge(ask(cs)[f][1]) >= need, (f, ask(cs)[f])


def _number(out):
    out.sort(key=lambda c: (c.fips, c.filed, c.offense, c.agency, c.code, c.pid[0], str(c.pid[1:]),
                            c.refile_of is not None))
    seq = {}
    for c in out:
        k = (c.fips, c.filed.year)
        seq[k] = seq.get(k, 0) + 1
        c.number = "CT-%02d-%05d" % (c.filed.year % 100, seq[k])


def rows(cs):
    out = []
    for c in sorted(cs, key=lambda c: (c.fips, c.filed, c.number)):
        out.append([c.fips, court_name(c.fips), c.number, c.filed.isoformat(), c.offense.isoformat(), c.agency, c.code,
                    c.charge, c.disp or "", c.dd.isoformat() if c.dd else "", c.conv[1] if c.conv else ""])
    return out


def ask(cs, year=2025):
    """Each county's impaired-driving prosecutions of the year's offenses, one for each person charged and offense (a
    refiled prosecution once), and the per cent of them that had ended in an impaired-driving conviction by the close:
    the prosecution's last case convicted on an impaired-driving charge. From the generator's own state."""
    pros = {}
    for c in cs:
        if c.dui and c.offense.year == year:
            pros.setdefault(c.pid, []).append(c)
    out = {cc["fips"]: [0, 0] for cc in W.COUNTIES}
    for pid, g in pros.items():
        last = max(g, key=lambda c: c.filed)
        out[g[0].fips][0] += 1
        out[g[0].fips][1] += last.disp in GUILTY and last.conv[0] in DUI_CODES
    return {f: (n, 100.0 * h / n) for f, (n, h) in out.items()}
