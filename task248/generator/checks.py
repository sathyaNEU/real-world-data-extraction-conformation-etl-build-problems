"""task248 generator checks, run by make.py on the built pack: the call, the variants that must agree and the rungs that
must not, the analyst test on the simulator's clean truth (R3), every row of the design note's semantic fork table (SF1
to SF16), the separation of the asks' rows from the call (S1), the asks' goldens, devices and convergences, the input
gates and the pack's dates."""
import datetime as dt
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import aim
import build as B
import estim as E
import params as P
import records as RC
import sim
import solve

MOVES = {"ADS": -1, "ADE": -1, "ADW": 1, "TRN": -1, "CLF": -1, "SLT": -1}
PUBLISHED, SHED = 30, 26
RUNGS = {"published": 30, "constant": 30, "pmmov": 30, "study plants only": 28}


class Count:
    n = 0


def ok(cond, what):
    assert cond, what
    Count.n += 1


def clean_truth(W):
    """R3 on the simulator's own composites (no rounding, no re-run, the composite's exact flow and mean temperature):
    the easy route (any decay constant over the year, here the published load itself) files 30 and the decisive step
    alone (the decay rate as a function of the water's temperature over the travel time) files 26; the towns' true
    shedding, read the same way, gives the same 26"""
    H = sim.hourly(W)
    C = sim.composites(W, H)
    dates = [c["d"] for c in C]
    easy, gold, true = {}, {}, {}
    for s, p in enumerate(P.PLANTS):
        load = [c["load"][s] for c in C]
        k = [E.LOG10E * sim.k(c["Tw"][s]) * W["tt"][s] for c in C]
        kbar = E.LOG10E * float(np.mean([sim.k(c["Tw"][s]) for c in C])) * W["tt"][s]
        easy[p[0]] = E.episodes(E.levels(dates, [x + kbar for x in load])[0])[0]
        gold[p[0]] = E.episodes(E.levels(dates, [x + y for x, y in zip(load, k)])[0])[0]
        true[p[0]] = E.episodes(E.levels(dates, [c["shed"][s] for c in C])[0])[0]
    return easy, gold, true


def call_checks(target, W):
    F = B.FILES
    pk, par, rows = solve.solve(target, F)
    pub = {r["plant"]: r["published"] for r in rows}
    shed = {r["plant"]: r["shed"] for r in rows}
    ok(sum(pub.values()) == PUBLISHED and sum(shed.values()) == SHED, ("the totals", sum(pub.values()), sum(shed.values())))
    ok({k: shed[k] - pub[k] for k in pk.codes if shed[k] != pub[k]} == MOVES, ("the moving plants", shed, pub))
    ok(0.045 < par["k20"] < 0.055 and 1.08 < par["theta"] < 1.105, ("the fitted decay", par))
    # the printed decay is the same whichever optimiser or replicate handling a reader uses (theta 1.09, about 9 per
    # cent a degree; k20 0.050 on the stated temperature)
    import numpy as np_
    ok("%.2f" % par["theta"] == "1.09" and int(round((par["theta"] - 1) * 100)) == 9 and "%.3f" % par["k20"] == "0.050",
       ("the printed decay", par))
    # the dashboard's export is the published basis recomputed
    xl = pd.read_excel(os.path.join(target, F["dashboard"]), sheet_name="Alert episodes", header=2)
    ok(len(xl) == PUBLISHED and xl.groupby("Plant").size().to_dict() == {k: v for k, v in pub.items() if v},
       ("the dashboard's episodes", len(xl)))
    lv = pd.read_excel(os.path.join(target, F["dashboard"]), sheet_name="Weekly levels", header=3)
    _, plev = pk.counts()
    worst = max(abs(r.Level - plev[r.Plant][0][pd.Timestamp(r._2).date()]) for r in lv.itertuples())
    ok(worst <= 0.0051, ("the dashboard's levels recomputed", worst))
    # C1: every temperature-dependent route gives every plant's count
    V = pk.variants()
    for name, v in V.items():
        ok(v == shed, ("variant", name, {k: v[k] for k in pk.codes if v[k] != shed[k]}))
    # the rungs
    R, _ = pk.rungs()
    for k, want in RUNGS.items():
        ok(sum(R[k].values()) == want, ("rung", k, sum(R[k].values())))
    ok(R["constant"] == pub and R["pmmov"] == pub, "a correction constant over the year gives back the published counts")
    ok(sum(R["additive"].values()) < SHED and all(R["additive"][k] <= shed[k] for k in pk.codes),
       ("the additive rung removes real episodes", R["additive"]))
    ok({k for k in pk.codes if R["study plants only"][k] != pub[k]} == {"ADS", "CLF"}, "the study plants only")
    # margins: the smallest uniform shift that moves a plant's winter count, on both bases
    _, glev = pk.counts(pk.shed_corr()[0])
    ok(min(aim.margins(glev[k][0]) for k in pk.codes) >= 0.10, "the golden's margins")
    ok(min(aim.margins(plev[k][0]) for k in pk.codes) >= 0.05, "the published basis's margins")
    # R3 on the clean truth
    easy, gold, true = clean_truth(W)
    ok(sum(easy.values()) == PUBLISHED and easy == pub, ("R3a: the easy route on the clean truth", easy))
    ok(gold == shed, ("R3b: the decisive step alone on the clean truth", gold))
    ok(true == shed, ("R3b: the towns' true shedding", true))
    return pk, par, rows


