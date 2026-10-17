"""The random world of task464: the state's two grade 8 cohorts the grants count (spring 2025 on the retiring test,
spring 2026 on the new one) with their reading abilities, testing districts and schools, mobility to the October 2026
count day, every administration's scores and codes, the grades 6 and 7 rows of both springs, the spring 2026 bridge
study and the count day's arrivals with no state record. Seeded and deterministic; each component draws from its own
stream, so an ask's records never move the calibrated main population."""
import numpy as np

import world as W

SEED = 464
SD_WITHIN = 0.97                 # ability spread inside a district cohort
MOVE_RATE = 0.04                 # tested in another district, enrolled in this one on the count day
LEAVE_RATE = {2025: 0.030, 2026: 0.020}   # tested here and gone from the state's public schools by the count day
ARRIVE_RATE = 0.025              # enrolled on the count day with no state test record
REPEAT9 = 0.025                  # grade 8 in 2025 and still in grade 9 on the count day
REPEAT8 = 0.015                  # grade 8 in both 2025 and 2026
BRIDGE_SCHOOLS = 24
STREAMS = ("ability", "scores", "status", "ids", "mobility", "bridge", "schools", "lower", "asks", "arrivals")


CAP = 6000                       # draws reserved per district cohort, so a cohort's size moves no other student


def streams(seed):
    return {k: np.random.default_rng([seed, i]) for i, k in enumerate(STREAMS)}


def _rng(x, stream, *key):
    """A stream of its own for one district (and cohort): changing one district's size moves nobody else."""
    return np.random.default_rng([x["seed"], stream] + [int(k) for k in key])


def testing_codes():
    """The codes the 2025 and 2026 tests carry: the consolidated district's two predecessors in place of its own."""
    out = []
    for code, name, _, n10, n9, *_ in W.DISTRICTS:
        if code in W.MERGER:
            out += [(sub, share) for sub, _, share in W.MERGER[code]]
        else:
            out.append((code, 1.0))
    return out


def schools(x):
    """Each testing code's middle schools (grades 6 to 8) and each current district's high schools (grades 9 to 12)."""
    mid, high = {}, {}
    for code, name, _, n10, n9, *_ in W.DISTRICTS:
        rng = _rng(x, 6, code)
        cohort = (n10 + n9) / 2.0
        k = max(1, int(round(cohort / 380.0)))
        high[code] = ["%s%03d" % (code, v) for v in sorted(rng.choice(np.arange(600, 900), size=k, replace=False))]
        parts = W.MERGER.get(code, ((code, name, 1.0),))
        for sub, _, share in parts:
            k = max(1, int(round(cohort * share / 170.0)))
            mid[sub] = ["%s%03d" % (sub, v) for v in sorted(rng.choice(np.arange(200, 600), size=k, replace=False))]
    return mid, high


def tested_code(u, current):
    if current in W.MERGER:
        parts = W.MERGER[current]
        return parts[0][0] if u < parts[0][2] else parts[1][0]
    return current


