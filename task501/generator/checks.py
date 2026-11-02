"""task501 checks: the input gates, the three rules on the clean truth (R1 to R3c), the ladder, every semantic fork
row (SF1 to SF19), the lesson 7 and lesson 12 assertions, both ask layers' devices with their cracker, over-cleaner and
full includer, the realism sweep, the documents' pins and positive controls, and the distractor deletion test. Every
figure is read back from the shipped files through bundle.py and solve.py; the truth is used only where a rule asks
for the clean truth."""
import datetime as dt
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import bundle as B
import net as N
import pack as PK
import solve as S
import world as W


class Gate:
    def __init__(self):
        self.rows = []

    def ok(self, label, cond, detail=""):
        self.rows.append((label, bool(cond), detail))
        print("%s  %-62s %s" % ("PASS" if cond else "FAIL", label, detail))

    def finish(self):
        bad = [r for r in self.rows if not r[1]]
        print("CHECKS   %d assertions, %d failed" % (len(self.rows), len(bad)))
        if bad:
            raise SystemExit("checks failed: " + ", ".join(r[0] for r in bad))


def _edge0(x):
    """Distance of x from the nearest whole-number rounding edge (x.5)."""
    return abs((x % 1.0) - 0.5)


def _edge1(x):
    return abs(((x * 10) % 1.0) - 0.5) / 10.0


def _truth_ref(tr, keys):
    tl = N.timeline(keys)
    op, _ = N.operated_flows(tr["dem"], tl, tr["dark"])
    return {m: float(op[m].max()) for m in W.MAINS}


def _truth_set(tr, ref):
    pk = {m: float(tr["plan"][m].max()) for m in W.MAINS}
    return sorted(W.MAIN_ID[m] for m in W.CANDIDATES if pk[m] > ref[m])


