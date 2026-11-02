"""task247 generator checks, run by make.py on the built pack: the call, its refill variants and conventions, the
rungs, the analyst test on the simulator's clean truth (R3), every row of the design note's semantic fork table (SF1 to
SF18), the separation of the ask files from the call (S1), the ask's device, its forcing and its stops, the input gates,
the pack's dates and that no shipped file describes the data."""
import datetime as dt
import os
import re
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
    # SF17 (the ask's convention) the logger seasons on the loggers' local clock against UTC: the same hours
    dep, reg = pk.logger_log()
    where = pk.pin_sites()
    rd = pd.read_csv(os.path.join(target, F["readings"]), dtype={"serial": str})
    rd["t"] = pd.to_datetime(rd.datetime_local)
    rd["u"] = rd.t + pd.Timedelta(hours=5)
    h = pk.logger_hours()
    hu = {c: 0 for c in pk.codes}
    for r, site in zip(dep.itertuples(index=False), where):
        if not isinstance(r.retrieved, str):
            continue
        a, z = solve.log_time(r.deployed), solve.log_time(r.retrieved)
        x = rd[(rd.serial == r.serial) & (rd.t >= a) & (rd.t <= z)]
        x = x[x.u.dt.year.isin([2024, 2025, 2026]) & x.u.dt.month.between(6, 10)]
        hu[site] += int((x.temperature_c >= pk.mmm[site]).sum())
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
    """S1: the call computed from the pack without the logger files and the distractors; and the ask computed without
    the call's documents and every distractor (each deleted file read by no step of the other)"""
    F = B.FILES
    for drop, what in ((("deployments", "pins", "readings") + tuple(B.DISTRACTORS), "the call"),
                       (tuple(B.DISTRACTORS), "the ask")):
        tmp = tempfile.mkdtemp()
        for k in B.PACK:
            if k not in drop:
                shutil.copy(os.path.join(target, F[k]), tmp)
        try:
            pk, b, rows = solve.solve(tmp, F)
            if what == "the call":
                ok([r["site"] for r in rows if r["level"] == "Alert Level 2"] == GOLD, "S1: the call without the ask files")
            else:
                full = solve.Pack(target, F).logger_hours()
                ok(pk.logger_hours() == full, "S1: the ask without the distractors")
        finally:
            shutil.rmtree(tmp)


