"""The fall 2026 records the two asks read, built from the October 1, 2026 roll: the student system's homeroom and
intervention sections with their enrollment lines (Ask A), and the preschool registration platform's enrollments with
the special education department's early childhood roster (Ask B). Neither touches the main call's files."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment

import common as K
import world as WD

F_SECTIONS = "sections_fall2026.csv"
F_SECT_ENR = "section_enrollment_fall2026.csv"
F_PRESCHOOL = "preschool_enrollments_2026-27.csv"
F_ECSE = "ecse_roster_2026-10-01.xlsx"

TERM_START = dt.date(2026, 8, 17)
TERM_END = K.LAST_DAY_2027
OCT1 = dt.date(2026, 10, 1)

CAP = {0: 23, 1: 24, 2: 25, 3: 26, 4: 27, 5: 28}
HALF_DAY_K = {"A", "P", "F"}            # Ortega, Fifth Street, North Fork run a morning and an afternoon kindergarten
COMBO = {   # one combination class in each band at every school: (band, lower grade, upper grade)
    "A": [(0, 1), (4, 5)], "B": [(1, 2), (3, 4)], "P": [(1, 2), (4, 5)], "C": [(0, 1), (3, 4)],
    "D": [(1, 2), (4, 5)], "E": [(0, 1), (3, 4)], "F": [(1, 2), (3, 4)],
}
COTAUGHT_35 = {"A": 3, "B": 5, "P": 3, "C": 5, "D": 3, "E": 5, "F": 5}       # grade of the co-taught class in 3-5
COTAUGHT_K2 = {"B": 2, "C": 2, "D": 1, "E": 2}                              # schools without half-day kindergarten
TEACHER_CHANGE = {"B": 4, "C": 1}        # a class whose teacher left in September (grade)
PLACEHOLDER = {"F": 4}                   # a section built in spring for a class that did not open
# September rebalancing: after the first weeks each school opened a class for a grade that came in above the spring
# master schedule, on a spare section the schedule had built for a neighbouring grade that came in below it; the
# section keeps the course it was built with. zone: [(grade of the class, grade the section was built for, opened)]
REBALANCE = {
    "A": [(3, 2, dt.date(2026, 9, 8)), (5, 4, dt.date(2026, 9, 14))],
    "B": [(3, 2, dt.date(2026, 9, 14))],
    "P": [(3, 2, dt.date(2026, 9, 8)), (1, 0, dt.date(2026, 9, 21))],
    "C": [(3, 2, dt.date(2026, 9, 21))],
    "D": [(2, 3, dt.date(2026, 9, 14)), (4, 5, dt.date(2026, 9, 8))],
    "E": [(3, 2, dt.date(2026, 9, 8)), (4, 3, dt.date(2026, 9, 14))],
    "F": [(3, 2, dt.date(2026, 9, 14))],
}
LABOR_DAY = dt.date(2026, 9, 7)


def prev_school_day(d):
    d = d - dt.timedelta(days=1)
    while d.weekday() >= 5 or d == LABOR_DAY:
        d -= dt.timedelta(days=1)
    return d


class Ask:
    pass


def _split(n, k):
    base, rem = divmod(n, k)
    return [base + (1 if i < rem else 0) for i in range(k)]


PROGRAM_ROOMS = {"A": 3, "B": 5, "P": 2, "C": 4, "D": 4, "E": 6, "F": 3}   # art, music, STEM, special education


def room_plan(z, cap):
    """The school's permanent rooms as Facilities assigns them for 2026-27: K-5 teaching stations (rated capacity at
    about 23.6 pupils a station), the preschool rooms, three intervention rooms and the school's program rooms (art,
    music, STEM, special education resource; their number varies with the building)."""
    stations = int(round(cap / 23.6))
    pre = [room for (room, kind, sizes) in PRESCHOOL.get(z, [])]
    npg = PROGRAM_ROOMS[z]
    n = stations + len(pre) + 3 + npg
    nums = ["1%02d" % (i + 1) if i < 30 else "2%02d" % (i - 29) for i in range(n)]
    assert all(p in nums for p in pre)
    rest = [x for x in nums if x not in pre]
    k = 3 + npg
    return dict(stations=stations, permanent=n, preschool=pre, intervention=rest[-3:], program=rest[-k:-3],
                homeroom=rest[:-k])


def build_homerooms(W, plans):
    """Classes, sections and enrollment lines for every school on October 1, 2026. plans: each school's room plan
    (room_plan, from the capacity report's rated capacity)."""
    r0 = K.rng("homerooms")
    A = Ask()
    A.sections = []          # dict rows
    A.lines = []             # (section_id, student_id, start, end)
    A.classes = {}           # zone -> list of dict(band, room, session, sections)
    pool = [int(x) for x in r0.choice(np.arange(10400, 48999), size=900, replace=False)]

    def teacher():
        return "T%05d" % pool.pop()

    hd_teacher = {}
    snap = {}
    for (pid, s, g) in W.snap[2026]:
        snap.setdefault(WD.Z[s], {}).setdefault(g, []).append(pid)
    seq = {}

    def sec_id(z):
        seq[z] = seq.get(z, 100) + int(r0.integers(1, 4))
        return "2627-%s-%04d" % (K.SCHOOLS[z]["state"], seq[z])

    for z in K.ZONES:
        r = K.rng("homerooms", z)
        grades = {g: list(snap[z].get(g, [])) for g in range(6)}
        for g in grades:
            idx = r.permutation(len(grades[g]))
            grades[g] = [grades[g][i] for i in idx]
        classes = []
        # combination classes first, one per band
        for (a, b) in COMBO[z]:
            na = int(r.integers(9, 13))
            nb = int(r.integers(10, 14))
            classes.append(dict(grades=[a, b], members={a: grades[a][:na], b: grades[b][:nb]}, kind="combo"))
            grades[a] = grades[a][na:]
            grades[b] = grades[b][nb:]
        # half-day kindergarten
        if z in HALF_DAY_K:
            n_am = int(r.integers(15, 19))
            n_pm = int(r.integers(14, 19))
            classes.append(dict(grades=[0], members={0: grades[0][:n_am]}, kind="halfday", session="AM"))
            classes.append(dict(grades=[0], members={0: grades[0][n_am:n_am + n_pm]}, kind="halfday", session="PM"))
            grades[0] = grades[0][n_am + n_pm:]
        # single-grade classes
        for g in range(6):
            n = len(grades[g])
            if n == 0:
                continue
            k = int(np.ceil(n / CAP[g]))
            sizes = _split(n, k)
            off = 0
            for j, sz in enumerate(sizes):
                classes.append(dict(grades=[g], members={g: grades[g][off:off + sz]}, kind="single"))
                off += sz
        # co-taught classes: the first single class of the named grade, split into two sections by IEP
        for g in [COTAUGHT_35[z]] + ([COTAUGHT_K2[z]] if z in COTAUGHT_K2 else []):
            for c in classes:
                if c["kind"] == "single" and c["grades"] == [g]:
                    c["kind"] = "cotaught"
                    break
        for g in [TEACHER_CHANGE.get(z)]:
            if g is None:
                continue
            for c in classes:
                if c["kind"] == "single" and c["grades"] == [g]:
                    c["kind"] = "changed"
                    break
        for (g, built, opened) in REBALANCE.get(z, []):
            for c in reversed(classes):
                if c["kind"] == "single" and c["grades"] == [g]:
                    c["kind"] = "rebalanced"
                    c["built_for"] = built
                    c["opened"] = opened
                    break
            else:
                raise AssertionError("no class to rebalance at %s grade %d" % (z, g))
        # rooms: the half-day pair shares one room; every other class its own; permanent rooms first, then portables
        hr_rooms = plans[z]["homeroom"]
        ri = 0
        pi = 0
        hd_room = None
        order = sorted(range(len(classes)), key=lambda i: (min(classes[i]["grades"]), classes[i]["kind"] != "halfday", i))
        for i in order:
            c = classes[i]
            if c["kind"] == "halfday" and hd_room is not None:
                c["room"] = hd_room
                continue
            if ri < len(hr_rooms):
                c["room"] = hr_rooms[ri]
                ri += 1
            else:
                pi += 1
                c["room"] = "P%d" % pi
            if c["kind"] == "halfday":
                hd_room = c["room"]
        A.resource_rooms = getattr(A, "resource_rooms", {})
        A.resource_rooms[z] = plans[z]["intervention"]
        A.portables_used = getattr(A, "portables_used", {})
        A.portables_used[z] = pi
        # sections and lines
        for c in sorted(classes, key=lambda c: (min(c["grades"]), c["room"])):
            sess = c.get("session", "FULL")
            if c["kind"] == "combo":
                t = teacher()
                c["sections"] = []
                for g in c["grades"]:
                    sid = sec_id(z)
                    c["sections"].append(sid)
                    A.sections.append(dict(z=z, section_id=sid, course=_course(g), teacher=t, room=c["room"], session=sess,
                                           start=TERM_START, end=TERM_END))
                    for pid in c["members"][g]:
                        A.lines.append((sid, pid, None, None))
            elif c["kind"] == "cotaught":
                g = c["grades"][0]
                t1, t2 = teacher(), teacher()
                s1, s2 = sec_id(z), sec_id(z)
                c["sections"] = [s1, s2]
                A.sections.append(dict(z=z, section_id=s1, course=_course(g), teacher=t1, room=c["room"], session=sess,
                                       start=TERM_START, end=TERM_END))
                A.sections.append(dict(z=z, section_id=s2, course=_course(g), teacher=t2, room=c["room"], session=sess,
                                       start=TERM_START, end=TERM_END))
                mem = c["members"][g]
                ieps = [p for p in mem if WD.iep_on(W, p, 2026)]
                if len(ieps) < 3:
                    ieps = mem[:4]
                ieps = ieps[:6]
                for pid in mem:
                    A.lines.append((s2 if pid in ieps else s1, pid, None, None))
            elif c["kind"] == "changed":
                g = c["grades"][0]
                t_old, t_new = teacher(), teacher()
                s_old, s_new = sec_id(z), sec_id(z)
                c["sections"] = [s_old, s_new]
                A.sections.append(dict(z=z, section_id=s_old, course=_course(g), teacher=t_old, room=c["room"],
                                       session=sess, start=TERM_START, end=dt.date(2026, 9, 18)))
                A.sections.append(dict(z=z, section_id=s_new, course=_course(g), teacher=t_new, room=c["room"],
                                       session=sess, start=dt.date(2026, 9, 21), end=TERM_END))
                for pid in c["members"][g]:
                    A.lines.append((s_old, pid, None, dt.date(2026, 9, 18)))
                    A.lines.append((s_new, pid, dt.date(2026, 9, 21), None))
            elif c["kind"] == "rebalanced":
                g = c["grades"][0]
                t = teacher()
                sid = sec_id(z)
                c["sections"] = [sid]
                A.sections.append(dict(z=z, section_id=sid, course=_course(c["built_for"]), teacher=t, room=c["room"],
                                       session=sess, start=TERM_START, end=TERM_END))
                for pid in c["members"][g]:
                    A.lines.append((sid, pid, max(c["opened"], W.spell[(pid, 2026)][0]), None))
            else:
                g = c["grades"][0]
                if c["kind"] == "halfday":          # one teacher teaches the morning and the afternoon class
                    if hd_teacher.get(z) is None:
                        hd_teacher[z] = teacher()
                    t = hd_teacher[z]
                else:
                    t = teacher()
                sid = sec_id(z)
                c["sections"] = [sid]
                A.sections.append(dict(z=z, section_id=sid, course=_course(g), teacher=t, room=c["room"], session=sess,
                                       start=TERM_START, end=TERM_END))
                for pid in c["members"][g]:
                    A.lines.append((sid, pid, None, None))
            c["teacher_sections"] = c["sections"]
        # the rebalanced classes' pupils sat in the grade's other classes until the class opened
        for c in classes:
            if c["kind"] != "rebalanced":
                continue
            g = c["grades"][0]
            donors = [d for d in classes if d["kind"] == "single" and d["grades"] == [g]]
            assert donors, (z, g)
            last = prev_school_day(c["opened"])
            for k, pid in enumerate(c["members"][g]):
                if W.spell[(pid, 2026)][0] > last:
                    continue
                A.lines.append((donors[k % len(donors)]["sections"][0], pid, None, last))
        if z in PLACEHOLDER:
            sid = sec_id(z)
            A.sections.append(dict(z=z, section_id=sid, course=_course(PLACEHOLDER[z]), teacher="T00000", room="TBD",
                                   session="FULL", start=TERM_START, end=TERM_END))
        # intervention groups in the resource rooms
        allp = [p for g in range(6) for p in snap[z].get(g, [])]
        for j, (code, title) in enumerate([("INT-RDG", "Reading Intervention"), ("INT-RDG", "Reading Intervention"),
                                            ("INT-MTH", "Math Intervention"), ("INT-ELD", "English Language Development")]):
            sid = sec_id(z)
            t = teacher()
            room = A.resource_rooms[z][j % len(A.resource_rooms[z])]
            A.sections.append(dict(z=z, section_id=sid, course=code, teacher=t, room=room, session="FULL",
                                   start=dt.date(2026, 9, 8), end=TERM_END, title=title))
            pick = r.choice(len(allp), size=int(r.integers(5, 9)), replace=False)
            for k in sorted(pick):
                A.lines.append((sid, allp[k], dt.date(2026, 9, 8), None))
        A.classes[z] = classes
    _line_dates(W, A)
    return A


def _course(g):
    return "HR-K" if g == 0 else "HR-%d" % g


def _line_dates(W, A):
    """Each homeroom line starts on the first day or the pupil's entry date; a few September moves between classes in a
    school; pupils who left the district between October 2 and October 8 have their line ended; new pupils who
    enrolled after the count day have lines starting then."""
    r = K.rng("line_dates")
    out = []
    for (sid, pid, st, en) in A.lines:
        if st is None:
            ed = W.spell[(pid, 2026)][0]
            st = max(TERM_START, ed)
            if st > OCT1:
                st = TERM_START
        out.append([sid, pid, st, en])
    A.lines = out
    # withdrawals after the count day: their roster lines end between October 2 and October 8
    hr_lines = [i for i, l in enumerate(A.lines) if l[3] is None and l[0] in {s["section_id"] for s in A.sections if s["course"].startswith("HR")}]
    for i in r.choice(hr_lines, size=19, replace=False):
        A.lines[int(i)][3] = dt.date(2026, 10, int(r.integers(2, 9)))
    A.late = []   # pupils enrolled after the count day (not on the October 1 roll)


def write_sections(W, A, out):
    rows = []
    for s in sorted(A.sections, key=lambda s: (K.SCHOOLS[s["z"]]["state"], s["section_id"])):
        title = s.get("title") or ("Homeroom Kindergarten" if s["course"] == "HR-K" else "Homeroom Grade %s" % s["course"][-1])
        rows.append([K.SCHOOLS[s["z"]]["state"], K.SCHOOLS[s["z"]]["name"], s["section_id"], s["course"], title,
                     s["teacher"], s["room"], s["session"], K.iso(s["start"]), K.iso(s["end"])])
    return K.write_csv(os.path.join(out, F_SECTIONS),
                       ["school_code", "school_name", "section_id", "course_code", "course_title", "teacher_id", "room",
                        "session", "section_start", "section_end"], rows)


def write_section_enrollment(W, A, out):
    sid_of = {pid: W.info[pid]["sid"] for (pid, s, g) in W.snap[2026]}
    rows = []
    for (sec, pid, st, en) in A.lines:
        rows.append([sec, sid_of[pid], K.iso(st), K.iso(en)])
    # pupils who enrolled after the count day, scheduled into a homeroom from their first day
    r = K.rng("late_enrollees")
    hr = [s for s in A.sections if s["course"].startswith("HR") and s["room"] != "TBD" and s["end"] == TERM_END]
    taken = set(v for v in sid_of.values())
    for k in range(11):
        s = hr[int(r.integers(0, len(hr)))]
        while True:
            new = "%010d" % int(r.integers(1300000000, 1899999999))
            if new not in taken:
                taken.add(new)
                break
        rows.append([s["section_id"], new, K.iso(dt.date(2026, 10, int(r.integers(5, 9)))), ""])
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return K.write_csv(os.path.join(out, F_SECT_ENR), ["section_id", "student_id", "start_date", "end_date"], rows)


# ---------------------------------------------------------------------------------------------------- preschool
PRESCHOOL = {
    # zone: list of (room, kind, sizes); kind upk = morning and afternoon half-day classes in one room; fd = a
    # full-day class; ecse = a self-contained special education classroom (a morning group, and an afternoon group
    # where there are two)
    "A": [("112", "upk", (16, 16)), ("114", "fd", (16,)), ("115", "upk", (15, 16)), ("116", "ecse", (8, 7))],
    "P": [("105", "upk", (16, 15)), ("107", "upk", (15, 16)), ("109", "fd", (16,)), ("110", "ecse", (6, 5))],
    "D": [("120", "upk", (16, 16)), ("122", "ecse", (7, 6)), ("124", "ecse", (6,))],
    "F": [("104", "fd", (16,)), ("106", "fd", (15,)), ("108", "ecse", (6,))],
}


CASE_FLOWS = [("P", "110", "A", 1), ("D", "122", "P", 2), ("A", "116", "D", 2), ("F", "108", "D", 1), ("D", "124", "F", 2)]


def build_preschool(W):
    r = K.rng("preschool")
    P = Ask()
    P.platform = []       # dict rows
    P.ecse = []
    taken = set(W.info[p]["sid"] for p in W.info)
    cid = [400]

    def new_sid():
        while True:
            s = "%010d" % int(r.integers(1300000000, 1899999999))
            if s not in taken:
                taken.add(s)
                return s

    def child_id():
        cid[0] += int(r.integers(1, 9))
        return "PK26-%05d" % cid[0]

    def bdate(three=False):
        lo, hi = (dt.date(2022, 10, 2), dt.date(2023, 10, 1)) if three else (dt.date(2021, 10, 2), dt.date(2022, 10, 1))
        return lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))

    P.truth = {}
    for z, rooms in PRESCHOOL.items():
        kids = set()
        rooms_used = set()
        for (room, kind, sizes) in rooms:
            if kind == "ecse":
                for sess, n in zip(("AM", "PM"), sizes):
                    for _ in range(n):
                        s = new_sid()
                        P.ecse.append(dict(z=z, case=z, sid=s, birth=bdate(r.random() < 0.45), service="ECSE classroom",
                                           room="Rm %s" % room, session=sess,
                                           iep_start=dt.date(2025, 1, 6) + dt.timedelta(days=int(r.integers(0, 600)))))
                        kids.add(s)
                rooms_used.add(room)
                continue
            sessions = ("AM", "PM") if kind == "upk" else ("Full Day",)
            for sess, n in zip(sessions, sizes):
                for k in range(n):
                    s = new_sid()
                    three = r.random() < 0.12
                    fund = ("UPK 15 hrs" if kind == "upk" else
                            ("UPK 30 hrs" if r.random() < 0.3 else ("UPK 15 hrs + tuition" if r.random() < 0.7 else "Tuition")))
                    row = dict(z=z, child=child_id(), sid=s, birth=bdate(three), cls="Rm %s %s" % (room, sess), session=sess,
                               funding=fund, start=dt.date(2026, 8, 24), end=None,
                               app=dt.date(2026, 2, 2) + dt.timedelta(days=int(r.integers(0, 150))))
                    P.platform.append(row)
                    kids.add(s)
            rooms_used.add(room)
        P.truth[z] = dict(kids=kids, rooms=rooms_used)
    # September changes, chosen first so each is a child with one platform record and no roster row: a child who
    # moved from North Fork to Kessler and one from Fifth Street to Ortega (the record moves, the old enrollment
    # ended), and a withdrawal at Ortega, Kessler and North Fork
    used = set()
    for (zf, zt, end, start) in (("F", "D", dt.date(2026, 9, 11), dt.date(2026, 9, 14)),
                                 ("P", "A", dt.date(2026, 9, 18), dt.date(2026, 9, 22))):
        src = [p for p in P.platform if p["z"] == zf][3]
        dst_cls = [p for p in P.platform if p["z"] == zt and p["session"] == "AM"][0]["cls"]
        q = dict(src)
        src["end"] = end
        P.truth[zf]["kids"].discard(src["sid"])
        q.update(z=zt, cls=dst_cls, start=start, end=None)
        P.platform.append(q)
        P.truth[zt]["kids"].add(q["sid"])
        used.add(src["sid"])
    for z in ("A", "D", "F"):
        cand = [p for p in P.platform if p["z"] == z and p["end"] is None and p["sid"] not in used]
        p = cand[-1]
        p["end"] = dt.date(2026, 9, int(r.integers(9, 26)))
        P.truth[z]["kids"].discard(p["sid"])
        used.add(p["sid"])
    # inclusive placements: children with an IEP in a preschool class appear on both sources (2 to 4 a site)
    for z in PRESCHOOL:
        rows = [p for p in P.platform if p["z"] == z and p["sid"] not in used]
        for p in [rows[int(i)] for i in r.choice(len(rows), size=int(r.integers(2, 5)), replace=False)]:
            room = p["cls"].replace(" Full Day", "") if p["cls"].endswith("Full Day") else p["cls"].rsplit(" ", 1)[0]
            P.ecse.append(dict(z=z, case=z, sid=p["sid"], birth=p["birth"], service="Inclusive classroom", room=room,
                               session=p["session"],
                               iep_start=dt.date(2025, 3, 3) + dt.timedelta(days=int(r.integers(0, 500)))))
            used.add(p["sid"])
    # itinerant services: on the roster under the site that holds the case, served at home or a community preschool
    for z in PRESCHOOL:
        for _ in range(int(r.integers(2, 5))):
            s = new_sid()
            P.ecse.append(dict(z=z, case=z, sid=s, birth=bdate(r.random() < 0.5), service="Itinerant", room="", session="",
                               iep_start=dt.date(2025, 6, 2) + dt.timedelta(days=int(r.integers(0, 400)))))
    # re-registrations: a family that applied again holds a second child record in the same class (1 or 2 a site)
    for z in PRESCHOOL:
        rows = [p for p in P.platform if p["z"] == z and p["sid"] not in used and p["end"] is None]
        for p in [rows[int(i)] for i in r.choice(len(rows), size=int(r.integers(1, 3)), replace=False)]:
            q = dict(p)
            q["child"] = child_id()
            q["app"] = p["app"] + dt.timedelta(days=int(r.integers(20, 90)))
            P.platform.append(q)
            used.add(p["sid"])
    # the special education classrooms are district programs: some children's IEP cases are held by the special
    # education team of another preschool site (host zone, room, case zone, children)
    for (host, room, case, n) in CASE_FLOWS:
        rows = [p for p in P.ecse if p["z"] == host and p["service"] == "ECSE classroom" and p["room"] == "Rm " + room
                and p["case"] == host]
        for p in rows[:n]:
            p["case"] = case
        assert any(p["case"] == host for p in P.ecse if p["z"] == host and p["room"] == "Rm " + room)
    # a waitlist offer that starts after the count day
    p = dict([q for q in P.platform if q["z"] == "P"][0])
    p.update(child=child_id(), sid=new_sid(), start=dt.date(2026, 10, 5), end=None, app=dt.date(2026, 5, 18))
    P.platform.append(p)
    return P