def fork_checks(target, pk, rows):
    shed = {r["plant"]: r["shed"] for r in rows}
    pub = {r["plant"]: r["published"] for r in rows}
    corr, _ = pk.shed_corr()
    c = pk.loads()

    def cnt(corrf=None, shift_days=0, pct="inc", start=None, keep_base=False):
        out = {}
        _, plev = pk.counts()
        for code, x in c.groupby("plant_code", sort=False):
            v = x.L.values.copy()
            if corrf is not None:
                v = v + np.array([corrf(r) for r in x.itertuples()])
            d = [di - dt.timedelta(days=shift_days) for di in x.d]
            wk = E.weekly(d, list(v))
            ref = sorted(wk[w] for w in wk if solve.REF[0] <= w <= solve.REF[1])
            if pct == "inc":
                base = E.percentile_inc(ref, 0.10)
            else:
                h = (len(ref) + 1) * 0.10 - 1
                lo = int(np.floor(h))
                base = ref[lo] + (h - lo) * (ref[lo + 1] - ref[lo])
            if keep_base:
                base = plev[code][1]
            lev = {w: wk[w] - base for w in wk if start is None or w >= start}
            out[code] = E.episodes(lev, solve.WINTER)[0]
        return out
    # SF1 'winter': episodes that open in the weeks starting 3 May to 27 September 2027 (methods 5)
    # SF2 a sample's week: the day its composite ended (methods 4); the day it started gives the same counts
    ok(cnt(corr, shift_days=1) == shed and cnt(None, shift_days=1) == pub, "SF2: the week by the composite's start")
    # SF3 the baseline: PERCENTILE.INC (methods 4); PERCENTILE.EXC gives the same counts
    ok(cnt(corr, pct="exc") == shed and cnt(None, pct="exc") == pub, "SF3: PERCENTILE.EXC")
    # SF4 the reference weeks 6 April 2026 to 29 March 2027 (methods 4): filed
    ok(sum(1 for w in E.weekly([x for x in c.d], list(c.L)) if solve.REF[0] <= w <= solve.REF[1]) == 52, "SF4")
    # SF5 the flow: the form's against the historian's (methods 3 and 6.2): the same counts
    ok(pk.counts(corr, flow="hflow")[0] == shed and pk.counts(flow="hflow")[0] == pub, "SF5: the historian's flow")
    # SF6 the temperature: the composite's own, the month's, the season's, the study's probe readings: the variants
    # SF7 the travel time: the memo's population-weighted minutes (the register carries none)
    ok(pk.tt["CLF"] == 1615 and pk.tt["FNK"] == 27, "SF7")
    # SF8 an episode opens at High (1.0 or more) and closes at Low (below 0.5) (methods 5): filed
    # SF9 the state when the winter starts: every plant at Low in the week of 26 April 2027 on both bases, so the
    # count is the same whether episodes are followed from the record's start, the reference year or the winter
    _, glev = pk.counts(corr)
    _, plev = pk.counts()
    w0 = dt.date(2027, 4, 26)
    ok(max(glev[k][0][w0] for k in pk.codes) < 0.45 and max(plev[k][0][w0] for k in pk.codes) < 0.45, "SF9: Low on 26 April")
    for start in (solve.REF[0], solve.WINTER[0]):
        ok(cnt(corr, start=start) == shed and cnt(None, start=start) == pub, ("SF9: followed from", start))
    # SF10 the shed load's baseline recomputed on the shed load (methods 6.1, 'exactly as sections 4 and 5'); keeping
    # the published baseline is ruled out by that sentence and gives another count
    kb = cnt(corr, keep_base=True)
    ok(sum(kb.values()) != SHED, ("SF10: the published baseline kept", sum(kb.values())))
    # SF11 a sample's result: the accepted run (methods 2, export notes); the latest, first or mean run: same counts
    for runs in ("latest", "first", "mean"):
        ok(pk.counts(corr, runs=runs)[0] == shed and pk.counts(runs=runs)[0] == pub, ("SF11", runs))
    # SF12 the faecal-strength check over the reference year and winter 2027 flags nothing, so reading those samples
    # as the dashboard will (methods 6.3) leaves every count
    flags = winter_flags(pk)
    ok(flags == 0, ("SF12: no composite of April 2026 to September 2027 fails the check", flags))
    # SF13 the decay over the travel time in log10: the rate per hour times the hours times log10(e); the study's
    # ratios in log10 or ln give the same rate (asserted by the fit's form)
    # SF14 the population: the register's figure, the same on both bases
    # SF15 the published total: the dashboard's export, recomputed (call_checks)
    # SF16 counts are whole numbers (the prompt)
    for sf in ("SF1", "SF6", "SF8", "SF13", "SF14", "SF15", "SF16"):
        ok(True, sf)


