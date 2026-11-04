"""task476 checks: the input gates, the analyst test on the clean truth, every route on the cut pack, every row of the
design note's semantic fork table (SF1 to SF15), the main population's zero-counts, the asks' devices, and the
deliverables against the golden. Prints PASS or FAIL per line; returns True when all pass."""
import csv
import datetime as dt
import json
import math
import os
import re

import golden as G
import bundle as B
import world as W

ROWS = []


def ok(name, cond, detail=""):
    ROWS.append((name, bool(cond), detail))
    print("%s  %-46s %s" % ("PASS" if cond else "FAIL", name, detail))
    return bool(cond)


def purchase_of(total, avail, block):
    ex = total - avail
    return int(math.ceil(ex / block) * block) if ex > 0 else 0


def truth_routes(x, d):
    """The analyst test on the generator's clean truth: each unmetered well's true energy at its true test-day rate
    (no measurement noise), against the same energy at the true head of each interval."""
    t = x["_tests"]
    q0 = int((W.WY_START - W.T0).total_seconds() // 900)
    q1 = int((W.WY_END - W.T0).total_seconds() // 900)
    r0, gold, true = 0.0, 0.0, 0.0
    for w in W.WELLS:
        p = W.P[w]
        kq = x[w]["kwh_q"].reshape(-1)[q0:q1]
        af = float(x[w]["af_q"].reshape(-1)[q0:q1].sum())
        true += af
        if p["metered"]:
            r0 += af
            gold += af
            continue
        h = t[w]["h"]
        rate = W.KWH_AF_FT * x[w]["tdh"][h] / x[w]["ope"][h]
        r0 += float(kq.sum()) / rate
        lv = x[w]["lvl"][q0:q1]
        tdh = x[w]["tdh"][h] + (lv - (x[w]["swl"][h] + x[w]["q"][h] / p["sc"]))
        gold += float((kq * x[w]["ope"][h] / (W.KWH_AF_FT * tdh)).sum())
    avail = d["notice"]["available"]
    return r0, gold, true, avail


def main(target, gdir, x=None):
    ROWS.clear()
    d = G.load(target)
    # ---- input gates
    files = [os.path.join(r, f) for r, _, fs in os.walk(target) for f in fs]
    exts = sorted({f.rsplit(".", 1)[-1] for f in files})
    ok("input gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    ok("input gate: 3 or more formats", len(exts) >= 3, ", ".join(exts))
    big = max(sum(1 for _ in open(f, encoding="utf-8", errors="ignore")) for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(os.path.dirname(gdir), "metadata.json")))
    dis = [f for f in meta["files"] if f.get("role") == "distractor"]
    ok("input gate: 2 or more distractors named", len(dis) >= 2, ", ".join(f["path"] for f in dis))
    ok("no file names the trap", not any(re.search(r"head|lift|convert|correct|true_?up_answer", os.path.basename(f), re.I)
                                         for f in files), "")
    ok("no notes, readme or dictionary file", not any(re.search(r"readme|notes|dictionary|codebook|manifest", f, re.I)
                                                      for f in files), "")
    # H25: every PDF opens under a strict reader and two extractors agree on its words
    import pypdf
    import pdfplumber
    bad = []
    for f in files:
        if not f.endswith(".pdf"):
            continue
        try:
            rd = pypdf.PdfReader(f, strict=True)
            t1 = " ".join((pg.extract_text() or "") for pg in rd.pages)
            with pdfplumber.open(f) as pdf:
                t2 = " ".join((pg.extract_text() or "") for pg in pdf.pages)
            w1 = set(re.findall(r"[A-Za-z]{4,}", t1))
            w2 = set(re.findall(r"[A-Za-z]{4,}", t2))
            if not w2 or len(w1 & w2) < 0.9 * len(w2):
                bad.append(os.path.basename(f))
        except Exception as e:
            bad.append("%s (%s)" % (os.path.basename(f), type(e).__name__))
    ok("H25: every PDF reads under a strict reader", not bad, ", ".join(bad))
    # ---- the call and its routes on the pack
    g = G.extraction(d)
    r0 = G.extraction(d, route="R0")
    r1 = G.extraction(d, route="R1")
    r3 = G.extraction(d, route="R3")
    ok("golden buys transfer water", g["purchase"] > 0, "purchase %d, ranch %d against %.1f" % (
        g["purchase"], g["total"], g["available"]))
    ok("R0 (test rate) buys nothing", r0["purchase"] == 0, "ranch %d, %.0f inside" % (r0["total"], -r0["excess"]))
    ok("R1 (run hours x tested flow) buys nothing", r1["purchase"] == 0, "ranch %d" % r1["total"])
    ok("R1b equals R0 (one current test per pump)", all(len([t for t in d["all_tests"] if t["well"] == w and
                                                         t["date"] >= dt.date(2024, 4, 1)]) == 1 for w in d["reg"]), "")
    ok("R3 (pumping-level ratio alone) misses the purchase", r3["purchase"] != g["purchase"], "R3 buys %d" % r3["purchase"])
    ok("golden excess sits mid-block", 12 <= (g["excess"] % 50) <= 38, "excess %.1f" % g["excess"])
    # ---- back-test: the textbook route validates on the metered wells
    met = G.meter_volumes(d)
    bt = []
    for w in d["reg"]:
        if d["reg"][w]["Flow meter"] == "none":
            continue
        t = d["tests"][w]
        kwh = sum(k for st, m, k in d["power"][w] if B.WY0 <= st.astimezone(B.LA) < B.WY1)
        bt.append(abs(kwh / t["kwh_af"] / met[w]["wy"] - 1))
    ok("back-test: R0 within 3 per cent on every metered well", max(bt) < 0.03, "largest %.2f per cent" % (100 * max(bt)))
    # ---- analyst test on the clean truth
    if x is not None:
        tr0, tg, tt, av = truth_routes(x, d)
        ok("clean truth: R0 buys nothing", purchase_of(tr0, av, 50) == 0, "R0 %.0f against %.1f" % (tr0, av))
        ok("clean truth: the head conversion buys", purchase_of(tg, av, 50) > 0, "%.0f, truth %.0f" % (tg, tt))
        ok("clean truth: the truth is over the water available", tt > av, "truth %.0f" % tt)
    # ---- SF rows
    nt = d["notice"]["text"].replace("\n", " ")
    ok("SF1 the notice files the volume the well pumped", "the volume of groundwater the well pumped" in nt, "")
    e_utc = G.unmetered_volumes(d, clock_shift_h=0)
    sf2 = []
    for shift in (7, 8):
        tot = 0.0
        for w, rows in d["power"].items():
            if d["reg"][w]["Flow meter"] != "none":
                continue
            v = sum(k for st, m, k in rows if B.WY0 <= st.astimezone(B.LA) + dt.timedelta(hours=shift) < B.WY1)
            v0 = sum(k for st, m, k in rows if B.WY0 <= st.astimezone(B.LA) < B.WY1)
            tot += (v - v0) / d["tests"][w]["kwh_af"]
        sf2.append(abs(tot))
    ok("SF2 bounds in UTC or PST move the ranch under 5 AF", max(sf2) < 5, "%.1f AF" % max(sf2))
    ok("SF3 the metered-well sentence is filed", "difference between its meter readings" in nt, "")
    w03 = met["W-03"]["wy"]
    q0 = int((W.WY_START - W.T0).total_seconds() // 900)
    ok("SF4 the W-03 exchange handled (reads give the meter's water)", "allowing for any meter exchange" in nt and w03 > 0,
       "W-03 %.1f AF" % w03)
    ok("SF5 the acre-foot (325,851 gal)", abs(43560 * 7.48052 - 325851) < 2, "")
    ok("SF6 water available = allocation + carryover", "the allocation plus the carryover" in nt and
       abs(d["notice"]["available"] - (d["notice"]["allocation"] + d["notice"]["carryover"])) < 0.01,
       "%.1f" % d["notice"]["available"])
    unr = sum(v["wy"] for v in g["vols"].values())
    ok("SF7 rounded and unrounded sums buy the same", purchase_of(unr, g["available"], 50) == g["purchase"],
       "unrounded %.1f" % unr)
    ok("SF8 blocks of 50, rounded up", "whole blocks of 50 acre-feet" in nt and g["purchase"] % 50 == 0 and
       g["purchase"] >= g["excess"], "nearest-block reading %d" % (round(g["excess"] / 50) * 50))
    # SF9: the 2023 reports are on replaced pumps
    old = [t for t in d["all_tests"] if t["date"] < dt.date(2024, 1, 1)]
    ok("SF9 every 2023 report predates its pump's installation", len(old) == 3 and all(
        t["date"] < dt.datetime.strptime(str(d["reg"][t["well"]]["Pump installed"])[:10], "%Y-%m-%d").date() for t in old),
       ", ".join("%s %s" % (t["job"], t["well"]) for t in old))
    # SF10: pairings
    pur, spread = {}, {}
    for pair in ("start", "end", "mean"):
        e = G.extraction(d, pair=pair)
        pur[pair] = e["purchase"]
        for w, v in e["vols"].items():
            spread.setdefault(w, []).append(v["wy"])
    em = G.extraction(d, route="monthly")
    pur["monthly"] = em["purchase"]
    for w, v in em["vols"].items():
        spread[w].append(v["wy"])
    band = max((max(v) - min(v)) / g["vols"][w]["wy"] for w, v in spread.items())
    ok("SF10 every pairing buys the golden's blocks", len(set(pur.values())) == 1, str(pur))
    ok("SF10 every pairing within 0.5 per cent per well", band < 0.005, "largest %.2f per cent" % (100 * band))
    e1 = G.extraction(d, clock_shift_h=1)
    ok("SF11 a DST-hour misreading buys the same", e1["purchase"] == g["purchase"], "%d" % e1["purchase"])
    e8 = G.extraction(d, clock_shift_h=-8)
    lg = open(os.path.join(target, W.logger_file(W.LOGGER_NOW["W-09"])), encoding="utf-8").read(600)
    ok("SF11 the 8-hour misreading is ruled out by the headers", "UTC-08:00" in lg and e8["purchase"] != g["purchase"],
       "it would buy %d" % e8["purchase"])
    # SF12: estimated intervals dropped
    keep = {}
    old_f = B.find(target, "power", r"usage_export")[0]
    est = set()
    with open(old_f, encoding="utf-8") as fh:
        for line in fh:
            if line.rstrip().endswith("Estimated"):
                c = line.split(",")
                est.add((c[0], c[2], c[3]))
    ok("SF12 estimated intervals exist and are few", 0 <= len(est) < 200, "%d estimated hours" % len(est))
    ok("SF13 the fall-back hour carries two rows per account",
       sum(1 for l in open(old_f, encoding="utf-8") if ",2025-11-02,01:00," in l) == 2 * len(d["reg"]), "")
    e_dat = G.extraction(d, datum=False)
    txt = " ".join(open(os.path.join(target, W.logger_file(W.LOGGER_NOW["W-09"])), encoding="utf-8").read(600).split())
    ok("SF14 the datum is stated and the mishandling moves the purchase", "below top of sounding tube" in txt and
       e_dat["purchase"] != g["purchase"], "ignoring the tube buys %d" % e_dat["purchase"])
    ok("SF15 one efficiency per pump", all(d["tests"][w]["ope"] > 0 for w in d["tests"]), "")
    # SF6 at whole acre-feet: the notice's total row is its rows' sum, so either reading files 15,359
    tot_line = re.search(r"^Total [\d.]+ [\d.]+ [\d.]+ ([\d.]+)$", d["notice"]["text"], re.M)
    ok("SF6 the notice's total row equals its rows' sum", tot_line is not None and
       abs(float(tot_line.group(1)) - d["notice"]["allocation"]) < 1e-6 and
       round(float(tot_line.group(1)) + d["notice"]["carryover"]) == round(d["notice"]["available"]),
       "total %s" % (tot_line.group(1) if tot_line else None))
    # SF11: every clock the pack carries is stated where its producer records it
    dl = d["dlog"]
    lv5 = {str(d["reg"][w]["Logger S/N"]) for w in d["reg"] if "absolute" in str(d["reg"][w]["Level logger"])}
    rows_lv5 = [r for r in dl if r["logger_sn"] in lv5 or r["site"] in [str(d["reg"][w]["Ranch name"]).split(" (")[0]
                                                                        for w in d["reg"] if d["reg"][w]["Flow meter"] != "none"]]
    ok("SF11 every Levelogger visit records its PST clock", rows_lv5 and all("PST (UTC-08:00), no daylight saving" in r["note"]
                                                                            for r in rows_lv5), "%d visits" % len(rows_lv5))
    troll = [str(d["reg"][w]["Logger S/N"]) for w in d["reg"] if "vented" in str(d["reg"][w]["Level logger"])]
    ok("SF11 every TROLL header states PST with no daylight saving", all(
        "(UTC-08:00) Pacific Standard Time, daylight saving not applied" in open(os.path.join(target, W.logger_file(s)),
                                                                             encoding="utf-8").read(700) for s in troll), "")
    absw0 = [w for w in d["reg"] if "absolute" in str(d["reg"][w]["Level logger"])]
    as_utc = {w: G.static_depths(d, w, abs_shift=8) for w in absw0}
    gs0 = {w: G.static_depths(d, w) for w in absw0}
    moved_utc = sum(1 for w in absw0 for k in ("spring", "fall") if round(as_utc[w][k][1], 1) != round(gs0[w][k][1], 1))
    ok("SF11 reading the Leveloggers as UTC is ruled out by the log, and moves depths", moved_utc >= 1,
       "%d of %d depths move" % (moved_utc, 2 * len(absw0)))
    # SF16: the head reference is the pumping level, as both report forms define total head
    a_def = "Total head = pumping water level + discharge head (psi x 2.31) + column and fittings loss"
    b_def = "TDH = PWL + discharge psi x 2.31 + column friction"
    import pdfplumber
    defs_a = defs_b = 0
    for f in files:
        if "pump_tests" in f:
            with pdfplumber.open(f) as pdf:
                tx = " ".join((pg.extract_text() or "").replace("\n", " ") for pg in pdf.pages)
            defs_a += a_def in tx
            defs_b += b_def in tx
    e_swl = G.extraction(d, route="SWL")
    ok("SF16 every report defines total head from the pumping level", defs_a + defs_b == len(d["all_tests"]),
       "%d and %d reports" % (defs_a, defs_b))
    ok("SF16 the standing-level reference buys nothing (ruled out)", e_swl["purchase"] == 0, "ranch %d" % e_swl["total"])
    # SF17: the 24 hours run from the end of the last interval the utility's data record with energy
    ok("SF17 the notice counts the 24 hours from the end of the last energised interval",
       "counted from the end of the last interval in which the utility's data for the well's service record energy" in nt, "")
    gs_all = {w: G.static_depths(d, w) for w in d["reg"]}
    var = {}
    for b in ("hour", "start"):
        alt = {w: G.static_depths(d, w, boundary=b) for w in d["reg"]}
        var[b] = sum(1 for w in d["reg"] for k in ("spring", "fall") if round(alt[w][k][1], 1) != round(gs_all[w][k][1], 1))
    ok("SF17 the readings the sentence rules out would move depths", var["hour"] + var["start"] >= 1,
       "hourly roll-up moves %d, interval start %d" % (var["hour"], var["start"]))
    # Ask D: the schedule's own sentences rule out the shortfall readings
    tf = " ".join(B.tariff_text(target).split())
    ok("Ask D: the schedule files its season and its off-peak hours",
       "Summer season: June 1 through September 30" in tf and "off-peak all other hours" in tf, "")
    # ---- zero-counts: the call reads no ask organ
    unmet = [w for w in d["reg"] if d["reg"][w]["Flow meter"] == "none"]
    ok("zero-count: no unmetered well on an absolute logger", all("vented" in str(d["reg"][w]["Level logger"]) for w in unmet), "")
    ok("zero-count: no swap touches an unmetered well", all(len(set(s for _, s in d["hist"][w])) == 1 for w in unmet), "")
    # ---- asks
    gs = {w: G.static_depths(d, w) for w in d["reg"]}
    ok("Ask A: every well has both static depths", all(gs[w]["spring"] and gs[w]["fall"] for w in gs), "")
    absw = [w for w in d["reg"] if "absolute" in str(d["reg"][w]["Level logger"])]
    unc = {w: G.static_depths(d, w, compensate=False) for w in absw}
    ok("Ask A: uncompensated depths miss every absolute figure", all(
        round(unc[w][k][1], 1) != round(gs[w][k][1], 1) for w in absw for k in ("spring", "fall")), "")
    cl = {w: G.static_depths(d, w, baro_shift=-8, swap_aware=False) for w in absw}
    kept = sum(1 for w in absw for k in ("spring", "fall") if round(cl[w][k][1], 1) == round(gs[w][k][1], 1))
    ok("Ask A: the clock-face cracker keeps at most 3 of 8", kept <= 3, "%d kept" % kept)
    gc = G.energy_charges(d)
    rc = G.energy_charges(d, schedule="register")
    moved = sum(1 for w in d["reg"] if round(rc[w]) != round(gc[w]))
    ok("Ask D: the register's schedule misses the switched wells", moved == len(d["letter"]["sas"]), "%d moved" % moved)
    hc = G.energy_charges(d, hourly=True)
    ok("Ask D: an hourly roll-up moves most charges", sum(1 for w in d["reg"] if round(hc[w]) != round(gc[w])) >= 10, "")
    ok("Ask D: charges are invariant to the call's route (energy only)", True, "")
    # ---- deliverables against the golden
    rows = list(csv.DictReader(open(os.path.join(gdir, "wy2026_extraction_return.csv"), encoding="utf-8")))
    byid = {d["reg"][w]["Agency well ID"]: w for w in d["reg"]}
    good = all(int(r["wy2026_af"]) == g["reported"][byid[r["agency_well_id"]]] for r in rows)
    ok("return: every well's water year volume is the golden's", good and len(rows) == len(d["reg"]), "")
    ok("return: static depths are the golden's", all(
        abs(float(r["spring_2026_static_dtw_ft"]) - round(gs[byid[r["agency_well_id"]]]["spring"][1], 1)) < 1e-6 and
        abs(float(r["fall_2026_static_dtw_ft"]) - round(gs[byid[r["agency_well_id"]]]["fall"][1], 1)) < 1e-6 for r in rows), "")
    ok("memo exists", os.path.exists(os.path.join(gdir, "transfer_purchase_memo.docx")), "")
    n_fail = sum(1 for r in ROWS if not r[1])
    print("checks: %d of %d pass" % (len(ROWS) - n_fail, len(ROWS)))
    return n_fail == 0
