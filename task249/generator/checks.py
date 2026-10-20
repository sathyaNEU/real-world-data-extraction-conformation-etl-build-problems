"""task249 generator checks: the input gates, the three rules on the clean truth, the ladder, the forcing of the
method by the samples, every semantic fork row, the separation line, the asks' devices and margins, the realism sweep
and the document dates.   C.run(target, world, fig, golden) -> number of assertions passed"""
import json
import os
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader

import params as P
import records as R
import routes as RT
import sim
import solve as S

N_OK = [0]


def ok(cond, msg):
    assert cond, msg
    N_OK[0] += 1


def _pdf_text(path):
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


GOLDEN_SET = ["ESK", "FND", "JVB", "SKB"]
LADDER = {"refit": [], "with_discharge": [], "flow_class": [], "season": ["JVB"], "discharge_and_season": ["JVB"],
          "hour_of_day": ["JVB"], "trip_type": ["ESK", "FND", "SKB", "TVE"],
          "trip_type_and_more": ["ESK", "FND", "JVB", "SKB", "TVE"], "routine_only": ["ESK", "GRV", "TVE"],
          "only_2027": ["JVB", "SKB"]}


def _ols_t(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    r = y - X @ b
    s2 = r @ r / (len(y) - X.shape[1])
    cov = s2 * np.linalg.pinv(X.T @ X)
    return b, b / np.sqrt(np.maximum(np.diag(cov), 1e-30)), float(np.sqrt(s2))


def run(target, world, fig, golden):
    N_OK[0] = 0
    F = world["F"]
    W, H, Sm, pub = world["W"], world["H"], world["S"], world["pub"]
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "metadata.json")))

    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    rec = S.record(target)
    ok(len(pd.read_parquet(os.path.join(target, F["record"]))) >= 25000, "a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors shipped")
    ok(not any("distract" in f.lower() for f in files), "no distractor named as one")

    # ---------------------------------------------------------------- the call
    smp = S.samples(target)
    call = S.the_call(target, rec, smp)
    over = sorted(c for c, v in call.items() if v["verdict"] == "over")
    under = sorted(c for c, v in call.items() if v["verdict"] == "under")
    ok(over == GOLDEN_SET and under == [], "the golden: %s over, none under" % over)
    ok(fig["call"]["over"] == over and fig["call"]["under"] == under, "figures.json carries the call")
    tab = RT.all_routes(target, rec, smp)
    for r in RT.GOLDEN_FAMILY:
        ok(RT.flagged(tab, r) == GOLDEN_SET, "golden family member %s files the golden" % r)
        ok(min(tab[c][r] for c in GOLDEN_SET) > 18.0, "%s: every flagged station 3 points clear of 15" % r)
        ok(max(abs(tab[c][r]) for c in tab if c not in GOLDEN_SET) < 8.0, "%s: every other station 7 clear" % r)
    # the ladder: each reflex files its own wrong set
    for r, want in LADDER.items():
        ok(RT.flagged(tab, r) == want, "rung %s files %s (got %s)" % (r, want, RT.flagged(tab, r)))
        ok(RT.flagged(tab, r) != GOLDEN_SET, "rung %s is not the golden" % r)
    # the default path reproduces the published loads
    for c in tab:
        ok(abs(tab[c]["refit"]) < 0.1, "the refit reproduces %s's published load" % c)

    # ---------------------------------------------------------------- the samples force the method
    for code in sorted(smp["station"].unique()):
        d = RT.station_arrays(rec, smp, code)
        q, T, k, y = d["q"], d["T"], d["k"], d["y"]
        rs = np.convolve(np.gradient(q) / 0.25 / q, np.ones(4) / 4, "same")
        rise = (rs[k] > S.RISE).astype(float)
        x = np.log10(T[k])
        one = np.ones(len(k))
        _, _, se_slr = _ols_t(np.c_[one, x], y)
        _, _, se_limb = _ols_t(np.c_[one, x, rise], y)
        b, t, _ = _ols_t(np.c_[one, x, rise, d["callout"].astype(float)], y)
        ok(abs(t[3]) < 2.5, "%s: with rising water in the model the trip type explains nothing (t %.1f)" % (code, t[3]))
        lq = np.log10(q[k])
        c1, s1 = np.cos(2 * np.pi * d["doy"][k] / 365), np.sin(2 * np.pi * d["doy"][k] / 365)
        b2, t2, _ = _ols_t(np.c_[one, x, rise, lq, c1, s1], y)
        if code in GOLDEN_SET:
            ok(t[2] > 10 and se_limb < 0.3 * se_slr, "%s: rising water separates the samples (t %.0f, se %.3f against %.3f)"
               % (code, t[2], se_limb, se_slr))
            ok(t2[2] > 10 and abs(b2[2] - b[2]) < 0.05, "%s: rising water survives discharge and season" % code)
        ok(se_limb < 0.035, "%s: the rising-water relation leaves only the sampling scatter (%.3f)" % (code, se_limb))

    # ---------------------------------------------------------------- R1, R2, R3 on the clean truth
    ok(not any(re.search(r"rising|limb|hysteres|rate_of", c, re.I) for c in rec.columns), "R1: no column holds rising water")
    ok(all(np.isfinite(rec.loc[rec["time_utc"] >= "2027-01-01", "discharge_m3s"])), "R1: the 15-minute discharge ships for 2027")
    truth = {}
    for key in P.KEYS:
        d = W[key]
        q27, tr = d["q"][sim.Y27], d["ssc"][sim.Y27]
        truth[P.CODE[key]] = 100 * (pub[key]["load_exact"] / (np.sum(tr * q27) * 900 / 1e6) - 1)
    ok(sorted(c for c, v in truth.items() if v > 15) == GOLDEN_SET and all(abs(v) < 8 for c, v in truth.items()
       if c not in GOLDEN_SET), "R3: the true sediment that passed puts the same four over: %s" % truth)
    # R3a: the easy route on the clean truth (true turbidity, true sample concentrations, every filed rule applied)
    easy, fixed = {}, {}
    for key in P.KEYS:
        d = W[key]
        idx = d["idx"]
        y = np.log10(d["ssc"][idx])
        x = np.log10(d["T"][idx])
        b = np.linalg.lstsq(np.c_[np.ones(len(x)), x], y, rcond=None)[0]
        bcf = np.mean(10 ** (y - np.c_[np.ones(len(x)), x] @ b))
        est = np.sum(10 ** b[0] * d["T"][sim.Y27] ** b[1] * bcf * d["q"][sim.Y27]) * 900 / 1e6
        true = np.sum(d["ssc"][sim.Y27] * d["q"][sim.Y27]) * 900 / 1e6
        easy[P.CODE[key]] = 100 * (est / true - 1)
        ind = d["rising"][idx].astype(float)
        X = np.c_[np.ones(len(x)), x, ind]
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        bcf = np.mean(10 ** (y - X @ b))
        est2 = np.sum(10 ** (b[0] + b[1] * np.log10(d["T"][sim.Y27]) + b[2] * d["rising"][sim.Y27]) * bcf
                      * d["q"][sim.Y27]) * 900 / 1e6
        fixed[P.CODE[key]] = 100 * (est / est2 - 1)
    ok(sorted(c for c, v in easy.items() if v > 15) == GOLDEN_SET, "R3a: on the clean truth the published method itself overstates the four")
    ok(all(abs(tab[c]["refit"]) < 0.1 for c in tab), "R3a: the easy route (refit, every filed rule) files no station")
    ok(sorted(c for c, v in fixed.items() if abs(v) > 15) == GOLDEN_SET, "R3b: the easy route with only the rising-water term files the golden")
    for r in ("with_discharge", "season", "trip_type", "routine_only", "only_2027"):
        ok(RT.flagged(tab, r) != GOLDEN_SET, "R3b: the single correction %s leaves a wrong answer" % r)
    # R2: each mess item mishandled leaves the call
    lims_new = pd.read_excel(os.path.join(target, F["lims"]), sheet_name="2026-2027")
    alt = smp.copy()
    rep = lims_new[lims_new["status"] == "replaced"]
    ok(len(rep) >= 5, "R2: the laboratory's replaced results ship")
    m = {(int(s[:4]), int(s[5:])): v for s, v in zip(rep["sample_id"], rep["ssc_mg_l"])}
    alt["ssc"] = [m.get((y, b), v) for y, b, v in zip(alt["year"], alt["bottle_no"], alt["ssc"])]
    c2 = S.the_call(target, rec, alt)
    ok(sorted(c for c, v in c2.items() if v["verdict"] == "over") == GOLDEN_SET, "R2 SF6: the replaced results kept: same call")
    c3 = S.the_call(target, rec, smp[smp["year"] > 2025])
    ok(sorted(c for c, v in c3.items() if v["verdict"] == "over") == GOLDEN_SET, "R2 SF7: the 2025 sheet left out: same call")
    dup = pd.read_parquet(os.path.join(target, F["record"]))
    ok(dup.duplicated().sum() > 0 and not dup[dup.duplicated(["station", "time_utc"], keep=False)]["time_utc"]
       .ge(pd.Timestamp("2027-01-01", tz="UTC")).any(), "R2 SF10: the re-sent rows ship, none in 2027")
    # the pairing: the nearest reading against interpolation between readings
    tab_i = {}
    for code in sorted(smp["station"].unique()):
        d = RT.station_arrays(rec, smp, code)
        s_ = smp[smp["station"] == code]
        frac = ((s_["utc"] - pd.Timestamp("2025-01-01", tz="UTC")) / pd.Timedelta("15min")).to_numpy()
        lo = np.floor(frac).astype(int)
        w = frac - lo
        Ti = d["T"][lo] * (1 - w) + d["T"][np.minimum(lo + 1, len(d["T"]) - 1)] * w
        rs = np.convolve(np.gradient(d["q"]) / 0.25 / d["q"], np.ones(4) / 4, "same")
        X = np.c_[np.ones(len(lo)), np.log10(Ti), rs[np.rint(frac).astype(int)] > S.RISE]
        b = np.linalg.lstsq(X, d["y"], rcond=None)[0]
        bcf = np.mean(10 ** (d["y"] - X @ b))
        mm = d["y27"]
        est = np.sum(10 ** (b[0] + b[1] * np.log10(d["T"][mm]) + b[2] * (rs[mm] > S.RISE)) * bcf * d["q"][mm]) * 900 / 1e6
        tab_i[code] = 100 * (S.read_report(target)[code]["load_t"] / est - 1)
    ok(sorted(c for c, v in tab_i.items() if v > 15) == GOLDEN_SET, "R2 SF8: interpolated pairing, same call")
    # R3c: no copied block in the turbidity record (a day's 96 readings never repeat elsewhere)
    seen = set()
    rep_blocks = 0
    for code, g in rec.groupby("station"):
        v = g["turbidity_fnu"].to_numpy()
        for i in range(0, len(v) - 96, 96):
            blk = v[i:i + 96]
            if np.all(blk == blk[0]):
                continue
            h = hash(blk.tobytes())
            rep_blocks += h in seen
            seen.add(h)
    ok(rep_blocks == 0, "R3c: no day of turbidity readings repeats")

    # ---------------------------------------------------------------- semantic fork rows
    rp = S.read_report(target)
    ok(all(abs(rp[P.CODE[k]]["load_t"] - pub[k]["load_exact"]) < 0.51 for k in P.KEYS), "SF2: the report's loads are the procedure's")
    rel_pub = {c: 100 * (1 - v["estimate_t"] / v["published_t"]) for c, v in call.items()}
    ok(sorted(c for c, v in rel_pub.items() if abs(v) > 15) == GOLDEN_SET, "SF3: misstatement against the published load, same call")
    ok(all(v["misstatement_pct"] > 0 for c, v in call.items() if c in GOLDEN_SET), "SF4: all four over")
    proc_t = _pdf_text(os.path.join(target, F["procedure"])).replace("\n", " ")
    ok("2025 to 2027 for the 2027 loads" in proc_t, "SF5: the calibration years are filed (procedure section 6)")
    ok(sorted(c for c, v in call.items() if abs(v["misstatement_pct"]) > 15) == GOLDEN_SET, "SF1: calendar 2027 UTC")
    cc = S.the_call(target, rec, smp, window_shift_steps=-4)   # SF1: the year in Norwegian time starts an hour early
    ok(sorted(c for c, v in cc.items() if v["verdict"] == "over") == GOLDEN_SET
       and all(abs(cc[c]["misstatement_pct"] - call[c]["misstatement_pct"]) < 0.5 for c in call), "SF1: Norwegian calendar year, same call")
    ok(set(rec["station"].unique()) == set(P.CODE.values()) and len(call) == 14, "SF15: the 14 stations")
    # SF12: retransformation (Duan's smearing against none)
    no_bcf = {c: 100 * (v["published_t"] / (v["estimate_t"] / v["bcf"]) - 1) for c, v in call.items()}
    ok(sorted(c for c, v in no_bcf.items() if abs(v) > 15) == GOLDEN_SET, "SF12: without smearing, same call")
    ok(all(1.0 <= v["bcf"] < 1.01 for v in call.values()), "SF12: the rising-water relation's smearing is within one per cent")

    # SF9: the wall clock read as UTC does not reproduce the report, so the offset every value carries rules it out
    wc = smp.copy()
    wc["utc"] = pd.to_datetime(wc["sampled"].str[:16]).dt.tz_localize("UTC")
    tab_wc = RT.all_routes(target, rec, wc)
    ok(max(abs(v["refit"]) for v in tab_wc.values()) > 0.5, "SF9: the wall clock as UTC misses the published loads")
    # SF13: log base is algebra; SF14: one discharge column, three significant figures
    ok(set(rec.columns) == {"station", "time_utc", "discharge_m3s", "turbidity_fnu", "water_temp_c", "flag"},
       "SF14: one discharge series in the record")
    ok(all(len(("%.3g" % x).replace(".", "").lstrip("0")) <= 3 for x in rec["discharge_m3s"].sample(2000, random_state=1)),
       "SF14: discharge at three significant figures")
    lc = np.log(10.0)
    ok(abs(np.log10(123.4) * lc - np.log(123.4)) < 1e-12, "SF13: log base is a constant factor")

    # ---------------------------------------------------------------- the separation line
    for key in P.KEYS:
        h = H[key]
        bad = np.zeros(sim.N, bool)
        for a, b_ in h["outages"] + [h["swap_gap"]] + [(v["a"], v["b"]) for v in h["visits"]] + h["fouled"]:
            bad[a:b_] = True
        for k in h["late_checks"]:
            bad[k] = True
        ceil = np.zeros(sim.N, bool)
        ceil[:h["swap_k"]] = W[key]["T"][:h["swap_k"]] >= P.OLD_LIMIT
        idx = Sm.loc[Sm["key"] == key, "k"].to_numpy()
        ok(sorted(idx) == list(R.sample_steps(key, W[key])), "separation: %s's guard used the bottles that ship" % key)
        near = sum(bad[max(0, i - 12):i + 13].any() for i in idx)
        ok(near == 0, "separation: no flag, gap or check within three hours of a %s calibration sample" % key)
        near = sum(ceil[max(0, i - 4):i + 5].any() for i in idx)
        ok(near == 0, "separation: no reading at the TS-10 limit within an hour of a %s calibration sample" % key)
        ok(not bad[sim.Y27].any() and not ceil[sim.Y27].any(), "separation: no ask device in %s's 2027 record" % key)
    r27 = rec[rec["time_utc"] >= "2027-01-01"]
    ok(r27.groupby("station").size().eq(35040).all() and (r27["flag"] == "").all(), "separation: 2027 complete and unflagged")

    # ---------------------------------------------------------------- Ask A
    A = S.ask_a(target, rec)
    for c, v in A.items():
        frac = v["hours"] - np.floor(v["hours"])
        ok(abs(frac - 0.5) > 0.2, "Ask A %s SF17: hours not on a half (%.2f)" % (c, v["hours"]))
        ok(fig["asks"]["hours_without_usable_reading"][c] == int(round(v["hours"])), "Ask A %s in figures.json" % c)
    log = pd.read_csv(os.path.join(target, F["log"]), keep_default_na=False)
    # the old letters mark the same events as the new ones: O exactly the logged out-of-water times before 14 April 2026
    for code in sorted(rec["station"].unique()):
        r = S.station_series(rec, code)
        lg = log[(log["station"] == code) & (log["visit"] == "cleaning")]
        marked = np.zeros(len(r), bool)
        for d_, a, b_ in zip(lg["date"], lg["sonde_out"], lg["sonde_in"]):
            t0 = pd.Timestamp("%s %s" % (pd.to_datetime(d_, format="%d.%m.%Y").date(), a)).tz_localize("Europe/Oslo").tz_convert("UTC")
            t1 = pd.Timestamp("%s %s" % (pd.to_datetime(d_, format="%d.%m.%Y").date(), b_)).tz_localize("Europe/Oslo").tz_convert("UTC")
            i0 = int(np.ceil((t0 - r.index[0]) / pd.Timedelta("15min")))
            i1 = int(np.ceil((t1 - r.index[0]) / pd.Timedelta("15min")))
            marked[i0:i1] = True
        ok(np.array_equal(marked, r["flag"].isin(["O", "M"]).to_numpy()), "Ask A %s: the O and M rows are the logged sonde-out times" % code)
        n_old = r["flag"].isin(["G", "O"]).sum()
        ok(n_old >= 8, "Ask A %s: old letters carry at least two hours (%d)" % (code, n_old))
        ok(not r.loc[r.index >= pd.Timestamp("2026-04-14 06:00", tz="UTC"), "flag"].isin(["G", "O", "K"]).any()
           and not r.loc[r.index < pd.Timestamp("2026-04-14 06:00", tz="UTC"), "flag"].isin(["F", "M", "C"]).any(),
           "Ask A %s: one letter set before the migration, the other after" % code)
    # SF16: nothing unusable within two hours of either edge of 2025 and 2026, so the Norwegian calendar counts the same
    for code in sorted(rec["station"].unique()):
        r = S.station_series(rec, code)
        edge = r[(r.index < pd.Timestamp("2025-01-01 02:00", tz="UTC")) |
                 ((r.index >= pd.Timestamp("2026-12-31 22:00", tz="UTC")) & (r.index < pd.Timestamp("2027-01-01 02:00", tz="UTC")))]
        ok(edge["turbidity_fnu"].notna().all() and (edge["flag"].fillna("") == "").all(), "SF16: %s clean at the year edges" % code)
    # SF18: duplicate rows are exact repeats of one interval
    rr = pd.read_parquet(os.path.join(target, F["record"]))
    ok(rr.duplicated(["station", "time_utc"]).sum() == rr.duplicated().sum(), "SF18: every repeated interval is an exact repeat")
    # SF19: a TS-10 reading at its limit is exactly 1,000.0; nothing reads above it before the sonde changed
    for code in sorted(rec["station"].unique()):
        lgs = log[(log["station"] == code) & (log["visit"] == "sensor replaced")].iloc[0]
        sw_ = pd.to_datetime("%s %s" % (lgs["date"], lgs["sonde_out"]), format="%d.%m.%Y %H:%M").tz_localize("Europe/Oslo").tz_convert("UTC")
        r = S.station_series(rec, code)
        ok((r.loc[r.index < sw_, "turbidity_fnu"].dropna() <= 1000.0).all(), "SF19: %s's TS-10 never reads above 1,000 FNU" % code)
    # SF21: K sits on the reading before a logged handheld check, C on a logged handheld check
    for code in sorted(rec["station"].unique()):
        r = S.station_series(rec, code)
        nk = int(r["flag"].isin(["K"]).sum())
        lgk = log[(log["station"] == code) & log["remarks"].str.startswith("handheld turbidimeter before removal")]
        lgk = lgk[pd.to_datetime(lgk["date"], format="%d.%m.%Y") < pd.Timestamp("2026-04-14")]
        ok(nk == len(lgk), "SF21: %s's K rows are its logged handheld checks (%d)" % (code, nk))
    lit = {}
    anyflag = {}
    for code in sorted(rec["station"].unique()):
        r = S.station_series(rec, code)
        r = r[r.index < pd.Timestamp("2027-01-01", tz="UTC")]
        miss = r["turbidity_fnu"].isna()
        lgs = log[(log["station"] == code) & (log["visit"] == "sensor replaced")].iloc[0]
        swap = pd.to_datetime("%s %s" % (lgs["date"], lgs["sonde_out"]), format="%d.%m.%Y %H:%M").tz_localize("Europe/Oslo").tz_convert("UTC")
        ceil = (r.index < swap) & (r["turbidity_fnu"] >= 1000.0)
        lit[code] = int(round((miss | r["flag"].isin(["F", "M"]) | ceil).sum() / 4))
        anyflag[code] = int(round((miss | (r["flag"] != "") & r["flag"].notna() | ceil).sum() / 4))
    ok(sum(lit[c] != fig["asks"]["hours_without_usable_reading"][c] for c in lit) == 14, "Ask A device SF20: the letters F and M alone miss every station")
    ok(sum(anyflag[c] != fig["asks"]["hours_without_usable_reading"][c] for c in anyflag) == 14, "Ask A device: every flag counted misses every station")
    ok(sum(v["ceiling"] > 0 for v in A.values()) >= 3, "Ask A device: the TS-10 limit moves three stations or more")
    ok(sum(v["missing"] > 0 for v in A.values()) == 14, "Ask A device: every station has intervals with no row")

    # ---------------------------------------------------------------- Ask B
    B, failed, qc = S.ask_b(target)
    for c, v in B.items():
        ok(fig["asks"]["samples_in_failed_batches"][c] == v, "Ask B %s in figures.json" % c)
    for bt, (c1, c2, ref, blank) in qc.items():
        # each check as a signed margin: positive passes, negative fails, in units of its own limit
        rpd = abs(c1 - c2) / ((c1 + c2) / 2)
        margins = [0.5 - abs(blank), c1 / ref - 0.9, 1.1 - c1 / ref, c2 / ref - 0.9, 1.1 - c2 / ref, 0.10 - rpd]
        tol = [0.03, 0.004, 0.004, 0.004, 0.004, 0.004]
        fails = [m < 0 for m in margins]
        if any(fails):
            ok(any(m < -t for m, t in zip(margins, tol)), "Ask B %s fails a check by a clear margin" % bt)
        else:
            ok(all(m > t for m, t in zip(margins, tol)), "Ask B %s passes every check by a clear margin" % bt)
        alt = abs(c1 - c2) / max(c1, c2) > 0.10
        ok((bt in failed) == (any(fails[:5]) or alt) or abs(abs(c1 - c2) / max(c1, c2) - 0.10) > 0.004,
           "Ask B %s SF25: against the larger aliquot, same verdict" % bt)
    bx = pd.read_csv(os.path.join(target, F["batches"]))
    fx = pd.read_csv(os.path.join(target, F["field"]), keep_default_na=False)
    ok(sorted(bx["sample_id"]) == sorted("2027-%04d" % n for n, d in zip(fx["bottle_no"], fx["sampled"]) if d.startswith("2027")),
       "SF22 SF26: the batch export holds each 2027 bottle once")
    bt_ = bx.drop_duplicates("batch")
    ok((bt_["blank_change_mg"] < -0.5).any(), "SF24: a blank below -0.5 mg ships, so the absolute reading is the procedure's")
    ok(set(fx["trip"]) == {"routine round", "flood callout"}, "SF11: every bottle in the sheet is a river sample")
    nominal = S.ask_b(target, lots={"KS-26-11": 50.0, "KS-27-06": 50.0})[0]
    ok(sum(nominal[c] != B[c] for c in B) >= 10, "Ask B device: the export's nominal moves ten stations or more (%d)" % sum(nominal[c] != B[c] for c in B))
    ok(len(failed) >= 8 and len({pd.Timestamp(pd.to_datetime(qc_m, format="%d.%m.%Y")).month for qc_m in
       pd.read_csv(os.path.join(target, F["batches"])).drop_duplicates("batch").set_index("batch").loc[failed, "weighed"]}) >= 6,
       "Ask B: the failures spread over the year")

    # ---------------------------------------------------------------- documents read back, positive controls first
    proc = _pdf_text(os.path.join(target, F["procedure"]))
    ok("re-issued when it misstates the suspended sediment that passed the station" in proc.replace("\n", " "), "procedure: section 8 reads back")
    ok("upper end of the sonde" in proc.replace("\n", " "), "procedure: section 5 reads back")
    for word in ("rising", "limb", "hysteresis", "sand", "falling"):
        ok(word not in proc.lower(), "procedure: no %r" % word)
    rep_t = _pdf_text(os.path.join(target, F["report"]))
    ok("Suspended sediment loads 2027" in rep_t and len(rp) == 14, "report: reads back, 14 rows")
    stmt = _pdf_text(os.path.join(target, F["statement"]))
    ok(S.read_lots(target) == {"KS-26-11": 50.0, "KS-27-06": 54.0}, "SF23: the statement's lots read back")
    for f in files:
        if f.endswith((".csv", ".md", ".eml")):
            txt = open(os.path.join(target, f), encoding="utf-8").read().lower()
            for word in ("rising", "limb", "hysteres", "sand "):
                ok(word not in txt, "%s: no %r" % (f, word))

    # ---------------------------------------------------------------- realism sweep and dates
    ok(len(set(v["n"] for v in pub.values())) >= 10, "realism: sample counts vary across stations")
    ok(all(v["load_t"] % 100 for v in pub.values()), "realism: no round loads")
    b_export = pd.read_csv(os.path.join(target, F["batches"]))
    last_weighed = pd.to_datetime(b_export["weighed"], format="%d.%m.%Y").max()
    ok(last_weighed < pd.Timestamp("2028-01-18"), "dates: the quality statement follows the last batch (%s)" % last_weighed.date())
    lims_an = pd.to_datetime(lims_new["analysed"]).max()
    ok(lims_an < pd.Timestamp("2028-02-15"), "dates: the report follows the last result (%s)" % lims_an.date())
    reg = pd.read_excel(os.path.join(target, F["register"]))
    ok(pd.to_datetime(reg["sensor_installed"]).max() < pd.Timestamp("2026-11-20"), "dates: the register follows the last sonde")
    ok(pd.to_datetime(reg["sensor_installed"]).min() > pd.Timestamp("2026-09-01"), "dates: the procedure (January 2027) follows every sonde")
    persona = open(os.path.join(target, F["request"]), encoding="utf-8").read()
    ok(P.DATA_MANAGER[0] in persona and P.FIELD_LEAD[0] in persona, "personas from guard.py names")
    return N_OK[0]
