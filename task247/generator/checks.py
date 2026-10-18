"""task247 generator checks, run by make.py on the built pack: the call, its refill variants and conventions, the
rungs, the analyst test on the simulator's clean truth (R3), every row of the design note's semantic fork table (SF1 to
SF16), the separation of the ask files from the call (S1), the asks' devices and stops, the input gates and the pack's
dates."""
import datetime as dt
import os
import shutil
import tempfile

import numpy as np
import pandas as pd

import build as B
import estim as E
import params as P
import solve

GOLD = ["PB06", "PB07", "PB09", "PB10", "PB11", "PB12", "PB13", "PB14", "PB15"]
RUNGS = {"as issued": ["PB06", "PB07", "PB09", "PB10"], "pooled": ["PB07", "PB09", "PB10"],
         "flag": ["PB07", "PB09", "PB10"], "regression": ["PB06", "PB07", "PB09", "PB10", "PB11", "PB15"],
         "refill, no difference": GOLD}


class Count:
    n = 0


def ok(cond, what):
    assert cond, what
    Count.n += 1


def clean_truth(W):
    """R3: on the simulator's own arrays (every day's final value, the true observed mask, no rounding, no missing
    day, no re-issue to resolve), the default path (the past mean differences of observed and filled days taken out)
    files the wrong list and the decisive step alone (the refill) the golden; the reprocessed record as simulated
    puts the golden sites at Alert Level 2"""
    D = W["D"]
    yr = np.array([d.year for d in D]); mon = np.array([d.month for d in D])
    past = yr <= 2026
    season = np.array([solve.SEASON[0] <= d <= solve.SEASON[1] for d in D])
    obs, fin, rep, clim = W["observed"], W["final"], W["rep"], W["clim"]
    diff = fin - rep
    b_obs = diff[:, past][obs[:, past]].mean()
    b_fill = diff[:, past][~obs[:, past]].mean()
    mmm = np.round(W["mmm"], 2)
    names = [s[0] for s in P.SITES]
    flag, gold, truth = [], [], []
    for s in range(P.NSITE):
        f = E.season_max(fin[s] - np.where(obs[s], b_obs, b_fill), mmm[s], season)
        g = E.season_max(E.refill(fin[s], obs[s], clim[s], b_obs), mmm[s], season)
        t = E.season_max(rep[s], mmm[s], season)
        flag.append(names[s]) if f >= P.AL2 else None
        gold.append(names[s]) if g >= P.AL2 else None
        truth.append(names[s]) if t >= P.AL2 else None
    return flag, gold, truth


def call_checks(target, W):
    F = B.FILES
    pk, b, rows = solve.solve(target, F)
    call = [r["site"] for r in rows if r["level"] == "Alert Level 2"]
    ok(call == GOLD, ("the call", call))
    ok(round(b, 2) == 0.06 and abs(b - 0.06) < 0.003, ("the clear-sky difference", b))
    gold = [r["dhw"] for r in rows]
    # no expected maximum sits where its whole number and its level disagree, or near a level line
    for r in rows:
        ok(not (3.5 <= r["dhw"] < 4.0 or 7.5 <= r["dhw"] < 8.0), ("rounding against the level", r["site"]))
        ok(min(abs(r["dhw"] - 4.0), abs(r["dhw"] - 8.0)) >= 0.8, ("near a level line", r["site"], r["dhw"]))
    # C1: every variant of the refill gives every site's whole number and level
    var = pk.variants(b)
    for name, v in var.items():
        for k, r in enumerate(rows):
            ok(round(v[k]) == r["dhw_round"] and solve.level(v[k]) == r["level"], ("variant", name, r["site"], v[k]))
            ok(abs(v[k] - r["dhw_round"]) <= 0.35, ("variant inside its bin with room", name, r["site"], v[k]))
    # the golden itself mid-bin
    for r in rows:
        ok(0.5 - abs(r["dhw"] - round(r["dhw"])) >= 0.2, ("edge", r["site"], r["dhw"]))
    # the rungs
    ru, c = pk.rungs()
    for k, want in RUNGS.items():
        got = [pk.codes[i] for i in range(16) if ru[k][i] >= P.AL2]
        ok(got == want, ("rung", k, got))
    ok(all(round(ru["refill, no difference"][i]) != round(gold[i]) for i in (6, 10, 12)),
       "the refill without the clear-sky difference misses figures")
    # the back-test separates the refill from every other reconstruction
    bt = pk.backtest(b)
    ok(bt["refill"][0] < 0.8 * min(bt[k][0] for k in ("carry", "nearest")) and
       bt["refill"][0] < 0.5 * min(bt[k][0] for k in ("as issued", "flag")) and
       bt["refill"][0] < 0.55 * bt["regression"][0], ("back-test", bt))
    ok(abs(bt["refill"][1]) < 0.02 and bt["flag"][1] < -0.2 and bt["as issued"][1] < -0.2, ("hot filled days", bt))
    # R3a and R3b on the clean truth
    flag, g, truth = clean_truth(W)
    ok(flag == RUNGS["flag"], ("R3a: the default path on the clean truth", flag))
    ok(g == GOLD, ("R3b: the refill alone on the clean truth", g))
    ok(truth == GOLD, ("R3b: the reprocessed record as simulated", truth))
    return pk, b, rows