def cohorts(x):
    """The 2025 and 2026 grade 8 cohorts, built from the districts they are enrolled in on the count day; movers tested
    elsewhere, leavers tested here and are gone. Each district and cohort draws from its own streams."""
    mid, high = x["mid"], x["high"]
    codes = [d[0] for d in W.DISTRICTS]
    w = np.array([d[3] + d[4] for d in W.DISTRICTS], float)
    w /= w.sum()
    out = []
    for code, name, _, n10, n9, mu10, mu9 in W.DISTRICTS:
        for cohort, n, mu in ((2025, n10, mu10), (2026, n9, mu9)):
            ra, rm = _rng(x, 1, code, cohort), _rng(x, 4, code, cohort)
            total = int(round(n / (1 - LEAVE_RATE[cohort])))
            th = ra.normal(mu + W.COHORT_SHIFT[cohort], SD_WITHIN, CAP)[:total]
            u = rm.random((CAP, 6))[:total]
            for k in range(total):
                s = dict(cohort=cohort, theta=float(th[k]), current=code, home=code, k=k)
                where = code
                if k >= n:
                    s["current"] = None
                elif u[k, 0] < MOVE_RATE:
                    others = [c for c in codes if c != code]
                    ww = np.array([w[codes.index(c)] for c in others])
                    where = others[int(np.searchsorted(np.cumsum(ww / ww.sum()), u[k, 1]))]
                s["tested_in"] = tested_code(u[k, 2], where)
                s["school8"] = mid[s["tested_in"]][int(u[k, 3] * len(mid[s["tested_in"]]))]
                if s["current"]:
                    s["high"] = high[code][int(u[k, 4] * len(high[code]))]
                    s["grade_now"] = 9 if (cohort == 2026 or u[k, 5] < REPEAT9) else 10
                s["repeat8"] = bool(cohort == 2026 and u[k, 5] < REPEAT8)
                out.append(s)
    return out


def score(test, theta, grade, z):
    """A reported scale score from ability and a standard normal measurement error: the new test reports any integer
    on its scale, the retiring test's fixed form reports the nearest score in its table."""
    p = W.OLD if test == "old" else W.NEW
    raw = p["mean"] + p["slope"] * (np.asarray(theta, float) + W.GRADE_SHIFT[grade]) + p["err"] * np.asarray(z, float)
    if test == "old":
        return W.glra_score(raw, grade)
    return np.clip(np.round(raw), p["lo"], p["hi"]).astype(int)


def scale(rng, test, theta, grade):
    return score(test, theta, grade, rng.normal(0, 1, np.shape(theta)))


def status(u, v):
    """One record's status as the vendor reports it, and whether an invalidated test was retaken in the make-up window."""
    st = "absent" if u < 0.024 else "exempt" if u < 0.031 else "invalid" if u < 0.039 else "scored"
    return st, bool(st == "invalid" and v < 0.5)


def records(x):
    """Every grade 8 (and the 2026 cohort's grade 7) administration of the two cohorts, with scores and codes; each
    district cohort's errors and statuses come from its own streams, one fixed slot per student."""
    groups = {}
    for s in x["students"]:
        groups.setdefault((s["home"], s["cohort"]), []).append(s)
    for (code, cohort), group in groups.items():
        Z = _rng(x, 2, code, cohort).normal(size=(CAP, 6))[:len(group)]
        U = _rng(x, 3, code, cohort).random((CAP, 4))[:len(group)]
        th = np.array([s["theta"] for s in group])
        g8_old, g8_new, g7_old = score("old", th, 8, Z[:, 0]), score("new", th, 8, Z[:, 1]), score("old", th, 7, Z[:, 2])
        for i, s in enumerate(group):
            recs = []
            if cohort == 2025:
                recs.append(dict(test="old", year=2025, grade=8, score=int(g8_old[i])))
            else:
                recs.append(dict(test="old", year=2025, grade=7 if not s["repeat8"] else 8,
                                 score=int(g7_old[i] if not s["repeat8"] else g8_old[i])))
                recs.append(dict(test="new", year=2026, grade=8, score=int(g8_new[i])))
            for m, r in enumerate(recs):
                r["status"], r["retake"] = status(U[i, 2 * m], U[i, 2 * m + 1])
                if r["status"] == "invalid" and r["retake"]:
                    r["retake_score"] = int(score(r["test"], s["theta"], r["grade"], Z[i, 3 + m]))
            s["records"] = recs
            s["bridge_z"] = float(Z[i, 5])


