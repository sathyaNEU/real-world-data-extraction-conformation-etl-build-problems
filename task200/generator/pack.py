"""Write the airport's own exports into target/ from the clean truth, each in the form its system writes it."""
import datetime as dt
import io
import os

import numpy as np
import pandas as pd

import params as P
import world as Wm

LONDON = Wm.LONDON

F = {
    "ct24": "screening_tip/ct_tip_events_2024.csv",
    "ct25": "screening_tip/ct_tip_events_2025.csv",
    "ct26": "screening_tip/ct_tip_events_2026.csv",
    "pb": "screening_tip/pierb_tip_log_2023-09_2026-12.csv",
    "roster": "staff/screening_roster_2026-12-31.xlsx",
    "ctpos": "positions/ct_workstation_sessions_2026.csv",
    "pbev": "positions/pierb_screen_events_2026.csv",
    "rej": "search/ct_tray_rejects_2026.csv",
    "search": "search/search_log_2026.csv",
    "lms": "training/lms_assessment_export_2027-01-11.xlsx",
    "certs": "training/assessment_centre_certificates.csv",
    "badges": "staff/id_centre_badge_register.csv",
    "sps": "docs/SPS-04_screener_performance_standard_issue3.docx",
    "eml": "docs/re_remedial_course_2027.eml",
    "thru": "ops/lane_throughput_daily_2026.csv",
    "queue": "ops/queue_time_samples_2026.csv",
    "review": "docs/security_compliance_review_2026.pdf",
}
DISTRACTORS = ["thru", "queue", "review"]


def _rng(tag):
    return np.random.default_rng([P.SEED, 7, sum(ord(c) * (i + 3) for i, c in enumerate(tag))])


def _write_csv(target, key, df, preamble=None):
    p = os.path.join(target, F[key])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    buf = io.StringIO()
    if preamble:
        for line in preamble:
            buf.write(line + "\r\n")
    df.to_csv(buf, index=False, lineterminator="\r\n")
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def _utc(s):
    return s.dt.tz_convert("UTC").dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _local(s, fmt):
    return s.dt.tz_convert(LONDON).dt.strftime(fmt)


# ----------------------------------------------------------------------------------------------- TIP exports
def tip_exports(target, W):
    pp, tp = W["people"], W["tip"]
    r = _rng("tipexp")
    login = pp.login.values
    badge = pp.badge.values
    ct = tp[tp.area == "C"].copy()
    ct["workstation"] = ct.screen
    ct["operator_login"] = login[ct.pid.values]
    ct["result"] = np.where(ct.cancelled, "CANCELLED", np.where(ct.hit, "HIT", "MISS"))
    ct["threat_class"] = ct.category.str.upper().replace({"OTHER": "OTHER"})
    ct["response_s"] = [("%.3f" % v) if h else "" for v, h in zip(ct.rt.values, ct.hit.values)]
    ct = ct.sort_values(["ts", "workstation"]).reset_index(drop=True)
    gaps = r.integers(1, 9, len(ct))
    ct["event_id"] = ["TIP%09d" % v for v in (410000123 + np.cumsum(gaps))]
    ct["projection_utc"] = _utc(ct.ts)
    ct["year"] = ct.ts.dt.year
    cols = ["event_id", "projection_utc", "lane", "workstation", "operator_login", "tip_image", "threat_class", "result",
            "response_s"]
    ct["tip_image"] = ct.image
    for y, key in ((2024, "ct24"), (2025, "ct25"), (2026, "ct26")):
        d = ct[ct.year == y][cols]
        if y >= 2025:
            # the annual file is built from monthly pulls, each run at 06:00 UTC on the first of the next month and
            # taking everything since the last pull began, so the first hours of each month's first day repeat
            first = d[(d.projection_utc.str[8:10] == "01") & (d.projection_utc.str[11:13] < "06")]
            first = first[first.projection_utc.str[5:7] != "01"]
            d = pd.concat([d, first]).sort_values(["projection_utc", "event_id"], kind="mergesort")
        _write_csv(target, key, d)
    pb = tp[tp.area == "B"].copy().sort_values(["ts", "screen"]).reset_index(drop=True)
    loc = pb.ts.dt.tz_convert(LONDON)
    out = pd.DataFrame({
        "Date": loc.dt.strftime("%d/%m/%Y"), "Time": loc.dt.strftime("%H:%M:%S"), "Screen": pb.screen,
        "Operator": ["%03d" % v for v in pp.op_no.values[pb.pid.values]], "Image": pb.image,
        "Class": pb.category.map({"IED": "A", "Firearm": "B", "Knife": "C", "Other": "D"}),
        "Result": np.where(pb.cancelled, "X", np.where(pb.hit, "H", "M")),
        "RT": [("%.1f" % v) if h else "" for v, h in zip(pb.rt.values, pb.hit.values)]})
    pre = ["TIP EVENT LOG  PIER B SEARCH  SCREENS PB1-PB3",
           "Library PIERB-L3  Class A IED  B FIREARM  C BLADE  D OTHER  Result H HIT  M MISS  X CANCELLED",
           "Exported 15/01/2027 08:12 by tipadmin"]
    _write_csv(target, "pb", out, preamble=pre)
    return ct


