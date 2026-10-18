"""The fall 2026 term: the students enrolled at the census, the courses they registered for, the section schedule
(lectures with linked lab, shop and clinical sections; classes taught to two campuses over interactive video; stacked
courses sharing a room; online sections; sections cancelled before the census) and the registration records, with
drops before the census and withdrawals after it; and the program changes that took effect in spring 2027."""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import common as K
import population as PO
import world as W

TERM = K.TERM[K.FALL26]
CENSUS = TERM["census"]

# subject number: title, credits, linked component (a section the course's registration also takes, 0 credits)
COURSES = {
    "IDS 110": ("Inquiry Seminar", 3, None), "IDS 250": ("Integrative Capstone", 3, None),
    "BIO 101": ("Principles of Biology I", 4, "LAB"), "BIO 105": ("Environmental Science", 3, None),
    "BIO 110": ("Human Nutrition", 3, None), "BIO 121": ("Anatomy and Physiology I", 4, "LAB"),
    "BIO 122": ("Anatomy and Physiology II", 4, "LAB"), "BIO 210": ("Microbiology", 4, "LAB"),
    "BIO 230": ("Genetics", 3, None),
    "CHE 101": ("General Chemistry I", 4, "LAB"), "CHE 110": ("Chemistry for the Health Sciences", 4, "LAB"),
    "PHY 101": ("College Physics I", 4, "LAB"),
    "BUS 101": ("Introduction to Business", 3, None), "BUS 140": ("Principles of Management", 3, None),
    "BUS 210": ("Business Law", 3, None), "BUS 220": ("Principles of Marketing", 3, None),
    "ACC 101": ("Financial Accounting", 3, None), "ACC 102": ("Managerial Accounting", 3, None),
    "PSY 101": ("General Psychology", 3, None), "PSY 201": ("Lifespan Development", 3, None),
    "PSY 210": ("Abnormal Psychology", 3, None), "PSY 230": ("Research Methods in Psychology", 3, None),
    "PSY 240": ("Social Psychology", 3, None),
    "MDA 101": ("Introduction to Medical Assisting", 3, None), "MDA 140": ("Clinical Procedures I", 4, "LAB"),
    "MDA 150": ("Medical Office Procedures", 3, None), "MDA 160": ("Phlebotomy", 4, "LAB"),
    "MDA 240": ("Clinical Procedures II", 4, "LAB"), "MDA 290": ("Medical Assisting Externship Seminar", 3, None),
    "ECE 101": ("Foundations of Early Childhood Education", 3, None), "ECE 120": ("Child Growth and Development", 3, None),
    "ECE 210": ("Curriculum and Assessment", 3, None), "ECE 230": ("Early Childhood Practicum", 3, None),
    "ECE 240": ("Infant and Toddler Care", 3, None),
    "CRJ 101": ("Introduction to Criminal Justice", 3, None), "CRJ 120": ("Criminology", 3, None),
    "CRJ 210": ("Criminal Law", 3, None), "CRJ 220": ("Policing in America", 3, None),
    "CRJ 230": ("Corrections", 3, None),
    "HVR 101": ("Refrigeration Fundamentals", 4, "SHP"), "HVR 110": ("Electricity for HVAC-R", 4, "SHP"),
    "HVR 201": ("Heating Systems", 4, "SHP"), "HVR 210": ("Air Conditioning Systems", 4, "SHP"),
    "NUR 101": ("Fundamentals of Nursing", 6, "CLN"), "NUR 120": ("Pharmacology for Nurses", 2, None),
    "NUR 201": ("Medical-Surgical Nursing I", 7, "CLN"), "NUR 220": ("Maternal and Child Nursing", 4, "CLN"),
    "WLD 101": ("Welding Fundamentals", 4, "SHP"), "WLD 120": ("Gas Metal Arc Welding", 4, "SHP"),
    "ENG 101": ("English Composition I", 3, None), "ENG 102": ("English Composition II", 3, None),
    "MAT 095": ("Intermediate Algebra", 3, None), "MAT 110": ("College Algebra", 3, None),
    "MAT 120": ("Elementary Statistics", 3, None), "HIS 101": ("United States History to 1877", 3, None),
    "SOC 101": ("Introduction to Sociology", 3, None), "COM 101": ("Public Speaking", 3, None),
    "CIS 101": ("Computer Concepts and Applications", 3, None), "ART 101": ("Art Appreciation", 3, None),
    "PHI 101": ("Introduction to Philosophy", 3, None), "ECO 201": ("Principles of Macroeconomics", 3, None),
    "SPA 101": ("Elementary Spanish I", 3, None),
    "IDS 260": ("Community Engagement Seminar", 3, None), "BIO 240": ("Ecology", 3, None),
    "BUS 250": ("Small Business Management", 3, None), "ACC 210": ("Federal Income Tax", 3, None),
    "PSY 250": ("Psychology of Gender", 3, None), "MDA 250": ("Medical Coding and Billing", 3, None),
    "ECE 250": ("Children with Special Needs", 3, None), "CRJ 240": ("Juvenile Justice", 3, None),
    "HVR 220": ("Codes, Estimating and Service Management", 3, None),
    "NUR 230": ("Transition to Professional Nursing", 2, None),
}
ELECTIVES = {"IDS 260", "BIO 240", "BUS 250", "ACC 210", "PSY 250", "MDA 250", "ECE 250", "CRJ 240", "HVR 220",
             "NUR 230"}
