"""task241 checks: every semantic fork (SF1 to SF13), the ladder's rungs and margins, the analyst test on the clean
truth, the oracles, the separation of the ask devices from the main population, each ask's golden against the truth
and against the routes that miss it, and the input gates. Run from make.py after every build."""
import glob
import os

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import params as P
import solve as S_

N = [0]
LOG = []
EDGE = float(os.environ.get("TASK241_EDGE", "0.05"))   # points between a graded share and its rounding edge


def ok(cond, msg):
    assert cond, msg
    N[0] += 1


def note(msg):
    LOG.append(msg)


def local_hours(placed, states, zones, arizona_dst=False):
    zmap = dict(zip(zones["state"], zones["time_zone"].map(S_.ZONES)))
    if arizona_dst:
        zmap = {k: ("America/Denver" if v == "America/Phoenix" else v) for k, v in zmap.items()}
    z = pd.Series(states).map(zmap).values
    loc = pd.Series(placed).dt.tz_localize("America/Chicago", ambiguous="NaT", nonexistent="NaT")
    out = np.full(len(z), np.nan)
    for zone in pd.unique(z):
        if not isinstance(zone, str):
            continue                      # a household the route cannot place
        idx = np.flatnonzero(z == zone)
        lt = loc.iloc[idx].dt.tz_convert(zone)
        out[idx] = (lt.dt.hour + lt.dt.minute / 60.0 + lt.dt.second / 3600.0).values
    return out


def interval(order, golden):
    """is the golden set one contiguous block of this ordering"""
    pos = sorted(order.index(j) for j in golden)
    return pos[-1] - pos[0] == len(golden) - 1


