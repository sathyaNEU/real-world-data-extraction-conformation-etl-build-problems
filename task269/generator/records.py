"""The pack's record files as each system exports them: the hand hygiene audit application's moments, the patient
acuity system's patient-by-shift extract, the rostering system's actuals, the laboratory's positive blood cultures, the
patient administration system's admissions, ward transfers and midnight census, the store's hand rub issues, the
cleaning contractor's dispenser rounds, the patient experience survey and the staff influenza programme."""
import csv
import datetime as dt
import numpy as np

import common as K
import side as SD

MOMENT_NAME = {1: "1 Before touching a patient", 2: "2 Before a procedure",
               3: "3 After a procedure or body fluid exposure risk", 4: "4 After touching a patient",
               5: "5 After touching a patient's surroundings"}
APP_DEPT = {"AMU": "AMU Acute Medical Unit", "ESSU": "ESSU Emergency Short Stay Unit", "4A": "4A General Medicine",
            "7A": "7A Respiratory Medicine", "5A": "5A General Surgery", "6A": "6A Orthopaedics",
            "S1A": "S1A Orthopaedics (Surgical Block)", "6B": "6B Cardiology", "7B": "7B Renal Medicine",
            "8A": "8A Oncology and Haematology", "9A": "9A Rehabilitation", "9B": "9B Aged Care",
            "PCU": "Palliative Care Unit", "CCU": "Coronary Care Unit", "ICU": "Intensive Care Unit",
            "ED": "Emergency Department", "OT": "Operating Theatres and Recovery", "DSU": "Day Surgery Unit",
            "RDU": "Renal Dialysis Unit", "OPC": "Outpatient Clinics", "MI": "Medical Imaging"}
LAB_LOC = {u: "AVH-" + u for u in K.WARD + [K.MOVED[1]] + K.AREA}
COST_CENTRE = {"AMU": ("4012", "AMU ACUTE MEDICAL UNIT"), "ESSU": ("4013", "ESSU EMERG SHORT STAY"),
               "4A": ("4041", "WARD 4A GEN MEDICINE"), "7A": ("4071", "WARD 7A RESP MEDICINE"),
               "5A": ("4051", "WARD 5A GEN SURGERY"), "6A": ("4061", "WARD 6A ORTHOPAEDICS"),
               "6B": ("4062", "WARD 6B CARDIOLOGY"), "7B": ("4072", "WARD 7B RENAL MEDICINE"),
               "8A": ("4081", "WARD 8A ONCOLOGY HAEM"), "9A": ("4091", "WARD 9A REHABILITATION"),
               "9B": ("4092", "WARD 9B AGED CARE"), "PCU": ("4085", "PALLIATIVE CARE UNIT"),
               "CCU": ("4021", "CORONARY CARE UNIT"), "ICU": ("4022", "INTENSIVE CARE UNIT")}
HANDHELD = {"G": "PDA-0412", "2": "PDA-0415", "4": "PDA-0418", "5": "PDA-0421", "6": "PDA-0423", "7": "PDA-0426",
            "8": "PDA-0429", "9": "PDA-0433", "S1": "PDA-0440"}


def dmy(d):
    return d.strftime("%d/%m/%Y")


def dmy_hm(t):
    return t.strftime("%d/%m/%Y %H:%M")


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


def h2(x):
    return "%.2f" % x