# the course record's credit hours from spring 2027, when English Composition I and College Algebra took on a fourth
# hour of integrated support; fall 2026 sections ran at the earlier credit hours
REVISED = {"ENG 101": 4, "MAT 110": 4}
# accelerated offerings: a course in the first eight weeks and a course in the second, one instructor, one room and
# one evening or weekend time for both
ACCEL = {"GS": ("IDS 110", "IDS 250"), "BIO": ("BIO 105", "BIO 230"), "BUS": ("BUS 140", "BUS 220"),
         "PSY": ("PSY 201", "PSY 240"), "MA": ("MDA 150", "MDA 290"), "ECE": ("ECE 120", "ECE 210"),
         "CJ": ("CRJ 120", "CRJ 230"), "HVR": ("HVR 201", "HVR 210"), "NUR": ("NUR 120", "NUR 120")}
WEEKEND = [("F", "17:30", "20:15"), ("S", "08:30", "11:15"), ("S", "12:00", "14:45")]
WEEKEND_LAB = [("S", "08:30", "11:20"), ("S", "12:00", "14:50"), ("S", "15:00", "17:50")]
PART = {"1": (TERM["start"], TERM["end"]), "A": (TERM["start"], TERM["start"] + dt.timedelta(days=53)),
        "B": (TERM["start"] + dt.timedelta(days=56), TERM["end"])}
# a class taught over interactive video meets at the instructor's campus in the first week and for its final
# examination; the other campus's section meets from the second week to the last day of classes
RECEIVING = (TERM["start"] + dt.timedelta(days=7), TERM["end"] - dt.timedelta(days=7))
GENED = ({"ENG 101": 10, "ENG 102": 1, "MAT 095": 3, "MAT 110": 4, "MAT 120": 1.5, "HIS 101": 1.5, "SOC 101": 1.5,
          "COM 101": 1.5, "CIS 101": 2, "ART 101": 1, "SPA 101": .8, "PSY 101": 2.5, "BIO 105": 1},
         {"ENG 101": .6, "ENG 102": 6, "MAT 110": 2, "MAT 120": 3, "HIS 101": 2, "SOC 101": 2, "COM 101": 2.5,
          "CIS 101": 1.2, "ART 101": 1.5, "PHI 101": 1.5, "ECO 201": 1.5, "SPA 101": 1, "PSY 101": 1.5, "BIO 105": 1.2,
          "BIO 101": .8, "CHE 101": .4})
# the program's own and required courses, weights for the first year and later years
CURRIC = {
    "GS": ({"IDS 110": 12, "PSY 101": 2.5, "BIO 101": 1.6, "CHE 101": .6, "PHY 101": .3},
           {"IDS 250": 2.6, "IDS 260": .30, "PSY 101": 2, "PSY 201": 1, "BIO 101": 1.4, "CHE 101": .7, "BUS 101": 1}),
    "BIO": ({"BIO 101": 14, "CHE 101": 9, "MAT 110": 4}, {"BIO 210": 8, "BIO 230": 6, "BIO 240": 2.6, "CHE 101": 3,
                                                          "PHY 101": 4, "BIO 122": 2, "MAT 120": 3}),
    "BUS": ({"BUS 101": 12, "ACC 101": 9, "BUS 140": 3, "BIO 101": .8},
            {"ACC 102": 7, "BUS 210": 6, "BUS 220": 6, "BUS 140": 3, "BUS 250": 1.5, "ACC 210": 1.5, "ECO 201": 4,
             "CHE 101": .5, "BIO 101": .6}),
    "PSY": ({"PSY 101": 13, "PSY 201": 4, "SOC 101": 3, "BIO 101": .9},
            {"PSY 210": 7, "PSY 230": 6, "PSY 240": 6, "PSY 250": 1.2, "PSY 201": 3, "MAT 120": 3, "BIO 101": .7}),
    "MA": ({"MDA 101": 13, "MDA 140": 9, "BIO 121": 6, "MDA 150": 4}, {"MDA 240": 10, "MDA 290": 7, "MDA 250": 1.7,
                                                                      "MDA 150": 4, "BIO 122": 3, "PSY 101": 2}),
    "ECE": ({"ECE 101": 13, "ECE 120": 9, "PSY 101": 3, "BIO 105": 1.5},
            {"ECE 210": 8, "ECE 230": 7, "ECE 240": 6, "ECE 250": 1.3, "PSY 201": 3, "BIO 101": .6}),
    "CJ": ({"CRJ 101": 13, "CRJ 120": 7, "SOC 101": 3, "PSY 101": 2, "BIO 101": .7},
           {"CRJ 210": 7, "CRJ 220": 6, "CRJ 230": 6, "CRJ 240": 1.2, "PSY 210": 2, "BIO 101": .6}),
    "HVR": ({"HVR 101": 14, "HVR 110": 11, "MAT 110": 3, "PHY 101": .9},
            {"HVR 201": 10, "HVR 210": 9, "HVR 220": 2.6, "PHY 101": 1.4, "CIS 101": 2}),
    "NUR": ({"NUR 101": 15, "BIO 121": 12, "PSY 201": 5, "NUR 120": 6, "CHE 110": 3},
            {"NUR 201": 14, "NUR 220": 9, "NUR 230": 1.0, "BIO 210": 7, "BIO 122": 4}),
    "CERT.PHLB": ({"MDA 160": 15, "MDA 101": 8}, {"MDA 160": 10, "MDA 150": 6}),
    "CERT.HVTC": ({"HVR 101": 14, "HVR 110": 10}, {"HVR 201": 8, "HVR 110": 5}),
    "CERT.CDAP": ({"ECE 101": 12, "ECE 120": 8}, {"ECE 240": 6, "ECE 210": 5}),
    "CERT.WELD": ({"WLD 101": 15, "WLD 120": 6, "MAT 095": 2}, {"WLD 120": 12, "WLD 101": 3}),
    "CERT.ACCT": ({"ACC 101": 12, "BUS 101": 6, "CIS 101": 5}, {"ACC 102": 9, "CIS 101": 3}),
    "DE.HSDE": ({"ENG 101": 9, "MAT 110": 6, "PSY 101": 6, "HIS 101": 5, "SOC 101": 4, "BIO 105": 3, "SPA 101": 3,
                 "COM 101": 3}, {}),
    "ND.NDEG": ({"CIS 101": 3, "SPA 101": 3, "ART 101": 3, "PSY 101": 3, "ACC 101": 2, "WLD 101": 2, "ENG 101": 2},
                {}),
}
CAP = {None: 32, "LAB": 22, "SHP": 16, "CLN": 8}
TAUGHT = {"NUR": ("QNL", "TRV"), "WLD": ("QNL", "TRV"), "PHY": ("QNL", "TRV"), "CHE": ("QNL", "TRV", "HOL")}
ONLINE = {"ENG 101": .22, "ENG 102": .3, "MAT 120": .25, "HIS 101": .35, "SOC 101": .35, "PSY 101": .3,
          "PSY 201": .3, "CIS 101": .4, "ART 101": .4, "PHI 101": .35, "ECO 201": .3, "BUS 101": .3, "BUS 140": .3,
          "BUS 210": .35, "BUS 220": .3, "ACC 101": .2, "ACC 102": .25, "CRJ 101": .3, "CRJ 120": .3,
          "CRJ 210": .25, "ECE 101": .3, "ECE 120": .3, "ECE 210": .25, "PSY 210": .3, "PSY 240": .3,
          "IDS 110": .12, "BIO 105": .3, "BIO 110": .3, "MDA 150": .25, "NUR 120": .3, "SPA 101": .2,
          "BUS 250": .35, "ACC 210": .3, "PSY 250": .4, "ECE 250": .35, "CRJ 240": .35, "MDA 250": .4, "IDS 260": .3,
          "NUR 230": .3}
