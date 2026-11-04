"""Who worked which workstation when: the four-weekly rosters as published, the relief signallers' relief days,
and what happened on the day (sickness, swaps, rest-day working). The truth is the list of worked spans; the
published roster, the roster changes log and the control system's logins are three partial views of it."""
import datetime as dt

import world as W

D_START, N_START = 7, 19
WORKING = ("D", "N", "RD", "RN")


def shift_span(day, shift):
    """Local start and end of a day or night shift (a night ends at 07:00 local on the next day)."""
    if shift == "D":
        return (dt.datetime(day.year, day.month, day.day, D_START),
                dt.datetime(day.year, day.month, day.day, D_START + 12))
    nxt = day + dt.timedelta(days=1)
    return (dt.datetime(day.year, day.month, day.day, N_START), dt.datetime(nxt.year, nxt.month, nxt.day, D_START))


def span_hours(start_local, end_local):
    """Hours worked between two local wall times, on the clock (13 on the October night, 11 in March)."""
    return (W.local_to_utc(end_local) - W.local_to_utc(start_local)).total_seconds() / 3600.0


def build(staff):
    r = W.rng(3)
    groups = {ws: [p for p in staff if p["home"] == ws] for ws in W.WS_IDS}
    relief = [p for p in staff if p["relief"]]
    all_days = list(W.days(W.SIM_START - dt.timedelta(days=30), W.SIM_END + dt.timedelta(days=12)))
    away = {}
    for p in staff:
        a = set()
        for _ in range(4):
            s = all_days[int(r.integers(0, len(all_days) - 12))]
            for k in range(int(r.integers(5, 10))):
                a.add(s + dt.timedelta(days=k))
        tr = set(all_days[int(i)] for i in r.choice(len(all_days), size=int(r.integers(8, 13)), replace=False))
        away[p["staff_no"]] = dict(leave=a, training=tr - a)
    planned, code = {}, {}
    st = {p["staff_no"]: dict(run=0, last_shift=None, last_day=None, worked=[]) for p in staff}

    def free(p, day, shift, table):
        sn = p["staff_no"]
        if day < p["qualified"] or day in away[sn]["leave"] or day in away[sn]["training"] or (sn, day) in table:
            return False
        s = st[sn]
        prev = day - dt.timedelta(days=1)
        if s["last_day"] == prev and s["last_shift"] == "N" and shift == "D":
            return False
        if s["last_day"] == prev and s["run"] >= 4:
            return False
        if s["last_shift"] == "N" and shift == "D" and s["last_day"] is not None and (day - s["last_day"]).days < 3:
            return False
        return True

    def load(p, day):
        w = [d for d in st[p["staff_no"]]["worked"] if (day - d).days < 28]
        st[p["staff_no"]]["worked"] = w
        return len(w)

    def take(p, day, shift, table, c):
        sn = p["staff_no"]
        s = st[sn]
        s["run"] = s["run"] + 1 if s["last_day"] == day - dt.timedelta(days=1) else 1
        s["last_shift"], s["last_day"] = shift, day
        s["worked"].append(day)
        table[(sn, day)] = c

    # 1. the published roster: each workstation group's own signallers, the gaps left for the relief signallers
    for day in all_days:
        for ws in W.WS_IDS:
            for sh in ("D", "N"):
                cands = [p for p in groups[ws] if free(p, day, sh, code)]
                pick = None
                if cands:
                    def pref(p):
                        fy = W.first_two_years(p, day)
                        bias = 7.0 if (fy and sh == "N") else (0.8 if (not fy and sh == "D") else 0.0)
                        return (load(p, day) + bias + float(r.uniform(0, 0.9)), p["staff_no"])
                    p = min(cands, key=pref)
                    if load(p, day) < 12:
                        pick = p
                if pick is not None:
                    take(pick, day, sh, code, sh)
                    planned[(ws, day, sh)] = pick["staff_no"]
                else:
                    planned[(ws, day, sh)] = None
        gaps = [(ws, sh) for ws in W.WS_IDS for sh in ("D", "N") if planned[(ws, day, sh)] is None]
        r.shuffle(gaps)
        for ws, sh in gaps:
            cands = [p for p in relief if free(p, day, sh, code)]
            if cands:
                p = min(cands, key=lambda q: (load(q, day) + float(r.uniform(0, 0.9)), q["staff_no"]))
                take(p, day, sh, code, "R" + sh)
                planned[(ws, day, sh)] = ("RELIEF", p["staff_no"])
        for p in staff:
            sn = p["staff_no"]
            if (sn, day) in code or day < p["qualified"]:
                continue
            if day in away[sn]["leave"]:
                code[(sn, day)] = "AL"
            elif day in away[sn]["training"]:
                code[(sn, day)] = "TR"
    published = dict(code)
    # 2. what happened on the day
    busy = {k for k, v in published.items() if v in WORKING}
    spans, changes = [], []
    rd = W.rng(4)

    def cover_from(cands, day):
        cands = [p for p in cands if (p["staff_no"], day) not in busy and day >= p["qualified"]
                 and day not in away[p["staff_no"]]["leave"]]
        if not cands:
            return None
        return sorted(cands, key=lambda q: (load(q, day), q["staff_no"]))[0]

    for day in all_days:
        for ws in W.WS_IDS:
            for sh in ("D", "N"):
                who = planned[(ws, day, sh)]
                s0, s1 = shift_span(day, sh)
                if who is None:
                    c = cover_from(groups[ws], day) or cover_from([q for q in staff if not q["relief"]
                                                                  and ws in q["competent"]], day)
                    busy.add((c["staff_no"], day))
                    st[c["staff_no"]]["worked"].append(day)
                    spans.append((c["staff_no"], ws, s0, s1, "rest day working"))
                    changes.append(dict(day=day, shift=sh, rostered="", worked=c["staff_no"], change="Rest day working",
                                        start=s0, end=s1, ws=ws))
                    continue
                if isinstance(who, tuple):
                    spans.append((who[1], ws, s0, s1, "relief"))
                    continue
                u = float(rd.random())
                if u < 0.027:
                    c = cover_from([q for q in groups[ws] if q["staff_no"] != who], day) or \
                        cover_from([q for q in staff if not q["relief"] and ws in q["competent"] and q["staff_no"] != who], day)
                    if c is None:
                        spans.append((who, ws, s0, s1, "rostered"))
                        continue
                    busy.add((c["staff_no"], day))
                    if float(rd.random()) < 0.45:
                        cut = s0 + dt.timedelta(minutes=int(rd.integers(95, 560)))
                        cut = cut.replace(minute=(cut.minute // 30) * 30, second=0)
                        spans.append((who, ws, s0, cut, "rostered (part)"))
                        spans.append((c["staff_no"], ws, cut, s1, "sickness cover (part)"))
                        changes.append(dict(day=day, shift=sh, rostered=who, worked=c["staff_no"], change="Sickness cover",
                                            start=cut, end=s1, ws=ws))
                    else:
                        spans.append((c["staff_no"], ws, s0, s1, "sickness cover"))
                        changes.append(dict(day=day, shift=sh, rostered=who, worked=c["staff_no"], change="Sickness cover",
                                            start=s0, end=s1, ws=ws))
                elif u < 0.045:
                    m = cover_from([q for q in groups[ws] if q["staff_no"] != who
                                    and day not in away[q["staff_no"]]["training"]], day)
                    if m is None:
                        spans.append((who, ws, s0, s1, "rostered"))
                        continue
                    busy.add((m["staff_no"], day))
                    spans.append((m["staff_no"], ws, s0, s1, "swap"))
                    changes.append(dict(day=day, shift=sh, rostered=who, worked=m["staff_no"], change="Swap",
                                        start=s0, end=s1, ws=ws))
                else:
                    spans.append((who, ws, s0, s1, "rostered"))
    # a few whole-shift changes agreed by telephone on the day never reached the changes list; the control
    # system shows who signed on and worked the desk
    byp = {p["staff_no"]: p for p in staff}
    ru = W.rng(5)
    for ws in W.WS_IDS:
        cand = [c for c in changes if c["ws"] == ws and c["rostered"] and c["start"] == shift_span(
                    c["day"], c["shift"])[0] and dt.date(2025, 10, 3) <= c["day"] <= dt.date(2026, 9, 28)
                and W.first_two_years(byp[c["rostered"]], c["day"]) != W.first_two_years(byp[c["worked"]], c["day"])]
        cand.sort(key=lambda c: (c["day"], c["shift"]))
        for k in sorted(ru.choice(len(cand), size=min(len(cand), 2), replace=False).tolist()):
            cand[k]["unrecorded"] = True
    return dict(planned=planned, published=published, spans=spans, changes=changes, away=away, all_days=all_days)


def on_duty_index(spans):
    """ws -> sorted list of (start_utc, end_utc, staff_no, start_local, how)."""
    idx = {ws: [] for ws in W.WS_IDS}
    for sn, ws, s0, s1, how in spans:
        idx[ws].append((W.local_to_utc(s0), W.local_to_utc(s1), sn, s0, how))
    for ws in idx:
        idx[ws].sort()
    return idx


def who_at(idx, ws, t_utc):
    import bisect
    lst = idx[ws]
    k = bisect.bisect_right(lst, (t_utc, dt.datetime.max, "", None, "")) - 1
    while k >= 0:
        a, b, sn, s0, how = lst[k]
        if a <= t_utc < b:
            return sn, s0, how
        if b <= t_utc:
            break
        k -= 1
    return None, None, None
