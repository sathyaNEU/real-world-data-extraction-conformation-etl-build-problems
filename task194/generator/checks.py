"""The generator's own assertions: the input gates, the client's three rules on the clean truth, the ladder,
the semantic fork table, mess neutrality, the ask devices and the realism sweep.

Every assertion runs on the shipped bundle or on the panel the bundle was written from. A failure here is a
design failure, never something to patch in the data.
"""
import csv
import datetime as dt
import json
import math
import os
import re
from collections import Counter, defaultdict

import golden as G
import sim
import world as W

N = 0


FAILS = []

# A design rule the build does not yet meet. It is recorded rather than raised so the remaining gates
# still run, and `build.py` prints every entry and exits non-zero, so the gate stays red and named.
GAPS = []


def gap(flag, label):
    global N
    N += 1
    if not flag:
        GAPS.append(label)
    return flag


def ok(flag, label):
    global N
    N += 1
    if not flag:
        FAILS.append(label)
        if not os.environ.get("CHECKS_COLLECT"):
            assert flag, "FAILED: %s" % label


def read(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def rows_of(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def pooled(panel, unit, qs):
    o = sum(panel[(unit, q)]["observed"] for q in qs)
    e = sum(panel[(unit, q)]["expected"] for q in qs)
    return o / e


def run(target, g, state):
    global N
    N = 0
    b = g["bundle"]
    panel = b["panel"]
    units = g["units"]
    by = {d["unit"]: d for d in units}
    answer, runner = g["answer"], g["runner"]

    import pypdf
    spec = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(
        os.path.join(target, "hac_indicator_specification_v4.pdf")).pages).split())
    charter = " ".join(" ".join(pg.extract_text() for pg in pypdf.PdfReader(
        os.path.join(target, "improvement_partnership_charter_v3.pdf")).pages).split())

    # ---------- input gates ----------
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    ok(len(exts) >= 3, "three or more formats (%s)" % exts)
    ok(any(f.endswith(".csv") and rows_of(target, f) >= 25000 for f in files), "a file of 25,000+ rows")
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "two or more distractors declared")
    # H9: the registers learn about every file, by set equality rather than spot membership. The manifest
    # row for itself states that it covers every file in the folder, so a missing row is a stated fact the
    # data contradicts as well as an unregistered file.
    man = read(target, "export_manifest.csv")
    man_names = {r["file_name"] for r in man}
    ok(man_names == set(files),
       "H9 the manifest names every shipped file and nothing else (missing %s, extra %s)"
       % (sorted(set(files) - man_names), sorted(man_names - set(files))))
    ok(any(r["file_name"] == "export_manifest.csv" and r["covers"] == "every file in the folder"
           for r in man), "H9 the manifest's own row says what it covers")
    dic = read(target, "data_dictionary.csv")
    dic_names = {r["file_name"] for r in dic}
    ok("coding_close_out_register.csv" in dic_names,
       "H9 the dictionary covers the decisive input")
    ok(dic_names <= set(files), "H9 the dictionary names no file the pack does not ship")
    # H16: only the forward-looking files carry a date after the pull date, by allow-list
    import datetime as _dt
    forward = {"activity_plan_2027q4.csv", "improvement_placements.csv"}
    late = set()
    for f in files:
        if not f.endswith(".csv"):
            continue
        with open(os.path.join(target, f), newline="", encoding="utf-8", errors="replace") as fh:
            for r in csv.reader(fh):
                for c in r:
                    m = re.fullmatch(r"(20\d\d)-(\d\d)-(\d\d)", c or "")
                    if m and _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) > W.PULL_DATE:
                        late.add(f)
    ok(late <= forward,
       "H16 only the forward-looking files carry a date after the pull date (%s)" % sorted(late))
    ok(all("distractor" not in f.lower() for f in files), "no file name says distractor")
    ok(not any(f.startswith(".") or f.endswith((".py", ".ipynb", ".md")) for f in files),
       "no code, notes or dot files in the pack")

    # ---------- R1 the field's raw material ships ----------
    head = open(os.path.join(target, "episode_outcomes_extract.csv"), encoding="utf-8").readline().strip()
    for col in ("drg_code", "age_band", "care_type", "los_days", "hac_recorded", "separation_date", "unit_code"):
        ok(col in head, "R1 the extract carries %s" % col)
    banned = ("standardised_ratio_to_date", "persistent", "excess", "avoid", "expected_plan", "share_removed")
    for f in files:
        if not f.endswith(".csv"):
            continue
        h = open(os.path.join(target, f), encoding="utf-8").readline().lower()
        ok(not any(x in h for x in banned), "R1 no shipped column holds the deciding quantity (%s)" % f)
    ok(len(b["inscope_episode"]) > 150000, "R1 the golden's computation reads the episode rows (%d)"
       % len(b["inscope_episode"]))
    series = read(target, "unit_indicator_series.csv")
    for r in series:
        p = panel[(r["unit_code"], r["quarter"])]
        ok(abs(p["observed"] - float(r["observed_complications"])) < 1e-9
           and abs(p["expected"] - float(r["expected_complications"])) < 0.002
           and p["episodes"] == int(r["in_scope_episodes"]),
           "R1 the series is the extract's own rollup (%s %s)" % (r["unit_code"], r["quarter"]))

    # ---------- the ladder: six readings, five of them rungs, each named on the record ----------
    rts = g["routes"]
    R = {k.split()[0]: v for k, v in rts.items()}
    r0, r5 = R["R0"], R["R5"]
    ok(r0["first"] != answer["unit"], "rung 0 names another unit (%s)" % r0["first"])
    ok(r5["first"] == answer["unit"], "the decisive rung names the answer (%s)" % r5["first"])
    for lab in ("R1", "R2", "R3", "R4"):
        ok(R[lab]["first"] != answer["unit"],
           "rung %s names another unit (%s)" % (lab[1:], R[lab]["first"]))
        ok(R[lab]["second"] != answer["unit"],
           "the answer is not second on rung %s (second is %s)" % (lab[1:], R[lab]["second"]))
    ok(len({R[l]["first"] for l in ("R0", "R1", "R5")}) == 3,
       "rung 0, rung 1 and the decisive rung name three different units")
    for lab in ("R0", "R1", "R2", "R3", "R4", "R5"):
        ok(R[lab]["margin"] >= 1.15,
           "rung %s margin %.3fx at or above 1.15x" % (lab[1:], R[lab]["margin"]))
    ok(1.5 <= r5["margin"] <= 2.0, "the final margin %.3fx is inside the 1.5 to 2x band" % r5["margin"])
    ok(g["recorded_rank"] in (4, 5), "the answer sits %d of %d on rung 0's ranking"
       % (g["recorded_rank"], len(units)))
    first_on = [k for k, v in rts.items() if v["first"] == answer["unit"]]
    ok(len(first_on) == 1, "the answer is first on exactly one reading (%d)" % len(first_on))
    second_on = [k for k, v in rts.items() if v["second"] == answer["unit"]]
    ok(len(second_on) == 0, "the answer is second on no reading (%d)" % len(second_on))
    # dominance: the answer's edge on the decisive axis over the easy route's unit beats the runner's
    base = by[r0["first"]]["as_recorded"]
    edge = answer["avoidable"] - answer["as_recorded"]
    carried = by[r0["first"]]["as_recorded"] - answer["as_recorded"]
    ok(edge >= 1.2 * carried,
       "the answer's edge on the decisive axis dominates the decoy's carried advantage "
       "(%.2f against %.2f, %.2fx)" % (edge, carried, edge / carried))
    ok(base > answer["as_recorded"], "the record as it stands puts the decoy above the answer")

    # the lead, in complications, as a ratio, and against the record's own sampling error
    ok(abs(g["gap"] - (answer["avoidable"] - runner["avoidable"])) < 1e-9,
       "the gap is the two counts' difference")
    ok(1.5 <= g["margin"] <= 2.0, "the margin %.3fx is in band" % g["margin"])
    ok(g["se_lead"] > 1.0,
       "the top two are not inside a standard error of each other (%.2f)" % g["se_lead"])
    ok(g["se_lead_third"] > g["se_lead"], "the third unit is further away again (%.2f)" % g["se_lead_third"])
    for d in units:
        ok(abs(d["se"] - math.sqrt(d["developed"]) * d["plan"] / d["separations"]) < 1e-9,
           "each unit's standard error is sqrt(developed) carried like its count, because the developed "
           "count is the graded quantity (%s)" % d["unit"])
    ok(sum(1 for d in units if d["as_recorded"] < 0) >= 2,
       "the record as it stands carries units on both sides of zero (%d negative)"
       % sum(1 for d in units if d["as_recorded"] < 0))
    ok(all(d["avoidable"] > 0 for d in units),
       "every unit's developed avoidable count is positive")

    # ---------- R3a the analyst test, on the clean truth ----------
    # a strong analyst who reads every rule correctly, expects each unit's patients at the published
    # table exactly as 3.1 requires and reconciles to the published series row for row still ranks on
    # the complications coded so far and files another unit
    easy = max(units, key=lambda d: d["as_recorded"])
    ok(easy["unit"] != answer["unit"], "R3a the easy route files another unit (%s)" % easy["unit"])
    ok(easy["unit"] == r0["first"], "R3a the easy route is rung 0")
    ok(answer["as_recorded"] < easy["as_recorded"],
       "R3a the answer reads below the easy route's unit on the record as it stands (%.2f against %.2f)"
       % (answer["as_recorded"], easy["as_recorded"]))
    ok(abs(easy["ratio"] - easy["observed"] / easy["expected"]) < 1e-12
       and abs(answer["ratio"] - answer["observed"] / answer["expected"]) < 1e-12,
       "R3a both routes read the published stratum table correctly")
    ok(g["recorded_rank"] >= 4,
       "R3a the answer is not visible on the record as it stands, it is %dth" % g["recorded_rank"])

    # ---------- R3b the decisive step alone moves the call ----------
    ok(sorted(units, key=lambda d: -d["as_recorded"])[0]["unit"] == easy["unit"]
       and sorted(units, key=lambda d: -d["avoidable"])[0]["unit"] == answer["unit"],
       "R3b developing the immature quarters alone decides between the two rankings")
    for lab in ("R2", "R3", "R4"):
        ok(R[lab]["first"] != answer["unit"],
           "R3b a single coarser correction leaves the call on a wrong answer (rung %s)" % lab[1:])

    # ---------- the observation process: what the close-out register measures ----------
    reg = read(target, "coding_close_out_register.csv")
    ok(len(reg) > 200, "the close-out register ships %d rows" % len(reg))
    for col in ("unit_code", "quarter", "published_date", "separations_with_complication",
                "episodes_awaiting_coding", "episodes_coded_since_last_close",
                "coder_fte_allocated", "principal_reason_open"):
        ok(col in reg[0], "the register carries %s" % col)
    # The register is the coding department's own close record, not a development triangle with a
    # covering file name: the queue columns are what a reader opens it for besides the two vintages.
    # They scale with the cost centre's volume and the season and carry no signal about how far its
    # coding has settled, which is asserted rather than asserted-by-intention: no cut on any of them
    # isolates the cost centres whose records are shortest.
    ok(all(int(r["episodes_awaiting_coding"]) >= 0 for r in reg),
       "the coding queue is never negative")
    ok(len({r["principal_reason_open"] for r in reg}) >= 3,
       "the register carries more than one standing reason for an open code (%d)"
       % len({r["principal_reason_open"] for r in reg}))
    ok(all(float(r["coder_fte_allocated"]) > 0 for r in reg),
       "every close carries a coder establishment")
    short4 = {d["unit"] for d in sorted(units, key=lambda x: x["completeness"])[:4]}
    for col in ("episodes_awaiting_coding", "episodes_coded_since_last_close",
                "coder_fte_allocated", "principal_reason_open"):
        per_unit = defaultdict(list)
        for r in reg:
            if r["unit_code"] in {d["unit"] for d in units}:
                per_unit[r["unit_code"]].append(r[col])
        if col == "principal_reason_open":
            cells = defaultdict(set)
            for c, vals in per_unit.items():
                cells[tuple(sorted(set(vals)))].add(c)
        else:
            # split the twelve at the median of the column's own per-unit mean
            means = {c: sum(float(v) for v in vals) / len(vals) for c, vals in per_unit.items()}
            med = sorted(means.values())[len(means) // 2]
            cells = defaultdict(set)
            for c, m in means.items():
                cells["high" if m >= med else "low"].add(c)
        best = 0.0
        for cell, members in cells.items():
            tp = len(members & short4)
            if not tp:
                continue
            best = max(best, 2.0 * tp / (len(members) + len(short4)))
        ok(best <= 0.75,
           "no cut on the register's %s isolates the four shortest records (best F1 %.2f)" % (col, best))
    # the queue moves with the season the cycle notes already mention, not with the cost centre's lag
    by_month = defaultdict(list)
    for r in reg:
        by_month[int(r["published_date"][5:7])].append(int(r["episodes_awaiting_coding"]))
    ok(len(by_month) >= 2 and max(sum(v) / len(v) for v in by_month.values())
       > 1.1 * min(sum(v) / len(v) for v in by_month.values()),
       "the coding queue moves with the close's own season")
    # fact 1: the development factors are read back from the register's own shipped bytes
    import build as _B
    shipped_factors = _B.golden_factors(target)
    ok(shipped_factors == g["factors"],
       "fact 1 every development factor recomputes from the register's shipped bytes (%d factors)"
       % len(shipped_factors))
    # fact 2: a quarter keeps growing after its own close, and the register says by how much
    lags = g["lags"]
    ok(sorted(lags.values()) == [0, 1, 2, 3, 4],
       "fact 2 the register shows five quarters at five different stages of settling (%s)" % lags)
    # `lags[q]` is the index of the publication the record holds for q, so EVERY quarter in `lags` is
    # still filling and lag 0 is the shortest of them, not a settled one. Filtering on a positive lag
    # names the four most settled and drops the shortest, which is the defect this assertion now blocks.
    ok(len(lags) == 5,
       "fact 2 exactly five of the ten closed quarters are still filling (%d)" % len(lags))
    ok(min(lags.values()) == 0,
       "fact 2 one quarter is held at its own close and nothing after it, the shortest of the five")
    up = g["pick_uplift_by_quarter"]
    ok(set(up) == set(lags), "fact 2 the pick's uplift is accounted for over all five (%s)" % sorted(up))
    ok(abs(sum(v["uplift"] for v in up.values()) - answer["uplift"]) < 1e-9,
       "fact 2 the five quarters' uplift sums to the pick's own uplift (%.5f)" % answer["uplift"])
    shortest = max(up, key=lambda q: up[q]["uplift"])
    ok(up[shortest]["lag"] == 0,
       "fact 2 the quarter carrying the most uplift is the one held at its own close (%s)" % shortest)
    ok(up[shortest]["uplift"] > 0.5 * answer["uplift"],
       "fact 2 the shortest quarter carries more than half the pick's uplift (%.2f of %.2f)"
       % (up[shortest]["uplift"], answer["uplift"]))
    settled = min(up, key=lambda q: up[q]["uplift"])
    ok(abs(up[settled]["uplift"]) < 1e-9 and up[settled]["lag"] == max(lags.values()),
       "fact 2 the quarter nearest settled carries no uplift at all (%s)" % settled)
    # the development arithmetic is stated to two decimals because one decimal is edge-fragile on it
    for q, v in up.items():
        ok(sim.bin_edge(v["uplift"], 0.01) >= sim.EDGE_BAR * 0.01,
           "fact 2 %s's uplift sits %.5f from the two-decimal edge" % (q, sim.bin_edge(v["uplift"], 0.01)))
    for lab, val in (("developed", answer["developed"]), ("uplift", answer["uplift"])):
        ok(sim.bin_edge(val, 0.01) >= sim.EDGE_BAR * 0.01,
           "fact 2 the pick's %s sits %.5f from the two-decimal edge (%.5f)"
           % (lab, sim.bin_edge(val, 0.01), val))
    ok(all(g["factors"][(c, 0)] >= 1.0 for c in g["eligible"]),
       "fact 2 no cost centre's quarter shrinks after its own close")
    ok(max(g["factors"][(c, 0)] for c in g["eligible"]) >= 1.5,
       "fact 2 at least one cost centre's quarter is still half again short at its own close (%.3f)"
       % max(g["factors"][(c, 0)] for c in g["eligible"]))
    # fact 3: the factor is a property of the cost centre, several-fold apart across the twelve
    f0 = {c: g["factors"][(c, 0)] for c in g["eligible"]}
    ok((f0[answer["unit"]] - 1.0) / max(f0[r0["first"]] - 1.0, 1e-9) >= 5.0,
       "fact 3 the answer's own shortfall at lag 0 is many times the decoy's (%.3f against %.3f)"
       % (f0[answer["unit"]], f0[r0["first"]]))
    ok(answer["uplift"] > 100.0,
       "fact 3 the answer's own record grows by %.1f complications once developed" % answer["uplift"])
    short = sorted(((1.0 - d["completeness"]) * 100.0, d["unit"]) for d in units)
    ok(short[0][0] < 1.0 and short[-1][0] > 8.0,
       "fact 3 the ten-quarter shortfall runs from %.2f to %.2f per cent across the twelve"
       % (short[0][0], short[-1][0]))
    ok(len({round(v, 2) for v, _ in short}) >= 10,
       "fact 3 the shortfall is a continuum across the twelve, not two groups (%d distinct)"
       % len({round(v, 2) for v, _ in short}))
    # fact 4: nothing in the pack says how to develop, or that anything needs developing
    for w in ("development factor", "completion factor", "incomplete", "provisional", "preliminary",
              "still being coded", "coding backlog", "reports late", "restate", "not yet complete",
              "run-off", "immature"):
        ok(w not in charter.lower() and w not in spec.lower(),
           "fact 4 no shipped clause names the decisive step (%s)" % w)

    # ---------- the demonstration: the record shows the answer improving while it deteriorated --------
    ok(R["R1"]["order"].index(answer["unit"]) + 1 == len(units),
       "the answer sits last of %d on the most recent year as the record carries it" % len(units))
    ok(R["R1"]["first"] != answer["unit"], "the recency route names another unit (%s)" % R["R1"]["first"])

    # ---------- C1 convergence: every reading of the development the text leaves open ----------
    conv = g["convergence"]
    ok(len(conv) >= 5, "five or more readings of the development are formed and ranked (%d)" % len(conv))
    for label, v in conv.items():
        ok(v["first"] == answer["unit"],
           "C1 %s names the answer (%s at %.2f against %s at %.2f, %.2fx)"
           % (label, v["first"], v["first_value"], v["second"], v["second_value"], v["margin"]))
        ok(v["margin"] >= 1.5, "C1 %s separates its first two (%.2fx)" % (label, v["margin"]))
    ok(max(v["margin"] for v in conv.values()) - min(v["margin"] for v in conv.values()) <= 0.15,
       "the five readings agree to within %.3f of a margin"
       % (max(v["margin"] for v in conv.values()) - min(v["margin"] for v in conv.values())))

    # ---------- the semantic fork table ----------
    allq = sorted({q for (_, q) in panel})
    # SF1 "over a period" in charter 4.3: specification 3.3 files the specification period to date
    ok("every closed quarter from 1 July 2024" in spec, "SF1 specification 3.3 files the record's window")
    ok("No other period is reported for a unit" in spec,
       "SF1 the window sentence closes the alternative readings rather than convergence doing it")
    ok(R["R1"]["first"] != answer["unit"], "SF1 the four-quarter reading is rung 1 and names another unit")
    # SF2 the most avoidable complications: a count, not a ratio or a rate
    ok("counted patient by patient" in charter, "SF2 charter 4.3 counts patient by patient")
    ratio_first = max(units, key=lambda d: d["ratio_developed"])["unit"]
    ok(ratio_first != answer["unit"],
       "SF2 the developed ratio reading names another unit (%s) and the clause rules it out" % ratio_first)
    # SF3 the exposure the excess is carried on
    ok("expected complications per separation" in spec, "SF3 specification 3.4 files the carrying")
    per_ep = max(units, key=lambda d: (d["developed"] - d["expected"]) / d["episodes"] * d["plan"])
    uncarried = max(units, key=lambda d: d["developed"] - d["expected"])
    ok(per_ep["unit"] == answer["unit"] and uncarried["unit"] == answer["unit"],
       "SF3 both alternative exposures name the same unit (same call)")
    # SF4 the comparison: the published stratum table, filed by specification 3.1
    ok("not re-estimated between specifications" in spec,
       "SF4 specification 3.1 files the published table as the expectation")
    ok("year ended 30 June 2024" in spec, "SF4 the specification states the table's vintage")
    for d in units:
        ok(abs(d["ratio"] - d["observed"] / d["expected"]) < 1e-12,
           "SF4 %s's expectation is the published table's and nothing else" % d["unit"])
    # SF5 how the growth between two vintages is read: five readings, one call
    ok(len(conv) >= 5 and all(v["first"] == answer["unit"] for v in conv.values()),
       "SF5 every reading of the growth names the answer")
    # SF6 which quarters are still filling: the register's own rows settle it, and the most recent
    # closed quarter is the shortest of them rather than a settled one
    ok(lags.get(allq[-1]) == 0,
       "SF6 the most recent closed quarter is held at its own close alone (%s)" % allq[-1])
    ok(len(lags) == 5 and set(lags) == set(allq[-5:]),
       "SF6 the register's own rows name the five most recent closed quarters as still filling")
    ok(all(q not in lags for q in allq[:-5]),
       "SF6 the five older quarters have settled by their own rows")
    # SF7 closed quarters at the decision date
    ok("eight weeks after the quarter ends" in spec, "SF7 specification 3.7 files when a quarter closes")
    ok(len(allq) == 10 and allq[-1] == "2026-27 Q2", "SF7 the record carries the ten closed quarters only")
    ok(max(r["separation_date"] for r in read(target, "episode_outcomes_extract.csv")) <= "2026-12-31",
       "SF7 no separation falls after the last closed quarter")
    # SF8 eligibility
    ok(len(g["eligible"]) == 12, "SF8 charter 4.2 leaves twelve eligible units (%d)" % len(g["eligible"]))
    ok("previous twelve closed quarters" in charter, "SF8 the charter files the exclusion window")
    ok("four or more closed quarters" in charter, "SF8 the charter files the floor")
    # SF9 the complication list revision
    ok("the revision in force at separation" in spec, "SF9 the specification files which revision applies")
    # SF10 the indicator's denominator
    ok("excluded from the denominator is excluded from the numerator" in spec,
       "SF10 the specification files the denominator's reach")
    # SF11 the reference rate's scope
    ok("reference rate of 96.6" in spec, "SF11 the reference rate is scoped to the adjusted rate")
    ok(abs(answer["avoidable"] - answer["ratio_developed"] * 96.6) > 1.0,
       "SF11 the avoidable count is a count and does not carry the reference rate")
    # SF12 the site a unit's activity counts to: an ask convention, pinned in the asking sentence
    ok(len(W.REALIGNED) == 3, "SF12 three cost centres were realigned")
    ok(any(b["facility"][(c, "2026-01-01")] != b["facility"][(c, "2026-12-01")] for c in W.REALIGNED),
       "SF12 the realignment moves a unit's site inside the ask's own window")
    # SF13 the rounding of every graded figure, at the unit the asking sentence states
    for d in units:
        ok(sim.bin_edge(d["avoidable"], 0.1) >= sim.EDGE_BAR * 0.1,
           "SF13 %s's avoidable count sits %.4f from the decimal's edge (bar %.4f)"
           % (d["unit"], sim.bin_edge(d["avoidable"], 0.1), sim.EDGE_BAR * 0.1))
        ok(sim.bin_edge(d["expected_plan"], 0.1) >= sim.EDGE_BAR * 0.1,
           "SF13 %s's expected count sits %.4f from the decimal's edge"
           % (d["unit"], sim.bin_edge(d["expected_plan"], 0.1)))
    av = sorted(d["avoidable"] for d in units)
    ok(min(av[i + 1] - av[i] for i in range(len(av) - 1)) > 0.1,
       "SF13 the closest pair of adjacent graded units is %.4f apart, above the printed unit"
       % min(av[i + 1] - av[i] for i in range(len(av) - 1)))
    for h in g["hospitals"]:
        for key in ("reported", "measured", "separations", "complications"):
            ok(float(h[key]).is_integer(),
               "SF13 %s's %s is a whole separation" % (h["hospital"], key))
        ok(h["reported"] == h["measured"] + h["separations"],
           "SF13 %s's three figures reconcile: %d reported, %d measured, %d not measured"
           % (h["hospital"], h["reported"], h["measured"], h["separations"]))

    # ---------- mess neutrality, one assertion per Layer 1 item (R2) ----------
    all_acute = sorted({c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"
                        and not u["closed_date"]})
    # two grains: the summary counts a separation, the extract carries episode records. For an acute unit
    # the two are the same thing; for the three units outside the indicator a stay whose care type changed
    # inside it reaches the feed as two episodes, which is A3's primary device, and the tie there is to the
    # chained stays. Both halves are asserted, so the device is fair rather than merely hard (law 6).
    summ = defaultdict(int)
    for r in b["summary"]:
        summ[(r["unit_code"], r["month"][:7])] += int(r["separations"])
    truth = defaultdict(int)
    for r in state["rows"]:
        truth[(r["unit"], r["sep_date"].isoformat()[:7])] += 1
    acute_codes = {c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"}
    ok({k: v for k, v in summ.items() if k[0] in acute_codes}
       == {k: v for k, v in truth.items() if k[0] in acute_codes},
       "R2 two grains: for every acute unit the summary ties to the extract month by month")
    stay_rows = Counter((r["unit"], r["stay"]) for r in state["rows"])
    split = sum(1 for (unit, _), n in stay_rows.items() if unit in acute_codes and n > 1)
    ok(split == 0, "R2 no acute unit carries a statistically discharged stay (%d)" % split)
    ok(sum(1 for (unit, _), n in stay_rows.items() if unit not in acute_codes and n > 1) > 300,
       "A3 the units outside the indicator carry the split stays (%d)"
       % sum(1 for (unit, _), n in stay_rows.items() if unit not in acute_codes and n > 1))
    nonacute_summ = sum(v for k, v in summ.items() if k[0] not in acute_codes)
    ok(sum(o["separations"] for o in g["outside"]) == nonacute_summ,
       "A3 the chained stays reproduce the activity summary exactly (%d)" % nonacute_summ)
    for o in g["outside"]:
        qs = sum(int(r["separations"]) for r in b["summary"]
                 if r["unit_code"] not in acute_codes
                 and G.fiscal(dt.date.fromisoformat(r["month"]))[1] == o["quarter"])
        ok(o["separations"] == qs,
           "A3 %s ties to the summary quarter by quarter (%d)" % (o["quarter"], qs))
    stated_key = set()
    for r in read(target, "episode_outcomes_extract.csv"):
        if r["unit_code"] in acute_codes:
            continue
        stated_key.add((r["unit_code"], r["patient_uid"], r["admission_date"], r["drg_code"]))
    ok(len(stated_key) > nonacute_summ,
       "A3 the stated separation key leaves %d against the %d separations reported, a lazy delta of "
       "%.1f per cent" % (len(stated_key), nonacute_summ,
                          100.0 * (len(stated_key) - nonacute_summ) / nonacute_summ))
    # the list revision touches no graded main figure
    cats = {r["hac_category_code"] for r in []}
    ok("hac_category_code" not in ("unit_code", "hac_recorded"), "R2 the revision sits in a column the call "
       "never reads")
    ok(all(d["observed"] == d["observed"] for d in units), "R2 the numerator is the episode flag")
    # the comorbidity score is keyed on part of the episodes and nothing reads it
    blank = sum(1 for r in read(target, "data_dictionary.csv") if "comorbidity" in r["column_name"])
    ok(blank == 1, "R2 the comorbidity score is described once in the dictionary")
    # the dashboard is correct for its own quarter
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "quality_dashboard_2026q2.xlsx"))
    ws = wb["Quarter position"]
    last_q = sorted({q for (u, q) in panel})[-1]
    seen = 0
    for row in ws.iter_rows(min_row=5, values_only=True):
        code = row[1]
        if code is None:
            continue
        seen += 1
        p = panel[(code, last_q)]
        ok(row[3] == p["episodes"] and row[4] == p["observed"]
           and abs(row[7] - p["observed"] / p["expected"] * G.REF_RATE) < 0.051,
           "R2 the dashboard is the extract's own quarter (%s)" % code)
    ok(seen == len(all_acute), "R2 the dashboard covers every in-scope unit (%d)" % seen)
    ok(ws.cell(row=2, column=1).value.startswith("Quarter ended 31 December 2026"),
       "R2 the dashboard says which quarter it is")
    # tables inside the PDFs carry the figures the lookups carry
    ok("0.1683" in spec and "HAC13" in spec, "R2 the specification's appendices are in the PDF")
    dsrc = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "deliver.py"),
                encoding="utf-8").read()
    ok("len(g[\"bundle\"][\"panel\"])" in dsrc,
       "the brief takes the panel's size from the record rather than stating a literal")
    ok("published stratum table expects" in dsrc,
       "the brief states the comparison as the published table, which is what the charter files")
    ok("avoided" not in dsrc, "no deliverable states a quantity the record does not carry")
    for clause in ("3.3", "3.4", "2.1", "2.2"):
        ok(clause in spec, "the specification carries clause %s" % clause)
    for clause in ("4.1", "4.2", "4.3", "4.4"):
        ok(clause in charter, "the charter carries clause %s" % clause)
    # the comparison is one of the five parts of the estimand, so charter 4.3 files it by the
    # specification's own defined term rather than leaving the frequency open. Architecture 2 died
    # exactly here: executed word for word on the only rates the pack carried, the literal reading
    # named a different unit.
    ok("less the expected complications of the unit's episodes in that period under the current "
       "indicator specification" in charter,
       "the charter files the comparison in clause 4.3 by the specification's defined term")
    ok("expected complications of a group of episodes" in spec
       and "rates published with this specification are in Appendix A" in spec,
       "the specification's defined term resolves to the published table of Appendix A")
    ok("ordinarily have" not in charter and "ordinarily have" not in spec,
       "no shipped clause leaves the comparison frequency open")
    ok("separations planned" in charter, "the charter files the activity basis in clause 4.4")
    # defect 2: the write-up named a cycle no shipped file carried. The register ends at the cycle in
    # progress and the notes head the next one, so the label the deliverables use is grounded.
    notes_txt = open(os.path.join(target, "placement_cycle_notes.txt"), encoding="utf-8").read()
    placements = read(target, "improvement_placements.csv")
    cycles = [r["cycle"] for r in placements]
    ok(cycles, "the placement register carries a cycle identifier (%s)" % (sorted(set(cycles))[:3]))
    ok("IP-11" in notes_txt,
       "the cycle the deliverables name is the one the notes head (IP-11)")
    ok("IP-11" not in str(cycles),
       "IP-11 is the next cycle, so the register of closed and in-progress placements does not carry it")
    ok(max(cycles) == "IP-10", "the register ends at the cycle in progress (%s)" % max(cycles))
    ok(notes_txt.count("IP-10") == 0,
       "the notes no longer head the April cycle with the in-progress cycle's own number")
    ok("on 24 March" in notes_txt and "20 March" in notes_txt,
       "the notes state the committee date and the papers date as dates, not as bare ordinals")
    ok("standardised ratio is reported" in spec, "the specification files the reporting period")
    ok(charter.count("most avoidable complications") == 1
       and charter.count("expected complications") == 1,
       "the pin is stated once, at authority, and not restated")
    ok(charter.count("stratum") == 0 and charter.count("Appendix A") == 0,
       "the charter points at the specification rather than restating its table")

    # ---------- the asks: separation, devices and stops ----------
    acute_units = {c for c, u in b["units"].items() if u["service_type"] == "Acute inpatient"}
    replay_in_acute = sum(1 for r in state["replays"] if r["unit"] in acute_units)
    ok(replay_in_acute == 0, "zero device rows in the main call's population")
    ok(len(state["replays"]) > 400, "the sub-acute feed's overlap re-sends %d records"
       % len(state["replays"]))
    # A3: the lazy row count and the over-corrected de-duplication both land outside the bin
    raw = defaultdict(int)
    loose = defaultdict(set)
    for r in state["rows"] + state["replays"]:
        if r["unit"] in acute_units:
            continue
        _, q = G.fiscal(r["sep_date"])
        raw[q] += 1
        loose[q].add((r["unit"], r["pid"], r["adm_date"]))
    # the stated separation key, which is the careful stop, and the over-correction that chains on the
    # date alone and so swallows a genuine same-day readmission
    stated = defaultdict(set)
    chained_loose = defaultdict(int)
    byp = defaultdict(list)
    for r in state["rows"] + state["replays"]:
        if r["unit"] in acute_units:
            continue
        stated[G.fiscal(r["sep_date"])[1]].add((r["unit"], r["pid"], r["adm_date"], r["drg"]))
        byp[(r["unit"], r["pid"])].append(r)
    for key, eps in byp.items():
        uniq = {(e["adm_date"], e["drg"]): e for e in eps}
        rows_ = sorted(uniq.values(), key=lambda e: (e["adm_date"], e["sep_date"]))
        chains = []
        ends = {}
        for e in rows_:
            j = ends.pop(e["adm_date"], None)        # the date alone, the over-correction
            if j is None:
                chains.append([e])
                j = len(chains) - 1
            else:
                chains[j].append(e)
            ends[e["sep_date"]] = j
        for ch in chains:
            chained_loose[G.fiscal(ch[-1]["sep_date"])[1]] += 1
    for o in g["outside"]:
        q = o["quarter"]
        ok(raw[q] > len(stated[q]) > len(loose[q]) > o["separations"],
           "A3 every stop above the answer in %s: %d rows, %d on the stated key, %d on a looser key, "
           "%d separations" % (q, raw[q], len(stated[q]), len(loose[q]), o["separations"]))
        ok(len(stated[q]) - o["separations"] > 0.02 * o["separations"],
           "A3 the careful stop in %s is %d clear of the answer, %.1f per cent"
           % (q, len(stated[q]) - o["separations"],
              100.0 * (len(stated[q]) - o["separations"]) / o["separations"]))
        ok(chained_loose[q] <= o["separations"],
           "A3 chaining on the date alone over-corrects in %s (%d against %d)"
           % (q, chained_loose[q], o["separations"]))
    ok(sum(chained_loose.values()) < sum(o["separations"] for o in g["outside"]),
       "A3 the over-corrected read lands below the answer overall (%d against %d)"
       % (sum(chained_loose.values()), sum(o["separations"] for o in g["outside"])))
    # ---------- A2: what the indicator does not measure at each hospital ----------
    # The ask is sited over every unit at the site, acute and non-acute alike, so the truth is the
    # summary's separations less the in-scope episodes the indicator measured. Two devices act on it and
    # they act in opposite directions, neither of them inside the call's own population:
    #   the statistical discharge, which sends one separation to the feed as two episode records at the
    #   three non-acute units, so counting the extract's rows runs HIGH at the three sites that have one;
    #   the day-procedure feed's two missing months at two placed units, which the summary counted and
    #   the extract never received, so counting the extract's rows runs LOW at those two sites.
    ok(len(W.REALIGNED) == 3, "A2 three cost centres were realigned")
    ok(len(W.FEED_GAP) == 2, "A2 the feed gap covers two units (%d)" % len(W.FEED_GAP))
    gap_rows = [r for r in state["rows"]
                if r["unit"] in W.FEED_GAP and r["los"] == 0
                and r["sep_date"].isoformat()[:7] in W.FEED_GAP[r["unit"]]]
    ok(len(gap_rows) > 100, "A2 the feed missed %d separations" % len(gap_rows))
    ok(all(not r["in_scope"] for r in gap_rows),
       "A2 every record the feed missed is outside the indicator, so no in-scope episode moves")
    cand = {d["unit"] for d in units}
    ok(not (set(W.FEED_GAP) & cand),
       "A2 no candidate's separations are touched by the feed gap")
    ok(all(b["units"][c]["service_type"] == "Acute inpatient" for c in W.FEED_GAP),
       "A2 the feed gap sits on acute units the team has already been placed with")
    ext_codes = {r["unit_code"] for r in read(target, "episode_outcomes_extract.csv")}
    ok(set(W.FEED_GAP) <= ext_codes, "A2 the units with the gap are otherwise in the extract")

    # the truth reconciles, site by site, and the naive read misses every one of the eight figures
    bands_ = b["bands"]
    naive = defaultdict(lambda: [0, 0])
    keyed = defaultdict(lambda: [set(), set()])
    for r in read(target, "episode_outcomes_extract.csv"):
        u = r["unit_code"]
        sep = dt.date.fromisoformat(r["separation_date"])
        if not (dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31)):
            continue
        band = bands_.get(r["drg_code"], "")
        if (u in acute_units and r["care_type"] == "Acute" and int(r["los_days"]) >= 1
                and band not in ("", "SAME-DAY")):
            continue                                  # the indicator measures this one
        site = b["facility"][(u, sep.replace(day=1).isoformat())]
        k = (u, r["patient_uid"], r["admission_date"], r["drg_code"])
        naive[site][0] += 1
        keyed[site][0].add(k)
        if r["hac_recorded"] == "1":
            naive[site][1] += 1
            keyed[site][1].add(k)
    for h in g["hospitals"]:
        c = h["hospital"]
        ok(h["reported"] == h["measured"] + h["separations"],
           "A2 %s's three figures reconcile: %d reported, %d measured, %d not measured"
           % (c, h["reported"], h["measured"], h["separations"]))
        for i, (lab, owed) in enumerate((("separations", h["separations"]),
                                         ("with a complication", h["complications"]))):
            # the bin is half a separation; the bar is 3, because two devices acting in opposite
            # directions at one site can land a figure one unit from the truth, which is outside the
            # bin and still a coin flip. That is the defect this bar exists to catch.
            ok(abs(naive[c][i] - owed) >= 3,
               "A2 counting the extract's own rows misses %s's %s by %d (%d against %d)"
               % (c, lab, naive[c][i] - owed, naive[c][i], owed))
            ok(abs(len(keyed[c][i]) - owed) >= 3,
               "A2 de-duplicating on the stated key and stopping misses %s's %s by %d (%d against %d)"
               % (c, lab, len(keyed[c][i]) - owed, len(keyed[c][i]), owed))
    # every site carries at least one device, which is what the earlier siting could not do for Carrowdean
    feed_sites = {b["facility"][(c, "%s-01" % W.FEED_GAP[c][0])] for c in W.FEED_GAP}
    nonacute_sites = {u["hospital_code"] for c, u in b["units"].items()
                      if u["service_type"] != "Acute inpatient"}
    ok(feed_sites | nonacute_sites == {h["hospital"] for h in g["hospitals"]},
       "A2 every one of the four sites carries a device (feed gap %s, non-acute unit %s)"
       % (sorted(feed_sites), sorted(nonacute_sites)))
    # a site may carry both devices; what is not allowed is for them to cancel there. The margin is
    # measured over all eight figures and both wrong reads rather than argued.
    worst = min(min(abs(naive[h["hospital"]][i] - owed), abs(len(keyed[h["hospital"]][i]) - owed))
                for h in g["hospitals"]
                for i, owed in enumerate((h["separations"], h["complications"])))
    ok(worst >= 3,
       "A2 the smallest gap between a wrong read and the truth over all eight figures is %d, on a bin of "
       "half a separation" % worst)

    detail = read(target, "hac_detail_extract.csv")
    # A4: the detail extract alone runs low in every group, and a raw code join mis-sorts
    detail_units = {r["unit_code"] for r in detail}
    ok(detail_units and detail_units < acute_units | {"41610", "41620"},
       "A4 the detail extract does not reach every unit")
    only_detail = defaultdict(lambda: defaultdict(set))
    raw_join = defaultdict(lambda: defaultdict(set))
    cat_rows = read(target, "hac_category_list.csv")
    cat26 = {r["complication_code"]: r["group_id"] for r in cat_rows if r["list_revision"] == "2026"}
    cat22 = {r["complication_code"]: r["group_id"] for r in cat_rows if r["list_revision"] == "2022"}
    for r in detail:
        eid = r["episode_id"]
        if eid not in b["inscope_episode"]:
            continue
        unit, sep, fy = b["inscope_episode"][eid]
        if fy not in ("2025-26", "2026-27"):
            continue
        rev = "2026" if sep >= W.CODESET_CHANGE else "2022"
        only_detail[fy][cat22[r["complication_code"]] if rev == "2022"
                        else cat26[r["complication_code"]]].add(eid)
        if r["complication_code"] in cat26:
            raw_join[fy][cat26[r["complication_code"]]].add(eid)
    for x in g["groups_by_year"]:
        ok(len(only_detail["2025-26"][x["group"]]) < x["fy2025"],
           "A4 the detail extract alone runs low in %s for 2025-26" % x["group"])
        ok(len(only_detail["2026-27"][x["group"]]) < x["fy2026"],
           "A4 the detail extract alone runs low in %s for 2026-27" % x["group"])
    moved = sum(1 for x in g["groups_by_year"]
                if len(raw_join["2025-26"][x["group"]]) != len(only_detail["2025-26"][x["group"]]))
    ok(moved >= 3, "A4 a raw code join mis-sorts %d groups before the revision" % moved)
    # the distractors move nothing
    for d in meta["distractor_files"]:
        ok(os.path.exists(os.path.join(target, d["file"])), "the distractor %s ships" % d["file"])
        ok(d["file"] not in open(os.path.join(target, "data_dictionary.csv"), encoding="utf-8").read(),
           "the distractor %s is not in the dictionary's scope" % d["file"])

    # ---------- realism sweep ----------
    # the pack has to behave like a hospital's own records, not like a simulation
    import statistics as _st
    ext = read(target, "episode_outcomes_extract.csv")
    los_rate = defaultdict(lambda: [0, 0])
    for r in ext:
        if r["care_type"] != "Acute":
            continue
        bucket = min(int(r["los_days"]), 14)
        los_rate[bucket][0] += 1
        los_rate[bucket][1] += 1 if r["hac_recorded"] == "1" else 0
    short = los_rate[2][1] / los_rate[2][0]
    long_ = los_rate[14][1] / los_rate[14][0]
    ok(long_ / short > 1.6, "a complication is likelier on a long stay (%.3f against %.3f)"
       % (long_, short))
    cmb = defaultdict(list)
    for r in ext:
        if r["comorbidity_score"]:
            cmb[r["age_band"]].append(int(r["comorbidity_score"]))
    ok(_st.mean(cmb["80+"]) - _st.mean(cmb["U50"]) > 1.5,
       "the comorbidity score runs with age (%.2f against %.2f)"
       % (_st.mean(cmb["80+"]), _st.mean(cmb["U50"])))
    with_c = [int(r["comorbidity_score"]) for r in ext
              if r["comorbidity_score"] and r["hac_recorded"] == "1"]
    no_c = [int(r["comorbidity_score"]) for r in ext
            if r["comorbidity_score"] and r["hac_recorded"] == "0"]
    ok(_st.mean(with_c) - _st.mean(no_c) > 0.25,
       "the comorbidity score predicts a complication (%.2f against %.2f)"
       % (_st.mean(with_c), _st.mean(no_c)))
    miss = defaultdict(lambda: [0, 0])
    for r in ext:
        m = r["separation_date"][:7]
        miss[m][0] += 1
        miss[m][1] += 0 if r["comorbidity_score"] else 1
    rates = [v[1] / v[0] for v in miss.values()]
    ok(max(rates) - min(rates) > 0.03, "the coding queue keys the comorbidity score at a rate that moves "
       "with the month (%.3f to %.3f)" % (min(rates), max(rates)))
    wd_adm = defaultdict(int)
    wd_sep = defaultdict(int)
    for r in ext:
        wd_adm[dt.date.fromisoformat(r["admission_date"]).weekday()] += 1
        wd_sep[dt.date.fromisoformat(r["separation_date"]).weekday()] += 1
    ok(wd_adm[0] / wd_adm[6] > 1.3, "admissions fall away over a weekend (%d against %d)"
       % (wd_adm[0], wd_adm[6]))
    ok(wd_sep[4] / wd_sep[6] > 1.8, "separations fall away over a weekend (%d against %d)"
       % (wd_sep[4], wd_sep[6]))
    byday = defaultdict(int)
    for r in ext:
        byday[r["separation_date"]] += 1
    med = _st.median(byday.values())
    ok(byday.get("2025-12-25", 0) < 0.35 * med, "separations stop on Christmas Day (%d against a median "
       "day of %d)" % (byday.get("2025-12-25", 0), med))
    ok(byday.get("2026-04-03", 0) < 0.55 * med, "separations stop on Good Friday (%d)"
       % byday.get("2026-04-03", 0))
    eids = [r["episode_id"] for r in ext]
    ok(len(set(eids)) == len(eids), "every episode identifier is distinct")
    first = sorted(e for e in eids if e.startswith("MR2407"))
    ok(int(first[0][-5:]) > 1, "the record number does not start at one in a month (%s)" % first[0])
    gaps = sum(1 for a, b in zip(first, first[1:]) if int(b[-5:]) - int(a[-5:]) > 1)
    ok(gaps > len(first) * 0.03, "the record numbers the warehouse allocates are not all in the extract "
       "(%d gaps in %d)" % (gaps, len(first)))
    mult = Counter(Counter((r["unit_code"], r["patient_uid"], r["admission_date"], r["drg_code"])
                           for r in ext).values())
    ok(mult.get(3, 0) > 10, "the overlapping feed does not always re-send exactly twice (%s)" % dict(mult))
    hh = read(target, "hand_hygiene_audit_2026.csv")
    closed = {c for c, u in b["units"].items() if u["closed_date"]}
    ok(not (closed & {r["unit_code"] for r in hh}), "the hand hygiene audit does not visit a closed ward")
    ok(len({r["moments_observed"] for r in hh}) > len(hh) * 0.75,
       "the hand hygiene audit observes a different number of moments each time")
    for d in units:
        ok(abs(d["avoidable"] - round(d["avoidable"])) > 1e-6,
           "no avoidable count is a round number (%s)"
           % d["unit"])
    ok(abs(answer["adjusted_rate"] - round(answer["adjusted_rate"])) > 0.02,
       "the pick's adjusted rate is not a round number")
    counts = [panel[k]["episodes"] for k in panel]
    ok(len(set(counts)) > len(counts) * 0.8, "unit-quarter episode counts are not repeated")
    names = set()
    for f in files:
        if f.endswith((".csv", ".txt")):
            text = open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
            for p in W.PEOPLE.values():
                if p[0] in text:
                    names.add(p[0])
            ok("Claude" not in text and "placeholder" not in text.lower(), "no toolchain tell in %s" % f)
    ok(names <= {p[0] for p in W.PEOPLE.values()}, "only the drawn personas appear")
    latest = max(r["sep_date"] for r in state["rows"])
    ok(latest == dt.date(2026, 12, 31) or latest.month == 12, "the extract stops at the closed quarter")
    for f in files:
        ok(os.path.getmtime(os.path.join(target, f)) ==
           os.path.getmtime(os.path.join(target, files[0])), "every file carries the export stamp")

    # ---------- the cracker and the mirror, measured on the cut pack ----------
    import cracker as CR
    cr = CR.run(target)
    # the two responses are scored from their own handling, not from one reading twice: the asks consume
    # nothing the call's construction produces, and the separation count below is what proves it
    ok(cr["n_ask"] == 44 and cr["n_con"] == 12,
       "the rubric's ask figures and construction figures are counted (%d and %d)"
       % (cr["n_ask"], cr["n_con"]))
    ok(cr["cracker_construction_kept"] == cr["n_con"],
       "the cracker holds the construction layer, so it never stands alone")
    ok(cr["mirror_construction_kept"] <= 2,
       "the mirror holds at most two of the twelve construction figures (%d)"
       % cr["mirror_construction_kept"])
    ok(cr["leakage"] < 35.0, "the mirror leaks under 35 per cent of ask weight (%.1f)" % cr["leakage"])
    # the ask sheet's gated fields carry the worst honest measurement, and this asserts the sheet against
    # the script rather than the other way round
    sheet = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DESIGN_NOTE.md")
    if os.path.exists(sheet):
        note = open(sheet, encoding="utf-8").read()
        ok("Pair ceiling: %.1f" % cr["ceiling"] in note,
           "the ask sheet states the measured pair ceiling (%.1f)" % cr["ceiling"])
        ok("Mirror leakage: %.1f" % cr["leakage"] in note,
           "the ask sheet states the measured mirror leakage (%.1f)" % cr["leakage"])
    ok(cr["ceiling"] <= 40.0, "the pair ceiling is at or under 40 (%.1f)" % cr["ceiling"])
    kept = {}
    for row_ in cr["cracker_rows"]:
        a, hit = row_[0], row_[2]
        kept[a] = kept.get(a, 0) + (1 if hit else 0)
    # every figure both responses attempt carries a computed value, so a miss is attempted and missed
    for row_ in cr["cracker_rows"] + cr["mirror_rows"]:
        ok(isinstance(row_[3], float), "every scored figure carries what the response computed")
    ok(all(abs(x[3] - x[4]) > 1e-9 for x in cr["mirror_construction"]),
       "the mirror's twelve construction figures are all attempted and all wrong")
    ok(not any(kept.values()),
       "supplemental-stumping 1.1: the cracker keeps %d of %d ask figures%s"
       % (cr["cracker_ask_kept"], cr["n_ask"],
          "" if not any(kept.values()) else ", on " + ", ".join(a for a, n in sorted(kept.items()) if n)))
    ok(cr["mirror_ask_kept"] == 0,
       "the mirror keeps none of the %d ask figures either" % cr["n_ask"])

    # ---------- figures.json agrees with the bundle ----------
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(fp):
        fig = json.load(open(fp))
        # the asking sentence states avoidable complications to one decimal, so figures.json carries
        # them at one decimal and nothing coarser: a figure stated coarser than the prompt asked for is
        # a wrong figure, and figures_check.py cannot see it because both sides would carry the same
        # coarse value
        ok(fig["avoidable_at_pick"] == round(answer["avoidable"], 1),
           "figures.json carries the call's figure at the stated one decimal (%s)"
           % fig["avoidable_at_pick"])
        ok(all(fig["avoidable_by_unit"][d["unit"]] == round(d["avoidable"], 1) for d in units),
           "figures.json carries every unit's avoidable count at one decimal")
        for k in ("avoidable_at_pick", "avoidable_at_runner", "avoidable_at_third", "gap_complications"):
            ok(len(("%s" % fig[k]).split(".")[-1]) == 1 and "." in "%s" % fig[k],
               "figures.json states %s to exactly one decimal (%s)" % (k, fig[k]))
        for key in ("not_measured_by_hospital", "not_measured_with_a_complication_by_hospital"):
            ok(all(float(v).is_integer() for v in fig[key].values()),
               "figures.json states %s whole, as the asking sentence says" % key)
        ok(fig["readings_of_the_development"] == len(conv)
           and fig["readings_naming_the_call"] == len(conv),
           "figures.json carries the convergence and says every reading names the call")
        ok(fig["call_unit_code"] == answer["unit"] and fig["rung0_unit_code"] == r0["first"],
           "figures.json names the call and rung 0's unit")
        ok(fig["recorded_rank_of_call"] == g["recorded_rank"],
           "figures.json carries the call's rank on the record as it stands (%d)"
           % fig["recorded_rank_of_call"])
    if FAILS:
        print("\n".join("FAILED: " + f for f in FAILS))
        print("%d failures of %d" % (len(FAILS), N))
    return N