# lecture slots: (days, begin, end); labs and shops; clinical days
SLOTS = [("MW", "08:00", "09:15"), ("MW", "09:30", "10:45"), ("MW", "11:00", "12:15"), ("MW", "12:30", "13:45"),
         ("MW", "14:00", "15:15"), ("TR", "08:00", "09:15"), ("TR", "09:30", "10:45"), ("TR", "11:00", "12:15"),
         ("TR", "12:30", "13:45"), ("TR", "14:00", "15:15"), ("MWF", "09:00", "09:50"), ("MWF", "10:00", "10:50"),
         ("MWF", "11:00", "11:50"), ("MW", "17:30", "18:45"), ("TR", "17:30", "18:45"), ("MW", "19:00", "20:15"),
         ("TR", "19:00", "20:15"), ("W", "18:00", "20:40"), ("T", "18:00", "20:40"), ("R", "18:00", "20:40")]
LAB_SLOTS = [("M", "13:00", "15:50"), ("T", "13:00", "15:50"), ("W", "13:00", "15:50"), ("R", "13:00", "15:50"),
             ("M", "08:00", "10:50"), ("W", "08:00", "10:50"), ("F", "08:00", "10:50"), ("F", "12:00", "14:50"),
             ("T", "18:00", "20:50"), ("R", "18:00", "20:50"), ("M", "18:00", "20:50"), ("T", "08:00", "10:50"),
             ("R", "08:00", "10:50"), ("W", "18:00", "20:50"), ("F", "15:00", "17:50")]
CLN_SLOTS = [("TR", "06:45", "15:15"), ("WF", "06:45", "15:15"), ("MW", "06:45", "15:15")]
ROOMS = {
    "QNL": {"lec": ["QNL-A1%02d" % i for i in range(1, 19)] + ["QNL-A2%02d" % i for i in range(1, 15)] +
            ["QNL-L204V", "QNL-L206V"] + ["QNL-C1%02d" % i for i in range(10, 18)],
            "LAB": ["QNL-S201", "QNL-S203", "QNL-S205", "QNL-S207", "QNL-S209", "QNL-S211"], "SHP": ["QNL-T104", "QNL-T106", "QNL-T108"],
            "CLN": ["OFF CAMPUS"], "MDA": ["QNL-H112", "QNL-H114"]},
    "TRV": {"lec": ["TRV-1%02d" % i for i in range(1, 17)] + ["TRV-2%02d" % i for i in range(1, 11)] +
            ["TRV-118V", "TRV-122V"],
            "LAB": ["TRV-S110", "TRV-S112", "TRV-S114"], "SHP": ["TRV-T01", "TRV-T02", "TRV-T03"], "CLN": ["OFF CAMPUS"],
            "MDA": ["TRV-H08", "TRV-H10"]},
    "HOL": {"lec": ["HOL-B%02d" % i for i in range(1, 11)] + ["HOL-B%02d" % i for i in range(14, 24)] +
            ["HOL-B11V", "HOL-B12V"],
            "LAB": ["HOL-S03", "HOL-S05"], "SHP": ["HOL-T05", "HOL-T06"], "CLN": ["OFF CAMPUS"], "MDA": ["HOL-H02", "HOL-H04"]},
}
VIDEO = {"QNL": ["QNL-L204V", "QNL-L206V"], "TRV": ["TRV-118V", "TRV-122V"], "HOL": ["HOL-B11V", "HOL-B12V"]}


