"""The clinical faculty, their industry relationships and how they report them, drawn forward from the world's facts.

Every faculty member has a tenure, a department history (appointment terms, the Department of Medicine's divisions
becoming departments on 1 July 2025), an NPI and one or two Open Payments profiles. Faculty with industry work hold
relationships with manufacturers (or companies outside Open Payments) that start, run for a few years and end. Each
relationship pays on its own calendar: consulting retainers in quarterly or monthly installments, advisory boards some
weeks after their meetings, speaker programs and other services per event; every payment carries its date.

Each faculty member reports with their own habits: a share of small relationships left out (recipiency error), the
amounts of the relationships named understated by a personal factor, now and then a partial report (amount error), and
a habit of filing in December, once the system opens, or in January before the deadline. A version of a disclosure
reports what each company had paid by the day it is submitted.

The docket region (docket_region) is drawn the same way from plans fixed by kind; each member's draws are kept only when
they land where the design needs them (a seed search over the member's own stream), never edited afterwards."""
import calendar
import datetime as dt

import numpy as np

import world as W

D = dt.date
UTC = dt.timezone.utc
EASTERN = dt.timezone(dt.timedelta(hours=-5))          # December and January are standard time
DEADLINE_UTC = W.DEADLINE_LOCAL.replace(tzinfo=EASTERN).astimezone(UTC)
CAP = 22000.0
PPART = 0.06
INDUSTRY = {"CARD": 0.46, "ORTH": 0.50, "HEON": 0.40, "NEUR": 0.36, "GAST": 0.42, "DERM": 0.40, "OPHT": 0.36,
            "UROL": 0.42, "PSYC": 0.26, "IMED": 0.15, "ANES": 0.10, "EMED": 0.08, "OBGY": 0.13, "PEDS": 0.07,
            "RADI": 0.12, "SURG": 0.21}
CONTACT = {"CARD": 0.85, "ORTH": 0.85, "HEON": 0.8, "NEUR": 0.75, "GAST": 0.8, "DERM": 0.75, "OPHT": 0.7,
           "UROL": 0.8, "PSYC": 0.65, "IMED": 0.6, "ANES": 0.35, "EMED": 0.3, "OBGY": 0.5, "PEDS": 0.35, "RADI": 0.3,
           "SURG": 0.6}
KINDS = ["consulting", "speaking", "advisory", "honoraria", "other"]
KIND_P = [0.34, 0.36, 0.14, 0.12, 0.04]
PAY_SIZE = {"consulting": 2600.0, "speaking": 2300.0, "advisory": 3200.0, "honoraria": 1800.0, "other": 2500.0,
            "expert": 3000.0}


class Faculty:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def holds(self, day):
        """An appointment on this day (start and end inclusive)."""
        return self.start <= day and (self.end is None or day <= self.end)

    def owes(self, year):
        return self.holds(D(year, 12, 31))


def _ratio(f, r):
    """One reported amount over the amount received: the faculty member's habit, now and then a partial report."""
    if r.random() < f.ppart:
        return float(r.uniform(0.2, 0.7)) * float(np.exp(f.mu))
    return min(1.12, float(np.exp(f.mu + r.normal(0, 0.10))))


def _omit_p(f, amount):
    return min(0.95, f.o * 2.0 / (1.0 + amount / 4000.0))


def _round(f, x):
    step = f.rounding
    return max(step, round(x / step) * step)