# ----------------------------------------------------------------------------------------------- roster
def roster_frames(W):
    pp = W["people"]
    cur = pp[pp.left.isna()].copy()
    r = _rng("roster")
    role = np.where(cur.supervisor, "Screening Supervisor", "Security Officer (Screener)")
    ros = pd.DataFrame({
        "Staff no": cur.staff_no.values, "Team": cur.team_end.values, "Role": role,
        "CT login": cur.login.values, "Pier B TIP operator": ["%03d" % v for v in cur.op_no.values],
        "ID badge": cur.badge.values, "Contract": cur.contract.values,
        "Start date": pd.to_datetime(cur.start.values)})
    ros = ros.sample(frac=1.0, random_state=int(r.integers(1, 10**6))).sort_values(["Team", "Staff no"], kind="mergesort")
    mv = pp[pp.move_date.notna()]
    moves = pd.DataFrame({"Staff no": mv.staff_no.values, "From team": mv.team_before.values,
                          "To team": mv.team_end.values, "Effective": pd.to_datetime(mv.move_date.values)})
    return ros.reset_index(drop=True), moves.sort_values("Effective", kind="mergesort").reset_index(drop=True)


# ----------------------------------------------------------------------------------------------- positions
def positions(target, W):
    pp, ss, rj = W["people"], W["sessions"], W["rejects"]
    r = _rng("positions")
    s26 = ss[pd.to_datetime(ss.day).dt.year == 2026].copy()
    # Central: one row per lane the workstation's queue served; a two-lane queue picks its second lane up part way
    c = s26[s26.area == "C"].copy().reset_index(drop=True)
    rows = []
    for row in c.itertuples():
        rows.append((row.screen, row.lane1, pp.login.values[row.pid], row.start, row.end))
        if row.mux:
            rows.append((row.screen, row.lane2, pp.login.values[row.pid], row.mux_on, row.mux_off))
    pos = pd.DataFrame(rows, columns=["workstation", "lane", "login", "on", "off"]).sort_values(
        ["on", "workstation", "lane"], kind="mergesort").reset_index(drop=True)
    pos["session_ref"] = ["WS%s-%07d" % (w[2:], v) for w, v in
                          zip(pos.workstation, 3100000 + np.cumsum(r.integers(1, 5, len(pos))))]
    out = pd.DataFrame({"session_ref": pos.session_ref, "workstation": pos.workstation, "lane": pos.lane,
                        "login": pos.login, "logon_utc": _utc(pos.on), "logoff_utc": _utc(pos.off)})
    _write_csv(target, "ctpos", out)
    # Pier B: the legacy screens write events; one operator at a time, and a log-on ends whoever was logged on
    b = s26[s26.area == "B"].copy().sort_values(["screen", "start"]).reset_index(drop=True)
    ev = []
    truth = []
    by_pid = {}
    for row in b.itertuples():
        by_pid.setdefault(row.pid, []).append(row.start)
    for p in by_pid:
        by_pid[p] = sorted(by_pid[p])
    for scr, g in b.groupby("screen", sort=True):
        g = g.sort_values("start").reset_index(drop=True)
        days = g.day.unique()
        for dday in sorted(days):
            gd = g[g.day == dday].reset_index(drop=True)
            open_t = gd.start.iloc[0] - pd.Timedelta(minutes=int(r.integers(6, 25)))
            ev.append((open_t, scr, "STARTUP", "", ""))
            close_t = gd.end.iloc[-1] + pd.Timedelta(minutes=int(r.integers(4, 30)))
            for i, row in enumerate(gd.itertuples()):
                ev.append((row.start, scr, "LOGON", str(Wm.badge_at(pp, row.pid, row.start)), ""))
                nxt = gd.start.iloc[i + 1] if i + 1 < len(gd) else None
                own_next = [t for t in by_pid[row.pid] if t > row.start]
                own_next = own_next[0] if own_next else None
                u = r.random()
                implicit_ok = nxt is not None and (own_next is None or nxt <= own_next) and \
                    (nxt - row.end) <= pd.Timedelta(minutes=12)
                # the screen's 20-minute warning: an operator still logged on 20 minutes after logging on is prompted
                # and logs off, so no log-on stays open past 20 minutes, whether the next log-on or the shutdown
                # would have closed it
                stays = (nxt if nxt is not None else close_t) - row.start <= pd.Timedelta(minutes=P.PB_PROMPT_MIN)
                if u < P.PB_LOGOFF_P or (not implicit_ok and nxt is not None) or not stays:
                    ev.append((row.end, scr, "LOGOFF", str(Wm.badge_at(pp, row.pid, row.start)), ""))
                    truth.append((row.pid, scr, row.start, row.end, "LOGOFF"))
                elif nxt is None:
                    truth.append((row.pid, scr, row.start, close_t, "SHUTDOWN"))
                else:
                    truth.append((row.pid, scr, row.start, nxt, "NEXT"))
            ev.append((close_t, scr, "SHUTDOWN", "", ""))
    # tray rejects at Pier B are screen events too
    rb = rj[rj.area == "B"]
    for row in rb.itertuples():
        ev.append((row.ts, row.screen, "REJECT", str(Wm.badge_at(pp, row.pid, row.ts)), row.tray))
    evd = pd.DataFrame(ev, columns=["t", "Screen", "Event", "Badge", "Tray"])
    order = {"STARTUP": 0, "LOGOFF": 1, "LOGON": 2, "REJECT": 3, "SHUTDOWN": 4}
    evd["o"] = evd.Event.map(order)
    evd = evd.sort_values(["t", "o", "Screen"], kind="mergesort").reset_index(drop=True)
    loc = evd.t.dt.tz_convert(LONDON)
    out = pd.DataFrame({"Date": loc.dt.strftime("%d/%m/%Y"), "Time": loc.dt.strftime("%H:%M:%S"),
                        "Screen": evd.Screen, "Event": evd.Event, "Badge": evd.Badge, "Tray": evd.Tray})
    _write_csv(target, "pbev", out)
    W["pb_logged"] = pd.DataFrame(truth, columns=["pid", "screen", "on", "off", "end_by"])
    W["ct_rows"] = pos


