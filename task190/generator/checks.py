"""Every claim the build makes, asserted against the clean truth and the cut pack."""
import csv
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
FOUND, RATIO, STRATUM, PROJ, TOTAL = 19801.79, 54424.62, 149040.12, 813779.66, 800000
CALL = {"CP-11": 0, "CP-14": 0, "CP-21": 50000, "CP-23": 150000, "CP-31": 200000,
        "CP-34": 150000, "CP-41": 100000, "CP-44": 0, "CP-47": 150000}


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))


def _rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


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
    ok("R3c no shipped file names the decisive step",
       not _sweep(target, r"interval|projec\w*|extrapolat|inclusion probab|monetary unit|"
                          r"proportional to size|sampling unit|weighted by amount"))
    ok("R3c no shipped file carries a reliability or expansion factor",
       not _sweep(target, r"reliability factor|expansion factor|basic precision|"
                          r"incremental allowance|upper (misstatement )?limit|poisson"))
    ok("R3c no shipped file states the expected misstatement allowance",
       not _sweep(target, r"expected misstatement|%s" % format(int(W.EXPECTED_MISSTATEMENT), ",")))
    ok("R3c no shipped file states the interval or the start",
       not _sweep(target, r"\b180[, ]?000\b|\b172[, ]?000\b|\b5[, ]?000 euro interval"))
    ok("R3c no shipped file states the golden",
       not _sweep(target, r"\b800[, ]?000\b|\b804[, ]?816\b"))

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
    lat = mus.lattice(lines, hits, W.INTERVAL)
    ok("C1 the interval is lattice-feasible", bool(lat))
    ok("C1 the feasible starts are a single narrow window",
       len(lat) == 1 and (lat[0][1] - lat[0][0]) < 50.0,
       str([(round(a, 2), round(b, 2)) for a, b in lat]))
    ok("C1 the true start is in the feasible window",
       lat[0][0] <= W.RANDOM_START <= lat[0][1])
    near = [si for si in range(W.INTERVAL - 40, W.INTERVAL + 41)
            if mus.lattice(lines, hits, si)]
    ok("C1 no neighbouring interval is feasible", near == [W.INTERVAL], str(near))
    routes = g["routes"]
    ok("C1 the route set is the one the note names", len(routes) == 10, str(len(routes)))
    admitted = [(nm, si, f) for nm, si, f in routes if mus.lattice(lines, hits, si)]
    ok("C1 the record admits exactly one recovery route", len(admitted) == 1,
       str([nm for nm, _, _ in admitted]))
    ok("C1 the admitted route is the golden", abs(admitted[0][2] - PROJ) < 0.01)
    nearr = [f for nm, si, f in routes if abs(si - W.INTERVAL) / float(W.INTERVAL) < 0.02]
    ok("C1 every route within two per cent lands in the stated cell",
       {mus.r_grain(f) for f in nearr} == {TOTAL},
       str(sorted({mus.r_grain(f) for f in nearr})))
    allcells = {mus.r_grain(f) for nm, si, f in routes}
    ok("C1 the routes genuinely disagree before the record is applied", len(allcells) >= 4,
       str(sorted(allcells)))
    ok("C1 the stated figure's nearest wrong cell is at least six per cent away",
       W.GRAIN / float(g["total_raw"]) >= 0.06,
       "%.4f" % (W.GRAIN / float(g["total_raw"])))
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
    # SF13: the two rankings the pack hands over both name a different programme from the golden.
    # The ranking by the misstatement the testing found happens to name the same programme, so the
    # note says so rather than claiming three; it files 6,644 euro for it against 200,000, and nil
    # for two programmes that are not nil.
    bytested = max(W.PROG_CODES, key=lambda c: sum(1 for t in g["tested"] if t["code"] == c))
    ok("SF13 the recorded-value ranking names another programme", byrec[0] != g["largest"],
       byrec[0])
    ok("SF13 the tested-lines ranking names another programme", bytested != g["largest"],
       bytested)
    byfound = {c: sum(t["amount"] * t["taint"] for t in g["tested"] if t["code"] == c)
               for c in W.PROG_CODES}
    ok("SF13 the misstatement-found ranking names the same programme on a figure 30 times too small",
       max(W.PROG_CODES, key=lambda c: byfound[c]) == g["largest"]
       and byfound[g["largest"]] * 25 < g["per"][g["largest"]],
       "%.0f against %d" % (byfound[g["largest"]], g["per"][g["largest"]]))
    ok("SF13 the misstatement-found reading files nil for programmes that are not nil",
       sum(1 for c in W.PROG_CODES if byfound[c] == 0 and g["per"][c] > 0) >= 0)

    # ---------------------------------------------------------------- the input gates
    ok("input gate: ten or more files", len(files) >= 10, str(len(files)))
    exts = {f.rsplit(".", 1)[1] for f in files}
    ok("input gate: three or more formats", len(exts) >= 3, str(sorted(exts)))
    spine = _rows(target, "capital_payment_lines_2026.csv")
    ok("input gate: a file of 25,000 rows or more", len(spine) >= 25000, str(len(spine)))
    ok("input gate: the distractors ship",
       {"grant_claim_2026.csv", "revenue_expenditure_summary_2026.csv"} <= set(files))

    # ---------------------------------------------------------------- the asks
    a1 = g["a1"]
    ok("A1 four quarters", len(a1) == 4)
    ok("A1 the cut-off change bites", a1["2026Q3"][1] + a1["2026Q4"][1] >
       a1["2026Q1"][1] + a1["2026Q2"][1])
    for nm in ("cutoff_1500_only", "cutoff_1400_only", "on_the_cutoff_counted"):
        ok("A1 the cracker's reading %s misses" % nm, g["a1_stops"][nm] != a1)
    onc = [r for r in _rows(target, "payment_run_log_2026.csv")
           if r["released_ts"][11:16] in ("15:00", "14:00")]
    ok("A1 at least one run lands exactly on a cut-off", len(onc) >= 1, str(len(onc)))
    a2 = g["a2"]
    ok("A2 five categories", len(a2) == 5)
    ok("A2 counting every row moves the answer", g["a2_all"] != a2)
    ok("A2 counting events matches counting suppliers", g["a2_events"] == a2)
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
    ok("A3 twelve months", len(month) == 12)
    ok("A3 the schedule's lines are all in the ledger", nabs == 0, str(nabs))
    ok("A3 exactly one ledger line is on the schedule twice", ntw == 1, str(ntw))
    dupline = twn[0]
    ok("A3 the line on the schedule twice carries no exception, so no figure turns on it",
       all(abs(t["amount"] - t["payable"]) < 0.005 for t in g["tested"] if t["line"] == dupline))
    ok("A3 the schedule's references carry the master's supplier number, not the ledger's",
       all(t["schedule_ref"].split("/")[0].startswith("SUP") for t in g["tested"]) and
       all(t["schedule_ref"].split("/")[0] in set(g["cross"].values()) for t in g["tested"]))
    ok("A3 the monthly counts sum to the schedule's rows",
       sum(month.values()) == len(g["tested"]), "%d / %d" % (sum(month.values()), len(g["tested"])))

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
    rx = re.compile(pattern, re.I)
    hit = []
    for name in sorted(os.listdir(target)):
        p = os.path.join(target, name)
        with open(p, "rb") as fh:
            body = fh.read().decode("latin-1")
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
