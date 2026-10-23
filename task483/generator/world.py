"""task483 world: Larkspur Basin Community College's programs, their completers, what they earned and where they worked.

Degree and long-certificate programs. Each campus's completers in award years 2020-21 and 2021-22 earn, in the third
calendar year after the award year (2024 and 2025), as full-year workers round the campus's level for the program or
as part-year workers on a share of it. The state's education and workforce data center releases each campus x program
x cohort cell as its completers with earnings and their 10th, 25th, 50th, 75th and 90th percentile earnings, rounded to
the nearest 100 dollars in the measurement year's dollars; a cell under 10 completers with earnings is suppressed.

Short-term programs. Every Career Training Grant participant since July 2023 holds jobs (some from before the
program), each paid weekly or every two weeks on the Friday after the pay period closes; the state's unemployment
insurance wage records hold each employer's pay to each participant in each calendar quarter, an amended filing
superseding the original. A grant completer of July 2024 to June 2025 completes on the last day of their section.
Nothing in the pack states how a job's days sit inside a quarter.
"""
import datetime as dt
from math import log

import numpy as np

SEED = 483
D = dt.date
TD = dt.timedelta

BENCH = 34200                 # the board's 2025 benchmark, dollars
CPI_2425 = 1.0294             # CPI-U annual average 2025 over 2024, filed in the standard
PLACED_LINE = 70              # per cent of grant completers working on day 180
SHARE_LINE = 75               # per cent of 2024-25 completers in passing programs
MIN_DEGREE = 30               # completers with earnings across the two cohorts, released cells
MIN_SHORT = 20                # grant completers in the window
DAY = 180
WINDOW = (D(2024, 7, 1), D(2025, 6, 30))
WAGE_Q0, WAGE_Q1 = (2023, 3), (2026, 2)      # the wage extract's first and last calendar quarters
AS_OF = D(2026, 10, 16)
PS = (10, 25, 50, 75, 90)

PEOPLE = {"board": "Kathryn Petersen", "center": "Rodney Randall"}
SYSTEM = "Larkspur Basin Community College"
CAMPUS = {"A": "Fennimore", "B": "Ridgefield", "C": "Copper Flats", "D": "Antelope Springs"}
BOARD = "State Workforce Development Board"
CENTER = "State Education and Workforce Data Center"
GRANT = "Career Training Grant"


# ---------------------------------------------------------------------------------------------------------------------
# degree and long-certificate programs
# code: (name, CIP 2020, CIP 2010 in the 2025 edition, award, cells {campus: (n 2020-21, n 2021-22, full-year level
#        in 2025 dollars, full-year share)}, 2024-25 completers {campus: n})
DEGREE = {
    "RN": ("Registered Nursing", "51.3801", "51.3801", "AAS",
           {"A": (58, 61, 71000, .90), "B": (34, 36, 68000, .90), "C": (18, 20, 64000, .88)},
           {"A": 76, "B": 48, "C": 32}),
    "RAD": ("Radiologic Technology", "51.0911", "51.0911", "AAS",
            {"A": (22, 24, 62000, .90)}, {"A": 25}),
    "WLD": ("Welding Technology", "48.0508", "48.0508", "AAS",
            {"A": (26, 28, 52000, .86), "B": (20, 19, 47000, .84), "C": (14, 15, 41000, .80), "D": (11, 12, 39000, .80)},
            {"A": 29, "B": 23, "C": 15, "D": 13}),
    "DSL": ("Diesel Technology", "47.0605", "47.0605", "AAS",
            {"B": (21, 23, 50000, .86), "C": (16, 17, 44000, .84)}, {"B": 22, "C": 17}),
    "BUS": ("Business Administration", "52.0201", "52.0201", "AAS",
            {"A": (44, 47, 48000, .82), "B": (25, 27, 39500, .76), "C": (16, 15, 34500, .72), "D": (12, 13, 33000, .70)},
            {"A": 60, "B": 38, "C": 20, "D": 16}),
    "ECE": ("Child Development", "19.0709", "19.0709", "AAS",
            {"A": (30, 31, 31000, .72), "B": (19, 20, 29500, .70), "C": (12, 12, 28000, .68)},
            {"A": 31, "B": 20, "C": 13}),
    "MA": ("Medical Assisting", "51.0801", "51.0801", "C2",
           {"A": (38, 40, 50500, .52), "B": (20, 21, 48000, .52), "D": (30, 31, 30200, .98, .08)},
           {"A": 50, "B": 30, "D": 20}),
    "IT": ("Information Technology", "11.0901", "11.0103", "AAS",
           {"A": (28, 31, 52000, .84), "B": (15, 16, 45000, .80)}, {"A": 38, "B": 20}),
    "CJ": ("Criminal Justice", "43.0104", "43.0103", "AAS",
           {"A": (24, 25, 34000, .76), "B": (17, 18, 28500, .70), "C": (12, 12, 27000, .68)},
           {"A": 27, "B": 19, "C": 12}),
    "AUT": ("Automotive Technology", "47.0604", "47.0604", "AAS",
            {"A": (21, 22, 46000, .82), "B": (17, 16, 43500, .82), "C": (12, 13, 40000, .78)},
            {"A": 22, "B": 16, "C": 12}),
    "CUL": ("Culinary Arts", "12.0503", "12.0503", "AAS", {"A": (18, 19, 30500, .70)}, {"A": 21}),
    "PAR": ("Paralegal Studies", "22.0302", "22.0302", "C2", {"A": (8, 9, 41000, .80)}, {"A": 12}),
}
COHORTS = (("2020-21", 2024), ("2021-22", 2025))

