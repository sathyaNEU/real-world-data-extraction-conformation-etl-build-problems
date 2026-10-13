"""Every assertion the design note's Build record lists, on the pack as shipped; writes generator/figures.json.

    python3 checks.py [target_dir]
"""
import datetime as dt
import json
import os
import re
import shutil
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
M_ = 0.15                 # the ladder's margin from the cap
BIN = 400                 # every golden ask figure at most this far from its stated thousand
STOP = 600                # every mishandling that moves a figure lands at least this far from the stated golden

# The sentences the semantic fork table quotes: (SF id, file key, text), each present once in its document.
QUOTES = [
    ("SF1", "policy", "Within growth assets the weights are 40 per cent the mandate, 30 per cent North American, 15 per "
                      "cent European and 15 per cent Japan; within defensive assets, 55 per cent gilts and 45 per cent "
                      "corporate bonds."),
    ("SF2", "policy", "The trustees set the growth share in ten-point steps from 20 to 100 per cent."),
    ("SF4", "policy", "The portfolio's expected volatility at the growth share set must be not more than 10 per cent."),
    ("SF5", "policy", "The estimate is compared with the cap before any rounding."),
    ("SF6", "policy", "The returns are daily, one for each business day of the two years, and every day is weighted equally."),
    ("SF7", "policy", "over the two years to the last month-end valuation before the review"),
    ("SF8", "policy", "each measured from the holding's own prices and the income it pays"),
    ("SF9", "policy", "Expected volatility is the standard deviation of the portfolio's total return over twelve months."),
    ("SF10", "policy", "combined in every period at the policy weights for the growth share under review"),
    ("SF11", "policy", "The returns are daily, one for each business day of the two years"),
    ("SF12", "policy", "The trust invests its permanent and expendable endowments as one portfolio under this policy."),
    ("SF12", "policy", "The mandate includes the cash its manager holds in it."),
    ("SF14", "policy", "At their December meeting the trustees set the growth share for the following calendar year."),
    ("SF14", "proc", "The budget year is the calendar year."),
]
# words no document may carry (the decisive step's vocabulary)
BANNED = re.compile(r"\blag(s|ged|ging)?\b|\bstale|synchron|autocorrel|dimson|scholes|newey|\bweekly\b|square root|"
                    r"annualis|time zone|fair value", re.I)


def ok(cond, msg):
    COUNT[0] += 1
    if not cond:
        FAILS.append(msg)
        print("FAIL", msg)


def call(v):
    return E.call(v)


def text_of(path):
    if path.endswith((".csv", ".txt")):
        return open(path, encoding="utf-8").read()
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    if path.endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            x = z.read("word/document.xml").decode("utf-8")
        paras = re.findall(r"<w:p[ >].*?</w:p>", x, re.S)
        return "\n".join("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras)
    if path.endswith(".xlsx"):
        with zipfile.ZipFile(path) as z:
            return " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")) for n in z.namelist()
                            if n.endswith(".xml"))
    return ""