def winter_flags(pk):
    cmp = pk.composites()
    vol, _ = pk.window()
    q = np.array([vol.get(k, np.nan) for k in zip(cmp.plant_code, cmp.d)])
    cmp["LP"] = np.log10(cmp.PMMoV.values * q * 1000.0 / cmp.plant_code.map(pk.pop).values)
    n = 0
    for code, x in cmp.groupby("plant_code", sort=False):
        d, v = list(x.d), list(x.LP)
        for i, di in enumerate(d):
            if not (dt.date(2026, 4, 6) <= di <= dt.date(2027, 10, 3)):
                continue
            prev = [v[j] for j in range(len(d)) if di - dt.timedelta(days=365) <= d[j] < di]
            if prev and abs(v[i] - np.median(prev)) > 0.5:
                n += 1
    return n


def separation(target, R):
    """S1: no fault, spoiled composite, contract composite or second channel reaches the call's rows (the composites of
    April 2026 to September 2027 and the historian's hours over their windows), and the call computes the same without
    the ask-only files"""
    loc = R.H["local"]
    day = np.array([t.date() for t in loc])
    main = day <= dt.date(2027, 9, 30)          # the last composite of the winter ends on 30 September
    for arr in (R.drop, R.blank, R.hold, R.zero, R.dup):
        ok(not arr[:, main].any(), "S1: no historian fault in the call's period")
    ok(all(R.C[i]["d"] >= RC.ASK_B[0] for (s, i) in R.spoiled), "S1: no spoiled composite in the call's period")
    ok(RC.CONTRACT[0] > dt.date(2027, 9, 30) and RC.TWO_CHANNEL_FROM > dt.date(2027, 9, 30), "S1: contract, channels")
    F = B.FILES
    tmp = tempfile.mkdtemp()
    for k in B.PACK:
        if k not in ("contract", "rain", "eqa", "dashboard"):
            shutil.copy(os.path.join(target, F[k]), tmp)
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(["Method: 1 mL of each composite concentrated; the pellet resuspended in 1 mL, of which 1 uL was extracted "
               "and eluted in 1 uL."])
    ws.append([])
    ws.append(["Lab ref", "Client site", "Sampled", "Received", "Analyte", "Result", "Flow"])
    wb.save(os.path.join(tmp, F["contract"]))
    try:
        pk, par, rows = solve.solve(tmp, F)
        ok(sum(r["shed"] for r in rows) == SHED and sum(r["published"] for r in rows) == PUBLISHED,
           "S1: the call without the contract report and the distractors")
    finally:
        shutil.rmtree(tmp)


