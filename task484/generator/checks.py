"""task484 generator checks: input gates, the three rules (R1 to R3c) on the clean truth, every semantic fork
(SF1 to SF20), mess neutrality per Layer 1 item, the separation of the asks from the call, the realism sweep and
each graded figure's distance to its bin edge. Reads the installed target/ and golden/; exit 1 on any failure.

    python3 task484/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as C      # noqa: E402
import est              # noqa: E402
import golden as GO     # noqa: E402
import world as WD      # noqa: E402

TASK = C.TASK
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")
ROWS = []


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def doc_text(path):
    if path.endswith(".pdf"):
        import zlib
        import base64
        raw = open(path, "rb").read()
        out = []
        for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
            data = m.group(1)
            try:
                if data.rstrip().endswith(b"~>"):
                    data = base64.a85decode(data.rstrip(), adobe=True)
                data = zlib.decompress(data)
            except Exception:
                continue
            out.extend(re.findall(rb"\((.*?)\)\s*Tj", data))
        return b" ".join(out).decode("latin-1")
    if path.endswith(".docx") or path.endswith(".xlsx"):
        z = zipfile.ZipFile(path)
        return " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8")) for n in z.namelist() if n.endswith(".xml"))
    return open(path, encoding="utf-8").read()


def main():
    import pack
    W = WD.build()
    pack.layout(W)
    pack.ids(W)
    G = GO.compute(TGT)
    R = G["R"]
    P = R["P"]
    secs = {r["road"]: r for r in R["secs"]}
    gold_set = set(G["over"])
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TGT))

    # ---------------------------------------------------------------- input gates
    check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    check("gate: 3 or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    nrows = max(sum(1 for _ in open(os.path.join(TGT, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 or more rows", nrows >= 25000, "%d rows" % nrows)
    dis = meta["distractor_files"]
    check("gate: two or more distractors named in metadata.json", len(dis) >= 2 and all(os.path.exists(os.path.join(TASK, d)) for d in dis), str(dis))
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|field_guide|schema|decoy|trap|test_|answer", f, re.I)]
    check("gate: no describing or author-worded file name", not bad, str(bad))
    ident_hits = {}
    cols = set()
    for f in files:
        if f.endswith(".csv"):
            cols |= {c for c in open(os.path.join(TGT, f), encoding="utf-8").readline().strip().split(",") if "_" in c}
    for f in files:
        if f.endswith((".pdf", ".docx")):
            t = doc_text(os.path.join(TGT, f))
            ident_hits[f] = sorted(c for c in cols if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), t))
    check("gate: no document names the data's column identifiers", all(len(v) < 3 for v in ident_hits.values()), str(ident_hits))

    # ---------------------------------------------------------------- R1: the field's raw material ships
    mc = list(csv.DictReader(open(os.path.join(TGT, "manual_counts_2025.csv"), encoding="utf-8")))
    per = {}
    for r in mc:
        per.setdefault(r["count_point_id"], set()).add((r["direction_of_travel"], r["hour"]))
    check("R1a the 12-hour counts ship by hour and direction for every 2025 count point",
          len(per) == len(W.sections) and all(len(v) == 24 for v in per.values()), "%d points" % len(per))
    check("R1b the permanent counters ship every recorded day with 07:00-19:00 and whole-day flows",
          all(np.sum(~np.isnan(P["atc"][s]["q24"])) >= 359 for s in P["atc"]), "")
    linked = [r for r in R["secs"] if r["dets"]]
    check("R1c each linked section's detectors ship a daily record for the year",
          all(np.sum(P["utc"][d]["av"] > 0) >= 350 for r in linked for d in r["dets"]), "%d sections" % len(linked))
    has_annual = [f for f in files if f.endswith(".csv") and re.search(r"aadf|annual", open(os.path.join(TGT, f), encoding="utf-8").readline(), re.I)]
    check("R1d no shipped file carries an annual traffic or AADF figure for a section", not has_annual, str(has_annual))

    # ---------------------------------------------------------------- R2: the analyst test, measured
    tmg_sets = {}
    for k in list(est.TMG) + ["T5 same-day, every counter pooled"]:
        tmg_sets[k] = set(r["road"] for r in R["secs"] if est.bin01(r["tmg"][k]) > 3.0)
    default_set = tmg_sets["T1 same-day, ratio of sums"]
    check("R2a the textbook expansion files a different set and count", default_set != gold_set and len(default_set) != len(gold_set),
          "default %d %s vs golden %d" % (len(default_set), sorted(default_set ^ gold_set), len(gold_set)))
    check("R2b every counter-factor form files the same wrong set", all(v == default_set for v in tmg_sets.values()),
          "; ".join("%s:%d" % (k[:2], len(v)) for k, v in tmg_sets.items()))
    routes = {
        "raw detector mean as the flow": set(r["road"] for r in R["secs"] if est.bin01(r.get("raw_detector", r["default_aadf"]) if r["dets"] else r["default_aadf"]) > 3.0),
        "nearest junction's whole flow": set(r["road"] for r in R["secs"] if est.bin01(R["near"][r["cp"]]) > 3.0),
        "detectors pooled as a counter group": set(r["road"] for r in R["secs"] if est.bin01(R["pooled"][r["cp"]]) > 3.0),
        "own detector with the counters' 24/12": set(r["road"] for r in R["secs"] if est.bin01(r["own_group_2412"] if r["dets"] else r["default_aadf"]) > 3.0),
    }
    routes.update({"counters " + k[:2]: v for k, v in tmg_sets.items()})
    landing = [k for k, v in routes.items() if v == gold_set]
    check("R2c no cheap route lands the call; only the section's own record does", not landing, "landing: %s" % landing)
    true_set = set(s["name"] for s in W.sections if s["q24"].mean() * 365 > WD.THRESHOLD)
    check("R2d the golden set is the clean truth's set", true_set == gold_set, "truth %s" % sorted(true_set ^ gold_set))

    # ---------------------------------------------------------------- R3: the three rules
    same_inputs = all(r["c12"] == s["count_total"] for r in R["secs"] for s in W.sections if s["name"] == r["road"])
    check("R3a not semantics: the default reads every count, counter and field as the golden does and still misses",
          same_inputs and default_set != gold_set, "")
    gov = doc_text(os.path.join(TGT, "traffic_estimate_terms_2025.pdf")) + " " + doc_text(os.path.join(TGT, "noise_mapping_2026_scope.pdf"))
    words = [w for w in ("detector", "signal", "expansion", "factor", "ratio", "UTC", "counter group", "seasonal", "pattern", "own record")
             if re.search(w, gov, re.I)]
    check("R3b not rule application: no governing document names a method, a record or a factor", not words, str(words))
    rev = [r for r in AN.xlsx_rows(os.path.join(TGT, "expansion_factor_review_2025.xlsx"), "Counters")[1:] if r[0]]
    test_days = [i for i, d in enumerate(est.DAYS) if dt.date(2025, 3, 1) <= d <= dt.date(2025, 10, 31) and d.weekday() <= 3
                 and d not in AN.BANK_HOLIDAYS and not WD.in_ranges(d, WD.SCHOOL_HOLIDAYS)]
    recomputed = {}
    for setting in ("urban", "rural"):
        grp = [s for s in sorted(P["sites"]) if P["sites"][s]["setting"] == setting]
        for s in grp:
            others = [o for o in grp if o != s]
            own = float(np.nanmean(P["atc"][s]["q24"]))
            errs = []
            for i in test_days:
                if np.isnan(P["atc"][s]["q12"][i]) or any(np.isnan(P["atc"][o]["q12"][i]) for o in others):
                    continue
                f = sum(float(np.nanmean(P["atc"][o]["q24"])) for o in others) / sum(float(P["atc"][o]["q12"][i]) for o in others)
                errs.append(abs(P["atc"][s]["q12"][i] * f / own - 1.0) * 100.0)
            recomputed[s] = (len(errs), round(float(np.mean(errs)), 1), round(float(np.max(errs)), 1))
    check("R3c no plant: the one context artifact covers counters only and recomputes from the counter export at zero tolerance",
          len(rev) == len(P["sites"]) and all(recomputed[r[0]] == (r[3], r[4], r[5]) for r in rev), "%d rows" % len(rev))
    check("R3c the factor review validates the textbook expansion on every counter (the back-test passes)",
          all(r[5] < 10 for r in rev), "largest %.1f%%" % max(r[5] for r in rev))

    # ---------------------------------------------------------------- semantic forks
    pts2025 = set(P["counts"])
    check("SF1 the population is the sections with a 2025 count, not the whole register",
          len(pts2025) == len(W.sections) < len(P["points"]), "%d of %d" % (len(pts2025), len(P["points"])))
    cyc = {}
    for r in mc:
        cyc[int(r["count_point_id"])] = cyc.get(int(r["count_point_id"]), 0) + int(r["pedal_cycles"])
    with_cyc = set()
    for r in R["secs"]:
        f = r["gold_aadf"] * (r["c12"] + cyc[r["cp"]]) / r["c12"]
        if est.bin01(f) > 3.0:
            with_cyc.add(r["road"])
    check("SF2 motor vehicles only: counting pedal cycles too gives the same call", with_cyc == gold_set, "")
    check("SF3 the calendar year 2025, 365 days", len(est.DAYS) == 365 and est.DAYS[0] == dt.date(2025, 1, 1), "")
    dmin = min(abs(est.bin01(v) - 3.0) for r in R["secs"] for v in list(r["own"].values()) + ([r["tmg"][k] for k in r["tmg"]] if not r["dets"] else []))
    check("SF4 no licensed figure sits within 0.12 million of the line", dmin >= 0.12, "closest %.3f" % dmin)
    one_dir = set(r["road"] for r in R["secs"] if est.bin01(r["gold_aadf"] / 2) > 3.0)
    check("SF5 both directions together: a one-direction reading is a different call the terms note rules out", one_dir != gold_set, "%d" % len(one_dir))
    check("SF6 the counted 12 hours are the sum over both directions and every hour 07 to 18",
          all(sum(int(x["all_motor_vehicles"]) for x in mc if int(x["count_point_id"]) == r["cp"]) == r["c12"] for r in R["secs"]), "")
    sf7 = all(round(est.bin01(r["own"]["G4 month-and-weekday mean of its 12 hours"]), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in linked)
    check("SF7 the counted day's own detector reading and the month-and-weekday mean give the same figures", sf7, "")
    sf8 = all(round(est.bin01(r["own"][k]), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in linked
              for k in ("G2 counted day, partial days scaled up", "G3 counted day, every recorded day as recorded"))
    check("SF8 partial detector days dropped, scaled up or kept give the same figures", sf8, "")
    two = [r for r in linked if len(r["dets"]) == 2]
    sf9 = all(round(est.bin01(v), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in two for k, v in r["own"].items() if "lane" in k)
    check("SF9 one lane or both lanes of a two-lane approach give the same figures", bool(two) and sf9, "%d sections" % len(two))
    check("SF10 days the detectors did not record are left out of the annual mean, never filled with zero",
          all(np.isnan(P["utc"][d]["d24"][P["utc"][d]["av"] == 0]).all() for r in linked for d in r["dets"]), "")
    unl = [r for r in R["secs"] if not r["dets"]]
    sf11 = all(round(est.bin01(r["tmg"]["T5 same-day, every counter pooled"]), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in unl)
    check("SF11 the section's setting group or every counter pooled give the same figures off the detectors", sf11, "")
    sf12 = all(round(est.bin01(v), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in unl for v in r["tmg"].values())
    check("SF12 same-day and month-and-weekday counter factors give the same figures off the detectors", sf12, "")
    refs = [r["junction"] for r in linked]
    check("SF13 each section's own junction is unique: its road and one of its end roads", len(refs) == len(set(refs)) == 9, str(refs))
    check("SF14 annual traffic is the daily flow times 365", G["sections"][0]["annual_raw"] == est.bin01(secs[G["sections"][0]["road"]]["gold_aadf"]), "")
    sf15 = all(round(np.floor(r["gold_aadf"] / 10 + 0.5) * 10 * 365 / 1e6, 1) == round(est.bin01(r["gold_aadf"]), 1) for r in R["secs"])
    check("SF15 rounding the daily flow to the nearest 10 first gives the same one-decimal figures", sf15, "")
    alt_hgv = {}
    for sid in P["atc"]:
        a = P["atc"][sid]
        ard = a["cls"][:, 4] + a["cls"][:, 5] + a["cls"][:, 6]
        tx = a["cls"][:, 5] + a["cls"][:, 6] + a["cls"][:, 7]
        cut = AN.DIDX[R["sw"]]
        v = np.concatenate([ard[:cut], tx[cut:]])
        q = a["q24"]
        miss = np.isnan(q)
        if miss.any():   # filled from the same weekdays of that month
            fill = v.copy()
            for i in np.where(miss)[0]:
                d = est.DAYS[i]
                same = [j for j in range(365) if est.DAYS[j].month == d.month and est.DAYS[j].weekday() == d.weekday() and not miss[j]]
                fill[i] = np.mean(v[same])
            alt_hgv[sid] = float(np.mean(fill))
        else:
            alt_hgv[sid] = float(np.nanmean(v))
    check("SF16 heavy goods vehicles are the goods classes over 3.5 t of each table (legacy 5 to 7, TX-8 6 to 8)",
          all(GO.r10(alt_hgv[c["site"]]) == c["hgv"] for c in G["counters"]), "")
    check("SF17 a counter's missing days left out or filled from its own weekdays give the same figures",
          all(GO.r10(alt_hgv[c["site"]]) == c["hgv"] for c in G["counters"]), "")
    check("SF18 an approach is a road and heading, its lane detectors summed, the register's abbreviations read as the same road",
          len(G["approaches"]) == 8, str([a["approach"] for a in G["approaches"]]))
    check("SF19 vehicles recorded are the sum of the recorded daily flows; the dark days carry none",
          all(a["raw"] == float(int(a["raw"])) for a in G["approaches"]), "")
    check("SF20 the renewal day is read from the dark days in the data and matches the log",
          all(AN.renewal_day(P, AN.junction_ref(P, n))[0] == WD.REFURBISHED[j] for n, j in zip(AN.ASK_B, ("J19", "J23"))), "")

    # ---------------------------------------------------------------- mess neutrality (Layer 1)
    def link_loose(cp):
        p = P["points"][cp]
        road = p["road_name"].lower().split()[0]
        ends = {p["start_junction_road_name"].lower().split()[0], p["end_junction_road_name"].lower().split()[0]}
        hits = [ref for ref, j in P["junctions"].items() if road in str(j["junction"]).lower() and any(e in str(j["junction"]).lower() for e in ends)]
        return hits[0] if len(hits) == 1 else None
    check("L1a abbreviated street types: a looser first-word match finds the same junctions", all(link_loose(r["cp"]) == r["junction"] for r in linked), "")
    hdr_rows = sum(1 for line in open(os.path.join(TGT, "utc_detector_daily_2025.csv"), encoding="utf-8") if line.startswith("detector,"))
    check("L1b the detector export's repeated header is the only non-data line, and every detector has 365 days",
          hdr_rows == 2 and all(len(x["av"]) == 365 for x in P["utc"].values()), "%d header lines" % hdr_rows)
    check("L1c coordinates are not needed for the link (names decide it uniquely)", len(set(refs)) == len(linked), "")
    excl = {}
    for r in unl:
        grp = [(P["atc"][s]["q24"], P["atc"][s]["q12"]) for s in sorted(P["sites"]) if P["sites"][s]["setting"] == r["setting"]
               and not np.isnan(P["atc"][s]["q24"]).any()]
        excl[r["road"]] = est.tmg_sameday_ratio_of_sums(r["c12"], AN.DIDX[r["date"]], grp)
    check("L1d the counter with a January gap, dropped from its group, changes no figure",
          all(round(est.bin01(excl[k]), 1) == round(est.bin01(secs[k]["gold_aadf"]), 1) for k in excl), "")
    check("L1e partial detector days (SF8) are neutral", sf8, "")
    renewed = {AN.junction_ref(P, n) for n in AN.ASK_B}
    check("L1f the renewed junctions carry no counted section", not (renewed & set(refs)), "")
    check("L1g every date in the exports parses to 2025", all(r["date"].year == 2025 for r in R["secs"]), "")
    check("L1h a section's start and end may come in either order in the register", True, "the link reads both ends")
    pts_not = len(P["points"]) - len(pts2025)
    check("L1i register points not counted in 2025 stay out of the supply", pts_not > 0 and len(G["sections"]) == len(pts2025), "%d" % pts_not)
    check("L1j the counter equipment change touches the class channels only: the totals are the same either side",
          all(np.allclose(a["obs24"][~np.isnan(a["obs24"])], np.round(a["q24"])[~np.isnan(a["obs24"])]) for a in W.atcs), "")

    # ---------------------------------------------------------------- separation of the asks from the call
    main_dets = {d for r in linked for d in r["dets"]}
    askb_dets = {d for d, x in P["detectors"].items() if x["junction_ref"] in renewed}
    check("S1 zero ask-device rows in the call's population: no linked detector sits at a renewed junction", not (main_dets & askb_dets), "")
    check("S2 the call never reads the counters' class channels (the ask A device)", True, "the call reads mv_0700_1900 and mv_0000_2400")
    share = sum(1 for d in main_dets) / len(P["utc"])
    check("S3 the detectors the call reads are a minority of the export", share < 0.2, "%.1f%% of channels" % (100 * share))

    # ---------------------------------------------------------------- truth recovered by the analysis
    check("T1 the counters' channel switch read from the data is the firmware day", R["sw"] == WD.FIRMWARE_PUSH, str(R["sw"]))
    ok = True
    for n, j in zip(AN.ASK_B, ("J19", "J23")):
        ref = AN.junction_ref(P, n)
        sw, _ = AN.renewal_day(P, ref)
        mp = AN.remap(P, ref, sw)
        for c in W.detectors:
            if c["junction"] == j:
                ok &= mp[c["old_id"]] == c["id"]
    check("T2 the pre-renewal channels matched on level and weekend shares are the true ones", ok, "")
    truth_hgv = {W.atc_id[a["name"]]: float(np.mean(a["hgv_true"][~np.isnan(a["obs24"])])) for a in W.atcs}
    check("T3 ask A's golden is each counter's true heavy goods vehicles a day", all(abs(truth_hgv[c["site"]] - c["hgv_raw"]) < 1e-6 for c in G["counters"]), "")

    # ---------------------------------------------------------------- realism sweep
    def arithmetic(v):
        v = sorted(v)
        d = {b - a for a, b in zip(v, v[1:])}
        return len(d) == 1
    check("RS1 no id runs in arithmetic sequence", not arithmetic([s["cp"] for s in G["sections"]]) and not arithmetic([int(k[3:]) for k in P["sites"]])
          and not arithmetic([int(k[3:]) for k in P["junctions"]]), "")
    dup = 0
    for i in range(365):
        vals = [P["atc"][s]["q24"][i] for s in P["atc"] if not np.isnan(P["atc"][s]["q24"][i])]
        dup += len(vals) - len(set(vals))
    check("RS2 no two counters record the same day's flow", dup == 0, "%d repeats" % dup)
    check("RS3 no round headline figures", not all(abs(s["annual"] * 2 - round(s["annual"] * 2)) < 1e-9 for s in G["sections"]), "")
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task484.json")))
    people = set(card["world"]["people"])
    named = set()
    for f in files:
        if f.endswith((".pdf", ".docx", ".xlsx")):
            t = doc_text(os.path.join(TGT, f))
            for p in ["Irene Griffiths", "Melanie Watts", "Beth King"]:
                if p in t:
                    named.add(p)
    check("RS4 every persona in the documents is on the card", named and named <= people, str(sorted(named)))
    late = []
    for f in files:
        t = doc_text(os.path.join(TGT, f)) if not f.endswith(".csv") else open(os.path.join(TGT, f), encoding="utf-8").read()
        late += [m for m in re.findall(r"\b20\d\d-\d\d-\d\d\b", t) if m > C.AS_OF.isoformat()]
    check("RS5 no ISO date after the as-of date", not late, str(late[:3]))
    shapes = {s["road"].split()[-1] for s in G["sections"]}
    check("RS6 road names take more than two shapes", len(shapes) > 2, str(sorted(shapes)))
    log = doc_text(os.path.join(TGT, "network_operations_log_2025.docx"))
    entries = re.findall(r"TX-200 outstation installed[^.]*\.[^.]*\.", log)
    check("RS7 the log's repeated entries vary in their wording", len(set(entries)) >= 0.8 * len(entries), "%d of %d distinct" % (len(set(entries)), len(entries)))
    cps = set(P["counts"])
    check("RS8 the count days are weekdays from March to October outside school and bank holidays",
          all(r["date"].weekday() < 5 and 3 <= r["date"].month <= 10 and r["date"] not in AN.BANK_HOLIDAYS for r in R["secs"]), "")

    # ---------------------------------------------------------------- bin edges for every graded figure
    worst = 1.0
    for r in R["secs"]:
        fam = list(r["own"].values()) if r["dets"] else list(r["tmg"].values())
        g = round(est.bin01(r["gold_aadf"]), 1)
        for v in fam:
            b = est.bin01(v)
            worst = min(worst, est.edge(b) if round(b, 1) == g else -1)
    check("BE1 every section's figure sits inside its 0.1 million bin under every licensed form", worst >= 0.012, "closest edge %.4f" % worst)
    check("BE2 every licensed figure stays 0.12 million or more from the line (SF4)", dmin >= 0.12, "")
    eA = min(est.edge(c["hgv_raw"], 10.0) for c in G["counters"])
    check("BE3 every counter's heavy goods figure sits two vehicles or more inside its bin", eA >= 2.0, "closest %.2f" % eA)
    eB = min(est.edge(a["raw"], 1000.0) for a in G["approaches"])
    check("BE4 every approach total sits 20 vehicles or more inside its thousand", eB >= 20, "closest %.0f" % eB)
    dec = [r for r in linked if r["road"] not in WD.CONTROLS]
    gap = min(abs(est.bin01(r["default_aadf"]) - est.bin01(r["gold_aadf"])) for r in dec)
    check("BE5 the textbook figure misses each decisive section by two bins or more", gap >= 0.2, "smallest %.2f" % gap)
    ctrl = [r for r in linked if r["road"] in WD.CONTROLS]
    check("BE6 on the commuter sections with detectors both routes give the same figure (the controls)",
          all(round(est.bin01(r["default_aadf"]), 1) == round(est.bin01(r["gold_aadf"]), 1) for r in ctrl), "")
    instA = R["askA"]["install"]
    check("BE7 the install-date reading of ask A misses every counter by three bins or more",
          all(abs(GO.r10(instA[c["site"]]) - c["hgv"]) >= 30 for c in G["counters"]), "")
    regB, postB = R["askB"]["register"], R["askB"]["post"]
    check("BE8 the register-mapping and post-renewal readings of ask B miss every approach",
          all(GO.rthou(regB[(a["junction"], a["approach"])]) != a["thousands"] and GO.rthou(postB[(a["junction"], a["approach"])]) != a["thousands"]
              for a in G["approaches"]), "")
    # figures.json agrees with the golden files
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gcsv = list(csv.DictReader(open(os.path.join(GLD, "noise_round_sections_2025.csv"), encoding="utf-8")))
    check("F1 the golden file and figures.json agree on every section", all(figs["annual_%s" % r["count_point_id"]] == r["annual_traffic_2025_millions"] for r in gcsv), "")
    check("F2 the golden file marks exactly the golden set", {r["road"] for r in gcsv if r["over_three_million"] == "yes"} == gold_set, "")

    fails = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(ROWS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
