"""task162 independent verifier: reads only the shipped bundle (and generator/figures.json to compare), on its own code
path (no import of calc, world or the writers), and recomputes the call, the default path and every ask figure; reads
back every format the pack ships, with a positive control on each reader.

    python3 task162/generator/verify.py <target>"""
from __future__ import annotations

import csv
import datetime as dt
import email
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def check(label, cond, detail=""):
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % detail) if detail != "" else ""))
    if not cond:
        FAIL.append(label)


def mon(d):
    return d - dt.timedelta(days=d.weekday())


def read_csv(t, f):
    with open(os.path.join(t, f), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ------------------------------------------------------------------------------------------------- readers
def pdf_text(path):
    import pypdf
    return "\n".join(p.extract_text() for p in pypdf.PdfReader(path).pages)


def docx_paras(path):
    import docx
    d = docx.Document(path)
    out = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            out.append(" ".join(c.text for c in row.cells))
    return out


def eml_body(path):
    with open(path, "rb") as fh:
        m = email.message_from_binary_file(fh)
    return m.get_payload(decode=True).decode("utf-8"), m


def xlsx_rows(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=False)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    return rows


def main(t):
    # ---- the release calendar (pypdf, its own parse of the table text)
    txt = pdf_text(os.path.join(t, "release_calendar_2025_2027.pdf"))
    rel = {}
    for m in re.finditer(r"(?m)^(\d{2})\.0\s+(\d{1,2})\.(\d{1,2})\.(\d{4})\s+(\d{1,2})\.(\d{1,2})\.(\d{4})", txt):
        rel[int(m.group(1))] = dt.date(int(m.group(7)), int(m.group(6)), int(m.group(5)))
    check("READ pdf: the calendar's table gives 22 versions with 49, 50 and 51 on 12 January, 9 February and "
          "9 March 2027", len(rel) == 22 and rel.get(49) == dt.date(2027, 1, 12) and rel.get(50) == dt.date(2027, 2, 9)
          and rel.get(51) == dt.date(2027, 3, 9), len(rel))
    # ---- the thread (email, quoted-printable)
    body, msg = eml_body(os.path.join(t, "staffing_plan_q1_2027.eml"))
    flat = re.sub(r"\s+", " ", body.replace("> ", " ").replace(">", " "))
    check("READ eml: the thread files the expected load in the quarter's busiest week at 120 triage items per "
          "triager-week, rounding up, and the 13 weeks from Monday 4 January to Sunday 4 April",
          "expected load in the quarter's busiest week at 120 triage items per triager-week, rounding up" in flat
          and "13 weeks Mon 4 Jan to Sun 4 Apr" in flat and "Monday to Sunday, Helsinki time" in flat
          and msg["Date"].startswith("Thu, 17 Dec"))
    # ---- the runbook and the agreement (python-docx)
    rb = " ".join(docx_paras(os.path.join(t, "tracker_cutover_runbook.docx")))
    check("READ docx: the runbook files the counting basis (every report through the form, duplicates included; "
          "the security group out; moved reports stay items; whatever version)",
          "Every report filed through the report form is a triage item, duplicates included" in rb and
          "are not triage items" in rb and "stays a triage item" in rb and "whatever version the reporter runs" in rb)
    ag = " ".join(docx_paras(os.path.join(t, "triage_working_agreement.docx")))
    check("READ docx: the agreement files a triage action, the 24-hour target, closed, the weeks and the run's span",
          "A triage action is a change by one of the rota's triagers" in ag and "within 24 hours of its filing" in ag
          and "sits in another team's project" in ag and "Monday to Sunday, Helsinki time" in ag
          and "23:59 on Sunday 29 November" in ag)
    check("READ docx: the agreement counts a group's intake by the component a report comes in with, once",
          "each report counted once, in the group of the component it comes in with; a component set in triage does "
          "not change where a report arrived" in ag)
    check("READ docx: the runbook puts every form report and no other in the old tracker's export",
          "every report filed through the form there and no other, wherever the report sits now" in rb)
    check("READ: no shipped file describes the data (no dictionary, field notes, manifest or readme)",
          not [f for f in os.listdir(t) if re.search(r"read_?me|dictionar|manifest|_fields|field_?notes", f, re.I)])
    # ---- the old export
    ex = read_csv(t, "old_tracker_export_20251001_20261217.csv")
    check("READ csv: the old export has %d rows, every bug id once" % len(ex), len({r["bug_id"] for r in ex}) == len(ex)
          and len(ex) >= 25000)
    start, last = dt.date(2025, 10, 1), dt.date(2026, 12, 17)
    days = [start + dt.timedelta(days=i) for i in range((last - start).days + 1)]
    di = {d: i for i, d in enumerate(days)}
    plats = ("Windows", "macOS", "Linux")
    y = {p: np.zeros(len(days)) for p in plats}
    opened = {}
    zoned = 0
    for r in ex:
        o = dt.datetime.strptime(r["opened"][:19], "%Y-%m-%d %H:%M:%S")
        zoned += r["opened"][19:] in (" +0200", " +0300")
        opened[int(r["bug_id"])] = o
        if r["groups"]:
            continue
        p = "Windows" if r["op_sys"].startswith("Win") else ("macOS" if r["op_sys"].startswith("mac") else "Linux")
        y[p][di[o.date()]] += 1
    check("READ csv: every opened time carries a Helsinki offset (+0200 or +0300)", zoned == len(ex), zoned)
    ytot = sum(y.values())
    inst = {p: np.zeros(len(days)) for p in plats}
    for r in read_csv(t, "active_installs_daily.csv"):
        inst[r["platform"]][di[dt.date.fromisoformat(r["date"])]] = float(r["active_installs_thousands"]) * 1000
    shares = {p: [dict() for _ in days] for p in plats}
    for r in read_csv(t, "version_share_daily.csv"):
        shares[r["platform"]][di[dt.date.fromisoformat(r["date"])]][r["version"]] = float(r["share_pct"])
    # weekly items (complete weeks)
    wk = {}
    for i, d in enumerate(days):
        wk.setdefault(mon(d), []).append(ytot[i])
    wk = {w: sum(v) for w, v in wk.items() if len(v) == 7}
    a = sum(inst[p][-56:].sum() for p in plats)
    b = sum(inst[p][-56 - 364:-364].sum() for p in plats)
    growth = a / b
    q1 = {w: v for w, v in wk.items() if dt.date(2026, 1, 5) <= w <= dt.date(2026, 3, 30)}
    w1 = max(q1, key=q1.get)
    default = q1[w1] * growth
    check("DEFAULT last year's busiest first-quarter week (%s, %d items) times install growth %.4f files %.0f items, "
          "%d triagers" % (w1, q1[w1], growth, default, math.ceil(default / 120)), math.ceil(default / 120) == 6)
    # ---- the restart model, its own code: daily hazards by day kind, a weekly reports model
    pts = []
    for yy in (2025, 2026, 2027):
        for mm in range(1, 13):
            d = dt.date(yy, mm, 1)
            while d.weekday() != 1:
                d += dt.timedelta(days=1)
            pts.append(d + dt.timedelta(days=7))
    burst = {pt + dt.timedelta(days=1): 1 for pt in pts}
    burst.update({pt + dt.timedelta(days=2): 2 for pt in pts})
    rels = sorted((m, d) for m, d in rel.items() if start <= d <= last)

    def kind(d, p, reldays):
        if d in reldays:
            return "rel"
        if p == "Windows" and d in burst:
            return "b%d" % burst[d]
        if (d.month == 12 and d.day >= 21) or (d.month == 1 and d.day <= 3):
            return "ye"
        return "we" if d.weekday() >= 5 else "wd"

    reldays = {d for _, d in rel.items()}
    reach = {p: np.zeros(len(days)) for p in plats}
    haz = {p: {} for p in plats}
    for p in plats:
        for k, (m, d0) in enumerate(rels):
            d1 = rels[k + 1][1] if k + 1 < len(rels) else last + dt.timedelta(days=1)
            prev = sum(v for ver, v in shares[p][di[d0] - 1].items() if ver.split(".")[0] == str(m)) / 100 if di[d0] else 0
            d = d0
            while d < d1:
                s = sum(v for ver, v in shares[p][di[d]].items() if ver.split(".")[0] == str(m)) / 100
                r_ = max(0.0, s - prev)
                reach[p][di[d]] = r_
                if 1 - prev > 0.03:
                    haz[p].setdefault(kind(d, p, reldays), []).append(r_ / (1 - prev))
                prev = s
                d += dt.timedelta(days=1)
        haz[p] = {k: float(np.median(v)) for k, v in haz[p].items()}
    # weekly reports model: items = b x installs + r0 x reach installs + r1 x last week's
    rw, iw, yw = {}, {}, {}
    for i, d in enumerate(days):
        w = mon(d)
        rw[w] = rw.get(w, 0) + sum(reach[p][i] * inst[p][i] for p in plats)
        iw[w] = iw.get(w, 0) + sum(inst[p][i] for p in plats)
        yw[w] = yw.get(w, 0) + ytot[i]
    ws_ = sorted(w for w in wk if w - dt.timedelta(days=7) in rw)
    X = np.array([[iw[w], rw[w], rw[w - dt.timedelta(days=7)]] for w in ws_])
    coef = np.linalg.lstsq(X, np.array([yw[w] for w in ws_]), rcond=None)[0]
    # forward: installs a year earlier times growth; adoption of the as-of version, then 49, 50, 51
    fdays = [last + dt.timedelta(days=i) for i in range(1, (dt.date(2027, 4, 4) - last).days + 1)]
    finst = {p: np.array([inst[p][di[d - dt.timedelta(days=364)]] for d in fdays]) *
             (inst[p][-56:].sum() / inst[p][-56 - 364:-364].sum()) for p in plats}
    last_m = max(m for m, d in rels)
    fwd = sorted((m, d) for m, d in rel.items() if last < d <= fdays[-1])
    freach = np.zeros(len(fdays))
    for p in plats:
        pend = 1 - sum(v for ver, v in shares[p][-1].items() if ver.split(".")[0] == str(last_m)) / 100
        cur = last_m
        for i, d in enumerate(fdays):
            for m, d0 in fwd:
                if d == d0:
                    cur, pend = m, 1.0
            h = haz[p].get(kind(d, p, {d0 for _, d0 in fwd}), haz[p]["wd"])
            x = pend * h
            pend -= x
            freach[i] += x * finst[p][i]
    frw, fiw = {}, {}
    for i, d in enumerate(fdays):
        w = mon(d)
        frw[w] = frw.get(w, 0) + freach[i]
        fiw[w] = fiw.get(w, 0) + sum(finst[p][i] for p in plats)
    q1w = [dt.date(2027, 1, 4) + dt.timedelta(days=7 * k) for k in range(13)]
    fc = {w: coef[0] * fiw[w] + coef[1] * frw[w] + coef[2] * frw.get(w - dt.timedelta(days=7), 0) for w in q1w}
    bw = max(fc, key=fc.get)
    tri = math.ceil(fc[bw] / 120)
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    check("CALL the verifier's own restart model (median hazards, weekly reports model) files %d triagers with the "
          "busiest week at %.0f items, 900 to the nearest 100" % (tri, fc[bw]),
          tri == figs["call"]["triagers"] == 8 and 850 <= fc[bw] < 950 and figs["call"]["busiest_week"] == "900")
    check("CALL the Windows hazards the verifier reads: about %.0f and %.0f per cent on the Wednesday and Thursday after "
          "Patch Tuesday, %.0f on ordinary weekdays" % (100 * haz["Windows"]["b1"], 100 * haz["Windows"]["b2"],
                                                       100 * haz["Windows"]["wd"]),
          haz["Windows"]["b1"] > 0.5 and haz["Windows"]["b2"] > 0.35 and haz["Windows"]["wd"] < 0.15)
    # ---- the asks, on their own code path
    jd = json.load(open(os.path.join(t, "newtracker_parallel_run_export.json"), encoding="utf-8"))
    issues = jd["issues"]
    check("READ json: %d issues, keys unique, every history with an author and items" % len(issues),
          len({i["key"] for i in issues}) == len(issues) == jd["total"] and
          all(h["author"]["displayName"] and h["items"] for i in issues for h in i["changelog"]["histories"]))
    rota = xlsx_rows(os.path.join(t, "triage_rota_2026-11.xlsx"), "Rota")
    triagers = set()
    for r in rota[3:]:
        if r[3]:
            triagers |= {x.strip() for x in r[3].split(",")}
    check("READ xlsx: the rota names six triagers", len(triagers) == 6, sorted(triagers))
    reg = xlsx_rows(os.path.join(t, "component_groups.xlsx"), "Component groups")
    group = {r[1]: r[0] for r in reg[4:] if r[0] and r[1] and r[0] != "Not in a group"}
    check("READ xlsx: the register maps %d components to eight groups" % len(group), len(set(group.values())) == 8)
    dash = xlsx_rows(os.path.join(t, "triage_dashboard_weekly.xlsx"), "Weekly")
    check("READ xlsx: the dashboard's weeks run from 29.9.2025", isinstance(dash[5][0], dt.datetime) and
          dash[5][0].date() == dt.date(2025, 9, 29))

    def utc_local(s):
        return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(hours=2)

    def old_number(i):
        f = i["fields"]
        if f.get("customfield_10410") is not None:
            return int(f["customfield_10410"])
        for h in i["changelog"]["histories"]:
            for x in h["items"]:
                if x["field"] == "Legacy bug" and x["toString"]:
                    return int(x["toString"])
        for lab in f.get("labels") or []:
            m = re.fullmatch(r"legacy-(\d+)", lab)
            if m:
                return int(m.group(1))
        return None

    end = dt.datetime(2026, 11, 29, 23, 59, 59)
    first = {}
    for i in sorted(issues, key=lambda i: (i["fields"]["created"], int(i["id"]))):
        f = i["fields"]
        came_from_brw = f["project"]["key"] == "BRW" or any(
            x["field"] == "project" and x["fromString"] == "Browser intake"
            for h in i["changelog"]["histories"] for x in h["items"])
        if f["issuetype"]["name"] != "Bug" or f["security"] or not came_from_brw:
            continue
        n = old_number(i)
        if n is None or n not in opened or n in first:
            continue
        if not (dt.datetime(2026, 11, 2) <= opened[n] < dt.datetime(2026, 11, 30)):
            continue
        first[n] = i
    weeks = [dt.date(2026, 11, 2) + dt.timedelta(days=7 * k) for k in range(4)]
    no_act = {w: 0 for w in weeks}
    closed = {w: 0 for w in weeks}
    arrived = {}
    for n, i in first.items():
        w = mon(opened[n].date())
        hs = sorted(i["changelog"]["histories"], key=lambda h: (h["created"], int(h["id"])))
        acts = [utc_local(h["created"]) for h in hs if h["author"]["displayName"] in triagers and
                any(x["field"] in ("status", "resolution", "Component", "priority", "project") for x in h["items"])]
        if not acts or acts[0] - opened[n] > dt.timedelta(hours=24):
            no_act[w] += 1
        st = proj = None
        for h in hs:
            if utc_local(h["created"]) > end:
                break
            for x in h["items"]:
                st = x["toString"] if x["field"] == "status" else st
                proj = x["toString"] if x["field"] == "project" else proj
        if st in ("Resolved", "Closed") or proj == "Web compatibility":
            closed[w] += 1
        comps = [c["name"] for c in i["fields"]["components"]]
        for h in reversed(hs):
            for x in reversed(h["items"]):
                if x["field"] == "Component":
                    if x["toString"] in comps:
                        comps.remove(x["toString"])
                    if x["fromString"]:
                        comps.append(x["fromString"])
        for g in {group.get(c) for c in comps} - {None}:
            arrived[g] = arrived.get(g, 0) + 1
    exp_a = [(r["no_action"], r["closed"]) for r in figs["answers"]["ask_a"]]
    got_a = [(no_act[w], closed[w]) for w in weeks]
    check("ASK A the verifier's count matches the golden in every week: %s" % got_a, exp_a == got_a)
    check("ASK B the verifier's arrivals match the golden in every group: %s" % arrived,
          all(arrived.get(g, 0) == v for g, v in figs["answers"]["ask_b"].items()))
    print("verify: %d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
