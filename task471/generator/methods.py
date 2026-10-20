"""The estimators every rung uses, on a plain data structure the generator and the bundle reader both build:

    d["census"][(region, sex, age)]   = (counted, imputed)          the census tables, counted including imputed
    d["e"][(region, sex, age)]        = (records, correct)          the survey's census-record sample
    d["p"][(region, sex, age)]        = (people, matched)           the survey's people
    d["roll"][region]                 = electors on census day
    d["births"][(year, sex)], d["deaths"|"departures"|"arrivals"][(year, sex, age)]   national flows

Ages are single years, 100 meaning 100 and over.
"""
import world as W

SEXES = ("M", "F")


def cells(d, groups=W.AGE_GROUPS):
    """sums of the census tables and the two samples by estimation cell (region, sex, age group)"""
    out = {}
    for (c, s, a), (cnt, imp) in d["census"].items():
        g = W.age_group(a)
        if g not in groups:
            continue
        o = out.setdefault((c, s, g), [0, 0, 0, 0, 0, 0])
        o[0] += cnt
        o[1] += imp
    for key, idx in (("e", 2), ("p", 4)):
        for (c, s, a), (n, k) in d[key].items():
            g = W.age_group(a)
            if g not in groups:
                continue
            o = out.setdefault((c, s, g), [0, 0, 0, 0, 0, 0])
            o[idx] += n
            o[idx + 1] += k
    return out


def dse(cell, erroneous=True, imputed=True):
    """dual-system estimate of a cell: census records that could be matched, kept at the survey's share correctly
    counted, raised by the survey's people over those the census also counted"""
    cnt, imp, e, ce, p, m = cell
    base = cnt - imp if imputed else cnt
    keep = ce / float(e) if erroneous else 1.0
    return base * keep * p / float(m)


def dse_cells(d, **kw):
    return {k: dse(v, **kw) for k, v in cells(d).items()}


def demographic(d, to_census_day=True, born_before=62.0 / 365.0):
    """people living in the country by sex and single year of age on census day (or at the end of 2024), rebuilt cohort
    by cohort: births, less deaths and departures, plus arrivals, each flow by year of birth; a cohort born in year c
    is aged 2024 - c on census day, or 2025 - c for those born before 4 March (the share `born_before`)"""
    pop = {}
    for s in SEXES:
        coh = {}
        for (y, sx), b in d["births"].items():
            if sx == s and y != "2025Q":
                coh[y] = coh.get(y, 0) + b
        for key, sign in (("deaths", -1), ("departures", -1), ("arrivals", 1)):
            for (y, sx, c), n in d[key].items():
                if sx != s or (y == "2025Q" and not to_census_day):
                    continue
                coh[c] = coh.get(c, 0) + sign * n
        for c, n in coh.items():
            if to_census_day:
                for k, age in ((n * (1 - born_before), 2024 - c), (n * born_before, 2025 - c)):
                    if age >= 0:
                        pop[(s, min(age, 100))] = pop.get((s, min(age, 100)), 0) + k
            else:
                pop[(s, min(2024 - c, 100))] = pop.get((s, min(2024 - c, 100)), 0) + n
        if to_census_day:
            pop[(s, 0)] = pop.get((s, 0), 0) + d["births"].get(("2025Q", s), 0)
    return pop


def da_ratio(d, groups=W.YOUNG_GROUPS, **kw):
    """demographic analysis's men per woman in each age group"""
    pop = demographic(d, **kw)
    out = {}
    for lo, hi in groups:
        m = sum(pop.get(("M", a), 0) for a in range(lo, min(hi, 100) + 1))
        f = sum(pop.get(("F", a), 0) for a in range(lo, min(hi, 100) + 1))
        out[(lo, hi)] = m / f
    return out


def factors(d, est, groups=W.YOUNG_GROUPS, mode="ratio", **kw):
    """the multiplier that brings each young age group's male estimates to demographic analysis's sex ratio against
    the female estimates (mode ratio), or to its male total (mode total)"""
    r = da_ratio(d, groups=groups, **kw)
    out = {}
    if mode == "total":
        pop = demographic(d, **kw)
    for g in groups:
        inside = lambda gg: g[0] <= gg[0] and gg[1] <= g[1]
        m = sum(v for (c, s, gg), v in est.items() if s == "M" and inside(gg))
        f = sum(v for (c, s, gg), v in est.items() if s == "F" and inside(gg))
        if mode == "ratio":
            out[g] = r[g] * f / m
        else:
            out[g] = sum(pop.get(("M", a), 0) for a in range(g[0], min(g[1], 100) + 1)) / m
    return out


def adults(est, fac=None):
    """adults per region from cell estimates, the young men's cells multiplied by their factors"""
    out = {c: 0.0 for c in W.CODES}
    for (c, s, g), v in est.items():
        if g[0] < 18:
            continue
        if fac and s == "M" and g in fac:
            v = v * fac[g]
        out[c] += v
    return out


def allocate(gap, total=W.ORGANISERS, floor=W.FLOOR):
    """largest remainders on each region's share of the adults not on the roll, at least `floor` each: regions whose
    quota falls under the floor take the floor and the rest is shared again among the others"""
    fixed = {}
    while True:
        free = [c for c in W.CODES if c not in fixed]
        left = total - sum(fixed.values())
        g = sum(gap[c] for c in free)
        quota = {c: gap[c] / g * left for c in free}
        low = [c for c in free if quota[c] < floor]
        if not low:
            break
        for c in low:
            fixed[c] = floor
    out = dict(fixed)
    for c in free:
        out[c] = int(quota[c])
    rest = left - sum(int(quota[c]) for c in free)
    order = sorted(free, key=lambda c: (-(quota[c] - int(quota[c])), c))
    for c in order[:rest]:
        out[c] += 1
    return out, quota