def rng_for(seed, *keys):
    return np.random.default_rng([seed, 26] + [int(k) for k in keys])


def overlaps(a, b):
    """Two meeting patterns share a day and a time."""
    if a is None or b is None:
        return False
    if not set(a[0]) & set(b[0]):
        return False
    return a[1] < b[2] and b[1] < a[2]


def enrolled(T, seed):
    """The students enrolled at the fall 2026 census, with their program at the census, load and campus."""
    out = []
    for i, a in enumerate(T["adm"]):
        if not PO.enrolled_fall26(a):
            continue
        rng = rng_for(seed, 1, i)
        prog = PO.program_at(a, K.FALL26)
        year2 = a["admit"] < "202620" and a["type"] not in ("D", "V")
        out.append(dict(sid=a["sid"], adm=a, prog=prog, pt=a["pt"], campus=a["campus"], year2=year2,
                        k=(int(rng.choice([1, 2, 2, 3, 3])) if a["pt"] else int(rng.choice([4, 4, 4, 5, 5])))))
    out.sort(key=lambda s: s["sid"])
    return out


def late_changes(T, students, seed):
    """Program changes that took effect in spring 2027 for students enrolled in fall 2026 whose admission stayed open
    into spring 2027."""
    for i, s in enumerate(students):
        a = s["adm"]
        rng = rng_for(seed, 2, i)
        if s["prog"] not in K.CODES:
            continue
        if a["reason"] is not None:
            continue
        if rng.random() < .034:
            opts = W.SWITCH[s["prog"]]
            new = opts[int(rng.integers(len(opts)))]
            if new != s["prog"]:
                a["switches"].append((K.LAST, new))


def choose_courses(s, rng):
    cur = CURRIC[s["prog"]][1 if s["year2"] and CURRIC[s["prog"]][1] else 0]
    pool = dict(GENED[1 if s["year2"] else 0]) if s["prog"] not in ("DE.HSDE", "ND.NDEG") else {}
    for c, w in cur.items():
        pool[c] = pool.get(c, 0) + w
    names = sorted(pool)
    w = np.array([pool[c] for c in names], float)
    k = min(s["k"], len(names))
    picks = list(rng.choice(len(names), size=k, replace=False, p=w / w.sum()))
    chosen = [names[i] for i in picks]
    # one lab science at most; nursing students do not take another lab science with nursing
    labs = [c for c in chosen if COURSES[c][2] == "LAB" and c.split()[0] in ("BIO", "CHE", "PHY")]
    for c in labs[1:]:
        chosen.remove(c)
    return sorted(chosen)


def build(T, seed=W.SEED):
    students = enrolled(T, seed)
    late_changes(T, students, seed)
    regs = {}
    for i, s in enumerate(students):
        rng = rng_for(seed, 3, i)
        s["courses"] = choose_courses(s, rng)
        for c in s["courses"]:
            online = rng.random() < ONLINE.get(c, 0) * (1.3 if s["pt"] else .8)
            where = "ONL" if online else (s["campus"] if s["campus"] == "QNL" or rng.random() < .82 else "QNL")
            if where != "ONL" and where not in TAUGHT.get(c.split()[0], K.CAMPUS):
                where = "QNL"
            regs.setdefault(c, []).append((s["sid"], where))
    sections, members = schedule(regs, seed)
    T["fall26"] = dict(students=students, sections=sections, members=members)
    registrations(T, seed)
    return T


# ---------------------------------------------------------------------------------------------- the schedule
class Book:
    """Room and instructor bookings, so no room or instructor is in two places at once."""

    def __init__(self):
        self.room, self.inst = {}, {}

    def free_room(self, room, slot):
        return room == "OFF CAMPUS" or not any(overlaps(slot, s) for s in self.room.get(room, []))

    def free_inst(self, inst, slot):
        return not any(overlaps(slot, s) for s in self.inst.get(inst, []))

    def take(self, room, inst, slot):
        if slot is None:
            return
        if room != "OFF CAMPUS":
            self.room.setdefault(room, []).append(slot)
        self.inst.setdefault(inst, []).append(slot)


def instructors(seed):
    """Each subject's instructors: employee numbers, a home campus, and how many sections each can carry."""
    rng = rng_for(seed, 9)
    subj = sorted({c.split()[0] for c in COURSES})
    pool = {}
    used = set()
    for s in subj:
        n = {"ENG": 22, "MAT": 18, "PSY": 13, "BIO": 16, "BUS": 9, "ACC": 6, "IDS": 9, "CRJ": 8, "ECE": 9, "MDA": 7,
             "HVR": 6, "NUR": 24, "CHE": 7, "PHY": 3, "WLD": 3, "SOC": 6, "HIS": 6, "COM": 5, "CIS": 6, "ART": 3,
             "PHI": 3, "ECO": 3, "SPA": 3}.get(s, 3)
        lst = []
        for _ in range(n):
            while True:
                e = "%06d" % int(rng.integers(410000, 589999))
                if e not in used:
                    break
            used.add(e)
            lst.append(dict(id=e, home=["QNL", "TRV", "HOL"][int(rng.choice(3, p=(.55, .27, .18)))],
                            load=int(rng.choice([2, 3, 5, 5, 5, 6])), n=0))
        pool[s] = lst
    return pool


