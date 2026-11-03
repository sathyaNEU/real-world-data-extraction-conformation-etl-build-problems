"""Write the pack under <out>: each system's own extract, from the clean truth in world.py.

Layer 1 is what these systems do to their records and nothing else: offsets on timestamps, a court that is a code in
one system and a name in another, a claim form whose columns moved with the financial year, two EM record systems
either side of 2 February 2026, a provider spreadsheet and then a case app either side of 1 June 2026, UTC in the
incident and upload logs."""
import csv
import datetime as dt
import io
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import docs as D
import postprocess as PP
import world as W

SEED_PACK = 3998
DL_WEIGHTS = {1: [1.0], 2: [0.62, 0.38], 4: [0.34, 0.27, 0.22, 0.17]}
NZ = dt.timezone(dt.timedelta(hours=12))
COURT_LONG = {c: W.COURT_NAME[c] + " District Court" for c in W.COURTS}


def nz_offset(d):
    """+13 between the last Sunday of September and the first Sunday of April, +12 otherwise."""
    def last_sun_sep(y):
        x = dt.date(y, 9, 30)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)

    def first_sun_apr(y):
        x = dt.date(y, 4, 1)
        return x + dt.timedelta(days=(6 - x.weekday()) % 7)

    y = d.year
    if d >= last_sun_sep(y) or d < first_sun_apr(y):
        return 13
    return 12