def clear_hours(target, W, floor=P.HOURS_EDGE_TARGET, rounds=4):
    """keep every team's 2026 screen time clear of a tenth-of-an-hour edge. Where a team's total sits within `floor`
    hours of one, its latest short sessions that end a screen's day (nothing after them at that screen that day, the
    operator's next session at least 25 minutes off, the session still no longer than 20 minutes and inside the
    area's hours) run a little longer, by whole seconds, until it clears. Every projection, reject and search was
    drawn before, inside the sessions as they were, so none of them moves; the positions are written again."""
    import solve as SV
    pp, ss = W["people"], W["sessions"]
    cur = pp[pp.left.isna()]
    team_of = dict(zip(cur.index, cur.team_end))
    ros = SV.roster(target)
    edge = lambda v: 0.05 - abs(v - round(v, 1))
    for _ in range(rounds):
        h = SV.ask_hours(target, ros)
        need = {}
        for t, v in h.items():
            if edge(v) < floor:
                step = 1
                while edge(v + step / 3600.0) < floor + 0.005:
                    step += 1
                need[t] = step
        tot = float(h.sum()) + sum(need.values()) / 3600.0
        if edge(tot) < floor:
            step = 1
            while edge(tot + step / 3600.0) < floor + 0.005:
                step += 1
            # the airport's total prints too: teams with room inside their own tenth carry the rest between them
            for t in sorted(h.index):
                v = float(h[t]) + need.get(t, 0) / 3600.0
                room = 0
                while room < step and edge(v + (room + 1) / 3600.0) >= floor + 0.005 and \
                        round(v + (room + 1) / 3600.0, 1) == round(v, 1):
                    room += 1
                if room:
                    need[t] = need.get(t, 0) + room
                    step -= room
                if step <= 0:
                    break
            else:
                raise AssertionError("no team can carry the airport total off its edge")
        if not need:
            W["hours_moved"] = W.get("hours_moved", {})
            return
        y26 = pd.to_datetime(ss.day).dt.year == 2026
        loc_end = ss.end.dt.tz_convert(LONDON)
        mins = (loc_end - loc_end.dt.normalize()).dt.total_seconds() / 60.0
        for t, sec in sorted(need.items()):
            m = ss[y26 & ss.pid.map(team_of).eq(t)].sort_values(["end", "sid"], ascending=False)
            left = sec
            for i in m.index:
                if left <= 0:
                    break
                row = ss.loc[i]
                dur = (row.end - row.start).total_seconds()
                room = 20 * 60 - dur
                close = (15 * 60 + 30 if row.area == "B" else 22 * 60) - mins[i]
                room = int(min(room, close * 60.0, 180))
                if room < 1:
                    continue
                later = ss[(ss.screen == row.screen) & (ss.day == row.day) & (ss.start > row.start)]
                if len(later):
                    continue
                own = ss[(ss.pid == row.pid) & (ss.start > row.start)]
                if len(own) and (own.start.min() - row.end).total_seconds() < 25 * 60 + room:
                    continue
                add = min(room, left)
                ss.loc[i, "end"] = row.end + pd.Timedelta(seconds=add)
                W.setdefault("hours_moved", {}).setdefault(t, []).append((int(row.sid), int(add)))
                left -= add
            assert left <= 0, ("no session to carry the screen-time move", t, left)
        positions(target, W)
    raise AssertionError("screen time still on a rounding edge after %d rounds" % rounds)