# ---------------------------------------------------------------------------------------------------------------------
# short-term programs (under 600 clock hours)
# code: (name, CIP 2020, clock hours, weeks, sections [(campus, first end date, step weeks, count, participants per
#        section)], process: find (a new job after completing), search (mean days), late (share of finders who search
#        for four to five months, late_lo to late_hi days), onboard (the employers' start days), freq (pay period in
#        weeks), wage (weekly), leave (share of new hires who leave in a tenure cluster), leave_lo and leave_hi (the
#        cluster's tenure in days), stay (mean tenure of the rest), rehire and gap, gap0 (a further job after leaving),
#        incumbent (a job held through the program), inc_keep (kept long), inc_lo and inc_hi (days after completing an
#        incumbent job ends when not kept)
BASE = dict(late=0.0, late_lo=130, late_hi=156, gap0=3, incumbent=.10, inc_keep=.5, inc_lo=10, inc_hi=40, quit=0.0,
            quit_lo=130, quit_hi=152)
SHORT = {
    "CDL": ("Commercial Driver License, Class A", "49.0205", 160, 4,
            [("A", D(2024, 8, 16), 13, 4, 13), ("C", D(2024, 7, 5), 13, 4, 9)],
            dict(BASE, find=.94, search=8, onboard="monday", freq=1, wage=1180, leave=.34, leave_lo=125, leave_hi=140,
                 stay=1400, rehire=.82, gap=12, gap0=45, incumbent=.08, inc_keep=.3)),
    "CNA": ("Nursing Assistant", "51.3902", 120, 6,
            [("A", D(2024, 7, 26), 6, 9, 4), ("B", D(2024, 8, 9), 6, 8, 4), ("C", D(2024, 8, 23), 6, 8, 4)],
            dict(BASE, quit=.07, find=.93, search=18, late=.03, onboard="semimonthly", freq=2, wage=660, leave=.06, leave_lo=200,
                 leave_hi=260, stay=800, rehire=.60, gap=25, incumbent=.15, inc_hi=60)),
    "PHL": ("Phlebotomy Technician", "51.1009", 140, 8,
            [("A", D(2024, 8, 23), 13, 4, 3), ("B", D(2024, 8, 23), 13, 4, 3)],
            dict(BASE, find=.875, search=5, late=.14, late_lo=131, late_hi=154, onboard="monday", freq=1, wage=700,
                 leave=.14, leave_lo=184, leave_hi=194, stay=900, rehire=.0, gap=90)),
    "PHT": ("Pharmacy Technician", "51.0805", 300, 12,
            [("A", D(2024, 9, 20), 12, 4, 11)],
            dict(BASE, quit=.14, find=.92, search=30, late=.02, onboard="cohort4", freq=2, wage=730, leave=.05, leave_lo=200,
                 leave_hi=260, stay=900, rehire=.6, gap=30, incumbent=.12, inc_keep=.6, inc_hi=60)),
    "EMT": ("Emergency Medical Technician", "51.0904", 180, 14,
            [("B", D(2024, 8, 9), 17, 3, 11), ("C", D(2024, 12, 13), 17, 2, 11)],
            dict(BASE, quit=.12, find=.52, search=40, onboard="monday", freq=2, wage=820, leave=.20, leave_lo=40, leave_hi=110,
                 stay=800, rehire=.4, gap=40, incumbent=.20, inc_hi=60)),
    "WLF": ("Welding Fundamentals", "48.0508", 320, 10,
            [("B", D(2024, 8, 30), 10, 5, 6), ("D", D(2024, 9, 27), 10, 4, 6)],
            dict(BASE, quit=.07, find=.94, search=25, late=.02, onboard="monday", freq=1, wage=960, leave=.06, leave_lo=200,
                 leave_hi=260, stay=900, rehire=.6, gap=30, incumbent=.12, inc_hi=60)),
    "MCD": ("Medical Coding", "51.0713", 360, 12,
            [("A", D(2024, 9, 27), 12, 4, 8)],
            dict(BASE, quit=.12, find=.62, search=70, onboard="semimonthly", freq=2, wage=830, leave=.10, leave_lo=60, leave_hi=110,
                 stay=900, rehire=.4, gap=50, incumbent=.18, inc_hi=60)),
    "ITS": ("IT Support Specialist", "11.1006", 300, 10,
            [("A", D(2024, 9, 13), 10, 5, 6), ("B", D(2024, 10, 11), 10, 4, 6)],
            dict(BASE, quit=.14, find=.93, search=45, late=.02, onboard="semimonthly", freq=2, wage=860, leave=.05, leave_lo=200,
                 leave_hi=260, stay=900, rehire=.5, gap=40, incumbent=.18, inc_keep=.6, inc_hi=60)),
    "HVC": ("HVAC Fundamentals", "47.0201", 240, 8,
            [("B", D(2024, 8, 23), 8, 6, 7)],
            dict(BASE, quit=.07, find=.94, search=22, late=.02, onboard="monday", freq=1, wage=920, leave=.05, leave_lo=200,
                 leave_hi=260, stay=900, rehire=.6, gap=30, incumbent=.12, inc_hi=60)),
    "WHS": ("Warehouse and Logistics Technician", "52.0203", 80, 2,
            [("A", D(2024, 7, 19), 4, 13, 5), ("C", D(2024, 8, 2), 4, 12, 5)],
            dict(BASE, quit=.07, find=.95, search=8, late=.02, onboard="monday", freq=1, wage=690, leave=.10, leave_lo=200,
                 leave_hi=260, stay=600, rehire=.75, gap=20)),
    "FRK": ("Forklift and Material Handling", "49.0202", 40, 1,
            [("C", D(2024, 8, 2), 8, 5, 3)],
            dict(BASE, find=.58, search=15, onboard="monday", freq=1, wage=680, leave=.35, leave_lo=30, leave_hi=110,
                 stay=500, rehire=.4, gap=30, incumbent=.20)),
}
VARIANT = {"RN": 54, "RAD": 6, "WLD": 15, "DSL": 26, "BUS": 44, "ECE": 78, "MA": 73, "IT": 41, "CJ": 19, "AUT": 9,
           "CUL": 69}       # per-program seed variants, set by tuning


