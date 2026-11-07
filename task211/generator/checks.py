"""The generator's assertions, run on every build: the three rules on the clean truth (R1 to R3c), every row of the
semantic fork table (SF1 to SF15), the reasonable family, the separation line, rounding clearance of every graded
figure, the ask conventions, the input gates and the realism sweep. Labels start with the block they belong to."""
import builtins
import csv
import datetime as dt
import glob
import json
import os
import re
import zipfile

import numpy as np
from openpyxl import load_workbook
from pypdf import PdfReader

import ceiling as CL
import golden as G
import pack
import sim
import world as W

N = [0]
TRUTH = set(W.RADIOGRAPHY)


def ok(label, cond, detail=""):
    if not cond:
        raise AssertionError("checks %s FAILED %s" % (label, detail))
    N[0] += 1


def call_of(vals, stat, **kw):
    det = G.detections(vals, stat, **kw)
    return {c: sorted(v["dates"]) for c, v in G.call_from(vals, stat, det).items()}


def gold_call(g):
    return {c: sorted(v["dates"]) for c, v in g["call"].items()}


def across_gaps(vals, stat, fall=G.FALL, floor=G.FLOOR):
    """The fall test on consecutive valid values whatever lies between them (a gap read as no gap)."""
    out = {}
    for c, v in vals.items():
        x = v.copy(); x[stat[c] != "V"] = np.nan
        ex = x - G.rolling_median(x)
        idx = np.where(~np.isnan(ex))[0]
        e = ex[idx]
        a, b, n2 = e[:-2], e[1:-1], e[2:]
        hit = (a >= floor) & ((a - b) > fall * a) & (n2 < (1 - fall) * a)
        days = sorted({(W.Q_START + dt.timedelta(minutes=10 * int(idx[k]))).date() for k in np.where(hit)[0]})
        if days:
            out[c] = days
    return out