class Records:
    def __init__(self, world, side, seed=K.SEED):
        self.w, self.s, self.seed = world, side, seed

    # ------------------------------------------------------------------ audits
    def audit_rows(self):
        head = ["session_id", "session_date", "session_start", "department", "auditor", "moment_seq", "moment",
                "hcw_category", "action"]
        rows = []
        for s in sorted(self.s.sessions, key=lambda x: x["sid"]):
            for j, (mo, h, act) in enumerate(s["moments"], 1):
                rows.append(["HH%06d" % s["sid"], dmy(s["date"]), s["start"].strftime("%H:%M"), APP_DEPT[s["unit"]],
                             s["auditor"], j, MOMENT_NAME[mo], h, act])
        return head, rows

    # ------------------------------------------------------------------ acuity
    def acuity_rows(self):
        rng = np.random.default_rng([269, self.seed, 60])
        enc, rows = {}, []
        head = ["ward", "shift_date", "shift", "bed", "encounter", "required_care_hours"]
        keys = sorted({k for (code, d, s), x in self.w.shifts.items() for k, b, h in x["patients"]})
        nums = rng.permutation(len(keys))
        for k, n in zip(keys, nums):
            enc[k] = "E%08d" % (30410000 + int(n) * 7 + int(rng.integers(0, 7)))
        for code in K.WARD:
            for d in K.DAYS:
                u = SD.ward_of(code, d)
                for s in ("AM", "PM"):
                    for k, b, h in sorted(self.w.shifts[(code, d, s)]["patients"], key=lambda p: p[1]):
                        bed = ("%s-%02d" % (u, b)) if b < 100 else ("%s-ESC%d" % (u, b - 99))
                        rows.append([u, d.isoformat(), s, bed, enc[k], "%.1f" % h])
        return head, rows

    # ------------------------------------------------------------------ roster
    def roster_rows(self):
        """each ward-shift's worked hours as the shifts of the nurses who worked them: 8-hour shifts and 4-hour
        half shifts, the ward's own nurses and the casual pool's under their employee numbers; supernumerary shifts beside
        them; night shifts of 10 hours"""
        rng = np.random.default_rng([269, self.seed, 61])
        head = ["roster_date", "ward", "shift_code", "staff_key", "staff_type", "designation", "shift_start",
                "shift_end", "worked_hours", "shift_category"]
        rows = []
        k = 0
        for code in K.WARD:
            nmed = np.median([self.w.shifts[(code, d, "AM")]["worked"] for d in K.DAYS]) / 8.0
            nday = max(sum(int(np.ceil(self.w.shifts[(code, d, s)]["worked"] / 8.0)) for s in ("AM", "PM"))
                       for d in K.DAYS) + max(2, int(round(nmed * 0.62))) + 2
            pool = []
            for _ in range(max(int(nmed * 7 / 4.2 * 1.6) + 4, int(nday * 1.3) + 4)):
                k += int(rng.integers(1, 12))
                des = rng.choice(["RN", "EN", "AIN"], p=[0.66, 0.20, 0.14])
                pool.append(("%06d" % (100000 + k * 3), str(des)))
            nd_n = max(2, int(round(nmed * 0.62)))
            for d in K.DAYS:
                u = SD.ward_of(code, d)
                used = set()
                for s in ("AM", "PM", "ND"):
                    if s == "ND":
                        n_full, half = nd_n, 0
                        surge = False
                    else:
                        x = self.w.shifts[(code, d, s)]
                        n_full, half = int(x["worked"] // 8), int(round((x["worked"] % 8) / 4))
                        surge = x["surge"]
                    for j in range(n_full + half):
                        is_half = j >= n_full
                        free = [p for p in pool if p[0] not in used]
                        p = free[int(rng.integers(0, len(free)))]
                        used.add(p[0])
                        key, typ, des = p[0], "Employee", p[1]
                        st, en, hrs = self._times(s, is_half, d)
                        rows.append([dmy(d), u, s, key, typ, des, st, en, h2(hrs), "Rostered"])
                    if s != "ND" and rng.random() < 0.08:
                        free = [p for p in pool if p[0] not in used]
                        p = free[int(rng.integers(0, len(free)))]
                        used.add(p[0])
                        cat = str(rng.choice(["Supernumerary - orientation", "Supernumerary - clinical education",
                                              "Supernumerary - student placement"], p=[0.5, 0.2, 0.3]))
                        key = p[0] if "student" not in cat else "S%05d" % int(rng.integers(10000, 99999))
                        des = "RN" if "student" not in cat else "Student"
                        st, en, hrs = self._times(s, False, d)
                        rows.append([dmy(d), u, s, key, "Employee" if des != "Student" else "Placement", des, st, en,
                                     h2(hrs), cat])
        return head, rows

    @staticmethod
    def _times(s, half, d):
        if s == "AM":
            return ("07:00", "11:00", 4.0) if half else ("07:00", "15:30", 8.0)
        if s == "PM":
            return ("17:30", "21:30", 4.0) if half else ("13:00", "21:30", 8.0)
        nxt = d + dt.timedelta(days=1)
        hrs = 10.0
        if nxt == dt.date(2025, 10, 5):
            hrs = 9.0       # clocks forward an hour on the morning of 5 October 2025
        if nxt == dt.date(2026, 4, 5):
            hrs = 11.0      # and back on the morning of 5 April 2026
        return "21:00", "07:30", hrs

    # ------------------------------------------------------------------ laboratory and patient administration
    def _mrn_at(self, p, t):
        """the record number a result carries: the retired number for cultures before the index merge"""
        if p["mrn"] in self.s.retired and t.date() < K.MPI_MERGE:
            return self.s.retired[p["mrn"]]
        return p["mrn"]

    def isolate_rows(self):
        rng = np.random.default_rng([269, self.seed, 62])
        head = ["lab_number", "mrn", "date_of_birth", "sex", "collected", "received", "location", "specimen",
                "organism"]
        rows = []
        for p in self.s.patients:
            for t, o, loc in p["cultures"]:
                when = t
                u = loc if loc in K.AREA else SD.ward_of(loc, when.date())
                rows.append([when, self._mrn_at(p, when), p["dob"], p["sex"], u, o])
        rows.sort(key=lambda r: (r[0], r[1]))
        out = []
        seqs = {}
        for when, mrn, dob, sex, u, o in rows:
            rec = when + dt.timedelta(minutes=int(rng.integers(25, 360)))
            yy = rec.strftime("%y")
            seqs[yy] = seqs.get(yy, 41000 + (0 if yy == "25" else 9000)) + int(rng.integers(1, 30))
            out.append(["%sB%06d" % (yy, seqs[yy]), mrn, dmy(dob), sex, dmy_hm(when), dmy_hm(rec), LAB_LOC[u],
                        "Blood culture", o])
        return head, out

    def admission_rows(self):
        rng = np.random.default_rng([269, self.seed, 63])
        head = ["admission_no", "mrn", "date_of_birth", "sex", "admitted", "admitting_ward", "separated",
                "separation_ward"]
        self.adm_no = {}
        recs = []
        for p in self.s.patients:
            if p["adm"] is None:
                continue
            for j, r in enumerate(p.get("pre", [])):
                recs.append((r["adm"], p["mrn"], (id(p), j), p, r))
            recs.append((p["adm"], p["mrn"], (id(p), "main"), p, p))
        recs.sort(key=lambda x: (x[0], x[1], str(x[2][1])))
        rows = []
        n = 2104000
        for adm, mrn, key, p, r in recs:
            n += int(rng.integers(5, 160))
            self.adm_no[key] = "IP%07d" % n
            last = r["moves"][-1][1] if r["moves"] else r["first"]
            rows.append([self.adm_no[key], p["mrn"], dmy(p["dob"]), p["sex"], dmy_hm(r["adm"]),
                         SD.ward_of(r["first"], r["adm"].date()), dmy_hm(r["dis"]), SD.ward_of(last, r["dis"].date())])
        return head, rows

    def transfer_rows(self):
        head = ["admission_no", "transfer_seq", "from_ward", "to_ward", "transferred"]
        rows = []
        for p in self.s.patients:
            if p["adm"] is None or not p["moves"]:
                continue
            cur = p["first"]
            for j, (t, w) in enumerate(p["moves"], 1):
                rows.append([self.adm_no[(id(p), "main")], j, SD.ward_of(cur, t.date()), SD.ward_of(w, t.date()),
                             dmy_hm(t)])
                cur = w
        rows.sort(key=lambda r: (dt.datetime.strptime(r[4], "%d/%m/%Y %H:%M"), r[0]))
        return head, rows

    def census_rows(self):
        head = ["census_date", "ward", "occupied_beds"]
        rows = []
        for d in K.DAYS:
            for code in K.WARD:
                rows.append([d.isoformat(), SD.ward_of(code, d), self.s.census[(code, d)]])
        return head, rows

    # ------------------------------------------------------------------ hand rub
    def issue_rows(self):
        rng = np.random.default_rng([269, self.seed, 64])
        head = ["issue_no", "issue_date", "transaction", "cost_centre", "cost_centre_name", "item_code",
                "item_description", "unit_of_issue", "quantity"]
        item = {c: (c, dsc, uoi) for c, dsc, uoi, _ in SD.HAND_RUB}
        # the contractor supplies its own refills and cartridges under its contract, so the store issues only the
        # wards' bottles
        lines = [(d, COST_CENTRE[code], it, q) for d, code, it, q in self.s.bottles]
        lines.sort(key=lambda x: (x[0], x[1][0], x[2]))
        rows = []
        n = 7700400
        for d, (cc, ccn), it, q in lines:
            n += int(rng.integers(1, 40))
            c, dsc, uoi = item[it]
            rows.append(["MI%07d" % n, dmy(d), "RETURN" if q < 0 else "ISSUE", cc, ccn, c, dsc, uoi, q])
        return head, rows

    def round_rows(self):
        """the contractor's round records as its handhelds sync them: the day's records at the evening's sync in the order
        they were scanned, and the records a handheld sent a second time at that day's sync"""
        rng = np.random.default_rng([269, self.seed, 65])
        head = ["record_id", "handheld", "job_no", "dispenser_id", "fitted", "product", "quantity", "cleaner"]
        cleaners = {fl: ["C%04d" % int(x) for x in rng.choice(np.arange(1000, 9999), size=6, replace=False)]
                    for fl in SD.FLOORS}
        cl_of = {}
        on_job = {}             # one cleaner does a terminal clean's whole job
        recs = []
        for i, (did, t, fl, kind) in enumerate(self.s.refills):
            if kind == "genuine":
                c = cleaners[fl][int(rng.integers(0, 6))]
                job = self.s.jobs.get((did, t))
                if job:
                    c = on_job.setdefault(job[0], c)
                cl_of[(did, t)] = c
            recs.append((did, t, fl, kind))
        out = []
        for did, t, fl, kind in recs:
            if kind == "genuine":
                c = cl_of[(did, t)]
                sync = (t.date(), 0)
                job = self.s.jobs.get((did, t))
            else:
                # the original record's cleaner and job, found from the record it repeats (same dispenser and time of
                # day, within the days the handheld held)
                held = [h for f, d0, h in SD.RESENDS if f == fl and d0 == t.date()][0]
                src = [x for x in cl_of if x[0] == did and x[1].time() == t.time()
                       and t.date() - dt.timedelta(days=held) <= x[1].date() < t.date()]
                c = cl_of[src[0]]
                sync = (t.date(), 1)
                job = self.s.jobs.get(src[0])
            out.append((sync, fl, t, did, c, kind, job))
        out.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
        rows = []
        n = 5531000
        for sync, fl, t, did, c, kind, job in out:
            n += 1
            rows.append([n, HANDHELD[fl], job[0] if job else "", did, t.strftime("%d/%m/%Y %H:%M"),
                         "FOAM 1L REFILL" if self.s.disp_type[did] == "Hand rub" else "SOAP 800ML CARTRIDGE",
                         job[1] if job else 1, c])
        return head, rows

    # ------------------------------------------------------------------ distractors
    def survey_rows(self):
        head = ["ward", "survey_month", "responses", "hand_hygiene_yes", "hand_hygiene_no", "hand_hygiene_dont_know"]
        return head, [[code, d.strftime("%b %Y"), n, y, no, dk] for code, d, n, y, no, dk in self.s.survey]

    def flu_rows(self):
        head = ["employee_no", "home_ward", "vaccinated_on"]
        return head, [[e, code, dmy(d) if d else ""] for e, code, d in self.s.flu]
