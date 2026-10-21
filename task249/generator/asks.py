"""The asks' records, on rows the call never reads.

Ask A (each form's 2027 sittings a failure of the candidate's workstation or its power interrupted) and the integrity
report's link item (each form's 2027 sittings that ran in part without the centre's link): the provider's seat plan, its
workstation event log (UTC) and the centres' invigilator incident reports (local time).

The provider's server logs WS_FAIL once a workstation serving a sitting has said nothing for three minutes while the
server still hears the centre. A computer that freezes is either restarted where it stands (it logs WS_REBOOT as it comes
back and the candidate resumes on it; a restart inside three minutes leaves no WS_FAIL) or left for a spare; near the
end of a sitting the invigilator may close it on the saved responses instead. A keyboard, mouse or screen that fails
under a running computer leaves no WS_FAIL and the candidate moves to a spare; so does a client that hangs as the
centre's link drops under it (the server hears nobody at the centre then). A change of seat at the candidate's request
also ends on a spare; an invigilator's pause resumes on the same workstation. The invigilators report every move to a
spare except that about three in ten of the freezes the server logged go unreported, half the restarts in place and three
pauses in four; about one report in ten has the workstation's number typed wrong (two digits swapped, or the seat
beside), and the spare and the times it names are right.

Two things put a WS_FAIL on a sitting nothing interrupted: an invigilator switching off a finished candidate's
workstation before the session closed (the server still counts it as serving the sitting), and a fault on one
workstation's own connection (its cable or port), when the server loses sight of a client that carries on: that client
alone logs NET_LOST and NET_BACK around it.

On 19 August 2027 a power cut at Kochi took the router and the local server down at once while the UPS carried the
workstations for about four minutes: the log has nothing for half an hour, the machines log WS_REBOOT as the power comes
back and each sitting resumes on its own workstation. Twice a whole hall's clocks were stopped before its link went
down: on 14 May 2027 smoke from the UPS in Chennai's communications cabinet set off the fire alarm (the invigilators
stopped every clock and cleared the hall, the cabinet's UPS and router were switched off two minutes later and the router
was back on the mains about twenty minutes after that), and on 16 November 2027 Hyderabad's building management gave
notice of a switch of the building's power to the generator (the clocks were stopped as a precaution, the hall stayed on
its UPS and the router, on the building supply, was off for about eleven minutes). In both the candidates resumed on their
own workstations after the link was back; no sitting ran while the link was down, and neither was a failure of a
workstation or its power.

A loss of a centre's link is logged by each client logged in at the time (NET_LOST, NET_BACK, the candidate's booking),
a finished candidate's too, until the session closes or the workstation is switched off; a client that logs in while
the link is down logs only NET_BACK when it comes back.   A = asks.build(W, R)

Ask B of an earlier layer (each content area's trial items standing accepted) ships as the panel's decision log, a
distractor."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import records as RC

P_FAIL = 0.0062      # the computer froze or crashed and the candidate went to a spare
P_RESTART = 0.0082   # the computer froze or crashed and was restarted where it stood
P_PERIPH = 0.0016    # a keyboard, mouse or screen failed under a running computer
P_MOVE = 0.0013      # a change of seat at the candidate's request
P_PAUSE = 0.0085     # an invigilator's pause
P_LATE = 0.14        # of the freezes in a sitting that reached its last item: near the end, closed on saved responses
P_HANG = 0.07        # a running client that hangs when the centre's link drops
P_FAULT = 0.0024     # a fault on one workstation's own connection; the client carries on
P_OFF = 0.0030       # a finished candidate's workstation switched off before the session closed
REPORTED = dict(fail=0.7, late=0.7, restart=0.5, periph=1.0, move=1.0, pause=0.75, hang=1.0)
P_TYPO = 0.10        # a workstation number typed wrong in a report (digits swapped, or the seat beside)
SILENCE = 3.0        # minutes a workstation serving a sitting may say nothing before the server logs WS_FAIL
POWER = dict(window=6, centre="Kochi", day=10, session="AM", cut=(11, 5), back=(11, 31))
# the two times a whole hall's clocks were stopped before its link went down: (minutes after the first word) the clocks
# stopped, the router went off, the link came back, the candidates resumed
HALL_STOPS = [dict(window=5, centre="Chennai", day=4, session="PM", at=(16, 12), stop=1.0, off=(2.5, 3.5), on=(21, 23),
                   back=(29, 31), text="smoke"),
              dict(window=7, centre="Hyderabad", day=8, session="AM", at=(11, 26), stop=1.0, off=(3.8, 4.4), on=(14.5, 16),
                   back=(18.5, 20), text="switch")]
PAUSE_REASONS = ["candidate unwell", "candidate's ID re-checked at the desk", "code book checked at the desk for added notes",
                 "candidate left for the washroom", "candidate's code book swapped for a clean copy",
                 "candidate taken out to take a call from home about an emergency"]
PARTS = ["keyboard stopped working", "mouse stopped responding", "screen went blank", "several keys on the keyboard stuck",
         "the mouse pointer froze while the computer ran"]
WHY = ["glare from the window", "noise from the corridor", "a wobbling desk", "a candidate coughing beside them",
       "the air conditioning blowing on them", "a broken chair"]
# each centre's invigilators write their reports in their own way
STYLE = {
    "Chennai": dict(fail=["{ws} stopped responding; candidate moved to {sp} and resumed at {back}",
                          "{ws} froze; candidate shifted to {sp}, resumed {back}",
                          "{ws} hung on the item screen; moved to {sp}, resumed at {back}",
                          "{ws} not responding to mouse or keyboard; candidate on {sp} from {back}"],
                    late=["{ws} stopped responding near the end; sitting closed on the saved responses",
                          "{ws} froze in the last minutes; closed on saved responses after two tries"],
                    restart=["{ws} froze; restarted, candidate continued on {ws} from {back}",
                             "{ws} stopped responding; system restarted and candidate resumed on it at {back}",
                             "{ws} hung; restarted at the desk, candidate back on {ws} at {back}"],
                    periph=["{ws}: {part}; candidate moved to {sp} and resumed at {back}",
                            "{ws}: {part}. Candidate shifted to {sp}, resumed {back}"],
                    move=["{ws}: candidate asked to move ({why}); moved to {sp}, resumed at {back}",
                          "{ws}: candidate asked to move because of {why}; given {sp}, resumed {back}"],
                    pause=["{ws}: {reason}, paused from {at} to {back}", "{ws}: {reason}; clock stopped {at} to {back}",
                           "{ws} paused {at} to {back} ({reason})"]),
    "Bengaluru": dict(fail=["Workstation {ws} froze. Candidate shifted to spare {sp}, exam resumed {back}.",
                            "Workstation {ws} hung. Spare {sp} given, exam resumed {back}.",
                            "Workstation {ws} stopped responding. Moved the candidate to spare {sp}; exam resumed {back}."],
                      late=["Workstation {ws} froze with a few minutes left. Sitting ended on the saved answers.",
                            "Workstation {ws} hung just before the end. Closed on the saved answers."],
                      restart=["Workstation {ws} froze. Restarted it; candidate resumed on {ws} at {back}.",
                               "Workstation {ws} hung. Restart done, exam resumed on the same system {back}."],
                      periph=["Workstation {ws}: {part}. Candidate shifted to spare {sp}, exam resumed {back}.",
                              "Workstation {ws}: {part}. Spare {sp} given, exam resumed {back}."],
                      move=["Workstation {ws}: candidate asked to move, {why}. Shifted to spare {sp}, resumed {back}.",
                            "Workstation {ws}: candidate requested another seat ({why}). Spare {sp}, resumed {back}."],
                      pause=["Workstation {ws}. {Reason}. Clock stopped {at} to {back}.",
                             "Workstation {ws}: {reason}. Stopped {at}, restarted {back}.",
                             "Workstation {ws}: {reason}. Exam paused {at}, continued {back}."]),
    "Hyderabad": dict(fail=["{ws} hung during the exam, candidate moved to {sp}, resumed {back} hrs",
                            "{ws} not responding, candidate shifted to {sp}, resumed {back} hrs",
                            "{ws} screen frozen, candidate given {sp}, resumed {back} hrs"],
                      late=["{ws} hung near completion, sitting closed with responses saved",
                            "{ws} not responding in the last few minutes, sitting closed with responses saved"],
                      restart=["{ws} hung, system restarted, candidate continued on same system {back} hrs",
                               "{ws} not responding, rebooted, candidate resumed on it {back} hrs"],
                      periph=["{ws} {part}, candidate moved to {sp}, resumed {back} hrs",
                              "{ws} {part}, shifted to {sp}, resumed {back} hrs"],
                      move=["{ws} candidate asked to move ({why}), shifted to {sp}, resumed {back} hrs"],
                      pause=["{ws} {reason}, paused {at} to {back} hrs", "{ws} {reason}, clock stopped {at} to {back} hrs"]),
    "Pune": dict(fail=["System {ws} not responding. Candidate continued on {sp} from {back}.",
                       "System {ws} crashed. Candidate continued on {sp} from {back}.",
                       "System {ws} froze on the item screen. Candidate continued on {sp} from {back}."],
                 late=["System {ws} not responding in the last minutes. Test closed on saved responses.",
                       "System {ws} crashed near the end. Test closed on saved responses."],
                 restart=["System {ws} froze. Restarted; candidate continued on {ws} from {back}.",
                          "System {ws} crashed. Rebooted and the candidate continued on it from {back}."],
                 periph=["System {ws}: {part}. Candidate continued on {sp} from {back}."],
                 move=["System {ws}: candidate asked to move, {why}. Continued on {sp} from {back}."],
                 pause=["System {ws}: {reason}. Paused {at}, restarted {back}.",
                        "System {ws}: {reason}. Clock stopped {at}, started again {back}."]),
    "Kochi": dict(fail=["{ws} screen frozen, candidate seated at {sp}, test resumed at {back}",
                        "{ws} hung, candidate seated at {sp}, resumed {back}",
                        "{ws} stopped working, candidate seated at {sp}, test resumed at {back}"],
                  late=["{ws} screen frozen near the end, sitting closed on saved responses"],
                  restart=["{ws} screen frozen, restarted, candidate resumed on it at {back}",
                           "{ws} hung, rebooted, test resumed at {back}"],
                  periph=["{ws} {part}, candidate seated at {sp}, test resumed at {back}"],
                  move=["{ws} candidate asked to move ({why}), seated at {sp}, resumed {back}"],
                  pause=["{ws} {reason}, paused {at} to {back}", "{ws} {reason}, test paused {at} to {back}"]),
    "Noida": dict(fail=["{ws} crashed. Candidate moved to {sp}, resumed {back}.",
                        "{ws} froze. Candidate moved to {sp}, resumed {back}.",
                        "{ws} stopped responding. Candidate moved to {sp}, resumed {back}."],
                  late=["{ws} crashed just before the end. Sitting closed, responses saved.",
                        "{ws} froze in the final minutes. Sitting closed, responses saved."],
                  restart=["{ws} froze. Restarted, candidate resumed on {ws} at {back}.",
                           "{ws} crashed. Restarted and resumed on the same machine at {back}."],
                  periph=["{ws}: {part}. Candidate moved to {sp}, resumed {back}.",
                          "{ws}: {part}. Moved to {sp}, resumed {back}."],
                  move=["{ws}: candidate asked to move ({why}). Moved to {sp}, resumed {back}."],
                  pause=["{ws}: {reason} ({at} to {back}).", "{ws}: {reason}, clock stopped {at} to {back}."]),
}
# what an invigilator sometimes adds
AFTER = dict(fail=["; {ws} left off for the technician", "; {ws} not used again that session", "", "", ""],
             restart=["; no answers lost", "", "", ""],
             pause=["; candidate given the time back on the clock", "", "", ""])


def typed(ws, cap, rs):
    """the workstation as the invigilator typed it: right, or two digits swapped, or the seat beside"""
    if rs.uniform() >= P_TYPO:
        return ws
    n = int(ws[2:])
    a, b = divmod(n, 10)
    swapped = b * 10 + a
    if a != b and b != 0 and 1 <= swapped <= cap:
        return "WS%02d" % swapped
    m = n + 1 if (rs.uniform() < 0.5 or n == 1) and n < cap else n - 1
    return "WS%02d" % m


def phrase(centre, kind, rs, **kw):
    for k in ("reason", "why"):
        if k in kw:
            kw[k.capitalize()] = kw[k][0].upper() + kw[k][1:]
    opts = STYLE[centre][kind]
    text = opts[int(rs.integers(0, len(opts)))].format(**kw)
    extra = AFTER.get(kind)
    if extra:
        tail = extra[int(rs.integers(0, len(extra)))].format(**kw)
        if tail:
            text = text.rstrip(".") + tail + ("." if text.endswith(".") else "")
    return text


def clock(date, hm, minutes=0.0):
    """local wall time on date at hh:mm plus minutes, as a naive datetime (IST)"""
    return dt.datetime(date.year, date.month, date.day, hm[0], hm[1]) + dt.timedelta(minutes=minutes)


def utc(t):
    return (t - RC.IST).strftime("%Y-%m-%d %H:%M:%S")


def mins(m):
    return dt.timedelta(minutes=float(m))


def secs(s):
    return dt.timedelta(seconds=float(s))


def whole(t):
    return t.replace(microsecond=0)


def outage_times(kd, base, rs):
    """a centre's link loss on one session, provisional: its start and end (end None: down until the session closed;
    end "after": decided once the session's clocks have started)"""
    if kd == "early":                       # before any client of the session has logged in, on past the last start
        return base - mins(rs.uniform(21, 26)), "after"
    if kd == "tutorial":                    # while most of the session is in the tutorial, back before any clock starts
        t0 = base - mins(rs.uniform(9, 11))
        return t0, t0 + mins(rs.uniform(2, 3))
    if kd == "straddle":
        return base - mins(rs.uniform(4, 7)), "after"
    if kd == "late":
        return base + mins(rs.uniform(222, 232)), None
    t0 = base + mins(rs.uniform(110, 185))
    return t0, t0 + mins(rs.uniform(6, 18))