def _records_for(rng_z, rng_u, group, plan):
    """Scores and statuses for a group of students; plan(s) lists each record's (test, year, grade). Each student owns a
    fixed slot of draws, so a group's size moves no earlier student."""
    Z = rng_z.normal(size=(CAP, 6))[:len(group)]
    U = rng_u.random((CAP, 6))[:len(group)]
    for i, st in enumerate(group):
        recs = []
        for m, (test, year, grade) in enumerate(plan(st)):
            r = dict(test=test, year=year, grade=grade, score=int(score(test, st["theta"], grade, Z[i, m])))
            r["status"], r["retake"] = status(U[i, 2 * m], U[i, 2 * m + 1])
            if r["status"] == "invalid" and r["retake"]:
                r["retake_score"] = int(score(test, st["theta"], grade, Z[i, 3 + m]))
            recs.append(r)
        st["records"] = recs


def younger(x):
    """The two cohorts behind them: the 2027 cohort (grade 6 on the retiring test in 2025, grade 7 on the new test in
    2026) and the 2028 cohort (grade 6 on the new test in 2026), each in its testing code's middle schools."""
    out = []
    for code, name, _, n10, n9, mu10, mu9 in W.DISTRICTS:
        base, mu = (n10 + n9) / 2.0, mu9 + W.COHORT_SHIFT[2026]
        for cohort, f in ((2027, 1.02), (2028, 1.03)):
            rs = _rng(x, 11, code, cohort)
            n = int(round(rs.normal(base * f, base * 0.02)))
            th = rs.normal(mu, SD_WITHIN, CAP)[:n]
            u = _rng(x, 12, code, cohort).random((CAP, 4))[:n]
            group = []
            for k in range(n):
                where = tested_code(u[k, 0], code)
                st = dict(cohort=cohort, theta=float(th[k]), home=code, k=k, tested_in=where,
                          school=x["mid"][where][int(u[k, 1] * len(x["mid"][where]))])
                if cohort == 2027:
                    st["school6"] = st["school"] if u[k, 2] > 0.06 else x["mid"][where][int(u[k, 3] * len(x["mid"][where]))]
                group.append(st)
            plan = (lambda st: [("old", 2025, 6), ("new", 2026, 7)]) if cohort == 2027 else (lambda st: [("new", 2026, 6)])
            _records_for(_rng(x, 13, code, cohort), _rng(x, 14, code, cohort), group, plan)
            out += group
    return out


def nonpublic(x):
    """The nonpublic schools' test takers in both springs; the grade 8 students of each spring who now attend a public
    high school join the count-day students (their result is a state reading result like any other)."""
    x["np_only"] = []
    tested = {}
    for code, name, where, per, mu in W.NONPUBLIC:
        current = "1700" if where in ("1701", "1702") else where
        for cohort in (2025, 2026, 2027, 2028):
            rng = _rng(x, 20, code, cohort)
            n = int(round(per * rng.uniform(0.85, 1.15)))
            shift = W.COHORT_SHIFT.get(cohort, 0.0)
            th = rng.normal(mu + shift, SD_WITHIN, CAP)[:n]
            u = rng.random((CAP, 3))[:n]
            group = []
            for k in range(n):
                st = dict(cohort=cohort, theta=float(th[k]), home=None, k=k, tested_in=where, school=code,
                          school8=code, nonpublic=True, repeat8=False, current=None)
                if cohort in W.NONPUBLIC_ENROL and u[k, 0] < W.NONPUBLIC_ENROL[cohort]:
                    st["current"] = current
                    st["high"] = x["high"][current][int(u[k, 1] * len(x["high"][current]))]
                    st["grade_now"] = 10 if cohort == 2025 else 9
                group.append(st)
            plan = {2025: lambda st: [("old", 2025, 8)], 2026: lambda st: [("old", 2025, 7), ("new", 2026, 8)],
                    2027: lambda st: [("old", 2025, 6), ("new", 2026, 7)], 2028: lambda st: [("new", 2026, 6)]}[cohort]
            _records_for(_rng(x, 21, code, cohort), _rng(x, 22, code, cohort), group, plan)
            for st in group:
                st["bridge_z"] = 0.0
                (x["students"] if st["current"] else x["np_only"]).append(st)
    return x


BRIDGE_DRAW = 11                 # the bridge study's own draw of schools and testing order


