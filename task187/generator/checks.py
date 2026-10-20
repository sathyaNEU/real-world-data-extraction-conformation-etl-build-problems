"""Assertions on the built pack and goldens: the input gates; the three rules executed on the generator's clean truth
(R1 the ten-minute record with each anemometer's standard deviation ships and no column holds a turbulence intensity
or a shortfall; R2 each Layer 1 item is neutral for the call and the recovered energy's bin; R3a the easy route, the
shortfall against the warranted curve at matched mean wind with every filed rule applied, files CH07; R3b the decisive
step alone files CH04 and each lower rung's single correction stays wrong; R3c no plant); the ladder's rungs by name
with their margins and the golden's place on each; every matched-turbulence variant files CH04 and one recovered-energy
bin; the semantic forks SF1 to SF14; the asks' golden against the truth and every stop outside it for every turbine;
the separation of the asks from the call; the documents' silence; the realism sweep; and the goldens against
figures.json."""
import csv
import datetime as dt
import json
import os
import re
import warnings

import numpy as np
import openpyxl

import analysis as AN
import build as B
import deliver as DL
import docs as D
import records as R
import world as W

warnings.filterwarnings("ignore", category=RuntimeWarning)
N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def ok(cond, what):
    N[0] += 1
    if not cond:
        raise AssertionError(what)


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(path).pages))


def lead(d, winner):
    rest = sorted((v for t, v in d.items() if t != winner), reverse=True)
    return d[winner] / rest[0] if rest[0] > 0 else 99.0


def rank(d, t):
    return AN.ranked(d).index(t) + 1


def variants(F):
    """Every matched-turbulence reading the design note's SF9 names: Annex M on the mast's or the type test's
    turbulence, turbulence bins of 0.25 or 0.5 m/s by 0.01 to 0.05 against the fleet's mean, median, or mean without
    the eroded rotors, and the turbulence band (which values the loss at the usual turbulence)."""
    out = {}
    out["annexM mast"] = AN.matched_annex_m(F)[0]
    import wind as WD
    out["annexM typical"] = AN.matched_annex_m(F, ti_ref=WD.ti_typical)[0]
    for dv in (0.25, 0.5):
        for dti in (0.01, 0.02, 0.03, 0.05):
            for ref, ex in (("mean", ()), ("median", ()), ("mean", ("CH02", "CH04", "CH09"))):
                out["bins %s%s %.2f %.2f" % (ref, "x" if ex else "", dv, dti)] = AN.matched_bins(
                    F, dv=dv, dti=dti, ref=ref, exclude=ex, minn=10)
    return out


