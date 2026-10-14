"""task136 generator checks (round 2): the call and its bins, the uplift corridor under NPP-114 4.2, the ladder and
every rival route the audit measured, the past campaigns' fit, the three-rules block on the clean truth (R1 to R3c),
every semantic fork row (SF1 to SF26), the closure axes, the four asks' stops, hazards and devices, the distractors,
the input gates and the realism sweep. Run by build.py on the built pack; raises on the first failure and prints the
count of assertions passed."""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import calc as C
import common as K

N = [0]
SF_SEEN = {}
WINDOW_VARIANTS = ("n365", "n730", "n1095", "conn", "all", "rate", "persontime")
GOLD = dict(winner="YRB27", runner="YRB24", excess=1.9, runner_excess=1.4, gap=0.5, bdw=0.4, wtv=1.7)


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N[0] += 1


def r1(x):
    return round(x + 1e-12, 1)


def ten(x):
    return int(round(x / 10.0) * 10)


def bin_room(x, unit):
    """Distance from x to the nearest rounding edge, as a share of the bin (0.5 at the centre)."""
    k = x / unit
    return abs((k - np.floor(k)) - 0.5)


def graded(v):
    w = v["winner"]
    return (w, v["runner"], r1(v["excess"][w]), r1(v["excess"][v["runner"]]), r1(v["gap"]),
            r1(v["add_mw"]["Bindarra Waters"]), r1(v["add_mw"]["Wattleview"]))


def golden_tuple():
    return (GOLD["winner"], GOLD["runner"], GOLD["excess"], GOLD["runner_excess"], GOLD["gap"], GOLD["bdw"], GOLD["wtv"])


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text() or "" for pg in PdfReader(path).pages).split())


def with_base(L, base_kw, lift, avgkw, pools, hc_case="hc29"):
    tot = dict(base_kw)
    add = {}
    for name, n in lift.items():
        f = pools[name]["feeder"]
        tot[f] += n * avgkw[f]
        add[name] = n * avgkw[f] / 1000.0
    ex = {f: tot[f] / 1000.0 - L["hca"][f][hc_case] for f in K.FEEDERS}
    order = sorted(K.FEEDERS, key=lambda f: -ex[f])
    return dict(excess=ex, order=order, winner=order[0], runner=order[1], gap=ex[order[0]] - ex[order[1]], lift=lift,
                add_mw=add, fc=tot)


def summed_capacity(reg, date):
    d = pd.Timestamp(date)
    live = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= d) & (reg.removal_date.isna() | (reg.removal_date > d))]
    return live.groupby("feeder").kw.sum()


def base_with(reg, cap_fn, trend_kw=None, years=K.YEARS_TO_DESIGN, base_date=K.BASE):
    cap = cap_fn(reg, base_date)
    tr = trend_kw if trend_kw is not None else C.trend(reg)[0]
    return {f: cap.get(f, 0.0) + years * tr[f] for f in K.FEEDERS}


# ------------------------------------------------------------------------------------------------------------------
# rival routes the audit names: fitted models on the obvious covariates

def penetration_lift(camps, pools):
    """Each campaign's systems per untapped owner-occupied house regressed on the suburb's PV penetration at the
    opening, then applied to each 2026 suburb's penetration and pool."""
    pen = np.array([1 - c["untapped"] / c["oo"] for c in camps])
    pu = np.array([c["systems"] / c["untapped"] for c in camps])
    b1, b0 = np.polyfit(pen, pu, 1)
    return {n: (b0 + b1 * (1 - p["untapped"] / p["oo"])) * p["untapped"] for n, p in pools.items()}


def covariate_lift(camps, pools, cols=("untapped", "letterboxed", "oo")):
    A = np.array([[1.0] + [c[k] for k in cols] for c in camps])
    y = np.array([c["systems"] for c in camps], float)
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    return {n: float(beta @ np.array([1.0] + [p[k] for k in cols])) for n, p in pools.items()}


def backcast_miss(camps, basis, estimator="pooled"):
    rr = C.rate_of(camps, basis, estimator)
    if basis == "count":
        pred = [rr["slope"]] * len(camps)
    else:
        pred = [rr["slope"] * C.denominator(c, basis) + rr["icpt"] for c in camps]
    miss = [abs(p - c["systems"]) / c["systems"] for p, c in zip(pred, camps)]
    i = int(np.argmax(miss))
    return miss[i], camps[i]["key"]


# ------------------------------------------------------------------------------------------------------------------
# the clean truth: the world before any file is written (dataset-generation 7.1)

def truth(W):
    """Connected capacity, trend, the FY2025-26 average, the seven campaigns and the 2026 suburbs, from the world's
    own records (no file, no join): the quantities every route is built from."""
    nmi_feeder = {n["nmi"]: n["feeder"] for n in W.nmis}
    apps = list(W.apps)

    def cap(date):
        latest = {}
        for a in apps:
            if a["status"] in ("Connected", "Removed") and a["connected"] and a["connected"] <= date and \
                    not (a.get("removed") and a["removed"] <= date):
                k = (a["connected"], 0 if a["type"] == "Alteration" else 1)
                if a["nmi"] not in latest or k > latest[a["nmi"]][0]:
                    latest[a["nmi"]] = (k, a["kw"])
        out = collections.defaultdict(float)
        for n, (_, kw) in latest.items():
            if n in nmi_feeder:
                out[nmi_feeder[n]] += kw
        return out

    c0 = cap(K.BASE)
    yearly = collections.defaultdict(list)
    for s, e in K.TREND_FYS:
        c1, cb = cap(e), cap(s - dt.timedelta(days=1))
        prog = collections.defaultdict(float)
        for a in apps:
            if a["program"] and a["type"] == "New" and a["status"] in ("Connected", "Removed") and s <= a["connected"] <= e \
                    and a["nmi"] in nmi_feeder:
                prog[nmi_feeder[a["nmi"]]] += a["kw"]
        for f in K.FEEDERS:
            yearly[f].append(c1[f] - cb[f] - prog[f])
    trend = {f: float(np.mean(yearly[f])) for f in K.FEEDERS}
    base = {f: c0[f] + K.YEARS_TO_DESIGN * trend[f] for f in K.FEEDERS}
    s, e = K.LAST_FY
    by = collections.defaultdict(list)
    for a in apps:
        if a["type"] == "New" and a["status"] in ("Connected", "Removed") and s <= a["connected"] <= e and a["nmi"] in nmi_feeder:
            by[nmi_feeder[a["nmi"]]].append(a["kw"])
    avgkw = {f: float(np.mean(v)) for f, v in by.items()}
    first = {}
    for a in apps:
        if a["status"] != "Withdrawn" and (a["nmi"] not in first or a["received"] < first[a["nmi"]]):
            first[a["nmi"]] = a["received"]

    def suburb(name, opening):
        oo = [p for p in W.props if p["kind"] == "house_oo" and p["locality"] == name]
        nm = [p["nmis"][0]["nmi"] for p in oo]
        n365 = sum(1 for n in nm if n in first and opening - dt.timedelta(days=365) <= first[n] < opening)
        untapped = sum(1 for n in nm if not (n in first and first[n] < opening))
        letter = sum(1 for n in W.nmis if n["locality"] == name and n["tariff"] == "Residential")
        return dict(oo=len(oo), n365=n365, untapped=untapped, letterboxed=letter,
                    feeder=[l["feeder"] for l in K.LOCALITIES if l["name"] == name][0])

    camps = []
    for c in K.CAMPAIGNS:
        st = suburb(c["suburb"], c["open"])
        ref = "SS-%s-%s" % (c["key"][-2:], c["key"][:3])
        st.update(key=c["key"], systems=sum(1 for a in apps if a["program"] == ref and a["type"] == "New"
                                            and a["status"] in ("Connected", "Removed")))
        camps.append(st)
    pools = {c["suburb"]: dict(suburb(c["suburb"], c["open"]), key=c["key"]) for c in K.CAMPAIGNS_2026}
    return dict(cap=c0, trend=trend, base=base, avgkw=avgkw, camps=camps, pools=pools)