# ---------------------------------------------------------------------------------------------- payment calendars
def _business(d):
    """A scheduled payment that falls on a weekend goes out the Friday before."""
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def _equal(total, k):
    cents = int(round(total * 100))
    out = [cents // k] * k
    out[-1] += cents - sum(out)
    return [c / 100.0 for c in out]


def _split(r, total, k):
    """k positive amounts in cents summing to total."""
    w = r.gamma(6.0, 1.0, size=k)
    cents = np.floor(w / w.sum() * round(total * 100)).astype(int)
    cents[-1] += int(round(total * 100)) - int(cents.sum())
    if cents.min() <= 0:
        cents = np.full(k, int(round(total * 100)) // k)
        cents[-1] += int(round(total * 100)) - int(cents.sum())
    return [int(c) / 100.0 for c in cents]


def schedule_for(kind, r):
    if kind == "consulting":
        u = r.random()
        return "quarterly" if u < 0.55 else ("monthly" if u < 0.72 else "events")
    if kind == "advisory":
        return "meetings"
    return "events"


def start_fraction(rel):
    """The share of a full year a relationship's first year covers."""
    if rel["schedule"] == "quarterly":
        return (5 - rel["start_q"]) / 4.0
    return (13 - rel["start_m"]) / 12.0


def payments(rel, y, a, r):
    """The payments a relationship makes in year y, summing to a: [(date, amount)] in date order."""
    s = rel["schedule"]
    first = y == min(rel["years"])
    if s == "quarterly":
        q0 = rel["start_q"] if first else 1
        days = [_business(D(y, 3 * q, 15)) for q in range(q0, 5)]
        return list(zip(days, _equal(a, len(days))))
    if s == "monthly":
        m0 = rel["start_m"] if first else 1
        days = [_business(D(y, m, calendar.monthrange(y, m)[1])) for m in range(m0, 13)]
        return list(zip(days, _equal(a, len(days))))
    m0 = rel["start_m"] if first else 1
    if s == "meetings":
        k = int(r.integers(1, 4))
        months = sorted(int(x) for x in r.choice(np.arange(max(3, m0), 12), size=min(k, 12 - max(3, m0)), replace=False))
        days = sorted(_business(min(D(y, 12, 21), D(y, m, int(r.integers(1, 26))) + dt.timedelta(days=int(r.integers(12, 30)))))
                      for m in months)
        return list(zip(days, _split(r, a, len(days))))
    k = max(1, min(14, int(round(a / PAY_SIZE[rel["kind"]] * float(np.exp(r.normal(0, 0.25)))))))
    lo, hi = D(y, m0, 1).toordinal(), D(y, 12, 31).toordinal()
    days = sorted(D.fromordinal(int(x)) for x in r.integers(lo, hi + 1, size=k))
    return list(zip(days, _split(r, a, k)))


def new_relationship(mfr, kind, r, company=None, schedule=None, start=1):
    rel = {"mfr": mfr, "kind": kind, "years": {}, "pay": {}, "schedule": schedule or schedule_for(kind, r)}
    if company:
        rel["company"] = company
    rel["start_q"] = start if rel["schedule"] == "quarterly" else 1
    rel["start_m"] = start if rel["schedule"] != "quarterly" else 1
    return rel


def pay_out(rel, r):
    for y in sorted(rel["years"]):
        rel["pay"][y] = payments(rel, y, rel["years"][y], r)


# ------------------------------------------------------------------------------------------------- filing times
def _t(day, r):
    hh = int(r.choice([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]))
    return dt.datetime(day.year, day.month, day.day, hh, int(r.integers(0, 60)), int(r.integers(0, 60)),
                       tzinfo=EASTERN).astimezone(UTC)


def filing_time(r, y, habit, last_day=31):
    """The first submission of the disclosure for year y (UTC), by habit: "dec" (in December, the system open since the
    1st), "jan" (in January before the deadline), "evening" (the deadline's last hours), "late" (after the deadline)."""
    dl = DEADLINE_UTC.replace(year=y + 1)
    if habit == "dec":
        day = D(y, 12, 1 + int(min(last_day - 1, np.floor(r.beta(1.2, 2.6) * last_day))))
        return _t(day, r)
    if habit == "jan":
        t = _t(D(y + 1, 1, int(r.integers(2, 16))), r)
        return min(t, dl - dt.timedelta(seconds=int(r.integers(5 * 3600, 30 * 3600))))
    if habit == "evening":
        return dl - dt.timedelta(seconds=int(r.integers(60, 5 * 3600)))
    if habit == "late":
        return dl + dt.timedelta(seconds=int(r.integers(30 * 60, 5 * 24 * 3600)))
    raise ValueError(habit)


def eastern_day(t):
    return t.astimezone(EASTERN).date()


def received(rel, y, t):
    """What the relationship had paid in year y by the Eastern date of t (all of it once the year is over)."""
    pay = rel["pay"].get(y, [])
    day = eastern_day(t)
    if day.year > y:
        return sum(a for _, a in pay)
    return sum(a for d, a in pay if d <= day)


def key_of(rel):
    return rel["mfr"] if rel["mfr"] is not None else rel["company"]


def lines_at(f, y, t):
    """{manufacturer id or company: amount} the faculty member enters for year y in a version submitted at t."""
    out = {}
    for rel in f.rels:
        if y not in rel["years"]:
            continue
        k = key_of(rel)
        if (k, y) not in f.draw:
            continue
        omit, ratio = f.draw[(k, y)]
        got = received(rel, y, t)
        if omit or got <= 0:
            continue
        out[k] = out.get(k, 0.0) + _round(f, got * ratio)
    return out


def _draws(f, r):
    """Each relationship-year's omission and reporting factor, drawn once and kept by every version."""
    f.draw = {}
    for rel in f.rels:
        k = key_of(rel)
        for y, a in sorted(rel["years"].items()):
            if not f.owes(y):
                continue
            force = rel.get("force")
            omit = False if force is True else bool(r.random() < _omit_p(f, a))
            ratio = _ratio(f, r)
            if rel.get("partial") == y:
                ratio = float(r.uniform(0.16, 0.26))
            f.draw[(k, y)] = (omit, ratio)


def first_lines(f):
    f.lines = {}
    for y, t in f.filing.items():
        if t is None:
            continue
        for k, d in lines_at(f, y, t).items():
            f.lines[(k, y)] = d


# ---------------------------------------------------------------------------------------------------------- roster
def _tenure(r, initial):
    if initial:
        start = D(int(r.integers(1994, 2021)), int(r.choice([7, 7, 7, 9, 1, 8])), 1)
        if start > D(2020, 12, 31):
            start = D(2020, 7, 1)
    else:
        year = int(r.choice(W.YEARS + [2027], p=[0.155, 0.16, 0.16, 0.165, 0.165, 0.165, 0.03]))
        if year == 2027:
            start = D(2027, 1, int(r.choice([4, 11, 18])))
        else:
            m = int(r.choice([7, 7, 7, 8, 9, 1, 10, 3]))
            start = D(year, m, 1)
    end = None
    y = max(2021, start.year)
    while y <= 2026:
        if r.random() < 0.052:
            m = int(r.choice([6, 6, 6, 12, 8, 3, 9]))
            last = {6: 30, 12: 31, 8: 31, 3: 31, 9: 30}[m]
            cand = D(y, m, last)
            if cand > start:
                end = cand
                break
        y += 1
    return start, end


def _terms(f, r):
    """Appointment terms: assistant professors and instructors renew each 1 July, associate professors and
    professors hold three-year terms. A term open across 1 July 2025 keeps the code it was issued with."""
    rows = []
    annual = f.rank in ("Instructor", "Assistant Professor")
    s = f.start
    while True:
        if annual:
            nxt = D(s.year + (1 if s.month >= 7 else 0), 7, 1)
        else:
            base = D(s.year + (1 if s.month >= 7 else 0), 7, 1)
            nxt = D(base.year + 2, 7, 1)
        e = nxt - dt.timedelta(days=1)
        if f.end is not None and f.end <= e:
            e = f.end
        rows.append((s, e))
        if (f.end is not None and e >= f.end) or s > D(2027, 6, 30):
            break
        if e >= D(2027, 6, 30):
            break
        s = e + dt.timedelta(days=1)
    out = []
    for s, e in rows:
        if e < D(2019, 7, 1):
            continue
        if f.dept in W.SUCCESSOR_OF and s < W.REORG:
            code, div = W.MED[0], W.SUCCESSOR_OF[f.dept]
        else:
            code, div = f.dept, ""
        out.append({"dept": code, "division": div, "start": s, "end": e, "primary": True})
    return out


def roster():
    r = np.random.default_rng([W.SEED, 2])
    ff, fm, ll = W.first_last_pools()
    depts = [c for c, _, _ in W.DEPTS]
    share = np.array([s for _, _, s in W.DEPTS])
    share = share / share.sum()
    fac = []
    used_names, used_npi = set(), set()
    emp = 4180000
    n_initial, n_hires = 1530, 640
    for k in range(n_initial + n_hires):
        initial = k < n_initial
        start, end = _tenure(r, initial)
        dept = depts[r.choice(len(depts), p=share)]
        cred = "MD" if r.random() < 0.80 else ("DO" if r.random() < 0.35 else ("NP" if r.random() < 0.55 else "PA"))
        female = r.random() < 0.47
        while True:
            first = (ff if female else fm)[int(r.integers(len(ff if female else fm)))]
            last = ll[int(r.integers(len(ll)))]
            if (first, last) not in used_names:
                break
        used_names.add((first, last))
        while True:
            n = W.npi(r)
            if n not in used_npi:
                break
        used_npi.add(n)
        emp += int(r.integers(3, 40))
        rank = str(r.choice(["Instructor", "Assistant Professor", "Assistant Professor", "Associate Professor",
                             "Professor"])) if cred in ("MD", "DO") else "Instructor"
        f = Faculty(emp_id="%07d" % emp, first=first, middle=str(r.choice(list("ABCDEFGHJKLMNPRSTW"))) if r.random() < 0.7 else "",
                    last=last, cred=cred, npi=n, dept=dept, rank=rank, start=start, end=end, group="bg", hire_block=not initial)
        f.terms = _terms(f, r)
        if r.random() < 0.06 and cred in ("MD", "DO"):
            other = depts[r.choice(len(depts), p=share)]
            if other != dept and other not in W.SUCCESSOR_OF and dept not in W.SUCCESSOR_OF:
                f.terms += [dict(t, dept=other, division="", primary=False) for t in f.terms]
        fac.append(f)
    return fac


# ---------------------------------------------------------------------------------------------- relationships
def _habits(f, r):
    f.mu = float(r.normal(np.log(0.96), 0.05) if r.random() < 0.7 else r.normal(np.log(0.60), 0.15))
    f.o = 0.04 if r.random() < 0.65 else 0.35
    f.ppart = PPART
    f.rounding = float(r.choice([100.0, 100.0, 100.0, 500.0, 1000.0]))


def _mfr_for(dept, mfrs, r):
    mfrs = [m for m in mfrs if not m.get("now_reporting")]
    pool = [m for m in mfrs if dept in m["depts"]] or mfrs
    if r.random() < 0.3:
        pool = mfrs
    return pool[int(r.integers(len(pool)))]


def relationships(fac, mfrs):
    """Background relationships: arrivals each year, continuing with probability 0.55, amounts drawn per
    relationship and varied by year, the first year covering the months after it starts; a few faculty also work for
    companies outside Open Payments."""
    for f in fac:
        r = np.random.default_rng([W.SEED, 3, int(f.emp_id)])
        rp = np.random.default_rng([W.SEED, 8, int(f.emp_id)])
        _habits(f, r)
        f.rels = []
        f.contact = r.random() < CONTACT[f.dept] * (0.4 if f.cred in ("NP", "PA") else 1.0)
        active = r.random() < INDUSTRY[f.dept] * (0.3 if f.cred in ("NP", "PA") else 1.0)
        if not active:
            continue
        lam = float(np.exp(r.normal(np.log(0.9), 0.9)))
        size = float(np.exp(r.normal(np.log(2600), 0.7)))

        live = []
        for y in W.YEARS:
            live = [x for x in live if r.random() < 0.55]
            for _ in range(int(r.poisson(lam))):
                while True:
                    a = size * float(np.exp(r.normal(0, 0.9)))
                    if 400 < a < CAP:
                        break
                held = {x["mfr"] for x in f.rels}
                m = _mfr_for(f.dept, mfrs, r)
                for _try in range(20):
                    if m["id"] not in held:
                        break
                    m = _mfr_for(f.dept, mfrs, r)
                if m["id"] in held:
                    continue
                kind = str(r.choice(KINDS, p=KIND_P))
                rel = new_relationship(m["id"], kind, rp)
                rel["start_q"] = int(rp.integers(1, 5)) if y > 2021 else 1
                rel["start_m"] = int(rp.integers(1, 12)) if y > 2021 else 1
                rel["base"] = a
                f.rels.append(rel)
                live.append(rel)
            for rel in live:
                amt = min(CAP, rel["base"] * float(np.exp(r.normal(0, 0.2))))
                if not rel["years"]:
                    amt = max(300.0, amt * start_fraction(rel))
                rel["years"][y] = amt
        if r.random() < 0.12:
            name, kind = W.NONREPORTING[int(r.integers(len(W.NONREPORTING)))]
            y0 = int(r.choice(W.YEARS))
            rel = new_relationship(None, kind, rp, company=name)
            rel["base"] = float(np.exp(r.normal(np.log(6000), 0.8)))
            for y in range(y0, min(2026, y0 + int(r.integers(1, 4))) + 1):
                rel["years"][y] = min(42000.0, rel["base"] * float(np.exp(r.normal(0, 0.2))))
            f.rels.append(rel)
        for rel in f.rels:
            pay_out(rel, rp)


def _filing_habits(f, r):
    f.p_dec = 0.62 if r.random() < 0.32 else 0.12
    f.evening = r.random() < 0.09
    f.lateish = r.random() < 0.07


def filing_plan(fac):
    """Each background faculty member's first submission for each year they owed a disclosure (None: not filed by the
    pull of 21 January 2027)."""
    for f in fac:
        if f.group != "bg":
            continue
        r = np.random.default_rng([W.SEED, 9, int(f.emp_id)])
        _filing_habits(f, r)
        f.filing = {}
        for y in W.YEARS:
            if not f.owes(y):
                continue
            if y == 2026 and r.random() < 0.024:
                f.filing[y] = None
                continue
            u = r.random()
            if f.lateish and u < 0.6:
                habit = "late"
            elif r.random() < f.p_dec:
                habit = "dec"
            elif f.evening and r.random() < 0.7:
                habit = "evening"
            else:
                habit = "jan"
            f.filing[y] = filing_time(r, y, habit)


def disclose_all(fac):
    for f in fac:
        if f.group != "bg":
            continue
        r = np.random.default_rng([W.SEED, 4, int(f.emp_id)])
        _draws(f, r)
        first_lines(f)


def device_relationships(fac, mfrs):
    """Expert testimony and other services for renamed manufacturers in 2026: product litigation the faculty member is
    retained in, paid per event."""
    r = np.random.default_rng([W.SEED, 6])
    renamed = [m for m in mfrs if m["index"] in W.RENAMED]
    pool = [f for f in fac if f.rels and f.owes(2026) and f.owes(2025) and f.cred in ("MD", "DO")
            and f.filing.get(2026) is not None]
    for j, k in enumerate(r.choice(len(pool), size=6, replace=False)):
        f = pool[int(k)]
        held = {x["mfr"] for x in f.rels}
        options = [m for m in renamed if m["id"] not in held] or renamed
        m = options[int(r.integers(len(options)))]
        kind = "expert" if j < 4 else "other"
        rel = new_relationship(m["id"], kind, r, schedule="events")
        rel["typed_former"] = True
        rel["years"][2026] = float(r.uniform(4500, 11000))
        if r.random() < 0.5:
            rel["years"][2025] = rel["years"][2026] * float(r.uniform(0.5, 1.0))
        pay_out(rel, r)
        f.rels.append(rel)
        rr = np.random.default_rng([W.SEED, 4, int(f.emp_id), 1])
        for y in rel["years"]:
            if f.owes(y):
                f.draw[(m["id"], y)] = (False, _ratio(f, rr))
        first_lines(f)


def now_reporting_relationships(fac, mfrs):
    """2026 relationships with the companies that began reporting to Open Payments for 2025 (world.NOW_REPORTING):
    launch-year consulting, speaker programs, expert work and other services, each faculty member also paid by a
    larger manufacturer in 2026."""
    r = np.random.default_rng([W.SEED, 10])
    byname = {m["name"]: m for m in mfrs}
    pool = [f for f in fac if f.rels and f.owes(2026) and f.filing.get(2026) is not None and f.cred in ("MD", "DO")
            and max([d for (k, y), d in f.lines.items() if y == 2026 and k in {m["id"] for m in mfrs}] or [0]) > 15000]
    picks = r.choice(len(pool), size=len(W.NOW_REPORTING_LINES), replace=False)
    for (name, kind, lo, hi), k in zip(W.NOW_REPORTING_LINES, picks):
        f = pool[int(k)]
        m = byname[name]
        if any(rel["mfr"] == m["id"] for rel in f.rels):
            continue
        rel = new_relationship(m["id"], kind, r, schedule="events", start=int(r.integers(2, 7)))
        rel["years"][2026] = float(r.uniform(lo, hi))
        rel["now_reporting"] = True
        pay_out(rel, r)
        f.rels.append(rel)
        rr = np.random.default_rng([W.SEED, 4, int(f.emp_id), 2])
        f.draw[(m["id"], 2026)] = (False, _ratio(f, rr))
        first_lines(f)


# ------------------------------------------------------------------------------------------------ docket region
# kinds: F large faithful January filers; U long-record under-reporters with a new large relationship; C faithful
# filers whose large quarterly retainer grew and who filed early in December 2026, before its December installment;
# X faithful filers who filed in early December in earlier years (their retainers' December installments missing from
# those disclosures), in January 2026, with a new large relationship; P faithful January filers just below; O faculty
# who leave small relationships out and report the ones they name in full; T new faculty with one matched line read
# low; B ordinary large faithful disclosers below the docket; S a long-standing faithful January filer below it. The
# comparison year (2025) carries U25, O25, T25, C25 and X25.
GROUPS = [("F", 5), ("U", 5), ("C", 5), ("X", 5), ("P", 5), ("O", 5), ("T", 5), ("B", 12),
          ("U25", 7), ("O25", 8), ("T25", 7), ("C25", 7), ("X25", 7), ("S", 1)]
GROUP_DEPTS = {"F": ["CARD", "ORTH", "HEON", "NEUR", "GAST"],
               "U": ["ORTH", "CARD", "NEUR", "UROL", "HEON"],
               "C": ["CARD", "ORTH", "GAST", "HEON", "DERM"],
               "X": ["NEUR", "CARD", "ORTH", "OPHT", "HEON"],
               "P": ["ORTH", "CARD", "UROL", "NEUR", "DERM"],
               "O": ["PSYC", "NEUR", "IMED", "CARD", "GAST"],
               "T": ["CARD", "ORTH", "DERM", "OPHT", "NEUR"],
               "B": ["CARD", "ORTH", "HEON", "NEUR", "GAST", "DERM", "OPHT", "UROL", "PSYC", "IMED", "CARD", "ORTH"],
               "U25": ["ORTH", "HEON", "CARD", "GAST", "NEUR", "UROL", "ORTH"],
               "O25": ["PSYC", "IMED", "NEUR", "HEON", "DERM", "GAST", "CARD", "ORTH"],
               "T25": ["CARD", "ORTH", "UROL", "NEUR", "DERM", "OPHT", "GAST"],
               "C25": ["CARD", "ORTH", "HEON", "NEUR", "GAST", "UROL", "DERM"],
               "X25": ["ORTH", "CARD", "NEUR", "HEON", "OPHT", "GAST", "UROL"],
               "S": ["UROL"]}
NAMED = ("F", "U", "C", "X", "P", "S")    # the kinds that can stand in the top sixteen take the fixed names


def _lu(r, lo, hi):
    return float(np.exp(r.uniform(np.log(lo), np.log(hi))))


def _plan(kind, f, mfrs, r, taken):
    """The member's relationships, the large one first: (manufacturer, kind, schedule, start, {year: amount}, force)."""
    def pick(dept, own=False):
        pool = ([m for m in mfrs if m["primary"] == dept and m["id"] not in taken] or
                [m for m in mfrs if dept in m["depts"] and m["id"] not in taken]) if own else None
        while True:
            m = pool[int(r.integers(len(pool)))] if pool else _mfr_for(dept, mfrs, r)
            if m["id"] not in taken and m["index"] not in W.RENAMED and m["name"] not in W.NOW_REPORTING:
                taken.add(m["id"])
                return m["id"]
    Y = 2025 if kind.endswith("25") else 2026
    base = kind[0]
    years = lambda a, b: list(range(a, b + 1))
    small = lambda lo, hi: _lu(r, lo, hi)
    P = []

    def extras(n, last_year, first_year=2021):
        for _ in range(n):
            k = str(r.choice(["speaking", "advisory", "honoraria", "speaking", "consulting"]))
            a0 = int(r.integers(first_year, last_year))
            a1 = int(r.integers(a0, last_year + 1))
            lvl = small(2500, 11000)
            P.append((pick(f.dept), k, None, 1, {y: lvl * float(np.exp(r.normal(0, 0.15))) for y in years(a0, a1)}, True))

    if base == "F":
        lvl = _lu(r, 88000, 135000)
        s0 = int(r.choice([2021, 2022, 2023]))
        g = float(r.uniform(1.0, 1.07))
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "monthly", "events"])), 1,
                  {y: lvl * g ** (y - Y) * float(np.exp(r.normal(0, 0.06))) for y in years(s0, Y)}, True))
        extras(int(r.integers(2, 5)), Y)
    elif base == "U":
        lvl = _lu(r, 80000, 95000)
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "monthly", "events"])), 1, {Y: lvl}, True))
        for k in ("speaking", "consulting", "advisory", "honoraria", "speaking", "consulting"):
            if len(P) > 1 and r.random() < 0.25:
                continue
            a0 = int(r.integers(2021, 2023))
            a1 = int(r.integers(max(a0 + 2, Y - 2), Y + 1))
            lvl2 = small(3000, 13000)
            P.append((pick(f.dept), k, None, 1, {y: lvl2 * float(np.exp(r.normal(0, 0.12))) for y in years(a0, a1)}, True))
    elif base == "C":
        lvl = _lu(r, 48500, 52500)
        s0 = int(r.choice([2021, 2022, 2023]))
        amounts = {y: lvl * float(np.exp(r.normal(0, 0.05))) for y in years(s0, Y - 1)}
        amounts[Y] = lvl * float(r.uniform(1.36, 1.46))
        P.append((pick(f.dept, True), "consulting", "quarterly", 1, amounts, True))
        extras(int(r.integers(1, 4)), Y)
    elif base == "X":
        lvl = _lu(r, 46500, 49500)
        P.append((pick(f.dept, True), "consulting", str(r.choice(["events", "quarterly"])), 1, {Y: lvl}, True))
        q = small(18000, 30000)
        P.append((pick(f.dept), "consulting", "quarterly", 1, {y: q * float(np.exp(r.normal(0, 0.06))) for y in years(2021, Y - 1)}, True))
        mo = small(6000, 12000)
        P.append((pick(f.dept), str(r.choice(["consulting", "advisory"])), "monthly", 1,
                  {y: mo * float(np.exp(r.normal(0, 0.08))) for y in years(int(r.integers(2021, 2023)), Y - 1)}, True))
        extras(int(r.integers(0, 2)), Y - 1)
    elif base == "S":
        lvl = _lu(r, 40000, 43000)
        s0 = int(r.choice([2021, 2022]))
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "monthly", "events"])), 1,
                  {y: lvl * float(np.exp(r.normal(0, 0.05))) for y in years(s0, Y)}, True))
        extras(int(r.integers(2, 4)), Y)
    elif base == "B":
        lvl = _lu(r, 24800, 43000)
        s0 = int(r.choice([2021, 2022, 2023, 2026, 2026]))
        P.append((pick(f.dept, True), str(r.choice(["consulting", "consulting", "advisory"])),
                  str(r.choice(["quarterly", "monthly", "events"])), 1,
                  {y: lvl * float(np.exp(r.normal(0, 0.08))) for y in years(s0, 2026)}, True))
        extras(int(r.integers(1, 4)), 2026)
    elif base == "P":
        lvl = _lu(r, 41500, 46000)
        s0 = int(r.choice([2021, 2022, 2023, 2024, Y]))
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "monthly", "events"])), 1,
                  {y: lvl * float(np.exp(r.normal(0, 0.05))) for y in years(s0, Y)}, True))
        extras(int(r.integers(1, 4)), Y)
    elif base == "O":
        lvl = _lu(r, 38000, 46000)
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "events"])), 1, {Y: lvl}, True))
        mid = small(8000, 11000)
        P.append((pick(f.dept), "consulting", None, 1, {y: mid for y in years(2021, Y - 1)}, True))
        for x in range(8):
            lvl2 = 2800 + 260 * x + float(r.uniform(-200, 200))
            P.append((pick("IMED" if x % 2 else f.dept), "speaking", "events", 1,
                      {y: lvl2 * float(np.exp(r.normal(0, 0.1))) for y in years(2021, Y)}, None))
    elif base == "T":
        lvl = _lu(r, 21500, 25500)
        y1 = f.start.year + (1 if f.start.month > 6 else 0)
        P.append((pick(f.dept, True), "consulting", str(r.choice(["quarterly", "events"])), 1, {Y: lvl}, True))
        P.append((pick(f.dept), "speaking", "events", 1, {y1: small(1400, 2600)}, "partial"))
    return P


