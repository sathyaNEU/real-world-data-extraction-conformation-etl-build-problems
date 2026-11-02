"""The clean truth of the Ardmuir University Library world, before any export is written.

Everything here is drawn from one seed. The lending platform is simulated event by event per title:
requests, holds, offers in the order holds were placed, loans, returns, cancellations whose rate rises
with how far down the queue a student stands, and metered licences lapsing at their fortieth loan.
"""
import datetime as dt
import heapq
import math
import random
from dataclasses import dataclass, field

import params as P

UTC = P.UTC


def uk_offset(t):
    """UK civil time offset from UTC at instant t (hours)."""
    if P.BST_2026_START <= t < P.BST_2026_END:
        return 1
    if t < P.BST_2025_END:
        return 1
    return 0


def to_uk(t):
    return t + dt.timedelta(hours=uk_offset(t))


def uk_local_to_utc(d, hh=0, mm=0):
    """A UK local wall-clock time on date d to UTC (no ambiguity for the times used)."""
    naive = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=UTC)
    # try BST first
    cand = naive - dt.timedelta(hours=1)
    if uk_offset(cand) == 1:
        return cand
    return naive


SCHOOLS = [
    # code, name, old faculty, students
    ("HIST", "History", "AH", 760), ("ENGL", "English Literature and Creative Writing", "AH", 690),
    ("PHIL", "Philosophy", "AH", 380), ("MLAN", "Modern Languages", "AH", 540),
    ("POLI", "Politics and International Relations", "SS", 880), ("ECON", "Economics", "SS", 1010),
    ("SOCI", "Sociology and Social Policy", "SS", 640), ("PSYC", "Psychology", "SS", 1180),
    ("EDUC", "Education", "SS", 520),
    ("ACFN", "Accounting and Finance", "BS", 1240), ("MGMT", "Management", "BS", 1420),
    ("MKTG", "Marketing", "BS", 610),
    ("LAWS", "Law", "LW", 1310), ("CRIM", "Criminology", "LW", 430),
    ("ENGN", "Engineering", "EN", 1530), ("COMP", "Computing Science", "EN", 1090),
    ("PHYS", "Physics and Astronomy", "PS", 520), ("CHEM", "Chemistry", "PS", 610),
    ("MATH", "Mathematics and Statistics", "PS", 740),
    ("BIOL", "Biological Sciences", "LS", 1130), ("BMSC", "Biomedical Sciences", "LS", 820),
    ("SPEX", "Sport and Exercise Science", "LS", 460),
    ("MEDI", "Medicine", "MD", 1360), ("DENT", "Dentistry", "MD", 410),
    ("NURS", "Nursing and Midwifery", "NH", 1150), ("AHPR", "Allied Health Professions", "NH", 560),
]


# titles a school owns that other schools' courses also list (owner: (probability, [(school, weight)]))
CROSS = {
    "ECON": (0.42, [("ACFN", 3), ("MGMT", 3), ("POLI", 1)]),
    "MATH": (0.40, [("ACFN", 2), ("ENGN", 2), ("COMP", 1), ("ECON", 1)]),
    "PSYC": (0.38, [("NURS", 3), ("AHPR", 2), ("MKTG", 2), ("EDUC", 1)]),
    "SOCI": (0.36, [("CRIM", 2), ("NURS", 2), ("LAWS", 1), ("POLI", 1)]),
    "POLI": (0.30, [("LAWS", 3), ("ECON", 1)]),
    "BIOL": (0.38, [("MEDI", 3), ("DENT", 1), ("BMSC", 1)]),
    "BMSC": (0.40, [("MEDI", 3), ("DENT", 2), ("NURS", 1)]),
    "CHEM": (0.25, [("MEDI", 2), ("BIOL", 1), ("DENT", 1)]),
    "PHIL": (0.28, [("LAWS", 2), ("POLI", 1)]),
    "HIST": (0.20, [("POLI", 1), ("LAWS", 1)]),
    "SPEX": (0.25, [("AHPR", 2), ("NURS", 1)]),
}


def new_faculty(old):
    for code, name, olds in P.FACULTIES:
        if old in olds:
            return code
    raise KeyError(old)


@dataclass
class Licence:
    lic_id: str
    title: int
    model: str            # "1U" perpetual, "1U-M" metered, "3U" perpetual (three concurrent)
    copies: int           # concurrent readers this line grants
    bought: dt.date
    po_line: str
    price_gbp: float
    remaining: list = field(default_factory=list)   # per copy, metered loans left
    lapsed_at: list = field(default_factory=list)   # per copy, UTC instant of lapse or None


