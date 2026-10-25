"""task170 independent verifier: its own readers (the csv module, openpyxl, pypdf), its own clock rule, its own count
of each driver's starts and its own placement of every error; the go-live dates read from the rollout plan's table.
Recomputes every graded figure in figures.json from target/ alone. Exit 1 on a mismatch.

    python3 task170/generator/verify.py [target]"""
from __future__ import annotations

import bisect
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
P4 = ["GLH", "DRC", "KVN", "ADM", "MSB", "FBK"]
REC = ["BRN", "TLM", "ALR", "KDB", "MWB", "FNJ", "SNH", "CNC"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def xrows(path):
    ws = openpyxl.load_workbook(path, read_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    return [dict(zip(head, v)) for v in it]


def summer(t_utc):
    """European summer time: from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of October"""
    def last_sun(y, m):
        d = dt.date(y, m, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return dt.datetime(d.year, d.month, d.day, 1)
    return last_sun(t_utc.year, 3) <= t_utc < last_sun(t_utc.year, 10)


def to_local(t_utc):
    return t_utc + dt.timedelta(hours=1) if summer(t_utc) else t_utc


def to_utc(t_local):
    c = t_local - dt.timedelta(hours=1)
    return c if summer(c) else t_local


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    P = lambda f: os.path.join(target, f)
    bad = []
    nxt = {r["old_staff_no"]: r["new_staff_no"] for r in rows(P("staff_number_crosswalk.csv"))}

    def person(s):
        while s in nxt:
            s = nxt[s]
        return s
    # each driver's starts in time order
    times = defaultdict(list)
    ref_at = {}
    for r in rows(P("obr_start_of_mission_log_2024-03_2026-10.csv")):
        if r["som_type"] == "TST":
            continue
        t = dt.datetime.strptime(r["obr_utc"], "%Y-%m-%dT%H:%M:%SZ")
        times[person(r["driver_id"])].append((t, r["som_ref"]))
    for p in times:
        times[p].sort()
        for n, (t, ref) in enumerate(times[p]):
            ref_at[ref] = (p, n)
    tonly = {p: [t for t, _ in v] for p, v in times.items()}
    T = defaultdict(int)
    for p, v in times.items():
        for n in range(len(v)):
            T[n] += 1
    # errors
    reg = xrows(P("safety_desk_register_2024-2026.xlsx"))
    tde = [r for r in reg if r["Category"] == "TDE" and r["Status"] != "Withdrawn"]
    link_ref = {}
    for r in tde:
        if r["Linked To"] and r["SoM Ref"]:
            link_ref.setdefault(r["Linked To"], r["SoM Ref"])
    E = defaultdict(int)
    nerr = 0
    for r in tde:
        if r["Linked To"]:
            continue
        nerr += 1
        ref = r["SoM Ref"] or link_ref.get(r["Report No"])
        if ref and ref in ref_at:
            E[ref_at[ref][1]] += 1
            continue
        p = person(str(r["Staff No"]))
        k = bisect.bisect_right(tonly.get(p, []), to_utc(r["Received"])) - 1
        if k < 0:
            bad.append("error %s not placed" % r["Report No"])
            continue
        E[k] += 1
    edges = list(range(0, 650, 50))
    rate = []
    for i in range(len(edges)):
        a = edges[i]
        b = edges[i + 1] if i + 1 < len(edges) else 10 ** 9
        st = sum(v for n, v in T.items() if a <= n < b)
        er = sum(v for n, v in E.items() if a <= n < b)
        rate.append(er / st)

    def p_of(n):
        return rate[min(n // 50, len(rate) - 1)]
    # the Phase 4 drivers and their starts
    roster = xrows(P("driver_roster_2026-10-31.xlsx"))
    p4 = [(str(r["Staff No"]), r["Depot"]) for r in roster if r["Depot"] in P4]
    latest = {}
    for r in rows(P("phase4_duty_records_2026.csv")):
        if r["status"] != "Worked":
            continue
        k = (r["duty_date"], r["staff_no"], r["duty_no"])
        if k not in latest or int(r["issue"]) > latest[k][0]:
            latest[k] = (int(r["issue"]), int(r["cab_activations"]))
    act = defaultdict(int)
    for (day, staff, duty), (iss, ca) in latest.items():
        act[person(staff)] += ca
    total, starts = 0.0, 0.0
    for staff, depot in p4:
        pp = person(staff)
        prior = len(times.get(pp, []))
        nn = act[pp] * 1.2
        starts += nn
        whole = int(nn)
        total += sum(p_of(prior + j) for j in range(whole)) + (nn - whole) * p_of(prior + whole)
    if int(250 * round(total / 250.0)) != figs["call_tde_errors_phase4_first_12_months"]:
        bad.append("call %.1f" % total)
    if len(p4) != figs["cc1_phase4_drivers"]:
        bad.append("drivers %d" % len(p4))
    if int(1000 * round(starts / 1000.0)) != figs["cc2_phase4_etcs_starts_first_12_months"]:
        bad.append("starts %.1f" % starts)
    if nerr != figs["_path"]["tde_errors_recorded"]:
        bad.append("errors %d" % nerr)
    # go-live dates from the rollout plan's table
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(P("etcs_rollout_plan_2024-2027.pdf")).pages)
    golive = {}
    for code in P4 + REC:
        m = re.search(r"\b%s\s+(\d{1,2}) (\w+) (\d{4})" % code, txt)
        if not m:
            bad.append("go-live of %s not in the plan" % code)
            continue
        golive[code] = dt.datetime.strptime("%s %s %s" % m.groups(), "%d %B %Y").date()
    # ask A
    form = {r["unit"]: (r["vehicle_a_end"], r["vehicle_b_end"]) for r in rows(P("unit_formations_2026-10-31.csv"))}
    when = {}
    for r in xrows(P("etcs_fitment_works_records.xlsx")):
        v = r["Accepted"] or r["Planned Acceptance"]
        when[str(r["Vehicle"])] = v.date() if hasattr(v, "date") else v
    acc = defaultdict(lambda: [0, 0])
    for r in rows(P("fleet_allocation_2027.csv")):
        a, b = form[r["unit"]]
        okk = when.get(a) and when.get(b) and when[a] <= golive[r["depot"]] and when[b] <= golive[r["depot"]]
        acc[r["depot"]][0 if okk else 1] += 1
    for c in P4:
        if tuple(acc[c]) != (figs["ask_units_accepted_by_golive_%s" % c.lower()], figs["ask_units_not_accepted_by_golive_%s" % c.lower()]):
            bad.append("units %s %s" % (c, acc[c]))
    # ask C
    lo, hi = dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1)
    ev = []
    for r in reg:
        if r["Category"] not in ("LTR", "BRK") or r["Status"] == "Withdrawn" or r["Linked To"]:
            continue
        t = r["Received"]
        is_obr = r["Reporter"] == "OBR download"
        if is_obr:
            t = to_local(t)
        if lo <= t < hi:
            ev.append((str(r["Staff No"]), str(r["Unit"]), r["Category"], t, is_obr, r["Depot"]))
    manual = defaultdict(list)
    for i, x in enumerate(ev):
        if not x[4]:
            manual[(x[0], x[1], x[2])].append((x[3], i))
    for k in manual:
        manual[k].sort()
    used, drop = set(), set()
    for i, x in sorted(enumerate(ev), key=lambda z: z[1][3]):
        if not x[4]:
            continue
        for t, j in manual.get((x[0], x[1], x[2]), []):
            m = (t - x[3]).total_seconds() / 60.0
            if 0 <= m <= 30 and j not in used:
                used.add(j)
                drop.add(i)
                break
    cnt = defaultdict(lambda: [0, 0])
    for i, x in enumerate(ev):
        if i not in drop:
            cnt[x[5]][0 if x[2] == "LTR" else 1] += 1
    for c in REC:
        if tuple(cnt[c]) != (figs["ask_level_transition_errors_2026_%s" % c.lower()], figs["ask_brake_interventions_2026_%s" % c.lower()]):
            bad.append("events %s %s" % (c, cnt[c]))
    print("verify: call %.1f -> %d, drivers %d, starts %.1f, %d errors placed, %d graded figures checked, %d failed%s"
          % (total, int(250 * round(total / 250.0)), len(p4), starts, nerr, 3 + 12 + 16, len(bad),
             (": " + "; ".join(bad[:8])) if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
