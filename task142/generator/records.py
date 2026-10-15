"""The pack's CSV files, written from the world: the alliance's HITH episode extract and daily census, the stream
crosswalk and campus list, Bellbird's July to September 2026 visit export, the referral portal's export, Bellbird's
client accounts, the alliance finance calendar, Bellbird's 2025-26 declined referrals and the export manifest."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as WD

EP_COLS = ["member_code", "campus_code", "patient_no", "episode_no", "admission_date", "separation_date",
           "separation_mode", "program_stream", "principal_diagnosis"]
CEN_COLS = ["census_date", "member_code", "campus_code", "patient_no", "episode_no", "program_stream", "day_of_stay",
            "nurse_visits"]
XW_COLS = ["old_program", "old_program_name", "principal_diagnosis_category", "new_stream", "new_stream_name"]
CAMPUS_COLS = ["member_code", "member_name", "campus_code", "campus_name", "valid_from", "valid_to", "note"]
BB_COLS = ["visit_no", "client_code", "patient_ref", "nurse_id", "visit_type", "start_time", "end_time", "status",
           "recorded_at"]
PORTAL_COLS = ["referral_id", "member_code", "campus_code", "patient_no", "program_stream", "sent_at",
               "requested_start", "status", "bellbird_response_at"]
ACC_COLS = ["client_code", "account_name", "alliance_member_code", "opened", "account_status", "note"]
CAL_COLS = ["date", "weekday", "week_commencing", "finance_period", "period_end", "public_holiday_vic"]
DECL_COLS = ["referral_date", "client_code", "patient_ref", "program_stream", "reason_code", "reason"]
MAN_COLS = ["file", "contents", "source_system", "covers", "prepared_by", "prepared_on", "rows_or_pages"]


def stream_code(e):
    return WD.OLD_CODE[e["stream"]] if e["adm"] < K.REVISION else e["stream"]


def episode_rows(W):
    for e in W.eps:
        yield {"member_code": e["member"], "campus_code": e["campus"], "patient_no": e["patient"],
               "episode_no": e["episode"], "admission_date": e["adm"].isoformat(),
               "separation_date": "" if e["open"] else e["last"].isoformat(),
               "separation_mode": "" if e["open"] else e["mode"], "program_stream": stream_code(e),
               "principal_diagnosis": e["dx"]}


def census_rows(W):
    rows = []
    for e in W.eps:
        for k in range(e["stay"]):
            d = e["adm"] + dt.timedelta(days=k)
            if d < K.CENSUS0 or d > K.D1:
                continue
            campus = e["campus"]
            if e["member"] == "WMH":
                campus = WD.WM_CAMPUS_NEW[e["letter"]]
            rows.append((d, e["member"], e["episode"], {"census_date": d.isoformat(), "member_code": e["member"],
                                                         "campus_code": campus, "patient_no": e["patient"],
                                                         "episode_no": e["episode"], "program_stream": e["stream"],
                                                         "day_of_stay": k + 1,
                                                         "nurse_visits": K.visits_on_day(e["stream"], k)}))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return [x[3] for x in rows]


def crosswalk_rows():
    for old, cat, new in WD.CROSSWALK:
        yield {"old_program": old, "old_program_name": K.OLD_PROGRAMS[old], "principal_diagnosis_category": cat,
               "new_stream": new, "new_stream_name": K.SNAME[new]}


CAMPUS_LIST = [("NGH", "4103", "Northgate Hospital", "2019-07-01", "", ""),
               ("RBH", "4211", "Riverbend Hospital", "2019-07-01", "", ""),
               ("RBH", "4218", "Craigend Community Hospital", "2021-02-01", "", ""),
               ("WMH", "5121", "Westmere Hospital", "2019-07-01", "2025-02-28", "reissued as 5140 at the merger"),
               ("WMH", "5133", "Altona Park Hospital", "2019-07-01", "2025-02-28",
                "Altona Park Health; reissued as 5141 when it merged into Westmere Health"),
               ("WMH", "5140", "Westmere Hospital", "2025-03-01", "", ""),
               ("WMH", "5141", "Altona Park Hospital", "2025-03-01", "", "Altona Park campus of Westmere Health"),
               ("KDH", "5212", "Kingsdale Hospital", "2019-07-01", "", ""),
               ("HCH", "5307", "Hillcrest Hospital", "2019-07-01", "", "")]


def campus_rows():
    for m, code, name, a, b, note in CAMPUS_LIST:
        yield {"member_code": m, "member_name": K.NAME[m], "campus_code": code, "campus_name": name,
               "valid_from": a, "valid_to": b, "note": note}


def _utc(t):
    return K.to_utc(t)


def bb_rows(W):
    status = {("done", False): "COMPLETE", ("attempt", False): "NOTHOME", ("cancel", False): "CANCELLED",
              ("done", True): "Completed", ("attempt", True): "Attempted", ("cancel", True): "Cancelled"}
    for x in sorted(W.bb, key=lambda x: x["visit_no"]):
        new = x["posted"] >= K.APP_RELEASE
        yield {"visit_no": x["visit_no"], "client_code": x["client"], "patient_ref": x["pref"], "nurse_id": x["nurse"],
               "visit_type": x["type"], "start_time": _utc(x["start"]).strftime("%Y-%m-%dT%H:%M:%S"),
               "end_time": _utc(x["end"]).strftime("%Y-%m-%dT%H:%M:%S") if x["end"] else "",
               "status": status[(x["status"], new)], "recorded_at": _utc(x["posted"]).strftime("%Y-%m-%dT%H:%M:%S")}


def portal_rows(W):
    r = K.rng("portal_ids")
    n = 418200
    out = []
    for ref in W.refs:
        if ref["phone"] or not (K.Q3S <= ref["sent"].date() <= K.Q3E):
            continue
        n += int(r.integers(2, 19))
        e = ref["ep"]
        campus = WD.WM_CAMPUS_NEW[e["letter"]] if e["member"] == "WMH" else e["campus"]
        out.append({"referral_id": "IHR-%06d" % n, "member_code": e["member"], "campus_code": campus,
                    "patient_no": e["patient"], "program_stream": e["stream"],
                    "sent_at": ref["sent"].strftime("%Y-%m-%d %H:%M"), "requested_start": ref["start"].isoformat(),
                    "status": "Declined" if ref["declined"] else "Accepted",
                    "bellbird_response_at": _utc(ref["resp"]).strftime("%Y-%m-%dT%H:%M:%SZ")})
        ref["referral_id"] = out[-1]["referral_id"]
    return out


def account_rows():
    rows = [("C3920", "Altona Park Health", "WMH", "2022-08-15", "Active",
             "Altona Park campus patients of Westmere Health (Altona Park Health merged into Westmere Health on "
             "1 March 2025); account kept for that campus"),
            ("C4471", "Northgate Health - Hospital in the Home", "NGH", "2024-07-01", "Active", ""),
            ("C4472", "Riverbend Health - Hospital in the Home", "RBH", "2024-07-01", "Active", ""),
            ("C4475", "Westmere Health - Hospital in the Home", "WMH", "2024-07-01", "Active", ""),
            ("C4478", "Kingsdale Health - Hospital in the Home", "KDH", "2024-07-01", "Active", ""),
            ("C4480", "Hillcrest Health - Hospital in the Home", "HCH", "2024-07-01", "Active", ""),
            ("C4466", "Ironbark Health Alliance - program office", "", "2024-06-20", "Active",
             "billing account for the overflow agreement; no patients")]
    for c, name, m, opened, st, note in rows:
        yield {"client_code": c, "account_name": name, "alliance_member_code": m, "opened": opened,
               "account_status": st, "note": note}


def calendar_rows():
    hol = dict(K.VIC_HOLIDAYS)
    for d in K.days(K.FY0, K.FY1):
        p = (d.month - 7) % 12 + 1
        yield {"date": d.isoformat(), "weekday": d.strftime("%a"),
               "week_commencing": (d - dt.timedelta(days=d.weekday())).isoformat(),
               "finance_period": "P%02d %s %d" % (p, K.MON3[d.month], d.year),
               "period_end": "Y" if d == K.month_end(d) else "", "public_holiday_vic": hol.get(d, "")}


REASONS = [("CAP", "No nurse capacity in the area on the requested start"), ("SVC", "Outside Bellbird service area"),
           ("CLN", "Clinical needs outside the agreement (for example, a central line Bellbird does not manage)"),
           ("LAT", "Requested start too soon after referral"), ("DUP", "Patient already under Bellbird")]


def declined_rows():
    r = K.rng("declined_2025_26")
    out = []
    for d in K.days(dt.date(2025, 7, 1), dt.date(2026, 6, 30)):
        if r.random() < (0.21 if d.weekday() < 5 else 0.06):
            m = K.MEMBERS[int(r.choice(5, p=[0.27, 0.22, 0.19, 0.17, 0.15]))]
            code = WD.CLIENT[m] if not (m == "WMH" and r.random() < 0.25) else WD.CLIENT_ALTONA
            s = K.STREAMS[int(r.choice(8, p=[0.3, 0.14, 0.15, 0.07, 0.03, 0.14, 0.09, 0.08]))]
            if m in ("NGH", "WMH") and s in ("H04", "H05"):
                s = "H01"
            rc = REASONS[int(r.choice(5, p=[0.52, 0.14, 0.12, 0.15, 0.07]))]
            lo, hi = {"NGH": (392000, 399500), "RBH": (207500, 213500), "WMH": (104500, 109500),
                      "KDH": (318500, 323000), "HCH": (296500, 300000)}[m]
            pno = WD._patient_no(m, int(r.integers(lo, hi)), "A" if code == WD.CLIENT_ALTONA else "W")
            digits = "".join(ch for ch in pno if ch.isdigit()).lstrip("0")
            out.append({"referral_date": d.isoformat(), "client_code": code,
                        "patient_ref": "%s/%s" % (code, digits), "program_stream": s,
                        "reason_code": rc[0], "reason": rc[1]})
    return out