def schedule(regs, seed):
    """Sections for every course from where its students study; labs, shops and clinical groups linked to their
    lectures; small advanced courses at two campuses taught together over interactive video; stacked courses."""
    rng = rng_for(seed, 4)
    pool = instructors(seed)
    book = Book()
    sections, members = [], {}
    taken = {}
    hired = set()
    pull = {}
    crn = [10011]

    def pick_inst(subject, campus, slot, prefer=None):
        cands = [p for p in pool[subject] if p["n"] < p["load"] and (slot is None or book.free_inst(p["id"], slot))]
        if prefer:
            cands = [p for p in cands if p["id"] == prefer] or cands
        home = [p for p in cands if p["home"] == campus]
        cands = home or cands
        if not cands:
            cands = [p for p in pool[subject] if slot is None or book.free_inst(p["id"], slot)]
        if not cands:
            # an adjunct hired for the term
            while True:
                e = "%06d" % int(rng.integers(600000, 689999))
                if e not in hired:
                    break
            hired.add(e)
            p = dict(id=e, home=campus if campus in K.CAMPUS else "QNL", load=int(rng.choice([2, 3])), n=0)
            pool[subject].append(p)
            cands = [p]
        cands.sort(key=lambda p: (p["n"], p["id"]))
        p = cands[0] if rng.random() < .7 else cands[int(rng.integers(len(cands)))]
        p["n"] += 1
        return p["id"]

    def place(course, campus, kind, inst_subject, slots, rooms, prefer_inst=None):
        order = list(rng.permutation(len(slots)))
        for k in order:
            slot = slots[k]
            rs = [r for r in rooms if book.free_room(r, slot)]
            if not rs:
                continue
            inst = pick_inst(inst_subject, campus, slot, prefer_inst)
            if not book.free_inst(inst, slot):
                [p for p in pool[inst_subject] if p["id"] == inst][0]["n"] -= 1
                continue
            room = rs[int(rng.integers(len(rs)))]
            return slot, room, inst
        raise RuntimeError("no room for %s at %s" % (course, campus))

    def new_section(course, campus, kind, slot, room, inst, link=None, sec=None):
        subj, num = course.split()
        s = dict(crn=str(crn[0]), subj=subj, num=num, course=course, title=COURSES[course][0], campus=campus,
                 kind=kind, slot=slot, room=room, inst=inst, link=link, status="A",
                 credits=COURSES[course][1] if kind in ("LEC", "ONL") else 0, cap=None, sec=sec, combined=None,
                 part="1")
        evening = slot is not None and slot[1] >= "17:00"
        pull[s["crn"]] = float(rng.uniform(.45, 1.55)) * (.62 if evening else 1.0)
        crn[0] += int(rng.integers(1, 4))
        sections.append(s)
        members[s["crn"]] = []
        book.take(room, inst, slot)
        return s

    def accelerate():
        """Each program's accelerated pair: students move from the course's sections at one campus into a
        first-eight-weeks section of one course and a second-eight-weeks section of the other, taught by one
        instructor in one room at one evening (or Friday evening or Saturday) time; a course with a linked section takes
        it in the same eight weeks, the two linked sections sharing their own room, time and instructor."""
        busy = defaultdict(list)
        for s in sections:
            if s["slot"]:
                for sid in members[s["crn"]]:
                    busy[sid].append((s["slot"], s["crn"]))
        evening = [x for x in SLOTS if x[1] >= "17:00"]
        for prog in K.CODES:
            pair = ACCEL[prog]
            subj = pair[0].split()[0]
            comp = COURSES[pair[0]][2]
            made = False
            tries = [(c, evening[int(k)], LAB_SLOTS) for c in ("QNL", "TRV", "HOL") if c in TAUGHT.get(subj, K.CAMPUS)
                     for k in rng.permutation(len(evening))]
            tries += [("QNL", WEEKEND[int(k)], WEEKEND_LAB) for k in rng.permutation(len(WEEKEND))]
            for campus, slot, labslots in tries:
                rooms = [r for r in ROOMS[campus]["MDA" if subj == "MDA" else "lec"] if book.free_room(r, slot)
                         and not r.endswith("V")]
                if not rooms or not any(book.free_inst(p["id"], slot) for p in pool[subj]):
                    continue
                lab = labroom = None
                if comp:
                    opts = [x for x in labslots if (x[1] >= "17:00" or x[0] == "S") and not overlaps(x, slot)]
                    opts = [x for x in opts if any(book.free_room(r, x) for r in ROOMS[campus][comp])]
                    if not opts:
                        continue
                    lab = opts[int(rng.integers(len(opts)))]
                    labroom = [r for r in ROOMS[campus][comp] if book.free_room(r, lab)][0]
                want = {"A": int(rng.integers(5, 10)), "B": int(rng.integers(6, 13))}
                chosen = {}
                taken_now = set()
                for half, course in zip("AB", pair):
                    src = [s for s in sections if s["course"] == course and s["campus"] == campus and s["kind"] == "LEC"
                           and not s["combined"] and s["part"] == "1" and s["status"] == "A"]
                    cands = []
                    for s in src:
                        links = {l["crn"] for l in sections if l["link"] == s["crn"]}
                        for sid in sorted(members[s["crn"]]):
                            if sid in taken_now:
                                continue
                            mine = [b for b, crn in busy[sid] if crn != s["crn"] and crn not in links]
                            if any(overlaps(slot, b) for b in mine) or (lab and any(overlaps(lab, b) for b in mine)):
                                continue
                            cands.append((sid, s))
                    if len(cands) < want[half]:
                        break
                    pick = sorted(rng.choice(len(cands), size=want[half], replace=False))
                    chosen[half] = [cands[int(i)] for i in pick]
                    taken_now.update(sid for sid, s in chosen[half])
                if len(chosen) < 2:
                    continue
                inst = pick_inst(subj, campus, slot)
                if not book.free_inst(inst, slot):
                    [p for p in pool[subj] if p["id"] == inst][0]["n"] -= 1
                    continue
                room = rooms[int(rng.integers(len(rooms)))]
                lab_inst = pick_inst(subj, campus, lab) if lab else None
                for half, course in zip("AB", pair):
                    new = new_section(course, campus, "LEC", slot, room, inst)
                    new["part"] = half
                    newlab = None
                    if lab:
                        newlab = new_section(course, campus, comp, lab, labroom, lab_inst, link=new["crn"])
                        newlab["part"] = half
                    for sid, s in chosen[half]:
                        members[s["crn"]].remove(sid)
                        members[new["crn"]].append(sid)
                        moved = {s["crn"]}
                        if newlab:
                            for l in sections:
                                if l["link"] == s["crn"] and sid in members[l["crn"]]:
                                    members[l["crn"]].remove(sid)
                                    members[newlab["crn"]].append(sid)
                                    moved.add(l["crn"])
                        busy[sid] = [b for b in busy[sid] if b[1] not in moved] + [(slot, new["crn"])] + (
                            [(lab, newlab["crn"])] if newlab else [])
                made = True
                break
            if not made:
                raise RuntimeError("no accelerated pair for %s" % prog)

    for course in sorted(regs):
        subj = course.split()[0]
        comp = COURSES[course][2]
        by = {}
        for sid, where in regs[course]:
            by.setdefault(where, []).append(sid)
        cap = CAP[None] if comp != "CLN" else 40
        small = {c: len(v) for c, v in by.items() if c != "ONL" and len(v) <= 11}
        advanced = int(course.split()[1]) >= 200 or course in ("MDA 150", "ACC 102", "BUS 140", "PSY 201")
        # two campuses with a small class each: one class over interactive video when the course is the program's own
        itv = None
        if course in ELECTIVES and comp is None:
            # an elective's two smallest campus sections are one class over interactive video
            sat = sorted((c for c in ("QNL", "TRV", "HOL") if by.get(c)), key=lambda c: (len(by[c]), c))[:2]
            if len(sat) == 2 and min(len(by[c]) for c in sat) < 10 and sum(len(by[c]) for c in sat) <= 26:
                itv = tuple(sorted(sat))
        elif advanced and comp is None and subj not in ("ENG", "MAT") and len(small) >= 2:
            pair = sorted(small, key=lambda c: (small[c], c))[:2]
            itv = tuple(sorted(pair))
        made = {}
        if itv:
            slot = None
            for k in rng.permutation(len(SLOTS)):
                cand = SLOTS[k]
                rooms = [[r for r in VIDEO[c] if book.free_room(r, cand)] for c in itv]
                if all(rooms):
                    inst = pick_inst(subj, itv[0], cand)
                    if book.free_inst(inst, cand):
                        slot = cand
                        break
                    pool_entry = [p for p in pool[subj] if p["id"] == inst][0]
                    pool_entry["n"] -= 1
            if slot:
                group = []
                for c, rs in zip(itv, rooms):
                    s = new_section(course, c, "LEC", slot, rs[0], inst)
                    if group:
                        book.inst[inst].pop()   # the same meeting, taught once
                    group.append(s)
                    made[c] = [s]
                for s in group:
                    s["combined"] = "ITV:" + group[0]["crn"]
                for s in group[1:]:
                    s["dates"] = RECEIVING
        for where in sorted(by):
            if where in made:
                continue
            n = len(by[where])
            if where == "ONL":
                k = max(1, math.ceil(n / 27)) if course not in ELECTIVES else (2 if n >= 9 else 1)
                inst = None
                if course in ELECTIVES:
                    # the subject's online instructor takes the elective's online sections too
                    have = sorted({x["inst"] for x in sections if x["subj"] == subj and x["kind"] == "ONL"})
                    if have:
                        inst = have[int(rng.integers(len(have)))]
                        [p for p in pool[subj] if p["id"] == inst][0]["n"] += 1
                inst = inst or pick_inst(subj, "QNL", None)
                lst = []
                for j in range(k):
                    if j and course not in ELECTIVES and rng.random() < .55:
                        inst = pick_inst(subj, "QNL", None)
                    lst.append(new_section(course, "ONL", "ONL", None, "ONLINE", inst))
                made[where] = lst
                continue
            k = max(1, math.ceil(n / (cap * .86)))
            lst = []
            for j in range(k):
                rooms = ROOMS[where]["MDA" if subj == "MDA" else "lec"]
                slot, room, inst = place(course, where, "LEC", subj, SLOTS, rooms)
                lst.append(new_section(course, where, "LEC", slot, room, inst))
            made[where] = lst
        # students into the lecture (or online) sections of their campus, around what they already have
        for where in sorted(by):
            secs = made[where]
            ids = sorted(by[where])
            lim = {x["crn"]: (15 if course in ELECTIVES and where == "ONL" else (cap if where != "ONL" else 30))
                   for x in secs}
            for k in rng.permutation(len(ids)):
                sid = ids[k]
                busy = taken.setdefault(sid, [])
                fits = [x for x in secs if not any(overlaps(x["slot"], b) for b in busy)] or secs
                w = np.array([pull[x["crn"]] * max(lim[x["crn"]] - len(members[x["crn"]]), .4) for x in fits])
                x = fits[int(rng.choice(len(fits), p=w / w.sum()))]
                members[x["crn"]].append(sid)
                if x["slot"]:
                    busy.append(x["slot"])
        # linked lab, shop and clinical sections
        if comp:
            for lec in [s for s in sections if s["course"] == course and s["kind"] in ("LEC", "ONL")]:
                stu = sorted(members[lec["crn"]])
                if not stu:
                    continue
                campus = lec["campus"] if lec["campus"] != "ONL" else "QNL"
                lcap = CAP[comp]
                k = max(1, math.ceil(len(stu) / (lcap * (.92 if comp != "CLN" else 1.0))))
                kind = {"LAB": "LAB", "SHP": "SHP", "CLN": "CLN"}[comp]
                slots = CLN_SLOTS if comp == "CLN" else LAB_SLOTS
                rooms = ROOMS[campus]["MDA" if subj == "MDA" else comp]
                labs = []
                for j in range(k):
                    slot, room, inst = place(course, campus, kind, subj, slots, rooms)
                    labs.append(new_section(course, campus, kind, slot, room, inst, link=lec["crn"]))
                for x in rng.permutation(len(stu)):
                    sid = stu[x]
                    busy = taken.setdefault(sid, [])
                    open_ = [l for l in labs if len(members[l["crn"]]) < lcap] or labs
                    fits = [l for l in open_ if not any(overlaps(l["slot"], b) for b in busy)] or open_
                    w = np.array([pull[l["crn"]] * max(lcap - len(members[l["crn"]]), .4) for l in fits])
                    l = fits[int(rng.choice(len(fits), p=w / w.sum()))]
                    members[l["crn"]].append(sid)
                    busy.append(l["slot"])
    stack(sections, members, book, rng)
    accelerate()
    # a linked section no student was placed in is not offered
    empty = {s["crn"] for s in sections if not members[s["crn"]]}
    sections[:] = [s for s in sections if s["crn"] not in empty]
    for c in empty:
        del members[c]
    number(sections, rng)
    for s in sections:
        s["cap"] = {"LEC": 32 if s["subj"] not in ("ENG", "MAT") else 26, "ONL": 30, "LAB": 24, "SHP": 16,
                    "CLN": 8}[s["kind"]]
        if s["combined"] and s["combined"].startswith("ITV"):
            s["cap"] = 16
        if s["part"] != "1" and s["kind"] == "LEC":
            s["cap"] = 24
    return sections, members


