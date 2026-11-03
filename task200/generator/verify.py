"""Independent verifier: reads only the shipped bundle (target/, the goldens, figures.json and submission.md) with
the standard library and openpyxl, on its own code path, and recomputes every graded figure.

    python3 task200/generator/verify.py
"""
import bisect
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

LON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
TEAMS = ["Arden", "Brook", "Cleve", "Dene", "Esk", "Fell"]


def rows(path, skip=0):
    with open(path, encoding="utf-8", newline="") as fh:
        for _ in range(skip):
            fh.readline()
        yield from csv.DictReader(fh)


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def local(s, fmt):
    return dt.datetime.strptime(s, fmt).replace(tzinfo=LON).astimezone(UTC)


def sheet(path, name):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[name]
    it = ws.iter_rows(values_only=True)
    head = None
    out = []
    for r in it:
        if head is None:
            if r and r[0] in ("Staff no", "Team", "Course month (2027)"):
                head = list(r)
            continue
        if r[0] is None:
            continue
        out.append(dict(zip(head, r)))
    return out


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x))


def main(target, golden, figures_path, submission_path):
    T = lambda rel: os.path.join(target, rel)
    roster = sheet(T("staff/screening_roster_2026-12-31.xlsx"), "Roster")
    team = {int(r["Staff no"]): r["Team"] for r in roster}
    login = {r["CT login"]: int(r["Staff no"]) for r in roster}
    opno = {str(r["Pier B TIP operator"]).zfill(3): int(r["Staff no"]) for r in roster}
    # ---------------------------------------------------------------- projections, every system, one history each
    seen = set()
    ev = []
    for y in (2024, 2025, 2026):
        for r in rows(T("screening_tip/ct_tip_events_%d.csv" % y)):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            who = login.get(r["operator_login"], "ct:" + r["operator_login"])
            ev.append((utc(r["projection_utc"]), len(ev), who, r["tip_image"], r["result"]))
    for r in rows(T("screening_tip/pierb_tip_log_2023-09_2026-12.csv"), skip=3):
        who = opno.get(r["Operator"].zfill(3), "pb:" + r["Operator"])
        res = {"H": "HIT", "M": "MISS", "X": "CANCELLED"}[r["Result"]]
        ev.append((local(r["Date"] + " " + r["Time"], "%d/%m/%Y %H:%M:%S"), len(ev), who, r["Image"], res))
    ev.sort()
    met = defaultdict(int)
    fn = defaultdict(int)
    fh = defaultdict(int)
    an = defaultdict(int)
    ah = defaultdict(int)
    for ts, _n, who, img, res in ev:
        if res == "CANCELLED":
            continue
        k = met[(who, img)]
        met[(who, img)] = k + 1
        if ts.astimezone(LON).year != 2026 or who not in team:
            continue
        tm = team[who]
        an[tm] += 1
        ah[tm] += res == "HIT"
        if k == 0:
            fn[tm] += 1
            fh[tm] += res == "HIT"
    rate = {t: fh[t] / fn[t] for t in TEAMS}
    order = sorted(TEAMS, key=lambda t: rate[t])
    F = json.load(open(figures_path))
    assert order == F["order"], (order, F["order"])
    for t in TEAMS:
        assert round(100 * rate[t]) == F["first_rate_pct"][t] and fn[t] == F["first_n"][t] and fh[t] == F["first_hits"][t], t
        assert round(100 * ah[t] / an[t]) == F["all_rate_pct"][t], t
    print("verify: order %s; first meetings %s" % (order, {t: round(100 * rate[t], 2) for t in TEAMS}))
    # ---------------------------------------------------------------- screen time
    sec = defaultdict(float)
    spans = defaultdict(list)
    for r in rows(T("positions/ct_workstation_sessions_2026.csv")):
        spans[r["login"]].append((utc(r["logon_utc"]), utc(r["logoff_utc"])))
    for lg, sp in spans.items():
        sp.sort()
        a0, a1 = sp[0]
        for b0, b1 in sp[1:]:
            if b0 > a1:
                if lg in login:
                    sec[team[login[lg]]] += (a1 - a0).total_seconds()
                a0, a1 = b0, b1
            else:
                a1 = max(a1, b1)
        if lg in login:
            sec[team[login[lg]]] += (a1 - a0).total_seconds()
    reg = defaultdict(list)
    for r in rows(T("staff/id_centre_badge_register.csv")):
        i = dt.datetime.strptime(r["issued"], "%d/%m/%Y").date()
        c = dt.datetime.strptime(r["cancelled"], "%d/%m/%Y").date() if r["cancelled"] else dt.date(2100, 1, 1)
        reg[r["badge_no"]].append((i, c, int(r["staff_no"])))

    def holder(badge, when):
        d = when.astimezone(LON).date()
        for i, c, s in reg.get(badge, []):
            if i <= d < c:
                return s
        return None
    cur = {}
    pbrej = defaultdict(list)
    for r in rows(T("positions/pierb_screen_events_2026.csv")):
        t = local(r["Date"] + " " + r["Time"], "%d/%m/%Y %H:%M:%S")
        scr, e, b = r["Screen"], r["Event"], r["Badge"]
        if e == "REJECT":
            pbrej[r["Tray"]].append((t, b))
            continue
        if e in ("LOGON", "SHUTDOWN") or (e == "LOGOFF" and scr in cur and cur[scr][0] == b):
            if scr in cur:
                ob, t0 = cur.pop(scr)
                s = holder(ob, t0)
                if s in team:
                    sec[team[s]] += (t - t0).total_seconds()
            if e == "LOGON":
                cur[scr] = (b, t)
    hours = {t: round(sec[t] / 3600.0 + 1e-9, 1) for t in TEAMS}
    for t in TEAMS:
        assert abs(hours[t] - F["hours"][t]) < 1e-6, (t, hours[t], F["hours"][t])
    print("verify: screen time %s" % hours)
    # ---------------------------------------------------------------- clear searches
    rej = defaultdict(list)
    for r in rows(T("search/ct_tray_rejects_2026.csv")):
        rej[r["tray_tag"]].append((utc(r["reject_utc"]), r["workstation"]))
    for v in rej.values():
        v.sort()
    for v in pbrej.values():
        v.sort()
    ws = defaultdict(list)
    for lg, sp in spans.items():
        pass
    for r in rows(T("positions/ct_workstation_sessions_2026.csv")):
        ws[r["workstation"]].append((utc(r["logon_utc"]), utc(r["logoff_utc"]), r["login"]))
    for v in ws.values():
        v.sort()
    starts = {k: [x[0] for x in v] for k, v in ws.items()}
    clear = defaultdict(int)
    for r in rows(T("search/search_log_2026.csv")):
        if r["outcome"] not in ("NF", "CLEAR"):
            continue
        taken = local(r["taken_local"], "%Y-%m-%d %H:%M:%S")
        for tray in r["tray_tag"].split(";"):
            if r["area"] == "Central":
                lst = [x for x in rej.get(tray, []) if x[0] < taken]
                if not lst:
                    continue
                t, w = lst[-1]
                i = bisect.bisect_right(starts[w], t)
                who = None
                for a, b, lg in ws[w][max(0, i - 3):i]:
                    if a <= t < b:
                        who = lg
                if who in login:
                    clear[team[login[who]]] += 1
            else:
                lst = [x for x in pbrej.get(tray, []) if x[0] < taken]
                if not lst:
                    continue
                s = holder(lst[-1][1], lst[-1][0])
                if s in team:
                    clear[team[s]] += 1
    for t in TEAMS:
        assert clear[t] == F["clear"][t], (t, clear[t], F["clear"][t])
    print("verify: clear searches %s" % dict(clear))
    # ---------------------------------------------------------------- certificates
    centre = {}
    for r in rows(T("training/assessment_centre_certificates.csv")):
        centre[r["certificate_no"]] = (int(r["candidate_staff_no"]),
                                       dt.datetime.strptime(r["assessment_date"], "%d/%m/%Y").date())
    last = {}
    for r in sheet(T("training/lms_assessment_export_2027-01-11.xlsx"), "Assessments"):
        if r["Result"] != "PASS" or r["Course code"] not in ("IIC", "EXT-IIC"):
            continue
        if r["Course code"] == "EXT-IIC":
            continue
        d = r["Completed"].date()
        s = int(r["Staff no"])
        last[s] = max(last.get(s, d), d)
    # every certificate the centre awarded, on its assessment date, whether or not the LMS holds it yet
    for s, d in centre.values():
        last[s] = max(last.get(s, d), d)
    certs = defaultdict(int)
    for s, d in last.items():
        if s in team and d.replace(year=d.year + 3) < dt.date(2027, 7, 1):
            certs[team[s]] += 1
    for t in TEAMS:
        assert certs[t] == F["certs"][t], (t, certs[t], F["certs"][t])
    print("verify: certificates %s" % dict(certs))
    # ---------------------------------------------------------------- the documents and the goldens read back
    sps = docx_text(T("docs/SPS-04_screener_performance_standard_issue3.docx"))
    assert "least likely to find a prohibited article" in sps
    from pypdf import PdfReader
    rv = " ".join(p.extract_text() for p in PdfReader(T("docs/security_compliance_review_2026.pdf")).pages)
    assert "covert" in rv.lower()
    eml = open(T("docs/re_remedial_course_2027.eml"), encoding="utf-8").read()
    assert "22 January" in eml
    g = sheet(os.path.join(golden, "remedial_course_2027.xlsx"), "Course order")
    assert [r["Team"] for r in g] == order
    gt = sheet(os.path.join(golden, "remedial_course_2027.xlsx"), "Teams 2026")
    for r in gt:
        if r["Team"] == "Airport":
            assert abs(r["Screen time 2026 (hours)"] - round(sum(sec.values()) / 3600.0 + 1e-9, 1)) < 1e-9
            assert r["Clear searches 2026"] == sum(clear.values())
            assert r["Certificates running out before 1 July 2027"] == sum(certs.values())
            continue
        assert abs(r["Screen time 2026 (hours)"] - hours[r["Team"]]) < 1e-9 and r["Clear searches 2026"] == clear[r["Team"]]
        assert r["Certificates running out before 1 July 2027"] == certs[r["Team"]]
    note = docx_text(os.path.join(golden, "remedial_course_2027_note.docx"))
    assert ("%s, %s, %s, %s, %s, %s" % tuple(order)) in note
    sub = open(submission_path, encoding="utf-8").read()
    assert ", ".join(order) in sub and "{:,}".format(F["first_hits"][order[0]]) in sub
    for t in TEAMS:
        assert ("%s: %s" % (t, "{:,.1f}".format(hours[t]))) in sub and ("%s: %s" % (t, "{:,}".format(clear[t]))) in sub
    print("verify: goldens, documents and submission agree")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(here, "figures.json"),
         os.path.join(task, "submission.md"))