def local_iso(d, minute):
    off = nz_offset(d)
    return "%sT%02d:%02d:00+%02d:00" % (d.isoformat(), minute // 60, minute % 60, off)


def utc_iso(d, minute):
    t = dt.datetime(d.year, d.month, d.day, minute // 60, minute % 60) - dt.timedelta(hours=nz_offset(d))
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ampm(minute):
    h, m = divmod(int(minute), 60)
    suf = "a.m." if h < 12 else "p.m."
    h12 = h % 12 or 12
    return "%d:%02d %s" % (h12, m, suf)


def write_csv(path, header, rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def write_xlsx(path, sheets, creator, created, modified, widths=None):
    wb = Workbook()
    wb.remove(wb.active)
    for name, header, rows in sheets:
        ws = wb.create_sheet(name)
        ws.append(header)
        for c in range(1, len(header) + 1):
            ws.cell(row=1, column=c).font = Font(bold=True)
        for r in rows:
            ws.append([None if (v == "" or v is None) else v for v in r])
        for i, h in enumerate(header, start=1):
            ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(11, min(34, len(h) + 4)))
        ws.freeze_panes = "A2"
    wb.save(path)
    PP.normalize_ooxml(path, creator, creator, created, modified, excel=True, company="Ministry of Justice")


def lawyers(rng, n=56):
    from faker import Faker
    fk = Faker("en_NZ")
    fk.seed_instance(SEED_PACK)
    return ["%s %s" % (fk.first_name(), fk.last_name()) for _ in range(n)]


def gapped(rng, n, lo=1, hi=9, base=0):
    """Identifiers as a system issues them to this extract: increasing, with the gaps other records left."""
    return [base + int(x) for x in np.cumsum(rng.integers(lo, hi, size=n))]


def addresses(rng, n):
    from faker import Faker
    fk = Faker("en_NZ")
    fk.seed_instance(SEED_PACK + 1)
    towns = ["Kestrel Bay", "Dunmore", "Ashgrove", "Thornmere", "Port Halsey", "Tarrin", "Ellsmere"]
    return ["%d %s, %s" % (int(rng.integers(1, 240)), fk.street_name(), towns[int(rng.integers(0, len(towns)))])
            for _ in range(n)]


def build_pack(w, out):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(SEED_PACK)
    law = lawyers(rng)
    fa, later, avl = w["first"], w["later"], w["avl"]

    # ---------------------------------------------------------------- the court's appearance extract (the spine)
    counsel_of = {}
    rows = []
    for r in fa.itertuples(index=False):
        cl = law[int(rng.integers(0, len(law)))] if r.own else ""
        counsel_of[r.crn] = cl
        rows.append((r.crn, "P%06d" % r.person, r.surname, r.given, r.dob.isoformat(), W.COURT_CODE[r.court],
                     "%s-1" % W.COURT_CODE[r.court], "Custody", "First appearance (custody)", r.date.isoformat(),
                     local_iso(r.date, r.call_min), r.officer, cl,
                     "Remanded in custody" if r.ric else _non_custody(rng), "", r.offence_code, r.offence,
                     r.date, r.call_min))
    assigned = {}
    for r in later.itertuples(index=False):
        if r.crn not in assigned:
            base = counsel_of.get(r.crn, "")
            assigned[r.crn] = base if base else (law[int(rng.integers(0, len(law)))] if rng.random() < 0.55 else "")
        cl = assigned[r.crn]
        rows.append((r.crn, "P%06d" % r.person, r.surname, r.given, r.dob.isoformat(), W.COURT_CODE[r.court],
                     "%s-%s" % (W.COURT_CODE[r.court], r.courtroom), r.list, r.appearance_type, r.date.isoformat(),
                     local_iso(r.date, int(r.call_min)), r.officer, cl, r.outcome,
                     r.next_date.isoformat() if r.next_date is not None and r.next_date == r.next_date else "",
                     r.offence_code, r.offence, r.date, int(r.call_min)))
    rows.sort(key=lambda x: (x[17], x[5], x[18], x[0]))
    # first appearances carry their next date
    nxt = {}
    for r in later.sort_values(["date"]).itertuples(index=False):
        nxt.setdefault(r.crn, r.date)
    final = []
    for r in rows:
        r = list(r[:17])
        if r[8] == "First appearance (custody)" and r[0] in nxt and r[13].startswith("Remanded"):
            r[14] = nxt[r[0]].isoformat()
        final.append(r)
    W_HDR = ["CRN", "PersonId", "Surname", "GivenNames", "DateOfBirth", "Court", "Courtroom", "List",
             "AppearanceType", "AppearanceDate", "CalledAt", "JudicialOfficer", "CounselOfRecord", "Outcome",
             "NextDate", "LeadOffenceCode", "LeadOffence"]
    write_csv(os.path.join(out, "cms_appearances_oct2024_sep2026.csv"), W_HDR, final)
    w["_appearances"] = final

    # ---------------------------------------------------------------- the sitting calendar
    sess = w["sessions"]
    avl_by = {a.date: a for a in avl.itertuples(index=False)}
    cal = []
    judges = W._officers()
    for s in sess.itertuples(index=False):
        c = s.court
        start = 600 if c != "RC" else 615
        cal.append((COURT_LONG[c], s.date, "Courtroom 1", "Custody list", s.am_officer, ampm(start), ampm(780)))
        if c == "KB":
            cal.append((COURT_LONG[c], s.date, "Courtroom 1", "Custody list", s.pm_officer, ampm(855), ampm(1005)))
            if s.date in avl_by:
                a = avl_by[s.date]
                cal.append((COURT_LONG[c], s.date, "Courtroom 2", "AVL remand list", a.officer, ampm(a.start),
                            ampm(a.end)))
        g = judges[c][int(rng.integers(0, len(judges[c])))]
        cal.append((COURT_LONG[c], s.date, "Courtroom 3", "General list", g, ampm(600), ampm(990)))
    cal.sort(key=lambda x: (x[1], x[0], x[2], x[5]))
    write_xlsx(os.path.join(out, "court_sitting_calendar_2024-2026.xlsx"),
               [("Sittings", ["Court", "Sitting date", "Courtroom", "List", "Presiding", "Start", "Finish"], cal)],
               "Halsey Coast scheduling", "2026-11-02T03:12:00Z", "2026-11-02T03:12:00Z",
               widths={"Court": 30, "Presiding": 32, "List": 18})

    # ---------------------------------------------------------------- duty lawyer returns, one workbook a year
    dl_names = {"KB": ["Hannah Moe", "Rawiri Pohatu", "Simon Kerr", "Leah Fifita"], "DN": ["Grant Ellery"],
                "AG": ["Mere Tautahi", "Owen Batts"], "RC": ["Owen Batts"]}
    # a duty lawyer claim is paid by the session and the hour: the return carries no defendant
    ret = {"2024-25": [], "2025-26": [], "2026-27": []}
    for s in sess.itertuples(index=False):
        c, d = s.court, s.date
        names = dl_names[c]
        lawyer = names[int(rng.choice(len(names), p=DL_WEIGHTS[len(names)]))]
        hours = round(float(np.clip(rng.normal(7.6 if c == "KB" else 4.8, 0.5), 3.0, 9.5)) * 4) / 4
        session = "Full day" if hours >= 6.0 else ("Morning" if rng.random() < 0.8 else "Afternoon")
        fy = "2024-25" if d < dt.date(2025, 7, 1) else ("2025-26" if d < dt.date(2026, 7, 1) else "2026-27")
        ret[fy].append((d, c, lawyer, session, hours))
    for fy, rr in ret.items():
        rr.sort(key=lambda x: (x[0], x[1]))
        if fy == "2024-25":
            hdr = ["Date", "Court", "Duty lawyer", "Session", "Hours"]
            body = [(d, COURT_LONG[c], l, se, h) for d, c, l, se, h in rr]
        else:
            hdr = ["Court", "Sitting date", "Duty lawyer", "Hours claimed", "Session claimed"]
            body = [(W.COURT_NAME[c], d, l, h, se) for d, c, l, se, h in rr]
        stamp = {"2024-25": ("2025-07-08T22:10:00Z", "2025-07-09T02:35:00Z"),
                 "2025-26": ("2026-07-07T21:55:00Z", "2026-07-08T03:20:00Z"),
                 "2026-27": ("2026-10-30T21:40:00Z", "2026-10-30T23:05:00Z")}[fy]
        write_xlsx(os.path.join(out, "duty_lawyer_returns_%s.xlsx" % fy), [("Returns", hdr, body)],
                   "Legal Aid Services", stamp[0], stamp[1], widths={"Court": 28})

    # ---------------------------------------------------------------- police bail summaries and the offence scale
    bs = []
    for r in fa.itertuples(index=False):
        arrest = r.date - dt.timedelta(days=1 if r.date.weekday() else 2)
        bs.append((r.crn, r.surname, r.given, r.dob.isoformat(), arrest.isoformat(), r.pri,
                   int(r.fta) * (1 + int(r.pri > 8)), "Y" if r.onb else "N", "N" if r.nfa else "Y",
                   "Y" if r.fv else "N"))
    write_csv(os.path.join(out, "police_bail_summaries_2024-2026.csv"),
              ["CRN", "Surname", "GivenNames", "DateOfBirth", "ArrestDate", "PriorConvictions", "PriorFTAWarrants",
               "OnBailAtArrest", "FixedAbode", "FamilyViolence"], bs)
    write_csv(os.path.join(out, "offence_seriousness_scale.csv"), ["OffenceCode", "Offence", "SeriousnessBand"],
              [(c, d, b) for c, d, b in W.OFFENCES])

    _em_files(w, out, rng)
    _bail_house_files(w, out, rng)
    _distractors(w, out, rng)
    D.build_docs(out)


def _non_custody(rng):
    u = rng.random()
    return "Remanded on bail" if u < 0.72 else ("Remanded at large" if u < 0.82 else "Convicted and sentenced")


def _em_files(w, out, rng):
    em = w["em"]
    addr = addresses(rng, int(em.n_addr.sum()) + 10)
    assessors = ["K. Haddon", "M. Te Hira", "J. Sorensen", "P. Ruakere", "A. Whitlock"]
    legacy, case, uploads = [], [], []
    ai = 0
    eref = dict(zip(em.order_id, gapped(rng, len(em), 1, 4, 1200)))
    cref = dict(zip(em.order_id, gapped(rng, len(em), 1, 6, 300)))
    switch, cutoff = W.EM_SWITCH, W.EM_SWITCH - dt.timedelta(days=3)
    for o in em.itertuples(index=False):
        names = addr[ai:ai + o.n_addr]
        ai += o.n_addr
        who = assessors[int(rng.choice(len(assessors), p=[0.29, 0.24, 0.2, 0.16, 0.11]))]
        if o.logged <= cutoff:
            done = o.filed <= cutoff
            for k, a in enumerate(names, start=1):
                legacy.append(("EMB-%05d/%d" % (eref[o.order_id], k), o.surname, o.given, o.dob, o.crn if o.crn_on_tracker else "",
                               COURT_LONG[o.court], o.logged, a, who, o.filed if done else None,
                               ("Suitable" if o.suitable else "Not suitable") if done else "",
                               "Completed" if done else "Migrated"))
            if done:
                continue
            order_date = switch
        else:
            order_date = o.order_date
        ref = "EMO-26-%05d" % cref[o.order_id]
        last = o.amended if (o.amended is not None and o.amended == o.amended) else None
        rep = max(o.filed, last) if last else o.filed
        for k, a in enumerate(names, start=1):
            case.append(("EMA-26-%05d-%d" % (cref[o.order_id], k), ref, o.crn, "%s, %s" % (o.surname, o.given),
                         W.COURT_CODE[o.court], order_date.isoformat(), a, rep.isoformat(),
                         "Suitable" if o.suitable else "Not suitable"))
        uploads.append((ref, "EM address assessment report", utc_iso(o.filed, int(rng.integers(540, 990))), who))
        if last and last > o.filed:
            uploads.append((ref, "EM address assessment report (amended)",
                            utc_iso(last, int(rng.integers(540, 990))), who))
    write_xlsx(os.path.join(out, "em_bail_tracker_2025-26.xlsx"),
               [("Tracker", ["Ref", "Surname", "First name", "DOB", "CRN", "Court", "Referral date", "Address",
                             "Assessor", "Report filed", "Outcome", "Status"], legacy)],
               "EM Bail Unit", "2025-08-01T20:05:00Z", "2026-02-01T22:48:00Z",
               widths={"Address": 34, "Court": 28})
    case.sort(key=lambda x: x[0])
    write_csv(os.path.join(out, "em_case_system_assessments.csv"),
              ["AssessmentId", "OrderRef", "CRN", "Name", "Court", "OrderDate", "Address", "ReportFiledDate",
               "Outcome"], case)
    uploads.sort(key=lambda x: (x[2], x[0]))
    write_csv(os.path.join(out, "em_document_uploads.csv"), ["OrderRef", "DocumentType", "UploadedAt", "UploadedBy"],
              uploads)
    w["_em_legacy"], w["_em_case"], w["_em_uploads"] = legacy, case, uploads


def _bail_house_files(w, out, rng):
    pl, ab = w["bh_place"], w["bh_abs"]
    place_rows, away_rows, inc = [], [], []
    pref = dict(zip(pl.placement, gapped(rng, len(pl), 1, 5, 2300)))
    for p in pl.itertuples(index=False):
        rec = p.end_recorded
        left = rec if rec <= W.EXTRACT else None
        if p.start_recorded < W.BH_SWITCH:
            fn = p.start_recorded.strftime("%d/%m/%Y")
        else:
            fn = p.start_recorded
        if left is not None and left < W.BH_SWITCH:
            lf = left.strftime("%d/%m/%Y")
        else:
            lf = left
        place_rows.append(("BH-%04d" % pref[p.placement], "%s %s" % (p.given, p.surname), p.dob, p.crn, p.house, fn,
                           lf, p.exit if left else ""))
        inc.append(("BH-%04d" % pref[p.placement], utc_iso(p.start, p.arrive_min), "Resident arrived"))
        if p.end <= W.EXTRACT:
            inc.append(("BH-%04d" % pref[p.placement], utc_iso(p.end, p.exit_min), p.exit_type))
    for a in ab.itertuples(index=False):
        if a.kind in ("custody", "hospital"):
            kind_out, kind_back = (("Taken into police custody", "Returned from police custody") if a.kind == "custody"
                                   else ("Admitted to hospital", "Returned from hospital"))
            inc.append(("BH-%04d" % pref[a.placement], utc_iso(a.out_date, a.out_min), kind_out))
            inc.append(("BH-%04d" % pref[a.placement], utc_iso(a.back_date, a.back_min), kind_back))
        if a.out_date >= W.BH_SWITCH and (a.kind == "leave" or a.nights >= 2):
            reason = {"custody": "Police custody", "hospital": "Hospital", "leave": "Approved leave"}[a.kind]
            away_rows.append(("BH-%04d" % pref[a.placement], a.out_date, a.back_date - dt.timedelta(days=1), reason))
    noise = ["Curfew check, resident present", "Visitor incident", "Property damage reported", "Medication incident",
             "Complaint from neighbour", "Curfew check, resident present"]
    gone = {}
    for a in ab.itertuples(index=False):
        gone.setdefault(a.placement, []).append((a.out_date.toordinal() * 1440 + a.out_min,
                                                 a.back_date.toordinal() * 1440 + a.back_min))
    for p in pl.itertuples(index=False):
        d = p.start + dt.timedelta(days=int(rng.integers(1, 9)))
        while d < min(p.end, W.EXTRACT):
            m = int(rng.integers(8 * 60, 21 * 60))
            k = noise[int(rng.integers(0, len(noise)))]
            t = d.toordinal() * 1440 + m
            if not any(lo - 60 <= t <= hi + 60 for lo, hi in gone.get(p.placement, [])):
                inc.append(("BH-%04d" % pref[p.placement], utc_iso(d, m), k))
            d += dt.timedelta(days=int(rng.integers(5, 16)))
    inc.sort(key=lambda x: (x[1], x[0]))
    away_rows.sort(key=lambda x: (x[1], x[0]))
    names = {"BH-%04d" % pref[p.placement]: "%s %s" % (p.given, p.surname) for p in pl.itertuples(index=False)}
    iid = gapped(rng, len(inc), 1, 7, 4100)
    inc = [("INC-%05d" % iid[i], pid, names[pid], t, k) for i, (pid, t, k) in enumerate(inc)]
    write_xlsx(os.path.join(out, "bail_house_register_2025-26.xlsx"),
               [("Placements", ["Placement", "Resident", "DOB", "CRN", "House", "First night", "Left",
                                "Reason left"], place_rows),
                ("Away", ["Placement", "Away from", "Away to (last night away)", "Reason"], away_rows)],
               "Coastline Bail Support Trust", "2025-07-01T19:30:00Z", "2026-11-01T23:02:00Z",
               widths={"Resident": 26, "Reason left": 30, "Away to (last night away)": 26})
    write_csv(os.path.join(out, "bail_house_incidents.csv"), ["IncidentId", "Placement", "Resident", "ReportedAt",
                                                               "Type"], inc)
    w["_bh_place_rows"], w["_bh_away_rows"], w["_bh_inc"] = place_rows, away_rows, inc


def _distractors(w, out, rng):
    fa, later = w["first"], w["later"]
    # the remand centre's daily muster by unit
    mus = []
    d = W.START
    base = 268.0
    while d <= W.END:
        drift = 1.0 + 0.10 * max(0.0, (d - W.P2_START).days) / 365.0
        for u, sh in (("Remand A", 0.34), ("Remand B", 0.31), ("Remand C", 0.25), ("Induction", 0.10)):
            mus.append((d.isoformat(), u, int(round(base * sh * drift + rng.normal(0, 4)))))
        d += dt.timedelta(days=1)
    write_csv(os.path.join(out, "remand_centre_daily_muster.csv"), ["MusterDate", "Unit", "Count"], mus)
    # the court-date reminder service's log, bailed defendants' later appearances
    rem = []
    k = 0
    for r in later.itertuples(index=False):
        if r.list != "General" or r.date < W.P2_START:
            continue
        if rng.random() < 0.62:
            k += 1
            sent = r.date - dt.timedelta(days=2)
            rem.append(("SMS%07d" % k, r.crn, r.date.isoformat(), local_iso(sent, 17 * 60 + int(rng.integers(0, 50))),
                        "Delivered" if rng.random() < 0.9 else "Failed"))
    rem.sort(key=lambda x: (x[3], x[0]))
    mid = gapped(rng, len(rem), 1, 12, 3300000)
    rem = [("SMS%07d" % mid[i],) + r[1:] for i, r in enumerate(rem)]
    write_csv(os.path.join(out, "court_reminder_service_log.csv"), ["MessageId", "CRN", "HearingDate", "SentAt",
                                                                    "Status"], rem)