def stack(sections, members, book, rng):
    """Two small courses of one subject at one campus taught together in one room at one time by one instructor."""
    by = {}
    for s in sections:
        if (s["kind"] == "LEC" and not s["combined"] and s["campus"] in K.CAMPUS and len(members[s["crn"]]) <= 12
                and int(s["num"]) >= 200 and COURSES[s["course"]][2] is None):
            by.setdefault((s["subj"], s["campus"]), []).append(s)
    for key in sorted(by):
        lst = sorted(by[key], key=lambda s: (len(members[s["crn"]]), s["crn"]))
        single = [s for s in lst if sum(1 for x in sections if x["course"] == s["course"] and x["campus"] == s["campus"]
                                        and x["kind"] == "LEC") == 1]
        if len(single) < 2 or single[0]["course"] == single[1]["course"]:
            continue
        a, b = single[0], single[1]
        if len(members[a["crn"]]) + len(members[b["crn"]]) > 24:
            continue
        if b["room"] in book.room and b["slot"] in book.room[b["room"]]:
            book.room[b["room"]].remove(b["slot"])
        if b["inst"] in book.inst and b["slot"] in book.inst[b["inst"]]:
            book.inst[b["inst"]].remove(b["slot"])
        b["slot"], b["room"], b["inst"] = a["slot"], a["room"], a["inst"]
        a["combined"] = b["combined"] = "STK:" + a["crn"]