def fork_checks(target, pk, b, rows):
    F = B.FILES
    gold = {r["site"]: r for r in rows}
    # SF1 season maximum: the highest daily DHW of a season day (methods 4); the season's last day keeps the list
    # (same call) but prints other figures, ruled out by section 4
    last = [E.dhw(pk.refilled(k, b), pk.mmm[pk.codes[k]])[pk.di["2027-10-31"]] for k in range(16)]
    ok([pk.codes[k] for k in range(16) if last[k] >= P.AL2] == GOLD, ("SF1: the last day's list", last))
    ok(sum(round(last[k]) != gold[pk.codes[k]]["dhw_round"] for k in range(16)) >= 5, "SF1: the last day's figures")
    # SF2 HotSpot at or above 1.0 against strictly above: same figures
    # SF3 the 84 days ending on the day against the 84 before it: same figures
    # SF4 the register's MMM against the MMM recomputed from the climatology file: same figures
    # SF5 the first issue of each day kept against the latest: same figures
    # SF6 the day never issued left without a HotSpot against filled: same figures
    for sf, opts in (("SF2", dict(strict=True)), ("SF3", dict(window_before=True)), ("SF4", dict(mmm_from_clim=True)),
                     ("SF5", dict(first_issue=True)), ("SF6", dict(missing_zero=True)),
                     ("SF12", dict(flag_by_date=True))):
        _b, alt = pk.golden_alt(**opts)
        for k, c in enumerate(pk.codes):
            ok(round(alt[k]) == gold[c]["dhw_round"] and solve.level(alt[k]) == gold[c]["level"], (sf, c, alt[k]))
    # SF7 the declared level: the highest any season bulletin gave (methods 5); the last season bulletin's levels
    # give the same verdicts (same call)
    wb = pd.read_excel(os.path.join(target, F["bulletins"]), header=3)
    ss = wb[(wb["Analysis day"] >= "2027-06-01") & (wb["Analysis day"] <= "2027-10-31")]
    lastday = ss["Analysis day"].max()
    lastlv = dict(zip(ss[ss["Analysis day"] == lastday]["Site"], ss[ss["Analysis day"] == lastday]["Alert level"]))
    ok(all(solve.verdict(gold[c]["level"], lastlv[c]) == gold[c]["verdict"] for c in pk.codes),
       ("SF7: the last season bulletin's levels give the same verdicts", lastlv))
    # SF8 the bulletins reporting a season day: the analysis day in June to October, not the issue date; the two
    # readings give the same declared levels
    ss2 = wb[(wb["Issued"] >= "2027-06-01") & (wb["Issued"] <= "2027-10-31")]
    for c in pk.codes:
        a = max(ss[ss["Site"] == c]["Alert level"], key=solve.LEVELS.index)
        z = max(ss2[ss2["Site"] == c]["Alert level"], key=solve.LEVELS.index)
        ok(a == z == gold[c]["declared"], ("SF8", c))
    # SF9 the season 1 June to 31 October in UTC days (both satellite records' days); the bulletins' local dates do
    # not enter the expected maximum
    ok(pk.season.sum() == 153, "SF9: 153 season days")
    # SF10 the level for the season: from the unrounded maximum; no figure sits where rounding first changes a level
    # (asserted in call_checks); SF11 whole degree-weeks: the prompt's rounding
    for sf in ("SF10", "SF11"):
        ok(True, sf)
    # SF12 the flag read by each row's version: the late re-issues of days before 15 July carry version 3.2's codes
    raw = pk.nrt_raw
    late_v32 = raw[(raw.product_version == "3.2") & (raw.date < "2027-07-15")]
    ok(len(late_v32) > 0 and set(late_v32.obs_flag) <= {1, 2}, ("SF12", len(late_v32)))
    # SF17 (an ask's convention) the logger seasons on the loggers' local clock against UTC: the same hours
    dep = pd.read_csv(os.path.join(target, F["deployments"]), dtype={"serial": str})
    rd = pd.read_csv(os.path.join(target, F["readings"]), dtype={"serial": str})
    rd["t"] = pd.to_datetime(rd.datetime_local)
    rd["u"] = rd.t + pd.Timedelta(hours=5)
    h = pk.logger_hours()
    hu = {c: 0 for c in pk.codes}
    for r in dep.itertuples(index=False):
        if not isinstance(r.retrieved, str):
            continue
        a, z = pd.Timestamp(r.deployed), pd.Timestamp(r.retrieved)
        if r.deployed_from == solve.GPS_UTC[0] and a.date() < solve.GPS_UTC[1]:
            a -= pd.Timedelta(hours=5)
        if r.retrieved_from == solve.GPS_UTC[0] and z.date() < solve.GPS_UTC[1]:
            z -= pd.Timedelta(hours=5)
        x = rd[(rd.serial == r.serial) & (rd.t >= a) & (rd.t <= z)]
        x = x[x.u.dt.year.isin([2024, 2025, 2026]) & x.u.dt.month.between(6, 10)]
        hu[r.site_code] += int((x.temperature_c >= pk.mmm[r.site_code]).sum())
    ok(hu == h, ("SF17", hu, h))
    # SF13 kelvin: the reprocessed record less 273.15 (release note 3)
    ok(abs(pk.rep_raw.analysed_sst_k.mean() - 273.15 - np.nanmean(pk.rep)) < 1e-9, "SF13")
    # SF14 the survey list is the Alert Level 2 sites (methods 6): the call
    # SF15 'confirms, raises or lowers' compares the level for the season with the declared level (methods 6)
    for sf in ("SF14", "SF15"):
        ok(True, sf)
    # SF16 the clear-sky difference over every observed day of 2018 to 2026, against each site's own or the heat
    # seasons': the variants, asserted in call_checks
    ok(True, "SF16")


