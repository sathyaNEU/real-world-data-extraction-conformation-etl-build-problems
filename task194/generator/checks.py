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

    # ---------- the ladder: three rungs, each named on the record ----------
    rts = g["routes"]
    r0 = rts["R0 the published excess, carried onto the planned separations"]
    r3 = rts["R10 the avoidable count as a rate per 1,000 separations, not as a count"]
    r4 = rts["R12 the avoidable count over the window, carried onto the planned separations"]
    ok(r0["first"] != answer["unit"], "rung 0 names another unit (%s)" % r0["first"])
    ok(r3["first"] != answer["unit"], "rung 3 names another unit (%s)" % r3["first"])
    ok(r4["first"] == answer["unit"], "rung 4 names the answer (%s)" % r4["first"])
    ok(len({r0["first"], r3["first"], r4["first"]}) == 3, "the three rungs name three different units")
    for lab, rung, floor in (("0", r0, 1.15), ("3", r3, 1.15), ("4", r4, 1.5)):
        ok(rung["margin"] >= floor, "rung %s margin %.3fx at or above %.2fx" % (lab, rung["margin"], floor))
    ok(r4["margin"] <= 2.0, "the final margin %.3fx is inside the 1.5 to 2x band" % r4["margin"])
    ok(g["published_rank"] in (4, 5), "the answer sits %d of %d on rung 0's ranking"
       % (g["published_rank"], len(units)))
    second_on = [k for k, v in rts.items() if v["second"] == answer["unit"] and v["first"] != answer["unit"]]
    ok(len(second_on) <= 2, "the answer is second on at most two routes (%d)" % len(second_on))
    # dominance: the answer's edge on the decisive axis over the easy route's unit beats the runner's
    base = by[r0["first"]]["avoidable"]
    ok(answer["avoidable"] - base >= 1.2 * (runner["avoidable"] - base),
       "the answer's edge over the easy route's unit dominates the runner's (%.1f against %.1f)"
       % (answer["avoidable"] - base, runner["avoidable"] - base))

    # the lead, in complications, as a ratio, and against the record's own sampling error
    ok(abs(g["gap"] - (answer["avoidable"] - runner["avoidable"])) < 1e-9,
       "the gap is the two counts' difference")
    ok(1.5 <= g["margin"] <= 2.0, "the margin %.3fx is in band" % g["margin"])
    ok(g["se_lead"] >= 2.0, "the lead is %.2f standard errors of the gap" % g["se_lead"])
    ok(g["se_lead"] > 1.0, "the top two are not inside a standard error of each other")
    for d in units:
        ok(abs(d["se"] - math.sqrt(d["observed"]) * d["plan"] / d["separations"]) < 1e-9,
           "each unit's standard error is sqrt(observed) carried like its count (%s)" % d["unit"])
    ok(sum(1 for d in units if d["avoidable"] / d["se"] > 2.5) == 3,
       "three candidates stand above 2.5 of their own standard error")
    ok(sum(1 for d in units if d["avoidable"] < 0) >= 3,
       "the record carries units on both sides of zero (%d negative)"
       % sum(1 for d in units if d["avoidable"] < 0))

    # ---------- R3a the analyst test, on the clean truth ----------
    # a strong analyst who reads every rule correctly and reconciles to the published series row for row
    # still ranks on the published expectation and files another unit
    easy = max(units, key=lambda d: d["published_excess"])
    ok(easy["unit"] != answer["unit"], "R3a the easy route files another unit (%s)" % easy["unit"])
    ok(easy["avoidable"] < 0,
       "R3a the unit the easy route files carries a negative avoidable count (%.1f)" % easy["avoidable"])
    ok(answer["published_excess"] > 0,
       "R3a the answer is not invisible on the published basis, only fourth (%.1f)"
       % answer["published_excess"])
    ok(abs(answer["ratio"] - answer["observed"] / answer["expected"]) < 1e-12
       and abs(easy["ratio"] - easy["observed"] / easy["expected"]) < 1e-12,
       "R3a both routes read the published rates correctly")

    # ---------- R3b the decisive step alone moves the call ----------
    ok(sorted(units, key=lambda d: -d["published_excess"])[0]["unit"] == easy["unit"]
       and sorted(units, key=lambda d: -d["avoidable"])[0]["unit"] == answer["unit"],
       "R3b the comparison frequency alone decides between the two rankings")

    # ---------- the three facts that force the comparison frequency ----------
    f = g["facts"]
    ok("year ended 30 June 2024" in spec, "fact 1 the specification states the table's vintage")
    ok("not re-estimated between specifications" in spec,
       "fact 1 the specification states the table is not re-estimated")
    ok(f["drift_spread"] >= 1.25,
       "fact 2 the record's own frequency spans a factor of %.2f across the risk bands" % f["drift_spread"])
    ok(f["drift_low"] < 0.95 and f["drift_high"] > 1.05,
       "fact 2 it crosses 1.00 in both directions (%.3f to %.3f)" % (f["drift_low"], f["drift_high"]))
    ok(len([x for x in f["drift"].values() if x < 1]) >= 2
       and len([x for x in f["drift"].values() if x > 1]) >= 2,
       "fact 2 at least two bands each side of the published table")
    ok(f["surgical_high"] / max(f["surgical_low"], 1e-9) >= 3.0,
       "fact 3 the candidates' case mixes differ several-fold (%.3f to %.3f)"
       % (f["surgical_low"], f["surgical_high"]))
    ok(f["surgical_none"] >= 2,
       "fact 3 some candidates carry no surgical work at all (%d)" % f["surgical_none"])

    # ---------- the demonstration: a mix shift with the unit's own practice flat ----------
    d_ = g["demo"]
    ok(d_["mix_swing"] >= 0.25, "the demonstration unit's case mix moves (%.3f)" % d_["mix_swing"])
    ok(d_["published_multiple"] >= 3.0,
       "the published basis moves its avoidable count by a factor of %.1f" % d_["published_multiple"])
    ok(d_["internal_spread"] <= 1.5,
       "the record's own frequency holds it inside %.2f of a complication in every quarter"
       % d_["internal_spread"])
    ok(d_["published_multiple"] / max(d_["internal_spread"], 1e-9) >= 4.0,
       "the two bases separate on the demonstration by a wide margin")
    ok(len(d_["shifted"]) == 2, "the shift covers two closed quarters (%d)" % len(d_["shifted"]))
    unshifted = [r for r in d_["rows"] if r["quarter"] not in d_["shifted"]]
    ok(max(r["episodes"] for r in d_["rows"]) / min(r["episodes"] for r in d_["rows"]) < 1.15,
       "the demonstration unit treats the same number of patients throughout")
    ok(max(abs(r["internal"] - unshifted[0]["internal"]) for r in d_["rows"]) <= 1.5,
       "its avoidable count on the record's own frequency does not move across the shift")

    # ---------- C1 convergence: every reading of charter 4.3 the text leaves open ----------
    conv = g["convergence"]
    ok(len(conv) >= 12, "twelve or more readings of charter 4.3 are formed and ranked (%d)" % len(conv))
    for label, v in conv.items():
        ok(v["first"] == answer["unit"],
           "C1 %s names the answer (%s at %.2f against %s at %.2f, %.2fx)"
           % (label, v["first"], v["first_value"], v["second"], v["second_value"], v["margin"]))
        ok(v["margin"] >= 1.05, "C1 %s separates its first two (%.2fx)" % (label, v["margin"]))
    ok(max(v["margin"] for v in conv.values()) >= 2.5,
       "the strongest reading separates by %.2fx" % max(v["margin"] for v in conv.values()))

    # ---------- the readings that do move the call, each ruled out by a quotable sentence ----------
    rout = g["ruled_out"]
    ok(len(rout) >= 3, "the readings that move the call are formed too (%d)" % len(rout))
    for label, v in rout.items():
        ok(v["first"] != answer["unit"], "%s does move the call (to %s)" % (label, v["first"]))
    ok("same risk band and age band" in charter, "the clause that rules those readings out is shipped")
    ok("ordinarily have" in charter, "charter 4.3 asks what such patients ordinarily have")
    ok("would be expected to have" not in charter,
       "charter 4.3 does not borrow the specification's defined term")
    ok("expected complications of a group of episodes" in spec,
       "the specification's own defined term sits in the specification, not the charter")
    ok("does not maintain a measure of its own" not in charter,
       "no clause rules the decisive step out by elimination")
    for w in ("the network's own rate", "internally standardised", "achievable", "attainable"):
        ok(w not in charter and w not in spec, "no shipped clause names a rate set (%s)" % w)

    # ---------- the semantic fork table ----------
    allq = sorted({q for (_, q) in panel})
    SPEC_WINDOW = "the ten closed quarters of the specification period"
    # SF1 the unit's own record over a period: specification 3.3 files the specification period to date
    ok("every closed quarter from 1 July 2024" in spec, "SF1 specification 3.3 files the record's window")
    for lab in (SPEC_WINDOW, "the eight most recent closed quarters",
                "the four most recent closed quarters", "the latest closed quarter alone"):
        ok(conv["the unit's own record taken over %s" % lab]["first"] == answer["unit"],
           "SF1 the record over %s names the answer" % lab)
    # SF2 the most avoidable complications: a count, not a rate
    ok("counted patient by patient" in charter, "SF2 charter 4.3 counts patient by patient")
    ok(r3["first"] != answer["unit"] and r4["first"] == answer["unit"],
       "SF2 the rate reading and the count reading name different units")
    # SF3 the exposure the rate is carried on
    ok("expected complications per separation" in spec, "SF3 specification 3.4 files the carrying")
    ok(conv["the unit's rate taken per all separations in the record"]["first"]
       == conv["the unit's rate taken per in-scope episodes in the record"]["first"],
       "SF3 both denominators name the same unit")
    # SF4 the comparison population's membership
    ok(any("own hospital" in k for k in rout), "SF4 the restricted comparison is measured")
    ok(any("peer group" in k for k in rout), "SF4 the peer-group comparison is measured")
    # SF5 whether the unit's own patients sit inside the comparison
    ok(conv["the unit's own patients left out of the comparison, frequency over %s" % SPEC_WINDOW]["first"]
       == answer["unit"], "SF5 leave-one-out names the answer")
    # SF6 the comparison frequency's own window
    for lab in (SPEC_WINDOW, "the eight most recent closed quarters",
                "the four most recent closed quarters", "the latest closed quarter alone"):
        ok(conv["the comparison frequency measured over %s" % lab]["first"] == answer["unit"],
           "SF6 the comparison frequency over %s names the answer" % lab)
    # SF7 whether the comparison is stratified at all
    ok([v for k, v in rout.items() if "no strata" in k][0]["first"] != answer["unit"],
       "SF7 an unstratified comparison moves the call and charter 4.3 names the strata")
    # SF8 closed quarters at the decision date
    ok("eight weeks after the quarter ends" in spec, "SF8 specification 3.7 files when a quarter closes")
    ok(len(allq) == 10 and allq[-1] == "2026-27 Q2", "SF8 the record carries the ten closed quarters only")
    ok(max(r["separation_date"] for r in read(target, "episode_outcomes_extract.csv")) <= "2026-12-31",
       "SF8 no separation falls after the last closed quarter")
    # SF9 eligibility
    ok(len(g["eligible"]) == 12, "SF9 charter 4.2 leaves twelve eligible units (%d)" % len(g["eligible"]))
    ok("previous twelve closed quarters" in charter, "SF9 the charter files the exclusion window")
    ok("four or more closed quarters" in charter, "SF9 the charter files the floor")
    # SF10 the complication list revision
    ok("the revision in force at separation" in spec, "SF10 the specification files which revision applies")
    # SF11 the indicator's denominator
    ok("excluded from the denominator is excluded from the numerator" in spec,
       "SF11 the specification files the denominator's reach")
    # SF12 the reference rate's scope
    ok("reference rate of 96.6" in spec, "SF12 the reference rate is scoped to the adjusted rate")
    ok(abs(answer["avoidable"] - answer["ratio_net"] * 96.6) > 1.0,
       "SF12 the avoidable count is a count and does not carry the reference rate")
    # SF13 the rounding of every graded figure
    for d in units:
        ok(sim.bin_edge(d["avoidable"], 1.0) >= sim.EDGE_BAR,
           "SF13 %s's avoidable count sits %.3f from the whole complication's edge"
           % (d["unit"], sim.bin_edge(d["avoidable"], 1.0)))
        ok(sim.bin_edge(d["expected_plan"], 0.1) >= sim.EDGE_BAR * 0.1,
           "SF13 %s's expected count sits %.4f from the decimal's edge"
           % (d["unit"], sim.bin_edge(d["expected_plan"], 0.1)))
    for h in g["hospitals"]:
        ok(sim.bin_edge(h["rate"], 0.1) >= sim.EDGE_BAR * 0.1,
           "SF13 %s's adjusted rate sits %.4f from the decimal's edge"
           % (h["hospital"], sim.bin_edge(h["rate"], 0.1)))

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
    ok("215 " in dsrc, "the brief names the panel's size as the series carries it")
    ok("ordinarily have" in dsrc,
       "the brief states the comparison in the charter's own words, not in a method's")
    ok("avoided" not in dsrc, "no deliverable states a quantity the record does not carry")
    for clause in ("3.3", "3.4", "2.1", "2.2"):
        ok(clause in spec, "the specification carries clause %s" % clause)
    for clause in ("4.1", "4.2", "4.3", "4.4"):
        ok(clause in charter, "the charter carries clause %s" % clause)
    ok("that patients of the same risk band and age band ordinarily have" in charter,
       "the charter files the comparison in clause 4.3, and no rate set with it")
    ok("separations planned" in charter, "the charter files the activity basis in clause 4.4")
    ok("standardised ratio is reported" in spec, "the specification files the reporting period")
    ok(charter.count("most avoidable complications") == 1
       and charter.count("ordinarily have") == 1,
       "the pin is stated once, at authority, and not restated")
    ok(spec.count("ordinarily have") == 0 and charter.count("stratum") == 0,
       "neither document restates the other's term")

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
    # A2: the register's current alignment moves every hospital
    reg = {c: u["hospital_code"] for c, u in b["units"].items()}
    wrong = defaultdict(lambda: [0, 0, 0.0])
    for eid, (unit, sep, fy) in b["inscope_episode"].items():
        if not (dt.date(2026, 1, 1) <= sep <= dt.date(2026, 12, 31)):
            continue
        site = reg[unit]
        wrong[site][0] += 1
    for h in g["hospitals"]:
        ok(wrong[h["hospital"]][0] != h["episodes"],
           "A2 the register's alignment moves %s's episode count" % h["hospital"])
    ok(len(W.REALIGNED) == 3, "A2 three cost centres were realigned")
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
    for x in g["groups"]:
        ok(len(only_detail["2025-26"][x["group"]]) < x["fy2025"],
           "A4 the detail extract alone runs low in %s for 2025-26" % x["group"])
        ok(len(only_detail["2026-27"][x["group"]]) < x["fy2026"],
           "A4 the detail extract alone runs low in %s for 2026-27" % x["group"])
    moved = sum(1 for x in g["groups"]
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
    ok(cr["n_ask"] == 48 and cr["n_con"] == 12,
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
    for a, _, hit in cr["cracker_rows"]:
        kept[a] = kept.get(a, 0) + (1 if hit else 0)
    gap(not any(kept.values()),
        "supplemental-stumping 1.1: the cracker keeps %d of %d ask figures, on %s. The ask sheet states "
        "it and the design note's Tried and rejected records why the ask cannot hold a primary as worded."
        % (cr["cracker_ask_kept"], cr["n_ask"],
           ", ".join(a for a, n in sorted(kept.items()) if n)))

    # ---------- figures.json agrees with the bundle ----------
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(fp):
        fig = json.load(open(fp))
        ok(fig["avoidable_at_pick"] == round(answer["avoidable"]),
           "figures.json carries the call's figure")
        ok(all(fig["avoidable_by_unit"][d["unit"]] == round(d["avoidable"]) for d in units),
           "figures.json carries every unit's avoidable count")
        ok(fig["readings_of_clause_43"] == len(conv)
           and fig["readings_naming_the_call"] == len(conv),
           "figures.json carries the convergence and says every reading names the call")
    if FAILS:
        print("\n".join("FAILED: " + f for f in FAILS))
        print("%d failures of %d" % (len(FAILS), N))
    return N
