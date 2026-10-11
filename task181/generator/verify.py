"""Independent verifier. Reads only target/ and golden/, shares no code with golden.py, and recomputes the
call, the rungs below it, the route speeds the slide states and every ask figure with the standard
library, openpyxl and pyarrow."""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

import openpyxl
import pyarrow.parquet as pq

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYD = ZoneInfo("Australia/Sydney")
TEN = ["Wagga Wagga", "Griffith", "Leeton", "Narrandera", "Murrumbidgee", "Hay", "Edward River", "Junee",
       "Cootamundra-Gundagai", "Snowy Valleys"]
D = dt.date


def day(s):
    return D.fromisoformat(s)


def local_day(stamp):
    return dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(SYD).date()


def main(target, golden):
    rows = list(csv.DictReader(open(os.path.join(target, "pertussis_notifications_2019-2026.csv"), newline="")))
    wb = openpyxl.load_workbook(os.path.join(target, "postcode_lga_concordance.xlsx"), read_only=True)
    shares = defaultdict(dict)
    for r in wb["Postcode to LGA"].iter_rows(min_row=5, values_only=True):
        if r[0]:
            shares[str(r[0])][r[2]] = float(r[4])

    def area_of(pc):
        if pc not in shares:
            return None
        lga = max(shares[pc].items(), key=lambda kv: kv[1])[0]
        return lga if lga in TEN else None

    for r in rows:
        r["s"] = day(r["specimen_date"])
        r["r"] = local_day(r["received_utc"])
    # PR-07 3.3: episodes of 90 days from the first specimen
    per = defaultdict(list)
    for r in rows:
        per[r["person_id"]].append(r)
    cases = []
    for pid, rs in per.items():
        rs.sort(key=lambda r: (r["s"], r["received_utc"]))
        cur = None
        for r in rs:
            if cur is None or (r["s"] - cur["date"]).days > 90:
                cur = {"date": r["s"], "rows": [r]}
                cases.append(cur)
            else:
                cur["rows"].append(r)
    for c in cases:
        f = c["rows"][0]
        c["area"] = area_of(f["postcode"])
        c["status"] = "Confirmed" if any(x["case_status"] == "Confirmed" for x in c["rows"]) else "Probable"
        c["lab"] = f["notifying_lab"]
        c["dob"] = day(f["dob"])
        c["mrn"] = next((x["mrn"] for x in c["rows"] if x["mrn"]), "")
        c["school"] = next((x["school_or_childcare"] for x in c["rows"] if x["school_or_childcare"]), "")
        c["role"] = next((x["school_role"] for x in c["rows"] if x["school_role"]), "")
        c["first_r"] = min(x["r"] for x in c["rows"])
    ex = D(2026, 10, 5)
    fortnight = [ex - dt.timedelta(days=k) for k in range(14, 0, -1)]

    def count(a, days, key="date"):
        return sum(1 for c in cases if c["area"] == a and days[0] <= c[key] <= days[-1])

    E = {a: sum(count(a, [D(y, d.month, d.day) for d in fortnight]) for y in range(2021, 2026)) / 5.0 for a in TEN}
    N = {a: count(a, fortnight) for a in TEN}

    def top(score):
        return sorted(TEN, key=lambda a: (-score[a], a))

    assert top(N)[0] == "Wagga Wagga", "rung 0"
    assert top({a: N[a] - E[a] for a in TEN})[0] == "Wagga Wagga", "rung 1"
    assert top({a: N[a] / E[a] if E[a] else 0 for a in TEN})[0] == "Wagga Wagga", "rung 2"
    # delays over specimens collected 24 August 2025 to 23 August 2026 (six weeks or more before the extract)
    hist = [r for r in rows if D(2025, 8, 24) <= r["s"] <= D(2026, 8, 23)]
    last = D(2026, 10, 4)

    def mean_completeness(sel):
        delays = [(r["r"] - r["s"]).days for r in sel]
        return sum(sum(1 for x in delays if x <= (last - d).days) / len(delays) for d in fortnight) / 14.0

    pooled = mean_completeness(hist)
    by_lab = {lab: mean_completeness([r for r in hist if r["notifying_lab"] == lab]) for lab in {r["notifying_lab"] for r in hist}}
    R3 = {a: N[a] / pooled - E[a] for a in TEN}
    assert top(R3)[0] == "Wagga Wagga", "rung 3: one pooled delay"
    R4 = {}
    for a in TEN:
        R4[a] = sum(sum(1 for c in cases if c["area"] == a and c["lab"] == lab and fortnight[0] <= c["date"] <= fortnight[-1])
                    / by_lab[lab] for lab in by_lab) - E[a]
    order = top(R4)
    assert order[0] == "Griffith", "the call: %s" % order[0]
    assert R4["Griffith"] >= 2.5 * R4[order[1]], "the call's margin"
    # the route speeds on the slide: notifications for specimens collected August 2025 to July 2026
    speed = {}
    for lab in by_lab:
        sel = [r for r in rows if r["notifying_lab"] == lab and D(2025, 8, 1) <= r["s"] <= D(2026, 7, 31)]
        speed[lab] = sum(1 for r in sel if (r["r"] - r["s"]).days <= 14) / len(sel)
    # ask A
    adm = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(target, "respiratory_admissions_2019-2026.csv"), newline="")):
        adm[int(r["mrn"])].append(dt.datetime.strptime(r["admission_date"], "%d/%m/%Y").date())
    births = {int(r["baby_mrn"]): r for r in csv.DictReader(open(os.path.join(target, "birth_records_2024-2026.csv"), newline=""))}
    t = pq.read_table(os.path.join(target, "antenatal_vaccinations_2019-2026.parquet")).to_pydict()
    dtpa = defaultdict(list)
    for card, irn, d, ag in zip(t["medicare_card"], t["irn"], t["dose_date"], t["antigen"]):
        if ag == "dTpa":
            dtpa[card.replace(" ", "") + str(irn)].append(d)

    def six_months(b):
        m = b.month + 6
        y = b.year + (m - 1) // 12
        m = (m - 1) % 12 + 1
        import calendar
        return D(y, m, min(b.day, calendar.monthrange(y, m)[1]))

    A = {}
    for a in TEN:
        sel = [c for c in cases if c["area"] == a and D(2026, 1, 1) <= c["date"] <= D(2026, 8, 31)]
        inf = [c for c in sel if c["date"] < six_months(c["dob"])]
        n_adm = sum(1 for c in inf if c["mrn"] and any(abs((x - c["date"]).days) <= 14 for x in adm.get(int(c["mrn"]), [])))
        n_vac = 0
        for c in inf:
            b = births.get(int(c["mrn"])) if c["mrn"] else None
            if not b:
                continue
            born = day(b["birth_date"])
            start = born - dt.timedelta(weeks=int(b["gestation_weeks"]))
            if any(start <= x <= born - dt.timedelta(days=14) for x in dtpa.get(b["mother_medicare_no"], [])):
                n_vac += 1
        A[a] = (sum(1 for c in sel if c["status"] == "Confirmed"), sum(1 for c in sel if c["status"] == "Probable"),
                len(inf), n_adm, n_vac)
    # ask B: roster names matched on their distinctive words
    rw = openpyxl.load_workbook(os.path.join(target, "school_rosters_term3_2026.xlsx"), read_only=True)
    schools = []
    generic = {"public", "school", "ps", "p", "s", "high", "hs", "primary", "the", "griffith", "wagga", "tumut",
               "leeton", "cootamundra", "narrandera", "st", "street", "rd", "road", "ave", "av", "avenue", "pub", "sth", "nth"}
    for ws in rw.worksheets:
        head = list(ws.iter_rows(min_row=1, max_row=6, values_only=True))
        name = head[0][0]
        lga = [v[1] for v in head if v[0] == "LGA"][0]
        words = set(re.findall(r"[a-z]+", name.lower())) - generic
        schools.append((name, lga, words, "high" in name.lower()))

    def which(text):
        w = set(re.findall(r"[a-z]+", text.lower()))
        if w & {"preschool", "pre"}:
            return None
        hits = [s for s in schools if s[2] and s[2] <= w and (s[3] == bool(w & {"high", "hs"}))]
        return hits[0] if len(hits) == 1 else None

    cnt = defaultdict(int)
    for c in cases:
        if c["role"] == "Student" and c["school"] and D(2026, 9, 5) <= c["date"] <= D(2026, 10, 4):
            s = which(c["school"])
            if s:
                cnt[(s[0], s[1])] += 1
    B = sorted(((k[0], k[1], n) for k, n in cnt.items() if n >= 2), key=lambda x: (-x[2], x[0]))
    # against the goldens
    gc = {r["lga"]: r for r in csv.DictReader(open(os.path.join(golden, "pertussis_cases_by_lga.csv"), newline=""))}
    cols = ("confirmed_cases", "probable_cases", "infants_under_6_months", "infants_admitted_to_hospital",
            "infants_mother_vaccinated_14d_before_birth")
    for a in TEN:
        assert tuple(int(gc[a][c]) for c in cols) == A[a], "golden CSV %s: %s against %s" % (a, gc[a], A[a])
    from pptx import Presentation
    text = []
    for sh in Presentation(os.path.join(golden, "response_team_brief.pptx")).slides[0].shapes:
        if sh.has_text_frame:
            text.append(sh.text_frame.text)
        if getattr(sh, "has_table", False) and sh.has_table:
            text.append("\n".join("|".join(c.text for c in r.cells) for r in sh.table.rows))
    slide = "\n".join(text)
    assert "Send the response team to %s this week" % order[0] in slide, "slide call"
    for name, lga, n in B:
        assert "%s|%s|%d" % (name, lga, n) in slide, "slide cluster %s" % name
    for a in TEN:
        assert "%s|%d|%.1f|" % (a, N[a], E[a]) in slide, "slide row %s" % a
    for lab, label in (("Wagga Wagga Hospital Laboratory", "Hospital laboratory"), ("Inland Pathology", "Inland Pathology")):
        assert "%s|%d%%" % (label, round(100 * speed[lab])) in slide, "slide speed %s" % lab
    print("verify: OK. %s (excess %.1f; next %s %.1f); rungs 0 to 3 Wagga Wagga; %d clusters; 50 ask A figures; "
          "route speeds %s" % (order[0], R4[order[0]], order[1], R4[order[1]], len(B),
                               ", ".join("%s %.1f%%" % (k, 100 * v) for k, v in sorted(speed.items()))))
    return dict(answer=order[0], N=N, E=E, A=A, B=B, speed=speed)


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
