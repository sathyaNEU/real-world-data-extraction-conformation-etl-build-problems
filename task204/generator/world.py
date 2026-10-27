#!/usr/bin/env python3
"""The clean truth for task204: the calendar, the stamp grid, the sessions, the attendance and the
carbon dioxide series each monitored space would really produce.

Nothing here is messy. build.py applies the Layer 1 complications on the way out to target/, and
checks.py asserts that each of them leaves the golden and every critical component where they were.

One RNG stream per purpose, each seeded from params.SEED and its own name, so adding a stream never
shifts the draws of another (dataset-generation section 11, byte-identical rebuilds).
"""
import datetime as dt
import math
import random
from zoneinfo import ZoneInfo

import params as P

TZ = ZoneInfo(P.TZ)
UTC = dt.timezone.utc


def rng(name):
    return random.Random("%s|%s" % (P.SEED, name))


# ----------------------------------------------------------------- calendar

def _d(s):
    return dt.date.fromisoformat(s)


def calendar_days():
    """One row per local day in the window: (date, weekday, kind), kind in teaching, weekend,
    midterm, closure."""
    out = []
    d, end = _d(P.TERM_START), _d(P.TERM_END)
    mt0, mt1 = _d(P.MIDTERM_BREAK[0]), _d(P.MIDTERM_BREAK[1])
    while d <= end:
        iso = d.isoformat()
        if d.weekday() >= 5:
            kind = "weekend"
        elif mt0 <= d <= mt1:
            kind = "midterm"
        elif iso in P.CLOSURE_DAYS:
            kind = "closure"
        else:
            kind = "teaching"
        out.append((iso, d.weekday(), kind))
        d += dt.timedelta(days=1)
    return out


def teaching_days():
    return [(iso, wd) for iso, wd, k in calendar_days() if k == "teaching"]


# ----------------------------------------------------------------- the five-minute stamp grid