def number(sections, rng):
    """Section numbers as the schedule shows them: day sections 01 on, evening sections N01 on, online sections W01
    on, laboratory, shop and clinical sections L01, S01 and C01 on after their lectures."""
    by = {}
    for s in sections:
        by.setdefault(s["course"], []).append(s)
    camp = {"QNL": 0, "TRV": 1, "HOL": 2, "ONL": 3}
    for course, lst in by.items():
        day = [s for s in lst if s["kind"] == "LEC" and s["slot"] and s["slot"][1] < "17:00"]
        eve = [s for s in lst if s["kind"] == "LEC" and s["slot"] and s["slot"][1] >= "17:00"]
        onl = [s for s in lst if s["kind"] == "ONL"]
        oth = [s for s in lst if s["kind"] in ("LAB", "SHP", "CLN")]
        for i, s in enumerate(sorted(day, key=lambda s: (camp[s["campus"]], s["crn"]))):
            s["sec"] = "%02d" % (i + 1)
        for i, s in enumerate(sorted(eve, key=lambda s: (camp[s["campus"]], s["crn"]))):
            s["sec"] = "N%02d" % (i + 1)
        for i, s in enumerate(sorted(onl, key=lambda s: s["crn"])):
            s["sec"] = "W%02d" % (i + 1)
        letters = {"LAB": "L", "SHP": "S", "CLN": "C"}
        for i, s in enumerate(sorted(oth, key=lambda s: (s["link"], s["crn"]))):
            s["sec"] = "%s%02d" % (letters[s["kind"]], i + 1)


