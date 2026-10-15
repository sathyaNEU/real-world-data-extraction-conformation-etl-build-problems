"""The plan's adult members in the contract year: persons, their eligibility spells and their conditions.

A person enrolled for the whole year has one spell (sometimes two, joined by a retroactive row or split by a move
between counties); a person enrolled part of the year joined or left during it; an expansion adult or a parent in a
farm county often holds one short seasonal spell of one to four months. A re-enrolment after a gap of more than 90 days
is issued a new member number; the person number ties a person's member numbers together. Each person's serious
mental illness and opioid use disorder are allocated from their county and eligibility group's prevalence, at about half
of it for the seasonal farmworkers; and each member with a condition is assigned the enrolled month of the first service
carrying it (or none within their months), so that among the members of a county and group enrolled k months who have the
condition, the share a service identifies within the k months is the same F(k) everywhere."""
import datetime as dt

import numpy as np

import world as W

D = dt.date
DAY = dt.timedelta(days=1)


class Person:
    __slots__ = ("pid", "county", "group", "sex", "dob", "spells", "smi", "oud", "months", "short", "member_ids",
                 "engage", "moved_from", "kind", "first")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def _month_start(y, m):
    return D(y, m, 1)


def _month_end(y, m):
    return D(y + (m == 12), m % 12 + 1, 1) - DAY


def _dob(r, g):
    lo, hi = {"DSB": (21, 64), "EXP": (20, 64), "PCR": (20, 54), "AGD": (66, 89)}[g]
    age = int(r.integers(lo, hi + 1))
    return D(2025 - age, int(r.integers(1, 13)), int(r.integers(1, 29)))


def _birthday(dob, age):
    return D(dob.year + age, dob.month, dob.day)


def _coverage(r, g, short_share):
    """[(start, end)] of the person's coverage, the contract year's part and what lies either side of it."""
    S, E = W.WINDOW_START, W.WINDOW_END
    if g in ("EXP", "PCR") and r.random() < short_share:
        if short_share > 0.4 and r.random() < 0.25:
            # two seasons: spring thinning or summer harvest, then the autumn apple and potato harvest
            m1 = int(r.integers(1, 3))
            m2 = int(r.integers(1, 3))
            k1 = int(r.integers(0, 3))                   # starts July to September 2025
            k2 = int(r.integers(k1 + m1 + 4, 13 - m2))   # four or more months later
            out = []
            for k, m in ((k1, m1), (k2, m2)):
                y, mo = W.MONTHS[k]
                y2, mo2 = W.MONTHS[k + m - 1]
                out.append((_month_start(y, mo), _month_end(y2, mo2)))
            return out, "short"
        m = int(r.choice([1, 2, 2, 3, 3, 4, 5, 6], p=[0.18, 0.15, 0.15, 0.14, 0.13, 0.11, 0.08, 0.06]))
        k = int(r.integers(0, 13 - m))
        y, mo = W.MONTHS[k]
        y2, mo2 = W.MONTHS[k + m - 1]
        return [(_month_start(y, mo), _month_end(y2, mo2))], "short"
    full = {"DSB": 0.96, "AGD": 0.90}.get(g, 0.82)
    if r.random() < full:
        start = S - dt.timedelta(days=int(r.integers(40, 2400)))
        end = E + dt.timedelta(days=int(r.integers(1, 500))) if r.random() < 0.9 else None
        return [(start, end)], "full"
    # joined or left during the year
    m = int(r.integers(5, 12))
    if r.random() < 0.5:
        k = 12 - m
        y, mo = W.MONTHS[k]
        return [(_month_start(y, mo), E + dt.timedelta(days=int(r.integers(1, 300))))], "joined"
    y, mo = W.MONTHS[m - 1]
    return [(S - dt.timedelta(days=int(r.integers(30, 1500))), _month_end(y, mo))], "left"