def write_preschool(W, P, out):
    rows = []
    for p in sorted(P.platform, key=lambda p: (K.SCHOOLS[p["z"]]["name"], p["cls"], p["child"])):
        rows.append([p["child"], p["sid"], K.iso(p["birth"]), K.SCHOOLS[p["z"]]["name"], p["cls"], p["session"],
                     p["funding"], K.iso(p["start"]), K.iso(p["end"]), K.iso(p["app"])])
    return K.write_csv(os.path.join(out, F_PRESCHOOL),
                       ["child_id", "state_id", "birth_date", "site", "class_name", "session", "funding",
                        "enroll_start", "enroll_end", "application_date"], rows)


ECSE_NOTES = [
    "Early Childhood Special Education roster: children aged 3 to 5 with an active IEP on 10/01/2026, listed by case "
    "school.",
    "Case school: the elementary school whose special education team holds the child's IEP case.",
    "Service model: ECSE classroom, a district early childhood special education classroom; Inclusive classroom, a "
    "district preschool class the child attends with special education support; Itinerant, special education services "
    "at the child's home or community preschool. A child served itinerantly is not enrolled in a district preschool "
    "class.",
    "Classroom: the school and room where the child's class meets. A morning and an afternoon class in the same room "
    "share the classroom.",
]


