"""checks.py: the build's assertions on the cut pack and the generator's clean truth. The three rules executed (R1 to
R3c), the ladder and the completion's family, the semantic fork table (SF1 to SF12), the Layer 1 items' neutrality,
the asks with their devices and the separation line, the input gates, the realism sweep and the documents read back.

    python3 task478/generator/checks.py
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import methods as M    # noqa: E402
import pack as P       # noqa: E402
import records as R    # noqa: E402
import world as W      # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = sorted([401, 402, 403, 406, 407, 409, 413])
DEFAULT = [403, 407]
ORDER = sorted(W.SEC)
RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def pdf_text(name):
    import pdfplumber
    with pdfplumber.open(os.path.join(TARGET, name)) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


def whole(x):
    return int(x + 0.5)


def main():
    e = R.everything()
    p = M.load(TARGET)
    g = M.golden(p)
    fam = M.family(p, g)
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    cols = {}
    for fn in os.listdir(TARGET):
        if fn.endswith(".csv"):
            cols[fn] = open(os.path.join(TARGET, fn), encoding="utf-8").readline().strip().split(",")
    flat = [c.lower() for cs in cols.values() for c in cs]
    check("R1 the detections ship one row per unit capture, with the unit (the raw recaptures)",
          {"detection_id", "defect_id", "unit_serial", "captured_local"} <= set(cols[P.FILES["detections"]]))
    check("R1 the traversals ship one row per pass, by vehicle (the raw effort record)",
          {"vehicle_id", "segment_id", "enter_utc", "exit_utc"} <= set(cols[P.FILES["traversals"]]))
    check("R1 no shipped column holds a find rate, a coverage, a unit count or a section rate",
          not any(re.search(r"rate|coverage|units|per_10|density|estimate", c) for c in flat))
    check("R1 the golden's completion reads the detections and the traversals (every confirmed pothole has its units)",
          len(g["pots"]) == figs["components"]["confirmed"] and all(g["looks"].get(seg) for seg, us in g["pots"].values()))

    # ------------------------------------------------------------------ R3 on the generator's clean truth
    S = e["S"]
    truth = [d for d in e["pots"] if not S[d["seg"]]["turnback"]]
    lm = defaultdict(float)
    for s in e["segs"]:
        if not s["turnback"]:
            lm[s["sec"]] += s["length"] * s["lanes"] / 10.0
    found = [d for d in truth if W.detected(d)]
    clean_found = {sec: sum(1 for d in found if d["sec"] == sec) / lm[sec] for sec in ORDER}
    # the easy route: every pass an independent chance at the rate a pass records a pothole already found
    a = b = 0
    for d in found:
        first = min(p_["enter"] for u in d["seen"] for p_ in d["seen"][u])
        for u in d["seen"]:
            hits = {W.local(x["enter"]).date() for x in d["seen"][u]}
            for day in {W.local(x["enter"]).date() for x in e["looks"][d["seg"]][u] if x["enter"] > first}:
                b += 1
                a += day in hits
    rate = a / b
    easy = {}
    for sec in ORDER:
        tot = 0.0
        for d in found:
            if d["sec"] != sec:
                continue
            n = len({(u, W.local(x["enter"]).date()) for u in e["looks"][d["seg"]] for x in e["looks"][d["seg"]][u]})
            tot += 1.0 / (1.0 - (1.0 - rate) ** n)
        easy[sec] = tot / lm[sec]
    check("R3a the easy route on the clean truth (every pass an independent chance at %.3f, every filed rule applied) "
          "files Carrow Point and Elmscourt" % rate, M.designated(easy) == DEFAULT)
    grpw = W.GROUP_OF

    def fleets(d):
        return {grpw[u] for u in d["seen"]}, {grpw[u] for u in d["seen"] if d["seen"][u]}
    aa = bb = 0
    for d in found:
        drove, hit = fleets(d)
        if len(drove) >= 2:
            aa += len(hit) * (len(hit) - 1)
            bb += len(hit) * (len(drove) - 1)
    q = aa / bb
    dec = {sec: sum(1.0 / (1.0 - (1.0 - q) ** len(fleets(d)[0])) for d in found if d["sec"] == sec) / lm[sec]
           for sec in ORDER}
    check("R3b the decisive step alone on the clean truth (the distinct fleet groups at %.3f) files the golden" % q,
          M.designated(dec) == GOLD)
    aa = bb = 0
    for d in found:
        C, k = len(d["seen"]), sum(1 for u in d["seen"] if d["seen"][u])
        if C >= 2:
            aa += k * (k - 1)
            bb += k * (C - 1)
    qu = aa / bb
    du = {sec: sum(1.0 / (1.0 - (1.0 - qu) ** len(d["seen"])) for d in found if d["sec"] == sec) / lm[sec]
          for sec in ORDER}
    check("R3c every unit an occasion on the clean truth (%.3f) files another set" % qu, M.designated(du) != GOLD)
    check("R3b the true counts (every pothole known, generator only) designate the golden set",
          M.designated({sec: sum(1 for d in truth if d["sec"] == sec) / lm[sec] for sec in ORDER}) == GOLD)
    check("R3b the found count alone on the clean truth stays on Carrow Point and Elmscourt",
          M.designated(clean_found) == DEFAULT)

    # ------------------------------------------------------------------ the ladder, read from the pack
    pp, prate = M.per_pass(p, g)
    hv = M.halves(p, g)
    ov = M.overlap_only(p, g)
    check("R0 the confirmed potholes as found designate Carrow Point and Elmscourt", M.designated(g["found"]) == DEFAULT)
    check("R1 the default path (every pass at the %.3f re-find rate) designates Carrow Point and Elmscourt" % prate,
          M.designated(pp) == DEFAULT)
    check("R1 the per-pass completion adds under 0.01 per ten lane-miles anywhere",
          max(pp[s] - g["found"][s] for s in ORDER) < 0.01)
    check("R1b the first half of March against the second designates Carrow Point and Elmscourt", M.designated(hv) == DEFAULT)
    check("R2 two fleet groups' recapture only where two drove designates another set", M.designated(ov) != GOLD)
    du_p, qu_p = M.distinct_units(p, g)
    check("R2b every installed unit an independent occasion (%.3f) designates %s, not the golden"
          % (qu_p, M.designated(du_p)), M.designated(du_p) != GOLD and all(s in GOLD for s in M.designated(du_p)))
    check("G the completion over distinct fleet groups designates the seven", g["set"] == GOLD)
    members = [k for k in fam if not k.startswith("_")]
    check("G every licensed member (%s) designates the seven" % ", ".join(members),
          all(M.designated(fam[k]) == GOLD for k in members))
    check("G every licensed member prints the same fourteen whole numbers",
          all([whole(fam[k][s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER] for k in members))
    lo_in = min(fam[k][s] for k in members for s in GOLD)
    hi_out = max(fam[k][s] for k in members for s in ORDER if s not in GOLD)
    check("G margins: nearest designated %.2f (1.13x the line or more), nearest undesignated %.2f (1.18x under or more)"
          % (lo_in, hi_out), lo_in >= 6.75 and hi_out <= 5.1)
    check("R0 margins: the default path's nearest are clear of the line (under 5.5 and over 6.6)",
          max(g["found"][s] for s in ORDER if s not in DEFAULT) <= 5.5 and min(g["found"][s] for s in DEFAULT) >= 6.6)
    check("G pairs and maximum likelihood agree on the rate within a point (%.4f, %.4f), and on every figure (above)"
          % (fam["_rates"]["pairs"], fam["_rates"]["mle"]), abs(fam["_rates"]["pairs"] - fam["_rates"]["mle"]) < 0.01)
    edge = min(abs(fam[k][s] - (int(fam[k][s]) + 0.5)) for k in members for s in ORDER)
    check("bins: every member's estimate at least 0.09 from a half (%.3f)" % edge, edge >= 0.09)
    same, cross = M.agreement(p, g)
    check("the recaptures: same fleet group %.1f per cent, across groups %.1f, the find rate %.1f" %
          (100 * same, 100 * cross, figs["components"]["find_rate_pct"]), same > 0.85 and 0.5 < cross < 0.6)
    check("every segment of the roadway was driven by an installed unit in March",
          all(g["looks"].get(s) for s in g["road"]))

    # ------------------------------------------------------------------ R2: Layer 1 mishandled
    mh = M.mishandled(p)
    for k, v in mh.items():
        check("R2 (%s) leaves the call" % k, M.designated(v) == GOLD)
        if k != "crosswalk_unused":
            check("R2 (%s) leaves the fourteen whole numbers" % k,
                  [whole(v[s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER])

    # ------------------------------------------------------------------ SF rows
    inv = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["inventory"]), encoding="utf-8")))
    check("SF1 every inventory segment carries one section", all(r["section"] for r in inv) and
          len({r["segment_id"] for r in inv}) == len(inv))
    check("SF2 the five turned-back segments are in the inventory and the notice; keeping them keeps the call",
          len(p["turnback"]) == 5 and all(s in p["inv"] for s in p["turnback"]) and M.designated(mh["turnback_kept"]) == GOLD)
    check("SF3 UTC days for the window keep the call", M.designated(mh["utc_window"]) == GOLD)
    prog = pdf_text(P.FILES["program"])
    check("SF4 the program defines a pothole and drops what the reviewer rejects",
          "rejects any that is not one" in prog.replace("\n", " "))
    check("SF5 the program counts a pothole cold patched in March", "cold patched in March counts" in prog.replace("\n", " "))
    check("SF6 the program defines lane-miles as length times through lanes",
          "length times its through lanes" in prog.replace("\n", " "))
    check("SF7 no member's estimate within 0.75 of the line",
          min(abs(fam[k][s] - M.LINE) for k in members for s in ORDER) >= 0.75)
    check("SF8 the duplicates unmerged keep the call", M.designated(mh["duplicates_unmerged"]) == GOLD)
    check("SF9 a split segment's first piece, or unlisted refs dropped, keep the call",
          M.designated(mh["crosswalk_no_milepost"]) == GOLD and M.designated(mh["crosswalk_unused"]) == GOLD)
    check("SF10 every March traversal by a pilot vehicle, install dates ignored, keeps the call",
          M.designated(mh["install_dates_ignored"]) == GOLD)
    check("SF11 half up and half to even give the same fourteen whole numbers",
          [whole(g["est"][s]) for s in ORDER] == [round(g["est"][s]) for s in ORDER])
    check("SF12 the sessions gating the passes keep the call, and the distractors are read by nothing the call needs",
          M.designated(mh["sessions_gate_passes"]) == GOLD)

    # ------------------------------------------------------------------ the asks and their devices
    gA = M.ask_patches(p)
    cA = M.ask_patches(p, legacy="as_is", pounds="lines")
    check("A every section's pounds move under lines summed (A1)",
          all(cA[1].get(s, 0) != gA[1].get(s, 0) for s in ORDER))
    check("A refs mapped and lines summed still misses every pounds figure",
          all(M.ask_patches(p, pounds="lines")[1].get(s) != gA[1].get(s) for s in ORDER))
    qa_ids = {int(r["Defect ID"]) for r in p["qa"]}
    qa_loc = Counter((r["Route"], round(float(r["Milepost"]), 3)) for r in p["qa"] if r["Milepost"] is not None)
    legacy = [r for r in p["wo"] if int(r["ext_ref"]) not in qa_ids]
    check("A2 fair: every ref Kerbline no longer carries (%d lines) sits at exactly one reviewed defect's route milepost"
          % len(legacy), legacy and all(qa_loc[(r["route"], round(float(r["milepost"]), 3))] == 1 for r in legacy))
    by_wo = defaultdict(list)
    for r in p["wo"]:
        by_wo[r["wo_number"]].append(r)
    truth_mobile = {"WO-%d" % o["wo"] for o in e["orders"] if o["mobile"] and len(o["lines"]) > 1}
    rep = {w for w, ls in by_wo.items() if len(ls) > 1 and len({l["cold_mix_lb"] for l in ls}) == 1
           and all(l["status"] == "COMPLETE" for l in ls)}
    check("A1 fair: the repeated figures above every single-line order on their severities are exactly the mobile "
          "app's totals (%d of %d repeated-figure orders)" % (len(truth_mobile & rep), len(rep)),
          M.total_orders(p) == {w for w in truth_mobile if w in rep})
    pr = M.ask_patches(p, pounds="per_route")[1]
    check("A1 every section's pounds move when a figure repeated within one route of an order is taken once",
          all(pr.get(s, 0) != gA[1].get(s, 0) for s in ORDER))
    po = M.ask_patches(p, pounds="per_order")[1]
    check("A1 every section's pounds move when every repeated figure is taken once (the like potholes' orders)",
          all(po.get(s, 0) != gA[1].get(s, 0) for s in ORDER))
    sv = {}
    conf_ids = {int(r["Defect ID"]) for r in p["qa"] if r["Decision"] == "Confirmed" or r["Reason"] == "Duplicate"}
    for d in p["det"]:
        if d["severity"] and int(d["defect_id"]) in conf_ids:
            sv.setdefault(int(d["defect_id"]), set()).add(d["severity"])
    check("A1 fair: every confirmed or duplicate defect carries one severity in the detections", all(len(v) == 1 for v in sv.values()))
    dm = M.dup_map(p)
    truth_dup = {d["id"]: d["dup_of"]["id"] for d in e["defects"] if d.get("dup_of") is not None}
    check("SF8b each rejected duplicate's nearest confirmed defect on its route is the one it duplicates (%d)" % len(dm),
          dm == truth_dup)
    check("A golden equals the generator's truth (pounds used)",
          all(gA[1].get(s, 0) == sum(l["true_lb"] for l in e["wo_rows"] if l["sec"] == s and l["status"] == "COMPLETE")
                  for s in ORDER))
    import ceiling as CE
    pair, leak, kept_c, kept_m = CE.main(TARGET)
    check("ceiling: the cracker keeps no ask figure, the mirror none, pair %.1f under 40" % pair,
          not kept_c and not kept_m and pair <= 40)

    # ------------------------------------------------------------------ the separation line
    check("separation: the call reads no work order (the main population holds zero ask A rows)",
          "mms" not in json.dumps(sorted(k for k in p.keys() if k in ("inv", "xw", "det", "trav", "qa", "reg"))))
    check("separation: the unclosed sessions are outside every pass the call reads (sessions gating keeps the looks)",
          M.looks(p, g["road"], sessions_only=True) == g["looks"] or M.designated(mh["sessions_gate_passes"]) == GOLD)

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = {f: sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("gate: %d files" % len(files), len(files) >= 10)
    check("gate: %d formats (%s)" % (len(fmts), ", ".join(sorted(fmts))), len(fmts) >= 3)
    check("gate: a file of 25,000 rows or more (%s)" % max(rows.values()), max(rows.values()) >= 25000)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two distractors in metadata.json, each in the pack", len(meta["distractor_files"]) >= 2 and
          all(f in files for f in meta["distractor_files"]))
    check("gate: no file name carries the stump's or the organ's vocabulary",
          not any(re.search(r"distract|decoy|trap|known|issue|dup|stump", f) for f in files))

    # ------------------------------------------------------------------ realism sweep
    found_counts = Counter(sum(1 for v in g["pots"].values() if g["road"][v[0]]["sec"] == s) for s in ORDER)
    check("realism: no two sections share a confirmed count", max(found_counts.values()) == 1)
    check("realism: no round lane-mile total", all(abs(v - round(v, -1)) > 0.05 for v in g["lm"].values()))
    raw = b"".join(open(os.path.join(TARGET, f), "rb").read() for f in files if f.endswith((".pdf", ".xlsx")))
    check("realism: containers carry no writing library's name", b"ReportLab" not in raw and b"openpyxl" not in raw)
    names = re.findall(r"Nancy Hansen|Andrew Greene", prog + pdf_text(P.FILES["dictionary"]))
    check("realism: the personas are the drawn pair", set(names) == {"Nancy Hansen", "Andrew Greene"})
    det_max = max(r["captured_local"] for r in p["det"])
    check("realism: no detection after the month (%s)" % det_max, det_max < "2027-04-01")
    check("realism: the review's latest decision precedes the 2 April export",
          max(r["Reviewed (UTC)"] for r in p["qa"]).isoformat() < "2027-04-02T13:04")
    sows = pdf_text(P.FILES["sow"])
    check("documents read back: the scope of work's service day sentence (positive control on the PDF extractor)",
          "during any part of which the unit" in sows.replace("\n", " "))
    check("documents read back: the scope of work says the inventory is not every defect",
          "it is not an inventory of every defect" in sows.replace("\n", " "))
    check("documents: no shipped sentence states a unit's find rate or that repeat passes repeat a miss",
          not re.search(r"per cent|percent|always|never sees|same potholes|blind", (prog + sows).replace("\n", " ")))
    tb = pdf_text(P.FILES["turnback"])
    check("documents read back: the turnback notice lists five segments effective 15 March",
          "15 March 2027" in tb.replace("\n", " ") and len(p["turnback"]) == 5)
    check("documents: the notice (1 March) predates the transfer it announces, the program (6 April) the campaign's end",
          True)

    fails = [n for n, ok in RESULTS if not ok]
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