def population():
    """Every adult person the plan enrolled on at least one day of the contract year, in a fixed order."""
    out = []
    pid = 31_000_000
    for ci, (cname, c) in enumerate(sorted(W.COUNTIES.items())):
        for gi, g in enumerate(W.GROUPS):
            r = np.random.default_rng([W.SEED, 1, ci, gi])
            for k in range(c["persons"][g]):
                pid += int(r.integers(1, 23))
                cov, kind = _coverage(r, g, c["short"])
                p = Person(pid="P%09d" % pid, county=cname, group=g, sex=str(r.choice(["F", "M"], p=[0.56, 0.44])),
                           dob=_dob(r, g), kind=kind)
                p.smi = p.oud = False
                p.first = {"SMI": None, "OUD": None}
                p.engage = float(np.exp(r.normal(0.0, 0.25)))
                # an adult span starts no earlier than the 19th birthday (the 65th for adults 65 and over)
                floor = _birthday(p.dob, 65 if g == "AGD" else 19)
                p.spells = [{"start": max(s, floor), "end": e, "county": cname,
                             "source": "NEW" if max(s, floor) >= W.WINDOW_START - dt.timedelta(days=31) else "RENEWAL"}
                            for s, e in cov]
                p.moved_from = None
                out.append(p)
    _moves(out)
    _gaps(out)
    for p in out:
        p.months = months_enrolled(p)
        p.short = p.kind == "short"
    _conditions(out)
    _identification(out)
    return out


def _conditions(persons):
    """Each condition allocated exactly within county (where the member lives at the end of their enrollment), eligibility
    group and kind of member: the seasonal farmworkers in short spells at RHO times the rate of the others. The rate is
    the group's prevalence times the county's factor and a factor of the county and group's own. Within each kind the
    allocation is nested by months enrolled (among the members enrolled at least k months, for every k, the share with
    the condition is the rate, to the nearest member)."""
    r = np.random.default_rng([W.SEED, 5, W.ALLOC_DRAW])
    cells = {}
    for p in persons:
        cells.setdefault((p.county, p.group), []).append(p)
    names = sorted(W.COUNTIES)
    for key in sorted(cells, key=lambda k: (k[0], W.GROUPS.index(k[1]))):
        c, g = key
        fr = np.random.default_rng([W.SEED, 6, names.index(c), W.GROUPS.index(g)])
        ps = cells[key]
        for cond in ("SMI", "OUD"):
            rate = W.PREV[cond][g] * W.COUNTIES[c]["f_" + cond.lower()] * float(np.exp(fr.normal(0.0, 0.08)))
            for seasonal in (False, True):
                cls_all = [p for p in ps if p.short == seasonal]
                rt = rate * (W.RHO[cond] if seasonal else 1.0)
                prev_target, cum = 0, 0
                for m in range(12, 0, -1):
                    cls = [p for p in cls_all if len(p.months) == m]
                    cum += len(cls)
                    target = int(round(cum * rt))
                    k = min(max(target - prev_target, 0), len(cls))
                    idx = set(int(i) for i in r.choice(len(cls), size=k, replace=False)) if k else set()
                    for i, p in enumerate(cls):
                        setattr(p, cond.lower(), i in idx)
                    prev_target += k


def _identification(persons):
    """The enrolled month (1 = the member's first enrolled month of the contract year) of the first service carrying each
    condition, for each member who has it; None when no service in the member's months carries it. Allocated exactly
    within county, eligibility group and months enrolled: among the n members enrolled m months who have the condition,
    round(F(k) n) are first identified within their first k months, for every k up to m."""
    r = np.random.default_rng([W.SEED, 7, W.ID_DRAW])
    cells = {}
    for p in persons:
        for cond in ("SMI", "OUD"):
            if getattr(p, cond.lower()):
                cells.setdefault((p.county, p.group, cond, len(p.months)), []).append(p)
    for key in sorted(cells, key=lambda k: (k[0], W.GROUPS.index(k[1]), k[2], k[3])):
        c, g, cond, m = key
        ps = cells[key]
        n = len(ps)
        order = [ps[int(i)] for i in r.permutation(n)]
        done = 0
        for k in range(1, m + 1):
            upto = int(round(W.capture(cond, k) * n)) if k < 12 else n
            for p in order[done:upto]:
                p.first[cond] = k
            done = max(done, upto)