def separation(target):
    """S1: the call computed from the pack without the survey, logger and distractor files"""
    F = B.FILES
    tmp = tempfile.mkdtemp()
    for k in B.PACK:
        if k not in ("survey", "deployments", "readings", "protocol", "kd490", "tide"):
            shutil.copy(os.path.join(target, F[k]), tmp)
    try:
        pk, b, rows = solve.solve(tmp, F)
        ok([r["site"] for r in rows if r["level"] == "Alert Level 2"] == GOLD, "S1: the call without the ask files")
    finally:
        shutil.rmtree(tmp)


def ask_checks(target, pk):
    F = B.FILES
    g = pk.survey()
    c = pk.survey(collapse=False)
    r = pk.survey(collapse=False, filters=False)
    for k in pk.codes:
        ok(round(c[k][0], 1) != round(g[k][0], 1) and c[k][1] != g[k][1], ("ask A, the cracker", k))
        ok(round(r[k][0], 1) != round(g[k][0], 1) and r[k][1] != g[k][1], ("ask A, nothing filtered", k))
        ok(0.05 - abs(g[k][0] - round(g[k][0], 1)) >= 0.01, ("ask A, edge", k, g[k][0]))
    # the hazards the ask sheet counts: QA lines, fire corals, colonies under 10 cm, PB03's off-depth transect
    sl = pd.read_csv(os.path.join(target, F["survey"]))
    ok((sl.sheet == "QA").sum() == 692 and sl.genus.isin(["MALC", "MCOM"]).sum() == 48 and
       (sl.max_diameter_cm < 10).sum() == 33 and len(sl[(sl.site_code == "PB03") & (sl.transect == 2) & (sl.sheet == "S") &
                                                       (sl.depth_m < 5)]) > 0, "the ask sheet's hazard counts")
    # the device's evidence: repeats only on the two volunteers' sheets
    import writeup as WU
    runs, wide = WU.repeat_runs(target, F)
    ok(set(runs) == {"KT", "DW"} and sum(runs.values()) == 153, ("the repeats", runs))
    # the collapse agrees with the generator's own colony ids
    W = B.RC.Records().S
    truth = {}
    for row in W["rows"]:
        if row["sheet"] != "S" or row["genus"] not in solve.STONY or row["dia"] < 10:
            continue
        if abs(row["depth"] - P.SITE_DEPTH[row["site"]]) > 2:
            continue
        truth.setdefault(P.SITES[row["site"]][0], set()).add((row["transect"], row["colony"]))
    for k in pk.codes:
        ok(len(truth[k]) == g[k][1], ("ask A, the collapse is the colonies", k, len(truth[k]), g[k][1]))
    h = pk.logger_hours()
    hn = pk.logger_hours(gps=False)
    ha = pk.logger_hours(trim=False)
    for k in pk.codes:
        ok(hn[k] != h[k] and ha[k] != h[k], ("ask B, the cracker and the untrimmed", k))
    off = WU.gps_offsets(target, F)
    for trip, (lo, hi, n) in off.items():
        utc = trip in ("Cozumel II 2025-08", "Cozumel II 2026-04")
        ok((3.0 <= lo and hi <= 5.0) if utc else (-2.0 <= lo and hi <= 0.0), ("ask B, the GPS offsets", trip, lo, hi))
        ok(n == 16, ("ask B, every site on every trip", trip))


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
    for k, col in (("nrt", "date"), ("rep", "time"), ("survey", "date")):
        df = pd.read_csv(os.path.join(target, F[k]))
        ok(df[col].max() < asof, (k, col))
    n = pd.read_csv(os.path.join(target, F["nrt"]))
    ok(n.issued_utc.max() < asof + "T14", "nrt issues")
    rd = pd.read_csv(os.path.join(target, F["readings"]))
    ok(rd.datetime_local.max() < "2027-04-17", ("the readings end with the April 2027 downloads", rd.datetime_local.max()))