def run(target, golden_dir, W, S, A):
    N[0] = 0
    LOG.clear()
    calls, inbound, reg, jobs, cases, zones = S["calls"], S["inbound"], S["reg"], S["jobs"], S["cases"], S["zones"]
    raw = S["raw"]
    m = S["main"].set_index("job")
    gold = sorted(m.index[m["off"]])
    ret = S["ret"]

    # ---- the main call: the golden set, its margins and the fork table --------------------------------------------
    ok(len(gold) == 6, "golden set is not six projects: %s" % gold)
    ok(sorted(A["off"]) == gold, "write-up off set differs from the solve")
    share = m["share"]
    ok((share - P.LIMIT).abs().min() >= 0.03, "SF10: a project within three points of the limit")
    note("nearest under the limit %s %.2f, lowest over %s %.2f" % (share[~m["off"]].idxmax(), 100 * share[~m["off"]].max(),
                                                                  share[m["off"]].idxmin(), 100 * share[m["off"]].min()))
    # SF1: the two detector codes are one detector result column
    for p in sorted(glob.glob(os.path.join(target, "dialer_exports", "*.csv"))):
        d = pd.read_csv(p, dtype=str, keep_default_na=False)
        if "CallID" in d.columns:
            ok(((d["AMD"] == "M") == (d["Disp"] == "A")).all(), "SF1: AMD letter and disposition disagree in " + p)
        else:
            ok(((d["amd_result"] == "MACHINE") == (d["outcome"] == "AMD_MACHINE")).all(), "SF1: amd_result disagrees in " + p)
    by_col = calls[calls["amd"].eq("MACHINE")].groupby("job").size().reindex(jobs)
    ok((by_col.values == m["n_am"].values).all(), "SF1: machine-classed counts differ by column")
    # SF2 and SF5: one line per job, and every return within the window lands on the calling project's line
    lines = S_.line_jobs(reg)
    ok(len(set(lines)) == len(jobs) == len(set(lines.values())), "SF2: the register's lines are not one to one")
    r20 = ret[(ret["delay_min"] <= 20) & ret["job"].isin(jobs)]
    ok((r20["dialed_line"].map(lines) == r20["job"]).all(), "SF5: a return landed on another project's line")
    # SF3: the repeated day is an exact copy, and the year window is the same in UTC
    dup = raw[raw.duplicated("call_id", keep=False)]
    ok(len(dup) > 0 and dup.drop_duplicates().shape[0] == dup["call_id"].nunique(), "SF3: a repeated row is not an exact copy")
    raw_m = S_.main_call(raw.sort_values(["placed", "call_id"]).reset_index(drop=True), inbound, jobs)
    ok(sorted(raw_m.loc[raw_m["off"], "job"]) == gold, "SF3: keeping the repeated rows moves the call")
    note("SF3 repeated rows %d; shares with them kept %s" % (len(dup) - dup["call_id"].nunique(),
                                                             (raw_m["share"] * 100).round().astype(int).tolist()))
    edge = calls[(calls["placed"] < pd.Timestamp("2026-01-01 06:00")) | (calls["placed"] >= pd.Timestamp("2026-12-31 18:00"))]
    ok(len(edge) == 0, "SF3: calls inside six hours of a year edge")
    # SF4: no column records who answered a machine-classed call
    ok(set(calls["amd"].unique()) <= {"MACHINE", "LIVE"}, "SF4: a detector value other than MACHINE or LIVE")
    # SF6: the latest outbound call is the only one to that number in the four hours before the return
    out = calls[["phone", "placed"]].sort_values("placed")
    cnt = 0
    grp = out.groupby("phone")["placed"].apply(np.array).to_dict()
    for ph, st in zip(r20["phone"], r20["started"]):
        a = grp[ph]
        cnt += int(((a <= np.datetime64(st)) & (a > np.datetime64(st - pd.Timedelta(hours=4)))).sum() != 1)
    note("SF6 returns with two outbound calls in the four hours before: %d" % cnt)
    alt = r20.copy()
    day = calls.assign(day=calls["placed"].dt.normalize()).sort_values("placed").drop_duplicates(["phone", "day"])
    first = dict(zip(zip(day["phone"], day["day"]), zip(day["outcome"], day["job"], day["placed"])))
    pick = [first.get((ph, st.normalize())) for ph, st in zip(alt["phone"], alt["started"])]
    alt["outcome"] = [p[0] if p and p[2] <= st else o for p, o, st in zip(pick, alt["outcome"], alt["started"])]
    alt["delay_min"] = 0.0
    m6 = S_.main_call(calls, inbound, jobs, ret=alt).set_index("job")
    ok(sorted(m6.index[m6["off"]]) == gold, "SF6: the day's first call moves the call")
    ok(((m6["share"] * 100).apply(lambda x: int(np.floor(x + 0.5))) == (share * 100).apply(lambda x: int(np.floor(x + 0.5)))).all(),
       "SF6: the day's first call moves a share")
    # SF7: the corridor, 5 to 40 minutes
    base = (share * 100).apply(lambda x: int(np.floor(x + 0.5)))
    for w in (5, 10, 15, 20, 30, 40):
        mw = S_.main_call(calls, inbound, jobs, window_min=w, ret=ret).set_index("job")
        ok(((mw["share"] * 100).apply(lambda x: int(np.floor(x + 0.5))) == base).all(), "SF7: window %d moves a share" % w)
        ok(sorted(mw.index[mw["off"]]) == gold, "SF7: window %d moves the call" % w)
    # SF8: one return per leg
    legs = inbound[inbound["phone"].ne("")].sort_values("started")
    ml = pd.merge_asof(legs, calls[["call_id", "job", "phone", "ended", "outcome"]].sort_values("ended"),
                       left_on="started", right_on="ended", by="phone", direction="backward")
    ml = ml[ml["call_id"].notna()]
    ml["delay_min"] = (ml["started"] - ml["ended"]).dt.total_seconds() / 60.0
    ml["leg"] = "1"
    mleg = S_.main_call(calls, inbound, jobs, ret=ml).set_index("job")
    ok(sorted(mleg.index[mleg["off"]]) == gold, "SF8: counting legs moves the call")
    note("SF8 per-leg shares %s" % (mleg["share"] * 100).round(1).tolist())
    # SF9: the test calls never match a dialed number
    tests = inbound[inbound["wrap_code"].eq("TEST")]
    ok(len(tests) > 0 and (tests["phone"] == "").all(), "SF9: a test call carries a dialed number")
    # SF11: the one-off study is in the exports, not on the register
    ok(P.ONE_OFF[0] in set(calls["job"]) and P.ONE_OFF[0] not in jobs and len(jobs) == len(P.PROJECTS),
       "SF11: the register's projects")
    # SF12: returns landing in January 2027 are counted, and dropping them does not move the call
    jan = ret[(ret["started"] >= pd.Timestamp("2027-01-01")) & (ret["delay_min"] <= 20)]
    ok(len(jan) == 0, "SF12: a return inside the window crosses the year edge")
    ok(len(ret[ret["started"] >= pd.Timestamp("2027-01-01")]) > 0, "SF12: the log holds no January calls")
    mj = S_.main_call(calls, inbound, jobs, ret=ret[ret["started"] < pd.Timestamp("2027-01-01")]).set_index("job")
    ok(sorted(mj.index[mj["off"]]) == gold, "SF12: dropping January returns moves the call")
    # SF13: the share from counts, rounded once, clear of a rounding edge; monthly averaging gives the same call
    frac = (share * 100) - np.floor(share * 100)
    ok(((frac - 0.5).abs() >= EDGE).all(), "SF13: a share within %.2f of a rounding edge" % EDGE)
    note("SF13 nearest rounding edge %.3f points" % (frac - 0.5).abs().min())
    rr = (m["r_am"] / m["n_am"]).round(2) / (m["r_ab"] / m["n_ab"]).round(2)
    ok(sorted(rr.index[rr >= P.LIMIT]) == gold, "SF13: rounding each rate first moves the call")
    # row order
    sh = calls.sample(frac=1.0, random_state=1)
    ms = S_.main_call(sh, inbound.sample(frac=1.0, random_state=2), jobs).set_index("job")
    ok(np.allclose(ms["share"].reindex(jobs).values, share.reindex(jobs).values), "axis 14: row order moves a share")

    # ---- the ladder ----------------------------------------------------------------------------------------------
    # rungs 0 and 1: the dispositions at face value and the certified rate carried to every project
    ok(m["off"].sum() > 0 and (P.CERTIFIED < P.LIMIT), "rung 1")
    msh = S_.machine_share(calls, jobs)
    live = 1 - msh
    bayes = P.CERTIFIED * live / (P.CERTIFIED * live + (1 - 0.065) * msh)
    ok((bayes < P.LIMIT).all(), "rung 1: the certified rate taken through each project's mix flags a project")
    ok(9 / 400 < P.LIMIT, "rung 1: the listening audit")
    order = list(msh.sort_values(ascending=False).index)
    top4 = sorted(order[:4])
    ok(top4 == sorted(["KR-2613", "KR-2612", "KR-2620", "KR-2622"]), "rung 2: the top four by machine share are %s" % top4)
    ok(100 * (msh[order[3]] - msh[order[4]]) >= 1.0, "rung 2: the fourth and fifth machine shares within a point")
    ok(len(set(top4) & set(gold)) == 2, "rung 2: two right")
    for j in ("KR-2613", "KR-2622"):          # the note: higher machine-classed shares than most of the six
        ok(int((msh[j] > msh[gold]).sum()) >= 4, "note: %s is not above most of the six on machine share" % j)
    any_d = S_.main_call(calls, inbound, jobs, any_delay=True, ret=ret)
    ok(any_d["off"].all(), "rung 3: returns at any delay do not flag every project")
    pooled = S_.main_call(calls, inbound, jobs, pooled=True, ret=ret).set_index("job")
    pset = sorted(pooled.index[pooled["off"]])
    ok(len(pset) == 5 and set(pset) < set(gold), "rung 4: the pooled denominator flags %s" % pset)
    miss = (set(gold) - set(pset)).pop()
    ok(pooled.loc[miss, "share"] <= P.LIMIT - 0.02, "rung 4: the project it drops sits within two points")
    note("rung 4 drops %s at %.2f; rung 2 gap %.2f points" % (miss, 100 * pooled.loc[miss, "share"],
                                                              100 * (msh[order[3]] - msh[order[4]])))
    # the shock line: the golden set is no interval of any shipped per-project statistic
    g = calls[calls["job"].isin(jobs)]
    answered = g.groupby("job").size().reindex(jobs)
    stats = {"machine share": msh, "abandoned rate": m["n_ab"] / answered,
             "machine-classed returned": m["r_am"] / m["n_am"], "abandoned returned": m["r_ab"] / m["n_ab"],
             "completion rate": S["askB"] / answered, "answered calls": answered,
             "line volume": inbound[inbound["leg"] == "1"].groupby(inbound["dialed_line"].map(lines)).size().reindex(jobs),
             "cases": cases.groupby("job").size().reindex(jobs), "hours": S["askC"]}
    for name, st in stats.items():
        ok(not interval(list(st.sort_values().index), gold), "shock: the golden set is an interval of " + name)
    # Gate F on the clean truth: the analyst test and the cheap routes
    tc = W["calls"]
    tr = tc[tc["outcome"].eq("AMD_MACHINE") & tc["job"].isin(jobs)]
    truth = tr.groupby("job")["is_machine"].apply(lambda x: (~x).mean()).reindex(jobs)
    ok(sorted(truth.index[truth >= P.LIMIT]) == gold, "the clean truth's set differs from the golden")
    ok(((truth >= P.LIMIT) == m["off"].reindex(jobs)).all() and (truth - P.LIMIT).abs().min() >= 0.02,
       "the clean truth sits near the limit")
    note("clean truth %s" % (truth * 100).round(1).tolist())
    note("estimate    %s" % (share.reindex(jobs) * 100).round(1).tolist())
    se = np.sqrt(share * (1 - share) / m["r_am"].clip(lower=1) + share ** 2 / m["r_ab"])   # delta method, rough
    ok(((truth - share.reindex(jobs)).abs() <= 3 * se.reindex(jobs)).all(), "the estimate strays from the clean truth")
    cheap = {"certified": set(), "listening": set(), "top4": set(top4), "any delay": set(any_d.loc[any_d["off"], "job"]),
             "pooled": set(pset)}
    landed = [k for k, v in cheap.items() if v == set(gold)]
    ok(not landed, "Gate F: a cheap route lands the call: %s" % landed)
    # oracles: the pilot inside the 2025 audit's interval
    from scipy.stats import beta
    lo, hi = beta.ppf(0.025, 9, 392), beta.ppf(0.975, 10, 391)
    ok(lo <= share[P.PILOT_JOB] <= hi, "oracle: the pilot's 2026 share %.3f outside the audit's %.3f to %.3f"
       % (share[P.PILOT_JOB], lo, hi))
    note("pilot %.2f inside the audit interval %.2f to %.2f" % (100 * share[P.PILOT_JOB], 100 * lo, 100 * hi))

    # ---- the separation line: no ask device on the main population ------------------------------------------------
    in_case = calls["phone"].isin(set(cases["phone"]))
    ok(not calls.loc[~in_case, "outcome"].isin(["AMD_MACHINE", "ABANDONED"]).any(),
       "separation: an appointment number carries a machine-classed or abandoned call")
    ok(not calls.loc[calls["agent"].eq("SUP1"), "outcome"].isin(["AMD_MACHINE", "ABANDONED"]).any(),
       "separation: a verification call is machine-classed or abandoned")
    icomp = S_.inbound_calls(inbound)
    icomp = icomp[icomp["complete"]]
    ok(not icomp["switch_call_id"].isin(set(r20["switch_call_id"])).any(), "separation: an inbound interview is a return")
    lean = calls[in_case & calls["agent"].ne("SUP1")]
    ml2 = S_.main_call(lean, inbound[~inbound["switch_call_id"].isin(set(icomp["switch_call_id"]))], jobs).set_index("job")
    ok(np.allclose(ml2["share"].values, share.values), "separation: deleting the ask devices moves a share")

    # ---- ask A: calling hours ------------------------------------------------------------------------------------
    rows = W["rows"]
    rows = rows[rows["job"].isin(jobs)]
    lh = local_hours(rows["placed"].values, rows["state"].values, zones)
    tA = pd.Series((lh < 8) | (lh >= 21), index=rows.index).groupby(rows["job"]).sum().reindex(jobs).astype(int)
    ok((tA.values == S["askA"].values).all(), "ask A: the golden differs from the truth")
    on_edge = ((np.abs(lh - 8) < 1e-9) | (np.abs(lh - 21) < 1e-9)).sum()
    ok(on_edge == 0, "ask A: %d calls ring exactly on 8:00 or 21:00" % on_edge)
    routes = {"cracker": S_.calling_hours(calls, cases, zones, jobs, route="cracker"),
              "mirror": S_.calling_hours(calls, cases, zones, jobs, route="mirror", arizona_dst=True),
              "area code": calling_hours_area(calls, zones, jobs),
              "phone only, unmatched dropped": calling_hours_drop(calls, cases, zones, jobs),
              "Arizona on daylight time": S_.calling_hours(calls, cases, zones, jobs, arizona_dst=True)}
    for k, v in routes.items():
        hits = int((v.values == S["askA"].values).sum())
        note("ask A %s keeps %d of 13" % (k, hits))
    ok((routes["cracker"].values != S["askA"].values).all(), "ask A: the careful route hits a figure")
    ok((routes["mirror"].values != S["askA"].values).sum() >= 11, "ask A: the mirror keeps more than two")

    # ---- ask B: completed interviews ----------------------------------------------------------------------------
    done = set(zip(tc.loc[tc["outcome"].eq("COMPLETE"), "job"], tc.loc[tc["outcome"].eq("COMPLETE"), "case_new"]))
    ti = W["inbound"]
    ti = ti[ti["kind"].eq("complete") & (ti["started"] < pd.Timestamp("2027-01-01"))]
    done |= set(zip(ti["job"], ti["case_new"]))
    tB = pd.Series([j for j, _ in done]).value_counts().reindex(jobs).fillna(0).astype(int)
    ok((tB.values == S["askB"].values).all(), "ask B: the golden differs from the truth")
    inv = invoices(target)
    rB = {"cracker": S_.completes(calls, inbound, reg, cases, jobs, route="cracker"),
          "invoiced": S_.completes(calls, inbound, reg, cases, jobs, route="invoiced")}
    ok((inv.reindex(jobs).values == rB["invoiced"].values).all(), "ask B: the invoices do not tie to the dialer's rows")
    for k, v in rB.items():
        note("ask B %s keeps %d of 13, misses by %d to %d" % (k, int((v.values == S["askB"].values).sum()),
                                                              int((v - S["askB"]).abs().min()), int((v - S["askB"]).abs().max())))
    ok(((rB["cracker"] - S["askB"]).abs() >= 5).all(), "ask B: the careful route within five of a figure")
    ok(((rB["invoiced"] - S["askB"]).abs() >= 5).all(), "ask B: the invoiced count within five of a figure")

    # ---- ask C: interviewer hours -------------------------------------------------------------------------------
    sh_ = W["shifts"].set_index("shift")
    cc = tc[(tc["shift"] >= 0)]
    sec = (cc["talk"] + cc["wrap"]).groupby([cc["shift"], cc["job"]]).sum().rename("sec").reset_index()
    sec["share"] = sec["sec"] / sec.groupby("shift")["sec"].transform("sum")
    sec["h"] = sec["shift"].map(sh_["hours"]) * sec["share"]
    tC = sec.groupby("job")["h"].sum().reindex(jobs).fillna(0)
    ok(np.allclose(tC.values, S["askC"].values, atol=1e-6), "ask C: the golden differs from the truth")
    frac = (S["askC"] * 10) - np.floor(S["askC"] * 10)
    ok(((frac - 0.5).abs() >= 0.01).all(), "ask C: an hours figure on a rounding edge")
    ts_dec = S_.load_hours(target, hhmm=False)
    rC = {"cracker": S_.hours(calls, ts_dec, jobs), "mirror": S_.hours(calls, ts_dec, jobs, route="by_code"),
          "by code, hours read right": S_.hours(calls, S["ts"], jobs, route="by_code"),
          "training charged": hours_with_training(calls, S["ts"], jobs)}
    for k, v in rC.items():
        d = (v.round(1) - S["askC"].round(1)).abs()
        note("ask C %s keeps %d of 13, misses by %.1f to %.1f" % (k, int((d < 0.05).sum()), d.min(), d.max()))
    ok(((rC["cracker"].round(1) - S["askC"].round(1)).abs() >= 1).all(), "ask C: the careful route within an hour")
    ok(((rC["mirror"].round(1) - S["askC"].round(1)).abs() >= 0.05).all(), "ask C: the mirror hits a figure")
    ok(len(W["training"]) > 0, "ask C: no training shifts")
    ok(not W["shifts"].duplicated(["agent", "date", "period"]).any(), "ask C: an interviewer on two shifts at once")

    # ---- the goldens carry the figures ----------------------------------------------------------------------------
    wb = load_workbook(os.path.join(golden_dir, "amd_review_2027.xlsx"), data_only=False)
    ws = wb["2027 setup"]
    got = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=17, values_only=True)}
    for r in A["rows"]:
        x = got[r["job"]]
        ok(abs(x[6] - r["pct"] / 100.0) < 1e-9 and (x[7] == "Off") == r["off"] and x[8] == r["outside"]
           and x[9] == r["completes"] and abs(x[10] - r["hours"]) < 1e-9, "golden workbook row " + r["job"])

    # ---- input gates ----------------------------------------------------------------------------------------------
    files = [p for p in glob.glob(os.path.join(target, "**", "*"), recursive=True) if os.path.isfile(p)]
    ok(len(files) >= 10, "input gate: fewer than ten files")
    ok(len({os.path.splitext(p)[1] for p in files}) >= 3, "input gate: fewer than three formats")
    big = max(sum(1 for _ in open(p, encoding="utf-8")) for p in files if p.endswith(".csv"))
    ok(big >= 25000, "input gate: no file of 25,000 rows")
    for f in ("mobile_consent_log_2026.csv", "qa_monitoring_scores_2026.csv"):
        ok(os.path.exists(os.path.join(target, f)), "input gate: distractor missing " + f)
    for p in files:
        if p.endswith((".csv",)):
            ok("—" not in open(p, encoding="utf-8").read(), "an em dash in " + p)
    return N[0]