def _member_filing(kind, f, r):
    Y = 2025 if kind.endswith("25") else 2026
    base = kind[0]
    f.filing = {}
    for y in W.YEARS:
        if not f.owes(y):
            continue
        if base == "C" and y == Y:
            f.filing[y] = filing_time(r, y, "dec", last_day=11)
        elif base == "X" and y < Y:
            f.filing[y] = filing_time(r, y, "dec", last_day=11) if r.random() < 0.88 else filing_time(r, y, "jan")
        else:
            f.filing[y] = filing_time(r, y, "evening" if r.random() < 0.15 else "jan")


def docket_region(fac, mfrs):
    """Draw the docket-region and comparison-year members, each from its own stream, keeping the first draw whose
    measured quantities land where the design needs them."""
    groups = []
    for k, (kind, n) in enumerate(GROUPS):
        for q in range(n):
            for s in range(6000):
                r = np.random.default_rng([W.SEED, 7, k, q, s])
                f = _member(kind, q, r, mfrs)
                if _member_ok(kind, f):
                    break
            else:
                raise SystemExit("no draw for %s %d" % (kind, q))
            f.seed = s
            groups.append(f)
    return groups


def _member(kind, q, r, mfrs):
    f = Faculty(group=kind, q=q)
    f.dept = GROUP_DEPTS[kind][q]
    if kind[0] == "T":
        f.start = D((2022 + q % 3) if kind == "T" else (2022 + q % 2), 7, 1)
        f.rank = "Assistant Professor"
    else:
        f.start = D(int(r.integers(2003, 2016)), int(r.choice([7, 7, 7, 9, 1])), 1)
        f.rank = str(r.choice(["Associate Professor", "Professor", "Professor"]))
    f.end = None
    f.cred = "MD"
    base = kind[0]
    f.mu = float(np.log(r.uniform(0.50, 0.62))) if base == "U" else float(np.log(r.uniform(0.95, 0.99)))
    f.o = 0.92 if base == "O" else 0.03
    f.ppart = 0.0 if base in ("F", "C", "X", "P", "U", "B", "S") else PPART
    f.rounding = float(r.choice([100.0, 100.0, 500.0]))
    f.contact = True
    taken = set()
    f.rels = []
    for j, (mfr, rk, sched, start, yrs, force) in enumerate(_plan(kind, f, mfrs, r, taken)):
        rel = new_relationship(mfr, rk, r, schedule=sched, start=start)
        rel["force"] = True if force in (True, "partial") else force
        rel["big"] = j == 0
        if force == "partial":
            rel["partial"] = min(yrs)
        rel["years"] = dict(yrs)
        pay_out(rel, r)
        f.rels.append(rel)
    _member_filing(kind, f, r)
    _draws(f, r)
    first_lines(f)
    return f