def flat(s):
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def main(target):
    F = LO.pack(target)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    fig = {}
    names = sorted(os.listdir(target))
    texts = {n: text_of(os.path.join(target, n)) for n in names}
    # ------------------------------------------------------------------ input gates
    ok(len(names) == 18, "18 files (%d)" % len(names))
    fmts = {n.rsplit(".", 1)[1] for n in names}
    ok(len(fmts) >= 3, "three or more formats (%s)" % sorted(fmts))
    ok(len(F["val"]) >= 25000, "the spine has 25,000 rows or more (%d)" % len(F["val"]))
    ok(len(meta["distractors"]) >= 2 and all(d in names for d in meta["distractors"]), "two or more distractors named")
    ok(not any("distractor" in n.lower() for n in names), "no file name says distractor")
    ok(sorted(names) == sorted(FL.FILES.values()), "the pack is exactly the files the generator names")
    fig["input_gates"] = dict(files=len(names), formats=sorted(fmts), spine_rows=len(F["val"]), distractors=meta["distractors"])

    # ------------------------------------------------------------------ C1 structure
    v = F["val"]
    ok(not v.duplicated(["valuation_date", "sub_account", "security_code", "lot_id"]).any(), "unique keys on the export")
    ok(set(v["sub_account"]) == set(W.SUB_ACCOUNTS), "the export carries the two designations and no other account")
    X, dates = LD.pack_matrix(F)
    ok(X.shape == (505, 6), "505 returns for each of six holdings (%s)" % (X.shape,))
    ok(dates[0] == dt.date(2024, 12, 2) and dates[-1] == W.VAL_DATE, "the window runs to the 30 November valuation")
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
    ok(mism == 0, "C1 version basis: the custodian's fund prices equal Kestwick's on every day (%d differ)" % mism)
    w = E.wvec(60)
    C = np.cov(X.T, ddof=1)
    ok(abs(np.var(X @ w, ddof=1) - w @ C @ w) < 1e-15, "C1 order of operations: portfolio returns first or covariances first")

    # ------------------------------------------------------------------ the ladder
    T = E.table(X, dates)
    Xi = CC.index_matrix(F["index"], dates)
    r2 = {s: E.simple(Xi, s) for s in W.STEPS}
    r0 = T["R0 daily"]
    ok(call(r0) == 70 and r0[70] <= 10 - M_ and r0[80] >= 10 + M_, "R0 daily calls 70 with margins (%.2f, %.2f)" % (r0[70], r0[80]))
    gold = {n: t for n, t in T.items() if E.GOLDEN(n)}
    ok(sorted(gold) == ["G cross-lag matrix 1", "G lead-lag 1", "G lead-lag 2", "G newey-west 4", "G newey-west 5"],
       "the golden family: the daily estimators that take in the cross-day covariances (policy 4.3, daily returns)")
    notd = {n: t for n, t in T.items() if E.NOT_DAILY(n)}
    ok(len(notd) == 30 and all(call(t) == 60 for t in notd.values()),
       "SF11 the 30 estimators on periods of several days, refused by policy 4.3, each land 60 (%d)" % len(notd))
    fig["not_daily"] = {n: {str(s): round(t[s], 4) for s in W.STEPS} for n, t in notd.items()}
    for n, t in gold.items():
        ok(call(t) == 60 and t[60] <= 10 - M_ and t[70] >= 10 + M_, "%s calls 60 with margins (%.2f, %.2f)" % (n, t[60], t[70]))
        ok(all(abs(t[s] - 10) >= M_ for s in W.STEPS), "SF4 %s: no step within 0.15 of the cap" % n)
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
    ok(n_months == 24, "R4 monthly: 24 monthly returns, refused by policy 4.3 (the returns are daily) (%d)" % n_months)
    ok(all(all(np.diff([t[s] for s in W.STEPS]) > 0) for t in list(T.values()) + [r2]),
       "SF3: the volatility rises with the step under every estimator")
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
    gv60 = [t[60] for t in gold.values()]
    gv70 = [t[70] for t in gold.values()]
    fig["golden_family_range"] = {"60": [round(min(gv60), 2), round(max(gv60), 2)], "70": [round(min(gv70), 2), round(max(gv70), 2)]}
    # the write-up's ranges, one decimal from the unrounded members; the lead-lag figures it quotes sit mid-bin
    fig["golden_family_range_stated"] = {"60": ["%.1f" % min(gv60), "%.1f" % max(gv60)],
                                         "70": ["%.1f" % min(gv70), "%.1f" % max(gv70)]}
    ok(fig["golden_family_range_stated"] == {"60": ["9.3", "9.6"], "70": ["10.6", "11.0"]},
       "the golden family's ranges as stated: %s" % fig["golden_family_range_stated"])
    ll1 = T["G lead-lag 1"]
    fig["lead_lag_1_stated"] = {"60": "%.1f" % ll1[60], "70": "%.1f" % ll1[70]}
    ok(all(abs(ll1[s] * 10 - np.floor(ll1[s] * 10) - 0.5) >= 0.35 for s in (60, 70)),
       "the lead-lag figures quoted (%.4f, %.4f) sit at least 0.035 from a rounding edge" % (ll1[60], ll1[70]))
    fig["newey_west_60_stated"] = sorted({"%.1f" % T[n][60] for n in ("G newey-west 4", "G newey-west 5")})
    fig["default_r0"] = {str(s): round(r0[s], 2) for s in (60, 70, 80)}
    fig["forcing"] = dict(lag1_autocorrelation_60=round(ac, 3), t=round(tstat, 2), uk_na_same_day=round(same, 2),
                          uk_na_next_day=round(nxt, 2), uk_na_five_day=round(wkc, 2), variance_ratio_five_day_60=round(vr, 3),
                          ledoit_wolf_intensity=round(lw_delta, 3),
                          single={h: [round(x, 2) for x in vv] for h, vv in sv.items()})
    fig["call"] = 60
    fig["call_default"] = call(r0)
    fig["conventions"] = dict(cap=W.CAP, steps=W.STEPS, days_a_year=252, weeks_a_year=52, returns_per_holding=int(X.shape[0]),
                              eur_rate=W.EUR_RATE)

    # ------------------------------------------------------------------ the semantic fork table
    sf = {}
    pol = flat(texts[FL.FILES["policy"]])
    proc = flat(texts[FL.FILES["proc"]])
    for sid, key, q in QUOTES:
        body = pol if key == "policy" else proc
        ok(body.count(flat(q)) == 1, "%s: the quoted sentence is in %s once (%s...)" % (sid, FL.FILES[key], q[:40]))
    # SF1 equities at today's drifted split
    last = v[v["valuation_date"] == W.VAL_DATE.isoformat()]
    mand = last[last["asset_class"].isin(CC.MAND_CLASSES)]["market_value_gbp"].sum()
    fv = {}
    for code, mv in zip(last["security_code"], last["market_value_gbp"]):
        if st.get(code) in fm:
            fv[fm[st[code]][0]] = fv.get(fm[st[code]][0], 0) + mv
    gv_ = mand + fv["NAEF"] + fv["EUEF"] + fv["JPEF"]
    dv_ = fv["GILT"] + fv["CORP"]
    drift_w = {"MAND": mand / gv_, "NAEF": fv["NAEF"] / gv_, "EUEF": fv["EUEF"] / gv_, "JPEF": fv["JPEF"] / gv_,
               "GILT": fv["GILT"] / dv_, "CORP": fv["CORP"] / dv_}

    def wv_drift(step):
        s = step / 100
        return np.array([drift_w[h] * (s if h in W.GROWTH else 1 - s) for h in W.HOLDINGS])
    orig = E.wvec
    E.wvec = wv_drift
    T1 = E.table(X, dates)
    E.wvec = orig
    sf["SF1"] = dict(default=call(T1["R0 daily"]), golden=sorted({call(t) for n, t in T1.items() if E.GOLDEN(n)}))
    ok(sf["SF1"]["golden"] == [60] and sf["SF1"]["default"] == 70, "SF1 drifted split: same call %s" % sf["SF1"])
    # SF2 a continuous share is not a step
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if E.leadlag(X, mid * 100, 1) <= 10 else (lo, mid)
    sf["SF2"] = dict(continuous_share=round(lo * 100, 1))
    ok(abs(lo * 100 - round(lo * 10) * 10) > 0.5, "SF2: the continuous share (%.1f) is not a step" % (lo * 100))
    # SF3 recorded above (monotone). SF4: not more than against strictly under
    strict = {n: max([s for s in W.STEPS if t[s] < W.CAP] or [None]) for n, t in gold.items()}
    sf["SF4"] = dict(strictly_under=sorted(set(strict.values())), default=max(s for s in W.STEPS if r0[s] < W.CAP))
    ok(sf["SF4"]["strictly_under"] == [60] and sf["SF4"]["default"] == 70, "SF4 strictly under the cap: same call %s" % sf["SF4"])
    # SF5 each step's volatility rounded first
    sf["SF5"] = {n: call({s: round(t[s]) for s in W.STEPS}) for n, t in gold.items()}
    ok(set(sf["SF5"].values()) == {60} and call({s: round(r0[s]) for s in W.STEPS}) == 70,
       "SF5 rounded to a whole per cent first: same call for every golden-family member %s, the default on 70" % sf["SF5"])
    # SF6 the exponentially weighted estimate (refused by 4.3)
    sf["SF6"] = dict(ewma=call(T["R1 ewma 0.94"]))
    ok(sf["SF6"]["ewma"] != 60, "SF6 exponentially weighted: not 60 (%s)" % sf["SF6"]["ewma"])
    # SF7 a window ending 31 October 2026: the pack's prices begin on 29 November 2024; the call on the returns to then
    first = min(F["kest"]["GILT"]["Date"])
    ok(first == W.WIN_START and v["valuation_date"].min() == W.WIN_START.isoformat(),
       "SF7: the pack's prices begin on 29 November 2024, two years before the 30 November valuation")
    cut = [k for k, d in enumerate(dates) if d <= dt.date(2026, 10, 30)]
    Toc = E.table(X[cut], [dates[k] for k in cut])
    sf["SF7"] = dict(first_price=W.WIN_START.isoformat(), october_default=call(Toc["R0 daily"]),
                     october_golden=sorted({call(t) for n, t in Toc.items() if E.GOLDEN(n)}))
    ok(sf["SF7"]["october_default"] == 70 and sf["SF7"]["october_golden"] == [60],
       "SF7 the returns to 31 October 2026: same call %s" % sf["SF7"])
    # SF8 benchmark indices (the declared wrong-basis distractor, refused by 4.2)
    sf["SF8"] = dict(indices=call(r2))
    ok(sf["SF8"]["indices"] not in (None, 60), "SF8 the benchmark indices: not 60 (%s)" % sf["SF8"]["indices"])
    # the Layer 1 grid: SF9 distributions left out, SF12 one endowment, SF13 days a year, and the slips
    grid = LD.slip_grid(F)
    # Every holding prices on every UK business day, so the holiday slips are deliberate filters on the calendars: the 46
    # days on which the North American or Japan fund carries no new close of its market taken out and merged into the
    # next day, or only the days on which London, New York and Tokyo are all open kept. At 252 periods a year either
    # lands the default on 60; both are a lower rung that policy 4.3 refuses (the periods left are not of equal length),
    # accepted at stage 3 and recorded in the design note's grid and As built. Asserted: the refusal, the default's 70
    # at the series' own count of periods a year, and that deleting the days instead leaves periods that no longer
    # divide the two years.
    pos = {d: k for k, d in enumerate(dates)}
    for ph, rows_of in (("post-holiday days dropped", CC.post_holiday_rows), ("common trading days kept", CC.non_common_rows)):
        Xm, dm = LD.slip_matrix(F, ph)
        drop = rows_of(F["cal"], dates)
        ok(len(Xm) == 505 - len(drop) and len(drop) > 0, "%s: %d periods merged into the next" % (ph, len(drop)))
        lengths = np.diff([-1] + [pos[d] for d in dm])
        ok(len(set(lengths.tolist())) > 1, "%s: periods of %s business days mixed (policy 4.3's equal lengths refuse it)"
           % (ph, sorted(set(lengths.tolist()))))
        grid[ph]["dropped"] = len(drop)
        grid[ph]["period_lengths"] = {str(k): int((lengths == k).sum()) for k in sorted(set(lengths.tolist()))}
        own, Town = LD.calls_on(Xm, dm, len(dm) / 2.0)
        ok(own["R0 daily"] == 70, "%s at the series' own %.1f periods a year: the default stays on 70 (%s)"
           % (ph, len(dm) / 2.0, own["R0 daily"]))
        grid[ph]["own_count_default"] = own["R0 daily"]
        grid[ph]["r0_70_at_252"] = round(E.table(Xm, dm)["R0 daily"][70], 2)
        grid[ph]["r0_70_at_own_count"] = round(Town["R0 daily"][70], 2)
        grid[ph]["own_count_golden"] = sorted({c for n, c in own.items() if E.GOLDEN(n)}, key=lambda x: (x is None, x))
        Xd = np.delete(X, sorted(drop), axis=0)
        dd = [d for k, d in enumerate(dates) if k not in set(drop)]
        ok(len(Xd) < 505, "%s, the days deleted instead of merged: %d one-day periods no longer divide the two years"
           % (ph, len(Xd)))
        cd, Td = LD.calls_on(Xd, dd)
        grid[ph]["deleted"] = dict(default=cd["R0 daily"], r0_70=round(Td["R0 daily"][70], 2),
                                   golden=sorted({c for n, c in cd.items() if E.GOLDEN(n)}, key=lambda x: (x is None, x)))
        if ph == "post-holiday days dropped":
            by, union = {}, set()
            for mk in ("New York", "Tokyo"):
                one = CC.post_holiday_rows(F["cal"], dates, (mk,))
                union |= set(one)
                co, To = LD.calls_on(*LD.merged(X, dates, set(one)))
                by[mk] = dict(dropped=len(one), default=co["R0 daily"], r0_70=round(To["R0 daily"][70], 2))
            ok(union == set(drop), "%s: the New York and Tokyo days (%d and %d) make up the %d"
               % (ph, by["New York"]["dropped"], by["Tokyo"]["dropped"], len(drop)))
            grid[ph]["by_market"] = by
    for s_, r in grid.items():
        if s_ in LD.ACCEPTED:
            continue
        ok(r["default"] != 60, "slip %s: the default does not land on 60 (%s)" % (s_, r["default"]))
    bad = LD.slip_ok(grid)
    ok(not bad, "Layer 1 grid: %s" % bad)
    # the benchmark index file is on the valuation dates (London business days), each index's last close carried on a
    # date it is not calculated, so an inner join of the holdings' prices with it drops no date and the default is 70
    price_dates = [W.WIN_START.isoformat()] + [d.isoformat() for d in dates]
    ix_dates = {nm: list(s["date"]) for nm, s in F["index"].groupby("index_name")}
    ok(len(ix_dates) == 6 and all(dl == price_dates for dl in ix_dates.values()),
       "the index file carries all six indices on each of the %d valuation dates and no other" % len(price_dates))
    joined = sorted(set(v["valuation_date"]) & set.intersection(*(set(dl) for dl in ix_dates.values()))
                    & set.intersection(*(set(F["kest"][f]["Date"].map(lambda x: x.isoformat())) for f in F["kest"])))
    ok(joined == price_dates, "inner join of the holdings' prices with the index file: %d of %d dates kept"
       % (len(joined), len(price_dates)))
    Xj, dj = LD.merged(X, dates, {k for k, d in enumerate(dates) if d.isoformat() not in set(joined)})
    cj, Tj = LD.calls_on(Xj, dj)
    ok(len(Xj) == 505 and cj["R0 daily"] == 70 and abs(Tj["R0 daily"][70] - r0[70]) < 1e-12,
       "inner join with the index file: 505 returns and the default path's 70 (%.2f at 70)" % Tj["R0 daily"][70])
    ok(len(F["index"]) == 6 * len(price_dates), "the index file has %d level rows" % len(F["index"]))
    fig["index_join"] = dict(dates_kept=len(joined), dates=len(price_dates), returns=len(Xj), default=cj["R0 daily"],
                             r0_70=round(Tj["R0 daily"][70], 2))
    fig["slips"] = grid
    sf["SF9"] = grid["distributions left out"]
    ok(sf["SF9"]["default"] == 70 and sf["SF9"]["golden"] == [60], "SF9 distributions left out: same call %s" % sf["SF9"])
    sf["SF12"] = {k: grid[k] for k in ("permanent endowment only", "expendable endowment only", "mandate cash left out")}
    for k in ("permanent endowment only", "expendable endowment only"):
        ok(grid[k]["default"] == 70 and grid[k]["golden"] == [60], "SF12 %s: same call %s" % (k, grid[k]))
    sf["SF13"] = {}
    for py in (250, 252, 253, 260):
        f = np.sqrt(py / 252)
        d0 = call({s: r0[s] * f for s in W.STEPS})
        g0 = sorted({call({s: t[s] * (f if not ("five-day blocks" in n or "calendar" in n) else 1.0) for s in W.STEPS})
                     for n, t in gold.items()})
        sf["SF13"][str(py)] = dict(default=d0, golden=g0)
        ok(d0 == 70 and g0 == [60], "SF13 at %d days a year: %s %s" % (py, d0, g0))
    # periods of several days are refused by policy 4.3 (the returns are daily); recorded: on any count a year they
    # land 60, so a solver who breaks the policy that way files the golden call by a refused route
    wkm = {n: t for n, t in T.items() if E.NOT_DAILY(n) and ("five-day blocks" in n or "calendar" in n)}
    for py in (50.5, 52.0, 52.18):
        f = np.sqrt(py / 52)
        g0 = sorted({call({s: t[s] * f for s in W.STEPS}) for n, t in wkm.items()})
        ok(g0 == [60], "SF11 refused five-day periods at %.2f a year land %s" % (py, g0))

    # SF10 weights drifting from the window's start
    def drifting(Xm, step):
        val_ = E.wvec(step).copy()
        out = []
        for r in Xm:
            out.append((val_ / val_.sum()) @ r)
            val_ = val_ * (1 + r)
        return np.array(out)
    p_d = {s: drifting(X, s) for s in W.STEPS}

    def ll1(p):
        y = p - p.mean()
        return float(np.sqrt(((y * y).sum() + 2 * (y[1:] * y[:-1]).sum()) / (len(y) - 1) * 252) * 100)
    sf["SF10"] = dict(default=call({s: E.vol_of(p_d[s], 252) for s in W.STEPS}), lead_lag=call({s: ll1(p_d[s]) for s in W.STEPS}))
    ok(sf["SF10"]["default"] == 70 and sf["SF10"]["lead_lag"] == 60, "SF10 drifting weights: same call %s" % sf["SF10"])
    # SF11 overlapping twelve-month returns (refused by 4.3)
    sf["SF11"] = dict(overlapping=call({s: E.overlapping_annual(X, s) for s in W.STEPS}),
                      at60=round(E.overlapping_annual(X, 60), 2))
    # SF14 the year the share is for: the calendar year (policy 3.2, procedure 7.1); the estimate's window is the same
    # under any reading of the year, so the call is the same
    sf["SF14"] = dict(default=call(r0), golden=sorted({call(t) for t in gold.values()}), window_end=W.VAL_DATE.isoformat())
    ok(sf["SF14"]["golden"] == [60], "SF14 for 2027: the same window and the same call %s" % sf["SF14"])
    fig["semantic_forks"] = sf
    # the clauses the write-up and the goldens cite resolve in their documents (reduce-house-fixes H8)
    cited = {"policy": ["2.2", "3.4", "4.1", "4.2", "4.3", "4.4", "5.1", "6.1"], "proc": ["7.2", "7.3", "7.4", "7.5", "7.6"]}
    for key, cl in cited.items():
        body = pol if key == "policy" else proc
        for c in cl:
            ok(re.search(r"(^|\s)%s [A-Z]" % re.escape(c), body) is not None, "cited clause %s is in %s" % (c, FL.FILES[key]))
    fig["cited_clauses"] = {"investment_policy": [float(c) for c in cited["policy"]],
                            "finance_procedure_7": [float(c) for c in cited["proc"]]}

    # clean-data test: the generator's own returns, before any export rounding or Layer 1 device
    import build as BLD
    M, fp, B, Xs, ds, g, i, p = BLD.world()
    Ts = E.table(Xs, ds)
    ok(call(Ts["R0 daily"]) == 70 and all(call(t) == 60 for n, t in Ts.items() if E.GOLDEN(n)),
       "clean-data test: the generator's own returns call 70 on the default and 60 on every golden member")
    ok(np.abs(Xs - X).max() < 1e-6, "the pack's returns reproduce the generator's (%.2e)" % np.abs(Xs - X).max())
    # lens swap: the default and the golden read one return matrix, one window, one set of weights; the one-day lead-lag
    # member differs from the default by exactly the portfolio's lag-one autocovariance (the identity's first term)
    pw = X @ E.wvec(60)
    yw = pw - pw.mean()
    gam1 = (yw[1:] * yw[:-1]).sum() / (len(yw) - 1)
    ok(abs((T["G lead-lag 1"][60] ** 2 - r0[60] ** 2) / 1e4 / 252 - 2 * gam1) < 1e-12,
       "lens swap: the golden's one-day lead-lag member is the default plus the lagged covariance on the same returns")
    # separation: scramble every ask-only file and recompute the call's returns
    tmp = tempfile.mkdtemp()
    rng = np.random.default_rng(5)
    F2 = dict(F)
    for k in ("ent", "reg", "inst", "pays"):
        df = F[k].copy()
        for c in df.columns:
            df[c] = rng.permutation(df[c].values)
        F2[k] = df
    X2, d2 = LD.pack_matrix(F2)
    ok(np.array_equal(X2, X), "separation: scrambling the ask-only files leaves the call's returns unchanged")
    F3 = {k: x for k, x in F.items() if k != "index"}
    X3, d3 = LD.pack_matrix(F3)
    ok(np.array_equal(X3, X), "distractor deletion: the call reads no index level, factsheet or manager report")
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ the asks
    running = sum(x for _, x in F["running"])
    capital = sum(x for _, x in F["capital"])
    P = FL.pack_for_asks(F, running, capital, F["kest_isins"])
    inc, info = A.income(P)
    G, parts = A.grant_payments(P)
    rel = A.release(P, inc, G, running)
    t = A.title(inc, G)
    gold_ask = A.figure_vector(inc, G, rel)
    stated = np.array([A.r1000(x) for x in gold_ask])
    labels = ["income %d" % s for s in A.STEPS] + ["grant payments"] + ["release %d" % s for s in A.STEPS]
    for x, r, lb in zip(gold_ask, stated, labels):
        ok(abs(x - r) <= BIN, "golden %s %.0f sits 100 pounds or more inside its bin (%s)" % (lb, x, r))
    # the releases round the same way from rounded parts
    for s in A.STEPS:
        ok(A.r1000(G) + A.r1000(running) - A.r1000(inc[s]) == A.r1000(rel[s]),
           "release %d: rounded parts give the stated figure" % s)
    ok(t is not None and t < 100 and inc[t] - G >= 0.025 * inc[t] and G - inc[t + 10] >= 0.025 * inc[t + 10],
       "title margins of 2.5 per cent of income on each side (title %s)" % t)
    # policy 6.1 and 6.2: the release comes from the expendable endowment, and a cap at its value never binds
    exp_mv = float(P.val[P.val["sub_account"] == "WRX-EX02"]["market_value_gbp"].sum())
    ok(all(30000 <= rel[s] < exp_mv for s in A.STEPS),
       "the golden release is 30,000 pounds or more at every step, and under the expendable endowment's %.2f at "
       "30 November (largest %.2f)" % (exp_mv, max(rel.values())))
    ok(all(np.diff([inc[s] for s in A.STEPS]) < 0), "income falls with the step")
    ok(running % 1000 != 0 and abs(G - round(G, -3)) > 0, "no round headline totals (running costs %d)" % running)
    lags = A.history_lags(P)
    ok(min(lags["later"]) >= 35 and max(lags["later"]) <= 70,
       "project later instalments paid 35 to 70 days after the due date (%s to %s)" % (min(lags["later"]), max(lags["later"])))
    ok(max(lags["core"]) == 0 and max(lags["first"]) == 0 and min(lags["core"]) == 0 and min(lags["first"]) == 0,
       "core and first instalments paid on their due date")
    Gs = {L: A.grant_payments(P, lag=L)[0] for L in range(35, 71)}
    ok(max(Gs.values()) - min(Gs.values()) < 0.005, "C3 corridor: every lag from 35 to 70 days gives the same grant payments")
    for stat in ("median", "mean", "min", "max"):
        Lh = int(round(getattr(np, stat)(lags["later"])))
        ok(abs(A.grant_payments(P, lag=Lh)[0] - G) < 0.005, "C3 corridor: the ledger's %s lag (%d days) gives the golden" % (stat, Lh))
    kinds = A.instalment_kinds(P)
    reg_i = P.reg.set_index("grant_ref")
    corridor_hits = unpaid_early = 0
    for (ref, no, due, amt, stt), kd in zip(P.inst[["grant_ref", "instalment_no", "due_date", "amount", "status"]].itertuples(index=False), kinds):
        d = A.ukdate(due)
        if kd == "later" and GR.in_corridor(d):
            corridor_hits += 1
        if kd == "later" and d < dt.date(2026, 10, 23) and stt == "Scheduled" and reg_i.loc[ref, "status"] != "Withdrawn":
            unpaid_early += 1
    ok(corridor_hits == 0, "no project later instalment falls due in either corridor")
    ok(unpaid_early == 0, "every later instalment due before 23 October 2026 is paid by 30 November")
    awards = [A.ukdate(x) for x in P.reg["award_date"]]
    ok(max(awards) <= dt.date(2026, 11, 20), "C1 procedure 7.4: no grant awarded after 20 November 2026 (%s)" % max(awards))
    # every mishandling the ask sheet prices, alone and composed
    combos = A.stop_combos()
    stops = A.all_stops(P, running, capital, combos)
    worst = (1e18, None, None)
    for key, (i2, g2, r2_, t2) in stops.items():
        vals = A.figure_vector(i2, g2, r2_)
        for x, gv, r, lb in zip(vals, gold_ask, stated, labels):
            if abs(x - gv) < 0.5:
                continue
            if abs(x - r) < worst[0]:
                worst = (abs(x - r), key, lb)
    ok(worst[0] >= STOP, "every mishandling lands %d pounds or more from the stated golden (%.0f at %s, %s)" % (STOP, *worst))
    # the lags 35 and 70 on every instalment
    for L in (35, 70):
        g2 = A.grant_payments(P, True, L, True, True, lag_all=True)[0]
        ok(abs(g2 - A.grant_payments(P, True, 50, True, True, lag_all=True)[0]) < 0.005, "o3 at %d days equals o3 at 50" % L)

    def figs(lines="position", months=12, route="history", clock="lag", conv=True, wout=True, fees=False, acc=False):
        i2 = A.income(P, lines, months, route, acc)[0]
        g2 = A.grant_payments(P, clock != "due", 50, wout, conv, lag_all=clock == "lag_all")[0]
        r2_ = A.release(P, i2, g2, running + (capital if fees else 0))
        return i2, g2, r2_, A.title(i2, g2)
    named = {
        "golden": figs(),
        "s1 cracker (lot lines summed, due dates)": figs(lines="lines", clock="due"),
        "s2 lazy (whole report, funds from the report, due dates, no register)": figs(lines="lines", months=13, route="extract",
                                                                                     clock="due", wout=False, conv=False),
        "o1 dedup on designation, security and ex-date": figs(lines="o1"),
        "o1 keeping the last line": figs(lines="o1_last"),
        "o2 dedup on security and event": figs(lines="o2"),
        "s3 funds from report lines over today's value": figs(route="extract"),
        "o3 lag on every instalment": figs(clock="lag_all"),
        "s4 withdrawn grants kept": figs(wout=False),
        "D6 alone": figs(lines="lines"),
        "D8 alone": figs(clock="due"),
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
    # the cracker sheet: every ask row a miss; the mirror sheet is the same response at R0 (the asks read no estimate)
    cr = fig["stops"]["s1 cracker (lot lines summed, due dates)"]
    ok(cr["income_hits"] == 0 and cr["release_hits"] == 0 and not cr["grants_hit"] and cr["title"] != t,
       "cracker sheet: every ask row a miss %s" % {k: cr[k] for k in ("income_hits", "release_hits", "grants_hit", "title")})
    ok(abs(cr["grant_payments"] - A.r1000(G)) >= STOP, "cracker: the grant payments line misses")
    ok(abs(cr["grant_payments"] + running - A.r1000(G + running)) >= STOP, "cracker: the grants plus running costs line misses")
    ok(fig["stops"]["D6 alone"]["title"] != t and fig["stops"]["D8 alone"]["title"] != t, "D6 alone and D8 alone each move the title")
    # necessity matrix
    nec = {}
    for nm in ("D6 alone", "H1 thirteen months", "accrued income in the value", "s3 funds from report lines over today's value",
               "D8 alone", "s4 withdrawn grants kept", "H3 euro as pounds", "fees counted as running costs"):
        r = fig["stops"][nm]
        nec[nm] = dict(income_moved=9 - r["income_hits"], release_moved=9 - r["release_hits"], grants_moved=not r["grants_hit"])
    fig["necessity"] = nec
    for nm in ("D6 alone", "H1 thirteen months", "s3 funds from report lines over today's value"):
        ok(nec[nm]["income_moved"] == 9 and nec[nm]["release_moved"] == 9, "necessity: %s moves all nine incomes and releases" % nm)
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
    reit = em[em["event_type"] == "Property income distribution"]
    ok(len(reit) > 0, "H2: the REITs' property income distributions are in the report beside their dividends")
    fig["devices"] = dict(lot_inflation=round(infl, 4), position_events_multi_lot=int((multi > 1).sum()),
                          position_events=int(len(multi)), apparent_mandate_yield=round(info["yields"]["MAND"] * (1 + infl), 4))
    # figures the write-up and the goldens state
    fig["portfolio_value"] = round(info["total"], 2)
    fig["mandate_value"] = round(info["mand_mv"], 2)
    fig["fund_values"] = {f: round(x, 2) for f, x in info["fund_mv"].items()}
    fig["yields"] = {h: round(y, 6) for h, y in info["yields"].items()}
    fig["yields_pct"] = {h: round(100 * y, 2) for h, y in info["yields"].items()}
    fig["income"] = {str(s): round(inc[s], 2) for s in A.STEPS}
    fig["income_stated"] = {str(s): A.r1000(inc[s]) for s in A.STEPS}
    fig["grant_payments_2027"] = round(G, 2)
    fig["grant_payments_2027_stated"] = A.r1000(G)
    fig["grant_payments_parts"] = {k: round(x, 2) for k, x in parts.items()}
    fig["running_costs"] = running
    fig["running_costs_stated"] = A.r1000(running)
    fig["grants_plus_running"] = round(G + running, 2)
    fig["grants_plus_running_stated"] = A.r1000(G + running)
    fig["capital_charges"] = capital
    fig["release"] = {str(s): round(rel[s], 2) for s in A.STEPS}
    fig["release_stated"] = {str(s): A.r1000(rel[s]) for s in A.STEPS}
    fig["title_step"] = t
    fig["title_margins"] = dict(above=round(inc[t] - G, 2), below=round(G - inc[t + 10], 2))
    fig["worst_stop"] = round(worst[0], 2)
    fig["lags"] = dict(later_min=min(lags["later"]), later_max=max(lags["later"]), later_n=len(lags["later"]))

    # ------------------------------------------------------------------ documents and realism
    for n in names:
        txt = texts[n]
        if n.endswith(".csv") and n not in (FL.FILES["moves"], FL.FILES["events"], FL.FILES["reg"], FL.FILES["cal"],
                                            FL.FILES["index"]):
            continue
        hits = BANNED.findall(txt)
        ok(not hits, "no stump vocabulary in %s (%s)" % (n, hits[:3]))
        ok("\u2014" not in txt, "no em dash in %s" % n)
        low = txt.lower()
        ok("portfolio volatility" not in low and "expected volatility of" not in low and "correlation" not in low,
           "%s states no portfolio volatility or correlation" % n)
    for n in (FL.FILES["budget"], FL.FILES["proc"], FL.FILES["policy"]):
        ok("2027 grant payments" not in texts[n].lower(), "%s carries no 2027 grant payments total" % n)
    for n in names:
        if not n.endswith(".csv"):
            ok("yield" not in texts[n].lower(), "%s states no yield" % n)
    ok("income" not in texts[FL.FILES["fernside"]].lower(), "Fernside's report shows no income figure")
    rows_per_day = v.groupby("valuation_date").size()
    ok(rows_per_day.nunique() > 3, "the export's rows per day vary")
    pay_month = F["pays"].groupby(F["pays"]["payment_date"].str[:7]).size()
    ok(pay_month.nunique() > 3, "payments per month vary")
    ok(F["reg"]["grantee"].nunique() == len(F["reg"]), "no grantee name repeats")
    ok(abs(info["total"] - round(info["total"], -4)) > 100, "the portfolio value is not round")
    narr = F["moves"]["narrative"].value_counts()
    ok(narr[~narr.index.str.startswith(("Quarterly rebalancing", "Fernside Partners fee"))].max() <= 6,
       "no movement narrative recurs beyond a real rate")
    fees_ = F["moves"][F["moves"]["movement_type"] == "Management fee"]["amount_gbp"].astype(float)
    ok(fees_.nunique() == len(fees_), "no constant stream: every quarterly fee differs")
    fig["checks"] = COUNT[0]
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=False,
                  default=lambda o: o.item() if isinstance(o, (np.integer, np.floating, np.bool_)) else str(o))
        f.write("\n")
    print("checks: %d assertions, %d failed" % (COUNT[0], len(FAILS)))
    return not FAILS


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    sys.exit(0 if main(tgt) else 1)
