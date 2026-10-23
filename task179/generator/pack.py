"""task179 pack: the Registry's, Admissions' and Timetabling's extracts as the Planning Office receives them, in each
system's own layout. Layer 1 only: two student systems with their own identifiers, dates and codes joined by a
crosswalk, leave carried on the census, conjoint students on two attempts, credit-transfer entrants beside first-time
entrants, an admissions workbook whose columns drift by intake, a timetable at meeting grain. The Semester 1 classes
are exactly the classes each entrant sat in at the census."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import xlsx_writer as XW

ARC_FAC = {"ASS": "FASS", "BUS": "FBUS", "SCI": "FSCI", "ENG": "FENG", "HLT": "FHLT"}
RATING_ARC = {"S": "Satisfactory", "C": "Some concern", "R": "At risk", "": ""}
TITLES = {
    "UNIV101": "Academic Communication", "ARTS101": "Ideas and Society", "ARTS102": "Inquiry and Argument",
    "BUSN101": "Business Foundations", "ECON101": "Principles of Economics", "SCIE101": "Science in Practice",
    "MATH101": "Mathematics for the Sciences", "ENGR101": "Engineering Fundamentals", "MATH151": "Engineering Mathematics 1",
    "HLTH101": "Health and Society", "HLTH102": "The Human Body", "HIST110": "Making the Modern World",
    "ENGL110": "Reading Literature", "POLS110": "Power and Politics", "PHIL110": "Reasoning and Ethics",
    "SOCI110": "Introducing Sociology", "PSYC110": "Psychology: Mind and Behaviour", "FINE110": "Studio Foundations",
    "ACCT110": "Accounting Essentials", "MKTG110": "Marketing Principles", "MGMT110": "Organisations and People",
    "LAWS110": "Law and Society", "BIOL110": "Cells and Organisms", "CHEM110": "Chemical Principles",
    "PHYS110": "Physics in Everyday Life", "STAT110": "Statistics and Data", "BMED110": "Foundations of Biomedicine",
    "ENGR120": "Design and Making", "COMP110": "Programming 1", "NURS110": "Foundations of Nursing Practice",
    "HSCI110": "Health Science Foundations", "SPEX110": "Exercise and Performance",
}
WORDS = ["Methods", "Theory", "Practice", "Analysis", "Design", "Systems", "Studies", "Topics", "Research",
         "Applications", "Perspectives", "Principles", "Processes", "Contexts", "Modelling", "Policy"]
SUBJ = {"HIST": "History", "ENGL": "Literature", "POLS": "Politics", "PHIL": "Philosophy", "SOCI": "Sociology",
        "PSYC": "Psychology", "FINE": "Fine Arts", "LING": "Linguistics", "ANTH": "Anthropology", "MUSC": "Music",
        "ACCT": "Accounting", "MKTG": "Marketing", "MGMT": "Management", "ECON": "Economics", "FINC": "Finance",
        "LAWS": "Law", "INFS": "Information Systems", "BIOL": "Biology", "CHEM": "Chemistry", "PHYS": "Physics",
        "STAT": "Statistics", "MATH": "Mathematics", "GEOL": "Earth Science", "BMED": "Biomedical Science",
        "ENVS": "Environmental Science", "ENGR": "Engineering", "COMP": "Computing", "ELEC": "Electrical Engineering",
        "MECH": "Mechanical Engineering", "CIVL": "Civil Engineering", "SOFT": "Software Engineering",
        "NURS": "Nursing", "HSCI": "Health Science", "SPEX": "Exercise Science", "PUBH": "Public Health",
        "NUTR": "Nutrition"}
BUILDINGS = {"ASS": ["HUM", "LIB", "AR"], "BUS": ["BL", "MC"], "SCI": ["SC", "LS"], "ENG": ["EN", "TB"],
             "HLT": ["HS", "CL"]}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
STARTS = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]


class Pack:
    def __init__(self, w):
        self.w = w
        self.g = C.stream("pack")
        self._class_codes()
        self._timetable_rows()

    # ------------------------------------------------------------------ identifiers and class numbers
    def sid_of(self, s, year):
        return str(s["arc"]) if year >= 2026 else str(s["legacy"])

    def _class_codes(self):
        """SIRIUS class numbers (five digits, unique in a term) and ARC class codes. A class's number says nothing
        about the group it was allocated to: numbers run in the order Timetabling created the classes."""
        g = C.stream("classcodes")
        self.cnum = {}
        for y, c in self.w.cohorts.items():
            for p in sorted(c.nclasses):
                n = c.nclasses[p]
                perm = g.permutation(n) + 1
                for k in range(1, n + 1):
                    self.cnum[(y, p, k)] = int(perm[k - 1])
        self.base = {}
        for y in C.INTAKES:
            papers = sorted(self.w.cohorts[y].nclasses)
            start = 30000 + 1000 * (y - 2019) + int(g.integers(0, 200))
            off = start
            for p in papers:
                self.base[(y, p)] = off
                off += self.w.cohorts[y].nclasses[p] + int(g.integers(3, 12))

    def sirius_class(self, y, p, k):
        return self.base[(y, p)] + self.cnum[(y, p, k)]

    def arc_class(self, p, k):
        return "%s-26S1-%03d" % (p, self.cnum[(2026, p, k)])

    # ------------------------------------------------------------------ first-year class extracts
    def write_sirius_classes(self, path):
        rows = []
        for y in C.INTAKES[:-1]:
            c = self.w.cohorts[y]
            studs = [s for s in self.w.students if s["cohort"] == y]
            for s in studs:
                i = s["ci"]
                for (p, k) in c.classes[i]:
                    rows.append((s["legacy"], "%dS1" % y, p, self.sirius_class(y, p, k), "15.00", "E", y))
        rows.sort(key=lambda r: (r[6], r[3], r[0]))
        head = ["STUDENT_NO", "TERM", "PAPER", "CLASS_NBR", "POINTS", "CENSUS_STAT", "COHORT_YR"]
        return C.write_csv(path, head, rows)

    def write_arc_classes(self, path):
        c = self.w.cohorts[2026]
        rows = []
        for s in self.w.students:
            if s["cohort"] != 2026:
                continue
            for (p, k) in c.classes[s["ci"]]:
                rows.append((s["arc"], "2026-S1", p, self.arc_class(p, k), "15", "ENROLLED", "2026-10-01"))
        rows.sort(key=lambda r: (r[3], r[0]))
        head = ["arc_student_id", "study_period", "paper_code", "class_code", "credit_points", "enrolment_status",
                "census_date"]
        return C.write_csv(path, head, rows, crlf=False)

    # ------------------------------------------------------------------ census history
    def census_rows(self):
        out = []
        for s in self.w.students:
            for y, (st, yos) in sorted(s["rows"].items()):
                progs = [s.get("prog_before", s["prog"]) if y < 2026 else s["prog"]]
                if s["prog2"]:
                    progs.append(s["prog2"])
                att = []
                if y >= 2026 and s.get("stale_old"):
                    att.append((1, s["stale_old"]))
                    att.append((2, s["prog"]))
                else:
                    base = 2 if (y >= 2026 and "prog_before" in s) else 1
                    for j, pr in enumerate(progs):
                        att.append((base + j, pr))
                pt = s["pt"]
                for seq, pr in att:
                    load = (0.5 if pt else 1.0) / (len(att) if s["prog2"] else 1)
                    out.append((y, s, seq, pr, st, yos, pt, load))
        return out

    def write_census(self, path):
        rows = []
        for y, s, seq, pr, st, yos, pt, load in self.census_rows():
            fac = C.PROG[pr][2]
            if y < 2026:
                rows.append((C.dmy(C.census_date(y)), self.sid_of(s, y), "SIRIUS", seq, pr, fac, yos,
                             "PT" if pt else "FT", "%.3f" % load, st))
            else:
                rows.append((C.iso(C.census_date(y)), self.sid_of(s, y), "ARC", seq, pr, ARC_FAC[fac], yos,
                             "Part-time" if pt else "Full-time", "%.3f" % load,
                             {"EN": "Enrolled", "LV": "On leave"}[st]))
        rows.sort(key=lambda r: (r[0][-4:] if "/" in r[0] else r[0][:4], r[1], r[3]))
        head = ["CENSUS_DATE", "STUDENT_ID", "SOURCE", "ATTEMPT_SEQ", "PROGRAMME", "FACULTY", "YEAR_OF_STUDY",
                "ATTENDANCE", "EFTS", "STATUS"]
        return C.write_csv(path, head, rows)

    def write_crosswalk(self, path):
        rows = []
        for s in self.w.students:
            if s["legacy"] is not None and s["arc"] is not None:
                rows.append((s["legacy"], s["arc"], "2026-06-01"))
        rows.sort()
        return C.write_csv(path, ["SIRIUS_STUDENT_NO", "ARC_ID", "MIGRATED"], rows)

    # ------------------------------------------------------------------ admissions workbook
    def write_admissions(self, path):
        g = C.stream("admissions")
        sheets = []
        for y in C.INTAKES:
            rows = []
            c = self.w.cohorts[y]
            for s in self.w.students:
                if s["intake"] != y:
                    continue
                if s["basis"] == "FT1":
                    i = s["ci"]
                    acc = c.hall_name[i] if c.hall[i] else ("Family home" if g.random() < 0.6 else "Private")
                    lc = "Y" if c.lc[i] else ""
                    rows.append([self.sid_of(s, y), "First-time", c.prog[i], c.prog2[i] or "",
                                 C.PROG[c.prog[i]][2], "PT" if c.pt[i] else "FT", c.dob[i], c.sex[i], c.region[i],
                                 "Y" if c.fif[i] else "N", int(c.asc[i]), "Y" if c.hard[i] else "N", acc, lc,
                                 c.accepted[i]])
                elif s["basis"] == "TRC":
                    dob = dt.date(y - int(g.integers(19, 34)), 1, 1) + dt.timedelta(days=int(g.integers(0, 365)))
                    acc_d = dt.date(y - 1, 11, 1) + dt.timedelta(days=int(g.integers(0, 280)))
                    rows.append([self.sid_of(s, y), "Credit transfer", s.get("prog_before", s["prog"]), "",
                                 C.PROG[s.get("prog_before", s["prog"])][2], "PT" if s["pt"] else "FT", dob,
                                 g.choice(["F", "M"]), g.choice(["Corriemoor", "Westray", "Halden", "Overseas"]),
                                 "", "", "N", "Private", "", acc_d])
            order = g.permutation(len(rows))
            rows = [rows[j] for j in order]
            rows.sort(key=lambda r: r[14])
            score = "ASC Points" if y <= 2022 else "ASC Score"
            head = ["Student No" if y < 2026 else "Student ID", "Entry Basis", "Programme", "Conjoint With", "Faculty",
                    "Attendance", "Date of Birth", "Gender", "Home Region", "First in Family", score,
                    "Hardship Grant", "Accommodation", "Living-Learning Community", "Offer Accepted"]
            sheets.append(("%d intake" % y, head, rows))
        XW.write_workbook(path, sheets, widths=[12, 15, 11, 13, 8, 10, 13, 7, 13, 9, 10, 9, 15, 10, 13])
        return sum(len(s[2]) for s in sheets)

    # ------------------------------------------------------------------ week-6 progress check
    def write_progress(self, path):
        rows = []
        for y in C.INTAKES:
            c = self.w.cohorts[y]
            for s in self.w.students:
                if s["cohort"] != y:
                    continue
                i = s["ci"]
                for (p, k), r in zip(c.classes[i], c.ratings[i]):
                    if y < 2026:
                        rows.append((y, "W6", self.sid_of(s, y), p, self.sirius_class(y, p, k), r))
                    else:
                        rows.append((y, "Week 6", self.sid_of(s, y), p, self.arc_class(p, k), RATING_ARC[r]))
        rows.sort(key=lambda r: (r[0], str(r[4]), r[2]))
        return C.write_csv(path, ["YEAR", "CHECK", "STUDENT", "PAPER", "CLASS", "RATING"], rows)

    # ------------------------------------------------------------------ programme catalogue and transfers
    def write_catalogue(self, path):
        rows = []
        for code, title, fac, yrs, _, _ in C.PROGRAMMES:
            rows.append(("Programme", code, title, ARC_FAC[fac], yrs, ""))
        for a, b in C.CONJOINTS:
            rows.append(("Conjoint", "%s/%s" % (a, b), "%s and %s" % (C.PROG[a][1], C.PROG[b][1]),
                         ARC_FAC[C.PROG[a][2]], max(C.PROG[a][3], C.PROG[b][3]) + 1,
                         "%s;%s" % (a, b)))
        return C.write_csv(path, ["TYPE", "CODE", "TITLE", "OWNING_FACULTY", "YEARS_FT", "COMPONENTS"], rows)

    def write_transfers(self, path):
        rows = []
        g = C.stream("transfer_rows")
        for t in self.w.transfers:
            s = t["s"]
            d = t["approved"]
            sid = str(s["arc"]) if d >= C.CUTOVER else str(s["legacy"])
            rows.append((sid, t["old"], t["new"], C.iso(d), "2026 S1" if d.month >= 6 or d.year == 2026 else "2026 S1",
                         g.choice(["Student request", "Student request", "Student request", "Academic advice"])))
        return C.write_csv(path, ["STUDENT", "FROM_PROGRAMME", "TO_PROGRAMME", "APPROVED", "EFFECTIVE", "REASON"], rows)

    # ------------------------------------------------------------------ Semester 1 2026 timetable
    def _timetable_rows(self):
        g = C.stream("tt_rows")
        from faker import Faker
        fk = Faker("en_IE")
        fk.seed_instance(179)
        fk2 = Faker("en_GB")
        fk2.seed_instance(1790)
        staff = {f: [] for f in C.FAC_CODES}
        seen = set()
        for f in C.FAC_CODES:
            while len(staff[f]) < 140:
                nm = (fk if g.random() < 0.6 else fk2).name()
                nm = nm.replace("Dr. ", "").replace("Mr. ", "").replace("Mrs. ", "").replace("Ms. ", "").replace("Prof. ", "")
                if nm in seen or len(nm.split()) != 2:
                    continue
                seen.add(nm)
                staff[f].append(nm)
        rooms = {}
        for f in C.FAC_CODES:
            rs = []
            for b in BUILDINGS[f]:
                for fl in range(1, 4):
                    for n in range(1, 9):
                        cap = int(g.choice([32, 32, 36, 40, 48, 60, 80, 120, 180, 240]))
                        rs.append(("%s %d.%02d" % (b, fl, n + 10 * int(g.integers(0, 2))), cap))
            rooms[f] = sorted(set(rs))
        busy = set()                    # (room, day, start, weeks-half)
        tbusy = set()                   # (teacher, day, start)
        self.tt = []                    # one dict per meeting row
        classes = self.w.classes
        paired = {}
        for a, b in self.w.pairs:
            paired[(b["paper"], b["k"])] = (a["paper"], a["k"])
        code_of = {}
        for x in classes:
            if x["level"] == 100:
                code_of[(x["paper"], x["k"])] = self.arc_class(x["paper"], x["k"])
            else:
                code_of[(x["paper"], x["k"])] = "%s-26S1-%03d" % (x["paper"], x["k"])
        meetings = {}

        def place(x, nmeet, teacher, weeks="1-12"):
            f = x["fac"]
            need = x["enrolled"] if x.get("pair") is None else x["enrolled"] + self._mate(x)["enrolled"]
            cand = [r for r in rooms[f] if r[1] >= need] or [max(rooms[f], key=lambda r: r[1])]
            out = []
            days = list(g.permutation(DAYS))
            for d in days:
                if len(out) == nmeet:
                    break
                for _ in range(40):
                    st = STARTS[int(g.integers(len(STARTS)))]
                    r = cand[int(g.integers(len(cand)))]
                    if (r[0], d, st) in busy or (teacher, d, st) in tbusy:
                        continue
                    busy.add((r[0], d, st))
                    tbusy.add((teacher, d, st))
                    out.append((d, st, r))
                    break
            return out
        self._by_key = {(x["paper"], x["k"]): x for x in classes}
        for x in sorted(classes, key=lambda x: (x["fac"], x["level"], x["paper"], x["k"])):
            key = (x["paper"], x["k"])
            if key in paired:
                continue                      # placed with its 300-level mate
            teacher = staff[x["fac"]][int(g.integers(len(staff[x["fac"]])))]
            nmeet = 2 if x["level"] == 100 else int(g.choice([1, 2, 2]))
            mt = place(x, nmeet, teacher)
            meetings[key] = (teacher, mt)
            if x.get("pair") is not None:
                # the honours paper's own coordinator is its teacher of record
                t2 = staff[x["fac"]][int(g.integers(len(staff[x["fac"]])))]
                while t2 == teacher:
                    t2 = staff[x["fac"]][int(g.integers(len(staff[x["fac"]])))]
                meetings[x["pair"]] = (t2, mt)
        # rows
        g2 = C.stream("tt_hazards")
        cancel = set()
        for x in classes:
            if x["level"] >= 200 and x["enrolled"] <= 8 and x.get("pair") is None and g2.random() < 0.35:
                cancel.add((x["paper"], x["k"]))
        for x in sorted(classes, key=lambda x: (x["paper"], x["k"])):
            key = (x["paper"], x["k"])
            teacher, mt = meetings[key]
            title = TITLES.get(x["paper"]) or "%s %s" % (SUBJ[x["paper"][:4]], WORDS[(int(x["paper"][4:]) * 7) % len(WORDS)])
            status = "Cancelled" if key in cancel else "Active"
            enrolled = 0 if key in cancel else x["enrolled"]
            if key in cancel:
                x["cancelled"] = True
            team = x["level"] >= 200 and x.get("pair") is None and g2.random() < 0.05 and key not in cancel
            moved = x["level"] >= 200 and x.get("pair") is None and g2.random() < 0.04 and key not in cancel
            others = [rr for rr in rooms[x["fac"]] if rr[1] >= x["enrolled"]]
            moved = moved and len(others) > 1
            for (d, st, r) in mt:
                end = "%02d:00" % (int(st[:2]) + (2 if x["level"] >= 200 and len(mt) == 1 else 1))
                base = dict(code=code_of[key], paper=x["paper"], title=title, fac=ARC_FAC[x["fac"]],
                            level=x["level"], day=d, start=st, end=end, room=r[0], cap=r[1], teacher=teacher,
                            enrolled=enrolled, status=status, weeks="1-12")
                if moved:
                    other = [rr for rr in rooms[x["fac"]] if rr[1] >= x["enrolled"] and rr[0] != r[0]]
                    r2 = other[int(g2.integers(len(other)))]
                    self.tt.append(dict(base, weeks="1-4"))
                    self.tt.append(dict(base, weeks="5-12", room=r2[0], cap=r2[1]))
                else:
                    self.tt.append(base)
                if team:
                    t2 = staff[x["fac"]][int(g2.integers(len(staff[x["fac"]])))]
                    self.tt.append(dict(self.tt[-1], teacher=t2))
        # half-semester papers sharing a slot, a teacher and a room (weeks 1-6 and 7-12): two groups
        self.halves = []
        for f in C.FAC_CODES:
            for j in range(3):
                stem = [k for k, v in SUBJ.items() if k in [p[:4] for p in self._papers_of(f)]][j % 3]
                teacher = staff[f][int(g2.integers(len(staff[f])))]
                pa, pb = "%s2%02d" % (stem, 50 + 2 * j), "%s2%02d" % (stem, 51 + 2 * j)
                if any(r["paper"] in (pa, pb) for r in self.tt):
                    continue
                r = [rr for rr in rooms[f] if rr[1] >= 40][int(g2.integers(4))]
                while True:
                    d, st = DAYS[int(g2.integers(5))], STARTS[int(g2.integers(10))]
                    if (r[0], d, st) not in busy and (teacher, d, st) not in tbusy:
                        busy.add((r[0], d, st))
                        tbusy.add((teacher, d, st))
                        break
                for pp, wk in ((pa, "1-6"), (pb, "7-12")):
                    n = int(g2.integers(16, 31))
                    self.tt.append(dict(code="%s-26S1-001" % pp, paper=pp, title="%s %s" % (SUBJ[stem], WORDS[(j * 5 + len(wk)) % len(WORDS)]),
                                        fac=ARC_FAC[f], level=200, day=d, start=st, end="%02d:00" % (int(st[:2]) + 2),
                                        room=r[0], cap=r[1], teacher=teacher, enrolled=n, status="Active", weeks=wk))
                    self.halves.append(dict(paper=pp, k=1, fac=f, level=200, enrolled=n, pair=None))
        self.tt.sort(key=lambda r: (r["fac"], r["paper"], r["code"], DAYS.index(r["day"]), r["start"], r["weeks"]))

    def _mate(self, x):
        return self._by_key[x["pair"]]

    def _papers_of(self, f):
        return sorted(set(x["paper"] for x in self.w.classes if x["fac"] == f and x["level"] >= 200))

    def write_timetable(self, path):
        head = ["Class Code", "Paper", "Paper Title", "Owning Faculty", "Level", "Day", "Start", "End", "Teaching Weeks",
                "Room", "Room Capacity", "Teacher", "Enrolled at Census", "Class Status"]
        rows = [[r["code"], r["paper"], r["title"], r["fac"], r["level"], r["day"], r["start"], r["end"], r["weeks"],
                 r["room"], r["cap"], r["teacher"], r["enrolled"], r["status"]] for r in self.tt]
        XW.write_workbook(path, [("S1 2026 classes", head, rows)],
                          widths=[20, 9, 34, 9, 6, 6, 7, 7, 9, 10, 9, 22, 11, 10])
        return len(rows)

    # ------------------------------------------------------------------ distractors
    def write_halls(self, path):
        g = C.stream("halls")
        rows = []
        beds = {"Ferrier Hall": 420, "Ashby House": 310, "Linton Court": 520, "Stanmore Hall": 380, "Wexcombe Hall": 290}
        for y in C.INTAKES:
            start = dt.date(y, 8, 24)
            for wk in range(1, 41):
                d = start + dt.timedelta(days=7 * (wk - 1))
                if d > dt.date(2026, 10, 12):
                    break
                for h, b in beds.items():
                    occ = b * (0.97 - 0.004 * max(0, wk - 14) - (0.05 if 15 <= wk <= 19 else 0)) + g.normal(0, 4)
                    rows.append((y, wk, C.iso(d), h, b, int(min(b, round(occ)))))
        return C.write_csv(path, ["ACADEMIC_YEAR", "WEEK", "WEEK_BEGINNING", "HALL", "BEDS", "OCCUPIED"], rows)

    def write_school_leavers(self, path):
        g = C.stream("nsl")
        regs = ["Corriemoor", "Westray", "Halden", "Northmoor", "Kelso Bay", "Upper Tarn", "Ruthven"]
        base = {"Corriemoor": 9800, "Westray": 4100, "Halden": 3600, "Northmoor": 3300, "Kelso Bay": 2700,
                "Upper Tarn": 2400, "Ruthven": 2100}
        rows = []
        for y in range(2019, 2027):
            for r in regs:
                n = int(base[r] * (1 + 0.006 * (y - 2019)) + g.normal(0, 60))
                ue = int(n * (0.47 + 0.004 * (y - 2019) + g.normal(0, 0.01)))
                rows.append((y, r, n, ue, int(ue * (0.52 + g.normal(0, 0.02)))))
        return C.write_csv(path, ["YEAR", "REGION", "SCHOOL_LEAVERS", "WITH_UNIVERSITY_ENTRANCE",
                                  "ENROLLED_IN_DEGREE_NEXT_YEAR"], rows)
