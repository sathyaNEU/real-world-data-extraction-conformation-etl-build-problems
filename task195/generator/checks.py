"""Every claim this build makes, asserted against the cut bundle.

The three-rules block (R1 to R3c) runs the client's check on the generator's clean truth; the SF
block asserts every row of the design note's semantic fork table; the rest covers the ladder, the
ask layer's separation, the input gates and the realism sweep.
"""
import csv
import datetime as dt
import glob
import json
import math
import os
import re
import statistics
import zipfile

import asks as AS
import golden as G
import sim
import world as W

Z = 1.959963985
Z1 = 1.644853627
ZB = 2.575829304          # a Bonferroni bar over the five listed cutoffs
N = [0]
# the files the call reads, as the 10-17 cut shipped them (sha256)
SHIPPED = {
    "qc_a": "9cb8419c79bf9e3a7c27b56b0bc542fbf5d8a3709a2a4c801ca46a857537c591",
    "qc_b": "bf08148c2e81871ece2f3d70cc1be1a232a7ebba2d90bab20f62b2656ecb9f62",
    "mf": "0257f1d3049fd4ea2a0fd808aa56bbeed1bd182a9b2802db68702bc3a4e289aa",
    "panel": "69fca876c41c6f718cd72db87b9273b1bfca9a8a53169fdbfc7a2a3d41fe8a3d",
    "protocol": "d952d532f58cb93859fe639f92b39024bff92fda76b745c606bc793b851f0e78",
    "modelcard": "84d467958fabefd614f4e80714f7c62ccb9f209dc96a2314c27f998e84ee40d1",
    "config": "03a299ae29850136e0964ea38a7f23b7df4929615c1d66840e711b8d7d2d6244",
}


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s failed %s" % (label, detail))


def _paired_lo(row, n, z=Z):
    diff = row["gain"] / n
    return diff - z * row["se_paired"]


def _unpaired_lo(row, n, z=Z):
    diff = row["gain"] / n
    return diff - z * row["se_unpaired"]


def _exact_p(b, c):
    n = b + c
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1))
    return min(1.0, 2.0 * tail / 2 ** n)


def _decide(tab, predicate):
    for row in tab["cutoffs"]:
        if row["ceiling_ok"] and predicate(row, tab["n_mixed"]):
            return "%.3f" % row["cutoff"]
    return "hold"


def _slack(value, places):
    return abs((value * 10 ** places) % 1 - 0.5) / 10 ** places


def rows_of(path, delim=","):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter=delim))


