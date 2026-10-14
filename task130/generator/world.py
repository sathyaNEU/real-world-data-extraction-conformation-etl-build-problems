"""The payroll world: every clinician position at Corvane's four entities from January 2012 to September 2026, the
paid FTE each held month by month, the October 2026 moves, the 2026 HCM pay lines and the 2027 staffing plan.

A position is one employee in one job at one cost centre between two dates; a clinician with a dual appointment holds
two at once. Paid FTE in a month is the position's FTE, prorated in the months a position starts or ends and zero in
months of unpaid leave."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

import common as K

# Sept 2026 FTE by entity and job (before the October 2026 moves)
TARGET = {
    "TFH": dict(OBG=4.0, OBL=2.0, CNM=2.0, GSU=4.0, URO=2.0, ENT=2.0, ORT=4.0, EMR=16.0, ANE=7.0, CRNA=8.0, HOS=16.0,
                CCM=3.0, CAR=2.0, RAD=3.0, NP=9.0, PA=10.0, FAM=8.0, INT=4.0, RES=8.0),
    "AMC": dict(OBG=6.0, OBL=5.0, MFM=3.0, CNM=3.0, GSU=9.0, ORT=9.0, URO=5.0, ENT=4.0, VAS=4.0, EMR=30.0, ANE=22.0,
                CRNA=24.0, HOS=30.0, CCM=9.0, CAR=8.0, GAS=4.0, ONC=4.0, NEU=4.0, RAD=9.0, PSY=3.0, NP=26.0, PA=15.0,
                FAM=12.0, INT=16.0, PED=9.0, RES=42.0, FEL=10.0),
    "CMG": dict(FAM=120.0, INT=62.0, PED=34.0, OBG=26.0, MFM=2.0, CNM=10.0, CAR=18.0, VAS=3.0, GAS=14.0, ONC=14.0,
                NEU=10.0, PSY=14.0, PSYC=14.0, ORT=18.0, URO=8.0, ENT=8.0, GSU=8.0, NP=92.0, PA=60.0),
    "BCH": dict(GSU=3.0, ORT=2.0, EMR=11.0, ANE=3.0, CRNA=5.0, HOS=9.0, CAR=1.0, RAD=1.0, NP=10.0, PA=7.0),
}
GROWTH = 0.024                      # covered FTE growth a year, 2012 to 2026
FTE_MIX = {
    "hosp": ((1.0, .70), (0.9, .10), (0.8, .10), (0.6, .05), (0.5, .05)),
    "phys": ((1.0, .60), (0.9, .15), (0.8, .15), (0.6, .10)),
    "clin": ((1.0, .45), (0.9, .15), (0.8, .20), (0.7, .10), (0.6, .10)),
    "res": ((1.0, 1.0),),
}
LEAVE_RATE = {"hosp": 0.0058, "phys": 0.0050, "clin": 0.0075, "res": 0.0}
WORLD_MONTHS = K.months(K.WORLD_FIRST, K.HCM_LAST)


@dataclass
class Position:
    pid: str
    emp: str
    job: str
    entity: str
    dept: str
    fte: float
    start: dt.date
    end: dt.date | None = None           # last day worked
    primary: bool = True
    fte_changes: list = field(default_factory=list)     # (first month, new fte)
    leave: set = field(default_factory=set)              # (y, m) of unpaid leave
    hcm_profile: str = ""

    @property
    def cc(self):
        return K.cost_centre(self.entity, self.dept)

    def fte_in(self, y, m):
        f = self.fte
        for (yy, mm), new in self.fte_changes:
            if (y, m) >= (yy, mm):
                f = new
        return f

    def paid(self, y, m):
        """Paid FTE in month (y, m): zero outside the position, prorated in its first and last month."""
        first = dt.date(y, m, 1)
        dim = K.days_in_month(y, m)
        last = dt.date(y, m, dim)
        if self.start > last or (self.end is not None and self.end < first):
            return None
        if (y, m) in self.leave:
            return 0.0
        a = max(self.start, first)
        b = min(self.end, last) if self.end is not None else last
        days = (b - a).days + 1
        f = self.fte_in(y, m)
        if days == dim:
            return f
        return max(0.1, round(f * days / dim + 1e-9, 1))


def _target(entity, job, y, m):
    base = TARGET[entity].get(job, 0.0)
    if not base:
        return 0.0
    if job in ("RES", "FEL"):
        return base
    t = y + (m - 0.5) / 12.0
    if entity == "BCH":
        joined = K.ENTITIES["BCH"]["joined"]
        if dt.date(y, m, 1) < joined:
            return 0.0
        return base * math.exp(GROWTH * 0.6 * (t - 2026.71))
    return base * math.exp(GROWTH * (t - 2026.71))


def _draw_fte(rng, mix):
    vals, probs = zip(*FTE_MIX[mix])
    return float(vals[int(rng.choice(len(vals), p=probs))])


class World:
    def __init__(self):
        self.positions: list[Position] = []
        self._emp_seq = 104210
        self._pid_seq = 20480

    def new_emp(self, rng):
        self._emp_seq += int(rng.integers(1, 9))
        return "%06d" % self._emp_seq

    def new_pid(self, rng):
        self._pid_seq += int(rng.integers(1, 4))
        return "P%06d" % self._pid_seq


def _dept_for(rng, entity, job):
    opts = [d for d in K.DEPTS[entity] if job in d[2]]
    if entity == "BCH" and job == "FAM":
        raise ValueError("BCH family medicine opens in October 2026 only")
    if len(opts) == 1:
        return opts[0][0]
    # the first department holding the job carries most of it
    w = [3.0 if k == 0 else 1.0 for k in range(len(opts))]
    if entity == "CMG" and job in ("NP", "PA"):
        w = [2.0, 1.5, 1.2, 1.2, 1.0, 1.0, 0.6, 0.6, 0.6, 0.5, 0.6, 0.6, 0.6, 0.6][:len(opts)]
    w = [x / sum(w) for x in w]
    return opts[int(rng.choice(len(opts), p=w))][0]


def _profile(rng, job):
    profs = K.JOB[job][5]
    if len(profs) == 1:
        return profs[0][0]
    return profs[0][0] if rng.random() < 0.8 else profs[1][0]


def build():
    """Simulate every position month by month; returns the World."""
    W = World()
    rng = K.stream("roster")
    slots = [(e, j) for e in K.ENTITY_ORDER for j in TARGET[e] if j not in ("RES", "FEL")]
    active = {s: [] for s in slots}
    first_y, first_m = K.WORLD_FIRST
    for (y, m) in WORLD_MONTHS:
        dim = K.days_in_month(y, m)
        for (e, j) in slots:
            mix = K.JOB[j][6]
            # departures this month
            keep = []
            for p in active[(e, j)]:
                if rng.random() < LEAVE_RATE[mix]:
                    p.end = dt.date(y, m, int(rng.integers(1, dim + 1)))
                else:
                    keep.append(p)
            active[(e, j)] = keep
            # FTE changes and unpaid leave
            for p in keep:
                if rng.random() < 0.004:
                    nf = round(min(1.0, max(0.5, p.fte_in(y, m) + float(rng.choice([-0.2, -0.1, 0.1, 0.2])))), 1)
                    p.fte_changes.append(((y, m), nf))
                if rng.random() < 0.0012:
                    for k in range(int(rng.integers(1, 4))):
                        mm, yy = m + k, y
                        if mm > 12:
                            mm, yy = mm - 12, y + 1
                        p.leave.add((yy, mm))
            # hires up to the target
            target = _target(e, j, y, m)
            have = sum(p.fte_in(y, m) for p in active[(e, j)])
            start_world = (y, m) == (first_y, first_m)
            joining = e == "BCH" and dt.date(y, m, 1) == K.ENTITIES["BCH"]["joined"]
            while have < target - 0.45:
                f = _draw_fte(rng, mix)
                start = dt.date(y, m, int(rng.integers(1, dim + 1)))
                if start_world:
                    start = dt.date(y, m, 1) - dt.timedelta(days=int(rng.integers(30, 4000)))
                elif joining:
                    start = K.ENTITIES["BCH"]["joined"]
                p = Position(W.new_pid(rng), W.new_emp(rng), j, e, _dept_for(rng, e, j), f, start)
                p.hcm_profile = _profile(rng, j)
                W.positions.append(p)
                active[(e, j)].append(p)
                have += f
    # residents and fellows: cohorts on 1 July, three-year residencies and two-year fellowships
    rr = K.stream("trainees")
    for e, job, n_per_year, years in (("AMC", "RES", 14, 3), ("TFH", "RES", 3, 3), ("AMC", "FEL", 5, 2)):
        if job == "RES" and e == "TFH":
            first_cohort = 2018      # the family medicine residency took its first residents in July 2018
        else:
            first_cohort = 2009
        for cy in range(first_cohort, 2027):
            n = n_per_year if not (e == "TFH" and cy < 2020) else 2
            for _ in range(n):
                start = dt.date(cy, 7, 1)
                end = dt.date(cy + years, 6, 30)
                if end < dt.date(2012, 1, 1) or start > dt.date(2026, 9, 30):
                    continue
                p = Position(W.new_pid(rr), W.new_emp(rr), job, e, "6910", 1.0, start, end)
                p.hcm_profile = _profile(rr, job)
                if job == "RES" and cy + years - 1 <= 2026 and rr.random() < 0.3:
                    p.hcm_profile = "JP-40102" if rr.random() < 0.2 else p.hcm_profile
                W.positions.append(p)
    # clinicians join on the first of a month and leave at a month's end in September 2026, and nobody is on unpaid
    # leave that month
    for p in W.positions:
        if p.start.year == 2026 and p.start.month == 9:
            p.start = dt.date(2026, 9, 1)
        if p.end is not None and p.end.year == 2026 and p.end.month == 9:
            p.end = dt.date(2026, 9, 30)
        p.leave.discard((2026, 9))
    _dual_appointments(W)
    _historic_transfers(W)
    W.movers = _october_moves(W)
    W.by_emp = {}
    for p in W.positions:
        W.by_emp.setdefault(p.emp, []).append(p)
    return W


def _active_on(W, d, entity=None, job=None):
    out = []
    for p in W.positions:
        if p.start <= d and (p.end is None or p.end >= d):
            if (entity is None or p.entity == entity) and (job is None or p.job == job) and (d.year, d.month) not in p.leave:
                out.append(p)
    return out


def _dual_appointments(W):
    """A few specialists held a second position at another entity: CMG cardiologists, urologists and orthopaedic
    surgeons covering the hospitals' clinics and on-call rotas, and Alderwick radiologists reading for Brennick. The
    second positions closed when HCM went live on 1 January 2026: since then each clinician holds one position at the
    home entity and the other entity pays for the sessions under an intercompany services agreement."""
    rng = K.stream("dual")
    plan = [("CMG", "CAR", "TFH", "6530"), ("CMG", "CAR", "BCH", "6510"), ("CMG", "URO", "TFH", "6210"),
            ("CMG", "ORT", "BCH", "6210"), ("CMG", "GAS", "AMC", "6535"), ("AMC", "RAD", "BCH", "6550"),
            ("CMG", "ONC", "TFH", "6530"), ("AMC", "CAR", "CMG", "7510")]
    last = dt.date(2025, 12, 31)
    for k, (e, j, e2, dept2) in enumerate(plan):
        start = dt.date(2016 + k % 6, 1 + (3 * k) % 12, 1)
        if e2 == "BCH" and start < K.ENTITIES["BCH"]["joined"]:
            start = dt.date(2019, 9, 1) + dt.timedelta(days=61 * k)
        cands = [p for p in _active_on(W, start, e, j)
                 if p.end is None and p.fte_in(start.year, start.month) >= 0.9 and p.primary]
        cands.sort(key=lambda p: p.pid)
        p = cands[int(rng.integers(0, len(cands)))]
        split = 0.3 if k % 3 else 0.2
        before = p.fte_in(start.year, start.month)
        p.fte_changes.append(((start.year, start.month), round(before - split, 1)))
        q = Position(W.new_pid(rng), p.emp, j, e2, dept2, split, start, last, primary=False)
        q.hcm_profile = p.hcm_profile
        W.positions.append(q)
        p.fte_changes.append(((2026, 1), round(before, 1)))


def _historic_transfers(W):
    """Clinicians who changed entity before 2026: a hospitalist or emergency physician moving between the hospitals
    keeps the employee id and takes a new position."""
    rng = K.stream("transfers")
    moves = [("AMC", "HOS", "TFH", "6510", dt.date(2018, 3, 5)), ("TFH", "EMR", "AMC", "6310", dt.date(2019, 10, 14)),
             ("AMC", "NP", "TFH", "6610", dt.date(2021, 2, 1)), ("CMG", "FAM", "CMG", "7120", dt.date(2022, 5, 16)),
             ("AMC", "HOS", "BCH", "6510", dt.date(2023, 8, 7)), ("TFH", "CRNA", "AMC", "6410", dt.date(2024, 4, 22))]
    for e, j, e2, dept2, d in moves:
        cands = [p for p in _active_on(W, d, e, j) if p.end is None and p.primary]
        cands.sort(key=lambda p: p.pid)
        p = cands[int(rng.integers(0, len(cands)))]
        p.end = d - dt.timedelta(days=1)
        q = Position(W.new_pid(rng), p.emp, j, e2, dept2, p.fte_in(d.year, d.month), d)
        q.hcm_profile = p.hcm_profile
        W.positions.append(q)


def _october_moves(W):
    """1 October 2026: Tolliver Falls hospitalists into Alderwick's hospitalist group, two medical group family
    physicians into Brennick's new rural health clinic, Alderwick CRNAs into the medical group's ambulatory surgery
    centre, and a Brennick emergency physician to Tolliver Falls."""
    rng = K.stream("october")
    d = K.MOVE_DATE
    sept = dt.date(2026, 9, 15)
    out = []
    for e, j, n, e2, dept2 in (("TFH", "HOS", 3, "AMC", "6510"), ("CMG", "FAM", 2, "BCH", "7110"),
                               ("AMC", "CRNA", 4, "CMG", "7810"), ("BCH", "EMR", 1, "TFH", "6310")):
        cands = [p for p in _active_on(W, sept, e, j) if p.end is None and p.primary
                 and not any(q.emp == p.emp and q is not p for q in W.positions if q.end is None)]
        cands.sort(key=lambda p: p.pid)
        idx = rng.choice(len(cands), size=n, replace=False)
        for i in sorted(int(x) for x in idx):
            p = cands[i]
            p.end = d - dt.timedelta(days=1)
            q = Position(W.new_pid(rng), p.emp, j, e2, dept2, p.fte_in(2026, 9), d)
            q.hcm_profile = p.hcm_profile
            W.positions.append(q)
            out.append((p, q))
    return out


def position_months(W, first=K.WORLD_FIRST, last=K.HCM_LAST):
    """(position, y, m, paid FTE) for every month a position is held."""
    out = []
    for p in W.positions:
        for (y, m) in K.months(first, last):
            f = p.paid(y, m)
            if f is not None:
                out.append((p, y, m, f))
    return out


def home_entity(W, emp, on=K.HCM_RUN):
    """The employee's home entity as HCM holds it on a date: the entity of the primary position held then, or of the
    last primary position held."""
    held = [p for p in W.by_emp[emp] if p.primary]
    cur = [p for p in held if p.start <= on and (p.end is None or p.end >= on)]
    if cur:
        return cur[0].entity
    held.sort(key=lambda p: (p.end or dt.date(2100, 1, 1), p.pid))
    return held[-1].entity


def plan_2027(W):
    """The 2027 staffing plan: covered FTE by entity, class and month, built by Finance from the October 2026
    roster and the recruitment plan."""
    rng = K.stream("plan")
    oct_ = dt.date(2026, 10, 15)
    base = {}
    for p in W.positions:
        cls = K.CLASS_OF_JOB[p.job]
        if cls is None:
            continue
        if p.start <= oct_ and (p.end is None or p.end >= oct_):
            base[(p.entity, cls)] = base.get((p.entity, cls), 0.0) + p.fte_in(2026, 10)
    plan = {}
    for (e, cls), f in sorted(base.items()):
        level = round(f, 1)
        row = []
        for mth in range(1, 13):
            if rng.random() < 0.22:
                step = float(rng.choice([0.5, 0.8, 1.0, 1.0, 1.6, 2.0]) if f > 20 else rng.choice([0.4, 0.6, 1.0]))
                level = round(level + (step if rng.random() < 0.75 else -step / 2), 1)
            row.append(max(0.5, level))
        plan[(e, cls)] = row
    return plan
