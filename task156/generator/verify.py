"""Independent verifier: reads only the shipped bundle (target/) and generator/figures.json, on its own code path (no
import of the generator's modules), and recomputes the request, every site's need and the three asks.

    python3 task156/generator/verify.py [target]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict
from xml.etree import ElementTree as ET_

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
TYPES = {"close_vote": "close", "first_post": "first_post", "low_quality": "low_quality", "suggested_edit": "edit"}
OLD_TYPE = {"Close votes": "close", "First posts": "first_post", "Low quality": "low_quality",
            "Suggested edits": "edit"}


def half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def read_csv(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheets(path):
    """Every worksheet's rows as lists of raw strings, straight from the package."""
    out = {}
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET_.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        wb = ET_.fromstring(z.read("xl/workbook.xml"))
        rels = ET_.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target_of = {r.get("Id"): r.get("Target") for r in rels}
        for sh in wb.find("m:sheets", NS):
            rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            part = "xl/" + target_of[rid].lstrip("/").replace("xl/", "")
            root = ET_.fromstring(z.read(part))
            rows = []
            for row in root.iter("{%s}row" % NS["m"]):
                vals = {}
                for c in row.findall("m:c", NS):
                    col = 0
                    for ch in re.match(r"([A-Z]+)", c.get("r")).group(1):
                        col = col * 26 + ord(ch) - 64
                    v = c.find("m:v", NS)
                    if v is None:
                        isel = c.find("m:is", NS)
                        if isel is not None:
                            vals[col] = "".join(t.text or "" for t in isel.iter("{%s}t" % NS["m"]))
                        continue
                    vals[col] = shared[int(v.text)] if c.get("t") == "s" else v.text
                rows.append([vals.get(i) for i in range(1, max(vals) + 1)] if vals else [])
            out[sh.get("name")] = rows
    return out


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return "\n".join(pg.extract_text() or "" for pg in pdf.pages)


def month_key(s):
    return int(s[:4]), int(s[5:7])