def calling_hours_area(calls, zones, jobs):
    g = calls[calls["job"].isin(jobs)]
    lh = local_hours(g["placed"].values, g["phone"].str[:3].map(S_.AREA_STATE).values, zones)
    return pd.Series((lh < 8) | (lh >= 21), index=g.index).groupby(g["job"]).sum().reindex(jobs).astype(int)


def calling_hours_drop(calls, cases, zones, jobs):
    g = calls[calls["job"].isin(jobs)]
    st = g["phone"].map(dict(zip(cases["phone"], cases["address_state"])))
    lh = local_hours(g["placed"].values, st.values, zones)
    return pd.Series((lh < 8) | (lh >= 21), index=g.index).groupby(g["job"]).sum().reindex(jobs).astype(int)


def hours_with_training(calls, ts, jobs):
    """the allocated hours with the training shifts charged to the project code they were booked to"""
    base = S_.hours(calls, ts, jobs)
    tr = ts[ts["start"] == "13:30"]
    return base.add(tr.groupby("project")["h"].sum().reindex(jobs).fillna(0), fill_value=0)


def invoices(target):
    wb = load_workbook(os.path.join(target, "client_invoices_2026.xlsx"), data_only=True)
    ws = wb.active
    out = {}
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0] and str(r[0]).startswith("KR-"):
            out[r[0]] = r[5]
    return pd.Series(out)
