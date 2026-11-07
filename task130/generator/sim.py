"""Simulate Redbud's workforce day by day from July 2021 to September 2026: crews and their members, technicians,
hours by type, injuries, the reporting choice each crew makes under the recognition programme, its 90-day
milestones and payouts. Returns the truth (every injury) and the records (what reached the log and the payroll)."""
import datetime as dt
import hashlib

import numpy as np

import world as W

ONE = dt.timedelta(days=1)


def _rng(*keys):
    h = hashlib.blake2b(("|".join(str(k) for k in (W.SEED,) + keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "little"))


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += ONE


def is_holiday(d, cache={}):
    if d.year not in cache:
        cache[d.year] = W.holidays(d.year)
    return d in cache[d.year]


def mutual_aid_window(d):
    for a, b, share in W.MUTUAL_AID:
        if a <= d <= b:
            return (a, share)
    return None


def build_units():
    """Crews and technicians with their codes, types, districts and own rates. Thirty Piedmont crews move to Lakes
    at the March 2025 reorganisation and are recoded; their streaks carry over."""
    rng = _rng("units")
    crews, techs = [], []
    serial = {}
    for t, spec in W.CREW_TYPES.items():
        for dist in W.DISTRICTS:
            for _ in range(spec["n"][dist]):
                k = (dist, t)
                serial[k] = serial.get(k, 0) + 1
                code = "%s-%s-%03d" % (W.DCODE[dist], t, serial[k])
                mult = float(np.exp(rng.normal(0, W.CREW_SIGMA) - W.CREW_SIGMA ** 2 / 2))
                crews.append(dict(code=code, type=t, district=dist, size=spec["size"], rate=spec["rate"] * mult,
                                  code_new=None, district_new=None))
    # the reorganisation: Piedmont's overhead, underground and vegetation crews in the old Oconee area move to Lakes
    moved = [c for c in crews if c["district"] == "Piedmont" and c["type"] in ("OH", "UG", "VEG")]
    pick = sorted(rng.choice(len(moved), 30, replace=False))
    for i in pick:
        c = moved[i]
        k = ("Lakes", c["type"])
        serial[k] = serial.get(k, 0) + 1
        c["code_new"] = "%s-%s-%03d" % ("LK", c["type"], serial[k])
        c["district_new"] = "Lakes"
    for t, spec in W.TECH_TYPES.items():
        for dist in W.DISTRICTS:
            for j in range(spec["n"][dist]):
                mult = float(np.exp(rng.normal(0, W.TECH_SIGMA) - W.TECH_SIGMA ** 2 / 2))
                techs.append(dict(team="%s-%s" % (W.DCODE[dist], t), type=t, district=dist, rate=spec["rate"] * mult))
    return crews, techs


def crew_code(c, d):
    return c["code_new"] if (c["code_new"] and d >= W.RENAME) else c["code"]


def crew_district(c, d):
    return c["district_new"] if (c["district_new"] and d >= W.RENAME) else c["district"]


def staff(crews, techs):
    """Employees in each crew slot over time: leavers replaced by new hires, and transfers that swap two members of
    crews of the same type in the same district. Returns slot timelines and the assignment rows."""
    rng = _rng("staff")
    next_id = [100100]

    def new_emp():
        next_id[0] += int(rng.integers(1, 4))
        return "E%06d" % next_id[0]
    slots = {}
    current = {}
    for ci, c in enumerate(crews):
        for s in range(c["size"]):
            slots[(ci, s)] = [(W.BURN0, new_emp())]
            current[(ci, s)] = slots[(ci, s)][0][1]
    horizon = W.HIST1
    events = []
    # leavers: about 9 per cent a year per slot, each replaced by a new hire
    for key in sorted(slots):
        t = W.BURN0
        while True:
            t = t + dt.timedelta(days=int(rng.exponential(365 / 0.09)) + 1)
            if t > horizon:
                break
            events.append((t, 0, key, key))
    # transfers: about 6 per cent a year of slots swap with a slot of a same-type crew, one in four of them across
    # districts
    by_group, by_type = {}, {}
    for ci, c in enumerate(crews):
        by_group.setdefault((c["district"], c["type"]), []).append(ci)
        by_type.setdefault(c["type"], []).append(ci)
    n_swaps = int(0.06 * len(slots) * ((horizon - W.BURN0).days / 365))
    groups = sorted(by_group)
    types = sorted(by_type)
    for _ in range(n_swaps):
        if rng.random() < 0.25:
            members = by_type[types[int(rng.integers(len(types)))]]
        else:
            members = by_group[groups[int(rng.integers(len(groups)))]]
        a, b = (int(x) for x in rng.choice(members, 2, replace=False))
        sa, sb = int(rng.integers(crews[a]["size"])), int(rng.integers(crews[b]["size"]))
        when = W.BURN0 + dt.timedelta(days=int(rng.integers(30, (horizon - W.BURN0).days)))
        events.append((when, 1, (a, sa), (b, sb)))
    events.sort()
    for when, kind, k1, k2 in events:
        if kind == 0:
            e = new_emp()
            slots[k1].append((when, e))
            current[k1] = e
        else:
            ea, eb = current[k1], current[k2]
            slots[k1].append((when, eb))
            slots[k2].append((when, ea))
            current[k1], current[k2] = eb, ea
    for key in slots:
        last = {}
        for t, e in slots[key]:
            last[t] = e
        slots[key] = sorted(last.items())
    tech_ids = []
    for ti, t in enumerate(techs):
        tech_ids.append(new_emp())
    return slots, tech_ids


def who(timeline, d):
    e = timeline[0][1]
    for t, emp in timeline:
        if t <= d:
            e = emp
        else:
            break
    return e


def p_report(day):
    if day < W.HIDE_FROM:
        return 1.0
    if day >= W.HIDE_FULL:
        return W.P_REPORT_END
    return 1.0 - (1.0 - W.P_REPORT_END) * (day - W.HIDE_FROM) / (W.HIDE_FULL - W.HIDE_FROM)


def simulate():
    crews, techs = build_units()
    slots, tech_ids = staff(crews, techs)
    rng = _rng("days")
    injuries = []          # every injury that happened, with whether it reached the log
    exposure = np.zeros(W.MILESTONE)   # Pinewater crew hours by cycle day, 2022 onwards
    milestones = []        # (crew index, date the 90th clean day ended, members paid)
    weekly = {}            # (unit code, week start) -> hours by type
    mix = [m for m, _ in W.CASE_MIX]
    pmix = [p for _, p in W.CASE_MIX]

    def add_week(code, district, utype, d, kind, h):
        # keyed by the biweekly pay period the day falls in and the district the hours were worked in
        wk = W.HIST0 + dt.timedelta(days=14 * ((d - W.HIST0).days // 14))
        rec = weekly.setdefault((code, wk, district), dict(district=district, type=utype, regular=0.0, overtime=0.0,
                                                            pto=0.0, holiday=0.0, mutual_aid=0.0, member_days=0))
        rec[kind] += h

    for ci, c in enumerate(crews):
        start = W.BURN0 - dt.timedelta(days=int(rng.integers(0, W.MILESTONE)))
        cyc = start
        aid_today = {}
        for a, b, share in W.MUTUAL_AID:
            aid_today[a] = rng.random() < (share if c["type"] in ("OH", "VEG") else share / 3)
        sup_today = {}
        for a, b, target, sources, share in W.SUPPORT:
            sup_today[a] = (crew_district(c, a) in sources and c["type"] in ("OH", "VEG", "UG")
                            and rng.random() < share)
        for d in days(W.BURN0, W.HIST1):
            if d == W.HIST0:
                cyc = d            # HR-14 Revision 2: every crew's count starts afresh on 11 January 2021
            code, dist = crew_code(c, d), crew_district(c, d)
            work_dist = dist
            for a, b, target, sources, share in W.SUPPORT:
                if a <= d <= b and sup_today[a]:
                    work_dist = target
            day_no = (d - cyc).days
            wd = d.weekday() < 5 and not is_holiday(d)
            ma = mutual_aid_window(d)
            on_aid = bool(ma and aid_today[ma[0]])
            present = 0
            hours = 0.0
            pto_h = 0.0
            if wd or on_aid:
                for s in range(c["size"]):
                    if not on_aid and rng.random() < W.PTO_SHARE:
                        pto_h += 8.0
                    else:
                        present += 1
                per = W.DAY_HOURS * (1.25 if on_aid else 1.0) * float(np.clip(rng.normal(1.0, 0.06), 0.8, 1.2))
                hours = present * per
            elif d.weekday() >= 5 and rng.random() < W.WEEKEND_CALLOUT:
                present = c["size"]
                hours = present * W.CALLOUT_HOURS
            if is_holiday(d) and d.weekday() < 5 and not on_aid:
                add_week(code, dist, c["type"], d, "holiday", 8.0 * c["size"])
            if pto_h:
                add_week(code, dist, c["type"], d, "pto", pto_h)
            if hours:
                if on_aid:
                    add_week(code, dist, c["type"], d, "mutual_aid", hours)
                else:
                    reg = min(hours, present * 8.0)
                    add_week(code, work_dist, c["type"], d, "regular", reg)
                    add_week(code, work_dist, c["type"], d, "overtime", hours - reg)
            if d >= W.HIST0 and not on_aid:
                exposure[day_no] += hours
            lam = c["rate"] * hours / W.RATE_BASE * (W.MUTUAL_AID_RISK if on_aid else 1.0)
            reset = False
            for _ in range(int(rng.poisson(lam)) if hours else 0):
                cls = mix[int(rng.choice(3, p=pmix))]
                p = 1.0 if cls == "DA" else p_report(day_no)
                rep = bool(rng.random() < p) and not reset
                if reset:
                    rep = True
                emp = who(slots[(ci, int(rng.integers(c["size"])))], d)
                injuries.append(dict(unit="crew", ci=ci, code=code, district=dist, type=c["type"], emp=emp, date=d,
                                     cls=cls, reported=rep, cycle_day=day_no, mutual_aid=on_aid,
                                     work_district=work_dist))
                if rep:
                    reset = True
            # first aid cases: logged in full, never hidden, no effect on the streak
            for _ in range(int(rng.poisson(lam * W.FIRST_AID_PER_RECORDABLE)) if hours else 0):
                emp = who(slots[(ci, int(rng.integers(c["size"])))], d)
                injuries.append(dict(unit="crew", ci=ci, code=code, district=dist, type=c["type"], emp=emp, date=d,
                                     cls="FA", reported=True, cycle_day=day_no, mutual_aid=on_aid,
                                     work_district=work_dist))
            if reset:
                cyc = d + ONE
            elif day_no == W.MILESTONE - 1:
                members = [who(slots[(ci, s)], d) for s in range(c["size"])]
                milestones.append(dict(ci=ci, code=code, district=dist, type=c["type"], date=d, members=members))
                cyc = d + ONE
    for ti, t in enumerate(techs):
        emp = tech_ids[ti]
        for d in days(W.BURN0, W.HIST1):
            wd = d.weekday() < 5 and not is_holiday(d)
            if is_holiday(d) and d.weekday() < 5:
                add_week(t["team"], t["district"], t["type"], d, "holiday", 8.0)
            if not wd:
                continue
            if rng.random() < W.PTO_SHARE:
                add_week(t["team"], t["district"], t["type"], d, "pto", 8.0)
                continue
            hours = 9.0 * float(np.clip(rng.normal(1.0, 0.05), 0.85, 1.15))
            reg = min(hours, 8.0)
            add_week(t["team"], t["district"], t["type"], d, "regular", reg)
            add_week(t["team"], t["district"], t["type"], d, "overtime", hours - reg)
            lam = t["rate"] * hours / W.RATE_BASE
            for _ in range(int(rng.poisson(lam))):
                cls = ("DA", "RW", "MT")[int(rng.choice(3, p=(0.24, 0.20, 0.56)))]
                injuries.append(dict(unit="tech", ti=ti, code=t["team"], district=t["district"], type=t["type"],
                                     emp=emp, date=d, cls=cls, reported=True, cycle_day=None, mutual_aid=False, work_district=t["district"]))
            for _ in range(int(rng.poisson(lam * W.FIRST_AID_PER_RECORDABLE))):
                injuries.append(dict(unit="tech", ti=ti, code=t["team"], district=t["district"], type=t["type"],
                                     emp=emp, date=d, cls="FA", reported=True, cycle_day=None, mutual_aid=False, work_district=t["district"]))
    return dict(crews=crews, techs=techs, slots=slots, tech_ids=tech_ids, injuries=injuries, exposure=exposure,
                milestones=milestones, weekly=weekly)
