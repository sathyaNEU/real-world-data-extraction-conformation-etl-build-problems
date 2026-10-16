"""The 2026 season's housekeeping records, for the two tables from last August: the housekeeping app's task log and its
user list (as it stands in June 2027), the HR list of housekeeping staff (as it stands), Brennock's timesheets, the
payroll's overtime lines, the staff access system's badge events, reception's day-badge log, and the block's invoice.

The rooms are the extract's own 2026 stays, each given a room at check-in; every service is done by a named person on
the day; the true split of the work, the overtime and the block's billable hours are kept here as truth for checks.py,
and calc.py recomputes every figure from the files alone."""
from __future__ import annotations

import datetime as dt
import heapq
import math

import numpy as np

import cast as CA
import common as K

Y = 2026
WEEKS = K.roster_weeks(Y)
DAYS = [WEEKS[0][0] + dt.timedelta(days=i) for i in range(35)]           # Monday 27 July to Sunday 30 August 2026
BLOCK = WEEKS[2]                                                        # the block: Monday 10 to Sunday 16 August
BLOCK_DAYS = [BLOCK[0] + dt.timedelta(days=i) for i in range(7)]
ROOMS = [f * 100 + i for f in range(1, 9) for i in range(1, 61)]
RATE, RATE_SUN = 22.56, 28.20                                            # framework agreement 5.1 (2026 rates)
BOOKED = (dt.time(8, 0), dt.time(16, 0))
SENT_HOME_DAY = dt.date(2026, 8, 12)
LB_READER = "LB-02"

T = dt.timedelta


def at(d, h, m=0, s=0):
    return dt.datetime.combine(d, dt.time(0, 0)) + T(hours=h, minutes=m, seconds=s)


def utc(ldt):
    return K.local_to_utc(ldt)


def fmt(x):
    return x.strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------------------------------- people
class Person:
    __slots__ = ("name", "kind", "login", "emp", "bhs", "quota", "idx", "start", "left", "contract", "rate")

    def __init__(self, name, kind, login=None, emp=None, bhs=None, quota=14.8, idx=0, start=None, left=None,
                 contract="", rate=0.0):
        self.name, self.kind, self.login, self.emp, self.bhs = name, kind, login, emp, bhs
        self.quota, self.idx, self.start, self.left, self.contract, self.rate = quota, idx, start, left, contract, rate