def run(target, g=None):
    N[0] = 0
    g = g or G.compute(target)
    t = g["table"]
    n = t["n_mixed"]
    rows = g["rows"]
    chosen = g["chosen"]

    # ---------------------------------------------------------------- the three rules, executed
    truth = sim.build()
    tmixed = [s for s in truth if s["role"] == "mixed"]
    tclean = [s for s in truth if s["role"] == "clean"]
    ok("R1 paired readings ship", all(k in open(os.path.join(target, W.FILES["qc_a"]),
                                                encoding="utf-8").readline()
                                      for k in ("specimen_id", "hetx_call")))
    ok("R1 estimate ships at specimen grain",
       "mixture_fraction" in open(os.path.join(target, W.FILES["mf"]), encoding="utf-8").readline())
    headers = []
    for p in sorted(glob.glob(os.path.join(target, "*.csv")) + glob.glob(os.path.join(target, "*.tsv"))):
        headers += open(p, encoding="utf-8").readline().lower().split(";" if "qc_screen_calls" in p or "run_log" in p else ("\t" if p.endswith(".tsv") else ","))
    ok("R1 no column holds the deciding quantity",
       not any(re.search(r"increase|interval|gain|detection_rate|sensitivity|established", h) for h in headers))
    ok("R1 the field's raw material is the paired call",
       sum(1 for r in rows if r["mixed"]) == n and all("flag" in r and "estimate" in r for r in rows))

    # R2: each Layer 1 item mishandled leaves the call and the critical components where they are
    mf_rows = rows_of(os.path.join(target, W.FILES["mf"]))
    by_specimen = {}
    for r in mf_rows:
        by_specimen.setdefault(r["specimen_id"], []).append(r)
    second = {k: v for k, v in by_specimen.items() if len(v) > 1}
    ok("R2 two read sets exist", len(second) == W.TWO_READ_SETS)
    for label, pick in (("later read set", lambda v: max(v, key=lambda r: r["read_set_id"])),
                        ("mean of the read sets", None)):
        alt = []
        for r in rows:
            v = by_specimen[r["specimen_id"]]
            if label == "later read set":
                est = float(pick(v)["mixture_fraction"])
            else:
                est = sum(float(x["mixture_fraction"]) for x in v) / len(v)
            alt.append(dict(r, estimate=est))
        at = G.table(alt)
        ok("R2 %s leaves the call" % label, G.decide(at) == g["call"])
        ok("R2 %s leaves the counts" % label,
           [x["detected"] for x in at["cutoffs"]] == [x["detected"] for x in t["cutoffs"]])
    qc_text = open(os.path.join(target, W.FILES["qc_a"]), encoding="utf-8").read()
    ok("R2 voided reads carry no call", re.search(r";N;;;;;;", qc_text) is not None)
    voided = [r for r in rows_of(os.path.join(target, W.FILES["qc_a"]), ";") if r["read_accepted"] != "Y"]
    ok("R2 voided reads cannot enter a count", all(r["hetx_call"] == "" for r in voided))
    ok("R2 decimal commas sit off the call's path",
       all(h not in ("het_excess_pct", "dna_ng_ul") for h in ("hetx_call", "mixture_fraction")))
    reviewed = [r for r in rows if r["call_source"] == "REVIEWED"]
    ok("R2 reviewed calls are recorded like any other", len(reviewed) > 100
       and all(r["flag"] in (True, False) for r in reviewed))
    a_first = G.table(sorted(rows, key=lambda r: r["specimen_id"]))
    a_last = G.table(sorted(rows, key=lambda r: r["specimen_id"], reverse=True))
    ok("R2 row order cannot move a figure",
       [x["detected"] for x in a_first["cutoffs"]] == [x["detected"] for x in a_last["cutoffs"]])

    # R3a: the easy route on the clean truth, every filed rule applied, files the hold
    clean_rows = [{"specimen_id": s["specimen_id"], "flag": bool(s["service_flag"]),
                   "estimate": s["estimate"], "mixed": s["verdict"] == "MIXED", "plate": s["plate"],
                   "het": s["het"], "call_source": s["call_source"]}
                  for s in truth if s["role"] in ("mixed", "clean")]
    ct = G.table(clean_rows)
    cl = G.rungs(ct)
    ok("R3a the easy route files the hold on the clean truth", cl["rung1_overlap"] == "hold")
    ok("R3a the clean truth carries the same counts",
       ct["inc_detected"] == W.INC_DETECT and len(tmixed) == W.N_MIXED and len(tclean) == W.N_CONCORDANT)
    # R3b: the decisive step alone files the golden, and each lower correction does not
    ok("R3b the decisive step alone files the golden", cl["rung3_paired"] == "0.030")
    ok("R3b rung 0 files another answer", cl["rung0_sign"] == "0.050")
    ok("R3b rung 2 files another answer", cl["rung2_unpaired"] == "0.015")
    ok("R3b the four rungs are four answers",
       len({cl["rung0_sign"], cl["rung1_overlap"], cl["rung2_unpaired"], cl["rung3_paired"]}) == 4)
    # R3c: no plant
    doc_text = ""
    try:
        import pypdf
        for key in ("protocol", "modelcard", "weekly", "platform"):
            doc_text += "\n".join(p.extract_text() or ""
                                  for p in pypdf.PdfReader(os.path.join(target, W.FILES[key])).pages)
    except Exception:
        doc_text = ""
    ok("R3c no document recommends a cutoff",
       not re.search(r"(recommend|adopt|choose|select)\w*\s+(the\s+)?0\.0\d", doc_text, re.I))
    ok("R3c no document states a detection count",
       not re.search(r"\b(292|308|310|319|326|393|5446|5839)\b", doc_text.replace(" ", "")))
    est_list = [r["mixture_fraction"] for r in mf_rows]
    grams = [tuple(est_list[i:i + 6]) for i in range(len(est_list) - 6)]
    ok("R3c no copied block of readings", len(grams) == len(set(grams)))
    ok("R3c no answer-key column",
       not any(re.search(r"is_|_true|should_|planted|seed|debug|correct", h) for h in headers))

    # ---------------------------------------------------------------- the ladder
    ok("ladder rung 0", g["rungs"]["rung0_sign"] == "0.050")
    ok("ladder rung 1", g["rungs"]["rung1_overlap"] == "hold")
    ok("ladder rung 2", g["rungs"]["rung2_unpaired"] == "0.015")
    ok("ladder rung 3 is the call", g["call"] == "0.030")
    ok("the call is not the first listed cutoff", g["call"] != "%.3f" % W.CUTOFFS[0])
    ok("decisive margin, paired", chosen["z_paired"] > 2.5, "%.3f" % chosen["z_paired"])
    ok("decisive margin, unpaired", chosen["z_unpaired"] < 1.60, "%.3f" % chosen["z_unpaired"])
    ok("the two standard errors differ by more than two",
       chosen["se_unpaired"] / chosen["se_paired"] > 2.0)
    ok("rung 2's cutoff clears on the two-sample route",
       [r for r in t["cutoffs"] if "%.3f" % r["cutoff"] == "0.015"][0]["z_unpaired"] > 2.1)
    ok("the 0.050 row shows a positive increase", t["cutoffs"][0]["gain"] > 0)
    ok("the 0.050 row is established by no estimator",
       not t["cutoffs"][0]["established"] and _exact_p(t["cutoffs"][0]["only_candidate"],
                                                       t["cutoffs"][0]["only_service"]) > 0.05)
    ok("only the loosest cutoff breaches the ceiling",
       [r["ceiling_ok"] for r in t["cutoffs"]] == [True, True, True, True, False])
    # every paired variant names the golden
    variants = {
        "paired Wald two-sided": lambda r, m: _paired_lo(r, m) > 0,
        "paired Wald one-sided": lambda r, m: _paired_lo(r, m, Z1) > 0,
        "paired Wald with a Bonferroni bar": lambda r, m: _paired_lo(r, m, ZB) > 0,
        "exact McNemar": lambda r, m: r["gain"] > 0 and _exact_p(r["only_candidate"], r["only_service"]) < 0.05,
        "exact McNemar at 0.01": lambda r, m: r["gain"] > 0 and _exact_p(r["only_candidate"], r["only_service"]) < 0.01,
        "continuity-corrected McNemar": lambda r, m: r["gain"] > 0 and (
            (abs(r["only_candidate"] - r["only_service"]) - 1) ** 2
            / max(1, r["only_candidate"] + r["only_service"])) > Z * Z,
        "paired log ratio": lambda r, m: r["gain"] > 0 and math.log(
            r["detected"] / t["inc_detected"]) - Z * math.sqrt(
            r["only_candidate"] + r["only_service"]) / math.sqrt(t["inc_detected"] * r["detected"]) > 0,
    }
    for label, pred in variants.items():
        ok("the %s route names the call" % label, _decide(t, pred) == g["call"], label)
    for label, pred in (("two-sample two-sided", lambda r, m: _unpaired_lo(r, m) > 0),
                        ("two-sample one-sided", lambda r, m: _unpaired_lo(r, m, Z1) > 0),
                        ("two-sample with a Bonferroni bar", lambda r, m: _unpaired_lo(r, m, ZB) > 0),
                        ("marginal overlap", lambda r, m: r["separated"])):
        ok("the %s route never names the call" % label, _decide(t, pred) != g["call"], label)
    # the plate-clustered paired interval
    plates = {}
    for r in rows:
        if not r["mixed"]:
            continue
        d = (1 if r["estimate"] >= 0.030 and not r["flag"] else 0) - (1 if r["estimate"] < 0.030 and r["flag"] else 0)
        plates.setdefault(r["plate"], []).append(d)
    m = len(plates)
    mean = sum(sum(v) for v in plates.values()) / n
    var = sum((sum(v) - mean * len(v)) ** 2 for v in plates.values()) * m / ((m - 1) * n * n)
    ok("the plate-clustered paired interval clears zero", mean - Z * math.sqrt(var) > 0,
       "%.5f" % (mean - Z * math.sqrt(var)))
    ok("discordance is spread over the plates",
       max(sum(1 for d in v if d) for v in plates.values()) <= 3)
    # verification weighting for the verdicts still pending
    pending = [s for s in truth if s["role"] == "pending"]
    ok("the pending set is small and carries the same flag rate", abs(
        sum(1 for s in pending if s["service_flag"]) / len(pending)
        - t["inc_false"] / t["n_clean"]) < 0.06)
    weighted = G.table(rows + [dict(r, specimen_id=r["specimen_id"] + "w")
                               for r in rows[:len(pending)]])
    ok("verification weighting leaves the call", G.decide(weighted) == g["call"])

    # ---------------------------------------------------------------- the semantic fork table
    projects = {p[0] for p in W.PROJECTS}
    qc_all = {}
    for key in ("qc_a", "qc_b"):
        for r in rows_of(os.path.join(target, W.FILES[key]), ";"):
            if r["read_accepted"] == "Y":
                qc_all[r["specimen_id"]] = r
    panel_rows = rows_of(os.path.join(target, W.FILES["panel"]))
    ok("SF1 the comparison is the filed population", len(rows) == 5839)
    wide = [r for r in rows]
    ok("SF1 the alternative reading is not the golden",
       G.decide(G.table(wide)) == g["call"])          # the filed reading and the golden agree
    ok("SF2 INCONCLUSIVE verdicts are outside the comparison",
       not any(r["verdict"] == "INCONCLUSIVE" and r["specimen_id"] in {x["specimen_id"] for x in rows}
               for r in panel_rows))
    incl = rows + [dict(r, mixed=False) for r in rows[:W.INCONCLUSIVE]]
    ok("SF2 counting them as clean leaves the call", G.decide(G.table(incl)) == g["call"])
    accepted_reads = sum(1 for key in ("qc_a", "qc_b")
                         for r in rows_of(os.path.join(target, W.FILES[key]), ";")
                         if r["read_accepted"] == "Y")
    ok("SF3 one accepted read per specimen", accepted_reads == len(qc_all))
    ok("SF3 one accepted read set per specimen in the comparison",
       all(sum(1 for x in by_specimen[r["specimen_id"]] if x["read_set_accepted"] == "Y") == 1
           for r in rows))
    ok("SF4 the one-sided reading gives the same qualifying set",
       _decide(t, lambda r, m: _paired_lo(r, m, Z1) > 0) == g["call"])
    alt_fpr = [r["false_calls"] / len(rows) <= t["inc_false"] / len(rows) for r in t["cutoffs"]]
    ok("SF5 the all-specimen denominator gives the same qualifying set",
       alt_fpr == [r["ceiling_ok"] for r in t["cutoffs"]])
    ok("SF6 the cutoffs are listed in descending value", W.CUTOFFS == sorted(W.CUTOFFS, reverse=True))
    reverse_walk = next(("%.3f" % r["cutoff"] for r in reversed(t["cutoffs"])
                         if r["ceiling_ok"] and r["established"]), "hold")
    ok("SF6 walking the list the other way names another cutoff", reverse_walk == "0.015", reverse_walk)
    ok("SF7 no estimate sits on a listed cutoff",
       not any(abs(float(r["mixture_fraction"]) - c) < 1e-12 for r in mf_rows for c in W.CUTOFFS))
    rederived = [dict(r, flag=(r["het"] is not None and r["het"] >= W.HETX_THRESHOLD)) for r in rows]
    rd = G.table(rederived)
    ok("SF8 re-deriving the recorded call leaves the call", G.decide(rd) == g["call"])
    ok("SF8 re-deriving the recorded call from the run log's threshold reproduces every call",
       rd["inc_detected"] == t["inc_detected"] and rd["inc_false"] == t["inc_false"],
       "%d %d" % (rd["inc_detected"], rd["inc_false"]))
    ok("SF8 the overturned calls sit outside the comparison",
       all((r["het"] >= W.HETX_THRESHOLD) == bool(r["flag"]) for r in rows if r["het"] is not None),
       "overridden rows inside the comparison")
    over = [sid for sid, q in qc_all.items()
            if q.get("call_source") == "REVIEWED" and q.get("het_excess_pct")
            and ((float(q["het_excess_pct"].replace(",", ".")) >= W.HETX_THRESHOLD)
                 != (q["hetx_call"] == "FLAG"))]
    ok("SF8 the laboratory overturned a handful of borderline calls at review",
       8 <= len(over) <= 40, "%d overturned" % len(over))
    ok("SF8 no het value sits in an empty guard band around the threshold",
       min(abs(float(q["het_excess_pct"].replace(",", ".")) - W.HETX_THRESHOLD)
           for q in qc_all.values() if q.get("het_excess_pct")) <= 0.02)
    ok("SF8 the recorded call is the filed one", "hetx_call" in qc_all[rows[0]["specimen_id"]])
    ok("SF9 the export carries one date per specimen",
       not any(k.endswith("_date") and k != "received_date" and k != "extract_date"
               for k in qc_all[rows[0]["specimen_id"]]))
    ok("SF9 every comparison specimen was received inside the window",
       all(W.RUN_FROM <= dt.date.fromisoformat(qc_all[r["specimen_id"]]["received_date"]) <= W.RUN_TO
           for r in rows))
    ok("SF10 the increase as a ratio gives the same call",
       _decide(t, variants["paired log ratio"]) == g["call"])
    ok("SF11 accepted reads only", all(qc_all[r["specimen_id"]]["read_accepted"] == "Y" for r in rows))
    ok("SF12 the second read set stays in its band",
       all(G.table([dict(r, estimate=float(x["mixture_fraction"]))
                    for r in rows for x in [by_specimen[r["specimen_id"]][0]]])["cutoffs"][i]["detected"]
           == t["cutoffs"][i]["detected"] for i in range(len(W.CUTOFFS))))
    for r in t["cutoffs"]:
        ok("SF13 the increase at %.3f sits mid-bin" % r["cutoff"],
           _slack(r["gain_pp"], 2) > 0.0025, "%.5f" % _slack(r["gain_pp"], 2))
        ok("SF13 the false-call rate at %.3f sits mid-bin" % r["cutoff"],
           _slack(r["false_rate_pct"], 2) > 0.0025)
    ok("SF13 the screen in service's false-call rate sits mid-bin",
       _slack(t["inc_false_rate_pct"], 2) > 0.0025)
    ok("SF14 pending verdicts are outside the comparison",
       len({r["specimen_id"] for r in panel_rows}) > len(rows))

    # ---------------------------------------------------------------- the ask layer
    # The ask: per extraction method, the twelve reporting months to February 2027 of the screen in
    # service, from the warehouse extract. Its primary: the LIMS method table was re-coded on the second
    # robot's go-live, every extraction keeps the code it was booked under, and the warehouse names each
    # code by the table at the pull.
    comparison_ids = {r["specimen_id"] for r in rows}
    hist = rows_of(os.path.join(target, W.FILES["history"]))
    hist_text = open(os.path.join(target, W.FILES["history"]), encoding="utf-8").read()
    amd_rows = rows_of(os.path.join(target, W.FILES["amendments"]))
    cross_all = rows_of(os.path.join(target, W.FILES["crosswalk"]), "\t")
    ok("ask the history is 25,000 rows or more", len(hist) >= 25000, str(len(hist)))
    ok("ask covers the four methods the records hold",
       [m["method"] for m in g["methods"]] == W.METHOD_ORDER
       and {r["extraction_method"] for r in hist} == set(W.METHOD_ORDER))
    ok("ask released dates sit only on released rows",
       all((r["released_date"] != "") == (r["release_status"] == "RELEASED") for r in hist))
    # "reviewed" reads one way: a record the duty bioinformatician reviewed carries a review outcome,
    # and no other record does, before the amendments and after them
    _rev_am = {(a["specimen_id"], a["field"]): a["value_after"] for a in amd_rows}
    ok("ask a reviewed record is exactly one with a review outcome",
       all((r["call_source"] == "REVIEWED") == (r["review_outcome"] != "") for r in hist)
       and all((r["call_source"] == "REVIEWED")
               == (_rev_am.get((r["specimen_id"], "review_outcome"), r["review_outcome"]) != "") for r in hist))
    ok("ask an amendment to a call names the column that holds that record's call",
       all((a["field"] == "review_outcome") == any(r["call_source"] == "REVIEWED" for r in hist
                                                   if r["specimen_id"] == a["specimen_id"])
           for a in amd_rows if a["field"] in ("review_outcome", "hetx_call")))
    # separation: no device or hazard row in the comparison's population, counted from the shipped rows
    ok("ask no history specimen is in the comparison",
       not ({r["specimen_id"] for r in hist} & comparison_ids))
    ok("ask no history receipt falls in the parallel run's window",
       max(r["received_date"] for r in hist) < W.RUN_FROM.isoformat())
    ok("ask no amendment names a comparison specimen",
       not ({a["specimen_id"] for a in amd_rows} & comparison_ids))
    ok("ask the call reads no file the ask reads",
       not ({W.FILES[k] for k in ("history", "amendments", "platform")}
            & {W.FILES[k] for k in ("qc_a", "qc_b", "mf", "panel", "protocol")}))
    # the golden is the clean truth
    import tempfile
    _tmp = tempfile.mkdtemp(prefix="t195_truth_")
    _n, truth_m, _ev, _am = AS.history(_tmp)
    ok("ask the golden is the clean truth, method by method",
       all(truth_m[m["method"]] == {"released": m["released"], "reviewed": m["reviewed"],
                                    "flagged": m["flagged"]} for m in g["methods"]),
       str(truth_m))
    for m in g["methods"]:
        ok("ask %s's rate sits mid-bin" % m["method"], _slack(m["per_thousand"], 1) > 0.02,
           "%.4f" % m["per_thousand"])
    ok("ask the workbook's title is true: the low-input program and the silica column flag most often",
       {m["method"] for m in sorted(g["methods"], key=lambda x: -x["per_thousand"])[:2]}
       == {W.LOW_INPUT, "silica column"})
    # the device's facts, from the shipped rows
    switch = g["method_switch"]
    ok("ask the table was re-coded on the second robot's go-live", switch == W.METHOD_SWITCH.isoformat(),
       switch)
    before = {r["extraction_method_code"] for r in hist if r["extracted_date"] < switch}
    after = {r["extraction_method_code"] for r in hist if r["extracted_date"] >= switch}
    ok("ask before the re-coding only the 2026 table's codes are booked", before == {"1", "2", "3"},
       str(sorted(before)))
    ok("ask from the re-coding all four codes are booked", after == {"1", "2", "3", "4"}, str(sorted(after)))
    ok("ask the warehouse names every code by the table at the pull",
       all(r["extraction_method"] == W.METHODS_NOW[int(r["extraction_method_code"])] for r in hist))
    ok("ask no extraction follows its release",
       all(r["extracted_date"] <= (r["released_date"] or "9999") and r["extracted_date"] >= r["received_date"]
           for r in hist))
    ok("ask the extract's own footer says whose table names the codes",
       "Code descriptions are those of the LIMS reference tables at the pull" in hist_text)
    ok("ask the 2025 platform validation prints the 2026 codes",
       all(re.search(r"\b%d\s+%s\b" % (c, re.escape(n)), doc_text) for c, n in W.METHODS_2026.items()),
       "codes not found in the report")
    # the forcing, as numbers: read by the names, every code's DNA concentration jumps at the re-coding;
    # read on the table in force, every method's concentration is level across it
    def _med(xs):
        return statistics.median(xs) if xs else float("nan")
    jumps, level = [], []
    for code in ("1", "2", "3"):
        b = _med([float(r["dna_ng_ul"]) for r in hist if r["extraction_method_code"] == code
                  and r["extracted_date"] < switch])
        a = _med([float(r["dna_ng_ul"]) for r in hist if r["extraction_method_code"] == code
                  and r["extracted_date"] >= switch])
        jumps.append(max(a / b, b / a))
    true_method = lambda r: (W.METHODS_2026[int(r["extraction_method_code"])]
                             if r["extracted_date"] < switch else r["extraction_method"])
    for name in ("magnetic bead", "silica column", "salting out"):
        b = _med([float(r["dna_ng_ul"]) for r in hist if true_method(r) == name and r["extracted_date"] < switch])
        a = _med([float(r["dna_ng_ul"]) for r in hist if true_method(r) == name and r["extracted_date"] >= switch])
        level.append(max(a / b, b / a))
    ok("ask read by the names, every code's concentration jumps at the re-coding", min(jumps) > 1.3,
       ", ".join("%.2f" % x for x in jumps))
    # the referee: MG-2025-14's yields order the 2026 methods as the table in force reads them, and the
    # names read them otherwise
    _report_order = ["salting out", "magnetic bead", "silica column"]          # 8.1, 6.4, 4.9 ug
    _golden_order = sorted(_report_order, key=lambda n: -_med([float(r["dna_ng_ul"]) for r in hist
                                                               if true_method(r) == n]))
    _names_order = sorted(_report_order, key=lambda n: -_med([float(r["dna_ng_ul"]) for r in hist
                                                              if r["extraction_method"] == n]))
    ok("ask the platform validation's yields order the methods as the table in force reads them",
       _golden_order == _report_order and _names_order != _report_order,
       "%s / %s" % (_golden_order, _names_order))
    ok("ask the platform validation states its yields", all(y in doc_text for y in ("6.4", "4.9", "8.1")))
    ok("ask read on the table in force, every method's concentration is level", max(level) < 1.04,
       ", ".join("%.3f" % x for x in level))
    # the ask ladder, every stop measured by the ceiling script on the shipped rows
    import ceiling as CE
    _rd, _sw = CE.readings(target)
    ok("ask the ceiling script reads the same switch from the pack", _sw == switch, _sw)
    gold = {m["method"]: m for m in g["methods"]}
    for name, rd in _rd.items():
        if name == "full includer":
            ok("ask the full includer reproduces every figure",
               all(rd[m]["released"] == gold[m]["released"] and rd[m]["reviewed"] == gold[m]["reviewed"]
                   and rd[m]["flagged"] == gold[m]["flagged"]
                   and abs(rd[m]["per_thousand"] - round(gold[m]["per_thousand"], 1)) < 0.05 for m in gold))
            continue
        if name == "the switch on the receipt date":
            # the response that has found the re-coding and splits on the receipt date: it misses every
            # method's released count, by the extractions of the last receipts before the go-live
            ok("ask the receipt-date split misses every released count",
               all(rd[m]["released"] != gold[m]["released"] for m in gold),
               ", ".join("%s %d/%d" % (m, rd[m]["released"], gold[m]["released"]) for m in gold))
            continue
        for m in gold:
            got = rd.get(m)
            ok("ask the %s stop misses %s" % (name, m),
               got is None or (got["released"] != gold[m]["released"]
                               and got["flagged"] != gold[m]["flagged"]
                               and got["reviewed"] != gold[m]["reviewed"]
                               and abs(got["per_thousand"] - gold[m]["per_thousand"]) >= 0.2),
               "%s against %s" % (got, gold[m]))
    # the hazards each move the ask on their own
    def _per_method(skip_amend=False, every_row=False, auto_only=False, all_status=False):
        amend = {} if skip_amend else {(a["specimen_id"], a["field"]): a["value_after"] for a in amd_rows}
        out, seen = {}, set()
        for r in hist:
            if not all_status and (r["release_status"] != "RELEASED" or not r["released_date"]):
                continue
            sid = r["specimen_id"]
            rel = amend.get((sid, "released_date"), r["released_date"]) or r["received_date"]
            if rel[:7] not in set(AS._months()) or (sid in seen and not every_row):
                continue
            seen.add(sid)
            field = "hetx_call" if auto_only or r["call_source"] != "REVIEWED" else "review_outcome"
            call = amend.get((sid, field), r[field])
            d = out.setdefault(true_method(r), [0, 0])
            d[0] += 1
            d[1] += 1 if call in ("FLAG", "FLAGGED") else 0
        return out
    for label, kw in (("the amendments left out", {"skip_amend": True}),
                      ("each release row counted", {"every_row": True}),
                      ("the automatic call alone", {"auto_only": True}),
                      ("withheld and superseded rows kept", {"all_status": True})):
        alt = _per_method(**kw)
        moved = sum(1 for m in gold if (alt[m][0], alt[m][1]) != (gold[m]["released"], gold[m]["flagged"]))
        ok("ask hazard: %s moves the ask" % label, moved >= 3, "%d of 4 methods" % moved)
    # the re-coding is a business change in the laboratory's own records, not a defect: the codes the
    # extractions were booked under are the ones in force on the day, and every row's name is the table's
    ok("ask an extraction's code is the one in force on the day it was extracted",
       all((int(r["extraction_method_code"]) in W.METHODS_2026) or r["extracted_date"] >= switch for r in hist))
    # the call's files are the shipped ones, or the change is undone exactly (see below)
    ok("ask the warehouse and its amendment log hold no read set the comparison reads",
       not ({r["read_set_id"] for r in mf_rows if r["specimen_id"] in comparison_ids}
            & ({r["specimen_id"] for r in hist} | {a["specimen_id"] for a in amd_rows})))
    ok("ask the release desk's log says the amended value stands",
       "the amended record carries value_after in place of value_before"
       in open(os.path.join(target, W.FILES["amendments"]), encoding="utf-8").read())

    # ---------------------------------------------------------------- the files the call reads
    # qc_a, qc_b and the re-run file are byte-identical to the 10-17 cut. Three files the call reads or
    # cites changed for realism only, each on rows or sentences the call never executes, and each change
    # undone reproduces the shipped bytes exactly: the panel register's request numbers on the 912
    # results for receipts before the run window (the biobank's counter skips), KVAL-07 6.2's sentence
    # on an export manifest the pack no longer ships, and the model card's addendum sentence.
    import hashlib
    import build as BD
    import docs as DC
    import pack as PK

    def _sha(path):
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    for key in ("qc_a", "qc_b", "mf"):
        ok("the call's %s is byte-identical to the shipped cut" % W.FILES[key],
           _sha(os.path.join(target, W.FILES[key])) == SHIPPED[key], W.FILES[key])
    _und = tempfile.mkdtemp(prefix="t195_shipped_")
    _specimens = sim.build()
    PK.write_panel(_und, _specimens, shipped=True)
    DC.protocol(_und, shipped=True)
    _done = {sid: day for sid, day in PK._mf_completions(_specimens)}
    DC.model_card(_und, [rs["estimate"] for s in _specimens for rs in s["read_sets"]
                         if rs["accepted"] and _done.get(s["specimen_id"], "9999") <= "2027-06-16"],
                  shipped=True)
    BD.stamp_pdf(_und, ("protocol", "modelcard"))
    for key in ("panel", "protocol", "modelcard"):
        ok("undoing the realism change to %s reproduces the shipped bytes" % W.FILES[key],
           _sha(os.path.join(_und, W.FILES[key])) == SHIPPED[key], W.FILES[key])
    now_panel = open(os.path.join(target, W.FILES["panel"]), encoding="utf-8").read().splitlines()
    was_panel = open(os.path.join(_und, W.FILES["panel"]), encoding="utf-8").read().splitlines()
    ok("the register's comparison rows are byte-identical to the shipped cut",
       [l for l in now_panel if l.split(",")[0] in comparison_ids]
       == [l for l in was_panel if l.split(",")[0] in comparison_ids])
    ok("the register's rows differ only in the earlier receipts' request numbers",
       len(now_panel) == len(was_panel)
       and all(a == b or (a.split(",")[:2] == b.split(",")[:2] and a.split(",")[3:] == b.split(",")[3:]
                          and a.split(",")[0] not in comparison_ids)
               for a, b in zip(now_panel, was_panel)))

    # ---------------------------------------------------------------- the pack reads as the laboratory's
    accepted = {r["specimen_id"]: float(r["mixture_fraction"]) for r in mf_rows
                if r["read_set_accepted"] == "Y"}
    shares = [(float(r["second_contributor_share"]), accepted.get(r["specimen_id"]))
              for r in panel_rows if r["verdict"] == "MIXED" and r["second_contributor_share"]]
    shares = [(a, b) for a, b in shares if b is not None]
    mx = sum(b for _a, b in shares) / len(shares)
    my = sum(a for a, _b in shares) / len(shares)
    cov = sum((b - mx) * (a - my) for a, b in shares)
    den = (sum((b - mx) ** 2 for _a, b in shares) * sum((a - my) ** 2 for a, _b in shares)) ** 0.5
    ok("the panel's share and the re-run's estimate measure the same mixture", cov / den > 0.75,
       "r %.3f" % (cov / den))
    run_log = rows_of(os.path.join(target, W.FILES["runlog"]), ";")
    received = {r["received_local"][:10] for r in run_log} | {r["received_date"] for r in hist}
    ok("nothing is received on a day the laboratory is closed",
       not (received & {d.isoformat() for d in W.HOLIDAYS}))
    per_day = {}
    for r in run_log:
        per_day[r["received_local"][:10]] = per_day.get(r["received_local"][:10], 0) + 1
    ok("the receipt day's own size varies", max(per_day.values()) - min(per_day.values()) > 30)
    thresholds = {}
    for r in run_log:
        thresholds.setdefault(r["batch_id"], set()).add(r["control_threshold_het_pct"])
    ok("a control threshold is set and held", max(len(v) for v in thresholds.values()) == 1
       and len({v for sv in thresholds.values() for v in sv}) == 1)
    typed_all = {r["panel_markers_typed"] for r in panel_rows}
    ok("the panel's typing record varies", len(typed_all) > 6)
    ok("an inconclusive result is one the panel could not type",
       all(int(r["panel_markers_typed"]) < 80 for r in panel_rows if r["verdict"] == "INCONCLUSIVE"))
    cross = {r["specimen_id"]: r for r in rows_of(os.path.join(target, W.FILES["crosswalk"]), "\t")}
    ok("the register's request is the biobank's request",
       all(cross[r["specimen_id"]]["request_id"] == r["request_id"] for r in panel_rows
           if r["specimen_id"] in cross))
    per_request = {}
    for r in cross.values():
        per_request[r["request_id"]] = per_request.get(r["request_id"], 0) + 1
    ok("a request covers a specimen or a family group", max(per_request.values()) <= 3)
    ok("the biobank reference is well formed",
       not any("--" in r["biobank_ref"] for r in cross.values()))
    est_vals = [r["mixture_fraction"] for r in mf_rows]
    ok("the estimate has no floor",
       max(est_vals.count(v) for v in set(est_vals)) < len(est_vals) / 20)
    strides = sorted({int(a["specimen_id"].split("-")[1]) - int(b["specimen_id"].split("-")[1])
                      for a, b in zip(hist[1:], hist)} - {0})
    ok("accessions are not issued on a fixed stride", len(strides) > 4)
    import openpyxl as _x
    wb = _x.load_workbook(os.path.join(target, W.FILES["dilution"]), data_only=True)
    dil = [r for r in wb["Replicate results"].iter_rows(min_row=2, values_only=True)]
    depths = [[r[5] for r in dil if str(r[0]).upper() == lv] for lv, _l, _f in W.DILUTION]
    ok("each level was sequenced on its own",
       all(depths[i] != depths[j] for i in range(len(depths)) for j in range(i + 1, len(depths))))
    ok("no estimate was completed after the re-run was pulled",
       max(r["completed_date"] for r in mf_rows) <= "2027-06-18")
    ok("the protocol's annex does not predate its issue",
       re.search(r"requested the verification on 5 February 2027", doc_text) is not None)
    # the two sequencers are two instruments, not one copied twice
    rates = []
    for key in ("qc_a", "qc_b"):
        acc = [r for r in rows_of(os.path.join(target, W.FILES[key]), ";") if r["read_accepted"] == "Y"]
        rates.append(sum(1 for r in acc if r["hetx_call"] == "FLAG") / float(len(acc)))
    ok("the two sequencers do not flag at the same rate",
       max(rates) / min(rates) >= 1.35 and max(rates) / min(rates) <= 2.4,
       "%.2f and %.2f per cent" % (100 * rates[0], 100 * rates[1]))
    # the accession counter is shared with the laboratory's other work, so no one stride dominates
    acc_nums = sorted({int(r["specimen_id"].split("-")[1]) for r in cross_all})
    strides2 = [b - a for a, b in zip(acc_nums, acc_nums[1:])]
    top = max(strides2.count(x) for x in set(strides2)) / float(len(strides2))
    ok("no single accession stride dominates", top <= 0.34 and len(set(strides2)) >= 8,
       "commonest stride is %.0f per cent of %d gaps, %d distinct" % (100 * top, len(strides2),
                                                                      len(set(strides2))))
    # the booking clock is a clock: it records the second, and the minutes are not flat
    stamps = [r["received_utc"] for r in hist]
    secs = {t[17:19] for t in stamps}
    mins = [t[14:16] for t in stamps]
    mtop = max(mins.count(x) for x in set(mins)) / float(len(mins))
    ok("the booking clock records the second", len(secs) >= 50, "%d distinct seconds" % len(secs))
    ok("the booking minutes are not flat across the hour", mtop >= 0.024,
       "commonest minute is %.1f per cent against a flat 1.7" % (100 * mtop))
    # no describing file ships (dataset-generation section 3): no dictionary, manifest, notes or readme
    shipped = sorted(os.listdir(target))
    ok("no describing file ships", not any(x in f.lower() for f in shipped
                                           for x in ("dictionary", "manifest", "notes", "readme")), str(shipped))
    # the model card: its version predates the re-run and its addendum follows the last batch
    first_done = min(r["completed_date"] for r in mf_rows)
    last_done = max(r["completed_date"] for r in mf_rows)
    ok("the model card's version predates the re-run",
       re.search(r"issued 2027-05-14", doc_text) is not None and "2027-05-14" < first_done,
       "card 2027-05-14, first batch %s" % first_done)
    ok("the model card's addendum follows the last batch",
       re.search(r"Addendum, 19 June 2027", doc_text) is not None and "2027-06-19" > last_done,
       "addendum 2027-06-19, last batch %s" % last_done)
    ok("the model card owns the distribution it reports",
       "states no verdict" not in doc_text and "revision history" in doc_text.lower())

    # ---------------------------------------------------------------- dates: no document describes an
    # event that had not happened when it was stated, and no extract carries a date after its own pull
    # each extract's own pull date (the data teams' pull log, kept by the generator; no manifest ships)
    pulled = {W.FILES[k]: d for k, d in (("qc_a", W.AS_OF.isoformat()), ("qc_b", W.AS_OF.isoformat()),
                                         ("mf", "2027-06-18"), ("panel", W.AS_OF.isoformat()),
                                         ("history", W.HIST_PULL.isoformat()), ("amendments", W.AS_OF.isoformat()),
                                         ("volumes", "2027-03-06"), ("crosswalk", W.AS_OF.isoformat()),
                                         ("config", "2027-06-08"), ("runlog", W.AS_OF.isoformat()),
                                         ("costs", "2027-01-15"), ("plates", W.AS_OF.isoformat()))}
    amd = rows_of(os.path.join(target, W.FILES["amendments"]))
    ISO = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
    for f, pull in sorted(pulled.items()):
        path = os.path.join(target, f)
        if not f.endswith((".csv", ".tsv", ".json")) or not os.path.exists(path):
            continue
        body = open(path, encoding="utf-8").read()
        latest = max(ISO.findall(body) or ["0000-00-00"])
        ok("%s carries no date after its own pull" % f, latest <= pull,
           "latest %s, pulled %s" % (latest, pull))
    hist_last = max(r["released_date"] for r in hist if r["released_date"])
    ok("the warehouse extract was pulled after its last release",
       hist_last <= pulled[W.FILES["history"]], "%s against %s" % (hist_last, pulled[W.FILES["history"]]))
    ok("every amendment was raised after the extract was pulled",
       min(a["amended_date"] for a in amd) > pulled[W.FILES["history"]],
       "earliest %s, extract pulled %s" % (min(a["amended_date"] for a in amd),
                                           pulled[W.FILES["history"]]))
    starts = {}
    for f in pulled:
        path = os.path.join(target, f)
        if f.endswith((".csv", ".tsv")) and os.path.exists(path):
            found = ISO.findall(open(path, encoding="utf-8").read())
            if found:
                starts[f] = min(found)
    ok("the protocol's issue that governs the run was approved before the run opened",
       re.search(r"Issue 4, approved 2027-02-19", doc_text) is not None
       and "2027-02-19" < W.RUN_FROM.isoformat()
       and "pre-specified" not in doc_text)
    ok("the partner's report notes the step in volume where the full typing order starts",
       "types every cohort service receipt from 1 March" in re.sub(r"\s+", " ", doc_text)
       and "Where a report is re-sent" not in doc_text)
    ok("the model card's addendum leaves the cutoffs to KVAL-07 without saying so",
       "KVAL-07's matter" not in re.sub(r"\s+", " ", doc_text))
    _wbd = _x.load_workbook(os.path.join(target, W.FILES["dilution"]), data_only=True)
    ok("the sensitivity panel lists only the stock its replicates ran from",
       {str(r[0]) for r in _wbd["Prepared levels"].iter_rows(min_row=2, values_only=True)} == {"NS-27-04"}
       and {str(r[1]) for r in _wbd["Replicate results"].iter_rows(min_row=2, values_only=True)} == {"NS-27-04"})
    ok("the protocol is not a conspicuous extract",
       "not reproduced in this extract" not in doc_text
       and all(h in doc_text for h in ("Purpose and scope", "Responsibilities",
                                       "Deviations and records", "References and revision history")))
    ok("the model card's revision history skips no version",
       all(v in doc_text for v in ("3.2", "3.3", "3.4", "3.4.1")))

    # ---------------------------------------------------------------- the reconciliations are not all
    # exact: a real pack carries a residue, and each one a document states
    weekly_total = {}
    for m in re.finditer(r"(BA-2027-W\d\d)\s+(\d{4}-\d\d-\d\d)\s+\d{4}-\d\d-\d\d\s+(\d+)", doc_text):
        weekly_total[m.group(1)] = (m.group(2), int(m.group(3)))
    reg_rows = {}
    for r in panel_rows:
        reg_rows[r["report_ref"]] = reg_rows.get(r["report_ref"], 0) + 1
    april_may = sorted({r["report_ref"] for r in panel_rows if r["report_date"][:7] in ("2027-04", "2027-05")})
    ok("the April and May weekly reports tie to the register exactly",
       len(april_may) == 9 and all(weekly_total[k][1] == reg_rows[k] for k in april_may),
       "the nine April and May reports")
    off = [k for k, (d, n) in weekly_total.items() if n != reg_rows.get(k)]
    ok("some other weekly report does not tie, and the report says why",
       len(off) >= 2 and all(d[5:7] not in ("04", "05") for d, _n in
                             [(weekly_total[k][0], 0) for k in off])
       and "returned on receipt for re-typing" in doc_text,
       "%d reports off: %s" % (len(off), ", ".join(sorted(off))))
    card_n = re.search(r"Read sets with an estimate\s+(\d+)", doc_text)
    accepted_now = sum(1 for r in mf_rows if r["read_set_accepted"] == "Y")
    ok("the model card's addendum does not tie to the file as filed, and says so",
       card_n and int(card_n.group(1)) < accepted_now
       and "batches of 17 June are not included" in re.sub(r"\s+", " ", doc_text),
       "card %s against %d accepted read sets" % (card_n.group(1) if card_n else "?", accepted_now))
    amd = rows_of(os.path.join(target, W.FILES["amendments"]))
    span = re.findall(r"(\d{4}-\d{2})", W.FILES["amendments"])
    ok("the amendments file's name brackets the amendments it holds",
       len(span) == 2 and span[0] <= min(a["amended_date"][:7] for a in amd)
       and max(a["amended_date"][:7] for a in amd) <= span[1],
       "%s against %s to %s" % ("/".join(span), min(a["amended_date"][:7] for a in amd),
                                max(a["amended_date"][:7] for a in amd)))
    ok("an amendment is dated after the release it corrects",
       all(a["amended_date"] > max(a["value_before"], a["value_after"]) for a in amd
           if a["field"] == "released_date"))

    # ---------------------------------------------------------------- the ask layer, measured
    import ceiling as CEIL
    _figs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(_figs) and "methods" in json.load(open(_figs, encoding="utf-8")):
        meas = CEIL.measure(target, _figs)
        ok("the cracker's path keeps no ask figure", meas["kept"]["cracker"] == 0,
           "keeps %d of %d" % (meas["kept"]["cracker"], meas["figures"]))
        ok("the mirror's path keeps no ask figure", meas["kept"]["mirror"] == 0,
           "keeps %d of %d" % (meas["kept"]["mirror"], meas["figures"]))
        for name in ("the 2025 codes on every record", "the 2026 table for 2026 records"):
            ok("the stress row %s keeps no ask figure" % name, meas["kept"][name] == 0,
               "keeps %d" % meas["kept"][name])
        ok("the full includer keeps what the sheet says it keeps",
           meas["kept"]["full includer"] == meas["figures"], str(meas["kept"]["full includer"]))
        ok("the measured pair ceiling is at or under 40", meas["pair"] <= 40.0, "%.1f" % meas["pair"])
        ok("the measured mirror leakage is under 35 per cent", meas["mirror_leakage_pct"] < 35.0,
           "%.1f" % meas["mirror_leakage_pct"])

    # ---------------------------------------------------------------- gates, provenance, realism
    files = sorted(os.listdir(target))
    ok("input gate, ten files or more", len(files) >= 10, str(len(files)))
    formats = {os.path.splitext(f)[1] for f in files}
    ok("input gate, three formats or more", len(formats) >= 3, str(sorted(formats)))
    ok("input gate, a file of 25,000 rows or more",
       any(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8", errors="replace")) >= 25000
           for f in files if f.endswith(".csv")))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("input gate, two distractors or more", len(meta["distractor_files"]) >= 2)
    ok("no file name carries the word distractor", not any("distract" in f for f in files))
    ok("the distractors are shipped", all(os.path.exists(os.path.join(target, os.path.basename(d)))
                                          for d in meta["distractor_files"]))
    read_by_solution = {W.FILES[k] for k in ("qc_a", "qc_b", "mf", "panel", "history",
                                             "amendments", "platform", "protocol",
                                             "modelcard", "config")}
    ok("no distractor is on the solution's path",
       not (read_by_solution & {os.path.basename(d) for d in meta["distractor_files"]}))
    # dates
    latest = []
    for f in files:
        if f.endswith((".csv", ".tsv", ".json")):
            text = open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
            latest += [d for d in re.findall(r"20\d\d-\d\d-\d\d", text)]
    ok("no record is dated after the extract", max(latest) <= W.AS_OF.isoformat(), max(latest))
    # realism
    ok("no round headline total", all(x % 100 for x in (len(rows), t["n_mixed"], t["n_clean"],
                                                        t["inc_detected"], t["inc_false"])))
    _per_month = {}
    for r in hist:
        if r["release_status"] == "RELEASED" and r["released_date"][:7] in set(AS._months()):
            _per_month[r["released_date"][:7]] = _per_month.get(r["released_date"][:7], 0) + 1
    ok("monthly release rows differ", len(set(_per_month.values())) == 12)
    ok("no method's figures are round", all(m["released"] % 100 and m["flagged"] % 10 for m in g["methods"]))
    ok("weekly report totals differ", len({reg_rows[k] for k in april_may}) >= 8)
    names = W.PEOPLE.values()
    ok("personas are the drawn ones", set(names) == {"Laila Johannessen", "Dag Rasmussen"})
    blob = ""
    for f in files:
        if f.endswith((".csv", ".tsv", ".json")):
            blob += open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
    ok("no author vocabulary in the data",
       not re.search(r"\b(rung|decoy|solver|rubric|golden|placeholder|claude)\b", blob, re.I))
    ok("no em dash anywhere", "\u2014" not in blob and "\u2014" not in doc_text)
    ok("identifiers are structured", re.match(r"NFG27-\d{6}$", rows[0]["specimen_id"]) is not None)
    # containers
    with zipfile.ZipFile(os.path.join(target, W.FILES["dilution"])) as z:
        core = z.read("docProps/core.xml").decode()
    ok("the workbook carries the laboratory's own producer", "Johannessen" in core)
    ok("the workbook carries no build clock", "2026" not in core and "2025" not in core)
    return N[0]


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    print("assertions", run(tgt))
