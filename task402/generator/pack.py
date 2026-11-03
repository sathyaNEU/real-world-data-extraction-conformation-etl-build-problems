"""task402 pack: the shipped files, written from the clean truth (world.py) with the Layer 1 forms the
service's systems produce: the record migration of 13 October 2025 (practitioner codes re-keyed, item-level
measures before it and totals after), the people team's booking register (extensions as new lines, UTC
stamps), the agency portal's weekly timesheets, the waiting list's month-end snapshots and the digital
vendor's event export. Ask truths are computed here from the clean truth and returned to build.py."""
import json
import os
from datetime import date, datetime, time, timedelta

import numpy as np
import pandas as pd
from faker import Faker

import postprocess as PP
import world as W

EXPORT = W.EXTRACT                      # the refreshed extract, 6 May 2026
MIG = W.MIGRATION
BST = [(datetime(2023, 3, 26, 1), datetime(2023, 10, 29, 1)), (datetime(2024, 3, 31, 1), datetime(2024, 10, 27, 1)),
       (datetime(2025, 3, 30, 1), datetime(2025, 10, 26, 1)), (datetime(2026, 3, 29, 1), datetime(2026, 10, 25, 1))]
AGENCIES = {"A": "Halberd Clinical Staffing", "B": "Tarnside Health Recruitment"}
RATES = {("A", 2024): 57.80, ("A", 2025): 60.35, ("B", 2024): 59.65, ("B", 2025): 62.10}
FRAMEWORK_2025 = date(2025, 10, 1)
V2_RELEASE = date(2026, 1, 5)
TS_SEED = 4058
PORTAL = date(2025, 8, 1)
NICK = {"Katherine": "Kate", "Catherine": "Cath", "Elizabeth": "Liz", "Rebecca": "Becky", "Jennifer": "Jen",
        "Samantha": "Sam", "Victoria": "Vicky", "Margaret": "Maggie", "Christopher": "Chris", "Robert": "Rob",
        "Michael": "Mike", "Thomas": "Tom", "Matthew": "Matt", "Daniel": "Dan", "Jonathan": "Jon",
        "William": "Will", "Alexander": "Alex", "Nicholas": "Nick", "Stephen": "Steve", "Deborah": "Debbie",
        "Rachel": "Rach", "Joanne": "Jo", "Susan": "Sue", "Patricia": "Trish", "Benjamin": "Ben"}
MODULES = ["Module 1: Getting started", "Module 2: Understanding low mood", "Module 3: Noticing your thoughts",
           "Module 4: Changing what you do", "Module 5: Tackling worry", "Module 6: Problem solving",
           "Module 7: Staying well"]
SECTIONS_V1 = [3, 2, 3, 4, 2, 3, 2]
SECTIONS_V2 = [3, 2, 4, 4, 3, 3, 2]


def to_utc(dt):
    """Local wall-clock datetime to UTC (UK rules)."""
    for a, b in BST:
        if a <= dt < b:
            return dt - timedelta(hours=1)
    return dt


def utc_z(dt):
    return to_utc(dt).strftime("%Y-%m-%dT%H:%M:%SZ")


def working_days_after(d, n):
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in W.BANK:
            n -= 1
    return d


def first_working_day_after(d):
    return working_days_after(d, 1)


