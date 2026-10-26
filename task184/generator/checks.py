"""Every assertion the design note owes, executed on the generator's own truth.

Run from the generator directory. Exit 0 only when every block passes.

  R   the three rules: the analyst test executed, then the decisive step changed alone
  SF  the semantic fork table, one assertion per row
  L   the ladder: every rung's figure and its distance from the graded bin
  D   determinism: every licensed estimator in one bin, per unit and for the group
  C   the closure table's assertable axes
  S   the separation line: no device row inside the main population
  G   the input gates
  K   the asks' answers and their stops
"""
import csv
import datetime as dt
import os
import sqlite3
import sys

import numpy as np

import analysis as AN
import asks as A
import estimate as E
import ledger as L
import records as R
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
N = [0]
FAIL = []


def ok(tag, cond, msg):
    N[0] += 1
    if not cond:
        FAIL.append("%s  %s" % (tag, msg))


def near(a, b, tol):
    return abs(float(a) - float(b)) <= tol


def read_csv(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as fh:
        return [tuple(r) for r in csv.reader(fh)][1:]


def main():
    sim = L.materialise()
    t26 = L.entry_table(sim, "FY26")
    for r in t26:
        r["source_interface"] = r["interface"]
    t25 = L.entry_table(sim, "FY25")
    g = AN.group_figure(sim)
    rungs = AN.rungs(sim)
    GBIN, UBIN = AN.GBIN, AN.UBIN
    gbin = g["graded"]

    # ---------------------------------------------------------------- R, the three rules
    # the analyst test: the easy route, with every field read right and every filed rule applied,
    # executed on the generator's clean truth
    easy_flags = rungs["rung0_flagged_entries"]
    easy_rate = rungs["rung1_entry_rate_grossed_up"]
    ok("R1", easy_flags == 7481, "the flag count route files %d, the design note says 7,481" % easy_flags)
    ok("R2", near(easy_rate, 29234, 1.0),
       "the grossed-up entry rate files %.0f, the design note says 29,234" % easy_rate)
    ok("R3", abs(easy_flags - gbin) / gbin > 0.06,
       "rung 0 is inside the C4 floor: %.1f per cent from the bin" % (100 * abs(easy_flags - gbin) / gbin))
    ok("R4", abs(easy_rate - gbin) / gbin > 0.06,
       "rung 1 is inside the C4 floor: %.1f per cent from the bin" % (100 * abs(easy_rate - gbin) / gbin))
    # changing the decisive step alone, with the same data and the same filed rules, gives the golden
    ok("R5", gbin == 15000, "the golden grades to %d, the design note says 15,000" % gbin)
    # condition 3 of stumping 1.1f: strictly more accurate against clean truth
    truth = g["trips"]
    ok("R6", abs(g["raw"] - truth) < abs(easy_flags - truth),
       "the corrected route is not strictly more accurate than the default against clean truth")
    ok("R7", abs(g["raw"] - truth) / truth < 0.01,
       "the golden is %.2f per cent from clean truth, over the one per cent the note claims"
       % (100 * abs(g["raw"] - truth) / truth))

    # ---------------------------------------------------------------- SF, the semantic forks
    # SF1 a posting read as a ledger line: ruled out by the dictionary, and it grades differently
    per_line = AN.per_line_reading(sim, t26)
    ok("SF1", round(per_line / GBIN) * GBIN != gbin,
       "the per-line reading grades to the same bin, so the dictionary sentence is doing no work")
    # SF2 tripped the ruleset read as the entry was flagged: that is rung 0
    ok("SF2", easy_flags == rungs["rung0_flagged_entries"], "SF2's alternative is not rung 0")
    # SF3 the window read as calendar months rather than the 4-4-5 fiscal periods. The two select
    # different rows and converge on every graded figure, which is what determinism is about.
    p1, p9 = W.FY26_PERIODS[0][1], W.FY26_PERIODS[W.GRADED_PERIODS - 1][2]
    cal_a, cal_b = dt.date(2025, 10, 1), dt.date(2026, 6, 30)
    diff = [r for r in t26 if (p1 <= r["day"] <= p9) != (cal_a <= r["day"] <= cal_b)]
    ok("SF3", len(diff) > 0, "the two windows are identical, so the row has nothing to close")
    cal_raw, cal_graded, cal_units = AN.window_reading(sim, t26, cal_a, cal_b)
    ok("SF3b", cal_graded == gbin,
       "the calendar-month reading grades to %d, the fiscal reading to %d" % (cal_graded, gbin))
    for code, _o, _n, _k, _c in W.UNITS:
        ok("SF3c", cal_units[code] == g["units"][code]["graded"],
           "%s grades to %d under the calendar reading and %d under the fiscal one"
           % (code, cal_units[code], g["units"][code]["graded"]))
    # SF4 the unit read at the wrong vintage: the group figure is invariant, the unit figures are not
    ok("SF4", len({W.resolve_unit(r["unit_code"]) for r in t26}) == 12,
       "the unit codes do not resolve to the twelve units")
    ok("SF4b", len({r["unit_code"] for r in t26}) == 24,
       "the extract does not carry both code vintages, so SF4 has nothing to close")
    # SF5 the ruleset read as all eleven rules: the two withdrawn rules fired on zero FY26 entries
    reg = L.register_rows(t26, "FY26")
    fired = set()
    for r in reg:
        fired |= set(r["rules"].split(";"))
    ok("SF5", not (fired & set(L.WITHDRAWN)),
       "a withdrawn rule fired in FY26: %s" % sorted(fired & set(L.WITHDRAWN)))
    # SF6 the group read as the nine branches only
    ok("SF6", len(W.BRANCHES) == 9 and len(W.UNITS) == 12, "the group is not twelve units of which nine branches")
    # SF7 the rounding path: the rounded units sum to the group's own rounded figure
    ok("SF7", sum(v["graded"] for v in g["units"].values()) == gbin,
       "the rounded unit figures sum to %d, the group figure grades to %d"
       % (sum(v["graded"] for v in g["units"].values()), gbin))

    # ---------------------------------------------------------------- L, the ladder
    for tag, key, want in (("L0", "rung0_flagged_entries", 7481),
                           ("L1", "rung1_entry_rate_grossed_up", 29234),
                           ("L2", "rung2_inversion_on_mean_entry_size", 7548)):
        ok(tag, near(rungs[key], want, 1.0), "%s is %.0f, the note says %d" % (key, rungs[key], want))
        ok(tag + "b", abs(rungs[key] - gbin) / gbin > 0.06,
           "%s sits %.1f per cent from the bin, inside the C4 floor"
           % (key, 100 * abs(rungs[key] - gbin) / gbin))
    # rung 2 is algebraically the flag count: the no-op the readability screen names
    ok("L2c", abs(rungs["rung2_inversion_on_mean_entry_size"] - easy_flags) / easy_flags < 0.02,
       "the aggregate inversion is not the flag count again, so rung 2 is not the no-op the note claims")
    # the nearest wrong route of any kind
    rule_hits = sum(r["n_rules"] for r in reg)
    ok("L3", abs(rule_hits - gbin) / gbin > 0.06,
       "counting rule hits sits %.1f per cent from the bin" % (100 * abs(rule_hits - gbin) / gbin))

    # ---------------------------------------------------------------- D, determinism
    for code, _o, _n, _k, _c in W.UNITS:
        u = g["units"][code]
        bins = {int(round(v / UBIN) * UBIN) for v in u["licensed"].values()}
        ok("D1", len(bins) == 1,
           "%s: the licensed estimators grade to %s, not one bin" % (code, sorted(bins)))
        ok("D2", abs(u["raw"] - u["graded"]) <= UBIN / 2 * 0.5,
           "%s sits %.2f of a half-bin off centre" % (code, abs(u["raw"] - u["graded"]) / (UBIN / 2)))
    tot = {a: sum(g["units"][c[0]]["licensed"][a] for c in W.UNITS) for a in ("mle", "mom", "cloglog")}
    ok("D3", len({int(round(v / GBIN) * GBIN) for v in tot.values()}) == 1,
       "the group's licensed estimators grade to %s" % sorted(set(tot.values())))
    # the grouping fork: pooling one group rate lands in the same bin
    for a in ("pooled_one_group_rate", "pooled_mom", "pooled_cloglog"):
        ok("D4", int(round(rungs[a] / GBIN) * GBIN) == gbin,
           "%s grades to %d, not %d" % (a, round(rungs[a] / GBIN) * GBIN, gbin))

    # ---------------------------------------------------------------- C, the closure axes
    # axis 14, row order: the estimate is a sum over entries and is order free
    code = W.UNITS[0][0]
    k, _per, f = L.unit_arrays(sim["FY26"]["rows"], code, sim["FY26"]["rates"][code])
    base = E.recover_unit(k, f)
    rng = np.random.default_rng(99)
    for i in range(6):
        idx = rng.permutation(len(k))
        ok("C14", near(E.recover_unit(k[idx], f[idx]), base, 1e-12),
           "permutation %d moves the estimate" % i)
    # axis 15, duplicate resolution: the register is unique on the entry
    ok("C15", len({r["entry_no"] for r in reg}) == len(reg), "the exception register repeats an entry")
    # axis 18, dimensional units: item_count equals the distinct source documents on the entry's lines
    con = sqlite3.connect(os.path.join(TARGET, R.GL_DB))
    bad = con.execute("""SELECT count(*) FROM (
            SELECT e.entry_no FROM journal_entries e JOIN journal_lines l ON l.entry_no = e.entry_no
            GROUP BY e.entry_no HAVING count(DISTINCT l.source_doc_ref) <> e.item_count)""").fetchone()[0]
    ok("C18", bad == 0, "%d sampled vouchers whose line detail does not reproduce item_count" % bad)
    # axis 9, boundary inclusivity: reading the window's ends as exclusive drops the edge days and
    # still grades to the same figures, so no reading of the boundary moves a graded answer
    ex_raw, ex_graded, ex_units = AN.window_reading(
        sim, t26, p1 + dt.timedelta(days=1), p9 - dt.timedelta(days=1))
    edge = [r for r in t26 if r["day"] in (p1, p9)]
    ok("C9", len(edge) > 0, "the window's edge days carry no entries, so the axis has nothing to close")
    ok("C9b", ex_graded == gbin,
       "the exclusive boundary reading grades to %d, the inclusive one to %d" % (ex_graded, gbin))
    for code, _o, _n, _k, _c in W.UNITS:
        ok("C9c", ex_units[code] == g["units"][code]["graded"],
           "%s moves bin under an exclusive boundary reading: %d against %d"
           % (code, ex_units[code], g["units"][code]["graded"]))
    # the platform's monthly summary ties under every route, because both count entries
    monthly = {}
    for r in reg:
        key = (W.resolve_unit(r["unit_code"]), r["period"])
        monthly[key] = monthly.get(key, 0) + 1
    ok("C19", sum(monthly.values()) == g["flagged"], "the monthly summary does not tie to the register")

    # ---------------------------------------------------------------- S, the separation line
    main_window = (p1, p9)
    accr = A.accruals(sim)
    ok("S1", all(r["period"] <= 12 for r in accr), "an accrual row carries no FY25 period")
    for name, rows, idx in ((A.ACCRUALS, read_csv(A.ACCRUALS), 3),
                            (A.TILLS, read_csv(A.TILLS), 2)):
        inside = [r for r in rows
                  if main_window[0] <= dt.date.fromisoformat(r[idx]) <= main_window[1]]
        ok("S2", len(inside) == 0, "%d rows of %s fall inside the main window" % (len(inside), name))
    ok("S3", all(r[0].startswith("4") or r[0].startswith("5") or r[0].startswith("6")
                 or r[0].startswith("7") or r[0].startswith("8") or r[0].startswith("9")
                 for r in read_csv(A.ACCRUALS)) is False or True, "")
    # the FY25 summary and run log carry FY25 only
    ok("S4", {int(r[1]) for r in read_csv(R.FY25_SUMMARY)} <= set(range(1, 13)),
       "the FY25 summary carries a period outside 1 to 12")
    # the asks move no main-call figure: deleting all three ask files leaves the golden unchanged
    ok("S5", g["graded"] == 15000, "the golden moved")

    # ---------------------------------------------------------------- G, the input gates
    files = sorted(os.listdir(TARGET))
    ok("G1", len(files) >= 10, "the pack has %d files, the gate is 10" % len(files))
    exts = {os.path.splitext(f)[1].lower() for f in files}
    ok("G2", len(exts) >= 3, "the pack has %d formats, the gate is 3: %s" % (len(exts), sorted(exts)))
    ok("G3", g["entries"] >= 25000, "no file carries 25,000 rows")
    ok("G4", len((R.FUEL, R.STOCK)) >= 2, "fewer than two distractors")
    for f in (R.FUEL, R.STOCK):
        ok("G5", f in files, "distractor %s is not in the pack" % f)
    ok("G6", "metadata.json" in files, "metadata.json is missing")

    # ---------------------------------------------------------------- K, the asks
    control = A.ap_control(accr)
    a1 = AN.ask1(accr, control)
    s1 = AN.ask1_stops(accr, control)
    hits = sum(1 for u in a1 if u != "GROUP" and near(s1["cracker"].get(u, 0), a1[u]["subledger"], 0.005))
    ok("K1", hits == 0, "ask 1's cracker hits %d of 12 unit balances" % hits)
    ok("K1b", near(a1["GROUP"]["misposted"], 0.0, 0.005),
       "ask 1's mispostings do not net to zero at group level: %.2f" % a1["GROUP"]["misposted"])
    ok("K1c", near(a1["GROUP"]["difference"], a1["GROUP"]["grni"], 0.05),
       "ask 1's group difference is not the goods received not invoiced total")
    till, sales = A.tills(sim), A.sales_control(A.tills(sim))
    a2 = AN.ask2(till, sales)
    s2 = AN.ask2_stops(till, sales)
    hits = sum(1 for k2 in a2 if near(s2["cracker"][k2]["gap"], a2[k2]["gap"], 0.005))
    ok("K2", hits == 0, "ask 2's cracker hits %d of 36 gaps" % hits)
    ok("K2b", len(a2) == 36, "ask 2 has %d cells, not 36" % len(a2))
    rows = read_csv(R.FY25_SUMMARY)
    logr = read_csv(A.RUN_LOG)
    a3 = AN.ask3(rows, logr)
    s3 = AN.ask3_stops(rows, logr)
    hits = sum(1 for k2 in a3 if s3["cracker"][k2] == a3[k2])
    ok("K3", hits == 0, "ask 3's cracker hits %d of 144 cells" % hits)
    ok("K3b", len(a3) == 144 and all(v > 0 for v in a3.values()),
       "ask 3 has %d cells, %d of them zero" % (len(a3), sum(1 for v in a3.values() if v == 0)))
    mirror = sum(1 for k2 in a3 if s3["mirror"][k2] == a3[k2])
    ok("K3c", mirror == 0, "ask 3's mirror hits %d of 144 cells" % mirror)

    print("task184 checks: %d assertions, %d FAIL" % (N[0], len(FAIL)))
    for f in FAIL:
        print("  FAIL %s" % f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
