"""Assertions over the built pack: the literal reading, the ladder by name, the back-test (every basis's
largest miss and the winner's margin, also under every combination of mishandled ask devices), the golden's
own variants, truth, bins, the separation zero-counts, the ask devices and their stops, the bridge, the top
holders and the input gates. Every check counts; the run fails on the first miss."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import golden as G
import world as W

N = [0]
LOG = {}


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def wd_types(wd):
    return {m["cik"]: m["type"] for m in wd.mgrs}


def run(wd, g, target, golden_dir, meta):
    cus = g["cusips"]
    ids = {c: f"W{k + 1:02d}" for k, c in enumerate(cus)}
    flags = lambda d: {ids[c] for c in cus if d[c] > 80.0}
    S4, S3 = g["S_dec"], g["S_sep"]
    ANS = {"W01", "W02", "W03", "W06", "W10"}

    # ---- the literal reading of OM-4 s.2 is the golden: managers due = September holdings or combination
    #      filers with no December filing of any kind; estimate by the basis the filed criterion selects
    ok(flags(g["dec_io"]) == ANS, f"answer {flags(g['dec_io'])}")
    bt = g["backtest"]
    GOLD = "sponsors_per_name"
    variants = ("sponsors_per_name", "sponsors_per_name_flat", "sponsors_stake")
    rivals = [k for k in bt if k not in variants]
    best = min(bt, key=bt.get)
    ok(best in variants, f"the criterion selects {best}")
    for v in variants:
        ok(bt[v] <= 0.15, f"variant {v} back-test {bt[v]:.3f}")
    rmin = min(bt[k] for k in rivals)
    ok(rmin - bt[GOLD] >= 0.4 and rmin >= 3 * bt[GOLD], f"criterion margin {rmin:.3f}")
    TARGET = {"stake_type_pooled_all": 0.6, "all_pooled": 0.6, "stake_sponsors": 0.9, "stake_all": 0.9,
              "one_rate": 0.6, "one_rate_per_name": 0.6, "type_mean_ratio": 0.6, "flat": 0.9, "all_per_name": 1.5,
              "issuer_factor": 1.5, "last_quarter": 3.0, "type_per_name": 1.5, "value_share": 8.0,
              "filer_share": 15.0, "onfile": 15.0}
    POOLED = ("type_pooled", "type_allsec", "sponsors_only")      # R4', the stump rung's family
    ok(set(TARGET) | set(POOLED) == set(rivals), f"rival list {sorted(rivals)}")
    for k, t in TARGET.items():
        ok(bt[k] >= t, f"rival {k} back-test {bt[k]:.3f} under {t}")
    for k in POOLED:
        ok(0.5 <= bt[k] <= 0.9, f"stump rung {k} back-test {bt[k]:.3f}")
        ok(min(bt[x] for x in TARGET) - bt[k] >= 0.05, f"stump rung {k} not below every other rival")
    five = ("onfile", "flat", "all_pooled", "all_per_name", "type_pooled")      # the default path's five
    ok(min(bt[x] for x in five if x != "type_pooled") - bt["type_pooled"] >= 0.15, "type-pooled not first of the five")
    LOG["backtest"] = {k: round(v, 3) for k, v in bt.items()}

    # ---- the ladder, every rung by name
    R = g["rungs"]
    R4 = {"W01", "W02", "W06", "W10"}
    expect = {"onfile": {"W01", "W06"}, "R1_last_quarter": {"W01", "W02", "W06", "W07", "W10"},
              "R3_value_share": {"W01", "W04", "W05", "W06", "W10"},
              "R2_filer_share": {"W01", "W02", "W03", "W04", "W05", "W06", "W07", "W09", "W10", "W12"},
              "flat": R4, "all_pooled": R4, "all_per_name": R4, "issuer_factor": R4, "stake_sponsors": R4,
              "type_pooled": R4, "type_allsec": R4, "sponsors_only": R4, "own_trend": R4,
              "one_rate": R4 | {"W07"}, "stake_all": R4 | {"W07"}, "type_mean_ratio": R4 | {"W07"},
              "one_rate_per_name": ANS | {"W07"}, "stake_type_pooled_all": ANS | {"W07"},
              "type_per_name": ANS | {"W07"}}
    ok(set(expect) == set(R), f"rung list {sorted(set(R) ^ set(expect))}")
    for k, v in expect.items():
        ok(flags(R[k]) == v, f"rung {k} flags {sorted(flags(R[k]))}")
        ok(flags(R[k]) != ANS, f"rung {k} lands the answer")
    W03, W07 = cus[2], cus[6]
    ok(R["type_pooled"][W03] <= 79.6, f"type-pooled OTF {R['type_pooled'][W03]:.2f}")
    for k in ("flat", "all_pooled", "all_per_name", "issuer_factor", "stake_sponsors", "type_allsec", "sponsors_only"):
        ok(R[k][W03] <= 79.7, f"{k} OTF {R[k][W03]:.2f}")
    for k in ("one_rate", "stake_all"):
        ok(R[k][W07] >= 80.1, f"R4b {k} FENN {R[k][W07]:.2f}")
    for k in ("one_rate_per_name", "stake_type_pooled_all", "type_per_name"):
        ok(R[k][W07] >= 80.2, f"R4c {k} FENN {R[k][W07]:.2f}")
    # the 24-cell grid: the sponsors' factor against every other type's, each cell's flags by name
    GRID = {}
    for a in G.GRID_SP:
        for b_ in G.GRID_OT:
            if a == "per_name":
                GRID[(a, b_)] = ANS if b_ in ("flat", "own_pooled") else ANS | {"W07"}
            elif b_ in ("flat", "own_pooled"):
                GRID[(a, b_)] = R4
            elif b_ == "own_per_name" and a != "none":
                GRID[(a, b_)] = ANS | {"W07"}
            else:
                GRID[(a, b_)] = R4 | {"W07"}
    for k, v in GRID.items():
        ok(flags(g["grid"][k]) == v, f"grid {k} flags {sorted(flags(g['grid'][k]))}")
    ok(sum(flags(g["grid"][k]) == ANS for k in GRID) == 2, "grid cells landing the answer")
    ok(all(abs(g["grid"][("per_name", "own_pooled")][c] - g["dec_io"][c]) < 1e-9 for c in cus), "grid golden cell")
    LOG["grid"] = {f"{a}|{b_}": dict(OTF=round(g["grid"][(a, b_)][W03], 2), FENN=round(g["grid"][(a, b_)][W07], 2))
                   for a, b_ in GRID}
    # no single rate for every manager still due gives the answer: FENN crosses well below OTF's crossing rate
    on, due = g["dec_onfile_shares"], {c: sum(v for (k, cc), v in g["_due_by"].items() if cc == c) for c in cus}
    cross = {c: (0.8 * S4[c] - on[c]) / due[c] - 1 for c in cus}
    ok(cross[W03] - cross[W07] >= 0.03, f"crossing rates OTF {cross[W03]:.4f} FENN {cross[W07]:.4f}")
    for r_ in np.arange(0.0, 0.20001, 0.0005):
        st = {ids[c] for c in cus if 100 * (on[c] + due[c] * (1 + r_)) / S4[c] > 80}
        ok(st != ANS, f"one rate {r_:.4f} lands the answer")
    LOG["cross"] = {"OTF": round(100 * cross[W03], 2), "FENN": round(100 * cross[W07], 2)}

    # ---- the golden's own variants converge on every flag and graded figure
    P4 = g["_P4"]
    VARS = dict(g["dec_variants"])
    filed_sp = [k for k in P4["both"] if wd_types(wd).get(k) == "passive"]
    ok(len(filed_sp) == 2, f"filed sponsor complexes {filed_sp}")
    # SF11: each filed complex alone gives the same per-name change (within 0.0005) and the same figures
    f0, inf0 = g["_frames"]["f"], g["_frames"]["inf"]
    hn = G.holdings(f0, inf0, G.PERIOD["Q4"], cut=G.EXTRACT, cusips=cus)
    hp = G.holdings(f0, inf0, G.PERIOD["Q3"], cusips=cus)
    due_sp = {c: P4["due_t"].get((G.PASSIVE, c), 0.0) for c in cus}
    for k in filed_sp:
        rn = (hn[hn.CIK == k].groupby("cusip9").SSHPRNAMT.sum() / hp[hp.CIK == k].groupby("cusip9").SSHPRNAMT.sum())
        alone = {}
        for c in cus:
            ok(abs(rn[c] - g["sponsor_change_name"][c]) <= 0.0005, f"complex {k} alone {ids[c]} {rn[c]:.5f}")
            alone[c] = g["dec_io"][c] + 100 * due_sp[c] * (rn[c] - g["sponsor_change_name"][c]) / S4[c]
        VARS[f"complex_{k}"] = alone
    # SF7 and SF11: the sponsors' stake change pooled over every covered security (the simulation's counts)
    sims = {}
    for qa, qb, Sa, Sb in (("Q4", "Q3", "S_oct", "S_sep"), ("Q3", "Q2", "S_sep", "S_apr")):
        num = den = 0.0
        for (mid, iid), v in wd.pos[qa].items():
            if mid in (wd.roles["P0"], wd.roles["P1"]):
                num += v / wd.I[iid][Sa]
        for (mid, iid), v in wd.pos[qb].items():
            if mid in (wd.roles["P0"], wd.roles["P1"]):
                den += v / wd.I[iid][Sb]
        sims[qa] = num / den
        ok(abs(sims[qa] - W.GROW) <= 0.0005, f"stake change over every security {qa} {sims[qa]:.5f}")
    ok(abs(g["sponsor_stake_change"] - W.GROW) <= 0.0005, f"stake change over the twelve {g['sponsor_stake_change']:.5f}")
    on4 = g["dec_onfile_shares"]
    VARS["sponsors_stake_allsec"] = {
        c: 100 * (on4[c] + due_sp[c] * sims["Q4"] * S4[c] / S3[c]
                  + sum(v for (t, cc), v in P4["due_t"].items() if cc == c and t != G.PASSIVE)) / S4[c] for c in cus}
    # sponsor dynamics: the filed sponsors' per-name share change is the stake growth times the name's count move
    for key, Sa, Sb in (("Q4", S4, S3), ("Q3", S3, g["S_jun"])):
        rn = g["sponsor_change_name"] if key == "Q4" else {c: g["bt_P3"]["rt_name"][(G.PASSIVE, c)] for c in cus}
        for c in cus:
            ok(abs(rn[c] - W.GROW * Sa[c] / Sb[c]) <= 0.0005, f"sponsor change {key} {ids[c]} {rn[c]:.5f}")
    LOG["sponsors"] = dict(stake_change_twelve=round(g["sponsor_stake_change"], 5),
                           stake_change_allsec={k: round(v, 5) for k, v in sims.items()},
                           pooled_share_change=dict(dec=round(g["type_change"][G.PASSIVE], 4),
                                                    sep=round(g["type_change3"][G.PASSIVE], 4)),
                           per_name_dec={ids[c]: round(g["sponsor_change_name"][c], 4) for c in cus})
    for k, v in VARS.items():  # SF10, SF11, SF7
        for c in cus:
            ok(abs(v[c] - g["dec_io"][c]) <= 0.01, f"variant {k} {ids[c]} {v[c]:.3f}")
            ok(round(v[c], 1) == round(g["dec_io"][c], 1), f"variant {k} {ids[c]} bin")
        ok(flags(v) == ANS, f"variant {k} flags")
    # type changes: every other type flat in aggregate (never exactly 1), both windows
    for key in ("type_change", "type_change_allsec", "type_change3"):
        for t, v in g[key].items():
            if t != G.PASSIVE:
                ok(0.998 <= v <= 1.002 and abs(v - 1) > 5e-5, f"{key} {t} {v}")

    # ---- bins: every graded figure at least 0.015 inside its one-decimal bin under every golden variant
    def inside(v):
        b = round(v, 1)
        return min(v - (b - 0.05), (b + 0.05) - v)
    for c in cus:
        for v in [g["dec_io"][c]] + [x[c] for x in VARS.values()]:
            ok(inside(v) >= 0.015, f"{ids[c]} December {v:.4f} near a bin edge")
        ok(inside(g["sep_io"][c]) >= 0.015, f"{ids[c]} September {g['sep_io'][c]:.4f} near a bin edge")
        ok(round(g["sep_io"][c], 1) % 1 != 0, f"{ids[c]} September lands on a whole per cent")
    for c in (W03, W07):
        for v in [g["dec_io"][c]] + [x[c] for x in VARS.values()]:
            ok(abs(v - 80.0) >= 0.3, f"{ids[c]} within 0.3 of the line: {v:.3f}")  # SF4

    # ---- truth: the simulation's December holdings give the same flags, within 0.15
    tru = {}
    for i in wd.iss:
        if i["watch"]:
            tru[i["cusip"]] = 100 * sum(v for (mid, iid), v in wd.pos["Q4"].items() if iid == i["iid"]) / i["S_oct"]
    for c in cus:
        ok((tru[c] > 80) == g["flag"][c], f"truth flag {ids[c]}")
        ok(abs(tru[c] - g["dec_io"][c]) < 0.15, f"truth {ids[c]} {tru[c]:.3f}")

    # ---- the population: no attrition, nobody due is a non-reporter, notice filers outside
    f, inf = G.load(target)
    wl = G.watch_table(target)
    inf["cusip9"], inf["fix"] = G.normalise_cusips(inf, wl)
    reg = G.register(target)
    mtype = dict(zip(reg.cik, reg.manager_type))
    P = G.PERIOD
    ciks = {q: set(f[f.period == P[q]].CIK) for q in P}
    hold = {q: set(f[(f.period == P[q]) & (f.REPORTTYPE != "13F NOTICE")].CIK) for q in P}
    ok(hold["Q2"] <= hold["Q3"], "a June filer without a September report")
    inactive = set(reg[reg.status == "inactive"].cik)
    ok(len(inactive) > 0 and not (inactive & set(f.CIK)), "inactive register rows file")
    due = set(g["due_ciks"])
    ok(due == hold["Q3"] - set(f[(f.period == P["Q4"]) & (f.fdate <= G.EXTRACT)].CIK), "due set")
    sep_notice_out = (ciks["Q3"] - hold["Q3"]) - ciks["Q4"]
    ok(len(sep_notice_out) >= 1 and not (sep_notice_out & due), "September notice filers with nothing for December")  # SF1
    ok(all(mtype[k] not in ("Bank trust and wealth department", "Broker-dealer") for k in due), "a bank trust or dealer is due")
    LOG["counts"] = dict(due=len(due), onfile=g["n_reporting_onfile"], sep_notice_out=len(sep_notice_out),
                         sep_any_no_dec=len(ciks["Q3"] - set(f[(f.period == P["Q4"]) & (f.fdate <= G.EXTRACT)].CIK)))
    ok(LOG["counts"]["sep_any_no_dec"] == len(due) + len(sep_notice_out), "count reconciliation")
    due3 = hold["Q2"] - set(f[(f.period == P["Q3"]) & (f.fdate <= G.CUT["Q3"])].CIK)
    ok(all(mtype[k] not in ("Bank trust and wealth department", "Broker-dealer") for k in due3), "bank trust due in September")
    ok(not (due3 ^ due), "the same managers are still due in both windows")  # SF5

    # ---- separation: zero device rows and zero hazard rows in the main call's declared population
    def bad(e):
        return int(((e.CUSIP != e.cusip9) | (e.fix != "") | (e.TITLEOFCLASS != "COM")).sum())
    q4acc = f[(f.period == P["Q4"]) & (f.fdate <= G.EXTRACT)]
    e4 = inf[inf.ACCESSION_NUMBER.isin(set(q4acc.ACCESSION_NUMBER)) & inf.cusip9.isin(cus) & (inf.PUTCALL == "")]
    z = {}
    z["dec_twelve_device_rows"] = bad(e4)
    z["dec_amendments"] = int((q4acc.ISAMENDMENT == "Y").sum() + q4acc.CIK.duplicated().sum())  # SF6
    z["dec_title_options"] = int(inf[inf.ACCESSION_NUMBER.isin(set(q4acc.ACCESSION_NUMBER)) & (inf.PUTCALL == "")
                                     & inf.TITLEOFCLASS.isin(["CALL", "PUT"])].shape[0])
    p3f = f[(f.period == P["Q3"]) & f.CIK.isin(due)]
    z["due_sep_amendments"] = int((p3f.ISAMENDMENT == "Y").sum() + p3f.CIK.duplicated().sum())
    l3due = inf[inf.ACCESSION_NUMBER.isin(set(p3f.ACCESSION_NUMBER)) & inf.cusip9.isin(cus)]
    z["due_sep_device_rows"] = bad(l3due) + int((l3due.PUTCALL != "").sum())
    types_due = {mtype[k] for k in due}
    ok(G.PASSIVE in types_due, "sponsors due")
    peers = {k for k in (hold["Q3"] | hold["Q4"]) if mtype[k] in types_due}
    pf = f[f.period.isin([P["Q2"], P["Q3"], P["Q4"]]) & f.CIK.isin(peers)]
    lp = inf[inf.ACCESSION_NUMBER.isin(set(pf.ACCESSION_NUMBER))]
    z["peer_amendments"] = int((pf.ISAMENDMENT == "Y").sum())
    z["peer_device_rows"] = int(((lp.CUSIP.str.upper().str.zfill(9) != lp.CUSIP) | (lp.fix != "") | (lp.TITLEOFCLASS != "COM")).sum())
    z["peer_option_rows"] = int((lp.PUTCALL != "").sum() + lp.TITLEOFCLASS.isin(["CALL", "PUT"]).sum())
    for k, v in z.items():
        ok(v == 0, f"separation: {k} = {v}")
    hosts = set(g["device_hosts"])
    ok(len(hosts) >= 9, f"device hosts {len(hosts)}")
    late_opt_only = 0
    for k in hosts:
        ok(mtype[k] == "Bank trust and wealth department", f"device host {k} is {mtype[k]}")
        q3 = f[(f.period == P["Q3"]) & (f.CIK == k)]
        for a in q3[q3.fdate > G.CUT["Q3"]].ACCESSION_NUMBER:     # DV-3: filed in January, option lines only
            la = inf[inf.ACCESSION_NUMBER == a]
            ok(len(la) > 0 and (la.PUTCALL != "").all(), f"device host {k} files share lines after 3 November")
            late_opt_only += 1
    ok(late_opt_only == 1, f"September filings after the cut {late_opt_only}")
    # every amendment and every same-day pair sits outside the declared population, under either period reading
    amend_acc = set(f[f.ISAMENDMENT == "Y"].ACCESSION_NUMBER)
    declared_acc = set(q4acc.ACCESSION_NUMBER) | set(p3f.ACCESSION_NUMBER) | set(pf.ACCESSION_NUMBER)
    fsub = G.sub_period(f)
    p3h = fsub[(fsub.period == P["Q3"]) & fsub.CIK.isin(due)]
    declared_acc |= set(p3h.ACCESSION_NUMBER)
    z2 = {"amendments_in_population": len(amend_acc & declared_acc),
          "header_period_disagreements_in_population": int((f[f.ACCESSION_NUMBER.isin(declared_acc)].PERIODOFREPORT
                                                            != f[f.ACCESSION_NUMBER.isin(declared_acc)].REPORTCALENDARORQUARTER).sum())}
    for k, v in z2.items():
        ok(v == 0, f"separation: {k} = {v}")
    z.update(z2)
    rows_dev = inf[inf.ACCESSION_NUMBER.isin(set(f[f.period == P["Q3"]].ACCESSION_NUMBER))]
    rows_dev = rows_dev[((rows_dev.fix != "") | (rows_dev.TITLEOFCLASS != "COM")) & rows_dev.cusip9.isin(cus)]
    LOG["separation"] = dict(z, device_rows_sep=int(len(rows_dev)), device_hosts=len(hosts),
                             declared_dec_rows=int(len(e4)), declared_due_sep_rows=int(len(l3due)), peer_rows=int(len(lp)))

    # ---- hazards on the main call: options, the January count, a December 10-Q/A
    so = {k: v for k, v in g["so"].items()}
    # SF9: the stake formulation read against the October-dated count as the September count moves OTF under the
    # line (refused by OM-4 s.5); read against the original 10-Q count for the three A5 names it keeps every flag
    Soct = {c: so[f"{c}|Q3_after"] for c in cus}
    alt = P4["bases"](S4, Soct)["sponsors_stake"]
    alt = {c: 100 * alt[c] / S4[c] for c in cus}
    ok(alt[W03] < 80.0 and flags(alt) == ANS - {"W03"}, f"SF9 October count {alt[W03]:.2f} {sorted(flags(alt))}")
    S10 = {c: (so[f"{c}|Q3_10q"] if ids[c] in W.A5_NAMES else S3[c]) for c in cus}
    alt2 = P4["bases"](S4, S10)["sponsors_stake"]
    alt2 = {c: 100 * alt2[c] / S4[c] for c in cus}
    ok(flags(alt2) == ANS, "SF9 the 10-Q count")
    LOG["sf9"] = dict(oct_OTF=round(alt[W03], 2), q10_max=round(max(abs(alt2[c] - g["dec_io"][c]) for c in cus), 3))
    for c in cus:
        ok(so[f"{c}|n_q3_amend"] == 0, f"a 10-Q/A for the September quarter on {ids[c]}")  # SF8
    opt4 = inf[inf.ACCESSION_NUMBER.isin(set(q4acc.ACCESSION_NUMBER)) & (inf.PUTCALL != "") & inf.cusip9.isin(cus)]
    o4 = opt4.groupby("cusip9").SSHPRNAMT.sum()
    ok(o4.get(W07, 0) == 0, "December options on FENN")
    for c in cus:
        alt = 100 * (g["dec_shares_est"][c] + o4.get(c, 0)) / S4[c]
        ok((alt > 80) == g["flag"][c], f"December options flip {ids[c]}")  # SF3
        alt = 100 * g["dec_shares_est"][c] / so[f"{c}|latest"]
        ok((alt > 80) == g["flag"][c], f"the January count flips {ids[c]}")  # SF2

    # ---- main-call invariance: every main-call figure and the declared population as snapshotted (loop 2)
    import json
    import maincall as MC
    ref = json.load(open(MC.REF, encoding="utf-8"))
    snap = MC.snapshot(target, g)
    for k, v in ref["populations"].items():
        ok(snap["populations"][k] == v, f"main call population {k} moved: {snap['populations'][k]} against {v}")
    for k, v in ref["figures"].items():
        cur = snap["figures"][k]
        if isinstance(v, dict) and k in ("rungs", "variants", "grid"):
            for kk, vv in v.items():
                for c, x in vv.items():
                    ok(abs(cur[kk][c] - x) < 1e-9, f"main call {k} {kk} {c} moved")
        elif isinstance(v, dict):
            ok(set(cur) == set(v), f"main call {k} keys")
            for c, x in v.items():
                ok(cur[c] == x if isinstance(x, bool) else abs(cur[c] - x) < 1e-9, f"main call {k} {c} moved {cur[c]} {x}")
        else:
            ok(cur == v, f"main call {k} moved")
    LOG["main_call_identity"] = {k: v["n"] for k, v in ref["populations"].items()}

    # SF12: the back-test's target under every reading of the ask devices keeps the golden basis first (below)
    # ---- back-test robustness: every reading of the September records (period source, seven amendment
    #      orders) and every combination of the line hazards and the counts keeps the golden basis first by 0.3
    fr = g["_frames"]
    combos = G.device_combos(g)
    worst = 9.0
    bt_fns = {}
    for per_src, ff in (("cover", fr["f"]), ("header", fr["fsub"])):
        for mode in G.MODES:
            bt_fns[(per_src, mode)] = G.make_backtest(ff, fr["inf"], cus, fr["mtype"], fr["S"], mode)[0]
    for cb in combos:
        if cb["names"][2] != "all":
            continue                                   # DV-3 is option lines only: no share line moves
        per_src, mode = cb["names"][:2]
        base = g["readings"][(per_src, mode, "all")]["shares"]
        delta = {c: cb["delta"][c] - (base[c] - g["sep_shares"][c]) for c in cus}   # the hazards on top
        b = bt_fns[(per_src, mode)](delta, cb["S"])
        m = min(b[k] for k in rivals) - b[GOLD]
        worst = min(worst, m)
        ok(m >= 0.3, f"back-test margin {m:.3f} under {cb['names']}")
    LOG["robust_margin"] = round(worst, 3)

    # ---- Ask A: September ownership per name. Every stop and every grid cell outside the golden's bin
    def bin_(v):
        return round(v, 1)
    gold = g["sep_io"]
    golden_like = lambda n: n[0] == "cover" and n[1] in ("num", "after") and all(x == "correct" for x in n[3:])
    nmin, cells = 9.0, 0
    for cb in combos:
        if golden_like(cb["names"]):
            ok(all(abs(cb["own"][c] - gold[c]) < 1e-12 for c in cus), f"{cb['names']} should converge on the golden")
            ok(cb["end"] == g["bridge"]["conformed"], f"{cb['names']} bridge end should converge")
            continue
        for c in cb["touched"]:
            d = abs(cb["own"][c] - gold[c])
            nmin = min(nmin, d)
            ok(d >= 0.06 and bin_(cb["own"][c]) != bin_(gold[c]), f"September {ids[c]} {d:.3f} under {cb['names']}")
        cells += 1
    LOG["grid_a"] = dict(cells=cells, min_pp=round(nmin, 3))
    SA = g["stops_a"]
    TGT = {"S1": (0.85, 1.6), "S2": (0.5, 0.9), "S3": (0.3, 0.7), "S4": (-2.3, -1.4)}
    LOG["stops_a"] = {}
    for k, (lo, hi) in TGT.items():
        mv = {ids[c]: round(SA[k][c] - gold[c], 2) for c in cus}
        LOG["stops_a"][k] = mv
        for c in cus:
            d = SA[k][c] - gold[c]
            ok(abs(d) >= 0.06 and bin_(SA[k][c]) != bin_(gold[c]), f"Ask A stop {k} {ids[c]} {d:.3f}")
            ok(lo <= d <= hi, f"Ask A stop {k} {ids[c]} {d:.3f} outside {lo} to {hi}")
    ok(all(abs(SA["S5"][c] - gold[c]) < 1e-12 for c in cus), "Ask A S5 is the golden")
    # the lazy sweep is S1 (period from SUBMISSION, amendments in file order); the over-cleaner is S4

    # ---- Ask B: the September bridge. Every stop moves its bars by more than 0.5 per cent of the golden bar
    GB = g["bridge"]
    BARS = ("raw", "options", "superseded", "cusip_repaired", "conformed")
    SB = g["stops_b"]
    LOG["stops_b"] = {k: {x: int(SB[k][x] - GB[x]) for x in BARS} for k in SB}
    moved_expect = {"S1": set(BARS), "S2": {"superseded", "conformed"}, "S3": set(BARS), "S4": {"raw", "options"}}
    for k, bars in moved_expect.items():
        moved = {x for x in BARS if SB[k][x] != GB[x]}
        ok(moved == bars, f"Ask B stop {k} moves {sorted(moved)}")
        for x in bars:
            d = abs(SB[k][x] - GB[x])
            if (k, x) == ("S4", "raw"):
                ok(d >= 150_000, f"Ask B S4 start {d}")      # DV-3's option lines, not 0.5 per cent of the start
            else:
                ok(d > 0.005 * GB[x], f"Ask B stop {k} {x} {d}")
        if "conformed" in bars:
            ok(abs(SB[k]["conformed"] - GB["conformed"]) >= 3_000_000, f"Ask B stop {k} end")
        gap = SB[k]["raw"] - SB[k]["conformed"]
        ok(round(gap / 1e6, 1) != round((GB["raw"] - GB["conformed"]) / 1e6, 1), f"Ask B stop {k} title gap")
    ok(all(SB["S5"][x] == GB[x] for x in BARS), "Ask B S5 is the golden")
    ok(9_000_000 > 0 and 7_500_000 <= SB["S1"]["conformed"] - GB["conformed"] <= 11_000_000, "Ask B S1 end")
    ok(3_900_000 <= SB["S2"]["conformed"] - GB["conformed"] <= 6_900_000, "Ask B S2 end")
    ok(250_000 <= GB["options"] - SB["S1"]["options"] <= 400_000, "DV-2 option lines")
    ok(GB["cusip_repaired"] - SB["S1"]["cusip_repaired"] >= 600_000, "DV-2 keyed lines")
    emin, ecells, seen = 1e18, 0, set()
    for cb in combos:
        n = cb["names"][:7]                          # the counts do not touch the bridge
        if n in seen:
            continue
        seen.add(n)
        core = n[0] == "cover" and n[1] in ("num", "after") and all(x == "correct" for x in n[3:7])
        e = abs(cb["end"] - GB["conformed"])
        if core:
            if n[2] == "q4":
                ok(e == 0 and cb["bridge"]["raw"] != GB["raw"], "DV-3 alone moves the start, not the end")
            continue
        ok(e > 0, f"bridge end equals the golden under {n}")
        emin = min(emin, e)
        ecells += 1
    LOG["grid_b"] = dict(cells=ecells, min_end=int(emin))

    # ---- single mishandlings: what each device and hazard moves on each ask (the necessity matrix)
    single = {}
    for cb in combos:
        n = cb["names"]
        wrong = []
        if n[0] != "cover":
            wrong.append("DV-2:header")
        if n[1] not in ("num",):
            wrong.append("DV-1:" + n[1])
        if n[2] != "all":
            wrong.append("DV-3:q4_drop")
        wrong += [x for x in n[3:7] if x != "correct"]
        if n[7] != "correct":
            wrong.append("count:" + n[7])
        if len(wrong) != 1:
            continue
        key = wrong[0]
        moved = {ids[c]: round(cb["own"][c] - gold[c], 2) for c in cus if abs(cb["own"][c] - gold[c]) > 1e-12}
        single[key] = dict(ask_a=moved, ask_b={x: int(cb["bridge"][x] - GB[x]) for x in BARS if cb["bridge"][x] != GB[x]})
        if key != "DV-1:after":
            ok(len(moved) >= 1 or single[key]["ask_b"], f"{key} moves nothing")
    LOG["single"] = single
    ok(not single["DV-1:after"]["ask_a"] and not single["DV-1:after"]["ask_b"], "filed-after converges")
    ok(len(single["DV-2:header"]["ask_a"]) == 12 and len(single["DV-1:file"]["ask_a"]) == 12, "DV-1 and DV-2 move every name")
    ok(not single["DV-3:q4_drop"]["ask_a"], "DV-3 moves Ask A")
    ok(len(single["count:oct"]["ask_a"]) == 12, "the October count moves every name")
    ok(set(single["count:q10"]["ask_a"]) == set(W.A5_NAMES), "the 10-Q count moves the three amended names")

    # ---- the cracker and the mirror: the asks read no estimate, so both stand on S1 on every ask figure
    rd = g["readings"][("header", "file", "all")]
    ok({c: 100 * rd["shares"][c] / S3[c] for c in cus} == SA["S1"] and rd["bridge"] == SB["S1"], "cracker S1")

    # ---- the hygiene battery on the natural path (S1) comes back clean
    for d_ in G.DROPS:
        s_ = pd.read_csv(os.path.join(target, d_, "SUBMISSION.tsv"), sep="\t", dtype=str, keep_default_na=False)
        c_ = pd.read_csv(os.path.join(target, d_, "COVERPAGE.tsv"), sep="\t", dtype=str, keep_default_na=False)
        i_ = pd.read_csv(os.path.join(target, d_, "INFOTABLE.tsv"), sep="\t", dtype=str, keep_default_na=False)
        ok(s_.ACCESSION_NUMBER.is_unique and c_.ACCESSION_NUMBER.is_unique, f"{d_} accession keys")
        ok(set(s_.ACCESSION_NUMBER) == set(c_.ACCESSION_NUMBER), f"{d_} submission and cover rows join")
        ok(set(i_.ACCESSION_NUMBER) <= set(s_.ACCESSION_NUMBER), f"{d_} infotable rows join")
        ok(i_.INFOTABLE_SK.is_unique, f"{d_} INFOTABLE_SK")
        ok(not i_.drop(columns=["INFOTABLE_SK"]).duplicated().any(), f"{d_} exact duplicate lines")
    for ff in (fr["f"], fr["fsub"]):
        h_ = ff[ff.REPORTTYPE != "13F NOTICE"]
        ok(not h_.duplicated(["CIK", "period", "AMENDMENTNO"]).any(), "CIK, period and amendment number unique")
    q3c = fr["f"][fr["f"].period == P["Q3"]]
    sameday = q3c.groupby(["CIK", "fdate"]).size()
    ok(int((sameday > 1).sum()) == 4, "four same-day September pairs (DV-1 and three ordinary re-filings)")
    allday = fr["f"].groupby(["CIK", "fdate"]).size()
    ok(int((allday > 1).sum()) >= 4, f"same-day filings by one manager {int((allday > 1).sum())}")
    agents = {a.split("-")[0] for a in fr["f"][fr["f"]["drop"] == "form13f_2022q4"].ACCESSION_NUMBER}
    ok({"0000950123", "0001104659"} <= agents, "both filing agents active in the drop")
    mism = fr["f"][fr["f"].PERIODOFREPORT != fr["f"].REPORTCALENDARORQUARTER]
    ok(len(mism) == 1 and mism.iloc[0].AMENDMENTTYPE == "RESTATEMENT", "one header period disagreement")

    # ---- the referee: the 30 September price each CUSIP's September lines imply; DV-2's restatement among them
    ln = inf[inf.ACCESSION_NUMBER.isin(set(q3c.ACCESSION_NUMBER)) & inf.cusip9.isin(cus) & (inf.PUTCALL == "")
             & ~inf.TITLEOFCLASS.isin(["CALL", "PUT"])].copy()
    ln = ln[ln.VALUE >= 200]
    ln["px"] = ln.VALUE * 1000 / ln.SSHPRNAMT
    med = ln.groupby("cusip9").px.median()
    dev_ = (ln.px / ln.cusip9.map(med) - 1).abs()
    ok((dev_ <= 0.005).all(), f"referee: a September line priced off the close {dev_.max():.4f}")
    rs_acc = mism.iloc[0].ACCESSION_NUMBER
    ok((ln.ACCESSION_NUMBER == rs_acc).sum() >= 9, "referee covers the restatement")
    q2c = fr["f"][(fr["f"].period == P["Q2"])]
    l2 = inf[inf.ACCESSION_NUMBER.isin(set(q2c.ACCESSION_NUMBER)) & inf.cusip9.isin(cus) & (inf.PUTCALL == "") & (inf.VALUE >= 200)].copy()
    med2 = (l2.VALUE * 1000 / l2.SSHPRNAMT).groupby(l2.cusip9).median()
    apart = sum(abs(med[c] / med2[c] - 1) > 0.02 for c in cus)
    ok(apart >= 10, f"June and September closes apart on {apart} names")
    LOG["referee"] = dict(lines=int(len(ln)), max_dev=round(float(dev_.max()), 5), names_apart=int(apart))

    # ---- the bridge ties
    b = g["bridge"]
    ok(b["conformed"] == b["conformed_check"], "bridge does not tie")
    ok(b["principal"] == 0, "principal lines on watchlist CUSIPs")
    for k in ("options", "superseded", "cusip_repaired"):
        ok(b[k] > 0.003 * b["raw"], f"bridge item {k} too small to read")

    # ---- identity: watchlist stems are unique across every covered issuer (the 13(f) list rows)
    stems = [G.stem(i["name"]) for i in wd.iss]
    for c in cus:
        st = G.stem([i["name"] for i in wd.iss if i["cusip"] == c][0])
        ok(stems.count(st) == 1, f"stem {st} not unique")

    # SF13: OM-4 s.8 names layout v4 and the layout file's header is v4
    import docs as D
    om4 = " ".join(t for _, t in D.METHOD)
    ok("The file layout is client flag file layout v4." in om4 and "layout v3" not in om4, "SF13 OM-4 s.8")
    lay = open(os.path.join(target, D.LAYOUT), encoding="utf-8").read()
    ok(lay.startswith("# Client flag file layout, v4") and "replaces v3" in lay, "SF13 layout header")
    # ---- input gates
    files = [os.path.join(dp, fn_) for dp, _, fns in os.walk(target) for fn_ in fns]
    ok(len(files) >= 10, "file count")
    fmts = {os.path.splitext(p)[1] for p in files}
    ok(len(fmts) >= 3, f"formats {fmts}")
    biggest = max(sum(1 for _ in open(p, encoding="utf-8")) - 1 for p in files if p.endswith(".tsv"))
    ok(biggest >= 25_000, f"largest file rows {biggest}")
    ok(len(meta["distractor_files"]) >= 2, "distractors")
    src = open(os.path.join(os.path.dirname(__file__), "golden.py"), encoding="utf-8").read()
    for dfile in meta["distractor_files"]:
        ok(os.path.exists(os.path.join(target, dfile)), f"distractor missing {dfile}")
        ok(os.path.basename(dfile) not in src, f"golden reads distractor {dfile}")
    for p in files:
        if p.endswith((".md", ".htm", ".txt", ".csv")) and "fsds" not in p:
            t = open(p, encoding="utf-8").read().lower()
            for wrd in ("distractor", "pending", "carry forward", "carried forward", "late filer", "censor",
                        "complete filing set", "index and etf sponsor grow", "type change"):
                ok(wrd not in t, f"'{wrd}' in {p}")
    src_note = open(os.path.join(target, "data_sources.md"), encoding="utf-8").read()
    for p in files:
        rel = os.path.relpath(p, target)
        top = rel.split(os.sep)[0]
        if rel != "data_sources.md":
            ok(("`" + top + ("/`" if os.sep in rel else "`")) in src_note, f"data_sources.md does not register {rel}")
    task = os.path.dirname(target)
    for nm in ("prompt.md", "submission.md"):
        hits = [os.path.join(dp, f_) for dp, _, fns in os.walk(task) for f_ in fns if f_ == nm]
        ok(len(hits) <= 1, f"more than one {nm}")
    for fn_ in ("crowded_flags_2022q4.csv", "sep_quarter_bridge.png"):
        ok(os.path.exists(os.path.join(golden_dir, fn_)), fn_)
    return N[0]
