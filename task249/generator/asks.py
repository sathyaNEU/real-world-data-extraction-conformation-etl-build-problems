"""The asks' records, on rows the call never reads.

Ask A (each form's 2027 sittings a workstation or power failure interrupted): the vendor's session seat plan, its
workstation event log (UTC) and the centres' invigilator incident reports (local time). A failed workstation logs
WS_FAIL with the booking its seat plan holds when the day's log is exported, so a workstation repaired at lunch and
used again in the afternoon carries the afternoon's booking on a morning failure; the candidate resumes on a spare.
On 19 August 2027 a power cut at Kochi outlasted the room's UPS and took the local server down with it: the log has
nothing for half an hour and then each sitting resumes on its own workstation. An invigilator's pause also ends in
SESSION_RESUME on the same workstation, with nothing before it in the log. Network losses log NET_LOST and NET_BACK
on every workstation in the room while the delivery client goes on offline.

Ask B (each content area's 2027 trial items standing accepted at the end of 2027): the item review panel's
decisions as the bank officer logs them, dated when they are entered. The December panel met on 14 December 2027
and its decisions were entered on 4 to 6 January 2028.   A = asks.build(W, R)"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import records as RC

P_FAIL = 0.0070
P_PAUSE = 0.0040
POWER = dict(window=6, centre="Kochi", day=10, session="AM", cut=(11, 5), back=(11, 31))
PAUSE_REASONS = ["candidate unwell", "candidate's ID re-checked at the desk", "code book checked at the desk for added notes",
                 "candidate left for the washroom"]
# each centre's invigilators write their reports in their own way
STYLE = {
    "Chennai": dict(fail="{ws} stopped responding; candidate moved to {sp} and resumed at {back}",
                    late="{ws} stopped responding near the end; sitting closed on the saved responses",
                    pause="{ws}: {reason}, paused from {at} to {back}"),
    "Bengaluru": dict(fail="Workstation {ws} froze. Candidate shifted to spare {sp}, exam resumed {back}.",
                      late="Workstation {ws} froze with a few minutes left. Sitting ended on the saved answers.",
                      pause="Workstation {ws}. {Reason}. Clock stopped {at} to {back}."),
    "Hyderabad": dict(fail="{ws} hung during the exam, candidate moved to {sp}, resumed {back} hrs",
                      late="{ws} hung near completion, sitting closed with responses saved",
                      pause="{ws} {reason}, paused {at} to {back} hrs"),
    "Pune": dict(fail="System {ws} not responding. Candidate continued on {sp} from {back}.",
                 late="System {ws} not responding in the last minutes. Test closed on saved responses.",
                 pause="System {ws}: {reason}. Paused {at}, restarted {back}."),
    "Kochi": dict(fail="{ws} screen frozen, candidate seated at {sp}, test resumed at {back}",
                  late="{ws} screen frozen near the end, sitting closed on saved responses",
                  pause="{ws} {reason}, paused {at} to {back}"),
    "Noida": dict(fail="{ws} crashed. Candidate moved to {sp}, resumed {back}.",
                  late="{ws} crashed just before the end. Sitting closed, responses saved.",
                  pause="{ws}: {reason} ({at} to {back})."),
}


def phrase(centre, kind, **kw):
    if "reason" in kw:
        kw["Reason"] = kw["reason"][0].upper() + kw["reason"][1:]
    return STYLE[centre][kind].format(**kw)


def clock(date, hm, minutes=0.0):
    """local wall time on date at hh:mm plus minutes, as a naive datetime (IST)"""
    return dt.datetime(date.year, date.month, date.day, hm[0], hm[1]) + dt.timedelta(minutes=minutes)


def utc(t):
    return (t - RC.IST).strftime("%Y-%m-%d %H:%M:%S")


def ask_a(W, R, rs):
    rows, sched = W["rows"], R["sched"]
    idx = [i for i, r in enumerate(rows) if r["w"] >= 4]
    seat, events, reports, truth, span = [], [], [], {}, {}
    # who sits at each workstation in each session, for the export-time seat plan
    occ = {}
    for i in idx:
        s = sched[i]
        occ[(s["centre"], s["date"], s["session"], s["workstation"])] = i
    power_key = (POWER["centre"], RC.window_day(POWER["window"], POWER["day"]), POWER["session"])
    spare_free = {}
    for i in idx:
        r, s = rows[i], sched[i]
        code = P.CENTRE_CODE[s["centre"]]
        seat.append(dict(booking_ref=s["booking_ref"], centre_code=code, session_date=s["date"].isoformat(),
                         session=s["session"], workstation=s["workstation"]))
        start = clock(s["date"], RC.SESSION_START[s["session"]], float(rs.uniform(0, 9)))
        used = float(r["ms"].sum()) / 60000.0
        ws = s["workstation"]
        events.append(dict(t=start - dt.timedelta(minutes=float(rs.uniform(8, 13))), centre_code=code, workstation=ws,
                           event="TUTORIAL_START", booking_ref=s["booking_ref"]))
        events.append(dict(t=start, centre_code=code, workstation=ws, event="SESSION_START", booking_ref=s["booking_ref"]))
        downtime = 0.0
        kind = None
        u = rs.uniform()
        if (s["centre"], s["date"], s["session"]) == power_key and start + dt.timedelta(minutes=used) > clock(s["date"], POWER["cut"]):
            kind = "power"
        elif u < P_FAIL:
            kind = "fail"
        elif u < P_FAIL + P_PAUSE:
            kind = "pause"
        end_ws = ws
        if kind == "power":
            cut = clock(s["date"], POWER["cut"])
            back = clock(s["date"], POWER["back"]) + dt.timedelta(minutes=float(rs.uniform(4, 9)))
            downtime = (back - cut).total_seconds() / 60
            events.append(dict(t=back, centre_code=code, workstation=ws, event="SESSION_RESUME", booking_ref=s["booking_ref"]))
            truth[s["booking_ref"]] = "power"
        elif kind == "fail":
            late = rs.uniform() < 0.14 and r["reach"][-1] is not None
            at = start + dt.timedelta(minutes=(float(rs.uniform(max(5.0, used - 4.5), max(6.0, used - 0.5))) if late
                                               else float(rs.uniform(5, max(6.0, used - 3)))))
            later = occ.get((s["centre"], s["date"], "PM", ws)) if s["session"] == "AM" else None
            ref = sched[later]["booking_ref"] if later is not None else s["booking_ref"]
            events.append(dict(t=at, centre_code=code, workstation=ws, event="WS_FAIL", booking_ref=ref))
            truth[s["booking_ref"]] = "fail"
            if late:
                # under five minutes of work left: the invigilator ends the sitting on the saved responses
                end_at = at + dt.timedelta(minutes=float(rs.uniform(2, 6)))
                events.append(dict(t=end_at, centre_code=code, workstation=ws, event="SESSION_END", booking_ref=s["booking_ref"]))
                span[s["booking_ref"]] = (start, end_at)
                if rs.uniform() < 0.7:
                    reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                        workstation=ws, incident=phrase(s["centre"], "late", ws=ws)))
                continue
            key = (s["centre"], s["date"])
            k = spare_free.get(key, 0) % RC.SPARES + 1
            spare_free[key] = spare_free.get(key, 0) + 1
            sp = "SP%02d" % k
            gap = float(rs.uniform(4, 9))
            events.append(dict(t=at + dt.timedelta(minutes=gap), centre_code=code, workstation=sp,
                               event="SESSION_RESUME", booking_ref=s["booking_ref"]))
            downtime = gap
            end_ws = sp
            if rs.uniform() < 0.7:
                reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                    workstation=ws, incident=phrase(s["centre"], "fail", ws=ws, sp=sp,
                                                                    back=(at + dt.timedelta(minutes=gap)).strftime("%H:%M"))))
        elif kind == "pause":
            at = start + dt.timedelta(minutes=float(rs.uniform(10, max(11.0, used - 10))))
            gap = float(rs.uniform(5, 14))
            events.append(dict(t=at + dt.timedelta(minutes=gap), centre_code=code, workstation=ws, event="SESSION_RESUME",
                               booking_ref=s["booking_ref"]))
            downtime = gap
            reports.append(dict(centre=s["centre"], date=s["date"], session=s["session"], time=at.strftime("%H:%M"),
                                workstation=ws, incident=phrase(
                                    s["centre"], "pause", ws=ws, reason=PAUSE_REASONS[int(rs.integers(0, len(PAUSE_REASONS)))],
                                    at=at.strftime("%H:%M"), back=(at + dt.timedelta(minutes=gap)).strftime("%H:%M"))))
        end = start + dt.timedelta(minutes=(P.LIMIT / 60 if not r["reach"][-1] else used + float(rs.uniform(0.5, 6))) + downtime)
        events.append(dict(t=end, centre_code=code, workstation=end_ws, event="SESSION_END", booking_ref=s["booking_ref"]))
        span[s["booking_ref"]] = (start, end)
    # the power cut: one invigilator report; the log holds nothing at Kochi while the server was down
    pdate = power_key[1]
    reports.append(dict(centre=POWER["centre"], date=pdate, session="AM", time="%02d:%02d" % POWER["cut"], workstation="",
                        incident="Power cut in the examination hall at 11:05. The UPS carried the workstations for about "
                                 "four minutes and the local server went down with them. Mains back at 11:31; candidates "
                                 "resumed on their own workstations as the server came back."))
    cut, back = clock(pdate, POWER["cut"]), clock(pdate, POWER["back"])
    events = [e for e in events if not (e["centre_code"] == P.CENTRE_CODE[POWER["centre"]] and cut <= e["t"] < back)]
    # link losses (ask B): every seated workstation in the room logs them, the client carries on offline
    offline = set()
    sess_of = {}
    for i in idx:
        sc = sched[i]
        sess_of.setdefault((sc["centre"], sc["date"], sc["session"]), []).append(i)
    plans = []
    for w in range(4, 8):
        days = [RC.window_day(w, d) for d in range(P.WINDOW_DAYS)]
        kinds = ["mid", "mid_flap", "straddle", "tutorial", "late"]
        for kd in kinds:
            while True:
                c = P.CENTRES[int(rs.integers(0, len(P.CENTRES)))]
                d = days[int(rs.integers(0, len(days)))]
                sess = "AM" if rs.uniform() < 0.5 else "PM"
                if (c, d, sess) != power_key and (c, d, sess) in sess_of and (c, d, sess) not in [p[:3] for p in plans]:
                    break
            plans.append((c, d, sess, kd))
    for c, d, sess, kd in plans:
        base = clock(d, RC.SESSION_START[sess])
        if kd == "tutorial":
            t0, t1 = base - dt.timedelta(minutes=float(rs.uniform(13, 16))), None
            t1 = t0 + dt.timedelta(minutes=float(rs.uniform(2, 3.5)))
        elif kd == "straddle":
            t0 = base - dt.timedelta(minutes=float(rs.uniform(4, 7)))
            t1 = base + dt.timedelta(minutes=float(rs.uniform(6, 12)))
        elif kd == "late":
            t0, t1 = base + dt.timedelta(minutes=float(rs.uniform(222, 232))), None
        else:
            t0 = base + dt.timedelta(minutes=float(rs.uniform(150, 205)))
            t1 = t0 + dt.timedelta(minutes=float(rs.uniform(6, 18)))
        for i in sess_of[(c, d, sess)]:
            sc = sched[i]
            b_ = sc["booking_ref"]
            st, en = span[b_]
            ws = sc["workstation"]
            j0 = t0 + dt.timedelta(seconds=float(rs.uniform(0, 25)))
            events.append(dict(t=j0, centre_code=P.CENTRE_CODE[c], workstation=ws, event="NET_LOST", booking_ref=b_))
            if kd == "mid_flap":
                events.append(dict(t=j0 + dt.timedelta(seconds=40), centre_code=P.CENTRE_CODE[c], workstation=ws,
                                   event="NET_BACK", booking_ref=b_))
                events.append(dict(t=j0 + dt.timedelta(seconds=95), centre_code=P.CENTRE_CODE[c], workstation=ws,
                                   event="NET_LOST", booking_ref=b_))
            hi = en
            if t1 is not None:
                hi = t1 + dt.timedelta(seconds=float(rs.uniform(0, 25)))
                events.append(dict(t=hi, centre_code=P.CENTRE_CODE[c], workstation=ws, event="NET_BACK", booking_ref=b_))
            if max(st, j0) < min(en, hi):
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
