"""task170 world: the people behind the records, drawn once from the seed.

Every hire carries two things the records never show together: a preference (to save in the plan or not, to keep
the income protection cover or not) and, for each benefit, the payroll month in which the hire first makes an active
choice about it. Until that month the benefit's default holds: under the plan's opt-in default the hire does not
contribute, under the cover's opt-out default the hire stays covered. The month of choice follows one law for every
hire and every benefit (a share choose at induction, before the first payroll's cut-off, the rest at a constant
monthly pace), whatever the default and whatever the preference."""
from __future__ import annotations

import numpy as np

import common as C

P_SAVE = 0.42            # share of hires who prefer to contribute to the plan
Q_DROP = 0.16            # share of hires who prefer to cancel the income protection cover
INDUCTION = 0.24         # share of hires who choose before the first payroll's cut-off
PACE = 6.0               # mean months to the choice for everyone else (exponential)
EARLY_LEAVERS = 0.22     # share of hires on short tenures
EARLY_MEAN, STAY_MEAN = 8.0, 110.0

RATES = np.array([1, 2, 3, 4, 5, 6, 7, 8, 10])
RATE_W = np.array([0.03, 0.07, 0.26, 0.12, 0.14, 0.22, 0.04, 0.07, 0.05])

HIRES_PER_MONTH = {"VCS": 84, "RDH": 45, "ASK": 37, "OSV": 32, "BRB": 27, "LDM": 22}
STOCK = {"VCS": 2900, "RDH": 1450, "ASK": 1200, "OSV": 1030, "BRB": 880, "LDM": 700}
GRADE_MIX = {
    "VCS": [0.13, 0.17, 0.20, 0.18, 0.13, 0.10, 0.06, 0.03],
    "RDH": [0.15, 0.19, 0.21, 0.17, 0.12, 0.09, 0.05, 0.02],
    "ASK": [0.16, 0.19, 0.21, 0.17, 0.12, 0.08, 0.05, 0.02],
    "OSV": [0.17, 0.20, 0.21, 0.16, 0.11, 0.08, 0.05, 0.02],
    "BRB": [0.18, 0.20, 0.21, 0.16, 0.11, 0.08, 0.04, 0.02],
    "LDM": [0.19, 0.21, 0.21, 0.15, 0.10, 0.08, 0.04, 0.02],
}
FTE = np.array([1.0, 0.8, 0.75, 0.6, 0.5])
FTE_W = np.array([0.62, 0.16, 0.10, 0.06, 0.06])
REHIRE = 0.05            # share of leavers rehired later at the same hospital
SECOND_POST = 0.06       # share of staff holding a bank post beside their main post


def choice_month(rng, n):
    """The payroll month (1 = the first) from which a hire's first active choice applies."""
    induct = rng.random(n) < INDUCTION
    t = rng.exponential(PACE, n)
    return np.where(induct, 1, np.floor(t).astype(int) + 1)


def tenure(rng, n):
    """Months on the payroll (1 = leaves at the end of the first month)."""
    early = rng.random(n) < EARLY_LEAVERS
    t = np.where(early, rng.exponential(EARLY_MEAN, n), rng.exponential(STAY_MEAN, n))
    return np.floor(t).astype(int) + 1


def draw_rates(rng, n):
    return rng.choice(RATES, n, p=RATE_W)