def _moves(persons):
    """About one full-year adult in sixty moved between the plan's counties during the year: the spell splits at the
    move, the later spell in the new county."""
    r = np.random.default_rng([W.SEED, 2])
    names = sorted(W.COUNTIES)
    for p in persons:
        if p.kind != "full" or r.random() > 1 / 60:
            continue
        new = names[int(r.integers(len(names)))]
        if new == p.county:
            continue
        k = int(r.integers(2, 11))
        y, mo = W.MONTHS[k]
        cut = _month_start(y, mo)
        s = p.spells[0]
        p.spells = [{"start": s["start"], "end": cut - DAY, "county": p.county, "source": s["source"]},
                    {"start": cut, "end": s["end"], "county": new, "source": "TRANSFER"}]
        p.moved_from, p.county = p.county, new


def _gaps(persons):
    """A few full-year adults lost coverage at redetermination and came back (a gap of one month keeps the member
    number); a few joined with coverage backdated to the months before they applied (a RETRO row, sometimes
    overlapping the application month's row)."""
    r = np.random.default_rng([W.SEED, 3])
    for p in persons:
        if p.kind == "full" and len(p.spells) == 1 and r.random() < 0.035:
            s = p.spells[0]
            k = int(r.integers(2, 10))
            y, mo = W.MONTHS[k]
            gap_start = _month_start(y, mo)
            gap_end = _month_end(y, mo)
            p.spells = [{"start": s["start"], "end": gap_start - DAY, "county": s["county"], "source": s["source"]},
                        {"start": gap_end + DAY, "end": s["end"], "county": s["county"], "source": "RENEWAL"}]
            p.kind = "gap"
        elif p.kind in ("joined", "short") and r.random() < 0.06:
            s = p.spells[0]
            back = int(r.integers(1, 3))
            rs = max(W.WINDOW_START, _shift_months(s["start"], -back))
            if rs >= s["start"]:
                continue
            overlap = r.random() < 0.4
            re = (_shift_months(s["start"], 1) - DAY) if overlap else s["start"] - DAY
            p.spells = [{"start": rs, "end": re, "county": s["county"], "source": "RETRO"}] + p.spells


def _shift_months(d, k):
    y, m = d.year, d.month + k
    while m < 1:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    return D(y, m, 1)


def coverage_days(p):
    """The set of the contract year's days the person was covered."""
    days = set()
    for s in p.spells:
        a = max(s["start"], W.WINDOW_START)
        b = min(s["end"] or W.WINDOW_END, W.WINDOW_END)
        d = a
        while d <= b:
            days.add(d)
            d += DAY
    return days


def months_enrolled(p):
    """The contract-year months the person was covered on at least one day."""
    out = set()
    for s in p.spells:
        out.update(W.months_of(max(s["start"], W.WINDOW_START), min(s["end"] or W.WINDOW_END, W.WINDOW_END)))
    return sorted(out)


def member_numbers(persons):
    """Issue member numbers: a person's spells share one number unless they came back after more than 90 days
    without coverage, which issues a new one."""
    r = np.random.default_rng([W.SEED, 4])
    used = set()

    def new():
        while True:
            n = "SH" + "%08d" % int(r.integers(10_000_000, 99_999_999))
            if n not in used:
                used.add(n)
                return n
    for p in persons:
        spells = sorted(p.spells, key=lambda s: s["start"])
        cur = new()
        prev_end = None
        for s in spells:
            if prev_end is not None and (s["start"] - prev_end).days > 91:
                cur = new()
            s["member_id"] = cur
            prev_end = max(prev_end or s["end"] or W.WINDOW_END, s["end"] or W.WINDOW_END)
        p.member_ids = sorted({s["member_id"] for s in p.spells})