def bridge(x, draw=None):
    """The spring 2026 bridge study: the grade 8 students of 24 middle schools drawn at random took the retiring test as
    well, in an order set by school; the SLM score is the student's operational score."""
    rng = np.random.default_rng([x["seed"], 50, BRIDGE_DRAW if draw is None else draw])
    public = set(v for vs in x["mid"].values() for v in vs)
    pool = sorted(set(s["school8"] for s in x["students"] if s["cohort"] == 2026 and s["school8"] in public))
    chosen = sorted(rng.choice(pool, size=BRIDGE_SCHOOLS, replace=False))
    first = {c: ("GLRA" if k % 2 == 0 else "SLM") for k, c in enumerate(rng.permutation(chosen))}
    rows = []
    for s in x["students"]:
        if s["cohort"] != 2026 or s["school8"] not in first or s.get("nonpublic"):
            continue
        r = s["records"][-1]
        if r["status"] != "scored":
            continue
        rows.append(dict(school=s["school8"], order=first[s["school8"]], new=r["score"],
                         old=int(score("old", s["theta"], 8, s["bridge_z"])), theta=s["theta"], student=s))
    return dict(schools=chosen, rows=rows)


def arrivals(x):
    """Grade 9 and 10 students enrolled this fall with no state test record (new to the state's public schools)."""
    out = []
    for code, name, _, n10, n9, *_ in W.DISTRICTS:
        rng = _rng(x, 9, code)
        for grade, n in ((9, n9), (10, n10)):
            for _ in range(int(rng.binomial(n, ARRIVE_RATE))):
                out.append(dict(current=code, grade_now=grade, records=[], arrival=True,
                                high=x["high"][code][int(rng.integers(len(x["high"][code])))]))
    return out


def upper(x):
    """Grades 11 and 12 on the October 2026 roll: the enrolment file's other rows (no test records in the folder)."""
    out = []
    for code, name, _, n10, n9, *_ in W.DISTRICTS:
        rng = _rng(x, 15, code)
        for grade, f in ((11, 0.94), (12, 0.90)):
            n = int(round(rng.normal(n10 * f, n10 * 0.02)))
            for _ in range(n):
                out.append(dict(current=code, grade_now=grade, records=[],
                                high=x["high"][code][int(rng.integers(len(x["high"][code])))]))
    return out


FIRST_DAY = {}                    # each district's first day of the 2026-27 school year (filled in enrolment)
TRANSFER_RATE = 0.012             # moved between districts in August or September, before the count day
LATE_RATE = 0.004                 # on the roll only after the count day (enrolled in October)
SEPT_LEAVE = 0.30                 # of those tested here and gone, the share who started the year and left in September


HOLIDAYS = {"2026-09-07"}           # Labor Day: no school


def _date(day, back=False):
    """A day of the 2026-27 school year (days from August 1) as a school day: a first day on the roll moves on to the
    next school day, a last day back to the one before."""
    import datetime as dt
    d = dt.date(2026, 8, 1) + dt.timedelta(days=int(day))
    while d.weekday() >= 5 or d.isoformat() in HOLIDAYS:
        d += dt.timedelta(days=-1 if back else 1)
    return d.isoformat()


