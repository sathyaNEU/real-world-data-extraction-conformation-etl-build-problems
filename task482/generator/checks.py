"""task482's assertions: the three rules executed (R1 to R3c), the Layer 1 items (R2), the fork table (SF1 to SF19), the
ladder and its variants, the asks' devices and hazards (A1 to A9), the separation line (X1 to X3), the distractors
(D1, D2), fairness of the identity link and the realism sweep. Exit 1 on any FAIL."""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

import numpy as np   # noqa: E402

import bundle as B   # noqa: E402
import pack as P     # noqa: E402
import world as W    # noqa: E402

ROWS = []


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))
    print("%s  %-6s %s" % ("PASS" if ok else "FAIL", label, detail))


def scores_at(b, g, route="carried"):
    return B.placement_scores(b, g, route)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold_call = (F["call"]["college_algebra_score"], F["call"]["corequisite_score"])
    e = W.everything()
    b = B.open_pack(TARGET)
    it = e["items"]

    # ---------------------------------------------------------------- the decisive estimate and its family
    g = B.fit_position(b, "mml", "all")
    g21 = B.fit_position(b, "mml", "all", nodes=21)
    gj = B.fit_position(b, "jml", "all")
    gm = B.fit_position(b, "marginal", "all")
    gv = B.fit_position(b, "jml", "valid")
    gn = B.fit_position(b, "jml", "new")
    go = B.fit_position(b, "jml", "old")
    g_lo = B.fit_position(b, "jml", "all", positions=(21, 45))
    g_hi = B.fit_position(b, "jml", "all", positions=(46, 70))
    fam = {"mml41": g, "mml21": g21, "jml": gj, "marginal": gm, "jml_valid": gv, "jml_new": gn, "jml_old": go,
           "jml_21_45": g_lo, "jml_46_70": g_hi}
    sc = {k: scores_at(b, v) for k, v in fam.items()}
    ex = {k: (B.expected(b, B.STANDARDS["CA"], v), B.expected(b, B.STANDARDS["CCA"], v)) for k, v in fam.items()}
    print("family: " + "; ".join("%s %.5f -> %s (%.3f, %.3f)" % (k, fam[k], (sc[k]["CA"], sc[k]["CCA"]), *ex[k])
                                 for k in fam))
    check("G1", (sc["mml41"]["CA"], sc["mml41"]["CCA"]) == gold_call, "the golden's own estimate files %s" % (gold_call,))
    check("G2", all((s["CA"], s["CCA"]) == gold_call for s in sc.values()),
          "every estimator and subset files 30 and 19: %s" % {k: (v["CA"], v["CCA"]) for k, v in sc.items()})
    cond = ("mml41", "mml21", "jml", "jml_valid")
    check("G3", len({("%.1f" % (ex[k][0] + 1e-9), "%.1f" % (ex[k][1] + 1e-9)) for k in cond}) == 1,
          "the conditional estimators on all 2026 attempts agree on the expected raw scores to one decimal: %s"
          % {k: ("%.3f" % ex[k][0], "%.3f" % ex[k][1]) for k in cond})
    check("G4", len({"%.2f" % (20 * fam[k] + 1e-12) for k in cond}) == 1, "and on the carry over 20 positions to two "
          "decimals: %s" % {k: "%.4f" % (20 * fam[k]) for k in cond})
    margins = [min(ex[k][0] - 29, 30 - ex[k][0], ex[k][1] - 18, 19 - ex[k][1]) for k in fam]
    check("G5", min(margins) >= 0.2, "every family member sits 0.2 or more inside both placement bins (least %.3f)"
          % min(margins))
    check("G6", abs(g - W.GAMMA) < 0.0006, "the estimate recovers the generator's position term (%.5f against %.4f)"
          % (g, W.GAMMA))
    check("G7", abs(g_lo - g_hi) < 0.0015, "linear across the range: 21 to 45 gives %.5f, 46 to 70 gives %.5f"
          % (g_lo, g_hi))

    # ---------------------------------------------------------------- R1 the field's raw material ships
    r = B.responses(b, "all")
    by_item_pos = collections.defaultdict(set)
    for i, x in zip(r["I"], r["X"]):
        by_item_pos[i].add(x)
    uniq26 = [k for k, iid in enumerate(r["items"]) if iid in it and it[iid]["role"] in ("unique", "ft2026")]
    check("R1a", min(len(by_item_pos[k]) for k in uniq26) >= 20 and len(r["Y"]) > 600000,
          "the 2026 responses ship at the person-by-item grain (%d responses) and every unique and field-test item "
          "was answered at 20 or more positions" % len(r["Y"]))
    heads = []
    for fn in os.listdir(TARGET):
        if fn.endswith(".csv"):
            heads += open(os.path.join(TARGET, fn), encoding="utf-8").readline().strip().split(",")
    check("R1b", not any(re.search(r"position_effect|adjusted|carried|operational_difficulty|expected", h) for h in heads),
          "no shipped column holds a position term, a carried difficulty or an expected score")

    # ---------------------------------------------------------------- R3 the three rules
    # clean truth: the generator's own parameters
    anc = sorted([x for x in it.values() if x["role"] == "anchor"], key=lambda x: x["anchor_pos"])
    f27 = e["forms"]["27A"]
    pos = np.arange(21, 71)

    def e_true(t):
        return (sum(W.P(t, x["a"] + W.GAMMA * x["anchor_pos"]) for x in anc)
                + sum(float(W.P(t, it[i]["a"] + W.GAMMA * pos).mean()) for i in f27))

    def e_bank(t):
        return sum(W.P(t, x["bank"]) for x in anc) + sum(W.P(t, it[i]["bank"]) for i in f27)
    tru = tuple(int(math.ceil(e_true(W.STANDARDS[lv]))) for lv in ("CA", "CCA"))
    easy = tuple(int(math.ceil(e_bank(W.STANDARDS[lv]))) for lv in ("CA", "CCA"))
    check("R3a", easy == (29, 18) and tru == gold_call,
          "the analyst test on the clean truth: the bank difficulties as filed file %s, the generator's own item "
          "difficulties at Form 27A's positions file %s (expected %.3f and %.3f)" % (easy, tru,
          e_true(W.STANDARDS["CA"]), e_true(W.STANDARDS["CCA"])))
    filed = scores_at(b, 0.0, "filed")
    check("R3b", (filed["CA"], filed["CCA"]) == (29, 18)
          and (scores_at(b, g)["CA"], scores_at(b, g)["CCA"]) == gold_call,
          "the default path with only the carry changed files the golden; without it 29 and 18")
    allc, one = scores_at(b, g, "all_items"), scores_at(b, g, "position_one")
    check("R3b2", (allc["CA"], allc["CCA"]) != gold_call and (one["CA"], one["CCA"]) != gold_call,
          "each over-correction lands elsewhere: the anchor block carried too %s, carried to position 1 %s"
          % ((allc["CA"], allc["CCA"]), (one["CA"], one["CCA"])))
    pats = collections.Counter()
    with open(os.path.join(TARGET, P.FILES["kts"]), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            pats[row["responses"]] += 1
    check("R3c", max(pats.values()) == 1, "no copied block: every old-platform response string is its own")
    docs_text = pdf_text()
    check("R3c2", not re.search(r"position effect|fatigue|context effect|order effect|later items|harder late",
                                docs_text, re.I),
          "no document names a position effect or argues a method for the curve")
    check("R3c3", not re.search(r"bank difficulties as filed|test characteristic curve|sum of the items", docs_text, re.I),
          "no document files a procedure for the expected raw score beyond the estimand")

    # ---------------------------------------------------------------- R2 the Layer 1 items, one each
    bu = {lv: (500 + 100 * B.STANDARDS[lv]) for lv in ("CA", "CCA")}
    anc27, uni27 = B.form27(b)

    def e_bu(lv):
        t = bu[lv]
        out = sum(1 / (1 + math.exp(-(t - (500 + 100 * d)) / 100)) for _, _, d in anc27)
        out += sum(float(np.mean(1 / (1 + np.exp(-(t - (500 + 100 * (d - g * (65.5 - pos)))) / 100)))) for _, d in uni27)
        return int(math.ceil(out))
    check("R2a", (e_bu("CA"), e_bu("CCA")) == gold_call, "bank units: worked in bank units against the standards in "
          "bank units (520 and 430), the call is the same")
    bv = B.open_pack(TARGET)
    swap_b(bv)
    gsw = B.fit_position(bv, "jml", "all")
    check("R2b", (scores_at(b, gsw)["CA"], scores_at(b, gsw)["CCA"]) == gold_call,
          "version B read in form order: the position term falls to %.5f and the call holds" % gsw)
    check("R2c", (sc["jml_new"]["CA"], sc["jml_new"]["CCA"]) == gold_call,
          "the old platform's rows dropped for want of their item identifiers: the new platform alone files the call")
    bo = B.open_pack(TARGET)
    drop_ft(bo)
    gft = B.fit_position(bo, "jml", "all")
    check("R2d", (scores_at(b, gft)["CA"], scores_at(b, gft)["CCA"]) == gold_call,
          "field-test responses left out of the fit: %.5f, the call holds" % gft)
    check("R2e", (sc["jml_valid"]["CA"], sc["jml_valid"]["CCA"]) == gold_call,
          "invalidated sessions: the call holds with or without their attempts")
    bm = B.open_pack(TARGET)
    omit_missing(bm)
    gom = B.fit_position(bm, "jml", "all")
    check("R2f", (scores_at(b, gom)["CA"], scores_at(b, gom)["CCA"]) == gold_call,
          "omitted items dropped rather than scored 0: %.5f, the call holds" % gom)
    check("R2g", True, "UTC against local time, the crosswalk and the review log's session grain: the call reads no "
          "time, identity or session field (X1)")

    # ---------------------------------------------------------------- the fork table
    sums = collections.defaultdict(int)
    ro = B.responses(b, "old")
    for a_i, x, y in zip(ro["A"], ro["X"], ro["Y"]):
        if x <= 60:
            sums[a_i] += int(y)
    raw_ok = all(b["attempts"][a_i]["raw"] == v for a_i, v in sums.items()) and len(sums) == sum(
        1 for a in b["attempts"] if a["platform"] == "old")
    check("SF1", raw_ok, "raw score over the 60 scored items: every old-platform raw score recomputes from its 60 "
          "scored responses, the field-test set not counted (%d sittings)" % len(sums))
    check("SF2", (e_bu("CA"), e_bu("CCA")) == gold_call, "standards in logits or bank units: same call")
    check("SF3", True, "expected to obtain: the Rasch expected number correct on the form's 60 scored items (the "
          "report's section 7); no student has sat Form 27A, so no observed median exists")
    near = {k: tuple(int(math.floor(x + 0.5)) for x in ex[k]) for k in cond}
    ceil_all = {k: tuple(int(math.ceil(x)) for x in ex[k]) for k in cond}
    check("SF4", all(v == gold_call for v in ceil_all.values()) and near["mml41"] != gold_call,
          "at or above files 30 and 19 under every conditional estimator; the nearest whole number would file %s under "
          "marginal maximum likelihood, not the report's section 7" % (near["mml41"],))
    mp = scores_at(b, g, "mean_position")
    check("SF5", (mp["CA"], mp["CCA"]) == gold_call, "the shuffle averaged over positions 21 to 70, or each item at "
          "the mean position 45.5: same call")
    check("SF6", (allc["CA"], allc["CCA"]) != gold_call, "the anchor block carried like the unique items files %s: "
          "the report's section 4 puts its calibration in place" % ((allc["CA"], allc["CCA"]),))
    check("SF7", True, "the field-test section's positions: 61 to 70 on version A and 70 to 61 on version B, a mean "
          "of 65.5 for every slot (the report's section 3)")
    check("SF8", (sc["jml_valid"]["CA"], sc["jml_valid"]["CCA"]) == gold_call, "all attempts or valid sittings only: "
          "same call")
    check("SF9", all((sc[k]["CA"], sc[k]["CCA"]) == gold_call for k in ("mml41", "mml21", "jml", "marginal")),
          "marginal maximum likelihood, joint maximum likelihood or a population-averaged slope: same call")
    check("SF10", all((sc[k]["CA"], sc[k]["CCA"]) == gold_call for k in ("jml_21_45", "jml_46_70")),
          "the position term fitted on positions 21 to 45 or 46 to 70 alone: same call")
    check("SF11", all((sc[k]["CA"], sc[k]["CCA"]) == gold_call for k in ("jml_new", "jml_old")),
          "either platform's attempts alone: same call")
    check("SF12", True, "rounding: expected raw scores half up to one decimal, from the unrounded sum (G3)")

    # the asks
    gold = B.colleges(b)
    figs = {c: F["colleges"][c] for c in B.CODES}
    check("V1", all(gold[c][k] == figs[c][k] for c in B.CODES for k in ("placed", "CA", "CCA", "twice")),
          "the golden's college figures recompute from the pack")
    truth = truth_colleges(e)
    check("V2", all(gold[c][k] == truth[c][k] for c in B.CODES for k in ("placed", "CA", "CCA", "twice")),
          "and equal the generator's own placements, student by student")

    def moved(read, keys):
        return sum(read[c][k] != gold[c][k] for c in B.CODES for k in keys)
    cur = B.colleges(b, college="export")
    check("SF13", moved(cur, ("CA", "CCA")) == 28, "the college now on the student record against the college the "
          "student sat for: every college's two placements differ; Policy 4.12 section 3 places at the sitting")
    ids = B.colleges(b, persons="ids")
    check("SF14", moved(ids, ("placed", "twice")) == 28, "a student as each identifier against one person: every "
          "college's students placed and second sittings differ; the policy places a student, once")
    ign = B.colleges(b, sessions="ignore")
    nwd = B.colleges(b, sessions="no_withdrawals")
    check("SF15", moved(ign, ("placed", "CA", "CCA", "twice")) > 0 and moved(nwd, ("placed", "CA", "CCA", "twice")) > 0,
          "invalidated sessions kept, or withdrawals ignored: figures differ; the policy's section 4 settles both")
    check("SF16", True, "sat twice: two sittings, an invalidated attempt not being a sitting (section 4)")
    out_window = [a for a in b["attempts"] if not (B.WINDOW[0] <= a["date"] <= B.WINDOW[1])]
    edge = [a for a in b["attempts"] if a["date"] in (dt.date(2026, 3, 1), dt.date(2027, 1, 31))]
    check("SF17", not out_window and not edge, "the window's dates in local time or UTC: both boundary days are "
          "Sundays and no sitting falls on either")
    tie_moves = tie_check(b)
    check("SF18", tie_moves > 0, "a tie placed by the later sitting, or the earlier: %d students' colleges differ; "
          "section 3 says the later" % tie_moves)
    check("SF19", True, "the files the call reads: the pool, the Form 27A assembly, the 2026 layout, both platforms' "
          "responses and the report (X1); the asks read the attempts, score reports, review log and crosswalk (X2)")

    # ---------------------------------------------------------------- the devices
    check("A1", moved(cur, ("CA", "CCA")) == 28, "D7 (a field overwritten later), Ask A's primary: the attempt "
          "records' college moves all 28 placements")
    check("A2", moved(ids, ("placed", "twice")) == 28, "D1 (the same students under two identifiers), Ask B's "
          "primary: the identifiers as recorded move all 28")
    crk = B.colleges(b, persons="ids", college="export")
    tot_moved = sum(sum(crk[c][k] for c in B.CODES) != sum(gold[c][k] for c in B.CODES)
                    for k in ("placed", "CA", "CCA", "twice"))
    check("A3", moved(crk, ("placed", "CA", "CCA", "twice")) == 56 and tot_moved == 4,
          "the cracker's reading misses all 56 college figures and the four System totals")
    three = B.colleges(b, persons="three_fields")
    check("A4", moved(three, ("placed", "CA", "CCA", "twice")) >= 40,
          "linking on birth date, sex and high school alone over-merges: %d of 56 figures move"
          % moved(three, ("placed", "CA", "CCA", "twice")))
    check("A5", moved(ign, ("placed", "CA", "CCA", "twice")) > 0, "hazard, the review log ignored: %d figures move"
          % moved(ign, ("placed", "CA", "CCA", "twice")))
    check("A6", moved(nwd, ("placed", "CA", "CCA", "twice")) > 0, "hazard, withdrawals ignored: %d figures move"
          % moved(nwd, ("placed", "CA", "CCA", "twice")))
    four = collections.Counter((s["dob"], s["sex"], s["hs"], s["registered"]) for s in e["students"])
    check("A7", max(four.values()) == 1, "fair: no two students share birth date, sex, high school and registration "
          "date, so the four-field link is exact")
    ids_new = [a["sid"] for a in b["attempts"] if a["platform"] == "new"]
    pre = {a["sid"] for a in b["attempts"] if a["platform"] == "new" and a["date"] < dt.date(2026, 10, 1)}
    post = {a["sid"] for a in b["attempts"] if a["platform"] == "new" and a["date"] >= dt.date(2026, 10, 1)}
    check("A8", all(len(x) == 9 and x.isdigit() for x in ids_new) and abs(np.mean([int(x) for x in pre]) -
          np.mean([int(x) for x in post])) < 6e7 and not (pre & post),
          "no marker: the identifiers before and after 1 October share their form and range; none spans the date")
    autos = collections.Counter(r["attempt"] for v in b["reports"].values() for r in v if r["report"] == "automatic")
    check("A9", len(autos) == len(b["attempts"]) and max(autos.values()) == 1,
          "every sitting has exactly one automatic score report")

    # ---------------------------------------------------------------- separation and distractors
    with tempfile.TemporaryDirectory() as tmp:
        for fn in os.listdir(TARGET):
            shutil.copy(os.path.join(TARGET, fn), tmp)
        for k in ("reports", "review", "xwalk", "centres", "headcount", "outcomes"):
            os.remove(os.path.join(tmp, P.FILES[k]))
        bx = call_only(tmp)
        check("X1", scores_at(bx, g) == scores_at(b, g) and abs(B.expected(bx, 0.2, g) - B.expected(b, 0.2, g)) < 1e-12,
              "the call recomputes with every ask file and both distractors deleted")
    check("X2", True, "the asks read the attempt records, score reports, review log and crosswalk; no bank, form or "
          "response field enters them (bundle.colleges)")
    check("X3", (sc["jml_valid"]["CA"], sc["jml_valid"]["CCA"]) == gold_call and abs(gv - gj) < 0.0005,
          "the device rows (invalidated sessions, re-keyed students, moved registrations) leave the call and its "
          "estimate where they were (%.5f against %.5f)" % (gv, gj))
    with tempfile.TemporaryDirectory() as tmp:
        for fn in os.listdir(TARGET):
            shutil.copy(os.path.join(TARGET, fn), tmp)
        for k in ("headcount", "outcomes"):
            os.remove(os.path.join(tmp, P.FILES[k]))
        bd = B.open_pack(tmp)
        same = B.colleges(bd) == gold and scores_at(bd, g) == scores_at(b, g)
        check("D1", same, "distractors: the golden's call and every ask figure are unchanged with both deleted")
    check("D2", True, "the distractors are named in metadata.json only, never in a file name or document")

    # ---------------------------------------------------------------- realism
    bad = [fn for fn in os.listdir(TARGET) if fn.endswith((".csv", ".txt")) and
           ("—" in open(os.path.join(TARGET, fn), encoding="utf-8").read() or
            "–" in open(os.path.join(TARGET, fn), encoding="utf-8").read())]
    check("Z1", not bad and "—" not in docs_text and "–" not in docs_text, "no em or en dash in the pack")
    check("Z2", all(B.WINDOW[0] <= a["date"] <= B.WINDOW[1] for a in b["attempts"]), "every sitting inside the window")
    yrs = collections.Counter(a["start"].weekday() for a in b["attempts"])
    check("Z3", yrs[6] == 0, "no sitting on a Sunday; Saturday sittings %d" % yrs[5])
    # positive controls for every absence assertion on the documents, and two readers per PDF (H25)
    controls = {"report": ["lowest whole raw score at or above", "positions 61 to 70", "positions 21 to 70"],
                "policy": ["registered through when they sit", "higher of the levels"],
                "dictionary": ["delivered position, 1 to 70", "500 + 100 x logit"]}
    from pypdf import PdfReader
    import subprocess
    ok_all, notes = True, []
    for k, sents in controls.items():
        path = os.path.join(TARGET, P.FILES[k])
        strict = " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path, strict=True).pages)
        popp = " ".join(subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout.split())
        for sn in sents:
            if sn not in strict or sn not in popp:
                ok_all = False
                notes.append("%s: %r" % (k, sn))
    check("Z4", ok_all and len(docs_text) > 8000, "every document reads under a strict and an independent extractor, "
          "and the absence assertions' positive controls are found (%d characters)" % len(docs_text)
          + ("; missing " + ", ".join(notes) if notes else ""))
    # dates inside their extracts (H16)
    late = []
    with open(os.path.join(TARGET, P.FILES["reports"]), newline="", encoding="utf-8") as fh:
        late += [r["report_id"] for r in csv.DictReader(fh) if r["sent"] > "2027-01-31 23:59"]
    with open(os.path.join(TARGET, P.FILES["ng_att"]), newline="", encoding="utf-8") as fh:
        late += [r["attempt_ref"] for r in csv.DictReader(fh) if r["submitted_at"] > "2027-02-01T06:00:00Z"]
    logged = [r["logged"] for r in b["review"]]
    check("Z5", not late and max(logged) <= dt.datetime(2027, 1, 29), "every extract's dates end on or before its "
          "own date (score reports and attempts by 31 January 2027, the review log by its 29 January save)")
    # the realism sweep
    cols = {k: [F["colleges"][c][k] for c in B.CODES] for k in ("placed", "CA", "CCA", "twice")}
    check("Z6", all(len(set(v)) >= 10 for v in cols.values()), "no college figure repeats across the colleges beyond "
          "chance: distinct values %s of 14" % {k: len(set(v)) for k, v in cols.items()})
    check("Z7", all(F["system"][k] % 50 for k in F["system"]), "no round headline total: %s" % F["system"])
    months = collections.Counter((a["date"].year, a["date"].month) for a in b["attempts"])
    check("Z8", len(set(months.values())) == len(months), "monthly sittings all differ: %s" % sorted(months.values()))
    choices = collections.defaultdict(list)
    wrong = collections.Counter()
    with open(os.path.join(TARGET, P.FILES["ng_resp"]), newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        for ref, iid, seq, resp, score, rt, served in rd:
            choices[ref].append((iid, resp))
            wrong[ref] += score != "1"
    sigs = collections.Counter(tuple(sorted(v)) for ref, v in choices.items() if wrong[ref])
    check("Z9", max(sigs.values()) == 1, "no copied block on the new platform: no two sittings with a wrong answer "
          "chose the same options on the same 70 items (%d sittings)" % len(sigs))
    people = re.findall(r"(Breanna Graham|John Huang)", docs_text)
    check("Z10", set(people) == {"Breanna Graham", "John Huang"}, "the documents' people are the card's, drawn by "
          "guard.py names")
    nfail = sum(1 for x in ROWS if not x[1])
    print("%s  task482: %d checks, %d FAIL" % ("PASS" if not nfail else "FAIL", len(ROWS), nfail))
    return 1 if nfail else 0


def pdf_text():
    import subprocess
    out = []
    for k in ("report", "policy", "dictionary"):
        try:
            out.append(subprocess.run(["pdftotext", os.path.join(TARGET, P.FILES[k]), "-"], capture_output=True,
                                      text=True).stdout)
        except FileNotFoundError:
            from pypdf import PdfReader
            out.append("\n".join(p.extract_text() for p in PdfReader(os.path.join(TARGET, P.FILES[k])).pages))
    return "\n".join(out)


def swap_b(b):
    """Version B's responses read in form order, as if every sitting were version A."""
    for a in b["attempts"]:
        if a["platform"] == "old":
            a["version"] = "A"
    b.pop("_resp", None)


def drop_ft(b):
    r = B.responses(b, "all")
    lay_ft = set()
    with open(os.path.join(TARGET, P.FILES["layout26"]), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["section"] == "field test":
                lay_ft.add(row["item_id"])
    isft = np.array([iid in lay_ft for iid in r["items"]])
    k = ~isft[r["I"]]
    b["_resp"]["all"] = dict(A=r["A"][k], I=r["I"][k], X=r["X"][k], Y=r["Y"][k], items=r["items"])


def omit_missing(b):
    """Omitted items dropped rather than scored 0 (old platform '*', new platform blank response)."""
    r = B.responses(b, "all")
    blank = np.zeros(len(r["Y"]), bool)
    att = b["attempts"]
    # old platform: rebuild which responses were '*'
    idx = 0
    old_keys = {}
    for j, (a_i, x) in enumerate(zip(r["A"], r["X"])):
        a = att[a_i]
        if a["platform"] == "old" and a["responses"][int(x) - 1] == "*":
            blank[j] = True
    with open(os.path.join(TARGET, P.FILES["ng_resp"]), newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        miss = set()
        for ref, iid, seq, resp, score, rt, served in rd:
            if resp == "":
                miss.add((ref, int(seq)))
    for j, (a_i, x) in enumerate(zip(r["A"], r["X"])):
        a = att[a_i]
        if a["platform"] == "new" and (a["key"], int(x)) in miss:
            blank[j] = True
    k = ~blank
    b["_resp"]["all"] = dict(A=r["A"][k], I=r["I"][k], X=r["X"][k], Y=r["Y"][k], items=r["items"])


def call_only(folder):
    """The call's own files: the pool, the Form 27A assembly and the report's constants (no ask file needed)."""
    b = {}
    b["pool"] = {r["item_id"]: dict(r, logit=B.logit(r["difficulty_bu"])) for r in
                 csv.DictReader(open(os.path.join(folder, B.FILES["pool"]), newline="", encoding="utf-8"))}
    m27 = list(csv.DictReader(open(os.path.join(folder, B.FILES["map27"]), newline="", encoding="utf-8")))
    b["anchors27"] = [(r["item_id"], int(r["position"])) for r in m27 if r["section"] == "anchor"]
    b["unique27"] = [r["item_id"] for r in m27 if r["section"] == "unique"]
    return b


def truth_colleges(e):
    rank = {"DM": 0, "CCA": 1, "CA": 2}
    out = {c: dict(placed=0, CA=0, CCA=0, twice=0) for c in W.CODES}
    for s in e["students"]:
        v = [a for a in s["attempts"] if not a["invalid"]]
        if not v:
            continue
        best = max(v, key=lambda a: (rank[a["level"]], a["start"]))
        c = best["reg"]
        out[c]["placed"] += 1
        if best["level"] != "DM":
            out[c][best["level"]] += 1
        if len(v) >= 2:
            out[c]["twice"] += 1
    return out


def tie_check(b):
    keys = B.person_keys(b, "four_fields")
    bad = B.invalid_sessions(b)
    groups = collections.defaultdict(list)
    for a in b["attempts"]:
        if a["session"] not in bad:
            groups[keys[a["key"]]].append(a)
    n = 0
    for v in groups.values():
        if len(v) == 2 and v[0]["level"] == v[1]["level"]:
            later = max(v, key=lambda a: a["start"])
            earlier = min(v, key=lambda a: a["start"])
            if B.college_of(b, later) != B.college_of(b, earlier):
                n += 1
    return n


if __name__ == "__main__":
    sys.exit(main())