def ask_a(W, R, rs):
    rows, sched = W["rows"], R["sched"]
    idx = [i for i, r in enumerate(rows) if r["w"] >= 4]
    seat, events, reports = [], [], []
    truth, device = {}, {k: set() for k in ("quiet_restart", "unreported_pause", "switch_off", "fault", "hall_stop",
                                            "unreported_fail")}
    sess_of = {}
    for i in idx:
        s = sched[i]
        sess_of.setdefault((s["centre"], s["date"], s["session"]), []).append(i)
        seat.append(dict(booking_ref=s["booking_ref"], centre_code=P.CENTRE_CODE[s["centre"]], session_date=s["date"].isoformat(),
                         session=s["session"], workstation=s["workstation"]))
    tut, start, used = {}, {}, {}
    for i in idx:
        s = sched[i]
        start[i] = clock(s["date"], RC.SESSION_START[s["session"]], float(rs.uniform(0, 9)))
        tut[i] = start[i] - mins(np.clip(rs.lognormal(np.log(9.0), 0.25), 5.5, 19.0))
        used[i] = float(rows[i]["ms"].sum()) / 60000.0
    power_key = (POWER["centre"], RC.window_day(POWER["window"], POWER["day"]), POWER["session"])
    halls = {}
    for h in HALL_STOPS:
        hd = RC.window_day(h["window"], h["day"])
        halls[(h["centre"], hd, h["session"])] = dict(
            spec=h, at=clock(hd, h["at"]), stop=clock(hd, h["at"], h["stop"]), off=clock(hd, h["at"], float(rs.uniform(*h["off"]))),
            on=clock(hd, h["at"], float(rs.uniform(*h["on"]))), back=clock(hd, h["at"], float(rs.uniform(*h["back"]))))
    plans = {}
    for w in range(4, 8):
        days = [RC.window_day(w, d) for d in range(P.WINDOW_DAYS)]
        for kd in ["mid", "mid", "mid_flap", "early", "straddle", "tutorial", "late"]:
            for _ in range(500):
                c = P.CENTRES[int(rs.integers(0, len(P.CENTRES)))]
                d = days[int(rs.integers(0, len(days)))]
                sess = "AM" if rs.uniform() < 0.5 else "PM"
                key = (c, d, sess)
                if key != power_key and key not in halls and key in sess_of and key not in plans:
                    break
            t0, t1 = outage_times(kd, clock(d, RC.SESSION_START[sess]), rs)
            plans[key] = dict(kd=kd, t0=t0, t1=t1, spread=float(rs.uniform(5, 60)))
    pdate = power_key[1]
    cut, pback = clock(pdate, POWER["cut"]), clock(pdate, POWER["back"])

    info = {}                               # booking -> the sitting's record
    for key in sorted(sess_of, key=lambda k: (k[1], P.CENTRES.index(k[0]), k[2])):
        ii = sess_of[key]
        c, d, sess = key
        code, cap = P.CENTRE_CODE[c], RC.WORKSTATIONS[c]
        plan = plans.get(key)
        if plan and plan["t1"] == "after":
            plan["t1"] = max(start[i] for i in ii) + mins(rs.uniform(1.5, 6))
        keep_out = []                       # stretches no incident may come near
        if plan:
            keep_out.append((plan["t0"] - mins(15), (plan["t1"] or clock(d, RC.SESSION_START[sess], 330)) + mins(15)))
        hall = halls.get(key)
        if hall:
            keep_out.append((hall["at"] - mins(15), hall["back"] + mins(15)))
        faulted = False
        S = {}
        for i in ii:
            r, s = rows[i], sched[i]
            b_ = s["booking_ref"]
            st = start[i]
            reached = bool(r["reach"][-1])
            exam = used[i] + float(rs.uniform(0.5, 6)) if reached else P.LIMIT / 60
            rec = dict(i=i, b=b_, ws=s["workstation"], st=st, tut=tut[i], exam=exam, reached=reached, kind=None,
                       stops=[], segs=[[tut[i], None, s["workstation"]]], ev=[], end=None)
            S[i] = rec
            u = rs.uniform()
            if key == power_key and st + mins(used[i]) > cut:
                rec["kind"] = "power"
            elif hall and st < hall["stop"] - mins(2) and st + mins(exam) > hall["stop"] + mins(1):
                rec["kind"] = "hall"
            elif u < P_FAIL:
                rec["kind"] = "late" if reached and rs.uniform() < P_LATE else "fail"
            elif u < P_FAIL + P_RESTART:
                rec["kind"] = "restart"
            elif u < P_FAIL + P_RESTART + P_PERIPH:
                rec["kind"] = "periph"
            elif u < P_FAIL + P_RESTART + P_PERIPH + P_MOVE:
                rec["kind"] = "move"
            elif u < P_FAIL + P_RESTART + P_PERIPH + P_MOVE + P_PAUSE:
                rec["kind"] = "pause"
            elif u < P_FAIL + P_RESTART + P_PERIPH + P_MOVE + P_PAUSE + P_FAULT and not plan and key != power_key and not hall \
                    and not faulted and used[i] > 90:
                rec["kind"] = "fault"
                faulted = True
            k = rec["kind"]
            if k in ("fail", "late", "restart", "periph", "move", "pause"):
                for _ in range(50):
                    if k == "late":
                        at = st + mins(rs.uniform(max(5.0, used[i] - 4.5), max(6.0, used[i] - 0.5)))
                        span = (at - mins(2), at + mins(9))
                    else:
                        at = st + mins(rs.uniform(5, max(6.0, used[i] - 3)))
                        span = (at - mins(2), at + mins(18))
                    if all(span[1] < a or span[0] > z for a, z in keep_out):
                        break
                else:
                    rec["kind"] = k = None
                if k:
                    rec["at"] = at
            elif k == "fault":
                rec["lf"] = st + mins(rs.uniform(25, used[i] - 60))
                rec["dur"] = float(rs.uniform(8, 35))
        # each incident's stop and resume
        for i, rec in S.items():
            k = rec["kind"]
            if k == "power":
                back = pback + mins(rs.uniform(4, 9))
                rec["stops"].append((cut + mins(4.0), back))
                rec["resume"] = (back, rec["ws"])
                rec["segs"][0][1] = cut + mins(4.0)
                rec["segs"].append([back, None, rec["ws"]])
            elif k == "hall":
                back = hall["back"] + mins(rs.uniform(0, 4))
                rec["stops"].append((hall["stop"], back))
                rec["resume"] = (back, rec["ws"])
            elif k in ("fail", "periph", "move"):
                rec["gap"] = float(rs.uniform(2, 5) if k == "move" else rs.uniform(4, 9))
            elif k == "restart":
                rec["R"] = float(rs.uniform(1.2, 4.6))
                rec["gap"] = rec["R"] + float(rs.uniform(0.6, 2.0))
            elif k == "pause":
                rec["gap"] = float(rs.uniform(5, 14))
        # moves to a spare in the order they happen: the lowest spare free at the resume
        free = {"SP%02d" % (q + 1): dt.datetime.min for q in range(RC.SPARES)}

        def place(rec):
            back = rec["at"] + mins(rec["gap"])
            for sp in sorted(free):
                if free[sp] <= back - mins(1):
                    rec["sp"] = sp
                    return True
            return False

        def finish(rec):
            """the sitting's stops, segments and end from its incident"""
            k = rec["kind"]
            if k in ("fail", "periph", "move", "hang"):
                back = rec["at"] + mins(rec["gap"])
                rec["stops"].append((rec["at"], back))
                rec["resume"] = (back, rec["sp"])
                rec["segs"][0][1] = rec["at"]
                rec["segs"].append([back, None, rec["sp"]])
            elif k in ("restart", "pause"):
                back = rec["at"] + mins(rec["gap"])
                rec["stops"].append((rec["at"], back))
                rec["resume"] = (back, rec["ws"])
                if k == "restart":
                    rec["segs"][0][1] = rec["at"]
                    rec["segs"].append([back, None, rec["ws"]])
            if k == "late":
                rec["end"] = rec["at"] + mins(rs.uniform(3.6, 7.0))
                rec["segs"][0][1] = rec["at"]
            else:
                down = sum((z - a).total_seconds() for a, z in rec["stops"]) / 60
                rec["end"] = rec["st"] + mins(rec["exam"] + down)
            if "sp" in rec:
                free[rec["sp"]] = rec["end"] + mins(2)

        movers = sorted([rec for rec in S.values() if rec["kind"] in ("fail", "periph", "move")],
                        key=lambda q: q["at"] + mins(q["gap"]))
        for rec in movers:
            if not place(rec):
                if rec["kind"] == "fail":
                    rec["kind"] = "restart"
                    rec["R"] = float(rs.uniform(1.2, 4.6))
                    rec["gap"] = rec["R"] + float(rs.uniform(0.6, 2.0))
                else:
                    rec["kind"] = None
            finish(rec)
        for rec in S.values():
            if rec["end"] is None:
                finish(rec)
        # the link loss's final times: no clock starts, ends or resumes within a client's notice of either edge (the
    # incidents keep fifteen minutes clear of where it was planned, the edges move ten minutes at most)
        if plan:
            marks = sorted([rec["st"] for rec in S.values()] + [rec["end"] for rec in S.values()] +
                           [rec["resume"][0] for rec in S.values() if "resume" in rec])
            sp_ = plan["spread"]
            wide = 100 if plan["kd"] == "mid_flap" else 0

            def clean(t, extra):
                lo, hi = t - secs(5), t + secs(sp_ + 5 + extra)
                return not any(lo <= m <= hi for m in marks)

            for edge, extra in (("t0", wide), ("t1", 0)):
                t = plan[edge]
                if t is None:
                    continue
                if plan["kd"] in ("mid", "mid_flap", "late") or not clean(t, extra):
                    for k_ in [int(q) for q in rs.permutation(np.arange(-60, 61))]:
                        tt = t + secs(10 * k_)
                        long_enough = edge == "t0" or tt >= plan["t0"] + secs(sp_ + wide) + mins(6)
                        if clean(tt, extra) and long_enough:
                            plan[edge] = tt
                            break
                    else:
                        raise RuntimeError("no clean edge for %s" % (key,))
            # clients that hang as the link drops: they go to a spare
            if plan["kd"] in ("mid", "mid_flap", "late"):
                for rec in sorted(S.values(), key=lambda q: q["i"]):
                    if rec["kind"] is not None or not (rec["st"] < plan["t0"] - mins(1) and rec["end"] > plan["t0"] + mins(2)):
                        continue
                    if rs.uniform() >= P_HANG:
                        continue
                    lost = plan["t0"] + secs(rs.uniform(0, plan["spread"]))
                    at = lost + secs(rs.uniform(5, 40))
                    old_end = rec["end"]
                    for _ in range(20):
                        gap = float(rs.uniform(4, 9))
                        new_end = old_end + mins(gap)
                        t1_ = plan["t1"]
                        ok_ = t1_ is None or not (t1_ - secs(5) <= new_end <= t1_ + secs(plan["spread"] + 5))
                        if ok_:
                            break
                    rec.update(kind="hang", lost=lost, at=at, gap=gap, end=None)
                    if place(rec):
                        finish(rec)
                    else:
                        rec.update(kind="hang_restart")
                        back = at + mins(gap)
                        rec["stops"].append((at, back))
                        rec["resume"] = (back, rec["ws"])
                        rec["segs"][0][1] = at
                        rec["segs"].append([back, None, rec["ws"]])
                        down = sum((z - a).total_seconds() for a, z in rec["stops"]) / 60
                        rec["end"] = rec["st"] + mins(rec["exam"] + down)
        close = max(rec["end"] for rec in S.values()) + mins(rs.uniform(3, 10))
        # finished candidates' workstations an invigilator switched off before the session closed
        for rec in sorted(S.values(), key=lambda q: q["i"]):
            if rec["kind"] is None and rec["reached"] and key != power_key and not hall and rs.uniform() < P_OFF:
                off = rec["end"] + mins(rs.uniform(2, 25))
                fail_at = off + mins(SILENCE) + secs(rs.uniform(0, 20))
                blocked = plan and plan["t0"] - mins(2) <= fail_at <= (plan["t1"] or close) + mins(2)
                if fail_at < close - mins(0.5) and not blocked:
                    rec.update(kind="off", off=off, fail_at=fail_at)
                    rec["segs"][-1][1] = off
        # the events each sitting leaves
        for rec in S.values():
            b_, ws, k = rec["b"], rec["ws"], rec["kind"]
            E = lambda t, wsx, e, b=b_: events.append(dict(t=t, centre_code=code, workstation=wsx, event=e, booking_ref=b))
            E(rec["tut"], ws, "TUTORIAL_START")
            E(rec["st"], ws, "SESSION_START")
            if k in ("fail", "late"):
                E(rec["at"] + mins(SILENCE) + secs(rs.uniform(0, 20)), ws, "WS_FAIL")
            if k == "restart":
                if rec["R"] > SILENCE:
                    E(rec["at"] + mins(SILENCE) + secs(rs.uniform(0, 20)), ws, "WS_FAIL")
                E(rec["at"] + mins(rec["R"]), ws, "WS_REBOOT", "")
            if k == "hang_restart":
                E(rec["at"] + mins(rec["gap"]) - mins(rs.uniform(0.6, 1.5)), ws, "WS_REBOOT", "")
            if "resume" in rec:
                E(rec["resume"][0], rec["resume"][1], "SESSION_RESUME")
            end_ws = rec["segs"][-1][2]
            E(rec["end"], end_ws, "SESSION_END")
            if k == "off":
                E(rec["fail_at"], ws, "WS_FAIL")
                device["switch_off"].add(b_)
            if k == "fault":
                lf = rec["lf"]
                E(lf + secs(rs.uniform(5, 60)), ws, "NET_LOST")
                E(lf + mins(SILENCE) + secs(rs.uniform(0, 20)), ws, "WS_FAIL")
                E(lf + mins(rec["dur"]) + secs(rs.uniform(5, 60)), ws, "NET_BACK")
                device["fault"].add(b_)
            if k == "hall":
                device["hall_stop"].add(b_)
            # the invigilators' reports
            kind_rep = {"fail": "fail", "late": "late", "restart": "restart", "periph": "periph", "move": "move",
                        "pause": "pause", "hang": "fail", "hang_restart": "restart"}.get(k)
            if kind_rep:
                share = REPORTED["hang"] if k in ("hang", "hang_restart") else REPORTED[k]
                if rs.uniform() < share:
                    wr = typed(ws, cap, rs)
                    at = rec["at"]
                    back = rec.get("resume", (None,))[0]
                    kw = dict(ws=wr, at=at.strftime("%H:%M"))
                    if back is not None:
                        kw["back"] = back.strftime("%H:%M")
                    if "sp" in rec:
                        kw["sp"] = rec["sp"]
                    if k == "periph":
                        kw["part"] = PARTS[int(rs.integers(0, len(PARTS)))]
                    if k == "move":
                        kw["why"] = WHY[int(rs.integers(0, len(WHY)))]
                    if k == "pause":
                        kw["reason"] = PAUSE_REASONS[int(rs.integers(0, len(PAUSE_REASONS)))]
                    reports.append(dict(centre=c, date=d, session=sess, time=at.strftime("%H:%M"), workstation=wr,
                                        incident=phrase(c, kind_rep, rs, **kw)))
                elif k == "restart" and rec["R"] <= SILENCE:
                    device["quiet_restart"].add(b_)
                elif k == "pause":
                    device["unreported_pause"].add(b_)
                elif k in ("fail", "late"):
                    device["unreported_fail"].add(b_)
            if k in ("fail", "late", "restart", "periph", "hang", "hang_restart", "power"):
                truth[b_] = k
        for rec in S.values():
            rec["close"] = close
            info[rec["b"]] = rec
        # the link losses each client logged
        losses = []
        if plan:
            losses.append((plan["kd"], plan["t0"], plan["t1"], plan["spread"]))
        if hall:
            losses.append(("hall", hall["off"], hall["on"], float(rs.uniform(5, 60))))
        for kd, t0, t1, spread in losses:
            hi_end = close
            for rec in sorted(S.values(), key=lambda q: q["i"]):
                b_ = rec["b"]
                for a, z, wsx in rec["segs"]:
                    z = z or hi_end
                    if a >= (t1 or hi_end) or z <= t0:
                        continue
                    ivs = []
                    if a <= t0:
                        L = rec["lost"] if "lost" in rec and wsx == rec["ws"] else t0 + secs(rs.uniform(0, spread))
                        if L >= z:
                            continue
                        events.append(dict(t=L, centre_code=code, workstation=wsx, event="NET_LOST", booking_ref=b_))
                        if kd == "mid_flap" and L + secs(95) < z:
                            events.append(dict(t=L + secs(40), centre_code=code, workstation=wsx, event="NET_BACK", booking_ref=b_))
                            events.append(dict(t=L + secs(95), centre_code=code, workstation=wsx, event="NET_LOST", booking_ref=b_))
                            ivs.append((L, L + secs(40)))
                            lo = L + secs(95)
                        else:
                            lo = L
                    else:
                        lo = a
                    hi = z
                    if t1 is not None:
                        Bk = t1 + secs(rs.uniform(0, spread))
                        if Bk < z:
                            events.append(dict(t=Bk, centre_code=code, workstation=wsx, event="NET_BACK", booking_ref=b_))
                            hi = Bk
                    ivs.append((lo, hi))
                    rec.setdefault("offline_ivs", []).extend(ivs)
    # the power cut: one report; the log holds nothing at Kochi while the server was down
    reports.append(dict(centre=POWER["centre"], date=pdate, session="AM", time="%02d:%02d" % POWER["cut"], workstation="",
                        incident="Power cut in the examination hall at 11:05. The router and the local server went down at "
                                 "once; the UPS carried the workstations for about four minutes, then they went down too. "
                                 "Mains back at 11:31; candidates resumed on their own workstations as the server came back."))
    pcode = P.CENTRE_CODE[POWER["centre"]]
    events = [e for e in events if not (e["centre_code"] == pcode and cut <= e["t"] < pback)]
    for q in range(RC.WORKSTATIONS[POWER["centre"]]):
        events.append(dict(t=pback + mins(rs.uniform(1.0, 3.2)), centre_code=pcode, workstation="WS%02d" % (q + 1),
                           event="WS_REBOOT", booking_ref=""))
    for q in range(RC.SPARES):
        events.append(dict(t=pback + mins(rs.uniform(1.0, 3.2)), centre_code=pcode, workstation="SP%02d" % (q + 1),
                           event="WS_REBOOT", booking_ref=""))
    # the hall stops: one report each
    for key, hall in halls.items():
        h, f = hall["spec"], (lambda t: t.strftime("%H:%M"))
        if h["text"] == "smoke":
            text = ("Fire alarm at %s: smoke from the UPS in the communications cabinet. All clocks stopped at %s and the "
                    "hall cleared. Facilities switched off the cabinet's UPS and the router at %s; the router was back on "
                    "the mains at %s. Candidates back in the hall and resumed on their own workstations from %s."
                    % (f(hall["at"]), f(hall["stop"]), f(hall["off"]), f(hall["on"]), f(hall["back"])))
        else:
            text = ("Building management gave notice at %s of a switch of the building's power to the generator. All "
                    "clocks stopped at %s as a precaution. The hall stayed on its UPS throughout; the router, on the "
                    "building supply, went off at %s and the link to Pariksha was back at %s. Clocks restarted from %s."
                    % (f(hall["at"]), f(hall["stop"]), f(hall["off"]), f(hall["on"]), f(hall["back"])))
        reports.append(dict(centre=key[0], date=key[1], session=key[2], time=f(hall["at"]), workstation="", incident=text))
    # the truth for the link item: each client's logged loss of the centre's link while its sitting's clock ran
    offline = set()
    for b_, rec in info.items():
        if rec["kind"] == "power":
            offline.add(b_)
            continue
        run = [(whole(rec["st"]), whole(rec["end"]))]
        for a, z in sorted(rec["stops"]):
            nxt = []
            for p, q in run:
                if z <= p or a >= q:
                    nxt.append((p, q))
                    continue
                if p < whole(a):
                    nxt.append((p, whole(a)))
                if whole(z) < q:
                    nxt.append((whole(z), q))
            run = nxt
        for lo, hi in rec.get("offline_ivs", []):
            if any(max(p, whole(lo)) < min(q, whole(hi)) for p, q in run):
                offline.add(b_)
                break
    # routine reboots between the sessions, on a workstation nobody is using
    busy = {}
    for b_, rec in info.items():
        for a, z, wsx in rec["segs"]:
            busy.setdefault((sched[rec["i"]]["centre"], a.date(), wsx), []).append((a, z or rec["close"]))
    for w in range(4, 8):
        for dd in range(P.WINDOW_DAYS):
            for c in P.CENTRES:
                if rs.uniform() < 0.35:
                    day = RC.window_day(w, dd)
                    t = clock(day, (13, 50), float(rs.uniform(0, 25)))
                    for _ in range(10):
                        wsx = "WS%02d" % rs.integers(1, RC.WORKSTATIONS[c] + 1)
                        if not any(a - mins(3) <= t <= z + mins(3) for a, z in busy.get((c, day, wsx), [])):
                            events.append(dict(t=t, centre_code=P.CENTRE_CODE[c], workstation=wsx, event="WS_REBOOT",
                                               booking_ref=""))
                            break
    ev = pd.DataFrame(events).sort_values(["t", "centre_code", "workstation", "event"]).reset_index(drop=True)
    ev.insert(0, "event_utc", [utc(t) for t in ev["t"]])
    ev = ev.drop(columns=["t"])
    rep = pd.DataFrame(reports)
    rep = rep.sort_values(["centre", "date", "session", "time"]).reset_index(drop=True)
    seatdf = pd.DataFrame(seat).sort_values(["session_date", "centre_code", "session", "workstation"]).reset_index(drop=True)
    return dict(events=ev, reports=rep, seat=seatdf, truth=truth, offline=offline, plans=plans, device=device,
                info=info, halls=halls)