def pdf_text(path):
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def run(tgt, T, g, info, figs):
    N[0] = 0
    S = T["S"]
    idx = {s["code"]: i for i, s in enumerate(S)}
    vals, stat = g["vals"], g["stat"]
    gc = gold_call(g)
    L = g["routes"]
    sessions = {}
    for s in T["sessions"]:
        sessions.setdefault(s["code"], []).append(s["date"])

    # ---------------------------------------------------------------- R: the three rules on the clean truth
    files = sorted(os.listdir(tgt))
    ok("R1 the ten-minute record of every station ships", len(vals) == len(S) and
       all((~np.isnan(v)).sum() > 12000 for v in vals.values()))
    data_text = ""
    for f in files:
        if f.endswith((".csv", ".json")):
            data_text += open(os.path.join(tgt, f), encoding="utf-8").read(400000).lower()
    ok("R1 no data file carries an origin, a detection or a cause", not re.search(r"artificial|radiograph|origin|weld",
                                                                                  data_text))
    rg = T["rain_g"]
    clean_ex = T["wash"] + T["art"]
    flagged, cleared_truth = set(), 0
    for s in S:
        i = idx[s["code"]]
        gi = sim.nearest_gauge(s)
        m = clean_ex[i] > 30
        t = 0
        while t < W.N10:
            if m[t]:
                a = t
                while t < W.N10 and m[t]:
                    t += 1
                wet = rg[gi, max(0, a - 6):t + 6].max() > 0
                if not wet:
                    flagged.add(s["code"])
                elif s["code"] in TRUTH and T["art"][i, a:t].max() > 0:
                    cleared_truth += 1
            else:
                t += 1
    ok("R2a on the clean truth the rain screen files another set", flagged != TRUTH and len(flagged - TRUTH) >= 4,
       sorted(flagged))
    ok("R2a on the clean truth the rain screen clears radiography nights", cleared_truth >= 3, cleared_truth)
    found = {}
    for s in S:
        i = idx[s["code"]]
        e = clean_ex[i]
        a, b, c = e[:-2], e[1:-1], e[2:]
        hit = (a >= 30) & ((a - b) > 0.5 * a) & (c < 0.5 * a)
        for k in np.where(hit)[0]:
            found.setdefault(s["code"], set()).add((W.Q_START + dt.timedelta(minutes=10 * int(k))).date())
    ok("R2b on the clean truth the decay bound finds exactly the radiography nights",
       {c: sorted(v) for c, v in found.items()} == {c: sorted(v) for c, v in sessions.items()}, found)
    w = T["wash"]
    a, b = w[:, :-1], w[:, 1:]
    sel = a >= 30
    nat_fall = float(((a - b) / np.where(a == 0, 1, a))[sel].max())
    ok("R2c the clean natural excess never falls by more than about a quarter in a step", nat_fall < 0.3, nat_fall)
    ok("R3a not semantics: every field read right, the procedure's rain screen still files %d stations"
       % len(L["R0_codes"]), set(L["R0_codes"]) != TRUTH and len(L["R0_codes"]) >= 8, L["R0_codes"])
    ok("R3a the neighbour and night refinements stay wrong", set(L["R1_codes"]) != TRUTH and set(L["R2_codes"]) != TRUTH)
    proc = pdf_text(os.path.join(tgt, pack.FILES["procedure"])).lower()
    agr = pdf_text(os.path.join(tgt, pack.FILES["agreement"])).lower()
    for term in ("radon", "lead-214", "bismuth", "progeny", "washout", "decay product", "falls by", "half of"):
        ok("R3b no governing document names the decisive physics (%s)" % term, term not in proc and term not in agr)
    ok("R3b the filed screen is the investigation level", "30 nsv/h or more above the reference level" in proc)
    ok("R3c no decoy: the distractors are named and rank nothing on origin",
       sorted(json.load(open(os.path.join(os.path.dirname(tgt), "metadata.json")))["distractor_files"]) ==
       sorted("target/" + pack.FILES[k] for k in ("national", "gammaspec")))
    nat_text = pdf_text(os.path.join(tgt, pack.FILES["national"])).lower()
    ok("R3c the annual report names no 2026 station or night", "2026q3" not in nat_text and "radiograph" not in nat_text)

    # ---------------------------------------------------------------- the call against the truth
    ok("CALL the golden is the radiography stations", set(gc) == TRUTH, sorted(gc))
    ok("CALL every radiography night and no other", gc == {c: sorted(v) for c, v in sessions.items()}, gc)
    for c in TRUTH:
        i = idx[c]
        v = vals[c]
        best = None
        for s, e, f in g["det"][c]:
            k = s + int(np.nanargmax(v[s:e]))
            if best is None or v[k] > v[best]:
                best = k
        ok("CALL %s's peak sits in a radiography interval" % c, T["art"][i, best] > 0)
        ok("CALL %s's peak is a recorded value" % c, g["call"][c]["peak"] == int(np.nanmax(v[best:best + 1])))
    ok("CALL natural falls stop at %d per cent, detections start at %d" % (g["nat_max_fall"], g["art_min_fall"]),
       g["nat_max_fall"] < 50 < g["art_min_fall"])

    # ---------------------------------------------------------------- SF: every row of the semantic fork table
    ok("SF1 station codes: the export and the call use platform codes", all(c.startswith("MV") for c in vals))
    tv = {c: v.copy() for c, v in vals.items()}
    ts = {c: np.where(s == "T", "V", s) for c, s in stat.items()}
    with_t = call_of(tv, ts)
    ok("SF2 source checks read as monitoring data add the checked stations (the schedule excludes them)",
       len(set(with_t) - TRUTH) >= 5, sorted(with_t))
    for c, v in g["call"].items():
        for s, e, f in v["episodes"]:
            ok("SF3 %s clear of the quarter's edges" % c, s > 288 and e < W.N10 - 288)
            st_utc = W.Q_START + dt.timedelta(minutes=10 * s)
            ok("SF4 %s date the same in UTC and BST" % c, st_utc.date() == (st_utc + W.BST).date())
            en = W.Q_START + dt.timedelta(minutes=10 * e) + W.BST
            ok("SF15 %s increase starts and ends on one BST date" % c, (st_utc + W.BST).date() == en.date() or
               en.time() == dt.time(0, 0))
    ok("SF5 the highest value recorded is the gross dose rate, and differs from the excess",
       all(g["call"][c]["peak"] > 120 for c in TRUTH))
    ok("SF6 one highest value per station, over all its increases",
       all(g["call"][c]["peak"] == max(int(round(np.nanmax(vals[c][s:e]))) for s, e, f in g["det"][c]) for c in TRUTH))
    dup = 0
    with open(os.path.join(tgt, pack.FILES["export"]), newline="") as f:
        rows = list(csv.reader(f))[1:]
    seen = set()
    for r in rows:
        if tuple(r) in seen:
            dup += 1
        seen.add(tuple(r))
    ok("SF7 the re-read station-days are exact duplicates", dup > 400 and len({(r[0], r[1]) for r in rows}) ==
       len(rows) - dup)
    raw = {c: v.copy() for c, v in vals.items()}
    for c in W.MICRO_UNIT_STATIONS:
        raw[c] = raw[c] / 1000.0
    ok("SF8 microsieverts read as nanosieverts move nothing", call_of(raw, stat) == gc)
    fs = {c: np.where(s == "F", "V", s) for c, s in stat.items()}
    ok("SF9 fault records carry no dose rate and move nothing", call_of(vals, fs) == gc)
    ok("SF10 test mode is outside the call (SF2) and the agreement says so", "own source checks, are not notified" in
       agr.replace("\n", " "))
    ok("SF11 the exchange step is small", "MV157" not in gc)
    ok("SF12 consecutive valid values across a gap give the same call", across_gaps(vals, stat) == gc,
       across_gaps(vals, stat))
    fam, bad = 0, []
    for base in ("c48", "t24", "w7"):
        for fall in (0.5, 0.55, 0.6, 0.7):
            for floor in (30, 35):
                for persist in (0, 1, 2):
                    fam += 1
                    if call_of(vals, stat, fall=fall, floor=floor, persist=persist, base=base) != gc:
                        bad.append((base, fall, floor, persist))
    ok("SF13 SF14 the reasonable family (baseline, fall, floor, persistence) files the golden, %d members" % fam,
       not bad, bad)
    edge = []
    for base in ("c48", "t24"):
        for fall in (0.45, 0.8):
            for floor in (25, 40):
                edge.append(call_of(vals, stat, fall=fall, floor=floor, persist=1, base=base) == gc)
    ok("SF14 the family's corners stay near the golden (at least half of them exact)", sum(edge) >= len(edge) // 2,
       edge)

    # ---------------------------------------------------------------- separation and shock
    for c in TRUTH:
        ok("SEP no fault record at %s" % c, not (stat[c] == "F").any())
    ok("SEP fault records only at the gland batch", {c for c in vals if (stat[c] == "F").any()} == set(W.GLAND_BATCH))
    opened = []
    real_open, real_zip = builtins.open, zipfile.ZipFile.__init__

    def spy_open(path, *a, **k):
        opened.append(str(path))
        return real_open(path, *a, **k)

    def spy_zip(self, file, *a, **k):
        opened.append(str(file))
        return real_zip(self, file, *a, **k)

    builtins.open, zipfile.ZipFile.__init__ = spy_open, spy_zip
    try:
        vv, ss = G.read_export(tgt)
        G.detections(vv, ss)
        G.compute(tgt)
    finally:
        builtins.open, zipfile.ZipFile.__init__ = real_open, real_zip
    ok("SEP the call reads the export alone", [p for p in opened[:1]] == [os.path.join(tgt, pack.FILES["export"])])
    for k in ("national", "gammaspec"):
        ok("SEP the golden never opens the distractor %s" % k, not any(pack.FILES[k] in p for p in opened))
    stats = {
        "investigation values": L["inv_counts"],
        "R0 dry days": {c: len(L["R0"].get(c, ())) for c in vals},
        "R1 lonely dry days": {c: len(L["R1"].get(c, ())) for c in vals},
        "R2 night days": {c: len(L["R2"].get(c, ())) for c in vals},
        "highest value": {c: float(np.nanmax(vals[c])) for c in vals},
        "mean value": {c: float(np.nanmean(vals[c])) for c in vals},
        "timeliness": {c: g["timely"][c]["pct"] for c in vals},
        "source check": {c: g["checks"][c]["pct"] for c in vals},
    }
    for name, st in stats.items():
        order = sorted(st, key=lambda c: (st[c], c))
        ok("SHOCK the call is not the top or bottom two on %s" % name, set(order[:2]) != TRUTH and
           set(order[-2:]) != TRUTH)

    # ---------------------------------------------------------------- asks: conventions converge, figures clear
    for c, v in g["checks"].items():
        for ylen in (365.0, 365.2425):
            no, ref, issued, cv = [x for x in G.certs()[v["source"]] if x[0] == v["cert"]][0]
            y = (v["date"] - ref).days / ylen
            p = v["net"] / (cv[v["jig"]] * 2 ** (-y / G.HALF)) * 100
            ok("A %s year length %s gives the same figure" % (c, ylen), "%.1f" % p == "%.1f" % v["pct"] and
               (abs(p - 100) <= 10) == v["passed"])
        ok("A %s clear of its rounding line" % c, abs((v["pct"] * 10) % 1 - 0.5) / 10 > 0.015, v["pct"])
        by_ref = [x for x in G.certs()[v["source"]] if x[1] <= v["date"]][-1][0]
        ok("A %s certificate by issue or by reference date agree" % c, by_ref == v["cert"])
    reg = CL.checks_by_register(tgt)
    moved = sorted(c for c in g["checks"] if reg[c][0] != round(g["checks"][c]["pct"], 1))
    ok("A the spare source in KIT-2 moves every KIT-2 check from 5 August to 3 September", moved ==
       sorted(c for c, v in g["checks"].items() if v["kit"] == "KIT-2" and W.CS0583_AWAY[0] <= v["date"] <
              W.CS0583_AWAY[1]) and len(moved) >= 6, moved)
    ok("A the swap moves no pass or fail", all(reg[c][1] == g["checks"][c]["passed"] for c in g["checks"]))
    ok("A two probes fail", sorted(c for c, v in g["checks"].items() if not v["passed"]) == ["MV184", "MV243"])
    ok("A every station checked once in the quarter", len(g["checks"]) == len(S))
    series = G.pump_series(tgt)
    q15 = dt.timedelta(minutes=15)
    filled = {}
    for fid, a_ in g["air"].items():
        t_, x_ = series[a_["sampler"]]
        alt = [sum(x_[k] * 0.25 for k in range(len(t_)) if a_["on"] <= t_[k] < a_["off"]),
               sum(x_[k] * 0.25 for k in range(len(t_)) if a_["on"] - q15 < t_[k] <= a_["off"]),
               sum(x_[k] * 0.25 for k in range(len(t_)) if a_["on"] - q15 <= t_[k] <= a_["off"] + q15)]
        for v_ in alt:
            ok("B %s integration bounds converge" % fid, "%.2f" % (a_["activity"] / v_ * 1000) == "%.2f" % a_["conc"])
        ok("B %s clear of its rounding line" % fid, abs((a_["conc"] * 100) % 1 - 0.5) / 100 > 0.0012, a_["conc"])
    for sampler, code, flow, style in W.AIR:
        A = T["air"][sampler]
        for f_ in A["filters"]:
            fid = f_["fid"]
            ok("B %s the golden volume is the measured flow with dropouts interpolated" % fid,
               abs(g["air"][fid]["volume"] - f_["gold_vol"]) < 1e-6, (g["air"][fid]["volume"], f_["gold_vol"]))
            concs = {how: round(g["air"][fid]["activity"] / v_ * 1000, 2) for how, v_ in f_["vols"].items()}
            ok("B %s every way of filling a dropout gives the same figure" % fid, len(set(concs.values())) == 1, concs)
    drops = sum(1 for s_ in W.AIR for f_ in T["air"][s_[0]]["filters"] if f_["dropout_rows"])
    ok("B flow dropouts sit inside most filters' weeks (%d of 39), never beside a stop" % drops, drops >= 25)
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        head = f.readline().strip().split(",")
    ok("B the controller export names its measured flow and its set-flow totaliser",
       head == ["sampler_id", "timestamp_utc", "pump_state", "measured_flow_m3_h", "run_totaliser_at_set_flow_m3"], head)
    fh, frows = G.read_rows(os.path.join(tgt, pack.FILES["field"]), "AS2")
    ok("B AS2's field sheet names its volume as hours at the set flow", "Volume at set flow (m3)" in fh, fh)
    ok("B the procedure files the volume of air drawn through the filter",
       "divided by the volume of air drawn through it" in proc.replace("\n", " "))
    log = {}
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        for s_, ts_, st_, fl_, tot_ in list(csv.reader(f))[1:]:
            if fl_:
                log.setdefault(s_, []).append((dt.datetime.strptime(ts_, "%Y-%m-%dT%H:%M:%SZ"), float(fl_)))
    tot_inc = {}
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        prev = {}
        for s_, ts_, st_, fl_, tot_ in list(csv.reader(f))[1:]:
            if tot_ and st_ == "RUN" and s_ in prev and float(tot_) >= prev[s_]:
                tot_inc.setdefault(s_, set()).add(round(float(tot_) - prev[s_], 1))
            if tot_:
                prev[s_] = float(tot_)
    ok("B the totalisers count running time at the set flow (their steps are the set flow's)",
       all(v <= {0.0, 2.5} for v in tot_inc.values()), tot_inc)
    for fid, a_ in g["air"].items():
        fl_ = [fl for t, fl in log[a_["sampler"]] if a_["on"] <= t < a_["off"] and fl > 0]
        k = len(fl_) // 4
        ok("B %s the measured flow falls as the filter loads" % fid, np.mean(fl_[:k]) > np.mean(fl_[-k:]))
    lab = load_workbook(os.path.join(tgt, pack.FILES["beta"]), read_only=True)
    lrows = list(lab["Gross beta"].iter_rows(values_only=True))[1:]
    ok("B two results re-issued as version 2", sorted(r[1] for r in lrows if r[8] == 2) == sorted(pack.REISSUED))
    ok("B thirteen filters a sampler, taken off in the quarter", all(sum(1 for k in g["air"] if k.startswith(p)) == 13
                                                                    for p in ("AF1", "AF2", "AF3")))
    for c, t in g["timely"].items():
        x = t["pct"]
        ok("C %s clear of its rounding line by an interval" % c,
           abs((x * 10) % 1 - 0.5) / 10 >= 100.0 / W.N10 or x == 100.0, x)
    fault_n = {c: int((stat[c] == "F").sum()) for c in vals}
    cr = CL.timely_by_ingest(tgt)
    for c in W.GLAND_BATCH:
        ok("C %s fault records move its figure" % c, cr[c] != round(g["timely"][c]["pct"], 1), (cr[c], g["timely"][c]))
    bare = G.timeliness(tgt, vals, stat)
    for c in g["timely"]:
        ok("C %s the same figure with test-mode values left out" % c,
           round(bare[c]["pct"], 1) == round(g["timely"][c]["pct"], 1), (bare[c]["pct"], g["timely"][c]["pct"]))
        x2 = bare[c]["pct"]
        ok("C %s clear of its rounding line with test-mode values left out" % c,
           abs((x2 * 10) % 1 - 0.5) / 10 >= 100.0 / W.N10 or x2 == 100.0, x2)
    ok("C the agreement counts a test-mode value", "in test mode for a source check is the station's value" in
       agr.replace("\n", " "))
    ok("C the denominator is the quarter's intervals", all(t["pct"] == t["timely"] / W.N10 * 100 for t in
                                                           g["timely"].values()))
    m = CL.measure(tgt, g)
    ok("ASK pair ceiling %.1f at or under 60" % m["pair"], m["pair"] <= 60)
    ok("ASK mirror leakage %.1f under 50" % m["mirror_leakage"], m["mirror_leakage"] < 50)
    ok("ASK the cracker misses part of every ask", all(m["rows"]["cracker"][k] < m["figures"][k] for k in "ABC"))
    ok("ASK the golden keeps every figure", m["full_keep"] == 100.0)

    # ---------------------------------------------------------------- input gates and realism
    ok("GATE 10 or more files", len(files) >= 10, len(files))
    ok("GATE 3 or more formats", len({os.path.splitext(f)[1] for f in files}) >= 3)
    ok("GATE a file of 25,000 rows", info["export_rows"] >= 25000 and info["pump_rows"] >= 25000)
    ok("GATE no file describes the data", not any(re.search(r"readme|dictionary|manifest|notes|schema", f, re.I)
                                                  for f in files))
    for f in files:
        if f.endswith(".xlsx"):
            wb = load_workbook(os.path.join(tgt, f), read_only=True)
            ok("GATE %s has no notes or readme sheet" % f, not any(re.search(r"readme|notes|about|dictionary", s, re.I)
                                                                   for s in wb.sheetnames))
    people = set(W.PEOPLE.values()) | {W.RPS}
    listed = {"Julia French", "Marian Ward", "Carole Davies", "Wayne Sanderson", "Antony Connolly", "Frances Stevens",
              "Katie Clarke", "Kim Simpson", "Shirley Collins", "Brian Smith", "Cameron Brown", "Hazel Lambert",
              "Rosemary Wood", "Gerard Buckley"}
    ok("REAL every persona from guard.py names", people <= listed, people - listed)
    for f in glob.glob(os.path.join(tgt, "*.pdf")):
        t = pdf_text(f)
        ok("REAL %s carries page numbers" % os.path.basename(f), "Page 1 of" in t)
        info_ = PdfReader(f).metadata
        made = str(info_.get("/CreationDate", ""))[2:10]
        ok("REAL %s made before the export" % os.path.basename(f), made <= "20261009", made)
    counts = {c: int((~np.isnan(v)).sum()) for c, v in vals.items()}
    short = [n for n in counts.values() if n < W.N10]
    ok("REAL the stations' value counts are spread, not uniform", len(set(short)) >= len(short) - 3 and
       max(short) - min(short) > 100, sorted(short))
    bids = []
    with open(os.path.join(tgt, pack.FILES["ingest"]), newline="") as f:
        for r in list(csv.reader(f))[1:2000]:
            bids.append(int(r[0][1:]))
    steps = np.diff(sorted(bids))
    ok("REAL batch numbers do not step evenly", len(set(steps.tolist())) > 2)
    ok("REAL every station has at least one telemetry outage", all(len(v) >= 1 for v in T["ingest"]["outages"].values()))
    cert = pdf_text(os.path.join(tgt, pack.FILES["certs"]))
    for serial, certs in W.SOURCES.items():
        for no, ref, issued, cv in certs:
            ok("PDF %s readable" % no, no in cert and ("%.0f" % cv["J1"]) in cert and issued.strftime("%d/%m/%Y") in cert)
    ann = re.findall(r"(MV\d{3})\s+[A-Za-z' ]+?\s+(\d+\.\d)\s+(\d+\.\d)", pdf_text(os.path.join(tgt, pack.FILES["national"])))
    ok("REAL the annual report lists every station", len(ann) == len(S), len(ann))
    ok("REAL no station's 2025 figure is its own Q3 timeliness or check", not [
        c for c, m_, cap in ann if cap == figs["timely"][c] or m_ == figs["timely"][c] or cap == figs["checks"][c]["pct"]])
    regtext = open(os.path.join(tgt, pack.FILES["sources"]), encoding="utf-8").read()
    ok("REAL the register records the transfer out and back", "transfer out" in regtext and "transfer in" in regtext)
    ok("A the register records CS-0583's return into KIT-2", "transfer in,KIT-2" in regtext)
    gs_text = pdf_text(os.path.join(tgt, pack.FILES["gammaspec"]))
    ok("PDF the spectrometry report carries its nuclide library", "Pb-214" in gs_text and "26.8 min" in gs_text and
       "Bi-214" in gs_text and "19.9 min" in gs_text)
    low = gs_text.lower()
    for term in ("dose rate", "rain", "rainfall", "washout", "increase", "fall", "falls", "excursion"):
        ok("PDF the spectrometry report says nothing of %s" % term, not re.search(r"\b%s\b" % term, low))
    return N[0]
