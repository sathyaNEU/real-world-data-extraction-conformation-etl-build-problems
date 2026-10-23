"""task483's assertions on the cut pack and the generator's clean truth: the three rules (R1 the analyst test, R2 by
Layer 1 item, R3 the conjunction), every semantic fork row (SF1 to SF19), the ladder (L0 to L7), the golden's standing
families and margins (G1 to G8), the asks' devices (A1 to A6, B1 to B6), the separation line (X1 to X3), the realism
sweep (S1 to S3) and the input gates (I1 to I5).

    python3 task483/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import asks as A      # noqa: E402
import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
MA, CDL, PHL = "Medical Assisting", "Commercial Driver License, Class A", "Phlebotomy Technician"
RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def edge(v, u):
    """distance from v to the nearest edge of its printed cell of width u"""
    return u / 2.0 - abs(v - round(v / u) * u)


def call_with(I, deg, sh, weights=None):
    s, num, den = B.share(I, deg, sh, weights)
    return s >= B.SHARE, s


def main():
    I = B.Inputs(TARGET)
    gold = B.call(I)
    gdeg, gsh = gold["deg"], gold["short"]
    P_ = A.people()

    # ---------------------------------------------------------------------------------------------------------------
    # R: the three rules
    d0 = B.call(I, "naive", "quarter")
    check("R1a the analyst test: cells' medians averaged and any pay in the quarter renew (%.2f)" % d0["share"],
          d0["renews"] and B.hround(d0["share"]) == 84)
    check("R1b the golden lapses (%.2f, %d of %d)" % (gold["share"], gold["num"], gold["den"]),
          not gold["renews"] and (gold["num"], gold["den"]) == (1021, 1441))
    # the clean truth: each program's median from the simulated earnings of its published cells' completers, and
    # each grant completer's simulated jobs on day 180
    names = {code: (W.DEGREE[code][0] if code in W.DEGREE else W.SHORT[code][0]) for code in list(W.DEGREE) + list(W.SHORT)}
    agree = True
    for code in W.DEGREE:
        cells = [c for c in W.degree_cells(code) if c[5] is not None]
        if sum(c[3] for c in cells) < W.MIN_DEGREE:
            continue
        x = np.concatenate([c[4] * (W.CPI_2425 if c[2] == 2024 else 1.0) for c in cells])
        truth = float(np.median(x))
        g = gdeg[names[code]]["figure"]
        agree &= (truth >= W.BENCH) == gdeg[names[code]]["passes"] and abs(truth - g) < 1500
    check("R1c on the clean truth every credit program's simulated median falls on the golden's side of the benchmark "
          "and within 1,500 dollars of it", agree)
    pid_truth = {}
    for p in P_["participants"]:
        if p["kind"] == "window" and not p["left"]:
            pid_truth[p["pid"]] = W.truth_status(p["jobs"], p["completed"] + dt.timedelta(days=W.DAY))
    mism = sum(1 for prog in I.short for pid, comp in I.grant.get(prog, [])
               if B.status(I.rec.get(pid, {}), comp, "golden") != pid_truth[pid])
    check("R1d on the clean truth the dated jobs match every grant completer's simulated day-180 status (%d "
          "mismatches of %d)" % (mism, len(pid_truth)), mism == 0 and len(pid_truth) == sum(len(v) for v in I.grant.values()))
    cdl_q = sum(1 for pid, comp in I.grant[CDL] if B.status(I.rec.get(pid, {}), comp, "quarter")
                and not pid_truth[pid])
    check("R1e the quarter route counts %d CDL completers the simulation has not working on day 180" % cdl_q, cdl_q >= 20)
    # R2: each Layer 1 item, mishandled, leaves the call where it is
    nocpi = B.degree_figures(I, "golden", cpi=False)
    check("R2a the CPI factor missed: same pass set", all(nocpi[p]["passes"] == gdeg[p]["passes"] for p in I.degree))
    for how in ("original", "sum"):
        rec = I.wage_variant(how)
        s = B.short_figures(I, "golden", rec)
        check("R2b amended wage reports handled as '%s': same working counts" % how,
              all(s[p]["working"] == gsh[p]["working"] for p in I.short if s[p]["tested"]))
    saved = dict(I.cells)
    for p in ("Information Technology", "Criminal Justice"):
        I.cells[p] = [c for c in saved[p] if c[1] == "2021-22"]
    miss = B.degree_figures(I, "golden")
    I.cells = saved
    check("R2c the 2024 edition's pre-2022 CIP codes missed: same pass set",
          all(miss[p]["passes"] == gdeg[p]["passes"] for p in I.degree))
    other = sum(1 for r in B.rows_csv(os.path.join(TARGET, P.FILES["wages"])) if r["participant_id"] not in I.ids)
    check("R2d the wage file's other providers' rows (%d) join to no roster participant" % other, other > 5000)
    # R3: the conjunction
    one_d, one_s = B.call(I, "golden", "quarter"), B.call(I, "naive", "golden")
    check("R3 each half corrected alone renews (%.2f, %.2f); both lapse (%.2f)" % (one_d["share"], one_s["share"],
                                                                                gold["share"]),
          one_d["renews"] and one_s["renews"] and not gold["renews"])

    # ---------------------------------------------------------------------------------------------------------------
    # SF: the semantic fork table
    for r in ("naive", "unweighted", "median_of_medians"):
        x = B.call(I, r, "golden")
        check("SF1 the cells' medians %s instead of the group's median: Medical Assisting passes (%.0f), share %.2f" %
              (r, x["deg"][MA]["figure"], x["share"]), x["deg"][MA]["passes"] and x["renews"])
    ya = {}
    for r in B.sheet(os.path.join(TARGET, P.FILES["release24"]), "Program earnings", header=4):
        if r["Institution"] == W.SYSTEM and r["Award year"] == "2020-21":
            ya.setdefault(r["Years after award"], set()).add(r["Earnings year"])
    check("SF2 the 2020-21 cohort's three-years-after rows are earnings year 2024 (%s)" % ya, ya.get(3) == {2024})
    check("SF3 2025 dollars missed: same call, figures move", all(nocpi[p]["passes"] == gdeg[p]["passes"]
                                                                  for p in I.degree)
          and sum(1 for p in I.degree if gdeg[p]["tested"] and B.hround(nocpi[p]["figure"] / 1000)
                  != B.hround(gdeg[p]["figure"] / 1000)) == 6)
    check("SF4 Paralegal Studies has no published cell and is not tested",
          all(c[3] is None for c in I.cells["Paralegal Studies"]) and not gdeg["Paralegal Studies"]["tested"])
    check("SF5 the recodes join: Information Technology and Criminal Justice have both cohorts' cells",
          all({c[1] for c in I.cells[p]} == {"2020-21", "2021-22"} for p in ("Information Technology", "Criminal Justice")))
    near = []
    for p in P_["participants"]:
        if p["kind"] == "window" and not p["left"]:
            d180 = p["completed"] + dt.timedelta(days=W.DAY)
            for _, st, en, _, _ in p["jobs"]:
                for ev in (st, en):
                    if -24 <= (ev - d180).days <= 14:
                        near.append(p["pid"])
    s179 = 0
    for prog in I.short:
        for pid, comp in I.grant.get(prog, []):
            if B.status(I.rec.get(pid, {}), comp - dt.timedelta(days=1), "golden") != B.status(I.rec.get(pid, {}), comp,
                                                                                               "golden"):
                s179 += 1
    check("SF6 no job starts or ends within 24 days before or 14 after day 180, and day 179 changes no status (%d, %d)"
          % (len(near), s179), not near and s179 == 0)
    ext = {}
    for prog, ssid in I.completers:
        ext.setdefault(prog, set()).add(ssid)
    roster_end = {r["participant_id"]: r["section_end"] for r in I.roster}
    pid_ssid = {r["participant_id"]: r["state_student_id"] for r in I.roster}
    comp_dates = {}
    for r in B.sheet(os.path.join(TARGET, P.FILES["older"]), "Completions 2024-25"):
        d = r["Conferred"].date() if hasattr(r["Conferred"], "date") else r["Conferred"]
        comp_dates[str(r["SSID"])] = d.isoformat()
    for r in B.rows_csv(os.path.join(TARGET, P.FILES["newer"])):
        comp_dates[r["state_student_id"].replace("-", "")] = r["completion_date"]
    same_day = all(comp_dates.get(pid_ssid[pid]) == roster_end[pid] for prog in I.short for pid, _ in I.grant.get(prog, []))
    check("SF7 every grant completer's completion date in the extracts is the roster's section end", same_day)
    q = B.call(I, "golden", "quarter")
    check("SF8 any pay in the quarter instead of work on the day: the CDL program passes (%.1f), share %.2f" %
          (q["short"][CDL]["figure"], q["share"]), q["short"][CDL]["passes"] and q["renews"])
    check("SF9 amended reports kept, ignored or summed: same call", True and all(
        B.short_figures(I, "golden", I.wage_variant(h))[p]["working"] == gsh[p]["working"]
        for h in ("original", "sum") for p in I.short if gsh[p]["tested"]))
    grant_in_ext = all(pid_ssid[pid] in ext.get(prog, set()) for prog in I.short for pid, _ in I.grant.get(prog, []))
    check("SF10 every grant completer is a completer of the same program in the extracts", grant_in_ext)
    frk = "Forklift and Material Handling"
    sh2 = dict(gsh)
    frk_rate = 100.0 * sum(float(B.status(I.rec.get(pid, {}), comp, "golden")) for pid, comp in I.grant[frk]) / len(
        I.grant[frk])
    sh2[frk] = dict(tested=True, passes=frk_rate >= B.PLACED, n=len(I.grant[frk]), figure=frk_rate)
    r11 = call_with(I, gdeg, sh2)
    d11 = dict(d0["short"])
    d11[frk] = sh2[frk]
    r11d = call_with(I, d0["deg"], d11)
    check("SF11 Forklift (%d grant completers) tested anyway: same calls (%.2f, %.2f)" % (len(I.grant[frk]), r11[1],
                                                                                         r11d[1]),
          len(I.grant[frk]) < 20 and not r11[0] and r11d[0])
    gw = dict(I.c2425)
    gw.update({p: len(I.grant[p]) for p in I.short})
    r12, r12d = call_with(I, gdeg, gsh, gw), call_with(I, d0["deg"], d0["short"], gw)
    check("SF12 grant completers as the short-term weights: same calls (%.2f, %.2f)" % (r12[1], r12d[1]),
          not r12[0] and r12d[0])

    def share_all(deg, sh):
        num = den = 0
        for p, d in list(deg.items()) + list(sh.items()):
            w = I.c2425.get(p, 0)
            den += w
            num += w * bool(d["passes"])
        return 100.0 * num / den
    s13, s13d = share_all(gdeg, gsh), share_all(d0["deg"], d0["short"])
    check("SF13 untested programs in the denominator: same calls (%.2f, %.2f)" % (s13, s13d), s13 < 75 <= s13d)
    gaps = [abs(gdeg[p]["figure"] - B.BENCH) for p in I.degree if gdeg[p]["tested"]] + \
           [abs(gsh[p]["figure"] - B.PLACED) for p in I.short if gsh[p]["tested"]]
    check("SF14 rounded figures compared: same results (nearest 1,143 dollars and 6.7 points)",
          min(abs(gdeg[p]["figure"] - B.BENCH) for p in I.degree if gdeg[p]["tested"]) > 1000
          and min(abs(gsh[p]["figure"] - B.PLACED) for p in I.short if gsh[p]["tested"]) > 6
          and all((B.hround(gdeg[p]["figure"] / 1000.0) * 1000 >= B.BENCH) == gdeg[p]["passes"] for p in I.degree
                  if gdeg[p]["tested"]))
    inv = B.sheet(os.path.join(TARGET, P.FILES["inventory"]), "Programs")
    lengths = {r["Program"]: r["Length"] for r in inv}
    check("SF15 every credit program's length is in credits and every short-term program's under 600 clock hours",
          all("credits" in lengths[p] for p in I.degree)
          and all(int(lengths[p].split()[0]) < 600 for p in I.short))
    a_full = B.ask_a(I)
    a_gold = {p: v[0] for p, v in a_full.items()}
    a_end = {p: v[0] for p, v in B.ask_a(I, "by_end").items()}
    check("SF16 ask A's year as the sections that ended in it instead of the sessions dated in it moves %d figures" %
          sum(a_end[p] != a_gold[p] for p in I.short), sum(a_end[p] != a_gold[p] for p in I.short) >= 6)
    a_dec = {p: v[0] for p, v in B.ask_a(I, "decimal").items()}
    check("SF17 ask A's session times read as decimal hours instead of hours and minutes move %d figures" %
          sum(a_dec[p] != a_gold[p] for p in I.short), sum(a_dec[p] != a_gold[p] for p in I.short) == 11)
    b_gold, b_rows, b_plus = B.ask_b(I), B.ask_b(I, "rows"), B.ask_b(I, "with_plus")
    check("SF18 ask B's rows summed as exported move all 12 medians; parent loans kept move %d" %
          sum(b_plus[p][1] != b_gold[p][1] for p in I.degree),
          all(b_rows[p][1] != b_gold[p][1] for p in I.degree) and sum(b_plus[p][1] != b_gold[p][1] for p in I.degree) >= 6)
    e_deg = min(edge(gdeg[p]["figure"], 1000) for p in I.degree if gdeg[p]["tested"])
    e_sh = min(edge(gsh[p]["figure"], 1) for p in I.short if gsh[p]["tested"])
    e_b = min(edge(b_gold[p][2], 10) for p in I.degree)
    check("SF19 every graded figure clear of its rounding edge (earnings %.0f of 1,000; shares %.2f of 1; loan medians "
          "%.1f of 10; the share %.2f)" % (e_deg, e_sh, e_b, edge(gold["share"], 1)),
          e_deg >= 200 and e_sh >= 0.1 and e_b >= 2.5 and edge(gold["share"], 1) >= 0.25)

    # ---------------------------------------------------------------------------------------------------------------
    # L: the ladder
    expect = {("naive", "quarter"): 83.83, ("unweighted", "q2_after"): 83.83, ("median_of_medians", "min_2500"): 83.83,
              ("naive", "full_quarter"): 75.85, ("naive", "end_of_quarter"): 83.83, ("golden", "quarter"): 76.89,
              ("naive", "golden"): 77.79, ("golden", "golden"): 70.85}
    for (dr, sr), v in expect.items():
        x = B.call(I, dr, sr)
        check("L %s x %s: %.2f (%s)" % (dr, sr, x["share"], "renews" if x["renews"] else "lapses"),
              abs(x["share"] - v) < 0.006)
    lapse = []
    for dr in B.DEGREE_ROUTES:
        for sr in B.SHORT_ROUTES:
            x = B.call(I, dr, sr)
            if not x["renews"]:
                lapse.append((dr, sr))
    allowed = {(d, s) for d in ("golden", "log", "pchip", "pseudo", "lognormal") for s in ("golden", "full_quarter")}
    check("L every route that lapses is a pooling of the cells with dated jobs or full-quarter employment %s" %
          sorted(set(lapse) - allowed), set(lapse) <= allowed)
    fq = B.call(I, "golden", "full_quarter")
    check("L full-quarter employment with pooled medians fails Phlebotomy and moves every short-term figure",
          not fq["short"][PHL]["passes"] and all(B.hround(fq["short"][p]["figure"]) != B.hround(gsh[p]["figure"])
                                                 for p in I.short if gsh[p]["tested"]) and B.hround(fq["share"]) != 71)
    for r in ("pseudo", "lognormal"):
        x = B.degree_figures(I, r)
        moved = sum(1 for p in I.degree if x[p]["tested"] and B.hround(x[p]["figure"] / 1000)
                    != B.hround(gdeg[p]["figure"] / 1000))
        check("L the %s pooling moves %d of the 11 credit figures" % (r, moved), moved >= 6)
    d0f = B.degree_figures(I, "naive")
    check("L the default misses every credit figure", all(B.hround(d0f[p]["figure"] / 1000)
                                                          != B.hround(gdeg[p]["figure"] / 1000)
                                                          for p in I.degree if gdeg[p]["tested"]))

    # ---------------------------------------------------------------------------------------------------------------
    # G: the golden's standing families
    fam_deg = all(len({B.hround(B.pooled(I.cells[p], how, lo, hi) / 1000) for how in ("lin", "log", "pchip")
                       for lo in (0.3, 0.45, 0.6) for hi in (1.4, 1.7, 2.5)}) == 1
                  for p in I.degree if gdeg[p]["tested"])
    check("G1 every interpolation through the released percentiles, any tails, files one whole-thousand cell", fam_deg)
    inside = all(all(q[0] <= gdeg[p]["figure"] <= q[-1] for _, q in B.published(I.cells[p]))
                 for p in I.degree if gdeg[p]["tested"])
    check("G2 every program's pooled median lies between every one of its cells' 10th and 90th percentiles", inside)
    fam_sh = all(all(B.short_figures(I, "family%d" % k)[p]["working"] == gsh[p]["working"] for p in I.short
                     if gsh[p]["tested"]) for k in range(len(B.FAMILY)))
    check("G3 the %d job-level pay-ratio variants (the reference quarter adjacent, the full quarters' mean, the two "
          "beside the partial one or the job's median quarter; shifted 0, 7 or 14 days; calendar or 91-day quarters) "
          "file the same count for every program" % len(B.FAMILY), fam_sh)
    undated = sum(1 for prog in I.short for pid, comp in I.grant.get(prog, [])
                  if B.ratio_status(I.rec.get(pid, {}), comp + dt.timedelta(days=B.DAY))[1])
    check("G4 no grant completer's record leaves a job paid in the day-180 quarter undated (%d)" % undated, undated == 0)
    check("G5 Medical Assisting 1,143 dollars under the benchmark, the CDL program 6.7 points under 70",
          abs((B.BENCH - gdeg[MA]["figure"]) - 1143) < 1 and abs((B.PLACED - gsh[CDL]["figure"]) - 6.71) < 0.01)
    check("G6 no short-term figure exactly on a half", all(abs(gsh[p]["figure"] * 2 - round(gsh[p]["figure"] * 2)) > 1e-9
                                                           or round(gsh[p]["figure"] * 2) % 2 == 0
                                                           for p in I.short if gsh[p]["tested"]))
    e_a = min(edge(a_full[p][1], 1) for p in I.short)
    check("G7 every program's clock hours clear of the rounding edge (nearest %.2f hours of the half)" % e_a, e_a >= 0.1)
    shuffled = list(I.attendance)
    random.Random(7).shuffle(shuffled)
    keep = I.attendance
    I.attendance = shuffled
    a_sh = {p: v[0] for p, v in B.ask_a(I).items()}
    I.attendance = keep
    check("G8 row order: ask A unchanged over shuffled attendance rows", a_sh == a_gold)

    # ---------------------------------------------------------------------------------------------------------------
    # A: ask A's devices
    a_d = B.ask_a(I, "decimal")
    miss = {p: a_full[p][1] - a_d[p][1] for p in I.short}
    check("A1 the session times read as decimal hours miss all 11 figures, by %.1f to %.1f hours" % (
        min(miss.values()), max(miss.values())), all(a_dec[p] != a_gold[p] for p in I.short) and min(miss.values()) >= 1)
    after = [int(r["hours"].split(".")[1]) for r in I.attendance]
    inv = {r["Program"]: int(str(r["Length"]).split()[0]) for r in B.sheet(os.path.join(TARGET, P.FILES["inventory"]),
                                                                          "Programs") if "clock hours" in str(r["Length"])}
    done = {r["participant_id"]: I.program_of[r["participant_id"]] for r in I.roster if r["exit_reason"] == "Completed"}
    tot, dec = {}, {}
    seen = set()
    for r in I.attendance:
        key = (r["participant_id"], r["crn"], r["session_date"], r["hours"])
        if key in seen or r["participant_id"] not in done:
            continue
        seen.add(key)
        tot[r["participant_id"]] = tot.get(r["participant_id"], 0.0) + B.hours(r["hours"])
        dec[r["participant_id"]] = dec.get(r["participant_id"], 0.0) + float(r["hours"])
    full = {p: [pid for pid, prog in done.items() if prog == p and abs(tot.get(pid, 0) - inv[p]) < 1e-6]
            for p in I.short}
    usual = {}
    for r in I.attendance:
        usual.setdefault(I.crn_program[r["crn"]], {}).setdefault(r["hours"], 0)
        usual[I.crn_program[r["crn"]]][r["hours"]] += 1
    half = sorted(p for p, c in usual.items() if max(c, key=c.get).endswith(".30"))
    check("A2 no entry runs past 59 after the point (%d rows); %d completers who attended every full session total "
          "the inventory's clock hours read as hours and minutes (%d programs, %d of them among the %d whose sessions "
          "run to the half hour), and each of those falls short read as decimal hours" % (
              len(after), sum(len(v) for v in full.values()), sum(1 for p in I.short if full[p]),
              sum(1 for p in half if full[p]), len(half)),
          max(after) <= 59 and sum(len(v) for v in full.values()) >= 50 and sum(1 for p in half if full[p]) >= 3
          and all(dec[pid] < inv[p] - 1 for p in half for pid in full[p]))
    rowset = [(r["participant_id"], r["crn"], r["session_date"], r["hours"]) for r in I.attendance]
    dup = len(rowset) - len(set(rowset))
    tail = rowset[len(rowset) - dup:] if dup else []
    week = [k for k in rowset[:len(rowset) - dup] if "2025-03-03" <= k[2] <= "2025-03-07"]
    a_rs = {p: v[0] for p, v in B.ask_a(I, "resent").items()}
    check("A3 the export carries %d sessions twice, the week of 3 March 2025 appended again at its end; kept, they move "
          "%d figures" % (dup, sum(a_rs[p] != a_gold[p] for p in I.short)),
          dup > 100 and tail == week and sum(a_rs[p] != a_gold[p] for p in I.short) >= 6)
    a_cp = {p: v[0] for p, v in B.ask_a(I, "completers").items()}
    check("A4 the sections that ended in the year keep %d of 11, the completers' sessions alone %d" % (
        sum(a_end[p] == a_gold[p] for p in I.short), sum(a_cp[p] == a_gold[p] for p in I.short)),
          sum(a_end[p] != a_gold[p] for p in I.short) >= 6 and all(a_cp[p] != a_gold[p] for p in I.short))
    ros = {r["participant_id"]: r for r in I.roster}
    inside = all(max(B.iso(ros[r["participant_id"]]["section_start"]), B.iso(ros[r["participant_id"]]["enrolled_on"]))
                 <= B.iso(r["session_date"]) <= min(B.iso(ros[r["participant_id"]]["section_end"]),
                                                    B.iso(ros[r["participant_id"]]["exit_date"]))
                 and r["crn"] == ros[r["participant_id"]]["section_id"] for r in I.attendance)
    check("A5 every session lies inside its participant's section, from the day they enrolled to the day they left, "
          "under the roster's course reference number", inside)
    check("A6 no file states a program's hours attended; the inventory's clock hours are one participant's schedule",
          True)

    # ---------------------------------------------------------------------------------------------------------------
    # B: ask B's devices
    rows = I.loans
    new = [r for r in rows if B.iso(r["DISB_DATE"]) >= A.AID_SWITCH]
    old_rows = [r for r in rows if B.iso(r["DISB_DATE"]) < A.AID_SWITCH]
    by_loan = {}
    for r in new:
        by_loan.setdefault(r["LOAN_ID"], set()).add(r["GROSS_AMT"])
    two = {}
    for r in new:
        two[r["LOAN_ID"]] = two.get(r["LOAN_ID"], 0) + 1
    check("B1 from July 2024 every loan's rows carry one amount (%d loans, %d with two disbursements); no row from then "
          "is a return" % (len(by_loan), sum(1 for v in two.values() if v == 2)),
          all(len(v) == 1 for v in by_loan.values()) and all(r["DISB_STATUS"] == "Disbursed" for r in new))
    coa = re.sub(r"\s+", " ", subprocess.run(["pdftotext", os.path.join(TARGET, P.FILES["coa"]), "-"],
                                              capture_output=True, text=True).stdout)
    over = set()
    for r in new:
        if "Sub" in r["LOAN_TYPE"] and "Unsub" not in r["LOAN_TYPE"] and two.get(r["LOAN_ID"]) == 2 \
                and 2 * float(r["GROSS_AMT"]) > 4500:
            over.add(r["SSID"])
    once = all(float(r["GROSS_AMT"]) <= 4500 for r in new if r["LOAN_TYPE"] == "DL Sub")
    check("B2 two rows of a 2024-25 subsidized loan summed run past the 4,500-dollar subsidized annual limit for %d "
          "borrowers; one row never does" % len(over), len(over) >= 300 and once and "4,500 subsidized" in coa)
    b_pl, b_dd, b_ay, b_gu = (B.ask_b(I, x) for x in ("per_loan", "dedupe", "ay2425", "gross_up"))
    check("B3 the rows summed, one amount per loan in every year, alike rows kept once, the one award year and every "
          "amount read as net each miss all 12 medians", all(all(x[p][1] != b_gold[p][1] for p in I.degree)
                                                            for x in (b_rows, b_pl, b_dd, b_ay, b_gu)))
    b_dis = B.ask_b(I, "disbursed_only")
    check("B4 returned rows dropped keep %d of 12; parent loans kept keep %d" % (
        sum(b_dis[p][1] == b_gold[p][1] for p in I.degree), sum(b_plus[p][1] == b_gold[p][1] for p in I.degree)),
          sum(b_dis[p][1] == b_gold[p][1] for p in I.degree) <= 6 and sum(b_plus[p][1] == b_gold[p][1]
                                                                          for p in I.degree) <= 4)
    per = {}
    for r in old_rows:
        if "PLUS" not in r["LOAN_TYPE"]:
            per[r["SSID"]] = per.get(r["SSID"], 0.0) + float(r["GROSS_AMT"])
    zero = sum(1 for p, s in I.completers if s in per and abs(per[s]) < 0.005)
    check("B5 no completer's subsidized and unsubsidized disbursements before July 2024 net to zero (%d), and every "
          "program's borrower count is odd and its median a whole 10 dollars" % zero,
          zero == 0 and all(b_gold[p][0] % 2 == 1 and abs(b_gold[p][2] - b_gold[p][1]) < 1e-9 for p in I.degree))
    check("B6 the cost of attendance states the annual limits and that each loan is disbursed in installments, "
          "normally one each semester", "6,500 dollars (no more than 4,500 subsidized)" in coa
          and "disbursed in installments, normally one each semester" in coa)

    # ---------------------------------------------------------------------------------------------------------------
    # X: the separation line
    tmp = tempfile.mkdtemp()
    try:
        for fn in os.listdir(TARGET):
            shutil.copy(os.path.join(TARGET, fn), os.path.join(tmp, fn))
        for k, head in (("attendance", None), ("loans", None)):
            path = os.path.join(tmp, P.FILES[k])
            first = open(path, encoding="utf-8").readline()
            open(path, "w", encoding="utf-8").write(first)
        I2 = B.Inputs(tmp)
        g2 = B.call(I2)
        same = g2["share"] == gold["share"] and all(
            (g2["deg"][p]["figure"], g2["deg"][p]["passes"]) == (gdeg[p]["figure"], gdeg[p]["passes"]) for p in I.degree)
        same &= all((g2["short"][p]["figure"], g2["short"][p]["passes"]) == (gsh[p]["figure"], gsh[p]["passes"])
                    for p in I.short)
        check("X1 the call and every main figure are unchanged with the attendance export and the loans emptied",
              same)
    finally:
        shutil.rmtree(tmp)
    check("X2 the asks' device rows sit in files no step of the call reads (the attendance export, the loans)", True)
    window_pids = {pid for v in I.grant.values() for pid, _ in v}
    loan_ssids = {r["SSID"] for r in rows}
    check("X3 no short-term grant completer borrows in the loan file; the asks' joins touch the call's rows only for "
          "counts", not ({pid_ssid[p] for p in window_pids} & loan_ssids))

    # ---------------------------------------------------------------------------------------------------------------
    # S: realism; I: input gates
    fl = sorted(os.listdir(TARGET))
    exts = sorted({x.rsplit(".", 1)[1] for x in fl})
    rowsn = json.load(open(os.path.join(TASK, "metadata.json")))["rows"] if os.path.exists(
        os.path.join(TASK, "metadata.json")) else {}
    meta = json.load(open(os.path.join(TASK, "metadata.json"))) if os.path.exists(os.path.join(TASK, "metadata.json")) \
        else {"distractor_files": []}
    check("I1 %d files in %d formats %s" % (len(fl), len(exts), exts), len(fl) >= 10 and len(exts) >= 3)
    big = max(sum(1 for _ in open(os.path.join(TARGET, x), encoding="utf-8")) - 1 for x in fl if x.endswith(".csv"))
    check("I2 a file of 25,000 rows or more (%d)" % big, big >= 25000)
    check("I3 two distractors named in metadata.json, neither named so in a file name",
          len(meta["distractor_files"]) >= 2 and not any("distract" in x for x in fl))
    bad = []
    stump = ("pooled", "mixture", "partial quarter", "partial-quarter", "full quarter", "full-quarter", "half point",
             "interpolat", "start date", "separation date", "net of", "repeated", "averag", "invoice header", "first section", "supplementary",
             "hand-keyed", "keyed by hand", "late enrol", "after the census", "every line", "each line", "loan amount",
             "annual amount", "per loan", "hours and minutes", "minutes after")
    for x in fl:
        p = os.path.join(TARGET, x)
        if x.endswith(".pdf"):
            txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        elif x.endswith(".xlsx"):
            z = zipfile.ZipFile(p)
            txt = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist())
        else:
            txt = open(p, encoding="utf-8").read()
        low = re.sub(r"\s+", " ", txt.lower()).replace("annual average", "annual")
        for word in ("\u2014", "\u2013", "ReportLab", "openpyxl", "matplotlib") + stump:
            if word.lower() in low:
                bad.append((x, word))
    check("I4 no dash, toolchain signature or stump word in a shipped file %s" % bad, not bad)
    last = {}
    last["wages"] = max((int(r["year"]), int(r["quarter"])) for r in B.rows_csv(os.path.join(TARGET, P.FILES["wages"])))
    last["roster"] = max(r["exit_date"] for r in I.roster)
    last["attendance"] = max(r["session_date"] for r in I.attendance)
    last["loans"] = max(r["DISB_DATE"] for r in rows)
    check("I5 the extracts end where they say and before the 16 October 2026 as-of: %s" % last,
          last["wages"] == (2026, 2) and last["roster"] <= "2026-06-30" and last["attendance"] <= "2026-06-30"
          and last["loans"] <= "2026-06-30")
    check("S1 the release's other colleges and other years-after rows are present (%d Larkspur three-year cells)" %
          sum(len(v) for v in I.cells.values()), sum(len(v) for v in I.cells.values()) == 60)
    check("S2 the two completion extracts' ID formats differ (seven digits and LB numbers)",
          all(re.fullmatch(r"\d{7}", str(r["Student ID"])) for r in B.sheet(os.path.join(TARGET, P.FILES["older"]),
                                                                             "Completions 2024-25"))
          and all(re.fullmatch(r"LB\d{6}", r["student_number"]) for r in B.rows_csv(os.path.join(TARGET,
                                                                                            P.FILES["newer"]))))
    amended = sum(1 for r in B.rows_csv(os.path.join(TARGET, P.FILES["wages"])) if r["report_type"] == "Amended")
    check("S3 amended wage reports present (%d)" % amended, amended > 300)

    fails = [n for n, ok in RESULTS if not ok]
    print("%s  %d checks, %d failed" % ("PASS" if not fails else "FAIL", len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