def stamps():
    """Every logging instant in the window, in order, as
    (utc_datetime, local_date, local_hhmmss, offset_string).

    The grid is the local wall clock, so the hour the clocks go back is logged twice and 25 October
    carries 300 stamps rather than 288. The offset column is what separates them.
    """
    start = dt.datetime.combine(_d(P.TERM_START), dt.time(0, 0), tzinfo=TZ).astimezone(UTC)
    end = (dt.datetime.combine(_d(P.TERM_END), dt.time(0, 0), tzinfo=TZ)
           + dt.timedelta(days=1)).astimezone(UTC)
    out, t = [], start
    step = dt.timedelta(seconds=P.STEP_S)
    while t < end:
        loc = t.astimezone(TZ)
        off = loc.utcoffset()
        sign = "+" if off >= dt.timedelta(0) else "-"
        mins = int(abs(off).total_seconds()) // 60
        out.append((t, loc.date().isoformat(), loc.strftime("%H:%M:%S"),
                    "%s%02d:%02d" % (sign, mins // 60, mins % 60)))
        t += step
    return out


# ----------------------------------------------------------------- plant status

def _hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def ahu_state(ahu, local_date, local_hhmmss, day_kind):
    """The unit's state for the five minutes beginning at this stamp."""
    cfg = P.AHU[ahu]
    if day_kind != "teaching":
        return "OFF"
    h, m, _ = local_hhmmss.split(":")
    mins = int(h) * 60 + int(m)
    o0, o1 = _hm(cfg["occupied"][0]), _hm(cfg["occupied"][1])
    s0, s1 = _hm(cfg["setback"][0]), _hm(cfg["setback"][1])
    if s0 <= mins < s1:
        return "SETBACK"
    if o0 <= mins < o1:
        return "OCCUPIED"
    return "OFF"


def plant_intervals():
    """The status log the building management system writes: one row per state change per unit."""
    kinds = {iso: k for iso, _, k in calendar_days()}
    rows = []
    for ahu in sorted(P.AHU):
        cur, run_start, run_date = None, None, None
        for (_, ld, lt, off) in stamps():
            st = ahu_state(ahu, ld, lt, kinds[ld])
            if st != cur or ld != run_date:
                if cur is not None:
                    rows.append((ahu, run_date, run_start, ld, lt, cur))
                cur, run_start, run_date = st, lt, ld
        rows.append((ahu, run_date, run_start, run_date, "24:00:00", cur))
    return rows


# ----------------------------------------------------------------- sessions and attendance

def _periods(space_code):
    block = dict((s[0], s[2]) for s in P.SPACES)[space_code]
    return P.TUL_PERIODS if block == "Tulrohan" else P.GEN_PERIODS


def _pattern(space_code):
    return P.TUL_PATTERN.get(space_code) or P.GEN_PATTERN[space_code]


def group_table():
    return {g[0]: {"programme": g[1], "enrolled": g[2], "subject": g[3]} for g in P.GROUPS}


def group_attendance_rates():
    r = rng("attendance-rate")
    lo, hi = P.ATTENDANCE_BAND
    return {g[0]: lo + (hi - lo) * r.random() for g in P.GROUPS}


def group_tutors():
    """Each group's own tutor, drawn from the tutors of the school the group's programme sits in,
    rather than cycled, so the tutor column has no fixed period, the counts per tutor are uneven and
    no staff record names a school its own sessions contradict."""
    r = rng("tutor-assign")
    by_school = {}
    for name, school in P.TUTOR_SCHOOL.items():
        by_school.setdefault(school, []).append(name)
    for v in by_school.values():
        v.sort()
    return {g[0]: r.choice(by_school[P.SCHOOL_OF_SUBJECT[g[3]]]) for g in P.GROUPS}


def sessions():
    """Every timetabled session in the window, with the occupants present."""
    groups = group_table()
    rates = group_attendance_rates()
    tutors = group_tutors()
    r_present = rng("present")
    r_cover = rng("cover")
    r_assist = rng("assistant")
    split_group, split_wd, split_pi, split_rooms = P.SPLIT_GROUP

    out = []
    for iso, wd in teaching_days():
        for code, name, block, ahu, *_ in P.SPACES:
            per = _periods(code)
            pat = _pattern(code)[wd]
            for pi, (pname, t0, t1) in enumerate(per):
                g = pat[pi] if pi < len(pat) else None
                if g is None:
                    continue
                enrolled = groups[g]["enrolled"]
                split_half = None
                if g == split_group and wd == split_wd and pi == split_pi and code in split_rooms:
                    # the cohort is taught in two rooms in the same period, so each room holds a part
                    split_half = 0 if code == split_rooms[0] else 1
                n_at_risk = enrolled if split_half is None else (enrolled + 1 - split_half) // 2
                n_at_risk = max(1, n_at_risk)
                present = sum(1 for _ in range(n_at_risk) if r_present.random() < rates[g])
                present = max(0, min(n_at_risk, present))
                tutor = tutors[g]
                if r_cover.random() < 0.035:
                    same = sorted(n for n, sc in P.TUTOR_SCHOOL.items()
                                  if sc == P.SCHOOL_OF_SUBJECT[groups[g]["subject"]])
                    tutor = r_cover.choice(same)
                assistant = r_assist.choice(P.ASSISTANTS) if r_assist.random() < P.ASSISTANT_SHARE else None
                staff = 1 + (1 if assistant else 0)
                out.append({
                    "session_id": "%s-%s-%s" % (iso.replace("-", ""), code, pname),
                    "date": iso, "weekday": wd, "space": code, "block": block, "ahu": ahu,
                    "period": pname, "start": t0, "end": t1,
                    "group": g, "enrolled": enrolled, "subject": groups[g]["subject"],
                    "learners_present": present, "tutor": tutor, "assistant": assistant,
                    "occupants": present + staff, "at_risk": n_at_risk, "split_half": split_half,
                })
    return out


def attendance_rows(sess):
    """The statutory register's marks, one row per person per session. Learner references are drawn
    per group from a block of references rather than stepped, so no column is an arithmetic run."""
    r_ref = rng("learner-ref")
    r_mark = rng("mark")
    r_amend = rng("amend")
    groups = group_table()
    # each group's learner references: a block per programme with real gaps
    refs = {}
    for g in P.GROUPS:
        base = 1000 * (3 + r_ref.randrange(0, 7)) + r_ref.randrange(100, 900)
        pool, cur = [], base
        while len(pool) < g[2]:
            cur += 1 + r_ref.randrange(1, 9)
            pool.append("L%06d" % cur)
        refs[g[0]] = pool

    rows = []
    for s in sess:
        pool = refs[s["group"]]
        n_at_risk = min(s["at_risk"], len(pool))
        take = pool[-n_at_risk:] if s["split_half"] == 1 else pool[:n_at_risk]
        present_set = set()
        order = list(take)
        r_mark.shuffle(order)
        for ref in order[:s["learners_present"]]:
            present_set.add(ref)
        for ref in take:
            if ref in present_set:
                mark = "present"
            else:
                mark = "authorised" if r_mark.random() < 0.28 else "absent"
            amended = r_amend.random() < 0.012
            rows.append({"session_id": s["session_id"], "date": s["date"], "space": s["space"],
                         "period": s["period"], "group": s["group"], "person_ref": ref,
                         "role": "learner", "mark": mark,
                         "amended": "Y" if amended else "N"})
        rows.append({"session_id": s["session_id"], "date": s["date"], "space": s["space"],
                     "period": s["period"], "group": s["group"],
                     "person_ref": staff_ref(s["tutor"]), "role": "tutor", "mark": "present",
                     "amended": "N"})
        if s["assistant"]:
            rows.append({"session_id": s["session_id"], "date": s["date"], "space": s["space"],
                         "period": s["period"], "group": s["group"],
                         "person_ref": staff_ref(s["assistant"]), "role": "assistant",
                         "mark": "present", "amended": "N"})
    return rows


_STAFF_REFS = {}


def staff_ref(name):
    if not _STAFF_REFS:
        r = rng("staff-ref")
        for n in P.TUTORS + P.ASSISTANTS:
            _STAFF_REFS[n] = "S%05d" % (4000 + r.randrange(1, 1800))
    return _STAFF_REFS[name]


# ----------------------------------------------------------------- the outdoor baseline

def outdoor_series(stamp_list):
    """The campus analyser's outdoor reading, ppm: a seasonal rise across the autumn, a diurnal
    cycle and weather-driven day-to-day variation."""
    r = rng("outdoor-day")
    day_shift = {}
    for iso, _, _ in calendar_days():
        day_shift[iso] = r.gauss(0.0, 5.2)
    out = []
    t0 = stamp_list[0][0]
    for (t, ld, lt, off) in stamp_list:
        days = (t - t0).total_seconds() / 86400.0
        hh, mm, _ = (int(x) for x in lt.split(":"))
        hour = hh + mm / 60.0
        seasonal = 0.0315 * days
        diurnal = 4.1 * math.cos(2 * math.pi * (hour - 5.0) / 24.0)
        out.append(P.OUTDOOR_BASE_PPM + seasonal + diurnal + day_shift[ld])
    return out


# ----------------------------------------------------------------- the carbon dioxide series

def terminals():
    """Supply terminals per space, drawn once so the zone assignment sheet and the as-built room
    data sheets agree: two systems holding the same asset count, as they would."""
    r = rng("terminal-count")
    return {s[0]: 2 + r.randrange(0, 5) for s in P.SPACES}


def supply_m3s(space, state, day_factor):
    """The space's outdoor-air supply for a five-minute step, cubic metres per second."""
    row = dict((s[0], s) for s in P.SPACES)[space]
    vol, q_occ, ach_off, ach_sb = row[4], row[5], row[6], row[7]
    if state == "OCCUPIED":
        return q_occ * day_factor
    if state == "SETBACK":
        return vol * ach_sb / 3600.0
    return vol * ach_off / 3600.0


def series():
    """The true excess over the outdoor baseline, ppm, per space per stamp, plus the per-step
    occupancy and plant state the balance is driven by.

    Returns (stamp_list, outdoor, excess, occ, state, day_factor) where excess[space] is a list the
    length of stamp_list.
    """
    stamp_list = stamps()
    outdoor = outdoor_series(stamp_list)
    kinds = {iso: k for iso, _, k in calendar_days()}
    index = {(ld, lt, off): i for i, (_, ld, lt, off) in enumerate(stamp_list)}

    sess = sessions()
    # occupancy per space per step: a session's occupants generate from its start stamp up to but not
    # including its end stamp, so generation runs for exactly the session's 3,300 seconds.
    occ = {s[0]: [0] * len(stamp_list) for s in P.SPACES}
    for s in sess:
        a = _hm(s["start"]) // 5
        b = _hm(s["end"]) // 5
        for k in range(a, b):
            hh, mm = divmod(k * 5, 60)
            key = (s["date"], "%02d:%02d:00" % (hh, mm), None)
            # find the stamp with this local date and time; on the repeated hour take the first
            for off in ("+01:00", "+00:00"):
                i = index.get((s["date"], "%02d:%02d:00" % (hh, mm), off))
                if i is not None:
                    occ[s["space"]][i] += s["occupants"]
                    break

    r_day = rng("day-factor")
    day_factor = {}
    for code, *_ in P.SPACES:
        for iso, _, _ in calendar_days():
            day_factor[(code, iso)] = max(0.75, min(1.25, r_day.gauss(1.0, P.ROOM_MIXING_SD)))

    state = {}
    for ahu in sorted(P.AHU):
        state[ahu] = [ahu_state(ahu, ld, lt, kinds[ld]) for (_, ld, lt, off) in stamp_list]

    excess = {}
    for row in P.SPACES:
        code, _, _, ahu, vol = row[0], row[1], row[2], row[3], row[4]
        st = state[ahu]
        # one warm-up pass so the opening state is the term's own rather than zero
        c, vals = 0.0, []
        for _pre in range(2):
            vals = []
            for i in range(len(stamp_list)):
                q = supply_m3s(code, st[i], day_factor[(code, stamp_list[i][1])])
                ceq = 1e6 * occ[code][i] * P.GENERATION_M3_PER_S / q
                decay = math.exp(-q * P.STEP_S / vol)
                vals.append(c)
                c = ceq + (c - ceq) * decay
            c = vals[min(len(vals) - 1, 4032)]
        excess[code] = vals
    return stamp_list, outdoor, excess, occ, state, day_factor


def session_windows(stamp_list):
    """Map each session to the indices of the stamps from its first to its last reading inclusive."""
    index = {}
    for i, (_, ld, lt, off) in enumerate(stamp_list):
        index.setdefault((ld, lt), i)   # the repeated hour's first occurrence
    out = {}
    for s in sessions():
        a = _hm(s["start"]) // 5
        b = _hm(s["end"]) // 5
        idx = []
        for k in range(a, b + 1):
            hh, mm = divmod(k * 5, 60)
            i = index.get((s["date"], "%02d:%02d:00" % (hh, mm)))
            if i is not None:
                idx.append(i)
        out[s["session_id"]] = idx
    return out


# ----------------------------------------------------------------- session frames on the clean truth

def truth_frames(cache={}):
    """One frame per timetabled session, built from the clean truth with no mess applied."""
    if "f" in cache:
        return cache["f"]
    stamp_list, outdoor, excess, occ, state, day_factor = series()
    win = session_windows(stamp_list)
    frames = []
    for s in sessions():
        idx = win[s["session_id"]]
        if len(idx) < 3:
            continue
        frames.append({
            "session_id": s["session_id"], "space": s["space"], "date": s["date"],
            "period": s["period"], "occupants": s["occupants"],
            "seconds": (_hm(s["end"]) - _hm(s["start"])) * 60,
            "readings": [excess[s["space"]][i] for i in idx],
        })
    cache["f"] = frames
    cache["w"] = (stamp_list, outdoor, excess, occ, state, day_factor)
    return frames


def truth_world(cache={}):
    truth_frames()
    return truth_frames.__defaults__[0]["w"]
