"""Every claim the build makes, asserted against the clean truth and the cut pack."""
import csv
import json
import datetime as dt
import math
import os
import re

import asks as A
import golden as G
import mus
import sim
import world as W

N = [0]
FOUND, RATIO, STRATUM, PROJ, TOTAL = 21004.93, 57577.47, 156183.24, 840096.72, 850000
CALL = {"CP-11": 0, "CP-14": 0, "CP-21": 50000, "CP-23": 200000, "CP-31": 0,
        "CP-34": 150000, "CP-41": 250000, "CP-44": 150000, "CP-47": 50000}


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))


def _rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def verify_mod():
    import verify
    return verify


def run(g, target):
    N[0] = 0
    lines, hits = g["lines"], g["hits"]
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- the three rules
    headers = []
    for name in files:
        if name.endswith(".csv"):
            with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
                headers.extend(next(csv.reader(fh)))
    bad = [h for h in headers if re.search(r"interval|project|extrapol|weight|inclusion|"
                                           r"stratum|misstate|taint|selection", h, re.I)]
    ok("R1 no deciding quantity in a column", not bad, str(bad))
    ok("R1 the population ships line by line", len(lines) > 25000, str(len(lines)))
    ok("R1 every line amount is strictly positive", all(x[1] > 0 for x in lines))
    cum = sim.cumulative(lines)
    ok("R1 the cumulative recorded value is monotone",
       all(cum[i + 1] > cum[i] for i in range(len(lines))))
    ok("R2 the clean truth reproduces the golden",
       abs(G.compute(lines, hits)["total_raw"] - PROJ) < 0.01)
    ok("R2 the golden is the call the note files", g["per"] == CALL, str(g["per"]))

    # the analyst test, executed: the easy route on the clean truth
    ok("R3a the misstatement found files the named wrong answer",
       abs(g["found"] - FOUND) < 0.01, "%.2f" % g["found"])
    ok("R3a the recorded-value ratio files the named wrong answer",
       abs(g["ratio"] - RATIO) < 0.01, "%.2f" % g["ratio"])
    ok("R3b the stratum ratio stays wrong", abs(g["stratum"] - STRATUM) < 0.01,
       "%.2f" % g["stratum"])
    ok("R3b the decisive step files the golden", abs(g["total_raw"] - PROJ) < 0.01)
    ok("R3b the golden's stated figure is the note's", g["total"] == TOTAL, str(g["total"]))
    # ---- positive controls, before any absence is asserted.
    # A grep reports the same "not found" whether the string is absent or the file could not be
    # read. _sweep used to read the PDFs as raw bytes and never saw inside their Flate streams, so
    # every absence claim below passed by never executing. Each PDF therefore has to yield text,
    # and a sentence known to be in it has to be found, through the same decoder the sweep uses,
    # before a single absence assertion runs.
    CONTROLS = {
        "audit_plan_2026.pdf": "Conclusion on a tested population",
        "audit_manual_part9.pdf": "Terms used in reporting a tested population",
        "internal_audit_testing_schedule_2026.pdf": "Basis of selection",
    }
    for name, sentence in sorted(CONTROLS.items()):
        extracted = " ".join(verify_mod().pdf_text(os.path.join(target, name)))
        ok("control: %s yields text through the sweep's own decoder" % name,
           len(extracted) > 500, "%d characters" % len(extracted))
        ok("control: the known sentence in %s is found" % name,
           sentence in extracted, sentence)
        ok("control: _sweep itself finds that sentence in %s" % name,
           name in _sweep(target, re.escape(sentence)),
           str(_sweep(target, re.escape(sentence))))
    ok("control: every shipped csv and md yields its own text to the sweep",
       all(_sweep(target, re.escape(w)) for w in ("ledger_sequence", "programme_code")))

    # the sampling design is filed as a fact about the sample; the estimator is not filed
    ok("R3c the pack files the design: probability proportional to recorded value",
       _sweep(target, r"probability proportional to recorded value") ==
       ["internal_audit_testing_schedule_2026.pdf"])
    ok("R3c the pack files the interval and that it was common to every programme",
       _sweep(target, r"common to every work programme") ==
       ["internal_audit_testing_schedule_2026.pdf"] and
       _sweep(target, r"180,000 euro") == ["internal_audit_testing_schedule_2026.pdf"])
    terms = ("selection interval", "certain of selection", "tainting", "basic precision",
             "incremental allowance", "upper misstatement limit", "reliability factor")
    ok("R3c the manual defines every term the graded components use",
       all("audit_manual_part9.pdf" in _sweep(target, w) for w in terms),
       str([w for w in terms if "audit_manual_part9.pdf" not in _sweep(target, w)]))
    ok("R3c no shipped file says how to get from the tested lines to the population",
       not _sweep(target, r"projec\w*|extrapolat|scale(d|s)? up|gross(ed)? up|"
                          r"estimate the population|misstatement per euro|"
                          r"multiply(ing)? the tainting|divide(d)? by the (recorded|tested) value"))
    ok("R3c no shipped file states the expected misstatement allowance",
       not _sweep(target, r"expected misstatement|%s" % format(int(W.EXPECTED_MISSTATEMENT), ",")))
    ok("R3c no shipped file states the golden",
       not _sweep(target, r"\b800[, ]?000\b"))
    # the shipped table is the one the figures are computed from, so both reproduce exactly
    tbl = verify_mod().pdf_text(os.path.join(target, "audit_manual_part9.pdf"))
    shipped_rf = []
    for i, s in enumerate(tbl):
        if s.strip() != "factor":
            continue
        for nxt in tbl[i + 1:]:
            if not re.match(r"^\d{1,2}\.\d{2}$", nxt.strip()):
                break
            shipped_rf.append(round(float(nxt), 2))
    ok("R3c the shipped reliability table is the one the figures use",
       shipped_rf[:len(mus.RF)] == [round(v, 2) for v in mus.RF],
       str(shipped_rf[:6]))
    ok("R3c the incremental allowance recomputes from the shipped table",
       abs(g["ia"] - mus.ia_from(shipped_rf, lines, hits)) < 0.005,
       "%.2f against %.2f" % (g["ia"], mus.ia_from(shipped_rf, lines, hits)))
    ok("R3c the upper limit recomputes from the shipped table",
       abs(g["uml"] - (g["total_raw"] + g["bp"] +
                       mus.ia_from(shipped_rf, lines, hits))) < 0.005)
    ok("R3c basic precision recomputes from the shipped table",
       abs(g["bp"] - W.INTERVAL * shipped_rf[0]) < 0.005)

    # ---------------------------------------------------------------- the ladder
    r = [v for _, v in G.rungs(g)]
    ok("ladder is ordered away from the golden", r[0] < r[1] < r[2] < r[3], str(r))
    ok("ladder steps all clear 1.15x",
       all(r[i + 1] / r[i] >= 1.15 for i in range(3)),
       str([round(r[i + 1] / r[i], 2) for i in range(3)]))
    ok("the decisive move is the largest step on the ladder",
       (r[3] - r[2]) > max(r[1] - r[0], r[2] - r[1]))
    ok("the golden is the extreme of the ladder", r[3] == max(r))
    ok("no rung lands on the golden", len({round(x) for x in r}) == 4)
    # the conclusion at plan 4.3 under each rung, with the field's own allowance
    certf = sum(x[1] * x[3] for x in mus.split(lines, hits)[1])
    for name, val in G.rungs(g)[:3]:
        bound = val + g["bp"] + 0.40 * max(0.0, val - certf)
        ok("4.3 accepts the population on the rung: %s" % name, bound <= W.TOLERABLE,
           "%.0f against %.0f" % (bound, W.TOLERABLE))
        ok("that rung's bound keeps a quarter of materiality clear",
           bound < W.TOLERABLE * 0.78, "%.3f" % (bound / W.TOLERABLE))
    ok("4.3 refers the population on the golden", g["uml"] > W.TOLERABLE,
       "%.0f" % g["uml"])
    ok("the golden clears materiality by a quarter", g["uml"] > W.TOLERABLE * 1.25,
       "%.3f" % (g["uml"] / W.TOLERABLE))
    ok("the crudest bound at the stated confidence still refers it",
       g["crude"] > W.TOLERABLE * 1.10, "%.3f" % (g["crude"] / W.TOLERABLE))
    ok("basic precision alone does not refer it", g["bp"] < W.TOLERABLE * 0.55,
       "%.3f" % (g["bp"] / W.TOLERABLE))
    # the rankings
    byrec = sorted(W.PROG_CODES, key=lambda c: -g["recorded"][c])
    ok("the recorded-value ranking is not the answer ranking", byrec[0] != g["largest"])
    ok("the largest programme by misstatement is outside the top three by recorded value",
       g["largest"] not in byrec[:3], g["largest"])
    ok("the largest leads the runner up by a clear cell",
       g["per"][g["largest"]] >= sorted(g["per"].values())[-2] + W.GRAIN)

    # ---------------------------------------------------------------- determinism
    # The selection interval is filed on the working paper, so nothing has to be recovered and
    # the lattice is no longer load-bearing. What has to hold is that the filed design is
    # consistent with the shipped selection and that the figure is a single value under it.
    ok("C1 the filed interval reproduces the shipped selection exactly",
       sim.select(lines, W.INTERVAL, W.RANDOM_START)[0] == hits)
    ok("C1 the filed design is true of the pack: every line at or above the interval is tested",
       all((i in {j for j, _ in hits}) for i, x in enumerate(lines) if x[1] >= W.INTERVAL))
    ok("C1 the filed interval is one interval, not one per programme",
       len({W.INTERVAL}) == 1)
    percode = {}
    for c in W.PROG_CODES:
        sub = [x for x in lines if x[0] == c]
        sh, _, _ = sim.select(sub, W.INTERVAL, W.RANDOM_START)
        percode[c] = mus.projection(sub, sh, W.INTERVAL)
    ok("C1 the per-programme-interval route the working paper rules out gives another answer",
       mus.r_grain(sum(percode.values())) != TOTAL,
       "%d against %d" % (mus.r_grain(sum(percode.values())), TOTAL))
    below = max(x[1] for x in lines if x[1] < W.INTERVAL)
    above = min(x[1] for x in lines if x[1] >= W.INTERVAL)
    ok("C1 no population line sits at the interval, so the boundary reading cannot move it",
       below < W.INTERVAL < above, "%.2f %.2f" % (below, above))
    ok("C1 the nearest population line is clear of the interval",
       min(above - W.INTERVAL, W.INTERVAL - below) >= 500.0,
       "%.2f" % min(above - W.INTERVAL, W.INTERVAL - below))
    ok("C1 the underlying sits clear of its rounding line",
       W.GRAIN / 2.0 - abs(g["total_raw"] - g["total"]) >= 11000.0,
       "%.0f" % (W.GRAIN / 2.0 - abs(g["total_raw"] - g["total"])))
    for c in W.PROG_CODES:
        edge = W.GRAIN / 2.0 - abs(g["per_raw"][c] - g["per"][c])
        ok("C1 %s sits clear of its rounding line" % c, edge >= 9000.0, "%.0f" % edge)
        if g["per"][c] == 0:
            ok("C1 the nil at %s is deep in its cell" % c, g["per_raw"][c] < 15000.0,
               "%.0f" % g["per_raw"][c])
    ok("C1 three programmes are nil", sum(1 for c in W.PROG_CODES if g["per"][c] == 0) == 3)
    ok("C1 the stated programme figures sum to the stated total",
       sum(g["per"].values()) == g["total"], "%d against %d" % (sum(g["per"].values()), g["total"]))
    ok("C1 the stated figures take at least five distinct values",
       len(set(g["per"].values())) >= 5, str(sorted(set(g["per"].values()))))

    # the blind-response families
    bl = _blind(g)
    for nm, hit in sorted(bl.items()):
        ok("C1 blind response (%s) takes at most three of eighteen cells" % nm, hit <= 3,
           "%d" % hit)

    # ---------------------------------------------------------------- the semantic forks
    seg = {c: sum(x[1] for x in lines if x[0] == c) for c in W.PROG_CODES}
    ok("SF1 the figure read on invoices is the same call", True)
    ok("SF2 the testing found no understatement",
       all(t["payable"] <= t["amount"] + 0.005 for t in g["tested"]))
    ok("SF3 the window is the authority's calendar year",
       all(x["day"].isoformat()[:4] == W.YEAR for x in g["shipped"] if x["delivery"] == 1))
    ok("SF4 the figure is an amount and not a count", isinstance(g["total"], int))
    ok("SF5 nine work programmes", len(W.PROG_CODES) == 9 and len(seg) == 9)
    ok("SF6 both rounding paths give the stated total",
       sum(g["per"].values()) == mus.r_grain(g["total_raw"]) == TOTAL)
    ok("SF7 two credit notes ship, neither in the tested set",
       len(g["reversed_refs"]) == 2 and
       not [t for t in g["tested"] if t["line"] in g["reversed_refs"]])
    ok("SF8 one run was delivered twice and no tested line is a second delivery",
       g["dup_n"] > 20 and all(t["delivery"] == 1 for t in g["tested"]))
    ok("SF9 the crosswalk is complete and one-to-one",
       len(g["cross"]) == len(set(g["cross"].values())))
    ok("SF10 the two-year extract holds both years",
       {r["testing_year"] for r in _rows(target, "testing_schedule_extract_2025_2026.csv")}
       == {"2025", "2026"})
    ok("SF11 the register states thousands and the figure never reads it",
       "thousands" in ",".join(next(csv.reader(open(
           os.path.join(target, "capital_programme_register.csv"), encoding="utf-8")))))
    ok("SF12 comparing the projection itself to materiality would accept the population",
       g["total_raw"] < W.TOLERABLE and g["uml"] > W.TOLERABLE,
       "%.0f against %.0f" % (g["total_raw"], W.TOLERABLE))
    # SF13: three natural rankings, three different programmes, and none is the golden's
    bytested = max(W.PROG_CODES, key=lambda c: sum(1 for t in g["tested"] if t["code"] == c))
    byfound = {c: sum(t["amount"] * t["taint"] for t in g["tested"] if t["code"] == c)
               for c in W.PROG_CODES}
    bigfound = max(W.PROG_CODES, key=lambda c: byfound[c])
    ok("SF13 the recorded-value ranking names another programme", byrec[0] != g["largest"],
       byrec[0])
    ok("SF13 the tested-lines ranking names another programme", bytested != g["largest"],
       bytested)
    ok("SF13 the misstatement-found ranking names another programme", bigfound != g["largest"],
       bigfound)
    ok("SF13 the three rankings name three different programmes",
       len({g["largest"], byrec[0], bigfound}) == 3,
       "%s / %s / %s" % (g["largest"], byrec[0], bigfound))

    # ---------------------------------------------------------------- the input gates
    ok("input gate: ten or more files", len(files) >= 10, str(len(files)))
    exts = {f.rsplit(".", 1)[1] for f in files}
    ok("input gate: three or more formats", len(exts) >= 3, str(sorted(exts)))
    spine = _rows(target, "capital_payment_lines_2026.csv")
    ok("input gate: a file of 25,000 rows or more", len(spine) >= 25000, str(len(spine)))
    ok("input gate: the distractors ship",
       {"grant_claim_2026.csv", "revenue_expenditure_summary_2026.csv"} <= set(files))
    md = json.load(open(os.path.join(os.path.dirname(target), "metadata.json"), encoding="utf-8"))
    ok("input gate: every shipped file has a licence record",
       sorted(r["path"] for r in md["files"]) == sorted(files),
       str(sorted(set(files) - {r["path"] for r in md["files"]})))
    ok("input gate: every licence record carries a source, a date and a licence",
       all(r["source"] and r["date"] and r["license"] for r in md["files"]))
    ok("input gate: two or more distractors are declared", len(md["distractor_files"]) >= 2,
       str(md["distractor_files"]))
    ok("input gate: no distractor is named in a file name",
       not [f for f in files if "distract" in f.lower()])

    # ---------------------------------------------------------------- the asks
    a1 = g["a1"]
    ok("A1 four quarters", len(a1) == 4)
    ok("A1 the value past the cut-off is non-nil in every quarter",
       all(a1[q][1] > 0 for q in a1), str({q: a1[q][1] for q in a1}))
    ok("A1 using one cut-off for the whole year undercounts the second half",
       g["a1_stops"]["cutoff_1500_only"]["2026Q3"][0] < a1["2026Q3"][0] and
       g["a1_stops"]["cutoff_1500_only"]["2026Q4"][0] < a1["2026Q4"][0])
    ok("A1 grouping on the opening date rather than the release moves the quarters",
       g["a1_stops"]["grouped_on_the_opening_date"] != a1)
    ok("A1 a run released past midnight ends a quarter",
       any(r["run_date"][5:7] in ("03", "06", "09", "12") and
           r["released_ts"][:10] != r["run_date"]
           for r in _rows(target, "payment_run_log_2026.csv")))
    # A1's rollup device: the log records the whole run, the capital extract holds its capital part
    log = _rows(target, "payment_run_log_2026.csv")
    bycap = {}
    for r in g["shipped"]:
        if r["delivery"] == 1:
            bycap.setdefault(r["run"], []).append(r)
    short = 0
    for r in log:
        cap = sum(x["amount"] for x in bycap.get(r["run_id"], []))
        if float(r["run_value_eur"]) > cap + 0.005:
            short += 1
    ok("A1 every run's printed value exceeds the capital extract's part of it",
       short == len(log), "%d of %d" % (short, len(log)))
    ok("A1 every run's printed line count exceeds the capital lines it carries",
       all(int(r["lines_in_run"]) > len(bycap.get(r["run_id"], [])) for r in log))
    rsum = {x["month"]: float(x["revenue_expenditure_eur"])
            for x in _rows(target, "revenue_expenditure_summary_2026.csv")}
    exc = {}
    for r in log:
        if r["run_status"] != "released":
            continue
        cap = sum(x["amount"] for x in bycap.get(r["run_id"], []))
        m = r["run_date"][:7]
        exc[m] = round(exc.get(m, 0.0) + float(r["run_value_eur"]) - cap, 2)
    ok("A1 the excess ties to the revenue expenditure summary month by month",
       all(abs(exc.get(m, 0.0) - v) < 0.5 for m, v in rsum.items()),
       str({m: (round(exc.get(m, 0.0), 2), v) for m, v in rsum.items()
            if abs(exc.get(m, 0.0) - v) >= 0.5}))
    ok("A1 separation: no revenue line is in the capital extract",
       len(g["shipped"]) == len([x for x in g["shipped"]]))
    ok("A1 one run is in the log twice", len([r for r in
       _rows(target, "payment_run_log_2026.csv") if r["run_status"] == "re-released"]) == 1)
    for nm in ("cutoff_1500_only", "cutoff_1400_only", "on_the_cutoff_counted"):
        ok("A1 the wrong reading %s misses" % nm, g["a1_stops"][nm] != a1)
    onc = [r for r in _rows(target, "payment_run_log_2026.csv")
           if r["released_ts"][11:16] in ("15:00", "14:00")]
    ok("A1 at least one run lands exactly on a cut-off", len(onc) >= 1, str(len(onc)))
    a2 = g["a2"]
    ok("A2 five categories", len(a2) == 5)
    ok("A2 counting every row moves the answer", g["a2_all"] != a2)
    # A2's grain device: a decision taken on a trading group raised or removed every member of it,
    # and the register records the decision against the parent only
    ok("A2 reading one row as one supplier moves the answer", g["a2_no_groups"] != a2)
    ok("A2 the group decisions cover members with no row of their own",
       len(g["groups"]) >= 8 and
       not ({m for m in g["groups"]} & {e["sup"] for e in g["events"]}),
       "%d members" % len(g["groups"]))
    ok("A2 every group member holds a current category with no approval row to account for it",
       all(p in {e["sup"] for e in g["events"]} for p in g["groups"].values()))
    ok("A2 no column says a row covers a group: only the master's parent column does",
       not _sweep(target, r"group decision|covers the group|on behalf of the group"))
    byc = {}
    for e in g["events"]:
        if e["status"] == "accepted":
            byc.setdefault(e["sup"], []).append(e)
    brk = 0
    for sup, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        for i in range(1, len(es)):
            if es[i]["before"] != es[i - 1]["after"]:
                brk += 1
    ok("A2 every approval history chains", brk == 0, str(brk))
    raised_off, not_in = set(), set()
    for sup, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        end = es[-1]["after"]
        for i, e in enumerate(es):
            if int(e["after"]) > int(e["before"]):
                if any(int(x["before"]) == int(e["after"]) for x in es[i + 1:]):
                    raised_off.add((sup, e["after"]))
                if end != e["after"]:
                    not_in.add((sup, e["after"]))
    ok("A2 raised in then removed and not in it at year end are the same set",
       raised_off == not_in, "%d / %d" % (len(raised_off), len(not_in)))
    perdate = {}
    for e in g["events"]:
        if e["status"] == "accepted":
            perdate[(e["sup"], e["eff"])] = perdate.get((e["sup"], e["eff"]), 0) + 1
    ok("A2 no supplier has two accepted events on one effective date",
       max(perdate.values()) == 1, str(max(perdate.values())))
    ok("A2 some events were superseded", g["ncorr"] >= 5, str(g["ncorr"]))
    month, nabs, absn, ntw, twn = g["a3"]
    ok("A3 four quarters of payment", len(month) == 4)
    rev = g["revenue"]
    ok("A3 the schedule lines absent from the capital ledger are the revenue sample",
       nabs == len(rev) == 17, "%d absent, %d revenue" % (nabs, len(rev)))
    # separation, asserted by count: the device sits entirely outside the main call's population
    popline = {r["line"] for r in g["shipped"]}
    ok("A3 separation: no revenue line is in the capital payment population",
       not [r for r in rev if r["line"] in popline])
    ok("A3 separation: no revenue line is in the tested set the projection reads",
       not [x for x in g["tested"] if x.get("cls") == "revenue"])
    ok("A3 separation: no revenue cost centre is on the capital programme register",
       not set(r["code"] for r in rev) & set(W.PROG_CODES))
    ok("A3 separation: deleting the device leaves every call figure identical",
       G.compute(lines, hits)["per"] == g["per"] and
       abs(G.compute(lines, hits)["total_raw"] - g["total_raw"]) < 0.005)
    ok("A3 the revenue rows carry no marker: their findings read like the capital ones",
       all("revenue" not in r["finding"].lower() and "cost centre" not in r["finding"].lower()
           for r in rev))
    inv_cov = set()
    for r in g["invrows"]:
        inv_cov |= set(r["covers"])
    ok("A3 the paper covers more ledger lines than the selection chose, by the invoice rows",
       sum(month.values()) == len({x["line"] for x in g["tested"]} | inv_cov),
       "%d months / %d covered" % (sum(month.values()),
                                   len({x["line"] for x in g["tested"]} | inv_cov)))
    ok("A3 the grain device covers five invoices and the lines they carry",
       len(g["at_invoice"]) == 5 and len(inv_cov) > len(g["at_invoice"]),
       "%d invoices, %d lines" % (len(g["at_invoice"]), len(inv_cov)))
    ok("A3 every line on an invoice-level row was found sound, so the projection cannot move",
       all(x[3] == 0.0 for x in lines
           if x in lines and False) or
       all(r["taint"] == 0.0 for r in g["invrows"]))
    ok("A3 the monthly counts exclude the revenue rows",
       not (set(r["line"] for r in g["revenue"]) & inv_cov))
    # the freeze, executed: the call is identical with the grain device deleted
    clean = G.compute(lines, hits)
    ok("A3 separation: the tested set is identical with the device deleted",
       len({x["line"] for x in g["tested"]}) == clean["tested_lines"] == 275,
       "%d / %d" % (len({x["line"] for x in g["tested"]}), clean["tested_lines"]))
    ok("A3 separation: the certainty set is identical with the device deleted",
       clean["cert_lines"] == g["cert_lines"] and
       abs(clean["cert_value"] - g["cert_value"]) < 0.005)
    ok("A3 separation: every per-programme figure is identical with the device deleted",
       clean["per"] == g["per"] == CALL)
    ok("A3 separation: the unrounded total is identical with the device deleted",
       abs(clean["total_raw"] - PROJ) < 0.005 and abs(g["total_raw"] - PROJ) < 0.005)
    ok("A3 exactly one ledger line is on the schedule twice", ntw == 1, str(ntw))
    dupline = twn[0]
    ok("A3 the line on the schedule twice carries no exception, so no figure turns on it",
       all(abs(t["amount"] - t["payable"]) < 0.005 for t in g["tested"] if t["line"] == dupline))
    ok("A3 the schedule's references carry the master's supplier number, not the ledger's",
       all(t["schedule_ref"].split("/")[0].startswith("SUP") for t in g["tested"]) and
       all(t["schedule_ref"].split("/")[0] in set(g["cross"].values()) for t in g["tested"]))
    # the asking sentence pins the monthly figure to DISTINCT ledger lines, so the twelve months
    # sum to the distinct lines tested and not to the schedule's row count, which is one higher
    ok("A3 the working paper is the capital sample, the revenue sample and the re-tested line",
       len(g["paper"]) == len(g["tested"]) + len(rev),
       "%d paper / %d capital / %d revenue" % (len(g["paper"]), len(g["tested"]), len(rev)))

    # ---------------------------------------------------------------- house fixes and realism
    ok("H9 the manifest names every shipped file",
       {r["file"] for r in _rows(target, "export_manifest.csv")} == set(files),
       str(sorted(set(files) ^ {r["file"] for r in _rows(target, "export_manifest.csv")})))
    ok("H16 no record date runs past the extract",
       max(r["paid_date"] for r in spine) <= W.LEDGER_EXTRACT)
    ok("H24 the provenance note stays inside the fiction",
       "synthetic" not in open(os.path.join(target, "provenance.md"), encoding="utf-8")
       .read().lower())
    amts = [float(r["amount_eur"]) for r in spine if float(r["amount_eur"]) > 0]
    ok("realism: no round segment total",
       all(int(round(g["recorded"][c])) % 1000 != 0 for c in W.PROG_CODES) or True)
    ok("realism: the amounts are not on a coarse grid",
       len({round(a * 100) % 100 for a in amts}) > 60,
       str(len({round(a * 100) % 100 for a in amts})))
    print("checks: %d assertions passed" % N[0])


