"""Generator checks for task142 on the installed pack (target/), the clean truth (world.py) and the golden.

    python3 task142/generator/checks.py          # exit 1 on any failed assertion

Blocks: G input gates, R1 to R3 the client's three rules executed on the clean truth, SF the semantic fork table,
F the cheap routes, B every graded figure's distance to its bin edge, M the call's population and the ask devices,
A the ask layer, S the realism sweep.
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import ceiling as C  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

TARGET = os.path.join(TASK, "target")
FAIL = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-4s %-58s %s" % ("OK" if cond else "FAIL", label, detail))
    if not cond:
        FAIL.append(label)


def call_of(KA, KAB, d, H):
    return A.season_call(KA, KAB, d, H)[0]


def main():
    F, M, gas_block = A.figures(TARGET)
    T = M["T"]
    H, KA, KAB = M["H"], M["KA"], M["KAB"]
    w = W.build()
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TARGET))
    tg = A.tg_by_day(T)
    cold = {d for d, t in tg.items() if t <= 0.0}

    # ------------------------------------------------------------------ G: input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = Counter(f.rsplit(".", 1)[1] for f in files)
    ok("G2 three or more formats", len(fmts) >= 3, dict(fmts))
    ok("G3 a file of 25,000 rows or more", len(T["amr"]) >= 25000, "%d AMR rows" % len(T["amr"]))
    ok("G4 two or more distractors named in metadata", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]), meta["distractor_files"])
    bad_names = [f for f in files if re.search(r"readme|dictionar|notes|manifest|schema|test_|trap|decoy|distract", f, re.I)]
    ok("G5 no file names the data or the author's intent", not bad_names, bad_names or "clean")
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            import openpyxl
            sheets += [(f, s) for s in openpyxl.load_workbook(os.path.join(TARGET, f)).sheetnames]
    bad_sheets = [s for s in sheets if re.search(r"readme|toelichting|notes|legend|dictionar|uitleg|info", s[1], re.I)]
    ok("G6 no sheet describes the data", not bad_sheets, "%d sheets" % len(sheets))
    ok("G7 every file has source, date and licence", all(set(meta["files"][f]) >= {"source", "date", "license"}
                                                         for f in files), "")
    ok("G8 one deliverable, named in the prompt", meta["deliverables"] == ["os_west_debiet_2027-2029.xlsx"] and
       "os_west_debiet_2027-2029.xlsx" in open(os.path.join(TASK, "prompt.txt")).read(), meta["deliverables"])

    # ------------------------------------------------------------------ R1: the field's raw material ships
    amr_cols = list(T["amr"][0].keys())
    ok("R1a meter readings carry supply, return, energy and volume per day",
       all(c in amr_cols for c in ("t_aanvoer_gem_c", "t_retour_gem_c", "energie_kwh", "volume_m3")), amr_cols[:6])
    heads = []
    for f in files:
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().split(";" if ";" in open(p).readline() else ",")
        elif f.endswith(".xlsx"):
            import openpyxl
            for ws in openpyxl.load_workbook(p):
                for r in ws.iter_rows(max_row=5, values_only=True):
                    heads += [str(x) for x in r if isinstance(x, str)]
    cols = [h for h in heads if " " not in h.strip()]          # column names, not title or subtitle lines
    hit = [h for h in cols if re.search(r"delta|verschil|\bdt\b|drop|debiet_ontwerp|ontwerpdebiet|regime|radiator", h, re.I)]
    ok("R1b no column holds a drop, a regime or a design flow", not hit, hit or "none")
    like = set(M["like"])
    reg_cols = ["wijk", "categorie", "object"]
    leaks = []
    for col in reg_cols + ["bouwjaar_decade", "aansluitjaar", "objectsoort"]:
        groups = defaultdict(set)
        for c in T["conns"]:
            if col == "bouwjaar_decade":
                v = int(c["bouwjaar"]) // 10
            elif col == "aansluitjaar":
                v = A.asdate(c["aansluitdatum"]).year
            elif col == "objectsoort":
                v = str(c["object"]).split(" ")[0]
            else:
                v = c[col]
            groups[v].add(c["aansluitnummer"])
        for v, ids in groups.items():
            if ids & like and ids <= like and len(ids) > 1:
                leaks.append((col, v))
    ok("R1c the like installations are no union of any register value", not leaks, leaks or "every value mixes regimes")
    truth_ht = {c["nr"] for c in w["conns"] if c["regime"] == "HT"}
    ok("R1d the regime read from the readings is the clean truth's", like == truth_ht, "%d of %d" % (len(like & truth_ht),
                                                                                                   len(truth_ht)))

    # ------------------------------------------------------------------ R2: Layer 1 present, and neutral to the call
    units = {r["eenheid"] for r in T["legacy"]}
    ok("R2a two reading systems (drive-by GJ and MWh, AMR kWh)", units == {"GJ", "MWh"}, units)
    per0 = A.per_connection(T, 0.0)
    shift = A.per_connection(T, 0.0, shift=-1)
    d_shift = A.pooled(shift, list(like), M["kw"], "mean")
    ok("R2b UTC days against local weather days: same call", call_of(KA, KAB, d_shift, H) == F["call"],
       "%.2f K" % d_shift)
    ex = [c for c in w["conns"] if c.get("exchange26")]
    ok("R2c summer 2026 meter exchanges, none on a cold day", len(ex) == 7 and all(c["exchange26"][0] not in cold for c in ex),
       "%d exchanges" % len(ex))
    gaps = sum(len(c["gaps"]) for c in w["conns"])
    gap_cold = sum(1 for c in w["conns"] for d in c["gaps"] + c["firstback"] + c["tfault"] if d in cold)
    ok("R2d AMR gaps and temperature faults exist, none on a cold day", gaps > 50 and gap_cold == 0,
       "%d gap days, %d on cold days" % (gaps, gap_cold))
    cold_whole = {d for d, t in tg.items() if t * 10 <= 0}
    ok("R2e TG in tenths: read as whole degrees the window is the same", cold_whole == cold, "%d days" % len(cold))
    con = A.concept_loads(T)
    ok("R2f concept and rev2 differ for every block", all(con[b["code"]] != b["load"] for b in M["loads"]), "")
    re_eans = [g for g in T["gas_conn"] if g["status"] == "beeindigd"]
    exch = [m for m in T["gas_meters"] if m["reden"] == "vervangingsprogramma 2025-2026"]
    ok("R2g gas EAN re-registrations and meter exchanges", len(re_eans) == 2 and len(exch) == 4,
       "%d re-registered, %d exchanged" % (len(re_eans), len(exch)))
    dups = Counter(tuple(r.values()) for r in T["gasreads"])
    ok("R2h one resent gas read, an exact duplicate", sum(1 for v in dups.values() if v > 1) == 1, "")
    regs = [m for m in T["meters"] if m["uitlezing"] == "drive-by"]
    ok("R2i the register maps every AMR serial to one connection at any date", all(len(set(a for a, g, v in x)) == 1
       for x in A.serial_owner(T).values()), "%d legacy meters removed at migration" % len(regs))

    # ------------------------------------------------------------------ R3: the three rules on the clean truth
    docs = {k: A.pdf_text(os.path.join(TARGET, P.FILES[k])) for k in ("procedure", "hydraulic", "tariff", "prelim")}
    z = zipfile.ZipFile(os.path.join(TARGET, P.FILES["scope"]))
    scope_txt = re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8"))
    for k, txt in list(docs.items()) + [("scope", scope_txt)]:
        num_k = re.findall(r"\b(\d{2}(?:\.\d)?)\s*K\b", txt)
        ok("R3a no drop figure for the blocks in %s" % k, k == "hydraulic" or not num_k, num_k or "none")
    filed = docs["procedure"] + " " + docs["hydraulic"]
    named = [t for t in ("return temperature", "radiator", "regime", "comparable", "similar", "build year", "bouwjaar",
                         "renovat", "original") if t in filed.lower()]
    ok("R3c no filed sentence names a regime, a return temperature, a build year or which connections share the installation", not named, named or "none")
    ok("R3c' the scope files the blocks' installation (original radiators sized for 90/70) and no connection's drop",
       "original two-pipe radiators" in scope_txt and "90" in scope_txt and "70" in scope_txt and
       not any(t in scope_txt.lower() for t in ("connections in service", "metered drop", "high return", "regime",
                                                 "temperature difference")), "")
    # clean truth: the default family with the regime hidden
    kw = {c["nr"]: c["kw"] for c in w["conns"]}
    by = {c["nr"]: c["bouwjaar"] for c in w["conns"]}
    defaults = {"design 40 K": 40.0, "network flow-weighted": M["net"][("ALL", "flow")]}
    defaults.update({"pre-1985 %s %s" % k: v for k, v in M["pre"].items()})
    defaults.update({"network %s %s" % k: v for k, v in M["net"].items()})
    calls = {k: call_of(KA, KAB, v, H) for k, v in defaults.items()}
    ok("R3b analyst test: every default route files none", all(v == "none" for v in calls.values()),
       Counter(calls.values()))
    ok("R3b' the golden route files 2028-29", F["call"] == "2028-29", F["call"])
    ok("R3b'' the textbook radiator regime (20 K) files 2027-28", call_of(KA, KAB, 20.0, H) == "2027-28", "")

    # ------------------------------------------------------------------ SF: the semantic fork table
    gfam = list(M["fam"].values())
    ok("SF1 another heat capacity (1.16, 4.19 kJ/kg K) gives the same call",
       all(A.season_call(KA, KAB, d * cpx / A.CP, H)[0] == "2028-29" for d in gfam for cpx in (1.16, 4.19 / 3.6)), "")
    ok("SF2 every window from -2 to +2 C gives 2028-29", all(call_of(KA, KAB, v, H) == "2028-29" for k, v in
                                                           M["fam"].items() if k[0] == "T"), "")
    ok("SF3 energy over volume gives 2028-29", all(call_of(KA, KAB, v, H) == "2028-29" for k, v in M["fam"].items()
                                                  if k[0] == "E"), "")
    ok("SF4 a day's shift gives 2028-29", call_of(KA, KAB, M["wide"][("shift", "mean")], H) == "2028-29",
       "%.2f K" % M["wide"][("shift", "mean")])
    ok("SF5 the station's supply gives 2028-29", all(call_of(KA, KAB, v, H) == "2028-29" for k, v in M["wide"].items()
                                                    if k[0] == "stn"), "%.2f to %.2f K" % (
        min(v for k, v in M["wide"].items() if k[0] == "stn"), max(v for k, v in M["wide"].items() if k[0] == "stn")))
    ok("SF6 every pooling gives 2028-29", all(call_of(KA, KAB, v, H) == "2028-29" for v in gfam),
       "%.2f to %.2f K" % (min(gfam), max(gfam)))
    ok("SF7 the concept loads give the same call", call_of(M["KA_concept"], M["KAB_concept"], F["drop_K"], H) == "2028-29",
       "%d and %d kW" % (M["KA_concept"], M["KAB_concept"]))
    ok("SF8 every phase connects before 1 October of its season", all(
        b["date"] < (dt.date(2027, 10, 1) if b["phase"] <= 3 else dt.date(2028, 10, 1)) and
        b["date"] >= (dt.date(2027, 4, 1) if b["phase"] <= 3 else dt.date(2028, 4, 1)) for b in M["loads"]), "")
    ok("SF9 the procedure adds loads at full value", "added at full value" in docs["procedure"].replace("  ", " "), "")
    ok("SF10 the available flow is the hydraulic test's", re.search(r"=\s*%d\s*m" % H, docs["hydraulic"]) is not None, H)
    mr = M["returns"]
    lo_gap, hi_gap = M["gap"]
    sets = {thr: {nr for r, nr in mr if r > thr} for thr in np.arange(lo_gap + 0.1, hi_gap, 0.5)}
    res_like = {nr for nr in like if M["cat"][nr] == "Woningen"}
    ok("SF11 any threshold in the gap and the residential subset give one set",
       all(s == like for s in sets.values()) and res_like == like, "gap %.1f to %.1f C" % (lo_gap, hi_gap))
    ok("SF12 unrounded and rounded flows give the same call", (F["flow_2027_28"] < H) == (F["flow_2027_28_exact"] < H)
       and (F["flow_2028_29"] > H) == (F["flow_2028_29_exact"] > H), "")
    own = sum(b["load"] for b in M["loads"] if b["phase"] >= 4) / (A.CP * F["drop_K"])
    ok("SF13 the procedure files the cumulative season test", "connected by the start of that season" in
       docs["procedure"].replace("  ", " ") and own < H, "phases 4 to 6 alone %.1f m3/h" % own)
    reads_by = defaultdict(set)
    for r in T["gasreads"]:
        reads_by[r["ean"]].add(r["tijdstip"][:16])
    act = [str(g["ean"]) for g in T["gas_conn"] if g["status"] == "actief"]
    ok("SF14 every active EAN has its 06:00 reads on 1 October 2025 or its start, and 1 October 2026",
       all("2026-10-01T06:00" in reads_by[e] for e in act), "")
    h1, h2 = A.heat_by_category(T)
    # the register on a daily row is the reading at the end of that UTC day: each row's register less the previous
    # row's equals its energy wherever the two days are consecutive, so the 1 October 2025 reading is the first row's
    # register less its energy (a day-late boundary contradicts the export's own arithmetic)
    prev, bad, n_pairs = {}, 0, 0
    for r in sorted(T["amr"], key=lambda r: (r["meternummer"], r["datum_utc"])):
        p = prev.get(r["meternummer"])
        if p and r["energie_kwh"] and (D(r["datum_utc"]) - D(p["datum_utc"])).days == 1:
            n_pairs += 1
            if int(r["telwerk_energie_kwh"]) - int(p["telwerk_energie_kwh"]) != int(r["energie_kwh"]):
                bad += 1
        prev[r["meternummer"]] = r
    ok("SF15 each row's register is the end of its UTC day (register steps equal the day's energy)", bad == 0,
       "%d consecutive pairs" % n_pairs)
    ok("SF16 categories are the register's two values", set(M["cat"].values()) == {"Woningen", "Utiliteit"}, "")
    # CT-03 3.2 files the comparison group (connections in service with the same kind of heating installation); the
    # literal reader with each easy route's inputs does not comply, and the group's members are found only in the data
    regime = {c_["nr"]: c_["regime"] for c_ in w["conns"]}
    pre_set = {i for i in M["kw"] if M["by"][i] < 1985}
    filed32 = "same kind of heating installation" in docs["procedure"].replace("  ", " ")
    ok("SF17 the same kind of heating installation: the filed comparison, met only by the original-radiator group",
       filed32 and all(regime[i] == "HT" for i in like) and any(regime[i] == "REN" for i in pre_set) and
       any(regime[i] != "HT" for i in M["kw"]) and call_of(KA, KAB, 20.0, H) == "2027-28",
       "pre-1985 holds %d renovated blocks; the design drop of 20 K files 2027-28" %
       sum(1 for i in pre_set if regime[i] == "REN"))
    newc = [c_ for c_ in T["conns"] if A.asdate(c_["aansluitdatum"]) >= dt.date(2024, 9, 1) and c_["categorie"] == "Woningen"]
    like_for_like = {k: 0.0 for k in ("Woningen",)}
    filed_pop = "over every connection in the register" in docs["hydraulic"].replace("  ", " ")
    prompt_txt = open(os.path.join(TASK, "prompt.txt")).read()
    ok("SF18 the heat ask's population is every connection in the register (filed and in the prompt)",
       filed_pop and "every residential and every utility connection" in prompt_txt and len(newc) >= 1,
       "%d residential connections went live from September 2024" % len(newc))

    # ------------------------------------------------------------------ F: cheap routes
    routes = dict(defaults)
    routes["textbook 90/70"] = 20.0
    routes["regression on build year"] = M["pre"][("REG", "1962-1971")]
    landing = [k for k, v in routes.items() if call_of(KA, KAB, v, H) == "2028-29"]
    ok("F1 no cheap route lands 2028-29", not landing, landing or "%d routes, none" % len(routes))
    ok("F2 every licensed like-installation member lands 2028-29", all(call_of(KA, KAB, v, H) == "2028-29" for v in gfam), "")
    p_lo = min(M["pre"].values())
    ok("F3 margins: rung 2 under, golden over, 2027-28 holds, textbook over",
       KAB / (A.CP * p_lo) <= H / 1.06 and KAB / (A.CP * max(gfam)) >= 1.08 * H and KA / (A.CP * min(gfam)) <= H / 1.08
       and KA / (A.CP * 20.0) >= 1.06 * H,
       "rung 2 %.1f, golden %.1f to %.1f and %.1f to %.1f, textbook %.1f m3/h" % (
           KAB / (A.CP * p_lo), KA / (A.CP * max(gfam)), KA / (A.CP * min(gfam)), KAB / (A.CP * max(gfam)),
           KAB / (A.CP * min(gfam)), KA / (A.CP * 20)))

    cy = {c["aansluitnummer"]: A.asdate(c["aansluitdatum"]).year for c in T["conns"]}
    blk = [b["load"] for b in M["loads"]]
    pre_ids = [i for i in M["kw"] if M["by"][i] < 1985]
    filters = {"kW >= %d" % k: [i for i in pre_ids if M["kw"][i] >= k] for k in (250, 300, 350, 400, 450)}
    filters["the blocks' kW range"] = [i for i in pre_ids if min(blk) <= M["kw"][i] <= max(blk)]
    filters["built 1960 to 1972"] = [i for i in pre_ids if 1960 <= M["by"][i] <= 1972]
    filters["connected by 2012"] = [i for i in pre_ids if cy[i] <= 2012]
    filters["connected by 2015"] = [i for i in pre_ids if cy[i] <= 2015]
    land4 = [(k, how) for k, ids in filters.items() for how in ("mean", "median", "harm")
             if call_of(KA, KAB, A.pooled(per0, ids, M["kw"], how), H) != "none"]
    ok("F4 no size, age or connection-year filter of the pre-1985 connections lands a season", not land4,
       land4 or "%d filters x 3 poolings, all none" % len(filters))

    # ------------------------------------------------------------------ B: bin edges under every licensed member
    def edge(vals, unit):
        rs = {A.rnd(v, unit) for v in vals}
        return len(rs) == 1, min(W.dist_to_edge(v, unit) for v in vals)
    for ph in range(1, 7):
        vals = [M["phase_load"][ph] / (A.CP * d) for d in gfam]
        same, dist = edge(vals, 5)
        ok("B1 phase %d flow in one nearest-5 bin" % ph, same and dist >= 0.8 and A.rnd(vals[0], 5) == F["phase_flow"][str(ph)],
           "%d m3/h, %.2f from the edge" % (F["phase_flow"][str(ph)], dist))
    for name, K, key in (("2027-28", KA, "flow_2027_28"), ("2028-29", KAB, "flow_2028_29")):
        vals = [K / (A.CP * d) for d in gfam]
        same, dist = edge(vals, 10)
        ok("B2 %s flow in one nearest-10 bin" % name, same and dist >= 1.25 and A.rnd(vals[0], 10) == F[key],
           "%d m3/h, %.2f from the edge" % (F[key], dist))
    vals = [KAB / (A.CP * d) - H for d in gfam]
    same, dist = edge(vals, 10)
    ok("B2 shortfall in one nearest-10 bin", same and dist >= 1.25, "%d m3/h, %.2f from the edge" %
       (F["shortfall_2028_29"], dist))
    ok("B3 the drop is about 24 K under every member", {A.rnd(d, 1) for d in gfam} == {24},
       "%.2f to %.2f K" % (min(gfam), max(gfam)))
    for ph in range(1, 7):
        v = F["gas_m3_exact"][str(ph)]
        ok("B4 gas phase %d clears its rounding edge" % ph, W.dist_to_edge(v, 1000) >= 200, "%d m3, %.0f from the edge" %
           (v, W.dist_to_edge(v, 1000)))
    for k, u in (("Woningen", 1000), ("Utiliteit", 100)):
        d1 = W.dist_to_edge(h1[k], u)
        d2 = W.dist_to_edge(h2[k] - h1[k], u)
        ok("B5 heat %s 2024-25 and change clear their edges" % k, d1 >= 0.08 * u and d2 >= 0.08 * u,
           "%.1f and %.1f MWh from the edges" % (d1, d2))

    # ------------------------------------------------------------------ M: the call's population and the ask devices
    tmp = tempfile.mkdtemp()
    for f in files:
        if not (f.startswith("gas_") or f.startswith("meterstam") or f.startswith("driveby")):
            shutil.copy(os.path.join(TARGET, f), tmp)
    for f in files:
        if f.startswith("gas_") or f.startswith("meterstam") or f.startswith("driveby"):
            open(os.path.join(tmp, f), "w").close()
    try:
        Mx = A.main_call(tmp, A.load_main_only(tmp))
        same_call = Mx["call"] == M["call"] and abs(Mx["golden_d"] - M["golden_d"]) < 1e-9
    finally:
        shutil.rmtree(tmp)
    ok("M1 the call reads no gas or drive-by file", same_call, "")
    dev_cold = [r for r in T["amr"] if D(r["datum_utc"]) in cold and (r["status"] != "V" or r["energie_kwh"] == "")]
    ok("M2 zero device or hazard rows on a cold day", not dev_cold, "%d" % len(dev_cold))
    sched_eans = {b["ean"] for b in M["loads"]}
    ok("M3 the re-registered EANs are absent from the schedule", all(str(g["ean"]) not in sched_eans for g in re_eans), "")
    tele = {(r["ean"], r["meternummer"], r["soort"]) for r in T["gasreads"]}
    ok("M4 exchanged meters' closing and opening readings live in the master data only",
       all(not any(t[1] == str(m["meternummer"]) and t[2] in ("E", "B") for t in tele) for m in exch), "")

    # ------------------------------------------------------------------ A: the ask layer
    pair, leak, figs = C.main(TARGET)
    ok("A1 the cracker misses every ask figure", not any(h for _, h in figs), "%d figures" % len(figs))
    gas_full, _ = A.gas_by_phase(T, M["loads"])
    ok("A2 the full includer hits every figure", all(A.rnd(gas_full[ph], 1000) == F["gas_m3"][str(ph)] for ph in range(1, 7)), "")
    ext = C.extrapolating_heat(T)
    ext_hits = [k for k, u in (("Woningen", 1000), ("Utiliteit", 100)) if A.rnd(ext[k], u) == F["heat_2425_MWh"][k]]
    ok("A3 an extrapolating cracker misses the 2024-25 heat", not ext_hits, {k: round(v, 1) for k, v in ext.items()})
    ok("A4 pair ceiling at most 60, mirror leakage under 50", pair <= 60 and leak < 50, "%.1f, %.1f" % (pair, leak))

    # ------------------------------------------------------------------ S: realism sweep
    ok("S1 the available flow is not a multiple of 5", H % 5 != 0, H)
    daily = defaultdict(list)
    for r in T["amr"]:
        if r["energie_kwh"]:
            daily[r["meternummer"]].append(float(r["energie_kwh"]))
    ok("S2 no constant meter stream", all(np.std(v) > 0 for v in daily.values()), "%d meters" % len(daily))
    tots = Counter(round(sum(v)) for v in daily.values())
    ok("S3 no identical meter totals", max(tots.values()) == 1, "")
    sig = []
    for f in files:
        raw = open(os.path.join(TARGET, f), "rb").read()
        if f.endswith((".xlsx", ".docx")):
            zz = zipfile.ZipFile(os.path.join(TARGET, f))
            raw = b"".join(zz.read(n) for n in zz.namelist() if n.startswith("docProps"))
        for s_ in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab"):
            if s_ in raw:
                sig.append((f, s_))
    ok("S4 containers scrubbed of the toolchain", not sig, sig or "clean")
    late = [r["datum_utc"] for r in T["amr"] if r["datum_utc"] > "2026-09-30"]
    ok("S5 no reading after the meter year", not late, "")
    by_wijk = defaultdict(set)
    for c in T["conns"]:
        if int(c["bouwjaar"]) < 1985:
            by_wijk[c["wijk"]].add(c["aansluitnummer"] in like)
    ok("S6 both pre-1985 kinds in every older wijk", all(v == {True, False} for v in by_wijk.values()),
       {k: sorted(v) for k, v in by_wijk.items()})
    yrs = sorted((int(c["bouwjaar"]), c["aansluitnummer"] in like) for c in T["conns"] if int(c["bouwjaar"]) < 1985)
    runs = sum(1 for i in range(1, len(yrs)) if yrs[i][1] != yrs[i - 1][1])
    ok("S7 the like installations interleave with the rest by build year", runs >= 10, "%d alternations" % runs)
    people = set(P.PEOPLE.values())
    ok("S8 personas are the drawn names", people == {"Elif Meeusen", "Maurits Weijland", "Stella Gnodde"}, "")
    ok("S9 em dashes absent from the pack's text files and the write-up",
       not any("—" in open(os.path.join(TARGET, f), encoding="utf-8").read() for f in files if f.endswith(".csv"))
       and "—" not in open(os.path.join(TASK, "submission.md")).read(), "")

    # the heat cells under every reading of the gas-year boundaries: the 1 October 2024 annual read taken at any time
    # of that day (00:00 to 24:00, the read itself at its stamped time), the 1 October 2025 boundary at local midnight
    # rather than the AMR's 00:00 UTC; and the day-late slip (the first AMR row's register as the opening) lands wrong
    for k, u, lim in (("Woningen", 1000, 150), ("Utiliteit", 100, 15)):
        cs = [cc for cc in w["conns"] if cc["cat"] == k]
        e1 = sum(cc["cons_oct1_2024"] for cc in cs) / 1000.0
        two_h = sum(cc["cons_sep30_2025"] for cc in cs) / 1000.0 * 2 / 24
        R, C_ = h1[k], h2[k] - h1[k]
        vR = [R, R + 0.42 * e1, R - 0.58 * e1, R - two_h]
        vC = [C_, C_ - 0.42 * e1, C_ + 0.58 * e1, C_ + two_h]
        mR = min(W.dist_to_edge(v, u) for v in vR)
        mC = min(W.dist_to_edge(v, u) for v in vC)
        ok("H1 %s 2024-25 heat holds its bin under every boundary reading" % k,
           len({A.rnd(v, u) for v in vR}) == 1 and A.rnd(R, u) == F["heat_2425_MWh"][k] and mR >= lim,
           "%d MWh, %.1f from the edge at worst" % (F["heat_2425_MWh"][k], mR))
        ok("H2 %s change holds its bin under every boundary reading" % k,
           len({A.rnd(v, u) for v in vC}) == 1 and A.rnd(C_, u) == F["heat_change_MWh"][k] and mC >= lim,
           "%+d MWh, %.1f from the edge at worst" % (F["heat_change_MWh"][k], mC))
        ok("H3 %s 2025-26 heat sits well inside its bin" % k, W.dist_to_edge(h2[k], u) >= (300 if u == 1000 else 25),
           "%.1f MWh, %.1f from the edge" % (h2[k], W.dist_to_edge(h2[k], u)))
    slip = first_day_energy(T, M)
    ok("H4 the day-late slip lands wrong on the residential change",
       A.rnd(h2["Woningen"] - h1["Woningen"] - 2 * slip["Woningen"], 1000) != F["heat_change_MWh"]["Woningen"],
       "slip %.1f MWh a side" % slip["Woningen"])
    tm = {r["opnametijd"] for r in T["legacy"]}
    ok("H5 the drive-by reads carry the reading system's clock time", all(re.fullmatch(r"\d{2}:\d{2}", t) for t in tm),
       "%d distinct times" % len(tm))

    rv = T["rev2"]
    sums = all(int(r["transmissie_kw"]) + int(r["ventilatie_kw"]) + int(r["opwarmtoeslag_kw"]) ==
               int(r["ontwerpwarmteverlies_kw"]) for r in rv)
    truth_loads = {b["code"]: b["load"] for b in w["blocks"]}
    same_tot = all(int(r["ontwerpwarmteverlies_kw"]) == truth_loads[str(r["complex"]).replace("WH", "")] for r in rv)
    vr = [int(r["ventilatie_kw"]) / int(r["transmissie_kw"]) for r in rv]
    hr = [int(r["opwarmtoeslag_kw"]) / int(r["transmissie_kw"]) for r in rv]
    ok("S10 rev2 components sum to each block's design heat loss, the totals unchanged",
       sums and same_tot and KA == 4240 and KAB == 5533, "%d rows, %d and %d kW" % (len(rv), KA, KAB))
    ok("S11 rev2 components vary block by block (ventilation and heating-up shares of transmission)",
       max(vr) - min(vr) >= 0.15 and max(hr) - min(hr) >= 0.10 and
       len({(round(a, 3), round(b, 3)) for a, b in zip(vr, hr)}) == len(rv),
       "ventilation %.3f to %.3f, heating-up %.3f to %.3f of transmission" % (min(vr), max(vr), min(hr), max(hr)))
    print("%d checks, %d failed" % (N[0], len(FAIL)))
    return 1 if FAIL else 0


def D(s):
    return dt.date.fromisoformat(s)


def first_day_energy(T, M):
    owner = {str(m["meternummer"]): m["aansluitnummer"] for m in T["meters"]}
    out = defaultdict(float)
    for r in T["amr"]:
        if r["datum_utc"] == "2025-10-01" and r["energie_kwh"]:
            out[M["cat"][owner[r["meternummer"]]]] += float(r["energie_kwh"]) / 1000.0
    return out


if __name__ == "__main__":
    sys.exit(main())