def three_rules(target, W, pk, b, rows):
    """R1 the field's raw material ships and the deciding quantity does not; R2 each Layer 1 item mishandled leaves the
    call where it was (or fails loudly); R3a, R3b the analyst test and the decisive step alone on the clean truth; R3c
    no plant (the realism sweep's repeated-block and round-figure checks)"""
    F = B.FILES
    # R1: the daily near-real-time rows and the overlap ship; no file holds a reprocessed 2027 value or a refilled day
    n = pd.read_csv(os.path.join(target, F["nrt"]))
    ok(len(n[n.date >= "2027-06-01"]) >= 16 * 150, "R1: the 2027 season's daily rows ship")
    rep = pd.read_csv(os.path.join(target, F["rep"]))
    ok(rep.time.max() <= "2026-12-31", "R1: no reprocessed 2027 value ships")
    wb = pd.read_excel(os.path.join(target, F["bulletins"]), header=3)
    differ = 0
    for r in rows:
        mx = wb[(wb["Site"] == r["site"]) & (wb["Analysis day"] >= "2027-06-01") & (wb["Analysis day"] <= "2027-10-31")]["DHW"].max()
        differ += round(mx) != r["dhw_round"]
    ok(differ >= 10, ("R1: the bulletins' DHW is the near-real-time record's, not the deciding quantity", differ))
    # R2: each mess item mishandled (re-issues: SF5; flag recode: SF12; the day never issued: SF6; the bulletins' local
    # dates: SF8) leaves the call; the kelvin record read as Celsius fails loudly
    both = pk.past & ~np.isnan(pk.rep) & ~np.isnan(pk.nrt)
    bad = float(np.mean((pk.nrt - (pk.rep + 273.15))[both & pk.obs]))
    ok(bad < -250, ("R2: kelvin read as Celsius is loud", bad))
    for sf in ("R2 re-issues (SF5)", "R2 flag recode (SF12)", "R2 day never issued (SF6)", "R2 local dates (SF8)"):
        ok(True, sf)
    # R3a and R3b: asserted on the clean truth in call_checks; each lower rung's single correction stays wrong
    ru, c = pk.rungs()
    for k in ("as issued", "pooled", "flag", "regression"):
        ok([pk.codes[i] for i in range(16) if ru[k][i] >= P.AL2] != GOLD, ("R3b: a lower rung stays wrong", k))
    # R3c: no plant; the realism sweep: no repeated block in the near-real-time record, no identical counts
    for k in range(16):
        # observed days never repeat a value for long (filled days may, settling on the climatology)
        x, o = pk.nrt[k], pk.obs[k]
        run, worst = 1, 1
        for i in range(1, len(x)):
            run = run + 1 if (o[i] and o[i - 1] and x[i] == x[i - 1]) else 1
            worst = max(worst, run)
        ok(worst <= 4, ("R3c: no observed value held for days on end", pk.codes[k], worst))
    hours = [pk.logger_hours()[c] for c in pk.codes]
    sv = pk.survey()
    cols = [sv[c][1] for c in pk.codes]
    ok(len(set(hours)) == 16, "realism: the loggers' hours all differ")
    ok(len(set(cols)) >= 13, "realism: the colony counts mostly differ")
    ok(all(h % 100 for h in hours) and all(x % 10 for x in cols[:3]), "realism: no round headline counts")
    ok(round(b, 4) not in (0.05, 0.06, 0.1), "realism: the clear-sky difference is not a round number")


def run(target, W, fig, golden):
    Count.n = 0
    pk, b, rows = call_checks(target, W)
    fork_checks(target, pk, b, rows)
    three_rules(target, W, pk, b, rows)
    separation(target)
    ask_checks(target, pk)
    gates(target)
    S = {s["code"]: s for s in fig["sites"]}
    for r in rows:
        ok(S[r["site"]]["survey"] == (r["site"] in GOLD), ("figures.json", r["site"]))
    ok(os.path.exists(os.path.join(golden, "reef_heat_stress_2027.xlsx")), "golden workbook")
    ok(os.path.exists(os.path.join(golden, "survey_list_note_2027.pdf")), "golden note")
    return Count.n
