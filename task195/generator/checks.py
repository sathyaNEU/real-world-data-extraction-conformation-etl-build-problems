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

import golden as G
import sim
import world as W

Z = 1.959963985
Z1 = 1.644853627
ZB = 2.575829304          # a Bonferroni bar over the five listed cutoffs
N = [0]


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
    ok("ask 1 covers nine reports", len(g["panel_weeks"]) == 9)
    ok("ask 1 every report carries a difference", all(w["difference"] >= 3 for w in g["panel_weeks"]))
    ok("ask 1 the row count is the report's own total",
       all(w["results_issued"] == w["specimens"] + w["difference"] for w in g["panel_weeks"]))
    comparison_ids = {r["specimen_id"] for r in rows}
    extra = [r for r in panel_rows if int(r["result_seq"]) > 1 or r["aliquot_id"] != "A1"]
    flipped = 0
    first = {}
    for r in panel_rows:
        if r["aliquot_id"] == "A1":
            first[r["specimen_id"]] = r["verdict"]
    for r in panel_rows:
        if r["aliquot_id"] != "A1" and first.get(r["specimen_id"]) not in (None, r["verdict"]):
            flipped += 1
    ok("ask 1 some repeat panels carry the other verdict", flipped >= 3, str(flipped))
    ok("ask 1 no device row sits in the comparison",
       not any(r["specimen_id"] in comparison_ids for r in extra), str(len(extra)))
    ok("ask 1 every comparison specimen has exactly one verdict row",
       all(sum(1 for r in panel_rows if r["specimen_id"] == s) == 1 for s in list(comparison_ids)[:400]))
    # A1's silent primary: a repeat panel typed under a second accession of the same specimen
    cross_all = rows_of(os.path.join(target, W.FILES["crosswalk"]), "\t")
    by_ref = {}
    for r in cross_all:
        by_ref.setdefault(r["biobank_ref"], []).append(r["specimen_id"])
    reacc = {s for ids in by_ref.values() if len(ids) > 1 for s in ids}
    ok("ask 1 the re-accessioned specimens exist", len(reacc) >= 2 * W.REACCESSIONED - 40, str(len(reacc)))
    ok("ask 1 no re-accession sits in the comparison",
       not (reacc & comparison_ids) or all(len(by_ref[r["biobank_ref"]]) == 1 for r in cross_all
                                           if r["specimen_id"] in comparison_ids),
       "comparison specimens sharing a biobank reference")
    naive_week = {}
    for r in panel_rows:
        day = r["report_date"]
        if day[:7] in ("2027-04", "2027-05"):
            naive_week.setdefault(r["report_ref"], set()).add(r["specimen_id"])
    for w in g["panel_weeks"]:
        ok("ask 1 the accession count misses %s" % w["report_ref"],
           len(naive_week[w["report_ref"]]) != w["specimens"],
           "%d against %d" % (len(naive_week[w["report_ref"]]), w["specimens"]))
    ok("ask 2 covers twelve months", len(g["baseline"]) == 12)
    hist = rows_of(os.path.join(target, W.FILES["history"]))
    ok("ask 2 the history is 25,000 rows or more", len(hist) >= 25000, str(len(hist)))
    ok("ask 2 no history specimen is in the comparison",
       not ({r["specimen_id"] for r in hist} & comparison_ids))
    ok("ask 2 released dates sit only on released rows",
       all((r["released_date"] != "") == (r["release_status"] == "RELEASED") for r in hist))
    naive = {}
    for r in hist:
        if r["release_status"] != "RELEASED":
            continue
        month = r["received_date"][:7]
        naive.setdefault(month, [0, 0])
        naive[month][0] += 1
        naive[month][1] += 1 if r["hetx_call"] == "FLAG" else 0
    auto, ored = {}, {}
    for r in hist:
        if r["release_status"] != "RELEASED" or not r["released_date"]:
            continue
        month = r["released_date"][:7]
        d = auto.setdefault(month, [0, 0])
        d[0] += 1
        d[1] += 1 if r["hetx_call"] == "FLAG" else 0
        o = ored.setdefault(month, [0, 0])
        o[0] += 1
        o[1] += 1 if (r["hetx_call"] == "FLAG" or r["review_outcome"] == "FLAGGED") else 0
    wide, autoer = 0, [0]
    for b in g["baseline"]:
        lazy = 1000.0 * naive[b["month"]][1] / naive[b["month"]][0]
        ok("ask 2 the lazy read is outside the bin in %s" % b["month"],
           round(lazy, 1) != round(b["per_thousand"], 1), "%.2f against %.2f" % (lazy, b["per_thousand"]))
        wide += 1 if abs(lazy - b["per_thousand"]) > 0.6 else 0
        only = 1000.0 * auto[b["month"]][1] / auto[b["month"]][0]
        autoer[0] += 1 if round(only, 1) != round(b["per_thousand"], 1) else 0
        both = 1000.0 * ored[b["month"]][1] / ored[b["month"]][0]
        ok("ask 2 reading the two columns together misses %s" % b["month"],
           round(both, 1) != round(b["per_thousand"], 1), "%.2f against %.2f" % (both, b["per_thousand"]))
        ok("ask 2 %s sits mid-bin" % b["month"], _slack(b["per_thousand"], 1) > 0.02)
    ok("ask 2 the lazy read misses widely in most months", wide >= 8, str(wide))
    ok("ask 2 the automatic column alone misses most months", autoer[0] >= 9, str(autoer[0]))
    # A2's silent primary: a correction released again inside the month, and a pack that counts releases
    vol = {r["reporting_month"]: int(r["results_released"].replace(" ", ""))
           for r in rows_of(os.path.join(target, W.FILES["volumes"]))}
    rowcount = {}
    for r in hist:
        if r["release_status"] == "RELEASED" and r["released_date"]:
            m = r["released_date"][:7]
            d = rowcount.setdefault(m, [0, 0])
            d[0] += 1
            call = r["review_outcome"] if r["call_source"] == "REVIEWED" else r["hetx_call"]
            d[1] += 1 if call in ("FLAG", "FLAGGED") else 0
    ok("ask 2 the reporting pack counts releases, and ties with the row count",
       all(vol[b["month"]] == rowcount[b["month"]][0] for b in g["baseline"]))
    ok("ask 2 the pack is above the specimens released",
       all(vol[b["month"]] > b["released"] for b in g["baseline"]))
    for b in g["baseline"]:
        naive_rate = 1000.0 * rowcount[b["month"]][1] / rowcount[b["month"]][0]
        ok("ask 2 the release-row route misses %s" % b["month"],
           round(naive_rate, 1) != round(b["per_thousand"], 1),
           "%.2f against %.2f" % (naive_rate, b["per_thousand"]))
    # A3's silent primary: the series was prepared from two stocks and each level ran from one
    import openpyxl as _xl
    _wb = _xl.load_workbook(os.path.join(target, W.FILES["dilution"]), data_only=True)
    first_row, stock_of = {}, {}
    for row in _wb["Prepared levels"].iter_rows(min_row=2, values_only=True):
        first_row.setdefault(str(row[1]).strip().upper(), float(row[3]))
    for row in _wb["Replicate results"].iter_rows(min_row=2, values_only=True):
        if row[4] not in (None, ""):
            stock_of[str(row[0]).strip().upper()] = str(row[1]).strip()
    ok("ask 3 the panel ran from one stock", set(stock_of.values()) == {"NS-27-04"},
       str(set(stock_of.values())))
    ok("ask 3 the workbook keeps the series of both stocks",
       len({str(r[0]).strip() for r in _wb["Prepared levels"].iter_rows(min_row=2, values_only=True)}) == 2)
    missed = sum(1 for d in g["dilution"] if abs(first_row[d["level"]] - d["prepared"]) > 1e-9)
    ok("ask 3 the level-only join takes the other stock at every level", missed == len(W.DILUTION),
       str(missed))
    ok("ask 3 covers the panel's levels", len(g["dilution"]) == len(W.DILUTION))
    for d in g["dilution"]:
        ok("ask 3 %s sits mid-bin" % d["level"], _slack(d["median_recovery"], 3) > 0.0004)
        ok("ask 3 %s recovers against the prepared fraction" % d["level"],
           0.80 < d["median_recovery"] < 1.10)
    ok("ask 3 the replicates within a fifth vary",
       len({d["within_fifth"] for d in g["dilution"]}) >= 2)
    ok("ask 3 the per cent label is two orders from the prepared level",
       all(abs(d["median_recovery"] - d["median_recovery"] * 100) > 1 for d in g["dilution"]))
    # the count the ask grades cannot turn on a hair: every replicate sits clear of the one-fifth
    # line, so the flip condition is a measured distance and not a rounding accident
    _vals = {}
    for row in _wb["Replicate results"].iter_rows(min_row=2, values_only=True):
        if row[4] not in (None, ""):
            _vals.setdefault(str(row[0]).strip().upper(), []).append(float(row[4]))
    for d in g["dilution"]:
        lv = d["level"]
        edge = min(abs(abs(v - d["prepared"]) - 0.20 * d["prepared"]) for v in _vals[lv])
        ok("ask 3 %s's replicates are clear of the one-fifth line" % lv, edge >= 0.0004,
           "nearest replicate %.5f from the line, %.1f stored steps" % (edge, edge / 0.0001))
    _covered = {r["specimen_id"] for r in cross_all}
    ok("ask 1 the biobank's register covers every accession the panel register holds",
       not ({r["specimen_id"] for r in panel_rows} - _covered),
       "%d uncovered" % len({r["specimen_id"] for r in panel_rows} - _covered))

    # the ask layer's devices sit outside the call's row population, counted in one place
    dev_a1 = sum(1 for r in panel_rows
                 if r["specimen_id"] in comparison_ids
                 and (int(r["result_seq"]) > 1 or r["aliquot_id"] != "A1"
                      or r["specimen_id"] in reacc))
    dev_a2 = len({a["specimen_id"] for a in rows_of(os.path.join(target, W.FILES["amendments"]))}
                 & comparison_ids)
    dil_ids = {str(r[3]) for r in _wb["Replicate results"].iter_rows(min_row=2, values_only=True)}
    dev_a3 = len(dil_ids & comparison_ids)
    ok("the ask devices hold no row of the comparison's population",
       (dev_a1, dev_a2, dev_a3) == (0, 0, 0), "A1 %d, A2 %d, A3 %d" % (dev_a1, dev_a2, dev_a3))
    read_sets = {r["read_set_id"] for r in mf_rows if r["specimen_id"] in comparison_ids}
    ok("no ask device names a read set the comparison reads",
       not (read_sets & dil_ids) and not (read_sets & {a["specimen_id"] for a in
            rows_of(os.path.join(target, W.FILES["amendments"]))}),
       "%d comparison read sets" % len(read_sets))

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
    lower = [i for i, r in enumerate(dil) if str(r[0])[0].islower()]
    ok("the operator's casing is not a pattern",
       len({b - a for a, b in zip(lower, lower[1:])}) > 2)
    for key, pulled in (("mf", "2027-06-18"), ("weekly", W.AS_OF.isoformat()),
                        ("panel", W.AS_OF.isoformat())):
        rowm = [r for r in rows_of(os.path.join(target, W.FILES["manifest"])) if r["file"] == W.FILES[key]]
        ok("the manifest's pull date for %s is the file's own" % key, rowm and rowm[0]["pulled"] == pulled)
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
    # the manifest and the dictionary are controlled documents
    man = rows_of(os.path.join(target, W.FILES["manifest"]))
    ok("the manifest records a licence for every file",
       all(r["licence"].strip() for r in man), "%d rows" % len(man))
    ok("the manifest records a source and a pull date for every file",
       all(r["produced_by"].strip() and r["pulled"].strip() for r in man))
    dicrows = rows_of(os.path.join(target, W.FILES["dictionary"]))
    ok("the dictionary records an owner and a review date for every entry",
       all(r["owner"].strip() and r["last_reviewed"].strip() for r in dicrows),
       "%d entries" % len(dicrows))
    ok("the dictionary carries its own issue history",
       open(os.path.join(target, W.FILES["dictionary"]), encoding="utf-8").read().count("# issue") >= 3)
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
    pulled = {r["file"]: r["pulled"] for r in man}
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
    for r in dicrows:
        if r["file"] in starts:
            ok("the dictionary entry for %s is not reviewed before that data begins" % r["file"],
               r["last_reviewed"] >= starts[r["file"]],
               "reviewed %s, data from %s" % (r["last_reviewed"], starts[r["file"]]))
    ok("the protocol's issue says it pre-specifies the run it governs",
       "pre-specified" in doc_text and "approved before a run opens" in doc_text)
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
    ok("the weekly reports the validation file reports tie to the register exactly",
       all(weekly_total[w["report_ref"]][1] == w["results_issued"] for w in g["panel_weeks"]),
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
       card_n and int(card_n.group(1)) < accepted_now and "batches of 17 June" in doc_text,
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
    import cracker as CR
    rows_c = CR.score(target, g)
    total_f, kept_f, share, pair, mirror = CR.ceiling(rows_c)
    for ask, n, hits in rows_c:
        ok("the cracker's path misses at least half of %s" % ask, hits <= n // 2,
           "keeps %d of %d" % (hits, n))
    ok("the measured pair ceiling is at or under 40", pair <= 40.0, "%.1f" % pair)
    ok("the measured mirror leakage is under 35 per cent", mirror < 35.0, "%.1f" % mirror)

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
    read_by_solution = {W.FILES[k] for k in ("qc_a", "qc_b", "mf", "panel", "weekly", "history",
                                             "volumes", "dilution", "protocol", "dictionary",
                                             "crosswalk", "modelcard", "config", "manifest")}
    ok("no distractor is on the solution's path",
       not (read_by_solution & {os.path.basename(d) for d in meta["distractor_files"]}))
    dic = {r["file"] for r in rows_of(os.path.join(target, W.FILES["dictionary"]))}
    ok("the dictionary names every validation extract",
       dic == {W.FILES[k] for k in ("qc_a", "qc_b", "mf", "panel", "history", "crosswalk",
                                     "amendments")}, str(dic))
    manifest = rows_of(os.path.join(target, W.FILES["manifest"]))
    ok("the manifest names every shipped file",
       {r["file"] for r in manifest} == set(files) - {W.FILES["manifest"]},
       str(set(files) - {r["file"] for r in manifest}))
    ok("the manifest stays inside the fiction",
       not re.search(r"constructed for|are invented|are fictional|exercise",
                     open(os.path.join(target, W.FILES["manifest"]), encoding="utf-8").read(), re.I))
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
    ok("monthly released counts differ", len({b["released"] for b in g["baseline"]}) == 12)
    ok("monthly flagged counts vary", len({b["flagged"] for b in g["baseline"]}) >= 8)
    ok("weekly report totals differ", len({w["results_issued"] for w in g["panel_weeks"]}) >= 8)
    names = W.PEOPLE.values()
    ok("personas are the drawn ones", set(names) == {"Laila Johannessen", "Dag Rasmussen"})
    blob = ""
    for f in files:
        if f.endswith((".csv", ".tsv", ".json")):
            blob += open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
    ok("no author vocabulary in the data",
       not re.search(r"\b(rung|decoy|solver|rubric|golden|placeholder|claude)\b", blob, re.I))
    ok("no em dash anywhere", "—" not in blob and "—" not in doc_text)
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
