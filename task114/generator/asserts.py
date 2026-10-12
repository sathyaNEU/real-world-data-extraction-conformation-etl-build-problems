"""The assertion regime for task114. Every check reads target/ through golden.py and fails the build loudly."""
import datetime as dt
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

import golden as G

N = 0
LOG = []


def ok(cond, msg):
    global N
    if not cond:
        raise AssertionError(msg)
    N += 1
    LOG.append(msg)


def far(x, ans, floor=0.08):
    return abs(x - ans) / ans >= floor


def run(W, out, T):
    T = Path(T)
    L = G.load(T)
    days = [d.isoformat() for d in L["work"]]
    R = out["main"]["rooms"]
    pk = out["daily_peaks"]

    # ---------------------------------------------------------- the main call is frozen
    m0 = out["main"]
    ok((R, m0["days_short_at"], m0["days_short_one_fewer"]) == (31, 7, 14), "main call frozen: 31 rooms, short 7 and 14")
    ok((m0["meetings_needing_room"], m0["split_meetings"]) == (27607, 9144), "main call frozen: 27,607 and 9,144")
    ok(m0["design_day"] == "2026-05-27", "main call frozen: design day 27 May 2026")
    sig = hashlib.sha256(";".join("%s=%d" % (d, pk[d]) for d in sorted(pk)).encode()).hexdigest()
    ok(sig == "f73b0d608de03e81c33d75fa23d8d1fe354984cff9c659474c319ab0c06ce6bb", "all 246 daily peaks frozen")

    # ---------------------------------------------------------- the committed count and the rule
    ok(R == G.rule_count(pk), "committed count is the rule's count")
    ok(G.days_short(pk, R) <= G.RULE_DAYS < G.days_short(pk, R - 1), "R short on <=12 days, R-1 on more")
    ok(all(G.days_short(pk, r) >= G.days_short(pk, r + 1) for r in range(R - 10, R + 10)), "days short monotone")
    ok(out["main"]["days_short_at"] == G.days_short(pk, R), "days short at R recorded")
    vals = sorted(pk.values(), reverse=True)
    ok(vals[G.RULE_DAYS] == R, "R is the thirteenth-highest daily peak")
    ok(R % 10 != 0, "committed count not on a round ten")
    ok(len(days) == 246, "246 working days in the reference year")

    # ---------------------------------------------------------- the grid of readings around the answer
    cells = {}
    rr = out["rungs"]
    cells["R0 offices sized apart and added"] = rr["R0_offices_added"]
    cells["R1 bookings on one timeline, solo kept"] = rr["R1_bookings_with_solo"]
    cells["R2 bookings on one timeline (natural stop)"] = rr["R2_bookings"]
    cells["R2 with client meetings in meeting rooms kept"] = G.booking_rungs(L, client_out=False)["R2_bookings"]
    m = G.internal_meetings(L)
    booked_somewhere = m[(m.na >= 2) | (m.nf >= 2)]
    cells["R2b paired bookings merged, split meetings not added"] = G.rule_count(
        G.peaks_by_day(zip(booked_somewhere.date, booked_somewhere.s, booked_somewhere.e), days))
    cells["accepted and organiser only"] = G.replay_count(L, response_reading="accepted_only")
    cells["declined invitees counted"] = G.replay_count(L, response_reading="all")
    cells["accepted, tentative and organiser"] = G.replay_count(L, response_reading="accepted_tentative")
    cells["tentative dropped, no response kept"] = G.replay_count(L, response_reading="no_tentative")
    cells["optional invitees ignored"] = G.replay_count(L, types=("required",))
    cells["presence ignored"] = G.replay_count(L, presence="ignore")
    cells["cancelled items kept"] = G.replay_count(L, include_cancelled=True)
    cells["client meetings kept"] = G.replay_count(L, include_client=True)
    cells["closed intervals"] = G.replay_count(L, closed=True)
    cells["one person counts (calls kept)"] = G.replay_count(L, min_n=1)
    # solo booking calls added to the replay
    A = G.typed(L, G.adelaide_holds(L))
    F = G.typed(L, G.front_holds(L))
    solo = pd.concat([A[A.one & A.date.isin(set(days))], F[F.one & F.date.isin(set(days))]])
    need = m[m.n >= 2]
    rows = list(zip(need.date, need.s, need.e)) + list(zip(solo.date, solo.s, solo.e))
    cells["solo bookings added to the replay"] = G.rule_count(G.peaks_by_day(rows, days))
    # bookings plus the split meetings without merging pairs
    split = m[(m.n >= 2) & (m.na < 2) & (m.nf < 2)]
    A, F = A[~G.client_meetings(L, A)], F[~G.client_meetings(L, F)]
    bk = pd.concat([A[(A.rtype == "meeting") & ~A.one & A.date.isin(set(days))],
                    F[(F.rtype == "meeting") & ~F.one & F.date.isin(set(days))]])
    rows = list(zip(bk.date, bk.s, bk.e)) + list(zip(split.date, split.s, split.e))
    cells["bookings plus split meetings, pairs not merged"] = G.rule_count(G.peaks_by_day(rows, days))
    out["grid"] = cells
    # defensible readings a competent analyst could file: at least 8 per cent away
    defensible = ["R0 offices sized apart and added", "R2 bookings on one timeline (natural stop)",
                  "R2 with client meetings in meeting rooms kept",
                  "R2b paired bookings merged, split meetings not added", "accepted and organiser only",
                  "presence ignored", "declined invitees counted", "accepted, tentative and organiser",
                  "tentative dropped, no response kept", "optional invitees ignored"]
    # readings that break a filed rule: a distinct figure, mapped to the sentence they break
    violations = {"R1 bookings on one timeline, solo kept": "brief 3: a call taken by one person goes to the booths",
                  "one person counts (calls kept)": "brief 3: a call taken by one person goes to the booths",
                  "solo bookings added to the replay": "brief 3: a call taken by one person goes to the booths",
                  "client meetings kept": "brief 3: client meetings are held in the client suite, sized separately",
                  "closed intervals": "close-outs method: a room freed at a minute is free for a start at that minute"}
    # texture that must not move the answer, or must clear it
    # (the hybrid needs the decisive class already, so landing on the answer is convergence, not a fork)
    neutral = ["cancelled items kept", "bookings plus split meetings, pairs not merged"]
    for k in defensible:
        ok(far(cells[k], R), "defensible cell '%s' (%d) at least 8 per cent from %d" % (k, cells[k], R))
    for k, rule in violations.items():
        ok(cells[k] != R, "violation cell '%s' (%d) is distinct; breaks %s" % (k, cells[k], rule))
    for k in neutral:
        ok(cells[k] == R or far(cells[k], R), "neutral cell '%s' (%d) converges or clears" % (k, cells[k]))
    ok(set(defensible) | set(violations) | set(neutral) == set(cells), "every grid cell is classified")
    ok(cells["R2 bookings on one timeline (natural stop)"] < R, "the natural stop lies below the answer")
    ok(cells["R2b paired bookings merged, split meetings not added"] <= cells["R2 bookings on one timeline (natural stop)"],
       "the partial insight lands no closer than the natural stop (L3)")
    reasonable = [v for k, v in cells.items() if k not in ("presence ignored", "one person counts (calls kept)",
                                                           "declined invitees counted", "client meetings kept",
                                                           "cancelled items kept", "solo bookings added to the replay",
                                                           "bookings plus split meetings, pairs not merged",
                                                           "closed intervals")]
    ok(max(reasonable) < R, "the answer is the extreme of the reasonable cells (L5)")

    # ---------------------------------------------------------- the empirical pin, both directions
    ev = L["events"]
    ab, fb = L["ab"], L["fb"]
    a_link = set(ab.loc[ab.status.isin(["Confirmed", "Released"]), "outlook_event_id"])
    uid_of = dict(zip(ev.event_id, ev.ical_uid))
    fb_ok = fb[fb.response_status.isin(["Accepted", "Tentative"])]

    def to_local(ts):
        t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        return t.astimezone(G.TOR).strftime("%Y-%m-%d %H:%M")
    f_link = set(zip(fb_ok.ical_uid, fb_ok.start_utc.map(to_local)))
    miss_a = miss_f = 0
    for eid, st, na, nf in zip(m.event_id, m.start_local, m.na, m.nf):
        if na >= 2 and eid not in a_link:
            miss_a += 1
        if nf >= 2 and (uid_of[eid], st) not in f_link:
            miss_f += 1
    ok(miss_a == 0 and miss_f == 0, "every meeting with two or more in an office has a booking there (%d, %d)"
       % (miss_a, miss_f))
    na_of = dict(zip(m.event_id, m.na))
    # a meeting booking is one for an item with two or more people of the firm on it (an outside party on a call's
    # invite is on the line, not in the room)
    conf = ab[(ab.status == "Confirmed") & (ab.outlook_event_id != "") & (~ab.room_code.str.contains(r"\+"))
              & (~ab.booking_ref.str.contains("/")) & (ab.outlook_event_id.map(L["n_int_eid"]).fillna(0) >= 2)]
    conf = conf[conf.outlook_event_id.isin(set(m.event_id))]
    ok(all(na_of[e] >= 2 for e in conf.outlook_event_id), "every confirmed Adelaide meeting booking had two in")
    rel = ab[ab.status == "Released"]
    rel = rel[rel.outlook_event_id.isin(set(m.event_id))]
    ok(len(rel) > 100 and all(na_of[e] < 2 for e in rel.outlook_event_id), "every released booking had fewer than two")
    out["pin"] = dict(meetings=int(len(m)), with_two_in_an_office=int(((m.na >= 2) | (m.nf >= 2)).sum()),
                      released=int(len(rel)))
    # the readings the pin refutes, tested both ways as the answer's reading is: a meeting with two in and no
    # booking there, or a confirmed meeting booking (not a call, not a shadow or combined row) with fewer than two
    conf_ids = set(conf.outlook_event_id)
    fb_m = fb_ok[fb_ok.ical_uid.map(L["n_int_uid"]).fillna(0) >= 2]
    f_conf = set(zip(fb_m.ical_uid, fb_m.start_utc.map(to_local)))
    for name, kw in (("accepted_only", dict(response_reading="accepted_only")),
                     ("accepted_tentative", dict(response_reading="accepted_tentative")),
                     ("no_tentative", dict(response_reading="no_tentative")),
                     ("declined_counted", dict(response_reading="all")),
                     ("required_only", dict(types=("required",)))):
        mr = G.internal_meetings(L, **kw)
        bad = 0
        for eid, st, na, nf in zip(mr.event_id, mr.start_local, mr.na, mr.nf):
            fk = (uid_of[eid], st)
            bad += (na >= 2 and eid not in a_link) + (nf >= 2 and fk not in f_link)
            bad += (eid in conf_ids and na < 2) + (fk in f_conf and nf < 2)
        ok(bad > 500, "the %s reading breaks the booking pattern (%d exceptions)" % (name, bad))
        out["pin"]["exceptions_" + name] = bad
    base_bad = 0
    for eid, st, na, nf in zip(m.event_id, m.start_local, m.na, m.nf):
        fk = (uid_of[eid], st)
        base_bad += (eid in conf_ids and na < 2) + (fk in f_conf and nf < 2)
    ok(base_bad == 0, "no confirmed meeting booking in either office had fewer than two in (%d)" % base_bad)
    # the free training instance: cross-office pairs who shared an office booked a room there
    dr = L["dir"]
    home = dict(zip(dr["UPN"].str.lower(), dr["Home Office"]))
    at = L["att"]
    at = at[at.event_id.isin(set(m.event_id)) & at.attendee_type.isin(["required", "optional"])]
    offices = at.groupby("event_id").attendee_address.agg(lambda s: {home.get(x.lower()) for x in s} - {None})
    cross = set(offices[offices.map(len) == 2].index)
    cr = m[m.event_id.isin(cross)]
    shared = cr[(cr.na >= 2) | (cr.nf >= 2)]
    ok(len(shared) > 200, "cross-office meetings whose people shared an office booked there (%d)" % len(shared))
    out["pin"]["cross_office_booked"] = int(len(shared))

    # ---------------------------------------------------------- the decisive class and its structural blindness
    ok(out["main"]["split_meetings"] > 3000, "the split class is large (%d)" % out["main"]["split_meetings"])
    ok(len(split) == out["main"]["split_meetings"], "split class recomputed")
    # twin days: identical booking peaks per office, one-floor peaks apart
    pa = G.peaks_by_day(zip(A[(A.rtype == "meeting") & ~A.one].date, A[(A.rtype == "meeting") & ~A.one].s,
                            A[(A.rtype == "meeting") & ~A.one].e), days)
    pf = G.peaks_by_day(zip(F[(F.rtype == "meeting") & ~F.one].date, F[(F.rtype == "meeting") & ~F.one].s,
                            F[(F.rtype == "meeting") & ~F.one].e), days)
    pb = G.peaks_by_day(zip(bk.date, bk.s, bk.e), days)
    groups = defaultdict(list)
    for d in days:
        groups[(pa[d], pf[d], pb[d])].append(d)
    twins = [(g, sorted(v, key=lambda d: pk[d])) for g, v in groups.items() if len(v) >= 2]
    best = max(twins, key=lambda gv: pk[gv[1][-1]] - pk[gv[1][0]])
    lo, hi = best[1][0], best[1][-1]
    ok(pk[hi] - pk[lo] >= 5, "twin days %s and %s: same booking peaks, one-floor peaks %d and %d" % (lo, hi, pk[lo], pk[hi]))
    out["twins"] = dict(days=[lo, hi], booking_peaks=list(best[0]), one_floor=[pk[lo], pk[hi]])
    # clean-data test: repair the booking exports into one row per physical hold, ended where the room was given back,
    # with no superseded series rows, and the answer and the natural stop do not move
    L2 = dict(L)
    rep = G.adelaide_holds(L)
    rep = rep.assign(end=[x[:11] + "%02d:%02d" % (e // 60, e % 60) for x, e in zip(rep.end, rep.e)], released_at="",
                     booking_ref=rep.booking_ref.str.replace("/", "-", regex=False))
    L2["ab"] = rep.drop(columns=["date", "s", "e", "office", "solo"])
    keep_rows = G.front_holds(L).index
    L2["fb"] = fb.loc[fb.index.isin(keep_rows) | ~fb.response_status.isin(["Accepted", "Tentative"])]
    main2, _ = G.main_call(L2)
    ok(main2["rooms"] == R, "repairing the booking exports leaves the answer")
    ok(G.booking_rungs(L2) == rr, "repairing the booking exports leaves every booking rung")
    ok(R != rr["R2_bookings"], "answer and natural stop differ")
    # the answer never reads a booking export
    L3 = dict(L)
    L3["ab"] = ab.iloc[0:0]
    L3["fb"] = fb.iloc[0:0]
    ok(G.main_call(L3)[0]["rooms"] == R, "the main call reads no booking export")
    # lens-swap test: the naive and the answer are different populations of meetings
    only_answer = set(split.event_id)
    merged_pairs = m[(m.na >= 2) & (m.nf >= 2)]
    ok(len(only_answer) > 0 and len(merged_pairs) > 0, "answer adds meetings the bookings lack, and folds paired ones")

    # ---------------------------------------------------------- Ask A
    aa = out["askA"]
    co = out["close_outs"]
    QS = ("Q1", "Q2", "Q3", "Q4")
    for o in ("A", "F"):
        for q in QS:
            x = aa[o][q]
            ok(0 < x["solo_hours"] < x["hours"], "solo hours inside the hours %s %s" % (o, q))
    ok(aa["A"]["rooms_30_sep"] != co["A"]["Q4"]["meeting_rooms"] and
       aa["F"]["rooms_30_sep"] != co["F"]["Q4"]["meeting_rooms"], "30 September counts are not the Q4 published counts")

    def figs(ah, fh, current_type=False):
        return {"A": G.office_figures(L, ah, "A", current_type), "F": G.office_figures(L, fh, "F", current_type)}

    def moved(v, base):
        mv = ["%s %s %s" % (o, q, k) for o in ("A", "F") for q in QS for k in ("hours", "solo_hours", "peak")
              if v[o][q][k] != base[o][q][k]]
        return mv + ["%s %s" % (o, k) for o in ("A", "F") for k in ("own_rule", "rooms_30_sep") if v[o][k] != base[o][k]]
    base = figs(G.adelaide_holds(L), G.front_holds(L))
    ok(base == {"A": aa["A"], "F": aa["F"]}, "Ask A recomputes")

    # the legacy reading, the convention set the portal's top responses filed
    LA, LF = G.legacy_adelaide_holds(L), G.legacy_front_holds(L)
    for o, H in (("A", LA), ("F", LF)):
        lco = G.close_out_figures(L, H, o)
        for q in QS:
            for k in ("meeting_rooms", "client_rooms", "peak", "peak_date"):
                ok(lco[q][k] == co[o][q][k], "close-out %s %s %s identical on the legacy reading" % (o, q, k))
    leg = {"A": G.office_figures(L, LA, "A", client_out=False), "F": G.office_figures(L, LF, "F", client_out=False)}
    out["askA_legacy"] = leg
    for o in ("A", "F"):
        ok(leg[o]["own_rule"] != base[o]["own_rule"], "legacy room count misses at %s (%d against %d)"
           % (o, leg[o]["own_rule"], base[o]["own_rule"]))
    for o in ("A", "F"):
        for q in QS:
            ok(leg[o][q]["hours"] != base[o][q]["hours"], "legacy hours miss %s %s" % (o, q))
            ok(leg[o][q]["solo_hours"] != base[o][q]["solo_hours"], "legacy call hours miss %s %s" % (o, q))
    peaks_missed = [(o, q) for o in ("A", "F") for q in QS if leg[o][q]["peak"] != base[o][q]["peak"]]
    ok(len(peaks_missed) >= 6, "legacy busiest moment misses in %d office-quarters" % len(peaks_missed))
    out["askA_legacy_peaks_missed"] = ["%s %s" % x for x in peaks_missed]
    for o in ("A", "F"):
        for q in QS:
            for k in ("hours", "solo_hours"):
                d = abs(leg[o][q][k] - base[o][q][k])
                ok(d >= 20, "legacy %s %s %s sits %.2f hours from the answer" % (o, q, k, d))

    # each device on its own: the correct reading with exactly one mishandling
    var = {
        "A1 release keyed on status (give-backs held to the end)": figs(G.adelaide_holds(L, released="status"),
                                                                        G.front_holds(L)),
        "A2 combined rows dropped (half rows kept)": figs(G.adelaide_holds(L, shadows="drop_combined"), G.front_holds(L)),
        "combined room as one room": figs(G.adelaide_holds(L, shadows="combined_as_one"), G.front_holds(L)),
        "every Adelaide row a room": figs(G.adelaide_holds(L, shadows="all"), G.front_holds(L)),
        "F1 cancelled rows filtered before the fold": figs(G.adelaide_holds(L), G.front_holds(L, fold="status_first")),
        "F2 the fold keyed on the room": figs(G.adelaide_holds(L), G.front_holds(L, fold="room_key")),
        "series rows kept (no fold)": figs(G.adelaide_holds(L), G.front_holds(L, fold="keep")),
        "released held to the end": figs(G.adelaide_holds(L, released="full"), G.front_holds(L)),
        "released dropped": figs(G.adelaide_holds(L, released="drop"), G.front_holds(L)),
        "declined rows kept": figs(G.adelaide_holds(L), G.front_holds(L, keep_declined=True)),
        "tentative rows dropped": figs(G.adelaide_holds(L), G.front_holds(L, tentative=False)),
        "cancelled kept": figs(G.adelaide_holds(L, keep_cancelled=True), G.front_holds(L, keep_cancelled=True)),
        "room type as on 30 September all year": figs(G.adelaide_holds(L), G.front_holds(L), current_type=True),
        "solo read as one recipient": figs(G.adelaide_holds(L), G.front_holds(L, solo_reading="one")),
        "solo read from the app and kiosk only": figs(G.adelaide_holds(L, solo_reading="source"), G.front_holds(L)),
        "S1 focus blocks read as calls": figs(G.adelaide_holds(L, focus_as_call=True), G.front_holds(L, focus_as_call=True)),
        "G1 people read from the headcount (an outside party on the line counted)":
            figs(G.adelaide_holds(L, solo_reading="headcount"), G.front_holds(L, solo_reading="room_included")),
        "C1 client meetings in meeting rooms counted toward the room count":
            {"A": G.office_figures(L, G.adelaide_holds(L), "A", client_out=False),
             "F": G.office_figures(L, G.front_holds(L), "F", client_out=False)},
    }
    out["askA_variants"] = {}
    for name, v in var.items():
        mv = moved(v, base)
        out["askA_variants"][name] = mv
        ok(len(mv) >= 2, "device '%s' moves Ask A figures (%d)" % (name, len(mv)))
    ok(out["askA_variants"]["C1 client meetings in meeting rooms counted toward the room count"] == ["A own_rule", "F own_rule"],
       "the client meetings move both room counts and nothing else")
    ok(out["askA_variants"]["S1 focus blocks read as calls"] == ["%s %s solo_hours" % (o, q) for o in ("A", "F") for q in QS],
       "the focus blocks move every call-hours figure and nothing else")
    g1name = "G1 people read from the headcount (an outside party on the line counted)"
    ok(sorted(out["askA_variants"][g1name]) == sorted(["%s %s solo_hours" % (o, q) for o in ("A", "F") for q in QS]
                                                     + ["A own_rule", "F own_rule"]),
       "the calls with an outside party move both room counts and every call-hours figure, and nothing else")
    for o in ("A", "F"):
        ok(var[g1name][o]["own_rule"] == base[o]["own_rule"] + 1,
           "%s room count with people read from the headcount stands one above (%d against %d)"
           % (o, var[g1name][o]["own_rule"], base[o]["own_rule"]))
    # every new device misses each hours figure it moves by fifteen hours or more, so no lenient band can pass it
    floors = {}
    for name in ("A1 release keyed on status (give-backs held to the end)", "A2 combined rows dropped (half rows kept)",
                 "F1 cancelled rows filtered before the fold", "F2 the fold keyed on the room", "S1 focus blocks read as calls",
                 g1name):
        v = var[name]
        ds = [abs(v[o][q][k] - base[o][q][k]) for o in ("A", "F") for q in QS for k in ("hours", "solo_hours")
              if v[o][q][k] != base[o][q][k]]
        floors[name] = round(min(ds), 2)
        ok(min(ds) >= 15, "%s misses each hours figure it moves by 15 hours or more (least %.2f)" % (name, min(ds)))
    out["askA_device_floors"] = floors
    for name in ("A1 release keyed on status (give-backs held to the end)", "F1 cancelled rows filtered before the fold"):
        mv = out["askA_variants"][name]
        o = name[0]
        ok(all("%s %s %s" % (o, q, k) in mv for q in QS for k in ("hours", "solo_hours")),
           "%s moves every quarter's hours and call hours" % name)
    utc_read = figs(G.adelaide_holds(L), G.front_holds(L, local=False))
    out["askA_utc_hazard_moves"] = len(moved(utc_read, base))

    # the pair simulation: which criteria a strong solver running the habitual battery files right, weighted as the
    # generated rubric grades them (one criterion per office and measure, the four quarters together)
    import pairsim
    pr = pairsim.profiles(L)
    ok(pr["everything handled"] == base and pr["legacy (the portal's first conventions)"] == leg, "pair profiles anchor")
    TOT = pairsim.TOTAL
    out["pairsim"] = {k: {"points": pairsim.points(v, base), "passed": pairsim.passed(v, base)} for k, v in pr.items()}
    pts = {k: v["points"] for k, v in out["pairsim"].items()}
    ok(pts["everything handled"] == TOT, "the golden takes all %d ask points" % TOT)
    ok(pts["legacy (the portal's first conventions)"] <= 8, "the legacy reading keeps %d of %d ask points"
       % (pts["legacy (the portal's first conventions)"], TOT))
    for k in ("legacy, give-backs read", "legacy, combined bookings expanded", "legacy, fold over every status",
              "legacy, fold across rooms", "legacy, client meetings out of the room count"):
        ok(pts[k] <= TOT // 2, "a solver handling one family keeps %d of %d (%s)" % (pts[k], TOT, k))
    one_office = sum(pairsim.WEIGHTS.values()) + pairsim.WEIGHTS["rooms_30_sep"]
    for k in ("every Adelaide device handled", "every Front Street device handled"):
        ok(pts[k] <= one_office, "a solver handling one office's devices keeps that office and the other's rooms, %d "
                                 "of %d (%s)" % (pts[k], TOT, k))
    g1_loss = 2 * (pairsim.WEIGHTS["own_rule"] + pairsim.WEIGHTS["solo_hours"])
    for k in ("everything handled but the calls with an outside party",
              "everything handled, calls told by a subject that is Call",
              "everything handled, calls told by a subject that says call"):
        ok(pts[k] == TOT - g1_loss, "%s keeps %d of %d (loses both room counts and both call hours)" % (k, pts[k], TOT))
    for k, cap in (("every representation device handled, focus blocks read as calls, client meetings kept",
                    TOT - g1_loss), ("everything handled but the focus blocks", TOT - 2 * pairsim.WEIGHTS["solo_hours"]),
                   ("everything handled but the client meetings", TOT - 2 * pairsim.WEIGHTS["own_rule"]),
                   ("portal run 3 (Adelaide right, Front Street fold keyed on the room, people from the headcount)",
                    TOT // 2)):
        ok(pts[k] <= cap, "%s keeps %d of %d (cap %d)" % (k, pts[k], TOT, cap))

    # S1: calls and focus blocks are told apart on the calendar, and the rule (a one-person booking is a call unless
    # its calendar item is a focus block; an Adelaide app or kiosk booking has no item) covers every one-person row
    evs = L["events"]
    ok(set(evs[evs.subject == "Focus time"].is_online_meeting) == {False}, "every focus block is offline")
    ok(set(evs[evs.subject.isin(["Call", "Canceled: Call"])].is_online_meeting) == {True}, "every call is online")
    # an item with one person of the firm on it (not all-day, not a client meeting) is a call, online, or a focus block
    one_items = evs[evs.event_id.map(L["n_int_eid"]).eq(1) & ~evs.is_all_day & ~evs.event_id.isin(L["client_eid"])]
    calls1 = one_items[one_items.subject != "Focus time"]
    ok(set(calls1.is_online_meeting) == {True} and set(calls1.categories) == {""},
       "every item with one person of the firm on it is a focus block or an online call (%d calls)" % len(calls1))
    call_e, call_u = set(calls1.event_id), set(calls1.ical_uid)
    a1 = ab[(ab.headcount == "1") & (ab.status != "Cancelled")]
    f1 = fb[(fb.attendee_count == "2") & fb.response_status.isin(["Accepted", "Tentative"])]
    A1h, F1h = G.adelaide_holds(L), G.front_holds(L)
    stray_a = A1h[A1h.one & ~(A1h.outlook_event_id.isin(call_e | L["focus_eid"]) | (A1h.outlook_event_id == ""))]
    stray_f = F1h[F1h.one & ~F1h.ical_uid.isin(call_u | L["focus_uid"])]
    ok(len(stray_a) == 0 and len(stray_f) == 0, "every one-person booking is a call or a focus block (%d, %d)"
       % (len(stray_a), len(stray_f)))
    nolink = ab[(ab.outlook_event_id == "") & (ab.status != "Cancelled")]
    ok(set(nolink.source) <= {"Mobile app", "Kiosk"} and set(nolink.headcount) == {"1"},
       "every Adelaide booking with no calendar item is an app or kiosk booking for one (%d)" % len(nolink))
    ok(a1.outlook_event_id.isin(L["focus_eid"]).sum() > 100 and f1.ical_uid.isin(L["focus_uid"]).sum() > 100,
       "focus blocks held in meeting rooms at both offices")
    # the room count does not move when the focus blocks are counted in it
    for o, H in (("A", G.adelaide_holds(L)), ("F", G.front_holds(L))):
        Hf = H.assign(one=H.solo)
        ok(G.office_figures(L, Hf, o)["own_rule"] == base[o]["own_rule"],
           "%s room count is the same with the focus blocks counted in it" % o)

    # separation: no device row enters the main call's meeting population
    ev = L["events"]
    cat = dict(zip(ev.event_id, ev.categories))
    canc = dict(zip(ev.event_id, ev.is_cancelled))
    n_int = m.set_index("event_id").n
    touched = [W.event_id[("sc", c["sid"], c["day"])] for c in W.standing_cancelled]
    ok(all(canc[e] for e in touched), "every cancelled standing call is cancelled in the calendar (%d)" % len(touched))
    moved_calls = [W.event_id[("s", b["meeting"])] for b in W.bookings if b.get("moved_from")]
    ok(all(n_int.get(e, 0) < 2 for e in moved_calls), "moved standing calls carry one person (%d)" % len(moved_calls))
    clients = sorted({b["meeting"] for b in W.bookings if b["kind"] == "client"})
    inmr = [b for b in W.bookings if b.get("in_meeting_room")]
    ok(len(inmr) > 40 and all(G.room_type_on(L["reg"], b["room"], b["day"]) == "meeting" for b in inmr),
       "client meetings held in a meeting room (%d)" % len(inmr))
    ok(all(cat[W.event_id[("c", k)]] == "Client meeting" for k in clients), "client meetings sit in the client category")
    out["device_log"] = W.device_log

    # ---------------------------------------------------------- G1: calls with an outside party on the line
    att = L["att"]
    outside = att[~att.attendee_address.str.lower().str.endswith("@harrowfield.ca")]
    guests_on = outside.groupby("event_id").size().to_dict()
    g = evs[evs.event_id.isin(set(guests_on)) & ~evs.event_id.isin(L["client_eid"])]
    ok(set(g.event_id.map(L["n_int_eid"])) == {1}, "every item with a guest that is no client meeting has one person "
                                                   "of the firm on it (%d)" % len(g))
    ok(set(g.is_online_meeting) == {True} and set(g.categories) == {""} and set(g.event_type) == {"singleInstance"}
       and not g.is_cancelled.any() and not g.is_all_day.any() and not g.subject.isin(["Call", "Focus time"]).any(),
       "every call with an outside party is one online item, uncategorised, named for the call")
    g_e, g_u = set(g.event_id), set(g.ical_uid)
    eid_of_uid = dict(zip(g.ical_uid, g.event_id))
    ga = ab[ab.outlook_event_id.isin(g_e) & (ab.status != "Cancelled")]
    gf = fb[fb.ical_uid.isin(g_u) & fb.response_status.isin(["Accepted", "Tentative"])]
    ok(len(ga) > 150 and len(gf) > 150, "calls with an outside party booked at both offices (%d, %d)" % (len(ga), len(gf)))
    ok(set(ga.source) == {"Outlook"} and all(int(h) == 1 + guests_on[e] for h, e in zip(ga.headcount, ga.outlook_event_id)),
       "Adelaide's headcount counts the people on the line")
    ok(all(int(c) == 2 + guests_on[eid_of_uid[u]] for c, u in zip(gf.attendee_count, gf.ical_uid)),
       "Front Street's attendee_count counts the outside party and the room")
    ok(set(m[m.event_id.isin(g_e)].n) <= {1}, "no call with an outside party needs a room in the replay (main call "
                                              "population untouched)")
    hc2 = (ab.headcount == "2") & (ab.status == "Confirmed")
    ac3 = (fb.attendee_count == "3") & fb.response_status.isin(["Accepted", "Tentative"])
    thr = [W.event_id[("s", b["meeting"])] for b in W.bookings if b.get("g1_threshold")]
    subj_of = dict(zip(evs.event_id, evs.subject))
    dl = W.device_log
    ok(len(thr) == dl.get("G1 calls with an outside party at the room-count threshold", 0)
       + dl.get("G1 calls with an outside party booked at the room-count threshold", 0) and len(thr) >= 13,
       "calls with an outside party at the room-count threshold: %d, the log's two counts" % len(thr))
    ok(not any("call" in subj_of[e].lower() for e in thr),
       "no call with an outside party at the room-count threshold is named a call (%d)" % len(thr))
    # the calls booked into a free room for the threshold: which office, and what they move (nothing but hours)
    booked = [b for b in W.bookings if b.get("g1_booked")]
    bk_e = {W.event_id[("s", b["meeting"])] for b in booked}
    bk_u = set(evs[evs.event_id.isin(bk_e)].ical_uid)
    booked_by_office = {nm: sum(1 for b in booked if b["office"] == o)
                        for o, nm in ((1, "Adelaide Street"), (2, "Front Street"))}
    A0 = G.adelaide_holds(L)
    A0 = A0[~A0.outlook_event_id.isin(bk_e)]
    F0 = G.front_holds(L)
    F0 = F0[~F0.ical_uid.isin(bk_u)]
    wo = {"A": G.office_figures(L, A0, "A"), "F": G.office_figures(L, F0, "F")}
    ok(all(wo[o][q]["peak"] == base[o][q]["peak"] for o in ("A", "F") for q in QS)
       and all(wo[o][k] == base[o][k] for o in ("A", "F") for k in ("own_rule", "rooms_30_sep")),
       "the calls booked at the threshold move no busiest moment and neither room count")
    co0 = {"A": G.close_out_figures(L, A0, "A"), "F": G.close_out_figures(L, F0, "F")}
    ok(all(co0[o][q][k] == co[o][q][k] for o in ("A", "F") for q in QS for k in ("peak", "peak_date")),
       "the calls booked at the threshold move no close-out busiest moment")
    out["guest_calls"] = dict(items=int(len(g)), adelaide=int(len(ga)), front=int(len(gf)), at_threshold=len(thr),
                              booked_at_threshold=booked_by_office,
                              named_a_call=int(g.subject.str.contains("call", case=False).sum()),
                              adelaide_share_of_headcount_2=round(len(ga[ga.headcount == "2"]) / int(hc2.sum()), 3),
                              front_share_of_attendee_count_3=round(len(gf[gf.attendee_count == "3"]) / int(ac3.sum()), 3))
    ok(out["guest_calls"]["adelaide_share_of_headcount_2"] < 0.05 and out["guest_calls"]["front_share_of_attendee_count_3"]
       < 0.08, "the calls are a small share of the bookings that read as two people (%s)" % out["guest_calls"])
    # the booking rung a headcount reader files is the stump's
    Ab = G.typed(L, G.adelaide_holds(L, solo_reading="headcount"))
    Fb = G.typed(L, G.front_holds(L, solo_reading="room_included"))
    Ab = Ab[Ab.date.isin(set(days)) & ~G.client_meetings(L, Ab) & (Ab.rtype == "meeting") & ~Ab.one]
    Fb = Fb[Fb.date.isin(set(days)) & ~G.client_meetings(L, Fb) & (Fb.rtype == "meeting") & ~Fb.one]
    bh = pd.concat([Ab, Fb])
    r2h = G.rule_count(G.peaks_by_day(zip(bh.date, bh.s, bh.e), days))
    ok(r2h == rr["R2_bookings"], "the booking rung is %d with people read from the headcount too (%d)"
       % (rr["R2_bookings"], r2h))
    # no reading of the two offices' own counts adds up to the new office's count
    own_reads = {}
    for o, Hc, Hh, Hl in (("A", G.adelaide_holds(L), G.adelaide_holds(L, solo_reading="headcount"), LA),
                          ("F", G.front_holds(L), G.front_holds(L, solo_reading="room_included"), LF)):
        own_reads[o] = sorted({G.office_figures(L, H, o, client_out=c)["own_rule"]
                               for H in (Hc, Hh) for c in (True, False)}
                              | {G.office_figures(L, Hl, o, client_out=False)["own_rule"]})
    sums = sorted({a + f for a in own_reads["A"] for f in own_reads["F"]})
    out["own_count_readings"] = dict(A=own_reads["A"], F=own_reads["F"], sums=sums)
    ok(R not in sums, "no reading of the two offices' own counts adds up to %d (%s)" % (R, sums))
    # no other mishandling cancels the headcount read back onto either room count (direction discipline)
    import itertools
    hazards = {"A": {"A1 release keyed on status": dict(released="status"),
                     "A2 combined rows dropped": dict(shadows="drop_combined"), "C1 client meetings kept": None},
               "F": {"F1 cancelled rows first": dict(fold="status_first"), "F2 fold keyed on the room": dict(fold="room_key"),
                     "tentative rows dropped": dict(tentative=False), "C1 client meetings kept": None}}
    cancels = []
    for o, hz in hazards.items():
        for r in range(len(hz) + 1):
            for sub in itertools.combinations(sorted(hz), r):
                kw = {"solo_reading": "headcount" if o == "A" else "room_included"}
                for h in sub:
                    if hz[h]:
                        kw.update(hz[h])
                if o == "F" and "F1 cancelled rows first" in sub and "F2 fold keyed on the room" in sub:
                    kw["fold"] = "legacy"
                H = G.adelaide_holds(L, **kw) if o == "A" else G.front_holds(L, **kw)
                got = G.office_figures(L, H, o, client_out="C1 client meetings kept" not in sub)["own_rule"]
                if got == base[o]["own_rule"]:
                    cancels.append((o, sub))
    ok(not cancels, "with people read from the headcount, no other mishandling lands either room count on the answer "
                    "(%s)" % cancels)
    # a partial catch by the subject misses the same figures, each call-hours figure by 15 hours or more
    for pat in (r"^Call$", "call"):
        v = {"A": G.office_figures(L, pairsim.by_subject(L, G.adelaide_holds(L, solo_reading="headcount"), "A", pat), "A"),
             "F": G.office_figures(L, pairsim.by_subject(L, G.front_holds(L, solo_reading="room_included"), "F", pat),
                                   "F")}
        ok(sorted(moved(v, base)) == sorted(out["askA_variants"][g1name]),
           "calls told by a subject matching %r miss the same figures" % pat)
        d = min(abs(v[o][q]["solo_hours"] - base[o][q]["solo_hours"]) for o in ("A", "F") for q in QS)
        ok(d >= 15, "calls told by a subject matching %r miss each call-hours figure by 15 hours or more (least %.2f)"
           % (pat, d))

    # ---------------------------------------------------------- device silence and placement
    exc = fb[fb.is_exception == "True"]
    took = set(zip(exc.ical_uid, exc.original_start_utc))
    took_room = set(zip(exc.ical_uid, exc.original_start_utc, exc.room_mailbox))
    acc = fb[fb.response_status.isin(["Accepted", "Tentative"]) & (fb.is_exception == "False")]
    ghosts = acc[[k in took for k in zip(acc.ical_uid, acc.start_utc)]]
    same = ghosts[[k in took_room for k in zip(ghosts.ical_uid, ghosts.start_utc, ghosts.room_mailbox)]]
    ok(len(ghosts) > 300 and len(ghosts) > len(same) > 40, "series rows a later exception took (%d, %d in the same room)"
       % (len(ghosts), len(same)))
    out["series_rows_superseded"] = dict(all=int(len(ghosts)), same_room=int(len(same)))
    fl = G.front_holds(L, fold="keep")
    clash = 0
    for (mb, d), g in fl.groupby(["room_mailbox", "date"]):
        iv = sorted(zip(g.s, g.e))
        clash += sum(1 for (a, b), (c, e) in zip(iv, iv[1:]) if c < b)
    ok(clash == 0, "no Front Street room is double-held, ghosts included")
    sh = ab[ab.booking_ref.str.contains("/")]
    ok(len(sh) >= 40 and len(sh) % 2 == 0, "shadow holds in pairs (%d)" % len(sh))
    rl = ab[ab.status == "Released"]
    ok(all(G.mins(r) - G.mins(s) == 15 for r, s in zip(rl.released_at, rl.start)), "released at fifteen minutes")
    gb = ab[(ab.status == "Confirmed") & (ab.released_at != "")]
    ok(len(gb) > 200 and all(G.mins(c) < G.mins(r) < G.mins(e) for c, r, e in zip(gb.checked_in_at, gb.released_at, gb.end)),
       "given back after check-in and before the end (%d)" % len(gb))
    comb = ab[ab.room_code.str.contains(r"\+") & (ab.status != "Cancelled")]
    with_half = set(sh.booking_ref.str.split("/").str[0])
    ok(all((ref in with_half) == (d < "2026-05-19") for ref, d in zip(comb.booking_ref, comb.start)),
       "half rows written before the platform upgrade and not after (%d combined)" % len(comb))
    ok(int((ab.headcount == "0").sum()) == int((ab.room_code == "AD-1.00").sum()), "headcount zero only on the Commons")

    # ---------------------------------------------------------- the people and their beliefs
    pres = L["pres"]
    ok(all(len(v) == 1 for v in pres.values()), "nobody is in both offices on one day")
    dr2 = dr.copy()
    end = dict(zip(dr2["Employee No"], dr2["End Date"]))
    late = sum(1 for (e, d) in pres if isinstance(end.get(e), str) and end[e] and d > end[e][:10])
    ok(late == 0, "no badge after a leaver's end date")
    for nm in ("Hernandez, Claudia", "Thompson, Louis", "Jimenez, Debbie", "Walker, Caleb", "Morgan, Kristie"):
        ok((dr["Display Name"] == nm).sum() == 1, "%s is on the directory once" % nm)
    # mid-morning, more rooms empty than full, at both offices
    for o, H in (("A", A), ("F", F)):
        h = H[(H.rtype == "meeting") & H.date.isin(set(days))]
        occ = []
        for d in days:
            g = h[h.date == d]
            occ.append(((g.s <= 11 * 60) & (g.e > 11 * 60)).sum())
        rooms = 30 if o == "A" else 29
        ok(sum(occ) / len(occ) < rooms / 2, "%s: rooms in use at 11:00 average under half" % o)
    fpk = pd.Series({d: v for d, v in pf.items()})
    wdmean = fpk.groupby(pd.to_datetime(fpk.index).dayofweek).mean()
    ok(wdmean.idxmax() in (1, 2), "Front Street busiest on Tuesday or Wednesday")
    forum = fb[fb.room_mailbox.str.startswith("fr.forum")]
    halls = ev[ev.categories == "Town hall"]
    ok(len(forum) == len(halls) and set(forum.ical_uid) == set(halls.ical_uid), "the Forum is booked only for the town halls")

    # ---------------------------------------------------------- input gates and hygiene
    files = sorted(p for p in T.iterdir() if p.is_file())
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    fmts = {p.suffix for p in files}
    ok(len(fmts) >= 3, "three or more formats (%s)" % sorted(fmts))
    ok(len(L["att"]) >= 25000, "a file of 25,000 rows or more (%d)" % len(L["att"]))
    for p in files:
        if p.suffix in (".md", ".csv", ".eml"):
            ok("—" not in p.read_text(encoding="utf-8"), "no em dash in %s" % p.name)
    return N