def ask_checks(target, pk):
    """the ask: each site's hours at or above its MMM at its logger while in the water, June to October 2024 to 2026.
    The log names each deployment by the tag on the site's pin as the divers read it; the dive team re-tagged the pins
    north to south on the Cozumel II's retrieval trip of August 2025 and the pin register holds the current tags. The
    device is silent to the hygiene battery, moves every figure under the register's reading and under the over-clean,
    and the rows leave one reading: the stop order of every trip and the logger pairs that stay on one pin across the
    re-tag. Every acceptable reconstruction files the golden."""
    import verify as V
    import writeup as WU
    F = B.FILES
    dep, reg = pk.logger_log()
    H = pk.logger_hours()
    rd = pd.read_csv(os.path.join(target, F["readings"]), dtype={"serial": str})
    trips = pk.service_trips()
    north = list(pk.sites.sort_values("latitude", ascending=False).site_code)
    # the battery passes: nothing is orphaned, repeated, overlapping or out of sequence
    ok(sorted(reg) == sorted(set(dep.pin)) and sorted(reg.values()) == sorted(pk.codes), "battery: every pin joins the register")
    ok(not dep.duplicated().any() and not rd.duplicated(["serial", "datetime_local"]).any(), "battery: no repeated rows")
    ok(set(rd.serial) == set(dep.serial), "battery: every serial in the log and in the readings")
    ok(len(trips) == 9 and all(len(t["stops"]) == 16 for t in trips), "battery: every pin once on every trip")
    for key in ("pin", "serial"):
        for k, g in dep.groupby(key):
            g = g.assign(a=g.deployed.map(solve.log_time)).sort_values("a")
            ok(all(solve.log_time(g.retrieved.iloc[j]) <= g.a.iloc[j + 1] for j in range(len(g) - 1)),
               ("battery: no overlap", key, k))
    ok(not dep.notes.fillna("").str.contains(r"PB\d\d|E\d\d").any(), "battery: no note names a site or a pin")
    # the device moves every figure: the register's reading (the careful solver's) and the over-clean
    reg_h, drop_h = pk.logger_hours(pins="register"), pk.logger_hours(pins="drop")
    for c in pk.codes:
        ok(reg_h[c] != H[c] and drop_h[c] != H[c], ("the ask: the register and the over-clean miss", c))
    ok(min(abs(reg_h[c] - H[c]) for c in pk.codes) >= 5, ("the register's reading moves every figure by several bins", reg_h))
    # the rows force the golden: every trip's stops run north to south, four a day, on the golden's reading; on the
    # register's only the four trips from the re-tag do
    where = pk.pin_sites()
    rows_of = {}
    for t in trips:
        for when, pin, i, kind in t["events"]:
            rows_of.setdefault(id(t), {})[pin] = where[i]
    follow_gold = sum([rows_of[id(t)][x] for x in t["stops"]] == north for t in trips)
    follow_reg = sum([reg[x] for x in t["stops"]] == north for t in trips)
    ok(follow_gold == 9 and follow_reg == 4, ("the stop order forces the earlier tags", follow_gold, follow_reg))
    ok(all(t["events"][0][0] >= pd.Timestamp("2025-08-18") for t in trips if [reg[x] for x in t["stops"]] == north) and
       all(t["events"][-1][0] <= pd.Timestamp("2025-08-15") for t in trips if [reg[x] for x in t["stops"]] != north),
       "the register's trips are exactly those from the re-tag")
    # the logger pairs that stay on one pin across the re-tag: one site on the golden's reading, two on the register's
    pairs = {}
    for r, site in zip(dep.itertuples(index=False), where):
        pairs.setdefault(r.serial, set()).add((site, reg[r.pin], solve.log_time(r.deployed) >= pd.Timestamp("2025-08-16")))
    across = [s for s, v in pairs.items() if {x[2] for x in v} == {True, False}]
    ok(len(across) >= 6 and all(len({x[0] for x in pairs[s]}) == 1 for s in across) and
       all(len({x[1] for x in pairs[s]}) == 2 for s in across), ("the pairs across the re-tag", across))
    # rival readings: the verifier's day-by-day reconstruction and the golden's trip-by-trip one agree row by row;
    # every earlier tag reads as one site on all five trips (asserted inside pin_sites); the register's reading and the
    # over-clean are ruled out above
    vw, old = V.pin_site(target, list(pd.read_csv(os.path.join(target, F["sites"])).to_dict("records")))
    ok(vw == where, "rival: the day-by-day reconstruction files the golden's placement")
    ok(len(old) == 16 and all(reg[p] != c for p, c in old.items()), ("every pin carried another tag before", old))
    # hazards: the Cozumel II's GPS clock (found from the loggers' own step out of the water) and the trimming
    off = WU.gps_offsets(target, F)
    for trip, (lo, hi, n) in off.items():
        utc = trip in ("Cozumel II 2025-08", "Cozumel II 2026-04")
        ok((3.0 <= lo and hi <= 5.0) if utc else (-2.0 <= lo and hi <= 0.0), ("the ask, the GPS offsets", trip, lo, hi))
        ok(n == 16, ("the ask, every site on every trip", trip))
    hn, ha = pk.logger_hours(gps=False), pk.logger_hours(trim=False)
    for c in pk.codes:
        ok(hn[c] != H[c] and ha[c] != H[c], ("the ask, the clock and the untrimmed", c))
    # the clock is the log's own: a time carries the GPS's UTC mark exactly when that boat's GPS kept UTC (the Cozumel
    # II before its unit was replaced in June 2026), and the verifier's reader of the mark agrees with the golden's
    for r in dep.itertuples(index=False):
        for when, boat in ((r.deployed, r.deployed_from), (r.retrieved, r.retrieved_from)):
            if not isinstance(when, str):
                continue
            utc = boat == solve.GPS_UTC[0] and when[:10] < solve.GPS_UTC[1].isoformat()
            ok(when.endswith(" UTC") == utc, ("SF19 the log's UTC mark", when, boat))
            ok(pd.Timestamp(V.local_time(when)) == solve.log_time(when), ("the two readers of the mark", when))
    ok(sum(dep.retrieved.fillna("").str.endswith(" UTC")) == 32 and sum(dep.deployed.str.endswith(" UTC")) == 16,
       "the marked times: the Cozumel II's August 2025 retrievals and its April 2026 swap")
    # the pin register is the list as the divers last checked it: each pin's checked date is its stop on the last
    # service trip, so the register states the tags as they stood from August 2025 on and says nothing of a tag written
    # before; the earlier tags are the rows' (the stop order and the pairs above)
    rg = pd.read_csv(os.path.join(target, F["pins"]))
    last = {r.pin: solve.log_time(r.deployed).date().isoformat() for r in dep.itertuples(index=False)
            if solve.log_time(r.deployed) >= pd.Timestamp("2027-04-01")}
    ok(list(rg.columns) == ["pin", "site_code", "checked"] and dict(zip(rg.pin, rg.checked)) == last,
       ("SF18 the register's checked dates are the April 2027 stops", dict(zip(rg.pin, rg.checked)), last))
    ok(max(solve.log_time(x) for x in list(dep.deployed) + list(dep.retrieved.dropna())) <
       pd.Timestamp(max(rg.checked)) + pd.Timedelta(days=1), "no log time after the register was last checked")


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