def enrolment(x):
    """The October 2026 enrolment spells of grades 9 to 12: one spell per student and school, with entry and exit
    dates. Transfers between districts before the count day leave a closed spell in the first district; late entrants
    open theirs after it; some of the tested students now gone started the year and withdrew in September."""
    rng = x["rng"]["status"]
    codes = [d[0] for d in W.DISTRICTS]
    for code in codes:
        FIRST_DAY[code] = 16 + int(rng.integers(0, 11))          # 17 to 27 August
    spells = []
    people = [s for s in x["students"] if s.get("current")] + x["arrivals"] + x["upper"]
    for s in people:
        code = s["current"]
        u = rng.random(4)
        start = FIRST_DAY[code]
        s["late"] = bool(u[0] < LATE_RATE and "arrival" not in s)
        if s["late"]:
            start = 65 + int(u[1] * 25)                           # 5 to 29 October
        elif u[0] < LATE_RATE + TRANSFER_RATE:
            other = codes[int(u[2] * len(codes))]
            if other != code:
                leave = 33 + int(u[3] * 24)                       # 3 to 26 September
                spells.append(dict(sid=None, who=s, district=other, school=x["high"][other][0], grade=s["grade_now"],
                                   entry=_date(FIRST_DAY[other]), exit=_date(leave, back=True)))
                start = leave + 1 + int(u[1] * 4)
                s["transfer_from"] = other
        end = ""
        if s["grade_now"] in (11, 12) and u[2] > 0.986 and not s.get("transfer_from"):
            end = _date(33 + int(u[3] * 24), back=True)           # withdrew in September (left school)
        spells.append(dict(sid=None, who=s, district=code, school=s["high"], grade=s["grade_now"], entry=_date(start),
                           exit=end))
    for s in x["students"]:
        if s.get("current") is None and not s.get("nonpublic"):
            u = rng.random(3)
            if u[0] < SEPT_LEAVE:
                code = s["home"]
                g = 10 if s["cohort"] == 2025 else 9
                spells.append(dict(sid=None, who=s, district=code, school=x["high"][code][int(u[1] * len(x["high"][code]))],
                                   grade=g, entry=_date(FIRST_DAY[code]), exit=_date(33 + int(u[2] * 26), back=True)))
    # after the count day: October withdrawals and transfers (a later spell elsewhere), from a stream of their own so
    # the count-day roll above is untouched
    r2 = np.random.default_rng([x["seed"], 31])
    for sp in list(spells):
        if sp["exit"] or sp["entry"] > W.COUNT_DAY:
            continue
        u = r2.random(3)
        if u[0] < 0.011:
            last = 65 + int(u[1] * 21)                            # 5 to 25 October
            sp["exit"] = _date(last, back=True)
            sp["october"] = True
            if u[2] < 0.45:
                other = codes[int(u[2] / 0.45 * len(codes))]
                if other != sp["district"]:
                    spells.append(dict(sid=None, who=sp["who"], district=other, school=x["high"][other][-1],
                                       grade=sp["grade"], entry=_date(last + 1 + int((u[1] * 21) % 1 * 4)), exit="",
                                       after=True))
                    sp["moved_to"] = other
    x["spells"] = spells


def ids(x):
    """State student identifiers for everyone in the folder, and the retiring test's vendor test-taker numbers (a
    paper booklet scanned without its pre-ID label carries the test-taker number only)."""
    rng = x["rng"]["ids"]
    seen = set()
    people = x["students"] + x["younger"] + x["np_only"] + x["arrivals"] + x["upper"]
    for s in people:
        while True:
            v = int(rng.integers(1_000_000_000, 9_000_000_000))
            if v not in seen:
                break
        seen.add(v)
        s["sid"] = "%010d" % v
    tts = set()
    for s in x["students"] + x["younger"] + x["np_only"]:
        for r in s["records"]:
            if r["test"] != "old":
                continue
            while True:
                t = "CT25-%07d" % int(rng.integers(0, 10_000_000))
                if t not in tts:
                    break
            tts.add(t)
            r["tt"] = t
            r["sid_on_file"] = bool(rng.random() > 0.065)
    for sp in x["spells"]:
        sp["sid"] = sp["who"]["sid"]


def everything(seed=SEED):
    x = dict(rng=streams(seed), seed=seed)
    x["mid"], x["high"] = schools(x)
    x["students"] = cohorts(x)
    records(x)
    x["younger"] = younger(x)
    x["bridge"] = bridge(x)
    nonpublic(x)
    x["arrivals"] = arrivals(x)
    x["upper"] = upper(x)
    enrolment(x)
    ids(x)
    return x
