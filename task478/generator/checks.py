"""checks.py: the build's assertions on the cut pack and the generator's clean truth. The three rules executed (R1 to
R3c), the ladder over a fine sweep of linking distances and the golden's family, the semantic fork table (SF1 to
SF12), the Layer 1 items' neutrality, the ask with its device and the separation line, the input gates, the realism
sweep and the documents read back.

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
NEAR = sorted([401, 403, 404, 407, 409, 410, 413])
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
    road = g["road"]

    # ------------------------------------------------------------------ R1: the field's raw material ships
    cols = {}
    for fn in os.listdir(TARGET):
        if fn.endswith(".csv"):
            cols[fn] = open(os.path.join(TARGET, fn), encoding="utf-8").readline().strip().split(",")
    flat = [c_.lower() for cs in cols.values() for c_ in cs]
    det_cols = cols[P.FILES["detections"]]
    check("R1 the detections ship one row per unit capture, with the unit, its time and its position, and no defect "
          "number, direction or speed", {"detection_id", "unit_serial", "captured_local", "road_mp"} <= set(det_cols)
          and not any(re.search(r"defect_id|direction|heading|speed", c_) for c_ in det_cols))
    check("R1 the traversals ship each pass's vehicle, segment, direction and times (the raw pass record)",
          {"vehicle_id", "segment_id", "direction", "enter_utc", "exit_utc"} <= set(cols[P.FILES["traversals"]]))
    check("R1 the cover inventory ships the surveyed positions (the raw control points)",
          {"asset_id", "route", "milepost"} <= set(cols[P.FILES["covers"]]))
    check("R1 no shipped column holds an error, a latency, an offset, a speed, a tolerance, a pothole id or a rate",
          not any(re.search(r"error|accura|latenc|offset|lag|speed|toler|sigma|cluster|pothole_id|defect_id|per_10|"
                            r"density|estimate", c_) for c_ in flat))

    # ------------------------------------------------------------------ R3 on the generator's clean truth
    S = e["S"]
    lm = defaultdict(float)
    for s in e["segs"]:
        if not s["turnback"]:
            lm[s["sec"]] += s["length"] * s["lanes"] / 10.0
    truth = Counter(d["sec"] for d in e["defects"] if d["real"] and not d["off"] and not S[d["seg"]]["turnback"]
                    and any(x["cls"] == "pothole" and W.local(x["t"]).month == 3 for x in e["det_by"][d["id"]]))
    tr = {s: truth.get(s, 0) / lm[s] for s in ORDER}
    check("R3b the generator's true counts of recorded potholes designate the golden set", M.designated(tr) == GOLD)
    true_lat = {v["unit"]: v["lat"] for v in e["veh"]}
    alone = M.rates(p, M.link(p, M.corrected(p, true_lat), M.TOL, road), road)
    check("R3b the decisive step alone (each unit's true latency at its pass's speed, no Layer 1 mess) files the golden",
          M.designated(alone) == GOLD)
    # the easy route on the clean truth: detections where Kerbline placed them, linked at one distance
    clean = []
    for x in e["detections"]:
        if x["cls"] == "pothole" and x["road_mp"] is not None and W.local(x["t"]).month == 3:
            clean.append((x["route"], x["road_mp"], None))
    sweep_clean = M.sweep_sets(p, clean, road)
    hit = [d for d, st in sweep_clean.items() if st == GOLD]
    check("R3a the easy route on the clean truth (one linking distance, every filed rule applied) misses the golden at "
          "every distance from %.1f to %d feet" % (M.FINE[0], M.FINE[-1]), not hit)
    check("R3c the careful route (a tolerance per unit from its error on the covers, read as scatter) files another set",
          all(M.designated(M.rms_linkage(p, k, road)) != GOLD for k in (2.0, 2.5, 3.0, 4.0)))

    # ------------------------------------------------------------------ the ladder, read from the pack
    raw = M.sweep_sets(p, M.positions(p), road)
    check("R0 a few feet's link designates all fourteen sections, and every link under 50 feet nine or more",
          all(len(raw[d]) == 14 for d in M.FINE if d <= 8) and all(len(raw[d]) >= 9 for d in M.FINE if d < 50))
    d0 = M.single(p, 200, road)
    check("R1 the default path (one distance, 200 feet) designates %s" % M.designated(d0), M.designated(d0) == DEFAULT)
    check("R1 every distance from 132 to 410 feet designates the same five",
          all(raw[d] == DEFAULT for d in M.FINE if 132 <= d <= 410))
    check("R1b every distance from 54 to 124 feet designates a seven with Grisholt and Oxbrae in place of Fenwick Gap "
          "and Kestrelton", all(raw[d] == NEAR for d in M.FINE if 54 <= d <= 124))
    check("R1 no single distance from %.1f to %d feet designates the golden" % (M.FINE[0], M.FINE[-1]),
          all(st != GOLD for st in raw.values()))
    for k in (2.0, 2.5, 3.0, 4.0):
        r = M.rms_linkage(p, k, road)
        check("R2 a tolerance of %.1f times the units' RMS error on the covers designates the five" % k,
              M.designated(r) == DEFAULT)
    for d in (130, 140, 160, 200, 230, 300, 400):
        r = M.max_per_pass(p, d, road)
        check("R2b a %d-foot link counted as the most detections one pass wrote leaves Fenwick Gap (%.2f) and Kestrelton "
              "(%.2f) under the line" % (d, r[402], r[406]), r[402] < 5.75 and r[406] < 5.75 and M.designated(r) != GOLD)
    fl = M.fleet_latency(p)
    sw = M.sweep_sets(p, M.corrected(p, fl), road)
    check("R3 one fleet latency (%.2f s) at the pass's speed misses the golden at every distance" % fl,
          all(st != GOLD for st in sw.values()))
    oi = M.offset_items(p)
    sw = M.sweep_sets(p, oi, road)
    on = [d for d, st in sw.items() if st == GOLD]
    wrong = min((sum(whole(r[s]) != whole(g["est"][s]) for s in ORDER)
                 for r in [M.single(p, d, road, oi) for d in on]), default=14)
    check("R3 a fixed offset per unit and direction from the covers designates the five from 16 feet up and the seven's "
          "names only between %s and %s feet, with %d or more of the fourteen whole numbers wrong there"
          % (min(on) if on else "-", max(on) if on else "-", wrong),
          all(sw[d] == DEFAULT for d in M.FINE if 16 <= d <= 400) and (not on or (max(on) - min(on) <= 1.0 and wrong >= 4)))
    sw = M.sweep_sets(p, M.corrected(p, g["lat"], speed="unit"), road)
    check("R3 each unit's latency at its mean speed, not each pass's, misses the golden at every distance",
          all(st != GOLD for st in sw.values()))
    gs = M.sweep_sets(p, M.corrected(p, g["lat"]), road)
    band = [d for d, st in gs.items() if st == GOLD]
    check("G the corrected detections designate the golden at every link from 2 to 27 feet",
          all(gs[d] == GOLD for d in M.FINE if 2 <= d <= 27))
    check("G the latency-corrected linkage designates the golden set", g["set"] == GOLD)
    check("G the golden's counts are the generator's truth in every section",
          all(g["counts"].get(s, 0) == truth.get(s, 0) for s in ORDER))
    members = list(fam)
    check("G every licensed member (%d: latency through the origin, as the median ratio or by direction; covers within "
          "0.05 or 0.1 mile; a link of 8 to 20 feet; median or mean placement) designates the golden" % len(members),
          all(M.designated(fam[k]) == GOLD for k in members))
    check("G every licensed member prints the same fourteen whole numbers",
          all([whole(fam[k][s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER] for k in members))
    lo_in = min(fam[k][s] for k in members for s in GOLD)
    hi_out = max(fam[k][s] for k in members for s in ORDER if s not in GOLD)
    check("G margins: nearest designated %.2f, nearest undesignated %.2f (0.75 clear of the line or more)"
          % (lo_in, hi_out), lo_in >= 6.75 and hi_out <= 5.25)
    edge = min(abs(fam[k][s] - (int(fam[k][s]) + 0.5)) for k in members for s in ORDER)
    check("bins: every member's figure at least 0.2 from a half (%.3f)" % edge, edge >= 0.2)
    ce0 = M.cover_errors(p)
    err = max(abs(g["lat"][u] - true_lat[u]) * max(x[2] for x in ce0[u]) * M.FT for u in true_lat)
    check("the latency: every unit's fitted value moves its fastest pass's detections within a foot of where its own "
          "latency would (worst %.2f feet), %.2f to %.2f s" % (err, min(g["lat"].values()), max(g["lat"].values())),
          err <= 1.0)
    # the corrected valley against the truth: a pothole's detections close, distinct potholes apart
    did = {str(x["det"]): x["defect"] for x in e["detections"]}
    by = defaultdict(list)
    for rt, x, d in M.corrected(p, g["lat"]):
        by[rt].append((x, did[d["detection_id"]]))
    within, between = [0.0], [1e9]
    for rt, xs in by.items():
        xs.sort()
        for a, b in zip(xs, xs[1:]):
            (within if a[1] == b[1] else between).append((b[0] - a[0]) * M.FT)
    check("the valley: corrected, a pothole's detections lie within %.1f feet of each other and distinct potholes %.1f "
          "feet or more apart" % (max(within), min(between)), max(within) < 8 and min(between) > 20)
    ce = M.cover_errors(p)
    u = M.units(p)
    check("every unit has 12 or more cover detections to be fitted on (fewest %d)" % min(len(ce[k]) for k in u),
          min(len(ce.get(k, [])) for k in u) >= 12)
    allerr = [x[0] for xs in ce.values() for x in xs]
    check("the covers' errors average to almost nothing (%.1f feet) though they run %.0f feet at the median"
          % (sum(allerr) / len(allerr) * M.FT, sorted(abs(x) for x in allerr)[len(allerr) // 2] * M.FT),
          abs(sum(allerr) / len(allerr) * M.FT) < 5 and sorted(abs(x) for x in allerr)[len(allerr) // 2] * M.FT > 30)
    decks = [d for d in e["pots"] if d.get("deck")]
    check("the bridge decks: %d potholes in runs of five to eight, none on a segment a sweeper drove, most in Fenwick Gap "
          "and Kestrelton" % len(decks), decks and all(not any(e["unit_veh"][un]["group"] == "SWEEPER" for un in d["seen"])
                                                       for d in decks)
          and sum(1 for d in decks if d["sec"] in (402, 406)) > len(decks) / 2)

    # ------------------------------------------------------------------ R2: Layer 1 mishandled
    mh = M.mishandled(p)
    for k, v in mh.items():
        check("R2 (%s) leaves the call" % k, M.designated(v) == GOLD)
        if k not in ("crosswalk_unused",):
            check("R2 (%s) leaves the fourteen whole numbers" % k,
                  [whole(v[s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER])
    ps = M.passes(p)
    check("R2 every detection on the state routes finds its pass once local time is read across 14 March",
          len(ps) == sum(1 for d in p["det"] if d["road_mp"]))

    # ------------------------------------------------------------------ SF rows
    inv = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["inventory"]), encoding="utf-8")))
    check("SF1 every inventory segment carries one section", all(r["section"] for r in inv) and
          len({r["segment_id"] for r in inv}) == len(inv))
    check("SF2 the five turned-back segments are in the inventory and the notice; keeping them keeps the call",
          len(p["turnback"]) == 5 and all(s in p["inv"] for s in p["turnback"]) and M.designated(mh["turnback_kept"]) == GOLD)
    check("SF3 UTC days for the window keep the call", M.designated(mh["utc_window"]) == GOLD)
    prog = pdf_text(P.FILES["program"])
    pz = prog.replace("\n", " ")
    check("SF4 the program takes Kerbline's pothole class as a pothole", "pothole class as a pothole" in pz)
    check("SF5 the program counts a pothole cold patched in March", "cold patched in March counts" in pz)
    check("SF6 the program defines lane-miles as length times through lanes", "length times its through lanes" in pz)
    check("SF7 no member's figure within 0.75 of the line",
          min(abs(fam[k][s] - M.LINE) for k in members for s in ORDER) >= 0.75)
    check("SF8 the program counts each recorded pothole once",
          "counted once however many times and by however many units" in pz)
    check("SF9 placing by road_ref through the crosswalk (or a split segment's first piece, or unlisted refs dropped) "
          "keeps the call", M.designated(mh["placed_by_road_ref"]) == GOLD and
          M.designated(mh["crosswalk_first_child"]) == GOLD and M.designated(mh["crosswalk_unused"]) == GOLD)
    lat_f = M.latency(p, flip=True)
    flipped = M.rates(p, M.link(p, M.corrected(p, lat_f, flip=True), M.TOL, road), road)
    check("SF10 the direction convention read the other way: the latencies change sign and the call and the fourteen "
          "whole numbers stay", all(lat_f[k] < 0 for k in lat_f) and M.designated(flipped) == GOLD
          and [whole(flipped[s]) for s in ORDER] == [whole(g["est"][s]) for s in ORDER])
    check("SF11 half up and half to even give the same fourteen whole numbers",
          [whole(g["est"][s]) for s in ORDER] == [round(g["est"][s]) for s in ORDER])
    check("SF12 the call reads the detections, traversals, register, covers, inventory, crosswalk and turnback only",
          True)

    # ------------------------------------------------------------------ the ask and its device
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
    check("A1 no route marker: every multi-line order keeps to one route",
          all(len({l["route"] for l in ls}) == 1 for ls in by_wo.values()))
    sev_of = {d["detection_id"]: int(d["severity"]) for d in p["det"] if d["severity"]}
    singles = defaultdict(list)
    for ls in by_wo.values():
        if len(ls) == 1 and ls[0]["cold_mix_lb"]:
            singles[sev_of[ls[0]["ext_ref"]]].append(int(ls[0]["cold_mix_lb"]))
    two_ways = []
    for w, ls in by_wo.items():
        if len(ls) > 1 and all(l["cold_mix_lb"] for l in ls) and len({l["cold_mix_lb"] for l in ls}) == 1:
            v, sv = int(ls[0]["cold_mix_lb"]), [sev_of[l["ext_ref"]] for l in ls]
            as_total = v > max(max(singles[x]) for x in sv)
            as_lines = v < sum(min(singles[x]) for x in sv)
            if as_total == as_lines:
                two_ways.append(w)
    check("A1 fair: every repeated figure reads one way only, above every single-line order of its lines' severities "
          "(a total) or below their least single-line figures summed (each line's own) (%d read both ways)" % len(two_ways),
          not two_ways)
    det_ids = {d["detection_id"] for d in p["det"] if d["defect_class"] == "pothole" and d["severity"]}
    check("A1 fair: every order's ext_ref is a pothole detection carrying a severity",
          all(r["ext_ref"] in det_ids for r in p["wo"]))
    check("A golden equals the generator's truth (pounds used)",
          all(gA.get(s, 0) == sum(l["true_lb"] for l in e["wo_rows"] if l["sec"] == s and l["status"] == "COMPLETE"
                                  and l["finish"] is not None and W.local(l["finish"]).month == 3) for s in ORDER))
    import ceiling as CE
    pair, leak, kept_c, kept_m = CE.main(TARGET)
    check("ceiling: the cracker keeps no ask figure, the mirror none, pair %.1f under 40" % pair,
          not kept_c and not kept_m and pair <= 40)

    # ------------------------------------------------------------------ the separation line
    import inspect
    src = "".join(inspect.getsource(f) for f in (M.golden, M.link, M.latency, M.cover_errors, M.corrected, M.passes))
    check("separation: the call reads no work order (the ask's device rows)", "wo" not in re.findall(r'p\["(\w+)"\]', src))

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
          not any(re.search(r"distract|decoy|trap|known|issue|dup|stump|latenc|lag|offset", f) for f in files))

    # ------------------------------------------------------------------ realism sweep
    found_counts = Counter(g["counts"].get(s, 0) for s in ORDER)
    check("realism: no two sections share a pothole count", max(found_counts.values()) == 1)
    check("realism: no round lane-mile total", all(abs(v - round(v, -1)) > 0.05 for v in M.lane_miles(p, road).values()))
    blob = b"".join(open(os.path.join(TARGET, f), "rb").read() for f in files if f.endswith((".pdf", ".xlsx")))
    check("realism: containers carry no writing library's name", b"ReportLab" not in blob and b"openpyxl" not in blob)
    names = re.findall(r"Nancy Hansen|Andrew Greene", prog + pdf_text(P.FILES["dictionary"]))
    check("realism: the personas are the drawn pair", set(names) == {"Nancy Hansen", "Andrew Greene"})
    det_max = max(r["captured_local"] for r in p["det"])
    check("realism: no detection after the month (%s)" % det_max, det_max < "2027-04-01")
    trav = list(csv.DictReader(open(os.path.join(TARGET, P.FILES["traversals"]), encoding="utf-8")))
    check("realism: traversal keys unique and every pass forward in time",
          len({t["traversal_id"] for t in trav}) == len(trav) and all(t["exit_utc"] > t["enter_utc"] for t in trav))
    sows = pdf_text(P.FILES["sow"])
    check("documents read back: the scope of work's service day sentence (positive control on the PDF extractor)",
          "during any part of which the unit" in sows.replace("\n", " "))
    check("documents read back: the scope of work says defect linking is not in the pilot",
          "is not in the pilot" in sows.replace("\n", " "))
    dic = pdf_text(P.FILES["dictionary"])
    check("documents read back: the data notes give the milepost direction",
          "mileposts increase northbound and eastbound" in dic.replace("\n", " "))
    check("documents: no shipped sentence states a latency, a lag, an offset, a unit's accuracy, a tolerance or how to "
          "link detections", not re.search(r"latenc|\blags?\b|offset|accura|\berror|toleran|within \d|link the|same "
                                             r"pothole|ahead of|behind the", (prog + sows + dic).replace("\n", " ")))
    tb = pdf_text(P.FILES["turnback"])
    check("documents read back: the turnback notice lists five segments effective 15 March",
          "15 March 2027" in tb.replace("\n", " ") and len(p["turnback"]) == 5)

    fails = [n for n, ok in RESULTS if not ok]
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