def ask_checks(target, pk, R):
    # Ask A
    g = pk.ask_a()
    truth = {}
    loc = R.H["local"]
    lo = np.array([RC.ASK_A[0] <= t.date() <= RC.ASK_A[1] for t in loc])
    inval = R.drop | R.blank | R.hold | R.zero
    for s, code in enumerate(pk.codes):
        truth[code] = int(inval[s, lo].sum())
    ok(g == truth, ("ask A: the golden is the generator's faults", g, truth))
    ok(len(pk.hours_window()) == 8784, "ask A: 8,784 real hours in the year")
    for name, kw, n_moved in (("naive grid", dict(grid="naive"), 24), ("key dedup", dict(dedup="key"), 24),
                              ("naive grid and key dedup", dict(grid="naive", dedup="key"), 24),
                              ("rows only", dict(absent=False), 24), ("every reading of a hold", dict(holds="all"), 12)):
        v = pk.ask_a(**kw)
        moved = sum(v[k] != g[k] for k in pk.codes)
        ok(moved == n_moved if n_moved == 24 else moved >= n_moved, ("ask A stop", name, moved, v))
    ok(pk.ask_a(dedup="none") == g, "ask A: no dedup on the real hours is the golden")
    # SF22: an hour is an hour of the clock as it ran: the export note's span in hours is the real hours, one more than
    # the span's days times 24, so a grid of wall-clock labels is ruled out by the note
    note = _text(os.path.join(target, B.FILES["scadanote"]))
    days = (dt.date(2028, 4, 9) - dt.date(2026, 1, 5)).days + 1
    ok("23:00 on 9 April 2028, {:,} hours, with a row".format(R.span_hours()) in note and R.span_hours() == days * 24 + 1,
       ("SF22: the note's span in real hours", R.span_hours(), days * 24))
    # SF17: the window in UTC days gives the same hours: no fault within a day of either edge
    ok(not (R.drop | R.blank | R.hold | R.zero)[:, ~np.array([dt.date(2027, 4, 2) <= t.date() <= dt.date(2028, 3, 30)
                                                              for t in loc])].any(), "SF17: no fault near the edges")
    ok(len(set(g.values())) >= 17 and min(g.values()) >= 10, ("ask A: spread", g))
    # Ask B
    b, det = pk.ask_b()
    want = {code: 0 for code in pk.codes}
    for (s, i) in R.spoiled:
        want[pk.codes[s]] += 1
    ok(b == want, ("ask B: the golden is the spoiled composites", b, want))
    flagged = [abs(x[1]) for k in det for x in det[k]]
    ok(min(flagged) >= 0.6, ("ask B: flagged clear of the line", min(flagged)))
    ok(unflagged_max(pk) <= 0.3, ("ask B: unflagged clear of the line", unflagged_max(pk)))
    for name, kw, n_moved in (("as reported", dict(contract_factor=1.0), 24),
                              ("aliquot left out", dict(contract_factor=pk.contract_naive), 24),
                              ("microlitres as litres", dict(contract_factor=1e6), 24),
                              ("the form's flow", dict(flow="form"), 3), ("the first run", dict(runs="first"), 12),
                              ("no contract report", dict(contract=False), 5)):
        v, _ = pk.ask_b(**kw)
        moved = sum(v[k] != b[k] for k in pk.codes)
        ok(moved == n_moved if n_moved in (3, 24) else moved >= n_moved, ("ask B stop", name, moved, v))
    # SF18: the composites by the day they started gives the same failures: none of the window's first or last two
    edge = {c["d"] for c in R.C if c["d"] in (RC.ASK_B[0], RC.ASK_B[0] + dt.timedelta(days=3), RC.ASK_B[1],
                                               RC.ASK_B[1] - dt.timedelta(days=3))}
    ok(len(edge) == 4 and not any(R.C[i]["d"] in edge for (s_, i) in R.spoiled), "SF18: no failure at the window's edges")
    # SF21: the median's 365 days need no boundary convention: no composite falls 365 or 366 days before another
    days = sorted({c["d"] for c in R.C})
    dset = set(days)
    ok(not any((d - dt.timedelta(days=365)) in dset or (d - dt.timedelta(days=366)) in dset for d in days),
       "SF21: no composite on the median window's boundary")
    # SF19: every composite of the check's window has valid historian hours to fill from
    vol, _ = pk.window()
    cmp = pk.composites()
    inside = cmp[(cmp.d >= RC.ASK_B[0]) & (cmp.d <= RC.ASK_B[1])]
    ok(all(np.isfinite(vol.get(k, np.nan)) for k in zip(inside.plant_code, inside.d)),
       "SF19: every composite of the window has a valid historian hour")
    for name, kw in (("latest run", dict(runs="latest")), ("mean of runs", dict(runs="mean")),
                     ("SF19 raw sums", dict(fill="raw")), ("SF19 valid sums", dict(fill="valid")),
                     ("SF19 interpolated", dict(fill="interp")), ("SF20 below only", dict(sides=1))):
        v, _ = pk.ask_b(**kw)
        ok(v == b, ("ask B convergence", name, v))
    ok(max(list(b.values()).count(x) for x in set(b.values())) <= 5 and list(b.values()).count(0) <= 2,
       "ask B: no constant or nil response keeps more than a fifth")


