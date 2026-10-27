"""Generator checks for task281, run on every build: the call against the world, the golden's family, the ladder,
the three rules (R1 to R3), each Layer 1 item mishandled, the semantic fork rows, the separation of the asks' devices
from the call, the asks' devices against their stops, the input gates and the realism sweep."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import math
import os
import re

import numpy as np

import analysis as A
import asks as AK
import common as K
import pack as PK

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))


def pdf_text(path):
    import subprocess
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return ""


def counts_with(pk, off, a1_of, after_of, weeks="fiscal", cut=K.K_WEEKS, rounding="ceil"):
    out = []
    for u in K.UNIT_CODES:
        if weeks == "fiscal":
            Au = np.zeros(K.WEEKS)
            for r in pk.roster:
                if r["unit_code"] == u and r["cat"] in off:
                    w = K.fweek(PK.Pack.day_index(r["shift_date"]))
                    if w:
                        Au[w - 1] += 8.0
        a = a1_of(u)
        need = Au + A.vacancy(pk.new_lines(u), after_of(u, a))
        x = np.sort(need)[::-1][cut] / (K.WEEK_H * a)
        out.append(int(np.ceil(x - 1e-9)) if rounding == "ceil" else int(round(x)))
    return out


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w, rc, py = b["w"], b["rc"], b["py"]
    pk = res["pk"]
    c = res["call"]
    cnt = c["counts"]
    gold = cnt[A.GOLDEN]
    U = K.UNIT_CODES

    # ------------------------------------------------------------------ the call against the world
    truth = []
    for u in U:
        t = K.UNIT_TITLE[u]
        js = [j for j, ln in enumerate(w.lines) if ln["unit"] == u]
        Aw = np.zeros(K.WEEKS)
        for j in js:
            for i in range(K.WEEKS * 7):
                if w.on[j, i] and w.status[j, i] in ("VAC", "SICK", "IOD", "TRN", "FMLA", "MIL"):
                    Aw[i // 7] += 8.0
        sched = off = 0
        for jj, ln in enumerate(w.lines):
            if K.UNIT_TITLE[ln["unit"]] != t:
                continue
            for i in range(K.FY26_DAYS):
                e = w.holder[jj, i]
                if w.on[jj, i] and e >= 0 and w.people[e]["cls"] == "2025-1":
                    sched += 1
                    off += w.status[jj, i] != "W"
        a1 = 1 - off / sched
        v = A.vacancy([(x["line_id"], x["first"], x["off"]) for x in rc.new_line_ids() if x["unit"] == u], 1 - a1)
        truth.append(int(np.ceil(A.q5(Aw + v) / (40 * a1) - 1e-9)))
    ok("CALL golden equals the world's placement", gold == truth, "%s vs %s" % (gold, truth))
    ok("CALL 59 of the 60 placed, one returned", sum(gold) == 59 and fig["call"]["returned_to_reserve"] == 1,
       str(sum(gold)))
    for k in A.FAMILY:
        ok("FAMILY %s places the golden counts" % k, cnt[k] == gold, str(cnt[k]))
    edge = min(min(r - np.floor(r), np.ceil(r) - r) for k in A.FAMILY for r, _ in c["table"][k].values())
    ok("MARGIN every family member sits 0.15 or more from a whole position on every unit", edge >= 0.15,
       "%.3f" % edge)

    # ------------------------------------------------------------------ the ladder
    want = {"mean": 38, "R1": 62, "R2t": 63, "R2": 64, "R3": 57, "R4": 50, "R5": 52, "R6": 67}
    for k in A.RUNGS:
        diff = sum(a != g for a, g in zip(cnt[k], gold))
        ok("LADDER %s files another placement (%d units differ, total %d)" % (k, diff, sum(cnt[k])),
           cnt[k] != gold and diff >= 3 and sum(cnt[k]) == want[k], str(cnt[k]))
    ok("LADDER the default path (R2t, the titles' average officers) is three short of the 60",
       sum(cnt["R2t"]) - K.FUNDED == 3, str(sum(cnt["R2t"])))
    ok("LADDER the default path places other counts on four units",
       sum(a != g for a, g in zip(cnt["R2t"], gold)) == 4, str(cnt["R2t"]))

    # ------------------------------------------------------------------ the three rules
    with open(os.path.join(target, K.FILES["rosters"]), newline="") as fh:
        head = next(csv.reader(fh))
    ok("R1 the rosters ship one row a scheduled line-shift with its holder and status",
       head[:3] == ["shift_date", "unit_code", "line_id"] and "employee_id" in head and "status_code" in head)
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), newline="") as fh:
                heads += next(csv.reader(fh))
    ok("R1 no shipped column holds an availability, a weekly need or a complement",
       not [h for h in heads if re.search(r"avail|need|relief|complement|net_hours|factor", h)], str(len(heads)))
    ok("R1 the decisive estimate reads the July 2025 classes' own roster rows",
       sum(1 for r in pk.roster if r["employee_id"] and pk.emp[r["employee_id"]]["academy_class"].endswith(" 2025-1"))
       > 3000)
    pk_dup = PK.Pack(target, dedupe=False)
    ok("R2 Layer 1: the February re-run rows counted twice leave the call", A.call(pk_dup)["counts"]["G"] == gold,
       str(len(pk_dup.roster) - len(pk.roster)))
    pk_cur = PK.Pack(target)
    pk_cur.emp = {e: v[0] for e, v in pk_cur.emp_hist.items()}
    ok("R2 Layer 1: HR's title rows read first or last leave the call", A.call(pk_cur)["counts"]["G"] == gold)
    pk_sl = PK.Pack(target, map_shiftlink=False)
    ok("R2 Layer 1: Thornmere's ShiftLink codes left unread leave the call", A.call(pk_sl)["counts"]["G"] == gold)
    ok("R2 Layer 1: the payroll is not read by the call (no payroll field in the placement)",
       "payroll" not in open(os.path.join(os.path.dirname(__file__), "analysis.py")).read().split("import pack")[1])
    ok("R3a analyst test: every rule applied with the title's average officer files 63, not 59",
       sum(cnt["R2t"]) == 63 and cnt["R2t"] != gold)
    ok("R3b the decisive step alone (R2t with the first-year availability) files the golden", cnt["G"] == gold)
    ok("R3b the vacancy rung alone (R1 to R2) stays off the golden", cnt["R2"] != gold and cnt["R1"] != gold)
    ok("R3b the availability alone on last year's vacancies (R3) stays off the golden", cnt["R3"] != gold)
    seqs = {}
    for r in pk.roster:
        seqs.setdefault(r["line_id"], []).append(r["status_code"])
    dup_lines = len(seqs) - len({tuple(v) for v in seqs.values()})
    ok("R3c no line's year of statuses is a copy of another's", dup_lines == 0, str(dup_lines))
    wk = [tuple(c["comp"][u]["A"]) for u in U]
    ok("R3c no two units carry the same weekly off-post series", len(set(wk)) == len(wk))
    memo = pdf_text(os.path.join(target, K.FILES["memo"])) + pdf_text(os.path.join(target, K.FILES["standard"]))
    ok("R3c no document carries a placement figure or a wrong total",
       not re.search(r"\b(38|50|52|57|62|64|67)\b", memo), "")

    # ------------------------------------------------------------------ semantic fork rows
    a1t = {u: c["comp"][u]["a1"] for u in U}
    ok("SF1 the July 2025 classes by title, by unit or as one class place the same counts",
       cnt["G"] == cnt["G_unit"] == cnt["G_class"])
    ok("SF2 every FY2026 first-year holder (mid-year classes in) places the same counts", cnt["G_first"] == gold)
    ok("SF3 pooled hours or the mean of members' shares place the same counts", cnt["G_ratios"] == gold)
    ok("SF4 a new line's holder after the first shift: first-year, none or the unit average, same counts",
       cnt["G_none"] == gold and cnt["G_avg"] == gold)
    std = pdf_text(os.path.join(target, K.FILES["standard"]))
    flat = re.sub(r"\s+", " ", std)
    alt4 = counts_with(pk, PK.OFF_POST, lambda u: a1t[u], lambda u, a: 40 * (1 - a), cut=3)
    ok("SF5 the fifth-heaviest week is filed (3.1, 3.2); the fourth would place other counts",
       "every week of the year planned for but four" in flat and "fifth-heaviest week" in flat and alt4 != gold,
       str(alt4))
    alt_r = counts_with(pk, PK.OFF_POST, lambda u: a1t[u], lambda u, a: 40 * (1 - a), rounding="round")
    ok("SF6 the smallest whole number reaching the need is filed (3.2); rounding would place other counts",
       "smallest whole number of relief positions" in flat and alt_r != gold, str(alt_r))
    ok("SF7 fiscal weeks from 1 July, leftover days in no week, are filed (2.2)",
       "seven days counted from 1 July" in flat and "belong to no week" in flat)
    off2 = tuple(x for x in PK.OFF_POST if x != "Training")
    ok("SF8 training away from the post is off post (2.3(a)) and the status table says so",
       "in training away from the post" in flat and
       any(r["state_category"] == "Training" and "off post" in r["description"].lower()
           for r in PK.rows(os.path.join(target, K.FILES["codes"]))), str(off2))
    ok("SF9 a line vacated during the year is outside the need (2.4)",
       "falls vacant during the year" in flat and "not sized for it" in flat)
    ok("SF10 the re-run rows counted once or twice place the same counts", A.call(pk_dup)["counts"]["G"] == gold)
    ok("SF11 Thornmere's ShiftLink rows read or left place the same counts", A.call(pk_sl)["counts"]["G"] == gold)
    memo_t = re.sub(r"\s+", " ", pdf_text(os.path.join(target, K.FILES["memo"])))
    ok("SF12 positions not needed return to the reserve; a shortfall is reported (memo)",
       "the rest return to the Governor's reserve" in memo_t and "how many more" in memo_t)
    ok("SF13 the year planned for is FY2028, the last closed year FY2026 (memo, 2.1)",
       "on the FY2026 rosters, our last closed year" in memo_t and "FY2028 position control" in memo_t)
    ok("SF14 the standard files no grain for a relief position's hours; by title or by unit the same counts, and the "
       "positions are filled from the July 2027 entry classes (memo)",
       "reckoned by title" not in flat and cnt["G_unit"] == gold and "July 2027 entry classes" in memo_t)

    # ------------------------------------------------------------------ separation of the asks from the call
    pk_np = PK.Pack(target)
    pk_np.payroll, pk_np.earn, pk_np.offers = [], [], []
    ok("SEP the call reads no payroll line and no offer: dropping both leaves the placement",
       A.call(pk_np)["counts"]["G"] == gold)
    dev = len(AK.repeats(pk)) + sum(1 for r in pk.offers if r["response"] == "Accepted")
    ok("SEP the asks' device rows sit in the payroll, the offer log and HR's rows outside the July 2025 classes",
       dev > 3000, str(dev))
    ch = AK.chains(pk)
    ok("SEP the rehired officers hold no July 2025 class record",
       all(not pk.emp[e]["academy_class"].endswith("2025-1") and not pk.emp[o]["academy_class"].endswith("2025-1")
           for e, o in ch.items()))
    movers = [e for e, v in pk.emp_hist.items() if len(v) > 1]
    ok("SEP the officers who changed title hold no July 2025 class record",
       all(not pk.emp[e]["academy_class"].endswith("2025-1") for e in movers), str(len(movers)))

    # ------------------------------------------------------------------ the asks' filed readings (SF16 to SF18)
    g = res["asks"]
    agr = re.sub(r"\s+", " ", pdf_text(os.path.join(target, K.FILES["agreement"])))
    pay_head = open(os.path.join(target, K.FILES["payroll"]), encoding="utf-8").readline().strip().split(",")
    off_head = open(os.path.join(target, K.FILES["offers"]), encoding="utf-8").readline().strip().split(",")
    ok("SF16 the payroll's own headers key every line to the employee's home timekeeper and cost center, the offer "
       "log names the post's unit, and MOU 14.3 holds over and calls in the unit's own employees",
       "home_timekeeper" in pay_head and "home_cost_center" in pay_head and "post_unit" in off_head and
       "employees of the same title at the State's other units may also join" in agr and
       "the unit holds over its junior employee on duty or calls in its junior employee off duty" in agr)
    def home_on(e, d):
        for x in pk.emp_hist.get(e, []):
            if x["title_effective_from"] <= d and (not x["title_effective_to"] or d <= x["title_effective_to"]):
                return x["home_unit"]
        return pk.emp[e]["home_unit"]
    hu = {}
    for r in pk.payroll:
        if r[AK.HOME] and r["work_date"]:
            hu.setdefault(r[AK.HOME], set()).add(home_on(r["employee_id"], r["work_date"]))
    ok("SF16 every line's home timekeeper is its employee's home unit in HR (SL-0410 Thornmere's employees only)",
       all(v == {AK.LOC.get(k, k)} for k, v in hu.items()), str({k: sorted(v) for k, v in hu.items()}))
    home = {e: p["unit"] for e, p in enumerate(w.people)}
    fy_ev = [ev for ev in py.events if K.FY26_START <= ev["date"] <= dt.date(2026, 6, 30)]
    ok("SF16 every piece not offered was worked at the employee's own unit, and every piece worked at another unit "
       "was offered", all(ev["vol"] or ev["unit"] == home[ev["e"]] for ev in fy_ev) and
       all(ev["vol"] for ev in fy_ev if ev["unit"] != home[ev["e"]]), str(len(fy_ev)))
    acc = [r for r in pk.offers if r["response"] == "Accepted"]
    key3 = {(r["employee_id"], r["post_date"], r["start_time"]): r["post_unit"] for r in acc}
    ok("SF16 an accepted offer is one piece: employee, date and start repeat in no two acceptances",
       len(key3) == len(acc), "%d acceptances" % len(acc))
    rep = AK.repeats(pk)
    canon = {old: new for new, old in AK.chains(pk).items()}
    lit_a, lit_b = collections.defaultdict(float), collections.defaultdict(set)
    for n, r in enumerate(pk.payroll):
        if r["earn_code"] not in ("OT",) + tuple(AK.COMP) or not AK.in_fy(r["work_date"]):
            continue
        u = key3.get((r["employee_id"], r["work_date"], r["start_time"]))
        u = u or AK.LOC.get(r[AK.HOME], r[AK.HOME])
        lit_b[u].add(canon.get(r["employee_id"], r["employee_id"]))
        if n not in rep:
            lit_a[u] += AK.hours_worked(r, True, False, False, AK.credit(pk, r))
    ok("SF16 the literal reading (the accepted offer's unit by employee, date and start, else the own unit) gives "
       "the golden hours and people", {u: int(round(lit_a[u])) for u in U} == g["a"] and
       {u: len(lit_b[u]) for u in U} == g["b"])
    wt = collections.defaultdict(float)
    for ev in fy_ev:
        wt[ev["unit"]] += ev["hours"]
    ok("SF16 the golden hours are the hours the world worked at each unit", {u: int(round(wt[u])) for u in U} == g["a"],
       str({u: int(round(wt[u])) for u in U}))
    ok("SF16 a join on a compensatory line's credited hours as if worked leaves its piece at the own unit, ruled out "
       "by MOU 14.2 and the codes", AK.ask_a(pk, cte="raw") != g["a"])
    earn = {r["earn_code"]: r["description"] for r in pk.earn}
    cts = [r for r in pk.payroll if r["earn_code"] == "CTS"]
    ok("SF17 the aides' compensatory time carries its own code, credited hour for hour; at 1.5 the forensic hospital "
       "moves", earn.get("CTS") == "Comp time earned 1.0" and earn.get("CTE") == "Comp time earned 1.5" and
       cts and all(pk.title_on(r["employee_id"], r["work_date"]) == "FSA" for r in cts) and
       not [r for r in pk.payroll if r["earn_code"] == "CTE" and pk.title_on(r["employee_id"], r["work_date"]) == "FSA"]
       and AK.ask_a(pk, flat=True)["FFH"] != g["a"]["FFH"], "%d CTS lines" % len(cts))
    no_cte = collections.defaultdict(set)
    for r in pk.payroll:
        if r["earn_code"] == "OT" and AK.in_fy(r["work_date"]):
            u = key3.get((r["employee_id"], r["work_date"], r["start_time"]))
            no_cte[u or AK.LOC.get(r[AK.HOME], r[AK.HOME])].add(canon.get(r["employee_id"], r["employee_id"]))
    ok("SF18 compensatory time is elected instead of overtime pay (MOU 14.2), so its holder worked overtime; counting "
       "OT lines only moves the people", "elect compensatory time instead of overtime pay" in agr and
       {u: len(no_cte[u]) for u in U} != g["b"])
    ok("GATE no file under target/ describes the data (dictionary, readme, notes, manifest)",
       not [f for f in os.listdir(target) if re.search(r"dictionar|readme|notes|manifest|codebook", f, re.I)])

    # ------------------------------------------------------------------ the asks' devices
    for name, kw, need in (("A by the keying timekeeper, the offer log unread", dict(offers=False), 6),
                           ("A a timesheet paid twice counted twice", dict(drop_repeats=False), 8),
                           ("A compensatory time read as worked hours", dict(cte="raw"), 7),
                           ("A compensatory time left out", dict(cte=False), 8),
                           ("A night differential hours counted", dict(otn=True), 8),
                           ("A compensatory time at 1.5 for every title", dict(flat=True), 1)):
        v = AK.ask_a(pk, **kw)
        n = sum(v[u] != g["a"][u] for u in U)
        ok("DEVICE %s moves %d of 8 units" % (name, n), n >= need, str(n))
    v = AK.ask_a(pk, flat=True)
    ok("DEVICE A the aides' compensatory time at 1.5 moves the forensic hospital", v["FFH"] != g["a"]["FFH"],
       "%d against %d" % (v["FFH"], g["a"]["FFH"]))
    v = AK.ask_a(pk, dedupe_all=True)
    ok("FAIR A: dropping every repeated piece key drops only the second payments",
       all(v[u] == g["a"][u] for u in U))
    for name, kw, need in (("B records counted as people", dict(merge=False), 4),
                           ("B by the keying timekeeper, the offer log unread", dict(offers=False), 6)):
        v = AK.ask_b(pk, **kw)
        n = sum(v[u] != g["b"][u] for u in U)
        ok("DEVICE %s moves %d of 8 units" % (name, n), n >= need, str(n))
    v = AK.ask_b(pk, offers=False, merge=False)
    ok("DEVICE B both unread moves every unit", all(v[u] != g["b"][u] for u in U), str(v))
    for name, kw, need in (("C records counted as people", dict(merge=False), 2),
                           ("C a timesheet paid twice counted twice", dict(drop_repeats=False), 1),
                           ("C titles from HR's latest row", dict(title="current"), 2),
                           ("C night differential hours counted", dict(otn=True), 2),
                           ("C compensatory time left out", dict(cte=False), 1)):
        v = AK.ask_c(pk, **kw)
        n = sum(v[t] != g["c"][t] for t in K.TITLE_ORDER)
        ok("DEVICE %s moves %d of 4 titles" % (name, n), n >= need, str(v))
    near = sorted(h for h in g["hours"].values() if 590 <= h <= 610)
    ok("ASK C no person within 10 hours of 600 on the golden handling", not near, str(near))
    ph = AK.person_hours(pk, merge=False)
    parts = [(ph.get(o, 0), ph.get(e, 0)) for e, o in ch.items()]
    ok("ASK C four rehires joined by seniority date, each record under 600 and each person over it",
       len(ch) == 4 and all(a < 600 and b < 600 and a + b > 615 for a, b in parts), str(parts))
    ok("ASK C a rehire in every title", sorted({pk.emp[e]["title_code"] for e in ch}) == sorted(K.TITLE_ORDER),
       str(sorted({pk.emp[e]["title_code"] for e in ch})))
    gaps = []
    for e, o in ch.items():
        days = (dt.date.fromisoformat(pk.emp[e]["hire_date"]) - dt.date.fromisoformat(pk.emp[o]["separation_date"])).days
        worked = [r for r in pk.payroll if r["employee_id"] in (e, o) and r["work_date"] and
                  pk.emp[o]["separation_date"] < r["work_date"] < pk.emp[e]["hire_date"]]
        rost = [r for r in pk.roster if r["employee_id"] in (e, o) and
                pk.emp[o]["separation_date"] < r["shift_date"] < pk.emp[e]["hire_date"]]
        gaps.append((days, len(worked), len(rost)))
    ok("REAL no rehire worked, was rostered or was paid between leaving and coming back",
       all(w_ == 0 and r_ == 0 for _, w_, r_ in gaps), str(gaps))
    ok("FAIR every rehire's restored seniority date matches one earlier record only",
       all(sum(1 for v in pk.emp.values() if v["seniority_date"] == pk.emp[e]["seniority_date"] and
               v["separation_date"] and v["separation_date"] < pk.emp[e]["hire_date"] and
               v["title_code"] == pk.emp[e]["title_code"]) == 1 for e in ch))
    retro = [r for r in pk.payroll if r["earn_code"] == "OTR"]
    rep = AK.repeats(pk)
    tie = 0
    ot = {}
    for n_, r in enumerate(pk.payroll):
        if r["earn_code"] == "OT":
            ot.setdefault(r["employee_id"], []).append((r["work_date"], float(r["hours"])))
    for r in retro:
        s_ = sum(h for d, h in ot.get(r["employee_id"], []) if r["service_period_start"] <= d <= r["service_period_end"])
        tie += abs(s_ - float(r["hours"])) < 1e-6
    ok("FAIR every retroactive line's hours are the hours of the overtime lines paid for its service period",
       tie == len(retro),
       "%d of %d" % (tie, len(retro)))
    pays = {}
    for n_, r in enumerate(pk.payroll):
        if n_ in rep:
            pays.setdefault(AK.piece_key(r), []).append(r["check_date"])
    first = {}
    for n_, r in enumerate(pk.payroll):
        if n_ not in rep and r["earn_code"] in ("OT", "OTN") + tuple(AK.COMP):
            first.setdefault(AK.piece_key(r), []).append(r["check_date"])
    ok("FAIR every second payment repeats a piece paid once before on an earlier check",
       all(len(first.get(k, [])) == 1 and min(v) > first[k][0] for k, v in pays.items()), str(len(rep)))
    acc = AK.worked_unit(pk)
    keys = [(r["employee_id"], r["post_date"], r["start_time"], r["hours"]) for r in pk.offers if r["response"] == "Accepted"]
    ok("FAIR every accepted offer names one piece", len(keys) == len(set(keys)), str(len(keys)))
    pieces = {(r["employee_id"], r["work_date"], r["start_time"], AK.worked_key(pk, r)) for n_, r in enumerate(pk.payroll)
              if r["earn_code"] in ("OT",) + tuple(AK.COMP) and n_ not in rep and AK.in_fy(r["work_date"])}
    ok("FAIR every accepted offer is paid as one piece", all(k in pieces for k in acc), str(len(acc)))
    day = {}
    for n_, r in enumerate(pk.payroll):
        if r["earn_code"] in ("OT",) + tuple(AK.COMP) and n_ not in rep:
            h = float(r["hours"]) / AK.COMP.get(r["earn_code"], 1.0)
            day[(r["employee_id"], r["work_date"])] = day.get((r["employee_id"], r["work_date"]), 0) + h
    ok("REAL no employee worked more than 12 hours of overtime on a day", max(day.values()) <= 12,
       str(max(day.values())))
    late = [n_ for n_, r in enumerate(pk.payroll) if r["work_date"] and r["earn_code"] != "OTR" and
            r["work_date"] < (dt.date.fromisoformat(r["pay_period_end"]) - dt.timedelta(days=13)).isoformat()]
    ok("SILENT lines paid after their period are mostly first payments, so the period gap marks no second payment",
       len(set(late) - rep) > len(set(late) & rep), "%d first, %d second" % (len(set(late) - rep), len(set(late) & rep)))
    straddle = sum(1 for r in retro if AK.quarter(r["service_period_start"]) != AK.quarter(r["service_period_end"]))
    ok("FAIR some retroactive periods straddle a quarter or the year's start", straddle > 50, str(straddle))

    # ------------------------------------------------------------------ input gates
    files = os.listdir(target)
    ok("GATE ten or more files", len(files) >= 10, str(len(files)))
    ok("GATE three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
       str(sorted({f.rsplit(".", 1)[1] for f in files})))
    ok("GATE a file of 25,000 rows or more", b["counts"]["rosters"] >= 25000, str(b["counts"]["rosters"]))
    ok("GATE two or more distractors", len(K.DISTRACTORS) >= 2)
    ok("GATE no file name names the stump",
       not [f for f in files if re.search(r"first.?year|availab|trap|issue|known", f, re.I)])

    # ------------------------------------------------------------------ realism sweep
    tot = [int(c["comp"][u]["A"].sum()) for u in U]
    ok("REAL no two units carry the same year of off-post hours", len(set(tot)) == len(tot), str(tot))
    ok("REAL overtime hours by unit are not round", all(v % 100 for v in g["a"].values()), str(g["a"]))
    text = ""
    for f in files:
        if f.endswith((".csv", ".txt")):
            text += open(os.path.join(target, f), encoding="utf-8").read()
        elif f.endswith(".pdf"):
            text += pdf_text(os.path.join(target, f))
    ok("REAL no em dash in the pack", "—" not in text)
    ok("REAL every persona named in the pack is drawn", all(p in text for p in
                                                            (K.PEOPLE["desk"], K.PEOPLE["director"],
                                                             K.PEOPLE["recruit"], K.PEOPLE["payroll"])))
    def week_read(new, after, through):
        v = np.zeros(K.WEEKS)
        for _, first, off in new:
            fw = (first - K.FY28_START).days // 7
            for i in range(K.WEEKS * 7):
                if (K.FY28_START + dt.timedelta(days=i)).weekday() in off:
                    continue
                vac = (i // 7 <= fw) if through else (i // 7 < fw)
                v[i // 7] += K.SHIFT_H if vac else K.SHIFT_H * after
        return v
    for through in (True, False):
        whole = []
        for u in U:
            cc = c["comp"][u]
            need = cc["A"] + week_read(cc["new"], 1 - cc["a1"], through)
            whole.append(int(math.ceil(A.q5(need) / (K.WEEK_H * cc["a1"]) - 1e-9)))
        ok("SF15 a new line's first week read whole (%s) places the same counts" % ("vacant" if through else "filled"),
           whole == gold, str(whole))
    splits = sum(1 for r in pk.position if r["status_fy2028_start"] == "Vacant" and
                 (dt.date.fromisoformat(r["first_shift_on_post"]) - K.FY28_START).days % 7)
    ok("DET most first shifts fall inside a fiscal week, so the day-level reading is exercised", splits >= 10, str(splits))

    print("checks: %d run, %d failed%s" % (N[0], len(FAILS), (": " + "; ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0
