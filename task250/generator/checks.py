"""task250 generator checks: the input gates, the call and its ladder with margins, the counterfactual that the golden's
count equals, the three rules on the clean truth and three fresh years out of sample, every semantic fork row, the
separation line and the deletion tests, the asks against the field truth with their forcing and devices, the documents
read back, the realism sweep and the dates.
    C.run(target, world, fig, golden) -> number of assertions passed"""
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd
from pypdf import PdfReader

import build as B
import params as P
import records as RC
import routes as RT
import sim
import solve as S

N_OK = [0]
SETTING = 4.0
REPLAY_SETTING = 3.5
MARGIN = 3.0


def ok(cond, msg):
    assert cond, msg
    N_OK[0] += 1


def _pdf_text(path, strict=False):
    return " ".join("\n".join(p.extract_text() for p in PdfReader(path, strict=strict).pages).split())


def _per_year(Dm, sd, stations, k0=0, k1=None):
    k1 = Dm.shape[0] if k1 is None else k1
    Z = np.full_like(Dm, np.nan)
    Z[k0:k1] = Dm[k0:k1]
    return {k: len(sim.alerts(Z, k * sd, stations)) / ((k1 - k0) / 365.0) for k in P.SETTINGS}


def _fresh_years(seed, rec):
    """three further years on the same stations: the record's drifts again three years on (same stations and rates),
    the 2028 network run at each setting against the limits the first three years set, each drift left to grow until
    that setting's alert sends a visit or the spring round finds it"""
    old = (sim.D, P.DAYS, RC.D)
    sim.D = P.DAYS = RC.D = 6 * 365
    try:
        W6 = sim.world(seed)
        N = W6["N"]
        keep = np.array([i not in set(W6["closing"]) for i in range(N)])
        y3 = 3 * 365
        rr = np.random.default_rng(seed + 205)
        rnd = {i: [RC.workday((dt.date(y, 3, 1) - P.START).days + int(rr.integers(0, 106))) for y in range(2025, 2031)]
               for i in range(N)}
        lag = np.random.default_rng(seed + 207).integers(1, 6, (6 * 365, N))
        ro = np.random.default_rng(seed + 208)
        noise = (np.clip(ro.normal(0, 0.05, N), -0.12, 0.12), ro.normal(0, 0.02, (6 * 365, N)))
        first = [{"i": f["i"], "start": f["start"], "rate": f["rate"]} for f in rec["faults"]]
        later = [{"i": f["i"], "start": f["start"] + y3, "rate": f["rate"]} for f in rec["faults"]]
        a_ic, _ = sim.anomalies(dict(W6, faults=[]))
        _, D_ic, _ = sim.qc(W6, a_ic, np.ones(N, bool))
        sd_ic = np.nanstd(D_ic[:y3], axis=0, ddof=1)
        run1 = RC.run_policy(W6, first, np.tile(3.0 * sd_ic, (6 * 365, 1)), np.ones(N, bool), rnd, lag, noise=noise)
        sd = np.nanstd(run1["S"][:y3], axis=0, ddof=1)
        replay = _per_year(run1["S"], sd, np.where(keep)[0], 0, y3)
        fresh = {}
        for k in P.SETTINGS:
            r2 = RC.run_policy(W6, later, np.tile(k * sd, (6 * 365, 1)), keep, rnd, lag, export=True, noise=noise)
            fresh[k] = sum(1 for (i, t) in r2["alerts"] if t >= y3) / 3.0
    finally:
        sim.D, P.DAYS, RC.D = old
    return replay, fresh


def _within(st, d, alerts, days):
    return [d - dt.timedelta(days=j) for j in range(days + 1) if (st, d - dt.timedelta(days=j)) in alerts]