# ----------------------------------------------------------------------------------------------- rejects and searches
def searches(target, W):
    pp, rj = W["people"], W["rejects"]
    r = _rng("search")
    c = rj[rj.area == "C"].sort_values(["ts", "lane"], kind="mergesort")
    out = pd.DataFrame({"reject_utc": _utc(c.ts), "lane": c.lane, "workstation": c.screen, "tray_tag": c.tray})
    _write_csv(target, "rej", out)
    s = rj.sort_values(["search_start", "tray"], kind="mergesort").reset_index(drop=True).copy()
    s["pos"] = np.where(s.area == "C", ["S%d" % v for v in r.integers(1, 5, len(s))], "PBS")
    # the tablet app's codes changed with its July update
    new = s.search_start >= pd.Timestamp("2026-07-01 03:00", tz="UTC")
    code_old = {"CLEAR": "NF", "RESTRICTED": "RI", "PROHIBITED": "PA"}
    s["code"] = np.where(new, s.outcome, s.outcome.map(code_old))
    # at the busiest times an officer clears two trays of one passenger on one record
    s["merged"] = False
    rows = []
    i = 0
    vals = s.to_dict("records")
    while i < len(vals):
        a = vals[i]
        if i + 1 < len(vals):
            b = vals[i + 1]
            if (a["area"] == b["area"] and a["pos"] == b["pos"] and a["outcome"] == "CLEAR" and b["outcome"] == "CLEAR"
                    and (b["search_start"] - a["search_start"]) <= pd.Timedelta(seconds=75) and b["ts"] < a["search_start"]
                    and a["tray"] != b["tray"] and r.random() < 0.55):
                rows.append(dict(search_id=a["search_id"], area=a["area"], pos=a["pos"], tray_tag=a["tray"] + ";" + b["tray"],
                                 taken=a["search_start"], completed=max(a["search_end"], b["search_end"]),
                                 outcome=a["code"], n=2, members=[a["search_id"], b["search_id"]]))
                i += 2
                continue
        rows.append(dict(search_id=a["search_id"], area=a["area"], pos=a["pos"], tray_tag=a["tray"],
                         taken=a["search_start"], completed=a["search_end"], outcome=a["code"], n=1,
                         members=[a["search_id"]]))
        i += 1
    sl = pd.DataFrame(rows)
    out = pd.DataFrame({"search_id": sl.search_id, "area": np.where(sl.area == "C", "Central", "Pier B"),
                        "search_position": sl.pos, "tray_tag": sl.tray_tag,
                        "taken_local": _local(sl.taken, "%Y-%m-%d %H:%M:%S"),
                        "completed_local": _local(sl.completed, "%Y-%m-%d %H:%M:%S"), "outcome": sl.outcome})
    _write_csv(target, "search", out)
    W["search_rows"] = sl


