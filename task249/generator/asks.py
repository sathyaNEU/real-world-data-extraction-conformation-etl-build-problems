"""The asks' records, on rows the call never reads.

Ask A (each form's 2027 sittings a workstation or power failure interrupted) and the integrity report's link item
(each form's 2027 sittings that ran in part without the centre's link): the provider's seat plan, its workstation event
log (UTC) and the centres' invigilator incident reports (local time).

The provider's server logs WS_FAIL when it stops hearing a workstation while it still hears the centre. A client that
hangs as the centre's link drops under it leaves no WS_FAIL (the server hears nobody at that centre), and nor does a
keyboard, mouse or screen that fails under a running computer; the invigilator stops the clock and moves the candidate
to a spare, and reports it. A change of seat at the candidate's request also ends on a spare, reported as a request.
Every incident the invigilators handle is reported except that about three in ten failures the server logged go
unreported, and about one report in ten carries the workstation's number typed wrong (two digits swapped, or the seat
beside); the spare and the resume time it names are right. On 19 August 2027 a power cut at Kochi took the router and the local server down at once while the UPS
carried the workstations for about four minutes: the log has nothing for half an hour and then each sitting resumes on
its own workstation.

A centre's link loss is logged by each client logged in at the time (NET_LOST, NET_BACK, the candidate's booking), a
finished candidate's too, until the session closes; a client that logs in while the link is down logs only NET_BACK
when it comes back.   A = asks.build(W, R)

Ask B of an earlier layer (each content area's trial items standing accepted) ships as the panel's decision log, a
distractor."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import records as RC

P_FAIL = 0.0062      # the computer froze or crashed
P_PERIPH = 0.0016    # a keyboard, mouse or screen failed under a running computer
P_MOVE = 0.0013      # a change of seat at the candidate's request
P_PAUSE = 0.0040
P_HANG = 0.07        # a running client that hangs when the centre's link drops
P_REPORTED = 0.7     # failures the server logged that the invigilators also report
POWER = dict(window=6, centre="Kochi", day=10, session="AM", cut=(11, 5), back=(11, 31))
PAUSE_REASONS = ["candidate unwell", "candidate's ID re-checked at the desk", "code book checked at the desk for added notes",
                 "candidate left for the washroom"]
PARTS = ["keyboard stopped working", "mouse stopped responding", "screen went blank"]
WHY = ["glare from the window", "noise from the corridor", "a wobbling desk", "a candidate coughing beside them"]
# each centre's invigilators write their reports in their own way
STYLE = {
    "Chennai": dict(fail=["{ws} stopped responding; candidate moved to {sp} and resumed at {back}",
                          "{ws} froze; candidate shifted to {sp}, resumed {back}"],
                    late=["{ws} stopped responding near the end; sitting closed on the saved responses"],
                    periph=["{ws}: {part}; candidate moved to {sp} and resumed at {back}"],
                    move=["{ws}: candidate asked to move ({why}); moved to {sp}, resumed at {back}"],
                    pause=["{ws}: {reason}, paused from {at} to {back}", "{ws}: {reason}; clock stopped {at} to {back}"]),
    "Bengaluru": dict(fail=["Workstation {ws} froze. Candidate shifted to spare {sp}, exam resumed {back}.",
                            "Workstation {ws} hung. Spare {sp} given, exam resumed {back}."],
                      late=["Workstation {ws} froze with a few minutes left. Sitting ended on the saved answers."],
                      periph=["Workstation {ws}: {part}. Candidate shifted to spare {sp}, exam resumed {back}."],
                      move=["Workstation {ws}: candidate asked to move, {why}. Shifted to spare {sp}, resumed {back}."],
                      pause=["Workstation {ws}. {Reason}. Clock stopped {at} to {back}.",
                             "Workstation {ws}: {reason}. Stopped {at}, restarted {back}."]),
    "Hyderabad": dict(fail=["{ws} hung during the exam, candidate moved to {sp}, resumed {back} hrs",
                            "{ws} not responding, candidate shifted to {sp}, resumed {back} hrs"],
                      late=["{ws} hung near completion, sitting closed with responses saved"],
                      periph=["{ws} {part}, candidate moved to {sp}, resumed {back} hrs"],
                      move=["{ws} candidate asked to move ({why}), shifted to {sp}, resumed {back} hrs"],
                      pause=["{ws} {reason}, paused {at} to {back} hrs"]),
    "Pune": dict(fail=["System {ws} not responding. Candidate continued on {sp} from {back}.",
                       "System {ws} crashed. Candidate continued on {sp} from {back}."],
                 late=["System {ws} not responding in the last minutes. Test closed on saved responses."],
                 periph=["System {ws}: {part}. Candidate continued on {sp} from {back}."],
                 move=["System {ws}: candidate asked to move, {why}. Continued on {sp} from {back}."],
                 pause=["System {ws}: {reason}. Paused {at}, restarted {back}."]),
    "Kochi": dict(fail=["{ws} screen frozen, candidate seated at {sp}, test resumed at {back}",
                        "{ws} hung, candidate seated at {sp}, resumed {back}"],
                  late=["{ws} screen frozen near the end, sitting closed on saved responses"],
                  periph=["{ws} {part}, candidate seated at {sp}, test resumed at {back}"],
                  move=["{ws} candidate asked to move ({why}), seated at {sp}, resumed {back}"],
                  pause=["{ws} {reason}, paused {at} to {back}"]),
    "Noida": dict(fail=["{ws} crashed. Candidate moved to {sp}, resumed {back}.",
                        "{ws} froze. Candidate moved to {sp}, resumed {back}."],
                  late=["{ws} crashed just before the end. Sitting closed, responses saved."],
                  periph=["{ws}: {part}. Candidate moved to {sp}, resumed {back}."],
                  move=["{ws}: candidate asked to move ({why}). Moved to {sp}, resumed {back}."],
                  pause=["{ws}: {reason} ({at} to {back})."]),
}


P_TYPO = 0.10        # a workstation number typed wrong in a report (digits swapped, or the seat beside)


def typed(ws, rs):
    """the workstation as the invigilator typed it"""
    if rs.uniform() >= P_TYPO:
        return ws
    n = int(ws[2:])
    a, b = divmod(n, 10)
    m = b * 10 + a if (a != b and b != 0) else (n + 1 if rs.uniform() < 0.5 or n == 1 else n - 1)
    return "WS%02d" % m


def phrase(centre, kind, rs, **kw):
    for k in ("reason", "why"):
        if k in kw:
            kw[k.capitalize()] = kw[k][0].upper() + kw[k][1:]
    opts = STYLE[centre][kind]
    return opts[int(rs.integers(0, len(opts)))].format(**kw)


def clock(date, hm, minutes=0.0):
    """local wall time on date at hh:mm plus minutes, as a naive datetime (IST)"""
    return dt.datetime(date.year, date.month, date.day, hm[0], hm[1]) + dt.timedelta(minutes=minutes)


def utc(t):
    return (t - RC.IST).strftime("%Y-%m-%d %H:%M:%S")


def mins(m):
    return dt.timedelta(minutes=float(m))


def outage_times(kd, base, rs):
    """a centre's link loss on one session: its start and end (end None: down until the session closed)"""
    if kd == "early":                       # before any client of the session has logged in
        return base - mins(rs.uniform(21, 26)), base + mins(rs.uniform(3, 12))
    if kd == "tutorial":
        t0 = base - mins(rs.uniform(13, 16))
        return t0, t0 + mins(rs.uniform(2, 3.5))
    if kd == "straddle":
        return base - mins(rs.uniform(4, 7)), base + mins(rs.uniform(6, 12))
    if kd == "late":
        return base + mins(rs.uniform(222, 232)), None
    t0 = base + mins(rs.uniform(110, 205))
    return t0, t0 + mins(rs.uniform(6, 18))


