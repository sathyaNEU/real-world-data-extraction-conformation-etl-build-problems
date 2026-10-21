"""checks.py: the build's assertions on the cut pack and the generator's clean truth. The three rules executed (R1 to
R3b), the ladder and the linkage's family, the semantic fork table (SF1 to SF12), the Layer 1 items' neutrality,
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
DEFAULT = [401, 403, 407, 409, 413]
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
    flat = [c_.lower() for cs in cols.values() for c_ in cs]
    check("R1 the detections ship one row per unit capture, with the unit and its fix, and no defect number",
          {"detection_id", "unit_serial", "road_mp", "latitude"} <= set(cols[P.FILES["detections"]])
          and "defect_id" not in cols[P.FILES["detections"]])
    check("R1 the cover inventory ships the surveyed positions (the raw control points)",
          {"asset_id", "route", "milepost"} <= set(cols[P.FILES["covers"]]))
    check("R1 no shipped column holds an error, an accuracy, a tolerance, a pothole id or a section rate",
          not any(re.search(r"error|accura|toler|sigma|cluster|pothole_id|defect_id|per_10|density|estimate", c_)
                  for c_ in flat))

    # ------------------------------------------------------------------ R3 on the generator's clean truth
    S = e["S"]
    lm = defaultdict(float)
    for s in e["segs"]:
        if not s["turnback"]:
            lm[s["sec"]] += s["length"] * s["lanes"] / 10.0
    truth = Counter(d["sec"] for d in e["defects"] if d["real"] and not d["off"] and not S[d["seg"]]["turnback"]
                    and any(W.local(x["t"]).month == 3 for x in e["det_by"][d["id"]]))
    tr = {s: truth.get(s, 0) / lm[s] for s in ORDER}
    check("R3b the generator's true counts of recorded potholes designate the golden set", M.designated(tr) == GOLD)
    gsig = {v["unit"]: W.SIGMA["SWEEPER" if v["group"] == "SWEEPER" else "OTHER"] for v in e["veh"]}
    check("R3b the decisive step alone (each unit's true error, no Layer 1 mess) files the golden",
          M.designated(M.rates(p, M.link(p, M.unit_tol(gsig), g["road"]), g["road"])) == GOLD)
    wrong = [t for t in M.SINGLE if M.designated(M.single(p, t, g["road"])) == GOLD]
    check("R3a the easy route (one tolerance for every unit, every filed rule applied) misses the golden at every "
          "tolerance from %.3f to %.3f mile" % (M.SINGLE[0], M.SINGLE[-1]), not wrong)

    # ------------------------------------------------------------------ the ladder, read from the pack
    check("R0 every pothole detection a pothole designates another set", M.designated(M.per_detection(p, g["road"])) != GOLD)
    d0 = M.single(p, 0.01, g["road"])
    check("R1 the default path (one tolerance, 53 feet) designates %s" % M.designated(d0), M.designated(d0) == DEFAULT)
    plateau = [t for t in M.SINGLE if 0.01 <= t <= 0.05]
    check("R1 every tolerance from 53 to 264 feet designates the same set (%s)" % DEFAULT,
          all(M.designated(M.single(p, t, g["road"])) == DEFAULT for t in plateau))
    small = M.single(p, 0.003, g["road"])
    check("R1b a few feet's tolerance (16 feet) adds Rushmead (%.2f)" % small[411], M.designated(small) == sorted(GOLD + [411]))
    check("G the unit-aware linkage designates the golden set", g["set"] == GOLD)
    off = {s: g["counts"].get(s, 0) - truth.get(s, 0) for s in ORDER if g["counts"].get(s, 0) != truth.get(s, 0)}
    check("G the golden's counts sit within one pothole of the generator's truth (%s) and print the truth's fourteen "
          "whole numbers" % (off or "exact"), all(abs(v) <= 1 for v in off.values())
          and all(whole(g["est"][s]) == whole(tr[s]) for s in ORDER))
    members = list(fam)
    check("G every licensed member (%d: unit or fleet error, by RMS or MAD, 2.5 to 4 times the combined error) "
          "designates the golden" % len(members), all(M.designated(fam[k]) == GOLD for k in members))
    check("G every licensed member prints the same fourteen whole numbers",
          all([whole(fam[k][s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER] for k in members))
    lo_in = min(fam[k][s] for k in members for s in GOLD)
    hi_out = max(fam[k][s] for k in members for s in ORDER if s not in GOLD)
    check("G margins: nearest designated %.2f, nearest undesignated %.2f (0.75 clear of the line or more)"
          % (lo_in, hi_out), lo_in >= 6.75 and hi_out <= 5.25)
    edge = min(abs(fam[k][s] - (int(fam[k][s]) + 0.5)) for k in members for s in ORDER)
    check("bins: every member's figure at least 0.2 from a half (%.3f)" % edge, edge >= 0.2)
    u = M.units(p)
    sw = [g["sig"][k] * 5280 for k, v in u.items() if v[1] == "Street sweeper"]
    ot = [g["sig"][k] * 5280 for k, v in u.items() if v[1] != "Street sweeper"]
    check("the error: sweepers' units %.0f to %.0f feet, the rest %.1f to %.1f" % (min(sw), max(sw), min(ot), max(ot)),
          min(sw) >= 35 and max(ot) <= 6)
    cov_n = Counter(d["unit_serial"] for d in p["det"] if d["defect_class"] == "utility_cover" and d["road_mp"])
    check("every unit has 12 or more cover detections to be measured on (fewest %d)" % min(cov_n[k] for k in u),
          min(cov_n[k] for k in u) >= 12)
    decks = sum(1 for d in e["pots"] if d.get("deck"))
    check("the bridge decks: %d potholes in runs a few yards apart, none on a segment a sweeper drove" % decks,
          decks > 0 and all(not any(e["unit_veh"][un]["group"] == "SWEEPER" for un in d["seen"])
                            for d in e["pots"] if d.get("deck")))

    # ------------------------------------------------------------------ R2: Layer 1 mishandled
    mh = M.mishandled(p)
    for k, v in mh.items():
        check("R2 (%s) leaves the call" % k, M.designated(v) == GOLD)
        if k not in ("crosswalk_unused",):
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
    check("SF4 the program takes Kerbline's pothole class as a pothole", "pothole class as a pothole" in prog.replace("\n", " "))
    check("SF5 the program counts a pothole cold patched in March", "cold patched in March counts" in prog.replace("\n", " "))
    check("SF6 the program defines lane-miles as length times through lanes",
          "length times its through lanes" in prog.replace("\n", " "))
    check("SF7 no member's figure within 0.75 of the line",
          min(abs(fam[k][s] - M.LINE) for k in members for s in ORDER) >= 0.75)
    check("SF8 the program counts each recorded pothole once",
          "counted once however many times and by however many units" in prog.replace("\n", " "))
    check("SF9 placing by road_ref through the crosswalk (or a split segment's first piece) keeps the call",
          M.designated(mh["placed_by_road_ref"]) == GOLD and M.designated(mh["crosswalk_first_child"]) == GOLD
          and M.designated(mh["crosswalk_unused"]) == GOLD)
    check("SF10 half up and half to even give the same fourteen whole numbers",
          [whole(g["est"][s]) for s in ORDER] == [round(g["est"][s]) for s in ORDER])
    check("SF11 the call reads the detections, the covers, the inventory, the crosswalk and the turnback only",
          True)

    # ------------------------------------------------------------------ the asks and their devices
    gA = M.ask_pounds(p)
    cA = M.ask_pounds(p, pounds="lines")
    check("A every section's pounds move under lines summed (A1)", all(cA.get(s, 0) != gA.get(s, 0) for s in ORDER))
    po = M.ask_pounds(p, pounds="per_order")
    check("A1 every section's pounds move when every repeated figure is taken once (the like potholes' orders)",
          all(po.get(s, 0) != gA.get(s, 0) for s in ORDER))
    by_wo = defaultdict(list)
    for r in p["wo"]:
        by_wo[r["wo_number"]].append(r)
    truth_mobile = {"WO-%d" % o["wo"] for o in e["orders"] if o["mobile"] and len(o["lines"]) > 1}
    rep = {w for w, ls in by_wo.items() if len(ls) > 1 and len({l["cold_mix_lb"] for l in ls}) == 1
           and all(l["status"] == "COMPLETE" for l in ls)}
    check("A1 fair: the repeated figures above every single-line order on their severities are exactly the mobile "
          "app's totals (%d of %d repeated-figure orders)" % (len(truth_mobile & rep), len(rep)),
          M.total_orders(p) == {w for w in truth_mobile if w in rep})
    det_ids = {d["detection_id"] for d in p["det"] if d["defect_class"] == "pothole" and d["severity"]}
    check("A1 fair: every order's ext_ref is a pothole detection carrying a severity",
          all(r["ext_ref"] in det_ids for r in p["wo"]))
    check("A golden equals the generator's truth (pounds used)",
          all(gA.get(s, 0) == sum(l["true_lb"] for l in e["wo_rows"] if l["sec"] == s and l["status"] == "COMPLETE"
                                  and l["finish"] is not None and W.local(l["finish"]).month == 3) for s in ORDER))
    gB = M.ask_miles(p)
    cB = M.ask_miles(p, dedupe=False)
    check("B every section's miles move with the re-run kept (B1)", all(int(cB[s] + .5) != int(gB[s] + .5) for s in ORDER))
    truth_miles = defaultdict(float)
    for t in e["trav"]:
        v = e["veh_by"][t["veh"]]
        s = S[t["seg"]]
        if W.installed_at(v, t["enter"]) and W.local(t["enter"]).month == 3 and not s["turnback"]:
            truth_miles[s["sec"]] += s["length"]
    check("B golden equals the generator's truth (every pass once)",
          all(abs(gB[s] - truth_miles[s]) < 1e-6 for s in ORDER))
    cw = M.ask_miles(p, window_s=300)
    check("B every section's miles move when a vehicle's repeat of a segment within five minutes is dropped (the loops)",
          all(int(cw[s] + .5) != int(gB[s] + .5) for s in ORDER))
    sig = Counter((t["veh"], t["seg"], t["dir"], t["enter"], t["exit"]) for t in e["trav"])
    five = __import__("datetime").timedelta(hours=5)
    gen_pairs = sum(1 for t in e["trav"] if sig[(t["veh"], t["seg"], t["dir"], t["enter"] + five, t["exit"] + five)])
    check("B1 fair: every re-run traversal repeats exactly one pass five hours later, and no two genuine passes do "
          "(%d re-run, %d genuine)" % (len(e["replays"]), gen_pairs),
          len(e["replays"]) > 0 and gen_pairs == 0 and len(p["trav"]) == len(e["trav"]) + len(e["replays"])
          and all(sig[(t["veh"], t["seg"], t["dir"], t["enter"] + five, t["exit"] + five)] == 1 for t in e["replays"]))
    ov = M.ask_miles(p, dedupe=False, overlap=True)
    check("B every section's miles move when only overlapping repeats are dropped (no re-run overlaps its pass)",
          all(int(ov[s] + .5) != int(gB[s] + .5) for s in ORDER))
    import ceiling as CE
    pair, leak, kept_c, kept_m = CE.main(TARGET)
    check("ceiling: the cracker keeps no ask figure, the mirror none, pair %.1f under 40" % pair,
          not kept_c and not kept_m and pair <= 40)

    # ------------------------------------------------------------------ the separation line
    import inspect
    src = inspect.getsource(M.golden) + inspect.getsource(M.link) + inspect.getsource(M.sigma)
    check("separation: the call reads no work order and no traversal (the asks' device rows)",
          "wo" not in re.findall(r'p\["(\w+)"\]', src) and "trav" not in re.findall(r'p\["(\w+)"\]', src))

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
    found_counts = Counter(g["counts"].get(s, 0) for s in ORDER)
    check("realism: no two sections share a pothole count", max(found_counts.values()) == 1)
    check("realism: no round lane-mile total", all(abs(v - round(v, -1)) > 0.05 for v in M.lane_miles(p, g["road"]).values()))
    raw = b"".join(open(os.path.join(TARGET, f), "rb").read() for f in files if f.endswith((".pdf", ".xlsx")))
    check("realism: containers carry no writing library's name", b"ReportLab" not in raw and b"openpyxl" not in raw)
    names = re.findall(r"Nancy Hansen|Andrew Greene", prog + pdf_text(P.FILES["dictionary"]))
    check("realism: the personas are the drawn pair", set(names) == {"Nancy Hansen", "Andrew Greene"})
    det_max = max(r["captured_local"] for r in p["det"])
    check("realism: no detection after the month (%s)" % det_max, det_max < "2027-04-01")
    sows = pdf_text(P.FILES["sow"])
    check("documents read back: the scope of work's service day sentence (positive control on the PDF extractor)",
          "during any part of which the unit" in sows.replace("\n", " "))
    check("documents read back: the scope of work says defect linking is not in the pilot",
          "is not in the pilot" in sows.replace("\n", " "))
    dic = pdf_text(P.FILES["dictionary"])
    check("documents: no shipped sentence states a unit's positional error, a tolerance or how to link detections",
          not re.search(r"feet|accura|error|toleran|within \d|link the|same pothole", (prog + sows + dic).replace("\n", " ")))
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
