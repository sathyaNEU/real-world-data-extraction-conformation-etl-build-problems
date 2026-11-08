"""task482 architecture 17: the independent verifier. Recomputes the call and every ask figure from the shipped files
alone (target/), with its own Rasch estimation and its own reading of the course review's appendix, and compares with
figures.json. Exit 1 on any difference."""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
NZ = dt.timezone(dt.timedelta(hours=12))
MON = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def pdf(name):
    return subprocess.run(["pdftotext", "-layout", os.path.join(T, name), "-"], capture_output=True, text=True,
                          check=True).stdout


def sheet(name, ws):
    rows = list(openpyxl.load_workbook(os.path.join(T, name), read_only=True)[ws].iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def start_date(s):
    s = s.strip()
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m = re.search(r"(\d{1,2}) ([A-Z][a-z]{2})", s)
    return dt.date(2026, MON[m.group(2)], int(m.group(1)))


def unit_of(name):
    n = name.lower()
    if any(k in n for k in ("force", "motion", "mechanic")):
        return "U5"
    if any(k in n for k in ("earth", "tecton")):
        return "U6"
    raise ValueError(name)


def appendix(names):
    """{school_code: (first Term 3 unit, its last day)} from Appendix B, columns found from its header line."""
    txt = pdf("y10sci_course_review_2026.pdf")
    pages = txt[txt.index("Appendix B"):].split("\f")
    rows, cur = [], None
    for page in pages:
        lines = [l for l in page.splitlines() if l.strip() and not l.strip().startswith("began")
                 and "course review 2026" not in l and not re.search(r"Page \d+", l)]
        hits = [m.start(1) for l in lines for m in [re.search(r"\s{3,}(Wks 1-|Weeks 1 to |\d{1,2}/\d{1,2} to )", l)] if m]
        if not hits:
            continue
        c3 = min(hits)       # the Term 3 column's left edge on this page
        for l in lines:
            name = next((n for n in sorted(names, key=len, reverse=True) if l.startswith(n)), None)
            if name:
                rest = l[len(name):].strip()
                cur = [name, re.split(r"\s{3,}", rest)[0], "", ""]
                rows.append(cur)
            if cur is None:
                continue
            cur[3] += " " + l[c3:].strip()
    out = {}
    for name, start, _, t3 in rows:
        ts = start_date(start)
        t3 = " ".join(t3.split())
        m = re.match(r"Wks 1-(\d+) (.+?); Wks", t3) or re.match(r"Weeks 1 to (\d+): (.+?)\. Weeks", t3)
        if m:
            k, first = int(m.group(1)), m.group(2)
            mon = ts - dt.timedelta(days=ts.weekday())
            end = mon + dt.timedelta(days=7 * (k - 1) + 4)
        else:
            m = re.match(r"\d{1,2}/\d{1,2} to (\d{1,2})/(\d{1,2}) (.+?); ", t3)
            end, first = dt.date(2026, int(m.group(2)), int(m.group(1))), m.group(3)
        out[names[name]] = (unit_of(first), end)
    return out


def sig(x):
    return 1 / (1 + np.exp(-x))


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    bank = {r["item_code"]: r for r in sheet("corlinn_item_bank_2026.xlsx", "Bank")}
    card = {}
    with open(os.path.join(T, "item_renumbering_2025.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["item_code"]:
                card[int(r["card_no"])] = r["item_code"]
    drafts = {d: [card[int(r["Card"])] for r in sheet("y10sci_2027_drafts.xlsx", "Paper " + d)] for d in "ABC"}
    ach = float(re.search(r"Achieved\s+([0-9.]+)", pdf("standard_setting_record_y10sci.pdf")).group(1))
    schools, names = {}, {}
    with open(os.path.join(T, "member_schools.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            schools[r["school_code"]] = r["region"]
            names[r["school_name"]] = r["school_code"]
    seq = appendix(names)
    sess = {}
    with open(os.path.join(T, "y10sci_aug2026_sessions.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            sess[r["session_id"]] = r
    day, school_of = {}, {}
    for r in sess.values():
        t = dt.datetime.strptime(r["started_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        day[r["entry_no"]] = t.astimezone(NZ).date()
        school_of[r["entry_no"]] = r["school_code"]
    last = {}
    with open(os.path.join(T, "y10sci_aug2026_responses.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            k = (r["entry_no"], r["item_code"])
            st = sess[r["session_id"]]["started_utc"]
            if k not in last or st >= last[k][0]:
                last[k] = (st, int(r["score"]))
    ents = sorted(day)
    codes = sorted(bank)
    ei = {e: i for i, e in enumerate(ents)}
    ci = {c: j for j, c in enumerate(codes)}
    R = np.zeros((len(ents), len(codes)))
    M = np.zeros_like(R)
    for (e, c), (_, v) in last.items():
        R[ei[e], ci[c]] = v
        M[ei[e], ci[c]] = 1
    b = np.array([float(bank[c]["difficulty"]) for c in codes])
    unit = [bank[c]["unit"] for c in codes]
    early = [j for j, u in enumerate(unit) if u in ("U1", "U2", "U3", "U4")]
    late = [j for j, u in enumerate(unit) if u in ("U5", "U6")]
    th = np.zeros(len(ents))
    for _ in range(40):
        p = sig(th[:, None] - b[None, early])
        th = np.clip(th + ((R[:, early] - p) * M[:, early]).sum(1) /
                     np.maximum((p * (1 - p) * M[:, early]).sum(1), 1e-9), -4.5, 4.5)
    taught = np.zeros((len(ents), len(late)))
    for i, e in enumerate(ents):
        first, end = seq[school_of[e]]
        for k, j in enumerate(late):
            taught[i, k] = 1.0 if (unit[j] == first and day[e] > end) else 0.0
    Mt = M[:, late] * taught
    bl = b[late].copy()
    for _ in range(40):
        p = sig(th[:, None] - bl[None, :])
        bl = bl + ((p - R[:, late]) * Mt).sum(0) / np.maximum((p * (1 - p) * Mt).sum(0), 1e-9)
    b2 = b.copy()
    b2[late] = bl
    marks = {d: float(sig(ach - b2[[ci[c] for c in drafts[d]]]).sum()) for d in "ABC"}
    bank_marks = {d: float(sig(ach - b[[ci[c] for c in drafts[d]]]).sum()) for d in "ABC"}
    call = min(marks, key=lambda d: abs(marks[d] - 25))
    print("verify: marks %s, bank %s, call Paper %s" % ({d: round(v, 2) for d, v in marks.items()},
                                                        {d: round(v, 2) for d, v in bank_marks.items()}, call))
    if "Paper " + call != fig["call"]:
        bad.append("call")
    for d in "ABC":
        if abs(marks[d] - float(fig["expected_achieved_mark_2dp"][d])) > 0.006:
            bad.append("mark %s" % d)
        if abs(bank_marks[d] - float(fig["bank_expected_achieved_mark_2dp"][d])) > 0.006:
            bad.append("bank mark %s" % d)
    # the asks
    reg = list(fig["entered"])
    ent = sheet("entries_register_aug2026.xlsx", "Entries")
    seen, exact, entered = set(), set(), {r: 0 for r in reg}
    sch_of_entry = {}
    for e in ent:
        sch_of_entry.setdefault(e["Entry no"], e["School code"])
        if e["Status"] != "E" or tuple(e.values()) in exact:
            continue
        exact.add(tuple(e.values()))
        key = (e["First name"], e["Surname"], str(e["Date of birth"]))
        if key not in seen:
            seen.add(key)
            entered[schools[e["School code"]]] += 1
    rost = {}
    for l in pdf("makeup_roster_aug2026.pdf").splitlines():
        s = re.search(r"\b(C\d{3}-\d{3})\b", l)
        if s and re.search(r"\b26-\d{5}\b", l):
            rost[s.group(1)] = re.search(r"\b(C\d{3})\b(?!-)", l).group(1)
    sat = {r: 0 for r in reg}
    for e, c in school_of.items():
        sat[schools[c]] += 1
    nmk = {r: 0 for r in reg}
    mk = {r: [] for r in reg}
    with open(os.path.join(T, "makeup_scripts_keyed.csv"), newline="") as fh:
        keyed = list(csv.DictReader(fh))
    # the roster's header: M26 is marked out of 50, the cover carries the mark and its percentage, and a keyer's
    # session is one batch on one template, so a batch holding values over 50 was keyed from the percentage
    off = {s["batch"] for s in keyed if float(s["mark"]) > 50}
    for s in keyed:
        home = rost.get(s["script_no"]) or sch_of_entry[s["entry_no"]]
        r = schools[home]
        sat[r] += 1
        nmk[r] += 1
        v = float(s["mark"])
        mk[r].append(v / 2 if s["batch"] in off else v)
    for r in reg:
        if entered[r] != fig["entered"][r]:
            bad.append("entered %s" % r)
        if sat[r] != fig["sat"][r]:
            bad.append("sat %s" % r)
        if nmk[r] != fig["makeup_candidates"][r]:
            bad.append("makeup count %s" % r)
        if "%.1f" % (sum(mk[r]) / len(mk[r])) != fig["makeup_mean"][r]:
            bad.append("makeup mean %s" % r)
    print("verify: entered %s sat %s make-up %s means %s" % (entered, sat, nmk,
                                                             {r: round(sum(v) / len(v), 2) for r, v in mk.items()}))
    for x in bad:
        print("FAIL verify " + x)
    print("verify: %s" % ("PASS" if not bad else "%d differences" % len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
