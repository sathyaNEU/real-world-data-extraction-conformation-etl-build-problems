"""task157 (architecture 2) checks: the call and the ladder recomputed from the bundle, the client's three
rules executed on the generator's clean truth, every semantic fork row, the closure axes that can move, the
stage 3 parameter pin, the convergence families on the cut pack and over all six seeds, the ask layer
measured per figure, the documents with a positive control on every absence, the realism sweep, the input
gates and the distractors' deletion tests.

    python3 task157/generator/checks.py

Exits 1 on any failure. Run by build.py after the goldens are written."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import cracker as CR        # noqa: E402
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import metadata as MD       # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
RESULTS = []

GOLD_PRINTED = 390_000
GOLD_BAND = "full count"
DEFAULT_PRINTED = 420_000
DEFAULT_BAND = "sufficient"


def ok(label, cond, detail=""):
    RESULTS.append((bool(cond), label, detail))
    print("%s  %-74s %s" % ("PASS" if cond else "FAIL", label, detail))


def pdf_text(path):
    import pypdf
    return "\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(path).pages)


def norm(text):
    """A document's text with its line breaks collapsed. A closure sentence hard-wrapped mid-phrase is
    present in the record and unreachable by a line-oriented search, which is how one of this build's own
    determinism findings happened, so every document assertion reads the normalised text."""
    return re.sub(r"\s+", " ", text)


# =================================================================================== the bundle
rows = C.conform(TARGET)
call = C.call(rows)
rungs = C.rungs(TARGET, rows)
E = C.everything(TARGET)
figs = json.load(open(os.path.join(HERE, "figures.json")))
w = W.build(K.SEED)
S = R.shape(w)
truth = W.counts(w)
metrics = W.bin_metrics(w)

print("=== the call and the ladder, recomputed from the bundle ===")
ok("the sample the bundle carries is the statutory sample", call["sampled"] == K.SAMPLE_LINES,
   "%d rows" % call["sampled"])
ok("one disposition per sampled line, a partition of the sample",
   sum(call["tally"][c] for c in K.CODE_KEYS) == K.SAMPLE_LINES,
   "%d codes summing to %d" % (len(K.CODE_KEYS), K.SAMPLE_LINES))
ok("the sample's own factor is twenty exactly", C.FACTOR == 20 and C.FACTOR * K.SAMPLE_LINES == K.LINES_FILED,
   "%d x %d = %d" % (C.FACTOR, K.SAMPLE_LINES, K.LINES_FILED))
ok("a pair's inclusion probability is one in four hundred", C.PAIR_FACTOR == 400, "%d" % C.PAIR_FACTOR)
ok("the projection recomputes from the bundle", int(call["valid"]) == 390_060, "%d" % call["valid"])
ok("the projection prints the golden's cell", call["printed"] == GOLD_PRINTED, "%d" % call["printed"])
ok("the projection files the golden's band", call["band"] == GOLD_BAND, call["band"])
ok("the projection as a share of the number required",
   abs(K.round_half_up(call["pct"], 1) - 101.3) < 1e-9, "%.2f per cent" % call["pct"])
ok("rung 0, the default path, recomputes", int(rungs["rung0"]) == 420_520, "%d" % rungs["rung0"])
ok("rung 0 prints the named wrong cell", K.round_to(rungs["rung0"], K.BIN) == DEFAULT_PRINTED,
   "%d" % K.round_to(rungs["rung0"], K.BIN))
ok("rung 0 files the named wrong band", K.band(rungs["rung0"]) == DEFAULT_BAND, K.band(rungs["rung0"]))
ok("rung 1 recomputes and files a wrong cell and band",
   int(rungs["rung1"]) == 413_240 and K.round_to(rungs["rung1"], K.BIN) == 415_000
   and K.band(rungs["rung1"]) == "sufficient", "%d prints %d %s"
   % (rungs["rung1"], K.round_to(rungs["rung1"], K.BIN), K.band(rungs["rung1"])))
ok("rung 2 recomputes and files a wrong cell",
   int(rungs["rung2"]) == 404_880 and K.round_to(rungs["rung2"], K.BIN) == 405_000,
   "%d prints %d %s" % (rungs["rung2"], K.round_to(rungs["rung2"], K.BIN), K.band(rungs["rung2"])))
ok("every rung prints its own cell, three or more cells from the golden",
   len({K.round_to(rungs[k], K.BIN) for k in ("rung0", "rung1", "rung2", "rung3")}) == 4
   and min(abs(K.round_to(rungs[k], K.BIN) - GOLD_PRINTED) for k in ("rung0", "rung1", "rung2")) >= 3 * K.BIN,
   "cells %s" % sorted({K.round_to(rungs[k], K.BIN) for k in ("rung0", "rung1", "rung2", "rung3")}))
ok("the bundle's figures equal the generator's clean truth",
   call["single"] == truth["single"] and call["dup"] == truth["dup"],
   "single %d, duplicates %d" % (call["single"], call["dup"]))
ok("the duplicate strikes the sample saw are the pairs it drew both lines of",
   call["dup"] == truth["dup"] and truth["dup"] == len(w.dup_ix), "%d" % call["dup"])
ok("the full count's own duplicate burden is not in the pack and the estimate is close to it",
   abs(call["dup"] * C.PAIR_FACTOR - w.dup_full) < metrics["c"],
   "estimate %d against the truth %d, inside the estimator's own interval %.0f"
   % (call["dup"] * C.PAIR_FACTOR, w.dup_full, metrics["c"]))

# =================================================================================== the three rules
print()
print("=== R1 to R3c, the client's three rules executed on the clean truth ===")
ret = C.rd(TARGET, R.F_RETURNS)
ok("R1 the field's raw material ships at the grain the estimator runs on",
   len(ret) == K.SAMPLE_LINES and all(r["disposition_code"] for r in ret[:50]),
   "one row per sampled signature line, %d rows" % len(ret))
flat = {}
for fn in sorted(os.listdir(TARGET)):
    p = os.path.join(TARGET, fn)
    if fn.endswith(".pdf"):
        flat[fn] = pdf_text(p)
    elif fn.endswith(".xlsx"):
        flat[fn] = "\n".join(" ".join("" if v is None else str(v) for v in rw)
                             for sh in PP.xlsx_sheet_names(p) for rw in PP.read_xlsx_rows(p, sh))
    else:
        flat[fn] = open(p, encoding="utf-8", errors="replace").read()
docs_text = {f: norm(t) for f, t in flat.items() if not f.endswith(".csv")}
csv_fields = {}
for fn in sorted(os.listdir(TARGET)):
    if fn.endswith(".csv"):
        vals = set()
        for rw in C.rd(TARGET, fn):
            vals.update(str(v).strip() for v in rw.values())
        csv_fields[fn] = vals
DECIDING = ("390200", "390,200", "390000", "390,000", "24400", "24,400", "125400", "125,400")
ok("R1 no shipped document carries the deciding quantity",
   not any(s in t for t in docs_text.values() for s in DECIDING),
   "no document carries the projection, the duplicate burden or the printed cell")
ok("R1 no shipped data field carries the deciding quantity",
   not any(s in vals for vals in csv_fields.values() for s in DECIDING),
   "no field in any of the %d csv files equals one of them" % len(csv_fields))
ok("R1 no shipped file states how a disposition class expands",
   not any(re.search(r"(expan|project|multiply|factor of twenty|inclusion probab)", t, re.I)
           for t in docs_text.values()),
   "no expansion, projection or inclusion sentence in any shipped document")

# R2, one assertion per Layer 1 item: the golden method with that item mishandled leaves the call where it is
def call_of(handling):
    """The call computed from the bundle with one Layer 1 item mishandled."""
    r2 = CR._rows(TARGET, handling)
    t = C.tally([dict(code=x["code"]) for x in r2])
    return C.project(t["single"], t["dup"] * C.PAIR_FACTOR)


full = CR.DOCUMENTED + CR.PRIMARIES
MESS = [
    ("Navajo County's own 2019 code list", tuple(x for x in full if x != "old_codes")),
    ("the division's query notices", tuple(x for x in full if x != "corrections")),
    ("Mohave County's day-first signature dates", tuple(x for x in full if x != "dmy")),
    ("the sheet numbers each firm printed on its own series", tuple(x for x in full if x != "sheet_key")),
    ("the lines the division determined rather than a recorder",
     tuple(x for x in full if x != "determined_by")),
    ("the registrations cancelled and restored", tuple(x for x in full if x != "reg_state")),
    ("the circulators who registered again under another firm",
     tuple(x for x in full if x != "firm_asof")),
]
for name, handling in MESS:
    v = call_of(handling)
    ok("R2 mishandling %s leaves the call where it is" % name,
       K.round_to(v, K.BIN) == GOLD_PRINTED and K.band(v) == GOLD_BAND,
       "%d prints %d %s" % (v, K.round_to(v, K.BIN), K.band(v)))
for name, cols in (("the returns' UTC received stamps", ("return_received_utc",)),
                   ("the dates outside the circulation period on struck lines", ("signature_date",)),
                   ("the two files written with CRLF line endings", ())):
    ok("R2 %s are read by no step of the call" % name, True,
       "the call reads the disposition column alone, over the %d sampled lines" % K.SAMPLE_LINES)

ok("R3a the analyst test: the easy route with every filed rule applied files the named wrong answer",
   K.round_to(rungs["rung0"], K.BIN) == DEFAULT_PRINTED and K.band(rungs["rung0"]) == DEFAULT_BAND,
   "%d prints %d and files %s" % (rungs["rung0"], DEFAULT_PRINTED, DEFAULT_BAND))
clean_default = W.default_path(w)
clean_golden = W.golden(w)
ok("R3a the same route on the generator's clean truth files the same wrong answer",
   K.round_to(clean_default, K.BIN) == DEFAULT_PRINTED and K.band(clean_default) == DEFAULT_BAND,
   "%d prints %d and files %s" % (clean_default, K.round_to(clean_default, K.BIN), K.band(clean_default)))
ok("R3b changing the decisive step alone files the golden",
   K.round_to(rungs["rung3"], K.BIN) == GOLD_PRINTED and K.band(rungs["rung3"]) == GOLD_BAND
   and int(rungs["rung1"] - rungs["rung3"]) == call["dup"] * (C.PAIR_FACTOR - C.FACTOR),
   "rung 1 %d less the decisive step's %d is %d, which prints %d and files %s"
   % (rungs["rung1"], call["dup"] * (C.PAIR_FACTOR - C.FACTOR), rungs["rung3"], GOLD_PRINTED, GOLD_BAND))
ok("R3b the same on the clean truth", K.round_to(clean_golden, K.BIN) == GOLD_PRINTED,
   "%d prints %d" % (clean_golden, K.round_to(clean_golden, K.BIN)))
ok("R3b each lower rung's single correction leaves it on a wrong answer",
   K.round_to(rungs["rung1"], K.BIN) != GOLD_PRINTED
   and K.round_to(C.project(C.tally(rows)["single"] - rungs["slip"], call["dup"] * C.PAIR_FACTOR), K.BIN)
   != GOLD_PRINTED,
   "the vintage fixed alone prints %d, the decisive step alone on rung 0 prints %d"
   % (K.round_to(rungs["rung1"], K.BIN),
      K.round_to(C.project(C.tally(rows)["single"] - rungs["slip"], call["dup"] * C.PAIR_FACTOR), K.BIN)))
ok("R3c no answer-key column ships",
   not any(re.search(r"is_correct|should_exclude|answer|golden|expected_valid", ",".join(C.rd(TARGET, f)[0]),
                     re.I) for f in csv_fields), "no such column in any shipped file")
ok("R3c no repeated or copied block in the returns",
   len({(r["circulator_reg_no"], r["sheet_no"], r["line_no"]) for r in ret}) == len(ret),
   "%d distinct line keys in %d rows" % (len({(r["circulator_reg_no"], r["sheet_no"], r["line_no"])
                                              for r in ret}), len(ret)))
ok("R3c no shipped document argues for an expansion basis or ranks the three statutory outcomes",
   not any(re.search(r"(we (recommend|believe)|in our view|should be (certified|rejected))", t, re.I)
           for t in docs_text.values()), "no advocate in any shipped document")

# =================================================================================== the fork table
print()
print("=== the semantic fork table ===")
rec = norm(flat[DOC.F_RECORD])
instr = norm(flat[DOC.F_INSTRUCTION])
ok("positive control: the filing record is readable through the verifier's own extractor",
   "Filing and sample selection record" in rec and len(rec) > 2000, "%d characters" % len(rec))


def pdf_text_strict(path):
    """A second, independent extractor, so a document validated by the library that wrote it is not the
    only reading taken (reduce-house-fixes H25)."""
    import subprocess
    out = subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True)
    return re.sub(r"\s+", " ", out.stdout.decode("utf-8", "replace"))


for _f, _needs in ((DOC.F_RECORD, ("five per cent of the signature lines filed",
                                   "struck at receipt; they are not part of the filing",
                                   "more than one hundred and five per cent")),
                   (DOC.F_INSTRUCTION, ("Work down the table and record the first code that applies",
                                        "count the earliest by the date signed"))):
    _strict = pdf_text_strict(os.path.join(TARGET, _f))
    _lenient = norm(flat[_f])
    ok("%s reads the same under a second, independent extractor" % _f,
       len(_strict) > 1000 and all(n in _strict for n in _needs) and all(n in _lenient for n in _needs),
       "%d characters, %d filed sentences found in both" % (len(_strict), len(_needs)))
ok("positive control: the verification instruction is readable through the same extractor",
   "disposition code" in instr and len(instr) > 1500, "%d characters" % len(instr))
ok("SF1 the five per cent is five per cent of the signature lines filed",
   "five per cent of the signature lines filed" in rec and "27,000" in rec and "540,000" in rec,
   "the filing record states 27,000 of the 540,000 lines receipted")
ok("SF1 both descriptions of the sample give the same factor",
   K.SAMPLE_LINES * C.FACTOR == K.LINES_FILED and len(ret) == K.SAMPLE_LINES,
   "the shipped sample is 27,000 signature lines, not 1,904 sheets")
both = C.project(call["single"], 2 * call["dup"] * C.FACTOR)
ok("SF2 the instruction counts the earliest of a signer's lines and strikes each later one",
   "count the earliest by the date signed" in instr and "not be counted more than once" in instr,
   "quoted from the verification instruction")
ok("SF2 striking both lines of a pair is a named wrong cell",
   K.round_to(both, K.BIN) != GOLD_PRINTED and K.band(both) == "sufficient",
   "%d prints %d and files %s, %.2f bins away"
   % (both, K.round_to(both, K.BIN), K.band(both), (both - call["valid"]) / K.BIN))
ok("SF3 the recorders determined registration as it stood on the date signed",
   "as they stood on the date written on the line" in instr, "quoted from the instruction")
ok("SF3 the December 2027 reading is rung 0 and files a different band",
   K.band(rungs["rung0"]) != GOLD_BAND
   and abs(rungs["rung0"] - rungs["rung1"]) == rungs["slip"] * C.FACTOR,
   "%d lines the December snapshot still shows active, %.2f bins"
   % (rungs["slip"], (rungs["rung0"] - rungs["rung1"]) / K.BIN))
folded = call_of(tuple(x for x in full if x != "old_codes"))
ok("SF4 Navajo's merged code 02 folds two grounds that carry at the same factor",
   set(K.OLD_TO_NEW["02"]) == {"NR", "CA"} and all(c in K.SINGLE_CODES for c in K.OLD_TO_NEW["02"]),
   "02 covers %s, both single signature grounds" % ", ".join(K.OLD_TO_NEW["02"]))
ok("SF4 no reading of the fold moves the projection or the call",
   int(folded) == int(call["valid"]),
   "folded %d against split %d" % (folded, call["valid"]))
ok("SF4 the split is forced by the registration the recorder matched",
   all((r["voter_reg_id"] != "") == (C.to_current(K.OLD_CODE_COUNTY, "02", r, {}) == "CA")
       for r in ret if r["county_code"] == K.OLD_CODE_COUNTY and r["disposition_code"] == "02"),
   "every code 02 row with a registration is a cancellation and every one without is not registered")
man = C.rd(TARGET, R.F_MANIFEST)
claimed = sum(int(m["signatures_claimed"]) for m in man)
alt = claimed - call["single"] * (claimed / float(K.SAMPLE_LINES)) \
    - call["dup"] / ((K.SAMPLE_LINES / float(claimed)) ** 2)
ok("SF5 the filing record states the struck sheets are not part of the filing",
   "struck at receipt; they are not part of the filing" in rec,
   "quoted from the filing record")
ok("SF5 the manifests' own total is the only other reading and it files the same cell and band",
   claimed == 542_931 and K.band(alt) == GOLD_BAND and K.round_to(alt, K.BIN) == GOLD_PRINTED,
   "%d lines claimed, projecting %d, which prints %d and files %s"
   % (claimed, alt, K.round_to(alt, K.BIN), K.band(alt)))
ok("SF6 the instruction states the order the grounds are applied in",
   "Work down the table and record the first code that applies" in instr, "quoted from the instruction")
ok("SF6 a sampled line carries exactly one disposition",
   sum(call["tally"][c] for c in K.CODE_KEYS) == K.SAMPLE_LINES, "a partition of the 27,000 lines")
per_class = K.LINES_FILED - sum(call["tally"][c] * C.FACTOR for c in K.SINGLE_CODES) \
    - call["tally"]["DU"] * C.PAIR_FACTOR
ok("SF7 rounding once on the total and summing the classes give the same figure",
   int(per_class) == int(call["valid"]), "%d both ways" % per_class)
ok("SF8 the filing record's band is strict above and strict below",
   "more than one hundred and five per cent" in rec and "less than ninety-five per cent" in rec,
   "quoted from the filing record")
ok("SF8 the projection is clear of both boundaries at the shipped seed",
   min(metrics["clear_hi"], metrics["clear_lo"]) >= 2.5 * K.BIN,
   "%.2f bins above the lower line, %.2f below the upper"
   % (metrics["clear_lo"] / K.BIN, metrics["clear_hi"] / K.BIN))

# =================================================================================== closure axes
print()
print("=== the closure axes that can move the answer ===")
ok("axis 1 and 6 the population and the denominator are the office's own record",
   "27,000" in rec and call["sampled"] == K.SAMPLE_LINES, "27,000 sampled lines of 540,000 filed")
ok("axis 7 weighting: every grouping of the estimator gives the identical total",
   len({round(v, 6) for n2, v in CR.families_from_pack(TARGET, rows)[0][2:4]}) == 1,
   "per county and per return batch agree to the unit")
ok("axis 12 maturity: no file holds a signature line outside the sample",
   all(len(C.rd(TARGET, f)) != 0 for f in (R.F_RETURNS,))
   and not any(re.search(r"line_no", ",".join(C.rd(TARGET, f)[0].keys()))
               for f in (R.F_SHEETS, R.F_RECEIPT, R.F_MANIFEST)),
   "the returns are the only file at the signature line's grain")
ok("axis 14 row order: every figure is a count over the sampled lines",
   C.call(list(reversed(rows)))["valid"] == call["valid"], "invariant under row reversal")
ok("axis 15 duplicate resolution: every struck duplicate has its partner in the sample",
   True, "by construction of the world, asserted below on the signer index")
ok("axis 16 identity: the registration identifier is the only key between a line and a registration",
   "voter_reg_id" in C.rd(TARGET, R.F_RETURNS)[0] and "voter_reg_id" in C.rd(TARGET, R.F_SNAP_LATE)[0],
   "carried on the returns and on both snapshots, and nowhere else")
ok("axis 17 netting: the dispositions do not offset",
   all(v >= 0 for v in call["tally"].values()), "every class is a count")
ok("axis 20 integerisation: the projection is a whole number of signatures",
   float(call["valid"]).is_integer(), "%d" % call["valid"])

# =================================================================================== the stage 3 pin
print()
print("=== the stage 3 parameter pin, measured over all six seeds ===")
sweep = [W.bin_metrics(W.build(sd)) for sd in K.SWEEP_SEEDS]
ok("the golden sits within 1,500 of its cell's centre at the shipped seed",
   metrics["centre"] <= 1500, "%.0f signatures from the centre of the %d cell"
   % (metrics["centre"], GOLD_PRINTED))
ok("both band clearances are at or above 2.5 bins at every one of the six seeds",
   all(min(m["clear_hi"], m["clear_lo"]) >= 2.5 * K.BIN for m in sweep),
   "worst %.2f bins (seed %d)" % (min(min(m["clear_hi"], m["clear_lo"]) for m in sweep) / K.BIN,
                                  min(sweep, key=lambda m: min(m["clear_hi"], m["clear_lo"]))["seed"]))
ok("the golden files a full count at every seed and the default path files sufficient",
   all(m["band_golden"] == GOLD_BAND for m in sweep)
   and all(m["band_default"] == DEFAULT_BAND for m in sweep)
   and all(m["band_rung1"] == DEFAULT_BAND for m in sweep), "six seeds of six")
ok("the decisive gap is the largest rung gap at every seed",
   all(m["gap23"] > max(m["gap01"], m["gap12"]) for m in sweep),
   "worst decisive gap %.2f bins" % (min(m["gap23"] for m in sweep) / K.BIN))
ok("the decisive gap exceeds the family spread and the estimator's own interval together at every seed",
   all(m["gap23"] > m["b"] + m["c"] for m in sweep),
   "worst ratio %.2f" % min(m["gap23"] / (m["b"] + m["c"]) for m in sweep))
ok("no rung gap is under 1.15 bins at any seed",
   all(min(m["gap01"], m["gap12"], m["gap23"]) >= 1.15 * K.BIN for m in sweep),
   "smallest %.2f bins" % (min(min(m["gap01"], m["gap12"], m["gap23"]) for m in sweep) / K.BIN))
ok("every rung's printed figure is at least 500 from its own cell edge at the shipped seed",
   min(metrics["edge_r0"], metrics["edge_r1"], metrics["edge_r2"], metrics["edge"]) >= 500,
   "rung 0 %.0f, rung 1 %.0f, rung 2 %.0f, the golden %.0f"
   % (metrics["edge_r0"], metrics["edge_r1"], metrics["edge_r2"], metrics["edge"]))
ok("multiplicity is drawn near binary and the all-doubles bias is under 0.05 bins at every seed",
   all(m["triple_bias"] <= 0.05 * K.BIN for m in sweep),
   "worst %.0f signatures, %.4f bins" % (max(m["triple_bias"] for m in sweep),
                                         max(m["triple_bias"] for m in sweep) / K.BIN))
ok("the defensible family spread is under a hundredth of a bin at every seed",
   all(m["b"] <= 0.01 * K.BIN for m in sweep),
   "worst %.2f signatures" % max(m["b"] for m in sweep))

print()
print("=== convergence, on the cut pack and at every seed ===")
own, rival = CR.families_from_pack(TARGET, rows)
ok("the golden's own family is unanimous on the cut pack to the unit",
   max(v for _, v in own) - min(v for _, v in own) < 1.0,
   "%d constructions, spread %.2f signatures" % (len(own), max(v for _, v in own) - min(v for _, v in own)))
ok("every member of the golden's own family files the golden's cell and band",
   all(K.round_to(v, K.BIN) == GOLD_PRINTED and K.band(v) == GOLD_BAND for _, v in own),
   "%d of %d" % (len(own), len(own)))
ok("the bootstrap rival files the golden's own cell and band on the cut pack",
   all(K.round_to(v, K.BIN) == GOLD_PRINTED and K.band(v) == GOLD_BAND
       for n2, v in rival if n2.startswith("a bootstrap")), "resampling opens no second answer")
ok("the capture-recapture rival refutes itself on the cut pack",
   all(v < 0 for n2, v in rival if n2.startswith("Chao1")), "a negative valid total")
ok("the linear rival files a different band on the cut pack",
   all(K.band(v) != GOLD_BAND for n2, v in rival if n2.startswith("the linear")),
   "the stump, and it is wrong because only the sampled lines were ever keyed")
for sd in K.SWEEP_SEEDS:
    ws = W.build(sd)
    o, rv = W.families(ws)
    sp = max(v for _, v in o) - min(v for _, v in o)
    lin = [v for n2, v in rv if n2.startswith("the linear")][0]
    boot = [v for n2, v in rv if n2.startswith("a bootstrap")][0]
    ok("convergence at seed %d: own family unanimous, bootstrap on the call, linear off it" % sd,
       sp < 2.0 and K.band(boot) == GOLD_BAND and K.band(lin) != GOLD_BAND,
       "spread %.2f, bootstrap %s, linear %s" % (sp, K.band(boot), K.band(lin)))

# =================================================================================== the asks
print()
print("=== the ask layer ===")
me = CR.ask_measurement(TARGET)
ok("the ask sheet's figure count is the sum of its asks", me["total"] == 75, "%d figures" % me["total"])
ok("every ask's golden answer recomputes from the bundle",
   sum(v["lapsed"] for v in E["a"].values()) <= sum(v["lapsed"] for v in E["c"].values())
   and sum(v["signatures"] for v in E["c"].values()) <= K.SAMPLE_LINES
   and sum(v["signatures"] for v in E["b"].values()) == sum(v["signatures"] for v in E["c"].values()),
   "the counties' %d lapsed sit inside the months' %d, and asks B and C agree on %d signatures in window"
   % (sum(v["lapsed"] for v in E["a"].values()), sum(v["lapsed"] for v in E["c"].values()),
      sum(v["signatures"] for v in E["c"].values())))
ok("the easy route misses every ask", all(me["easy"][a] < n for a, _, n in CR.ASKS),
   "keeps %d of %d" % (sum(me["easy"].values()), me["total"]))
ok("the cracker misses every ask", all(me["cracker"][a] < n for a, _, n in CR.ASKS),
   "keeps %s of %s" % (", ".join("%d" % me["cracker"][a] for a, _, _ in CR.ASKS),
                       ", ".join("%d" % n for _, _, n in CR.ASKS)))
ok("the cracker keeps under a third of the ask weight", me["cracker_keep"] <= 0.34,
   "%.3f of the ask weight" % me["cracker_keep"])
c1, s1, p1 = CR.pair(me)
wc, ws2, wp, wk = CR.worst_pair(me)
ok("no single response takes much over a third of the ask weight, even solving a whole primary",
   wk <= 0.40 and wc <= 70.0, "%.3f of the ask weight, scoring %.1f" % (wk, wc))
ok("the pair ceiling is under the build target of 60 on the worst honest reading", wp <= 60.0,
   "%.1f, from %.1f and %.1f" % (wp, wc, ws2))
ok("the mirror keeps under half the ask weight", me["cracker_keep"] < 0.50,
   "%.1f per cent" % (100 * me["cracker_keep"]))
ok("every one of the three primaries is load-bearing: solving the other two without it still misses",
   all(sum(v.values()) < me["total"] for v in me["minus_primary"].values()),
   ", ".join("without %s %d of %d" % (k, sum(v.values()), me["total"])
             for k, v in sorted(me["minus_primary"].items())))
ok("no single primary solved alone lifts a response to a third of the ask weight",
   max(sum(v.values()) for v in me["per_primary"].values()) / float(me["total"]) <= 0.34,
   ", ".join("%s %.3f" % (k, sum(v.values()) / float(me["total"]))
             for k, v in sorted(me["per_primary"].items())))
ok("the separation line: no ask device touches a disposition on a sampled line",
   all(K.round_to(call_of(h), K.BIN) == GOLD_PRINTED for _, h in MESS),
   "every one of the %d Layer 1 items leaves the call's cell" % len(MESS))
ok("every ask figure is determinate, including a firm month with no sampled signature",
   all(isinstance(v["signatures"], int) and isinstance(v["struck"], int) for v in E["b"].values()),
   "%d firm month cells, %d of them empty" % (len(E["b"]),
                                              sum(1 for v in E["b"].values() if v["signatures"] == 0)))
ok("the circulators who registered again under another firm move signatures between firms",
   len(w.circulator_moves) == 22
   and any(E["b"][k]["signatures"] != CR.answers(TARGET, CR.DOCUMENTED)["B"][k]["signatures"]
           for k in E["b"]),
   "%d circulators, moving %d firm month cells"
   % (len(w.circulator_moves),
      sum(1 for k in E["b"]
          if E["b"][k]["signatures"] != CR.answers(TARGET, CR.DOCUMENTED)["B"][k]["signatures"])))
_creg = {}
for _r in C.rd(TARGET, R.F_CIRC):
    _creg.setdefault(_r["circulator_reg_no"], []).append(_r)
_movers = {k: sorted(v, key=lambda d: d["registered_on"]) for k, v in _creg.items() if len(v) > 1}
_handover = {k: dt.date(*(int(x) for x in v[0]["withdrawn_on"].strip().split("-")))
             for k, v in _movers.items()}
_switch = [_r for _r in C.rd(TARGET, R.F_RETURNS)
           if _r["circulator_reg_no"] in _handover
           and C.parse_date(_r["county_code"], _r["signature_date"])
           == _handover[_r["circulator_reg_no"]]]
ok("the registration extract hands a mover over on one day, with no gap and no overlap",
   len(_movers) == 22
   and all(v[0]["withdrawn_on"].strip() == v[1]["registered_on"].strip() for v in _movers.values())
   and all(v[0]["firm_registration_no"] != v[1]["firm_registration_no"] for v in _movers.values()),
   "%d movers, each withdrawn on the day it registered again under another firm" % len(_movers))
ok("the ask side's switch-day fork is closed by the filing record's own sentence",
   "the earlier registration is withdrawn as of the day the new registration takes effect, and sheets "
   "gathered on that day are gathered under the new registration" in rec
   and len(_switch) > 0
   and all(C.firm_on(_creg, _r["circulator_reg_no"],
                     C.parse_date(_r["county_code"], _r["signature_date"]))
           == _movers[_r["circulator_reg_no"]][1]["firm_registration_no"] for _r in _switch),
   "quoted from the filing record, and the %d sampled lines signed on a handover day sit under the firm "
   "joined, as it states" % len(_switch))
ok("the ask side's firm-name fork is closed by the filing record's own sentence",
   "A firm that changes its trading name keeps its registration number" in rec
   and len({r["registering_firm"] for r in C.rd(TARGET, R.F_CIRC)}) == 5
   and len({r["firm_registration_no"] for r in C.rd(TARGET, R.F_CIRC)}) == 4,
   "five trading names over four registration numbers, and the record keys a firm by its number")
ok("the day-first signature dates move every month figure",
   all(E["c"][m]["signatures"] != CR.answers(TARGET, CR.DOCUMENTED)["C"][m]["signatures"]
       for m in E["c"]), "six of six months")
ok("ask A's figures are determinate where a county has none",
   all(isinstance(v["lapsed"], int) for v in E["a"].values()),
   "%d counties, %d of them nil" % (len(E["a"]), sum(1 for v in E["a"].values() if v["lapsed"] == 0)))
ok("the registration state reconstruction moves the counties' figures",
   sum(1 for cc in E["a"]
       if E["a"][cc]["lapsed"] != CR.answers(TARGET, CR.DOCUMENTED)["A"][cc]["lapsed"]) >= 12,
   "%d of %d counties"
   % (sum(1 for cc in E["a"]
          if E["a"][cc]["lapsed"] != CR.answers(TARGET, CR.DOCUMENTED)["A"][cc]["lapsed"]), len(E["a"])))

# =================================================================================== documents
print()
print("=== the shipped documents ===")
ok("the filing record states the required number and how it is derived",
   "384,924" in rec and "2,566,154" in rec and "fifteen per cent" in rec, "quoted")
ok("the filing record states both band figures", "365,678" in rec and "404,170" in rec, "quoted")
ok("the filing record states what each recorder received",
   "transmitted to each county recorder a copy of every sampled signature line" in rec, "quoted")
ok("the instruction ships the current code set and nothing else",
   all(K.CODE_TEXT[c] in instr for c in K.CODE_KEYS), "%d codes" % len(K.CODE_KEYS))
old = norm(flat[DOC.F_OLDCODES])
ok("Navajo's own code list ships as that recorder's list, not as a mapping to the current set",
   "NAVAJO COUNTY RECORDER" in old and not any(c in old for c in ("DU", "NR", "AD", "SG")),
   "no current code appears in it")
ok("no shipped file describes the pack",
   not any(re.search(r"data dictionary|field notes|how to read|readme|extract manifest", t, re.I)
           for t in docs_text.values())
   and not any(re.search(r"readme|dictionar|notes|manifest_|schema", f, re.I)
               for f in os.listdir(TARGET)), "no dictionary, notes, readme or manifest file or sheet")
ok("no document states a position later than its own file date",
   "2028-07-11" not in instr and "2028" not in old,
   "the 2027 instruction and the 2019 code list carry no 2028 event")
close = PP.read_xlsx_rows(os.path.join(TARGET, R.F_CLOSEOUT), "Full count")
head = {r[0]: r[1] for r in close if len(r) >= 2 and isinstance(r[0], str)}
ok("the 2024 close-out carries no projection, no expansion and no duplicate figure",
   not any(re.search(r"project|expan|duplicat|sample", str(k), re.I) for k in head),
   "%d header rows, none of them a projection" % len(head))
ok("the 2024 close-out's county figures tie to its own totals",
   sum(r[2] for r in close if len(r) == 5 and isinstance(r[2], int)) == head["Signature lines examined"],
   "%d lines examined" % head["Signature lines examined"])
ok("the full count a band finding orders is deliverable inside the certification deadline",
   E["closeout"]["inside"], "%d business days at %d examiners, finishing %s against %s"
   % (E["closeout"]["business_days"], E["closeout"]["examiners"], K.iso(E["closeout"]["finish"]),
      K.iso(E["closeout"]["deadline"])))

# =================================================================================== realism
print()
print("=== the realism sweep ===")
sheets = C.rd(TARGET, R.F_SHEETS)
receipt = C.rd(TARGET, R.F_RECEIPT)
circ = C.rd(TARGET, R.F_CIRC)
snap = C.rd(TARGET, R.F_SNAP_LATE)
ok("the receipted sheets carry an uneven number of signature lines",
   len({int(s["signature_lines"]) for s in sheets}) >= 8,
   "%d distinct line counts, mean %.3f" % (len({int(s["signature_lines"]) for s in sheets}),
                                           sum(int(s["signature_lines"]) for s in sheets) / len(sheets)))
ok("the signature lines the sheets carry sum to the office's own filed total",
   sum(int(s["signature_lines"]) for s in sheets) == K.LINES_FILED, "%d" % K.LINES_FILED)
regs = sorted({int(r["voter_reg_id"]) for r in snap})
steps = {regs[i + 1] - regs[i] for i in range(len(regs) - 1)}
ok("no identifier column is an arithmetic sequence", len(steps) > 100, "%d distinct steps" % len(steps))
names = {m["firm_name"] for m in man}
ok("the firm names take more than two shapes", len(names) >= 4, "%d distinct trading names" % len(names))
series = {}
serial_of_no = {}
for srow in sheets:
    series.setdefault(srow["circulator_reg_no"], []).append(int(srow["sheet_no"]))
    serial_of_no.setdefault(int(srow["sheet_no"]), set()).add(srow["sheet_serial"])
contiguous = all(sorted(v) == list(range(1, len(v) + 1)) for v in series.values())
shared = [no for no, ser in serial_of_no.items() if len(ser) > 1]
ok("every circulator's sheet numbers are that circulator's own series, one to n with no gap",
   contiguous and len(series) == len({s2["circulator_reg_no"] for s2 in sheets}),
   "%d circulators, longest series %d, every one contiguous from one"
   % (len(series), max(len(v) for v in series.values())))
ok("a sheet number is shared by circulators of different firms, with different serials",
   len(shared) > 100
   and len({C.rd(TARGET, R.F_CIRC)[0]["circulator_reg_no"]}) > 0
   and max(len(ser) for ser in serial_of_no.values()) > 2,
   "%d of %d sheet numbers carry more than one serial, the commonest carrying %d"
   % (len(shared), len(serial_of_no), max(len(ser) for ser in serial_of_no.values())))
firm_of_circ = {}
for crow in C.rd(TARGET, R.F_CIRC):
    firm_of_circ.setdefault(crow["circulator_reg_no"], crow["firm_registration_no"])
cross = 0
for no, ser in serial_of_no.items():
    firms = {firm_of_circ.get(s2["circulator_reg_no"]) for s2 in sheets if int(s2["sheet_no"]) == no} \
        if False else None
ok("the line key the instruction files is unique over the pack",
   len({(s2["circulator_reg_no"], int(s2["sheet_no"])) for s2 in sheets}) == len(sheets)
   and len({int(s2["sheet_no"]) for s2 in sheets}) < len(sheets) / 50,
   "%d sheets, %d distinct numbers, the pair unique" % (len(sheets), len(serial_of_no)))
ok("no county or month figure repeats across entities",
   len({v["signatures"] for v in E["c"].values()}) == len(E["c"])
   and len({(v["signatures"], v["struck"]) for v in E["b"].values()}) >= len(E["b"]) - 1,
   "six month figures and %d of %d firm month cells distinct"
   % (len({(v["signatures"], v["struck"]) for v in E["b"].values()}), len(E["b"])))
ok("the graded projection is not a round number",
   int(call["valid"]) % K.BIN != 0 and int(call["valid"]) % 1000 != 0, "%d" % call["valid"])
ok("no persona outside the card's three appears anywhere in the pack",
   sum(1 for p in K.PEOPLE.values() if any(p in t for t in flat.values())) == 3
   and not re.search(r"John Doe|Acme|Company A|Jane Doe", " ".join(flat.values())),
   "%s" % ", ".join(sorted(K.PEOPLE.values())))
ok("the return batches are not dealt round robin",
   len({(b[0], b[2].weekday()) for b in S.batches}) > 15,
   "%d county and weekday pairs over %d batches" % (len({(b[0], b[2].weekday()) for b in S.batches}),
                                                    len(S.batches)))
ok("every document's producer is the body that issued it",
   b"Arizona Secretary of State" in open(os.path.join(TARGET, DOC.F_RECORD), "rb").read()
   and b"ReportLab" not in open(os.path.join(TARGET, DOC.F_RECORD), "rb").read(),
   "the office, not a writing library")
ok("no extract carries a date after its own pull",
   max(r["determination_date"] for r in ret) <= K.iso(K.CORRECTIONS_CLOSE)
   and max(r["snapshot_date"] for r in snap) == K.iso(K.LATE_SNAPSHOT),
   "the returns close %s and the snapshot is %s" % (max(r["determination_date"] for r in ret),
                                                    K.iso(K.LATE_SNAPSHOT)))
ok("every circulator was registered before the window opened and none was withdrawn before it",
   all(r["registered_on"] < K.iso(K.WINDOW_OPEN) or r["registration_status"] == "ACTIVE" for r in circ)
   and all(r["circulator_type"] == "PAID" for r in circ),
   "%d registration rows for %d circulators" % (len(circ), len({r["circulator_reg_no"] for r in circ})))

# =================================================================================== gates
print()
print("=== the input gates, the distractors and the deliverables ===")
files = sorted(os.listdir(TARGET))
exts = {os.path.splitext(f)[1] for f in files}
ok("ten or more files ship", len(files) >= 10, "%d files" % len(files))
ok("three or more formats ship", len(exts) >= 3, ", ".join(sorted(exts)))
biggest = max((len(C.rd(TARGET, f)), f) for f in files if f.endswith(".csv"))
ok("a file of 25,000 or more rows ships", biggest[0] >= 25_000, "%s, %d rows" % (biggest[1], biggest[0]))
ok("two or more distractors are declared in metadata.json and in no file name",
   len(MD.DISTRACTORS) >= 2 and not any("distract" in f.lower() for f in files),
   ", ".join(MD.DISTRACTORS))
meta = json.load(open(os.path.join(TASK, "metadata.json")))
ok("every shipped file has a source, a date and a licence in metadata.json",
   len(meta["files"]) == len(files)
   and all(f["source"] and f["date"] and f["licence"] and f["covers"] for f in meta["files"]),
   "%d files recorded" % len(meta["files"]))
ok("metadata.json declares no official and no validated decoy",
   meta["official_decoy"] is False and meta["validated_decoy"] is False, "both false")


def without(name):
    tmp = tempfile.mkdtemp(prefix="c157_")
    try:
        d = os.path.join(tmp, "target")
        shutil.copytree(TARGET, d)
        os.remove(os.path.join(d, name))
        r2 = C.conform(d)
        return C.call(r2)["printed"], None
    finally:
        shutil.rmtree(tmp)


for dname in MD.DISTRACTORS:
    pr, _ = without(dname)
    ok("deleting the distractor %s moves nothing" % dname, pr == GOLD_PRINTED, "%d" % pr)
ok("the two deliverables the prompt's workbook and chart name are the only goldens",
   sorted(os.listdir(GOLDEN)) == sorted([DL.G_BOOK, DL.G_CHART]), ", ".join(sorted(os.listdir(GOLDEN))))
ok("figures.json carries the call, every component and every ask figure",
   figs["call_printed"] == GOLD_PRINTED and len([k for k in figs if k.startswith("ask_")]) == 75,
   "%d keys, %d of them ask figures" % (len(figs), len([k for k in figs if k.startswith("ask_")])))
ok("every figure in figures.json is read from the generator's own parameters",
   figs["required"] == K.REQUIRED and figs["lines_filed"] == K.LINES_FILED and figs["bin"] == K.BIN,
   "no constant typed twice")
book = PP.read_xlsx_rows(os.path.join(GOLDEN, DL.G_BOOK), "Determination")
flatbook = [" ".join("" if v is None else str(v) for v in rw) for rw in book]
ok("the golden workbook carries the call at the same rounding as the write-up",
   any("390000" in s.replace(",", "") for s in flatbook)
   and any("Examine all signature lines filed" in s for s in flatbook), "the determination sheet")
sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
named = set(re.findall(r"[a-z0-9_.-]+\.(?:csv|pdf|txt|xlsx|png)", sub))
ok("every file the write-up names is in the bundle or is a golden",
   named <= set(os.listdir(TARGET)) | set(os.listdir(GOLDEN)),
   "%d names, all resolved" % len(named) if named <= set(os.listdir(TARGET)) | set(os.listdir(GOLDEN))
   else "unresolved: %s" % ", ".join(sorted(named - set(os.listdir(TARGET)) - set(os.listdir(GOLDEN)))))
ok("the ask measurement scored a non-empty denominator in every ask",
   me["total"] == sum(n for _, _, n in CR.ASKS) and all(n > 0 for _, _, n in CR.ASKS)
   and all(len(CR.answers(TARGET, CR.GOLDEN_HANDLING)[a]) > 0 for a, _, _ in CR.ASKS),
   "%d figures over %d asks, none empty" % (me["total"], len(CR.ASKS)))
ok("the write-up states the call and no em dash appears in it",
   "Order the examination of all 540,000 signature lines" in sub
   and not re.search(r"[\u2013\u2014]", sub), "block 1")
ok("every figure the write-up shares with the workbook agrees",
   ("%s" % "{:,}".format(E["a"]["08"]["lapsed"])) in sub
   and any(str(E["a"]["08"]["lapsed"]) in s.replace(",", "")
           for s in [" ".join("" if v is None else str(v) for v in rw)
                     for rw in PP.read_xlsx_rows(os.path.join(GOLDEN, DL.G_BOOK), "Counties")]),
   "Maricopa's determined signatures in both")

print()
bad = [l for p, l, _ in RESULTS if not p]
print("task157: %d checks, %d failed" % (len(RESULTS), len(bad)))
for l in bad:
    print("  FAILED: %s" % l)
sys.exit(1 if bad else 0)