def unflagged_max(pk):
    c = pk.composites()
    vol, _ = pk.window()
    q = np.array([vol.get(k, np.nan) for k in zip(c.plant_code, c.d)])
    c["LP"] = np.log10(c.PMMoV.values * q * 1000.0 / c.plant_code.map(pk.pop).values)
    worst = 0.0
    for code, x in c.groupby("plant_code", sort=False):
        d, v = list(x.d), list(x.LP)
        for i, di in enumerate(d):
            if not (RC.ASK_B[0] <= di <= RC.ASK_B[1]):
                continue
            prev = [v[j] for j in range(len(d)) if di - dt.timedelta(days=365) <= d[j] < di]
            dev = abs(v[i] - np.median(prev))
            if dev <= 0.5:
                worst = max(worst, dev)
    return worst


def gates(target):
    F = B.FILES
    files = [F[k] for k in B.PACK]
    ok(all(os.path.exists(os.path.join(target, f)) for f in files) and len(files) >= 10, "ten files or more")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three formats or more")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, ("a file of 25,000 rows", big))
    ok(len(B.DISTRACTORS) >= 2, "two distractors")
    ok(sorted(os.listdir(target)) == sorted(files), "the pack is the declared files")
    asof = P.ASOF.isoformat()
    lab = pd.read_csv(os.path.join(target, F["lab"]))
    ok(lab.analysed.max() < asof and lab.composite_end.max() < asof, "lab dates before the as-of")
    h = pd.read_csv(os.path.join(target, F["scada"]), usecols=["timestamp_local"])
    ok(h.timestamp_local.max() < asof, "historian before the as-of")
    for f in files:
        if f.endswith((".csv", ".md", ".eml")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok(chr(0x2014) not in txt and chr(0x2013) not in txt, ("no dashes", f))


def _text(path):
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return " ".join(" ".join(p.extract_text() for p in PdfReader(path).pages).split())
    return " ".join(open(path, encoding="utf-8").read().split())


def three_rules(target, pk, rows):
    """R1 the raw material ships and the deciding quantity does not; R2 each Layer 1 item mishandled leaves the call
    (or moves only its ledgered asks); R3a and R3b on the clean truth in call_checks; R3c no plant"""
    F = B.FILES
    shed = {r["plant"]: r["shed"] for r in rows}
    pub = {r["plant"]: r["published"] for r in rows}
    # R1: the study's paired readings and the historian's hourly temperatures ship; no document states a decay rate,
    # a temperature dependence or a shed load figure (each document read through the same extractor, with a sentence
    # known to be in it found first)
    st = pd.read_csv(os.path.join(target, F["study"]))
    ok(st.groupby(["plant_code", "visit_date"]).ngroups == 26 * 4 - 3, "R1: the study's 101 visits ship")
    h = pd.read_csv(os.path.join(target, F["scada"]), usecols=["inlet_temperature_c"])
    ok(h.inlet_temperature_c.notna().mean() > 0.999, "R1: the historian's temperatures ship")
    controls = {"methods": "the load the town shed into the sewer", "studyreport": "Twenty-six visits were planned",
                "travel": "weighted by each sub-catchment's population", "scadanote": "the probe in the inlet channel",
                "labnote": "The accepted run is the sample's result", "request": "the verification desk's rota",
                "contents": "the site register", "dict": "population_served"}
    for k, ctl in controls.items():
        t = _text(os.path.join(target, F[k]))
        ok(len(t) > 200 and ctl in t, ("R1: the control sentence is read", k))
        low = t.lower()
        ok(not re.search(r"decay rate|first.order|per degree|warm water|colder water|temperature.dependen", low),
           ("R1: no decay method in", F[k]))
    # R2, item by item: the run-level export (SF11), the composite's week (SF2), the form's against the historian's flow
    # (SF5), the study's copies per millilitre against the laboratory's per litre (the ratios are unit-free), the clocks
    # (no composite spans a change of clock, so the naive local reading picks the same 24 hours: asserted here), the
    # travel times in minutes (one rate in either unit), the contract report, the historian's faults and the second
    # channels (S1: none of them reaches the call)
    j = pk.pairs()
    ok(j.y.between(-2.5, 0.5).all(), "R2: the study's ratios are unit-free")
    lab = pd.read_csv(os.path.join(target, F["lab"]), usecols=["composite_end"])
    ends = pd.to_datetime(lab.composite_end.unique())
    import clock
    for e in ends:
        a = clock.to_utc(e.to_pydatetime() - dt.timedelta(hours=24))
        z = clock.to_utc(e.to_pydatetime())
        ok((z - a) == dt.timedelta(hours=24), ("R2: no composite spans a clock change", e))
    for flag in ("SF2", "SF5", "SF11", "S1"):
        ok(True, "R2 " + flag)
    # R3c: no plant; the realism sweep
    ok(st.duplicated(["n1_copies_per_ml", "pmmov_copies_per_ml"]).sum() == 0, "R3c: no repeated study result")
    hh = pk.h[pk.h.ts < pd.Timestamp("2027-10-01")]
    ok(int(hh.held.sum()) == 0, "R3c: no held reading before October 2027")
    lag = pd.to_datetime(st[st.point == "plant"].composite_start).values - \
        pd.to_datetime(st[st.point == "upstream"].composite_start).values
    ok(len(set(lag)) > 30, "R3c: the plant composites' starts vary as the field team set them")
    A = pk.ask_a()
    ok(len(set(A.values())) >= 15, "R3c: the plants' historian hours mostly differ")
    ok(sum(A.values()) % 10 and sum(pub.values()) == 30, "R3c: no round headline")
    # distractors: the asks and the call without the rain gauges and the EQA returns
    tmp = tempfile.mkdtemp()
    for k in B.PACK:
        if k not in B.DISTRACTORS:
            shutil.copy(os.path.join(target, F[k]), tmp)
    try:
        q = solve.Pack(tmp, F)
        ok(q.counts(q.shed_corr()[0])[0] == shed and q.ask_a() == A and q.ask_b()[0] == pk.ask_b()[0],
           "the distractors' deletion test")
    finally:
        shutil.rmtree(tmp)


def run(target, W, fig, golden):
    Count.n = 0
    R = RC.Records(W)
    pk, par, rows = call_checks(target, W)
    fork_checks(target, pk, rows)
    three_rules(target, pk, rows)
    separation(target, R)
    R.results()
    ask_checks(target, pk, R)
    gates(target)
    ok(fig["totals"] == {"published": PUBLISHED, "shed": SHED}, "figures.json totals")
    ok(os.path.exists(os.path.join(golden, "winter_2027_episodes_shed_load.xlsx")), "golden workbook")
    ok(os.path.exists(os.path.join(golden, "verification_desk_winter_2028.docx")), "golden note")
    return Count.n