def spells(seed=C.SEED):
    """Every employment spell from January 2019 to October 2026: the stock in post in January 2019 and every hire
    after it, rehires as new spells. One dict per spell, months as integer indices (C.mindex)."""
    rng = np.random.default_rng(seed)
    first, last = C.mindex(C.HIST_START), C.mindex(C.LAST_PAYROLL)
    out = []
    emp = [100000]

    def new_no():
        emp[0] += int(rng.integers(1, 4))
        return emp[0]

    # the stock: staff in post on 1 January 2019, hired between 1990 and 2018
    for h in C.H_CODES:
        n = STOCK[h]
        start = first - rng.integers(1, 29 * 12, n)
        member = rng.random(n) < 0.47
        rate = draw_rates(rng, n)
        left_after = np.floor(rng.exponential(150.0, n)).astype(int) + 1    # months from January 2019
        late_join = rng.random(n) < 0.004 * 12 * 3                           # a few join after 2019 on their own
        late_when = rng.integers(0, last - first + 1, n)
        grade = rng.choice(C.GRADES, n, p=GRADE_MIX[h])
        fte = rng.choice(FTE, n, p=FTE_W)
        join_m = np.where(member, start + rng.integers(0, 60, n), -1)
        join_m = np.where(member, np.minimum(join_m, first - 1), join_m)
        for i in range(n):
            j = int(join_m[i]) if member[i] else (first + int(late_when[i]) if late_join[i] else None)
            end = first + int(left_after[i]) - 1
            out.append(dict(emp=new_no(), hosp=h, start=int(start[i]), end=end, grade=str(grade[i]), fte=float(fte[i]),
                            stock=True, save=bool(member[i] or late_join[i]), join=j, rate=int(rate[i]),
                            drop=False, cancel=None, spell=1))
    # the hires, January 2019 to October 2026
    for h in C.H_CODES:
        for m in range(first, last + 1):
            n = int(rng.poisson(HIRES_PER_MONTH[h]))
            if n == 0:
                continue
            save = rng.random(n) < P_SAVE
            drop = rng.random(n) < Q_DROP
            a_pen = choice_month(rng, n)
            a_ipc = choice_month(rng, n)
            L = tenure(rng, n)
            rate = draw_rates(rng, n)
            grade = rng.choice(C.GRADES, n, p=GRADE_MIX[h])
            fte = rng.choice(FTE, n, p=FTE_W)
            for i in range(n):
                end = m + int(L[i]) - 1
                join = m + int(a_pen[i]) - 1 if (save[i] and a_pen[i] <= L[i]) else None
                cancel = m + int(a_ipc[i]) - 1 if (drop[i] and a_ipc[i] <= L[i]) else None
                out.append(dict(emp=new_no(), hosp=h, start=m, end=end, grade=str(grade[i]), fte=float(fte[i]),
                                stock=False, save=bool(save[i]), join=join, rate=int(rate[i]), drop=bool(drop[i]),
                                cancel=cancel, spell=1, a_pen=int(a_pen[i]), a_ipc=int(a_ipc[i]), L=int(L[i])))
    # rehires: a share of leavers come back to the same hospital 3 to 24 months later as a new spell
    extra = []
    for s in out:
        if s["end"] < last - 3 and rng.random() < REHIRE:
            m = s["end"] + int(rng.integers(3, 25))
            if m > last or m < first:
                continue
            save, drop = rng.random() < P_SAVE, rng.random() < Q_DROP
            a_pen, a_ipc = int(choice_month(rng, 1)[0]), int(choice_month(rng, 1)[0])
            L = int(tenure(rng, 1)[0])
            extra.append(dict(emp=s["emp"], hosp=s["hosp"], start=m, end=m + L - 1, grade=s["grade"], fte=s["fte"],
                              stock=False, save=save, join=(m + a_pen - 1) if (save and a_pen <= L) else None,
                              rate=int(draw_rates(rng, 1)[0]), drop=drop,
                              cancel=(m + a_ipc - 1) if (drop and a_ipc <= L) else None, spell=s["spell"] + 1,
                              a_pen=a_pen, a_ipc=a_ipc, L=L))
    out.extend(extra)
    # a bank post beside the main post for a share of staff in post at the cutover
    for s in out:
        s["second_fte"] = 0.0
        if s["end"] >= C.mindex(C.DEDUCT_START) and rng.random() < SECOND_POST:
            s["second_fte"] = float(rng.choice([0.1, 0.15, 0.2]))
    return out


PLAN_PEAK, PLAN_BASE = 1.06, 0.98     # requisitions a month against the 2019 to 2026 intake: January, August and September


def plan_2027(seed=C.SEED + 7, peak=None, base=None):
    """The approved 2027 requisitions: hospital, start month (1 to 12), grade, FTE."""
    rng = np.random.default_rng(seed)
    reqs = []
    for h in C.H_CODES:
        for m in range(1, 13):
            mult = (PLAN_PEAK if peak is None else peak) if m in (1, 8, 9) else (PLAN_BASE if base is None else base)
            n = int(rng.poisson(HIRES_PER_MONTH[h] * mult))
            grade = rng.choice(C.GRADES, n, p=GRADE_MIX[h])
            fte = rng.choice(FTE, n, p=FTE_W)
            for i in range(n):
                reqs.append(dict(hosp=h, month=m, grade=str(grade[i]), fte=float(fte[i])))
    return reqs