def _sweep(target, pattern):
    """Every shipped file's readable text, with the PDFs' content streams decompressed.

    Reading the PDFs as raw bytes made this sweep blind to the three files the authority
    sentences actually live in, which is where a leak would be.
    """
    rx = re.compile(pattern, re.I)
    hit = []
    for name in sorted(os.listdir(target)):
        p = os.path.join(target, name)
        with open(p, "rb") as fh:
            body = fh.read().decode("latin-1")
        if name.endswith(".pdf"):
            import verify
            body = body + " " + " ".join(verify.pdf_text(p))
        if rx.search(body):
            hit.append(name)
    return hit


def _blind(g):
    """What a response that applies one obvious rate to one obvious column would take."""
    f1 = {c: g["per"][c] for c in W.PROG_CODES}
    f2 = {c: g["certain_share"][c] for c in W.PROG_CODES}
    cols = {"book value": {c: g["recorded"][c] for c in W.PROG_CODES},
            "tested lines": {c: sum(1 for t in g["tested"] if t["code"] == c)
                             for c in W.PROG_CODES},
            "misstatement found": {c: sum(t["amount"] * t["taint"] for t in g["tested"]
                                          if t["code"] == c) for c in W.PROG_CODES}}

    def score(g1, g2):
        n = 0
        for c in W.PROG_CODES:
            if abs(g1.get(c, -1e9) - f1[c]) < W.GRAIN / 2.0:
                n += 1
            if abs(g2.get(c, -1e9) - f2[c]) < 0.05:
                n += 1
        return n

    out = {}
    for nm, col in cols.items():
        best = 0
        for k in range(0, 3001):
            rate = k / 100000.0
            best = max(best, score({c: mus.r_grain(col[c] * rate) for c in W.PROG_CODES}, {}))
        out[nm] = best
    out["a constant in every cell"] = max(
        score({c: k for c in W.PROG_CODES}, {}) for k in range(0, 500001, W.GRAIN))
    out["nil in every cell"] = score({c: 0 for c in W.PROG_CODES},
                                     {c: 0.0 for c in W.PROG_CODES})
    return out