@dataclass
class Hold:
    hold_id: str
    title: int
    student: int
    placed: dt.datetime
    status: str = "waiting"          # fulfilled / expired / cancelled_user / cancelled_system / waiting
    offered: dt.datetime = None
    borrowed: dt.datetime = None
    closed: dt.datetime = None


@dataclass
class Loan:
    loan_id: str
    title: int
    student: int
    start: dt.datetime
    days: int
    due: dt.datetime
    returned: dt.datetime
    hold_id: str = ""
    meter: tuple = None              # (licence id, copy index) a metered loan was counted against


class World:
    pass


def weekly_shape(rng):
    """Relative request intensity by week of a semester's demand window."""
    base = [0.55, 1.0, 0.95, 0.8, 0.6, 0.5, 0.45, 0.55, 0.62, 0.55, 0.42, 0.3, 0.22, 0.34, 0.44, 0.46, 0.40,
            0.28, 0.12]
    return [b * rng.uniform(0.85, 1.15) for b in base]


def build(seed=P.SEED):
    rng = random.Random(seed)
    W = World()
    W.schools = SCHOOLS
    W.school_old = {s[0]: s[2] for s in SCHOOLS}
    W.school_new = {s[0]: new_faculty(s[2]) for s in SCHOOLS}

    # students: id, school, group, graduates in 2026
    students = []
    sid = 0
    for code, name, old, n in SCHOOLS:
        for _ in range(n):
            g = rng.random()
            grp = "UG" if g < 0.70 else ("PGT" if g < 0.93 else "PGR")
            imp = rng.random() < P.BEHAVIOUR[old]["imp"]
            students.append(dict(id=sid, school=code, group=grp, imp=imp,
                                 leaves=rng.random() < (0.24 if grp == "UG" else 0.62)))
            sid += 1
    W.students = students
    by_school = {}
    for s in students:
        by_school.setdefault(s["school"], []).append(s["id"])
    W.by_school = by_school

    # titles: each owned by a school, some cross-listed
    titles = []
    tid = 0
    for code, name, old, n in SCHOOLS:
        k = max(14, int(round(n / 34.0 * rng.uniform(0.85, 1.15))))
        for _ in range(k):
            sem = rng.choices(["S26", "A", "both"], weights=[0.42, 0.33, 0.25])[0]
            cross = None
            aff = CROSS.get(code)
            if aff and rng.random() < aff[0]:
                cross = rng.choices([c for c, _ in aff[1]], weights=[x for _, x in aff[1]])[0]
            elif rng.random() < 0.08:
                same_fac = [c for c in by_school if W.school_old[c] == old and c != code]
                if same_fac:
                    cross = rng.choice(same_fac)
            pop = rng.lognormvariate(0.0, 0.62)
            titles.append(dict(id=tid, school=code, cross=cross, sem=sem, pop=pop))
            tid += 1
    W.titles = titles

    # licences, bought before the record or before the autumn 2026 semester
    lic = []
    lic_by_title = {}
    po = 410200
    for t in titles:
        beh = P.BEHAVIOUR[W.school_old[t["school"]]]
        exp_peak = t["pop"] * beh["demand"] * 3.0
        n = max(1, min(6, int(round(exp_peak * beh["copies"] * rng.uniform(0.55, 0.9)))))
        u = rng.random()
        model = "1U" if u < 0.55 else ("1U-M" if u < 0.9 else "3U")
        lines = []
        if model == "3U":
            nlines = max(1, int(round(n / 3.0)))
            for i in range(nlines):
                lines.append((3, dt.date(2024, rng.randint(1, 12), rng.randint(1, 28))))
        else:
            left = n
            while left > 0:
                q = min(left, rng.choice([1, 1, 1, 2, 2, 3]))
                y = rng.choice([2023, 2024, 2024, 2025])
                d = dt.date(y, rng.randint(1, 12), rng.randint(1, 28))
                if d > dt.date(2025, 8, 20):
                    d = dt.date(2025, 8, rng.randint(1, 20))
                lines.append((q, d))
                left -= q
        for q, d in sorted(lines, key=lambda x: x[1]):
            po += rng.randint(1, 37)
            unit = round(rng.uniform(58, 260) * (1.5 if model == "3U" else 1.0) * (0.8 if model == "1U-M" else 1.0), 2)
            L = Licence(lic_id="L%06d" % (po * 3 % 999983), title=t["id"], model=model, copies=q, bought=d,
                        po_line="POL-%d-%d" % (po, 1), price_gbp=unit)
            L.remaining = [P.METER_LOANS if model == "1U-M" else None for _ in range(q)]
            L.lapsed_at = [None for _ in range(q)]
            lic.append(L)
            lic_by_title.setdefault(t["id"], []).append(L)
    W.licences = lic
    W.lic_by_title = lic_by_title

    # requests per title per semester
    reqs = {t["id"]: [] for t in titles}
    for t in titles:
        beh = P.BEHAVIOUR[W.school_old[t["school"]]]
        for sname, start, weeks in P.SEMESTERS:
            active = (t["sem"] == "both") or (t["sem"] == "S26" and sname == "S26") or \
                     (t["sem"] == "A" and sname in ("A25", "A26"))
            if not active:
                continue
            shape = weekly_shape(rng)[:weeks]
            scale = t["pop"] * beh["demand"] * P.DEMAND_SCALE
            for w, f in enumerate(shape):
                lam = scale * f
                n = poisson(rng, lam)
                for _ in range(n):
                    day = start - dt.timedelta(days=start.weekday()) + dt.timedelta(days=7 * w + rng.randint(0, 6))
                    hh = rng.choices(range(24), weights=[1, .6, .4, .3, .2, .2, .4, 1, 2, 3.2, 3.6, 3.4, 3, 3.2, 3.4, 3.2,
                                                         2.9, 2.5, 2.3, 2.5, 2.8, 2.6, 2, 1.4])[0]
                    t0 = uk_local_to_utc(day, hh, rng.randint(0, 59)) + dt.timedelta(seconds=rng.randint(0, 59))
                    if t0 >= P.EXTRACT or t0 < P.RECORD_START:
                        continue
                    school = t["school"]
                    if t["cross"] and rng.random() < P.CROSS_SHARE:
                        school = t["cross"]
                    stu = rng.choice(by_school[school])
                    reqs[t["id"]].append((t0, stu))
    W.requests = reqs

    holds, loans = [], []
    hcount = [0]
    lcount = [0]
    for t in titles:
        simulate_title(W, t, rng, holds, loans, hcount, lcount)
    W.holds = holds
    W.loans = loans
    return W