def seed(code, k):
    return SEED * 1000 + sum(ord(ch) * (i + 3) for i, ch in enumerate(code)) * 7 + k + 100003 * VARIANT.get(code, 0)


# ---------------------------------------------------------------------------------------------------------------------
# calendar
def qstart(d):
    return D(d.year, 3 * ((d.month - 1) // 3) + 1, 1)


def qnext(q):
    return D(q.year + (q.month == 10), 1 if q.month == 10 else q.month + 3, 1)


def qprev(q):
    return D(q.year - (q.month == 1), 10 if q.month == 1 else q.month - 3, 1)


def qend(q):
    return qnext(q) - TD(days=1)


def qlabel(q):
    return q.year, (q.month - 1) // 3 + 1


def onboard(day, rule):
    """the first start date an employer offers on or after day"""
    if rule == "monday":
        return day + TD(days=(7 - day.weekday()) % 7)
    if rule == "semimonthly":
        if day.day in (1, 16):
            return day
        if day.day < 16:
            return D(day.year, day.month, 16)
        return D(day.year + (day.month == 12), 1 if day.month == 12 else day.month + 1, 1)
    k = int(rule[6:])                       # a class of new hires every k weeks from an anchor Monday
    a = D(2023, 1, 9)
    n = -(-((day - a).days) // (7 * k))
    return a + TD(days=7 * k * max(n, 0))


# ---------------------------------------------------------------------------------------------------------------------
# degree half
def earnings(r, n, level, full_share, sigma=0.24):
    """annual earnings of n completers with earnings: full-year workers round the level, part-year on a share of it"""
    full = r.random(n) < full_share
    x = level * np.exp(r.normal(0.06, sigma, n))
    return np.round(np.where(full, x, x * r.uniform(0.18, 0.78, n)), 2)


def degree_cells(code):
    """[(campus, cohort, measurement year, n with earnings, unit earnings in measurement-year dollars, released
    percentiles or None if suppressed)]"""
    name, cip, cip10, award, cells, _ = DEGREE[code]
    r = np.random.default_rng(seed(code, 1))
    out = []
    for camp, cell in cells.items():
        n1, n2, level, fs = cell[:4]
        sg = cell[4] if len(cell) > 4 else 0.24
        for (coh, year), n in zip(COHORTS, (n1, n2)):
            lv = level / CPI_2425 if year == 2024 else level
            x = earnings(r, n, lv, fs, sg)
            q = None if n < 10 else tuple(int(round(v / 100.0)) * 100 for v in np.percentile(x, PS))
            out.append((camp, coh, year, n, x, q))
    return out


def in_2025(cell):
    """a released cell's percentiles in 2025 dollars"""
    camp, coh, year, n, x, q = cell
    f = CPI_2425 if year == 2024 else 1.0
    return n, tuple(v * f for v in q)


def cdf_cell(xv, q, how="lin"):
    """a cell's share of completers earning at or below xv, its released percentiles joined straight (in dollars, or in
    log dollars), held at 0 below half the 10th percentile and at 1 above 1.7 times the 90th"""
    pts = [0.45 * q[0]] + list(q) + [1.7 * q[-1]]
    ps = [0.0, .10, .25, .50, .75, .90, 1.0]
    if how == "log":
        return float(np.interp(log(xv), np.log(pts), ps))
    return float(np.interp(xv, pts, ps))


def pooled_median(cells, how="lin"):
    """the half point of the cells' rebuilt distributions pooled by completers with earnings"""
    cs = [in_2025(c) for c in cells if c[5] is not None]
    n = sum(c[0] for c in cs)
    if not n:
        return None
    lo, hi = 1000.0, 400000.0
    for _ in range(80):
        m = (lo + hi) / 2
        f = sum(c[0] * cdf_cell(m, c[1], how) for c in cs) / n
        lo, hi = (m, hi) if f < 0.5 else (lo, m)
    return (lo + hi) / 2


def averaged_median(cells):
    """the default path: the released cells' medians averaged by completers with earnings"""
    cs = [in_2025(c) for c in cells if c[5] is not None]
    if not cs:
        return None
    return sum(c[0] * c[1][2] for c in cs) / sum(c[0] for c in cs)


def lognormal_median(cells):
    """a log-normal fitted by least squares through each cell's five points, pooled"""
    from statistics import NormalDist
    z = [NormalDist().inv_cdf(p / 100) for p in PS]
    fits = []
    for c in cells:
        if c[5] is None:
            continue
        n, q = in_2025(c)
        b, a = np.polyfit(z, np.log(q), 1)
        fits.append((n, a, b))
    nn = sum(f[0] for f in fits)
    if not nn:
        return None
    lo, hi = 1000.0, 400000.0
    for _ in range(80):
        m = (lo + hi) / 2
        f = sum(k * NormalDist().cdf((log(m) - a) / b) for k, a, b in fits) / nn
        lo, hi = (m, hi) if f < 0.5 else (lo, m)
    return (lo + hi) / 2


def released_n(cells):
    return sum(c[3] for c in cells if c[5] is not None)


# ---------------------------------------------------------------------------------------------------------------------
# short-term half
def paychecks(r, st, en, freq, wage):
    """(pay date, amount) for each pay period of a job, paid on the Friday of the week after the period closes"""
    out = []
    p0 = st
    step = 7 * freq
    while p0 <= en:
        p1 = min(p0 + TD(days=step - 1), en)
        days = (p1 - p0).days + 1
        pay = p1 + TD(days=(4 - p1.weekday()) % 7 + 7)
        out.append((pay, round(wage * freq * days / step * (1 + r.normal(0, 0.02)), 2)))
        p0 = p1 + TD(days=1)
    return out


def quarterly(r, jobs):
    """{(employer, quarter start): pay}"""
    rec = {}
    for emp, st, en, wage, freq in jobs:
        for d, v in paychecks(r, st, en, freq, wage):
            k = (emp, qstart(d))
            rec[k] = round(rec.get(k, 0.0) + v, 2)
    return rec


def sections(code):
    """[(campus, first day, last day, participants)] of the sections that end in the window"""
    out = []
    for camp, first, step, count, per in SHORT[code][4]:
        for i in range(count):
            end = first + TD(weeks=step * i)
            if WINDOW[0] <= end <= WINDOW[1]:
                out.append((camp, end - TD(weeks=SHORT[code][3]) + TD(days=3), end, per))
    return out


def clear(jobs, d180, before=24, after=14):
    """a completer the records date: no job begins or ends in the 24 days before day 180 or the 14 days after it, and no
    job both begins and ends inside the quarter that holds it. Pay reaches a quarter a week or two after the work, so
    a start or exit dated from a quarter's pay lands up to about three weeks later than it was, or a few days earlier
    when the reference quarter held an extra pay day; the margins keep every such reading on the true side of day 180,
    with or without a correction for the pay lag"""
    q = qstart(d180)
    for _, st, en, _, _ in jobs:
        for ev in (st, en):
            gap = (ev - d180).days
            if -before <= gap <= after:
                return False
        if qstart(st) == q and qstart(en + TD(days=14)) == q:
            return False
    return True


def full_quarters(rec, e):
    """the quarters in which employer e paid the person and paid them in the quarters on both sides too"""
    return sorted(k for (ee, k) in rec if ee == e and (e, qprev(k)) in rec and (e, qnext(k)) in rec)


def ratio_status(rec, d180, ref="adjacent", shift=0, qlen=None):
    """the golden: a job paid in the quarter holding day 180 is running on that day when it was paid in the quarters on
    both sides, or when its start (paid in the next quarter, not the one before) or its exit (paid in the one before,
    not the next) dated from its pay there against its pay in a full quarter falls on the right side. The family: the
    full quarter is the adjacent one (ref "adjacent") or the mean of the job's full quarters ("mean"); the dated day is
    moved `shift` days earlier for the pay lag; the quarter is its own length in days or `qlen` days"""
    q = qstart(d180)
    ql = qlen or (qend(q) - q).days + 1
    on, undated = False, False
    for e in sorted({e for e, qq in rec if qq == q}):
        has = lambda k: (e, k) in rec
        if has(qprev(q)) and has(qnext(q)):
            on = True
            continue
        side = "start" if has(qnext(q)) else "exit" if has(qprev(q)) else None
        if side is None:
            undated = True
            continue
        adj = qnext(q) if side == "start" else qprev(q)
        far = qnext(adj) if side == "start" else qprev(adj)
        if not has(far):
            undated = True
            continue
        if ref == "mean":
            fq = full_quarters(rec, e)
            base = float(np.mean([rec[(e, k)] for k in fq])) if fq else rec[(e, adj)]
        elif ref == "two":                      # the adjacent quarter and the one beyond it, averaged
            base = (rec[(e, adj)] + rec[(e, far)]) / 2.0
        elif ref == "median":                   # the job's median quarter, partial quarters included
            base = float(np.median([v for (ee, k), v in rec.items() if ee == e and k != q]))
        else:
            base = rec[(e, adj)]
        frac = min(rec[(e, q)] / base, 1.0)
        if side == "start":
            day = qend(q) - TD(days=frac * ql) - TD(days=shift)
            on = on or day <= d180
        else:
            day = q + TD(days=frac * ql) - TD(days=shift)
            on = on or day >= d180
    return on, undated


FAMILY = [dict(ref=r, shift=sh, qlen=ql) for r in ("adjacent", "mean", "two", "median") for sh in (0, 7, 14)
          for ql in (None, 91)]


def dated_alike(rec, d180, truth):
    """every dating variant files the completer's true day-180 status"""
    return all(ratio_status(rec, d180, **f)[0] == truth for f in FAMILY)


def participants(code):
    """every grant participant of the program since July 2023: completers in the window (each with a record that dates
    their day 180), completers a year before it and a year after it, and those who left a section; each with jobs [(employer, start, end,
    weekly wage, weeks per pay period)] and the employer-quarter pay those jobs leave. The completers' paths (a job held
    through the program and kept or left, a new job found or not, found late, left in the cluster, a further job) are
    dealt in the program's shares; only a path's days are drawn again until the record dates day 180, and then again
    from the completer's own stream until every dating reading in FAMILY files the same day-180 status"""
    name, cip, hours, weeks, _, p = SHORT[code]
    r = np.random.default_rng(seed(code, 2))
    emps = ["%s%02d" % (code, k) for k in range(1, 31)]
    out = []
    secs = sections(code)
    early = [(camp, s - TD(weeks=52), e - TD(weeks=52), per) for camp, s, e, per in secs]
    later = [(camp, s + TD(weeks=52), e + TD(weeks=52), per) for camp, s, e, per in secs]
    idx = 0
    for kind, sec_list in (("window", secs), ("before", early), ("after", later)):
        seats = [(camp, s, e) for camp, s, e, per in sec_list for i in range(per + int(r.integers(0, 3)))]
        n_left = int(round(0.18 * len(seats)))
        left_set = set(int(i) for i in r.permutation(len(seats))[:n_left])
        paths = iter(path_quota(r, len(seats) - n_left, p))
        for i, (camp, s, e) in enumerate(seats):
            idx += 1
            left = i in left_set
            comp = e if not left else s + TD(days=int(r.integers(3, max(4, weeks * 7 - 3))))
            path = person_path(r, p) if left else next(paths)
            for attempt in range(4000):
                if attempt == 400 and path.get("quit"):
                    path = dict(path, quit=False)       # a fifth-month exit the quarters cannot date: kept on
                jobs = person_jobs(r, p, comp, emps, path)
                pr = np.random.default_rng([seed(code, 3), idx, attempt])
                rec = quarterly(pr, jobs)
                if kind != "window" or left:
                    break
                d180 = comp + TD(days=DAY)
                on, undated = ratio_status(rec, d180)
                if clear(jobs, d180) and not undated:
                    break
            else:
                raise RuntimeError("no clear record for %s path %s" % (code, path))
            if kind == "window" and not left and not dated_alike(rec, d180, truth_status(jobs, d180)):
                rr = np.random.default_rng([seed(code, 5), idx])     # its own stream, so no other path moves
                for attempt in range(4000):
                    jobs = person_jobs(rr, p, comp, emps, path)
                    rec = quarterly(np.random.default_rng([seed(code, 6), idx, attempt]), jobs)
                    if clear(jobs, d180) and not ratio_status(rec, d180)[1] and dated_alike(rec, d180,
                                                                                            truth_status(jobs, d180)):
                        break
                else:
                    raise RuntimeError("no record every dating reading agrees on for %s path %s" % (code, path))
            out.append(dict(code=code, kind=kind, left=left, campus=camp, section=(s, e),
                            completed=None if left else comp, exit_day=comp, jobs=jobs, rec=rec, path=path))
    return out


def _person(r, p, **flags):
    d = dict(inc=False, keep=False, found=False, late=False, leave=False, rehire=False, quit=False)
    d.update(flags)
    d.update(wage=float(p["wage"] * np.exp(r.normal(0, 0.12))), f_inc=int(r.choice([1, 2])), f_re=int(r.choice([1, 2])))
    return d


def path_quota(r, n, p):
    """n completers' paths in the program's shares, dealt in a shuffled order"""
    n_inc = int(round(n * p["incumbent"]))
    n_keep = int(round(n_inc * p["inc_keep"]))
    n_found = int(round((n - n_keep) * p["find"]))
    n_late = int(round(n_found * p["late"]))
    n_leave = int(round(n_found * p["leave"]))
    n_quit = int(round(n_found * p["quit"]))
    n_rehire = int(round(n_leave * p["rehire"]))
    rows = [dict(inc=True, keep=True)] * n_keep
    rest = n - n_keep
    inc_left = n_inc - n_keep
    kinds = (["leave_rehire"] * n_rehire + ["leave"] * (n_leave - n_rehire) + ["late"] * n_late + ["quit"] * n_quit
             + ["stay"] * (n_found - n_leave - n_late - n_quit) + ["none"] * (rest - n_found))
    order = r.permutation(len(kinds))
    for j, k in enumerate(order):
        f = dict(inc=j < inc_left)
        kind = kinds[int(k)]
        if kind != "none":
            f["found"] = True
        if kind == "late":
            f["late"] = True
        if kind == "quit":
            f["quit"] = True
        if kind.startswith("leave"):
            f["leave"] = True
            f["rehire"] = kind == "leave_rehire"
        rows.append(f)
    out = [_person(r, p, **f) for f in rows]
    return [out[int(i)] for i in r.permutation(len(out))]


def person_path(r, p):
    inc = r.random() < p["incumbent"]
    keep = inc and r.random() < p["inc_keep"]
    found = (not keep) and r.random() < p["find"]
    late = found and r.random() < p["late"]
    leave = found and not late and r.random() < p["leave"]
    rehire = leave and r.random() < p["rehire"]
    return _person(r, p, inc=inc, keep=keep, found=found, late=late, leave=leave, rehire=rehire)


def person_jobs(r, p, comp, emps, path):
    jobs = []
    used = set()
    wage = path["wage"]

    def pick(lo, hi):
        while True:
            e = emps[int(r.integers(lo, hi))]
            if e not in used:
                used.add(e)
                return e
    free = comp
    if path["inc"]:                              # a job held through the program
        st = comp - TD(days=int(r.integers(120, 900)))
        if path["keep"]:
            jobs.append((pick(20, 30), st, comp + TD(days=int(r.integers(420, 900))), round(wage * 0.85, 2),
                         path["f_inc"]))
            return jobs
        en = comp + TD(days=int(r.integers(p["inc_lo"], p["inc_hi"] + 1)))
        jobs.append((pick(20, 30), st, en, round(wage * 0.85, 2), path["f_inc"]))
        free = en
    if path["found"]:
        wait = int(r.integers(p["late_lo"], p["late_hi"] + 1)) if path["late"] else int(r.exponential(p["search"])) + 2
        st = onboard(max(free, comp) + TD(days=wait), p["onboard"])
        if path.get("quit"):                     # left in the fifth month after completing, before day 180
            en = max(st + TD(days=30), comp + TD(days=int(r.integers(p["quit_lo"], p["quit_hi"] + 1))))
            jobs.append((pick(0, 20), st, en, round(wage, 2), p["freq"]))
        elif path["leave"]:
            en = st + TD(days=int(r.integers(p["leave_lo"], p["leave_hi"] + 1)))
            jobs.append((pick(0, 20), st, en, round(wage, 2), p["freq"]))
            if path["rehire"]:
                s2 = onboard(en + TD(days=int(r.exponential(p["gap"])) + p.get("gap0", 3)), "monday")
                jobs.append((pick(0, 30), s2, s2 + TD(days=int(r.exponential(p["stay"])) + 200),
                             round(wage * 1.04, 2), path["f_re"]))
        else:
            jobs.append((pick(0, 20), st, st + TD(days=int(r.exponential(p["stay"])) + 200), round(wage, 2),
                         p["freq"]))
    return jobs


def truth_status(jobs, d180):
    return any(st <= d180 <= en for _, st, en, _, _ in jobs)


def routes(rec, comp):
    """each route's day-180 status for one completer: the golden (job pay ratio) and the easy ones"""
    d180 = comp + TD(days=DAY)
    q = qstart(d180)
    ql = (qend(q) - q).days + 1
    pos = (d180 - q).days
    emps = {e for e, _ in rec}
    paid = lambda e, k: (e, k) in rec
    out = {}
    out["ratio"] = ratio_status(rec, d180)[0]
    out["family"] = [ratio_status(rec, d180, **f)[0] for f in FAMILY]
    out["quarter"] = any(k == q for _, k in rec)
    out["q2_after"] = any(k == qnext(qnext(qstart(comp))) for _, k in rec)
    out["full_quarter"] = any(paid(e, qprev(q)) and paid(e, q) and paid(e, qnext(q)) for e in emps)
    out["end_of_quarter"] = any(paid(e, q) and paid(e, qnext(q)) for e in emps)
    out["start_of_quarter"] = any(paid(e, qprev(q)) and paid(e, q) for e in emps)
    out["pos_qwi"] = out["start_of_quarter"] if pos < ql / 2 else out["end_of_quarter"]
    pn = 1.0
    for e in emps:
        if not paid(e, q):
            continue
        b, a = paid(e, qprev(q)), paid(e, qnext(q))
        pn *= 1 - (1.0 if (a and b) else (pos / ql if a else ((1 - pos / ql) if b else 0.0)))
    out["prorate"] = 1 - pn
    qpay = sum(v for (e, k), v in rec.items() if k == q)
    for t in (500, 1000, 2500):
        out["min_%d" % t] = qpay >= t
    half = False
    for e in emps:
        if not paid(e, q):
            continue
        fulls = [rec[(e, k)] for k in (qprev(q), qnext(q)) if paid(e, k) and paid(e, qprev(k)) and paid(e, qnext(k))]
        if paid(e, qprev(q)) and paid(e, qnext(q)):
            half = True
        elif fulls and rec[(e, q)] >= 0.5 * max(fulls):
            half = True
    out["half_quarter"] = half
    tot = lambda k: sum(v for (e, kk), v in rec.items() if kk == k)
    if tot(q) <= 0:
        out["person_ratio"] = False
    elif tot(qprev(q)) > 0 and tot(qnext(q)) > 0:
        out["person_ratio"] = True
    elif tot(qnext(q)) > 0:
        out["person_ratio"] = qend(q) - TD(days=min(tot(q) / tot(qnext(q)), 1.0) * ql) <= d180
    elif tot(qprev(q)) > 0:
        out["person_ratio"] = q + TD(days=min(tot(q) / tot(qprev(q)), 1.0) * ql) >= d180
    else:
        out["person_ratio"] = False
    return out
