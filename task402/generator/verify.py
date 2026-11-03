"""task402 independent verifier: reads only the shipped bundle (target/), on its own code path, and recomputes the
call, A's cost, the critical components and every ask figure; compares them with generator/figures.json.

    python3 task402/generator/verify.py [target_dir]
"""
import io
import json
import os
import re
import sys
import zipfile
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LON = ZoneInfo("Europe/London")
FY = (date(2025, 4, 1), date(2026, 3, 31))
FY0 = (date(2024, 4, 1), date(2025, 3, 31))
SHORT = {"Katherine": "Kate", "Catherine": "Cath", "Elizabeth": "Liz", "Rebecca": "Becky", "Jennifer": "Jen",
         "Samantha": "Sam", "Victoria": "Vicky", "Margaret": "Maggie", "Christopher": "Chris", "Robert": "Rob",
         "Michael": "Mike", "Thomas": "Tom", "Matthew": "Matt", "Daniel": "Dan", "Jonathan": "Jon", "William": "Will",
         "Alexander": "Alex", "Nicholas": "Nick", "Stephen": "Steve", "Deborah": "Debbie", "Rachel": "Rach",
         "Joanne": "Jo", "Susan": "Sue", "Patricia": "Trish", "Benjamin": "Ben"}
BANKS = {date(2025, 5, 5), date(2025, 5, 26), date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26),
         date(2026, 1, 1), date(2025, 4, 18), date(2025, 4, 21)}