def poisson(rng, lam):
    if lam <= 0:
        return 0
    if lam > 40:
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    L = math.exp(-lam)
    k, p = 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1


def simulate_title(W, t, rng, holds, loans, hcount, lcount):
    beh = P.BEHAVIOUR[W.school_old[t["school"]]]
    lics = sorted(W.lic_by_title.get(t["id"], []), key=lambda L: (L.bought, L.lic_id))
    # capacity changes: licences bought during the record (none here) and lapses
    capacity = sum(L.copies for L in lics if L.bought <= P.RECORD_START.date())
    pending_lic = [L for L in lics if L.bought > P.RECORD_START.date()]
    in_use = 0
    queue = []           # waiting holds, FIFO
    ev = []              # (time, seq, kind, payload)
    seq = [0]

    def push(time, kind, payload):
        seq[0] += 1
        heapq.heappush(ev, (time, seq[0], kind, payload))

    for (t0, stu) in sorted(W.requests[t["id"]]):
        push(t0, "req", stu)
    for L in pending_lic:
        push(dt.datetime(L.bought.year, L.bought.month, L.bought.day, 9, 0, tzinfo=UTC), "lic", L)
    sys_cancel = dt.datetime(2026, 7, 1, 2, 15, tzinfo=UTC)
    push(sys_cancel, "sys", None)
    d = dt.date(2025, 9, 1)
    while d < P.EXTRACT.date():
        push(uk_local_to_utc(d, 8, 0) + dt.timedelta(seconds=rng.randint(0, 900)), "email", None)
        d += dt.timedelta(days=7)

    active_by_student = set()
    lapsing = []

    def renew(L, time):
        k = len([x for x in W.licences if x.title == L.title]) + 1
        rn = Licence(lic_id="L%06d" % ((int(L.lic_id[1:]) * 7 + k * 131) % 999983), title=L.title, model="1U-M",
                     copies=1, bought=time.date(), po_line="AR-%s-%d" % (L.lic_id, k),
                     price_gbp=round(L.price_gbp * rng.uniform(1.0, 1.08), 2))
        rn.remaining = [P.METER_LOANS]
        rn.lapsed_at = [None]
        rn.renewal_of = L.lic_id
        return rn

    def meter_loan():
        for L in lics:
            if L.model != "1U-M":
                continue
            for i, r in enumerate(L.remaining):
                if L.lapsed_at[i] is None and r and r > 0:
                    L.remaining[i] = r - 1
                    return (L, i)
        return None

    def start_loan(time, stu, hold=None):
        nonlocal in_use
        lcount[0] += 1
        days = rng.choices([d for d, _ in P.LOAN_DAYS], weights=[w for _, w in P.LOAN_DAYS])[0]
        due = time + dt.timedelta(days=days)
        ret = due
        if rng.random() < P.P_EARLY_RETURN:
            ret = time + dt.timedelta(seconds=int(days * 86400 * rng.uniform(0.25, 0.9)))
        m = meter_loan()
        loan = Loan(loan_id="LN%07d" % lcount[0], title=t["id"], student=stu, start=time, days=days, due=due,
                    returned=ret, hold_id=hold.hold_id if hold else "", meter=(m[0].lic_id, m[1]) if m else None)
        loans.append(loan)
        if m and m[0].remaining[m[1]] == 0:
            lapsing.append((ret, m[0], m[1]))
        push(ret, "ret", (loan, m))

    def offer_heads(time):
        nonlocal in_use
        while queue and capacity - in_use > 0:
            h = queue.pop(0)
            h.offered = time
            in_use += 1
            if rng.random() < P.P_BORROW:
                delay = min(P.OFFER_HOURS * 3600 - 60, int(rng.expovariate(1 / 7.0) * 3600) + 120)
                push(time + dt.timedelta(seconds=delay), "borrow", h)
            else:
                push(time + dt.timedelta(hours=P.OFFER_HOURS), "expire", h)

    def hazard(pos, h):
        return beh["base"]

    def estimate_weeks(pos):
        """what the platform shows a student: place in the queue over copies, a week a loan"""
        return pos / max(1, capacity)

    def decide(time, h, pos, at_placement=False):
        """an impatient student weighs the shown estimate when placing a hold and at each Monday email"""
        if not W.students[h.student]["imp"]:
            return
        est = estimate_weeks(pos)
        k = P.IMPATIENT_PLACE if at_placement else P.IMPATIENT_EMAIL
        q = min(0.92, k * max(0.0, est - 1.0))
        if q > 0 and rng.random() < q:
            push(time + dt.timedelta(seconds=rng.randint(240, 6 * 3600)), "cancel", h)

    now = None
    while ev:
        nxt = ev[0][0]
        # competing cancellations among waiting holds
        if queue:
            hz = [hazard(i + 1, queue[i]) for i in range(len(queue))]
            tot = sum(hz)
            if tot > 0:
                gap_days = rng.expovariate(tot)
                tc = (now or nxt) + dt.timedelta(seconds=int(gap_days * 86400) + 1)
                if tc < nxt and tc < P.EXTRACT:
                    r = rng.random() * tot
                    acc = 0.0
                    for i, v in enumerate(hz):
                        acc += v
                        if acc >= r:
                            break
                    h = queue.pop(i)
                    h.status = "cancelled_user"
                    h.closed = tc
                    active_by_student.discard(h.student)
                    now = tc
                    continue
        time, _, kind, payload = heapq.heappop(ev)
        now = time
        if time >= P.EXTRACT:
            break
        if kind == "req":
            stu = payload
            if stu in active_by_student:
                continue
            if not queue and capacity - in_use > 0:
                in_use += 1
                start_loan(time, stu)
                active_by_student.add(stu)
            else:
                hcount[0] += 1
                h = Hold(hold_id="", title=t["id"], student=stu, placed=time)
                holds.append(h)
                queue.append(h)
                active_by_student.add(stu)
                decide(time, h, len(queue), at_placement=True)
        elif kind == "borrow":
            h = payload
            h.status = "fulfilled"
            h.borrowed = time
            h.closed = time
            in_use -= 1          # the reservation becomes a loan below
            in_use += 1
            start_loan(time, h.student, h)
            # start_loan does not add to in_use; the reserved copy carries the loan
        elif kind == "expire":
            h = payload
            h.status = "expired"
            h.closed = time
            in_use -= 1
            active_by_student.discard(h.student)
            offer_heads(time)
        elif kind == "ret":
            loan, m = payload
            in_use -= 1
            active_by_student.discard(loan.student)
            if m and m[0].remaining[m[1]] == 0 and m[0].lapsed_at[m[1]] is None:
                m[0].lapsed_at[m[1]] = time
                # the platform re-licenses a lapsed metered copy at once (auto-renewal on titles on current lists)
                rn = renew(m[0], time)
                lics.append(rn)
                W.licences.append(rn)
            offer_heads(time)
        elif kind == "lic":
            capacity += payload.copies
            offer_heads(time)
        elif kind == "email":
            for i, h in enumerate(list(queue)):
                decide(time, h, i + 1)
        elif kind == "cancel":
            h = payload
            if h in queue:
                queue.remove(h)
                h.status = "cancelled_user"
                h.closed = time
                active_by_student.discard(h.student)
        elif kind == "sys":
            keep = []
            for h in queue:
                if W.students[h.student]["leaves"]:
                    h.status = "cancelled_system"
                    h.closed = time
                    active_by_student.discard(h.student)
                else:
                    keep.append(h)
            queue[:] = keep
            offer_heads(time)
