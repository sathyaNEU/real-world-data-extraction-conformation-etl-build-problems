"""task248 generator checks: run against a built target/ (and the simulated clean truth). Exit 1 on any FAIL."""
import os, sys, re, csv, json, datetime as dt
import numpy as np
import params as P
import world as W
import analysis as A
import verify as V
import ceiling as C

RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def main(target, golden_dir=None, meta_path=None):
    res, pk = A.analyse(target)
    T = res["tanks"]
    GOLD = ["BP-2", "CF-2", "DH-1", "FL-1", "GC-1", "HS-2"]
    files = sorted(os.listdir(target))
    # ---------------- input gates ----------------
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, {f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith((".csv", ".jsonl")))
    ok("gate: a file of 25,000 rows or more", big >= 25000, big)
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok("gate: two or more distractors declared", len(meta.get("distractor_files", [])) >= 2, meta.get("distractor_files"))
    banned = re.compile(r"readme|dictionary|manifest|notes|field_guide|schema|decoy|trap|test_|answer|stump", re.I)
    ok("gate: no file describes the data or names the author's intent", not [f for f in files if banned.search(f)], files)
    # ---------------- R1 to R3c: the three rules ----------------
    hdrs = []
    for f in files:
        if f.endswith(".csv"):
            hdrs += next(csv.reader(open(os.path.join(target, f), encoding="utf-8")))
    ok("R1 the raw material ships: gauge readings, dock sales and bills of lading read by the golden", T["BP-2"]["n_intervals"] > 1000 and T["CF-2"]["n_deliveries"] >= 4)
    ok("R1 no shipped column holds a chart error, offset or misstatement", not [h for h in hdrs if re.search(r"error|offset|misstat|bias|correction", h, re.I)], hdrs)
    o = W.simulate()
    def truth_parts(tid):
        t = o["tanks"][tid]
        c = lambda h: t.chart_gal(h) - float(W.vol(h - t.delta, t.D, t.Lt))
        return (c(t.half_h) - c(t.reorder_h), c(t.fill_h) - c(t.half_h), c(t.fill_h) - c(t.reorder_h))
    true_list = sorted(t for t in P.TANKS if max(abs(x) for x in truth_parts(t)) > P.LIMIT_GAL)
    ok("R3 clean truth: the true chart errors list the golden six", true_list == GOLD, true_list)
    # analyst test on the clean truth: deliveries' true discrepancies carried over the working range
    r1_clean = []
    for tid in P.TANKS:
        t = o["tanks"][tid]
        c = lambda h: t.chart_gal(h) - float(W.vol(h - t.delta, t.D, t.Lt))
        ds = [d for d in o["deliveries"] if d["tank"] == tid and dt.datetime(2026, 4, 1) <= d["start"] < dt.datetime(2026, 11, 1)]
        tot = sum(c(d["h1"]) - c(d["h0"]) for d in ds); vol_ = sum(t.chart_gal(d["h1"]) - t.chart_gal(d["h0"]) for d in ds)
        eps = tot / vol_ if vol_ else 0
        if abs(eps * (t.chart_gal(t.fill_h) - t.chart_gal(t.reorder_h))) > P.LIMIT_GAL:
            r1_clean.append(tid)
    ok("R3a analyst test: the delivery check on the clean truth files CF-2 and GC-1, not the golden", sorted(r1_clean) == ["CF-2", "GC-1"], r1_clean)
    ok("R3a the monthly reconciliation passes every tank", res["R0_list"] == [], res["R0_list"])
    ok("R3b the decisive step alone (anchoring the intervals on the deliveries) files the golden", res["golden_list"] == GOLD, res["golden_list"])
    ok("R3b the lower rung's single correction (intervals unanchored) leaves a wrong list", res["R2_list"] != GOLD and len(res["R2_list"]) == 10, res["R2_list"])
    ok("R3b the mixed rung (delivery full range, unanchored halves) leaves a wrong list", res["R2p_list"] != GOLD and set(res["R2p_list"]) - set(GOLD) == {"DH-2", "EB-1"}, res["R2p_list"])
    seqs = {}
    for r in csv.DictReader(open(os.path.join(target, "atg_inventory_2026.csv"), encoding="utf-8")):
        seqs.setdefault((r["console_sn"], r["tank"]), []).append(r["tc_gal_60f"])
    dup_block = False
    for k, s in seqs.items():
        seen = set()
        for i in range(0, len(s) - 24, 12):
            blk = tuple(s[i:i + 24])
            if len(set(blk)) > 3 and blk in seen:
                dup_block = True
            seen.add(blk)
    ok("R3c no plant: no copied block of 24 readings in any tank's series", not dup_block)
    docs_txt = V.pdf_text(os.path.join(target, "FS-3_fuel_systems_standard.pdf")) + V.pdf_text(os.path.join(target, "wetstock_onboarding_2027.pdf"))
    ok("R3c no plant: no document ranks the tanks or names a tank to re-chart", not re.search(r"\b(AH|BP|CF|DH|EB|FL|GC|HS)-\d\b", docs_txt))
    # ---------------- semantic forks SF1 to SF10 ----------------
    ok("SF1 no strapping or alternative tank geometry ships; the golden reads misstatement against gallons moved", "tank_strapping" not in " ".join(files))
    reg_h = {t: (pk.reg[t]["re"], pk.reg[t]["half"], pk.reg[t]["fill"]) for t in pk.reg}
    ok("SF2 the three heights are the register's (reorder, half-full, normal fill)", all(reg_h[t] == (o["tanks"][t].reorder_h, o["tanks"][t].half_h, o["tanks"][t].fill_h) for t in pk.reg))
    inv = pk.inventory(); dls = pk.deliveries(); bls = pk.bols(); sales = pk.sales_legacy()
    def golden_under(season=True, gross=False, no_dlv_sales=False, half_shift=0.0):
        out = []
        for tid in pk.reg:
            iv, dl = A.build_obs(pk, tid, inv, dls, bls, sales, season=season)
            if gross:
                k = A.K[pk.reg[tid]["product"]]
                iv = (iv[0], iv[1], iv[2], iv[3])
            if no_dlv_sales:
                dl = (dl[0], dl[1], dl[2], dl[3])
            g = pk.reg[tid]
            if half_shift:
                saved = g["half"]; g["half"] = saved + half_shift
            parts, _ = A.fit_hat(pk, tid, iv, dl)
            if half_shift:
                g["half"] = saved
            if max(abs(x) for x in parts) > A.LIMIT:
                out.append(tid)
        return sorted(out)
    saved = A.SEASON
    A.SEASON = (dt.datetime(2026, 3, 1), dt.datetime(2026, 11, 16))
    wide = golden_under()
    A.SEASON = saved
    ok("SF3 the whole legacy-covered boating year (1 March to 15 November) files the same list as the season", wide == GOLD, wide)
    # SF4: gross against net. The intervals' gross change against gross sales:
    gross_list = []
    for tid in pk.reg:
        rows = [r for r in inv.get(tid, []) if A.SEASON[0] <= r[0] < A.SEASON[1]]
        gross_inv = {tid: [(r[0], r[1], r[2], r[3], r[4], r[4], r[6]) for r in rows]}
        iv, dl = A.build_obs(pk, tid, gross_inv, dls, bls, sales)
        parts, _ = A.fit_hat(pk, tid, iv, dl)
        if max(abs(x) for x in parts) > A.LIMIT:
            gross_list.append(tid)
    ok("SF4 gross gallons throughout file the same list as net", sorted(gross_list) == GOLD, gross_list)
    ok("SF5 the gauge export and the dock sales share one local clock (no conversion on the call's path)", "reading_time" in hdrs and "sale_time" in hdrs)
    nodl = []
    for tid in pk.reg:
        iv, dl = A.build_obs(pk, tid, inv, dls, bls, {k: v for k, v in sales.items()})
        # rebuild the delivery checks without the sales during each delivery
        D = [d for d in dls.get(tid, []) if A.SEASON[0] <= d["start"] < A.SEASON[1]]
        y = []
        for d in D:
            cand = [b for b in bls.get(tid, []) if d["start"] - dt.timedelta(hours=3) <= b["t"] <= d["start"] + dt.timedelta(minutes=30)]
            if cand:
                y.append((d["h0"], d["h1"], d["n1"] - d["n0"] - cand[0]["net"], cand[0]["net"]))
        dl2 = tuple(np.array([x[i] for x in y]) for i in range(4))
        parts, _ = A.fit_hat(pk, tid, iv, dl2)
        if max(abs(x) for x in parts) > A.LIMIT:
            nodl.append(tid)
    ok("SF6 leaving out the dock sales during a delivery files the same list", sorted(nodl) == GOLD, nodl)
    pipe_keys = list(pk.piping)
    ok("SF7 the piping record is one row per hose (no re-piping inside the season)", len(pipe_keys) == len(set(pipe_keys)))
    signed = sorted(t for t in T if max(T[t]["gold"]) > A.LIMIT)
    ok("SF8 the size reading is filed (FS-3: by more than 25 gallons): a signed reading would drop GC-1", "GC-1" not in signed and res["golden_list"] == GOLD, signed)
    a3 = res["A3"]
    # dock gallons are exact sums of registered gallons with no fitted parameter: every handling that takes the
    # devices right sums the same rows, so the figure is the same to the unit; assert no float knife-edge
    ok("SF9 every dock-gallon figure an exact sum clear of its rounding edge by more than 0.005 gallon", all(abs(v - round(v)) < 0.495 for v in a3.values()), min(0.5 - abs(v - round(v)) for v in a3.values()))
    fam = ["v_hat6", "v_dlvpts", "v_geom_exact", "v_geom_first", "v_cycles"]
    ok("SF10 every anchored construction files the golden list", all(res[v + "_list"] == GOLD for v in fam), {v: res[v + "_list"] for v in fam})
    pairs_same = all(A.largest(T[t][v])[1] == T[t]["gold_pair"] for t in GOLD for v in fam)
    ok("SF10 every anchored construction names the same heights for each listed tank", pairs_same)
    # ---------------- rung margins ----------------
    lmin = min(min(np.nanmax(np.abs(T[t][v])) for v in fam + ["gold"]) for t in GOLD)
    umax = max(max(np.nanmax(np.abs(T[t][v])) for v in fam + ["gold"]) for t in T if t not in GOLD)
    ok("margin: every listed tank 12 gallons or more over the limit under every anchored construction", lmin >= 37, round(lmin, 1))
    ok("margin: every unlisted tank 8 gallons or more under the limit under every anchored construction", umax <= 17, round(umax, 1))
    r1_out = max(T[t]["R1"] for t in T if t not in ("CF-2", "GC-1")); r1_in = min(T[t]["R1"] for t in ("CF-2", "GC-1"))
    ok("margin: the delivery check's two tanks clear 25 by 15 and the rest stay under 17", r1_in >= 40 and r1_out <= 17, (round(r1_in, 1), round(r1_out, 1)))
    r1b_out = max(T[t]["R1_per_delivery"] for t in T if t not in ("CF-2", "GC-1"))
    ok("margin: the per-delivery form of the check files the same two", res["R1b_list"] == ["CF-2", "GC-1"] and r1b_out <= 19.5, round(r1b_out, 1))
    r2_edge = min(abs(T[t]["R2_largest"] - 25) for t in T)
    ok("margin: every tank 4 gallons or more from the limit on the unanchored intervals", r2_edge >= 4, round(r2_edge, 1))
    r2p_edge = min(abs(T[t]["R2p_largest"] - 25) for t in T)
    ok("margin: every tank 4 gallons or more from the limit on the mixed rung", r2p_edge >= 4, round(r2p_edge, 1))
    ratio = min(sorted(np.abs(T[t]["gold"]))[-1] / sorted(np.abs(T[t]["gold"]))[-2] for t in GOLD)
    ok("margin: each listed tank's largest misstatement 1.25 times its next", ratio >= 1.25, round(ratio, 2))
    # ---------------- mess neutrality (Layer 1, the call's path) ----------------
    cur = []
    for tid in pk.reg:
        iv, dl = A.build_obs(pk, tid, inv, dls, bls, sales)
        parts, _ = A.fit_hat(pk, tid, iv, dl)
        if max(abs(x) for x in parts) > A.LIMIT:
            cur.append(tid)
    ok("R2 mess: the console tank numbering applied by the current setup leaves the season's list unchanged", sorted(cur) == GOLD)
    ok("R2 mess: delivery-report endpoints taken as readings leave the list unchanged", res["v_dlvpts_list"] == GOLD)
    ok("R2 mess: the September network outage leaves every tank with 1,500 or more season intervals", min(T[t]["n_intervals"] for t in T) >= 1500, min(T[t]["n_intervals"] for t in T))
    raw = list(csv.DictReader(open(os.path.join(target, "atg_inventory_2026.csv"), encoding="utf-8")))
    season_2016 = sum(1 for r in raw if r["reading_time"].startswith("2016") and False)
    reset_in_season = [r for r in raw if r["reading_time"].startswith("2016")]
    ok("separation: every storm-reset row is a January console stamp (outside the season)", all(r["reading_time"] < "2016-01-12" for r in reset_in_season) and len(reset_in_season) > 100)
    newpos = [json.loads(l) for l in open(os.path.join(target, "dock_sales_2026-11-09_2026-12-31.jsonl"), encoding="utf-8")]
    ok("separation: the new point of sale holds no season rows", min(A.loc(j["ts"]) for j in newpos) >= dt.datetime(2026, 11, 1))
    ok("separation: the leak-test log is read by no step of the call", "atg_leak_tests" not in open(os.path.join(os.path.dirname(__file__), "analysis.py")).read().split("def ask_tests")[0])
    # ---------------- the asks ----------------
    st = res["stops"]
    mv = lambda a, b: sum(1 for k in a if a[k] != b.get(k))
    ok("A1 device: dropping the storm-reset rows moves 10 or more tanks", mv(res["A1"], st["A1_drop_reset"]) >= 10, mv(res["A1"], st["A1_drop_reset"]))
    ok("A1 device: Dellwood keyed by its current numbering moves both its tanks", st["A1_current_setup"]["DH-1"] != res["A1"]["DH-1"] and st["A1_current_setup"]["DH-2"] != res["A1"]["DH-2"])
    ok("A2 device: counting every logged pass moves 4 or more marinas", mv(res["A2"], st["A2_every_row"]) >= 4, mv(res["A2"], st["A2_every_row"]))
    ok("A2 device: dating each test by its first logged row moves at least one marina", mv(res["A2"], st["A2_no_redate"]) >= 1)
    r3 = lambda d: {k: round(v) for k, v in d.items()}
    g3 = r3(res["A3"])
    ok("A3 device: keeping both exports moves 12 or more cells", mv(g3, r3(st["A3_both"])) >= 12, mv(g3, r3(st["A3_both"])))
    ok("A3 device: reading card settlement stamps as sale times moves 10 or more cells", mv(g3, r3(st["A3_stamp_dates"])) >= 10, mv(g3, r3(st["A3_stamp_dates"])))
    ok("A3 device: the grade table as published moves the four cells of the two winter marinas", mv(g3, r3(st["A3_grade_table"])) == 4)
    # world truth for the asks
    year = {dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)}
    tA1 = {t: len(year - {r["local"].date() for r in o["readings_kept"] if r["tank"] == t}) for t in P.TANKS}
    ok("A1 golden equals the world's own missing days", tA1 == res["A1"], {t: (tA1[t], res["A1"][t]) for t in tA1 if tA1[t] != res["A1"][t]})
    tA3 = {}
    for s in o["sales"]:
        key = "%s|%s" % (P.MARINAS[s["marina"]][0], P.PRODUCTS[s["product"]])
        tA3[key] = tA3.get(key, 0.0) + round(s["gal_reg"], 2 if s["local"] < P.POS_GOLIVE else 3)
    ok("A3 golden equals the world's registered gallons (to the gallon)", all(abs(tA3[k] - res["A3"].get(k, 0)) < 0.6 for k in tA3), max(abs(tA3[k] - res["A3"].get(k, 0)) for k in tA3))
    passes = {}
    for x in o["tests"]:
        if x["result"] == "PASS":
            passes.setdefault(x["tank"], set()).add(x["start"].month)
    exported_nos = {(x["tank"], x["test_no"]) for x in o["tests_exported"]}
    passes_known = {}
    for x in o["tests"]:
        if x["result"] == "PASS" and (x["tank"], x["test_no"]) in exported_nos:
            passes_known.setdefault(x["tank"], set()).add(x["start"].month)
    tA2 = {}
    for t, v in P.TANKS.items():
        nm = P.MARINAS[v[0]][0]
        tA2[nm] = tA2.get(nm, 0) + sum(1 for mo in range(1, 13) if mo not in passes_known.get(t, set()))
    ok("A2 golden equals the world's tank-months without a recorded passing test", tA2 == res["A2"], (tA2, res["A2"]))
    # ---------------- ceiling ----------------
    cl = C.run(target, verbose=False)
    ok("ceiling: pair at or under 60", cl["pair_ceiling"] <= 60, round(cl["pair_ceiling"], 1))
    ok("ceiling: mirror leakage under 50 per cent", cl["mirror_leakage_pct"] < 50, round(cl["mirror_leakage_pct"], 1))
    ok("ceiling: the cracker misses every ask", cl["cracker_misses_every_ask"], cl["cracker"]["per_ask_kept"])
    # ---------------- realism sweep ----------------
    bols_ = list(csv.DictReader(open(os.path.join(target, "bols_2026.csv"), encoding="utf-8")))
    steps = np.diff(sorted(int(b["bol_no"][2:]) for b in bols_))
    ok("realism: bill of lading numbers have no constant step", len(set(steps.tolist())) > 5)
    sites = sorted(int(s["site_id"][1:]) for s in pk.setup)
    ok("realism: site ids are not an arithmetic sequence", len(set(np.diff(sorted(set(sites))).tolist())) > 2)
    names = {re.sub(r"^\w+\s", "", P.MARINAS[m][0]) for m in P.MARINAS}
    ok("realism: marina names take more than two shapes", len({n.split()[-1] for n in names}) > 2, names)
    ok("realism: no dock-gallon figure is a round thousand", not any(round(v) % 1000 == 0 for v in res["A3"].values()))
    ok("realism: no two tanks share identical missing-day and test-gap profiles in every ask", len(set(res["A1"].values())) >= 5)
    ok("realism: personas in the documents are the card's", "Miranda Collins" in docs_txt and "Theresa Shelton" in docs_txt)
    ok("realism: documents dated before the export (FS-3 14 Sep 2026, letter 3 Dec 2026)", "14 September 2026" in docs_txt and "3 December 2026" in docs_txt)
    # positive controls before absence checks
    ctrl = V.pdf_text(os.path.join(target, "FS-3_fuel_systems_standard.pdf"))
    ok("control: FS-3 text extracted through the verifier's reader (3.4 present)", "re-charted by the calibration contractor" in ctrl and len(ctrl) > 1500, len(ctrl))
    ok("absence: FS-3 names no estimator, interval, meter error or delivery anchor", not re.search(r"interval|meter error|anchor|regress|shape|tilt|offset", ctrl, re.I))
    lt_ = V.pdf_text(os.path.join(target, "wetstock_onboarding_2027.pdf"))
    ok("control: onboarding letter extracted (readiness sentence present)", "local calendar day" in lt_)
    ok("absence: the letter names no tank and no method", not re.search(r"\b[A-Z]{2}-\d\b|interval|deliver(y|ies) check|meter", lt_))
    # ---------------- distractors ----------------
    src = open(os.path.join(os.path.dirname(__file__), "analysis.py")).read() + open(os.path.join(os.path.dirname(__file__), "verify.py")).read()
    ok("distractor: lake levels unread by the golden or the verifier", "lake_levels" not in src)
    ok("distractor: monthly close-outs unread by the golden", "monthly_closeouts" not in open(os.path.join(os.path.dirname(__file__), "analysis.py")).read())
    if golden_dir:
        gl = list(csv.DictReader(open(os.path.join(golden_dir, "recharting_list_2027.csv"), encoding="utf-8")))
        ok("golden: the list file carries the six tanks and their heights", [r["tank"] for r in gl] == GOLD and all(r["misstates_most_between"] == T[r["tank"]]["gold_pair"] for r in gl))
        gp = V.pdf_text(os.path.join(golden_dir, "cutover_readiness_2027.pdf"))
        ok("golden: the PDF states the number and names each tank", "6 tanks" in gp and all(t in gp for t in GOLD))
    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print(("PASS " if good else "FAIL ") + label + ("" if good else "  [%s]" % (detail,)))
    print("checks: %d assertions, %d failed" % (len(RES), len(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target")
    gd = sys.argv[2] if len(sys.argv) > 2 else None
    mp = sys.argv[3] if len(sys.argv) > 3 else None
    sys.exit(main(tgt, gd, mp))
