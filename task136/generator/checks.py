"""task136 generator checks: the ladder, the margins, the estimator corridor, every semantic fork row (SF1 to SF22),
the asks' stops and devices, the input gates and the realism sweep. Run by build.py on the built pack; raises on the
first failure and prints the count of assertions passed."""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import calc as C
import common as K

N = [0]
SF_SEEN = {}


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N[0] += 1


def r1(x):
    return round(x + 1e-12, 1)


def ten(x):
    return int(round(x / 10.0) * 10)


def bin_room(x, unit):
    """Distance from x to the nearest rounding edge, as a share of the bin."""
    k = x / unit
    return abs((k - np.floor(k)) - 0.5)


def variant_forecast(L, base_kw=None, avgkw=None, lift_override=None, hc_case="hc29", camps=None, pools=None,
                     basis="untapped"):
    camps = camps or C.campaigns(L)
    pools = pools or C.pools_2027(L)
    fc = C.forecast(L, basis=basis, camps=camps, pools=pools, hc_case=hc_case)
    if base_kw is None and avgkw is None and lift_override is None:
        return fc
    b = base_kw if base_kw is not None else fc["base"]["base"]
    ak = avgkw if avgkw is not None else fc["avgkw"]
    lf = lift_override if lift_override is not None else fc["lift"]
    tot = dict(b)
    for name, n in lf.items():
        f = pools[name]["feeder"]
        tot[f] += n * ak[f]
    ex = {f: tot[f] / 1000.0 - L["hca"][f][hc_case] for f in K.FEEDERS}
    order = sorted(K.FEEDERS, key=lambda f: -ex[f])
    return dict(excess=ex, order=order, winner=order[0], runner=order[1], gap=ex[order[0]] - ex[order[1]], lift=lf)


def graded(v):
    w = v["winner"]
    return (w, v["runner"], r1(v["excess"][w]), r1(v["excess"][v["runner"]]), r1(v["gap"]),
            ten(v["lift"]["Bindarra Waters"]), ten(v["lift"]["Wattleview"]))


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text() or "" for pg in PdfReader(path).pages).split())


def summed_capacity(reg, date):
    d = pd.Timestamp(date)
    live = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= d) & (reg.removal_date.isna() | (reg.removal_date > d))]
    return live.groupby("feeder").kw.sum()


def base_with(reg, cap_fn, trend_kw=None, years=K.YEARS_TO_DESIGN, base_date=K.BASE):
    cap = cap_fn(reg, base_date)
    tr = trend_kw if trend_kw is not None else C.trend(reg)[0]
    return {f: cap.get(f, 0.0) + years * tr[f] for f in K.FEEDERS}


def report(L, base, camps, pools, rb, fc):
    """The ladder and the campaign fits as the design note quotes them (printed on every build)."""
    print("ladder: basis | winner and excess | margin over second | YRB24 position | Bindarra, Wattleview systems")
    for b in ["none", "count", "letterboxed", "ratio", "oo", "udw", "feeder_unt", "untapped"]:
        f = C.forecast(L, basis=b, base=base, camps=camps, pools=pools)
        e = f["excess"]
        print("  %-11s %s %.3f | %.2f | %d | %.1f, %.1f" % (b, f["winner"], e[f["winner"]], e[f["order"][0]] / e[f["order"][1]],
              f["order"].index("YRB24") + 1, f["lift"]["Bindarra Waters"], f["lift"]["Wattleview"]))
    print("campaign fits: basis | coefficient of variation | largest back-cast miss (campaign)")
    for b in ["count", "letterboxed", "ratio", "oo", "udw", "feeder_unt", "untapped"]:
        if b == "count":
            pred = [rb["count"]["mean"] for c in camps]
        elif b == "ratio":
            pred = [(rb["ratio"]["mean"] - 1) * c["before12"] for c in camps]
        elif b == "untapped":
            pred = [rb["untapped"]["pooled"] * c["untapped"] for c in camps]
        else:
            pred = [rb[b]["mean"] * c[b] for c in camps]
        miss = [abs(p - c["systems"]) / c["systems"] for p, c in zip(pred, camps)]
        i = int(np.argmax(miss))
        print("  %-11s %.3f | %.3f (%s)" % (b, rb[b]["cv"], miss[i], camps[i]["key"]))
    # the grid's other axis: alterations summed instead of replaced (against NPP-114 2.2)
    reg = L["reg"]
    tr2 = {}
    for f in K.FEEDERS:
        vals = []
        for s_, e_ in K.TREND_FYS:
            c1, c0 = summed_capacity(reg, e_), summed_capacity(reg, s_ - dt.timedelta(days=1))
            vals.append(c1.get(f, 0) - c0.get(f, 0) - C.program_kw(reg, s_, e_).get(f, 0))
        tr2[f] = float(np.mean(vals))
    b2 = base_with(reg, summed_capacity, tr2)
    print("grid, alterations summed: basis | winner and excess | runner-up and excess")
    for b in ["none", "count", "letterboxed", "ratio", "oo", "udw", "feeder_unt", "untapped"]:
        lf = C.lifts(camps, pools, b) if b != "none" else {k: 0.0 for k in pools}
        v = variant_forecast(L, base_kw=b2, lift_override=lf, camps=camps, pools=pools)
        print("  %-11s %s %.3f | %s %.3f" % (b, v["winner"], v["excess"][v["winner"]], v["runner"], v["excess"][v["runner"]]))
    tw = {c["key"]: c for c in camps}
    print("twin pair: TWR21 %d letterboxed, %d owner-occupied, %d systems; BNR23 %d, %d, %d"
          % (tw["TWR21"]["letterboxed"], tw["TWR21"]["oo"], tw["TWR21"]["systems"], tw["BNR23"]["letterboxed"],
             tw["BNR23"]["oo"], tw["BNR23"]["systems"]))
    print("excess by feeder: " + ", ".join("%s %.3f" % (f, fc["excess"][f]) for f in fc["order"]))
    net = L["net"]
    live = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= pd.Timestamp(K.BASE)) &
               (reg.removal_date.isna() | (reg.removal_date > pd.Timestamp(K.BASE)))]
    tc = dict(zip(net.nmi, net.tariff_class))
    nres = sum(1 for n in set(live.nmi) if tc.get(n) == "Residential")
    print("world: %d NMIs (%d residential); %d systems connected at the base date (%d residential, %d business)"
          % (len(net), int((net.tariff_class == "Residential").sum()), live.nmi.nunique(), nres, live.nmi.nunique() - nres))
    first = C.first_app(reg)
    on_open = {}
    for c in camps:
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        on_open[c["key"]] = int(first[first.index.isin(set(nm.nmi))].eq(pd.Timestamp(c["opening"])).sum())
    edges = sum(int((reg.connection_date == pd.Timestamp(d_)).sum()) for s_, e_ in K.TREND_FYS for d_ in (s_, e_))
    print("boundary days: %d connections on the base date; applications received on an opening day %s; %d connections "
          "on financial-year edges" % (int((reg.connection_date == pd.Timestamp(K.BASE)).sum()), on_open, edges))
    u = rb["untapped"]
    print("estimators (per cent): pooled %.3f, mean %.3f, origin %.3f, median %.3f, ols slope %.3f with intercept %.2f "
          "systems" % (100 * u["pooled"], 100 * u["mean"], 100 * u["origin"], 100 * u["median"], 100 * u["ols"][0], u["ols"][1]))
    print("SF variants: %s" % {k: tuple(str(x) for x in v) for k, v in SF_SEEN.items()})
    res = set(net[net.tariff_class == "Residential"].nmi)
    rr = reg[reg.nmi.isin(res)]
    b1 = base_with(rr, C.connected_kw, C.trend(rr)[0])
    share = {f: 1 - b1[f] / base["base"][f] for f in K.FEEDERS}
    print("business share of each base: %.3f to %.3f" % (min(share.values()), max(share.values())))
    prog_kw = sum(c["kw_program"] for c in camps) / sum(c["systems"] for c in camps)
    v = variant_forecast(L, avgkw={f: prog_kw for f in K.FEEDERS}, camps=camps, pools=pools)
    print("SF10 past programs' average %.2f kW: %s" % (prog_kw, tuple(str(x) for x in graded(v))))


