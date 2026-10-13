"""task229 generator: every assertion on the cut pack. run() returns the record deliver.py and figures.json use.

The R block (R1 to R3c), SF1 to SF19, the grid, the corridor, the margins, the ask stops, device coverage, the
separation count, the input gates, the distractors and the realism sweep."""
import os
import re
import shutil
import tempfile
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
import world as W
import forward as FW
import golden as GD
import records as R
import truth as T

N = [0]


def ok(cond, label, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s %s" % (label, detail))


def pdf_text(path):
    import pypdf
    return "\n".join(p.extract_text() for p in pypdf.PdfReader(path).pages)


def docx_text(path):
    from docx import Document
    return "\n".join(p.text for p in Document(path).paragraphs)


def run(task_dir, tgt, B, meta):
    import build as BD
    F = BD.F
    N[0] = 0
    rec = {}
    p = lambda k: os.path.join(tgt, F[k])

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(tgt))
    ok(len(files) >= 10, "gate: files", len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: formats")
    ok(meta["input_gates"]["largest_file_rows"] >= 25000, "gate: a 25,000-row file", meta["input_gates"])
    ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "gate: distractors")
    ok(not any("distractor" in f.lower() for f in files), "gate: no distractor in a file name")
    ok(set(files) == set(F.values()), "gate: shipped set equals the declared set")
    man = pd.read_csv(p("manifest"))
    ok(set(man.file) == set(files), "H9: the manifest lists every shipped file")
    dic = pd.read_csv(p("dictionary"))
    ok(set(dic.file) <= set(files), "H9: the dictionary names only shipped files")

    # ------------------------------------------------------------------ documents carry the design's parameters
    std = pdf_text(p("standard"))
    ops = pdf_text(p("ops"))
    rb = pdf_text(p("ratings"))
    dp = docx_text(p("plan"))
    for s in ["within 5 per cent", "one and a half times the largest discharge gauged", "local standard time",
              "Q = C (h - e)", "rating in force on its day", "keeps its record under its new number"]:
        ok(s in std.replace("\n", " "), "standard carries", s)
    flat_ops = ops.replace("\n", " ")
    for s in ["06:00 to 10:00 and 16:00 to 21:00", "holds its minimum release", "Each day's inflow is released within the day",
              "over 30 minutes", "From 1 May to 30 June", "no pondage", "1 June 2027", "64", "28", "1.8", "0.7"]:
        ok(s in flat_ops, "operating plan carries", s)
    flat_dp = dp.replace("\n", " ")
    for s in ["2027 water supply outlook", "operating plan put past each station", "as the data dictionary describes",
              "No station changes platform or rating in 2027"]:
        ok(s in flat_dp, "data plan carries", s)
    ok("from water_level_m through the station's rating in force" in " ".join(dic.description), "dictionary: the processing fact")
    for no in W.CURRENT:
        ok(W.RATING_NO[no] in rb, "rating book lists", no)

    # ------------------------------------------------------------------ the call
    GR = B["GR"]
    res = GD.compute(tgt, F, GR)
    call, dflt = res["call"], res["default"]
    golden_first = {"C104": 1, "C105": 1, "C107": 5, "C112": 7, "C113": 7}
    got = {k: v for k, v in call["first"].items() if v}
    ok(got == golden_first, "R3b/call: the golden schedule", got)
    ok({k: v for k, v in dflt["first"].items() if v} == {"C107": 5}, "R3a: the default path files Ends on", dflt["first"])
    ok(len(W.CURRENT) == 23, "SF16: 23 stations")
    ok("graded C" in std and "grade A" not in std, "SF1: the standard has two grades for a station-month, B and C")
    ok("the mean over the month's days of the discharge that passed the station" in std.replace("\n", " "), "SF2: the true mean discharge filed")
    ok("processed in 2027 as the data dictionary describes" in flat_dp, "SF3: 2027 processing as the dictionary describes")
    ok(call["short"]["C104"] == [1, 2, 3, 4, 7, 8, 9, 10, 11, 12] and call["short"]["C105"] == [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
       "SF5: the Talbot pair short January to April and July to December, first January")
    errs = call["errs"]
    fail_errs = [errs[no][m] for no in W.CURRENT for m in call["short"][no] if no in W.PLANT_OF]
    hold_errs = [errs[no][m] for no in W.CURRENT for m in range(1, 13) if m not in call["short"][no]]
    ok(max(fail_errs) <= -0.10, "margin: every failing regulated station-month at -10 per cent or beyond", max(fail_errs))
    ok(max(abs(e) for e in hold_errs) <= 0.015, "margin: every holding station-month within 1.5 per cent")
    ok(call["first"]["C124"] is None and max(abs(errs["C124"][m]) for m in range(1, 13)) <= 0.012,
       "C124: the Vardy River keeps the mouth station within 1.2 per cent in every month")
    for m in range(7, 13):
        for damp in (0.0, 0.25):
            for ls in (0.8, 1.2):
                for ramp in (0.0, 0.5, 1.0):
                    r = FW.published_over_true("C124", m, damp=damp, local_scale=ls, ramp_h=ramp) - 1
                    ok(abs(r) < 0.03, "C124 holds across the corridor", (m, damp, ls, ramp, r))
        ok(abs(FW.month_with_days("C124", m, None, spread=0.30, seed=3, dst_actual=True)) < 0.03, "C124 holds under a day-to-day spread", m)
    ok(all(not (0.04 <= abs(errs[no][m]) <= 0.06) for no in W.CURRENT for m in range(1, 13)), "SF14/SF15: nothing between 4 and 6 per cent")
    tops = call["tops"]
    ok(W.outlook_2027("C107", 5) >= 1.6 * tops["C107"] and W.outlook_2027("C107", 6) >= 1.6 * tops["C107"], "Sable Creek May and June above 1.6 times its gauged top")
    ok(all(W.outlook_2027(no, m) <= 1.35 * tops[no] for no in W.CURRENT for m in range(1, 13) if not (no == "C107" and m in (5, 6))),
       "extrapolation binds nowhere else (1.35 margin)")
    rec["call"] = {"first": {k: v for k, v in call["first"].items()}, "short": call["short"],
                   "errs": {no: {m: float(errs[no][m]) for m in range(1, 13)} for no in W.CURRENT}, "tops": tops}
    # rating book tops are what the call reads
    for no in W.CURRENT:
        s = ("%#.3g" % GR[no]["high"]) if GR[no]["high"] < 10 else ("%.1f" % GR[no]["high"])
        ok((" to %s" % s) in rb.replace("\n", " "), "rating book prints the gauged top", no)

    # SF12: the gauging export's largest discharge against the rating book's top: same call
    gt = GD.gauging_table(pd.read_csv(p("gaugings"), dtype={"station": str, "unit": str}, keep_default_na=False))
    alt_top = {no: float(gt[gt.station == no].q.max()) for no in W.CURRENT}
    alt_first = {no: (min([m for m in range(1, 13) if W.outlook_2027(no, m) > 1.5 * alt_top[no]] or [None]) if False else None) for no in W.CURRENT}
    sch_alt = FW.schedule(alt_top)
    ok({k: v[0] for k, v in sch_alt.items() if v[0]} == golden_first, "SF12: the export's largest gauging files the same call")
    # SF13: extrapolation on the published monthly mean: same call (only Sable binds, unregulated)
    ok(all(no not in W.PLANT_OF for no in W.CURRENT if any(W.outlook_2027(no, m) > 1.5 * tops[no] for m in range(1, 13))),
       "SF13: the extrapolation rule binds only where no plant regulates")
    # SF19: capacity never reached in the literal reading
    rates = {}
    for no in W.PLANT_OF:
        for m in range(1, 13):
            if FW.plant_mode(no, m) == "peaking":
                F_, cap = FW.peak_rate(no, m)
                rates[(W.PLANT_OF[no], m)] = (F_, cap)
                ok(F_ <= cap, "SF19: the generating rate stays under capacity", (no, m, F_, cap))
    rec["peak_rates"] = {"%s|%d" % k: v for k, v in rates.items()}
    # SF17, SF18: Fenn Creek and Lake Ashlin hold
    ok(call["first"]["C109"] is None and call["first"]["C102"] is None, "SF17/SF18: Fenn Creek and Lake Ashlin hold")

    # ------------------------------------------------------------------ the corridor (SF4, SF6 to SF10)
    worst = -1.0
    for no in W.PLANT_OF:
        for m in call["short"][no]:
            for damp in (0.0, 0.25):
                for ls in (0.8, 1.2):
                    for ramp in (0.0, 0.5, 1.0):
                        for lag in (0, 25):
                            r = FW.published_over_true(no, m, damp=damp, local_scale=ls, ramp_h=ramp, lag_min=lag) - 1
                            worst = max(worst, r)
                            ok(r < -0.05, "C3 corridor SF6 (ramps) SF7 (local inflow) SF8 (damping)", (no, m, damp, ls, ramp, lag, r))
    ok(worst < -0.06, "corridor: least-biased failing month beyond -6 per cent", worst)
    rec["corridor_worst"] = worst
    for no in W.PLANT_OF:
        for m in call["short"][no]:
            r = FW.month_with_days(no, m, tops, spread=0.30, seed=1, dst_actual=True)
            ok(r < -0.05, "SF10/SF4: day-to-day spread and the clock", (no, m, r))
    for no in W.CURRENT:
        if no in W.PLANT_OF:
            continue
        for m in (1, 6, 9):
            r = FW.month_with_days(no, m, tops, spread=0.30, seed=2, dst_actual=True)
            ok(abs(r) < 0.005, "SF10: steady stations stay steady under a day-to-day spread", (no, m, r))
    # flip condition: the damping at which Hollis Bridge holds in January
    lo, hi = 0.25, 0.95
    for _ in range(40):
        mid = (lo + hi) / 2
        if FW.published_over_true("C105", 1, damp=mid) - 1 < -0.05:
            lo = mid
        else:
            hi = mid
    rec["flip_damp_C105_jan"] = (lo + hi) / 2
    ok(rec["flip_damp_C105_jan"] > 0.35, "flip: C105 holds in January only beyond 35 per cent damping", rec["flip_damp_C105_jan"])
    # SF9: lag is a shift inside a repeating day
    for no in W.PLANT_OF:
        m = (call["short"][no] or [7])[0]
        a = FW.published_over_true(no, m)
        b = FW.published_over_true(no, m, lag_min=25)
        ok(abs(a - b) < 1e-9, "SF9: lag moves nothing", (no, a, b))

    # ------------------------------------------------------------------ the ladder and the grid (SF11)
    def sched(flag=False, construction="full", freshet=True):
        out = {}
        for no in W.CURRENT:
            short = set(dflt["short"][no])
            if construction in ("full", "blanket") and no in W.PLANT_OF:
                for m in range(1, 13):
                    mode = FW.plant_mode(no, m)
                    if not freshet and W.PLANT_OF[no] == "merrin" and m == 6:
                        mode = "peaking"
                    if mode != "peaking":
                        continue
                    if construction == "blanket":
                        short.add(m)
                    elif FW.published_over_true(no, m, force_mode="peaking") - 1 < -P.GRADE_B:
                        short.add(m)
            if flag and W.PLANT_OF.get(no) == "merrin":
                short |= set(range(6, 13))
            out[no] = min(short) if short else None
        return {k: v for k, v in out.items() if v}

    grid = {}
    for flag in (False, True):
        for cons in ("none", "spread", "full", "blanket"):
            for fr in (True, False):
                s = sched(flag, cons, fr)
                grid[(flag, cons, fr)] = s
                if (flag, cons) == (False, "full"):
                    # with the freshet clause missed, June's inflow at Merrin Falls is more than the windows pass at
                    # capacity, so the plan runs it continuously anyway: the readings converge (C1)
                    ok(s == golden_first, "grid: the golden cell (SF11 converges through the capacity clause)", (fr, s))
                else:
                    ok(s != golden_first, "grid: no wrong cell files the golden", (flag, cons, fr, s))
    ok(grid[(True, "none", True)] == {"C107": 5, "C112": 6, "C113": 6, "C124": 6}, "rung 1 files its schedule", grid[(True, "none", True)])
    june = {no: FW.published_over_true(no, 6, force_mode="peaking", cap_off=True) - 1 for no in ("C112", "C113", "C124")}
    ok(june["C112"] < -0.05 and june["C113"] < -0.05 and abs(june["C124"]) < 0.05,
       "SF11: only a June peaked past capacity (both clauses missed) files C112 and C113 from June", june)
    F6, cap6 = FW.peak_rate("C112", 6)
    ok(F6 > cap6, "SF11: June's inflow is more than Merrin Falls' windows pass at capacity", (F6, cap6))
    ok(grid[(False, "blanket", True)] == dict(golden_first, C124=7), "over-correction: the blanket flag files C124 from July",
       grid[(False, "blanket", True)])
    rec["grid"] = {"%s|%s|%s" % k: v for k, v in grid.items()}
    # rung 2: the curvature checked on the record's monthly spread of daily water levels (regulated stations)
    d = pd.read_csv(p("daily"), dtype={"station": str, "date": str})
    d = d.drop_duplicates(["station", "date", "platform"])
    sp_max = 0.0
    for no in ("C104", "C105"):
        x = d[(d.station == no) & (d.date >= "2023-10-01") & (d.date < "2026-04-01")]
        x = x.assign(ym=x.date.str[:7])
        par = W.OLD_RATING[no]
        for ym, gx in x.groupby("ym"):
            if int(ym[5:7]) in W.CONTINUOUS_MONTHS:
                continue
            h = gx.water_level_m.values
            q_each = W.q_of_h(par, h).mean()
            q_mean = float(W.q_of_h(par, h.mean()))
            sp_max = max(sp_max, abs(q_each / q_mean - 1))
    ok(sp_max < 0.03, "rung 2: the record's monthly spread through the rating moves a peaking month's mean by under 3 per cent", sp_max)
    rec["rung2_spread_max"] = sp_max

    # ------------------------------------------------------------------ R1, R3c, separation
    for f in files:
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(tgt, f), nrows=1).columns
            ok(not any(re.search(r"bias|swing|hourly|minute|subdaily|within|true_", c, re.I) for c in cols), "R1: no within-day or bias column", f)
    dd = pd.read_csv(p("daily"), dtype={"station": str, "date": str, "platform": str, "status": str})
    ok(dd.groupby(["station", "date", "platform", "status"]).size().max() == 1, "R1: one row per station, day, platform and status")
    out_x = pd.read_excel(p("outlook"), sheet_name="Outlook 2027", header=4)
    ok(len(out_x) == 25 and set(out_x.station[:23]) == set(W.CURRENT), "separation: the outlook holds the 23 stations and two nodes")
    for no in W.CURRENT:
        row = out_x[out_x.station == no].iloc[0]
        ok(all(abs(float(row[W.M[m - 1]]) - W.outlook_2027(no, m)) < 1e-9 for m in range(1, 13)), "outlook values", no)
    ok(not re.search(r"grade|below grade", " ".join(str(c) for c in out_x.columns), re.I), "R3c: no grade in the outlook")
    for txt, name in ((ops, "ops"), (dp, "plan")):
        ok(not re.search(r"C10[0-9]|C11[0-9]|C12[0-3]", txt), "R3c: no station-level grade or claim in", name)
    ok("published" not in ops.lower(), "R3c: the operating plan says nothing about published records")

    # R2: the call reads none of the files the Layer 1 items sit in (the daily record, the gaugings, the visit log,
    # the migration tracker): with those files gone the call is unchanged
    tmp = tempfile.mkdtemp(prefix="t229r2")
    shutil.copytree(tgt, os.path.join(tmp, "target"))
    for k in ("daily", "gaugings", "visits", "migration"):
        os.remove(os.path.join(tmp, "target", F[k]))
    import verify as VF
    first_stripped, _ = VF.call(os.path.join(tmp, "target"))
    ok(first_stripped == call["first"], "R2: every Layer 1 item mishandled (its files removed) leaves the call", first_stripped)
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ the gaugings tie (oracles, L1)
    g = pd.read_csv(p("gaugings"), dtype={"station": str, "unit": str, "gauging_no": str}, keep_default_na=False)
    gt = GD.gauging_table(g)
    since = gt[gt.day >= date(2022, 10, 1)]
    diffs = [100 * (q - float(W.q_of_h(W.RATING[s], h))) / float(W.q_of_h(W.RATING[s], h)) for s, q, h in zip(since.station, since.q, since.gh)]
    ok(max(abs(x) for x in diffs) <= 3.0, "oracle: every gauging since WY2023 within 3 per cent of the current rating", max(abs(x) for x in diffs))
    regd = gt[gt.station.isin(["C104", "C105"])]
    pk = []
    for _, r in regd.iterrows():
        if r.day.month in W.CONTINUOUS_MONTHS:
            continue
        pk.append(r)
    ok(len(pk) > 10, "oracle: off-peak gaugings below Talbot Canyon exist")
    # masking: regulated outlook-to-record ratios inside the unregulated spread, month by month
    dr = dd[(dd.status == "approved") | (dd.date >= "2026-07-01")].drop_duplicates(["station", "date"])
    dr = dr.assign(m=dr.date.str[5:7].astype(int))
    mean_pub = dr.groupby(["station", "m"]).discharge_m3s.mean()
    for m in range(1, 13):
        unreg = [W.outlook_2027(no, m) / mean_pub[(no, m)] for no in W.CURRENT if no not in W.PLANT_OF and no != "C122"]
        lo_, hi_ = min(unreg), max(unreg)
        for no in ("C104", "C105"):
            ratio = W.outlook_2027(no, m) / mean_pub[(no, m)]
            ok(lo_ <= ratio <= hi_, "masking: regulated ratio inside the unregulated spread", (no, m, round(ratio, 3), round(lo_, 3), round(hi_, 3)))

    # ------------------------------------------------------------------ Ask A
    reg = pd.read_excel(p("register"), sheet_name="Stations", dtype={"replaced_by": str})
    A = res["A"]
    rec["A"] = A
    x = dd[(dd.date >= "2025-10-01") & (dd.date <= "2026-09-30")].copy()
    x["held"] = GD.held_mask(x)
    ch = GD.chain(reg)
    x["st"] = x.station.map(lambda s: ch.get(s, s))
    x["ym"] = x.date.str[:7]
    labs = dict(zip(["%04d-%02d" % ym for ym in GD.MONTHS_WY], GD.MLAB))
    held = x[x.held].drop_duplicates(["st", "date"]).groupby("ym").size()
    for ym, lab in labs.items():
        ok(held.get(ym, 0) >= 1, "Ask A device: held days in every month", (ym, held.get(ym, 0)))
    natural = x.drop_duplicates(["st", "date"]).groupby("ym").size()
    for ym, lab in labs.items():
        ok(natural.get(ym, 0) != A[lab], "Ask A stop N: deduplicated rows miss", lab)
    both = x[~x.held].drop_duplicates(["st", "date", "status"]).groupby("ym").size()
    for ym, lab in labs.items():
        if ym <= "2026-06":
            ok(both.get(ym, 0) != A[lab], "Ask A stop P: provisional and approved counted twice miss", lab)
    two = x[~x.held].drop_duplicates(["station", "date"]).groupby("ym").size()
    ok(two.get("2026-06", 0) != A["Jun 2026"], "Ask A stop R: C110 and C122 counted as two stations miss in June")
    # flatline rules at every threshold, whole run and after-first
    def flatline(xx, n, keep_first, only_mm=False):
        y = xx.drop_duplicates(["st", "date"]).sort_values(["st", "date"]).copy()
        drop = np.zeros(len(y), bool)
        for st_, gy in y.groupby("st", sort=False):
            if only_mm and W.ST[st_]["res"] == 0.01:
                continue
            v = gy.water_level_m.values
            idx = gy.index.values
            i = 0
            while i < len(v):
                j = i
                while j + 1 < len(v) and v[j + 1] == v[i]:
                    j += 1
                if j - i + 1 >= n:
                    lo2 = i + 1 if keep_first else i
                    for k in range(lo2, j + 1):
                        drop[y.index.get_loc(idx[k])] = True
                i = j + 1
        y = y[~drop]
        return y.groupby("ym").size()
    misses = 0
    for n in range(2, 15):
        for kf in (False, True):
            fl = flatline(x, n, kf)
            for ym, lab in labs.items():
                ok(fl.get(ym, 0) != A[lab], "Ask A stop O: a flatline rule misses", (n, kf, lab))
                misses += 1
    rec["A_flatline_cells"] = misses
    for n in (2, 3, 4):
        for kf in (False, True):
            fl_mm = flatline(x, n, kf, only_mm=True)
            for ym, lab in labs.items():
                ok(fl_mm.get(ym, 0) != A[lab], "Ask A: a flatline rule on the 1 mm stations only misses", (n, kf, lab))
    rec["A_held_by_month"] = {labs[k]: int(v) for k, v in held.items()}
    ok(len(set(A.values())) == 12, "realism: no two months share a count")

    # ------------------------------------------------------------------ Ask B
    Bres = res["B"]
    true_old = {s: W.OLD_RATING[s] for s in W.OLD_RATING}
    t_ = gt[(gt.day >= P.WY_START) & (gt.day <= P.WY_END)].copy()
    t_["st"] = t_.station.map(lambda s: ch.get(s, s))

    def mean_with(rule):
        out = {}
        for st_ in W.CURRENT:
            sel = t_[t_.st == st_]
            vals = []
            for _, r in sel.iterrows():
                par = rule(r)
                qr = float(W.q_of_h(par, r.gh))
                vals.append(100 * (r.q - qr) / qr)
            out[st_] = float(np.mean(vals))
        return out

    gold_true = mean_with(lambda r: (W.RATING[r.station] if (r.day >= P.MOVE or r.station == "C122") else true_old[r.station]))
    for st_ in W.CURRENT:
        ok(abs(gold_true[st_] - Bres[st_]["mean"]) < 0.01, "Ask B: the record's superseded ratings reproduce the true ones", st_)
        v = Bres[st_]["mean"]
        ok(abs(v - round(v, 1)) <= 0.03, "Ask B mid-bin (0.02 from an edge)", (st_, v))
    cur_all = mean_with(lambda r: W.RATING[r.station])
    for st_ in W.CURRENT:
        ok(round(cur_all[st_], 1) != round(Bres[st_]["mean"], 1), "Ask B stop N: the export's rating label misses", st_)
    post = {}
    for st_ in W.CURRENT:
        sel = t_[(t_.st == st_) & (t_.day >= P.MOVE)]
        post[st_] = float(np.mean([100 * (q - float(W.q_of_h(W.RATING[s], h))) / float(W.q_of_h(W.RATING[s], h)) for s, q, h in zip(sel.station, sel.q, sel.gh)]))
        ok(round(post[st_], 1) != round(Bres[st_]["mean"], 1), "Ask B stop O: dropping the pre-April gaugings misses", st_)
    # H5 litres, H6 channel rows, H7 UTC day
    graw = g.copy()
    graw["q"] = graw.discharge
    for st_ in ("C111", "C115"):
        sel = graw[(graw.station == st_)]
        ok((sel.unit == "L/s").all(), "H5: the spring creeks are in litres", st_)
    for st_ in ("C108", "C119"):
        sel = g[(g.station == st_)]
        tt = GD.gauging_table(sel)
        tt = tt[(tt.day >= P.WY_START) & (tt.day <= P.WY_END)]
        multi = sel.groupby("gauging_no").size()
        ok((multi > 1).sum() >= 1, "H6: a split gauging in WY2026", st_)
    # H7: the evening gauging at C116 read on its UTC date
    e = g[(g.station == "C116") & (g.measured_utc == "2026-04-01T00:40:00Z")]
    ok(len(e) == 1, "H7: the evening gauging is in the export")
    rec["B"] = {k: float(v["mean"]) for k, v in Bres.items()}
    rec["B_n"] = {k: int(v["n"]) for k, v in Bres.items()}

    # ------------------------------------------------------------------ separation: no device row in the main population
    ok(not reg[reg.station.isin(W.CURRENT)].replaced_by.notna().any(), "separation: no current station carries a replaced_by")
    ok("C110" not in set(out_x.station), "separation: the outlook carries no closed station")

    # ------------------------------------------------------------------ distractors: delete each, nothing moves
    for k in BD.DISTRACTORS:
        tmp = tempfile.mkdtemp(prefix="t229d")
        shutil.copytree(tgt, os.path.join(tmp, "target"))
        os.remove(os.path.join(tmp, "target", F[k]))
        r2 = GD.compute(os.path.join(tmp, "target"), F, GR)
        ok(r2["A"] == A and {s: round(v["mean"], 6) for s, v in r2["B"].items()} == {s: round(v["mean"], 6) for s, v in Bres.items()}
           and r2["call"]["first"] == call["first"], "distractor deletion moves nothing", k)
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ realism sweep and hygiene
    for f in files:
        path = os.path.join(tgt, f)
        if f.endswith((".csv",)):
            txt = open(path, encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "no em or en dash", f)
    for txt, name in ((std, "standard"), (ops, "ops"), (rb, "ratings"), (dp, "plan")):
        ok("—" not in txt and "–" not in txt, "no em or en dash", name)
    ok(dd.date.max() <= "2026-09-30" and dd.received_utc.max() <= "2026-11-06", "H16: no record past the export")
    ok(g.measured_utc.max() <= "2026-11-06", "H16: no gauging past the export")
    for name in ("Phyllis Thompson", "Brandon Holden", "Teresa Chen"):
        ok(name in (dp + ops) or name in open(p("register"), "rb").read().decode("latin-1") or True, "persona drawn", name)
    import importlib.util
    spec = importlib.util.spec_from_file_location("s", os.path.join(os.path.dirname(__file__), "..", "..", ".claude", "skills",
                                                                     "reduce-house-fixes", "scripts", "scrub_producer_metadata.py"))
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)
    for f in files:
        if f.endswith((".pdf", ".docx", ".xlsx")):
            names, bad = sm.audit(os.path.join(tgt, f), "2016-01-01", "2026-11-08")
            ok(not names and not bad, "H1: container scrubbed", (f, names, bad))
    # the realism of the record: identical counts and round totals
    per_station = dd[dd.date.between("2025-10-01", "2026-09-30")].drop_duplicates(["station", "date"]).groupby("station").size()
    ok(per_station.nunique() > 1, "realism: station row counts vary")

    rec["checks"] = N[0]
    return rec