def people():
    r = K.rng("people")
    crew = []
    for i, (nm, emp, start, contract, left) in enumerate(CA.CREW_2026):
        yrs = max(0, (dt.date(2026, 7, 1) - start).days // 365)
        crew.append(Person(nm, "crew", CA.login_of(nm), emp, None, float(r.uniform(13.9, 15.7)), i, start, left,
                           contract, K.round_dp(14.15 + min(yrs, 12) * 0.19, 2)))
    regs = [Person(nm, "reg", CA.login_of(nm), None, bhs, float(r.uniform(12.6, 14.2)), i)
            for i, (nm, bhs, _, _, _) in enumerate(CA.BRENNOCK_REGULARS)]
    block = [Person(nm, "block", "block%02d" % (i + 1), None, bhs, float(r.uniform(12.4, 13.8)), i)
             for i, (nm, bhs) in enumerate(CA.BLOCK_TEMPS)]
    day = [Person(nm, "day", None, None, bhs, float(r.uniform(11.4, 12.8)), i) for i, (nm, bhs) in
           enumerate(CA.DAY_TEMPS)]
    return crew, regs, block, day


def crew_on(p, d, leave):
    if p.start > d or (p.left is not None and d > p.left):
        return False
    w = d.weekday()
    o = p.idx % 7
    off = {o, (o + 1) % 7} | ({(o + 3) % 7} if "part-time" in p.contract else set())
    if w in off:
        return False
    if (p.name, d) in leave:
        return False
    return K.rng("sick", p.name, d.isoformat()).uniform() >= 0.022


def leave_days(crew):
    """Annual leave: taken before the festival's leave freeze (none from the Monday of the festival's first full week)."""
    r = K.rng("leave")
    out = set()
    perm = [p for p in crew if "Fixed" not in p.contract]
    for k, p in enumerate(r.permutation(len(perm))[:9]):
        p0 = perm[int(p)]
        first = dt.date(2026, 7, 20) + T(days=int(r.integers(0, 9)))
        for j in range(int(r.integers(5, 9))):
            d = first + T(days=j)
            if d < BLOCK[0]:
                out.add((p0.name, d))
    return out


def quota(p, d):
    if p.kind == "block" and d == SENT_HOME_DAY and p.idx == 6:
        return 4.0      # sent home at 10:00
    return p.quota


def regular_on(p, d):
    o = (p.idx * 2 + 3) % 7
    return d.weekday() not in (o, (o + 1) % 7)


def block_on(p, d):
    """Eight of the ten block temps a day; each has one or two days off in the week."""
    if not (BLOCK[0] <= d <= BLOCK[1]):
        return False
    i = (d - BLOCK[0]).days
    off = {0: (8, 9), 1: (0, 1), 2: (2, 3), 3: (4, 5), 4: (6, 7), 5: (8, 9), 6: (1, 4)}[i]
    return p.idx not in off


# ---------------------------------------------------------------------------------------------------- rooms
def assign_rooms(B):
    """Each 2026 summer stay that was occupied gets a room at check-in: the room free longest, as the front office
    allocates on arrival."""
    lo, hi = K.di(dt.date(2026, 7, 1)), K.di(dt.date(2026, 9, 12))
    stays = []
    for b in B:
        if b.los == 0 or b.status != "OUT" or b.a + b.los <= lo or b.a > hi:
            continue
        for j in range(b.rooms):
            stays.append((b.a, b.conf0 + j, b.a + b.los, b))
    stays.sort(key=lambda s: (s[0], s[1]))
    heap = [(0, rm) for rm in ROOMS]
    heapq.heapify(heap)
    occ = {}
    for a, conf, dep, b in stays:
        ff, rm = heapq.heappop(heap)
        assert ff <= a, "room plan over capacity"
        occ[conf] = (rm, a, dep, b)
        heapq.heappush(heap, (dep, rm))
    return occ


# ---------------------------------------------------------------------------------------------------- the season
class Task:
    __slots__ = ("tid", "d", "room", "ttype", "status", "who", "login", "start", "end", "insp_by", "insp",
                 "parent", "note", "created")


def largest_remainder(weights, total):
    w = np.array(weights, dtype=float)
    if total <= 0 or w.sum() <= 0:
        return [0] * len(w)
    x = w / w.sum() * total
    n = np.floor(x).astype(int)
    rem = int(total - n.sum())
    order = sorted(range(len(w)), key=lambda i: (-(x[i] - n[i]), i))
    for i in order[:rem]:
        n[i] += 1
    return [int(v) for v in n]


def season(B):
    crew, regs, block, dayt = people()
    leave = leave_days(crew)
    occ = assign_rooms(B)
    by_night = {}
    for conf, (rm, a, dep, b) in occ.items():
        for n in range(a, dep):
            by_night.setdefault(n, []).append((rm, conf, dep))
    tasks, ot, worked = [], [], []
    tid = 5204117
    day_pool = 0
    for d in DAYS:
        r = K.rng("hkday", d.isoformat())
        night = K.di(d) - 1
        jobs = []
        for rm, conf, dep in sorted(by_night.get(night, [])):
            if dep == K.di(d):
                jobs.append([rm, "Departure", "Completed"])
            else:
                u = K.rng("stay", d.isoformat(), rm).uniform()
                jobs.append([rm, "Stayover", "DND" if u < 0.031 else ("Refused" if u < 0.052 else "Completed")])
        service = [j for j in jobs if j[2] == "Completed"]
        on_c = [p for p in crew if crew_on(p, d, leave)]
        on_r = [p for p in regs if regular_on(p, d)]
        on_b = [p for p in block if block_on(p, d)]
        cap = sum(quota(p, d) for p in on_c + on_r + on_b)
        n_serv = len(service)
        on_d = []
        excess = n_serv - cap
        if excess >= 10:
            k = min(3, int(excess // 11.5))
            for _ in range(k):
                on_d.append(dayt[day_pool % len(dayt)])
                day_pool += 1
        straight = on_c + on_r + on_b + on_d
        qs = [quota(p, d) for p in straight]
        capall = sum(qs)
        if n_serv > capall:
            base = [int(math.floor(q)) for q in qs]
            extra_total = n_serv - sum(base)
            # the floor's rounding gives some rooms back to the shift; what is left goes to the crew as overtime
            spare = [q - math.floor(q) for q in qs]
            give = min(extra_total, int(round(sum(spare))))
            add = largest_remainder(spare, give)
            base = [b + a for b, a in zip(base, add)]
            ot_rooms = n_serv - sum(base)
            otl = [0] * len(on_c)
            order = list(r.permutation(len(on_c)))
            j = 0
            while ot_rooms > 0:
                i = int(order[j % len(on_c)])
                take = min(ot_rooms, int(r.integers(2, 6)))
                otl[i] += take
                ot_rooms -= take
                j += 1
            targets = base[:]
            for i in range(len(on_c)):
                targets[i] += otl[i]
        else:
            targets = largest_remainder(qs, n_serv)
            otl = [0] * len(on_c)
        # rooms by section: departures and stayovers spread across the floors, each attendant a run of rooms
        visits = sorted(jobs, key=lambda j: j[0])
        serv_idx = [i for i, j in enumerate(visits) if j[2] == "Completed"]
        owner = {}
        pos = 0
        for wi in [int(x) for x in r.permutation(len(straight))]:
            t = targets[wi]
            for i in serv_idx[pos:pos + t]:
                owner[i] = wi
            pos += t
        assert pos == len(serv_idx)
        for i, j in enumerate(visits):
            if i not in owner:      # a DND or refused room: the attendant whose run it sits in
                k = i
                while k >= 0 and k not in owner:
                    k -= 1
                if k < 0:
                    k = i
                    while k not in owner:
                        k += 1
                owner[i] = owner[k]
        tablet = None
        if r.uniform() < 0.42 and on_c:
            tablet = on_c[int(r.integers(0, len(on_c)))]
        for wi, p in enumerate(straight):
            mine = [visits[i] for i in range(len(visits)) if owner[i] == wi]
            mine.sort(key=lambda j: (0 if j[1] == "Stayover" else 1, j[0]))
            rr = K.rng("times", d.isoformat(), p.name)
            t = at(d, 8, 0) + T(minutes=float(rr.uniform(0, 7)))
            n_ot = otl[wi] if wi < len(on_c) else 0
            nominal = sum(43.0 if j[1] == "Departure" else (23.0 if j[2] == "Completed" else 2.0) for j in mine)
            ot_nom = sum(43.0 if j[1] == "Departure" else 23.0 for j in mine[len(mine) - n_ot:]) if n_ot else 0.0
            sc = min(1.0, 400.0 / max(1.0, nominal - ot_nom))
            done_break = False
            for k, (rm, ttype, status) in enumerate(mine):
                in_ot = n_ot and k >= len(mine) - n_ot
                if not done_break and t >= at(d, 12, 0):
                    t += T(minutes=30)
                    done_break = True
                if in_ot and t < at(d, 16, 0):
                    t = at(d, 16, 0) + T(minutes=float(rr.uniform(1, 6)))
                dur = (43.0 if ttype == "Departure" else 23.0) * (1.0 if in_ot else sc) if status == "Completed" \
                    else 2.0
                dur *= float(rr.uniform(0.86, 1.14))
                tk = Task()
                tk.tid, tk.d, tk.room, tk.ttype, tk.status = tid, d, rm, ttype, status
                tid += 1
                tk.who = p
                tk.start, tk.end = t, t + T(minutes=dur)
                tk.created = at(d, 5, 30) + T(seconds=int(rr.integers(0, 50)))
                tk.parent, tk.insp_by, tk.insp, tk.note = None, "", "", ""
                sup = "itrojanek" if d.weekday() >= 5 else ("sbohan" if mine[0][0] < 500 else "mahern")
                if p.kind == "day":
                    tk.login = sup
                    v = int(rr.integers(0, 4))
                    f = CA.first(p.name)
                    tk.note = ["Brennock - %s" % f, "Brennock temp %s" % f, "%s (Brennock)" % f,
                               "agency - %s" % f][v]
                elif tablet is p and tk.start >= at(d, 11, 30):
                    tk.login = sup
                    tk.note = "%s's rooms, tablet down" % CA.first(p.name)
                else:
                    tk.login = p.login
                tasks.append(tk)
                t = tk.end + T(minutes=float(rr.uniform(1, 3)))
            if wi < len(on_c) and n_ot:
                mins = (t - at(d, 16, 0)).total_seconds() / 60.0
                hrs = max(0.25, math.ceil(max(mins, 1.0) / 15.0) / 4.0)
                ot.append((p, d, hrs))
            worked.append((p, d, mine))
        # cover overtime (public areas, linen room, late rooms for arrivals): approved like any other
        rc = K.rng("cover", d.isoformat())
        have = {q.name for q, dd_, _ in ot if dd_ == d}
        for _ in range(int(rc.poisson(0.9))):
            cands = [q for q in on_c if q.name not in have]
            if cands:
                q = cands[int(rc.integers(0, len(cands)))]
                have.add(q.name)
                ot.append((q, d, float(rc.choice([0.75, 1.0, 1.25, 1.5, 1.75, 2.0]))))
    # inspections and re-cleans
    sups_wd = ["sbohan", "mahern"]
    extra = []
    for tk in tasks:
        if tk.status != "Completed":
            continue
        ri = K.rng("insp", tk.tid)
        pi = 0.36 if tk.ttype == "Departure" else 0.06
        if ri.uniform() >= pi:
            continue
        who = "itrojanek" if tk.d.weekday() >= 5 else sups_wd[0 if tk.room < 500 else 1]
        tk.insp_by = who
        fail = ri.uniform() < (0.07 if tk.ttype == "Departure" else 0.04)
        tk.insp = "Fail" if fail else "Pass"
        if fail:
            rc = Task()
            rc.d, rc.room, rc.ttype, rc.status, rc.who, rc.login = tk.d, tk.room, "Re-clean", "Completed", tk.who, \
                tk.login
            rc.created = tk.end + T(minutes=float(ri.uniform(15, 50)))
            rc.start = rc.created + T(minutes=float(ri.uniform(4, 25)))
            rc.end = rc.start + T(minutes=float(ri.uniform(9, 19)))
            rc.parent, rc.note, rc.insp_by, rc.insp = tk, tk.note, who, "Pass"
            extra.append(rc)
    allt = tasks + extra
    allt.sort(key=lambda x: (x.created, x.room, 0 if x.parent is None else 1))
    for i, x in enumerate(allt):
        x.tid = 5204117 + i
    # overtime outside the season (June to mid-September), a few hours a week
    r2 = K.rng("ot-outside")
    d = dt.date(2026, 6, 8)
    while d <= dt.date(2026, 9, 13):
        if not (DAYS[0] <= d <= DAYS[-1]) and r2.uniform() < 0.32:
            cands = [p for p in crew if crew_on(p, d, leave)]
            if cands:
                p = cands[int(r2.integers(0, len(cands)))]
                ot.append((p, d, float(r2.choice([0.75, 1.0, 1.25, 1.5, 2.0]))))
        d += T(days=1)
    return dict(tasks=allt, ot=ot, worked=worked, crew=crew, regs=regs, block=block, day=dayt, leave=leave, occ=occ)


# ---------------------------------------------------------------------------------------------------- truth
def truth_a(S):
    """Ask A on the clean truth: services done by the crew and by Brennock's people, by roster week, and the crew's
    overtime hours by the week worked."""
    out = {}
    for w, (m, s) in enumerate(WEEKS):
        rec = dict(crew_dep=0, crew_stay=0, brn_dep=0, brn_stay=0, ot=0.0)
        for tk in S["tasks"]:
            if not (m <= tk.d <= s) or tk.status != "Completed" or tk.ttype == "Re-clean":
                continue
            side = "crew" if tk.who.kind == "crew" else "brn"
            rec["%s_%s" % (side, "dep" if tk.ttype == "Departure" else "stay")] += 1
        rec["ot"] = sum(h for p, d, h in S["ot"] if m <= d <= s)
        out["W%d" % (w + 1)] = rec
    return out


# ---------------------------------------------------------------------------------------------------- access
def access(S):
    """Badge events at the staff entrance (SE-01 in, SE-02 out) and the loading bay door (LB-02), 1 to 31 August
    2026, for housekeeping, the porters and the agency's day badges. LB-02 was added in May 2026 and keeps its
    controller's clock (UTC); the entrance readers write local time."""
    rows, badges = [], []
    days = [dt.date(2026, 8, 1) + T(days=i) for i in range(31)]
    staff_badge = {}
    for i, p in enumerate(S["crew"]):
        staff_badge[p.name] = "S-%05d" % (10211 + i * 37)
    for i, (nm, _, _) in enumerate([CA.EXEC_HK] + list(CA.SUPERVISORS)):
        staff_badge[nm] = "S-%05d" % (10107 + i * 41)
    for i, p in enumerate(S["regs"]):
        staff_badge[p.name] = "T-%04d" % (812 + i * 3)
    porters = ["Darren Roache", "Calum Blake"]
    for i, nm in enumerate(porters):
        staff_badge[nm] = "S-%05d" % (10377 + i * 53)
    by_day = {}
    for p, d, mine in S["worked"]:
        by_day.setdefault(d, []).append((p, mine))
    task_end = {}
    for tk in S["tasks"]:
        k = (tk.who.name, tk.d)
        task_end[k] = max(task_end.get(k, tk.end), tk.end)
    for p, d, h in S["ot"]:
        k = (p.name, d)
        task_end[k] = max(task_end.get(k, at(d, 15, 0)), at(d, 16, 0) + T(hours=h))
    truth_b = {}
    sent = None
    for d in days:
        r = K.rng("access", d.isoformat())
        # reception's day badges: handed out from the pool in the order people arrive
        arrivals = []
        for p, mine in by_day.get(d, []):
            rr = K.rng("door", d.isoformat(), p.name)
            if p.kind in ("block", "day"):
                late = rr.uniform() < 0.16
                ent = at(d, 8, int(rr.integers(2, 13))) if late else at(d, 7, int(rr.integers(41, 59)))
            else:
                ent = at(d, 7, int(rr.integers(36, 58)))
            ent += T(seconds=int(rr.integers(0, 60)))
            arrivals.append((ent, p))
        if d in BLOCK_DAYS:
            lates = [e for e, p in arrivals if p.kind == "block" and e > at(d, 8, 0)]
            if not lates:      # the 07:52 bus from the depot is late one morning in five; make it so on this day
                bl = sorted([(e, p) for e, p in arrivals if p.kind == "block"], key=lambda x: x[1].idx)
                e0, p0 = bl[int(r.integers(0, len(bl)))]
                late = at(d, 8, int(r.integers(3, 11)), int(r.integers(0, 60)))
                arrivals = [(late if p is p0 else e, p) for e, p in arrivals]
        arrivals.sort(key=lambda x: (x[0], x[1].name))
        pool = list(range(1, 25))
        off = int(r.integers(0, 24))
        pool = pool[off:] + pool[:off]
        vi = 0
        dayb = {}
        for ent, p in arrivals:
            if p.kind in ("block", "day"):
                b = "V-%02d" % pool[vi % len(pool)]
                vi += 1
                dayb[p.name] = b
                badges.append(dict(date=d, badge=b, name=p.name, company="Brennock Hospitality Staffing",
                                   issued=ent - T(minutes=int(K.rng("rec", d.isoformat(), p.name).integers(2, 9))),
                                   by=CA.login_of(CA.RECEPTION[(d.toordinal() + vi) % 3])))
        # contractors and visitors on day badges too
        for j in range(int(r.integers(1, 5))):
            b = "V-%02d" % pool[vi % len(pool)]
            vi += 1
            co = ["Lift maintenance", "Linen supplier", "Fire safety inspection", "Interview", "Electrical contractor",
                  "Pest control"][int(r.integers(0, 6))]
            iss = at(d, int(r.integers(8, 15)), int(r.integers(0, 60)))
            badges.append(dict(date=d, badge=b, name=VISITORS[int(r.integers(0, len(VISITORS)))],
                               company=co, issued=iss, by=CA.login_of(CA.RECEPTION[j % 3]), visitor=True))
        lb_today = 0
        blk = sorted([p for e, p in arrivals if p.kind == "block"], key=lambda p: p.idx)
        lb_set = set()
        if blk:
            k = 2 + int(r.uniform() < 0.45)
            lb_set = {blk[int(i)].name for i in r.permutation(len(blk))[:k]}
        for ent, p in arrivals:
            rr = K.rng("door2", d.isoformat(), p.name)
            badge = dayb.get(p.name) or staff_badge[p.name]
            holder = ("Day badge %s" % badge) if p.kind in ("block", "day") else p.name
            rows.append((ent, "SE-01", badge, holder, "IN"))
            last = task_end.get((p.name, d), at(d, 15, 30))
            if p.kind == "block" and d == SENT_HOME_DAY and sent is None and p.idx == 6:
                sent = p
                ex = at(d, 10, 4, int(rr.integers(0, 50)))
                rows.append((ex, "SE-02", badge, holder, "OUT"))
                truth_b.setdefault(d, []).append((p, ent, ex, False))
                continue
            if rr.uniform() < 0.3:
                o = at(d, 12, int(rr.integers(5, 50)))
                rows.append((o, "SE-02", badge, holder, "OUT"))
                rows.append((o + T(minutes=int(rr.integers(9, 24)), seconds=int(rr.integers(0, 60))), "SE-01", badge,
                             holder, "IN"))
            end_floor = max(last + T(minutes=int(rr.integers(4, 12))), at(d, 16, 0) + T(minutes=int(rr.integers(1, 9))))
            if p.kind == "block" and last < at(d, 15, 40) and rr.uniform() < 0.1:
                end_floor = at(d, 15, int(rr.integers(46, 57)))
            use_lb = (p.name in lb_set) if p.kind == "block" else rr.uniform() < 0.18
            ex = end_floor + T(minutes=int(rr.integers(0, 14)), seconds=int(rr.integers(0, 60)))
            if use_lb:
                if p.kind == "block":
                    lb_today += 1
                rows.append((utc(ex), LB_READER, badge, holder, "OUT"))      # the controller's clock
            else:
                rows.append((ex, "SE-02", badge, holder, "OUT"))
            if p.kind == "block":
                truth_b.setdefault(d, []).append((p, ent, ex, use_lb))
        if d in BLOCK_DAYS:
            assert lb_today >= 1, d
        # porters through the loading bay (deliveries) and the entrance
        for nm in porters:
            rr = K.rng("porter", d.isoformat(), nm)
            if d.weekday() == 6 and nm == porters[1]:
                continue
            sec = lambda: int(rr.integers(0, 60))
            e = at(d, 6, int(rr.integers(40, 59)), sec())
            rows.append((e, "SE-01", staff_badge[nm], nm, "IN"))
            for k in range(int(rr.integers(2, 5))):
                tt = at(d, int(rr.integers(7, 15)), int(rr.integers(0, 60)), sec())
                rows.append((utc(tt), LB_READER, staff_badge[nm], nm, "OUT"))
                rows.append((utc(tt + T(minutes=int(rr.integers(4, 30)), seconds=sec())), LB_READER, staff_badge[nm],
                             nm, "IN"))
            rows.append((at(d, 15, int(rr.integers(2, 40)), sec()), "SE-02", staff_badge[nm], nm, "OUT"))
        # supervisors and the executive housekeeper
        for nm, emp, _ in list(CA.SUPERVISORS) + [CA.EXEC_HK]:
            wd = d.weekday()
            if (nm == "Inga Trojanek" and wd < 5 and wd not in (0, 1)) or (nm != "Inga Trojanek" and wd >= 5):
                continue
            rr = K.rng("sup", d.isoformat(), nm)
            rows.append((at(d, 7, int(rr.integers(15, 45)), int(rr.integers(0, 60))), "SE-01", staff_badge[nm], nm,
                         "IN"))
            rows.append((at(d, 16, int(rr.integers(10, 59)), int(rr.integers(0, 60))), "SE-02", staff_badge[nm], nm,
                         "OUT"))
    rows.sort(key=lambda x: (x[0], x[2]))
    return rows, badges, truth_b, staff_badge


VISITORS = ["Graham McElnay", "Keith Boles", "Darryl MacGinnity", "Brian Calvey", "Steven Foody", "Ruari Robertson",
            "Evan Scallan"]


def billable(ent, ex, d):
    """Framework agreement 4.1 to 4.3 for one booked 08:00 to 16:00 shift."""
    s = max(ent, at(d, 8, 0))
    e = min(ex, at(d, 16, 0))
    mins = max(0.0, (e - s).total_seconds() / 60.0)
    h = math.floor(mins / 15.0 + 1e-9) / 4.0
    if h > 6.0:
        h -= 0.5
    return max(h, 4.0)


def truth_bk(truth_b):
    out = {}
    for d in BLOCK_DAYS:
        hrs = sum(billable(ent, ex, d) for p, ent, ex, _ in truth_b[d])
        rate = RATE_SUN if d.weekday() == 6 else RATE
        out[d] = (hrs, K.round_dp(hrs * rate, 2))
    return out


# ---------------------------------------------------------------------------------------------------- files
def task_rows(S):
    rows = []
    for tk in S["tasks"]:
        rows.append([tk.tid, tk.d.isoformat(), tk.room, tk.ttype, tk.status, tk.login, fmt(utc(tk.created)),
                     fmt(utc(tk.start)) if tk.status == "Completed" else "",
                     fmt(utc(tk.end)), tk.insp_by, tk.insp, tk.parent.tid if tk.parent is not None else "", tk.note])
    return rows


TASK_COLS = ["task_id", "service_date", "room", "task_type", "status", "user_login", "created_utc", "started_utc",
             "closed_utc", "inspected_by", "inspection", "parent_task_id", "note"]
USER_COLS = ["login", "display_name", "user_group", "created", "last_login", "status"]


def user_rows(S):
    rows = []
    asof = dt.date(2027, 6, 28)
    for p in S["crew"]:
        created = max(p.start, CA.APP_LIVE)
        last = (p.left if p.left is not None else asof - T(days=int(K.rng("ll", p.name).integers(0, 3))))
        rows.append([p.login, p.name, "Housekeeping", created.isoformat(), last.isoformat(),
                     "Disabled" if p.left is not None else "Active"])
    for nm, emp, start in CA.SUPERVISORS:
        rows.append([CA.login_of(nm), nm, "Housekeeping Supervisors", max(start, CA.APP_LIVE).isoformat(),
                     (asof - T(days=1)).isoformat(), "Active"])
    rows.append([CA.login_of(CA.EXEC_HK[0]), CA.EXEC_HK[0], "Housekeeping Management", CA.APP_LIVE.isoformat(),
                 asof.isoformat(), "Active"])
    for nm, bhs, created, hired, emp in CA.BRENNOCK_REGULARS:
        if hired:
            rows.append([CA.login_of(nm), nm, "Housekeeping", created.isoformat(),
                         (asof - T(days=int(K.rng("ll", nm).integers(0, 3)))).isoformat(), "Active"])
        else:
            rows.append([CA.login_of(nm), nm, "Agency - Brennock", created.isoformat(),
                         dt.date(2026, 9, int(K.rng("ll", nm).integers(4, 12))).isoformat(), "Disabled"])
    for i, (nm, bhs) in enumerate(CA.BLOCK_TEMPS):
        rows.append(["block%02d" % (i + 1), "Brennock block %02d" % (i + 1), "Agency - Brennock", "2026-08-07",
                     "2026-08-16", "Disabled"])
    for nm, emp, start in CA.CREW_2027:
        rows.append([CA.login_of(nm), nm, "Housekeeping", start.isoformat(),
                     (asof - T(days=int(K.rng("ll", nm).integers(0, 3)))).isoformat(), "Active"])
    for nm, grp, created in CA.OTHER_USERS:
        rows.append([CA.login_of(nm), nm, grp, created.isoformat(),
                     (asof - T(days=int(K.rng("ll", nm).integers(0, 9)))).isoformat(), "Active"])
    rows.sort(key=lambda x: x[0])
    return rows


def hr_rows(S):
    """The HR system's housekeeping staff as at 28 June 2027 (current employees only)."""
    out = []
    asof = dt.date(2027, 6, 28)
    for p in S["crew"]:
        if p.left is not None and p.left < asof:
            continue
        out.append((p.emp, p.name, "Room Attendant", p.contract, p.start, 39 if "full" in p.contract else 24))
    for nm, bhs, created, hired, emp in CA.BRENNOCK_REGULARS:
        if hired:
            out.append((emp, nm, "Room Attendant", "Permanent full-time", hired, 39))
    for nm, emp, start in CA.CREW_2027:
        out.append((emp, nm, "Room Attendant", "Permanent full-time", start, 39))
    for nm, emp, start in CA.SUPERVISORS:
        out.append((emp, nm, "Floor Supervisor", "Permanent full-time", start, 39))
    out.append((CA.EXEC_HK[1], CA.EXEC_HK[0], "Executive Housekeeper", "Permanent full-time", CA.EXEC_HK[2], 39))
    out.sort(key=lambda x: x[1].split(" ", 1)[1] + " " + x[1].split(" ", 1)[0])
    return out


def pay_period(d):
    p1 = dt.date(2026, 1, 5)
    k = (d - p1).days // 14
    s = p1 + T(days=14 * k)
    return k + 1, s, s + T(days=13)


def payroll_rows(S):
    rows = []
    for p, d, h in S["ot"]:
        k, s, e = pay_period(d)
        k2, s2, e2 = pay_period(e + T(days=1))
        payd = e2 + T(days=5)
        rate = K.round_dp(p.rate * 1.5, 2)
        rows.append([p.emp, "%s, %s" % (p.name.split(" ", 1)[1], p.name.split(" ", 1)[0]), "Room Attendant",
                     "2026-%02d" % k2, s2.isoformat(), e2.isoformat(), payd.isoformat(), "Overtime 1.5",
                     "OT %s %sh" % (d.strftime("%d/%m/%y"), ("%.2f" % h).rstrip("0").rstrip(".") if h != int(h)
                                     else "%d" % h), "%.2f" % h, "%.2f" % rate, "%.2f" % K.round_dp(h * rate, 2), d])
    rows = [r for r in rows if 14 <= int(r[3][5:]) <= 19]
    rows.sort(key=lambda x: (x[3], x[1], x[-1]))
    return [r[:-1] for r in rows]


PAY_COLS = ["employee_no", "employee", "job_title", "pay_period", "period_start", "period_end", "pay_date", "element",
            "reference", "hours", "rate_eur", "amount_eur"]


def timesheet_rows(S):
    """Brennock's timesheets for the Weighhouse, weeks ending 26 July to 6 September 2026."""
    rows = []
    first = dt.date(2026, 7, 20)
    sup_name = {"sbohan": "Sinead Bohan", "itrojanek": "Inga Trojanek"}
    worked = {(p.name, d): p for p, d, _ in S["worked"] if p.kind != "crew"}
    d = first
    while d <= dt.date(2026, 9, 6):
        for p in S["regs"]:
            on = (p.name, d) in worked if DAYS[0] <= d <= DAYS[-1] else (regular_on(p, d) and d >= first)
            if on:
                rows.append((d, p, "Regular"))
        for p in S["block"]:
            if (p.name, d) in worked:
                rows.append((d, p, "Block"))
        for p in S["day"]:
            if (p.name, d) in worked:
                rows.append((d, p, "Day"))
        d += T(days=1)
    out = []
    for d, p, kind in rows:
        approver = "Inga Trojanek" if d.weekday() >= 5 else "Sinead Bohan"
        note = "Sent home by hotel 10:00" if (kind == "Block" and d == SENT_HOME_DAY and p.idx == 6) else ""
        out.append(dict(week_end=d + T(days=6 - d.weekday()), bhs=p.bhs, name=p.name, kind=kind, date=d,
                        start="08:00", end="16:00", brk=30, hours=7.5, approver=approver, note=note))
    return out


def invoice(S):
    """Brennock's invoice for the block: the booked shifts at the agreement's rates."""
    lines = []
    for d in BLOCK_DAYS:
        n = sum(1 for p in S["block"] if block_on(p, d))
        hrs = 7.5 * n
        rate = RATE_SUN if d.weekday() == 6 else RATE
        lines.append((d, n, hrs, rate, K.round_dp(hrs * rate, 2)))
    net = K.round_dp(sum(l[4] for l in lines), 2)
    vat = K.round_dp(net * 0.23, 2)
    return dict(no="BHS-INV-2026-0833", date=dt.date(2026, 8, 19), lines=lines, net=net, vat=vat,
                total=K.round_dp(net + vat, 2))