def run(target, golden, W=None, meta_path=None):
    N[0] = 0
    L = C.load(target)
    reg = L["reg"]
    base = C.base_forecast(reg)
    camps = C.campaigns(L)
    pools = C.pools_2027(L)
    rb = C.rates_by_basis(camps)
    fc = C.forecast(L, base=base, camps=camps, pools=pools)
    ex = fc["excess"]

    # ---------------------------------------------------------------- the call
    ok(fc["winner"] == "YRB24", "golden winner %s" % fc["winner"])
    ok(fc["runner"] == "YRB22", "runner-up %s" % fc["runner"])
    ok(r1(ex["YRB24"]) == 1.9, "YRB24 excess %.4f" % ex["YRB24"])
    ok(r1(ex["YRB22"]) == 1.5, "YRB22 excess %.4f" % ex["YRB22"])
    ok(r1(fc["gap"]) == 0.4, "gap %.4f" % fc["gap"])
    ok(abs(r1(fc["gap"]) - (r1(ex["YRB24"]) - r1(ex["YRB22"]))) < 1e-9, "SF22 gap equals the rounded difference")
    ok(ten(fc["lift"]["Bindarra Waters"]) == 240, "Bindarra systems %.2f" % fc["lift"]["Bindarra Waters"])
    ok(ten(fc["lift"]["Wattleview"]) == 30, "Wattleview systems %.2f" % fc["lift"]["Wattleview"])
    ok(ex["YRB24"] / ex["YRB22"] >= 1.20, "golden margin %.3f" % (ex["YRB24"] / ex["YRB22"]))
    for x, unit, name in ((ex["YRB24"], 0.1, "excess"), (ex["YRB22"], 0.1, "runner-up excess"), (fc["gap"], 0.1, "gap"),
                          (fc["lift"]["Bindarra Waters"], 10, "Bindarra"), (fc["lift"]["Wattleview"], 10, "Wattleview")):
        ok(bin_room(x, unit) >= 0.07, "%s %.4f too near a rounding edge" % (name, x))
    ok(abs(ex["YRB24"] * 10 - round(ex["YRB24"] * 10)) > 1e-6, "no round headline")

    # ---------------------------------------------------------------- the ladder
    wrong = ["none", "count", "letterboxed", "ratio", "oo", "udw", "feeder_unt"]
    second = 0
    for b in wrong:
        f = C.forecast(L, basis=b, base=base, camps=camps, pools=pools)
        e = f["excess"]
        ok(f["winner"] == "YRB22", "rung %s winner %s" % (b, f["winner"]))
        ok(e[f["order"][0]] / e[f["order"][1]] >= 1.15, "rung %s margin %.3f" % (b, e[f["order"][0]] / e[f["order"][1]]))
        pos = f["order"].index("YRB24") + 1
        ok(pos >= 2, "rung %s puts YRB24 first" % b)
        if pos == 2:
            second += 1
            ok(e["YRB22"] / e["YRB24"] >= 1.20, "rung %s: YRB24 second within 1.20 (%.3f)" % (b, e["YRB22"] / e["YRB24"]))
        if b != "none":
            ok(ten(f["lift"]["Bindarra Waters"]) != 240, "rung %s lands Bindarra in the golden bin" % b)
            ok(ten(f["lift"]["Wattleview"]) != 30, "rung %s lands Wattleview in the golden bin" % b)
    ok(second <= 1, "YRB24 second on %d rungs" % second)
    d = C.forecast(L, basis="letterboxed", base=base, camps=camps, pools=pools)
    ok(d["order"].index("YRB24") + 1 in (4, 5), "default path places YRB24 %d" % (d["order"].index("YRB24") + 1))
    ok(r1(d["excess"]["YRB22"]) == 1.5, "default path files YRB22 at 1.5")

    # the seven campaigns: the conjunction alone fits, no partial step is rewarded
    ok(rb["untapped"]["cv"] < 0.01, "per-untapped spread %.4f" % rb["untapped"]["cv"])
    for b in ("oo", "udw", "feeder_unt", "ratio"):
        ok(rb[b]["cv"] >= rb["letterboxed"]["cv"] - 1e-9, "basis %s fits better than per letterbox (%.3f < %.3f)"
           % (b, rb[b]["cv"], rb["letterboxed"]["cv"]))
    ok(rb["count"]["cv"] >= 0.30, "systems installed spread %.3f" % rb["count"]["cv"])
    ok(rb["letterboxed"]["cv"] >= 0.20, "per-letterbox spread %.3f" % rb["letterboxed"]["cv"])
    # each refused basis misses at least one campaign by a quarter (SF16 to SF20)
    for b, sf in (("letterboxed", "SF16"), ("oo", "SF17"), ("udw", "SF18"), ("feeder_unt", "SF19"), ("count", "SF20"),
                  ("ratio", "SF20")):
        if b == "count":
            pred = [rb["count"]["mean"] for c in camps]
        elif b == "ratio":
            pred = [(rb["ratio"]["mean"] - 1) * c["before12"] for c in camps]
        else:
            pred = [rb[b]["mean"] * c[b] for c in camps]
        miss = max(abs(p - c["systems"]) / c["systems"] for p, c in zip(pred, camps))
        ok(miss >= 0.25, "%s basis %s misses at most %.3f" % (sf, b, miss))
    pred = [rb["untapped"]["pooled"] * c["untapped"] for c in camps]
    ok(max(abs(p - c["systems"]) for p, c in zip(pred, camps)) <= 1.5, "the pooled rate reproduces each campaign")
    # twin pair: Tallowwood Rise and Bunya Ridge
    tw = {c["key"]: c for c in camps}
    a_, b_ = tw["TWR21"], tw["BNR23"]
    ok(abs(a_["letterboxed"] / b_["letterboxed"] - 1) < 0.02 and abs(a_["oo"] / b_["oo"] - 1) < 0.04, "twin pair visible fields")
    ok(a_["systems"] / b_["systems"] >= 1.8, "twin pair outcomes %.2f" % (a_["systems"] / b_["systems"]))
    # the council's log and letter agree with the distributor's records
    for c in camps:
        ok(c["systems_log"] == c["systems"], "%s log %d register %d" % (c["key"], c["systems_log"], c["systems"]))
        ok(c["letterboxed"] == c["res_nmis"], "%s letterboxed %d residential NMIs %d" % (c["key"], c["letterboxed"], c["res_nmis"]))
    for name, p in pools.items():
        ok(p["letterboxed"] == p["res_nmis"], "%s letter %d NMIs %d" % (name, p["letterboxed"], p["res_nmis"]))

    # ---------------------------------------------------------------- estimator and pool-date corridor (SF11, SF15)
    for est in ("pooled", "mean", "origin", "median", "ols"):
        for pdate in ("open", "base"):
            v = C.forecast(L, basis="untapped", estimator=est, pool_date=pdate, base=base, camps=camps, pools=pools)
            tag = "SF15 %s / SF11 %s" % (est, pdate)
            ok(v["winner"] == "YRB24" and v["runner"] == "YRB22", tag + " call")
            ok(r1(v["excess"]["YRB24"]) == 1.9 and r1(v["gap"]) == 0.4, tag + " excess %.4f gap %.4f"
               % (v["excess"]["YRB24"], v["gap"]))
            ok(ten(v["lift"]["Bindarra Waters"]) == 240 and ten(v["lift"]["Wattleview"]) == 30,
               tag + " systems %.2f %.2f" % (v["lift"]["Bindarra Waters"], v["lift"]["Wattleview"]))

    # ---------------------------------------------------------------- the semantic fork rows
    # SF1 residential NMIs only
    res = set(L["net"][L["net"].tariff_class == "Residential"].nmi)
    reg_res = reg[reg.nmi.isin(res)]
    b1 = base_with(reg_res, C.connected_kw, C.trend(reg_res)[0])
    v = variant_forecast(L, base_kw=b1, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24", "SF1 residential only files %s" % v["winner"])
    ok(r1(v["excess"]["YRB24"]) != 1.9, "SF1 residential only keeps every figure")
    SF_SEEN["SF1 residential only"] = graded(v)
    npp = pdf_text(os.path.join(target, K.NPP))
    ok("at a residential or business NMI" in npp, "SF1 NPP-114 2.1 no longer names business NMIs")
    ok(reg.kw.max() <= 30.0, "SF1 a register system above 30 kVA (%.1f)" % reg.kw.max())
    # SF2 alterations summed; panel capacity
    tr2 = {}
    for f in K.FEEDERS:
        vals = []
        for s, e in K.TREND_FYS:
            c1, c0, pk = summed_capacity(reg, e), summed_capacity(reg, s - dt.timedelta(days=1)), C.program_kw(reg, s, e)
            vals.append(c1.get(f, 0) - c0.get(f, 0) - pk.get(f, 0))
        tr2[f] = float(np.mean(vals))
    b2 = base_with(reg, summed_capacity, tr2)
    v = variant_forecast(L, base_kw=b2, camps=camps, pools=pools)
    ok(graded(v) != graded(fc), "SF2 summed alterations keeps every figure")
    ok("An alteration replaces the configuration it alters." in npp, "SF2 NPP-114 2.2 alteration sentence missing")
    SF_SEEN["SF2 summed"] = graded(v)
    reg_p = reg.assign(kw=reg.panel_kwp.replace("", np.nan).astype(float))
    b2p = base_with(reg_p, C.connected_kw, C.trend(reg_p)[0])
    v = variant_forecast(L, base_kw=b2p, avgkw=C.avg_new_kw(reg_p), camps=camps, pools=pools)
    ok(graded(v) != graded(fc), "SF2 panel capacity keeps every figure")
    ok("inverter capacity (kW, AC rating)" in npp, "SF2 NPP-114 2.2 inverter capacity sentence missing")
    SF_SEEN["SF2 panel"] = graded(v)
    # SF3 migrated rows dropped
    reg_m = reg[reg.legacy_application_no == ""]
    b3 = base_with(reg_m, C.connected_kw, C.trend(reg_m)[0])
    v = variant_forecast(L, base_kw=b3, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24", "SF3 migrated rows dropped files %s" % v["winner"])
    # SF23 the legacy join is one to one: every legacy application number is issued once in the equipment table and
    # once in the register, so a lookup, a merge (each register row's matches summed) and a first-match join select
    # the same inverter for every migrated row (C1). Stage 3 drew 40 numbers twice; summing both rows then filed YRB22
    # at 1.6 MW and a 0.3 MW gap.
    leg = L["leg"]
    regl = reg[reg.legacy_application_no != ""]
    ok(leg.legacy_application_no.is_unique, "SF23 a legacy application number repeats in the equipment table")
    ok(regl.legacy_application_no.is_unique, "SF23 a legacy application number repeats in the register")
    ok(set(regl.legacy_application_no) == set(leg.legacy_application_no), "SF23 the legacy numbers do not pair one to one")
    lk = leg.assign(kw_row=leg.inverter_kw_ac_each.astype(float) * leg.inverter_count.astype(int))
    mg = regl[["legacy_application_no"]].reset_index().merge(lk[["legacy_application_no", "kw_row"]],
                                                              on="legacy_application_no", how="left")
    ok(len(mg) == len(regl), "SF23 the legacy join fans out")
    summed_kw = mg.groupby("index").kw_row.sum().reindex(regl.index)
    first_kw = regl.legacy_application_no.map(lk.drop_duplicates("legacy_application_no", keep="first")
                                              .set_index("legacy_application_no").kw_row)
    ok(np.allclose(summed_kw.values, regl.kw.values) and np.allclose(first_kw.values, regl.kw.values),
       "SF23 a lookup, a merge and a first-match join give different inverters")
    SF_SEEN["SF23 legacy numbers reissued"] = (int(leg.legacy_application_no.duplicated().sum()),)
    # SF4 approved but not connected counted
    reg4 = reg.copy()
    m = reg4.status.isin(["Approved"])
    reg4.loc[m, "status"] = "Connected"
    reg4.loc[m, "connection_date"] = reg4.loc[m, "approved_date"]
    b4 = base_with(reg4, C.connected_kw, C.trend(reg)[0])
    v = variant_forecast(L, base_kw=b4, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24", "SF4 files %s" % v["winner"])
    ok(max(abs(b4[f] / base["base"][f] - 1) for f in K.FEEDERS) < 0.02, "SF4 moves a base by 2 per cent or more")
    # SF5 the feeder recorded on the application
    reg5 = reg.assign(feeder=reg.feeder_at_application)
    b5 = base_with(reg5, C.connected_kw, C.trend(reg5)[0])
    v = variant_forecast(L, base_kw=b5, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24" and v["runner"] == "YRB22", "SF5 feeder at application files %s" % v["winner"])
    moved = [f for f in K.FEEDERS if abs(b5[f] - base["base"][f]) > 1e-6]
    ok(set(moved) == {"YRB21", "YRB23"}, "SF5 moves %s" % moved)
    # SF6 base date 30 June 2026
    b6 = base_with(reg, C.connected_kw, base_date=dt.date(2026, 6, 30))
    v = variant_forecast(L, base_kw=b6, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24", "SF6 files %s" % v["winner"])
    # SF7 trend variants
    tr_new = {}
    for f in K.FEEDERS:
        vals = []
        for s, e in K.TREND_FYS:
            new = reg[(reg.application_type == "New") & reg.status.isin(C.CONNECTED) & (reg.connection_date >= pd.Timestamp(s))
                      & (reg.connection_date <= pd.Timestamp(e)) & (reg.program_ref == "") & (reg.feeder == f)]
            vals.append(new.kw.sum())
        tr_new[f] = float(np.mean(vals))
    for name, trv in (("new connections only", tr_new), ("program systems left in", C.trend(reg, exclude_program=False)[0])):
        bb = base_with(reg, C.connected_kw, trv)
        v = variant_forecast(L, base_kw=bb, camps=camps, pools=pools)
        ok(v["winner"] == "YRB24", "SF7 %s files %s" % (name, v["winner"]))
    # SF8 3.25 or 2.92 years
    for yrs in (3.25, 2.92):
        bb = base_with(reg, C.connected_kw, years=yrs)
        v = variant_forecast(L, base_kw=bb, camps=camps, pools=pools)
        ok(v["winner"] == "YRB24", "SF8 %.2f years files %s" % (yrs, v["winner"]))
    # SF9 contracts instead of systems installed
    contracts = {r_["Suburb"]: int(r_["Contracts signed"]) for r_ in L["log"]}
    camps9 = [dict(c, systems=contracts[c["suburb"]]) for c in camps]
    v = C.forecast(L, base=base, camps=camps9, pools=pools)
    ok(v["winner"] == "YRB24", "SF9 contracts files %s" % v["winner"])
    ok(ten(v["lift"]["Bindarra Waters"]) != 240 or ten(v["lift"]["Wattleview"]) != 30, "SF9 contracts move the campaign figures")
    # SF10 program systems at the past campaigns' own average size
    prog_kw = sum(c["kw_program"] for c in camps) / sum(c["systems"] for c in camps)
    v = variant_forecast(L, avgkw={f: prog_kw for f in K.FEEDERS}, camps=camps, pools=pools)
    ok(v["winner"] == "YRB24", "SF10 files %s" % v["winner"])
    ok(abs(prog_kw / fc["avgkw"]["YRB24"] - 1) < 0.08, "SF10 size ratio %.3f" % (prog_kw / fc["avgkw"]["YRB24"]))
    # SF12 only owner-occupied houses ever took a program system
    prog_n = set(reg[(reg.program_ref != "") & reg.status.isin(C.CONNECTED)].nmi)
    xp = L["xref"][L["xref"].nmi.isin(prog_n)].merge(L["rates"], on="property_no")
    ok(len(xp) == len(prog_n) and set(xp.land_use_code) == {"02"} and set(xp.rating_category) == {"R1"},
       "SF12 a program system sits on a property other than an owner-occupied house")
    # SF13 approved-not-yet-connected at an opening treated as untapped
    first_conn = reg[reg.status.isin(C.CONNECTED)].groupby("nmi").received_date.min()
    camps13 = []
    for c in camps:
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        tp = C.tapped_props(nm, first_conn, c["opening"])
        camps13.append(dict(c, untapped=int((~r_.property_no.isin(tp)).sum())))
    rb13 = C.rates_by_basis(camps13)
    ok(abs(rb13["untapped"]["pooled"] - rb["untapped"]["pooled"]) < 0.0002, "SF13 rate moves %.5f"
       % (rb13["untapped"]["pooled"] - rb["untapped"]["pooled"]))
    v = C.forecast(L, base=base, camps=camps13, pools=pools)
    ok(ten(v["lift"]["Bindarra Waters"]) == 240 and r1(v["excess"]["YRB24"]) == 1.9, "SF13 figures move")
    # SF13 also: "without PV" read as no live connected system at the date (removed systems and applications not
    # yet connected count as without PV), at the openings and for the 2027 pools
    def live_at(d):
        d = pd.Timestamp(d)
        x = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date < d) & (reg.removal_date.isna() | (reg.removal_date >= d))]
        return set(x.nmi)
    camps13b, pools13b = [], {}
    for c in camps:
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        tp = set(nm[nm.nmi.isin(live_at(c["opening"]))].property_no)
        camps13b.append(dict(c, untapped=int((~r_.property_no.isin(tp)).sum())))
    for name, p_ in pools.items():
        r_, nm = C.houses(L["rates"], L["xref"], name)
        tp = set(nm[nm.nmi.isin(live_at(K.BASE + dt.timedelta(days=1)))].property_no)
        ub = int((~r_.property_no.isin(tp)).sum())
        pools13b[name] = dict(p_, untapped_base=ub, untapped_open=ub - p_["adopt_fy"])
    ok(graded(C.forecast(L, base=base, camps=camps13b, pools=pools13b)) == graded(fc), "SF13 live-system reading moves a figure")
    ok(graded(C.forecast(L, base=base, camps=camps13b, pools=pools13b, pool_date="base")) == graded(fc),
       "SF13 live-system reading with the pool at the base date (SF11) moves a figure")
    # SF24: an application of any status, a withdrawn one included, read as PV. The seven campaigns fit it about
    # as well, so the records do not separate it; it files Bindarra Waters at 244.6 systems, 245.8 (250) with the pool
    # at the base date. Ruled out by the dictionary: nothing is connected under a withdrawn application, so the house
    # is still without PV.
    first_any = reg.groupby("nmi").received_date.min()
    campsW = [dict(c, untapped=len(C.untapped(L["rates"], L["xref"], first_any, c["suburb"], c["opening"]))) for c in camps]
    poolsW = {}
    for name, p_ in pools.items():
        ub = len(C.untapped(L["rates"], L["xref"], first_any, name, K.BASE + dt.timedelta(days=1)))
        r_, nm = C.houses(L["rates"], L["xref"], name)
        f_oo = first_any[first_any.index.isin(set(nm.nmi))]
        ad = int(((f_oo >= pd.Timestamp(K.LAST_FY[0])) & (f_oo <= pd.Timestamp(K.LAST_FY[1]))).sum())
        poolsW[name] = dict(p_, untapped_base=ub, adopt_fy=ad, untapped_open=ub - ad)
    ok(C.rates_by_basis(campsW)["untapped"]["cv"] < 0.01, "SF24 withdrawn-as-PV now scatters: the records separate it")
    vW = C.forecast(L, base=base, camps=campsW, pools=poolsW)
    vW0 = C.forecast(L, base=base, camps=campsW, pools=poolsW, pool_date="base")
    ok(vW["winner"] == "YRB24" and vW0["winner"] == "YRB24", "SF24 withdrawn-as-PV moves the call")
    ok(ten(vW0["lift"]["Bindarra Waters"]) == 250, "SF24 withdrawn-as-PV at the base date: Bindarra %.2f (the row says 250)"
       % vW0["lift"]["Bindarra Waters"])
    SF_SEEN["SF24 withdrawn as PV"] = graded(vW)
    SF_SEEN["SF24 withdrawn as PV, pool at the base date"] = graded(vW0)
    import openpyxl
    wbd = openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True)
    sdef = [r_[1] for r_ in wbd["Connections register"].iter_rows(values_only=True) if r_ and r_[0] == "status"]
    ok(len(sdef) == 1 and "Withdrawn: withdrawn by the applicant or lapsed before connection; nothing was connected "
       "under the application." in sdef[0], "SF24 the dictionary no longer defines Withdrawn")
    wd = reg[reg.status == "Withdrawn"]
    ok((wd.connection_date.isna()).all() and (wd.inverter_kw_ac == "").all() and (wd.legacy_application_no == "").all(),
       "SF24 a withdrawn application carries a connection or a system")
    # every program system went to a house without PV at its campaign's opening
    first_ok = C.first_app(reg)
    for c in camps:
        ref = "SS-%s-%s" % (c["key"][-2:], c["key"][:3])
        nm_sys = set(reg[(reg.program_ref == ref) & (reg.application_type == "New") & reg.status.isin(C.CONNECTED)].nmi)
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        props = set(nm[nm.nmi.isin(nm_sys)].property_no)
        tapped = C.tapped_props(nm, first_ok, c["opening"])
        ok(len(props) == len(nm_sys) and not (props & tapped), "SF12 %s: a program system on a house with PV" % c["key"])

    # SF14 suburb by the network model's locality: the same NMIs
    for c in camps:
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        net_loc = set(L["net"][L["net"].locality.str.upper() == c["suburb"].upper()].nmi)
        ok(set(nm.nmi) <= net_loc, "SF14 %s rates-roll houses outside the network model's locality" % c["key"])
    # SF21 the 2026 case
    v = C.forecast(L, base=base, camps=camps, pools=pools, hc_case="hc26")
    ok(v["winner"] == "YRB24", "SF21 the 2026 case files %s" % v["winner"])
    SF_SEEN["SF21 the 2026 case"] = graded(v)
    # SF16 also: the stage 4 reader's reading of NPP-114 4.1, systems installed over homes letterboxed pooled over the
    # seven campaigns, files YRB22 at 1.5 MW with Bindarra Waters at 90 and Wattleview at 50 and YRB24 fifth. Ruled
    # out by the records: the seven rates vary 0.6 per cent per untapped owner-occupied house (sample coefficient of
    # variation) against 25.5 per letterbox, 30.1 per owner-occupied house and 27.5 per address without PV.
    pooled_lb = sum(c["systems"] for c in camps) / sum(c["letterboxed"] for c in camps)
    lf = {k: pooled_lb * p["letterboxed"] for k, p in pools.items()}
    v = variant_forecast(L, lift_override=lf, camps=camps, pools=pools)
    ok(v["winner"] == "YRB22" and r1(v["excess"]["YRB22"]) == 1.5 and v["order"].index("YRB24") + 1 == 5,
       "SF16 pooled per letterbox files %s, YRB24 %d" % (v["winner"], v["order"].index("YRB24") + 1))
    ok(ten(lf["Bindarra Waters"]) == 90 and ten(lf["Wattleview"]) == 50, "SF16 pooled per letterbox systems %.1f %.1f"
       % (lf["Bindarra Waters"], lf["Wattleview"]))
    cv1 = {b: float(np.std(rb[b]["values"], ddof=1) / rb[b]["mean"]) for b in ("untapped", "letterboxed", "oo", "udw")}
    ok(cv1["untapped"] < 0.01, "SF16 per untapped owner-occupied house scatters %.4f" % cv1["untapped"])
    ok(min(cv1[b] for b in ("letterboxed", "oo", "udw")) >= 0.25, "SF16 a refused basis fits the records: %s" % cv1)
    SF_SEEN["SF16 pooled per letterbox"] = graded(dict(v, lift=lf))
    # SF16 to SF20 listed with the ladder above; SF22 with the call.

    # ---------------------------------------------------------------- closure axes asserted
    pend = reg[(reg.program_ref != "") & reg.status.isin(["Approved", "Under assessment"])]
    ok(len(pend) == 0, "closure 12: program systems pending at the base date")
    for c in camps:
        ref = "SS-%s-%s" % (c["key"][-2:], c["key"][:3])
        conn = reg[(reg.program_ref == ref) & reg.status.isin(C.CONNECTED)].connection_date
        fys = {K.fy_of(x.date()) for x in conn}
        if pd.Timestamp(c["opening"]) >= pd.Timestamp(K.TREND_FYS[0][0]):
            ok(len(fys) == 1, "closure 3: %s program systems span financial years %s" % (c["key"], fys))
        ok((conn - pd.Timestamp(c["opening"])).dt.days.max() <= 270, "closure 3: %s connection lag" % c["key"])
    # closure 9: records on a boundary day moved across it change no graded figure
    g0 = graded(fc)
    ok((reg.connection_date == pd.Timestamp(K.BASE)).sum() > 0, "closure 9: no connection on the base date to test")
    b9 = base_with(reg, C.connected_kw, base_date=K.BASE - dt.timedelta(days=1))
    ok(graded(variant_forecast(L, base_kw=b9, camps=camps, pools=pools)) == g0, "closure 9: base date read exclusively")
    late = [(s_ + dt.timedelta(days=1), e_ + dt.timedelta(days=1)) for s_, e_ in K.TREND_FYS]
    b9 = base_with(reg, C.connected_kw, C.trend(reg, fys=late)[0])
    ok(graded(variant_forecast(L, base_kw=b9, camps=camps, pools=pools)) == g0, "closure 9: financial years a day late")
    first = C.first_app(reg)
    camps9, on_day = [], 0
    for c in camps:
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        on_day += int(first[first.index.isin(set(nm.nmi))].eq(pd.Timestamp(c["opening"])).sum())
        tp = set(nm[nm.nmi.isin(first[first <= pd.Timestamp(c["opening"])].index)].property_no)
        camps9.append(dict(c, untapped=int((~r_.property_no.isin(tp)).sum())))
    ok(on_day > 0, "closure 9: no application received on an opening day to test")
    ok(graded(C.forecast(L, base=base, camps=camps9, pools=pools)) == g0, "closure 9: an opening read inclusively")
    # row order changes nothing
    shuffled = dict(L, reg=reg.sample(frac=1.0, random_state=7).reset_index(drop=True))
    v = C.forecast(shuffled, base=C.base_forecast(shuffled["reg"]), camps=C.campaigns(shuffled), pools=C.pools_2027(shuffled))
    ok(abs(v["excess"]["YRB24"] - ex["YRB24"]) < 1e-9, "closure 14 row order")
    # no property with two NMIs in a campaign suburb
    xr = L["xref"].merge(L["rates"][["property_no", "locality"]], on="property_no")
    multi = xr.groupby("property_no").nmi.count()
    sub = {c["suburb"].upper() for c in K.CAMPAIGNS} | {c["suburb"].upper() for c in K.CAMPAIGNS_2027}
    ok(not xr[xr.property_no.isin(multi[multi > 1].index)].locality.isin(sub).any(), "closure 15 dual occupancy in a campaign suburb")
    # NMIs are ten characters in the main files
    ok(reg.nmi.str.len().eq(10).all() and L["net"].nmi.str.len().eq(10).all() and L["xref"].nmi.str.len().eq(10).all(),
       "closure 16 NMI formats on the main path")
    # tie-break: no two feeders within 0.1 MW at the top
    ok(ex[fc["order"][0]] - ex[fc["order"][1]] > 0.1, "closure 11")

    # ---------------------------------------------------------------- the asks
    ga, gb = C.ask_a(L, "golden")
    for mode in ("norm", "raw", "rows"):
        a, b = C.ask_a(L, mode)
        ok(all(a[f] != ga[f] for f in K.FEEDERS), "ask A %s matches the golden first figure somewhere" % mode)
        ok(all(b[f] != gb[f] for f in K.FEEDERS), "ask A %s matches the golden second figure somewhere" % mode)
    a, b = C.ask_a(L, "dropunknown")
    ok(all(b[f] != gb[f] for f in K.FEEDERS), "ask A over-cleaner lands the second figure")
    ok(all(a[f] != ga[f] for f in K.FEEDERS), "ask A over-cleaner lands the first figure")
    gs = C.ask_b(L, "golden")
    rows = C.ask_b(L, "rows")
    ok(all(ten(rows[f]) != ten(gs[f]) for f in K.FEEDERS), "ask B summed device rows lands a figure")
    # "sites" counted as AC connections instead of NMIs: the same counts
    remap = dict(zip(L["realloc"].old_nmi, L["realloc"].new_nmi))
    der_k = L["der"].assign(key=L["der"].nmi.map(C.norm_nmi).map(lambda x: remap.get(x, x)))
    live_n = set(reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= pd.Timestamp(K.BASE)) &
                     (reg.removal_date.isna() | (reg.removal_date > pd.Timestamp(K.BASE)))].nmi)
    act_k = der_k[(der_k.ac_connection_status == "Active") & ~der_k.key.isin(live_n)]
    per_conn = act_k.groupby("ac_connection_id").agg(key=("key", "first"), feeder=("feeder", "first"))
    per_conn = per_conn.assign(f=[L["feeder"].get(k_, f_) for k_, f_ in zip(per_conn.key, per_conn.feeder)])
    ok(per_conn.groupby("f").size().reindex(K.FEEDERS, fill_value=0).to_dict() == gb, "ask A sites by AC connection differ")
    # the DER Register read as at 31 August 2026 (registrations after it dropped, later decommissionings undone)
    der_b = L["der"]
    late = der_b[pd.to_datetime(der_b.registered_date) > pd.Timestamp(K.BASE)]
    undo = (der_b.ac_connection_status == "Decommissioned") & (pd.to_datetime(der_b.status_date) > pd.Timestamp(K.BASE))
    der_at = der_b.drop(late.index).copy()
    der_at.loc[undo[~undo.index.isin(late.index)][lambda x: x].index, "ac_connection_status"] = "Active"
    L_at = dict(L, der=der_at)
    ok(C.ask_a(L_at, "golden") == (ga, gb), "ask A as at 31 August 2026 differs")
    ok({f: ten(v) for f, v in C.ask_b(L_at, "golden").items()} == {f: ten(v) for f, v in gs.items()},
       "ask B as at 31 August 2026 differs")
    nd = C.ask_b(L, "nodecom")
    ok(sum(ten(nd[f]) != ten(gs[f]) for f in K.FEEDERS) >= 3, "ask B decommissioned hazard moves too few feeders")
    for f in K.FEEDERS:
        ok(bin_room(gs[f], 10) >= 0.07, "ask B %s %.2f too near a rounding edge" % (f, gs[f]))
    # every feeder carries the devices
    der = L["der"]
    der10 = der.assign(n10=der.nmi.map(C.norm_nmi))
    temp = set(L["realloc"][L["realloc"].reason.str.startswith("Builder")].old_nmi)
    per = der10[der10.n10.isin(temp) & (der10.ac_connection_status == "Active")].groupby("feeder").n10.nunique()
    ok(all(per.get(f, 0) >= 1 for f in K.FEEDERS), "ask A primary absent on a feeder: %s" % per.to_dict())
    bat = der[(der.device_type == "Battery") & (der.ac_connection_status == "Active")]
    multi = bat.groupby("ac_connection_id").agg(n=("nmi", "size"), f=("feeder", "first"))
    ok(all((multi[multi.f == f].n >= 2).any() for f in K.FEEDERS), "ask B primary absent on a feeder")
    # ask B's one reading, carried by the data and never written in the pack: a connection's storage capacity is one
    # value on all its battery rows, does not rise with the number of module rows, is a home battery's size (the
    # register's battery_kwh, the rebate file's nominal_kwh) and matches the site's own connection record, while the
    # row sums run to several times both
    allb = der[der.device_type == "Battery"].assign(kwh=lambda d: d.storage_capacity_kwh.astype(float))
    per_c = allb.groupby("ac_connection_id").agg(k=("kwh", "size"), lo=("kwh", "min"), hi=("kwh", "max"),
                                                 st=("ac_connection_status", "first"), nmi=("nmi", "first"))
    ok((per_c.lo == per_c.hi).all(), "ask B a connection's battery rows carry different capacities")
    act_c = per_c[per_c.st == "Active"]
    by_k = act_c.groupby("k").lo.mean()
    ok(len(by_k) >= 4 and by_k.max() / by_k.min() < 1.25, "ask B capacity rises with the module rows: %s"
       % by_k.round(2).to_dict())
    ok(abs(act_c[["k", "lo"]].corr(method="spearman").iloc[0, 1]) < 0.2, "ask B capacity follows the row count")
    app_kwh = reg.battery_kwh[reg.battery_kwh != ""].astype(float)
    reb = pd.read_csv(os.path.join(target, K.REBATE), dtype=str, keep_default_na=False)
    reb_kwh = reb.nominal_kwh[reb.nominal_kwh != ""].astype(float)
    home_lo, home_hi = min(app_kwh.min(), reb_kwh.min()), max(app_kwh.max(), reb_kwh.max())
    ok(act_c.lo.min() >= home_lo - 0.05 and act_c.lo.max() <= 1.05 * home_hi, "ask B capacity %.1f to %.1f outside "
       "a home battery's %.1f to %.1f" % (act_c.lo.min(), act_c.lo.max(), home_lo, home_hi))
    ok((act_c.k * act_c.lo).max() >= 3 * home_hi, "ask B row sums stay inside a home battery's range")
    last_b = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= pd.Timestamp(K.BASE)) &
                 (reg.removal_date.isna() | (reg.removal_date > pd.Timestamp(K.BASE)))]
    last_b = last_b.sort_values(["nmi", "connection_date", "application_type"]).groupby("nmi").tail(1)
    site_kwh = dict(zip(last_b.nmi, last_b.battery_kwh))
    act_c = act_c.assign(app=act_c.nmi.map(C.norm_nmi).map(lambda x: remap.get(x, x)).map(site_kwh).fillna(""))
    m_c = act_c[act_c.app != ""].assign(app=lambda d: d.app.astype(float))
    once = (m_c.lo / m_c.app).groupby(m_c.k).median()
    summed = (m_c.lo * m_c.k / m_c.app).groupby(m_c.k).median()
    ok(len(m_c) >= 0.9 * len(act_c), "ask B %d of %d active battery connections match a site record" % (len(m_c), len(act_c)))
    ok(once.between(0.8, 1.2).all() and (summed[summed.index >= 2] >= 1.5).all(),
       "ask B once per connection %s, summed %s, against the site's battery_kwh" % (once.round(3).to_dict(),
                                                                                     summed.round(3).to_dict()))
    print("ask B one reading: capacity by module rows %s (Spearman %.3f); per connection %.1f to %.1f kWh against the "
          "register's battery_kwh %.1f to %.1f and the rebate file's nominal_kwh %.1f to %.1f, row sums to %.1f; "
          "median against the site record once %s, summed %s"
          % (by_k.round(2).to_dict(), act_c[["k", "lo"]].corr(method="spearman").iloc[0, 1], act_c.lo.min(),
             act_c.lo.max(), app_kwh.min(), app_kwh.max(), reb_kwh.min(), reb_kwh.max(), (act_c.k * act_c.lo).max(),
             once.round(3).to_dict(), summed.round(3).to_dict()))
    # zero device rows in the main call's population: the call ignores the DER extract and the re-allocation log
    L2 = dict(L, der=L["der"].iloc[0:0], realloc=L["realloc"].iloc[0:0])
    v = C.forecast(L2, base=base, camps=camps, pools=pools)
    ok(abs(v["excess"]["YRB24"] - ex["YRB24"]) < 1e-12, "the call reads an ask file")
    # the main register carries no temporary NMI and no 11-character NMI
    ok(not reg.nmi.isin(temp).any(), "a temporary NMI in the connection register")

    # ---------------------------------------------------------------- distractors: deleting each moves nothing graded
    import tempfile
    meta_d = json.load(open(meta_path))["distractor_files"] if meta_path else list(K.DISTRACTORS)
    for gone in meta_d:
        tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(target)), suffix=".tmp")
        try:
            for f in os.listdir(target):
                if f != gone:
                    os.symlink(os.path.abspath(os.path.join(target, f)), os.path.join(tmp, f))
            L3 = C.load(tmp)
            v = C.forecast(L3)
            ok(graded(v) == graded(fc), "deleting %s moves the call" % gone)
            ok(C.ask_a(L3, "golden") == (ga, gb) and C.ask_b(L3, "golden") == gs, "deleting %s moves an ask" % gone)
        finally:
            import shutil
            shutil.rmtree(tmp)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "%d files" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "largest file %d rows" % big)
    if meta_path:
        meta = json.load(open(meta_path))
        ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "distractors")
    for f in files:
        ok(not re.search(r"distract|decoy|trap|answer|golden|solution", f, re.I), "file name %s" % f)
    man = pd.read_csv(os.path.join(target, K.MANIFEST), dtype=str, keep_default_na=False)
    ok(set(man.owner) - {"Merindah City Council"} <= set(K.PEOPLE.values()), "a manifest owner outside the drawn personas: %s"
       % (set(man.owner) - set(K.PEOPLE.values())))

    # ---------------------------------------------------------------- the pack's own registers (H9) and dates (H16)
    ok(set(man.file) == set(files) - {K.MANIFEST}, "manifest lists %s" % (set(files) ^ set(man.file)))
    import openpyxl
    dwb = openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True)
    dnames = {r[0] for r in dwb["Files"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    ok(dnames == {f for f in files if f.endswith(".csv") and f != K.MANIFEST}, "dictionary files %s" % dnames)
    # the dictionary describes every extract it lists, so it is dated on or after the latest of them, in the manifest
    # and in its own properties alike
    ext = dict(zip(man.file, man.extracted))
    ok(ext[K.DICTIONARY] >= max(ext[f] for f in dnames), "the dictionary (%s) predates an extract it describes"
       % ext[K.DICTIONARY])
    import zipfile
    core = zipfile.ZipFile(os.path.join(target, K.DICTIONARY)).read("docProps/core.xml").decode()
    ok(re.search(r"<dcterms:modified[^>]*>(\d{4}-\d\d-\d\d)", core).group(1) == ext[K.DICTIONARY],
       "the dictionary's properties and the manifest give different dates")
    for r_ in man.itertuples():
        if r_.file.endswith(".csv"):
            df = pd.read_csv(os.path.join(target, r_.file), dtype=str, keep_default_na=False)
            ok(int(r_.rows) == len(df), "manifest rows for %s" % r_.file)
            for col in df.columns:
                if col.endswith("_date") or col in ("first_energised", "last_verified"):
                    vals = df[col][df[col] != ""]
                    ok(vals.max() <= r_.extracted, "%s %s runs to %s after its extract %s" % (r_.file, col, vals.max(), r_.extracted))

    # ---------------------------------------------------------------- realism sweep
    counts = [c["systems"] for c in camps]
    ok(len(set(counts)) == len(counts), "two campaigns installed the same number of systems")
    ok(len(set(c["letterboxed"] for c in camps)) == len(camps), "identical letterbox counts")
    hcs = [L["hca"][f]["hc29"] for f in K.FEEDERS]
    ok(len(set(hcs)) == len(hcs), "two feeders share a hosting capacity")
    ok(sum(abs(h * 10 - round(h * 10)) < 1e-6 for h in hcs) <= 2, "round hosting capacities")
    # the assessment's published 2029 case stands (the call's inputs); its 2026 case moves with each feeder's spring
    # minimum demand at the report's own sensitivity (a 0.5 MW lower minimum, 0.3 to 0.6 MW less hosting capacity),
    # in both directions and by different amounts, never a steady step on every feeder
    for f in K.FEEDERS:
        ok(L["hca"][f]["hc29"] == K.HC29_PUBLISHED[f], "%s 2029 hosting capacity %.2f, published %.2f"
           % (f, L["hca"][f]["hc29"], K.HC29_PUBLISHED[f]))
    hca_txt = pdf_text(os.path.join(target, K.HCA))
    ok("a 0.5 MW lower minimum lowers hosting capacity by 0.3 to 0.6 MW" in hca_txt, "the assessment's sensitivity sentence")
    rows_hc = {m.group(1): tuple(float(m.group(k)) for k in (4, 5, 6, 7)) for m in re.finditer(
        r"(YRB2\d) ([\d.]+) ([\d,]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", hca_txt)}
    ok(set(rows_hc) == set(K.FEEDERS), "the assessment's table rows %s" % sorted(rows_hc))
    steps26 = []
    for f, (m26, m29, h26, h29) in rows_hc.items():
        dm, dh = m26 - m29, h26 - h29
        lo_, hi_ = sorted((0.6 * dm, 1.2 * dm))
        ok(lo_ - 0.0051 <= dh <= hi_ + 0.0051, "%s 2026 case %.2f against minimum demand %.2f to %.2f" % (f, h26, m26, m29))
        steps26.append(dh)
    ok(min(steps26) < 0 < max(steps26) and max(steps26) - min(steps26) >= 0.5 and len({round(x, 2) for x in steps26}) == 8,
       "the 2026 case steps alike on every feeder: %s" % [round(x, 2) for x in steps26])
    for name, vals in (("ask A first", list(ga.values())), ("ask A second", list(gb.values()))):
        ok(max(collections.Counter(vals).values()) <= 2, "%s: three feeders share a count" % name)
    ok(abs(rb["untapped"]["pooled"] * 100 - round(rb["untapped"]["pooled"] * 100)) > 0.05, "a round conversion rate")
    report(L, base, camps, pools, rb, fc)
    print("checks: %d assertions passed (call %s at %.3f MW, runner-up %s at %.3f, gap %.3f; Bindarra %.1f, "
          "Wattleview %.1f systems)" % (N[0], fc["winner"], ex["YRB24"], fc["runner"], ex["YRB22"], fc["gap"],
                                        fc["lift"]["Bindarra Waters"], fc["lift"]["Wattleview"]))
    return N[0]


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    run(t, os.path.join(task, "golden"), meta_path=os.path.join(task, "metadata.json"))