def truth_route(T, L, basis):
    rate = sum(c["systems"] for c in T["camps"]) / sum(c[basis if basis != "uplift" else "n365"] for c in T["camps"])
    lift = {n: rate * p[basis if basis != "uplift" else "n365"] for n, p in T["pools"].items()}
    return with_base(L, T["base"], lift, T["avgkw"], T["pools"])


# ------------------------------------------------------------------------------------------------------------------

def run(target, golden, W=None, meta_path=None):
    N[0] = 0
    SF_SEEN.clear()
    L = C.load(target)
    reg = L["reg"]
    base = C.base_forecast(reg)
    camps = C.campaigns(L)
    pools = C.pools_2026(L)
    fc = C.forecast(L, base=base, camps=camps, pools=pools)
    ex = fc["excess"]
    files = sorted(os.listdir(target))
    npp = pdf_text(os.path.join(target, K.NPP))
    letter = pdf_text(os.path.join(target, K.LETTER))
    hca_txt = pdf_text(os.path.join(target, K.HCA))
    figs_path = os.path.join(os.path.dirname(os.path.abspath(target)), "generator", "figures.json")
    figs = json.load(open(figs_path)) if os.path.exists(figs_path) else None

    # ---------------------------------------------------------------- the call
    ok(graded(fc) == golden_tuple(), "golden %s" % (graded(fc),))
    ok(abs(r1(fc["gap"]) - (r1(ex["YRB27"]) - r1(ex["YRB24"]))) < 1e-9, "SF22 gap equals the rounded difference")
    ok(ex["YRB27"] / ex["YRB24"] >= 1.20, "golden margin %.3f" % (ex["YRB27"] / ex["YRB24"]))
    ok(ex["YRB24"] - ex[fc["order"][2]] >= 0.10, "the runner-up within 0.1 MW of third (%s)" % fc["order"][2])
    for x, name in ((ex["YRB27"], "excess"), (ex["YRB24"], "runner-up excess"), (fc["gap"], "gap"),
                    (fc["add_mw"]["Bindarra Waters"], "Bindarra Waters MW"), (fc["add_mw"]["Wattleview"], "Wattleview MW")):
        ok(bin_room(x, 0.1) >= 0.30, "%s %.4f too near a rounding edge" % (name, x))
    if figs:
        cf = figs["call"]
        ok((cf["feeder"], cf["runner_up"], float(cf["excess_mw"]), float(cf["runner_up_excess_mw"]), float(cf["gap_mw"]),
            float(cf["bindarra_waters_mw"]), float(cf["wattleview_mw"])) == golden_tuple(), "figures.json call block")

    # ---------------------------------------------------------------- NPP-114 4.2 and the uplift corridor (SF11 to SF13, SF25)
    ok("A rate taken from past programs is their total systems divided by their combined total of the quantity the "
       "rate is expressed per." in npp, "NPP-114 4.2 pooled-rate sentence missing")
    ok("first application" not in npp.lower() and "uptake" not in npp.lower() and "letterbox" not in npp.lower(),
       "NPP-114 names a basis")
    band = {}
    for var in WINDOW_VARIANTS:
        v = C.forecast(L, basis="uplift", estimator="pooled", variant=var, base=base, camps=camps, pools=pools)
        band[var] = v
        ok(graded(v) == golden_tuple(), "uplift %s moves a graded figure: %s" % (var, graded(v)))
    for k, getter in (("excess", lambda v: v["excess"]["YRB27"]), ("gap", lambda v: v["gap"]),
                      ("runner_excess", lambda v: v["excess"]["YRB24"]),
                      ("bdw", lambda v: v["add_mw"]["Bindarra Waters"]), ("wtv", lambda v: v["add_mw"]["Wattleview"])):
        vals = [getter(v) for v in band.values()]
        lo, hi = min(vals), max(vals)
        centre = GOLD[k]
        ok(lo - (centre - 0.05) >= 0.008 and (centre + 0.05) - hi >= 0.008,
           "uplift corridor for %s %.3f to %.3f sits within 0.008 of a bin edge" % (k, lo, hi))
        SF_SEEN["corridor %s" % k] = (round(lo, 3), round(hi, 3))
    # the estimators NPP-114 4.2 rules out, recorded (a mean, median or regression on the rates)
    for est in ("mean", "median", "origin", "ols"):
        vals = [C.forecast(L, basis="uplift", estimator=est, variant=var, base=base, camps=camps, pools=pools)
                for var in WINDOW_VARIANTS]
        ok(all(v["winner"] == "YRB27" and v["runner"] == "YRB24" for v in vals), "SF15 estimator %s moves the call" % est)
        SF_SEEN["SF15 %s" % est] = (round(min(v["excess"]["YRB27"] for v in vals), 3),
                                    round(max(v["excess"]["YRB27"] for v in vals), 3))

    # ---------------------------------------------------------------- the past campaigns: the uplift alone fits
    rr = {b: C.rate_of(camps, b) for b in C.BASES}
    up = rr["uplift"]
    ok(0.06 <= up["cv"] <= 0.12, "uplift spread %.3f outside a measured regularity's 0.06 to 0.12" % up["cv"])
    ks = up["values"]
    ok(len(set(np.round(ks, 3))) == len(ks), "two campaigns share a rate")
    ok(min(ks) <= 1.06 and max(ks) >= 1.30, "the seven rates scatter %.3f to %.3f" % (min(ks), max(ks)))
    for b in ("count", "letterboxed", "oo", "udw", "feeder_unt", "untapped"):
        ok(rr[b]["cv"] >= 5 * up["cv"], "basis %s fits within five times the uplift's spread (%.3f)" % (b, rr[b]["cv"]))
        miss, key = backcast_miss(camps, b)
        ok(miss >= 0.40, "basis %s back-casts every campaign within %.2f" % (b, miss))
        SF_SEEN["fit %s" % b] = (round(rr[b]["cv"], 3), round(miss, 3), key)
    # SF16 to SF20: the refused transfer bases, each priced by the records (the seven campaigns' spread and worst
    # back-cast miss) and each filing a wrong feeder (the rivals below)
    for sf, b in (("SF16", "letterboxed"), ("SF17", "oo"), ("SF18", "untapped"), ("SF19", "udw"), ("SF19", "feeder_unt"),
                  ("SF20", "count")):
        miss, key = backcast_miss(camps, b)
        ok(rr[b]["cv"] >= 5 * up["cv"] and miss >= 0.40, "%s basis %s fits the seven campaigns" % (sf, b))
    miss_u, _ = backcast_miss(camps, "uplift")
    ok(miss_u <= 0.16, "the uplift misses a campaign by %.3f" % miss_u)
    SF_SEEN["fit uplift"] = (round(up["cv"], 3), round(miss_u, 3))
    for c in camps:
        ok(c["systems_log"] == c["systems"], "%s log %d register %d" % (c["key"], c["systems_log"], c["systems"]))
        ok(c["letterboxed"] == c["res_nmis"], "%s letterboxed %d residential NMIs %d" % (c["key"], c["letterboxed"], c["res_nmis"]))
    for name, p in pools.items():
        ok(p["letterboxed"] == p["res_nmis"], "%s letter %d NMIs %d" % (name, p["letterboxed"], p["res_nmis"]))
    # the decisive contrast is in the data: Wattleview's uptake against Bindarra Waters' pool
    pb, pw = pools["Bindarra Waters"], pools["Wattleview"]
    ok(pw["n365"] / pb["n365"] >= 1.2 * pb["untapped"] / pw["untapped"], "dominance: uptake ratio %.2f, pool ratio %.2f"
       % (pw["n365"] / pb["n365"], pb["untapped"] / pw["untapped"]))
    ok(pb["untapped"] > 1.5 * pw["untapped"] and pb["letterboxed"] > pw["letterboxed"], "Bindarra Waters' pool is not the larger")
    SF_SEEN["dominance"] = (round(pw["n365"] / pb["n365"], 2), round(pb["untapped"] / pw["untapped"], 2))

    # ---------------------------------------------------------------- the ladder and every rival route
    rungs = {"R0 per home letterboxed (default path)": C.forecast(L, basis="letterboxed", base=base, camps=camps, pools=pools),
             "R1 per owner-occupied house without PV at the opening (the reflex)":
                 C.forecast(L, basis="untapped", base=base, camps=camps, pools=pools)}
    r0, r1_ = rungs.values()
    ok(r0["winner"] == "YRB24" and r0["excess"]["YRB24"] / r0["excess"][r0["runner"]] >= 1.15, "R0 files %s at margin %.3f"
       % (r0["winner"], r0["excess"]["YRB24"] / r0["excess"][r0["runner"]]))
    ok(r1(r0["excess"]["YRB24"]) != GOLD["excess"] and r1(r0["gap"]) != GOLD["gap"], "R0's figures coincide with the golden's")
    ok(r0["order"].index("YRB27") + 1 in (4, 5), "R0 places YRB27 %d" % (r0["order"].index("YRB27") + 1))
    ok(r1_["winner"] == "YRB24" and r1_["excess"]["YRB24"] / r1_["excess"][r1_["runner"]] >= 1.15, "R1 files %s at margin %.3f"
       % (r1_["winner"], r1_["excess"]["YRB24"] / r1_["excess"][r1_["runner"]]))
    ok(r1_["order"].index("YRB27") + 1 >= 2 and r1_["excess"]["YRB24"] / r1_["excess"]["YRB27"] >= 1.20,
       "R1 places YRB27 within 1.20 of the top")
    ok(r1_["runner"] != GOLD["runner"] and r0["runner"] != GOLD["runner"], "a rung's runner-up is the golden's")
    if figs:
        ok(figs["default_path"]["feeder"] == "YRB24" and figs["reflex_path"]["feeder"] == "YRB24", "figures.json rungs")
    rivals = {}
    for b in ("none", "count", "letterboxed", "oo", "udw", "feeder_unt", "untapped"):
        for est in (("pooled",) if b in ("none", "count") else ("pooled", "mean", "median", "origin", "ols")):
            rivals["%s %s" % (b, est)] = C.forecast(L, basis=b, estimator=est, base=base, camps=camps, pools=pools)
    rivals["penetration regression"] = C.forecast(L, lift=penetration_lift(camps, pools), base=base, camps=camps, pools=pools)
    rivals["regression on pool, letterboxed and owner-occupied"] = C.forecast(L, lift=covariate_lift(camps, pools),
                                                                              base=base, camps=camps, pools=pools)
    rivals["regression on pool and letterboxed"] = C.forecast(
        L, lift=covariate_lift(camps, pools, ("untapped", "letterboxed")), base=base, camps=camps, pools=pools)
    for key in ("TWR21", "PBG24", "BNR23"):
        an = [c for c in camps if c["key"] == key][0]
        for b in ("letterboxed", "oo", "untapped"):
            lf = {n: an["systems"] / an[b] * p[b] for n, p in pools.items()}
            rivals["%s analog per %s" % (key, b)] = C.forecast(L, lift=lf, base=base, camps=camps, pools=pools)
    sf_of = {"letterboxed pooled": "SF16", "oo pooled": "SF17", "untapped pooled": "SF18", "udw pooled": "SF19",
             "feeder_unt pooled": "SF19", "count pooled": "SF20", "penetration regression": "SF20",
             "regression on pool, letterboxed and owner-occupied": "SF20"}
    for name, sf in sf_of.items():
        ok(rivals[name]["winner"] == "YRB24", "%s %s files %s" % (sf, name, rivals[name]["winner"]))
    for name, v in rivals.items():
        ok(v["winner"] != "YRB27", "rival %s lands the call" % name)
        ok(v["excess"][v["winner"]] - v["excess"]["YRB27"] >= 0.10, "rival %s keeps YRB27 within 0.1 MW (%.3f)"
           % (name, v["excess"][v["winner"]] - v["excess"]["YRB27"]))
        g = graded(v)
        ok(g[5] != GOLD["bdw"] or g[6] != GOLD["wtv"], "rival %s lands both bulk-buy figures" % name)
        SF_SEEN["rival " + name] = (v["winner"], round(v["excess"][v["winner"]], 3), round(v["excess"]["YRB27"], 3))
    ok(rivals["letterboxed pooled"]["winner"] == "YRB24" and rivals["untapped pooled"]["winner"] == "YRB24",
       "the default path and the reflex")
    ok(sum(1 for v in rivals.values() if v["runner"] == GOLD["runner"] and r1(v["excess"][GOLD["runner"]]) == GOLD["runner_excess"]) == 0,
       "a rival files the golden's runner-up and its figure")

    # ---------------------------------------------------------------- the three rules, executed (dataset-generation 7.1)
    heads = " ".join(open(os.path.join(target, f), encoding="utf-8").readline().lower() for f in files if f.endswith(".csv"))
    ok(not re.search(r"first_app|uptake|adoption|untapped|participation|per_letterbox|campaign_rate", heads),
       "R1: a shipped column holds the deciding quantity")
    ok({"received_date", "status", "application_type", "nmi"} <= set(reg.columns) and
       {"land_use_code", "rating_category", "locality"} <= set(L["rates"].columns) and len(L["xref"]) > 40000,
       "R1: the register's application rows, the rates roll and the cross-reference ship at their own grain")
    import openpyxl
    wbp = openpyxl.load_workbook(os.path.join(target, K.PROGRAM_LOG), read_only=True)
    plog_txt = " ".join(str(c) for ws in wbp.worksheets for row in ws.iter_rows(values_only=True) for c in row if c)
    ok(not re.search(r"first application|uptake|per cent of|participation rate|expect", (plog_txt + " " + letter).lower()),
       "R1: the council's files state a rate, an uptake or an expectation")
    if W is not None:
        T = truth(W)
        # R2: the mess on the call's path (application grain with alterations, withdrawn and unconnected rows, removals,
        # migrated rows with inverters in the legacy table, feeder at application after load transfers, the rates roll
        # joined through the GIS cross-reference, the council's workbook layout), read by the filed rules and the
        # dictionary, gives back the world's own figures
        for f in K.FEEDERS:
            ok(abs(base["cap"].get(f, 0.0) - T["cap"][f]) < 1e-6, "R2: %s connected capacity %.3f, truth %.3f"
               % (f, base["cap"].get(f, 0.0), T["cap"][f]))
            ok(abs(base["trend"][f] - T["trend"][f]) < 1e-6, "R2: %s trend differs from the truth" % f)
        ok(all(abs(fc["avgkw"][f] - T["avgkw"][f]) < 1e-9 for f in K.FEEDERS), "R2: the FY2025-26 averages differ")
        for c, t in zip(camps, T["camps"]):
            got = (c["systems"], c["n365"], c["untapped"], c["letterboxed"], c["oo"])
            want = (t["systems"], t["n365"], t["untapped"], t["letterboxed"], t["oo"])
            ok(got == want, "R2: %s read from the pack %s, truth %s" % (c["key"], got, want))
            ok(t["n365"] == W.camp_n12[c["key"]] and t["systems"] == W.camp_systems[c["key"]],
               "R2: %s the simulation's own counts" % c["key"])
        for name, p in pools.items():
            t = T["pools"][name]
            ok((p["n365"], p["untapped"], p["letterboxed"], p["oo"]) == (t["n365"], t["untapped"], t["letterboxed"], t["oo"]),
               "R2: %s read from the pack differs from the truth" % name)
        # R3a: the easy route on the clean truth, every filed rule applied (NPP-114 2.2 to 7.1, the pooled rate of 4.2),
        # files the default path's wrong answer; the textbook reflex files the other
        t0 = truth_route(T, L, "letterboxed")
        ok(graded(t0) == graded(rivals["letterboxed pooled"]) and t0["winner"] == "YRB24",
           "R3a: the per-letterbox route on the clean truth files %s" % (graded(t0),))
        t1 = truth_route(T, L, "untapped")
        ok(graded(t1) == graded(rivals["untapped pooled"]) and t1["winner"] == "YRB24",
           "R3a: the reflex on the clean truth files %s" % (graded(t1),))
        ok(truth_route(T, L, "oo")["winner"] != "YRB27", "R3a: per owner-occupied house on the clean truth lands the call")
        # R3b: the same route with only the decisive step changed (the yield carried on the suburb's own uptake)
        # files the golden
        tg = truth_route(T, L, "uplift")
        ok(graded(tg) == golden_tuple(), "R3b: the uplift on the clean truth files %s" % (graded(tg),))
        SF_SEEN["R3 truth"] = (graded(t0), graded(t1), graded(tg))
    # R3c: nothing planted
    ok(not any(w in f.lower() for f in files for w in ("memo", "draft", "briefing", "estimate")),
       "R3c: a memo, draft, briefing or estimate ships")
    docs_txt = " ".join(pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf"))
    ok(not re.search(r"\b\d+ systems\b|\bsystems per\b|\bper cent of (?:the )?(?:homes|houses|households)\b", docs_txt),
       "R3c: a filed document states a campaign forecast or a rate")
    ok("excess" not in hca_txt.lower() and "headroom" not in hca_txt.lower() and "rank" not in hca_txt.lower(),
       "R3c: the assessment ranks the feeders or states an excess")

    # ---------------------------------------------------------------- the semantic fork rows
    def variant(base_kw=None, avgkw=None, lift=None, camps_=None, pools_=None, hc_case="hc29"):
        cc = camps_ or camps
        pp = pools_ or pools
        lf = lift if lift is not None else C.lifts(cc, pp, "uplift")
        return with_base(L, base_kw if base_kw is not None else base["base"], lf,
                         avgkw if avgkw is not None else fc["avgkw"], pp, hc_case)

    # SF1 residential NMIs only
    res = set(L["net"][L["net"].tariff_class == "Residential"].nmi)
    reg_res = reg[reg.nmi.isin(res)]
    v = variant(base_kw=base_with(reg_res, C.connected_kw, C.trend(reg_res)[0]))
    ok(graded(v) != golden_tuple(), "SF1 residential only keeps every figure")
    SF_SEEN["SF1 residential only"] = graded(v)
    ok("at a residential or business NMI" in npp, "SF1 NPP-114 2.1 no longer names business NMIs")
    ok(reg.kw.max() <= 30.0, "SF1 a register system above 30 kVA (%.1f)" % reg.kw.max())
    # SF2 alterations summed; panel capacity
    tr2 = {}
    for f in K.FEEDERS:
        vals = []
        for s, e in K.TREND_FYS:
            c1, c0 = summed_capacity(reg, e), summed_capacity(reg, s - dt.timedelta(days=1))
            vals.append(c1.get(f, 0) - c0.get(f, 0) - C.program_kw(reg, s, e).get(f, 0))
        tr2[f] = float(np.mean(vals))
    v = variant(base_kw=base_with(reg, summed_capacity, tr2))
    ok(graded(v) != golden_tuple(), "SF2 summed alterations keeps every figure")
    ok("An alteration replaces the configuration it alters." in npp, "SF2 NPP-114 2.2 alteration sentence missing")
    SF_SEEN["SF2 summed"] = graded(v)
    reg_p = reg.assign(kw=reg.panel_kwp.replace("", np.nan).astype(float))
    v = variant(base_kw=base_with(reg_p, C.connected_kw, C.trend(reg_p)[0]), avgkw=C.avg_new_kw(reg_p))
    ok(graded(v) != golden_tuple(), "SF2 panel capacity keeps every figure")
    ok("inverter capacity (kW, AC rating)" in npp, "SF2 NPP-114 2.2 inverter capacity sentence missing")
    SF_SEEN["SF2 panel"] = graded(v)
    # SF3 migrated rows dropped
    reg_m = reg[reg.legacy_application_no == ""]
    v = variant(base_kw=base_with(reg_m, C.connected_kw, C.trend(reg_m)[0]))
    SF_SEEN["SF3 migrated dropped"] = graded(v)
    ok(graded(v) != golden_tuple(), "SF3 dropping the migrated rows keeps every figure")
    kw_def = [r_[1] for r_ in openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True)
              ["Connections register"].iter_rows(values_only=True) if r_ and r_[0] == "inverter_kw_ac"]
    ok(len(kw_def) == 1 and "Blank on applications migrated from the legacy system." in kw_def[0],
       "SF3 the dictionary no longer says where the migrated inverters are")
    reg_pk = reg.assign(kw=np.where(reg.legacy_application_no != "", reg.panel_kwp.replace("", np.nan).astype(float), reg.kw))
    v = variant(base_kw=base_with(reg_pk, C.connected_kw, C.trend(reg_pk)[0]))
    SF_SEEN["SF3 migrated at panel capacity"] = graded(v)
    # SF23 the legacy join is one to one
    leg = L["leg"]
    regl = reg[reg.legacy_application_no != ""]
    ok(leg.legacy_application_no.is_unique and regl.legacy_application_no.is_unique and
       set(regl.legacy_application_no) == set(leg.legacy_application_no), "SF23 the legacy numbers do not pair one to one")
    # SF4 approved but not connected counted
    reg4 = reg.copy()
    m = reg4.status.isin(["Approved"])
    reg4.loc[m, "status"] = "Connected"
    reg4.loc[m, "connection_date"] = reg4.loc[m, "approved_date"]
    b4 = base_with(reg4, C.connected_kw, C.trend(reg)[0])
    v = variant(base_kw=b4)
    ok(v["winner"] == "YRB27", "SF4 files %s" % v["winner"])
    ok(max(abs(b4[f] / base["base"][f] - 1) for f in K.FEEDERS) < 0.02, "SF4 moves a base by 2 per cent or more")
    SF_SEEN["SF4 approved counted"] = graded(v)
    # SF5 the feeder recorded on the application
    reg5 = reg.assign(feeder=reg.feeder_at_application)
    v = variant(base_kw=base_with(reg5, C.connected_kw, C.trend(reg5)[0]))
    ok(v["winner"] == "YRB27", "SF5 feeder at application files %s" % v["winner"])
    SF_SEEN["SF5 feeder at application"] = graded(v)
    # SF6 base date 30 June 2026
    v = variant(base_kw=base_with(reg, C.connected_kw, base_date=dt.date(2026, 6, 30)))
    ok(v["winner"] == "YRB27", "SF6 files %s" % v["winner"])
    SF_SEEN["SF6 30 June"] = graded(v)
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
        v = variant(base_kw=base_with(reg, C.connected_kw, trv))
        ok(v["winner"] == "YRB27", "SF7 %s files %s" % (name, v["winner"]))
        SF_SEEN["SF7 " + name] = graded(v)
    # SF8 3.25 or 2.92 years
    for yrs in (3.25, 2.92):
        v = variant(base_kw=base_with(reg, C.connected_kw, years=yrs))
        ok(v["winner"] == "YRB27", "SF8 %.2f years files %s" % (yrs, v["winner"]))
        SF_SEEN["SF8 %.2f years" % yrs] = graded(v)
    # SF9 contracts instead of systems installed
    contracts = {r_["Suburb"]: int(r_["Contracts signed"]) for r_ in L["log"]}
    camps9 = [dict(c, systems=contracts[c["suburb"]]) for c in camps]
    v = variant(camps_=camps9)
    ok(v["winner"] == "YRB27", "SF9 contracts files %s" % v["winner"])
    SF_SEEN["SF9 contracts"] = graded(v)
    # SF10 program systems at the past campaigns' own average size
    prog_kw = sum(c["kw_program"] for c in camps) / sum(c["systems"] for c in camps)
    v = variant(avgkw={f: prog_kw for f in K.FEEDERS})
    ok(v["winner"] == "YRB27", "SF10 files %s" % v["winner"])
    SF_SEEN["SF10 past program size %.2f kW" % prog_kw] = graded(v)
    ok("average inverter capacity of the micro EG systems first connected on that feeder in the last complete "
       "financial year" in npp, "SF10 NPP-114 4.3 sentence missing")
    # SF26 the PV a bulk-buy adds: its systems at the feeder's FY2025-26 average inverter capacity, in MW
    for name, p in pools.items():
        ok(abs(fc["add_mw"][name] - fc["lift"][name] * fc["avgkw"][p["feeder"]] / 1000.0) < 1e-12, "SF26 %s" % name)
    # SF11 a first application dated by connection; SF12 all residential addresses; SF13 the window; SF25 hazard forms
    for sf, var in (("SF11", "conn"), ("SF12", "all"), ("SF13", "n730"), ("SF13", "n1095"), ("SF25", "rate"),
                    ("SF25", "persontime")):
        SF_SEEN["%s %s" % (sf, var)] = graded(band[var])
    # SF14 a suburb by the network model's locality: the same NMIs
    for c in camps + list(pools.values()):
        r_, nm = C.houses(L["rates"], L["xref"], c["suburb"])
        net_loc = set(L["net"][L["net"].locality.str.upper() == c["suburb"].upper()].nmi)
        ok(set(nm.nmi) <= net_loc, "SF14 %s rates-roll houses outside the network model's locality" % c["suburb"])
    # SF21 the 2026 case
    v = C.forecast(L, base=base, camps=camps, pools=pools, hc_case="hc26")
    ok(graded(v) != golden_tuple(), "SF21 the 2026 case keeps every figure")
    ok("the figure in the current hosting capacity assessment for the design year's spring minimum-demand case" in npp
       and "Design point: 31 August of the design year" in npp, "SF21 NPP-114 5.1 or 2.4 sentence missing")
    SF_SEEN["SF21 the 2026 case"] = graded(v)
    # SF24 a withdrawn application read as a first application
    first_any = reg.groupby("nmi").received_date.min()
    first_ok = C.first_app(reg)

    def n365_with(first, name, opening):
        nm = set(C.houses(L["rates"], L["xref"], name)[1].nmi)
        op = pd.Timestamp(opening)
        return C.uptake(first, nm, op - pd.Timedelta(days=365), op)
    campsW = [dict(c, n365=n365_with(first_any, c["suburb"], c["opening"])) for c in camps]
    poolsW = {n: dict(p, n365=n365_with(first_any, n, p["opening"])) for n, p in pools.items()}
    v = variant(lift=C.lifts(campsW, poolsW, "uplift"), camps_=campsW, pools_=poolsW)
    ok(v["winner"] == "YRB27", "SF24 withdrawn as a first application files %s" % v["winner"])
    SF_SEEN["SF24 withdrawn counted"] = graded(v)
    wbd = openpyxl.load_workbook(os.path.join(target, K.DICTIONARY), read_only=True)
    sdef = [r_[1] for r_ in wbd["Connections register"].iter_rows(values_only=True) if r_ and r_[0] == "status"]
    ok(len(sdef) == 1 and "nothing was connected under the application." in sdef[0], "SF24 the dictionary's Withdrawn")

    # ---------------------------------------------------------------- closure axes
    pend = reg[(reg.program_ref != "") & reg.status.isin(["Approved", "Under assessment"])]
    ok(len(pend) == 0, "closure 12: program systems pending at the base date")
    ok(not reg.program_ref.str.startswith("SS-26").any(), "closure 22: a 2026 program reference already lodged")
    for c in camps:
        ref = "SS-%s-%s" % (c["key"][-2:], c["key"][:3])
        conn = reg[(reg.program_ref == ref) & reg.status.isin(C.CONNECTED)].connection_date
        if pd.Timestamp(c["opening"]) >= pd.Timestamp(K.TREND_FYS[0][0]):
            ok(len({K.fy_of(x.date()) for x in conn}) == 1, "closure 3: %s program systems span financial years" % c["key"])
        ok((conn - pd.Timestamp(c["opening"])).dt.days.max() <= 270, "closure 3: %s connection lag" % c["key"])
    g0 = golden_tuple()
    ok((reg.connection_date == pd.Timestamp(K.BASE)).sum() > 0, "closure 9: no connection on the base date to test")
    v = variant(base_kw=base_with(reg, C.connected_kw, base_date=K.BASE - dt.timedelta(days=1)))
    ok(graded(v) == g0, "closure 9: base date read exclusively")
    late = [(s_ + dt.timedelta(days=1), e_ + dt.timedelta(days=1)) for s_, e_ in K.TREND_FYS]
    v = variant(base_kw=base_with(reg, C.connected_kw, C.trend(reg, fys=late)[0]))
    ok(graded(v) == g0, "closure 9: financial years a day late")
    on_day = 0
    camps9b, pools9b = [], {}
    for c in camps:
        nm = set(C.houses(L["rates"], L["xref"], c["suburb"])[1].nmi)
        f_ = first_ok[first_ok.index.isin(nm)]
        op = pd.Timestamp(c["opening"])
        on_day += int(f_.eq(op).sum() + f_.eq(op - pd.Timedelta(days=365)).sum())
        camps9b.append(dict(c, n365=int(((f_ > op - pd.Timedelta(days=365)) & (f_ <= op)).sum())))
    for n, p in pools.items():
        nm = set(C.houses(L["rates"], L["xref"], n)[1].nmi)
        f_ = first_ok[first_ok.index.isin(nm)]
        op = pd.Timestamp(p["opening"])
        pools9b[n] = dict(p, n365=int(((f_ > op - pd.Timedelta(days=365)) & (f_ <= op)).sum()))
    ok(on_day > 0, "closure 9: no first application on a window edge to test")
    ok(graded(variant(lift=C.lifts(camps9b, pools9b, "uplift"), camps_=camps9b, pools_=pools9b)) == g0,
       "closure 9: the window read (open, close]")
    SF_SEEN["closure 9 window edges"] = on_day
    shuffled = dict(L, reg=reg.sample(frac=1.0, random_state=7).reset_index(drop=True))
    v = C.forecast(shuffled, base=C.base_forecast(shuffled["reg"]), camps=C.campaigns(shuffled), pools=C.pools_2026(shuffled))
    ok(abs(v["excess"]["YRB27"] - ex["YRB27"]) < 1e-9, "closure 14 row order")
    xr = L["xref"].merge(L["rates"][["property_no", "locality"]], on="property_no")
    multi = xr.groupby("property_no").nmi.count()
    sub = {c["suburb"].upper() for c in K.CAMPAIGNS} | {c["suburb"].upper() for c in K.CAMPAIGNS_2026}
    ok(not xr[xr.property_no.isin(multi[multi > 1].index)].locality.isin(sub).any(), "closure 15 dual occupancy in a campaign suburb")
    ok(reg.nmi.str.len().eq(10).all() and L["net"].nmi.str.len().eq(10).all() and L["xref"].nmi.str.len().eq(10).all(),
       "closure 16 NMI formats on the main path")
    ok(ex[fc["order"][0]] - ex[fc["order"][1]] > 0.1, "closure 11")
    for c in K.CAMPAIGNS_2026:
        ok(c["open"] == K.BASE + dt.timedelta(days=1), "closure 4: a 2026 opening is not the day after the base date")
    ok("1 September 2026" in letter and "27 November 2026" in letter, "closure 22 the letter's sign-up dates")

    # ---------------------------------------------------------------- the asks
    asks = {"D sites": (C.ask_d, ("stamp", "connections", "no_map", "raw"), False),
            "A first lodged": (C.ask_a, ("active_first", "no_map", "raw"), False),
            "B storage": (C.ask_b, ("once", "rows", "stamp", "no_map"), True),
            "C inverter": (C.ask_c, ("once", "rows", "dedupe", "stamp", "no_map"), True)}
    primary = {"D sites": ("stamp",), "A first lodged": ("active_first",), "B storage": ("once", "rows"),
               "C inverter": ("once", "rows", "dedupe")}
    gold_asks = {}
    for name, (fn, modes, tens) in asks.items():
        g = fn(L)
        gold_asks[name] = g
        key = ten if tens else (lambda x: x)
        for m in modes:
            v = fn(L, m)
            hits = sum(key(v[f]) == key(g[f]) for f in K.FEEDERS)
            if m in primary[name]:
                ok(hits == 0, "ask %s primary stop %s lands %d feeders" % (name, m, hits))
            else:
                ok(hits <= 5, "ask %s hazard %s lands %d feeders" % (name, m, hits))
            SF_SEEN["ask %s %s misses" % (name, m)] = 8 - hits
        if tens:
            for f in K.FEEDERS:
                ok(bin_room(g[f], 10) >= 0.07, "ask %s %s %.2f too near a rounding edge" % (name, f, g[f]))
        ok(max(collections.Counter(g.values()).values()) <= 2, "ask %s: three feeders share a figure" % name)
    ok(all(C.ask_a(L, "stamp")[f] == gold_asks["A first lodged"][f] for f in K.FEEDERS),
       "ask A: the feeder stamp moves a site first lodged after the last transfer")
    if figs:
        for f in K.FEEDERS:
            d = figs["der"][f]
            ok((d["active_sites"], d["first_lodged_fy2025_26"], int(d["inverter_kw"].replace(",", "")),
                int(d["storage_kwh"].replace(",", ""))) == (gold_asks["D sites"][f], gold_asks["A first lodged"][f],
                                                             ten(gold_asks["C inverter"][f]), ten(gold_asks["B storage"][f])),
               "figures.json DER row %s" % f)
    # the asks' answers against the world
    if W is not None:
        tsites, tfirst = collections.Counter(), collections.Counter()
        tinv, tbat = collections.defaultdict(float), collections.defaultdict(float)
        by_site = collections.defaultdict(list)
        for s in W.der_systems:
            by_site[s["perm"]].append(s)
        nmi_by = {n["nmi"]: n for n in W.nmis}
        for perm, ss in by_site.items():
            act_s = [s for s in ss if s["status"] == "Active"]
            if not act_s or perm not in nmi_by:
                continue
            f = nmi_by[perm]["feeder"]
            tsites[f] += 1
            if K.LAST_FY[0] <= min(s["registered"] for s in ss) <= K.LAST_FY[1]:
                tfirst[f] += 1
            for s in act_s:
                tinv[f] += s["kw"]
                tbat[f] += s["storage"]
        ok(all(tsites[f] == gold_asks["D sites"][f] for f in K.FEEDERS), "ask D against the world")
        ok(all(tfirst[f] == gold_asks["A first lodged"][f] for f in K.FEEDERS), "ask A against the world")
        ok(all(abs(tinv[f] - gold_asks["C inverter"][f]) < 1e-6 for f in K.FEEDERS), "ask C against the world")
        ok(all(abs(tbat[f] - gold_asks["B storage"][f]) < 1e-6 for f in K.FEEDERS), "ask B against the world")
    der = L["der"]
    act = der[der.ac_connection_status == "Active"]
    keys = C.der_keys(L)
    keys = keys.assign(net=keys.key.map(L["feeder"]))
    act_k = keys[keys.ac_connection_status == "Active"]
    moved = act_k[act_k.net.notna() & (act_k.net != act_k.feeder)]
    ok(set(moved.net) | set(moved.feeder) == set(K.FEEDERS), "ask D stamp device misses a feeder: %s"
       % sorted(set(moved.net) | set(moved.feeder)))
    SF_SEEN["ask D stamp rows"] = (len(moved), moved.ac_connection_id.nunique())
    bat = act[act.device_type == "Battery"]
    sbr = act_k[(act_k.device_type == "Battery") & act_k.model.isin(C.SYSTEM_LODGED)]
    ok(set(sbr.net.dropna()) == set(K.FEEDERS), "ask B: a feeder without a Sungrow SBR stack")
    modular = bat[bat.model.isin(["Battery-Box Premium HVS", "Lynx Home U"])]
    ok(len(modular) > 0, "ask B: no module-by-module battery")
    inv = act[act.device_type == "Inverter"].assign(kw=lambda d: d.rated_power_kw.astype(float))
    g_inv = inv.groupby("ac_connection_id").agg(n=("kw", "size"), kw=("kw", "first"), model=("model", "first"),
                                                reg=("registered_date", "first"), nmi=("nmi", "first"))
    duals = g_inv[g_inv.n > 1].assign(plate=lambda d: d.model.map(C.nameplate))
    old_d = duals[duals.reg < K.iso(K.PORTAL_SWITCH)]
    new_d = duals[duals.reg >= K.iso(K.PORTAL_SWITCH)]
    ok(old_d.plate.notna().all() and new_d.plate.notna().all(), "ask C: a two-inverter connection without a nameplate")
    ok((abs(old_d.kw - old_d.plate * old_d.n) < 0.011).all() and (abs(new_d.kw - new_d.plate) < 0.011).all(),
       "ask C: a two-inverter row's rating against its nameplate")
    ok(len(old_d) >= 40 and len(new_d) >= 8, "ask C devices %d old, %d new two-inverter connections" % (len(old_d), len(new_d)))
    SF_SEEN["ask C duals"] = (len(old_d), len(new_d))
    # the referee: the register's own figures for each NMI agree with the golden handling, never with the stops
    remap = dict(zip(L["realloc"].old_nmi, L["realloc"].new_nmi))
    live = reg[reg.status.isin(C.CONNECTED) & (reg.connection_date <= pd.Timestamp(K.BASE)) &
               (reg.removal_date.isna() | (reg.removal_date > pd.Timestamp(K.BASE)))]
    last = live.sort_values(["nmi", "connection_date", "application_type"]).groupby("nmi").tail(1).set_index("nmi")
    bt = bat.assign(kwh=bat.storage_capacity_kwh.astype(float), key=keys.loc[bat.index, "key"])
    per = bt.groupby("ac_connection_id").agg(k=("kwh", "size"), v=("kwh", "first"), s=("kwh", "sum"),
                                             model=("model", "first"), key=("key", "first"))
    per = per.assign(app=per.key.map(last.battery_kwh).replace("", np.nan).astype(float)).dropna(subset=["app"])
    sb, ot = per[per.model.isin(C.SYSTEM_LODGED)], per[~per.model.isin(C.SYSTEM_LODGED)]
    ok(len(sb) >= 20 and (abs(sb.v - sb.app) < 0.011).mean() >= 0.9 and (abs(sb.s - sb.app) < 0.011).mean() <= 0.05,
       "ask B referee: SBR rows against the register's battery_kwh")
    ok((abs(ot.s - ot.app) < 0.011).mean() >= 0.9, "ask B referee: module rows against the register's battery_kwh")
    gi = g_inv.assign(key=g_inv.nmi.map(C.norm_nmi).map(lambda x: remap.get(x, x)))
    gi = gi.assign(app=gi.key.map(last.kw)).dropna(subset=["app"])
    od, nd = gi[(gi.n > 1) & (gi.reg < K.iso(K.PORTAL_SWITCH))], gi[(gi.n > 1) & (gi.reg >= K.iso(K.PORTAL_SWITCH))]
    ok((abs(od.kw - od.app) < 0.011).mean() >= 0.8 and (abs(nd.kw * nd.n - nd.app) < 0.011).mean() >= 0.8,
       "ask C referee: two-inverter rows against the register's inverter_kw_ac")
    # zero device rows in the main call's population: the call ignores the DER extract and the re-allocation log
    L2 = dict(L, der=L["der"].iloc[0:0], realloc=L["realloc"].iloc[0:0])
    ok(graded(C.forecast(L2, base=base, camps=camps, pools=pools)) == g0, "R2: the call reads an ask file")
    ok(not reg.nmi.isin(set(L["realloc"].old_nmi)).any(), "a replaced NMI in the connection register")

    # ---------------------------------------------------------------- distractors: deleting each moves nothing graded
    meta_d = json.load(open(meta_path))["distractor_files"] if meta_path else list(K.DISTRACTORS)
    for gone in meta_d:
        tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(target)), suffix=".tmp")
        try:
            for f in os.listdir(target):
                if f != gone:
                    os.symlink(os.path.abspath(os.path.join(target, f)), os.path.join(tmp, f))
            L3 = C.load(tmp)
            ok(graded(C.forecast(L3)) == g0, "deleting %s moves the call" % gone)
            ok(C.ask_d(L3) == gold_asks["D sites"] and C.ask_a(L3) == gold_asks["A first lodged"] and
               C.ask_b(L3) == gold_asks["B storage"] and C.ask_c(L3) == gold_asks["C inverter"], "deleting %s moves an ask" % gone)
        finally:
            shutil.rmtree(tmp)

    # ---------------------------------------------------------------- input gates
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
    ok(set(man.owner) - {"Merindah City Council"} <= set(K.PEOPLE.values()), "a manifest owner outside the drawn personas")
    ok(set(man.file) == set(files) - {K.MANIFEST}, "manifest lists %s" % (set(files) ^ set(man.file)))
    dnames = {r[0] for r in wbd["Files"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    ok(dnames == {f for f in files if f.endswith(".csv") and f != K.MANIFEST}, "dictionary files %s" % dnames)
    ext = dict(zip(man.file, man.extracted))
    ok(ext[K.DICTIONARY] >= max(ext[f] for f in dnames), "the dictionary predates an extract it describes")
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
    ok(der.registered_date.max() <= K.iso(K.BASE) and der.status_date.max() <= K.iso(K.BASE),
       "the DER extract runs past 31 August 2026")

    # ---------------------------------------------------------------- realism sweep
    counts = [c["systems"] for c in camps]
    ok(len(set(counts)) == len(counts), "two campaigns installed the same number of systems")
    ok(len(set(c["letterboxed"] for c in camps)) == len(camps), "identical letterbox counts")
    ok(len(set(c["n365"] for c in camps)) == len(camps), "identical first-application counts")
    hcs = [L["hca"][f]["hc29"] for f in K.FEEDERS]
    ok(len(set(hcs)) == len(hcs), "two feeders share a hosting capacity")
    ok(sum(abs(h * 10 - round(h * 10)) < 1e-6 for h in hcs) <= 2, "round hosting capacities")
    ok("a 0.5 MW lower minimum lowers hosting capacity by 0.3 to 0.6 MW" in hca_txt, "the assessment's sensitivity sentence")
    rows_hc = {m.group(1): tuple(float(m.group(k)) for k in (4, 5, 6, 7)) for m in re.finditer(
        r"(YRB2\d) ([\d.]+) ([\d,]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", hca_txt)}
    ok(set(rows_hc) == set(K.FEEDERS), "the assessment's table rows %s" % sorted(rows_hc))
    steps26 = []
    for f, (m26, m29, h26, h29) in rows_hc.items():
        dm, dh = m26 - m29, h26 - h29
        lo_, hi_ = sorted((0.6 * dm, 1.2 * dm))
        ok(lo_ - 0.0051 <= dh <= hi_ + 0.0051, "%s 2026 case %.2f against minimum demand" % (f, h26))
        steps26.append(dh)
    ok(min(steps26) < 0 < max(steps26) and len({round(x, 2) for x in steps26}) == 8, "the 2026 case steps alike")
    ok(abs(up["slope"] * 100 - round(up["slope"] * 100)) > 0.05, "a round pooled rate")
    report(L, camps, pools, rr, fc, rungs, band)
    print("checks: %d assertions passed (call %s at %.3f MW, runner-up %s at %.3f, gap %.3f; Bindarra Waters %.3f MW "
          "(%.1f systems), Wattleview %.3f MW (%.1f systems))" % (
              N[0], fc["winner"], ex["YRB27"], fc["runner"], ex[fc["runner"]], fc["gap"], fc["add_mw"]["Bindarra Waters"],
              fc["lift"]["Bindarra Waters"], fc["add_mw"]["Wattleview"], fc["lift"]["Wattleview"]))
    return N[0]


def report(L, camps, pools, rr, fc, rungs, band):
    """The ladder, the fits and the fork rows as the design note quotes them (printed on every build)."""
    print("campaigns: key | first applications 12 months before | untapped at opening | letterboxed | systems | per "
          "first application")
    for c in camps:
        print("  %s %d | %d | %d | %d | %.3f" % (c["key"], c["n365"], c["untapped"], c["letterboxed"], c["systems"],
                                                c["systems"] / c["n365"]))
    for n, p in pools.items():
        print("  %s %d | %d | %d" % (n, p["n365"], p["untapped"], p["letterboxed"]))
    print("fits: " + ", ".join("%s cv %.3f" % (b, rr[b]["cv"]) for b in C.BASES))
    for name, v in rungs.items():
        e = v["excess"]
        print("rung %s: %s %.3f, %s %.3f, YRB27 %.3f (%d), YRB24 %.3f (%d); Bindarra %.3f MW, Wattleview %.3f MW" % (
            name, v["winner"], e[v["winner"]], v["runner"], e[v["runner"]], e["YRB27"], v["order"].index("YRB27") + 1,
            e["YRB24"], v["order"].index("YRB24") + 1, v["add_mw"]["Bindarra Waters"], v["add_mw"]["Wattleview"]))
    print("golden: " + ", ".join("%s %.3f" % (f, fc["excess"][f]) for f in fc["order"]))
    print("corridor: " + "; ".join("%s %.3f/%.3f/%.3f/%.3f" % (k, v["excess"]["YRB27"], v["gap"], v["add_mw"]["Bindarra Waters"],
                                                               v["add_mw"]["Wattleview"]) for k, v in band.items()))
    for k, v in SF_SEEN.items():
        print("  %s: %s" % (k, v))


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    run(t, os.path.join(task, "golden"), meta_path=os.path.join(task, "metadata.json"))
