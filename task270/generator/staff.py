"""task270 staff world (Ask A): the clinical staff of each community team and of the Complex Emotional Needs Service,
their assignments as the staff record holds them at 4 January 2027, and their training on the learning system since
it opened in April 2022.

PTD-114 was the trust's four-day DBT skills group facilitation course until 31 March 2025. When the learning team
rebuilt its catalogue from 1 April 2025, the four-day course took PTD-301 and PTD-114 passed to a one-day DBT skills
refresher; the learning records keep each completion under the code it was recorded with, and the 2026 catalogue
carries only the current titles."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font

import common as K

ORG = {c: n + " CMHT" for c, n in K.TEAMS + K.OLD_TEAMS}
ORG["CEN"] = "Complex Emotional Needs Service"
# per current team: four-day trained clinicians in post on 1 April 2027 at 0.4 WTE or more, by how they trained
# (PTD-114 before April 2025, PTD-301, external four-day), and refresher-only clinicians
PLAN = {"BW-CM02": (3, 2, 1, 1), "BW-CM05": (2, 2, 1, 1), "BW-CM11": (1, 2, 0, 1), "BW-CM31": (2, 1, 1, 0),
        "BW-CM17": (1, 1, 0, 1), "BW-CM03": (2, 0, 0, 1), "BW-CM08": (1, 0, 0, 1), "BW-CM20": (1, 2, 0, 0),
        "BW-CM09": (1, 0, 0, 1), "BW-CM22": (1, 1, 0, 1), "BW-CM12": (1, 0, 1, 1)}
POSITIONS = [("Community Mental Health Nurse", "Nursing and Midwifery Registered", 0.33),
             ("Senior Mental Health Practitioner", "Nursing and Midwifery Registered", 0.10),
             ("Clinical Psychologist", "Add Prof Scientific and Technic", 0.10),
             ("Psychological Therapist", "Add Prof Scientific and Technic", 0.08),
             ("Occupational Therapist", "Allied Health Professionals", 0.12),
             ("Social Worker", "Add Prof Scientific and Technic", 0.11),
             ("Support Time Recovery Worker", "Additional Clinical Services", 0.11),
             ("Peer Support Worker", "Additional Clinical Services", 0.05)]
TRAINABLE = ("Community Mental Health Nurse", "Senior Mental Health Practitioner", "Clinical Psychologist",
             "Psychological Therapist", "Occupational Therapist", "Social Worker")
MANDATORY = [("MAN-101", 3), ("MAN-104", 1), ("MAN-110", 1), ("MAN-122", 3), ("MAN-131", 2)]
CLINICAL = ["PTD-205", "PTD-118", "PTD-226", "PTD-232", "EXT-0390"]
CATALOGUE = [
    ("MAN-101", "Safeguarding adults and children, level 3", 1, "2019-04-01", "Current"),
    ("MAN-104", "Data security awareness", 0.5, "2019-04-01", "Current"),
    ("MAN-110", "Basic life support (adults)", 0.5, "2019-04-01", "Current"),
    ("MAN-122", "Prevent: radicalisation awareness", 0.5, "2020-09-01", "Current"),
    ("MAN-131", "Clinical risk assessment and safety planning", 1, "2021-02-01", "Current"),
    ("PTD-114", "DBT skills refresher", 1, "2025-04-01", "Current"),
    ("PTD-118", "Mentalisation-based treatment: awareness", 1, "2020-06-01", "Current"),
    ("PTD-205", "Motivational interviewing", 2, "2019-04-01", "Current"),
    ("PTD-226", "Structured clinical management", 3, "2021-10-01", "Current"),
    ("PTD-232", "Trauma-informed care in community teams", 1, "2023-05-01", "Current"),
    ("PTD-301", "DBT skills group facilitation", 4, "2025-04-01", "Current"),
    ("EXT-0390", "External course: introduction to DBT", 1, "2019-04-01", "Current"),
    ("EXT-0412", "External course: DBT skills training", 4, "2019-04-01", "Current"),
]
OLD_RUNS = [dt.date(2022, 6, 16), dt.date(2022, 11, 10), dt.date(2023, 3, 9), dt.date(2023, 6, 22),
            dt.date(2023, 10, 19), dt.date(2024, 2, 8), dt.date(2024, 5, 23), dt.date(2024, 10, 3),
            dt.date(2025, 2, 27)]
NEW_RUNS = [dt.date(2025, 6, 12), dt.date(2025, 10, 9), dt.date(2026, 2, 26), dt.date(2026, 6, 18),
            dt.date(2026, 10, 15)]
REFRESHERS = [dt.date(2025, 5, 14), dt.date(2025, 9, 17), dt.date(2025, 11, 26), dt.date(2026, 3, 18),
              dt.date(2026, 5, 13), dt.date(2026, 9, 9), dt.date(2026, 11, 25)]


class Person:
    pass


def emp_number(r, used):
    while True:
        n = "%08d" % int(r.integers(20_000_000, 29_999_999))
        if n not in used:
            used.add(n)
            return n


def build():
    r = K.rng("staff")
    used = set()
    people = []

    def new(team, position=None, group=None, wte=None, start=None):
        p = Person()
        p.emp = emp_number(r, used)
        p.prev = ""
        if position is None:
            u = r.random()
            acc = 0
            for pos, grp, w in POSITIONS:
                acc += w / sum(x[2] for x in POSITIONS)
                if u < acc:
                    position, group = pos, grp
                    break
        p.position, p.group = position, group
        p.team = team
        p.wte = wte if wte is not None else float(r.choice([1.0, 1.0, 1.0, 1.0, 0.8, 0.8, 0.6, 0.53, 0.67, 0.92]))
        p.start = start or (dt.date(2026, 1, 1) - dt.timedelta(days=int(r.integers(200, 5200))))
        p.leaving = None
        p.extra = []                 # further assignments (team code, wte, start, end)
        p.train = []                 # (code, date, under employee number)
        p.kind = "plain"
        people.append(p)
        return p

    for team, _n in K.TEAMS:
        rt = K.rng("staff team", team)
        old114, new301, ext, refresh = PLAN[team]
        trained = []
        for kind, k in (("old114", old114), ("new301", new301), ("ext", ext)):
            for _ in range(k):
                pos = TRAINABLE[int(rt.integers(0, len(TRAINABLE)))]
                grp = [g for q, g, _w in POSITIONS if q == pos][0]
                p = new(team, pos, grp, wte=float(rt.choice([1.0, 1.0, 0.8, 0.67, 0.6, 0.53, 0.92])))
                p.kind = kind
                trained.append(p)
        for _ in range(refresh):
            pos = TRAINABLE[int(rt.integers(0, len(TRAINABLE)))]
            grp = [g for q, g, _w in POSITIONS if q == pos][0]
            p = new(team, pos, grp)
            p.kind = "refresher_only"
        for _ in range(int(rt.integers(12, 19))):
            new(team)
        new(team, "Team Manager", "Nursing and Midwifery Registered", 1.0)
        for _ in range(2):
            new(team, "Administrative Officer", "Administrative and Clerical", float(rt.choice([1.0, 0.6])))
    # the Complex Emotional Needs Service: DBT therapists, some holding a sessional assignment in a team
    for i in range(14):
        pos = ["Clinical Psychologist", "Psychological Therapist", "Senior Mental Health Practitioner"][i % 3]
        grp = [g for q, g, _w in POSITIONS if q == pos][0]
        p = new("CEN", pos, grp, wte=1.0)
        p.kind = "hub_trained" if i < 9 else "plain"
    hub_spokes = {"BW-CM02": 0.2, "BW-CM05": 0.2, "BW-CM11": 0.3, "BW-CM12": 0.2, "BW-CM22": 0.2}
    hubbers = [p for p in people if p.team == "CEN" and p.kind == "hub_trained"]
    for (team, w), p in zip(hub_spokes.items(), hubbers):
        p.wte = round(1.0 - w, 1)
        p.extra.append((team, w, dt.date(2025, 9, 1) + dt.timedelta(days=int(r.integers(0, 200))), None))
    # trained clinicians who were re-employed under a new number, their training under the old one
    for team in ("BW-CM09", "BW-CM22", "BW-CM17"):
        cands = [p for p in people if p.team == team and p.kind == "old114"]
        p = cands[0]
        p.prev = emp_number(r, used)
        p.start = dt.date(2025, 3, 3) + dt.timedelta(days=int(r.integers(0, 300)))
        p.old_end = dt.date(2024, 6, 28) + dt.timedelta(days=int(r.integers(0, 120)))
        p.kind = "old114_rehired"
    # leaving dates: trained clinicians under notice
    for team, when in (("BW-CM20", dt.date(2027, 6, 30)), ("BW-CM05", dt.date(2027, 2, 28)),
                       ("BW-CM03", dt.date(2027, 10, 31))):
        extra_p = new(team, "Community Mental Health Nurse", "Nursing and Midwifery Registered", 1.0)
        extra_p.kind = "leaver_old114"
        extra_p.leaving = when
    # a trained clinician whose team assignment is under 0.4 WTE, the rest of their time in another team
    sp = new("BW-CM31", "Occupational Therapist", "Allied Health Professionals", wte=0.6)
    sp.kind = "split_new301"
    sp.extra.append(("BW-CM08", 0.3, dt.date(2026, 4, 6), None))
    # starters: one before the groups begin, one after
    a = new("BW-CM17", "Clinical Psychologist", "Add Prof Scientific and Technic", 1.0, start=dt.date(2027, 3, 1))
    a.kind = "starter_ext"
    b = new("BW-CM08", "Psychological Therapist", "Add Prof Scientific and Technic", 1.0, start=dt.date(2027, 4, 12))
    b.kind = "late_starter_ext"
    # leavers during 2026 (assignment ended), some trained
    for _ in range(26):
        team = K.TEAMS[int(r.integers(0, 11))][0]
        p = new(team)
        p.end = dt.date(2026, 1, 1) + dt.timedelta(days=int(r.integers(10, 360)))
        p.kind = "left_2026" if r.random() < 0.7 or p.position not in TRAINABLE else "left_2026_trained"
    # training records
    for p in people:
        rp = K.rng("train", p.emp)
        num = p.prev or p.emp
        if p.kind in ("old114", "old114_rehired", "leaver_old114", "hub_trained", "left_2026_trained"):
            d = OLD_RUNS[int(rp.integers(0, 7 if p.kind == "old114_rehired" else len(OLD_RUNS)))]
            if p.kind == "hub_trained" and rp.random() < 0.35:
                d = NEW_RUNS[int(rp.integers(0, 3))]
                p.train.append(("PTD-301", d, p.emp))
            else:
                p.train.append(("PTD-114", d, num))
            if rp.random() < 0.45 and p.kind != "left_2026_trained":
                p.train.append(("PTD-114", REFRESHERS[int(rp.integers(0, len(REFRESHERS)))], p.emp))
        elif p.kind in ("new301", "split_new301"):
            p.train.append(("PTD-301", NEW_RUNS[int(rp.integers(0, len(NEW_RUNS)))], p.emp))
        elif p.kind in ("ext", "starter_ext", "late_starter_ext"):
            p.train.append(("EXT-0412", dt.date(2021, 1, 1) + dt.timedelta(days=int(rp.integers(0, 1700))), p.emp))
        elif p.kind == "refresher_only":
            p.train.append(("PTD-114", REFRESHERS[int(rp.integers(2, len(REFRESHERS)))], p.emp))
            if rp.random() < 0.5:
                p.train.append(("EXT-0390", dt.date(2023, 1, 1) + dt.timedelta(days=int(rp.integers(0, 800))), p.emp))
        # mandatory and other courses
        first = max(dt.date(2022, 4, 4), p.start)
        last = min(dt.date(2026, 12, 18), getattr(p, "end", None) or dt.date(2026, 12, 18))
        spans = [(first, last, p.emp)]
        if p.prev:
            spans.insert(0, (dt.date(2022, 4, 4), p.old_end, p.prev))
        for s0, s1, who in spans:
            for code_, years in MANDATORY:
                d = s0 + dt.timedelta(days=int(rp.integers(0, 200)))
                while d <= s1:
                    p.train.append((code_, d, who))
                    d = d + dt.timedelta(days=int(365 * years + rp.integers(-40, 40)))
        if p.position in TRAINABLE:
            for code_ in CLINICAL:
                if rp.random() < 0.22:
                    d = first + dt.timedelta(days=int(rp.integers(0, max(1, (last - first).days))))
                    p.train.append((code_, d, p.emp))
    return people


def active(start, end, day):
    return start <= day and (end is None or end >= day)


def assignments(people):
    """ESR rows: (employee, previous, assignment no, organisation, position, staff group, wte, start, end, leaving)."""
    rows = []
    for p in people:
        k = 1
        end = getattr(p, "end", None)
        if p.team == "BW-CM31" and p.start < K.MERGER:
            half = "BW-CM14" if K.rng("half", p.emp).random() < 0.5 else "BW-CM15"
            rows.append((p.emp, p.prev, "%s-%d" % (p.emp, k), ORG[half], p.position, p.group, p.wte, p.start,
                         min(end, K.MERGER - dt.timedelta(days=1)) if end else K.MERGER - dt.timedelta(days=1), None))
            k += 1
            if end is None or end >= K.MERGER:
                rows.append((p.emp, p.prev, "%s-%d" % (p.emp, k), ORG["BW-CM31"], p.position, p.group, p.wte,
                             K.MERGER, end, p.leaving))
                k += 1
        else:
            rows.append((p.emp, p.prev, "%s-%d" % (p.emp, k), ORG[p.team], p.position, p.group, p.wte, p.start, end,
                         p.leaving))
            k += 1
        for team, w, s, e in p.extra:
            rows.append((p.emp, p.prev, "%s-%d" % (p.emp, k), ORG[team], p.position, p.group, w, s, e, p.leaving))
            k += 1
    return rows


def write_all(out_dir, people):
    rows = assignments(people)
    rows.sort(key=lambda z: (z[3], z[0], z[2]))
    with open(os.path.join(out_dir, K.F_ESR), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["employee_number", "previous_employee_number", "assignment_number", "organisation",
                    "position_title", "staff_group", "assignment_wte", "assignment_start", "assignment_end",
                    "projected_leaving_date"])
        for e, prev, an, org, pos, grp, wte, s, en, lv in rows:
            w.writerow([e, prev, an, org, pos, grp, "%.2f" % wte, s.strftime("%d/%m/%Y"),
                        en.strftime("%d/%m/%Y") if en else "", lv.strftime("%d/%m/%Y") if lv else ""])
    recs = []
    for p in people:
        for code_, d, num in p.train:
            delivery = "external" if code_.startswith("EXT") else ("e-learning" if code_ in ("MAN-104", "MAN-122")
                                                                    else "classroom")
            recs.append((num, code_, d, delivery))
    recs.sort(key=lambda z: (z[2], z[1], z[0]))
    with open(os.path.join(out_dir, K.F_LEARN), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["employee_number", "course_code", "completed_on", "delivery"])
        for num, code_, d, delivery in recs:
            w.writerow([num, code_, d.isoformat(), delivery])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Catalogue"
    ws.append(["Course code", "Title", "Length (days)", "First offered", "Status"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for code_, title, days, first, status in CATALOGUE:
        ws.append([code_, title, days, dt.date.fromisoformat(first), status])
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDE", (13, 50, 14, 14, 10)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    wb.save(os.path.join(out_dir, K.F_CATALOGUE))
    return {K.F_ESR: len(rows), K.F_LEARN: len(recs), K.F_CATALOGUE: len(CATALOGUE)}


def course_table():
    """The learning team's clinical skills programmes, runs and completions by year (April to March) for the annual
    report, counted from the records."""
    return None