def write_ecse(W, P, out):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Roster 10-01-2026"
    ws.append(["%s, Special Education Department" % K.DISTRICT])
    ws.append(["Early Childhood Special Education (ages 3 to 5), active IEPs on 10/01/2026, by case school"])
    ws.append([])
    ws.append(["State ID", "Birth date", "Case school", "Service model", "Classroom", "Session", "IEP start"])

    def classroom(p):
        return "%s %s" % (K.SCHOOLS[p["z"]]["short"], p["room"]) if p["room"] else ""

    for p in sorted(P.ecse, key=lambda p: (K.SCHOOLS[p["case"]]["name"], p["service"], classroom(p), p["sid"])):
        ws.append([p["sid"], p["birth"], K.SCHOOLS[p["case"]]["name"], p["service"], classroom(p), p["session"],
                   p["iep_start"]])
    ws["A1"].font = Font(bold=True)
    for c in ws[4]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCDEFG", (13, 12, 24, 20, 20, 9, 12)):
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=5):
        row[1].number_format = "mm/dd/yyyy"
        row[6].number_format = "mm/dd/yyyy"
    ws.freeze_panes = "A5"
    nt = wb.create_sheet("Notes")
    for line in ECSE_NOTES:
        nt.append([line])
        nt.cell(row=nt.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 110
    K.save_workbook(wb, os.path.join(out, F_ECSE), dt.datetime(2026, 10, 2, 9, 14, 0), "Special Education")
    return len(P.ecse)