def utc_to_local_date(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")).astimezone(LON).date()


def utc_to_local(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC")).astimezone(LON).replace(tzinfo=None)


def load(t):
    p = lambda f: os.path.join(t, f)
    refs = pd.read_csv(p("referrals_received_2023-10_to_2026-03.csv"), dtype=str)
    users = pd.read_excel(p("clinical_system_users_2026-05-06.xlsx"), dtype=str)
    leg = dict(zip(users["Legacy user code"], users["User ID"]))
    old = pd.read_csv(p("care_contacts_2023-10-02_to_2025-10-12.csv"), dtype=str)
    items = pd.read_csv(p("outcome_measures_items_2023-10-02_to_2025-10-12.csv"), dtype=str)
    it = items.set_index("ContactID")
    phq = it[[c for c in it.columns if c.startswith("PHQ9")]].astype(int).sum(axis=1)
    gad = it[[c for c in it.columns if c.startswith("GAD7")]].astype(int).sum(axis=1)
    o = pd.DataFrame({"ref": old.ReferralID, "date": pd.to_datetime(old.ApptDate, format="%d/%m/%Y").dt.date,
                      "time": old.ApptTime, "type": old.ContactType.str.lower(), "att": old.Attendance.str.lower(),
                      "step": old.CareStep.str[-1].astype(int), "user": old.TherapistCode.map(leg),
                      "phq": old.ContactID.map(phq), "gad": old.ContactID.map(gad)})
    new = pd.read_parquet(p("appointments_2025-10-13_to_2026-05-06.parquet"))
    n = pd.DataFrame({"ref": new.referral_id, "date": new.appointment_start.dt.date,
                      "time": new.appointment_start.dt.strftime("%H:%M"),
                      "type": new.appointment_type.map({"initial_assessment": "assessment", "treatment": "treatment"}),
                      "att": new.outcome.map({"attended": "attended", "did_not_attend": "dna",
                                              "cancelled_by_patient": "cancelled by patient"}),
                      "step": new.care_step.astype(int), "user": new.clinician_user_id,
                      "phq": new.phq9_total.astype("float"), "gad": new.gad7_total.astype("float")})
    c = pd.concat([o, n], ignore_index=True)
    assert c.user.notna().all(), "every contact maps to a user"
    bk = pd.read_excel(p("agency_bookings_psychological_therapies_2025-26.xlsx"), header=4, dtype=str)
    return refs, users, c, bk


def national(refs, c):
    t = c[(c.type == "treatment") & (c.att == "attended")].sort_values(["ref", "date", "time"])
    g = t.groupby("ref")
    out = refs.set_index("referral_id")[["discharge_date"]].copy()
    out["end"] = pd.to_datetime(out.discharge_date).dt.date
    out["n_att"] = g.size()
    out["n_att"] = out.n_att.fillna(0).astype(int)
    first, last = g.first(), g.last()
    out["case"] = (first.phq >= 10) | (first.gad >= 8)
    out["rec"] = (out.n_att >= 2) & out.case.fillna(False) & (last.phq <= 9) & (last.gad <= 7)
    out["first_user"] = first.user
    return out


def match_agency(users, bk):
    """Directory users of the agency staff group to booking references, by surname and a compatible forename."""
    ag = users[users["Staff group"] == "Agency"]
    rows = bk.groupby("Booking ref").agg(worker=("Worker", "first")).reset_index()
    rows["surname"] = rows.worker.str.split(",").str[0].str.strip().str.lower()
    rows["fore"] = rows.worker.str.split(",").str[1].str.strip().str.split(" ").str[0]
    out = {}
    for u in ag.itertuples():
        fn, sn = u.Name.split(" ", 1)[0], u.Name.split(" ", 1)[1].lower()
        cand = rows[(rows.surname == sn) & rows.fore.apply(lambda f: f == fn or SHORT.get(f) == fn)]
        assert len(cand) == 1, (u.Name, len(cand))
        out[u._1] = cand["Booking ref"].iloc[0]
    return out


def assignment_end(bk):
    e = bk.groupby("Booking ref")["Line end (UTC)"].max()
    return {k: utc_to_local_date(v) for k, v in e.items()}


def main_call(refs, users, c, bk, figs):
    m = national(refs, c)
    res = {}
    for fy, (a, b) in (("2024-25", FY0), ("2025-26", FY)):
        res["recoveries_" + fy] = int(m[(m.end >= a) & (m.end <= b)].rec.sum())
    hi_users = set(users[~users["Job title"].str.contains("Wellbeing Practitioner")]["User ID"])
    step3 = set(c[(c.type == "treatment") & c.user.isin(hi_users)].ref)
    assert step3 == set(c[(c.type == "treatment") & (c.step == 3)].ref), "SF7: the HI-therapist rule equals CareStep"
    ag = match_agency(users, bk)
    aend = assignment_end(bk)
    first_line = bk.groupby("Booking ref")["Line start (UTC)"].min().map(utc_to_local_date)
    cover = {u: r for u, r in ag.items() if first_line[r] >= date(2025, 5, 1)}
    yr = m[(m.end >= FY[0]) & (m.end <= FY[1]) & m.index.isin(step3) & (m.n_att >= 1)].copy()
    cc = c[c.ref.isin(yr.index)].sort_values(["ref", "date", "time"])
    broken, kat = {}, {}
    for ref, g in cc.groupby("ref"):
        tr = g[g.type == "treatment"]
        fu = tr.user.iloc[0]
        if fu not in cover:
            continue
        e = aend[cover[fu]]
        after = g[g.date > e]
        if len(after) and after.user.iloc[0] != fu:
            broken[ref] = True
            kat[ref] = int(((g.type == "treatment") & (g.att == "attended") & (g.date <= e)).sum())
    yr["broken"] = yr.index.isin(list(broken))
    br = yr[yr.broken]
    ub = yr[~yr.broken]
    exp = sum(ub[ub.n_att >= max(1, kat[r])].rec.mean() for r in br.index)
    res["broken_courses"] = len(br)
    res["broken_recovered"] = int(br.rec.sum())
    res["broken_expected"] = round(float(exp), 1)
    res["a_cost_exact"] = round(float(exp - br.rec.sum()), 1)
    res["a_cost"] = int(round((exp - br.rec.sum()) / 50.0) * 50)
    return res, m, cover


def ask_waiting(t, c):
    out = {}
    fa = c[(c.type == "treatment") & (c.att == "attended")].groupby("ref").date.min()
    for fn, col_t, col_r, fmt in (("step3_waiting_list_month_end_2025-04_to_2025-09.csv", "SnapshotTaken", "ReferralID", "%d/%m/%Y %H:%M"),
                                  ("step3_waiting_list_month_end_2025-10_to_2026-03.csv", "snapshot_at", "referral_id", "%Y-%m-%d %H:%M")):
        s = pd.read_csv(os.path.join(t, fn), dtype=str)
        s["taken"] = pd.to_datetime(s[col_t], format=fmt)
        for tk, g in s.groupby("taken"):
            mend = (tk.to_period("M") - 1).end_time.date()
            seen = g[col_r].map(fa)
            n = int((~(seen.notna() & (seen <= mend))).sum())
            out[str(pd.Period(mend, "M"))] = n
    return out


def ask_digital(t):
    d = json.load(open(os.path.join(t, "steadyway_activity_export_2025-07_to_2026-05.json")))
    ev = pd.DataFrame(d["events"])
    ev["local"] = ev.at_utc.map(utc_to_local)
    first = ev[ev.event == "section_started"].groupby("user_id").local.min()
    ev["begin"] = ev.user_id.map(first)
    ev["v2"] = ev.begin >= datetime(2026, 1, 5)
    secs = {v: ev[ev.v2 == v].groupby("module").content_id.nunique().to_dict() for v in (False, True)}
    done = ev[ev.event == "section_completed"]
    out = {}
    for uid, g in done.groupby("user_id"):
        b = first[uid]
        v2 = b >= datetime(2026, 1, 5)
        lim = b + timedelta(days=56)
        ok = g[g.local <= lim].groupby("module").content_id.nunique()
        fin = sum(1 for mod, k in ok.items() if k == secs[v2][mod])
        key = str(pd.Period(b.date(), "M"))
        out[key] = out.get(key, 0) + int(fin >= 4)
    return {k: out.get(k, 0) for k in ["2025-09", "2025-10", "2025-11", "2025-12", "2026-01", "2026-02"]}


def ask_agency(t, c, users, bk, cover):
    ts = pd.read_csv(os.path.join(t, "agency_timesheets_2025-04_to_2026-03.csv"), dtype=str)
    ts["wk"] = pd.to_datetime(ts["Week commencing"], format="%d/%m/%Y").dt.date
    ts["hrs"] = ts["Hours claimed"].astype(float)
    bk = bk.copy()
    bk["s"] = bk["Line start (UTC)"].map(utc_to_local_date)
    bk["e"] = bk["Line end (UTC)"].map(utc_to_local_date)
    bk["rate"] = bk["Charge rate (GBP per hour)"].astype(float)
    ref_user = {r: u for u, r in cover.items()}
    days_hours = []
    for ref, g in ts[ts["Booking ref"].isin(set(cover.values()))].groupby("Booking ref"):
        u = ref_user[ref]
        lines = bk[bk["Booking ref"] == ref]
        wd_seen = set(pd.Series(list(c[c.user == u].date)).map(lambda d: d.weekday()))
        if float(lines["Hours per week"].iloc[0]) >= 37.5:
            pat = {0, 1, 2, 3, 4}
        else:
            assert (0 in wd_seen) != (4 in wd_seen), ref
            pat = {0, 1, 2, 3} if 0 in wd_seen else {1, 2, 3, 4}
        t0, t1 = lines.s.min(), lines.e.max()

        def wdays(wk):
            return [wk + timedelta(days=i) for i in range(7) if (wk + timedelta(days=i)).weekday() in pat
                    and (wk + timedelta(days=i)) not in BANKS and t0 <= wk + timedelta(days=i) <= t1]
        weeks = sorted(g.wk.unique())
        w_start = t0 - timedelta(days=t0.weekday())
        for wk in weeks:
            rows = g[g.wk == wk].copy()
            rows["sub"] = pd.to_datetime(rows["Submitted"], format="%d/%m/%Y %H:%M")
            if wk == weeks[0] and wk > w_start and len(rows) >= 2:
                # a late first claim: the largest line covers every earlier week of the booking
                lump = rows.sort_values("hrs").iloc[-1]
                rows = rows.drop(lump.name)
                prev = []
                w0 = w_start
                while w0 < wk:
                    prev += wdays(w0)
                    w0 += timedelta(days=7)
                for d in prev:
                    days_hours.append((d, lump.hrs / len(prev), ref))
            rows = rows.sort_values("sub")
            if len(rows) == 2:
                # a corrected claim: a replacement timesheet on the agency portal, an adjustment line on e-rostering
                hrs = rows.hrs.iloc[1] if rows["sub"].iloc[0] < pd.Timestamp(2025, 8, 1) else rows.hrs.sum()
            else:
                hrs = rows.hrs.iloc[0]
            wd = wdays(wk)
            for d in wd:
                days_hours.append((d, hrs / len(wd), ref))
    dh = pd.DataFrame(days_hours, columns=["d", "h", "ref"])
    dh["rate"] = [float(bk[(bk["Booking ref"] == r) & (bk.s <= d) & (bk.e >= d)].rate.iloc[0]) for d, r in zip(dh.d, dh.ref)]
    dh["m"] = pd.to_datetime(dh.d).dt.to_period("M").astype(str)
    dh["cost"] = dh.h * dh.rate
    g = dh.groupby("m")[["h", "cost"]].sum()
    keep = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"]
    return ({k: int(round(g.at[k, "h"])) for k in keep}, {k: int(round(g.at[k, "cost"] / 100.0) * 100) for k in keep},
            {k: float(g.at[k, "h"]) for k in keep}, {k: float(g.at[k, "cost"]) for k in keep})


def check_pdf_and_docs(t):
    from pypdf import PdfReader
    txt = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(t, "monthly_performance_report_2026-03_provisional.pdf")).pages)
    assert "Staff group of the discharging clinician" in txt and len(txt) > 500
    from docx import Document
    plan = "\n".join(p.text for p in Document(os.path.join(t, "improvement_plan_2026-27.docx")).paragraphs)
    assert "read from the year's other referrals at the same step" in plan, "SF4 filed in the plan"
    assert "PHQ-9 total of 10 or more" in plan and "refreshed extract of 6 May 2026" in plan
    return True


def main(argv):
    t = argv[0] if argv else os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    refs, users, c, bk = load(t)
    res, m, cover = main_call(refs, users, c, bk, figs)
    bad = []
    for k, v in res.items():
        if figs[k] != v:
            bad.append((k, figs[k], v))
    w = ask_waiting(t, c)
    if w != figs["ask_waiting"]:
        bad.append(("ask_waiting", figs["ask_waiting"], w))
    dg = ask_digital(t)
    if dg != figs["ask_digital"]:
        bad.append(("ask_digital", figs["ask_digital"], dg))
    hrs, cost, hx, cx = ask_agency(t, c, users, bk, cover)
    if hrs != figs["ask_hours"]:
        bad.append(("ask_hours", figs["ask_hours"], hrs))
    if cost != figs["ask_cost"]:
        bad.append(("ask_cost", figs["ask_cost"], cost))
    check_pdf_and_docs(t)
    print("main", res)
    print("waiting", w)
    print("digital", dg)
    print("hours", hrs, "cost", cost)
    if bad:
        for b in bad:
            print("MISMATCH", b)
        print("VERIFY FAIL")
        return 1
    print("VERIFY PASS: every graded figure recomputes from the bundle")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