def main(target):
    here = os.path.dirname(os.path.abspath(__file__))
    F = json.load(open(os.path.join(here, "figures.json"), encoding="utf-8"))
    bad = []
    reg = read_csv(target, "site_register.csv")
    live = [r for r in reg if r["status"] == "live"]
    codes = [r["site_code"] for r in live]
    name = {r["site_code"]: r["site_name"] for r in live}
    old_code = {r["review_system_name_to_2023"]: r["site_code"] for r in reg}
    old_code["Graphics & Shaders"] = "gamedev"

    # the filed numbers: standards, FTE hours, envelope
    std_txt = pdf_text(os.path.join(target, "handle_time_standards_2027.pdf"))
    std = {}
    for label, key in (("Moderator flag", "flag"), ("Close vote", "close"), ("First post", "first_post"),
                       ("Low quality", "low_quality"), ("Suggested edit", "edit")):
        m = re.search(r"%s\s+(\d+\.\d)\s+(\d+\.\d)" % label, std_txt)
        std[key] = float(m.group(2))
    charter = re.sub(r"\s+", " ", pdf_text(os.path.join(target, "moderation_council_charter_2025.pdf")))
    fte_hours = float(re.search(r"One FTE is ([\d,]+) hours", charter).group(1).replace(",", ""))
    env_txt = re.sub(r"\s+", " ", pdf_text(os.path.join(target, "finance_envelope_2027_paid_moderation.pdf")))
    envelope = int(re.search(r"an envelope of (\d+) FTE", env_txt).group(1))

    # the platform's records, by site and month
    ent = defaultdict(float)
    ent_t = defaultdict(float)
    rev = defaultdict(float)
    rout = defaultdict(float)
    for r in read_csv(target, "review_inbox_daily_2024-01-01_2026-09-30.csv"):
        k = (r["site"],) + month_key(r["entry_date_utc"])
        ent[k] += int(r["entered"])
        ent_t[k + (TYPES[r["item_type"]],)] += int(r["entered"])
        rev[k] += int(r["reviewed_by_volunteer"])
        rout[k] += int(r["routed_to_moderation"])
    flags = defaultdict(float)
    for r in read_csv(target, "modtool_flag_summary_daily_2024-01-01_2026-09-30.csv"):
        flags[(r["site"],) + month_key(r["date_utc"])] += int(r["handled_by_moderator"])
    q = {}
    for r in read_csv(target, "posts_questions_by_site_month_2024-01_2026-09.csv"):
        q[(r["site"],) + month_key(r["month"])] = int(r["questions"])
    months = []
    y, m = 2024, 1
    while (y, m) <= (2026, 9):
        months.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    active = defaultdict(int)
    lapses = defaultdict(int)
    joins = defaultdict(int)
    for r in read_csv(target, "reviewer_roster_2026-10-08.csv"):
        a, b = month_key(r["first_review_on_platform"]), month_key(r["last_review"])
        for ym in months:
            if a <= ym <= b:
                active[(r["site"],) + ym] += 1
        if r["access_status"] == "lapsed":
            lapses[(r["site"],) + b] += 1
        if r["access_granted"] >= "2024-01-01":
            joins[(r["site"],) + month_key(r["access_granted"])] += 1
    # the old system's months
    old = []
    for sheet, rows in sheets(os.path.join(target, "review_queues_monthly_2021-2023.xlsx")).items():
        head = None
        for row in rows:
            if row and row[0] == "Site":
                head = row
                continue
            if head and row and row[0] in old_code and row[1] and str(row[1])[:3] != "Yea":
                rec = dict(zip(head, row))
                e = sum(float(rec[h]) for h in head if h and h.endswith(" in"))
                rt = sum(float(rec[h]) for h in head if h and h.endswith(" to moderators"))
                old.append(dict(site=row[0], year=int(sheet), mon=str(row[1])[:3], ent=e, rout=rt,
                                R=float(rec["Active reviewers"]), vol=float(rec["Volunteer reviews"]),
                                q=float(rec["Questions"])))
    # the pace kept when the inbox outruns the volunteers, and the share nobody picks up
    num = den = 0.0
    for o in old:
        if o["ent"] and o["rout"] / o["ent"] > 0.05:
            num += o["vol"]
            den += o["R"]
    fl_n = fl_d = 0.0
    for s in codes:
        for ym in months:
            k = (s,) + ym
            if ent[k] and rout[k] / ent[k] > 0.05:
                num += rev[k]
                den += active[k]
            if ent[k] and rout[k] / ent[k] < 1 / 60.0:
                fl_n += rout[k]
                fl_d += ent[k]
    pace, floor = num / den, fl_n / fl_d
    # the plan
    plan = {}
    for row in sheets(os.path.join(target, "question_plan_2027.xlsx"))["Plan 2027"]:
        if row and row[0] in codes:
            plan[row[0]] = [float(x) for x in row[2:14]]
    need = {}
    for s in codes:
        per_q = {t: sum(ent_t[(s,) + ym + (t,)] for ym in months) / sum(q[(s,) + ym] for ym in months)
                 for t in std if t != "flag"}
        flag_q = sum(flags[(s,) + ym] for ym in months) / sum(q[(s,) + ym] for ym in months)
        last24 = months[-25:-1]                                      # September 2024 to August 2026
        h = sum(lapses[(s,) + ym] for ym in last24) / sum(active[(s,) + ym] for ym in last24)
        inflow = sum(joins[(s,) + ym] for ym in months[-12:]) / 12.0
        pool = active[(s, 2026, 9)]
        mins = 0.0
        for k in range(15):
            pool = pool * (1 - h) + inflow
            if k < 3:
                continue
            qm = plan[s][k - 3]
            A = qm * sum(per_q.values())
            share = max(floor, 1 - pool * pace / A)
            mins += qm * flag_q * std["flag"] + A * share * sum(per_q[t] / sum(per_q.values()) * std[t] for t in per_q)
        need[s] = mins / 60.0 / fte_hours
    whole = {s: int(half_up(v)) for s, v in need.items()}
    request = sum(whole.values())
    for s in codes:
        if whole[s] != F["call"]["need_fte"][name[s]]:
            bad.append("need %s %.3f against %s" % (s, need[s], F["call"]["need_fte"][name[s]]))
    if request != F["call"]["request_fte"] or request - envelope != F["call"]["above_envelope_fte"]:
        bad.append("request %d, envelope %d" % (request, envelope))
    if int(half_up(pace)) != F["components"]["reviews_a_month"]:
        bad.append("pace %.2f" % pace)

    # Ask A: first action within 24 hours, the decision-review log's first action where a decision was reviewed
    first = {r["flag_id"]: r["first_action_at_utc"] for r in read_csv(target, "flag_decision_reviews_2026-07_to_2026-09.csv")}
    seen = {}
    for f in ("modtool_flags_2026-07-01_to_2026-08-15.csv", "modtool_flags_2026-08-15_to_2026-09-30.csv"):
        for r in read_csv(target, f):
            seen[r["flag_id"]] = r
    n_in, n_all = defaultdict(int), defaultdict(int)
    for fid, r in seen.items():
        if r["outcome"] == "closed_post_deleted":
            continue
        t0 = dt.datetime.fromisoformat(r["raised_at_utc"])
        t1 = dt.datetime.fromisoformat(first.get(fid, r["handled_at_utc"]))
        k = (r["site"], t0.month)
        n_all[k] += 1
        n_in[k] += (t1 - t0).total_seconds() <= 86400
    mname = {7: "July", 8: "August", 9: "September"}
    for (s, mo), n in n_all.items():
        v = "%.1f" % half_up(100.0 * n_in[(s, mo)] / n, 1)
        if v != F["answers"]["ask_a_pct"]["%s %s 2026" % (name[s], mname[mo])]:
            bad.append("ask A %s %d %s" % (s, mo, v))

    # Ask B: approved lines, the site from the HR history on the shift's start day, the quarter of that day
    by_name = {r["site_name"]: r["site_code"] for r in live}
    spans = defaultdict(list)
    for r in read_csv(target, "moderator_site_assignments.csv"):
        spans[r["employee_no"]].append((r["effective_from"], r["effective_to"] or "9999-12-31", by_name[r["site"]]))
    hrs = defaultdict(float)
    for r in read_csv(target, "wfm_shift_lines_2026-01-01_2026-09-30.csv"):
        if r["line_status"] != "approved":
            continue
        d = r["shift_date"]
        site = next(c for a, b, c in spans[r["employee_no"]] if a <= d <= b)
        hrs[(site, (int(d[5:7]) + 2) // 3)] += float(r["paid_hours"])
    for (s, qn), v in hrs.items():
        if format(int(half_up(v)), ",") != F["answers"]["ask_b_hours"]["%s Q%d 2026" % (name[s], qn)]:
            bad.append("ask B %s Q%d %.1f" % (s, qn, v))

    # Ask C: 2022 rebuilt from the workbook and the migration log (each question on its site today, in its month)
    q22 = defaultdict(float)
    for o in old:
        if o["year"] == 2022 and ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"].count(o["mon"]):
            q22[old_code[o["site"]]] += o["q"]
    for r in read_csv(target, "question_moves_2021-2023.csv"):
        a, b = r["asked_at_utc"], r["moved_at_utc"]
        src, dst = old_code[r["from_site"]], old_code[r["to_site"]]
        if "2022-01-01" <= a < "2022-10-01":
            q22[src] -= 1
            q22[dst] += 1
        if "2022-01-01" <= b < "2022-10-01":
            q22[dst] -= 1
    for s in codes:
        q26 = sum(q[(s, 2026, mm)] for mm in range(1, 10))
        v = "%.1f" % half_up(100.0 * q26 / q22[s], 1)
        if v != F["answers"]["ask_c_pct"][name[s]]:
            bad.append("ask C %s %s" % (s, v))

    print("verify: request %d (%s), pace %.2f, floor %.4f; ask A %d, ask B %d, ask C %d figures; %s" % (
        request, ", ".join("%s %d" % (s, whole[s]) for s in codes), pace, floor, len(n_all), len(hrs), len(codes),
        "all reproduce" if not bad else "MISMATCH: " + "; ".join(bad)))
    if bad:
        raise SystemExit("verify failed")


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target"))