def no_describing(target):
    """no shipped file describes the data (dataset-generation section 3): none by name (no readme, dictionary, codebook,
    manifest, field notes, definitions or file list, no notes file), and no document that lists a data file's columns,
    read through the verifier's own extractor (positive control first) and judged by the leak sweep's own rule (eight
    identifier-like column names, or two fifths of one file's columns with three identifiers)"""
    import verify as V
    F = B.FILES
    shipped = sorted(os.listdir(target))
    describing = ("readme", "dictionary", "codebook", "manifest", "field_notes", "fieldnotes", "definitions",
                  "file_list", "data_notes", "extract_notes", "export_notes", "schema")
    ok(not [f for f in shipped if any(w in f.lower().replace("-", "_") for w in describing)],
       ("a file whose name says it describes the data", shipped))
    ok(not [f for f in shipped if f.lower().endswith((".md", ".txt", ".docx", ".rtf", ".html"))], ("a notes file", shipped))
    cols = {}
    for f in shipped:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
            cols[f] = {c for c in head if len(c) >= 4}
    text = {}
    for f in shipped:
        if f.endswith(".pdf"):
            text[f] = " ".join(V.pdf_text(os.path.join(target, f)).split())
        elif f.endswith(".eml"):
            text[f] = open(os.path.join(target, f), encoding="utf-8").read()
    # the positive control, through the same extractor and the same search: the methods note names two register fields
    find = lambda c, t: re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), t) is not None
    ok(find("pixel_id", text[F["methods"]]) and find("mmm_c", text[F["methods"]]) and
       find("genus", text[F["protocol"]]), "control: the extractor and the search see the field names a document carries")
    every = set().union(*cols.values())
    for d, t in text.items():
        found = {c for c in every if find(c, t)}
        ident = {c for c in found if "_" in c or re.search(r"\d", c) or re.search(r"[a-z][A-Z]", c)}
        worst = max((len(found & cs) / len(cs) for cs in cols.values() if len(cs) >= 5 and len(found & cs) >= 5),
                    default=0.0)
        ok(len(ident) < 8 and not (worst >= 0.4 and len(ident) >= 3), ("a document lists the data's columns", d,
                                                                       sorted(found), round(worst, 2)))


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
    ok(len(set(hours)) == 16, "realism: the loggers' hours all differ")
    ok(all(h % 100 for h in hours), "realism: no round headline counts")
    ok(round(b, 4) not in (0.05, 0.06, 0.1), "realism: the clear-sky difference is not a round number")


def run(target, W, fig, golden):
    Count.n = 0
    pk, b, rows = call_checks(target, W)
    fork_checks(target, pk, b, rows)
    three_rules(target, W, pk, b, rows)
    separation(target)
    ask_checks(target, pk)
    gates(target)
    no_describing(target)
    S = {s["code"]: s for s in fig["sites"]}
    for r in rows:
        ok(S[r["site"]]["survey"] == (r["site"] in GOLD), ("figures.json", r["site"]))
    ok(os.path.exists(os.path.join(golden, "reef_heat_stress_2027.xlsx")), "golden workbook")
    ok(os.path.exists(os.path.join(golden, "survey_list_note_2027.pdf")), "golden note")
    return Count.n
