"""task177 pack: every file under target/, written from the records (records.py, ask.py) the way each source system
exports them, then made reproducible (postprocess.py)."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C          # noqa: E402
import docs as D            # noqa: E402
import postprocess as PP    # noqa: E402
import records as Rc        # noqa: E402

HEAD_FILL = PatternFill("solid", fgColor="DCE6F1")
STAMPS = {
    C.F_CODES: ("Contact Centre Systems", "Contact Centre Systems", "2026-06-22T15:10:00Z", "2026-07-08T19:44:00Z"),
    C.F_INVOICES: ("Accounts Payable", "Accounts Payable", "2026-02-09T16:02:00Z", "2027-01-04T15:21:00Z"),
    C.F_DICT: ("Sabrina Ward", "Sabrina Ward", "2026-03-03T17:25:00Z", "2027-01-04T16:02:00Z"),
}
LEG_HEAD = ("interaction_id", "leg_no", "source_system", "leg_type", "line_dnis", "caller_ani", "caller_entered",
            "menu_path", "start_utc", "end_utc", "queue", "adviser_id", "leg_result", "disposition", "talk_sec",
            "hold_sec", "wrap_sec", "transfer_to")
SESSION_KEYS = ("session_id", "conversation_id", "account_ref", "account_type", "org_ref", "channel", "call_ref",
                "started", "ended", "user_turns", "assistant_turns", "intent", "end_state", "release")

_CACHE = {}


def records():
    if "rec" not in _CACHE:
        w = Rc.World()
        _CACHE["world"] = w
        _CACHE["rec"] = Rc.Records(w)
    return _CACHE["world"], _CACHE["rec"]


def _col(j):
    s = ""
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def _sheet(ws, head, rows, widths=None):
    for j, h in enumerate(head):
        c = ws.cell(row=1, column=j + 1, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="top")
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            if v is None or v == "":
                continue
            c = ws.cell(row=i + 2, column=j + 1, value=v)
            if isinstance(v, str) and len(v) > 60:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for j, w in enumerate(widths):
            ws.column_dimensions[_col(j)].width = w
    ws.freeze_panes = ws.cell(row=2, column=1)


def _save(wb, path, key):
    wb.save(path)
    creator, last_by, created, modified = STAMPS[key]
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.ORG)


def write_legs(out, rec):
    legs = rec.legs_claimant + rec.legs_general + rec.legs_employer
    first = {}
    for lg in legs:
        k = lg["interaction_id"]
        if k not in first or lg["start_utc"] < first[k]:
            first[k] = lg["start_utc"]
    legs.sort(key=lambda lg: (first[lg["interaction_id"]], lg["interaction_id"], lg["leg_no"]))
    end = C.to_utc(dt.datetime.combine(C.REC_END + dt.timedelta(days=1), dt.time()))
    stop = Rc.iso_z(end)
    start = Rc.iso_z(C.to_utc(dt.datetime.combine(C.REC_START, dt.time())))
    rows = [tuple(lg[h] for h in LEG_HEAD) for lg in legs if start <= first[lg["interaction_id"]] < stop]
    return C.write_csv(os.path.join(out, C.F_LEGS), LEG_HEAD, rows)


def write_sessions(out, rec):
    ss = rec.sessions_claimant + rec.sessions_employer + rec.sessions_internal
    lo = dt.datetime.combine(C.REC_START, dt.time()).isoformat()
    hi = dt.datetime.combine(C.REC_END + dt.timedelta(days=1), dt.time()).isoformat()
    ss = [s for s in ss if lo <= s["started"] < hi]
    ss.sort(key=lambda s: (s["started"], s["session_id"]))
    with open(os.path.join(out, C.F_CONV), "w", encoding="utf-8", newline="\n") as fh:
        for s in ss:
            fh.write(json.dumps({k: s[k] for k in SESSION_KEYS}, ensure_ascii=False, separators=(",", ":")) + "\n")
    return len(ss)


def write_register(out, rec):
    rows = [(r["case_no"], r["claim_id"], r["program"], r["office"], r["opened"], r["closed"]) for r in rec.register]
    return C.write_csv(os.path.join(out, C.F_CLAIMS), ("case_no", "claim_id", "program", "office", "opened", "closed"),
                       rows)


def write_crosswalk(out, rec):
    rows = []
    for i, num, a, b in rec.phone_rows:
        rows.append((rec.case_no[i], "phone", num, a.isoformat(), "" if b is None else b.isoformat()))
    for i, acct in rec.accounts.items():
        first = rec.acct_first[i].date()
        linked = first - dt.timedelta(days=int(Rc.hexid("link", acct, n=4), 16) % 9)
        rows.append((rec.case_no[i], "assistant_account", acct, linked.isoformat(), ""))
    rows.sort(key=lambda r: (r[0], r[1], r[3]))
    return C.write_csv(os.path.join(out, C.F_XWALK),
                       ("case_no", "detail_type", "detail_value", "valid_from", "valid_to"), rows)


def write_overflow(out, world):
    rows = []
    k = 0
    initials = ("TJ", "BM", "LW", "ML", "JD")
    for d in sorted(world.ct.windows):
        if not (C.REC_START <= d <= C.REC_END):
            continue
        for a, b in world.ct.windows[d]:
            k += 1
            s = dt.datetime.combine(d, dt.time()) + dt.timedelta(minutes=a)
            e = dt.datetime.combine(d, dt.time()) + dt.timedelta(minutes=b)
            rows.append(("OE-%04d" % k, "Claimant Services", s.strftime("%Y-%m-%d %H:%M"), e.strftime("%Y-%m-%d %H:%M"),
                         initials[int(Rc.hexid("sup", k, n=4), 16) % len(initials)]))
    return C.write_csv(os.path.join(out, C.F_OVERFLOW), ("episode_no", "queue", "start_local", "end_local",
                                                           "logged_by"), rows)


def write_survey(out, rec):
    return C.write_csv(os.path.join(out, C.F_SURVEY), ("survey_id", "channel", "contact_ref", "sent_utc", "score"),
                       rec.survey)


CODE_SHEETS = {
    "leg_types": (("legacy_code", "new_code", "meaning"), (
        ("ACD", "ivr + queue", "Legacy reported the IVR and the queue wait as one leg, from the IVR's answer to the "
                               "queue's exit; the new platform splits them"),
        ("AGT", "agent", "An adviser on the call"),
        ("XFR", "transfer", "A transfer leg (not used on the claimant line since 2025: an overflow transfer is "
                            "recorded on the queue leg it left, with transfer_to)"))),
    "results": (("legacy_code", "new_code", "meaning"), (
        ("ANS", "answered", "Queue leg: an adviser answered"),
        ("ABN", "abandoned", "Queue leg: the caller hung up while waiting"),
        ("XFR", "transferred", "Queue leg: the call left the queue on a transfer to transfer_to"),
        ("CMP", "completed", "The leg ended normally"),
        ("REL", "released", "IVR leg: the caller hung up in the IVR"))),
    "dispositions": (("legacy_code", "new_code", "meaning"), (
        ("RS", "RESOLVED", "Adviser wrap-up: resolved on the call"),
        ("CB", "CALLBACK_BOOKED", "Adviser wrap-up: a callback booked to finish it"))),
    "queues": (("legacy_queue", "new_queue", "line"), (
        ("Q_CLM", "Claimant Services", "2049450100"),
        ("Q_GEN", "General Enquiries", "2049450100"),
        ("Q_EMP", "Employer Services", "2049450200"))),
    "cutover": (("item", "detail"), (
        ("Cutover", "The new platform (NLC) took both lines at 06:00 on Monday 6 July 2026."),
        ("History", "Legacy (AVX) legs from 5 January 2026 were loaded into the new platform's export layout with "
                    "their own codes and identifiers; times converted to UTC."),
        ("Agent legs", "Legacy agent legs carry talk time including hold; hold_sec is blank for them."))),
}


def write_codes(out):
    path = os.path.join(out, C.F_CODES)
    wb = Workbook()
    first = True
    for name, (head, rows) in CODE_SHEETS.items():
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name
        _sheet(ws, head, rows, widths=[18, 22, 90] if len(head) == 3 else [14, 110])
    _save(wb, path, C.F_CODES)


DICT_ROWS = [
    (C.F_LEGS, "", "The contact-centre platform's interaction-leg export, both lines, 5 January 2026 to 3 January 2027 "
                   "(calls by their first leg's start). One row per leg; every leg of a call carries its "
                   "interaction_id."),
    (C.F_LEGS, "interaction_id", "The call's identifier. Calls before the 6 July 2026 cutover keep the legacy "
                                 "platform's identifier."),
    (C.F_LEGS, "leg_no", "The leg's place in the call."),
    (C.F_LEGS, "source_system", "AVX: the legacy platform's history loaded at cutover. NLC: the new platform."),
    (C.F_LEGS, "leg_type", "What the leg is; codes in " + C.F_CODES + "."),
    (C.F_LEGS, "line_dnis", "The number dialled: 2049450100 the claimant line, 2049450200 the employer line."),
    (C.F_LEGS, "caller_ani", "The caller's number as presented (on the call's first leg)."),
    (C.F_LEGS, "caller_entered", "What the caller keyed in the IVR (on the call's first leg): the case number on the "
                                 "claimant line, the business number on the employer line. Blank where nothing was "
                                 "keyed."),
    (C.F_LEGS, "menu_path", "IVR options chosen (on the call's first leg). Claimant line: 1 then the topic (1 check-in, "
                            "2 payments, 3 earnings, 4 appointments, 5 documents, 0 other); 9 general enquiries (no "
                            "case number)."),
    (C.F_LEGS, "start_utc", "Leg start, UTC."),
    (C.F_LEGS, "end_utc", "Leg end, UTC."),
    (C.F_LEGS, "queue", "The queue the leg was in."),
    (C.F_LEGS, "adviser_id", "The adviser on an agent leg."),
    (C.F_LEGS, "leg_result", "How the leg ended; codes in " + C.F_CODES + "."),
    (C.F_LEGS, "disposition", "The adviser's wrap-up code on an agent leg."),
    (C.F_LEGS, "talk_sec", "Agent leg: seconds talking."),
    (C.F_LEGS, "hold_sec", "Agent leg: seconds on hold."),
    (C.F_LEGS, "wrap_sec", "Agent leg: seconds of after-call work."),
    (C.F_LEGS, "transfer_to", "Where a transferred call went (ASKPW-VOICE: the assistant's voice service)."),
    (C.F_CONV, "", "The assistant vendor's session export for the Prairie Works tenant, sessions started 5 January "
                   "2026 to 3 January 2027, one JSON object per line."),
    (C.F_CONV, "session_id", "One session."),
    (C.F_CONV, "conversation_id", "The conversation the session belongs to. A session closes after 30 minutes without a "
                                  "message; if the user comes back to the conversation it continues in a new session "
                                  "under the same conversation_id."),
    (C.F_CONV, "account_ref", "The account the session ran under. Blank on voice sessions."),
    (C.F_CONV, "account_type", "claimant, employer or staff; caller on a voice session."),
    (C.F_CONV, "org_ref", "For an employer account, the business number it is registered to."),
    (C.F_CONV, "channel", "app; web; voice (a claimant-line call passed to the voice service); employer (the employer "
                          "portal); console (the staff console)."),
    (C.F_CONV, "call_ref", "Voice sessions: the interaction_id of the call passed to the voice service."),
    (C.F_CONV, "started", "When the session started."),
    (C.F_CONV, "ended", "When the session ended."),
    (C.F_CONV, "user_turns", "Messages from the user."),
    (C.F_CONV, "assistant_turns", "Messages from the assistant."),
    (C.F_CONV, "intent", "What the session was about, as the assistant classified it."),
    (C.F_CONV, "end_state", "resolved: the assistant completed the task or answered without an adviser. handoff: an "
                            "adviser callback booked. abandoned: the user left. timeout: the session closed after 30 "
                            "minutes without a message."),
    (C.F_CONV, "release", "The assistant release in production when the session started."),
    (C.F_CLAIMS, "", "The case system's claims register: every claim open at any time from 5 January 2026 to 3 January "
                     "2027. Extracted 4 January 2027."),
    (C.F_CLAIMS, "case_no", "The jobseeker's case number."),
    (C.F_CLAIMS, "claim_id", "The claim."),
    (C.F_CLAIMS, "program", "The program the claim is under."),
    (C.F_CLAIMS, "office", "The office holding the case."),
    (C.F_CLAIMS, "opened", "The day the claim opened."),
    (C.F_CLAIMS, "closed", "The last day the claim was open. Blank: open at the extract."),
    (C.F_XWALK, "", "The case system's contact details by case, with their history."),
    (C.F_XWALK, "case_no", "The case."),
    (C.F_XWALK, "detail_type", "phone, or assistant_account (the Ask Prairie Works account linked to the case)."),
    (C.F_XWALK, "detail_value", "The number or the account."),
    (C.F_XWALK, "valid_from", "First day the detail held."),
    (C.F_XWALK, "valid_to", "Last day it held. Blank: current."),
    (C.F_OVERFLOW, "", "Workforce team's log of overflow episodes on the Claimant Services queue (the predicted wait over "
                       "the threshold, calls reaching the queue transferred to the assistant's voice service)."),
    (C.F_OVERFLOW, "start_local", "Start, Manitoba time."),
    (C.F_OVERFLOW, "end_local", "End, Manitoba time."),
    (C.F_OVERFLOW, "logged_by", "Supervisor on shift."),
    (C.F_SURVEY, "", "Post-contact survey: a sample of contacts sent a one-question survey by text message."),
    (C.F_SURVEY, "channel", "phone, assistant_chat or assistant_voice."),
    (C.F_SURVEY, "contact_ref", "interaction_id of the call, or conversation_id of the conversation."),
    (C.F_SURVEY, "sent_utc", "When the survey was sent, UTC."),
    (C.F_SURVEY, "score", "1 (very dissatisfied) to 5 (very satisfied). Blank: no answer."),
    (C.F_INVOICES, "", "The vendor's monthly invoices for 2026, as received."),
]


FIELD_TYPES = {"leg_no": "integer", "talk_sec": "integer", "hold_sec": "integer", "wrap_sec": "integer",
               "user_turns": "integer", "assistant_turns": "integer", "score": "integer",
               "start_utc": "timestamp", "end_utc": "timestamp", "started": "timestamp", "ended": "timestamp",
               "start_local": "timestamp", "end_local": "timestamp", "sent_utc": "timestamp",
               "opened": "date", "closed": "date", "valid_from": "date", "valid_to": "date"}


def write_dictionary(out):
    path = os.path.join(out, C.F_DICT)
    wb = Workbook()
    ws = wb.active
    ws.title = "fields"
    rows = [(f, fld, FIELD_TYPES.get(fld, "text") if fld else "", text) for f, fld, text in DICT_ROWS]
    _sheet(ws, ("file", "field", "type", "description"), rows, widths=[34, 20, 11, 120])
    _save(wb, path, C.F_DICT)


def _band(tiers, v):
    for code, band, fee in tiers:
        hi = band.replace(",", "").split()[-1]
        if v <= int(hi):
            return code
    return tiers[-1][0]


def invoice_tiers(rec):
    """the vendor bills sessions by the UTC month they start in, and voice by the started minute; its own support
    desk's sessions are not billed"""
    chat = [0] * 13
    voice = [0] * 13
    for s in rec.sessions_claimant + rec.sessions_employer + rec.sessions_internal:
        if s["org_ref"] == C.VENDOR_BN:
            continue
        t = dt.datetime.fromisoformat(s["started"])
        u = t if s["channel"] == "employer" else C.to_utc(t)
        if u.year != 2026:
            continue
        if s["channel"] == "voice":
            secs = (dt.datetime.fromisoformat(s["ended"]) - t).total_seconds()
            voice[u.month] += int(-(-secs // 60))
        else:
            chat[u.month] += 1
    return {m: (_band(D.CHAT_TIERS, chat[m]), _band(D.VOICE_TIERS, voice[m])) for m in range(1, 13)}


def write_invoices(out, rec):
    path = os.path.join(out, C.F_INVOICES)
    chat = {a: (b, c) for a, b, c in D.CHAT_TIERS}
    voice = {a: (b, c) for a, b, c in D.VOICE_TIERS}
    tiers = invoice_tiers(rec)
    rows = []
    for mth in range(1, 13):
        ct_, vt = tiers[mth]
        fee = chat[ct_][1] + voice[vt][1]
        issued = dt.date(2026 + (mth == 12), 1 if mth == 12 else mth + 1, 4 if mth == 12 else 6)
        rows.append(("RDI-INV-26%02d-0412" % mth, C.VENDOR, C.VENDOR_BN + " RT0001", "2026-%02d" % mth,
                     issued.isoformat(), ct_, chat[ct_][0], vt, voice[vt][0], fee, round(fee * 0.05, 2),
                     round(fee * 1.05, 2)))
    wb = Workbook()
    ws = wb.active
    ws.title = "invoices_2026"
    _sheet(ws, ("invoice_no", "supplier", "supplier_gst_hst", "service_month", "issued", "chat_tier", "chat_band",
                "voice_tier", "voice_band", "fees_cad", "gst_cad", "total_cad"), rows,
           widths=[20, 24, 18, 14, 12, 10, 20, 10, 20, 12, 10, 12])
    _save(wb, path, C.F_INVOICES)


MANIFEST = (
    (C.F_LEGS, "Contact centre platform (NLC), interaction-leg export", "Calls to the claimant and employer lines whose "
     "first leg started 5 January 2026 to 3 January 2027, Manitoba time; legacy platform (AVX) history from 5 January "
     "to the 6 July 2026 cutover as loaded into the new platform", "2027-01-04 05:40"),
    (C.F_CONV, "Riverlot reporting console, session export, Prairie Works tenant", "Sessions started 5 January 2026 to "
     "3 January 2027, every channel", "2027-01-04 06:15"),
    (C.F_CLAIMS, "Case system, claims register", "Claims open at any time from 5 January 2026 to 3 January 2027",
     "2027-01-04 07:02"),
    (C.F_XWALK, "Case system, contact details with history", "The register's cases", "2027-01-04 07:05"),
    (C.F_OVERFLOW, "Workforce team, overflow log", "Claimant Services queue, 2026", "2027-01-04 08:30"),
    (C.F_SURVEY, "Survey platform, post-contact survey export", "Surveys sent 5 January 2026 to 3 January 2027",
     "2027-01-04 08:44"),
    (C.F_INVOICES, "Accounts payable, vendor invoices", "Service months January to December 2026", "2027-01-04 09:21"),
    (C.F_CODES, "Contact Centre Systems, cutover code list", "Legacy and new platform codes", "2026-07-08"),
    (C.F_DICT, "Digital Channels, field descriptions", "The files in this pull", "2027-01-04 10:02"),
    (C.F_PLAN, "Digital Channels, rollout plan", "Release 4.0 rollout, version 1.4", "2026-12-16"),
    (C.F_ACCEPT, "Riverlot Dialogue Inc., acceptance test summary", "Release 4.0", "2026-12-01"),
    (C.F_ORDER, "Riverlot Dialogue Inc., usage tier order form", "Service months January to April 2027", "2026-12-14"),
)


def write_manifest(out, n):
    rows = []
    for f, system, covers, pulled in MANIFEST:
        rows.append((f, system, covers, n.get(f, ""), pulled))
    return C.write_csv(os.path.join(out, C.F_MANIFEST), ("file", "source", "covers", "rows", "pulled_or_issued"), rows)


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    world, rec = records()
    n = {}
    n[C.F_LEGS] = write_legs(out, rec)
    n[C.F_CONV] = write_sessions(out, rec)
    n[C.F_CLAIMS] = write_register(out, rec)
    n[C.F_XWALK] = write_crosswalk(out, rec)
    n[C.F_OVERFLOW] = write_overflow(out, world)
    n[C.F_SURVEY] = write_survey(out, rec)
    write_codes(out)
    write_dictionary(out)
    write_invoices(out, rec)
    D.write_plan(out)
    D.write_acceptance(out)
    D.write_order(out)
    n[C.F_MANIFEST] = write_manifest(out, n)
    return n