def ask_b(W, R, rs):
    """the bank officer's log of the panel's decisions on tried items (2026 and 2027 windows): entered a few days after
    each meeting, the December 2027 meeting's on 4 to 6 January 2028; three acceptances withdrawn later in 2027;
    the October batch entered twice after a failed save"""
    dec, ids = R["dec"], R["ids"]
    out, logged = [], {}
    entry = 0
    by_w = {}
    for j, d in dec.items():
        by_w.setdefault(d["w"], []).append(j)
    withdrawn = set()
    for w in sorted(by_w):
        items = sorted(by_w[w], key=lambda j: ids["new"][j])
        meet = RC.PANEL[w]
        for j in [items[q] for q in rs.permutation(len(items))]:
            if w == 7:
                on = dt.date(2028, 1, 4) + dt.timedelta(days=int(rs.integers(0, 3)))
            else:
                on = meet + dt.timedelta(days=int(rs.integers(1, 5)))
            iid = ids["old"][j] if on < RC.MIGRATION else ids["new"][j]
            out.append(dict(item_id=iid, decision=dec[j]["decision"], logged_on=on))
            logged[j] = (dec[j]["decision"], on)
            if w == 6 and rs.uniform() < 0.25:
                out.append(dict(item_id=iid, decision=dec[j]["decision"], logged_on=on + dt.timedelta(days=1)))
        if w in (4, 5):
            acc = [j for j in items if dec[j]["decision"] == "accept"]
            for j in [acc[q] for q in rs.choice(len(acc), 2 if w == 4 else 1, replace=False)]:
                on = RC.PANEL[w + 1] + dt.timedelta(days=int(rs.integers(1, 5)))
                out.append(dict(item_id=ids["new"][j], decision="withdraw", logged_on=on))
                logged[j] = ("withdraw", on)
                withdrawn.add(j)
    df = pd.DataFrame(out).sort_values(["logged_on", "item_id"]).reset_index(drop=True)
    df.insert(0, "entry_no", ["PD-%05d" % (k + 1) for k in range(len(df))])
    df["logged_on"] = [d.isoformat() for d in df["logged_on"]]
    # the golden: 2027 windows' tried items whose last 2027-meeting decision is accept
    gold = {a: 0 for a in P.AREAS}
    for j, d in dec.items():
        if d["w"] >= 4 and d["decision"] == "accept" and j not in withdrawn:
            gold[P.AREAS[W["B"]["area"][j]]] += 1
    return dict(log=df, logged=logged, withdrawn=withdrawn, gold=gold)


def build(W, R, seed=P.SEED):
    # the asks' own stream; the shift is the first at which every route short of the golden misses every form's figure
    # on both items (checks.py asserts it on the cut pack)
    ss = np.random.SeedSequence(seed + 307)
    ra, rb = [np.random.default_rng(s) for s in ss.spawn(2)]
    return dict(a=ask_a(W, R, ra), panel=ask_b(W, R, rb))