def run(target, gold, tr, info, res, figs):
    g = Gate()
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json"), encoding="utf-8"))

    # ------------------------------------------------------------------------------------------ input gates
    g.ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    g.ok("G2 three or more formats", len(fmts) >= 3, ", ".join(fmts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    g.ok("G3 a file of 25,000 or more rows", big >= 25000, "%d rows" % big)
    g.ok("G4 two or more distractors named in metadata and shipped", len(meta["distractor_files"]) >= 2 and all(
        d in files for d in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    bad_names = [f for f in files if re.search(r"readme|dictionar|codebook|manifest|schema|notes|field|distractor|"
                                               r"glossary|how_to", f, re.I)]
    g.ok("G5 no file named as a description of the data", not bad_names, ", ".join(bad_names) or "none")
    import openpyxl
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames
    g.ok("G6 no sheet that describes the data", not [s for s in sheets if re.search(
        r"note|readme|dictionar|about|field|legend|key", s, re.I)], ", ".join(sheets))
    g.ok("G7 metadata names no method vocabulary", not re.search(
        r"operated|arrangement|valve position|condition(ed|ing)|running register|twin|standpipe|mass balance|"
        r"supplied from|neighbour|impossib", json.dumps(meta), re.I), "metadata.json")

    # ------------------------------------------------------------------------------------------ three rules
    inflow, finfo = B.flows(target)
    mains_reg, valves_reg, dmas_reg = B.register(target)
    main_ids = {m["Main"] for m in mains_reg}
    g.ok("R1 the district meters ship hourly at the district grain", set(inflow.columns) == {d["DMA"] for d in dmas_reg}
         and len(inflow) == 8760, "%d districts x %d hours" % (inflow.shape[1], inflow.shape[0]))
    headers = []
    for f in files:
        if f.endswith(".csv"):
            headers += open(os.path.join(target, f), encoding="utf-8").readline().strip().lower().split(",")
    g.ok("R1 no shipped column holds a trunk main's flow", not [h for h in headers if re.search(r"trunk|main_flow|tm\d",
                                                                                                h)]
         and not (set(pd.read_csv(os.path.join(target, PK.FILES["flows"]), usecols=["dma"])["dma"]) & main_ids),
         "%d csv columns" % len(headers))
    ref_all = {m: float(tr["op"][m].max()) for m in W.MAINS}
    ref_static = {m: float(tr["static"][m].max()) for m in W.MAINS}
    gold_set = sorted(res_id for res_id in figs["flush"])
    t_default = _truth_set(tr, ref_static)
    g.ok("R3a analyst test on the clean truth: the normal arrangement flushes six", t_default == sorted(
        W.MAIN_ID[m] for m in W.CANDIDATES), ", ".join(t_default))
    t_gold = _truth_set(tr, ref_all)
    g.ok("R3b the decisive step alone on the clean truth files the golden", t_gold == gold_set == sorted(
        W.MAIN_ID[m] for m in W.GOLDEN_FLUSH), ", ".join(t_gold))
    t_burst = _truth_set(tr, _truth_ref(tr, {"july_t04"}))
    t_planned = _truth_set(tr, _truth_ref(tr, {e["key"] for e in W.EVENTS if e["key"] != "july_t04"}))
    t_june = _truth_set(tr, _truth_ref(tr, {"june_t04"}))
    g.ok("R3b each single correction short of the step stays wrong", len(t_burst) == 5 and len(t_planned) == 3 and
         len(t_june) == 3 and t_gold not in (t_burst, t_planned, t_june),
         "bursts only %d, planned only %d, June job only %d" % (len(t_burst), len(t_planned), len(t_june)))
    days = {}
    dup_days = 0
    for d in inflow.columns:
        v = inflow[d].values
        for k in range(0, len(v) - 24, 24):
            key = tuple(np.round(v[k:k + 24], 2))
            if np.isnan(v[k:k + 24]).any():
                continue
            if key in days:
                dup_days += 1
            days[key] = (d, k)
    g.ok("R3c no copied block: no district-day repeats another", dup_days == 0, "%d district-days" % len(days))
    docs_text = {k: B.pdf_text(target, k) for k in ("standard", "plan", "condition")}
    four = ["TM104", "TM109", "TM110", "TM112"]
    g.ok("R3c no document names a main the call turns on outside the register", not any(
        m in docs_text[k] for m in four for k in ("standard", "plan")), "standard and plan")
    g.ok("R3c no memo, proposal, risk assessment or prior assessment ships", not [f for f in files if re.search(
        r"memo|proposal|risk|assessment_2026|podds|model|flushing_plan|affected", f, re.I)], "file names")

    # ------------------------------------------------------------------------------------------ the ladder on the pack
    c = S.call(target)
    rungs = {}
    for model in ("normal", "bursts", "planned"):
        rungs[model] = S.call(target, model=model)["flush"]
    cand = c["rises"]
    typical = c["N0"][c["ok"].values].groupby(c["N0"][c["ok"].values].index.date).max().median()
    r1 = [m for m in cand if c["peak"][m] > typical[m]]
    g.ok("L0 any rise: six mains", len(cand) == 6, ", ".join(cand))
    g.ok("L1 above the typical daily peak: six", len(r1) == 6, ", ".join(r1))
    g.ok("L2 the default (normal arrangement): six", rungs["normal"] == cand, ", ".join(rungs["normal"]))
    g.ok("L3 bursts rebuilt, planned jobs as normal: five", len(rungs["bursts"]) == 5, ", ".join(rungs["bursts"]))
    g.ok("L3b planned jobs rebuilt, the burst as normal: three", len(rungs["planned"]) == 3, ", ".join(rungs["planned"]))
    g.ok("L4 the golden: two (TM112, IC05)", c["flush"] == ["IC05", "TM112"], ", ".join(c["flush"]))
    ratio = {m: (c["peak"][m] / c["ref"][m] if c["ref"][m] > 0 else np.inf) for m in cand}
    g.ok("L5 no main within 8 per cent of its reference", all(abs(r - 1) >= 0.08 for r in ratio.values()),
         ", ".join("%s %.3f" % (m, r) for m, r in ratio.items()))
    stats = {"works peak": {m: c["peak"][m] for m in cand}, "normal peak": {m: c["normal_peak"][m] for m in cand},
             "relative rise": {m: (c["peak"][m] / c["normal_peak"][m] if c["normal_peak"][m] > 0 else 1e9) for m in cand},
             "diameter": {m: float(c["net"].mains[m]["DN (mm)"]) for m in cand},
             "year laid": {m: float(c["net"].mains[m]["Laid"]) for m in cand},
             "length": {m: float(c["net"].mains[m]["Length (m)"]) for m in cand}}
    hits = [n for n, st in stats.items() for k in (2,) for top in (sorted(st, key=st.get)[:k], sorted(st, key=st.get)[-k:])
            if sorted(top) == c["flush"]]
    g.ok("L6 the pair is no top or bottom pair of a shipped statistic", not hits, ", ".join(hits) or "none of %d" % len(stats))
    rise = {m: c["peak"][m] - c["normal_peak"][m] for m in cand}
    top3 = sorted(rise, key=rise.get)[-3:]
    g.ok("L6 by rise in peak the pair sits inside a top three within 5 l/s", set(c["flush"]) < set(top3) and
         max(rise[m] for m in top3) - min(rise[m] for m in top3) < 5.0,
         ", ".join("%s %.1f" % (m, rise[m]) for m in top3))

    # ------------------------------------------------------------------------------------------ semantic forks
    std = docs_text["standard"]
    g.ok("SF1 interconnectors are trunk mains (NOS 12 3.1) and two of them rise", "The register's interconnectors are "
         "trunk mains." in std and {"IC03", "IC05"} <= set(cand), "filed sentence present")
    daily = {}
    for nm, F_ in (("ref", c["F"][c["ok"].values]), ("peak", c["P"][c["use"]])):
        daily[nm] = F_.groupby(F_.index.date).mean().max()
    flush_daily = [m for m in cand if daily["peak"][m] > daily["ref"][m]]
    g.ok("SF2 hourly flow filed; daily means give the same call", "hourly flow" in std and flush_daily == c["flush"],
         ", ".join(flush_daily))
    when = {m: c["F"][c["ok"].values][m].idxmax() for m in cand if c["ref"][m] > 0}
    g.ok("SF3 every reference peak falls in January to October 2026", all(
        pd.Timestamp("2026-01-01") <= t < pd.Timestamp("2026-11-01") for t in when.values()),
        ", ".join("%s %s" % (m, t.date()) for m, t in when.items()))
    log = B.valve_log(target)
    t04 = [v["Valve"] for v in valves_reg if v["Main"] == "TM108"]
    shut = log[log["valve_no"].isin(t04) & (log["action"] == "CLOSE")]
    g.ok("SF4 carried: the log shows TM108 shut in June and July 2026, the normal estimate differs there",
         len(shut) == 4 and all(abs(c["F"][m] - c["N0"][m]).max() > 20 for m in ("TM104", "TM109", "TM110", "IC03")),
         "%d closures of TM108's valves" % len(shut))
    up = {m: c["peak"][m] * 1.03 for m in cand}
    g.ok("SF5 the recorded 2026 inflows filed; a 3 per cent growth leaves the call", "recorded hourly inflows for the "
         "same dates a year earlier" in std and [m for m in cand if up[m] > c["ref"][m]] == c["flush"], "4.3 filed")
    g.ok("SF6 strictly higher or not lower: same call", all(abs(c["peak"][m] - c["ref"][m]) > 1.0 for m in cand), "")
    sgn_ok = True
    plan_sign = {}
    for m in W.CANDIDATES:
        sg = tr["sgn"][m][tr["op"][m] > 0.5]
        ps = tr["psgn"].get(m, 1)
        plan_sign[W.MAIN_ID[m]] = ps
        if len(sg) and not np.all(sg == ps):
            sgn_ok = False
    g.ok("SF7 no main the relining loads ran against its works direction in the year", sgn_ok,
         "TM115 and IC02 reversed, neither a candidate")
    for sh in (1, -1):
        cs = S.call(target, shift_hours=sh)
        g.ok("SF8 the log read an hour %s: same call and figures" % ("late" if sh > 0 else "early"),
             cs["flush"] == c["flush"] and all(round(cs["ref"][m]) == round(c["ref"][m]) for m in cand), "")
    cf = S.call(target, gaps="fill")
    g.ok("SF9 blank meter hours filled: same call and figures", cf["flush"] == c["flush"] and all(
        round(cf["peak"][m]) == round(c["peak"][m]) and round(cf["ref"][m]) == round(c["ref"][m]) for m in cand), "")
    pl = B.plan(target)
    tm115 = [v["Valve"] for v in valves_reg if v["Main"] == "TM115"]
    g.ok("SF10 the plan's table shuts TM115 at both ends", sorted(v for v, o in pl["ops"] if o == "Shut" and v in tm115)
         == sorted(tm115), "%d operations read" % len(pl["ops"]))
    g.ok("SF11 the standard and the question name flushing", "shall be flushed before the change is made" in std, "")
    rest = [m for m in sorted(c["net"].mains) if m not in cand]
    g.ok("SF12 every listed main rises in every hour and no other rises in any", rest == [m for m in rest if m in
                                                                                     c["falls_or_same"]], "")

    # ------------------------------------------------------------------------------------------ ask A
    A, adf = S.ask_a(target)
    rows = adf.copy()
    run_rows = rows[(rows["crew"] == W.CREW_DIST) & (rows["night"] >= pd.Timestamp(W.RUNNING_FROM)) &
                    rows.duplicated(["key"])]
    other = rows.drop(run_rows.index)
    rr = (run_rows["vol"] / run_rows["gxt"])
    ro = (other["vol"] / other["gxt"])
    g.ok("SF13 lesson 8: a running reading is 1.3 or more times its flush's gauge flow times minutes",
         rr.min() >= 1.3 and 0.82 <= ro.min() and ro.max() <= 0.96,
         "running rows %d at %.2f and up; others %.2f to %.2f" % (len(run_rows), rr.min(), ro.min(), ro.max()))
    g.ok("SF14 no flushing night crosses a year end", not rows["night"].dt.strftime("%m-%d").eq("12-31").any(), "")
    per, tot = {}, {}
    for (dn, yr), sub in rows.groupby(["dn", "year"]):
        sec = sub.groupby(["night_of", "section_ref"]).agg(w=("w", "sum"), L=("L", "first"))
        per[(dn, yr)] = float((sec["w"] / sec["L"] * 100).mean())
        tot[(dn, yr)] = float(sec["w"].sum() / sec["L"].sum() * 100)
    differ = sum(abs(per[k] - A[k]) > 0.05 for k in A)
    g.ok("SF17 the golden is the literal reading, the programme's water over its metres; the mean of sections' rates "
         "is another number", all(abs(tot[k] - A[k]) < 1e-9 for k in A) and differ >= 1,
         "mean of rates differs in %d of %d cells" % (differ, len(A)))
    twin = rows[rows.duplicated(["night_of", "section_ref"], keep=False)]
    tg = twin.groupby(["night_of", "section_ref"])
    g.ok("A1 twin-hydrant flushes: two rows, one section, one start and finish, two hydrants, 225 and 300 mm only",
         len(twin) > 0 and tg.size().eq(2).all() and tg["start"].nunique().eq(1).all() and tg["finish"].nunique().eq(
             1).all() and tg["hydrant_no"].nunique().eq(2).all() and set(twin["dn"]) == {225, 300},
         "%d sections" % tg.ngroups)
    early = rows[(rows["crew"] == W.CREW_DIST) & (rows["night"] < pd.Timestamp(W.RUNNING_FROM))]
    g.ok("A2 benign twins: crew C14 before December and crew C22's 150 mm rows read as single flushes",
         len(early) > 20 and ((early["vol"] / early["gxt"]).between(0.82, 0.96)).all() and
         (rows[(rows["crew"] == W.CREW_TRUNK) & (rows["dn"] == 150)]["vol"] / rows[(rows["crew"] == W.CREW_TRUNK) &
                                                                                   (rows["dn"] == 150)]["gxt"]
          ).between(0.82, 0.96).all(), "%d early rows" % len(early))
    routes = {h: S.ask_a(target, h)[0] for h in ("plain", "gauge", "diff_all", "dedup", "running_only", "twin_only")}
    near = lambda a, b: abs(a - b) < 0.05
    for h in ("plain", "gauge"):
        g.ok("A3 %s route misses every diameter-year" % h, all(not near(routes[h][k], A[k]) for k in A),
             "%d cells" % len(A))
    miss = sum(not near(routes["diff_all"][k], A[k]) for k in A)
    g.ok("A3 every night differenced (the over-cleaner) misses seven or more diameter-years", miss >= 7,
         "%d of %d" % (miss, len(A)))
    small = [k for k in A if k[0] <= 150]
    large = [k for k in A if k[0] >= 225]
    g.ok("A4 disjoint blocks: running nights alone fixed hits only the small mains", all(
        near(routes["running_only"][k], A[k]) for k in small) and not any(near(routes["running_only"][k], A[k])
                                                                           for k in large), "")
    g.ok("A4 disjoint blocks: twin flushes alone fixed hits only the large mains", all(
        near(routes["twin_only"][k], A[k]) for k in large) and not any(near(routes["twin_only"][k], A[k])
                                                                       for k in small), "")
    g.ok("A5 one row per section kept misses the large mains", not any(near(routes["dedup"][k], A[k]) for k in large), "")
    g.ok("A6 every ask A figure clear of its rounding edge", all(_edge1(v) > 0.004 for v in A.values()),
         "min %.4f" % min(_edge1(v) for v in A.values()))
    g.ok("A7 golden figures equal figures.json", all(figs["flushing_water_m3_per_100m"]["%d mm %d" % k] == "%.1f" % (
        np.floor(A[k] * 10 + 0.5) / 10) for k in A), "")

    # ------------------------------------------------------------------------------------------ ask B
    rer = [W.DCODE[d] for d in W.REROUTED]
    Bg, moved = S.ask_b(target, "golden", rer)
    Bp, _ = S.ask_b(target, "plain", rer)
    Bc, movedc = S.ask_b(target, "corr", rer)
    g.ok("SF15 lesson 8: each moved supply point uses more than its recorded DMA's whole inflow for 100 hours or more",
         len(moved) == 4 and all(v[2] >= 100 for v in moved.values()),
         ", ".join("%s %d h" % (k, v[2]) for k, v in sorted(moved.items())))
    sec_ok = all(sorted(v[3].values())[-1] - sorted(v[3].values())[-2] > 0.15 for v in moved.values())
    g.ok("SF15 the supplying DMA is the one inflow that carries each moved point's steps", sec_ok and {
        (v[0], v[1]) for v in moved.values()} == {(W.DCODE[b], W.DCODE[s]) for _, _, b, s, _ in N.USERS if b != s}, "")
    sp = B.supply(target)
    con = B.consumption(target)
    a = B.amr(target)
    a["local"] = pd.to_datetime(a["read_start_local"], format="%d/%m/%Y %H:%M")
    a["month"] = a["local"].dt.strftime("%Y-%m")
    am = a.groupby(["logger_id", "month"])["volume_m3"].sum()
    lg = sp[sp["AMR logger"].notna()].set_index("SPID")["AMR logger"]
    cm = con[con["spid"].isin(lg.index) & (con["month"] >= "2025-11")].copy()
    cm["amr"] = [am.get((lg[s], m), np.nan) for s, m in zip(cm["spid"], cm["month"])]
    g.ok("SF16 each logged point's monthly settlement equals its logger total to the cubic metre",
         (cm["consumption_m3"] - cm["amr"]).abs().max() <= 0.51, "%d months" % len(cm))
    ends = pd.to_datetime(sp["Supply end"].dropna())
    g.ok("SF19 no supply ended inside the window (present and past tense agree)", not ((ends >= "2025-11-01") &
                                                                                     (ends <= "2026-10-31")).any(), "")
    g.ok("SF18 the window's months are November 2025 to October 2026 in the settlement", sorted(set(
        cm["month"])) == S_months(), "")
    g.ok("B1 plain DMA misses every re-routed district", all(abs(Bp[d] - Bg[d]) >= 1.0 for d in rer),
         ", ".join("%s %.1f" % (d, Bp[d] - Bg[d]) for d in rer))
    g.ok("B2 the correlation mover misses four or more districts", sum(abs(Bc[d] - Bg[d]) >= 0.05 for d in rer) >= 4,
         "%d moved" % len(movedc))
    g.ok("B3 every re-routed district gains or loses a moved point", all(any(d in (v[0], v[1]) for v in moved.values())
                                                                         for d in rer), "")
    g.ok("B4 every ask B figure clear of its rounding edge", all(_edge1(v) > 0.004 for v in Bg.values()), "")
    rep = a[a.duplicated(["logger_id", "read_start_local"], keep="first")]
    lg2 = sp[sp["AMR logger"].notna()].set_index("AMR logger")
    home = {l_: (moved[l_][1] if l_ in moved else lg2.loc[l_, "DMA"]) for l_ in lg2.index}
    worst, crossed = 0.0, []
    for d in rer:
        dv = rep[rep["logger_id"].isin([l_ for l_, h_ in home.items() if h_ == d])]["volume_m3"].sum() / 1000.0
        worst = max(worst, dv)
        if np.floor((Bg[d] - dv) * 10 + 0.5) != np.floor(Bg[d] * 10 + 0.5):
            crossed.append(d)
    g.ok("R2 the autumn repeated hour dropped from logger totals moves no ask B figure", not crossed,
         "largest %.3f Ml" % worst)
    nf = {k: v for k, v in figs["nonhousehold_water_ml"].items()}
    g.ok("B5 golden figures equal figures.json", all(nf["%s %s" % (W.DCODE[d], W.DISTRICTS[d][1])] == "%.1f" % (
        np.floor(Bg[W.DCODE[d]] * 10 + 0.5) / 10) for d in W.REROUTED), "")

    # ------------------------------------------------------------------------------------------ lesson 7
    out = B.outlet(target)
    tot = inflow.sum(axis=1, min_count=18)
    gap = (out.reindex(tot.index) - tot) / tot
    burst_h = pd.Timestamp(W.to_utc(W.BURST_LOSS[0])).floor("h")
    mb = gap.drop([burst_h, burst_h + pd.Timedelta(hours=1)], errors="ignore").dropna()
    g.ok("C1 the works outlet closes on the districts within 3 per cent outside the burst", mb.abs().max() < 0.03,
         "max %.4f, mean %.4f over %d hours" % (mb.abs().max(), mb.mean(), len(mb)))
    g.ok("C2 every hour's arrangement is a fed tree", all(S._is_tree(c["net"], s) for s in set(c["sets"])),
         "%d arrangements" % len(set(c["sets"])))
    change_hours = {pd.Timestamp(t).floor("h") for t in log[log["valve_no"].isin(c["net"].valves) &
                                                             log["action"].isin(["OPEN", "CLOSE"])]["utc"]}
    pk_hours = [c["F"][c["ok"].values][m].idxmax() for m in cand if c["ref"][m] > 0]
    g.ok("C3 no reference peak in an hour with a valve operation or next to one", all(
        min(abs((h - t).total_seconds()) for t in change_hours) >= 7200 for h in pk_hours), "")
    ev_sets = {frozenset(W.MAIN_ID[m] for m in (set(W.TRUNK) - ev["out"]) | ev["open"]) for ev in W.EVENTS}
    got = set(c["sets"]) - {c["net"].normal()}
    g.ok("C4 every arrangement other than normal is one the logged trunk valve operations make", got == ev_sets,
         "%d arrangements from %d jobs" % (len(got), len(W.EVENTS)))
    g.ok("C5 graded flows clear of their rounding edges", all(_edge0(c["peak"][m]) > 0.1 for m in cand) and all(
        _edge0(c["ref"][m]) > 0.08 or c["ref"][m] == 0 for m in cand),
        "min %.2f" % min(_edge0(c["peak"][m]) for m in cand))
    g.ok("C6 meter gaps sit away from every peak", all(inflow.loc[h - pd.Timedelta(hours=24):h + pd.Timedelta(
        hours=24)].notna().all().all() for h in pk_hours), "")
    g.ok("C7 the plan is prepared in November 2026, the window ends October 2026", pl["date"] == "16 November 2026" and
         "twelve months to the end of the month before the outage plan is prepared" in std, pl["date"] or "")

    # ------------------------------------------------------------------------------------------ lesson 12
    val = S.turbidity_backtest(target, c)
    g.ok("V1 the operated flows explain the inlet turbidity record", val["recall_op"] >= 0.75,
         "%.2f of %d observed event days" % (val["recall_op"], val["n_obs"]))
    g.ok("V2 the normal arrangement explains almost none of it", val["recall_nm"] <= 0.1, "%.2f" % val["recall_nm"])
    g.ok("V3 the normal arrangement predicts July turbidity below TM109 and TM110 that never came", val["false_nm"] >= 2
         and val["false_op"] == 0, "normal %d, operated %d" % (val["false_nm"], val["false_op"]))

    # ------------------------------------------------------------------------------------------ R2 mess items
    g.ok("R2 re-sent meter rows are exact copies", finfo["dup"] == 24, "%d" % finfo["dup"])
    raw = pd.read_csv(os.path.join(target, PK.FILES["flows"]), dtype=str)
    ser = raw.groupby("meter_serial")["dma"].nunique()
    g.ok("R2 every meter serial belongs to one district (the meter changes key on the DMA)", ser.max() == 1 and
         raw.groupby("dma")["meter_serial"].nunique().max() == 2, "")
    raw_s = raw[raw["quality"] != "S"]
    g.ok("R2 substituted hours dropped: same figures", True if not len(raw_s) else _same_without(target, raw_s, c), "")
    ex = log[log["action"] == "EXERCISE"]
    g.ok("R2 exercising moves no arrangement", len(ex) > 20 and set(ex["valve_no"]) <= set(c["net"].valves), "%d" % len(ex))
    # SF20: an exercised boundary valve read as the interconnector in service for that hour. Only IC05's and IC03's
    # boundary valves sit on listed mains; IC03's reference can only rise (it stays unflushed); IC05 is bounded above by
    # the whole inflow of the districts its far end serves (Ferrars Corner and Mill Bridge) in each exercise hour.
    shut_v = {v["Valve"]: v["Main"] for v in valves_reg if v["Normal position"] == "Shut"}
    ex_b = ex[ex["valve_no"].isin(shut_v)]
    ex_mains = {shut_v[v] for v in ex_b["valve_no"]}
    far = [d["DMA"] for d in dmas_reg if d["Inlet junction"] in ("Ferrars Corner", "Mill Bridge")]
    ic05_hours = [pd.Timestamp(t).floor("h") for t, v in zip(ex_b["utc"], ex_b["valve_no"]) if shut_v[v] == "IC05"]
    bound = max(float(inflow.loc[h, far].sum()) for h in ic05_hours) if ic05_hours else 0.0
    reshut = all(re.search(r"reshut|left shut", r_, re.I) for r_ in ex_b["remarks"])
    g.ok("SF20 an exercised boundary valve read as in service for its hour: same call", reshut and len(ic05_hours) >= 1
         and bound < c["peak"]["IC05"] and ex_mains <= {"IC05", "IC03", "IC02", "IC08"} and c["ref"]["IC03"] >
         c["peak"]["IC03"], "IC05 at most %.1f l/s in %d exercise hours against %.1f" % (bound, len(ic05_hours),
                                                                                        c["peak"]["IC05"]))
    dist = log[~log["valve_no"].isin(c["net"].valves)]
    g.ok("R2 distribution valves are outside the register", len(dist) > 1000, "%d rows" % len(dist))
    jd = B.jobs(target)
    slash = [x for x in jd["night_of"] if "/" in x]
    g.ok("R2 the job sheets' day-first dates are fixed by the column itself and carry the year either way",
         any(int(x[:2]) > 12 for x in slash) and all(len(x) == 10 for x in jd["night_of"]),
         "%d day-first, %d ISO" % (len(slash), len(jd) - len(slash)))

    # ------------------------------------------------------------------------------------------ realism
    seqs = {"valve_no": [int(v["Valve"][1:]) for v in valves_reg],
            "log_ref": [int(x[2:]) for x in log["log_ref"]],
            "spid": [int(x[2:10]) for x in sp["SPID"]],
            "section_ref": [int(x[2:]) for x in jd["section_ref"].unique()],
            "hydrant": [int(x[1:]) for x in jd["hydrant_no"].unique()],
            "dma": [int(d["DMA"][3:]) for d in dmas_reg]}
    arith = [k for k, v in seqs.items() if len(set(np.diff(sorted(set(v))))) <= 1]
    g.ok("X1 no id column is an arithmetic sequence", not arith, ", ".join(arith) or "%d columns" % len(seqs))
    names = [d["Name"] for d in dmas_reg]
    g.ok("X2 districts in code order are not alphabetical", names != sorted(names), "")
    shapes = {re.sub(r"[A-Z][a-z']+", "W", n) for n in sp["Customer"]}
    g.ok("X3 customer names take many shapes", len(shapes) > 8, "%d shapes" % len(shapes))
    ops = list(log["logged_by"])
    per_ok = all(any(ops[i] != ops[i + p] for i in range(len(ops) - p)) for p in range(1, 9))
    g.ok("X4 no operator dealt round-robin", per_ok, "")
    cnt = con.groupby("month").size()
    g.ok("X5 monthly settlement rows vary", cnt.nunique() > 1, "")
    g.ok("X6 no document dated after its own file date", "16 November 2026" in docs_text["plan"] and
         "23 September 2024" in docs_text["condition"] and "1 April 2025" in std and "2026" not in std, "")
    g.ok("X7 no extract carries a record after its pull", log["local"].max() < pd.Timestamp("2026-11-02") and
         rows["night"].max() <= pd.Timestamp("2026-04-02") and inflow.index.max() < pd.Timestamp("2026-11-02"),
         "log to %s, sheets to %s" % (log["local"].max(), rows["night"].max().date()))

    # ------------------------------------------------------------------------------------------ documents
    for k, s_ in (("standard", "Network Operations Standard NOS 12"), ("plan", "TM107 Ferrars Lane trunk main relining"),
                  ("condition", "Trunk mains condition assessment 2024")):
        g.ok("P1 %s read back (positive control)" % k, s_ in docs_text[k] and len(docs_text[k]) > 800,
             "%d characters" % len(docs_text[k]))
    g.ok("P2 the reference clause is filed once", std.count("highest hourly flow it carried") == 1, "")
    allpdf = " ".join(docs_text.values())
    g.ok("P3 no document names an operated arrangement, the valve log or a past job", not re.search(
        r"valve log|operations log|June 2026|July 2026|burst|back.?feed|as operated|actually carried", allpdf, re.I)
         and "valve job" not in allpdf, "positive control: %s" % ("Network Operations Standard" in allpdf))
    g.ok("P4 no stated factor, margin or threshold on flow", not re.search(r"per cent of|% of|factor|margin|1\.\d+ times|"
                                                                           r"shear", allpdf, re.I), "")
    g.ok("P5 the plan lists the re-routed districts", all(W.DCODE[d] in docs_text["plan"] for d in W.REROUTED), "")
    import subprocess
    from pypdf import PdfReader
    strict_ok = True
    for k, s_ in (("standard", "highest hourly flow it carried in the twelve months"),
                  ("plan", "out of service from 15 March to 15 September 2027"),
                  ("condition", "Trunk mains condition assessment 2024")):
        fp = os.path.join(target, PK.FILES[k])
        lay = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", fp, "-"], capture_output=True,
                                                  text=True).stdout)
        st_txt = re.sub(r"\s+", " ", " ".join(p_.extract_text() for p_ in PdfReader(fp, strict=True).pages))
        strict_ok &= s_ in lay and s_ in st_txt
    g.ok("P6 every PDF reads under a strict reader and poppler's extractor (H25)", strict_ok, "")
    sub = open(os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()
    cited = set(re.findall(r"\b[\w.-]+\.(?:csv|xlsx|pdf)\b", sub)) - {"ferrars_lane_flushing_2027.xlsx",
                                                                         "ferrars_lane_flushing_note.pdf"}
    g.ok("P7 every file the write-up cites ships under that name (H8)", cited <= set(files) and len(cited) >= 6,
         "%d cited" % len(cited))

    # ------------------------------------------------------------------------------------------ distractors
    tmp = tempfile.mkdtemp(prefix="task501_dx_")
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), tmp)
        cd = S.call(tmp)
        Ad, _ = S.ask_a(tmp)
        Bd, _ = S.ask_b(tmp, "golden", rer)
        g.ok("D1 the call and every ask unchanged with the distractors deleted", cd["flush"] == c["flush"] and Ad == A
             and Bd == Bg, ", ".join(meta["distractor_files"]))
        os.remove(os.path.join(tmp, PK.FILES["jobs"]))
        for k in ("supply", "consumption", "amr"):
            os.remove(os.path.join(tmp, PK.FILES[k]))
        ce = S.call(tmp)
        g.ok("D2 the call is unchanged with every ask-only file deleted", ce["flush"] == c["flush"] and all(
            ce["peak"][m] == c["peak"][m] for m in cand), "")
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------ goldens
    import openpyxl as ox
    wb = ox.load_workbook(os.path.join(gold, "ferrars_lane_flushing_2027.xlsx"), data_only=True)
    ws = wb["Flushing call"]
    vals = {r[0]: r for r in ws.iter_rows(values_only=True) if r and r[0] in figs["mains"]}
    g.ok("GX1 the workbook's mains and flows equal figures.json", all(
        vals[m][3] == figs["mains"][m]["highest_hourly_flow_during_works_l_s"] and vals[m][6] == figs["mains"][m]["flush"]
        for m in figs["mains"]), "")
    note = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in __import__("pypdf").PdfReader(
        os.path.join(gold, "ferrars_lane_flushing_note.pdf")).pages))
    g.ok("GX2 the note leads with the call", figs["call"][:40] in note[:400], "")
    g.ok("GX3 no em or en dash in any golden or the submission", not re.search("[–—]", note + open(
        os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()), "")
    g.finish()


def S_months():
    return ["2025-11", "2025-12"] + ["2026-%02d" % m for m in range(1, 11)]


def _same_without(target, raw_s, c):
    tmp = tempfile.mkdtemp(prefix="task501_s_")
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        raw_s.to_csv(os.path.join(tmp, PK.FILES["flows"]), index=False)
        cs = S.call(tmp)
        return cs["flush"] == c["flush"] and all(round(cs["peak"][m]) == round(c["peak"][m]) and
                                                 round(cs["ref"][m]) == round(c["ref"][m]) for m in c["rises"])
    finally:
        shutil.rmtree(tmp)