def _matched(f, cut, aligned):
    """[(published, disclosed)] on the member's matched lines before `cut`; aligned: published counted to the filing."""
    out = []
    for rel in f.rels:
        if rel["mfr"] is None:
            continue
        for y in rel["years"]:
            d = f.lines.get((rel["mfr"], y))
            if y < cut and d:
                a = received(rel, y, f.filing[y]) if aligned else sum(x for _, x in rel["pay"][y])
                out.append((a, d))
    return out


def line_ratio_member(f, cut, aligned=False):
    """The faculty member's amount-reporting ratio on matched lines before `cut`: (ratio, lines)."""
    pairs = _matched(f, cut, aligned)
    if not pairs:
        return None, 0
    return sum(d for a, d in pairs) / sum(a for a, d in pairs), len(pairs)


def overall_ratio_member(f, cut):
    """The share of the register's remuneration (years the member owed a disclosure, before `cut`) disclosed."""
    a_sum = d_sum = 0.0
    for rel in f.rels:
        if rel["mfr"] is None:
            continue
        for y, a in rel["years"].items():
            if y < cut and f.owes(y):
                a_sum += a
                d_sum += f.lines.get((rel["mfr"], y)) or 0.0
    return d_sum / a_sum if a_sum else None


def _member_ok(kind, f):
    Y = 2025 if kind.endswith("25") else 2026
    base = kind[0]
    c, n = line_ratio_member(f, Y)
    ca, _ = line_ratio_member(f, Y, aligned=True)
    co = overall_ratio_member(f, Y)
    if c is None:
        return False
    big = f.rels[0]
    d = f.lines.get((big["mfr"], Y))
    if not d:
        return False
    true = big["years"][Y]
    if base == "F":
        return 0.90 <= ca <= 1.0 and d >= 0.88 * true
    if base == "U":
        return 0.47 <= ca <= 0.64 and n >= 15 and 0.94 <= d / true / ca <= 1.06
    if base == "C":
        return (0.93 <= c <= 1.0 and 0.96 <= d / (0.75 * true * c) <= 1.04 and 49000 <= d / c <= 56500
                and 70500 <= true <= 75500)
    if base == "X":
        return (0.68 <= c <= 0.78 and 0.93 <= ca <= 1.01 and 0.93 * true <= d <= 1.0 * true and 60000 <= d / c <= 70000
                and true <= 49500)
    if base == "P":
        return 0.92 <= ca <= 1.0 and 0.92 * true <= d <= 1.0 * true and true <= 46000
    if base == "B":
        return 0.93 <= ca <= 1.0 and 0.93 <= c <= 1.0 and 0.93 * true <= d <= 1.0 * true and true <= 44000
    if base == "S":
        return (0.94 <= ca <= 1.0 and 0.94 <= c <= 1.0 and 0.95 * true <= d <= 1.0 * true and 40000 <= true <= 43500
                and n >= 8)
    if base == "O":
        return 0.90 <= c <= 1.0 and co is not None and co <= 0.55 and n >= 5 and d <= true <= 44000
    if base == "T":
        return n == 1 and c <= 0.27
    return True