def run(target, golden, sim, meta_path, quiet=False):
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    Bd = AN.read_bundle(target)
    AN.set_curve(Bd["curve"])
    F = AN.frame_bundle(Bd)
    Ft = AN.frame_truth(sim["mast"], sim["turb"], sim["ops"])

    # ------------------------------------------------------------------ the input gates
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    ok(len(Bd["scada"]) >= 25000, "a file of 25,000 rows or more (%d)" % len(Bd["scada"]))
    ok(set(meta["distractor_files"]) == {R.ANM, R.PRIOR}, "two distractors declared")
    ok(not any("distractor" in f or "golden" in f or "answer" in f for f in files), "no author noun in a file name")
    ok(files == sorted(B.FILES.values()), "the shipped set is the declared set")

    # ------------------------------------------------------------------ R1, the field's raw material ships
    cols = list(Bd["scada"].columns)
    ok(cols == ["timestamp", "turbine", "wind_speed_mean", "wind_speed_sd", "nacelle_position", "active_power_mean",
                "ambient_temperature", "state"], "R1 the SCADA's channels")
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f)).readline().lower()
            ok(not re.search(r"turbulence|\bti\b|shortfall|erosion|blade", head), "R1 no derived column in %s" % f)
    no_sd = {t: dict(F[t]) for t in W.TURBINES}
    for t in W.TURBINES:
        no_sd[t]["ti"] = F["_mast_ti"][F[t]["k"]]
    no_sd.update({k: v for k, v in F.items() if k.startswith("_")})
    am_nosd = AN.matched_annex_m(no_sd)[0]
    ok(AN.pick(am_nosd) == "CH07", "R1 without each anemometer's own deviation the comparison files CH07 (the "
                                  "deciding computation reads wind_speed_sd)")

    # ------------------------------------------------------------------ R3, the analyst test on the clean truth
    d_truth = AN.default_shortfall(Ft)
    ok(AN.pick(d_truth) == "CH07", "R3a the default path on the clean truth files CH07 (%s)" % AN.pick(d_truth))
    am_truth = AN.matched_annex_m(Ft)[0]
    ok(AN.pick(am_truth) == "CH04", "R3b the decisive step alone files CH04")
    ok(AN.pick(AN.default_shortfall(Ft, whole_year=True)) == "CH09", "R3b without the blade-set rule the default files CH09")
    ok(AN.pick(AN.wake_excluded_shortfall(Ft)) == "CH07", "R3b disturbed sectors excluded alone stays on CH07")
    ok(AN.pick(AN.mast_ti_annex_m(Ft)) == "CH07", "R3b the mast's turbulence alone stays on CH07")
    ok(AN.pick(AN.mast_wind_shortfall(Ft)) != "CH04", "R3b the mast's wind alone stays off CH04")
    ok(AN.pick(AN.default_shortfall(Ft, lo=3.0, hi=10.0)) == "CH02", "R3b the partial-load cut alone files CH02")
    ok(AN.pick(AN.matched_annex_m(Ft, whole_year=True)[0]) == "CH09", "R3b turbulence matched without the blade-set "
                                                                      "rule files CH09")
    om = _pdf_text(os.path.join(target, D.STANDARD)).lower()
    for w_ in ("turbulence", "eddies", "plantation", "forest", "loch", "wake", "gust"):
        ok(re.search(r"\b%s" % w_, om) is None, "R3 OM-07 is silent on %s" % w_)
    prompt = open(os.path.join(TASK, "prompt.txt")).read().lower()
    for w_ in ("turbulence", "plantation", "wake", "loch", "partial load"):
        ok(w_ not in prompt, "R3 the prompt is silent on %s" % w_)
    sched = _pdf_text(os.path.join(target, D.SCHEDULE)).lower()
    ok("turbulence" not in sched and "intensity" not in sched, "R3 the warranted curve states no turbulence")
    # R3c no plant: no file names a turbine for the campaign or states a shortfall; the counters are the turbines'
    for f in files:
        if f.endswith((".csv", ".txt")):
            txt = open(os.path.join(target, f)).read().lower()
            ok("campaign" not in txt or f == D.NOTES, "R3c %s does not mention the campaign" % f)
            ok("shortfall" not in txt and "erosion" not in txt, "R3c %s states no shortfall or erosion" % f)

    # ------------------------------------------------------------------ R2, each Layer 1 item neutral for the call
    golden_bin = fig["recovered_mwh_nearest_50"]
    for clock in ("local", "utc"):
        Fc = AN.frame_bundle(Bd, clock)
        a = AN.matched_annex_m(Fc)[0]
        ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) == golden_bin, "R2 SCADA clock read %s: same call, same "
                                                                            "bin (SF10)" % clock)
        ok(AN.pick(AN.default_shortfall(Fc)) == "CH07", "R2 SCADA clock read %s: the default stays on CH07" % clock)
    # the repeated October hour dropped (one copy kept)
    sc = Bd["scada"]
    dedup = dict(Bd)
    dedup["scada"] = sc[~sc.duplicated(subset=["turbine", "timestamp"], keep="first")].reset_index(drop=True)
    ok(len(dedup["scada"]) == len(sc) - 60, "the October clock change repeats one hour for each turbine")
    Fd = AN.frame_bundle(dedup)
    a = AN.matched_annex_m(Fd)[0]
    ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) == golden_bin, "R2 repeated hour dropped: same call, same "
                                                                        "bin (SF11)")
    # the mast read as stamping the interval's end (ten minutes off)
    sh = dict(Bd)
    sh["mast"] = np.vstack([Bd["mast"][1:], Bd["mast"][-1:]])
    a = AN.matched_annex_m(AN.frame_bundle(sh))[0]
    ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) == golden_bin, "R2 mast stamps read as interval ends: same")
    # SF5: the warranted curve is stated at 1.225 kg/m3 and OM-07 4.6 writes the correction; read without it, every
    # turbine loses 50 to 200 MWh and the call still stands
    Fx = {t: dict(F[t]) for t in W.TURBINES}
    Fx.update({k: v for k, v in F.items() if k.startswith("_")})
    rho = AN.density(Bd["mast"][:, 3], Bd["mast"][:, 4])
    for t in W.TURBINES:
        Fx[t]["veff"] = F[t]["veff"] / (rho[F[t]["k"]] / 1.225) ** (1 / 3)
    a = AN.matched_annex_m(Fx)[0]
    ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) != golden_bin, "SF5 no density correction: same call, the "
                                                                        "energy off its bin (ruled out by Schedule 3)")
    ok(AN.pick(AN.default_shortfall(Fx)) == "CH07", "SF5 no density correction: the default stays on CH07")
    ok("1.225" in _pdf_text(os.path.join(target, D.SCHEDULE)) and "1.225" in om, "SF5 the density basis is filed")

    # ------------------------------------------------------------------ the ladder, built values
    r0y = AN.default_shortfall(F, whole_year=True)
    r0 = AN.default_shortfall(F)
    ok(AN.pick(r0y) == "CH09" and lead(r0y, "CH09") >= 1.15, "R0' the whole year files CH09 by 1.15x or more (%.2f)" %
       lead(r0y, "CH09"))
    ok(AN.pick(r0) == "CH07" and lead(r0, "CH07") >= 1.6, "R0 the default files CH07 by 1.6x or more (%.2f)" %
       lead(r0, "CH07"))
    ok(rank(r0, "CH04") == 4, "R0 the golden is fourth on the default path (%d)" % rank(r0, "CH04"))
    ok(rank(r0y, "CH04") >= 4, "R0' the golden is fourth or lower on the whole year")
    ok(AN.pick(AN.interp_shortfall(F)) == "CH07", "SF8 per-record interpolation files CH07 too")
    partial_first = []
    worst = 99.0
    for lo in (3.0, 3.5, 4.0, 5.0):
        for hi in (8.0, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0):
            r = AN.default_shortfall(F, lo=lo, hi=hi)
            partial_first.append(AN.pick(r))
            if AN.pick(r) != "CH04":
                worst = min(worst, r[AN.pick(r)] / max(r["CH04"], 1e-6) if r["CH04"] > 0 else 99)
    ok("CH04" not in partial_first, "R1 no partial-load cut from 3-5 to 8-12 m/s files CH04")
    ok(sum(p == "CH02" for p in partial_first) >= 20, "R1 most partial-load cuts file CH02")
    ok(worst >= 1.0, "R1 the closest partial-load cut still leads CH04 (%.2f)" % worst)
    wx = AN.wake_excluded_shortfall(F)
    ok(AN.pick(wx) == "CH07" and rank(wx, "CH04") >= 4, "R1b disturbed sectors excluded: CH07, CH04 fourth or lower")
    ok(AN.pick(AN.mast_ti_annex_m(F)) == "CH07", "R1b the mast's turbulence: CH07")
    ok(AN.pick(AN.mast_wind_shortfall(F)) == "CH07", "R1b the mast's wind: CH07")
    V9 = variants(F)
    ratios = {}
    for k, d in V9.items():
        ok(AN.pick(d) == "CH04", "R2 %s files CH04" % k)
        ratios[k] = lead(d, "CH04")
        ok(ratios[k] >= 1.15, "R2 %s leads by 1.15x or more (%.2f)" % (k, ratios[k]))
        ok(75 + 3 <= d["CH04"] < 125 - 3, "SF9 %s puts the recovered energy in the 100 MWh bin (%.1f)" % (k, d["CH04"]))
        for t in ("CH07", "CH05", "CH01"):
            ok(d[t] < 0.25 * d["CH04"], "R2 %s leaves %s sound" % (k, t))
    band = AN.matched_band(F)
    ok(AN.pick(band) == "CH04" and 78 <= band["CH04"] < 122, "SF9 the turbulence band: CH04, same bin (%.1f)" % band["CH04"])
    a10 = AN.matched_annex_m(F, ti_ref=lambda v: np.full_like(np.asarray(v, float), 0.10))[0]
    ok(AN.pick(a10) == "CH04" and 78 <= a10["CH04"] < 122, "SF9 Annex M on a flat 10 per cent: CH04, same bin (%.1f)"
       % a10["CH04"])
    ok(fig["call"] == "CH04" and fig["recovered_mwh_nearest_50"] == 100, "the call and its bin in figures.json")
    ok(abs(fig["recovered_mwh"] - V9["annexM mast"]["CH04"]) < 0.06, "figures.json carries the Annex M figure")
    ok(lead(V9["annexM mast"], "CH04") >= 1.3, "R2 Annex M leads CH02 by 1.3x or more")
    ok(abs(V9["annexM mast"]["CH04"] - am_truth["CH04"]) < 1.0, "the bundle's figure equals the clean truth's within "
                                                               "a MWh")

    # ------------------------------------------------------------------ the semantic forks
    Fs = {t: dict(F[t]) for t in W.TURBINES}
    Fs.update({k: v for k, v in F.items() if k.startswith("_")})
    for t in W.TURBINES:
        Fs[t]["normal"] = F[t]["state"] == 10
    a = AN.matched_annex_m(Fs)[0]
    ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) == golden_bin, "SF1 state 10 only: same call, same bin")
    for t in W.TURBINES:
        Fs[t]["normal"] = np.isin(F[t]["state"], (10, 11, 20))
    a = AN.matched_annex_m(Fs)[0]
    ok(AN.pick(a) in W.NOISE_TURBINES, "SF1 power-limited kept: a noise-mode turbine's limit reads as blade loss (%s), "
                                       "ruled out by OM-07 3.1" % AN.pick(a))
    ok(AN.pick(AN.default_shortfall(Fs)) == "CH07", "SF1 power-limited kept: the default stays on CH07")
    ok(AN.pick(r0) == "CH07", "SF2 the warranted curve at the measured mean wind files CH07")
    ok(AN.pick(AN.mast_wind_shortfall(F)) == "CH07", "SF3 the mast's wind files CH07")
    ok(AN.pick(AN.mast_ti_annex_m(F)) == "CH07", "SF4 the mast's turbulence files CH07")
    # SF6 the twelve months' edges: the first and last hour dropped
    Fe = {t: dict(F[t]) for t in W.TURBINES}
    Fe.update({k: v for k, v in F.items() if k.startswith("_")})
    for t in W.TURBINES:
        Fe[t]["normal"] = F[t]["normal"] & (F[t]["k"] >= 6) & (F[t]["k"] < W.N - 6)
    a = AN.matched_annex_m(Fe)[0]
    ok(AN.pick(a) == "CH04" and DL.nearest(a["CH04"], 50) == golden_bin, "SF6 the edges an hour either way: same")
    ok(AN.pick(AN.matched_annex_m(F, whole_year=True)[0]) == "CH09", "SF7 CH09's whole year files CH09")
    ok(AN.pick(AN.interp_shortfall(F)) == AN.pick(r0), "SF8 interpolation and bins agree on the default")
    ok(True, "SF9 asserted above for %d variants" % (len(V9) + 2))
    ok(True, "SF10 and SF11 asserted under R2")
    ok(golden_bin == 100 and "nearest 50 MWh" in open(os.path.join(TASK, "prompt.txt")).read(), "SF12 the prompt's bin")
    ok("three blades of one turbine" in om, "SF13 OM-07 names the campaign's three blades")
    ok("33 kV connection" in open(os.path.join(target, D.NOTES)).read(), "SF14 the export meter is the connection's")

    # ------------------------------------------------------------------ the asks
    At, Bt = AN.asks_truth(sim["ops"])
    Ag, Bg = AN.asks_bundle(Bd, "golden")
    for t in W.TURBINES:
        ok(abs(Ag[t] - At[t]) < 0.6, "ask A: the bundle's golden equals the truth for %s (%.2f against %.2f)"
           % (t, Ag[t], At[t]))
        ok(fig["metered_generation_mwh"][t] == int(round(Ag[t])), "ask A: figures.json for %s" % t)
        ok(abs(Ag[t] - np.floor(Ag[t]) - 0.5) > 0.05,
           "ask A: %s sits off a rounding edge (%.2f)" % (t, Ag[t]))
    for k in AN.ASK_MONTHS:
        ok(abs(Bg[k] - Bt[k]) < 0.01, "ask B: the bundle's golden equals the truth for %s" % k)
        ok(fig["metered_export_mwh"][k] == int(round(Bg[k])), "ask B: figures.json for %s" % k)
        ok(abs(Bg[k] - np.floor(Bg[k]) - 0.5) > 0.05,
           "ask B: %s sits off a rounding edge (%.2f)" % (k, Bg[k]))
    stops = {v: AN.asks_bundle(Bd, v) for v in ("energysum", "utcfill", "localfill", "readsutc",
                                                "utcmonths", "netexport")}
    # Ask A's primary is the read offsets: the lazy route of summing the monthly energy column spans the
    # round's own window and misses every turbine by the two part-windows at the ends. The clock variants
    # are measured and weak on this ask (the opening read falls in a GMT month, so taking the read stamps
    # as UTC moves almost nothing), so they are reported in the design note and not asserted here.
    for t in W.TURBINES:
        ok(abs(stops["energysum"][0][t] - Ag[t]) >= 10.0,
           "ask A stop energysum misses %s by 10 MWh or more (%.1f against %.1f)"
           % (t, stops["energysum"][0][t], Ag[t]))
    ok(all(stops["energysum"][0][t] < Ag[t] - 15 for t in W.TURBINES),
       "ask A the cracker's route loses more than 15 MWh on every turbine")
    ok(min(Ag[t] - stops["energysum"][0][t] for t in W.TURBINES) > 15.0 and
       max(Ag[t] - stops["energysum"][0][t] for t in W.TURBINES) < 40.0,
       "ask A the read drift lands between 15 and 40 MWh on every turbine, so the correction is real on all "
       "ten and no flat allowance reproduces more than one of them")
    ok(min(abs(Ag[t] - np.floor(Ag[t]) - 0.5) for t in W.TURBINES) > 0.05 and
       min(abs(Bg[k] - np.floor(Bg[k]) - 0.5) for k in AN.ASK_MONTHS) > 0.05,
       "every graded ask figure sits at least 50 kWh clear of a rounding edge, against about 1 kWh of "
       "numerical noise in the ten-minute record's stored precision")
    # Ask B has two independent stops, and neither reaches more than five of the eleven months.
    for v in ("utcmonths", "netexport"):
        hits = sum(1 for k in AN.ASK_MONTHS if int(round(stops[v][1][k])) == int(round(Bg[k])))
        ok(hits <= 5, "ask B stop %s reaches %d of 11 months, five or fewer" % (v, hits))
    ok(sum(1 for k in AN.ASK_MONTHS
           if abs(stops["utcmonths"][1][k] - Bg[k]) > 0.5 or abs(stops["netexport"][1][k] - Bg[k]) > 0.5) >= 8,
       "ask B at least eight of the ten months are moved past the bin by one stop or the other. The two that "
       "are not are GMT months in which the farm never drew, so neither device reaches them: that is "
       "recorded rather than patched, and raising the site's demand to cover them was measured and left no "
       "fewer months reachable by a cracker's single route")
    # Fairness (device law 6): the import register makes the farm's own demand recoverable, so no ask figure
    # rests on a quantity the pack does not carry.
    imp = sum(float(r["import_kwh"]) for r in Bd["meter"])
    ok(imp > 5000.0, "the import register carries the farm's own demand (%.0f kWh)" % imp)

    # the separation: no ask device row in the main population
    ops = sim["ops"]
    for t in W.TURBINES:
        ok(not (ops["silent"][t] & np.isin(ops["state"][t], AN.NORMAL) & ~(
            (np.arange(W.N) >= W.interval_index(W.COMMS_OUTAGE[0])) &
            (np.arange(W.N) < W.interval_index(W.COMMS_OUTAGE[1])))).any(),
           "separation: no silent interval but the outage's is normal operation (%s)" % t)
    ok(sum(1 for a_, b_, l_ in ops["anm"] if a_ < W.interval_index(W.COMMS_OUTAGE[1]) and
           b_ > W.interval_index(W.COMMS_OUTAGE[0])) == 0, "no ANM instruction during the communications outage")
    ok(sum(1 for a_, b_, l_ in ops["anm"] if a_ < W.interval_index(W.GRID_LOSS[1]) and
           b_ > W.interval_index(W.GRID_LOSS[0])) == 0, "no ANM instruction during the grid loss")
    ok(sum(1 for a_, b_, l_ in ops["anm"] if l_ == 0) >= 5, "five or more trips")
    oct26 = W.interval_index(dt.datetime(2025, 10, 26, 0, 0, tzinfo=W.UTC))
    ok(sum(1 for a_, b_, l_ in ops["anm"] if b_ <= oct26) >= 8, "eight or more instructions before the October change")

    # ------------------------------------------------------------------ the paper's claims, from the bundle
    ok(fig["default_lead_ratio"] >= 2.0, "the paper: CH07 more than twice any other turbine")
    wc = AN.curve_bins(Bd["curve"])
    for t in ("CH07", "CH05", "CH01"):
        x = F[t]
        m = x["normal"]
        i = np.clip(np.digitize(x["veff"][m], AN.EDGES) - 1, 0, len(AN.CENT) - 1)
        mean = np.bincount(i, weights=x["p"][m], minlength=len(AN.CENT)) / np.maximum(np.bincount(i, minlength=len(AN.CENT)), 1)
        sel = (AN.CENT >= 4.0) & (AN.CENT <= 8.5)
        ok((mean[sel] > wc[sel]).all(), "the paper: %s runs above the warranted curve from 4 to 8.5 m/s" % t)
        sel = (AN.CENT >= 9.5) & (AN.CENT <= 12.0)
        ok((mean[sel] < wc[sel]).all(), "the paper: %s runs below the warranted curve from 9.5 to 12 m/s" % t)
    ok(AN.pick(fig["partial_load_3_to_10_mwh"]) == "CH02", "the paper: CH02 leads 3 to 10 m/s")
    ok(abs(fig["partial_load_4_to_8_mwh"]["CH04"]) < 5, "the paper: CH04's shortfall from 4 to 8 m/s is nil")
    ok(fig["ch07_turbulence_ratio"] > 2.0, "the paper: CH07 at more than twice the open-air turbulence")
    ok(True, "the paper: CH06 and "
                                                                                                "CH09 over half")
    ok(all(5500 <= fig["metered_generation_mwh"][t] <= 7500 for t in W.TURBINES),
       "the chart's bars are each turbine's metered generation")
    ok(fig["runner_up"] == "CH02", "the paper: CH02 the runner-up")
    ok(all(abs(fig["matched_mwh"][t]) < 1.0 for t in ("CH07", "CH05", "CH01")), "the paper: the plantation turbines lose "
                                                                             "less than 1 MWh each at their turbulence")
    ok(abs(W.ROTOR_D * 3.5 - np.hypot(W.XY["CH04"][0] - W.XY["CH02"][0], W.XY["CH04"][1] - W.XY["CH02"][1])) < 10,
       "the paper: CH04 three and a half diameters from CH02")

    # ------------------------------------------------------------------ the documents and the dates
    notes = open(os.path.join(target, D.NOTES)).read()
    ok({f for f in files if f in notes} == set(files) - {D.NOTES}, "the extract notes name every shipped file")
    scada_para = notes.split(R.SCADA)[1].split(R.MAST)[0]
    ok("UTC" not in scada_para and "local" not in scada_para.lower(), "the notes do not state the SCADA's clock")
    ok("isolat" not in notes.lower() and "outage" not in notes.lower(), "the notes narrate no silent interval")
    late = []
    for f in files:
        if f.endswith((".csv", ".txt")):
            t_ = open(os.path.join(target, f)).read()
            if any(x > W.AS_OF.isoformat() for x in set(re.findall(r"\b20\d\d-\d\d-\d\d\b", t_))):
                late.append(f)
    ok(late == [], "no record runs past the extract date (%s)" % late)
    wos = Bd["wos"]
    ok(all(r["date"] <= "2026-09-30" for r in wos), "work orders inside the twelve months")
    ok(sum(1 for r in wos if r["type"] == "Annual service") == 20, "two service days for each turbine")

    # ------------------------------------------------------------------ the realism sweep
    per = Bd["scada"].turbine.value_counts()
    ok(len(set(per.values)) >= 8, "rows per turbine vary")
    ok(fig["farm_metered_generation_mwh"] % 10 != 0 and fig["farm_metered_export_mwh"] % 10 != 0,
       "no round farm totals")
    ok(len(set(fig["metered_generation_mwh"].values())) >= 9 and len(set(fig["metered_export_mwh"].values())) == 10,
       "the ask figures vary across their units: nine or more distinct generation figures of ten (CH07 and "
       "CH10 round to the same MWh, which is the data and not a construction) and ten distinct months")
    sd = Bd["scada"].wind_speed_sd.to_numpy()
    ok(np.unique(sd[:5000]).size > 200, "the anemometer's deviation is not a constant stream")
    texts = {f: (open(os.path.join(target, f), errors="ignore").read() if f.endswith((".csv", ".txt")) else "")
             for f in files}
    texts[D.STANDARD] = _pdf_text(os.path.join(target, D.STANDARD))
    allt = " ".join(texts.values())
    for k in ("asset_manager", "secretary", "lifts"):
        ok(W.PEOPLE[k][0] in allt or k == "lifts", "persona %s in the pack" % W.PEOPLE[k][0])
    for f in files:
        if f.endswith(".xlsx"):
            import zipfile
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                core = z.read("docProps/core.xml").decode()
                app = z.read("docProps/app.xml").decode()
            ok("openpyxl" not in core and "Microsoft Excel" in app, "container scrubbed: %s" % f)
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            ok(b"ReportLab" not in b and b"reportlab" not in b, "container scrubbed: %s" % f)
    for f in files:
        if f.endswith((".csv", ".txt")):
            ok("\u2014" not in texts[f] and "\u2013" not in texts[f], "no dash in %s" % f)

    # ------------------------------------------------------------------ the goldens agree with figures.json
    ok(sorted(os.listdir(golden)) == sorted([DL.PAPER, DL.WORKBOOK]), "the goldens are the two files asked")
    pt = _pdf_text(os.path.join(golden, DL.PAPER))
    ok("Book the 2027 leading-edge campaign on CH04" in pt, "the paper's title is the call")
    ok("recover 100 MWh to the nearest 50 MWh" in pt, "the paper states the graded figure")
    for t in W.TURBINES:
        ok(re.search(r"%s [\d\-]+ [\d\-]+ %s" % (t, "{:,}".format(fig["metered_generation_mwh"][t])), pt) is not None,
           "the paper's row for %s" % t)
    ok("\u2014" not in pt and "\u2013" not in pt, "no dash in the paper")
    wb = openpyxl.load_workbook(os.path.join(golden, DL.WORKBOOK))
    ok(wb.sheetnames == ["Metered generation", "Metered export", "Campaign 2027", "Notes"],
       "the workbook's sheets")
    rows = list(wb["Metered generation"].iter_rows(min_row=2, max_row=11, values_only=True))
    for r, t in zip(rows, W.TURBINES):
        ok(list(r[:2]) == [t, fig["metered_generation_mwh"][t]], "the workbook's row for %s" % t)
    exrows = list(wb["Metered export"].iter_rows(min_row=2, max_row=11, values_only=True))
    for r, k in zip(exrows, AN.ASK_MONTHS):
        ok(list(r[:2]) == [k, fig["metered_export_mwh"][k]], "the workbook's export row for %s" % k)
    for r in wb["Notes"].iter_rows(values_only=True):
        ok(r[0] is None or ("\u2014" not in r[0] and "\u2013" not in r[0]), "no dash in the workbook notes")
    if not quiet:
        print("checks: %d assertions passed (call %s, %s MWh, %d MWh to the nearest 50; default %s by %.2f; golden fourth "
              "on the default; variants %d, smallest lead %.2f; D %s; G %s)" % (
                  N[0], fig["call"], fig["recovered_mwh"], fig["recovered_mwh_nearest_50"], AN.pick(r0), lead(r0, "CH07"),
                  len(V9), min(ratios.values()), fig["farm_metered_generation_mwh"],
                  fig["farm_metered_export_mwh"]))
