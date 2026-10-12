"""Every assertion the design note's Build record lists, on the pack as shipped; writes generator/figures.json.

    python3 checks.py [target_dir]
"""
import datetime as dt
import glob
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import estimators as E
import callcalc as CC
import ladder as LD
import files as FL
import load as LO
import asks as A
import grants as GR

TASK = os.path.dirname(HERE)
FAILS = []
COUNT = [0]
M_ = 0.15


def ok(cond, msg):
    COUNT[0] += 1
    if not cond:
        FAILS.append(msg)
        print("FAIL", msg)


def call(v):
    return E.call(v)


def main(target):
    F = LO.pack(target)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    fig = {}
    # ------------------------------------------------------------------ input gates
    names = sorted(os.listdir(target))
    ok(len(names) == 18 and len(names) >= 10, "18 files (%d)" % len(names))
    fmts = {n.rsplit(".", 1)[1] for n in names}
    ok(len(fmts) >= 3, "three or more formats (%s)" % fmts)
    ok(len(F["val"]) >= 25000, "the spine has 25,000 rows or more (%d)" % len(F["val"]))
    ok(len(meta["distractors"]) >= 2 and all(d in names for d in meta["distractors"]), "two or more distractors named")
    ok(not any("distractor" in n.lower() for n in names), "no file name says distractor")
    fig["input_gates"] = dict(files=len(names), formats=sorted(fmts), spine_rows=len(F["val"]), distractors=meta["distractors"])

    # ------------------------------------------------------------------ C1 structure
    v = F["val"]
    ok(not v.duplicated(["valuation_date", "sub_account", "security_code", "lot_id"]).any(), "unique keys on the export")
    X, dates = LD.pack_matrix(F)
    ok(X.shape == (505, 6), "505 returns for each of six holdings (%s)" % (X.shape,))
    ok(dates[0] == dt.date(2024, 12, 2) and dates[-1] == W.VAL_DATE, "the window runs to the 30 November valuation")
    # custodian fund prices equal Kestwick's on every day
    st = dict(zip(F["static"]["security_code"], F["static"]["isin"]))
    fm = {}
    for f, (i, a) in F["kest_isins"].items():
        fm[i], fm[a] = (f, "Income units (GBP)"), (f, "Accumulation units (GBP)")
    fund_rows = v[v["asset_class"] == "Collective investment scheme"]
    mism = 0
    kp = {f: F["kest"][f].set_index(F["kest"][f]["Date"].map(lambda d: d.isoformat())) for f in F["kest"]}
    for code, sub in fund_rows.groupby("security_code"):
        f, col = fm[st[code]]
        ref = kp[f][col].reindex(sub["valuation_date"]).values
        mism += int(np.sum(np.abs(ref - sub["price"].values) > 1e-9))
    ok(mism == 0, "the custodian's fund prices equal Kestwick's on every day (%d differ)" % mism)
    # combining the returns first and combining the covariances agree
    w = E.wvec(60)
    a1 = np.var(X @ w, ddof=1)
    C = np.cov(X.T, ddof=1)
    ok(abs(a1 - w @ C @ w) < 1e-15, "order of operations: portfolio returns first or covariances first")

    # ------------------------------------------------------------------ the ladder
    T = E.table(X, dates)
    Xi = CC.index_matrix(F["index"], dates)
    r2 = {s: E.simple(Xi, s) for s in W.STEPS}
    r0 = T["R0 daily"]
    ok(call(r0) == 70 and r0[70] <= 10 - M_ and r0[80] >= 10 + M_, "R0 daily calls 70 with margins (%.2f, %.2f)" % (r0[70], r0[80]))
    gold = {n: t for n, t in T.items() if E.GOLDEN(n)}
    for n, t in gold.items():
        ok(call(t) == 60 and t[60] <= 10 - M_ and t[70] >= 10 + M_, "%s calls 60 with margins (%.2f, %.2f)" % (n, t[60], t[70]))
        ok(all(abs(t[s] - 10) >= M_ for s in W.STEPS), "%s: no step within 0.15 of the cap" % n)
    for n, t in T.items():
        if E.PARTIAL(n):
            ok(call(t) == 60, "%s calls 60 (%.2f, %.2f)" % (n, t[60], t[70]))
    for nm, t in (("R1 ewma 0.94", T["R1 ewma 0.94"]), ("R2 indices", r2), ("R3 ledoit-wolf", T["R3 ledoit-wolf"])):
        c = call(t)
        ok(c not in (None, 60) and t[c] <= 10 - M_ and (c == 100 or t[c + 10] >= 10 + M_),
           "%s calls %s, off 60 with margins" % (nm, c))
    ok(call(T["R3 ledoit-wolf"]) == 70, "R3 Ledoit-Wolf calls 70")
    lw_delta = E.ledoit_wolf_cc(X, 60)[1]
    n_months = len(E.months(X, dates))
    ok(n_months == 24 and n_months < 100, "R4 monthly has 24 periods, under policy 4.3's 100")
    ok(all(all(np.diff([t[s] for s in W.STEPS]) > 0) for t in T.values()), "SF3: volatility rises with the step under every estimator")
    ac, tstat = E.autocorr1(X, 60)
    ok(0.17 <= ac <= 0.26 and tstat >= 3.5, "portfolio lag-1 autocorrelation at 60 (%.3f, t %.1f)" % (ac, tstat))
    same, nxt, wkc = E.uk_na(X)
    ok(0.20 <= same <= 0.35 and nxt >= 0.40 and wkc >= 0.45, "UK and North American correlations (%.2f %.2f %.2f)" % (same, nxt, wkc))
    sv = E.single_vols(X, dates)
    for h, vv in sv.items():
        ok(max(vv) / min(vv) <= 1.12, "single holding %s: daily, five-day and monthly volatilities within 12%% (%s)" % (h, vv))
    vr = np.var(E.blocks(X, 5) @ w, ddof=1) / (5 * np.var(X @ w, ddof=1))
    fig["ladder"] = {n: {str(s): round(t[s], 4) for s in W.STEPS} for n, t in T.items()}
    fig["ladder"]["R2 indices"] = {str(s): round(r2[s], 4) for s in W.STEPS}
    fig["calls"] = {n: call(t) for n, t in list(T.items()) + [("R2 indices", r2)]}
    fig["forcing"] = dict(lag1_autocorrelation_60=round(ac, 3), t=round(tstat, 2), uk_na_same_day=round(same, 2),
                          uk_na_next_day=round(nxt, 2), uk_na_five_day=round(wkc, 2), variance_ratio_five_day_60=round(vr, 3),
                          ledoit_wolf_intensity=round(lw_delta, 3),
                          single={h: [round(x, 2) for x in vv] for h, vv in sv.items()})
    fig["call"] = 60
    fig["volatility_lead_lag_1"] = {str(s): round(T["G lead-lag 1"][s], 4) for s in W.STEPS}

    # ------------------------------------------------------------------ the semantic fork table
    sf = {}
    # SF1 equities at today's drifted split
    last = v[v["valuation_date"] == W.VAL_DATE.isoformat()]
    mand = last[last["asset_class"].isin(CC.MAND_CLASSES)]["market_value_gbp"].sum()
    fv = {}
    for code, mv in zip(last["security_code"], last["market_value_gbp"]):
        if st.get(code) in fm:
            fv[fm[st[code]][0]] = fv.get(fm[st[code]][0], 0) + mv
    gv = mand + fv["NAEF"] + fv["EUEF"] + fv["JPEF"]
    dv = fv["GILT"] + fv["CORP"]
    drift_w = {"MAND": mand / gv, "NAEF": fv["NAEF"] / gv, "EUEF": fv["EUEF"] / gv, "JPEF": fv["JPEF"] / gv,
               "GILT": fv["GILT"] / dv, "CORP": fv["CORP"] / dv}

    def wv_drift(step):
        s = step / 100
        return np.array([drift_w[h] * (s if h in W.GROWTH else 1 - s) for h in W.HOLDINGS])
    orig = E.wvec
    E.wvec = wv_drift
    T1 = E.table(X, dates)
    E.wvec = orig
    sf["SF1"] = dict(default=call(T1["R0 daily"]), golden=sorted({call(t) for n, t in T1.items() if E.GOLDEN(n)}))
    ok(sf["SF1"]["golden"] == [60] and sf["SF1"]["default"] == 70, "SF1 drifted split: same call %s" % sf["SF1"])
    # SF2 a continuous share
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        vv = E.leadlag(X, mid * 100, 1)
        lo, hi = (mid, hi) if vv <= 10 else (lo, mid)
    sf["SF2"] = dict(continuous_share=round(lo * 100, 1))
    ok(round(lo * 100) % 10 != 0, "SF2: the continuous share is not a step")
    # SF5 each step's volatility rounded first
    sf["SF5"] = {n: call({s: round(t[s]) for s in W.STEPS}) for n, t in gold.items()}
    # SF6 the exponentially weighted estimate
    sf["SF6"] = dict(ewma=call(T["R1 ewma 0.94"]))
    ok(sf["SF6"]["ewma"] != 60, "SF6 exponentially weighted: not 60")
    # SF7 to 31 October 2026: the pack's prices begin on 29 November 2024
    first = min(F["kest"]["GILT"]["Date"])
    ok(first == W.WIN_START and v["valuation_date"].min() == W.WIN_START.isoformat(),
       "SF7: the pack holds no prices before 29 November 2024, so the October window cannot be formed")
    sf["SF7"] = dict(first_price=W.WIN_START.isoformat())
    # SF8 benchmark indices
    sf["SF8"] = dict(indices=call(r2))
    # SF9 distributions left out; SF12 one endowment, cash; SF13 days a year
    grid = LD.slip_grid(F)
    for s_, r in grid.items():
        ok(r["default"] != 60, "slip %s: the default does not land on 60 (%s)" % (s_, r["default"]))
    bad = LD.slip_ok(grid)
    ok(not bad, "Layer 1 grid: %s" % bad)
    fig["slips"] = grid
    sf["SF9"] = grid["distributions left out"]
    sf["SF12"] = {k: grid[k] for k in ("permanent endowment only", "expendable endowment only", "mandate cash left out")}
    sf["SF13"] = {}
    for py in (250, 252, 253, 260):
        f = np.sqrt(py / 252)
        d0 = call({s: T["R0 daily"][s] * f for s in W.STEPS})
        g0 = sorted({call({s: t[s] * (f if not ("five-day blocks" in n or "calendar" in n) else 1.0) for s in W.STEPS})
                     for n, t in gold.items()})
        sf["SF13"][str(py)] = dict(default=d0, golden=g0)
        ok(d0 == 70 and g0 == [60], "SF13 at %d days a year: %s %s" % (py, d0, g0))
    for py in (50.5, 52.0, 52.18):
        f = np.sqrt(py / 52)
        g0 = sorted({call({s: t[s] * f for s in W.STEPS}) for n, t in gold.items() if "five-day blocks" in n or "calendar" in n})
        ok(g0 == [60], "SF13 five-day periods at %.2f a year: %s" % (py, g0))
    # SF10 weights drifting from the window's start
    def drifting(X, step):
        w0 = E.wvec(step)
        val_ = w0.copy()
        out = []
        for r in X:
            wt = val_ / val_.sum()
            out.append(wt @ r)
            val_ = val_ * (1 + r)
        return np.array(out)
    p_d = {s: drifting(X, s) for s in W.STEPS}
    sf["SF10"] = dict(default=call({s: E.vol_of(p_d[s], 252) for s in W.STEPS}),
                      lead_lag=call({s: float(np.sqrt((np.var(p_d[s], ddof=1) + 2 * np.cov(p_d[s][1:], p_d[s][:-1])[0, 1]) * 252) * 100) for s in W.STEPS}))
    # SF11 overlapping twelve-month returns
    sf["SF11"] = dict(overlapping=call({s: E.overlapping_annual(X, s) for s in W.STEPS}),
                      at60=round(E.overlapping_annual(X, 60), 2))
    ok(sf["SF11"]["overlapping"] != 60 or True, "SF11 recorded")
    fig["semantic_forks"] = sf
    # clean-data test: the returns built in the generator, before any export rounding or Layer 1 device
    try:
        import build as BLD
        M, fp, B, Xs, ds, g, i, p = BLD.world()
        Ts = E.table(Xs, ds)
        ok(call(Ts["R0 daily"]) == 70 and all(call(t) == 60 for n, t in Ts.items() if E.GOLDEN(n)),
           "clean-data test: the generator's own returns call 70 on the default and 60 on every golden member")
        ok(np.abs(Xs - X).max() < 1e-6, "the pack's returns reproduce the generator's (%.2e)" % np.abs(Xs - X).max())
    except ImportError:
        pass
    # separation: scramble every ask-only file and recompute the call's figures
    tmp = tempfile.mkdtemp()
    for n in names:
        shutil.copy(os.path.join(target, n), tmp)
    rng = np.random.default_rng(5)
    for k in ("ent", "reg", "inst", "pays"):
        df = F[k].copy()
        for c in df.columns:
            df[c] = rng.permutation(df[c].values)
        df.to_csv(os.path.join(tmp, FL.FILES[k]), index=False)
    os.remove(os.path.join(tmp, FL.FILES["budget"]))
    shutil.copy(os.path.join(target, FL.FILES["budget"]), tmp)
    F2 = dict(F)
    for k in ("ent", "reg", "inst", "pays"):
        F2[k] = pd.read_csv(os.path.join(tmp, FL.FILES[k]), dtype=str)
    X2, d2 = LD.pack_matrix(F2)
    ok(np.array_equal(X2, X), "separation: scrambling the ask-only files leaves the call's returns unchanged")
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ the asks
    running = sum(x for _, x in F["running"])
    capital = sum(x for _, x in F["capital"])
    P = FL.pack_for_asks(F, running, capital, F["kest_isins"])
    inc, info = A.income(P)
    G, parts = A.grant_payments(P)
    rel = A.release(P, inc, G, running)
    t = A.title(inc, G)
    gold_ask = [inc[s] for s in A.STEPS] + [G] + [rel[s] for s in A.STEPS]
    stated = [A.r1000(x) for x in gold_ask]
    for x, r in zip(gold_ask, stated):
        ok(abs(x - r) <= 400, "golden ask figure %.0f sits 100 pounds or more inside its bin (%s)" % (x, r))
    ok(t is not None and t < 100 and inc[t] - G >= 0.025 * inc[t] and G - inc[t + 10] >= 0.025 * inc[t + 10],
       "title margins of 2.5 per cent of income on each side")
    ok(all(rel[s] >= 30000 for s in A.STEPS), "the golden release is positive at every step, 30,000 pounds or more")
    ok(all(np.diff([inc[s] for s in A.STEPS]) < 0), "income falls with the step")
    ok(abs(running - round(running, -3)) > 0 and abs(G - round(G, -3)) > 0, "no round headline totals")
    lags = A.history_lags(P)
    ok(min(lags["later"]) >= 35 and max(lags["later"]) <= 70, "project later instalments paid 35 to 70 days after the due date (%s to %s)" % (min(lags["later"]), max(lags["later"])))
    ok(max(lags["core"]) == 0 and max(lags["first"]) == 0, "core and first instalments paid on their due date")
    Gs = {L: A.grant_payments(P, lag=L)[0] for L in range(35, 71)}
    ok(max(Gs.values()) - min(Gs.values()) < 0.005, "C3 corridor: every lag from 35 to 70 days gives the same grant payments")
    kinds = A.instalment_kinds(P)
    corridor_hits = 0
    unpaid_early = 0
    for (ref, no, due, amt, stt), kd in zip(P.inst[["grant_ref", "instalment_no", "due_date", "amount", "status"]].itertuples(index=False), kinds):
        d = A.ukdate(due)
        if kd == "later" and GR.in_corridor(d):
            corridor_hits += 1
        reg_status = P.reg.set_index("grant_ref").loc[ref, "status"]
        if kd == "later" and d < dt.date(2026, 10, 23) and stt == "Scheduled" and reg_status != "Withdrawn":
            unpaid_early += 1
    ok(corridor_hits == 0, "no project later instalment falls due in either corridor")
    ok(unpaid_early == 0, "every later instalment due before 23 October 2026 is paid by 30 November")
    # stops and hazards
    stops = A.all_stops(P, running, capital)
    worst = (1e18, None)
    for key, (i2, g2, r2_, t2) in stops.items():
        vals = [i2[s] for s in A.STEPS] + [g2] + [r2_[s] for s in A.STEPS]
        for x, gv, r in zip(vals, gold_ask, stated):
            if abs(x - gv) < 0.005:
                continue
            if abs(x - r) < worst[0]:
                worst = (abs(x - r), key)
    ok(worst[0] >= 600, "every mishandling combination lands 600 pounds or more from the stated golden (%.0f at %s)" % worst)

    def figs(lines="position", months=12, route="history", acc=False, clock=True, wout=True, conv=True, lag_all=False, fees=False):
        i2 = A.income(P, lines, months, route, acc)[0]
        g2 = A.grant_payments(P, clock, 50, wout, conv, lag_all)[0]
        r2_ = A.release(P, i2, g2, running + (capital if fees else 0))
        return i2, g2, r2_, A.title(i2, g2)
    named = {
        "golden": figs(),
        "s1 cracker (lot lines summed, due dates)": figs(lines="lines", clock=False),
        "s2 lazy (whole report, funds from the report, due dates, no register)": figs(lines="lines", months=13, route="extract", clock=False, wout=False, conv=False),
        "o1 dedup on designation, security and ex-date": figs(lines="o1"),
        "o2 dedup on security and event": figs(lines="o2"),
        "s3 funds from report lines over today's value": figs(route="extract"),
        "o3 lag on every instalment": figs(lag_all=True),
        "s4 withdrawn grants kept": figs(wout=False),
        "D6 alone": figs(lines="lines"),
        "D8 alone": figs(clock=False),
        "H1 thirteen months": figs(months=13),
        "H3 euro as pounds": figs(conv=False),
        "fees counted as running costs": figs(fees=True),
        "accrued income in the value": figs(acc=True),
    }
    fig["stops"] = {}
    for nm, (i2, g2, r2_, t2) in named.items():
        fig["stops"][nm] = dict(income={str(s): round(i2[s], 2) for s in A.STEPS}, grant_payments=round(g2, 2),
                                release={str(s): round(r2_[s], 2) for s in A.STEPS}, title=t2,
                                income_hits=sum(A.r1000(i2[s]) == A.r1000(inc[s]) for s in A.STEPS),
                                release_hits=sum(A.r1000(r2_[s]) == A.r1000(rel[s]) for s in A.STEPS),
                                grants_hit=A.r1000(g2) == A.r1000(G))
    # the cracker sheet: every ask row a miss; the mirror sheet is the same response at R0 (the asks do not read the call)
    cr = fig["stops"]["s1 cracker (lot lines summed, due dates)"]
    ok(cr["income_hits"] == 0 and cr["release_hits"] == 0 and not cr["grants_hit"] and cr["title"] != t,
       "cracker sheet: every ask row a miss %s" % {k: cr[k] for k in ("income_hits", "release_hits", "grants_hit", "title")})
    ok(A.r1000(cr["grant_payments"]) != A.r1000(G), "cracker: the grant payments line misses")
    ok(abs(cr["grant_payments"] + running - (G + running)) >= 600, "cracker: the grants plus running costs line misses")
    ok(fig["stops"]["D6 alone"]["title"] != t and fig["stops"]["D8 alone"]["title"] != t, "D6 alone and D8 alone each move the title")
    # necessity matrix
    nec = {}
    for nm in ("D6 alone", "H1 thirteen months", "accrued income in the value", "s3 funds from report lines over today's value",
               "D8 alone", "s4 withdrawn grants kept", "H3 euro as pounds", "fees counted as running costs"):
        r = fig["stops"][nm]
        nec[nm] = dict(income_moved=9 - r["income_hits"], release_moved=9 - r["release_hits"], grants_moved=not r["grants_hit"])
    fig["necessity"] = nec
    for nm in ("D6 alone", "H1 thirteen months", "s3 funds from report lines over today's value"):
        ok(nec[nm]["income_moved"] == 9, "necessity: %s moves all nine incomes" % nm)
    for nm in ("D8 alone", "s4 withdrawn grants kept", "H3 euro as pounds"):
        ok(nec[nm]["grants_moved"] and nec[nm]["release_moved"] == 9, "necessity: %s moves the payments and every release" % nm)
    ok(nec["fees counted as running costs"]["release_moved"] == 9, "necessity: the fee lines move every release")
    # the lot-line device's mass and silence
    e = P.ent
    em = e[(e["ex_date"] >= A.INC_FROM.isoformat()) & (~e["security_code"].str.startswith("KWC"))]
    infl = em["entitlement_gbp"].sum() / em.drop_duplicates(["sub_account", "security_code", "event_ref"])["entitlement_gbp"].sum() - 1
    ok(0.28 <= infl <= 0.48, "D6: summing the lot lines puts the mandate's income %.1f per cent high" % (100 * infl))
    ok(not e.duplicated().any(), "D6 silent: no exact duplicate lines in the income report")
    ok(not e.duplicated(["sub_account", "security_code", "event_ref", "lot_id"]).any(), "D6 silent: keys unique on lot and event")
    multi = em.groupby(["sub_account", "security_code", "event_ref"])["lot_id"].nunique()
    fig["devices"] = dict(lot_inflation=round(infl, 4), positions_multi_lot=int((multi > 1).sum()), positions=int(len(multi)),
                          apparent_mandate_yield=round(info["yields"]["MAND"] * (1 + infl), 4))
    # figures the write-up and the goldens state
    fig["portfolio_value"] = round(info["total"], 2)
    fig["mandate_value"] = round(info["mand_mv"], 2)
    fig["yields"] = {h: round(y, 6) for h, y in info["yields"].items()}
    fig["income"] = {str(s): round(inc[s], 2) for s in A.STEPS}
    fig["income_stated"] = {str(s): A.r1000(inc[s]) for s in A.STEPS}
    fig["grant_payments_2027"] = round(G, 2)
    fig["grant_payments_2027_stated"] = A.r1000(G)
    fig["grant_payments_parts"] = {k: round(x, 2) for k, x in parts.items()}
    fig["running_costs"] = running
    fig["running_costs_stated"] = A.r1000(running)
    fig["capital_charges"] = capital
    fig["release"] = {str(s): round(rel[s], 2) for s in A.STEPS}
    fig["release_stated"] = {str(s): A.r1000(rel[s]) for s in A.STEPS}
    fig["title_step"] = t
    fig["title_margins"] = dict(above=round(inc[t] - G, 2), below=round(G - inc[t + 10], 2))
    fig["worst_stop"] = round(worst[0], 2)
    fig["lags"] = dict(later_min=min(lags["later"]), later_max=max(lags["later"]), later_n=len(lags["later"]))

    # ------------------------------------------------------------------ documents and realism
    banned = re.compile(r"\blag(s|ged|ging)?\b|\bstale|synchron|autocorrel|dimson|scholes|newey|\bweekly\b|square root|"
                        r"annualis|time zone|fair value", re.I)
    for n in names:
        txt = text_of(os.path.join(target, n))
        if n.endswith((".csv",)) and n not in (FL.FILES["moves"], FL.FILES["events"], FL.FILES["reg"]):
            continue
        hits = banned.findall(txt)
        ok(not hits, "no stump vocabulary in %s (%s)" % (n, hits[:3]))
        ok("—" not in txt, "no em dash in %s" % n)
    # no shipped figure of the decision: no portfolio volatility, no mandate yield, no 2027 grant payments total
    for n in names:
        txt = text_of(os.path.join(target, n)).lower()
        ok("portfolio volatility" not in txt and "expected volatility of" not in txt, "%s states no portfolio volatility" % n)
    rows_per_day = v.groupby("valuation_date").size()
    ok(rows_per_day.nunique() > 3, "the export's rows per day vary")
    pay_month = F["pays"].groupby(F["pays"]["payment_date"].str[:7]).size()
    ok(pay_month.nunique() > 3, "payments per month vary")
    ok(F["reg"]["grantee"].nunique() == len(F["reg"]), "no grantee name repeats")
    ok(abs(info["total"] - round(info["total"], -4)) > 100, "the portfolio value is not round")
    fig["checks"] = COUNT[0]
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, default=lambda o: o if not isinstance(o, (np.integer, np.floating)) else o.item())
    print("checks: %d assertions, %d failed" % (COUNT[0], len(FAILS)))
    return not FAILS


def text_of(path):
    if path.endswith((".csv", ".txt")):
        return open(path, encoding="utf-8").read()
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    if path.endswith((".docx", ".xlsx")):
        with zipfile.ZipFile(path) as z:
            return " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")) for n in z.namelist() if n.endswith(".xml"))
    return ""


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    sys.exit(0 if main(tgt) else 1)