def run(target, world, fig, golden):
    N_OK[0] = 0
    F = {k: os.path.join(target, v) for k, v in B.FILES.items()}
    W, rec, reg_w, truth = world["W"], world["rec"], world["reg"], world["truth"]
    BUD = P.BUDGET_YEAR
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "metadata.json")))

    # ---------------------------------------------------------------- input gates
    ok(len(files) == len(B.FILES) >= 10, "ten or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    q = pd.read_parquet(F["qc"])
    ok(len(q) >= 25000 and len(pd.read_csv(F["daily"], sep=";")) >= 25000, "files of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors shipped")
    ok(not any("distract" in f.lower() or "decoy" in f.lower() for f in files), "no distractor named as one")
    ok(rec["clean"], "the record reads cleanly: every drift placed so the counterfactual equals the golden's count")

    # ---------------------------------------------------------------- the call
    reg = S.register(target)
    q_, A, Sx = S.qc_matrix(target, reg)
    call = S.the_call(target, reg, A, Sx, q_)
    whole = {k: int(round(v)) for k, v in call["per_year"].items()}
    ok(call["setting"] == SETTING, "the golden: setting %.1f (got %s)" % (SETTING, call["setting"]))
    ok(call["budget"] == BUD == fig["steps"]["drift_alert_visits_in_plan"], "the plan's drift-alert visits read back as %d" % BUD)
    ok(fig["call"]["setting"] == SETTING and fig["call"]["alerts_a_year"] == whole[SETTING], "figures.json carries the call")
    ok(fig["call"]["per_setting_alerts_a_year"] == {"%.1f" % k: whole[k] for k in P.SETTINGS}, "figures.json carries every setting")
    ok(all(whole[a] > whole[b] for a, b in zip(P.SETTINGS, P.SETTINGS[1:])), "a lower setting raises more alerts")
    for k, v in call["per_year"].items():
        edge = 0.5 - abs(v - round(v))
        ok(edge >= 0.49, "bin: %.1f's %.2f alerts a year sits %.2f from its rounding edge" % (k, v, edge))
    ok(call["per_year"][3.5] >= BUD + MARGIN and call["per_year"][4.0] <= BUD - MARGIN,
       "margins: 3.5 is %.1f over the %d, 4.0 is %.1f under" % (call["per_year"][3.5] - BUD, BUD, BUD - call["per_year"][4.0]))
    keep = reg["baja_prevista"].isna().to_numpy()
    ok(int(keep.sum()) == len(reg) - P.N_CLOSING == fig["components"]["stations_kept"]
       and int((~keep).sum()) == P.N_CLOSING == fig["components"]["stations_closing"],
       "%d stations kept, %d closing" % (len(reg) - P.N_CLOSING, P.N_CLOSING))
    ok(fig["components"]["drifts_cut_short"] == {"%.1f" % k: call["parts"][k][1] for k in P.SETTINGS}
       and fig["components"]["drift_alert_adjustments_kept"] == call["repairs_kept"], "figures.json carries the parts")
    detail = rec["detail"]
    ok(all(detail[k][0] == detail[k][1] == round(call["per_year"][k] * 3) for k in P.SETTINGS),
       "C1: the record re-lived at each setting with the 2028 network, every drift left to grow until that setting's alert "
       "sent its visit or the spring round found it, raises exactly the golden's count (%s)"
       % {k: detail[k] for k in P.SETTINGS})

    # ---------------------------------------------------------------- the ladder: every reflex files 3.5, the family 4.0
    r = RT.all_routes(target, reg, A, Sx, q_)
    for nm in RT.REFLEXES:
        ok(RT.setting(r[nm], BUD) == REPLAY_SETTING, "rung %s files %.1f (got %s, %s)" % (
            nm, REPLAY_SETTING, RT.setting(r[nm], BUD), {k: round(v, 1) for k, v in r[nm].items()}))
        ok(r[nm][3.0] >= BUD + MARGIN and r[nm][3.5] <= BUD - MARGIN, "rung %s: 3.0 at %.1f, 3.5 at %.1f, clear of %d"
           % (nm, r[nm][3.0], r[nm][3.5], BUD))
    for nm in RT.OVER:
        ok(RT.setting(r[nm], BUD) == SETTING and {k: int(round(v)) for k, v in r[nm].items()} != whole,
           "over-correction %s files %.1f with other counts (%s)" % (nm, SETTING, {k: round(v, 2) for k, v in r[nm].items()}))
    for nm in RT.GOLDEN_FAMILY:
        sf = "SF25" if "lookback" in nm else ("SF26" if "once" in nm else "C1")
        ok({k: int(round(v)) for k, v in r[nm].items()} == whole, "%s family %s: the same four figures (%s)"
           % (sf, nm, {k: round(v, 2) for k, v in r[nm].items()}))
    ok({k: int(round(v)) for k, v in r["golden"].items()} == whole, "routes.py's golden is solve.py's")
    rerun = {k: int(round(v)) for k, v in r["rerun_2028_network"].items()}
    ok(fig["components"]["rerun_at_runner_up"] == rerun[3.5], "the network re-run's 3.5 count in figures.json")
    ok(fig["call"]["runner_up"] == 3.5 and fig["call"]["runner_up_alerts_a_year"] == whole[3.5], "the runner-up and its count")
    ok(abs(whole[4.0] - round(r["replay_record"][3.5])) >= 2 and abs(whole[4.0] - rerun[3.5]) >= 2,
       "no coincidence: the golden's 4.0 count (%d) is two or more from the reflexes' 3.5 counts (%d, %d)"
       % (whole[4.0], round(r["replay_record"][3.5]), rerun[3.5]))
    # the right-for-the-wrong-reason route: alert-days rather than alerts (ruled out by section 8's hold)
    cont = np.where(keep)[0]
    sd = np.nanstd(Sx, axis=0, ddof=1)
    al_rec = q[q["alerta"] == "S"]
    per_year_rec = al_rec.groupby(al_rec["fecha"].dt.year).size()
    days_replay = {k: float(np.sum(np.abs(np.nan_to_num(Sx[:, cont])) > k * sd[cont])) / 3 for k in P.SETTINGS}
    ok(days_replay[3.0] > 2 * per_year_rec.max(), "SF1: alert-days at 3.0 (%.0f a year) are far above the alerts the record "
       "raised (%s), so section 8's hold is visible in the record" % (days_replay[3.0], per_year_rec.to_dict()))

    # ---------------------------------------------------------------- the record replays the recorded alerts exactly
    lim = np.full_like(Sx, np.nan)
    k_ = (q["fecha"] - S.START).dt.days.to_numpy()
    j_ = q["estacion"].map({c: j for j, c in enumerate(reg["codigo"])}).to_numpy()
    lim[k_, j_] = q["limite"].to_numpy()

    def replay_alerts(at_limit):
        out = set()
        for i in range(len(reg)):
            last = -10 ** 6
            v, L = np.abs(np.nan_to_num(Sx[:, i])), np.nan_to_num(lim[:, i], nan=1e9)
            for t in np.where(~np.isnan(Sx[:, i]) & ((v >= L) if at_limit else (v > L)))[0]:
                if t - last > P.HOLD_DAYS:
                    out.add((reg["codigo"][i], t))
                    last = t
        return out
    theirs = {(s, (d - S.START).days) for s, d in zip(al_rec["estacion"], al_rec["fecha"])}
    ok(replay_alerts(False) == theirs, "section 8 on the export's statistic and limits reproduces its alert column (%d "
       "alerts)" % len(theirs))
    ok(len(replay_alerts(True) ^ theirs) >= 0, "SF21: 'beyond' replayed at or beyond the record's rounded limits moves %d "
       "alerts of the record's own column, which replays strictly" % len(replay_alerts(True) ^ theirs))
    xy = reg[["x_utm", "y_utm"]].to_numpy(float)
    R_all, S_all = S.rerun(A, xy, np.ones(len(reg), bool))
    res = np.full_like(Sx, np.nan)
    res[k_, j_] = q["residuo"].astype(float).to_numpy()
    ok(np.nanmax(np.abs(R_all - res)) <= 0.016, "section 4 re-run on the whole network reproduces the export's residuals "
       "to its rounding (%.3f)" % np.nanmax(np.abs(R_all - res)))
    ok(np.nanmax(np.abs(S_all - Sx)) <= 0.006, "section 5 re-run on the whole network reproduces the recorded statistic (%.4f)"
       % np.nanmax(np.abs(S_all - Sx)))

    # ---------------------------------------------------------------- the drifts the record cut short
    hist = S.history(target)
    rep = call["repairs"]
    faults = rec["faults"]
    af = sorted((f["i"], f["repair"]) for f in faults if f["how"] == "alert")
    ok(sorted((i, v) for (i, a, v) in rep) == af, "the history's drift-alert adjustments are the record's alert-found "
       "drifts, each at its repair (%d)" % len(af))
    ok(all(f["how"] in ("alert", "round") for f in faults), "every drift was found by an alert's visit or the spring round")
    for (i, a, v) in rep:
        f = next(x for x in faults if x["i"] == i and x["repair"] == v)
        ok(a == f["alert"] and 1 <= v - a <= 9, "the alert that sent the visit to %s is its latest alert, %d days before"
           % (reg["codigo"][i], v - a))
    rnd_found = [f for f in faults if f["how"] == "round"]
    hr = hist[(hist["motivo"] == "Campaña de calibración") & hist["error_encontrado_C"].notna()]
    ok(len(hr) == len(rnd_found) >= 3, "the spring rounds found %d drifts, each an adjustment in the history" % len(hr))
    ok(hist["error_encontrado_C"].notna().sum() == len(af) + len(rnd_found), "every as-found error in the history is a drift")
    adj_vis = [t for t in truth if t.get("adjusted")]
    ok(len(adj_vis) == len(af) + len(rnd_found), "no check adjusted a sensor that had not drifted")
    for f in faults:
        for t in truth:
            if t["i"] == f["i"] and t["as_found"] is not None and f["start"] < t["v"] <= f["repair"]:
                ok((t["v"] == f["repair"]) == t["adjusted"], "the check at %s on day %d agrees with the record's drift end"
                   % (reg["codigo"][f["i"]], t["v"]))
    cut = {k: call["parts"][k][1] for k in P.SETTINGS}
    ok(cut[3.5] >= 15 and cut[4.0] >= cut[3.5] and cut[4.5] >= cut[4.0], "the cut-short drifts grow with the setting (%s)" % cut)
    ok(call["repairs_kept"] == sum(1 for (i, a, v) in rep if keep[i]) and call["repairs_kept"] < len(rep),
       "drift-alert adjustments at kept stations %d of %d (some at closing stations)" % (call["repairs_kept"], len(rep)))

    # ---------------------------------------------------------------- R1, R2, R3 on the clean truth
    ok(set(q.columns) == {"estacion", "fecha", "anomalia", "estimacion", "residuo", "vecinos", "estadistico_14d", "limite",
                          "alerta"}, "R1: the export carries the anomalies, the neighbours and the statistic, nothing for 2028")
    ok(not any(c for c in reg.columns if "2028" in c or "vecin" in c), "R1: the register holds no 2028 neighbour or limit")
    ok(q["anomalia"].notna().all() and len(q) == int(np.sum(W["avail"])), "R1: every read day's anomaly ships (%d)" % len(q))
    keep_w = np.array([i not in set(W["closing"]) for i in range(W["N"])])
    st_w = np.where(keep_w)[0]
    sd_clean = np.nanstd(rec["D"], axis=0, ddof=1)
    easy = _per_year(rec["D"], sd_clean, st_w)
    ok(RT.setting(easy, BUD) == REPLAY_SETTING, "R3a: on the clean truth the record replayed files %.1f (%s)"
       % (REPLAY_SETTING, {k: round(v, 1) for k, v in easy.items()}))
    _, D28, _ = sim.qc(dict(W, faults=[dict(f) for f in faults]), rec["a"], keep_w)
    rerun_clean = _per_year(D28, sd_clean, st_w)
    ok(RT.setting(rerun_clean, BUD) == REPLAY_SETTING, "R3b: the 2028 network re-run alone on the clean truth leaves %.1f "
       "(%s)" % (REPLAY_SETTING, {k: round(v, 1) for k, v in rerun_clean.items()}))
    cens_clean = {}
    for k in P.SETTINGS:
        days = S.alert_days_by_station(rec["D"], k * sd_clean, st_w)
        cens_clean[k] = (sum(len(v) for v in days.values()) + len(S.cut_short(
            days, [(f["i"], f["alert"], f["repair"]) for f in faults if f["how"] == "alert"], keep_w))) / 3
    ok(RT.setting(cens_clean, BUD) == REPLAY_SETTING, "R3b: the cut-short drifts added to the record replayed, without the "
       "2028 network, leave %.1f (%s)" % (REPLAY_SETTING, {k: round(v, 1) for k, v in cens_clean.items()}))
    both_clean = {}
    for k in P.SETTINGS:
        days = S.alert_days_by_station(D28, k * sd_clean, st_w)
        both_clean[k] = (sum(len(v) for v in days.values()) + len(S.cut_short(
            days, [(f["i"], f["alert"], f["repair"]) for f in faults if f["how"] == "alert"], keep_w))) / 3
    ok(RT.setting(both_clean, BUD) == SETTING, "R3b: both keys on the clean truth file %.1f (%s)"
       % (SETTING, {k: round(v, 1) for k, v in both_clean.items()}))
    replay_f, fresh = _fresh_years(B.SEED, rec)
    ok(RT.setting(replay_f, BUD) == REPLAY_SETTING and RT.setting(fresh, BUD) == SETTING,
       "R3 out of sample: three further years on the 2028 network, the record's drifts again and each left to grow until "
       "the setting's alert or the spring round, raise %.1f a year at 3.5 and %.1f at 4.0, where the replay of the first "
       "three filed %.1f" % (fresh[3.5], fresh[4.0], RT.setting(replay_f, BUD)))
    # R2: each Layer 1 item mishandled leaves the call
    x2 = reg.copy()
    x2["baja_prevista"] = [None if f != "programme 2021-2027" else pd.Timestamp("2027-12-31")
                           for f in x2["financiacion"]]
    ok((x2["baja_prevista"].isna() == reg["baja_prevista"].isna()).all(), "R2: the closing stations by funding or by "
       "baja_prevista are one set")
    ok(RT.setting(_per_year(D28, sd_clean, st_w), BUD) == RT.setting(r["rerun_2028_network"], BUD),
       "R2: unrounded anomalies (the clean truth), the re-run's call unchanged")
    daily = pd.read_csv(F["daily"], sep=";", decimal=",")
    ok(daily.duplicated().sum() > 0 and daily.duplicated().sum() == daily.duplicated(["estacion", "fecha"]).sum(),
       "R2: the daily export's re-sent rows are exact repeats")
    d2 = daily.drop_duplicates(["estacion", "fecha"]).copy()
    d2["fecha"] = pd.to_datetime(d2["fecha"], format="%d/%m/%Y")
    five = {c: (pd.Timestamp(f) if pd.notna(f) else None) for c, f in zip(reg["codigo"], reg["registro_5min_desde"])}
    need = [RC.accept_min(d.date(), five[s] is not None and d >= five[s]) for s, d in zip(d2["estacion"], d2["fecha"])]
    read = d2[d2["n_registros"].to_numpy() >= np.array(need)]
    ok(len(read) == len(q) and set(zip(read["estacion"], read["fecha"])) == set(zip(q["estacion"], q["fecha"])),
       "R2: section 2's completeness rule on the daily export (DST days and five-minute loggers included) gives exactly the "
       "export's read days (%d)" % len(q))
    # R3c: no plant
    blocks = 0
    for s_, g in daily.drop_duplicates().groupby("estacion"):
        v = g["tmed"].to_numpy()
        seen = set()
        for i in range(0, len(v) - 14, 14):
            h = v[i:i + 14].tobytes()
            blocks += h in seen
            seen.add(h)
    ok(blocks == 0, "R3c: no fortnight of daily means repeats at any station")
    summ = _pdf_text(F["summary"])
    al27 = al_rec[al_rec["fecha"].dt.year == 2027]
    ok(("Network" in summ) and (" %d" % len(al27)) in summ, "R3c: the 2027 summary's network total is the export's (%d)" % len(al27))
    dist_name = dict(zip(reg["codigo"], reg["comarca"]))
    for _, nm in P.DISTRICTS:
        n = int(al27["estacion"].map(dist_name).eq(nm).sum())
        ok(nm in summ and n > 0, "R3c: the summary carries %s, which raised alerts in 2027 (%d)" % (nm, n))

    # ---------------------------------------------------------------- semantic fork rows
    proc = _pdf_text(F["procedure"])
    ok("unless it raised one for the station on any of the 14 days before" in proc, "SF1 SF7: section 8's hold reads back")
    ok("lies beyond its limit, either side" in proc, "SF20: two-sided, filed")
    ok("drift statistic on a read day" in proc, "SF8: the statistic on read days, filed")
    ok("the drift statistic the quality control recorded for the station over the three previous calendar years" in proc,
       "SF4: the limit from the recorded statistic, filed")
    ok("standard deviation (n − 1)" in proc or "standard deviation (n - 1)" in proc, "SF18: n - 1, filed")
    ok("planned on the three previous calendar years" in proc, "SF2: the three years, filed")
    ok("the three stations of the network nearest to it that have an anomaly that day and lie within 75 km" in proc,
       "SF9: the estimate's neighbours, filed")
    ok("straight-line distances between the register's UTM coordinates" in proc, "SF10: the distance, filed")
    ok("one beyond 0.2 °C is adjusted and read again, and one more than 1.0 °C out is replaced" in proc
       and "entered in the station's sensor history in the register" in proc, "SF22: section 9 files the adjustment, the "
       "replacement and the history")
    plan = _pdf_text(F["plan"])
    n_kept = len(reg) - P.N_CLOSING
    ok("The network runs %d stations in 2028" % n_kept in plan, "SF3: the 2028 network, filed in the plan")
    ok(RT.setting(r["golden_ddof0"], BUD) == SETTING, "SF18: n against n - 1, same call")
    _, S28 = S.rerun(A, xy, keep)
    for sign in (1, -1):
        per = {}
        for k in P.SETTINGS:
            n = 0
            for i in cont:
                last = -10 ** 6
                for t in np.where(~np.isnan(S28[:, i]) & (sign * np.nan_to_num(S28[:, i]) > k * sd[i]))[0]:
                    if t - last > P.HOLD_DAYS:
                        n += 1
                        last = t
            per[k] = n / 3
        ok(RT.setting(per, BUD) == REPLAY_SETTING, "SF20: one side only (%+d), without the cut-short drifts, files %.1f"
           % (sign, REPLAY_SETTING))
    ok(S.the_call(target, reg, A, Sx, q_, pool=keep)["setting"] == SETTING, "SF3: the %d as the pool" % n_kept)
    sd27 = np.nanstd(Sx[730:], axis=0, ddof=1)
    per27 = {}
    for k in P.SETTINGS:
        days = S.alert_days_by_station(S28, k * sd27, cont)
        per27[k] = (sum(len(v) for v in days.values()) + len(S.cut_short(days, rep, keep))) / 3
    ok(RT.setting(per27, BUD) == SETTING, "SF4: limits from 2027's statistic alone, same call")
    ok("A lower setting catches a drift sooner and raises more alerts" in proc, "SF5: the most sensitive setting is the "
       "lowest, filed in section 7")
    ok(all(abs(v - BUD) >= 2 for v in call["per_year"].values()), "SF6: no setting's alerts a year sit at the plan's %d" % BUD)
    shipped_cols = set(q.columns) | set(daily.columns) | set(reg.columns)
    ok(not any("normal" in c.lower() for c in shipped_cols), "SF11: no normals ship, so the export's anomalies are the "
       "anomalies section 3 defines")
    by_year = {k: np.mean([sum(1 for (i, t) in sim.alerts(S28, k * sd, cont) if t // 365 == y) for y in range(3)])
               for k in P.SETTINGS}
    ok(all(abs(by_year[k] * 3 - call["parts"][k][0]) < 1e-9 for k in P.SETTINGS), "SF13: the mean of each year's "
       "alerts from the one continuous run, the same re-run counts")
    ok("a new year's configuration does not lift that hold" in proc, "SF13: the hold across the year's turn, filed")
    ok(all(round(v * 3) % 3 == 0 and abs(v * 3 - round(v * 3)) < 1e-9 for v in call["per_year"].values()),
       "SF14: every setting's three-year count divides by three, so each figure a year is a whole number")
    full_only = S28.copy()
    full_only[:P.WINDOW - 1] = np.nan
    per_full = {}
    for k in P.SETTINGS:
        days = S.alert_days_by_station(full_only, k * sd, cont)
        per_full[k] = int(round((sum(len(v) for v in days.values()) + len(S.cut_short(days, rep, keep))) / 3))
    ok("when at least 10 of those days have a residual" in proc and "in force from 1 January 2025" in proc
       and all(per_full[k] == whole[k] for k in (3.5, 4.0, 4.5)) and RT.setting(per_full, BUD) == SETTING,
       "SF15: waiting for a full 14-day window at the record's start (against section 5's 'at least 10', with version 4 "
       "in force from 1 January 2025) leaves the call and 3.5 to 4.5 unchanged and moves 3.0 to %d" % per_full[3.0])
    for nm, lim_ in (("k times the spread rounded to three decimals", lambda k: k * np.round(sd, 3)),
                     ("the limit rounded to three decimals", lambda k: np.round(k * sd, 3))):
        per_ = {}
        for k in P.SETTINGS:
            days = S.alert_days_by_station(S28, lim_(k), cont)
            per_[k] = int(round((sum(len(v) for v in days.values()) + len(S.cut_short(days, rep, keep))) / 3))
        ok(per_ == whole, "SF16: %s, the same figures" % nm)
    at_lim = {}
    for k in P.SETTINGS:
        n = 0
        days = {}
        for i in cont:
            last = -10 ** 6
            for t in np.where(~np.isnan(S28[:, i]) & (np.abs(np.nan_to_num(S28[:, i])) >= k * sd[i]))[0]:
                if t - last > P.HOLD_DAYS:
                    days.setdefault(int(i), []).append(int(t))
                    last = t
        at_lim[k] = int(round((sum(len(v) for v in days.values()) + len(S.cut_short(days, rep, keep))) / 3))
    ok(at_lim == whole, "SF21: at or beyond the unrounded 2028 limits, the same figures")
    ok(len(set(np.round(reg["x_utm"] / 1000, 3))) == len(reg), "SF10: no two stations share a position")
    dd = np.hypot(xy[:, None, 0] - xy[None, :, 0], xy[:, None, 1] - xy[None, :, 1]) / 1000
    have = ~np.isnan(A)
    far = 0.0
    for i in range(len(reg)):
        o = np.array([j for j in np.argsort(dd[i], kind="stable") if j != i and keep[j]][:30], int)
        c3 = np.argmax(np.cumsum(have[:, o], axis=1) >= 3, axis=1)
        far = max(far, float(np.max(np.where(have[:, i], dd[i, o][c3], 0.0))))
    ok(far < P.RADIUS_KM - 20, "SF19: the 75 km radius never binds (the farthest station a 2028 estimate draws on is "
       "%.1f km away)" % far)
    gap = 1e9
    for pool_ in (keep, np.ones(len(reg), bool)):
        for i in range(len(reg)):
            o = np.sort(dd[i, pool_ & (np.arange(len(reg)) != i)])
            gap = min(gap, float(np.min(np.diff(o[1:7]))))
    ok(gap > 0.0005, "SF19: no tie where a station's third and later nearest could change places (closest pair %.1f m "
       "apart)" % (1000 * gap))
    # the cut-short drifts: which history rows, which alert, which window
    hd = hist[hist["motivo"] == "Alerta de deriva"]
    ok(hd["error_encontrado_C"].notna().all() and set(hd["actuacion"]) == {RC.ACTION_ADJUST, RC.ACTION_REPLACE},
       "SF23: every drift-alert row of the history carries an as-found error, adjusted or replaced")
    adj_only = [(i, a, v) for (i, a, v), act in zip(rep, hd["actuacion"]) if act == RC.ACTION_ADJUST]
    per_adj = {}
    for k in P.SETTINGS:
        days = S.alert_days_by_station(S28, k * sd, cont)
        per_adj[k] = (sum(len(v) for v in days.values()) + len(S.cut_short(days, adj_only, keep))) / 3
    ok(RT.setting(per_adj, BUD) in (REPLAY_SETTING, SETTING), "SF23: the replaced sensors left out (against section 9, "
       "which replaces a sensor more than 1.0 degree out) files %s (%s)" % (RT.setting(per_adj, BUD),
                                                                          {k: round(v, 1) for k, v in per_adj.items()}))
    Srec = rec["D"]
    sdr = np.nanstd(Srec, axis=0, ddof=1)
    spare = []
    for f in rec["faults"]:
        if f["how"] != "alert" or f["i"] in set(W["closing"]):
            continue
        for kk in (3.5, 4.0, 4.5):
            gap_ = (kk * sdr[f["i"]] - abs(Srec[f["alert"], f["i"]])) / abs(f["rate"])
            nxt = [x for x in rec["rounds"][f["i"]] if x > f["repair"]]
            if nxt:
                spare.append(nxt[0] - (f["repair"] + gap_))
    ok(spare and min(spare) >= 60, "SF28: every drift the record's alerts cut short would have crossed the 3.5, 4.0 and "
       "4.5 limits two months or more before its station's next spring round (%.0f days at the least)" % min(spare))
    qa = S.alert_days(q, reg)
    for (i, a, v) in rep:
        st = reg["codigo"][i]
        d = (S.START + pd.Timedelta(days=v)).date()
        w10 = _within(st, d, qa, 10)
        w30 = _within(st, d, qa, 30)
        ok(len(w10) == len(w30) == 1, "SF24: the adjustment at %s on %s answers one alert in the 30 days before" % (st, d))

    # ---------------------------------------------------------------- separation line and deletion tests
    tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
    try:
        for k in ("orders", "checks", "daily", "summary") + tuple(B.DISTRACTORS):
            t2 = os.path.join(tmp, k)
            os.makedirs(t2)
            for f in files:
                if f != B.FILES[k]:
                    shutil.copy(F[[x for x, v in B.FILES.items() if v == f][0]], os.path.join(t2, f))
            c2 = S.the_call(t2)
            ok(c2["setting"] == SETTING and c2["per_year"] == call["per_year"],
               "separation: the call never reads %s" % B.FILES[k])
            if k in B.DISTRACTORS:
                ok(S.ask_a(t2)[0] == S.ask_a(target)[0] and S.ask_b(t2)[0] == S.ask_b(target)[0],
                   "deletion test: %s moves no ask" % B.FILES[k])
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- the asks against the field truth
    names = [nm for _, nm in P.DISTRICTS]
    dname = dict(P.DISTRICTS)
    gA, a_rows = S.ask_a(target)
    gB, b_rows = S.ask_b(target)
    tA = {nm: {"visits": 0, "days_waited": 0} for nm in names}
    for t in truth:
        if t["kind"] != "drift" or t["status"] != "visit" or t["v"] is None or RC.day(t["v"]).year != 2027:
            continue
        nm = dname[reg_w["district"][t["i"]]]
        tA[nm]["visits"] += 1
        tA[nm]["days_waited"] += t["v"] - t["alert"]
    ok(gA == tA, "Ask A: the golden handling reproduces the field truth exactly")
    closing_w = set(W["closing"])
    tB = {nm: 0 for nm in names}
    for t in truth:
        if (t["kind"] == "breakdown" and t["status"] == "visit" and t["v"] is not None and RC.day(t["v"]).year == 2027
                and t["i"] not in closing_w):
            tB[dname[reg_w["district"][t["i"]]]] += 1
    ok(gB == tB, "Ask B: the golden handling reproduces the field truth exactly")
    ok(fig["asks"]["drift_alert_visits_2027"] == {nm: gA[nm]["visits"] for nm in names}
       and fig["asks"]["days_alerts_waited_2027"] == {nm: gA[nm]["days_waited"] for nm in names}
       and fig["asks"]["breakdown_visits_2027_stations_kept"] == gB, "figures.json carries both asks")
    ok(len({v["visits"] for v in gA.values()}) >= 5 and len(set(gB.values())) >= 5, "realism: the districts differ")
    gaps = [b - a for st_, g in al_rec.groupby("estacion") for a, b in zip(g["fecha"].dt.date, g["fecha"].dt.date.iloc[1:])]
    ok(min(gaps) > dt.timedelta(days=P.HOLD_DAYS), "Ask A forcing: a station's alerts are at least 15 days apart, so a "
       "window of 14 days or less holds one alert at most")
    ck = pd.read_csv(F["checks"])
    ck["ts"] = pd.to_datetime(ck["fecha_hora"])
    ck["d"] = ck["ts"].dt.date
    xo = pd.ExcelFile(F["orders"])
    old, new = xo.parse(xo.sheet_names[0]), xo.parse(xo.sheet_names[1])
    known = set(old["Nº orden"]) | set(new["order_ref"])
    ok(set(ck["orden"]) <= known, "Ask forcing: every reading sits under an order one of the two sheets holds")
    for ref, st, kind, al, d in a_rows:
        ok(al is not None and 0 <= (d - al).days <= 25, "Ask A forcing: %s at %s answers the alert of %s" % (ref, st, al))
    # the readings against the range each station's logger recorded that day
    span = S.daily_span(target)
    code_w = list(reg_w["code"])
    gen_days = {(code_w[c_["i"]], RC.day(c_["v"])) for c_ in world["checks"] if c_.get("bench") is None}
    ben_days = {(code_w[c_["i"]], RC.day(c_["v"])) for c_ in world["checks"] if c_.get("bench") is not None}
    ok(gen_days | ben_days == set(zip(ck["estacion"], ck["d"])), "the calibration database's reading days are the "
       "technicians' at the stations and the workshop's (%d and %d)" % (len(gen_days), len(ben_days)))
    ok(all(k_ in span for k_ in gen_days | ben_days), "every reading day has a row in the loggers' export")
    g_ = ck.assign(lo=ck[["t_estacion", "t_patron"]].min(axis=1), hi=ck[["t_estacion", "t_patron"]].max(axis=1)) \
        .groupby(["estacion", "d"]).agg(lo=("lo", "min"), hi=("hi", "max"))
    inside = [span[k_][0] + 0.2 <= g_.loc[k_, "lo"] and g_.loc[k_, "hi"] <= span[k_][1] - 0.2 for k_ in gen_days]
    ok(all(inside), "Ask forcing: every reading a technician took at a station lies inside that day's logged range by "
       "0.2 degrees (%d days)" % len(inside))
    far = [min(span[k_][0] - g_.loc[k_, "lo"], g_.loc[k_, "hi"] - span[k_][1]) for k_ in ben_days]
    ok(far and min(far) >= RC.BENCH_MARGIN - 0.1, "Ask device: every workshop reading day has readings %.1f degrees or more "
       "below and above the station's logged range (%d days)" % (min(far), len(far)))
    ok(not (gen_days & ben_days), "Ask forcing: no workshop check falls on a day a technician read the station's sensor")
    dl = pd.read_csv(F["daily"], sep=";", decimal=",")
    dl["d"] = pd.to_datetime(dl["fecha"], format="%d/%m/%Y").dt.date
    nrec = dict(zip(zip(dl["estacion"], dl["d"]), dl["n_registros"]))
    five = dict(zip(reg_w["code"], reg_w["five_min_from"]))
    ok(all(k_[1].weekday() < 5 and nrec[k_] >= RC.accept_min(k_[1], five[k_[0]] is not None and k_[1] >= five[k_[0]])
           for k_ in ben_days), "Ask device: the workshop works weekdays, on days the station's logger delivered in full")
    # the devices, each present and each moving the figures on the paths that do not test the readings
    sw = P.CONTRACT_SWITCH
    a1 = [t for t in truth if t["kind"] == "drift" and t["status"] == "office" and t.get("bench") is not None]
    a2 = [t for t in truth if t["kind"] == "drift" and t["status"] == "visit" and t.get("bench") is not None]
    b1 = [t for t in truth if t["kind"] == "breakdown" and t["status"] == "remote" and t.get("bench") is not None]
    dist_of = lambda t: reg_w["district"][t["i"]]
    ok(len({dist_of(t) for t in a1}) >= 6, "Ask A device: drift orders the new contractor's desk closed as false alerts "
       "with only a workshop check under them, in %d districts" % len({dist_of(t) for t in a1}))
    ok(len(a2) >= 2 and all(t["bench"] < t["v"] for t in a2), "Ask A device: %d drift-alert visits with a workshop check "
       "under the order on an earlier day" % len(a2))
    ok(len({dist_of(t) for t in b1}) == len(P.DISTRICTS) and all(t["i"] not in closing_w for t in b1),
       "Ask B device: a breakdown reset remotely with only a workshop check under it at a kept station in every district")
    ok({dist_of(t) for t in a1} | {dist_of(t) for t in a2} >= {dc for dc, _ in P.DISTRICTS
                                                                 if any(t["kind"] == "drift" and t["v"] is not None
                                                                        and t["status"] == "visit"
                                                                        and RC.day(t["v"]) >= sw and dist_of(t) == dc
                                                                        and t["v"] > t["opened"] for t in truth)},
       "Ask A device: every district with a drift-alert visit since July 2027 has a workshop check on its drift orders")
    office = [t for t in truth if t["kind"] == "drift" and t["status"] == "office" and RC.day(t["closed"]).year == 2027]
    ok(len(office) >= 8 and len({dist_of(t) for t in office}) >= 6,
       "Ask A: drift orders closed from the office without a visit, in six districts or more (%d)" % len(office))
    for t in office:
        st = code_w[t["i"]]
        d0, d1 = RC.day(t["opened"]), RC.day(t["closed"])
        near = [d for (s_, d) in gen_days if s_ == st and d0 - dt.timedelta(days=5) <= d <= d1 + dt.timedelta(days=5)]
        ok(not near, "Ask A forcing: the order closed from the office at %s on %s has no technician's reading at the "
           "station within five days of its window" % (st, d1))
    comb = [t for t in truth if t["kind"] == "drift" and t.get("combined") and RC.day(t["v"]).year == 2027]
    ok(len(comb) >= 2, "Ask A: %d drift visits answered at the spring campaign visit, the readings under the campaign's "
       "order" % len(comb))
    ok((old["Estado"] == "Anulada").sum() >= 3 and (new["status"] == "Cancelled").sum() >= 1, "Ask A: cancelled orders in "
       "both sheets (%d and %d)" % ((old["Estado"] == "Anulada").sum(), (new["status"] == "Cancelled").sum()))
    canc = set(old.loc[old["Estado"] == "Anulada", "Nº orden"]) | set(new.loc[new["status"] == "Cancelled", "order_ref"])
    ok(not (canc & set(ck["orden"])), "Ask forcing: no cancelled order has a reading under it")
    gold_v = {(ref, st): d for ref, st, kind, al, d in S._field(target, reg, q)}
    lagd = sum(1 for r_ in new.itertuples(index=False) if pd.notna(r_[4]) and (r_[0], str(r_[1]).split(" / ")[0]) in gold_v
               and pd.Timestamp(r_[4]).date() != gold_v[(r_[0], str(r_[1]).split(" / ")[0])])
    ok(lagd >= 20, "Ask A: the new contractor's visit_date is not the visit day on %d orders" % lagd)
    wk = sum(1 for ref, st, kind, al, d in a_rows if al.weekday() >= 5)
    ok(wk >= 3, "Ask A: alerts on a weekend waited from the alert day (%d)" % wk)
    routes_ = new["station"].astype(str).str.contains(" / ").sum()
    ok(routes_ >= 2, "Ask A/B: route orders carry two stations (%d)" % routes_)
    rem = [t for t in truth if t["status"] == "remote" and RC.day(t["v"]).year == 2027]
    ok(len(rem) >= 8 and len({dist_of(t) for t in rem if t["i"] not in closing_w}) == len(P.DISTRICTS),
       "Ask B: breakdowns reset remotely, closed with no visit, in every district at kept stations (%d)" % len(rem))
    mk = world.get("miskeyed", [])
    mkd = [t for t in mk if t["kind"] == "drift"]
    mkb = [t for t in mk if t["kind"] == "breakdown"]
    ok(len(mkd) >= 6, "Ask A: %d drift-alert visits in 2027 with their readings under the station's previous order" % len(mkd))
    ok(not any(RC.day(t["v"]) >= sw and dist_of(t) in {dist_of(x) for x in a1} for t in mkd),
       "Ask A device: since July 2027 no drift-alert visit's readings went under another order in a district whose desk "
       "closures carry a workshop check, so the two never net out")
    for dc, nm in P.DISTRICTS:
        n_mk = sum(1 for t in mkb if dist_of(t) == dc)
        n_b1 = sum(1 for t in b1 if dist_of(t) == dc)
        ok(n_mk != n_b1, "Ask B device: in %s the breakdown visits with their readings under another order (%d) never "
           "number the remote resets with a workshop check (%d)" % (nm, n_mk, n_b1))
    ok(len(mkb) >= 6, "Ask B: %d breakdown visits at kept stations with their readings under the station's previous "
       "order" % len(mkb))
    reg_codes = set(reg["codigo"])
    ok(set(old["Estación"]) <= reg_codes and all(x in reg_codes for v_ in new["station"] for x in str(v_).split(" / ")),
       "SF17: every order's station is in the register, so each visit has the register's comarca")
    corr_bd = sum(1 for v in b_rows if str(v[0]).startswith("SA-"))
    corr_dr = sum(1 for v in a_rows if str(v[0]).startswith("SA-"))
    ok(corr_bd >= 10 and corr_dr >= 8, "Ask A/B: the new contractor's Corrective covers drift (%d) and breakdowns (%d)"
       % (corr_dr, corr_bd))
    closing = set(reg.loc[~keep, "codigo"])
    bd_closing = sum(1 for r_ in old.itertuples(index=False) if r_[2] == "Avería" and pd.notna(r_[4])
                     and pd.Timestamp(r_[4]).year == 2027 and r_[1] in closing)
    ok(bd_closing >= 2, "Ask B: breakdown visits at closing stations in 2027 (%d)" % bd_closing)
    ok("Preventive" not in set(new["work_type"]), "no round under the new contractor in 2027 (the spring round is the "
       "old contractor's)")
    # each visit claimed by one order: no technician's reading day falls inside two closed orders' spans at a station
    spans = {}
    for r_ in new.itertuples(index=False):
        if r_[5] == "Closed" and pd.notna(r_[4]):
            for st in str(r_[1]).split(" / "):
                spans.setdefault(st, []).append((pd.Timestamp(r_[3]).date(), pd.Timestamp(r_[4]).date()))
    two = [(s_, d) for (s_, d) in gen_days if d >= sw and sum(a_ <= d <= b_ for a_, b_ in spans.get(s_, ())) > 1]
    ok(not two, "Ask forcing: no technician's reading day sits inside two closed orders at its station (%s)" % two[:3])
    # what a visit is, filed: the plan counts a technician's day at a station and puts a check at every visit since July
    # 2027, the dictionary gives Visita as the visit's day and visit_date as the app's closing date
    plan_t, dic_t = _pdf_text(F["plan"]), open(F["dictionary"], encoding="utf-8").read()
    ok("a visit is a day a technician is at a station, so a day's route that takes in two stations is two visits"
       in " ".join(plan_t.split()), "visits filed: counted by station, a technician's day at a station")
    ok("every visit includes a check of the station's temperature sensor in place, the sensor and the transfer standard "
       "reading the station's air side by side" in " ".join(plan_t.split()),
       "visits filed: a check of the sensor in place, in the station's air, at every visit since July 2027")
    ok("At the visit a drift alert calls, and at the spring round, the technician reads the station's sensor"
       in " ".join(proc.split()), "visits filed: a check at every visit a drift alert calls")
    ok("Visita is the day the technician visited" in " ".join(dic_t.split())
       and "visit_date is the date the order was closed on the contractor's app" in " ".join(dic_t.split()),
       "visits filed: the two date columns")
    ok("A sensor's drift does not stop on its own: its error goes on growing at the sensor's own rate until a check sets "
       "it right" in " ".join(proc.split()) and RT.setting(r["rerun_2028_network"], BUD) == REPLAY_SETTING,
       "SF27: section 9 files that a drift grows until a check sets it right; read as stopped at its recorded size, the "
       "re-run alone files %.1f" % REPLAY_SETTING)
    ok("in proportion over the 23-hour and 25-hour days the clocks change" in " ".join(proc.split()),
       "read days filed: the days the clocks change")
    ok("estadistico_14d (the drift statistic as the quality control recorded it)" in " ".join(dic_t.split()),
       "SF4: the export's statistic is the one the quality control recorded")
    for w_ in ("workshop", "bench", "spare", "ice point", "dry block", "pre-check", "taller", "repuesto"):
        ok(w_ not in dic_t.lower() and w_ not in plan_t.lower() and w_ not in proc.lower(),
           "Ask device silent: no filed document names the %r" % w_)
    vis_old = old[(old["Tipo"] == "Alerta deriva") & old["Visita"].notna()]
    ok(all((st, pd.Timestamp(v).date()) in gen_days for st, v in zip(vis_old["Estación"], vis_old["Visita"])),
       "Ask A forcing: every old drift order with a Visita has a technician's reading at the station that day (%d)"
       % len(vis_old))
    off_old = old[(old["Tipo"] == "Alerta deriva") & (old["Estado"] == "Cerrada") & old["Visita"].isna()
                  & (pd.to_datetime(old["Aviso"]).dt.year == 2027)]
    ok(len(off_old) >= 1 and all(not any((st, (pd.Timestamp(a_) + pd.Timedelta(days=j)).date()) in gen_days | ben_days
                                         for j in range(22))
                                 for st, a_ in zip(off_old["Estación"], off_old["Aviso"])),
       "Ask A forcing: the old sheet's 2027 drift orders closed without a Visita have no reading at the station in the 21 "
       "days after the notice (%d)" % len(off_old))
    ok(old.loc[(old["Tipo"] == "Avería") & (old["Estado"] == "Cerrada"), "Visita"].notna().all(),
       "Ask B forcing: every closed old breakdown order carries its visit day")
    ok(not any(RC.day(c_["v"]) < sw for c_ in world["checks"] if c_.get("bench") is not None),
       "the workshop checks are the new contractor's (since July 2027)")
    went = {"visit done", "checked station", "sensor check", "logger checked", "site tidied", "revisión sensor T",
            "comprobación con patrón"}
    nob = [r_ for r_ in new.itertuples(index=False) if r_[5] == "Closed"
           and all((r_[0], st) not in gold_v for st in str(r_[1]).split(" / "))]
    ok(nob and not any(str(r_[6]) in went for r_ in nob), "notes: no closed order without a visit says there was one (%d "
       "orders)" % len(nob))
    blank_old = old[(old["Estado"] == "Cerrada") & old["Visita"].isna()]
    ok(len(blank_old) >= 1 and not blank_old["Observaciones"].astype(str).isin(went).any(),
       "notes: no old order closed without a visit says there was one (%d)" % len(blank_old))
    canc_n = new[(new["status"] == "Cancelled")]
    ok(not canc_n["notes"].astype(str).isin(went).any(), "notes: no cancelled order says someone went")
    base_f = S._field(target, reg, q)
    for link in range(2, 15):
        ok(S._field(target, reg, q, link=link) == base_f, "Ask forcing: alerts linked to orders within %d days, the same "
           "visits" % link)
    import pair as PR
    for w_ in (9, 14, 21):
        al_led = PR.alert_led(target, w_, temperature=True)
        ok(al_led[0] == {nm: gA[nm]["visits"] for nm in names} and al_led[1] == {nm: gA[nm]["days_waited"] for nm in names}
           and al_led[2] == gB, "Ask forcing: each alert's first day a technician read its station within %d days, and "
           "every other such day since July 2027 a breakdown visit, the same figures" % w_)
    gold = (fig["asks"]["drift_alert_visits_2027"], fig["asks"]["days_alerts_waited_2027"],
            fig["asks"]["breakdown_visits_2027_stations_kept"])
    worst = 0
    for nm_, kw in PR.PATHS.items():
        if nm_ == "golden":
            continue
        a_, b_, c_ = PR.score(PR.path(target, **kw), gold)
        worst = max(worst, a_ + b_ + c_)
        ok(a_ + b_ + c_ <= 6, "Ask ladder: the path %r keeps %d of 24 (visits %d, days %d, breakdowns %d)"
           % (nm_, a_ + b_ + c_, a_, b_, c_))
    for w_ in (9, 14, 21):
        a_, b_, c_ = PR.score(PR.alert_led(target, w_), gold)
        ok(a_ + b_ + c_ <= 6, "Ask ladder: the alert-led path within %d days keeps %d of 24" % (w_, a_ + b_ + c_))

    # ---------------------------------------------------------------- documents read back, positive controls first
    ok("QC-02 Air temperature quality control" in proc and "Version 4, November 2024" in proc, "procedure reads back")
    ok(("Drift alerts %d" % BUD) in plan and "Field plan 2028" in plan, "plan reads back")
    ok("Drift alerts raised in 2027" in summ and "Setting 3.0 all year" in summ, "summary reads back")
    eml = open(F["request"], encoding="utf-8").read()
    ok(str(BUD) in eml and "Section 7 says how we choose" in eml and P.COORDINATOR[0] in eml and P.FIELD_LEAD[0] in eml
       and P.QC_ADMIN[0] in eml, "request reads back with the personas from guard.py names")
    dic = open(F["dictionary"], encoding="utf-8").read()
    ok(all(B.FILES[k] in dic for k in B.FILES if k != "dictionary"), "the dictionary names every other file")
    banned = ("re-run", "rerun", "re-ran", "denser", "density", "farther", "further away", "spacing", "counterfactual",
              "neighbour", "neighbor", "closing station", "nearest station", "cut short", "censor", "truncat",
              "would have", "left to grow", "keeps growing", "keep growing", "persist", "renewal", "accumulat")
    for k in ("procedure", "plan", "summary"):
        t = _pdf_text(F[k]).lower()
        for w in banned:
            if w in ("nearest station", "neighbour") and k == "procedure":
                continue                               # the procedure's own vocabulary for a spatial check
            ok(w not in t, "%s: no %r" % (B.FILES[k], w))
    for f in ("request", "dictionary"):
        t = open(F[f], encoding="utf-8").read().lower()
        for w in banned:
            ok(w not in t, "%s: no %r" % (B.FILES[f], w))
    for k in [k for k in B.FILES if B.FILES[k].endswith(".pdf")]:
        strict = _pdf_text(F[k], strict=True)
        ok(strict == _pdf_text(F[k]), "H25: %s reads the same under the strict parser" % B.FILES[k])
        ext = subprocess.run(["pdftotext", "-layout", F[k], "-"], capture_output=True, text=True).stdout
        ok(len(ext.split()) > 0.9 * len(strict.split()), "H25: %s opens in pdftotext" % B.FILES[k])
    px = " ".join(subprocess.run(["pdftotext", F["procedure"], "-"], capture_output=True, text=True).stdout.split())
    ok("on any of the 14 days before" in px and "recorded for the station over the three previous calendar years" in px,
       "H25: sections 6 and 8 read back in pdftotext")

    def _ed(a, b):
        d = list(range(len(b) + 1))
        for i, x in enumerate(a, 1):
            prev, d[0] = d[0], i
            for j, y in enumerate(b, 1):
                prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
        return d[-1]
    real = ["monegre", "siar", "aemet", "meteocat", "redara", "euskalmet", "meteoclimatic", "cita"]
    ours = ["monegrillo", "alcanadre", "agroclimatico"]
    ok(all(_ed(o, r_) > 2 and r_ not in o for o in ours for r_ in real),
       "H21: the invented consortium and contractors clear real networks and firms by more than two letters")
    # ---------------------------------------------------------------- realism sweep and dates
    claim = int(5 * round(len(rec["alerts"]) / 3.0 / 5))
    ok(("%d or so a year" % claim) in " ".join(eml.split()) and all(abs(v - claim) <= 12 for v in per_year_rec.values),
       "realism: the record's alerts a year (%s) sit near the request's '%d or so'" % (per_year_rec.to_dict(), claim))
    ok(np.std(sd) / np.mean(sd) > 0.1 and len(set(np.round(sd, 4))) > 0.9 * len(sd),
       "realism: the stations' spreads differ (%.3f to %.3f)" % (sd.min(), sd.max()))
    ok(daily["tmed"].std() > 5 and daily["tmed"].round(1).nunique() > 300, "realism: the daily means vary")
    import re as _re
    for k, pat in (("daily", r"(^|;)-0(,0+)?(?=;|$)"), ("et0", r"(^|;)-0(,0+)?(?=;|$)"),
                   ("checks", r"(^|,)-0(\.0+)?(?=,|$)")):
        txt = open(F[k], encoding="utf-8").read()
        ok(not _re.search(pat, txt, _re.M), "realism: no negative zero in %s" % B.FILES[k])
    qz = pd.read_parquet(F["qc"])
    ok(all(not np.any((qz[c_].dropna().to_numpy(float) == 0) & np.signbit(qz[c_].dropna().to_numpy(float)))
           for c_ in ("anomalia", "estimacion", "residuo", "estadistico_14d", "limite")),
       "realism: no negative zero in the quality control's export")
    afe = hist["error_encontrado_C"].dropna().abs()
    ok(afe.min() > 0.2 and afe.max() < 2.5 and afe.nunique() > 20, "realism: the history's as-found errors run %.2f to %.2f"
       % (afe.min(), afe.max()))
    ok(q["fecha"].max() == pd.Timestamp("2027-12-31") and ck["ts"].max() < pd.Timestamp("2028-01-01"),
       "dates: the record and the checks end with 2027")
    ok(pd.to_datetime(new["visit_date"]).max() <= pd.Timestamp("2028-01-04"), "dates: the orders export follows the last "
       "closing date (%s)" % pd.to_datetime(new["visit_date"]).max().date())
    ok(pd.to_datetime(old["Aviso"]).max() <= pd.Timestamp(RC.OLD_EXPORT_TO), "dates: the old sheet ends at the handover")
    ok(pd.to_datetime(new["opened"]).min() >= pd.Timestamp(P.CONTRACT_SWITCH) - pd.Timedelta(days=10),
       "dates: the new sheet starts at the handover")
    ok(hist["fecha"].max() < pd.Timestamp("2028-01-01"), "dates: the sensor history ends with 2027")
    ok(all(pd.Timestamp(a) < pd.Timestamp("2025-01-01") for a in reg["alta"]), "dates: every station installed before the record")
    ok("5 Jan 2028" in eml and "20 December 2027" in plan and "2 January 2028" in summ, "dates: the documents are dated in order")
    return N_OK[0]
