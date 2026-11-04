"""The generator's assertions on the built pack and its clean truth: the three rules (R1 to R3c), the ladder and its
margins, the semantic fork table (SF1 to SF18), mess neutrality, bin edges, the ask devices and their separation
from the main call, the input gates, the realism sweep and the documents read back with positive controls."""
import csv
import datetime as dt
import json
import os
import re
from collections import Counter, defaultdict

import golden as G
import reader as R
import sim as S
import world as W

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def edge(v, unit):
    """Distance from v to the nearest edge of the cell it prints in at unit."""
    return unit / 2 - abs(v - round(v / unit) * unit)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as p:
        return "\n".join((pg.extract_text() or "") for pg in p.pages)


def run(target, golden_dir, xy=None, n=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    x, y = xy
    c = G.compute(target)
    fig = json.load(open(fig_path))
    ld = c["load"]
    tot = lambda r: sum(ld[r].values())
    stack = sum(c["stack"].values())

    # ------------------------------------------------------------------ R1: the field's raw material ships
    tms = R.tms_loads(target)
    ok("R1 every 2026 load ships with its gross litres and meter temperature at compartment grain",
       all(l["gross"] > 0 and 5 < l["temp"] < 40 for l in tms) and len(tms) > 30000, "%d loads" % len(tms))
    ok("R1 every distillate load has a previous drop of its own compartment in the dockets", c["missing"] == 0,
       "%d without" % c["missing"])
    heads = []
    for k in ("tas_old", "dockets", "sites", "vru_cems", "vru_plc", "gauging", "shiftlog", "workorders"):
        with open(os.path.join(target, W.FILES[k]), encoding="utf-8") as f:
            heads += next(csv.reader(f))
    ok("R1 no shipped column holds the deciding quantity (a previous product, a vapour state, a switch flag)",
       not any(re.search(r"prev|vapou?r_state|switch|last_prod|arrival", h, re.I) for h in heads), str(heads)[:120])

    # ------------------------------------------------------------------ R3a, R3b: the analyst test on the clean truth
    truth = [l for l in x["loads"] if l["terminal"] == "WARRENBY" and l["bay"] in W.DISTILLATE_BAYS
             and W.YEAR_START_UTC <= l["utc"] < W.YEAR_END_UTC]
    t_g = sum(S.load_vapour(l) for l in truth) / 1000
    t_r0 = sum(l["gross"] / 1000 * W.vapour_kg_per_kl("diesel", l["temp"], 0.6) for l in truth) / 1000
    vru_true = sum(v for k, v in y["outlet_15"].items() if W.YEAR_START_UTC <= k < W.YEAR_END_UTC) / 1000
    ok("R3a the easy route on the clean truth (each load at its own product's vapour pressure) files a release "
       "within the 20-tonne limit", t_r0 + vru_true < W.LIMIT_T * 0.2, "%.2f t" % (t_r0 + vru_true))
    ok("R3a the clean truth's release is over the limit", t_g + vru_true > W.LIMIT_T * 1.5, "%.2f t" % (t_g + vru_true))
    ok("R3b the pack's golden reproduces the clean truth's distillate release", abs(tot("G") - t_g) < 0.05,
       "%.3f against %.3f" % (tot("G"), t_g))
    ok("R3b the decisive step alone (previous delivery from the dockets) turns the easy route into the golden",
       abs(tot("G") + stack - c["total"]) < 1e-6 and tot("R0") < 1.0)
    ok("R3b each lower rung's single correction leaves a wrong figure: exports-only history at %.2f of the golden"
       % (tot("R2") / tot("G")), tot("G") / tot("R2") >= 1.15)
    ok("R3b every retail diesel load at petrol vapour overshoots by 1.15x or more", tot("R1") / tot("G") >= 1.15,
       "%.2f" % (tot("R1") / tot("G")))
    ok("R3b saturation 0.6 on the switched loads still files over the limit", tot("G_s06") + stack > W.LIMIT_T,
       "%.2f t" % (tot("G_s06") + stack))
    fam = {s: tot("R0") * s / 0.6 + stack for s in (0.5, 0.6, 1.0, 1.45)}
    ok("R3a the per-product equation at every saturation factor of the field's table (0.5 to 1.45) files within the "
       "limit", max(fam.values()) < W.LIMIT_T, " ".join("S %.2f: %.2f t" % kv for kv in sorted(fam.items())))
    pl_ = c["per_load"]
    retail = [p for p in pl_ if p["l"]["operator"] == "BRN"]
    sw_ = [p for p in pl_ if p["switch"]]
    ex_ = [p for p in sw_ if p["prev"]["terminal"] != "WARRENBY"]
    ok("R3b the switch fills are ordinary: about half the retail fleet's distillate loads, a large part after a drop "
       "of petrol lifted at Selwyn Point", 0.3 < len(sw_) / len(retail) < 0.7 and len(ex_) / len(sw_) > 0.2,
       "%d of %d retail loads (%.1f per cent), %d of them (%.1f per cent) after a Selwyn Point drop" % (
           len(sw_), len(retail), 100.0 * len(sw_) / len(retail), len(ex_), 100.0 * len(ex_) / len(sw_)))
    # R3c: no plant
    old = list(csv.DictReader(open(os.path.join(target, W.FILES["tas_old"]), encoding="utf-8")))
    blocks = Counter(tuple(r[k] for k in ("GROSS_L", "TEMPERATURE", "VCF")) for r in old)
    ok("R3c no copied block in the loads (no gross, temperature and VCF triple repeated more than a handful of times)",
       max(blocks.values()) <= 6, "max repeat %d" % max(blocks.values()))
    ok("R3c no memo, draft, prior return or stakeholder figure ships",
       not any(re.search(r"memo|draft|prior_return|briefing|email|notes|readme|dictionary|manifest", f, re.I)
               for f in os.listdir(target)))

    # ------------------------------------------------------------------ the semantic fork table, each row computed
    loads = c["per_load"]

    def call_of(variant_dist):
        return variant_dist + stack > W.LIMIT_T

    def dist(res):
        return sum(res["G"].values())

    def same_bins(res):
        return all(round(res["G"].get((bay, qi), 0.0), 1) == round(c["quarters"][("BAY-%d" % bay, qi)], 1)
                   for bay in (4, 5) for qi in range(1, 5))
    ok("SF1 the release counts every distillate load in calendar 2026 local time, each at its own compartment's "
       "vapour", all(pl["l"]["local"].year == 2026 for pl in loads) and len(loads) > 15000, "%d loads" % len(loads))
    v_utc, _, _ = G.loading(target, window=(dt.datetime(2026, 1, 1, 11), dt.datetime(2027, 1, 1, 11)))
    ok("SF2 a UTC calendar year keeps the call", call_of(dist(v_utc)), "%.2f t" % dist(v_utc))
    v_net, _, _ = G.loading(target, volume="net")
    ok("SF3 net 15 C litres instead of the observed litres keep the call, and protocol 4.4 files the observed volume",
       call_of(dist(v_net)) and "observed volume" in pdf_text(os.path.join(target, W.FILES["protocol"])),
       "%.3f t" % dist(v_net))
    v_mon, _, _ = G.loading(target, temp_mode="month")
    ok("SF4 a month's mean product temperature instead of each load's meter temperature (protocol 4.4) keeps the "
       "call and every quarter's bin", call_of(dist(v_mon)) and same_bins(v_mon), "%.3f t" % dist(v_mon))
    v_sea, _, _ = G.loading(target, season_mode="previous")
    ok("SF5 the previous drop's grade season instead of the load month's (protocol 4.3) keeps the call",
       call_of(dist(v_sea)), "%.3f t" % dist(v_sea))
    ok("SF6 saturation 1.0 for a compartment back from a vapour-balanced petrol drop; 0.6 keeps the call",
       call_of(tot("G_s06")), "%.2f t" % (tot("G_s06") + stack))
    v_sh, _, _ = G.loading(target, tms_kw=dict(keep_shadow=True))
    ok("SF7 the 29 and 30 June shadow-run rows counted twice keep the call", call_of(dist(v_sh)), "%.3f t" % dist(v_sh))
    v_can, _, _ = G.loading(target, tms_kw=dict(keep_cancelled=True))
    ok("SF8 cancelled transactions counted as loads keep the call", call_of(dist(v_can)), "%.3f t" % dist(v_can))
    v_dog, _, _ = G.loading(target, tms_kw=dict(dog_through=False))
    ok("SF9 a B-double's dog compartments left at 1 to 4 in the legacy export keep the call", call_of(dist(v_dog)),
       "%.3f t" % dist(v_dog))
    v_pl, _, _ = G.loading(target, tms_kw=dict(current_plates_only=True))
    ok("SF10 a re-registered trailer's loads under its old plate dropped keep the call", call_of(dist(v_pl)),
       "%.3f t" % dist(v_pl))
    spare = sum(1 for pl in loads if pl["prev"] is not None and (pl["l"]["local"] - pl["prev"]["done"]).days >= 2)
    ok("SF11 a compartment carried empty keeps the vapour of its last drop: %d loads follow a drop two or more days "
       "earlier" % spare, spare > 0)
    ok("SF12 the year is over the limit by more than any rounding", c["total"] - W.LIMIT_T > 5)
    rows = R.cems(target)
    cal0 = sum(r_["rate"] or 0.0 for r_ in rows) * 0.25 / 1000
    ok("SF13 VRU-1 with each CAL interval at zero instead of the hour either side keeps the call", cal0 + tot("G") >
       W.LIMIT_T, "%.3f t" % cal0)
    ok("SF14 a switched load's petrol vapour in place of, not beside, diesel's own keeps the call and every "
       "quarter's bin", call_of(tot("G_replace")) and all(round(ld["G_replace"].get((bay, qi), 0.0), 1) ==
                                                      round(c["quarters"][("BAY-%d" % bay, qi)], 1)
                                                      for bay in (4, 5) for qi in range(1, 5)),
       "%.3f t" % tot("G_replace"))
    dks = R.dockets(target)
    by = defaultdict(set)
    for d in dks:
        by[(d["ref"], d["unit"], d["comp"])].add(d["product"])
    ok("SF15 a compartment split between two sites delivered one product", all(len(v) == 1 for v in by.values()))
    ok("SF16 no receipt or transfer runs between a quarter's opening midnight and its 06:00 AEST dip (asserted inside "
       "golden.stock_account, which ran)", len(c["gain"]) == 20)
    ok("SF17 the tank method's day rule is filed (protocol 5.2: the seal at the start of the day)",
       "start of that day" in pdf_text(os.path.join(target, W.FILES["protocol"])).replace("\n", " "))
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    ok("SF18 the rounding is the prompt's own closing sentence (tonnes to one decimal, whole kilograms and kilolitres)",
       prompt.rstrip().endswith("Tonnes to one decimal, kilograms and kilolitres to the nearest whole unit.")
       and "kilolitres at 15 C" in prompt and "local midnight" in prompt)

    # ------------------------------------------------------------------ R2: every Layer 1 item mishandled keeps the call
    v_raw, _, _ = G.loading(target)
    ok("R2 the dockets' offsets dropped leave their wall time, the terminal's clock (the golden's own reading)",
       abs(dist(v_raw) - tot("G")) < 1e-9)
    for nm, v in (("shadow rows", v_sh), ("cancelled rows", v_can), ("dog numbering", v_dog), ("old plates", v_pl),
                  ("UTC year", v_utc)):
        ok("R2 %s mishandled keep the call" % nm, call_of(dist(v)))
    raw = list(csv.DictReader(open(os.path.join(target, W.FILES["vru_cems"]), encoding="utf-8")))
    as_kgh = sum(float(r_["value"]) for r_ in raw if r_["value"]) * 0.25 / 1000
    dropped = sum(float(r_["value"]) for r_ in raw if r_["value"] and r_["unit"] == "kg/h") * 0.25 / 1000
    ok("R2 the VRU channel's g/min read as kg/h, or the new channel left out, keep the call",
       as_kgh + tot("G") > W.LIMIT_T and dropped + tot("G") > W.LIMIT_T, "%.2f and %.2f t" % (as_kgh, dropped))

    # ------------------------------------------------------------------ bins
    # The loading equation's two constant forms a solver may use: the field's US-unit form (12.46 S P M / T in lb per
    # 1000 gal, psia and degrees Rankine, converted to kg per kL) and the exact gas constant in place of 8.314. Both
    # scale every distillate-bay figure uniformly; each figure must keep its bin under both, and sit clear of its edge
    # by at least twice the largest shift either puts on a quarter.
    f_us = 12.46 * 0.1450377 * (0.45359237 / 3.785411784) / 1.8 * W.R_GAS
    f_r = W.R_GAS / 8.314462618
    shift = max(abs(v * (f - 1)) for (p, qi), v in c["quarters"].items() if p != "VRU-1" for f in (f_us, f_r))
    floor = max(0.004, 2 * shift)
    for p in ("VRU-1", "BAY-4", "BAY-5"):
        for qi in range(1, 5):
            v = c["quarters"][(p, qi)]
            fs = (1.0,) if p == "VRU-1" else (f_us, f_r)
            ok("bin %s Q%d %.3f t clear of its 0.1 t edge by %.4f, its bin kept under both constant forms"
               % (p, qi, v, floor), edge(v, 0.1) >= floor and all(round(v * f, 1) == round(v, 1) for f in fs),
               "%.4f" % edge(v, 0.1))
    bays = sum(v for (p, qi), v in c["quarters"].items() if p != "VRU-1")
    vru_t = sum(v for (p, qi), v in c["quarters"].items() if p == "VRU-1")
    for nm, v, off in (("total", c["total"], 0.0), ("excess", c["excess"], W.LIMIT_T)):
        ok("bin %s %.3f t, its bin kept under both constant forms" % (nm, v),
           edge(v, 0.1) >= floor and all(round(bays * f + vru_t - off, 1) == round(v, 1) for f in (f_us, f_r)),
           "%.4f" % edge(v, 0.1))
    for tk, v in c["tanks"].items():
        ok("bin %s %.2f kg (filed rates, whole days, exact litres: no convention moves it)" % (tk, v),
           edge(v, 1.0) >= 0.01, "%.3f" % edge(v, 1.0))
    # The legacy export's net litres: gross times its printed VCF (the golden), that product rounded to whole litres
    # per load (the measurement standard's practice), or the VCF recomputed unrounded from the 54B form at the row's
    # own temperature and density. Each gain keeps its whole kilolitre under all three; the new TMS files its net.
    g_rn, _ = G.stock_account(target, tms_kw=dict(round_net=True))
    g_tb, _ = G.stock_account(target, tms_kw=dict(vcf_table=True))
    for k, v in c["gain"].items():
        ok("bin %s Q%d gain %.3f kL, its whole kL kept under per-load rounding (%.3f) and the unrounded VCF (%.3f)"
           % (k + (v, g_rn[k], g_tb[k])), edge(v, 1.0) >= 0.002 and round(g_rn[k]) == round(v) == round(g_tb[k]),
           "%.3f" % edge(v, 1.0))

    # ------------------------------------------------------------------ the asks' devices and separation
    gn, _ = G.stock_account(target, night_shift_dates=False)
    gr, _ = G.stock_account(target, with_returns=False)
    moved_n = [k for k in c["gain"] if round(gn[k]) != round(c["gain"][k])]
    moved_r = [k for k in c["gain"] if round(gr[k]) != round(c["gain"][k])]
    ok("ask A primary D7: the line-up read on calendar dates moves every diesel tank cell", len(moved_n) == 8,
       str(sorted(moved_n)))
    ok("ask A primary D4: leaving out VRU-1's returns moves every TK-1 cell and the absorber's line-ups move TK-2 Q3, "
       "TK-3 Q3 and TK-3 Q4", sorted(moved_r) == sorted([("TK-1", q) for q in range(1, 5)] +
                                                       [("TK-2", 3), ("TK-3", 3), ("TK-3", 4)]), str(sorted(moved_r)))
    g1, _ = G.stock_account(target, returns_to_tk1=True)
    moved_1 = [k for k in c["gain"] if round(g1[k]) != round(c["gain"][k])]
    ok("ask A D4 second half: every return booked to TK-1 (the pump's usual tank) moves TK-1 Q3, TK-1 Q4, TK-2 Q3, "
       "TK-3 Q3 and TK-3 Q4", sorted(moved_1) == sorted([("TK-1", 3), ("TK-1", 4), ("TK-2", 3), ("TK-3", 3),
                                                        ("TK-3", 4)]), str(sorted(moved_1)))
    gd, _ = G.stock_account(target, dip_offset=False)
    moved_d = [k for k in c["gain"] if round(gd[k]) != round(c["gain"][k])]
    ok("ask A primary D8: the gauging's AEST dips read on the terminal's clock move cells of every tank",
       {k[0] for k in moved_d} == set(W.TANKS) and all(k[1] != 3 for k in moved_d), str(sorted(moved_d)))
    gc, _ = G.stock_account(target, night_shift_dates=False, with_returns=False, dip_offset=False)
    kept = [k for k in c["gain"] if round(gc[k]) == round(c["gain"][k])]
    ok("ask A: the careful route that misses the three primaries keeps no cell", not kept, str(sorted(kept)))
    tn = G.tank_voc(target, seal_history=False)
    ok("ask B primary D2: the register's current seals and vents miss every tank", all(
        round(tn[t]) != round(c["tanks"][t]) for t in W.TANKS), str({t: round(tn[t]) for t in W.TANKS}))
    ok("realism: no two tanks release the same whole kilograms", len({round(v) for v in c["tanks"].values()}) == 5)
    gm, _ = G.stock_account(target, with_manual=False)
    moved_m = [k for k in c["gain"] if round(gm[k]) != round(c["gain"][k])]
    ok("ask A D4b: the petrol rack's loads on manual BOLs, which only the dispatch dockets hold, move the fault "
       "quarters' petrol cells when left out", bool(moved_m) and all(k[0] in ("TK-1", "TK-2", "TK-3") and k[1] in (2, 4)
                                                                     for k in moved_m), str(sorted(moved_m)))
    gp, _ = G.stock_account(target, manual_per_line=True)
    moved_p = [k for k in c["gain"] if round(gp[k]) != round(c["gain"][k])]
    ok("ask A D4b second half: a split compartment's bill quantity, printed on each of its docket lines, summed per "
       "line moves a fault-quarter cell", bool(moved_p), str(sorted(moved_p)))
    gf, _ = G.stock_account(target, returns_to_tk1=True, manual_per_line=True)
    moved_f = [k for k in c["gain"] if round(gf[k]) != round(c["gain"][k])]
    ok("ask A: the full includer (every primary noticed, the returns booked to TK-1, the bill quantities summed per "
       "line) still misses a block of cells", len(moved_f) >= 4, "%d cells: %s" % (len(moved_f), sorted(moved_f)))
    main_files = {W.FILES[k] for k in ("tas_old", "tas_new", "dockets", "tankers", "vru_cems", "protocol", "licence")}
    ask_organs = {W.FILES[k] for k in ("vru_plc", "gauging", "shiftlog", "workorders", "tankreg", "outturns")}
    real_dockets = R.dockets
    R.dockets = lambda t, **kw: [dict(d, ref="X", loaded=0) for d in real_dockets(t, **kw)]
    try:
        blind, _, _ = G.loading(target)
    finally:
        R.dockets = real_dockets
    ok("separation: the asks' organs sit in files the main call never reads, and the dockets' manual-BOL device in "
       "columns it never reads (the release is unchanged with source_doc and bol_litres_15c blanked)",
       not (main_files & ask_organs) and abs(sum(blind["G"].values()) - tot("G")) < 1e-9)

    # ------------------------------------------------------------------ input gates
    files = os.listdir(target)
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", big >= 25000, str(big))
    meta = json.load(open(meta_path))
    ok("input gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    ok("no file under target/ describes the data", not any(re.search(r"readme|dictionary|manifest|field_notes|"
                                                                      r"codebook|schema", f, re.I) for f in files))

    # ------------------------------------------------------------------ realism sweep
    sites = list(csv.DictReader(open(os.path.join(target, W.FILES["sites"]), encoding="utf-8")))
    codes = sorted(int(s["site_code"][1:]) for s in sites)
    steps = {b - a for a, b in zip(codes, codes[1:])}
    ok("realism: site codes are no arithmetic sequence", len(steps) > 5)
    shapes = Counter(len(s["site_name"].split()) for s in sites)
    ok("realism: site names take more than two shapes", len(shapes) > 2)
    q_counts = Counter((l["local"].month - 1) // 3 for l in tms if l["local"].year == 2026)
    ok("realism: no identical load counts across quarters", len(set(q_counts.values())) == len(q_counts))
    ok("realism: the year's release is no round figure", edge(c["total"], 1.0) < 0.45)

    # ------------------------------------------------------------------ documents read back, with positive controls
    lic = pdf_text(os.path.join(target, W.FILES["licence"]))
    pro = pdf_text(os.path.join(target, W.FILES["protocol"]))
    ok("doc: the licence reads back and states the 20-tonne limit (positive control)",
       len(lic) > 1000 and "must not exceed 20 tonnes in any calendar year" in lic.replace("\n", " "))
    ok("doc: the protocol reads back with Table 1's petrol rows", "13.687" in pro and "2952.8" in pro and
       "2891.9" in pro and "4948.3" in pro)
    flat = re.sub(r"\s+", " ", pro + " " + lic).lower()
    ok("doc: no governing sentence names a compartment's previous load, vapour balance, saturation or switching",
       not re.search(r"previous (load|deliver|cargo)|vapour balanc|vapor balanc|saturat|switch load|dedicated "
                     r"service|carried back|compartment", flat))
    ok("doc: the protocol files no loading equation", "s p m" not in flat and "12.46" not in flat)

    # ------------------------------------------------------------------ figures.json carries the call
    ok("figures.json carries the call", abs(fig["call"]["total_t"] - round(c["total"], 1)) < 1e-9)
    good = all(r[1] for r in RESULTS)
    for name, passed, detail in RESULTS:
        if not passed:
            print("FAIL", name, detail)
    print("checks: %d of %d passed" % (sum(1 for r in RESULTS if r[1]), len(RESULTS)))
    return good