def margin(quota, alloc):
    """how far the largest-remainder cut sits from the nearest region on either side, in organisers"""
    rem = sorted(((q - int(q), c) for c, q in quota.items()), reverse=True)
    got = [c for c in quota if alloc[c] > int(quota[c])]
    k = len(got)
    if k == 0 or k == len(rem):
        return 1.0
    return rem[k - 1][0] - rem[k][0]


# ------------------------------------------------------------------ the asks, on the roll's transaction log as shipped

import datetime as _dt

LOG_COLS = ["TXN_ID", "PROCESSED", "TXN_TYPE", "REASON", "SOURCE", "STATUS", "ELECTOR_NO", "PERSON_REF", "ELECTORATE",
            "ADDRESS_TYPE", "SEX", "BIRTH_YEAR", "REF_TXN"]


def old_platform(row):
    return row["TXN_ID"].startswith("R25-")


def local_time(row, utc=True):
    """the country's time of a transaction: the old platform stamped local time, the new one UTC (utc="all" reads every
    stamp as UTC, utc=False every stamp as written)"""
    t = row.get("_t")
    if t is None:
        t = row["_t"] = _dt.datetime.strptime(row["PROCESSED"], "%Y-%m-%d %H:%M:%S")
    if not utc or (old_platform(row) and utc != "all"):
        return t
    lo, hi = W.DST_2025
    for off in (13, 12):
        loc = t + _dt.timedelta(hours=off)
        if (lo <= loc < hi) == (off == 13):
            return loc
    return t + _dt.timedelta(hours=12)


def in_window(t, start_on_census_day=False):
    first = W.CENSUS_DAY if start_on_census_day else W.CENSUS_DAY + _dt.timedelta(days=1)
    return first <= t.date() <= W.LOG_END


def new_electors(rows, region, utc=True, link=True, prior="record", census_day=False, overseas=False, rejected=False):
    """people added to the roll in the window who were not on it on census day, each once, in the region of the
    residential address of their first enrolment in the window. A person is every person reference the transactions'
    REF_TXN ties together (link); a person was on the roll on census day if one of their removals in the window took off
    a record no enrolment in the window had created (prior "record"), or, as a reader may take it, if their first
    transaction in the window is a removal (prior "first")"""
    ok = lambda r: r["STATUS"] == "A" or rejected
    win = sorted(((local_time(r, utc), i, r) for i, r in enumerate(rows)), key=lambda x: (x[0], x[1]))
    win = [(t, r) for t, i, r in win if in_window(t, census_day) and ok(r)]
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    if link:
        by_id = {r["TXN_ID"]: r for r in rows}
        for r in rows:
            if r["REF_TXN"] in by_id:
                a, b = find(r["PERSON_REF"]), find(by_id[r["REF_TXN"]]["PERSON_REF"])
                if a != b:
                    parent[a] = b
    created = {r["ELECTOR_NO"] for t, r in win if r["TXN_TYPE"] == "NEW"}
    on_roll, first, seen = set(), {}, set()
    for t, r in win:
        p = find(r["PERSON_REF"])
        if prior == "record" and r["TXN_TYPE"] == "DEL" and r["ELECTOR_NO"] not in created:
            on_roll.add(p)
        if prior == "first" and p not in seen and r["TXN_TYPE"] == "DEL":
            on_roll.add(p)
        seen.add(p)
        if r["TXN_TYPE"] == "NEW" and p not in first:
            first[p] = r
    out = {c: 0 for c in W.CODES}
    for p, r in first.items():
        if p in on_roll or (r["ADDRESS_TYPE"] != "R" and not overseas):
            continue
        out[region(r)] += 1
    return out


DEATH_CODES = {"old": ("01",), "new": ("11", "12")}


def removed_dead(rows, region, utc=True, codes="platform", reversals="all", census_day=False):
    """electors removed in the window because they had died, in the region of the address they were removed from; a
    removal reversed (by a reinstatement, or on the old platform by an enrolment pointing at it) was not a removal"""
    if reversals == "all":
        back = {r["REF_TXN"] for r in rows if r["STATUS"] == "A" and r["REF_TXN"] and r["TXN_TYPE"] in ("REI", "NEW")}
    elif reversals == "rei":
        back = {r["REF_TXN"] for r in rows if r["STATUS"] == "A" and r["REF_TXN"] and r["TXN_TYPE"] == "REI"}
    else:
        back = set()
    out = {c: 0 for c in W.CODES}
    for r in rows:
        if r["TXN_TYPE"] != "DEL" or r["STATUS"] != "A" or r["TXN_ID"] in back:
            continue
        if not in_window(local_time(r, utc), census_day):
            continue
        if codes == "platform":
            ok = r["REASON"] in DEATH_CODES["old" if old_platform(r) else "new"]
        elif codes == "current":
            ok = r["REASON"] in ("11", "12")
        else:
            ok = r["REASON"] in ("01", "11", "12")
        if ok:
            out[region(r)] += 1
    return out