# ----------------------------------------------------------------------------------------------- ID badges
def badge_register(target, W):
    """the ID Centre's register of the badges it has issued to screening staff"""
    pp = W["people"]
    rows = []
    for pr in pp.itertuples():
        issued = pd.Timestamp(pr.start) - pd.Timedelta(days=int(3 + (pr.staff_no % 9)))
        if pd.notna(pr.badge_change):
            rows.append((int(pr.old_badge), pr.staff_no, issued, pr.badge_change, pr.badge_reason))
            rows.append((int(pr.badge), pr.staff_no, pr.badge_change, pd.NaT, ""))
        else:
            left = pd.Timestamp(pr.left) if pr.left is not None else pd.NaT
            rows.append((int(pr.badge), pr.staff_no, issued, left, "LEAVER" if pr.left is not None else ""))
    d = pd.DataFrame(rows, columns=["badge_no", "staff_no", "issued", "cancelled", "cancel_reason"])
    d = d.sort_values(["issued", "badge_no"], kind="mergesort")
    out = pd.DataFrame({"badge_no": d.badge_no.astype(str), "staff_no": d.staff_no.astype(str),
                        "issued": d.issued.dt.strftime("%d/%m/%Y"),
                        "cancelled": d.cancelled.dt.strftime("%d/%m/%Y").fillna(""), "cancel_reason": d.cancel_reason,
                        "issued_by": "ID Centre"})
    _write_csv(target, "badges", out)