def ask_a(W, R, rs):
    rows, sched = W["rows"], R["sched"]
    idx = [i for i, r in enumerate(rows) if r["w"] >= 4]
    seat, events, reports, truth = [], [], [], {}
    power_key = (POWER["centre"], RC.window_day(POWER["window"], POWER["day"]), POWER["session"])
    sess_of = {}
    for i in idx:
        s = sched[i]
        sess_of.setdefault((s["centre"], s["date"], s["session"]), []).append(i)
        seat.append(dict(booking_ref=s["booking_ref"], centre_code=P.CENTRE_CODE[s["centre"]], session_date=s["date"].isoformat(),
                         session=s["session"], workstation=s["workstation"]))
    # each sitting's tutorial, clock start and examination minutes used
    tut, start, used = {}, {}, {}
    for i in idx:
        s = sched[i]
        start[i] = clock(s["date"], RC.SESSION_START[s["session"]], float(rs.uniform(0, 9)))
        tut[i] = start[i] - mins(np.clip(rs.lognormal(np.log(9.0), 0.25), 5.5, 19.0))
        used[i] = float(rows[i]["ms"].sum()) / 60000.0
    # the centres' link losses, planned before the incidents so that a stop never sits inside one
    plans = []
    for w in range(4, 8):
        days = [RC.window_day(w, d) for d in range(P.WINDOW_DAYS)]
        for kd in ["mid", "mid", "mid_flap", "early", "straddle", "tutorial", "late"]:
            for _ in range(500):
                c = P.CENTRES[int(rs.integers(0, len(P.CENTRES)))]
                d = days[int(rs.integers(0, len(days)))]
                sess = "AM" if rs.uniform() < 0.5 else "PM"
                key = (c, d, sess)
                if key != power_key and key in sess_of and key not in [p[0] for p in plans]:
                    break
            t0, t1 = outage_times(kd, clock(d, RC.SESSION_START[sess]), rs)
            plans.append((key, kd, t0, t1, float(rs.uniform(5, 60))))
    out_of = {p[0]: p for p in plans}
    spare_next = {}
    seg = {}            # booking -> list of client segments [login, logout or hang, workstation]
    stop_at, end_of = {}, {}
    for i in idx:
        r, s = rows[i], sched[i]
        b_, ws, code = s["booking_ref"], s["workstation"], P.CENTRE_CODE[s["centre"]]
        key = (s["centre"], s["date"], s["session"])
        st = start[i]
        events.append(dict(t=tut[i], centre_code=code, workstation=ws, event="TUTORIAL_START", booking_ref=b_))
        events.append(dict(t=st, centre_code=code, workstation=ws, event="SESSION_START", booking_ref=b_))
        plan = out_of.get(key)
        planned_end = st + mins(P.LIMIT / 60 if not r["reach"][-1] else used[i] + 3)
        u = rs.uniform()
        kind = None
        if key == power_key and st + mins(used[i]) > clock(s["date"], POWER["cut"]):
            kind = "power"
        elif plan and plan[1] in ("mid", "mid_flap", "late") and st < plan[2] - mins(1) and planned_end > plan[2] + mins(2) \
                and rs.uniform() < P_HANG:
            kind = "hang"
        elif u < P_FAIL:
            kind = "fail"
        elif u < P_FAIL + P_PERIPH:
            kind = "periph"
        elif u < P_FAIL + P_PERIPH + P_MOVE:
            kind = "move"
        elif u < P_FAIL + P_PERIPH + P_MOVE + P_PAUSE:
            kind = "pause"
        downtime, end_ws = 0.0, ws
        segs = [[tut[i], None, ws]]
        if kind in ("fail", "periph", "move", "pause"):
            late = kind == "fail" and rs.uniform() < 0.14 and r["reach"][-1]
            for _ in range(50):
                at = st + (mins(rs.uniform(max(5.0, used[i] - 4.5), max(6.0, used[i] - 0.5))) if late
                           else mins(rs.uniform(5, max(6.0, used[i] - 3))))
                gap = float(rs.uniform(2, 5) if kind == "move" else rs.uniform(5, 14) if kind == "pause" else rs.uniform(4, 9))
                lo, hi = at - mins(2), at + mins(gap + 2)
                if not plan or hi < plan[2] or lo > (plan[3] or planned_end + mins(30)):
                    break
            else:
                kind = None
        if kind == "power":
            cut = clock(s["date"], POWER["cut"])
            back = clock(s["date"], POWER["back"]) + mins(rs.uniform(4, 9))
            downtime = (back - cut).total_seconds() / 60
            events.append(dict(t=back, centre_code=code, workstation=ws, event="SESSION_RESUME", booking_ref=b_))
            truth[b_] = "power"
        elif kind == "hang":
            lost = plan[2] + dt.timedelta(seconds=float(rs.uniform(0, plan[4])))
            at = lost + dt.timedelta(seconds=float(rs.uniform(5, 40)))
            stop_at[b_] = (lost, at)
        elif kind in ("fail", "periph", "move", "pause"):
            if kind == "fail":
                events.append(dict(t=at, centre_code=code, workstation=ws, event="WS_FAIL", booking_ref=b_))
            if late:
                end_at = at + mins(rs.uniform(2, 6))
                events.append(dict(t=end_at, centre_code=code, workstation=ws, event="SESSION_END", booking_ref=b_))
                end_of[b_] = end_at
                segs[0][1] = end_at
                seg[b_] = segs
                truth[b_] = "fail"
                if rs.uniform() < P_REPORTED:
                    wr = typed(ws, rs)
                    reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                        workstation=wr, incident=phrase(s["centre"], "late", rs, ws=wr)))
                continue
            back = at + mins(gap)
            downtime = gap
            if kind == "pause":
                events.append(dict(t=back, centre_code=code, workstation=ws, event="SESSION_RESUME", booking_ref=b_))
                wr = typed(ws, rs)
                reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                    workstation=wr, incident=phrase(s["centre"], "pause", rs, ws=wr,
                                                                    reason=PAUSE_REASONS[int(rs.integers(0, len(PAUSE_REASONS)))],
                                                                    at=at.strftime("%H:%M"), back=back.strftime("%H:%M"))))
            else:
                kk = (s["centre"], s["date"])
                sp = "SP%02d" % (spare_next.get(kk, 0) % RC.SPARES + 1)
                spare_next[kk] = spare_next.get(kk, 0) + 1
                events.append(dict(t=back, centre_code=code, workstation=sp, event="SESSION_RESUME", booking_ref=b_))
                segs[0][1] = at
                segs.append([back, None, sp])
                end_ws = sp
                wr = typed(ws, rs)
                kw = dict(ws=wr, sp=sp, back=back.strftime("%H:%M"))
                if kind == "periph":
                    kw["part"] = PARTS[int(rs.integers(0, len(PARTS)))]
                if kind == "move":
                    kw["why"] = WHY[int(rs.integers(0, len(WHY)))]
                if kind != "fail" or rs.uniform() < P_REPORTED:
                    reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                        workstation=wr, incident=phrase(s["centre"], kind, rs, **kw)))
                if kind in ("fail", "periph"):
                    truth[b_] = kind
        if b_ in stop_at:
            lost, at = stop_at[b_]
            gap = float(rs.uniform(4, 9))
            back = at + mins(gap)
            downtime = gap
            kk = (s["centre"], s["date"])
            sp = "SP%02d" % (spare_next.get(kk, 0) % RC.SPARES + 1)
            spare_next[kk] = spare_next.get(kk, 0) + 1
            events.append(dict(t=back, centre_code=code, workstation=sp, event="SESSION_RESUME", booking_ref=b_))
            segs[0][1] = at
            segs.append([back, None, sp])
            end_ws = sp
            wr = typed(ws, rs)
            reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                workstation=wr, incident=phrase(s["centre"], "fail", rs, ws=wr, sp=sp,
                                                                back=back.strftime("%H:%M"))))
            truth[b_] = "hang"
        end = st + mins((P.LIMIT / 60 if not r["reach"][-1] else used[i] + float(rs.uniform(0.5, 6))) + downtime)
        events.append(dict(t=end, centre_code=code, workstation=end_ws, event="SESSION_END", booking_ref=b_))
        end_of[b_] = end
        seg[b_] = segs
    # sessions close a few minutes after their last candidate; a finished candidate's client stays on its end screen
    close = {}
    for key, ii in sess_of.items():
        close[key] = max(end_of[sched[i]["booking_ref"]] for i in ii) + mins(rs.uniform(3, 10))
    # the power cut: one report; the log holds nothing at Kochi while the server was down
    pdate = power_key[1]
    reports.append(dict(centre=POWER["centre"], date=pdate, session="AM", time="%02d:%02d" % POWER["cut"], workstation="",
                        incident="Power cut in the examination hall at 11:05. The router and the local server went down at "
                                 "once; the UPS carried the workstations for about four minutes, then they went down too. "
                                 "Mains back at 11:31; candidates resumed on their own workstations as the server came back."))
    cut, back = clock(pdate, POWER["cut"]), clock(pdate, POWER["back"])
    events = [e for e in events if not (e["centre_code"] == P.CENTRE_CODE[POWER["centre"]] and cut <= e["t"] < back)]
    # link losses: each client logged in at the time logs them; a client logging in while the link is down logs only
    # NET_BACK; the link state each client logged is the record the integrity report reads
    offline = {b_ for b_, k in truth.items() if k == "power"}
    for key, kd, t0, t1, spread in plans:
        c = key[0]
        code = P.CENTRE_CODE[c]
        hi_end = close[key]
        for i in sess_of[key]:
            b_ = sched[i]["booking_ref"]
            for a, z, wsx in seg[b_]:
                z = z or hi_end
                if a >= (t1 or hi_end) or z <= t0:
                    continue
                ivs = []
                if a <= t0:
                    L = t0 + dt.timedelta(seconds=float(rs.uniform(0, spread)))
                    if b_ in stop_at and wsx == sched[i]["workstation"]:
                        L = stop_at[b_][0]
                    if L >= z:
                        continue
                    events.append(dict(t=L, centre_code=code, workstation=wsx, event="NET_LOST", booking_ref=b_))
                    if kd == "mid_flap" and L + dt.timedelta(seconds=95) < z:
                        events.append(dict(t=L + dt.timedelta(seconds=40), centre_code=code, workstation=wsx,
                                           event="NET_BACK", booking_ref=b_))
                        events.append(dict(t=L + dt.timedelta(seconds=95), centre_code=code, workstation=wsx,
                                           event="NET_LOST", booking_ref=b_))
                    lo = L
                else:
                    lo = a
                hi = z
                if t1 is not None:
                    Bk = t1 + dt.timedelta(seconds=float(rs.uniform(0, spread)))
                    if Bk < z:
                        events.append(dict(t=Bk, centre_code=code, workstation=wsx, event="NET_BACK", booking_ref=b_))
                        hi = Bk
                ivs.append((lo, hi))
                sec = lambda t: t.replace(microsecond=0)        # the log keeps whole seconds
                st, en = sec(start[i]), sec(end_of[b_])
                for lo_, hi_ in ivs:
                    if max(st, sec(lo_)) < min(en, sec(hi_)):
                        offline.add(b_)
    # routine reboots between sessions
    for w in range(4, 8):
        for d in range(P.WINDOW_DAYS):
            for c in P.CENTRES:
                if rs.uniform() < 0.35:
                    t = clock(RC.window_day(w, d), (13, 50), float(rs.uniform(0, 25)))
                    events.append(dict(t=t, centre_code=P.CENTRE_CODE[c], workstation="WS%02d" % rs.integers(1, RC.WORKSTATIONS[c] + 1),
                                       event="WS_REBOOT", booking_ref=""))
    ev = pd.DataFrame(events).sort_values(["t", "centre_code", "workstation", "event"]).reset_index(drop=True)
    ev.insert(0, "event_utc", [utc(t) for t in ev["t"]])
    ev = ev.drop(columns=["t"])
    rep = pd.DataFrame(reports)
    rep = rep.sort_values(["centre", "date", "session", "time"]).reset_index(drop=True)
    seatdf = pd.DataFrame(seat).sort_values(["session_date", "centre_code", "session", "workstation"]).reset_index(drop=True)
    return dict(events=ev, reports=rep, seat=seatdf, truth=truth, offline=offline, plans=plans)


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
    ss = np.random.SeedSequence(seed + 303)
    ra, rb = [np.random.default_rng(s) for s in ss.spawn(2)]
    return dict(a=ask_a(W, R, ra), panel=ask_b(W, R, rb))