class Pack:
    def __init__(self, w, seed=40211):
        self.w = w
        self.rng = np.random.default_rng(seed)
        self.fk = Faker("en_GB")
        self.fk.seed_instance(seed)
        self.truth = {}
        self._ids()

    # -------------------------------------------------------------- identifiers and people
    def _ids(self):
        r = self.rng
        w = self.w
        refs = w.referrals.sort_values("ref")
        n = len(refs)
        rid, cur, new = {}, 1384217, 70412
        for row in refs.itertuples():
            if row.received >= MIG:
                new += int(r.choice([1, 1, 1, 2, 3, 5]))
                rid[row.ref] = "FTT%07d" % new
            else:
                cur += int(r.choice([1, 1, 1, 1, 2, 2, 3, 4, 7]))
                rid[row.ref] = str(cur)
        self.rid = rid
        alphabet = np.array(list("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"))
        pts = {}
        for row in refs.itertuples():
            pts[row.patient] = "".join(r.choice(alphabet, 10))
        self.pt = pts
        # practitioners: names, legacy codes, user ids
        used, prac = set(), {}
        codes = r.choice(np.arange(1100, 9800), size=len(w.prac), replace=False)
        uids = r.choice(np.arange(30100, 98900), size=len(w.prac), replace=False)
        for i, p in enumerate(w.prac.itertuples()):
            while True:
                female = r.random() < 0.78
                fn = self.fk.first_name_female() if female else self.fk.first_name_male()
                sn = self.fk.last_name()
                if (fn, sn) not in used:
                    used.add((fn, sn))
                    break
            legal = fn
            pref = NICK.get(fn, fn) if r.random() < 0.45 else fn
            middle = (self.fk.first_name_female() if female else self.fk.first_name_male()) if r.random() < 0.35 else ""
            legacy = "" if (p.start >= MIG) else "TH%04d" % codes[i]
            prac[p.pid] = dict(pid=p.pid, legal=legal, pref=pref, middle=middle, surname=sn, legacy=legacy,
                               uid="U%05d" % uids[i], kind=p.kind, step=p.step, start=p.start, leave=p.leave,
                               agency=("A" if (p.pid == "S3A-00" or r.random() < 0.55) else "B"))
        self.pr = prac

    def name_dir(self, pid):
        p = self.pr[pid]
        return "%s %s" % (p["pref"], p["surname"])

    def name_booking(self, pid):
        p = self.pr[pid]
        return "%s, %s%s" % (p["surname"].upper(), p["legal"], (" " + p["middle"]) if p["middle"] else "")

    # -------------------------------------------------------------- referrals
    def referrals(self, out):
        w, r = self.w, self.rng
        tr = w.truth.set_index("ref")
        reason = {"completed": "Mutually agreed completion of treatment",
                  "dropped_out": "Termination of treatment earlier than care professional planned",
                  "assessment_dna": "Not seen: did not attend assessment",
                  "signposted": "Assessed: signposted to another service",
                  "not_entered": "Did not attend first treatment appointment"}
        src = ["Self-referral", "Self-referral", "Self-referral", "GP", "GP", "Other primary care",
               "Secondary mental health", "Employer or occupational health"]
        rows = []
        for row in w.referrals.sort_values("ref").itertuples():
            t = tr.loc[row.ref]
            end = row.end
            er = t.end_reason
            if er == "left_waiting_list":
                rsn = "Declined treatment while waiting" if r.random() < 0.55 else "No response to contact while waiting"
            else:
                rsn = reason[er]
            if end > EXPORT:
                end, rsn = None, ""
            rows.append(dict(referral_id=self.rid[row.ref], nhs_number_pseudo=self.pt[row.patient],
                             referral_received=row.received.isoformat(),
                             referral_source=src[int(r.integers(0, len(src)))],
                             age_at_referral=int(row.age),
                             discharge_date=end.isoformat() if end else "", discharge_reason=rsn))
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(out, "referrals_received_2023-10_to_2026-03.csv"), index=False, lineterminator="\n")
        return df

    # -------------------------------------------------------------- contacts and measures
    def contacts(self, out):
        w, r = self.w, self.rng
        c = w.contacts.copy()
        c = c[c.date <= EXPORT].sort_values(["date", "hour", "cid"]).reset_index(drop=True)
        sc = w.scores.set_index("cid")
        med_old = {"phone": "Telephone", "face_to_face": "Face to face", "video": "Video",
                   "digital": "Internet enabled therapy", "group": "Group"}
        med_new = {"phone": "telephone", "face_to_face": "face_to_face", "video": "video_consultation",
                   "digital": "digital_supported", "group": "group"}
        att_old = {"attended": "Attended", "dna": "DNA", "cancelled_patient": "Cancelled by patient"}
        att_new = {"attended": "attended", "dna": "did_not_attend", "cancelled_patient": "cancelled_by_patient"}
        old = c[c.date < MIG]
        new = c[c.date >= MIG]
        # legacy system export
        oid = 5502817 + np.cumsum(r.choice([1, 1, 1, 2, 2, 3], size=len(old)))
        mins = r.choice([0, 0, 0, 15, 30, 30, 45], size=len(old))
        o = pd.DataFrame(dict(
            ContactID=oid, ReferralID=old.ref.map(self.rid).values,
            ApptDate=[d.strftime("%d/%m/%Y") for d in old.date],
            ApptTime=["%02d:%02d" % (h, m) for h, m in zip(old.hour, mins)],
            ContactType=np.where(old.ctype == "assessment", "Assessment", "Treatment"),
            Attendance=old.attend.map(att_old).values, ConsultMedium=old.modality.map(med_old).values,
            CareStep=np.where(old.step == 3, "Step 3", "Step 2"),
            TherapistCode=old.pid.map(lambda x: self.pr[x]["legacy"]).values))
        o.to_csv(os.path.join(out, "care_contacts_2023-10-02_to_2025-10-12.csv"), index=False, lineterminator="\r\n")
        # item-level measures on the legacy system
        rows = []
        for cid_new, cid in zip(oid, old.cid.values):
            if cid in sc.index:
                ph, ga = int(sc.at[cid, "phq9"]), int(sc.at[cid, "gad7"])
                rows.append([cid_new] + self.items(ph, 9) + self.items(ga, 7))
        cols = ["ContactID"] + ["PHQ9_Q%d" % i for i in range(1, 10)] + ["GAD7_Q%d" % i for i in range(1, 8)]
        pd.DataFrame(rows, columns=cols).to_csv(
            os.path.join(out, "outcome_measures_items_2023-10-02_to_2025-10-12.csv"), index=False, lineterminator="\r\n")
        # new system export, totals on the appointment row
        nid = r.choice(np.arange(81000000, 89999999), size=len(new), replace=False)
        nid.sort()
        mins = r.choice([0, 0, 0, 15, 30, 30, 45], size=len(new))
        starts = [datetime.combine(d, time(h, m)) for d, h, m in zip(new.date, new.hour, mins)]
        ph = [int(sc.at[x, "phq9"]) if x in sc.index else None for x in new.cid]
        ga = [int(sc.at[x, "gad7"]) if x in sc.index else None for x in new.cid]
        n = pd.DataFrame(dict(
            appointment_id=nid.astype("int64"), referral_id=new.ref.map(self.rid).values,
            appointment_start=pd.to_datetime(starts),
            appointment_type=np.where(new.ctype == "assessment", "initial_assessment", "treatment"),
            outcome=new.attend.map(att_new).values, consultation_medium=new.modality.map(med_new).values,
            care_step=new.step.astype("int64").values,
            clinician_user_id=new.pid.map(lambda x: self.pr[x]["uid"]).values,
            phq9_total=pd.array(ph, dtype="Int64"), gad7_total=pd.array(ga, dtype="Int64")))
        n.to_parquet(os.path.join(out, "appointments_2025-10-13_to_2026-05-06.parquet"), index=False)
        self.c_all = c
        return o, n

    def items(self, total, k):
        """Split a questionnaire total into k item scores of 0 to 3."""
        r = self.rng
        it = [0] * k
        for _ in range(total):
            cand = [i for i in range(k) if it[i] < 3]
            it[cand[int(r.integers(0, len(cand)))]] += 1
        return it

    # -------------------------------------------------------------- the user directory
    def directory(self, out):
        r = self.rng
        rows = []
        titles3e = ["High Intensity Therapist", "High Intensity Therapist", "CBT Therapist",
                    "Senior High Intensity Therapist", "Counsellor (Counselling for Depression)", "High Intensity CBT Therapist"]
        titles3a = ["High Intensity Therapist", "CBT Therapist", "Locum High Intensity Therapist", "High Intensity CBT Therapist"]
        seen = set(self.w.contacts.pid)
        for pid, p in sorted(self.pr.items(), key=lambda kv: kv[1]["uid"]):
            if pid not in seen:
                continue
            if p["step"] == 2:
                title = "Senior Psychological Wellbeing Practitioner" if r.random() < 0.15 else "Psychological Wellbeing Practitioner"
            elif p["kind"] == "agency":
                title = titles3a[int(r.integers(0, len(titles3a)))]
            else:
                title = titles3e[int(r.integers(0, len(titles3e)))]
            active = p["leave"] is None or p["leave"] >= EXPORT
            rows.append({"User ID": p["uid"], "Legacy user code": p["legacy"] or None, "Name": self.name_dir(pid),
                         "Job title": title, "Staff group": "Agency" if p["kind"] == "agency" else "Substantive",
                         "Account status": "Active" if active else "Inactive"})
        df = pd.DataFrame(rows)
        path = os.path.join(out, "clinical_system_users_2026-05-06.xlsx")
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append([None if (isinstance(v, float) and np.isnan(v)) or v is None or v == "" else v for v in row])
        for i, wdt in enumerate([10, 18, 26, 38, 14, 15]):
            ws.column_dimensions[chr(65 + i)].width = wdt
        wb.save(path)
        PP.normalize_ooxml(path, "Hollie Smith", "Hollie Smith", "2026-05-06T08:31:00Z", "2026-05-06T08:31:00Z",
                           excel=True, company="Fenwold Wellbeing Partnership")
        return df

    # -------------------------------------------------------------- the booking register
    def bookings(self, out):
        w, r = self.w, self.rng
        lines = []
        refs = {}
        seen = set(w.contacts.pid)
        for pid in sorted({b.pid for b in w.blocks.itertuples()} & seen):
            p = self.pr[pid]
            bl = w.blocks[w.blocks.pid == pid].sort_values("block")
            yy = bl.start.iloc[0].year % 100
            refs[pid] = "BK%02d-%04d" % (yy, int(r.integers(1000, 9999)))
            prev_end = None
            for b in bl.itertuples():
                if b.start > date(2026, 3, 31):
                    break
                if b.block == 0:
                    booked = b.start - timedelta(days=int(r.integers(6, 19)))
                else:
                    booked = prev_end - timedelta(days=int(r.integers(4, 24)))
                fw = 2025 if booked >= FRAMEWORK_2025 else 2024
                pat = w.pattern.get(pid, W.WEEK)
                hrs = 37.5 if len(pat) == 5 else 30.0
                lines.append({"pid": pid, "Booking ref": refs[pid], "Line": int(b.block) + 1,
                              "Worker": self.name_booking(pid), "Agency": AGENCIES[p["agency"]],
                              "Assignment": "High intensity therapist (CBT), Step 3",
                              "Booked on": booked.isoformat(),
                              "Line start (UTC)": utc_z(datetime.combine(b.start, time(0, 0))),
                              "Line end (UTC)": utc_z(datetime.combine(b.end, time(23, 59))),
                              "Hours per week": hrs, "Charge rate (GBP per hour)": RATES[(p["agency"], fw)],
                              "Framework": "NHS staffing framework 2024" if fw == 2024 else "NHS staffing framework 2025",
                              "_start": b.start, "_end": b.end, "_rate": RATES[(p["agency"], fw)]})
                prev_end = b.end
        bk = pd.DataFrame(lines).sort_values(["Booked on", "Booking ref", "Line"]).reset_index(drop=True)
        self.bk = bk
        self.bref = refs
        path = os.path.join(out, "agency_bookings_psychological_therapies_2025-26.xlsx")
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Bookings"
        ws.append(["Agency bookings: psychological therapies (step 3)"])
        ws.append(["Exported 05/05/2026 16:42 (times shown in UTC)"])
        ws.append(["An extension is booked as an additional line under the original booking reference; each line "
                   "covers the dates shown. Timesheets for these bookings were submitted through the agency portal "
                   "until 31 July 2025 and through e-rostering from 1 August 2025."])
        ws.append([])
        cols = [c for c in bk.columns if not c.startswith("_") and c != "pid"]
        ws.append(cols)
        for row in bk[cols].itertuples(index=False):
            ws.append(list(row))
        widths = [11, 6, 30, 30, 36, 12, 22, 22, 15, 26, 30]
        for i, wdt in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = wdt
        wb.save(path)
        PP.normalize_ooxml(path, "Josh Parry", "Josh Parry", "2026-05-05T15:42:00Z", "2026-05-05T15:44:00Z",
                           excel=True, company="Fenwold Wellbeing Partnership")
        return bk

    def line_rate(self, pid, d):
        b = self.bk[(self.bk.pid == pid) & (self.bk._start <= d) & (self.bk._end >= d)]
        return float(b._rate.iloc[0]) if len(b) else None

    # -------------------------------------------------------------- timesheets (ask 2)
    def timesheets(self, out, ts_seed=TS_SEED):
        w, r = self.w, np.random.default_rng(ts_seed)
        rows, daily = [], []
        mgrs = ["Angela Pritchard", "Fiona Hardy", "Daniel Armstrong"]
        for pid in sorted(self.bref):
            p = self.pr[pid]
            pat = w.pattern.get(pid, W.WEEK)
            bl = w.blocks[w.blocks.pid == pid]
            t0 = max(bl.start.min(), date(2025, 3, 31))
            t1 = min(bl.end.max(), date(2026, 3, 29))
            if t0 > t1:
                continue
            per_day = (37.5 if len(pat) == 5 else 30.0) / len(pat)
            wk = t0 - timedelta(days=t0.weekday())
            weeks = []
            # a late first claim: the portal account came late, so the first weeks are claimed together at the
            # contracted daily hours
            late = pid != "S3A-00" and r.random() < 0.55
            k = int(r.integers(2, 4)) if late else 0
            while wk <= t1:
                days = [wk + timedelta(days=i) for i in range(7)
                        if (wk + timedelta(days=i)).weekday() in pat and (wk + timedelta(days=i)) not in W.BANK
                        and t0 <= wk + timedelta(days=i) <= t1 and self.line_rate(pid, wk + timedelta(days=i))]
                if days:
                    jit = float(np.round(r.normal(0, 1.1) * 4) / 4) if len(weeks) >= k else 0.0
                    hrs = round(per_day * len(days) + jit, 2)
                    hrs = max(hrs, round(per_day * len(days) * 0.6, 2))
                    weeks.append((wk, days, hrs))
                    for d in days:
                        daily.append(dict(pid=pid, date=d, hours=hrs / len(days), rate=self.line_rate(pid, d)))
                wk += timedelta(days=7)
            if len(weeks) <= 4:
                k = 0
            for j, (wk, days, hrs) in enumerate(weeks):
                if j < k:
                    continue
                sub = wk + timedelta(days=int(r.integers(4, 9)))
                if r.random() < 0.14:
                    # a claim corrected after submission: the agency portal takes a replacement timesheet for the
                    # week; e-rostering, from 1 August 2025, takes an adjustment line for the difference
                    err = float(r.choice([-4, -3, -2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3, 3.75]))
                    claim = round(max(hrs + err, 1.0), 2)
                    later = sub + timedelta(days=int(r.integers(2, 10)))
                    rows.append(self._ts(pid, wk, claim, sub, mgrs, r))
                    fix = hrs if sub < PORTAL else round(hrs - claim, 2)
                    rows.append(self._ts(pid, wk, fix, later, mgrs, r))
                else:
                    rows.append(self._ts(pid, wk, hrs, sub, mgrs, r))
                if j == k and k:
                    tot = round(sum(h for _, _, h in weeks[:k]), 2)
                    rows.append(self._ts(pid, wk, tot, sub + timedelta(hours=int(r.integers(1, 30))), mgrs, r))
        ts = pd.DataFrame(rows).sort_values(["Submitted", "Timesheet no"]).reset_index(drop=True)
        ts.to_csv(os.path.join(out, "agency_timesheets_2025-04_to_2026-03.csv"), index=False, lineterminator="\r\n")
        dl = pd.DataFrame(daily)
        self.daily = dl
        # ask 2 truth: the initiative's therapists (not the long-standing locum), hours and cost by month
        ini = dl[dl.pid != "S3A-00"].copy()
        ini["month"] = pd.to_datetime(ini.date).dt.to_period("M")
        ini["cost"] = ini.hours * ini.rate
        g = ini.groupby("month")[["hours", "cost"]].sum()
        self.truth["ask2"] = {str(k): dict(hours=float(v.hours), cost=float(v.cost)) for k, v in g.iterrows()}
        return ts

    def _ts(self, pid, wk, hrs, sub, mgrs, r=None):
        r = r if r is not None else self.rng
        p = self.pr[pid]
        auth = sub + timedelta(days=int(r.integers(0, 4)), hours=int(r.integers(1, 8)))
        return {"Timesheet no": "TS%06d" % int(r.integers(100000, 999999)), "Booking ref": self.bref[pid],
                "Agency": AGENCIES[p["agency"]], "Worker": "%s %s" % (p["legal"], p["surname"]),
                "Week commencing": wk.strftime("%d/%m/%Y"), "Hours claimed": hrs,
                "Submitted": datetime.combine(sub, time(int(r.integers(8, 21)), int(r.integers(0, 60)))).strftime("%d/%m/%Y %H:%M"),
                "Authorised": datetime.combine(auth, time(int(r.integers(8, 18)), int(r.integers(0, 60)))).strftime("%d/%m/%Y %H:%M"),
                "Authorised by": mgrs[int(r.integers(0, len(mgrs)))], "Status": "Authorised"}

    # -------------------------------------------------------------- waiting list snapshots (ask 3)
    def waitlist(self, out):
        w, r = self.w, self.rng
        tr = w.truth
        c = w.contacts
        firstatt = c[(c.ctype == "treatment") & (c.attend == "attended")].groupby("ref").date.min()
        firstany = c[c.ctype == "treatment"].groupby("ref").date.min()
        recs = []
        for t in tr[tr.step == 3].itertuples():
            added = working_days_after(t.a_date, int(r.choice([0, 0, 1, 1, 2]))) if r.random() < 0.8 else t.a_date
            fa = firstatt.get(t.ref)
            if t.left_list:
                # the list is updated by the admin team on a working day
                d = t.left_date if (t.left_date.weekday() < 5 and t.left_date not in W.BANK) else first_working_day_after(t.left_date)
                rem_true = d
                rem_snap = datetime.combine(d, time(10, 0))
            elif fa is not None:
                rem_true = fa
                lag = int(r.choice([0, 0, 0, 1, 1, 2, 3, 4]))
                rem_snap = datetime.combine(working_days_after(fa, lag) if lag else fa, time(17, 30))
            else:
                d = t.end if (t.end.weekday() < 5 and t.end not in W.BANK) else first_working_day_after(t.end)
                rem_true = d
                rem_snap = datetime.combine(d, time(9, 0))
            therapy = "CBT" if r.random() < 0.72 else "Counselling for Depression"
            recs.append((t.ref, added, rem_true, rem_snap, therapy, fa))
        snaps_old, snaps_new, truth = [], [], {}
        months = pd.period_range("2025-04", "2026-03", freq="M")
        for m in months:
            mend = m.end_time.date()
            taken = datetime.combine(first_working_day_after(mend), time(6, 0))
            n_true = 0
            for ref, added, rem_true, rem_snap, therapy, fa in recs:
                if added <= mend and rem_true > mend:
                    n_true += 1
                if added <= taken.date() and rem_snap > taken and added < taken.date():
                    wk = (taken.date() - added).days // 7
                    status = "First appointment booked" if (fa is not None and (fa - taken.date()).days <= 21) else "Awaiting allocation"
                    row = (taken, ref, added, therapy, wk, status)
                    (snaps_old if m <= pd.Period("2025-09", "M") else snaps_new).append(row)
            truth[str(m)] = n_true
        self.truth["ask3"] = truth
        so = pd.DataFrame([dict(SnapshotTaken=t.strftime("%d/%m/%Y %H:%M"), ReferralID=self.rid[ref],
                                DateAddedToList=a.strftime("%d/%m/%Y"), TherapyRequested=th, WeeksOnList=wk,
                                ListStatus=st) for t, ref, a, th, wk, st in snaps_old])
        so.to_csv(os.path.join(out, "step3_waiting_list_month_end_2025-04_to_2025-09.csv"), index=False,
                  lineterminator="\r\n")
        sn = pd.DataFrame([dict(snapshot_at=t.strftime("%Y-%m-%d %H:%M"), referral_id=self.rid[ref],
                                added_to_list=a.isoformat(), therapy=th.lower().replace(" ", "_"),
                                weeks_on_list=wk, status=st.lower().replace(" ", "_"))
                           for t, ref, a, th, wk, st in snaps_new])
        sn.to_csv(os.path.join(out, "step3_waiting_list_month_end_2025-10_to_2026-03.csv"), index=False,
                  lineterminator="\n")
        return so, sn

    # -------------------------------------------------------------- digital programme (ask 1)
    def digital(self, out):
        w, r = self.w, self.rng
        tr = w.truth
        dig = tr[(tr.step == 2) & (tr.modality == "digital")]
        ids_v1 = [["%08x" % int(r.integers(0, 2 ** 32)) for _ in range(k)] for k in SECTIONS_V1]
        # the January 2026 content release: module 3 drops its last section for two new ones, module 5 gains one
        keep = {2: 2}
        ids_v2 = [list(ids_v1[i][:keep.get(i, len(ids_v1[i]))]) +
                  ["%08x" % int(r.integers(0, 2 ** 32)) for _ in range(SECTIONS_V2[i] - keep.get(i, len(ids_v1[i])))]
                  for i in range(7)]
        users, events, truth, legacy = [], [], {}, []
        for t in dig.sort_values("start").itertuples():
            st = t.start
            if st < date(2025, 4, 1) or st > date(2026, 3, 31):
                continue
            begin = datetime.combine(st, time(0)) + timedelta(days=int(r.integers(0, 3)),
                                                             minutes=int(r.integers(7 * 60, 23 * 60 + 30)))
            keen = 0.035 if t.rec else 0.14
            if st < W.DIGITAL_SWITCH:
                # the previous vendor: module completions by referral, local time
                tt = begin
                for mi in range(8):
                    if r.random() < keen * 1.6 and mi > 0:
                        break
                    tt = tt + timedelta(days=float(r.gamma(2.2, 3.4)))
                    legacy.append(dict(ReferralNo=self.rid[t.ref], ModuleNo=mi + 1,
                                       CompletedOn=tt.strftime("%d/%m/%Y %H:%M")))
                continue
            v = ids_v2 if st >= V2_RELEASE else ids_v1
            uid = "%08x-%04x-4%03x-%04x-%012x" % tuple(int(r.integers(0, 16 ** k)) for k in (8, 4, 3, 4, 12))
            invited = begin - timedelta(days=int(r.integers(1, 9)), minutes=int(r.integers(0, 600)))
            users.append(dict(user_id=uid, service_ref=self.rid[t.ref], invited_utc=utc_z(invited)))
            tt = begin
            done = {}
            stop = False
            for mi in range(7):
                for si, cid in enumerate(v[mi]):
                    if (mi or si) and r.random() < keen:
                        stop = True
                        break
                    if mi or si:
                        tt = tt + timedelta(days=float(r.gamma(1.6, 1.55)), minutes=int(r.integers(0, 300)))
                    events.append(dict(user_id=uid, module=MODULES[mi], content_id=cid, event="section_started",
                                       at_utc=utc_z(tt)))
                    tc = tt + timedelta(minutes=int(r.integers(6, 95)))
                    events.append(dict(user_id=uid, module=MODULES[mi], content_id=cid, event="section_completed",
                                       at_utc=utc_z(tc)))
                    done[(mi, si)] = tc
                    tt = tc
                if stop:
                    break
            lim = begin + timedelta(days=56)
            fin = sum(1 for mi in range(7) if all((mi, si) in done and done[(mi, si)] <= lim for si in range(len(v[mi]))))
            m = str(pd.Period(begin.date(), "M"))
            truth.setdefault(m, [0, 0])
            truth[m][0] += 1
            truth[m][1] += int(fin >= 4)
        # invited, never began
        for t in tr[(tr.step == 2) & (tr.modality == "phone")].sample(frac=0.025, random_state=int(r.integers(0, 10 ** 6))).itertuples():
            if t.start is None or not (W.DIGITAL_SWITCH <= t.start <= date(2026, 3, 20)):
                continue
            uid = "%08x-%04x-4%03x-%04x-%012x" % tuple(int(r.integers(0, 16 ** k)) for k in (8, 4, 3, 4, 12))
            users.append(dict(user_id=uid, service_ref=self.rid[t.ref],
                              invited_utc=utc_z(datetime.combine(t.start, time(int(r.integers(9, 17)), 5)))))
        events.sort(key=lambda e: (e["at_utc"], e["user_id"], e["event"]))
        users.sort(key=lambda u: u["invited_utc"])
        doc = {"export": {"exported_utc": "2026-05-06T07:14:52Z", "organisation": "Fenwold Talking Therapies",
                          "programme": "Steadyway: guided CBT for low mood and worry", "from": "2025-07-01", "to": "2026-05-05"},
               "users": users, "events": events}
        with open(os.path.join(out, "steadyway_activity_export_2025-07_to_2026-05.json"), "w") as f:
            json.dump(doc, f, indent=1)
        pd.DataFrame(legacy).to_csv(os.path.join(out, "quillfern_module_completions_2025-04_to_2025-06.csv"),
                                    index=False, lineterminator="\r\n")
        self.truth["ask1"] = {k: v for k, v in sorted(truth.items())}
        return users, events

    # -------------------------------------------------------------- the group programme schedule (distractor)
    def groups(self, out):
        r = self.rng
        rows = []
        venues = ["Marshby Library community room", "St Botolph's Centre, Hollingby", "Fenwold Leisure Centre, studio 2",
                  "Online (video)", "Ashwold Road Health Centre"]
        d = date(2024, 4, 8)
        k = 0
        while d < W.GROUPS_END:
            for v in venues:
                if r.random() < 0.62:
                    k += 1
                    st = d + timedelta(days=int(r.integers(0, 4)))
                    places = int(r.choice([10, 12, 12, 14, 16]))
                    rows.append(dict(course_code="SMG-%02d%02d-%s" % (st.year % 100, st.month, chr(65 + k % 26)),
                                     venue=v, first_session=st.isoformat(), sessions=6,
                                     places=places, booked=int(min(places, r.integers(places - 6, places + 3))),
                                     facilitators=int(r.choice([2, 2, 2, 1]))))
            d += timedelta(weeks=int(r.choice([6, 7, 8])))
        pd.DataFrame(rows).to_csv(os.path.join(out, "stress_management_groups_schedule_2024-04_to_2025-08.csv"),
                                  index=False, lineterminator="\n")


def build(out, w=None):
    w = w or W.simulate()
    os.makedirs(out, exist_ok=True)
    pk = Pack(w)
    pk.referrals(out)
    pk.contacts(out)
    pk.directory(out)
    pk.bookings(out)
    pk.timesheets(out)
    pk.waitlist(out)
    pk.digital(out)
    pk.groups(out)
    return pk
