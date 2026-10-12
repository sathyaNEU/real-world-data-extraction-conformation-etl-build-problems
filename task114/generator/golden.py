"""Every graded figure and every rung, recomputed from the files in target/ and nothing else."""
import datetime as dt
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TOR = ZoneInfo("America/Toronto")
QUARTERS = [("Q1", dt.date(2025, 10, 1), dt.date(2025, 12, 31)), ("Q2", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("Q3", dt.date(2026, 4, 1), dt.date(2026, 6, 30)), ("Q4", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]
RULE_DAYS = 12


def quarter_of(d):
    for q, a, b in QUARTERS:
        if a <= d <= b:
            return q
    return None


def load(T):
    T = Path(T)
    L = {}
    cal = pd.read_csv(T / "firm_calendar_fy2026.csv")
    L["work"] = sorted(dt.date.fromisoformat(x) for x in cal.loc[cal.day_type == "Working day", "date"])
    L["workset"] = set(L["work"])
    dr = pd.read_excel(T / "staff_directory_fy2026.xlsx", dtype=str)
    L["dir"] = dr
    L["upn2emp"] = dict(zip(dr["UPN"].str.lower(), dr["Employee No"]))
    card = dict(zip(dr["Adelaide Card"], dr["Employee No"]))
    badge = dict(zip(dr["Front St Badge"], dr["Employee No"]))
    a = pd.read_csv(T / "adelaide_access_events_fy2026.csv", dtype=str)
    a = a[a.result == "Granted"]
    a["emp"] = a.card_number.map(card)
    a = a.dropna(subset=["emp"])
    a["date"] = a.event_time.str[:10]
    f = pd.read_csv(T / "front_st_door_events_fy2026.csv", dtype=str)
    f["emp"] = f.Badge.map(badge)
    f = f.dropna(subset=["emp"])
    f["date"] = pd.to_datetime(f.Date, format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    pres = {}
    for emp, d in set(zip(a.emp, a.date)):
        pres.setdefault((emp, d), set()).add("A")
    for emp, d in set(zip(f.emp, f.date)):
        pres.setdefault((emp, d), set()).add("F")
    L["pres"] = pres
    L["events"] = pd.read_parquet(T / "calendar_events_fy2026.parquet")
    cl = L["events"][L["events"].categories == "Client meeting"]
    L["client_eid"], L["client_uid"] = set(cl.event_id), set(cl.ical_uid)
    fo = L["events"][L["events"].subject == "Focus time"]
    L["focus_eid"], L["focus_uid"] = set(fo.event_id), set(fo.ical_uid)
    L["att"] = pd.read_csv(T / "calendar_attendees_fy2026.csv", dtype=str)
    # people of the firm on each item (rooms and guests aside): one of them is one person, whatever else the booking
    # says; a series shares its iCal UID, so the UID takes the most any of its occurrences carries
    at = L["att"]
    firm = at[at.attendee_type.isin(["required", "optional"]) & at.attendee_address.str.lower().isin(L["upn2emp"])]
    L["n_int_eid"] = firm.groupby("event_id").size().to_dict()
    uid_of = dict(zip(L["events"].event_id, L["events"].ical_uid))
    n_uid = {}
    for eid, n in L["n_int_eid"].items():
        u = uid_of[eid]
        n_uid[u] = max(n_uid.get(u, 0), n)
    L["n_int_uid"] = n_uid
    cur = pd.read_excel(T / "room_register.xlsx", sheet_name="Rooms")
    chg = pd.read_excel(T / "room_register.xlsx", sheet_name="Changes")
    chg["Effective Date"] = pd.to_datetime(chg["Effective Date"]).dt.date
    spells = []
    for _, r in cur.iterrows():
        cs = chg[chg["Room Code"] == r["Room Code"]].sort_values("Effective Date")
        frm = dt.date(2019, 1, 1)
        for _, c in cs.iterrows():
            if c["Change"] != "Opened":
                spells.append(dict(r, **{"Room Type": c["Type Before"], "Valid From": frm,
                                         "Valid To": c["Effective Date"] - dt.timedelta(days=1)}))
            frm = c["Effective Date"]
        spells.append(dict(r, **{"Valid From": frm, "Valid To": None}))
    reg = pd.DataFrame(spells)
    L["reg"] = reg
    L["reg_current"] = cur
    L["halves"] = {c: w.split(";") for c, w in zip(cur["Room Code"], cur["Combinable With"].fillna(""))
                   if "+" in c and w}
    L["ab"] = pd.read_csv(T / "adelaide_room_bookings_fy2026.csv", dtype=str, keep_default_na=False)
    L["fb"] = pd.read_csv(T / "front_st_room_calendar_export.csv", dtype=str, keep_default_na=False)
    return L


def mins(hhmm):
    return int(hhmm[11:13]) * 60 + int(hhmm[14:16])


def peaks_by_day(rows, days, closed=False):
    """rows: iterable of (date_str, start_min, end_min). Half-open: a room freed at t serves a start at t."""
    by = defaultdict(list)
    for d, s, e in rows:
        by[d].append((s, 1))
        by[d].append((e + (1 if closed else 0), -1))
    out = {}
    for d in days:
        ev = sorted(by.get(d, []))
        c = m = 0
        for _, v in ev:
            c += v
            m = max(m, c)
        out[d] = m
    return out


def rule_count(pk, k=RULE_DAYS):
    """Fewest rooms with which no more than k days ran short (a day runs short when its peak exceeds the rooms)."""
    vals = sorted(pk.values(), reverse=True)
    return vals[k] if len(vals) > k else 0


def days_short(pk, R):
    return sum(1 for v in pk.values() if v > R)


# ---------------------------------------------------------------- the main call: the new office replayed
def internal_meetings(L, response_reading="non_declined", presence="either", include_cancelled=False,
                      include_client=False, include_townhall=False, types=("required", "optional")):
    ev = L["events"]
    excl = [c for c, inc in (("Client meeting", include_client), ("Town hall", include_townhall)) if not inc]
    keep = ev[(include_cancelled | ~ev.is_cancelled) & (~ev.is_all_day) & (~ev.categories.isin(excl))].copy()
    keep["date"] = keep.start_local.str[:10]
    keep = keep[keep.date.isin({d.isoformat() for d in L["workset"]})]
    at = L["att"]
    at = at[at.event_id.isin(set(keep.event_id)) & at.attendee_type.isin(list(types))].copy()
    at["emp"] = at.attendee_address.str.lower().map(L["upn2emp"])
    at = at.dropna(subset=["emp"])
    if response_reading == "non_declined":
        at = at[at.response != "declined"]
    elif response_reading == "accepted_only":
        at = at[at.response.isin(["accepted", "organizer"])]
    elif response_reading == "accepted_tentative":
        at = at[at.response.isin(["accepted", "tentative", "organizer"])]
    elif response_reading == "no_tentative":
        at = at[at.response.isin(["accepted", "none", "organizer"])]
    date_of = dict(zip(keep.event_id, keep.date))
    pres = L["pres"]
    n = defaultdict(int)
    na = defaultdict(int)
    nf = defaultdict(int)
    for eid, emp in zip(at.event_id, at.emp):
        d = date_of[eid]
        where = pres.get((emp, d))
        if presence == "ignore":
            n[eid] += 1
            continue
        if where:
            n[eid] += 1
            if "A" in where:
                na[eid] += 1
            if "F" in where:
                nf[eid] += 1
    keep["n"] = keep.event_id.map(n).fillna(0).astype(int)
    keep["na"] = keep.event_id.map(na).fillna(0).astype(int)
    keep["nf"] = keep.event_id.map(nf).fillna(0).astype(int)
    keep["s"] = keep.start_local.map(mins)
    keep["e"] = keep.end_local.map(mins)
    return keep


def main_call(L):
    days = [d.isoformat() for d in L["work"]]
    m = internal_meetings(L)
    need = m[m.n >= 2]
    pk = peaks_by_day(zip(need.date, need.s, need.e), days)
    R = rule_count(pk)
    order = sorted(pk.items(), key=lambda kv: (-kv[1], kv[0]))
    out = dict(rooms=R, days_short_at=days_short(pk, R), days_short_one_fewer=days_short(pk, R - 1),
               peaks=pk, meetings_needing_room=int(len(need)), ranked_days=order,
               days_above=[d for d, v in order if v > R])
    # the class the closed records never put on a room: no booking in either office, two or more in on one floor
    split = need[(need.na < 2) & (need.nf < 2)]
    out["split_meetings"] = int(len(split))
    return out, m


# ---------------------------------------------------------------- booking-based readings (the rungs below)
def room_type_on(reg, code, d):
    r = reg[(reg["Room Code"] == code) & (reg["Valid From"] <= d) & ((reg["Valid To"].isna()) | (reg["Valid To"] >= d))]
    return r["Room Type"].iloc[0] if len(r) else None


def adelaide_holds(L, released="held", shadows="physical", keep_cancelled=False, solo_reading="internal",
                   focus_as_call=False):
    """Room holds on the Adelaide platform: one row per physical room held, local time.

    released: held (to released_at wherever the platform gave the room back), status (only Released rows),
    full (to the booked end), drop (Released rows dropped).
    shadows: physical (half rows dropped, each combined booking counted on both halves), drop_combined (combined rows
    dropped, half rows kept), combined_as_one (half rows dropped, the combined room counted once), all (every row).
    solo_reading: internal (one person of the firm on the calendar item, a client meeting aside; the headcount where
    the booking has no item), headcount (headcount 1), source (headcount 1 on an app or kiosk booking).
    """
    b = L["ab"].copy()
    if not keep_cancelled:
        b = b[b.status != "Cancelled"]
    b["date"] = b.start.str[:10]
    b["s"] = b.start.map(mins)
    b["e"] = b.end.map(mins)
    if released in ("held", "status"):
        rel = (b.released_at != "") if released == "held" else (b.status == "Released")
        if rel.any():
            b.loc[rel, "e"] = b.loc[rel, "released_at"].map(mins).astype(int)
    elif released == "drop":
        b = b[b.status != "Released"]
    combined = b.room_code.str.contains(r"\+")
    half = b.booking_ref.str.contains("/")
    if shadows == "physical":
        whole = b[combined & ~half]
        parts = []
        for code, hs in L["halves"].items():
            w = whole[whole.room_code == code]
            for h in hs:
                parts.append(w.assign(room_code=h))
        b = pd.concat([b[~combined & ~half]] + parts).sort_index(kind="mergesort")
    elif shadows == "drop_combined":
        b = b[~combined]
    elif shadows == "combined_as_one":
        b = b[~half]
    b = b.copy()
    b["office"] = "A"
    if solo_reading == "internal":
        linked = b.outlook_event_id != ""
        firm_one = (b.outlook_event_id.map(L["n_int_eid"]) == 1) & ~b.outlook_event_id.isin(L["client_eid"])
        b["one"] = (linked & firm_one) | (~linked & (b.headcount == "1"))
    elif solo_reading == "headcount":
        b["one"] = b.headcount == "1"
    else:
        b["one"] = (b.headcount == "1") & b.source.isin(["Mobile app", "Kiosk"])
    b["solo"] = b["one"] & (focus_as_call | ~b.outlook_event_id.isin(L["focus_eid"]))
    return b


def front_holds(L, fold="series", local=True, keep_declined=False, keep_cancelled=False, solo_reading="internal",
                tentative=True, focus_as_call=False):
    """Room holds in the Front Street mailboxes, Toronto local time.

    fold: series (a series row whose slot an exception of any status took is dropped, whatever room it sits in),
    status_first (cancelled and declined rows filtered before the fold), room_key (the fold also matches the room),
    legacy (both), keep (no fold).
    solo_reading: internal (one person of the firm on the item the request carries, a client meeting aside),
    room_included (attendee_count 2, the organiser and the room), one (attendee_count 1).
    """
    b = L["fb"].copy()
    exc = b[b.is_exception == "True"]
    if fold in ("series", "room_key"):
        pool = exc
    else:
        keep_st = ["Accepted"] + (["Tentative"] if tentative else [])
        pool = exc[exc.response_status.isin(keep_st)]
    if fold != "keep":
        if fold in ("room_key", "legacy"):
            took = set(zip(pool.ical_uid, pool.original_start_utc, pool.room_mailbox))
            key = list(zip(b.ical_uid, b.start_utc, b.room_mailbox))
        else:
            took = set(zip(pool.ical_uid, pool.original_start_utc))
            key = list(zip(b.ical_uid, b.start_utc))
        series_row = (b.is_exception == "False") & pd.Series([k in took for k in key], index=b.index)
        b = b[~series_row]
    keep = ["Accepted"] + (["Tentative"] if tentative else []) + (["Declined"] if keep_declined else []) + (
        ["Cancelled"] if keep_cancelled else [])
    b = b[b.response_status.isin(keep)]

    def loc(ts):
        t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
        return t.astimezone(TOR) if local else t
    st = b.start_utc.map(loc)
    en = b.end_utc.map(loc)
    b = b.copy()
    b["date"] = st.map(lambda t: t.date().isoformat())
    b["s"] = st.map(lambda t: t.hour * 60 + t.minute)
    b["e"] = en.map(lambda t: t.hour * 60 + t.minute)
    wrap = b.e <= b.s
    b.loc[wrap, "e"] = b.loc[wrap, "e"] + 1440
    b["office"] = "F"
    reg = L["reg"]
    mb2code = dict(zip(reg.Mailbox, reg["Room Code"]))
    b["room_code"] = b.room_mailbox.map(mb2code)
    if solo_reading == "internal":
        b["one"] = (b.ical_uid.map(L["n_int_uid"]) == 1) & ~b.ical_uid.isin(L["client_uid"])
    else:
        b["one"] = b.attendee_count.astype(int) == (2 if solo_reading == "room_included" else 1)  # organiser and room
    b["solo"] = b["one"] & (focus_as_call | ~b.ical_uid.isin(L["focus_uid"]))
    return b


def legacy_adelaide_holds(L, released="held", shadows="physical", keep_cancelled=False, solo_reading="headcount"):
    """The legacy reading: release keyed on status, combined rows dropped (their half rows kept)."""
    b = L["ab"].copy()
    if not keep_cancelled:
        b = b[b.status != "Cancelled"]
    b["date"] = b.start.str[:10]
    b["s"] = b.start.map(mins)
    b["e"] = b.end.map(mins)
    if released == "held":
        rel = b.status == "Released"
        b.loc[rel, "e"] = b.loc[rel, "released_at"].map(mins)
    elif released == "drop":
        b = b[b.status != "Released"]
    combined = b.room_code.str.contains(r"\+")
    if shadows == "physical":
        b = b[~combined]
    elif shadows == "combined_as_one":
        b = b[~b.booking_ref.str.contains("/")]
    b["office"] = "A"
    if solo_reading == "headcount":
        b["solo"] = b.headcount == "1"
    else:
        b["solo"] = (b.headcount == "1") & b.source.isin(["Mobile app", "Kiosk"])
    return b


def legacy_front_holds(L, ghosts="drop", local=True, keep_declined=False, keep_cancelled=False, solo_reading="room_included",
                tentative=True):
    b = L["fb"].copy()
    keep = ["Accepted"] + (["Tentative"] if tentative else []) + (["Declined"] if keep_declined else []) + (
        ["Cancelled"] if keep_cancelled else [])
    b = b[b.response_status.isin(keep)]
    if ghosts == "drop":
        # a moved occurrence leaves its pattern row at the old slot; the exception row carries the old slot
        moved = set(zip(b.loc[b.is_exception == "True", "ical_uid"], b.loc[b.is_exception == "True", "original_start_utc"],
                        b.loc[b.is_exception == "True", "room_mailbox"]))
        pat = b.is_exception == "False"
        b = b[~(pat & pd.Series([(u, s, r) in moved for u, s, r in zip(b.ical_uid, b.start_utc, b.room_mailbox)],
                                index=b.index))]
    def loc(ts):
        t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
        return t.astimezone(TOR) if local else t
    st = b.start_utc.map(loc)
    en = b.end_utc.map(loc)
    b["date"] = st.map(lambda t: t.date().isoformat())
    b["s"] = st.map(lambda t: t.hour * 60 + t.minute)
    b["e"] = en.map(lambda t: t.hour * 60 + t.minute)
    wrap = b.e <= b.s
    b.loc[wrap, "e"] = b.loc[wrap, "e"] + 1440
    b["office"] = "F"
    reg = L["reg"]
    mb2code = dict(zip(reg.Mailbox, reg["Room Code"]))
    b["room_code"] = b.room_mailbox.map(mb2code)
    b["solo"] = b.attendee_count.astype(int) == (2 if solo_reading == "room_included" else 1)  # organiser plus the room
    return b


def typed(L, b, current_type=False):
    reg = L["reg"]
    cache = {}
    t = []
    for code, d in zip(b.room_code, b.date):
        on = dt.date(2026, 9, 30) if current_type else dt.date.fromisoformat(d)
        key = (code, on)
        if key not in cache:
            cache[key] = room_type_on(reg, code, on)
            if cache[key] is None and current_type:
                cache[key] = room_type_on(reg, code, dt.date.fromisoformat(d))
        t.append(cache[key])
    b = b.copy()
    b["rtype"] = t
    return b


def client_meetings(L, holds):
    """Holds whose calendar item is a client meeting (Adelaide by Outlook event id, Front Street by iCal UID)."""
    if "outlook_event_id" in holds.columns:
        return holds.outlook_event_id.isin(L["client_eid"])
    return holds.ical_uid.isin(L["client_uid"])


def office_figures(L, holds, office, current_type=False, client_out=True):
    """Ask A for one office: meeting-room hours and solo hours by quarter, the quarter's most rooms in use,
    rooms on 30 September, and the count its own bookings justify on the rule (calls out, and client meetings out,
    which the brief sends to the client suite)."""
    days = [d.isoformat() for d in L["work"]]
    h = typed(L, holds, current_type=current_type)
    h = h[h.date.isin(set(days))]
    mr = h[h.rtype == "meeting"]
    out = {}
    for q, a, b in QUARTERS:
        qd = [d for d in days if a.isoformat() <= d <= b.isoformat()]
        x = mr[mr.date.isin(set(qd))]
        hours = (x.e - x.s).sum() / 60.0
        solo = x[x.solo]
        pk = peaks_by_day(zip(x.date, x.s, x.e), qd)
        out[q] = dict(hours=round(hours, 2), solo_hours=round((solo.e - solo.s).sum() / 60.0, 2),
                      peak=max(pk.values()) if pk else 0)
    one = mr["one"] if "one" in mr.columns else mr.solo
    nonsolo = mr[~one & ~(client_meetings(L, mr) if client_out else False)]
    pk = peaks_by_day(zip(nonsolo.date, nonsolo.s, nonsolo.e), days)
    out["own_rule"] = rule_count(pk)
    reg = L["reg"]
    on = dt.date(2026, 9, 30)
    rr = reg[(reg.Office == ("Adelaide Street" if office == "A" else "Front Street")) & (reg["Room Type"] == "meeting")
             & (~reg["Room Code"].str.contains(r"\+")) & (reg["Valid From"] <= on)
             & ((reg["Valid To"].isna()) | (reg["Valid To"] >= on))]
    out["rooms_30_sep"] = int(rr["Room Code"].nunique())
    return out


def close_out_figures(L, holds, office):
    """The quarterly close-out figures on the all-rooms scope (meeting and client rooms as typed on the day)."""
    days = [d.isoformat() for d in L["work"]]
    h = typed(L, holds)
    h = h[h.date.isin(set(days)) & h.rtype.isin(["meeting", "client"])]
    reg = L["reg"]
    oname = "Adelaide Street" if office == "A" else "Front Street"
    out = {}
    for q, a, b in QUARTERS:
        qd = [d for d in days if a.isoformat() <= d <= b.isoformat()]
        x = h[h.date.isin(set(qd))]
        # bookable hours: each room bookable that day, 08:00 to 18:00
        cap = 0
        for d in qd:
            dd = dt.date.fromisoformat(d)
            rr = reg[(reg.Office == oname) & reg["Room Type"].isin(["meeting", "client"])
                     & (~reg["Room Code"].str.contains(r"\+")) & (reg["Valid From"] <= dd)
                     & ((reg["Valid To"].isna()) | (reg["Valid To"] >= dd))]
            cap += rr["Room Code"].nunique() * 600
        core = (x.e.clip(upper=18 * 60) - x.s.clip(lower=8 * 60)).clip(lower=0).sum()
        pk = peaks_by_day(zip(x.date, x.s, x.e), qd)
        top = sorted(pk.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        start = a
        rr = reg[(reg.Office == oname) & (~reg["Room Code"].str.contains(r"\+")) & (reg["Valid From"] <= start)
                 & ((reg["Valid To"].isna()) | (reg["Valid To"] >= start))]
        out[q] = dict(meeting_rooms=int(rr[rr["Room Type"] == "meeting"]["Room Code"].nunique()),
                      client_rooms=int(rr[rr["Room Type"] == "client"]["Room Code"].nunique()),
                      hours=round((x.e - x.s).sum() / 60.0, 2), utilisation=round(100.0 * core / cap, 1),
                      peak=top[1], peak_date=top[0])
    return out


def booking_rungs(L, client_out=True):
    """The booking-based rungs, the brief applied: calls out, and client meetings out of the meeting rooms."""
    days = [d.isoformat() for d in L["work"]]
    A = typed(L, adelaide_holds(L))
    F = typed(L, front_holds(L))
    A = A[A.date.isin(set(days))]
    F = F[F.date.isin(set(days))]
    if client_out:
        A, F = A[~client_meetings(L, A)], F[~client_meetings(L, F)]
    am, fm = A[A.rtype == "meeting"], F[F.rtype == "meeting"]
    r = {}
    both = pd.concat([am, fm])
    nonsolo = both[~both.one]
    r["R1_bookings_with_solo"] = rule_count(peaks_by_day(zip(both.date, both.s, both.e), days))
    r["R2_bookings"] = rule_count(peaks_by_day(zip(nonsolo.date, nonsolo.s, nonsolo.e), days))
    pa = peaks_by_day(zip(am[~am.one].date, am[~am.one].s, am[~am.one].e), days)
    pf = peaks_by_day(zip(fm[~fm.one].date, fm[~fm.one].s, fm[~fm.one].e), days)
    r["R0_offices_added"] = rule_count(pa) + rule_count(pf)
    return r


def golden(T):
    L = load(T)
    main, m = main_call(L)
    out = {"main": {k: v for k, v in main.items() if k not in ("peaks", "ranked_days")}}
    out["main"]["design_day"] = main["ranked_days"][RULE_DAYS][0]
    out["daily_peaks"] = main["peaks"]
    out["rungs"] = booking_rungs(L)
    out["askA"] = {"A": office_figures(L, adelaide_holds(L), "A"), "F": office_figures(L, front_holds(L), "F")}
    out["askA"]["today_rooms"] = out["askA"]["A"]["rooms_30_sep"] + out["askA"]["F"]["rooms_30_sep"]
    out["close_outs"] = {"A": close_out_figures(L, adelaide_holds(L), "A"),
                         "F": close_out_figures(L, front_holds(L), "F")}
    return out


def replay_count(L, min_n=2, closed=False, **kw):
    days = [d.isoformat() for d in L["work"]]
    m = internal_meetings(L, **kw)
    need = m[m.n >= min_n]
    return rule_count(peaks_by_day(zip(need.date, need.s, need.e), days, closed=closed))
