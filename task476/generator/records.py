"""The utility's records as kept: the survey schedule, the survey finds, the odor-call log (UTC), the repair orders
with every visit, the GIS main segments, and for the asks the work-order cost lines, the service interruption tickets
and the meter premises. Built from truth.py; nothing here decides anything."""
import datetime as dt

import truth as T
import world as W

UTC_OFF = {False: 6, True: 5}     # Central standard and daylight offsets to UTC


def _dst(d):
    """US daylight time: second Sunday of March to first Sunday of November."""
    y = d.year
    m = dt.date(y, 3, 8)
    start = m + dt.timedelta(days=(6 - m.weekday()) % 7)
    n = dt.date(y, 11, 1)
    stop = n + dt.timedelta(days=(6 - n.weekday()) % 7)
    return start <= d < stop


def to_utc(t):
    return t + dt.timedelta(hours=UTC_OFF[_dst(t.date())])


STREETS = ["Abbott", "Barrow", "Cheshire", "Dalton", "Easton", "Fairmount", "Garland", "Hawley", "Ingram", "Jasper",
           "Kendall", "Larkin", "Merritt", "Newcomb", "Oakes", "Pembrook", "Quimby", "Rutledge", "Sexton", "Thayer",
           "Underhill", "Vance", "Whitcomb", "Yardley", "Alcott", "Bixby", "Corliss", "Danforth", "Emery", "Foss"]
SFX = ["St", "Ave", "Rd", "Pl", "Ct", "Ter"]


def street(s):
    r = T.rng_for("street", s.district, s.street)
    return "%s %s" % (STREETS[(s.street + sum(map(ord, s.district)) % 7) % len(STREETS)], SFX[int(r.integers(0, len(SFX)))])


def address(L):
    r = T.rng_for("addr", L.lid)
    return "%d %s" % (int(r.integers(1, 60)) * 20 + int(r.integers(0, 19)), street(L.seg))


def visits(L):
    """Repair-order visits: (local datetime, action, grade). A grade 3 is monitored about every six months until
    repaired; a grade 2 is checked once before repair when its repair waits more than 30 days."""
    out = []
    r = T.rng_for("visits", L.lid)
    g = L.grade
    if g == 2 and (L.repaired - L.found).days > 30:
        out.append((L.found + dt.timedelta(days=int(r.integers(10, 25)), hours=2), "CHECKED", 2))
    if g == 3:
        t = L.found + dt.timedelta(days=int(r.integers(150, 200)))
        while t < L.repaired and t.date() <= W.EXTRACT:
            out.append((t.replace(hour=int(r.integers(8, 15))), "MONITORED", 3))
            t = t + dt.timedelta(days=int(r.integers(150, 200)))
    if L.repaired.date() <= W.EXTRACT:
        out.append((L.repaired, "REPAIRED", g))
    return out


def grade_code(g, when):
    return "ABC"[g - 1] if when.year < 2025 else str(g)