# ---------------------------------------------------------------------------------------------- registrations
def registrations(T, seed):
    """One row per student and section: registered at the census (RE, or RW when made on the web), withdrawn after
    the census (WC, a W grade), or dropped before it (DD, or DW on the web), the drop kept with its date. A student
    in a course with a linked section is registered on both."""
    F = T["fall26"]
    secs = {s["crn"]: s for s in F["sections"]}
    rows = []
    rng = rng_for(seed, 5)
    start = TERM["start"]
    for crn in sorted(F["members"]):
        s = secs[crn]
        for sid in sorted(F["members"][crn]):
            web = rng.random() < .71
            reg_on = start - dt.timedelta(days=int(rng.integers(2, 120)))
            status, when = ("RW" if web else "RE"), reg_on
            if s["kind"] in ("LEC", "ONL") and rng.random() < .083:
                status = "WC"
                hi = 80 if s["part"] != "A" else (PART["A"][1] - CENSUS).days - 10
                when = CENSUS + dt.timedelta(days=int(rng.integers(6, hi)))
            rows.append(dict(sid=sid, crn=crn, status=status, date=when))
    # withdrawals after the census carry to the linked section
    wc = {(r["sid"], secs[r["crn"]]["course"]) for r in rows if r["status"] == "WC"}
    wdate = {(r["sid"], secs[r["crn"]]["course"]): r["date"] for r in rows if r["status"] == "WC"}
    for r in rows:
        s = secs[r["crn"]]
        if s["kind"] in ("LAB", "SHP", "CLN") and (r["sid"], s["course"]) in wc:
            r["status"], r["date"] = "WC", wdate[(r["sid"], s["course"])]
    # added after the census by the registrar (a late add, never later withdrawn), the linked section with it; full-term
    # sections only, and never a section's every registration
    late = {}
    for r in rows:
        s = secs[r["crn"]]
        if s["kind"] in ("LEC", "ONL") and s["part"] == "1" and r["status"] in ("RE", "RW") and rng.random() < .015:
            late[(r["sid"], s["course"])] = CENSUS + dt.timedelta(days=int(rng.integers(1, 14)))
    at = defaultdict(int)
    for r in rows:
        if (r["sid"], secs[r["crn"]]["course"]) not in late:
            at[r["crn"]] += 1
    for k in sorted(late):
        crns = [r["crn"] for r in rows if (r["sid"], secs[r["crn"]]["course"]) == k]
        if any(at[c] == 0 for c in crns):
            del late[k]
            for c in crns:
                at[c] += 1
    for r in rows:
        k = (r["sid"], secs[r["crn"]]["course"])
        if k in late:
            r["status"], r["date"] = "RE", late[k]
    # drops before the census: a section tried and dropped, often for another section of the course
    drops = []
    by_course = {}
    for s in F["sections"]:
        if s["kind"] in ("LEC", "ONL"):
            by_course.setdefault(s["course"], []).append(s)
    for r in rows:
        s = secs[r["crn"]]
        if s["kind"] not in ("LEC", "ONL") or rng.random() > .072:
            continue
        others = [o for o in by_course[s["course"]] if o["crn"] != s["crn"] and o["status"] == "A"]
        if others:
            o = others[int(rng.integers(len(others)))]
            d = CENSUS - dt.timedelta(days=int(rng.integers(1, 30)))
            drops.append(dict(sid=r["sid"], crn=o["crn"], status="DW" if rng.random() < .6 else "DD", date=d))
    # sections cancelled before the census: registrations dropped on the cancellation date
    small = [s for s in F["sections"] if s["kind"] == "LEC" and s["campus"] != "ONL" and not s["combined"]
             and len(F["members"][s["crn"]]) >= 12]
    for k in sorted(rng.choice(len(small), size=7, replace=False)):
        s = small[int(k)]
        same = [x for x in F["sections"] if x["course"] == s["course"] and x["sec"] and x["sec"].isdigit()]
        ghost = dict(s, crn=str(int(max(x["crn"] for x in F["sections"])) + 3 + int(k)), status="X",
                     sec="%02d" % (max(int(x["sec"]) for x in same) + 1), combined=None)
        ghost["slot"], ghost["room"], ghost["inst"] = s["slot"], None, None
        F["sections"].append(ghost)
        F["members"][ghost["crn"]] = []
        when = CENSUS - dt.timedelta(days=int(rng.integers(8, 20)))
        for sid in sorted(F["members"][s["crn"]])[: int(rng.integers(3, 8))]:
            drops.append(dict(sid=sid, crn=ghost["crn"], status="DD", date=when))
    rows.extend(drops)
    F["rows"] = rows