# --------------------------------------------------------------------------------------------- the whole faculty
def _emp_slots(fac, groups, r):
    """Employee numbers for the docket region inside the roster's own runs (hires among hires), so nothing in the number
    marks them."""
    taken = {int(f.emp_id) for f in fac}
    runs = {False: sorted(int(f.emp_id) for f in fac if not f.hire_block),
            True: sorted(int(f.emp_id) for f in fac if f.hire_block)}
    out = []
    for f in groups:
        seq = runs[f.start.year >= 2021]
        while True:
            i = int(r.integers(1, len(seq)))
            lo, hi = seq[i - 1], seq[i]
            if hi - lo >= 3:
                x = int(r.integers(lo + 1, hi))
                if x not in taken:
                    taken.add(x)
                    out.append("%07d" % x)
                    break
    return out


def population():
    """The faculty (background and docket region, identities drawn from one pool), the namesakes and the faculty whose
    employee numbers changed in 2026."""
    mfrs = W.manufacturers()
    fac = roster()
    relationships(fac, mfrs)
    filing_plan(fac)
    disclose_all(fac)
    device_relationships(fac, mfrs)
    now_reporting_relationships(fac, mfrs)
    groups = docket_region(fac, mfrs)
    r = np.random.default_rng([W.SEED, 5])
    ff, fm, ll = W.first_last_pools()
    names = {(f.first, f.last) for f in fac}
    npis = {f.npi for f in fac}
    fixed = [nm for nm in W.REGION_NAMES]
    fixed_firsts = {a for a, _ in fixed}
    fixed_lasts = {b for _, b in fixed}
    slots = _emp_slots(fac, groups, r)
    k_named = 0
    for f, emp in zip(groups, slots):
        if f.group in NAMED:
            first, last = fixed[k_named]
            k_named += 1
        else:
            while True:
                female = r.random() < 0.47
                first = (ff if female else fm)[int(r.integers(len(ff if female else fm)))]
                last = ll[int(r.integers(len(ll)))]
                if (first, last) not in names and first not in fixed_firsts and last not in fixed_lasts:
                    break
        assert (first, last) not in names
        names.add((first, last))
        while True:
            n = W.npi(r)
            if n not in npis:
                break
        npis.add(n)
        f.emp_id, f.first, f.last, f.npi = emp, first, last, n
        f.middle = str(r.choice(list("ABCDEFGHJKLMNPRSTW")))
        f.terms = _terms(f, r)
        if f.dept in W.SUCCESSOR_OF:
            # the docket region's appointments in the new departments were reissued on 1 July 2025
            f.terms = [t for t in f.terms if t["end"] < W.REORG] + [
                {"dept": f.dept, "division": "", "start": max(t["start"], W.REORG), "end": t["end"], "primary": True}
                for t in f.terms if t["end"] >= W.REORG]
    allfac = sorted(fac + groups, key=lambda f: f.emp_id)
    namesakes = []
    twins = [f for f in fac if f.contact and f.group == "bg" and f.rels]
    pick = r.choice(len(twins), size=46, replace=False)
    for k in sorted(pick):
        t = twins[int(k)]
        while True:
            n = W.npi(r)
            if n not in npis:
                break
        npis.add(n)
        ns = Faculty(first=t.first, last=t.last, middle=str(r.choice(list("ABCDEFGHJKLMNPRSTW"))), npi=n, twin=t,
                     lam=float(np.exp(r.normal(np.log(3.0), 0.6))), group="namesake", emp_id=None,
                     city=r.integers(0, 15))
        namesakes.append(ns)
    rekey(allfac, r)
    return allfac, namesakes, mfrs


def rekey(fac, r):
    """Faculty who moved between the university and the health system in 2026 and were issued a new employee number
    (their appointment reissued under it the next day); the disclosure system keeps the number it first knew. Drawn from
    faculty with no industry relationships, in every department."""
    used = {int(f.emp_id) for f in fac}
    top = max(used)
    by_dept = {}
    for f in fac:
        if (f.group == "bg" and not f.rels and f.owes(2025) and f.owes(2026) and f.end is None
                and f.filing.get(2026) is not None and all(t["primary"] for t in f.terms)):
            by_dept.setdefault(f.dept, []).append(f)
    for dept in sorted(by_dept):
        pool = by_dept[dept]
        n = min(len(pool), int(r.integers(1, 4)))
        for k in r.choice(len(pool), size=n, replace=False):
            f = pool[int(k)]
            day = D(2026, int(r.choice([3, 5, 7, 8, 9, 10])), 1)
            top += int(r.integers(3, 40))
            f.new_emp_id = "%07d" % top
            f.rekey_day = day