# ----------------------------------------------------------------------------------------------- training
def training_frames(W):
    pp, a, e = W["people"], W["assess"], W["external"]
    desc = {"IIC": "Image Interpretation Certification (internal assessor)",
            "EXT-IIC": "Image Interpretation Certification (assessment centre)",
            "IIR": "Image Interpretation Refresher (annual)"}
    cur = pp[pp.left.isna()]
    aa = a[a.pid.isin(cur.index) & (a.date <= P.LMS_EXPORT)].copy()
    lms = pd.DataFrame({"Staff no": pp.staff_no.values[aa.pid.values], "Course code": aa.code.values,
                        "Course": aa.code.map(desc).values, "Completed": pd.to_datetime(aa.date.values),
                        "Result": aa.result.values, "Certificate ref": aa.cert_no.fillna("").values})
    lms = lms.sort_values(["Staff no", "Completed", "Course code"], kind="mergesort").reset_index(drop=True)
    ee = e[e.pid.isin(cur.index)].copy()
    assessed = pd.to_datetime(ee.assessed)
    keyed = pd.to_datetime(ee.keyed)
    lag = np.clip((keyed - assessed).dt.days.values // 2, 5, 30)
    issued = assessed + pd.to_timedelta(lag, unit="D")
    certs = pd.DataFrame({"certificate_no": ee.cert_no.values, "candidate_staff_no": pp.staff_no.values[ee.pid.values],
                          "assessment_date": assessed.dt.strftime("%d/%m/%Y").values,
                          "issued_date": issued.dt.strftime("%d/%m/%Y").values,
                          "centre": "Midlands Aviation Security Assessment Centre"})
    certs = certs.sort_values(["certificate_no"], kind="mergesort").reset_index(drop=True)
    return lms, certs


# ----------------------------------------------------------------------------------------------- distractors
def ops_files(target, W):
    r = _rng("ops")
    days = pd.date_range("2026-01-01", "2026-12-31", freq="D")
    rows = []
    for d in days:
        season = 1.0 + 0.32 * np.sin((d.dayofyear - 105) / 365.25 * 2 * np.pi)
        for lane in ["C%d" % i for i in range(1, 9)]:
            rows.append((d.strftime("%Y-%m-%d"), "Central", lane, int(r.poisson(1180 * season * r.uniform(0.7, 1.15)))))
        for lane in ("PB1", "PB2", "PB3"):
            v = int(r.poisson(560 * season * r.uniform(0.5, 1.2))) if ((d.toordinal() + 3) % 8 < 4 or r.random() < 0.6) else 0
            rows.append((d.strftime("%Y-%m-%d"), "Pier B", lane, v))
    _write_csv(target, "thru", pd.DataFrame(rows, columns=["date", "search_area", "lane", "trays_screened"]))
    q = []
    for d in days:
        for h in (5, 6, 7, 9, 12, 16, 18):
            if r.random() < 0.8:
                q.append((d.strftime("%Y-%m-%d"), "%02d:%02d" % (h, int(r.integers(0, 60))), "Central",
                          int(max(1, r.normal(9 + 6 * (h in (6, 7, 16)), 4)))))
            if h <= 12 and r.random() < 0.45:
                q.append((d.strftime("%Y-%m-%d"), "%02d:%02d" % (h, int(r.integers(0, 60))), "Pier B",
                          int(max(1, r.normal(7 + 5 * (h in (6, 7)), 3)))))
    _write_csv(target, "queue", pd.DataFrame(q, columns=["date", "sampled_at", "search_area", "minutes_queued"]))


def run(target):
    import docs as D
    import office as O
    W = Wm.run()
    tip_exports(target, W)
    ros, moves = roster_frames(W)
    O.xlsx(os.path.join(target, F["roster"]), [("Roster", ros), ("Moves 2026", moves)],
           author="Marian Taylor", created="2025-01-06T09:14:00Z", modified="2027-01-05T16:02:00Z",
           widths={"Roster": [10, 8, 28, 10, 12, 9, 9, 12], "Moves 2026": [10, 11, 10, 12]})
    positions(target, W)
    searches(target, W)
    badge_register(target, W)
    clear_hours(target, W)
    lms, certs = training_frames(W)
    O.xlsx(os.path.join(target, F["lms"]), [("Assessments", lms)], author="LMS Reporting",
           created="2027-01-11T07:30:00Z", modified="2027-01-11T07:30:00Z", widths={"Assessments": [10, 11, 52, 12, 8, 14]})
    _write_csv(target, "certs", certs)
    ops_files(target, W)
    D.write_all(target, F)
    return W
